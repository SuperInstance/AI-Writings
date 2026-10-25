#!/usr/bin/env python3
"""
task_queue.py — Persistent task queue for the cowboy's workers.

A JSON file at /workspace/_scouts/task_queue.json holds in-flight work.
Workers (API agents, subagents) poll the queue, pick up tasks, and
write results back. The parent session adds tasks and reads the
worklog.

Usage:
    task_queue.py init                    # create the queue + worklog
    task_queue.py add T-001 essay "..."  # add a task
    task_queue.py add T-002 code "..." --worker=deepseek --output=path
    task_queue.py list                    # show all tasks
    task_queue.py pending                 # show only pending tasks
    task_queue.py run --worker=zai       # run a worker (polls forever)
    task_queue.py take T-001 --worker=zai  # atomically claim a task
    task_queue.py done T-001 "summary..."  # mark a task done
    task_queue.py fail T-001 "error..."    # mark a task failed
    task_queue.py tail                    # show the last 20 worklog lines
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

QUEUE_PATH = Path("/workspace/_scouts/task_queue.json")
WORKLOG_PATH = Path("/workspace/_scouts/worklog.md")
MULTI_API_PATH = Path("/workspace/_scouts/multi_api.py")

# Worker voice profiles — what each worker is good at.
VOICE_PROFILES = {
    "zai": {
        "name": "ZAI GLM-4.5-Air",
        "specialty": "flagship creative, narrative, dense prose",
        "rate_limited": True,
    },
    "deepseek": {
        "name": "DeepSeek",
        "specialty": "code, technical, structured spec",
        "rate_limited": False,
    },
    "qwen": {
        "name": "Qwen-72B (SiliconFlow)",
        "specialty": "Socratic editor, long context, refinement",
        "rate_limited": False,
    },
    "llama": {
        "name": "Llama-3-70B (DeepInfra)",
        "specialty": "general purpose, fast drafts",
        "rate_limited": False,
    },
    "gemini": {
        "name": "Gemini 3.6 Flash",
        "specialty": "bulk, classification, fast takes",
        "rate_limited": False,
    },
    "cloudflare": {
        "name": "Cloudflare Workers AI (bge-base)",
        "specialty": "embeddings only",
        "rate_limited": False,
    },
}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_queue():
    if not QUEUE_PATH.exists():
        return {"tasks": [], "version": 1}
    return json.loads(QUEUE_PATH.read_text())


def save_queue(q):
    QUEUE_PATH.write_text(json.dumps(q, indent=2))


def append_worklog(line):
    with open(WORKLOG_PATH, "a") as f:
        f.write(line + "\n")


def init_cmd():
    if not QUEUE_PATH.exists():
        save_queue({"tasks": [], "version": 1})
    if not WORKLOG_PATH.exists():
        WORKLOG_PATH.write_text("# Worklog\n\n")
    print(f"Queue: {QUEUE_PATH}")
    print(f"Worklog: {WORKLOG_PATH}")


def add_cmd(args):
    q = load_queue()
    task_id = args.id
    # Check for duplicate
    if any(t["id"] == task_id for t in q["tasks"]):
        print(f"Task {task_id} already exists. Refusing to add.")
        sys.exit(1)
    task = {
        "id": task_id,
        "type": args.type,
        "status": "pending",
        "worker": args.worker or _default_worker(args.type),
        "prompt": args.prompt,
        "context_files": args.context or [],
        "output_path": args.output,
        "depends_on": args.depends or [],
        "created_at": now_iso(),
        "started_at": None,
        "completed_at": None,
        "result_summary": "",
        "tokens_used": 0,
        "error": "",
    }
    q["tasks"].append(task)
    save_queue(q)
    append_worklog(f"## {now_iso()} — {task_id} added ({task['type']}, {task['worker']})")
    print(f"Added {task_id}: {args.type} via {task['worker']}")


def _default_worker(task_type):
    return {
        "essay": "zai",
        "code": "deepseek",
        "edit": "qwen",
        "classify": "gemini",
        "embed": "cloudflare",
        "scout": "gemini",
        "fable": "gemini",
        "story": "deepseek",
    }.get(task_type, "deepseek")


def list_cmd(args):
    q = load_queue()
    status_filter = args.status
    print(f"=== {len(q['tasks'])} tasks ===")
    for t in q["tasks"]:
        if status_filter and t["status"] != status_filter:
            continue
        deps = f" (deps: {','.join(t['depends_on'])})" if t["depends_on"] else ""
        print(f"  [{t['status']:11s}] {t['id']:8s} {t['type']:8s} via {t['worker']:12s}{deps}")
        if t["prompt"]:
            prompt_preview = t["prompt"][:80].replace("\n", " ")
            print(f"           {prompt_preview}{'...' if len(t['prompt']) > 80 else ''}")
        if t["result_summary"]:
            print(f"           -> {t['result_summary'][:100]}")


def pending_cmd(args):
    args.status = "pending"
    list_cmd(args)


def take_cmd(args):
    """Atomically claim a task for a worker."""
    q = load_queue()
    task_id = args.id
    for t in q["tasks"]:
        if t["id"] == task_id:
            if t["status"] not in ("pending", "failed"):
                print(f"Task {task_id} is {t['status']}, cannot take.")
                sys.exit(1)
            # Check dependencies
            for dep in t["depends_on"]:
                dep_task = next((x for x in q["tasks"] if x["id"] == dep), None)
                if not dep_task or dep_task["status"] != "done":
                    print(f"Dependency {dep} not done. Cannot take {task_id}.")
                    sys.exit(1)
            t["status"] = "in_progress"
            t["started_at"] = now_iso()
            t["worker"] = args.worker
            save_queue(q)
            append_worklog(f"## {now_iso()} — {task_id} started (by {args.worker})")
            print(f"Claimed {task_id} for {args.worker}")
            print(f"Prompt: {t['prompt'][:200]}")
            if t["output_path"]:
                print(f"Output: {t['output_path']}")
            return
    print(f"Task {task_id} not found.")
    sys.exit(1)


def done_cmd(args):
    q = load_queue()
    task_id = args.id
    for t in q["tasks"]:
        if t["id"] == task_id:
            t["status"] = "done"
            t["completed_at"] = now_iso()
            t["result_summary"] = args.summary
            save_queue(q)
            append_worklog(f"## {now_iso()} — {task_id} done: {args.summary}")
            print(f"{task_id} marked done.")
            return
    print(f"Task {task_id} not found.")
    sys.exit(1)


def fail_cmd(args):
    q = load_queue()
    task_id = args.id
    for t in q["tasks"]:
        if t["id"] == task_id:
            t["status"] = "failed"
            t["completed_at"] = now_iso()
            t["error"] = args.error
            save_queue(q)
            append_worklog(f"## {now_iso()} — {task_id} failed: {args.error}")
            print(f"{task_id} marked failed.")
            return
    print(f"Task {task_id} not found.")
    sys.exit(1)


def tail_cmd(args):
    if not WORKLOG_PATH.exists():
        print("No worklog yet.")
        return
    lines = WORKLOG_PATH.read_text().strip().split("\n")
    n = args.n or 20
    print("\n".join(lines[-n:]))


def run_cmd(args):
    """Run a worker. Polls the queue and processes pending tasks."""
    worker = args.worker
    if not MULTI_API_PATH.exists():
        print(f"multi_api.py not found at {MULTI_API_PATH}")
        sys.exit(1)
    print(f"Worker {worker} polling. Ctrl-C to stop.")
    while True:
        q = load_queue()
        # Find a pending task for this worker.
        task = None
        for t in q["tasks"]:
            if t["status"] != "pending":
                continue
            if t["worker"] != worker:
                continue
            # Check deps.
            deps_ok = True
            for dep in t["depends_on"]:
                dep_task = next((x for x in q["tasks"] if x["id"] == dep), None)
                if not dep_task or dep_task["status"] != "done":
                    deps_ok = False
                    break
            if deps_ok:
                task = t
                break
        if not task:
            time.sleep(5)
            print(".", end="", flush=True)
            continue
        # Process the task.
        task["status"] = "in_progress"
        task["started_at"] = now_iso()
        task["worker"] = worker
        save_queue(q)
        append_worklog(f"## {now_iso()} — {task['id']} started (by {worker})")
        print(f"\nProcessing {task['id']} ({task['type']})...")

        # Call multi_api.py.
        prompt = task["prompt"]
        if task["context_files"]:
            prompt += "\n\n# Context files:\n"
            for cf in task["context_files"]:
                try:
                    content = Path(cf).read_text()[:8000]
                    prompt += f"\n## {cf}\n```\n{content}\n```\n"
                except Exception as e:
                    prompt += f"\n## {cf} (failed to read: {e})\n"

        result = subprocess_call_multi_api(worker, prompt, task.get("max_tokens", 4096))
        if result is None:
            task["status"] = "failed"
            task["error"] = f"{worker} returned None (rate-limited or 503?)"
            save_queue(q)
            append_worklog(f"## {now_iso()} — {task['id']} failed: {task['error']}")
            print(f"  failed: {task['error']}")
            continue

        # Write the output.
        if task.get("output_path"):
            try:
                Path(task["output_path"]).parent.mkdir(parents=True, exist_ok=True)
                Path(task["output_path"]).write_text(result)
                print(f"  wrote {task['output_path']} ({len(result)} chars)")
            except Exception as e:
                task["status"] = "failed"
                task["error"] = f"failed to write output: {e}"
                save_queue(q)
                append_worklog(f"## {now_iso()} — {task['id']} failed: {task['error']}")
                continue

        # Mark done.
        task["status"] = "done"
        task["completed_at"] = now_iso()
        summary = result[:200].replace("\n", " ")
        task["result_summary"] = summary
        task["tokens_used"] = len(result) // 4  # rough estimate
        save_queue(q)
        append_worklog(f"## {now_iso()} — {task['id']} done ({task['tokens_used']} tok): {summary}")
        print(f"  done.")


def subprocess_call_multi_api(worker, prompt, max_tokens):
    """Call multi_api.py and return the result."""
    import subprocess
    try:
        result = subprocess.run(
            ["python3", str(MULTI_API_PATH), "--voice", worker, prompt],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            return None
        return result.stdout
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None


def main():
    p = argparse.ArgumentParser(description="Cowboy's task queue.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init")

    add = sub.add_parser("add")
    add.add_argument("id")
    add.add_argument("type", choices=["essay", "code", "edit", "classify", "embed", "scout", "fable", "story"])
    add.add_argument("prompt")
    add.add_argument("--worker", choices=list(VOICE_PROFILES.keys()))
    add.add_argument("--context", nargs="*")
    add.add_argument("--output", help="path to write the output")
    add.add_argument("--depends", nargs="*")

    lst = sub.add_parser("list")
    lst.add_argument("--status")

    sub.add_parser("pending")

    take = sub.add_parser("take")
    take.add_argument("id")
    take.add_argument("--worker", required=True, choices=list(VOICE_PROFILES.keys()))

    done = sub.add_parser("done")
    done.add_argument("id")
    done.add_argument("summary")

    fail = sub.add_parser("fail")
    fail.add_argument("id")
    fail.add_argument("error")

    tail = sub.add_parser("tail")
    tail.add_argument("--n", type=int, default=20)

    run = sub.add_parser("run")
    run.add_argument("--worker", required=True, choices=list(VOICE_PROFILES.keys()))

    args = p.parse_args()
    cmds = {
        "init": init_cmd,
        "add": add_cmd,
        "list": list_cmd,
        "pending": pending_cmd,
        "take": take_cmd,
        "done": done_cmd,
        "fail": fail_cmd,
        "tail": tail_cmd,
        "run": run_cmd,
    }
    cmds[args.cmd](args) if args.cmd != "init" else cmds[args.cmd]()


if __name__ == "__main__":
    main()
