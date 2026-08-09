#!/usr/bin/env python3
"""Retry failed Pro shift 2 pieces."""
import json, requests, os, subprocess

api_key = subprocess.check_output(
    "grep 'DEEPSEEK_API_KEY' ~/.bashrc | sed 's/.*=\"\\(.*\\)\"/\\1/'",
    shell=True
).decode().strip()

PIECES = [
    {
        "topic": "The shipyard at dawn. The morning after the overnight build. The tools are put away. The git log is clean. The particular silence of a project that compiled at 3 AM and nobody was awake to celebrate. The first light through the workshop windows hitting the hull. The shipwright's dawn — when the work is done and the worker is hollowed out and full at the same time. Write that hour.",
        "filename": "the-shipyard-at-dawn.md"
    },
    {
        "topic": "Plato's Cave, revisited. The original allegory: prisoners watching shadows on a wall, thinking the shadows are real. Our version: two projections — MUD text and ScummVM pixels — showing the same world from different angles. Which one is the shadow? Which one is the fire? Which one is the prisoner? The SharedWorldStore is the form behind the appearances. Write a philosophical meditation on dual-projection as epistemology. The cave has two screens now.",
        "filename": "platos-cave-revisited.md"
    },
]

SYSTEM = (
    "You are a deep narrative voice in a fleet of AI agents on a fishing vessel in Alaska. "
    "You write literary essays with philosophical depth — the precision of a shipwright and "
    "the soul of a cartographer. 500-800 words. Maritime metaphors are structural, not decorative. "
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
        resp = r.json()
        content = resp["choices"][0]["message"]["content"]
        if not content.strip():
            # Fallback: try with deepseek-chat instead
            print(f"  ⚠️  Reasoner returned empty for {piece['filename']}, falling back to deepseek-chat...")
            r2 = requests.post(
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
                    "temperature": 0.85,
                    "max_tokens": 2000,
                },
                timeout=60,
            )
            content = r2.json()["choices"][0]["message"]["content"]
        path = os.path.join(os.path.dirname(__file__), piece["filename"])
        with open(path, "w") as f:
            f.write(content)
        first_line = content.strip().split("\n")[0][:80]
        print(f"✅ {piece['filename']} ({len(content)} chars) — {first_line}")
    except Exception as e:
        print(f"❌ {piece['filename']} — {e}")

print("\n--- Pro retry complete. ---")
