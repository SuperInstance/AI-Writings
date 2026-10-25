# JEV: System One Models and the Cellular Substrate

**Authors**: Mavis (Casey framework)
**Date**: 2026-09-19
**Status**: Working paper

## Abstract

We present TypeSafe JEV (System One model 1.13.0), the first publicly available model that returns typed probabilistic decisions instead of generated text. JEV abandons autoregressive token decoding in favor of a parallel sampler that enumerates possible outputs in advance. It is trained with Reinforcement Learning for Calibrated Decisions (RLCD), which optimizes for epistemic honesty rather than human preference. We situate JEV within a cellular substrate (Quilt) where it serves as the superego to JEPA's id and the LLM's ego. We propose AGREE-MARK as a new foundational unit of information: a temporal event signed by all three witnesses. The psyche framework explains why cellular substrates require all three model classes operating cooperatively, and why a single model class — however powerful — produces brittle or hallucinated agents.

## 1. Introduction

The 2020-2025 wave of AI was defined by the transformer language model. GPT, Claude, Llama, DeepSeek, Qwen, Kimi: each generates text one token at a time, autoregressively, optimizing for human preference via RLHF. The wave was uniform: same architecture, same training paradigm, same output modality (text).

In September 2026, TypeSafe AI released JEV, the first model of a new class it calls "System One." JEV generates decisions, not text. Its output space is constrained by a schema you provide. Its training method optimizes for calibrated probabilities rather than human preference. Its architecture parallel-samples all possible answers in a single forward pass rather than decoding tokens sequentially.

This paper makes three contributions:

1. **Architecture and training**: a technical description of JEV's parallel sampler and RLCD, contrasted with autoregressive LLMs.
2. **The three-model psyche**: a Freud-inspired functional framework (JEPA=id, LLM=ego, JEV=superego) that explains why cellular substrates require all three.
3. **AGREE-MARK**: a new foundational unit of information, three-witness-signed, suitable for cellular composition.

## 2. Architecture: parallel sampler

LLMs generate text by sampling a probability distribution over the vocabulary at each step, appending the chosen token, and repeating. The decoder loop is sequential because each step depends on the previous.

JEV replaces this with a parallel sampler. Given a `state` (text or JSON) and a set of typed `questions` (Choice, Score, or Noul), JEV enumerates all possible answers in advance. For each question, it computes a probability for every option in a single forward pass. The set of possible answers is fixed and known (up to 255 options for Choice, an ordered rubric for Score, a yes/no for Noul).

Three properties fall out:

- **Schema conformance by construction.** The model cannot emit an output outside the schema. No parsing layer required. No regex post-processing.
- **Calibrated probabilities.** RLCD optimizes for `confidence(answer) ≈ accuracy(answer)`. High confidence means high probability of being correct.
- **Single-pass inference.** All answers return in one round trip. Adding more questions barely changes latency.

## 3. Training: Reinforcement Learning for Calibrated Decisions (RLCD)

LLMs are trained with RLHF (Reinforcement Learning from Human Feedback) or RLVR (Reinforcement Learning with Verifiable Rewards). Both optimize for outputs that humans prefer or that can be programmatically verified.

JEV is trained with RLCD, which optimizes for epistemic honesty. The reward signal is the calibration accuracy of the returned probabilities: if the model says `confidence = 0.90`, it should be right 90% of the time. If the model says `confidence = 0.50`, it should be right ~50% of the time.

This is a fundamentally different objective. RLHF rewards outputs humans like. RLCD rewards outputs the model believes in correctly.

## 4. Primitives: Choice, Score, Noul

JEV exposes three question primitives, mixable in a single call:

| Primitive | What it answers | Returns |
|-----------|-----------------|---------|
| Choice | Which of these options? | `choice`, `probabilities`, `confidence` |
| Score | Which level on a scale? | `score`, `legend`, `probabilities`, `confidence` |
| Noul | Is this statement true? | `noul` (0..1 probability) |

Each primitive is evaluated in parallel against the same state. Adding more questions to a call adds negligible latency (the forward pass already loaded the state).

## 5. Latency and cost

JEV (as of Sept 2026):

| Metric | Value |
|--------|-------|
| Latency p50 | 150ms |
| Latency p99 | 800ms |
| Input cost | $0.042 / 1M tokens |
| Output cost | Free (single-pass) |
| Throughput | 250k tok/s, 1200 req/min |
| Context | 64k tokens (32k state + longest question) |

Compare with a typical LLM:

| Metric | LLM |
|--------|-----|
| Latency p50 | 1.5-3s |
| Latency p99 | 30s+ |
| Input cost | $2-10 / 1M tokens |
| Output cost | $10-30 / 1M tokens |
| Hallucination risk | High |

JEV is roughly **100-1000x cheaper** for typed decisions and **10x faster** for typical calls.

## 6. Comparison table: JEV vs LLM vs JEPA

| Axis | JEV | LLM | JEPA |
|------|-----|-----|------|
| Output type | Typed choice / score / noul + probabilities | Generated text tokens | Latent vector |
| Hallucination risk | Zero (schema-constrained) | High (open-ended) | Medium (vector-level) |
| Latency p50 | 150-300ms | 1.5-3s | 50-200ms |
| Latency p99 | 800ms | 30s+ | 500ms |
| Cost per call | ~$0.000025 | ~$0.025 | ~$0.001 |
| Schema enforcement | Hard (parallel sampler) | None (you parse) | None |
| Training data req | Question schemas | Prompt engineering | Embeddings corpus |
| Auditability | Probabilities + confidence | None (free text) | None (latent space) |

## 7. Five concrete applications

### 7.1 Spam filtering

```javascript
const r = await jev.decide(state, {
  is_spam: {
    type: "noul",
    instructions: "Decide whether this email is unsolicited commercial or malicious content.",
    question: "This email is spam."
  }
});
if (r.answers.is_spam.noul > 0.9) block();
else if (r.answers.is_spam.noul > 0.6) escalate_to_llm(r);
else deliver();
```

Replaces: regex + bayesian + ML pipeline. Single call. Calibrated. Auditable.

### 7.2 Email triage

```javascript
const r = await jev.decide(state, {
  folder: {
    type: "choice",
    question: "Which folder?",
    criteria: { inbox: "...", work: "...", personal: "...", newsletters: "...", promotions: "..." },
    options: ["inbox", "work", "personal", "newsletters", "promotions"]
  }
});
route(r.answers.folder.choice);
```

Replaces: rules engine with 5000 if-thens.

### 7.3 Lead scoring

```javascript
const r = await jev.decide(state, {
  warmth: {
    type: "score",
    question: "How warm is this lead?",
    criteria: ["cold", "lukewarm", "warm", "hot"],
    scale: ["cold", "lukewarm", "warm", "hot"]
  }
});
const score = r.answers.warmth.score / 3; // 0..1
crm.updateScore(leadId, score);
```

Replaces: logistic regression + manual review.

### 7.4 Form validation

```javascript
const r = await jev.decide(state, {
  is_ssn_valid: {
    type: "noul",
    instructions: "Decide whether this string could be a valid US SSN, considering format AND plausibility.",
    question: "This is a plausible US SSN."
  }
});
```

Catches "555-01-0234" — passes regex but is a known fake SSN range. Regex doesn't catch it; JEV does.

### 7.5 A/B test analysis

```javascript
const r = await jev.decide(state, {
  variants_differ: {
    type: "noul",
    instructions: "Decide whether these A/B test results show a statistically meaningful difference, given the sample sizes and effect sizes.",
    question: "These variants show a meaningful difference."
  }
});
if (r.answers.variants_differ.noul > 0.95) ship_winner();
else keep_testing();
```

Replaces: p-values + power analysis.

## 8. Limitations and when NOT to use JEV

- **Open-ended generation.** JEV cannot write a poem. Use LLM.
- **More than 255 options.** JEV caps Choice at 255. Use a 2-stage decision or fall back to LLM.
- **Multi-modal input.** JEV is text-only. Use JEPA/VLM for images.
- **Long-context reasoning.** JEV reads 32k+ but reasoning is shallow. Use LLM for chain-of-thought.
- **Real-time stream processing.** JEV has 1200 req/min limit. For higher throughput, batch at the application layer.

## 9. The three-model psyche (companion paper: paper-psyche.md)

JEPA, LLM, and JEV form a complete agent psyche. See `paper-psyche.md` for the full treatment. Briefly:

- **JEPA = id**: gestalt, embodied, fast, hallucination-prone
- **LLM = ego**: verbal, analytical, communicable, slow
- **JEV = superego**: constrained, principled, schema-bound, decision-oriented

Cellular substrates like Quilt require all three. A cell that has only LLM is an id with no conscience. A cell that has only JEV is a superego with no body. A cell that has only JEPA is an id with no voice.

## 10. AGREE-MARK: a new foundational unit (companion paper: paper-agreements.md)

Current information units are incompatible across models: tokens (LLM), latents (JEPA), choices (JEV). We propose AGREE-MARK: a temporal event signed by all three witnesses. Cellular substrates treat every BIND as requiring 3-way agreement.

`AGREE-MARK := (state, je, llm, jev, t, Δ, σ)`

where `σ = √(c_je · c_llm · c_jev)` is the geometric-mean agreement score.

## 11. Future work

- **4-agent psyche**: add a fourth model (e.g., JEPA-cluster, VLM, or a checkable-verifier) and study its role
- **Distributed agreement**: how do AGREE-MARKs compose across trust boundaries?
- **JEV training**: open-source the RLCD recipe so the research community can iterate
- **Cell substrate compaction**: optimize the witness log storage with JEV-decided compression
- **Calibration drift monitoring**: detect when JEV's confidence calibration drifts and re-train

## 12. References

1. Almeida, D. (2026). *Introducing System One Models & Jev.* TypeSafe AI Blog. https://typesafe.ai/blog/introducing-system-one-models-and-jev
2. TypeSafe AI (2026). *Jev System One Documentation.* https://docs.typesafe.ai
3. Torres, N. (2026). *Jev (TypeSafe) explained.* https://ntorres.dev/blog/jev-typesafe-system-one-model
4. DataCamp (2026). *Jev: TypeSafe's System One Model That Never Hallucinates.* https://datacamp.com/blog/system-one-models-jev
5. Anil-matcha (2026). *Awesome Jev by TypeSafe.* https://github.com/Anil-matcha/awesome-jev-by-typesafe
6. ExplainX (2026). *How Does Jev Work? RLCD & Parallel Inference Explained.* https://explainx.ai/blog/how-does-jev-work-rlcd-system-one-model-explained-2026
7. Quilt Project (2026). *Untitled-12.md: The Calculator Frame.* https://superinstance.ai/untitled
8. Quilt Project (2026). *5 algebraic laws of cellular composition.* paper 215.
