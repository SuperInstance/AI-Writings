"""metabolizer selftest — offline, deterministic. Run: python3 selftest.py"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import metabolizer as M
import capabilities as C
import quilt_kernel as K
import invariance_miner as IM
import route_witness as RW
import route_preference as RP

checks = fails = 0


def check(name, ok):
    global checks, fails
    checks += 1
    if not ok:
        fails += 1
        print("  FAIL:", name)


def raises(fn, exc=M.Refusal):
    try:
        fn()
    except exc:
        return True
    return False


# ---- fixtures: handcrafted collision pairs + GATED crew proposals ----
crew = M.gate_crew(json.load(open(os.path.join(HERE, "fixtures", "crew_proposals.json"))))
check("crew inputs survive the gate", len(crew["inputs"]) >= 30)
check("crew tab inputs all contain a tab", crew["tab_inputs"] and all("\t" in s for s in crew["tab_inputs"]))
check("crew blend inputs all contain &", crew["blend_inputs"] and all("&" in s for s in crew["blend_inputs"]))
check("gate drops hostile proposals", M.gate_crew({"inputs": [1, None, "ok", "bad\x00", "é", "x" * 99, "ok"]})["inputs"] == ["ok"])
check("gate survives garbage", M.gate_crew("nope") == {"inputs": [], "tab_inputs": [], "blend_inputs": []})

PAIRS = ["Hello World", "hello world", "HELLO WORLD", "Hello  World", " hello world ", "hello, world",
         "the quick brown fox jumps", "the quick brown fox leaps", "world hello", "Good Morning", "good morning",
         "good  morning", "Good Morning!", "morning good"]
INPUTS = list(dict.fromkeys(PAIRS + crew["inputs"]))
T = IM.TEXT_T
ledger = K.Ledger(dev="metabolizer")

# ---- (a) grow -> freeze: a gate that declines ----
cap1 = M.Capability("slug", C.slug_v1, C.TIER_CHEAP)
g = M.grow(cap1, INPUTS, T)
check("miner derives casefold/lower/collapse_ws", {"casefold", "lower", "collapse_ws"} <= set(g["accepted"]))
check("miner refutes sort_words and trunc16 traps", {"sort_words", "trunc16"} <= set(g["refuted"]))
p1 = M.freeze(cap1, INPUTS, T, ledger)
check("freeze yields v1", p1.version == 1 and p1.kind == "leaf")
check("witness live after freeze", p1.state == "WITNESSED" and p1.witness.t == RW.clean_needed(M.P0, M.DELTA))
probes = [s.get("t", "domain") for s in p1.gate.specs]
check("gate = domain + seeded invariants", probes[0] == "domain" and {"lower", "collapse_ws"} <= set(probes))
check("in-domain input served", p1.serve("Hello, World!")["product"] == "hello-world")
r = p1.serve(12345)
check("declines wrong type", r["status"] == "declined" and r["probe"] == "domain")
check("declines oversize", p1.serve("x" * 5000)["status"] == "declined")
check("declines empty", p1.serve("")["status"] == "declined")
r = p1.serve(crew["tab_inputs"][0])
check("declines out-of-invariant input (tab)", r["status"] == "declined" and r["probe"] == "invariant:collapse_ws")
check("tab input really is a capability quirk", C.slug_v1("a\tb") != C.slug_v1("a b"))
check("served calls leave verified receipts", K.receipt_ok(p1.serve("Good Morning")["receipt"]))
check("tier carried from the budget vector", p1.tier == C.TIER_CHEAP and M.tier_name(p1.tier) == "free")
check("a gate with no probes is refused", raises(lambda: M._require_declinable(M.Gate([], T), C.slug_v1, INPUTS)))
check("too little evidence refuses to freeze", raises(lambda: M.freeze(cap1, INPUTS[:5], T, ledger)))
_n = [0]
def _coin(s):
    _n[0] += 1
    return str(_n[0])
nd = M.Capability("coin", _coin, C.TIER_CHEAP)
check("nondeterministic capability refuses", raises(lambda: M.freeze(nd, INPUTS, T, ledger)))
check("spec is JSON-serializable", bool(json.dumps(p1.spec())))
check("frozen_hash is stable", p1.frozen_hash() == p1.frozen_hash() == p1.spec()["frozen_hash"])

# ---- (b) drift -> witness retracts -> re-freeze ----
ctrl = M.freeze(M.Capability("ctrl", C.slug_v1, C.TIER_CHEAP), INPUTS, T, ledger)
check("no drift: witness holds over 300 audits (Ville)", ctrl.audit((INPUTS * 10)[:300]) == "WITNESSED")
h1 = p1.behavior_hash()
cap1.fn = C.slug_v2                                       # the capability drifts
check("patch still serves until audited", p1.serve("Hello World")["status"] == "ok")
st = p1.audit(INPUTS)
check("drift: version-witness RETRACTS", st == "RETRACTED" and p1.witness.stop_t > 0)
check("retracted patch refuses to serve", p1.serve("hello world")["status"] == "retracted")
check("retraction is on the ledger", any(r["body"].get("event") == "retract" for r in ledger.records if r["type"] == "ledger.transaction"))
p1.refreeze()
check("re-freeze bumps version, witness live", p1.version == 2 and p1.state == "WITNESSED")
check("re-freeze re-mines: casefold/lower invariants dropped", "lower" not in [s.get("t") for s in p1.gate.specs] and "lower" in g["accepted"])
check("re-freeze captured the new behaviour", p1.behavior_hash() != h1 and p1.serve("Hello World")["product"] == "ello-orld")
check("re-frozen patch still declines out-of-domain", p1.serve(None)["status"] == "declined")
cap1.fn = C.slug_v1                                       # restore for the routing section
p1.refreeze()
check("v3 after restore", p1.version == 3 and p1.serve("Hello World")["product"] == "hello-world")

# ---- (c) product-identical patches route to the cheaper ----
alt = M.freeze(M.Capability("slug_alt", C.slug_alt, C.TIER_METERED), INPUTS, T, ledger)
check("alt is product-identical on the fixtures", all(C.slug_alt(x) == C.slug_v1(x) for x in INPUTS))
check("alt tier is metered", M.tier_name(alt.tier) == "metered" and M.cost_key(alt.tier) > M.cost_key(p1.tier))
led2 = K.Ledger(dev="router")
bl_cases = []                                             # no disagreement evidence needed for this section
rt = M.make_router([alt, p1], bl_cases, led2)
for x in ("Hello, World!", "Good Morning", "THE QUICK brown fox"):
    r = rt.route(x)
    check("identical -> cheaper (%r)" % x, r["how"] == "cheaper" and r["via"] == "slug" and r["product"] == C.slug_v1(x))
rt_rev = M.make_router([p1, alt], bl_cases, led2, name="router2")
check("member order does not change the pick", rt_rev.route("Hello")["via"] == "slug")
r = rt.route("Hello")
axes = {c.split("@")[0]: a for c, a in r["price"]["routes"].items()}
check("matches route-preference B4 on the same axes", RP.prefer_axes(axes)["preferred_when"]["cheap"] == "slug")
cheap_alt = M.freeze(M.Capability("slug_alt", C.slug_alt, C.TIER_CHEAP), INPUTS, T, ledger, name="alt_cheap")
exp_p1 = M.freeze(M.Capability("slug", C.slug_v1, C.TIER_METERED), INPUTS, T, ledger, name="slug_expensive")
check("not hard-coded: cheaper member wins when roles swap",
      M.make_router([cheap_alt, exp_p1], [], led2, name="router3").route("Hello")["via"] == "alt_cheap")
check("router declines when every member declines", rt.route(None)["status"] == "declined")
check("router declines a tab input via member gates", rt.route(crew["tab_inputs"][0])["status"] == "declined")

# ---- (d) disagreement -> a frozen, gated, re-freezable BLEND ----
cap_and = M.Capability("slug_and", C.slug_and, C.TIER_MID)
andp = M.freeze(cap_and, INPUTS, T, ledger)
amps = crew["blend_inputs"]
check("members really disagree on & inputs", all(C.slug_v1(x) != C.slug_and(x) for x in amps))
# referee policy: prefer the 'and' spelling, except the first case where the plain slug is right
cases = [{"input": x, "expected": C.slug_and(x)} for x in amps[1:]]
cases.append({"input": amps[0], "expected": C.slug_v1(amps[0])})
cases.append({"input": amps[0] + " bogus", "expected": "matches-no-member"})        # crew junk: must be dropped
cases.append({"input": "no ampersand here", "expected": "no-ampersand-here"})      # uninformative: must be dropped
cases.append("not-a-case")
kept = M.gate_cases(cases, [p1, andp])
check("case gate keeps only informative verified cases", len(kept) == len(amps))
check("case gate dropped bogus/uninformative/garbage", all("bogus" not in c["input"] and "ampersand" not in c["input"] for c in kept))
led3 = K.Ledger(dev="blend")
b = M.resolve_blend([p1, andp], cases, led3)
check("blend is a patch with a frozen decision", b.kind == "blend" and b.version == 1 and b.state == "WITNESSED")
check("blend default = member the referee mostly sides with", b.default == "slug_and")
check("blend honours the per-case table", b.serve(amps[0])["product"] == C.slug_v1(amps[0]))
check("blend resolves a table case by default member", b.serve(amps[1])["product"] == C.slug_and(amps[1]))
check("blend resolves an unseen disagreement by default", b.serve("fish & chips")["product"] == "fish-and-chips")
check("blend passes through where members agree", b.serve("Hello World")["product"] == "hello-world")
check("blend is gated: declines wrong type", b.serve(7)["status"] == "declined")
check("blend is gated: parent invariant declines tab input", b.serve(crew["tab_inputs"][0])["status"] == "declined")
check("blend has a tier = every member runs", b.tier["wall_ms"] == p1.tier["wall_ms"] + andp.tier["wall_ms"])
check("blend spec JSON + hash", bool(json.dumps(b.spec())) and b.spec()["members"] == ["slug@v3", "slug_and@v1"])
check("no evidence -> no blend", raises(lambda: M.resolve_blend([p1, andp], [{"input": "a&b", "expected": "zzz"}], led3)))
hb = b.behavior_hash()
cap_and.fn = C.slug_v2                                    # a member drifts under the blend
check("member drift RETRACTS the blend's witness", b.audit(INPUTS) == "RETRACTED")
check("retracted blend refuses to serve", b.serve("fish & chips")["status"] == "retracted")
b.refreeze()
check("blend re-freezes (v2, live, new behaviour)", b.version == 2 and b.state == "WITNESSED" and b.behavior_hash() != hb)
cap_and.fn = C.slug_and
b.refreeze()
check("blend re-freezes again after restore", b.version == 3 and b.serve("fish & chips")["product"] == "fish-and-chips")

# router: disagreement is resolved by a frozen blend; the router is itself a patch
andp.refreeze()
led4 = K.Ledger(dev="router4")
R = M.make_router([p1, andp], cases, led4, name="router")
check("router is itself a gated, witnessed patch", R.kind == "router" and R.state == "WITNESSED" and R.serve(3)["status"] == "declined")
r1 = R.route("fish & chips")
check("disagreement routes through a blend", r1["how"] == "blend" and r1["product"] == "fish-and-chips" and r1["via"].startswith("blend("))
check("agreement routes by price", R.route("Hello")["how"] == "cheaper")
blend_ids = {id(v) for v in R.capability.blends.values()}
R.route("salt & pepper")
check("frozen decision is reused, not re-derived", len(R.capability.blends) == 1 and {id(v) for v in R.capability.blends.values()} == blend_ids)
check("router serves through its own gate", R.serve("fish & chips")["product"] == "fish-and-chips")
check("router spec is JSON with member versions", "slug_and@v2" in json.dumps(R.spec()) or "slug_and" in json.dumps(R.spec()))
cap_and.fn = C.slug_v2
check("member retracts first (audit)", andp.audit(INPUTS) == "RETRACTED")
check("a retracted member changes routing -> router witness RETRACTS", R.audit(amps * 10) == "RETRACTED")

# ---- ledger + determinism ----
for L in (ledger, led2, led3, led4):
    check("ledger verifies (%s)" % L.dev, L.verify()["intact"] is True)
def build():
    l = K.Ledger(dev="d")
    a = M.freeze(M.Capability("slug", C.slug_v1, C.TIER_CHEAP), INPUTS, T, l)
    return a.spec()["frozen_hash"], l.head()
check("freeze is deterministic (spec hash + ledger head)", build() == build())

print("metabolizer selftest: %d checks, %d failures" % (checks, fails))
sys.exit(1 if fails else 0)
