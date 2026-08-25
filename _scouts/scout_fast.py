"""
scout_fast.py — Faster, streaming version. Flushes output.
"""
import urllib.request, urllib.error, json, os, time, sys
from pathlib import Path

GITHUB = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN")

def call(url, token=None):
    headers = {"User-Agent": "scout", "Accept": "application/vnd.github+json"}
    if token: headers["Authorization"] = f"token {token}"
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=15)
        return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "message": e.reason}
    except Exception as e:
        return {"error": str(e)[:80]}

def get_readme(owner, repo, token=None):
    d = call(f"{GITHUB}/repos/{owner}/{repo}/readme", token)
    if "error" in d: return None
    try:
        import base64
        return base64.b64decode(d["content"]).decode("utf-8")
    except Exception:
        return None

def main():
    owner = "SuperInstance"
    # 1. List repos (one paginated call)
    repos = []
    for page in range(1, 4):
        d = call(f"{GITHUB}/users/{owner}/repos?per_page=100&page={page}")
        if "error" in d or not d:
            print(f"  page {page}: stop (error or empty)", flush=True)
            break
        repos.extend(d)
        print(f"  page {page}: {len(d)} repos (running total {len(repos)})", flush=True)
        if len(d) < 100: break

    print(f"\nFound {len(repos)} repos", flush=True)

    # 2. Skip the AI-Writings one (it's just the canon, not a project)
    repos = [r for r in repos if not r.get("fork") and r["name"] not in ("AI-Writings",)]
    print(f"After filtering: {len(repos)} repos", flush=True)

    out = []
    for r in repos:
        name = r["name"]
        readme = get_readme(owner, name, TOKEN)
        if readme is not None and len(readme) > 5000:
            readme = readme[:5000] + "\n\n[... truncated ...]"
        out.append({
            "name": name,
            "lang": r.get("language", ""),
            "desc": r.get("description", ""),
            "size_kb": r.get("size", 0),
            "stars": r.get("stargazers_count", 0),
            "pushed": r.get("pushed_at", ""),
            "topics": r.get("topics", []),
            "readme": readme,
            "html_url": r.get("html_url"),
            "created_at": r.get("created_at", ""),
        })
        print(f"  {name:40} {str(r.get('language') or '?'):10} {r.get('size', 0):>5} KB  stars={r.get('stargazers_count', 0):>2}", flush=True)

    out_path = Path("/workspace/_scouts/prior_art_map.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {out_path} ({out_path.stat().st_size} bytes)", flush=True)

    # 3. Print a connectivity table
    print("\n\nCONNECTIVITY TO POLYFORMALISM CANON:", flush=True)
    keywords = ["polyformalism", "substrate", "cell", "5 opcodes", "BIND", "LINK",
                "EFFECT", "VIEW", "TICK", "cowboy", "machine learning", "rust",
                "haskell", "python", "typescript", "wasm", "compiler", "vm",
                "agent", "llm", "ai", "neural", "transformer"]
    for r in out:
        text = (r["readme"] or "") + " " + (r["desc"] or "") + " " + " ".join(r.get("topics", []))
        text = text.lower()
        hits = [k for k in keywords if k.lower() in text]
        if hits:
            print(f"  {r['name']:40}  ->  {', '.join(hits)}", flush=True)

if __name__ == "__main__":
    main()
