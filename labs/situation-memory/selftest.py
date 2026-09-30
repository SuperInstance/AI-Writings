#!/usr/bin/env python3
"""selftest.py — situation-memory over the REAL corpus. Stdlib only, offline, no writes.

    python3 selftest.py      # -> "situation-memory selftest: N checks, 0 failures"

Checks: every source transcript replays; the mission index chains from GENESIS and catches
tamper; a planted-near mission ranks ahead of a planted-far one (float AND 4-bit-code mode,
transcript AND text query); same input -> same hits + same fnv1a-64 results_hash; hits carry
distance + outcome; unverified transcripts are refused; the embedder declares itself a
non-semantic stand-in and a different embedder plugs into the same interface.
"""

from __future__ import annotations

import copy
import sys

import situation_memory as sm
from recorder import Situation, verify

CHECKS = {"n": 0, "fail": 0}


def check(name, cond, detail=""):
    CHECKS["n"] += 1
    if not cond:
        CHECKS["fail"] += 1
    print("  %s %s%s" % ("ok  " if cond else "FAIL", name, ("  — " + detail) if detail else ""))


def _clock():
    n = iter(range(1000))
    return lambda: "2026-09-30T00:00:%02dZ" % (next(n) % 60)


def planted(sid, brief, rels):
    """A real recorder-built transcript (chained, verifiable) with the given rel sequence."""
    s = Situation(sid, ts=_clock())
    disp = {"tier": "dispatcher", "id": "selftest", "session": "selftest"}
    cap = {"tier": "captain", "id": "selftest", "session": "selftest"}
    t = s.task(disp, brief)
    last = t["hash"]
    for rel in rels:
        if rel == "ROUTE":
            last = s.route(disp, "verify", to="builder", why="selftest", refs=[last])["hash"]
        elif rel == "MARK":
            last = s.mark(cap, kind="branch", ref="selftest", refs=[last])["hash"]
        elif rel == "FOLD":
            last = s.fold({"tier": "referee", "id": "selftest"}, claim="c",
                          leaves=[{"claim": "whole", "verdict": 0.8, "is_whole": True},
                                  {"claim": "leaf", "verdict": 0.9}], refs=[last])["hash"]
        elif rel == "KEEP":
            last = s.keep(cap, candidate_ref=last, reason="selftest")["hash"]
        elif rel == "DRAW":
            last = s.draw({"tier": "dice", "id": "selftest"}, request="r", value=1,
                          receipt={"note": "selftest"}, refs=[last])["hash"]
        elif rel == "DRAFT":
            last = s.draft({"tier": "crew", "id": "selftest"}, prompt="p", response="r", refs=[last])["hash"]
        elif rel == "OUTCOME":
            last = s.outcome(disp, of_ref=last, result="DONE")["hash"]
    return s.records


def main():
    print("situation-memory selftest (real corpus)")

    # 1. corpus + source-chain verification
    sits, sources = sm.load_corpus()
    live = [s for s in sits if sources[s] == "live"]
    back = [s for s in sits if sources[s] == "backfill"]
    check("real corpus loads (live + backfill)", len(live) >= 1 and len(back) >= 1,
          "%d live, %d backfill" % (len(live), len(back)))
    bad = [sid for sid, recs in sits.items() if not verify(recs)[0]]
    check("every source transcript chain replays", not bad, "%d/%d" % (len(sits) - len(bad), len(sits)))

    # 2. index chain
    idx = sm.build_index()
    ok, msg = idx.verify_chain()
    check("index chain verifies from GENESIS", ok and idx.cells[0]["prev_hash"] == sm.GENESIS, msg)
    check("one mission cell per situation", len(idx.cells) == len(sits), str(len(idx.cells)))
    check("each cell anchors its transcript head hash",
          all(c["transcript_head"] == sits[c["sid"]][-1]["hash"] for c in idx.cells))
    check("fnv1a-64 constants are the fleet's",
          sm.FNV_OFFSET == 0xCBF29CE484222325 and sm.FNV_PRIME == 0x100000001B3
          and sm.GENESIS == "0x0000000000000000" and sm.fnv1a64("") == 0xCBF29CE484222325)

    t = copy.deepcopy(idx)
    t.cells[3]["outcome"] = "DONE" if t.cells[3]["outcome"] != "DONE" else "SCAR"
    check("tamper (edit one cell's outcome) is caught", not t.verify_chain()[0], t.verify_chain()[1])
    t = copy.deepcopy(idx)
    del t.cells[5]
    check("tamper (drop one cell) is caught", not t.verify_chain()[0], t.verify_chain()[1])

    # 3. substrate-style codes retained
    dims = idx.embedder.blocks
    check("4-bit codes retained per block (dim hex nibbles each)",
          all(len(c["codes"][b]) == d for c in idx.cells for b, d in dims.items()))

    # 4. planted near vs far, anchored on a REAL live mission
    anchor_sid = "sit-2026-09-29-syzygy-p1-harvest"
    anchor = sits.get(anchor_sid) or sits[live[0]]
    rels = [r["rel"] for r in anchor][1:]
    brief = sm.task_text(anchor)
    near = planted("planted-near", brief.replace("POC", "prototype"), rels)
    far = planted("planted-far", "Compose a lullaby about tides for the fleet radio night show.",
                  ["DRAFT", "DRAFT", "DRAFT", "DRAW", "DRAW"])
    idx2 = sm.build_index()
    idx2.add(near, "planted")
    idx2.add(far, "planted")
    check("index with planted cells still verifies", idx2.verify_chain()[0])
    ranks = {}
    for mode in ("float", "codes"):
        for qname, q in (("transcript", anchor), ("text", brief)):
            hits = idx2.find_similar_missions(q, k=len(idx2.cells), mode=mode, exclude=[anchor_sid])
            pos = {h["sid"]: h["rank"] for h in hits}
            ranks[(mode, qname)] = (pos["planted-near"], pos["planted-far"])
            check("planted-near ranks ahead of planted-far [%s, %s query]" % (mode, qname),
                  pos["planted-near"] < pos["planted-far"],
                  "near #%d, far #%d of %d" % (pos["planted-near"], pos["planted-far"], len(hits)))
    check("planted-near is the #1 hit for the transcript query (float)",
          ranks[("float", "transcript")][0] == 1, "near #%d" % ranks[("float", "transcript")][0])

    # 5. hit shape: decision-useful
    hits = idx.find_similar_missions(anchor, k=5, exclude=[anchor_sid])
    check("k respected", len(hits) == 5)
    check("hits sorted by distance", [h["distance"] for h in hits] == sorted(h["distance"] for h in hits))
    check("every hit carries distance + outcome class + raw outcome",
          all(isinstance(h["distance"], float) and h["outcome"] in
              {"DONE", "OPEN", "SCAR", "OTHER", "UNLABELED"} and "outcome_raw" in h for h in hits))
    check("exclude drops the query's own mission", all(h["sid"] != anchor_sid for h in hits))

    # 6. determinism
    a = sm.build_index()
    b = sm.build_index()
    check("same corpus -> same index head", a.head() == b.head(), a.head())
    ha = a.find_similar_missions(anchor, k=5, exclude=[anchor_sid])
    hb = b.find_similar_missions(anchor, k=5, exclude=[anchor_sid])
    check("same query -> same hits", ha == hb)
    check("same query -> same fnv1a-64 results_hash", sm.results_hash(ha) == sm.results_hash(hb),
          sm.results_hash(ha))
    tq = "harvest and independently verify a builder cell before booking it"
    check("text query deterministic too",
          sm.results_hash(a.find_similar_missions(tq, 5)) == sm.results_hash(b.find_similar_missions(tq, 5)))

    # 7. outcome classes
    cases = {"DONE": "DONE", "OPEN": "OPEN", "PENDING": "OPEN", "BLOCKED": "SCAR", "ABANDONED": "SCAR",
             "scar-booked": "SCAR", "P1-byte-exact-verified": "DONE",
             "fix-structurally-verified-awaiting-CI": "OPEN", None: "UNLABELED", "FOO": "OTHER"}
    got = {k: sm.classify_outcome(k) for k in cases}
    check("outcome classifier maps DONE/OPEN/SCAR/UNLABELED/OTHER", got == cases,
          "" if got == cases else str({k: v for k, v in got.items() if cases[k] != v}))
    classes = {c["outcome"] for c in idx.cells}
    check("real corpus yields DONE, OPEN and SCAR missions", {"DONE", "OPEN", "SCAR"} <= classes,
          ", ".join(sorted(classes)))

    # 8. refusal + honesty + swappable interface
    tampered = copy.deepcopy(anchor)
    tampered[1]["body"]["why"] = "edited after the fact"
    try:
        sm.MissionIndex().add(tampered)
        refused = False
    except ValueError:
        refused = True
    check("unverified (tampered) transcript is refused", refused)
    check("embedder declares itself a non-semantic stand-in",
          idx.embedder.semantic is False and all(c["semantic"] is False for c in idx.cells))

    class OnlyRel:
        id, semantic, blocks = "selftest/only-rel", False, {"rel": 9}

        def embed(self, records):
            return {"rel": sm.MissionEmbedder().embed(records)["rel"]}

        def embed_text(self, text):
            raise NotImplementedError

    alt = sm.build_index(embedder=OnlyRel())
    ah = alt.find_similar_missions(anchor, k=3, exclude=[anchor_sid])
    check("a different embedder plugs into the same interface",
          alt.verify_chain()[0] and len(ah) == 3 and alt.cells[0]["embedder"] == "selftest/only-rel")

    print("situation-memory selftest: %d checks, %d failures" % (CHECKS["n"], CHECKS["fail"]))
    return 0 if CHECKS["fail"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
