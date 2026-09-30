"""mlq_system2 — plug the cell-native forward pass into the fleet's mature systems.

    B1  activeledger      every run is an ActiveLog v1 slice (cell.tick ... ledger.transaction)
    B7  system2-backtest  fp vs each alternative route, product-identity gate FIRST
    B4  route-preference  frontier + preferred_when over the routes the gate lets through
    at_rest (ALR1+RS)     weights and activation logs at rest, repairable
    situation-memory      recall "have we seen a situation like this, which route held?"

Everything in the report is computed here, from the toy model, under a DECLARED cost model
(cellml.DEVICES). Nothing is a hardware measurement except `python_wall_ms`, which is a
sidecar and is never written into a log (wall-clock noise would break replay == live).

CLI:  python3 mlq_system2.py [--json]
"""

from __future__ import annotations

import copy
import json
import lzma
import math
import os
import sys
import time

import cellml as C

sys.path.insert(0, os.path.join(C.LABS, "situation-memory"))

import activeledger as al  # noqa: E402
import at_rest  # noqa: E402
import backtest as bt  # noqa: E402
import route_preference as rp  # noqa: E402

N_TOKENS = 12
Q8 = {"attn": "q8", "mlp": "q8", "head": "q8"}
Q4 = {"attn": "q4", "mlp": "q4", "head": "q4"}
JEPA = {"exit": 1}

# name -> (plan for greedy) or ("spec", draft, verify, k)
ROUTES = {
    "fp": {},
    "q8": Q8,
    "q4": Q4,
    "spec-q4": ("spec", Q4, {}, 4),
    "spec-jepa": ("spec", JEPA, {}, 4),
}

# Situations: corpus slices (in-distribution) + recombinations the corpus never contains.
PROMPTS = ["the cat ", "the dog s", "a cat and", "the rat ", "the dog ate", "on the m",
           "the frog", "a dog sat", "sat on the ", "the cat ate", "ate the r", "and a dog ",
           "the mat. ", "the log", "a frog sat", "the dog and", "rat ate the", "on a cat",
           "the cat and the", "dog sat on", "a rat", "the frog ate", "mat. the", "cat sat"]


def run_route(model, name, prompt, n=N_TOKENS):
    r = ROUTES[name]
    if isinstance(r, tuple):
        _, draft, verify, k = r
        return C.run_speculative(model, prompt, n, draft, verify, name, k=k).records
    return C.run_greedy(model, prompt, n, r, name).records


def run_pcache(model, warm: str, prompt: str, n=N_TOKENS, plan=None):
    """fp + content-addressed prefix cache warmed by an earlier situation."""
    plan = plan or {}
    pc = C.PrefixCache()
    C.run_greedy(model, warm, n, plan, "warm", prefix_cache=pc, log=False)
    lg = C.run_greedy(model, prompt, n, plan, "fp+pcache", prefix_cache=pc)
    tx = lg.records[-1]["body"]
    tx["chosen"]["warm"] = warm
    # re-seal: the transaction body changed after emit, so rebuild the last envelope
    recs = lg.records[:-1]
    out = al.ActiveLog(dev="ml-in-quilt")
    for r in recs:
        out.emit(r["type"], r["body"])
    out.emit("ledger.transaction", tx)
    return out.records


# ---- replay == live, and divergence localization --------------------------------------

def replay(model, records):
    """Re-execute a logged run from its transaction alone; compare record by record.
    Returns {"equal": bool, "first_divergence": None | {seq, cell, kind}}."""
    tx = records[-1]["body"]
    ch = tx["chosen"]
    dev = next(k for k, v in C.DEVICES.items() if v["name"] == ch["device"])
    saved = dict(C.DEVICE)
    C.use_device(dev)
    try:
        n = len(tx["tokens"])
        plan = ch["plan"]
        if "warm" in ch:
            again = run_pcache(model, ch["warm"], tx["prompt"], n, plan)
        elif "draft" in plan:
            again = C.run_speculative(model, tx["prompt"], n, plan["draft"], plan["verify"],
                                      tx["route"], k=ch["k"]).records
        else:
            again = C.run_greedy(model, tx["prompt"], n, plan, tx["route"]).records
    finally:
        C.DEVICE.clear()
        C.DEVICE.update(saved)
    # compare BODIES to localize: once one envelope differs, every later `prev` differs too
    for i, (a, b) in enumerate(zip(records, again)):
        if al.canon(a["body"]) != al.canon(b["body"]):
            body = a["body"]
            first_compute = next((r["body"]["cell"] for r, s in zip(records[i:], again[i:])
                                  if al.canon(r["body"]) != al.canon(s["body"])
                                  and r["body"].get("kind") not in ("load", None)), None)
            return {"equal": False, "first_divergence": {
                "seq": i, "cell": body.get("cell", "ledger.transaction"),
                "first_compute_cell": first_compute}}
    return {"equal": len(records) == len(again)
            and al.canon(records) == al.canon(again), "first_divergence": None}


def tampered(model, wname="L1.w1", delta=0.25):
    m2 = copy.deepcopy(model)
    m2.W[wname][0][0] = C.f32(m2.W[wname][0][0] + delta)
    m2._k = {}
    return m2


# ---- per-cell differ: teacher-forced token agreement + logit error ---------------------

def _logits(model, plan, ids):
    return C.Stream(model, plan, None, "probe").feed(ids)


def differ_profile(model, text=C.CORPUS):
    """For each alternative plan, feed the SAME tokens (teacher forcing) and compare to fp:
    argmax agreement per position, max/mean |dlogit|, and a calibrated margin gate:
    eps = max |dlogit| on the first half; on the second half, positions whose ALT margin
    exceeds 2*eps are 'safe to skip verify' — count them and any that still flipped."""
    ids = C.tokenize(text)
    win = [ids[s:s + model.cfg["ctx"]] for s in range(0, len(ids), model.cfg["ctx"])]
    ref = [row for w in win for row in _logits(model, {}, w)]
    half = len(ref) // 2
    plans = {"q8": Q8, "q4": Q4, "q4-attn": {"attn": "q4"}, "q4-mlp": {"mlp": "q4"},
             "q4-head": {"head": "q4"}, "jepa-exit1": JEPA}
    out = {}
    for name, plan in plans.items():
        alt = [row for w in win for row in _logits(model, plan, w)]
        agree = sum(C.argmax(a) == C.argmax(b) for a, b in zip(ref, alt))
        errs = [max(abs(x - y) for x, y in zip(a, b)) for a, b in zip(ref, alt)]
        eps = max(errs[:half])
        safe = flips = 0
        for a, b in zip(ref[half:], alt[half:]):
            srt = sorted(b, reverse=True)
            if srt[0] - srt[1] > 2 * eps:
                safe += 1
                flips += C.argmax(a) != C.argmax(b)
        out[name] = {"positions": len(ref), "agree": agree,
                     "agree_rate": round(agree / len(ref), 4),
                     "max_dlogit": round(max(errs), 4),
                     "mean_dlogit": round(sum(errs) / len(errs), 4),
                     "gate_eps": round(eps, 4), "gate_safe": safe,
                     "gate_safe_rate": round(safe / (len(ref) - half), 4), "gate_flips": flips}
    return out


# ---- B7: coverage + workload verdict per route, per device ----------------------------

def b7_matrix(model, devices=("edge", "accel"), prompts=PROMPTS):
    res, runs = {}, {}
    for dev in devices:
        C.use_device(dev)
        fp = {p: run_route(model, "fp", p) for p in prompts}
        runs[dev] = {"fp": fp}
        res[dev] = {}
        for name in ROUTES:
            if name == "fp":
                continue
            alt = {p: run_route(model, name, p) for p in prompts}
            runs[dev][name] = alt
            rep = bt.backtest_corpus([{"id": p, "a": fp[p], "b": alt[p]} for p in prompts],
                                     ("fp", name))
            res[dev][name] = {"certified": rep["certified"], "refused": rep["refused"],
                              "totals": rep.get("totals"),
                              "class": rep.get("workload", {}).get("class"),
                              "dominant": rep.get("workload", {}).get("dominant"),
                              "preferred_when": rep.get("workload", {}).get("preferred_when"),
                              "verdict_hash": rep["verdict_hash"]}
            if isinstance(ROUTES[name], tuple):
                acc = [alt[p][-1]["body"]["chosen"]["accept"] for p in prompts]
                res[dev][name]["accept"] = [sum(a for a, _ in acc), sum(b for _, b in acc)]
    C.use_device("edge")
    return res, runs


def b4_views(runs, dev, prompts=PROMPTS):
    """(1) workload B4 over the routes certified on EVERY situation, with standing =
    certified-rate x 1000 (robustness as `good`); (2) per-situation B4 over whichever
    routes the gate let through for that situation — the preferred route is a function
    of the situation, not a global constant."""
    R = runs[dev]
    cert = {n: [bt.backtest_pair(R["fp"][p], R[n][p])["status"] == "certified" for p in prompts]
            for n in R if n != "fp"}
    always = ["fp"] + sorted(n for n, c in cert.items() if all(c))
    axes = {}
    for n in always:
        tot = {"wall_ms": 0.0, "usd": 0.0, "tokens": 0, "storage_bytes": 0}
        for p in prompts:
            ax = bt.replay_route(R[n][p])["axes"]
            for k in tot:
                tot[k] = tot[k] + ax[k] if k != "storage_bytes" else max(tot[k], ax[k])
        tot["wall_ms"] = round(tot["wall_ms"], 6)
        axes[n] = tot
    workload = rp.prefer_axes(axes)
    per = {}
    book = rp.PreferenceBook()
    for i, p in enumerate(prompts):
        cands = [("fp", R["fp"][p])] + [(n, R[n][p]) for n in sorted(cert) if cert[n][i]]
        r = rp.prefer(cands)
        book.observe(r)
        per[p] = {"routes": [n for n, _ in cands], "fast": r["preferred_when"]["fast"],
                  "cheap": r["preferred_when"]["cheap"], "frontier": r["frontier"]}
    fast_counts = {}
    for v in per.values():
        fast_counts[v["fast"]] = fast_counts.get(v["fast"], 0) + 1
    return {"exact_routes": always, "workload": {k: workload[k] for k in
                                                 ("class", "frontier", "preferred_when")},
            "per_situation_fast": dict(sorted(fast_counts.items())),
            "settled": book.settled(), "per_situation": per,
            "cert_rate": {n: round(sum(c) / len(c), 4) for n, c in sorted(cert.items())}}


# ---- prefix cache: content-addressed KV ----------------------------------------------

def pcache_experiment(model, warm="the cat sat on the ", prompt="the cat sat on the log"):
    C.use_device("edge")
    a = run_route(model, "fp", prompt)
    b = run_pcache(model, warm, prompt)
    v = bt.backtest_pair(a, b)
    hit = next(r["body"] for r in b if r["type"] == "cell.tick" and r["body"]["kind"] == "kvcache")
    reuse = hit["pos"][1]
    # the loaded K/V chain head must equal the head the uncached run computed at that position
    kv_at = {}
    for r in a:
        bd = r["body"]
        if r["type"] == "cell.tick" and bd.get("kind") == "attn" and bd["pos"][0] == 0:
            kv_at[bd["cell"]] = bd
    heads_loaded = hit["out"].split(",")
    s = C.Stream(model, {}, None, "probe")
    s.feed(C.tokenize(prompt)[:reuse])
    heads_computed = [h[-1] for h in s.kvh]
    flops = [sum(r["body"].get("flops", 0) for r in x if r["type"] == "cell.tick") for x in (a, b)]
    return {"warm": warm, "prompt": prompt, "reused_positions": reuse,
            "kv_heads_match": heads_loaded == heads_computed, "status": v["status"],
            "class": v.get("class"), "flops": {"fp": flops[0], "fp+pcache": flops[1]},
            "routes": v.get("routes"),
            "blind_spot": "cache residency is logged in mem_mb, which B7 does not score"}


# ---- at rest: weights (RS-repairable) and activation logs (ALR1) -----------------------

def at_rest_experiment(model, sample_run):
    names = sorted(w for w in model.W if w != "embed")
    sizes, blobs = {}, {}
    for impl in C.IMPLS:
        blob = b"".join(model.linear(w, impl).blob for w in names)
        sizes[impl] = len(blob)
        blobs[impl] = blob
    wrapped = at_rest.rs_wrap(blobs["q4"])
    bad = bytearray(wrapped)
    # corrupt 12 bytes in each of the first 8 interleaved 255-byte codewords' span
    step = max(1, (len(bad) - 16) // 96)
    hits = 0
    for i in range(8, len(bad), step):
        bad[i] ^= 0x5A
        hits += 1
        if hits >= 96:
            break
    repaired = at_rest.rs_unwrap(bytes(bad))
    # decode repaired q4 bytes back to dequantized rows and compare to the live kernel
    off, rows_ok = 0, True
    for w in names:
        lin = model.linear(w, "q4")
        chunk = repaired[off:off + lin.nbytes]
        off += lin.nbytes
        rows_ok &= C.unpack_blob(chunk, "q4", lin.rows, lin.cols) == lin.deq
    jsonl = "".join(al.canon(r) + "\n" for r in sample_run).encode()
    packed = at_rest.pack(sample_run, repair=True)
    back = at_rest.unpack(packed)
    return {"weight_bytes": sizes, "q4_vs_fp": round(sizes["fp"] / sizes["q4"], 3),
            "q8_vs_fp": round(sizes["fp"] / sizes["q8"], 3),
            "rs_overhead": round(len(wrapped) / len(blobs["q4"]), 3),
            "corrupted_bytes": hits, "repaired_exact": repaired == blobs["q4"],
            "repaired_weights_equal_live": rows_ok,
            "log_records": len(sample_run), "log_jsonl_bytes": len(jsonl),
            "log_jsonl_lzma_bytes": len(lzma.compress(jsonl, preset=9)),
            "log_alr1_rs_bytes": len(packed),
            "log_roundtrip_exact": al.canon(back) == al.canon(sample_run)}


# ---- situation recall: which route held for situations like this? ---------------------

def _cos(a, b):
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(x * x for x in b)) or 1.0
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def recall_experiment(model, runs, dev="edge", route="q8", prompts=PROMPTS, k=3):
    """Label each situation by whether `route` held product identity with fp. Predict the
    label leave-one-out from three situation encodings, by k-NN:
      lexical  situation-memory's MissionEmbedder.embed_text (hash bag-of-words stand-in)
      latent   Z_in: the model's own mean final hidden state over the prompt
      margin   the cheap route's OWN min sample margin (no fp run needed)."""
    import situation_memory as sm
    R = runs[dev]
    labels = [bt.backtest_pair(R["fp"][p], R[route][p])["status"] == "certified" for p in prompts]
    emb = sm.MissionEmbedder()
    lex = [emb.embed_text(p) for p in prompts]
    lat = []
    for p in prompts:
        h = C._hidden(C.Stream(model, {}, None, "probe"), C.tokenize(p))
        lat.append([sum(r[i] for r in h) / len(h) for i in range(len(h[0]))])
    mar = [[min(r["body"]["margin"] for r in R[route][p]
                if r["type"] == "cell.tick" and r["body"]["kind"] == "sample")] for p in prompts]
    maj = max(sum(labels), len(labels) - sum(labels)) / len(labels)

    def loo(vecs, sim):
        hit = 0
        for i in range(len(vecs)):
            nb = sorted((j for j in range(len(vecs)) if j != i),
                        key=lambda j: (-sim(vecs[i], vecs[j]), j))[:k]
            vote = sum(labels[j] for j in nb)
            hit += (vote * 2 > k) == labels[i]
        return round(hit / len(vecs), 4)

    return {"route": route, "situations": len(prompts), "held": sum(labels),
            "majority_baseline": round(maj, 4),
            "loo_knn_acc": {"lexical": loo(lex, _cos), "latent": loo(lat, _cos),
                            "margin": loo(mar, lambda a, b: -abs(a[0] - b[0]))},
            "embedder": emb.id, "semantic": emb.semantic}


# ---- the whole report -------------------------------------------------------------------

def python_wall(model, name, prompt="the cat ", reps=3):
    best = 1e9
    for _ in range(reps):
        t = time.perf_counter()
        run_route(model, name, prompt)
        best = min(best, (time.perf_counter() - t) * 1000)
    return round(best, 1)


def report(model=None, fit=None, timing=False):
    if model is None:
        model, fit = C.build_model()
    C.use_device("edge")
    rep = {"model": {"cfg": model.cfg, "vocab": len(C.VOCAB), "fit": fit,
                     "weights_hash": model.weights_hash(),
                     "params": sum(len(w) * len(w[0]) for w in model.W.values())}}
    rep["differ"] = differ_profile(model)
    rep["b7"], runs = b7_matrix(model)
    rep["b4"] = {dev: b4_views(runs, dev) for dev in ("edge", "accel")}
    sample = runs["edge"]["spec-q4"][PROMPTS[0]]
    live = replay(model, sample)
    tam = replay(tampered(model), sample)
    rep["replay"] = {"route": "spec-q4", "records": len(sample), "replay_equal": live["equal"],
                     "tamper": {"weight": "L1.w1[0][0]+0.25", **tam["first_divergence"]}}
    rep["pcache"] = pcache_experiment(model)
    rep["at_rest"] = at_rest_experiment(model, sample)
    rep["recall"] = recall_experiment(model, runs)
    rep["report_hash"] = al.content_hash(rep)
    if timing:   # sidecar: real python wall time, best of 3; NOT hashed, NOT logged
        rep["python_wall_ms"] = {n: python_wall(model, n) for n in ROUTES}
    return rep, runs


def _fmt(rep):
    L = []
    m = rep["model"]
    L.append("model  d=%(d)d layers=%(layers)d heads=%(heads)d ff=%(ff)d ctx=%(ctx)d" % m["cfg"]
             + "  params=%d  readout train_acc=%.4f  jepa r2=%.4f"
             % (m["params"], m["fit"]["train_acc"], m["fit"]["jepa"]["r2"]))
    L.append("\n== differ (teacher-forced vs fp, %d positions)" % rep["differ"]["q8"]["positions"])
    L.append("   %-11s %-7s %-10s %-10s %-9s %-9s" % ("plan", "agree", "max|dz|", "mean|dz|",
                                                     "gate-safe", "gate-flip"))
    for k, v in rep["differ"].items():
        L.append("   %-11s %-7.4f %-10.4f %-10.4f %-9.4f %-9d" % (
            k, v["agree_rate"], v["max_dlogit"], v["mean_dlogit"], v["gate_safe_rate"],
            v["gate_flips"]))
    for dev, rows in rep["b7"].items():
        L.append("\n== B7 fp vs route, %d situations x %d tokens, device=%s"
                 % (len(PROMPTS), N_TOKENS, dev))
        for name, v in rows.items():
            t = v["totals"] or {}
            extra = "  accept=%d/%d" % tuple(v["accept"]) if "accept" in v else ""
            L.append("   %-10s certified %2d refused %2d  class=%-26s wall fp=%s alt=%s%s" % (
                name, v["certified"], v["refused"], v["class"],
                t.get("fp", {}).get("wall_ms", "-") if t else "-",
                t.get(name, {}).get("wall_ms", "-") if t else "-", extra))
    for dev, b in rep["b4"].items():
        L.append("\n== B4 device=%s  exact routes=%s" % (dev, b["exact_routes"]))
        L.append("   workload: class=%s frontier=%s fast=%s cheap=%s" % (
            b["workload"]["class"], b["workload"]["frontier"],
            b["workload"]["preferred_when"]["fast"], b["workload"]["preferred_when"]["cheap"]))
        L.append("   per-situation fast pick counts: %s   settled=%s" % (
            b["per_situation_fast"], b["settled"]))
    r = rep["replay"]
    L.append("\n== replay==live (%s, %d records): %s   tamper %s -> first divergence seq %d %s,"
             " first compute cell %s" % (r["route"], r["records"], r["replay_equal"],
                                         r["tamper"]["weight"], r["tamper"]["seq"],
                                         r["tamper"]["cell"], r["tamper"]["first_compute_cell"]))
    p = rep["pcache"]
    L.append("== prefix cache: reused %d positions, kv heads match=%s, B7 %s %s, flops %s" % (
        p["reused_positions"], p["kv_heads_match"], p["status"], p["class"], p["flops"]))
    a = rep["at_rest"]
    L.append("== at rest: weights fp=%d q8=%d q4=%d B (q4 %.2fx smaller); RS x%.3f, %d bytes"
             " corrupted -> repaired=%s, weights==live=%s" % (
                 a["weight_bytes"]["fp"], a["weight_bytes"]["q8"], a["weight_bytes"]["q4"],
                 a["q4_vs_fp"], a["rs_overhead"], a["corrupted_bytes"], a["repaired_exact"],
                 a["repaired_weights_equal_live"]))
    L.append("   activation log %d records: jsonl %d B, jsonl+lzma %d B, ALR1+RS %d B, exact=%s" % (
        a["log_records"], a["log_jsonl_bytes"], a["log_jsonl_lzma_bytes"],
        a["log_alr1_rs_bytes"], a["log_roundtrip_exact"]))
    c = rep["recall"]
    L.append("== recall (%s held on %d/%d situations; majority %.4f): LOO 3-NN %s" % (
        c["route"], c["held"], c["situations"], c["majority_baseline"], c["loo_knn_acc"]))
    if "python_wall_ms" in rep:
        L.append("== python wall ms (best of 3, sidecar, not the cost model): %s"
                 % rep["python_wall_ms"])
    L.append("\nreport_hash %s" % rep["report_hash"])
    return "\n".join(L)


if __name__ == "__main__":
    rep, _ = report(timing="--no-timing" not in sys.argv)
    if "--json" in sys.argv:
        slim = {k: v for k, v in rep.items()}
        for dev in slim["b4"]:
            slim["b4"][dev].pop("per_situation", None)
        print(json.dumps(slim, sort_keys=True, indent=1))
    else:
        print(_fmt(rep))
