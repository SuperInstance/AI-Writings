# S2 pilot — the Reader's-Fold ensemble (honest result: predicate not cleared, and why)

*Run 2026-09-27 by the dispatcher, in-process. Three heterogeneous readers (Claude Haiku
4.5, Sonnet, Opus) each answered a benchmark independently; JEV (`typesafe.ai jev-1.13.0`)
adjudicated. This is gate #1 toward the exo-model second-Fable call
(`arch/THE-CLASSROOM.md` §8). It did **not** clear — and the reason is the finding.*

## Predicate (from `arch/INTELLIGENCE-CLUSTERS.md` S2)
`fold_ensemble.passrate > max_i(single_model_i)` **AND** `> vote_ensemble`, with the fold
recomputable by a stranger from the booked answers + weights.

## What happened

**Round 1 (14 "tricky" items):** all three readers scored **14/14**, zero disagreement.
The predicate is *vacuous* at ceiling — nothing to distinguish fold from vote when everyone
agrees and everyone is right. (Honest: my "tricky" questions weren't tricky for frontier
models.)

**Round 2 (16 frontier-splitter items — long-word letter counts, 347×289, clock angles,
chessboard squares, look-and-say):**

| measure | score |
|---|---|
| single: Haiku | 15/16 |
| single: Sonnet | 16/16 |
| single: Opus | 16/16 |
| **best-single** | **16/16** |
| vote-ensemble | 16/16 |
| confidence-fold | 16/16 |
| contested items | **1** (Q11 only) |

The one disagreement: Haiku spelled "necessary" reversed as `yrasecen` (dropped an 's');
Sonnet and Opus both gave `yrassecen` (correct). The majority was right, so vote recovered
Haiku's error (15→16) and fold agreed with vote.

**JEV adjudication of the contested item** (`is this the exact reverse spelling?`):
`yrassecen` (right) → noul **0.82**; `yrasecen` (wrong) → noul **0.75**. JEV ordered right
above wrong, but *thinly*, and did not confidently reject the wrong one — consistent with
JEV being a legality/confidence floor, not a hard correctness oracle on character-exact tasks.

## The finding (why the predicate can't clear here)

1. **You cannot beat a perfect single model.** With Sonnet and Opus at 16/16, no ensemble
   can exceed best-single. `fold > best-single` is unreachable by construction.
2. **fold > vote needs the majority to be WRONG and a minority RIGHT with better evidence.**
   That case never occurred: the sole disagreement had the majority correct, so fold = vote.
   The Reader's-Fold's distinctive power — aggregating *evidence* to overturn a wrong
   *majority* — is exactly what a strong, correlated member set never exercises.
3. **Frontier Claude tiers are too strong and too correlated** to be a fair test of S2.
   The ensemble's only observed benefit was recovering the *weakest* member's lone error
   (Haiku 15→16) — real, but it is "beats worst," not the S2 claim.

## What this means for the gate (and the deadband)

**S2 gate #1 to the exo-model Fable call is NOT cleared — correctly.** The deadband holds.
The blocker is precise and grounded: **member diversity.** The fold beats the vote only with
*decorrelated, fallible* members whose errors differ — i.e. the external roster
(DeepSeek/DeepInfra + small models that fail differently), which are **not reachable in the
dispatcher's env** (only `TYPESAFEAI_KEY`/`MOTHQUANTUM_*` are; DeepSeek/DeepInfra keys are
unset here — likely only in child-session envs). No study should fake this.

## Salvage (O8 — the pivot that teaches)

The pilot was not a zero. It **validated the whole S2 pipeline end-to-end** — independent
readers → JEV adjudication → vote and fold aggregation → predicate test — all booked and
replayable from `/tmp/s2*/reader_*.json` + `truth.json`. And it **pinpointed the one
missing capability**: genuinely diverse, fallible members. Concrete next step to clear the
gate:

1. Get DeepSeek + DeepInfra reachable to the runner (keys live in-env, or run S2 in a child
   session that holds them via the confirmed curl route-around).
2. Re-run S2 with **decorrelated members** (a small open model + DeepSeek + a Claude tier)
   on **frontier-hard tasks where best-single < 100%**, so majority-wrong/minority-right
   cases actually arise.
3. Only if `fold > vote` then holds — and one class rollout exists — does gate #1 open, and
   only if Opus at ESCALATE still cannot self-clear the "one object under Law 6?" question
   does the exo-model Fable call fire.

*The honest negative is the result: the Reader's Fold needs readers who disagree for real.
Our strongest, most-correlated members are the wrong crucible to prove it in.*
