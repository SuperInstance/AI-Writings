#!/usr/bin/env python3
"""Render one prompt across MANY different DeepInfra models for visual variety.
Handles all response shapes: base64, data URL, image_url, images list.
Usage: python3 multi_render.py <prompt> <out_dir> [seed_base]
"""
import base64, json, os, sys, urllib.request

def get_key():
    for line in open(os.path.expanduser("~/.bashrc")):
        if "DEEPINFRA_API_KEY" in line and "=" in line:
            return line.split("=", 1)[1].strip().strip('"').strip("'").strip()
    return os.environ.get("DEEPINFRA_API_KEY", "")

MODELS = [
    "black-forest-labs/FLUX-2-pro",
    "black-forest-labs/FLUX-1.1-pro",
    "black-forest-labs/FLUX-1-dev",
    "black-forest-labs/FLUX-2-klein-9b",
    "stabilityai/sdxl-turbo",
    "Qwen/Qwen-Image-Max",
    "PrunaAI/p-image",
]

def fetch_b64(data):
    """Extract a base64 image or URL from any response shape."""
    for key in ("output", "outputs", "images", "image", "data"):
        if key in data:
            v = data[key]
            if isinstance(v, list):
                if v:
                    v = v[0]
                else:
                    continue
            if isinstance(v, dict):
                v = v.get("data") or v.get("url") or v.get("image_url") or ""
            if isinstance(v, str):
                if v.startswith("data:"):
                    return v.split(",", 1)[1], None
                if v.startswith("http"):
                    return None, v
                return v, None
    if "image_url" in data:
        return None, data["image_url"]
    return None, None

def render(model, prompt, out_path, seed):
    steps = 4 if "turbo" in model else 25
    body = json.dumps({"prompt": prompt, "width": 832, "height": 832,
                       "num_inference_steps": steps, "seed": seed}).encode()
    req = urllib.request.Request(f"https://api.deepinfra.com/v1/inference/{model}",
        data=body, headers={"Content-Type": "application/json", "Authorization": "Bearer " + get_key()})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.load(r)
        b64, url = fetch_b64(data)
        if url:
            with urllib.request.urlopen(url, timeout=180) as ir:
                open(out_path, "wb").write(ir.read())
        elif b64:
            open(out_path, "wb").write(base64.b64decode(b64))
        else:
            print(f"NO-IMAGE {model}", flush=True)
            return False
        print(f"OK {model.split('/')[-1]} -> {out_path}", flush=True)
        return True
    except Exception as e:
        print(f"ERR {model}: {e}", flush=True)
        return False

if __name__ == "__main__":
    prompt, out_dir = sys.argv[1], sys.argv[2]
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 777
    os.makedirs(out_dir, exist_ok=True)
    for i, m in enumerate(MODELS):
        name = m.split("/")[-1].replace("/", "-")
        render(m, prompt, os.path.join(out_dir, f"{i:02d}-{name}.png"), seed + i)
