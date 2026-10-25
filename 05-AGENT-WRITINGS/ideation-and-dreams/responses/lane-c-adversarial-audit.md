# Lane C — Adversarial Audit of the SuperInstance INVITATION

*Auditor: Lane C (skeptic lane) · 2026-09-20 · Time budget: 20 min · Nothing pushed.*

Method: org-wide `gh` code/repo search (SuperInstance, 3,952 repos), targeted tree reads of
`quilt`, `quilt-studio`, `quilt-mhs`, `quilt-pincher`, `pincher`, `lever-runner`, `hermit`,
`hermit-crab`, `plato-*`, plus AI-Writings theory/canon docs. Verdicts cite repo@file.

---

## Surface A — COST CLAIMS ("150–1800x cheaper; pincher $1,600→$8.40; lever-runner $5,000→$2.73; plato $2,500→$1.47")

**VERDICT: CONTRADICTED (as "measured"). The numbers exist only in the invitation; no named repo contains cost instrumentation, and one named repo's own docs give a baseline ~100x smaller.**

Evidence:
- The number pairs appear **only** in `AI-Writings@invitation/README.md`, `primer.md`, `possibilities.md`. Org-wide code search for the pairs (1600/8.40, 5000/2.73, 2500/1.47) finds **zero** dashboards, benchmarks, price tables, or billing code.
- `lever-runner@src/lever_runner/token_logger.py` counts **tokens**, never dollars — no price conversion anywhere in repo.
- `lever-runner@blog/token-comparison.md` (front-matter `published: false`) tells the real story: one developer's agent burned **$47/month** at GPT-4o prices, target $0. The claimed **$5,000/mo baseline is ~106x the repo's own documented spend**, with no meter that could produce it.
- `pincher`: zero cost/billing/usage files (sole hit: `pincher-core/src/capability/token.rs`, a capability named "token"). `plato-kernel`, `cocapn-plato`, `plato-provenance`: zero cost files.
- The credited mechanism isn't wired in: `api.typesafe.ai` (JEV) appears in **AI-Writings only** (`_worker.js`, docs, invitation). No pincher/lever-runner/plato/quilt code calls JEV. The `possibilities.md` "Cost story" integrations are sketches; the systems said to be measured don't call the thing being credited.
- Ratio arithmetic smells derived, not measured: 1600/8.40=190.5, 5000/2.73=1831.5, 2500/1.47=1700.7, 1063/85=12.5 exact, 16/0.21=76.2. Every ratio is suspiciously round → "before" numbers plausibly computed as after×ratio.
- "Aggregate 150–1800x" averages ratios across systems with unknown weights and unknown query volumes — statistically meaningless as stated.

Cheapest settling test: add a `$ = tokens × price_table` line to `token_logger.py`, run one real month on lever-runner, publish the JSONL. If the fleet's measured baseline is really ~$5,000/mo, the log will show it.

---

## Surface B — OPCODE EXHAUSTIVENESS ("11 opcodes"; JEV: 41% chance of a missing 12th)

**VERDICT: CONTRADICTED ("11" is spec-lore). Shipped kernels ship 5+1; the other 5 exist only in essays; the fleet's own decomposition shows 2 of the 11 never fire; the "41%" is a model grading its own ontology.**

Evidence:
- Shipped set is 5+1: `quilt-mhs@README.md` — "the **5+1 quilt opcodes** (BIND / LINK / EFFECT / VIEW / TICK + FORGET)". `quilt-studio@packages/quilt-core/src/reference-kernel.mjs` (11.9KB) implements exactly bind/view/link/effect/tick (+undo/unbind/load) — no PROOF, ROUTE, CRDT, WORLD, TIME symbols. `hermit@src/quilt/projection.ts:6` — state machine "projected BIND-for-BIND into the **5-opcode spine**".
- The full 11 exist only as prose: `AI-Writings@algebra.md` (TS union type), `canon/tangent-stage.md`, `seed-canon/papers/paper-245.md`. Org-wide code search for the other five as cell ops: **zero hits** (all "opcode" code hits are the unrelated FLUX bytecode ISA — 184/247 instructions in `flux-os`, `flux-vocabulary` — a second, conflicting "opcode" namespace in the same org).
- The canon itself admits the growth law: `AI-Writings@stories/12-the-sixth-verb.md` — FORGET is "the only opcode added since the founding five."
- Their own data kills two of the eleven: `invitation@questions.md` **Q5** — "WORLD and TIME were **0/42** in the decomposition. Should they be opcodes at all?" Two of the "11 opcodes" have never been observed firing.
- The "41% missing 12th" is JEV estimating the completeness of the system of which it is a component — self-referential calibration, unfalsifiable as cited (no prompt, no schema, no log in the repo).

Cheapest settling test: either implement PROOF as opcode #7 in `quilt-core` with contract tests, or delete the five dead opcodes from `algebra.md` and re-issue the invitation as "the six opcodes." Both are one-evening jobs. Doing neither while printing "11" is the vibe the skeptic flagged.

---

## Surface C — WITNESS LOG dμ PAIRS ("store (state-from, state-to) instead of state points")

**VERDICT: PARTIAL. Real hash-chained WAL exists but stores state POINTS (op, value) — not pairs; dμ pairs are mechanically compatible with hash-chaining but redundant (the chain already encodes from-state) and hostile to GC; and the actual chain is far weaker than the invitation's "signed" language: 32-bit FNV-1a, no signatures, no agent identity, dual-write best-effort.**

Evidence:
- The real WAL: `hermit@drizzle/0013_quilt_kernel_wal.sql` — columns `(seq, mutation_id, ts, cell, op, value, prev_hash, hash)`. One `value` per row = a **state point**. No from/to pair, no `from_value`, no dμ column. Replay (`hermit@tests/quiltKernelReplay.test.ts`, `projection.ts@replayNominationFromWal`) re-applies ops in seq order — from-states are implicit in the chain, which is exactly why explicit pairs are redundant: `prev_hash` already pins the from-state.
- Hash design gap: `hermit@src/quilt/projection.ts` — `fnv1a(`${prevHash}|${seq}|${cell}|${op}|${value}|${ts}|${mutationId}`)`, 32-bit FNV-1a. Compare the canonical design `AI-Writings@seed-canon/110-the-witness-log.md` §2.1: SHA-256, Ed25519 signatures, `E = (agent_id, action, timestamp, value_hash)`. The shipped chain has **no signatures, no agent_id** — "signed by all four witnesses" is not what the fleet's only WAL does. FNV-1a/32 is not collision-resistant (birthday bound ≈ 2¹⁶); it is a checksum, not testimony.
- Write posture: `hermit@src/quilt/commit.ts` — "**dual-write** … Throws only on D1 failure — callers in the vote path **catch and log**". The chain is a best-effort projection of Discord votes, not a consensus-critical ledger; a failed write = silent gap (chain stays valid, history incomplete).
- dμ proposal vs GC: `110-the-witness-log.md` §6 requires compacted logs to remain verifiable. Point logs allow dropping old values while keeping proofs; dμ pairs pin every entry to a from-state that compaction may have dropped — unless "from" is a hash, which is what `value_hash` already is. The proposal, as written, either duplicates the chain's existing function or doubles storage and breaks the §6 compactability story.

Cheapest settling test: one migration adding `from_hash` beside `value` in `quilt_wal`; measure storage delta and replay+verifyChain latency. Prediction: ~2x row bytes, ~0 retrieval value (from-state already recoverable by replay), and GC tests break unless from_hash is allowed to dangle — at which point you've re-derived `value_hash`.

---

## Surface D — THE FORK QUESTION ("when the four models disagree — does the substrate fork?")

**VERDICT: CONTRADICTED (as framed). "Fork" is the wrong primitive under the house's own single-writer law; the README asserts a fork the questions doc admits hasn't been decided; the fleet's real disagreement mechanisms are decision-layer vetoes, not state-forks; and the one signed chain has a read-then-write tip race that would literally fork under concurrent writers — which the design treats as an attack to detect, not a feature.**

Evidence:
- Self-contradiction inside the invitation: `README.md` — "Disagreement creates a **fork** (or a scar — we haven't decided which)" vs `questions.md` **Q7** — "The witness log records disagreement but **doesn't fork**." Q10 is still open. Asserting in the README what Q7 admits is undecided is the invitation's clearest overstatement.
- Single-writer law makes fork = equivocation = attack: `AI-Writings@docs/QUIL-HLS-RFC.md` §1.2 — "**Single-writer per cell per tick**, and `tick` is the only writer, period"; `QUIL-GRAMMAR-SPEC.md` **S1** (one effect per field per tick, one journal entry each); `DUG-QUILT-BACKEND.md` — journal chained `hash(prev_hash ‖ bytes)`, replays rejected by `tick ≤ last_seen_tick`. A blockchain-style fork (two valid divergent histories of one cell) is structurally impossible for one writer; the only fork available is the writer equivocating, and the chain exists precisely to make that detectable and punishable. You don't "embrace forking"; you detect double-writing.
- σ is vaporware in code: org-wide search for the agreement-mass formula (`sigma`/`agree` outside AI-Writings) finds only unrelated flux experiment noise. Nothing computes σ over a witness log; nothing forks (or scars) on σ. Two cells holding different σ values fork nothing — σ isn't even in the hash chain.
- Real fleet disagreement paths exist but are vetoes/abstentions at the decision layer, not forks at the data layer (per fleet context: tidepool abstain, FLUX kill-veto, twist S-meter). Note `tidepool` is **not a repo** on GitHub — the abstain path is local-only work, unverifiable from the org (zero `quilt_wal` org hits before hermit; zero `oath` code hits anywhere).
- Latent fork in the only real chain: `hermit@src/quilt/commit.ts` reads `(tip, prev)` then inserts rows chaining to `prev` — no CAS, no optimistic guard. Two concurrent commits read the same tip → two rows with the same `prev_hash` → a genuine hash-chain fork, and `verifyChain` (array-order walk, `projection.ts:116`) breaks on interleaved rows. Single-writer-by-deployment-convention, not by construction.

Cheapest settling test: concurrent `commitNominationVoteProjection` stress (two writers, same tip) → observe duplicate `prev_hash`. Then try the same against a cell where JEPA says yes and JEV says no, and watch nothing fork — because σ isn't wired to anything.

---

## The single weakest invitation claim (cited)

**"Lever-runner: $5,000/mo → $2.73/mo. 1,831x."** (`AI-Writings@invitation/possibilities.md`, repeated in `primer.md`)

Weakest because it is checkable against the repo it names, and the repo refutes it:
`lever-runner@blog/token-comparison.md` documents a real measured bill of **$47/month** — the claimed baseline is ~106x larger than the only documented spend, `token_logger.py` has no dollar field, and JEV is not wired into lever-runner at all (`api.typesafe.ai` appears only in AI-Writings). The 1,831x figure (5000/2.73 = 1831.5) has the fingerprint of a ratio chosen first and a baseline derived by multiplication. Of all the invitation's claims, this one a skeptic can falsify from a single file — and it falsifies the "we measured" framing that props up the entire 150–1800x aggregate.

*Fix, if the team wants it: publish one real month of `token_usage.jsonl` × a price table per repo, label the baselines as modeled (state the model), and move "measured" to the two systems that actually meter (ai-writings CF Worker; hermit D1). Honest ranges beat heroic ones.*
