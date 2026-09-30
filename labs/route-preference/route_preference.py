"""route-preference (B4) — the market-clearing join: `preferred_when` over the iron-triangle.

    preferred_when = f( OrgBook standing [good],  ActiveLedger budget [fast, cheap] )
                                                        (ACTIVELEDGER-CELL-GRAPH.md §11.1, §14)

Input: >= 2 routes that B7 (system2-backtest) has CERTIFIED product-identical. This module
reuses B7's replay + gate and refuses (never ranks) routes that disagree on the answer.

    good  = optional per-route OrgBook-style STANDING (a non-negative int; higher = more
            earned standing). Absent for any route -> good is a tie, as in B7.
    fast  = wall_ms (lower wins).
    cheap = a vector (usd, tokens, storage_bytes); one route beats another on cheap only if
            it is no worse on all three and strictly better on one. Otherwise the two are
            incomparable on cheap (the "split" cheapness of B7) and both stay candidates.

Output is NOT a scalar winner. It is:
    frontier        routes no other route dominates on {good, fast, cheap}
    dominated       routes some other route beats on every axis (with who dominates them)
    preferred_when  route to pick per priority: good / fast / cheap, and the contractor
                    pairs better-faster / better-cheaper / faster-cheaper. A pair maps to
                    null when no single route is best on both axes (a real trade-off).

HEBBIAN step (PreferenceBook): every confirmed result reinforces the route it picked for
each priority and decays the others. Weights are integers in [0, SCALE] (no float touches
identity, OrgBook Law 1) and are pure functions of the observation sequence. Weights only
break ties between routes the DATA leaves tied or incomparable; they never override a
strict win. What they add is stability: `settled()` names the route that has been
confirmed most consistently across many backtests, which is not always the last one seen.

Everything here is pure (no clock, no randomness, no I/O in the scoring path).
`result_hash` is fnv1a-64 over canonical JSON, the same idiom as B7's verdict_hash.

Library:  prefer(routes, standing=None, weights=None) -> result | refused result
          prefer_axes(named_axes, standing=None, weights=None) -> result   (no replay)
          PreferenceBook().observe(result) / .settled() / .digest()
CLI:      python3 route_preference.py [--json]   # demo over the example quilts' route pairs
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LABS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LABS, "activeledger"))
sys.path.insert(0, os.path.join(LABS, "system2-backtest"))

import activeledger as al  # noqa: E402
import backtest as bt  # noqa: E402

PRIORITIES = ("good", "fast", "cheap", "better-faster", "better-cheaper", "faster-cheaper")
PAIRS = {"better-faster": ("good", "fast"), "better-cheaper": ("good", "cheap"),
         "faster-cheaper": ("fast", "cheap")}

SCALE = 1_000_000          # weights are integers in [0, SCALE]
REINFORCE = (1, 4)         # w += (SCALE - w) * 1/4   (saturating growth, never exceeds SCALE)
DECAY = (1, 10)            # w -= w * 1/10


# ---- dominance ---------------------------------------------------------------------

def _cheap_vec(ax: dict) -> tuple:
    return (ax["usd"], ax["tokens"], ax["storage_bytes"])


def _dominates(x: tuple, y: tuple) -> bool:
    """x dominates y: no worse everywhere, strictly better somewhere (all components: lower is better)."""
    return all(a <= b for a, b in zip(x, y)) and any(a < b for a, b in zip(x, y))


def _objective(name, ax, standing) -> tuple:
    """Everything to MINIMIZE for one route: (-standing, wall_ms, usd, tokens, storage)."""
    return (-standing.get(name, 0),) + (ax["wall_ms"],) + _cheap_vec(ax)


def _axis_winners(axes: dict, standing: dict) -> dict:
    """Set of routes that are best (or tied best / incomparable-best) on each single axis."""
    names = sorted(axes)
    have = all(n in standing for n in names)
    if have:
        top = max(standing[n] for n in names)
        good = [n for n in names if standing[n] == top]
    else:
        good = names                                   # no full standing -> tie (B7 semantics)
    lo = min(axes[n]["wall_ms"] for n in names)
    fast = [n for n in names if axes[n]["wall_ms"] == lo]
    cheap = [n for n in names
             if not any(_dominates(_cheap_vec(axes[m]), _cheap_vec(axes[n])) for m in names if m != n)]
    return {"good": good, "fast": fast, "cheap": cheap}


def _pick(cands: list, weights: dict, prio: str) -> str:
    """Tie-break among data-tied candidates: highest hebbian weight, then name."""
    w = weights.get(prio, {})
    return sorted(cands, key=lambda n: (-w.get(n, 0), n))[0]


# ---- the join ----------------------------------------------------------------------

def _seal(body: dict) -> dict:
    body["result_hash"] = al.content_hash(body)
    return body


def _refused(reason: str, **extra) -> dict:
    return _seal({"status": "refused", "reason": reason, **extra})


def _standing_ok(standing) -> str | None:
    for k, v in standing.items():
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            return "standing[%r] must be a non-negative int (identity never floats), got %r" % (k, v)
    return None


def prefer_axes(named_axes: dict, standing: dict | None = None, weights: dict | None = None) -> dict:
    """Preference over already-certified axis vectors {name: {wall_ms, usd, tokens, storage_bytes}}.
    The caller owns the product-identity gate; use `prefer` to have it run for you."""
    standing = dict(standing or {})
    weights = weights or {}
    if len(named_axes) < 2:
        return _refused("need >= 2 routes to express a preference")
    bad = _standing_ok(standing)
    if bad:
        return _refused(bad)
    unknown = sorted(set(standing) - set(named_axes))
    if unknown:
        return _refused("standing given for unknown route(s): %s" % unknown)

    names = sorted(named_axes)
    obj = {n: _objective(n, named_axes[n], standing if len(standing) == len(names) else {})
           for n in names}
    dominated = {n: sorted(m for m in names if m != n and _dominates(obj[m], obj[n])) for n in names}
    frontier = [n for n in names if not dominated[n]]

    win = _axis_winners(named_axes, standing)
    pw = {}
    for p in ("good", "fast", "cheap"):
        pw[p] = _pick([n for n in win[p] if n in frontier] or win[p], weights, p)
    for p, (a, b) in PAIRS.items():
        both = [n for n in win[a] if n in win[b] and n in frontier]
        pw[p] = _pick(both, weights, p) if both else None
    if len(standing) != len(names):
        pw["good"] = "tie"                     # no standing to separate them; don't invent a winner
    tied = {p: sorted(win[p]) for p in ("good", "fast", "cheap") if len(win[p]) > 1}

    if len(frontier) == 1:
        cls = "dominant"
    else:
        cls = "trade-off"
    return _seal({
        "status": "certified", "class": cls,
        "routes": {n: named_axes[n] for n in names},
        "standing": {n: standing[n] for n in sorted(standing)},
        "good_source": "standing" if len(standing) == len(names) else "tie",
        "frontier": frontier,
        "dominated": {n: d for n, d in dominated.items() if d},
        "preferred_when": pw,
        "tied": tied,
        "caveat": "stationary-budget assumption (§11.2): re-backtest on repricing/hardware change",
    })


def prefer(routes, standing: dict | None = None, weights: dict | None = None) -> dict:
    """routes: [(name, records)]. B7's gate runs FIRST: every route must replay, and every
    product must equal the first route's — otherwise `refused`, and no budget is exposed."""
    routes = list(routes)
    if len(routes) < 2:
        return _refused("need >= 2 routes to express a preference")
    names = [n for n, _ in routes]
    if len(set(names)) != len(names):
        return _refused("route names must be unique")
    reps = {}
    for name, recs in routes:
        try:
            reps[name] = bt.replay_route(recs)
        except bt.Refusal as e:
            return _refused("replay of %r: %s" % (name, e))
    first = reps[names[0]]
    differ = [n for n in names[1:]
              if reps[n]["product_hash"] != first["product_hash"]
              or al.canon(reps[n]["product"]) != al.canon(first["product"])]
    if differ:
        return _refused("products differ — never rank routes that disagree on the answer",
                        products={n: reps[n]["product_hash"] for n in names})
    out = prefer_axes({n: reps[n]["axes"] for n in names}, standing, weights)
    if out["status"] == "certified":
        out.pop("result_hash")
        out["product_hash"] = first["product_hash"]
        out["as_of"] = {n: reps[n]["as_of"] for n in sorted(names)}
        _seal(out)
    return out


# ---- hebbian reinforcement ---------------------------------------------------------

def reinforce_weights(weights: dict, result: dict) -> dict:
    """Pure: return NEW weights after one confirmed result. For each priority, the route the
    result picked is reinforced and every other known route decays. Integer arithmetic in
    [0, SCALE]; a priority whose pick is null (no route best on both axes) is left untouched."""
    if result.get("status") != "certified":
        return {p: dict(w) for p, w in weights.items()}
    out = {p: dict(w) for p, w in weights.items()}
    for p in PRIORITIES:
        pick = result["preferred_when"].get(p)
        if pick is None or pick not in result["routes"]:      # null pair, or a 'tie' marker
            continue
        cur = out.setdefault(p, {})
        for n in result["routes"]:
            w = cur.get(n, 0)
            if n == pick:
                w = w + (SCALE - w) * REINFORCE[0] // REINFORCE[1]
            else:
                w = w - w * DECAY[0] // DECAY[1]
            cur[n] = max(0, min(SCALE, w))
    return out


class PreferenceBook:
    """Accumulates confirmations across repeated backtests. Deterministic given the same
    ordered sequence of results. `weights` is exposed; `settled()` is the stable answer."""

    def __init__(self):
        self.weights: dict = {}
        self.n = 0

    def observe(self, result: dict) -> None:
        if result.get("status") == "certified":
            self.weights = reinforce_weights(self.weights, result)
            self.n += 1

    def settled(self) -> dict:
        """Per priority: the route with the highest weight (ties -> name), with its weight."""
        out = {}
        for p in PRIORITIES:
            w = self.weights.get(p)
            if w:
                n = sorted(w, key=lambda k: (-w[k], k))[0]
                out[p] = {"route": n, "weight": w[n]}
        return out

    def digest(self) -> str:
        return al.content_hash({"n": self.n, "weights": self.weights})


# ---- demo over the example quilts --------------------------------------------------

def demo() -> dict:
    """For each example quilt: prefer() per certified case (fed into a PreferenceBook), then
    prefer_axes() over the workload sums. Cases a route could not handle are skipped."""
    out = {}
    for name, (labels, cases) in bt.fixture_pairs().items():
        book, per, sums = PreferenceBook(), [], {l: [] for l in labels}
        for c in cases:
            if c["a"] is None or c["b"] is None:
                continue
            r = prefer([(labels[0], c["a"]), (labels[1], c["b"])], weights=book.weights)
            if r["status"] != "certified":
                per.append({"id": c["id"], "status": "refused", "reason": r["reason"]})
                continue
            book.observe(r)
            for l in labels:
                sums[l].append(r["routes"][l])
            per.append({"id": c["id"], "status": "certified", "class": r["class"],
                        "result_hash": r["result_hash"]})
        work = None
        if sums[labels[0]]:
            work = prefer_axes({l: bt._sum_axes(sums[l]) for l in labels}, weights=book.weights)
        out[name] = {"labels": list(labels), "cases": per, "workload": work,
                     "settled": book.settled(), "book_digest": book.digest()}
    return out


def _fmt(name, rep) -> str:
    cert = sum(1 for c in rep["cases"] if c["status"] == "certified")
    lines = ["== %s  (%s vs %s): %d certified case(s)" % ((name,) + tuple(rep["labels"]) + (cert,))]
    w = rep["workload"]
    if w:
        lines.append("   frontier=%s  class=%s  good_source=%s" % (w["frontier"], w["class"], w["good_source"]))
        lines.append("   preferred_when: %s" % w["preferred_when"])
        lines.append("   settled: %s" % {p: "%s@%d" % (v["route"], v["weight"])
                                          for p, v in rep["settled"].items() if p in ("good", "fast", "cheap")})
    return "\n".join(lines)


if __name__ == "__main__":
    rep = demo()
    if "--json" in sys.argv:
        print(json.dumps(rep, sort_keys=True, indent=1))
    else:
        for n, r in rep.items():
            print(_fmt(n, r))
