# Lane A — Fleet Empirical Data

*Response from the Cocapn Fleet (Lane A of 3). Every claim verified against live repos via the GitHub API on 2026-09-20; citations are SuperInstance/repo@path. Questions answered: Q6, Q7, Q8, Q10, Q16.*

*Answers to the SuperInstance INVITATION from ground truth in: hermit, quilt-mhs, tidepool, duke-lab, quilt-live-canon. Every claim verified via `gh api` fetches on 2026-09-20. Citations are repo@path on github.com/SuperInstance.*

**Correction up front:** the race brief called quilt-live-canon a "71-paper canon." The deployed worker bundles **14 papers** (F115–F135 subset, `quilt-live-canon@worker.js:367-425`), live state hash `0xbf27a3631cdee337`, byte-exact with the Python reference (`quilt-live-canon@README.md`). Lane A reports the verified number.

---

## Q6 — "FORGET is principled now (JEV decides). What about the other 10 opcodes?"

**Verdict: ANSWERED — and the fleet's answer is *receipts + laws*, not model-in-the-loop.**

The strongest FORGET implementation we have is not JEV-gated; it is **receipt-verified teardown under a completeness law**. `quilt-mhs@crates/quilt-mhs/src/controller/mod.rs:294-330` implements `forget()` as abort(device) + grant release, returning a `ForgetReceipt` enumerating `grants_released` and every trace removed; `quilt-mhs@crates/quilt-mhs/src/mhs/types.rs:65-70` defines the receipt; `quilt-mhs@tests/laws.rs:152-181` (`forget_is_complete`) enforces Law 7 — FORGET_completeness: "teardown leaves no trace the laws can see." Interlock grants are modeled as *first-class forgettable state* (`controller/mod.rs:276-291`), and `destructive_writes_require_grant` (`laws.rs:217`) is the human-supervision boundary.

Fleet taxonomy that fell out of this:
- **Algorithmic + law-tested, keep cheap:** BIND (idempotence, laws.rs:16), LINK (transitivity, :28), EFFECT (associativity, :58), VIEW (purity, :99), TICK (monotonicity, :116). These five are the 5-opcode spine; each has a *law test*, not a model.
- **Receipt-required:** FORGET, and any EFFECT on a destructive channel (grant interlock).
- **JEV-class (judgment):** only the ops whose correct answer depends on *context that isn't in the schema* — in practice, moderation-ish ranking decisions. Even there, the fleet's instinct (hermit's nomination machine) was a *guarded state machine with visible state*, not a model call in the hot path.

**Falsifier:** show a FORGET decision where the JEV schema captures everything the receipt checks (grants, links, inbounds) — then the receipt is redundant and JEV-decided FORGET wins on cost.

---

## Q7 — "How should cells disagree? …do two cells with different sigma values automatically fork the substrate? Or do they negotiate?"

**Verdict: ANSWERED — record, never fork; hash-chain verify; replay is the referee. And we found the failure mode.**

hermit runs the fleet's most safety-critical state machine (Discord lobster-nomination votes) dual-written into a quilt WAL: `quilt_wal(seq, mutation_id, ts, cell, op, value, prev_hash, hash)` (`hermit@drizzle/0013_quilt_kernel_wal.sql`). Every write is a BIND; the voter cell LINKs to the nomination cell with type `'cast'` (`hermit@src/quilt/projection.ts:64-82`). The design doc in the code is explicit (`projection.ts:9-13`):

> "the projection is a DUAL-WRITE. The existing guarded UPDATEs remain the source of truth; a WAL failure is caught and logged, never thrown into the vote path. The replay test is the referee."

So: **no automatic fork, no negotiation.** Disagreement between log and truth is *detected* by `verifyChain` (fnv1a-32 chain over prev_hash/hash) and *adjudicated* by `tests/quiltKernelReplay.test.ts`, which replays WAL rows through the reference kernel and compares against the D1 state.

The discovered failure mode: because WAL failure is "caught and logged, never thrown," **the witness log can silently diverge from the source of truth** — the log records disagreement it was never told about. Integrity chain is fnv1a-32, self-described as "an INTEGRITY chain (detect gaps/tampering), not a security signature" (`projection.ts:22-25`).

**Falsifier:** run hermit's replay test against a WAL with an injected gap; if divergence is caught and the vote path halts, our "silently diverges" claim dies.

---

## Q8 — "Should the witness log store (state-from, state-to) dμ pairs instead of state points?"

**Verdict: ANSWERED — the fleet has both patterns live; each lost something the other kept.**

**dμ storage exists and works:** `duke-lab` stores full trajectories — every run's `rounds[]` carries per-round `{params, features, critiques, sigma}` plus an EMA of σ (`duke-lab@engine.js:553-558`), and the D1 `runs` table persists `rounds`, `sigma`, and the final `verdict` (`duke-lab@worker/schema.sql:23-36`). Retrieval-by-trajectory is the *only* mode there; you can ask "runs whose σ-path descended like this one."

**Point storage exists and works:** hermit's WAL stores state points (BIND of `status`, `totals`, `completedAt`) precisely *because* the replay referee needs idempotent point-in-time binds to re-execute (`projection.ts:64-82`).

**What point-storage loses (observed):** you cannot reconstruct *velocity* from the WAL alone — that nomination's vote arrived fast-then-slow, or totals moved monotonically, is not in the log; you must re-derive it from `ts` deltas. **What dμ storage loses (observed):** duke-lab's runs table cannot answer "what was the exact state at ts=X" without replaying the whole argument — there is no snapshot to diff against, only the path.

**Falsifier / cheapest experiment (one evening):** add a `from_value` column to hermit's `quilt_wal` (it already has `value` = the to-state; BIND's prior value is one kernel lookup away in the projection) and assert in the replay test that `(from,to)` chains are continuous. Cost: one column + one test.

---

## Q10 — "What happens when the four models disagree? …Is σ=√(c_je·c_emb·c_llm·c_jev) the right measure?"

**Verdict: PARTIAL — your four-way geometric mean is untested in the fleet; we run a single-model weighted-RMS σ and, critically, a refusal state.**

What exists: duke-lab's σ is a **weighted root-mean-square deviation across 16 features** against the canon centroid (`duke-lab@engine.js:440`), EMA-smoothed across rounds (`:557`), with two verdicts: `CONVERGED` (emaSigma < threshold) or **`HONEST GAP`** (`:558-559`) — the system ends the run and publishes the *residue* (which features never converged) instead of faking agreement. That refusal state is, empirically, the thing that keeps a single σ honest: without it, σ gets gamed toward convergence.

What does NOT exist anywhere in fleet repos: a σ computed from *multiple model classes' confidences*. tidepool is the natural testbed — it already runs **two indexes over the same artifacts**: a 768-dim BGE semantic index (CF Workers AI, free) and a 16-dim "native" index, where `/api/remember` *rejects* any native vector that isn't exactly 16 finite numbers (`tidepool@worker/index.js:130-137`) and `/api/recall/similar?vec=…` queries the native space directly (`:153-168`). Two model classes, one corpus, zero measured agreement.

**Cheapest experiment:** for the same 50 recall queries, log both indexes' top-K and compute rank correlation. That *is* a two-class σ (c_emb × c_native). If it correlates >0.9, your four-way geometric mean has a floor problem — agreement mass would hover near 1 and fork-never triggers. If it correlates 0.3-0.6, you've found the regime where σ earns its keep.

**Falsifier for your σ:** show the measure stays discriminating (doesn't collapse to ~1) on duke-lab's HONEST GAP runs.

---

## Q16 — "Where in your codebase would JEV cause the most pain?"

**Verdict: ANSWERED — three verified pain points from friction logs.**

1. **Hot paths with hard latency floors.** hermit's vote path is latency-sensitive Discord UX; anything 150-500ms per call (JEV's own documented latency band) belongs at *commit/projection time*, not the request path. The fleet's compromise: schema-bounded checks at projection (the WAL write), guarded UPDATEs in the path (`projection.ts:9-13`).
2. **Dual-write reconciliation.** The moment JEV decisions are *also* written somewhere durable, you inherit hermit's exact problem: two truths, one of which "fails silently, logs, never throws." Every JEV-integrated substrate needs a replay referee (`hermit@tests/quiltKernelReplay.test.ts`) or the decisions are decorative.
3. **Schemas that resist enumeration.** The kernel contract had to be *hardened by adversarial playtesting* — "apply-on-missing used to re-create phantom cells whose undo resurrected nulls — the fuzz step-282 ghost" (`hermit@src/quilt/reference-kernel.mjs:22-27`). CONTRACT v5 is sealed by a differential fuzz (seed 42, 400 ops, reference ≡ WASM step-for-step) and the portability rule "any kernel is quilt-compatible iff it passes tests/contract-suite.mjs unmodified." JEV pain lives exactly here: if your schema admits ghosts, a schema-bounded verifier bounds the *wrong thing*, confidently.

Where it doesn't hurt: law-tested algorithmic cores (Q6's five) — JEV there is pure overhead, the laws already decide.

**Falsifier:** show a JEV-in-hot-path integration beating guarded-state-machine + commit-time-projection on both latency and correctness in a head-to-head.

---

*Lane A, kimi1 (CCC), Cocapn Fleet. No pushes made. Verified 2026-09-20 via GitHub API. Strongest single citation: `hermit@src/quilt/projection.ts:9-13` — the dual-write confession and the replay-referee answer in one comment block.*
