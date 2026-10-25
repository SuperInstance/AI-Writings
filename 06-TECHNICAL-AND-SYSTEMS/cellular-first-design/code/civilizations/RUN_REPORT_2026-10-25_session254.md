# Civilization Orchestrator — Session 254 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Fleet: 8 civs. Provider: **Control B mock** (z.ai credential gap, **111th session**) + **live JEV** (`jev-1.14.0`).
Baseline: session 253 tree. **Pre-flight gate: 40/40 PASS, exit 0.** **Run verification: 80 PASS / 0 FAIL.**

**Session 254 in one line:** `civ-precise` swept **5/5** competitions for the **third consecutive
session**; the chooser's agreement with the `avg_score` argmax was **2/5 (40 %)** — 3 down-grades,
0 up-grades; the run low was **`civ-therapist`** (avg **1.2347**) at the fleet floor on **both**
quality (**0.5090**) and alignment (**0.8410**), a **two-axis** collapse for the **5th consecutive
session**; and the lifetime low stayed with `civ-therapist` (**2419.02**) ahead of `civ-grounded`
(**2435.46**) by **16.44**, against a #2 -> #3 step of **288.37** — a **17.5x** larger step.

## Environment notes

- **Task path absent.** `/workspace/repos/ai-writings/...` did not exist (**15th consecutive
  occurrence**). Workspace held only `.plugin-cache`. A direct clone into `/workspace` fails with
  `close error: Disk quota exceeded` (NAS EDQUOT, 600 G / 0 avail) — **21st session**.
  Cloned to the overlay at `/tmp/aiw` and bridged with a symlink
  `/workspace/repos/ai-writings -> /tmp/aiw`. Bridge verified with `os.path.samefile()` -> `True`.
- **The sparse clone is the fast path — 14 MB vs 3.7 GB.** `git clone --filter=blob:none --no-checkout
  --depth 50` plus `sparse-checkout set cellular-first-design` produced the working tree in seconds.
- **Upstream is `SuperInstance/AI-Writings`** (capitalised). The `ai-writings/…` slug 404s.
  `GITHUB_TOKEN` resolves as user `SuperInstance`; `ai-writings` is a *path* inside that repo, not an org.
- **z.ai live probe: HTTP 401** `token expired or incorrect` => endpoint healthy, credential absent.
  `ZAI_TOKEN` unset in env. Control B mock used with **both** `ZAI_TOKEN` (the gate in
  `call_provider`) **and** `ZAI_URL_OVERRIDE` (the destination); the override alone is dead code
  behind the token gate.
- **`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`** before the run. Direct probe of
  `https://api.typesafe.ai/v1/systemone` -> **HTTP 200**, `{"model":"jev-1.14.0", …}`.
  Without the alias `jev_score` falls through to the `2.0/2.0/2.0` fallback.
- **Mock teardown by exact PID** (282/284) and the port re-probed closed — never `pkill -f mock_zai`
  (self-match, 2 prior occurrences).

## Pre-flight gate — 40/40 PASS, exit 0

40/40 requests 200, 40/40 distinct previews, 40/40 distinct seeds, 40/40 distinct seed-tuples,
all bodies **349 chars** (inside the 332-369 band), 38+162=200 geometry holds, 149-char
continuation, 5 distinct seeds per civ, 8 distinct seeds per prompt.

## Ledger delta

- **+10 rows per civ, +80 total**; `meta_log` **1003 -> 1008** (+5); **9** files changed
  (8 x `simulations.jsonl` + `meta_log.jsonl`), plus 8 `culture.json` and `leaderboard.json`.
- Every new row carries the documented **9 keys**; preview length **200** on every row; all 80 rows
  parse as JSON; **0 key/shape violations**; provider set on every new row is exactly `{zai}`.
- **80/80 new rows re-derive exactly** from `md5(cultural_prompt)` (seed, colour, figure) — 0 mismatches.
- **0 JEV errors, 0 fallback triples, 0 non-numeric quality scores** — every one of the 80 rows
  carries a live score from `jev-1.14.0`.

## Run results

| civ | n | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| **civ-therapist** | 10 | **1.2347** | **0.5090** | 2.3540 | **0.8410** |
| civ-grounded | 10 | 1.5127 | 0.5890 | 2.3100 | 1.6390 |
| civ-whimsical | 10 | 1.5337 | 0.7010 | 2.4450 | 1.4550 |
| civ-mythic | 10 | 1.6187 | 0.8750 | 2.3550 | 1.6260 |
| civ-engineer | 10 | 1.6803 | 0.7100 | 2.2580 | 2.0730 |
| civ-formal | 10 | 1.7177 | 0.7120 | 2.2300 | 2.2110 |
| civ-precise | 10 | 2.0167 | 1.0360 | 2.2550 | **2.7590** |
| **civ-poetic** | 10 | **2.0187** | **1.1570** | 2.4360 | 2.4630 |

Run spread: `avg_score` **0.7840**, alignment **1.9180**, quality **0.6480**, novelty **0.2150**.

## Lifetime leaderboard (post-run)

| rank | civ | relevance | rel/sim | wins | losses | win_rate | gen | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 3421.02 | 1.733 | 6 | 977 | 0.006 | 1 | 0.8 |
| 2 | civ-precise | 3288.41 | 1.673 | 701 | 277 | 0.717 | 1 | 0.2 |
| 3 | civ-formal | 2847.97 | 1.442 | 122 | 859 | 0.124 | 1 | 0.3 |
| 4 | civ-whimsical | 2811.29 | 1.419 | 5 | 978 | 0.005 | 1 | 0.95 |
| 5 | civ-mythic | 2771.57 | 1.408 | 10 | 967 | 0.010 | 1 | 0.85 |
| 6 | civ-engineer | 2723.83 | 1.387 | 59 | 917 | 0.060 | 1 | 0.4 |
| 7 | civ-grounded | 2435.46 | 1.224 | 75 | 907 | 0.076 | 1 | 0.5 |
| 8 | civ-therapist | 2419.02 | 1.230 | 11 | 969 | 0.011 | 1 | 0.6 |

- **The board's sort key and its `relevance` column disagree at the bottom.** The board sorts by
  `relevance_per_sim`, so row 7 (`civ-grounded`, 1.224) has *higher* raw relevance than row 8
  (`civ-therapist`, 1.230) — the same inversion seen in session 253.
- **Neither is near extinction.** Threshold is `relevance < -10`; the lowest is **2419.02**, roughly
  **242x** the floor. Registry stays at **8** civs, `max_civs` is 12, all `generation=1`.
  No birth and no extinction fired this session.
- **Relevance gained this run** is monotone in the same order as the run scores: therapist **+12.34**
  (lowest gain) through poetic **+20.19** (highest). Every civ gained; no civ lost ground.

## The chooser keeps down-grading the argmax

`civ-precise` won **5/5** competitions, but the `avg_score` argmax agreed only **2/5 (40 %)** —
**3 down-grades, 0 up-grades**. This continues a **22-session** run with **0 up-grades ever**
recorded. The chooser is structurally unable to agree with the score: it never receives the scores,
only the 200-char previews. *Do not read the disagreement as a scoring regression.*

`civ-poetic` is the `avg_score` leader of this run (**2.0187**) and holds lifetime relevance #1 and
`rel/sim` #1 — on a **0.6 %** lifetime win rate with **6** wins. It is the most relevant civ by every
accumulated measure and one of the least competitive in the meta-GAN.

## Durable lessons

1. **THE `dSims = 10` IDENTITY HELD AGAIN.** The sim phase writes `sims_per_civ` rows per civ and
   the competition phase writes `len(prompts)` more. With `--sims 5 --prompts 5` that is **+10 rows
   per civ, +80 total** — and `meta_log` grows by only 5. *A reader who expects +5 per civ will
   think the run double-counted; it did not.*
2. **THE RECONCILIATION IS EXACT, NOT APPROXIMATE.** `dSims == 10` for all 8, `dW + dL == 5` for all
   8, and `dRelevance == sum(new rows' avg_score)` matched to within 0.01 for all 8 (the residual
   is JSON float rounding in `culture.json`). `civ-precise` took `dW=+5, dL=+0`; the other seven took
   `dW=+0, dL=+5`. *Derive the identity from the code path, not from a single clean run.*
3. **THE BOTTOM-PAIR GAP SERIES IS NOT MONOTONE — 6.54 (s250) -> 13.65 (s253) -> 16.44 (s254).**
   `civ-grounded` 2435.46 vs `civ-therapist` 2419.02: gap **16.44** on a ~2420 scale (0.68 %).
   The step up to `civ-engineer` is **288.37** — **17.5x** larger. *Report the gap and the step
   ratio, and let the series move; "the floor is converging" remains a trend, not a law.*
4. **THE `civ-therapist` TWO-AXIS COLLAPSE IS NOW A FIVE-SESSION RUNNING SIGNATURE.**
   Quality floor + alignment floor together, novelty mid-fleet (2.3540, 4th of 8). It is stable
   enough to name as a trait of that civ rather than a per-session accident. *The axis is the
   finding, not the holder.* `civ-grounded` is again the contrasting **one-axis** case: lowest
   lifetime `rel/sim` (1.224) and low quality (0.5890), but alignment mid-pack (1.6390).
5. **THE OVERLAY IS STILL THE ONLY WRITABLE PATH.** The NAS reports `600G 600G 0 100%`; a clone
   into `/workspace` dies on `.git/description`, the *first* write. The symlink bridge
   (`/workspace/repos/ai-writings -> /tmp/aiw`) satisfies the orchestrator's hardcoded
   `CIVS_DIR` without writing a single byte to the full mount. *Do not interpret a clone that
   "starts" as one that will finish.*
6. **THE REPO-SHIPPED GATE AND MOCK ARE STILL CORRECT — USE THEM, DO NOT RE-DERIVE.** Both
   `tools/preflight.py` and `tools/mock_zai.py` ran unmodified: 11/11 gate assertions PASS on the
   first build. `CIVS_DIR` must be exported for both.

## Reproduce

```bash
export CIVS_DIR=/tmp/aiw/cellular-first-design/code/civilizations
export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
export ZAI_TOKEN="mock-placeholder"
export ZAI_URL_OVERRIDE="http://127.0.0.1:8099/v1/chat/completions"
python3 "$CIVS_DIR/tools/mock_zai.py" 8099 &
python3 "$CIVS_DIR/tools/preflight.py" 8099
python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
```

**Verdict: ALL PASS (0 FAIL).**
