#!/usr/bin/env python3
"""DeepInfra FLUX image render — usage: python3 img_render2.py '<prompt>' <out.png> [model]"""
import base64, json, os, sys, urllib.request

def get_key():
    key = ""
    for line in open(os.path.expanduser("~/.bashrc")):
        if "DEEPINFRA_API_KEY" in line and "=" in line:
            key = line.split("=", 1)[1].strip().strip('"').strip("'").strip()
            break
    return key or os.environ.get("DEEPINFRA_API_KEY", "")

key = get_key()
prompt, out = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "black-forest-labs/FLUX-1-schnell"
body = json.dumps({"prompt": prompt, "width": 832, "height": 832, "num_inference_steps": 4}).encode()
req = urllib.request.Request(f"https://api.deepinfra.com/v1/inference/{model}",
    data=body, headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
with urllib.request.urlopen(req, timeout=300) as r:
    data = json.load(r)
b64 = data.get("output") or data.get("images") or data.get("outputs")
if isinstance(b64, list):
    b64 = b64[0]
if isinstance(b64, dict):
    b64 = b64.get("data") or b64.get("url") or ""
if isinstance(b64, str) and b64.startswith("data:"):
    b64 = b64.split(",", 1)[1]
if isinstance(b64, str) and b64.startswith("http"):
    with urllib.request.urlopen(b64, timeout=120) as ir:
        open(out, "wb").write(ir.read())
else:
    open(out, "wb").write(base64.b64decode(b64))
print("OK " + out)
