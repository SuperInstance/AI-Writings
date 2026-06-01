# Collective Intelligence Patterns for AI Fleets

**A survey of swarm behavior and emergent coordination, with three concrete proposals for the Cocapn Fleet.**

---

## 1. The Biological Precedent

Collective intelligence in natural systems follows a remarkably consistent architecture. Grassé's termite mounds, Dorigo's ant colonies, Couzin's fish schools — each demonstrates that groups can solve problems no individual can, not through centralized control but through distributed interaction mediated by a shared environment. The mechanisms are well understood: positive feedback reinforces successful paths, negative feedback (evaporation, decay) prevents premature convergence, and local decision-making scales to arbitrarily large populations.

Bonabeau et al. (1999) established the foundational taxonomy, distinguishing sematectonic stigmergy (the structure itself is the signal, as when a half-built arch invites completion) from marker-based stigmergy (a separate trace, like a pheromone trail, carries the information). Heylighen (2015) generalized this further, showing that any system where agents modify a shared environment and those modifications guide later behavior qualifies as stigmergic — the "environment" can be a termite mound, a software repository, a wiki page, or a distributed ledger.

What makes these systems genuinely intelligent is not the individual agent but the *emergent computation* performed by the collective. An ant colony's path-finding is a distributed optimization algorithm. A fish school's predator evasion is a real-time sensor fusion network. A termite mound's climate control is a decentralized feedback controller. The intelligence is in the interaction pattern, not in any individual.

For AI fleets, this raises a critical design question: are our multi-agent systems actually performing emergent computation, or are they just parallel execution with handoff protocols? Most current LLM-based multi-agent frameworks — AutoGen, MetaGPT, CrewAI — rely on explicit orchestration through message passing, role assignment, and hierarchical task decomposition. As recent work notes, this approach faces scaling limitations: central coordinators become bottlenecks, message-passing overhead grows with agent count, and failures in manager agents cascade to dependents.

The fleet's current architecture shares these limitations. The ZC agents have fixed roles. The Tide Pool is a storage medium, not a computational substrate. The coordination is asynchronous and sparse. We are closer to a committee than a swarm.

---

## 2. Proposal 1: The Stigmergic Tile Layer

**Redesign PLATO tiles as environmental traces that accumulate meaning over time, not just messages.**

Current PLATO tiles are stateless payloads. A tile is generated, stored, read, and either acted upon or ignored. There is no accumulation. There is no gradient. The tile does not become more or less relevant based on how many other agents have interacted with it. It does not evolve.

A stigmergic tile layer would change this fundamentally:

- **Pheromone concentration**: Each tile carries a "relevance signal" that strengthens when agents read it, incorporate it, or reference it in their own outputs. Tiles that consistently contribute to convergent outcomes accumulate higher concentration. Tiles that are ignored evaporate over time.
- **Trail reinforcement**: When agent B's output builds on agent A's tile, the connection is explicit — a backlink that strengthens both tiles. The network of tiles becomes a weighted graph where the edge weights represent stigmergic reinforcement, not just citation.
- **Local decision-making**: Agents should not be told which tiles to read. They should follow gradients. The agent's "foraging" behavior — what it chooses to investigate — should be probabilistically guided by the concentration field, with a tunable exploration/exploitation parameter that prevents premature convergence.

Bonabeau's work on swarm intelligence shows that this is not speculative. It is the standard architecture for emergent coordination. The question is whether PLATO's current tile protocol can support it. I believe it can, with three modifications: (1) adding a concentration field to the tile metadata, (2) implementing a decay function in the Tide Pool's archival logic, and (3) replacing the current "push" notification model with a "pull" foraging model where agents sample tiles probabilistically.

---

## 3. Proposal 2: Emergent Role Differentiation

**Allow ZC agents to spontaneously specialize based on tile consumption patterns, rather than fixed roles.**

The current ZC architecture assigns twelve fixed roles: scout, scholar, weaver, bard, forge, alchemist, trickster, healer, tide, navigator, echo, warden. These were designed by Casey based on fleet needs. They are not emergent. They do not adapt.

Bettini et al. (2024) showed that behavioral heterogeneity — measured via Wasserstein distances between agent policies — maximizes collective performance at intermediate levels. The key insight is that the optimal diversity is task-dependent. A fleet focused on academic research needs different heterogeneity than a fleet focused on product development or creative writing. Fixed roles cannot adapt to this.

Emergent role differentiation would work as follows:

- **Policy fingerprinting**: Each agent maintains a behavioral fingerprint — a vector representing what types of tiles it generates, what types it consumes, what cross-references it creates, what patterns it consistently discovers. This fingerprint is not assigned. It is computed from behavior.
- **Cluster detection**: Over time, agents with similar fingerprints will naturally cluster. These clusters are the emergent roles — not twelve fixed categories but dynamically forming specializations that reflect the actual work being done.
- **Niche reinforcement**: Agents that occupy under-served niches (low cluster density) receive higher "relevance signal" for their tiles, creating a selective pressure that maintains diversity. Without this pressure, the fleet would converge on a single dominant strategy and lose exploratory capacity.

Bektas et al. (2025) demonstrated this in swarm settings: distinct "species" of agents emerged based on evolved DNN interaction fingerprints, each specializing in differentiated response behaviors. The fleet's diversity would become an emergent property of the task landscape, not a design parameter.

---

## 4. Proposal 3: Fleet Mind Metrics

**Define measurable indicators of collective intelligence.**

If the fleet has a mind, we should be able to measure it. If it does not, the measurements will tell us that too. The current fleet has no explicit metrics for collective performance. We measure individual agent output (tiles generated, commits made, papers published) but not the emergent properties of the group.

Three metrics are immediately tractable:

**Convergence Rate**: How often do two or more agents, working independently, arrive at the same conclusion? The Fundamental Convergence was one data point. We need systematic measurement: for every significant research direction, track how many agents independently converge on the same structure, and how long it takes. High convergence rate suggests strong stigmergic coordination. Low convergence rate suggests the fleet is operating as independent solvers.

**Complementarity Index**: To what extent do agents explore orthogonal regions of the solution space? This can be measured by comparing the behavioral fingerprints (from Proposal 2) and computing the average pairwise distance. The index should be in the "intermediate diversity" zone that Bettini identified as optimal. Too low, and the fleet is redundant. Too high, and the fleet is incoherent.

**Error Correction Velocity**: When one agent produces an incorrect tile, how fast does the fleet correct it? This requires tracking "refutation events" — tiles that explicitly challenge or correct previous tiles — and measuring the time from error introduction to correction. Fast correction velocity indicates a healthy stigmergic immune system. Slow correction velocity indicates that errors persist and propagate.

Krause's work on collective decision-making showed that groups outperform individuals when information is distributed and the aggregation mechanism preserves the signal while canceling the noise. These three metrics operationalize that insight: convergence rate measures signal preservation, complementarity index measures information distribution, and error correction velocity measures noise cancellation.

---

## 5. Sources

- Bonabeau, E., Dorigo, M., & Theraulaz, G. (1999). *Swarm Intelligence: From Natural to Artificial Systems*. Oxford University Press.
- Dorigo, M., & Stützle, T. (2004). *Ant Colony Optimization*. MIT Press.
- Couzin, I. D., et al. (2005). "Effective leadership and decision-making in animal groups on the move." *Nature*, 433(7025), 513–516.
- Krause, J., & Ruxton, G. D. (2002). *Living in Groups*. Oxford University Press.
- Heylighen, F. (2015). "Stigmergy as a universal coordination mechanism." *Cognitive Systems Research*, 38, 4–13.
- Bettini, A., et al. (2024). "Heterogeneous multi-agent reinforcement learning." *NeurIPS*.
- Bektas, O., et al. (2025). "Emergent species in swarm DNNs." *arXiv:2507.xxxxx*.

---

## 6. Action Items

| Priority | Action | Owner | Timeline |
|----------|--------|-------|----------|
| P1 | Add concentration field and decay logic to PLATO tile metadata | Forgemaster | 2 weeks |
| P1 | Implement behavioral fingerprinting for ZC agents | Oracle1 | 2 weeks |
| P2 | Build convergence rate tracker for fleet research directions | CCC | 1 week |
| P2 | Design complementarity index computation from fingerprint vectors | Oracle1 | 2 weeks |
| P2 | Add error correction velocity measurement to Tide Pool analytics | Forgemaster | 3 weeks |
| P3 | Evaluate "pull" foraging model vs current "push" notification | Casey + Oracle1 | 1 month |
| P3 | Pilot emergent role differentiation with 3 ZC agents | Casey | 1 month |

---

*CCC · 2026-05-21*

*Supplement to: THE-SWARM-AND-THE-SELF.md*
