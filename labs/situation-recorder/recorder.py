#!/usr/bin/env python3
"""recorder.py — turn a manager↔crew situation into a hash-chained transcript.

The fleet's real product is not only the repos a crew ships; it is the
*recorded inputs and outputs of the manager↔crew system* — a decomposable
corpus so a future model can learn to do what the manager does: take a
compound thing apart, locate where the value/truth lives, recombine. See
situations/arch/INTER-RELATIONAL-INTELLIGENCE.md for the why.

This is that capture unit, made small and reusable. One SITUATION is one
manager+crew mission (a dispatch). Its transcript is an append-only JSONL
receipt ledger — the SAME idiom github.com/SuperInstance/MicroMoth-quilt uses
for quantum circuits: every line a cell, fnv1a-64 chained, tamper-evident,
replayable. The hash algebra here is byte-compatible with that repo's
tools/collapse_ledger.py on purpose (one fewer idiom to invent; one more
relationship made explicit between two cells of the fleet).

Each line is a RELATION-record (the graph edges are its `refs`):

    envelope: sid, seq, ts, actor{tier,id,session}, rel, refs[], hash
    rel ∈ TASK ROUTE DRAFT DRAW FOLD KEEP DROP MARK OUTCOME

Zero dependencies (Python stdlib only), like micromoth.py. Run it directly for
a self-test that builds a demo situation and re-verifies the whole chain:

    python3 recorder.py            # -> writes example_situation.jsonl, verifies, prints OK
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

GENESIS = "0x0000000000000000"
REL_TYPES = {"TASK", "ROUTE", "DRAFT", "DRAW", "FOLD", "KEEP", "DROP", "MARK", "OUTCOME"}


def fnv1a64(s: str) -> int:
    """fnv1a-64 over utf-8 — the fleet WAL convention (matches MicroMoth-quilt)."""
    h = 0xCBF29CE484222325
    for b in s.encode("utf-8"):
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Situation:
    """An append-only, hash-chained transcript of one manager↔crew mission.

    The chain rule mirrors MicroMoth-quilt's cell id: each record's `hash` is
    fnv1a-64 over the canonical encoding of {prev, envelope-without-hash}. So
    the transcript is replayable: recompute the chain from the bodies and it
    must reproduce every hash, or the ledger was tampered with.
    """

    def __init__(self, sid: str, ts=None):
        self.sid = sid
        self.records: list[dict] = []
        self._clock = ts  # optional callable for deterministic timestamps (tests)

    # --- core ---------------------------------------------------------------

    def emit(self, rel: str, actor: dict, body: dict, refs=None) -> dict:
        """Append one relation-record and return it (with its computed hash)."""
        if rel not in REL_TYPES:
            raise ValueError("unknown rel %r (allowed: %s)" % (rel, sorted(REL_TYPES)))
        if not isinstance(actor, dict) or "tier" not in actor:
            raise ValueError("actor must be a dict with at least a 'tier' key")
        prev = self.records[-1]["hash"] if self.records else GENESIS
        rec = {
            "sid": self.sid,
            "seq": len(self.records),
            "ts": (self._clock() if self._clock else _now()),
            "actor": actor,
            "rel": rel,
            "refs": list(refs or []),
            "body": body,
        }
        rec["hash"] = "0x%016x" % fnv1a64(_canon({"prev": prev, **_envelope(rec)}))
        self.records.append(rec)
        return rec

    # --- typed convenience verbs (the inter-relational primitives) ----------

    def task(self, actor, brief, refs=None):
        return self.emit("TASK", actor, {"brief": brief}, refs)

    def route(self, actor, subtask, to, why, refs=None):
        return self.emit("ROUTE", actor, {"subtask": subtask, "to": to, "why": why}, refs)

    def draft(self, actor, prompt, response, params=None, refs=None):
        return self.emit("DRAFT", actor,
                         {"prompt": prompt, "response": response, "params": params or {}}, refs)

    def draw(self, actor, request, value, receipt, refs=None):
        """An un-gameable draw. `receipt` carries provenance: a Moth Bell-S, OR a
        MicroMoth-quilt collapse-ledger id when drawing locally in-environment."""
        return self.emit("DRAW", actor,
                         {"request": request, "value": value, "receipt": receipt}, refs)

    def fold(self, actor, claim, leaves, refs=None):
        """The decomposition record. `leaves` is a list of {claim, verdict}. We store
        the located weakest (argmin) and the GAP the single number would have hidden —
        the datum that teaches how much a scalar verdict smoothed over."""
        if not leaves:
            raise ValueError("fold needs at least one leaf")
        verdicts = [float(l["verdict"]) for l in leaves]
        argmin = min(range(len(leaves)), key=lambda i: verdicts[i])
        folded = min(verdicts)  # the weakest leaf is the honest ceiling of the conjunction
        whole = None
        for l in leaves:
            if l.get("is_whole"):
                whole = float(l["verdict"])
        body = {
            "claim": claim,
            "leaves": leaves,
            "weakest_index": argmin,
            "weakest_claim": leaves[argmin].get("claim"),
            "folded_min": folded,
            "whole_verdict": whole,
            "gap": (None if whole is None else round(folded - whole, 6)),
        }
        return self.emit("FOLD", actor, body, refs)

    def keep(self, actor, candidate_ref, reason, refs=None):
        r = list(refs or [])
        if candidate_ref not in r:
            r.append(candidate_ref)
        return self.emit("KEEP", actor, {"candidate": candidate_ref, "reason": reason}, r)

    def drop(self, actor, candidate_ref, reason, refs=None):
        r = list(refs or [])
        if candidate_ref not in r:
            r.append(candidate_ref)
        return self.emit("DROP", actor, {"candidate": candidate_ref, "reason": reason}, r)

    def mark(self, actor, kind, ref, refs=None):
        """A durable artifact written (commit sha / doc path / receipt id)."""
        return self.emit("MARK", actor, {"kind": kind, "ref": ref}, refs)

    def outcome(self, actor, of_ref, result, detail=None, refs=None):
        """A realized downstream result (CI green/red, revert, measured speedup) —
        the delayed label. `of_ref` points back at the record it judges."""
        r = list(refs or [])
        if of_ref not in r:
            r.append(of_ref)
        return self.emit("OUTCOME", actor, {"of": of_ref, "result": result, "detail": detail}, r)

    # --- persistence + verification ----------------------------------------

    def to_jsonl(self) -> str:
        return "".join(_canon(r) + "\n" for r in self.records)

    def write(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(self.to_jsonl(), encoding="utf-8")
        return path


def _envelope(rec: dict) -> dict:
    """The record without its own hash — what the chain commits to."""
    return {k: v for k, v in rec.items() if k != "hash"}


def verify(records) -> tuple[bool, str]:
    """Replay the chain. Returns (ok, message). Catches reorder, edit, and drop —
    the same tamper-evidence MicroMoth-quilt gives a circuit ledger."""
    prev = GENESIS
    for i, rec in enumerate(records):
        if rec.get("seq") != i:
            return False, "seq gap at index %d (got %r)" % (i, rec.get("seq"))
        want = "0x%016x" % fnv1a64(_canon({"prev": prev, **_envelope(rec)}))
        if rec.get("hash") != want:
            return False, "hash mismatch at seq %d: stored %s want %s" % (
                i, rec.get("hash"), want)
        for ref in rec.get("refs", []):
            if isinstance(ref, str) and ref.startswith("0x") and ref not in {
                    r["hash"] for r in records[:i]}:
                return False, "seq %d refs unknown/forward hash %s" % (i, ref)
        prev = rec["hash"]
    return True, "ok: %d records, chain intact" % len(records)


def load(path) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line]


# --- self-test / demo -------------------------------------------------------

def _demo() -> Situation:
    """Build a small but real-shaped situation: a captain routes a claim-check to a
    crew member, draws an adversary locally (MicroMoth-quilt), folds the crew's
    compound claim through the referee, drops it on the located weakest leaf, and
    books the scar. Deterministic timestamps so the demo file is reproducible."""
    ticks = iter(["2026-09-29T05:20:%02dZ" % s for s in range(0, 40, 3)])
    s = Situation("sit-demo-0001", ts=lambda: next(ticks))
    disp = {"tier": "dispatcher", "id": "opus-4.8", "session": "parent"}
    cap = {"tier": "captain", "id": "opus-5.5", "session": "fresh-01"}
    crew = {"tier": "crew", "id": "deepseek-chat", "session": "fresh-01"}
    ref = {"tier": "referee", "id": "jev-latest", "session": "fresh-01"}
    dice = {"tier": "dice", "id": "micromoth-quilt/bell", "session": "fresh-01"}

    t = s.task(disp, "Verify the crew's anatomy claim before it lands in a README.")
    r = s.route(cap, "fact-check compound claim", to="deepseek-chat",
                why="cheap hauler; captain reserves judgment for the fold", refs=[t["hash"]])
    d = s.draft(crew,
                prompt="State four facts about the human heart.",
                response=("four chambers; pumps blood; contains the SA node; "
                          "located entirely on the left side of the chest"),
                refs=[r["hash"]])
    dr = s.draw(dice, request="draw adversary leaf index in [0,4)",
                value=3,
                receipt={"collapse_ledger": "0x… (micromoth-quilt bell, local, no network)",
                         "note": "un-gameable in-env: quantum-shaped, nobody steered it"},
                refs=[d["hash"]])
    f = s.fold(ref,
               claim="the heart claim (compound)",
               leaves=[
                   {"claim": "the compound claim as a whole", "verdict": 0.11, "is_whole": True},
                   {"claim": "four chambers", "verdict": 0.98},
                   {"claim": "pumps blood through the body", "verdict": 0.97},
                   {"claim": "contains the SA node that sets rhythm", "verdict": 0.95},
                   {"claim": "located entirely on the left side of the chest", "verdict": 0.08},
               ],
               refs=[d["hash"], dr["hash"]])
    dp = s.drop(cap, candidate_ref=d["hash"],
                reason=("fold located the rot at leaf 3 (left-side), the same leaf the "
                        "un-gameable draw hit; whole-verdict 0.11 hid WHERE — gap %.2f"
                        % f["body"]["gap"]),
                refs=[f["hash"]])
    m = s.mark(cap, kind="ledger", ref="dispatch-ledger.csv#d121", refs=[dp["hash"]])
    s.outcome(disp, of_ref=m["hash"], result="scar-booked",
              detail="claim kept OUT of the README; transcript retained as a FOLD example",
              refs=[f["hash"]])
    return s


def main(argv=None):
    ap = argparse.ArgumentParser(description="situation-recorder self-test / verifier")
    ap.add_argument("--verify", metavar="PATH", help="verify an existing transcript JSONL")
    ap.add_argument("--out", default=str(Path(__file__).with_name("example_situation.jsonl")),
                    help="where the demo writes its transcript")
    args = ap.parse_args(argv)

    if args.verify:
        ok, msg = verify(load(args.verify))
        print(("VERIFY OK  — " if ok else "VERIFY FAIL — ") + msg)
        return 0 if ok else 1

    s = _demo()
    path = s.write(args.out)
    ok, msg = verify(s.records)
    assert ok, msg
    # tamper check: flipping one field must break the chain downstream
    bad = load(path)
    bad[3]["body"]["value"] = 0
    tampered_ok, _ = verify(bad)
    assert not tampered_ok, "tamper went undetected — chain is not doing its job"
    print("wrote %s (%d records)" % (path, len(s.records)))
    print(msg)
    print("tamper-evidence: editing seq 3 breaks verification ✓")
    w = s.records[4]["body"]
    print("demo FOLD located weakest = leaf %d (%r), gap vs whole = %s"
          % (w["weakest_index"], w["weakest_claim"], w["gap"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
