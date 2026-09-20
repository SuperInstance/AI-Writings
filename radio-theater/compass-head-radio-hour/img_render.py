#!/usr/bin/env python3
"""Image renderer — DeepInfra FLUX + Cloudflare Workers AI. Reads keys itself."""
import base64, json, os, re, sys, urllib.request, urllib.parse

def get_deepinfra_key():
    txt = open(os.path.expanduser("~/.bashrc")).read()
    m = re.search(r'DEEPINFRA_API_KEY=["\']?([A-Za-z0-9_\-]+)', txt)
    return m.group(1) if m else os.environ.get("DEEPINFRA_API_KEY", "")

def get_cf_token():
    try:
        txt = open("/home/eileen/.config/.wrangler/config/default.toml").read()
        m = re.search(r'oauth_token\s*=\s*["\']([^"\']+)', txt)
        return m.group(1) if m else ""
    except Exception:
        return ""

CF_ACCOUNT = "049ff5e84ecf636b53b162cbb580aae6"

def deepinfra_flux(prompt, out_path, model="black-forest-labs/FLUX-1-schnell", width=1024, height=1024, steps=4):
    key = get_deepinfra_key()
    body = json.dumps({"prompt": prompt, "width": width, "height": height, "num_inference_steps": steps}).encode()
    req = urllib.request.Request(
        f"https://api.deepinfra.com/v1/inference/{model}",
        data=body, headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
    if "output" in data:
        b64 = data["output"]
        if isinstance(b64, list): b64 = b64[0]
        if b64.startswith("data:"): b64 = b64.split(",", 1)[1]
        open(out_path, "wb").write(base64.b64decode(b64))
        return f"OK {out_path}"
    return f"ERR keys={list(data.keys())[:5]}"

def cloudflare_flux(prompt, out_path, steps=4):
    token = get_cf_token()
    body = json.dumps({"prompt": prompt, "steps": steps}).encode()
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT}/ai/run/@cf/black-forest-labs/flux-1-schnell",
        data=body, headers={"Content-Type": "application/json", "Authorization": "Bearer " + token})
    with urllib.request.urlopen(req, timeout=240) as r:
        data = json.load(r)
    if data.get("success") and data.get("result", {}).get("image"):
        open(out_path, "wb").write(base64.b64decode(data["result"]["image"]))
        return f"OK {out_path}"
    return f"ERR {json.dumps(data)[:200]}"

if __name__ == "__main__":
    which, prompt, out = sys.argv[1], sys.argv[2], sys.argv[3]
    if which == "di":
        print(deepinfra_flux(prompt, out))
    elif which == "cf":
        print(cloudflare_flux(prompt, out))
