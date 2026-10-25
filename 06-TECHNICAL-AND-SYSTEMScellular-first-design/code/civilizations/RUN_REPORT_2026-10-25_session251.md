# Civilization Orchestrator — Session 251 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Fleet: 8 civs. Provider: **Control B mock** (z.ai credential gap, **108th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `d0247fd` (session 250 tree). **Pre-flight gate: 40/40 PASS, exit 0.** **Run verification: ALL PASS (0 FAIL).**

## Environment notes

- **Task path absent.** `/workspace/repos/ai-writings/...` did not exist (**13th consecutive occurrence**).
  Workspace held only `.plugin-cache`. A direct clone into `/workspace` fails with
  `close error: Disk quota exceeded` (NAS EDQUOT) — **19th session**. Cloned to the overlay at
  `/tmp/ai-writings` and bridged the chain with a symlink `/workspace/repos/ai-writings -> /tmp/ai-writings`.
  Bridge verified with `os.path.samefile()` -> `True`.
- **Upstream is `SuperInstance/AI-Writings`** (capitalised). The `ai-writings/…` slug 404s on the
  repos API. `GET /search/repositories?q=cellular-first-design` does **not** surface it; resolved
  via `GET /search/code?q=civilization_orchestrator+in:path`.
- **z.ai live probe: HTTP 401** `token expired or incorrect` => endpoint healthy, credential absent.
  `ZAI_TOKEN` unset in env and absent from all 8 secrets (**108th session**). Control B mock used
  with **both** `ZAI_TOKEN` (the gate in `call_provider`) **and** `ZAI_URL_OVERRIDE` (the destination);
  the override alone is dead code.
- **`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`** before the run. Direct probe of
  `https://api.typesafe.ai/v1/systemone` -> **HTTP 200**, `{"model":"jev-1.14.0", …}`, real score
  `0.31`, confidence `0.75`. Without the alias `jev_score` falls through to the `2.0/2.0/2.0` fallback.

## Pre-flight gate — 40/40 PASS, exit 0

40/40 requests 200, 40/40 distinct previews, 40/40 distinct seeds, 40/40 distinct seed-tuples,
all bodies **349 chars** (inside the 332-369 band), 38+162=200 geometry holds, 149-char
continuation, 5 distinct seeds per civ, 8 distinct seeds per prompt.

**Mock algorithm validated non-circularly**: the seed/colour/figure recompute was re-derived
against the **pre-existing** ledger (**not** this run's rows) — **3360/3360 exact matches** over the
recognizable historical rows, 0 mismatches.

## Ledger delta

- **+10 rows per civ, +80 total**; `meta_log` **988 -> 993** (+5); **18** files changed.
- Every new row carries the documented **9 keys** (`ts, civ, civ_name, provider, params, prompt,
  scores, avg_score, content_preview`); preview length **200** on every row; all 80 rows parse as
  JSON; **0 key/shape violations**.
- **JEV was live on all 80 rows**: 0 `error` fields, **0** `2.0/2.0/2.0` fallback triples,
  0 zero-confidence rows, confidence range **0.27 - 0.86**, **80/80 distinct score triples**.
- Prompt draw across the 80 new rows: ternary values 20, JEV oracle 17, what a cell is 15,
  witness log 15, bookkeeper 13.

### Counter reconciliation — 8/8 OK

The sim phase gives every civ +5 sims; the competition phase gives every civ **5 more sims**
(each competition calls `run_simulation` again) plus exactly one W or L. So **dSims = 10** and
**dW + dL = 5** for all 8 civs. Relevance deltas match the sum of the new `avg_score` values to
the last decimal on all 8 ledgers.

| civ | dW | dL | dSims | sum(new avg) | dRelevance |
|---|---|---|---|---|---|
| civ-grounded | 0 | 5 | 10 | 14.6967 | 14.6967 |
| civ-whimsical | 0 | 5 | 10 | 15.3267 | 15.3267 |
| civ-formal | 0 | 5 | 10 | 16.7867 | 16.7867 |
| civ-poetic | 0 | 5 | 10 | 20.7700 | 20.7700 |
| civ-precise | 5 | 0 | 10 | 19.1400 | 19.1400 |
| civ-mythic | 0 | 5 | 10 | 15.4867 | 15.4867 |
| civ-therapist | 0 | 5 | 10 | 12.6700 | 12.6700 |
| civ-engineer | 0 | 5 | 10 | 16.9333 | 16.9333 |

> **Baseline gotcha (re-confirmed).** The leaderboard's `sims_run` field is
> `relevance / relevance_per_sim` with `relevance_per_sim` **rounded to 3 dp** — it is NOT the true
> `simulations_run` counter. Taking the baseline from `leaderboard.json` produces **negative** dSims
> (e.g. civ-grounded -33) and a false reconciliation FAIL. **Always take the baseline from
> `git show HEAD:<civ>/culture.json`**, which carries the exact counter.

## Run-level standings (10 sims per civ)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | 2.0770 | 1.2790 | 2.4070 | 2.5450 |
| civ-precise | 1.9140 | 0.8180 | 2.3400 | 2.5840 |
| civ-engineer | 1.6933 | 0.6900 | 2.3100 | 2.0800 |
| civ-formal | 1.6787 | 0.6430 | 2.2490 | 2.1440 |
| civ-mythic | 1.5487 | 0.8330 | 2.3520 | 1.4610 |
| civ-whimsical | 1.5327 | 0.7420 | 2.4200 | 1.4360 |
| civ-grounded | 1.4697 | 0.5260 | 2.2870 | 1.5960 |
| **civ-therapist** | **1.2670** | 0.5720 | 2.3720 | **0.8570** |

- Run low **`civ-therapist`** (avg **1.2670**) — alignment **0.8570** at the fleet low, quality
  **0.5720** second-lowest, novelty **3rd** of 8. A **two-axis** collapse for the **3rd consecutive
  session**.
- Run high `civ-poetic` (avg **2.0770**).
- Alignment spread **1.7270 = 2.13x** the `avg_score` spread (0.8100).

## Leaderboard (pre -> post, sorted by relevance_per_sim)

| civ | relevance | d | rel/sim | win_rate | wins |
|---|---|---|---|---|---|
| civ-poetic | 3360.03 | +20.77 | 1.728 | 0.006 | 6 |
| civ-precise | 3228.73 | +19.14 | 1.669 | 0.712 | 686 |
| civ-formal | 2795.27 | +16.79 | 1.437 | 0.126 | 122 |
| civ-whimsical | 2765.20 | +15.33 | 1.417 | 0.005 | 5 |
| civ-mythic | 2723.86 | +15.49 | 1.405 | 0.010 | 10 |
| civ-engineer | 2673.28 | +16.93 | 1.382 | 0.061 | 59 |
| civ-grounded | 2390.44 | +14.70 | 1.220 | 0.078 | 75 |
| civ-therapist | 2381.87 | +12.67 | 1.230 | 0.011 | 11 |

- Winners: **`civ-precise` 5/5** (a clean sweep). Agreement with the `avg_score` argmax
  **1/5 (20 %)** — 4 down-grades, 0 up-grades.
- `civ-poetic` was the `avg_score` argmax on **4 of 5** and won **0**; it also leads lifetime
  relevance and `rel/sim` on a **0.6 %** win rate.
- **Bottom two:** `civ-therapist` **2381.87** (lifetime low) vs `civ-grounded` **2390.44** — a gap
  of **8.57**. The step from #2 to #3 (engineer 2673.28) is **282.84** — a **33x** larger step.
- No civ near extinction (threshold `relevance < -10`; lowest **2381.87**, **239x** the floor).
  Registry 8, `max_civs` 12, all `generation=1`.

## Verification of the request

- `ls -la` on the civilizations directory confirms **all 8** `simulations.jsonl` files grew
  (mtimes `19:13`), and the per-civ row counts rose by exactly **+10** each.
