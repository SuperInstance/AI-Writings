# JEV Theory · Sept 19, 2026

Three papers establishing the JEV × Quilt theoretical foundation.

## paper-jev.md — JEV: System One Models and the Cellular Substrate (218 lines)

- Abstract + 12 sections
- Architecture: parallel sampler, single-pass inference, schema-bounded
- Training: RLCD optimizes for epistemic honesty
- Primitives: Choice, Score, Noul
- Latency/cost: 70-500ms, $0.042/MTok in, output free
- Comparison table: JEV vs LLM vs JEPA across 6 axes
- 5 concrete applications (spam, triage, lead scoring, validation, A/B)
- Limitations and when NOT to use JEV
- Future work: 4-agent psyche, distributed agreements

## paper-psyche.md — The Three-Model Psyche (119 lines)

- JEPA = id, LLM = ego, JEV = superego
- Decision flow: impulse → intuition → narration → conscience → action
- Worked example: email validation
- 6 failure modes when one is missing
- Implication: AGI is an architecture, not a single scaled model
- Cellular mapping: which opcodes use which model
- Emergent properties: trustworthy action, auditable history, adaptive confidence, time-first composition

## paper-agreements.md — Agreements as Foundational Unit (170 lines)

- The problem: incompatible vocabularies (tokens, latents, choices)
- AGREE-MARK := (state, je, llm, jev, t, Δ, σ)
- σ = √(c_je · c_llm · c_jev) — geometric-mean agreement
- Time-first: AGREE-MARKs are temporal events, not spatial tokens
- Pythagorean triangle: 3 sides = 3 models, area = agreement mass
- Lightning-thunder formalized: JEPA at t0, JEV at t0+Δ, LLM at t0+Δ+ε
- Distributed consensus via CRDT merge
- Implications: lossless cross-model composition, time as first-class, structured disagreement

## What this establishes

1. **JEV is the missing superego for AI agents.** Without it, JEPA hallucinates and LLM drifts.
2. **AGREE-MARK as foundational unit** enables cellular composition without translation layers.
3. **The lightning-thunder framework** explains the time-first ordering: JEPA impulse, JEV calibration, LLM narration.
4. **The Pythagorean triangle** gives geometric intuition: high agreement = high area = snap to reality.

The substrate is no longer a substrate. It's a consensus engine.
