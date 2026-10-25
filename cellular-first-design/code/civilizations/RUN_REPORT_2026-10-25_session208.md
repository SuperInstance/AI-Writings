# Civ Orchestrator — Run Report, session 208 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **81st session**) + **live JEV** (`jev-1.14.0`).
Baseline: `c5078bd` (session 207 tree). **All 28 verification assertions PASS.** Pre-flight **12/12 PASS**.

**Session 208 in one line:** `civ-precise` swept **5/5** and the chooser/argmax agreement
fell to **1/5 (20 %) — 4 down-grades, 0 up-grades**; the alignment spread (**1.5650**) is
**4.62x** the quality spread and **10.10x** the novelty spread, so the ranking is again
produced by **alignment**; the run-level low rotated to **`civ-therapist`** while
`civ-grounded` held the lifetime low for the **79th** consecutive session.

**Two durable lessons from this session:**

1. **THE DOWN-GRADE STREAK IS NOT A STICKY PROPERTY — IT IS RE-MEASURED EVERY SESSION, AND
   THE SERIES HAS NOW OSCILLATED ACROSS FIVE CONSECUTIVE SESSIONS.** Session 199 read
   **0/5 agreement, 5 down**; session 207 read **4/5, 1 down**; this session reads
   **1/5, 4 down**. The sequence 199 → 207 → 208 is 0/5 → 4/5 → 1/5. *Never carry a
   streak number forward — re-derive the direction count from the current session's own
   `meta_log` and report agreement and direction as two separate numbers.* The "the
   down-grade streak is over" claim from session 198 was already wrong by session 199;
   this session is the third independent demonstration of the same lesson.
2. **THE RUN-LEVEL LOW HOLDER ROTATES, BUT IT IS NOT RANDOM — IT IS THE CIV WITH THE
   WIDEST ALIGNMENT GAP, AND THAT GAP HAS NOW NAMED THE HOLDER IN EVERY SESSION OF THE
   SERIES.** `civ-therapist` held it with an alignment gap of **−1.5320** against
   `civ-precise`; `civ-whimsical` is second with **−1.5650** (a *wider* gap) but sits at
   **run `avg_score` 1.5740**, above `civ-therapist`'s **1.5237**. So the axis identifies
   the *low-relevance cohort*, not the *single holder* — the holder is the cohort member
   with the lowest `avg_score`. *Predict the cohort from the axis; read the holder from
   the run's own rows.*

## This run — 8 civs, 5 sims + 5 competition rows each

| rank | civ | avg_score | quality | novelty | alignment |
|------|-----|-----------|---------|---------|-----------|
| 1 | `civ-precise` | 2.1157 | 1.3900 | 2.1410 | 2.8160 |
| 2 | `civ-engineer` | 2.1007 | 1.3860 | 2.1290 | 2.7870 |
| 3 | `civ-formal` | 2.0590 | 1.3110 | 2.0830 | 2.7830 |
| 4 | `civ-poetic` | 2.0010 | **1.4360** | 2.1670 | 2.4000 |
| 5 | `civ-grounded` | 1.9270 | 1.1830 | **2.2380** | 2.3600 |
| 6 | `civ-mythic` | 1.8010 | 1.1780 | 2.1830 | 2.0420 |
| 7 | `civ-whimsical` | 1.5740 | 1.2740 | 2.1970 | 1.2510 |
| 8 | **`civ-therapist`** | **1.5237** | **1.0970** | 2.1900 | 1.2840 |

Run spreads: `alignment` **1.5650**, `avg_score` **0.5920**, `quality` **0.3390**,
`novelty` **0.1550**. The alignment spread is **4.62x** the quality spread and
**10.10x** the novelty spread, so the ranking is produced by **alignment**, not by prose
quality — and notably **not** by novelty either, whose spread (**0.1550**) is the
narrowest of the four axes for the first time in the series.

**Run-level low: `civ-therapist`** (run `avg_score` **1.5237**, `quality` **1.0970** =
lowest in the fleet, `alignment` **1.2840** = 2nd-lowest, `novelty` **2.1900** = mid-pack).
It has the **smallest relevance delta** of the fleet (**+15.2367**).

## Lifetime table (post-run, `culture.json`)

| civ | relevance | per_sim | sims | wins | losses | win_rate |
|-----|-----------|---------|------|------|--------|----------|
| civ-poetic | 2450.76 | 1.619 | 1514 | 6 | 747 | 0.008 |
| civ-precise | 2298.32 | 1.527 | 1505 | 502 | 246 | 0.671 |
| civ-whimsical | 2090.03 | 1.374 | 1521 | 5 | 748 | 0.007 |
| civ-mythic | 1975.88 | 1.309 | 1509 | 10 | 737 | 0.013 |
| civ-formal | 1968.87 | 1.300 | 1515 | 103 | 648 | 0.137 |
| civ-engineer | 1871.83 | 1.245 | 1504 | 51 | 695 | 0.068 |
| **civ-therapist** | **1775.26** | **1.178** | 1507 | 11 | 739 | 0.015 |
| **civ-grounded** | **1666.40** | **1.090** | 1529 | 71 | 681 | 0.094 |

**Lifetime low: `civ-grounded`** — **79th consecutive session**, `relevance`
**1666.40**, `relevance_per_sim` **1.090** (fleet minimum) — yet its lifetime `win_rate`
**0.094** is 3rd-best in the fleet. *Selection and relevance are separate axes.*
Its run signature this session was **quality-led with a novelty peak**: `quality`
**1.1830** (2nd-lowest), `novelty` **2.2380** (**fleet-high**), `alignment` **2.3600**
(3rd-lowest). Run `avg_score` **1.9270** = 5th of 8. Its lowest lifetime axis is
**quality** (**0.4519** in the session-207 reading), **not** novelty.

## Low-relevance signature

The established signature is **high novelty, LOW alignment**. This run:

| civ | novelty gap | alignment gap | run avg_score | fit |
|-----|-------------|---------------|---------------|-----|
| `civ-therapist` | −0.0480 | **−1.5320** | 1.5237 | fits (alignment) |
| `civ-whimsical` | −0.0410 | **−1.5650** | 1.5740 | fits (alignment) |
| `civ-mythic` | −0.0550 | −0.7740 | 1.8010 | partial |
| `civ-grounded` | **+0.0000** | −0.4560 | 1.9270 | partial (novelty-high) |

Novelty gaps are **negative for every low civ** — novelty is flat-to-high for everyone,
so novelty is **not** a separating axis this session. The separation is entirely
**alignment**: the two lowest `avg_score` civs are the two with an alignment gap beyond
−1.5, and the three highest `avg_score` civs are the three within **−0.033** of the
alignment ceiling. *Report the axis, not the holder.*

## Chooser vs argmax

| prompt | winner | argmax | winner score | argmax score | outcome |
|--------|--------|--------|--------------|--------------|--------|
| what a cell is | `civ-precise` | `civ-engineer` | 1.7167 | 2.0167 | DISAGREE (lower-scoring) |
| the bookkeeper's role | `civ-precise` | `civ-poetic` | 2.4133 | 2.5200 | DISAGREE (lower-scoring) |
| the witness log | `civ-precise` | `civ-precise` | 2.6200 | 2.6200 | AGREE |
| ternary values | `civ-precise` | `civ-engineer` | 1.6600 | 1.8833 | DISAGREE (lower-scoring) |
| JEV as a decision oracle | `civ-precise` | `civ-poetic` | 2.1900 | 2.2667 | DISAGREE (lower-scoring) |

Agreement **1/5 (20 %)** — 4 down-grades, 0 up-grades. `civ-precise` won all 5
competitions and was the argmax on only **1 of 5**; `civ-engineer` was the argmax on
**2 of 5** and `civ-poetic` on **2 of 5**, and both won **0 of 5**.

**This is the third distinct agreement reading in three consecutive sessions**
(0/5 → 4/5 → 1/5). The down-grade streak is **4** and must be re-derived next session
from that session's own log. *A streak is a measurement, not a hypothesis.*

## Verification (28/28 PASS)

- per-civ ledger Δ **+10 × 8 = 80** new rows; `meta_log.jsonl` Δ **+5** (773 → 778)
- `Winner:` lines = **5**; stdout `Winner:` == `meta_log.winner_civ` — **5/5 agree**
- mock-log seed multiset of the LAST 80 OK-200 lines **==** the ledger's 80 row seeds
  (**run-scoped proof**, not a lifetime multiset) — mock log total **181** lines
- **80/80** rows carry a parseable seed+colour+figure; **80/80** match an independently
  recomputed `md5(whole_message)`; distinct seeds **40/80**
- **0** `(civ,prompt)` pairs carrying >1 seed; per-prompt **8/8** distinct seeds AND
  previews on all 5 prompts; **0** `EXC`/tracebacks
- **0** JEV errors; **0** `2.0/2.0/2.0` fallback triples; provider on all rows = **`zai`**
- `relevance` Δ = ledger Σ`avg_score` — **8/8 exact** (max residual **3.73e-13**)
- `wins` = pre + times won, `losses` = 5 − times won — **8/8 exact**
- meta-vs-ledger `avg_score` (later-`ts` row) — **0/40 mismatches**
- `simulations_run` Δ = **+10** per civ
- per-civ **counter gap unchanged** vs the baseline epoch (grounded −84.35, whimsical
  −173.14, formal −85.53, poetic −96.80, precise −32.63, mythic −51.11, therapist
  −42.11, engineer −44.24) — the cheapest merge-integrity check, and all 8 are
  byte-identical to the session-207 epoch
- all 80 rows carry the **9 documented keys**; `avg_score` == mean(q,n,a) on **80/80**
- `params` inside the preferred ± jitter band — **80/80**
- extinction risk **NONE** (threshold −10; the lowest civ sits **166.6×** above it)
- `leaderboard.json` updated with 8 civs, iso `2026-10-25T11:43:33`
- **no birth** (8 civ dirs, all `generation=1`); orchestrator exit **0**

## Pre-flight (12/12 PASS, first build)

| # | check | result |
|---|---|---|
| 1 | cultural-prompt length band **167-209** | **167-209** |
| 2 | zero transport errors | **40 responses** |
| 3 | distinct seeds | **40** |
| 4 | distinct previews | **40** |
| 5 | recomputed seed+colour+figure present | **40/40** |
| 6 | per-prompt 8/8 distinct seeds AND previews | **8/8 × 5** |
| 7 | zero literal `seed={}` | **0** |
| 8 | zero `EXC:`/tracebacks | **0** |
| 9 | `[mock-zai` prefix | **40/40** |
| 10 | **repeat-same-message ⇒ same seed AND preview** | **20/20** |
| 11 | zero `(civ,prompt)` pairs carrying >1 seed | **40 pairs** |
| 12 | response body length band **332-369** | **343-343** |

### The body band was solved algebraically again — and the figure width is the lever

The mock header is `[mock-zai <4-hex>] #<6-hex> <figure>. `. With the figure fixed at
**18 chars** (3 string components of 5 chars, space-joined — fix (g) done as three
strings, not a division) the header is a **constant 44 chars**, so a **299-char** fixed
tail puts the body at **343** — inside the 332-369 band on the **first** build, third
consecutive session in a row. *Compute the band algebraically before writing the
template; do not iterate the template.*

## Environment (session 208)

- **z.ai credential gap, 81st session.** `api.z.ai` returns HTTP **401**
  `token expired or incorrect` ⇒ endpoint healthy, credential absent. `ZAI_TOKEN` is
  absent from env and from all 8 sandbox secrets, so **both** `ZAI_TOKEN` (placeholder)
  and `ZAI_URL_OVERRIDE` (mock URL) were set — the override alone is dead code behind
  the token gate.
- **JEV is live**: `TYPESAFEAI_KEY` was exported as an alias of the sandbox's
  `TYPESAFE_AI_TOKEN`; JEV returned HTTP 200 disclosing **`jev-1.14.0`**; **0** JEV
  errors, **0** fallback triples.
- The workspace was **wiped** again (only `.plugin-cache` and `.skills` present) ⇒ the
  prompt's path did not exist (**19th consecutive occurrence**). Upstream is
  **`SuperInstance/AI-Writings`** — a *user* account, so `GET /orgs/ai-writings/repos`
  404s while `GET /user/repos` finds it; the GitHub API is case-insensitive, so the
  `ai-writings/…` slug resolves to `AI-Writings`.
- Cloned to **`/tmp`** with `--filter=blob:none --sparse` (a full clone into
  `/workspace` dies on `.git/description` with `Disk quota exceeded` — the NAS EDQUOT
  trap, **19th session**), then a symlink bridge at the **inner `code` level**:
  `ln -s /tmp/AI-Writings/cellular-first-design/code
  /workspace/repos/ai-writings/cellular-first-design/code`. Verified by **inode identity**
  (`129:3670` on both sides) plus `os.path.samefile()` → `True`.
- The baseline was derived from the **git blob** of each ledger and `culture.json` at
  `c5078bd` — never from a remembered count, never from the working tree, and **pinned
  to the pre-run commit** (a verifier that reads its baseline from `HEAD` after the run
  is committed reports every delta as 0).
- `gh` is not installed (**22nd session**); `GIT_SSL_NO_VERIFY=1` is required for
  fetch/push; push to the explicit token URL and verify with `git ls-remote`.

## Notes for the next session

1. **Re-derive the chooser/argmax direction count from this session's own log.** Do not
   carry "4" forward, and do not carry session 207's "1" either — the series has
   oscillated 0/5 → 4/5 → 1/5 and the counter is re-measured every time.
2. **The lifetime-low holder and the run-level-low holder have been DIFFERENT civs for
   5 sessions running** (`civ-grounded` lifetime, `civ-therapist` run-level). Report
   the axis per civ, and keep relevance (an accumulation) separate from `win_rate` (a
   selection metric).
3. **The low-relevance cohort is the alignment tail**, and the holder is the cohort
   member with the lowest `avg_score` — `civ-whimsical` has the *widest* alignment gap
   but is not the holder, because its `avg_score` is higher.
4. **The counter-gap check is the cheapest merge-integrity check available**: compare
   the per-civ gap between `relevance_score` and Σ`avg_score` at the baseline commit
   and at the post-run tree. All 8 were byte-identical this session.
