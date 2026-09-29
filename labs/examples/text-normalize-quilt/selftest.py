"""text-normalize-quilt selftest — offline, deterministic."""

from __future__ import annotations

import random
import sys

import textnorm_quilt as tq
from textnorm_quilt import al_mod

checks = 0
fails = 0


def check(name: str, ok: bool):
    global checks, fails
    checks += 1
    if not ok:
        fails += 1
        print("  FAIL: " + name)
    else:
        print("  ok  : " + name)


ascii_cases = [t for t in tq.WORKLOAD if t.isascii()]
uni_cases = [t for t in tq.WORKLOAD if not t.isascii()]

# 1. Identity on the shared workload cases.
check("cheap and full routes reach the IDENTICAL string on all pure-ASCII workload inputs",
      len(ascii_cases) >= 5 and all(tq.cheap_route(t) == tq.full_route(t) for t in ascii_cases))

# 2. Exhaustive: every ASCII code point, alone and flanked by text.
exh = all(tq.cheap_route(c) == tq.full_route(c)
          and tq.cheap_route("A%sB" % c) == tq.full_route("A%sB" % c)
          and tq.cheap_route(" %s " % c) == tq.full_route(" %s " % c)
          for c in map(chr, range(128)))
check("identical on ALL 128 ASCII code points (incl. 0x1c-0x1f controls) in 3 contexts", exh)

# 3. Seeded fuzz over the ASCII alphabet.
rng = random.Random(4)
fuzz = ["".join(chr(rng.randrange(128)) for _ in range(rng.randrange(0, 40))) for _ in range(2000)]
check("identical on 2000 seeded random ASCII strings", all(tq.cheap_route(t) == tq.full_route(t) for t in fuzz))

# 4. Cheap refuses non-ASCII; full handles it and genuinely differs from a naive lower().
refused = False
try:
    tq.cheap_route("café")
except ValueError:
    refused = True
check("cheap route refuses non-ASCII input (lacks the tooling)", refused)
check("full route needs the unicode path: NFKC/casefold/unicode-whitespace do real work",
      tq.full_route("Straße  ﬁne  Ⅷ  ＡＢＣ") == "strasse fine viii abc"
      and tq.full_route("a 　b") == "a b")

# 5. Chooser.
check("chooser picks cheap iff input is pure ASCII",
      all(tq.choose(t) == "cheap" for t in ascii_cases + fuzz[:200])
      and all(tq.choose(t) == "full" for t in uni_cases)
      and tq.choose("x\u0080") == "full" and tq.choose("x\x7f") == "cheap")

# 6. Iron triangle: cheap cheaper on compute AND storage (same input, forced routes).
sample = "  Hello,   World!  "
rc = tq.run(sample, route="cheap")
rf = tq.run(sample, route="full")
bc, bf = rc["total_budget"], rf["total_budget"]
check("products identical when both routes are forced on the same ASCII input", rc["out"] == rf["out"] == "hello, world!")
check("cheap route is cheaper on COMPUTE (wall_ms)", bc["wall_ms"] < bf["wall_ms"])
check("cheap route is cheaper on STORAGE (prod bytes)", bc["storage_bytes"]["prod"] < bf["storage_bytes"]["prod"])
check("cheap route is also cheaper on mem and power", bc["mem_mb"] < bf["mem_mb"] and bc["power_w"] < bf["power_w"])
check("quilt's own choice on ASCII input == the cheap route's budget", tq.run(sample)["total_budget"] == bc)

# 7. Budgets well-formed; route total reconciles with the ledger.transaction.
recs = rc["log"].records
budgeted = [r for r in recs if r["type"] in ("cell.tick", "route.hop")]
check("every cell.tick and route.hop carries a well-formed budget vector (storage_bytes incl.)",
      len(budgeted) == 5 and all(al_mod.budget_ok(r["body"]["budget"]) for r in budgeted))
txn = [r for r in recs if r["type"] == "ledger.transaction"][0]["body"]
check("ledger.transaction total_budget == route_total(ticks+hops)",
      al_mod.route_total(recs, rc["route_id"]) == txn["total_budget"] == bc)

# 8. Double entry.
hops = [r for r in recs if r["type"] == "route.hop"]
check("route.hops balance after translation (both routes)",
      len(hops) == 2 and all(al_mod.hop_balanced(h["body"]) for h in hops)
      and all(al_mod.hop_balanced(h["body"]) for h in rf["log"].records if h["type"] == "route.hop"))

# 9. Chain tamper-evident (also on a mixed-route log).
mixed = al_mod.ActiveLog(dev="text-normalize-quilt")
for t in tq.WORKLOAD:
    tq.run(t, mixed)
tam = [dict(r) for r in mixed.records]
tam[3] = dict(tam[3], body={"evil": 1})
check("mixed-route ActiveLog chain verifies clean, breaks under tampering, ledger validates",
      al_mod.verify_chain(mixed.records) and not al_mod.verify_chain(tam)
      and all(al_mod.validate_envelope(r) for r in mixed.records))
check("workload routes split as expected (cheap for ASCII, full for unicode)",
      [r["body"]["path"] for r in mixed.records if r["type"] == "ledger.transaction"]
      == [tq.choose(t) for t in tq.WORKLOAD])

# 10. Determinism.
def all_jsonl():
    log = al_mod.ActiveLog(dev="text-normalize-quilt")
    for t in tq.WORKLOAD:
        tq.run(t, log)
    return log.to_jsonl()

check("re-running the workload is byte-identical (deterministic)", all_jsonl() == all_jsonl())

print("text-normalize-quilt selftest: %d checks, %d failures" % (checks, fails))
sys.exit(1 if fails else 0)
