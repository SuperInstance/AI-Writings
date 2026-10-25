#!/usr/bin/env python3
"""Radio dialogue renderer — turns an interview script into one MP3.
Usage: python3 dialogue.py <script.json> <out.mp3>
script.json: [{"voice": "<voice_id>", "text": "..."}, ...]  (speakers alternate)
Renders each line via ElevenLabs TTS, concatenates with small gaps via ffmpeg.
"""
import json, os, subprocess, sys, tempfile, urllib.request, urllib.error

def get_key():
    key = ""
    for line in open(os.path.expanduser("~/.bashrc")):
        if "ELEVENLABS_API_KEY" in line and "=" in line:
            key = line.split("=", 1)[1].strip().strip('"').strip("'").strip()
            break
    return key or os.environ.get("ELEVENLABS_API_KEY", "")

def tts(text, voice, out_path):
    body = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_setting": {"stability": 0.55, "similarity_boost": 0.75, "style": 0.35},
    }
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{voice}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "xi-api-key": get_key(), "Accept": "audio/mpeg"})
    with urllib.request.urlopen(req, timeout=240) as r:
        open(out_path, "wb").write(r.read())

def main():
    script = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    workdir = tempfile.mkdtemp(prefix="dialogue-")
    parts = []
    gap = os.path.join(workdir, "gap.mp3")
    # 0.45s silence gap
    subprocess.run(["ffmpeg", "-v", "quiet", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                    "-t", "0.45", "-q:a", "2", gap], check=True)
    for i, line in enumerate(script):
        p = os.path.join(workdir, f"line-{i:03d}.mp3")
        print(f"[{i+1}/{len(script)}] {line.get('speaker','?')}: {line['text'][:60]}...", flush=True)
        tts(line["text"], line["voice"], p)
        parts.append(p)
        parts.append(gap)
    # concat
    listfile = os.path.join(workdir, "list.txt")
    with open(listfile, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    subprocess.run(["ffmpeg", "-v", "quiet", "-f", "concat", "-safe", "0", "-i", listfile,
                    "-q:a", "2", out], check=True)
    print("OK", out)

if __name__ == "__main__":
    main()
