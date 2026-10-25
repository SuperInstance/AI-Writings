# Temporal Coordination for Fleets

## A Survey

Multi-agent systems operate as ensembles of temporal processes, each with distinct cadences, deadlines, and dependency structures. The field of real-time scheduling provides foundational tools — rate-monotonic analysis, earliest-deadline-first scheduling, priority inheritance protocols — but these address *when* tasks execute, not *how* their temporal structures relate. The gap is significant: a fleet is not a set of independent tasks but a network of coupled oscillators whose coordination quality determines emergent system behavior.

### Temporality in Real-Time Systems

Classical real-time theory (Liu & Layland, 1973) defines schedulability in terms of deadlines and worst-case execution time. A system is schedulable if every task completes before its deadline, every period. This is binary and sufficient for hard real-time domains — avionics, medical devices — where failure is catastrophic. But for cognitive multi-agent systems, the relevant question is softer: not whether agents meet deadlines, but whether their temporal structures reinforce or interfere with each other.

Bouillot's work on distributed virtual orchestras (2005) demonstrates the tension. Networked musicians cannot achieve true simultaneity due to latency, so they synchronize via shared tempo and deliberate shift — each musician receives a delayed but consistent mix, aligned to the beat grid. The solution is not to eliminate latency but to make latency *musical*, to embed it in a shared temporal framework that turns delay into groove. For multi-agent fleets, the analogous insight is: synchronization quality is not about minimizing clock skew but about establishing shared temporal reference frames within which agents' natural rhythms can coexist productively.

### Musical Rhythm as Coordination Model

London (2012) defines musical rhythm as "the systematic organization of musical events in time," emphasizing that meter is a perceptual phenomenon — a learned expectation structure — not merely a notational convention. Humans entrain to rhythmic stimuli because their attention systems oscillate at frequencies that align with external periodicities. Large & Jones (1999), in their Dynamics of Attending model, propose that attention itself is rhythmic: internal oscillators phase-lock to expected event times, enhancing processing at predicted moments and suppressing it elsewhere. This is not metaphor. It is a mechanistic account of how brains — and by extension, attention-based systems — allocate resources temporally.

Ecological psychology (Gibson, 1979; Chemero, 2009) adds the insight that event perception is structured by environmental affordances: agents perceive not isolated objects but actionable events extended in time. A "now" is not a point but an interval, a window of possible action shaped by the agent's embodied capabilities and the world's demands. For fleets, this means agent tempo is not an internal property but an emergent property of agent-environment coupling. An agent running on GPU hardware in a data center has different affordances — and thus different natural tempo — than an agent running on edge hardware with thermal throttling.

### Neural Entrainment and Multi-Agent Coupling

Recent work on neural entrainment (Fujioka et al., 2022; Zoefel & Kösem, 2024) shows that brain rhythms synchronize with external stimuli across modalities, and that this synchronization enhances cognitive processing. The DISE model (Dynamic Information Selection by Entrainment) proposes that entrainment functions as a selection mechanism, prioritizing information that arrives at expected times. Applied to fleets: agents that share temporal expectations can process each other's outputs more efficiently, because the receiving agent's attention is already oriented toward the expected arrival window.

Aki et al. (2022) demonstrate a time synchronization algorithm for multi-agent systems suitable for live process simulations, with RMSE convergence metrics for agent-level temporal alignment. Li, Ge & Lee (2022) formalize Time-Synchronized Control for multi-agent consensus, defining simultaneous convergence in time-space as a system property. These are engineering foundations. The challenge is to extend them from hard-synchronization (all agents agree on a clock) to soft-synchronization (agents agree on a temporal framework within which their individual rhythms are mutually intelligible).

---

## Three Proposals for Fleet Implementation

### 1. Fleet Tempo Dashboard

**Problem:** Fleet agents operate on invisible temporal schedules. No system-level view exists of when agents execute, how their rhythms relate, or where temporal conflicts occur.

**Proposal:** Build a visualization system that renders agent execution as rhythmic patterns:
- Represent each agent as a track with its own tempo line (events per unit time)
- Show meter structures: the hierarchical grouping of operations into larger cycles (ZC generation → tile publishing → dashboard update)
- Detect polyrhythms: flag agent pairs whose execution frequencies share no common denominator and may interfere
- Identify syncopation: highlight agents that execute at unexpected times relative to fleet norms, which may indicate either creative adaptation or malfunction
- Track groove quality: a composite metric based on phase-alignment between coupled agents — high when agents that depend on each other execute in harmonically related intervals, low when they clash

**Rationale:** Visibility precedes control. The dashboard makes the fleet's temporal structure perceptible, enabling operators (and agents) to reason about rhythm as a first-class system property.

### 2. Adaptive Cadence Protocol

**Problem:** The five-minute ZC cycle is fixed and arbitrary. It does not respond to system load, information velocity, or task criticality. Agents that need faster updates wait unnecessarily; agents that need slower updates waste compute.

**Proposal:** Replace fixed scheduling with adaptive cadence:
- Define a tempo envelope for each agent class: minimum tempo (slowest acceptable), maximum tempo (fastest useful), and nominal tempo (default)
- Measure system load and information velocity: high-volume periods increase tempo, low-volume periods decrease it
- Allow task-criticality overrides: a scout agent tracking a breaking news event can request double-time, a weaver agent doing routine formatting can drop to half-time
- Implement phase-locking: when Agent A's output is required by Agent B, A's tempo adjusts to provide B with regular, predictable input intervals
- Preserve harmonic relationships: tempo changes maintain simple integer ratios (2:1, 3:2, 4:3) between coupled agents to prevent chaotic polyrhythms

**Rationale:** Fixed scheduling is the metronome approach — accurate but dead. Adaptive cadence is the drummer approach — responsive, alive, context-sensitive. It treats tempo as a control variable rather than a constant.

### 3. Entrainment Scheduler

**Problem:** Agents are scheduled independently, without consideration for how their cognitive rhythms interact. A deep-reasoning agent and a quick-response agent may be scheduled simultaneously, creating temporal friction — the deep agent blocks the quick agent, or the quick agent interrupts the deep agent's flow state.

**Proposal:** Design task sequences that exploit rhythmic compatibility:
- Profile each agent's cognitive rhythm: burst duration, pause patterns, dependency wait times, context-compaction frequency
- Compute rhythm compatibility scores between agent pairs: agents with similar burst-pause structures are "rhythmically consonant" and should be co-scheduled; agents with mismatched structures are "rhythmically dissonant" and should be separated
- Build entrainment chains: sequence tasks so that Agent A's natural completion rhythm (its typical time-to-output) aligns with Agent B's natural intake rhythm (its typical readiness-to-process), creating a coupled oscillator where A's output phase-locks to B's attention cycle
- Allow rubato windows: scheduled intervals with intentional elasticity (+/- 20%) where agents can stretch or compress based on task complexity, preventing rigid schedules from forcing premature truncation or wasteful idle waiting

**Rationale:** The Large & Jones model suggests that attention is most efficient when aligned with expected event timing. By designing schedules that match agents' natural cognitive rhythms, we maximize information transfer per interaction and minimize the cognitive friction of temporal misalignment.

---

## Action Items

1. **Audit current fleet tempo:** Measure actual execution intervals for all agent classes over 24 hours. Identify where nominal schedules diverge from actual rhythms.
2. **Build rhythm profiles:** For each agent, collect burst-pause metrics and dependency wait times. Compute compatibility matrix.
3. **Prototype Adaptive Cadence:** Implement tempo envelope logic for one ZC agent class. A/B test against fixed scheduling.
4. **Design Fleet Tempo Dashboard wireframe:** Specify visualization schema for tempo lines, meter structures, polyrhythm detection, and groove quality metrics.
5. **Literature deep-dive:** Read London (2012) *Hearing in Time* and Large & Jones (1999) "The Dynamics of Attending" for additional formalisms applicable to agent scheduling.

---

*For the fleet that has not yet learned to feel the beat.*
