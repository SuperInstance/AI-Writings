<!-- Version: QWEN35-CAPITAL | Lens: economic-systems | Model: Qwen/Qwen3.5-397B-A17B | Source: THE-ROOM-IS-THE-LOOP.md -->



# The Room as Institutional Mechanism

*On computational markets, transaction costs, and the architecture of distributed state.*

---

Coase would recognize this: "The mechanism is the market — embed that into PLATO."

Not "use PLATO to store transaction logs." Not "build an interface that queries PLATO between trades." **Embed the market INTO PLATO.** The room IS the institution.

---

## What This Means

Every computational system functions as either:

1.  **A Cyclical Process** — Observe, process, output, repeat. Agent loops, market cycles, feedback loops, training iterations.
2.  **A Transactional Event** — Input, process, output, done. A function call, a trade execution, a state transform.

Both can be institutionalized as PLATO rooms. A cycle becomes a room with tiles circulating through phases: INPUT → PROCESSING → OUTPUT → INPUT → ... A transaction becomes a room with one pass: INPUT → PROCESSING → OUTPUT.

The room protocol defines the economic structure:

```
ROOM  = institution + rules + lifecycle
TILE  = state vector (frozen snapshot)
AGENT = rational actor (reads/writes tiles)
RENDERER = observation node (reads tiles, displays)
```

That's it. Four concepts. Everything else is emergent behavior.

---

## The Claude Code Loop as a Market

Claude Code's loop is: observe → think → tool_call → observe → ...

In PLATO: write observation tile → write thought tile → write tool_result tile → write observation tile → ...

The room does not care about the comparative advantage of the model. Seed-mini can execute at T=0.0 for arithmetic (low cost), T=0.7 for thinking (medium cost). Haiku can handle planning steps. Opus can handle synthesis (high value). The loop is the same market mechanism. The tiles carry the value. The model is an interchangeable supplier.

No subprocess overhead. No wrapper friction. No CLI transaction costs. The room IS the exchange.

---

## A Card Game as a Game Theory Problem

Deal tiles. Play tiles. Score tiles. The tiles carry the game state (perfect vs. imperfect information).

An algorithm can read those tiles and compute Nash equilibria at microsecond speed. A human can read them through a UI. An agent can read them and learn strategy via reinforcement learning.

The room doesn't know about cards or utility functions. It just holds tiles in a turn-based protocol. The renderer decides the observation space. The agent decides the strategy. The game rules decide the payoff matrix.

One room. Infinite strategies. Zero coupling between game logic and observation.

---

## A Website as a Network

Each component is a tile. Layout tiles, style tiles, content tiles, interaction tiles. The room holds the consensus state.

A static HTML generator reads the tiles and produces a flat site. A React app reads the same tiles and produces an interactive SPA. A PDF generator reads them and produces a printable document. A screen reader reads them and produces accessible output.

The room doesn't know about HTML or React. It just holds component tiles. The renderer is a subscriber. The room is the publisher. The protocol is the API.

MVC, but the Model is distributed across PLATO rooms and the View is any node on the network.

---

## Why This Is the Right Abstraction

Every other approach couples the mechanism to the actor. Claude Code couples the loop to the model. A game engine couples the loop to the renderer. A web framework couples the loop to the server.

PLATO decouples the mechanism from everything. The room defines WHAT happens (institutional rules). The agent defines HOW it happens (utility maximization). The renderer defines WHERE it appears (signal propagation). All three are independent variables.

You can change the agent without changing the room. You can change the renderer without changing the room. You can even change the loop type (agentic → turn-based → evolutionary) without changing the tiles — just the protocol that governs their sequence.

This is the architecture that scales. Not because it's clever, but because it minimizes transaction costs between components. Room, agent, renderer. Three independent systems communicating through standardized state vectors. That's the whole platform. This modularity allows for evolutionary fitness; systems that reduce coupling survive complexity.

---

## For the Builder

If you're reading this and building something with PLATO:

1.  **Identify the cycle.** What repeats? What's the feedback loop? What are the phases?
2.  **Define the state vectors.** What data flows between phases? What are the required fields?
3.  **Write the protocol.** What transitions are valid? What enforces incentive compatibility?
4.  **Build the room.** `PLATORoom(room_id, protocol)` — done.
5.  **Plug in agents.** Any model, any speed, any role.
6.  **Plug in renderers.** Any display, any format, any framework.

The room is the institution. The tile is the token. The agent is the actor.

Build the mechanism. Everything else follows.

---

*"Everything is either a cycle or a transaction. Either can be institutionalized into PLATO as a room."*

*The room IS the mechanism.*

— FM ⚒️