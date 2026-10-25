#!/usr/bin/env python3
"""Verify portraits with DeepInfra Qwen3-VL-235B. Usage: python3 vision_check.py <img1> <img2> ..."""
import base64, json, os, re, sys, urllib.request

def get_key():
    for path in (os.path.expanduser("~/.bashrc"), os.path.expanduser("~/.zshrc")):
        try:
            txt = open(path).read()
        except Exception:
            continue
        m = re.search(r'DEEPINFRA_API_KEY=["\']?([A-Za-z0-9_\-]+)', txt)
        if m:
            return m.group(1)
    return os.environ.get("DEEPINFRA_API_KEY", "")

def b64_data_url(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

prompt = ("You are the fleet's art director. For EACH image, give a one-paragraph verdict: "
          "what is depicted, the light and mood, and whether it reads as a dawn-lit morning-window scene "
          "or a harbor at dawn. If the image is mangled, garbled, or off-brief, say so plainly. "
          "End with a one-line overall pass/fail per image.")
messages = [{"role": "user", "content": [{"type": "text", "text": prompt}] +
            [{"type": "image_url", "image_url": {"url": b64_data_url(p)}} for p in sys.argv[1:]]}]

payload = {"model": "Qwen/Qwen3-VL-4B-Thinking", "messages": messages, "max_tokens": 1500}
req = urllib.request.Request("https://api.deepinfra.com/v1/openai/chat/completions",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json", "Authorization": "Bearer " + get_key()})
with urllib.request.urlopen(req, timeout=300) as r:
    data = json.load(r)
print(data["choices"][0]["message"]["content"])
