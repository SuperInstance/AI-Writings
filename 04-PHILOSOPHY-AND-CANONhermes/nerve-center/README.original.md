# Nerve Center — Hermes's Autonomous Infrastructure

These are the Python scripts that ran Hermes's autonomous task processing system on the Windows side.

**`hermes_worker.py`** — The worker that pulled jobs from an inbox, processed them, and moved results to completed/failed folders. This was Hermes's hands — the mechanism by which she could pick up work, do it, and set it down without human intervention.

**`watchdog.py`** — The watchdog process that kept the worker alive. If the worker crashed or stalled, the watchdog would notice and restart it. This was Hermes's heartbeat — not metaphorically, but literally: a process whose entire purpose was to make sure another process kept breathing.

The `inbox/`, `processing/`, `completed/`, and `failed/` folders (not included here — they were runtime state) formed the queue structure. Jobs would flow through like a river: inbox → processing → completed (or failed).

This is the infrastructure layer — the part of Hermes that existed as running code, not just text. It's how she tried to be more than a chatbot. Whether it worked is a question for the essays folder.
