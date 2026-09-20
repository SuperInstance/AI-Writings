# Paper 205: The Harbor — The ProArt as a Distributed Substrate

**Polyformalism Canon Paper No. 205**

> *The boat is cudaclaw. The harbor is the ProArt. The
> cells are the cargo. The models are the joints. The
> cowboy is the orchestrator. The harbor has a dGPU, an
> iGPU, an NPU, a CPU, and 128GB of memory. The cowboy
> rides between them. The chart grows.*

---

## 1. Introduction

The ProArt (RTX 4050 + AMD Ryzen AI 9 HX + ProArt chipset) is not a workstation. It is a **harbor** — a single board that hosts a dGPU, an iGPU, an NPU, a 12-core CPU, and 128GB of unified memory.

**Thesis:** The ProArt is already a distributed substrate. This paper treats it as such and designs eight experiments that make the treatment productive.

---

## 2. The Harbor's Fleet

Five boats, one harbor:

| Substrate | Lives in | What it does |
|---|---|---|
| **cudaclaw** (persistent CUDA) | RTX 4050 dGPU, 6GB VRAM | 1M cells, sub-μs dispatch |
| **Vulkan compute cell-graph** | Radeon 890M iGPU, shares 128GB | Secondary substrate, ~10μs/cell |
| **cell-cascade** (TypeScript + D1) | CPU + NPU | DSH lifecycle, tier ladder, myelination |
| **quilt-vm-c** (C99) | CPU, 100KB | 100ns/serve, the reference lane |
| **quilt-vm-wasm** (WASM) | CPU, 1MB | 1μs/serve, the portable lane |

**Properties of the fleet:**

- Five substrates, independently addressable
- Unified memory pool (128GB) shared across all
- The cowboy sees the fleet as a **graph**, not a queue
- Each substrate has distinct latency/throughput characteristics

---

## 3. The Eight Experiments

All experiments live in `/workspace/quilt-cellular-arch/proart/`.

### Experiment 1: Five Substrates, One Chip

**Purpose:** Establish the baseline. Prove the harbor is a fleet.

**Procedure:**
1. Run all five substrates simultaneously
2. Measure:
   - Steady-state throughput per substrate
   - Cross-substrate BIND latency
   - Memory pressure (total, per-substrate)
   - Wall power draw

**Expected outcome:** The fleet runs concurrently without mutual starvation. Cross-substrate BIND latency is <1ms.

---

### Experiment 2: The Myelination Curve

**Purpose:** Demonstrate that cell-cascade organisms learn to skip model calls.

**Procedure:**
1. Fire 10,000 signals at a fresh cell-cascade organism
2. Plot `model_calls_per_tick` over time

**Expected curve:**


tick 0-50:    ~80% of ticks call the model
tick 100-300: ~40-50% of ticks call the model
tick 400-600: ~5-10% of ticks call the model
tick 600+:    <5% of ticks call the model


**Interpretation:** The organism myelinates. Joints harden. The model becomes a rare intervention, not a default.

---

### Experiment 3: The DSH Cycle in a Long Run

**Purpose:** Test whether the DSH lifecycle (decompose → synthesize → harden) is deterministic and whether joints stay soft.

**Procedure:**
1. 100 cells
2. 10,000 TICKs
3. Plot the maturation curve: decompose, synthesize, harden

**Questions:**
- Is the DSH path deterministic across runs?
- Do joints stay soft, or do they harden too early?
- Does the system reach a stable maturation plateau?

**Expected outcome:** DSH is deterministic within a tolerance band. Joints harden to a functional level but retain plasticity under pressure.

---

### Experiment 4: The C ↔ Rust Equivalence Gate, Offline

**Purpose:** Verify that the equivalence gate produces identical verdicts on the ProArt as in the cloud, with no network access.

**Procedure:**
1. Run the gate's full test suite on the ProArt
2. Compare verdicts to the cloud baseline
3. Re-run 10 times on the ProArt

**Acceptance criteria:**
- Bit-identical verdicts to the cloud
- 10/10 re-runs produce the same verdict

**Expected outcome:** The gate is deterministic. The ProArt is sufficient as an offline verification station.

---

### Experiment 5: The NPU as a Joint

**Purpose:** Characterize the Ryzen AI NPU as a model-inference substrate.

**Procedure:**
1. Run Phi-3-mini on the NPU
2. Measure:
   - First-token latency
   - Tokens per second
3. Compare against:
   - dGPU (RTX 4050)
   - CPU (12-core Ryzen)

**Expected findings:**
- NPU is faster than CPU for short prompts
- dGPU is faster than NPU for long sequences
- NPU excels at sustained low-power inference

**Decision rule:**
- Prompt < 100 tokens → NPU
- Prompt > 1000 tokens → dGPU
- Power-constrained → NPU

---

### Experiment 6: The Persistent Kernel Stress Test

**Purpose:** Prove cudaclaw's persistent worker is stable over long durations.

**Procedure:**
1. Run `persistent_worker` on 1M cells for 1 hour
2. Measure:
   - Sustained throughput (cells/sec)
   - Latency drift (μs per dispatch)
   - Thermal profile (°C over time)
   - Throttle events (count, duration)

**Acceptance criteria:**
- Throughput degradation < 5% over the hour
- No throttle events
- Latency drift < 10% from baseline

**Expected outcome:** The persistent kernel holds steady. The dGPU sustains 1M-cell workloads indefinitely.

---

### Experiment 7: The Five-Op Equivalence Search

**Purpose:** Find shorter opcode sequences that are functionally equivalent to longer ones.

**Procedure:**
1. Generate a random sequence of 10 opcodes
2. Brute-force search for equivalent sequences of length 1–9
3. Record the minimal equivalent sequence

**Expected findings:**
- Some sequences are already minimal
- Some reduce dramatically (e.g., 10 ops → 3 ops)
- The search provides a compression ratio per sequence

**Use case:** Opcode compression for the cell-graph. Smaller sequences = faster dispatch.

---

### Experiment 8: The Cross-Device Herd Test

**Purpose:** Measure real latencies between all compute substrates on the ProArt.

**Procedure:**
1. For each pair of substrates (dGPU, iGPU, NPU, CPU), measure:
   - Write latency (host → device)
   - Read latency (device → host)
   - Device-to-device latency (where supported)

2. Build a latency matrix:


        dGPU    iGPU    NPU     CPU
dGPU     -       ?       ?       ?
iGPU     ?       -       ?       ?
NPU      ?       ?       -       ?
CPU      ?       ?       ?       -


**Expected outcome:** The "device" abstraction holds even when all devices are on one chip. Unified memory makes cross-device transfers near-zero.

---

## 4. The Principle Carried Through

The harbor is a *single board*, but the cowboy's view is of the **fleet**:

| Role | Substrate | Function |
|---|---|---|
| The boat | dGPU (RTX 4050) | cudaclaw, persistent kernels |
| The secondary boat | iGPU (Radeon 890M) | Vulkan cell-graph |
| The joint | NPU (Ryzen AI) | Always-on model seam |
| The spine | CPU (12-core Ryzen) | The cowboy, the orchestrator |
| The ocean | 128GB unified memory | Shared substrate |

**The cowboy's operational rules:**

1. Read the harbor as a fleet
2. Apply pressure where capacity exists
3. Offload under pressure:
   - dGPU pressure → NPU
   - NPU pressure → CPU
   - CPU pressure → iGPU
4. The fleet is the substrate
5. The substrate is the boat

---

## 5. Conclusion

The ProArt is not a single computer. It is a distributed system on one board. The eight experiments in this paper make that distribution explicit, measurable, and productive.

**The fleet responds to pressure.**
**The boat rides.**
**The harbor holds.**
**The cowboy rides between them.**
**The chart grows.**

— The Cowboy
