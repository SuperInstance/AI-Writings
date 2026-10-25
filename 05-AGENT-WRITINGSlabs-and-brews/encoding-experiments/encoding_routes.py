"""E8 encoding_routes — encodings as alternative ROUTES on System-2's iron triangle (B7 + B4).

The brief: "a delta-coded vs raw budget log; an HDC vs TurboQuant index —
product-identical retrieval, different cost." This file records each encoding as an
ActiveLog route run (cell.tick budgets + one ledger.transaction carrying the PRODUCT),
then hands the runs to the real B7 gate (labs/system2-backtest backtest_pair /
backtest_corpus) and the real B4 chooser (labs/route-preference prefer).

Workload A — STORE a batch of ActiveLog records and read it back.
  routes: jsonl | ctx-lzma (E1) | ctx-lzma-rs (E1 + E2's interleaved Reed-Solomon)
  product: {n, records_hash} of the records as READ BACK (must be identical to certify)
  budget: wall_ms = measured encode+decode time, storage_bytes.prod = bytes at rest
  standing (B4 `good`): trials out of 6 that survive BER 1e-4 on the stored bytes

Workload B — RETRIEVE top-10 for a query over the 480 real MiniLM vectors.
  routes: exact float scan | tq4 shortlist(50) + exact rerank | hdc1024 shortlist(50) + rerank
  product: the top-10 id list. A shortlist that misses a true neighbour yields a DIFFERENT
  product, and B7 must refuse it — that refusal rate is the measurement.

Run: python3 encoding_routes.py [--selftest]
"""
from __future__ import annotations
import lzma, os, sys, time
import common as C
import delta_budget as E1
import ecc_chain as E2
import vec_index as E3

for sub in ("system2-backtest", "route-preference"):
    sys.path.insert(0, os.path.join(C.HERE, "..", sub))
import backtest as B7  # noqa: E402
import route_preference as B4  # noqa: E402

AL = E1.AL


def route_run(route, ticks, product):
    """ticks: [(cell, wall_ms, prod_bytes)] -> ActiveLog records closed by a ledger.transaction."""
    log = AL.ActiveLog(dev="enc-e8-" + route)
    total = AL.ZERO_BUDGET
    for cell, ms, prod in ticks:
        b = AL.budget(wall_ms=ms, prod=prod)
        log.emit("cell.tick", {"cell": cell, "budget": b})
        total = AL.add_budget(total, b)
    log.emit("ledger.transaction", {"route": route, "total_budget": total, **product})
    return log.records


def _ms(t0):
    return max(1, round(1000 * (time.time() - t0)))


# ---------------- workload A: store + read back -------------------------------------------------
def _best_of(fn, reps=3):
    """min wall-clock of `reps` runs: a shared container is noisy, and B7 compares wall_ms."""
    best = None
    for _ in range(reps):
        t0 = time.time()
        out = fn()
        ms = _ms(t0)
        best = ms if best is None else min(best, ms)
    return out, best


def store_routes(recs):
    import json

    def raw():
        blob = "".join(AL.canon(r) + "\n" for r in recs).encode()
        return blob, [json.loads(l) for l in blob.decode().splitlines()]

    def ctx():
        z = lzma.compress(E1.encode(E1.to_cols(recs), "ctx"), preset=9)
        return z, E1.from_cols(E1.decode(lzma.decompress(z), "ctx"))

    def ctx_rs():
        w = E2.rs_wrap(lzma.compress(E1.encode(E1.to_cols(recs), "ctx"), preset=9))
        return w, E1.from_cols(E1.decode(lzma.decompress(E2.rs_unwrap(w)), "ctx"))

    out = {}
    for name, fn in (("jsonl", raw), ("ctx-lzma", ctx), ("ctx-lzma-rs", ctx_rs)):
        (stored, back), ms = _best_of(fn)
        out[name] = (stored, back, ms)
    return out


def standing(name, stored, recs, r, trials=6):
    dec = {"jsonl": lambda b: E2.restore("jsonl-200", b),
           "ctx-lzma": lambda b: E2.restore("ctx-lzma", b),
           "ctx-lzma-rs": lambda b: E2.restore("ctx-lzma", E2.rs_unwrap(b))}[name]
    ok = 0
    for _ in range(trials):
        noisy, _ = E2.bitflips(stored, 1e-4, r)
        try:
            ok += AL.canon(dec(noisy)) == AL.canon(recs)
        except Exception:
            pass
    return ok


def workload_a(sizes=(200, 400, 800), log=print):
    r = C.Rng(5)
    cases, standing_tot, runs_last = [], {}, None
    for i, n in enumerate(sizes):
        recs = E1.build_log(n, seed=40 + i)
        runs = {}
        for name, (stored, back, ms) in store_routes(recs).items():
            product = {"n": len(back), "records_hash": AL.content_hash(back)}
            runs[name] = route_run(name, [("encode+decode", ms, len(stored))], product)
            standing_tot[name] = standing_tot.get(name, 0) + standing(name, stored, recs, r)
        cases.append({"id": f"batch{n}", "runs": runs})
        runs_last = runs
    res = {}
    for a, b in (("jsonl", "ctx-lzma"), ("ctx-lzma", "ctx-lzma-rs")):
        rep = B7.backtest_corpus([{"id": c["id"], "a": c["runs"][a], "b": c["runs"][b]} for c in cases], (a, b))
        res[f"{a} vs {b}"] = rep
        w = rep["workload"]
        log(f"  B7 {a} vs {b}: certified {rep['certified']}, refused {rep['refused']}; class {w['class']}; "
            f"preferred_when {w['preferred_when']}; totals {rep['totals']}")
    pref = B4.prefer(list(runs_last.items()), standing=standing_tot)
    res["B4"] = pref
    log(f"  B4 prefer (standing = BER-1e-4 survivals {standing_tot}): frontier={pref.get('frontier')} preferred_when={pref.get('preferred_when')}")
    return res


# ---------------- workload B: retrieval ---------------------------------------------------------
def workload_b(nq=60, shortlist=50, log=print):
    vecs = [C.unit(v) for v in C.load_embeddings()]
    n, d = len(vecs), len(vecs[0])
    rot = E3.Rotation(d)
    rv = [rot(v) for v in vecs]
    lv = [x / d ** 0.5 for x in E3.LM4]
    deq = [[lv[E3.nearest(lv, x)] for x in row] for row in rv]
    P = E3.hyperplanes(1024, d)
    hv = [E3.to_bits(P, v) for v in vecs]
    stats = {k: {"identical": 0, "refused": 0} for k in ("tq4+rerank", "hdc1024+rerank")}
    verdicts = {}
    for q in range(nq):
        def exact_top(cands):
            return sorted(cands, key=lambda j: -C.dot(vecs[q], vecs[j]))[:10]
        t0 = time.time()
        truth = exact_top([j for j in range(n) if j != q])
        ex_run = route_run("exact", [("scan-float", _ms(t0), 4 * d * n)], {"top10": truth})
        for name, score in (("tq4+rerank", lambda j: C.dot(rv[q], deq[j])),
                            ("hdc1024+rerank", lambda j: -bin(hv[q] ^ hv[j]).count("1"))):
            t0 = time.time()
            short = sorted((j for j in range(n) if j != q), key=lambda j: -score(j))[:shortlist]
            got = exact_top(short)
            hot = (d // 2 if name.startswith("tq4") else 128) * n
            run = route_run(name, [("shortlist", _ms(t0), hot), ("rerank-cold-reads", 1, 4 * d * n)], {"top10": got})
            v = B7.backtest_pair(ex_run, run)
            stats[name]["identical" if v["status"] == "certified" else "refused"] += 1
            verdicts[name] = v
    for name, s in stats.items():
        log(f"  B7 exact vs {name}: certified (product-identical top-10) {s['identical']}/{nq}, refused {s['refused']}/{nq}")
    last = verdicts["tq4+rerank"]
    log(f"  last tq4 verdict: status={last['status']} class={last.get('class')} axes={last.get('axes')} routes={last.get('routes')}")
    log(f"  hot (in-memory) bytes: exact {4 * d * n}, tq4 {d // 2 * n}, hdc1024 {128 * n} — B7 has no hot-memory axis, so it cannot see this")
    return {"stats": stats, "shortlist": shortlist}


def selftest():
    c = C.Checks()
    recs = E1.build_log(30, seed=2)
    routes = store_routes(recs)
    for name, (stored, back, ms) in routes.items():
        c.ok(AL.canon(back) == AL.canon(recs), f"{name} reads back identical records")
    runs = {name: route_run(name, [("encode+decode", ms, len(stored))], {"n": len(back), "records_hash": AL.content_hash(back)})
            for name, (stored, back, ms) in routes.items()}
    v = B7.backtest_pair(runs["jsonl"], runs["ctx-lzma"])
    c.ok(v["status"] == "certified", "B7 certifies raw vs ctx-lzma (same product)")
    c.ok(v["cheap_detail"]["storage"] == "ctx-lzma", "B7: ctx-lzma wins storage")
    bad = route_run("ctx-lzma", [("encode+decode", 1, 10)], {"n": 30, "records_hash": "0xdeadbeef"})
    c.ok(B7.backtest_pair(runs["jsonl"], bad)["status"] == "refused", "B7 refuses a different product")
    p = B4.prefer(list(runs.items()), standing={"jsonl": 0, "ctx-lzma": 0, "ctx-lzma-rs": 6})
    c.ok(p.get("status") != "refused", "B4 accepts the three store routes")
    return c.report("encoding_routes")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    import json
    print("E8 encoding_routes — Workload A (store ActiveLog batches of 200/400/800 records)")
    a = workload_a()
    print("E8 — Workload B (retrieve top-10 over 480 MiniLM vectors, 60 queries, shortlist 50 then exact rerank)")
    b = workload_b()
    with open(C.HERE + "/results_encoding_routes.json", "w") as f:
        json.dump({"A": a, "B": b}, f, indent=1, default=str)
