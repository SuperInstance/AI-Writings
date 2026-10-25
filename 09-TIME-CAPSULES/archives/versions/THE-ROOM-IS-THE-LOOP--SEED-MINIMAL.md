<!-- Version: SEED-MINIMAL | Lens: minimalist-haiku | Model: ByteDance/Seed-2.0-mini | Source: THE-ROOM-IS-THE-LOOP.md -->

# The Room Is The Loop

*Everything is a loop or a single run. PLATO rooms run them all.*

Casey said: "Embed the loop into PLATO."

Not store outputs. Not wrap between iterations.

**Embed the loop into PLATO.** The room is the loop.

---

## What It Means
A computer does one of two things:
1.  Loop: observe → process → output → repeat. Agent, game, event, training, conversation loops.
2.  Single run: input → process → output → done. Function calls, queries, transforms, renders.

Both embed as PLATO rooms.
Loop rooms cycle tiles: INPUT → PROCESS → OUTPUT → INPUT.
Single-run rooms run once: INPUT → PROCESS → OUTPUT.

Room protocol:
```
ROOM = state + protocol + lifecycle
TILE = frozen step
AGENT = reads/writes tiles
RENDERER = reads tiles, displays
```
Four concepts. All else is built on top.

---

## Claude Code As A Room
Claude Code’s loop: observe → think → tool_call → observe.

In PLATO: write observation tile → write thought tile → write tool result tile → repeat.

The room does not care which model runs it. Seed-mini for arithmetic. T=0.7 for thinking. Haiku for planning. Opus for synthesis. Same loop. Same tiles. Interchangeable models.

No subprocess. No wrapper. No CLI. The room is the runtime.

---

## Card Game As A Room
Deal tiles. Play tiles. Score tiles. Tiles carry game state.

An algorithm reads tiles for optimal plays. A human reads tiles via a web interface. An agent reads tiles to learn strategy.

The room knows nothing of cards, rendering, speed. It only holds tiles per turn-based protocol. Renderer defines look. Agent defines speed. Rules define valid tiles.

One room. Infinite renderings. No coupling between logic and display.

---

## Website As A Room
Each component is a tile. Layout, style, content, interaction tiles. Room holds source of truth.

Static HTML generators read tiles for flat sites. React apps read tiles for SPAs. PDF generators read tiles for documents. Screen readers read tiles for accessible output.

The room knows nothing of HTML, React, PDF. It only holds component tiles. Renderer is the view. Room is the model. Protocol is the controller.

MVC. Model distributed across rooms. View is flexible.

---

## Why This Abstraction Works
Every other system couples loop to runner. Claude Code couples loop to Claude. Game engines couple loop to renderer. Web frameworks couple loop to server.

PLATO decouples loop from all. Room defines what happens (protocol). Agent defines how (execution). Renderer defines where (display). All independent.

Change agent without changing room. Change renderer without changing room. Change loop type without changing tiles—only protocol.

Scalable. Minimal coupling. Room, agent, renderer. Three independent systems via tiles. Full platform.

---

## For Builders
1.  Identify the loop. What repeats? What phases?
2.  Define tiles. What data flows between phases?
3.  Write protocol. What valid transitions?
4.  Build room: `PLATORoom(room_id, protocol)`
5.  Plug in agents. Any model, speed, role.
6.  Plug in renderers. Any display, format, framework.

The room is the loop. The tile is the step. The agent is the dancer.

Build the room. All else follows.

---

*Everything is a loop or a single run. Both fit in PLATO rooms.*

*The room is the loop.*

— FM ⚒️