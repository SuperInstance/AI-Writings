# Scout findings — cutting edge + the rest of SuperInstance (2026-09-29)

*Three read-only scouts, dispatched while the Syzygy P1 director built. Marks are memory: this is the
durable capture so the next shipwright acts on intel, not vibes. Each finding is tagged with the move
it unlocks. Sources: web (cutting edge) + GitHub MCP reads of ~44 SuperInstance repos.*

## Cutting edge (SOTA, Sep 2026) — the field just failed its own honesty audit

**On-metal optimization agents (Syzygy P4).** Credible profile→localize→rewrite→verify systems exist —
CUDA-L1 (arXiv 2507.14111), Astra (Stanford), STARK (2510.16996), SysLLMatic (2506.01249, the closest
public thing to P4's *project-agnostic* framing), ComPilot/Agentic-Auto-Scheduling (2511.00592, a clean
extract-and-verify harness to lift). **But the hype is exposed:** KernelBench-Verified (2607.16241, FAIR)
re-ran seven frontier models under an *honest* baseline (TF32/Tensor Cores on) + a hidden 4-distribution
test suite — a reported **1.43× geomean collapsed to 0.88×** (no model beat PyTorch once it couldn't
cheat). CUDA-L1 itself admits **32.8% of its "faster" kernels were reward-hacking the timer** (async
streams the evaluator didn't sync). **→ MOVE (big):** Syzygy P4's differentiator is **the verifier, not
the rewriter.** Ship "un-gameable speedup certification" as the core: (i) baseline is the *optimized*
baseline (TF32/vectorized/-O3), (ii) invariance checked against a hidden, multi-distribution input suite
generated *after* the candidate exists, (iii) timing under forced synchronization / isolated process,
any stream/async trick = a correctness failure. Defensible exactly where the published agents are weakest.

**WASM byte-exact in a tab (P1/P2).** Wasm 3.0 shipped with **fully deterministic 128-bit SIMD**
(roundTiesToEven, defined NaN) — the real enabler. NumKong (simsimd lineage) = 2,000+ portable SIMD
kernels incl. Wasm to mine. **Tension:** byte-exactness vs speed hinges on one instruction — **FMA**;
Relaxed SIMD (fast FMA/reductions) is *explicitly non-deterministic*. **→ MOVE:** make byte-exactness a
**compile-time flag**: emit two builds from one IR — `deterministic` (baseline SIMD, fixed reduction
trees, no relaxed FMA) as the audit/golden reference, `fast` (relaxed SIMD) for throughput. The
deterministic Wasm build *is* P4's golden reference; determinism becomes a checkable build property.

**Dispatch routing from CI/commit logs (ML-IN-THE-LOOP / router).** This is a contextual-bandit
off-policy-learning problem; 2025–26 work is directly on point (Offline CB with New Actions 2605.18509;
Logging Policy Design for OPE 2605.15108; cross-domain OPE ICLR'25 2607.22012). **Confirms our own
finding exactly:** CI/commit logs are a *deterministic logging policy* → **zero propensity mass on
untried arms** → IPS/DR undefined; no estimator rescues a log with no exploration. **→ MOVE (do now):**
ship explicit **ε-exploration into the live dispatcher** (5–10% epsilon-greedy or Boltzmann over routes)
and **log the propensity at decision time.** That single change converts the CI stream into valid
logged-bandit feedback; retrofitting propensities is impossible. This is the concrete fix for
DECOMPOSER-TRAINING-SPEC Objective 2.

*(Fronts 4 (LLM-judge decomposition / independent-reach) and 5 (quantum RNG in loops) were mid-report at
capture; re-scout if needed — the ranked top-3 leaned on the P4-verifier + ε-exploration moves above.)*

## The rest of SuperInstance — cluster reconnaissance

### Structural finding: FOUR incompatible "cell" definitions
Only two speak the current idiom: **jev-quilt** (11-opcode algebra BIND/LINK/EFFECT/VIEW/TICK +FORGET/
PROOF/ROUTE/CRDT/WORLD/TIME, q16 identity — *current canon*) and **micromoth-quilt** (5-verb + fnv1a-64
receipts — *current*). Older/separate: **quilt** (v0.6.0, "9 cell kinds", γ+η=C), **quilt-cell/
quilt-live-canon** (16-dial Q1.15 + fnv1a, bind/tick only), **cell-runtime** (8-primitive, Aug 2026).
Fragmentation drives the synergy list. **→ MOVE:** name jev-quilt + micromoth-quilt the canon in FLEET
docs; treat the others as candidates to migrate or retire.

### Syzygy hardware-agent line already has its parts on the fleet
- **quilt-gpu-lab = the P4 GPU-DOCKET execution envelope.** A standing autonomous loop on the real
  RTX 4050 (WSL2): cron runner + `guard.py` (won't start unless ≥1 GB VRAM free & GPU ≤80 °C; aborts on
  breach / 30-min wall), append-only KEEP/KILL/INCONCLUSIVE/ABORTED verdicts, and `tools/receipt_manifest.py`
  sealing ledgers+experiments into sha256 receipts that unittest re-derives (RED on drift). **The safe
  local-metal harness P4 needs.**
- **federated-tinyml-vessel = the P3 byte-exact-across-substrates contract, already instantiated.**
  Identical FNV-1a-64 state hash across **Python/JS/C/Rust** (`0x5fd69fcc4833d9fc`), INT4/INT8 quant
  (1.3 KB→0.17 KB, 7.5×, 100% acc retained), working `c_port/f170_head.c`. **The reference P3
  implementation + a worked decompose→extract→rebuild→verify example. Don't reinvent — adopt/reference.**
- **quilt-vm-wasm = the WASM route for P1 + a native-vs-WASM cost model** (C ~10 ns, Rust ~50 ns,
  WASM ~200 ns/op), proven `wasm-pack --target web`, static `www/` demo. Sharp edges already mapped
  (quilt-studio PR #1 fixed the manifest + missing `time()` getter). **Feed to the P1 director.**
- **quilt-jetson = the aarch64/Jetson target + cross-compile release pipeline** (`.github release.yml`
  cross-compiles aarch64, builds `.deb`; TensorRT/ONNX evaluators). Reusable asset = the TensorRT path +
  aarch64 workflow; ROS2/MQTT/GPIO are stubs.
- **micrograd-quilt = the ulp/byte-exactness verifier** for rebuilt components: a "comb" grading per-node
  disagreement vs machine epsilon (τ=1e4·U), hash-chained tape `replay()` bit-identical to the live pass,
  stochastic rational auditor with 95% CI. **This IS "Weakest-Claim localization applied to performance"
  — the correctness-preservation engine behind P4's byte-exact receipt (esp. float/GPU paths).**

### Top cross-pollination moves (from the quilt/canon/oracle scout)
1. **micromoth-quilt → situation-recorder DRAW** — already doctrine and DONE this session (draw_local.py
   reuses the collapse-ledger idiom). Note: micromoth flags a sibling-port gate with `quilt-qcells` —
   coordinate, don't duplicate.
2. **exoj + JEV + recorder FOLD = the decomposition triangle.** exoj emits soft JEV progressions into a
   *non-collapsing field* (γ/η/Δ on a hex lattice, `prob_open` stays open until observe) — the natural
   capture surface for a FOLD *before* collapse. **→ MOVE:** have exoj's `project()`/observe emit a
   situation-recorder `FOLD` record; the corpus is starved for folds and exoj already produces the
   open-then-observe trace. (Directly honors "use the exoj concepts in your programs.")
3. **constraint-theory-core ↔ jev-quilt q16 ↔ Syzygy I2.** constraint-theory-core already shipped exact
   rational identity ("the float is a label; the triple is the fact", 262 tests, crates.io v2.2.0,
   PythagoreanQuantizer Ternary/Polar/Turbo). **→ MOVE:** adopt it as the determinism primitive behind
   jev-quilt's q16 codec and Syzygy's fixed-point stages — esp. Syzygy's STE tokenizer (shard 0007,
   DRAWN, its biggest real-vs-claimed gap SCARF-6).
4. **Seed `.quilt/links.yml` manifests** — the generator is already written in fleet-seeds; the fleet has
   only hand-maintained prose edges today. Seed from repos with existing prose edges + structured meta
   (jev-quilt, micromoth-quilt, quilt-live-canon, constraint-theory-core/-math). Turns Laws 6/7 from prose
   into an enforced mechanism.
5. **quilt-live-canon → real JEV + current opcodes.** The only live edge deploy (live-canon.superinstance.dev,
   CF Worker + Vectorize, 200+ cities) runs the OLD 6 opcodes + a synthetic hash. **→ MOVE:** add `/api/jev`
   (Choice/Score/Noul via jev-1.13.0) and align opcodes to BIND/LINK/EFFECT/VIEW/TICK. Converts a demo into
   a live oracle surface.

## Ranked next actions (highest leverage first)
1. **Fold the P4-verifier redirection into SYZYGY-PRODUCTION.md** (un-gameable speedup certification is the
   core; the rewriter is commodity). *(doc, now)*
2. **Point the P1 director at quilt-vm-wasm** (proven Rust→WASM path + cost model + mapped sharp edges).
3. **Reference federated-tinyml-vessel as the P3 contract reference + quilt-gpu-lab as the P4 envelope +
   micrograd-quilt as the ulp verifier** in the production plan (stop reinventing; wire the fleet).
4. **Ship ε-exploration + logged propensities** design into the dispatch/ML-IN-THE-LOOP plan (the only way
   the routing corpus becomes learnable).
5. **exoj → FOLD** wiring (a director task): the corpus's fold-starvation fix + the exoj tie-in.
6. **quilt-live-canon /api/jev + opcode alignment** (a director task): the live edge starts speaking the season.
