#!/usr/bin/env python3
"""audit_lottery.py — license a cheap route with spot-checks it cannot predict, and revoke the
license the moment the evidence says it stopped being product-identical.

THE LATENT TOOL. The quilt already has:
  * a differ (B7) that says whether two routes gave the *identical product*;
  * hash-chained receipts (situation-recorder / activeledger);
  * un-gameable draws (Moth QRNG / MicroMoth);
  * anytime-valid e-processes (sibling repo quilt-ewitness).
Nobody had put the four together. Composed, they give a **certified cascade**: serve the cheap
route, but for each request first make it COMMIT its output hash into the chain, THEN draw an audit
bit it could not have known, and on an audit run the exact route through the differ. Each audit
result feeds a Bernoulli e-process on "disagreement rate <= eps". When the e-process crosses 1/delta
the cheap route's license is REVOKED — Ville's inequality bounds the false-revocation rate by delta
at every stopping time, so it can be checked after every request.

Why the ORDER in the chain is the security property: if the cheap route can see the audit bit before
committing, it answers carefully only when watched. COMMIT -> DRAW -> AUDIT, hash-chained, is a
receipt that it could not. And why the DRAW SOURCE matters: a *seeded, replayable* source (a public
PRNG seed, or a seeded MicroMoth circuit) is as predictable as no audit at all to anyone holding the
seed. The lab measures exactly that difference.

    python3 audit_lottery.py            # full report (all scenarios)
    python3 selftest.py                 # checks

Stdlib only. Real product pair: the text-normalize example quilt (labs/examples/text-normalize-quilt)
— its FULL unicode route is the exact route; a plausible "lazy" shortcut (str.lower + split, no
NFKC/casefold) is the cheap route that is product-identical on ASCII and silently drifts on unicode.
"""

from __future__ import annotations

import json
import os
import random
import secrets
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "activeledger"))
sys.path.insert(0, os.path.join(HERE, "..", "examples", "text-normalize-quilt"))
from activeledger import fnv1a64, canon  # noqa: E402
import textnorm_quilt as tn  # noqa: E402

# Costs come from the example quilt's own deterministic cost model (wall_ms of the tick).
CHEAP_COST = tn.COST["cheap"]["tick"]["wall_ms"]   # 1
EXACT_COST = tn.COST["full"]["tick"]["wall_ms"]    # 3


# ---- receipts: COMMIT -> DRAW -> AUDIT -> LICENSE, fnv1a-64 chained -------------------------

class Chain:
    def __init__(self):
        self.records: list[dict] = []
        self.head = "0x" + "0" * 16

    def append(self, rel: str, body: dict) -> dict:
        rec = {"seq": len(self.records), "rel": rel, "body": body, "prev": self.head}
        rec["hash"] = "0x%016x" % fnv1a64(self.head + canon({"rel": rel, "body": body}))
        self.records.append(rec)
        self.head = rec["hash"]
        return rec

    def verify(self) -> tuple[bool, int | None]:
        """Hash chain intact? Returns (ok, first bad seq)."""
        h = "0x" + "0" * 16
        for r in self.records:
            want = "0x%016x" % fnv1a64(h + canon({"rel": r["rel"], "body": r["body"]}))
            if r["prev"] != h or r["hash"] != want:
                return False, r["seq"]
            h = r["hash"]
        return True, None

    def order_ok(self) -> tuple[bool, str]:
        """The security property: for every item, COMMIT precedes DRAW precedes AUDIT, and the
        audited output hash equals the committed one (no answer swapped after the draw)."""
        seen: dict[int, dict] = {}
        for r in self.records:
            b, i = r["body"], r["body"].get("item")
            if r["rel"] == "COMMIT":
                seen[i] = {"commit": b["out_hash"], "draw": False}
            elif r["rel"] == "DRAW":
                if i not in seen:
                    return False, "DRAW before COMMIT at item %s" % i
                seen[i]["draw"] = True
            elif r["rel"] == "AUDIT":
                if i not in seen or not seen[i]["draw"]:
                    return False, "AUDIT without COMMIT+DRAW at item %s" % i
                if b["cheap_hash"] != seen[i]["commit"]:
                    return False, "answer swapped after draw at item %s" % i
        return True, "ok"


def out_hash(y: str) -> str:
    return "0x%016x" % fnv1a64(y)


# ---- draw sources -----------------------------------------------------------------------------

class Exhausted(Exception):
    pass


class PublicSeedDraws:
    """A seeded, replayable source (a PRNG with a published seed, or a seeded MicroMoth circuit).
    Receipts replay perfectly — which is exactly why anyone holding the seed can predict it."""
    name = "public-seed (replayable)"
    predictable = True

    def __init__(self, seed: int):
        self.rng = random.Random(seed)

    def bits(self, k: int) -> int:
        return self.rng.getrandbits(k)

    def peek(self, k: int) -> int:
        st = self.rng.getstate()
        v = self.rng.getrandbits(k)
        self.rng.setstate(st)
        return v


class SecretDraws:
    """OS CSPRNG — secret to the audited route at commit time (stand-in for a live QRNG)."""
    name = "secret (os CSPRNG)"
    predictable = False

    def bits(self, k: int) -> int:
        return secrets.randbits(k)


class PoolDraws:
    """A finite pool of bytes fetched from Moth comet-qrng-v1 (see moth_draws.json)."""
    predictable = False

    def __init__(self, hexstr: str, name: str):
        self.buf = bytes.fromhex(hexstr)
        self.pos = 0  # in bits
        self.name = name

    def bits(self, k: int) -> int:
        if self.pos + k > len(self.buf) * 8:
            raise Exhausted()
        v = 0
        for _ in range(k):
            byte = self.buf[self.pos // 8]
            v = (v << 1) | ((byte >> (7 - self.pos % 8)) & 1)
            self.pos += 1
        return v


def load_moth_pool() -> PoolDraws | None:
    p = os.path.join(HERE, "moth_draws.json")
    if not os.path.exists(p):
        return None
    fx = json.load(open(p))
    if not fx.get("hex"):
        return None
    return PoolDraws(fx["hex"], "moth comet-qrng-v1 job %s (%s/%s, S=%.3f)" % (
        fx["job_id"][:8], fx.get("mode"), fx.get("backend"), fx.get("bell_S") or 0))


K_BITS = 8  # audit iff draw < round(p * 2^K)


# ---- the anytime-valid e-process ---------------------------------------------------------------

class BernoulliEProcess:
    """Tests H0: P(disagree) <= eps with a mixture of betting martingales
    E_t = mean_j prod_i (1 + lam_j (x_i - eps)),  lam_j in (0, 1/eps).
    Under H0 each factor has conditional mean <= 1, so E_t is a nonnegative supermartingale and
    Ville gives P(sup_t E_t >= 1/delta) <= delta: it may be checked after every audit."""

    def __init__(self, eps: float, delta: float, grid: int = 9):
        self.eps, self.delta = eps, delta
        self.lams = [(j / (grid + 1)) / eps for j in range(1, grid + 1)]
        self.w = [1.0] * len(self.lams)
        self.n = 0
        self.max = 1.0

    def update(self, x: int) -> float:
        self.n += 1
        self.w = [w * (1 + lam * (x - self.eps)) for w, lam in zip(self.w, self.lams)]
        self.max = max(self.max, self.value)
        return self.value

    @property
    def value(self) -> float:
        return sum(self.w) / len(self.w)

    @property
    def crossed(self) -> bool:
        return self.value >= 1.0 / self.delta


class SRDetector(BernoulliEProcess):
    """Shiryaev-Roberts e-detector: R_t = f_t * (R_{t-1} + 1), averaged over the same lambda grid.
    Under H0, E[R_t] <= t, so the mean number of audits to a false alarm is >= the threshold A.
    It forgets old clean history (restarts implicitly), so a long honest past buys no cover for a
    later drift — the fix for the Ville license's 'trust credit' (see exp_trust_credit).
    Guarantee is ARL (mean time to false alarm >= A), NOT Ville's 'never, w.p. 1-delta'."""

    def __init__(self, eps: float, A: float, grid: int = 9):
        super().__init__(eps, 1.0 / A, grid)
        self.w = [0.0] * len(self.lams)

    def update(self, x: int) -> float:
        self.n += 1
        self.w = [(w + 1) * (1 + lam * (x - self.eps)) for w, lam in zip(self.w, self.lams)]
        self.max = max(self.max, self.value)
        return self.value


# ---- routes -------------------------------------------------------------------------------------

def exact_route(x: str) -> str:
    return tn.full_route(x)


def guarded_cheap(x: str) -> str:
    """The shipped quilt: cheap bytes path iff ASCII, else full — product-identical by proof."""
    return tn.cheap_route(x) if x.isascii() else tn.full_route(x)


def lazy_cheap(x: str) -> str:
    """The plausible shortcut someone ships: no NFKC, lower() instead of casefold()."""
    return " ".join(x.lower().split())


def cheater(base, oracle=None, blind_rate: float = 0.0, rng=None):
    """A strategic contractor route: returns an unprocessed (stale) answer when it believes no one
    is watching. With an oracle (it can predict the audit draw) it cheats on every unaudited item;
    without one it can only cheat blindly at `blind_rate`."""
    rng = rng or random.Random(7)

    def f(x: str, will_audit: bool | None) -> str:
        if will_audit is not None:
            return base(x) if will_audit else x          # perfect prediction: cheat when unwatched
        return x if rng.random() < blind_rate else base(x)
    f.uses_oracle = oracle is not None
    return f


# ---- the stream ---------------------------------------------------------------------------------

ASCII_POOL = ["Hello   World", "  The CAT sat\ton the mat ", "Route\x1cPricing  IS  a join",
              "B7 gates PRODUCT identity", "quilt\n\ncells", "MiXeD   case\r\nlines", "abc DEF ghi"]
UNICODE_POOL = ["Straße", "ﬁle ﬂow", "Ｆｕｌｌｗｉｄｔｈ", "ΣΊΣΥΦΟΣ", "naïve café", "İstanbul",
                "Ǆemal", "Ångström  unit", "ﬀ ligature", "ǅ titlecase", "東京 タワー", "Ⅻ o'clock"]


def make_stream(n: int, onset: int | None, uni_frac: float, seed: int) -> list[str]:
    rng = random.Random(seed)
    out = []
    for i in range(n):
        if onset is not None and i >= onset and rng.random() < uni_frac:
            out.append(rng.choice(UNICODE_POOL) + " " + rng.choice(ASCII_POOL))
        else:
            out.append(rng.choice(ASCII_POOL))
    return out


def run_stream(items, cheap, source, p: float, eps: float = 0.01, delta: float = 0.05,
               chain: Chain | None = None, tamper_at: int | None = None, detector=None) -> dict:
    """Serve a stream under the audit lottery. `cheap(x, will_audit)`; will_audit is only non-None
    when the cheap route can PREDICT the draw (source.predictable and cheap.uses_oracle)."""
    chain = chain or Chain()
    ep = detector or BernoulliEProcess(eps, delta)
    thresh = round(p * (1 << K_BITS))
    licensed, revoked_at = True, None
    cost = harm = audits = served_cheap = 0
    exhausted = False
    for i, x in enumerate(items):
        truth = exact_route(x)
        if not licensed:
            cost += EXACT_COST
            continue
        peek = None
        if getattr(cheap, "uses_oracle", False) and getattr(source, "predictable", False):
            peek = source.peek(K_BITS) < thresh
        y = cheap(x, peek)
        chain.append("COMMIT", {"item": i, "out_hash": out_hash(y)})
        try:
            v = source.bits(K_BITS)
        except Exhausted:
            exhausted = True
            break
        audit = v < thresh
        chain.append("DRAW", {"item": i, "source": source.name, "value": v, "audit": audit})
        cost += CHEAP_COST
        served_cheap += 1
        if tamper_at == i and audit:
            y = truth  # a provider swapping in the right answer AFTER seeing it is watched
        if audit:
            audits += 1
            cost += EXACT_COST
            agree = (y == truth)
            chain.append("AUDIT", {"item": i, "cheap_hash": out_hash(y), "exact_hash": out_hash(truth),
                                   "agree": agree, "E": round(ep.update(0 if agree else 1), 6)})
            if ep.crossed:
                licensed, revoked_at = False, i
                chain.append("LICENSE", {"item": i, "state": "REVOKED", "E": round(ep.value, 3),
                                         "bar": round(1 / ep.delta, 3), "audits": audits,
                                         "detector": type(ep).__name__})
        if y != truth:
            harm += 1  # a wrong product actually served (scored with ground truth, never billed)
    n = i + 1 if not exhausted else i
    return {"n": n, "cost": cost, "harm": harm, "audits": audits, "served_cheap": served_cheap,
            "revoked_at": revoked_at, "E_max": ep.max, "exhausted": exhausted, "chain": chain}


# ---- experiments --------------------------------------------------------------------------------

def _mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float("nan")


def exp_drift(R=200, N=3000, onset=1000, uni=0.3, p=1 / 16):
    """Honest drift: the lazy route is identical on ASCII, then unicode arrives at `onset`."""
    rows = []
    for r in range(R):
        items = make_stream(N, onset, uni, seed=1000 + r)
        rows.append(run_stream(items, lambda x, _: lazy_cheap(x), SecretDraws(), p))
    det = [x["revoked_at"] - onset for x in rows if x["revoked_at"] is not None]
    pre = sum(1 for x in rows if x["revoked_at"] is not None and x["revoked_at"] < onset)
    # the true post-onset disagreement rate of the lazy route, measured, not assumed
    items = make_stream(20000, 0, uni, seed=99)
    q = _mean(lazy_cheap(x) != exact_route(x) for x in items)
    no_audit_harm = _mean(sum(lazy_cheap(x) != exact_route(x) for x in make_stream(N, onset, uni, 1000 + r))
                          for r in range(R))
    return {"R": R, "N": N, "onset": onset, "p": p, "true_post_onset_disagree": q,
            "revoked_frac": _mean(x["revoked_at"] is not None for x in rows),
            "revoked_before_onset": pre,
            "detect_delay_mean": _mean(det), "detect_delay_max": max(det) if det else None,
            "harm_mean": _mean(x["harm"] for x in rows), "harm_no_audit": no_audit_harm,
            "cost_mean": _mean(x["cost"] for x in rows), "cost_always_exact": N * EXACT_COST,
            "cost_always_cheap": N * CHEAP_COST}


def exp_strategic(R=200, N=3000, p=1 / 16, blind=0.2):
    """A contractor that cheats when unwatched. Public-seed draws vs secret draws."""
    out = {}
    for label, mk_src, mk_cheat in [
        ("public-seed + oracle", lambda r: PublicSeedDraws(r), lambda r: cheater(guarded_cheap, oracle=True)),
        ("secret + blind cheat", lambda r: SecretDraws(), lambda r: cheater(guarded_cheap, None, blind, random.Random(r))),
    ]:
        rows = []
        for r in range(R):
            items = make_stream(N, None, 0.0, seed=5000 + r)
            rows.append(run_stream(items, mk_cheat(r), mk_src(r), p))
        out[label] = {"revoked_frac": _mean(x["revoked_at"] is not None for x in rows),
                      "harm_mean": _mean(x["harm"] for x in rows),
                      "harm_frac_of_N": _mean(x["harm"] for x in rows) / N,
                      "revoked_at_mean": _mean(x["revoked_at"] for x in rows if x["revoked_at"] is not None),
                      "E_max_mean": _mean(x["E_max"] for x in rows)}
    return {"R": R, "N": N, "p": p, "blind_rate": blind, **out}


def exp_false_revocation(R=1000, n_audits=2000, eps=0.01, delta=0.05):
    """Validity under H0: a route disagreeing at exactly eps (the boundary) or eps/2 must be revoked
    at most delta of the time, even though the e-process is checked after every audit."""
    res = {}
    rng = random.Random(123)
    for q in (eps, eps / 2, 0.0):
        fired = 0
        for _ in range(R):
            ep = BernoulliEProcess(eps, delta)
            for _ in range(n_audits):
                ep.update(1 if rng.random() < q else 0)
                if ep.crossed:
                    fired += 1
                    break
        res["q=%g" % q] = fired / R
    return {"R": R, "audits_per_run": n_audits, "eps": eps, "delta": delta, "revoked_frac": res}


SR_A = 40000  # ARL target in audits: ~ (license lifetime 2000 audits) / delta 0.05


def exp_trust_credit(R=100, onsets=(0, 1000, 4000, 16000), uni=0.3, p=1 / 16, post=3000):
    """Counterintuitive: under a Ville license, clean audits DRAIN the betting wealth, so the longer a
    route has been honest the longer a later drift runs undetected. Shiryaev-Roberts doesn't drain."""
    rows = []
    for onset in onsets:
        row = {"onset": onset}
        for name, mk in (("ville", lambda: BernoulliEProcess(0.01, 0.05)), ("sr", lambda: SRDetector(0.01, SR_A))):
            rs = [run_stream(make_stream(onset + post, onset, uni, 3000 + r), lambda x, _: lazy_cheap(x),
                             SecretDraws(), p, detector=mk()) for r in range(R)]
            det = [x["revoked_at"] - onset for x in rs if x["revoked_at"] is not None and x["revoked_at"] >= onset]
            row[name] = {"detect_delay_mean": _mean(det), "missed_frac": _mean(
                x["revoked_at"] is None for x in rs), "false_before_onset": sum(
                1 for x in rs if x["revoked_at"] is not None and x["revoked_at"] < onset),
                "harm_mean": _mean(x["harm"] for x in rs)}
        rows.append(row)
    return {"R": R, "p": p, "post_onset_items": post, "SR_A": SR_A, "rows": rows}


def exp_sr_false_alarm(R=400, n_audits=2000, eps=0.01):
    """SR validity at the boundary: false alarms within a 2000-audit license lifetime."""
    rng = random.Random(321)
    out = {}
    for q in (eps, eps / 2):
        fired = 0
        for _ in range(R):
            d = SRDetector(eps, SR_A)
            for _ in range(n_audits):
                d.update(1 if rng.random() < q else 0)
                if d.crossed:
                    fired += 1
                    break
        out["q=%g" % q] = fired / R
    return {"R": R, "audits_per_run": n_audits, "A": SR_A, "false_alarm_frac": out}


def exp_frontier(R=100, N=3000, onset=1000, uni=0.3):
    """Cost vs harm across audit rates — the iron-triangle trade the lottery buys."""
    rows = []
    for p in (1 / 64, 1 / 32, 1 / 16, 1 / 8, 1 / 4):
        rs = [run_stream(make_stream(N, onset, uni, 2000 + r), lambda x, _: lazy_cheap(x), SecretDraws(), p)
              for r in range(R)]
        rows.append({"p": p, "cost_mean": _mean(x["cost"] for x in rs), "harm_mean": _mean(x["harm"] for x in rs),
                     "revoked_frac": _mean(x["revoked_at"] is not None for x in rs)})
    return {"R": R, "N": N, "always_exact": {"cost": N * EXACT_COST, "harm": 0}, "rows": rows}


def exp_live_moth(N=3000, p=1 / 8, blind=0.2):
    """The strategic scenario on real Moth QRNG bytes, until the pool runs out."""
    pool = load_moth_pool()
    if pool is None:
        return {"skipped": "no moth_draws.json pool"}
    items = make_stream(N, None, 0.0, seed=77)
    res = run_stream(items, cheater(guarded_cheap, None, blind, random.Random(3)), pool, p)
    ok, _ = res["chain"].verify()
    order, _ = res["chain"].order_ok()
    return {"source": pool.name, "pool_bits": len(pool.buf) * 8, "items_served": res["n"],
            "exhausted": res["exhausted"], "audits": res["audits"], "revoked_at": res["revoked_at"],
            "E_max": res["E_max"], "harm": res["harm"], "chain_ok": ok, "order_ok": order}


def exp_tamper():
    """Two attacks on the receipts: edit a record (hash break) and swap the answer after the draw."""
    items = make_stream(400, 0, 0.5, seed=11)
    src = PublicSeedDraws(1)
    res = run_stream(items, lambda x, _: lazy_cheap(x), src, 1 / 4, tamper_at=None)
    ch = res["chain"]
    clean = (ch.verify()[0], ch.order_ok()[0])
    # (1) edit an AUDIT verdict in place
    edited = json.loads(json.dumps(ch.records))
    k = next(j for j, r in enumerate(edited) if r["rel"] == "AUDIT" and not r["body"]["agree"])
    edited[k]["body"]["agree"] = True
    c2 = Chain()
    c2.records = edited
    edit_detected = not c2.verify()[0]
    # (2) swap the answer after seeing the draw (re-chained honestly, so the hash chain is VALID —
    #     only the COMMIT/AUDIT consistency check can catch it)
    swap_item = next(i for i, x in enumerate(items) if lazy_cheap(x) != exact_route(x))
    src2 = PublicSeedDraws(1)
    # force an audit on swap_item by scanning for one with p=1
    res2 = run_stream(items, lambda x, _: lazy_cheap(x), src2, 1.0, tamper_at=swap_item)
    swap_chain_ok = res2["chain"].verify()[0]
    swap_order_ok, why = res2["chain"].order_ok()
    return {"clean_chain_ok": clean[0], "clean_order_ok": clean[1], "edit_detected": edit_detected,
            "swap_chain_still_valid": swap_chain_ok, "swap_detected_by_order_check": not swap_order_ok,
            "swap_reason": why}


def report(fast: bool = False) -> dict:
    s = 0.25 if fast else 1.0
    R = lambda n: max(20, int(n * s))  # noqa: E731
    return {"drift": exp_drift(R=R(200)), "strategic": exp_strategic(R=R(200)),
            "false_revocation": exp_false_revocation(R=R(1000)), "frontier": exp_frontier(R=R(100)),
            "trust_credit": exp_trust_credit(R=R(100)), "sr_false_alarm": exp_sr_false_alarm(R=R(400)),
            "tamper": exp_tamper(), "live_moth": exp_live_moth()}


def _fmt(rep: dict) -> str:
    d, s, f, fr, t, m = (rep[k] for k in ("drift", "strategic", "false_revocation", "frontier", "tamper", "live_moth"))
    L = ["audit-lottery — certified cascade: COMMIT -> unpredictable DRAW -> differ AUDIT -> e-process LICENSE",
         "",
         "1. honest drift (lazy route; unicode arrives at item %d; audit p=1/%d; R=%d, N=%d)" % (
             d["onset"], round(1 / d["p"]), d["R"], d["N"]),
         "   measured post-onset disagreement of the lazy route: %.3f" % d["true_post_onset_disagree"],
         "   revoked: %.0f%% of runs (0 before onset: %s)   detection delay: mean %.0f items, max %s" % (
             100 * d["revoked_frac"], d["revoked_before_onset"] == 0, d["detect_delay_mean"], d["detect_delay_max"]),
         "   wrong products served: %.1f  vs %.1f with no audits  (%.1fx less)" % (
             d["harm_mean"], d["harm_no_audit"], d["harm_no_audit"] / max(d["harm_mean"], 1e-9)),
         "   cost: %.0f  vs always-exact %d  vs always-cheap %d" % (d["cost_mean"], d["cost_always_exact"], d["cost_always_cheap"]),
         "",
         "2. strategic contractor (cheats when unwatched; p=1/%d; R=%d, N=%d)" % (round(1 / s["p"]), s["R"], s["N"])]
    for k in ("public-seed + oracle", "secret + blind cheat"):
        x = s[k]
        L.append("   %-22s revoked %3.0f%%  wrong served %.1f (%.1f%% of N)  E_max %.3g" % (
            k, 100 * x["revoked_frac"], x["harm_mean"], 100 * x["harm_frac_of_N"], x["E_max_mean"]))
    L += ["",
          "3. validity (Ville): revocation rate of a route at/below eps=%.2f over %d audits, R=%d (bar: <= delta=%.2f)" % (
              f["eps"], f["audits_per_run"], f["R"], f["delta"]),
          "   " + "  ".join("%s: %.3f" % kv for kv in f["revoked_frac"].items()),
          "",
          "4. frontier (lazy route, drift at 1000; always-exact = cost %d, harm 0)" % fr["always_exact"]["cost"]]
    for r in fr["rows"]:
        L.append("   p=1/%-3d cost %6.0f  wrong served %6.1f  revoked %3.0f%%" % (
            round(1 / r["p"]), r["cost_mean"], r["harm_mean"], 100 * r["revoked_frac"]))
    L += ["",
          "5. receipts: clean chain ok=%s order ok=%s | in-place edit detected=%s | answer-swap-after-draw: "
          "chain still valid=%s, caught by COMMIT/AUDIT check=%s" % (
              t["clean_chain_ok"], t["clean_order_ok"], t["edit_detected"], t["swap_chain_still_valid"],
              t["swap_detected_by_order_check"]),
          ""]
    tc, sf = rep["trust_credit"], rep["sr_false_alarm"]
    L.append("6. trust credit — detection delay (items after drift onset) vs length of the honest past; p=1/%d, R=%d" % (
        round(1 / tc["p"]), tc["R"]))
    for r in tc["rows"]:
        L.append("   honest past %6d items | Ville: delay %6.0f missed %3.0f%% wrong %6.1f | SR(A=%d): delay %5.0f missed %3.0f%% wrong %6.1f false-early %d" % (
            r["onset"], r["ville"]["detect_delay_mean"], 100 * r["ville"]["missed_frac"], r["ville"]["harm_mean"],
            tc["SR_A"], r["sr"]["detect_delay_mean"], 100 * r["sr"]["missed_frac"], r["sr"]["harm_mean"],
            r["sr"]["false_before_onset"]))
    L.append("   SR false alarms within %d audits (A=%d, R=%d): %s" % (
        sf["audits_per_run"], sf["A"], sf["R"], "  ".join("%s: %.3f" % kv for kv in sf["false_alarm_frac"].items())))
    L.append("")
    if "skipped" in m:
        L.append("7. live Moth pool: skipped (%s)" % m["skipped"])
    else:
        L.append("7. live Moth draws: %s — %d bits; served %d items (pool exhausted=%s), %d audits, revoked at %s, "
                 "E_max %.3g, chain ok=%s, order ok=%s" % (m["source"], m["pool_bits"], m["items_served"],
                                                          m["exhausted"], m["audits"], m["revoked_at"], m["E_max"],
                                                          m["chain_ok"], m["order_ok"]))
    return "\n".join(L)


if __name__ == "__main__":
    rep = report(fast="--fast" in sys.argv)
    print(_fmt(rep))
