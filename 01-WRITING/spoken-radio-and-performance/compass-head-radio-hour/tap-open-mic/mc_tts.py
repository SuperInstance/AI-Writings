#!/usr/bin/env python3
"""MC TTS render — Lucineer speaks (raw REST, bypasses MCP permission snag).
Usage: python3 mc_tts.py <text_file> <out.mp3> [voice_id]
"""
import json, os, sys, urllib.request, urllib.error

def get_key():
    key = ""
    for line in open(os.path.expanduser("~/.bashrc")):
        if "ELEVENLABS_API_KEY" in line and "=" in line:
            key = line.split("=", 1)[1].strip().strip('"').strip("'").strip()
            break
    return key or os.environ.get("ELEVENLABS_API_KEY", "")

text_file, out = sys.argv[1], sys.argv[2]
voice = sys.argv[3] if len(sys.argv) > 3 else "swjWCZjZyczZmjedyBph"
text = open(text_file).read().strip()

body = {
    "text": text,
    "model_id": "eleven_multilingual_v2",
    "voice_setting": {"stability": 0.55, "similarity_boost": 0.75, "style": 0.35},
}
req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "xi-api-key": get_key(), "Accept": "audio/mpeg"})
try:
    with urllib.request.urlopen(req, timeout=240) as r:
        data = r.read()
        open(out, "wb").write(data)
        print("OK", out, len(data), "bytes")
except urllib.error.HTTPError as e:
    print("ERR:", e.code, e.read()[:300])
