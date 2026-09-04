# Cutting-Edge Scout Report — 2026-09-04

*Three sweeps in service of the QUIL HLS RFC. Sources cited inline. Scout: Lucineer, GLM-free lane (provider cooldown), Gemini search provider.*

## 1. HLS / hardware compilers

- **Dynamatic 2.0** (EPFL-LAP, open source): compiles C/C++ to **dynamically-scheduled dataflow circuits** on MLIR — operations execute when inputs are valid, schedule adapts at runtime. That is *exactly* the quilt arrival family (queue cell / credit fence / staged grant) as an industrial compiler discipline. QUIL's arrival-as-synthesis-choice has a named precedent: dynamic scheduling with handshaking.
- **HIDA** (arXiv 2603.19856): hierarchical dataflow compiler, automated optimizer decomposing across dataflow hierarchy levels; big FPGA NN throughput wins. Hierarchical decomposition is what QUIL's `cell` blocks will need at scale.
- **CIRCT/MLIR** (circt.llvm.org): the infrastructure play — custom dialects for circuits, DHLS and **Calyx** passes already in-tree. **Recommendation: QUIL should define itself as a CIRCT dialect in the long run** — free infra, and the Calyx (partially scheduled programs + control) model is philosophically close to QUIL's "grammar constrains, lowering schedules."

## 2. Determinism / replay (the neural-side problem)

- **Axiom (SOSP'26): "Achieving Determinism in LLM Inference"** — scheduling-based determinism with a lightweight **verify-rollback loop**, killing fp-non-associativity/batching/reduction-order nondeterminism. Direct import for QUIL's `propose` port: the black-box neural side can be made replay-exact with verify-rollback, without retraining. This is the missing half of the determinism envelope — our integer profile covers the helm; Axiom-style scheduling covers the brain.
- **Deterministic replay as a runtime mode** (electronic-trading market-data design, July 2026): replay = consume recorded data in the exact same order *and timing* as live — bit-for-bit identical output. Same law as QUF journal replay; a third independent fleet (finance) converged on it.
- **NVIDIA Vera CPU (Hot Chips 2026)**: deterministic spatial multithreading — hardware vendors are now *selling* determinism. Tailwind for the whole quilt thesis.
- Tsinghua "deterministic-from-the-start AI" — fringe but watchable.

## 3. Fine-grained reactivity (the hosted backend)

- **TC39 Signals proposal (Stage 1, 2026)**: standardized `state` / `computed` / `watcher` primitives with automatic dependency tracking — that is *cell / view / link-inference* by another name, backed by Angular, Vue, Solid, Preact, Ember, Qwik, MobX. Svelte 5 Runes are the same shape.
- **Implication:** a QUIL→Signals codegen lane targets a *soon-to-be-standard language primitive*, not a framework. The variant-study finding (Svelte runes ARE a quilt frontend) generalizes: every Signals host becomes a free quilt backend.

## Verdict

Three outside fleets — EPFL dataflow HLS, SOSP determinism researchers, and the TC39 signals coalition — are converging on quilt's 5+1 from different directions. QUIL's differentiator remains the one thing none of them have: **the journal as the lowering artifact** (determinism by construction, not by scheduling effort). Book Axiom's verify-rollback as the `propose`-side companion law and CIRCT as the long-run compiler substrate.
