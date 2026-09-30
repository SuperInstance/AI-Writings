"""Shared stdlib helpers for labs/encoding-experiments.

Everything here is deterministic and offline except `embed()` / `chat()`, which
call DeepInfra and cache every response under data/ so reruns cost nothing.
"""
from __future__ import annotations
import gzip, hashlib, json, math, os, struct, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# ---- fnv1a-64 (the fleet idiom: offset 0xcbf29ce484222325, prime 0x100000001b3)
FNV_OFFSET, FNV_PRIME, MASK64 = 0xcbf29ce484222325, 0x100000001b3, (1 << 64) - 1


def fnv1a64(b: bytes | str) -> int:
    if isinstance(b, str):
        b = b.encode()
    h = FNV_OFFSET
    for x in b:
        h = ((h ^ x) * FNV_PRIME) & MASK64
    return h


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


# ---- zigzag + LEB128 varint (delta-encode's `zigzag` + `vdelta`)
def zigzag(n: int) -> int:
    return (n << 1) ^ (n >> 63) if -(1 << 63) <= n < (1 << 63) else (n << 1 if n >= 0 else ((-n) << 1) - 1)


def unzigzag(z: int) -> int:
    return (z >> 1) ^ -(z & 1)


def varint(u: int) -> bytes:
    out = bytearray()
    while True:
        b = u & 0x7F
        u >>= 7
        if u:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def read_varint(buf: bytes, i: int) -> tuple[int, int]:
    shift = val = 0
    while True:
        b = buf[i]
        i += 1
        val |= (b & 0x7F) << shift
        if not b & 0x80:
            return val, i
        shift += 7


# ---- deterministic PRNG (xorshift64*, so every experiment is reproducible)
class Rng:
    def __init__(self, seed: int):
        self.s = (seed * 0x9E3779B97F4A7C15 + 1) & MASK64 or 1

    def u64(self) -> int:
        s = self.s
        s ^= s >> 12; s ^= (s << 25) & MASK64; s ^= s >> 27
        self.s = s
        return (s * 0x2545F4914F6CDD1D) & MASK64

    def random(self) -> float:
        return (self.u64() >> 11) / float(1 << 53)

    def randint(self, a: int, b: int) -> int:
        return a + self.u64() % (b - a + 1)

    def gauss(self) -> float:
        u1 = self.random() or 1e-12
        return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * self.random())

    def choice(self, xs):
        return xs[self.u64() % len(xs)]


# ---- corpus + embeddings (built once by build_corpus.py, committed under data/)
def load_corpus() -> list[dict]:
    with open(os.path.join(DATA, "corpus.jsonl"), encoding="utf-8") as f:
        return [json.loads(l) for l in f]


def load_embeddings(name="minilm") -> list[list[float]]:
    """float16-packed, gzip'd: header {n,d} then n*d halfs. Ground truth uses these exact values."""
    with gzip.open(os.path.join(DATA, f"emb_{name}.f16.gz"), "rb") as f:
        raw = f.read()
    n, d = struct.unpack("<II", raw[:8])
    flat = struct.unpack("<%de" % (n * d), raw[8:])
    return [list(flat[i * d:(i + 1) * d]) for i in range(n)]


def save_embeddings(vecs, name="minilm"):
    n, d = len(vecs), len(vecs[0])
    raw = struct.pack("<II", n, d) + struct.pack("<%de" % (n * d), *[x for v in vecs for x in v])
    with open(os.path.join(DATA, f"emb_{name}.f16.gz"), "wb") as f:
        f.write(gzip.compress(raw, mtime=0))


# ---- vector helpers
def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(a):
    return math.sqrt(dot(a, a))


def unit(a):
    n = norm(a) or 1.0
    return [x / n for x in a]


def topk(scores, k):
    return [i for i, _ in sorted(enumerate(scores), key=lambda t: -t[1])[:k]]


# ---- DeepInfra (cached). Never called by selftests.
DI = "https://api.deepinfra.com/v1/openai"


def _post(path, payload):
    req = urllib.request.Request(DI + path, data=json.dumps(payload).encode(),
                                 headers={"Authorization": "Bearer " + os.environ["DEEPINFRA_KEY"],
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def _cache_path(kind):
    return os.path.join(DATA, f"cache_{kind}.jsonl")


def _cache_get(kind, key):
    p = _cache_path(kind)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for line in f:
                row = json.loads(line)
                if row["k"] == key:
                    return row["v"]
    return None


def _cache_put(kind, key, val):
    with open(_cache_path(kind), "a", encoding="utf-8") as f:
        f.write(json.dumps({"k": key, "v": val}, ensure_ascii=False) + "\n")


def chat(prompt, model="meta-llama/Meta-Llama-3.1-8B-Instruct", max_tokens=400, temperature=0.0):
    key = hashlib.sha256(canon([model, prompt, max_tokens, temperature]).encode()).hexdigest()[:24]
    hit = _cache_get("chat", key)
    if hit is not None:
        return hit
    d = _post("/chat/completions", {"model": model, "messages": [{"role": "user", "content": prompt}],
                                    "max_tokens": max_tokens, "temperature": temperature})
    out = {"text": d["choices"][0]["message"]["content"], "usage": d.get("usage", {})}
    _cache_put("chat", key, out)
    return out


def embed_batch(texts, model="sentence-transformers/all-MiniLM-L6-v2"):
    return [r["embedding"] for r in _post("/embeddings", {"model": model, "input": texts})["data"]]


class Checks:
    """Tiny selftest harness: `c.ok(cond, label)`, then `c.report(name)`."""

    def __init__(self):
        self.n = self.fail = 0

    def ok(self, cond, label):
        self.n += 1
        if not cond:
            self.fail += 1
            print("  FAIL:", label)

    def report(self, name):
        print(f"{name} selftest: {self.n} checks, {self.fail} failures")
        return self.fail == 0
