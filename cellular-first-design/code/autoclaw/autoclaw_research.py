#!/usr/bin/env python3
"""
AutoClaw Autoresearch — runs in background, finds better numbers

Like Casey's vision: Autoclaw does autoresearch in the background.
JEV feeds cells the BEST numbers. The numbers improve over time.

This module:
1. Runs thousands of small simulations
2. Each simulation: random parameters -> generate response -> score via JEV
3. Track which parameters produce the best outcomes
4. Periodically publish improved "best parameters" to substrate

The dance:
- Many LLMs (ZAI/Kimi/Groq/DeepSeek) generate responses with varying parameters
- JEV scores each response on quality/novelty/alignment
- Best parameters are kept and shared across the substrate
"""
import os
import sys
import json
import time
import random
import hashlib
import argparse
import urllib.request
import concurrent.futures
from pathlib import Path
from collections import defaultdict

# === Config ===
PROVIDERS = {
    "zai": {
        "url": "https://api.z.ai/api/coding/paas/v4/chat/completions",
        "model": "glm-4.5",
        "env": "ZAI_TOKEN",
        "extra": {"thinking": {"type":"disabled"}},
    },
    "groq": {
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "model": "qwen/qwen3.8-27b",
        "env": "GROQ_TOKEN",
    },
    "deepinfra": {
        "url": "https://api.deepinfra.com/v1/openai/chat/completions",
        "model": "Qwen/Qwen3-235B-A22B-Instruct-2507",
        "env": "DEEPINFRA_TOKEN",
    },
    "deepseek": {
        "url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-chat",
        "env": "DEEPSEEK_TOKEN",
    },
}

JEV_URL = "https://api.typesafe.ai/v1/systemone"
JEV_KEY = os.environ.get("TYPESAFEAI_KEY", "")

RESULTS_DIR = Path("/workspace/repos/ai-writings/cellular-first-design/code/autoclaw")
SIMULATIONS_PATH = RESULTS_DIR / "simulations.jsonl"
BEST_PARAMS_PATH = RESULTS_DIR / "best_params.json"
WITNESS_PATH = RESULTS_DIR / "witness.log"


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


def call_provider(name, prompt, params):
    """Call LLM with given parameters"""
    p = PROVIDERS.get(name)
    if not p:
        return None
    
    token = os.environ.get(p["env"], "")
    if not token:
        return None
    
    data = {
        "model": p["model"],
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": params.get("max_tokens", 400),
        "temperature": params.get("temperature", 0.7),
        "top_p": params.get("top_p", 0.9),
    }
    data.update(p.get("extra", {}))
    
    req = urllib.request.Request(
        p["url"],
        data=json.dumps(data).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            r = json.loads(resp.read().decode())
            return r["choices"][0]["message"]["content"]
    except Exception as e:
        return None


def jev_score(content, prompt):
    """Score response via JEV"""
    if not JEV_KEY or not content:
        return {"quality": 2.0, "novelty": 2.0, "alignment": 2.0, "confidence": 0.5}
    
    state = f"PROMPT: {prompt[:200]}\n\nRESPONSE: {content[:400]}"
    body = {
        "model": "jev-latest",
        "state": state,
        "questions": {
            "quality": {"type": "score", "instructions": "Quality?", "criteria": ["poor", "mediocre", "good", "excellent", "landmark"]},
            "novelty": {"type": "score", "instructions": "Novelty?", "criteria": ["redundant", "incremental", "novel", "highly-novel", "groundbreaking"]},
            "alignment": {"type": "score", "instructions": "Cellular-first alignment?", "criteria": ["misaligned", "partial", "aligned", "tightly-aligned", "embodies"]},
        },
    }
    req = urllib.request.Request(
        JEV_URL,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {JEV_KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            r = json.loads(resp.read().decode())
            ans = r.get("answers", {})
            def g(k):
                s = ans.get(k, {}).get("score", 2.0)
                return s if isinstance(s, (int, float)) else s.get("level", 2.0) if isinstance(s, dict) else 2.0
            return {
                "quality": g("quality"),
                "novelty": g("novelty"),
                "alignment": g("alignment"),
                "confidence": ans.get("quality", {}).get("confidence", 0.5),
            }
    except Exception as e:
        return {"quality": 2.0, "novelty": 2.0, "alignment": 2.0, "confidence": 0.0, "error": str(e)}


# Parameter search space
PARAM_SPACE = [
    {"temperature": 0.3, "top_p": 0.9, "max_tokens": 300, "label": "conservative"},
    {"temperature": 0.7, "top_p": 0.9, "max_tokens": 300, "label": "balanced"},
    {"temperature": 0.9, "top_p": 0.95, "max_tokens": 300, "label": "creative"},
    {"temperature": 0.5, "top_p": 0.85, "max_tokens": 300, "label": "focused"},
    {"temperature": 1.0, "top_p": 0.9, "max_tokens": 300, "label": "exploratory"},
    {"temperature": 0.4, "top_p": 0.9, "max_tokens": 500, "label": "long_focused"},
    {"temperature": 0.8, "top_p": 0.9, "max_tokens": 500, "label": "long_balanced"},
    {"temperature": 0.6, "top_p": 0.95, "max_tokens": 300, "label": "diverse"},
]

PROMPTS = [
    "Write 100 words on what a cell is. Use cellular-first vocabulary.",
    "Write 100 words on how a bookkeeper works. Be specific.",
    "Write 100 words on the witness log. No AI-cliche phrases.",
    "Write 100 words on ternary values (-1, 0, +1). Use a concrete example.",
    "Write 100 words on JEV as a decision oracle. Be grounded.",
]


def run_one_sim(provider, prompt, params):
    """Run one simulation: provider + prompt + params -> JEV score"""
    content = call_provider(provider, prompt, params)
    if not content:
        return None
    score = jev_score(content, prompt)
    return {
        "provider": provider,
        "prompt": prompt[:80],
        "params": params,
        "content": content[:300],
        "score": score,
        "avg_score": (score["quality"] + score["novelty"] + score["alignment"]) / 3,
    }


def run_simulation_batch(n_simulations=50, providers=None):
    """Run N simulations across providers x prompts x params"""
    if providers is None:
        providers = ["zai", "groq"]
    
    sims = []
    tasks = []
    for _ in range(n_simulations):
        provider = random.choice(providers)
        prompt = random.choice(PROMPTS)
        params = random.choice(PARAM_SPACE)
        tasks.append((provider, prompt, params))
    
    print(f"[AUTOCLAW] running {n_simulations} simulations across {len(providers)} providers x {len(PROMPTS)} prompts x {len(PARAM_SPACE)} params")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(run_one_sim, t[0], t[1], t[2]): t for t in tasks}
        for fut in concurrent.futures.as_completed(futures):
            try:
                result = fut.result()
                if result:
                    sims.append(result)
            except Exception as e:
                pass
    
    # Save simulations
    SIMULATIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SIMULATIONS_PATH.open("a") as f:
        for s in sims:
            f.write(json.dumps(s) + "\n")
    
    # Find best parameters
    by_label = defaultdict(list)
    for s in sims:
        label = s["params"].get("label", "?")
        by_label[label].append(s["avg_score"])
    
    best_label = max(by_label, key=lambda l: sum(by_label[l])/len(by_label[l]) if by_label[l] else 0)
    
    best_params = {
        "best_label": best_label,
        "scores_by_label": {l: {"avg": sum(v)/len(v), "count": len(v)} for l, v in by_label.items()},
        "total_simulations": len(sims),
        "ts": time.time(),
    }
    
    BEST_PARAMS_PATH.write_text(json.dumps(best_params, indent=2))
    
    witness("simulation_batch", best_params)
    
    return best_params, sims


def find_best():
    """Read all simulations, find best parameters"""
    if not SIMULATIONS_PATH.exists():
        return None
    
    sims = []
    with SIMULATIONS_PATH.open() as f:
        for line in f:
            if line.strip():
                try:
                    sims.append(json.loads(line))
                except: pass
    
    if not sims:
        return None
    
    # Aggregate by param label
    by_label = defaultdict(list)
    by_provider = defaultdict(list)
    by_provider_label = defaultdict(list)
    
    for s in sims:
        label = s.get("params", {}).get("label", "?")
        provider = s.get("provider", "?")
        score = s.get("avg_score", 0)
        by_label[label].append(score)
        by_provider[provider].append(score)
        by_provider_label[f"{provider}|{label}"].append(score)
    
    return {
        "total": len(sims),
        "best_label": max(by_label, key=lambda l: sum(by_label[l])/len(by_label[l])) if by_label else "?",
        "best_provider": max(by_provider, key=lambda p: sum(by_provider[p])/len(by_provider[p])) if by_provider else "?",
        "by_label": {l: {"avg": sum(v)/len(v), "count": len(v)} for l, v in by_label.items()},
        "by_provider": {p: {"avg": sum(v)/len(v), "count": len(v)} for p, v in by_provider.items()},
        "by_provider_label": {k: {"avg": sum(v)/len(v), "count": len(v)} for k, v in by_provider_label.items()},
    }


def main():
    parser = argparse.ArgumentParser(description="AutoClaw Autoresearch")
    parser.add_argument("--batch", type=int, default=20, help="simulations per batch")
    parser.add_argument("--providers", default="zai,groq")
    parser.add_argument("--analyze", action="store_true", help="analyze existing simulations")
    args = parser.parse_args()
    
    witness("autoclaw_started", {"providers": args.providers, "batch": args.batch})
    
    if args.analyze:
        best = find_best()
        if best:
            print(json.dumps(best, indent=2))
        else:
            print("No simulations yet")
    else:
        providers = [p.strip() for p in args.providers.split(",") if p.strip() in PROVIDERS]
        if not providers:
            providers = ["zai", "groq"]
        
        best_params, sims = run_simulation_batch(args.batch, providers)
        
        print(f"\n=== Batch results ===")
        print(f"  Simulations run: {len(sims)}")
        print(f"  Best param label: {best_params['best_label']}")
        print(f"\n  Scores by label:")
        for l, s in sorted(best_params["scores_by_label"].items(), key=lambda x: -x[1]["avg"]):
            print(f"    {l}: avg={s['avg']:.2f} (n={s['count']})")


if __name__ == "__main__":
    main()
