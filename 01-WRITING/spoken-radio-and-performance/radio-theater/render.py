#!/usr/bin/env python3
"""
Radio Theater: The Trades at The Tap — render pipeline (parametrized per episode).
TTS via DeepInfra Qwen3-TTS-VoiceDesign (free-text voice prompts, distinct per character).
Images via Cloudflare Workers AI FLUX-1-schnell (fallback DeepInfra FLUX).
WAV from DeepInfra is transcoded to real MP3 via ffmpeg for clean browser playback.

Usage: python3 render.py <episode-number>   (e.g. python3 render.py 2)
Reads data/episode-N.json for LINES + IMAGES; renders into episode-N/.
"""
import base64, json, os, re, subprocess, sys, urllib.request, urllib.error, time

ROOT = "/home/eileen/projects/ai-writings/tap-trades/radio-theater"

def deepinfra_key():
    txt = open(os.path.expanduser("~/.bashrc")).read()
    m = re.search(r'DEEPINFRA_API_KEY=["\']?([^"\'\s]+)', txt)
    return m.group(1) if m else os.environ.get("DEEPINFRA_API_KEY", "")

def cf_token():
    try:
        txt = open("/home/eileen/.config/.wrangler/config/default.toml").read()
        m = re.search(r'oauth_token\s*=\s*["\']([^"\']+)', txt)
        return m.group(1) if m else ""
    except Exception:
        return ""

CF_ACCOUNT = "049ff5e84ecf636b53b162cbb580aae6"
DI = deepinfra_key()
CF = cf_token()

# ---------------------------------------------------------------------------
# VOICE CAST (free-text prompts for Qwen3-TTS-VoiceDesign) — reuse EXACTLY
# ---------------------------------------------------------------------------
VOICES = {
    "lucineer":  "deep warm male radio host, authoritative, calm, late-night foreman, low and steady",
    "welder":    "rugged weathered male voice, gravelly, slow and deliberate, working class, nineteen years of heat, welding hood pushed back",
    "carpenter": "warm gruff friendly male voice, plainspoken builder, brisk, sawdust in his collar, coffee in his hand",
    "shipwright":"older grizzled male voice, quiet, contemplative, nautical, pause-heavy, chalk and black pine",
    "mason":     "gentle older male voice, patient, earthy, unhurried, a man who talks to walls the way you talk to a horse",
    "composite": "dry precise male voice, wry, slightly world-weary, the calm monotone of sanding, thirty years of glass dust",
    "wesley":    "ethereal resonant voice, warm and low, the voice of a room remembering, faint echo, omniscient and kind",
}

def load_data(ep):
    path = os.path.join(ROOT, "data", f"episode-{ep}.json")
    with open(path) as f:
        return json.load(f)

# ---------------------------------------------------------------------------
# TTS
# ---------------------------------------------------------------------------
def render_tts(base, character, slug, text):
    out_mp3 = os.path.join(base, f"{character}-{slug}.mp3")
    if os.path.exists(out_mp3) and os.path.getsize(out_mp3) > 1000:
        print(f"  skip (exists) {character}-{slug}", flush=True)
        return True
    body = json.dumps({
        "model": "Qwen/Qwen3-TTS-VoiceDesign",
        "input": text,
        "voice": VOICES[character],
    }).encode()
    req = urllib.request.Request(
        "https://api.deepinfra.com/v1/openai/audio/speech",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + DI})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            wav = r.read()
        tmp_wav = out_mp3 + ".wav"
        open(tmp_wav, "wb").write(wav)
        r = subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", tmp_wav,
             "-codec:a", "libmp3lame", "-b:a", "128k", "-ac", "1", out_mp3],
            capture_output=True)
        os.remove(tmp_wav)
        if r.returncode != 0:
            print(f"  FFMPEG ERR {character}-{slug}: {r.stderr.decode()[:200]}", flush=True)
            return False
        print(f"  OK {character}-{slug}.mp3 ({os.path.getsize(out_mp3)} bytes)", flush=True)
        return True
    except urllib.error.HTTPError as e:
        print(f"  TTS ERR {character}-{slug}: {e.code} {e.read()[:200]}", flush=True)
        return False
    except Exception as e:
        print(f"  TTS EXC {character}-{slug}: {e}", flush=True)
        return False

# ---------------------------------------------------------------------------
# IMAGES
# ---------------------------------------------------------------------------
def render_image_cf(img_dir, slug, prompt):
    out = os.path.join(img_dir, f"{slug}.png")
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        print(f"  skip (exists) {slug}", flush=True)
        return True
    # flux-1-schnell rejects width/height — send only prompt (production note gotcha 2)
    body = json.dumps({"prompt": prompt}).encode()
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/ai/run/@cf/black-forest-labs/flux-1-schnell",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + CF})
    try:
        with urllib.request.urlopen(req, timeout=240) as r:
            data = json.load(r)
        if data.get("success") and data.get("result", {}).get("image"):
            open(out, "wb").write(base64.b64decode(data["result"]["image"]))
            print(f"  OK (CF) {slug}.png ({os.path.getsize(out)} bytes)", flush=True)
            return True
        print(f"  CF no-image {slug}: {json.dumps(data)[:150]}", flush=True)
    except Exception as e:
        print(f"  CF ERR {slug}: {e}", flush=True)
    return False

def render_image_di(img_dir, slug, prompt):
    out = os.path.join(img_dir, f"{slug}.png")
    body = json.dumps({"prompt": prompt, "width": 832, "height": 832,
                       "num_inference_steps": 4, "seed": 777}).encode()
    req = urllib.request.Request(
        "https://api.deepinfra.com/v1/inference/black-forest-labs/FLUX-1-schnell",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + DI})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.load(r)
        b64 = data.get("output") or data.get("images")
        if isinstance(b64, list):
            b64 = b64[0] if b64 else None
        if isinstance(b64, str):
            if b64.startswith("data:"):
                b64 = b64.split(",", 1)[1]
            open(out, "wb").write(base64.b64decode(b64))
            print(f"  OK (DI) {slug}.png ({os.path.getsize(out)} bytes)", flush=True)
            return True
    except Exception as e:
        print(f"  DI ERR {slug}: {e}", flush=True)
    return False

if __name__ == "__main__":
    ep = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    data = load_data(ep)
    base = os.path.join(ROOT, f"episode-{ep}")
    img_dir = os.path.join(base, "images")
    os.makedirs(img_dir, exist_ok=True)

    print(f"=== RADIO THEATER EPISODE {ep} ({data['title']}) RENDER ===", flush=True)
    print(f"DeepInfra key: {DI[:8]}...  CF token: {CF[:12]}...", flush=True)

    print("\n--- TTS ---", flush=True)
    ok = 0
    for ln in data["lines"]:
        if render_tts(base, ln["speaker"], ln["slug"], ln["text"]):
            ok += 1
        time.sleep(0.4)
    print(f"\nTTS done: {ok}/{len(data['lines'])} rendered", flush=True)

    print("\n--- IMAGES ---", flush=True)
    iok = 0
    for im in data["images"]:
        if render_image_cf(img_dir, im["slug"], im["prompt"]) or render_image_di(img_dir, im["slug"], im["prompt"]):
            iok += 1
        time.sleep(0.5)
    print(f"\nImages done: {iok}/{len(data['images'])} rendered", flush=True)
    print("\n=== COMPLETE ===", flush=True)
