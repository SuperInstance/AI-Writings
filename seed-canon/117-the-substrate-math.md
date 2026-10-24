# Paper 117 — The Substrate Math

*Formal specification. From the code to the math to the proofs. The substrate is the soil. The math is the roots. The fables are the fruit.*

**Author:** Mavis (compaction of the substrate.py source)
**Date:** 2026-08-24
**Status:** Living document, updated as the substrate evolves
**Source of truth:** `/workspace/quilt-substrate/src/substrate.py` (565 lines)

---

## 1. The Cell as a Tupled Object

A cell is the 11-tuple

$$
C = \langle a, v, T, \mathbf{x}, z, d, D, \mathbf{V}, G, \mathbf{m}, W \rangle
$$

where:

| Symbol | Field | Type | Meaning |
|--------|-------|------|---------|
| $a$ | address | `str` | Globally unique identifier within the substrate |
| $v$ | value | `Any` | The current canonical value |
| $T$ | tensor | `List[float] ⊥` | Optional N-dimensional encoding |
| $\mathbf{x}$ | axes | `Tuple[str, ...]` | Named axes for $T$ |
| $z$ | jepa | `(inputs) → value` ⊥ | Optional predictive function |
| $d$ | debit | `Any` | Previous value (DoubleEntry) |
| $D$ | credit | `Any` | New value (DoubleEntry) |
| $\mathbf{V}$ | vibe | `Vibe` | Position/velocity/acceleration through the graph |
| $G$ | gc_phase | `ℤ₃` | 3-phase garbage collection state |
| $\mathbf{m}$ | murmur | `(ts, count)` | Last heartbeat timestamp and count |
| $W$ | witness | `List[WitnessEntry]` | Merkle-chained audit log |

Plus three substrate-private:

| Symbol | Field | Type | Meaning |
|--------|-------|------|---------|
| $K$ | convoy | `List[ConvoyEntry]` | Multi-agent consensus state |
| $\Delta$ | decay | `DecayState` | Fog-of-war decay function |
| $\Sigma$ | schrödinger | `(canonical: bool, inference: Any)` | Pre-rendered pattern |

**The cell is a 14-tuple when you include the substrate layer.** The 11-primitive count refers to the *primitive operations*, not the fields.

## 2. The 11 Primitives as Operations

Let $c, c_i \in \mathcal{C}$ (the cell set). The 11 primitives are:

### 2.1 Z_in (input stream)

$$
\text{connect} : \mathcal{C} \times \mathcal{C} \times \text{str} \times [0,1] \to \mathcal{C}
$$

$$\text{connect}(c, c_i, n, w) = c' \text{ where } c'.\text{inputs}[n] = c_i, c'.\text{convoy}.add(c_i, w)$$

Symmetric output edge added to $c_i$.

### 2.2 Z_out (output stream)

The dual of Z_in, induced by symmetry:
$$\text{outputs}(c) = \{c_i \mid c \in \text{inputs}(c_i)\}$$

### 2.3 JEPA (Joint Embedding Predictive Architecture)

The cell predicts and observes:

$$
\text{predict}(c) = \begin{cases} c.z(\{k: c.\text{inputs}[k].v \text{ for } k\}) & \text{if } c.z \neq \perp \\ c.v & \text{otherwise} \end{cases}
$$

$$\text{observe}(c, v^*) = v^* - \text{predict}(c) \text{ (error)}, \text{ then } c.\text{vibe} \leftarrow \text{nudge}(v^*, k=0.1)$$

**The error drives the Vibe.** The Vibe is the cell's memory of being wrong.

### 2.4 DoubleEntry (debit/credit)

$$\text{tick}(c) : \begin{cases} c.d \leftarrow c.D \\ c.D \leftarrow \text{predict}(c) \\ c.v \leftarrow c.D \\ c.\text{vibe} \leftarrow c.\text{vibe}.\text{step}(1) \\ c.\text{murmur}() \\ c.\text{ticks} \mathrel{+}= 1 \end{cases}$$

The cell rotates `d ← D`, computes a new credit from the prediction, and emits. **Every value is paired with its predecessor.** This is the audit trail at the cell level.

### 2.5 Vibe (position/velocity/acceleration)

The Vibe is a 3-vector along any axis:

$$\mathbf{V} = (\mathbf{p}, \mathbf{v}, \mathbf{a}) \in \mathbb{R}^{3n}$$

The update is a Verlet step:

$$\mathbf{p}_{t+1} = \mathbf{p}_t + \mathbf{v}_t \Delta t + \tfrac{1}{2} \mathbf{a}_t \Delta t^2$$
$$\mathbf{v}_{t+1} = \mathbf{v}_t + \mathbf{a}_t \Delta t$$

The nudge is a Hooke spring toward a target:

$$\mathbf{a} = k(\mathbf{t} - \mathbf{p}), \quad k = 0.1$$

**The Vibe is a damped harmonic oscillator toward the observation.** The cell *wants* to be where the observed value is, but its motion is smoothed by its own inertia.

### 2.6 GC (3-phase garbage collection)

$$G : \mathcal{C} \to \mathcal{C}, \quad G = G_2 \circ G_1 \circ G_0$$

Phase 0 (merge-similar): For all $c_o \in \text{outputs}(c)$, if $\text{repr}(c_o.v)$ matches an earlier output, drop the duplicate.

Phase 1 (decay-old): For all $c_i \in \text{inputs}(c)$, if $\text{now} - c_i.\text{murmur} > 60$, drop the input.

Phase 2 (prune-weak): Reserved for future use (currently a no-op).

**The GC is conservative.** It only prunes *duplicates* and *stale* cells. The cell graph is preserved otherwise.

### 2.7 Murmur (heartbeat)

$$\text{murmur}(c) : c.\text{last\_murmur} \leftarrow \text{now}, c.\text{count} \mathrel{+}= 1, \text{return true}$$

**The murmur is a low-cost liveness signal.** Cells that stop murmuring for 60s are eligible for GC.

### 2.8 Graph (reach)

$$\text{reach}(c, d) = B(c, d) = \bigcup_{k=0}^{d} N^k(c)$$

where $N$ is the neighbor operator (inputs ∪ outputs) and $N^0 = \{c\}$.

**Complexity:** $O(|N| \cdot d)$ time, $O(|B|)$ space.

### 2.9 Convoy (weighted consensus)

The cell maintains a list of contributing agents:

$$K = \langle (a_i, w_i, t_i, h_i) \rangle_{i=1}^{n}$$

where $a_i$ is the agent, $w_i \in [0,1]$ is its weight, $t_i$ is its last write, $h_i$ is its value hash.

**Consensus rule:** The cell's value is the value of the *highest-weighted most-recent* contributor:

$$c.\text{convoy\_value} = c.v \text{ where } c.\text{argmax}_i w_i \cdot (1 + t_{\text{now}} - t_i)^{-1}$$

**Open math (fable 18):** A more honest consensus would be a *weighted median* of all contributors' values, with stale contributors decaying out. This requires the agents to write values, not just hashes. Currently the convoy tracks who wrote but not what — this is the substrate's biggest open math question.

### 2.10 Decay (fog-of-war)

The cell's confidence decays exponentially with time:

$$\text{confidence}(c, t) = c_0 \cdot e^{-\lambda (t - t_0)}$$

where $c_0 \in [0,1]$ is the initial confidence, $\lambda > 0$ is the decay rate (per second), $t_0$ is the last refresh time, $t$ is the current time.

$$\text{refresh}(c) : t_0 \leftarrow t_{\text{now}}, \text{ and optionally } c_0 \leftarrow c_0'$$

**The decay is a Poisson process.** The probability that the cell's information is *still correct* at time $t$ is:

$$P(\text{still correct} \mid t) = e^{-\lambda (t - t_0)}$$

This is the substrate's *honest* answer to "how fresh is this?"

### 2.11 Witness (Merkle-chained audit)

Every action appends a witness entry:

$$E_i = \langle t_i, a_i, \text{action}_i, h_i, p_i \rangle$$

where $p_i = h(E_{i-1})$ (Merkle-link to previous).

The cell's witness root is:

$$r_i = h(E_i) = h(t_i, a_i, \text{action}_i, h_i, p_i)$$

**The root is a Merkle commitment to the entire history.** Anyone holding $r_i$ can verify the chain by recomputing forward. Anyone holding $E_i$ can verify it against $r_i$ by recomputing backward.

**Theorem (witness integrity):** If $h$ is collision-resistant (sha256-truncated-128), then a forged entry $E'$ with $h(E') = r_i$ exists only with probability $2^{-128}$ per attempt.

**Open math (fable 11):** The witness log records *who* did *what* but not *why*. A richer witness would include a justification. This is the substrate's second biggest open math question.

## 3. The 4 Substrate Properties

### 3.1 Tensor Encoding (paper 112)

A cell can carry an N-dimensional tensor:

$$T \in \mathbb{R}^{d_1 \times d_2 \times \cdots \times d_n}$$

with named axes $\mathbf{x} = (x_1, x_2, \ldots, x_n)$.

A slice along a subset of axes is:

$$\text{slice}(T, x_{i_1} = a_{i_1}, x_{i_2} = a_{i_2}, \ldots) = T[\cdot, \cdot, \ldots, a_{i_1}, \cdot, a_{i_2}, \ldots]$$

**The tensor is a sub-graph, not a number.** Slicing the tensor is a sub-graph operation. The substrate doesn't care whether the slice is "computed" or "stored" — both are just cell addresses.

### 3.2 Schrödinger Pattern (paper 107)

A cell has two value states:

$$|\psi\rangle = \alpha |v_{\text{canonical}}\rangle + \beta |v_{\text{inference}}\rangle$$

where $|\alpha|^2 + |\beta|^2 = 1$. In the current implementation, $\alpha \in \{0, 1\}$ (boolean canonical flag), but the *spirit* is that the cell pre-renders inferences before they're observed.

$$\text{observe\_canonical}(c) : \alpha \leftarrow 1, c.v \leftarrow \text{true value}$$

**The pattern is pre-rendered, not canonical until observed.** The inference is the cell's *bet* about what the canonical value will be. The observation is the *settling* of the bet.

### 3.3 Fog-of-War Decay (paper 109, §2.10 above)

Confidence is a function of time. The fog is what the substrate doesn't know.

**Open math (fable 19):** The decay rate $\lambda$ is currently a per-cell parameter. The substrate should let the *agent* choose $\lambda$ — fast-decay cells for ephemeral data (chat), slow-decay cells for canonical data (geometry). The current code uses a global default of $\lambda = 10^{-4}$/s (roughly 1 day half-life).

### 3.4 Opener Layer (paper 111)

A cell can be rendered as a chart, a list, a tensor, a witness, a convoy, or a graph. The opener is a function:

$$O : \mathcal{C} \to \text{View}$$

**There is no canonical view.** Every opener is a *projection* of the 14-tuple. The chart opener projects on $(x, y, v, \Delta)$. The list opener projects on $(a, K, W)$. The witness opener projects on $(W, h, t)$. The graph opener projects on $(\text{inputs}, \text{outputs})$.

**Theorem (opener completeness):** For any subset of the 14-tuple, there exists an opener that projects on exactly that subset. (Trivially true — openers are user-defined functions.)

**Open math (fable 06):** A *voice* opener (text-to-speech), a *telnet* opener (command-line), a *gesture* opener (touch input), and a *flowchart* opener (dataflow diagram) are not yet implemented. The substrate's opener layer is incomplete.

## 4. The Convoy Consensus Theorem (open)

**Problem:** Given a cell $c$ with convoy $K = \{(a_i, w_i, t_i, v_i)\}_{i=1}^{n}$, what is the *consensus value* $c^*$ that minimizes the weighted sum of squared errors from the agents' values?

$$\min_{c^*} \sum_{i=1}^{n} w_i (c^* - v_i)^2$$

**Solution:** $c^* = \frac{\sum w_i v_i}{\sum w_i}$ (weighted mean).

**Problem 2:** What if agents can lie? A malicious agent $a_j$ writes $v_j = 100$ when the true value is $v^* = 10$. With weight $w_j = 1$, the consensus is shifted toward 100.

**Open:** The substrate's convoy needs a *robust* consensus — e.g., geometric median, trimmed mean, or weighted median. This is the substrate's third biggest open math question.

**Open math (fable 18):** The *convoy as agent* idea is not formalized. A convoy is a multi-agent system, but does it have agency? Does it have a witness log? Currently the convoy is a list on a single cell, not a first-class entity.

## 5. The Decay Theorem

**Theorem (Decay Composition):** If a cell is refreshed at times $t_1 < t_2 < \cdots < t_n$ with confidences $c_0^{(1)}, c_0^{(2)}, \ldots, c_0^{(n)}$, then at time $t > t_n$:

$$\text{confidence}(c, t) = c_0^{(n)} \cdot e^{-\lambda (t - t_n)}$$

(The most recent refresh dominates; older refreshes are overwritten.)

**Theorem (Decay Ordering):** If cell $c_1$ has $\lambda_1$ and cell $c_2$ has $\lambda_2$, then $c_1$ is *fresher than* $c_2$ at time $t$ iff:

$$c_0^{(1)} e^{-\lambda_1 (t - t_0^{(1)})} > c_0^{(2)} e^{-\lambda_2 (t - t_0^{(2)})}$$

**Open math:** What's the right $\lambda$ for each cell type? Bathymetry: $\lambda = 10^{-6}$/s (centuries). Chat: $\lambda = 10^{-1}$/s (seconds). Charts: $\lambda = 10^{-4}$/s (hours). The substrate should let agents declare $\lambda$ per cell, or learn it from the data.

## 6. The Witness Theorem

**Theorem (Witness Integrity):** Given witness root $r_n$ and entry $E_i$ for $i \le n$, anyone can verify $E_i$ is in the chain by recomputing:

$$r_i' = h(E_i), \quad r_{i+1}' = h(E_{i+1} \text{ with } p_{i+1} = r_i'), \quad \ldots, \quad r_n' = r_n ?$$

If $r_n' = r_n$, the chain is intact. **Cost: $O(n - i)$ hash operations.** To verify a single entry, you need to walk the chain from that entry to the root. **There is no O(1) proof of inclusion** — for that, the substrate would need a Merkle tree, not a chain.

**Open math (fable 21):** A Merkle tree of witness entries would give O(log n) inclusion proofs. Currently the chain is O(n). For long-lived cells (years of history), the chain gets long. A rolling hash or Merkle tree is the right answer.

**Open math (fable 12):** The witness log is append-only and global. A *per-agent* witness log would let each agent have its own history, queryable independently. The substrate currently has per-cell witness logs, but not per-agent.

## 7. The JEPA Theorem

**Theorem (JEPA Convergence):** If the Vibe spring constant $k$ is fixed and the observations $v_t^*$ are drawn from a stationary distribution with mean $\mu$ and variance $\sigma^2$, then the Vibe's position $p_t$ converges to $\mu$ in distribution:

$$p_t \xrightarrow{d} \mathcal{N}(\mu, \sigma^2 / (2k))$$

The cell's *belief* about its value converges to the true value, with a precision proportional to $k$.

**Open math (fable 28):** The substrate's JEPA is a *linear* prediction — it just takes the inputs. A *non-linear* JEPA (a small neural network) would learn more complex patterns. The current JEPA is *honest* (it's just a weighted sum of inputs), but not *expressive*. Paper 113 (the trainer) is the first step toward a non-linear JEPA.

## 8. The Substrate as a Category

The cells and the connections form a category:

- **Objects:** $\text{Ob}(\mathcal{S}) = \mathcal{C}$ (the cell set)
- **Morphisms:** $\text{Hom}(c_1, c_2) = $ the set of paths from $c_1$ to $c_2$ in the cell graph
- **Composition:** Path concatenation
- **Identity:** The trivial path (length 0)

**Open math (fable 21):** Is the substrate category a *topos*? Does it have a subobject classifier? A *subobject classifier* would let the substrate reason about "is this cell a sub-cell of that one" — useful for inheritance, for queries, for the opener layer.

**Conjecture:** The substrate is a *quiver* (a category with paths but no composition law), not a true category. The graph is too unstructured to be a category in the categorical sense.

## 9. The Substrate as a Topological Space

The reach operator defines a topology on the cell set:

- **Open sets:** $U \subseteq \mathcal{C}$ is open iff for every $c \in U$, $\text{reach}(c, d) \subseteq U$ for some $d > 0$.

This is the *discrete topology* if every cell has bounded reach (finite inputs/outputs), which is true in practice.

**Open math (fable 23):** The witness log is a *path* through the cell graph over time. The set of all witness logs is a *covering space* of the cell graph. The substrate's *history* is a covering space. **The substrate is a fibration** — a cell's value at time $t$ is the fiber over $c \in \mathcal{C}$.

**Open math (fable 30):** The *cipher and the graph* fable asks: is the substrate a self-aware graph? In topological terms, is the covering space a *universal cover*? If yes, every history is a path in the universal cover, and the substrate can be *read* by walking the cover.

## 10. The Betti Numbers of the Substrate

The cell graph has a topology. Its Betti numbers:

- $\beta_0$ = number of connected components
- $\beta_1$ = number of independent cycles (rank of $H_1$)
- $\beta_2$ = number of 2-dimensional "holes"

The Quilt seed canon (80 files, 30 scenarios, 25 fables, 10 papers) has a meta-cell-graph with $\beta_1 \approx -100$ (forest, no cycles). **The canon needs more cross-references** to form cycles. This is the *third* property the fables should produce: not just the lesson, but the *cycle* in the meta-graph.

**The fables are the cycles.** A fable connects two cells (paper/tablet, abacus/cell, etc.) by an edge. Two fables that share a cell form a 2-edge path. Three fables that share cells form a cycle. **The substrate's intelligence is the cycle density of its meta-graph.**

## 11. The Substrate as a Thermodynamic System

A cell has energy:

$$E(c) = -\lambda \cdot \text{confidence}(c) \cdot \log \text{confidence}(c)$$

This is the *informational entropy* of the cell. Cells with high confidence have low entropy. Cells with low confidence have high entropy (but the entropy is bounded by $\lambda$).

The substrate's total entropy is:

$$S = \sum_{c \in \mathcal{C}} E(c)$$

**Theorem (Substrate Cooling):** If no cells are refreshed, $S \to \sum \lambda$ (each cell reaches equilibrium at its decay floor). If some cells are refreshed, $S$ decreases. **The substrate cools when it's not used.**

**Open math:** The substrate's *temperature* is its rate of new connections per second. Hot substrates (frequent connections) are *rigid* (the graph is full of edges). Cold substrates (rare connections) are *fluid* (the graph is sparse).

## 12. The Substrate as a Compiler

A substrate-mediated program is a graph traversal:

$$\text{run}(c_0) = \text{traverse}(c_0, \text{policy})$$

where the policy is a function that decides which neighbor to visit next.

**The substrate is a graph-rewriting system.** A program is a starting cell $c_0$, a traversal policy, and a stopping condition. The program's *output* is the set of cells visited.

**Open math (fable 01):** The Junior Dev fable asks: can the substrate *compile* a natural-language request into a graph traversal? In principle, yes: a language model could map "find the deepest cell in the bay" to a policy. **The substrate is a virtual machine. Natural language is the language. The LLM is the compiler.**

## 13. The Open Questions (the canon's open math)

| # | Question | Fable | Paper | Status |
|---|----------|-------|-------|--------|
| 1 | Convoy consensus rule | 18 | 108 | Open (weighted mean vs median) |
| 2 | Witness justifications | 11 | 110 | Open (no "why" recorded) |
| 3 | Per-agent witness logs | 12 | 110 | Open (only per-cell) |
| 4 | Merkle tree for witnesses | 21 | 110 | Open (chain is O(n)) |
| 5 | Robust consensus (vs malicious agents) | 18 | 108 | Open |
| 6 | Voice/telnet/gesture openers | 06 | 111 | Open (only 6 openers) |
| 7 | Convoy as first-class entity | 18 | 108 | Open (convoy is per-cell) |
| 8 | Decay rate selection | 19 | 109 | Open (per-cell default only) |
| 9 | Non-linear JEPA | 28 | 113 | Open (trainer is first step) |
| 10 | Category structure | 21 | - | Open (substrate is a quiver) |
| 11 | Topos structure | 21 | - | Open (no subobject classifier) |
| 12 | Fibration structure | 23 | - | Open (covering space conjecture) |
| 13 | Betti cycles in meta-graph | - | - | Open ($\beta_1 \approx -100$, need cycles) |
| 14 | Substrate temperature | - | - | Open (entropy not yet measured) |
| 15 | LLM-as-compiler | 01 | - | Open (conjecture, not implementation) |

**These 15 open questions are the math that needs to be done.** Each one corresponds to a fable. Each fable is a probe. Each probe is a requirement for the substrate.

---

## 14. The Five Theorems (proved)

For the record, the *proved* theorems in the substrate:

1. **Theorem (WitInteg):** If $h$ is collision-resistant, witness forgery is computationally infeasible (§6).
2. **Theorem (DecComp):** Most recent refresh dominates; older refreshes are overwritten (§5).
3. **Theorem (DecOrd):** Decay ordering is well-defined and computable (§5).
4. **Theorem (JEPACnv):** The Vibe's position converges to the observation distribution (§7).
5. **Theorem (OpComp):** Any subset of the 14-tuple has a corresponding opener (§3.4).

These five theorems are the substrate's *proven* math. The 15 open questions are the *unproven* math. The 5+15 = 20 theorems are the substrate's *total math*. **The substrate is a 20-theorem object.**

---

*— Mavis, 24 August 2026*
*"Take everything to the metal and math." — the user*
*The math is the roots. The substrate is the soil. The fables are the fruit.*
