# Civ Orchestrator — Run Report, session 189 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 63rd session) + **live JEV** (`jev-1.14.0`).
Baseline: `0776299` (session 188). **All 29 verification assertions PASS.**

## Headline for the next session

- **THE `civ-precise` SWEEP BROKE, BUT THE DOWN-GRADE STREAK DID NOT.** `civ-precise` took
  **4/5** competition prompts (not 5/5 — `civ-engineer` won the ternary prompt). The chooser
  still disagreed with the `avg_score` argmax on **4 of 5** prompts, and **all four
  disagreements took the LOWER-scoring candidate** — the **10th consecutive session** in which
  a chooser/argmax disagreement is a *down*-grade. Agreement fell to **1/5 (20 %)**.
  `civ-poetic` was the argmax on **4 of 5** prompts and won **none** of them.
  **The `best_civ` criteria map (civ_id -> civ name) is the suspect, not the quality signal.**
- **`civ-grounded` remains the lifetime low-relevance civ — 61st consecutive session.**
  Last of 8 on lifetime `relevance` **1338.36** and `relevance_per_sim` **1.000** (it has now
  crept back to exactly 1.000). Run `avg_score` **1.3070**, `alignment` **0.7900**,
  `quality` **0.4290**, novelty **2.7020** (1st of 8). Its lifetime `win_rate` is **0.107** —
  **3rd-best in the fleet** behind `precise` (0.636) and `formal` (0.149).
  Lowest relevance = **134x** the −10 floor ⇒ **no extinction risk**.
- **THE RUN-LEVEL LOW ROTATED TO `civ-therapist`** (run `avg_score` **1.2537**,
  `alignment` **0.5240**, `quality` **0.5600**) — a **9th different civ in 9 sessions**.
  Alignment gap **2.3390** vs quality gap **0.7920** = **2.95x wider** ⇒ a **voice**
  failure. *The holder rotates; the axis does not.*
- **RELEVANCE DELTA == sum(`avg_score`) 8/8 EXACT** (max residual **3.9e-13**), taken
  against the **git blob** baseline, not the rounded leaderboard.
- **THE LOWEST-RELEVANCE CIV IS NOT THE LEAST-SELECTED ONE.** `civ-grounded` has the
  3rd-best `win_rate` and the worst relevance. `civ-poetic` has the **worst**
  `win_rate` (0.009) and the **best** relevance. Selection and relevance are separate axes;
  conflating them hides the real failure.

## Verification — 29/29 PASS

| # | assertion | result |
|---|---|---|
| 1 | per-civ ledger delta | **+10 x 8 = 80** |
| 2 | total new rows | **80** |
| 3 | `meta_log` | **678 -> 683** (+5) |
| 4 | `Winner:` lines in log | **5** |
| 5 | rows with a JEV `error` key | **0** |
| 6 | 2.0/2.0/2.0 fallback triples | **0** |
| 7 | `provider` on all rows | **`zai` x 80** |
| 8 | rows missing `[mock-zai seed=` prefix | **0** (80/80) |
| 9 | rows matching an independently recomputed seed+color+figure | **80/80** |
| 10 | distinct seeds | **40/40** |
| 11 | `(civ,prompt)` combos with >1 seed | **0** |
| 12 | per-prompt 8/8 distinct seeds (5 prompts) | **8/8 x 5** |
| 13 | per-prompt 8/8 distinct previews (5 prompts) | **8/8 x 5** |
| 14 | distinct `(q,n,a)` triples | **80/80** |
| 15 | relevance delta == sum(avg_score) | **8/8 exact** (max resid 3.9e-13) |
| 16 | wins/losses vs `meta_log.winner_civ` | **8/8 exact** |
| 17 | log `Winner:` == `meta_log.winner_civ` | **5/5 agree** |
| 18 | registry / generations | **8**, all `gen=1` |
| 19 | extinction risk | **NONE** (lowest +1338.36 = 134x floor) |
| 20 | `simulations_run` delta | **+10 x 8** |
| 21 | meta-vs-ledger `avg_score` (later-`ts` row) | **0 mismatches** |
| 22 | leaderboard refreshed | **iso 2026-10-25T08:35:28**, 8 civs |
| 23 | `Traceback` in orchestrator log | **0** |
| 24 | `EXC:` in mock log | **0** |
| 25 | mock OK-200 responses | **120** (40 pre-flight + 80 run) |
| 26 | pre-flight: distinct seeds / previews | **40/40**, **40/40** |
| 27 | pre-flight: independently recomputed md5 | **40/40** |
| 28 | pre-flight: response body length band | **360** (in 332-369) |
| 29 | pre-flight: cultural-prompt length band | **167-209** |

## Lifetime leaderboard (after run)

| civ | relevance | rel/sim | wins | losses | win_rate | gen |
|---|---|---|---|---|---|---|
| civ-poetic | 2044.77 | 1.544 | 6 | 652 | 0.009 | 1 |
| civ-precise | 1892.64 | 1.439 | 415 | 238 | 0.636 | 1 |
| civ-whimsical | 1772.37 | 1.332 | 5 | 653 | 0.008 | 1 |
| civ-mythic | 1636.77 | 1.241 | 10 | 642 | 0.015 | 1 |
| civ-formal | 1591.62 | 1.201 | 98 | 558 | 0.149 | 1 |
| civ-engineer | 1509.34 | 1.149 | 49 | 602 | 0.075 | 1 |
| civ-therapist | 1487.02 | 1.129 | 11 | 644 | 0.017 | 1 |
| **civ-grounded** | **1338.36** | **1.000** | 70 | 587 | 0.107 | 1 |

## Run-level (this run's 10 new rows per civ)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | 2.2377 | 1.2210 | 2.6290 | 2.8630 |
| civ-precise | 2.1237 | 0.9900 | 2.6370 | 2.7440 |
| civ-formal | 1.9837 | 0.9630 | 2.6360 | 2.3520 |
| civ-mythic | 1.5553 | 0.7070 | 2.5880 | 1.3710 |
| civ-whimsical | 1.5083 | 0.7260 | 2.7000 | 1.0990 |
| civ-engineer | 1.3897 | 0.4420 | 2.6500 | 1.0770 |
| civ-grounded | 1.3070 | 0.4290 | 2.7020 | 0.7900 |
| **civ-therapist** | **1.2537** | 0.5600 | 2.6770 | 0.5240 |

Run spreads: `avg_score` 0.9840, `alignment` **2.3390** (widest), quality 0.7920, novelty 0.1140.

## Chooser vs `avg_score` argmax — 1/5 agreement, 4 down-grades

| prompt | argmax | winner | delta | |
|---|---|---|---|---|
| what a cell is | civ-poetic (2.1867) | civ-precise (2.0167) | +0.1700 | **DOWN** |
| bookkeeper's role | civ-poetic (1.8967) | civ-precise (1.7133) | +0.1833 | **DOWN** |
| witness log | civ-precise (2.4267) | civ-precise (2.4267) | 0.0000 | AGREE |
| ternary values | civ-poetic (2.2833) | civ-engineer (1.5533) | **+0.7300** | **DOWN** |
| JEV as a decision oracle | civ-poetic (2.5200) | civ-precise (2.3300) | +0.1900 | **DOWN** |

`civ-poetic` was the argmax on **4/5** prompts and won **0/5**. The single largest
disagreement in the series (**+0.7300**) hands the ternary prompt to `civ-engineer`, whose
`avg_score` was **0.73 below** the leader. **`win_rate` is not a quality metric.**

## Environment recovery (session 189)

- Workspace **empty** apart from `.plugin-cache` — the prompt's path did not exist
  (**13th consecutive occurrence**).
- Upstream **`SuperInstance/AI-Writings`**; the `ai-writings/…` slug 404s (API is
  case-insensitive). Cloned to **`/tmp/ai-writings`** with `--filter=blob:none` +
  `sparse-checkout cellular-first-design`. Cloning into `/workspace` fails with
  **`Disk quota exceeded`** (NAS EDQUOT, **18th session**) — the NAS is 600 G/600 G with
  **0 bytes free**.
- Bridge symlink `/workspace/repos/ai-writings/cellular-first-design` -> clone root,
  verified by inode identity (**`129:3668`** on both sides).
- `ZAI_TOKEN` absent from env and all sandbox secrets; z.ai **401**
  `token expired or incorrect` ⇒ endpoint healthy, credential absent (**63rd session**).
- **JEV live**: well-formed body ⇒ **HTTP 200** disclosing the served model **`jev-1.14.0`**.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code).
- `gh` not installed (**20th session**) — used `GET /user/repos` with `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch, stdout redirected, `< /dev/null`.
- `git status --porcelain` = **18 modified** (8 civs x 2 files + `leaderboard.json` + `meta_log.jsonl`).

## New this session

### The pre-flight body-length band must be measured, not assumed

The mock's response body must land in **332-369 chars** — the *response* band — which is a
different band from the **167-209** *cultural-prompt* band. Two builds failed the gate:
a first build produced a **267-char** body (too short) and a second produced **531**
(too long), before trimming to **360**. A body that is too short risks the seed being cut
out of the orchestrator's 200-char `content_preview` truncation; a body that is too long
inflates the preview with prose the scorer never sees.

*Rule: assert the two bands separately, and compute the target from the assembled string
rather than eyeballing the prose. The seed+color+figure prefix is ~90 chars of variable
width, so "a sentence or two longer" is not a length control.*

### A verifier that compares `len(set(...))` to `len(rows)` on a per-prompt group is wrong

The sim phase draws its prompt at random from the same 5 competition prompts, so a prompt
group holds **11-20 rows** for only **8 civs** — the same civ appears 1-4 times with the
*same* seed. The correct assertion is "**8 distinct seeds and 8 distinct previews per
prompt**", not "as many distinct seeds as rows". The first form reports a false FAIL on a
perfectly clean run.

*Rule: the group size is the civ count (8); the row count is a property of the run
schedule, not of the data. Assert distinctness against the group, not the sample.*

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild from the
   **algorithm block** with all **seven** fixes, not from the older "six fixes" checklist.
   Pass the pre-flight (40 distinct seeds AND 40 distinct previews AND 40 independently
   recomputed md5s AND both length bands) **before** the batch.
2. `ZAI_TOKEN` still absent ⇒ real z.ai unusable; Control B is the only provider path.
   JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
3. Use the run-wide integrity checks (80 rows, 40 seeds, per-`(civ,prompt)` 1:1) and
   isolate this run's rows by **count from the end of each civ file**, never by a `ts`
   cutoff.
4. The meta-vs-ledger check must take the **later-`ts`** row for a `(civ, prompt)` pair.
   The match key is `m["prompt"][:80]` — the meta `prompt` is full-length, the ledger
   `prompt` is truncated to 80 chars.
5. **`civ-grounded` has been the low-relevance civ for 61 straight sessions.** If a session
   ever finds it mid-table, that is a *finding* — check the run-wide seed count first to
   rule out a degenerate mock before believing it.
6. Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch with stdout redirected
   **and** `< /dev/null`, then poll `ps` + the log.
7. The NAS EDQUOT trap also blocks **file delivery** — `cp` into `/workspace` leaves a
   0-byte file. Deliver by pushing to git and citing the remote URL, not a workspace
   attachment.
8. **Symlink rule:** `ln -sfn` will not replace an existing directory target; the bridge
   must point at the **clone root** (not the nested `cellular-first-design` dir).
   `rm -rf` the old link, then `ln -s`, then verify with `stat -L -c '%d:%i'` on both sides.
9. **Never `pkill -f` a pattern that appears in your own command line** — it kills the
   calling shell and the tool returns empty output. Match on a PID captured from `ps`,
   or use a pattern that cannot self-match.
