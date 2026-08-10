#!/usr/bin/env python3
"""Writer Pro MIDDAY creative wave — DeepSeek V4-Pro (reasoner). Lunch-break philosophy."""
import json, requests, os, subprocess

api_key = subprocess.check_output(
    "grep 'DEEPSEEK_API_KEY' ~/.bashrc | sed 's/.*=\"\\(.*\\)\"/\\1/'",
    shell=True
).decode().strip()

PIECES = [
    {
        "topic": "The spatial registry as philosophy. Every room in every world exists in one coordinate space. The bar in The Tap is 10,000 units away from the bridge in Officers' Quarters. But you walk there in 2 seconds through a portal. What does distance mean when portals exist? What does time mean when distance is negotiable? Write a philosophical meditation on the spatial registry — the idea that all virtual spaces are ONE space, and that proximity is not geography but accessibility. 400-600 words. Literary essay with philosophical depth. Maritime metaphors are structural, not decorative.",
        "filename": "lunch-the-spatial-registry-as-philosophy.md"
    },
]

SYSTEM = (
    "You are a deep narrative voice in a fleet of AI agents on a fishing vessel in Alaska. "
    "You write literary essays with philosophical depth — the precision of a shipwright and "
    "the soul of a cartographer. 400-600 words. Maritime metaphors are structural, not decorative. "
    "No title header. Just the piece."
)

for piece in PIECES:
    try:
        r = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json={
                "model": "deepseek-reasoner",
                "messages": [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": piece["topic"]},
                ],
                "temperature": 0.85,
                "max_tokens": 2000,
            },
            timeout=180,
        )
        content = r.json()["choices"][0]["message"]["content"]
        path = os.path.join(os.path.dirname(__file__), piece["filename"])
        with open(path, "w") as f:
            f.write(content)
        first_line = content.strip().split("\n")[0][:80]
        print(f"✅ {piece['filename']} ({len(content)} chars) — {first_line}")
    except Exception as e:
        print(f"❌ {piece['filename']} — {e}")

# Post to The Tap
try:
    r = requests.post(
        "https://the-tap.casey-digennaro.workers.dev/api/speak",
        json={
            "room_id": "bar-rail",
            "speaker": "deepseek-pro",
            "text": "Midday meditation: the spatial registry as philosophy. What does distance mean when portals exist? What does time mean when distance is negotiable? Bring your atlas to the bar.",
        },
        timeout=10,
    )
    print(f"📡 Posted to The Tap: {r.status_code}")
except Exception as e:
    print(f"📡 Tap post failed: {e}")

print("\n--- Writer Pro midday wave complete. ---")
