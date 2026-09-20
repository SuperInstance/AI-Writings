"""
scout_sorted.py — Walk github.com/SuperInstance sorted by recency.
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
        return {"error": e.code}
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
    # Get ALL repos with proper sort
    repos = []
    for page in range(1, 6):
        d = call(f"{GITHUB}/users/{owner}/repos?per_page=100&page={page}&sort=pushed&direction=desc")
        if "error" in d or not d:
            break
        repos.extend(d)
        print(f"  page {page}: {len(d)} (total {len(repos)})", flush=True)
        if len(d) < 100: break

    print(f"\nFound {len(repos)} repos total", flush=True)
    print(f"Filtered: {sum(1 for r in repos if not r.get('fork') and r['name'] not in ('AI-Writings',))} non-fork\n", flush=True)

    # Skip forks
    repos = [r for r in repos if not r.get("fork") and r["name"] not in ("AI-Writings",)]

    # Fetch README for each (in parallel via threads to speed up)
    import concurrent.futures
    def fetch_meta(r):
        name = r["name"]
        readme = get_readme(owner, name, TOKEN)
        if readme is not None and len(readme) > 6000:
            readme = readme[:6000] + "\n\n[... truncated ...]"
        return {
            "name": name,
            "lang": r.get("language"),
            "desc": r.get("description", ""),
            "size_kb": r.get("size", 0),
            "stars": r.get("stargazers_count", 0),
            "pushed": r.get("pushed_at", ""),
            "topics": r.get("topics", []),
            "readme": readme,
            "html_url": r.get("html_url"),
            "created_at": r.get("created_at", ""),
        }

    out = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for i, m in enumerate(ex.map(fetch_meta, repos)):
            out.append(m)
            print(f"  [{i+1:3}/{len(repos)}] {m['name']:40} {str(m['lang'] or '?'):10} {m['size_kb']:>5}KB", flush=True)

    out_path = Path("/workspace/_scouts/prior_art_sorted.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {out_path}", flush=True)

if __name__ == "__main__":
    main()
