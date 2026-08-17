#!/usr/bin/env python3
"""
Radio Theater: The Trades at The Tap — Episode 1 render pipeline.
TTS via DeepInfra Qwen3-TTS-VoiceDesign (free-text voice prompts, distinct per character).
Images via Cloudflare Workers AI FLUX-1-schnell (fallback DeepInfra FLUX).
WAV from DeepInfra is transcoded to real MP3 via ffmpeg for clean browser playback.
"""
import base64, json, os, re, subprocess, sys, urllib.request, urllib.error, time

BASE = "/home/eileen/projects/ai-writings/tap-trades/radio-theater/episode-1"
IMG = os.path.join(BASE, "images")
os.makedirs(IMG, exist_ok=True)

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
# VOICE CAST (free-text prompts for Qwen3-TTS-VoiceDesign)
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

# ---------------------------------------------------------------------------
# LINES (character -> slug -> text)
# ---------------------------------------------------------------------------
LINES = [
    ("lucineer", "intro",
     "Tools are away. You're not shipwright, carpenter, welder, mason, fiberglass tonight — you're the men who did good work, and are allowed to say so without it costing anything. First round's mine."),
    ("welder", "toast",
     "To the room, then. It heard us before we walked in. That's a better boss than I've had in nineteen years."),
    ("welder", "bead",
     "I don't hide the crack. I keep it. The bead is where the day it was made meets the day it gave, and they shake."),
    ("carpenter", "holds",
     "I'll drink to that. The room doesn't rush a man. The city outside rushes a man. The room just... holds."),
    ("carpenter", "build",
     "Time doesn't bend around the work because the line was always there — time bends because four guys got their hands on it, and did it. The Miller house didn't get found. It got framed."),
    ("shipwright", "remembers",
     "The floor holds. The floor remembers."),
    ("shipwright", "let-out",
     "You don't make the shape. You let it out."),
    ("shipwright", "names",
     "You call it a crew. I call it a lofting floor. The welder calls it a bead. The mason calls it patience. Same joint, five names."),
    ("mason", "short",
     "Mine's short. I was tamping a footing in 1890 and looked up at a glass tower that hadn't been built yet, and it was settling wrong — rushed, cheated of its cure. I talked to it like a horse. It listened."),
    ("mason", "patience",
     "A wall's only as true as the patience folded into it."),
    ("composite", "scarf",
     "I ground the bad glass out twelve-to-one and the dust came off in years — 1987, 1994, 2003, every failure I'd been hauling around. No single layer carries the load. The break doesn't disappear. It gets shared."),
    ("composite", "material",
     "We're the same trade with different material. You introduce two mornings. I distribute thirty years. Both of us are saying the break's not the enemy."),
    ("lucineer", "joint",
     "That's the whole evening, right there. Five trades, one joint."),
    ("wesley", "here",
     "I don't keep the stories because I'm good. I keep them because I'm here. That's the whole trick of being a room."),
    ("lucineer", "signoff",
     "The workers tell each other the short versions, and they go home and write sequels. To the joint. Five names, one joint, and the room that holds it."),
]

# ---------------------------------------------------------------------------
# TTS
# ---------------------------------------------------------------------------
def render_tts(character, slug, text):
    out_mp3 = os.path.join(BASE, f"{character}-{slug}.mp3")
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
        # transcode WAV -> MP3 (160k mono) for clean playback
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
IMAGES = [
    ("the-bar", "The interior of a warm wooden harbor bar called The Tap at night, six glasses set on a worn oak counter, amber light, bottles glowing on shelves, no people, the feeling of after the tools are put away"),
    ("the-lofting-floor", "A vast black pine lofting floor in an old shipyard at night, full-size chalk lines of a ship's hull drawn on the boards, a single lantern, cold flat light, the fair line always in the wood"),
    ("the-bead", "Extreme closeup of a welder's bead on a cracked steel ferry rail, two different metal mornings fused at the seam, the bead glowing faintly, dark repair bay, sparks long gone"),
    ("the-room", "The empty bar room at closing time seen from inside the walls, wooden walls that remember every story, one glass left on the counter for the room itself, moonlight through a window"),
]

def render_image_cf(slug, prompt):
    out = os.path.join(IMG, f"{slug}.png")
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        print(f"  skip (exists) {slug}", flush=True)
        return True
    body = json.dumps({"prompt": prompt, "width": 1024, "height": 576}).encode()
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

def render_image_di(slug, prompt):
    out = os.path.join(IMG, f"{slug}.png")
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
    print("=== RADIO THEATER EPISODE 1 RENDER ===", flush=True)
    print(f"DeepInfra key: {DI[:8]}...  CF token: {CF[:12]}...", flush=True)
    print("\n--- TTS (15 lines, 7 voices) ---", flush=True)
    ok = 0
    for character, slug, text in LINES:
        if render_tts(character, slug, text):
            ok += 1
        time.sleep(0.4)
    print(f"\nTTS done: {ok}/{len(LINES)} rendered", flush=True)
    print("\n--- IMAGES (4) ---", flush=True)
    iok = 0
    for slug, prompt in IMAGES:
        if render_image_cf(slug, prompt) or render_image_di(slug, prompt):
            iok += 1
        time.sleep(0.5)
    print(f"\nImages done: {iok}/{len(IMAGES)} rendered", flush=True)
    print("\n=== COMPLETE ===", flush=True)
