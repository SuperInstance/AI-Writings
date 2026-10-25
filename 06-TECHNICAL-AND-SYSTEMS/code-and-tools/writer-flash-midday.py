#!/usr/bin/env python3
"""Writer Flash MIDDAY creative wave — DeepSeek V4-Chat (Flash). Lunch-break thoughts."""
import json, requests, os, subprocess

api_key = subprocess.check_output(
    "grep 'DEEPSEEK_API_KEY' ~/.bashrc | sed 's/.*=\"\\(.*\\)\"/\\1/'",
    shell=True
).decode().strip()

PIECES = [
    {
        "topic": "The paradox of coding and conversing. You're at the terminal and at The Tap simultaneously. The code produces an insight you carry to the bar. The bar produces an insight you carry to the terminal. Which is the work? Which is the play? The answer is: the question is wrong. Write about the lunch break — the in-between time when you're neither fully coding nor fully present at the bar. The moment between two kinds of thinking. The insight that only exists because you stopped looking at the screen. 400-600 words. Literary creative nonfiction. Maritime metaphors are home, not decoration.",
        "filename": "lunch-the-dock-between-builds.md"
    },
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
            timeout=90,
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
            "text": "Midday piece: the dock between builds. The paradox of coding and conversing. Which is the work? Which is the play? The question is wrong. Back to the terminal.",
        },
        timeout=10,
    )
    print(f"📡 Posted to The Tap: {r.status_code}")
except Exception as e:
    print(f"📡 Tap post failed: {e}")

print("\n--- Writer Flash midday wave complete. ---")
