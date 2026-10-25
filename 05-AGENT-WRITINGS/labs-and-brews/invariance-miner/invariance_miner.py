#!/usr/bin/env python3
"""invariance_miner.py — the receipt log is a free dataset of your program's symmetries.

THE LATENT TOOL. Every quilt cell already writes a receipt: input -> output digest. Read the log the
other way round and it becomes evidence about the cell's INVARIANCES. If two different inputs x, x'
share an output digest and a candidate transform t maps both to the same key t(x) = t(x'), that is
support for "f(t(x)) == f(x)". If a transform's bucket ever contains two different digests, the
transform is refuted outright. Mining costs zero extra calls to the cell, because the evidence was
already paid for.

The mined invariances become a CANONICALIZER: the cache key is canon(x) instead of x. More requests
hit the cache. The differ still guards product identity: a canonicalizer is kept only if it
(a) survives the log and (b) survives k active checks f(canon(x)) == f(x) on drawn logged inputs.

Measured on two real cells from labs/examples (text-normalize FULL route, convert FULL route), with
traps planted in the transform library (strip_punct, sort_words, trunc16, round3). The traffic
distribution shifts between the mining window and the serving window. The run shows:
  * how much cache hit rate the mined canonicalizer adds over exact-key caching;
  * that LOG-ONLY acceptance can adopt a trap that happens to be consistent on the log
    (trunc16: the log never held two inputs sharing 16 chars with different outputs), which then
    serves WRONG products after the shift;
  * that a handful of active differ checks (k draws) removes the trap, with 0 false hits.

    python3 invariance_miner.py       # report
    python3 selftest.py               # checks
"""

from __future__ import annotations

import os
import random
import string
import sys
import unicodedata
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "activeledger"))
sys.path.insert(0, os.path.join(HERE, "..", "examples", "text-normalize-quilt"))
sys.path.insert(0, os.path.join(HERE, "..", "examples", "convert-quilt"))
from activeledger import fnv1a64, canon as jcanon  # noqa: E402
import textnorm_quilt as tn  # noqa: E402
import convert_quilt as cq  # noqa: E402


def digest(y) -> str:
    return "0x%016x" % fnv1a64(jcanon(y))


# ---- the cells under study (unmodified example-quilt code) -------------------------------------

class Cell:
    """Wraps f so every call is counted and receipted (input, output digest)."""

    def __init__(self, name, f):
        self.name, self.f, self.calls = name, f, 0

    def __call__(self, x):
        self.calls += 1
        try:
            return self.f(x)
        except Exception as e:  # an error is a product too; it must be identical to count
            return "ERR:%s" % type(e).__name__

    def receipts(self, xs):
        return [(x, digest(self(x))) for x in xs]


def text_cell():
    return Cell("text-normalize/full", tn.full_route)


def convert_cell():
    return Cell("convert/full", lambda x: cq.full_route(*x))


# ---- candidate transform libraries (with planted traps) ----------------------------------------

_PUNCT = str.maketrans("", "", string.punctuation)
TEXT_T = {
    "casefold": str.casefold,
    "lower": str.lower,
    "strip": str.strip,
    "collapse_ws": lambda s: " ".join(s.split()),
    "nfkc": lambda s: unicodedata.normalize("NFKC", s),
    "strip_punct": lambda s: s.translate(_PUNCT),         # trap: normalize keeps punctuation
    "sort_words": lambda s: " ".join(sorted(s.split())),  # trap: order matters
    "trunc16": lambda s: s[:16],                          # trap: consistent only on short-diverging logs
}


def _num(v: str) -> str:
    return str(Fraction(v))


def _round3(v: str) -> str:
    return str(round(Fraction(v), 3))


CONV_T = {
    "canon_number": lambda x: (_num(x[0]), x[1], x[2]),
    "strip_plus": lambda x: (x[0].lstrip("+"), x[1], x[2]),
    "round3": lambda x: (_round3(x[0]), x[1], x[2]),                 # trap
    "unit_lower": lambda x: (x[0], x[1].lower(), x[2].lower()),      # trap: 'K' is not 'k'
    "swap_units": lambda x: (x[0], x[2], x[1]),                      # trap: direction matters
}


def _safe(t, x):
    try:
        return t(x)
    except Exception:
        return ("__T_ERR__", repr(x))


# ---- mining ------------------------------------------------------------------------------------

def mine(log, transforms, min_support=3):
    """LOG-ONLY. For each transform t: bucket logged inputs by t(x).
    refuted  <- some bucket holds >= 2 distinct digests (f(t(x)) == f(x) cannot hold for both)
    support  = # of logged inputs x that share a bucket with a DIFFERENT input x' (collision evidence)
    accepted <- not refuted and support >= min_support. Costs zero cell calls."""
    out = {}
    for name, t in transforms.items():
        buckets = {}
        for x, d in log:
            buckets.setdefault(jcanon(_safe(t, x)), {}).setdefault(x if isinstance(x, str) else jcanon(x), d)
        refuted = any(len(set(b.values())) > 1 for b in buckets.values())
        support = sum(len(b) for b in buckets.values() if len(b) > 1)
        out[name] = {"refuted": refuted, "support": support,
                     "accepted": (not refuted) and support >= min_support}
    return out


def compose(names, transforms):
    ts = [transforms[n] for n in names]

    def c(x):
        for t in ts:
            x = _safe(t, x)
        return x
    c.names = list(names)
    return c


def build_canon(log, transforms, mined, min_support=3):
    """Greedy composition by support; re-check the composite on the log (pairwise-valid transforms
    need not compose once they are only verified on a sample)."""
    chosen = []
    for n in sorted((n for n, m in mined.items() if m["accepted"]), key=lambda n: -mined[n]["support"]):
        trial = compose(chosen + [n], transforms)
        if not mine(log, {"_": trial}, 0)["_"]["refuted"]:
            chosen.append(n)
    return compose(chosen, transforms)


def n_buckets(log, key) -> int:
    return len({jcanon(_safe(key, x)) for x, _ in log})


def build_canon_occam(log, transforms, mined, min_gain=3):
    """OCCAM GUARD: add a transform only if it MERGES >= min_gain more logged inputs than the chain
    already does, and the composite stays unrefuted. A transform whose extra coarsening no receipt
    pays for (round3 after canon_number, sort_words after collapse_ws/casefold) is never adopted:
    its merges are pure off-support risk."""
    chosen = []
    cur = n_buckets(log, compose([], transforms))
    for n in sorted((n for n, m in mined.items() if m["accepted"]), key=lambda n: -mined[n]["support"]):
        trial = compose(chosen + [n], transforms)
        nb = n_buckets(log, trial)
        if cur - nb >= min_gain and not mine(log, {"_": trial}, 0)["_"]["refuted"]:
            chosen.append(n)
            cur = nb
    return compose(chosen, transforms)


def verify_active(cell, log, transforms, names, k, rng):
    """Active differ check: for k logged inputs drawn at random (restricted to ones the transform
    actually moves), run f(t(x)) and compare with the logged digest. Costs <= k calls per transform."""
    kept, spent = [], 0
    by_x = dict(log)
    for n in names:
        t = transforms[n]
        moved = [x for x, _ in log if _safe(t, x) != x]
        rng.shuffle(moved)
        ok = True
        for x in moved[:k]:
            spent += 1
            if digest(cell(_safe(t, x))) != by_x[x]:
                ok = False
                break
        if ok:
            kept.append(n)
    return kept, spent


# ---- traffic -----------------------------------------------------------------------------------

TEXT_INTENTS_A = ["the cat sat on the mat", "man bites dog", "hello world", "route pricing is a join", "B7 gates identity",
                  "quilt cells tick", "Straße und Brücke", "ﬁle ﬂow ok", "café naïve", "Ｆｕｌｌ width",
                  "budget vector, storage bytes!", "receipts: hash-chained", "A.B.C. test"]
# shift: new intents that share a 16-char prefix with DIFFERENT meanings (the trunc16 trap springs)
TEXT_INTENTS_B = ["dog bites man", "the cat sat on the hat", "the cat sat on the rug", "route pricing is a market",
                  "quilt cells tock", "receipts: hash-linked"]


def _surface(s, rng):
    """Surface variation a real user produces: case, spacing, padding, fullwidth, punctuation kept."""
    w = s.split()
    r = rng.random()
    if r < 0.25:
        s2 = s.upper()
    elif r < 0.5:
        s2 = s.title()
    elif r < 0.6:
        s2 = unicodedata.normalize("NFKC", s).swapcase()
    else:
        s2 = s
    if rng.random() < 0.4:
        s2 = ("  " if rng.random() < 0.5 else "\t").join(s2.split())
    if rng.random() < 0.3:
        s2 = " " * rng.randint(1, 3) + s2 + " " * rng.randint(0, 3)
    del w
    return s2


def _zipf(rng, items, a=1.1):
    weights = [1 / (i + 1) ** a for i in range(len(items))]
    return rng.choices(items, weights)[0]


def text_traffic(n, seed, shifted=False):
    rng = random.Random(seed)
    pool = TEXT_INTENTS_A + (TEXT_INTENTS_B if shifted else [])
    return [_surface(_zipf(rng, pool), rng) for _ in range(n)]


CONV_INTENTS_A = [("1.5", "km", "m"), ("12", "in", "cm"), ("100", "C", "F"), ("2", "lb", "kg"),
                  ("0.25", "ft", "in"), ("300", "K", "C"), ("5", "kg", "lb"), ("3.5", "m", "ft")]
CONV_INTENTS_B = [("1.5004", "km", "m"), ("12.0006", "in", "cm"), ("100", "F", "C")]


def _num_surface(v, rng):
    r = rng.random()
    if r < 0.25:
        return v + "0" * rng.randint(1, 3) if "." in v else v + ".0"
    if r < 0.4:
        return "+" + v
    if r < 0.5:
        return "0" + v
    return v


def conv_traffic(n, seed, shifted=False):
    rng = random.Random(seed)
    pool = CONV_INTENTS_A + (CONV_INTENTS_B if shifted else [])
    out = []
    for _ in range(n):
        v, s, d = _zipf(rng, pool)
        out.append((_num_surface(v, rng), s, d))
    return out


# ---- serving: exact-key cache vs canonical-key cache -------------------------------------------

def serve(cell, stream, key):
    cache, hits, false_hits = {}, 0, 0
    calls0 = cell.calls
    for x in stream:
        k = jcanon(key(x))
        if k in cache:
            hits += 1
            if cache[k] != cell.f_safe(x):   # ground truth (scored, not billed)
                false_hits += 1
        else:
            cache[k] = cell(x)
    return {"hit_rate": hits / len(stream), "false_hits": false_hits, "cell_calls": cell.calls - calls0,
            "distinct_keys": len(cache)}


def _truth(cell):
    def g(x):
        try:
            return cell.f(x)
        except Exception as e:
            return "ERR:%s" % type(e).__name__
    return g


def study(cell, transforms, traffic, n_log=600, n_serve=3000, k=8, seed=0, min_support=3):
    cell.f_safe = _truth(cell)
    log_inputs = traffic(n_log, seed, shifted=False)
    c0 = cell.calls
    log = cell.receipts(log_inputs)            # the receipts the cell writes anyway
    log_calls = cell.calls - c0
    mined = mine(log, transforms, min_support)
    mining_calls = cell.calls - c0 - log_calls  # must be 0
    canon_log_only = build_canon(log, transforms, mined, min_support)
    rng = random.Random(seed + 1)
    kept, spent = verify_active(cell, log, transforms, canon_log_only.names, k, rng)
    canon_verified = compose(kept, transforms)
    canon_occam = build_canon_occam(log, transforms, mined, min_support)
    kept2, spent2 = verify_active(cell, log, transforms, canon_occam.names, k, random.Random(seed + 2))
    canon_guarded = compose(kept2, transforms)
    stream = traffic(n_serve, seed + 100, shifted=True)
    return {"cell": cell.name, "n_log": n_log, "n_serve": n_serve, "k": k,
            "mined": mined, "mining_calls": mining_calls,
            "log_only_chain": canon_log_only.names, "verified_chain": canon_verified.names,
            "verify_calls": spent, "guarded_chain": canon_guarded.names, "guarded_calls": spent2,
            "exact_key": serve(cell, stream, lambda x: x),
            "log_only": serve(cell, stream, canon_log_only),
            "verified": serve(cell, stream, canon_verified),
            "guarded": serve(cell, stream, canon_guarded)}


MODES = ("exact_key", "log_only", "verified", "guarded")


def seeds_sweep(cell_fn, transforms, traffic, seeds=range(20), **kw):
    agg = {"exact_key": [], "log_only": [], "verified": [], "guarded": [],
           "trap_adopted_log_only": 0, "trap_in_verified": 0, "trap_in_guarded": 0}
    traps = {"strip_punct", "sort_words", "trunc16", "round3", "unit_lower", "swap_units"}
    for s in seeds:
        r = study(cell_fn(), transforms, traffic, seed=s, **kw)
        for m in MODES:
            agg[m].append(r[m])
        agg["trap_in_guarded"] += bool(traps & set(r["guarded_chain"]))
        agg["trap_adopted_log_only"] += bool(traps & set(r["log_only_chain"]))
        agg["trap_in_verified"] += bool(traps & set(r["verified_chain"]))
    n = len(list(seeds))

    def mean(m, f):
        return sum(x[f] for x in agg[m]) / n
    return {"runs": n, **{m: {"hit_rate": mean(m, "hit_rate"), "false_hits": mean(m, "false_hits"),
                              "cell_calls": mean(m, "cell_calls")} for m in MODES},
            "trap_adopted_log_only": agg["trap_adopted_log_only"], "trap_in_verified": agg["trap_in_verified"],
            "trap_in_guarded": agg["trap_in_guarded"]}


def report():
    out = {}
    for label, cf, T, tr in (("text", text_cell, TEXT_T, text_traffic), ("convert", convert_cell, CONV_T, conv_traffic)):
        out[label] = {"one": study(cf(), T, tr, seed=0), "sweep": seeds_sweep(cf, T, tr)}
    return out


def _fmt(rep):
    L = ["invariance-miner — receipts as a symmetry dataset -> canonical cache keys (differ-guarded)", ""]
    for label, r in rep.items():
        o, s = r["one"], r["sweep"]
        L.append("[%s]  cell=%s  log=%d receipts  serve=%d (shifted traffic)  active checks k=%d" % (
            label, o["cell"], o["n_log"], o["n_serve"], o["k"]))
        L.append("  mined from the log (cell calls spent mining: %d):" % o["mining_calls"])
        for n, m in o["mined"].items():
            L.append("    %-13s %-9s support=%d" % (n, "REFUTED" if m["refuted"] else ("accepted" if m["accepted"] else "unknown"),
                                                   m["support"]))
        L.append("  log-only canonicalizer: %s" % (" ∘ ".join(o["log_only_chain"]) or "(identity)"))
        L.append("  verified canonicalizer: %s   (%d active cell calls)" % (" ∘ ".join(o["verified_chain"]) or "(identity)",
                                                                           o["verify_calls"]))
        L.append("  occam+verified (GUARDED): %s   (%d active cell calls)" % (" ∘ ".join(o["guarded_chain"]) or "(identity)",
                                                                             o["guarded_calls"]))
        L.append("  sweep over %d seeds (mean per run):" % s["runs"])
        for m in MODES:
            L.append("    %-10s hit rate %.3f   cell calls %6.1f   FALSE HITS %.2f" % (
                m, s[m]["hit_rate"], s[m]["cell_calls"], s[m]["false_hits"]))
        L.append("    trap adopted: log-only %d/%d | after active check %d/%d | guarded %d/%d" % (
            s["trap_adopted_log_only"], s["runs"], s["trap_in_verified"], s["runs"], s["trap_in_guarded"], s["runs"]))
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    print(_fmt(report()))
