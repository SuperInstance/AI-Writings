#!/usr/bin/env python3
"""ledger_to_transcript.py — backfill the corpus from the dispatch-ledger.

ML-IN-THE-LOOP.md: "the dispatch-ledger is a decision log … a (state, action,
outcome) tuple … an RL trajectory, already booked." So the fleet's own recent
history is corpus we already have — we just never wrote it in the transcript
shape. This transcodes each ledger row into a small situation-transcript:

    TASK    ← task (what was asked)
    ROUTE   ← tier/model (who it was handed to) + serves_gap (the why)
    MARK    ← receipt / booked_up_to (the artifact produced)
    OUTCOME ← status + verdict + the short 'tell'

HONESTY (keeps the corpus clean): these are RECONSTRUCTED from a summary ledger,
not live-captured, and carry NO real FOLD/DRAFT/DRAW (those weren't recorded at
the time). Every backfilled record is stamped provenance="backfill-from-ledger
(reconstructed)". A model must be able to tell a live capture from a
reconstruction, or it will learn from its own shadow. Live transcripts stay the
gold standard; this is honest silver that gives ROUTE→OUTCOME real volume now.

Writes ONE bundle file (many situations, each chained from GENESIS by its sid);
corpus.py groups by sid and verifies each chain independently.

    python3 ledger_to_transcript.py     # -> ../../situations/transcripts/backfill/ledger.jsonl
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from recorder import Situation, verify

HERE = Path(__file__).resolve().parent
DEFAULT_LEDGER = HERE.parent.parent / "situations" / "dispatch-ledger.csv"
DEFAULT_OUT = HERE.parent.parent / "situations" / "transcripts" / "backfill" / "ledger.jsonl"

PROV = "backfill-from-ledger (reconstructed)"


def _clock(when: str):
    # ledger has date granularity only; give each record a stable within-row tick
    n = {"i": 0}

    def tick():
        n["i"] += 1
        return "%sT00:00:%02dZ" % (when, n["i"])
    return tick


def transcode(ledger_path: Path):
    rows = list(csv.DictReader(open(ledger_path, encoding="utf-8")))
    situations = []
    for row in rows:
        did = row["dispatch_id"].strip()
        if not did:
            continue
        s = Situation("ledger-%s" % did, ts=_clock(row.get("booked_at", "2026-01-01")))
        disp = {"tier": "dispatcher", "id": "ledger", "session": "backfill"}
        worker = {"tier": (row.get("tier") or "?").lower(), "id": row.get("model") or "?",
                  "session": "backfill"}

        def body(extra):  # stamp provenance on every reconstructed record
            extra = dict(extra); extra["provenance"] = PROV; return extra

        t = s.emit("TASK", disp, body({"brief": row.get("task", "")[:2000]}))
        r = s.emit("ROUTE", disp, body({
            "subtask": (row.get("serves_gap") or "").strip() or "dispatch",
            "to": row.get("model") or row.get("tier") or "?",
            "why": "handed_down_from=%s cost_class=%s" % (
                row.get("handed_down_from", ""), row.get("cost_class", "")),
        }), refs=[t["hash"]])
        marks = []
        artifact = (row.get("booked_up_to") or "").strip()
        if artifact:
            m = s.emit("MARK", worker, body({"kind": "artifact", "ref": artifact[:500]}),
                       refs=[r["hash"]])
            marks.append(m["hash"])
        status = (row.get("status") or "").strip() or "UNKNOWN"
        s.emit("OUTCOME", disp, body({
            "of": marks[0] if marks else r["hash"],
            "result": status,
            "detail": {"verdict": row.get("verdict"), "standing": row.get("standing"),
                       "tell": (row.get("receipt") or "")[:800]},
        }), refs=(marks or [r["hash"]]))
        situations.append(s)
    return situations


def main(argv=None):
    ap = argparse.ArgumentParser(description="backfill corpus transcripts from the dispatch-ledger")
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args(argv)

    sits = transcode(Path(args.ledger))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines, bad = [], []
    for s in sits:
        ok, msg = verify(s.records)
        if not ok:
            bad.append((s.sid, msg))
        lines.append(s.to_jsonl())
    if bad:
        print("VERIFY FAILED for %d:" % len(bad))
        for sid, msg in bad[:10]:
            print("  %s: %s" % (sid, msg))
        return 2
    out.write_text("".join(lines), encoding="utf-8")
    print("backfilled %d situations (%d records) → %s"
          % (len(sits), sum(len(s.records) for s in sits), out))
    print("all chains verified ✓  provenance stamped: %r" % PROV)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
