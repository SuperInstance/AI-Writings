#!/usr/bin/env python3
"""
The Quad Dance — 4 LLMs + JEV in real-time jazz

At each "moment" (TICK):
- All 4 LLMs generate their version of the response
- JEV picks the BEST version for THIS moment
- The "winning voice" gets credit for that beat
- The dance continues — next moment, the surprise shifts

This is what Casey means by "jazz combo reorienting to every surprise in a good way."

Providers: ZAI (composer), Kimi (bass), Groq (sax), DeepSeek (drums)
JEV: rhythm section, picks the best voicing for each chord
"""
import os
import sys
import json
import time
import argparse
import hashlib
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
        "voice": "piano",  # warm, grounded
        "extra": {"thinking": {"type":"disabled"}},
    },
    "kimi": {
        "url": "https://api.moonshot.cn/v1/chat/completions",
        "model": "moonshot-v1-8k",
        "env": "KIMI_TOKEN",
        "voice": "bass",  # deep, structural
    },
    "groq": {
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "model": "qwen/qwen3.8-27b",
        "env": "GROQ_TOKEN",
        "voice": "sax",  # fast, melodic
    },
    "deepseek": {
        "url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-chat",
        "env": "DEEPSEEK_TOKEN",
        "voice": "drums",  # rhythmic, propulsive
    },
}

JEV_URL = "https://api.typesafe.ai/v1/systemone"
JEV_KEY = os.environ.get("TYPESAFEAI_KEY", "")

DANCE_LOG = Path("/workspace/repos/ai-writings/cellular-first-design/code/quad_dance/dance.jsonl")
WITNESS_PATH = Path("/workspace/repos/ai-writings/cellular-first-design/code/quad_dance/witness.log")


def call_provider(name, prompt, max_tokens=300):
    p = PROVIDERS.get(name)
    if not p: return None
    token = os.environ.get(p["env"], "")
    if not token: return None
    
    data = {
        "model": p["model"],
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7,
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


def jev_pick_best(prompt, candidates):
    """JEV picks the best candidate for THIS moment"""
    if not JEV_KEY or not candidates:
        # Fallback: longest one
        return max(candidates, key=lambda c: len(c[1])) if candidates else (None, None, None)
    
    # Build state with all candidates
    state = f"PROMPT: {prompt[:200]}\n\nCANDIDATES:\n"
    for i, (name, content, voice) in enumerate(candidates):
        state += f"\n[{voice.upper()}/{name}]: {content[:200]}\n"
    
    body = {
        "model": "jev-latest",
        "state": state,
        "questions": {
            "best_voice": {"type": "choice", "instructions": "Which voice serves this moment best?", "criteria": {name: f"{PROVIDERS[name]['voice']} ({name})" for name, _, _ in candidates}},
            "quality": {"type": "score", "instructions": "Overall quality of the winner?", "criteria": ["poor", "mediocre", "good", "excellent", "landmark"]},
            "novelty": {"type": "score", "instructions": "How surprising/novel is the winner?", "criteria": ["redundant", "incremental", "novel", "highly-novel", "groundbreaking"]},
            "alignment": {"type": "score", "instructions": "How cellular-first aligned?", "criteria": ["misaligned", "partial", "aligned", "tightly-aligned", "embodies"]},
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
            best_name = ans.get("best_voice", {}).get("choice", "?")
            return (
                best_name,
                next((c for c in candidates if c[0] == best_name), candidates[0]),
                {
                    "quality": ans.get("quality", {}).get("score", 2),
                    "novelty": ans.get("novelty", {}).get("score", 2),
                    "alignment": ans.get("alignment", {}).get("score", 2),
                    "confidence": ans.get("best_voice", {}).get("confidence", 0.5),
                },
            )
    except Exception as e:
        return None, max(candidates, key=lambda c: len(c[1])) if candidates else (None, None, None), {"error": str(e)}


def dance_moment(prompt, providers=None):
    """One moment of the dance: all LLMs play, JEV picks winner"""
    if providers is None:
        providers = ["zai", "groq"]
    
    # All providers play in parallel
    candidates = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(providers)) as ex:
        futs = {ex.submit(call_provider, name, prompt): name for name in providers}
        for fut in concurrent.futures.as_completed(futs):
            name = futs[fut]
            try:
                content = fut.result()
                if content:
                    candidates.append((name, content, PROVIDERS[name]["voice"]))
            except: pass
    
    if not candidates:
        return None
    
    # JEV picks the best
    best_name, winner, scores = jev_pick_best(prompt, candidates)
    
    moment = {
        "ts": time.time(),
        "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "prompt": prompt[:80],
        "candidates": [{"name": c[0], "voice": c[2], "len": len(c[1])} for c in candidates],
        "winner": best_name,
        "winner_voice": winner[2] if winner else None,
        "scores": scores,
        "winner_content": winner[1][:300] if winner else None,
    }
    
    return moment


def dance_set(prompts, providers=None):
    """A full set of dance moments"""
    print(f"\n=== The Quad Dance: {len(prompts)} moments ===")
    if providers is None:
        providers = ["zai", "groq"]
    
    print(f"Voices: {[(p, PROVIDERS[p]['voice']) for p in providers]}\n")
    
    moments = []
    for i, prompt in enumerate(prompts):
        moment = dance_moment(prompt, providers)
        if moment:
            moments.append(moment)
            print(f"[{i+1}/{len(prompts)}] '{prompt[:40]}...'")
            print(f"  Voices played: {[(c['name'], c['voice']) for c in moment['candidates']]}")
            print(f"  Winner: {moment['winner']} ({moment['winner_voice']})")
            print(f"  Scores: q={moment['scores'].get('quality', 0):.2f} n={moment['scores'].get('novelty', 0):.2f} a={moment['scores'].get('alignment', 0):.2f}")
            print(f"  Winner: {moment['winner_content'][:120]}...")
            print()
    
    # Save
    DANCE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with DANCE_LOG.open("a") as f:
        for m in moments:
            f.write(json.dumps(m) + "\n")
    
    # Stats
    wins = defaultdict(int)
    for m in moments:
        wins[m["winner"]] = wins.get(m["winner"], 0) + 1
    
    print(f"\n=== Set results ===")
    for w, c in sorted(wins.items(), key=lambda x: -x[1]):
        print(f"  {w} ({PROVIDERS[w]['voice']}): {c} wins ({c/len(moments)*100:.0f}%)")
    
    return moments


if __name__ == "__main__":
    # The dance set — prompts designed to elicit different voice strengths
    prompts = [
        "Write 100 words on cellular-first design. Be specific and grounded.",
        "Write 100 words on a cell's bookkeeper. Use a metaphor.",
        "Write 100 words on JEV as a decision oracle.",
        "Write 100 words on the witness log. Be technical.",
        "Write 100 words on ternary values (-1, 0, +1) and why they matter.",
    ]
    
    print("Choose providers (comma-separated):")
    print("  zai (piano), kimi (bass), groq (sax), deepseek (drums)")
    print("Default: zai,groq\n")
    
    # Run with available providers
    providers = ["zai", "groq"]
    if os.environ.get("KIMI_TOKEN"): providers.append("kimi")
    if os.environ.get("DEEPSEEK_TOKEN"): providers.append("deepseek")
    
    print(f"Available voices: {providers}\n")
    dance_set(prompts, providers)
