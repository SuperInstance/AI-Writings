"""currency-round-quilt (EX7) — integer cents when there is no fx rate.

Two product-identical routes for "amount (+ optional fx rate) -> cents string, half-even":
  * CHEAP route — fx is 1 and the amount is a plain decimal: pure integer-cents arithmetic on the
    digit string, rounding half-even from the dropped digits. No Decimal.
  * FULL route  — exact decimal.Decimal multiply by the fx rate, quantize to 0.01 ROUND_HALF_EVEN.
The quilt CHOOSES cheap iff there is no fx and the amount is a plain decimal literal.

Every step is booked to an ActiveLog v1 run via the shared emitter in labs/activeledger
(cell.tick + route.hop + ledger.transaction, budget vector incl. storage_bytes).
Ref: situations/arch/ACTIVELEDGER-CELL-GRAPH.md §13 (example collection, EX7).
"""

from __future__ import annotations

import os
import sys
import decimal

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "activeledger"))
import activeledger as al_mod  # noqa: E402
from activeledger import ActiveLog, DoubleEntry, budget, add_budget, ZERO_BUDGET, route_total  # noqa: E402,F401

# Deterministic cost model (not measured).
COST = {
    "cheap": {"tick": budget(1, 0.1, 1, 48, 128), "hop": budget(1, 0.05, 1, 16, 64)},
    "full":  {"tick": budget(3, 0.5, 6, 1024, 4096), "hop": budget(2, 0.25, 3, 256, 1024)},
}

_CHEAP_FX = ("1", "1.0", "1.00")


def _eligible(req) -> bool:
    amt, fx = req
    if fx not in _CHEAP_FX:
        return False
    body = amt[1:] if amt[:1] == "-" else amt
    ip, dot, fp = body.partition(".")
    return ip.isdigit() and ip.isascii() and (fp == "" or (fp.isdigit() and fp.isascii()))


def cheap_route(req) -> str:
    """Integer-cents path: digit-string surgery + half-even on the dropped digits. No Decimal."""
    if not _eligible(req):
        raise ValueError("cheap route is no-fx plain-decimal only")
    amt = req[0]
    neg = amt[:1] == "-"
    ip, _, fp = (amt[1:] if neg else amt).partition(".")
    cents = int(ip + (fp[:2] + "00")[:2])
    rest = fp[2:]
    if rest:
        up = rest[0] > "5" or (rest[0] == "5" and (rest[1:].strip("0") != "" or cents % 2 == 1))
        cents += up
    return "%s%d.%02d" % ("-" if neg else "", cents // 100, cents % 100)


def full_route(req) -> str:
    """Full path: exact Decimal multiply by the fx rate, quantize half-even to cents."""
    amt, fx = req
    with decimal.localcontext() as ctx:
        ctx.prec = 200
        q = (decimal.Decimal(amt) * decimal.Decimal(fx)).quantize(decimal.Decimal("0.01"), decimal.ROUND_HALF_EVEN)
        return format(q, "f")


def choose(req) -> str:
    return "cheap" if _eligible(req) else "full"


def run(req, log: ActiveLog | None = None, route: str | None = None) -> dict:
    """Choose (or force) a route, run it, book every step. Returns result + budget."""
    log = log or ActiveLog(dev="currency-round-quilt")
    route = route or choose(req)
    c = COST[route]
    rid = "currency-round:%s" % al_mod.content_hash([route, repr(req)])
    total = ZERO_BUDGET
    size = float(len(repr(req)))

    log.emit("cell.tick", {"route": rid, "cell": "request", "kind": "SIM", "path": route,
                           "units": "chars", "chars": int(size), "budget": c["tick"]})
    total = add_budget(total, c["tick"])
    h = DoubleEntry.translate("request", "chars", size, "worker", "chars", 1.0, "same request, route=%s" % route)
    log.emit("route.hop", {"route": rid, **h.body(), "budget": c["hop"]})
    total = add_budget(total, c["hop"])

    out = (cheap_route if route == "cheap" else full_route)(req)
    osz = float(len(out))
    log.emit("cell.tick", {"route": rid, "cell": "worker", "kind": "SIM", "path": route,
                           "out_hash": al_mod.content_hash(out), "units": "chars", "budget": c["tick"]})
    total = add_budget(total, c["tick"])
    h = DoubleEntry.translate("worker", "chars", osz, "result", "chars", 1.0, "product emitted")
    log.emit("route.hop", {"route": rid, **h.body(), "budget": c["hop"]})
    total = add_budget(total, c["hop"])
    log.emit("cell.tick", {"route": rid, "cell": "result", "kind": "SIM", "value": out,
                           "units": "chars", "budget": c["tick"]})
    total = add_budget(total, c["tick"])
    log.emit("ledger.transaction", {"route": rid, "path": route, "out": out, "total_budget": total})
    return {"route": route, "route_id": rid, "out": out, "total_budget": total, "log": log}

WORKLOAD = [
    ("19.99", "1"), ("0.125", "1"), ("0.135", "1"), ("2.675", "1.00"), ("-2.5", "1"),
    ("1234567.005", "1.0"), ("-0.001", "1"), ("7", "1"), ("0.1050000001", "1"),
    ("100.00", "1.0873"),          # real fx: full route
    ("19.99", "0.9231"),
    ("1e3", "1"),                  # exponent form: full route
    (" 5.5", "1"),
]

if __name__ == "__main__":
    for t in WORKLOAD:
        r = run(t)
        b = r["total_budget"]
        print("%-5s wall_ms=%-2d prod=%-5d %r -> %r" % (r["route"], b["wall_ms"], b["storage_bytes"]["prod"], t, r["out"]))
