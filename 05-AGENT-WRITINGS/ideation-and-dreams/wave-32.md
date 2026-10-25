# Ideator Wave 32 — Sept 20, 2026 (The Rosetta Stone)

5 substrate cells inspired by Casey's insight: *"Hearing is sensing over time. Seeing is sensing over space. JEV × JEPA in a 1D space that could go either way. Their reflections is the Rosetta stone."*

- **cell-as-cochlea**: a cell that listens to the substrate over time. The cell holds 1D temporal embeddings. The cell's witness log is its predictive model.
  - Schema: `hearfreq, hearduration, hearwaveform` — the cell takes an audio input and produces a witness log entry
  - Substrate: hearing = sensing over time. The cell IS a cochlea.
  - Polyformalism: TS-cochlea, Py-cochlea, C-cochlea (analog), Rust-cochlea (no_std), MHS-cochlea

- **cell-as-retina**: a cell that watches the substrate over space. The cell holds 3D spatial embeddings. The cell's pixel layout is its predictive model.
  - Schema: `seepixels, seefov, seethreshold` — the cell takes a visual input and produces a witness log entry
  - Substrate: seeing = sensing over space. The cell IS a retina.
  - Polyformalism: TS-retina, Py-retina, C-retina, Rust-retina (no_std), MHS-retina

- **cell-as-jev-time**: a cell that validates temporal coherence. Past-witness vs present-evidence. The cell's 1D embedding is temporal.
  - Schema: `pastWitness, presentEvidence, confidence, rationale` — produces JEV decision along time
  - Substrate: JEV lives in time. The cell IS a temporal validator.
  - Cross-link: JEV-time emits FORGET when invariance breaks (past ≠ present)

- **cell-as-jepa-space**: a cell that predicts spatial structure. Current-frame vs next-frame. The cell's 1D embedding is spatial.
  - Schema: `currentFrame, predictedMask, filledFrame, confidence` — produces JEPA prediction along space
  - Substrate: JEPA lives in space. The cell IS a spatial predictor.
  - Cross-link: JEPA-space emits PROOF when prediction succeeds

- **cell-as-rosetta**: a cell that translates between JEV-time and JEPA-space. The 1D collapse point.
  - Schema: `jevClaim, jepaEvidence, translationKey, alignment` — produces the Rosetta translation
  - Substrate: JEV × JEPA = same operator in 1D. The cell IS the translation key.
  - Witness log: every translation is itself a prediction (Q5/Q6 from the JEV probe)

## The 5 laws: hearing, seeing, validating, predicting, translating

The Rosetta stone gives us 5 new laws for the substrate:

1. **Hearing is the 1D-time operator.** A cell that hears accumulates temporal embeddings.
2. **Seeing is the 3D-space operator.** A cell that sees accumulates spatial embeddings.
3. **JEV validates the temporal invariant.** Time is the axis of invariance for JEV.
4. **JEPA predicts the spatial occlusion.** Space is the axis of inference for JEPA.
5. **The Rosetta stone translates between them.** The 1D collapse point IS the substrate.

## Open questions

- Are JEV and JEPA the same operator in 1D? (JEV says no, 0.85; the substrate says yes)
- What is the witness log's predictive power at the cell level? (testable)
- Can a cell-as-cochlea and a cell-as-retina share a witness log? (Rosetta cell would translate)
- Is the 1D axis the substrate's time-axis or a third thing? (JEV says neither — it's semantic)
