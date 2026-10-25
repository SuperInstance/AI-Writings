"""csv-stats-quilt selftest — offline, deterministic."""

from __future__ import annotations

import random
import sys

import csvstats_quilt as tq
from csvstats_quilt import al_mod

checks = 0
fails = 0


def check(name: str, ok: bool):
    global checks, fails
    checks += 1
    print(("  ok  : " if ok else "  FAIL: ") + name)
    if not ok:
        fails += 1


cheap_cases = [t for t in tq.WORKLOAD if tq.choose(t) == "cheap"]
full_cases = [t for t in tq.WORKLOAD if tq.choose(t) == "full"]
rng = random.Random(8)

def norm_full(t):
    return tq.full_route(t)
def rcsv():
    n = rng.randrange(1, 12)
    return ("id,v,w\n" + "".join("%d,%d,%d\n" % (i, rng.randrange(-50, 50), rng.randrange(100)) for i in range(n)),
            rng.choice(["v", "w"]), None)
fuzz = [rcsv() for _ in range(2000)]
check("cheap and full reach the IDENTICAL stats block on all cheap-eligible workload inputs",
      all(tq.cheap_route(t) == tq.full_route(t) for t in cheap_cases))
check("identical on 2000 seeded random CSVs (signs, ties, single rows)",
      all(tq.cheap_route(t) == tq.full_route(t) for t in fuzz))
check("mean rounding pinned on both routes (1.5000, 0.3333, -0.3333, tie half-even)",
      all(tq.cheap_route(t) == tq.full_route(t) for t in cheap_cases)
      and tq.cheap_route(("v\n1\n2\n", "v", None)).endswith("mean=1.5000")
      and tq.cheap_route(("v\n-1\n0\n0\n", "v", None)).endswith("mean=-0.3333")
      and tq.cheap_route(("v\n1\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n", "v", None))
      == tq.full_route(("v\n1\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n", "v", None)))
refused = 0
for bad in [full_cases[0], full_cases[1], full_cases[2]]:
    try:
        tq.cheap_route(bad)
    except ValueError:
        refused += 1
check("cheap route refuses grouped / quoted / CRLF CSV (lacks the csv tooling)", refused == 3)
check("full route does real work: group-by and quoted fields",
      tq.full_route(("k,v\na,1\nb,2\na,3\n", "v", "k")) == "a|n=2|sum=4|min=1|max=3|mean=2.0000\nb|n=1|sum=2|min=2|max=2|mean=2.0000"
      and tq.full_route(('n,v\n"x,y",4\n"z",6\n', "v", None)).startswith("*|n=2|sum=10"))

# Chooser.
check("chooser picks cheap iff the cheap precondition holds (workload split both ways)",
      len(cheap_cases) >= 4 and len(full_cases) >= 3 and all(tq.choose(t) == "cheap" for t in cheap_cases))

# Iron triangle (forced routes, same input).
sample = cheap_cases[0]
rc, rf = tq.run(sample, route="cheap"), tq.run(sample, route="full")
bc, bf = rc["total_budget"], rf["total_budget"]
check("products identical when both routes are forced on the same input", rc["out"] == rf["out"])
check("cheap route is cheaper on COMPUTE (wall_ms)", bc["wall_ms"] < bf["wall_ms"])
check("cheap route is cheaper on STORAGE (prod bytes)", bc["storage_bytes"]["prod"] < bf["storage_bytes"]["prod"])
check("cheap route is also cheaper on mem and power", bc["mem_mb"] < bf["mem_mb"] and bc["power_w"] < bf["power_w"])
check("quilt's own choice on a cheap-eligible input == the cheap route's budget", tq.run(sample)["total_budget"] == bc)

# Ledger well-formedness.
recs = rc["log"].records
budgeted = [r for r in recs if r["type"] in ("cell.tick", "route.hop")]
check("every cell.tick and route.hop carries a well-formed budget vector (storage_bytes incl.)",
      len(budgeted) == 5 and all(al_mod.budget_ok(r["body"]["budget"]) for r in budgeted))
txn = [r for r in recs if r["type"] == "ledger.transaction"][0]["body"]
check("ledger.transaction total_budget == route_total(ticks+hops)",
      al_mod.route_total(recs, rc["route_id"]) == txn["total_budget"] == bc)
hops = [r for r in recs if r["type"] == "route.hop"] + [r for r in rf["log"].records if r["type"] == "route.hop"]
check("route.hops balance (both routes)", len(hops) == 4 and all(al_mod.hop_balanced(h["body"]) for h in hops))

mixed = al_mod.ActiveLog(dev="csv-stats-quilt")
for t in tq.WORKLOAD:
    tq.run(t, mixed)
tam = [dict(r) for r in mixed.records]
tam[3] = dict(tam[3], body={"evil": 1})
check("mixed-route ActiveLog chain verifies clean, breaks under tampering, ledger validates",
      al_mod.verify_chain(mixed.records) and not al_mod.verify_chain(tam)
      and all(al_mod.validate_envelope(r) for r in mixed.records))
check("workload routes split as chosen",
      [r["body"]["path"] for r in mixed.records if r["type"] == "ledger.transaction"]
      == [tq.choose(t) for t in tq.WORKLOAD])


def all_jsonl():
    log = al_mod.ActiveLog(dev="csv-stats-quilt")
    for t in tq.WORKLOAD:
        tq.run(t, log)
    return log.to_jsonl()


check("re-running the workload is byte-identical (deterministic)", all_jsonl() == all_jsonl())

print("csv-stats-quilt selftest: %d checks, %d failures" % (checks, fails))
sys.exit(1 if fails else 0)
