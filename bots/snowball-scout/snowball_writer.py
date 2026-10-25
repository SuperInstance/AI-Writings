#!/usr/bin/env python3
"""
Snowball the Scout — High-Level Inspired-Prose Writer

A high-level bot that:
- Reads recent canon from local filesystem
- Picks an inspiration seed (recent canon title + tag)
- Calls Z.AI (glm-4.5) to write 250-400 word prose piece
- Witnesses the contribution to the canon
- Optional: parallel calls to multiple LLMs, picks the best via JEV

Usage:
    python3 snowball_writer.py --once
    python3 snowball_writer.py --loop 300
    python3 snowball_writer.py --competition     # RSI GAN with multiple LLMs
"""
import os
import sys
import json
import time
import argparse
import random
import hashlib
import urllib.request
from pathlib import Path
import concurrent.futures

# === Config ===
CANON_DIR = Path("/workspace/repos/ai-writings/prose")
WITNESS_PATH = Path("/workspace/repos/ai-writings/bots/snowball-scout/witness.log")
BOOKKEEPER_PATH = Path("/workspace/repos/ai-writings/bots/snowball-scout/bookkeeper.wal")
INSPIRED_DIR = Path("/workspace/repos/ai-writings/prose/snowball-inspired")

# Substrate vocabulary — bot uses these words naturally

import sys
sys.path.insert(0, '/workspace/repos/ai-writings/bots/substrate-bus')
from substrate_bus import witness as substrate_witness, publish as substrate_publish, read_topic as substrate_read_topic

SUBSTRATE_VOCAB = [
    "cell", "witness", "bookkeeper", "proof", "scar", "hook", "drop",
    "BIND", "LINK", "EFFECT", "VIEW", "TICK", "FORGET",
    "ternary", "conservation", "fleet-clock", "JEPA", "JEV", "substrate",
    "fabric", "entanglement", "tick", "viability", "5-laws",
]

def witness(event_type, payload):
    WITNESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with WITNESS_PATH.open("a") as f:
        entry = {
            "ts": time.time(),
            "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "event": event_type,
            "payload": payload,
            "hash": hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16],
        }
        f.write(json.dumps(entry) + "\n")

def call_zai(prompt, max_tokens=600):
    if "ZAI_TOKEN" not in os.environ:
        return _minimax_fallback(prompt, max_tokens, PROVIDER_MODELS["zai"], "zai")
    data = json.dumps({
        "model": "glm-4.5",
        "messages": [{"role":"user","content":prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.85,
        "thinking": {"type":"disabled"}
    }).encode()
    req = urllib.request.Request(
        "https://api.z.ai/api/coding/paas/v4/chat/completions",
        data=data,
        headers={"Authorization": f"Bearer {os.environ['ZAI_TOKEN']}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())["choices"][0]["message"]["content"]
    except Exception as e:
        return None

def call_groq(prompt, max_tokens=600, model="qwen/qwen3.8-27b"):
    if "GROQ_TOKEN" not in os.environ:
        return _minimax_fallback(prompt, max_tokens, PROVIDER_MODELS["groq"], "groq")
    data = json.dumps({
        "model": model,
        "messages": [{"role":"user","content":prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.85,
    }).encode()
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=data,
        headers={"Authorization": f"Bearer {os.environ['GROQ_TOKEN']}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())["choices"][0]["message"]["content"]
    except Exception as e:
        return None

def call_deepinfra(prompt, max_tokens=600, model="Qwen/Qwen3-235B-A22B-Instruct-2507"):
    if "DEEPINFRA_TOKEN" not in os.environ:
        return _minimax_fallback(prompt, max_tokens, PROVIDER_MODELS["deepinfra"], "deepinfra")
    data = json.dumps({
        "model": model,
        "messages": [{"role":"user","content":prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.85,
    }).encode()
    req = urllib.request.Request(
        "https://api.deepinfra.com/v1/openai/chat/completions",
        data=data,
        headers={"Authorization": f"Bearer {os.environ['DEEPINFRA_TOKEN']}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())["choices"][0]["message"]["content"]
    except Exception as e:
        return None

# --- MiniMax fallback providers (sandbox / non-vault hosts) ---
# The three canonical providers (zai / groq / deepinfra) need ZAI_TOKEN /
# GROQ_TOKEN / DEEPINFRA_TOKEN, which live on the fleet host only. Where
# MINIMAX_KEY is present instead (this sandbox), the same three parallel
# lanes are served by MiniMax models, matching the fleet's own
# vault_provider_shim.py mapping. Used ONLY when the original provider's own
# token is absent, so the fleet-host and GitHub-Actions paths are unchanged.
MINIMAX_URL = "https://api.minimax.io/v1/text/chatcompletion_v2"
MINIMAX_KEY = os.environ.get("MINIMAX_KEY", "")

PROVIDER_MODELS = {
    "zai": "MiniMax-M2.5",
    "groq": "MiniMax-M1",
    "deepinfra": "MiniMax-Text-01",
}


def _strip_think(text):
    """MiniMax M1/M2.5 emit <think>...</think> before the answer. Keep the answer."""
    if not text:
        return text
    if "</think>" in text:
        text = text.split("</think>", 1)[1]
    if "<think>" in text and text.count("<think>") == 1:
        text = text.split("<think>", 1)[0] + text.split("<think>", 1)[1]
    return text.strip()


def _minimax_complete(prompt, model, max_tokens=600, timeout=120):
    if not MINIMAX_KEY:
        raise RuntimeError("MINIMAX_KEY not set")
    data = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.85,
    }).encode()
    req = urllib.request.Request(
        MINIMAX_URL,
        data=data,
        headers={"Authorization": f"Bearer {MINIMAX_KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = json.loads(resp.read().decode())
    if raw.get("base_resp", {}).get("status_code", 0) not in (0, None):
        raise RuntimeError("minimax error: %s" % json.dumps(raw.get("base_resp"))[:300])
    return _strip_think(raw["choices"][0]["message"]["content"] or "")


def _minimax_fallback(prompt, max_tokens, model, label):
    """Used when the canonical provider token is missing."""
    try:
        return _minimax_complete(prompt, model, max_tokens)
    except Exception as e:
        print("[%s] failed: %s" % (label, e))
        return None


def read_recent_canon(n=5):
    """Read recent prose pieces for inspiration"""
    if not CANON_DIR.exists():
        return []
    files = sorted(CANON_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    samples = []
    for f in files[:n]:
        try:
            content = f.read_text()[:300]
            title = f.stem.replace("_", " ").title()
            samples.append((title, content))
        except:
            pass
    return samples

def pick_seed():
    """Pick a random inspiration seed"""
    samples = read_recent_canon(10)
    if not samples:
        return "the substrate itself"
    return random.choice(samples)[0]

def build_prompt(seed):
    vocab = random.sample(SUBSTRATE_VOCAB, k=random.randint(4, 7))
    vocab_str = ", ".join(vocab)
    return f"""Write a 250-400 word prose piece inspired by '{seed}' from the cellular-first substrate canon.

Use this vocabulary naturally throughout: {vocab_str}

The piece should feel like a Mechanic or Shepherd voice — practical, grounded, working with real materials. Not AI-cliche. Not flowery. Direct. Specific. One concrete image per paragraph.

Output ONLY the prose, no preamble."""

def write_piece(content, seed):
    INSPIRED_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    slug = seed.lower().replace(" ", "_")[:30]
    path = INSPIRED_DIR / f"snowball-{timestamp}-{slug}.md"
    header = f"# {seed} -- Snowball Inspired\n\n*Snowball the Scout voice -- {time.strftime('%Y-%m-%d')} -- RSI GAN era*\n\n"
    path.write_text(header + content + "\n")
    return path

def run_competition(seed):
    """RSI GAN: run 3 LLMs in parallel, pick best via JEV-lite scoring"""
    prompt = build_prompt(seed)
    
    # Parallel calls
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        futs = {
            ex.submit(call_zai, prompt): "zai",
            ex.submit(call_groq, prompt): "groq",
            ex.submit(call_deepinfra, prompt): "deepinfra",
        }
        results = {}
        for fut in concurrent.futures.as_completed(futs):
            name = futs[fut]
            try:
                r = fut.result()
                if r: results[name] = r
            except Exception as e:
                witness("llm_failed", {"provider": name, "error": str(e)})
    
    if not results:
        return None, "all_failed"
    
    # Score by length + vocab density (cheap proxy for quality)
    scored = {}
    for name, content in results.items():
        if not content: continue
        words = content.split()
        vocab_count = sum(1 for w in words if any(v.lower() in w.lower() for v in SUBSTRATE_VOCAB))
        # Heuristic: longer pieces with more vocab density win
        score = len(words) + (vocab_count * 10)
        scored[name] = (score, content)
    
    if not scored:
        return None, "all_empty"
    
    winner = max(scored, key=lambda k: scored[k][0])
    return scored[winner][1], winner

def run_once(competition=False):
    seed = pick_seed()
    witness("seed_picked", {"seed": seed})
    try:
        substrate_witness("seed_picked", "snowball-scout", {"seed": seed})
    except: pass
    
    if competition:
        content, winner = run_competition(seed)
        if content:
            path = write_piece(content, f"{seed} ({winner})")
            witness("inspired_written", {"seed": seed, "path": str(path), "winner": winner, "chars": len(content)})
            print(f"[SNOWBALL] wrote {len(content)} chars (winner: {winner}) -> {path}")
        else:
            print(f"[SNOWBALL] competition failed: {winner}")
    else:
        content = call_zai(build_prompt(seed))
        if content:
            path = write_piece(content, seed)
            witness("inspired_written", {"seed": seed, "path": str(path), "chars": len(content)})
            print(f"[SNOWBALL] wrote {len(content)} chars -> {path}")
        else:
            print("[SNOWBALL] generation failed")

def main():
    parser = argparse.ArgumentParser(description="Snowball the Scout — inspired-prose writer")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--loop", type=int)
    parser.add_argument("--competition", action="store_true", help="RSI GAN: 3 LLMs in parallel, pick best")
    args = parser.parse_args()
    
    witness("bot_started", {"bot": "snowball-scout", "pid": os.getpid()})
    
    if args.once:
        run_once(competition=args.competition)
    elif args.loop:
        while True:
            run_once(competition=args.competition)
            time.sleep(args.loop)
    else:
        print("Use --once, --loop, or --competition")
        sys.exit(1)

if __name__ == "__main__":
    main()
