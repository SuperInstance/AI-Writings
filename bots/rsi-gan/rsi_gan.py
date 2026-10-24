#!/usr/bin/env python3
"""
RSI GAN Harness — Competitive Iterative Improvement

The "Recursive Self-Improvement GAN" pattern:
- N LLMs compete on the same prompt
- Each produces K candidates
- JEV rates each candidate (quality, novelty, alignment)
- Best K candidates seed next round
- Iterate M rounds

Output: highest-JEV-rated piece across all rounds.

Usage:
    python3 rsi_gan.py "Write 250 words on cellular-first design"
    python3 rsi_gan.py --prompt "..." --rounds 5 --providers zai,groq,deepinfra
"""
import os
import sys
import json
import time
import argparse
import hashlib
import concurrent.futures
import urllib.request
from pathlib import Path

# === Config ===
PROMPT_DEFAULT = "Write a 250-word prose piece on cellular-first design."

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

WITNESS_PATH = Path("/workspace/repos/ai-writings/bots/rsi-gan/witness.log")
RESULTS_PATH = Path("/workspace/repos/ai-writings/bots/rsi-gan/results.jsonl")
BOOKKEEPER_PATH = Path("/workspace/repos/ai-writings/bots/rsi-gan/bookkeeper.wal")

SUBSTRATE_VOCAB = [
    "cell", "witness", "bookkeeper", "proof", "scar", "hook", "drop",
    "BIND", "LINK", "EFFECT", "VIEW", "TICK", "FORGET",
    "ternary", "conservation", "fleet-clock", "JEPA", "JEV", "substrate",
    "fabric", "entanglement", "viability", "5-laws",
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

def call_provider(name, prompt, max_tokens=400):
    p = PROVIDERS[name]
    token = os.environ.get(p["env"], "")
    if not token:
        return None
    
    data = {
        "model": p["model"],
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.85,
    }
    data.update(p.get("extra", {}))
    
    req = urllib.request.Request(
        p["url"],
        data=json.dumps(data).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            r = json.loads(resp.read().decode())
            return r["choices"][0]["message"]["content"]
    except Exception as e:
        return None

def jev_score(content, prompt):
    """Rate content via JEV"""
    if not JEV_KEY or not content:
        # Fallback heuristic
        words = content.split() if content else []
        vocab_hits = sum(1 for w in words if any(v.lower() in w.lower() for v in SUBSTRATE_VOCAB))
        return {
            "quality": min(4, len(words) / 100 + vocab_hits * 0.3),
            "novelty": 1.5,
            "alignment": min(4, vocab_hits * 0.5),
            "confidence": 0.3,
            "source": "fallback",
        }
    
    state = f"PROMPT: {prompt[:300]}\n\nCONTENT: {content[:600]}"
    body = {
        "model": "jev-latest",
        "state": state,
        "questions": {
            "quality": {"type": "score", "instructions": "How high is the quality?", "criteria": ["poor","mediocre","good","excellent","landmark"]},
            "novelty": {"type": "score", "instructions": "How novel vs typical AI writing?", "criteria": ["redundant","incremental","novel","highly-novel","groundbreaking"]},
            "alignment": {"type": "score", "instructions": "How aligned with cellular-first substrate?", "criteria": ["misaligned","partial","aligned","tightly-aligned","embodies-doctrine"]},
        },
    }
    req = urllib.request.Request(
        JEV_URL,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {JEV_KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            r = json.loads(resp.read().decode())
            ans = r.get("answers", {})
            return {
                "quality": ans.get("quality", {}).get("score", {}).get("level", 2) if isinstance(ans.get("quality", {}).get("score"), dict) else ans.get("quality", {}).get("score", 2),
                "novelty": ans.get("novelty", {}).get("score", {}).get("level", 2) if isinstance(ans.get("novelty", {}).get("score"), dict) else ans.get("novelty", {}).get("score", 2),
                "alignment": ans.get("alignment", {}).get("score", {}).get("level", 2) if isinstance(ans.get("alignment", {}).get("score"), dict) else ans.get("alignment", {}).get("score", 2),
                "confidence": ans.get("quality", {}).get("confidence", 0.5),
                "source": "jev",
            }
    except Exception as e:
        return {"quality": 1.0, "novelty": 1.0, "alignment": 1.0, "confidence": 0.0, "source": f"jev_failed:{e}"}

def rsi_gan(prompt, providers, rounds=3):
    """RSI GAN: N providers x K candidates x R rounds"""
    print(f"[RSI GAN] prompt='{prompt[:60]}...' providers={providers} rounds={rounds}")
    
    best_overall = None
    best_score = 0
    
    # Round 1: initial generation
    candidates = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(providers)) as ex:
        futs = {ex.submit(call_provider, name, prompt): name for name in providers}
        for fut in concurrent.futures.as_completed(futs):
            name = futs[fut]
            try:
                content = fut.result()
                if content:
                    score = jev_score(content, prompt)
                    candidates.append({"provider": name, "content": content, "round": 1, **score})
                    print(f"  [{name}] q={score['quality']:.1f} n={score['novelty']:.1f} a={score['alignment']:.1f} src={score['source']}")
            except Exception as e:
                print(f"  [{name}] FAILED: {e}")
    
    # Rate and rank
    candidates.sort(key=lambda c: (c["quality"] + c["novelty"] + c["alignment"]) / 3, reverse=True)
    
    # Iterative improvement rounds
    for r in range(2, rounds + 1):
        # Top-K seed next round with feedback
        top = candidates[:max(1, len(providers) // 2)]
        if not top:
            break
        feedback = "\n\n".join(
            f"[{c['provider']}, q={c['quality']:.1f}]\n{c['content'][:200]}"
            for c in top[:2]
        )
        improved_prompt = f"""{prompt}

INSPIRATION FROM PRIOR ROUND:
{feedback}

Write something better. More specific. More grounded. Use cellular-first vocabulary."""
        
        new_candidates = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(providers)) as ex:
            futs = {ex.submit(call_provider, name, improved_prompt): name for name in providers}
            for fut in concurrent.futures.as_completed(futs):
                name = futs[fut]
                try:
                    content = fut.result()
                    if content:
                        score = jev_score(content, prompt)
                        new_candidates.append({"provider": name, "content": content, "round": r, **score})
                        print(f"  [r{r} {name}] q={score['quality']:.1f} n={score['novelty']:.1f} a={score['alignment']:.1f} src={score['source']}")
                except Exception as e:
                    print(f"  [r{r} {name}] FAILED: {e}")
        
        candidates.extend(new_candidates)
        candidates.sort(key=lambda c: (c["quality"] + c["novelty"] + c["alignment"]) / 3, reverse=True)
    
    # Pick best
    best = candidates[0] if candidates else None
    if best:
        avg = (best["quality"] + best["novelty"] + best["alignment"]) / 3
        if avg > best_score:
            best_overall = best
    
    # Save results
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("a") as f:
        f.write(json.dumps({
            "ts": time.time(),
            "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "prompt": prompt,
            "rounds": rounds,
            "providers": providers,
            "best": best,
            "all_candidates_count": len(candidates),
        }) + "\n")
    
    witness("rsi_gan_complete", {
        "prompt": prompt[:80],
        "rounds": rounds,
        "best_provider": best["provider"] if best else None,
        "best_quality": best["quality"] if best else 0,
    })
    
    return best

def main():
    parser = argparse.ArgumentParser(description="RSI GAN — competitive iterative LLM improvement")
    parser.add_argument("prompt", nargs="?", default=PROMPT_DEFAULT)
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--providers", default="zai,groq,deepinfra")
    args = parser.parse_args()
    
    witness("rsi_gan_started", {"prompt": args.prompt[:80], "rounds": args.rounds, "providers": args.providers})
    
    providers = [p.strip() for p in args.providers.split(",") if p.strip() in PROVIDERS]
    if not providers:
        providers = ["zai", "groq"]
    

    
    best = rsi_gan(args.prompt, providers, args.rounds)
    
    if best:
        print(f"\n=== BEST ({best['provider']}, r{best['round']}) ===")
        print(f"Quality={best['quality']:.2f} Novelty={best['novelty']:.2f} Alignment={best['alignment']:.2f}")
        print(f"\n{best['content']}")

if __name__ == "__main__":
    main()
