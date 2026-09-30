"""nettrain — a tiny cell-native training loop with interchangeable UPDATE implementations.

Mirrors SuperInstance/quilt-nn (read-only, cited, not merged): weights, gradients and the SGD
step are explicit cells; init and per-epoch shuffle come from one seeded LCG (Numerical
Recipes, mod 2^32); every epoch appends one sha256-linked receipt that commits to the loss
bytes and the full weight state. Two quilt-nn conventions are kept verbatim so digests are
portable: a scalar is sealed as sha256("f64|8|<big-endian IEEE-754 hex>"), and aggregation
happens in a LISTED order. One convention is added from cellgraph's float32 scar: the weight
root carries the STORAGE dtype in every preimage ("f32|4|…", "bf16|2|…"), so an fp32 weight
and an fp64 weight with the same value can never collide.

What differs between routes is ONLY the update step (the `tick` cell). Everything else — the
init stream, the shuffle stream, the forward/backward arithmetic (float64), the data — is
shared, so any divergence is caused by the update implementation alone:

    fp64       reference: w <- w - lr*g, float64 storage, batch sums in listed order
    fp64-rev   same math, batch gradient/loss sums accumulated in REVERSE order
               (the xruntime-conformance situation: identical arithmetic, different order)
    fp32       weights stored in float32 (round-to-nearest-even after every update)
    bf16-sr    weights stored in bfloat16 with STOCHASTIC rounding (seeded, own LCG stream)
    bf16-rn    weights stored in bfloat16 with round-to-nearest-even (the classic stall:
               updates smaller than half an ulp are swallowed — Gupta et al. 2015)
    fsum       the CONSTRUCTIVE candidate: float64, but every cross-sample reduction (batch
               gradient sums, epoch loss sum) is correctly rounded (math.fsum, Shewchuk), so
               its result does not depend on accumulation order
    fsum-rev   fsum with the batch order reversed — the reorder test for the canonical step

Tasks: `sine` (1-8-1 tanh/linear, regression, y = sin(pi x)) and `circle` (2-8-1 tanh/sigmoid,
classification, y = [x^2 + y^2 < 0.5]). Stdlib only, deterministic, offline.
"""

from __future__ import annotations

import hashlib
import math
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LABS = os.path.dirname(HERE)
for _d in ("activeledger", "system2-backtest", "route-preference"):
    _p = os.path.join(LABS, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import activeledger as al  # noqa: E402

IMPLS = ("fp64", "fp64-rev", "fp32", "bf16-sr", "bf16-rn", "fsum", "fsum-rev")
DTYPE = {"fp64": ("f64", 8), "fp64-rev": ("f64", 8), "fp32": ("f32", 4),
         "bf16-sr": ("bf16", 2), "bf16-rn": ("bf16", 2), "fsum": ("f64", 8), "fsum-rev": ("f64", 8)}
EXACT_SUM = ("fsum", "fsum-rev")
REVERSED = ("fp64-rev", "fsum-rev")

TASKS = {
    "sine": {"n_in": 1, "hidden": 8, "out": "linear", "n_train": 32, "batch": 8,
             "epochs": 300, "lr": 0.2},
    "circle": {"n_in": 2, "hidden": 8, "out": "sigmoid", "n_train": 64, "batch": 8,
               "epochs": 200, "lr": 1.0},
}

# Declared cost models (roofline), the same two profiles labs/ml-in-quilt prices under.
# NOT measurements: time = max(flops/F, bytes/B). Python wall time is a sidecar only.
DEVICES = {
    "edge": {"name": "edge-cpu-roofline-v1", "flops_per_ms": 1.0e7, "bytes_per_ms": 1.0e7},
    "accel": {"name": "accel-roofline-v1", "flops_per_ms": 1.0e9, "bytes_per_ms": 1.0e7},
}


# ---- LCG (Numerical Recipes, mod 2^32) — quilt-nn's generator ----------------------------

class LCG:
    def __init__(self, seed: int):
        self.s = seed & 0xFFFFFFFF

    def u32(self) -> int:
        self.s = (1664525 * self.s + 1013904223) & 0xFFFFFFFF
        return self.s

    def uniform(self, lo=0.0, hi=1.0) -> float:
        return lo + (hi - lo) * (self.u32() / 4294967296.0)

    def shuffle(self, xs: list) -> list:
        xs = list(xs)
        for i in range(len(xs) - 1, 0, -1):
            j = self.u32() % (i + 1)
            xs[i], xs[j] = xs[j], xs[i]
        return xs


# ---- storage precisions -----------------------------------------------------------------

def _f32_bits(x: float) -> int:
    return struct.unpack(">I", struct.pack(">f", x))[0]


def _from_f32_bits(b: int) -> float:
    return struct.unpack(">f", struct.pack(">I", b & 0xFFFFFFFF))[0]


def to_f32(x: float) -> float:
    return struct.unpack(">f", struct.pack(">f", x))[0]


def to_bf16_rn(x: float) -> float:
    """float64 -> bfloat16, round-to-nearest-even (via float32; double rounding is ignored)."""
    b = _f32_bits(x)
    b = b + 0x7FFF + ((b >> 16) & 1)
    return _from_f32_bits(b & 0xFFFF0000)


def to_bf16_sr(x: float, r16: int) -> float:
    """float64 -> bfloat16, stochastic rounding: add 16 random bits below the kept mantissa,
    truncate. In the magnitude domain this rounds up with probability = the dropped fraction,
    so it is unbiased in expectation."""
    b = _f32_bits(x)
    return _from_f32_bits((b + (r16 & 0xFFFF)) & 0xFFFF0000)


def store(impl: str, x: float, rng: LCG | None) -> float:
    if impl in ("fp64", "fp64-rev", "fsum", "fsum-rev"):
        return x
    if impl == "fp32":
        return to_f32(x)
    if impl == "bf16-rn":
        return to_bf16_rn(x)
    if impl == "bf16-sr":
        return to_bf16_sr(x, rng.u32() >> 16)
    raise ValueError("unknown impl %r" % impl)


# ---- digests (quilt-nn v2 preimages + dtype-in-digest) ----------------------------------

def scalar_preimage(x: float, dtype: str = "f64") -> str:
    if dtype == "f64":
        return "f64|8|" + struct.pack(">d", x).hex()
    if dtype == "f32":
        return "f32|4|" + struct.pack(">f", x).hex()
    if dtype == "bf16":
        return "bf16|2|" + struct.pack(">f", x).hex()[:4]
    raise ValueError(dtype)


def scalar_sha(x: float, dtype: str = "f64") -> str:
    return hashlib.sha256(scalar_preimage(x, dtype).encode()).hexdigest()


def weight_root(w: list[float], dtype: str) -> str:
    return hashlib.sha256("|".join(scalar_preimage(v, dtype) for v in w).encode()).hexdigest()


def vec_sha(xs: list[float]) -> str:
    return hashlib.sha256("|".join(scalar_preimage(v) for v in xs).encode()).hexdigest()


# ---- data -------------------------------------------------------------------------------

def target(task: str, x: tuple) -> float:
    if task == "sine":
        return math.sin(math.pi * x[0])
    return 1.0 if x[0] * x[0] + x[1] * x[1] < 0.5 else 0.0


def sample_points(task: str, n: int, seed: int) -> list[tuple]:
    rng = LCG(seed)
    k = TASKS[task]["n_in"]
    return [tuple(rng.uniform(-1.0, 1.0) for _ in range(k)) for _ in range(n)]


def dataset(task: str) -> list[tuple]:
    """Training set: fixed (seed-independent), so routes and seeds see the same data."""
    return [(x, target(task, x)) for x in sample_points(task, TASKS[task]["n_train"], 0xDA7A)]


def heldout(task: str, n: int, seed: int = 0x4E1D) -> list[tuple]:
    return sample_points(task, n, seed)


# ---- the net (scalar cells: W1, b1, W2, b2 in graph order) -------------------------------

def n_params(task: str) -> int:
    c = TASKS[task]
    return c["hidden"] * c["n_in"] + c["hidden"] + c["hidden"] + 1


def init_weights(task: str, rng: LCG) -> list[float]:
    c = TASKS[task]
    s1, s2 = 1.0 / math.sqrt(c["n_in"]), 1.0 / math.sqrt(c["hidden"])
    w = [rng.uniform(-s1, s1) for _ in range(c["hidden"] * c["n_in"])]
    w += [0.0] * c["hidden"]
    w += [rng.uniform(-s2, s2) for _ in range(c["hidden"])]
    return w + [0.0]


def forward(task: str, w: list[float], x: tuple) -> tuple[float, list[float]]:
    c = TASKS[task]
    H, k = c["hidden"], c["n_in"]
    h = []
    for j in range(H):
        s = w[H * k + j]
        for i in range(k):
            s += w[j * k + i] * x[i]
        h.append(math.tanh(s))
    z = w[-1]
    for j in range(H):
        z += w[H * k + H + j] * h[j]
    out = z if c["out"] == "linear" else 1.0 / (1.0 + math.exp(-z))
    return out, h


def grad_one(task: str, w: list[float], x: tuple, y: float) -> tuple[float, list[float]]:
    """Per-sample squared error and its analytic gradient (the `grad` cells)."""
    c = TASKS[task]
    H, k = c["hidden"], c["n_in"]
    out, h = forward(task, w, x)
    err = out - y
    dz = 2.0 * err * (1.0 if c["out"] == "linear" else out * (1.0 - out))
    g = [0.0] * len(w)
    for j in range(H):
        g[H * k + H + j] = dz * h[j]
        dh = dz * w[H * k + H + j] * (1.0 - h[j] * h[j])
        g[H * k + j] = dh
        for i in range(k):
            g[j * k + i] = dh * x[i]
    g[-1] = dz
    return err * err, g


def predict(task: str, w: list[float], xs: list[tuple]) -> list[float]:
    return [forward(task, w, x)[0] for x in xs]


def labels(preds: list[float]) -> list[int]:
    return [1 if p >= 0.5 else 0 for p in preds]


# ---- declared cost model ------------------------------------------------------------------

def step_cost(task: str, impl: str) -> dict:
    """Per-step flops and bytes under a DECLARED model: fwd = 2P, bwd = 4P flops per sample,
    update 2P, rounding 2P (rn) / 4P (sr, incl. RNG); a correctly rounded sum (fsum) is
    declared at 4 extra flops per accumulated term (Shewchuk partials, typical case). Weights streamed once per sample for fwd
    and bwd plus one read-modify-write per step at storage width; the gradient buffer is fp64."""
    P, B = n_params(task), TASKS[task]["batch"]
    bw = DTYPE[impl][1]
    rnd = {"fp64": 0, "fp64-rev": 0, "fp32": 2, "bf16-rn": 2, "bf16-sr": 4,
           "fsum": 0, "fsum-rev": 0}[impl]
    flops = 6 * P * B + 2 * P + rnd * P + (4 * P * B if impl in EXACT_SUM else 0)
    nbytes = P * bw * (2 * B + 2) + P * 8
    return {"flops": flops, "bytes": nbytes}


def modeled_ms(flops: int, nbytes: int, device: str) -> float:
    d = DEVICES[device]
    return round(max(flops / d["flops_per_ms"], nbytes / d["bytes_per_ms"]), 9)


# ---- training ----------------------------------------------------------------------------

def train(task: str, impl: str, seed: int, epochs: int | None = None) -> dict:
    """Train one route. Returns final weights, per-epoch receipts, and per-epoch cost."""
    if impl not in IMPLS:
        raise ValueError("unknown impl %r" % impl)
    c = TASKS[task]
    epochs = c["epochs"] if epochs is None else epochs
    data = dataset(task)
    rng = LCG(seed)                              # init + shuffle: SHARED across routes
    sr = LCG(seed ^ 0x5EED5EED)                  # stochastic-rounding bits: own stream
    dtype = DTYPE[impl][0]
    w = [store(impl, v, sr) for v in init_weights(task, rng)]
    B, lr = c["batch"], c["lr"]
    chain, prev = [], "0" * 64
    cost = step_cost(task, impl)
    steps_per_epoch = (len(data) + B - 1) // B
    swallowed = updates = 0          # updates the storage precision rounded back to no-op
    for ep in range(epochs):
        order = rng.shuffle(range(len(data)))
        loss_sum, losses = 0.0, []
        w_in = weight_root(w, dtype)
        for s in range(0, len(order), B):
            idx = order[s:s + B]
            if impl in REVERSED:
                idx = idx[::-1]
            if impl in EXACT_SUM:
                lg = [grad_one(task, w, *data[i]) for i in idx]
                losses += [l for l, _ in lg]
                gsum = [math.fsum(g[p] for _, g in lg) for p in range(len(w))]
            else:
                gsum = [0.0] * len(w)
                for i in idx:
                    l, g = grad_one(task, w, *data[i])
                    loss_sum += l
                    for p in range(len(w)):
                        gsum[p] += g[p]
            n = len(idx)
            new = [store(impl, w[p] - lr * (gsum[p] / n), sr) for p in range(len(w))]
            swallowed += sum(1 for p in range(len(w)) if gsum[p] != 0.0 and new[p] == w[p])
            updates += len(w)
            w = new
        loss = (math.fsum(losses) if impl in EXACT_SUM else loss_sum) / len(data)
        entry = {"v": 2, "seq": ep, "epoch": ep, "impl": impl, "loss": loss,
                 "loss_sha": scalar_sha(loss), "w_in": w_in,
                 "weight_root_sha": weight_root(w, dtype), "prev": prev}
        entry["sha"] = hashlib.sha256(al.canon(entry).encode()).hexdigest()
        prev = entry["sha"]
        chain.append(entry)
    return {"task": task, "impl": impl, "seed": seed, "dtype": dtype, "weights": w,
            "chain": chain, "tip": prev, "final_loss": chain[-1]["loss"],
            "swallowed": swallowed, "updates": updates,
            "flops_per_epoch": cost["flops"] * steps_per_epoch,
            "bytes_per_epoch": cost["bytes"] * steps_per_epoch}


def verify_chain(chain: list[dict]) -> bool:
    """Recompute every link and every loss commitment (quilt-nn's verify, our fields)."""
    prev = "0" * 64
    for i, e in enumerate(chain):
        body = {k: v for k, v in e.items() if k != "sha"}
        if (e.get("seq") != i or e.get("prev") != prev or e.get("loss_sha") != scalar_sha(e["loss"])
                or hashlib.sha256(al.canon(body).encode()).hexdigest() != e.get("sha")):
            return False
        if i and e["w_in"] != chain[i - 1]["weight_root_sha"]:
            return False
        prev = e["sha"]
    return True


# ---- ActiveLog run + ledger.transaction (so B7 / B4 can replay it unmodified) -------------

PRODUCT_LEVELS = ("step", "preds", "labels")


def step_trace(run: dict) -> str:
    """Digest of every epoch's (loss_sha, weight_root) — the whole trajectory, WITHOUT the route
    label (the receipt chain tip carries `impl`, so two routes' tips never match by design)."""
    return hashlib.sha256("|".join(e["loss_sha"] + ":" + e["weight_root_sha"]
                                   for e in run["chain"]).encode()).hexdigest()


def product_of(run: dict, level: str, xs: list[tuple]) -> dict:
    """What a training route PRODUCES, at three strengths:
    step   — the trained weights and the loss digest (what xruntime-conformance compared)
    preds  — the exact float64 predictions on the held-out set (the learned function)
    labels — the decisions on the held-out set (classification only: the product boundary)"""
    task = run["task"]
    base = {"task": task, "heldout": vec_sha([v for x in xs for v in x])}
    if level == "step":
        return {**base, "loss_sha": run["chain"][-1]["loss_sha"], "trace": step_trace(run),
                "weight_root": weight_root(run["weights"], "f64")}
    preds = predict(task, run["weights"], xs)
    if level == "preds":
        return {**base, "preds_sha": vec_sha(preds)}
    if level == "labels":
        if TASKS[task]["out"] != "sigmoid":
            raise ValueError("labels product needs a classifier")
        return {**base, "labels": labels(preds)}
    raise ValueError(level)


def to_activelog(run: dict, level: str, xs: list[tuple], device: str = "edge") -> list[dict]:
    """One ActiveLog v1 slice: one `cell.tick` per epoch (kind train.step), one eval tick,
    one checkpoint tick (storage at rest), closed by one `ledger.transaction`."""
    log = al.ActiveLog(dev="priced-training")
    name = run["impl"]
    total = al.ZERO_BUDGET
    ms_ep = modeled_ms(run["flops_per_epoch"], run["bytes_per_epoch"], device)
    for e in run["chain"]:
        b = al.budget(wall_ms=ms_ep)
        log.emit("cell.tick", {"route": name, "cell": "epoch:%d" % e["epoch"], "kind": "train.step",
                               "impl": name, "in": e["w_in"], "out": e["weight_root_sha"],
                               "loss_sha": e["loss_sha"], "receipt": e["sha"],
                               "flops": run["flops_per_epoch"], "bytes": run["bytes_per_epoch"],
                               "budget": b})
        total = al.add_budget(total, b)
    P = len(run["weights"])
    ev_flops, ev_bytes = 2 * P * len(xs), P * DTYPE[name][1]
    b = al.budget(wall_ms=modeled_ms(ev_flops, ev_bytes, device))
    prod = product_of(run, level, xs)
    log.emit("cell.tick", {"route": name, "cell": "eval", "kind": "eval", "impl": name,
                           "in": run["chain"][-1]["weight_root_sha"], "out": al.content_hash(prod),
                           "flops": ev_flops, "bytes": ev_bytes, "budget": b})
    total = al.add_budget(total, b)
    b = al.budget(prod=P * DTYPE[name][1])
    log.emit("cell.tick", {"route": name, "cell": "checkpoint", "kind": "store", "impl": name,
                           "in": run["chain"][-1]["weight_root_sha"],
                           "out": run["chain"][-1]["weight_root_sha"], "flops": 0, "bytes": 0,
                           "budget": b})
    total = al.add_budget(total, b)
    log.emit("ledger.transaction", {"route": name, "path": name, **prod, "total_budget": total,
                                    "chosen": {"impl": name, "seed": run["seed"], "level": level,
                                               "device": DEVICES[device]["name"],
                                               "final_loss": run["final_loss"]}})
    return log.records
