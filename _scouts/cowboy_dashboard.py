#!/usr/bin/env python3
"""
cowboy_dashboard.py — The cowboy's view of the task queue + worklog.

This is what the parent session reads at the start of every turn
to know what's happening across the workers.

Usage:
    cowboy_dashboard.py           # show the full state
    cowboy_dashboard.py --compact # one-screen summary
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

QUEUE_PATH = Path("/workspace/_scouts/task_queue.json")
WORKLOG_PATH = Path("/workspace/_scouts/worklog.md")


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def time_ago(iso):
    if not iso:
        return "—"
    try:
        then = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - then
        s = int(delta.total_seconds())
        if s < 60: return f"{s}s ago"
        if s < 3600: return f"{s // 60}m ago"
        if s < 86400: return f"{s // 3600}h ago"
        return f"{s // 86400}d ago"
    except Exception:
        return iso


def main():
    compact = "--compact" in sys.argv

    if not QUEUE_PATH.exists():
        print("No task queue yet. Run: python3 /workspace/_scouts/task_queue.py init")
        return

    q = json.loads(QUEUE_PATH.read_text())
    tasks = q["tasks"]

    if not compact:
        print("=" * 70)
        print("THE COWBOY'S DASHBOARD")
        print("=" * 70)
        print()

    # Stats
    by_status = {}
    by_worker = {}
    for t in tasks:
        by_status[t["status"]] = by_status.get(t["status"], 0) + 1
        by_worker[t["worker"]] = by_worker.get(t["worker"], 0) + 1
    total_tokens = sum(t.get("tokens_used", 0) for t in tasks)
    print(f"=== Queue: {len(tasks)} tasks ===")
    print(f"  by status: {by_status}")
    print(f"  by worker: {by_worker}")
    print(f"  total tokens: {total_tokens:,}")
    print()

    # Pending tasks (the cowboy's next moves)
    pending = [t for t in tasks if t["status"] == "pending"]
    if pending:
        print(f"=== {len(pending)} pending ===")
        for t in pending:
            deps = f" (deps: {','.join(t['depends_on'])})" if t["depends_on"] else ""
            print(f"  {t['id']:8s} {t['type']:8s} via {t['worker']:12s}{deps}")
            print(f"           {t['prompt'][:80]}{'...' if len(t['prompt']) > 80 else ''}")
        print()
    else:
        print("=== No pending tasks ===")
        print()

    # In progress
    in_progress = [t for t in tasks if t["status"] == "in_progress"]
    if in_progress and not compact:
        print(f"=== {len(in_progress)} in progress ===")
        for t in in_progress:
            print(f"  {t['id']:8s} via {t['worker']:12s} (started {time_ago(t['started_at'])})")
        print()

    # Recently done
    done = sorted(
        [t for t in tasks if t["status"] == "done"],
        key=lambda t: t.get("completed_at") or "",
        reverse=True,
    )
    if done and not compact:
        print(f"=== {len(done)} done (showing last 5) ===")
        for t in done[:5]:
            print(f"  {t['id']:8s} via {t['worker']:12s} ({time_ago(t['completed_at'])})")
            if t.get("result_summary"):
                print(f"           {t['result_summary'][:80]}")
        print()

    # Failed
    failed = [t for t in tasks if t["status"] == "failed"]
    if failed and not compact:
        print(f"=== {len(failed)} failed (re-dispatch?) ===")
        for t in failed:
            print(f"  {t['id']:8s} via {t['worker']:12s}: {t.get('error', '?')[:80]}")
        print()

    # Worklog tail
    if WORKLOG_PATH.exists():
        lines = WORKLOG_PATH.read_text().strip().split("\n")
        n = 5 if compact else 12
        print(f"=== Worklog (last {min(n, len(lines))} lines) ===")
        for line in lines[-n:]:
            print(f"  {line[:120]}")
        print()

    # Next actions for the cowboy
    print("=== Next actions for the cowboy ===")
    if pending:
        print(f"  - {len(pending)} pending task(s) waiting for workers")
        for t in pending[:3]:
            print(f"    * {t['id']}: dispatch to {t['worker']} via 'python3 task_queue.py run --worker={t['worker']}'")
    if failed:
        print(f"  - {len(failed)} failed task(s) need re-routing")
    if not pending and not failed:
        print("  - queue is clear; add new tasks:")
        print("    python3 task_queue.py add T-NNN essay '...prompt...' --output=path")
    print()


if __name__ == "__main__":
    main()
