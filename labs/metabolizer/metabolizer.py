"""metabolizer — grow -> freeze -> patch-in -> refine -> re-freeze.

A VERIFIED capability becomes a reusable, routable EXPERT PATCH (a patch is a cell). A frozen
patch carries three things:

  GATE     probes that can say "no": a domain probe plus invariance probes seeded from
           invariance-miner's derived invariants (f(t(x)) == f(x)). A gate that cannot decline
           is refused at freeze time.
  TIER     the budget vector (quilt-kernel `budget`) so a router can compare cost.
  WITNESS  priced-training's RouteWitness over "live capability == frozen snapshot" audits. The
           version-claim holds only while the e-process stays above 1/delta; when the capability
           drifts it RETRACTS, the patch refuses to serve, and it must re-freeze.

COMPOSITION is routing. Members that reach a product the Differ certifies identical -> the cheaper
wins (quilt-kernel `price`, B4). Members that DISAGREE -> the resolution is frozen as a BLEND patch
(itself gated, tiered, witnessed, re-freezable). The router is itself a patch.

Dependency-light: stdlib + the four sibling labs. Importable:  import metabolizer as M
"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LABS = os.path.dirname(HERE)
for _d in ("quilt-kernel", "invariance-miner", "priced-training", "route-preference"):
    sys.path.insert(0, os.path.join(LABS, _d))

import quilt_kernel as K  # noqa: E402
import invariance_miner as IM  # noqa: E402
import route_witness as RW  # noqa: E402

Refusal = K.Refusal
P0, DELTA = 0.2, 0.05           # version-claim: "live-vs-frozen miss rate < 0.2", false-witness <= 5%
MAX_LEN_SLACK = 2


def _hash(x):
    return K.content_hash(x)


def tier_name(tier):
    ax = K.axes_of(tier)
    if ax["usd"] >= 0.001:
        return "premium"
    return "metered" if (ax["usd"] > 0 or ax["tokens"] > 0) else "free"


def cost_key(tier):
    ax = K.axes_of(tier)
    return (ax["usd"], ax["tokens"], ax["storage_bytes"], ax["wall_ms"])


# ---- capability -------------------------------------------------------------------------------

class Capability:
    """A mutable, pure function plus its declared per-call cost. `fn` may change (drift)."""

    def __init__(self, name, fn, cost):
        self.name, self.fn, self.cost = name, fn, cost


def _safe(fn, x):
    try:
        return fn(x)
    except Exception as e:                       # an error is a product too
        return "ERR:%s" % type(e).__name__


# ---- grow -------------------------------------------------------------------------------------

def grow(cap, inputs, transforms, min_support=3):
    """Run the capability over `inputs`, mine invariants from the log (zero extra calls)."""
    inputs = list(inputs)
    if not inputs:
        raise Refusal("grow needs inputs")
    types = {type(x).__name__ for x in inputs}
    if len(types) != 1:
        raise Refusal("mixed input types %s" % sorted(types))
    log = [(x, IM.digest(_safe(cap.fn, x))) for x in inputs]
    mined = IM.mine(log, transforms, min_support)
    dom = {"kind": "domain", "type": types.pop()}
    if dom["type"] == "str":
        dom["max_len"] = max(len(x) for x in inputs) * MAX_LEN_SLACK
    return {"inputs": inputs, "log": log, "mined": mined, "domain": dom,
            "accepted": sorted(n for n, m in mined.items() if m["accepted"]),
            "refuted": sorted(n for n, m in mined.items() if m["refuted"])}


# ---- gate -------------------------------------------------------------------------------------

def _probe(spec, transforms):
    """-> predicate (x, fn) -> (ok, reason)."""
    if spec["kind"] == "domain":
        def dom(x, fn):
            if type(x).__name__ != spec["type"]:
                return False, "type %s != %s" % (type(x).__name__, spec["type"])
            if spec["type"] == "str" and not 1 <= len(x) <= spec["max_len"]:
                return False, "length outside 1..%d" % spec["max_len"]
            return True, ""
        return dom
    if spec["kind"] == "invariant":
        t = transforms[spec["t"]]

        def inv(x, fn):
            try:
                tx = t(x)
            except Exception:
                return False, "transform %s failed" % spec["t"]
            ok = _hash(_safe(fn, tx)) == _hash(_safe(fn, x))
            return ok, "" if ok else "f(%s(x)) != f(x)" % spec["t"]
        return inv
    raise Refusal("unknown probe kind %r" % spec["kind"])


class Gate:
    """Ordered probes; the first "no" declines. `parents` (blend/router) are consulted too."""

    def __init__(self, specs, transforms, parents=(), any_parent=False):
        self.specs, self.transforms = list(specs), transforms
        self.parents, self.any_parent = list(parents), any_parent
        self._fns = [(s, _probe(s, transforms)) for s in self.specs]

    def check(self, x, fn):
        for s, p in self._fns:
            ok, why = p(x, fn)
            if not ok:
                return False, (s["kind"] if s["kind"] == "domain" else "invariant:" + s["t"]), why
        if self.parents:
            res = [m.gate.check(x, m.frozen_fn) for m in self.parents]
            if self.any_parent:
                if not any(r[0] for r in res):
                    return (False,) + res[0][1:]
            else:
                for r in res:
                    if not r[0]:
                        return r
        return True, "", ""

    def spec(self):
        return {"probes": self.specs, "parents": [m.name for m in self.parents],
                "mode": "any" if self.any_parent else "all"}


def _require_declinable(gate, fn, sample_inputs):
    """A patch that can never decline is not trustworthy: probe it with canary negatives."""
    str_dom = next((s for s in gate.specs if s["kind"] == "domain" and s["type"] == "str"), None)
    negatives = [object()]
    if str_dom:
        negatives += ["", "x" * (str_dom["max_len"] + 1)]
    declined = [n for n in negatives if not gate.check(n, fn)[0]]
    if not declined and gate.parents:
        declined = [n for n in negatives if not gate.check(n, fn)[0]]
    if not declined:
        raise Refusal("gate cannot decline: a patch that never says no is not trustworthy")
    return len(declined)


# ---- patch ------------------------------------------------------------------------------------

class Patch:
    """A frozen expert patch (a cell): gate + tier + version-witness around a frozen function."""

    def __init__(self, name, kind, cap, transforms, ledger, grow_inputs, p0=P0, delta=DELTA, members=()):
        self.name, self.kind, self.cap, self.transforms = name, kind, cap, transforms
        self.ledger, self.grow_inputs, self.p0, self.delta = ledger, list(grow_inputs), p0, delta
        self.members, self.version = list(members), 0
        self.frozen_fn = self.gate = self.tier = self.witness = self.growth = None
        self._retracted_flag = None            # set only on snapshots
        self._retract_logged = False

    # -- freeze (also re-freeze: refine = re-mine on the live capability) --
    def freeze(self):
        g = grow(self.cap, self.grow_inputs, self.transforms)
        fn = self.cap.fn                                     # snapshot: later drift cannot touch it
        specs = [g["domain"]]
        dropped = []
        for n in g["accepted"]:                              # keep a probe only if it accepts its own training set
            spec = {"kind": "invariant", "t": n}
            ok = all(_probe(spec, self.transforms)(x, fn)[0] for x in g["inputs"])
            (specs if ok else dropped).append(spec if ok else n)
        parents = self.members if self.kind in ("blend", "router") else ()
        gate = Gate(specs, self.transforms, parents, any_parent=(self.kind == "router"))
        n_declined = _require_declinable(gate, fn, g["inputs"])
        w = RW.RouteWitness(self.p0, self.delta)
        need = RW.clean_needed(self.p0, self.delta)
        if len(g["inputs"]) < need:
            raise Refusal("%d grown inputs < %d clean audits needed to witness the claim" % (len(g["inputs"]), need))
        for x in g["inputs"][:need]:                         # determinism audit: f(x) twice must agree
            w.observe(0.0 if K.diff(_safe(fn, x), _safe(fn, x))["identical"] else 1.0)
        if w.state != "WITNESSED":
            raise Refusal("capability is not deterministic; cannot freeze")
        self.frozen_fn, self.gate, self.witness, self.growth = fn, gate, w, g
        self.dropped_probes = dropped
        self.tier = self.cap.cost
        self.version += 1
        self._retract_logged = False
        self._cell = K.Cell(self.frozen_fn, "%s@v%d" % (self.name, self.version), self.ledger,
                            cost=lambda out, *a, **k: dict(wall_ms=self.tier["wall_ms"], usd=self.tier["usd"],
                                                           tokens=self.tier["tokens"]),
                            keep=("input", "product"))
        self.ledger.emit("ledger.transaction", {"event": "freeze", "patch": self.name, "kind": self.kind,
                                                "version": self.version, "frozen_hash": self.frozen_hash(),
                                                "probes": [s["t"] if s["kind"] == "invariant" else "domain" for s in specs],
                                                "dropped": dropped, "declines_canaries": n_declined})
        return self

    refreeze = freeze

    def behavior_hash(self):
        return _hash([IM.digest(_safe(self.frozen_fn, x)) for x in self.grow_inputs])

    def frozen_hash(self):
        return _hash({"patch": self.name, "kind": self.kind, "version": self.version, "gate": self.gate.spec(),
                      "tier": self.tier, "behavior": self.behavior_hash(),
                      "claim": {"p0": self.p0, "delta": self.delta}})

    def spec(self):
        return {"patch": self.name, "kind": self.kind, "version": self.version, "gate": self.gate.spec(),
                "tier": self.tier, "tier_name": tier_name(self.tier), "witness": self.witness.summary(),
                "members": [m.name + "@v%d" % m.version for m in self.members],
                "behavior_hash": self.behavior_hash(), "frozen_hash": self.frozen_hash()}

    # -- the version-witness --
    @property
    def state(self):
        return "RETRACTED" if self._retracted_flag else (
            "WITNESSED" if self._retracted_flag is False else self.witness.state)

    def audit(self, inputs):
        """Compare the LIVE capability to the frozen snapshot; feed the e-process. -> state."""
        for x in inputs:
            same = K.diff(_safe(self.frozen_fn, x), _safe(self.cap.fn, x))["identical"]
            self.witness.observe(0.0 if same else 1.0)
            if self.witness.state == "RETRACTED" and not self._retract_logged:
                self._retract_logged = True
                self.ledger.emit("ledger.transaction", {"event": "retract", "patch": self.name,
                                                        "version": self.version, "t": self.witness.t,
                                                        "misses": self.witness.misses})
        return self.state

    # -- serving --
    def serve(self, x):
        if self.state != "WITNESSED":
            return {"status": "retracted", "patch": self.name, "version": self.version}
        ok, probe, why = self.gate.check(x, self.frozen_fn)
        if not ok:
            return {"status": "declined", "patch": self.name, "probe": probe, "why": why}
        out = self._cell(x)
        return {"status": "ok", "patch": self.name, "version": self.version, "product": out,
                "receipt": self._cell.last}

    def snapshot(self):
        """A status-frozen copy (serves from the frozen function with its current retraction flag)."""
        s = Patch.__new__(Patch)
        s.__dict__.update(self.__dict__)
        s._retracted_flag = self.state != "WITNESSED"
        s.ledger = K.Ledger(dev="snapshot")
        s._cell = K.Cell(self.frozen_fn, "%s@v%d" % (self.name, self.version), s.ledger, cost=self._cell.cost,
                         keep=("input", "product"))
        return s


def freeze(cap, inputs, transforms, ledger, p0=P0, delta=DELTA, name=None):
    """grow -> freeze a leaf capability into a Patch (raises Refusal if it cannot be trusted)."""
    return Patch(name or cap.name, "leaf", cap, transforms, ledger, inputs, p0, delta).freeze()


# ---- composition: blend -----------------------------------------------------------------------

class BlendCapability:
    """Resolution over members' LIVE capabilities. Agree -> that product. Disagree -> the frozen
    table decides per case, else the default member."""

    def __init__(self, members, table, default):
        self.members, self.table, self.default = members, table, default
        self.name = "blend(%s)" % "+".join(sorted(m.name for m in members))
        c = members[0].tier
        for m in members[1:]:
            c = K.add_budget(c, m.tier)                       # a blend runs every member
        self.cost = c

    @property
    def fn(self):
        fns = {m.name: m.cap.fn for m in self.members}        # snapshot of live fns at access time
        table, default = self.table, self.default

        def resolve(x):
            outs = {n: f(x) for n, f in fns.items()}
            if len({K.canon(o) for o in outs.values()}) == 1:
                return outs[default]
            return outs[table.get(K.canon(x), default)]
        return resolve


def gate_cases(cases, members):
    """Cheap models propose referee cases; only those whose expected product equals a member's
    product survive (a cell decides, the crew does not)."""
    kept = []
    for c in cases:
        if not isinstance(c, dict) or "input" not in c or "expected" not in c:
            continue
        x = c["input"]
        outs = {m.name: _safe(m.frozen_fn, x) for m in members}
        hit = sorted(n for n, o in outs.items() if K.canon(o) == K.canon(c["expected"]))
        if hit and len(set(K.canon(o) for o in outs.values())) > 1:    # informative: members disagree here
            kept.append({"input": x, "expected": c["expected"], "winners": hit})
    return kept


def resolve_blend(members, cases, ledger, inputs=None, transforms=None):
    """Freeze the disagreement resolution as a BLEND patch. Raises Refusal without evidence."""
    members = sorted(members, key=lambda m: m.name)
    kept = gate_cases(cases, members)
    if not kept:
        raise Refusal("no valid referee case: cannot freeze a resolution without evidence")
    wins = {m.name: 0 for m in members}
    table = {}
    for c in kept:
        if len(c["winners"]) == 1:
            table[K.canon(c["input"])] = c["winners"][0]
        for n in c["winners"]:
            wins[n] += 1
    default = sorted(members, key=lambda m: (-wins[m.name], cost_key(m.tier), m.name))[0].name
    cap = BlendCapability(members, table, default)
    ins = list(inputs) if inputs is not None else [x for m in members for x in m.grow_inputs]
    ins = list(dict.fromkeys(ins + [c["input"] for c in kept]))
    tr = transforms or members[0].transforms
    b = Patch(cap.name, "blend", cap, tr, ledger, ins, members[0].p0, members[0].delta, members=members).freeze()
    b.table, b.default, b.cases = table, default, kept
    ledger.emit("ledger.transaction", {"event": "blend", "patch": b.name, "members": [m.name for m in members],
                                       "default": default, "table_size": len(table), "cases": len(kept)})
    return b


# ---- composition: router (itself a patch) -----------------------------------------------------

def route(views, x, blender):
    """Gate each member, then: identical products -> cheaper (B4); disagree -> frozen blend."""
    served = [(v, v.serve(x)) for v in views]
    ok = [(v, r) for v, r in served if r["status"] == "ok"]
    if not ok:
        return {"status": "declined", "via": None, "reasons": {v.name: r.get("probe", r["status"]) for v, r in served}}
    if len(ok) == 1:
        return {"status": "ok", "via": ok[0][0].name, "product": ok[0][1]["product"], "how": "sole"}
    res = K.price({r["receipt"]["cell"]: r["receipt"] for _, r in ok})
    if res["status"] == "certified":
        pick = K.which(res, "cheap")
        r = next(r for v, r in ok if r["receipt"]["cell"] == pick)
        return {"status": "ok", "via": pick.split("@")[0], "product": r["product"], "how": "cheaper",
                "price": res, "candidates": sorted(r["receipt"]["cell"] for _, r in ok)}
    b = blender([v for v, _ in ok])
    if b is None:
        return {"status": "unresolved", "via": None, "reason": res["reason"]}
    r = b.serve(x)
    if r["status"] != "ok":
        return {"status": r["status"], "via": b.name}
    return {"status": "ok", "via": b.name, "product": r["product"], "how": "blend"}


class RouterCapability:
    def __init__(self, members, referee_cases, ledger, name="router"):
        self.members, self.referee_cases, self.ledger, self.name = list(members), list(referee_cases), ledger, name
        self.blends = {}
        c = members[0].tier
        for m in members[1:]:
            c = K.add_budget(c, m.tier)                       # certifying identity runs every candidate
        self.cost = c

    def blender(self, views):
        names = {v.name for v in views}
        real = sorted((m for m in self.members if m.name in names), key=lambda m: m.name)
        key = tuple((m.name, m.version) for m in real)
        if key not in self.blends:
            try:
                self.blends[key] = resolve_blend(real, self.referee_cases, self.ledger)
            except Refusal:
                self.blends[key] = None
        return self.blends[key]

    @property
    def fn(self):
        views = [m.snapshot() for m in self.members]
        by_name = {m.name: m for m in views}

        def routed(x):
            r = route(views, x, lambda vs: self.blender(vs))
            return r["product"] if r["status"] == "ok" else "DECLINED:" + r["status"]
        return routed


def make_router(members, referee_cases, ledger, name="router", inputs=None):
    cap = RouterCapability(members, referee_cases, ledger, name)
    ins = list(inputs) if inputs is not None else list(dict.fromkeys(x for m in members for x in m.grow_inputs))
    p = Patch(name, "router", cap, members[0].transforms, ledger, ins, members[0].p0, members[0].delta,
              members=members).freeze()
    p.route = lambda x: route([m.snapshot() for m in cap.members], x, cap.blender)
    p.capability = cap
    return p


# ---- crew gate --------------------------------------------------------------------------------

def gate_crew(obj):
    """Filter UNTRUSTED crew proposals into usable fixture inputs (strings only, bounded, deduped)."""
    def clean(xs, need=None, allow_tab=False):
        out = []
        for x in xs if isinstance(xs, list) else []:
            if not isinstance(x, str) or not 1 <= len(x) <= 40:
                continue
            if any(ord(c) < 32 and not (allow_tab and c == "\t") for c in x) or not x.isascii():
                continue
            if need and need not in x:
                continue
            if x not in out:
                out.append(x)
        return out
    obj = obj if isinstance(obj, dict) else {}
    return {"inputs": clean(obj.get("inputs")),
            "tab_inputs": clean(obj.get("tab_inputs"), "\t", True),
            "blend_inputs": clean([c.get("input") for c in obj.get("blend_cases", []) if isinstance(c, dict)], "&")}
