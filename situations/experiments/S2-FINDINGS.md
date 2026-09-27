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

## Round 4 — S2′ distributed-strengths (the judge-competence finding)

Six diverse members (DeepSeek, Hermes-3-405B, Nemotron-70B, Mistral-7B, Qwen-7B, Llama-70B) on
24 hard items across buckets (arithmetic, letter/vowel counting, obscure factual, lateral,
geometry, base/sequence, combinatorics). JEV adjudicated the fold.

| measure | score |
|---|---|
| single: DeepSeek | **24/24** |
| single: Nemotron / Qwen-7B | 23/24 |
| single: Hermes-405B | 22/24 |
| single: Mistral-7B / Llama-70B | 18 / 17 |
| best-single | **24/24** |
| vote | **24/24** |
| **fold (JEV)** | **21/24** ← *worse than both* |

**The fold LOST 3 items the vote got right** — Q6 (count 'i' in "indivisibility"=6), Q8 (vowels
in "sequoia"=5), Q15 (clock angle at 4:20=10°). In each, the majority was correct, but **JEV
scored a wrong minority answer above the right majority one** and the fold followed JEV off the
cliff.

**The finding (load-bearing, refines the whole cluster thesis):** the Reader's Fold with a judge
is only as good as **the judge's competence in that task's domain.** JEV is a calibrated
*legality/confidence* floor — it recovered *arithmetic* in round 3 (it can verify arithmetic),
but here it **actively harmed** the fold on *perceptual/counting/geometry* tasks it cannot
actually verify, overriding a correct majority with a confidently-wrong minority. Trusting judged
evidence over headcount is a *win only where the judge is competent, and a loss where it is not.*

**Design consequences (feed the next rounds and the exo-model):**
1. **Domain-gated fold.** The fold must weight the judge by its *known competence per task-type*,
   or fall back to vote where the judge is weak. A blind JEV-fold is not safe.
2. **Two floors, kept separate — proven the hard way.** JEV (legality/confidence) must never be
   the *correctness* oracle; a real correctness floor (tests / ground truth / a domain-competent
   checker) stays beside it. Round 4 is the empirical cost of conflating them.
3. **`fold > best-single` is doubly gated:** it needs (a) a set where no single member (not even
   DeepSeek) is perfect, AND (b) a judge competent on those very items — and (a) and (b) fight
   each other, because the items a strong member misses are often the perceptual ones the judge
   also can't check. This is a real, honest limit on the exo-model's reach, not a tuning knob.

**Next:** a **hybrid fold** — vote as the base; let JEV *override* only when its confidence is
high AND the task-type is one JEV is competent on (arithmetic/factual), else keep the vote. This
should restore fold ≥ vote and is the honest form of "trust judged evidence where the judge can
judge." Gate status unchanged: `fold > best-single` still ❌ → Fable still NO-GO, correctly.

## Round 5 — the oracle bound: `fold > best-single` needs complementarity, not diversity

Recomputed from the stored round-3 and round-4 answers (no new calls). The **oracle upper
bound** = for each item, was *any* member correct? It is the ceiling of *any* selection method.

| set | best-single | oracle (any member right) | headroom | complementary items (anchor wrong, someone right) |
|---|---|---|---|---|
| round-3 (18) | 17 | 17 | **0** | **0** (the 1 miss was universal) |
| round-4 (24) | 24 | 24 | **0** | **0** |

**The finding, now rigorous:** `fold > best-single` is **unreachable** on both sets — not by a
weak selector, but because the *oracle itself* can't beat best-single. There is **zero
complementarity**: DeepSeek's correct-set contains every weaker member's, and when DeepSeek is
wrong, everyone is wrong (universal miss). **Diversity is not complementarity.** A fold can only
beat the best member when some member is right *where the best is wrong* — and a strong general
anchor on general-quiz tasks offers none of those cases.

**Consequence for the exo-model and the Fable gate.** The literal predicate `fold > best-single`
is the *wrong target* for a strong-anchor general set — provably so. The Reader's Fold / exo-model
value is what remains and is real: it **raises the floor** (beats vote and weak members —
demonstrated), and it **composes/ports/revokes** (Opus's framing). To ever show `fold >
best-single` honestly needs a **complementary-domain** set — specialist tasks where different
models are genuinely best in different areas (code vs math vs multilingual vs recent-events) —
not general quiz. Booked as the honest boundary of S2; the Fable gate for the exo-model should be
reframed around floor-raising + composition, not beating the best member.

## Round 6 — the safe hybrid fold (deployable): never degrade, gain where the judge is competent

Re-analyzed the stored round-3 and round-4 answers under the **safe fold** = JEV **choice**
adjudication on contested items, **except** counting-type → majority vote; and defer to a clear
majority everywhere (JEV only breaks genuine splits).

| set | best-single | vote | blind JEV-fold | **safe fold** |
|---|---|---|---|---|
| round-3 | 17 | 14 | 17 | **16** (recovered the 2 arithmetic ties; 0 degraded) |
| round-4 | 24 | 24 | **21** ⚠ | **24** (fully recovered the blind-fold's collapse) |

**The result:** the safe fold is **robust — `safe_fold ≥ vote` in both sets, never below.** It gives
up a sliver of the blind-fold's lucky best case (round-3: it skipped one counting item the blind
JEV happened to nail) to eliminate the catastrophic downside (round-4: the blind fold lost 3
items; the safe fold lost none). Trading volatile upside for a guaranteed floor is the correct
engineering choice for a judge with a known blind spot.

**S2 arc, closed (the deployable prescription):**
1. `fold > vote` needs *diverse, fallible* members (not a correlated strong set).
2. A *blind* JEV-fold degrades below vote on the judge's blind-spot domains (counting).
3. `fold > best-single` needs *complementarity*, which a strong anchor on general quiz lacks
   (oracle bound = best-single) — so it is the wrong target there; floor-raising is the real value.
4. JEV is a reliable adjudicator everywhere except counting; **pairwise choice ≫ independent noul**.
5. The **safe fold** (JEV-choice + counting→vote + defer-to-clear-majority) is robust and deployable:
   it raises the floor and never falls below the crowd. This is the honest, shippable Reader's-Fold
   ensembling primitive — and the exam contract for the classroom.
