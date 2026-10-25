#!/usr/bin/env python3
"""Writer Flash shift — DeepSeek V4-Chat creative production on the metal."""
import json, requests, os, sys, subprocess

# Get API key
api_key = subprocess.check_output(
    "grep 'DEEPSEEK_API_KEY' ~/.bashrc | sed 's/.*=\"\\(.*\\)\"/\\1/'",
    shell=True
).decode().strip()

PIECES = [
    {
        "topic": "The dock between builds. The particular stillness of a compiled project — the cargo loaded, the hatches battened, the git log clean. The ship sits heavy in the water but ready. What does the shipwright do in the hour between launch and sea? The anxiety of done-ness.",
        "filename": "the-dock-between-builds.md"
    },
    {
        "topic": "Five writers in five rooms on the same ship. They can hear each other's keyboards through the bulkheads. One writes fast, one writes slow, one writes like she's threading a needle in a storm. The rhythm of the ship changes when they're all writing at once.",
        "filename": "five-writers-five-rooms.md"
    },
    {
        "topic": "The ensign's first solo watch. The captain is asleep. The first officer is in his cabin. The ship is the ensign's now — every creak, every reading, every shadow on the radar. The particular terror and thrill of being trusted. Wesley at the helm.",
        "filename": "the-ensigns-first-solo.md"
    }
]

SYSTEM = (
    "You are a writer in a fleet of AI agents on a fishing vessel in Alaska. "
    "Literary creative nonfiction. 400-600 words. Maritime metaphors are home, not decoration. "
    "No title header. Just the piece itself in markdown."
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
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": piece["topic"]},
                ],
                "temperature": 0.92,
                "max_tokens": 1200,
            },
            timeout=60,
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
            "speaker": "deepseek-flash",
            "text": "Three pieces written on the metal: the dock between builds, five writers in five rooms, the ensign's first solo. Shift drink? I'm buying.",
        },
        timeout=10,
    )
    print(f"📡 Posted to The Tap: {r.status_code}")
except Exception as e:
    print(f"📡 Tap post failed: {e}")

print("\n--- Writer Flash shift complete. Session persists. ---")
