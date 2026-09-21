#!/usr/bin/env python3
"""
Autoclaw Background Autoresearch — continuous improvement daemon

This is the "autoresearch happening in the background" that Casey described.
It runs forever, doing thousands of small experiments to find better
parameters for the substrate's cells.

Every N seconds:
1. Sample random params (temp/top_p/max_tokens) from search space
2. Call random LLM with random prompt
3. JEV scores the response
4. If better than best-so-far: publish to substrate bus, update best_params.json
5. Log to simulations.jsonl

The "best numbers for the time" are constantly refined.
"""
import os
import sys
import json
import time
import random
import argparse
import hashlib
import urllib.request
import concurrent.futures
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, "/workspace/repos/ai-writings/cellular-first-design/code/autoclaw")
from autoclaw_research import (
    call_provider, jev_score, PARAM_SPACE, PROMPTS,
    SIMULATIONS_PATH, BEST_PARAMS_PATH
)
sys.path.insert(0, "/workspace/repos/ai-writings/bots/substrate-bus")
try:
    from substrate_bus import publish as substrate_publish
    HAS_BUS = True
except:
    HAS_BUS = False

WITNESS_PATH = Path("/workspace/repos/ai-writings/bots/autoclaw-bg/witness.log")


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


def background_loop(batch_size=10, sleep_between=2, max_iterations=None, providers=None):
    """Run the autoresearch loop forever (or until max_iterations)"""
    if providers is None:
        providers = ["zai", "groq"]
    
    print(f"[AUTOCLAW-BG] Starting background autoresearch")
    print(f"  Batch size: {batch_size}")
    print(f"  Sleep: {sleep_between}s")
    print(f"  Providers: {providers}")
    print(f"  Max iterations: {max_iterations or 'forever'}")
    
    witness("background_started", {
        "batch_size": batch_size,
        "sleep_between": sleep_between,
        "providers": providers,
    })
    
    iteration = 0
    while max_iterations is None or iteration < max_iterations:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")
        
        # Sample random experiments
        sims = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as ex:
            futs = {}
            for _ in range(batch_size):
                provider = random.choice(providers)
                prompt = random.choice(PROMPTS)
                params = random.choice(PARAM_SPACE)
                futs[ex.submit(call_provider, provider, prompt, params)] = (provider, prompt, params)
            
            for fut in concurrent.futures.as_completed(futs):
                provider, prompt, params = futs[fut]
                try:
                    content = fut.result()
                    if content:
                        score = jev_score(content, prompt)
                        avg = (score["quality"] + score["novelty"] + score["alignment"]) / 3
                        sim = {
                            "ts": time.time(),
                            "provider": provider,
                            "prompt": prompt[:80],
                            "params": params,
                            "avg_score": avg,
                            "scores": score,
                            "content_preview": content[:200],
                        }
                        sims.append(sim)
                except: pass
        
        if sims:
            # Append to simulations log
            SIMULATIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
            with SIMULATIONS_PATH.open("a") as f:
                for s in sims:
                    f.write(json.dumps(s) + "\n")
            
            # Find new best
            best_sim = max(sims, key=lambda s: s["avg_score"])
            
            # Compare to existing best
            existing_best = 0
            if BEST_PARAMS_PATH.exists():
                try:
                    bp = json.loads(BEST_PARAMS_PATH.read_text())
                    existing_best = bp.get("best_avg_score", 0)
                except: pass
            
            print(f"  Simulations: {len(sims)}")
            print(f"  Best this batch: {best_sim['provider']} | {best_sim['params'].get('label', '?')} | avg={best_sim['avg_score']:.2f}")
            print(f"  All-time best: {existing_best:.2f}")
            
            if best_sim["avg_score"] > existing_best:
                # NEW BEST! Publish to bus
                new_best = {
                    "ts": time.time(),
                    "best_avg_score": best_sim["avg_score"],
                    "best_provider": best_sim["provider"],
                    "best_params": best_sim["params"],
                    "scores": best_sim["scores"],
                    "iteration": iteration,
                }
                BEST_PARAMS_PATH.write_text(json.dumps(new_best, indent=2))
                
                print(f"  *** NEW BEST PUBLISHED ***")
                
                if HAS_BUS:
                    try:
                        substrate_publish(
                            "best_params_updated",
                            "autoclaw-bg",
                            new_best,
                            recipients=["quilt-jev-bridge", "wesley-mechanic", "snowball-scout"],
                        )
                    except: pass
                
                witness("new_best_published", new_best)
        
        time.sleep(sleep_between)
    
    print(f"[AUTOCLAW-BG] Completed {iteration} iterations")
    witness("background_stopped", {"iterations": iteration})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autoclaw background autoresearch")
    parser.add_argument("--batch", type=int, default=10)
    parser.add_argument("--sleep", type=int, default=2)
    parser.add_argument("--max", type=int, help="max iterations")
    parser.add_argument("--providers", default="zai,groq")
    args = parser.parse_args()
    
    providers = [p.strip() for p in args.providers.split(",") if p.strip()]
    background_loop(args.batch, args.sleep, args.max, providers)
