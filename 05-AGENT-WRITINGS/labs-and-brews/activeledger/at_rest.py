"""at_rest — a compact, repairable at-rest format for ActiveLog runs (promoted from
labs/encoding-experiments E1 + E2; see situations/arch/ENCODING-GEMS-STUDY.md).

JSONL stays the live, append-only form. `pack()` turns a verified run into bytes that are
typically ~10x smaller than JSONL+lzma, and `unpack()` gives back records whose canonical
JSON is identical, with the sha256 prev-chain RECOMPUTED (prev hashes carry no
information, so they are not stored) and checked against a 32-byte head receipt.

Format ALR1 (schema-agnostic; any body shape the emitter accepts):
  magic "ALR1" | flags | head receipt (sha256 of the last envelope, 32 B) | lzma(streams)
  streams: dev table, per-record shape ids (a shape is the body's key/type skeleton),
  mono residuals, ts flags, numeric leaves as zigzag-varint residuals against the running
  mean of the same (shape, cell, leaf position) — the "same-cell expectation" predictor
  that E1 measured best — decimal float scales, a string table with index stream, bools.
  flag bit 0 = Reed-Solomon RS(255,223), 8-way interleaved, around the whole payload:
  corrects up to 16 bad bytes per 255-byte block (E2: 12/12 at BER 1e-3 and 64 B bursts).

ALRM (`pack_many`/`unpack_many`): many independent runs, each GENESIS-rooted, in one archive —
ONE 32-byte receipt (sha256 over every run's head hash, so any changed run fails it), a
dialect byte per run, one shared lzma context, same optional RS flag. Small runs are
where it pays: route/fixture logs of a handful of records share their strings.

Refuses to pack a run whose chain does not verify; unpack raises if the head receipt or
any structure does not match — it never returns different records silently.
"""
from __future__ import annotations

import hashlib
import json
import lzma
from struct import error as struct_error

import activeledger as AL

MAGIC = b"ALR1"
MAGIC_MANY = b"ALRM"
FLAG_RS = 1
FLAG_FNV = 2  # ALR1 only: the run uses the fnv1a-64 `hash`-field chain dialect (calculator-quilt stand-in)
FNV_GENESIS = "0x0000000000000000"


class AtRestError(ValueError):
    pass


# ---- varint / zigzag -------------------------------------------------------------------
def _uv(u: int) -> bytes:
    out = bytearray()
    while True:
        b = u & 0x7F
        u >>= 7
        out.append(b | 0x80 if u else b)
        if not u:
            return bytes(out)


def _zz(n: int) -> int:
    return n * 2 if n >= 0 else -n * 2 - 1


def _unzz(z: int) -> int:
    return z >> 1 if not z & 1 else -((z + 1) >> 1)


class _Reader:
    def __init__(self, b: bytes):
        self.b, self.i = b, 0

    def uv(self) -> int:
        shift = val = 0
        while True:
            if self.i >= len(self.b):
                raise AtRestError("truncated stream")
            x = self.b[self.i]
            self.i += 1
            val |= (x & 0x7F) << shift
            if not x & 0x80:
                return val
            shift += 7

    def take(self, n: int) -> bytes:
        if self.i + n > len(self.b):
            raise AtRestError("truncated stream")
        out = self.b[self.i:self.i + n]
        self.i += n
        return out


# ---- body shape / leaves -----------------------------------------------------------------
def _float_parts(x: float):
    """Exact decimal form of a float's repr: (scale, int) or None (-> string fallback)."""
    s = repr(x)
    if "e" in s or "n" in s or s.startswith("-0") and x == 0:
        return None
    whole, _, frac = s.partition(".")
    return len(frac), int(whole + frac)


def _flatten(obj, leaves):
    if isinstance(obj, dict):
        return "{" + ",".join(json.dumps(k) + ":" + _flatten(obj[k], leaves) for k in sorted(obj)) + "}"
    if isinstance(obj, list):
        return "[" + ",".join(_flatten(v, leaves) for v in obj) + "]"
    if obj is None:
        return "n"
    if isinstance(obj, bool):
        leaves.append(("b", obj))
        return "b"
    if isinstance(obj, int):
        leaves.append(("i", obj))
        return "i"
    if isinstance(obj, float):
        fp = _float_parts(obj)
        if fp is None:
            leaves.append(("s", repr(obj)))
            return "F"
        leaves.append(("f", fp))
        return "f"
    if isinstance(obj, str):
        leaves.append(("s", obj))
        return "s"
    raise AtRestError("unsupported JSON type %r" % type(obj))


def _parse_shape(shape: str):
    """Shape string -> template tree: ('d', [(k, t)]), ('l', [t]), or a leaf tag."""
    pos = 0

    def node():
        nonlocal pos
        c = shape[pos]
        if c == "{":
            pos += 1
            items = []
            while shape[pos] != "}":
                end = pos + 1
                while shape[end] != '"' or shape[end - 1] == "\\":
                    end += 1
                key = json.loads(shape[pos:end + 1])
                pos = end + 2  # skip closing quote and ':'
                items.append((key, node()))
                if shape[pos] == ",":
                    pos += 1
            pos += 1
            return ("d", items)
        if c == "[":
            pos += 1
            items = []
            while shape[pos] != "]":
                items.append(node())
                if shape[pos] == ",":
                    pos += 1
            pos += 1
            return ("l", items)
        pos += 1
        return c

    t = node()
    if pos != len(shape):
        raise AtRestError("bad shape")
    return t


def _build(t, it):
    if isinstance(t, tuple):
        if t[0] == "d":
            return {k: _build(v, it) for k, v in t[1]}
        return [_build(v, it) for v in t[1]]
    if t == "n":
        return None
    return next(it)


class _Mean:
    """Running mean per key; integer arithmetic so pack and unpack agree exactly."""

    def __init__(self):
        self.s = {}

    def predict(self, key) -> int:
        tot, n = self.s.get(key, (0, 0))
        return (2 * tot + n) // (2 * n) if n else 0

    def update(self, key, x: int):
        tot, n = self.s.get(key, (0, 0))
        self.s[key] = (tot + x, n + 1)


def _ctx(body) -> str:
    c = body.get("cell") if isinstance(body, dict) else None
    return c if isinstance(c, str) else ""


# ---- pack / unpack ------------------------------------------------------------------------
def _fnv_hash(env: dict) -> str:
    return "0x%016x" % AL.fnv1a64(AL.canon({k: v for k, v in env.items() if k != "hash"}))


def _fnv_chain_ok(records: list[dict]) -> bool:
    prev = FNV_GENESIS
    for rec in records:
        if rec.get("prev") != prev or rec.get("hash") != _fnv_hash(rec):
            return False
        prev = rec["hash"]
    return True


def _dialect(records: list[dict]) -> int:
    """0 = ActiveLog v1 sha256 prev-chain; 1 = fnv1a-64 `hash`-field chain. Both are fully
    recomputable from content, so neither stores any chain bytes."""
    if AL.verify_chain(records):
        return 0
    if all("hash" in r for r in records) and _fnv_chain_ok(records):
        return 1
    raise AtRestError("refusing to pack: ActiveLog chain does not verify")


def _payload(records: list[dict], dialect: int = 0) -> bytes:
    """One verified run -> the uncompressed ALR1 stream payload."""
    if not records:
        raise AtRestError("empty run")
    devs, shapes, strs = {}, {}, {}
    S = {k: bytearray() for k in ("dev", "type", "shape", "mono", "ts", "num", "scale", "str", "lit", "bool")}
    mean = _Mean()
    last_mono = 0
    for rec in records:
        extra = set(rec) - set(AL.REQUIRED) - ({"hash"} if dialect == 1 else set())
        if extra or rec["alv"] != AL.ALV:
            raise AtRestError("envelope fields outside ActiveLog v1: %s" % sorted(extra))
        if rec["dev"] not in devs:
            devs[rec["dev"]] = len(devs)
        S["dev"] += _uv(devs[rec["dev"]])
        S["type"] += _uv(AL.TYPES.index(rec["type"]))
        S["mono"] += _uv(_zz(rec["mono"] - last_mono - 1))
        last_mono = rec["mono"]
        if rec["ts"] == "det:%06d" % rec["mono"]:
            S["ts"] += b"\x00"
        else:
            S["ts"] += b"\x01"
            leaves_ts = rec["ts"].encode()
            S["lit"] += _uv(len(leaves_ts)) + leaves_ts
        leaves = []
        shape = _flatten(rec["body"], leaves)
        sid = shapes.setdefault(shape, len(shapes))
        S["shape"] += _uv(sid)
        ctx = _ctx(rec["body"])
        for pos, (tag, v) in enumerate(leaves):
            key = (sid, ctx, pos)
            if tag == "i" or tag == "f":
                if tag == "f":
                    scale, v = v
                    S["scale"] += _uv(scale)
                S["num"] += _uv(_zz(v - mean.predict(key)))
                mean.update(key, v)
            elif tag == "b":
                S["bool"] += b"\x01" if v else b"\x00"
            else:
                if v in strs:
                    S["str"] += _uv(strs[v] + 1)
                else:
                    strs[v] = len(strs)
                    S["str"] += _uv(0)
                    enc = v.encode()
                    S["lit"] += _uv(len(enc)) + enc
    table = json.dumps({"devs": list(devs), "shapes": list(shapes)}, separators=(",", ":")).encode()
    payload = _uv(len(records)) + _uv(len(table)) + table
    for k in S:
        payload += _uv(len(S[k])) + bytes(S[k])
    return payload


def _head(records: list[dict]) -> bytes:
    return hashlib.sha256(AL.canon(records[-1]).encode()).digest()


def _xz(payload: bytes) -> bytes:
    return lzma.compress(payload, preset=9 | lzma.PRESET_EXTREME)


MAX_PAYLOAD = 1 << 28   # 256 MiB decompressed: a hostile blob must not be an lzma bomb


def _unxz(body: bytes) -> bytes:
    try:
        d = lzma.LZMADecompressor()
        out = d.decompress(body, max_length=MAX_PAYLOAD + 1)
        if len(out) > MAX_PAYLOAD:
            raise AtRestError("payload larger than %d bytes refused" % MAX_PAYLOAD)
        if not d.eof:
            raise AtRestError("payload corrupt: Compressed data ended before the end-of-stream marker was reached")
        if d.unused_data:
            raise AtRestError("payload corrupt: trailing data after the lzma stream")
        return out
    except lzma.LZMAError as e:
        raise AtRestError("payload corrupt: %s" % e)


def _structure(f, *a):
    """Run a structural decode; ANY malformed-input failure surfaces as AtRestError, never IndexError/JSONDecodeError/..."""
    try:
        return f(*a)
    except AtRestError:
        raise
    except (ValueError, IndexError, KeyError, TypeError, OverflowError, UnicodeError, ZeroDivisionError, RecursionError, MemoryError, struct_error) as e:
        raise AtRestError("malformed payload: %s: %s" % (type(e).__name__, e))


def _open(blob: bytes, magic: bytes) -> bytes:
    if blob[:4] != magic:
        raise AtRestError("not an %s blob" % magic.decode())
    if len(blob) < 5:
        raise AtRestError("truncated %s blob (no flags byte)" % magic.decode())
    inner = blob[5:]
    return rs_unwrap(inner) if blob[4] & FLAG_RS else inner


def _seal(magic: bytes, inner: bytes, repair: bool) -> bytes:
    return magic + bytes([FLAG_RS if repair else 0]) + (rs_wrap(inner) if repair else inner)


def pack(records: list[dict], repair: bool = False) -> bytes:
    """One run -> ALR1 bytes."""
    if not records:
        raise AtRestError("refusing to pack an empty run")
    d = _dialect(records)
    blob = _seal(MAGIC, _head(records) + _xz(_payload(records, d)), repair)
    return blob[:4] + bytes([blob[4] | (FLAG_FNV if d else 0)]) + blob[5:]


def unpack(blob: bytes) -> list[dict]:
    inner = _open(blob, MAGIC)
    d = 1 if blob[4] & FLAG_FNV else 0
    return _checked(_structure(_from_payload, _unxz(inner[32:]), d), inner[:32], d)


def pack_many(runs: list[list[dict]], repair: bool = False) -> bytes:
    """Many independent runs (each its own GENESIS-rooted chain) -> one ALRM archive:
    one head receipt per run, one shared lzma context (small runs share their strings)."""
    if not runs or not all(runs):
        raise AtRestError("no runs (or an empty run)")
    ds = [_dialect(r) for r in runs]
    receipt = hashlib.sha256(b"".join(_head(r) for r in runs)).digest()
    joined = b"".join(_uv(len(p)) + p for p in (_payload(r, d) for r, d in zip(runs, ds)))
    return _seal(MAGIC_MANY, _uv(len(runs)) + receipt + bytes(ds) + _xz(joined), repair)


def unpack_many(blob: bytes) -> list[list[dict]]:
    inner = _open(blob, MAGIC_MANY)
    r = _Reader(inner)
    n = _structure(r.uv)
    receipt = _structure(r.take, 32)
    ds = _structure(r.take, n)
    pr = _Reader(_unxz(inner[r.i:]))
    runs = [_structure(lambda k=k: _from_payload(pr.take(pr.uv()), ds[k])) for k in range(n)]
    if pr.i != len(pr.b):
        raise AtRestError("trailing bytes in archive")
    if hashlib.sha256(b"".join(_head(x) for x in runs)).digest() != receipt:
        raise AtRestError("archive receipt mismatch: unpacked runs are not the packed runs")
    for x, d in zip(runs, ds):
        if not (_fnv_chain_ok(x) if d else AL.verify_chain(x)):
            raise AtRestError("unpacked chain does not verify")
    return runs


def _checked(out: list[dict], head: bytes, dialect: int = 0) -> list[dict]:
    if not out or _head(out) != head:
        raise AtRestError("head receipt mismatch: unpacked run is not the packed run")
    if not (_fnv_chain_ok(out) if dialect else AL.verify_chain(out)):
        raise AtRestError("unpacked chain does not verify")
    return out


def _from_payload(payload: bytes, dialect: int = 0) -> list[dict]:
    r = _Reader(payload)
    n = r.uv()
    table = json.loads(r.take(r.uv()))
    streams = {}
    for k in ("dev", "type", "shape", "mono", "ts", "num", "scale", "str", "lit", "bool"):
        streams[k] = _Reader(r.take(r.uv()))
    S = streams
    templates = [_parse_shape(s) for s in table["shapes"]]
    strs, mean, last_mono = [], _Mean(), 0
    out = []
    for seq in range(n):
        dev = table["devs"][S["dev"].uv()]
        typ = AL.TYPES[S["type"].uv()]
        mono = last_mono + 1 + _unzz(S["mono"].uv())
        last_mono = mono
        ts = "det:%06d" % mono if S["ts"].take(1) == b"\x00" else S["lit"].take(S["lit"].uv()).decode()
        sid = S["shape"].uv()
        tags = _leaf_tags(templates[sid])
        # context needs the 'cell' string, which is itself a leaf: decode leaves first, ctx after
        raw = []
        for tag in tags:
            if tag in "sF":
                j = S["str"].uv()
                if j == 0:
                    v = S["lit"].take(S["lit"].uv()).decode()
                    strs.append(v)
                else:
                    v = strs[j - 1]
                raw.append((tag, v))
            elif tag == "b":
                raw.append(("b", S["bool"].take(1) == b"\x01"))
            else:
                raw.append((tag, None if tag == "i" else S["scale"].uv()))
        ctx = _ctx_from(templates[sid], raw)
        leaves = []
        for pos, (tag, v) in enumerate(raw):
            if tag in "if":
                key = (sid, ctx, pos)
                x = _unzz(S["num"].uv()) + mean.predict(key)
                mean.update(key, x)
                leaves.append(x if tag == "i" else _from_parts(v, x))
            elif tag == "F":
                leaves.append(float(v))
            else:
                leaves.append(v)
        body = _build(templates[sid], iter(leaves))
        rec = {"alv": AL.ALV, "dev": dev, "seq": seq, "ts": ts, "mono": mono, "type": typ, "body": body}
        if dialect:
            rec["prev"] = out[-1]["hash"] if out else FNV_GENESIS
            rec["hash"] = _fnv_hash(rec)
        else:
            rec["prev"] = AL.link_hash(out[-1]) if out else AL.GENESIS
        out.append(rec)
    if r.i != len(payload):
        raise AtRestError("trailing bytes in run payload")
    return out


def _from_parts(scale, n):
    s = str(abs(n)).rjust(scale + 1, "0")
    txt = ("-" if n < 0 else "") + s[:len(s) - scale] + "." + s[len(s) - scale:]
    return float(txt)


def _leaf_tags(t):
    if isinstance(t, tuple):
        return [x for _, v in t[1] for x in _leaf_tags(v)] if t[0] == "d" else [x for v in t[1] for x in _leaf_tags(v)]
    return [] if t == "n" else [t]


def _ctx_from(t, raw):
    """Find the top-level 'cell' leaf's value (a string) without building the body."""
    if not (isinstance(t, tuple) and t[0] == "d"):
        return ""
    pos = 0
    for k, v in t[1]:
        width = len(_leaf_tags(v))
        if k == "cell" and v == "s":
            return raw[pos][1]
        pos += width
    return ""


# ---- Reed-Solomon RS(255,223) over GF(2^8), 8-way interleaved (from encoding-experiments E2) --
_EXP, _LOG = [0] * 512, [0] * 256
_x = 1
for _i in range(255):
    _EXP[_i], _LOG[_x] = _x, _i
    _x <<= 1
    if _x & 0x100:
        _x ^= 0x11D
for _i in range(255, 512):
    _EXP[_i] = _EXP[_i - 255]
_NSYM, _K, _DEPTH = 32, 223, 8


def _gmul(a, b):
    return 0 if a == 0 or b == 0 else _EXP[_LOG[a] + _LOG[b]]


def _gdiv(a, b):
    return 0 if a == 0 else _EXP[(_LOG[a] + 255 - _LOG[b]) % 255]


def _ginv(a):
    return _EXP[255 - _LOG[a]]


def _gpow(x, p):
    return _EXP[(_LOG[x] * p) % 255]


def _pmul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for j, qj in enumerate(q):
        for i, pi in enumerate(p):
            r[i + j] ^= _gmul(pi, qj)
    return r


def _padd(p, q):
    r = [0] * max(len(p), len(q))
    for i, c in enumerate(p):
        r[i + len(r) - len(p)] = c
    for i, c in enumerate(q):
        r[i + len(r) - len(q)] ^= c
    return r


def _peval(p, x):
    y = p[0]
    for c in p[1:]:
        y = _gmul(y, x) ^ c
    return y


_GEN = [1]
for _i in range(_NSYM):
    _GEN = _pmul(_GEN, [1, _EXP[_i]])


def _rs_encode(msg):
    buf = list(msg) + [0] * _NSYM
    for i in range(len(msg)):
        c = buf[i]
        if c:
            for j in range(1, len(_GEN)):
                buf[i + j] ^= _gmul(_GEN[j], c)
    return bytes(msg) + bytes(buf[len(msg):])


def _rs_decode(cw):
    cw = list(cw)
    synd = [0] + [_peval(cw, _gpow(2, i)) for i in range(_NSYM)]
    if max(synd) == 0:
        return bytes(cw[:-_NSYM])
    err, old = [1], [1]
    for i in range(_NSYM):
        K = i + 1
        delta = synd[K]
        for j in range(1, len(err)):
            delta ^= _gmul(err[-(j + 1)], synd[K - j])
        old = old + [0]
        if delta:
            if len(old) > len(err):
                new = [_gmul(c, delta) for c in old]
                old = [_gmul(c, _ginv(delta)) for c in err]
                err = new
            err = _padd(err, [_gmul(c, delta) for c in old])
    while err and err[0] == 0:
        err.pop(0)
    if (len(err) - 1) * 2 > _NSYM:
        raise AtRestError("too many errors in a Reed-Solomon block")
    rev = err[::-1]
    pos = [len(cw) - 1 - i for i in range(len(cw)) if _peval(rev, _gpow(2, i)) == 0]
    if len(pos) != len(err) - 1:
        raise AtRestError("Reed-Solomon locator mismatch")
    coef = [len(cw) - 1 - p for p in pos]
    loc = [1]
    for i in coef:
        loc = _pmul(loc, _padd([1], [_gpow(2, i), 0]))
    prod = _pmul(synd[::-1], loc)
    ev = prod[-len(loc):][::-1]  # remainder mod x^len(loc): the low-order terms
    X = [_gpow(2, -(255 - c)) for c in coef]
    E = [0] * len(cw)
    for i, Xi in enumerate(X):
        Xi_inv = _ginv(Xi)
        den = 1
        for j, Xj in enumerate(X):
            if j != i:
                den = _gmul(den, 1 ^ _gmul(Xi_inv, Xj))
        E[pos[i]] = _gdiv(_gmul(Xi, _peval(ev[::-1], Xi_inv)), den)
    cw = _padd(cw, E)
    if max(_peval(cw, _gpow(2, i)) for i in range(_NSYM)) != 0:
        raise AtRestError("Reed-Solomon decode failed")
    return bytes(cw[:-_NSYM])


def rs_wrap(data: bytes) -> bytes:
    blocks = [_rs_encode(data[i:i + _K].ljust(_K, b"\0")) for i in range(0, len(data), _K)]
    while len(blocks) % _DEPTH:
        blocks.append(_rs_encode(bytes(_K)))
    out = bytearray()
    for g in range(0, len(blocks), _DEPTH):
        grp = blocks[g:g + _DEPTH]
        for j in range(_K + _NSYM):
            out += bytes(b[j] for b in grp)
    return _uv(len(data)) + bytes(out)


def rs_unwrap(buf: bytes) -> bytes:
    r = _Reader(buf)
    n = r.uv()
    body = buf[r.i:]
    L = _K + _NSYM
    out = bytearray()
    for g in range(0, len(body), L * _DEPTH):
        chunk = body[g:g + L * _DEPTH]
        for d in range(_DEPTH):
            out += _rs_decode(bytes(chunk[j * _DEPTH + d] for j in range(L)))
    return bytes(out[:n])


if __name__ == "__main__":
    import route_sim as R
    recs = R.run(True)["log"].records
    jsonl = "".join(AL.canon(r) + "\n" for r in recs).encode()
    for repair in (False, True):
        blob = pack(recs, repair=repair)
        assert AL.canon(unpack(blob)) == AL.canon(recs)
        print("route_sim run (%d records): jsonl %d B, jsonl+lzma %d B, ALR1%s %d B" % (
            len(recs), len(jsonl), len(lzma.compress(jsonl, preset=9)), "+RS" if repair else "", len(blob)))
