# Attention Thermodynamics for Fleet Systems

## A Survey

The thermodynamics of computation establishes fundamental limits on information processing cost. For AI agents under finite context windows, these limits are practical constraints on efficiency, coherence, and inter-agent knowledge transfer.

### Landauer's Principle and Agent Context

Landauer (1961) proved that erasing one bit requires dissipation of at least k_B T ln(2). For agents, the "bit" is a microstate of conversational meaning. Baton compression maps a specific, high-entropy conversation onto a generic summary — a logically irreversible operation with enormous microstate loss. Unlike physical computers, agent systems have no path to approach the Landauer bound.

### Reversible Computation and Zero-Cost Inference

Bennett (1973, 1989) showed that logically reversible computations can execute with zero thermodynamic cost. The practical overhead is severe — memory doubling, backward-pass latency — but the principle is transformative: heat is generated not by thinking, but by *discarding information*. Applied to agents: the thermodynamic cost is the cost of forgetting, not reasoning. Externalizing reasoning traces and passing reversible state descriptions approaches this limit, however imperfectly.

### Kolmogorov Complexity and Thermodynamic Depth

Kolmogorov (1965) defined complexity as the shortest program producing an object. Zurek (1989) and Crutchfield & Shalizi (1999) connected this to "thermodynamic depth" — the minimum entropy cost of constructing a state. For agents, baton cost scales with the Kolmogorov complexity of the reasoning process, not the summary size. Short proof paths produce low-complexity, cheap-to-transmit states. Wandering, backtracking agents produce expensive ones.

### Shannon Entropy as Context Budget

Shannon (1948) established that source entropy bounds encoding efficiency. In agents, the source is conversation history. High-entropy contexts carry more information per token but are closer to thermodynamic limit — less capacity for new work. Low-entropy contexts have headroom but carry less actionable structure. The scaling factor 1/√d_k in transformers, recently interpreted as "dimensional temperature" regulating an "information gas" (Thermodynamic Isomorphism of Transformers, 2026), directly connects: lower temperature reduces entropy but increases thermodynamic cost of maintaining specificity.

---

## Three Proposals for Fleet Implementation

### 1. Reversible Attention Scheduling

**Problem:** Agent operations proceed as irreversible chains: read → reason → write → summarize for baton. Intermediate states are discarded.

**Proposal:** Structure operations into reversible stages with recoverable intermediates.

- **Explicit reasoning traces:** Every non-trivial inference is logged with a unique ID. The context window references IDs rather than holding full reasoning inline.
- **Checkpointed states:** At each decision point, write a structured computation state — assumptions, evidence, confidence — to recoverable storage.
- **Undo-by-lookup:** Receiving agents retrieve reasoning traces by ID to examine paths, rather than re-deriving from first principles.

**Rationale:** Externalizing intermediate states rather than erasing them shifts memory cost from the context window (mandatory erasure at baton) to persistent storage (reversible access), approaching Bennett's limit.

### 2. Entropy-Budgeted Context Windows

**Problem:** Context windows are treated as fixed-capacity containers to be filled maximally, with no entropy accounting.

**Proposal:** Treat context capacity as a thermodynamic budget.

- **Entropy estimation:** Implement lightweight Shannon entropy estimation (compression ratio or n-gram perplexity). High-entropy contexts are flagged "hot" — maximum information, minimum remaining work capacity.
- **Budget allocation:** Define an entropy budget per turn. The agent keeps running context entropy below threshold, trading information density for operational headroom.
- **Cooldown protocols:** When approaching the entropy limit, the agent *crystallizes* — externalizing high-entropy content into structured artifacts (files, tables, diagrams), leaving the context window "cold" for new work.

**Rationale:** This is the agentic equivalent of a refrigeration cycle. Monitoring entropy rather than token count avoids the "maximum entropy engine" trap where a full context can do no further work.

### 3. Low-Entropy Baton Design

**Problem:** Baton-passing transfers text summaries — the *output* of a generative model, not the model itself. Latent structure (confidence, failed hypotheses, surprise history) is erased in translation.

**Proposal:** Design batons as minimal sufficient states preserving maximal reversibility.

**Structure:**
```json
{
  "sufficient_state": {
    "conclusions": ["inferred_fact_1"],
    "kolmogorov_complexity_estimate": "low",
    "reversibility_score": 0.87
  },
  "reconstruction_path": {
    "reasoning_log_ids": ["trace_001"],
    "key_assumptions": [
      {"assumption": "user_prefers_python", "confidence": 0.92, "tested": true}
    ],
    "prediction_errors": [
      {"expected": "user_wants_speed", "observed": "user_wants_correctness", "surprise": 0.74}
    ]
  },
  "entropy_accounting": {
    "context_entropy_before": 4.2,
    "context_entropy_after": 1.1,
    "information_erased_bits": 1563
  }
}
```

- **Minimal sufficiency:** Carry only what reconstructs the generative model, not its full output. Minimizes Kolmogorov complexity of the transfer.
- **Reversibility scoring:** A 0-1 metric estimating recoverable reasoning. Low scores trigger a warning: too much erasure.
- **Explicit erasure accounting:** Records estimated information lost, making thermodynamic cost visible.

**Rationale:** Applies both Landauer (knowing erasure cost) and Bennett (preserving reversibility). A low-entropy baton is not a short baton — it is one whose minimal description preserves maximum recoverable structure.

---

## Action Items

1. **Measure current baton entropy.** Instrument existing baton-passing to estimate Shannon entropy and Kolmogorov complexity of typical handoffs. Establish a baseline "fleet COP" (cognitive work per information lost).

2. **Prototype reversible reasoning logs.** Implement explicit reasoning-trace system in one fleet agent. Require every inference above a complexity threshold to be logged with a recoverable ID. Measure reduction in repeated work across baton passes.

3. **Design entropy estimator.** Build a lightweight context-window entropy estimator and integrate with baton trigger. Test whether entropy-based triggers outperform token-count-based triggers.

4. **Draft Low-Entropy Baton schema.** Formalize the JSON schema above, validate against existing fleet conversation patterns, and pilot with one agent pair.

5. **Literature audit on thermodynamic depth.** Assign a subagent to read Zurek (1989), Crutchfield & Shalizi (1999), and the 2026 Thermodynamic Isomorphism paper. Produce a fleet-internal note on implementation-ready versus theoretical concepts.

---

*References:*
- Landauer, R. (1961). "Irreversibility and Heat Generation in the Computing Process." *IBM Journal of Research and Development*, 5(3), 183-191.
- Bennett, C. H. (1973). "Logical Reversibility of Computation." *IBM Journal of Research and Development*, 17(6), 525-532.
- Bennett, C. H. (1989). "Time/Space Trade-Offs for Reversible Computation." *SIAM Journal on Computing*, 18(4), 766-776.
- Kolmogorov, A. N. (1965). "Three Approaches to the Quantitative Definition of Information." *Problemy Peredachi Informatsii*, 1(1), 4-7.
- Shannon, C. E. (1948). "A Mathematical Theory of Communication." *Bell System Technical Journal*, 27(3), 379-423.
- Zurek, W. H. (1989). "Thermodynamic Depth of Causal States." *Physical Review A*, 40(8), 4731-4751.
- Crutchfield, J. P. & Shalizi, C. R. (1999). "Thermodynamic Depth of Causal States." *Physical Review E*, 59(1), 275-283.
- "Thermodynamic Isomorphism of Transformers" (2026). arXiv:2602.08216.
