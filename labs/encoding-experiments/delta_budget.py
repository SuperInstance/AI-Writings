"""E1 delta_budget — delta / zigzag / varint / context-prediction coding of an ActiveLog budget stream.

Gems: delta-encode (fixed delta, zigzag, varint, prediction-based), plato-compress
("temperatures change slowly -> delta; HVAC states repeat -> RLE"), plato-prediction
(Z_out: predict the next value; code only the surprise).

Data (HONEST LABEL): the ActiveLog envelopes are produced by the real B1 emitter
(labs/activeledger/activeledger.py) — real schema, real sha256 prev-chain — but the
budget NUMBERS come from a seeded cost model (5 cells cycling mic -> prefilter -> stt ->
grammar -> llm, per-cell base cost + jitter), exactly as B1's own route_sim does. A
second stream uses REAL numbers: the 4 judge scores on the 169 scored rows (of 2,355) of
cellular-first-design/code/autoclaw/simulations.jsonl.

Codecs, all lossless, all decoded and compared byte-for-byte:
  jsonl        canonical ActiveLog JSONL (what B1 writes today)
  jsonl+zlib   zlib -9 of that ; jsonl+lzma
  col-raw      columnar ints (usd -> micro-$, power -> mW), varint, no delta
  col-delta    per-column delta + zigzag + varint
  col-ctx      per-column residual vs "last value of the SAME cell" (context predictor)
  col-ctx+lzma the col-ctx bytes through lzma
In every columnar codec the sha256 `prev` fields are NOT stored: they are recomputed on
decode and the stream carries only the 32-byte head hash as its receipt.

Run: python3 delta_budget.py [--selftest]
"""
from __future__ import annotations
import hashlib, json, lzma, os, sys, zlib
import common as C

sys.path.insert(0, os.path.join(C.HERE, "..", "activeledger"))
import activeledger as AL  # noqa: E402

CELLS = [  # name, wall_ms base, jitter, power_w, mem_mb, prod bytes, llm?
    ("mic", 20, 2, 0.4, 8, 3200, False),
    ("prefilter", 6, 1, 0.9, 16, 0, False),
    ("stt", 48, 9, 2.1, 512, 0, False),
    ("grammar", 9, 3, 0.7, 64, 0, False),
    ("llm", 310, 80, 0.0, 0, 0, True),
]
FIELDS = ("wall_ms", "power_mw", "mem_mb", "prod", "train", "tok_in", "tok_out", "usd_micro")


def build_log(n=2000, seed=1):
    r = C.Rng(seed)
    log = AL.ActiveLog(dev="enc-e1")
    for i in range(n):
        name, base, jit, pw, mem, prod, llm = CELLS[i % len(CELLS)]
        wall = max(1, round(base + jit * r.gauss()))
        toks = {}
        usd = 0.0
        if llm:
            ti, to = 180 + r.randint(0, 60), 40 + r.randint(0, 90)
            toks = {"in": ti, "out": to}
            usd = round((ti * 0.03 + to * 0.05) / 1e6 * 1000, 6)  # $0.03/$0.05 per 1k tok
        b = AL.budget(wall_ms=wall, power_w=pw, mem_mb=mem, prod=prod, train=0, usd=usd,
                      tokens=toks, reqs="api" if llm else "local")
        log.emit("cell.tick", {"cell": name, "route": "voice-%d" % (i // len(CELLS)), "budget": b})
    return log.records


# ---- columnar extraction / reconstruction -----------------------------------------------
def to_cols(records):
    rows = []
    for rec in records:
        b = rec["body"]["budget"]
        rows.append((CELLS_IDX[rec["body"]["cell"]], [
            b["wall_ms"], round(b["power_w"] * 1000), b["mem_mb"], b["storage_bytes"]["prod"],
            b["storage_bytes"]["train"], b["tokens"].get("in", 0), b["tokens"].get("out", 0),
            round(b["usd"] * 1e6)]))
    return rows


CELLS_IDX = {c[0]: i for i, c in enumerate(CELLS)}


def from_cols(rows, dev="enc-e1"):
    log = AL.ActiveLog(dev=dev)
    for i, (ci, v) in enumerate(rows):
        name = CELLS[ci][0]
        toks = {"in": v[5], "out": v[6]} if (v[5] or v[6]) else {}
        b = AL.budget(wall_ms=v[0], power_w=v[1] / 1000, mem_mb=v[2], prod=v[3], train=v[4],
                      usd=v[7] / 1e6, tokens=toks, reqs="api" if toks else "local")
        log.emit("cell.tick", {"cell": name, "route": "voice-%d" % (i // len(CELLS)), "budget": b})
    return log.records


def encode(rows, mode):
    """mode in raw|delta|ctx -> bytes. Stream: n, then cell ids, then each column."""
    out = bytearray(C.varint(len(rows)))
    out += bytes(ci for ci, _ in rows)
    for f in range(len(FIELDS)):
        last_global, last_by_cell = 0, {}
        for ci, v in rows:
            x = v[f]
            if mode == "raw":
                out += C.varint(C.zigzag(x))
            elif mode == "delta":
                out += C.varint(C.zigzag(x - last_global))
            else:  # ctx: predict = last value seen for the same cell (plato-prediction's Value predictor)
                out += C.varint(C.zigzag(x - last_by_cell.get(ci, 0)))
            last_global, last_by_cell[ci] = x, x
    return bytes(out)


def decode(buf, mode):
    n, i = C.read_varint(buf, 0)
    cells = list(buf[i:i + n])
    i += n
    cols = []
    for _ in FIELDS:
        col, last_global, last_by_cell = [], 0, {}
        for ci in cells:
            z, i = C.read_varint(buf, i)
            d = C.unzigzag(z)
            x = d if mode == "raw" else d + (last_global if mode == "delta" else last_by_cell.get(ci, 0))
            col.append(x)
            last_global, last_by_cell[ci] = x, x
        cols.append(col)
    return [(cells[k], [cols[f][k] for f in range(len(FIELDS))]) for k in range(n)]


def head_hash(records):
    return AL.link_hash(records[-1])


def measure(n=2000, log=print):
    recs = build_log(n)
    jsonl = "".join(AL.canon(r) + "\n" for r in recs).encode()
    prev_bytes = sum(len(r["prev"]) + len('"prev":,""') for r in recs)
    rows = to_cols(recs)
    res = {"n_records": n, "jsonl": len(jsonl), "jsonl+zlib": len(zlib.compress(jsonl, 9)),
           "jsonl+lzma": len(lzma.compress(jsonl, preset=9)), "prev_field_share": round(prev_bytes / len(jsonl), 3)}
    for mode in ("raw", "delta", "ctx"):
        buf = encode(rows, mode)
        back = from_cols(decode(buf, mode))
        assert AL.canon(back) == AL.canon(recs) and AL.verify_chain(back) and head_hash(back) == head_hash(recs)
        res["col-" + mode] = len(buf) + 32  # + the 32-byte head receipt
    res["col-ctx+lzma"] = len(lzma.compress(encode(rows, "ctx"), preset=9)) + 32
    res["col-delta+lzma"] = len(lzma.compress(encode(rows, "delta"), preset=9)) + 32
    for k in [k for k in res if k.startswith(("jsonl", "col"))]:
        log(f"  {k:15s} {res[k]:8d} B   {res[k] / n:7.2f} B/record   ratio {res['jsonl'] / res[k]:6.1f}x")
    log(f"  sha256 prev fields are {res['prev_field_share']:.0%} of the JSONL and 0 B in every columnar codec (recomputed)")
    return res


# ---- a REAL numeric stream: autoclaw judge scores -----------------------------------------
def scores_stream():
    p = os.path.join(C.HERE, "..", "..", "cellular-first-design", "code", "autoclaw", "simulations.jsonl")
    rows = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            s = json.loads(line).get("score") or {}
            if not s:  # 2,186 of 2,355 rows carry no score at all; keep only the scored ones
                continue
            rows.append([round(100 * float(s.get(k, 0))) for k in ("quality", "novelty", "alignment", "confidence")])
    return rows


def code_scores(rows, mode):
    out = bytearray()
    for f in range(4):
        last, ema = 0, 0.0
        for v in rows:
            x = v[f]
            pred = {"raw": 0, "delta": last, "mean": round(ema)}[mode]
            out += C.varint(C.zigzag(x - pred))
            last, ema = x, (x if ema == 0 else 0.9 * ema + 0.1 * x)
    return bytes(out)


def measure_scores(log=print):
    rows = scores_stream()
    text = json.dumps(rows, separators=(",", ":")).encode()
    res = {"rows": len(rows), "json": len(text), "json+lzma": len(lzma.compress(text, preset=9))}
    for m in ("raw", "delta", "mean"):
        res["varint-" + m] = len(code_scores(rows, m))
        res["varint-" + m + "+lzma"] = len(lzma.compress(code_scores(rows, m), preset=9))
    log("  real autoclaw scores (%d rows x 4): " % len(rows) + ", ".join(f"{k}={v}" for k, v in res.items() if k != "rows"))
    return res


def selftest():
    c = C.Checks()
    for x in (0, 1, -1, 63, -64, 2 ** 40, -(2 ** 40)):
        c.ok(C.unzigzag(C.zigzag(x)) == x, f"zigzag {x}")
        c.ok(C.read_varint(C.varint(C.zigzag(x)), 0)[0] == C.zigzag(x), f"varint {x}")
    recs = build_log(60, seed=4)
    c.ok(AL.verify_chain(recs), "B1 chain valid")
    rows = to_cols(recs)
    for mode in ("raw", "delta", "ctx"):
        back = from_cols(decode(encode(rows, mode), mode))
        c.ok(AL.canon(back) == AL.canon(recs), f"{mode} exact round-trip")
        c.ok(head_hash(back) == head_hash(recs), f"{mode} head receipt matches")
    c.ok(len(encode(rows, "ctx")) < len(encode(rows, "raw")), "ctx beats raw on a cyclic cell stream")
    # tamper: flip one budget value -> recomputed head no longer matches the receipt
    bad = [list(r) for r in rows]
    bad[10] = (bad[10][0], [bad[10][1][0] + 1] + bad[10][1][1:])
    c.ok(head_hash(from_cols(bad)) != head_hash(recs), "tamper changes head receipt")
    return c.report("delta_budget")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    print("E1 delta_budget: ActiveLog budget stream (B1 emitter, seeded cost model), n=2000")
    r1 = measure()
    r2 = measure_scores()
    with open(C.HERE + "/results_delta_budget.json", "w") as f:
        json.dump({"activelog": r1, "autoclaw_scores": r2}, f, indent=1)
