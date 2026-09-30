"""E4 hdc_theorems — measure flux-hdc's five stated theorems on 1024-bit hypervectors.

flux-hdc's README states five "proven theorems" but its source was not reachable
(raw paths 404), so each claim is re-implemented from its one-line statement and
MEASURED here. Hypervectors are Python ints used as 1024-bit sets.

  T1 binding (XOR) preserves orthogonality      -> sim(a^b, a) ~ 0.5, unbind exact
  T2 bundling (majority) preserves similarity   -> sim(bundle, member) and codebook capacity
  T3 1024 bits gives < 1% matching error        -> estimator std + a concrete matching task
  T4 1024->128 fold: eps <= 0.003 for sim >= 0.7 -> |sim_fold - sim_full| for XOR- and subsample-fold
  T5 JL-bounded dimension reduction             -> SimHash cosine error at 1024 vs 128 bits on real vectors

Run: python3 hdc_theorems.py [--selftest]
"""
from __future__ import annotations
import math, sys
import common as C
from vec_index import fold_xor, fold_sub, hyperplanes, to_bits

D = 1024


def rand_hv(r, n=D):
    x = 0
    for k in range(0, n, 64):
        x |= r.u64() << k
    return x & ((1 << n) - 1)


def sim(a, b, n=D):
    return 1 - bin(a ^ b).count("1") / n


def flip(r, x, frac, n=D):
    """flip exactly round(frac*n) distinct bits -> a vector at similarity 1-frac."""
    idx = list(range(n))
    for i in range(n - 1, 0, -1):
        j = r.randint(0, i)
        idx[i], idx[j] = idx[j], idx[i]
    for i in idx[:round(frac * n)]:
        x ^= 1 << i
    return x


def bundle(vs, r, n=D):
    out = 0
    half = len(vs) / 2
    for i in range(n):
        cnt = sum((v >> i) & 1 for v in vs)
        if cnt > half or (cnt == half and r.random() < 0.5):
            out |= 1 << i
    return out


def measure(r=None, trials=200, log=print):
    r = r or C.Rng(2026)
    out = {}
    # T1
    dev, exact = [], 0
    for _ in range(trials):
        a, b = rand_hv(r), rand_hv(r)
        ab = a ^ b
        dev.append(abs(sim(ab, a) - 0.5))
        exact += (ab ^ b) == a
    out["T1"] = {"mean_abs_dev_from_0.5": round(sum(dev) / len(dev), 4), "unbind_exact": exact / trials}
    log(f"T1 bind: |sim(a^b,a)-0.5| mean={out['T1']['mean_abs_dev_from_0.5']}  unbind exact {exact}/{trials}")
    # T2: bundle m members; can we still pick every member out of a 1000-item codebook?
    book = [rand_hv(r) for _ in range(1000)]
    cap = {}
    for m in (3, 5, 9, 17, 33, 65, 129):
        hits = sims = 0
        reps = 4
        for rep in range(reps):
            members = list(range(rep * 7, rep * 7 + m))
            members = [i % 1000 for i in members]
            bnd = bundle([book[i] for i in members], r)
            scores = [sim(bnd, v) for v in book]
            top = set(C.topk(scores, m))
            hits += len(top & set(members))
            sims += sum(scores[i] for i in members) / m
        cap[m] = {"member_sim": round(sims / reps, 4), "recovered": round(hits / (reps * m), 3)}
    out["T2"] = cap
    log("T2 bundle capacity (1000-item codebook): " + ", ".join(f"m={m}: sim {v['member_sim']}, recov {v['recovered']}" for m, v in cap.items()))
    # T3: estimator noise + a matching task (does a 0.7-similar partner beat 999 randoms?)
    est_std = math.sqrt(0.25 / D)
    wins = 0
    for _ in range(trials):
        a = rand_hv(r)
        partner = flip(r, a, 0.30)
        best_random = max(sim(a, rand_hv(r)) for _ in range(999))
        wins += sim(a, partner) > best_random
    out["T3"] = {"random_pair_sim_std": round(est_std, 4), "match_error_at_sim0.7_vs_999": round(1 - wins / trials, 4)}
    log(f"T3 random-pair sim std={est_std:.4f}; matching error (0.7-partner vs 999 randoms)={out['T3']['match_error_at_sim0.7_vs_999']}")
    # T4: fold error for pairs with true sim >= 0.7
    t4 = {}
    for s in (0.7, 0.8, 0.9, 0.95):
        ex, es = [], []
        for _ in range(trials):
            a = rand_hv(r)
            b = flip(r, a, 1 - s)
            full = sim(a, b)
            ex.append(abs(sim(fold_xor(a), fold_xor(b), 128) - full))
            es.append(abs(sim(fold_sub(a), fold_sub(b), 128) - full))
        t4[s] = {"xor_mean_err": round(sum(ex) / trials, 4), "sub_mean_err": round(sum(es) / trials, 4),
                 "xor_theory": round(abs((1 + (2 * s - 1) ** 8) / 2 - s), 4)}
    out["T4"] = t4
    log("T4 fold |err| (claim: <= 0.003): " + ", ".join(f"s={s}: xor {v['xor_mean_err']} (theory {v['xor_theory']}), sub {v['sub_mean_err']}" for s, v in t4.items()))
    return out


def measure_t5(log=print):
    vecs = [C.unit(v) for v in C.load_embeddings()[:120]]
    P = hyperplanes(1024, len(vecs[0]))
    hv = [to_bits(P, v) for v in vecs]
    e1024, e128 = [], []
    for i in range(0, 120, 2):
        for j in range(1, 120, 7):
            if i == j:
                continue
            cos = max(-1, min(1, C.dot(vecs[i], vecs[j])))
            true = 1 - math.acos(cos) / math.pi  # SimHash expectation
            e1024.append(abs(sim(hv[i], hv[j]) - true))
            e128.append(abs(sim(hv[i] & ((1 << 128) - 1), hv[j] & ((1 << 128) - 1), 128) - true))
    out = {"pairs": len(e1024), "mean_err_1024": round(sum(e1024) / len(e1024), 4),
           "mean_err_128": round(sum(e128) / len(e128), 4)}
    log(f"T5 SimHash angle-estimate error on real MiniLM pairs: 1024b {out['mean_err_1024']}, 128b {out['mean_err_128']} ({out['pairs']} pairs)")
    return out


def selftest():
    c = C.Checks()
    r = C.Rng(5)
    a = rand_hv(r)
    c.ok(a < (1 << D), "hv width")
    c.ok(abs(sim(a, flip(r, a, 0.25)) - 0.75) < 1e-9, "flip sets exact similarity")
    c.ok(sim(a, a) == 1.0 and sim(a, a ^ ((1 << D) - 1)) == 0.0, "sim bounds")
    m = measure(C.Rng(9), trials=20, log=lambda *x: None)
    c.ok(m["T1"]["unbind_exact"] == 1.0, "T1 unbind exact")
    c.ok(m["T1"]["mean_abs_dev_from_0.5"] < 0.03, "T1 bound ~ orthogonal")
    c.ok(m["T2"][3]["recovered"] == 1.0, "T2 small bundles recover all members")
    c.ok(m["T3"]["match_error_at_sim0.7_vs_999"] == 0.0, "T3 0.7 partner always wins")
    # T4 theory check: XOR-fold similarity collapses toward 0.5 as predicted
    c.ok(abs(m["T4"][0.9]["xor_mean_err"] - m["T4"][0.9]["xor_theory"]) < 0.05, "T4 xor-fold matches (1+(2s-1)^8)/2")
    c.ok(m["T4"][0.7]["xor_mean_err"] > 0.003, "T4 claim eps<=0.003 does NOT hold for xor fold")
    c.ok(m["T4"][0.7]["sub_mean_err"] > 0.003, "T4 claim eps<=0.003 does NOT hold for subsample fold")
    return c.report("hdc_theorems")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    import json
    res = measure()
    res["T5"] = measure_t5()
    with open(C.HERE + "/results_hdc_theorems.json", "w") as f:
        json.dump(res, f, indent=1)
