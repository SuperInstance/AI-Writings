"""E7 holos_flock — HOLOS "holographic shards" measured against a same-bytes 4-bit quantizer.

Gem: HOLOS (Forge/Runtime): shard S_k = P_k W P_k^T with P_k a seeded random
orthonormal k x n projection; reconstruction W' = P_k^T S_k P_k; a "flock" of m shards
is combined by "wavefront synthesis" (unit-normalise each shard's output, weight by
mean pairwise coherence). Claims: quality rises as you load more shards; no re-encoding.

Matrices (n = 128):
  gauss     i.i.d. Gaussian (no structure — the worst case for any projection)
  lowrank   rank-8 signal + 10% noise (the best case)
  real-cov  covariance of the first 128 dims of the 480 real MiniLM embeddings (data/)

Measured per matrix, as relative Frobenius error ||W - c*W'|| / ||W|| (c = best scalar,
since averaged shards are shrunk by ~(k/n)^2):
  shard k            one shard at k (bytes = 4 k^2)
  flock m x k        mean of m shards (bytes = 4 m k^2)
  one big shard      a single shard with the SAME bytes as the flock (k' = k*sqrt(m))
  q4                 4-bit per-row absmax quantisation of W itself (bytes = n^2/2 + 4n)
and the wavefront-synthesis output cosine vs a plain mean, for y = W x.

Run: python3 holos_flock.py [--selftest]
"""
from __future__ import annotations
import math, sys
import common as C


def matmul(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]


def T(A):
    return [list(r) for r in zip(*A)]


def fro(A):
    return math.sqrt(sum(x * x for r in A for x in r))


def sub(A, B, c=1.0):
    return [[a - c * b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]


def inner(A, B):
    return sum(a * b for ra, rb in zip(A, B) for a, b in zip(ra, rb))


def ortho_rows(k, n, r):
    rows = []
    while len(rows) < k:
        v = [r.gauss() for _ in range(n)]
        for u in rows:
            d = C.dot(v, u)
            v = [a - d * b for a, b in zip(v, u)]
        nv = C.norm(v)
        if nv > 1e-9:
            rows.append([a / nv for a in v])
    return rows


def shard(W, P):
    return matmul(matmul(P, W), T(P))


def recon(S, P):
    return matmul(matmul(T(P), S), P)


def rel_err(W, Wr):
    """Best-scalar relative error: min_c ||W - c Wr|| / ||W||."""
    den = inner(Wr, Wr)
    c = inner(W, Wr) / den if den else 0.0
    return fro(sub(W, Wr, c)) / fro(W)


def q4(W):
    out = []
    for row in W:
        m = max(abs(x) for x in row) or 1.0
        out.append([round(x / m * 7) / 7 * m for x in row])  # 15 levels in 4 bits, per-row scale
    return out


def matrices(n=128, seed=3):
    r = C.Rng(seed)
    g = [[r.gauss() for _ in range(n)] for _ in range(n)]
    U = [[r.gauss() for _ in range(8)] for _ in range(n)]
    V = [[r.gauss() for _ in range(n)] for _ in range(8)]
    lr = matmul(U, V)
    s = fro(lr) / n
    lr = [[x + 0.1 * s * r.gauss() for x in row] for row in lr]
    out = {"gauss": g, "lowrank": lr}
    try:
        E = [v[:n] for v in C.load_embeddings()]
        mu = [sum(col) / len(E) for col in zip(*E)]
        Ec = [[x - m for x, m in zip(v, mu)] for v in E]
        out["real-cov"] = matmul(T(Ec), Ec)
    except FileNotFoundError:
        pass
    return out


def wavefront(ys):
    us = [C.unit(y) for y in ys]
    m = len(us)
    coh = [[C.dot(us[i], us[j]) for j in range(m)] for i in range(m)]
    trust = [sum(row) / m for row in coh]
    tot = sum(trust) or 1.0
    return [sum(trust[i] / tot * us[i][d] for i in range(m)) for d in range(len(us[0]))]


def measure(n=128, k=32, flock=(1, 2, 4, 8), log=print):
    res = {}
    for name, W in matrices(n).items():
        r = C.Rng(17)
        Ps = [ortho_rows(k, n, r) for _ in range(max(flock))]
        recs = [recon(shard(W, P), P) for P in Ps]
        row = {}
        for m in flock:
            mean = [[sum(R[i][j] for R in recs[:m]) / m for j in range(n)] for i in range(n)]
            kb = min(n, round(k * math.sqrt(m)))
            Pb = ortho_rows(kb, n, C.Rng(100 + m))
            row[m] = {"bytes": 4 * m * k * k, "flock_err": round(rel_err(W, mean), 4),
                      "one_big_shard_k": kb, "one_big_shard_err": round(rel_err(W, recon(shard(W, Pb), Pb)), 4)}
        Wq = q4(W)
        qerr = fro(sub(W, Wq)) / fro(W)
        # wavefront synthesis vs plain mean of shard outputs, y = W x
        x = [C.Rng(5).gauss() for _ in range(n)]
        y = [C.dot(rw, x) for rw in W]
        ys = [[C.dot(rw, x) for rw in R] for R in recs[:max(flock)]]
        wf = wavefront(ys)
        pm = [sum(v[d] for v in ys) / len(ys) for d in range(n)]
        res[name] = {"flock": row, "q4": {"bytes": n * n // 2 + 4 * n, "err": round(qerr, 4)},
                     "cos_single": round(C.dot(C.unit(ys[0]), C.unit(y)), 4),
                     "cos_wavefront": round(C.dot(C.unit(wf), C.unit(y)), 4),
                     "cos_plain_mean": round(C.dot(C.unit(pm), C.unit(y)), 4)}
        log(f"  {name:9s} full={4 * n * n} B | " + "  ".join(
            f"m={m}: {v['bytes']}B err {v['flock_err']} (one k={v['one_big_shard_k']} shard: {v['one_big_shard_err']})" for m, v in row.items()) +
            f" | q4 {res[name]['q4']['bytes']}B err {res[name]['q4']['err']}")
        log(f"  {'':9s} y=Wx cosine: single shard {res[name]['cos_single']}, wavefront({max(flock)}) {res[name]['cos_wavefront']}, plain mean {res[name]['cos_plain_mean']}")
    return res


def selftest():
    c = C.Checks()
    r = C.Rng(1)
    P = ortho_rows(6, 16, r)
    G = matmul(P, T(P))
    c.ok(all(abs(G[i][j] - (i == j)) < 1e-9 for i in range(6) for j in range(6)), "P has orthonormal rows")
    W = [[r.gauss() for _ in range(16)] for _ in range(16)]
    Pf = ortho_rows(16, 16, r)
    c.ok(rel_err(W, recon(shard(W, Pf), Pf)) < 1e-9, "k = n shard reconstructs exactly")
    c.ok(fro(sub(W, q4(W))) / fro(W) < 0.15, "q4 error small")
    small = measure(n=24, k=6, flock=(1, 4), log=lambda *a: None)
    g = small["gauss"]["flock"]
    c.ok(g[4]["flock_err"] < g[1]["flock_err"], "more shards -> lower error (HOLOS claim holds)")
    c.ok(small["gauss"]["q4"]["err"] < g[1]["flock_err"] and small["gauss"]["q4"]["bytes"] < 4 * 24 * 24, "q4 beats a shard")
    wf = wavefront([[1, 0], [1, 0.1], [0.9, 0]])
    c.ok(abs(C.norm(wf) - 1) < 0.05 and wf[0] > 0.9, "wavefront of agreeing shards ~ their direction")
    return c.report("holos_flock")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    import json
    print("E7 holos_flock: n=128, shard k=32 (16x smaller than W), relative Frobenius error (best scalar)")
    res = measure()
    with open(C.HERE + "/results_holos_flock.json", "w") as f:
        json.dump(res, f, indent=1)
