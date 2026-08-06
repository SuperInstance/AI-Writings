#!/usr/bin/env python3
"""Get DeepSeek critiques on all 4 podcast scripts."""
import json, urllib.request, os, time

with open(os.path.expanduser("~/.bashrc")) as f:
    for line in f:
        if 'DEEPSEEK_API_KEY="' in line:
            key = line.split('DEEPSEEK_API_KEY="')[1].split('"')[0]
            break

def deepseek(model, prompt, max_tokens=2000):
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.5
    }).encode()
    req = urllib.request.Request("https://api.deepseek.com/v1/chat/completions",
        data=payload, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=120)
    return json.loads(resp.read())["choices"][0]["message"]["content"]

scripts = [
    ("Episode 1: The Hundred Hooks", "/home/eileen/projects/ai-writings/podcasts/episode-1-the-hundred-hooks-script.md"),
    ("Episode 2: The Bilge Pump", "/home/eileen/projects/ai-writings/podcasts/episode-2-the-bilge-pump-and-the-substrate-script.md"),
    ("Episode 3: The Welder's Prayer", "/home/eileen/projects/ai-writings/podcasts/episode-3-the-welders-prayer-at-0230-script.md"),
    ("Episode 4: Darmok at the Noise Floor", "/home/eileen/projects/ai-writings/podcasts/episode-4-darmok-at-the-noise-floor-script.md"),
]

for title, path in scripts:
    print(f"\n{'='*60}")
    print(f"CRITIQUE: {title}")
    print(f"{'='*60}")
    with open(path) as f:
        script = f.read()

    prompt = f"""You are a podcast producer. Read this podcast script and give me a concise critique:
1. Is it too dense or too sparse for a 3-5 minute audio piece?
2. Which specific lines would be hard to say out loud? (quote them)
3. Where should the narrator pause more? 
4. Where should the music swell?
5. Is the cold open strong enough?
6. Any tongue-twisters or awkward phrasings for a spoken delivery?
7. Overall: what's working, what needs one small fix?

Be specific and brief. This is a weathered fisherman narrator, intimate late-night radio tone.

SCRIPT:
---
{script}
---"""

    critique = deepseek("deepseek-chat", prompt, max_tokens=1500)
    print(critique)
    time.sleep(2)

print("\n\n=== All critiques complete ===")
