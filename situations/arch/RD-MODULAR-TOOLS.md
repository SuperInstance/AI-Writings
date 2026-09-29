# R&D modular-tool backlog — trending papers/repos → composable cells (2026-09-29)

*Owner: "R&D from trending and cutting-edge papers and repos. Synergize and think of modular tools
that could enhance our projects. Wide-scope quest." Three R&D scouts (agent-infra / systems-edge /
leftfield) surveyed 2025–2026 SOTA, each verifying load-bearing sources by fetching, each told to go
net-new vs SCOUT-FINDINGS-2026-09-29.md. This is the synthesis: a ranked backlog of modular CELLS —
each with inputs→outputs, the trending source it's grounded in, the repo it enhances, size, and
status. The through-line: **the strongest proposals are receipt/verifier cells — "who verifies the
verifier" — which is our fold/receipt ethos, scaled.***

## Build-now shortlist (ranked by leverage × buildability)

1. **`tool-pin-receipts`** (S) — hash-pin every MCP tool manifest before a crew loads it; a later
   description change flips the hash → RED (rug-pull / tool-poisoning defense). *Grounded:* MCPTox
   (2508.14925, >60% attack success across 45+ real MCP servers), OWASP MCP Top-10. *Enhances:*
   fishing-fleet + situation-recorder — tool-description hash-pinning **is** our fnv1a receipt idiom
   applied to the tool surface; drift-detection = the RED-on-drift pattern quilt-gpu-lab already runs.
   Cheapest, defends the whole dispatch fleet.
2. **`wasm-native-drift-differ`** (S–M) — **SHIPPED** (Syzygy `claude/verifier-cells`, mark V02;
   independently verified 2026-09-29: selftest 27/27, all 6 planted drifts D1–D6 caught with correct
   first-divergent-field + minimal repro, port byte-exact vs native on 2405 cases) — differential-test
   the native vs WASM build of one IR on a
   fuzzed suite, deterministic build = golden, localize the first divergent op with a minimal repro.
   *Grounded:* Kaizen metamorphic+differential (2607.04058), bit-exact inference verification
   (2606.00279). *Enhances:* **the Syzygy P1 POC we just shipped** (an automated drift alarm vs the C,
   extending the `0x6dbdd1a8` idiom) + quilt-vm-wasm (adds a correctness differ beside its cost model).
3. **`kernel-oracle-mutant-gauge`** (S) — **SHIPPED** (Syzygy `claude/verifier-cells`, mark V01;
   independently verified 2026-09-29: selftest 13/13, full gauge reproduced oracle-strength 41/41=100%
   — 0 survivors, hash-chain re-derivation byte-identical. Honest SHORTCUT: 100% is *of a hand-written
   42-mutant catalog*, not operator-generated) — mutation-test the *oracle itself*: seed documented buggy
   kernel variants, report the fraction that escape the suite = an **oracle-strength score**.
   *Grounded:* "Measuring the Checker" (2609.22220), "Correctness Illusion in LLM GPU Kernels"
   (2606.20128 — 9/9 seeded bugs passed KernelBench/TritonBench/GEAK). *Enhances:* **Syzygy P4** — a
   speedup verifier is only as un-gameable as its correctness oracle; this certifies the differentiator
   + turns micrograd-quilt's "comb" into the mutant detector.
4. **`rubric-forge`** (M) — JEV emits an instance-specific *weighted rubric* {criterion, weight,
   score} that aggregates to a dense scalar reward, not just a verdict. *Grounded:* Rubrics-as-Rewards
   (2507.17746, +31% HealthBench, +7% even on verifiable GPQA). *Enhances:* JEV + ML-IN-THE-LOOP —
   JEV's decomposed leaves already **are** rubric criteria; this supplies the weighting so the corpus
   gets a **graded** training label instead of the thin 0.29 binary. Directly attacks the router's
   signal problem.
5. **`skill-forge`** (M) — distill retrievable "reasoning cards" {trigger, strategy, counterexample,
   provenance-hash} from the corpus's DROP/failure records (not raw trajectories). *Grounded:*
   ReasoningBank (2509.25140 — **failure traces are the most transferable memory units**), Memp
   (2508.06433). *Enhances:* the situation-recorder corpus (our biggest untapped asset, and its DROP
   verb already marks exactly the failures) + tidepool (cards live behind the JEV recall gate). The
   non-RL learn-from-logs path, complementary to the planned ε-exploration router.
6. **`sol-ceiling-gate`** (M) — report a kernel's speed as **% of hardware speed-of-light** (roofline
   from measured arithmetic intensity + microbenchmarked peaks), not speedup-vs-baseline. *Grounded:*
   SOL-ExecBench (2603.19173), CANN-Bench (2607.20518). *Enhances:* Syzygy P4 (removes baseline
   selection entirely — the one degree of freedom KernelBench-Verified showed models exploit) +
   quilt-gpu-lab (a physical KEEP/KILL axis). Runs on the local RTX 4050.
7. **`dominated-novelty-search`** (M) — threshold-free QD: rank each candidate vs only its k nearest
   behavioral neighbors — no grid, no bins to tune. *Grounded:* Dominated Novelty Search (2502.00593,
   GECCO'25; already the SOTA baseline others benchmark against). *Enhances:* **labs/qd-arena** —
   drop-in replacement for the MAP-Elites grid that breaks in high-dim/unsupervised descriptor spaces;
   the domination score is a cleaner novelty signal for Moth to explore.
8. **`timelock-beacon-collapse`** (S) — encrypt a decision/field so it is *provably* un-openable until
   a future public-randomness round, then it collapses on the world's schedule with a public BLS
   verifier. *Grounded:* drand quicknet + tlock (live since 2023, HTTP API today). *Enhances:* **exoj**
   — makes `prob_open` non-collapse a *cryptographic fact*, and each observe emits a beacon-anchored
   receipt (a FOLD the corpus is starved for); also an un-steerable, publicly-auditable draw for
   quantum-fx/qd-arena **without hardware** (defends the seed-hijack vector).

## The rest of the backlog (grouped by substrate)

**Verifier / Syzygy line (the "who verifies the verifier" cluster):**
- **`schema-fuzz-suite`** (M, now) — generate a hidden, multi-distribution input suite *after* the
  candidate exists, from symbolic dims + all dtypes + boundary/tail values; fp64 reference + per-dtype
  tolerances; byte-stream generators so byte-mutation = structured input mutation. *Grounded:*
  2606.20128, Gentoo generators (2604.01442). Makes the P4 "hidden suite" MOVE concrete; also gives
  federated-tinyml-vessel a real multi-shape/dtype invariance suite.
- **`det-reduce-tree`** (M, now) — a fixed-order reduction schedule keyed on problem shape (fused
  upcast, IEEE-FMA, deterministic split-K, no atomics): byte-exactness as a *constructed* property that
  is **also faster**. *Grounded:* 2609.25624 (**1.17–3.1× faster while bitwise-identical across
  Ampere/Ada/Hopper**) — refutes the assumed determinism↔speed tradeoff. *Enhances:* the Syzygy golden
  reference + quilt-vm-wasm's deterministic build + quilt-gpu-lab replay.
- **`mxfp4-sensitivity-guard`** (M, needs-hardware) — layer/block-wise FP4 sensitivity → mixed
  MXFP4/6/8 assignment by measured error budget, with a byte-exact accuracy-retention receipt across
  substrates. *Grounded:* the 2025–26 MXFP4 wave. *Enhances:* federated-tinyml-vessel (its 100%-acc
  claim gets a graded, receipted precision map).
- **`zk-subproof-linker`** (L, research-bet) — decompose an inference into independent sub-proofs
  linked by shared boundary commitments; verify the whole from the parts. *Enhances:* upgrades our
  fnv1a receipts toward cryptographic proof-of-computation (the same decompose-then-fold shape).

**Agent / corpus / context:**
- **`tool-shelf`** (M, now) — retrieve only top-k relevant tools per mission + hand the crew code-API
  stubs so tool defs and intermediate results never bloat context. *Grounded:* RAG-MCP (2505.03275),
  Anthropic "Code execution with MCP" (98–99% token cut at 100+ tools). *Enhances:* fishing-fleet crew
  cost; retrieval propensities log as ROUTE records the router corpus needs for free.
- **`delta-fold`** (M, now) — compact a long mission into an append-only *delta* to a running playbook
  (not a lossy re-summary), hash-chained so context-collapse becomes a detectable broken chain.
  *Grounded:* ACE (2510.04618, +10.6% w/ no labels; names brevity-bias + context-collapse), Chroma
  "Context Rot". *Enhances:* the FOLD verb + tidepool.

**Retrieval / canon:**
- **`colqwen-page-cell`** (M, now) — content-addressed *visual* retrieval: index a page as an image
  (no OCR), retrieve by late-interaction MaxSim over patch embeddings; page-hash = address, match-map =
  spatially-grounded citation. *Grounded:* ColPali (2407.01449, ICLR'25) → ColQwen3-4B / ColModernVBERT
  (250M, on-device). *Enhances:* canon-* (visual/PDF knowledge, patch-hash as the content address) +
  tidepool (a visual recall gate).

**Generative / creative (bets):**
- **`masked-field-denoiser`** (M, research-bet) — a masked-diffusion LLM that holds an output as a
  superposed field of `[MASK]` and collapses by confidence-ordered any-order unmasking; deterministic
  replayable tape. *Grounded:* LLaDA (2502.09992, 8B matches LLaMA3-8B, beats GPT-4o on reversal) →
  LLaDA2.0. *Enhances:* **exoj made generative** (the masked field IS the open probability field;
  unmasking IS observation) + any-order melody infilling for tensor-midi / musician-soul.

## The unifying reading (why this set, not a random reading list)

Three independent scouts, three lenses, converged on the **same shape**: the frontier this year is not
"a better generator" — it is **verified, receipted, decomposable computation**, which is what this
fleet already is. Every build-now cell above is a *receipt or a verifier*: pin the tool (receipt),
diff the builds (verifier), mutate the oracle (verify the verifier), weight the rubric (a graded
receipt), distill the failure (a provenance-hashed card), measure % of light (a physical receipt),
rank by local domination (a re-derivable transform), timelock the collapse (a cryptographic receipt).
So the highest-leverage R&D is not adopting a new paradigm — it is **applying our fold/receipt idiom
to the surfaces we don't yet cover**: the tool surface, the build boundary, the oracle itself, the
reward, the memory, the performance ceiling, the randomness, and the field's collapse.

## Recommended first three to build (a coherent slice)
- **`tool-pin-receipts`** + **`wasm-native-drift-differ`** + **`kernel-oracle-mutant-gauge`** — all
  size-S, all buildable-now, all pure applications of our receipt idiom, and together they harden the
  three surfaces we're most exposed on right now: the crew's tools, the P1 browser POC we just shipped,
  and the P4 verifier that is Syzygy's whole differentiator. Then `rubric-forge` + `skill-forge` to
  give the corpus a graded reward and a failure-memory, and `dominated-novelty-search` to upgrade
  qd-arena. Build as `labs/` cells (the RSI pattern: a small honest cell the next director reuses).
