"""code-real-quant: a TurboQuant index whose compression is measured, not nominal.

Two retrieval paths over the same added vectors:
  FloatIndex  - keeps the float vector on each cell, exact L2 (what the turbovec family does today).
  CodeIndex   - keeps ONLY packed 4-bit codes on each cell; ranks by asymmetric distance (ADC):
                float rotated query vs. each stored code's dequantized centroid.

Stdlib only, offline, deterministic (xorshift64, seed 42). Cells carry an fnv1a-64 prev_hash chain.
"""
import math
from array import array

FNV_OFFSET = 0xcbf29ce484222325
FNV_PRIME = 0x100000001b3
GENESIS = 0x0000000000000000
MASK64 = (1 << 64) - 1
SEED = 42
LEVELS = 16


def fnv1a64(data, h=FNV_OFFSET):
    for b in data:
        h = ((h ^ b) * FNV_PRIME) & MASK64
    return h


class XorShift64:
    def __init__(self, seed=SEED):
        self.s = seed & MASK64 or 1

    def next_u64(self):
        x = self.s
        x ^= (x << 13) & MASK64
        x ^= x >> 7
        x ^= (x << 17) & MASK64
        self.s = x
        return x

    def uniform(self):  # (0, 1)
        return ((self.next_u64() >> 11) + 0.5) / (1 << 53)

    def gauss(self):  # Box-Muller
        u1, u2 = self.uniform(), self.uniform()
        return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def lloyd_max_gaussian(levels=LEVELS, iters=300):
    """Lloyd-Max centroids for N(0,1), computed (not copied). Returns a sorted list."""
    pdf = lambda x: math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)
    cdf = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    c = [-3.0 + 6.0 * (i + 0.5) / levels for i in range(levels)]
    for _ in range(iters):
        b = [-math.inf] + [(c[i] + c[i + 1]) / 2 for i in range(levels - 1)] + [math.inf]
        for i in range(levels):
            lo, hi = b[i], b[i + 1]
            plo = 0.0 if lo == -math.inf else pdf(lo)
            phi = 0.0 if hi == math.inf else pdf(hi)
            mass = cdf(hi) - cdf(lo)
            c[i] = (plo - phi) / mass
    return c


CENTROIDS = lloyd_max_gaussian()


def make_rotation(dim, seed=SEED):
    """Orthonormal matrix: Gram-Schmidt over xorshift-seeded Gaussian rows."""
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


def _normalize(v):
    n = math.sqrt(sum(x * x for x in v))
    if n == 0:
        raise ValueError("zero vector")
    return [x / n for x in v]


def _nearest(x):
    best, bi = 1e30, 0
    for i, c in enumerate(CENTROIDS):
        d = (x - c) ** 2
        if d < best:
            best, bi = d, i
    return bi


def pack_codes(codes):
    if len(codes) % 2:
        codes = list(codes) + [0]
    return bytes((codes[i] << 4) | codes[i + 1] for i in range(0, len(codes), 2))


def unpack_codes(buf, dim):
    out = []
    for b in buf:
        out.append(b >> 4)
        out.append(b & 15)
    return out[:dim]


class Cell:
    """One chained entry. `payload` is bytes: float32 vector (float path) or packed codes (code path)."""
    __slots__ = ("cell_id", "kind", "payload", "prev_hash", "hash")

    def __init__(self, cell_id, kind, payload, prev_hash):
        self.cell_id, self.kind, self.payload, self.prev_hash = cell_id, kind, payload, prev_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        h = fnv1a64(self.cell_id.encode() + b"|" + self.kind.encode() + b"|")
        h = fnv1a64(self.payload, h)
        return fnv1a64(self.prev_hash.to_bytes(8, "big"), h)

    def nbytes(self):
        """Bytes this cell holds as data: payload + two 8-byte hashes (id/kind strings excluded, equal on both paths)."""
        return len(self.payload) + 16


class _Base:
    kind = "vec"

    def __init__(self, dim=64, seed=SEED):
        self.dim, self.cells, self.rot = dim, [], make_rotation(dim, seed)
        self.scale = math.sqrt(dim)  # unit vector -> rotated coords ~ N(0,1), the Lloyd-Max domain

    def _rotate(self, v):
        v = _normalize(v)
        return [self.scale * sum(a * b for a, b in zip(r, v)) for r in self.rot]

    def _link(self, cell_id, payload):
        prev = self.cells[-1].hash if self.cells else GENESIS
        self.cells.append(Cell(cell_id, self.kind, payload, prev))

    def verify_chain(self):
        prev = GENESIS
        for c in self.cells:
            if c.prev_hash != prev or c.hash != c.compute_hash():
                return False
            prev = c.hash
        return True

    def bytes_per_cell(self):
        return sum(c.nbytes() for c in self.cells) / len(self.cells)

    def vector_bytes_per_cell(self):
        return sum(len(c.payload) for c in self.cells) / len(self.cells)


class FloatIndex(_Base):
    """Baseline: full float32 vector per cell (float32 is generous; Python floats are 8 bytes)."""
    kind = "vec-float"

    def add(self, cell_id, vec):
        self._link(cell_id, array("f", _normalize(vec)).tobytes())

    def search(self, query, k=10):
        q = _normalize(query)
        scored = []
        for c in self.cells:
            v = array("f")
            v.frombytes(c.payload)
            scored.append((sum((a - b) ** 2 for a, b in zip(q, v)), c.cell_id))
        scored.sort()
        return scored[:k]


class CodeIndex(_Base):
    """Codes only: rotate, quantize to 4 bits, pack, and discard the float vector."""
    kind = "vec-code4"

    def add(self, cell_id, vec):
        codes = [_nearest(x) for x in self._rotate(vec)]
        self._link(cell_id, pack_codes(codes))

    def search(self, query, k=10):
        qr = self._rotate(query)
        table = [[(x - c) ** 2 for c in CENTROIDS] for x in qr]  # ADC lookup: query coord x centroid
        scored = []
        for c in self.cells:
            codes = unpack_codes(c.payload, self.dim)
            scored.append((sum(table[i][codes[i]] for i in range(self.dim)), c.cell_id))
        scored.sort()
        return scored[:k]


def synthetic(n, dim, seed):
    rng = XorShift64(seed)
    return [[rng.gauss() for _ in range(dim)] for _ in range(n)]


def measure(n=2000, m=50, dim=64, k=10, data_seed=7, query_seed=1234):
    """Build both indexes over the same n vectors; return recall@k and bytes/cell."""
    data, queries = synthetic(n, dim, data_seed), synthetic(m, dim, query_seed)
    fi, ci = FloatIndex(dim), CodeIndex(dim)
    for i, v in enumerate(data):
        fi.add("v%d" % i, v)
        ci.add("v%d" % i, v)
    hits = 0
    for q in queries:
        truth = {cid for _, cid in fi.search(q, k)}
        got = {cid for _, cid in ci.search(q, k)}
        hits += len(truth & got)
    return {
        "n": n, "m": m, "dim": dim, "k": k,
        "recall_at_k": hits / (m * k),
        "float_vec_bytes": fi.vector_bytes_per_cell(), "code_vec_bytes": ci.vector_bytes_per_cell(),
        "float_cell_bytes": fi.bytes_per_cell(), "code_cell_bytes": ci.bytes_per_cell(),
    }


if __name__ == "__main__":
    r = measure()
    print("n=%(n)d queries=%(m)d dim=%(dim)d k=%(k)d" % r)
    print("recall@%d           : %.4f" % (r["k"], r["recall_at_k"]))
    print("vector bytes/cell  : float %.0f  code %.0f  (%.2fx)" % (
        r["float_vec_bytes"], r["code_vec_bytes"], r["float_vec_bytes"] / r["code_vec_bytes"]))
    print("total bytes/cell   : float %.0f  code %.0f  (%.2fx)" % (
        r["float_cell_bytes"], r["code_cell_bytes"], r["float_cell_bytes"] / r["code_cell_bytes"]))
