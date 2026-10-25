"""datetime-quilt selftest — offline, deterministic (fixed inputs, no now())."""

from __future__ import annotations

import sys

import datetime_quilt as dq
from activeledger import ActiveLog, budget_ok, hop_balanced, verify_chain, route_total

checks = 0
fails = 0


def check(name: str, ok: bool):
    global checks, fails
    checks += 1
    fails += 0 if ok else 1
    print(("  ok  : " if ok else "  FAIL: ") + name)


utc_cases = [r for r in dq.WORKLOAD if dq.all_utc(r)]
tz_cases = [r for r in dq.WORKLOAD if not dq.all_utc(r)]

check("workload has both all-UTC and non-UTC cases", len(utc_cases) >= 4 and len(tz_cases) >= 2)

check("utc and full routes reach the IDENTICAL instant on every all-UTC case",
      all(dq.utc_route(r) == dq.full_route(r) for r in utc_cases))

check("utc route matches a known epoch (2026-09-29T06:30Z = 1790663400)",
      dq.utc_epoch({"iso": "2026-09-29T06:30:00", "tz": "UTC"}) == 1790663400
      and dq.full_epoch({"iso": "2026-09-29T06:30:00", "tz": "UTC"}) == 1790663400)

try:
    dq.utc_route(tz_cases[0])
    refused = False
except dq.NeedsTZ:
    refused = True
check("utc route refuses a non-UTC input (NeedsTZ)", refused)

check("chooser picks utc iff EVERY input is UTC, else full",
      all(dq.choose(r) == "utc" for r in utc_cases)
      and all(dq.choose(r) == "full" for r in tz_cases)
      and dq.choose({"op": "diff", "a": {"iso": "2026-01-01T00:00:00", "tz": "UTC"},
                     "b": {"iso": "2026-01-01T00:00:00", "tz": "Asia/Kolkata"}}) == "full")

check("full route is genuinely tz-aware: NY spring-forward add and fall-back diff",
      dq.render_utc(dq.full_route(tz_cases[0])) == "2026-03-08T07:30:00Z"
      and dq.full_route(tz_cases[1]) == 4 * 3600)   # 00:30 EDT -> 03:30 EST is 4 real hours

sample = utc_cases[0]
ru, rf = dq.run(sample), dq.run(sample, force="full")
bu, bf = ru["total_budget"], rf["total_budget"]
check("forced full route reaches the same result as the chosen utc route",
      ru["route"] == "utc" and rf["route"] == "full" and ru["result"] == rf["result"])
check("utc route is cheaper on COMPUTE (wall_ms) than full",
      bu["wall_ms"] < bf["wall_ms"])
check("utc route is cheaper on STORAGE (prod bytes) than full",
      bu["storage_bytes"]["prod"] < bf["storage_bytes"]["prod"]
      and bu["storage_bytes"]["train"] < bf["storage_bytes"]["train"])

recs = ru["log"].records
budgeted = [r for r in recs if r["type"] in ("cell.tick", "route.hop")]
check("every cell.tick and route.hop carries a well-formed budget vector",
      len(budgeted) == 5 and all(budget_ok(r["body"]["budget"]) for r in budgeted))

txn = [r for r in recs if r["type"] == "ledger.transaction"][0]["body"]
check("ledger.transaction total_budget == sum of the route's records == declared cost model",
      txn["total_budget"] == route_total(recs, txn["route"]) == dq.route_cost("utc"))

check("every route.hop balances after translation",
      all(hop_balanced(r["body"]) for r in recs if r["type"] == "route.hop"))

good = verify_chain(recs)
bad = [dict(r) for r in recs]
bad[1] = dict(bad[1], body={"cell": "evil"})
check("ActiveLog chain verifies clean AND breaks under tampering", good and not verify_chain(bad))


def run_all() -> str:
    return "".join(dq.run(r)["log"].to_jsonl() for r in dq.WORKLOAD)


check("re-running the whole workload is byte-identical", run_all() == run_all())

print(f"datetime-quilt selftest: {checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
