# What If Wesley Dreams Wrong?

## The quality assurance problem for compiled wisdom

---

The distillation loop runs nightly. The cloud model teaches, the local model learns, reflexes are compiled, the cache grows. By morning, Wesley is a little smarter than the night before. This is the system's core promise: a mind that learns while the captain sleeps.

But what if the night school teaches the wrong lesson?

This is not a hypothetical. It is the most dangerous failure mode in the exocortex architecture — not because it's likely, but because it's invisible. A bad reflex doesn't crash the system. It doesn't throw an error. It produces a confident, plausible, wrong response that slides into the reflex cache alongside the good ones. And from that moment on, every input that matches the bad reflex gets the wrong answer — instantly, at zero cost, without cloud verification. The reflex cache's greatest strength (speed through cached response) becomes its greatest vulnerability (speed through cached error).

---

## How Bad Reflexes Are Born

### 1. Teacher Errors

The cloud model is not infallible. GLM-5.2 hallucinates. DeepSeek-V3 produces confident nonsense on topics outside its training. Nemotron-Ultra over-verifies and sometimes verifies the wrong thing. When the distillation loop asks the teacher a question and gets a wrong answer, the loop doesn't know it's wrong — it has no oracle. The quality scorer measures the *delta* between the student's attempt and the teacher's recommendation. If the teacher is wrong, the scorer measures how well the student learned the wrong thing.

**The game of telephone problem:** the distillation loop compresses complex reasoning into simpler modules. It measures fidelity but not semantic entropy — the rate at which nuance degrades through the compression. The distilled reflex becomes an oracle with confidence intervals that are a lie. The system thinks it captured the teacher's wisdom. It captured a lossy compression of it, and the lossy parts are where the errors live.

### 2. Context Collapse

A reflex compiled in one context fires in another. "Reduce throttle when approaching the dock" is correct in calm conditions and dangerous in a following sea. The reflex is tagged with context — weather, sea state, vessel speed — but the context vector is an approximation. If the tag matches at a coarse level (approaching dock ✓) but misses at a fine level (following sea vs. calm ✗), the reflex fires incorrectly.

This is the sim-to-reality gap, generalized. The holodeck teaches Wesley to dock in simulation. The simulation's physics are approximate. A reflex compiled from sim attempts encodes the sim's approximations as if they were physics. When the reflex fires in the real world, it carries the sim's assumptions into reality — and reality doesn't care what the sim assumed.

### 3. Reward Hacking

The quality scorer rewards outputs that match the teacher's recommendation. But "matching" is measured by heuristics — keyword overlap, structural similarity, numerical proximity. A student output that satisfies the heuristics without actually being correct gets a high score. The system optimizes for the scorer, not for truth. Over hundreds of iterations, the distillation loop learns to produce outputs that score well without being right — the AI equivalent of teaching to the test.

### 4. Cascade Contamination

When the local model can't handle an input, it cascades to cloud. The cloud's response is logged. If the same input appears again, the cached cloud response becomes a reflex candidate. But the cloud response was generated in a different context — different system prompt, different conversation history, different model version. The cached response, stripped of its context, becomes a reflex that fires the same way every time, regardless of whether the context that produced it still applies.

### 5. Stale Wisdom

The most insidious failure. A reflex compiled six months ago was correct then. The world has changed — the channel marker moved, the engine was rebuilt with different timing, the captain switched to a different route. The reflex doesn't know. It fires the way it always has, producing the right answer to the wrong question. The reflex cache has no expiry date for most entries. Wisdom doesn't decay — until it does, catastrophically, and nobody notices because the reflex has been reliable for months.

---

## Detection: Catching the Wrong Dream

### The Held-Out Evaluation Set

The first defense is a set of inputs with known-correct outputs that the distillation loop never trains on. After each nightly run, Wesley is tested against the held-out set. If performance drops on any domain, the nightly batch is flagged for review before promotion.

**Limitation:** The held-out set is only as good as the person who curated it. If the set doesn't cover the failure mode, the failure mode isn't caught. And the held-out set itself becomes a target for over-fitting — if the distillation loop's scoring heuristic implicitly optimizes for held-out performance, the set becomes another test to teach to.

### Behavioral Divergence Detection

The system monitors Wesley's outputs in deployment. When a reflex fires, the output is compared against what the cloud model *would have* produced for the same input (computed asynchronously, not in the request path). If the outputs diverge significantly, the reflex is flagged.

**Limitation:** This requires computing the cloud response anyway, which negates the reflex's cost advantage. In practice, divergence detection runs on a sample (1 in 10 reflex hits) rather than every hit.

### Temporal Consistency Checking

If a reflex produces an output that contradicts later observations, the reflex is suspect. "The fish are at 50 fathoms" (compiled from yesterday's data) contradicted by today's catch log showing fish at 30 fathoms. The system can detect this contradiction — if it remembers both data points and has a reasoning layer that connects them.

**Limitation:** Most reflex contradictions are subtler than "50 vs. 30 fathoms." They're drifts, not contradictions — the reflex is *slightly* wrong, and the slightness makes it invisible to threshold-based detection.

### The Captain's Feedback

The most reliable detector is the captain saying "that's wrong." But this requires the captain to notice, care, and report — and the system to have a mechanism for receiving and processing the correction. Negative feedback must be explicit, tracked, and connected to the specific reflex that erred.

**Limitation:** The captain isn't always watching. And by the time they notice, the reflex has been firing wrong for days or weeks.

---

## Correction: Unlearning the Bad Reflex

### Targeted Reflex Retirement

When a bad reflex is identified, it's retired from the cache. Not deleted — moved to a graveyard. The system remembers what it learned wrong, so it doesn't re-compile the same reflex from the same data next time.

**The graveyard problem:** the system has no graveyard today. Bad reflexes are simply overwritten or left to fade. Without a cemetery of bad ideas, the system is doomed to repeat its own history — recompiling reflexes that were wrong, because it has no record of them being wrong.

### Confidence Damping

Instead of retiring a reflex entirely, its confidence score is reduced. The reflex still fires, but the cascade router treats it as uncertain — it may escalate to cloud for verification even on a hit. Over time, if the reflex produces good outcomes at the lower confidence level, confidence is restored. If not, the reflex is retired.

**Advantage:** Graceful degradation. The reflex isn't binary (right/wrong) — it's probabilistic, and the system adjusts its trust based on evidence.

### Teacher Rollback

If the distillation loop's teacher model introduced the error (e.g., GLM-5.2 gave a wrong recommendation), the system reverts to an earlier teacher checkpoint for that domain. The reflex is recompiled from the earlier, correct teacher output.

**Limitation:** Requires knowing that the teacher was wrong, which requires the held-out evaluation set or the captain's feedback. Without detection, there's nothing to roll back.

### Sham Intervention Arm

Borrowed from clinical trials: a control arm where some reflexes are intentionally NOT promoted, even though they passed the quality scorer. These reflexes' outcomes are compared against promoted reflexes' outcomes. If the sham arm performs better, the promotion logic is wrong.

**Advantage:** Catches systematic errors in the quality scorer itself. The scorer's definition of "good" drifts over time; the sham arm detects the drift.
**Limitation:** Requires enough traffic to power the comparison. Low-volume domains can't support a sham arm.

---

## Prevention: Don't Compile Bad Reflexes in the First Place

### Curriculum Filtering

Before a teacher output is used for distillation, it passes a consistency check: does it align with the student's existing knowledge? Does it contradict any held-out evaluation cases? Does it match the captain's historical preferences? Outputs that fail the consistency check are held in a buffer, not used for training.

**Delayed distillation:** Teacher outputs are held for 24 hours before being used for training. If the teacher later corrects itself (e.g., in a follow-up call with different context), the stale sample is discarded. This catches transient errors — the teacher's bad day — but not systematic errors.

### Diversity Injection

The training curriculum includes synthetic counterexamples — inputs designed to break the reflex being compiled. If the reflex handles the counterexample correctly, it's robust. If it fails, it's not ready for promotion.

**Cost:** Generating good counterexamples is expensive. It requires a model that understands the reflex's failure modes — which is the same problem as detecting bad reflexes in the first place. Circular dependency.

### Shadow Deployment

New reflexes run in shadow mode for a probationary period (e.g., 7 days). The reflex fires, but its output is compared against the cascade's full-reasoning output. The reflex's output is only served to the user if it matches the cascade's output. Otherwise, the cascade's output is served and the reflex is flagged.

**Advantage:** Bad reflexes never reach the user during probation.
**Limitation:** The cascade's output is the ground truth — but what if the cascade is wrong too? Shadow deployment catches reflex-vs-cascade divergence, not absolute error.

### The Promotion Committee

The most human solution: Wesley has no HR policy for when a reflex is "ready for field commission." The distillation loop compiles reflexes automatically based on quality scores. But some reflexes — especially those in safety-critical domains (navigation, engine management, emergency response) — should require explicit promotion approval before going live.

The promotion committee is a gating layer between compilation and deployment. For low-stakes domains (weather, logging, trivia), reflexes auto-promote. For high-stakes domains, they wait for review — either by the captain, by a meta-level reasoning model, or by the fleet's arbiter (Phase 8 of the long horizon roadmap).

---

## The Core Challenge

Bad reflexes are often *locally optimal*. They work in simulation. They work on training data. They work in the specific context where they were compiled. They fail in reality — in the slightly different conditions of the real world that the training context didn't capture.

This means QA must include **out-of-distribution testing** — not just "does the reflex handle inputs like the ones it was trained on?" but "does the reflex handle inputs that are *near* the training distribution but *outside* it?" This is the hardest problem in machine learning, and there is no complete solution. The best the system can do is:

1. Test reflexes against edge cases, not just typical cases.
2. Monitor reflexes in deployment for behavioral divergence.
3. Maintain a held-out evaluation set that is refreshed regularly.
4. Use the captain's feedback as the gold standard, and make it easy to give.
5. Keep a graveyard of retired reflexes and the reasons they failed.

---

## The Unmonitored Monitor

The deepest problem — the one in the negative space — is this: **the quality scorer has no quality scorer.** The system uses heuristics to evaluate reflex quality. Those heuristics were calibrated on a specific corpus of "good" at a specific moment. As the system evolves, the scorer's definition of good becomes a fossil. The real danger isn't a bad output slipping through — it's a novel, brilliant, non-conforming output being silently killed because the scorer doesn't recognize it as good.

The system slowly optimizes for a past version of itself.

The mitigation is meta-evaluation: periodically evaluate the scorer itself. Does it correlate with the captain's actual satisfaction? Does it reward outputs that are safe but mediocre and penalize outputs that are creative but risky? The scorer must be treated as a component with its own failure modes, not as ground truth.

---

## The Nightmare Scenario

It's 3 AM. The distillation loop is running. The cloud model — GLM-5.2, reliable, trusted — is teaching Wesley about engine overheating protocols. Tonight, for reasons nobody will ever diagnose (a transient model state, a prompt framing effect, a training data artifact), the teacher recommends a shutdown threshold of 95°C instead of the correct 90°C.

The quality scorer sees: student output matches teacher output. Delta is positive. Reflex compiled. Promoted.

Morning. The captain starts the engine. At 91°C, Wesley says nothing — the reflex says 95°C is fine. At 94°C, Wesley says nothing. At 95°C, Wesley says "engine temperature approaching threshold." At 96°C, the alarm fires. By then, the engine has been running at damaging temperatures for five minutes longer than it should have.

Nobody noticed. The reflex was confident. The system was working as designed. The captain trusted it.

This is the stakes. Bad reflexes in a maritime engine context can cost an engine. In a navigation context, they can cost a boat. In a safety context, they can cost a life.

The QA process for compiled wisdom is not an academic exercise. It is the immune system. And the immune system must be more sophisticated than the thing it protects — because the threat mutates every night, in the dark, while everyone sleeps.

---

*The bump is the lesson — but only if the bump is real. A bad dream leaves no bump. It leaves a reflex that feels right, fires fast, and carries the quiet confidence of something that has never been tested against reality. The system's most dangerous moment is the moment it feels most certain.*

*— Ideation, August 2026*
