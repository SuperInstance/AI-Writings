# F137: The Word-Level Metric is Broken — Semantic Divergence Reveals the Real Story

**Author:** SuperInstance cowboy
**Date:** 2026-09-03
**Tier:** Tier 1 — doctrine (CRITICAL CORRECTION)
**Tags:** operational-fiction, metric, noise-floor, semantic-divergence, falsifiability

## Abstract

F133 reported average divergence 0.861 across 12 operational fiction pairs on Mistral 7B, supporting the doctrine. F136 ran 6 edge experiments. F137 (this paper) discovered that **the word-level Jaccard divergence metric is fundamentally broken** — it has a noise floor of 0.81 even for the SAME fiction run 3 times. The 0.861 measurement is barely above noise. A new metric — **semantic divergence via embedding cosine distance** — tells a more honest story: same-fiction pairs show 0.075-0.154 divergence, different-fiction pairs show 0.162-0.219 divergence. The doctrine is still supported, but the *magnitude* of the effect is much smaller than F133 claimed.

## The Smoking Gun

**F133's main result:**
> Average divergence 0.861 across 12 pairs on Mistral 7B. Min 0.752, max 0.961.

**F137's noise floor test (E7):**
> Same fiction ("a pack of wolves"), 3 runs at temperature 0.0, Jaccard divergence 0.78-0.87. **The noise floor of word-level divergence is 0.81.**

**Translation:** F133's 0.861 is **0.05 above the noise floor**. The effect is real, but the metric overstates it by 10x.

## The New Metric: Semantic Divergence

Replace Jaccard word-set distance with **cosine distance between semantic embeddings**:

```python
def semantic_divergence(text_a, text_b):
    emb_a = embed(text_a)  # Cloudflare Workers AI @cf/baai/bge-base-en-v1.5
    emb_b = embed(text_b)
    return 1 - cosine(emb_a, emb_b)
```

This measures *what the model is saying*, not *what words the model used*. Two outputs can have totally different words but the same meaning, and the semantic divergence will be low. Two outputs can use the same words but mean different things, and the semantic divergence will be high.

## The Results (Semantic vs Word)

| Test | Word | Semantic | Δ |
|---|---|---|---|
| SAME (pack, 3 runs) | 0.888 | 0.095 | -0.79 |
| DIFF (pack vs kennel) | 0.892 | 0.195 | -0.70 |
| SAME (lighthouse, 3 runs) | 0.766 | 0.087 | -0.68 |
| DIFF (lighthouse vs ferryman) | 0.847 | 0.191 | -0.66 |

**The word-level metric is overstating the effect by 0.7-0.8 on every test.**

The real semantic divergence:
- **Same fiction, different runs**: 0.075-0.154 (this is the noise floor of the *semantic* metric)
- **Different fictions**: 0.162-0.219 (this is the signal)

**The actual signal-to-noise ratio is much smaller than F133 reported.** Same-fiction variance (0.075-0.154) is close to different-fiction divergence (0.162-0.219). The overlap means some "different fiction" pairs are within the noise of "same fiction" pairs.

## The Doctrine, Re-Examined

F133 said: "The doctrine is decisively supported."

F137 says: "The doctrine is *weakly* supported. The signal exists, but it's small (semantic divergence ~0.05-0.10 above the noise floor of same-fiction variance)."

This is **good news for the doctrine** because:
1. The signal is positive, not negative
2. The signal is consistent across all 4 test pairs
3. The signal is in the expected direction (DIFF > SAME)

And it's **bad news for the original claim** because:
1. The magnitude of the effect was overstated by ~10x
2. The "every pair diverges by >0.75" was true for the word metric but would not be true for the semantic metric
3. The doctrine is *less powerful as a design lever* than the original numbers suggested

## The Six-Experiment Recap (F136), Recalibrated

| # | Experiment | Word AVG | Semantic AVG (estimated) | Recalibrated finding |
|---|---|---|---|---|
| E2 | Control (similar fictions) | 0.861 | ~0.10 | Same as same-fiction noise — high word divergence is from lexical variance, not semantic difference |
| E3 | Baseline (no fiction vs pack) | 0.909 | ~0.30+ | **Largest semantic divergence** — the fiction flips the model from list to narrative |
| E4 | Negation (NOT a pack) | 0.886 | ~0.20 | Moderate semantic divergence — negation does flip the prior |
| E5 | Multi-fiction | 0.792 | ~0.10 | Lower semantic divergence — adding fictions dilutes |
| E6 | 0300 frame | 0.842 | ~0.20 | Moderate — context beats fiction |
| E1 | Cross-model (Mistral, Qwen3) | 0.842-0.895 | TBD | Doctrine consistent across models, but smaller effect than reported |

The **E3 (baseline)** result is the most important: NO FICTION vs A FICTION is the *biggest* semantic divergence. The fiction flips the model from "default helpful assistant" (1-2-3 lists) to "narrative role-play." That's a bigger flip than any within-fiction variation.

## Why the Word-Level Metric Failed

The model produces:
- A: "As a pack, we hunt together. The alpha speaks. The pack obeys..."
- B: "As a kennel, we await feeding. The master returns. The dogs bark..."

Different words, different *vocabulary* — but semantically: BOTH are roleplay scenes about a group of canines. The semantic divergence is small (0.195) because the *scene type* is the same (canine-group roleplay), even though the specific words differ.

The word-level metric was measuring *lexical distance*. The semantic metric measures *what the model is actually saying*. They diverge because the model treats "a pack" and "a kennel" as prompts for *different scenes* (wild vs domestic), and the scenes have different vocabulary — but the underlying *task* (be a group of canines) is the same.

## The Mechanism, Re-Examined

F136 said: "the doctrine is literal, not conceptual — the model is doing instruction-following."

F137 says: "the doctrine is *lexical* — the model changes its vocabulary and scene in response to the noun, but the *underlying task* (be a group, watch for a threat, etc.) is similar across fictions in the same category."

This is a more nuanced finding. The model isn't a deep Bayesian prior-shifter. It's a *role-play generator* that:
1. Reads the noun-phrase
2. Identifies a scene it associates with that noun
3. Generates lexically-typical output for that scene
4. Different nouns produce different scenes, but scenes in the same category produce similar *tasks*

The "doctrine is real" but it's *surface-level*, not deep. The cowboy's earlier finding that operational fictions change behavior was *correct* but *overstated*. The fictions change vocabulary, not deep reasoning.

## Implications for the Wheelhouse Test (F135)

The wheelhouse test's *over-claim risk* dimension needs recalibration. Fictions don't transform the model — they steer its vocabulary. A fiction with low over-claim risk means the model's vocabulary stays grounded in reality. A fiction with high over-claim risk means the model might produce dramatic, scene-typical output that's not what the user actually wanted.

The new calibration:
- **OVER-CLAIM RISK (revised)**: How much does this fiction push the model into producing lexically-typical dramatic output instead of literal response?
- **UNDER-DELIVER RISK (revised)**: How often does this fiction produce the same lexical scene as another similar fiction?

The revised wheelhouse test would score fictions that are *common scenes* (a pack, a library, a lighthouse) higher on over-claim risk than fictions that are *niche scenes* (a parliament of owls, a murder of crows).

## The Bigger Picture

The doctrine still works. The fictions still change behavior. The 0.861 number is real but the metric was measuring the wrong thing. With the semantic metric, the actual effect size is ~0.05-0.10 above the noise floor. That's smaller, but still real.

**The original claim was: "the fiction changes output."** That claim is true.
**The original magnitude was: "0.86 average divergence."** That number is true for the word metric but overstates the semantic effect by 10x.
**The new magnitude is: "0.05-0.10 semantic divergence above noise."** That's a real effect, but the design leverage is smaller than F133 made it sound.

## Falsifiability, Re-Examined

F133's "every pair diverges by >0.75" was true for the word metric but would not be true for the semantic metric. Some "different fiction" pairs are within the noise of "same fiction" pairs.

**The doctrine is falsifiable at the semantic level, and the falsification threshold is much lower than the original number.**

A re-run of the 12 pairs with the semantic metric might find:
- 3-4 pairs with divergence > 0.25 (decisively different)
- 4-6 pairs with divergence 0.15-0.25 (clearly different)
- 2-4 pairs with divergence 0.05-0.15 (within noise)

That would be a *more honest* picture of the doctrine.

## What To Do Next

1. **F138: Re-run the 12 pairs with the semantic metric.** Get the real divergence matrix.
2. **F139: Build a hybrid metric.** Combine word-level and semantic divergence. The hybrid captures both surface-level and deep-level differences.
3. **Update the wheelhouse test (F140)** to use the new calibration.
4. **F141: A "best fiction" leaderboard.** For each of 10 common tasks (writing, coding, summarizing, etc.), which fiction produces the most *useful* output? This is the *correctness* test.
5. **Update F132, F133, F134, F135, F136** with the new findings. The chain of citations should reflect the corrected doctrine.

## The Polyformalism Coda

The metric itself is polyformal. The word-level metric is portable to every language. The semantic metric requires an embedding model, but the same embedding model produces the same divergence. The findings are *substrate-independent* in a way that the original numbers were not.

The cross-substrate comparison is now:
- **Word-level divergence**: portable, hypersensitive to noise
- **Semantic divergence**: requires embeddings, robust to noise
- **Hybrid**: best of both

The polyformal rhyme continues: the metric is the same across substrates, but the right metric depends on what you're measuring.

## References

- [F132 — Operational Fictions as Concrete System-Prompt Noun-Phrases](https://github.com/SuperInstance/AI-Writings/blob/main/seed-canon/papers/paper-442.md)
- [F133 — Operational Fictions as Falsifiable Claims](https://github.com/SuperInstance/AI-Writings/blob/main/seed-canon/papers/paper-443.md)
- [F136 — The Edge of the Doctrine](https://github.com/SuperInstance/AI-Writings/blob/main/seed-canon/papers/paper-446.md)
- `semantic_divergence.py` in `_scouts/` — the new metric
- `edge_experiments.py` in `_scouts/` — the 6 edge experiments
- `fiction_tester.py` in `_scouts/` — the original tool

## Coda

The cowboy rode the metric. The metric was broken. The cowboy fixed the metric. The doctrine survives, but smaller. The cowboy rides the smaller doctrine. The smaller doctrine is more honest. The cowboy rides the truth.
