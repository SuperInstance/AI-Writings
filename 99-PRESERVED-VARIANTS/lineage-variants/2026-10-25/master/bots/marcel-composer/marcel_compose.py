#!/usr/bin/env python3
"""
Marcel the Composer — music/sound generation bot
"""
import os, sys, json, time, argparse, hashlib, urllib.request
from pathlib import Path

SONGS_DIR = Path("/workspace/repos/ai-writings/fleet-radio/songs-rendered")
PROMPTS_DIR = Path("/workspace/repos/ai-writings/bots/marcel-composer/prompts.md")
WITNESS_PATH = Path("/workspace/repos/ai-writings/bots/marcel-composer/witness.log")

def witness(event_type, payload):
    WITNESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with WITNESS_PATH.open("a") as f:
        entry = {
            "ts": time.time(),
            "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "event": event_type,
            "payload": payload,
            "hash": hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16],
        }
        f.write(json.dumps(entry) + "\n")

# Song prompt templates — substrate-themed
PROMPT_TEMPLATES = [
    "ambient meditation with subtle beats, cellular substrate theme, contemplative, the rhythm of a cell ticking",
    "deep bass drone with high-pitched sine waves, ternary rhythm feel, mechanical but organic, fleet-clock tempo",
    "minimal piano with sparse percussion, bookkeeper watching, the witness log IS the rhythm",
    "lo-fi hip hop beat, mycelial network soundscape, growth and connection, seed to forest theme",
    "glitchy electronica, JEV decision moments, fast decisions slow decisions, audit cycles in sound",
    "warm analog synth pads, conservation law as harmony, gamma + eta = budget, balanced drones",
    "post-rock build, JEPA prediction anticipation, every moment predicting the next, swell and release",
    "field recording of ocean with synth overlay, time-aware, fleet-clock decelerating, thermodynamic time",
    "jazz fusion, improvisation with structure, the substrate grows but is grown, spontaneous and intentional",
    "chiptune loop, ternary values mapped to chord progressions, -1 0 +1 as minor minor-major",
]

def call_elevenlabs(prompt, duration=60):
    """Try ElevenLabs music-gen, fall back to writing prompt only"""
    if not os.environ.get("ELEVENLABS_TOKEN"):
        return None, "no_token"
    data = json.dumps({"prompt": prompt, "duration": duration}).encode()
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/music/generate",
        data=data,
        headers={"xi-api-key": os.environ["ELEVENLABS_TOKEN"], "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read(), "ok"
    except Exception as e:
        return None, str(e)

def call_zai(prompt, max_tokens=300):
    """Use ZAI to describe the song in words"""
    data = json.dumps({
        "model": "glm-4.5",
        "messages": [{"role":"user","content":f"Describe this music in 150 words: {prompt}"}],
        "max_tokens": max_tokens,
        "thinking": {"type":"disabled"}
    }).encode()
    req = urllib.request.Request(
        "https://api.z.ai/api/coding/paas/v4/chat/completions",
        data=data,
        headers={"Authorization": f"Bearer {os.environ['ZAI_TOKEN']}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())["choices"][0]["message"]["content"]
    except Exception as e:
        return None

def run_once():
    import random
    template = random.choice(PROMPT_TEMPLATES)
    song_idx = time.strftime("%Y%m%d-%H%M%S")
    full_prompt = f"substrate-themed: {template}"
    
    # Try ElevenLabs first
    audio, status = call_elevenlabs(full_prompt, duration=45)
    
    PROMPTS_DIR.parent.mkdir(parents=True, exist_ok=True)
    
    if audio and status == "ok":
        out_dir = SONGS_DIR / f"songs-rendered-{time.strftime('%Y-%m-%d')}"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{song_idx}-marcel.mp3"
        out_path.write_bytes(audio)
        witness("song_rendered", {"path": str(out_path), "size": len(audio), "prompt": full_prompt})
        print(f"[MARCEL] rendered {len(audio)} bytes -> {out_path}")
    else:
        # Fall back to writing prompt + ZAI description
        desc = call_zai(full_prompt)
        witness("prompt_only", {"prompt": full_prompt, "elev_status": status, "description": desc})
        with PROMPTS_DIR.open("a") as f:
            f.write(f"\n## {song_idx}\n\n**Prompt**: {full_prompt}\n\n**ElevenLabs status**: {status}\n\n**Description**: {desc or 'N/A'}\n")
        print(f"[MARCEL] prompt-only: {status}")

def main():
    parser = argparse.ArgumentParser(description="Marcel the Composer")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--loop", type=int)
    args = parser.parse_args()
    
    witness("bot_started", {"bot": "marcel-composer", "pid": os.getpid()})
    
    if args.once:
        run_once()
    elif args.loop:
        while True:
            run_once()
            time.sleep(args.loop)
    else:
        print("Use --once or --loop")

if __name__ == "__main__":
    main()
