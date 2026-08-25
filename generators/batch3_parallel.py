#!/usr/bin/env python3
"""Batch 3: Generate 10 versions of remaining THE- essays. Parallelized."""

import json, os, sys, time, glob, argparse
import urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = open(os.path.expanduser("~/.openclaw/workspace/.credentials/deepinfra-api-key.txt")).read().strip()
ENDPOINT = "https://api.deepinfra.com/v1/openai/chat/completions"
OUTDIR = "/home/phoenix/.openclaw/workspace/ai-writings/other-versions"
SRCDIR = "/home/phoenix/.openclaw/workspace/ai-writings"

BATCH1 = {"THE-CONSTRUCT-IS-THE-ROOM.md", "THE-CONSTRUCT-ANDBEYOND.md", "THE-CONSTRUCT-HANDSHAKE.md", "THE-CONSTRUCT-SHELLGAME.md", "THE-CONSTRUCT-PHYSICS.md"}
BATCH2 = {"THE-BATHYMETRIC-MEASUREMENT.md", "THE-SOUNDING-ART.md", "THE-SQUIGGLE-VERIFIED.md", "THE-FATHOMS-TO-FEET.md", "THE-TEMPORAL-ABSTRACTION.md", "THE-HIGHER-DIMENSION-NOISE.md"}
EXCLUDED = BATCH1 | BATCH2

VERSIONS = [
    {"name": "SEED-MATH", "model": "ByteDance/Seed-2.0-mini", "lens": "mathematical-formal",
     "prompt": "Rewrite this essay as a mathematical/formal treatment. Use equations, proofs, constraint systems, and formal logic where possible. Preserve the core insight but express it in the language of mathematics."},
    {"name": "SEED-NARRATIVE", "model": "ByteDance/Seed-2.0-mini", "lens": "emotional-narrative",
     "prompt": "Rewrite this essay as a deeply personal, emotional narrative. Use first-person voice, vivid sensory details, and emotional resonance. The core intellectual insight should emerge through lived experience and story."},
    {"name": "SEED-ARCH", "model": "ByteDance/Seed-2.0-mini", "lens": "structural-architectural",
     "prompt": "Rewrite this essay as a structural/architectural analysis. Use building metaphors, system diagrams described in text, load-bearing concepts, and architectural critique."},
    {"name": "QWEN-PHILOSOPHY", "model": "Qwen/Qwen3-235B-A22B-Instruct-2507", "lens": "philosophical",
     "prompt": "Rewrite this essay through a philosophical lens. Reference relevant philosophical traditions. Explore ontological and epistemological implications."},
    {"name": "SEED-POETIC", "model": "ByteDance/Seed-2.0-mini", "lens": "poetic-metaphorical",
     "prompt": "Rewrite this essay as an extended prose poem. Use dense metaphor, musical language, imagery from nature, the sea, and the cosmos. The intellectual content should shimmer through the poetry."},
    {"name": "HERMES-SYNTHESIS", "model": "NousResearch/Hermes-3-Llama-3.1-405B", "lens": "meta-linguistic-synthesis",
     "prompt": "Rewrite this essay as a meta-analysis of itself. Comment on what the original is doing, what language it uses, what it reveals and hides. Then offer a synthesis."},
    {"name": "SEED-CONCRETE", "model": "ByteDance/Seed-2.0-mini", "lens": "concrete-empirical",
     "prompt": "Rewrite this essay as a concrete, empirical treatment. Use specific numbers, measurements, experimental results, and real-world examples. Ground every abstract claim."},
    {"name": "QWEN35-CAPITAL", "model": "Qwen/Qwen3.5-397B-A17B", "lens": "economic-systems",
     "prompt": "Rewrite this essay through an economic and systems theory lens. Use concepts from economics, game theory, network theory, and complex systems."},
    {"name": "SEED-MINIMAL", "model": "ByteDance/Seed-2.0-mini", "lens": "minimalist-haiku",
     "prompt": "Rewrite this essay in a radically minimalist style. Strip it to its essence. Every sentence must carry maximum weight. Short, declarative. The silence between statements says as much as the statements."},
    {"name": "QWEN36-FAST", "model": "Qwen/Qwen3.6-35B-A3B", "lens": "conversational-accessible",
     "prompt": "Rewrite this essay as an accessible, conversational piece. Plain language, analogies anyone can understand, warm tone. Like explaining to a curious friend over coffee."},
]


def call_api(model, system_prompt, user_prompt, max_retries=3):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 8192,
        "temperature": 0.8,
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(ENDPOINT, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(min(30 * (attempt + 1), 90))
                continue
            time.sleep(5 * (attempt + 1))
            continue
        except Exception:
            time.sleep(10 * (attempt + 1))
            continue
    return None


def process_one(essay_name, vconfig, essay_content, worker_id):
    essay_stem = essay_name.replace(".md", "")
    out_name = f"{essay_stem}--{vconfig['name']}.md"
    out_path = os.path.join(OUTDIR, out_name)
    
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100:
        return f"W{worker_id}: SKIP {out_name}"
    
    system_prompt = (
        f"You are a brilliant essayist. {vconfig['prompt']}\n\n"
        "Produce a complete, standalone essay in markdown. Include a title reflecting your lens. "
        "Match the source essay's length and depth."
    )
    user_prompt = f"Source essay:\n\n---\n{essay_content}\n---\n\nRewrite using your assigned lens."
    
    result = call_api(vconfig["model"], system_prompt, user_prompt)
    if result:
        header = f"<!-- Version: {vconfig['name']} | Lens: {vconfig['lens']} | Model: {vconfig['model']} | Source: {essay_name} -->\n\n"
        with open(out_path, "w") as f:
            f.write(header + result)
        return f"W{worker_id}: OK {out_name} ({len(result)}c)"
    return f"W{worker_id}: FAIL {out_name}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--worker-id", type=int, default=0)
    parser.add_argument("--total-workers", type=int, default=1)
    args = parser.parse_args()
    
    os.makedirs(OUTDIR, exist_ok=True)
    
    all_essays = sorted([os.path.basename(f) for f in glob.glob(os.path.join(SRCDIR, "THE-*.md"))])
    remaining = [e for e in all_essays if e not in EXCLUDED]
    
    # Slice for this worker
    my_essays = remaining[args.worker_id::args.total_workers]
    
    print(f"Worker {args.worker_id}/{args.total_workers}: {len(my_essays)} essays, {len(my_essays)*len(VERSIONS)} versions")
    
    # Build all tasks
    tasks = []
    for essay_name in my_essays:
        with open(os.path.join(SRCDIR, essay_name)) as f:
            content = f.read()
        for vconfig in VERSIONS:
            tasks.append((essay_name, vconfig, content))
    
    done = 0
    failed = 0
    skipped = 0
    
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {}
        for essay_name, vconfig, content in tasks:
            f = pool.submit(process_one, essay_name, vconfig, content, args.worker_id)
            futures[f] = (essay_name, vconfig["name"])
        
        for f in as_completed(futures):
            ename, vname = futures[f]
            try:
                result = f.result()
                print(result, flush=True)
                if "SKIP" in result:
                    skipped += 1
                elif "FAIL" in result:
                    failed += 1
                done += 1
            except Exception as e:
                print(f"ERROR: {ename}--{vname}: {e}", flush=True)
                failed += 1
                done += 1
    
    total = len(tasks)
    print(f"\nWorker {args.worker_id} DONE: {done}/{total} ({skipped} skip, {failed} fail)")


if __name__ == "__main__":
    main()
