"""match-quilt (EX6) — skip the regex engine when the pattern is a literal.

Two product-identical routes for "find every match span of PATTERN in TEXT":
  * CHEAP route — pattern is a non-empty literal (no regex metacharacters): a str.find loop.
  * FULL route  — compile the pattern and run re.finditer; handles ALL patterns.
The quilt CHOOSES cheap iff the pattern is a literal. Spans are identical because re.finditer on
a literal is exactly a non-overlapping left-to-right substring scan.

Every step is booked to an ActiveLog v1 run via the shared emitter in labs/activeledger
(cell.tick + route.hop + ledger.transaction, budget vector incl. storage_bytes).
Ref: situations/arch/ACTIVELEDGER-CELL-GRAPH.md §13 (example collection, EX6).
"""

from __future__ import annotations

import os
import sys
import re

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "activeledger"))
import activeledger as al_mod  # noqa: E402
from activeledger import ActiveLog, DoubleEntry, budget, add_budget, ZERO_BUDGET, route_total  # noqa: E402,F401

# Deterministic cost model (not measured).
COST = {
    "cheap": {"tick": budget(1, 0.1, 1, 48, 128), "hop": budget(1, 0.05, 1, 16, 64)},
    "full":  {"tick": budget(3, 0.5, 6, 1024, 4096), "hop": budget(2, 0.25, 3, 256, 1024)},
}

META = set("\\.^$*+?{}[]|()")


def cheap_route(req) -> str:
    """Literal fast-path: str.find loop. Raises ValueError if the pattern needs the regex engine."""
    pat, text = req
    if not pat or META & set(pat):
        raise ValueError("cheap route is literal-only (non-empty, no regex metachars)")
    out, i = [], text.find(pat)
    while i != -1:
        out.append("%d-%d" % (i, i + len(pat)))
        i = text.find(pat, i + len(pat))          # non-overlapping, like re.finditer
    return ",".join(out)


def full_route(req) -> str:
    """Full regex engine: compile + finditer. Handles every pattern."""
    pat, text = req
    return ",".join("%d-%d" % m.span() for m in re.finditer(pat, text))


def choose(req) -> str:
    pat = req[0]
    return "cheap" if pat and not (META & set(pat)) else "full"


def run(req, log: ActiveLog | None = None, route: str | None = None) -> dict:
    """Choose (or force) a route, run it, book every step. Returns result + budget."""
    log = log or ActiveLog(dev="match-quilt")
    route = route or choose(req)
    c = COST[route]
    rid = "match:%s" % al_mod.content_hash([route, repr(req)])
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
    ("cat", "the cat sat on the cat mat"),
    ("aa", "aaaaa"),                     # non-overlap: 0-2,2-4
    ("needle", "haystack without it"),
    ("é", "café été"),
    ("x y", "ax y x yx y"),
    ("", "empty pattern"),               # full: matches at every position
    ("c.t", "cat cot cut c.t"),          # full: '.' is a metachar
    ("^the", "the end the"),
    ("[ae]+", "beaten leaves"),
    ("(a|b)+c", "abac bbc"),
]

if __name__ == "__main__":
    for t in WORKLOAD:
        r = run(t)
        b = r["total_budget"]
        print("%-5s wall_ms=%-2d prod=%-5d %r -> %r" % (r["route"], b["wall_ms"], b["storage_bytes"]["prod"], t, r["out"]))
