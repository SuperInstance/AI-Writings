#!/usr/bin/env python3
"""corpus.py — turn a pile of situation-transcripts into model-ready tables.

The transcripts (situations/transcripts/) are the saved manager↔crew system.
This reader is the bridge from "we saved it" to "here is the training set": it
verifies every chain, groups records into situations (a file may be a single
situation OR a bundle of many, each chained from GENESIS by its own `sid`), and
emits the three tables a future model learns from — the ones named in
situations/arch/{INTER-RELATIONAL-INTELLIGENCE,ML-IN-THE-LOOP}.md:

  decompositions.jsonl  every FOLD → claim, leaves, weakest(argmin), gap        (learn to DECOMPOSE)
  routes.jsonl          every ROUTE → subtask, to, why, + reachable OUTCOME     (learn to ROUTE)
  judgments.jsonl       every KEEP/DROP → candidate, reason, kept, + OUTCOME     (the value function)

Zero dependencies (stdlib). Run directly to (re)build the tables + print a report:

    python3 corpus.py                       # reads ../../situations/transcripts, writes ../../situations/corpus
    python3 corpus.py --dir D --out O
"""

from __future__ import annotations

import argparse
import json
from collections import OrderedDict, defaultdict
from pathlib import Path

from recorder import verify  # same chain rule as the writer

HERE = Path(__file__).resolve().parent
DEFAULT_IN = HERE.parent.parent / "situations" / "transcripts"
DEFAULT_OUT = HERE.parent.parent / "situations" / "corpus"


def _iter_records(transcript_dir: Path):
    for path in sorted(transcript_dir.rglob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                yield path, json.loads(line)


def load_situations(transcript_dir: Path) -> "OrderedDict[str, list]":
    """Group all records by sid (order preserved). A file may hold one situation
    or a bundle of many; grouping by sid recovers each independent chain."""
    sits: "OrderedDict[str, list]" = OrderedDict()
    for _path, rec in _iter_records(transcript_dir):
        sits.setdefault(rec["sid"], []).append(rec)
    for sid, recs in sits.items():
        recs.sort(key=lambda r: r["seq"])
    return sits


def verify_all(sits) -> tuple[int, list]:
    ok = 0
    bad = []
    for sid, recs in sits.items():
        good, msg = verify(recs)
        if good:
            ok += 1
        else:
            bad.append((sid, msg))
    return ok, bad


def _by_hash(recs):
    return {r["hash"]: r for r in recs}


def _reachable_outcome(recs, from_hash):
    """First OUTCOME whose refs (transitively) include from_hash — the realized
    label for a route/judgment. Simple forward scan is enough for these chains."""
    idx = _by_hash(recs)
    for r in recs:
        if r["rel"] != "OUTCOME":
            continue
        seen, stack = set(), list(r.get("refs", []))
        while stack:
            h = stack.pop()
            if h in seen:
                continue
            seen.add(h)
            if h == from_hash:
                return r["body"].get("result")
            ref = idx.get(h)
            if ref:
                stack.extend(ref.get("refs", []))
    return None


def build_tables(sits):
    decompositions, routes, judgments = [], [], []
    for sid, recs in sits.items():
        for r in recs:
            b = r.get("body", {})
            if r["rel"] == "FOLD":
                decompositions.append({
                    "sid": sid, "actor": r["actor"].get("id"),
                    "claim": b.get("claim"), "n_leaves": len(b.get("leaves", [])),
                    "weakest_index": b.get("weakest_index"),
                    "weakest_claim": b.get("weakest_claim"),
                    "folded_min": b.get("folded_min"), "whole_verdict": b.get("whole_verdict"),
                    "gap": b.get("gap"), "leaves": b.get("leaves"),
                })
            elif r["rel"] == "ROUTE":
                routes.append({
                    "sid": sid, "actor": r["actor"].get("id"),
                    "subtask": b.get("subtask"), "to": b.get("to"), "why": b.get("why"),
                    "outcome": _reachable_outcome(recs, r["hash"]),
                })
            elif r["rel"] in ("KEEP", "DROP"):
                judgments.append({
                    "sid": sid, "actor": r["actor"].get("id"), "kept": r["rel"] == "KEEP",
                    "candidate": b.get("candidate"), "reason": b.get("reason"),
                    "outcome": _reachable_outcome(recs, r["hash"]),
                })
    return {"decompositions": decompositions, "routes": routes, "judgments": judgments}


def _write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows), encoding="utf-8")


def report(sits, tables) -> str:
    n_rec = sum(len(r) for r in sits.values())
    rel_counts = defaultdict(int)
    provenance = defaultdict(int)
    for recs in sits.values():
        for r in recs:
            rel_counts[r["rel"]] += 1
            provenance[r.get("body", {}).get("provenance", r["actor"].get("tier"))] += 1
    dec = tables["decompositions"]
    gaps = [d["gap"] for d in dec if d.get("gap") is not None]
    routes = tables["routes"]
    route_out = defaultdict(int)
    for r in routes:
        route_out[r["outcome"] or "unlabeled"] += 1
    lines = []
    lines.append("situations: %d   records: %d" % (len(sits), n_rec))
    lines.append("relation mix: " + ", ".join("%s=%d" % (k, rel_counts[k]) for k in sorted(rel_counts)))
    lines.append("decompositions (FOLD): %d" % len(dec))
    if gaps:
        lines.append("  gap (folded_min − whole): min=%.3f mean=%.3f max=%.3f  (how much a scalar hid)"
                     % (min(gaps), sum(gaps) / len(gaps), max(gaps)))
    lines.append("routes: %d   outcome mix: %s" % (
        len(routes), ", ".join("%s=%d" % (k, route_out[k]) for k in sorted(route_out))))
    lines.append("judgments: %d (kept=%d dropped=%d)" % (
        len(tables["judgments"]),
        sum(1 for j in tables["judgments"] if j["kept"]),
        sum(1 for j in tables["judgments"] if not j["kept"])))
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="build model-ready tables from situation-transcripts")
    ap.add_argument("--dir", default=str(DEFAULT_IN))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args(argv)

    sits = load_situations(Path(args.dir))
    if not sits:
        print("no transcripts found under %s" % args.dir)
        return 1
    ok, bad = verify_all(sits)
    if bad:
        print("CHAIN VERIFY FAILED for %d situation(s):" % len(bad))
        for sid, msg in bad:
            print("  %s: %s" % (sid, msg))
        return 2
    tables = build_tables(sits)
    out = Path(args.out)
    for name, rows in tables.items():
        _write_jsonl(out / (name + ".jsonl"), rows)
    print("all %d chains verified ✓" % ok)
    print(report(sits, tables))
    print("wrote tables to %s/" % out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
