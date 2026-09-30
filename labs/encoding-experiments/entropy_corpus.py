"""E9 entropy_corpus — do the classic entropy coders earn a place next to stdlib lzma/bz2?

Gems: huffman-code / compress-huffman-rs (canonical Huffman), arithmetic-code (adaptive
frequency model), lau-compression (entropy yardstick, BWT -> MTF pipeline, and an
AgentCompressor that "analyses the entropy to pick" a strategy).

Payloads (all real bytes from this repo):
  corpus     the 480-paragraph story corpus text (data/corpus.jsonl texts, 178 KB)
  activelog  2,000 ActiveLog records as canonical JSONL (E1's stream)
  emb-f16    the float16 embedding matrix (binary, near-incompressible)

Coders:
  H0 / H2          empirical order-0 / order-2 conditional entropy (the yardsticks)
  huffman0         canonical Huffman, real bitstream + 256-byte length table (round-trips)
  arith0           adaptive order-0 arithmetic coder, real bitstream (round-trips)
  ctx2-ideal       adaptive order-2 blended model, IDEAL code length (sum -log2 p); an
                   arithmetic coder lands within a few bytes of this, not implemented here
  bwt+mtf+arith0   lau-compression's pipeline: BWT -> move-to-front -> arith0 (real, round-trips)
  zlib9 / bz2-9 / lzma9   stdlib baselines

Run: python3 entropy_corpus.py [--selftest]
"""
from __future__ import annotations
import bz2, heapq, lzma, math, sys, zlib
from collections import Counter, defaultdict
import common as C


# ---------------- yardsticks --------------------------------------------------------------
def H0(b):
    n = len(b)
    return -sum(c / n * math.log2(c / n) for c in Counter(b).values())


def Hk(b, k=2):
    ctx = defaultdict(Counter)
    for i in range(k, len(b)):
        ctx[b[i - k:i]][b[i]] += 1
    n = len(b) - k
    h = 0.0
    for cnt in ctx.values():
        t = sum(cnt.values())
        h -= sum(c * math.log2(c / t) for c in cnt.values())
    return h / n


# ---------------- canonical Huffman --------------------------------------------------------
def huff_lengths(b):
    freq = Counter(b)
    if len(freq) == 1:
        return {next(iter(freq)): 1}
    heap = [(f, i, (s,)) for i, (s, f) in enumerate(sorted(freq.items()))]
    heapq.heapify(heap)
    L = Counter()
    uid = len(heap)
    while len(heap) > 1:
        f1, _, a = heapq.heappop(heap)
        f2, _, b2 = heapq.heappop(heap)
        for s in a + b2:
            L[s] += 1
        heapq.heappush(heap, (f1 + f2, uid, a + b2))
        uid += 1
    return dict(L)


def canon_codes(lengths):
    code, prev, out = 0, 0, {}
    for s, l in sorted(lengths.items(), key=lambda t: (t[1], t[0])):
        code <<= (l - prev)
        out[s] = (code, l)
        code += 1
        prev = l
    return out


def huff_encode(b):
    L = huff_lengths(b)
    codes = canon_codes(L)
    acc, nb = 0, 0
    out = bytearray(bytes(L.get(s, 0) for s in range(256)))  # length table
    out += C.varint(len(b))
    for x in b:
        c, l = codes[x]
        acc = (acc << l) | c
        nb += l
        while nb >= 8:
            nb -= 8
            out.append((acc >> nb) & 0xFF)
        acc &= (1 << nb) - 1
    if nb:
        out.append((acc << (8 - nb)) & 0xFF)
    return bytes(out)


def huff_decode(buf):
    L = {s: buf[s] for s in range(256) if buf[s]}
    dec = {(l, c): s for s, (c, l) in canon_codes(L).items()}
    n, i = C.read_varint(buf, 256)
    out = bytearray()
    code = l = 0
    while len(out) < n:
        byte = buf[i]
        i += 1
        for bit in range(7, -1, -1):
            code = (code << 1) | ((byte >> bit) & 1)
            l += 1
            s = dec.get((l, code))
            if s is not None:
                out.append(s)
                code = l = 0
                if len(out) == n:
                    break
    return bytes(out)


# ---------------- adaptive order-0 arithmetic coder (32-bit, Fenwick cumulative freqs) -----
class Fenwick:
    def __init__(self, n):
        self.n, self.t = n, [0] * (n + 1)
        for i in range(n):
            self.add(i, 1)

    def add(self, i, d):
        i += 1
        while i <= self.n:
            self.t[i] += d
            i += i & -i

    def prefix(self, i):  # sum of [0, i)
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s

    def find(self, target):  # largest i with prefix(i) <= target
        pos, bit = 0, 1 << (self.n.bit_length())
        while bit:
            nxt = pos + bit
            if nxt <= self.n and self.t[nxt] <= target:
                pos = nxt
                target -= self.t[nxt]
            bit >>= 1
        return pos


TOP, HALF, Q1, Q3 = (1 << 32) - 1, 1 << 31, 1 << 30, 3 << 30
INC, LIMIT = 24, 1 << 16


def _rescale(f, total):
    vals = [f.prefix(i + 1) - f.prefix(i) for i in range(f.n)]
    g = Fenwick(f.n)
    for i, v in enumerate(vals):
        g.add(i, (v + 1) // 2 - 1)
    return g, sum((v + 1) // 2 for v in vals)


def arith_encode(b):
    f, total = Fenwick(256), 256
    lo, hi, pending = 0, TOP, 0
    bits = []

    def emit(bit):
        nonlocal pending
        bits.append(bit)
        bits.extend([1 - bit] * pending)
        pending = 0

    for x in b:
        r = hi - lo + 1
        cl, ch = f.prefix(x), f.prefix(x + 1)
        hi = lo + r * ch // total - 1
        lo = lo + r * cl // total
        while True:
            if hi < HALF:
                emit(0)
            elif lo >= HALF:
                emit(1)
                lo -= HALF
                hi -= HALF
            elif lo >= Q1 and hi < Q3:
                pending += 1
                lo -= Q1
                hi -= Q1
            else:
                break
            lo, hi = 2 * lo, 2 * hi + 1
        f.add(x, INC)
        total += INC
        if total > LIMIT:
            f, total = _rescale(f, total)
    pending += 1
    emit(0 if lo < Q1 else 1)
    out = bytearray(C.varint(len(b)))
    for i in range(0, len(bits), 8):
        chunk = bits[i:i + 8] + [0] * (8 - len(bits[i:i + 8]))
        out.append(int("".join(map(str, chunk)), 2))
    return bytes(out)


def arith_decode(buf):
    n, i = C.read_varint(buf, 0)
    data = buf[i:]
    nbits = len(data) * 8

    def bit(k):
        return (data[k >> 3] >> (7 - (k & 7))) & 1 if k < nbits else 0

    f, total = Fenwick(256), 256
    lo, hi, val, k = 0, TOP, 0, 0
    for _ in range(32):
        val = (val << 1) | bit(k)
        k += 1
    out = bytearray()
    for _ in range(n):
        r = hi - lo + 1
        target = ((val - lo + 1) * total - 1) // r
        x = f.find(target)
        cl, ch = f.prefix(x), f.prefix(x + 1)
        hi = lo + r * ch // total - 1
        lo = lo + r * cl // total
        while True:
            if hi < HALF:
                pass
            elif lo >= HALF:
                lo -= HALF
                hi -= HALF
                val -= HALF
            elif lo >= Q1 and hi < Q3:
                lo -= Q1
                hi -= Q1
                val -= Q1
            else:
                break
            lo, hi = 2 * lo, 2 * hi + 1
            val = (val << 1) | bit(k)
            k += 1
        out.append(x)
        f.add(x, INC)
        total += INC
        if total > LIMIT:
            f, total = _rescale(f, total)
    return bytes(out)


# ---------------- order-2 blended model, ideal code length -----------------------------------
def ctx2_ideal_bytes(b):
    c0 = Counter()
    c1 = defaultdict(Counter)
    c2 = defaultdict(Counter)
    t1, t2 = Counter(), Counter()
    bits, n0 = 0.0, 0
    for i, x in enumerate(b):
        k1 = b[i - 1] if i >= 1 else -1
        k2 = b[i - 2:i] if i >= 2 else b"--"
        p0 = (c0[x] + 0.02) / (n0 + 0.02 * 256)
        n1, n2 = t1[k1], t2[k2]
        p1 = (c1[k1][x] + 2 * p0) / (n1 + 2)
        p2 = (c2[k2][x] + 2 * p1) / (n2 + 2)  # order-2 backs off into order-1 into order-0
        bits -= math.log2(p2)
        c0[x] += 1
        n0 += 1
        c1[k1][x] += 1
        t1[k1] += 1
        c2[k2][x] += 1
        t2[k2] += 1
    return int(bits / 8) + 1


# ---------------- BWT -> MTF (lau-compression pipeline) ----------------------------------------
def suffix_array(s):
    n = len(s)
    rank = list(s)
    sa = list(range(n))
    k = 1
    while True:
        key = lambda i: (rank[i], rank[i + k] if i + k < n else -1)
        sa.sort(key=key)
        new = [0] * n
        for j in range(1, n):
            new[sa[j]] = new[sa[j - 1]] + (key(sa[j]) != key(sa[j - 1]))
        rank = new
        if rank[sa[-1]] == n - 1:
            return sa
        k *= 2


def bwt(b):
    s = list(b) + [-1]  # unique sentinel smaller than every byte
    sa = suffix_array(s)
    last, primary = bytearray(), 0
    for j, i in enumerate(sa):
        if i == 0:
            primary = j
        else:
            last.append(s[i - 1] if s[i - 1] >= 0 else 0)
    return bytes(last), primary


def ibwt(last, primary):
    n = len(last) + 1
    col = list(last[:primary]) + [-1] + list(last[primary:])
    order = sorted(range(n), key=lambda i: (col[i], i))
    out, j = bytearray(), order[primary]
    for _ in range(n - 1):
        out.append(col[j])
        j = order[j]
    return bytes(out)


def mtf(b):
    table, out = list(range(256)), bytearray()
    for x in b:
        i = table.index(x)
        out.append(i)
        table.insert(0, table.pop(i))
    return bytes(out)


def imtf(b):
    table, out = list(range(256)), bytearray()
    for i in b:
        x = table[i]
        out.append(x)
        table.insert(0, table.pop(i))
    return bytes(out)


def bwt_pipeline(b):
    last, p = bwt(b)
    return C.varint(p) + arith_encode(mtf(last))


def bwt_pipeline_decode(buf):
    p, i = C.read_varint(buf, 0)
    return ibwt(imtf(arith_decode(buf[i:])), p)


# ---------------- measure ---------------------------------------------------------------------
def payloads():
    import delta_budget as E1
    import gzip, os
    corpus = "\n".join(d["text"] for d in C.load_corpus()).encode()
    recs = E1.build_log(2000)
    activelog = "".join(E1.AL.canon(r) + "\n" for r in recs).encode()
    with open(os.path.join(C.DATA, "emb_minilm.f16.gz"), "rb") as f:
        emb = gzip.decompress(f.read())[8:]
    return {"corpus": corpus, "activelog": activelog[:180000], "emb-f16": emb[:180000]}


def measure(log=print):
    res = {}
    for name, b in payloads().items():
        n = len(b)
        row = {"bytes": n, "H0_bpb": round(H0(b), 3), "H2_bpb": round(Hk(b, 2), 3)}
        hb = huff_encode(b)
        assert huff_decode(hb) == b
        ab = arith_encode(b)
        assert arith_decode(ab) == b
        row["huffman0"] = len(hb)
        row["arith0"] = len(ab)
        row["ctx2-ideal"] = ctx2_ideal_bytes(b)
        if name != "emb-f16":
            bw = bwt_pipeline(b)
            assert bwt_pipeline_decode(bw) == b
            row["bwt+mtf+arith0"] = len(bw)
        row["zlib9"] = len(zlib.compress(b, 9))
        row["bz2-9"] = len(bz2.compress(b, 9))
        row["lzma9"] = len(lzma.compress(b, preset=9))
        res[name] = row
        codecs = [k for k in row if k not in ("bytes", "H0_bpb", "H2_bpb")]
        best = min(codecs, key=lambda k: row[k])
        log(f"  {name:9s} {n:7d} B  H0={row['H0_bpb']} H2={row['H2_bpb']} bits/byte | " +
            "  ".join(f"{k}={8 * row[k] / n:.2f}" for k in codecs) + f"  (bits/byte; best: {best})")
    return res


def selftest():
    c = C.Checks()
    r = C.Rng(8)
    samples = [b"", b"a", b"abracadabra", bytes(r.randint(0, 255) for _ in range(3000)),
               b"the cat sat on the mat " * 40]
    for s in samples[1:]:
        c.ok(huff_decode(huff_encode(s)) == s, f"huffman round-trip {len(s)}")
        c.ok(arith_decode(arith_encode(s)) == s, f"arith round-trip {len(s)}")
        c.ok(ibwt(*bwt(s)) == s, f"bwt round-trip {len(s)}")
        c.ok(imtf(mtf(s)) == s, f"mtf round-trip {len(s)}")
        c.ok(bwt_pipeline_decode(bwt_pipeline(s)) == s, f"pipeline round-trip {len(s)}")
    c.ok(abs(H0(b"ab" * 50) - 1.0) < 1e-9, "H0 of fair coin = 1")
    rep = b"the cat sat on the mat " * 40
    c.ok(len(arith_encode(rep)) < len(rep) * H0(rep) / 8 * 1.1, "adaptive arith near/below H0 on repetitive text")
    c.ok(ctx2_ideal_bytes(rep) < len(arith_encode(rep)), "order-2 context beats order-0")
    return c.report("entropy_corpus")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    import json
    print("E9 entropy_corpus: bits per byte (lower is better); every real coder round-trips")
    res = measure()
    with open(C.HERE + "/results_entropy_corpus.json", "w") as f:
        json.dump(res, f, indent=1)
