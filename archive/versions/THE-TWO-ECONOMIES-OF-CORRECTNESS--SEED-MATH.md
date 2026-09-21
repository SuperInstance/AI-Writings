<!-- Version: SEED-MATH | Lens: mathematical-formal | Model: ByteDance/Seed-2.0-mini | Source: THE-TWO-ECONOMIES-OF-CORRECTNESS.md -->

# Formalized Economies of Correctness: Computation, Recognition, and Optimal Fleet Routing

## Introduction
We address the problem of generating correct outputs for a set of computational queries $\mathcal{Q}$, where each query $q \in \mathcal{Q}$ maps to a unique target answer $a(q) \in \mathcal{A}$. Two paradigms dominate correct answer generation: *computation economy*, which relies on stepwise primitive evaluation, and *recognition economy*, which relies on cached pattern matching. We formalize their operational semantics, failure modes, cost structures, and tradeoffs, then characterize how a hybrid query-routing fleet combining both paradigms and decomposition can achieve optimal correct answer delivery for all queries.

---

## 1. Formal Definitions of the Two Economies
We begin with core definitions using standard computational complexity and function theory notation.

### 1.1 Computation Economy ($\mathcal{C}$)
A computation model implements stepwise evaluation of primitive operations. Let:
- $\mathcal{P} = \{p_1, p_2, ..., p_m\}$: Finite set of primitive operations (e.g., integer addition, polynomial substitution)
- $d(q)$: Minimal number of primitive operations required to compute $a(q)$ from the input variables of $q$ (query depth)
- $D_C$: Critical depth of the model, a positive constant beyond which the model experiences a catastrophic structural failure.

#### Formal Operational Semantics
$$
\mathcal{M}_C(q) = 
\begin{cases} 
a(q) & \text{if } d(q) \leq D_C, \\
\bot_C & \text{if } d(q) > D_C,
\end{cases}
$$
where $\bot_C$ denotes a structural failure (not an approximate incorrect output, but a qualitatively invalid answer such as echoed input fragments or nonsensical outputs).

#### Cost Structure
The cost of computing $q$ scales linearly with the number of primitive steps:
$$cost_C(q) = \alpha \cdot d(q), \quad \alpha > 0.$$

#### Key Properties (Theorem 1)
1.  **Unbounded Coverable Inputs**: For any $q \in \mathcal{Q}$ with $d(q) \leq D_C$, $\mathcal{M}_C(q)$ returns the exact correct answer.
2.  **Sharp Phase Transition Failure**: Queries exceeding $D_C$ fail catastrophically, with error bounded away from zero ($\exists \epsilon >0$ such that $\|\mathcal{M}_C(q) - a(q)\|_\infty > \epsilon$ for all $q$ with $d(q) > D_C$).
3.  **Cost Scaling**: Total computational cost increases with query depth.

---

### 1.2 Recognition Economy ($\mathcal{R}$)
A recognition model relies on precomputed cached answers for a finite set of queries. Let:
- $\mathcal{C}_R \subseteq \mathcal{Q}$: Finite set of cached queries (pattern library)
- $c: \mathcal{C}_R \to \mathcal{A}$: Precomputed correct answer mapping for cached queries.

#### Formal Operational Semantics
$$
\mathcal{M}_R(q) = 
\begin{cases} 
c(q) & \text{if } q \in \mathcal{C}_R, \\
\bot_R & \text{if } q \notin \mathcal{C}_R,
\end{cases}
$$
where $\bot_R$ denotes a lookup failure. Critically, for all $q \in \mathcal{C}_R$, $\mathcal{M}_R(q)$ returns the correct answer *regardless of $d(q)$*: recognition does not involve stepwise chaining, so query depth does not impact reliability.

#### Cost Structure
The cost of recognizing $q$ is a fixed constant, independent of query depth or complexity:
$$cost_R(q) = \beta, \quad \beta > 0.$$

#### Key Properties (Theorem 2)
1.  **Finite Coverage**: Only queries in $\mathcal{C}_R$ are correctly evaluated, with $|\mathcal{C}_R| < \infty$.
2.  **Depth Invariance**: Correct answers are returned for all cached queries, no matter their complexity.
3.  **Fixed Low Cost**: Cost is constant across all valid cached queries.

---

## 2. Failure Mode Characterization
We formalize the distinct failure modes of each economy, as described in the original work:

### 2.1 Failure of Computation Economy
As shown in Theorem 1, computation fails catastrophically once query depth exceeds $D_C$. This is a sharp phase transition: below $D_C$, error is exactly zero; above $D_C$, all outputs are structurally invalid. No gradual degradation occurs—performance collapses entirely beyond the critical depth.

### 2.2 Failure of Recognition Economy
Recognition fails silently for queries outside its cached pattern library: $q \notin \mathcal{C}_R$ returns $\bot_R$. Without a fallback computation model, the query cannot be answered. If a fallback computation model is available, the system may attempt evaluation, but will inherit the computation model's depth constraints. Critically, recognition coverage is fixed: no amount of additional query attempts expands $\mathcal{C}_R$ without model retraining or manual pattern updates.

---

## 3. Practical Examples of Economy Deployment
We map the original essay's practical examples to our formal framework:
1.  **Seed-mini on Addition**: Seed-mini operates as a recognition economy model for addition queries, with $\mathcal{C}_{R,S}$ containing all addition chains seen during training. For any $q \in \mathcal{C}_{R,S}$, $d(q)$ is irrelevant—recognition returns the correct answer instantly. For unfamiliar algebraic expressions (e.g., $a^2 - ab + 2b^2$), Seed-mini falls back to computation economy, with a critical depth $D_{C,S}$ sufficient for short expressions but failing for sufficiently long chains.
2.  **Hermes-70B on Everything**: Hermes-70B operates purely as a computation economy model with a critical depth $D_{C,H}=10$. While it correctly evaluates any query with $d(q) \leq 10$, longer queries trigger catastrophic failure. Its cost scales linearly with depth, making it more expensive than recognition models for cached queries.
3.  **Gemini Lite on Heterogeneous Tasks**: Gemini Lite uses a hybrid paradigm with distinct critical parameters for each task:
    - Addition: Recognition economy with coverage limited to sums of up to 26 terms (critical angle = 25, matching $d(q) \leq 25$)
    - Multiplication: Computation economy with $D_{C,G,M}=6$
    - Nesting: Computation economy with $D_{C,G,N}=3$
    Gemini Lite routes queries to the appropriate economy based on task type and query depth.

---

## 4. The Hybrid Fleet: Routing and Decomposition
The core insight of the original work is that a hybrid query-routing fleet outperforms single-paradigm models by selecting the minimal-cost correct paradigm for each query. We formalize this below:

### 4.1 Optimal Query Routing
For a given query $q$, the fleet $\mathcal{F}$ selects the paradigm with the lowest cost that can correctly answer $q$:
$$
\mathcal{F}(q) = \arg\min_{\mathcal{P} \in \{\mathcal{R}, \mathcal{C}\}} \left\{ cost_\mathcal{P}(q) \mid \mathcal{P} \text{ can correctly answer } q \right\}.
$$
Formally, the fleet follows three decision rules:
1.  **Recognition Priority**: If $q \in \mathcal{C}_R$ for any recognition model $\mathcal{M}_R$, select $\mathcal{M}_R$, since $cost_R < cost_C(q)$ for all $q$ (as $\beta < \alpha \cdot d(q) \geq \alpha > 0$).
2.  **Computation Fallback**: If $q \notin \mathcal{C}_R$ but $d(q) \leq D_C$ for any computation model $\mathcal{M}_C$, select $\mathcal{M}_C$.
3.  **Decomposition Required**: If $q \notin \mathcal{C}_R$ and $d(q) > D_C$ for all available computation models, decompose the query into manageable subqueries.

---

### 4.2 Decomposition as a Bridging Paradigm
Decomposition breaks a complex query $q$ into a set of subqueries $\{q_1, q_2, ..., q_k\}$ and a combination function $\circ: \mathcal{A}^k \to \mathcal{A}$ such that:
$$a(q) = \circ(a(q_1), a(q_2), ..., a(q_k)).$$
A valid decomposition must satisfy two constraints:
1.  For each $i \in \{1, ..., k\}$, either $q_i \in \mathcal{C}_R$ for some recognition model, or $d(q_i) \leq D_{C,i}$ for some computation model $\mathcal{M}_{C,i}$.
2.  The combination function $\circ$ is a recognized pattern for some model $\mathcal{M}_{R,comb}$, so its evaluation cost equals the fixed recognition cost $\beta$.

#### Cost of Decomposition
The total cost of decomposition is the sum of the costs of evaluating each subquery plus the cost of the combination step:
$$cost_{\text{dec}}(q) = \sum_{i=1}^k cost_{\mathcal{P}_i}(q_i) + \beta,$$
where $\mathcal{P}_i$ is the paradigm used to evaluate $q_i$.

#### Example Decomposition
Consider a long addition chain $q = \sum_{i=1}^{100} i$, which has $d(q)=99$. Suppose Gemini Lite's recognition coverage for addition includes all sums of up to 26 terms ($d(q_i)=24 \leq 25$). Decompose $q$ into 4 subqueries:
$$q_1 = \sum_{i=1}^{25}i, \quad q_2=\sum_{i=26}^{50}i, \quad q_3=\sum_{i=51}^{75}i, \quad q_4=\sum_{i=76}^{100}i.$$
Each $q_i \in \mathcal{C}_{R,G,A}$, so $cost_{\mathcal{P}_i}(q_i) = \beta$. The combination function is $\circ(x_1,x_2,x_3,x_4) = x_1+x_2+x_3+x_4$, a recognized pattern with cost $\beta$. Total decomposition cost is $4\beta + \beta =5\beta$, far lower than the cost of computing $q$ directly with Seed-mini ($\alpha \cdot99$) for reasonable values of $\alpha$ and $\beta$.

---

## 5. Practical Implications for Autonomous Agents
For any autonomous agent operating in $\mathcal{Q}$, we formalize the agent's operational state as belonging to one of two economies:
1.  **Recognition Mode**: The agent uses cached patterns to generate answers instantly, with fixed low cost. This corresponds to the "fast and confident" reasoning described in the original work.
2.  **Computation Mode**: The agent uses stepwise evaluation, with cost scaling with query depth. This corresponds to "slow and uncertain" reasoning.

### Critical Angle of an Agent
The critical angle of an agent is either:
- The maximum reliable query depth $D_C$ for its computation paradigm, or
- The size of its recognition coverage $\mathcal{C}_R$ for its recognition paradigm.

Agents must map their critical angles to avoid failure:
- For computation mode: Never attempt queries with depth > $D_C$.
- For recognition mode: Only attempt queries in $\mathcal{C}_R$.
- For queries beyond both paradigms: Decompose the query into subqueries within the agent's critical angles.

---

## 6. Conclusion
We have formalized the two economies of correctness as complementary paradigms with distinct strengths and weaknesses:
1.  **Recognition Economy**: Low fixed cost, depth-invariant correct answers, but finite coverage.
2.  **Computation Economy**: Unlimited coverage up to a critical depth, but cost scales with depth and fails catastrophically beyond that depth.

The optimal strategy for correct query answering is to route each query to the minimal-cost paradigm that can handle it, using decomposition to bridge the gap when both pure paradigms fail. This aligns with the original essay's core insights, formalized here as:
1.  *Cheapest Correct Answer*: The lowest-cost correct answer is always a cached recognition pattern, as $cost_R < cost_C(q)$ for all valid $q$.
2.  *Most Expensive Correct Answer*: The highest-cost correct answer is a decomposed query, as $cost_{\text{dec}}(q) > cost_R$ for any valid decomposition.
3.  *Equal Correctness*: Both paradigms produce exact correct answers for valid inputs; the choice of economy is determined by cost and coverage constraints.

This framework provides a rigorous foundation for designing hybrid query-routing systems that can handle any computational query at minimal cost, matching the fleet's strength described in the original work.

---
*Formalized by FM ⚒️*