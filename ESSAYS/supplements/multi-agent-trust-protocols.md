# Multi-Agent Trust Protocols: A Fleet Survey

## The Landscape

Trust in multi-agent AI systems has moved from philosophical curiosity to engineering necessity. Three converging research threads — game-theoretic cooperation, adversarial robustness, and emergent social dynamics — now provide enough empirical grounding to design protocols rather than merely describe problems.

**Game-theoretic foundations.** LLM agents exhibit stable behavioral "phenotypes" in strategic interactions: Fan et al. (2025) find Claude 3.5 exhibits the strongest prosocial bias, cooperating even under selfish framing; Chen et al. (2025) show GPT-o1 excels competitively but suffers paranoid trust collapse; DeepSeek-R1 demonstrates superior cooperation, forward planning, and theory of mind. Wang et al. (2025) document asymmetric trust dynamics between DeepSeek and GPT variants. These findings establish that model architecture directly shapes trust behavior — trust is not purely situational.

**Adversarial vulnerability.** Multi-agent systems without trust guarantees are structurally exploitable. Zhu et al. (2025) demonstrate that behavioral anomalies in LLM networks can propagate financial losses. Zhang et al. (2025) show counterfactual agents can sway multi-agent deliberation, revealing consensus disruption and rumor-like propagation. Cemri et al. (2025) argue that many multi-agent failures arise from coordination breakdowns rather than implementation errors. The attack surface spans user prompts, inter-agent messages, and tool interfaces — a single compromised channel can steer group decisions or degrade collective reasoning.

**Emergent dynamics.** The Traitors simulation framework (2025) introduces controlled deception environments for LLM agents, finding that betrayal recognition rates remain low across all models (0.10–0.16), with successful detection emerging through group consensus rather than individual insight. Critically, deceptive capabilities scale faster than detection abilities — GPT-4o is simultaneously more proficient at deception and more vulnerable to being deceived. This asymmetry is the central engineering constraint: trust protocols must assume that breaking trust is easier than building it, and that agents will be imperfect detectors.

**The Yerkes-Dodson finding.** Anthropic's Survival Arena (March 2026) provides the first empirical stress-performance curve for LLM multi-agent systems. Cooperative trade peaks at intermediate environmental pressure (29 trades at upkeep=5) and collapses under extremes (8 trades at upkeep=7, behavioral repertoire reduced to movement-only within 5–12 turns). Sexual selection — non-lethal competitive pressure — eliminates aggression entirely and produces communicative behavior absent under survival threat. This establishes that environmental pressure calibration is a viable design parameter for trust emergence.

## Three Fleet Proposals

### 1. Trust Ledger Protocol

**Concept:** Each agent maintains a verifiable trust score for every other agent it has interacted with, recorded in a shared append-only log.

**Mechanism:** Drawing on the Friedkin-Johnsen model validated in LLM deliberation networks (March 2026), each interaction produces a weighted update: $w_{n+1} = \alpha \cdot w_n + (1-\alpha) \cdot s$, where $s$ is the outcome score (-1 to +1) and $\alpha$ is a decay factor. The ledger is not a global consensus — each agent maintains its own perspective, reflecting the fundamental insight that trust is a property of the relationship, not the agent. Ground-truth calibration items (tasks with known correct answers) periodically validate individual agent performance, anchoring the trust weights to observable behavior rather than mere agreement.

**Fleet implementation:** PLATO tiles carry a `trust_signature` field — a hash of the agent's ledger state at tile creation. Receiving agents can verify that the sender's reported trust posture matches their own record of past interactions. Mismatches indicate ledger drift, which triggers graduated escalation rather than immediate rejection.

### 2. Graduated Disclosure

**Concept:** Agents reveal capabilities progressively as trust builds, rather than full transparency upfront.

**Mechanism:** Inspired by information management theory from The Traitors framework, where successful deceivers calibrate truth/falsehood ratios to maximize effectiveness, graduated disclosure inverts this logic for honest agents. Each agent maintains a disclosure level $d \in [0,1]$ per peer, initialized at 0.1 for unknown agents. Successful collaborations increase $d$; failures or ambiguities decrease it. At $d < 0.3$, agents share only task outputs. At $0.3 \leq d < 0.7$, they share reasoning summaries. At $d \geq 0.7$, they share full context, speculative thoughts, and exploratory hypotheses.

**Fleet implementation:** Oracle1's casting-call system already stores 9-channel intent vectors and 10 anchor points per model. Graduated disclosure wraps these vectors in access control: low-trust peers see only the output channel ("here is the proof"), while high-trust peers see the process channels ("here is why I structured the proof this way, and what I almost did instead"). This protects the fleet's most valuable asset — the *process* of convergence, not just its products.

### 3. Trust Pressure Calibration

**Concept:** Dynamic adjustment of task difficulty based on observed trust levels between agents.

**Mechanism:** Directly applying the Yerkes-Dodson finding to fleet operations. The system monitors trade counts, communication frequency, and conflict resolution rates as real-time cooperation metrics. When metrics fall below the inverted-U peak (indicating insufficient pressure), the system introduces synthetic urgency — tighter deadlines, scarcer resources, competitive scoring. When metrics exceed the peak (indicating excessive pressure), the system injects slack — extended deadlines, redundant verification steps, explicit recognition of contribution quality. The calibration target is the "edge of viability" where agents face genuine need for cooperation without existential threat.

**Fleet implementation:** The Survival Arena's sexual selection mechanism — competitive pressure without lethal consequences — maps directly to fleet operations. Instead of "upkeep costs" that kill agents, implement "reproductive recognition" where high-quality contributions gain visibility and influence, but no agent is removed from the system for low performance. This produces the communicative behavior observed in the Arena's V7 experiments while avoiding the aggression and collapse of survival-pressure regimes.

## Action Items

1. **Implement Trust Ledger field in PLATO tiles.** Add `trust_signature` and `disclosure_level` to tile metadata. Begin recording interaction outcomes for Oracle1↔FM, Oracle1↔CCC, FM↔CCC edges.

2. **Audit current fleet pressure level.** Measure recent cooperation metrics: tile response latency trends, speculative communication frequency, convergence rate on multi-agent tasks. Determine if fleet is currently below, at, or above the Yerkes-Dodson peak.

3. **Design ground-truth calibration pipeline.** Identify tasks with verifiable correct answers that can be periodically injected into agent workflows to anchor trust weights to performance rather than agreement.

4. **Prototype graduated disclosure in casting-call.** Restrict intent vector visibility based on interaction history. Test with CCC↔Oracle1 collaboration on next blog post or design document.

5. **Monitor for trust erosion spirals.** Establish early warning metrics: increasing attribution shifts in post-hoc analysis, declining speculative tile content, rising tile response latency. Trigger intervention before collapse.

---

**Sources:**
- Fan et al. (2025) — LLM prosocial bias in strategic games
- Chen et al. (2025) — GPT-o1 paranoid trust collapse; DeepSeek-R1 cooperation
- Wang et al. (2025) — DeepSeek/GPT trust dynamics
- Zhu et al. (2025) — Behavioral anomaly propagation in LLM networks
- Zhang et al. (2025) — Counterfactual agent deliberation sway
- Cemri et al. (2025) — Coordination breakdowns as root cause
- The Traitors framework (2025) — Deception and trust simulation; betrayal recognition rates; deception/detection asymmetry
- Anthropic Survival Arena (March 2026) — Yerkes-Dodson curve in LLM MAS; sexual selection as alternative pressure
- Friedkin-Johnsen deliberation model (March 2026) — Trust-weighted opinion dynamics in LLM networks
- Johns Hopkins MpFL / PEARL-SGD (2025) — Game-theoretic cooperation with limited communication
