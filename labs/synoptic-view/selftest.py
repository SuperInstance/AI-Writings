#!/usr/bin/env python3
"""synoptic-view selftest — offline, deterministic. Proves:
  * replay == live: the recorded runs/*.jsonl are byte-identical to a fresh re-run of every producer,
    and every chain verifies with its OWNER's verify (activeledger / calc-quilt);
  * pivots reconcile: for many 2D projections the cells, margins and grand total sum back to the
    ledger (independent add_budget fold, route_total, txn declared totals, OTel span projection);
  * rewind reproduces the exact per-tick state (== a live tap captured while the run was emitted);
  * fork is byte-identical up to the fork tick and independent after it; the recorded run is untouched.
"""

from __future__ import annotations

import copy
import random

import synoptic_view as S
from synoptic_view import AL, CALC

checks = failures = 0


def check(name, ok):
    global checks, failures
    checks += 1
    if not ok:
        failures += 1
        print("FAIL", name)


def raises(fn, exc=Exception):
    try:
        fn()
    except exc:
        return True
    return False


# ---- corpus: replay == live --------------------------------------------------------------

logs = S.read_runs()
check("four recorded logs on disk", sorted(logs) == ["calculator", "examples.shared", "route_sim.filtered",
                                                      "route_sim.nofilter"])
live = S.record_corpus()
for name in live:
    check("replay==live bytes: " + name, S.to_jsonl(live[name]) == (S.RUNS / (name + ".jsonl")).read_text())
    check("owner verify: " + name, S.verify(logs[name]))
check("flavors", S.flavor(logs["calculator"]) == "fnv1a-hash" and S.flavor(logs["route_sim.filtered"]) == "sha256-prev")
shared_devs = {r["dev"] for r in logs["examples.shared"]}
check("six examples on ONE shared chain", shared_devs == set(S.SHARED_EXAMPLES) and S.verify(logs["examples.shared"]))
before = {k: S.run_hash(v) for k, v in logs.items()}

# ---- pivot / synopsis --------------------------------------------------------------------

fs = S.facts(logs)
PAIRS = [("cell", "component"), ("route", "axis"), ("dev", "kind"), ("log", "type"), ("kind", "axis"),
         ("run", "component"), ("reqs", "api"), ("path", "axis"), ("cell", "axis"), ("type", "component")]
for rows, cols in PAIRS:
    p = S.pivot(fs, rows, cols)
    try:
        rep = S.reconcile(logs, p, fs)
        ok = rep["checks"] > 100
    except S.ReconcileError as e:
        print("  ", e)
        ok = False
    check("pivot %s x %s reconciles to ledger" % (rows, cols), ok)
    check("render %s x %s" % (rows, cols), S.render(p, "wall_ms").count("\n") == len(p["row_keys"]) + 2)

# per-tick pivot over one run
pt = S.pivot(fs, "tick", "component", where=lambda f: f["log"] == "route_sim.filtered")
check("tick x component reconciles to route total",
      S._close(pt["grand"], S._budget_vec(AL.route_total(logs["route_sim.filtered"], "route:mic-stt-llm:filtered"))))

# anchors from upstream READMEs (activeledger: route total wall_ms 175 -> 113; calc: simple 5 vs full 16)
bylog = S.pivot(fs, "log", "component")["row_tot"]
check("route_sim filtered wall_ms == 113", bylog["route_sim.filtered"]["wall_ms"] == 113)
check("route_sim nofilter wall_ms == 175", bylog["route_sim.nofilter"]["wall_ms"] == 175)
calc_runs = S.pivot(fs, "run", "component", where=lambda f: f["log"] == "calculator")["row_tot"]
check("calc runs: 5 simple @5ms + 1 full @16ms",
      sorted(v["wall_ms"] for v in calc_runs.values()) == [5, 5, 5, 5, 5, 16])

# synopsis per cell: the four headline aggregates reconcile to the ledger fold
syn = S.synopsis(fs, "cell")
fold = AL.ZERO_BUDGET
for recs in logs.values():
    for r in recs:
        if r["type"] in S.BUDGETED:
            fold = AL.add_budget(fold, r["body"]["budget"])
tot = {"wall_ms": 0, "tokens": 0, "usd": 0, "storage_bytes": 0}
for agg in syn["rows"].values():
    for k in tot:
        tot[k] += agg[k]
check("synopsis wall_ms sums to ledger", tot["wall_ms"] == fold["wall_ms"] == syn["total"]["wall_ms"])
check("synopsis tokens sums to ledger", tot["tokens"] == sum(fold["tokens"].values()) == syn["total"]["tokens"])
check("synopsis usd sums to ledger", abs(float(tot["usd"]) - fold["usd"]) < 1e-9)
check("synopsis storage sums to ledger",
      tot["storage_bytes"] == fold["storage_bytes"]["train"] + fold["storage_bytes"]["prod"])

# the iron-triangle 'good' corner is honestly empty: standing is not in the ledger
ax = S.pivot(fs, "route", "axis")
check("good axis present but empty", ax["col_tot"]["good"] == {} and "good" in ax["col_keys"])
check("unknown dimension refused", raises(lambda: S.pivot(fs, "pattern", "env"), ValueError))

# negative controls: a projection that does not sum back MUST be caught
bad = copy.deepcopy(fs)
bad[5]["value"] += 1
check("tampered fact -> ReconcileError", raises(lambda: S.reconcile(logs, None, bad), S.ReconcileError))
check("dropped fact -> ReconcileError", raises(lambda: S.reconcile(logs, None, fs[1:]), S.ReconcileError))
check("duplicated fact -> ReconcileError", raises(lambda: S.reconcile(logs, None, fs + fs[:1]), S.ReconcileError))
tl = copy.deepcopy(logs)
tl["route_sim.filtered"][2]["body"]["budget"]["wall_ms"] += 1
check("tampered ledger -> ReconcileError (owner verify)", raises(lambda: S.reconcile(tl), S.ReconcileError))
tc = copy.deepcopy(logs)
tc["calculator"][1]["body"]["budget"]["usd"] = 1.0
check("tampered fnv1a chain -> ReconcileError", raises(lambda: S.reconcile(tc), S.ReconcileError))
pm = S.pivot(fs, "cell", "axis")
pm["row_tot"][pm["row_keys"][0]]["wall_ms"] += 1
check("broken margin -> ReconcileError", raises(lambda: S.reconcile(logs, pm, fs), S.ReconcileError))

# findings: declared txn totals vs each run's own segment (an UPSTREAM property, not a projection bug)
rep = S.reconcile(logs, None, fs)
fdevs = sorted({f["dev"] for f in rep["findings"]})
check("findings = route-id reuse in convert + image-thumb", fdevs == ["convert-quilt", "image-thumb-quilt"]
      and len(rep["findings"]) == 9 and all(f["declared_wall_ms"] > f["own_run_wall_ms"] for f in rep["findings"]))
# crew-proposed invariant "sum of txn totals == sum of records" is FALSE here (cumulative route ids) — rejected
txn_sum = AL.ZERO_BUDGET
for r in logs["examples.shared"]:
    if r["type"] == "ledger.transaction":
        txn_sum = AL.add_budget(txn_sum, r["body"]["total_budget"])
shared_fold = S.pivot(fs, "log", "component")["row_tot"]["examples.shared"]
check("crew invariant (sum txn totals == records) rejected", txn_sum["wall_ms"] != shared_fold["wall_ms"])

# ---- tick-scrubber ----------------------------------------------------------------------

# live tap: capture the head + per-route totals AFTER EACH EMIT while route_sim runs for real
taps = []


class TapLog(AL.ActiveLog):
    def emit(self, type_, body):
        env = super().emit(type_, body)
        routes = {str(r["body"].get("route")) for r in self.records if r["type"] in S.BUDGETED}
        taps.append({"n": len(self.records), "head": AL.link_hash(self.records[-1]),
                     "by_route": {rt: AL.route_total(self.records, rt) for rt in routes}})
        return env


orig_cls = S.route_sim.ActiveLog
S.route_sim.ActiveLog = TapLog
try:
    tapped = S.route_sim.run(True)["log"].records
finally:
    S.route_sim.ActiveLog = orig_cls
rec = logs["route_sim.filtered"]
check("tapped live run == recorded run", S.to_jsonl(tapped) == S.to_jsonl(rec))
sc = S.Scrubber(rec, "route_sim.filtered")
check("rewind == live tap at every tick", all(
    sc.state_at(tp["n"])["head"] == tp["head"] and sc.state_at(tp["n"])["by_route"] == tp["by_route"]
    for tp in taps))

for name in ("route_sim.filtered", "examples.shared", "calculator"):
    recs = logs[name]
    sc = S.Scrubber(recs, name)
    fwd = [S.state_hash(sc.state_at(0))]
    while sc.t < sc.n:
        fwd.append(S.state_hash(sc.step()))
    check("%s: incremental step == fresh fold at every tick" % name,
          all(fwd[t] == S.state_hash(S.fold(recs, t)) for t in range(sc.n + 1)))
    rev_ok = all(S.state_hash(sc.seek(t)) == fwd[t] for t in range(sc.n, -1, -1))
    order = list(range(sc.n + 1))
    random.Random(5).shuffle(order)
    rnd_ok = all(S.state_hash(sc.seek(t)) == fwd[t] for t in order)
    check("%s: rewind (reverse + shuffled seek) reproduces exact per-tick state" % name, rev_ok and rnd_ok)
    sc.seek(sc.n)
    back_ok = True
    while sc.t > 0:
        t = sc.t
        back_ok &= S.state_hash(sc.back()) == fwd[t - 1]
    check("%s: back() walks to genesis exactly" % name, back_ok and raises(sc.back, IndexError))
    heads = all(sc.state_at(t)["head"] == S.head_of(recs[:t], S.flavor(recs)) for t in range(sc.n + 1))
    check("%s: per-tick head == chain link" % name, heads)
    end = sc.state_at(sc.n)
    tf = AL.ZERO_BUDGET
    for r in recs:
        if r["type"] in S.BUDGETED:
            tf = AL.add_budget(tf, r["body"]["budget"])
    check("%s: state at N totals == ledger fold" % name, end["total"] == tf)

sc = S.Scrubber(rec, "route_sim.filtered")
N = sc.n
check("t=0 is genesis", sc.state_at(0)["head"] == AL.GENESIS and sc.state_at(0)["total"] == AL.ZERO_BUDGET)
check("calc t=0 genesis is its own", S.Scrubber(logs["calculator"], "c").state_at(0)["head"] == CALC.GENESIS)
check("out of range ticks refused", all(raises(lambda t=t: sc.state_at(t), IndexError) for t in (-1, N + 1, True, "3", 1.0)))
sc.seek(N)
check("step past end refused", raises(sc.step, IndexError))
s3 = sc.state_at(3)
s3["total"]["wall_ms"] = 10 ** 9
s3["cells"].clear()
check("mutating a returned state does not alias", S.state_hash(sc.state_at(3)) == fwd_h if (fwd_h := S.state_hash(S.fold(rec, 3))) else False)
mut = copy.deepcopy(rec)
sm = S.Scrubber(mut, "m")
h3 = S.state_hash(sm.state_at(3))
mut[0]["body"]["cell"] = "hacked"
check("scrubber holds a private copy", S.state_hash(sm.state_at(3)) == h3)
tamp = copy.deepcopy(rec)
tamp[4]["body"]["load"] = 99
check("tampered record refused", raises(lambda: S.Scrubber(tamp, "t"), ValueError))
tamp2 = copy.deepcopy(rec)
tamp2[3]["prev"] = AL.GENESIS
check("tampered prev refused", raises(lambda: S.Scrubber(tamp2, "t"), ValueError))
sorted_keys = [{k: r[k] for k in reversed(list(r))} for r in rec]
check("key order does not change the fold", S.state_hash(S.fold(sorted_keys, N)) == S.state_hash(S.fold(rec, N)))

# ---- fork ------------------------------------------------------------------------------


def fork_suite(name, recs, ts, mk_body):
    sc = S.Scrubber(recs, name)
    orig_bytes, orig_hash = S.to_jsonl(recs), S.run_hash(recs)
    for t in ts:
        f = sc.fork(t, "b%d" % t)
        check("%s fork@%d: prefix byte-identical" % (name, t), S.to_jsonl(f.records) == S.to_jsonl(recs[:t]))
        check("%s fork@%d: state identical up to fork tick" % (name, t),
              all(S.state_hash(f.scrubber().state_at(k)) == S.state_hash(sc.state_at(k)) for k in range(t + 1)))
        e1 = f.emit("cell.tick", mk_body("whatif-%d" % t))
        e2 = f.emit("cell.tick", mk_body("whatif2-%d" % t))
        link = e1["prev"] if "hash" not in e1 else e1["prev"]
        check("%s fork@%d: first append chains to head at t" % (name, t), link == S.head_of(recs[:t], S.flavor(recs)))
        check("%s fork@%d: appends carry branch prefix + verify" % (name, t),
              e1["dev"] == e2["dev"] == "%s#b%d" % (name, t) and S.verify(f.records) and e1["seq"] == t)
        okeys = {(r["dev"], r["seq"]) for r in recs}
        fkeys = {(r["dev"], r["seq"]) for r in f.records[t:]}
        check("%s fork@%d: no (dev,seq) collision" % (name, t), not okeys & fkeys)
        check("%s fork@%d: recorded run untouched" % (name, t),
              S.to_jsonl(recs) == orig_bytes and S.run_hash(recs) == orig_hash and sc.recorded_hash == orig_hash)
        if t < len(recs):
            check("%s fork@%d: independent after the fork tick" % (name, t),
                  S.state_hash(f.scrubber().state_at(t + 1)) != S.state_hash(sc.state_at(t + 1)))
        if t:
            f.records[0]["body"]["poke"] = 1
            check("%s fork@%d: mutating fork does not touch original" % (name, t),
                  S.to_jsonl(recs) == orig_bytes and not S.verify(f.records))


sim_body = lambda tag: {"cell": tag, "kind": "SIM", "route": "whatif",  # noqa: E731
                        "budget": AL.budget(wall_ms=1, prod=8, train=16)}
calc_body = lambda tag: {"cell": tag, "kind": "SIM", "budget": CALC.budget(1, 0.1, 1, 8, 16)}  # noqa: E731
fork_suite("route_sim.filtered", rec, [0, 1, 4, N], sim_body)
fork_suite("calculator", logs["calculator"], [0, 7, len(logs["calculator"])], calc_body)
fork_suite("examples.shared", logs["examples.shared"], [150], sim_body)

# fork re-emitting the original continuation: same budgets, distinct branch (links diverge by dev)
sc = S.Scrubber(rec, "route_sim.filtered")
f = sc.fork(2, "replay")
for r in rec[2:]:
    f.emit(r["type"], copy.deepcopy(r["body"]))
check("replayed fork: same budgets at N", f.scrubber().state_at(N)["total"] == sc.state_at(N)["total"])
check("replayed fork: prefix links equal, suffix links differ",
      [r["prev"] for r in f.records[:3]] == [r["prev"] for r in rec[:3]]
      and all(a["prev"] != b["prev"] for a, b in zip(f.records[3:], rec[3:])))
# appending to a copy of the ORIGINAL does not touch the fork
orig_live = AL.ActiveLog(dev="route_sim.filtered")
orig_live.records, orig_live.seq, orig_live.mono = copy.deepcopy(rec), N, rec[-1]["mono"]
fb = S.to_jsonl(f.records)
orig_live.emit("cell.tick", sim_body("orig-grows"))
check("original growing does not touch the fork", S.to_jsonl(f.records) == fb)

# fork of a fork
f1 = sc.fork(4, "a")
f1.emit("cell.tick", sim_body("a1"))
f2 = f1.fork(5, "b")
f2.emit("cell.tick", sim_body("b1"))
check("fork-of-fork: prefix == parent fork prefix", S.to_jsonl(f2.records[:5]) == S.to_jsonl(f1.records[:5]))
check("fork-of-fork: dev nests + verifies", f2.records[-1]["dev"] == "route_sim.filtered#a#b" and S.verify(f2.records)
      and S.to_jsonl(f2.records[:4]) == S.to_jsonl(rec[:4]))
check("fork emit reuses owner validation (unbalanced hop refused)", raises(lambda: f2.emit("route.hop", {
    "credit": {"cell": "a", "units": "u", "amount": 1}, "debit": {"cell": "b", "units": "u", "amount": 5},
    "price": {"from": "u", "to": "u", "rate": 1, "ref": "x"}, "budget": AL.budget()}), ValueError))
check("bad branch names refused", raises(lambda: sc.fork(1, ""), ValueError) and raises(lambda: sc.fork(1, "a#b"), ValueError)
      and raises(lambda: sc.fork(N + 1, "x"), IndexError))

# ---- read-only: nothing above changed any recorded run -----------------------------------

check("projections are read-only (run hashes unchanged)", {k: S.run_hash(v) for k, v in logs.items()} == before)
check("recorded files still verify after everything", all(S.verify(v) for v in S.read_runs().values()))

print("synoptic-view selftest: %d checks, %d failures" % (checks, failures))
raise SystemExit(1 if failures else 0)
