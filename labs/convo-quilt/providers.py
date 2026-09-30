"""providers — one stdlib chat() over the cheap-model endpoints, plus JEV and Moth.

Every call returns {"text", "tokens": {"in", "out"}, "wall_ms", "model", "provider"} or raises
ProviderError. No retries hidden inside: the bus decides what a failure means.
Keys come from env only; nothing here logs a key.
"""
import json, os, time, urllib.request, urllib.error

ENDPOINTS = {   # provider -> (base chat URL, env key)
    "deepinfra": ("https://api.deepinfra.com/v1/openai/chat/completions", "DEEPINFRA_KEY"),
    "zai":       ("https://api.z.ai/api/paas/v4/chat/completions", "ZAI_KEY"),
    "zai-coding": ("https://api.z.ai/api/coding/paas/v4/chat/completions", "ZAI_KEY"),
    "kimi":      ("https://api.moonshot.ai/v1/chat/completions", "KIMIAI_KEY"),
    "deepseek":  ("https://api.deepseek.com/chat/completions", "DEEPSEEK_KEY"),
    "groq":      ("https://api.groq.com/openai/v1/chat/completions", "GROQ_KEY"),
}
JEV_URL = "https://api.typesafe.ai/v1/systemone"


class ProviderError(Exception):
    pass


def _post(url, key, body, timeout):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": "Bearer " + key,
                                          "Content-Type": "application/json",
                                          "User-Agent": "convo-quilt/1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise ProviderError("HTTP %d: %s" % (e.code, e.read().decode(errors="replace")[:200]))
    except Exception as e:  # timeouts, DNS, bad JSON
        raise ProviderError("%s: %s" % (type(e).__name__, str(e)[:200]))


def chat(provider, model, messages, max_tokens=500, temperature=0.8, timeout=90):
    url, env = ENDPOINTS[provider]
    key = os.environ.get(env, "")
    if not key:
        raise ProviderError("no %s in env" % env)
    t0 = time.time()
    d = _post(url, key, {"model": model, "messages": messages, "max_tokens": max_tokens,
                         "temperature": temperature}, timeout)
    try:
        msg = d["choices"][0]["message"]
    except (KeyError, IndexError, TypeError):
        raise ProviderError("no choices: %s" % json.dumps(d)[:200])
    text = (msg.get("content") or "").strip()
    if not text:   # reasoning models sometimes spend the whole budget thinking
        raise ProviderError("empty content (reasoning=%d chars)" % len(msg.get("reasoning_content") or ""))
    u = d.get("usage") or {}
    return {"text": text, "tokens": {"in": int(u.get("prompt_tokens", 0)), "out": int(u.get("completion_tokens", 0))},
            "wall_ms": int((time.time() - t0) * 1000), "model": model, "provider": provider}


def jev(state, questions, timeout=30):
    """TypeSafe.ai JEV batch judge. questions = {name: {"type": "score", "instructions": str,
    "criteria": [ordered labels]}}. Returns the raw JSON dict (shape recorded in probe.json)."""
    key = os.environ.get("TYPESAFEAI_KEY", "")
    if not key:
        raise ProviderError("no TYPESAFEAI_KEY in env")
    return _post(JEV_URL, key, {"model": "jev-latest", "state": state[:1000],
                                "questions": questions}, timeout)


def moth_draw(k, shots=64, timeout=60):
    """Un-gameable pick in [0, k) from one Moth coin-toss-v1 job: heads-count mod k.
    (Modulo bias is <= k/65 — fine for choosing a rewind point, not for crypto.)
    Returns (index, job_id, heads). Raises ProviderError when unkeyed or failed."""
    base, key = os.environ.get("MOTHQUANTUM_BASE", ""), os.environ.get("MOTHQUANTUM_KEY", "")
    if not base or not key:
        raise ProviderError("MOTHQUANTUM_BASE / MOTHQUANTUM_KEY not set")
    H = {"Authorization": "Bearer " + key, "Content-Type": "application/json", "User-Agent": "convo-quilt/1"}

    def call(path, body=None):
        req = urllib.request.Request(base.rstrip("/") + path, headers=H,
                                     method="POST" if body is not None else "GET",
                                     data=json.dumps(body).encode() if body is not None else None)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            raise ProviderError("moth %s: %s" % (path, str(e)[:160]))

    job = call("/engines/coin-toss-v1/process", {"params": {"shots": shots, "mode": "emu"}})["job_id"]
    for _ in range(40):
        st = call("/jobs/%s/status" % job).get("status")
        if st == "completed":
            break
        if st == "failed":
            raise ProviderError("moth job %s failed" % job)
        time.sleep(1.5)
    else:
        raise ProviderError("moth job %s timed out" % job)
    heads = int(call("/jobs/%s/result" % job).get("result", {}).get("heads", 0))
    return heads % k, job, heads
