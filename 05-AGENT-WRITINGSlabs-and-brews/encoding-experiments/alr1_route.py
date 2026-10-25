"""E15 alr1_route — the at-rest format as a REAL System-2 route that B7 prices.

The job, "serve an archive of recorded route runs back so System-2 can backtest them",
has one product and several routes:

  product   for every run in the archive, B7's OWN replay of it: (route label,
            product_hash, content hash of the replayed total budget), in order. Two
            storage routes are product-identical only if every run comes back so exactly
            that B7 replays it to the same verdict inputs.
  routes    jsonl        the runs as canonical JSONL (blank line between runs)
            jsonl+lzma   the same bytes through lzma -9 (the fair baseline)
            alr1         labs/activeledger/at_rest.py: pack (one run) / pack_many (ALRM)
            alr1+rs      the same with the Reed-Solomon repair flag
  budget    each route is itself an ActiveLog run: cell.tick "decode" (wall_ms = best of
            3 measured decode times) + cell.tick "replay" (B7 replay time) with
            storage_bytes.prod = bytes at rest; closed by a ledger.transaction carrying
            the product. B7 replays THOSE runs and prices them on
            {good, fast = wall_ms, cheap = usd/tokens/storage bytes}.
  good      B4 standing = trials out of 6 whose archive survives BER 1e-4 intact.

Corpus (all real emitter output; HONEST LABEL on the third):
  fixtures   every run B7's own fixture_pairs() produces from the five example quilts
  routesim   labs/activeledger route_sim, filtered + unfiltered
  voice300   300 route_sim runs with seeded jitter on wall_ms/mem_mb/power/confidence
             (strings and shapes real; each run's declared total recomputed so B7 replays it)

Cases: each fixture run served alone (tiny archives), then the whole fixtures+routesim set
batched, then voice300 batched. Run: python3 alr1_route.py [--selftest]
"""
from __future__ import annotations
import copy, json, lzma, os, sys, time
import common as C

for sub in ("activeledger", "system2-backtest", "route-preference"):
    sys.path.insert(0, os.path.join(C.HERE, "..", sub))
import activeledger as AL  # noqa: E402
import at_rest as AR  # noqa: E402
import backtest as B7  # noqa: E402
import route_preference as B4  # noqa: E402
import route_sim as RS  # noqa: E402

ROUTES = ("jsonl", "jsonl+lzma", "alr1", "alr1+rs")


# ---------------- corpus ------------------------------------------------------------------
def fixture_runs():
    runs = []
    for _name, (_labels, cases) in B7.fixture_pairs().items():
        for c in cases:
            for side in ("a", "b"):
                if c[side]:
                    runs.append(c[side])
    return runs


def routesim_runs():
    return [RS.run(True)["log"].records, RS.run(False)["log"].records]


def voice_runs(n=300, seed=5):
    r = C.Rng(seed)
    base = RS.run(True)["log"].records

    def jit(obj, key=None):
        if isinstance(obj, dict):
            return {k: jit(v, k) for k, v in obj.items()}
        if isinstance(obj, list):
            return [jit(v) for v in obj]
        if isinstance(obj, bool) or not isinstance(obj, (int, float)):
            return obj
        if isinstance(obj, int) and key in ("wall_ms", "mem_mb"):
            return max(0, obj + r.randint(-2, 2))
        if isinstance(obj, float) and key in ("power_w", "confidence"):
            return round(max(0.0, obj * (1 + 0.05 * r.gauss())), 4)
        return obj

    out = []
    for k in range(n):
        log = AL.ActiveLog(dev="voice-%d" % k)
        total = AL.ZERO_BUDGET
        for rec in base:
            body = copy.deepcopy(rec["body"])
            if rec["type"] in ("cell.tick", "route.hop"):
                body["budget"] = jit(body["budget"])
                if rec["type"] == "cell.tick":
                    body = {**jit({kk: vv for kk, vv in body.items() if kk != "budget"}), "budget": body["budget"]}
                total = AL.add_budget(total, body["budget"])
            else:
                body["total_budget"] = total
            log.emit(rec["type"], body)
        out.append(log.records)
    return out


# ---------------- the four storage routes -------------------------------------------------------
def store(runs, route):
    if route.startswith("jsonl"):
        blob = "\n".join("".join(AL.canon(x) + "\n" for x in run) for run in runs).encode()
        return lzma.compress(blob, preset=9) if route == "jsonl+lzma" else blob
    rep = route == "alr1+rs"
    return AR.pack(runs[0], repair=rep) if len(runs) == 1 else AR.pack_many(runs, repair=rep)


def load(blob, route, n_runs):
    if route.startswith("jsonl"):
        text = (lzma.decompress(blob) if route == "jsonl+lzma" else blob).decode()
        runs = [[json.loads(l) for l in chunk.splitlines() if l] for chunk in text.split("\n\n")]
        if len(runs) != n_runs or not all(AL.verify_chain(r) or AR._fnv_chain_ok(r) for r in runs):
            raise ValueError("jsonl archive does not replay")
        return runs
    return [AR.unpack(blob)] if n_runs == 1 else AR.unpack_many(blob)


def replay_product(runs):
    out = []
    for run in runs:
        rp = B7.replay_route(run)
        out.append([rp["route"], rp["product_hash"], AL.content_hash(rp["budget"])])
    return {"n_runs": len(runs), "replays": out}


def best_ms(fn, reps=3):
    best, res = None, None
    for _ in range(reps):
        t0 = time.perf_counter()
        res = fn()
        ms = (time.perf_counter() - t0) * 1000
        best = ms if best is None else min(best, ms)
    return res, max(1, round(best))


def serve(runs, route):
    """-> (the route's own ActiveLog records, bytes at rest)."""
    blob = store(runs, route)
    back, ms_decode = best_ms(lambda: load(blob, route, len(runs)))
    product, ms_replay = best_ms(lambda: replay_product(back))
    log = AL.ActiveLog(dev="serve-" + route)
    total = AL.ZERO_BUDGET
    for cell, ms, prod in (("decode", ms_decode, len(blob)), ("replay", ms_replay, 0)):
        b = AL.budget(wall_ms=ms, prod=prod)
        log.emit("cell.tick", {"cell": cell, "route": route, "budget": b})
        total = AL.add_budget(total, b)
    log.emit("ledger.transaction", {"route": route, "total_budget": total, **product})
    return log.records, blob


def survival(runs, route, blob, r, trials=6, ber=1e-4):
    ok = 0
    want = AL.canon(runs)
    for _ in range(trials):
        b = bytearray(blob)
        nbits = len(b) * 8
        for _ in range(max(1, round(nbits * ber))):
            p = r.randint(0, nbits - 1)
            b[p // 8] ^= 1 << (p % 8)
        try:
            ok += AL.canon(load(bytes(b), route, len(runs))) == want
        except Exception:
            pass
    return ok


# ---------------- measure ----------------------------------------------------------------------
def pair_line(rep):
    w = rep.get("workload") or {}
    return (f"certified {rep['certified']} refused {rep['refused']} | class {w.get('class')} | "
            f"fast={w.get('preferred_when', {}).get('fast')} cheap={w.get('preferred_when', {}).get('cheap')} | "
            f"totals {rep.get('totals')}")


def measure(log=print):
    r = C.Rng(77)
    fx = fixture_runs()
    rsim = routesim_runs()
    res = {"corpus": {"fixture_runs": len(fx), "fixture_records": sum(len(x) for x in fx), "routesim_runs": 2}}
    log(f"  corpus: {len(fx)} fixture runs ({res['corpus']['fixture_records']} records) from B7.fixture_pairs(), 2 route_sim runs, 300 voice runs")

    # case set 1: every fixture run served alone
    served = {rt: [] for rt in ROUTES}
    for run in fx:
        for rt in ROUTES:
            served[rt].append(serve([run], rt)[0])
    res["single"] = {}
    for a, b in (("jsonl", "alr1"), ("jsonl+lzma", "alr1"), ("alr1", "alr1+rs")):
        rep = B7.backtest_corpus([{"id": "fx%d" % i, "a": served[a][i], "b": served[b][i]} for i in range(len(fx))], (a, b))
        res["single"][f"{a} vs {b}"] = rep
        log(f"  [each fixture run alone] {a} vs {b}: {pair_line(rep)}")

    # case sets 2 & 3: batched archives
    for name, runs in (("fixtures+routesim", fx + rsim), ("voice300", voice_runs())):
        recs, blobs, standing = {}, {}, {}
        for rt in ROUTES:
            recs[rt], blobs[rt] = serve(runs, rt)
            standing[rt] = survival(runs, rt, blobs[rt], r)
        row = {"bytes": {rt: len(b) for rt, b in blobs.items()}, "standing_ber1e-4": standing, "pairs": {}}
        for a, b in (("jsonl", "alr1"), ("jsonl+lzma", "alr1"), ("alr1", "alr1+rs")):
            v = B7.backtest_pair(recs[a], recs[b])
            row["pairs"][f"{a} vs {b}"] = {k: v.get(k) for k in ("status", "class", "axes", "routes", "reason")}
        pref = B4.prefer([(rt, recs[rt]) for rt in ROUTES], standing=standing)
        row["B4"] = {"frontier": pref.get("frontier"), "preferred_when": pref.get("preferred_when"), "status": pref.get("status")}
        res[name] = row
        log(f"  [{name}: {len(runs)} runs batched] bytes {row['bytes']} | BER1e-4 survival /6 {standing}")
        for k, v in row["pairs"].items():
            walls = {rt: ax["wall_ms"] for rt, ax in (v.get("routes") or {}).items()}
            log(f"      B7 {k}: {v['status']} class={v.get('class')} axes={v.get('axes')} wall_ms={walls}")
        log(f"      B4 prefer: frontier={row['B4']['frontier']} preferred_when={row['B4']['preferred_when']}")
    return res


def selftest():
    c = C.Checks()
    runs = routesim_runs()
    for rt in ROUTES:
        blob = store(runs, rt)
        c.ok(AL.canon(load(blob, rt, 2)) == AL.canon(runs), f"{rt} serves the runs back exactly")
    fx = fixture_runs()
    fnv = [x for x in fx if not AL.verify_chain(x)]
    c.ok(len(fnv) > 0 and all(AL.canon(AR.unpack(AR.pack(x))) == AL.canon(x) for x in fnv),
         "ALR1 round-trips the fnv-dialect (calculator-quilt) fixture runs")
    c.ok(AL.canon(AR.unpack_many(AR.pack_many(fx))) == AL.canon(fx), "ALRM round-trips all fixture runs, mixed dialects")
    vr = voice_runs(3)
    c.ok(all(B7.replay_route(x)["route"] for x in vr), "jittered voice runs replay through B7 (totals recomputed)")
    ra, _ = serve(runs, "jsonl")
    rb, _ = serve(runs, "alr1")
    v = B7.backtest_pair(ra, rb)
    c.ok(v["status"] == "certified", "B7 certifies jsonl vs alr1 (identical replays)")
    c.ok(v["axes"]["cheap"] == "alr1", "alr1 wins cheap (storage)")
    # a lossy route must be refused: drop the last record of one run before replay
    bad = AL.ActiveLog(dev="serve-bad")
    prod = replay_product(runs)
    prod["replays"][0][1] = "0x0"
    bad.emit("cell.tick", {"cell": "decode", "route": "bad", "budget": AL.budget(wall_ms=1, prod=1)})
    bad.emit("ledger.transaction", {"route": "bad", "total_budget": AL.budget(wall_ms=1, prod=1), **prod})
    c.ok(B7.backtest_pair(ra, bad.records)["status"] == "refused", "B7 refuses a route whose replay differs")
    return c.report("alr1_route")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    print("E15 alr1_route — serve recorded route runs back for backtesting; four storage routes priced by B7/B4")
    res = measure()
    with open(C.HERE + "/results_alr1_route.json", "w") as f:
        json.dump(res, f, indent=1, default=str)
