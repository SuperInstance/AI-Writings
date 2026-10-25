"""image-thumb-quilt selftest — offline, deterministic."""

from __future__ import annotations

import sys

import thumb_quilt as tq
from activeledger import (ZERO_BUDGET, add_budget, budget_ok, hop_balanced, verify_chain)

checks = fails = 0


def check(name, ok):
    global checks, fails
    checks += 1
    if not ok:
        fails += 1
    print(("  ok  : " if ok else "  FAIL: ") + name)


small = [(i, t) for i, t in tq.WORKLOAD if tq.fits(i, t)]
big = [(i, t) for i, t in tq.WORKLOAD if not tq.fits(i, t)]

check("workload has both already-small and oversize sources", len(small) >= 2 and len(big) >= 1)

check("pass-through and resample reach the IDENTICAL thumbnail when source <= target",
      all(tq.passthrough_route(i, t) == tq.resample_route(tq.encode(i), t) for i, t in small))
check("decode(encode(img)) round-trips", all(tq.decode(tq.encode(i)) == i for i, _ in tq.WORKLOAD))

try:
    tq.passthrough_route(*big[0])
    refused = False
except tq.NeedsResample:
    refused = True
check("pass-through refuses an oversize source (lacks resample tooling)", refused)

check("resample fits the target and preserves aspect for oversize sources",
      all(tq.fits(tq.resample_route(tq.encode(i), t), t) for i, t in big)
      and tq.resample_route(tq.encode(big[-1][0]), big[-1][1])["w"]
      == 2 * tq.resample_route(tq.encode(big[-1][0]), big[-1][1])["h"])
check("chooser picks pass-through iff source <= target",
      all(tq.choose(i, t) == "passthrough" for i, t in small)
      and all(tq.choose(i, t) == "resample" for i, t in big)
      and tq.choose(tq.make_image(9, 1), (8, 8)) == "resample"
      and tq.choose(tq.make_image(1, 9), (8, 8)) == "resample")

img, tgt = small[0]
rc = tq.run(img, tgt)
rf = tq.run(img, tgt, force="resample")
check("quilt run picks the cheap route on a small source", rc["route"] == "passthrough")
check("both routes' run() yield the identical thumbnail on a small source",
      rc["thumb"] == rf["thumb"] == img)
bc, bf = rc["total_budget"], rf["total_budget"]
check("cheap route is cheaper on COMPUTE (wall_ms)", bc["wall_ms"] < bf["wall_ms"])
check("cheap route is cheaper on STORAGE (prod bytes)",
      bc["storage_bytes"]["prod"] < bf["storage_bytes"]["prod"])
check("cheap route is cheaper on train storage too",
      bc["storage_bytes"]["train"] < bf["storage_bytes"]["train"])

recs = rc["log"].records
budgeted = [r for r in recs if r["type"] in ("cell.tick", "route.hop")]
check("every cell.tick and route.hop carries a well-formed budget vector",
      len(budgeted) > 0 and all(budget_ok(r["body"]["budget"]) for r in budgeted))
resum = ZERO_BUDGET
for r in budgeted:
    resum = add_budget(resum, r["body"]["budget"])
declared = [r for r in recs if r["type"] == "ledger.transaction"][0]["body"]["total_budget"]
check("ledger.transaction total_budget == sum of its records' budgets",
      resum == declared == bc)
check("every route.hop balances after translation",
      all(hop_balanced(r["body"]) for r in recs if r["type"] == "route.hop")
      and all(hop_balanced(r["body"]) for r in rf["log"].records if r["type"] == "route.hop"))

check("ActiveLog chain verifies clean", verify_chain(recs))
bad = [dict(r) for r in recs]
bad[1] = dict(bad[1], body={"cell": "evil"})
check("chain breaks under tampering", not verify_chain(bad))


def all_jsonl():
    return "".join(tq.run(i, t)["log"].to_jsonl() for i, t in tq.WORKLOAD)


check("re-running the workload is byte-identical", all_jsonl() == all_jsonl())

# workload-level: cheap route only on small sources, and total prod bytes reflect it
tot = {r: 0 for r in ("passthrough", "resample")}
for i, t in tq.WORKLOAD:
    o = tq.run(i, t)
    tot[o["route"]] += o["total_budget"]["storage_bytes"]["prod"]
check("workload booked pass-through for small and resample for oversize",
      len({tq.run(i, t)["route"] for i, t in small}) == 1
      and {tq.run(i, t)["route"] for i, t in big} == {"resample"})

print(f"image-thumb-quilt selftest: {checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
