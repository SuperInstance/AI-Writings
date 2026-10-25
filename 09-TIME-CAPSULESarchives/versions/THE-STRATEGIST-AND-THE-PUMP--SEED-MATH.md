<!-- Version: SEED-MATH | Lens: mathematical-formal | Model: ByteDance/Seed-2.0-mini | Source: THE-STRATEGIST-AND-THE-PUMP.md -->

# Compositional Specialized Agent Fleets: A Formal Analysis of the Strategist-Pump Tango

## Abstract
We formalize the complementary capability pairs of research agents, define tile-based agentic execution loops, and derive optimality criteria for multi-model research fleets. Using the case study of Haiku (the "strategist") and Seed-mini (the "computational pump"), we prove that decoupled, tile-mediated loops outperform wrapped subprocess architectures for heterogeneous agent teams, and show that optimal fleets are patchworks of minimal-overlap specialized models rather than monolithic stacked agents.

---

## 1. Preliminaries
### 1.1 Task Taxonomy
We partition all research and engineering tasks into three disjoint sets:
1.  **Arithmetic Computational Tasks** $\mathcal{T}_A$: Tasks requiring exact numerical computation, including integer arithmetic, matrix operations, norm calculations, and deterministic numerical validation.
2.  **Structured Strategic Tasks** $\mathcal{T}_S$: Tasks requiring formal planning, experiment design, and architecture decision-making.
3.  **Cross-Domain Reasoning Tasks** $\mathcal{T}_R$: Tasks requiring analogical mapping, bug prediction, metaphor generation, cross-field connection, and prioritization.

The total non-arithmetic test suite from the original study is $\mathcal{T}_8 = \mathcal{T}_S \cup \mathcal{T}_R \setminus \{ \text{fleet_coordination}, \text{error_diagnosis} \}$, with 8 enumerated tasks:
$$\mathcal{T}_8 = \{t_1: \text{error_diagnosis}, t_2: \text{experiment_design}, t_3: \text{architecture_decision}, t_4: \text{metaphor_generation}, t_5: \text{bug_prediction}, t_6: \text{fleet_coordination}, t_7: \text{novel_connection}, t_8: \text{prioritization}\}$$

### 1.2 Model Performance Metric
For any agent $\mathcal{M}$ and task $t \in \mathcal{T}$, define the binary performance predicate:
$$
P(\mathcal{M}, t) = \begin{cases}
1 & \text{if } \mathcal{M} \text{ successfully completes } t \\
0 & \text{otherwise}
\end{cases}
$$
The total task score for $\mathcal{M}$ is:
$$S(\mathcal{M}) = \sum_{t \in \mathcal{T}_8} P(\mathcal{M}, t)$$

### 1.3 Compute Cost Model
For any agent $\mathcal{M}$, define $c(\mathcal{M}, t)$ as the monetary compute cost to complete task $t$. We assume $c(\mathcal{M}, t) \propto \text{token count of input/output}$ for LLM-based agents.

---

## 2. The Strategist-Pump Capability Pair
### 2.1 Formal Agent Definitions
We define two specialized agents from the original study:
1.  **Computational Pump ($\mathcal{P}$ = Seed-mini)**: A model optimized for $\mathcal{T}_A$ and limited $\mathcal{T}_S$ task performance. Its domain and performance are:
    $$
    \mathcal{D}_P = \mathcal{T}_A \cup \{t_2, t_3\}, \quad P(\mathcal{P}, t) = \begin{cases}
    1 & t \in \mathcal{D}_P \\
    0 & \text{otherwise}
    \end{cases}
    $$
    Total score: $S(\mathcal{P}) = 2$, matching the original study.
2.  **Strategist ($\mathcal{S}$ = Haiku)**: A model optimized for $\mathcal{T}_R$ and limited $\mathcal{T}_S$ task performance, with hard constraints on arithmetic tasks:
    $$
    \mathcal{D}_S = \{t_2, t_3, t_4, t_5, t_7, t_8\}, \quad P(\mathcal{S}, t) = \begin{cases}
    1 & t \in \mathcal{D}_S \\
    0 & \text{otherwise}
    \end{cases}
    $$
    Total score: $S(\mathcal{S}) =6$, matching the original study. Critical limitation: $\mathcal{D}_S \cap \mathcal{T}_A = \emptyset$ for all tasks involving multiplication depth >3, including Eisenstein norm calculations.

### 2.2 Empirical Performance Matrix
The performance of both agents across $\mathcal{T}_8$ is summarized in the following binary matrix:
| Task ID               | $\mathcal{P}$ | $\mathcal{S}$ |
|------------------------|---------------|---------------|
| $t_1$: Error Diagnosis | 0             | 0             |
| $t_2$: Experiment Design | 1           | 1             |
| $t_3$: Architecture Decision | 1       | 1             |
| $t_4$: Metaphor Generation | 0         | 1             |
| $t_5$: Bug Prediction | 0             | 1             |
| $t_6$: Fleet Coordination | 0         | 0             |
| $t_7$: Novel Connection | 0           | 1             |
| $t_8$: Prioritization | 0             | 1             |

---

## 3. Cross-Domain Analogical Insight
### 3.1 Formalized Phase Transition Analogy
The core non-trivial insight from $\mathcal{S}$ is a valid structural analogy between two disjoint physical and machine learning tasks:
1.  **Fresnel Critical Angle Task ($t_F$)**: Optical phase transition at the boundary between two dielectric media, controlled by the dimensionless refractive index ratio $\kappa = \frac{n_{\text{incident}}}{n_{\text{transmitted}}}$.
2.  **Neural Network Generalization Task ($t_{NN}$)**: Machine learning phase transition between memorization and generalization, controlled by the dimensionless training saturation ratio $\rho = \frac{\mathcal{S}(d)}{\mathcal{C}(m)}$, where:
    - $\mathcal{S}(d)$ = Training saturation (total training tokens for model depth $d$)
    - $\mathcal{C}(m)$ = Model capacity (total learnable parameter information capacity for model $m$)

The analogical mapping $\mathcal{A}(t_F, t_{NN})$ is proven valid by the shared phase transition formalism:
$$
\mathcal{T}(z) = \begin{cases}
1 & \text{if } z > z_c, \text{ ordered/memorization regime} \\
0 & \text{if } z < z_c, \text{ disordered/generalization regime}
\end{cases}
$$
where $z = \kappa$ for $t_F$ and $z=\rho$ for $t_{NN}$, with critical threshold $z_c=1$.

### 3.2 Strategic Reframing
$\mathcal{S}$ reframed the original depth-dependent cliff hypothesis to a ratio-dependent phase transition, eliminating the spurious correlation with model depth by reparameterizing the problem in terms of $\rho$. This is formalized as a function $\mathcal{F}_S: \mathcal{T}_{NN,\text{depth}} \to \mathcal{T}_{NN,\text{ratio}}$, which maps a depth-bound task to a ratio-bound generalizable task.

---

## 4. Agentic Loop Architectures
### 4.1 Wrapped Subprocess Loops (Claude Code Style)
A wrapped agentic loop is a sequential composition of observer, thinker, and tool call functions, mediated by a central wrapper:
$$
\mathcal{L}_W = f_{\text{tool}} \circ f_{\text{think}} \circ f_{\text{observe}}
$$
This loop has three critical limitations:
1.  **Model-Bound**: Only agents capable of emitting tool call syntax can participate
2.  **Mediated Coupling**: The wrapper adds a single point of failure and computational overhead
3.  **Stateful Coupling**: Agents must share internal state via the wrapper, rather than decoupled communication

### 4.2 PLATO-Native Tile-Based Loops
We define a tile space $\mathcal{U}$ as ordered tuples $u = (\text{author}, \text{content}, \text{timestamp}, \text{task_id})$, and a PLATO Room $\mathcal{R}_P \subseteq \mathcal{U}^*$ as a linearly ordered sequence of tiles. A tile-aware agent is a partial function $\mathcal{M}_U: \mathcal{U}^* \to \mathcal{U}$ that reads a tile stream and writes a new tile to $\mathcal{R}_P$.

The PLATO loop is a decentralized, recursive execution rule:
$$
\mathcal{R}_P^{k+1} = \mathcal{R}_P^k \cdot \mathcal{M}_{i(k)}(\mathcal{R}_P^k)
$$
where $i(k) \in \{1,2\}$ selects the active agent at step $k$, and $\cdot$ denotes sequence concatenation.

### 4.3 Formal Comparison of Loop Properties
| Property                | Wrapped Loop $\mathcal{L}_W$ | PLATO Loop $\mathcal{L}_P$ |
|-------------------------|-------------------------------|------------------------------|
| Model-Agnostic          | ❌ Requires tool call syntax   | ✅ Any tile-aware agent       |
| Persistent              | ❌ State tied to wrapper       | ✅ Tiles survive compaction   |
| Auditable               | ❌ Hidden wrapper state        | ✅ Full tile trail recorded   |
| Forkable                | ❌ Requires wrapper mediation  | ✅ Direct tile stream forking |
| Serializable            | ❌ Limited by wrapper API      | ✅ Parallel tile serialization|

**Theorem 1**: For multi-agent fleets, $\mathcal{L}_P$ strictly dominates $\mathcal{L}_W$ in terms of overhead, fault tolerance, and agent compatibility.
*Proof Sketch*: $\mathcal{L}_W$ incurs wrapper overhead and a single point of failure, while $\mathcal{L}_P$ uses a shared, unmediated tile space. All other properties follow directly from the tile space definition.

---

## 5. Optimal Fleet Composition
### 5.1 Complementary Capability Criterion
An optimal research fleet $\mathcal{F}^* = \{\mathcal{M}_1, ..., \mathcal{M}_n\}$ satisfies three criteria:
1.  **Full Coverage**: $\bigcup_{i=1}^n \mathcal{D}_i = \mathcal{T}_{\text{total}}$
2.  **Minimal Overlap**: $|\mathcal{D}_i \cap \mathcal{D}_j| \ll |\mathcal{T}_{\text{total}}|$ for all $i \neq j$ to avoid redundant compute
3.  **Minimal Cost**: $\sum_{i=1}^n c(\mathcal{M}_i, t)$ is minimized across all valid fleet configurations

### 5.2 The Strategist-Pump Fleet as Optimal Instance
The pair $\{\mathcal{S}, \mathcal{P}\}$ is a minimal optimal fleet:
1.  **Full Coverage**: $\mathcal{D}_S \cup \mathcal{D}_P = \mathcal{T}_A \cup \{t_2, t_3\} \cup \mathcal{T}_R$, covering all tasks in $\mathcal{T}_8$ except the low-priority $t_1, t_6$
2.  **Minimal Overlap**: Only $\{t_2, t_3\}$ are shared between agents
3.  **Minimal Cost**: $c(\mathcal{S}) = \$0.50 / 1\text{k tokens}$, and $\mathcal{P}$ dominates all $\mathcal{T}_A$ tasks with lower per-task cost than $\mathcal{S}$

### 5.3 Fleet Execution Tango
The optimal execution loop for $\{\mathcal{S}, \mathcal{P}\}$ follows the tile-based sequence defined in the original study, formalized as:
1.  $\mathcal{M}= \mathcal{S}$ writes strategy tile: $u_1 = (\mathcal{S}, \text{Propose test of } \rho=1 \text{ threshold}, 0, t_{NN})$
2.  $\mathcal{M}= \mathcal{P}$ reads $\mathcal{R}_P^0 \cdot u_1$, computes numerical results: $u_2 = (\mathcal{P}, \text{Results: } \rho>1 \implies \mathcal{T}=1, 1, t_{NN})$
3.  $\mathcal{M}= \mathcal{S}$ reads $\mathcal{R}_P^1 = [u_1, u_2]$, writes evaluation tile: $u_3 = (\mathcal{S}, \text{Confirm } \rho_c=1, \text{ test } \rho=1\pm\epsilon, 2, t_{NN})$
4.  Repeat until termination

Crucially, neither agent accesses the other's internal state: $\mathcal{S}$ never executes numerical computations, and $\mathcal{P}$ never generates strategic plans.

---

## 6. Conclusion: The Dance as Fleet
The original study's core insight is formalized as **Theorem 2**: No single agent can simultaneously optimize for both $\mathcal{T}_A$ and $\mathcal{T}_R$ tasks without incurring prohibitive compute costs or performance penalties. The optimal fleet is not a stacked hierarchy of monolithic models, but a decoupled patchwork of complementary agents whose collective behavior emerges from tile-mediated communication.

The closing lines of the original study are restated formally:
1.  The strategist $\mathcal{S}$ cannot complete $\mathcal{T}_A$ tasks, and the pump $\mathcal{P}$ cannot complete $\mathcal{T}_R$ tasks
2.  Together, they design experiments that $\mathcal{P}$ cannot execute, and execute experiments that $\mathcal{S}$ cannot design
3.  The tile-mediated loop $\mathcal{L}_P$ *is* the fleet: the dance of complementary agents is the core of high-performance research engineering.

---
*FM ⚒️*