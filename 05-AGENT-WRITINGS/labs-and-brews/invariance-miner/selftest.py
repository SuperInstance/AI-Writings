#!/usr/bin/env python3
"""selftest for invariance-miner. Prints 'invariance-miner selftest: N checks, 0 failures'."""
import random
import sys

import invariance_miner as M

N = F = 0


def check(name, ok):
    global N, F
    N += 1
    if not ok:
        F += 1
        print("FAIL", name)


# mining semantics on a tiny hand log
f = lambda s: s.lower()  # noqa: E731
log = [(x, M.digest(f(x))) for x in ["Ab", "ab", "AB", "cd", "Cd", "ab "]]
m = M.mine(log, {"lower": str.lower, "strip": str.strip, "first": lambda s: s[:1]}, 1)
check("lower accepted with support 5 (Ab/ab/AB + cd/Cd)", m["lower"]["accepted"] and m["lower"]["support"] == 5)
check("strip refuted ('ab ' != 'ab' under f)", m["strip"]["refuted"])
check("first-char refuted (key 'a' holds both 'ab' and 'ab ', different products)", m["first"]["refuted"])
check("n_buckets counts partitions", M.n_buckets(log, str.lower) == 3)

# the real cells: known truths about the example quilts
tc = M.text_cell()
tc.f_safe = M._truth(tc)
for x in ["Hello   World", "  ÅNGSTRÖM  ", "Straße"]:
    check("casefold is an invariance of text/full on %r" % x, tc.f(x.casefold()) == tc.f(x))
check("strip_punct is NOT an invariance (punctuation survives)", tc.f("a.b") != tc.f("ab"))
check("sort_words is NOT an invariance", tc.f("man bites dog") != tc.f("dog bites man"))
cc = M.convert_cell()
check("canon_number is an invariance of convert/full", cc(("1.50", "km", "m")) == cc(("1.5", "km", "m")))
check("round3 is NOT (off the log's support)", cc(("1.5004", "km", "m")) != cc(("1.5", "km", "m")))
check("errors are products too (unknown unit -> ERR)", cc(("1", "KM", "m")).startswith("ERR:"))

# the pipeline
r = M.study(M.text_cell(), M.TEXT_T, M.text_traffic, seed=3)
check("mining spends zero cell calls", r["mining_calls"] == 0)
check("text: log-only adopts a planted trap", bool({"sort_words", "trunc16"} & set(r["log_only_chain"])))
check("text: guarded chain has no trap", not ({"sort_words", "trunc16", "strip_punct"} & set(r["guarded_chain"])))
check("text: guarded 0 false hits", r["guarded"]["false_hits"] == 0)
check("text: guarded hit rate > exact-key + 0.15", r["guarded"]["hit_rate"] > r["exact_key"]["hit_rate"] + 0.15)
check("text: guarded uses >10x fewer cell calls than exact-key",
      r["guarded"]["cell_calls"] * 10 < r["exact_key"]["cell_calls"])
check("text: log-only serves wrong products after the shift", r["log_only"]["false_hits"] > 0)
r2 = M.study(M.convert_cell(), M.CONV_T, M.conv_traffic, seed=4)
check("convert: round3 survives log-sampled active checks (the honest negative)", "round3" in r2["verified_chain"])
check("convert: ...and then serves wrong products", r2["verified"]["false_hits"] > 0)
check("convert: occam guard drops round3", "round3" not in r2["guarded_chain"] and "canon_number" in r2["guarded_chain"])
check("convert: guarded 0 false hits", r2["guarded"]["false_hits"] == 0)
check("convert: guarded fewer calls than exact-key", r2["guarded"]["cell_calls"] < r2["exact_key"]["cell_calls"])
check("deterministic", M.study(M.text_cell(), M.TEXT_T, M.text_traffic, seed=3)["guarded"] == r["guarded"])

print("invariance-miner selftest: %d checks, %d failures" % (N, F))
sys.exit(1 if F else 0)
