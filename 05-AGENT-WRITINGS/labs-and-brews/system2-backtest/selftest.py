#!/usr/bin/env python3
"""system2-backtest selftest — offline, deterministic (no network, no clock, no randomness)."""

from __future__ import annotations

import copy
import sys

import backtest as bt
import activeledger as al

checks = failures = 0


def check(name, cond):
    global checks, failures
    checks += 1
    if not cond:
        failures += 1
        print("FAIL:", name)


# ---- synthetic route builder (a known pair with known axes) ---------------------------
def route(label, product, wall, usd=0.0, tokens=None, prod=0, train=0, dev="synth"):
    log = al.ActiveLog(dev=dev)
    b = al.budget(wall_ms=wall, usd=usd, tokens=tokens, prod=prod, train=train)
    log.emit("cell.tick", {"route": label, "cell": "x", "kind": "SIM", "budget": b})
    log.emit("ledger.transaction", {"route": label, "path": label, "product": product,
                                    "total_budget": al.route_total(log.records, label)})
    return log.records


P = {"answer": 42}

# 1. product-identity gating: refuses on a deliberately non-identical pair, exposes no budgets
cheat = bt.backtest_pair(route("cheat", {"answer": 41}, 1), route("full", P, 100))
check("refuses non-identical products", cheat["status"] == "refused")
check("refusal reason names the law", "different answer" in cheat["reason"])
check("refusal exposes no axes/winners", "axes" not in cheat and "routes" not in cheat)
same = bt.backtest_pair(route("cheap", P, 1), route("full", P, 100))
check("certifies identical products", same["status"] == "certified")

# 2. axis-domination on known pairs
d = bt.backtest_pair(route("a", P, 10, prod=100), route("b", P, 50, prod=900))
check("faster-cheaper dominance detected",
      d["class"] == "dominates-faster-cheaper" and d["dominant"] == "a" and d["satisfices"] == "b")
check("good axis ties on identical product", d["axes"]["good"] == "tie")
d = bt.backtest_pair(route("a", P, 10, prod=900), route("b", P, 50, prod=100))
check("trade-off: fast vs cheap", d["class"] == "trade-off"
      and d["preferred_when"]["fast"] == "a" and d["preferred_when"]["cheap"] == "b")
d = bt.backtest_pair(route("a", P, 10, usd=0.5, prod=100), route("b", P, 50, usd=0.0, prod=900))
check("split cheapness (compute vs storage) is named, not merged",
      d["axes"]["cheap"] == "split" and d["cheap_detail"] == {"compute": "b", "storage": "a"})
d = bt.backtest_pair(route("a", P, 10), route("b", P, 50))
check("dominates-one-axis (fast only)", d["class"] == "dominates-one-axis" and d["dominant"] == "a")
d = bt.backtest_pair(route("a", P, 10, tokens={"m": 5}), route("b", P, 10, tokens={"m": 5}))
check("equivalent when all axes tie", d["class"] == "equivalent")
d = bt.backtest_pair(route("a", P, 10, prod=1), route("b", P, 50, prod=9),
                     quality={"A": 0.9, "B": 0.5})
check("better-faster when oracle quality also favors the same route",
      d["class"] == "dominates-all-three" and d["axes"]["good"] == "a")
d = bt.backtest_pair(route("a", P, 10, prod=5), route("b", P, 50, prod=5),
                     quality={"A": 0.9, "B": 0.5})
check("better-faster (good+fast) named", d["class"] == "dominates-better-faster")

# 3. replay integrity: tampered chain / receipt is refused, not scored
t = copy.deepcopy(route("a", P, 10)); t[0]["body"]["budget"]["wall_ms"] = 1
check("tampered record refused", bt.backtest_pair(t, route("b", P, 50))["status"] == "refused")
t = route("a", P, 10); t[-1]["body"]["total_budget"]["wall_ms"] = 999  # breaks chain? tx is last: chain ok
check("receipt/budget mismatch refused", bt.backtest_pair(t, route("b", P, 50))["status"] == "refused")

# 4. determinism: identical input -> identical verdict; verdict_hash stable
v1 = bt.backtest_pair(route("a", P, 10, prod=3), route("b", P, 50, prod=7))
v2 = bt.backtest_pair(route("a", P, 10, prod=3), route("b", P, 50, prod=7))
check("same input -> same verdict", v1 == v2 and v1["verdict_hash"] == v2["verdict_hash"])
r1, r2 = bt.run_fixtures(), bt.run_fixtures()
check("fixture replay deterministic (whole corpus)", bt.al.canon(r1) == bt.al.canon(r2))

# 5. the real example quilts' route pairs
EXPECT = {"calculator": (5, 1), "convert": (3, 5), "datetime": (5, 3),
          "text-normalize": (7, 2), "image-thumb": (3, 2)}
check("all 5 example quilts backtested", set(r1) == set(EXPECT))
for name, (cert, inapp) in EXPECT.items():
    rep = r1[name]
    check("%s: certified/inapplicable counts" % name,
          (rep["certified"], rep["inapplicable"]) == (cert, inapp))
    check("%s: no refusals (routes are product-identical)" % name, rep["refused"] == 0)
    w = rep["workload"]
    check("%s: cheap route dominates faster-cheaper" % name,
          w["class"] == "dominates-faster-cheaper" and w["dominant"] == rep["labels"][0])
    ta, tb = rep["totals"][rep["labels"][0]], rep["totals"][rep["labels"][1]]
    check("%s: cheap route strictly faster and smaller" % name,
          ta["wall_ms"] < tb["wall_ms"] and ta["storage_bytes"] < tb["storage_bytes"])

# 6. corpus-level gate: one poisoned case is refused and excluded from the totals
labels, cases = bt.fixture_pairs()["convert"]
poisoned = copy.deepcopy(cases)
tx = next(r for r in poisoned[0]["a"] if r["type"] == "ledger.transaction")
tx["body"]["product"] = "999"          # forge the product; chain also breaks -> refused either way
rep = bt.backtest_corpus(poisoned, labels)
check("poisoned case refused, rest still certified",
      rep["refused"] == 1 and rep["certified"] == r1["convert"]["certified"] - 1)

# ---- playtest hardening (PLAYTEST-REPORT.md) ----------------------------------------------
pa, pb = route("A", {"v": 1}, 5, usd=1.0), route("B", {"v": 1}, 3, usd=2.0)
check("PT: same route label on both sides is refused (was: verdict silently collapsed to one key)",
      bt.backtest_pair(route("X", {"v": 1}, 1), route("X", {"v": 1}, 2))["status"] == "refused")
try:
    bt.backtest_corpus([{"id": 1, "a": pa, "b": pb}], ("A", "A")); same_lab = False
except ValueError:
    same_lab = True
check("PT: backtest_corpus(labels=('A','A')) raises ValueError", same_lab)
check("PT: non-envelope records are 'refused', not KeyError/TypeError",
      all(bt.backtest_pair(x, x)["status"] == "refused" for x in ([{"x": 1}], [1], None, "abc")))
dl = route("A", {"v": 1}, 1); dl[-1]["body"]["path"] = {"plan": 1}
check("PT: dict-valued route label is refused (was: TypeError unhashable)", bt.backtest_pair(dl, pb)["status"] == "refused")
check("PT: non-numeric quality is refused (was: TypeError)", bt.backtest_pair(pa, pb, quality={"A": "hi", "B": 3})["status"] == "refused")
check("PT: corpus labels that do not match the routes are 'refused' per case (was: KeyError)",
      bt.backtest_corpus([{"id": 1, "a": pa, "b": pb}], ("x", "y"))["refused"] == 1)
check("PT: corpus case without an id gets its index (was: KeyError)", bt.backtest_corpus([{"a": pa, "b": pb}], ("A", "B"))["cases"][0]["id"] == 0)
check("PT: NFC vs NFD products are DIFFERENT products (byte-exact identity, documented strictness)",
      bt.backtest_pair(route("A", {"v": "\u00e9"}, 1), route("B", {"v": "e\u0301"}, 1))["status"] == "refused")
check("PT: 1 vs 1.0 and True vs 1 are different products (type-exact)",
      bt.backtest_pair(route("A", {"v": 1}, 1), route("B", {"v": 1.0}, 1))["status"] == "refused"
      and bt.backtest_pair(route("A", {"v": True}, 1), route("B", {"v": 1}, 1))["status"] == "refused")
check("PT: key order in a product does not matter", bt.backtest_pair(route("A", {"a": 1, "b": 2}, 1), route("B", {"b": 2, "a": 1}, 1))["status"] == "certified")
check("PT: empty corpus is a verdict with no workload block", "workload" not in bt.backtest_corpus([], ("A", "B")))
print("system2-backtest selftest: %d checks, %d failures" % (checks, failures))
sys.exit(1 if failures else 0)
