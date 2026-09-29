"""activeledger (B1) — thin adapter: ActiveLog v1 envelope + three namespaced types.

We do NOT author a record format. The envelope is the internal ActiveLog v1:
    {alv, dev, seq, ts, mono, type, body, fix?, prev?}
append-only, (dev,seq)-keyed, monotonic clock, per-device sha256 `prev` chain.
We only add three namespaced types (ACTIVELEDGER-CELL-GRAPH.md §8):

    cell.tick           a cell's intra-step in its OWN units      (ActiveLog / yin)
    route.hop           balanced double-entry {credit,debit,price} (ActiveLedger / yang)
    ledger.transaction  binds the two sides (+ route total budget)

Every cell.tick and route.hop body carries a BUDGET VECTOR
    {wall_ms, tokens:{api:int}, usd, power_w, mem_mb, storage_bytes:{train,prod}, reqs}
and a route's total budget is the sum of ALL its records' budgets (cell.tick + route.hop);
see route_total() (compute lives on ticks, so hops alone would undercount — matches EX1).

Hashing: fnv1a-64 over canonical JSON (fleet idiom, == situation-recorder) for CONTENT
hashes; sha256 for the per-device `prev` chain (ActiveLog v1 rule).

`emit`/`verify_chain`/`budget`/`add_budget` mirror labs/examples/calculator-quilt/calc_quilt.py
so EX1 can import this module instead of its inline stand-in.
"""

from __future__ import annotations

import hashlib
import json

ALV = 1
GENESIS = "sha256:" + "0" * 64
TYPES = ("cell.tick", "route.hop", "ledger.transaction")


# ---- hashing ---------------------------------------------------------------------

def fnv1a64(s: str) -> int:
    h = 0xCBF29CE484222325
    for b in s.encode("utf-8"):
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def content_hash(obj) -> str:
    """fnv1a-64 over canonical JSON, '0x%016x' — deterministic content address."""
    return "0x%016x" % fnv1a64(canon(obj))


def link_hash(env: dict) -> str:
    """sha256 of an envelope's canonical JSON — what the NEXT envelope's `prev` holds."""
    return "sha256:" + hashlib.sha256(canon(env).encode("utf-8")).hexdigest()


# ---- budget vector ---------------------------------------------------------------

def budget(wall_ms=0, power_w=0.0, mem_mb=0, prod=0, train=0, usd=0.0, tokens=None, reqs="local"):
    return {"wall_ms": wall_ms, "tokens": dict(tokens or {}), "usd": usd,
            "power_w": power_w, "mem_mb": mem_mb,
            "storage_bytes": {"train": train, "prod": prod}, "reqs": reqs}


ZERO_BUDGET = budget()


def add_budget(a: dict, b: dict) -> dict:
    tokens = dict(a["tokens"])
    for k, v in b["tokens"].items():
        tokens[k] = tokens.get(k, 0) + v
    reqs = sorted(set(a["reqs"].split("+")) | set(b["reqs"].split("+")) - {""})
    return {"wall_ms": a["wall_ms"] + b["wall_ms"], "tokens": tokens,
            "usd": round(a["usd"] + b["usd"], 6),
            "power_w": round(a["power_w"] + b["power_w"], 6),
            "mem_mb": a["mem_mb"] + b["mem_mb"],
            "storage_bytes": {k: a["storage_bytes"][k] + b["storage_bytes"][k]
                              for k in ("train", "prod")},
            "reqs": "+".join(reqs)}


def budget_ok(b) -> bool:
    try:
        return (isinstance(b["wall_ms"], (int, float)) and b["wall_ms"] >= 0
                and isinstance(b["tokens"], dict)
                and all(isinstance(v, int) and v >= 0 for v in b["tokens"].values())
                and isinstance(b["usd"], (int, float)) and b["usd"] >= 0
                and (b["power_w"] is None or b["power_w"] >= 0)
                and (b["mem_mb"] is None or b["mem_mb"] >= 0)
                and set(b["storage_bytes"]) == {"train", "prod"}
                and isinstance(b["reqs"], str))
    except (KeyError, TypeError):
        return False


# ---- DoubleEntry (minimal local; same contract as cell-runtime's) ------------------

class DoubleEntry:
    """credit (source cell, source units) / debit (dest cell, dest units) / price.

    price = {"from", "to", "rate", "ref"}: dest_amount = source_amount * rate.
    `balanced()` is the beancount zero-sum test: the translated credit and the debit
    must cancel (|credit*rate - debit| <= tol). The translation IS the routing code.
    """

    def __init__(self, credit: dict, debit: dict, price: dict):
        self.credit, self.debit, self.price = credit, debit, price

    @classmethod
    def translate(cls, src, src_units, src_amt, dst, dst_units, rate, ref):
        return cls({"cell": src, "units": src_units, "amount": src_amt},
                   {"cell": dst, "units": dst_units, "amount": round(src_amt * rate, 9)},
                   {"from": src_units, "to": dst_units, "rate": rate, "ref": ref})

    def balanced(self, tol=1e-6) -> bool:
        return abs(self.credit["amount"] * self.price["rate"] - self.debit["amount"]) <= tol

    def body(self) -> dict:
        return {"credit": self.credit, "debit": self.debit, "price": self.price}


def hop_balanced(body: dict, tol=1e-6) -> bool:
    return DoubleEntry(body["credit"], body["debit"], body["price"]).balanced(tol)


# ---- ActiveLog v1 emitter --------------------------------------------------------

class ActiveLog:
    """Append-only, (dev,seq)-keyed ActiveLog v1 run with a sha256 prev chain."""

    def __init__(self, dev="activeledger"):
        self.dev, self.seq, self.mono = dev, 0, 0
        self.records: list[dict] = []

    def emit(self, type_: str, body: dict) -> dict:
        if type_ not in TYPES:
            raise ValueError("unknown type %r (allowed %s)" % (type_, TYPES))
        if type_ in ("cell.tick", "route.hop") and not budget_ok(body.get("budget", {})):
            raise ValueError("%s requires a well-formed budget vector" % type_)
        if type_ == "route.hop" and not hop_balanced(body):
            raise ValueError("route.hop does not balance after translation")
        prev = link_hash(self.records[-1]) if self.records else GENESIS
        self.mono += 1
        env = {"alv": ALV, "dev": self.dev, "seq": self.seq, "ts": "det:%06d" % self.mono,
               "mono": self.mono, "type": type_, "body": body, "prev": prev}
        self.seq += 1
        self.records.append(env)
        return env

    def to_jsonl(self) -> str:
        return "".join(canon(r) + "\n" for r in self.records)

    def run_hash(self) -> str:
        return content_hash(self.records)


REQUIRED = ("alv", "dev", "seq", "ts", "mono", "type", "body", "prev")


def validate_envelope(rec: dict) -> bool:
    return (all(k in rec for k in REQUIRED) and rec["alv"] == ALV
            and rec["type"] in TYPES and isinstance(rec["body"], dict)
            and isinstance(rec["seq"], int) and isinstance(rec["mono"], int))


def verify_chain(records: list[dict]) -> bool:
    """Each `prev` must equal sha256 of the previous envelope; (dev,seq) contiguous."""
    prev = GENESIS
    for i, rec in enumerate(records):
        if not validate_envelope(rec) or rec["prev"] != prev or rec["seq"] != i:
            return False
        prev = link_hash(rec)
    return True


def route_total(records: list[dict], route_id: str) -> dict:
    """Sum of every budgeted record (cell.tick + route.hop) on a route — as EX1 does."""
    total = ZERO_BUDGET
    for r in records:
        if r["type"] in ("cell.tick", "route.hop") and r["body"].get("route") == route_id:
            total = add_budget(total, r["body"]["budget"])
    return total
