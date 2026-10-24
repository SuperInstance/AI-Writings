"""E13 hdc_vs_crq — HDC as the turbovec substrate, head-to-head against code-real-quant's ADC.

code-real-quant (labs/code-real-quant, landed on main) is the fleet's real TurboQuant
index: cells hold ONLY 4-bit codes, searched by asymmetric distance (ADC). This imports
its `CodeIndex` unchanged and races hypervectors against it AT EQUAL BYTES PER VECTOR.

Contenders (bytes/vector = dim/2 for all but the last):
  crq-adc4        code-real-quant CodeIndex.code_search (4 bits/coord, ADC)       dim/2 B
  hdc-sym         random-hyperplane hypervector of 4*dim bits, Hamming (flux-hdc) dim/2 B
  hdc-adc         same bits, but the QUERY stays float: score = sum_i s_i * <p_i, q>
                  (the asymmetric trick applied to HDC)                           dim/2 B
  hdc1024-sym     flux-hdc's native 1024 bits, Hamming                           128 B

Benchmarks:
  crq-synth   code-real-quant's own protocol: synth(N=2000, dim=64, seed 7), M=50 queries
              = stored vector + N(0, 0.3) noise; recall@10 vs its float_search
  minilm-384  the 480 real MiniLM vectors (data/), 60 leave-one-out queries

Run: python3 hdc_vs_crq.py [--selftest]
"""
from __future__ import annotations
import os, sys, time
import common as C
from vec_index import hyperplanes

sys.path.insert(0, os.path.join(C.HERE, "..", "code-real-quant"))
import code_real_quant as CRQ  # noqa: E402


def hv_bits(planes, v):
    return [1 if C.dot(p, v) >= 0 else -1 for p in planes]


def pack_bits(signs):
    x = 0
    for i, s in enumerate(signs):
        if s > 0:
            x |= 1 << i
    return x


def run(vecs, queries, exclude_self, dim, log=print, k=10):
    idx = CRQ.CodeIndex(dim=dim, keep_float=True)
    t0 = time.time()
    for v in vecs:
        idx.add(v)
    t_crq = time.time() - t0
    nb = 4 * dim
    P = hyperplanes(nb, dim, seed=23)
    P1024 = hyperplanes(1024, dim, seed=29)
    units = [C.unit(v) for v in vecs]
    hv = [pack_bits(hv_bits(P, u)) for u in units]
    signs = [hv_bits(P, u) for u in units]
    hv1024 = [pack_bits(hv_bits(P1024, u)) for u in units]
    rec = {"crq-adc4": 0, "hdc-sym": 0, "hdc-adc": 0, "hdc1024-sym": 0}
    tot = 0
    for qi, q in queries:
        def top(ids_scores):
            ranked = [i for i, _ in sorted(ids_scores, key=lambda t: -t[1]) if not (exclude_self and i == qi)]
            return set(ranked[:k])
        truth = [i for i in idx.float_search(q, k + 1) if not (exclude_self and i == qi)][:k]
        got_crq = [i for i in idx.code_search(q, k + 1) if not (exclude_self and i == qi)][:k]
        qu = C.unit(q)
        qh = pack_bits(hv_bits(P, qu))
        qp = [C.dot(p, qu) for p in P]
        qh1024 = pack_bits(hv_bits(P1024, qu))
        n = len(vecs)
        got = {
            "crq-adc4": set(got_crq),
            "hdc-sym": top([(i, -bin(qh ^ hv[i]).count("1")) for i in range(n)]),
            "hdc-adc": top([(i, sum(a * b for a, b in zip(qp, signs[i]))) for i in range(n)]),
            "hdc1024-sym": top([(i, -bin(qh1024 ^ hv1024[i]).count("1")) for i in range(n)]),
        }
        for kname in rec:
            rec[kname] += len(set(truth) & got[kname])
        tot += len(truth)
    out = {kname: round(v / tot, 4) for kname, v in rec.items()}
    out["bytes"] = {"crq-adc4": dim // 2, "hdc-sym": nb // 8, "hdc-adc": nb // 8, "hdc1024-sym": 128}
    out["crq_build_s"] = round(t_crq, 1)
    return out


def measure(log=print):
    res = {}
    vecs = CRQ.synth(2000, 64, 7)
    rng = CRQ.XorShift64(11)
    qs = []
    for m in range(50):
        i = rng.next() % len(vecs)
        qs.append((i, [x + 0.3 * rng.gauss() for x in vecs[i]]))
    res["crq-synth"] = run(vecs, qs, exclude_self=False, dim=64)
    real = C.load_embeddings()
    res["minilm-384"] = run(real, [(i, real[i]) for i in range(60)], exclude_self=True, dim=384)
    for name, r in res.items():
        log(f"  {name:10s} " + "  ".join(f"{k}={r[k]:.3f} ({r['bytes'][k]} B)" for k in r["bytes"]))
    return res


def selftest():
    c = C.Checks()
    r = C.Rng(4)
    vecs = [[r.gauss() for _ in range(16)] for _ in range(60)]
    out = run(vecs, [(i, vecs[i]) for i in range(8)], exclude_self=True, dim=16, log=lambda *a: None)
    c.ok(all(0.0 <= out[k] <= 1.0 for k in out["bytes"]), "recalls in [0,1]")
    c.ok(out["bytes"]["crq-adc4"] == out["bytes"]["hdc-sym"] == 8, "equal bytes per vector")
    s = hv_bits(hyperplanes(8, 4, seed=1), [1, 0, 0, 0])
    c.ok(set(s) <= {-1, 1} and len(s) == 8, "sign bits")
    c.ok(pack_bits([1, -1, 1]) == 0b101, "pack bits")
    idx = CRQ.CodeIndex(dim=16)
    for v in vecs[:5]:
        idx.add(v)
    c.ok(idx.verify_chain() and not hasattr(idx.cells[0], "vector"), "using the real code-real-quant cells (codes only)")
    return c.report("hdc_vs_crq")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    import json
    print("E13 hdc_vs_crq — recall@10 vs float, equal bytes/vector (except hdc1024)")
    res = measure()
    with open(C.HERE + "/results_hdc_vs_crq.json", "w") as f:
        json.dump(res, f, indent=1)
