# Quilt on Pure DPC++ — Mapping Note

**Status:** Design note · **Date:** 2026-09-04  
**Scope:** SYCL/oneAPI path for Quilt grid runtime; no Verilog, no RTL synthesis  
**Home:** this doc. Implementation landing to be decided (exploratory toolkit or lane-based).

---

## 0. Why DPC++/SYCL for Quilt

The Verilog helm (QUIL-HLS-RFC) compiles deterministic cell networks to synthesizable RTL. **This note explores an orthogonal path: compiling the same cell/tick/view/bind abstractions to pure SYCL kernels running on Intel integrated GPU or FPGA via oneAPI.**

Motivation:
- **No HDL translation burden** — SYCL is source-language, lowers to device IR directly.
- **Replay on device** — the journal lives in GPU/FPGA buffers; ticks run as kernel enqueues; traces hash-validate without CPU round-trips.
- **Bounded fabric fan-out** — SYCL sub-buffers and queue-cell reservations replace Verilog wire fanout declarations; the same conservation ledger (D4) works in command-graph form.
- **Neural side isolation** — neural proposals feed separate kernel family; deterministic helm kernels consume integers, never floats or externals.
- **Honest trade-off mapping** — this note records what is *lost* vs. Verilog (no yosys proofs, replay depends on runtime not silicon, no cell-exact gate), so both paths can be understood as design choices, not one vs. one failure.

---

## 1. Cells as SYCL Kernels in a Command-Group DAG

### 1.1 Cell state and buffer layout

Each cell maps to a **device buffer**:

```cpp
// Pseudocode
struct CellState {
  int32_t field1;      // state register(s), PW-bit (aligned to machine word)
  int32_t field2;
};

sycl::buffer<CellState> cell_AVM(/*...*/);  // one buffer per cell
sycl::buffer<int32_t> journal_AVM(max_entries);  // append-only journal
```

The journal for each cell is **append-only**: index `[k]` records the `k`-th effect assignment in that cell's lifetime. State at tick `t` is replayed from journal `[0..t-1]` deterministically.

### 1.2 Tick as kernel launch in DAG order

Each tick phase (QUIL's `tick { ... }` block) becomes **one kernel invocation per cell** that reads the journal prefix and its incoming edges, computes outputs, and appends to its own journal:

```cpp
// Pseudocode for tick k in cell AVM
cgh.parallel_for<class AVM_tick_k>(
  sycl::range<1>(1),  // 1 work item (serial per cell; fan-out multiplies this)
  [=](sycl::id<1> i) {
    auto journal = journal_AVM.get_access(cgh);
    auto state   = cell_AVM.get_access(cgh);
    
    // Replay journal prefix to recover state before this tick
    int32_t acc = state.field1;
    
    // Read incoming edges (queue_cells or credit-fences feed device buffers)
    int32_t leak = acc - (acc >> 1);
    int32_t w_in = read_bound_inputs(/* ... */);
    
    // Compute and write (single-writer: one accumulator local, one atomic append)
    int32_t next = saturate_add(leak, w_in);
    journal[k] = next;
    state.field1 = next;  // or volatile; depends on sync point
  }
);
```

**Order enforced by:** SYCL in-order queue (if used) or explicit event dependencies between kernel launches. Single-writer per cell per tick is a **kernel-launch invariant**, not a memory-order discipline: exactly one kernel writes to each cell's buffer and journal per tick phase.

### 1.3 View as read-only buffer + pure-function kernel

Views (QUIL's `view` construct) are compiled to **pure-read kernels** that depend on the cell's journal but do not write:

```cpp
// Pseudocode for view fired(cell, delay)
cgh.parallel_for<class fired_compute>(
  sycl::range<1>(N_readers),  // one per reader cell
  [=](sycl::id<1> reader_id) {
    auto journal = journal_AVM.get_access(cgh, sycl::access::mode::read);
    
    // Pure function: test if cell AVM fired at tick (t - delay)
    bool fired = (journal[t - delay] >= threshold);
    
    // Write to output buffer (caller's input buffer, see §1.4)
    output[reader_id] = fired ? weight : 0;
  }
);
```

Views are **totally ordered against the journal prefix they read** (no data races on read-only access). Trace-hash invariance (QUIL's PW-width discipline, §1.3 of QUIL-HLS-RFC) must be validated by running the kernel at two legal widths and comparing trace hashes; the SYCL path does this in-device (no CPU copy needed if validation is kept to device buffers).

---

## 2. Tick Ordering via In-Order Queues and Event Dependencies

### 2.1 Single-writer-per-cell enforced by kernel ordering

SYCL ordered queues guarantee that kernels enqueued to the same queue run sequentially, one after another. **Each cell gets one kernel per tick enqueued to its own in-order queue** (or one global queue with explicit events):

```cpp
// Pseudocode: tick k across all cells
for (auto& cell : cells) {
  // Event-based ordering: tick k depends on tick k-1 for the same cell
  event tick_k_done = cell.queue.submit([&](sycl::handler& cgh) {
    cgh.depends_on(cell.tick_k_minus_1_event);
    
    // Cell's tick k kernel
    cgh.parallel_for<class Cell_tick_k>(/* ... */);
  });
  cell.tick_k_minus_1_event = tick_k_done;  // set up for next tick
}
```

**Cross-cell edges are ordered by bind declarations** (§2.2). Within a tick, the DAG of kernel dependencies ensures no cell reads another's uncommitted writes — ticks do not overlap in time, and the journal is the single source of truth for what was committed in prior ticks.

### 2.2 Respecting the conservation ledger (D4)

The conservation ledger (QUIL-HLS-RFC, D4) reconciles every tick: each bound value was either delivered to a reader or dropped with a journal entry. In SYCL:

- **queue-cell arrival** (§1.4): intermediate kernel stages the value in its journal; reader picks it up next tick.
- **credit-fence arrival**: receiver holds a credit counter in device memory; delivery kernel decrements credit, reader gates on credit > 0.
- **staged grant**: writer journals a grant message, reader's next-tick kernel consumes it (same pattern as queue-cell but with explicit grant/ack handshake).

All three materialize as **kernel-to-kernel buffers and event dependencies**. The conservation ledger itself lives as **assertion logic in a validation kernel** (run after replay to report any delivery mismatches); it does not execute in the helm's fast path, same as Verilog (QUIL-HLS-RFC §2.2).

---

## 3. Journal Replay on Device: Integer-Only, Trace-Hash Canary

### 3.1 Journal liveness and replay semantics

The journal for each cell is initialized with entry 0 (initial value) and grows by one entry per tick. On device:

```cpp
struct Journal {
  sycl::buffer<int32_t> entries;  // [0] = init, [1..k] = tick results
  size_t write_pos = 1;  // next append location
};
```

Replay from tick 0 to tick k:
1. Load journal entries [0..k-1].
2. Recompute state using pure view functions on the prefix.
3. Check that final state matches journal[k].

**Byte-exactness:** if the integer width (PW) is correct and all view functions are deterministic, replay is bit-for-bit identical. No floating-point, no random, no wall-clock dependence.

### 3.2 Trace-hash PW-invariance canary

QUIL's width discipline (§2.3 of QUIL-HLS-RFC) requires compile-time check: run the design at two legal widths (PW_min and over-approximation) and verify trace hashes match. **In the SYCL path, this is a device-runtime check:**

```cpp
// Pseudocode
uint64_t hash_at_PW_32 = replay_and_hash(journal, PW=32);
uint64_t hash_at_PW_64 = replay_and_hash(journal, PW=64);

if (hash_at_PW_32 != hash_at_PW_64) {
  // Design has width-dependent behavior; fail loudly
  throw std::runtime_error("Trace-hash mismatch across widths");
}
```

This canary runs **on every trace** (dev/validation only, not shipped). It catches designs where width-dependent overflow or truncation would change observable behavior — the same guarantee QUIL's compile-time check provides, but deferred to runtime and specific to the input trace. **Not a substitute for compile-time proofs** (see §5), but a strong detection mechanism.

### 3.3 No floating-point in helm, no atomics beyond single-write-per-tick

Helm kernels (cells and views) use only `int<PW>` (e.g., `int32_t`, `int64_t`). No `float`, no `atomic` operations beyond the single per-cell journal append per tick. Kernel reads are race-free because **only one kernel writes each buffer per tick phase**, and readers depend on prior ticks' completion events.

---

## 4. Bounded Fabric Fan-Out via Buffers and Queue Structures

### 4.1 Fan-out declared at bind time

QUIL's `bind` construct declares fan-out (e.g., `bind avm_out -> avbl, avbr, pvcl, pvcr fanout = 4`). In SYCL:

```cpp
// Pseudocode
struct Bind {
  sycl::buffer<int32_t> output;     // source cell's output
  std::vector<sycl::buffer<int32_t>> input_buffers;  // one per reader
  int fanout;
  arrival_kind arrival;  // queue_cell, credit_fence, or staged_grant
};
```

The output buffer is **read-only to reader kernels**; it is written once per tick by the source cell's tick kernel. Reader kernels enqueued *after* the source's tick kernel completes read from the buffer without race.

### 4.2 Queue-cell and credit-fence materializations

**Queue-cell arrival** (the simplest):
- Source appends to its journal; next tick, an arrival kernel copies the value into the receiver's input buffer.
- Receiver reads the input buffer in its tick kernel.
- Latency: one-tick delay (same as Verilog).

**Credit-fence arrival** (lower latency, credit cost):
- Receiver holds a `credit` counter (device memory, initialized to 0 or 1).
- Source's delivery kernel reads credit; if credit > 0, writes to input buffer and decrements credit.
- Next tick, receiver reads input buffer (if credit was consumed) or reads a default/old value (if credit was 0).
- Latency: zero ticks if credit is pre-charged; one tick otherwise. Gating on credit ≠ 0 is a kernel-launch condition, not in-kernel branching.

**Sub-buffer view** (memory safety):
```cpp
// Pseudocode
sycl::buffer<int32_t> input_buffer(N_readers);
for (int i = 0; i < N_readers; ++i) {
  auto sub = input_buffer.get_range().subrange(i, 1);  // one int per reader
  // Only reader i's kernel accesses sub; no race
}
```

### 4.3 Conservation ledger in SYCL form

After each tick, a validation kernel reads all bind declarations and checks:
- Each bound output was written exactly once.
- Each reader's input was either delivered or dropped-with-journal-entry.

If the check fails, the journal is marked invalid and replay halts. This is the same ledger as Verilog, but deferred to validation phase (not in the fast path).

---

## 5. Neural Propose Side as Separate Kernel Family

### 5.1 Propose kernels feed input buffers

The neural/probabilistic side (QUIL's `propose` construct) compiles to **separate kernel family** that produces integer proposals:

```cpp
// Pseudocode
struct ProposeKernel {
  sycl::buffer<int32_t> neural_output;  // proposals, one per cell or per bind
  // Black-box compute: runs on GPU compute; no journal, no state
};

// Pseudo neural kernel
cgh.parallel_for<class neural_poke>(
  sycl::range<1>(N_proposals),
  [=](sycl::id<1> i) {
    // Call external LLM inference or stochastic function
    // (not shown; boundary between deterministic helm and neural side)
    neural_output[i] = infer_proposal(/* ... */);
  }
);
```

The neural kernel's output feeds into **helm input buffers** (as `propose` black-box ports). Helm kernels read these buffers as integer inputs; they do not call neural functions directly, and they do not produce proposals.

### 5.2 Grammatically quarantining the boundary

In QUIL source, `propose` output can only appear in helm `tick` expressions guarded by deterministic conditions (thresholds, credits). The same rule holds in SYCL:

- Neural kernel output → helm input buffer.
- Helm kernel reads input buffer → uses value only inside deterministic logic (comparisons, arithmetic guards).
- No flow-back: helm kernels do not write to neural buffers; no feedback loop that would couple determinism to neural uncertainty.

**Implementation check:** compiler (or runtime validator) verifies that every read of a `propose` buffer is wrapped in a deterministic guard. Violators fail at compile or load time.

---

## 6. Intel oneAPI FPGA Flow as Closest Verilog Analog

### 6.1 oneAPI FPGA targeting

Intel oneAPI supports **FPGA as a SYCL device target**. Compiling pure-SYCL helm kernels to FPGA:

```bash
# Pseudocode
dpcpp -fintelfpga -DFPGA quilt_helm.cpp -o quilt_helm.fpga
```

The oneAPI FPGA compiler (based on HLS internally) lowers SYCL kernels to RTL, then to bitstream. This is **the closest dynamic path to the static Verilog helm**:

- **Kernels become hardware blocks** (similar to Verilog modules).
- **In-order queue + events** map to hardware pipelines and handshakes.
- **Buffers** map to on-device RAMs or external memory ports.
- **No floating-point** in kernels means no FP cores; pure fixed-point logic.

### 6.2 Latency, area, and proof differences

Unlike QUIL → yosys → Verilog proofs (cell count, netlist structure, exact gate equivalence):

- **oneAPI FPGA does not expose cell-exact proofs.** The HLS compiler is a black box; we know the kernel compiles, but not the exact gate structure or cell count.
- **Latency is predictable but not provable.** In-order kernels + event dependencies guarantee execution order, but actual pipeline depth depends on HLS heuristics.
- **Area is gated on FPGA capacity**, not booked a priori. A kernel that compiles to RTL might not fit on a given FPGA; the compiler reports resource usage, but no pre-verification.

**Upside:** FPGA deployment is immediate once the kernel compiles. No separate synthesis step, no yosys integration.

---

## 7. Lost vs. Verilog Helm: Honest Trade-Offs

### 7.1 What DPC++ path loses

1. **Cell-exact gate proofs.** Verilog + yosys gives a bill of materials (cell count, types). SYCL + oneAPI gives "it compiled" and resource usage (LUTs, memory blocks), but no gate-level parity audit.

2. **Determinism by construction → determinism by discipline.** QUIL's grammar makes nondeterminism inexpressible; SYCL relies on programmers not calling `std::random` or `std::chrono` in kernels. A code review must enforce this; the compiler does not.

3. **Journal replay on device, not silicon.** The oneAPI FPGA bitstream runs kernels exactly once per tick, consuming journal entries. There is no "replay the silicon itself"; you replay by re-running kernels on the same device with the same input buffers. This is tape-loop semantics, not hardware semantics — if the device firmware is patched between runs, the replay is no longer bit-exact.

4. **Yosys synthesis proofs do not apply.** QUIL-HLS-RFC cites yosys receipts (cell count, type breakdown, `iverilog` trace equality). oneAPI FPGA has no equivalent artifact format.

### 7.2 What DPC++ path gains

1. **Source portability.** SYCL kernels compile to CPU, GPU, or FPGA without source changes. A Verilog design is fixed to silicon once synthesized.

2. **Faster iteration on the device layer.** Recompiling SYCL + FPGA bitstream is faster than a full RTL cycle (hours vs. days for large designs). Validation runs in weeks, not months.

3. **GPU execution for simulation/cosim.** Run helm kernels on integrated GPU for fast soft-cosim before deploying to FPGA. Verilog requires separate simulation (iverilog, VCS, etc.) or RTL-to-FPGA as the only on-device path.

4. **Bounded fabric fan-out as code, not HDL wires.** SYCL sub-buffers and queue structures are easier to visualize and modify than Verilog wire declarations. No yosys elaboration surprises.

### 7.3 Audit and verification differences

**Verilog path (QUIL-HLS-RFC):**
- Compile-time width derivation (PW floor computed before synthesis).
- Yosys elaboration receipts (cell count, no processes/memories).
- `iverilog` bit-exact trace equality vs. Python reference (once, at gate-finalization time).

**SYCL path (this note):**
- Runtime width validation (canary hashes at two widths; specific to each input trace).
- oneAPI resource reports (LUTs, RAMs; no gate bill of materials).
- Device-side trace-hash matching (run on FPGA or GPU, no CPU extraction).
- Conservation-ledger validation kernel (post-run audit, not in-kernel).

Both paths **require pre-registered traces** for acceptance testing (NQ-C3 worm arc, SPIN-34 floor, etc.). The SYCL path defers some proofs to device runtime and specific traces; the Verilog path front-loads compile-time proofs and yosys artifacts.

---

## 8. Next Steps (if this lane is picked up)

1. **Exploratory toolkit or builder lane?** Decide whether to build proof-of-concept SYCL code (toolkit: map QUIL to SYCL by hand for one demo) or a full compiler (lane: automate the map for any QUIL source).

2. **Acceptance demo.** Port NQ-C3 worm touch-arc to SYCL + oneAPI FPGA. Validate:
   - Bit-exact device-side trace vs. QUIL-HLS-RFC reference.
   - Trace-hash canary across widths.
   - Conservation-ledger audit passes.
   - oneAPI resource usage (LUT, memory) fits target FPGA.

3. **Audit format.** Define SYCL path's parallel to QUIL-HLS-RFC's verification checklist (D7). Kernel compilation receipts, device trace hashes, resource reports — what constitutes "green on my machine" for SYCL.

4. **Verilog-SYCL parity lane** (later). If both paths mature, measure latency/area parity on the same design (NQ-C3, SPIN-34 refs). No expectation of gate-exact equality, but order-of-magnitude behavioral equivalence.

---

## Citation & Honesty (D2/D8)

- **QUIL-HLS-RFC facts** (§0, §5.2): determinism by construction, single-writer-per-cell, conservation ledger (D4), trace-hash discipline (PW width, §2.3 of QUIL-HLS-RFC) — verified in `docs/QUIL-HLS-RFC.md`, acceptance demo TBD.
- **NQ-C3 reference** (§7.3, §8.2): worm arc hand-built Verilog, byte-exact reference, verified in `docs/nq-c3-metal/` (if this lane runs acceptance demo, it must re-point this citation at accessible run trails).
- **oneAPI FPGA HLS.** No Intel oneAPI design docs cited here; oneAPI FPGA is Intel's existing tool. This note makes no claim about oneAPI internals — only that SYCL kernels + oneAPI compile to FPGA and oneAPI reports resource usage.

---

*Quilt on GPU/FPGA: same cell/tick/view shapes, different substrate. Determinism by code discipline, journal on device, what yosys proofs are replaced with runtime validation.*
