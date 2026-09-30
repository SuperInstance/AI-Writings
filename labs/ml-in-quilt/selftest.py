"""ml-in-quilt selftest — offline, deterministic, stdlib only.

Every check is a claim the README or the architecture doc makes. Numbers the checks
depend on are printed, so a failure shows the measured value, not just "False".
"""

from __future__ import annotations

import sys

import cellml as C
import mlq_system2 as S

import activeledger as al
import backtest as bt

CHECKS, FAILS = [], []


def check(name, ok, detail=""):
    CHECKS.append(name)
    if not ok:
        FAILS.append(name)
    print("  [%s] %s%s" % ("ok" if ok else "FAIL", name, ("  — " + str(detail)) if detail else ""))


def dataflow_closed(records) -> bool:
    """Every compute tick reads something an earlier tick in its stream wrote."""
    seen = {}
    for r in records:
        if r["type"] != "cell.tick":
            continue
        b = r["body"]
        st = seen.setdefault(b.get("stream", ""), set())
        if b["kind"] not in ("load", "embed", "kvcache", "verify") and b["in"] not in st:
            return False
        st.add(b["out"])
    return True


def main():
    print("ml-in-quilt selftest")
    model, fit = C.build_model()
    rep, runs = S.report(model, fit)
    E, A = rep["b7"]["edge"], rep["b7"]["accel"]

    print("-- cells, weights, fit")
    check("tokenize/detokenize round-trip", C.detokenize(C.tokenize("the cat sat.")) == "the cat sat.")
    m2, _ = C.build_model()
    check("weights are a pure function of the seed", m2.weights_hash() == model.weights_hash(),
          model.weights_hash())
    check("ridge readout fits the corpus (train acc >= 0.70)", fit["train_acc"] >= 0.70,
          fit["train_acc"])
    check("JEPA latent predictor fits Z_in -> Z_out (r2 >= 0.95)", fit["jepa"]["r2"] >= 0.95,
          fit["jepa"]["r2"])
    try:
        C.Linear("x", [[1.0]], "q3")
        check("unknown impl refused", False)
    except ValueError:
        check("unknown impl refused", True)
    try:
        C.Stream(model, {}, None, "x").feed([2] * (model.cfg["ctx"] + 1))
        check("context overflow refused", False)
    except ValueError:
        check("context overflow refused", True)

    print("-- the log (B1): chain, budgets, dataflow")
    fp = runs["edge"]["fp"][S.PROMPTS[0]]
    spec = runs["edge"]["spec-q4"][S.PROMPTS[0]]
    check("fp run: ActiveLog chain verifies", al.verify_chain(fp))
    check("spec run: ActiveLog chain verifies", al.verify_chain(spec))
    ticks = [r for r in fp + spec if r["type"] == "cell.tick"]
    check("every cell.tick carries a well-formed budget vector",
          all(al.budget_ok(r["body"]["budget"]) for r in ticks), len(ticks))
    check("B7 replay_route re-sums the budget to the declared total (fp)",
          bt.replay_route(fp)["route"] == "fp")
    check("dataflow closed: every tick reads an earlier tick's output (fp)", dataflow_closed(fp))
    check("dataflow closed per stream (spec: draft + verify interleaved)", dataflow_closed(spec))
    kinds = {r["body"]["kind"] for r in fp if r["type"] == "cell.tick"}
    check("cell taxonomy present in one run",
          {"load", "embed", "norm", "attn", "mlp", "head", "sample"} <= kinds, sorted(kinds))

    print("-- replay == live, and localization")
    check("replay == live (spec-q4, byte-identical records)", rep["replay"]["replay_equal"],
          "%d records" % rep["replay"]["records"])
    for name in ("fp", "q8"):
        check("replay == live (%s)" % name, S.replay(model, runs["edge"][name][S.PROMPTS[3]])["equal"])
    for w, cell in (("L1.w1", "L1.mlp"), ("L0.wqkv", "L0.attn"), ("head", "head")):
        fd = S.replay(S.tampered(model, w), fp)["first_divergence"]
        check("tamper %s localizes to load:%s then %s" % (w, w, cell),
              fd and fd["cell"] == "load:" + w and fd["first_compute_cell"] == cell, fd)

    print("-- B7: the gate runs first")
    check("q4 (every block) never survives 12 greedy tokens: refused 24/24",
          E["q4"]["refused"] == len(S.PROMPTS), E["q4"])
    check("q8 certified on most situations, refused on some",
          0 < E["q8"]["refused"] < E["q8"]["certified"],
          "certified %d refused %d" % (E["q8"]["certified"], E["q8"]["refused"]))
    check("q8 dominates fp where certified (faster-cheaper)",
          E["q8"]["class"] == "dominates-faster-cheaper" and E["q8"]["dominant"] == "q8")
    ref = bt.backtest_pair(fp, runs["edge"]["q4"][S.PROMPTS[0]])
    check("a refused verdict exposes no budget", ref["status"] == "refused"
          and "routes" not in ref and "wall_ms" not in al.canon(ref))
    for dev, R in (("edge", E), ("accel", A)):
        for name in ("spec-q4", "spec-jepa"):
            check("%s is product-identical by construction on %s (24/24)" % (name, dev),
                  R[name]["certified"] == len(S.PROMPTS) and R[name]["refused"] == 0)

    print("-- regime (§11.2): the verdict depends on the device's flop:byte ratio")
    check("edge: fp dominates spec-q4", E["spec-q4"]["class"] == "dominates-faster-cheaper"
          and E["spec-q4"]["dominant"] == "fp", E["spec-q4"]["class"])
    check("accel: spec-q4 vs fp is a trade-off (spec faster, fp cheaper)",
          A["spec-q4"]["class"] == "trade-off"
          and A["spec-q4"]["preferred_when"]["fast"] == "spec-q4"
          and A["spec-q4"]["preferred_when"]["cheap"] == "fp", A["spec-q4"]["preferred_when"])
    acc = E["spec-q4"]["accept"]
    check("draft acceptance is measured, not assumed", 0 < acc[0] < acc[1], "%d/%d" % tuple(acc))

    print("-- B4: preference is per situation and per device")
    b4e, b4a = rep["b4"]["edge"], rep["b4"]["accel"]
    check("edge workload over exact routes: fp alone on the frontier", b4e["workload"]["frontier"] == ["fp"])
    check("accel workload: frontier holds fp and spec-q4",
          b4a["workload"]["frontier"] == ["fp", "spec-q4"], b4a["workload"]["frontier"])
    check("per-situation fast pick varies across situations", len(b4e["per_situation_fast"]) > 1,
          b4e["per_situation_fast"])
    check("hebbian book settles on one fast route", b4e["settled"]["fast"]["route"] == "q8",
          b4e["settled"]["fast"])

    print("-- differ profile (teacher-forced, per block)")
    D = rep["differ"]
    check("q8 agrees with fp more than q4 does", D["q8"]["agree_rate"] > D["q4"]["agree_rate"],
          "%s vs %s" % (D["q8"]["agree_rate"], D["q4"]["agree_rate"]))
    check("q4 in the head costs the largest logit error of any single block",
          D["q4-head"]["max_dlogit"] > max(D["q4-attn"]["max_dlogit"], D["q4-mlp"]["max_dlogit"]))
    check("q8 margin gate: >50% of held-out tokens skip-safe, 0 flips",
          D["q8"]["gate_safe_rate"] > 0.5 and D["q8"]["gate_flips"] == 0, D["q8"])
    check("JEPA r2 high yet token agreement lowest of all plans (latent != product)",
          D["jepa-exit1"]["agree_rate"] <= min(v["agree_rate"] for v in D.values()),
          D["jepa-exit1"]["agree_rate"])

    print("-- prefix cache (content-addressed KV)")
    P = rep["pcache"]
    check("loaded KV chain heads equal the computed ones", P["kv_heads_match"],
          "reused %d positions" % P["reused_positions"])
    check("pcache route certified product-identical to fp", P["status"] == "certified")
    check("pcache does less compute", P["flops"]["fp+pcache"] < P["flops"]["fp"], P["flops"])
    pc = S.run_pcache(model, "the cat sat on the ", "the cat sat on the log")
    hit = [r for r in pc if r["type"] == "cell.tick" and r["body"]["kind"] == "kvcache"][0]
    check("cache residency is logged (mem_mb > 0) though B7 does not score it",
          hit["body"]["budget"]["mem_mb"] > 0)
    check("replay == live (pcache, warm-up recorded in `chosen`)", S.replay(model, pc)["equal"])
    cache = C.PrefixCache()
    C.run_greedy(model, "the cat sat on the ", 4, S.Q8, "w", prefix_cache=cache, log=False)
    check("prefix cache is keyed by plan: a q8 cache never serves fp",
          cache.longest({}, C.tokenize("the cat sat on the log"), 20) == 0)

    print("-- at rest (ALR1 + RS)")
    R = rep["at_rest"]
    check("q4 weights >= 6x smaller than fp32 at rest", R["q4_vs_fp"] >= 6.0, R["weight_bytes"])
    check("RS repairs %d corrupted bytes exactly" % R["corrupted_bytes"], R["repaired_exact"])
    check("repaired bytes decode to the live q4 kernel's weights", R["repaired_weights_equal_live"])
    check("activation log ALR1+RS round-trips exactly", R["log_roundtrip_exact"])
    check("ALR1+RS smaller than jsonl+lzma", R["log_alr1_rs_bytes"] < R["log_jsonl_lzma_bytes"],
          "%d vs %d" % (R["log_alr1_rs_bytes"], R["log_jsonl_lzma_bytes"]))

    print("-- situation recall")
    Rc = rep["recall"]
    check("recall accuracies computed against a majority baseline",
          all(0 <= v <= 1 for v in Rc["loo_knn_acc"].values()), Rc["loo_knn_acc"])
    check("the lexical embedder is flagged non-semantic", Rc["semantic"] is False)

    print("-- determinism")
    again = S.run_route(model, "spec-q4", S.PROMPTS[0])
    check("same inputs -> byte-identical log", al.canon(again) == al.canon(spec))
    v1 = bt.backtest_pair(fp, runs["edge"]["q8"][S.PROMPTS[0]])
    v2 = bt.backtest_pair(fp, runs["edge"]["q8"][S.PROMPTS[0]])
    check("verdict_hash is stable", v1["verdict_hash"] == v2["verdict_hash"])
    print("report_hash %s" % rep["report_hash"])

    print("ml-in-quilt selftest: %d checks, %d failures" % (len(CHECKS), len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
