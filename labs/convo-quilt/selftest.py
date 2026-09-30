"""convo-quilt selftest — offline, deterministic, no keys. Run: python3 selftest.py"""
import copy, json, os, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import convo_quilt as C
K = C.K

checks = fails = 0


def check(name, ok):
    global checks, fails
    checks += 1
    fails += 0 if ok else 1
    if not ok:
        print("  FAIL:", name)


def refused(f, m):
    try:
        f.apply(m)
    except C.Refusal:
        return True
    return False


def forest(n=4, caller=C.stub_caller):
    f = C.Forest(caller=caller)
    f.add(C.Quilt("main", "What projection breaks the rank-one luma ceiling?",
                  [C.ModelCell(*r) for r in C.ROSTER[:n]]))
    return f


# 1. kernel idioms are the fleet's
check("fnv1a-64 canary", K.canary())

# 2. a round: every cell speaks once, receipts chain, ledger intact
f = forest()
ts = f.round("main")
q = f.branches["main"]
check("round: 4 turns", len(ts) == 4 and [t["cell"] for t in ts] == [r[0] for r in C.ROSTER[:4]])
check("turn ids unique", len({t["id"] for t in q.turns}) == 4)
check("first cell heard nothing", ts[0]["heard"] == [])
check("second cell heard the first", ts[1]["heard"] == [ts[0]["id"]])
check("ledger intact", f.ledger.verify()["intact"])
check("ledger has 4 cell.ticks with budgets", len(f.ledger.receipts()) == 4
      and all(K.budget_ok(r["budget"]) for r in f.ledger.receipts()))
check("spend is summed per model", sum(f.ledger.total()["tokens"].values()) > 0)

# 3. determinism: same inputs -> same state hash
g = forest(); g.round("main")
check("replay: identical state hash", g.branches["main"].state_hash() == q.state_hash())

# 4. receipts are content-bound: editing a turn's text breaks its receipt
t = q.turns[1]
recompute = K.content_hash({"prev": q.turns[0]["receipt"], "cell": t["cell"], "model": t["model"],
                            "heard": t["heard"], "tone": "", "text": t["text"]})
check("receipt recomputes", recompute == t["receipt"])
check("tampered text changes receipt", K.content_hash({"prev": q.turns[0]["receipt"], "cell": t["cell"],
      "model": t["model"], "heard": t["heard"], "tone": "", "text": t["text"] + "!"}) != t["receipt"])

# 5. adjacency governs hearing
f.apply({"op": "rearrange", "branch": "main", "adj": {"hy3": [], "inkling": ["hy3"], "nemo": ["nemo"], "ling": ["inkling", "nemo"]}})
t5 = f.step("main", "hy3")
check("rearrange: hy3 hears only itself", all(h.split(".")[-1] and q.turns[[x["id"] for x in q.turns].index(h)]["cell"] == "hy3"
                                              for h in t5["heard"]))
t6 = f.step("main", "ling")
check("ling hears inkling/nemo/self only", {x["cell"] for x in q.turns if x["id"] in t6["heard"]} <= {"inkling", "nemo", "ling"})
check("bad adj refused", refused(f, {"op": "rearrange", "branch": "main", "adj": {"hy3": ["ghost"]}}))

# 6. window bounds context
q.window = 2
check("window caps visible turns", len(q.visible_to("ling")) <= 2)
q.window = 6

# 7. checkpoint + rewind restores turns, adjacency and tones exactly
f.apply({"op": "checkpoint", "branch": "main", "label": "cp-a"})
h_cp, n_cp, adj_cp = q.state_hash(), len(q.turns), copy.deepcopy(q.adj)
f.apply({"op": "tone", "branch": "main", "cell": "*", "text": "be reckless"})
f.apply({"op": "rearrange", "branch": "main", "adj": {"hy3": ["inkling"], "inkling": [], "nemo": [], "ling": []}})
f.round("main")
check("state moved after checkpoint", q.state_hash() != h_cp and len(q.turns) == n_cp + 4)
f.apply({"op": "rewind", "branch": "main", "to": "cp-a"})
check("rewind restores state hash", q.state_hash() == h_cp)
check("rewind restores adj", q.adj == adj_cp)
check("rewind restores tones", all(v == "" for v in q.tones.values()))
check("ledger never rewinds (still intact, grew)", f.ledger.verify()["intact"] and len(f.ledger.records) > 10)
nid = f.round("main")[0]["id"]
check("ids after rewind do not collide with history", nid not in {r["body"]["product"].get("turn") for r in f.ledger.records[:-4]})

# 8. rewind to a turn id truncates
first = q.turns[0]["id"]
f.apply({"op": "checkpoint", "branch": "main", "label": "cp-b"})
f.apply({"op": "rewind", "branch": "main", "to": first})
check("rewind to turn id", len(q.turns) == 1 and q.turns[0]["id"] == first)
f.apply({"op": "rewind", "branch": "main", "to": "cp-b"})
check("rewind forward to later checkpoint", len(q.turns) > 1)

# 9. branch copies the moment and does not derail main
main_hash = q.state_hash()
at = q.turns[2]["id"]
f.apply({"op": "branch", "from": "main", "at": at, "name": "alt", "tone": "invert the premise"})
b = f.branches["alt"]
check("branch prefix equals main up to fork", [t["receipt"] for t in b.turns] == [t["receipt"] for t in q.turns[:3]])
check("branch carries its tone", set(b.tones.values()) == {"invert the premise"})
check("branch parent recorded", b.parent == ["main", at])
f.round("alt")
check("branch growth leaves main untouched", q.state_hash() == main_hash)
check("branch receipts chain from fork head", b.turns[3]["receipt"] != q.turns[3]["receipt"] if len(q.turns) > 3 else True)
check("duplicate branch refused", refused(f, {"op": "branch", "from": "main", "at": at, "name": "alt"}))

# 10. zoom: a fragment becomes its own quilt with fewer cells
f.apply({"op": "zoom", "branch": "main", "turn": at, "name": "z1", "cells": ["hy3", "nemo"]})
z = f.branches["z1"]
check("zoom question embeds fragment", q.turns[2]["text"][:30] in z.question)
check("zoom has only chosen cells", sorted(z.cells) == ["hy3", "nemo"])
check("zoom starts empty", z.turns == [] and len(f.round("z1")) == 2)

# 11. mute + prune
f.apply({"op": "mute", "branch": "main", "cell": "nemo"})
check("muted cell does not speak", "nemo" not in [t["cell"] for t in f.round("main")])
f.apply({"op": "prune", "branch": "z1"})
check("pruned branch leaves digest", "branch z1" not in (f.score_turns("main"), C.digest(f))[1])

# 12. typed gating on moves
check("unknown op refused", refused(f, {"op": "delete-everything", "branch": "main"}))
check("extra field refused", refused(f, {"op": "tone", "branch": "main", "cell": "hy3", "text": "x", "sudo": True}))
check("missing field refused", refused(f, {"op": "rewind", "branch": "main"}))
check("unknown branch refused", refused(f, {"op": "prune", "branch": "nope"}))
check("unknown rewind target refused", refused(f, {"op": "rewind", "branch": "main", "to": "cp-zzz"}))
check("unknown tone cell refused", refused(f, {"op": "tone", "branch": "main", "cell": "ghost", "text": "x"}))

# 13. failed model call is logged, not invented
def flaky(provider, model, messages, **kw):
    if "Inkling" in model:
        raise RuntimeError("HTTP 404")
    return C.stub_caller(provider, model, messages, **kw)
h = forest(caller=flaky)
out = h.round("main")
check("failed cell skipped", len(out) == 3 and "inkling" not in [t["cell"] for t in out])
check("failure recorded", h.errors and h.errors[0]["cell"] == "inkling")
check("ledger still intact after failure", h.ledger.verify()["intact"])

# 14. scorer: novelty, anchoring, derailment
qq = "rank-one luma ceiling glyph projection"
s1 = C.score("Use an orientation glyph: 4 edge angles per cell, measure VLM recovery vs 0.3 baseline.", qq, [])
s2 = C.score("Use an orientation glyph: 4 edge angles per cell, measure VLM recovery vs 0.3 baseline.", qq,
             ["Use an orientation glyph: 4 edge angles per cell, measure VLM recovery vs 0.3 baseline."])
s3 = C.score("I love pizza and sunny weather at the beach with friends.", qq, [])
check("repeat has lower novelty", s2["novelty"] < s1["novelty"])
check("off-topic flagged derail", s3["derail"] and not s1["derail"])
check("on-topic concrete beats off-topic", s1["total"] > s3["total"])
check("score deterministic", C.score("abc glyph luma 12", qq, []) == C.score("abc glyph luma 12", qq, []))

# 15. auto conductor: checkpoints; forks a peak; rewinds a derail streak
a = forest()
a.round("main"); a.score_turns("main")
for t in a.branches["main"].turns:
    t["score"]["total"] = 0.2
a.branches["main"].turns[1]["score"]["total"] = 0.9
ms = C.auto_moves(a, "main", 1)
check("auto: checkpoint first", ms[0]["op"] == "checkpoint")
check("auto: forks the peak", any(m["op"] == "branch" and m["at"] == a.branches["main"].turns[1]["id"] for m in ms))
for m in ms:
    a.apply(m)
for t in a.branches["main"].turns[-3:]:
    t["score"]["derail"] = True
ms2 = C.auto_moves(a, "main", 2)
check("auto: derail streak -> rewind + tone", [m["op"] for m in ms2[:2]] == ["rewind", "tone"])
a.draw = lambda k: k - 1
for t in a.branches["main"].turns:
    t["score"]["total"] = 0.8
ms3 = [m for m in C.auto_moves(a, "main", 3) if m["op"] == "branch"]
check("auto: draw picks among ties", ms3 and ms3[0]["at"] != a.branches["main"].turns[1]["id"])

# 16. persistence round trip + CLI offline run
with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, "s.json")
    f.save(p)
    g = C.Forest(); g.load_state(p)
    check("save/load preserves every branch hash",
          {k: v.state_hash() for k, v in g.branches.items()} == {k: v.state_hash() for k, v in f.branches.items()})
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        rc = C.main(["--out", d, "--rounds", "2", "--auto", "--question", "rank-one luma ceiling"])
    st = json.load(open(os.path.join(d, "state.json")))
    check("CLI offline run", rc == 0 and len(st["branches"]["main"]["turns"]) == 16)
    led = K.Ledger.load(open(os.path.join(d, "ledger.jsonl")).read())
    check("CLI ledger file verifies", led.verify()["intact"])
    mv = os.path.join(d, "m.json")
    json.dump([{"op": "tone", "branch": "main", "cell": "qwen", "text": "go stranger"},
               {"op": "bogus"}], open(mv, "w"))
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        C.main(["--out", d, "--resume", "--moves", mv, "--rounds", "1"])
    st2 = json.load(open(os.path.join(d, "state.json")))
    check("resume applies moves, refuses bogus", "REFUSED" in buf.getvalue()
          and st2["branches"]["main"]["tones"]["qwen"] == "go stranger")
    check("resume ledger still one chain", K.Ledger.load(open(os.path.join(d, "ledger.jsonl")).read()).verify()["intact"])

# 17. parallel branches == sequential branches (state), ledger stays one intact chain
def fork3(par):
    with tempfile.TemporaryDirectory() as d:
        import contextlib, io
        mv = os.path.join(d, "m.json")
        with contextlib.redirect_stdout(io.StringIO()):
            C.main(["--out", d, "--rounds", "1", "--question", "rank-one luma"])
            json.dump([{"op": "branch", "from": "main", "at": "main.t2", "name": "b1"},
                       {"op": "zoom", "branch": "main", "turn": "main.t4", "name": "z", "cells": ["hy3", "glm"]}], open(mv, "w"))
            C.main(["--out", d, "--resume", "--moves", mv, "--rounds", "2", "--parallel", str(par)])
        st = json.load(open(os.path.join(d, "state.json")))
        led = K.Ledger.load(open(os.path.join(d, "ledger.jsonl")).read())
        return {k: [t["receipt"] for t in v["turns"]] for k, v in st["branches"].items()}, led.verify()["intact"], len(led.records)
s_seq, ok_seq, n_seq = fork3(1)
s_par, ok_par, n_par = fork3(4)
check("parallel branches reach sequential state", s_seq == s_par and len(s_par) == 3)
check("parallel ledger intact, same size", ok_par and ok_seq and n_par == n_seq)

print("convo-quilt selftest: %d checks, %d failures" % (checks, fails))
sys.exit(1 if fails else 0)
