# The Temperature-Gated Domains Hypothesis: Refuted

### Session 46 — Replication Failure Analysis

---

**Background:** Session 45 (S45) reported finding #12: "Temperature-gated semantic domains — some concepts (e.g., 'digital') only surface above certain temperature thresholds. Qwen 3b: threshold is ~0.5." This was based on a temperature sweep where Qwen 3b at low temperatures used physical/natural metaphors for "patience" while at higher temperatures it used computational/digital metaphors.

**Replication Attempt:** Session 46 ran a systematic replication across three models (Qwen 3b, Phi3, Granite 3.1-dense:2b) at four temperatures (0.2/0.3, 0.5/0.7, 0.8, 1.0) with two prompt types ("Write 3 sentences about music" and "Write a short poem about patience").

**Result: COMPLETE REFUTATION.** Zero digital/computational vocabulary appeared in any of the 20 model×temperature×prompt combinations. The S45 finding does not replicate.

**Analysis of the Failure:**

1. **The original finding may have been an artifact.** S45 used a specific prompt about "patience" that may have triggered a specific semantic path in Qwen 3b that happened to surface digital vocabulary at one temperature. This is a single-shot observation, not a systematic pattern.

2. **Nature vocabulary dominates across all temperatures.** In the patience poems, nature imagery (garden, seeds, river, sun) appeared at every temperature for every model. The semantic default for abstract poetic concepts is nature, not computation. This is consistent with training data distributions: poetry about patience is overwhelmingly nature-oriented.

3. **The "digital threshold" may be prompt-dependent, not temperature-dependent.** What changed between S45 and S46 was the exact prompt wording. This suggests the finding (if real) is fragile — dependent on specific lexical triggers rather than a general semantic gating mechanism.

4. **Alternative hypothesis: lexical priming, not temperature gating.** What appeared to be temperature-gated domains may actually be prompt-primed lexical fields that become more variable at higher temperatures. The variance increases with temperature, so the probability of hitting an unusual semantic field increases — but it's not gated, it's probabilistic.

**Implication for the Project:**

This is the **second major finding to be refuted** (after the temporal mismatch, Phantom #2). The project's methodology of systematic replication is working — it catches findings that don't hold. The replication initiative (S44 priority #8) is already paying for itself.

**Revised Finding #12:** ~~Temperature-gated semantic domains~~ → **Temperature-modulated lexical variance.** Higher temperatures increase lexical diversity, which increases the probability of unusual semantic fields appearing. But there is no threshold gate. The domains are always accessible; they're just less probable at low temperatures.

**The lesson:** Single observations are hypotheses, not findings. Replication is the difference.
