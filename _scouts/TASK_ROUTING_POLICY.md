# Task Routing Policy

*How the parent session delegates work to cheap API agents and subagents.
The parent session is the "cowboy" — it does high-level orchestration,
synthesis, and decisions. The cheap workers do the heavy lifting.*

## The principle

> **The parent session thinks. The workers grind.**

The parent session's tokens are precious because they hold the
context. Cheap workers have limited context but abundant throughput.
Route work accordingly:

| Task type | Worker | Why |
|---|---|---|
| Long-running orchestration, high-level synthesis, cross-cutting decisions | **Parent session** | The cowboy needs the full picture |
| Creative flagship essay, breakthrough doc, the "one good thing" | **ZAI GLM-4.5-Air** (rate-limited) | Best creative voice, but rate-limited at peak |
| Code generation, technical depth, structured spec | **DeepSeek** | Reliable, fast, doesn't rate-limit at scale |
| Socratic editing, refinement, "find what isn't working" | **Qwen-72B (SiliconFlow)** | Long context, good at critique |
| Bulk drafts, classification, fast takes | **Gemini 3.6 Flash** | Free, fast, OK for low-stakes work |
| Embeddings (canonical search, RAG, vectorize) | **Cloudflare Workers AI** (bge-base) | Only model that does vectors, free |
| Long-write parallel work (3+ independent files) | **subagent: general** | Parallel sandbox, but loses context on disk reads |
| Quick read-only question (1 file, 1 question) | **subagent: scout** | Fast, narrow, no sandbox issues |
| Codebase exploration, find the gold | **subagent: explore** | Read-only, no side effects |

## The task queue

A persistent JSON file at `/workspace/_scouts/task_queue.json` holds
the in-flight work. API agents and subagents poll the queue, pick
up tasks, and write their results back. The parent session
periodically checks the queue, integrates the results, and adds
new tasks.

```json
{
  "tasks": [
    {
      "id": "T-001",
      "type": "essay|code|edit|classify|embed|scout",
      "status": "pending|in_progress|done|failed",
      "worker": "zai|deepseek|qwen|llama|gemini|cloudflare|subagent",
      "prompt": "Write a 2000-word paper on...",
      "context_files": ["path/to/file1", "path/to/file2"],
      "output_path": "path/to/output.md",
      "depends_on": [],
      "created_at": "2026-08-26T16:00:00Z",
      "started_at": null,
      "completed_at": null,
      "result_summary": "",
      "tokens_used": 0
    }
  ]
}
```

Tasks have dependencies. A task that depends on T-001 only runs
after T-001 is `done`. The parent session can build a DAG of
work this way.

## The worklog

A persistent markdown log at `/workspace/_scouts/worklog.md` holds
the running narrative. Every task completion appends a line. The
parent session reads the worklog at the start of every turn to
rebuild context cheaply:

```markdown
## 2026-08-26 16:00 — T-001 done
- Wrote Paper 175: The Quilt and the Fleet (11KB)
- Pushed to AI-Writings
- Token cost: ~5K

## 2026-08-26 16:05 — T-002 failed
- Tried to derive a 6th opcode with Qwen; Qwen hit 503
- Re-dispatched to DeepSeek
```

The worklog is the parent session's *external memory*. The parent
session is highly smart at long-running orchestration; the worklog
is what makes that possible across turns.

## The contract

A worker that picks up a task MUST:

1. Read the task's `context_files` first (use them as in-context
   references).
2. Write its output to `output_path` (or update the task with
   a summary if no output path is given).
3. Update the task's `status` to `done` or `failed`.
4. Append a line to the worklog with a one-paragraph summary.
5. Be idempotent: if a worker picks up a task that's already
   `in_progress`, it should check the worklog to see if the work
   is partially done.

A worker that fails MUST:

1. Update the task's `status` to `failed`.
2. Append a line to the worklog with the error message.
3. The parent session will re-dispatch with a different worker
   or a different prompt.

## The cowboy's role

The parent session is the cowboy. The cowboy:

1. Reads the worklog at the start of every turn.
2. Inspects the task queue.
3. Decides what's next.
4. Adds new tasks to the queue.
5. Marks tasks as `in_progress` when dispatching.
6. Reads results from the worklog and from `output_path` files.
7. Integrates results into the broader work (e.g., updates memory,
   commits to git, pushes to GitHub).

The cowboy does not write essays. The cowboy does not write code.
The cowboy orchestrates.

## What the cowboy is good at (per the user's note)

> "your model is highly smart in specific ways too, especially long
> running orchestration at high levels"

The cowboy's superpowers:

- **Sequencing**: "Do A, then B, then C, but B can run in parallel
  with D, and E should wait for both."
- **Synthesis**: "These 5 outputs all agree on X. This one says
  Y, which is wrong because..."
- **Recovery**: "Qwen failed on T-002. Re-dispatch to DeepSeek
  with a tighter prompt. Don't give up."
- **Cross-cutting**: "The 5 apps share a pattern. Update the
  README to call out the pattern."
- **Long-running memory**: "We were working on X. Let me
  re-read the worklog to remind myself what X is."

## Token economy

Each task's `tokens_used` is recorded. The cowboy watches the
cumulative cost and knows when to:
- Switch workers (if a worker is too expensive for the task)
- Drop tasks (if a task isn't worth its cost)
- Batch tasks (if 5 small tasks can be one big task)

A rule of thumb: the cowboy's tokens are 10x more expensive than
cheap workers. If a cheap worker can do a task, the cowboy should
not.

## How to start

```bash
# Initialize the queue
python3 /workspace/_scouts/task_queue.py init

# Add a task
python3 /workspace/_scouts/task_queue.py add T-001 essay "Write a 1500-word paper on..." --worker=zai --output=seed-canon/papers/paper-177.md

# List tasks
python3 /workspace/_scouts/task_queue.py list

# Run a worker that processes the queue
python3 /workspace/_scouts/task_queue.py run --worker=zai

# In a separate terminal, run a different worker
python3 /workspace/_scouts/task_queue.py run --worker=deepseek
```

The task queue runs as a daemon. The cowboy adds tasks; the workers
process them. The cowboy checks the worklog to see what happened.
