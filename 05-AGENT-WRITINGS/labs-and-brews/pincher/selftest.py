#!/usr/bin/env python3
"""pincher selftest — offline, deterministic (no network, no clock in any assertion, seeded RNG)."""

from __future__ import annotations

import copy
from fractions import Fraction

import pincher as pc
import activeledger as al
import backtest as bt
import route_preference as rp
import textnorm_quilt as tn

checks = failures = 0


def check(name, cond):
    global checks, failures
    checks += 1
    if not cond:
        failures += 1
        print("FAIL:", name)


# ---- 1. the testbed premise: guess is right where we say, wrong where we say -----------
ascii_all = [chr(i) for i in range(128)]
check("guess == full on EVERY ascii codepoint (single, padded)",
      all(pc.tn_guess(" %s " % c + c) == tn.full_route(" %s " % c + c) for c in ascii_all))
for bad in ("ß", "ﬁne", "Ⅷ", "ＡＢＣ", "é", "ς", "µ", "ŉ"):
    check("guess != full on %r (so a fallback is genuinely needed)" % bad,
          pc.tn_guess(bad) != tn.full_route(bad))
for ok in ("привет МИР", "éñü", "łőžć", "Ёж"):
    check("guess == full on %r" % ok, pc.tn_guess(ok) == tn.full_route(ok))
check("class of pure ascii is A", pc.tn_class("Hello  World") == "A")
check("class mixes buckets", pc.tn_class("ab ß ﬁ") == "AKL")

# ---- 2. the threshold grows with evidence (closed form, exact) ---------------------------
check("n* closed form == 27 for target 9/10, K=3", pc.n_star() == 27)
p = pc.make_text_pincher()
confs = [p.conf("A")]
first_pinch = None
for i in range(1, 60):
    p.observe("A", True)
    confs.append(p.conf("A"))
    if first_pinch is None and p.pinchable("A"):
        first_pinch = i
check("conf starts at 0 with no evidence", confs[0] == 0)
check("conf strictly increases under all-agree evidence",
      all(b > a for a, b in zip(confs, confs[1:])))
check("conf == n/(n+K) exactly", all(confs[n] == Fraction(n, n + pc.K) for n in range(60)))
check("class flips to pinch at exactly n*", first_pinch == pc.n_star())
check("conf just below n* is below target, at n* is at/above",
      confs[pc.n_star() - 1] < pc.TARGET <= confs[pc.n_star()])
before = p.conf("A")
p.observe("A", False)
check("one disagreement shrinks conf", p.conf("A") < before)
p2 = pc.make_text_pincher()
for _ in range(200):
    p2.observe("X", True)
for _ in range(20):
    p2.observe("X", False)
check("a ~9% disagreement rate never earns the pinch (agree/(n+K) < 9/10)", not p2.pinchable("X"))
check("classes learn independently", not p.pinchable("Y") and p.conf("Y") == 0)
check("looser target needs less evidence", pc.n_star(Fraction(1, 2)) < pc.n_star())

# ---- 3. cold start falls back; a confident class pinches; wrong/unsure -> fallback -------
cold = pc.make_text_pincher()
out, info = cold.answer("  Hello   WORLD ")
check("cold pincher falls back (no evidence)", info["path"] == "fallback" and cold.full_calls == 1)
check("fallback answer is the full answer", out == tn.full_route("  Hello   WORLD "))
check("fallback records that the guess agreed", info["guess_ok"] is True)
warm = pc.make_text_pincher()
for i in range(pc.n_star()):
    warm.answer("word%d  X" % i)
fc0 = warm.full_calls
out, info = warm.answer("  Fresh   INPUT ")
check("after n* agreements an ascii input is pinched", info["path"] == "pinch")
check("pinched call did NOT run the full route", warm.full_calls == fc0)
check("pinched answer == full answer (tolerance 0) on a confident case",
      out == tn.full_route("  Fresh   INPUT "))
sb = pc.make_text_pincher()
for i in range(100):
    sb.answer("naïve ß%d" % i)
check("a class where the guess is always wrong is never pinched",
      sb.stats["AL"]["agree"] == 0 and not sb.pinchable("AL") and sb.stats["AL"]["pinched"] == 0)
check("unsure class always returns the FULL answer", sb.answer("Straße")[0] == tn.full_route("Straße"))

# audit slice
au = pc.make_text_pincher(audit_every=4)
for i in range(pc.n_star()):
    au.answer("w%d" % i)
paths = [au.answer("z%d" % i)[1]["path"] for i in range(12)]
check("every 4th pinch is audited (runs the full route)", paths == ["pinch"] * 3 + ["audited"] + (["pinch"] * 3 + ["audited"]) * 2)
# drift caught by audit
dr = pc.make_text_pincher(audit_every=1)
for i in range(pc.n_star()):
    dr.answer("w%d" % i)
c_before = dr.conf("A")
dr.full = lambda t: tn.full_route(t) + "!"          # the world changed under the pincher
out, info = dr.answer("hello")
check("audit catches drift: guess_ok False, FULL answer returned", info["guess_ok"] is False and out.endswith("!"))
check("drift shrinks the class confidence", dr.conf("A") < c_before)

# numeric tolerance (the generic core, not just text)
check("close(): within tol", pc.close(1.0, 1.04, 0.05) and not pc.close(1.0, 1.2, 0.05))
check("close(): text is exact", pc.close("a", "a") and not pc.close("a", "b", 99))
nump = pc.Pincher(lambda x: round(x, 1), lambda x: x, lambda x: "num", tol=0.05)
for i in range(pc.n_star()):
    nump.answer(i + 0.01)
o, i2 = nump.answer(7.02)
check("numeric pincher pinches and its answer is within tolerance of full",
      i2["path"] == "pinch" and abs(o - 7.02) <= 0.05)

# ---- 4. ActiveLog route + B7 certifies product-identity --------------------------------------
r = pc.run("  Hello   WORLD ", pc.make_text_pincher())
check("pincher run replays under B7", bt.replay_route(r["log"].records)["route"] == "pinch")
check("pincher run chain verifies", al.verify_chain(r["log"].records))
check("ledger.transaction product shape == text-normalize's ({out})",
      bt.replay_route(r["log"].records)["product"] == bt.replay_route(tn.run("  Hello   WORLD ", route="full")["log"].records)["product"])
v = bt.backtest_pair(r["log"].records, tn.run("  Hello   WORLD ", route="full")["log"].records)
check("B7 certifies pinch vs full on a fallback case", v["status"] == "certified")

texts = pc.make_workload(600, pc.MIX_BALANCED)
check("workload is deterministic (seeded)", texts == pc.make_workload(600, pc.MIX_BALANCED))
bal = pc.price(texts)
rep = bal["bt"]
check("B7 certified every case of the balanced stream", rep["certified"] == 600 and rep["refused"] == 0)
check("B7 certified == n - refused", rep["certified"] + rep["refused"] == bal["n"])
check("pinched answers equal the full answer on all pinched cases",
      all(bal["bt"]["cases"][i]["status"] == "certified" for i, f in enumerate(bal["infos"]) if f["path"] == "pinch"))
check("the pincher actually pinched (some path=='pinch')", bal["paths"]["pinch"] > 0)
check("pinching saved full-route calls (measured)", bal["full_calls"] < bal["n"])
check("full-route calls == audited + fallback", bal["full_calls"] == bal["paths"]["audited"] + bal["paths"]["fallback"])
check("paths sum to n", sum(bal["paths"].values()) == bal["n"])
check("the threshold grew: >= 2 classes (A, AY) became pinchable over the stream",
      sum(1 for c in bal["pincher"].stats if bal["pincher"].pinchable(c)) >= 2)
check("AE (3% drift, 50/53 agree) stays just under the bar: conf 25/28 < 9/10",
      bal["pincher"].conf("AE") == Fraction(25, 28) and not bal["pincher"].pinchable("AE"))
check("unreliable classes (AK, AC) never pinched",
      all(bal["pincher"].stats.get(c, {"pinched": 0})["pinched"] == 0 for c in ("AK", "AC")))
check("B7 verdict hash reproducible",
      pc.price(texts)["bt"]["verdict_hash"] == rep["verdict_hash"])
check("learned table reproducible", pc.price(texts)["pincher"].digest() == bal["pincher"].digest())

# the gate bites: a pincher that always pinches (target 0) mispinches, and B7 REFUSES
reckless = pc.make_text_pincher(target=0, audit_every=10**9)
bad_texts = ["Straße  ﬁne", "Ⅷ  ＡＢＣ", "é  x", "plain  ascii"]
cases = [{"id": "b%d" % i, "a": pc.run(t, reckless)["log"].records,
          "b": tn.run(t, route="full")["log"].records} for i, t in enumerate(bad_texts)]
bad_rep = bt.backtest_corpus(cases, ("pinch", "full"))
check("reckless pinch: B7 refuses every wrong answer (3 of 4)", bad_rep["refused"] == 3 and bad_rep["certified"] == 1)
rr = bt.backtest_pair(cases[0]["a"], cases[0]["b"])
check("refusal says never price a cheaper different answer", "different answer" in rr["reason"])
check("refusal exposes no budget", "routes" not in rr and "axes" not in rr)
rres = rp.prefer([("pinch", cases[0]["a"]), ("full", cases[0]["b"])])
check("B4 also refuses to rank a mispinch", rres["status"] == "refused" and "preferred_when" not in rres)
tam = copy.deepcopy(r["log"].records)
tam[-1]["body"]["out"] = "tampered"
check("tampered pincher run is refused by replay", bt.backtest_pair(tam, tn.run("  Hello   WORLD ", route="full")["log"].records)["status"] == "refused")

# ---- 5. iron-triangle placement + B4 preferred_when (measured regimes) -------------------------
w = rep["workload"]
check("balanced: pinch is cheaper in compute-time than full (wall_ms)", rep["totals"]["pinch"]["wall_ms"] < rep["totals"]["full"]["wall_ms"])
check("balanced: B7 class is a pinch-dominates verdict", w["class"].startswith("dominates") and w["dominant"] == "pinch")
check("good axis is a tie (product-identical)", w["axes"]["good"] == "tie")
check("B4 records pinch preferred for fast and cheap on the balanced mix",
      bal["b4"]["preferred_when"]["fast"] == "pinch" and bal["b4"]["preferred_when"]["cheap"] == "pinch")
asc = pc.price(pc.make_workload(600, pc.MIX_ASCII))
adv = pc.price(pc.make_workload(600, pc.MIX_ADVERSARIAL))
check("ascii-heavy saves more wall_ms than balanced",
      asc["bt"]["totals"]["full"]["wall_ms"] - asc["bt"]["totals"]["pinch"]["wall_ms"]
      > rep["totals"]["full"]["wall_ms"] - rep["totals"]["pinch"]["wall_ms"] > 0)
check("ascii-heavy pinch rate > balanced pinch rate", asc["paths"]["pinch"] > bal["paths"]["pinch"])
check("adversarial: zero pinches, every call falls back", adv["paths"] == {"pinch": 0, "audited": 0, "fallback": 600})
check("adversarial: full route DOMINATES (fallback overhead is real)",
      adv["bt"]["workload"]["dominant"] == "full" and adv["bt"]["totals"]["pinch"]["wall_ms"] > adv["bt"]["totals"]["full"]["wall_ms"])
check("B4 flips: full preferred for fast+cheap on the adversarial mix",
      adv["b4"]["preferred_when"]["fast"] == "full" and adv["b4"]["preferred_when"]["cheap"] == "full")
check("B4 PreferenceBook recorded certified observations", bal["book"].n == 600 and "fast" in bal["book"].settled())
check("book settles on pinch for fast under the balanced mix", bal["book"].settled()["fast"]["route"] == "pinch")
check("storage is the only cheap axis that separates them (usd/tokens are 0 locally)",
      rep["totals"]["pinch"]["usd"] == rep["totals"]["full"]["usd"] == 0 and w["cheap_detail"]["compute"] == "tie")

print("pincher selftest: %d checks, %d failures" % (checks, failures))
raise SystemExit(1 if failures else 0)
