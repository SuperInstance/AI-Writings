"""unit-translation-audit selftest — offline, deterministic, stdlib only."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import audit as A
al = A.al

n = fails = 0
def check(name, cond):
    global n, fails
    n += 1
    if not cond:
        fails += 1
        print("FAIL:", name)

def hop(src, dst, su, du, sa, da, rate, **extra):
    b = {"credit": {"cell": src, "units": su, "amount": sa},
         "debit": {"cell": dst, "units": du, "amount": da},
         "price": {"from": su, "to": du, "rate": rate}, "budget": al.budget(1)}
    b.update(extra)
    return b

def raw(body):  # bypass ActiveLog.emit's zero-sum gate so lossy fixtures can exist
    return [{"type": "route.hop", "seq": 0, "body": body}]

def run_of(hops):
    log = al.ActiveLog(dev="fixture")
    for h in hops:
        log.emit("route.hop", h)
    return log

# --- exact-rate hops -> EXACT -----------------------------------------------------------------
exact = A.audit_run(run_of([
    hop("a", "b", "USD", "USD-cents", 12.34, 1234, 100.0),
    hop("b", "c", "USD-cents", "USD", 1800.0, 18, 0.01),
    hop("a", "b", "m", "m", 12.5, 12.5, 1.0),
    hop("a", "b", "cm", "m", 100.0, 1.0, 0.01),
]))
check("exact: 4 hops audited", exact["receipt"]["n_hops"] == 4)
check("exact: all EXACT", [h["cls"] for h in exact["hops"]] == [A.EXACT] * 4)
check("exact: zero residual", all(h["residual_abs"] == "0" for h in exact["hops"]))
check("exact: round_trips", exact["receipt"]["round_trips"] is True)
check("exact: 0.01 read as 1/100", A.rat(0.01) == A.Fraction(1, 100))
check("exact: 12.34*100 exact", A.rat(12.34) * 100 == 1234)

# --- Effect contract ---------------------------------------------------------------------------
eff = A.Effect.from_rate(A.Fraction(1, 100))
check("effect: inverse(forward(x)) == x", eff.inverse(eff.forward(A.Fraction(617))) == 617)
check("effect: zero rate has no inverse", A.Effect.from_rate(A.Fraction(0)).inverse is None)

# --- deliberately lossy fixtures ----------------------------------------------------------------
h = A.audit_run(raw(hop("calc", "res", "USD-cents", "USD", 617.0, 6, 0.01)))["hops"][0]
check("lossy: classified LOSSY", h["cls"] == A.LOSSY)
check("lossy: reason names integer quantization", "integer-quantized" in h["reason"])
check("lossy: 17 cents dropped", "0.17" in h["reason"])
check("lossy: not balanced at 1e-6 either", h["balanced_1e-6"] is False)
check("lossy: receipt round_trips False",
      A.audit_run(raw(hop("c", "r", "USD-cents", "USD", 617.0, 6, 0.01)))["receipt"]["round_trips"] is False)
try:
    run_of([hop("c", "r", "USD-cents", "USD", 617.0, 6, 0.01)])
    check("emit gate rejects the lossy hop", False)
except ValueError:
    check("emit gate rejects the lossy hop", True)
dp = A.audit_run(raw(hop("a", "b", "g", "kg", 4535.9237, 4.5, 0.001)))["hops"][0]
check("lossy: k-dp rounded debit explained", dp["cls"] == A.LOSSY and "1 decimal" in dp["reason"])
zr = A.audit_run(raw(hop("a", "b", "x", "y", 5, 0, 0)))["hops"][0]
check("lossy: zero rate not invertible", zr["cls"] == A.LOSSY and "not invertible" in zr["reason"])

# --- within tolerance ----------------------------------------------------------------------------
wt_body = hop("a", "b", "g", "kg", 4535.9237, 4.535924, 0.0010000000661386785)
check("within-tol: float-rate hop WITHIN_TOL", A.audit_run(raw(wt_body))["hops"][0]["cls"] == A.WITHIN_TOL)
check("within-tol: tighter tol reclassifies LOSSY",
      A.audit_run(raw(wt_body), rel_tol=1e-17)["hops"][0]["cls"] == A.LOSSY)

# --- affine caveat -------------------------------------------------------------------------------
af = A.audit_run(raw(hop("a", "b", "K", "C", 300.0, 26.85, 0.08950000000000001)))["hops"][0]
check("affine: caveat recorded", len(af["caveats"]) == 1)

# --- replay determinism --------------------------------------------------------------------------
log = run_of([hop("a", "b", "USD", "USD-cents", 12.34, 1234, 100.0)])
a1, a2 = A.audit_run(log), A.audit_run(log)
check("replay: identical audit", a1 == a2)
check("replay: identical digest", a1["receipt"]["audit_digest"] == a2["receipt"]["audit_digest"])
check("replay: JSONL replay == live", A.audit_run(log.to_jsonl())["receipt"] == a1["receipt"])
check("replay: input_digest = content hash of hop bodies",
      a1["receipt"]["input_digest"] == al.content_hash([r["body"] for r in log.records]))
check("input accepts records list", A.audit_run(log.records) == a1)
t = json.loads(log.to_jsonl().splitlines()[0]); t["body"]["debit"]["amount"] = 1235
check("replay: tamper changes digest",
      A.audit_run([t])["receipt"]["audit_digest"] != a1["receipt"]["audit_digest"])
check("non-hop records ignored", A.audit_run([{"type": "cell.tick", "body": {}}])["receipt"]["n_hops"] == 0)

# --- REAL example quilts as fixtures -----------------------------------------------------------------
ex1, ex2 = A.audit_examples(), A.audit_examples()
m = A.merge_receipts(ex1)
check("examples: audited twice identically", m == A.merge_receipts(ex2))
check("examples: 25 real hops", m["n_hops"] == 25)
check("examples: counts 16/4/5",
      (m["counts"]["EXACT"], m["counts"]["WITHIN_TOL"], m["counts"]["LOSSY"]) == (16, 4, 5))
calc_hops = [h for k, a in ex1.items() if k.startswith("calc/") for h in a["hops"]]
check("calc: every USD->cents hop EXACT",
      all(h["cls"] == A.EXACT for h in calc_hops if h["translation"] == "USD->USD-cents"))
check("calc: 5 of 6 cents->USD hops LOSSY",
      [h["cls"] for h in calc_hops if h["translation"] == "USD-cents->USD"].count(A.LOSSY) == 5)
conv_hops = [h for k, a in ex1.items() if k.startswith("convert/") for h in a["hops"]]
check("convert: no LOSSY hops", all(h["cls"] != A.LOSSY for h in conv_hops))
check("convert: identity hops EXACT", all(h["cls"] == A.EXACT for h in conv_hops if h["rate"] == 1.0))
check("convert: 3 temperature hops carry affine caveat", sum(1 for h in conv_hops if h["caveats"]) == 3)

print("unit-translation-audit selftest: %d checks, %d failures" % (n, fails))
sys.exit(1 if fails else 0)
