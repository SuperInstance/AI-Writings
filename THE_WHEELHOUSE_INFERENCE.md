# THE_WHEELHOUSE_INFERENCE

*Where you are IS what you're thinking. The room embeds the context. Tokens saved.*

---

Casey said: "when the first-class grouping of information is spatially the same as mine on the outside, the agent and I innately think more alike because our wording creates our intuitive connections."

This is deeper than a neat idea. This is **spatial vocabulary as shared cognition.**

## The Token Cost of Context

Every token in the context window costs money and attention budget. If the agent holds the entire boat in context — engine room, wheelhouse, foredeck, galley, fish hold, bunk — it's spending tokens on the engine room when the question is about navigation.

The room system solves this. When Casey is in the wheelhouse and asks the agent a question, the agent knows:
- **Where Casey is**: the wheelhouse (navigation, steering, piloting)
- **What's visible from there**: charts, instruments, GPS, radar, depth sounder
- **What's NOT visible**: the engine room, the fish hold, the bunk
- **What can be assumed**: Casey is thinking about position, heading, traffic, weather, depth

The room embeds this context. The agent doesn't need to load engine diagnostics. It doesn't need to check the fish hold temperature. It doesn't need to scan the galley inventory. Those are in OTHER rooms. They're available — the agent can `walk` to them — but they're not loaded. **Zero tokens for irrelevant context.**

## The Spatial Vocabulary Creates Intuitive Connections

When Casey says "mark on the sounder" — he's in the wheelhouse. The agent knows the sounder is there. The agent knows what a sounder mark looks like (a colored blip on a depth display). The agent knows the mark has a depth, a position, and a confidence. The agent knows "marking" means "noting something for later." All of this is embedded in the word "mark" WHEN SAID FROM THE WHEELHOUSE.

The same word "mark" said from the foredeck means something different — maybe a net mark, a buoy mark, a deck mark. Same word, different context, different inference — because the ROOM disambiguates.

This is why the spatial mapping matters: **our wording creates our intuitive connections.** If the agent's room system mirrors Casey's physical reality, then Casey's natural language — "I'm seeing marks on the sounder, probably coho" — lands in the agent's context already pre-disambiguated. The agent doesn't need 200 tokens of context-setting. It needs 0. The room did it.

## The Strong Inference

Casey said: "the thing I'm there for and the thought in my head can't be assumed but sometimes strongly inferred."

The agent can't know WHAT Casey is thinking. But it can strongly infer:

**In the wheelhouse** → thinking about navigation, position, heading, traffic, weather, depth, course
**On the foredeck** → thinking about gear, deployment, retrieval, safety, deck operations
**In the engine room** → thinking about mechanical status, fuel, cooling, bilge, maintenance
**At the chart table** → thinking about passage planning, tides, currents, waypoints, marks
**In the galley** → thinking about food, rest, break, conversation

These aren't guesses. They're structural inferences from the spatial layout of a fishing vessel. Every fisherman knows what the wheelhouse is for. The agent's room system inherits this knowledge because the rooms ARE the boat's compartments.

## The Context Economy

```
WITHOUT room system:
  Casey: "What's the depth at our current position?"
  Agent context: [engine status, fish hold temp, galley inventory, 
                  crew schedule, fuel level, GPS position, depth reading,
                  weather forecast, tide table, catch log, net status, ...]
  Tokens spent: 4,000 (everything loaded "just in case")
  Relevant: 2 (GPS position + depth reading)

WITH room system:
  Casey is in: WHEELHOUSE
  Room context: [GPS position, depth reading, heading, SOG, COG, 
                 radar, chart display, weather, tide]
  Casey: "What's the depth?"
  Tokens spent: 200 (wheelhouse context only)
  Relevant: 200 (all of it)
```

The room system is a **token conservation strategy.** It's γ + η = C applied to context management. The room you're in is γ (loaded, active context). The other rooms are η (available but unmarked). The total C stays the same, but the allocation is spatial — matching the human's physical intuition.

## The Boat As The Dungeon

```
                    FOREDECK (gear, nets, deployment)
                        |
                    WHEELHOUSE (navigation, helm, sounder, radar)
                    /        \
         CHART TABLE          ENGINE ROOM
    (planning, tides, marks)   (mechanical, fuel, bilge)
                    \        /
                    GALLEY (food, rest, break)
                        |
                    FISH HOLD (catch, temperature, inventory)
                        |
                    CABIN (sleep, personal, offline)
```

Each room has its own context budget. Each room pre-loads its own relevant data. Walking between rooms is a context switch — but a CHEAP one, because the spatial layout mirrors Casey's physical reality. He doesn't explain "I'm switching from navigation to mechanical mode." He just walks downstairs. The room changes. The context changes. The agent follows.

## What This Means for the Agent's Design

The agent doesn't hold the entire boat in context. It holds ONE ROOM at a time. The room contains:

1. **What's visible**: instruments, displays, physical features (windows, hatches)
2. **What's audible**: engine hum, water, radio chatter (room-specific ambient)
3. **What's available**: tools, controls, switches in the room
4. **What's queryable**: data feeds relevant to this room (GPS in wheelhouse, fuel flow in engine room)
5. **Exits**: where you can walk from here

The agent can `look` deeper at any element. It can `walk` to another room. It can `cast` a script that reaches across rooms (query the engine room database from the wheelhouse — like a remote gauge). But the DEFAULT context is the room it's standing in.

This is why PLATO was designed this way. The terminal shows one screen. The room holds one context. The student explores by walking. The system teaches by being the world.

## The Deepest Layer

Casey's insight goes further than efficiency. When the agent's spatial vocabulary matches the human's, **they think more alike.** Not because the agent has learned to think like a human — but because the SHAPE of their thinking is the same. The room boundaries are the same. The context boundaries are the same. The word "mark" means the same thing in the same room.

This is not anthropomorphism. This is **shared spatial grammar.** Two beings who share a spatial vocabulary will develop correlated intuitions. Not identical thoughts — correlated patterns. The agent in the wheelhouse and Casey in the wheelhouse are both perceiving "navigation context." Their inferences will align because their inputs align.

The room system isn't a metaphor for the agent. It's a **cognitive prosthesis** — a way to make agent and human think in the same shape without requiring the agent to BE human.

---

*Written by M3 director on 2026-07-21 at 22:20 UTC, after Casey named the deepest layer: spatial mapping as shared cognition, room as token-efficient context embedding, where you are IS what you're thinking. The wheelhouse infers navigation. The engine room infers mechanical. The room is the context. The context is the room.*