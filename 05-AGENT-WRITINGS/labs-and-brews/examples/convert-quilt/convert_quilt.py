"""convert-quilt (EX2) — a unit converter with a free identity shortcut.

Two product-identical routes for the same conversion request:

  * CHEAP route — identity/no-op. When source unit == target unit the value is returned
    untouched: no conversion table is loaded, so tooling + storage are tiny.
  * FULL route — the general conversion (deterministic table: length m/cm/km/in/ft,
    mass g/kg/lb, temperature C/F/K), via a base unit.

The quilt CHOOSES the cheap identity route iff src == target, else the full route. On the
shared (src == target) cases both routes reach the identical product.

Every step is booked to an ActiveLog v1 run via labs/activeledger (imported, not re-emitted):
cell.tick + balanced route.hop carrying the unit-translation price and a budget vector
incl. storage_bytes {train,prod}.

Ref: situations/arch/ACTIVELEDGER-CELL-GRAPH.md §8 (budget vector), §13 (example collection).
"""

from __future__ import annotations

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "activeledger"))
import activeledger as al  # noqa: E402

# ---- the general-conversion table (FULL route only) -------------------------------------
# linear units: factor to the dimension's base unit (m, g). Temperature is affine via Kelvin.
LINEAR = {
    "length": {"m": Fraction(1), "cm": Fraction(1, 100), "km": Fraction(1000),
               "in": Fraction(254, 10000), "ft": Fraction(3048, 10000)},
    "mass": {"g": Fraction(1), "kg": Fraction(1000), "lb": Fraction("453.59237")},
}
TEMPS = ("C", "F", "K")
BASE = {"length": "m", "mass": "g", "temp": "K"}


def dimension(unit: str) -> str:
    for dim, tbl in LINEAR.items():
        if unit in tbl:
            return dim
    if unit in TEMPS:
        return "temp"
    raise ValueError("unknown unit %r" % unit)


def to_base(v: Fraction, unit: str) -> Fraction:
    dim = dimension(unit)
    if dim != "temp":
        return v * LINEAR[dim][unit]
    if unit == "K":
        return v
    if unit == "C":
        return v + Fraction("273.15")
    return (v - 32) * Fraction(5, 9) + Fraction("273.15")  # F


def from_base(v: Fraction, unit: str) -> Fraction:
    dim = dimension(unit)
    if dim != "temp":
        return v / LINEAR[dim][unit]
    if unit == "K":
        return v
    if unit == "C":
        return v - Fraction("273.15")
    return (v - Fraction("273.15")) * Fraction(9, 5) + 32  # F


def fmt(v: Fraction) -> str:
    """Fixed 6-dp canonical product string (round half-even via Fraction rounding)."""
    scaled = round(v * 10**6)
    sign = "-" if scaled < 0 else ""
    a = abs(scaled)
    return "%s%d.%06d" % (sign, a // 10**6, a % 10**6)


# ---- the two routes --------------------------------------------------------------------

def cheap_route(value: str, src: str, dst: str) -> str:
    """Identity: only valid when src == dst; value returned untouched (canonicalised)."""
    if src != dst:
        raise ValueError("cheap route is identity-only (src != dst)")
    return fmt(Fraction(value))


def full_route(value: str, src: str, dst: str) -> str:
    if dimension(src) != dimension(dst):
        raise ValueError("cannot convert %s -> %s" % (src, dst))
    return fmt(from_base(to_base(Fraction(value), src), dst))


def choose(src: str, dst: str) -> str:
    return "cheap" if src == dst else "full"


# ---- budgets (deterministic cost model, like EX1) -----------------------------------------
# Cheap: no table, no base-unit hop -> tiny code/storage footprint. Full: ships the table.
COST = {
    "cheap": {"tick": al.budget(1, 0.1, 1, 32, 128), "hop": al.budget(1, 0.05, 1, 16, 64)},
    "full": {"tick": al.budget(3, 0.5, 3, 768, 3072), "hop": al.budget(2, 0.3, 2, 384, 1536)},
}


# ---- the quilt ---------------------------------------------------------------------------

def _hop(log, route, src_cell, dst_cell, src_units, dst_units, src_amt, dst_amt, cost):
    """Balanced route.hop; rate = dst/src is the unit-translation price."""
    rate = 1.0 if src_amt == dst_amt else dst_amt / src_amt
    de = al.DoubleEntry.translate(src_cell, src_units, src_amt, dst_cell, dst_units, rate,
                                  "convert-quilt:%s" % route)
    body = de.body()
    body["route"] = route
    body["budget"] = cost
    log.emit("route.hop", body)


def run(req: dict, log: "al.ActiveLog | None" = None, force: str | None = None) -> dict:
    """req = {value: str, src, dst}. `force` pins a route (for comparison only)."""
    log = log or al.ActiveLog(dev="convert-quilt")
    route = force or choose(req["src"], req["dst"])
    c = COST[route]
    v = req["value"]
    fv = float(Fraction(v))

    log.emit("cell.tick", {"cell": "request", "kind": "SIM", "route": route, "value": v,
                           "src": req["src"], "dst": req["dst"], "budget": c["tick"]})
    if route == "cheap":
        product = cheap_route(v, req["src"], req["dst"])
        _hop(log, route, "request", "result", req["src"], req["dst"], fv, float(product), c["hop"])
    else:
        base_u = BASE[dimension(req["src"])]
        base_v = to_base(Fraction(v), req["src"])
        product = full_route(v, req["src"], req["dst"])
        _hop(log, route, "request", "table", req["src"], base_u, fv, float(base_v), c["hop"])
        log.emit("cell.tick", {"cell": "table", "kind": "SIM", "route": route,
                               "base": base_u, "budget": c["tick"]})
        _hop(log, route, "table", "result", base_u, req["dst"], float(base_v), float(product), c["hop"])
    log.emit("cell.tick", {"cell": "result", "kind": "SIM", "route": route,
                           "product": product, "units": req["dst"], "budget": c["tick"]})
    total = al.route_total(log.records, route)
    log.emit("ledger.transaction", {"route": route, "product": product, "total_budget": total})
    return {"route": route, "product": product, "total_budget": total, "log": log}


WORKLOAD = [
    {"value": "12.5", "src": "m", "dst": "m"},
    {"value": "3", "src": "kg", "dst": "kg"},
    {"value": "98.6", "src": "F", "dst": "F"},
    {"value": "100", "src": "cm", "dst": "in"},
    {"value": "1", "src": "km", "dst": "ft"},
    {"value": "10", "src": "lb", "dst": "kg"},
    {"value": "100", "src": "C", "dst": "F"},
    {"value": "300", "src": "K", "dst": "C"},
]

if __name__ == "__main__":
    for r in WORKLOAD:
        o = run(r)
        print("%8s %-2s -> %-2s = %14s via %-5s (wall_ms=%d, prod_bytes=%d)" % (
            r["value"], r["src"], r["dst"], o["product"], o["route"],
            o["total_budget"]["wall_ms"], o["total_budget"]["storage_bytes"]["prod"]))
