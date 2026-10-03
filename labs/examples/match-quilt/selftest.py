"""match-quilt selftest — offline, deterministic."""

from __future__ import annotations

import random
import sys

import match_quilt as tq
from match_quilt import al_mod

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
rng = random.Random(6)

# Seeded fuzz on literal patterns over a small alphabet (forces overlaps, repeats, misses).
alpha = "ab c.é"
def lit():
    while True:
        p = "".join(rng.choice(alpha) for _ in range(rng.randrange(1, 4)))
        if tq.choose((p, "")) == "cheap":
            return p
fuzz = [(lit(), "".join(rng.choice(alpha) for _ in range(rng.randrange(0, 30)))) for _ in range(3000)]
check("cheap and full reach the IDENTICAL span list on all cheap-eligible workload inputs",
      all(tq.cheap_route(t) == tq.full_route(t) for t in cheap_cases))
check("identical on 3000 seeded literal pattern/text pairs (overlap, repeat, miss, unicode)",
      all(tq.cheap_route(t) == tq.full_route(t) for t in fuzz))
check("non-overlapping semantics pinned: 'aa' in 'aaaaa' -> 0-2,2-4 on both routes",
      tq.cheap_route(("aa", "aaaaa")) == tq.full_route(("aa", "aaaaa")) == "0-2,2-4")
refused = 0
for bad in [("", "x"), ("a.c", "abc"), ("a|b", "a")]:
    try:
        tq.cheap_route(bad)
    except ValueError:
        refused += 1
check("cheap route refuses empty/metachar patterns (lacks the regex tooling)", refused == 3)
check("full route does real regex work (anchors, classes, groups, dot)",
      tq.full_route(("c.t", "cat cot cut c.t")) == "0-3,4-7,8-11,12-15"
      and tq.full_route(("^the", "the end the")) == "0-3"
      and tq.full_route(("[ae]+", "beaten leaves")) == "1-3,4-5,8-10,11-12")

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

mixed = al_mod.ActiveLog(dev="match-quilt")
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
    log = al_mod.ActiveLog(dev="match-quilt")
    for t in tq.WORKLOAD:
        tq.run(t, log)
    return log.to_jsonl()


check("re-running the workload is byte-identical (deterministic)", all_jsonl() == all_jsonl())

print("match-quilt selftest: %d checks, %d failures" % (checks, fails))
sys.exit(1 if fails else 0)
