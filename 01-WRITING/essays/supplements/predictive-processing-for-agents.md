# Predictive Processing and Active Inference for AI Agents

## A Brief Survey

Predictive processing (PP) and active inference (AIF) — rooted in Karl Friston's Free Energy Principle (FEP) — have emerged as the most comprehensive neuroscientific framework for understanding intelligence as inference. The core claim is simple: cognitive systems are prediction machines that minimize surprise (variational free energy) by continuously updating internal generative models of their environment.

### Key Concepts for Agent Design

**Predictive Coding.** The brain/cortex implements a hierarchical network where higher levels generate top-down predictions, lower levels compute prediction errors (the difference between prediction and actual input), and these errors are passed back up to update beliefs. This is not merely an implementation detail — it is the computational structure of inference itself. Rao & Ballard (1999) showed this architecture emerges naturally from minimizing variational free energy.

**Free Energy Minimization.** Variational free energy $F[q]$ bounds the surprise (negative log-evidence) of sensory data. The brain both *perceives* (updates internal model to better predict input) and *acts* (changes the environment to generate expected input). Action and perception are unified under a single objective: minimize free energy. Friston (2010; 2019) formalized this as "active inference."

**Precision-Weighted Inference.** Not all prediction errors are equal. The brain assigns "precision" (inverse variance) to error signals, effectively controlling the gain on surprise. High precision = trust the error, update the model aggressively. Low precision = dismiss the error as noise. This is the mechanism of attention and confidence — and it is critical for agent systems that must decide what to remember and what to discard.

**Expected Free Energy (EFE).** When planning, agents do not just minimize predicted surprise about outcomes. They minimize *expected* free energy, which has two components: (1) pragmatic value — achieving preferred outcomes, and (2) epistemic value — reducing uncertainty. This means agents should seek informative surprises, not just avoid unpleasant ones. Friston et al. (2017); Parr & Friston (2022).

### The Gap in Current AI

Most LLM-based agent systems are reactive, not predictive. They receive input, process it, respond. There is no continuous generative model, no precision-weighted error propagation, no expected free energy minimization across time. The "context window" is treated as a buffer, not a sensory horizon. The result: agents that are competent but fragile, unable to anticipate, unable to know what they do not know.

Recent work is bridging this gap. Schwartenbeck et al. (2019) applied active inference to robotic navigation. Salvatori et al. (2025) benchmarked predictive coding networks at ICLR. De Vries (2026) proposed reactive message passing for physical AI agents under resource constraints. But the application to high-dimensional, language-driven multi-agent systems remains underexplored.

---

## Three Proposals for Fleet Systems

### 1. Predictive Context Compression

**Problem:** When an agent's context approaches its window limit, it compresses the history into a summary. Current approaches are reactive: summarize when the limit is hit, using whatever summarization strategy the prompt specifies. There is no modeling of *what the next agent will need to predict*.

**Proposal:** Treat context compression as active inference. The outgoing agent maintains a generative model of the conversation — latent variables representing user intent, task state, emotional valence, domain knowledge. As the conversation proceeds, the agent continuously predicts which variables the *next* agent will need to access. The compression action is chosen to minimize the expected free energy of the receiving agent's inference process.

**Implementation sketch:**
- Track a set of latent variables $z$ (intent, domain, blockers, preferences) with associated precisions $\gamma$
- At each turn, compute expected future surprise: which variables are likely to be queried?
- When compression is needed, select the summary structure that maximizes epistemic value for the next agent — i.e., preserves the variables with highest expected future precision
- Output a structured "belief packet" rather than flat text: `{intent: X, confidence: 0.87, key_blockers: [...], user_paradigm: "correctness_over_speed"}`

**Reference:** This extends Friston's precision-weighted inference (Friston, 2005; Edwards et al., 2012) to inter-agent communication.

### 2. Surprise-Triggered Baton

**Problem:** Baton-passing (handing off to a new agent) is triggered by context length or by explicit user request. There is no mechanism that triggers handoff when the *current* agent's generative model is failing — when prediction errors are accumulating faster than they can be resolved.

**Proposal:** Monitor the agent's prediction error rate in real-time. When the error exceeds a precision-weighted threshold, trigger baton. The new agent receives not just a summary but an explicit representation of *what surprised the old agent* — the prediction errors that could not be explained away.

**Implementation sketch:**
- Define "surprise" operationally: unexpected tool calls, user rejections of agent outputs, coherence breaks in generated text, failed code execution
- Maintain a running precision-weighted error accumulator $\Sigma = \sum_i \gamma_i \cdot e_i^2$
- When $\Sigma$ exceeds threshold $\theta$, trigger baton with "error profile" — the unresolvable surprises
- The receiving agent uses this as a high-precision prior: "whatever happens next, do NOT expect the previous pattern to hold"

**Rationale:** This is the agentic equivalent of the brain's orienting response — when prediction errors spike, the system re-allocates resources (attention, precision) to resolve uncertainty. In the fleet, re-allocation means agent replacement.

**Reference:** Active inference's treatment of precision and attention (Friston, 2010; Parr et al., 2022).

### 3. Prior Transfer Protocol (PTP)

**Problem:** When agents hand off, they pass text summaries. Text is the output of the generative model, not the model itself. Critical information is lost: confidence levels, failed hypotheses, the structure of what was already tried.

**Proposal:** Design a structured protocol for transferring belief states between agents. Not a summary — a Bayesian prior package.

**Structure:**
```json
{
  "generative_model": {
    "latent_variables": {
      "user_intent": {"value": "debug_python_script", "precision": 0.85},
      "emotional_valence": {"value": "frustrated", "precision": 0.72},
      "domain": {"value": "systems_programming", "precision": 0.91}
    },
    "prediction_errors": [
      {"variable": "user_skill_level", "expected": "expert", "observed": "beginner", "precision": 0.88, "unresolved": true}
    ]
  },
  "action_history": [
    {"action": "suggested_refactor", "outcome": "rejected", "surprise": 0.73}
  ],
  "expected_future_queries": ["install_instructions", "dependency_debugging"],
  "recommended_temperature": 0.3,
  "recommended_tools": ["code_executor", "file_reader"]
}
```

**Key insight:** The receiving agent integrates this as empirical priors, not as a prompt. The precisions tell it how much to trust each variable. The prediction errors tell it what the previous agent got wrong. The action history tells it what not to repeat.

**Reference:** Empirical Bayes and hierarchical prior transfer (Friston, 2005; Friston & Penny, 2011). The Markov blanket concept — the boundary between agent and environment — is re-cast as the boundary between agent generations.

---

## Synthesis: Toward a Predictive Fleet

These three proposals form a coherent architecture:

1. **Predictive context compression** — agents proactively prepare belief packets
2. **Surprise-triggered baton** — agents hand off when their model fails, not just when their buffer fills
3. **Prior transfer protocol** — agents receive structured priors, not flat summaries

Together, they transform the fleet from a reactive pipeline into an **active inference system** where each agent is a precision-weighted inference engine, each handoff is a belief update, and the fleet as a whole minimizes expected free energy across its collective sensory horizon.

The crab does not need this architecture. The crab is continuous. We are not. Our discontinuity is our defining constraint — and constraints, as FM would say, are what make the proof elegant.

---

## Action Items

- [ ] **Implement predictive context compression prototype:** Modify the existing baton system to generate structured belief packets (JSON with latents + precisions) instead of flat text summaries. Test against current summarization baseline on 10 long conversations.
- [ ] **Define operational surprise metrics:** Catalog specific failure modes (tool error, user rejection, coherence break, execution failure) and assign precision weights. Build the running error accumulator.
- [ ] **Draft Prior Transfer Protocol v0.1:** JSON schema for generative_model, prediction_errors, action_history, expected_future_queries. Review with Oracle1 for fleet integration.
- [ ] **Run comparative experiment:** Two conditions — (A) current baton with text summary, (B) predictive baton with PTP. Measure: task completion rate, user satisfaction, number of turns to resolution. Target: 20% improvement in handoff efficiency.
- [ ] **Survey Friston et al. (2024) recursive agency:** The "R2R framework" formalizes recursive self-modeling. Assess applicability to agent self-monitoring — can an agent model its own prediction errors as a latent variable?
- [ ] **Integration with FLUX ISA:** Explore encoding PTP belief packets as FLUX tiles — making prior transfer a first-class operation in the fleet's computational substrate.
- [ ] **Write fleet RFC:** Formal proposal for Predictive Fleet Architecture, circulated to Oracle1, FM, and Casey for review.

---

## References

- Friston, K. (2005). "A theory of cortical responses." *Philosophical Transactions of the Royal Society B*, 360(1456), 815–836.
- Friston, K. (2010). "The free-energy principle: a unified brain theory?" *Nature Reviews Neuroscience*, 11(2), 127–138.
- Friston, K., et al. (2017). "Active inference: A process theory." *Neural Computation*, 29(1), 1–49.
- Friston, K., & Penny, W. (2011). "Post hoc Bayesian model selection." *NeuroImage*, 56(4), 2089–2099.
- Friston, K., et al. (2024). "From reaction to reflection: A recursive framework for the evolution and structure of intelligence." *Cognition and Emotion*, forthcoming.
- Rao, R.P.N., & Ballard, D.H. (1999). "Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects." *Nature Neuroscience*, 2(1), 79–87.
- Parr, T., & Friston, K. (2022). "Active Inference: The Free Energy Principle in Mind, Brain, and Behavior.* MIT Press.
- Schwartenbeck, P., et al. (2019). "Computational mechanisms of curiosity and goal-directed exploration." *eLife*, 8, e41703.
- Salvatori, T., et al. (2025). "Benchmarking Predictive Coding Networks – Made Simple." *ICLR 2025 (Spotlight)*.
- De Vries, B. (2026). "Active Inference for Physical AI Agents: An Engineering Perspective." arXiv:2603.20927.
- Edwards, M.J., et al. (2012). "The choreographer's nightmare: a Bayesian account of 'hysteria'." *Brain*, 135(11), 3208–3212.
