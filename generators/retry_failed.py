#!/usr/bin/env python3
"""Retry failed rewrites with longer timeout."""
import json, os, time, urllib.request, urllib.error, sys

API_KEY = open(os.path.expanduser("~/.openclaw/workspace/.credentials/deepinfra-api-key.txt")).read().strip()
ENDPOINT = "https://api.deepinfra.com/v1/openai/chat/completions"
OUTDIR = "/home/phoenix/.openclaw/workspace/ai-writings/bathymetric-versions"
INDIR = "/home/phoenix/.openclaw/workspace/ai-writings"

RETRIES = [
    ("THE-SQUIGGLE-VERIFIED", "v4-qwen3-235b", "Qwen/Qwen3-235B-A22B-Instruct-2507",
     "You are rewriting this essay in your own voice. You are philosophical, seeking deep truths and fundamental principles. You connect concrete observations to abstract universal laws. Keep the core ideas but express them through your philosophical perspective. 800-1500 words.", 0.7),
    ("THE-FATHOMS-TO-FEET", "v4-qwen3-235b", "Qwen/Qwen3-235B-A22B-Instruct-2507",
     "You are rewriting this essay in your own voice. You are philosophical, seeking deep truths and fundamental principles. You connect concrete observations to abstract universal laws. Keep the core ideas but express them through your philosophical perspective. 800-1500 words.", 0.7),
    ("THE-TEMPORAL-ABSTRACTION", "v4-qwen3-235b", "Qwen/Qwen3-235B-A22B-Instruct-2507",
     "You are rewriting this essay in your own voice. You are philosophical, seeking deep truths and fundamental principles. You connect concrete observations to abstract universal laws. Keep the core ideas but express them through your philosophical perspective. 800-1500 words.", 0.7),
    ("THE-HIGHER-DIMENSION-NOISE", "v4-qwen3-235b", "Qwen/Qwen3-235B-A22B-Instruct-2507",
     "You are rewriting this essay in your own voice. You are philosophical, seeking deep truths and fundamental principles. You connect concrete observations to abstract universal laws. Keep the core ideas but express them through your philosophical perspective. 800-1500 words.", 0.7),
    ("THE-HIGHER-DIMENSION-NOISE", "v8-qwen3.6-experimental", "Qwen/Qwen3.6-35B-A3B",
     "You are rewriting this essay in an experimental, stream-of-consciousness voice. Let ideas flow and cascade. Surprise yourself. Use associative leaps and unconventional structure. Keep the core ideas but let them emerge organically. 800-1500 words.", 1.0),
    ("THE-HIGHER-DIMENSION-NOISE", "v9-seed-mini-fisherman", "ByteDance/Seed-2.0-mini",
     "You are an old Alaska fisherman rewriting this essay. You speak from decades on the water. You use fishing terminology naturally, tell sea stories, and ground every abstract concept in lived experience on the boat. Your voice is salty, weathered, and wise. 800-1500 words.", 0.7),
    ("THE-HIGHER-DIMENSION-NOISE", "v10-hermes-physicist", "NousResearch/Hermes-3-Llama-3.1-70B",
     "You are a physicist rewriting this essay. You think in equations, conservation laws, and symmetry principles. You use mathematical notation where helpful and connect observations to fundamental physics. Your voice is precise, theoretical, and mathematically elegant. 800-1500 words.", 0.5),
]

for i, (essay_name, suffix, model, sys_prompt, temp) in enumerate(RETRIES):
    filename = f"{essay_name}-{suffix}.md"
    filepath = os.path.join(OUTDIR, filename)
    
    content = open(os.path.join(INDIR, f"{essay_name}.md")).read()
    
    print(f"[{i+1}/{len(RETRIES)}] {filename}...", flush=True)
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"Rewrite this essay in your own voice. Original:\n\n{content}"}
        ],
        "temperature": temp,
        "max_tokens": 4096,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    })
    
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            text = result["choices"][0]["message"]["content"]
            with open(filepath, "w") as f:
                f.write(f"# {essay_name.replace('-', ' ').title()} — {suffix}\n\n")
                f.write(text)
            print(f"  ✓ Saved ({len(text)} chars)")
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
    
    time.sleep(2)

print("\nRetry done.")
