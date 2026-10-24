"""pincher (B3) — a learned early-exit route: "cheap when confident, else the full route".

    The pincher sits in front of a FULL route and holds a cheap GUESS of the same answer.
    It learns, per input CLASS, how often the guess equalled the full answer. Once the
    confidence for a class clears TARGET it "pinches off" the route and returns the guess
    without running the full route; below TARGET it falls back and runs the full route
    (and keeps learning from it). A deterministic audit slice of pinched calls still runs
    the full route, so a class that drifts is noticed.  (ACTIVELEDGER-CELL-GRAPH.md B3,
    mirroring the quilt-pincher idea; self-contained, no external import.)

Confidence is a conservative pseudo-count lower bound, exact rational arithmetic:

        conf(class) = agree / (n + K)        K phantom disagreements, TARGET = 9/10

  * all-agree evidence: conf = n/(n+K), strictly increasing -> the threshold GROWS with
    evidence and a class flips to "pinch" at n* = ceil(TARGET*K/(1-TARGET)) (closed form,
    `n_star()`); any disagreement leaves `agree` flat while `n` grows, so conf SHRINKS.
  * no float touches the decision (fractions.Fraction), so a run is bit-reproducible.

Product-identity is NOT claimed here — it is CERTIFIED by B7 (labs/system2-backtest):
the pinched run and the full run are replayed, and if their `ledger.transaction` products
differ (a mispinch the audit slice did not catch) B7 refuses and prices nothing. B4
(labs/route-preference) then records which route is preferred when.

Testbed: labs/examples/text-normalize-quilt (lowercase + NFKC/casefold + whitespace
collapse). FULL = unicode path (unicodedata). GUESS = `" ".join(t.lower().split())`
(no NFKC, no casefold): right on ASCII/Cyrillic/most Latin, wrong on ß, ligatures,
fullwidth, decomposed accents, final sigma. CLASS = which codepoint ranges appear in the
text (a range scan, no unicodedata) — coarse on purpose, so some classes are only
*partly* reliable and the pincher must learn to decline them.

Library:  Pincher(guess, full, classify, ...).answer(x) -> (out, info)
          run(text, pincher, log=None) -> {route, out, total_budget, log, info}   (ActiveLog run)
CLI:      python3 pincher.py [--json]      # demo: warm stream, B7 pricing, B4 preferred_when
"""

from __future__ import annotations

import json
import os
import random
import re
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
LABS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LABS, "activeledger"))
sys.path.insert(0, os.path.join(LABS, "system2-backtest"))
sys.path.insert(0, os.path.join(LABS, "route-preference"))
sys.path.insert(0, os.path.join(LABS, "examples", "text-normalize-quilt"))

import activeledger as al  # noqa: E402
import backtest as bt  # noqa: E402
import route_preference as rp  # noqa: E402
import textnorm_quilt as tn  # noqa: E402
from activeledger import ActiveLog, DoubleEntry, budget, add_budget, ZERO_BUDGET  # noqa: E402

TARGET = Fraction(9, 10)      # confidence required to pinch
K = 3                         # phantom disagreements in conf = agree / (n + K)
AUDIT_EVERY = 10              # every 10th pinch in a class still runs the full route


def n_star(target: Fraction = TARGET, k: int = K) -> int:
    """Least all-agree evidence n with n/(n+k) >= target  (closed form)."""
    x = target * k / (1 - target)
    return int(-(-x.numerator // x.denominator))


# ---- the generic early-exit core -----------------------------------------------------

def close(a, b, tol=0) -> bool:
    """Within tolerance: numbers by |a-b| <= tol, everything else (text, tuples) exactly."""
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) \
            and not isinstance(a, bool) and not isinstance(b, bool):
        return abs(a - b) <= tol
    return a == b


class Pincher:
    """Learns per class when `guess` suffices. State is a plain table, a pure function of
    the observation sequence (no clock, no randomness)."""

    def __init__(self, guess, full, classify, tol=0, target=TARGET, k=K, audit_every=AUDIT_EVERY):
        self.guess, self.full, self.classify = guess, full, classify
        self.tol, self.target, self.k, self.audit_every = tol, Fraction(target), k, audit_every
        self.stats: dict[str, dict] = {}
        self.full_calls = 0
        self.calls = 0

    def conf(self, cls: str) -> Fraction:
        s = self.stats.get(cls)
        return Fraction(s["agree"], s["n"] + self.k) if s else Fraction(0)

    def pinchable(self, cls: str) -> bool:
        s = self.stats.get(cls) or {"agree": 0, "n": 0}   # integer cross-multiply == conf >= target
        return s["agree"] * self.target.denominator >= self.target.numerator * (s["n"] + self.k)

    def observe(self, cls: str, agreed: bool) -> None:
        s = self.stats.setdefault(cls, {"agree": 0, "n": 0, "pinched": 0})
        s["n"] += 1
        s["agree"] += 1 if agreed else 0

    def row_bytes(self, cls: str) -> int:
        """Measured size of the learned row this call consults (the `train` storage it reads)."""
        return len(al.canon({cls: self.stats.get(cls, {"agree": 0, "n": 0, "pinched": 0})}).encode())

    def digest(self) -> str:
        return al.content_hash(self.stats)

    def answer(self, x):
        """-> (out, info). info['path'] in {'pinch','audited','fallback'}; info['guess_ok'] is
        None only for an UNAUDITED pinch (nobody checked it — B7 is the backstop)."""
        self.calls += 1
        cls = self.classify(x)
        g = self.guess(x)
        conf_before = self.conf(cls)
        if self.pinchable(cls):
            s = self.stats.setdefault(cls, {"agree": 0, "n": 0, "pinched": 0})
            s["pinched"] += 1
            if s["pinched"] % self.audit_every != 0:
                return g, {"path": "pinch", "cls": cls, "conf": conf_before, "guess_ok": None}
            path = "audited"
        else:
            path = "fallback"
        self.full_calls += 1
        out = self.full(x)
        ok = close(g, out, self.tol)
        self.observe(cls, ok)
        return out, {"path": path, "cls": cls, "conf": conf_before, "guess_ok": ok}


# ---- the testbed: text-normalize --------------------------------------------------------

def tn_guess(text: str) -> str:
    return " ".join(text.lower().split())


def _bucket(o: int) -> str:
    if o < 0x80:
        return "A"                      # ascii
    if o < 0x100:
        return "L"                      # latin-1 (holds é ñ AND ß µ)
    if o < 0x250:
        return "E"                      # latin extended
    if 0x300 <= o < 0x370:
        return "C"                      # combining marks
    if 0x370 <= o < 0x400:
        return "G"                      # greek (final sigma)
    if 0x400 <= o < 0x500:
        return "Y"                      # cyrillic
    if 0x2000 <= o < 0x2190 or 0xFB00 <= o < 0xFB50 or 0xFF00 <= o < 0xFFF0:
        return "K"                      # compat: ligatures, fullwidth, letterlike, roman numerals
    return "O"


_RANGES = re.compile("|".join("(?P<%s>[%s])" % (k, v) for k, v in (
    ("L", "\u0080-\u00ff"), ("E", "\u0100-\u024f"), ("C", "\u0300-\u036f"),
    ("G", "\u0370-\u03ff"), ("Y", "\u0400-\u04ff"),
    ("K", "\u2000-\u218f\ufb00-\ufb4f\uff00-\uffef"))))


def tn_class(text: str) -> str:
    """Which codepoint ranges appear. ASCII fast path first; no unicodedata."""
    if text.isascii():
        return "A"
    seen = {m.lastgroup for m in _RANGES.finditer(text)}
    if any(not (c.isascii() or _bucket(ord(c)) != "O") for c in set(text)):
        seen.add("O")
    return "".join(sorted(seen | ({"A"} if any(c.isascii() for c in text) else set())))


def make_text_pincher(**kw) -> Pincher:
    return Pincher(tn_guess, tn.full_route, tn_class, **kw)


# Pincher route costs: deterministic model in the style of the example quilts (like
# textnorm's COST — declared, not measured). A pinched call is a cheap-route-sized call plus a
# class scan + table row; a fallback pays that overhead AND the full route.
COST = {
    "pinch": {"tick": budget(1, 0.1, 1, 64, 0), "hop": budget(1, 0.05, 1, 16, 64)},
    "full": tn.COST["full"],
}


def _cost_with_row(tick: dict, row_bytes: int) -> dict:
    t = json.loads(json.dumps(tick))
    t["storage_bytes"]["train"] = row_bytes        # measured, not modeled
    return t


def run(text: str, pincher: Pincher, log: ActiveLog | None = None) -> dict:
    """Pincher route for one request, booked to an ActiveLog v1 run. The ledger.transaction
    product ({out}) has the same shape as text-normalize's, so B7 can certify identity."""
    log = log or ActiveLog(dev="pincher")
    rid = "pinch:%s" % al.content_hash(text)
    out, info = pincher.answer(text)
    ran_full = info["path"] != "pinch"
    pc, fc = COST["pinch"], COST["full"]
    total = ZERO_BUDGET

    def tick(cell, cost, **extra):
        nonlocal total
        log.emit("cell.tick", {"route": rid, "cell": cell, "kind": "PINCHER", "path": "pinch",
                               "budget": cost, **extra})
        total = add_budget(total, cost)

    def hop(a, ua, amt, b, ub, cost, ref):
        nonlocal total
        h = DoubleEntry.translate(a, ua, float(amt), b, ub, 1.0, ref)
        log.emit("route.hop", {"route": rid, **h.body(), "budget": cost})
        total = add_budget(total, cost)

    base = fc if ran_full else pc          # a fallback pays the FULL route's own steps ...
    tick("request", base["tick"], units="chars", chars=len(text))
    hop("request", "chars", len(text), "pincher", "codepoints", base["hop"], "chars==codepoints")
    # ... PLUS the pincher's gate (class scan + guess + table row) on top
    tick("pincher", _cost_with_row(pc["tick"], pincher.row_bytes(info["cls"])),
         cls=info["cls"], decision=info["path"], conf="%d/%d" % (info["conf"].numerator, info["conf"].denominator))
    if ran_full:
        hop("pincher", "codepoints", len(text), "normalizer", "codepoints", fc["hop"], "fall back to full")
        tick("normalizer", fc["tick"], out_hash=al.content_hash(out))
        hop("normalizer", "codepoints", len(out), "result", "chars", fc["hop"], "chars==codepoints")
        tick("result", fc["tick"], value=out, units="chars")
    else:
        hop("pincher", "codepoints", len(out), "result", "chars", pc["hop"], "pinched: guess returned")
        tick("result", pc["tick"], value=out, units="chars")
    log.emit("ledger.transaction", {"route": rid, "path": "pinch", "out": out, "total_budget": total})
    return {"route": "pinch", "route_id": rid, "out": out, "total_budget": total, "log": log, "info": info}


# ---- a seeded workload (stdlib random, fixed seed -> identical every run) ---------------

_WORDS = ["Hello", "WORLD", "alpha", "Beta", "gamma", "DATA", "route", "Quilt", "cell", "tick",
          "ledger", "TEXT", "Mixed", "case", "norm", "ONE", "two", "Three", "x1", "Y2"]
_WS = [" ", "  ", "\t", "\n", " \r\n", "\x0b", "\x0c", "\x1c", "   "]
# per-class decoration pools: (safe chars, unsafe chars, P(unsafe))
_POOLS = {   # class -> (safe tokens, unsafe tokens, P(unsafe token))
    "A": ([], [], 0),
    "AE": (["ł", "ő", "ž", "ć", "ę", "č"], ["ŉ"], 0.03),     # rare drift inside a mostly-safe class
    "AY": (["привет", "МИР", "Ёж"], [], 0),
    "AL": (["é", "ñ", "ü", "Å"], ["ß", "µ"], 0.30),            # genuinely mixed class
    "AG": (["α", "β", "γ", "Ω"], ["ς"], 0.40),                 # final sigma
    "AK": ([], ["ﬁne", "Ⅷ", "ＡＢＣ"], 1.0),                    # compat: guess always wrong
    "AC": ([], ["e\u0301"], 1.0),                              # decomposed accent: always wrong
}
MIX_BALANCED = {"A": 55, "AE": 10, "AY": 10, "AL": 10, "AG": 5, "AK": 5, "AC": 5}
MIX_ASCII = {"A": 90, "AE": 5, "AY": 5}
MIX_ADVERSARIAL = {"AK": 50, "AC": 30, "AL": 10, "AG": 10}


def make_workload(n: int, mix: dict, seed: int = 20260929) -> list[str]:
    rnd = random.Random(seed)
    classes, weights = list(mix), [mix[c] for c in mix]
    out = []
    for _ in range(n):
        cls = rnd.choices(classes, weights)[0]
        safe, unsafe, pu = _POOLS[cls]
        toks = [rnd.choice(_WORDS) for _ in range(rnd.randint(2, 6))]
        pool = unsafe if (unsafe and (not safe or rnd.random() < pu)) else safe
        if pool:
            toks.insert(rnd.randint(0, len(toks)), rnd.choice(pool))
        s = "".join(t + rnd.choice(_WS) for t in toks)
        out.append(rnd.choice(_WS) + s)
    return out


# ---- pricing: B7 gate + score, B4 preferred_when -----------------------------------------

def price(texts: list[str], pincher: Pincher | None = None) -> dict:
    """Run the pincher over `texts` (it learns as it goes), run the full route on each, and
    hand BOTH record sets to B7 (gate first) and B4. Returns the workload verdicts + counts."""
    pincher = pincher or make_text_pincher()
    cases, pinned, infos = [], 0, []
    for i, t in enumerate(texts):
        r = run(t, pincher)
        infos.append(r["info"])
        cases.append({"id": "t%d" % i, "a": r["log"].records, "b": tn.run(t, route="full")["log"].records})
    rep = bt.backtest_corpus(cases, ("pinch", "full"))
    book = rp.PreferenceBook()
    sums = {"pinch": [], "full": []}
    for c in cases:
        res = rp.prefer([("pinch", c["a"]), ("full", c["b"])], weights=book.weights)
        if res["status"] == "certified":
            book.observe(res)
            for l in sums:
                sums[l].append(res["routes"][l])
    pref = rp.prefer_axes({l: bt._sum_axes(v) for l, v in sums.items()}, weights=book.weights) if sums["pinch"] else None
    paths = {p: sum(1 for i in infos if i["path"] == p) for p in ("pinch", "audited", "fallback")}
    return {"n": len(texts), "paths": paths, "full_calls": pincher.full_calls, "bt": rep,
            "b4": pref, "book": book, "cases": cases, "pincher": pincher, "infos": infos}


def _fmt(label: str, p: dict) -> str:
    rep, w = p["bt"], p["bt"].get("workload")
    L = ["== %s: n=%d  paths=%s  full-route calls=%d/%d" % (label, p["n"], p["paths"], p["full_calls"], p["n"]),
         "   B7: certified %d, refused %d (mispinches the audit slice missed), inapplicable %d"
         % (rep["certified"], rep["refused"], rep["inapplicable"])]
    if w:
        for lab in ("pinch", "full"):
            x = rep["totals"][lab]
            L.append("   %-6s wall_ms=%-6d usd=%-7s tokens=%-5d storage_bytes=%d"
                     % (lab, x["wall_ms"], x["usd"], x["tokens"], x["storage_bytes"]))
        L.append("   iron-triangle: %s  axes=%s  cheap=%s" % (w["class"], w["axes"], w["cheap_detail"]))
        if p["b4"]:
            L.append("   B4 preferred_when: %s" % p["b4"]["preferred_when"])
    return "\n".join(L)


def timing(texts: list[str]) -> dict:
    """REAL wall time (perf_counter_ns) of guess vs full over a workload — measured, not modeled."""
    out = {}
    for name, fn in (("guess", tn_guess), ("full", tn.full_route), ("class-scan", tn_class)):
        t0 = time.perf_counter_ns()
        for _ in range(20):
            for t in texts:
                fn(t)
        out[name + "_ns_per_call"] = (time.perf_counter_ns() - t0) // (20 * len(texts))
    return out


def timing_stream(texts: list[str]) -> dict:
    """REAL end-to-end ns/call: warmed pincher.answer vs the full route, same texts."""
    p = make_text_pincher()
    for t in texts:
        p.answer(t)
    t0 = time.perf_counter_ns()
    for _ in range(10):
        for t in texts:
            p.answer(t)
    a = (time.perf_counter_ns() - t0) // (10 * len(texts))
    t0 = time.perf_counter_ns()
    for _ in range(10):
        for t in texts:
            tn.full_route(t)
    f = (time.perf_counter_ns() - t0) // (10 * len(texts))
    return {"pincher_ns_per_call": a, "full_ns_per_call": f}


if __name__ == "__main__":
    mixes = (("ascii-heavy", MIX_ASCII), ("balanced", MIX_BALANCED), ("adversarial", MIX_ADVERSARIAL))
    res = {n: price(make_workload(600, m)) for n, m in mixes}
    if "--json" in sys.argv:
        print(json.dumps({n: {"paths": p["paths"], "full_calls": p["full_calls"],
                              "b7": {k: p["bt"][k] for k in ("certified", "refused", "totals", "workload") if k in p["bt"]},
                              "b4": p["b4"]} for n, p in res.items()}, sort_keys=True, indent=1))
    else:
        for n, p in res.items():
            print(_fmt(n, p))
        print("real ns/call (components, balanced):", timing(make_workload(200, MIX_BALANCED)))
        for n, m in mixes:
            print("real ns/call end-to-end, %-11s" % n, timing_stream(make_workload(600, m)))
