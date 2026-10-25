#!/usr/bin/env python3
"""Champions Day 2026-08-14 — multi-stack renders of the four champion creative pieces.
One hero scene per piece × three stacks (local SDXL-turbo, DeepInfra FLUX, Cloudflare FLUX) + Wan video for the best piece.
"""
import json, os, re, subprocess, sys, time, urllib.request, base64, io

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images")
os.makedirs(OUT, exist_ok=True)

def get_key(name):
    for line in open(os.path.expanduser("~/.bashrc")):
        m = re.search(name + r'="([^"]+)"', line)
        if m: return m.group(1)
    return os.environ.get(name, "")

DI_KEY = get_key("DEEPINFRA_API_KEY")
CF_TOK = ""
for line in open(os.path.expanduser("~/.config/.wrangler/config/default.toml")):
    m = re.search(r'oauth_token="([^"]+)"', line)
    if m: CF_TOK = m.group(1); break
CF_ACCT = "049ff5e84ecf636b53b162cbb580aae6"

# scene prompts — one hero image per piece (rich, cinematic, painterly)
SCENES = {
    "keeper-round": {
        "file": "keeper-round",
        "prompt": "A lighthouse keeper's round at night during a power failure: an old stone lighthouse interior, one hundred sixty-one small oil lamps burning on shelves, a great clockwork mechanism with brass gears turning on its own, a beam of light sweeping across a black glass sea through the window, warm lamplight against deep blue night, cinematic, painterly, detailed",
        "video_prompt": "A lighthouse at night during a power failure. Inside, a single warm beam of light sweeps slowly across the room from a great brass clockwork lamp mechanism, casting moving shadows over rows of small burning oil lamps. Through the window a black sea glitters far below. Slow cinematic pan, warm amber light against deep blue night, painterly, atmospheric",
    },
    "annealing": {
        "file": "annealing",
        "prompt": "Third watch at a glassblower's furnace: a long annealing lehr like a bread oven with a hundred shelves full of glowing glass pieces cooling slowly, a finisher holding a small vase from the glory hole, amber furnace glow, deep shadows, dust motes in the light, cinematic, painterly",
        "video_prompt": "",
    },
    "furnace-night": {
        "file": "furnace-night",
        "prompt": "A mountain glasshouse at night, the road ends here: an annealing kiln glowing softly, seven hundred hand-blown glass vessels in racks being inventoried by an apprentice with a ledger, one knuckle tapping a bowl, cold starlight through a high window meeting warm furnace light, cinematic, painterly",
        "video_prompt": "",
    },
    "chart-of-a-coast": {
        "file": "chart-of-a-coast",
        "prompt": "A coastal cartographer at dusk walking a strand with a board and reed pen, a coastline that rearranges itself like a sleeper turning over — a spit that was a peninsula at noon is an island by supper, harbor mouth shrugging, ink that cannot be persuaded, lantern-lit studio table, sea glass, cinematic, painterly",
        "video_prompt": "",
    },
}

def save_b64_or_url(data, path):
    """Handle base64 / data URL / URL / list responses."""
    if isinstance(data, list):
        data = data[0]
    if isinstance(data, dict):
        for k in ("output", "outputs", "images", "image", "data"):
            if k in data: return save_b64_or_url(data[k], path)
        return False
    if isinstance(data, str):
        if data.startswith("data:"):
            b64 = data.split(",", 1)[1]
            raw = base64.b64decode(b64)
        elif data.startswith("http"):
            req = urllib.request.Request(data)
            raw = urllib.request.urlopen(req, timeout=120).read()
        else:
            raw = base64.b64decode(data)
        with open(path, "wb") as f: f.write(raw)
        return True
    return False

def render_deepinfra(model, prompt, out_path):
    body = json.dumps({"prompt": prompt, "num_inference_steps": 4}).encode()
    req = urllib.request.Request(f"https://api.deepinfra.com/v1/inference/{model}",
        data=body, headers={"Content-Type": "application/json", "Authorization": "Bearer " + DI_KEY})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.load(r)
    for k in ("images", "output"):
        if k in d and save_b64_or_url(d[k], out_path):
            return True
    return False

def render_cloudflare(model, prompt, out_path):
    body = json.dumps({"prompt": prompt}).encode()
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCT}/ai/run/{model}",
        data=body, headers={"Content-Type": "application/json", "Authorization": "Bearer " + CF_TOK})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    res = d.get("result", {})
    img = res.get("image") or res.get("images") or ""
    if isinstance(img, list): img = img[0]
    if isinstance(img, str) and img.startswith("data:"):
        raw = base64.b64decode(img.split(",", 1)[1])
        with open(out_path, "wb") as f: f.write(raw)
        return True
    return False

def render_local(prompt, out_path, seed=42):
    subprocess.run([sys.executable, os.path.join(HERE, "..", "local_render.py"), prompt, out_path, str(seed)],
                   check=True, timeout=300, capture_output=True)
    return os.path.exists(out_path)

results = {}
for key, sc in SCENES.items():
    p = sc["prompt"]
    # 1) local SDXL-turbo
    out = os.path.join(OUT, f"{sc['file']}-local.png")
    try:
        render_local(p, out, seed=42)
        results[f"{key}-local"] = os.path.exists(out)
        print(f"[local] {key}: {results[f'{key}-local']}", flush=True)
    except Exception as e:
        print(f"[local] {key}: FAIL {e}", flush=True)
        results[f"{key}-local"] = False
    # 2) DeepInfra FLUX-1-dev
    out = os.path.join(OUT, f"{sc['file']}-deepinfra.png")
    try:
        results[f"{key}-deepinfra"] = render_deepinfra("black-forest-labs/FLUX-1-dev", p, out)
        print(f"[deepinfra] {key}: {results[f'{key}-deepinfra']}", flush=True)
    except Exception as e:
        print(f"[deepinfra] {key}: FAIL {e}", flush=True)
        results[f"{key}-deepinfra"] = False
    # 3) Cloudflare flux-1-schnell
    out = os.path.join(OUT, f"{sc['file']}-cloudflare.png")
    try:
        results[f"{key}-cloudflare"] = render_cloudflare("@cf/black-forest-labs/flux-1-schnell", p, out)
        print(f"[cloudflare] {key}: {results[f'{key}-cloudflare']}", flush=True)
    except Exception as e:
        print(f"[cloudflare] {key}: FAIL {e}", flush=True)
        results[f"{key}-cloudflare"] = False

# 4) VIDEO — the best piece: The Keeper's Round (Wan2.6-T2V)
vid = os.path.join(HERE, "video")
os.makedirs(vid, exist_ok=True)
vp = SCENES["keeper-round"]["video_prompt"]
body = json.dumps({"prompt": vp}).encode()
req = urllib.request.Request("https://api.deepinfra.com/v1/inference/Wan-AI/Wan2.6-T2V",
    data=body, headers={"Content-Type": "application/json", "Authorization": "Bearer " + DI_KEY})
print("[video] rendering Wan2.6-T2V (can take 1-2 min)...", flush=True)
try:
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.load(r)
    vurl = d.get("video_url") or d.get("output")
    if isinstance(vurl, list): vurl = vurl[0]
    if vurl:
        raw = urllib.request.urlopen(vurl, timeout=180).read()
        vpath = os.path.join(vid, "keeper-round.mp4")
        with open(vpath, "wb") as f: f.write(raw)
        print(f"[video] OK {vpath} ({len(raw)} bytes) cost={d.get('inference_status',{}).get('cost')}", flush=True)
    else:
        print("[video] no url in:", str(d)[:200], flush=True)
except Exception as e:
    print(f"[video] FAIL {e}", flush=True)

print(json.dumps(results))
