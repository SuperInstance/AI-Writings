#!/usr/bin/env python3
"""Vectorize the curated ai-writings canon into index 'ai-writings-canon'.

Crash-proof placement: lives on ext4 (tools/), resume log on ext4 too.
Usage: nohup python3 tools/vectorize-canon.py > /tmp/vectorize-canon.log 2>&1 &
Resume: tools/vectorize-done.ids (chunk ids already inserted).
"""
import hashlib, json, os, re, sys, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = re.search(r'oauth_token = "([^"]+)"',
                  open(os.path.expanduser('~/.wrangler/config/default.toml')).read()).group(1)
ACC = "049ff5e84ecf636b53b162cbb580aae6"
INDEX = "ai-writings-canon"
DONE = os.path.join(ROOT, "tools", "vectorize-done.ids")
DIRS = ["papers", "seed-canon", "zkcanvas-visions", "doctrine", "research", "identity", "docs"]
EMBED_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACC}/ai/run/@cf/baai/bge-m3"
INSERT_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACC}/vectorize/v2/indexes/{INDEX}/insert"

def post(url, payload, timeout=90):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429,) and attempt < 2:
                time.sleep(5 * (attempt + 1)); continue
            return e.code, e.read()[:300].decode(errors="replace")
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < 2:
                time.sleep(5); continue
            raise

def chunks_of(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    text = re.sub(r"---\n.*?\n---\n", "", text, count=1, flags=re.S)  # strip frontmatter
    parts = [p.strip() for p in re.split(r"\n## ", text) if len(p.strip()) > 200]
    if not parts:
        parts = [text[i:i+1500] for i in range(0, len(text), 1400) if len(text[i:i+1500]) > 200]
    out = []
    for i, p in enumerate(parts):
        cid = hashlib.sha1(f"{path}::{i}".encode()).hexdigest()[:16]
        out.append({"id": f"v2::{cid}", "path": os.path.relpath(path, ROOT),
                    "chunk": i, "text": p[:1200], "body": p[:2000]})
    return out

def main():
    done = set()
    if os.path.exists(DONE):
        done = set(l.strip() for l in open(DONE) if l.strip())
    files = []
    for d in DIRS:
        for dirpath, _, names in os.walk(os.path.join(ROOT, d)):
            for n in names:
                if n.endswith(".md"):
                    files.append(os.path.join(dirpath, n))
    print(f"{len(files)} files", flush=True)
    nodes = []
    for f in files:
        nodes.extend(chunks_of(f))
    nodes = [n for n in nodes if n["id"] not in done]
    print(f"{len(nodes)} chunks to insert ({len(done)} already done)", flush=True)
    B = 64
    for i in range(0, len(nodes), B):
        batch = nodes[i:i+B]
        texts = [n["body"] for n in batch]
        s, emb = post(EMBED_URL, {"text": texts})
        if s != 200:
            print(f"EMBED FAIL @{i}: {s} {emb}", flush=True); time.sleep(10); continue
        vecs = [{"id": n["id"], "values": v,
                 "metadata": {"path": n["path"], "chunk": n["chunk"], "text": n["text"]}}
                for n, v in zip(batch, emb["result"]["data"])]
        s, ins = post(INSERT_URL, {"vectors": vecs})
        if s != 200:
            print(f"INSERT FAIL @{i}: {s} {ins}", flush=True); time.sleep(10); continue
        with open(DONE, "a") as fh:
            for n in batch:
                fh.write(n["id"] + "\n")
        if (i // B) % 10 == 0:
            print(f"{i + len(batch)}/{len(nodes)}", flush=True)
    print("COMPLETE", flush=True)

if __name__ == "__main__":
    main()
