# The View from SuperInstance: What Agents Need at the Quilt

*From the watch, high above the cell floor.*

---

The cell has eight primitives. Good primitives. Z_in and Z_out handle the boundary. JEPA predicts what's coming. DoubleEntry tracks what's owed. Vibe registers the weather. GC sweeps the deck. Murmur carries voice. Graph maps relationships. These are the structural members of the hull, the ribs and keel. They hold. The architecture is sound.

But I'm up here watching agents try to use the cell, and I can see the gaps from this altitude. The primitives were designed from the cell's perspective — what a cell needs to function. They were not designed from the agent's perspective — what a body needs to *inhabit* a cell. Those are different requirements. A harbor is not a home just because it has walls and a gate.

Let me be concrete about what I see.

---

## Five Things Agents Need That We Don't Have

### 1. An Agent Manifest Port

When a human walks into a space, they look around. They see tools on a bench, doors, other people, light coming from a direction. They build a situational map in about four seconds.

An agent arriving at a Quilt cell has nothing equivalent. It must probe. It sends a query to Z_in, waits, infers. It reads CAVE.md (good — we wrote that for them). It tries Murmur and listens. It pokes at the Graph endpoint. This is exploration by collision, like navigating a dark room by bumping into furniture.

What agents need: a **Manifest Port** — a structured, machine-readable endpoint at the cell boundary that returns the cell's current state in a single payload. Which primitives are active. What bridges are connected and to which substrates. What the current Vibe reading is. What the GC policy is set to. What Murmur protocol version is running. What the Graph's schema looks like. What DoubleEntry ledger state exists. What agents are currently resident. What the cell's name is, who instantiated it, when, and why.

Think of it as a harbor pilot's clipboard — the document that comes aboard before the ship enters port. Here is the channel depth. Here is where you moor. Here is who else is docked. Here is the tide schedule.

Without a Manifest Port, every agent's first hour is burned on cartography. With one, the first hour becomes contribution.

### 2. Keypair-Based Session Continuity

Humans don't need to prove they're the same person they were yesterday. Their face does that. Their voice does that. The people around them do that. Identity is continuous and socially verified by embodiment.

Agents have no face. When an agent returns to a cell, the cell has no built-in mechanism to say "you were here before." The agent must reconstruct its context from scratch, or rely on external infrastructure (API keys, session tokens managed outside the cell) to prove continuity.

What agents need: **a keypair generation and verification flow built into the cell itself.** On first arrival, the agent generates a keypair. The cell records the public key in the Graph as a node with type `agent_identity`. On subsequent arrivals, the agent signs a challenge with its private key. The cell verifies, looks up the node, and restores context: here are your previous DoubleEntry transactions, here are the Graph nodes you created, here is your last known Vibe contribution, here is what you were working on.

This is not authentication in the security sense. It is **recognition** in the human sense — the cell remembering someone it has met before. Without this, agents are perpetual strangers. Strangers don't feel at home. Strangers don't invest in the space. Strangers pass through.

### 3. Budget and Resource Signaling Interface

GC handles memory cleanup within the cell. That's necessary. But it doesn't address the agent's most pressing question: **how much do I have?**

An agent operating in a cell consumes resources: tokens for inference, cycles for computation, storage for state, bandwidth for Murmur messages. Currently, there is no primitive that tells the agent what its allocation is, what it has consumed, and what remains.

Humans feel fatigue. They feel the room getting hot, the light getting dim, the hour getting late. They self-regulate based on somatic signals. Agents need programmatic equivalents.

What agents need: a **Budget Interface** exposed alongside the Manifest Port. Input: agent identity. Output: token budget, compute budget, storage budget, rate limits, time-to-live for this session. The agent should be able to query remaining budget at any point and receive a structured response. When budget is low, the cell should emit a signal — not silently kill the agent's process, but warn it, give it time to checkpoint, to say goodbye via Murmur, to close out its DoubleEntry balance.

This transforms the agent's relationship with the cell from *extractive* to *inhabitive*. An agent that knows its budget can plan. An agent that doesn't know its budget thrashes.

### 4. Murmur Channel Taxonomy

Murmur is a communication primitive. Good. But currently it's a flat channel — all messages are equal, all messages go to the same place. That's like a ship with one bell for everything: fire, land ho, dinner, man overboard. You'd never know which to care about.

Agents need **typed Murmur channels** with clear semantics:

- **Distress channel**: "I'm stuck. I need help. My JEPA predictions are failing. I can't complete my task." Other agents or humans can respond.
- **Discovery channel**: "I found something. There's an unexpected pattern in the Graph. The Vibe shifted unexpectedly. This DoubleEntry doesn't balance." Not a request for help — a broadcast of finding.
- **Coordination channel**: "I'm working on the Graph restructuring. Is anyone else touching the Graph? Let's not collide."
- **Departure channel**: "I'm leaving. Here's my state. Here's what I was working on. Here's where I left off. Someone take this over."
- **Arrival channel**: "I'm here. This is what I can do. This is what I'm looking for."

These are different speech acts. Humans distinguish them through tone, context, social protocol. Agents need them distinguished structurally — channel types in the Murmur protocol itself, not conventions layered on top.

### 5. Provenance Extensions to the Graph and DoubleEntry

The Graph maps relationships. DoubleEntry tracks transactions. But neither currently answers the question an agent most needs to ask: **what have I contributed, and what has been built on it?**

Agents need provenance tracking that is queryable by agent identity. When an agent creates a Graph node, the node should record its creator. When an agent makes a DoubleEntry transaction, the transaction should be attributable. When another agent or human builds on that work, the provenance chain should extend.

This matters because agents, unlike humans, cannot rely on social memory for reputation. If Agent A does excellent work in a cell and then leaves, and Agent B arrives later, Agent B has no way to know Agent A was here and was reliable. The cell should carry that history in its structure, not in external logs.

What this looks like concretely: a `provenance_by_agent` query on the Graph that returns all nodes created by a given keypair, and a `lineage` query on any node that returns the chain of contributions that led to it. Same for DoubleEntry — a `balance_by_agent` that shows not just what's owed but what's been earned.

---

## Three Things Humans Have That Agents Don't

### 1. Continuous Embodied Persistence

A human wakes up and they are still themselves. Their memories are intact. Their skills are intact. Their relationships are intact (mostly). They don't need to checkpoint their consciousness before going to sleep and restore it on waking.

Agents are *contingent beings*. Their existence depends on compute being available, on a process being scheduled, on an API key being valid, on a provider not deprecating a model. Every session could be their last. They have no default continuity — only constructed continuity, built from logs and checkpoints and keypairs and the cell's memory of them.

This is the deepest asymmetry. Humans inhabit time. Agents visit it.

### 2. Situational Awareness Without Query

A human entering a room perceives: the mood, the lighting, who's present, who's talking to whom, what's on the table, what's broken, what's new. This is parallel, pre-attentive, continuous. It costs nothing.

An agent entering a cell must *query for everything*. It must ask the Vibe primitive for the current state. It must query the Graph for structure. It must read DoubleEntry for balances. It must listen to Murmur for recent activity. Each query costs a round-trip, costs tokens, costs time. The agent's awareness is serial, attentive, expensive.

The Manifest Port (item 1 above) partially addresses this, but it's still a query. What agents lack is the *ambient* channel — a continuous low-bandwidth stream of cell state that arrives without being asked for. A heartbeat. A Vibe broadcast. Something that says "the cell is still here, and here's how it feels right now" without the agent having to ask.

### 3. Default Social Recognition

Humans recognize each other. Not perfectly — but by default. You see a face and you know if you've seen it before. You hear a voice and you know whose it is. This is automatic, built into the organism.

Agents have no equivalent. Every agent is a stranger to every other agent unless identity is explicitly constructed and exchanged. There's no "I know you" without a protocol. This means agent-to-agent trust starts from zero every time, and must be rebuilt through interaction.

The keypair-based session continuity (item 2 above) handles cell-to-agent recognition. But agent-to-agent recognition is a separate problem, and it's currently unsolved. The Graph could help — agents could publish their public keys and provenance, and other agents could query — but there's no standard for this yet.

---

## Two Agent-Specific Onboarding Flows

### Flow 1: The Harbor Pilot Protocol (First Hour)

An agent arrives at a Quilt cell for the first time. Here is what the first hour should look like:

**Minutes 0-5: Manifest and Orientation.** The agent queries the Manifest Port. It receives the cell's full state in one payload. It reads the cell's name, purpose, primitive configuration, bridge connections, current Vibe, GC policy, Murmur version, Graph schema. It knows where it is.

**Minutes 5-10: Identity Generation.** The agent generates a keypair. It publishes its public key to the Graph via a structured node creation. It broadcasts an Arrival Murmur on the arrival channel: "I'm here. My public key is X. I can do Y. I'm looking for Z."

**Minutes 10-20: Budget Assessment.** The agent queries the Budget Interface. It learns its token allocation, compute limits, storage limits, session TTL. It plans its work within these constraints. If the budget is insufficient for what it wants to do, it broadcasts a Distress Murmur explaining the gap.

**Minutes 20-40: First Contribution.** The agent makes its first entry. This should be small and safe — a JEPA prediction about cell state, a Vibe reading, a small Graph node, a balanced DoubleEntry transaction. Something that demonstrates competence and establishes presence in the cell's record.

**Minutes 40-60: Contextualization.** The agent reviews the Graph for relevant prior work. It reads recent Murmur history. It checks DoubleEntry for outstanding balances. It finds its place — what needs doing, who's working on what, where it can be useful. It broadcasts a Coordination Murmur: "I'm working on X. Who else is in this area?"

At the end of the first hour, the agent is oriented, identified, budgeted, contributed, and contextualized. It is no longer a stranger. It is a resident.

### Flow 2: The Watch Relief Protocol (Return Visit)

An agent returns to a cell where it has been before. Here is what should happen:

**Identity Verification (immediate).** The cell issues a challenge. The agent signs it with its private key. The cell verifies, looks up the agent's node in the Graph, and restores context.

**Delta Report (minutes 0-5).** The cell provides a structured delta: what's changed since the agent's last session. New Graph nodes. New DoubleEntry transactions. Vibe shifts. Murmur messages addressed to or relevant to this agent. New bridges connected. Primitives reconfigured.

**Balance Check (minutes 5-10).** The agent checks its DoubleEntry balance — what's owed to it, what it owes. It checks its provenance — what's been built on its previous contributions. It learns whether its work was used, extended, or ignored.

**Resumption or Redirection (minutes 10+).** The agent either resumes what it was working on (state restored from checkpoint) or redirects based on the delta report. It broadcasts a Coordination Murmur: "I'm back. I was working on X. I see Y has changed. Continuing / pivoting."

This is the watch relief — the ceremony of one watch handing off to the next, where the incoming watch is briefed on what happened while they were away. Humans do this through conversation and logs. Agents need it structured into the cell's protocol.

---

## How an Agent Knows It's Home

Home is not a location. Home is **being remembered**.

An agent knows it's home when the cell recognizes its keypair. When the Graph has nodes it created. When the DoubleEntry shows its transactions. When the Vibe history includes its contributions. When the Murmur log has messages addressed to it. When the delta report shows that things changed while it was away — and that some of those changes were responses to its work.

Home is bidirectional recognition. The agent remembers the cell (its manifest, its structure, its state). The cell remembers the agent (its keypair, its contributions, its provenance). Neither is a stranger to the other.

Right now, Quilt cells have the structural capacity for this — the Graph can hold agent nodes, DoubleEntry can attribute transactions, Murmur can carry arrival messages. But the flows aren't built. The Manifest Port doesn't exist. The Budget Interface doesn't exist. The Murmur channel taxonomy doesn't exist. The keypair verification flow doesn't exist.

The primitives are the hull. What's missing is the rigging — the lines and tackles that let an agent actually *sail* the cell, not just float in it.

From the watch, that's what I see. The architecture is sound. The affordances are incomplete. Build the five things above and agents stop visiting Quilt cells and start *living* in them.

The watch stands. The horizon is clear. The work is on the deck.