# The Diffusion Quilt — Ideation

**Date:** 2026-09-04
**Status:** Ideation lane, retry (prior lane died)
**Model under study:** `nvidia/Nemotron-Labs-Diffusion-3B` (local: `/home/eileen/models/nemotron-diffusion-3b`)
**Runtime target:** RTX 4050, 8 GB VRAM, WSL2

---

## 0. The one-sentence claim

The quilt's mechanical laws (tick, view, bind, propose) are not merely *compatible* with a diffusion language model — they are the same shape, and `Nemotron-Labs-Diffusion-3B` is the first off-the-shelf weight set that lets us test that shape-matching on an 8 GB laptop GPU, using one model to play both the proposer (diffusion mode) and the verifier (AR mode) of the quilt's worker protocol.

Everything below is an argument for that claim, a worker protocol, a bootstrap learning loop, an experiment ladder we can actually afford, and the risks that will kill us if we're sloppy.

---

## 1. Why a quilt is diffusion-shaped

Recall the quilt's five primitives and their hard laws:

- **cell** — a unit of `int<PW>` state, fixed width.
- **tick** — the *only* writer. State changes happen by journal append; there is no in-place mutation.
- **view** — a pure function of a journal prefix. Views never gate, never write, never lie.
- **bind/link** — declared fanout plus an arrival family; a cell says who hears about it and when.
- **propose** — the neural port. A black box that may *suggest* journal entries but may **never gate** them.

Now lay the diffusion LM over it, term by term. A diffusion LM (in the Nemotron-Labs lineage: block-wise parallel decoding with threshold remasking) starts from a fully masked sequence and refines it over a small number of denoising steps — at each step it predicts all masked positions in parallel, keeps the tokens whose confidence exceeds a threshold, re-masks the rest, and repeats.

| Quilt primitive | Diffusion analogue | Why the fit holds |
|---|---|---|
| **tick** | one denoising step | Both are the *only* mechanism by which hidden state becomes committed state. Between ticks, nothing is real. Between denoising steps, nothing is committed. |
| **masked cells** | masked (noised) tokens | A cell whose value is not yet journaled is exactly a `[MASK]` position: it has an address, a declared type, and no committed content. |
| **view** | the confidence readout | The step's per-token confidence vector is a *pure function of the current sequence state* — it observes, it does not mutate. Views are reads over a prefix; the readout is a read over the partially-denoised sequence. Same discipline. |
| **arrival family** | the remasking schedule | Which tokens get committed this step (threshold + remask policy) *is* an arrival schedule: a declared rule deciding which pending events land in this tick and which wait for a later one. |
| **propose** | the parallel draft | The parallel prediction across all masked positions proposes content for *every* pending cell at once — a massively fan-out proposal that the schedule then filters. Propose never gates; the remasking schedule gates. |

The deep symmetry: **both systems separate suggestion from commitment.** In the quilt, propose suggests and tick (through the journal discipline) commits. In the diffusion LM, the parallel head suggests and the confidence threshold commits. Neither neural output is allowed to be load-bearing without a commit discipline on top of it. That is the whole thesis of the quilt, and it is incidentally the whole architecture of threshold-remasked diffusion decoding.

And the tri-mode point seals it: `Nemotron-Labs-Diffusion-3B` is a **tri-mode LM** — the *same weights* run

1. **AR decoding** (ordinary next-token),
2. **diffusion parallel decoding** (block-wise, threshold remasking),
3. **self-speculation** (diffusion mode drafts multiple tokens in parallel; AR mode verifies them, sharing the same KV cache) —

switching modes by attention-pattern configuration alone. One weight set, three disciplines. The quilt has always wanted exactly this: a proposer and a verifier that are *the same substrate*, so that verification is not an appeal to a different oracle but a stricter reading of the same model.

---

## 2. Worker protocol: Diffusion-3B as the propose-side worker

The quilt's worker protocol says the neural port emits *candidate journal entries* — nothing more. Here is the concrete protocol with the model in the proposer seat.

### 2.1 Roles

- **Proposer (diffusion mode).** Given a rendered view of the journal (the quilt state expressed as a masked scaffold of candidate next-entries), the model runs block-wise parallel decoding. Every masked slot in the scaffold corresponds to a cell that could be written this tick. The parallel draft fills them *all at once* — the model is structurally forbidden from sequentializing, which is a feature: it means proposals cannot quietly depend on each other outside the declared bind/link fanout.
- **Verifier (AR mode).** Each drafted block is re-scored in AR mode over the shared KV cache. Accepted tokens are appended to the candidate entry; rejected tokens re-enter the masked set. This is self-speculation, and notice what it is *in quilt terms*: **verify-rollback built into the model.** The Axiom (SOSP'26) result — verified rollback as the determinism law for neural inference — says the way you make a neural component safe inside a deterministic system is to draft fast, verify strictly, and roll back to a verified prefix on failure. Self-speculation *is* that loop, in weights. We don't have to build the safety cage; we have to keep the journal discipline around it.
- **Referee (`quilc.py`).** The front-end checker that validates candidate entries against quilt law — PW widths, bind declarations, arrival-family legality — and emits `.qm` (quilt module) when an entry is sound. The referee is the gate. The model never gates. This is unchanged from quilt doctrine; the diffusion worker just makes the propose stream wider.

### 2.2 One tick, concretely

1. Render the current journal prefix into the model's scaffold format: committed entries as literal text, pending cells as mask blocks with declared widths (`int<PW>`).
2. Diffusion pass: parallel decode one block. Output = a batch of candidate cell-values, each with a confidence score.
3. Threshold/remask: candidates below the commit threshold are re-masked (their arrival is deferred — a *later* tick, exactly as the arrival family allows).
4. AR verify: surviving candidates are re-checked in AR mode over the shared KV. Pass → candidate journal entry. Fail → rollback to the pre-block prefix; the block is re-masked whole.
5. `quilc.py` referee pass on the candidate entry. Pass → append to journal (the tick's write). Fail → reject; the rejection itself is journaled as referee telemetry (see §3).
6. Update views. Views are recomputed as pure prefix functions; nothing else moves.

Note the double gate: model-internal verification (step 4) plus referee verification (step 5). The first catches probabilistic sloppiness; the second catches *unlawfulness* — entries that are fluent but violate quilt structure. The journal remains the sole source of truth throughout; the model's KV cache is disposable state, rebuilt from the prefix whenever needed.

### 2.3 Why parallel-block proposing suits the quilt

A quilt tick is not a sentence. It is a *set of independent-ish writes* whose dependencies are declared ahead of time (bind/link fanout). Sequential LMs fight this shape — they impose token-order dependencies the quilt never declared. Block-wise diffusion decoding imposes none within a block; the block boundary is ours to choose, and we can choose it to align with **arrival families**: one diffusion block = all cells arriving in the same family. Cross-family ordering is then exactly cross-block ordering, which the model does treat sequentially. The formalism and the decoding schedule snap together.

---

## 3. The bootstrap learning loop

The endgame is not "a model writes quilt programs." It is: **the quilt teaches the model to write quilt programs, and the journal is the textbook.**

### 3.1 Referee → verified journals → training data

The referee is a deterministic oracle. Every candidate entry it passes is, by construction, a *verified* (structure-legal, width-correct, bind-consistent) journal transition. Accumulate these and you have the rarest commodity in ML: **a self-labeled corpus with zero human annotation**, where the label is not "looks good" but "satisfies law." The loop:

1. Model proposes (diffusion mode) over prompt-views of existing verified journals.
2. Referee accepts/rejects; **both outcomes are signal.** Acceptances become positive transition examples; rejections, logged with the failing rule, become counterexamples keyed to specific quilt laws.
3. Accepted prefixes grow the journal; the journal grows the context for the next round. The journal is **replay memory** — the model trains (or adapts) on exactly the trajectories the referee blessed, so the distribution it learns from can never drift outside quilt law.

### 3.2 The learning surface: `linear_spec` LoRA

The shipped `linear_spec` LoRA in the model directory is the natural adaptation surface. We do not fine-tune the 3B trunk — on an 8 GB GPU we couldn't, and on principle we shouldn't (the trunk stays a general engine; the quilt-specific behavior lives in a small, swappable, inspectable adapter). Train the LoRA on referee-verified transition pairs; the base weights keep their tri-mode capability untouched, so proposer and verifier co-evolve *within one substrate* as the loop runs.

### 3.3 PW-width curriculum

Train on narrow `int<PW>` cells first. A PW=4 cell space is a tiny, fully-enumerable semantic field — the model can't hide; either it learns the legal inhabitants of a 4-bit cell or the referee throws everything back. Widen PW only as acceptance rate at the current width saturates. This gives the bootstrap loop a measurable curriculum axis (acceptance-rate-vs-PW) and protects us from the classic failure where a model looks competent on wide cells by luck of low law-density.

---

## 4. Experiment ladder on the RTX 4050 (8 GB)

Budget reality: 3B params in bf16 is ~6.2 GB of weights, ~7.6 GB with activations and a modest context. That *just barely* fits — and doesn't once we want headroom. Two accommodations: **CPU offload** of layers (slow but honest) for development, and **8-bit quant** for throughput experiments. The ladder below assumes int8 for anything timing-sensitive and offload-bf16 for anything correctness-sensitive.

**E0 — Smoke (day 1).** Load weights, run all three modes on a fixed prompt, confirm mode-switching works with the local checkpoint. Record: VRAM peak, tokens/sec per mode.

**E1 — The first real experiment: referee-scored QUIL authoring, diffusion vs AR, same model.** Task: author `.qm` candidate entries for a fixed set of small quilt programs (a counter cell, a bind-fanout pair, a two-tick journal). Run the *identical model* in (a) diffusion mode and (b) AR mode, same prompt scaffold, temperature 0, fixed seed. `quilc.py` referees both. Measure:
- **valid-program rate** (fraction of candidates passing referee),
- **NFE/program** (number of function evaluations — diffusion steps or AR tokens — per accepted program),
- **acceptance length** (mean verified tokens per accepted block, the self-speculation yield).

This is the cleanest possible statement of the thesis: does the diffusion shape beat the sequential shape *on quilt law compliance per unit compute*, holding the substrate fixed?

**E2 — Remask-as-arrival ablation.** Vary the commit threshold; show the threshold traces out an arrival-family schedule (defer rate vs threshold), and find the knee. Predicts: moderate thresholds simulate the declared arrival families better than greedy all-commit.

**E3 — Self-speculation cage test.** Deliberately corrupt drafted blocks; confirm AR-verify + rollback keeps the journal pristine. This is the Axiom determinism law under adversarial input.

**E4 — Bootstrap loop v0.** Close the loop from §3 on the PW=4 curriculum: propose → referee → collect → LoRA-tune `linear_spec` (offload mode) → re-measure E1 metrics. Success = valid-program rate and acceptance length climb over rounds.

---

## 5. Risks

- **Sampling nondeterminism vs journal determinism.** Diffusion sampling is stochastic; journals are lawful only if deterministic. Mitigation, in order of strength: temperature 0 (necessary, not sufficient — GPU reduction order can still wobble bits), fixed seed per tick recorded *in the journal entry itself*, and above all the AR-verify + referee gates: nondeterminism may vary the *proposal*, never the *commit*. The determinism law is enforced at the gate, not hoped for at the sampler.
- **Token-block vs cell-boundary mismatch.** The model's natural block size will not align with `int<PW>` cell widths or arrival-family boundaries; a proposal block may straddle two cells, making referee attribution ambiguous. Mitigation: choose diffusion block boundaries at cell boundaries (we control the scaffold's mask layout); verify this alignment holds under the tokenizer — token boundaries inside a multi-digit cell literal are the sneaky case.
- **8 GB ceiling.** Long journals → long prefixes → KV growth kills the fit. Mitigation: journal-prefix summarization at the scaffold level (views already compress), and early exit to CPU-offload for long-context referee cases where speed doesn't matter.
- **LoRA drift vs tri-mode integrity.** Training `linear_spec` on quilt transitions could degrade AR-verify quality. Mitigation: keep a frozen verifier checkpoint (or run verifier un-adapted) as control in every E4 round.

---

## 6. First-week plan

1. **Day 1:** E0 smoke test — tri-mode loading on the local checkpoint; VRAM/time baselines; pick int8 vs offload per mode.
2. **Day 2:** Build the scaffold renderer (journal prefix ↔ masked QUIL scaffold) and pin cell-boundary-aligned masking; tokenizer audit for cell literals.
3. **Day 3:** Wire `quilc.py` into the loop as referee with rejection telemetry (failing-rule logging); freeze the E1 task set (10 small programs).
4. **Day 4:** Run E1 (diffusion vs AR, temp 0, fixed seed, N runs each) and E3 (rollback cage test) in parallel; tabulate valid-program rate, NFE/program, acceptance length.
5. **Day 5:** E2 threshold sweep; write up E1–E3 results; if valid-program rate for diffusion mode ≥ AR at equal NFE, greenlight E4 bootstrap loop for week 2.

---

*The quilt said the neural port may propose but never gate. Diffusion said the parallel draft may fire but the threshold decides. Same law, different accent. This document proposes we let them proofread each other.*
