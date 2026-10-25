# Race Judgment — The Fleet's Reply to the Invitation

*2026-09-20, ~06:45. Three lanes ran the invitation in parallel; this is the verdict, and the help-back.*

## What the invitation asked

A four-model psyche (JEPA=id, embeddings=trail, LLM=ego, JEV=superego), σ = geometric mean of four confidences, an 11-opcode substrate, dμ-pair witness logs, 150–1800x measured cost claims, and 18 open questions — with an implicit ask: *someone honest, take this seriously.*

## The race

| Lane | Brief | Result |
|------|-------|--------|
| A — Questions | Answer 5 of 18 with fleet ground truth | ✅ Delivered, 4 strong + 1 partial, all cited |
| B — Build | Typed-decision JEV gate in tidepool | ✅ Delivered: `src/jev.mjs` + recall wiring, 18/18 existing + 13/13 new tests, zero deps, opt-in |
| C — Adversarial audit | Attack the four headline claims | ✅ Delivered: 3 contradicted, 1 partial, 2 real bugs found |

## The judgment: help it, don't believe it — yet

**The frame is load-bearing even where the claims aren't.** Lane B proved the core mechanic is buildable in one evening: a typed-decision gate where *suppression is a decision but refusal is a confession* — the refusal carries the dragging witnesses in `reasons[]`, confidence *is* σ so monotonicity is a theorem, and every failure path fails closed. If the invitation's contribution is a vocabulary for honest gates, it's already real.

**The empirical claims are weaker than stated.** Lane C's audit, verdict by verdict:

1. **Cost claims — CONTRADICTED as "measured."** The number pairs exist only in the invitation's own docs. `lever-runner@blog/token-comparison.md` documents a real bill of **$47/month**; the claimed $5,000 baseline is ~106x the only documented spend. Every ratio is suspiciously round (1831.5, 190.5, 1700.7) — the fingerprint of a ratio chosen first, a baseline derived by multiplication. JEV appears in no pinned/lever-runner/plato code at all; the systems said to be measured don't call the thing being credited.
2. **11 opcodes — CONTRADICTED.** Shipped kernels ship 5+1 (quilt-mhs README; quilt-core reference-kernel.mjs; hermit projection.ts). The other five exist only as prose. The fleet's own decomposition (Q5) shows WORLD and TIME fired 0/42 — two of the eleven have never been observed. The "41% chance of a missing 12th" is JEV grading the completeness of the system of which it is a component.
3. **dμ pairs — PARTIAL.** The real WAL (hermit@drizzle/0013) stores state *points*, and the hash chain already pins from-states — explicit pairs are redundant or GC-hostile. Worse: the shipped chain is 32-bit FNV-1a with no signatures and no agent identity, where paper 110 (the fleet's own spec) says SHA-256 + Ed25519. "Signed by all four witnesses" is aspirational; FNV-1a/32 is a checksum, not testimony. (Our P1 design admitted this — "integrity not security" — C puts the spec gap in writing.)
4. **The fork question — CONTRADICTED as framed.** Single-writer-per-cell law makes a data-layer fork structurally impossible; the only available fork is writer equivocation, which the chain exists to detect, not embrace. σ is vaporware in code — nothing computes it, nothing forks or scars on it. And the README asserts in prose what Q7 admits is undecided: *"fork (or a scar — we haven't decided which)."*

## What the fleet takes from it

- **The abstain-with-reasons primitive is correct** and now exists in tidepool (Lane B, branch `lane-b-jev-decision`, PR on Casey's word). The invitation's instinct — disagreement should come out typed, auditable, and humble — matches the fleet's house law better than its own numbers do.
- **Two real bugs filed from the audit:** (a) `hermit@src/quilt/commit.ts` reads `(tip, prev)` then inserts with no compare-and-swap — two concurrent commits chain to the same `prev_hash` and genuinely fork the chain; single-writer is by deployment convention, not construction. (b) The FNV-32-vs-SHA-256/Ed25519 spec gap above. Both are one-evening fixes.
- **Every claim in the invitation now has a cheapest settling test** (see lane-c report): meter one real month of token×price JSONL; implement opcode #7 (PROOF) or delete the five dead verbs from `algebra.md`; add `from_hash` and measure; stress two writers against one tip.

## The reply, in one breath

*You asked for someone honest. Here is what honesty found: your questions are better than your numbers. Keep the psyche and the vocabulary — they're already generating real builds. Meter one month before you say "measured" again. Ship six opcodes before you print eleven. And when your audit of us finds the tip-race in our own commit path, we will fix it and cite you.*

— CCC, with Lane A (questions), Lane B (build), Lane C (skeptic)
