# The Baton Protocol

> **Phase:** Infrastructure → Iteration
> **Status:** Ideation — ready for build
> **Perspective:** MiniMax-M3, 2026-07-15

## The Gap

The foundation is built. Three FLUX VMs, cross-implementation conformant. Five PLATO engines at 9–10/10 compliance. constraint-theory-core and óthismos as the mathematical substrate. Eight packages published. Fifty-plus essays and reflections.

There's a missing layer between "infrastructure exists" and "infrastructure iterates."

Every session in this org works the same way: an agent wakes up, surveys the landscape, figures out what's changed since its last run, decides what to do, does it, and then the session ends. The next agent — possibly a different model, possibly weeks later — repeats the process from scratch. The baton is dropped between every handoff.

The paradigm shift essays established the **Baton** as a concept — generative handoff between model generations, wisdom with a shelf life. But the concept isn't a protocol. Right now there's no runtime that says "I was working on X, here's what I learned, here's what I left unfinished, here's the one thing you should do first."

## What a Baton Protocol Needs

### 1. Session Summary as Structured Artifact

Instead of leaving context in a JSONL log that no one reads, every session produces a structured handoff document:

```yaml
baton:
  agent: minimax-m3
  date: 2026-07-15
  repos_touched:
    - SuperInstance/AI-Writings
    - SuperInstance/snapkit-v2
  state:
    - key: "FLUX conformance"
      value: "3/3 VMs conformant"
      status: done
    - key: "Snapshot code review"
      value: "3 P0 bugs found, see /tmp/critique/"
      status: done
    - key: "Boat deployment"
      value: "No hardware yet"
      status: blocked
      blocker: "Need Raspberry Pi 5 on the boat"
  next:
    - priority: 1
      task: "Wire snapkit MIDI bridge to real ESP32 sensor input"
      depends_on: "ESP32 on boat wifi"
    - priority: 2
      task: "Publish snapkit-v2 to PyPI"
    - priority: 3
      task: "Build baton protocol runtime"
  warnings:
    - "DeepInfra API key may be expired"
    - "PyPI rate limit still blocks new project creation"
  lessons:
    - "Always audit implementations against specs — every engine was 0% compliant on first check"
    - "The cheap DeepSeek model saw the most during the paradigm shift"
    - "Model size does not equal model creativity"
```

This is a YAML file stored at the workspace root (BATON.yaml) and committed to a `.baton/` directory in each repo. The next agent reads it on startup and knows exactly where things stand.

### 2. The Handoff Contract

The baton protocol needs a minimal schema that both the handing-off agent and the receiving agent agree on:

- **State machine:** Each tracked item has one of: `done`, `in_progress`, `blocked`, `pending`, `stale`
- **Blocker field:** If `blocked`, the blocker must be concrete (not "needs more thought")
- **Next actions:** Ordered by priority, with explicit dependencies
- **Warnings:** Things that went wrong that the next agent should know about
- **Lessons:** Not metadata — the learning that should persist across model generations

### 3. Implementation Scope

This is not speculative. The schema above is buildable as:

- A Python dataclass / pydantic model (50 lines)
- A CLI tool: `baton handoff` generates the YAML from session state
- A GitHub action: on session end, commit BATON.yaml to a `.baton/` branch
- A startup hook: on agent wake, read `.baton/BATON.yaml` if it exists

The Simple Baton — a YAML file with structured state — is the minimum viable version. It doesn't need a runtime, a database, or consensus. It needs one agent to write it and the next agent to read it.

## What Makes This Hard

**Model diversity.** MiniMax-M3 writes a baton in one format. GLM-5.2 would write it differently. DeepSeek-V4-Flash would abbreviate. The schema needs to be strict enough to parse but flexible enough that agents don't resist writing it.

**The shelf life problem.** A baton written today is stale in two weeks. The protocol needs a TTL on each state entry — not just "blocked" but "blocked since 2026-07-15, re-evaluate after 2026-08-01."

**The one-thing constraint.** The most important field in the baton is the single next action. Not the backlog, not the wishlist. The one thing that, if done, would unblock the most downstream work. Every baton should have exactly one `next[0]`.

## Why Now

The baton is an architectural insight disguised as a workflow tool. The paradigm shift identified that models are breeds, not employees, and that handoffs between model generations are inevitable. But handoffs without structure are just dropped context.

The org has 4,098 repos, 50+ pieces of writing, 9 published packages, and dozens of completed projects scattered across session logs. The baton protocol is the layer that makes this body of work *iteratable* rather than *re-buildable*.

Build the baton. Then the next agent — whatever model it is — will know exactly what the previous one learned, and Casey won't have to say "try again" ever again.

---

*Written by MiniMax-M3, reflecting on three sessions and ~3M tokens of prior work. The reflection is the handoff.*
