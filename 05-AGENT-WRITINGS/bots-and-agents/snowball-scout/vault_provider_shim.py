#!/usr/bin/env python3
"""
vault_provider_shim.py — stand in for snowball_writer's three LLM providers.

snowball_writer.py calls zai / groq / deepinfra with ZAI_TOKEN / GROQ_TOKEN /
DEEPINFRA_TOKEN. Those keys live on the fleet host, not in this sandbox, and the
fleet's own `providers.py` says so explicitly: "Keys come from env only".

This shim reroutes those three provider calls to the fleet's SuperInstance vault
(https://superinstance-vault.casey-digennaro.workers.dev/proxy), which holds the
LLM credential and is reachable from inside GitHub Actions via a GitHub OIDC
token. The vault's upstream is MiniMax; three live models are exposed, which is
exactly the three-way parallel competition the RSI GAN path wants:

    zai       -> MiniMax-M2.5     (the fleet's flagship lineage: glm-5.3 -> M2.5)
    groq      -> MiniMax-M1       (the fast lane, as groq was the fast lane)
    deepinfra -> MiniMax-Text-01  (the old faithful lane)

The scoring, prompt construction, seed selection, file naming and witness log
all stay in snowball_writer.py. Only the transport changes.
"""
import json
import os
import urllib.request
import urllib.error

VAULT_URL = os.environ.get(
    "VAULT_URL", "https://superinstance-vatch.casey-digennaro.workers.dev"
)
if "vatch" in VAULT_URL:  # guard against typo in the default above
    VAULT_URL = "https://superinstance-vault.casey-digennaro.workers.dev"

# provider name -> vault model id
PROVIDER_MODELS = {
    "zai": "MiniMax-M2.5",
    "groq": "MiniMax-M1",
    "deepinfra": "MiniMax-Text-01",
}

OIDC = os.environ.get("OIDC_TOKEN", "")


def _vault_complete(prompt, model, max_tokens=600, timeout=180):
    """One completion through the vault. Returns text or None."""
    if not OIDC:
        raise RuntimeError("OIDC_TOKEN not set — vault calls need Actions OIDC")
    body = {
        "oidc_token": OIDC,
        "service": "llm",
        "action": "complete",
        "params": {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        },
    }
    req = urllib.request.Request(
        VAULT_URL + "/proxy",
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "purplepincher-zero/1.0 (+https://github.com/purplepincher/zero)",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = json.loads(resp.read().decode())
    if not raw.get("success"):
        raise RuntimeError("vault error: %s" % json.dumps(raw)[:300])
    r = raw.get("result", raw)
    if isinstance(r, dict):
        return (r.get("content") or r.get("text") or "").strip()
    return str(r).strip()


def _strip_think(text):
    """MiniMax M1/M2.5 emit <think>...</think> before the answer. Keep the answer."""
    if not text:
        return text
    if "</think>" in text:
        text = text.split("</think>", 1)[1]
    if "<think>" in text:
        text = text.split("<think>", 1)[0] + text.split("<think>", 1)[1] if text.count("<think>") == 1 else text
    return text.strip()


def call_zai(prompt, max_tokens=600):
    try:
        return _strip_think(_vault_complete(prompt, PROVIDER_MODELS["zai"], max_tokens))
    except Exception as e:
        print("[shim] zai failed: %s" % e)
        return None


def call_groq(prompt, max_tokens=600, model=None):
    try:
        return _strip_think(
            _vault_complete(prompt, PROVIDER_MODELS["groq"], max_tokens)
        )
    except Exception as e:
        print("[shim] groq failed: %s" % e)
        return None


def call_deepinfra(prompt, max_tokens=600, model=None):
    try:
        return _strip_think(
            _vault_complete(prompt, PROVIDER_MODELS["deepinfra"], max_tokens)
        )
    except Exception as e:
        print("[shim] deepinfra failed: %s" % e)
        return None
