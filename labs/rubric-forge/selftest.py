#!/usr/bin/env python3
"""selftest.py — the laws a dense reward must obey, checked offline.

  bounded       0 <= R <= 1, and min(criteria) <= R <= max(criteria)
  monotone      raising any criterion's verdict never lowers R (sweeps every leaf)
  degenerate    all criteria = v  ->  R = v;  no criteria  ->  R = whole verdict
  whole-blind   the is_whole leaf is graded, not a criterion: moving it never moves R
  verdict-blind weights never depend on scores (permuting verdicts keeps weights)
  conjunctive   one zeroed criterion zeroes R; a weak leaf carries the influence
  weights       leaf.weight / RaR importance honored; scale-invariant; bad ones refused
  ordering      the real hermit fold (0.45 weakest) scores below an all-high fold
  reproducible  fixture.json (real FOLD bodies + expected rewards/hashes) re-derives
                byte-identically; two runs agree; the JEV cache serves offline
  corpus        every real transcript chain still verifies (recorder.verify)

Zero network. `python3 selftest.py --regen` rewrites fixture.json expectations
(only after a deliberate scheme change — the diff is then the review surface).
"""

from __future__ import annotations

import copy
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import forge as F  # noqa: E402
from recorder import verify  # noqa: E402  (forge put situation-recorder on the path)

FIXTURE = HERE / "fixture.json"
EPS = 1e-9
checks = 0
failures = []


def check(cond, what):
    global checks
    checks += 1
    if not cond:
        failures.append(what)


def fold(verdicts, whole=0.5, **extra):
    leaves = [{"claim": "whole", "verdict": whole, "is_whole": True}]
    leaves += [{"claim": f"c{i}", "verdict": v, **extra} for i, v in enumerate(verdicts)]
    return {"claim": "synthetic", "leaves": leaves}


def real_folds():
    paths = sorted(str(p) for p in F.DEFAULT_IN.glob("*.jsonl"))
    return list(F.iter_folds(paths))


def regen():
    cases = []
    for path, rec in real_folds():
        cases.append({"name": f"{path.name}:{rec['sid']}", "fold": rec["body"]})
    cases.append({"name": "synthetic:importance", "fold": {"claim": "rubric with RaR categories", "leaves": [
        {"claim": "whole", "verdict": 0.6, "is_whole": True},
        {"claim": "core property holds", "verdict": 0.9, "importance": "essential"},
        {"claim": "docs updated", "verdict": 0.4, "importance": "optional"},
        {"claim": "tests added", "verdict": 0.7, "importance": "important"}]}})
    cases.append({"name": "synthetic:whole-only", "fold": {"claim": "undecomposed", "leaves": [
        {"claim": "whole", "verdict": 0.42, "is_whole": True}]}})
    for c in cases:
        out = F.forge(c["fold"])
        c["expect"] = {"reward": out["reward"], "rubric_hash": out["rubric_hash"]}
    FIXTURE.write_text(json.dumps({"scheme": {"p": F.P}, "cases": cases}, indent=1,
                                  ensure_ascii=False, sort_keys=True) + "\n")
    print(f"wrote {FIXTURE.name}: {len(cases)} cases")


def main():
    rng = random.Random(2507_17746)  # the RaR arXiv id, as a fixed seed

    # ── reproducible from the committed fixture ────────────────────────────────
    fx = json.loads(FIXTURE.read_text())
    check(fx["scheme"]["p"] == F.P, "fixture p matches shipped p")
    for c in fx["cases"]:
        a, b = F.forge(copy.deepcopy(c["fold"])), F.forge(copy.deepcopy(c["fold"]))
        check(a == b, f"deterministic: {c['name']}")
        check(a["reward"] == c["expect"]["reward"], f"fixture reward: {c['name']}")
        check(a["rubric_hash"] == c["expect"]["rubric_hash"], f"fixture hash: {c['name']}")

    # ── laws over the real folds + seeded random folds ─────────────────────────
    bodies = [c["fold"] for c in fx["cases"]]
    for _ in range(40):
        n = rng.randint(1, 7)
        bodies.append(fold([round(rng.random(), 3) for _ in range(n)], whole=round(rng.random(), 3)))

    for body in bodies:
        out = F.forge(body)
        R = out["reward"]
        check(0.0 <= R <= 1.0, f"bounded [0,1]: {body['claim']}")
        crit = [l for l in body["leaves"] if not l.get("is_whole")]
        if not crit:
            continue
        s = [float(l["verdict"]) for l in crit]
        check(min(s) - EPS <= R <= max(s) + EPS, f"within [min,max]: {body['claim']}")
        check(abs(sum(r["weight"] for r in out["rubric"]) - 1) < 1e-5, f"weights normalized: {body['claim']}")
        check(abs(sum(r["influence"] for r in out["rubric"]) - 1) < 1e-5, f"influence sums to 1: {body['claim']}")

        # monotone: sweep every criterion upward in steps
        for i, leaf in enumerate(body["leaves"]):
            if leaf.get("is_whole"):
                continue
            prev = R
            for step in (0.05, 0.2, 0.5, 1.0):
                b2 = copy.deepcopy(body)
                b2["leaves"][i]["verdict"] = min(1.0, float(leaf["verdict"]) + step)
                r2 = F.forge(b2)["reward"]
                check(r2 + EPS >= prev, f"monotone leaf {i} +{step}: {body['claim']}")
                prev = r2

        # whole-blind: the graded thing is not a criterion
        b3 = copy.deepcopy(body)
        for leaf in b3["leaves"]:
            if leaf.get("is_whole"):
                leaf["verdict"] = 1.0 - float(leaf["verdict"])
        check(F.forge(b3)["reward"] == R, f"whole-blind: {body['claim']}")

        # verdict-blind weights: permute verdicts, weights unchanged
        b4 = copy.deepcopy(body)
        vs = [l["verdict"] for l in b4["leaves"] if not l.get("is_whole")]
        rng.shuffle(vs)
        it = iter(vs)
        for leaf in b4["leaves"]:
            if not leaf.get("is_whole"):
                leaf["verdict"] = next(it)
        check([r["weight"] for r in F.forge(b4)["rubric"]] == [r["weight"] for r in out["rubric"]],
              f"verdict-blind weights: {body['claim']}")

    # ── degenerate / equal-weight cases ────────────────────────────────────────
    for v in (0.0, 0.08, 0.45, 0.5, 0.7, 0.99, 1.0):
        for n in (1, 3, 6):
            check(abs(F.forge(fold([v] * n, whole=v))["reward"] - v) < 1e-6, f"all-equal {v} x{n} -> {v}")
        out = F.forge({"claim": "w", "leaves": [{"claim": "w", "verdict": v, "is_whole": True}]})
        check(out["reward"] == v and out["scheme"]["basis"] == "whole-only", f"whole-only -> {v}")
    try:
        F.forge({"claim": "empty", "leaves": []})
        check(False, "empty fold refused")
    except ValueError:
        check(True, "empty fold refused")

    # ── conjunctive behaviour ──────────────────────────────────────────────────
    check(F.forge(fold([0.98, 0.0, 0.94]))["reward"] == 0.0, "a zeroed criterion zeroes R")
    z = F.forge(fold([0.98, 0.0, 0.94]))["rubric"]
    check(z[1]["influence"] == 1.0, "zeroed criterion carries all influence")
    h = F.forge(fold([0.97, 0.96, 0.9, 0.8, 0.45]))
    check(max(h["rubric"], key=lambda r: r["influence"])["score"] == 0.45, "weakest leaf has max influence")
    check(h["reward"] < sum(r["score"] for r in h["rubric"]) / 5, "harmonic below arithmetic mean")
    check(h["reward"] > h["folded_min"], "dense: above the hard min")

    # ── explicit weights ───────────────────────────────────────────────────────
    ess = F.forge({"claim": "x", "leaves": [{"claim": "a", "verdict": 0.2, "importance": "essential"},
                                            {"claim": "b", "verdict": 0.9, "importance": "optional"}]})
    opt = F.forge({"claim": "x", "leaves": [{"claim": "a", "verdict": 0.2, "importance": "optional"},
                                            {"claim": "b", "verdict": 0.9, "importance": "essential"}]})
    check(ess["reward"] < opt["reward"], "essential failing criterion costs more than optional")
    check(ess["scheme"]["weights"] == "importance", "importance source recorded")
    w1 = F.forge({"claim": "x", "leaves": [{"claim": "a", "verdict": 0.3, "weight": 2},
                                           {"claim": "b", "verdict": 0.8, "weight": 1}]})
    w2 = F.forge({"claim": "x", "leaves": [{"claim": "a", "verdict": 0.3, "weight": 20},
                                           {"claim": "b", "verdict": 0.8, "weight": 10}]})
    check(w1["reward"] == w2["reward"], "weights scale-invariant")
    for bad in ({"weight": 0}, {"weight": -1}, {"importance": "vital"}):
        try:
            F.forge({"claim": "x", "leaves": [{"claim": "a", "verdict": 0.5, **bad}]})
            check(False, f"bad weight refused: {bad}")
        except ValueError:
            check(True, f"bad weight refused: {bad}")
    try:
        F.forge(fold([1.2]))
        check(False, "verdict > 1 refused")
    except ValueError:
        check(True, "verdict > 1 refused")

    # ── ordering on the REAL corpus ────────────────────────────────────────────
    by_sid = {}
    for _, rec in real_folds():
        by_sid[rec["sid"]] = F.forge(rec)["reward"]
    hermit = by_sid.get("sit-2026-09-29-hermit-harvest")
    check(hermit is not None, "hermit fold present")
    all_high = F.forge(fold([0.97, 0.96, 0.95, 0.98, 0.96]))["reward"]
    check(hermit < all_high, "hermit (0.45 weakest) < an all-high fold")
    check(by_sid["jev-fold-claimA"] < by_sid["sit-2026-09-29-capture-path"] < hermit,
          "false-fact fold < stated-limitation fold < hermit")
    check(hermit < by_sid["sit-2026-09-29-tool-pin-harvest"], "hermit (0.45) < tool-pin (0.55 weakest)")

    # ── JEV cache serves offline (no key, no network) ──────────────────────────
    if F.JEV_CACHE.exists():
        weigher = F.cached_jev_weigher(key="")
        for _, rec in real_folds():
            out = F.forge(rec, weigher=weigher)
            check(out["scheme"]["weights"] == "jev", f"jev cache offline: {rec['sid']}")
            check(out == F.forge(rec, weigher=weigher), f"jev cache deterministic: {rec['sid']}")

    # ── corpus chains intact ───────────────────────────────────────────────────
    sits = {}
    for p in sorted(F.DEFAULT_IN.glob("*.jsonl")):
        for line in p.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                sits.setdefault(r["sid"], []).append(r)
    for sid, recs in sits.items():
        ok, msg = verify(sorted(recs, key=lambda r: r["seq"]))
        check(ok, f"chain verifies: {sid} ({msg})")

    for f in failures:
        print("FAIL:", f)
    print(f"rubric-forge selftest: {checks} checks, {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    if "--regen" in sys.argv:
        regen()
    else:
        sys.exit(main())
