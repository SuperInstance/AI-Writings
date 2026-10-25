#!/usr/bin/env python3
"""forge.py — turn a JEV FOLD into a weighted rubric and one dense scalar reward.

A FOLD record (labs/situation-recorder) already holds a decomposition: the whole
claim (the leaf marked `is_whole`) plus its criteria leaves, each with a verdict
in [0,1]. The corpus labels built from it are thin (a whole verdict, a KEEP/DROP).
rubric-forge adds a WEIGHT per criterion and aggregates {criterion, weight, score}
into one scalar reward in [0,1] — a graded training label, per Rubrics-as-Rewards
(arXiv 2507.17746), where explicit per-criterion rubrics beat a single Likert score.

The whole-claim leaf is the thing being graded, not a criterion: it is carried
through as `whole_verdict` (the thin label) for comparison, and only used as the
reward when a fold has no criteria at all (the degenerate case).

THE SCHEME (fixed, documented, never tuned per instance)

  weights    VERDICT-BLIND. A weight never looks at any score, so the grader cannot
             buy reward by moving weight onto the leaves that scored well, and
             monotonicity holds by construction. Sources, first match wins:
               1. leaf["weight"]  (a number > 0, written by whoever built the fold)
               2. leaf["importance"] in RaR categories:
                    essential 1.0 · important 0.7 · optional 0.3
               3. --jev: JEV scores "is this criterion ESSENTIAL to the whole
                  claim holding?" from the claim texts ONLY (no verdicts), and
                  w = 0.25 + 0.75 * noul, so no criterion drops out entirely
               4. fallback: uniform, w = 1  (the offline default)

  aggregate  weighted power mean, p = -1 (weighted harmonic mean):
                 R = ( sum w_i * s_i^p / sum w_i ) ^ (1/p)
             A conjunction is capped by its weakest conjunct: the recorder's
             folded_min is the p -> -inf end, RaR's weighted average is p = 1.
             p = -1 sits between them: still graded (dense) but one failed
             criterion dominates (0.01 among 0.98s gives ~0.03, not ~0.64). Any
             fixed p gives: monotone in every s_i, min <= R <= max, and
             R = v when every criterion scores v. A zero score gives R = 0.

  influence  per criterion, its share of dR/ds_i (proportional to w_i * s_i^(p-1)):
             how much raising this leaf would move the reward. For p = -1 that is
             w_i / s_i^2, so the weak leaves carry the reward's gradient. This is
             the "how much the leaf moves the whole" signal, kept as a diagnostic
             so it never feeds back into the weights.

Zero dependencies (stdlib). Run directly over the real transcripts:

    python3 forge.py                       # table: transcript -> reward vs whole vs min
    python3 forge.py --json                # one rubric record per FOLD, JSONL
    python3 forge.py --calibrate           # best-fit p against whole verdicts (a diagnostic)
    python3 forge.py --jev                 # JEV importance weights (cached in jev_weights.json;
                                           #   live TYPESAFEAI_KEY calls only fill cache misses)
    python3 forge.py path/to/t.jsonl ...   # specific transcripts
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "situation-recorder"))
from recorder import _canon, fnv1a64  # noqa: E402  (same hash idiom as the corpus)

DEFAULT_IN = HERE.parent.parent / "situations" / "transcripts"
P = -1.0
IMPORTANCE = {"essential": 1.0, "important": 0.7, "optional": 0.3}
JEV_FLOOR = 0.25
ROUND = 6
JEV_CACHE = HERE / "jev_weights.json"  # committed: makes --jev reproducible offline

JEV_URL = "https://api.typesafe.ai/v1/systemone"
# Cloudflare error-1010 blocks non-browser fingerprints; a browser UA is load-bearing.
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"


def power_mean(scores, weights, p=P):
    """Weighted power mean of scores in [0,1]. Monotone in every score for any p."""
    total = sum(weights)
    if total <= 0:
        raise ValueError("weights must sum to > 0")
    if p == 0:  # the geometric-mean limit
        if any(s == 0 for s, w in zip(scores, weights) if w > 0):
            return 0.0
        import math
        return math.exp(sum(w * math.log(s) for s, w in zip(scores, weights)) / total)
    if p < 0 and any(s == 0 for s, w in zip(scores, weights) if w > 0):
        return 0.0  # the limit: a zeroed criterion zeroes a conjunctive mean
    return (sum(w * s ** p for s, w in zip(scores, weights)) / total) ** (1.0 / p)


def influence(scores, weights, p=P):
    """Normalized gradient shares: each criterion's share of dR/ds_i."""
    if p < 1 and any(s == 0 for s in scores):
        zs = [w if s == 0 else 0.0 for s, w in zip(scores, weights)]
        t = sum(zs)
        return [z / t for z in zs]
    g = [w * s ** (p - 1) for s, w in zip(scores, weights)]
    t = sum(g)
    return [x / t for x in g] if t > 0 else [1.0 / len(g)] * len(g)


def _static_weight(leaf):
    """Weight from the leaf itself, or None to defer. Never reads the verdict."""
    if "weight" in leaf:
        w = float(leaf["weight"])
        if w <= 0:
            raise ValueError(f"criterion weight must be > 0: {leaf.get('claim')!r}")
        return w, "leaf.weight"
    imp = leaf.get("importance")
    if imp is not None:
        if imp not in IMPORTANCE:
            raise ValueError(f"importance must be one of {sorted(IMPORTANCE)}: {imp!r}")
        return IMPORTANCE[imp], f"importance:{imp}"
    return None


def jev_importance(whole_claim, criterion, key):
    """One verdict-blind JEV noul: is this criterion essential to the whole claim?"""
    body = {
        "model": "jev-latest",
        "state": f'Compound claim: "{whole_claim}"\nCriterion: "{criterion}"',
        "questions": {"essential": {
            "type": "noul",
            "question": "If this criterion failed, would the compound claim fail?",
            "criteria": {
                "true": "the criterion is essential: the compound claim cannot hold without it",
                "false": "the criterion is peripheral: the compound claim mostly holds without it",
            },
        }},
    }
    req = urllib.request.Request(
        JEV_URL, data=json.dumps(body).encode(), method="POST",
        headers={"authorization": f"Bearer {key}", "content-type": "application/json",
                 "user-agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return float(json.loads(r.read())["answers"]["essential"]["noul"])


def cached_jev_weigher(key, cache_path=JEV_CACHE):
    """JEV importance, served from the committed cache; live calls only fill misses
    (and are written back). Keyed by fnv1a64 of the two claim texts — no verdicts."""
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}

    def weigher(whole_claim, criterion):
        k = "0x%016x" % fnv1a64(_canon({"claim": whole_claim, "criterion": criterion}))
        if k not in cache:
            if not key:
                raise SystemExit(f"--jev cache miss for {criterion!r} and TYPESAFEAI_KEY unset")
            cache[k] = {"criterion": criterion, "noul": jev_importance(whole_claim, criterion, key),
                        "model": "jev-latest"}
            cache_path.write_text(json.dumps(cache, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
        return float(cache[k]["noul"])

    return weigher


def forge(fold, p=P, weigher=None):
    """FOLD body (or a whole FOLD record) -> rubric record with a dense reward.

    `weigher(whole_claim, criterion_claim) -> float in [0,1]` is an optional
    verdict-blind importance oracle (e.g. JEV); it is only consulted for leaves
    that carry no weight/importance of their own. Without it: uniform weights.
    """
    body = fold.get("body", fold)
    leaves = body.get("leaves") or []
    whole = None
    criteria = []
    for leaf in leaves:
        if leaf.get("is_whole"):
            whole = float(leaf["verdict"])
        else:
            criteria.append(leaf)
    claim = body.get("claim")

    rubric, sources = [], set()
    for leaf in criteria:
        s = float(leaf["verdict"])
        if not 0.0 <= s <= 1.0:
            raise ValueError(f"verdict out of [0,1]: {s}")
        sw = _static_weight(leaf)
        if sw is None and weigher is not None:
            sw = (JEV_FLOOR + (1 - JEV_FLOOR) * weigher(claim, leaf.get("claim")), "jev:essential")
        if sw is None:
            sw = (1.0, "uniform")
        rubric.append({"criterion": leaf.get("claim"), "weight": sw[0], "score": s})
        sources.add(sw[1].split(":")[0])

    if rubric:
        scores = [r["score"] for r in rubric]
        weights = [r["weight"] for r in rubric]
        reward = power_mean(scores, weights, p)
        for r, inf in zip(rubric, influence(scores, weights, p)):
            r["influence"] = round(inf, ROUND)
        wsum = sum(weights)
        for r in rubric:
            r["weight"] = round(r["weight"] / wsum, ROUND)  # normalized; sums to ~1
        basis = "criteria"
    elif whole is not None:
        reward, basis = whole, "whole-only"
    else:
        raise ValueError("fold has neither criteria nor a whole verdict")

    reward = round(min(1.0, max(0.0, reward)), ROUND)
    out = {
        "claim": claim,
        "rubric": rubric,
        "reward": reward,
        "whole_verdict": whole,
        "folded_min": min((r["score"] for r in rubric), default=whole),
        "delta_vs_whole": None if whole is None else round(reward - whole, ROUND),
        "scheme": {"aggregate": "weighted-power-mean", "p": p, "basis": basis,
                   "weights": "+".join(sorted(sources)) or "n/a"},
    }
    out["rubric_hash"] = "0x%016x" % fnv1a64(_canon({k: out[k] for k in ("claim", "rubric", "reward", "scheme")}))
    return out


def iter_folds(paths):
    for path in paths:
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                rec = json.loads(line)
                if rec.get("rel") == "FOLD":
                    yield Path(path), rec


def calibrate(folds, grid=None):
    """Diagnostic: which fixed p best reproduces the referees' whole verdicts?"""
    grid = grid or [x / 4 for x in range(-16, 5)]  # -4.0 .. 1.0
    best = None
    for p in grid:
        err = 0.0
        for _, rec in folds:
            f = forge(rec, p=p)
            if f["whole_verdict"] is not None:
                err += (f["reward"] - f["whole_verdict"]) ** 2
        if best is None or err < best[1]:
            best = (p, err)
    return best


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--json", action="store_true", help="emit one rubric record per FOLD")
    ap.add_argument("--calibrate", action="store_true", help="best-fit p vs whole verdicts")
    ap.add_argument("--jev", action="store_true", help="JEV importance weights (TYPESAFEAI_KEY)")
    ap.add_argument("-p", type=float, default=P, help="power-mean exponent (default -1)")
    a = ap.parse_args(argv)

    paths = a.paths or sorted(str(x) for x in DEFAULT_IN.glob("*.jsonl"))
    folds = list(iter_folds(paths))

    weigher = None
    if a.jev:
        weigher = cached_jev_weigher(os.environ.get("TYPESAFEAI_KEY", "").strip())

    if a.calibrate:
        p, err = calibrate(folds)
        print(f"best-fit p vs whole verdicts over {len(folds)} folds: p={p} (SSE {err:.4f})")
        print(f"shipped p={P} (SSE {calibrate(folds, [P])[1]:.4f})")
        return

    rows = []
    for path, rec in folds:
        out = forge(rec, p=a.p, weigher=weigher)
        out["sid"], out["fold_hash"] = rec["sid"], rec["hash"]
        rows.append((path, out))

    if a.json:
        for _, out in rows:
            print(json.dumps(out, ensure_ascii=False, sort_keys=True))
        return

    print(f"{'sid':<40} {'n':>2} {'whole':>6} {'min':>6} {'mean':>6} {'REWARD':>7} {'weights':<8}")
    for _, o in sorted(rows, key=lambda r: r[1]["reward"]):
        mean = sum(r["score"] * r["weight"] for r in o["rubric"]) if o["rubric"] else o["reward"]
        print(f"{o['sid']:<40} {len(o['rubric']):>2} {o['whole_verdict']:>6.2f} "
              f"{o['folded_min']:>6.2f} {mean:>6.3f} {o['reward']:>7.3f} {o['scheme']['weights']:<8}")


if __name__ == "__main__":
    main()
