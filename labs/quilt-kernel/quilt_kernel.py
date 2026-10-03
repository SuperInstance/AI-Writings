"""quilt_kernel — receipt, differ and price your own cells.  Python 3.9+, stdlib only.

Distilled from four labs in this repo (see EXTRACTION.md for the lineage):
    labs/activeledger        ActiveLog v1 envelope, budget vector, prev-chain, double-entry
    labs/system2-backtest    product-identity gate ("never price a cheaper different answer")
    labs/route-preference    Pareto frontier over {good, fast, cheap} + Hebbian tie-break
    labs/situation-recorder  fnv1a-64 canonical-JSON idiom, chain + tamper evidence
API names follow SuperInstance/forge-quilt (openapi.yaml): verify -> {intact, firstBreak},
anchored head, canary.  Nothing here touches the network, the clock (unless you ask), or disk
(unless you pass a path).

    Cell(fn, name, ledger)   wrap a pure function; every call appends a receipt
    Ledger()                 append-only hash-chained log; .verify() .anchor() .total()
    diff(a, b)               product identity between two outputs / receipts
    price({name: receipts})  gate on identity FIRST, then place on {good, fast, cheap}
"""

from __future__ import annotations

import hashlib
import json
import time

__all__ = ["Cell", "Ledger", "diff", "price", "which", "Book", "replay", "budget", "add_budget",
           "fnv1a64", "canon", "content_hash", "canary", "Refusal"]

ALV = 1
TYPES = ("cell.tick", "route.hop", "ledger.transaction")   # the ActiveLog v1 namespaced types
LINKS = {"sha256": lambda b: "sha256:" + hashlib.sha256(b).hexdigest(),
         "blake2b-256": lambda b: "blake2b-256:" + hashlib.blake2b(b, digest_size=32).hexdigest()}
REQUIRED = ("alv", "dev", "seq", "ts", "mono", "type", "body", "prev")


class Refusal(Exception):
    """A step that cannot be honestly performed (never raised by price(); it returns a refusal)."""


# ---- hashing ------------------------------------------------------------------------

def fnv1a64(s: str) -> int:
    """fnv1a-64 over UTF-8. A CONFORMANCE hash (do two ports agree?), not tamper evidence."""
    h = 0xCBF29CE484222325
    for b in s.encode("utf-8"):
        h = ((h ^ b) * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


def _default(o):
    if isinstance(o, (bytes, bytearray)):
        return {"$bytes": bytes(o).hex()}
    if isinstance(o, (set, frozenset)):
        return sorted(o, key=canon)
    if isinstance(o, tuple):
        return list(o)
    raise TypeError("not canonicalisable: %s (make the product JSON-shaped)" % type(o).__name__)


def canon(obj) -> str:
    """Canonical JSON: sorted keys, no spaces. Raises TypeError on non-deterministic types
    (arbitrary objects, NaN floats) rather than hashing a repr() that can differ per run."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=_default, allow_nan=False)


def content_hash(obj) -> str:
    return "0x%016x" % fnv1a64(canon(obj))


def canary() -> bool:
    """The fleet's pinned fnv1a-64 vector (forge-quilt getCanary). The accent is load-bearing."""
    return fnv1a64("café Δ 日本語") == 0x024A555471370B18D


# ---- budget vector (ActiveLog v1) ----------------------------------------------------

def budget(wall_ms=0, tokens=None, usd=0.0, power_w=0.0, mem_mb=0, train=0, prod=0, reqs="local"):
    return {"wall_ms": wall_ms, "tokens": dict(tokens or {}), "usd": usd, "power_w": power_w,
            "mem_mb": mem_mb, "storage_bytes": {"train": train, "prod": prod}, "reqs": reqs}


def add_budget(a: dict, b: dict) -> dict:
    tok = dict(a["tokens"])
    for k, v in b["tokens"].items():
        tok[k] = tok.get(k, 0) + v
    reqs = sorted((set(a["reqs"].split("+")) | set(b["reqs"].split("+"))) - {""})
    return {"wall_ms": a["wall_ms"] + b["wall_ms"], "tokens": tok,
            "usd": round(a["usd"] + b["usd"], 6), "power_w": round(a["power_w"] + b["power_w"], 6),
            "mem_mb": a["mem_mb"] + b["mem_mb"],
            "storage_bytes": {k: a["storage_bytes"][k] + b["storage_bytes"][k] for k in ("train", "prod")},
            "reqs": "+".join(reqs)}


def budget_ok(b) -> bool:
    try:
        return (b["wall_ms"] >= 0 and b["usd"] >= 0 and b["mem_mb"] >= 0 and b["power_w"] >= 0
                and all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in b["tokens"].values())
                and set(b["storage_bytes"]) == {"train", "prod"} and isinstance(b["reqs"], str))
    except (KeyError, TypeError, AttributeError):
        return False


# ---- Ledger --------------------------------------------------------------------------

class Ledger:
    """Append-only ActiveLog v1 run: {alv, dev, seq, ts, mono, type, body, prev}.

    `prev` = hash of the previous envelope's canonical JSON (sha256 per ActiveLog v1; pass
    link="blake2b-256" to match forge-quilt's integrity rule). ts is a deterministic
    "det:NNNNNN" stamp unless you pass clock=callable, so a replayed run is byte-identical.
    Pass path= to also append each record as a JSON line (load with Ledger.load).
    """

    def __init__(self, dev="kernel", link="sha256", clock=None, path=None):
        self.dev, self.link, self.clock, self.path = dev, link, clock, path
        self._h = LINKS[link]
        self.records: list[dict] = []
        self.genesis = link + ":" + "0" * 64

    def link_hash(self, env: dict) -> str:
        return self._h(canon(env).encode("utf-8"))

    def emit(self, type_: str, body: dict) -> dict:
        if type_ not in TYPES:
            raise ValueError("unknown type %r (allowed %s)" % (type_, TYPES))
        if type_ in ("cell.tick", "route.hop") and not budget_ok(body.get("budget", {})):
            raise ValueError("%s needs a well-formed budget vector" % type_)
        n = len(self.records)
        env = {"alv": ALV, "dev": self.dev, "seq": n, "mono": n + 1, "type": type_, "body": body,
               "ts": self.clock() if self.clock else "det:%06d" % (n + 1),
               "prev": self.link_hash(self.records[-1]) if n else self.genesis}
        canon(env)                                   # fail now, not at verify time
        self.records.append(env)
        if self.path:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(canon(env) + "\n")
        return env

    def hop(self, src, src_units, amount, dst, dst_units, rate, ref, route=None, **bud) -> dict:
        """Balanced double-entry: credit(src) * rate == debit(dst). The translation is the routing code."""
        body = {"credit": {"cell": src, "units": src_units, "amount": amount},
                "debit": {"cell": dst, "units": dst_units, "amount": round(amount * rate, 9)},
                "price": {"from": src_units, "to": dst_units, "rate": rate, "ref": ref},
                "budget": budget(**bud)}
        if route:
            body["route"] = route
        return self.emit("route.hop", body)

    def head(self) -> str:
        return self.link_hash(self.records[-1]) if self.records else self.genesis

    def anchor(self) -> dict:
        """Digest of the current head. Store it SOMEWHERE ELSE: a chain alone cannot show that its
        own writer did not rewrite all of it (forge-quilt getAnchoredHead)."""
        return {"digest": self.head(), "seq": len(self.records) - 1, "link": self.link}

    def verify(self, anchor: dict | None = None) -> dict:
        """{intact, firstBreak, reason}. firstBreak is the 1-based id of the FIRST bad record
        (the earliest break, not a count). With anchor=, the chain must also reproduce it."""
        prev = self.genesis
        for i, r in enumerate(self.records):
            why = None
            if not isinstance(r, dict) or not all(k in r for k in REQUIRED) or r["alv"] != ALV or r["type"] not in TYPES:
                why = "malformed envelope"
            elif r["seq"] != i:
                why = "seq not contiguous"
            elif r["prev"] != prev:
                why = "prev-chain broken"
            elif r["type"] == "cell.tick" and not receipt_ok(r):
                why = "receipt inconsistent with its own activation hash"
            if why:
                return {"intact": False, "firstBreak": i + 1, "reason": why}
            prev = self.link_hash(r)
        if anchor is not None:
            s = anchor.get("seq") if isinstance(anchor, dict) else None
            if s == -1 and not self.records:             # anchor of an empty ledger = the genesis digest
                ok = anchor.get("digest") == self.genesis
            else:
                ok = (isinstance(s, int) and not isinstance(s, bool) and 0 <= s < len(self.records)
                      and self.link_hash(self.records[s]) == anchor.get("digest"))
            if not ok:
                return {"intact": False, "firstBreak": None, "reason": "does not reproduce anchored head"}
        return {"intact": True, "firstBreak": None, "reason": None}

    def total(self, route=None) -> dict:
        """Sum of every budgeted record (cell.tick + route.hop), optionally for one route."""
        t = budget()
        for r in self.records:
            if r["type"] in ("cell.tick", "route.hop") and (route is None or r["body"].get("route") == route):
                t = add_budget(t, r["body"]["budget"])
        return t

    def receipts(self, cell=None) -> list[dict]:
        return [r["body"] for r in self.records
                if r["type"] == "cell.tick" and (cell is None or r["body"]["cell"] == cell)]

    def run_hash(self) -> str:
        return content_hash(self.records)

    def to_jsonl(self) -> str:
        return "".join(canon(r) + "\n" for r in self.records)

    @classmethod
    def load(cls, text: str, **kw) -> "Ledger":
        led = cls(**kw)
        led.records = [json.loads(l) for l in text.splitlines() if l.strip()]
        return led


def activation(cell, input_hash, product_hash) -> str:
    return content_hash({"cell": cell, "input": input_hash, "product": product_hash})


def receipt_ok(rec: dict) -> bool:
    """A receipt body must agree with itself: activation recomputes, and a kept product/input
    must still hash to what the receipt says."""
    b = rec["body"] if "body" in rec and "budget" not in rec else rec
    try:
        if b["activation"] != activation(b["cell"], b["input_hash"], b["product_hash"]):
            return False
        if "product" in b and content_hash(b["product"]) != b["product_hash"]:
            return False
        if "input" in b and content_hash(b["input"]) != b["input_hash"]:
            return False
        return budget_ok(b["budget"])
    except (KeyError, TypeError):
        return False


# ---- Cell ----------------------------------------------------------------------------

class Cell:
    """Wrap a pure function; every call appends a `cell.tick` receipt to `ledger`.

        Cell(fn, name, ledger, cost=None, route=None, keep=("input",), ignore=(), clock=time.perf_counter)

    cost(result, *args, **kw) -> dict of budget fields ({"usd":..,"tokens":{"api":n},"storage_bytes"..
    as train=/prod=}); return only what you know, the rest stays 0. If cost does not supply wall_ms
    it is measured with `clock`. Pass a deterministic cost (incl. wall_ms) for replay-exact budgets.
    keep: what to store in the receipt besides hashes — "input" (needed by replay()) and/or
    "product" (lets deep verify re-hash it). Default stores hashes + input only.
    ignore: top-level keys of a dict product that are metadata, not the answer (e.g. "via"); they are
    dropped before hashing so implementations may differ there. The function returns them untouched.
    The function must be deterministic in its JSON-shaped inputs, or replay() will say so.
    """

    def __init__(self, fn, name, ledger, cost=None, route=None, keep=("input",), ignore=(),
                 clock=time.perf_counter):
        self.fn, self.name, self.ledger, self.cost, self.ignore = fn, name, ledger, cost, tuple(ignore)
        self.route, self.keep, self.clock = route, tuple(keep), clock

    def __call__(self, *args, **kw):
        t0 = self.clock()
        out = self.fn(*args, **kw)
        wall = round((self.clock() - t0) * 1000, 3)
        fields = dict(self.cost(out, *args, **kw)) if self.cost else {}
        fields.setdefault("wall_ms", wall)
        inp, prod = {"args": list(args), "kw": kw}, _strip(out, self.ignore)
        body = {"cell": self.name, "input_hash": content_hash(inp), "product_hash": content_hash(prod),
                "budget": budget(**fields)}
        body["activation"] = activation(self.name, body["input_hash"], body["product_hash"])
        if "input" in self.keep:
            body["input"] = inp
        if "product" in self.keep:
            body["product"] = prod
        if self.route:
            body["route"] = self.route
        self.last = self.ledger.emit("cell.tick", body)["body"]
        return out


def replay(ledger: Ledger, cells: dict) -> dict:
    """Re-run every stored-input cell.tick through cells[name] (a Cell or plain function) and
    compare product hashes. replay == live iff `mismatches` is empty. Budgets are not compared
    (wall time is physics); products and activations are."""
    bad, n = [], 0
    for r in ledger.records:
        b = r["body"]
        if r["type"] != "cell.tick" or "input" not in b or b["cell"] not in cells:
            continue
        fn = getattr(cells[b["cell"]], "fn", cells[b["cell"]])
        n += 1
        out = fn(*b["input"]["args"], **b["input"]["kw"])
        if content_hash(_strip(out, getattr(cells[b["cell"]], "ignore", ()))) != b["product_hash"]:
            bad.append(r["seq"])
    return {"replayed": n, "mismatches": bad, "ok": not bad}


# ---- Differ --------------------------------------------------------------------------

def _body(x):
    return x["body"] if isinstance(x, dict) and "body" in x and "type" in x else x


def _is_receipt(x) -> bool:
    return isinstance(x, dict) and "product_hash" in x and "activation" in x


def _first_diff(a, b, path="$"):
    if type(a) is not type(b):
        return path
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                return "%s.%s" % (path, k)
            d = _first_diff(a[k], b[k], "%s.%s" % (path, k))
            if d:
                return d
        return None
    if isinstance(a, (list, tuple)):
        for i in range(max(len(a), len(b))):
            if i >= len(a) or i >= len(b):
                return "%s[%d]" % (path, i)
            d = _first_diff(a[i], b[i], "%s[%d]" % (path, i))
            if d:
                return d
        return None
    return None if a == b else path


def diff(a, b, ignore=()) -> dict:
    """Product identity. a, b: raw outputs OR receipts (an envelope, a body, or a Cell.last).
    `ignore` drops top-level dict keys from raw products (naming/metadata that is not the answer).
    -> {identical, a, b, first_difference}; first_difference is a JSON path when both raw
    products are available, else None (hashes alone cannot localise)."""
    ra, rb = _is_receipt(_body(a)), _is_receipt(_body(b))
    pa = _body(a)["product_hash"] if ra else content_hash(_strip(a, ignore))
    pb = _body(b)["product_hash"] if rb else content_hash(_strip(b, ignore))
    va = _body(a).get("product") if ra else _strip(a, ignore)
    vb = _body(b).get("product") if rb else _strip(b, ignore)
    where = None
    if pa != pb and (ra is False or "product" in _body(a)) and (rb is False or "product" in _body(b)):
        where = _first_diff(va, vb)
    return {"identical": pa == pb, "a": pa, "b": pb, "first_difference": where}


def _strip(x, ignore):
    return {k: v for k, v in x.items() if k not in ignore} if ignore and isinstance(x, dict) else x


# ---- Price (B7 gate + B4 placement) ---------------------------------------------------

PRIORITIES = ("good", "fast", "cheap", "better-faster", "better-cheaper", "faster-cheaper")
PAIRS = {"better-faster": ("good", "fast"), "better-cheaper": ("good", "cheap"),
         "faster-cheaper": ("fast", "cheap")}
SCALE, REINFORCE, DECAY = 1_000_000, (1, 4), (1, 10)


def axes_of(b: dict) -> dict:
    st = b["storage_bytes"]
    return {"wall_ms": b["wall_ms"], "usd": b["usd"], "tokens": sum(b["tokens"].values()),
            "storage_bytes": st["train"] + st["prod"]}


def _cheap(ax):
    return (ax["usd"], ax["tokens"], ax["storage_bytes"])


def _dom(x, y):
    return all(p <= q for p, q in zip(x, y)) and any(p < q for p, q in zip(x, y))


def _seal(d):
    d["result_hash"] = content_hash(d)
    return d


def _refused(reason, **extra):
    return _seal({"status": "refused", "reason": reason, **extra})


def _sum_axes(axs):
    return {k: sum(a[k] for a in axs) for k in ("wall_ms", "usd", "tokens", "storage_bytes")}


def price(candidates: dict, standing: dict | None = None, weights: dict | None = None) -> dict:
    """Which implementation, when?

    candidates: {name: receipt | [receipts]} — each name is one implementation; a list is one
    run per workload item (same order for every name). Receipts may be envelopes, bodies or
    Cell.last. The product-identity gate runs FIRST: if any item's product differs between
    implementations (or a receipt is self-inconsistent, or lengths differ) the result is
    {"status": "refused", ...} and NO budget is exposed — never price a cheaper different answer.

    standing: optional {name: non-negative int} — earned quality standing; if omitted for any
    name, `good` is a tie (we do not invent quality). weights: Hebbian tie-break (see Book).
    Returns status, class ("dominant" | "trade-off"), frontier (undominated names), dominated,
    preferred_when {good, fast, cheap, better-faster, better-cheaper, faster-cheaper} (a pair is
    None on a real trade-off), tied, per-name axes, product_hash, result_hash (fnv1a-64).
    """
    standing, weights = dict(standing or {}), weights or {}
    if len(candidates) < 2:
        return _refused("need >= 2 implementations to express a preference")
    if not all(isinstance(n, str) for n in candidates):
        return _refused("implementation names must be strings")
    if not (isinstance(weights, dict) and all(isinstance(w, dict) for w in weights.values())):
        return _refused("weights must be {priority: {name: int}} (e.g. Book.weights)")
    runs = {n: [_body(r) for r in (v if isinstance(v, (list, tuple)) else [v])] for n, v in candidates.items()}
    names = sorted(runs)
    if len({len(v) for v in runs.values()}) != 1 or not runs[names[0]]:
        return _refused("every implementation needs the same, non-zero number of receipts")
    for n in names:
        for r in runs[n]:
            if not (_is_receipt(r) and receipt_ok(r)):
                return _refused("receipt for %r is missing or inconsistent with itself" % n)
    for i in range(len(runs[names[0]])):
        for n in names[1:]:
            if not diff(runs[names[0]][i], runs[n][i])["identical"]:
                return _refused("products differ at item %d — never price a cheaper different answer" % i,
                                products={m: runs[m][i]["product_hash"] for m in names})
    bad = [k for k, v in standing.items() if isinstance(v, bool) or not isinstance(v, int) or v < 0 or k not in runs]
    if bad:
        return _refused("standing must be {known name: non-negative int}; bad: %s" % sorted(bad))
    axes = {n: _sum_axes([axes_of(r["budget"]) for r in runs[n]]) for n in names}
    full = len(standing) == len(names)
    obj = {n: (-(standing[n] if full else 0), axes[n]["wall_ms"]) + _cheap(axes[n]) for n in names}
    dominated = {n: sorted(m for m in names if m != n and _dom(obj[m], obj[n])) for n in names}
    frontier = [n for n in names if not dominated[n]]
    top = max(standing.values()) if full else None
    lo = min(axes[n]["wall_ms"] for n in names)
    win = {"good": [n for n in names if not full or standing[n] == top],
           "fast": [n for n in names if axes[n]["wall_ms"] == lo],
           "cheap": [n for n in names if not any(_dom(_cheap(axes[m]), _cheap(axes[n])) for m in names if m != n)]}

    def pick(c, p):
        return sorted(c, key=lambda n: (-weights.get(p, {}).get(n, 0), n))[0]
    pw = {p: pick([n for n in win[p] if n in frontier] or win[p], p) for p in ("good", "fast", "cheap")}
    for p, (a, b) in PAIRS.items():
        both = [n for n in win[a] if n in win[b] and n in frontier]
        pw[p] = pick(both, p) if both else None
    if not full:
        pw["good"] = "tie"
    return _seal({"status": "certified", "class": "dominant" if len(frontier) == 1 else "trade-off",
                  "product_hash": content_hash([r["product_hash"] for r in runs[names[0]]]),
                  "items": len(runs[names[0]]), "routes": axes, "frontier": frontier,
                  "dominated": {n: d for n, d in dominated.items() if d}, "preferred_when": pw,
                  "tied": {p: sorted(win[p]) for p in win if len(win[p]) > 1},
                  "good_source": "standing" if full else "tie",
                  "caveat": "stationary-budget assumption: re-price when prices or hardware change"})


def which(result: dict, want: str = "cheap"):
    """The implementation to use when you want `want` (a PRIORITIES key). None on a real
    trade-off for a pair; raises Refusal if the result was refused."""
    if result["status"] != "certified":
        raise Refusal(result["reason"])
    return result["preferred_when"][want]


class Book:
    """Hebbian PreferenceBook: each confirmed result reinforces the pick and decays the rest.
    Integer weights in [0, SCALE]; deterministic given the ordered results. Weights only break
    ties the data leaves open — they never override a strict win. Feed `.weights` to price()."""

    def __init__(self):
        self.weights: dict = {}
        self.n = 0

    def observe(self, result: dict) -> None:
        if result.get("status") != "certified":
            return
        self.n += 1
        for p in PRIORITIES:
            pick = result["preferred_when"].get(p)
            if pick is None or pick not in result["routes"]:
                continue
            cur = self.weights.setdefault(p, {})
            for n in result["routes"]:
                w = cur.get(n, 0)
                w = w + (SCALE - w) * REINFORCE[0] // REINFORCE[1] if n == pick else w - w * DECAY[0] // DECAY[1]
                cur[n] = max(0, min(SCALE, w))

    def settled(self) -> dict:
        return {p: sorted(w, key=lambda k: (-w[k], k))[0] for p, w in self.weights.items() if w}
