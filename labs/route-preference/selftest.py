#!/usr/bin/env python3
"""route-preference selftest — offline, deterministic (no network, no clock, no randomness)."""

from __future__ import annotations

import copy
import sys

import route_preference as rp
import activeledger as al

checks = failures = 0


def check(name, cond):
    global checks, failures
    checks += 1
    if not cond:
        failures += 1
        print("FAIL:", name)


def route(label, product, wall, usd=0.0, tokens=None, prod=0, train=0):
    log = al.ActiveLog(dev="synth")
    b = al.budget(wall_ms=wall, usd=usd, tokens=tokens, prod=prod, train=train)
    log.emit("cell.tick", {"route": label, "cell": "x", "kind": "SIM", "budget": b})
    log.emit("ledger.transaction", {"route": label, "path": label, "product": product,
                                    "total_budget": al.route_total(log.records, label)})
    return log.records


P = {"answer": 42}

# 1. refusal: the product gate runs first
r = rp.prefer([("cheat", route("cheat", {"answer": 41}, 1)), ("full", route("full", P, 100))])
check("refuses when products differ", r["status"] == "refused")
check("refusal names the law", "disagree on the answer" in r["reason"])
check("refusal exposes no axes/frontier/preferences",
      not ({"routes", "frontier", "preferred_when"} & set(r)))
r3 = rp.prefer([("a", route("a", P, 1)), ("b", route("b", P, 2)), ("c", route("c", {"answer": 0}, 3))])
check("one odd route out among three refuses the whole set", r3["status"] == "refused")
check("refuses a single route", rp.prefer([("a", route("a", P, 1))])["status"] == "refused")
check("refuses duplicate names", rp.prefer([("a", route("a", P, 1)), ("a", route("a", P, 2))])["status"] == "refused")
bad = route("b", P, 2)
bad[0] = copy.deepcopy(bad[0]); bad[0]["body"]["budget"]["wall_ms"] = 1
tam = rp.prefer([("a", route("a", P, 1)), ("b", bad)])
check("refuses a tampered route (replay fails)", tam["status"] == "refused" and "replay" in tam["reason"])
check("refuses float standing (identity never floats)",
      rp.prefer_axes({"a": rp.bt.axes_of(al.budget(wall_ms=1)), "b": rp.bt.axes_of(al.budget(wall_ms=2))},
                     {"a": 0.5, "b": 1})["status"] == "refused")
check("refuses negative standing",
      rp.prefer([("a", route("a", P, 1)), ("b", route("b", P, 2))], {"a": -1, "b": 0})["status"] == "refused")
check("refuses standing for an unknown route",
      rp.prefer([("a", route("a", P, 1)), ("b", route("b", P, 2))], {"zzz": 1})["status"] == "refused")

# 2. pareto frontier
A = ("A", route("A", P, 10, prod=900))              # fastest, big storage
B = ("B", route("B", P, 50, prod=100))              # slowest of the pair, smallest storage
C = ("C", route("C", P, 60, prod=950))              # worse than A and B on every axis
res = rp.prefer([A, B, C])
check("certified", res["status"] == "certified")
check("genuine trade-off: A and B both on the frontier", res["frontier"] == ["A", "B"])
check("class is trade-off (no route dominates)", res["class"] == "trade-off")
check("C is dominated, and by whom", res["dominated"] == {"C": ["A", "B"]})
pw = res["preferred_when"]
check("fast -> A, cheap -> B", pw["fast"] == "A" and pw["cheap"] == "B")
check("faster-cheaper is null: no route is best on both", pw["faster-cheaper"] is None)
check("good is a tie without standing", pw["good"] == "tie" and res["good_source"] == "tie")
check("with good tied, better-faster reduces to the fast winner", pw["better-faster"] == "A")
check("with good tied, better-cheaper reduces to the cheap winner", pw["better-cheaper"] == "B")

dom = rp.prefer([("a", route("a", P, 10, prod=100)), ("b", route("b", P, 50, prod=900))])
check("a dominating route is the sole frontier member", dom["frontier"] == ["a"] and dom["class"] == "dominant")
check("dominating route takes every priority incl. faster-cheaper",
      dom["preferred_when"]["faster-cheaper"] == "a" and dom["dominated"] == {"b": ["a"]})

# split cheapness: usd vs storage -> incomparable, both stay
sp = rp.prefer([("s", route("s", P, 10, usd=0.5, prod=100)), ("t", route("t", P, 10, usd=0.0, prod=900))])
check("incomparable cheapness keeps both on the frontier", sp["frontier"] == ["s", "t"])
check("incomparable cheap tie is reported", sp["tied"].get("cheap") == ["s", "t"])
check("equal routes: all tie, nothing dominated",
      rp.prefer([("x", route("x", P, 5)), ("y", route("y", P, 5))])["dominated"] == {})

# 3. the OrgBook join: standing supplies good
st = rp.prefer([A, B, C], standing={"A": 1, "B": 5, "C": 5})
check("standing makes good a real axis", st["good_source"] == "standing" and st["preferred_when"]["good"] == "B")
check("better-cheaper now names B (best good AND cheap)", st["preferred_when"]["better-cheaper"] == "B")
check("better-faster is null: A is fast, B has the standing", st["preferred_when"]["better-faster"] is None)
check("C still dominated by B (equal standing, worse budget)", "B" in st["dominated"]["C"])
d = rp.prefer([A, B, ("D", route("D", P, 90, prod=990))], standing={"A": 1, "B": 1, "D": 9})
check("high standing keeps a slow, pricey route on the frontier", "D" in d["frontier"])
check("...and good picks it", d["preferred_when"]["good"] == "D")
part = rp.prefer([A, B], standing={"A": 3})
check("partial standing is treated as a tie (not invented)", part["good_source"] == "tie")

# 4. hebbian reinforcement
book = rp.PreferenceBook()
hist = []
for _ in range(6):
    book.observe(rp.prefer([A, B, C], weights=book.weights))
    hist.append(book.weights["fast"]["A"])
check("weight for the confirmed route grows with each confirmation",
      all(x < y for x, y in zip(hist, hist[1:])))
check("weight is bounded by SCALE", all(0 <= w <= rp.SCALE for p in book.weights.values() for w in p.values()))
for _ in range(200):
    book.observe(rp.prefer([A, B, C]))
check("weight saturates below/at SCALE, never past it", book.weights["fast"]["A"] <= rp.SCALE
      and book.weights["fast"]["A"] > 0.99 * rp.SCALE)
check("the unconfirmed route decays toward 0 for that priority", book.weights["fast"]["B"] < 10)
check("weights are ints (no float)", all(isinstance(w, int) for p in book.weights.values() for w in p.values()))
check("settled() names the consistently confirmed route",
      book.settled()["fast"]["route"] == "A" and book.settled()["cheap"]["route"] == "B")
check("null pair priority never accumulates weight", "faster-cheaper" not in book.weights)
w0 = copy.deepcopy(book.weights)
book.observe(rp.prefer([("cheat", route("cheat", {"answer": 1}, 1)), ("f", route("f", P, 2))]))
check("a refused result changes nothing", book.weights == w0)
before = copy.deepcopy(book.weights)
rp.reinforce_weights(book.weights, rp.prefer([A, B, C]))
check("reinforce_weights is pure (input not mutated)", book.weights == before)

# evidence flips the settled answer only when it accumulates
book2 = rp.PreferenceBook()
fast_a = rp.prefer([("A", route("A", P, 10, prod=100)), ("B", route("B", P, 50, prod=100))])
fast_b = rp.prefer([("A", route("A", P, 50, prod=100)), ("B", route("B", P, 10, prod=100))])
for _ in range(5):
    book2.observe(fast_a)
book2.observe(fast_b)
check("one contrary result does not flip a well-confirmed preference", book2.settled()["fast"]["route"] == "A")
for _ in range(8):
    book2.observe(fast_b)
check("sustained contrary evidence does flip it", book2.settled()["fast"]["route"] == "B")

# weights break ties only; they never override a strict win
tie = [("p", route("p", P, 10, prod=100)), ("q", route("q", P, 10, prod=100))]
check("tie with no weights -> name order", rp.prefer(tie)["preferred_when"]["fast"] == "p")
check("tie with weights -> heavier route", rp.prefer(tie, weights={"fast": {"q": 500}})["preferred_when"]["fast"] == "q")
check("weights cannot override a strict win",
      rp.prefer([A, B], weights={"fast": {"B": rp.SCALE}})["preferred_when"]["fast"] == "A")

# 5. determinism + hash
r1, r2 = rp.prefer([A, B, C], {"A": 1, "B": 5, "C": 5}), rp.prefer([A, B, C], {"A": 1, "B": 5, "C": 5})
check("same inputs -> identical result", r1 == r2)
check("result_hash is fnv1a-64 shaped", r1["result_hash"].startswith("0x") and len(r1["result_hash"]) == 18)
body = {k: v for k, v in r1.items() if k != "result_hash"}
check("result_hash recomputes from the body (replay == live)", al.content_hash(body) == r1["result_hash"])
check("route order does not change the result", rp.prefer([C, B, A], {"A": 1, "B": 5, "C": 5}) == r1)
check("standing changes the hash", rp.prefer([A, B, C])["result_hash"] != r1["result_hash"])
check("refused results are hashed too", "result_hash" in r)
bk1, bk2 = rp.PreferenceBook(), rp.PreferenceBook()
for x in (r1, r2, rp.prefer([A, B, C])):
    bk1.observe(x); bk2.observe(x)
check("book digest is reproducible from the same sequence", bk1.digest() == bk2.digest())

# 6. real example-quilt fixtures
demo = rp.demo()
check("demo covers all 5 example quilts", len(demo) == 5)
check("every example workload is certified with a non-empty frontier",
      all(v["workload"] and v["workload"]["status"] == "certified" and v["workload"]["frontier"] for v in demo.values()))
check("no fixture case was refused",
      all(c["status"] == "certified" for v in demo.values() for c in v["cases"]))
check("the cheap route is preferred for fast and cheap on every quilt",
      all(v["workload"]["preferred_when"]["fast"] == v["labels"][0]
          and v["workload"]["preferred_when"]["cheap"] == v["labels"][0] for v in demo.values()))
check("demo is deterministic", rp.demo() == demo)

print("route-preference selftest: %d checks, %d failures" % (checks, failures))
sys.exit(1 if failures else 0)
