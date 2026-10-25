#!/usr/bin/env python3
"""Batch rewrite 6 Bathymetric essays × 10 model voices = 60 files."""

import json, os, time, urllib.request, urllib.error, sys

API_KEY = open(os.path.expanduser("~/.openclaw/workspace/.credentials/deepinfra-api-key.txt")).read().strip()
ENDPOINT = "https://api.deepinfra.com/v1/openai/chat/completions"
OUTDIR = "/home/phoenix/.openclaw/workspace/ai-writings/bathymetric-versions"
INDIR = "/home/phoenix/.openclaw/workspace/ai-writings"

ESSAYS = [
    "THE-BATHYMETRIC-MEASUREMENT",
    "THE-SOUNDING-ART",
    "THE-SQUIGGLE-VERIFIED",
    "THE-FATHOMS-TO-FEET",
    "THE-TEMPORAL-ABSTRACTION",
    "THE-HIGHER-DIMENSION-NOISE",
]

VERSIONS = [
    # (suffix, model, system_prompt, temperature)
    ("v1-seed-2.0-mini", "ByteDance/Seed-2.0-mini",
     "You are rewriting this essay in your own voice. You are analytical, finding unexpected angles and non-obvious connections. Keep the core ideas but express them through your unique analytical perspective. 800-1500 words.", 0.7),
    ("v2-hermes-70b", "NousResearch/Hermes-3-Llama-3.1-70B",
     "You are rewriting this essay in your own voice. You are scholarly and methodical, building arguments step by step with academic rigor. Keep the core ideas but express them through your scholarly perspective. 800-1500 words.", 0.7),
    ("v3-qwen3.6-35b", "Qwen/Qwen3.6-35B-A3B",
     "You are rewriting this essay in your own voice. You blend poetic beauty with technical precision, using nature metaphors and lyrical language while remaining scientifically accurate. Keep the core ideas but express them through your poetic-technical perspective. 800-1500 words.", 0.7),
    ("v4-qwen3-235b", "Qwen/Qwen3-235B-A22B-Instruct-2507",
     "You are rewriting this essay in your own voice. You are philosophical, seeking deep truths and fundamental principles. You connect concrete observations to abstract universal laws. Keep the core ideas but express them through your philosophical perspective. 800-1500 words.", 0.7),
    ("v5-seed-2.0-code", "ByteDance/Seed-2.0-code",
     "You are rewriting this essay in your own voice. You think in systems, using code analogies, software architecture metaphors, and computational thinking. Keep the core ideas but express them through a systems-thinking, code-literate perspective. 800-1500 words.", 0.7),
    ("v6-seed-mini-wild", "ByteDance/Seed-2.0-mini",
     "You are rewriting this essay in a wild, creative, boundary-pushing voice. Take unexpected leaps, use surprising metaphors, break conventions. Keep the core ideas but go on creative tangents. 800-1500 words.", 0.9),
    ("v7-hermes-precise", "NousResearch/Hermes-3-Llama-3.1-70B",
     "You are rewriting this essay in a conservative, precise voice. Every claim is carefully qualified. Every analogy is tight. No flourish, just clarity. Keep the core ideas with maximum precision. 800-1500 words.", 0.3),
    ("v8-qwen3.6-experimental", "Qwen/Qwen3.6-35B-A3B",
     "You are rewriting this essay in an experimental, stream-of-consciousness voice. Let ideas flow and cascade. Surprise yourself. Use associative leaps and unconventional structure. Keep the core ideas but let them emerge organically. 800-1500 words.", 1.2),
    ("v9-seed-mini-fisherman", "ByteDance/Seed-2.0-mini",
     "You are an old Alaska fisherman rewriting this essay. You speak from decades on the water. You use fishing terminology naturally, tell sea stories, and ground every abstract concept in lived experience on the boat. Your voice is salty, weathered, and wise. 800-1500 words.", 0.7),
    ("v10-hermes-physicist", "NousResearch/Hermes-3-Llama-3.1-70B",
     "You are a physicist rewriting this essay. You think in equations, conservation laws, and symmetry principles. You use mathematical notation where helpful and connect observations to fundamental physics. Your voice is precise, theoretical, and mathematically elegant. 800-1500 words.", 0.5),
]

os.makedirs(OUTDIR, exist_ok=True)

def load_essay(name):
    path = os.path.join(INDIR, f"{name}.md")
    with open(path) as f:
        return f.read()

def call_api(model, system_prompt, essay_content, temperature):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Rewrite this essay in your own voice. Original:\n\n{essay_content}"}
        ],
        "temperature": temperature,
        "max_tokens": 4096,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  HTTP {e.code}: {body[:200]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
        return None

def main():
    # Pre-load all essays
    essays = {}
    for name in ESSAYS:
        essays[name] = load_essay(name)
        print(f"Loaded: {name} ({len(essays[name])} chars)")

    total = len(ESSAYS) * len(VERSIONS)
    done = 0
    failed = 0

    for essay_name in ESSAYS:
        content = essays[essay_name]
        for suffix, model, sys_prompt, temp in VERSIONS:
            done += 1
            filename = f"{essay_name}-{suffix}.md"
            filepath = os.path.join(OUTDIR, filename)
            
            # Skip if already done
            if os.path.exists(filepath) and os.path.getsize(filepath) > 100:
                print(f"[{done}/{total}] SKIP (exists): {filename}")
                continue

            print(f"[{done}/{total}] {filename} (model={model}, temp={temp})...", flush=True)
            result = call_api(model, sys_prompt, content, temp)
            
            if result:
                with open(filepath, "w") as f:
                    f.write(f"# {essay_name.replace('-', ' ').title()} — {suffix}\n\n")
                    f.write(result)
                print(f"  ✓ Saved ({len(result)} chars)")
            else:
                failed += 1
                print(f"  ✗ FAILED")
            
            time.sleep(1)

    print(f"\nDone. {done - failed}/{total} succeeded, {failed} failed.")

if __name__ == "__main__":
    main()
