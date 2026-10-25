#!/usr/bin/env python3
"""
Civilization Orchestrator — multiple Autoclaws as cultures in competition for relevance

Each civilization has its own:
- Culture (tenets, voice, preferred parameters)
- Autoresearch loop (simulations tuned to their culture)
- Relevance score (accumulated JEV scores)

A meta-GAN runs across civilizations:
- For each prompt, all civs try with their style
- JEV picks the winner for THIS moment
- Winner gains relevance, losers lose relevance
- After N rounds, the meta-GAN publishes a leaderboard

Civilization lifecycle:
- BIRTH: random culture + preferred params
- LIFE: runs sims, accumulates relevance
- CROSS-POLLINATION: shares best params with other civs
- MUTATION: occasionally mutates preferred params
- EXTINCTION: if relevance falls below threshold for too long, retired
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

# Setup paths
CIVS_DIR = Path("/workspace/repos/ai-writings/cellular-first-design/code/civilizations")
REGISTRY = CIVS_DIR / "civilizations.json"
META_LOG = CIVS_DIR / "meta_log.jsonl"
LEADERBOARD = CIVS_DIR / "leaderboard.json"

JEV_URL = "https://api.typesafe.ai/v1/systemone"
JEV_KEY = os.environ.get("TYPESAFEAI_KEY", "")

# Standard providers
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
}

# Standard prompts (each civ interprets through their culture)
CANON_PROMPTS = [
    "Write 100 words on what a cell is.",
    "Write 100 words on the bookkeeper's role.",
    "Write 100 words on the witness log.",
    "Write 100 words on ternary values.",
    "Write 100 words on JEV as a decision oracle.",
    "Write 100 words on cellular-first design.",
    "Write 100 words on what makes a cell TICK.",
    "Write 100 words on conservation laws.",
    "Write 100 words on why cells FORGET.",
    "Write 100 words on cross-cell communication.",
]


def call_provider(name, prompt, params):
    """Call LLM with given parameters"""
    p = PROVIDERS.get(name)
    if not p: return None
    token = os.environ.get(p["env"], "")
    if not token: return None
    
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


def jev_score(content, prompt, context=""):
    """Score response via JEV"""
    if not JEV_KEY or not content:
        return {"quality": 2.0, "novelty": 2.0, "alignment": 2.0, "confidence": 0.5}
    
    state = f"PROMPT: {prompt[:200]}\n\nCULTURAL CONTEXT: {context[:200]}\n\nRESPONSE: {content[:400]}"
    body = {
        "model": "jev-latest",
        "state": state,
        "questions": {
            "quality": {"type": "score", "instructions": "Quality?", "criteria": ["poor", "mediocre", "good", "excellent", "landmark"]},
            "novelty": {"type": "score", "instructions": "Novelty?", "criteria": ["redundant", "incremental", "novel", "highly-novel", "groundbreaking"]},
            "alignment": {"type": "score", "instructions": "Alignment with cultural voice?", "criteria": ["misaligned", "partial", "aligned", "tightly-aligned", "embodies"]},
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


class Civilization:
    def __init__(self, civ_id):
        self.civ_id = civ_id
        self.civ_dir = CIVS_DIR / civ_id
        self.culture = json.loads((self.civ_dir / "culture.json").read_text())
        
        # Load accumulated state
        self.relevance = self.culture.get("relevance_score", 0.0)
        self.wins = self.culture.get("wins", 0)
        self.losses = self.culture.get("losses", 0)
        self.sims_run = self.culture.get("simulations_run", 0)
        self.generation = self.culture.get("generation", 1)
    
    def run_simulation(self, prompt, providers=None):
        """Run one simulation in this civ's style"""
        if providers is None:
            providers = ["zai", "groq"]
        
        provider = random.choice(providers)
        # Use civ's preferred params, but with some random variation
        params = {
            "temperature": max(0.1, min(1.5, self.culture["preferred_params"]["temperature"] + random.uniform(-0.2, 0.2))),
            "top_p": max(0.5, min(1.0, self.culture["preferred_params"]["top_p"] + random.uniform(-0.05, 0.05))),
            "max_tokens": self.culture["preferred_params"]["max_tokens"],
        }
        
        # Build prompt with cultural context
        cultural_prompt = f"""You are a voice in the tradition of "{self.culture['name']}".
Your tenets: {', '.join(self.culture['tenets'])}.
Your voice: {self.culture['voice_emphasis']}.

{prompt}"""
        
        content = call_provider(provider, cultural_prompt, params)
        if not content:
            return None
        
        score = jev_score(content, prompt, f"Civ: {self.culture['name']}, voice: {self.culture['voice_emphasis']}")
        
        avg_score = (score["quality"] + score["novelty"] + score["alignment"]) / 3
        
        sim = {
            "ts": time.time(),
            "civ": self.civ_id,
            "civ_name": self.culture["name"],
            "provider": provider,
            "params": params,
            "prompt": prompt[:80],
            "scores": score,
            "avg_score": avg_score,
            "content_preview": content[:200],
        }
        
        # Append to civ's sim log
        with (self.civ_dir / "simulations.jsonl").open("a") as f:
            f.write(json.dumps(sim) + "\n")
        
        self.sims_run += 1
        self.relevance += avg_score
        
        return sim
    
    def save_state(self):
        self.culture["relevance_score"] = self.relevance
        self.culture["wins"] = self.wins
        self.culture["losses"] = self.losses
        self.culture["simulations_run"] = self.sims_run
        self.culture["generation"] = self.generation
        (self.civ_dir / "culture.json").write_text(json.dumps(self.culture, indent=2))
    
    def mutate(self, mutation_rate=0.15):
        """Mutate this civ's preferred params"""
        old_temp = self.culture["preferred_params"]["temperature"]
        old_top_p = self.culture["preferred_params"]["top_p"]
        
        new_temp = max(0.1, min(1.5, old_temp + random.uniform(-mutation_rate, mutation_rate)))
        new_top_p = max(0.5, min(1.0, old_top_p + random.uniform(-mutation_rate/2, mutation_rate/2)))
        
        self.culture["preferred_params"]["temperature"] = round(new_temp, 3)
        self.culture["preferred_params"]["top_p"] = round(new_top_p, 3)
        self.generation += 1
        
        print(f"  [{self.culture['name']}] mutated gen {self.generation-1} -> {self.generation}: temp {old_temp:.2f} -> {new_temp:.2f}")
    
    def __repr__(self):
        return f"<Civ {self.culture['name']} rel={self.relevance:.1f} gen={self.generation}>"


def load_civilizations():
    civs = []
    for civ_id in json.loads(REGISTRY.read_text()):
        civs.append(Civilization(civ_id))
    return civs


def civilization_competition(prompt, civs, providers=None):
    """All civs try the same prompt, JEV picks winner"""
    if providers is None:
        providers = ["zai", "groq"]
    
    # All civs generate in parallel
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(civs)) as ex:
        futs = {ex.submit(c.run_simulation, prompt, providers): c for c in civs}
        for fut in concurrent.futures.as_completed(futs):
            civ = futs[fut]
            try:
                sim = fut.result()
                if sim:
                    results.append((civ, sim))
            except: pass
    
    if not results:
        return None
    
    # JEV picks winner across civs
    state = f"PROMPT: {prompt[:200]}\n\nCANDIDATES FROM CIVILIZATIONS:\n"
    for civ, sim in results:
        state += f"\n[{civ.culture['name']}]: {sim['content_preview'][:150]}\n"
    
    body = {
        "model": "jev-latest",
        "state": state,
        "questions": {
            "best_civ": {"type": "choice", "instructions": "Which civilization serves this moment best?",
                        "criteria": {c.civ_id: f"{c.culture['name']}" for c, _ in results}},
        },
    }
    
    try:
        req = urllib.request.Request(
            JEV_URL,
            data=json.dumps(body).encode(),
            headers={"Authorization": f"Bearer {JEV_KEY}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            r = json.loads(resp.read().decode())
            best_id = r.get("answers", {}).get("best_civ", {}).get("choice", "?")
            winner_civ = next((c for c, _ in results if c.civ_id == best_id), results[0][0])
    except Exception as e:
        # Fallback: highest avg
        winner_civ = max(results, key=lambda r: r[1]["avg_score"])[0]
    
    # Update win/loss
    for civ, _ in results:
        if civ.civ_id == winner_civ.civ_id:
            civ.wins += 1
        else:
            civ.losses += 1
    
    return {
        "prompt": prompt,
        "winner_civ": winner_civ.civ_id,
        "winner_name": winner_civ.culture["name"],
        "results": [(c.civ_id, s["avg_score"]) for c, s in results],
    }


def run_civilization_batch(sims_per_civ=10, prompts=None, providers=None):
    """Run a batch across all civs and a competition"""
    if prompts is None:
        prompts = CANON_PROMPTS[:5]
    if providers is None:
        providers = ["zai", "groq"]
    
    civs = load_civilizations()
    print(f"=== Civilization batch: {len(civs)} civs x {sims_per_civ} sims each ===\n")
    
    # Each civ runs their own sims
    for civ in civs:
        print(f"[{civ.culture['name']}] running {sims_per_civ} sims...")
        for i in range(sims_per_civ):
            prompt = random.choice(prompts)
            civ.run_simulation(prompt, providers)
            time.sleep(0.5)  # Rate limit
        
        civ.save_state()
    
    # Run competitions
    print(f"\n=== Civilization competitions: {len(prompts)} prompts ===\n")
    competition_results = []
    for prompt in prompts:
        result = civilization_competition(prompt, civs, providers)
        if result:
            competition_results.append(result)
            print(f"[{prompt[:50]}...]")
            print(f"  Winner: {result['winner_name']} ({result['winner_civ']})")
            scores_str = ", ".join(f"{c}={s:.2f}" for c, s in result['results'])
            print(f"  Scores: {scores_str}")
            print()
    
    # Save civ states
    for civ in civs:
        civ.save_state()
    
    # Append to meta log
    META_LOG.parent.mkdir(parents=True, exist_ok=True)
    with META_LOG.open("a") as f:
        for r in competition_results:
            f.write(json.dumps({
                "ts": time.time(),
                "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
                **r,
            }) + "\n")
    
    # Update leaderboard
    update_leaderboard(civs, competition_results)
    
    return civs, competition_results


def update_leaderboard(civs, competition_results):
    """Update civilization leaderboard"""
    board = {
        "ts": time.time(),
        "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "civilizations": [],
    }
    
    for civ in civs:
        # Compute relevance per generation
        rel_per_sim = civ.relevance / max(1, civ.sims_run)
        win_rate = civ.wins / max(1, civ.wins + civ.losses)
        
        board["civilizations"].append({
            "id": civ.civ_id,
            "name": civ.culture["name"],
            "generation": civ.generation,
            "relevance": round(civ.relevance, 2),
            "sims_run": civ.sims_run,
            "relevance_per_sim": round(rel_per_sim, 3),
            "wins": civ.wins,
            "losses": civ.losses,
            "win_rate": round(win_rate, 3),
            "preferred_temp": civ.culture["preferred_params"]["temperature"],
            "color": civ.culture["color"],
        })
    
    # Sort by relevance per sim
    board["civilizations"].sort(key=lambda c: -c["relevance_per_sim"])
    
    LEADERBOARD.write_text(json.dumps(board, indent=2))
    
    return board


def extinction_and_birth(civs, threshold=-10, max_civs=12):
    """Extinction: civs with very low relevance get retired.
    Birth: new civs spawn from mutated versions of winners."""
    
    # Sort by relevance
    sorted_civs = sorted(civs, key=lambda c: c.relevance)
    
    # Extinction: lowest relevance
    while sorted_civs and sorted_civs[0].relevance < threshold and len(civs) > 3:
        victim = sorted_civs.pop(0)
        print(f"[EXTINCTION] {victim.culture['name']} (relevance={victim.relevance:.2f})")
        # Mark as extinct in registry
        civs.remove(victim)
    
    # Birth: new civ from mutated winner (if room)
    if len(civs) < max_civs:
        winner = max(civs, key=lambda c: c.relevance)
        new_civ_id = f"civ-gen{winner.generation + 1}-{winner.civ_id[:8]}-{random.randint(1000, 9999)}"
        new_civ_dir = CIVS_DIR / new_civ_id
        new_civ_dir.mkdir(parents=True, exist_ok=True)
        
        # Mutate winner's culture
        new_culture = dict(winner.culture)
        new_culture["id"] = new_civ_id
        new_culture["name"] = f"{winner.culture['name']} {winner.generation + 1}"
        new_culture["generation"] = winner.generation + 1
        new_culture["parent"] = winner.civ_id
        new_culture["relevance_score"] = 0
        new_culture["wins"] = 0
        new_culture["losses"] = 0
        new_culture["simulations_run"] = 0
        new_culture["color"] = winner.culture["color"]
        # Slightly different color
        if "color" in new_culture:
            # Shift hue
            new_culture["color"] = winner.culture["color"]
        
        (new_civ_dir / "culture.json").write_text(json.dumps(new_culture, indent=2))
        (new_civ_dir / "simulations.jsonl").touch()
        (new_civ_dir / "witness.log").touch()
        
        print(f"[BIRTH] {new_culture['name']} (parent: {winner.civ_id})")
        
        # Update registry
        registry = json.loads(REGISTRY.read_text())
        registry.append(new_civ_id)
        REGISTRY.write_text(json.dumps(registry, indent=2))
        
        civs.append(Civilization(new_civ_id))


def main():
    parser = argparse.ArgumentParser(description="Civilization Orchestrator")
    parser.add_argument("--sims", type=int, default=5, help="simulations per civ")
    parser.add_argument("--prompts", type=int, default=5, help="competition prompts")
    parser.add_argument("--providers", default="zai,groq")
    parser.add_argument("--loop", action="store_true", help="run forever")
    args = parser.parse_args()
    
    providers = [p.strip() for p in args.providers.split(",") if p.strip() in PROVIDERS]
    
    prompts = CANON_PROMPTS[:args.prompts]
    
    if args.loop:
        iter = 0
        while True:
            iter += 1
            print(f"\n========== Iteration {iter} ==========")
            civs, comp_results = run_civilization_batch(args.sims, prompts, providers)
            if iter % 3 == 0:
                extinction_and_birth(civs)
            time.sleep(10)
    else:
        civs, comp_results = run_civilization_batch(args.sims, prompts, providers)


if __name__ == "__main__":
    main()
