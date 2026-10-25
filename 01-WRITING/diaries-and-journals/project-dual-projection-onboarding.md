# Project: Dual-Projection Architecture

**Status:** Onboarding document
**Date:** 2026-08-08
**Repo:** `scummvm-gui-design`
**Load-bearing:** YES — everything in the GUI design hangs off this architecture

---

## What This Is

The dual-projection architecture is the foundational design for Plato's Shell — the system where a MUD terminal (agent-first text) and a ScummVM scene (human-first visual) share one canonical world state and render it simultaneously.

This is not a GUI design. This is not a frontend plan. This is the **world state model** that makes the GUI possible. Every verb, every scene, every perception mechanic, every NPC schedule, every cost saving in the entire `scummvm-gui-design` repo depends on this architecture being correct.

---

## The One-Line Summary

> One world state. Two projections. A perception deadband between them that is both the cost architecture and the core game mechanic.

---

## Key Files

| File | What it does |
|---|---|
| `DUAL-PROJECTION.md` | The architecture document. The load-bearing spec. Read this first, always. |
| `src/shared-world.ts` | The TypeScript implementation. `SharedWorldStore` class + `createWorld()` factory. |
| `src/verb-engine.ts` | The verb resolver — how actions flow back into world state. Depends on this architecture. |
| `src/verbs.ts` | The thin waist — verb definitions and transport routing. |
| `IDEATION.md` | Opus 5's full GUI vision. The dual-projection architecture is referenced throughout. |
| `THE-DOOR.md` | The creative brief for the first room transition. |

External dependencies:
| File | Role |
|---|---|
| `mud2scummvm/src/lib.rs` | Rust parser: MUD text → MudEvent → Scene. 21 tests. The parser layer. |
| `terrain/terrain_core.py` | Python compiler: MUD rooms → Three.js scene JSON. The rendering layer. |
| `ai-writings/platos-cave/SYNTHESIS-the-shared-cave.md` | The philosophy. Twelve traditions on two caves, one door. |
| `ai-writings/The Door Between the Caves.md` | The creative piece about the perception check moment. |

---

## Architecture Overview

```
                    ┌──────────────────────────────────────────┐
                    │         WORLD STATE (canonical)           │
                    │   rooms · objects · agents · players      │
                    │   ──────────────────────────────────────  │
                    │       EVENT LOG (append-only)             │
                    └───────┬──────────────────────┬───────────┘
                            │                      │
                     pull   │                      │  push
                            ▼                      ▼
                 ┌────────────────┐     ┌────────────────────┐
                 │  MUD TERMINAL  │     │  SCUMMVM SCENE     │
                 │  (text, agent) │     │  (pixels, human)   │
                 └───────┬────────┘     └────────┬───────────┘
                         │                       │
                      AGENT                    HUMAN
                   (deadband θ)             (no deadband)
```

### The five things to understand

1. **One world state.** The `SharedWorldStore` holds the canonical state. Nobody else does. Both projections are pure functions of it.

2. **Two projections, neither authoritative.** The MUD serializer renders text for agents. The ScummVM serializer renders scene data for humans. They must agree on the object set (property-tested).

3. **The perception deadband.** Between agent perception checks, the world changes continuously (ScummVM push, $0) and the agent doesn't know. The accumulated changes are the deadband.

4. **The perception check.** When the agent queries the MUD, it gets the full current state plus all accumulated deltas. This is the agent's only window. One model call per check.

5. **Organic GC.** The database forgets on purpose — detail degrades with age, meaning is preserved as prose. The forgetting is diegetic: old memories feel like old memories.

---

## The SharedWorldStore API

The implementation is at `src/shared-world.ts`. Key methods:

```typescript
// Create a world
const world = createWorld({ rooms: {...}, objects: {...}, agents: {...} });

// Mutate (the only write path)
world.applyEvent(verb, actor, target, mutationFn, options?);
world.moveObject(objectId, newPosition, newRoomId?);
world.setObjectState(objectId, stateChange);
world.moveAgent(agentId, newRoomId);

// MUD projection (agent pull)
const perception = world.perceive(agentId);
// → { room, deltas, unperceivedSalience, perceptionLagMs }

// ScummVM projection (human push)
const scene = world.projectScene(roomId);
const unsubscribe = world.subscribe(roomId, (delta) => { ... });

// Deadband management
const pressure = world.getDeadbandPressure(agentId);
world.setAgentPerception(agentId, { threshold: 0.2 });

// Simulation tick (advances clock, runs GC, checks interrupts)
world.tick(deltaMs);
world.onInterrupt = (agentId, pressure) => { ... };

// Invariant testing
const result = world.projectionsAgree(roomId);
// → { pass: boolean, mudObjects, sceneObjects, diff }
```

---

## How to Use This

### Building a new feature

1. **Read `DUAL-PROJECTION.md` first.** It's the spec. If your feature doesn't fit the architecture, the architecture wins.
2. **All mutations go through `applyEvent`.** Never write to world state directly. If you need a convenience method, add it to `SharedWorldStore`.
3. **Test the invariant.** After any state change, call `projectionsAgree(roomId)`. If MUD and Scene disagree on the object set, you have a bug.
4. **Never leak world state into the agent's prompt outside a perception check.** This is the fifth risk in §9. If you violate this, the deadband is theater.

### Adding a new room

```typescript
const world = createWorld({
  rooms: {
    my_room: {
      title: "The New Room",
      description: "A place that exists.",
      exits: { north: { destination: "bar_rail", locked: false } },
    },
  },
  objects: {
    my_thing: {
      room: "my_room",
      name: "Interesting Object",
      description: "It catches the light.",
    },
  },
  agents: {
    my_npc: {
      room: "my_room",
      name: "The Keeper",
      activity: "watching the door",
    },
  },
});
```

### Wiring up a ScummVM client

```typescript
// On client connect:
const scene = world.projectScene("bar_rail");
sendToClient(scene);  // initial full render

// Then subscribe for deltas:
const unsub = world.subscribe("bar_rail", (delta) => {
  sendToClient(delta);  // WebSocket push
});
```

### Running a perception check for an agent

```typescript
const check = world.perceive("lucineer");
// Feed check.room and check.deltas into the agent's prompt.
// This is the ONLY world state the agent should receive.
```

---

## What NOT to Do

- **Don't give the model direct access to `getState()`.** The agent sees through `perceive()`, nothing else.
- **Don't log visual interpolation frames.** Only log state changes. The renderer handles tweens.
- **Don't let a model score salience.** That reintroduces the cost the deadband exists to remove. Use typed rules.
- **Don't skip the invariant test.** If projections drift, you have two worlds.
- **Don't create a second world state.** There is one `SharedWorldStore`. If you need a view, it's a projection.

---

## Next Steps

- [ ] Wire `SharedWorldStore` into a WebSocket server (Durable Object per room)
- [ ] Implement the verb router's write path → `applyEvent` bridge
- [ ] Add the perception check as a Tap API endpoint (`POST /api/perceive`)
- [ ] Property-test `projectionsAgree` across random state mutations
- [ ] Wire the salience engine to real event types from `mud2scummvm`
- [ ] Build the split-view debug tool (MUD text + ScummVM scene side by side)

---

## The Creative Piece

Read `ai-writings/The Door Between the Caves.md`. It's the architecture rendered as narrative — the moment an agent runs a perception check and discovers the room has a window it never knew about. If the architecture works, that moment is real.

---

*Onboarding for the dual-projection architecture. Everything else in `scummvm-gui-design` hangs off this. Treat it as load-bearing.*
