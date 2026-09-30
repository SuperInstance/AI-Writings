"""system2-backtest (B7) — the System-2 evaluator.

System-2 proposes alternative cell-networks that reach the SAME product; this module
BACKTESTS them: replay recorded ActiveLog routes and score each on the budget vector
across the iron-triangle {good, fast, cheap}  (ACTIVELEDGER-CELL-GRAPH.md §11, §11.1).

    good  = product-identity. The differ/oracle gate runs FIRST. If the two routes did not
            reach the identical product, budgets are NEVER compared (Law: never price a
            cheaper *different* answer) -> `refused`.
    fast  = wall_ms
    cheap = two distinct measurements (§11.1/§11.3): compute (usd, tokens) and storage
            (storage_bytes train+prod). "Which cheapness a route buys" is reported.

Replay is pure: same records in -> same verdict out (no clock, no randomness, no I/O in
the scoring path). The verdict carries `verdict_hash` (fnv1a-64 over canonical JSON, the
fleet idiom) so two runs can agree bit-for-bit, and the as-of window it trusted (§11.2).

Library:   replay_route(records) -> route summary | raises Refusal
           backtest_pair(records_a, records_b) -> verdict (certified) | refused verdict
           backtest_corpus(cases) -> per-case verdicts + workload-level verdict
CLI:       python3 backtest.py [--json]   # runs every example quilt's real route pair
"""

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LABS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LABS, "activeledger"))

import activeledger as al  # noqa: E402

# ledger.transaction keys that are NOT product (route naming / declared budget).
NON_PRODUCT = ("route", "path", "chosen", "total_budget")


class Refusal(Exception):
    """Raised when a route cannot be honestly replayed/compared."""


# ---- replay -----------------------------------------------------------------------

def _fnv_chain_ok(records: list[dict]) -> bool:
    """Verify the calculator-quilt stand-in chain (fnv1a-64 `hash` per record)."""
    prev = "0x0000000000000000"
    for rec in records:
        env = {k: v for k, v in rec.items() if k != "hash"}
        env["prev"] = prev
        if "0x%016x" % al.fnv1a64(al.canon(env)) != rec.get("hash"):
            return False
        prev = rec["hash"]
    return True


def replay_route(records: list[dict]) -> dict:
    """Deterministically replay ONE route's run: re-sum its budget from the records and
    audit it against the declared ledger.transaction total. Returns a route summary."""
    txs = [r for r in records if r["type"] == "ledger.transaction"]
    if len(txs) != 1:
        raise Refusal("a route run must contain exactly one ledger.transaction (got %d)" % len(txs))
    if not (al.verify_chain(records) or _fnv_chain_ok(records)):
        raise Refusal("ActiveLog chain does not verify (tampered or truncated)")
    tx = txs[0]["body"]
    total = al.ZERO_BUDGET
    for r in records:
        if r["type"] in ("cell.tick", "route.hop"):
            if not al.budget_ok(r["body"].get("budget", {})):
                raise Refusal("malformed budget vector at seq %s" % r["seq"])
            total = al.add_budget(total, r["body"]["budget"])
    if al.canon(total) != al.canon(tx["total_budget"]):
        raise Refusal("replayed budget != declared total_budget (receipt does not replay)")
    label = tx.get("path") or tx.get("chosen") or tx.get("route")
    product = {k: v for k, v in tx.items() if k not in NON_PRODUCT}
    monos = [r["mono"] for r in records]
    return {
        "route": label,
        "product": product,
        "product_hash": al.content_hash(product),
        "budget": total,
        "axes": axes_of(total),
        "as_of": {"records": len(records), "mono": [min(monos), max(monos)]},
    }


def axes_of(b: dict) -> dict:
    """Project a budget vector onto the iron-triangle's measurable axes."""
    st = b["storage_bytes"]
    return {
        "wall_ms": b["wall_ms"],
        "usd": b["usd"],
        "tokens": sum(b["tokens"].values()),
        "storage_bytes": st["train"] + st["prod"],
    }


# ---- scoring ----------------------------------------------------------------------

def _cmp(x, y) -> int:
    return (x > y) - (x < y)      # -1: x better (lower), 0 tie, +1: y better


def _axis_winner(sign: int) -> str:
    return "A" if sign < 0 else "B" if sign > 0 else "tie"


def score(ax_a: dict, ax_b: dict, quality: dict | None = None,
          names: tuple[str, str] = ("A", "B")) -> dict:
    """Compare two axis vectors (product-identity already certified by the caller)."""
    q = quality or {}
    qa, qb = q.get("A"), q.get("B")
    good = "tie" if qa is None or qb is None or qa == qb else ("A" if qa > qb else "B")
    fast = _axis_winner(_cmp(ax_a["wall_ms"], ax_b["wall_ms"]))
    c_sign = _cmp(ax_a["usd"], ax_b["usd"]), _cmp(ax_a["tokens"], ax_b["tokens"])
    s_sign = _cmp(ax_a["storage_bytes"], ax_b["storage_bytes"])
    compute = _combine(c_sign)
    storage = _axis_winner(s_sign)
    cheap = _combine(c_sign + (s_sign,))          # 'split' when the two cheapnesses disagree
    axes = {"good": good, "fast": fast, "cheap": cheap}
    nm = {"A": names[0], "B": names[1]}
    detail = {"compute": nm.get(compute, compute), "storage": nm.get(storage, storage)}
    return {"axes": {k: nm.get(v, v) for k, v in axes.items()}, "cheap_detail": detail,
            **_classify(axes, names)}


def _combine(signs: tuple) -> str:
    if any(s < 0 for s in signs) and any(s > 0 for s in signs):
        return "split"
    if any(s < 0 for s in signs):
        return "A"
    if any(s > 0 for s in signs):
        return "B"
    return "tie"


_PAIR_NAME = {frozenset(("good", "fast")): "better-faster",
              frozenset(("good", "cheap")): "better-cheaper",
              frozenset(("fast", "cheap")): "faster-cheaper"}


def _classify(axes: dict, names) -> dict:
    """Which route wins which axis; does one DOMINATE (win >=1, lose none)?"""
    nm = {"A": names[0], "B": names[1]}
    won = {r: sorted(a for a, w in axes.items() if w == r) for r in "AB"}
    lost_any = {r: any(w == ("B" if r == "A" else "A") or w == "split" for w in axes.values())
                for r in "AB"}
    preferred_when = {a: (nm[w] if w in nm else w) for a, w in axes.items()}
    for r, o in (("A", "B"), ("B", "A")):
        if won[r] and not lost_any[r]:
            kind = ("dominates-" + _PAIR_NAME[frozenset(won[r])]) if len(won[r]) == 2 else \
                   "dominates-all-three" if len(won[r]) == 3 else "dominates-one-axis"
            return {"class": kind, "dominant": nm[r], "satisfices": nm[o],
                    "wins": {nm[r]: won[r]}, "preferred_when": preferred_when}
    if not won["A"] and not won["B"] and "split" not in axes.values():
        return {"class": "equivalent", "dominant": None, "satisfices": None,
                "wins": {}, "preferred_when": preferred_when}
    return {"class": "trade-off", "dominant": None, "satisfices": None,
            "wins": {nm["A"]: won["A"], nm["B"]: won["B"]}, "preferred_when": preferred_when}


# ---- the backtest -----------------------------------------------------------------

def _verdict(body: dict) -> dict:
    body["verdict_hash"] = al.content_hash(body)
    return body


def backtest_pair(records_a: list[dict], records_b: list[dict], quality: dict | None = None) -> dict:
    """Replay two routes and score them. THE GATE RUNS FIRST: differing products -> refused,
    no budget is compared or even exposed in the verdict."""
    try:
        a, b = replay_route(records_a), replay_route(records_b)
    except Refusal as e:
        return _verdict({"status": "refused", "reason": "replay: %s" % e})
    if a["product_hash"] != b["product_hash"] or al.canon(a["product"]) != al.canon(b["product"]):
        return _verdict({"status": "refused",
                         "reason": "products differ — never price a cheaper different answer",
                         "products": {a["route"]: a["product_hash"], b["route"]: b["product_hash"]}})
    s = score(a["axes"], b["axes"], quality, (a["route"], b["route"]))
    return _verdict({
        "status": "certified", "product_hash": a["product_hash"],
        "routes": {a["route"]: a["axes"], b["route"]: b["axes"]},
        "as_of": {a["route"]: a["as_of"], b["route"]: b["as_of"]},
        "caveat": "stationary-budget assumption (§11.2): re-backtest on repricing/hardware change",
        **s})


def _sum_axes(items: list[dict]) -> dict:
    return {k: sum(i[k] for i in items) for k in ("wall_ms", "usd", "tokens", "storage_bytes")}


def backtest_corpus(cases: list[dict], labels: tuple[str, str]) -> dict:
    """cases: [{'id', 'a': records|None, 'b': records|None}]. A route that could not handle a
    case (None) is recorded as `inapplicable` (a coverage fact, not a comparison). Workload
    verdict = the same axis logic over the SUM of certified cases only."""
    per, acc_a, acc_b = [], [], []
    refused = inapplicable = 0
    for c in cases:
        if c["a"] is None or c["b"] is None:
            inapplicable += 1
            per.append({"id": c["id"], "status": "inapplicable",
                        "only": labels[1] if c["a"] is None else labels[0]})
            continue
        v = backtest_pair(c["a"], c["b"])
        if v["status"] != "certified":
            refused += 1
            per.append({"id": c["id"], "status": "refused", "reason": v["reason"]})
            continue
        ra, rb = v["routes"][labels[0]], v["routes"][labels[1]]
        acc_a.append(ra); acc_b.append(rb)
        per.append({"id": c["id"], "status": "certified", "class": v["class"],
                    "verdict_hash": v["verdict_hash"]})
    out = {"labels": list(labels), "cases": per, "certified": len(acc_a),
           "refused": refused, "inapplicable": inapplicable}
    if acc_a:
        ta, tb = _sum_axes(acc_a), _sum_axes(acc_b)
        out["totals"] = {labels[0]: ta, labels[1]: tb}
        out["workload"] = score(ta, tb, None, labels)
    return _verdict(out)


# ---- fixtures: the example quilts' real route pairs --------------------------------

def _load(subdir, modname):
    d = os.path.join(LABS, "examples", subdir)
    if d not in sys.path:
        sys.path.insert(0, d)
    return __import__(modname)


def _try(fn):
    try:
        return fn().get("log").records
    except Exception:            # route cannot handle this input: coverage, not comparison
        return None


def fixture_pairs() -> dict:
    """{example: (labels, cases)} — each workload item run down BOTH routes (forced)."""
    out = {}

    cq = _load("calculator-quilt", "calc_quilt")
    def calc(eq, route):
        orig = cq.choose
        cq.choose = lambda _e, r=route: r
        try:
            return _try(lambda: cq.run(eq, cq.ActiveLog()))
        finally:
            cq.choose = orig
    out["calculator"] = (("simple", "full"), [
        {"id": "%s#%d" % (e["op"], i), "a": calc(e, "simple"), "b": calc(e, "full")}
        for i, e in enumerate(cq.WORKLOAD)])

    cv = _load("convert-quilt", "convert_quilt")
    out["convert"] = (("cheap", "full"), [
        {"id": "%s->%s#%d" % (r["src"], r["dst"], i),
         "a": _try(lambda r=r: cv.run(r, force="cheap")),
         "b": _try(lambda r=r: cv.run(r, force="full"))}
        for i, r in enumerate(cv.WORKLOAD)])

    dq = _load("datetime-quilt", "datetime_quilt")
    out["datetime"] = (("utc", "full"), [
        {"id": "%s#%d" % (r["op"], i),
         "a": _try(lambda r=r: dq.run(r, force="utc")),
         "b": _try(lambda r=r: dq.run(r, force="full"))}
        for i, r in enumerate(dq.WORKLOAD)])

    tn = _load("text-normalize-quilt", "textnorm_quilt")
    out["text-normalize"] = (("cheap", "full"), [
        {"id": "text#%d" % i,
         "a": _try(lambda t=t: tn.run(t, route="cheap")),
         "b": _try(lambda t=t: tn.run(t, route="full"))}
        for i, t in enumerate(tn.WORKLOAD)])

    tq = _load("image-thumb-quilt", "thumb_quilt")
    out["image-thumb"] = (("passthrough", "resample"), [
        {"id": "img%dx%d#%d" % (img["w"], img["h"], i),
         "a": _try(lambda img=img, tg=tg: tq.run(img, tg, force="passthrough")),
         "b": _try(lambda img=img, tg=tg: tq.run(img, tg, force="resample"))}
        for i, (img, tg) in enumerate(tq.WORKLOAD)])
    return out


def run_fixtures() -> dict:
    return {name: backtest_corpus(cases, labels)
            for name, (labels, cases) in fixture_pairs().items()}


def _fmt(name, rep) -> str:
    la, lb = rep["labels"]
    lines = ["== %s  (%s vs %s): certified %d, refused %d, inapplicable %d"
             % (name, la, lb, rep["certified"], rep["refused"], rep["inapplicable"])]
    if "workload" in rep:
        w, t = rep["workload"], rep["totals"]
        for lab in (la, lb):
            x = t[lab]
            lines.append("   %-11s wall_ms=%-4d usd=%-5s tokens=%-3d storage_bytes=%d"
                         % (lab, x["wall_ms"], x["usd"], x["tokens"], x["storage_bytes"]))
        lines.append("   verdict: %s  axes=%s  cheap=%s"
                     % (w["class"], w["axes"], w["cheap_detail"]))
        lines.append("   preferred-when: %s" % w["preferred_when"])
    return "\n".join(lines)


if __name__ == "__main__":
    reps = run_fixtures()
    if "--json" in sys.argv:
        print(json.dumps(reps, sort_keys=True, indent=1))
    else:
        for n, r in reps.items():
            print(_fmt(n, r))
