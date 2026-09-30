"""priced_training — can a training STEP be priced like a forward route, or only bounded?

Runs the experiment end to end and prints the report. Four questions, in order:

  E1  the honest negative: does the loss digest (the step's product) agree across update
      impls? (xruntime-conformance found: forward digests 23/23 agree, loss digest does not)
  E2  the deeper question: is the LEARNED FUNCTION identical — exact float predictions, or
      decisions (labels) — on a held-out set, even when the loss digest differs?
  E3  the anytime-valid bound (route_witness): "the cheap route stays within EPS of the
      reference", per function (streamed held-out points) and per route (across seeds),
      with a retraction control and a null-validity control
  E4  System-2: B7 (system2-backtest) gates each (reference, cheap) pair at three product
      levels; B4 (route-preference) prices whatever the gate certifies, on two devices

Everything is computed here, from pre-registered constants (prereg.py). Modeled wall times
come from the declared rooflines in nettrain.DEVICES; Python wall time is a sidecar only.

CLI:  python3 priced_training.py [--json]
"""

from __future__ import annotations

import json
import sys
import time

import nettrain as N
import prereg as R
import route_witness as W

import activeledger as al  # noqa: E402  (path set by nettrain)
import backtest as bt  # noqa: E402
import route_preference as rp  # noqa: E402

REF = "fp64"
CHEAP = ("fp64-rev", "fp32", "bf16-sr", "bf16-rn", "fsum-rev")
# fsum-rev is compared against its own canonical reference (fsum), not fp64: the question for
# it is "is the correctly-rounded step order-invariant?". Every other route is vs fp64.
REF_OF = {i: REF for i in CHEAP} | {"fsum-rev": "fsum"}
SEEDS = tuple(range(1, R.N_SEEDS + 1))
STREAM_SEED = 0x57AE

_RUNS: dict = {}
_PRED: dict = {}


def run(task, impl, seed):
    key = (task, impl, seed)
    if key not in _RUNS:
        _RUNS[key] = N.train(task, impl, seed)
    return _RUNS[key]


def preds(task, impl, seed, n=None):
    """Cached held-out (n=None) or streamed (n=N_STREAM) predictions."""
    key = (task, impl, seed, n)
    if key not in _PRED:
        xs = N.heldout(task, R.N_HELDOUT) if n is None else N.sample_points(task, n, STREAM_SEED)
        _PRED[key] = N.predict(task, run(task, impl, seed)["weights"], xs)
    return _PRED[key]


def diverge_epoch(a, b):
    """First epoch whose loss digest or weight root differs (the step's 'product horizon'); None if never."""
    for ea, eb in zip(a["chain"], b["chain"]):
        if ea["loss_sha"] != eb["loss_sha"] or ea["weight_root_sha"] != eb["weight_root_sha"]:
            return ea["epoch"]
    return None


def fails(task, pa, pb):
    """Held-out verdict for one learned function vs the reference."""
    d = [abs(x - y) for x, y in zip(pa, pb)]
    out = {"max_abs": max(d), "mean_abs": sum(d) / len(d),
           "over_eps": sum(1 for v in d if v > R.EPS[task])}
    if N.TASKS[task]["out"] == "sigmoid":
        out["flips"] = sum(1 for x, y in zip(N.labels(pa), N.labels(pb)) if x != y)
    out["fail"] = out["over_eps"] > 0 or out.get("flips", 0) > 0
    return out


# ---- E1 + E2 ---------------------------------------------------------------------------

def e1_e2(task):
    rows = {}
    for impl in CHEAP:
        ref = REF_OF[impl]
        same_loss = same_root = same_trace = 0
        horizons, maxd, flips, fail_seeds, swallowed = [], [], [], 0, 0.0
        for s in SEEDS:
            a, b = run(task, ref, s), run(task, impl, s)
            same_loss += a["chain"][-1]["loss_sha"] == b["chain"][-1]["loss_sha"]
            same_root += N.weight_root(a["weights"], "f64") == N.weight_root(b["weights"], "f64")
            same_trace += N.step_trace(a) == N.step_trace(b)
            h = diverge_epoch(a, b)
            horizons.append(h)
            f = fails(task, preds(task, impl, s), preds(task, ref, s))
            maxd.append(f["max_abs"])
            flips.append(f.get("flips", 0))
            fail_seeds += f["fail"]
            swallowed += b["swallowed"] / b["updates"]
        hs = [h for h in horizons if h is not None]
        rows[impl] = {
            "ref": ref, "seeds": len(SEEDS), "loss_digest_equal": same_loss,
            "weight_root_equal": same_root, "trace_equal": same_trace,
            "diverge_epoch_first": min(hs) if hs else None, "diverge_epoch_max": max(hs) if hs else None,
            "max_abs_pred_diff": max(maxd), "median_max_abs": sorted(maxd)[len(maxd) // 2],
            "seeds_within_eps": sum(1 for v in maxd if v <= R.EPS[task]),
            "label_flips_total": sum(flips) if N.TASKS[task]["out"] == "sigmoid" else None,
            "seeds_label_identical": (sum(1 for v in flips if v == 0)
                                      if N.TASKS[task]["out"] == "sigmoid" else None),
            "seeds_failing": fail_seeds,
            "swallowed_update_share": round(swallowed / len(SEEDS), 6),
            "final_loss_mean": sum(run(task, impl, s)["final_loss"] for s in SEEDS) / len(SEEDS),
        }
    for r in (REF, "fsum"):
        rows[r] = {"final_loss_mean": sum(run(task, r, s)["final_loss"] for s in SEEDS) / len(SEEDS),
                   "swallowed_update_share": 0.0}
    rows["fsum_vs_fp64_trace_equal"] = sum(N.step_trace(run(task, "fsum", s)) ==
                                           N.step_trace(run(task, REF, s)) for s in SEEDS)
    return rows


# ---- quality: the explicit SECOND relation (prereg amendment 1) -------------------------

def quality_fail(task, impl, seed):
    xs = N.heldout(task, R.N_HELDOUT)
    truth = [N.target(task, x) for x in xs]
    ref = REF_OF[impl]
    pa, pr = preds(task, impl, seed), preds(task, ref, seed)
    kind, tol = R.QUALITY[task]
    if kind == "acc_drop":
        acc = lambda p: sum(1 for l, y in zip(N.labels(p), truth) if l == y) / len(p)  # noqa: E731
        return acc(pr) - acc(pa) > tol, acc(pa), acc(pr)
    mse = lambda p: sum((v - y) ** 2 for v, y in zip(p, truth)) / len(p)  # noqa: E731
    return mse(pa) > tol * mse(pr), mse(pa), mse(pr)


def quality(task):
    out = {}
    for impl in CHEAP:
        rs = [quality_fail(task, impl, s) for s in SEEDS]
        xs = [1.0 if f else 0.0 for f, _, _ in rs]
        w = W.witness(xs, R.P0_SEED, R.DELTA, R.BET_GRID)
        out[impl] = {"metric": R.QUALITY[task][0], "cheap_mean": sum(a for _, a, _ in rs) / len(rs),
                     "ref_mean": sum(b for _, _, b in rs) / len(rs), "seeds_failing": int(sum(xs)),
                     "witness": w["state"], "stop_t": w["stop_t"], "E_final": w["E_final"],
                     "ucb": W.upper_bound(xs, R.DELTA, bets=R.BET_GRID)}
    return out


def reference_determinism(task):
    """Control: the reference route retrained from scratch reproduces its own chain."""
    a = N.train(task, REF, SEEDS[0])
    b = run(task, REF, SEEDS[0])
    return a["tip"] == b["tip"] and N.verify_chain(a["chain"])


# ---- E3: the witness -------------------------------------------------------------------

def point_stream(task, impl, seed):
    pa, pb = preds(task, REF_OF[impl], seed, R.N_STREAM), preds(task, impl, seed, R.N_STREAM)
    out = []
    for x, y in zip(pa, pb):
        miss = abs(x - y) > R.EPS[task]
        if N.TASKS[task]["out"] == "sigmoid":
            miss = miss or ((x >= 0.5) != (y >= 0.5))
        out.append(1.0 if miss else 0.0)
    return out


def e3(task):
    out = {}
    for impl in CHEAP:
        per_fn = [W.witness(point_stream(task, impl, s), R.P0_POINT, R.DELTA, R.BET_GRID)
                  for s in SEEDS]
        seed_x = [1.0 if fails(task, preds(task, impl, s), preds(task, REF_OF[impl], s))["fail"]
                  else 0.0 for s in SEEDS]
        route = W.witness(seed_x, R.P0_SEED, R.DELTA, R.BET_GRID)
        out[impl] = {
            "per_function": {"witnessed": sum(1 for r in per_fn if r["state"] == "WITNESSED"),
                             "retracted": sum(1 for r in per_fn if r["state"] == "RETRACTED"),
                             "seeds": len(SEEDS),
                             "median_stop_t": _median([r["stop_t"] for r in per_fn if r["stop_t"] > 0]),
                             "total_misses": sum(r["misses"] for r in per_fn),
                             "worst_ucb": _worst_ucb(task, impl)},
            "per_route": {**route, "ucb": W.upper_bound(seed_x, R.DELTA, bets=R.BET_GRID)},
        }
    return out


def _median(v):
    return sorted(v)[len(v) // 2] if v else None


def _worst_ucb(task, impl):
    """Largest per-function anytime upper bound on the miss rate across seeds (None = unbounded)."""
    worst = 0.0
    for s in SEEDS:
        u = W.upper_bound(point_stream(task, impl, s), R.DELTA, bets=R.BET_GRID)
        if u is None:
            return None
        worst = max(worst, u)
    return worst


def retraction_control(task, good, bad):
    """A route that is clean for N_SEEDS runs, then regresses (e.g. a kernel swap mid-life):
    the witness must fire on the clean half and RETRACT on the bad half."""
    def x(impl, s):
        return 1.0 if fails(task, preds(task, impl, s), preds(task, REF, s))["fail"] else 0.0
    stream = [x(good, s) for s in SEEDS] + [x(bad, s) for s in SEEDS]
    w = W.RouteWitness(R.P0_SEED, R.DELTA, R.BET_GRID)
    at_switch = None
    for i, v in enumerate(stream):
        w.observe(v)
        if i == len(SEEDS) - 1:
            at_switch = w.state
    return {"good": good, "bad": bad, "state_at_switch": at_switch, **w.summary()}


def null_control():
    return [W.null_false_witness_rate(R.P0_SEED, R.P0_SEED, R.DELTA, 2000, 200, seed=11,
                                      bets=R.BET_GRID),
            W.null_false_witness_rate(R.P0_POINT, R.P0_POINT, R.DELTA, 400, R.N_STREAM, seed=13,
                                      bets=R.BET_GRID)]


# ---- E4: System-2 ----------------------------------------------------------------------

def e4(task, device):
    xs = N.heldout(task, R.N_HELDOUT)
    levels = ["step", "preds"] + (["labels"] if N.TASKS[task]["out"] == "sigmoid" else [])
    out = {}
    for level in levels:
        per = {}
        for impl in CHEAP:
            cert, classes, acc = 0, {}, {impl: []}
            for s in SEEDS:
                ref = REF_OF[impl]
                ra = N.to_activelog(run(task, ref, s), level, xs, device)
                rb = N.to_activelog(run(task, impl, s), level, xs, device)
                v = bt.backtest_pair(ra, rb)
                if v["status"] == "certified":
                    cert += 1
                    classes[v["class"]] = classes.get(v["class"], 0) + 1
                    acc.setdefault(ref, []).append(v["routes"][ref])
                    acc[impl].append(v["routes"][impl])
            row = {"certified": cert, "refused": len(SEEDS) - cert, "classes": classes}
            if cert:
                row["workload"] = {n: bt._sum_axes(acc[n]) for n in acc if acc[n]}
            per[impl] = row
        out[level] = per
    return out


def b4_frontier(task, device, level):
    """B4 over the reference + every cheap route, on the seeds where ALL of them are certified
    (B4 needs one shared product across all routes)."""
    xs = N.heldout(task, R.N_HELDOUT)
    names = (REF,) + tuple(i for i in CHEAP if REF_OF[i] == REF)
    axes, used = {n: [] for n in names}, 0
    for s in SEEDS:
        recs = [(n, N.to_activelog(run(task, n, s), level, xs, device)) for n in names]
        # drop any route refused against the reference, then B4's own gate runs on the rest
        keep = [recs[0]] + [r for r in recs[1:]
                            if bt.backtest_pair(recs[0][1], r[1])["status"] == "certified"]
        if len(keep) < len(names):
            continue
        res = rp.prefer(keep)
        if res["status"] != "certified":
            continue
        used += 1
        for n in names:
            axes[n].append(res["routes"][n])
    if not used:
        return {"seeds_all_certified": 0, "status": "refused"}
    wl = rp.prefer_axes({n: bt._sum_axes(axes[n]) for n in names})
    return {"seeds_all_certified": used, "frontier": wl["frontier"], "class": wl["class"],
            "preferred_when": {k: wl["preferred_when"][k] for k in ("fast", "cheap")},
            "dominated": wl["dominated"]}


def b4_subset(task, device, level, routes):
    """B4 over a chosen subset, on the seeds where each is certified against the reference."""
    xs = N.heldout(task, R.N_HELDOUT)
    axes, used = {n: [] for n in routes}, 0
    for s in SEEDS:
        recs = [(n, N.to_activelog(run(task, n, s), level, xs, device)) for n in routes]
        res = rp.prefer(recs)
        if res["status"] != "certified":
            continue
        used += 1
        for n in routes:
            axes[n].append(res["routes"][n])
    if not used:
        return {"seeds_all_certified": 0, "status": "refused"}
    wl = rp.prefer_axes({n: bt._sum_axes(axes[n]) for n in routes})
    return {"seeds_all_certified": used, "frontier": wl["frontier"], "class": wl["class"],
            "preferred_when": {k: wl["preferred_when"][k] for k in ("fast", "cheap")}}


def python_wall(task):
    """Sidecar: best-of-3 Python wall ms for one training run per impl. Never logged."""
    out = {}
    for impl in (REF, "fsum") + CHEAP:
        best = None
        for _ in range(3):
            t = time.perf_counter()
            N.train(task, impl, SEEDS[0])
            ms = (time.perf_counter() - t) * 1000
            best = ms if best is None else min(best, ms)
        out[impl] = round(best, 1)
    return out


# ---- verdict ---------------------------------------------------------------------------

def verdict(task, e12, e3r, e4r):
    """Per cheap route: priceable (B7 certified on every seed at the task's product boundary),
    priceable-where-certified (some seeds), bounded (witness live, no exact product), or
    flagged (neither)."""
    boundary = "labels" if N.TASKS[task]["out"] == "sigmoid" else "preds"
    out = {}
    for impl in CHEAP:
        cert = e4r["edge"][boundary][impl]["certified"]
        wit = e3r[impl]["per_route"]["state"] == "WITNESSED"
        step = e4r["edge"]["step"][impl]["certified"]
        if step == len(SEEDS):
            v = "priceable at the step (byte-identical trajectory)"
        elif cert == len(SEEDS):
            v = "priceable at the product boundary"
        elif cert and wit:
            v = "priceable-where-certified + bounded"
        elif cert:
            v = "priceable-where-certified, route unbounded (flagged)"
        elif wit:
            v = "bounded"
        else:
            v = "flagged"
        out[impl] = {"step_certified": step, "boundary": boundary, "boundary_certified": cert,
                     "route_witness": e3r[impl]["per_route"]["state"], "verdict": v}
    return out


def report() -> dict:
    rep = {"prereg": {"EPS": R.EPS, "P0_POINT": R.P0_POINT, "P0_SEED": R.P0_SEED,
                      "DELTA": R.DELTA, "BET_GRID": list(R.BET_GRID), "N_SEEDS": R.N_SEEDS,
                      "N_STREAM": R.N_STREAM, "N_HELDOUT": R.N_HELDOUT,
                      "clean_needed_point": W.clean_needed(R.P0_POINT, R.DELTA, R.BET_GRID),
                      "clean_needed_seed": W.clean_needed(R.P0_SEED, R.DELTA, R.BET_GRID)},
           "tasks": {}}
    for task in N.TASKS:
        e12 = e1_e2(task)
        e3r = e3(task)
        e4r = {d: e4(task, d) for d in N.DEVICES}
        bnd = "labels" if N.TASKS[task]["out"] == "sigmoid" else "preds"
        rep["tasks"][task] = {
            "config": N.TASKS[task], "params": N.n_params(task),
            "ref_deterministic": reference_determinism(task),
            "e1_e2": e12, "e3": e3r, "e4": e4r,
            "b4": {d: b4_frontier(task, d, bnd) for d in N.DEVICES},
            "verdict": verdict(task, e12, e3r, e4r),
            "step_cost": {i: N.step_cost(task, i) for i in (REF, "fsum") + CHEAP},
            "quality": quality(task),
            "python_wall_ms": python_wall(task),
        }
    rep["tasks"]["circle"]["b4_certified_pair"] = {
        d: b4_subset("circle", d, "labels", (REF, "fp32", "fp64-rev")) for d in N.DEVICES}
    rep["fsum_step_b4"] = {d: b4_subset("sine", d, "step", ("fsum", "fsum-rev")) for d in N.DEVICES}
    rep["fsum_vs_fp64_b7"] = {}
    for d in N.DEVICES:
        xs = N.heldout("sine", R.N_HELDOUT)
        v = bt.backtest_pair(N.to_activelog(run("sine", REF, 1), "preds", xs, d),
                             N.to_activelog(run("sine", "fsum", 1), "preds", xs, d))
        rep["fsum_vs_fp64_b7"][d] = v["status"]
    rep["retraction"] = retraction_control("circle", "fp32", "bf16-sr")
    rep["null_validity"] = null_control()
    return rep


def _fmt(rep) -> str:
    L = []
    p = rep["prereg"]
    L.append("prereg: EPS=%s  P0_POINT=%s  P0_SEED=%s  DELTA=%s  seeds=%d  (clean obs to cross: "
             "point %d, seed %d)" % (p["EPS"], p["P0_POINT"], p["P0_SEED"], p["DELTA"], p["N_SEEDS"],
                                     p["clean_needed_point"], p["clean_needed_seed"]))
    for task, t in rep["tasks"].items():
        L.append("")
        L.append("=== %s  (%d params, %s)  reference deterministic: %s" %
                 (task, t["params"], {k: t["config"][k] for k in ("hidden", "batch", "epochs", "lr")},
                  t["ref_deterministic"]))
        L.append("E1/E2  vs fp64 over %d seeds" % len(SEEDS))
        L.append("   impl       vs     loss=  root=  trace= div@ep  max|df|     med max|df|  <=eps  lbl=   flips  swallow  final_loss")
        for impl in CHEAP:
            r = t["e1_e2"][impl]
            L.append("   %-9s  %-5s  %3d    %3d    %3d    %-6s  %.3e   %.3e    %3d    %-5s  %-5s  %.2e  %.3e" % (
                impl, r["ref"], r["loss_digest_equal"], r["weight_root_equal"], r["trace_equal"],
                r["diverge_epoch_first"],
                r["max_abs_pred_diff"], r["median_max_abs"], r["seeds_within_eps"],
                r["seeds_label_identical"] if r["seeds_label_identical"] is not None else "-",
                r["label_flips_total"] if r["label_flips_total"] is not None else "-",
                r["swallowed_update_share"], r["final_loss_mean"]))
        L.append("   fp64 final_loss mean %.3e   fsum final_loss mean %.3e   fsum trace == fp64 trace: %d/%d"
                 % (t["e1_e2"][REF]["final_loss_mean"], t["e1_e2"]["fsum"]["final_loss_mean"],
                    t["e1_e2"]["fsum_vs_fp64_trace_equal"], len(SEEDS)))
        L.append("E3  witness (per function: %d streamed points, p0=%s; per route: seeds, p0=%s)" %
                 (p["N_STREAM"], p["P0_POINT"], p["P0_SEED"]))
        for impl in CHEAP:
            f, r = t["e3"][impl]["per_function"], t["e3"][impl]["per_route"]
            L.append("   %-9s  functions witnessed %2d/%d (retracted %d, misses %d, worst ucb %s)   "
                     "route: %s stop_t=%s misses=%d E=%.3g ucb=%s" % (
                         impl, f["witnessed"], f["seeds"], f["retracted"], f["total_misses"],
                         f["worst_ucb"], r["state"], r["stop_t"], r["misses"], r["E_final"], r["ucb"]))
        for d in N.DEVICES:
            L.append("E4  B7 on %s:" % d)
            for level, per in t["e4"][d].items():
                L.append("   level=%-6s " % level + "  ".join(
                    "%s %d/%d%s" % (i, per[i]["certified"], len(SEEDS),
                                    (" " + ",".join("%s:%d" % kv for kv in per[i]["classes"].items()))
                                    if per[i]["classes"] else "") for i in CHEAP))
            b = t["b4"][d]
            L.append("   B4 all-routes: %s" % json.dumps(b))
        if "b4_certified_pair" in t:
            for d, b in t["b4_certified_pair"].items():
                L.append("   B4 fp64 vs fp32 (%s): %s" % (d, json.dumps(b)))
        L.append("quality (explicit second relation, prereg amendment 1; per-seed fail -> route witness p0=%s)"
                 % p["P0_SEED"])
        for impl, q in t["quality"].items():
            L.append("   %-9s  %s cheap %.4g vs ref %.4g   seeds failing %d   witness %s stop_t=%s ucb=%s" % (
                impl, q["metric"], q["cheap_mean"], q["ref_mean"], q["seeds_failing"], q["witness"],
                q["stop_t"], q["ucb"]))
        L.append("verdict:")
        for impl, v in t["verdict"].items():
            L.append("   %-9s  step %d/%d   %s %d/%d   witness %-13s -> %s" % (
                impl, v["step_certified"], len(SEEDS), v["boundary"], v["boundary_certified"],
                len(SEEDS), v["route_witness"], v["verdict"]))
        L.append("cost (declared, per step): " + "  ".join(
            "%s %dF/%dB" % (i, c["flops"], c["bytes"]) for i, c in t["step_cost"].items()))
        L.append("python wall ms (best of 3, sidecar): " + "  ".join(
            "%s %.1f" % kv for kv in t["python_wall_ms"].items()))
    L.append("")
    L.append("fsum (canonical step) vs fsum-rev, sine, B4 at level=step: " + json.dumps(rep["fsum_step_b4"]))
    L.append("fsum vs fp64 (sine seed 1, level=preds) B7: " + json.dumps(rep["fsum_vs_fp64_b7"]))
    r = rep["retraction"]
    L.append("retraction control (circle, %s x%d then %s x%d): at switch %s -> final %s "
             "(stop_t=%d, E_max=%.3g, E_final=%.3g)" % (r["good"], len(SEEDS), r["bad"], len(SEEDS),
                                                        r["state_at_switch"], r["state"], r["stop_t"],
                                                        r["E_max"], r["E_final"]))
    for nv in rep["null_validity"]:
        L.append("null validity: Bernoulli(p=%s) vs p0=%s, %d streams x %d: fired %d (rate %.4f, "
                 "Ville bound %s)" % (nv["p"], nv["p0"], nv["streams"], nv["length"], nv["fired"],
                                      nv["rate"], nv["delta"]))
    return "\n".join(L)


if __name__ == "__main__":
    rep = report()
    print(json.dumps(rep, indent=1, default=str) if "--json" in sys.argv else _fmt(rep))
