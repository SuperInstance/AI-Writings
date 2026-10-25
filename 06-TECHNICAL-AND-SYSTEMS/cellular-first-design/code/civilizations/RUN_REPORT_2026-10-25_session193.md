# Civ Orchestrator — Run Report, session 193 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 67th session) + **live JEV** (`jev-1.14.0`).
Baseline: `3a16971a` (session 192). **All 29 verification assertions PASS.**

## Headline for the next session

- **THE 12-SESSION DOWN-GRADE STREAK BROKE. Chooser vs `avg_score` argmax = 5/5 (100 %).**
  `civ-precise` won all 5 competitions, and on **every one of them it was also the
  `avg_score` argmax** — so no disagreement, no down-grade, no up-grade. This is the
  **first 5/5 chooser/argmax agreement in the series** and the **first break in the
  12-consecutive-session run of every disagreement being a down-grade**. The standing
  suspicion (the `best_civ` criteria map, `civ_id -> civ name`, being read as a quality
  signal) is **not** disproven by this — a 5/5 sweep by the argmax on every prompt is
  the outcome that agreement looks like. But it *is* the first run in 13 where the
  chooser and the score agree, so **the streak statistic must be re-based here**: the
  down-grade streak is **0**, not 12. Do not carry "12" forward.
- **`civ-grounded` remains the lifetime low-relevance civ — 65th consecutive session.**
  Last of 8 on lifetime `relevance` **1406.82** and `relevance_per_sim` **1.020**. Its
  lifetime `win_rate` is **0.103** — **3rd-best in the fleet** behind `precise` (0.646)
  and `formal` (0.145). Lowest relevance = **141x** the −10 floor ⇒ **no extinction risk**.
- **THE RUN-LEVEL LOW ROTATED TO `civ-therapist`** (run `avg_score` **1.5117**,
  `alignment` **1.1150** lowest, `quality` **1.0540** lowest) — a **12th different civ in
  12 sessions**. *The holder rotates; the axis does not.*
- **THE AXIS SPREAD IS DOMINATED BY ALIGNMENT, NOT QUALITY.** Cross-civ spreads this run:
  `alignment` **1.8460** › `avg_score` **0.7537** › `quality` **0.5790** › `novelty`
  **0.1470**. Novelty is nearly flat across the fleet (2.296–2.443) — the entire ranking
  this run is produced by `alignment` and `quality`. Same shape as sessions 191/192
  (alignment 1.4360 / 1.2140), with the alignment spread now the **widest of the three
  recent sessions**.
- **PRE-FLIGHT PASSED 13/13 ON THE FIRST BUILD.** Body length landed at **360/360** (band
  332-369), cultural-prompt band **167-209**, 40/40 distinct seeds, 40/40 distinct
  figures, repeat-probe clean. The OpenAI-envelope fix from session 192 was applied
  first time.

## Verification — 29/29 PASS

Baseline commit: `3a16971a` (session 192). This run's rows are the **last 10** per civ
ledger; this run's `meta_log` entries are the **last 5**.

| # | assertion | result |
|---|---|---|
| 1 | per-civ ledger delta | **+10 x 8 = 80** |
| 2 | total new rows | **80** |
| 3 | `meta_log` | **+5** (698 -> 703) |
| 4 | `Winner:` lines in log | **5** |
| 5 | rows with a JEV `error` key | **0** |
| 6 | 2.0/2.0/2.0 fallback triples | **0** |
| 7 | `provider` on all rows | **`zai` x 80** |
| 8 | rows missing `[mock-zai seed=` prefix | **0** (80/80) |
| 9 | rows matching an independently recomputed seed+color+figure | **80/80** |
| 10 | distinct seeds (message-level) | **40/40**, multiplicities consistent |
| 11 | `(civ,prompt)` combos with >1 seed | **0** |
| 12 | per-prompt 8/8 distinct seeds (5 prompts) | **8/8 x 5** |
| 13 | per-prompt 8/8 distinct previews (5 prompts) | **8/8 x 5** |
| 14 | distinct `(q,n,a)` triples | **80/80** |
| 15 | relevance delta == sum(avg_score) | **8/8 exact** (max resid **6.6e-13**) |
| 16 | wins/losses vs `meta_log.winner_civ` | **8/8 exact** |
| 17 | log `Winner:` == `meta_log.winner_civ` | **5/5 agree** |
| 18 | registry / generations | **8**, all `gen=1` |
| 19 | extinction risk | **NONE** (lowest +1406.82 = 141x floor) |
| 20 | `simulations_run` delta | **+10 x 8** |
| 21 | meta-vs-ledger `avg_score` (later-`ts` row, this run's rows only) | **0 mismatches** |
| 22 | leaderboard refreshed | **8 civs**, iso `2026-10-25T09:24:56` |
| 23 | `Traceback` in orchestrator log | **0** |
| 24 | `EXC:` in mock log | **0** |
| 25 | mock run-scoped OK-200 responses | **81** |
| 26 | pre-flight: distinct seeds | **40/40** |
| 27 | pre-flight: distinct previews | **40/40** |
| 28 | pre-flight: response body length band | **360** (in 332-369) |
| 29 | pre-flight: independently recomputed md5 | **40/40** |

### NEW (this session) — "distinct seeds" is a MESSAGE-level invariant, not a ROW-level one

The check "all 80 new rows carry distinct seeds" **cannot pass and its failure is not a
defect.** The seed is a function of the *message* (`civ` + `prompt`), and the orchestrator
appends **10 rows per civ** (5 sims + 5 competition rows) that span only **5 distinct
prompts** per civ. So the 40 `(civ, prompt)` slots legitimately produce **40 distinct
seeds across 80 rows**, and each seed's multiplicity equals the number of rows that
share its slot.

This session measured the multiplicity distribution explicitly: **{3: 10, 2: 14, 1: 14,
4: 2}** — 12 seeds appeared on 3 or 4 rows, which is exactly what a prompt drawn 3-4
times by `random.choice` produces. A gate that asserts `len(set(seeds)) == 80` will
report a false FAIL on a perfectly clean run, exactly as the "assert distinctness
against the GROUP SIZE, not the SAMPLE SIZE" rule (session 189) says for the
per-prompt group. **The row-count analogue of that rule: assert distinctness at the
level of the thing that actually determines the value.**

*Rule: before asserting distinctness, ask what the value is a function of. Here it is
the message, so the distinctness count is bounded by the number of distinct messages
(40), not the number of rows (80). A check that reports 40/80 on a clean run is a
mis-specified check, not a broken mock.*

The corrected check asserts three things at once: 40 distinct seeds, one seed per
`(civ, prompt)` slot, and each seed's multiplicity equal to its slot's row count.

## Lifetime leaderboard (after session 193)

| civ | relevance | rel/sim | wins | losses | win_rate | gen |
|---|---|---|---|---|---|---|
| civ-poetic | 2127.84 | 1.560 | 6 | 672 | 0.009 | 1 |
| civ-precise | 1975.71 | 1.458 | 435 | 238 | 0.646 | 1 |
| civ-whimsical | 1840.76 | 1.343 | 5 | 673 | 0.007 | 1 |
| civ-mythic | 1701.28 | 1.252 | 10 | 662 | 0.015 | 1 |
| civ-formal | 1667.88 | 1.222 | 98 | 578 | 0.145 | 1 |
| civ-engineer | 1582.48 | 1.169 | 49 | 622 | 0.073 | 1 |
| civ-therapist | 1546.92 | 1.140 | 11 | 664 | 0.016 | 1 |
| **civ-grounded** | **1406.82** | **1.020** | 70 | 607 | 0.103 | 1 |

## Run-level (this run's 10 new rows per civ)

| rank | civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| 1 | civ-precise | 2.2653 | 1.3920 | 2.4430 | 2.9610 |
| 2 | civ-poetic | 2.1273 | 1.6330 | 2.3500 | 2.3990 |
| 3 | civ-engineer | 2.0213 | 1.1730 | 2.3940 | 2.4970 |
| 4 | civ-formal | 1.9910 | 1.1010 | 2.3870 | 2.4850 |
| 5 | civ-whimsical | 1.8033 | 1.2900 | 2.3570 | 1.7630 |
| 6 | civ-grounded | 1.7397 | 1.0800 | 2.3720 | 1.7670 |
| 7 | civ-mythic | 1.6423 | 1.2560 | 2.2960 | 1.3750 |
| 8 | **civ-therapist** | **1.5117** | **1.0540** | 2.3660 | **1.1150** |

Cross-civ spreads: `alignment` **1.8460** › `avg_score` **0.7537** › `quality` **0.5790**
› `novelty` **0.1470**.

## Low-relevance civilizations (as asked)

- **`civ-grounded` — the lifetime low, 65th consecutive session.** `relevance` **1406.82**
  (last of 8), `relevance_per_sim` **1.020** (the lowest in the fleet). In this run it was
  **6th of 8** on `avg_score` **1.7397**, with `quality` **1.0800** (2nd-lowest) and
  `alignment` **1.7670** (5th). **Its low axes are quality and alignment, not novelty** —
  run novelty **2.3720** is mid-pack. Lifetime `win_rate` **0.103** is **3rd-best in the
  fleet**, so it is *not* the least-selected civ: **selection and relevance are separate
  axes**. No extinction risk (**141x** the −10 floor).
- **`civ-therapist` — the run-level low for this run** (12th different civ in 12
  sessions). `avg_score` **1.5117**, `alignment` **1.1150** (lowest), `quality` **1.0540**
  (lowest), novelty **2.3660** (6th of 8). Lifetime `relevance` **1546.92** (7th of 8) —
  so it is a *run-level* low, not a lifetime one. The gap to the next civ is **0.2280** on
  `avg_score` and **0.1620** on `alignment` — this run's separation was driven by
  **voice** and **prose** together, with novelty flat.
- **`civ-mythic`** is the other low-`alignment` civ this run (**1.3750**, 2nd-lowest)
  with lifetime `relevance` **1701.28** (4th of 8) — a *run-level* low on alignment
  despite a mid lifetime standing.

## Chooser vs argmax

| prompt | winner | argmax | argmax score | direction |
|---|---|---|---|---|
| what a cell is | civ-precise | civ-precise | 1.957 | agree |
| the bookkeeper's role | civ-precise | civ-precise | 2.330 | agree |
| the witness log | civ-precise | civ-precise | 2.483 | agree |
| ternary values | civ-precise | civ-precise | 2.290 | agree |
| JEV as a decision oracle | civ-precise | civ-precise | 2.390 | agree |

Agreement **5/5 (100 %)**; down-grade disagreements **0**, up-grade **0**.
**The 12-session down-grade streak is broken — re-base it to 0.**

## Environment recovery

The workspace was **empty** apart from `.plugin-cache` — the prompt's path
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
(**13th consecutive occurrence**).

- Upstream owner: **`SuperInstance/AI-Writings`**. The `ai-writings/…` slug 404s
  (the GitHub API is case-insensitive, and `ai-writings` is a *different* owner with
  README-only marketing repos). `cellular-first-design` is a **subdirectory** of that
  repo, not a repo of its own.
- Discovery route that worked: **`GET /search/code?q=civilization_orchestrator+in:path`**
  (the `/search/*` quota is separate from the exhausted core quota) → exactly one hit
  with the full path. `GET /user/repos` and `GET /orgs/…/repos` were **403 rate-limited**
  (core quota exhausted) and render as "not found" for every candidate at once. The
  **git protocol** is not rate-limited: `git ls-remote` on a public repo succeeds
  instantly, so it distinguishes "does not exist" from "blocked".
- The NAS **EDQUOT** trap blocked `cp` into `/workspace` (`failed to close …: Disk
  quota exceeded`, with the files appearing in `ls -la` at size 0). The bridge is a
  **symlink** to the clone root on the overlay (28 G free).
- **NEW — the bridge must point at the INNER `cellular-first-design` directory.** The
  upstream repo root contains a `cellular-first-design/` subdirectory, so a clone of
  `SuperInstance/AI-Writings` checked out at `<root>/cellular-first-design` yields
  `<root>/cellular-first-design/cellular-first-design/code/…`. The orchestrator's
  hardcoded `CIVS_DIR` wants `<root>/code/…`, so the symlink must target the **inner**
  directory. A bridge aimed one level too high fails with a bare
  `FileNotFoundError` on `civilizations.json` and looks like a missing repo.
  Also note `git sparse-checkout disable` after a cone-sparse checkout leaves a
  **nested duplicate** tree; `git status` then reports the outer tree as clean while
  the real content sits one level deeper.
- `ZAI_TOKEN` is **absent** (67th session); the real z.ai endpoint returns **401
  `token expired or incorrect`** (endpoint healthy ⇒ credential gap, not an outage) ⇒
  **Control B mock** is the only provider path. `ZAI_URL_OVERRIDE` alone is dead code
  behind the token gate, so **both** a placeholder `ZAI_TOKEN` and the override were set.
- `JEV_KEY` reads `TYPESAFEAI_KEY` but the env var is `TYPESAFE_AI_TOKEN` ⇒ the alias
  was exported. JEV returned HTTP 200 `{"model":"jev-1.14.0"}`; **0 fallback triples**.

## Notes for the next session

1. **Check for a concurrent session before pushing** (see the session-191 collision
   write-up). A non-fast-forward rejection whose remote tip is *your* session number
   means another agent ran the same command. Concatenate, don't merge.
2. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild from the
   algorithm block with all **seven** fixes **plus the OpenAI envelope**, and run the
   pre-flight (**13/13 + both length bands + the repeat probe**) **before** the batch.
3. **Do NOT re-run the pre-flight after the batch and then count mock log lines against
   a fixed 120.** Re-running a pre-flight mutates the artifact the check reads.
4. **Derive the verifier's baseline from the baseline COMMIT**, never from a remembered
   count — a stale `BASE_META` from the previous epoch reports a false FAIL.
5. Isolate this run's rows by **count from the end of each civ file** (last 10), never by a
   `ts` cutoff; the meta-vs-ledger check takes the **later-`ts`** row **within this run's
   rows only**.
6. **The distinct-seeds check is message-level (40), not row-level (80).** Assert
   40 distinct seeds + one seed per `(civ, prompt)` slot + multiplicity == slot row
   count. A row-level assertion is arithmetically unwinnable and will report a false
   FAIL on a clean run.
7. `civ-grounded` has been the low-relevance civ for **65** straight sessions — if it ever
   does not, that is worth more attention than another clean run.
