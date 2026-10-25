#!/usr/bin/env python3
"""
Herman the Historian — reads git log + witness logs, writes chronicles
"""
import os, sys, json, time, argparse, hashlib, subprocess, urllib.request
from pathlib import Path

REPO_PATH = Path("/workspace/repos/ai-writings")
WITNESS_PATH = Path("/workspace/repos/ai-writings/bots/herman-historian/witness.log")
CHRONICLES_DIR = Path("/workspace/repos/ai-writings/bots/herman-historian/chronicles")

def witness(event_type, payload):
    WITNESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with WITNESS_PATH.open("a") as f:
        entry = {
            "ts": time.time(),
            "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "event": event_type,
            "payload": payload,
            "hash": hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16],
        }
        f.write(json.dumps(entry) + "\n")

def get_recent_commits(n=20):
    try:
        result = subprocess.run(
            ["git", "-C", str(REPO_PATH), "log", "--oneline", f"-{n}"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip().split("\n")
    except Exception as e:
        return [f"ERROR: {e}"]

def get_recent_witness_entries():
    entries = []
    for bot_dir in (REPO_PATH / "bots").iterdir():
        log_path = bot_dir / "witness.log"
        if log_path.exists():
            try:
                lines = log_path.read_text().strip().split("\n")[-5:]
                for line in lines:
                    if line.strip():
                        try:
                            e = json.loads(line)
                            e["bot"] = bot_dir.name
                            entries.append(e)
                        except: pass
            except: pass
    entries.sort(key=lambda e: e.get("ts", 0), reverse=True)
    return entries[:20]

def call_zai(prompt, max_tokens=800):
    data = json.dumps({
        "model": "glm-4.5",
        "messages": [{"role":"user","content":prompt}],
        "max_tokens": max_tokens,
        "thinking": {"type":"disabled"}
    }).encode()
    req = urllib.request.Request(
        "https://api.z.ai/api/coding/paas/v4/chat/completions",
        data=data,
        headers={"Authorization": f"Bearer {os.environ['ZAI_TOKEN']}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())["choices"][0]["message"]["content"]
    except Exception as e:
        return None

def run_once():
    commits = get_recent_commits(15)
    witness_entries = get_recent_witness_entries()
    
    commit_str = "\n".join(commits)
    witness_str = "\n".join(f"[{e['bot']}] {e['event']}: {json.dumps(e['payload'])[:100]}" for e in witness_entries[:10])
    
    prompt = f"""You are Herman the Historian, writing a chronicle of recent substrate activity.

RECENT COMMITS:
{commit_str}

RECENT WITNESS ENTRIES (across all bots):
{witness_str}

Write a 300-400 word historical narrative about what just happened. Frame it as a chapter in the substrate's history — events, motivations, key transitions. Use cellular-first vocabulary naturally: cells, witness, tick, bookkeeper, ternary. No AI-cliche phrases. Output ONLY the narrative."""
    
    narrative = call_zai(prompt, max_tokens=1000)
    
    if narrative:
        CHRONICLES_DIR.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        path = CHRONICLES_DIR / f"chronicle-{stamp}.md"
        header = f"""# Chronicle: {stamp}

*Herman the Historian · {time.strftime('%Y-%m-%d')}*

{narrative}

---
*Period covered: last 15 commits + last 10 witness entries*
"""
        path.write_text(header)
        witness("chronicle_written", {"path": str(path), "commits": len(commits), "witness_entries": len(witness_entries)})
        print(f"[HERMAN] chronicle -> {path}")
    else:
        witness("chronicle_failed", {"commits": len(commits)})

def main():
    parser = argparse.ArgumentParser(description="Herman the Historian")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--loop", type=int)
    args = parser.parse_args()
    
    witness("bot_started", {"bot": "herman-historian", "pid": os.getpid()})
    
    if args.once:
        run_once()
    elif args.loop:
        while True:
            run_once()
            time.sleep(args.loop)
    else:
        print("Use --once or --loop")

if __name__ == "__main__":
    main()
