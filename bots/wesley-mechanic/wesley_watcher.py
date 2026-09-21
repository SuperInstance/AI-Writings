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
WITNESS_PATH = Path("/workspace/repos/ai-writings/bots/wesley-mechanic/witness.log")
STATE_PATH = Path("/workspace/repos/ai-writings/bots/wesley-mechanic/state.json")
BOOKKEEPER_PATH = Path("/workspace/repos/ai-writings/bots/wesley-mechanic/bookkeeper.wal")

def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"last_hash": None, "last_count": 0, "first_seen": None}

def save_state(state):
    STATE_PATH.write_text(json.dumps(state, indent=2))


import sys
sys.path.insert(0, '/workspace/repos/ai-writings/bots/substrate-bus')
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

def poll_canon():
    """Poll canon endpoint and compute state hash"""
    try:
        with urllib.request.urlopen(CANON_URL, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        # Compute hash from paper_count + a sample
        canon_str = json.dumps(data, sort_keys=True, default=str)
        canon_hash = hashlib.sha256(canon_str.encode()).hexdigest()[:16]
        paper_count = data.get("paper_count", 0) if isinstance(data, dict) else len(data)
        return canon_hash, paper_count, data
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
        if verbose: print(f"[WESLEY] poll failed: {raw.get('error')}")
        return False
    
    if state["last_hash"] is None:
        # First poll
        state["last_hash"] = canon_hash
        state["last_count"] = paper_count
        state["first_seen"] = time.time()
        save_state(state)
        witness("first_poll", {"hash": canon_hash, "count": paper_count})
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
        # Conservation: gamma grows with canon growth, eta grows with witness events
        bookkeeper_tick(float(delta), 1.0)
        if verbose:
            print(f"[WESLEY] canon changed: {state['last_hash']} -> {canon_hash} ({state['last_count']} -> {paper_count}, delta={delta})")
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
