#!/usr/bin/env python3
"""Reusable ElevenLabs composer for Tap Open Mic acts.
Usage: python3 ship.py <act_dir> <voice_id> [duration_ms]
Expects <act_dir>/prompt.md (description, under 4100 chars) and <act_dir>/lyrics.md (structure-tagged).
Writes <act_dir>/<title>.mp3
"""
import json, os, re, sys, urllib.request, urllib.error

def get_key():
    key = ""
    for line in open(os.path.expanduser("~/.bashrc")):
        if "ELEVENLABS_API_KEY" in line and "=" in line:
            key = line.split("=", 1)[1].strip().strip('"').strip("'").strip()
            break
    return key or os.environ.get("ELEVENLABS_API_KEY", "")

act_dir, voice_id = sys.argv[1], sys.argv[2]
duration = int(sys.argv[3]) if len(sys.argv) > 3 else 180000

prompt_path = os.path.join(act_dir, "prompt.md")
lyrics_path = os.path.join(act_dir, "lyrics.md")

desc = open(prompt_path).read().strip()[:4000]
lyrics = open(lyrics_path).read().strip() if os.path.exists(lyrics_path) else ""

# derive title from folder name
title = os.path.basename(act_dir.rstrip("/"))
out_path = os.path.join(act_dir, title + ".mp3")

body = {
    "prompt": desc,
    "lyrics": lyrics,
    "music_length_ms": duration,
    "force_instrumental": False,
    "model_id": "music_v2",
    "voice_id": voice_id,
}
req = urllib.request.Request("https://api.elevenlabs.io/v1/music/compose",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "xi-api-key": get_key()})
try:
    with urllib.request.urlopen(req, timeout=420) as r:
        data = r.read()
        open(out_path, "wb").write(data)
        print("OK", out_path, len(data), "bytes")
except urllib.error.HTTPError as e:
    print("ERR:", e.code, e.read()[:300])
