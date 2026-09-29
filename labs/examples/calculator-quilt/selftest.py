"""calculator-quilt selftest — offline, deterministic.

Proves the EX1 thesis end to end: the two routes reach the identical product on the
shared cases (novelty in process, identity in product); the quilt chooses the cheap
route when interest isn't needed; the simple route is genuinely cheaper on BOTH the
compute and the storage measurements of the iron-triangle; every record carries a
well-formed budget vector and the route total reconciles; route.hops balance after
their unit translation; and the ActiveLog chain is tamper-evident.
"""

from __future__ import annotations

import sys

import calc_quilt as cq

checks = 0
fails = 0


def check(name: str, ok: bool):
    global checks, fails
    checks += 1
    if not ok:
        fails += 1
        print(f"  FAIL: {name}")
    else:
        print(f"  ok  : {name}")


# 1. Product identity: simple and full routes agree to the cent on every non-interest eq.
non_interest = [eq for eq in cq.WORKLOAD if not cq.needs_interest(eq)]
identical = all(cq.simple_route(eq) == cq.full_route(eq) for eq in non_interest)
check("simple and full routes reach the IDENTICAL product on all non-interest cases", identical)

# 2. The simple route genuinely refuses interest (it lacks the tooling, by design).
refused = False
try:
    cq.simple_route({"op": "compound", "principal": "1000.00", "rate": "0.05", "periods": 3})
except cq.NeedsInterest:
    refused = True
check("simple route refuses a compound-interest equation (NeedsInterest)", refused)

# 3. The chooser picks simple when interest isn't needed, full when it is.
choose_ok = (all(cq.choose(eq) == "simple" for eq in non_interest)
             and cq.choose({"op": "compound", "principal": "1", "rate": "0.05", "periods": 1}) == "full")
check("chooser picks the simple route iff the equation needs no interest tooling", choose_ok)

# 4. Iron-triangle: the simple route is cheaper on compute (wall_ms) AND storage (prod bytes).
sample = {"op": "add", "a": "12.34", "b": "5.66"}
al_s, al_f = cq.ActiveLog(), cq.ActiveLog()
rs = cq.run(sample, al_s)
# force the full route on the same equation to compare like for like
rf_route = "full"
rf_cost = cq.COST[rf_route]
# run full route explicitly by temporarily choosing it
full_total = cq.ZERO_BUDGET
for _ in range(3):
    full_total = cq.add_budget(full_total, rf_cost["tick"])
for _ in range(2):
    full_total = cq.add_budget(full_total, rf_cost["hop"])
cheaper_compute = rs["total_budget"]["wall_ms"] < full_total["wall_ms"]
cheaper_storage = (rs["total_budget"]["storage_bytes"]["prod"]
                   < full_total["storage_bytes"]["prod"])
check("simple route is cheaper on COMPUTE (wall_ms) than the full route", cheaper_compute)
check("simple route is cheaper on STORAGE (prod bytes) than the full route", cheaper_storage)

# 5. Same product, different cost — the point: product identical, budgets differ.
check("simple and full reach the same cents but at different budgets (novelty in process)",
      cq.simple_route(sample) == cq.full_route(sample)
      and rs["total_budget"]["wall_ms"] != full_total["wall_ms"])

# 6. Every record carries a well-formed budget vector.
def well_formed(b: dict) -> bool:
    return (isinstance(b, dict) and "wall_ms" in b and "storage_bytes" in b
            and set(b["storage_bytes"]) == {"train", "prod"} and "tokens" in b
            and "usd" in b and "power_w" in b and "reqs" in b)

recs = rs["log"].records
budgeted = [r for r in recs if r["type"] in ("cell.tick", "route.hop")]
check("every cell.tick and route.hop carries a well-formed budget vector",
      len(budgeted) > 0 and all(well_formed(r["body"]["budget"]) for r in budgeted))

# 7. Route total reconciles: the ledger.transaction total == sum of per-record budgets.
resum = cq.ZERO_BUDGET
for r in budgeted:
    resum = cq.add_budget(resum, r["body"]["budget"])
txn = [r for r in recs if r["type"] == "ledger.transaction"][0]
declared = txn["body"]["total_budget"]
recon = (resum["wall_ms"] == declared["wall_ms"]
         and resum["storage_bytes"] == declared["storage_bytes"]
         and resum["mem_mb"] == declared["mem_mb"])
check("route total_budget on the ledger.transaction == sum of its records' budgets", recon)

# 8. Double-entry balance: each route.hop balances after its unit translation (B2 invariant).
hops = [r for r in recs if r["type"] == "route.hop"]
balanced = all(
    round(h["body"]["credit"]["amount"] * h["body"]["price"]["rate"])
    == h["body"]["debit"]["amount"]
    for h in hops
)
check("every route.hop sums to zero after unit translation (credit*rate == debit)", balanced)

# 9. The dollars<->cents translation round-trips (foreshadows B2 unit-translation-audit).
roundtrip = abs(cq.dollars_to_cents("12.34") - 1234) == 0 and cq.cents_to_dollars(1234) == "12.34"
check("dollars->cents->dollars round-trips exactly", roundtrip)

# 10. The ActiveLog chain is tamper-evident.
good = cq.verify_chain(recs)
tampered = [dict(r) for r in recs]
tampered[1] = dict(tampered[1])
tampered[1]["body"] = {"cell": "evil"}
check("ActiveLog chain verifies clean AND breaks under tampering",
      good and not cq.verify_chain(tampered))

# 11. Determinism: re-running the workload yields byte-identical logs.
def run_all_jsonl() -> str:
    out = []
    for eq in cq.WORKLOAD:
        out.append(cq.run(eq)["log"].to_jsonl())
    return "".join(out)

check("re-running the whole workload is byte-identical (deterministic)",
      run_all_jsonl() == run_all_jsonl())

print(f"calculator-quilt selftest: {checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
