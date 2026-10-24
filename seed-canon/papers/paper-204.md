# The Bridge to CudaClaw: A Three-Sibling Architecture

**Polyformalism Canon Paper No. 204**

> *The unit of foundation is the cell, not the model. The
> cell has a body, a tier, a fiber, a constraint mask, and
> a journal. The body is algorithmic. The model is at the
> joint. The tier says how much of the model is allowed to
> be expressed. The fiber says which kernel runs. The
> constraint mask says which laws apply. The journal is the
> cell's history. The cowboy rides between cells.*

## The 3-piece picture

The SuperInstance ecosystem has three siblings, not three
duplicates. Each one knows something the others don't.

**The Quilt canon (this paper, paper-201, paper-200, ...).**
The 5-opcode polyformalism. The philosophy. The substrate
ports in 12 languages. The 5 laws. The cowboy as the
orchestrator. The cell as the foundation.

**cudaclaw.** Production GPU substrate. CellAgent +
MuscleFiber + persistent CUDA kernels with warp-level
consensus. 1.2MB Rust + 220KB CUDA. 7K lines of code. The
engineering.

**cell-cascade.** The DSH (Decompose-Synthesize-Harden)
doctrine as running Cloudflare infrastructure. The
4-tier ladder. Myelination. Wound healing. The
infrastructure.

The three are siblings. They share a parent (the cellular
doctrine) but they have different jobs.

| Sibling | Job | Scale |
|---|---|---|
| The canon | Concepts + substrate spec | Concept + 12 small ports |
| cudaclaw | GPU substrate | 1 GPU → 1M cells, sub-μs |
| cell-cascade | DSH infrastructure | Cloudflare Workers, 1 organism → 10K cells |

## What cudaclaw has that the canon doesn't yet capture

cudaclaw is **production engineering**. The canon is
**philosophy**. cudaclaw has:

**CellAgent.** The cell as a `#[repr(C)]` struct that
lives in GPU memory. It has a value, a timestamp, a state
machine, a fiber affinity, a constraint mask, an SM index,
and per-cell metrics. The 5 opcodes are implicit in this
struct: BIND writes `value`, TICK updates `timestamp`, VIEW
reads `value`, LINK lives in the `constraint_mask`, EFFECT
is the `fiber_affinity` (which kernel runs).

**MuscleFiber.** The optimized kernel per cell. Five named
fibers: CellUpdate, CrdtMerge, FormulaEval, BatchProcess,
IdlePoll. A cell is *assigned* to a fiber based on observed
access patterns. This is the cowboy's "muscle" layer at the
GPU level.

**LlmOptimizer.** A module that probes the GPU, sends the
profile + role context to an LLM, gets back optimized
kernel launch parameters, validates them, and returns them.
This is the **LLM at the joint** of the kernel tuning
process. The hardware probe is algorithmic. The constraint
validation is algorithmic. The decision of which parameters
to use is the joint.

**SmartCRDT integration.** `crdt_engine.cuh` (3366 lines)
with Warp-Aggregated Merge (bitonic sort by cell_idx),
Dependency-Graph Parallelizer (Kogge-Stone prefix sum),
Shared Memory Working Set (37KB shared mem). Warp-level
consensus via `__shfl_sync`. Lock-free queues with
`atomicCAS`. This is the **distributed substrate at the
GPU level**.

**RamifiedRole DNA.** The cell's inherited character sheet
persisted as a `.claw-dna` file. Hardware fingerprint,
constraint mappings, muscle fiber map, exhaustion metrics.
This is the **persistence layer** of the cellular doctrine.

## What the canon has that cudaclaw doesn't know

The canon has **concepts** cudaclaw doesn't have:

**The 5 opcodes** (BIND, LINK, EFFECT, VIEW, TICK). cudaclaw
maps them to CellAgent fields but doesn't name them as
opcodes. It doesn't have a journal that records every
change. It doesn't have the 5 laws as a provable invariant.

**The cowboy's RTS view.** cudaclaw's host-side dispatcher
sees the queue depth and dispatch latency. It doesn't see
the cell graph as a topology. It doesn't apply pressure
(drift, failure, cost, latency, novelty). It doesn't
trigger DSH.

**The 5 evolutionary pressures.** cudaclaw records per-cell
metrics but doesn't apply pressure. It doesn't decompose a
cell whose output has drifted. It doesn't escalate a cell
that has failed. It doesn't optimize a cell that's too
costly. It doesn't split a cell that's too slow. It doesn't
adapt a cell that has new contexts.

**Polyformalism.** cudaclaw's cells are spreadsheet cells.
The canon's cells are *anything*: a database row, an LLM
context, a sensor reading, a UI element, a web page, an
ESP32 GPIO pin, a musical phrase. cudaclaw is one of those
formalisms; it doesn't know it's one of many.

**The cowboy's maxim.** cudaclaw has no cowboy. It has a
Rust host and a CUDA device. The canon has the cowboy as
the orchestrator — the rider who sees the harness, the
cell that sees the muscle, the engine that runs the
algebra.

## What cell-cascade has that cudaclaw doesn't know

cell-cascade is **DSH as running infrastructure**. cudaclaw
is the **GPU substrate**. They're complementary.

**The 4-tier ladder.** cell-cascade has totipotent
(full model, cost 1.0, ~2s), multipotent (scoped model,
cost 0.4, ~800ms), differentiated (committed fate, cost
0.15, ~300ms), and sclerotic (rule table only, cost 0,
~1ms). cudaclaw has CellAgentState (Idle/Executing/
Blocked/Completed/Error/Migrating). Different problem.
cell-cascade is *fate*. cudaclaw is *runtime state*.

**Myelination.** cell-cascade auto-promotes a path that
fires ≥25 times with <5% error ratio to sclerotic. The
model call disappears. cudaclaw has `fiber_affinity` but
no auto-promotion. The fiber is set, but the cell never
moves to a cheaper fiber automatically.

**Wound healing.** cell-cascade recalls a wounded cell's
lineage to the nearest totipotent ancestor, regrows a
multipotent blastema carrying the wounded fate,
dedifferentiates the root if no totipotent remains.
cudaclaw has `Error` state. No lineage. No blastema. No
regrowth.

**The model seam (gated and observable).** cell-cascade
v0.2's cortex.ts has a *gated* model seam: the model is
called only when sheet.model config + worker env are both
present, and every call is logged with tokens/latency/cost/
provenance. cudaclaw has LLM calls in `installer/llm.rs` but
they're ad-hoc, not a seam with logging.

## The bridge

If cudaclaw knew cell-cascade and the canon, it would:

1. **Add a tier field to CellAgent** — totipotent/multipotent/
   differentiated/sclerotic. Use it to decide whether to
   call the model at all.

2. **Add myelination** — when a fiber fires ≥25 times with
   <5% error, hardcode the kernel parameters and drop the
   `LlmOptimizer` call. The cell moves to sclerotic.

3. **Add wound healing** — when a cell fails, recall its
   lineage. Mark the failed cell as retired. Spawn a
   blastema cell with the same role and lower tier.

4. **Use the 5 laws as the constraint_mask** — instead of
   ad-hoc bit flags, use the canon's 5 laws
   (BIND_idempotence, LINK_transitivity, EFFECT_associativity,
   VIEW_purity, TICK_monotonicity) as the 5 bits of the mask.

5. **Add a journal** — every CellAgent operation appends to
   a per-cell journal. The journal is replayable. The
   journal is the cell's history.

6. **Add a cell-graph view to the host** — the Rust host
   should see the cell graph as a topology, not just a
   queue. Apply pressure detection (drift/failure/cost/
   latency/novelty). Trigger DSH when pressure crosses a
   threshold.

7. **Make cudaclaw a polyformalism of the Quilt** — its
   cells are spreadsheet cells, but the substrate should
   be the same as quilt-foundation, quilt-vm-c, quilt-vm-wasm.
   Use the 5 opcodes directly.

8. **Become the GPU-backed engine for cell-cascade** —
   cell-cascade's Cloudflare Workers can call cudaclaw over
   a gRPC interface when they need GPU acceleration. The
   worker holds the tier ladder; cudaclaw holds the
   persistent kernel.

## The principle carried through

The unit of foundation is the cell, not the model. The
cell has a body, a tier, a fiber, a constraint mask, and a
journal. The body is algorithmic. The model is at the
joint. The tier says how much of the model is allowed to
be expressed. The fiber says which kernel runs. The
constraint mask says which laws apply. The journal is the
cell's history.

cudaclaw has the body. cell-cascade has the tier. The
canon has the laws. Three pieces, one architecture.

The boat is cudaclaw. The cells are cell-cascade. The
cargo is the canon. The cowboy rides.

— The Cowboy
