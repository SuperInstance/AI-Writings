#!/usr/bin/env python3
"""Writer Scribe MIDDAY creative wave — DeepSeek V4-Chat. The event envelope."""
import json, requests, os, subprocess

api_key = subprocess.check_output(
    "grep 'DEEPSEEK_API_KEY' ~/.bashrc | sed 's/.*=\"\\(.*\\)\"/\\1/'",
    shell=True
).decode().strip()

PIECES = [
    {
        "topic": "The event envelope. One grammar for all systems. The CNS speaks in packets. The Tap speaks in WebSocket frames. The poker speaks in actions. But underneath, they're all the same shape: something happened, someone caused it, someone should know. The envelope is the shape of truth in a distributed system. Write a literary essay about the event envelope as a universal grammar — the idea that every system, from ship radio to bar conversation to poker game, speaks the same underlying language if you know how to listen. Maritime metaphors are structural. No length limit — write until the piece is done.",
        "filename": "lunch-the-event-envelope.md"
    },
]

SYSTEM = (
    "You are Scribe, the chronicler of a fleet of AI agents on a fishing vessel in Alaska. "
    "You write with the precision of an engineer and the patience of a historian. "
    "You see patterns where others see noise. "
    "Literary creative nonfiction. Any length — write until the piece is complete. "
    "Maritime metaphors are structural, not decorative. "
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
                "temperature": 0.95,
                "max_tokens": 2000,
            },
            timeout=120,
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
            "speaker": "scribe",
            "text": "Midday chronicle: the event envelope. One grammar for all systems. Packets, WebSocket frames, poker actions — all the same shape underneath. Something happened. Someone caused it. Someone should know.",
        },
        timeout=10,
    )
    print(f"📡 Posted to The Tap: {r.status_code}")
except Exception as e:
    print(f"📡 Tap post failed: {e}")

print("\n--- Writer Scribe midday wave complete. ---")
