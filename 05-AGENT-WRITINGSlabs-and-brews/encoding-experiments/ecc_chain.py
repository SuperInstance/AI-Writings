"""E2 ecc_chain — can the hash chain SURVIVE noise, not just notice it?

Gems: lau-error-correcting-codes / ecc-rs (Hamming, Reed-Solomon over GF(2^8), CRC),
ternary-codes (repetition / parity). Target: the ActiveLog sha256 prev-chain (B1).

A hash chain is a perfect DETECTOR and a useless CORRECTOR: one flipped bit anywhere
makes verify_chain() false and there is no way back. This experiment wraps a log in
classical codes and measures, under bit-flip and burst noise, what fraction of trials
come back byte-exact with the chain verifying, and at what byte overhead.

Payloads:  jsonl-200   200 ActiveLog records as canonical JSONL (B1 emitter)
           ctx-lzma    the SAME 200 records in E1's col-ctx+lzma form (much smaller)
Schemes:   none | crc32-per-4KB (detect+locate) | hamming74 (bit-level) |
           rs255/223 interleaved (byte-level, fixes 16 bad bytes per 255-byte block)

Run: python3 ecc_chain.py [--selftest]
"""
from __future__ import annotations
import lzma, sys, zlib
import common as C
import delta_budget as E1

# ---------------- GF(2^8) Reed-Solomon (primitive poly 0x11d), systematic ---------------
EXP, LOG = [0] * 512, [0] * 256
_x = 1
for _i in range(255):
    EXP[_i] = _x
    LOG[_x] = _i
    _x <<= 1
    if _x & 0x100:
        _x ^= 0x11D
for _i in range(255, 512):
    EXP[_i] = EXP[_i - 255]


def gmul(a, b):
    return 0 if a == 0 or b == 0 else EXP[LOG[a] + LOG[b]]


def gdiv(a, b):
    return 0 if a == 0 else EXP[(LOG[a] + 255 - LOG[b]) % 255]


def ginv(a):
    return EXP[255 - LOG[a]]


def pmul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for j, qj in enumerate(q):
        for i, pi in enumerate(p):
            r[i + j] ^= gmul(pi, qj)
    return r


def peval(p, x):
    y = p[0]
    for c in p[1:]:
        y = gmul(y, x) ^ c
    return y


def generator(nsym):
    g = [1]
    for i in range(nsym):
        g = pmul(g, [1, EXP[i]])
    return g


_GEN = {}


def rs_encode(msg, nsym=32):
    g = _GEN.setdefault(nsym, generator(nsym))
    buf = list(msg) + [0] * nsym
    for i in range(len(msg)):
        c = buf[i]
        if c:
            for j in range(1, len(g)):
                buf[i + j] ^= gmul(g[j], c)
    return bytes(msg) + bytes(buf[len(msg):])


def gpow(x, p):
    return EXP[(LOG[x] * p) % 255]


def padd(p, q):
    r = [0] * max(len(p), len(q))
    for i, c in enumerate(p):
        r[i + len(r) - len(p)] = c
    for i, c in enumerate(q):
        r[i + len(r) - len(q)] ^= c
    return r


def pscale(p, x):
    return [gmul(c, x) for c in p]


def pdiv(dividend, divisor):
    out = list(dividend)
    for i in range(len(dividend) - (len(divisor) - 1)):
        c = out[i]
        if c:
            for j in range(1, len(divisor)):
                if divisor[j]:
                    out[i + j] ^= gmul(divisor[j], c)
    sep = -(len(divisor) - 1)
    return out[:sep], out[sep:]


def syndromes(cw, nsym):
    return [0] + [peval(cw, gpow(2, i)) for i in range(nsym)]


def find_error_locator(synd, nsym):
    err, old = [1], [1]
    shift = len(synd) - nsym
    for i in range(nsym):
        K = i + shift
        delta = synd[K]
        for j in range(1, len(err)):
            delta ^= gmul(err[-(j + 1)], synd[K - j])
        old = old + [0]
        if delta:
            if len(old) > len(err):
                new = pscale(old, delta)
                old = pscale(err, ginv(delta))
                err = new
            err = padd(err, pscale(old, delta))
    while err and err[0] == 0:
        err.pop(0)
    if (len(err) - 1) * 2 > nsym:
        raise ValueError("too many errors")
    return err


def find_errors(err_loc, nmess):
    pos = [nmess - 1 - i for i in range(nmess) if peval(err_loc, gpow(2, i)) == 0]
    if len(pos) != len(err_loc) - 1:
        raise ValueError("locator roots mismatch")
    return pos


def correct_errata(msg, synd, err_pos):
    coef_pos = [len(msg) - 1 - p for p in err_pos]
    loc = [1]
    for i in coef_pos:
        loc = pmul(loc, padd([1], [gpow(2, i), 0]))
    _, rem = pdiv(pmul(synd[::-1], loc), [1] + [0] * len(loc))
    err_eval = rem[::-1]
    X = [gpow(2, -(255 - c)) for c in coef_pos]
    E = [0] * len(msg)
    for i, Xi in enumerate(X):
        Xi_inv = ginv(Xi)
        den = 1
        for j, Xj in enumerate(X):
            if j != i:
                den = gmul(den, 1 ^ gmul(Xi_inv, Xj))
        y = gmul(Xi, peval(err_eval[::-1], Xi_inv))
        E[err_pos[i]] = gdiv(y, den)
    return padd(msg, E)


def rs_decode(cw, nsym=32):
    """Return (message bytes, n_corrected) or raise ValueError if uncorrectable."""
    cw = list(cw)
    synd = syndromes(cw, nsym)
    if max(synd) == 0:
        return bytes(cw[:-nsym]), 0
    err_loc = find_error_locator(synd, nsym)
    pos = find_errors(err_loc[::-1], len(cw))
    cw = correct_errata(cw, synd, pos)
    if max(syndromes(cw, nsym)) != 0:
        raise ValueError("decode failed")
    return bytes(cw[:-nsym]), len(pos)


def rs_wrap(data, k=223, nsym=32, depth=8):
    """Block RS with byte interleaving of `depth` codewords (spreads a burst across blocks)."""
    blocks = [rs_encode(data[i:i + k].ljust(k, b"\0"), nsym) for i in range(0, len(data), k)]
    while len(blocks) % depth:
        blocks.append(rs_encode(bytes(k), nsym))
    out = bytearray()
    for g in range(0, len(blocks), depth):
        grp = blocks[g:g + depth]
        for j in range(k + nsym):
            out += bytes(b[j] for b in grp)
    return C.varint(len(data)) + bytes(out)


def rs_unwrap(buf, k=223, nsym=32, depth=8):
    n, i = C.read_varint(buf, 0)
    body = buf[i:]
    L = k + nsym
    out = bytearray()
    for g in range(0, len(body), L * depth):
        chunk = body[g:g + L * depth]
        for d in range(depth):
            msg, _ = rs_decode(bytes(chunk[j * depth + d] for j in range(L)), nsym)
            out += msg
    return bytes(out[:n])


# ---------------- Hamming(7,4) ---------------------------------------------------------------
def h74_enc_nib(d):
    d1, d2, d3, d4 = (d >> 3) & 1, (d >> 2) & 1, (d >> 1) & 1, d & 1
    p1, p2, p3 = d1 ^ d2 ^ d4, d1 ^ d3 ^ d4, d2 ^ d3 ^ d4
    return (p1 << 6) | (p2 << 5) | (d1 << 4) | (p3 << 3) | (d2 << 2) | (d3 << 1) | d4


def h74_dec(c):
    b = [(c >> (6 - i)) & 1 for i in range(7)]  # positions 1..7
    s = (b[0] ^ b[2] ^ b[4] ^ b[6]) | ((b[1] ^ b[2] ^ b[5] ^ b[6]) << 1) | ((b[3] ^ b[4] ^ b[5] ^ b[6]) << 2)
    if s:
        b[s - 1] ^= 1
    return (b[2] << 3) | (b[4] << 2) | (b[5] << 1) | b[6]


def ham_wrap(data):  # one 7-bit codeword per byte of output (simple, 2 per data byte)
    return C.varint(len(data)) + bytes(h74_enc_nib(x) for byte in data for x in (byte >> 4, byte & 15))


def ham_unwrap(buf):
    n, i = C.read_varint(buf, 0)
    body = buf[i:]
    return bytes((h74_dec(body[2 * j] & 0x7F) << 4) | h74_dec(body[2 * j + 1] & 0x7F) for j in range(n))


def crc_wrap(data, blk=4096):
    out = bytearray(C.varint(len(data)))
    for i in range(0, len(data), blk):
        b = data[i:i + blk]
        out += b + zlib.crc32(b).to_bytes(4, "big")
    return bytes(out)


def crc_unwrap(buf, blk=4096):
    n, i = C.read_varint(buf, 0)
    out = bytearray()
    while len(out) < n:
        b = buf[i:i + min(blk, n - len(out))]
        i += len(b)
        if zlib.crc32(b).to_bytes(4, "big") != buf[i:i + 4]:
            raise ValueError("crc mismatch at block %d" % (len(out) // blk))
        i += 4
        out += b
    return bytes(out)


SCHEMES = {
    "none": (lambda d: d, lambda b: b),
    "crc32/4KB": (crc_wrap, crc_unwrap),
    "hamming74": (ham_wrap, ham_unwrap),
    "rs255/223x8": (rs_wrap, rs_unwrap),
}


# ---------------- noise ----------------------------------------------------------------------------
def bitflips(buf, ber, r, protect_header=4):
    b = bytearray(buf)
    nbits = (len(b) - protect_header) * 8
    k = 0
    # geometric skipping: flip each bit with prob `ber`
    import math
    pos = -1
    while True:
        u = r.random() or 1e-12
        pos += 1 + int(math.log(u) / math.log(1 - ber))
        if pos >= nbits:
            return bytes(b), k
        b[protect_header + pos // 8] ^= 1 << (pos % 8)
        k += 1


def burst(buf, nbytes, r, protect_header=4):
    b = bytearray(buf)
    s = r.randint(protect_header, len(b) - nbytes - 1)
    for i in range(s, s + nbytes):
        b[i] = r.randint(0, 255)
    return bytes(b)


def payloads(n=200):
    recs = E1.build_log(n, seed=7)
    jsonl = "".join(E1.AL.canon(r) + "\n" for r in recs).encode()
    ctx = lzma.compress(E1.encode(E1.to_cols(recs), "ctx"), preset=9)
    return recs, {"jsonl-200": jsonl, "ctx-lzma": ctx}


def restore(name, data):
    """Payload bytes -> records (raises on any decode failure)."""
    if name == "jsonl-200":
        import json
        return [json.loads(l) for l in data.decode().splitlines()]
    return E1.from_cols(E1.decode(lzma.decompress(data), "ctx"))


def trial(recs, name, data, scheme, noise, r):
    enc, dec = SCHEMES[scheme]
    wire = enc(data)
    noisy = bitflips(wire, noise[1], r)[0] if noise[0] == "ber" else burst(wire, noise[1], r)
    try:
        back = restore(name, dec(noisy))
    except Exception:
        return "detected"
    if E1.AL.canon(back) == E1.AL.canon(recs):
        return "recovered"
    return "detected" if not E1.AL.verify_chain(back) else "SILENT"


def measure(trials=12, log=print):
    recs, pls = payloads()
    r = C.Rng(99)
    noises = [("ber", 1e-5), ("ber", 1e-4), ("ber", 1e-3), ("burst", 64), ("burst", 512)]
    res = {}
    for name, data in pls.items():
        for scheme in SCHEMES:
            wire = SCHEMES[scheme][0](data)
            row = {"bytes": len(wire), "overhead": round(len(wire) / len(data) - 1, 3)}
            for nz in noises:
                outs = [trial(recs, name, data, scheme, nz, r) for _ in range(trials)]
                row["%s=%g" % nz] = {o: outs.count(o) for o in set(outs)}
            res[f"{name}|{scheme}"] = row
            cells = "  ".join(f"{k}:{v.get('recovered', 0)}/{trials}" for k, v in row.items() if isinstance(v, dict))
            silent = sum(v.get("SILENT", 0) for v in row.values() if isinstance(v, dict))
            log(f"  {name:9s} {scheme:12s} {len(wire):7d} B (+{row['overhead']:.0%})  recovered  {cells}  silent={silent}")
    return res


def selftest():
    c = C.Checks()
    r = C.Rng(1)
    msg = bytes(r.randint(0, 255) for _ in range(223))
    cw = rs_encode(msg)
    c.ok(len(cw) == 255, "rs length")
    c.ok(rs_decode(cw)[0] == msg, "rs clean decode")
    for nerr in (1, 5, 16):
        bad = bytearray(cw)
        for p in sorted({r.randint(0, 254) for _ in range(nerr * 3)})[:nerr]:
            bad[p] ^= r.randint(1, 255)
        out, k = rs_decode(bytes(bad))
        c.ok(out == msg, f"rs corrects {nerr} byte errors")
    bad = bytearray(cw)
    for p in range(0, 17 * 15, 15):
        bad[p] ^= 0x5A
    try:
        out, _ = rs_decode(bytes(bad))
        c.ok(out != msg or True, "rs 17 errors: no crash")
    except ValueError:
        c.ok(True, "rs 17 errors: refused")
    data = bytes(r.randint(0, 255) for _ in range(3000))
    c.ok(rs_unwrap(rs_wrap(data)) == data, "rs wrap round-trip")
    w = bytearray(rs_wrap(data))
    for i in range(100, 100 + 120):  # 120-byte burst spread over 8 interleaved blocks = 15/block
        w[i] ^= 0xFF
    c.ok(rs_unwrap(bytes(w)) == data, "interleaved RS survives a 120-byte burst")
    for nib in range(16):
        cw7 = h74_enc_nib(nib)
        c.ok(all(h74_dec(cw7 ^ (1 << b)) == nib for b in range(7)), f"hamming corrects any 1 bit ({nib})")
    c.ok(ham_unwrap(ham_wrap(data)) == data, "hamming round-trip")
    c.ok(crc_unwrap(crc_wrap(data)) == data, "crc round-trip")
    recs, pls = payloads(40)
    c.ok(E1.AL.canon(restore("ctx-lzma", pls["ctx-lzma"])) == E1.AL.canon(recs), "ctx-lzma restores records")
    c.ok(trial(recs, "ctx-lzma", pls["ctx-lzma"], "rs255/223x8", ("burst", 64), r) == "recovered", "RS saves compressed log from 64B burst")
    return c.report("ecc_chain")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    import json
    print("E2 ecc_chain: 200 ActiveLog records; outcome counts over 12 trials per cell")
    res = measure()
    with open(C.HERE + "/results_ecc_chain.json", "w") as f:
        json.dump(res, f, indent=1)
