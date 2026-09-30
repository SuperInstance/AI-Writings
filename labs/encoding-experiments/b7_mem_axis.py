"""E14 b7_mem_axis — give System-2's B7 a hot-memory axis and see which verdicts change.

E8 found a blind spot: `backtest.axes_of` reads wall_ms, usd, tokens and storage bytes,
but IGNORES the budget's `mem_mb`. So a route that holds 8x less in RAM (tq4 codes hot,
floats cold) looks strictly worse to B7 (it also pays for the cold floats on disk).

This experiment does NOT modify labs/system2-backtest. It re-scores B7's own replayed
routes with one extra cheapness sign, using B7's own `_combine` / `_classify`:
    cheap = combine(usd, tokens, storage_bytes, mem_mb)      (proposed)
    cheap = combine(usd, tokens, storage_bytes)              (B7 today)
The gate is untouched: products must be identical before anything is scored.

Routes (real replays through B7.replay_route), per query over 480 MiniLM vectors:
  exact          float scan; hot = 480 x 1536 B; storage = same floats
  crq+rerank     code-real-quant codes hot (192 B/vec), shortlist 50, exact rerank from
                 cold floats; storage = codes + floats
Also run on B7's five shipped fixtures. They DO report mem_mb (1-6 MB per tick,
checked), so this is a real regression test: does the extra axis change any verdict
where memory moves with the other cheapness measurements?

Run: python3 b7_mem_axis.py [--selftest]
"""
from __future__ import annotations
import os, sys, time
import common as C

for sub in ("system2-backtest", "code-real-quant", "activeledger"):
    sys.path.insert(0, os.path.join(C.HERE, "..", sub))
import activeledger as AL  # noqa: E402
import backtest as B7  # noqa: E402
import code_real_quant as CRQ  # noqa: E402


def score_with_mem(a, b, names):
    """B7.score with mem_mb as a fourth cheapness measurement (lower wins)."""
    ax_a, ax_b = a["axes"], b["axes"]
    fast = B7._axis_winner(B7._cmp(ax_a["wall_ms"], ax_b["wall_ms"]))
    signs = (B7._cmp(ax_a["usd"], ax_b["usd"]), B7._cmp(ax_a["tokens"], ax_b["tokens"]),
             B7._cmp(ax_a["storage_bytes"], ax_b["storage_bytes"]),
             B7._cmp(a["budget"]["mem_mb"] or 0, b["budget"]["mem_mb"] or 0))
    axes = {"good": "tie", "fast": fast, "cheap": B7._combine(signs)}
    return B7._classify(axes, names)


def run_pair(ra, rb):
    a, b = B7.replay_route(ra), B7.replay_route(rb)
    if a["product_hash"] != b["product_hash"]:
        return None, None
    today = B7.score(a["axes"], b["axes"], None, (a["route"], b["route"]))
    return today, score_with_mem(a, b, (a["route"], b["route"]))


def route(name, ticks, product):
    log = AL.ActiveLog(dev="e14-" + name)
    total = AL.ZERO_BUDGET
    for cell, ms, prod, mem in ticks:
        bud = AL.budget(wall_ms=ms, prod=prod, mem_mb=mem)
        log.emit("cell.tick", {"cell": cell, "budget": bud})
        total = AL.add_budget(total, bud)
    log.emit("ledger.transaction", {"route": name, "total_budget": total, **product})
    return log.records


def mb(nbytes):
    return round(nbytes / 1048576, 4)


def measure(nq=30, log=print):
    vecs = C.load_embeddings()
    n, d = len(vecs), len(vecs[0])
    idx = CRQ.CodeIndex(dim=d, keep_float=True)
    for v in vecs:
        idx.add(v)
    code_b = sum(len(c.codes) for c in idx.cells)
    float_b = 4 * d * n
    counts = {}
    changed = 0
    refused = 0
    for q in range(nq):
        t0 = time.time()
        truth = [i for i in idx.float_search(vecs[q], 11) if i != q][:10]
        ms_exact = max(1, round(1000 * (time.time() - t0)))
        t0 = time.time()
        short = [i for i in idx.code_search(vecs[q], 51) if i != q][:50]
        qu = CRQ._unit_scaled(vecs[q])
        got = sorted(short, key=lambda i: sum((a - b) ** 2 for a, b in zip(qu, idx._float[i])))[:10]
        ms_crq = max(1, round(1000 * (time.time() - t0)))
        ra = route("exact", [("scan", ms_exact, float_b, mb(float_b))], {"top10": truth})
        rb = route("crq+rerank", [("shortlist", ms_crq, code_b + float_b, mb(code_b)),
                                  ("rerank-cold", 1, 0, 0)], {"top10": got})
        today, prop = run_pair(ra, rb)
        if today is None:
            refused += 1
            continue
        key = (today["class"], prop["class"])
        counts[key] = counts.get(key, 0) + 1
        changed += today["class"] != prop["class"]
    res = {"queries": nq, "refused_product_differs": refused,
           "class_today->with_mem": {f"{a} -> {b}": v for (a, b), v in counts.items()},
           "verdicts_changed": changed, "hot_bytes": {"exact": float_b, "crq+rerank": code_b}}
    log(f"  retrieval routes, {nq} queries: refused {refused}; verdict class (B7 today -> with mem axis): {res['class_today->with_mem']}")
    log(f"  hot bytes: exact {float_b}, crq+rerank {code_b} ({float_b / code_b:.1f}x less)")
    # fixtures: must be unchanged
    fx_changed = fx_total = 0
    for name, (labels, cases) in B7.fixture_pairs().items():
        for c in cases:
            if c["a"] is None or c["b"] is None:
                continue
            try:
                today, prop = run_pair(c["a"], c["b"])
            except B7.Refusal:
                continue
            if today is None:
                continue
            fx_total += 1
            fx_changed += today["class"] != prop["class"]
    res["fixtures"] = {"certified_pairs": fx_total, "verdicts_changed": fx_changed}
    log(f"  B7's shipped fixtures: {fx_total} certified pairs, verdicts changed by the mem axis: {fx_changed}")
    return res


def selftest():
    c = C.Checks()
    ra = route("a", [("x", 10, 100, 5.0)], {"p": 1})
    rb = route("b", [("x", 10, 100, 1.0)], {"p": 1})
    today, prop = run_pair(ra, rb)
    c.ok(today["class"] == "equivalent", "B7 today: memory invisible -> equivalent")
    c.ok(prop["class"] == "dominates-one-axis" and prop["dominant"] == "b", "with mem axis: less RAM wins cheap")
    rc = route("c", [("x", 10, 50, 5.0)], {"p": 1})
    _, prop2 = run_pair(rc, rb)
    c.ok(prop2["class"] == "trade-off", "less storage vs less RAM -> split cheap -> trade-off")
    c.ok(run_pair(ra, route("d", [("x", 1, 1, 0.0)], {"p": 2}))[0] is None, "gate still refuses different products")
    return c.report("b7_mem_axis")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    import json
    print("E14 b7_mem_axis — B7 re-scored with a hot-memory (mem_mb) cheapness measurement")
    res = measure()
    with open(C.HERE + "/results_b7_mem_axis.json", "w") as f:
        json.dump(res, f, indent=1)
