"""code-real-quant — make TurboQuant's compression real, and measure what it costs.

Self-contained (stdlib only, offline). Mirrors the turbovec-substrate idea:
seeded Gaussian rotation -> 4-bit Lloyd-Max codes -> fnv1a-64 prev_hash chain.
Two retrieval paths over the same added vectors:
  float_search : exact L2 over the full float vectors (baseline, kept on the side)
  code_search  : asymmetric distance (ADC) over 4-bit codes only; cells hold no float.
"""
import math
import struct
import sys

FNV_OFFSET = 0xcbf29ce484222325
FNV_PRIME = 0x100000001b3
GENESIS = 0x0
MASK = (1 << 64) - 1
SEED = 42
BITS = 4
LEVELS = 1 << BITS


def fnv1a64(data, h=FNV_OFFSET):
    for b in data:
        h = ((h ^ b) * FNV_PRIME) & MASK
    return h


class XorShift64:
    def __init__(self, seed):
        self.s = (seed * 0x9E3779B97F4A7C15 + 1) & MASK or 1

    def next(self):
        x = self.s
        x ^= (x << 13) & MASK
        x ^= x >> 7
        x ^= (x << 17) & MASK
        self.s = x
        return x

    def uniform(self):  # (0,1)
        return ((self.next() >> 11) + 0.5) / (1 << 53)

    def gauss(self):
        u1, u2 = self.uniform(), self.uniform()
        return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def rotation_matrix(dim, seed=SEED):
    """Gram-Schmidt-orthonormalized Gaussian matrix, deterministic in (dim, seed)."""
    rng = XorShift64(seed)
    rows = []
    for _ in range(dim):
        v = [rng.gauss() for _ in range(dim)]
        for r in rows:
            d = sum(a * b for a, b in zip(v, r))
            v = [a - d * b for a, b in zip(v, r)]
        n = math.sqrt(sum(a * a for a in v))
        rows.append([a / n for a in v])
    return rows


def _phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def _cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def lloyd_max_gaussian(levels=LEVELS, iters=200):
    """Lloyd-Max centroids for N(0,1), computed in closed form per iteration.
    NOTE: these are the true Gaussian optimum (symmetric, about +-2.73 at the
    tails). The substrate's quoted -2.79..5.50 table is not reproduced here; the
    study gives only its endpoints."""
    c = [-3.0 + 6.0 * (i + 0.5) / levels for i in range(levels)]
    for _ in range(iters):
        b = [-math.inf] + [(c[i] + c[i + 1]) / 2 for i in range(levels - 1)] + [math.inf]
        for i in range(levels):
            lo, hi = b[i], b[i + 1]
            p = _cdf(hi) - _cdf(lo)
            if p > 1e-15:
                pl = 0.0 if lo == -math.inf else _phi(lo)
                ph = 0.0 if hi == math.inf else _phi(hi)
                c[i] = (pl - ph) / p
    return c


CENTROIDS = lloyd_max_gaussian()


def _unit_scaled(v):
    """Unit-normalize then scale by sqrt(dim) so rotated coords are ~N(0,1)."""
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    s = math.sqrt(len(v)) / n
    return [x * s for x in v]


def _matvec(R, v):
    return [sum(a * b for a, b in zip(r, v)) for r in R]


def quantize(coords):
    codes = []
    for x in coords:
        best, bd = 0, 1e300
        for i, c in enumerate(CENTROIDS):
            d = (x - c) * (x - c)
            if d < bd:
                best, bd = i, d
        codes.append(best)
    return codes


def pack(codes):
    if len(codes) % 2:
        codes = codes + [0]
    return bytes((codes[i] << 4) | codes[i + 1] for i in range(0, len(codes), 2))


def unpack(blob, dim):
    out = []
    for b in blob:
        out.append(b >> 4)
        out.append(b & 15)
    return out[:dim]


class Cell:
    """A chained cell. Holds ONLY the packed 4-bit code (no float vector)."""
    __slots__ = ("cell_id", "codes", "prev_hash", "hash")

    def __init__(self, cell_id, codes, prev_hash):
        self.cell_id = cell_id
        self.codes = codes
        self.prev_hash = prev_hash
        self.hash = fnv1a64(
            struct.pack("<QQ", cell_id, prev_hash) + codes)

    def nbytes(self):
        """Payload bytes a cell must store: id(8) + prev_hash(8) + hash(8) + codes."""
        return 24 + len(self.codes)


class CodeIndex:
    def __init__(self, dim=64, seed=SEED, keep_float=False):
        self.dim = dim
        self.R = rotation_matrix(dim, seed)
        self.cells = []
        # float baseline lives OUTSIDE the cells, only when requested (for measurement)
        self._float = [] if keep_float else None

    def add(self, vec):
        assert len(vec) == self.dim
        u = _unit_scaled(vec)
        codes = pack(quantize(_matvec(self.R, u)))
        prev = self.cells[-1].hash if self.cells else GENESIS
        cell = Cell(len(self.cells), codes, prev)
        self.cells.append(cell)
        if self._float is not None:
            self._float.append(u)
        return cell

    def verify_chain(self):
        prev = GENESIS
        for i, c in enumerate(self.cells):
            if c.cell_id != i or c.prev_hash != prev:
                return False
            if c.hash != fnv1a64(struct.pack("<QQ", c.cell_id, c.prev_hash) + c.codes):
                return False
            prev = c.hash
        return True

    def float_search(self, query, k):
        """Exact L2 over full float vectors (baseline)."""
        q = _unit_scaled(query)
        d = [(sum((a - b) ** 2 for a, b in zip(q, v)), i)
             for i, v in enumerate(self._float)]
        d.sort()
        return [i for _, i in d[:k]]

    def code_search(self, query, k):
        """ADC: float query rotated once; each cell scored via a per-dim table
        lookup of its dequantized centroid. Reads only cell.codes."""
        qr = _matvec(self.R, _unit_scaled(query))
        table = [[(x - c) ** 2 for c in CENTROIDS] for x in qr]
        d = []
        for cell in self.cells:
            codes = unpack(cell.codes, self.dim)
            d.append((sum(table[j][codes[j]] for j in range(self.dim)), cell.cell_id))
        d.sort()
        return [i for _, i in d[:k]]


def synth(n, dim, seed, clusters=20, noise=0.5):
    """Deterministic clustered Gaussian vectors."""
    rng = XorShift64(seed)
    centers = [[rng.gauss() for _ in range(dim)] for _ in range(clusters)]
    out = []
    for i in range(n):
        c = centers[rng.next() % clusters]
        out.append([x + noise * rng.gauss() for x in c])
    return out


def measure(n=2000, m=50, dim=64, k=10, data_seed=7):
    vecs = synth(n, dim, data_seed)
    idx = CodeIndex(dim, keep_float=True)
    for v in vecs:
        idx.add(v)
    rng = XorShift64(data_seed + 1)
    queries = []
    for _ in range(m):  # a stored vector plus fresh noise
        b = vecs[rng.next() % n]
        queries.append([x + 0.3 * rng.gauss() for x in b])
    hits = 0
    for q in queries:
        base = set(idx.float_search(q, k))
        hits += len(base & set(idx.code_search(q, k)))
    recall = hits / (m * k)
    float_bytes = 24 + 4 * dim  # id+prev+hash + float32 vector
    code_bytes = idx.cells[0].nbytes()
    return {"n": n, "m": m, "dim": dim, "k": k, "recall": recall,
            "float_bytes": float_bytes, "code_bytes": code_bytes,
            "vec_float": 4 * dim, "vec_code": len(idx.cells[0].codes),
            "chain_ok": idx.verify_chain()}


if __name__ == "__main__":
    dims = [int(a) for a in sys.argv[1:]] or [64, 128]
    print("dim  N     M   recall@10  bytes/cell float  code   vector-only float  code")
    for d in dims:
        r = measure(dim=d)
        print(f"{d:<4} {r['n']:<5} {r['m']:<3} {r['recall']:<10.4f} "
              f"{r['float_bytes']:<17} {r['code_bytes']:<6} {r['vec_float']:<18} {r['vec_code']}")
