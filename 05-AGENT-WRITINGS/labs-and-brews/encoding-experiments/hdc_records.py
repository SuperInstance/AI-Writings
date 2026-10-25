"""E11 hdc_records — where HDC is NOT dominated: structured cells as role-filler hypervectors.

E3 showed flux-hdc-style hypervectors lose to TurboQuant as a plain nearest-neighbour
substrate. Their distinctive power is algebra: a record is a bundle of bound pairs,
    rec = MAJ( ROLE_rel ^ VAL(rel), ROLE_actor ^ VAL(actor), ROLE_tier ^ VAL(tier), ... )
and any field reads back by unbinding (rec ^ ROLE_f -> nearest VAL), while a partial
record works as a query (bundle only the fields you know, rank by Hamming similarity).

Data: situation cells shaped like labs/situation-recorder records (rel, actor, tier, sid,
outcome, route-to), 600 cells, seeded. Measured at D = 1024 bits:
  readback   accuracy of recovering every field by unbinding, vs number of fields bundled
  query      conjunctive query by partial record (2 known fields): precision@|matches|
  cost       bytes per record and the comparison count; no index was built

Run: python3 hdc_records.py [--selftest]
"""
from __future__ import annotations
import sys
import common as C
from hdc_theorems import rand_hv, sim, bundle

FIELDS = {
    "rel": ["TASK", "ROUTE", "DRAFT", "DRAW", "FOLD", "KEEP", "DROP", "MARK", "OUTCOME"],
    "actor": ["opus-5.5", "sonnet-5.5", "deepseek-chat", "glm-4.6", "kimi-k2", "llama-8b"],
    "tier": ["dispatcher", "captain", "crew"],
    "sid": ["sit-%02d" % i for i in range(20)],
    "outcome": ["kept", "dropped", "open"],
    "to": ["deepinfra", "zai", "deepseek", "moth", "local"],
}


class Space:
    def __init__(self, fields, D=1024, seed=31):
        r = C.Rng(seed)
        self.D, self.fields, self.r = D, fields, r
        self.role = {f: rand_hv(r, D) for f in fields}
        self.val = {(f, v): rand_hv(r, D) for f, vs in fields.items() for v in vs}

    def encode(self, rec):
        return bundle([self.role[f] ^ self.val[(f, v)] for f, v in rec.items()], self.r, self.D)

    def read(self, hv, f):
        probe = hv ^ self.role[f]
        return max(self.fields[f], key=lambda v: sim(probe, self.val[(f, v)], self.D))


def records(n, fields, seed=8):
    r = C.Rng(seed)
    return [{f: r.choice(vs) for f, vs in fields.items()} for _ in range(n)]


def measure(n=600, D=1024, log=print):
    res = {"readback": {}}
    for nf in (2, 3, 4, 6):
        fs = dict(list(FIELDS.items())[:nf])
        sp = Space(fs, D)
        recs = records(n, fs)
        hvs = [sp.encode(x) for x in recs]
        ok = sum(sp.read(h, f) == x[f] for h, x in zip(hvs, recs) for f in fs)
        res["readback"][nf] = round(ok / (n * nf), 4)
    log(f"  field read-back by unbinding (D={D}, {n} records): " + ", ".join(f"{k} fields bundled -> {v:.3f}" for k, v in res["readback"].items()))
    sp = Space(FIELDS, D)
    recs = records(n, FIELDS)
    hvs = [sp.encode(x) for x in recs]
    precs = []
    for qi, (rel, actor) in enumerate([("DRAFT", "deepseek-chat"), ("FOLD", "opus-5.5"), ("ROUTE", "sonnet-5.5"),
                                       ("DROP", "glm-4.6"), ("MARK", "kimi-k2"), ("DRAW", "llama-8b")]):
        probe = bundle([sp.role["rel"] ^ sp.val[("rel", rel)], sp.role["actor"] ^ sp.val[("actor", actor)]], sp.r, D)
        truth = {i for i, x in enumerate(recs) if x["rel"] == rel and x["actor"] == actor}
        ranked = C.topk([sim(probe, h, D) for h in hvs], len(truth))
        precs.append(len(truth & set(ranked)) / max(len(truth), 1))
    res["query_precision_at_matches"] = round(sum(precs) / len(precs), 4)
    res["bytes_per_record"] = D // 8
    res["json_bytes_per_record"] = round(sum(len(C.canon(x)) for x in recs) / n, 1)
    log(f"  conjunctive query (rel AND actor) by partial-record probe, 6 fields bundled: precision@|matches| = {res['query_precision_at_matches']}")
    sweep = {}
    for d in (64, 128, 256, 512):
        spd = Space(FIELDS, d)
        hd = [spd.encode(x) for x in recs[:200]]
        rb = sum(spd.read(h, f) == x[f] for h, x in zip(hd, recs[:200]) for f in FIELDS) / (200 * len(FIELDS))
        pr = []
        for rel, actor in [("DRAFT", "deepseek-chat"), ("FOLD", "opus-5.5"), ("ROUTE", "sonnet-5.5")]:
            probe = bundle([spd.role["rel"] ^ spd.val[("rel", rel)], spd.role["actor"] ^ spd.val[("actor", actor)]], spd.r, d)
            truth = {i for i, x in enumerate(recs[:200]) if x["rel"] == rel and x["actor"] == actor}
            ranked = C.topk([sim(probe, h, d) for h in hd], len(truth))
            pr.append(len(truth & set(ranked)) / max(len(truth), 1))
        sweep[d] = {"bytes": d // 8, "readback": round(rb, 3), "query_prec": round(sum(pr) / len(pr), 3)}
    res["dim_sweep_6_fields"] = sweep
    log("  dimension sweep (6 fields, 200 records): " + ", ".join(f"D={d} ({v['bytes']} B): readback {v['readback']}, query {v['query_prec']}" for d, v in sweep.items()))
    log(f"  cost: {res['bytes_per_record']} B/record hypervector vs {res['json_bytes_per_record']} B canonical JSON; query = {n} Hamming compares, no index")
    return res


def selftest():
    c = C.Checks()
    sp = Space(dict(list(FIELDS.items())[:3]), 1024)
    rec = {"rel": "FOLD", "actor": "kimi-k2", "tier": "crew"}
    hv = sp.encode(rec)
    for f in rec:
        c.ok(sp.read(hv, f) == rec[f], f"read back {f}")
    other = sp.encode({"rel": "TASK", "actor": "opus-5.5", "tier": "dispatcher"})
    c.ok(sim(hv, other) < 0.6, "unrelated records ~ orthogonal")
    m = measure(n=80, log=lambda *a: None)
    c.ok(m["readback"][3] == 1.0, "3-field records read back perfectly")
    c.ok(m["query_precision_at_matches"] > 0.5, "partial-record query beats chance")
    return c.report("hdc_records")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    import json
    print("E11 hdc_records")
    res = measure()
    with open(C.HERE + "/results_hdc_records.json", "w") as f:
        json.dump(res, f, indent=1)
