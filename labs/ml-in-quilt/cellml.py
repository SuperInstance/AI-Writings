"""ml-in-quilt — a cell-native transformer forward pass (toy scale, stdlib only).

Every piece of the forward pass is a CELL: a pure function of (inputs, weights) with
  (a) a budget vector on every tick (labs/activeledger B1 shape; cost from a declared
      roofline model, not the wall clock, so replay == live bit-for-bit),
  (b) hash-chained activations: each tick logs the content hash of what it read and what
      it wrote, inside an ActiveLog v1 sha256 prev-chain; the KV cache is itself a hash
      chain per layer, so a KV entry is content-addressed,
  (c) a product identity declared at the SAMPLE boundary (the token), because that is the
      only place a quantized route can ever equal the float route exactly,
  (d) several interchangeable IMPLEMENTATIONS (fp32 / q8 / q4-Lloyd-Max) selected by a
      route PLAN, so System-2 (B7 system2-backtest, B4 route-preference) can price them.

    tokenize -> embed -> [norm -> attn(+kv) -> norm -> mlp] x L -> norm -> head -> sample

The model is an echo-state transformer: all weights are seeded Gaussian except the
readout (head), which is ridge-fitted to a tiny corpus in closed form (see fit_readout).
It is a mechanism toy, not a language model. Nothing here was trained by backprop.
"""

from __future__ import annotations

import math
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LABS = os.path.dirname(HERE)
for _d in ("activeledger", "code-real-quant", "system2-backtest", "route-preference"):
    _p = os.path.join(LABS, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import activeledger as al  # noqa: E402
import code_real_quant as crq  # noqa: E402

# ---- configuration ------------------------------------------------------------------

VOCAB = " .abcdefghijklmnopqrstuvwxyz"
CFG = {"d": 32, "heads": 2, "layers": 2, "ff": 64, "ctx": 64, "seed": 1234}
CORPUS = ("the cat sat on the mat. the dog sat on the log. the cat ate the rat. "
          "the dog ate the frog. a cat and a dog sat on a mat. the rat sat on the cat. ")

# Declared cost models (roofline). NOT measurements. time = max(flops/F, bytes/B).
# The two profiles differ only in the flop:byte ratio, which is what decides whether a
# batched verify pass is nearly free (accel) or costs as much as it computes (edge).
DEVICES = {
    "edge": {"name": "edge-cpu-roofline-v1", "flops_per_ms": 1.0e7, "bytes_per_ms": 1.0e7},
    "accel": {"name": "accel-roofline-v1", "flops_per_ms": 1.0e9, "bytes_per_ms": 1.0e7},
}
DEVICE = dict(DEVICES["edge"])


def use_device(key: str) -> dict:
    """Switch the active cost profile (every later tick is priced under it)."""
    DEVICE.clear()
    DEVICE.update(DEVICES[key])
    return DEVICE

IMPLS = ("fp", "q8", "q4")          # interchangeable linear kernels
LINEAR_KINDS = ("attn", "mlp", "head")


# ---- hashing -------------------------------------------------------------------------

def act_hash(rows) -> str:
    """fnv1a-64 over the IEEE-754 little-endian bytes of an activation (list of rows,
    list of floats, or ints). Exact: two activations hash equal iff bit-identical."""
    if rows and isinstance(rows[0], list):
        flat = [x for r in rows for x in r]
    else:
        flat = list(rows)
    if flat and isinstance(flat[0], int):
        blob = struct.pack("<%dq" % len(flat), *flat)
    else:
        blob = struct.pack("<%dd" % len(flat), *flat)
    return "0x%016x" % crq.fnv1a64(blob)


def chain(prev: str, item: str) -> str:
    return "0x%016x" % crq.fnv1a64((prev + item).encode())


# ---- tokenize cell (a naive port is fine here: exact, integer, no alternatives) ---------

def tokenize(text: str) -> list[int]:
    return [VOCAB.index(c) for c in text if c in VOCAB]


def detokenize(ids) -> str:
    return "".join(VOCAB[i] for i in ids)


# ---- tensors (lists) -----------------------------------------------------------------

def f32(x: float) -> float:
    return struct.unpack("<f", struct.pack("<f", x))[0]


def rmsnorm(x: list[float]) -> list[float]:
    s = math.sqrt(sum(v * v for v in x) / len(x) + 1e-6)
    return [v / s for v in x]


def gelu(x: float) -> float:
    return 0.5 * x * (1.0 + math.tanh(0.7978845608 * (x + 0.044715 * x * x * x)))


def pos_enc(p: int, d: int) -> list[float]:
    out = []
    for i in range(d):
        k = i // 2
        ang = p / (10000 ** (2 * k / d))
        out.append(math.sin(ang) if i % 2 == 0 else math.cos(ang))
    return out


# ---- linear kernels: three implementations of the same cell -------------------------

class Linear:
    """y = W x. `impl` decides how W is stored and read; all return floats.

    fp : fp32 weights (4 B/param).
    q8 : per-row absmax int8 (1 B/param + 4 B scale/row).
    q4 : per-row sigma + 4-bit Lloyd-Max codes from labs/code-real-quant (0.5 B/param +
         4 B/row). The codes are the SAME centroid table code-real-quant measured.
    Python keeps a dequantized copy for speed; the cost model charges `nbytes`, the packed
    size a fused dequant kernel would stream. (Shortcut, booked in the README.)
    """

    def __init__(self, name: str, W: list[list[float]], impl: str):
        self.name, self.impl = name, impl
        self.rows, self.cols = len(W), len(W[0])
        if impl == "fp":
            self.deq = W
            self.blob = struct.pack("<%df" % (self.rows * self.cols), *[x for r in W for x in r])
        elif impl == "q8":
            self.deq, blob = [], bytearray()
            for r in W:
                s = f32(max(abs(x) for x in r) / 127.0 or 1.0)
                q = [max(-127, min(127, round(x / s))) for x in r]
                self.deq.append([v * s for v in q])
                blob += struct.pack("<f", s) + struct.pack("<%db" % len(q), *q)
            self.blob = bytes(blob)
        elif impl == "q4":
            self.deq, blob = [], bytearray()
            for r in W:
                sig = f32(math.sqrt(sum(x * x for x in r) / len(r)) or 1.0)
                codes = crq.quantize([x / sig for x in r])
                self.deq.append([crq.CENTROIDS[c] * sig for c in codes])
                blob += struct.pack("<f", sig) + crq.pack(codes)
            self.blob = bytes(blob)
        else:
            raise ValueError("unknown impl %r" % impl)
        self.nbytes = len(self.blob)
        self.whash = "0x%016x" % crq.fnv1a64(self.blob)

    def __call__(self, x: list[float]) -> list[float]:
        return [sum(a * b for a, b in zip(r, x)) for r in self.deq]

    def flops(self, n_pos: int) -> int:
        return 2 * self.rows * self.cols * n_pos


def unpack_blob(blob: bytes, impl: str, rows: int, cols: int) -> list[list[float]]:
    """Inverse of Linear.blob -> dequantized rows (proves the at-rest bytes are the weights)."""
    out, i = [], 0
    for _ in range(rows):
        if impl == "fp":
            out.append(list(struct.unpack_from("<%df" % cols, blob, i)))
            i += 4 * cols
        elif impl == "q8":
            s = struct.unpack_from("<f", blob, i)[0]
            q = struct.unpack_from("<%db" % cols, blob, i + 4)
            out.append([v * s for v in q])
            i += 4 + cols
        else:
            s = struct.unpack_from("<f", blob, i)[0]
            nb = (cols + 1) // 2
            codes = crq.unpack(blob[i + 4:i + 4 + nb], cols)
            out.append([crq.CENTROIDS[c] * s for c in codes])
            i += 4 + nb
    return out


# ---- the model: weights + cached kernels ----------------------------------------------

def _gauss_matrix(rng, rows, cols, scale):
    return [[f32(rng.gauss() * scale) for _ in range(cols)] for _ in range(rows)]


class Model:
    def __init__(self, cfg=None, head=None):
        self.cfg = dict(cfg or CFG)
        d, ff, V = self.cfg["d"], self.cfg["ff"], len(VOCAB)
        rng = crq.XorShift64(self.cfg["seed"])
        self.W = {"embed": _gauss_matrix(rng, V, d, 1.0)}
        for l in range(self.cfg["layers"]):
            self.W["L%d.wqkv" % l] = _gauss_matrix(rng, 3 * d, d, 1.0 / math.sqrt(d))
            self.W["L%d.wo" % l] = _gauss_matrix(rng, d, d, 1.0 / math.sqrt(d))
            self.W["L%d.w1" % l] = _gauss_matrix(rng, ff, d, 1.0 / math.sqrt(d))
            self.W["L%d.w2" % l] = _gauss_matrix(rng, d, ff, 1.0 / math.sqrt(ff))
        # head reads [h, 1] (bias folded in). Seeded until fit_readout replaces it.
        self.W["head"] = head or _gauss_matrix(rng, V, d + 1, 1.0 / math.sqrt(d))
        self._k = {}

    def kind_of(self, wname: str) -> str:
        if wname in ("head", "jepa"):
            return wname
        return "attn" if wname.split(".")[1] in ("wqkv", "wo") else "mlp"

    def linear(self, wname: str, impl: str) -> Linear:
        key = (wname, impl)
        if key not in self._k:
            self._k[key] = Linear(wname, self.W[wname], impl)
        return self._k[key]

    def weights_hash(self) -> str:
        return al.content_hash({k: act_hash(v) for k, v in sorted(self.W.items())})


def plan_impl(plan: dict, cell: str, kind: str) -> str:
    """A plan maps a cell name ('L0.mlp') or a kind ('mlp') to an impl; default fp."""
    return plan.get(cell, plan.get(kind, "fp"))


def plan_sig(plan: dict) -> str:
    return al.content_hash(dict(sorted(plan.items())))


# ---- cost model -------------------------------------------------------------------------

def cost(flops: int, nbytes: int) -> float:
    return round(max(flops / DEVICE["flops_per_ms"], nbytes / DEVICE["bytes_per_ms"]), 6)


# ---- a Stream: one sequence's live state under one plan (KV cache + hash chains) --------

class Stream:
    """Runs cells for one sequence under one plan, emitting a cell.tick per cell call.

    kv[l]      = list of (k_row, v_row) per position (per-head split at use time)
    kvh[l]     = list of chained hashes; kvh[l][p] addresses the whole prefix 0..p
    `fed`      = number of positions whose K/V is in the cache
    """

    def __init__(self, model: Model, plan: dict, log, route: str, tag: str = "",
                 prefix_cache=None):
        self.m, self.plan, self.log, self.route, self.tag = model, plan, log, route, tag
        L = model.cfg["layers"]
        self.kv = [[] for _ in range(L)]
        self.kvh = [[] for _ in range(L)]
        self.fed = 0
        self.pc = prefix_cache
        self.fed_tokens: list[int] = []
        self.last_out = ""

    # -- logging ---------------------------------------------------------------
    def tick(self, cell, kind, impl, pos, h_in, h_out, flops, nbytes, whash="", kvh="",
             extra=None, mem=0):
        if self.log is None:
            return
        body = {"route": self.route, "cell": cell, "kind": kind, "impl": impl,
                "pos": list(pos), "in": h_in, "out": h_out, "w": whash, "kv": kvh,
                "flops": flops, "bytes": nbytes,
                "budget": al.budget(wall_ms=cost(flops, nbytes), mem_mb=round(mem / 1e6, 6))}
        if self.tag:
            body["stream"] = self.tag
        if extra:
            body.update(extra)
        self.log.emit("cell.tick", body)

    def truncate(self, n: int):
        """Roll the KV cache (and its hash chain) back to n positions."""
        for l in range(len(self.kv)):
            del self.kv[l][n:]
            del self.kvh[l][n:]
        del self.fed_tokens[n:]
        self.fed = min(self.fed, n)

    # -- the cells ---------------------------------------------------------------
    def feed(self, tokens: list[int]) -> list[list[float]]:
        """Feed new tokens at positions fed..fed+n-1; return logits for each position."""
        m, d = self.m, self.m.cfg["d"]
        start = self.fed
        if start + len(tokens) > m.cfg["ctx"]:
            raise ValueError("context overflow")
        pos = (start, start + len(tokens))
        n = len(tokens)
        # prefix cache: reuse K/V for positions whose token-prefix was seen under this plan
        reuse = 0
        if self.pc is not None and start == 0:
            reuse = self.pc.longest(self.plan, tokens, limit=n - 1)
            if reuse:
                for l in range(len(self.kv)):
                    self.kv[l], self.kvh[l] = self.pc.load(self.plan, tokens[:reuse], l)
                kv_bytes = 4 * 2 * d * reuse * len(self.kv)
                self.tick("kvcache", "kvcache", "hit", (0, reuse), act_hash(tokens[:reuse]),
                          ",".join(h[-1] for h in self.kvh), 0, kv_bytes, mem=kv_bytes)
                self.fed = reuse
                self.fed_tokens = list(tokens[:reuse])
                tokens = tokens[reuse:]
                start, n = reuse, len(tokens)
                pos = (start, start + n)

        # embed
        E = m.W["embed"]
        x = [[E[t][i] + pe for i, pe in enumerate(pos_enc(start + j, d))]
             for j, t in enumerate(tokens)]
        self.tick("embed", "embed", "fp", pos, act_hash(tokens), act_hash(x),
                  d * n, 4 * d * n + 4 * d * n)
        exit_at = self.plan.get("exit")
        for l in range(exit_at if exit_at else m.cfg["layers"]):
            h = [rmsnorm(r) for r in x]
            self.tick("L%d.norm1" % l, "norm", "fp", pos, act_hash(x), act_hash(h),
                      4 * d * n, 8 * d * n)
            x = self._attn(l, h, x, pos)
            h = [rmsnorm(r) for r in x]
            self.tick("L%d.norm2" % l, "norm", "fp", pos, act_hash(x), act_hash(h),
                      4 * d * n, 8 * d * n)
            x = self._mlp(l, h, x, pos)
        h = [rmsnorm(r) for r in x]
        self.tick("final.norm", "norm", "fp", pos, act_hash(x), act_hash(h), 4 * d * n, 8 * d * n)
        if exit_at:
            # JEPA-style latent predictor: Z_in = normed residual after layer exit_at-1,
            # Z_out = predicted final normed hidden. Skips the remaining layers entirely.
            pr = m.linear("jepa", plan_impl(self.plan, "jepa", "jepa"))
            z = [pr(r + [1.0]) for r in h]
            self.tick("jepa.predict", "jepa", pr.impl, pos, act_hash(h), act_hash(z),
                      pr.flops(n), pr.nbytes + 8 * d * n, pr.whash)
            h = z
        impl = plan_impl(self.plan, "head", "head")
        head = m.linear("head", impl)
        logits = [head(r + [1.0]) for r in h]
        self.last_out = act_hash(logits)
        self.tick("head", "head", impl, pos, act_hash(h), self.last_out,
                  head.flops(n), head.nbytes + 4 * (d + len(VOCAB)) * n, head.whash)
        self.fed = start + n
        self.fed_tokens.extend(tokens)
        if self.pc is not None:
            self.pc.store(self.plan, self.fed_tokens, self.kv, self.kvh)
        return logits

    def _attn(self, l, h, x, pos):
        m, d, H = self.m, self.m.cfg["d"], self.m.cfg["heads"]
        hd = d // H
        cell = "L%d.attn" % l
        impl = plan_impl(self.plan, cell, "attn")
        wqkv, wo = m.linear("L%d.wqkv" % l, impl), m.linear("L%d.wo" % l, impl)
        out, flops, kv_read = [], 0, 0
        for j, r in enumerate(h):
            qkv = wqkv(r)
            q, k, v = qkv[:d], qkv[d:2 * d], qkv[2 * d:]
            p = pos[0] + j
            self.kv[l].append((k, v))
            prev = self.kvh[l][-1] if self.kvh[l] else "0x0000000000000000"
            self.kvh[l].append(chain(prev, act_hash([k, v])))
            ctx = self.kv[l][:p + 1]
            att = []
            for hh in range(H):
                sl = slice(hh * hd, (hh + 1) * hd)
                qs = q[sl]
                sc = [sum(a * b for a, b in zip(qs, kk[sl])) / math.sqrt(hd) for kk, _ in ctx]
                mx = max(sc)
                e = [math.exp(s - mx) for s in sc]
                z = sum(e)
                att.extend(sum(e[t] / z * ctx[t][1][i] for t in range(len(ctx)))
                           for i in range(sl.start, sl.stop))
            o = wo(att)
            out.append([a + b for a, b in zip(x[j], o)])
            flops += 4 * d * len(ctx)
            kv_read += 4 * 2 * d * len(ctx)
        flops += wqkv.flops(len(h)) + wo.flops(len(h))
        nbytes = wqkv.nbytes + wo.nbytes + kv_read + 4 * 3 * d * len(h)
        self.tick(cell, "attn", impl, pos, act_hash(h), act_hash(out), flops, nbytes,
                  al.content_hash([wqkv.whash, wo.whash]), self.kvh[l][-1])
        return out

    def _mlp(self, l, h, x, pos):
        m = self.m
        cell = "L%d.mlp" % l
        impl = plan_impl(self.plan, cell, "mlp")
        w1, w2 = m.linear("L%d.w1" % l, impl), m.linear("L%d.w2" % l, impl)
        out = []
        for j, r in enumerate(h):
            y = w2([gelu(v) for v in w1(r)])
            out.append([a + b for a, b in zip(x[j], y)])
        flops = w1.flops(len(h)) + w2.flops(len(h))
        nbytes = w1.nbytes + w2.nbytes + 4 * 3 * m.cfg["d"] * len(h)
        self.tick(cell, "mlp", impl, pos, act_hash(h), act_hash(out), flops, nbytes,
                  al.content_hash([w1.whash, w2.whash]))
        return out

    def sample(self, logits: list[float], pos: int) -> int:
        """Greedy sample cell. The PRODUCT boundary: logs the token and the top-1 margin."""
        order = sorted(range(len(logits)), key=lambda i: (-logits[i], i))
        tok = order[0]
        margin = logits[order[0]] - logits[order[1]]
        # reads row -1 of the head's output: `in` is the head tick's `out` (dataflow closure)
        self.tick("sample", "sample", "greedy", (pos, pos + 1), self.last_out, act_hash([tok]),
                  2 * len(logits), 4 * len(logits), extra={"token": tok, "row": -1,
                                                           "margin": round(margin, 6)})
        return tok


def argmax(v):
    return max(range(len(v)), key=lambda i: (v[i], -i))


# ---- prefix cache (content-addressed KV) ----------------------------------------------

class PrefixCache:
    """K/V per (plan, token-prefix). Because the KV cache is hash-chained, a hit can be
    checked: the loaded chain head must equal what computing would have produced."""

    def __init__(self):
        self.store_ = {}

    def _key(self, plan, toks):
        return (plan_sig(plan), act_hash(list(toks)) if toks else "")

    def store(self, plan, toks, kv, kvh):
        for p in range(1, len(toks) + 1):
            key = self._key(plan, toks[:p])
            if key not in self.store_:
                self.store_[key] = [(list(kv[l][:p]), list(kvh[l][:p])) for l in range(len(kv))]

    def longest(self, plan, toks, limit):
        for p in range(min(limit, len(toks)), 0, -1):
            if self._key(plan, toks[:p]) in self.store_:
                return p
        return 0

    def load(self, plan, toks, l):
        kv, kvh = self.store_[self._key(plan, toks)][l]
        return list(kv), list(kvh)


# ---- routes: each run is one ActiveLog closed by one ledger.transaction ------------------

def _close(log, route, prompt, toks, extra=None):
    """Product = {prompt, tokens, text}. Route metadata goes under `chosen`, which B7
    (system2-backtest NON_PRODUCT) excludes from the identity gate."""
    total = al.route_total(log.records, route)
    body = {"route": route, "path": route, "prompt": prompt, "tokens": toks,
            "text": detokenize(toks), "total_budget": total}
    if extra:
        body.update(extra)
    body.setdefault("chosen", {})["device"] = DEVICE["name"]
    log.emit("ledger.transaction", body)
    return log


def _load_ticks(log, model, route, plans):
    """One tick per weight tensor a route will read: storage at rest + hot bytes."""
    seen = set()
    for plan in plans:
        ex = plan.get("exit")
        for wname in sorted(model.W):
            if wname == "jepa" and not ex:
                continue
            if ex and wname.startswith("L") and int(wname[1:wname.index(".")]) >= ex:
                continue
            if wname == "embed":
                impl, nb, wh = "fp", 4 * len(model.W["embed"]) * model.cfg["d"], act_hash(model.W["embed"])
            else:
                kind = model.kind_of(wname)
                cellname = wname if kind in ("head", "jepa") else wname.split(".")[0] + "." + kind
                impl = plan_impl(plan, cellname, kind)
                lin = model.linear(wname, impl)
                nb, wh = lin.nbytes, lin.whash
            if (wname, impl) in seen:
                continue
            seen.add((wname, impl))
            log.emit("cell.tick", {"route": route, "cell": "load:" + wname, "kind": "load",
                                   "impl": impl, "pos": [0, 0], "in": "", "out": wh, "w": wh,
                                   "kv": "", "flops": 0, "bytes": nb,
                                   "budget": al.budget(prod=nb, mem_mb=round(nb / 1e6, 6))})


def run_greedy(model, prompt: str, n: int, plan: dict, route: str, prefix_cache=None,
               log=True):
    """Plain greedy decode under one plan. Returns the ActiveLog (closed)."""
    lg = al.ActiveLog(dev="ml-in-quilt") if log else None
    if lg is not None:
        _load_ticks(lg, model, route, [plan])
    s = Stream(model, plan, lg, route, prefix_cache=prefix_cache)
    toks = tokenize(prompt)
    logits = s.feed(toks)
    out = []
    for i in range(n):
        t = s.sample(logits[-1], s.fed)
        out.append(t)
        if i + 1 < n:
            logits = s.feed([t])
    if lg is None:
        return out
    return _close(lg, route, prompt, out, {"chosen": {"plan": dict(sorted(plan.items()))}})


def run_speculative(model, prompt: str, n: int, draft_plan: dict, verify_plan: dict,
                    route: str, k: int = 4):
    """Draft k tokens with a cheap plan, verify them in ONE batched pass of the exact plan.
    Every committed token is the verify plan's argmax given the committed prefix, so the
    product equals run_greedy(verify_plan) by construction — the verifier cell IS the gate."""
    lg = al.ActiveLog(dev="ml-in-quilt")
    _load_ticks(lg, model, route, [draft_plan, verify_plan])
    dr = Stream(model, draft_plan, lg, route, tag="draft")
    vf = Stream(model, verify_plan, lg, route, tag="verify")
    seq = tokenize(prompt)
    p0 = len(seq)
    proposed = accepted = 0
    while len(seq) - p0 < n:
        kk = min(k, n - (len(seq) - p0))
        d = []
        for _ in range(kk):
            lo = dr.feed((seq + d)[dr.fed:])
            d.append(argmax(lo[-1]))
        lv = vf.feed((seq + d)[vf.fed:])
        # lv rows cover positions vf.fed_before .. len(seq)+kk-1; take the last kk+1
        preds = [argmax(r) for r in lv[-(kk + 1):]]
        j = 0
        while j < kk and d[j] == preds[j]:
            j += 1
        new = d[:j] + ([preds[j]] if len(seq) - p0 + j < n else [])
        new = new[:n - (len(seq) - p0)]
        vf.tick("verify", "verify", "exact", (len(seq), len(seq) + kk), act_hash(d),
                act_hash(new), 0, 0, extra={"proposed": kk, "accepted": j})
        proposed += kk
        accepted += j
        old = len(seq)
        seq = seq + new
        vf.truncate(len(seq) - 1)
        dr.truncate(min(dr.fed, old + j))
    toks = seq[p0:]
    return _close(lg, route, prompt, toks,
                  {"chosen": {"plan": {"draft": dict(sorted(draft_plan.items())),
                                       "verify": dict(sorted(verify_plan.items()))},
                              "accept": [accepted, proposed], "k": k}})


def run_gated(model, prompt: str, n: int, cheap_plan: dict, exact_plan: dict, route: str,
              eps: float, final_verify: bool = True):
    """Margin-triggered speculative decoding. The cheap plan decodes greedily; a token whose
    top-1 margin exceeds 2*eps is committed PENDING (trusted for now). When the cheap plan is
    unsure, the exact plan catches up on every pending token in ONE batched pass, fixes the
    first disagreement, and supplies the uncertain token itself.
      final_verify=True : pending tokens are verified at the end -> exact by construction.
      final_verify=False: tokens trusted by calibration are never re-checked -> B7 decides."""
    lg = al.ActiveLog(dev="ml-in-quilt")
    _load_ticks(lg, model, route, [cheap_plan, exact_plan])
    dr = Stream(model, cheap_plan, lg, route, tag="draft")
    vf = Stream(model, exact_plan, lg, route, tag="verify")
    seq = tokenize(prompt)
    p0 = len(seq)
    pending = verifies = fixed = 0

    def verify(extra_token: bool):
        nonlocal seq, pending, verifies, fixed
        rows = vf.feed(seq[vf.fed:])
        start = len(seq) - pending                   # first pending position
        preds = [argmax(r) for r in rows[-(pending + 1):]]   # preds for start..len(seq)
        j = 0
        while j < pending and seq[start + j] == preds[j]:
            j += 1
        before = list(seq)
        if j < pending:
            seq = seq[:start + j] + [preds[j]]
            fixed += 1
        elif extra_token:
            seq = seq + [preds[pending]]
        vf.tick("verify", "verify", "exact", (start, len(before)), act_hash(before[start:]),
                act_hash(seq[start:]), 0, 0, extra={"proposed": pending, "accepted": j})
        verifies += 1
        vf.truncate(len(seq) - 1)
        dr.truncate(min(dr.fed, start + j))
        pending = 0

    while True:
        if len(seq) - p0 >= n:
            if final_verify and pending:
                verify(extra_token=False)
                continue
            break
        lo = dr.feed(seq[dr.fed:])[-1]
        order = sorted(range(len(lo)), key=lambda i: (-lo[i], i))
        margin = lo[order[0]] - lo[order[1]]
        if margin > 2 * eps:
            seq = seq + [order[0]]
            pending += 1
        else:
            verify(extra_token=True)
    toks = seq[p0:p0 + n]
    return _close(lg, route, prompt, toks,
                  {"chosen": {"plan": {"draft": dict(sorted(cheap_plan.items())),
                                       "verify": dict(sorted(exact_plan.items()))},
                              "gate": {"eps": eps, "final_verify": final_verify,
                                       "verifies": verifies, "fixed": fixed}}})


# ---- readout fit (the only "training"): ridge regression, closed form ---------------------

def features(model, text: str, chunk: int = None) -> tuple[list, list]:
    """Final normed hidden state [h,1] at every position of `text`, with next-token targets."""
    chunk = chunk or model.cfg["ctx"]
    ids = tokenize(text)
    X, Y = [], []
    for s in range(0, len(ids) - 1, chunk // 2):
        seg = ids[s:s + chunk]
        if len(seg) < 2:
            break
        st = Stream(model, {}, None, "fit")
        # run up to final norm by feeding and capturing h: reuse feed, then back out h from
        # head input is not exposed, so recompute cheaply via a hook
        hs = _hidden(st, seg)
        first = 0 if s == 0 else chunk // 2   # overlapping windows: only new positions
        for j in range(max(first, 0), len(seg) - 1):
            X.append(hs[j] + [1.0])
            Y.append(seg[j + 1])
    return X, Y


def _hidden(stream: Stream, tokens, layers=None):
    """Forward to the final norm (no head), no logging. Used only for fitting."""
    m, d = stream.m, stream.m.cfg["d"]
    E = m.W["embed"]
    x = [[E[t][i] + pe for i, pe in enumerate(pos_enc(j, d))] for j, t in enumerate(tokens)]
    pos = (0, len(tokens))
    for l in range(m.cfg["layers"] if layers is None else layers):
        x = stream._attn(l, [rmsnorm(r) for r in x], x, pos)
        x = stream._mlp(l, [rmsnorm(r) for r in x], x, pos)
    return [rmsnorm(r) for r in x]


def _solve(A, B):
    """Gauss-Jordan with partial pivoting: A (n x n) X = B (n x m)."""
    n, mcols = len(A), len(B[0])
    M = [A[i][:] + B[i][:] for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [v / pv for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0.0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [row[n:n + mcols] for row in M]


def fit_readout(model, text=CORPUS, lam=1e-3):
    X, Y = features(model, text)
    D, V = len(X[0]), len(VOCAB)
    A = [[sum(X[r][i] * X[r][j] for r in range(len(X))) + (lam if i == j else 0.0)
          for j in range(D)] for i in range(D)]
    B = [[0.0] * V for _ in range(D)]
    for r, y in enumerate(Y):
        for i in range(D):
            B[i][y] += X[r][i]
    Wt = _solve(A, B)                      # D x V
    model.W["head"] = [[f32(Wt[i][v]) for i in range(D)] for v in range(V)]
    model._k = {k: v for k, v in model._k.items() if k[0] != "head"}
    hits = sum(1 for x, y in zip(X, Y)
               if argmax([sum(a * b for a, b in zip(row, x)) for row in model.W["head"]]) == y)
    return {"positions": len(X), "train_acc": round(hits / len(X), 4), "lambda": lam}


def fit_latent_predictor(model, exit_at=1, text=CORPUS, lam=1e-3):
    """Fit the JEPA-style predictor Z_in (normed residual after layer exit_at-1) ->
    Z_out (final normed hidden), ridge, closed form. Stored as weight 'jepa' (d x d+1)."""
    ids = tokenize(text)
    Zi, Zo = [], []
    chunk = model.cfg["ctx"]
    for s in range(0, len(ids) - 1, chunk // 2):
        seg = ids[s:s + chunk]
        if len(seg) < 2:
            break
        first = 0 if s == 0 else chunk // 2
        a = _hidden(Stream(model, {}, None, "fit"), seg, layers=exit_at)
        b = _hidden(Stream(model, {}, None, "fit"), seg)
        for j in range(first, len(seg)):
            Zi.append(a[j] + [1.0])
            Zo.append(b[j])
    D, d = len(Zi[0]), len(Zo[0])
    A = [[sum(Zi[r][i] * Zi[r][j] for r in range(len(Zi))) + (lam if i == j else 0.0)
          for j in range(D)] for i in range(D)]
    B = [[sum(Zi[r][i] * Zo[r][c] for r in range(len(Zi))) for c in range(d)] for i in range(D)]
    Wt = _solve(A, B)
    model.W["jepa"] = [[f32(Wt[i][c]) for i in range(D)] for c in range(d)]
    model._k = {k: v for k, v in model._k.items() if k[0] != "jepa"}
    err = sum(sum((sum(w * z for w, z in zip(row, zi)) - zo[c]) ** 2
                  for c, row in enumerate(model.W["jepa"])) for zi, zo in zip(Zi, Zo))
    var = sum(sum(v * v for v in zo) for zo in Zo)
    return {"positions": len(Zi), "r2": round(1 - err / var, 4), "exit": exit_at}


def build_model():
    m = Model()
    fit = fit_readout(m)
    fit["jepa"] = fit_latent_predictor(m)
    return m, fit
