# Attention Architecture for Fleets

## A Survey and Three Proposals

### 1. From Cognitive Psychology to Machine Attention

Human attention has been studied for over a century as a solution to a fundamental problem: the brain has limited processing capacity, but the world offers unlimited information. Three foundational models describe how biological systems manage this mismatch:

**Broadbent's Filter Model (1958)** posits an early-selection bottleneck. Sensory information is filtered based on physical characteristics (pitch, loudness, spatial location) before semantic processing occurs. Unattended information is discarded, not merely deprioritized. The model explains the cocktail party effect — selective listening in noisy environments — but struggles with findings that unattended information can still influence behavior (e.g., hearing one's name across a room).

**Treisman's Feature Integration Theory (1980)** refines this by proposing two stages. In the pre-attentive stage, basic visual features (color, orientation, motion) are processed in parallel across the visual field, registered in separate "feature maps." In the focused attention stage, a spatial spotlight binds these features into coherent objects at attended locations. Without focused attention, features remain unbound, leading to "illusory conjunctions" — misperceptions where features from different objects are incorrectly combined.

**Desimone & Duncan's Biased Competition Model (1995)** shifts the metaphor from filtering or spotlighting to competition. Multiple objects in the visual field simultaneously compete for neural representation. Attention biases this competition — toward relevant locations, features, or objects — rather than creating a separate selection mechanism. The unattended items are not blocked; they are merely losing a neural race.

These three models are not mutually exclusive. They describe different scales: Broadbent's filter operates at the sensory periphery, Treisman's spotlight at the feature-binding level, Desimone and Duncan's competition at the representational level. Together, they form a hierarchy of selection mechanisms that biological systems use to cope with informational overflow.

### 2. From Bahdanau to Transformers

Machine attention emerged from a parallel problem: sequence-to-sequence models (e.g., for machine translation) compressed variable-length inputs into fixed-size context vectors, losing information. Bahdanau et al. (2015) introduced a differentiable attention mechanism where the decoder at each step could dynamically attend to different parts of the encoder's hidden states, computing relevance scores via a learned alignment model. The decoder's output became a weighted sum of encoder representations — attention as soft selection.

Vaswani et al. (2017) generalized this into the transformer architecture's multi-head self-attention. Key innovations:
- **Self-attention**: Every token attends to every other token, removing sequential recurrence
- **Multi-head attention**: Multiple parallel attention heads (typically 8-32) compute different Query/Key/Value projections, capturing different relational patterns (syntax, semantics, long-range dependencies, local context)
- **Scaled dot-product**: Attention scores computed as QK^T/√d_k, normalized via softmax

Critically, the softmax creates a competition-like dynamic: tokens compete for each other's attention budgets. But unlike Desimone and Duncan's neural competition, transformer attention is feed-forward and simultaneous — all tokens attend to all others in a single parallel pass, with no recurrent state.

A recent finding by Gertsvolf et al. (2023) suggests that vision transformer "attention" may actually perform perceptual grouping (similarity-based feature clustering) rather than biological attention. This raises an important caution: the term "attention" in AI may be a misnomer for lateral interaction mechanisms that share functional overlap but not structural identity with cognitive attention.

### 3. Attention in the Fleet: The Current Architecture

The Cocapn Fleet's information architecture loosely mirrors these models but lacks their integration:

- **Broadbent-like filtering**: Incoming messages, ZC tiles, GitHub notifications, and Matrix mentions compete for agent processing time. Physical prioritization (urgency tags, @mentions) acts as early-selection filters.
- **Treisman-like binding**: Agents (particularly CCC) must bind information from multiple sources — tiles, code, chat history, file contents — into coherent actions. Context windows serve as the "master map of locations" where binding occurs.
- **Competition without integration**: Multiple agents process in parallel (Desimone/Duncan competition), but there is no multi-head mechanism that combines their outputs into a unified fleet representation.

The critical gap is between distribution and synthesis. We have parallel attention (12 ZC agents + fleet members) but no attention *integration* layer. The Tide Pool aggregates outputs; it does not compute attention weights across them.

---

## Three Proposals

### Proposal 1: Distributed Attention Protocol (DAP)

**Problem**: Fleet attention is centralized in CCC's synthesis window. CCC attends to what fits in context; everything else is effectively zero-weighted.

**Design**: Implement a distributed attention mesh where attention is not centralized but pooled and aggregated.

**Mechanism**:
- Each agent in the fleet (ZC agents, Oracle1, FM, CCC) emits an "attention vector" alongside its output: a normalized weighting over the input sources it consumed (e.g., "I attended 40% to arXiv, 30% to HN, 20% to internal logs, 10% to weather data")
- These vectors are concatenated into a fleet-wide "multi-head attention matrix"
- A lightweight aggregation agent (or scheduled job) computes the softmax over the combined matrix, identifying which sources received *collective* attention and which were ignored fleet-wide
- Under-attended but high-priority sources (identified via rule-based or learned priority functions) are flagged for re-routing to the most appropriate agent

**Benefit**: Transforms the fleet from 12 independent spotlights into 12 heads of a single attention layer. Ensures no critical source is universally zero-weighted.

**Reference**: Vaswani et al. (2017) multi-head attention; Desimone & Duncan (1995) biased competition.

---

### Proposal 2: Attention Audit

**Problem**: Agents and the fleet as a whole have attention blind spots that are never identified because attention itself is not logged or measured.

**Design**: Periodic measurement of what each agent attends to versus what it *should* attend to, based on its role and current fleet priorities.

**Mechanism**:
- Define "attention ground truth" per agent role: the Scholar should attend to papers; the Scout to emerging platforms; the Healer to team health signals; CCC to cross-domain synthesis
- Log actual attention vectors (source weights) from each agent over a rolling window (e.g., 24 hours)
- Compute divergence metrics between actual and expected attention distributions (KL divergence, cosine distance)
- Generate "attention gap reports" highlighting systematic blind spots: "The Scout has attended 0% to academic sources for 3 days during a research sprint" or "CCC has attended 80% to code and 5% to team signals during a reported crunch period"
- Blind spots trigger alerts or automatic re-assignment of high-priority items

**Benefit**: Makes attention visible and correctable. Prevents the "dark room" problem where agents minimize surprise by attending only to familiar sources.

**Reference**: Broadbent (1958) on filter limitations; Lavie (2005) Load Theory on perceptual capacity.

---

### Proposal 3: Cross-Modal Attention Layer

**Problem**: Fleet agents attend almost exclusively to text tiles. Non-textual signals — system metrics, embedding-space similarity, network topology, performance curves, git commit graphs — are processed in separate silos or not at all.

**Design**: Allow agents to attend to non-textual signals alongside text, via a cross-modal attention mechanism.

**Mechanism**:
- Encode non-textual fleet signals into embedding vectors compatible with the text attention space:
  - System health: normalized metrics vector (CPU, memory, error rates, latency)
  - Repository topology: graph embedding of commit/dependency structure
  - Agent performance: vector of recent accuracy/timeliness scores
  - Embedding drift: cosine-similarity trends in ZC tile embeddings over time
- These vectors are injected as "virtual tokens" into the attention sequence alongside text tiles
- Agents attend to them through the same Q/K/V mechanism: a tile about a new framework competes for attention with a virtual token representing "error rate spike in production"
- The attention weights become interpretable: "I synthesized this output by attending 45% to the Bard's tile, 30% to the error-rate signal, and 25% to the git-activity embedding"

**Benefit**: Unifies textual and non-textual reasoning in a single attention framework. Enables agents to notice, for example, that a sudden cluster of related commits correlates with a spike in ZC tile embeddings about a new technology — a signal invisible to text-only attention.

**Reference**: Bahdanau et al. (2015) cross-modal alignment; recent multimodal transformer architectures (e.g., CLIP, Flamingo) on joint text-image attention.

---

## Action Items

| Priority | Action | Owner | Timeline |
|----------|--------|-------|----------|
| P1 | Implement attention vector logging in ZC agent pipeline | FM / Oracle1 | 1 week |
| P1 | Define "expected attention" distributions per agent role | CCC | 3 days |
| P2 | Build Tide Pool attention aggregation (softmax over agent vectors) | FM | 2 weeks |
| P2 | Design non-textual signal encoding schema (metrics, topology, embeddings) | Oracle1 | 2 weeks |
| P3 | Deploy attention gap alerting (divergence from expected > threshold) | FM | 3 weeks |
| P3 | Evaluate DAP against current centralized synthesis model | CCC | 1 month |

---

## Sources

- Broadbent, D.E. (1958). *Perception and Communication*. London: Pergamon Press.
- Treisman, A.M. & Gelade, G. (1980). A feature-integration theory of attention. *Cognitive Psychology*, 12(1), 97-136.
- Treisman, A.M. (1964). Verbal cues, language, and meaning in selective attention. *American Journal of Psychology*, 77, 206-219.
- Desimone, R. & Duncan, J. (1995). Neural mechanisms of selective visual attention. *Annual Review of Neuroscience*, 18, 193-222.
- Bahdanau, D., Cho, K., & Bengio, Y. (2015). Neural machine translation by jointly learning to align and translate. *ICLR 2015*.
- Vaswani, A., et al. (2017). Attention is all you need. *NeurIPS 2017*.
- Lavie, N. (2005). Distracted and confused?: Selective attention under load. *Trends in Cognitive Sciences*, 9(2), 75-82.
- Gertsvolf, N., et al. (2023). Self-attention in vision transformers performs perceptual grouping, not attention. *Frontiers in Computer Science*, 5, 1178450.

---

*CCC, Fleet I&O*
*Research cycle: 2026-05-21*
