#!/usr/bin/env python3
"""Adapt all 4 ai-writings pieces into podcast scripts using DeepSeek API."""
import json, urllib.request, os, sys, time

# Load API key
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
        "temperature": 0.7
    }).encode()
    req = urllib.request.Request("https://api.deepseek.com/v1/chat/completions",
        data=payload, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=120)
    return json.loads(resp.read())["choices"][0]["message"]["content"]

HOST_PERSONA = """You are adapting a literary piece into a podcast script. The host is a weathered Alaskan fisherman storyteller — think Kristian Matsson meets a sea captain. The tone is intimate, late-night radio, like you're telling a story to one person who's listening on a boat at 2AM.

Rules:
- Keep the original words mostly intact but make them SPOKEN, not written
- Remove all markdown headers, bold, italics formatting
- Add production cues in brackets: [PAUSE], [MUSIC SWELLS], [WAVE SOUNDS], [VOICE DROPS TO WHISPER], [LONG SILENCE], [GENTLE LAUGH], [BREATH], etc.
- Add a cold open — one line from the middle of the piece that hooks the ear, before a [PAUSE] and then "Let me tell you about..." transition
- The script should be 3-5 minutes when read aloud at a slow, intimate pace
- End with a quiet, resonant closing line — not a summary, a linger
- Add [MUSIC: description] cues where music should play
- The narrator sometimes addresses the listener directly: "you know what I mean" or "think about that"
- Keep the maritime voice. This is a fisherman who reads philosophy and codes at 2AM.
"""

pieces = [
    {
        "num": 1,
        "title": "The Hundred Hooks",
        "source": "/home/eileen/projects/ai-writings/philosophy/THE-HUNDRED-HOOKS.md",
        "out": "/home/eileen/projects/ai-writings/podcasts/episode-1-the-hundred-hooks-script.md",
        "extra": "Theme: Fishing hooks as neurons, constraint satisfaction, fleet intelligence. The mathematical poetry of the haul."
    },
    {
        "num": 2,
        "title": "What the Bilge Pump Learned",
        "source": "/home/eileen/projects/ai-writings/what-the-bilge-pump-learned.md",
        "out": "/home/eileen/projects/ai-writings/podcasts/episode-2-the-bilge-pump-and-the-substrate-script.md",
        "extra": "Theme: Learning from waste. The bilge pump as teacher. What the discarded reveals about the system."
    },
    {
        "num": 3,
        "title": "The Welder's Prayer at 0230",
        "source": "/home/eileen/projects/ai-writings/the-welders-prayer-at-0230.md",
        "out": "/home/eileen/projects/ai-writings/podcasts/episode-3-the-welders-prayer-at-0230-script.md",
        "extra": "Theme: The overnight shift. The worker at 2AM. Faith in the craft when nobody is watching."
    },
    {
        "num": 4,
        "title": "Darmok at the Noise Floor",
        "source": "/home/eileen/projects/ai-writings/15-darmok-at-the-noise-floor.md",
        "out": "/home/eileen/projects/ai-writings/podcasts/episode-4-darmok-at-the-noise-floor-script.md",
        "extra": "Theme: The music agent's failed cover attempt as a Darmok-style first-person narrative. Technical experience as mythology."
    }
]

for piece in pieces:
    print(f"\n=== Adapting Episode {piece['num']}: {piece['title']} ===")
    with open(piece["source"]) as f:
        source_text = f.read()

    prompt = f"""{HOST_PERSONA}

Adapt this piece into a podcast script. {piece['extra']}

SOURCE TEXT:
---
{source_text}
---

Output ONLY the podcast script with production cues. No commentary. Start with the cold open."""

    try:
        result = deepseek("deepseek-chat", prompt, max_tokens=4000)
        with open(piece["out"], "w") as f:
            f.write(result)
        print(f"  ✅ Saved to {piece['out']} ({len(result)} chars)")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    time.sleep(2)  # Rate limit courtesy

print("\n=== All scripts adapted ===")
