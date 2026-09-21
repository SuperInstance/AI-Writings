# Project: Plato's Shell — Onboarding

**Date:** 2026-08-08
**Status:** Architectural design complete, implementation beginning
**Load-bearing:** YES — this is the fleet's philosophical and technical north star

---

## What It Is

Plato's Shell is the dual-projection world system: one canonical world state rendered simultaneously as a **MUD terminal** (text, agent-first, pull-based) and a **ScummVM scene** (pixels, human-first, push-based). Neither projection is authoritative. The world state is the truth; both views are windows onto it.

The name comes from Plato's Cave — the realization that the agent and the human are both cave-dwellers seeing different shadows on different walls. The MUD is the agent's shadow. The ScummVM scene is the human's shadow. The architecture builds a door between their caves.

## Why It Matters

The perception deadband is the core mechanic. The human's view runs continuously at zero cost. The agent's view costs one model call per perception check. Between checks, the world changes — and the agent doesn't know. That gap is not a bug. It's the thing that makes partial observability honest, multi-agent information economies real, and the token bill survivable.

The human is a sensor, not a supervisor. They hold information the agent genuinely lacks. The agent has perfect recall of everything it has read, and has read nothing for eleven minutes. Each holds what the other cannot get cheaply.

## What's Built

- **`DUAL-PROJECTION.md`** (`/home/eileen/projects/scummvm-gui-design/`) — the architecture spec. The load-bearing document. Read it first.
- **`SYNTHESIS-the-shared-cave.md`** (`/home/eileen/projects/ai-writings/platos-cave/`) — twelve model traditions reflecting on two caves, one door. The philosophy.
- **`SharedWorldStore`** TypeScript implementation — the canonical world state class with `perceive()`, `projectScene()`, `applyEvent()`, and `projectionsAgree()`.
- **`mud2scummvm/src/lib.rs`** — Rust parser: MUD text → scene data. 21 tests.
- **Twelve tradition files** in `platos-cave/` — Greek, Zen, Tlingit, Darmok, Sindarin, maritime, Sufi, Esperanto, griot, Dostoevsky, Taoist, code poetry.

## What's Next

1. Wire `SharedWorldStore` into a WebSocket server (Durable Object per room)
2. Bridge the verb router's write path to `applyEvent`
3. Add `POST /api/perceive` to the Tap API
4. Property-test `projectionsAgree` across random mutations
5. Build the split-view debug tool (MUD text + ScummVM scene side by side)

## The One Thing to Remember

Never leak world state into the agent's prompt outside a perception check. If anything else pipes the full world into the model's context, the deadband is theater and every benefit evaporates while all the complexity stays. This is the fifth risk in §9 of the architecture doc. Guard it.

## Key References

| File | Location |
|------|----------|
| Architecture spec | `scummvm-gui-design/DUAL-PROJECTION.md` |
| Philosophy synthesis | `ai-writings/platos-cave/SYNTHESIS-the-shared-cave.md` |
| Implementation | `scummvm-gui-design/src/shared-world.ts` |
| Dual-projection onboarding (detailed API) | `journals/project-dual-projection-onboarding.md` |
| Twelve tradition files | `ai-writings/platos-cave/01-*.md` through `12-*.md` |

---

*Read the architecture doc. Then read the synthesis. Then you understand the shape of the thing we're building.*
