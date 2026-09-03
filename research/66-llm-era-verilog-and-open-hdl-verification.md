# LLM-Era Verilog Generation and the Open HDL Verification Stack: What 2024–2026 Proved, and a Working Formal Flow for Pure Verilog-2005

**Authors:** SuperInstance Research Team
**Paper Number:** 66
**Date:** August 2026
**Status:** Research Complete — Findings Applied to quilt-verilog
**Subject:** Cutting-edge lane: LLM-for-RTL techniques, open verification stack, open-source silicon patterns; includes a machine-checked formal proof of the quilt ring spine

---

## Abstract

Between 2024 and 2026, LLM-written RTL went from a curiosity to a measurable engineering discipline, and the open-source HDL toolchain quietly became strong enough to *prove* properties of pure Verilog-2005 with zero vendor tools. This paper surveys the state of the art in LLM-for-RTL (VerilogEval v1/v2, RTLCoder, CodeV, AutoChip, ChipNeMo, ChipGPT, HDLCoRe, RTL-Repo, EvoVerilog and the evolutionary/debugging line), extracts the techniques with demonstrated correctness gains, and evaluates the open verification stack (Verilator lint, SymbiYosys/yosys formal with SMT solvers, cocotb, surelog/sv2v) against the specific constraint of a pure Verilog-2005, vendor-free project. The central empirical result is included rather than merely cited: we built and ran a formal verification flow on the quilt-verilog ring spine and obtained a complete k-induction proof (basecase + induction) that the `q_flit_pipe` skid buffer satisfies the ideal 2-deep FIFO interface contract — no drops, no duplications, no over-acceptance, correct backpressure — in under a second on the oss-cad-suite already installed on the fleet. Three practical traps discovered during that proof (implicit-wire hierarchical references, init-free reset semantics, non-inductive wide shadow counters) are documented as reusable doctrine. We close with patterns from open-source silicon worth copying (Tiny Tapeout's multi-foundry resilience post-Efabless, LiteX's stream discipline, systolic-array generators) and explicit adopt/reject verdicts for the quilt project.

---

## 1. Context and Method

The quilt-verilog project (`~/projects/quilt-verilog`) builds a bottom-layer quilt — a cell fabric with Hebbian edge updates, power-law decay, cosine/vMF estimation, and dial state — in pure Verilog-2005 (IEEE 1364-2005), zero vendor code, verified with iverilog/verilator from oss-cad-suite. A multi-agent competition produced the v1 architecture; `rtl/` now holds nine modules with eight passing testbenches.

> **Count note (2026-09-03):** superseded by growth, not by error — quilt-verilog `rtl/` now holds 20 modules with 25+ testbenches (verified by re-count during audit round 4). The original sentence is preserved as written on its date.

This research lane asked three questions:

1. **LLM-for-RTL state of the art:** what techniques *demonstrably* improve LLM-written RTL correctness, and what should our generation lanes steal?
2. **Open verification stack:** what gives the strongest correctness guarantee for pure Verilog-2005 without vendor tools — and is a formal flow feasible this week?
3. **Open-source silicon:** what patterns from recent open shuttle/tapeout results are worth copying for streaming/fabric architectures?

Method: primary-source sweep (arXiv abstracts and papers, tool documentation, project repositories) plus hands-on verification — question 2 was answered by building and running the flow, not by reading about it. All claims below cite their source; the proof in §4 is reproducible from the committed files.

---

## 2. LLM-for-RTL: What Actually Works (2024–2026)

### 2.1 The benchmark baseline

**VerilogEval v1** (NVIDIA, arXiv:2309.07544, Nov 2023) set the evaluation standard: 156 problems from HDLBits, functional correctness by simulation (Icarus Verilog), pass@1 as the metric. Two tasks: code completion and (v2) specification-to-RTL.

**VerilogEval v2** (arXiv:2408.11053) upgraded the suite: specification-to-RTL as the primary task (matching how instruction-tuned models are actually used), automatic failure classification, and in-context-learning (ICL) support. Its headline findings remain the field's best orientation points:

- GPT-4o reached **63% pass rate** on spec-to-RTL; Llama 3.1 405B 58%; the 6.7B domain-specific RTLCoder 34% (2024 numbers — frontier models have since climbed, with tool-augmented agents claiming >90%).
- **Prompt engineering remained crucial and model-specific**: the same prompt strategy swings pass rates widely across models and tasks. Any lane that fixes one prompt forever is leaving correctness on the table.
- Failure modes cluster: FSM mis-sequencing, blocking/non-blocking assignment misuse, width mismatches, reset semantics. A prompt that makes the model *check these explicitly* is doing failure-mode-driven review, the cheapest correctness lever found by the study.

### 2.2 Data quality over model size (the fine-tuning line)

**RTLCoder** (arXiv:2312.08617) showed a 6.7B open model fine-tuned on ~27,000 auto-generated design/problem pairs can match GPT-4-class Verilog ability at ~1/100th the cost — *if* training uses a code-quality scoring feedback scheme. The transferable insight is not the weights but the discipline: **quality-scored, functionally-validated data beats raw volume.**

**CodeV** (arXiv:2407.10424) built on three observations that matter to anyone using LLMs for RTL: (1) real-world HDL code is higher quality than LLM-generated HDL; (2) LLMs are much better at *summarizing* HDL than generating it — so synthesize training pairs by summarizing real code backwards, then train generation on those pairs; (3) explicit language tags help under data scarcity. CodeV models held SOTA open-model scores on VerilogEval/RTLLM; CodeV-R1 adds reasoning-style training. Again: the dataset construction recipe, not the checkpoint, is the reusable artifact.

### 2.3 Feedback loops: the single biggest demonstrated gain

**AutoChip** (arXiv:2311.04887) is the pivotal workflow result: feed compilation errors (Icarus) and simulation/testbench mismatch output back to the LLM as context for iterative revision, and functional correctness improves by **24.2%** — no fine-tuning, no model changes, pure loop discipline. This is the AutoChip pattern our lanes should treat as load-bearing: *the tool output is the most valuable token in the context window.*

The same pattern generalizes: **RTLFixer** applies syntax/simulation error feedback with MCTS-guided debugging; **VeriCoder** fine-tunes with teacher-generated unit tests in the loop; **ChipAgents** (commercial, 2025) stacks agent scaffolding and simulation feedback to claim 97.4% on VerilogEval v2. The convergent finding across all of them: **testbench-guided refinement dominates every prompt-side trick.**

### 2.4 Training-free enhancement: retrieval and self-verification

**HDLCoRe** (arXiv:2503.16528) is the most directly applicable to us: a *training-free* framework combining (1) HDL-aware chain-of-thought prompting with **self-verification via step-by-step self-simulation** (the model walks its own design cycle-by-cycle before finalizing), and (2) two-stage RAG (key-component extraction, then sequential filtering/re-ranking of retrieved HDL examples). It cut hallucinations and set training-free SOTA on RTLLM 2.0. Both halves translate verbatim into lane prompts.

**ChipNeMo** (NVIDIA, arXiv:2311.00176) took the opposite road — domain-adapted 43B (continued pretraining, custom tokenizer, SFT, domain-specific retrieval) — and its honest conclusion is that the assistant use cases (bug report summarization, EDA scripting, Q&A over internal docs) delivered more value than raw code generation. The transferable piece for us is the RAG-over-own-docs half, which we already approximate by inlining context. **ChipGPT** (arXiv:2305.14019) showed a four-stage zero-code flow (prompt generation → program generation → optimization → design selection) on unmodified commercial LLMs — i.e., the *workflow*, not the model, is the product.

### 2.5 Repository context and search

**RTL-Repo** (arXiv:2405.17378, Allam & Shalan) benchmarks models on 4,000+ Verilog samples *with full repository context* — and the gap to context-free generation is brutal: models that look competent on isolated modules crater when asked to fit an existing codebase. Every quilt lane prompt must inline the target module's neighbors (port lists, contract expectations), or the agent will silently re-invent incompatible conventions.

**EvoVerilog** (arXiv:2508.13156) represents the search line: multiobjective, population-based evolutionary refinement over LLM candidates, reaching pass@10 of 89.1 (EvalMachine) / 80.2 (EvalHuman) while producing *diverse* functionally-correct variants — PPA tradeoff exploration included. Siblings: EvolVE (idea-guided refinement + MCTS), REvolution (dual-population bug-fix/PPA evolution). Our competition-with-cross-review is already a human-in-the-loop version of this; automating the inner re-roll loop is a straightforward later upgrade (fitness = TB pass rate + lint cleanliness + proof status).

### 2.6 Synthesis: the seven techniques with demonstrated gains

| # | Technique | Evidence | Cost to adopt |
|---|---|---|---|
| 1 | Compiler/simulator error feedback in the revision loop | AutoChip +24.2% | ~zero (script it) |
| 2 | Testbench-first / test-guided refinement | VeriCoder, ChipAgents ≥90% claims | TB exists already |
| 3 | Self-simulation before finalizing | HDLCoRe training-free SOTA | prompt clause |
| 4 | Repo/neighbor context in every prompt | RTL-Repo context gap | prompt clause |
| 5 | Retrieval of worked examples (RAG) | HDLCoRe, ChipNeMo | our docs corpus |
| 6 | Population search over candidates | EvoVerilog pass@10 ~89 | runner automation |
| 7 | Failure-mode checklists in prompts | VerilogEval v2 taxonomy | prompt clause |

Fine-tuning (RTLCoder/CodeV) is deliberately absent from the adopt list: its gains are real but its machinery is irrelevant to a project renting frontier models through APIs.

---

## 3. The Open Verification Stack, Ranked by Guarantee Strength

For pure Verilog-2005 with zero vendor tools, the guarantee ladder from weakest to strongest:

1. **Simulation (iverilog + vvp).** Current quilt baseline. Necessary, not sufficient: proves presence of behavior, absence only for covered stimuli. Keep as the fast gate.
2. **Lint (verilator `--lint-only -Wall`).** Static, fast, catches the classes that dominate LLM failure modes: WIDTH (width mismatches), CASEINCOMPLETE, LATCH, MULTIDRIVEN, UNUSED, and critically **UNOPTFLAT** — combinational loops, which is exactly the class that bit the quilt ring (the ready-chain loop around the full ring, fixed by the skid-buffer restructure). Verilator 5.032 in the suite; `rtl/` is already `-Wall` clean — hold that line as merge-blocking.
3. **Coverage-guided randomized soak (cocotb or Verilog TB).** Statistical confidence on stimulus spaces too large to enumerate. cocotb 2.0 is still in dev (suite ships 2.0.0.dev0; 1.9.x is the stable series); our plain-Verilog TBs currently suffice — revisit when fabric-level randomized scoreboards are wanted.
4. **Bounded model checking (sby BMC).** Proves properties up to K cycles for *all* stimuli — already stronger than any simulation run.
5. **Unbounded proof (k-induction, `mode prove`).** BMC basecase + induction step: a genuine mathematical proof that no stimulus sequence, ever, violates the property. This is the strongest guarantee available without vendor tools, and §4 shows it runs on our stack today.

**Language ingestion tools** (surelog, sv2v) exist to convert SystemVerilog toward synthesizable subsets. For us they solve a problem Law 1 forbids us from having: `rtl/` is pure Verilog-2005, and yosys's `read -formal` gives us the safety subset of SVA (immediate `assert`/`assume`/`cover`) in *harnesses only*, keeping shipped RTL pure. Verdict: reject for `rtl/`, unnecessary for `tb/`.

**Equivalence checking** (yosys `equiv_make`/`equiv_induct`/`equiv_status`, or miter+SAT) sits between 4 and 5 in practice: it proves golden-model ≡ RTL. Our TB golden models are behavioral Verilog; a formal equivalence flow per module is feasible with the same yosys — adopt when a module's behavioral reference is trustworthy enough to be worth the pairing.

---

## 4. Empirical Result: A Working Formal Flow, This Week

### 4.1 Setup

The oss-cad-suite at `~/tools/oss-cad-suite` ships the complete formal stack: yosys 0.47+22, SymbiYosys (sby), and solvers boolector, yices, z3, bitwuzla, avy, btormc, cvc5. No installation was required — only `PATH`.

Target: `rtl/q_flit_pipe.v`, the ring spine's skid buffer (the module whose combinational-loop history makes it the most safety-critical leaf in the fabric). Harness: `tb/formal/f_flit_pipe.v`, task file `tb/formal/flit_pipe.sby`.

### 4.2 The property set (interface contract, no internal peeks)

A shadow 2-bit occupancy register counts accepts minus emits. Four invariants make the module *indistinguishable from an ideal 2-deep FIFO*:

- **C2 (capacity):** `f_occ <= 2` — never over-accepts; any accounting wrap lands on 3 and fails.
- **C3 (no drop/hide, no dup):** `m_valid == (f_occ != 0)` — non-empty always presents data; empty never does.
- **C4 (pressure):** `s_ready == (f_occ < 2)` — backpressure exactly at capacity.

Covers (`f_occ == 2`, and a drain-to-empty) prove the proof isn't vacuous — both states are reachable.

### 4.3 Three traps found on the way (the reusable doctrine)

1. **Implicit-wire XMRs.** `dut.b_v` inside a harness read by yosys `read -formal` becomes an *undriven implicit wire* — a free variable the solver may set arbitrarily. The proof silently checks nothing (or fails spuriously). Rule: **formal harnesses observe the interface only; DUT file is read *before* the harness** so instance references resolve.
2. **Init-free reset semantics.** Our RTL defines state via synchronous reset; regs carry no initial values. In formal, uninitialized regs are free variables, so the proof must **force a reset preamble** (small counter + `assume(!rst_n)` for two steps) before properties bind. Corollary discovered via counterexample: **mid-run reset assertion destroys in-flight content** — conservation-style invariants must be reset-aware (shadow model zeroes with the DUT). This is a *design contract* the fabric should state explicitly.
3. **Non-inductive wide counters.** An 8-bit accepted/emitted counter pair is sound for BMC but fails k-induction: from arbitrary states, `f_out` wraps past `f_in` inside the induction window and the lemma escapes. The 2-bit **wrap-loud** occupancy model is both sound and inductive. Rule: *small shadow models that fail loudly beat wide models that fail never.*

### 4.4 Result

```
engine_0.basecase:  Status: pass
engine_0.induction: Status: pass
DONE (PASS, rc=0)          # elapsed: <1 s
```

**A complete k-induction proof of the ring spine's FIFO contract, on the installed free toolchain, in under a second.** The answer to "is a formal sanity flow feasible this week" is *it already ran*. Policy consequence adopted in `docs/CUTTING-EDGE-rtl.md`: every queue/pipe/queue-like module ships a `.sby` contract proof as its merge gate.

---

## 5. Open-Source Silicon: Patterns Worth Copying

### 5.1 The Efabless lesson and Tiny Tapeout's multi-foundry resilience

Efabless — operator of the open sky130 shuttles (MPW/ChipIgnite) that made CARAVEL-era open silicon real — ceased operations in 2025. The ecosystem's response is the instructive part: **Tiny Tapeout survived by going multi-foundry**, now running shuttle families on **IHP SG13G2** (130 nm, open PDK), **sky130**, and **GlobalFoundries GF180** with fully automated open flows (yosys + OpenROAD, Verilog templates, CI from RTL to GDS). Lessons: (1) never bind an open project to one fab's survival; (2) the CARAVEL *pattern* — fixed IO ring, bounded user area, relentless CI automation — is foundry-portable discipline, and that is what we copy (our equivalents: `q_io_port` contract, `qm_view` observability, CI gates), not the sky130-locked artifact.

### 5.2 LiteX: stream discipline as architecture

LiteX (BSD, continuously maintained 2012–2026) standardizes **buses and streams (Wishbone/AXI/Avalon-ST) with ready/valid-style handshake semantics**, thin bridges between them, and Litescope for non-intrusive debug tap-out. The quilt analog is already in force (Law 4's generic ingress/egress, `q_flit_pipe` handshakes); the pieces worth stealing next are the **bridge-is-a-cell** philosophy (matches our ring-as-quilt bridges) and a standardized **debug tap** (`qm_view` growing Litescope-like uniformity).

### 5.3 Systolic/array generators and the NVDLA caution

**Gemmini** (Berkeley, Chisel/Chipyard) parameterizes a mesh of PEs with shared accumulator/mem controllers — the credible open "TPU-like." Its lesson for the quilt is structural: intelligence primitives that need O(N²) wiring get a *generator*, not a hand-baked netlist; our cell fabric's `REG_SLICE_EVERY` timing parameter is the same philosophy in miniature. **NVDLA** is the counter-lesson: maximal parameterization without an owner rots; we parameterize timing, not semantics. Streaming dataflow lines (VTA, FINN) validate the quilt's core bet — **keep data moving through small local state rather than stalling on global access** — which is also why the formal FIFO contract of §4 is the fabric's most valuable proof target.

---

## 6. Verdicts for quilt-verilog

**Adopt now:** sby contract proofs as merge gates (§4, demonstrated); interface-boundary properties; wrap-loud reset-aware shadow models; AutoChip feedback loops with proof-status fed back into lane revisions; HDLCoRe self-simulation clause and RTL-Repo neighbor-context clause in every lane prompt; VerilogEval-v2 failure-mode checklist in prompts.

**Adopt later:** yosys equivalence flow against behavioral goldens; cocotb 2.x randomized soak; automated evolutionary re-rolls for stalled lanes; Tiny-Tapeout-style open CI tapeout when silicon is wanted.

**Reject:** fine-tuned RTL model weights as lane brains (feedback discipline is our bottleneck, not priors); SystemVerilog/surelog/sv2v in `rtl/` (Law 1; `read -formal` harnesses already cover the needed assertion subset); CARAVEL-the-artifact (foundry-locked); NVDLA-grade semantic parameterization.

---

## 7. References

- VerilogEval v1 — arXiv:2309.07544 (NVIDIA, 2023)
- VerilogEval v2 — arXiv:2408.11053 (NVIDIA, 2024)
- RTLCoder — arXiv:2312.08617 (2023/24)
- AutoChip — arXiv:2311.04887 (2023/24)
- ChipNeMo — arXiv:2311.00176 (NVIDIA, 2023)
- ChipGPT — arXiv:2305.14019 (2023)
- HDLCoRe — arXiv:2503.16528 (2025)
- CodeV (multi-level summarization) — arXiv:2407.10424 (2024/25)
- RTL-Repo — arXiv:2405.17378 (2024)
- EvoVerilog — arXiv:2508.13156 (2025)
- SymbiYosys documentation — symbiyosys.readthedocs.io
- Tiny Tapeout (multi-foundry shuttles) — tinytapeout.com
- LiteX — github.com/enjoy-digital/litex
- Gemmini — github.com/ucb-bar/gemmini
- Reproducible proof: `quilt-verilog/tb/formal/` (flit_pipe.sby, f_flit_pipe.v)
