"""
indexer.py — Cloudflare Vectorize indexer for the polyformalism canon.

Walks the canon and the polyformalism repo READMEs, chunks them, embeds
via Cloudflare Workers AI, and outputs a JSON file of vectors ready to
batch-upload to a Vectorize index.

Usage:
    python indexer.py [--out canon_vectors.json] [--limit 50] [--types fable,paper,story,readme,test]
    python indexer.py --emit-search-handler  # writes search_handler.js

Without a CF_API_TOKEN, falls back to writing chunks without vectors
(metadata only) so the indexer is still useful for planning.

Workers AI endpoint:
    POST https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/baai/bge-base-en-v1.5
    Headers: Authorization: Bearer {CF_API_TOKEN}
    Body: {"text": "..."}
    Returns: {"result": {"shape": [1, 768], "data": [[0.012, -0.034, ...]]}}
"""
import os
import json
import argparse
import re
import sys
import time
from pathlib import Path

# Config
CF_API_TOKEN = os.environ.get("CF_API_TOKEN", "")
CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID", "")
CF_AI_MODEL = "@cf/baai/bge-base-en-v1.5"
CHUNK_SIZE = 500  # tokens
CHUNK_OVERLAP = 50

# Paths
CANON_ROOT = Path("/workspace/ai-writings-new/seed-canon")
REPO_ROOT = Path("/workspace")


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list:
    """Naive chunker by words (approximates tokens). 500 words ~ 600-700 tokens."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]
        if not chunk:
            break
        chunks.append(" ".join(chunk))
        if i + chunk_size >= len(words):
            break
        i += chunk_size - overlap
    return chunks


def extract_sections(markdown: str) -> list:
    """Extract sections by ## headers."""
    sections = []
    current = {"title": "", "text": ""}
    for line in markdown.split("\n"):
        m = re.match(r"^#{1,3}\s+(.+)$", line)
        if m:
            if current["text"].strip():
                sections.append(current)
            current = {"title": m.group(1).strip(), "text": ""}
        else:
            current["text"] += line + "\n"
    if current["text"].strip():
        sections.append(current)
    return sections


def walk_canon() -> list:
    """Walk the AI-Writings seed-canon. Returns list of {id, text, metadata} chunks."""
    chunks = []

    # Fables
    for f in sorted((CANON_ROOT / "fables").glob("fable-*.md")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        # Title
        m = re.match(r"^#\s+(.+)$", text, re.MULTILINE)
        title = m.group(1) if m else f.stem
        for i, chunk in enumerate(chunk_text(text)):
            chunks.append({
                "id": f"fable-{f.stem}-{i}",
                "text": chunk[:2000],  # cap at 2000 chars
                "metadata": {
                    "type": "fable",
                    "title": title,
                    "path": str(f.relative_to(REPO_ROOT)),
                }
            })

    # Papers
    for f in sorted((CANON_ROOT / "papers").glob("paper-*.md")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        m = re.match(r"^#\s+(.+)$", text, re.MULTILINE)
        title = m.group(1) if m else f.stem
        for i, chunk in enumerate(chunk_text(text)):
            chunks.append({
                "id": f"paper-{f.stem}-{i}",
                "text": chunk[:2000],
                "metadata": {
                    "type": "paper",
                    "title": title,
                    "path": str(f.relative_to(REPO_ROOT)),
                }
            })

    # Stories
    for f in sorted((CANON_ROOT / "stories").glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        m = re.match(r"^#\s+(.+)$", text, re.MULTILINE)
        title = m.group(1) if m else f.stem
        for i, chunk in enumerate(chunk_text(text)):
            chunks.append({
                "id": f"story-{f.stem}-{i}",
                "text": chunk[:2000],
                "metadata": {
                    "type": "story",
                    "title": title,
                    "path": str(f.relative_to(REPO_ROOT)),
                }
            })

    return chunks


def walk_repos() -> list:
    """Walk the polyformalism repo READMEs. Returns list of chunks."""
    chunks = []
    for readme in sorted(REPO_ROOT.glob("quilt-*/README.md")):
        text = readme.read_text(encoding="utf-8", errors="ignore")
        # First heading as title
        m = re.match(r"^#\s+(.+)$", text, re.MULTILINE)
        title = m.group(1) if m else readme.parent.name
        # Chunk by section
        for i, chunk in enumerate(chunk_text(text, chunk_size=400, overlap=40)):
            chunks.append({
                "id": f"readme-{readme.parent.name}-{i}",
                "text": chunk[:2000],
                "metadata": {
                    "type": "readme",
                    "title": title,
                    "repo": readme.parent.name,
                    "path": str(readme.relative_to(REPO_ROOT)),
                }
            })
    return chunks


def walk_tests() -> list:
    """Walk test function names. Returns list of chunks."""
    chunks = []
    for testfile in sorted(REPO_ROOT.glob("quilt-*/tests/test_*.py")):
        repo = testfile.parent.parent.name
        try:
            text = testfile.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # Find all def test_* names
        for m in re.finditer(r"def\s+(test_\w+)\s*\(", text):
            name = m.group(1)
            chunks.append({
                "id": f"test-{repo}-{name}",
                "text": f"Test: {name} in {repo}",
                "metadata": {
                    "type": "test",
                    "name": name,
                    "repo": repo,
                    "path": str(testfile.relative_to(REPO_ROOT)),
                }
            })
    return chunks


def embed_via_workers_ai(text: str) -> list:
    """Call Cloudflare Workers AI to embed. Returns 768-dim vector."""
    if not CF_API_TOKEN or not CF_ACCOUNT_ID:
        return None
    import urllib.request
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/{CF_AI_MODEL}"
    body = json.dumps({"text": text}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    return data.get("result", {}).get("data", [[]])[0]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="/workspace/_scouts/canon_vectors.json")
    p.add_argument("--limit", type=int, default=None, help="Limit chunks (for testing)")
    p.add_argument("--types", default="fable,paper,story,readme,test", help="Comma-separated types to include")
    p.add_argument("--emit-search-handler", action="store_true")
    args = p.parse_args()

    types = set(args.types.split(","))
    all_chunks = []
    if "fable" in types or "paper" in types or "story" in types:
        print("Walking canon...")
        canon = walk_canon()
        print(f"  {len(canon)} chunks from fables/papers/stories")
        all_chunks.extend(canon)
    if "readme" in types:
        print("Walking repos...")
        repos = walk_repos()
        print(f"  {len(repos)} chunks from repo READMEs")
        all_chunks.extend(repos)
    if "test" in types:
        print("Walking tests...")
        tests = walk_tests()
        print(f"  {len(tests)} test name chunks")
        all_chunks.extend(tests)

    if args.limit:
        all_chunks = all_chunks[:args.limit]
        print(f"Limited to {len(all_chunks)} chunks")

    print(f"Total chunks: {len(all_chunks)}")

    if CF_API_TOKEN and CF_ACCOUNT_ID:
        print("Embedding via Workers AI...")
        for i, chunk in enumerate(all_chunks):
            try:
                chunk["vector"] = embed_via_workers_ai(chunk["text"])
            except Exception as e:
                print(f"  [{i}] failed: {e}")
                chunk["vector"] = None
            if i % 10 == 0:
                print(f"  [{i}/{len(all_chunks)}]")
            time.sleep(0.05)  # rate limit
    else:
        print("No CF_API_TOKEN — writing chunks without vectors (metadata only)")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(all_chunks, f, indent=2)
    print(f"Wrote {out} ({out.stat().st_size} bytes)")

    if args.emit_search_handler:
        handler = '''// search_handler.js — Cloudflare Worker for the canon semantic search
// Bind in wrangler.toml:
//   [[vectorize]] binding = "CANON" index_name = "quilt-canon-embeddings"
//   [[ai]] binding = "AI"

export async function handleSearch(request, env) {
  const { query, topK = 10 } = await request.json();

  // Embed the query
  const embedding = await env.AI.run("@cf/baai/bge-base-en-v1.5", { text: query });
  const vector = embedding.data[0];

  // Search Vectorize
  const matches = await env.CANON.query(vector, { topK, returnMetadata: true });

  return new Response(JSON.stringify(matches, null, 2), {
    headers: { "Content-Type": "application/json" }
  });
}

export async function handleEmbed(request, env) {
  const { text } = await request.json();
  const embedding = await env.AI.run("@cf/baai/bge-base-en-v1.5", { text });
  return new Response(JSON.stringify(embedding, null, 2), {
    headers: { "Content-Type": "application/json" }
  });
}
'''
        handler_path = Path("/workspace/_scouts/search_handler.js")
        with open(handler_path, "w") as f:
            f.write(handler)
        print(f"Wrote {handler_path}")


if __name__ == "__main__":
    main()
