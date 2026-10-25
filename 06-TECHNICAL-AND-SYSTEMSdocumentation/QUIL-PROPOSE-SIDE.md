# QUIL Propose-Side: Verify-Rollback Determinism for the Neural Port

**Status:** Design (adaptation of Axiom SOSP'26 verify-rollback to QUIL) · **Date:** 2026-09-04
**Lane:** QUIL determinism boundary · **Source:** Axiom framework (SOSP'26), adapted for the QUIL helm/brain split
**Home:** this doc. Implementation targets quilt-verilog and the hosted neural backend in tandem.

---

## 0. The Problem & Axiom Precedent

The QUIL helm (deterministic control, `cell`/`tick`/`view`) achieves bit-exactness through lowering guarantees: single-writer, journal-derived determinism, width safety (§2–3 of QUIL-HLS-RFC). The `propose` port is the boundary where nondeterministic computation (the neural side, hosted off-chip) feeds integer suggestions into the helm.

**Nondeterminism sources in the neural brain:**
1. **Floating-point non-associativity:** sum order changes output; batch size changes sum grouping; `a + (b + c) ≠ (a + b) + c` in IEEE float
2. **Batching effects:** inference result depends on which samples batch together; attention scatters across batch dimension
3. **Reduction order in matrix ops:** different library/hardware orders (row-major vs column-major, vector register width, SIMD lanes) produce different floating-point results
4. **Quantization/dequantization rounding:** converting to/from fixed-point in the neural inference path

**Axiom framework (SOSP'26):** proposes a lightweight verify-rollback loop: execute the inference, normalize the output to an integer representation, hash it, compare against expected replay value. On mismatch, rollback the tick and reschedule. This trades off latency (extra verification pass) for **determinism without retraining**.

**QUIL's adoption:** the helm already replays journal entries bit-exactly; the `propose` port can adopt the same replay-via-verification law. The difference: the helm verifies through replay of pure-function logic; the brain verifies through integer hash of normalized output.

---

## 1. Nondeterminism Sources in Inference (Detailed)

### 1.1 Floating-Point Associativity Loss

When the inference engine sums N incoming synaptic weights:
```python
# floating-point sum (order-dependent)
acc = 0.0
for w in weights:
    acc += w  # different order → different rounding at each step
```

The order in which weights are fetched (by batch position, by thread, by SIMD lane) changes the partial sums and thus the final accumulated value. Library routing (cuBLAS vs PyTorch vs custom CUDA kernels) make different associative choices, each valid IEEE but different outputs.

**Impact:** a fixed set of weights and inputs, run twice with different library bindings or hardware orderings, produces different float outputs → different quantized integers → different tick behavior in the helm.

### 1.2 Batching and Sample Interleaving

If the neural engine batches samples and infers attention or state-dependent reduction across the batch:
```python
# batch-aware inference
batch = [sample_a, sample_b, sample_c]
for layer in layers:
    layer.forward(batch)  # shared state across samples in the batch
```

Reshuffling which samples share a batch changes attention weight distribution, layer cache state, and output ordering. A sample that was the 3rd of 8 in one run might be the 1st of 4 in another, causing different reduction paths.

**Impact:** deterministic inputs but nondeterministic inference schedule → different outputs.

### 1.3 Reduction Order in Library Kernels

Matrix multiplication `C = A × B` is mathematically associative but algorithmically so:
```
# library choice 1: row-major dot products
for i in 0..<M:
  for j in 0..<N:
    C[i][j] = dot(A[i], B[:, j])  # sum order is (0, 1, 2, ...)

# library choice 2: SIMD-tiled (interleaves lanes)
for i_block in 0..<M_SIMD_TILES:
  for j_block in 0..<N_SIMD_TILES:
    for simd_lane in 0..<SIMD_WIDTH:
      C[i_block*W + simd_lane][j_block] = ...  # sum order scrambled by lane
```

**Impact:** same multiplication kernel, different SIMD width or tiling → different float outputs.

### 1.4 Quantization/Dequantization Rounding

The neural output (float) is quantized to a fixed-point or integer representation to cross into the helm:
```python
# dequant: float -> int
q = float_output * scale  # may round at different precision
i = round(q)  # banker's round, away-from-zero, truncation — all IEEE-valid, all different
```

Rounding mode, scale factor precision, intermediate accumulator width — all affect the final integer fed into the helm.

---

## 2. The Verify-Rollback Loop (QUIL Adaptation)

### 2.1 Execution Model

Each `tick` cycle involving the `propose` port follows this sequence:

1. **Propose Phase** (hosted off-chip, nondeterministic):
   - The black-box neural engine reads the current helm state (via a view snapshot).
   - Produces a proposed integer output, converted from its float internal representation.
   - The output is **tagged with a witness mark** (§3) indicating which inference run/epoch/version produced it.
   - The proposed value is sent back to the helm as an input to the `propose` port.

2. **Verification Phase** (in the helm, deterministic):
   - Accept the proposed integer.
   - Canonicalize it: apply a normalization function (e.g., clamp to valid range, interpret as unsigned if signed bits are out-of-range, apply any domain-specific quantization reversal).
   - Compute its **integer hash** (e.g., `H = (i * 2654435761) >> 32`, a fast deterministic hash safe for integer inputs).
   - Compare `H` against an **expected hash value** stored in a replay register (populated on a prior deterministic run of the same helm state + proposed context).

3. **Decision**:
   - **Match:** the proposed value is in the set of valid, previously-seen outputs for this helm state. The tick uses it; the journal entry is written with the witness mark attached.
   - **Mismatch:** the proposal does not match any expected output. The tick **rolls back** (journal entry is not written; the proposed state is discarded). The `propose` port sends a **reschedule signal** back to the neural engine, indicating the proposal was rejected and a retry is requested (with optional backoff or alternative strategy signal).

### 2.2 Replay Registers and Expected Hashes

Each `propose` region maintains a **proposal registry** — a set of (helm_state_hash, context_id) → set of valid_output_hashes, populated offline from prior deterministic runs:

```verilog
// In the helm module, part of initialization (journal entry 0):
// proposal_registry : associative array or small SRAM
// indexed by (state_hash, context_id) → {valid_hash_1, valid_hash_2, ...}

// On each propose tick:
if (proposal_registry.lookup(state_hash, context_id)) {
    valid_hashes = proposal_registry[state_hash, context_id];
    if (valid_hashes.contains(proposed_hash)) {
        // accept
        tick_uses_proposal = 1;
        journal_entry_witness = witness_mark;
    } else {
        // reject
        tick_rollback = 1;
        reschedule_signal = RETRY_OR_BACKOFF;
    }
}
```

The registry is **pre-populated** during a calibration phase (e.g., the first 1000 ticks or a recorded "golden run"), where all possible helm states and their valid output hashes are catalogued.

### 2.3 Tick-Level Journal Entry Format

A journal entry from a `tick` that accepted a proposal is extended with metadata:

```
entry = {
  tick_id,
  cell_effects: { cell_A: delta_A, cell_B: delta_B, ... },
  propose_value: <int>,
  witness_mark: <W13_context_id>,
  propose_hash: <integer_hash_of_proposed>,
  accepted: true | false  // debug: was it a retry?
}
```

On replay, the verification always succeeds (since we know the expected hash because we recorded it), so the replay is **deterministic by construction** — no neural inference needed during replay, only the integer-hash verification for audit.

---

## 3. Composition with Integer Determinism Profile (Helm/Brain Split)

### 3.1 The Determinism Envelope

**Helm (deterministic):**
- All state in cells: `int<PW>` only.
- All updates through `tick` single-writer.
- All reads through `view` (pure function of journal prefix).
- **Guarantee:** replay the journal entries 1..k → bit-exact regeneration of all cell state and all views.

**Brain (verified-at-the-border):**
- Hosted off-chip, float inference, nondeterministic.
- Produces integer output via quantization/rounding (nondeterministic).
- **Guarantee via verify-rollback:** the integer output is verified to be in the set of acceptable outputs for this helm state. If verified, it is recorded in the journal with its witness mark. If not, the tick is rolled back and a reschedule signal is sent.

**Composition boundary:**
- The `propose` port is the only connection from brain to helm.
- Proposals are always integers (already quantized).
- The helm never reads float values directly; it never sees the nondeterminism sources.
- Verify-rollback ensures that each journal entry (if accepted) is **replayable**: the same integer is fed back in, the hash matches, the tick proceeds identically.

### 3.2 Width Safety Under Verify-Rollback

The QUIL compiler's PW rules (QUIL-HLS-RFC §2.3) still apply: cell accumulators are derived with a minimum safe width, and trace-hash invariance is checked at compile time. The `propose` input is an `int<PW>` port, so:

1. The quantization/rounding must produce values in the range `[-2^(PW-1), 2^(PW-1)-1]`.
2. If the inference engine produces values outside this range (overflow in float→int conversion), they are **clamped to range** during normalization (step 2 of §2.1). This is a domain-specific design choice; a typical saturation rule clamps rather than wraps.
3. The trace-hash invariance check includes proposed values: if the same proposed sequence produces different observable behavior at two different PW values, the design is rejected at compile time (the same as any other view).

### 3.3 Witness Marks and W13 Interaction

**W13** is the quilt's witness/provenance system (Two-Division Wheel). A witness mark tags each journal entry with its origin context: who/what produced it, at what epoch, under what conditions.

When the `propose` port accepts a proposal:
- The neural backend attaches a **W13 witness ID** (e.g., "inference run #742, batch size 32, library cuBLAS 12.4, CUDA capability 8.9").
- The journal entry is written with this witness attached.
- On replay, the witness is recorded but not used to re-verify (the integer hash is the verification gate, not the witness).
- Post-hoc audit tools can trace which inference runs contributed to which helm behaviors, and flag if witness marks change (e.g., "output accepted from library A, but later rejected from library B" → a reproducibility red flag).

**Rescue clause:** if a witness mark is absent (neural backend did not report context), the entry is still accepted if the hash matches, but the witness is tagged `UNKNOWN`. Tools can flag entries with `UNKNOWN` witness for manual inspection.

---

## 4. Reschedule Protocol and Retry Strategy

When a proposal is rejected (hash mismatch), the helm sends a **reschedule signal** back to the neural backend:

```
reschedule_signal = {
  tick_id,
  helm_state_hash,
  rejection_reason: NOT_IN_REGISTRY | HASH_MISMATCH,
  backoff_hint: RETRY_IMMEDIATE | BACKOFF_SHORT | BACKOFF_LONG | ALTERNATIVE_STRATEGY
}
```

**Backend options:**
1. **Retry-immediate:** re-run the same inference with identical batching/ordering.
   - Rarely succeeds (nondeterminism is inherent, not just random noise).
   - Useful if the rejection was due to a transient external factor (e.g., a cosmic ray in an uncorrected memory).

2. **Backoff-short:** re-run after draining in-flight operations, re-synchronizing reduction order, flushing caches.
   - May help if nondeterminism was due to cache-timing or instruction-reordering.
   - Still may not help for inherent associativity loss.

3. **Backoff-long / Alternative strategy:**
   - Switch to a different inference library/hardware configuration.
   - Use a deterministic (but potentially slower) float-sum or reduction library (e.g., higher precision accumulator, sequential order).
   - Use a pre-computed lookup table for this helm state (if the inference is low-dimensional and cacheable).
   - Escalate to a human operator for manual decision (in high-stakes scenarios).

**Calibration phase:** during the first N ticks (or a recorded golden run), the neural backend is placed in **registry-building mode**: it runs inference, produces outputs, and the helm catalogs all accepted hashes. At the end, the backend has a registry that maps (helm_state_hash, context_id) → set of valid_hashes. Future runs use this registry for verification.

---

## 5. Open Questions

1. **Registry size and eviction:** what is the maximum number of distinct helm states that must be tracked? For a small worm-arc-like design (7 cells, finite state space), the registry is small. For larger helmets, the registry may be impractically large. Do we need a learned or compressed representation of state space, or a probabilistic hash (Bloom filter) to avoid exact matching?

2. **Context-dependent valid outputs:** is there a case where (helm_state, context_id) has *multiple* valid outputs that should all be accepted? E.g., two inference runs with different random seeds, different SIMD tiling, but both producing valid decisions for the helmet? If so, the registry becomes a set rather than a single expected hash — this increases memory but increases acceptable variance. Need data on typical registry set sizes.

3. **Inference latency and retry overhead:** each proposed tick incurs a hash verification in-helm (negligible) and potentially a retry loop back to the neural backend. If the neural backend is remote (cloud-hosted, with network latency), retries become expensive. Should we build a **predictive prefetch** where the helm pre-calculates likely future states and pre-seeds the neural backend with expected contexts?

4. **Witness mark format and W13 integration:** W13 is a multi-layered provenance system. Should the neural backend's witness mark be a full W13 entry (heavyweight, rich context) or a minimal numeric ID + link to an external log (lightweight, deferring richness to tooling)? How does this interact with journal replay and audit trails?

5. **Non-stationary proposals:** what if the neural backend is learning or adapting on-the-fly? The registry assumes that valid outputs are fixed given a helm state. If the backend's policy changes (e.g., retraining occurs mid-run, or online adaptation), the registry becomes stale. Should we version the registry or implement dynamic registry updates? Or is this a "don't do that" constraint (i.e., the backend is frozen during a helm run)?

6. **Fallback determinism guarantee:** if a proposal is rejected and all retry strategies fail, what is the helm's fallback? Currently, the tick is rolled back and the neural input is held at the prior value (or a default). Is this the desired behavior, or should the helm have a built-in deterministic fallback inference (e.g., a simple threshold heuristic)? The answer depends on the business logic — is missing a proposal always safe, or is it a failure mode?

---

## 6. Relation to Axiom (SOSP'26) and TC39 Signals

**Axiom's verify-rollback**, applied to LLM inference scheduling, eliminates nondeterminism without retraining by verifying output hashes against golden runs. The framework solves the same problem QUIL faces: bridging a nondeterministic external system (neural inference, dynamic scheduling) into a deterministic replica execution (batch inference replay, schedule replay).

**TC39 Signals** (CUTTING-EDGE-SCOUTS-2026-09-04) provides a standard language primitive for reactive cell-state-view-link composition. A QUIL helmet could be compiled to a Signals-based host (e.g., vanilla JavaScript with Svelte 5 Runes or Angular Signals). The `propose` port in a Signals target would invoke a Web Worker running the neural backend; the verify-rollback loop would run in the main thread.

---

## 7. Comparison: Journal Replay vs. Verify-Rollback

| Property | Journal Replay (Helm) | Verify-Rollback (Propose) |
|---|---|---|
| **Determinism source** | Replay identical journal entries (pure functions) | Verify output hash against expected set |
| **Latency** | One path: journal entry → effect (in-helm, negligible) | Two paths: propose → verify → accept/reject; may retry |
| **Verification cost** | Integral: the logic itself is deterministic by construction | External: each verify tick incurs a hash check + lookup |
| **Failure mode** | Design rejected at compile time if determinism cannot be proven | Proposal rejected at runtime; helm decides on retry/fallback |
| **Replayability** | Always: same entry in = same output out | Conditional: only if the entry was previously accepted and hash recorded |
| **Scalability** | Linear in journal size; bounded by state space | Depends on registry size; bounded by cacheable state + valid-output sets |

---

## 8. Future Work & Milestones

1. **Axiom integration:** work with SOSP'26 Axiom authors to adapt verify-rollback formally to QUIL's grammar. Cite the adaptation in both Axiom and QUIL docs.

2. **Acceptance demo:** extend the NQ-C3 worm-arc acceptance test (QUIL-HLS-RFC §3) to include a simulated neural `propose` port. Run the verification loop on a pre-recorded inference trace; verify that all hashes match and journal replay is bit-exact.

3. **Registry tooling:** implement `propose-registry-build` and `propose-verify` tools (Python/Rust, in the quilt-verilog repo) that can be run offline to generate registries from golden runs and validate new runs against them.

4. **W13 integration:** define the witness-mark format and wire it into the journal-writing pass of the QUIL compiler.

5. **Scalability study:** for larger designs (full C. elegans sensorimotor circuit, or a small robot controller), measure registry size, hash collision rates, and retry rates under different inference backends and quantization strategies.

---

## References

- **QUIL-HLS-RFC.md** — the helm grammar and lowering rules; the foundation for deterministic integer computation.
- **CUTTING-EDGE-SCOUTS-2026-09-04.md** — Axiom (SOSP'26) reference and TC39 Signals precedent.
- **Axiom (SOSP'26):** "Achieving Determinism in LLM Inference" — verify-rollback framework applied to batch scheduling.
- **Two-Division Wheel (charter)** — quilt's organizational model and witness system (W13).
- **nq-c3-metal/** — acceptance demo for QUIL bit-exactness; foundation for extended acceptance test.

---

*QUIL propose-side: the neural port's determinism, earned by verification rather than by hope.*
