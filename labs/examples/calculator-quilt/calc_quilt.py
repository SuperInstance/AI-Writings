"""calculator-quilt (EX1) — the anti-GAN-of-programming example.

Two product-identical routes for the same money equation:

  * simple money route — integer-cents fixed-point. No interest tooling, so the
    routing (and its on-disk footprint) is tiny. Reaches the answer for every
    equation that does NOT need compounding.
  * full route — decimal.Decimal + interest/compounding tooling. Reaches the answer
    for ALL equations, but ships more code, more memory, more time.

The quilt CHOOSES the simple route whenever the equation does not need the extra
math tooling, and only escalates to the full route for interest. Both routes reach
the *identical* product (to the cent) on the shared cases — novelty in process,
identity in product.

Everything is booked to an ActiveLog v1 run (envelope + budget vector, incl.
storage_bytes {train,prod}) so System-2 can backtest this quilt against alternatives
on time / power / storage. The `ActiveLog` class here is a self-contained stand-in
for labs/activeledger (B1); swap the import when B1 lands — the record shape matches.

Ref: situations/arch/ACTIVELEDGER-CELL-GRAPH.md §8 (schema), §11 (iron-triangle +
storage), §13 (the example collection).
"""

from __future__ import annotations

import json
from decimal import Decimal, ROUND_HALF_EVEN

ALV = 1  # ActiveLog envelope version


# ---- fleet WAL idiom (matches labs/situation-recorder + MicroMoth-quilt) -----------

def fnv1a64(s: str) -> int:
    """fnv1a-64 over utf-8 — the fleet content-hash convention."""
    h = 0xCBF29CE484222325
    for b in s.encode("utf-8"):
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


GENESIS = "0x0000000000000000"


# ---- the budget vector (schema §8) --------------------------------------------------

def budget(wall_ms, power_w, mem_mb, prod_store, train_store, usd=0.0, tokens=None, reqs="local"):
    return {
        "wall_ms": wall_ms,
        "tokens": tokens or {},          # {api_name: int}; local compute uses none
        "usd": usd,
        "power_w": power_w,
        "mem_mb": mem_mb,
        "storage_bytes": {"train": train_store, "prod": prod_store},
        "reqs": reqs,
    }


def add_budget(a: dict, b: dict) -> dict:
    """Field-by-field sum of two budget vectors (tokens + storage merge)."""
    tokens = dict(a["tokens"])
    for k, v in b["tokens"].items():
        tokens[k] = tokens.get(k, 0) + v
    return {
        "wall_ms": a["wall_ms"] + b["wall_ms"],
        "tokens": tokens,
        "usd": round(a["usd"] + b["usd"], 6),
        "power_w": round(a["power_w"] + b["power_w"], 6),
        "mem_mb": a["mem_mb"] + b["mem_mb"],
        "storage_bytes": {
            "train": a["storage_bytes"]["train"] + b["storage_bytes"]["train"],
            "prod": a["storage_bytes"]["prod"] + b["storage_bytes"]["prod"],
        },
        "reqs": a["reqs"] if a["reqs"] == b["reqs"] else f"{a['reqs']}+{b['reqs']}",
    }


ZERO_BUDGET = budget(0, 0.0, 0, 0, 0)

# Per-record cost models. The full route genuinely ships more (Decimal + interest
# tooling) — bigger prod footprint, more memory, slower — so it MUST cost more on
# both the compute and the storage measurements of the iron-triangle's cheap axis.
COST = {
    "simple": {"tick": budget(1, 0.2, 1, 64, 256), "hop": budget(1, 0.1, 1, 32, 128)},
    "full":   {"tick": budget(4, 0.6, 4, 1024, 4096), "hop": budget(2, 0.3, 2, 512, 2048)},
}


# ---- ActiveLog v1 emitter (stand-in for labs/activeledger / B1) ---------------------

class ActiveLog:
    """Append-only, (dev,seq)-keyed, fnv1a-64 prev-chained ActiveLog v1 run."""

    def __init__(self, dev: str = "calc-quilt"):
        self.dev = dev
        self.seq = 0
        self.mono = 0
        self.records: list[dict] = []

    def emit(self, type_: str, body: dict) -> dict:
        prev = self.records[-1]["hash"] if self.records else GENESIS
        self.mono += 1
        env = {"alv": ALV, "dev": self.dev, "seq": self.seq, "ts": "det",
               "mono": self.mono, "type": type_, "body": body, "prev": prev}
        env["hash"] = "0x%016x" % fnv1a64(_canon({"prev": prev, **env}))
        self.seq += 1
        self.records.append(env)
        return env

    def to_jsonl(self) -> str:
        return "".join(_canon(r) + "\n" for r in self.records)


def verify_chain(records: list[dict]) -> bool:
    """Re-derive each hash from the running prev; tamper-evident."""
    prev = GENESIS
    for rec in records:
        env = {k: v for k, v in rec.items() if k != "hash"}
        env["prev"] = prev
        if ("0x%016x" % fnv1a64(_canon(env))) != rec["hash"]:
            return False
        prev = rec["hash"]
    return True


# ---- money + the two routes ---------------------------------------------------------

class NeedsInterest(Exception):
    """Raised by the simple route when an equation needs the full route."""


def dollars_to_cents(s: str) -> int:
    return int((Decimal(s) * 100).to_integral_value(rounding=ROUND_HALF_EVEN))


def cents_to_dollars(c: int) -> str:
    return str((Decimal(c) / 100).quantize(Decimal("0.01")))


def needs_interest(eq: dict) -> bool:
    return eq["op"] == "compound"


def simple_route(eq: dict) -> int:
    """Integer-cents. Handles add/sub/scale/pct exactly; refuses interest."""
    op = eq["op"]
    if op == "add":
        return dollars_to_cents(eq["a"]) + dollars_to_cents(eq["b"])
    if op == "sub":
        return dollars_to_cents(eq["a"]) - dollars_to_cents(eq["b"])
    if op == "scale":
        return dollars_to_cents(eq["a"]) * int(eq["k"])
    if op == "pct":
        # p% of amount; test values chosen to divide exactly (see README SHORTCUT).
        return (dollars_to_cents(eq["a"]) * int(eq["p"])) // 100
    raise NeedsInterest(op)


def full_route(eq: dict) -> int:
    """decimal.Decimal dollars + interest tooling. Handles everything."""
    op = eq["op"]
    q = Decimal("0.01")
    if op == "add":
        r = Decimal(eq["a"]) + Decimal(eq["b"])
    elif op == "sub":
        r = Decimal(eq["a"]) - Decimal(eq["b"])
    elif op == "scale":
        r = Decimal(eq["a"]) * int(eq["k"])
    elif op == "pct":
        r = Decimal(eq["a"]) * Decimal(eq["p"]) / 100
    elif op == "compound":
        # principal * (1+rate)**periods — the tooling the simple route lacks.
        r = Decimal(eq["principal"]) * (1 + Decimal(eq["rate"])) ** int(eq["periods"])
    else:
        raise ValueError(op)
    return int((r.quantize(q, rounding=ROUND_HALF_EVEN) * 100).to_integral_value())


def choose(eq: dict) -> str:
    return "full" if needs_interest(eq) else "simple"


# ---- the quilt: run a route, booking every step + budget ----------------------------

def _hop(al: ActiveLog, src, dst, src_units, dst_units, src_amt, rate, cost):
    """A balanced double-entry route.hop with a unit translation price."""
    dst_amt = int(round(src_amt * rate))
    body = {
        "credit": {"cell": src, "units": src_units, "amount": src_amt},
        "debit": {"cell": dst, "units": dst_units, "amount": dst_amt},
        "price": {"from": src_units, "to": dst_units, "rate": rate},
        "budget": cost,
    }
    al.emit("route.hop", body)
    return dst_amt


def run(eq: dict, al: ActiveLog | None = None) -> dict:
    """Choose a route, run it with full ActiveLog booking, return the result."""
    al = al or ActiveLog()
    route = choose(eq)
    c = COST[route]
    total = ZERO_BUDGET

    # cell.tick: parse the request (dollars, human units)
    al.emit("cell.tick", {"cell": "request", "kind": "SIM", "op": eq["op"],
                          "units": "USD", "budget": c["tick"]})
    total = add_budget(total, c["tick"])

    # route.hop: translate dollars -> cents (into the calculator's own units)
    primary = eq.get("a") or eq.get("principal")
    _hop(al, "request", "calc", "USD", "USD-cents", float(Decimal(primary)), 100.0, c["hop"])
    total = add_budget(total, c["hop"])

    # cell.tick: compute in the route's native representation
    cents = full_route(eq) if route == "full" else simple_route(eq)
    al.emit("cell.tick", {"cell": "calc", "kind": "SIM", "route": route,
                          "result_cents": cents, "units": "USD-cents", "budget": c["tick"]})
    total = add_budget(total, c["tick"])

    # route.hop: translate cents -> dollars (back to human units)
    _hop(al, "calc", "result", "USD-cents", "USD", float(cents), 0.01, c["hop"])
    total = add_budget(total, c["hop"])

    # cell.tick: present the result
    al.emit("cell.tick", {"cell": "result", "kind": "SIM",
                          "value": cents_to_dollars(cents), "units": "USD", "budget": c["tick"]})
    total = add_budget(total, c["tick"])

    # ledger.transaction: bind the route + its declared total budget
    al.emit("ledger.transaction", {"route": route, "result_cents": cents,
                                    "total_budget": total})
    return {"route": route, "cents": cents, "dollars": cents_to_dollars(cents),
            "total_budget": total, "log": al}


# A small, obvious workload for demos + backtesting.
WORKLOAD = [
    {"op": "add", "a": "12.34", "b": "5.66"},
    {"op": "sub", "a": "100.00", "b": "0.01"},
    {"op": "scale", "a": "9.99", "k": 3},
    {"op": "pct", "a": "12.34", "p": 50},          # exact: 617 cents
    {"op": "pct", "a": "10.00", "p": 25},          # exact: 250 cents
    {"op": "compound", "principal": "1000.00", "rate": "0.05", "periods": 3},  # needs full route
]


if __name__ == "__main__":
    for eq in WORKLOAD:
        r = run(eq)
        print(f"{eq['op']:9s} -> {r['dollars']:>10s}  via {r['route']:6s} "
              f"(wall_ms={r['total_budget']['wall_ms']}, "
              f"prod_bytes={r['total_budget']['storage_bytes']['prod']})")
