"""csv-stats-quilt (EX8) — single-pass split when there is no grouping.

Two product-identical routes for "stats of one integer column of a CSV":
  * CHEAP route — ungrouped, no quote characters, LF line ends: split on ',' once per line, keep
    running int accumulators, integer-only half-even mean to 4dp. No csv module, no Fraction.
  * FULL route  — csv.DictReader (handles quotes/CRLF), optional group-by, Fraction -> Decimal mean.
The quilt CHOOSES cheap iff there is no group column and the text has no quotes or CR.

Every step is booked to an ActiveLog v1 run via the shared emitter in labs/activeledger
(cell.tick + route.hop + ledger.transaction, budget vector incl. storage_bytes).
Ref: situations/arch/ACTIVELEDGER-CELL-GRAPH.md §13 (example collection, EX8).
"""

from __future__ import annotations

import os
import sys
import csv
import decimal
import fractions
import io

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "activeledger"))
import activeledger as al_mod  # noqa: E402
from activeledger import ActiveLog, DoubleEntry, budget, add_budget, ZERO_BUDGET, route_total  # noqa: E402,F401

# Deterministic cost model (not measured).
COST = {
    "cheap": {"tick": budget(1, 0.1, 1, 48, 128), "hop": budget(1, 0.05, 1, 16, 64)},
    "full":  {"tick": budget(3, 0.5, 6, 1024, 4096), "hop": budget(2, 0.25, 3, 256, 1024)},
}

def _parse_ints(col, rows):
    return [int(r[col]) for r in rows]


def _stats(vals):
    return len(vals), sum(vals), min(vals), max(vals)


def _fmt(g, n, s, lo, hi, mean):
    return "%s|n=%d|sum=%d|min=%d|max=%d|mean=%s" % (g, n, s, lo, hi, mean)


def _eligible(req) -> bool:
    text, col, grp = req
    return grp is None and '"' not in text and "\r" not in text


def cheap_route(req) -> str:
    """Single-pass path: str.split(','), running int accumulators, integer-only mean. No csv, no Fraction."""
    if not _eligible(req):
        raise ValueError("cheap route is ungrouped, unquoted LF-only CSV")
    text, col, _ = req
    lines = [ln for ln in text.split("\n") if ln]
    ci = lines[0].split(",").index(col)
    n = s = 0
    lo = hi = None
    for ln in lines[1:]:
        v = int(ln.split(",")[ci])
        n, s = n + 1, s + v
        lo = v if lo is None or v < lo else lo
        hi = v if hi is None or v > hi else hi
    q, r = divmod(abs(s) * 10000, n)
    q += (2 * r > n) or (2 * r == n and q % 2 == 1)
    mean = "%s%d.%04d" % ("-" if s < 0 else "", q // 10000, q % 10000)
    return _fmt("*", n, s, lo, hi, mean)


def full_route(req) -> str:
    """Full path: csv.DictReader (quotes, CRLF), optional group-by, exact Fraction mean."""
    text, col, grp = req
    groups = {}
    for row in csv.DictReader(io.StringIO(text)):
        groups.setdefault(row[grp] if grp else "*", []).append(row)
    out = []
    for g in sorted(groups):
        n, s, lo, hi = _stats(_parse_ints(col, groups[g]))
        f = fractions.Fraction(s, n)
        with decimal.localcontext() as ctx:
            ctx.prec = 100
            m = (decimal.Decimal(f.numerator) / decimal.Decimal(f.denominator)).quantize(
                decimal.Decimal("0.0001"), decimal.ROUND_HALF_EVEN)
        out.append(_fmt(g, n, s, lo, hi, format(m, "f")))
    return "\n".join(out)


def choose(req) -> str:
    return "cheap" if _eligible(req) else "full"


def run(req, log: ActiveLog | None = None, route: str | None = None) -> dict:
    """Choose (or force) a route, run it, book every step. Returns result + budget."""
    log = log or ActiveLog(dev="csv-stats-quilt")
    route = route or choose(req)
    c = COST[route]
    rid = "csv-stats:%s" % al_mod.content_hash([route, repr(req)])
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
    ("id,amt\n1,10\n2,20\n3,30\n", "amt", None),
    ("name,qty,price\nx,1,5\ny,2,-7\nz,3,0\n", "price", None),
    ("a,b\n1,2\n", "b", None),
    ("v\n1\n2\n", "v", None),                        # mean 1.5
    ("v\n1\n0\n0\n", "v", None),                     # mean 0.3333
    ("v\n-1\n0\n0\n", "v", None),                    # mean -0.3333
    ("k,v\na,1\nb,2\na,3\n", "v", "k"),             # group-by: full route
    ('n,v\n"x,y",4\n"z",6\n', "v", None),            # quoted field: full route
    ("n,v\r\nx,4\r\ny,5\r\n", "v", None),            # CRLF: full route
]

if __name__ == "__main__":
    for t in WORKLOAD:
        r = run(t)
        b = r["total_budget"]
        print("%-5s wall_ms=%-2d prod=%-5d %r -> %r" % (r["route"], b["wall_ms"], b["storage_bytes"]["prod"], t, r["out"]))
