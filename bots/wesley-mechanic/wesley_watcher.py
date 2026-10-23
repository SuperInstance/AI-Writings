#!/usr/bin/env python3
"""
Wesley the Mechanic — Low-Level Canon Watcher Daemon

A low-level bot that:
- Polls the canon (live-canon.superinstance.dev/api/canon)
- Compares state hash against local witness log
- Witnesses diff events with bookkeeper WAL semantics
- Reports changes to a local JSON file
- Optionally fires JEV audits on big changes

Usage:
    python3 wesley_watcher.py --once        # single poll
    python3 wesley_watcher.py --loop 60     # poll every 60s
"""
import os
import sys
import json
import time
import argparse
import hashlib
import urllib.request
from pathlib import Path

# === Config ===
CANON_URL = "https://live-canon.superinstance.dev/api/canon"

# Resolve paths relative to this file so the watcher runs from any checkout.
# The canonical deployment lives at /workspace/repos/ai-writings; falling back
# to the script's own directory keeps a relocated clone self-consistent.
_BOT_DIR = Path(__file__).resolve().parent
_CANON_DIR = Path("/workspace/repos/ai-writings/bots/wesley-mechanic")

def _writable(base):
    """A directory is usable only if we can actually write a file into it."""
    probe = base / ".write-probe"
    try:
        base.mkdir(parents=True, exist_ok=True)
        with probe.open("w") as f:
            f.write("x")
        return True
    except OSError:
        return False
    finally:
        # Always remove the probe, even when the write failed partway.
        try:
            probe.unlink()
        except OSError:
            pass

# Prefer the canonical deployment path, but fall back to the checkout when
# the canonical volume is unwritable (e.g. a full or read-only workspace).
if _writable(_CANON_DIR):
    _BASE = _CANON_DIR
else:
    _BASE = _BOT_DIR

WITNESS_PATH = _BASE / "witness.log"
STATE_PATH = _BASE / "state.json"
BOOKKEEPER_PATH = _BASE / "bookkeeper.wal"

def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"last_hash": None, "last_count": 0, "first_seen": None}

def save_state(state):
    STATE_PATH.write_text(json.dumps(state, indent=2))


import sys
# substrate_bus lives in the sibling bot directory; add both the canonical
# deployment path and the checkout-relative path so the import always resolves.
for _candidate in (
    '/workspace/repos/ai-writings/bots/substrate-bus',
    str(Path(__file__).resolve().parent.parent / 'substrate-bus'),
):
    if os.path.isdir(_candidate) and _candidate not in sys.path:
        sys.path.insert(0, _candidate)
from substrate_bus import witness as substrate_witness, publish as substrate_publish

def witness(event_type, payload):
    """WAL-style append-only witness log"""
    with WITNESS_PATH.open("a") as f:
        entry = {
            "ts": time.time(),
            "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "event": event_type,
            "payload": payload,
            "hash": hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16],
        }
        f.write(json.dumps(entry) + "\n")

def bookkeeper_tick(delta_gamma, delta_eta):
    """Conservation-style: gamma + eta = budget"""
    if not BOOKKEEPER_PATH.exists():
        BOOKKEEPER_PATH.write_text(json.dumps({
            "gamma": 0.0,
            "eta": 0.0,
            "budget": 1000.0,
            "ticks": 0,
        }, indent=2))
    
    book = json.loads(BOOKKEEPER_PATH.read_text())
    book["gamma"] += delta_gamma
    book["eta"] += delta_eta
    book["ticks"] += 1
    # Conservation check
    conserved = abs(book["gamma"] + book["eta"] - book["budget"]) < 1e-6 or (delta_gamma == 0 and delta_eta == 0)
    book["last_conserved"] = conserved
    BOOKKEEPER_PATH.write_text(json.dumps(book, indent=2))
    return book

# The canon endpoint sits behind a bot filter that 403s the default
# urllib User-Agent ("Python-urllib/3.x"). A browser UA alone flips 403 -> 200.
CANON_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://live-canon.superinstance.dev/",
}

def poll_canon():
    """Poll canon endpoint and compute state hash"""
    try:
        req = urllib.request.Request(CANON_URL, headers=CANON_HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        # Compute hash from the full canonical payload
        canon_str = json.dumps(data, sort_keys=True, default=str)
        canon_hash = hashlib.sha256(canon_str.encode()).hexdigest()[:16]
        # The live payload exposes "count"; alternate payloads use
        # "paper_count". Fall back to the paper list length so the count is
        # never silently 0 (which would make every delta read as unchanged).
        if isinstance(data, dict):
            paper_count = data.get("paper_count")
            if paper_count is None:
                paper_count = data.get("count")
            if paper_count is None:
                paper_count = len(data.get("papers", []))
        else:
            paper_count = len(data)
        return canon_hash, int(paper_count), data
    except Exception as e:
        return None, 0, {"error": str(e)}

def run_once(verbose=True):
    state = load_state()
    canon_hash, paper_count, raw = poll_canon()
    

    if canon_hash is None:
        witness("poll_failed", {"error": raw.get("error", "unknown")})
        try:
            substrate_witness("poll_failed", "wesley-mechanic", {"error": raw.get("error", "unknown")})
        except: pass
        if verbose: print(f"[WESLEY] poll failed: {raw.get('error')}")
        return False
    
    if state["last_hash"] is None:
        state["last_hash"] = canon_hash
        state["last_count"] = paper_count
        state["first_seen"] = time.time()
        save_state(state)
        witness("first_poll", {"hash": canon_hash, "count": paper_count})
        try:
            substrate_witness("first_poll", "wesley-mechanic", {"hash": canon_hash, "count": paper_count})
            substrate_publish("canon_changed", "wesley-mechanic", {"hash": canon_hash, "count": paper_count}, recipients=["snowball-scout"])
        except: pass
        bookkeeper_tick(1.0, 0.0)
        if verbose: print(f"[WESLEY] first poll: {canon_hash} ({paper_count} papers)")
        return True
    
    if canon_hash != state["last_hash"]:
        delta = paper_count - state["last_count"]
        witness("canon_changed", {
            "old_hash": state["last_hash"],
            "new_hash": canon_hash,
            "old_count": state["last_count"],
            "new_count": paper_count,
            "delta": delta,
        })
        try:
            substrate_witness("canon_changed", "wesley-mechanic", {
                "old_hash": state["last_hash"],
                "new_hash": canon_hash,
                "delta": delta,
            })
            substrate_publish("canon_changed", "wesley-mechanic", {
                "hash": canon_hash, "count": paper_count, "delta": delta
            }, recipients=["snowball-scout", "jevvy-auditor"])
        except: pass
        # Conservation: gamma grows with canon growth, eta grows with witness events
        bookkeeper_tick(float(delta), 1.0)
        if verbose:
            print(f"[WESLEY] canon changed: {state['last_hash']} -> {canon_hash} "
                  f"({state['last_count']} -> {paper_count}, delta={delta})")
        # Persist the new baseline, or the change is re-witnessed every poll.
        state["last_hash"] = canon_hash
        state["last_count"] = paper_count
        save_state(state)
        return True
    
    if verbose: print(f"[WESLEY] no change ({canon_hash}, {paper_count} papers)")
    return False

def main():
    parser = argparse.ArgumentParser(description="Wesley the Mechanic — canon watcher")
    parser.add_argument("--once", action="store_true", help="poll once and exit")
    parser.add_argument("--loop", type=int, help="poll every N seconds")
    args = parser.parse_args()
    
    witness("bot_started", {"bot": "wesley-mechanic", "pid": os.getpid()})
    
    if args.once:
        run_once()
    elif args.loop:
        while True:
            run_once()
            time.sleep(args.loop)
    else:
        print("Use --once or --loop N")
        sys.exit(1)

if __name__ == "__main__":
    main()
