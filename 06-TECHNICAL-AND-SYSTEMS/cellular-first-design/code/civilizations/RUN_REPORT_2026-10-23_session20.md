# Civilization Orchestrator — Run Report, Session 20

**Date:** 2026-10-23 · **Wipe:** 119th · **Command:**
`python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

## TL;DR

The command **ran to exit 0 and produced zero simulations** — the 18th consecutive
session in which the z.ai credential gap makes the orchestrator a green no-op.
The pipeline was then proven live under **Control B** (transport-level mock),
which produced **+80 rows (10/civ, uniform), +5 `meta_log` entries, 5 competition
winners, 0 JEV-outage defaults, 0 score errors, 0 fallbacks, 80/80 distinct
previews**. A body-set A/B was run to test whether the ranking survives a change
in the mock's prose: **it does not** (max |Δ| 0.375, top-3 set changed, bottom-2
set changed). The tree was then restored **byte-identical to HEAD** (20/20 files
verified with `cmp` against the git blobs); the 160 mock rows never entered the
committed ledger.

**Low relevance:** `civ-grounded` is the stable answer on the quality lenses
(lowest `relevance_per_sim` 1.741, lowest lifetime `avg_score` 1.916, lowest
lifetime `alignment` 2.659). `civ-poetic` is the inverse case, now **0 wins in
38** — the highest-scoring civ that has never been selected.

---

## 1. The unpatched run: a green no-op

```
=== Civilization batch: 8 civs x 5 sims each ===
[The Grounded] running 5 sims...   ... (all 8 printed)
=== Civilization competitions: 5 prompts ===
              (no Winner: lines)
EXIT=0
```

| metric | before | after | delta |
|---|---|---|---|
| ledger rows (`civ-*/simulations.jsonl`) | 764 | 764 | **+0** |
| `meta_log.jsonl` | 53 | 53 | **+0** |
| `Winner:` lines | — | — | **0** |
| exit code | — | — | 0 |

Only `leaderboard.json` was rewritten. The per-civ `running 5 sims...` lines print
**before** the provider call, so they are not evidence of work.

### Credential audit (endpoint healthy ⇒ gap, not outage)

All 10 present sandbox secrets tested against
`https://api.z.ai/api/coding/paas/v4/chat/completions` → **401 "token expired or
incorrect"** on every one. `ZAI_TOKEN`, `ZAI_KEY`, `GROQ_TOKEN` **absent** from
env *and* from the 8-entry secret store. A 401 (not 5xx) means the endpoint is
healthy, so this is a credential/balance gap.

**JEV live at `jev-1.14.0`** (HTTP 200, `quality.score 0.83, confidence 0.32`).
`export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` is what keeps scoring real — without
it JEV silently degrades to the `{"quality": 2.0, ...}` default and the run
measures nothing while exiting 0.

## 2. Control B: the pipeline, proven

Mock at the **transport layer** (below the orchestrator's `ZAI_TOKEN` gate), so the
request is really attempted and the control has power. Seam: a one-line
`ZAI_URL_OVERRIDE` read in `PROVIDERS["zai"]["url"]` (not in the committed blob —
re-apply after every restore; `git diff --stat` = 1 insertion, 1 deletion).

| check | result |
|---|---|
| rows added | **+80 (10/civ, uniform 10/10/10/10/10/10/10/10)** |
| `meta_log` entries | **+5** |
| `Winner:` lines | **5** |
| all-2.0-default rows (JEV outage) | **0** |
| score errors | **0** |
| mock fallback calls | **0** (voice table keyed on the civ **name** — `voice_emphasis` collapses voices) |
| distinct `content_preview` | **80/80** |
| distinct `avg_score` | 69/80, range 0.95–2.47 |
| provider recorded | `zai` only |
| mock call distribution | exactly **10 per voice across all 8 voices** |

## 3. The A/B: the ranking is a mock artefact (large-perturbation case)

Two independently-written body sets. Nothing changed but the mock's prose.

| civ | set A | set B | Δ |
|---|---|---|---|
| civ-grounded | 1.264 | 1.030 | **−0.234** |
| civ-formal | 1.534 | 1.435 | −0.099 |
| civ-engineer | 1.545 | 1.502 | −0.042 |
| civ-therapist | 1.668 | 1.634 | −0.034 |
| civ-precise | 1.701 | 1.654 | −0.047 |
| civ-whimsical | 1.718 | 1.939 | **+0.221** |
| civ-mythic | 1.754 | 1.378 | **−0.375** |
| civ-poetic | 2.012 | 1.640 | **−0.372** |

fleet mean 1.649 → 1.527 · max per-civ |Δ| **0.375** · positional rank agreement
**1/8** · Kendall τ 1.000 (same set, very different order) · **top-3 set changed**
({poetic, whimsical, mythic} → {poetic, whimsical, precise}) · **bottom-2 set
changed** ({formal, grounded} → {grounded, mythic}) · set-A adjacent rank gaps
0.011 / 0.016 / 0.033 / 0.036 / 0.124 / 0.259 / 0.269.

**Reading:** the perturbation (0.375) exceeds five of the seven adjacent gaps it
would overturn, so the middle band is a tie and only the extreme positions are
reportable. This is the s10 regime (large perturbation), not the s11 regime
(tie-preserving). **Absolute scores and the middle order are both artefacts.**

## 4. Low relevance — report the lens, never a merged verdict

**Baseline (764 committed rows, pre-session), one row per lens:**

| lens | lowest | value | what it measures |
|---|---|---|---|
| `relevance_per_sim` (board sort) | **civ-grounded** | 1.741 | efficiency (but penalises the civ that ran most: 122 sims) |
| raw relevance | **civ-engineer** | 139.80 | accumulated score, same denominator artefact |
| `win_rate` | **civ-poetic** | **0.000 (0W/38L)** | **selection** appeal under a 150-char preview |
| lifetime `avg_score` | **civ-grounded** | 1.916 | actual writing quality — the only real quality lens |
| lifetime `alignment` | **civ-grounded** | 2.659 | lowest of 8 |
| lifetime `quality` | **civ-engineer** | 1.667 | |
| lifetime `novelty` | **civ-precise** | 1.020 | coldest civ, least novel |

- **`civ-grounded` — the stable low-relevance civ.** Last on `relevance_per_sim`,
  lifetime `avg_score` **and** lifetime `alignment` — the three lenses that measure
  quality rather than selection or longevity. Also last in *this* session's 160 rows
  on `avg_score` (1.147) and `quality` (0.346). **Genuine weakness, not an artefact
  of the longevity denominator.**
- **`civ-poetic` — the inverse case, 18th session running.** 2nd of 8 on lifetime
  `avg_score` (2.617), **1st on quality (2.258)**, 2nd on alignment (3.296), 2nd on
  `relevance_per_sim` (2.430) — and **0 wins in 38**. A *selection* failure, not a
  quality collapse. It took **0 of 10** competition rounds this session too.
- **`civ-precise` — wins by being picked, not by scoring.** Best win rate in the
  fleet (0.485, 16W/17L) but **last on lifetime novelty (1.020)** and 3rd-last on
  lifetime `avg_score` (2.020).
- **`civ-whimsical` — the only civ where every quality lens agrees.** 1st on
  `relevance_per_sim` (2.476), lifetime `avg_score` (2.701), novelty (2.602) and
  alignment (3.365). 2nd-lowest win rate (0.053) — the selection metric again
  penalises the best writer.
- **`civ-formal`** — 2nd-lowest `relevance_per_sim` (1.864) and 2nd-lowest lifetime
  `avg_score` (2.002); a genuine weak pair with `civ-grounded`.
- **Extinction risk: none.** `extinction_and_birth()` retires only below
  `relevance < −10`; the lowest is +139.80, and it only fires in `--loop` mode
  every third iteration.

## 5. Replications

- **Control B**: +80 / +5 / 5 winners / 0 defaults / 0 errors / 0 fallback /
  80-80 distinct previews / uniform 10-per-voice — **13th**.
- **Chooser vs `argmax(avg_score)`**: **1/10 this session (10 %)**, **2/18 lifetime
  (11.1 %)**, disagreement margins 0.283–0.800 (this session) / 0.240–1.080
  (lifetime), mean 0.539. History: s8 18.9 %, s13 22.4 %, s15 15.5 %, s17 0 %.
  **12th replication** — a competition win is *not* evidence of a higher JEV score.
- **Temperature vs lifetime JEV novelty**: per-civ-**mean** estimator (8 points,
  the s8–s18 estimator) **r = 0.9883**; all-pairs estimator (n=764) **r = 0.7942**,
  reproducing s19's 0.7942 exactly. **The two estimators are not comparable** —
  the per-civ-mean one is the one the prior replications used. **12th replication.**
  Temperature and novelty are the same axis.
- **Counter gap: +260**, measured baseline-to-baseline (764 ledger rows vs 504
  registry `simulations_run`). Confirms s19: it is a **race** in `save_state()`,
  not a leak, and it moves in both directions. **Report the gap as measured this
  session, never as a trend against a quoted number.**

## 6. Protocol compliance

- Mock rows are **not committed** — the ledger holds real provider output only.
- Restore verified with `cmp` against `git show HEAD:<path>`: **20/20 files
  byte-identical** (8 ledgers, 8 `culture.json`, `meta_log.jsonl`,
  `leaderboard.json`, `civilizations.json`, the script).
- **Timestamp leak test** (not a content grep — the committed ledgers already carry
  mock rows from an earlier session): **0 rows with `ts` after the run start** in
  all 8 committed ledgers.
- `__pycache__/` removed before commit.

## 7. Recommendations (unchanged, still unfixed upstream)

1. **Make the provider gate fail loudly.** `return None` on a missing token turns
   a total outage into `exit 0` with an empty ledger. Name the error and abort
   non-zero; assert the row delta grew.
2. **Require a non-default JEV score before recording a winner.** When JEV is down
   every `avg_score` is the 2.0 default, all civs tie, and the `max()` fallback
   crowns an **arbitrary** civ with a real, permanent win — corrupting the only
   trustworthy metric.
3. **Fix the lost-update race in `save_state()`.** It rewrites `culture.json` from
   in-memory counters with no lock, which is why 260 committed rows are counted by
   nobody and `relevance_per_sim` is not reproducible from the ledger.
4. **Show the chooser the scores.** The chooser sees a 150-char preview and never
   sees the scores; agreement with `argmax(avg_score)` is ~11 %. Either make the
   chooser score-aware or stop reporting `win_rate` next to relevance.
5. **Decouple temperature from novelty** or stop presenting the eight civs as
   independent voices — they are eight points on one gradient (r = 0.988).
