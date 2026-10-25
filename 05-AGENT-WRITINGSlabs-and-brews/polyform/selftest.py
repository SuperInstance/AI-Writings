#!/usr/bin/env python3
"""polyform selftest: golden correctness, agreement among formalisms that actually ran,
the reference-only path, and that a deliberately wrong impl is caught and localized."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import polyform as pf

n = fails = 0


def check(cond, label):
    global n, fails
    n += 1
    if not cond:
        fails += 1
        print("FAIL:", label)


# 1. golden correctness --------------------------------------------------------------------------
PUBLISHED = {"empty": "cbf29ce484222325", "a": "af63dc4c8601ec8c", "foobar": "85944171f73967e8",
             "fox": "f3f9b7f5e7e47110"}
for name, (data, want) in pf.GOLDEN.items():
    check(pf._hex(pf.fnv1a64(data)) == want, "python baseline == pinned golden for %r" % name)
    check(pf._hex(pf.limb_model(data)) == want, "limb model (the BQN/Uiua algorithm) == golden for %r" % name)
for name, want in PUBLISHED.items():
    check(pf.GOLDEN[name][1] == want, "pin for %r equals the published FNV-1a-64 value" % name)
check(pf.OFFSET == 0xCBF29CE484222325 and pf.PRIME == 0x100000001B3, "constants are the FNV-64 offset/prime")
check(len({g for _, g in pf.GOLDEN.values()}) == len(pf.GOLDEN), "golden hashes are all distinct")

# 2. the real N-way run --------------------------------------------------------------------------
res = pf.run_all(disabled=[])
by = {r["name"]: r for r in res}
check(set(by) == {"python", "bqn", "futhark", "uiua"}, "all four formalisms are registered")
check(by["python"]["status"].startswith("ran, agreed"), "python baseline runs and agrees")
check(pf.ok(res), "no divergence and no toolchain error among present toolchains")
ran = [r for r in res if r["status"].startswith("ran, agreed")]
for r in res:
    check(r["status"].startswith(("ran, agreed", "reference-only")), "%s is either ran+agreed or reference-only" % r["name"])
    if r["status"].startswith("reference-only"):
        check(r["toolchain"] is None, "%s reference-only only because its toolchain is absent" % r["name"])
    else:
        check(all(r["results"][v] == g for v, (_, g) in pf.GOLDEN.items()), "%s: every vector matches golden" % r["name"])
check(len({tuple(sorted(r["results"].items())) for r in ran}) == 1, "all formalisms that ran produced identical outputs")
print("  (ran here: %s)" % ", ".join(r["name"] for r in ran))

# 3. absent toolchain -> reference-only, never 'agreed' -----------------------------------------
res2 = pf.run_all(disabled=["bqn", "futhark", "uiua"])
for r in res2:
    if r["name"] != "python":
        check(r["status"] == "reference-only (toolchain absent)", "%s marked reference-only when absent" % r["name"])
        check("agreed" not in r["status"], "%s never claims agreement without running" % r["name"])
        check(r["reference_check"]["constants_in_source"], "%s source carries the FNV constants" % r["name"])
        check(r["reference_check"]["model_matches_golden"], "%s algorithm model matches golden" % r["name"])
        check("results" not in r, "%s has no run results when absent" % r["name"])
check(pf.ok(res2), "absent toolchains do not fail the harness")
check("reference-only: bqn, futhark, uiua" in pf.report(res2), "report lists the reference-only formalisms")

# 4. a deliberately wrong impl is caught and localized ------------------------------------------
def wrong_prime(_tc, data):
    h = pf.OFFSET
    for b in data:
        h = ((h ^ b) * 0x100000001B4) & ((1 << 64) - 1)   # prime off by one
    return pf._hex(h)


def fnv1_order(_tc, data):
    h = pf.OFFSET
    for b in data:
        h = (((h * pf.PRIME) & ((1 << 64) - 1)) ^ b)      # FNV-1 (multiply then xor), not 1a
    return pf._hex(h)


def trunc32_long(_tc, data):
    v = pf.fnv1a64(data)
    return pf._hex(v & 0xFFFFFFFF) if len(data) >= 256 else pf._hex(v)   # breaks only on long inputs


def boom(_tc, data):
    raise RuntimeError("simulated crash")


good = pf.FORMALISMS[0]
mk = lambda name, fn: pf.Formalism(name, "fnv1a.py", lambda: "x", fn, model=pf.fnv1a64)
res3 = pf.run_all([good, mk("wrong-prime", wrong_prime), mk("fnv1", fnv1_order), mk("trunc32", trunc32_long), mk("crash", boom)])
by3 = {r["name"]: r for r in res3}
check(by3["python"]["status"].startswith("ran, agreed"), "good formalism still agrees next to broken ones")
check(by3["wrong-prime"]["status"] == "DIVERGED", "wrong prime is caught as DIVERGED")
check(set(by3["wrong-prime"]["diverged_on"]) == set(pf.GOLDEN) - {"empty"}, "wrong prime diverges on every non-empty vector (empty has no multiply)")
check(by3["fnv1"]["status"] == "DIVERGED" and "empty" not in by3["fnv1"]["diverged_on"], "FNV-1 order is caught, not on the empty input")
check(by3["trunc32"]["diverged_on"] == ["all-bytes", "kilo-mixed"], "length-dependent bug is localized to the long vectors only")
check(by3["crash"]["status"] == "toolchain error", "a present toolchain that crashes is an error, not reference-only")
check(not pf.ok(res3), "harness fails when any formalism diverges")
check("DIVERGENCE localized to wrong-prime" in pf.report(res3), "report names the diverging formalism")
check(pf.ok([by3["python"]]), "ok() passes with only agreeing formalisms")

# 4. playtest hardening (PLAYTEST-REPORT.md) -------------------------------------------------
import random, subprocess
rng = random.Random(5)
mism = 0
for _ in range(3000):
    d = bytes(rng.randrange(256) for _ in range(rng.choice((0, 1, 2, 3, 7, 8, 9, 16, 17, 255, 256, 1000))))
    mism += pf.limb_model(d) != pf.fnv1a64(d)
check(mism == 0, "PT: limb model (the BQN/Uiua algorithm) == python fnv1a64 on 3000 random inputs (carry edge cases incl. 0xff runs)")
check(pf.limb_model(b"\xff" * 5000) == pf.fnv1a64(b"\xff" * 5000), "PT: limb model correct on 5000 x 0xff")
check(not pf.ok([]), "PT: ok([]) is False (was vacuously True)")
check(not pf.ok(pf.run_all(disabled=["python", "bqn", "futhark", "uiua"])), "PT: ok() is False when NO formalism ran (everything disabled was 'OK')")
try:
    pf.run_all(vectors={}, disabled=[]); empty_ok = False
except ValueError:
    empty_ok = True
check(empty_ok, "PT: an empty vector set is refused (was 'ran, agreed on golden (0/0 vectors)')")
for bad in ("1 2 3 -4", "1 2 3 ¯4", "1.5 2 3", "1e3 2 3", "65536 0 0 0", "1 2 3"):
    try:
        pf._limbs_to_hex(bad); got = False
    except RuntimeError:
        got = True
    check(got, "PT: _limbs_to_hex rejects %r" % bad)
check(pf._limbs_to_hex("⟨ 8997 33826 40164 52210 ⟩") == "cbf29ce484222325", "PT: _limbs_to_hex still parses a BQN-style vector")
cli = lambda *a: subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "polyform.py"), *a],
                                capture_output=True, text=True).returncode
check(cli("--require=bqnn") == 2, "PT: --require with an unknown formalism name exits 2 (typo used to exit 0 = false assurance)")
check(cli("--require", "bqnn") == 2, "PT: space-separated '--require NAME' is parsed too (was silently ignored)")
check(cli("--require=python") == 0, "PT: --require=python (present) still passes")
check(pf.check_reference_only(pf.FORMALISMS[1], {"a": (b"a", pf.GOLDEN["a"][1])})["constants_in_source"],
      "KNOWN LIMIT: reference-only = constants-in-source text + python model of the algorithm; it is NOT a run of BQN/Uiua/Futhark (none installed here)")
print("polyform selftest: %d checks, %d failures" % (n, fails))
sys.exit(1 if fails else 0)
