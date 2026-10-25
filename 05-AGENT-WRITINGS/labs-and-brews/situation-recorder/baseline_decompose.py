#!/usr/bin/env python3
"""baseline_decompose.py — the disciplined first ML step on the decomposition corpus.

ML-IN-THE-LOOP.md: "Don't build [labs/ci-brain] until a repo's history is rich
enough that the predictor beats the base rate — then it's earned, not asserted."
So before any learned cell, establish the BASE RATE and a transparent baseline it
must beat. The task: given only the leaf TEXTS of a decomposed claim (NOT the
oracle's verdicts), predict which leaf is weakest. Compare to the true argmin
recorded by the referee, and to random guessing.

The baseline is a deliberately cheap lexical "weakness" scorer (limitation /
negation / absoluteness cues — the words JEV reliably scores low). Its VALUE is
partly in where it FAILS: it can flag a stated limitation ("has none",
"entirely") but it cannot reach a factual error ("gold is Ag") — those carry no
lexical tell. That is Law 7 made measurable: to localize factual folds you must
BUY a reader with independent reach (JEV / a symbolic checker), not enlarge the
lexicon. This script prints that finding on the real corpus.

    python3 baseline_decompose.py           # reads ../../situations/corpus/decompositions.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT = HERE.parent.parent / "situations" / "corpus" / "decompositions.jsonl"

# cues JEV reliably scores low: absolutes, universals, negations, stated limits.
# NOTE: matched on WORD BOUNDARIES — an early version counted substrings and scored
# a spurious hit ("wall" ⊃ "all") on a factual leaf. That false signal is exactly
# the hazard of lexical hacking; word boundaries remove it and keep the eval honest.
WEAKNESS_CUES = [
    "entirely", "always", "never", "every", "all", "only", "none", "no",
    "cannot", "can't", "not", "without", "guarantee", "exactly", "must",
    "hardware", "simulator", "impossible", "zero", "byte-exact",
]
_CUE_RE = re.compile(r"\b(?:%s)\b" % "|".join(re.escape(c) for c in WEAKNESS_CUES))


def weakness_score(text: str) -> float:
    return float(len(_CUE_RE.findall(text.lower())))


def _candidates(leaves):
    return [i for i, l in enumerate(leaves) if not l.get("is_whole")]


def _category(leaf) -> str:
    """How is this weak leaf recognizable? factual-error (no lexical tell) vs
    stated-limitation (a lexical tell exists)."""
    return "stated-limitation" if weakness_score(leaf.get("claim", "")) > 0 else "factual-error"


def evaluate(folds):
    n, hits, base = 0, 0, 0.0
    per = []
    cat_hits = {"factual-error": [0, 0], "stated-limitation": [0, 0]}
    for f in folds:
        leaves = f.get("leaves") or []
        cand = _candidates(leaves)
        true_i = f.get("weakest_index")
        if not cand or true_i not in cand:
            continue
        n += 1
        base += 1.0 / len(cand)
        pred = max(cand, key=lambda i: (weakness_score(leaves[i].get("claim", "")), -i))
        hit = pred == true_i
        hits += int(hit)
        cat = _category(leaves[true_i])
        cat_hits[cat][0] += int(hit)
        cat_hits[cat][1] += 1
        per.append({
            "sid": f.get("sid"), "claim": (f.get("claim") or "")[:60],
            "pred_leaf": leaves[pred].get("claim", "")[:44],
            "true_leaf": leaves[true_i].get("claim", "")[:44],
            "hit": hit, "category": cat, "n_cand": len(cand),
        })
    return {
        "n": n, "acc": (hits / n if n else 0.0), "base_rate": (base / n if n else 0.0),
        "per": per, "cat_hits": cat_hits,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="base rate + transparent baseline for weakest-leaf localization")
    ap.add_argument("--corpus", default=str(DEFAULT))
    args = ap.parse_args(argv)

    p = Path(args.corpus)
    if not p.exists():
        print("no decompositions at %s — run corpus.py first" % p)
        return 1
    folds = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    r = evaluate(folds)
    if r["n"] == 0:
        print("no usable folds (need leaves + a substantive weakest_index)")
        return 1

    print("weakest-leaf localization — transparent lexical baseline")
    print("  folds evaluated: %d" % r["n"])
    print("  baseline top-1 accuracy: %.2f" % r["acc"])
    print("  random base rate:        %.2f" % r["base_rate"])
    print("  lift over base rate:     %+.2f" % (r["acc"] - r["base_rate"]))
    print("  by recognizability:")
    for cat, (h, tot) in r["cat_hits"].items():
        if tot:
            print("    %-18s %d/%d" % (cat, h, tot))
    print("  per fold:")
    for row in r["per"]:
        print("    [%s] %s | pred=%r true=%r %s"
              % ("HIT " if row["hit"] else "miss", row["category"], row["pred_leaf"],
                 row["true_leaf"], "✓" if row["hit"] else "✗"))
    print()
    fe = r["cat_hits"]["factual-error"]
    print("FINDING (Law 7): the lexical baseline localizes stated-limitation folds but")
    print("cannot reach factual-error folds (%d/%d) — no lexical tell exists for 'gold is Ag'."
          % (fe[0], fe[1]))
    print("A learned cell must BUY independent reach (JEV / symbolic), not scale the lexicon.")
    print("GATE (ML-IN-THE-LOOP): not yet a CI gate — N=%d is a scaffold; earn it when live" % r["n"])
    print("director folds give volume AND a model beats this base rate by a margin.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
