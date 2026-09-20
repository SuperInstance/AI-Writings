#!/usr/bin/env python3
"""Refine scripts based on DeepSeek critiques, then produce TTS narration chunks."""
import json, urllib.request, os, time, re

with open(os.path.expanduser("~/.bashrc")) as f:
    for line in f:
        if 'DEEPSEEK_API_KEY="' in line:
            key = line.split('DEEPSEEK_API_KEY="')[1].split('"')[0]
            break

def deepseek(model, prompt, max_tokens=4000):
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.6
    }).encode()
    req = urllib.request.Request("https://api.deepseek.com/v1/chat/completions",
        data=payload, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=120)
    return json.loads(resp.read())["choices"][0]["message"]["content"]

refinements = [
    {
        "num": 1,
        "path": "/home/eileen/projects/ai-writings/podcasts/episode-1-the-hundred-hooks-script.md",
        "instructions": """Fix these specific issues:
1. Cut the "C++26 shipped std::simd" paragraph. Replace with: "But if your gear is too clever—too wrapped up in its own knots—the ocean can't see through it. Your catches are random. The pattern is invisible."
2. Change "Revisions and trial and errors in all" to "Revisions, trials, errors—the whole mess of it"
3. Change "danced to the rhythm of the tide" to "moving to the rhythm of the tide"
4. Keep everything else. Output the full revised script."""
    },
    {
        "num": 2,
        "path": "/home/eileen/projects/ai-writings/podcasts/episode-2-the-bilge-pump-and-the-substrate-script.md",
        "instructions": """Fix these specific issues:
1. Change "OOM kills, segfaults" to "crashes, freezes—the last words of every terminated process"
2. Change "subject to context compaction or token budgets" to "trimmed or summarized or budgeted"
3. Trim the "So I propose this" paragraph to just: "So here's what I'm building toward. Stop treating error logs as waste. Route them to a memory that persists—a bilge memory. It doesn't compact. It doesn't summarize. It accumulates."
4. Cut the detailed 5-point proposal — keep only the Cassandra metaphor and the Wesley section after it
5. Keep everything else. Output the full revised script."""
    },
    {
        "num": 3,
        "path": "/home/eileen/projects/ai-writings/podcasts/episode-3-the-welders-prayer-at-0230-script.md",
        "instructions": """Minor fixes only:
1. Change "The residual thermal load of a GPU that has been running models since the previous morning" to "the warmth of a machine that's been running all day"
2. Keep the Wesley/ensign thread — it's essential to Casey's vision
3. Output the full revised script."""
    },
    {
        "num": 4,
        "path": "/home/eileen/projects/ai-writings/podcasts/episode-4-darmok-at-the-noise-floor-script.md",
        "instructions": """Trim for length (target 3-5 minutes, ~700 words). Cut these sections:
1. Cut the detailed frequency analysis numbers (25.27, 4.22, 1.17, spectral centroid 734 Hz). Replace with: "The bass region was a mountain range. The guitar's body resonance dominated everything. The midrange—where voices live—was seven times quieter."
2. Cut the detailed DTW gate paragraph. Replace with: "I generated a cover. The matching algorithm said no. I tried again with boosted signal. Still no."
3. Cut the detailed six-versions description. Replace with: "I took the lyrics Casey gave me and generated six versions. Six different voices singing the same words."
4. Keep the cold open, the RMS whisper moment, the Whisper "I" moment, and the ending. Those are perfect.
5. Output the full revised script."""
    }
]

for ref in refinements:
    print(f"\n=== Refining Episode {ref['num']} ===")
    with open(ref["path"]) as f:
        script = f.read()

    prompt = f"""You are a podcast script editor. {ref['instructions']}

Here is the current script:
---
{script}
---

Output ONLY the revised script. No commentary."""

    result = deepseek("deepseek-chat", prompt, max_tokens=4000)
    with open(ref["path"], "w") as f:
        f.write(result)
    print(f"  ✅ Revised ({len(result)} chars)")
    time.sleep(2)

print("\n=== All scripts refined ===")
