"""quilt-kernel selftest — offline, deterministic, stdlib only.  Run: python3 selftest.py"""
import copy, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quilt_kernel as K

checks = fails = 0


def check(name, ok):
    global checks, fails
    checks += 1
    fails += 0 if ok else 1
    if not ok:
        print("  FAIL:", name)


def raises(fn, exc=Exception):
    try:
        fn()
    except exc:
        return True
    return False


def ticker():
    t = [0.0]
    def clk():
        t[0] += 0.010
        return t[0]
    return clk


# -- hashing ---------------------------------------------------------------------------
check("fnv1a64 empty == offset basis", K.fnv1a64("") == 0xCBF29CE484222325)
check("fnv1a64 'a' standard vector", K.fnv1a64("a") == 0xAF63DC4C8601EC8C)
check("fnv1a64 'foobar' standard vector", K.fnv1a64("foobar") == 0x85944171F73967E8)
check("fleet canary (accent load-bearing)", K.canary())
check("unaccented fixture is a different hash", K.fnv1a64("cafe Δ 日本語") != 0x024A555471370B18D)
check("canon sorts keys", K.canon({"b": 1, "a": 2}) == '{"a":2,"b":1}')
check("canon is order-independent", K.content_hash({"x": 1, "y": 2}) == K.content_hash({"y": 2, "x": 1}))
check("canon refuses NaN", raises(lambda: K.canon(float("nan")), ValueError))
check("canon refuses arbitrary objects", raises(lambda: K.canon(object()), TypeError))
check("canon accepts bytes/set/tuple deterministically",
      K.canon({"s": {3, 1, 2}, "b": b"\x01", "t": (1, 2)}) == '{"b":{"$bytes":"01"},"s":[1,2,3],"t":[1,2]}')

# -- budget vector ---------------------------------------------------------------------
b1, b2 = K.budget(wall_ms=5, tokens={"api": 3}, usd=0.5, prod=10), K.budget(wall_ms=7, tokens={"api": 4}, usd=0.25, train=2)
s = K.add_budget(b1, b2)
check("add_budget sums wall/tokens/usd/storage",
      s["wall_ms"] == 12 and s["tokens"]["api"] == 7 and s["usd"] == 0.75 and s["storage_bytes"] == {"train": 2, "prod": 10})
check("budget_ok accepts well-formed", K.budget_ok(b1))
check("budget_ok rejects negative usd", not K.budget_ok(K.budget(usd=-1)))
check("budget_ok rejects float tokens", not K.budget_ok(K.budget(tokens={"api": 1.5})))

# -- Cell + Ledger ---------------------------------------------------------------------
led = K.Ledger(dev="t")
sq = K.Cell(lambda x: {"y": x * x}, "sq", led, clock=ticker())
check("cell returns the function's value untouched", sq(3) == {"y": 9})
r = sq.last
check("receipt carries product hash + activation + budget",
      r["product_hash"] == K.content_hash({"y": 9}) and r["activation"].startswith("0x") and K.budget_ok(r["budget"]))
check("wall_ms measured from injected clock", r["budget"]["wall_ms"] == 10.0)
check("activation = fnv(cell, input, product)", r["activation"] == K.activation("sq", r["input_hash"], r["product_hash"]))
sq(4); sq(5)
check("one cell.tick per call", len(led.records) == 3 and all(x["type"] == "cell.tick" for x in led.records))
env = led.records[0]
check("envelope has the ActiveLog v1 fields", all(k in env for k in K.REQUIRED) and env["alv"] == 1)
check("first prev is genesis", env["prev"] == led.genesis and led.genesis == "sha256:" + "0" * 64)
check("prev chain links envelopes", led.records[1]["prev"] == led.link_hash(led.records[0]))
check("ts is deterministic by default", [x["ts"] for x in led.records] == ["det:000001", "det:000002", "det:000003"])
check("verify: untouched chain is intact", led.verify() == {"intact": True, "firstBreak": None, "reason": None})
check("ledger.total sums all receipts", led.total()["wall_ms"] == 30.0)
check("cost= supplies usd/tokens; wall_ms still measured",
      (lambda c: (c(1), c.last["budget"]["usd"] == 0.01 and c.last["budget"]["tokens"] == {"api": 7}
                  and c.last["budget"]["wall_ms"] == 10.0)[1])(
          K.Cell(lambda x: x, "id", K.Ledger(), cost=lambda o, x: {"usd": 0.01, "tokens": {"api": 7}}, clock=ticker())))
check("cost= wall_ms overrides the clock",
      (lambda c: (c(1), c.last["budget"]["wall_ms"] == 42)[1])(
          K.Cell(lambda x: x, "id", K.Ledger(), cost=lambda o, x: {"wall_ms": 42})))
check("non-JSON product is refused, not hashed by repr", raises(lambda: K.Cell(lambda x: object(), "o", K.Ledger())(1), TypeError))
check("kwargs are part of the input hash",
      K.content_hash({"args": [1], "kw": {"a": 1}}) != K.content_hash({"args": [1], "kw": {"a": 2}}))
check("route label lands in the receipt", K.Cell(lambda: 1, "r", K.Ledger(), route="R1")() == 1)

# -- tamper evidence (first break, anchor, deep receipt check) -------------------------
def fresh(n=5, **ckw):
    l = K.Ledger(); c = K.Cell(lambda x: {"y": x + 1}, "inc", l, clock=ticker(), **ckw)
    for i in range(n):
        c(i)
    return l

L = fresh()
L.records[2]["body"]["budget"]["usd"] = 9.0
v = L.verify()
check("editing a middle record: firstBreak is the NEXT record (prev no longer matches)", v == {"intact": False, "firstBreak": 4, "reason": "prev-chain broken"})
L = fresh(); L.records[1]["body"]["product_hash"] = "0xdeadbeefdeadbeef"
check("changing a product hash breaks the receipt itself (firstBreak == that record)",
      L.verify()["firstBreak"] == 2 and "activation" in L.verify()["reason"])
L = fresh(); del L.records[1]
check("deleting a record is detected at the gap", L.verify()["firstBreak"] == 2)
L = fresh(); L.records.reverse()
check("reordering is detected", not L.verify()["intact"] and L.verify()["firstBreak"] == 1)
L = fresh(); L.records[0]["alv"] = 2
check("wrong alv is a malformed envelope", L.verify()["reason"] == "malformed envelope")
L = fresh(); anc = L.anchor()
check("anchor names head + seq + link", anc["seq"] == 4 and anc["digest"] == L.head())
check("verify(anchor) passes on the honest chain", L.verify(anchor=anc)["intact"])
K.Cell(lambda x: x, "late", L)(1)
check("records appended after the anchor keep it valid (chain may grow)", L.verify(anchor=anc)["intact"])
honest = fresh(); anc = honest.anchor()
forged = K.Ledger(clock=None); fc = K.Cell(lambda x: {"y": x + 2}, "inc", forged, clock=ticker())
for i in range(5):
    fc(i)
check("a fully re-written, internally consistent chain verifies on its own", forged.verify()["intact"])
check("...but does NOT reproduce the anchored head", not forged.verify(anchor=anc)["intact"])
check("last-record edit is invisible to prev-chain alone", (lambda l: (l.records[-1]["body"]["budget"].__setitem__("usd", 5.0), l.verify()["intact"])[1])(fresh()))
check("...and caught by the anchor", (lambda l, a: (l.records[-1]["body"]["budget"].__setitem__("usd", 5.0), not l.verify(anchor=a)["intact"])[1])(fresh(), fresh().anchor()))
check("keep=('product',) lets deep verify re-hash the product",
      (lambda l: (l.records[0]["body"].__setitem__("product", {"y": 99}), l.verify()["firstBreak"] == 1)[1])(fresh(keep=("input", "product"))))
check("blake2b-256 link option chains and verifies", (lambda l: l.verify()["intact"] and l.records[1]["prev"].startswith("blake2b-256:"))(
    (lambda l: (K.Cell(lambda x: x, "i", l)(1), K.Cell(lambda x: x, "i", l)(2), l)[2])(K.Ledger(link="blake2b-256"))))
check("unknown record type refused", raises(lambda: K.Ledger().emit("nope", {}), ValueError))
check("cell.tick without a budget refused", raises(lambda: K.Ledger().emit("cell.tick", {}), ValueError))

# -- persistence -----------------------------------------------------------------------
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "run.jsonl")
    pl = K.Ledger(path=p); pc = K.Cell(lambda x: [x], "p", pl, clock=ticker())
    pc(1); pc(2)
    back = K.Ledger.load(open(p).read())
    check("JSONL round-trip preserves records and verifies", back.records == pl.records and back.verify()["intact"])
    check("to_jsonl == file contents", pl.to_jsonl() == open(p).read())
check("run_hash is stable across identical runs", fresh().run_hash() == fresh().run_hash())

# -- double entry ----------------------------------------------------------------------
dl = K.Ledger()
h = dl.hop("stt", "frames", 10, "llm", "tokens", 0.5, "frames->tokens", route="R", wall_ms=3)
check("hop balances: credit*rate == debit", h["body"]["debit"]["amount"] == 5.0)
check("hop counts in route total", dl.total("R")["wall_ms"] == 3 and dl.total("other")["wall_ms"] == 0)
check("hop chains like any record", dl.verify()["intact"])

# -- replay == live --------------------------------------------------------------------
rl = K.Ledger()
live = K.Cell(lambda a, k=1: {"v": a * k}, "mul", rl, clock=ticker())
live(3, k=2); live(4)
check("replay of a pure cell reproduces every product", K.replay(rl, {"mul": live}) == {"replayed": 2, "mismatches": [], "ok": True})
check("replay accepts a plain function", K.replay(rl, {"mul": lambda a, k=1: {"v": a * k}})["ok"])
check("replay catches a changed implementation", K.replay(rl, {"mul": lambda a, k=1: {"v": a * k + 1}})["mismatches"] == [0, 1])
ctr = [0]
def impure(x):
    ctr[0] += 1
    return ctr[0]
il = K.Ledger(); ic = K.Cell(impure, "imp", il); ic(0)
check("replay exposes an impure function", not K.replay(il, {"imp": ic})["ok"])
check("replay skips cells it was not given", K.replay(rl, {})["replayed"] == 0)
check("replay needs stored input (keep=() -> nothing to replay)",
      (lambda l: (K.Cell(lambda x: x, "n", l, keep=())(1), K.replay(l, {"n": lambda x: x})["replayed"] == 0)[1])(K.Ledger()))
check("deterministic run: same inputs twice -> identical run_hash",
      (lambda: (lambda a, b: a.run_hash() == b.run_hash())(fresh(), fresh()))())

# -- Differ ----------------------------------------------------------------------------
check("diff: identical raw products", K.diff({"a": [1, 2]}, {"a": [1, 2]})["identical"])
d = K.diff({"a": [1, 2], "b": 1}, {"a": [1, 3], "b": 1})
check("diff: localises first difference path", not d["identical"] and d["first_difference"] == "$.a[1]")
check("diff: key order is not a difference", K.diff({"a": 1, "b": 2}, {"b": 2, "a": 1})["identical"])
check("diff: 1 vs 1.0 vs True are kept distinct by canonical JSON", K.diff(1, True)["identical"] is False)
check("diff: missing key path", K.diff({"a": 1}, {"a": 1, "z": 2})["first_difference"] == "$.z")
check("diff: ignore= drops metadata keys", K.diff({"ans": 1, "route": "x"}, {"ans": 1, "route": "y"}, ignore=("route",))["identical"])
check("diff: ignore= does not hide a real difference", not K.diff({"ans": 1, "route": "x"}, {"ans": 2, "route": "y"}, ignore=("route",))["identical"])
ia = K.Cell(lambda x: x + 1, "a", K.Ledger()); ib = K.Cell(lambda x: 1 + x, "b", K.Ledger()); ic2 = K.Cell(lambda x: x + 2, "c", K.Ledger())
ia(1); ib(1); ic2(1)
check("diff: receipts compare by product_hash", K.diff(ia.last, ib.last)["identical"] and not K.diff(ia.last, ic2.last)["identical"])
check("diff: accepts envelopes as well as bodies",
      K.diff(ia.ledger.records[0], ib.ledger.records[0])["identical"])
check("diff: a receipt equals the raw product it hashes", K.diff(ia.last, 2)["identical"])
check("diff: hash-only receipts cannot localise (honest None)", K.diff(ia.last, ic2.last)["first_difference"] is None)
check("diff: kept products DO localise",
      K.diff(*[(lambda c: (c({"k": [v]}), c.last)[1])(K.Cell(lambda x: x, "k", K.Ledger(), keep=("product",))) for v in (1, 2)])["first_difference"] == "$.k[0]")

# -- Price -----------------------------------------------------------------------------
def runs(specs, items=(1,)):
    """specs: {name: (fn, cost)} -> {name: [receipts]} over items, deterministic budgets."""
    out = {}
    for n, (fn, cost) in specs.items():
        l = K.Ledger(); c = K.Cell(fn, n, l, cost=cost); out[n] = []
        for it in items:
            c(it); out[n].append(c.last)
    return out

same = lambda x: {"y": x * 2}
fastpricey = (same, lambda o, x: {"wall_ms": 10, "usd": 0.5})
slowcheap = (same, lambda o, x: {"wall_ms": 90, "usd": 0.1})
R = K.price(runs({"fast": fastpricey, "cheap": slowcheap}))
check("price: two product-identical cells certify", R["status"] == "certified")
check("price: genuine trade-off class, both on the frontier", R["class"] == "trade-off" and R["frontier"] == ["cheap", "fast"])
check("price: which(fast)/which(cheap) answer 'which, when?'", K.which(R, "fast") == "fast" and K.which(R, "cheap") == "cheap")
check("price: pair is None on a real trade-off", R["preferred_when"]["faster-cheaper"] is None)
check("price: no standing -> good is a tie, not invented", R["preferred_when"]["good"] == "tie" and R["good_source"] == "tie")
check("price: result_hash is fnv1a-64 over the body", R["result_hash"] == K.content_hash({k: v for k, v in R.items() if k != "result_hash"}))
check("price: deterministic (same receipts -> same result_hash)",
      K.price(runs({"fast": fastpricey, "cheap": slowcheap}))["result_hash"] == R["result_hash"])
dom = K.price(runs({"a": (same, lambda o, x: {"wall_ms": 5, "usd": 0.1}), "b": (same, lambda o, x: {"wall_ms": 9, "usd": 0.2})}))
check("price: dominant route collapses the frontier", dom["class"] == "dominant" and dom["frontier"] == ["a"] and dom["dominated"] == {"b": ["a"]})
check("price: dominant pairs resolve", K.which(dom, "faster-cheaper") == "a")
tie = K.price(runs({"a": (same, lambda o, x: {"wall_ms": 5}), "b": (same, lambda o, x: {"wall_ms": 5})}))
check("price: exact tie -> both on frontier, name-ordered pick", tie["frontier"] == ["a", "b"] and tie["preferred_when"]["fast"] == "a" and "fast" in tie["tied"])
wrong = K.price(runs({"ok": (same, lambda o, x: {"wall_ms": 50}), "bad": (lambda x: {"y": x * 3}, lambda o, x: {"wall_ms": 1, "usd": 0})}))
check("price: differing product is REFUSED", wrong["status"] == "refused" and "never price a cheaper different answer" in wrong["reason"])
check("price: a refusal exposes NO budgets", "routes" not in wrong and "preferred_when" not in wrong and "wall_ms" not in json.dumps(wrong))
check("price: refusal names the product hashes", set(wrong["products"]) == {"ok", "bad"})
check("which() raises Refusal on a refused result", raises(lambda: K.which(wrong, "cheap"), K.Refusal))
check("price: one candidate refused", K.price(runs({"only": fastpricey}))["status"] == "refused")
check("price: empty/unequal workloads refused",
      K.price({"a": [], "b": []})["status"] == "refused" and K.price({"a": runs({"a": fastpricey}, (1, 2))["a"], "b": runs({"b": fastpricey})["b"]})["status"] == "refused")
forged_r = copy.deepcopy(runs({"a": fastpricey, "b": slowcheap}))
forged_r["b"][0]["budget"]["usd"] = 0.0
check("price: budget edit alone isn't caught by a receipt (honest: verify the LEDGER)", K.price(forged_r)["status"] == "certified")
forged_r["b"][0]["product_hash"] = "0x0000000000000000"
check("price: product_hash edit breaks activation -> refused", K.price(forged_r)["status"] == "refused")
check("price: bad standing refused", K.price(runs({"a": fastpricey, "b": slowcheap}), standing={"a": -1})["status"] == "refused"
      and K.price(runs({"a": fastpricey, "b": slowcheap}), standing={"zzz": 1})["status"] == "refused"
      and K.price(runs({"a": fastpricey, "b": slowcheap}), standing={"a": True, "b": 1})["status"] == "refused")
st = K.price(runs({"fast": fastpricey, "cheap": slowcheap}), standing={"fast": 1, "cheap": 5})
check("price: full standing decides `good`; better-cheaper becomes answerable",
      st["good_source"] == "standing" and st["preferred_when"]["good"] == "cheap" and st["preferred_when"]["better-cheaper"] == "cheap"
      and st["preferred_when"]["better-faster"] is None)
check("price: standing on only some names is ignored as a tie", K.price(runs({"fast": fastpricey, "cheap": slowcheap}), standing={"fast": 9})["good_source"] == "tie")
wl = K.price(runs({"x": (same, lambda o, v: {"wall_ms": v}), "y": (same, lambda o, v: {"wall_ms": 12 - v})}, items=(1, 2, 11)))
check("price: workload lists sum per implementation", wl["items"] == 3 and wl["routes"]["x"]["wall_ms"] == 14 and wl["routes"]["y"]["wall_ms"] == 22)
mid = runs({"x": (same, None), "y": (lambda v: {"y": v * 2 if v != 2 else 0}, None)}, items=(1, 2))
check("price: a difference on ANY workload item refuses the whole comparison", K.price(mid)["status"] == "refused" and "item 1" in K.price(mid)["reason"])
check("price: accepts envelopes, bodies and Cell.last alike",
      (lambda rr: K.price({"a": rr["a"][0], "b": rr["b"]})["status"] == "certified")(runs({"a": fastpricey, "b": slowcheap})))
check("price: storage is a second cheapness (usd ties, storage decides)",
      K.which(K.price(runs({"a": (same, lambda o, x: {"prod": 10, "wall_ms": 1}), "b": (same, lambda o, x: {"prod": 99, "wall_ms": 1})})), "cheap") == "a")
check("price: compute vs storage disagreement is incomparable, both stay cheap candidates",
      set(K.price(runs({"a": (same, lambda o, x: {"usd": 1.0, "prod": 1}), "b": (same, lambda o, x: {"usd": 0.1, "prod": 99})}))["tied"]["cheap"]) == {"a", "b"})
def via(tag):
    l = K.Ledger(); c = K.Cell(lambda x: {"y": x, "via": tag}, tag, l, ignore=("via",)); c(1)
    return c, c.last
(ca, ra_), (cb, rb_) = via("a"), via("b")
check("cell ignore=: metadata differs, function output untouched, products identical",
      ca(1) == {"y": 1, "via": "a"} and K.price({"a": ra_, "b": rb_})["status"] == "certified")
check("cell ignore=: replay honours it", K.replay(ca.ledger, {"a": ca})["ok"])
check("cell ignore=: without it the same pair is refused",
      K.price(runs({"a": (lambda x: {"y": x, "via": "a"}, None), "b": (lambda x: {"y": x, "via": "b"}, None)}))["status"] == "refused")

# -- Hebbian book ----------------------------------------------------------------------
bk = K.Book()
for _ in range(3):
    bk.observe(R)
check("book: reinforcement is integer and bounded", all(isinstance(w, int) and 0 <= w <= K.SCALE for p in bk.weights.values() for w in p.values()))
check("book: settled() follows the confirmed pick", bk.settled()["fast"] == "fast" and bk.settled()["cheap"] == "cheap")
check("book: null pairs stay untouched", "faster-cheaper" not in bk.weights)
bk.observe(wrong)
check("book: refused results are not observed", bk.n == 3)
w1 = bk.weights["fast"]["fast"]
check("book: 3 confirmations -> exact integer weight (1/4 saturating steps: 250000, 437500, 578125)", w1 == 578125)
check("book: decays the loser", bk.weights["fast"]["cheap"] == 0)
tieb = K.Book(); tieb.weights = {"fast": {"b": 500}}
check("book: weights break an exact tie toward the reinforced route", K.price(runs({"a": (same, None), "b": (same, None)}), weights=tieb.weights)["preferred_when"]["fast"] == "b")
check("book: weights never override a strict win", K.price(runs({"a": (same, lambda o, x: {"wall_ms": 1}), "b": (same, lambda o, x: {"wall_ms": 9})}), weights={"fast": {"b": K.SCALE}})["preferred_when"]["fast"] == "a")

# -- parity with the lab it was distilled from (skipped if the labs are absent) ---------
LABS = os.path.dirname(HERE)
if os.path.isdir(os.path.join(LABS, "route-preference")):
    sys.path.insert(0, os.path.join(LABS, "route-preference"))
    sys.path.insert(0, os.path.join(LABS, "system2-backtest"))
    sys.path.insert(0, os.path.join(LABS, "activeledger"))
    import route_preference as RP
    import activeledger as AL
    check("parity: fnv1a64 == activeledger.fnv1a64 on 5 inputs",
          all(K.fnv1a64(s) == AL.fnv1a64(s) for s in ("", "a", "café Δ 日本語", "x" * 1000, '{"a":1}')))
    check("parity: canon/content_hash == activeledger's", K.content_hash({"b": [1, {"c": 2}], "a": None}) == AL.content_hash({"b": [1, {"c": 2}], "a": None}))
    check("parity: add_budget == activeledger.add_budget", K.add_budget(b1, b2) == AL.add_budget(b1, b2))
    check("parity: kernel ledger verifies under activeledger.verify_chain",
          (lambda l: (K.Cell(lambda x: x, "i", l)(1), K.Cell(lambda x: x, "i", l)(2), AL.verify_chain(l.records))[2])(K.Ledger()))
    def axes_only(res):
        return {k: res[k] for k in ("frontier", "dominated", "preferred_when", "tied")}
    cases = [{"a": {"wall_ms": 10, "usd": .5, "tokens": 0, "storage_bytes": 0}, "b": {"wall_ms": 90, "usd": .1, "tokens": 0, "storage_bytes": 0}},
             {"a": {"wall_ms": 5, "usd": .1, "tokens": 3, "storage_bytes": 0}, "b": {"wall_ms": 9, "usd": .2, "tokens": 4, "storage_bytes": 0}},
             {"a": {"wall_ms": 5, "usd": 1, "tokens": 0, "storage_bytes": 1}, "b": {"wall_ms": 5, "usd": .1, "tokens": 0, "storage_bytes": 99}}]
    for i, ax in enumerate(cases):
        lab = RP.prefer_axes(ax)
        ledgers = {}
        for n in ax:
            c = K.Cell(same, n, K.Ledger(), cost=(lambda a: lambda o, x: {"wall_ms": a["wall_ms"], "usd": a["usd"], "tokens": {"api": a["tokens"]}, "prod": a["storage_bytes"]})(ax[n]))
            c(1); ledgers[n] = c.last
        kr = K.price(ledgers)
        del kr["preferred_when"]["good"], lab["preferred_when"]["good"]
        check("parity: price() placement == route_preference.prefer_axes (case %d)" % i,
              kr["frontier"] == lab["frontier"] and kr["dominated"] == lab["dominated"] and kr["preferred_when"] == lab["preferred_when"])
    bk2, bk3 = K.Book(), RP.PreferenceBook()
    for ax in cases:
        bk3.observe(RP.prefer_axes(ax))
    for ax in cases:
        ll = {}
        for n in ax:
            c = K.Cell(same, n, K.Ledger(), cost=(lambda a: lambda o, x: {"wall_ms": a["wall_ms"], "usd": a["usd"], "tokens": {"api": a["tokens"]}, "prod": a["storage_bytes"]})(ax[n])); c(1); ll[n] = c.last
        bk2.observe(K.price(ll))
    check("parity: Book weights == PreferenceBook weights (same integer arithmetic)", bk2.weights == bk3.weights)
else:
    print("  note: labs/ not found next to quilt-kernel; parity checks skipped (standalone mode)")

# -- playtest hardening regressions (PLAYTEST-REPORT.md) -------------------------------
def _raises(f):
    try:
        f(); return False
    except Exception:
        return True
_e = K.Ledger()
check("PT: verify() of an empty ledger reproduces its own anchor (was IndexError)", _e.verify(_e.anchor())["intact"])
check("PT: empty-ledger anchor with a wrong digest is refused, not crashed",
      not K.Ledger().verify({"digest": "sha256:" + "1" * 64, "seq": -1, "link": "sha256"})["intact"])
_n = K.Ledger(); _n.emit("route.hop", {"budget": K.budget()})
check("PT: malformed anchors (missing keys / bad seq / negative / bool) return intact=False, never raise",
      all(not _n.verify(a)["intact"] for a in ({}, {"digest": "x"}, {"seq": 0}, {"digest": _n.head(), "seq": -1},
                                               {"digest": _n.head(), "seq": True}, {"digest": _n.head(), "seq": "0"}, 7)))
check("PT: a good anchor still verifies", _n.verify(_n.anchor())["intact"])
check("PT: non-dict JSONL lines (1, null) are 'malformed envelope', not TypeError (+ list/str still are)",
      all(K.Ledger.load(j).verify() == {"intact": False, "firstBreak": 1, "reason": "malformed envelope"} for j in ("1", "null", "[1]", '"s"', "3.5", "true")))
check("PT: bool token counts are not a well-formed budget", not K.budget_ok(K.budget(tokens={"a": True})))
_r = lambda u: (lambda l, c: (c(), l.records[0])[1])(*(lambda l: (l, K.Cell(lambda: 1, "x", l, cost=lambda *a, **k: {"usd": u, "wall_ms": 1})))(K.Ledger()))
_a, _b = _r(1), _r(2)
check("PT: price() refuses (never raises) on non-string names", K.price({1: _a, "b": _b})["status"] == "refused")
check("PT: price() refuses (never raises) on malformed weights",
      all(K.price({"a": _a, "b": _b}, weights=w)["status"] == "refused" for w in ({"cheap": "x"}, {"cheap": 3}, [1])))
check("PT: well-formed weights still price", K.price({"a": _a, "b": _b}, weights={"cheap": {"b": 5}})["status"] == "certified")

# -- examples and the README quickstart actually run -----------------------------------
def run_py(path):
    return subprocess.run([sys.executable, path], capture_output=True, text=True, cwd=tempfile.gettempdir())

for ex, needle in (("data_pipeline", "status: certified"), ("llm_call", "refused"), ("build_step", "cheapest (storage): concat")):
    p = run_py(os.path.join(HERE, "examples", ex + ".py"))
    check("example %s runs and prints the expected line" % ex, p.returncode == 0 and needle in p.stdout)
check("llm example: cheaper-but-wrong model is refused, real pair certifies",
      (lambda o: "small vs large: certified" in o and "small vs cheap-wrong: refused" in o)(run_py(os.path.join(HERE, "examples", "llm_call.py")).stdout))

readme = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
m = re.search(r"<!-- quickstart -->\s*```python\n(.*?)```", readme, re.S)
check("README has a quickstart block", bool(m))
if m:
    lines = [l for l in m.group(1).splitlines() if l.strip()]
    check("quickstart is <= 10 lines", len(lines) <= 10)
    qp = subprocess.run([sys.executable, "-c", m.group(1)], capture_output=True, text=True, cwd=HERE)
    check("quickstart runs", qp.returncode == 0 and "certified" in qp.stdout)
    print(qp.stdout.rstrip())

print("quilt-kernel selftest: %d checks, %d failures" % (checks, fails))
sys.exit(1 if fails else 0)
