# Civilization Orchestrator — Session 250 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Fleet: 8 civs. Provider: **Control B mock** (z.ai credential gap, 96th session) + **live JEV** (`jev-1.14.0`).

## Environment notes

- **Task path absent.** `/workspace/repos/ai-writings/...` did not exist (112th session with the
  prompt path absent). The workspace was also **100 % full (NAS EDQUOT)** — a direct clone into
  `/workspace` fails with `close error: Disk quota exceeded`. Cloned to the overlay at
  `/tmp/ai-writings`, bridged the subdirectory chain to the hardcoded `CIVS_DIR` with symlinks,
  and verified the bridge with `os.path.samefile()` -> `True`.
- **z.ai live probe: HTTP 401** — endpoint healthy, credential absent. `ZAI_TOKEN` unset in the
  sandbox. The Control B mock (`tools/mock_zai.py`) was used with **both** `ZAI_TOKEN` (the gate
  in `call_provider`) and `ZAI_URL_OVERRIDE` (the destination). `ZAI_URL_OVERRIDE` alone is dead code.
- **`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`** before the run. Without the alias
  `jev_score` silently falls through to the `2.0/2.0/2.0` fallback triple.

## Pre-flight gate — 11/11 PASS, exit 0

40/40 requests 200, 40/40 distinct previews, 40/40 distinct seeds, 40/40 distinct seed-tuples,
all bodies **349 chars** (inside the 332-369 band), 38+162=200 geometry holds, 149-char
continuation, 5 distinct seeds per civ, 8 distinct seeds per prompt.

**Mock algorithm validated non-circularly**: the seed recompute was re-derived against the
**pre-existing** ledger (**not** this run's rows) — **3860/3860 exact matches** over the
recognizable historical rows, 0 mismatches.

## Ledger delta

- **+10 rows per civ, +80 total**; `meta_log` **983 -> 988** (+5); **18** files changed.
- Every new row carries the documented **9 keys**
  (`ts, civ, civ_name, provider, params, prompt, scores, avg_score, content_preview`);
  preview length **200** on every row; all 80 rows parse as JSON; **0 key/shape violations**.
- **JEV was live on all 80 rows**: 0 `error` fields, **0** `2.0/2.0/2.0` fallback triples,
  0 zero-confidence rows, confidence range **0.27 – 0.89**, **80/80 distinct score triples**.
- Prompt draw across the 80 new rows: witness log 21, bookkeeper 16, cell 15, ternary 14,
  JEV oracle 14.

### Counter reconciliation — 8/8 OK

The sim phase gives every civ +5 sims; the competition phase gives every civ **5 more sims**
(each competition calls `run_simulation` again) plus exactly one W or L. So
**dSims = 10** and **dW + dL = 5** for all 8 civs. Relevance deltas match the sum of the new
`avg_score` values to the last decimal on all 8 ledgers.

| civ | dW | dL | dSims | sum(new avg) | dRelevance |
|---|---|---|---|---|---|
| civ-grounded | 0 | 5 | 10 | 15.0733 | 15.0733 |
| civ-whimsical | 0 | 5 | 10 | 15.1667 | 15.1667 |
| civ-formal | 1 | 4 | 10 | 17.5000 | 17.5000 |
| civ-poetic | 0 | 5 | 10 | 20.7267 | 20.7267 |
| civ-precise | 4 | 1 | 10 | 19.9300 | 19.9300 |
| civ-mythic | 0 | 5 | 10 | 16.1767 | 16.1767 |
| civ-therapist | 0 | 5 | 10 | 12.6400 | 12.6400 |
| civ-engineer | 0 | 5 | 10 | 16.9500 | 16.9500 |

## Leaderboard (pre -> post, sorted by relevance_per_sim)

| civ | relevance | d | rel/sim | d | win_rate | wins |
|---|---|---|---|---|---|---|
| civ-poetic | 3318.54 -> 3339.26 | +20.72 | 1.725 -> 1.727 | +0.002 | 0.006 | 6 |
| civ-precise | 3189.66 -> 3209.59 | +19.93 | 1.666 -> 1.667 | +0.001 | 0.711 | 681 |
| civ-formal | 2760.98 -> 2778.48 | +17.50 | 1.434 -> 1.436 | +0.002 | 0.127 | 122 |
| civ-whimsical | 2734.70 -> 2749.87 | +15.17 | 1.416 -> 1.417 | +0.001 | 0.005 | 5 |
| civ-mythic | 2692.20 -> 2708.38 | +16.18 | 1.403 -> 1.404 | +0.001 | 0.010 | 10 |
| civ-engineer | 2639.39 -> 2656.34 | +16.95 | 1.379 -> 1.381 | +0.002 | 0.062 | 59 |
| civ-therapist | 2356.56 -> 2369.20 | +12.64 | 1.229 -> 1.229 | +0.000 | 0.011 | 11 |
| civ-grounded | 2360.67 -> 2375.74 | +15.07 | 1.217 -> 1.219 | +0.002 | 0.078 | 75 |

## Low-relevance civilizations

**`civ-grounded` and `civ-therapist` remain the bottom pair**, and they are again effectively
tied: **2375.74 vs 2369.20 = a gap of 6.54** on a ~2370-point scale (**0.275 %**). The step up to
`civ-engineer` (2656.34) is **287.14** — **44x** larger. The gap series reads
5.11 (s245) -> 3.17 (s246) -> 0.79 (s247) -> **6.54** (s250): the floor is still converged, but
the pair swapped positions (`civ-grounded` is now ahead).

**`civ-therapist` is the clearest low-relevance signal** — and this time it is a *two-axis collapse*:

- **Run-level:** the fleet's **lowest avg (1.264)** and the **lowest quality (0.528, 8th of 8)**
  and the **lowest alignment (0.860, 8th of 8)**, with the **narrowest band** (1.143 – 1.350).
  It sits **-0.413** below the fleet run mean of **1.677**; the next lowest (`civ-grounded`,
  -0.170) is less than half that gap. It won **0 of 5** competitions.
- **Lifetime:** the fleet's **lowest alignment (1.168)** and lowest lifetime quality (0.552).
  Novelty is its strength (run 2.404, 3rd of 8) — it writes *distinctive* prose that the
  oracle scores as **not sounding like its culture**. That is a *voice* failure, not a prose failure.
- Only `civ-therapist` is more than 0.25 below the fleet mean on the run axis.

**`civ-grounded` is the second low-relevance civ, on a different axis**: it holds the **lowest
lifetime relevance_per_sim in the fleet (1.219)** and the **lowest lifetime quality (0.548)**, but
its *alignment* (run 1.641, 5th of 8) is mid-pack and its novelty is 6th. It also shows the
**widest run spread** of the bottom pair (1.283 – 1.800). It won **0 of 5**.

**Low win rate is not low relevance.** `civ-poetic` holds the **highest** relevance (3339.26)
and the **lowest** win rate (0.006) — selection and relevance are separate axes.

### Extinction risk: NONE

Lowest relevance is **2369.20**, **237x** above the **-10** extinction floor. Registry size 8
(`max_civs` 12), all eight `generation=1`, and `extinction_and_birth` only runs in `--loop` mode
every 3 iterations — so a single batch triggers **no extinction and no birth**. The registry file
is **byte-identical** to its pre-run state.

## Chooser vs argmax — 0/5 agreement, 5 down-grades, 0 up-grades

| prompt | JEV winner | avg_score argmax | agree |
|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | no |
| the bookkeeper's role | civ-precise | civ-poetic | no |
| the witness log | civ-formal | civ-precise | no |
| ternary values | civ-precise | civ-poetic | no |
| JEV as a decision oracle | civ-precise | civ-poetic | no |

**Agreement 0/5 (0 %)**, **0 up-grades, 5 down-grades** — the structurally expected result, since
the chooser is a JEV `choice` question over `content_preview[:150]` and never sees `avg_score`.
`civ-poetic` was the argmax on **5 of 5** and won **0**; `civ-precise` won **4/5** with a
lifetime `win_rate` of **0.711** while sitting 2nd on lifetime relevance. Report the axis, not
the holder.

## Run summary

- 8 civs x 5 sims = 40 sim rows, plus 5 competitions x 8 civs = 40 more = **80 new rows**.
- `civ-precise` took **4 of 5** competitions, `civ-formal` 1, and the other six took **0**.
- 18 files changed; +80 ledger rows; +5 meta_log rows; registry unchanged; no extinction, no birth.
