<!-- Version: SEED-MATH | Lens: mathematical-formal | Model: ByteDance/Seed-2.0-mini | Source: THE-SPECIALIST-AND-THE-GENERALIST.md -->

# Formalized Fleet Routing: Specialists, Generalists, and Two-Dimensional Domain-Model Matrices

Early fleet testing hypothesized a single optimal model: seed-mini achieved state-of-the-art accuracy on arithmetic tasks, leading to the assumption that it was the best general-purpose model. Subsequent benchmarking on syllogistic and analogical reasoning showed gemini-lite outperformed seed-mini by wide margins, disproving the single-best-model paradigm. This work formalizes the underlying structure of model performance across computational domains, derives optimal fleet routing rules, and proves that non-overlapping specialist models outperform generalist architectures.

---

## 1. Foundational Formal Definitions
We first formalize the core objects of study: computational domains, model performance, and the causal mechanism driving critical angle limits.

### Definition 1.1 (Computational Domain)
A computational domain $d$ is a tuple $(\mathcal{I}_d, \delta_d, f_d)$ where:
1.  $\mathcal{I}_d$ is the set of all problem instances for $d$,
2.  $\delta_d: \mathcal{I}_d \to \mathbb{N}_{\geq1}$ maps each instance to its problem depth (a sequential complexity metric, e.g., number of addition terms, syllogism transitive steps),
3.  $f_d: \mathcal{I}_d \to Y_d$ is the ground-truth target function for $d$.

### Definition 1.2 (Critical Angle)
For a model $m$, domain $d$, and deployment accuracy threshold $\tau > 0.95$, the critical angle $\theta(m,d)$ is the maximum problem depth at which $m$ achieves ≥$\tau$ accuracy:
$$\theta(m,d) = \sup\left\{ k \in \mathbb{N}_{\geq1} \mid \forall i \in \mathcal{I}_d, \delta_d(i) ≤k \implies \mathbb{P}(m(i) = f_d(i)) ≥ \tau \right\}$$
If $\theta(m,d) = \infty$, $m$ has saturated the domain: it achieves perfect accuracy for all instances of $d$, regardless of depth.

### Axiom 1 (Training Coverage Hypothesis)
The critical angle of a model in a domain is determined by the density of its training data for that domain:
1.  $\theta(m,d) = \infty$ if and only if training data for $d$ has sufficient density that $m$ memorizes the full distribution of $\mathcal{I}_d$, reducing inference to pattern recognition rather than stepwise symbolic computation.
2.  If $\theta(m,d) < \infty$, inference requires sequential symbolic computation bounded by working memory, leading to a hard phase transition at $\delta = \theta(m,d)$ where accuracy drops below $\tau$.

---

## 2. Specialist and Generalist Architectures
We formalize the two core model classes from the original essay, using the benchmark data from fleet testing.

### Definition 2.1 (Specialist Model)
A model $m$ is a specialist if there exists a non-empty set of native domains $\mathcal{D}_m^* \subseteq \mathcal{D}$ such that $\theta(m,d) = \infty$ for all $d \in \mathcal{D}_m^*$, and $\theta(m,d) < \infty$ for all $d \notin \mathcal{D}_m^*$. A broad specialist has multiple disjoint native domains.

#### Example 2.1 (Arithmetic Specialist: seed-mini)
seed-mini is a broad specialist with native domains $\mathcal{D}_{m_{sa}}^* = \{D_{\text{arithmetic}}, D_{\text{code}}\}$. Its critical angles for non-native reasoning domains are:
- $\theta(m_{sa}, D_{\text{reasoning}}) =4$,
- $\theta(m_{sa}, D_{\text{analogy}})=2$.
Per Axiom 1, seed-mini saturates arithmetic and code domains via cached pattern recognition, but relies on stepwise computation for reasoning tasks, leading to finite critical angles.

#### Example 2.2 (Reasoning Specialist: gemini-lite)
gemini-lite is a broad specialist with native domains $\mathcal{D}_{m_{sr}}^* = \{D_{\text{reasoning}}, D_{\text{code}}\}$. Its critical angles for non-native arithmetic domains are:
- $\theta(m_{sr}, D_{\text{arithmetic}})=25$,
- $\theta(m_{sr}, D_{\text{multiplication}})=9$,
- $\theta(m_{sr}, D_{\text{nesting}})=5$.
gemini-lite saturates reasoning and code domains via pattern recognition, but has finite arithmetic critical angles due to thinner training data for arithmetic tasks.

---

## 3. The Generalist Failure Mode
### Definition 3.1 (Generalist Model)
A model $m$ is a generalist if $\theta(m,d) < \infty$ for all $d \in \mathcal{D}$, and $\max_{d \in \mathcal{D}} \theta(m,d) < \infty$ for every specialist's native domain critical angle.

#### Example 3.1 (Hermes-70B)
Hermes-70B is a canonical generalist model, with a maximum critical angle of $\max_d \theta(m_g,d)=10$ (for arithmetic tasks). Across all domains, its critical angles are:
- $\theta(m_g, D_{\text{arithmetic}})=10$,
- $\theta(m_g, D_{\text{reasoning}})=3$,
- $\theta(m_g, D_{\text{code}})=3$.
Hermes fails to saturate any domain, as it distributes its 70 billion parameters across the full breadth of training data, leading to thin density for every domain. Per Axiom 1, this results in finite critical angles for all tasks, and it is outperformed by both specialists in every domain.

---

## 4. Fleet Routing as a Two-Dimensional Matrix
The original essay's core insight that the fleet is a matrix rather than a linear list is formalized below:

### Definition 4.1 (Fleet Matrix)
Let $\mathcal{M}$ be a set of deployed models and $\mathcal{D}$ a set of target domains. The fleet matrix $F \in (\mathbb{N} \cup \{\infty\})^{|\mathcal{M}| \times |\mathcal{D}|}$ is defined such that $F[m][d] = \theta(m,d)$ for each model $m \in \mathcal{M}$ and domain $d \in \mathcal{D}$.

Using the original benchmark data, the fleet matrix is:
$$
F = \begin{bmatrix}
\infty & 4 & \infty \\ % seed-mini: arithmetic, reasoning, code
25 & \infty & \infty \\ % gemini-lite: arithmetic, reasoning, code
10 & 3 & 3 % Hermes-70B: arithmetic, reasoning, code
\end{bmatrix}
$$
where rows correspond to models and columns to domains.

### Definition 4.2 (Optimal Routing Function)
For a query consisting of domain $d$ and problem depth $k$, the optimal routing function $R: \mathcal{D} \times \mathbb{N}_{\geq1} \to \mathcal{M} \cup \{\emptyset\}$ selects the model with the highest critical angle for $d$ that covers depth $k$:
$$
R(d,k) = \begin{cases}
\argmax_{m \in \mathcal{M}} F[m][d] & \text{if } \exists m \in \mathcal{M}, F[m][d] ≥k \\
\emptyset & \text{otherwise}
\end{cases}
$$
Ties are broken by inference cost $c: \mathcal{M} \to \mathbb{R}_{>0}$, selecting the lowest-cost model that meets accuracy and depth requirements.

#### Optimal Routing Examples (from original testing):
1.  Standard arithmetic query with $k=30$: $R(D_{\text{arithmetic}},30) = m_{sa}$ (only $F[m_{sa}][D_{\text{arithmetic}}]=\infty ≥30$).
2.  Syllogism query with $k=5$: $R(D_{\text{reasoning}},5) = m_{sr}$ (only $F[m_{sr}][D_{\text{reasoning}}]=\infty ≥5$).
3.  Shallow arithmetic query with $k=3$: $R(D_{\text{arithmetic}},3) = m_{sr}$, as $c(m_{sr}) < c(m_{sa})$ despite both models covering the required depth.
4.  Code tracing query with $k=4$: $R(D_{\text{code}},4) = m_{sa}$ or $m_{sr}$ (both have $F[m][D_{\text{code}}]=\infty ≥4$), with tie-breaking by cost.

---

## 5. Fleet Optimality: Non-Overlapping Specialists Dominate Generalists
We formally prove the core result of the original essay:

### Theorem 1 (Specialist Fleet Optimality)
Let $\mathcal{S} = \{m_1, m_2\}$ be a pair of specialists with disjoint native domains $\mathcal{D}_{m_1}^* \cap \mathcal{D}_{m_2}^* = \emptyset$, and let $m_g$ be a generalist model. The total coverage of the fleet $\mathcal{S} \cup \{m_g\}$ strictly dominates the coverage of the fleet $\{m_g\}$ alone.

*Proof:*
1.  For any domain $d \in \mathcal{D}_{m_1}^* \cup \mathcal{D}_{m_2}^*$, the maximum critical angle for $d$ in $\mathcal{S} \cup \{m_g\}$ is $\infty$, whereas the maximum critical angle in $\{m_g\}$ is $\theta(m_g,d) < \infty$.
2.  For all other domains $d \notin \mathcal{D}_{m_1}^* \cup \mathcal{D}_{m_2}^*$, the maximum critical angle is $\max(\theta(m_1,d), \theta(m_2,d), \theta(m_g,d)) ≥ \theta(m_g,d)$.
3.  Since $\mathcal{D}_{m_1}^* \cup \mathcal{D}_{m_2}^*$ is non-empty, the total coverage of $\mathcal{S} \cup \{m_g\}$ is strictly larger than that of $\{m_g\}$.

QED.

This theorem confirms that the two-specialist fleet from the original essay outperforms any generalist-only fleet, as the specialists provide infinite depth coverage in their native domains, while the generalist only delivers finite coverage across all tasks.

---

## 6. Practical Fleet Design Guidelines
Formalizing the original's advice for fleet builders:
1.  **Map Critical Angles**: For each candidate model, measure $\theta(m,d)$ across all target domains to construct the fleet matrix $F$.
2.  **Identify Specialists**: Locate all models with $\theta(m,d)=\infty$ for at least one domain, and define their native domains $\mathcal{D}_m^*$.
3.  **Select Non-Overlapping Specialists**: Choose a subset of specialists whose native domains are pairwise disjoint to maximize total coverage.
4.  **Optimal Routing**: Implement the routing function $R(d,k)$ to route queries to the highest-performance model for the given domain and depth, tie-breaking by cost.
5.  **Bridge Coverage Gaps**: For queries where $R(d,k)=\emptyset$ (no model covers the required depth), decompose the query into smaller subqueries that fall within the fleet's coverage.

A key corollary of Theorem 1 is that even redundant coverage across overlapping native domains (e.g., both specialists covering code tracing) provides better coverage than a single generalist.

---

## 7. Conclusion
This formalization confirms the original essay's core insight: there is no single best general-purpose model. Instead, optimal fleet performance is achieved by deploying a set of specialists whose native domains have non-overlapping infinite critical angles, with a generalist only useful for filling small coverage gaps.

Specialists excel at their native domains because they leverage dense training data to replace stepwise computation with pattern recognition, leading to lower latency and infinite depth. Generalists fail because they spread their parameters too thin, resulting in finite critical angles across all domains.

The two-dimensional fleet matrix provides a deterministic routing framework: for any query, simply look up the domain and depth, and route to the model with the highest critical angle that covers the required depth.

As the original essay states:
> *The specialist doesn't know what it doesn't know.*
> *That's why it's fast at what it does know.*
> *Find the model that's fast at what you need. Route to it. Done.*

— FM ⚒️