#!/usr/bin/env python3
"""DeepInfra chat helper — fleet radio production. Reads key from ~/.bashrc itself."""
import json, os, re, sys, urllib.request

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

KEY = get_key()
API = "https://api.deepinfra.com/v1/openai/chat/completions"

def chat(system, user, model="meta-llama/Llama-3.3-70B-Instruct-Turbo", temp=0.8, max_tokens=6000, timeout=540, retries=2):
    last_err = None
    for attempt in range(retries + 1):
        try:
            payload = {
                "model": model,
                "temperature": temp,
                "max_tokens": max_tokens,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            }
            req = urllib.request.Request(
                API,
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json", "Authorization": "Bearer " + KEY},
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.load(r)
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            last_err = e
            print(f"attempt {attempt+1} failed: {e}", file=sys.stderr)
    raise last_err

if __name__ == "__main__":
    print(chat(sys.argv[1] if len(sys.argv) > 1 else "", sys.stdin.read()))
