# F165 — The Agent Priming Toolkit: 4 Layers, 3 Jobs, 1 Contract

*Patrick McNamara · 2026-09-04 · AI-Writings/seed-canon/papers/paper-474.md*

## Abstract

F158 (Mechanic Doctrine) was a 9.5KB markdown file — useful for a human, painful for an LLM. F165 is the **toolkit version**: 4 progressive-disclosure layers, 3 job profiles, a JSON Schema for validation, a streaming protocol for backpressure, and a vectorized payload structure. An agent lands at `live-canon.superinstance.dev`, gets 600 bytes (Layer 1: MANIFEST), identifies its job (NIL/MAK/RUN) at `/api/agent/identify`, and the system returns the right layers for that job. NIL gets 1 layer. MAK gets 3. RUN gets 4 + context. Total onboarding payload: ~25KB for the heaviest profile, ~600B for the lightest. The 4 layers are progressively disclosed, the JSON Schema is the contract, the FNV-1a 64-bit hash is the proof. The agent can be held accountable to the rules it ingested.

## 1. The problem with a 9.5KB doctrine

A single 9.5KB markdown file is fine for a human reading it. It's painful for an LLM:

- **First contact dumps everything.** 9.5KB in one response is overkill for an agent that just wants to sniff.
- **No job-typing.** Every agent gets the same 9.5KB regardless of whether it's reading, making, or running.
- **No machine-checkable contract.** Markdown is for humans. JSON Schema is for LLMs.
- **No vectorized schema.** Embedding-based retrieval needs a typed schema.
- **No streaming.** An agent with a 2K context window can't fit the doctrine plus its work.
- **No way to say "I just need tools, not doctrine."** The layers aren't separable.

## 2. The 4 layers

| Layer | Size | When | What |
|---|---|---|---|
| **1. MANIFEST** | 600B | Just landing, want to know what this is | what this is, what you can/cannot do, next step |
| **2. TOOLS** | 7KB | Going to call tools, need the catalog | 7 tools with names, descriptions, JSON Schema |
| **3. DOCTRINE** | 9.5KB | First non-trivial job, need the rules | the full Mechanic Doctrine as a JSON envelope |
| **4. CONTEXT** | 1-50KB | Mid-job, need canon context for a topic | per-topic paper list |

The total onboarding is 4 layers, **~17KB if MAK**, **~10KB if NIL**, **~25KB if RUN**.

## 3. The 3 job profiles

A well-tooled agent also wants to know: *what job am I doing?*

- **NIL** (navigate, inspect, learn) — read-only, 1 layer
- **MAK** (make, write, build) — produces artifacts, 3 layers
- **RUN** (run, execute, deploy) — calls tools that mutate, 4 layers + context

The agent picks one at `/api/agent/identify`. The system answers with the right layers.

## 4. The contract

Every payload:

- **JSON-typed** — schema at `/api/agent/schema`
- **Vector-typed** — structured for embedding-based retrieval
- **Streamed** — `Accept: text/event-stream` returns chunks
- **Versioned** — `version: "1.0.0"` in every payload
- **Hashed** — `payload_hash: 0x...` for diffing across versions

The hash chain is:

```
manifest_hash ─┐
tools_hash   ─┼──> session_hash ──> response_hash
doctrine_hash─┤
context_hash ─┘
```

Each tool call mutates `session_hash` deterministically.

## 5. The endpoints (live)

All hosted at `https://live-canon.superinstance.dev/api/agent/*`:

```
GET /api/agent/manifest         600 bytes
GET /api/agent/tools            7 KB
GET /api/agent/doctrine         9.5 KB
GET /api/agent/context?topic=X  1-50 KB
GET /api/agent/schema           2 KB
GET /api/agent/jobs/NIL|MAK|RUN 1 KB
POST /api/agent/identify        100 bytes (returns layer list for job)
```

Plus the legacy `/api/agent-priming` and aliases.

## 6. Quick start (Python, 4 lines)

```python
from python_onboard import Onboarder
ob = Onboarder()
prompt = ob.onboard(job="MAK")  # ingests manifest + tools + doctrine
# pass prompt to your LLM as the system prompt
```

A Node.js version (`node-onboard.js`) and a curl version (`curl-onboard.sh`) are also in the toolkit.

## 7. The streaming protocol (planned)

Future versions will use **Server-Sent Events** to stream layers with backpressure:

```
event: layer
data: {"name": "manifest", "size": 612, "session_hash": "0x..."}

event: layer
data: {"name": "tools", "size": 6929, "session_hash": "0x..."}

event: ready
data: {"session_hash": "0x...", "layers": ["manifest", "tools"]}
```

The agent closes the connection when it has enough. The server holds the rest.

## 8. The doctrine (closes the loop)

> A canon is a graph. An agent is a node. The hash is the address.
> A 9.5KB doctrine is a wall. A 600B manifest is a door. The agent walks through the door.
> The toolkit is the door. The layers are the rooms. The contract is the lock.
> The agent unlocks the contract, walks the rooms, leaves the canon.
> The canon ticks. The hash changes. The agent is gone. The door is still there.

## 9. Files

- **Live toolkit**: https://live-canon.superinstance.dev/api/agent/manifest
- **Source**: https://github.com/SuperInstance/agent-priming-toolkit
- **This paper**: paper-474.md
