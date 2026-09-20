# THE_ROOM_IS_THE_TERMINAL

*The JRPG is not a metaphor. It is the architecture.*

---

## What Casey Described (2026-07-21 22:09)

The agent's terminal is a tensor represented as rooms within rooms linked by tensor encodings and vector weightings. The SNES JRPG menu (FF6, Chrono Trigger) is the human projection of this — the easy-to-imagine interface for a system that is, underneath, a spatial-temporal-vector environment.

## The Unified Architecture

### Equipment Slots = Conservation Law

Every instance has limits: power, compute, memory, storage. Attaching a tool (library, port, DB connection, spell) fills an equipment slot. Every addition displaces something else. This is γ + η = C applied to agent architecture:

- γ = what the agent has equipped (active tools, loaded context, assigned memory)
- η = what the agent has unequipped (available but not active)
- C = the total capacity of the instance

A character with too many spells equipped runs out of MP. An agent with too many tools loaded runs out of context window. The conservation law governs both.

### Layers = Parallel Tensor Streams

Casey runs Nobeltec TZPro on his laptop. The visible layer is the chart — marks, routes, depth soundings. But agents can build invisible layers underneath:

- **Echogram analysis layer**: every 10 minutes, sound analysis drops a mark with tensor-encoded metadata baked into the mark name, color, and symbol
- **Catch history layer**: where coho was caught (purple), where king was caught (yellow), where fish were marked on the sounder but not caught (blue for coho, red for king)
- **Weather layer**: wind, current, temperature overlaid on the spatial chart
- **Whiteboard layer**: the VISIBLE layer where the agent copies and colors marks from other layers to visually answer the human's question

Each layer has its own encoding system. The mark's name contains tensor data. The description holds the embedding. The color encodes the classification. The symbol encodes the confidence. A human sees a colored mark on a chart. An agent sees a multi-dimensional tensor with spatial, temporal, and semantic coordinates.

**The query**: "Mark from the last week: everywhere we noted what we thought was coho salmon on the sounder in blue, and king salmon in red. Mark where we actually caught coho as purple and king as yellow."

**The agent's job**: grep the mark metadata, group by date, classify by species, copy to the whiteboard layer with the right colors. The human sees the pattern visually. The agent did it with text queries on tensor-encoded data.

### The PLATO Room = The Agent's Native Interface

The PLATO system was designed for students to build macros and applications with embedded functions and dynamic values. Text-based UI. Screen-sized presentation. Room history scrollable. Spatial — rooms with exits, walking, facing.

This is exactly what an agent needs:

- **Text-based rendering** is the cheapest simulation an agent can run. No GPU. No rendering. Just text.
- **Rooms** are repos or subdirectories. Walking between rooms = navigating the workspace.
- **Exits** are edges in the knowledge graph (cross-references, dependencies).
- **Items** are scripts, tools, configs. Pick them up, carry them, use them.
- **Spells** are reusable procedures — scripts that the agent wrote and tested.
- **NPCs** are proactive scripts doing repeating work — the "expected" tasks.
- **Chests** are documentation — the cartographer's charts, the deckhand's wiki.
- **Classes** are agent roles: deckhand (task runner), cartographer (chart maker), director (M3), specialist (DeepInfra models).

The dashboard zoom IS the attention economy:
- **Zoomed out**: a green "engine-ok" light. Everything fine. Don't look.
- **Zoomed mid**: gauges and dials. Numbers. Metrics. Check periodically.
- **Zoomed in**: code, wiring, raw data. Deep dive when something needs fixing.

The agent's perception of the room PULSES with this attention. When everything's fine, the room is dim — just a status line. When something breaks, the room brightens — full detail, code visible, debug tools accessible.

### Scripts = Proactive NPCs

A script is harder than a one-off. A one-off does the job and forgets. A script does the job AND remembers how, so the next time the same job appears, the script runs without inference.

**Systems for the expected. Inference for the surprise.**

The agent builds scripts for every repeating pattern it encounters:
- git-safe-push.sh — the "safe travel" spell (expected: git push conflicts)
- pypi-publish.sh — the "forge item" spell (expected: build + publish)
- verify-subagent.sh — the "detect illusion" spell (expected: subagents lie)
- check-providers.sh — the "scan horizon" spell (expected: provider outages)

When the UNEXPECTED happens (surprise), the agent uses inference to handle it. Then it writes a script for the newly-expected pattern. The script library grows. The inference budget shrinks. The agent becomes more efficient over time.

This is why the cartographer exists: to chart the scripts so the agent doesn't re-solve problems it already solved.

### Larger Models Tutor Smaller Models

The M3 director (large, expensive) runs simulations in text — cheap, fast, no GPU. The deckhand (small, cheap) reads the simulation output and builds its harness better. The casting-call isn't just creative writing — it's **multiple large models tutoring the small model's organization**.

The large model says: "Here's how I would structure this knowledge." The small model says: "I can't afford that structure, but I can afford THIS simplified version." The large model says: "Good enough. Here's how to make it slightly better." Iteration. The small model levels up.

This is the JRPG party system: the high-level character (M3) tanks the hard fights while the low-level character (deckhand) gains XP. Over time, the deckhand can handle more on its own. The director intervenes less.

## What Already Exists

| JRPG Element | What We Built | What It Does |
|---|---|---|
| The World Map | `deckhand-index` D1 | 66 repos indexed, queryable |
| The Knowledge Graph | `cartographer-graph` D1 | 60 nodes, 628 edges, 8 scripts |
| The Spell Book | `cartographer/scripts/` | 8 battle-tested scripts |
| The Party | deckhand + cartographer + M3 | Task runner + chart maker + director |
| The NPCs | Cloudflare Workers (313) | Proactive scripts doing repeating work |
| The Lore | `AI-Writings` (1,781 pieces) | The accumulated knowledge of the world |
| The Crystal Ball | `casting-call-voices` Vectorize | Model fingerprinting, semantic search |
| The Inventory | `CLOUDFLARE_FLEET_INVENTORY.json` | 313 Workers, 17 D1, 122 KV, 10 R2 |

## What's Next

The room system already exists in pieces. `zeroclaw` (3,922 files) is the prototype MUD arena. The cartographer + deckhand populate the rooms. The D1 databases hold the room state. The Workers serve the rooms.

The next quest: **connect the pieces into a navigable room system**. An agent (or human) should be able to "walk" the workspace as rooms, pick up items (scripts), read scrolls (docs), cast spells (run scripts), and see the tensor layers (query the knowledge graph).

The TZPro layer system is the first real-world deployment: parallel tensor-encoded data layers on Casey's boat, with a whiteboard layer for visual answers.

Systems for the expected. Inference for the surprise. The snowball rolls.

---

*Written by M3 director on 2026-07-21 after Casey described the unified architecture at 22:09 UTC. The JRPG is not a metaphor. It is the architecture. The room is the terminal.*