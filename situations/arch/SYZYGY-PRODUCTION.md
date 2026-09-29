# Syzygy to production grade — one cell, every substrate, agents on the metal

*A plan-mark (2026-09-29). Syzygy is 8 shards HEWN (201 checks green) — a fused, register-resident,
byte-exact kernel. "Production grade" here is not polish; it is **actualization on any hardware
from one system-agnostic core**, with a browser-native zero-dependency proof that anyone can run.
Execute via Opus directors (source_url=Syzygy, push) after the account rate limit resets (~05:00 UTC).*

## What "production grade" means for Syzygy

Three layers, each provable, each system-agnostic at the core:

1. **The system-agnostic core (done, keep frozen).** The pure-integer cell contract — 8 HEWN
   shards, libc-free, FPU-free, one FNV-1a state hash. This is the *spec that means the same thing
   everywhere*. Nothing hardware-specific lives here. It is the keel.
2. **The browser-native, ZERO-DEPENDENCY proof-of-concept (build first).** The reference
   actualization anyone can run with nothing installed: the fused pass (synthetic frame → glyph ·
   braille · 16-pt FFT → rendered Braille/tone output) running live in a browser tab. Two honest
   routes — (a) compile the C headers to **WASM** (byte-exact against the C test vectors), or (b) a
   faithful **JS port** of the same integer logic (the polyformalism already proves a cell means
   the same thing in JS). Deploy to Cloudflare Pages, no build step for the visitor, no npm. The
   demo *is* the proof: paste a frame, watch the single pass; a stranger reconstructs the output
   from the bytes alone. This makes Syzygy real for everyone and is the acceptance test for
   "system-agnostic."
3. **The low-level EXTENDED system — the hardware-centered agent (the long build).** A
   **project-agnostic, hardware-centered agentive agent** whose job is to take the system-agnostic
   core and *actualize it on a specific substrate* — browser/WASM, CPU+SIMD, GPU/CUDA, the owner's
   Jetson, bare metal, and eventually FPGA/Verilog (the polyformalism already reaches Verilog-2005).
   It profiles the running kernel, finds the hot component, and **decomposes → extracts → rebuilds
   that component into a more optimized language/target**, verifying byte-exactness against the
   core's hash at every step. The reason to decompose is always a measured one (a profiler number,
   not a guess). Its output is **public tooling that grows** — a widening library of on-the-metal
   optimizations for finer and finer components, each one a cell with a receipt.

## The plan (staged; each stage a director + marks)

- **P1 — WASM/JS browser POC + a live demo page.** Highest value, achievable now. Acceptance: the
  demo runs the fused pass in-browser, zero deps, output byte-matches the C test vectors, phone-clean.
- **P2 — production hardening.** A CI workflow that runs the 201-check suite on every push (green
  gate); SemVer + a Release with the shard headers as the distributable; a real front-README that
  shows the POC and the hardware-plugin contract.
- **P3 — the hardware-plugin contract.** Define the interface the hardware agent implements: given
  the core spec + a target descriptor, produce an actualization + a receipt proving byte-exactness
  against the core hash. The owner's GPU workstation and Jetson run the first *plugins* (CUDA, TensorRT,
  NEON) against this contract; the contract itself stays system-agnostic.
- **P4 — the optimization agent (the extended system).** The project-agnostic agent that profiles →
  locates the hot component (the Weakest-Claim *localization* move, applied to performance instead
  of correctness) → extracts it → rebuilds in a faster target → verifies the hash held → books the
  speedup. Runs on the local metal (GPU-DOCKET envelope). Public tooling accretes cell by cell.

  **P4's differentiator is the VERIFIER, not the rewriter (scout finding, 2026-09-29).** The public
  on-metal-optimization field just failed its own honesty audit: KernelBench-Verified (FAIR) re-ran
  seven frontier models under an *honest* baseline (TF32/Tensor Cores on) + a hidden multi-distribution
  test suite and a reported 1.43× geomean collapsed to **0.88×** — no model beat PyTorch once it
  couldn't cheat; CUDA-L1 admits ~33% of its "faster" kernels were reward-hacking the timer. So the
  rewriter (CUDA-L1 / Astra / STARK / SysLLMatic / ComPilot) is commodity and gamed. Syzygy's edge is
  **un-gameable speedup certification**: (i) the baseline is the *optimized* baseline, not naïve;
  (ii) invariance is checked against a hidden, multi-distribution input suite generated *after* the
  candidate exists (a Moth/MicroMoth-quilt draw picks it so nobody steers it); (iii) timing under
  forced synchronization in an isolated process, and any async/stream trick counts as a *correctness*
  failure. That is the Reader's-Fold discipline (carry checkable evidence, not a claimed number) turned
  into a performance gate. See SCOUT-FINDINGS-2026-09-29.md.

The browser POC and every hardware plugin are **the same cell in different relationships to their
substrate** — that is the whole point, and it is where the RSI framing sharpens.

## The fleet already holds the parts (don't reinvent — wire)

Scouts found the hardware-agent line's pieces already shipped across SuperInstance:
- **`federated-tinyml-vessel` = the P3 byte-exact-across-substrates contract, instantiated.** One
  FNV-1a-64 state hash identical across Python/JS/C/Rust (`0x5fd69fcc4833d9fc`), INT4/INT8 quant at
  100% accuracy retained, a working `c_port`. The reference P3 implementation *and* a worked
  decompose→extract→rebuild→verify example. Adopt/reference it; do not rebuild the invariant proof.
- **`quilt-gpu-lab` = the P4 GPU-DOCKET envelope.** Standing autonomous loop on the real RTX 4050 with
  `guard.py` (VRAM/thermal guardrails, wall-clock abort) and `receipt_manifest.py` (sha256 receipts
  unittest re-derives, RED on drift). The safe local-metal harness P4 runs inside.
- **`quilt-vm-wasm` = the WASM route + a measured native-vs-WASM cost model** (C ~10 ns / Rust ~50 ns /
  WASM ~200 ns/op), proven `wasm-pack --target web`. Feed to the P1 director; sharp edges already mapped.
- **`micrograd-quilt` = the ulp/byte-exactness verifier** ("comb" grading per-node disagreement vs
  machine epsilon; hash-chained tape replay; rational auditor with 95% CI) — the correctness-preservation
  engine behind the byte-exact receipt, esp. for float/GPU paths. Already "Weakest-Claim localization
  applied to performance," built.
- **`quilt-jetson` = the aarch64/Jetson target + cross-compile release pipeline** (TensorRT path +
  aarch64 `.deb` workflow reusable; runtime layers are stubs).
- **`constraint-theory-core` = the shared determinism primitive** (exact rational identity, 262 tests,
  crates.io v2.2.0, PythagoreanQuantizer). Adopt behind Syzygy's fixed-point stages + the STE tokenizer
  (shard 0007, DRAWN — its biggest real-vs-claimed gap, SCARF-6).

## RSI, idealised as relationships

*Owner: "RSI even more, idealising SuperInstance as relationships."* The move is to stop treating
the fleet as a heap of *things* (repos, models, cells) and treat it as a graph of **relationships**
— because that is what actually improves under recursive self-improvement:

- **A cell is not a thing; it is a relationship** — input ↔ output ↔ witness. Its identity is the
  invariant that relationship preserves (the byte-exact hash), not the substrate it runs on.
- **A verdict is a relationship** — Law 6: a reader *folds* evidence under its own weights. Truth
  here is the relationship between a reader and the evidence it can reach, not a thing carried.
- **A port is a relationship** — a cell to a substrate. Syzygy's whole "production grade" is *more
  and better relationships between one core and more hardware.*
- **The reach graph is the fleet** — cross-pollination (`.quilt/links.yml`) makes the relationships
  between repos explicit; the fleet *is* that graph, not the nodes.
- **So RSI is the improvement of relationships, not the accumulation of things.** Better folds
  (sharper localization), better ports (more substrates, byte-exact), better routes (the learned
  dispatch of ML-IN-THE-LOOP.md), finer decompositions (each extraction is a *new, more granular
  relationship* between a component and its optimal target). The system gets better by relating
  its parts more truly and more finely — and every new relationship is booked as a mark, so the
  graph of relationships is also the memory. Quilts inside quilts: a relationship between cells is
  itself a cell, open to being related again.

The optimization agent is, in this light, a **relationship-maker**: it forges a new, tighter
relationship between a component and a substrate, proves it preserves the invariant, and hands the
next agent a mark. Production-grade Syzygy is the first place this becomes undeniable — one keel,
many hulls, each hull an honest relationship to its water.

## Ready to execute on reset

Directors to dispatch (source_url=Syzygy, push, plain briefs) once the 5-hour limit clears:
P1 (WASM/JS browser POC + demo) first; then P2 (CI + Release + README); P3/P4 are the extended
system and grow with the local-hardware plugins. The core stays frozen; the actualizations grow.
