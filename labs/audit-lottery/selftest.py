#!/usr/bin/env python3
"""selftest for audit-lottery. Prints 'audit-lottery selftest: N checks, 0 failures'."""
import json
import random
import sys

import audit_lottery as A

N = F = 0


def check(name, ok):
    global N, F
    N += 1
    if not ok:
        F += 1
        print("FAIL", name)


# product identity of the shipped quilt, and the lazy route's drift
items = A.make_stream(3000, 0, 0.5, seed=4)
check("guarded cheap route is product-identical to exact on 3000 mixed items",
      all(A.guarded_cheap(x) == A.exact_route(x) for x in items))
asc = A.make_stream(2000, None, 0.0, seed=5)
check("lazy route agrees on all ASCII", all(A.lazy_cheap(x) == A.exact_route(x) for x in asc))
bad = [u for u in A.UNICODE_POOL if A.lazy_cheap(u) != A.exact_route(u)]
check("lazy route diverges on some unicode (Straße, ligatures, fullwidth…)", len(bad) >= 4)
check("lazy route agrees on some unicode too (naïve café)", len(bad) < len(A.UNICODE_POOL))

# draw sources
s = A.PublicSeedDraws(9)
pk = s.peek(8)
check("public seed is predictable: peek == next draw", pk == s.bits(8))
check("secret source is flagged unpredictable", A.SecretDraws.predictable is False)
p = A.PoolDraws("a5ff", "t")
check("pool bit reader MSB-first", p.bits(4) == 0xA and p.bits(4) == 0x5 and p.bits(8) == 0xFF)
try:
    p.bits(1)
    check("pool exhaustion raises", False)
except A.Exhausted:
    check("pool exhaustion raises", True)

# e-processes
e = A.BernoulliEProcess(0.01, 0.05)
for _ in range(500):
    e.update(0)
check("clean audits never revoke", not e.crossed and e.max == 1.0)
e.update(1)
check("one disagreement after 500 clean audits does NOT revoke (wealth drained)", not e.crossed)
e2 = A.BernoulliEProcess(0.01, 0.05)
e2.update(1)
check("a disagreement on the very first audit revokes (prob <= eps under H0)", e2.crossed)
rng = random.Random(1)
fired = 0
for _ in range(300):
    d = A.BernoulliEProcess(0.01, 0.05)
    for _ in range(1000):
        d.update(1 if rng.random() < 0.01 else 0)
        if d.crossed:
            fired += 1
            break
check("Ville validity at the boundary q=eps: false revocation <= delta (+MC slack)", fired / 300 <= 0.08)
tot = 0.0
for _ in range(400):
    d = A.SRDetector(0.01, 1e9)
    for _ in range(50):
        d.update(1 if rng.random() < 0.01 else 0)
    tot += d.value
check("SR e-detector: E[R_50] <= 50 under H0 (MC)", tot / 400 <= 50 * 1.25)

# receipts
res = A.run_stream(A.make_stream(300, 0, 0.5, 2), lambda x, _: A.lazy_cheap(x), A.PublicSeedDraws(3), 0.25)
check("chain verifies", res["chain"].verify()[0])
check("COMMIT->DRAW->AUDIT order holds", res["chain"].order_ok()[0])
res2 = A.run_stream(A.make_stream(300, 0, 0.5, 2), lambda x, _: A.lazy_cheap(x), A.PublicSeedDraws(3), 0.25)
check("deterministic under a fixed seed (same head)", res["chain"].head == res2["chain"].head)
check("LICENSE REVOKED record written", any(r["rel"] == "LICENSE" for r in res["chain"].records))
t = A.exp_tamper()
check("in-place edit breaks the hash chain", t["edit_detected"])
check("answer swapped after draw: chain still hash-valid", t["swap_chain_still_valid"])
check("…but COMMIT/AUDIT consistency catches it", t["swap_detected_by_order_check"])
c = A.Chain()
c.append("DRAW", {"item": 0, "value": 1})
c.append("COMMIT", {"item": 0, "out_hash": "0x0"})
check("DRAW before COMMIT is rejected", not c.order_ok()[0])

# the two headline effects
st = A.exp_strategic(R=20, N=1500)
pub, sec = st["public-seed + oracle"], st["secret + blind cheat"]
check("public-seed audits: oracle cheater never revoked", pub["revoked_frac"] == 0.0)
check("public-seed audits: oracle cheater serves >85% wrong", pub["harm_frac_of_N"] > 0.85)
check("secret audits: blind cheater always revoked", sec["revoked_frac"] == 1.0)
check("secret audits: harm < 3% of N", sec["harm_frac_of_N"] < 0.03)
tc = A.exp_trust_credit(R=12, onsets=(0, 12000), post=2500)
v0, v1, s1 = tc["rows"][0]["ville"], tc["rows"][1]["ville"], tc["rows"][1]["sr"]
check("trust credit: Ville is slower (or misses) after a long honest past",
      v1["missed_frac"] > 0.5 or v1["detect_delay_mean"] > 2 * v0["detect_delay_mean"])
check("SR catches the late drift in every run", s1["missed_frac"] == 0.0)
check("SR no false alarm before onset", s1["false_before_onset"] == 0)
d = A.exp_drift(R=20, N=2000, onset=800)
check("drift: revoked in every run, never before onset", d["revoked_frac"] == 1.0 and d["revoked_before_onset"] == 0)
check("drift: cheaper than always-exact", d["cost_mean"] < d["cost_always_exact"])
check("drift: >2x fewer wrong products than no audit", d["harm_no_audit"] > 2 * d["harm_mean"])

# live Moth fixture (if present)
m = A.exp_live_moth()
if "skipped" not in m:
    fx = json.load(open(A.os.path.join(A.HERE, "moth_draws.json")))
    check("moth fixture carries its commitment + honest mode", fx["commitment"]["commit"] and fx["mode"] == "emu")
    check("live-draw run: chain + order ok", m["chain_ok"] and m["order_ok"])

print("audit-lottery selftest: %d checks, %d failures" % (N, F))
sys.exit(1 if F else 0)
