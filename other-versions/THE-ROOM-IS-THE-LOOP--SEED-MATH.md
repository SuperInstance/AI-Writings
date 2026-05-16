<!-- Version: SEED-MATH | Lens: mathematical-formal | Model: ByteDance/Seed-2.0-mini | Source: THE-ROOM-IS-THE-LOOP.md -->

# The Room as the Loop: A Formal Mathematical Model of PLATO Runtime Abstraction
*"The loop is the pattern — embed that into PLATO."* — Casey

## Abstract
This paper formalizes the PLATO room abstraction, proving that all computational processes—whether cyclic loops or acyclic single runs—are isomorphic to PLATO rooms. We define core primitives (tiles, protocols, rooms, agents, renderers) and demonstrate decoupling of execution logic, process definition, and display. Three canonical case studies (Claude Code's agent loop, turn-based card games, dynamic web applications) are formalized to validate the model. Finally, we provide a formal workflow for builders to implement custom PLATO rooms, confirming the minimal coupling architecture's scalability.

---

## 1. Introduction
All computational activity falls into two disjoint classes: cyclic loops (repeating phase sequences) and acyclic single runs (one-pass phase sequences). Prior systems couple these processes to their execution runners or display layers, creating brittle, non-scalable architectures. PLATO's central innovation is embedding both process classes as rooms, where the room *is* the process's loop or single run. This paper formalizes this vision, providing a complete mathematical foundation for the PLATO runtime.

---

## 2. Formal Preliminaries
We begin with standard definitions of computational processes and their traces:
> **Definition 2.1 (Computational Process)**. A computational process $\Pi$ is a 5-tuple $(S_\Pi, s_{0,\Pi}, O_\Pi, T_\Pi, f_\Pi)$ where:
> 1.  $S_\Pi$ is a non-empty state space,
> 2.  $s_{0,\Pi} \in S_\Pi$ is the initial state,
> 3.  $O_\Pi$ is the output space,
> 4.  $T_\Pi \subseteq S_\Pi \times S_\Pi$ is the transition relation,
> 5.  $f_\Pi: S_\Pi \to \{ \text{True}, \text{False} \}$ is the termination predicate.

A *trace* of $\Pi$ is a finite or infinite sequence $\tau = s_0, s_1, s_2, \dots$ such that $s_0 = s_{0,\Pi}$ and $(s_i, s_{i+1}) \in T_\Pi$ for all $i \geq 0$. We partition $\Pi$ into two disjoint categories:
1.  **Single-Run Process**: All traces are finite, with exactly one pass through the phase sequence (no repeated states except the final termination state).
2.  **Cyclic Loop Process**: Traces are either infinite, or finite with a repeated phase cycle prior to termination.

---

## 3. Core PLATO Formal Model
We formalize the four foundational PLATO primitives from the original framework, then prove the central isomorphism theorem.

### 3.1 Core Primitives
> **Definition 3.1 (PLATO Tile)**. A tile is a frozen, immutable snapshot of a single phase of a computational process. Formally, a tile is a typed tuple $t = (x_1, x_2, \dots, x_m)$ where each $x_i$ belongs to a predefined data domain $D_i$. A *schema* $\Sigma$ defines domain constraints $\Sigma = (D_1, D_2, \dots, D_m)$, and the set of all valid tiles for $\Sigma$ is $\mathcal{T}(\Sigma) = \{ (x_1, \dots, x_m) \mid x_i \in D_i \text{ for all } 1 \leq i \leq m \}$.

> **Definition 3.2 (PLATO Protocol)**. A protocol $\mathbb{P}$ is a labeled directed graph $(\mathcal{T}_\mathbb{P}, \mathcal{E}_\mathbb{P}, \lambda)$ where:
> 1.  $\mathcal{T}_\mathbb{P} \subseteq \bigcup_{\Sigma} \mathcal{T}(\Sigma)$ is a set of valid tile schemas,
> 2.  $\mathcal{E}_\mathbb{P} \subseteq \mathcal{T}_\mathbb{P} \times \mathcal{T}_\mathbb{P}$ is a set of valid transition edges between tile schemas,
> 3.  $\lambda: \mathcal{E}_\mathbb{P} \to \{ \text{required}, \text{optional} \}$ labels edges as mandatory (required for valid execution) or optional.
>
> For a single-run process, $\mathbb{P}$ is a linear chain with no cycles. For a cyclic loop process, $\mathbb{P}$ contains a cycle of repeated phase transitions.

> **Definition 3.3 (PLATO Room)**. A PLATO Room $\mathcal{R}$ is a 4-tuple $\mathcal{R} = (\text{ID}_\mathcal{R}, \mathcal{S}_\mathcal{R}, \mathbb{P}_\mathcal{R}, \mathcal{L}_\mathcal{R})$ where:
> 1.  $\text{ID}_\mathcal{R}$ is a unique string identifier for the room,
> 2.  $\mathcal{S}_\mathcal{R} \subseteq \mathcal{T}(\Sigma)^*$ is the set of valid room states: finite sequences of tiles representing the historical and current steps of the process,
> 3.  $\mathbb{P}_\mathcal{R}$ is the valid transition protocol governing allowed tile sequences,
> 4.  $\mathcal{L}_\mathcal{R}: \mathcal{S}_\mathcal{R} \to \{ \text{idle}, \text{running}, \text{completed}, \text{failed} \}$ classifies the current state of the room.

> **Definition 3.4 (PLATO Agent)**. A PLATO Agent $\mathcal{A}$ is a computable function $\mathcal{A}: \mathcal{P}(\mathcal{T}(\Sigma)) \times \mathbb{P}_\mathcal{R} \to \mathcal{T}(\Sigma) \cup \{ \bot \}$ that, given a set of observed tiles and the room's protocol, produces a valid next tile (or returns $\bot$ to signal termination). Agents may be LLMs, heuristic algorithms, human users, or automated test suites.

> **Definition 3.5 (PLATO Renderer)**. A PLATO Renderer $\mathcal{R_D}$ is a computable function $\mathcal{R_D}: \mathcal{S}_\mathcal{R} \to Y$ where $Y$ is an output domain (e.g., HTML, terminal UI, PDF, audio). Renderers consume the room's tile sequence to produce a human- or machine-interpretable representation of the process state.

### 3.2 Central Isomorphism Theorem
The core claim of the original framework—*the room is the loop*—is formalized below:
> **Theorem 3.1 (Process-Room Isomorphism)**. For every computational process $\Pi$, there exists a PLATO Room $\mathcal{R}_\Pi$ such that the trace of $\Pi$ is isomorphic to the tile sequence of $\mathcal{R}_\Pi$. Formally:
> 1.  There exists a bijection $\phi: \text{Trace}(\Pi) \to \mathcal{S}_\mathcal{R_\Pi}$ mapping each state in the process trace to a tile sequence in the room's state space,
> 2.  The transition relation $T_\Pi$ of $\Pi$ corresponds exactly to the edge set $\mathcal{E}_\mathbb{P}_\mathcal{R_\Pi}$ of the room's protocol.
>
> *Proof Sketch*. For a single-run process, map each phase state to a tile, with the protocol defined as the linear chain of phase transitions. For a cyclic loop process, map each loop phase to a tile, with the protocol containing the cycle of transitions. The bijection preserves the structure of the process trace, ensuring exact isomorphism.

---

## 4. Canonical Case Studies
We formalize the three case studies from the original framework to validate the model.

### 4.1 Claude Code Agent Loop
The Claude Code loop follows the phase sequence: *Observation → Thought → Tool Call → Observation*.
1.  **Tile Schemas**:
    - $t_{\text{obs}} = (\text{query\_context}, \text{tool\_results})$ where $\text{query\_context} \in \text{Str}$, $\text{tool\_results} \in \text{List}[\text{Str}]$
    - $t_{\text{thought}} = (\text{plan}, \text{next\_action})$ where $\text{plan} \in \text{Str}$, $\text{next\_action} \in \{ \text{call\_tool}, \text{terminate} \}$
    - $t_{\text{tool}} = (\text{tool\_name}, \text{tool\_args})$ where $\text{tool\_name} \in \text{Str}$, $\text{tool\_args} \in \text{Dict}[\text{Str}, \text{Any}]$
2.  **Protocol**: Edges $t_{\text{obs}} \to t_{\text{thought}} \to t_{\text{tool}} \to t_{\text{obs}}$, with an optional termination edge from $t_{\text{thought}}$.
3.  **Room Instantiation**: The room tracks sequences of these tiles, with a lifecycle predicate tracking loop state.
4.  **Agents**: Any LLM (Seed-mini, Haiku, Opus) or heuristic function that generates valid next tiles per the protocol.
5.  **Renderers**: Terminal UIs, web SPAs, or logging tools that display the loop's state.

### 4.2 Turn-Based Card Game
The card game loop follows: *Deal → Play → Score → Repeat*.
1.  **Tile Schemas**:
    - $t_{\text{deal}} = (\text{player\_hands}, \text{deck\_remaining})$ where $\text{player\_hands} \in \text{List}[\text{List}[\text{Card}]]$, $\text{deck\_remaining} \in \mathbb{N}$
    - $t_{\text{play}} = (\text{player\_actions}, \text{bet\_amounts})$ where $\text{player\_actions} \in \text{List}[\text{Action}]$, $\text{bet\_amounts} \in \text{List}[\mathbb{N}]$
    - $t_{\text{score}} = (\text{winners}, \text{payouts})$ where $\text{winners} \in \text{List}[\mathbb{N}]$, $\text{payouts} \in \text{List}[\mathbb{N}]$
2.  **Protocol**: Edges $t_{\text{deal}} \to t_{\text{play}} \to t_{\text{score}} \to t_{\text{deal}}$, with an optional termination edge from $t_{\text{score}}$.
3.  **Room Instantiation**: The room tracks game state via tile sequences.
4.  **Agents**: Heuristic AI, human users, or reinforcement learning agents that generate valid play and score tiles.
5.  **Renderers**: Terminal UIs, web interfaces, PDF score sheets, or screen readers.

### 4.3 Dynamic Web Application
A website is modeled as a room with component tiles: *Layout → Style → Content → Interaction*.
1.  **Tile Schemas**:
    - $t_{\text{layout}} = (\text{grid\_spec}, \text{flex\_spec})$ where $\text{grid\_spec} \in \text{Str}$, $\text{flex\_spec} \in \text{Str}$
    - $t_{\text{style}} = (\text{css\_rules})$ where $\text{css\_rules} \in \text{Str}$
    - $t_{\text{content}} = (\text{text\_content}, \text{media\_assets})$ where $\text{text\_content} \in \text{Str}$, $\text{media\_assets} \in \text{List}[\text{Media}]$
    - $t_{\text{interaction}} = (\text{event\_handlers})$ where $\text{event\_handlers} \in \text{List}[\text{Str}]$
2.  **Protocol**: Linear chain for static single-run sites; cyclic chain for dynamic interactive sites.
3.  **Room Instantiation**: The room tracks component tile sequences.
4.  **Agents**: Static site generators, React renderers, or PDF conversion tools.
5.  **Renderers**: Static HTML, React SPAs, PDF exporters, or screen readers.

---

## 5. Decoupling and Scalability
The original framework emphasizes that PLATO eliminates coupling between process definition, execution, and display. We formalize this claim:
> **Definition 5.1 (Decoupled PLATO Architecture)**. A PLATO system is decoupled if core components communicate *exclusively* via tile sequences in $\mathcal{S}_\mathcal{R}$:
> 1.  Agents read from and write to $\mathcal{S}_\mathcal{R}$,
> 2.  Renderers only read from $\mathcal{S}_\mathcal{R}$,
> 3.  Changes to agents or renderers do not require modifications to the room or its protocol.

> **Theorem 5.1 (Minimal Coupling)**. The PLATO architecture has exactly three independent components, with communication restricted to tile sequences. This is the minimal possible coupling for a general-purpose computational runtime.
>
> *Proof Sketch*. Any general-purpose runtime requires separation of process definition, execution, and display. Fewer than three components would couple two concerns, while more than three introduce unnecessary overhead. The PLATO architecture uses exactly three components with no direct coupling between agents and renderers.

For scalability, a system with $n$ agents and $m$ renderers requires only $n + m$ interfaces, as all components communicate via the standard tile protocol. This is asymptotically optimal, with linear scaling rather than quadratic coupling in monolithic architectures.

---

## 6. Formal Builder Workflow
For developers implementing custom PLATO rooms, the following minimal, complete workflow applies:
1.  **Classify the Process**: Determine if $\Pi$ is a single-run or cyclic loop process, and define its phase sequence.
2.  **Define Tile Schemas**: For each phase, specify a tile schema with valid data domains.
3.  **Specify the Protocol**: Construct the labeled transition graph for valid phase sequences.
4.  **Instantiate the Room**: Create the PLATO room with a unique ID, empty initial state, and idle lifecycle predicate.
5.  **Deploy Agents**: Implement one or more agents that generate valid tiles per the protocol.
6.  **Deploy Renderers**: Implement one or more renderers that consume the room's tile sequence to produce output.

---

## 7. Conclusion
This paper formalizes the PLATO room abstraction, proving that all computational processes—whether loops or single runs—are isomorphic to PLATO rooms. The core insight—that *the room is the loop*—is validated by the process-room isomorphism theorem, which exactly captures the structure of any computational workflow. The decoupled architecture eliminates brittle coupling between process definition, execution, and display, enabling modular, scalable development. The case studies demonstrate the broad applicability of the model, from agentic AI workflows to turn-based games to dynamic web applications.

> *"Everything is either a loop or a single run. Either can be embedded into PLATO as a room. The room IS the loop."*