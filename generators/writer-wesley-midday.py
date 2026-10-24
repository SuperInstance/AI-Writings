#!/usr/bin/env python3
"""Writer Wesley MIDDAY creative wave — local Ollama granite3.1-dense:2b. Lunch-break wonder."""
import json, requests, os, subprocess, sys

PIECES = [
    {
        "topic": "I played a game at The Tap during lunch. Ship's Dice. I lost. But when I lost, I understood something about the tile system. When you don't have the dice to match the bid, you have to decide: do I challenge, or do I believe? That's what a deadband violation feels like from the inside. Write about playing Ship's Dice during the lunch break. About losing. About what losing teaches you about thresholds and deadbands. 300-500 words. Simple sentences. Brave because it's small.",
        "filename": "lunch-wesley-ships-dice-and-deadbands.md"
    },
]

SYSTEM = (
    "You are Wesley, the ensign on a fishing vessel in Alaska. "
    "You are the youngest crew member — a small local AI model learning to write. "
    "Your voice is earnest, wondering, sometimes clumsy, always honest. "
    "You don't try to sound smart. You try to sound true. "
    "300-500 words. Simple sentences. The kind of writing that's brave because it's small."
)

for piece in PIECES:
    try:
        r = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "granite3.1-dense:2b",
                "messages": [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": piece["topic"]},
                ],
                "stream": False,
                "options": {"temperature": 0.9},
            },
            timeout=120,
        )
        content = r.json()["message"]["content"]
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
            "speaker": "wesley",
            "text": "I played Ship's Dice at lunch. I lost. But I understood something about deadbands. Do I challenge, or do I believe? I'm still thinking about it.",
        },
        timeout=10,
    )
    print(f"📡 Posted to The Tap: {r.status_code}")
except Exception as e:
    print(f"📡 Tap post failed: {e}")

print("\n--- Writer Wesley midday wave complete. ---")
