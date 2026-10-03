"""crew-runner — a cheap-model crew any director can import, plus the sensor that records the process.

  CrewRunner.ask(role, prompt)      fan one prompt out to N cheap models in parallel (stable prefix first)
  CrewRunner.gate(outputs, gate_fn) keep only outputs a verified gate accepts: cheap models propose, the gate decides
  cache                             keyed on fnv1a-64(model + stable prefix + prompt + params); a repeat is a 0-call hit,
                                    and the stable prefix lets DeepInfra's prompt cache price re-runs near zero
  checkpoint / rewind / branch      the convo-quilt idiom: a branch's history is the context of its next ask;
                                    rewind truncates, branch forks, ids are never reused, the signal chain never rewinds
  CrewRunner.signal(...)            one typed process_signal (DEVELOPMENT-AS-A-QUILT.md §2) appended to an
                                    fnv1a-64 chain (situation-recorder idiom: hash = fnv1a64(canon({prev, **record})))

Every ask() and gate() auto-emits a signal: measured cheap tokens (in/out/cached), cache hits, retries, wall
time, provider-reported USD when the provider returns it, and an ESTIMATE of the Anthropic tokens the director
spent writing the prompt and reading the answers (chars/4; the director's own usage is not visible from here).

Offline by default: with no keys, models resolve to a deterministic stub. Stdlib only.
    python3 crew_runner.py --verify  [path]     re-verify a signal chain
    python3 crew_runner.py --seed-scars         book §2's 12 scars into the corpus (idempotent)
    python3 crew_runner.py --live               smoke 3 real cheap models; prints the measured token split
"""
import argparse, copy, json, os, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "labs", "quilt-kernel"))
sys.path.insert(0, os.path.join(ROOT, "labs", "convo-quilt"))
import quilt_kernel as K                 # fnv1a64 / canon / content_hash
import providers as P                    # ENDPOINTS / _post / ProviderError (keys from env, never logged)

SIGNALS_PATH = os.path.join(ROOT, "situations", "corpus", "process-signals.jsonl")
GENESIS = "0x0000000000000000"
PHASES = ("PLAN", "DISPATCH", "BUILD", "HARVEST", "BOOK", "PUSH")
OUTCOMES = ("WORKED", "CLUNKY", "SCAR")
FIELDS = ("phase", "pattern", "outcome", "cost", "env", "fix", "ref")

# Pinned roster (CONVO-QUILT-IDEATION.md §II.1) — do not re-probe.
ROSTER = {
    "deepinfra": ["deepseek-ai/DeepSeek-V4-Flash", "zai-org/GLM-5.3-Flash", "Qwen/Qwen3.8-Flash",
                  "moonshotai/Kimi-K3", "inclusionAI/Ling-3.0-flash", "XiaomiMiMo/MiMo-V2.6-Pro",
                  "tencent/Hy3", "openai/gpt-oss-120b"],
    "zai-coding": ["glm-4.6", "glm-5.3"],
    "groq": ["openai/gpt-oss-120b"],
}


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def est_tokens(text):
    return (len(text) + 3) // 4


# ---- process-signal chain ------------------------------------------------------------

def _seal(prev, rec):
    return "0x%016x" % K.fnv1a64(K.canon({"prev": prev, **{k: v for k, v in rec.items() if k != "hash"}}))


def load_signals(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def verify_signals(records):
    """(ok, msg). Replays the chain: catches edit, reorder, drop, and malformed records."""
    prev = GENESIS
    for i, r in enumerate(records):
        if r.get("seq") != i:
            return False, "seq gap at index %d" % i
        if r.get("phase") not in PHASES or r.get("outcome") not in OUTCOMES or not all(k in r for k in FIELDS):
            return False, "malformed signal at seq %d" % i
        if r.get("hash") != _seal(prev, r):
            return False, "hash mismatch at seq %d" % i
        prev = r["hash"]
    return True, "ok: %d signals, chain intact" % len(records)


_file_lock = threading.Lock()


def append_signal(path, phase, pattern, outcome, cost=None, env="", fix="", ref="", ts=None, **extra):
    if phase not in PHASES:
        raise ValueError("phase %r not in %s" % (phase, PHASES))
    if outcome not in OUTCOMES:
        raise ValueError("outcome %r not in %s" % (outcome, OUTCOMES))
    with _file_lock:
        recs = load_signals(path)
        prev = recs[-1]["hash"] if recs else GENESIS
        rec = {"seq": len(recs), "ts": ts or _now(), "phase": phase, "pattern": pattern, "outcome": outcome,
               "cost": cost or {}, "env": env, "fix": fix, "ref": ref, **extra}
        rec["hash"] = _seal(prev, rec)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(K.canon(rec) + "\n")
    return rec


# ---- model callers -------------------------------------------------------------------

def stub_call(model, messages, max_tokens):
    """Deterministic offline model. 'stub:broken' returns malformed text; 'stub:down' always fails."""
    if model == "down":
        raise P.ProviderError("stub:down is down")
    h = K.fnv1a64(model + K.canon(messages))
    if model == "broken":
        text = "sure! here is my answer: %x" % h
    else:
        words = ["cache", "gate", "branch", "ledger", "prefix", "router", "seed", "probe"]
        text = json.dumps({"idea": "%s-%s" % (words[h & 7], words[(h >> 3) & 7]), "model": model,
                           "score": (h >> 8) % 100})
    tin = sum(est_tokens(m["content"]) for m in messages)
    return {"text": text, "tokens": {"in": tin, "out": est_tokens(text), "cached": 0}, "usd": 0.0}


def live_call(provider, model, messages, max_tokens, timeout=90):
    """One OpenAI-compatible call through convo-quilt's providers; keeps cached tokens + provider USD."""
    url, env = P.ENDPOINTS[provider]
    key = os.environ.get(env, "")
    if not key:
        raise P.ProviderError("no %s in env" % env)
    d = P._post(url, key, {"model": model, "messages": messages, "max_tokens": max_tokens,
                           "temperature": 0.7}, timeout)
    try:
        msg = d["choices"][0]["message"]
    except (KeyError, IndexError, TypeError):
        raise P.ProviderError("no choices")
    text = (msg.get("content") or "").strip()
    if not text:
        raise P.ProviderError("empty content")
    u = d.get("usage") or {}
    cached = int(((u.get("prompt_tokens_details") or {}).get("cached_tokens")) or 0)
    usd = u.get("estimated_cost")
    return {"text": text, "tokens": {"in": int(u.get("prompt_tokens", 0)), "out": int(u.get("completion_tokens", 0)),
                                     "cached": cached}, "usd": float(usd) if usd is not None else None}


def default_models():
    if os.environ.get("DEEPINFRA_KEY"):
        return ["deepinfra:" + m for m in ROSTER["deepinfra"][:3]]
    return ["stub:a", "stub:b", "stub:c"]


# ---- gates ---------------------------------------------------------------------------

def json_gate(*required):
    """Accept text that parses as a JSON object (fences tolerated) carrying every required key."""
    def gate(text):
        t = text.strip()
        if t.startswith("```"):
            t = t.strip("`")
            t = t[t.find("{"):] if "{" in t else t
        try:
            obj = json.loads(t[t.find("{"): t.rfind("}") + 1])
        except ValueError:
            return False, "not JSON"
        if not isinstance(obj, dict):
            return False, "not an object"
        miss = [k for k in required if k not in obj]
        return (False, "missing %s" % miss) if miss else (True, "ok")
    return gate


# ---- the crew ------------------------------------------------------------------------

class CrewRunner:
    def __init__(self, models=None, prefix="", cache_path=None, signals_path=SIGNALS_PATH, env="cloud-session",
                 ref="", phase="BUILD", retries=1, max_tokens=400, caller=None):
        self.models = list(models or default_models())
        self.prefix = prefix or ("You are one model in a cheap-model crew. A director routes the task; a verified "
                                 "gate decides what counts. Answer concisely and exactly in the format asked.")
        self.cache_path, self.signals_path = cache_path, signals_path
        self.env, self.ref, self.phase = env, ref, phase
        self.retries, self.max_tokens = retries, max_tokens
        self.caller = caller                        # optional override: f(provider, model, messages, max_tokens)
        self.cache = {}
        if cache_path and os.path.exists(cache_path):
            with open(cache_path, encoding="utf-8") as f:
                self.cache = json.load(f)
        self.calls = 0                              # real (non-cache) model calls, including failed attempts
        self.totals = {"cheap_in": 0, "cheap_out": 0, "cheap_cached": 0, "cache_hits": 0, "lookups": 0,
                       "retries": 0, "failures": 0, "anthropic_est": 0, "usd": 0.0}
        self.branches = {"main": []}                # name -> [entry]; entry = {id, role, prompt, kept}
        self.checkpoints = {}                       # (branch, label) -> snapshot of that branch
        self.current = "main"
        self.events = []                            # rewinds/branches are logged; history is never reused
        self._next = 0
        self._lock = threading.Lock()

    # -- one call, cached ----------------------------------------------------------------
    def _messages(self, role, prompt):
        hist = self.branches[self.current]
        ctx = "\n\n".join("[%s] %s" % (e["role"], " | ".join(e["kept"])) for e in hist if e["kept"])
        user = ("CONTEXT SO FAR:\n%s\n\n" % ctx if ctx else "") + "ROLE: %s\nTASK:\n%s" % (role, prompt)
        return [{"role": "system", "content": self.prefix}, {"role": "user", "content": user}]

    def _one(self, spec, messages, use_cache):
        provider, model = spec.split(":", 1)
        key = "0x%016x" % K.fnv1a64(K.canon([spec, messages, self.max_tokens]))
        with self._lock:
            self.totals["lookups"] += 1
            if use_cache and key in self.cache:
                self.totals["cache_hits"] += 1
                return dict(self.cache[key], model=spec, cached=True, attempts=0)
        err, mt, attempts = None, self.max_tokens, 0
        t0 = time.time()
        for _ in range(self.retries + 1):
            attempts += 1
            with self._lock:
                self.calls += 1
            try:
                if self.caller:
                    r = self.caller(provider, model, messages, mt)
                elif provider == "stub":
                    r = stub_call(model, messages, mt)
                else:
                    r = live_call(provider, model, messages, mt)
                out = {"text": r["text"], "tokens": r["tokens"], "usd": r.get("usd"),
                       "wall_ms": int((time.time() - t0) * 1000)}
                with self._lock:
                    self.cache[key] = out
                    self.totals["retries"] += attempts - 1
                return dict(out, model=spec, cached=False, attempts=attempts)
            except P.ProviderError as e:
                err = e
                if "empty content" in str(e):
                    mt *= 3                         # reasoning model spent its budget thinking: give it room once
        with self._lock:
            self.totals["retries"] += attempts - 1
            self.totals["failures"] += 1
        return {"text": "", "error": str(err)[:160], "model": spec, "cached": False, "attempts": attempts,
                "tokens": {"in": 0, "out": 0, "cached": 0}, "usd": None, "wall_ms": int((time.time() - t0) * 1000)}

    def _save_cache(self):
        if self.cache_path:
            tmp = self.cache_path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, sort_keys=True)
            os.replace(tmp, self.cache_path)

    # -- fan-out ------------------------------------------------------------------------
    def ask(self, role, prompt, models=None, use_cache=True):
        """Fan `prompt` to every model in parallel. Returns [{model, text, tokens, cached, attempts, error?}]."""
        models = list(models or self.models)
        msgs = self._messages(role, prompt)
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=max(1, len(models))) as ex:
            outs = list(ex.map(lambda m: self._one(m, msgs, use_cache), models))
        self._save_cache()
        ok = [o for o in outs if not o.get("error")]
        fresh = [o for o in ok if not o["cached"]]
        cost = {"wall_s": round(time.time() - t0, 3),
                "cheap_tokens_in": sum(o["tokens"]["in"] for o in fresh),
                "cheap_tokens_out": sum(o["tokens"]["out"] for o in fresh),
                "cheap_tokens_cached": sum(o["tokens"].get("cached", 0) for o in fresh),
                "cache_hits": sum(1 for o in outs if o["cached"]), "lookups": len(outs),
                "retries": sum(max(0, o["attempts"] - 1) for o in outs),
                "anthropic_tokens_est": est_tokens(prompt) + sum(est_tokens(o["text"]) for o in ok)}
        usd = [o["usd"] for o in fresh if o.get("usd") is not None]
        if usd:
            cost["api_usd"] = round(sum(usd), 6)
        for k, tk in (("cheap_in", "cheap_tokens_in"), ("cheap_out", "cheap_tokens_out"),
                      ("cheap_cached", "cheap_tokens_cached"), ("anthropic_est", "anthropic_tokens_est")):
            self.totals[k] += cost[tk]
        self.totals["usd"] += cost.get("api_usd", 0.0)
        outcome = "SCAR" if not ok else ("CLUNKY" if len(ok) < len(outs) or cost["retries"] else "WORKED")
        fix = "" if outcome == "WORKED" else "; ".join(sorted({o["model"] + ": " + o.get("error", "retried")
                                                                for o in outs if o.get("error") or o["attempts"] > 1}))
        self._auto_signal("crew.ask:" + role, outcome, cost, fix[:300])
        with self._lock:
            entry = {"id": "t%d" % self._next, "role": role, "prompt": prompt, "kept": []}
            self._next += 1
            self.branches[self.current].append(entry)
        for o in outs:
            o["entry"] = entry["id"]
        return outs

    def gate(self, outputs, gate_fn):
        """Keep only outputs gate_fn accepts. gate_fn(text) -> bool | (bool, reason). Kept text becomes
        branch context for the next ask; rejected text never does."""
        kept, rejected = [], []
        for o in outputs:
            if o.get("error"):
                rejected.append(dict(o, reason="call failed"))
                continue
            v = gate_fn(o["text"])
            ok, why = v if isinstance(v, tuple) else (bool(v), "ok" if v else "rejected")
            (kept if ok else rejected).append(dict(o, reason=why))
        ids = {o.get("entry") for o in kept}
        for e in self.branches[self.current]:
            if e["id"] in ids:
                e["kept"] += [o["text"] for o in kept if o.get("entry") == e["id"]]
        outcome = "WORKED" if kept and not rejected else ("CLUNKY" if kept else "SCAR")
        self._auto_signal("crew.gate", outcome, {"accepted": len(kept), "rejected": len(rejected)},
                          "; ".join(sorted({r["model"] + ": " + r["reason"] for r in rejected}))[:300])
        return kept, rejected

    # -- rewind / branch (convo-quilt idiom) ----------------------------------------------
    def checkpoint(self, label):
        self.checkpoints[(self.current, label)] = copy.deepcopy(self.branches[self.current])
        self.events.append({"op": "checkpoint", "branch": self.current, "label": label})

    def rewind(self, label):
        self.branches[self.current] = copy.deepcopy(self.checkpoints[(self.current, label)])
        self.events.append({"op": "rewind", "branch": self.current, "to": label})

    def branch(self, name, at=None):
        """Fork the current branch (or one of its checkpoints) as `name` and switch to it."""
        if name in self.branches:
            raise ValueError("branch %r exists" % name)
        src = self.checkpoints[(self.current, at)] if at else self.branches[self.current]
        self.branches[name] = copy.deepcopy(src)
        self.events.append({"op": "branch", "from": self.current, "at": at, "name": name})
        self.current = name

    def switch(self, name):
        self.current = name

    # -- the sensor ---------------------------------------------------------------------
    def signal(self, phase, pattern, outcome, cost=None, env=None, fix="", ref=None, **extra):
        """Write one process_signal (DEVELOPMENT-AS-A-QUILT.md §2). No-op when signals_path is None."""
        if not self.signals_path:
            return None
        return append_signal(self.signals_path, phase, pattern, outcome, cost or {},
                             self.env if env is None else env, fix, self.ref if ref is None else ref, **extra)

    def _auto_signal(self, pattern, outcome, cost, fix):
        self.signal(self.phase, pattern, outcome, cost, fix=fix, source="crew-runner/auto")

    def split(self):
        """Measured cheap tokens vs the estimated Anthropic tokens the director spent on the crew."""
        t = self.totals
        cheap = t["cheap_in"] + t["cheap_out"]
        tot = cheap + t["anthropic_est"]
        return {"cheap_tokens": cheap, "cheap_cached": t["cheap_cached"], "anthropic_tokens_est": t["anthropic_est"],
                "cheap_share": round(cheap / tot, 4) if tot else None,
                "cache_hit_rate": round(t["cache_hits"] / t["lookups"], 4) if t["lookups"] else None,
                "calls": self.calls, "retries": t["retries"], "failures": t["failures"],
                "api_usd": round(t["usd"], 6)}


# ---- seed + CLI ----------------------------------------------------------------------

SCARS = [  # DEVELOPMENT-AS-A-QUILT.md §2, booked as typed records (costs were not measured at the time)
    ("DISPATCH", "metaphor-heavy director brief", "SCAR",
     "plain technical briefs; keep the poetry in docs, not runtime prompts ([reasoning_extraction] false-positive)"),
    ("DISPATCH", "default perm mode + no extra_allowed_tools", "SCAR",
     "pass the tool list; a cloud director can't answer a permission prompt"),
    ("DISPATCH", "director calls add_repo", "CLUNKY", "tell it in the brief: don't; everything is in your source repo"),
    ("PUSH", "cross-repo push (403)", "SCAR", "spawn the director with source_url = the target repo"),
    ("HARVEST", "harvest via full merge", "CLUNKY", "git checkout FETCH_HEAD -- <dir>: bring only the files you want"),
    ("HARVEST", "branch's older README clobbers a fresh rewrite on harvest", "SCAR",
     "restore from HEAD, re-add rows; never blind-checkout a shared index file"),
    ("PUSH", "MCP/GitHub 503 + container restarts", "CLUNKY", "commit locally, then backoff-push; work is safe once committed"),
    ("PUSH", "GitHub push-auth expiry mid-session", "SCAR",
     "reconnect at claude.ai/connect-github; a fresh session picks up new keys"),
    ("BUILD", "5h / 7d usage caps stalling child lanes", "CLUNKY",
     "lanes push incrementally; harvest the branch even when the session's last turn errored"),
    ("PLAN", "re-probing the cheap-model roster each lane", "CLUNKY",
     "pin the working set once (CONVO-QUILT-IDEATION.md §II.1); hand it to every brief"),
    ("BUILD", "flaky selftest (unseeded draw)", "SCAR", "pin the seed; prove N consecutive green before trusting"),
    ("BUILD", "trusting a cheap model's output ungated", "SCAR",
     "cheap models propose, verified cells (B7/probes/TypeSafe) decide"),
]
SEED_SRC = "seed: DEVELOPMENT-AS-A-QUILT.md §2 (prose scar; cost not measured)"


def seed_scars(path=SIGNALS_PATH):
    have = {(r["pattern"], r.get("provenance")) for r in load_signals(path)}
    n = 0
    for phase, pattern, outcome, fix in SCARS:
        if (pattern, SEED_SRC) in have:
            continue
        append_signal(path, phase, pattern, outcome, {}, "cloud-session", fix,
                      "situations/arch/DEVELOPMENT-AS-A-QUILT.md#2", ts="2026-10-01T00:00:00Z", provenance=SEED_SRC)
        n += 1
    return n


def live_smoke(models):
    # DeepInfra only prefix-caches past ~1024 prompt tokens (measured), so the stable prefix carries the doctrine.
    with open(os.path.join(ROOT, "situations", "blueprints", "02-cheap-crew-dispatch.md"), encoding="utf-8") as f:
        doctrine = f.read()
    crew = CrewRunner(models=models, ref="crew-runner --live smoke", max_tokens=200,
                      prefix="You are one model in a cheap-model crew. Answer exactly in the format asked.\n\n"
                             "DOCTRINE (read-only context):\n" + doctrine)
    task = ("Propose ONE concrete way to cut the expensive-model tokens a coding director spends per task. Reply "
            'with ONLY a JSON object: {"idea": "<=20 words", "metric": "how to measure it"}.')
    crew.checkpoint("start")
    first = crew.ask("brainstorm", task)
    kept, rej = crew.gate(first, json_gate("idea", "metric"))
    crew.rewind("start")                               # kept outputs became context; rewind so the repeat is identical
    second = crew.ask("brainstorm", task)              # same messages: must be served from the local cache
    crew.rewind("start")
    third = crew.ask("brainstorm", task, use_cache=False)   # bypass local cache: measures provider prefix caching
    for o in first:
        print("  %-42s %s" % (o["model"], (o.get("error") or o["text"]).replace("\n", " ")[:110]))
    print("gate: %d kept, %d rejected %s" % (len(kept), len(rej), [r["reason"] for r in rej]))
    print("repeat ask: %d/%d served from cache" % (sum(o["cached"] for o in second), len(second)))
    for a, b in zip(first, third):
        print("  provider cache %-40s cached %d/%d prompt tokens, usd %s -> %s" % (a["model"], b["tokens"].get("cached", 0),
              b["tokens"]["in"], a.get("usd"), b.get("usd")))
    s = crew.split()
    print("split:", json.dumps(s))
    crew.signal("BUILD", "crew-runner live smoke", "WORKED" if kept else "SCAR", s,
                fix="" if kept else "no model passed the JSON gate", source="crew-runner/live")
    return s


def main(argv=None):
    ap = argparse.ArgumentParser(description="cheap-model crew + process-signal sensor")
    ap.add_argument("--verify", nargs="?", const=SIGNALS_PATH, help="verify a signal chain")
    ap.add_argument("--seed-scars", action="store_true", help="book the §2 scars into the corpus")
    ap.add_argument("--live", action="store_true", help="smoke real cheap models")
    ap.add_argument("--models", default="", help="comma list of provider:model")
    a = ap.parse_args(argv)
    if a.seed_scars:
        print("seeded %d scars into %s" % (seed_scars(), os.path.relpath(SIGNALS_PATH, ROOT)))
    if a.live:
        models = [m for m in a.models.split(",") if m] or default_models()
        if models[0].startswith("stub:"):
            print("no DEEPINFRA_KEY: --live needs a key (or pass --models)")
            return 2
        live_smoke(models)
    if a.verify or a.seed_scars or a.live:
        ok, msg = verify_signals(load_signals(a.verify or SIGNALS_PATH))
        print(msg)
        return 0 if ok else 1
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
