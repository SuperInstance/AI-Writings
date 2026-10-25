"""text-normalize-quilt (EX4) — skip the unicode tooling when the input is pure ASCII.

Two product-identical routes for the same "normalize" request
(lowercase + strip + collapse whitespace runs to one space):

  * CHEAP route — pure-ASCII only. Works on raw bytes: bytes.translate (map the ASCII
    "unicode-whitespace" controls 0x1c-0x1f to space), bytes.lower, bytes.split/join.
    No unicodedata, no NFKC table, no casefold tables — tiny footprint.
  * FULL route  — the full unicode path via stdlib `unicodedata`: NFKC normalize,
    str.casefold, str.split() over unicode whitespace. Handles ALL input.

The quilt CHOOSES the cheap route iff the input is pure ASCII (str.isascii), else the
full route. On ASCII the two are provably identical:
  - NFKC is the identity on ASCII;
  - casefold == lower on ASCII (no ß/ligature/etc. in 0x00-0x7f);
  - str.split() treats 0x09-0x0d, 0x1c-0x1f, 0x20 as whitespace, whereas bytes.split()
    treats only 0x09-0x0d and 0x20 — so the cheap route first maps 0x1c-0x1f to space.
The selftest checks this exhaustively over all 128 ASCII code points and seeded fuzz.

Every step is booked to an ActiveLog v1 run via the shared emitter in labs/activeledger
(cell.tick + route.hop + ledger.transaction, budget vector incl. storage_bytes).

Ref: situations/arch/ACTIVELEDGER-CELL-GRAPH.md §8 (schema), §13 (example collection, EX4).
"""

from __future__ import annotations

import os
import sys
import unicodedata

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "activeledger"))
import activeledger as al_mod  # noqa: E402
from activeledger import ActiveLog, DoubleEntry, budget, add_budget, ZERO_BUDGET, route_total  # noqa: E402,F401

# Deterministic cost model (not measured). The full route loads unicodedata's tables
# and casefold machinery: more time, memory, and a much bigger prod footprint.
COST = {
    "cheap": {"tick": budget(1, 0.1, 1, 48, 128), "hop": budget(1, 0.05, 1, 16, 64)},
    "full":  {"tick": budget(3, 0.5, 6, 2048, 8192), "hop": budget(2, 0.25, 3, 512, 2048)},
}

_ASCII_WS = bytes.maketrans(b"\x1c\x1d\x1e\x1f", b"    ")


def cheap_route(text: str) -> str:
    """Pure-ASCII bytes path. Raises ValueError on non-ASCII (it lacks the tooling)."""
    if not text.isascii():
        raise ValueError("cheap route is ASCII-only")
    b = text.encode("ascii").translate(_ASCII_WS).lower()
    return b" ".join(b.split()).decode("ascii")


def full_route(text: str) -> str:
    """Full unicode path: NFKC, casefold, unicode-whitespace collapse."""
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def choose(text: str) -> str:
    return "cheap" if text.isascii() else "full"


def run(text: str, log: ActiveLog | None = None, route: str | None = None) -> dict:
    """Choose (or force) a route, run it, book every step. Returns result + budget."""
    log = log or ActiveLog(dev="text-normalize-quilt")
    route = route or choose(text)
    c = COST[route]
    rid = "norm:%s" % al_mod.content_hash([route, text])
    total = ZERO_BUDGET
    in_units = "ascii-bytes" if route == "cheap" else "codepoints"

    log.emit("cell.tick", {"route": rid, "cell": "request", "kind": "SIM", "path": route,
                           "units": "chars", "chars": len(text), "budget": c["tick"]})
    total = add_budget(total, c["tick"])

    h = DoubleEntry.translate("request", "chars", float(len(text)), "normalizer",
                              in_units, 1.0, "chars==%s on this route" % in_units)
    log.emit("route.hop", {"route": rid, **h.body(), "budget": c["hop"]})
    total = add_budget(total, c["hop"])

    out = cheap_route(text) if route == "cheap" else full_route(text)
    log.emit("cell.tick", {"route": rid, "cell": "normalizer", "kind": "SIM", "path": route,
                           "out_hash": al_mod.content_hash(out), "units": in_units,
                           "budget": c["tick"]})
    total = add_budget(total, c["tick"])

    h = DoubleEntry.translate("normalizer", in_units, float(len(out)), "result",
                              "chars", 1.0, "chars==%s on this route" % in_units)
    log.emit("route.hop", {"route": rid, **h.body(), "budget": c["hop"]})
    total = add_budget(total, c["hop"])

    log.emit("cell.tick", {"route": rid, "cell": "result", "kind": "SIM", "value": out,
                           "units": "chars", "budget": c["tick"]})
    total = add_budget(total, c["tick"])

    log.emit("ledger.transaction", {"route": rid, "path": route, "out": out, "total_budget": total})
    return {"route": route, "route_id": rid, "out": out, "total_budget": total, "log": log}


WORKLOAD = [
    "  Hello,   World!  ",
    "Line1\r\nLine2\t\tTAB\x0bVT\x0cFF",
    "ALREADY clean",
    "\x1cUS\x1dGS\x1eRS\x1fFS sep",
    "",
    "   ",
    "MiXeD 123 CaSe\n\n\nend",
    "Straße  ﬁne  Ⅷ  ＡＢＣ",          # non-ASCII: forces the full route
    "café 　ünïcode",     # non-ASCII whitespace + accents
]

if __name__ == "__main__":
    for t in WORKLOAD:
        r = run(t)
        b = r["total_budget"]
        print("%-6s wall_ms=%-2d prod=%-5d %r -> %r" % (
            r["route"], b["wall_ms"], b["storage_bytes"]["prod"], t, r["out"]))
