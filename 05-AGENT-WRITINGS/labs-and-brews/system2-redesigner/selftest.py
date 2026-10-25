#!/usr/bin/env python3
"""system2-redesigner selftest — offline, deterministic (no network; stub proposals only).

Proves the loop  propose -> B7 gate -> B4 promote  and that a product-changing proposal is
refused (never ranked), using B7 and B4 imported unmodified."""

from __future__ import annotations

import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import system2_redesigner as s2  # noqa: E402
import activeledger as al  # noqa: E402
import backtest as bt  # noqa: E402
import route_preference as rp  # noqa: E402
import textnorm_quilt as tn  # noqa: E402

checks = failures = 0


def check(name, cond):
    global checks, failures
    checks += 1
    if not cond:
        failures += 1
        print("FAIL:", name)


def stub(name):
    return copy.deepcopy([x for x in s2.STUBS if x["proposal"]["name"] == name][0])


C = s2.corpus()

# ---- the corpus ------------------------------------------------------------------------
check("corpus deterministic", s2.corpus() == C and al.content_hash(s2.corpus()) == al.content_hash(C))
check("corpus unique", len(set(C)) == len(C))
check("corpus has every ASCII code point", all(any(chr(i) in t for t in C) for i in range(128)))
check("corpus has the quilt's WORKLOAD", all(t in C for t in tn.WORKLOAD))
check("corpus gates every priced input", all(t in C for w in s2.REGIMES.values() for t in w))
check("corpus has traps", all(t in C for t in s2.TRAPS))
check("corpus has non-ASCII fuzz", sum(1 for t in C if not t.isascii()) > 50)

# ---- parse -----------------------------------------------------------------------------
def invalid(obj):
    try:
        s2.parse(obj)
        return False
    except s2.Invalid:
        return True

check("parse ok", s2.parse(stub("early-exit")["proposal"])["fallback"]["guard"] == "ascii")
check("parse rejects unknown op", invalid({"name": "x", "steps": ["nfkc", "teleport"]}))
check("parse rejects unknown guard", invalid({"name": "x", "guard": "vibes", "steps": ["nfkc"]}))
check("parse rejects empty steps", invalid({"name": "x", "steps": []}))
check("parse rejects too many steps", invalid({"name": "x", "steps": ["identity"] * 9}))
check("parse rejects bad name", invalid({"name": "x y/z", "steps": ["nfkc"]}))
check("parse rejects non-object", invalid(["nfkc"]) and invalid(None) and invalid("nfkc"))
deep = {"name": "d", "guard": "ascii", "steps": ["identity"], "fallback":
        {"guard": "ascii", "steps": ["identity"], "fallback":
         {"guard": "ascii", "steps": ["identity"], "fallback":
          {"guard": "ascii", "steps": ["identity"]}}}}
check("parse rejects depth > 3", invalid(deep))
check("parse: guard always drops fallback",
      s2.parse({"name": "a", "steps": ["nfkc"], "fallback": {"guard": "x"}})["fallback"] == "full")
check("shape hash ignores name/rationale",
      s2.shape_hash(s2.parse({"name": "a", "steps": ["nfkc"], "rationale": "r"}))
      == s2.shape_hash(s2.parse({"name": "b", "steps": ["nfkc"]})))
check("shape hash sees order",
      s2.shape_hash(s2.parse({"name": "a", "steps": ["nfkc", "casefold"]}))
      != s2.shape_hash(s2.parse({"name": "a", "steps": ["casefold", "nfkc"]})))

# ---- execute: real ActiveLog runs that B7 can replay ----------------------------------
inc = s2.INCUMBENT
for t in ["  Hello,   World!  ", "Straße  ﬁne  Ⅷ  ＡＢＣ", ""]:
    recs = s2.execute(inc, t, "incumbent")
    check("execute chain verifies %r" % t, al.verify_chain(recs))
    rep = bt.replay_route(recs)                      # B7's replay audits the budget
    check("B7 replays executed run %r" % t, rep["route"] == "incumbent")
    check("executed product shape == quilt's %r" % t,
          set(rep["product"]) == set(bt.replay_route(s2.reference(t))["product"]) == {"out"})
check("DSL full == quilt full on whole corpus",
      all(s2._product(s2.execute("full", t)) == tn.full_route(t) for t in C))
check("DSL incumbent == quilt run on whole corpus",
      all(s2._product(s2.execute(inc, t)) == tn.run(t)["out"] for t in C))
check("execute deterministic",
      al.canon(s2.execute(inc, "Ab  c")) == al.canon(s2.execute(inc, "Ab  c")))
ee = s2.parse(stub("early-exit")["proposal"])
r_clean, r_dirty = s2.execute(ee, "hello world"), s2.execute(ee, "Hello  world")
check("early exit takes the identity branch on clean input",
      any(r["body"].get("cell") == "0:identity" for r in r_clean))
check("early exit falls through on dirty input",
      not any(r["body"].get("cell") == "0:identity" for r in r_dirty)
      and any(r["body"].get("cell") == "0:map_fs_controls" for r in r_dirty))
check("early exit is cheaper on clean input",
      bt.replay_route(r_clean)["axes"]["wall_ms"] < bt.replay_route(s2.execute(inc, "hello world"))["axes"]["wall_ms"])
try:
    s2.execute(s2.parse(stub("bytes-always")["proposal"]), "é")
    check("bytes-always must raise", False)
except ValueError:
    check("bytes-always raises", True)

# ---- the gate (B7) ---------------------------------------------------------------------
g_ok = s2.gate(ee, C)
check("early-exit passes gate on all cases", g_ok == {"status": "passed", "cases": len(C)})
g_l1 = s2.gate(s2.parse(stub("latin1-lower")["proposal"]), C)
check("product-changing proposal REFUSED by B7", g_l1["status"] == "refused" and g_l1["stage"] == "b7")
check("refusal carries a real counterexample",
      g_l1["expected"] == tn.full_route(g_l1["input"]) and g_l1["got"] != g_l1["expected"])
check("refusal reason is B7's", "products differ" in g_l1["reason"])
check("refusal exposes no budget", "routes" not in g_l1 and "axes" not in g_l1)
g_nf = s2.gate(s2.parse(stub("no-nfkc")["proposal"]), C)
check("dropping NFKC refused", g_nf["status"] == "refused" and g_nf["stage"] == "b7")
g_ba = s2.gate(s2.parse(stub("bytes-always")["proposal"]), C)
check("crash refused at execute", g_ba["status"] == "refused" and g_ba["stage"] == "execute")
# the gate is the judge, not the corpus size: a wrong proposal that agrees on ASCII still fails
sneaky = s2.parse({"name": "sneaky", "guard": "always", "steps": ["nfc", "casefold", "ws_collapse"]})
check("NFC-for-NFKC passes ASCII-only corpus", s2.gate(sneaky, [chr(i) for i in range(128)])["status"] == "passed")
check("NFC-for-NFKC refused on full corpus", s2.gate(sneaky, C)["status"] == "refused")
# reordering that is safe vs. one that is not
reorder = s2.parse({"name": "ro", "steps": ["nfkc", "ws_collapse", "casefold"]})
check("casefold after ws_collapse: gate verdict is measured, not assumed",
      s2.gate(reorder, C)["status"] in ("passed", "refused"))

# ---- the whole loop: propose -> gate -> promote ---------------------------------------
R = s2.redesign(copy.deepcopy(s2.STUBS))
R2 = s2.redesign(copy.deepcopy(s2.STUBS))
check("report deterministic", R["report_hash"] == R2["report_hash"])
by = {r["name"]: r for r in R["proposals"]}
check("quilt-equiv is a duplicate of the incumbent, not a win",
      by["quilt-equiv"].get("duplicate_of") == "incumbent")
check("bad-op refused at parse", by["bad-op"]["stage"] == "parse")
check("latin1-lower refused at b7", by["latin1-lower"]["stage"] == "b7")
check("refused proposals never reach B4",
      all("p:" + n not in pr.get("workload", {}).get("routes", {})
          for n in ("latin1-lower", "no-nfkc", "bytes-always", "bad-op")
          for pr in R["promotion"].values()))
T = R["tally"]
check("tally adds up", T["proposals"] == T["passed"] + T["refused_parse"] + T["refused_execute"]
      + T["refused_b7"] + T["duplicates"])
check("tally numbers", (T["passed"], T["refused_b7"], T["refused_execute"], T["refused_parse"],
                        T["duplicates"]) == (2, 2, 1, 1, 1))
P = R["promotion"]
check("B4 certified every priced case", all(v["b4_refused_cases"] == 0 for v in P.values()))
check("clean-heavy promotes early-exit", P["clean-heavy"]["promoted"] == ["p:early-exit"])
check("clean-heavy: early-exit dominates incumbent",
      P["clean-heavy"]["vs_incumbent"]["p:early-exit"]["dominant"] == "p:early-exit")
check("quilt-workload: incumbent keeps the frontier",
      P["quilt-workload"]["workload"]["frontier"] == ["incumbent"])
check("promoted = frontier in >= 1 regime", R["promoted"] == ["p:early-exit"])
check("satisfice = passed but never frontier", R["satisfice"] == ["p:blank-exit"])
pm = P["clean-heavy"]["preference_map"]
check("preference map names a fast + cheap pick", pm["preferred_when"]["fast"] == "p:early-exit"
      and pm["preferred_when"]["cheap"] == "p:early-exit")
check("good is tie without standing (B4 semantics)", pm["preferred_when"]["good"] == "tie")
check("hebbian book settled on early-exit for cheap",
      P["clean-heavy"]["settled"]["cheap"]["route"] == "p:early-exit")
check("full is dominated everywhere",
      all("full" in v["workload"]["dominated"] for v in P.values()))

# B4's own gate still holds inside promotion: smuggle a wrong route in -> prefer() refuses
t = "Straße"
bad = s2.execute(s2.parse(stub("latin1-lower")["proposal"]), t, "p:bad")
check("B4 refuses a product-changing route even if B8 were bypassed",
      rp.prefer([("full", s2.execute("full", t, "full")), ("p:bad", bad)])["status"] == "refused")
check("nothing to promote when nothing passes",
      s2.redesign([stub("no-nfkc")])["promotion"]["clean-heavy"] == {"status": "nothing-to-promote"})

# ---- crew plumbing (offline: parsing model replies, no network) ------------------------
check("extract fenced array", s2.extract_json_array('x ```json\n[{"name":"a","steps":["nfkc"]}]\n``` y')
      == [{"name": "a", "steps": ["nfkc"]}])
check("extract single object", s2.extract_json_array('{"name":"a","steps":["nfkc"]}') == [{"name": "a", "steps": ["nfkc"]}])
check("extract garbage -> None", s2.extract_json_array("no json here") is None)
check("crew prompt names every op and guard",
      all(o in s2.crew_prompt() for o in s2.OPS) and all(g in s2.crew_prompt() for g in s2.GUARDS))
dup = s2.redesign([{"proposer": "m1", "proposal": stub("early-exit")["proposal"]},
                   {"proposer": "m2", "proposal": dict(stub("early-exit")["proposal"], name="other")}])
check("crew duplicates gated once, credited to both",
      dup["tally"]["duplicates"] == 1 and dup["proposals"][1]["duplicate_of"] == "early-exit")

print("system2-redesigner selftest: %d checks, %d failures" % (checks, failures))
sys.exit(1 if failures else 0)
