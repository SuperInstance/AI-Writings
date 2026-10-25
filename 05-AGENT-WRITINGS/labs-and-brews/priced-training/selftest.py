"""priced-training selftest — offline, deterministic, stdlib only (~2.5 min).

Every check is a claim README.md or situations/arch/PRICED-TRAINING.md makes. Each prints the
measured value it depends on, so a failure shows the number, not just "False".
"""

from __future__ import annotations

import copy
import sys

import nettrain as N
import prereg as R
import priced_training as P
import route_witness as W

import backtest as bt

CHECKS, FAILS = [], []


def check(name, ok, detail=""):
    CHECKS.append(name)
    if not ok:
        FAILS.append(name)
    print("  [%s] %s%s" % ("ok" if ok else "FAIL", name, ("  — " + str(detail)) if detail else ""))


def main():
    S = len(P.SEEDS)
    print("== trainer + receipts")
    r = N.train("circle", "fp64", 1)
    check("receipt chain verifies", N.verify_chain(r["chain"]), r["tip"][:16])
    bad = copy.deepcopy(r["chain"])
    bad[5]["loss"] += 1e-12
    check("edited loss is detected", not N.verify_chain(bad))
    bad = copy.deepcopy(r["chain"])
    del bad[3]
    check("dropped epoch is detected", not N.verify_chain(bad))
    check("same seed -> byte-identical chain", N.train("circle", "fp64", 1)["tip"] == r["tip"])
    check("different seed -> different chain", N.train("circle", "fp64", 2)["tip"] != r["tip"])
    check("dtype is in the digest (f32 vs f64 of the same value differ)",
          N.weight_root([0.5], "f32") != N.weight_root([0.5], "f64"))
    check("bf16 rounding keeps 8 mantissa bits", N.to_bf16_rn(1.0 + 2 ** -9) == 1.0
          and N.to_bf16_rn(1.0 + 2 ** -7) == 1.0 + 2 ** -7)
    sr = [N.to_bf16_sr(1.0 + 2 ** -9, k) for k in range(0, 65536, 257)]
    check("stochastic rounding is unbiased-ish (mean within 2% of the exact value's offset)",
          abs(sum(sr) / len(sr) - (1.0 + 2 ** -9)) < 0.02 * 2 ** -9 + 2 ** -16, sum(sr) / len(sr))
    xs = N.heldout("circle", 64)
    recs = N.to_activelog(r, "labels", xs)
    rep = bt.replay_route(recs)
    check("ActiveLog run replays in B7 (chain + budget audit)", rep["route"] == "fp64", rep["axes"])

    print("== the full report (E1-E4)")
    rp = P.report()
    for task in N.TASKS:
        t = rp["tasks"][task]
        e = t["e1_e2"]
        check("%s: reference is deterministic" % task, t["ref_deterministic"])
        for impl in ("fp64-rev", "fp32", "bf16-sr", "bf16-rn"):
            check("%s: %s weight roots NEVER equal fp64 (honest negative)" % (task, impl),
                  e[impl]["weight_root_equal"] == 0 and e[impl]["trace_equal"] == 0,
                  e[impl]["weight_root_equal"])
            check("%s: %s diverges in epoch 0" % (task, impl), e[impl]["diverge_epoch_first"] == 0)
            check("%s: %s step refused by B7 on every seed and device" % (task, impl),
                  all(t["e4"][d]["step"][impl]["certified"] == 0 for d in N.DEVICES))
        check("%s: fp64-rev differs only at rounding scale (max |df| < 1e-12)" % task,
              e["fp64-rev"]["max_abs_pred_diff"] < 1e-12, e["fp64-rev"]["max_abs_pred_diff"])
        check("%s: fp32 function within EPS on all seeds" % task,
              e["fp32"]["seeds_within_eps"] == S, e["fp32"]["max_abs_pred_diff"])
        check("%s: bf16 routes exceed EPS on some seed" % task,
              e["bf16-sr"]["seeds_within_eps"] < S and e["bf16-rn"]["seeds_within_eps"] < S,
              (e["bf16-sr"]["seeds_within_eps"], e["bf16-rn"]["seeds_within_eps"]))
        check("%s: bf16 swallows >10%% of updates, fp32 <0.1%%" % task,
              e["bf16-rn"]["swallowed_update_share"] > 0.1 and e["fp32"]["swallowed_update_share"] < 1e-3,
              (e["bf16-rn"]["swallowed_update_share"], e["fp32"]["swallowed_update_share"]))
        # the constructive result
        check("%s: fsum-rev == fsum, every epoch, every seed (loss+weights)" % task,
              e["fsum-rev"]["trace_equal"] == S and e["fsum-rev"]["diverge_epoch_first"] is None)
        check("%s: fsum step CERTIFIED by B7 on every seed, both devices" % task,
              all(t["e4"][d]["step"]["fsum-rev"]["certified"] == S for d in N.DEVICES))
        check("%s: fsum trajectory != plain fp64 trajectory (canon is a choice)" % task,
              e["fsum_vs_fp64_trace_equal"] == 0)
        check("%s: fsum costs more declared flops than fp64" % task,
              t["step_cost"]["fsum"]["flops"] > t["step_cost"]["fp64"]["flops"])
        check("%s: exact float predictions refused for every non-canonical route" % task,
              all(t["e4"]["edge"]["preds"][i]["certified"] == 0
                  for i in ("fp64-rev", "fp32", "bf16-sr", "bf16-rn")))
        # the witness
        for impl in ("fp64-rev", "fp32", "fsum-rev"):
            w = t["e3"][impl]
            check("%s: %s route WITNESSED within EPS (stop_t=%s)" % (task, impl, w["per_route"]["stop_t"]),
                  w["per_route"]["state"] == "WITNESSED" and w["per_function"]["witnessed"] == S)
        for impl in ("bf16-sr", "bf16-rn"):
            check("%s: %s route NOT witnessed (flagged)" % (task, impl),
                  t["e3"][impl]["per_route"]["state"] == "NOT_WITNESSED",
                  t["e3"][impl]["per_route"]["misses"])
            check("%s: %s quality NOT witnessed either" % (task, impl),
                  t["quality"][impl]["witness"] == "NOT_WITNESSED", t["quality"][impl]["seeds_failing"])
        check("%s: fp32 quality witnessed" % task, t["quality"]["fp32"]["witness"] == "WITNESSED")
    c = rp["tasks"]["circle"]
    check("circle: fp32 labels certified 40/40 and dominate fp64 (faster-cheaper)",
          c["e4"]["edge"]["labels"]["fp32"] == {**c["e4"]["edge"]["labels"]["fp32"], "certified": S}
          and c["e4"]["edge"]["labels"]["fp32"]["classes"].get("dominates-faster-cheaper") == S)
    check("circle: bf16 labels certified on a minority of seeds only",
          0 < c["e4"]["edge"]["labels"]["bf16-sr"]["certified"] < S // 2,
          c["e4"]["edge"]["labels"]["bf16-sr"]["certified"])
    check("circle: B4 prefers fp32 over fp64 on both devices",
          all(c["b4_certified_pair"][d]["preferred_when"]["fast"] == "fp32" for d in N.DEVICES))
    check("sine: nothing but the canonical step is certifiable (B4 all-routes refused)",
          all(rp["tasks"]["sine"]["b4"][d].get("status") == "refused" for d in N.DEVICES))
    check("verdicts: fsum-rev priceable at the step; fp32 bounded (sine) / priceable at labels (circle)",
          rp["tasks"]["sine"]["verdict"]["fsum-rev"]["verdict"].startswith("priceable at the step")
          and rp["tasks"]["sine"]["verdict"]["fp32"]["verdict"] == "bounded"
          and rp["tasks"]["circle"]["verdict"]["fp32"]["verdict"] == "priceable at the product boundary")

    print("== route_witness (the general tool)")
    ret = rp["retraction"]
    check("retraction: witnessed at the switch, RETRACTED after regression",
          ret["state_at_switch"] == "WITNESSED" and ret["state"] == "RETRACTED", ret["E_final"])
    for nv in rp["null_validity"]:
        check("null validity p=p0=%s: false-witness rate %.4f <= delta" % (nv["p0"], nv["rate"]),
              nv["rate"] <= R.DELTA)
    check("price of evidence: 40 clean runs for p0=0.1, 421 clean points for p0=0.01",
          rp["prereg"]["clean_needed_seed"] == 40 and rp["prereg"]["clean_needed_point"] == 421)
    try:
        W.witness([0.0] * 5, None, 0.05)
        check("refuses without a pre-registered p0", False)
    except ValueError:
        check("refuses without a pre-registered p0", True)
    check("upper bound is monotone: more clean evidence -> tighter bound",
          W.upper_bound([0.0] * 400, 0.05) > W.upper_bound([0.0] * 4000, 0.05))

    print("priced-training selftest: %d checks, %d failures" % (len(CHECKS), len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
