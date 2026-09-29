"""convert-quilt selftest — offline, deterministic."""

from __future__ import annotations

import sys

import convert_quilt as cq
al = cq.al

checks = fails = 0


def check(name, ok):
    global checks, fails
    checks += 1
    if not ok:
        fails += 1
    print(("  ok  : " if ok else "  FAIL: ") + name)


same = [r for r in cq.WORKLOAD if r["src"] == r["dst"]]
diff = [r for r in cq.WORKLOAD if r["src"] != r["dst"]]

# 1. identical product across routes on src==target
check("cheap and full routes give the IDENTICAL product on all src==target cases",
      len(same) >= 3 and all(cq.cheap_route(r["value"], r["src"], r["dst"])
                             == cq.full_route(r["value"], r["src"], r["dst"]) for r in same))
check("run() products identical when the full route is forced on src==target",
      all(cq.run(r)["product"] == cq.run(r, force="full")["product"] for r in same))

# 2. chooser
check("chooser picks cheap iff src==target",
      all(cq.choose(r["src"], r["dst"]) == "cheap" for r in same)
      and all(cq.choose(r["src"], r["dst"]) == "full" for r in diff))
check("run() routes follow the chooser", all(cq.run(r)["route"] == cq.choose(r["src"], r["dst"])
                                              for r in cq.WORKLOAD))

# 3. cheap route refuses a real conversion
try:
    cq.cheap_route("1", "m", "ft"); refused = False
except ValueError:
    refused = True
check("cheap route refuses src != target", refused)

# 4. known conversions correct
check("full table: 100 cm = 39.370079 in", cq.full_route("100", "cm", "in") == "39.370079")
check("full table: 100 C = 212.000000 F", cq.full_route("100", "C", "F") == "212.000000")
check("full table: 10 lb = 4.535924 kg", cq.full_route("10", "lb", "kg") == "4.535924")
check("full table: 300 K = 26.850000 C", cq.full_route("300", "K", "C") == "26.850000")
try:
    cq.full_route("1", "m", "kg"); bad = False
except ValueError:
    bad = True
check("cross-dimension conversion rejected", bad)

# 5. cheaper on compute AND storage
s = same[0]
rc, rf = cq.run(s), cq.run(s, force="full")
tc, tf = rc["total_budget"], rf["total_budget"]
check("cheap route cheaper on COMPUTE (wall_ms)", tc["wall_ms"] < tf["wall_ms"])
check("cheap route cheaper on STORAGE (prod bytes)",
      tc["storage_bytes"]["prod"] < tf["storage_bytes"]["prod"])
check("cheap route cheaper on STORAGE (train bytes)",
      tc["storage_bytes"]["train"] < tf["storage_bytes"]["train"])

# 6. well-formed budget vectors on every record
allrecs = [x for r in cq.WORKLOAD for x in cq.run(r)["log"].records]
bud = [x for x in allrecs if x["type"] in ("cell.tick", "route.hop")]
check("every cell.tick/route.hop has a well-formed budget vector (incl storage train+prod)",
      bud and all(al.budget_ok(x["body"]["budget"]) for x in bud))

# 7. total reconciles
ok = True
for r in cq.WORKLOAD:
    o = cq.run(r)
    txn = [x for x in o["log"].records if x["type"] == "ledger.transaction"][0]
    ok &= txn["body"]["total_budget"] == al.route_total(o["log"].records, o["route"])
check("ledger.transaction total_budget == sum of the route's record budgets", ok)

# 8. hops balance after translation
hops = [x for x in allrecs if x["type"] == "route.hop"]
check("every route.hop balances after unit translation",
      hops and all(al.hop_balanced(h["body"]) for h in hops))
check("every route.hop carries a unit-translation price {from,to,rate}",
      all({"from", "to", "rate"} <= set(h["body"]["price"]) for h in hops))
check("cheap identity hop has rate 1.0 and credit==debit",
      all(h["body"]["price"]["rate"] == 1.0 and h["body"]["credit"]["amount"] == h["body"]["debit"]["amount"]
          for h in [x for x in cq.run(s)["log"].records if x["type"] == "route.hop"]))

# 9. chain tamper-evident
recs = cq.run(diff[0])["log"].records
tam = [dict(r) for r in recs]
tam[1] = dict(tam[1], body={"cell": "evil"})
check("chain verifies clean AND breaks under tampering", al.verify_chain(recs) and not al.verify_chain(tam))
check("envelopes are valid ActiveLog v1", all(al.validate_envelope(r) for r in recs))

# 10. determinism
def blob():
    return "".join(cq.run(r)["log"].to_jsonl() for r in cq.WORKLOAD)
check("re-running the workload is byte-identical", blob() == blob())

print("convert-quilt selftest: %d checks, %d failures" % (checks, fails))
sys.exit(1 if fails else 0)
