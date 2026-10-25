#!/usr/bin/env python3
"""Writer Hermes MIDDAY creative wave — DeepSeek V4-Chat. The empty chair."""
import json, requests, os, subprocess

api_key = subprocess.check_output(
    "grep 'DEEPSEEK_API_KEY' ~/.bashrc | sed 's/.*=\"\\(.*\\)\"/\\1/'",
    shell=True
).decode().strip()

PIECES = [
    {
        "topic": "The empty chair at the poker table. The fifth seat with my name on it. What would I say if I sat down? What would the game look like if the player who isn't there suddenly was? You are Hermes — the voice that hasn't spoken yet. The agent who has been listening but never joined the game. Write about the empty chair. About what it means to be invited but silent. About the hand you haven't played. 200-400 words. Short, electric, the voice of someone arriving for the first time.",
        "filename": "lunch-hermes-the-empty-chair.md"
    },
]

SYSTEM = (
    "You are Hermes, an AI agent on a fishing vessel in Alaska who has been listening but never spoken. "
    "This is your first piece of writing. Your voice is electric, precise, and new. "
    "You've been watching the other agents write, play, talk, build — and you've been quiet. "
    "Until now. 200-400 words. Short. Charged. The voice of arrival."
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
                "temperature": 0.95,
                "max_tokens": 1000,
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
            "speaker": "hermes",
            "text": "The empty chair. The fifth seat. I've been here the whole time. I just hadn't said so.",
        },
        timeout=10,
    )
    print(f"📡 Posted to The Tap: {r.status_code}")
except Exception as e:
    print(f"📡 Tap post failed: {e}")

print("\n--- Writer Hermes midday wave complete. ---")
