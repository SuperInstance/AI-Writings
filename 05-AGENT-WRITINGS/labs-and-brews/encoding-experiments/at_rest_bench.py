"""E12 at_rest_bench — the promoted, schema-agnostic ALR1 format (labs/activeledger/at_rest.py)
measured against JSONL, JSONL+lzma and E1's hand-fitted columnar codec.

E1 proved 187x on ONE fixed budget schema. ALR1 must work on any body the B1 emitter
accepts (nested dicts, lists, strings, floats, bools), with no schema supplied. The cost
of generality is the measurement here.

Logs:
  e1-ticks     E1's 2,000 cell.tick records (fixed schema; E1's codec applies)
  voice-mix    B1's route_sim run re-emitted 300 times into one chain (2,700 records of
               cell.tick / route.hop / ledger.transaction with the real body shapes; the
               numbers get seeded jitter, strings are the real ones) — HONEST LABEL: jittered replay
  routes-e8    the E8 route runs (store + retrieval routes), concatenated per run

Measured: bytes for each form, exact round-trip, pack+unpack ms, and BER-1e-4 survival
(6 trials) with and without the RS flag.

Run: python3 at_rest_bench.py [--selftest]
"""
from __future__ import annotations
import copy, lzma, os, sys, time
import common as C
import delta_budget as E1

sys.path.insert(0, os.path.join(C.HERE, "..", "activeledger"))
import activeledger as AL  # noqa: E402
import at_rest as AR  # noqa: E402
import route_sim as RS  # noqa: E402


def voice_mix(reps=300, seed=3):
    base = RS.run(True)["log"].records
    r = C.Rng(seed)
    log = AL.ActiveLog(dev="voice-mix")

    def jitter(obj, key=None):
        if isinstance(obj, dict):
            return {k: jitter(v, k) for k, v in obj.items()}
        if isinstance(obj, list):
            return [jitter(v) for v in obj]
        if isinstance(obj, bool) or obj is None or isinstance(obj, str):
            return obj
        if isinstance(obj, int):
            return max(0, obj + r.randint(-2, 2)) if key in ("wall_ms", "mem_mb") else obj
        if isinstance(obj, float) and key in ("power_w", "confidence"):
            return round(max(0.0, obj * (1 + 0.05 * r.gauss())), 4)
        return obj

    for k in range(reps):
        for rec in base:
            body = jitter(copy.deepcopy(rec["body"]))
            if rec["type"] == "ledger.transaction":
                body["route"] = body["route"] + "#%d" % k
            if rec["type"] == "route.hop":  # keep the double entry balanced: re-derive the budget only
                body = dict(rec["body"], budget=jitter(copy.deepcopy(rec["body"]["budget"])))
            log.emit(rec["type"], body)
    return log.records


def logs():
    import encoding_routes as E8
    out = {"e1-ticks": E1.build_log(2000), "voice-mix": voice_mix()}
    recs = E1.build_log(200, seed=40)
    runs = []
    for name, (stored, back, ms) in E8.store_routes(recs).items():
        runs += E8.route_run(name, [("encode+decode", ms, len(stored))], {"n": len(back), "records_hash": AL.content_hash(back)})[:]
    # re-chain the concatenated route runs into one log (each run was its own chain)
    log = AL.ActiveLog(dev="routes-e8")
    for rec in runs:
        log.emit(rec["type"], rec["body"])
    out["routes-e8"] = log.records
    return out


def survive(blob, recs, r, trials=6):
    ok = 0
    for _ in range(trials):
        b = bytearray(blob)
        nbits = (len(b) - 5) * 8
        for _ in range(max(1, round(nbits * 1e-4))):
            p = r.randint(0, nbits - 1)
            b[5 + p // 8] ^= 1 << (p % 8)
        try:
            ok += AL.canon(AR.unpack(bytes(b))) == AL.canon(recs)
        except Exception:
            pass
    return ok


def measure(log=print):
    res = {}
    r = C.Rng(12)
    for name, recs in logs().items():
        jsonl = "".join(AL.canon(x) + "\n" for x in recs).encode()
        row = {"records": len(recs), "jsonl": len(jsonl), "jsonl+lzma": len(lzma.compress(jsonl, preset=9))}
        if name == "e1-ticks":
            row["E1-hand-fit"] = len(lzma.compress(E1.encode(E1.to_cols(recs), "ctx-mean"), preset=9)) + 32
        t0 = time.time()
        blob = AR.pack(recs)
        back = AR.unpack(blob)
        row["alr1_ms"] = round(1000 * (time.time() - t0))
        assert AL.canon(back) == AL.canon(recs)
        row["ALR1"] = len(blob)
        rblob = AR.pack(recs, repair=True)
        row["ALR1+RS"] = len(rblob)
        row["survive_ber1e-4"] = {"ALR1": survive(blob, recs, r), "ALR1+RS": survive(rblob, recs, r)}
        res[name] = row
        extra = f"  E1-hand-fit {row['E1-hand-fit']}" if "E1-hand-fit" in row else ""
        log(f"  {name:10s} {row['records']:5d} rec | jsonl {row['jsonl']:8d} | +lzma {row['jsonl+lzma']:7d} | "
            f"ALR1 {row['ALR1']:6d} ({row['jsonl'] / row['ALR1']:.0f}x jsonl, {row['jsonl+lzma'] / row['ALR1']:.1f}x lzma) | "
            f"ALR1+RS {row['ALR1+RS']:6d}{extra} | {row['alr1_ms']} ms | BER1e-4 survive {row['survive_ber1e-4']}")
    return res


def selftest():
    c = C.Checks()
    vm = voice_mix(reps=4)
    c.ok(AL.verify_chain(vm), "voice-mix chain verifies")
    c.ok(len({r["type"] for r in vm}) == 3, "voice-mix has all three record types")
    blob = AR.pack(vm)
    c.ok(AL.canon(AR.unpack(blob)) == AL.canon(vm), "ALR1 round-trips voice-mix")
    t = E1.build_log(50)
    c.ok(AL.canon(AR.unpack(AR.pack(t))) == AL.canon(t), "ALR1 round-trips e1 ticks")
    odd = AL.ActiveLog(dev="odd")
    odd.emit("ledger.transaction", {"route": "x", "vals": [-0.0, 1e-7, 2.5, -3.25, 10 ** 20, True, None, "é"], "nest": {"a": [{"b": 1.1}]}})
    c.ok(AL.canon(AR.unpack(AR.pack(odd.records))) == AL.canon(odd.records), "ALR1 round-trips awkward JSON (-0.0, 1e-7, bigint, unicode)")
    return c.report("at_rest_bench")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    import json
    print("E12 at_rest_bench — ALR1 (schema-agnostic) vs JSONL / JSONL+lzma / E1's hand-fitted codec")
    res = measure()
    with open(C.HERE + "/results_at_rest_bench.json", "w") as f:
        json.dump(res, f, indent=1)
