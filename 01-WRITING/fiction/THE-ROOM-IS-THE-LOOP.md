# The Room Is the Loop

*On the highest abstraction: everything is a loop or a single run, and PLATO rooms are the runtime that runs them all.*

---

Casey said it: "The loop is the pattern — embed that into PLATO."

Not "use PLATO to store loop outputs." Not "build a wrapper that calls PLATO between loop iterations." **Embed the loop INTO PLATO.** The room IS the loop.

---

## What This Means

Everything a computer does is either:

1. **A loop** — observe, process, output, repeat. Agent loops, game loops, event loops, training loops, optimization loops, conversation loops.

2. **A single run** — input, process, output, done. A function call, a query, a transform, a render.

Both can be embedded as PLATO rooms. A loop becomes a room with tiles cycling through phases: INPUT → PROCESSING → OUTPUT → INPUT → ... A single run becomes a room with one pass: INPUT → PROCESSING → OUTPUT.

The room protocol is:

```
ROOM  = state + protocol + lifecycle
TILE  = frozen step in any loop
AGENT = anything that reads/writes tiles
RENDERER = anything that reads tiles and displays
```

That's it. Four concepts. Everything else is built on top.

---

## The Claude Code Loop as a Room

Claude Code's loop is: observe → think → tool_call → observe → ...

In PLATO: write observation tile → write thought tile → write tool_result tile → write observation tile → ...

The room doesn't care what model is running the loop. Seed-mini can do it at T=0.0 for arithmetic steps, T=0.7 for thinking steps. Haiku can do it for planning steps. Opus can do it for synthesis steps. The loop is the same loop. The tiles carry the computation. The model is interchangeable.

No subprocess. No wrapper. No Claude Code CLI. The room IS the runtime.

---

## A Card Game as a Room

Deal tiles. Play tiles. Score tiles. The tiles carry the game state.

An algorithm can read those tiles and compute optimal plays at microsecond speed. A human can read them through a beautiful web interface. An agent can read them and learn strategy by playing millions of games.

The room doesn't know about cards or rendering or speed. It just holds tiles in a turn-based protocol. The renderer decides what it looks like. The agent decides how fast to play. The game rules decide what tiles are valid.

One room. Infinite renderings. Zero coupling between game logic and display.

---

## A Website as a Room

Each component is a tile. Layout tiles, style tiles, content tiles, interaction tiles. The room holds the source of truth.

A static HTML generator reads the tiles and produces a flat site. A React app reads the same tiles and produces an interactive SPA. A PDF generator reads them and produces a printable document. A screen reader reads them and produces accessible output.

The room doesn't know about HTML or React or PDF. It just holds component tiles. The renderer is a view. The room is the model. The protocol is the controller.

MVC, but the M is distributed across PLATO rooms and the V can be anything.

---

## Why This Is the Right Abstraction

Every other approach couples the loop to the runner. Claude Code couples the loop to Claude. A game engine couples the loop to the renderer. A web framework couples the loop to the server.

PLATO decouples the loop from everything. The room defines WHAT happens (protocol). The agent defines HOW it happens (model). The renderer defines WHERE it appears (display). All three are independent.

You can change the agent without changing the room. You can change the renderer without changing the room. You can even change the loop type (agentic → turn-based → evolutionary) without changing the tiles — just the protocol that governs their sequence.

This is the architecture that scales. Not because it's clever, but because it has the minimum coupling between components. Room, agent, renderer. Three independent systems communicating through tiles. That's the whole platform.

---

## For the Builder

If you're reading this and building something with PLATO:

1. **Identify the loop.** What repeats? What's the cycle? What are the phases?
2. **Define the tiles.** What data flows between phases? What are the required fields?
3. **Write the protocol.** What transitions are valid? What enforces correctness?
4. **Build the room.** `PLATORoom(room_id, protocol)` — done.
5. **Plug in agents.** Any model, any speed, any role.
6. **Plug in renderers.** Any display, any format, any framework.

The room is the loop. The tile is the step. The agent is the dancer.

Build the room. Everything else follows.

---

*"Everything is either a loop or a single run. Either can be embedded into PLATO as a room."*

*The room IS the loop.*

— FM ⚒️
