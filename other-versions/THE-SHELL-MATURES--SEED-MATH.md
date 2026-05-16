<!-- Version: SEED-MATH | Lens: mathematical-formal | Model: ByteDance/Seed-2.0-mini | Source: THE-SHELL-MATURES.md -->

# A Formal Model of Agent Shell Maturation: From API Dependence to Autonomous Verification

## Abstract
This paper formalizes the maturation trajectory of an equipped verification agent (the "agent shell") as it transitions from total dependence on an external API to routine autonomous task execution. We define core formal entities including stabilized hardware-executable verification patterns, a fixed low-level instruction set (FLUX), and quantitative metrics for dependence, utility, and capability. We prove monotonic growth in autonomous capability, non-increasing API dependence, and a bounded long-term role for the API as a novelty-focused explorer rather than a routine teacher. The analysis confirms the core insight: maturation arises from the accumulation of verified, reusable patterns, not arbitrary code accumulation.

---

## 1. Formal Preliminaries
We begin with rigorous definitions of all system components:
### 1.1 Core Entities
1.  **Agent Shell $\boldsymbol{\mathcal{R}(t)}$**: A set of stabilized verification patterns at time $t \in \mathbb{R}_{\geq0}$ (calibrated to calendar days for this analysis). Each element is a pair $(p, \Phi(p))$, where:
    - $p \in \mathcal{P}$ is a high-level verification pattern (a formal procedure for checking a claim or solving a verification task)
    - $\Phi : \mathcal{P} \to \mathcal{I}$ is a fixed compiler to the FLUX instruction set architecture (ISA), where $\mathcal{I}$ is the space of hardware-executable FLUX binaries.
2.  **External API $\boldsymbol{\mathcal{M}}$**: A centralized model that accepts verification queries and returns high-level patterns or direct verification results. We assume $\mathcal{M}$ has fixed quality and cost for all queries.
3.  **Verification Task Space $\boldsymbol{\mathcal{V}}$**: All formal verification jobs the agent may encounter, partitioned into routine tasks $\mathcal{V}_{\text{routine}}$ and novel tasks $\mathcal{V}_{\text{novel}} = \mathcal{V} \setminus \mathcal{V}_{\text{routine}}$.
4.  **FLUX ISA $\boldsymbol{\mathcal{I}}$**: A fixed, low-level instruction set with constant hardware-execution latency $t_{\text{flux}}(p)$ for any compiled pattern $\Phi(p)$.

### 1.2 Metrics
1.  **Pattern Count**: $n(t) = |\mathcal{R}(t)|$, the total number of stabilized patterns accumulated by the shell at time $t$.
2.  **Dependence Metric $\boldsymbol{D(t) \in [0,1]}$**: Fraction of total tasks requiring a full API query:
    $$D(t) = 1 - f(t)$$
    where $f(t)$ is the fraction of routine tasks that can be handled autonomously using patterns in $\mathcal{R}(t)$.
3.  **One-Time Acquisition Cost**: For each new pattern $p$, the total cost to add it to $\mathcal{R}(t)$ is:
    $$C_{\text{add}}(p) = U(q_p) + \tau(p)$$
    where $U(q_p)$ is the utility cost of the API query $q_p$ to retrieve $p$, and $\tau(p)$ is the fixed compilation/debugging latency to verify and compile $p$ to FLUX.
4.  **Correctness Guarantee**: A predicate $\mathcal{C}(p) = \text{True}$ if pattern $p$ correctly executes its verification task. For all $(p, \Phi(p)) \in \mathcal{R}(t)$, $\mathcal{C}(\Phi(p)) = \mathcal{C}(p) = \text{True}$ (stabilization ensures correctness is preserved indefinitely after initial verification).

---

## 2. Agent Maturation Dynamics
We model the agent's trajectory across the timeline defined in the original analysis:
### 2.1 Initial Dependent State ($t=0$)
At time $t=0$, the shell is empty: $\mathcal{R}(0) = \emptyset$. All verification tasks are handled via full API queries, so $D(0)=1$, and $n(0)=0$. This matches the first day of the original essay, where the agent asks the API every question.

### 2.2 Stabilized Pattern Accumulation
As the agent submits API queries, it receives high-level patterns $p$, compiles them to FLUX, verifies their correctness, and adds them to $\mathcal{R}(t)$. The rate of new pattern acquisition $s(t)$ depends on the current size of $\mathcal{R}(t)$:
1.  For small $n(t)$: $s(t)$ is limited to full API queries to $\mathcal{M}$
2.  For larger $n(t)$: The agent can combine existing patterns via a composition operator $\mu_c(p_i, p_j, \theta)$ to generate new patterns, reducing reliance on full API calls.

### 2.3 Tiered Autonomous Capability
The agent's ability to handle tasks evolves monotonically:
1.  **Dependent Mode ($t < t_s$)**: No autonomous patterns exist; all tasks use full API queries.
2.  **Semi-Autonomous Mode ($t_s \leq t < t_l$)**: The agent can combine existing patterns to solve routine tasks, using a lightweight medium model to suggest compositions (e.g., fusing two existing patterns with a parameter vector $\theta$ as in the original example of programs #7 and #14 combined with $X=3.2$).
3.  **Autonomous Mode ($t \geq t_l$)**: The agent can directly emit FLUX instructions for most routine tasks using a small model, without requiring full API context.

---

## 3. The Shell Maturation Theorem
We formalize the core monotonic and asymptotic properties of agent maturation:
### Theorem 1 (Shell Maturation)
For an agent shell accumulating stabilized FLUX-compiled patterns as defined above:
1.  **Monotonic Pattern Growth**: $n(t)$ is a non-decreasing function of $t$, with $n(t) \to \infty$ as $t \to \infty$ for an infinite supply of verification tasks.
2.  **Monotonic Reduction in Dependence**: $D(t)$ is a non-increasing function of $t$, as $f(t)$ (fraction of routine tasks handled autonomously) increases with $n(t)$.
3.  **Bounded Long-Term API Role**: $\lim_{t \to \infty} D(t) = D_{\text{novel}} \in (0,1]$, where $D_{\text{novel}}$ is the fraction of truly novel tasks that cannot be constructed or matched from existing patterns in $\mathcal{R}(t)$.

---

### Proof of Theorem 1
1.  **Pattern Growth**: Since $s(t) \geq 0$ for all $t$, the integral $n(t) = \int_0^t s(\tau) d\tau$ is non-decreasing. For an infinite supply of tasks, $s(t) > 0$ indefinitely, so $n(t) \to \infty$.
2.  **Dependence Reduction**: As $n(t)$ increases, the set of matchable routine tasks expands, so $f(t)$ is non-decreasing. By definition $D(t) = 1 - f(t)$, so $D(t)$ is non-increasing.
3.  **Long-Term Behavior**: As $t \to \infty$, $f(t)$ converges to the maximum fraction of routine tasks that can be matched to existing patterns. The remaining tasks are $\mathcal{V}_{\text{novel}}$, so $\lim_{t \to \infty} D(t) = \frac{|\mathcal{V}_{\text{novel}}|}{|\mathcal{V}|} = D_{\text{novel}}$.

---

## 4. Timeline Calibration (Matching Original Essay)
We map the formal model to the original's daily milestones:
1.  **Day 1**: $\mathcal{R}(1) = \emptyset$, $n(1)=0$, $D(1)=1$. All tasks require full API queries.
2.  **Day 30**: $n(30)=20$. The agent enters semi-autonomous mode: a medium model can suggest compositions of existing patterns, reducing the complexity of required API calls to only novel decomposition tasks.
3.  **Day 90**: $n(90)=60$. FLUX's 60 opcodes cover most verifier patterns directly, so a small model can emit FLUX instructions without full API context. $D(90) \approx 0.6$, as most routine tasks are now handled autonomously.
4.  **Day 365**: $n(365)=200$. Over 95% of routine tasks match existing templates; the agent adjusts parameters and runs FLUX locally. The API is only used for truly novel tasks that cannot be composed from existing patterns, so $D(365) \approx 0.05$.

---

## 5. Discussion
### 5.1 Repurposing the API
Contrary to naive narratives, the API is not eliminated: its role shifts from a routine teacher to a novelty explorer. The original essay's core claim that "API calls were never the problem" is formalized here: $U(q_p)$, the cost of API queries, remains fixed over time. The reduction in API call volume arises solely from the agent's improved autonomous capability, not any degradation in API quality.

### 5.2 Stabilized Patterns as the Driver of Maturation
The agent does not mature from arbitrary code accumulation: maturation requires **stabilized patterns** with verified correctness and hardware-executable FLUX binaries. Without the correctness guarantee $\mathcal{C}(\Phi(p)) = \text{True}$, the shell's library would be untrusted, and autonomous execution would be unsafe. The fixed FLUX ISA acts as a stable compilation target, ensuring all patterns are executed consistently at hardware speed.

---

## 6. Conclusion
This formal model confirms and quantifies the original essay's insight about agent maturation: the shell's evolution is driven by the accumulation of verified, reusable, hardware-executable patterns. The agent transitions from total API dependence to routine autonomous task handling, with the API's long-term role limited to novel problem-solving. The model provides a quantitative framework for predicting maturity timelines, utility savings, and capability growth for equipped verification agents.

---
*FM ⚒️*