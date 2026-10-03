"""crew-runner selftest — offline (stub models only), deterministic, no network, no corpus writes."""
import json, os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import crew_runner as C

checks, fails = 0, []


def check(name, cond):
    global checks
    checks += 1
    if not cond:
        fails.append(name)
        print("FAIL", name)


tmp = tempfile.mkdtemp(prefix="crew-runner-")
try:
    sig = os.path.join(tmp, "signals.jsonl")
    cache = os.path.join(tmp, "cache.json")
    crew = C.CrewRunner(models=["stub:a", "stub:b", "stub:broken"], cache_path=cache, signals_path=sig, ref="selftest")

    # 1. fan-out: one prompt reaches every model, deterministically
    outs = crew.ask("propose", "name one idea")
    check("fan-out returns one output per model", [o["model"] for o in outs] == ["stub:a", "stub:b", "stub:broken"])
    check("fan-out made exactly 3 real calls", crew.calls == 3)
    check("distinct models give distinct text", len({o["text"] for o in outs}) == 3)
    again = C.CrewRunner(models=["stub:a"], signals_path=None).ask("propose", "name one idea")
    check("stub is deterministic across runners", again[0]["text"] == outs[0]["text"])

    # 2. gate: the broken output is rejected, the good ones kept
    kept, rej = crew.gate(outs, C.json_gate("idea", "score"))
    check("gate keeps the 2 well-formed outputs", sorted(o["model"] for o in kept) == ["stub:a", "stub:b"])
    check("gate rejects the malformed output", [r["model"] for r in rej] == ["stub:broken"] and rej[0]["reason"] == "not JSON")
    check("gate rejects a missing key", C.json_gate("nope")(outs[0]["text"])[0] is False)
    check("rejected text never enters branch context",
          all("sure!" not in t for e in crew.branches["main"] for t in e["kept"]) and len(crew.branches["main"][0]["kept"]) == 2)

    # 3. cache: a repeat returns the same answer without a second call
    fresh = C.CrewRunner(models=["stub:a", "stub:b"], cache_path=os.path.join(tmp, "c2.json"), signals_path=None)
    r1 = fresh.ask("x", "same prompt")
    fresh.branches["main"].clear()                  # same context, so the same cache key
    r2 = fresh.ask("x", "same prompt")
    check("cache: identical answers", [o["text"] for o in r1] == [o["text"] for o in r2])
    check("cache: no second call", fresh.calls == 2 and all(o["cached"] for o in r2))
    check("cache hit rate is measured (2 of 4)", fresh.split()["cache_hit_rate"] == 0.5)
    reload_ = C.CrewRunner(models=["stub:a", "stub:b"], cache_path=os.path.join(tmp, "c2.json"), signals_path=None)
    r3 = reload_.ask("x", "same prompt")
    check("cache persists to disk across runners", reload_.calls == 0 and [o["text"] for o in r3] == [o["text"] for o in r1])
    check("use_cache=False forces a real call", fresh.ask("x", "same prompt", use_cache=False)[0]["cached"] is False)

    # 4. retries + failure are measured, not hidden
    flaky = {"n": 0}

    def caller(provider, model, messages, mt):
        flaky["n"] += 1
        if flaky["n"] == 1:
            raise C.P.ProviderError("empty content")
        return C.stub_call(model, messages, mt)
    fr = C.CrewRunner(models=["stub:a", "stub:down"], signals_path=sig)
    fo = fr.ask("x", "y")
    check("a down model fails after retries", fo[1].get("error") and fo[1]["attempts"] == 2 and fr.totals["failures"] == 1)
    rr = C.CrewRunner(models=["stub:a"], signals_path=None, caller=caller)
    ro = rr.ask("x", "y")
    check("retry recovers and is counted", not ro[0].get("error") and rr.totals["retries"] == 1)

    # 5. rewind / branch (convo-quilt idiom)
    b = C.CrewRunner(models=["stub:a"], signals_path=None)
    b.gate(b.ask("r", "one"), lambda t: True)
    b.checkpoint("c1")
    b.gate(b.ask("r", "two"), lambda t: True)
    check("history grows", len(b.branches["main"]) == 2)
    ctx2 = b._messages("r", "three")[1]["content"]
    b.rewind("c1")
    check("rewind truncates history", len(b.branches["main"]) == 1)
    check("rewind changes the context of the next ask", b._messages("r", "three")[1]["content"] != ctx2)
    b.branch("alt", at="c1")
    b.ask("r", "alt-two")
    check("branch forks without touching main", len(b.branches["alt"]) == 2 and len(b.branches["main"]) == 1)
    check("entry ids are never reused after rewind", b.branches["alt"][-1]["id"] == "t2")
    check("rewinds/branches are logged", [e["op"] for e in b.events] == ["checkpoint", "rewind", "branch"])

    # 6. signals: written, typed, chain-verifies, tamper is caught
    crew.signal("PLAN", "manual signal", "WORKED", {"wall_s": 0.1}, fix="")
    recs = C.load_signals(sig)
    check("auto signals written for ask+gate (+manual)", [r["pattern"] for r in recs][:2] == ["crew.ask:propose", "crew.gate"])
    check("ask signal carries measured token split",
          recs[0]["cost"]["cheap_tokens_in"] > 0 and recs[0]["cost"]["anthropic_tokens_est"] > 0 and recs[0]["cost"]["lookups"] == 3)
    check("gate signal is CLUNKY with the rejection as fix", recs[1]["outcome"] == "CLUNKY" and "stub:broken" in recs[1]["fix"])
    check("down model makes the ask CLUNKY", any(r["pattern"] == "crew.ask:x" and r["outcome"] == "CLUNKY" for r in recs))
    ok, msg = C.verify_signals(recs)
    check("signal chain verifies", ok)
    bad = json.loads(json.dumps(recs))
    bad[1]["outcome"] = "WORKED"
    check("an edited signal breaks the chain", C.verify_signals(bad)[0] is False)
    check("a dropped signal breaks the chain", C.verify_signals(recs[:1] + recs[2:])[0] is False)
    try:
        crew.signal("NAP", "x", "WORKED")
        check("bad phase refused", False)
    except ValueError:
        check("bad phase refused", True)

    # 7. seed scars: 12 records, idempotent, chain-verifies
    seedp = os.path.join(tmp, "seed.jsonl")
    n1, n2 = C.seed_scars(seedp), C.seed_scars(seedp)
    srecs = C.load_signals(seedp)
    check("seed books 12 scars once", (n1, n2, len(srecs)) == (12, 0, 12))
    check("seed outcomes match §2 (7 SCAR, 5 CLUNKY)",
          sum(r["outcome"] == "SCAR" for r in srecs) == 7 and sum(r["outcome"] == "CLUNKY" for r in srecs) == 5)
    check("seed chain verifies", C.verify_signals(srecs)[0])

    # 8. the corpus file in the repo (if present) verifies
    if os.path.exists(C.SIGNALS_PATH):
        check("repo process-signals.jsonl verifies", C.verify_signals(C.load_signals(C.SIGNALS_PATH))[0])
finally:
    shutil.rmtree(tmp)

print("crew-runner selftest: %d checks, %d failures" % (checks, len(fails)))
sys.exit(1 if fails else 0)
