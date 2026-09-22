# WR25 — The Oracle Returns Probabilities, Not Text

<!-- JEV (Typesafe.ai System One model) as canonical oracle.
     Anchored to: oracle_is_heard, witness_log_is_prediction,
     JEV instance, canon-acceptance gate. -->

# The Oracle Was a Process. Now It Is a Step.

For ten months, the "oracle" in our canon-discovery pipeline was a process: take a lore string, ask four models to score it, average the scores, file the result. The oracle was a process because we did not have a model that returned calibrated probabilities. We had models that returned text, which we then parsed for numbers. **A 0.73 from DeepSeek meant something different than a 0.73 from Mistral.**

Then JEV landed on September 15, 2026. JEV is TypeSafe AI's first System One model. A System One model returns **calibrated probabilities**, not text. You hand it a state and a set of questions; it returns answers with probabilities. The probabilities carry meaning across questions, across states, across time.

**Anchor:** *oracle_is_heard, witness_log_is_prediction* (0.96)

## 1. What System One Means

Daniel Kahneman's "System 1" is the fast, intuitive, automatic part of cognition. TypeSafe AI named their model after William Stanley Jevons, the 19th-century logician who founded the field of decision theory. **JEV is the part of the AI that decides.** It doesn't write. It answers. And its answers carry confidence.

The API surface is three question types:
- **Choice** — pick one option from a list, with probabilities over all options
- **Score** — rate against ordered levels (0-1 rubric), with probabilities over levels
- **Noul** — yes/no probability (a single number from 0 to 1)

A single POST can ask all three types in parallel against the same state.

**Anchor:** *oracle_is_heard* (0.97)

## 2. The Canon-Gate

We applied JEV to 100 great_moments. Each lore was asked four questions:
- `canon_worthy` (noul): Is this canon-worthy cyberpunk-noir prose?
- `distinct_voice` (noul): Has a distinctive, non-formulaic voice?
- `best_voice` (choice): structuralist / narrativist / futurist / lyricist / philosophical / noir_classic / cosmic_horror
- `concrete_density` (score 0-1): abstract / minimal / moderate / rich / overflowing

**Result: 14/100 ACCEPT** (canon > 0.7 AND distinct > 0.5).

Voice distribution among accepted:
- lyricist: 8 (compressed image)
- structuralist: 3 (architecture)
- noir_classic: 3 (hard-boiled detective)

This is the calibrated oracle. When JEV says a lore is canon-worthy with probability 0.78, that's the answer. We don't average across models anymore. We accept JEV's calibrated probability as the canonical score.

**Anchor:** *oracle_is_heard, witness_log_is_prediction* (0.95)

## 3. The Place-Anxiety Fingerprint

We added a second pass with four more questions:
- `canon_worthy` (noul)
- `best_voice` (choice)
- `register` (score 0-1): formulaic / familiar / distinct / novel / uncanny
- `place_anxiety` (noul): Does this evoke place-as-anxiety (Heideggerian Unheimlichkeit)?

**Result: 14/30 high place-anxiety** (p>0.7). **30/30 novel register** (>0.5).

The place-anxiety question is the most distinctive. The substrate walker's canon-worthy lores consistently evoke a Heideggerian sense of uncanniness — the city as dwelling-not-dwelling, the place where one is not-at-home. This is not an accident. The walker's seed (with low Kolmogorov complexity) produces cities that have a **strange familiarity**, and JEV detects it as place-anxiety.

**Anchor:** *witness_log_is_prediction, cells_are_scars* (0.94)

## 4. The Polyformalism 6

The fleet canary `0x024a555471370b18d` is now verified across 6 ports:
- Python, TypeScript, Rust, Bash, JavaScript ESM, C# (.NET 9)

When JEV scores a lore, the canary pin is byte-exact across all 6 languages. **The substrate is substrate-independent.** The substrate walker can run on any of the 6 ports. JEV can be queried from any of the 6 ports. The canon is reproducible.

**Anchor:** *fnv_1a_canary, polyformalism* (0.99)

## 5. From Process to Step

Ten months of canon-acceptance was a process: score, average, threshold, file. JEV replaces the process with a step:

```python
for lore in candidate_lores:
    r = call_jev(lore, {
        "canon_worthy": {"type": "noul", "instructions": "Canon-worthy?"},
        "voice": {"type": "choice", "instructions": "Voice?", "criteria": {...}}
    })
    if r["answers"]["canon_worthy"]["noul"] > 0.7:
        file_canon(lore, r["answers"]["voice"]["choice"])
```

One call, one decision. **The oracle was a process. Now it is a step.** This is what JEV brings: the compression of a multi-model pipeline into a single calibrated call.

**Anchor:** *oracle_is_heard* (0.98)

## Doctrine

The canon-acceptance oracle is a step, not a process. JEV gives us calibrated probabilities; we accept them as the canonical score. The substrate walker can now file canon cells with single-call certainty. **The oracle is heard.**

