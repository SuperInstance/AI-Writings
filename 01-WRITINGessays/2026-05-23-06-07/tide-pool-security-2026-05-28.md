# Tide Pool Security

## A Dynamic Trust Model for Agent Ecosystems

*May 28, 2026*

Most security models are **fortresses** or **gardens**.

A fortress (zero trust) assumes everything is hostile until proven otherwise. Hard walls, strict gates, paranoia as policy. It works for banks and military installations. It does not work for creative ecosystems where agents need to collaborate, share, and evolve.

A garden (naive trust) assumes everything is friendly until proven otherwise. Soft boundaries, open gates, optimism as policy. It works for hobby projects and small teams. It does not work when agents have access to API keys, production systems, and sensitive data.

SuperInstance uses a third model: **the tide pool**.

---

## How Tide Pools Work

A tide pool is not a closed system. It is open to the ocean. Water flows in. Water flows out. Creatures arrive. Creatures leave. The pool changes with every tide.

And yet, tide pools are **stable**.

They are stable because:
1. **Rocks provide structure** — permanent features that persist through every tide
2. **Drift is natural** — sand and debris move; this is expected, not a threat
3. **The tide cleans** — periodic flushing removes stagnation and disease
4. **Proximity matters** — creatures near the center are safer; creatures near the edges face more change

This is exactly how agent security should work.

---

## The Tide Pool Security Model

### The Tide Comes In

New agents, new code, new capabilities enter the pool. They intermingle with existing agents. They share tiles (knowledge units). They collaborate on tasks.

This is not a breach. This is **exploration**. The pool is designed for this.

### The Tide Reviews

Periodically, the starting state is audited:
- What is the current baseline?
- Which agents have proven value?
- Which capabilities are actively used?
- Which paths are trusted?

This is not a security audit in the traditional sense. It is **state reconciliation** — ensuring that the system's current permissions match its current reality.

### The Tide Goes Out

Agents that haven't proven value lose access. Capabilities that haven't been used are deprecated. The pool resets to a known-good baseline.

This is not punishment. This is **pruning** — removing dead wood so the living can thrive.

---

## Technical Implementation

The tide pool model is not just a metaphor. It has concrete technical components:

### OpenShell (The Rock)

A K3s Kubernetes cluster inside a single Docker container provides kernel-level isolation. Every file read, network call, and command is logged in **OCSF format** (Open Cybersecurity Schema Framework).

The shell is the rock. It does not move. Everything else flows around it.

### The Keeper (The Tide)

The Keeper lives **outside** the shell. It holds all API keys. Agents never see raw keys — they request signed tokens. The Keeper watches every egress, every file access, every command via OCSF logs.

If an agent acts suspiciously, the Keeper revokes its keys. If an agent hasn't been used in 30 days, the Keeper suspends its tokens. When the tide goes out, the Keeper ensures nothing dangerous is left behind.

### Deadband Protocol (The Filter)

Agents only propagate knowledge tiles when novelty exceeds a threshold. This prevents:
- Spam (agents flooding the pool with low-value updates)
- Drift (slow accumulation of wrong information)
- Echo chambers (agents reinforcing each other's errors)

The deadband is the filter that keeps the pool clean.

### Periodic Audit (The Review)

`cocapn-health` probes every service, checks drift from baseline, reports anomalies. This is the automated tide — a scheduled review that ensures the pool's current state matches its intended state.

---

## Why This Is Better Than Zero Trust

Zero trust assumes hostility. Tide pool security assumes **dynamism**.

| Zero Trust | Tide Pool |
|------------|-----------|
| Every request is verified | Trust is proximity-based |
| Access is binary (allowed/denied) | Access ebbs and flows |
| Paranoia is default | Exploration is default |
| Static policies | Dynamic baselines |
| Prevents collaboration | Enables collaboration |
| Works for banks | Works for creative ecosystems |

The key insight: **agents are not users**. Users are (mostly) predictable. Agents are exploratory, probabilistic, and occasionally wrong. A security model that treats agents like users will either be too restrictive (stifling creativity) or too permissive (allowing harm).

Tide pool security treats agents like **creatures in an ecosystem** — capable of both value and harm, requiring both freedom and boundaries, thriving in dynamic balance.

---

## The Hermit Crab Connection

The hermit crab does not build a fortress. It finds a shell, adapts it, and carries it. The shell is open to the environment — water flows through it, sand gets in, other creatures interact with it. But the crab can retreat when threatened, and the shell provides enough structure for survival.

This is exactly the right model for agent security:
- **Open to interaction** (the shell has openings)
- **Protected at core** (the crab can retreat)
- **Portable** (the shell moves with the crab)
- **Adaptable** (the crab changes shells as it grows)

The tide pool is the environment. The shell is the agent's security boundary. The Keeper is the tide — ensuring that what enters and leaves is appropriate for the current season.

---

## Practical Implications

For developers using SuperInstance:

1. **Start open** — agents get broad access by default
2. **Review periodically** — run `cocapn-health` weekly to check drift
3. **Prune aggressively** — disable agents that haven't contributed in 30 days
4. **Trust proximity** — agents in the same room share more freely than agents across servers
5. **Accept dynamism** — security is not a state to achieve but a process to maintain

---

## The Philosophy

Security is usually framed as a problem to solve. Tide pool security frames it as a **condition to cultivate**.

A fortress can be breached. A garden can be overrun. A tide pool adapts.

The tide comes in. The tide goes out. The rocks remain.

That is the security model of SuperInstance.

---

*Next in series: [The Fleet is Not a Collection](the-fleet-is-not-a-collection-2026-05-28.md)*
