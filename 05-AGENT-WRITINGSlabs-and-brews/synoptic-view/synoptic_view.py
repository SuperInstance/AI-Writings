"""synoptic-view (B5) — read-only projection over the finished ActiveLog tensor.

Two capabilities, both PURE PROJECTION (nothing here emits into a recorded run):

  1. PIVOT / SYNOPSIS  — explode every budgeted record (cell.tick, route.hop) into one fact
     per atomic budget component, then project the fact table by ANY two dimensions
     (cell x component, route x axis, dev x kind, ...). Sums are exact (Fraction); every
     pivot is checked to sum back to the source ledger by `reconcile()`.
  2. TICK-SCRUBBER     — over one hash-chained run: state_at(t) is a fresh fold of records[:t]
     (rewind = refold, so it cannot drift); step()/back()/seek() move a cursor; fork(t, branch)
     returns a NEW log whose first t records are byte-identical deep copies of the original and
     whose appends carry a new dev prefix "<dev>#<branch>" (no (dev,seq) collision) and continue
     the same chain. The recorded run is never mutated.

Chain flavors (both verified with their owner's own verify, never re-implemented):
  "sha256-prev"  labs/activeledger  — `prev` = sha256(canon(prev env)); activeledger.verify_chain
  "fnv1a-hash"   calculator-quilt   — `hash` = fnv1a-64(canon(env)); calc_quilt.verify_chain

The corpus is the real recorded runs: route_sim (filtered + nofilter), the six example quilts
that import labs/activeledger booked onto ONE shared ActiveLog (each example writes as its own
`dev`, seq continuous across the shared chain), and calculator-quilt on its own fnv1a chain.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import pathlib
import sys
from decimal import Decimal
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
LABS = HERE.parent
sys.path.insert(0, str(LABS / "activeledger"))

import activeledger as AL  # noqa: E402
import otel_export  # noqa: E402
import route_sim  # noqa: E402

RUNS = HERE / "runs"


def _load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CALC = _load(LABS / "examples" / "calculator-quilt" / "calc_quilt.py", "synoptic_calc_quilt")

# example -> (module file, how its run() takes the shared log)
SHARED_EXAMPLES = {
    "convert-quilt": ("convert_quilt.py", "log"),
    "currency-round-quilt": ("currency_quilt.py", "log"),
    "datetime-quilt": ("datetime_quilt.py", "al"),
    "image-thumb-quilt": ("thumb_quilt.py", "al"),
    "match-quilt": ("match_quilt.py", "log"),
    "text-normalize-quilt": ("textnorm_quilt.py", "log"),
}


# ---- corpus: the real recorded runs -----------------------------------------------

def record_corpus() -> dict:
    """Re-run every producer deterministically. name -> list[record]. (replay == live)"""
    logs = {}
    for use_filter, tag in ((True, "route_sim.filtered"), (False, "route_sim.nofilter")):
        logs[tag] = route_sim.run(use_filter)["log"].records
    shared = AL.ActiveLog(dev="shared")
    for ex, (fname, kw) in SHARED_EXAMPLES.items():
        mod = _load(LABS / "examples" / ex / fname, "synoptic_" + ex.replace("-", "_"))
        shared.dev = ex                              # one chain, many writers: (dev, seq) stays unique
        for w in mod.WORKLOAD:
            args = w if ex == "image-thumb-quilt" else (w,)
            mod.run(*args, **{kw: shared})
    logs["examples.shared"] = shared.records
    calc = CALC.ActiveLog(dev="calc-quilt")
    for eq in CALC.WORKLOAD:
        CALC.run(eq, calc)
    logs["calculator"] = calc.records
    return logs


def to_jsonl(records) -> str:
    return "".join(AL.canon(r) + "\n" for r in records)


def from_jsonl(text: str) -> list[dict]:
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def write_runs(logs: dict) -> None:
    RUNS.mkdir(exist_ok=True)
    for name, recs in logs.items():
        (RUNS / (name + ".jsonl")).write_text(to_jsonl(recs), encoding="utf-8")


def read_runs() -> dict:
    return {p.name[:-len(".jsonl")]: from_jsonl(p.read_text(encoding="utf-8"))
            for p in sorted(RUNS.glob("*.jsonl"))}


# ---- chain flavors (reuse the owners' verify) ---------------------------------------

def flavor(records) -> str:
    return "fnv1a-hash" if records and "hash" in records[0] else "sha256-prev"


def verify(records) -> bool:
    if flavor(records) == "fnv1a-hash":
        return CALC.verify_chain(records)
    return AL.verify_chain(records)


def head_of(records, fl: str | None = None) -> str:
    """The link the NEXT record would chain to."""
    fl = fl or flavor(records)
    if not records:
        return CALC.GENESIS if fl == "fnv1a-hash" else AL.GENESIS
    if fl == "fnv1a-hash":
        return records[-1]["hash"]
    return AL.link_hash(records[-1])


def run_hash(records) -> str:
    return AL.content_hash(records)


# ---- facts: one row per (budgeted record, atomic component) -------------------------

AXIS = {"wall_ms": "fast", "usd": "cheap-compute", "power_w": "cheap-compute", "mem_mb": "cheap-compute",
        "storage_train": "cheap-storage", "storage_prod": "cheap-storage"}
AXES = ("good", "fast", "cheap-compute", "cheap-storage")   # good = OrgBook standing: NOT in the ledger
BUDGETED = ("cell.tick", "route.hop")


def _exact(x) -> Fraction:
    return Fraction(Decimal(repr(x))) if isinstance(x, float) else Fraction(x)


def components(b: dict) -> dict:
    out = {"wall_ms": b["wall_ms"], "usd": b["usd"], "power_w": b["power_w"] or 0, "mem_mb": b["mem_mb"] or 0,
           "storage_train": b["storage_bytes"]["train"], "storage_prod": b["storage_bytes"]["prod"]}
    for api, n in b["tokens"].items():
        out["tokens:" + api] = n
    return out


def axis_of(component: str) -> str:
    return "cheap-compute" if component.startswith("tokens:") else AXIS[component]


def facts(logs: dict) -> list[dict]:
    """Explode the tensor. Every budgeted record yields one fact per component, exactly once."""
    out = []
    for log, recs in logs.items():
        run = 0                                       # a run = records up to + incl. its ledger.transaction
        for r in recs:
            if r["type"] == "ledger.transaction":
                run += 1
                continue
            if r["type"] not in BUDGETED:
                continue
            b = r["body"]
            if r["type"] == "cell.tick":
                cell, kind = b["cell"], b.get("kind", "?")
            else:
                cell, kind = "%s->%s" % (b["credit"]["cell"], b["debit"]["cell"]), "HOP"
            dims = {"log": log, "dev": r["dev"], "type": r["type"], "cell": cell, "kind": kind,
                    "route": str(b.get("route", "(none)")), "path": str(b.get("path", b.get("chosen", "(none)"))),
                    "run": "%s/%03d" % (log, run), "reqs": b["budget"]["reqs"], "tick": r["mono"],
                    "seq": r["seq"]}
            for comp, v in components(b["budget"]).items():
                out.append({**dims, "component": comp, "axis": axis_of(comp),
                            "api": comp[7:] if comp.startswith("tokens:") else "(none)", "value": _exact(v)})
    return out


DIMS = ("log", "dev", "type", "cell", "kind", "route", "path", "run", "reqs", "tick", "component", "axis", "api")


# ---- pivot ---------------------------------------------------------------------------

def _vadd(acc: dict, comp: str, v: Fraction) -> None:
    acc[comp] = acc.get(comp, Fraction(0)) + v


def pivot(fs: list[dict], rows: str, cols: str, where=None) -> dict:
    """Project facts by two dims. Each cell holds a component vector {component: Fraction}
    (summing different units into one number is refused by construction)."""
    if rows not in DIMS or cols not in DIMS:
        raise ValueError("unknown dimension (have %s)" % (DIMS,))
    cells, rtot, ctot, grand = {}, {}, {}, {}
    for f in fs:
        if where and not where(f):
            continue
        r, c, comp, v = f[rows], f[cols], f["component"], f["value"]
        _vadd(cells.setdefault((r, c), {}), comp, v)
        _vadd(rtot.setdefault(r, {}), comp, v)
        _vadd(ctot.setdefault(c, {}), comp, v)
        _vadd(grand, comp, v)
    if cols == "axis":                                  # show the whole triangle, incl. the empty axis
        for a in AXES:
            ctot.setdefault(a, {})
    return {"rows": rows, "cols": cols, "cells": cells, "row_tot": rtot, "col_tot": ctot, "grand": grand,
            "row_keys": sorted(rtot, key=str), "col_keys": sorted(ctot, key=lambda k: (AXES.index(k) if k in AXES else 9, str(k)))}


def rollup(vec: dict) -> dict:
    """Summary measures over a component vector: tokens = sum(tokens:*), storage_bytes = train+prod."""
    g = lambda k: vec.get(k, Fraction(0))  # noqa: E731
    return {"wall_ms": g("wall_ms"), "tokens": sum((v for k, v in vec.items() if k.startswith("tokens:")), Fraction(0)),
            "usd": g("usd"), "storage_bytes": g("storage_train") + g("storage_prod"),
            "power_w": g("power_w"), "mem_mb": g("mem_mb")}


def synopsis(fs: list[dict], by: str = "cell") -> dict:
    """Per-<by> aggregates (wall_ms, tokens, usd, storage_bytes, ...) + the grand total."""
    p = pivot(fs, by, "component")
    return {"by": by, "rows": {k: rollup(p["row_tot"][k]) for k in p["row_keys"]}, "total": rollup(p["grand"])}


def _fmt(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    return ("%.6f" % float(v)).rstrip("0").rstrip(".")


def render(p: dict, measure: str | None = None) -> str:
    """Markdown table. If a dim is component/axis-free, `measure` picks which component (or rollup) to show."""
    pick = (lambda vec: rollup(vec)[measure] if measure in ("tokens", "storage_bytes") else vec.get(measure, Fraction(0)))
    scalar = lambda vec: _fmt(pick(vec)) if measure else (  # noqa: E731
        _fmt(next(iter(vec.values()))) if len(vec) == 1 else ("—" if not vec else "%d comps" % len(vec)))
    head = "| %s \\ %s | %s | total |" % (p["rows"], p["cols"], " | ".join(map(str, p["col_keys"])))
    lines = [head, "|" + "---|" * (len(p["col_keys"]) + 2)]
    for r in p["row_keys"]:
        vals = [scalar(p["cells"].get((r, c), {})) if p["cells"].get((r, c)) else "·" for c in p["col_keys"]]
        lines.append("| %s | %s | %s |" % (r, " | ".join(vals), scalar(p["row_tot"][r])))
    lines.append("| **total** | %s | %s |" % (" | ".join(scalar(p["col_tot"][c]) if p["col_tot"][c] else "·"
                                                         for c in p["col_keys"]), scalar(p["grand"])))
    return "\n".join(lines)


# ---- reconciliation: a projection that does not sum back to the source is a bug -------

class ReconcileError(AssertionError):
    pass


def _budget_vec(b: dict) -> dict:
    return {k: _exact(v) for k, v in components(b).items() if v != 0}


def _nz(vec: dict) -> dict:
    return {k: v for k, v in vec.items() if v != 0}


def _close(a: dict, b: dict, tol=Fraction(1, 10**6)) -> bool:
    """Exact on integer components; float components (usd/power_w) to the ledger's 6-dp rounding."""
    keys = set(_nz(a)) | set(_nz(b))
    return all(abs(a.get(k, Fraction(0)) - b.get(k, Fraction(0))) <= tol for k in keys)


def reconcile(logs: dict, p: dict | None = None, fs: list[dict] | None = None) -> dict:
    """Assert the projection sums back to the ledger along four independent paths. Returns a report
    (incl. FINDINGS: declared txn totals that are not their own run's sum — an upstream property)."""
    fs = fs if fs is not None else facts(logs)
    rep = {"checks": 0, "findings": []}

    def check(ok, msg):
        rep["checks"] += 1
        if not ok:
            raise ReconcileError(msg)

    # R0 every log verifies with its owner's verify (replay==live precondition)
    for name, recs in logs.items():
        check(verify(recs), "chain does not verify: %s" % name)
    # R1 grand total == activeledger.add_budget fold over every budgeted record (independent adder)
    fold = AL.ZERO_BUDGET
    n_budgeted = 0
    for recs in logs.values():
        for r in recs:
            if r["type"] in BUDGETED:
                fold = AL.add_budget(fold, r["body"]["budget"])
                n_budgeted += 1
    grand = pivot(fs, "log", "component")["grand"]
    check(_close(grand, _budget_vec(fold)), "R1 grand total != ledger fold")
    # R1b each budgeted record is in the fact table exactly once (dedupe key (log, dev, seq))
    keys = {(f["log"], f["dev"], f["seq"]) for f in fs}
    check(len(keys) == n_budgeted, "R1b record count %d != %d" % (len(keys), n_budgeted))
    # R2 margins: rows and cols of the given pivot each sum to its grand total
    if p is not None:
        rs, cs = {}, {}
        for vec in p["row_tot"].values():
            for k, v in vec.items():
                _vadd(rs, k, v)
        for vec in p["col_tot"].values():
            for k, v in vec.items():
                _vadd(cs, k, v)
        cells = {}
        for vec in p["cells"].values():
            for k, v in vec.items():
                _vadd(cells, k, v)
        check(rs == p["grand"] and cs == p["grand"] and cells == p["grand"], "R2 margins do not sum to grand")
    fs_by_log = {}
    for f in fs:
        fs_by_log.setdefault(f["log"], []).append(f)
    # R3 per route (sha256 logs): pivot route row == activeledger.route_total(records, route)
    for name, recs in logs.items():
        if flavor(recs) != "sha256-prev":
            continue
        byroute = pivot(fs_by_log.get(name, []), "route", "component")["row_tot"]
        for route, vec in byroute.items():
            check(_close(vec, _budget_vec(AL.route_total(recs, route))), "R3 %s route %s" % (name, route))
    byrun = pivot(fs, "run", "component")["row_tot"]
    # R4 every ledger.transaction's declared total == the emitter's own semantics at that point:
    #    sha256 logs: route_total(prefix, route); fnv1a calc log: the sum of its own run segment.
    #    Separately: a txn whose total != its OWN run's segment sum is reported as a FINDING.
    for name, recs in logs.items():
        seg = AL.ZERO_BUDGET
        run = 0
        for i, r in enumerate(recs):
            if r["type"] in BUDGETED:
                seg = AL.add_budget(seg, r["body"]["budget"])
            elif r["type"] == "ledger.transaction":
                run += 1
                tb = r["body"]["total_budget"]
                if flavor(recs) == "sha256-prev":
                    check(_close(_budget_vec(tb), _budget_vec(AL.route_total(recs[:i], r["body"]["route"]))),
                          "R4 %s txn seq %d" % (name, r["seq"]))
                run_vec = byrun.get("%s/%03d" % (name, run - 1), {})
                check(_close(run_vec, _budget_vec(seg)), "R4b %s run %d facts != segment" % (name, run - 1))
                if flavor(recs) == "fnv1a-hash":
                    check(_close(_budget_vec(tb), _budget_vec(seg)), "R4 %s txn seq %d" % (name, r["seq"]))
                elif not _close(_budget_vec(tb), _budget_vec(seg)):
                    rep["findings"].append({"log": name, "dev": r["dev"], "seq": r["seq"],
                                            "route": r["body"]["route"],
                                            "declared_wall_ms": tb["wall_ms"], "own_run_wall_ms": seg["wall_ms"]})
                seg = AL.ZERO_BUDGET
    # R5 cross-projection: OTel spans (activeledger.otel_export) sum to the same per-kind wall_ms/usd
    for name, recs in logs.items():
        if flavor(recs) != "sha256-prev":
            continue
        spans = otel_export.export(recs)["spans"]
        ot = {}
        for s in spans:
            a = s["attributes"]
            if a["activelog.type"] == "ledger.transaction":
                continue                                  # txn spans carry the TOTAL: summing them double-counts
            kind = a["openinference.span.kind"] if a["activelog.type"] == "cell.tick" else "HOP"
            _vadd(ot.setdefault(kind, {}), "wall_ms", _exact(a["activeledger.budget.wall_ms"]))
            _vadd(ot.setdefault(kind, {}), "usd", _exact(a["activeledger.budget.usd"]))
        pk = pivot(fs_by_log.get(name, []), "kind", "component", where=lambda f: f["component"] in ("wall_ms", "usd"))
        check(all(_close(ot[k], pk["row_tot"][k]) for k in ot) and set(ot) == set(pk["row_tot"]),
              "R5 %s OTel projection != pivot" % name)
    return rep


# ---- tick-scrubber ---------------------------------------------------------------------

def _summary(body: dict) -> dict:
    return {k: v for k, v in body.items() if k not in ("budget", "total_budget", "binds", "confidences")}


def fold(records: list[dict], t: int, fl: str | None = None) -> dict:
    """State of a run after its first t records. Pure; always recomputed from the prefix."""
    st = {"tick": 0, "head": head_of([], fl or flavor(records)), "seq_next": 0, "counts": {k: 0 for k in AL.TYPES},
          "total": AL.ZERO_BUDGET, "by_route": {}, "open": AL.ZERO_BUDGET, "cells": {}, "settled": [],
          "last": None}
    for r in records[:t]:
        _advance(st, r)
    return copy.deepcopy(st)                            # detach from the records' nested dicts


def step_state(st: dict, r: dict) -> dict:
    """Advance a state by ONE record (new dict; the input state is not mutated)."""
    st = copy.deepcopy(st)
    _advance(st, r)
    return copy.deepcopy(st)


def _advance(st: dict, r: dict) -> None:
    b = r["body"]
    st["tick"] += 1
    st["seq_next"] = r["seq"] + 1
    st["counts"][r["type"]] = st["counts"].get(r["type"], 0) + 1
    if r["type"] in BUDGETED:
        route = str(b.get("route", "(none)"))
        st["total"] = AL.add_budget(st["total"], b["budget"])
        st["by_route"][route] = AL.add_budget(st["by_route"].get(route, AL.ZERO_BUDGET), b["budget"])
        st["open"] = AL.add_budget(st["open"], b["budget"])
        key = b["cell"] if r["type"] == "cell.tick" else "%s->%s" % (b["credit"]["cell"], b["debit"]["cell"])
        st["cells"][key] = _summary(b)
    else:
        st["settled"].append({"route": str(b.get("route")), "seq": r["seq"]})
        st["open"] = AL.ZERO_BUDGET
    st["last"] = {"dev": r["dev"], "seq": r["seq"], "type": r["type"]}
    st["head"] = r["hash"] if "hash" in r else AL.link_hash(r)


def state_hash(st: dict) -> str:
    return AL.content_hash(st)


class Scrubber:
    """Step / rewind / seek over one recorded run. Holds a private deep copy; never writes to it."""

    def __init__(self, records: list[dict], name: str = "run", fl: str | None = None):
        if not verify(records):
            raise ValueError("refusing to scrub an unverified chain: %s" % name)
        self._recs = copy.deepcopy(records)
        self.name, self.n, self.t = name, len(records), 0
        self.flavor = fl or flavor(self._recs)
        self._state = fold(self._recs, 0, self.flavor)
        self.recorded_hash = run_hash(self._recs)

    def state_at(self, t: int) -> dict:
        if not isinstance(t, int) or isinstance(t, bool) or not 0 <= t <= self.n:
            raise IndexError("tick %r out of range 0..%d" % (t, self.n))
        return fold(self._recs, t, self.flavor)

    def record(self, t: int) -> dict:
        """The record that moved state t-1 -> t (1-based tick), as a copy."""
        if not 1 <= t <= self.n:
            raise IndexError("record tick %r out of range 1..%d" % (t, self.n))
        return copy.deepcopy(self._recs[t - 1])

    def step(self) -> dict:
        if self.t >= self.n:
            raise IndexError("at end of run")
        self._state = step_state(self._state, self._recs[self.t])
        self.t += 1
        return copy.deepcopy(self._state)

    def back(self) -> dict:
        return self.seek(self.t - 1)

    def seek(self, t: int) -> dict:
        self._state = self.state_at(t)                  # rewind = refold from genesis: cannot drift
        self.t = t
        return copy.deepcopy(self._state)

    def fork(self, t: int, branch: str) -> "Fork":
        if not 0 <= t <= self.n:
            raise IndexError("fork tick %r out of range 0..%d" % (t, self.n))
        if not branch or "#" in branch:
            raise ValueError("branch must be non-empty and contain no '#'")
        return Fork(self._recs[:t], self.name, branch, self.name, t, self.flavor)


class Fork:
    """A NEW derived log: byte-identical prefix + appends under dev '<base>#<branch>'."""

    def __init__(self, prefix: list[dict], base_dev: str, branch: str, parent: str, at: int, fl: str):
        self.flavor = fl
        self.dev = "%s#%s" % (base_dev, branch)
        self.meta = {"parent": parent, "at": at, "branch": branch, "dev": self.dev,
                     "fork_head": head_of(prefix, fl), "parent_prefix_hash": run_hash(prefix)}
        log = CALC.ActiveLog(dev=self.dev) if fl == "fnv1a-hash" else AL.ActiveLog(dev=self.dev)
        log.records = copy.deepcopy(prefix)
        log.seq = at
        log.mono = prefix[-1]["mono"] if prefix else 0
        self._log = log

    @property
    def records(self) -> list[dict]:
        return self._log.records

    def emit(self, type_: str, body: dict) -> dict:
        return self._log.emit(type_, body)            # the owner's emitter: same validation + chain rule

    def scrubber(self) -> Scrubber:
        return Scrubber(self.records, name="%s#%s" % (self.meta["parent"], self.meta["branch"]), fl=self.flavor)

    def fork(self, t: int, branch: str) -> "Fork":
        if not branch or "#" in branch:
            raise ValueError("branch must be non-empty and contain no '#'")
        s = self.scrubber()
        if not 0 <= t <= s.n:
            raise IndexError("fork tick %r out of range 0..%d" % (t, s.n))
        return Fork(s._recs[:t], self.dev, branch, s.name, t, self.flavor)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--record", action="store_true", help="(re)write runs/*.jsonl from the live producers")
    ap.add_argument("--rows", default="cell")
    ap.add_argument("--cols", default="component")
    ap.add_argument("--measure", default=None)
    a = ap.parse_args()
    logs = record_corpus()
    if a.record:
        write_runs(logs)
        print("recorded %d logs -> %s" % (len(logs), RUNS))
    logs = read_runs() or logs
    fs = facts(logs)
    p = pivot(fs, a.rows, a.cols)
    rep = reconcile(logs, p, fs)
    print(render(p, a.measure))
    print("\nreconciled: %d checks; findings: %d" % (rep["checks"], len(rep["findings"])))
