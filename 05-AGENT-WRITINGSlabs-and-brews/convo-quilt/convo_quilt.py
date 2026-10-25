"""convo-quilt — many cheap models talking to and listening to each other; one expensive conductor.

  ModelCell   one cheap model as a quilt cell: visible turns in -> one turn out + budget + receipt
  Quilt       one line of conversation: turns, a mutable who-hears-whom adjacency, per-cell tones,
              checkpoints. The quilt REWINDS; the ledger never does (rewinds are logged events).
  Forest      all branches + the shared hash-chained ledger (quilt-kernel ActiveLog v1).
  score()     cheap per-turn scorer: heuristic always, TypeSafe JEV when keyed.
  digest()    the short text the conductor reads.
  apply()     the conductor's typed moves: checkpoint/rewind/branch/rearrange/tone/zoom/mute/prune.
  auto_moves  a heuristic stand-in conductor for unattended runs.

Offline by default (stub model). `python3 convo_quilt.py --help` for the live loop.
"""
import argparse, copy, json, os, re, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "quilt-kernel"))
sys.path.insert(0, HERE)
import quilt_kernel as K          # fnv1a64 / canon / content_hash / budget / Ledger / activation

OPS = {   # the conductor's whole vocabulary; anything else is refused (typed gating)
    "checkpoint": {"branch", "label"},
    "rewind":     {"branch", "to"},                       # to = checkpoint label | turn id
    "branch":     {"from", "at", "name", "tone", "question", "adj"},
    "rearrange":  {"branch", "adj"},
    "tone":       {"branch", "cell", "text"},
    "zoom":       {"branch", "turn", "name", "cells"},    # a fragment becomes its own question
    "mute":       {"branch", "cell"},
    "prune":      {"branch"},
}
REQ = {"checkpoint": {"branch", "label"}, "rewind": {"branch", "to"}, "branch": {"from", "at", "name"},
       "rearrange": {"branch", "adj"}, "tone": {"branch", "cell", "text"}, "zoom": {"branch", "turn", "name"},
       "mute": {"branch", "cell"}, "prune": {"branch"}}


class Refusal(Exception):
    pass


# ---- model cell ----------------------------------------------------------------------

def stub_caller(provider, model, messages, max_tokens=400, temperature=0.8):
    """Deterministic offline 'model': echoes a hash-derived idea so tests never touch a network."""
    h = K.fnv1a64(model + K.canon(messages))
    words = ["glyph", "luma", "chroma", "edge", "rank", "palette", "dither", "sparse", "router",
             "compactor", "reflex", "cache", "phase", "orientation", "depth", "saliency"]
    pick = [words[(h >> (4 * i)) & 15] for i in range(6)]
    text = "[%s] try %s-%s via %s with %s; test by %s %s." % (model.split("/")[-1], *pick)
    return {"text": text, "tokens": {"in": sum(len(m["content"]) // 4 for m in messages), "out": len(text) // 4},
            "wall_ms": 1, "model": model, "provider": provider}


class ModelCell:
    def __init__(self, name, provider, model, persona, max_tokens=380):
        self.name, self.provider, self.model, self.persona, self.max_tokens = name, provider, model, persona, max_tokens

    def spec(self):
        return {"name": self.name, "provider": self.provider, "model": self.model,
                "persona": self.persona, "max_tokens": self.max_tokens}

    def messages(self, question, visible, tone):
        # Stable prefix first (system + question), then turns in log order: prefix-cache friendly.
        sys_ = ("You are cell '%s' in a conversation quilt of several AI models working one problem.\n"
                "Persona: %s\nRules: one turn, <=170 words. Build on or push against what you heard; name "
                "whose idea you extend (by cell name). Prefer concrete mechanisms, numbers and a falsifiable "
                "test over vibes. No preamble." % (self.name, self.persona))
        if tone:
            sys_ += "\nConductor's tone for you right now: " + tone
        convo = "\n\n".join("[%s | %s]\n%s" % (t["id"], t["cell"], t["text"]) for t in visible) or "(you speak first)"
        return [{"role": "system", "content": sys_},
                {"role": "user", "content": "QUESTION:\n%s\n\nWHAT YOU CAN HEAR:\n%s\n\nYour turn, %s." % (question, convo, self.name)}]


# ---- one line of conversation --------------------------------------------------------

class Quilt:
    def __init__(self, name, question, cells, adj=None, window=6):
        self.name, self.question, self.window = name, question, window
        self.cells = {c.name: c for c in cells}
        self.adj = adj or {c.name: [o.name for o in cells if o.name != c.name] for c in cells}
        self.tones = {c.name: "" for c in cells}
        self.muted = set()
        self.turns = []                 # [{id, cell, text, heard, receipt, score?}]
        self.checkpoints = {}           # label -> snapshot
        self.parent = None              # (branch name, turn id) when forked
        self.alive = True
        self._next = 0

    # state ---------------------------------------------------------------------------
    def snapshot(self):
        return copy.deepcopy({"turns": self.turns, "adj": self.adj, "tones": self.tones,
                              "muted": sorted(self.muted), "next": self._next})

    def restore(self, snap):
        s = copy.deepcopy(snap)
        self.turns, self.adj, self.tones, self.muted = s["turns"], s["adj"], s["tones"], set(s["muted"])
        self._next = max(self._next, s["next"])     # ids stay unique across rewinds: history is never reused

    def state_hash(self):
        return K.content_hash({"q": self.question, "turns": [t["receipt"] for t in self.turns],
                               "adj": self.adj, "tones": self.tones})

    def head_receipt(self):
        return self.turns[-1]["receipt"] if self.turns else "0x" + "0" * 16

    def visible_to(self, cell):
        hears = set(self.adj.get(cell, [])) | {cell}
        vis = [t for t in self.turns if t["cell"] in hears]
        return vis[-self.window:]

    def speakers(self):
        return [c for c in self.cells if c not in self.muted]

    def to_dict(self):
        return {"name": self.name, "question": self.question, "window": self.window,
                "cells": [c.spec() for c in self.cells.values()], "adj": self.adj, "tones": self.tones,
                "muted": sorted(self.muted), "turns": self.turns, "checkpoints": self.checkpoints,
                "parent": self.parent, "alive": self.alive, "next": self._next}

    @classmethod
    def from_dict(cls, d):
        q = cls(d["name"], d["question"], [ModelCell(**c) for c in d["cells"]], d["adj"], d["window"])
        q.tones, q.muted, q.turns = d["tones"], set(d["muted"]), d["turns"]
        q.checkpoints, q.parent, q.alive, q._next = d["checkpoints"], d["parent"], d["alive"], d["next"]
        return q


# ---- the forest: branches + one append-only ledger -----------------------------------

class Forest:
    def __init__(self, caller=stub_caller, ledger_path=None, jev=None, draw=None):
        self.branches = {}
        self.caller, self.jev, self.draw = caller, jev, draw
        self.ledger = K.Ledger(dev="convo-quilt", path=ledger_path)
        self.errors = []
        self._lock = threading.Lock()   # branches may run in parallel; the ledger stays one chain

    def add(self, q):
        if q.name in self.branches:
            raise Refusal("branch %r exists" % q.name)
        self.branches[q.name] = q
        return q

    def _log(self, cell, inp, product, bud):
        ih, ph = K.content_hash(inp), K.content_hash(product)
        with self._lock:
            return self.ledger.emit("cell.tick", {"cell": cell, "input_hash": ih, "product_hash": ph,
                                              "activation": K.activation(cell, ih, ph),
                                              "product": product, "budget": bud})

    def step(self, bname, cell):
        """One cell speaks on one branch. A failed call is logged and skipped, never invented."""
        q = self.branches[bname]
        c = q.cells[cell]
        vis = q.visible_to(cell)
        msgs = c.messages(q.question, vis, q.tones.get(cell, ""))
        try:
            r = self.caller(c.provider, c.model, msgs, max_tokens=c.max_tokens)
        except Exception as e:
            with self._lock:
                self.errors.append({"branch": bname, "cell": cell, "model": c.model, "error": str(e)[:160]})
            self._log("conductor", {"op": "call-failed", "branch": bname, "cell": cell},
                      {"error": str(e)[:160]}, K.budget(reqs="none"))
            return None
        tid = "%s.t%d" % (bname, q._next)
        q._next += 1
        heard = [t["id"] for t in vis]
        receipt = K.content_hash({"prev": q.head_receipt(), "cell": cell, "model": c.model,
                                  "heard": heard, "tone": q.tones.get(cell, ""), "text": r["text"]})
        turn = {"id": tid, "cell": cell, "model": c.model, "text": r["text"], "heard": heard, "receipt": receipt}
        q.turns.append(turn)
        tok = {c.model: r["tokens"]["in"] + r["tokens"]["out"]}
        self._log(cell, {"branch": bname, "heard": heard, "prev": turn["receipt"]},
                  {"turn": tid, "receipt": receipt},
                  K.budget(wall_ms=r["wall_ms"], tokens=tok, reqs=c.provider))
        return turn

    def round(self, bname, order=None):
        q = self.branches[bname]
        return [t for t in (self.step(bname, c) for c in (order or q.speakers())) if t]

    # scoring -------------------------------------------------------------------------
    def score_turns(self, bname, use_jev=True):
        q = self.branches[bname]
        for i, t in enumerate(q.turns):
            if "score" not in t:
                t["score"] = score(t["text"], q.question, [u["text"] for u in q.turns[:i]])
                if use_jev and self.jev:
                    try:
                        t["score"]["jev"] = self.jev(q.question, t["text"])
                        t["score"]["total"] = round(0.5 * t["score"]["total"] + 0.5 * t["score"]["jev"], 3)
                    except Exception as e:
                        t["score"]["jev_error"] = str(e)[:80]
        return q.turns

    # conductor moves (typed) ------------------------------------------------------------
    def apply(self, move):
        if not isinstance(move, dict) or move.get("op") not in OPS:
            raise Refusal("unknown op: %r" % (move.get("op") if isinstance(move, dict) else move))
        op = move["op"]
        extra = set(move) - OPS[op] - {"op", "why"}
        missing = REQ[op] - set(move)
        if extra or missing:
            raise Refusal("%s: extra %s missing %s" % (op, sorted(extra), sorted(missing)))
        b = move.get("branch") or move.get("from")
        if b not in self.branches:
            raise Refusal("no branch %r" % b)
        q = self.branches[b]
        if op == "checkpoint":
            q.checkpoints[move["label"]] = q.snapshot()
        elif op == "rewind":
            to = move["to"]
            if to in q.checkpoints:
                q.restore(q.checkpoints[to])
            else:
                idx = next((i for i, t in enumerate(q.turns) if t["id"] == to), None)
                if idx is None:
                    raise Refusal("rewind target %r not found" % to)
                q.turns = q.turns[:idx + 1]
        elif op == "branch":
            idx = next((i for i, t in enumerate(q.turns) if t["id"] == move["at"]), None)
            if idx is None:
                raise Refusal("branch point %r not found" % move["at"])
            n = Quilt(move["name"], move.get("question", q.question),
                      [ModelCell(**c.spec()) for c in q.cells.values()], copy.deepcopy(move.get("adj", q.adj)), q.window)
            n.turns = copy.deepcopy(q.turns[:idx + 1])      # copies the moment; main line untouched
            n.tones = dict(q.tones)
            if move.get("tone"):
                n.tones = {c: move["tone"] for c in n.cells}
            n.parent, n._next = [b, move["at"]], q._next
            self.add(n)
        elif op == "rearrange":
            self._check_adj(q, move["adj"])
            q.adj = copy.deepcopy(move["adj"])
        elif op == "tone":
            if move["cell"] not in q.cells and move["cell"] != "*":
                raise Refusal("no cell %r" % move["cell"])
            for c in (q.cells if move["cell"] == "*" else [move["cell"]]):
                q.tones[c] = move["text"]
        elif op == "zoom":
            t = next((t for t in q.turns if t["id"] == move["turn"]), None)
            if t is None:
                raise Refusal("zoom target %r not found" % move["turn"])
            keep = move.get("cells") or list(q.cells)
            if not isinstance(keep, list) or set(keep) - set(q.cells):
                raise Refusal("zoom cells must come from branch %r: %s" % (b, sorted(q.cells)))
            cells = [ModelCell(**q.cells[c].spec()) for c in keep]
            n = Quilt(move["name"], "Go one level deeper on this single fragment; make it buildable.\n"
                      "PARENT QUESTION: %s\nFRAGMENT (%s, %s): %s" % (q.question, t["id"], t["cell"], t["text"]),
                      cells, None, q.window)
            n.parent, n._next = [b, t["id"]], 0
            self.add(n)
        elif op == "mute":
            q.muted.add(move["cell"])
        elif op == "prune":
            q.alive = False
        self._log("conductor", {"move": move}, {"branch": b, "state": q.state_hash()}, K.budget(reqs="conductor"))
        return True

    @staticmethod
    def _check_adj(q, adj):
        if not isinstance(adj, dict) or set(adj) - set(q.cells):
            raise Refusal("adj keys must be cells")
        for k, v in adj.items():
            if not isinstance(v, list) or set(v) - set(q.cells):
                raise Refusal("adj[%s] names unknown cells" % k)

    # persistence -----------------------------------------------------------------------
    def save(self, path):
        with open(path, "w") as f:
            json.dump({"branches": {k: v.to_dict() for k, v in self.branches.items()}, "errors": self.errors}, f, indent=1)

    def load_state(self, path):
        d = json.load(open(path))
        self.branches = {k: Quilt.from_dict(v) for k, v in d["branches"].items()}
        self.errors = d.get("errors", [])


# ---- cheap scorer --------------------------------------------------------------------

_W = re.compile(r"[a-z][a-z0-9\-]{2,}")
STOP = set("the and for that this with you are from but not can have will our its into more than then they what "
           "which when your their them also just like each over only such some very would could should about".split())


def _words(s):
    return {w for w in _W.findall(s.lower()) if w not in STOP}


def score(text, question, prior):
    """Heuristic ideation head-space in [0,1] + a derailment flag. Cheap, deterministic, honest about
    being a heuristic: novelty vs everything said before, anchoring to the question, concreteness."""
    w, qw = _words(text), _words(question)
    nov = 1.0 - max([len(w & _words(p)) / max(1, len(w | _words(p))) for p in prior] or [0.0])
    anchor = min(1.0, len(w & qw) / max(1.0, 0.12 * len(qw)))
    concrete = min(1.0, (len(re.findall(r"\d", text)) / 6 + len(re.findall(r"\b(test|measure|metric|if|then|"
                                                                            r"ablat\w*|baseline|predict\w*|falsif\w*)\b", text.lower())) / 4) / 2)
    derail = anchor < 0.25 or nov < 0.15 or len(text) < 40
    total = round(0.4 * nov + 0.3 * anchor + 0.3 * concrete - (0.3 if derail else 0), 3)
    return {"novelty": round(nov, 3), "anchor": round(anchor, 3), "concrete": round(concrete, 3),
            "derail": derail, "total": total}


def jev_scorer(question, text):
    """TypeSafe JEV 'generativity' score mapped to [0,1]."""
    import providers as P
    d = P.jev("QUESTION: %s\nTURN: %s" % (question[:300], text[:650]),
              {"ideation": {"type": "score", "instructions": "How generative and on-question is TURN "
                            "(concrete, new, testable mechanism for QUESTION)?",
                            "criteria": ["derailed", "flat", "useful", "generative", "breakthrough"]}})
    return round(d["answers"]["ideation"]["score"] / 4.0, 3)


# ---- digest + the stand-in conductor -------------------------------------------------

def digest(forest, top=4, clip=220):
    out = []
    for b, q in forest.branches.items():
        if not q.alive:
            continue
        sc = [t for t in q.turns if "score" in t]
        best = sorted(sc, key=lambda t: -t["score"]["total"])[:top]
        der = [t["id"] for t in sc[-6:] if t["score"]["derail"]]
        out.append("## branch %s (parent %s) turns=%d state=%s\nadj=%s\ntones=%s\nmuted=%s\nrecent derails=%s\n"
                   "checkpoints=%s" % (b, q.parent, len(q.turns), q.state_hash(), json.dumps(q.adj),
                                       json.dumps({k: v[:60] for k, v in q.tones.items() if v}), sorted(q.muted),
                                       der, list(q.checkpoints)))
        for t in best:
            out.append("  * %s %s (%.2f): %s" % (t["id"], t["cell"], t["score"]["total"], t["text"][:clip].replace("\n", " ")))
    if forest.errors:
        out.append("errors: %d (last: %s)" % (len(forest.errors), forest.errors[-1]))
    return "\n".join(out)


def auto_moves(forest, bname, tick, branch_at=0.62):
    """Heuristic stand-in for the expensive conductor: checkpoint, rewind a derail streak, mute a
    cell that came back empty twice, fork a peak.
    Moth (when wired) breaks ties among equally good fork points."""
    q = forest.branches[bname]
    moves = [{"op": "checkpoint", "branch": bname, "label": "cp%d" % tick}]
    last = [t for t in q.turns[-3:] if "score" in t]
    if len(last) == 3 and all(t["score"]["derail"] for t in last) and len(q.checkpoints) > 0:
        moves = [{"op": "rewind", "branch": bname, "to": list(q.checkpoints)[-1]},
                 {"op": "tone", "branch": bname, "cell": "*", "text": "Return to the QUESTION; one concrete mechanism."}]
    # reflex metabolized from the meta-quilt run (runs/meta): a cell that came back empty twice on this
    # branch is a capacity failure (reasoning model out of budget), not a content signal -> mute it.
    empties = {}
    for e in forest.errors:
        if e["branch"] == bname and "empty content" in e["error"]:
            empties[e["cell"]] = empties.get(e["cell"], 0) + 1
    moves += [{"op": "mute", "branch": bname, "cell": c} for c, n in sorted(empties.items())
              if n >= 2 and c not in q.muted]
    peaks = [t for t in q.turns if "score" in t and t["score"]["total"] >= branch_at
             and not any(b.parent == [bname, t["id"]] for b in forest.branches.values())]
    if peaks and len(forest.branches) < 6:
        top = max(p["score"]["total"] for p in peaks)
        tied = [p for p in peaks if p["score"]["total"] >= top - 0.03]
        i = forest.draw(len(tied)) if forest.draw else 0
        moves.append({"op": "branch", "from": bname, "at": tied[i]["id"], "name": "%s-b%d" % (bname, tick),
                      "tone": "Take %s's idea somewhere the main line is not going." % tied[i]["cell"]})
    return moves


# ---- CLI -----------------------------------------------------------------------------

ROSTER = [   # (name, provider, model, persona) — from probe.json's working set
    ("hy3", "deepinfra", "tencent/Hy3", "systems engineer; wants the smallest mechanism that could work"),
    ("inkling", "deepinfra", "thinkingmachines/Inkling-Small", "perception scientist; thinks in human vision"),
    ("nemo", "deepinfra", "nvidia/NVIDIA-Nemotron-3.5-Lightning", "skeptic; names the failure mode and the baseline"),
    ("ling", "deepinfra", "inclusionAI/Ling-3.0-flash", "information theorist; counts bits per glyph"),
    ("qwen", "deepinfra", "Qwen/Qwen3.8-Flash", "wild-card inventor; proposes the strange option"),
    ("mimo", "deepinfra", "XiaomiMiMo/MiMo-V2.6-Pro", "integrator; composes existing primitives instead of new ones"),
    ("dsv4", "deepinfra", "deepseek-ai/DeepSeek-V4-Flash", "experimentalist; turns ideas into a 1-day test"),
    ("glm", "zai-coding", "glm-5.3", "architect; maps ideas onto the Quilt cell/witness model"),
]


def live_caller(retries=1):
    import providers as P

    def call(provider, model, messages, max_tokens=400, temperature=0.8):
        err = None
        for _ in range(retries + 1):
            try:
                return P.chat(provider, model, messages, max_tokens=max_tokens, temperature=temperature)
            except P.ProviderError as e:
                err = e
                if "empty content" in str(e):
                    max_tokens *= 3        # reasoning model: give it room once
                time.sleep(1)
        raise err
    return call


def moth_draw_or_none():
    import providers as P

    def draw(k):
        try:
            return P.moth_draw(k)[0]
        except P.ProviderError:
            return 0
    return draw


def main(argv=None):
    ap = argparse.ArgumentParser(description="conductor-over-cheap-model conversation quilt")
    ap.add_argument("--out", default=os.path.join(HERE, "runs", "demo"))
    ap.add_argument("--question", default="")
    ap.add_argument("--play", action="store_true", help="live models (else offline stub)")
    ap.add_argument("--rounds", type=int, default=2, help="rounds per active branch before pausing")
    ap.add_argument("--resume", action="store_true", help="load <out>/state.json")
    ap.add_argument("--moves", default="", help="conductor moves JSON file to apply before playing")
    ap.add_argument("--auto", action="store_true", help="apply heuristic auto_moves at the pause")
    ap.add_argument("--cells", default="", help="comma list of roster names (default all)")
    ap.add_argument("--no-jev", action="store_true")
    ap.add_argument("--parallel", type=int, default=4, help="branches played concurrently (1 = sequential)")
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    live = a.play
    f = Forest(caller=live_caller() if live else stub_caller, ledger_path=os.path.join(a.out, "ledger.jsonl"),
               jev=(jev_scorer if live and not a.no_jev and os.environ.get("TYPESAFEAI_KEY") else None),
               draw=moth_draw_or_none() if live else None)
    lp = os.path.join(a.out, "ledger.jsonl")
    if a.resume:
        f.load_state(os.path.join(a.out, "state.json"))
        if os.path.exists(lp):
            f.ledger = K.Ledger.load(open(lp).read(), dev="convo-quilt", path=lp)
    else:
        if os.path.exists(lp):
            os.remove(lp)
        want = a.cells.split(",") if a.cells else [r[0] for r in ROSTER]
        f.add(Quilt("main", a.question or "What is the next step?", [ModelCell(*r) for r in ROSTER if r[0] in want]))
    if a.moves:
        for m in json.load(open(a.moves)):
            try:
                f.apply(m)
                print("applied", m["op"], m.get("name") or m.get("branch"))
            except Refusal as e:
                print("REFUSED", e)
    alive = [b for b, q in f.branches.items() if q.alive]

    def play(b):
        for _ in range(a.rounds):
            f.round(b)
        f.score_turns(b)
    with ThreadPoolExecutor(max(1, a.parallel)) as ex:
        list(ex.map(play, alive))
    for b in alive:
        if a.auto:
            for m in auto_moves(f, b, len(f.ledger.records)):
                f.apply(m)
    f.save(os.path.join(a.out, "state.json"))
    d = digest(f)
    open(os.path.join(a.out, "digest.md"), "w").write(d + "\n")
    v = f.ledger.verify()
    print(d)
    print("\nledger: %d records, intact=%s, spend=%s" % (len(f.ledger.records), v["intact"],
                                                           json.dumps(f.ledger.total()["tokens"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
