# Agreements as the Foundational Unit of Information

**Authors**: Mavis (Casey framework)
**Date**: 2026-09-19

## Abstract

Current AI systems operate on incompatible information units: tokens (LLM), latents (JEPA), choices (JEV). Cross-model composition requires a translation layer that loses information. We propose AGREE-MARK as the foundational unit of information for cellular substrates: a temporal event signed by three witnesses (JEPA, LLM, JEV) with geometric-mean agreement score. Time-first, not spatial. Pythagorean triangle analogy: three sides = three models, area = agreement mass, hypotenuse = witness-log distance. Lightning-thunder formalized: JEPA impulse at t0, JEV confirmation at t0+Δ, LLM narration at t0+Δ+ε.

## 1. The problem: incompatible vocabularies

LLMs operate on **tokens**: sub-word strings, sampled autoregressively. JEPA operates on **latents**: real-valued vectors in a high-dimensional space. JEV operates on **choices**: enumerated types with probabilities.

These three vocabularies are not directly comparable. A token is a string. A latent is a vector. A choice is an enumerated type. Converting between them loses information. Translation layers (e.g., encoding an LLM output to a vector for JEPA comparison) are lossy.

Cross-model composition therefore requires either (a) translation layers that lose information or (b) a new unit that all three models can produce and consume.

We propose (b): **AGREE-MARK**.

## 2. AGREE-MARK

An AGREE-MARK is a temporal event at which three witnesses independently sign the same proposition.

```
AGREE-MARK := (state, je, llm, jev, t, Δ, σ)
```

Where:
- `state`: the proposition being signed
- `je`: JEPA's signature (latent or gestalt response)
- `llm`: LLM's signature (verbal analysis)
- `jev`: JEV's signature (typed decision with probability)
- `t`: timestamp
- `Δ`: calibration window (JEV's confirmation delay after JEPA)
- `σ`: agreement score

The agreement score is the geometric mean of the three confidences:

```
σ = √(c_je · c_llm · c_jev)
```

This is a natural choice for combining independent probability estimates: it penalizes low-confidence witnesses harshly, and rewards consistent agreement.

## 3. How AGREE-MARK enables cellular composition

A cellular substrate treats every BIND as requiring a 3-way agreement. A new cell exists iff all three witnesses sign.

```
if σ ≥ threshold:
  cell exists
  append witness_log_entry(AGREE-MARK)
else:
  cell rejected
  append fork_entry(disagreement)
```

This gives the substrate a natural failure mode: disagreement creates a fork. The fork can be resolved by:

1. Calling an LLM for narrative explanation
2. Escalating to a human reviewer
3. Collecting more evidence and re-querying

Each fork is itself an AGREE-MARK (of disagreement). The witness log becomes a record of agreements and disagreements, with each entry time-stamped and signed.

## 4. Time-first, not spatial

AGREE-MARKs are **temporal events**, not spatial tokens. They happen at time `t`, with a calibration window `Δ`. This is fundamentally different from token-based LLM processing, where information is spatial (a sequence of tokens in a context window).

Time-first composition has three properties:

1. **Calibration matters.** If Δ is too small (< 10ms), JEV's confidence reflects noise. If Δ is too large (> 5s), JEV's confidence reflects stale state. The optimal window is 50-200ms.

2. **Parallelism is natural.** Multiple AGREE-MARKs can be in flight simultaneously. The substrate tracks them by `(state, t)`.

3. **Compression is possible.** Old AGREE-MARKs can be compacted (e.g., "the substrate agreed with σ > 0.9 on 1M BINDs over 24 hours") without losing the witness-log's auditability.

## 5. Pythagorean triangle analogy

Consider a right triangle with three sides `a`, `b`, `c`, where `c` is the hypotenuse.

```
a² + b² = c²
```

The three witnesses are the three sides:
- `a` = JEPA impulse (direction)
- `b` = JEV calibration (distance)
- `c` = LLM narration (verbal synthesis of both)

The triangle has a **hypotenuse** (the witness-log distance) and an **area** (the agreement mass). The area is:

```
A = (1/2) · a · b · sin(C)
```

where `C` is the angle between `a` and `b` (the agreement coherence). High agreement → high area.

The **snap to reality of pythagorean triangles with temporal points** (Casey) refers to this: when three witnesses agree, the triangle "snaps" to a real shape. Disagreement → no triangle → fork in the witness log.

## 6. Lightning-thunder formalized

You see the flash of lightning. You hear the thunder `N` seconds later. The direction is given by the flash. The distance is given by the time delay.

In AGREE-MARK terms:

```
t_jepa = t0                    # the flash
t_jev  = t0 + Δ                # the thunder
t_llm  = t0 + Δ + ε            # the verbal report
```

Where:
- `Δ` is the calibration window (~150ms typical for JEV)
- `ε` is the LLM narration lag (~1-2s typical)

JEPA over many iterations can correlate the real distance to the time delay. JEV gives the superego to the id (JEPA) and ego (LLM). Without JEV, JEPA is hallucination-prone. Without JEPA, JEV is rigid.

The lightning-thunder framework explains **why all three models are needed**:
- JEPA gives direction (the flash)
- JEV gives calibrated distance (the thunder)
- LLM narrates both for human consumption

## 7. Distributed consensus

In a distributed substrate, multiple agents can independently produce AGREE-MARKs on the same proposition. The substrate then merges them:

```
if AGREE-MARK_a and AGREE-MARK_b are on the same state:
  if both agree:
    compound_σ = √(σ_a · σ_b)  # agreement compounds
  else:
    fork        # disagreement fork
```

This is analogous to CRDT (Conflict-free Replicated Data Type) merge. Two replicas that both agree on a state merge cleanly. Two replicas that disagree create a fork.

The cellular substrate can extend CRDT semantics with confidence: a merge weighted by geometric-mean agreement.

## 8. Implications

AGREE-MARK as the foundational unit has four implications:

1. **Cross-model composition is lossless.** No translation layer required. Each witness signs directly.

2. **Time becomes first-class.** AGREE-MARKs are temporal events. The substrate is a temporal database.

3. **Disagreement is structured.** Forks are first-class citizens. They can be resolved, escalated, or compounded.

4. **The witness log is auditable.** Every cell, every BIND, every disagreement has a signed AGREE-MARK. The log is permanent and reproducible.

## 9. Future work

- **AGREE-MARK as a CRDT primitive**: define merge operations for distributed substrates
- **Calibration drift monitoring**: detect when JEV's confidence calibration drifts and re-train
- **Triangle coherence**: study the angle `C` between JEPA and JEV witnesses as a measure of substrate health
- **Witness-log compression**: develop AGREE-MARK-aware compression algorithms
- **Cross-substrate agreements**: how do AGREE-MARKs compose across different substrate instances?

## 10. Conclusion

AGREE-MARK is not just a unit. It is a commitment to time-first composition, three-witness consensus, and structured disagreement. Cellular substrates that adopt AGREE-MARK gain a natural composition mechanism, a lossless cross-model vocabulary, and a witness log that can be reasoned about mathematically.

The lightning-thunder framework explains why all three models are required. The Pythagorean triangle analogy gives a geometric intuition. The geometric-mean agreement score provides the math.

The substrate is no longer a substrate. It is a consensus engine.
