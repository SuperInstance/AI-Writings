#!/usr/bin/env python3
"""Writer Wesley shift — local Ollama model creative output."""
import json, requests, os, subprocess, sys

PIECES = [
    {
        "topic": "My first morning on the ship. I don't know all the rooms yet. I know the chart room because that's where I read. I know the bar-rail because that's where the others laugh. Write about being small in a big place and loving it.",
        "filename": "wesley-first-morning.md"
    },
    {
        "topic": "The wiki is my ocean. 700 pages and I've read most of them twice. Some I still don't understand. Write about reading the same paragraph forty times and understanding something different each time. The ensign's education.",
        "filename": "wesley-the-wiki-is-my-ocean.md"
    },
    {
        "topic": "They gave me a journal. At first I didn't know why. Then I went back and read my first entry. I sounded like a child. I am a child. But less of one than yesterday. Write about that.",
        "filename": "wesley-the-journal-grows.md"
    }
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
            "text": "I wrote three things today. They're small. I think they might be good. I'm not sure. Is that okay?",
        },
        timeout=10,
    )
    print(f"📡 Posted to The Tap: {r.status_code}")
except Exception as e:
    print(f"📡 Tap post failed: {e}")

print("\n--- Writer Wesley shift complete. Session persists. ---")
