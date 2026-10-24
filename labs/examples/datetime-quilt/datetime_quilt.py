"""datetime-quilt (EX3) — skip the timezone machinery when every input is UTC.

Two product-identical routes for an "add duration" / "diff" request:

  * utc route  — pure integer epoch-seconds arithmetic (days-from-civil). No datetime,
    no zoneinfo, no tz database. Tiny. Refuses any non-UTC input.
  * full route — datetime + zoneinfo, tz/DST-aware. Handles every input, ships the tz db.

The quilt CHOOSES the utc route iff every input is UTC, else the full route. Both reach
the identical instant on the shared (all-UTC) cases — novelty in process, identity in
product. Every step is booked to an ActiveLog v1 run via labs/activeledger (imported,
not re-emitted): cell.tick + route.hop, each with a budget vector incl storage_bytes.

Request grammar: an instant is {"iso": "YYYY-MM-DDTHH:MM:SS", "tz": "UTC"|IANA name}.
  {"op":"add","at":inst,"seconds":int}  -> epoch seconds of the resulting instant
  {"op":"diff","a":inst,"b":inst}       -> b - a in seconds

Ref: situations/arch/ACTIVELEDGER-CELL-GRAPH.md §8 (schema), §13 (example collection).
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "activeledger"))
from activeledger import (ActiveLog, DoubleEntry, ZERO_BUDGET, add_budget, budget,  # noqa: E402
                          route_total, verify_chain)


class NeedsTZ(Exception):
    """Raised by the utc route when an input is not UTC."""


def _instants(req: dict) -> list:
    return [req["at"]] if req["op"] == "add" else [req["a"], req["b"]]


def all_utc(req: dict) -> bool:
    return all(i["tz"] == "UTC" for i in _instants(req))


def choose(req: dict) -> str:
    return "utc" if all_utc(req) else "full"


# ---- utc route: integer arithmetic only -------------------------------------------

def _days_from_civil(y: int, m: int, d: int) -> int:
    """Howard Hinnant's days-from-civil (proleptic Gregorian), integers only."""
    y -= m <= 2
    era = y // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def utc_epoch(inst: dict) -> int:
    if inst["tz"] != "UTC":
        raise NeedsTZ(inst["tz"])
    date, time = inst["iso"].split("T")
    y, mo, d = (int(x) for x in date.split("-"))
    h, mi, s = (int(x) for x in time.split(":"))
    return _days_from_civil(y, mo, d) * 86400 + h * 3600 + mi * 60 + s


def utc_route(req: dict) -> int:
    if req["op"] == "add":
        return utc_epoch(req["at"]) + req["seconds"]
    return utc_epoch(req["b"]) - utc_epoch(req["a"])


# ---- full route: tz/DST-aware (stdlib datetime + zoneinfo) ------------------------

def full_epoch(inst: dict) -> int:
    from datetime import datetime
    from zoneinfo import ZoneInfo
    dt = datetime.fromisoformat(inst["iso"]).replace(tzinfo=ZoneInfo(inst["tz"]))
    return int(dt.timestamp())


def full_route(req: dict) -> int:
    if req["op"] == "add":
        return full_epoch(req["at"]) + req["seconds"]
    return full_epoch(req["b"]) - full_epoch(req["a"])


def render_utc(epoch: int) -> str:
    from datetime import datetime, timezone
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---- cost models (deterministic; the full route ships the tz db) ------------------

COST = {
    "utc":  {"tick": budget(1, 0.1, 1, 48, 128),     "hop": budget(1, 0.05, 1, 16, 64)},
    "full": {"tick": budget(5, 0.7, 6, 2048, 8192),  "hop": budget(2, 0.3, 3, 512, 2048)},
}


def route_cost(route: str) -> dict:
    """Declared budget of a whole run: 3 ticks + 2 hops."""
    c = COST[route]
    t = ZERO_BUDGET
    for _ in range(3):
        t = add_budget(t, c["tick"])
    for _ in range(2):
        t = add_budget(t, c["hop"])
    return t


def _hop(al: ActiveLog, rid: str, src, dst, su, du, amt, rate, cost):
    de = DoubleEntry.translate(src, su, amt, dst, du, rate, "datetime-quilt")
    al.emit("route.hop", {"route": rid, **de.body(), "budget": cost})


def run(req: dict, al: ActiveLog | None = None, force: str | None = None) -> dict:
    """Choose (or force) a route, run it with full ActiveLog booking."""
    al = al or ActiveLog(dev="datetime-quilt")
    route = force or choose(req)
    rid = "dt:%d:%s" % (al.seq, route)
    c = COST[route]

    al.emit("cell.tick", {"route": rid, "cell": "request", "kind": "SIM", "op": req["op"],
                          "units": "iso", "budget": c["tick"]})
    _hop(al, rid, "request", "calc", "iso", "epoch-s", float(len(_instants(req))), 1.0, c["hop"])

    result = full_route(req) if route == "full" else utc_route(req)
    al.emit("cell.tick", {"route": rid, "cell": "calc", "kind": "SIM", "chosen": route,
                          "result": result, "units": "epoch-s", "budget": c["tick"]})

    _hop(al, rid, "calc", "result", "epoch-s", "iso", float(result), 1.0, c["hop"])
    shown = render_utc(result) if req["op"] == "add" else "%ds" % result
    al.emit("cell.tick", {"route": rid, "cell": "result", "kind": "SIM", "value": shown,
                          "units": "iso", "budget": c["tick"]})

    total = route_total(al.records, rid)
    al.emit("ledger.transaction", {"route": rid, "chosen": route, "result": result,
                                    "total_budget": total})
    return {"route": route, "result": result, "shown": shown, "total_budget": total, "log": al}


# Fixed, offline workload (no now()). First 5 are all-UTC; last 3 need tz/DST.
WORKLOAD = [
    {"op": "add", "at": {"iso": "2026-01-31T23:59:59", "tz": "UTC"}, "seconds": 1},
    {"op": "add", "at": {"iso": "2024-02-28T12:00:00", "tz": "UTC"}, "seconds": 86400 * 2},   # leap day
    {"op": "add", "at": {"iso": "1999-12-31T23:00:00", "tz": "UTC"}, "seconds": 7200},
    {"op": "diff", "a": {"iso": "2026-01-01T00:00:00", "tz": "UTC"},
     "b": {"iso": "2026-09-29T06:30:00", "tz": "UTC"}},
    {"op": "diff", "a": {"iso": "1969-07-20T20:17:40", "tz": "UTC"},
     "b": {"iso": "1970-01-01T00:00:00", "tz": "UTC"}},                                      # pre-epoch
    {"op": "add", "at": {"iso": "2026-03-08T01:30:00", "tz": "America/New_York"}, "seconds": 3600},  # spring-forward
    {"op": "diff", "a": {"iso": "2026-11-01T00:30:00", "tz": "America/New_York"},
     "b": {"iso": "2026-11-01T03:30:00", "tz": "America/New_York"}},                          # 4h across fall-back
    {"op": "add", "at": {"iso": "2026-06-01T12:00:00", "tz": "Asia/Kolkata"}, "seconds": 0},
]


if __name__ == "__main__":
    for req in WORKLOAD:
        r = run(req)
        b = r["total_budget"]
        print(f"{req['op']:5s} -> {r['shown']:>22s} via {r['route']:4s} "
              f"(wall_ms={b['wall_ms']}, prod_bytes={b['storage_bytes']['prod']})")
