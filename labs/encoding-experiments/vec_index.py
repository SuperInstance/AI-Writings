"""E3 vec_index — which compressed vector substrate keeps retrieval? (turbovec vs HDC vs ternary)

Corpus: 480 real paragraphs from this repo, embedded with all-MiniLM-L6-v2 (384-d,
DeepInfra, cached in data/). Queries: the first 60 docs, leave-one-out. Ground truth:
exact cosine top-10 on the stored float16 vectors. Every method is scored by recall@10
against that ground truth, with its measured bytes per stored vector.

Methods
  float            exact cosine, 384 x float32                          (1536 B)
  tv-asis          turbovec-substrate as written: its own rotation, its
                   unscaled LLOYD_MAX_4BIT table, ranked by code-match count
                   (its search() ranks by the stored FLOAT vector, so this
                   is the only compressed signal it actually keeps)      (192 B)
  tq4 / tq2        TurboQuant done carefully: exactly-orthonormal rotation
                   (two rounds of sign-flip + block Walsh-Hadamard), Lloyd-Max
                   N(0,1) centroids scaled by 1/sqrt(d), asymmetric scoring (192 / 96 B)
  tern             ternary {-1,0,+1} of rotated coords, packed 5 trits/byte
                   (ternary-compression), asymmetric scoring              (77 B)
  sign1            1 bit/coord of the rotated vector, asymmetric         (48 B)
  hdc1024          flux-hdc style 1024-bit hypervector (random-hyperplane
                   sign bits), Hamming similarity                         (128 B)
  hdc-fold-xor     1024 -> 128 bits by XOR-folding 8 chunks               (16 B)
  hdc-fold-sub     1024 -> 128 bits by keeping 1 bit in 8                (16 B)
  hdc128           a native 128-bit hypervector (same bytes as the folds)  (16 B)

Run: python3 vec_index.py            (measure; ~1-2 min, pure python, offline)
     python3 vec_index.py --selftest (fast property checks on synthetic data)
"""
from __future__ import annotations
import math, sys, time
import common as C

LLOYD_MAX_4BIT_TV = [-2.79, -2.05, -1.40, -0.88, -0.44, -0.06, 0.34, 0.77,
                     1.22, 1.68, 2.16, 2.69, 3.26, 3.89, 4.62, 5.50]  # turbovec-substrate, verbatim
# Lloyd-Max optimal levels for N(0,1) (Max 1960), symmetric
LM4 = [0.1284, 0.3881, 0.6568, 0.9424, 1.2562, 1.6181, 2.0690, 2.7326]
LM4 = [-x for x in reversed(LM4)] + LM4
LM2 = [-1.5104, -0.4528, 0.4528, 1.5104]


# ---------------- turbovec-substrate, reproduced verbatim (rotation + quantize) ----------
def tv_rotation(dim, seed=42):
    state = seed

    def rand():
        nonlocal state
        state ^= (state << 13) & 0xFFFFFFFFFFFFFFFF
        state ^= (state >> 7) & 0xFFFFFFFFFFFFFFFF
        state ^= (state << 17) & 0xFFFFFFFFFFFFFFFF
        return state

    def gauss():
        u1 = (rand() & 0xFFFFFF) / 0xFFFFFF + 1e-10
        u2 = (rand() & 0xFFFFFF) / 0xFFFFFF
        return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)

    m = [[gauss() for _ in range(dim)] for _ in range(dim)]
    for i in range(dim):  # normalise THEN orthogonalise, as written upstream
        n = math.sqrt(sum(x * x for x in m[i]))
        m[i] = [x / n for x in m[i]]
        for k in range(i):
            d = C.dot(m[i], m[k])
            mk = m[k]
            m[i] = [a - d * b for a, b in zip(m[i], mk)]
    return m


def matvec(m, v):
    return [C.dot(row, v) for row in m]


def nearest(levels, x):
    # levels sorted ascending; binary search
    lo, hi = 0, len(levels) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if levels[mid] <= x:
            lo = mid
        else:
            hi = mid
    return lo if abs(levels[lo] - x) <= abs(levels[hi] - x) else hi


# ---------------- exactly-orthonormal fast rotation ----------------------------------------
def fwht(a):
    h, n = 1, len(a)
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j], a[j + h] = x + y, x - y
        h *= 2
    return a


class Rotation:
    """x -> P2 . S2 . H . P1 . S1 . H . P0 . S0 x  with H = block-diag Walsh-Hadamard (blocks of
    `blk`), S = random +-1 diagonal, P = random permutation. Every factor is orthonormal."""

    def __init__(self, d, seed=7, blk=128, rounds=3):
        assert d % blk == 0
        r = C.Rng(seed)
        self.d, self.blk, self.rounds = d, blk, rounds
        self.signs = [[1 if r.random() < 0.5 else -1 for _ in range(d)] for _ in range(rounds)]
        self.perms = []
        for _ in range(rounds):
            p = list(range(d))
            for i in range(d - 1, 0, -1):
                j = r.randint(0, i)
                p[i], p[j] = p[j], p[i]
            self.perms.append(p)
        self.scale = 1 / math.sqrt(blk)

    def __call__(self, x):
        v = list(x)
        for s, p in zip(self.signs, self.perms):
            v = [v[i] * s[i] for i in range(self.d)]
            out = []
            for b in range(0, self.d, self.blk):
                out += fwht(v[b:b + self.blk])
            v = [out[p[i]] * self.scale for i in range(self.d)]
        return v


# ---------------- encoders -----------------------------------------------------------------
def pack_trits(ts):
    """ternary-compression: 5 trits per byte (3^5 = 243 <= 256)."""
    out = bytearray()
    for i in range(0, len(ts), 5):
        b = 0
        for k, t in enumerate(ts[i:i + 5]):
            b += (t + 1) * 3 ** k
        out.append(b)
    return bytes(out)


def unpack_trits(bs, n):
    ts = []
    for b in bs:
        for _ in range(5):
            ts.append(b % 3 - 1)
            b //= 3
    return ts[:n]


def hyperplanes(nbits, d, seed=11):
    r = C.Rng(seed)
    return [[r.gauss() for _ in range(d)] for _ in range(nbits)]


def to_bits(planes, v):
    x = 0
    for i, p in enumerate(planes):
        if C.dot(p, v) >= 0:
            x |= 1 << i
    return x


def fold_xor(x, nbits=1024, to=128):
    out, mask = 0, (1 << to) - 1
    for k in range(nbits // to):
        out ^= (x >> (k * to)) & mask
    return out


def fold_sub(x, nbits=1024, to=128):
    step, out = nbits // to, 0
    for i in range(to):
        if (x >> (i * step)) & 1:
            out |= 1 << i
    return out


def ham_sim(a, b, nbits):
    return 1 - bin(a ^ b).count("1") / nbits


# ---------------- the shootout -------------------------------------------------------------
def recall(gt, got):
    return len(set(gt) & set(got)) / len(gt)


def run(vecs, nq=60, k=10, include_asis=True, log=print):
    vecs = [C.unit(v) for v in vecs]
    n, d = len(vecs), len(vecs[0])
    qs = list(range(min(nq, n)))
    res = {}

    def score_method(name, bytes_per, sim_fn, t_enc):
        t0 = time.time()
        rs = []
        for q in qs:
            s = [sim_fn(q, j) if j != q else -1e9 for j in range(n)]
            rs.append(recall(gt[q], C.topk(s, k)))
        res[name] = {"bytes": bytes_per, "recall@10": round(sum(rs) / len(rs), 4),
                     "encode_s": round(t_enc, 2), "search_s": round(time.time() - t0, 2)}
        log(f"  {name:13s} {bytes_per:5d} B/vec  recall@10={res[name]['recall@10']:.3f}")

    gt = {q: C.topk([C.dot(vecs[q], vecs[j]) if j != q else -1e9 for j in range(n)], k) for q in qs}
    score_method("float", 4 * d, lambda q, j: C.dot(vecs[q], vecs[j]), 0.0)

    diag = {}
    if include_asis:
        t0 = time.time()
        R = tv_rotation(d)
        t_rot = time.time() - t0
        norms = [math.sqrt(C.dot(r, r)) for r in R]
        codes = [[nearest(LLOYD_MAX_4BIT_TV, x) for x in matvec(R, v)] for v in vecs]
        used = sorted({c for cs in codes for c in cs})
        diag = {"tv_rotation_build_s": round(t_rot, 1),
                "tv_row_norm_min": round(min(norms), 4), "tv_row_norm_mean": round(sum(norms) / d, 4),
                "tv_levels_used": used}
        score_method("tv-asis", d // 2, lambda q, j: sum(a == b for a, b in zip(codes[q], codes[j])),
                     time.time() - t0)

    rot = Rotation(d)
    t0 = time.time()
    rv = [rot(v) for v in vecs]
    t_r = time.time() - t0
    sd = 1 / math.sqrt(d)
    for name, levels, bits in (("tq4", LM4, 4), ("tq2", LM2, 2)):
        t0 = time.time()
        lv = [x * sd for x in levels]
        deq = [[lv[nearest(lv, x)] for x in r] for r in rv]
        score_method(name, d * bits // 8, lambda q, j, deq=deq: C.dot(rv[q], deq[j]), t_r + time.time() - t0)

    t0 = time.time()
    th = 0.6745 * sd  # zero band = the middle half of N(0, 1/d)
    packed = [pack_trits([0 if abs(x) < th else (1 if x > 0 else -1) for x in r]) for r in rv]
    tern = [unpack_trits(p, d) for p in packed]
    score_method("tern", len(packed[0]), lambda q, j: C.dot(rv[q], tern[j]), t_r + time.time() - t0)

    t0 = time.time()
    sgn = [[1 if x >= 0 else -1 for x in r] for r in rv]
    score_method("sign1", d // 8, lambda q, j: C.dot(rv[q], sgn[j]), t_r + time.time() - t0)

    t0 = time.time()
    P = hyperplanes(1024, d)
    hv = [to_bits(P, v) for v in vecs]
    t_h = time.time() - t0
    score_method("hdc1024", 128, lambda q, j: ham_sim(hv[q], hv[j], 1024), t_h)
    fx = [fold_xor(x) for x in hv]
    score_method("hdc-fold-xor", 16, lambda q, j: ham_sim(fx[q], fx[j], 128), t_h)
    fs = [fold_sub(x) for x in hv]
    score_method("hdc-fold-sub", 16, lambda q, j: ham_sim(fs[q], fs[j], 128), t_h)
    h128 = [x & ((1 << 128) - 1) for x in hv]  # the first 128 planes = an independent 128-bit HV
    score_method("hdc128", 16, lambda q, j: ham_sim(h128[q], h128[j], 128), t_h)
    return res, diag


def selftest():
    c = C.Checks()
    r = C.Rng(3)
    # rotation is exactly orthonormal: preserves norms and dot products
    rot = Rotation(256, seed=1, blk=128)
    a = [r.gauss() for _ in range(256)]
    b = [r.gauss() for _ in range(256)]
    c.ok(abs(C.dot(rot(a), rot(b)) - C.dot(a, b)) < 1e-9, "rotation preserves dot")
    c.ok(abs(C.norm(rot(a)) - C.norm(a)) < 1e-9, "rotation preserves norm")
    # trit packing round-trips and hits 1.6 bits/trit
    ts = [r.randint(-1, 1) for _ in range(385)]
    p = pack_trits(ts)
    c.ok(unpack_trits(p, 385) == ts, "trit pack round-trip")
    c.ok(len(p) == 77, "5 trits/byte")
    # folds keep 128 bits
    x = r.u64() | (r.u64() << 64) | (r.u64() << 128) | (r.u64() << 192)
    c.ok(fold_xor(x, 256, 128) == (x & ((1 << 128) - 1)) ^ (x >> 128), "xor fold")
    c.ok(fold_sub(x, 256, 128) < (1 << 128), "sub fold width")
    # turbovec-as-written rotation is NOT orthonormal (rows shrink after Gram-Schmidt)
    R = tv_rotation(32)
    norms = [C.norm(row) for row in R]
    c.ok(min(norms) < 0.99, "tv rotation rows are not unit-norm (upstream scar reproduced)")
    # nearest() agrees with brute force
    for _ in range(50):
        v = r.gauss() * 2
        c.ok(nearest(LM4, v) == min(range(16), key=lambda i: abs(LM4[i] - v)), "nearest level")
    # tiny end-to-end: clustered synthetic vectors, exact method has recall 1, tq4 high
    cent = [[r.gauss() for _ in range(128)] for _ in range(8)]
    vecs = [[x + 0.3 * r.gauss() for x in cent[i % 8]] for i in range(64)]
    res, _ = run(vecs, nq=16, include_asis=False, log=lambda *a: None)
    c.ok(res["float"]["recall@10"] == 1.0, "float is ground truth")
    c.ok(res["tq4"]["recall@10"] >= 0.8, "tq4 keeps recall on clustered data")
    c.ok(res["hdc-fold-sub"]["bytes"] == 16, "fold bytes")
    return c.report("vec_index")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    vecs = C.load_embeddings()
    print(f"E3 vec_index: {len(vecs)} x {len(vecs[0])}-d MiniLM vectors, 60 queries, recall@10 vs exact cosine")
    res, diag = run(vecs)
    print("diagnostics (turbovec-substrate as written):", diag)
    import json
    with open(C.DATA + "/../results_vec_index.json", "w") as f:
        json.dump({"results": res, "diag": diag}, f, indent=1)
