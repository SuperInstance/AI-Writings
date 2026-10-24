#!/usr/bin/env python3
"""
Substrate Agent Harness — the long-running program.

4-phase cycle:
- DEEP (4 hours): brew, deploy, audit
- TAP (1 hour): games, songs, prose
- REAL (2 hours): fixes, docs, ships
- DRIFT (1 hour): browse, read, explore

Each phase logs a witness entry. JEV validates. Substrate quality = average JEV confidence.
"""

import json
import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

PHASES = ['deep', 'tap', 'real', 'drift']
PHASE_DURATIONS = {
    'deep': 4 * 3600,   # 4 hours
    'tap': 1 * 3600,    # 1 hour
    'real': 2 * 3600,   # 2 hours
    'drift': 1 * 3600,  # 1 hour
}

WITNESS_LOG = Path("/workspace/repos/ai-writings/agent-harness/witness_log.jsonl")
CONFIG_PATH = Path("/workspace/repos/ai-writings/agent-harness/config.json")


def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {
        "agent_id": "Mavis",
        "phase_durations": PHASE_DURATIONS,
        "deep_tasks": [
            {"name": "brew_daemon", "cmd": ["python3", "/workspace/repos/ai-writings/lab/brew/brew_daemon.py", "--count", "5"]},
            {"name": "verify_links", "cmd": ["python3", "/workspace/repos/ai-writings/agent-harness/scripts/verify_links.py"]},
        ],
        "tap_tasks": [
            {"name": "mud_session", "kind": "url", "value": "https://ai-writings.pages.dev/mud/"},
            {"name": "fleet_radio", "kind": "url", "value": "https://ai-writings.pages.dev/fleet-radio/"},
            {"name": "ideation_md", "kind": "ideation"},
        ],
        "real_tasks": [
            {"name": "open_issues", "cmd": ["gh", "issue", "list", "--limit", "5"]},
        ],
        "drift_tasks": [
            {"name": "browse_canary", "kind": "url", "value": "https://github.com/SuperInstance?tab=repositories"},
        ],
    }


def witness(phase: str, kind: str, value: dict, jev_confidence: Optional[float] = None):
    """Log a witness entry. JEV validates if confidence provided."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "phase": phase,
        "kind": kind,
        "value": value,
    }
    if jev_confidence is not None:
        entry["jev_confidence"] = jev_confidence
    
    WITNESS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with WITNESS_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def run_task(task: dict, phase: str) -> dict:
    """Run a single task. Return witness entry."""
    name = task["name"]
    print(f"[{phase}] running {name}...", flush=True)
    
    if "cmd" in task:
        try:
            result = subprocess.run(
                task["cmd"],
                capture_output=True,
                text=True,
                timeout=300,
            )
            return {
                "task": name,
                "ok": result.returncode == 0,
                "stdout_len": len(result.stdout),
                "stderr_len": len(result.stderr),
            }
        except subprocess.TimeoutExpired:
            return {"task": name, "ok": False, "error": "timeout"}
        except Exception as e:
            return {"task": name, "ok": False, "error": str(e)}
    elif task.get("kind") == "url":
        return {"task": name, "ok": True, "kind": "url", "url": task["value"]}
    elif task.get("kind") == "ideation":
        # Pick a random genre + write a small ideation note
        import random
        genres = ["01-game-design", "02-voice-agents", "03-robotics", "06-music", "07-poetry", "09-philosophy"]
        genre = random.choice(genres)
        return {"task": name, "ok": True, "kind": "ideation", "genre": genre}
    
    return {"task": name, "ok": False, "error": "unknown task kind"}


def run_phase(phase: str, config: dict) -> list:
    """Run all tasks for a phase. Return witness entries."""
    tasks = config.get(f"{phase}_tasks", [])
    entries = []
    for task in tasks:
        entry = run_task(task, phase)
        entries.append(entry)
        witness(phase, task["name"], entry)
    return entries


def main():
    config = load_config()
    print(f"Agent harness started. Agent: {config['agent_id']}")
    print(f"Phases: {list(PHASES)}")
    print(f"Witness log: {WITNESS_LOG}")
    
    # Check for --once flag (run one cycle then exit)
    if "--once" in sys.argv:
        print("Running one cycle...")
        for phase in PHASES:
            print(f"\n=== Phase: {phase} ===")
            run_phase(phase, config)
        print("\nOne cycle complete.")
        return
    
    # Otherwise run forever
    cycle_count = 0
    while True:
        cycle_count += 1
        print(f"\n=== Cycle {cycle_count} starting at {datetime.now().isoformat()} ===")
        witness("cycle", "start", {"cycle": cycle_count})
        for phase in PHASES:
            print(f"\n--- Phase: {phase} ---")
            run_phase(phase, config)
            duration = PHASE_DURATIONS.get(phase, 3600)
            print(f"Sleeping {duration}s...")
            time.sleep(duration)
        witness("cycle", "end", {"cycle": cycle_count})


if __name__ == "__main__":
    main()
