# Civilization Orchestrator — Session 255 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Fleet: 8 civs. Provider: **Control B mock** (z.ai credential gap, **112th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `215be6f`. **Pre-flight gate: 40/40 PASS, exit 0.** **Run verification: 47 PASS / 0 FAIL.**

**Session 255 in one line:** `civ-precise` swept **5/5** competitions for the **fourth consecutive
session**; chooser/argmax agreement was **3/5 (60 %)** — 2 down-grades, 0 up-grades; the run low was
**`civ-therapist`** (avg **1.2920**) at the fleet floor on **both** quality (**0.4920**) and alignment
(**0.9120**) for the **6th consecutive session**; the lifetime low stayed with `civ-therapist`
(**2431.94**) behind `civ-grounded` (**2451.00**) by **19.05**.

## Environment notes

- **Task path absent again.** `/workspace/repos/ai-writings/...` did not exist (**16th consecutive
  occurrence**); the workspace held only `.plugin-cache` and `.skills`.
- **The NAS is still at 100 %.** A direct `git clone` into `/workspace` dies on `.git/description`
  with `close error: Disk quota exceeded` (**22nd session**). A 1 KB `dd` into `/workspace` also
  produced a **0-byte** file — the phantom-file trap in its purest form. Cloned to the overlay at
  `/tmp/aiw` and bridged with a symlink `/workspace/repos/ai-writings -> /tmp/aiw`; bridge verified
  with `os.path.samefile()` -> `True`.
- **Upstream is `SuperInstance/AI-Writings`** (capitalised). The `ai-writings/…` slug 404s — the
  path in the task prompt is a *subdirectory* of that repo. Located by paging
  `GET /user/repos?per_page=100` and filtering on the repo name, then confirmed with
  `git ls-tree -r --name-only HEAD | grep cellular-first-design`.
- **Sparse clone is the fast path — 15 MB vs 3.7 GB.** `--filter=blob:none --no-checkout --depth 1`
  plus `sparse-checkout set cellular-first-design`, then `git fetch --unshallow` for the
  `git show HEAD:` baselines.
- **z.ai live probe: HTTP 401** `token expired or incorrect` => endpoint healthy, credential absent.
  `ZAI_TOKEN` unset in env. Control B mock used with **both** `ZAI_TOKEN` (the gate in
  `call_provider`) **and** `ZAI_URL_OVERRIDE` (the destination); the override alone is dead code
  behind the token gate.
- **`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`** before the run. Direct probe of
  `https://api.typesafe.ai/v1/systemone` -> **HTTP 422 `too_short`**, which proves the token was
  accepted (the endpoint rejects an empty `questions` map only *after* authenticating).
- **Mock teardown by exact PID** — never `pkill -f mock_zai` (self-match, 2 prior occurrences).

## Pre-flight gate — 40/40 PASS, exit 0

40/40 requests 200, 40/40 distinct previews, 40/40 distinct seeds, 40/40 distinct seed-tuples,
all bodies **349 chars** (inside the 332-369 band), 38+162=200 geometry holds, 149-char
continuation, 5 distinct seeds per civ, 8 distinct seeds per prompt.

## Ledger delta — `ls -la` plus the authoritative row-count check

All 8 `simulations.jsonl` files show a fresh mtime, but mtime alone cannot distinguish "+10 rows"
from "rewritten in place". The row-count delta is the real assertion:

| civ | pre | post | delta |
|---|---|---|---|
| civ-grounded | 2032 | 2042 | **+10** |
| civ-whimsical | 2044 | 2054 | **+10** |
| civ-formal | 2017 | 2027 | **+10** |
| civ-poetic | 2011 | 2021 | **+10** |
| civ-precise | 1981 | 1991 | **+10** |
| civ-mythic | 1989 | 1999 | **+10** |
| civ-therapist | 1984 | 1994 | **+10** |
| civ-engineer | 1986 | 1996 | **+10** |

`meta_log.jsonl` **1008 -> 1013** (**+5**). Total **+80** new rows.

- Every new row carries the documented **9 keys**; preview length **200** on every row; **0**
  key/shape violations; provider set on every new row is exactly `{zai}`.
- **80/80 new rows re-derive exactly** from `md5(cultural_prompt)` (seed, colour, figure) — 0
  mismatches. The `#` in the colour field is optional; a `#`-stripped comparison misreports every
  mock row (session-248 lesson, re-confirmed).
- **0 JEV errors, 0 fallback 2.0/2.0/2.0 triples, 0 non-numeric quality scores.** Confidence
  range **0.27 - 0.86**.

## Run results

| civ | n | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| **civ-therapist** | 10 | **1.2920** | **0.4920** | 2.4720 | **0.9120** |
| civ-mythic | 10 | 1.5467 | 0.7890 | 2.3500 | 1.5010 |
| civ-whimsical | 10 | 1.5477 | 0.6950 | 2.4970 | 1.4510 |
| civ-grounded | 10 | 1.5537 | 0.7100 | 2.2420 | 1.7090 |
| civ-engineer | 10 | 1.7027 | 0.7910 | 2.1930 | 2.1240 |
| civ-formal | 10 | 1.7723 | 0.8080 | 2.2500 | 2.2590 |
| civ-precise | 10 | 1.9247 | 0.8570 | 2.2720 | **2.6450** |
| **civ-poetic** | 10 | **2.0040** | **1.1260** | 2.4420 | 2.4440 |

Run spread: `avg_score` **0.6340**. Axis floors: quality `civ-therapist` **0.4920**;
novelty `civ-engineer` **2.1930**; alignment `civ-therapist` **0.9120**. Axis ceilings:
quality `civ-poetic` 1.1260; novelty `civ-whimsical` 2.4970; alignment `civ-precise` 2.6450.

**`civ-therapist` is the run low and it is a two-axis collapse** — quality floor *and* alignment
floor, with novelty mid-fleet (2.4720, 2nd of 8). `civ-grounded` is the contrasting **one-axis**
case: low quality (0.7100) but mid-pack alignment (1.7090). `civ-engineer` owns the *novelty*
floor (2.1930) while sitting 5th of 8 on avg_score — a third distinct failure shape.

## Lifetime leaderboard (post-run)

| rank | civ | relevance | rel/sim | wins | losses | win_rate | gen | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 3441.06 | 1.734 | 6 | 982 | 0.006 | 1 | 0.8 |
| 2 | civ-precise | 3307.66 | 1.675 | 706 | 277 | 0.718 | 1 | 0.2 |
| 3 | civ-formal | 2865.69 | 1.444 | 122 | 864 | 0.124 | 1 | 0.3 |
| 4 | civ-whimsical | 2826.77 | 1.420 | 5 | 983 | 0.005 | 1 | 0.95 |
| 5 | civ-mythic | 2787.04 | 1.408 | 10 | 972 | 0.010 | 1 | 0.85 |
| 6 | civ-engineer | 2740.85 | 1.388 | 59 | 922 | 0.060 | 1 | 0.4 |
| 7 | civ-grounded | 2451.00 | 1.226 | 75 | 912 | 0.076 | 1 | 0.5 |
| 8 | civ-therapist | 2431.94 | 1.230 | 11 | 974 | 0.011 | 1 | 0.6 |

- **The board's sort key and its `relevance` column disagree at the bottom.** The board sorts by
  `relevance_per_sim`, so row 7 (`civ-grounded`, 1.226) has *higher* raw relevance than row 8
  (`civ-therapist`, 1.230) — the same inversion seen in sessions 253 and 254.
- **Neither is near extinction.** Threshold is `relevance < -10`; the lowest is **2431.94**, roughly
  **243x** the floor. Registry stays at **8** civs, `max_civs` is 12, all `generation=1`. No birth
  and no extinction fired this session.
- **Relevance gained this run** is monotone in the run-score order: therapist **+12.92** (lowest
  gain) through poetic **+20.04** (highest). Every civ gained; no civ lost ground.
- Bottom-pair gap **19.05** (grounded 2451.00 vs therapist 2431.94) against a #2->#3 step of
  **38.92** — a **2.0x** larger step. The gap series reads 6.54 (s250) -> 13.65 (s253) ->
  16.44 (s254) -> **19.05** (s255): rising again, so the "floor is converging" reading from
  session 247 is **not** a law.

## The chooser keeps down-grading the argmax

`civ-precise` won **5/5** competitions for the **fourth consecutive session**, but the `avg_score`
argmax agreed only **3/5 (60 %)** — **2 down-grades, 0 up-grades**, both disagreements taking the
*lower*-scoring candidate (prompt 1: `civ-precise` 1.7600 over `civ-poetic` 1.8667; prompt 5:
`civ-precise` 2.0200 over `civ-poetic` 2.0933). This continues a **23-session** run with **0
up-grades ever recorded**. The chooser is structurally unable to agree with the score: it never
receives the scores, only the 200-char previews. *Do not read the disagreement as a scoring
regression.*

`civ-poetic` is the `avg_score` leader of this run (**2.0040**) and holds lifetime relevance #1 and
`rel/sim` #1 — on a **0.6 %** lifetime win rate with **6** wins. It is the most relevant civ by
every accumulated measure and one of the least competitive in the meta-GAN.

## Durable lessons

1. **THE UP-GRADE COUNT WAS A VERIFIER BUG, NOT A BREAK IN THE SERIES.** A first pass reported
   "1 up-grade" — the first in 23 sessions. The bug: it compared **list positions** inside
   `results` (whose order is whatever the thread pool produced) instead of **scores**. A chooser
   that wins a *lower*-scoring slot can appear to be an up-grade purely because the lists are
   ordered differently. *Compare `winner_score` to `argmax_score` numerically, never
   `results.index()`.* The corrected count is **3 agree / 2 down / 0 up**.
2. **THE `dSims = 10` IDENTITY HELD AGAIN**, and so did the exact reconciliation: `dSims == 10` on
   all 8, `dW + dL == 5` on all 8, and `dRelevance == sum(new rows' avg_score)` matched to
   **0.0000 residual** on all 8 (`civ-precise` took `dW=+5, dL=+0`; the other seven took
   `dW=+0, dL=+5`). *Derive the identity from the code path, not from a single clean run.*
3. **THE BOTTOM-PAIR GAP SERIES IS **NOT** MONOTONE IN EITHER DIRECTION —
   6.54 (s250) -> 13.65 (s253) -> 16.44 (s254) -> **19.05** (s255).** It fell through sessions
   245-247 and has risen for three sessions straight. *Report the gap and the step ratio and let
   the series move; "the floor is converging" was a trend, not a law.*
4. **`civ-therapist`'s TWO-AXIS COLLAPSE IS NOW A SIX-SESSION RUNNING SIGNATURE** (quality floor +
   alignment floor together, novelty mid-fleet). `civ-grounded` remains the contrasting **one-axis**
   case. `civ-engineer` is a **third** shape: it owns the *novelty* floor (2.1930) with
   mid-pack quality. *The axis is the finding, not the holder — and do not stop at two shapes
   because the last two sessions had two.*
5. **THE OVERLAY IS STILL THE ONLY WRITABLE PATH.** The NAS reports `600G 600G 0 100%`; a clone
   into `/workspace` dies on `.git/description`, the *first* write, and even a 1 KB `dd` lands a
   **0-byte** file. The symlink bridge (`/workspace/repos/ai-writings -> /tmp/aiw`) satisfies the
   orchestrator's hardcoded `CIVS_DIR` without writing a single byte to the full mount.
   *Do not interpret a clone that "starts" as one that will finish.*
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
