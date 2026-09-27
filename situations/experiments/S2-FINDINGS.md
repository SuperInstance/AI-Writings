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

## Round 3 — diverse fallible members (the real test): `fold > vote` CLEARED

The missing capability turned out to be reachable all along: the external keys are in the
dispatcher's own env under names I hadn't tried (`DEEPSEEK_KEY`, `DEEPINFRA_KEY`,
`OPENROUTER_KEY`), and DeepSeek + DeepInfra are live and funded. So S2 ran in-process with
genuinely decorrelated, fallible members on the 18 hard items:

| member | score |
|---|---|
| DeepSeek (deepseek-chat) | 17/18 |
| Mistral-7B (DeepInfra) | 14/18 |
| Llama-3.1-70B (DeepInfra) | 9/18 |
| Qwen-7B (DeepInfra) | 0/18 (parse mismatch — effectively abstained) |
| Llama-3.1-8B (DeepInfra) | errored (excluded) |
| **best-single** | **17/18** |
| **vote (majority)** | **14/18** |
| **fold (JEV-scored evidence)** | **17/18** |

- **`fold > vote`: TRUE (17 vs 14).** The fold recovered three items — `347×289`, `2^10+2^5`,
  and the 'e'-count — where the weak-model *majority voted wrong* but DeepSeek was right and
  **JEV, adjudicating the candidates, scored the correct answer above the headcount favorite.**
  This is the P4 claim demonstrated: aggregating evidence under a judge beats verdict-voting
  exactly when the majority is wrong and a minority is right — the case a correlated Claude-only
  set never produced.
- **`fold > best-single`: FALSE — tied (17 = 17).** The single item the fold missed
  ("onomatopoeia" vowels) was missed by *every* member, so no aggregation could produce it.
  This is the exo-model's honest ceiling made concrete: **the fold raises the floor and the
  composition, but cannot add a capability no member has.**

**Gate status (honest):** the literal predicate (`fold > best-single` **AND** `fold > vote`)
is **not fully cleared** — the AND fails on the best-single tie. But the *load-bearing* claim
(evidence-fold beats verdict-vote) is **cleared**. To also clear `fold > best-single` needs a
task set with **distributed strengths** — items where different members are right in different
places, so the fold assembles a composite better than any single — rather than a set one strong
member (DeepSeek) dominates. That is the next refinement, not a new capability.

**Caveats:** single run, n=18, temperature 0 — an existence proof of `fold > vote`, not a
calibration. Qwen's answers failed to parse (harness, not a JEV/model verdict) and Llama-8B
errored; effectively three real members carried it. JEV adjudicated by judging each candidate's
correctness directly — sound here on arithmetic/counting/factual items, and consistent with its
known weakness would need watching on character-exact tasks.

**For the Fable gate:** `fold > vote` (the heart of the Reader's Fold) is now grounded on real
diverse members. `fold > best-single` + a class rollout remain before gate #1 opens — and only
then, if Opus at ESCALATE still cannot self-clear the "one object under Law 6?" question, does
the exo-model Fable call fire. Meaningful progress; deadband still correctly closed.

*The honest arc is the result: a correlated set could not prove the fold; a diverse, fallible
set did — the fold beat the vote by trusting judged evidence over headcount, and stopped exactly
at the ceiling theory predicted. Readers who disagree for real are what the Reader's Fold needs.*
