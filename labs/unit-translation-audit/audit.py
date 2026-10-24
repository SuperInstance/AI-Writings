"""unit-translation-audit (B2) — prove every route.hop's unit translation round-trips.

Given an ActiveLog run, replay each `route.hop` {credit, debit, price} through an
EFFECT(forward, inverse) pair built from `price.rate` (mirrors quilt-studio's contract:
the inverse IS the round-trip auditor) and classify it:

    EXACT       forward reproduces the recorded debit and inverse returns the recorded
                credit with ZERO residual, in exact rational arithmetic
                (floats are read as the decimal literal they print as: 0.01 -> 1/100).
    WITHIN_TOL  not bit-exact (float representation / 9-dp rounding) but the round-trip
                residual is <= rel_tol of the credit.
    LOSSY       the round trip does NOT return the original beyond rel_tol. The record
                names WHY (integer-quantized debit, k-dp rounded debit, zero rate, ...).

The audit is a PURE REPLAY over recorded hops (OrgBook's replay = live): no clocks, no
randomness, no I/O, so the same run always audits to the same `audit_digest`.

    python3 audit.py            # audits the calculator + convert example quilts
"""

from __future__ import annotations

import os
import sys
from decimal import Decimal
from fractions import Fraction

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "activeledger"))
import activeledger as al  # noqa: E402

AUDIT_V = 1
EXACT, WITHIN_TOL, LOSSY = "EXACT", "WITHIN_TOL", "LOSSY"
AFFINE_UNITS = {"C", "F"}  # offset scales: a single multiplicative `rate` cannot be their true translation
DEFAULT_REL_TOL = 1e-9


def rat(x) -> Fraction:
    """Read a recorded number as the decimal literal it prints as (exact, deterministic)."""
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x)
    return Fraction(Decimal(repr(x)))


class Effect:
    """EFFECT(forward, inverse): inverse(forward(x)) == x is the round-trip contract."""

    def __init__(self, forward, inverse):
        self.forward, self.inverse = forward, inverse

    @classmethod
    def from_rate(cls, rate: Fraction):
        if rate == 0:
            return cls(lambda x: x * rate, None)  # no inverse exists
        return cls(lambda x: x * rate, lambda y: y / rate)


def _dp(x: Fraction) -> int:
    """Decimal places needed to write x exactly (capped) — 0 for integers."""
    d = 0
    while x.denominator != 1 and d < 15:
        x *= 10
        d += 1
        x = Fraction(x)
    return d if x.denominator == 1 else 15


def _explain(credit: Fraction, debit: Fraction, ideal: Fraction) -> str:
    err = abs(debit - ideal)
    k = _dp(debit)
    if k == 0:
        return ("debit is an integer but credit*rate = %s has a fractional part; "
                "sub-unit remainder %s dropped (integer-quantized debit)"
                % (_fmt(ideal), _fmt(err)))
    return ("debit carries only %d decimal place(s) but credit*rate = %s; "
            "rounding error %s exceeds tolerance (%d-dp rounded debit)"
            % (k, _fmt(ideal), _fmt(err), k))


def _fmt(x: Fraction) -> str:
    return "%.12g" % float(x)


def audit_hop(rec: dict, rel_tol: float = DEFAULT_REL_TOL) -> dict:
    """Audit one route.hop envelope -> a per-hop audit record (pure function)."""
    b = rec["body"]
    cr, de, pr = b["credit"], b["debit"], b["price"]
    credit, debit, rate = rat(cr["amount"]), rat(de["amount"]), rat(pr["rate"])
    out = {"seq": rec.get("seq"), "route": b.get("route"),
           "credit": "%s %s" % (cr["amount"], cr["units"]),
           "debit": "%s %s" % (de["amount"], de["units"]),
           "rate": pr["rate"], "translation": "%s->%s" % (pr.get("from", cr["units"]),
                                                          pr.get("to", de["units"])),
           "ref": pr.get("ref"), "units_match_price": (pr.get("from", cr["units"]) == cr["units"]
                                                      and pr.get("to", de["units"]) == de["units"]),
           "balanced_1e-6": al.hop_balanced(b)}
    out["caveats"] = []
    if out["translation"].split("->")[0] != out["translation"].split("->")[1] and (
            {cr["units"], de["units"]} & AFFINE_UNITS):
        out["caveats"].append("affine unit: rate is a per-value ratio (valid for this amount only), "
                              "not a linear translation; round-trip proves self-consistency, not the law")
    eff = Effect.from_rate(rate)
    if eff.inverse is None:
        out.update(cls=LOSSY, residual=None, reason="zero rate: translation is not invertible")
        return out
    ideal = eff.forward(credit)                 # what the price says the debit should be
    back = eff.inverse(debit)                   # push the RECORDED debit back through the inverse
    fwd_res = abs(ideal - debit)
    rt_res = abs(back - credit)                 # round-trip residual, in credit units
    scale = abs(credit) if credit != 0 else Fraction(1)
    rel = rt_res / scale
    out["residual_abs"] = _fmt(rt_res)
    out["residual_rel"] = _fmt(rel)
    if fwd_res == 0 and rt_res == 0:
        out.update(cls=EXACT, reason="forward and inverse exact in rational arithmetic")
    elif rel <= Fraction(rel_tol):
        out.update(cls=WITHIN_TOL,
                   reason="float/9-dp representation; round-trip residual %s <= rel_tol %g"
                          % (_fmt(rel), rel_tol))
    else:
        out.update(cls=LOSSY, reason=_explain(credit, debit, ideal))
    return out


def hops_of(run) -> list:
    """Accept an ActiveLog, a records list, or a JSONL string; return route.hop envelopes."""
    if hasattr(run, "records"):
        run = run.records
    elif isinstance(run, str):
        import json
        run = [json.loads(l) for l in run.splitlines() if l.strip()]
    return [r for r in run if r.get("type") == "route.hop"]


def audit_run(run, rel_tol: float = DEFAULT_REL_TOL) -> dict:
    """Audit every hop of a run -> {hops:[...], receipt:{...}}. Deterministic replay."""
    hops = hops_of(run)
    recs = [audit_hop(h, rel_tol) for h in hops]
    counts = {EXACT: 0, WITHIN_TOL: 0, LOSSY: 0}
    for r in recs:
        counts[r["cls"]] += 1
    receipt = {"audit_v": AUDIT_V, "rel_tol": rel_tol, "n_hops": len(recs), "counts": counts,
               "round_trips": counts[LOSSY] == 0,
               "input_digest": al.content_hash([h["body"] for h in hops]),
               "audit_digest": al.content_hash(recs)}
    return {"hops": recs, "receipt": receipt}


def merge_receipts(named: dict) -> dict:
    """Roll several {name: audit_run(...)} into one summary receipt."""
    counts = {EXACT: 0, WITHIN_TOL: 0, LOSSY: 0}
    for a in named.values():
        for k, v in a["receipt"]["counts"].items():
            counts[k] += v
    return {"audit_v": AUDIT_V, "runs": len(named), "n_hops": sum(counts.values()),
            "counts": counts,
            "audit_digest": al.content_hash({k: a["receipt"]["audit_digest"]
                                             for k, a in sorted(named.items())})}


# ---- CLI over the example quilts ---------------------------------------------------------

def audit_examples() -> dict:
    ex = os.path.join(_HERE, "..", "examples")
    sys.path.insert(0, os.path.join(ex, "calculator-quilt"))
    sys.path.insert(0, os.path.join(ex, "convert-quilt"))
    import calc_quilt as calc
    import convert_quilt as conv
    named = {}
    for i, eq in enumerate(calc.WORKLOAD):
        named["calc/%d:%s" % (i, eq["op"])] = audit_run(calc.run(eq)["log"])
    for i, q in enumerate(conv.WORKLOAD):
        named["convert/%d:%s%s->%s" % (i, q["value"], q["src"], q["dst"])] = audit_run(conv.run(q)["log"])
    return named


if __name__ == "__main__":
    named = audit_examples()
    for name, a in named.items():
        for h in a["hops"]:
            print("%-22s %-11s %-10s %s -> %s  rate=%s" % (
                name, h["cls"], h["translation"], h["credit"], h["debit"], h["rate"]))
            if h["cls"] == LOSSY:
                print("    why: %s" % h["reason"])
    print("SUMMARY", merge_receipts(named))
