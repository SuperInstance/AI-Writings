# Civ Orchestrator — Run Report, session 192 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 66th session) + **live JEV** (`jev-1.14.0`).
Baseline: `ede4ce3` (session 191). **All 29 verification assertions PASS.**

Full detail: this report.

## Headline for the next session

- **`civ-precise` SWEPT 5/5 FOR THE FOURTH CONSECUTIVE SWEEP — AND IT IS A CHOOSER EFFECT,
  NOT QUALITY.** The chooser disagreed with the `avg_score` argmax on **4 of 5** prompts and
  **all four took the LOWER-scoring candidate** — the **12th consecutive session** in which
  a chooser/argmax disagreement is a *down*-grade. Agreement **1/5 (20 %)**, the worst
  agreement rate in the series. `civ-poetic` was the argmax on **4 of 5** prompts and won
  **none** of them. The `best_civ` criteria map (civ_id -> civ name) remains the standing
  suspect, not the quality signal. **Never treat `win_rate` as a quality metric.**
- **`civ-grounded` remains the lifetime low-relevance civ — 64th consecutive session.**
  Last of 8 on lifetime `relevance` **1389.42** and `relevance_per_sim` **1.015**. Its
  lifetime `win_rate` is **0.104** — **3rd-best in the fleet** behind `precise` (0.644) and
  `formal` (0.146). Lowest relevance = **139x** the −10 floor ⇒ **no extinction risk**.
- **THE RUN-LEVEL LOW ROTATED TO `civ-mythic`** (run `avg_score` **1.9147**,
  `alignment` **1.8060** lowest, `quality` **1.3190**) — an **11th different civ in 11
  sessions**. *The holder rotates; the axis does not.*
- **THE AXIS SPREAD IS DOMINATED BY ALIGNMENT, NOT QUALITY.** Cross-civ spreads this run:
  `alignment` **1.2140** › `quality` **0.5070** › `avg_score` **0.5007** › `novelty`
  **0.1400**. Novelty is nearly flat across the fleet (2.535–2.675) — the entire ranking
  this run is produced by `alignment` and `quality`. This is the same shape as session 191
  (alignment 1.4360 › quality 0.2670), but the quality spread **nearly doubled**.
- **PRE-FLIGHT PASSED 12/12 ON THE FIRST BUILD, AND THE MOCK REBUILD TOOK ONE FIX.**
  The mock must return an **OpenAI-shaped envelope**
  (`choices[0].message.content`), not the raw body — the orchestrator's `call_provider`
  does `r["choices"][0]["message"]["content"]` and a bare body is a `JSONDecodeError`.
  That is the one thing the algorithm block in the learnings file does not state.

## Verification — 29/29 PASS

Baseline commit: `ede4ce3` (session 191). This run's rows are the **last 10** per civ
ledger; this run's `meta_log` entries are the **last 5**.

| # | assertion | result |
|---|---|---|
| 1 | per-civ ledger delta | **+10 x 8 = 80** |
| 2 | total new rows | **80** |
| 3 | `meta_log` | **+5** (693 -> 698) |
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
| 15 | relevance delta == sum(avg_score) | **8/8 exact** (git-blob baseline `ede4ce3`) |
| 16 | wins/losses vs `meta_log.winner_civ` | **8/8 exact** |
| 17 | log `Winner:` == `meta_log.winner_civ` | **5/5 agree** |
| 18 | registry / generations | **8**, all `gen=1` |
| 19 | extinction risk | **NONE** (lowest +1389.42 = 139x floor) |
| 20 | `simulations_run` delta | **+10 x 8** |
| 21 | meta-vs-ledger `avg_score` (later-`ts` row, this run's rows only) | **0 mismatches** |
| 22 | leaderboard refreshed | **8 civs**, iso `2026-10-25T09:06:36` |
| 23 | `Traceback` in orchestrator log | **0** |
| 24 | `EXC:` in mock log | **0** |
| 25 | mock run-scoped OK-200 responses | **323** (log total 323) |
| 26 | pre-flight: distinct seeds | **40/40** |
| 27 | pre-flight: distinct previews | **40/40** |
| 28 | pre-flight: response body length band | **360** (in 332-369) |
| 29 | pre-flight: independently recomputed md5 | **40/40** |

## Lifetime leaderboard (after session 192)

| civ | relevance | rel/sim | wins | losses | win_rate | gen |
|---|---|---|---|---|---|---|
| civ-poetic | 2106.56 | 1.556 | 6 | 667 | 0.009 | 1 |
| civ-precise | 1953.05 | 1.452 | 430 | 238 | 0.644 | 1 |
| civ-whimsical | 1822.73 | 1.339 | 5 | 668 | 0.007 | 1 |
| civ-mythic | 1684.86 | 1.249 | 10 | 657 | 0.015 | 1 |
| civ-formal | 1647.97 | 1.216 | 98 | 573 | 0.146 | 1 |
| civ-engineer | 1562.26 | 1.162 | 49 | 617 | 0.074 | 1 |
| civ-therapist | 1531.80 | 1.137 | 11 | 659 | 0.016 | 1 |
| **civ-grounded** | **1389.42** | **1.015** | 70 | 602 | 0.104 | 1 |

## Run-level (this run's 10 new rows per civ)

| rank | civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| 1 | civ-poetic | 2.4153 | 1.6720 | 2.5960 | 2.9780 |
| 2 | civ-precise | 2.1980 | 1.1940 | 2.6240 | 2.7760 |
| 3 | civ-formal | 2.1940 | 1.3290 | 2.6100 | 2.6430 |
| 4 | civ-whimsical | 2.1667 | 1.3720 | 2.6750 | 2.4530 |
| 5 | civ-engineer | 2.0033 | 1.3720 | 2.5350 | 2.1030 |
| 6 | civ-grounded | 1.9810 | 1.1650 | 2.6460 | 2.1320 |
| 7 | civ-therapist | 1.9627 | 1.4670 | 2.6570 | 1.7640 |
| 8 | **civ-mythic** | **1.9147** | 1.3190 | 2.6190 | 1.8060 |

Cross-civ spreads: `alignment` **1.2140** › `quality` **0.5070** › `avg_score` **0.5007**
› `novelty` **0.1400**.

## Low-relevance civilizations (as asked)

- **`civ-grounded` — the lifetime low, 64th consecutive session.** `relevance` **1389.42**
  (last of 8), `relevance_per_sim` **1.015** (the lowest in the fleet, and the only civ
  that has sat at ≈1.000 for the whole series). In this run it was **6th of 8** on
  `avg_score` **1.9810**, with `quality` **1.1650** (2nd-lowest) and `alignment`
  **2.1320** (5th). **Its low axes are quality and alignment, not novelty** — run
  novelty **2.6460** is 2nd-highest in the fleet. Lifetime `win_rate` **0.104** is
  **3rd-best in the fleet**, so it is *not* the least-selected civ: **selection and
  relevance are separate axes**. No extinction risk (**139x** the −10 floor).
- **`civ-mythic` — the run-level low for this run** (11th different civ in 11 sessions).
  `avg_score` **1.9147**, `alignment` **1.8060** (lowest), `quality` **1.3190** (2nd-lowest),
  novelty **2.6190** (5th of 8). Lifetime `relevance` **1684.86** (4th of 8) — so it is a
  *run-level* low, not a lifetime one. The alignment gap to the next civ
  (**0.0570**) vs the quality gap (**0.1460**) inverts the usual shape: this run's
  separation was driven at least as much by **prose quality** as by **voice**.
- **`civ-therapist`** is the other low-`alignment` civ this run (**1.7640**, lowest by
  0.0420 over `civ-mythic`), with lifetime `relevance` **1531.80** (7th of 8).

## Chooser vs argmax

| prompt | winner | argmax | argmax score | direction |
|---|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | 2.600 | **down** |
| the bookkeeper's role | civ-precise | civ-poetic | 2.073 | **down** |
| the witness log | civ-precise | civ-precise | 2.587 | agree |
| ternary values | civ-precise | civ-poetic | 2.583 | **down** |
| JEV as a decision oracle | civ-precise | civ-poetic | 2.460 | **down** |

Agreement **1/5 (20 %)**; down-grade disagreements **4**, up-grade **0**.
**12th consecutive session** in which every disagreement is a down-grade.

## Environment recovery

The workspace was **empty** apart from `.plugin-cache` — the prompt's path
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
(**12th consecutive occurrence**).

- Upstream owner: **`SuperInstance/AI-Writings`** — the `ai-writings/…` slug 404s
  (the GitHub API is case-insensitive, and `ai-writings` is a *different* owner with
  README-only marketing repos). `cellular-first-design` is a **subdirectory** of that
  repo, not a repo of its own.
- Discovery route that worked: **`GET /search/code?q=filename:civilization_orchestrator.py`**
  (the `/search/*` quota is separate from the exhausted core quota) → exactly one hit
  with the full path. `GET /user/repos` and `GET /orgs/…/repos` were **403 rate-limited**
  (core 0/5000 remaining, reset ~4.4 h out) and render as "not found" for every
  candidate at once. The **git protocol** is not rate-limited: `git ls-remote` on a
  public repo succeeds instantly, so it distinguishes "does not exist" from "blocked".
- The NAS **EDQUOT** trap blocks `cp` into `/workspace`: the copy reported
  `failed to close …: Disk quota exceeded` while the files **appeared** in `ls -la` at
  size 0. The bridge is a **symlink** to the `/tmp` clone root; all real writes then
  land on the overlay (28 G free) instead of the full NAS mount.
- `ZAI_TOKEN` is **absent** (66th session) ⇒ **Control B mock** is the only provider path.
  `ZAI_URL_OVERRIDE` alone is dead code behind the token gate, so **both** a placeholder
  `ZAI_TOKEN` and the override were set.
- `JEV_KEY` reads `TYPESAFEAI_KEY` but the env var is `TYPESAFE_AI_TOKEN` ⇒ the alias was
  exported. JEV returned HTTP 200 `{"model":"jev-1.14.0"}`; **0 fallback triples**.

## Mock rebuild

All **seven** fixes applied, and the gate passed **12/12 on the FIRST build**. The seed
slice is the **contiguous 4-char slice** `h[(i*2)%8:(i*2)%8+4]` (fix **e**), the index is
**message-derived** `d[0] % 4` (fix **f**), and the figure is
`f"{h[12:16]}/{h[16:20]}/{h[20:24]}"` — three **string** components (fix **g**).

**One thing the algorithm block does not state: the mock must return an OpenAI-shaped
JSON envelope.** `call_provider` reads `r["choices"][0]["message"]["content"]`, so
returning the raw body as the HTTP payload is a `JSONDecodeError` on the first request.
The envelope is `{"choices":[{"index":0,"finish_reason":"stop","message":{"role":
"assistant","content":<body>}}],"model":"glm-4.5",...}`.

Pre-flight body length is **computed from the assembled string** to land on **360**,
inside the response band **332-369**. The cultural-prompt band measured **167-209**.
Both bands were asserted separately. Pre-flight included the
**repeat-same-message probe (40 x 2)** — the check that a distinctness-only gate cannot
make — and the **0 `(civ,prompt)` with >1 seed** check.

**A pre-flight that hardcodes civ names/tenets/voices is a false-failure generator.**
The first pre-flight attempt reported check 12 FAIL at a **145-177** cultural-prompt
band because the fixture used invented tenet strings. The real band **167-209** is
measured from the on-disk `culture.json` files. **Read the real cultures into the
pre-flight; do not hand-type the fixture.**

## Notes for the next session

1. **Check for a concurrent session before pushing** (see the session-191 collision
   write-up). A non-fast-forward rejection whose remote tip is *your* session number
   means another agent ran the same command. Concatenate, don't merge.
2. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild from the
   algorithm block with all **seven** fixes **plus the OpenAI envelope**, and run the
   pre-flight (**12/12 + both length bands + the repeat probe**) **before** the batch.
3. **Do NOT re-run the pre-flight after the batch and then count mock log lines against a
   fixed 120.** Re-running a pre-flight mutates the artifact the check reads.
4. **Derive the verifier's baseline from the baseline COMMIT**, never from a remembered
   count — a stale `BASE_META` from the previous epoch reports a false FAIL.
5. Isolate this run's rows by **count from the end of each civ file** (last 10), never by a
   `ts` cutoff; the meta-vs-ledger check takes the **later-`ts`** row **within this run's
   rows only**.
6. `civ-grounded` has been the low-relevance civ for **64** straight sessions — if it ever
   reads mid-table, check the run-wide seed count first.
7. Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch, stdout redirected **and**
   `< /dev/null`, then poll the log.
8. The NAS EDQUOT trap also blocks **file delivery** — deliver by pushing to git and
   citing the remote URL, not a workspace attachment.
9. **Never `pkill -f` a pattern that appears in your own command line** — it kills the
   calling shell and the tool returns empty output. Match on a PID captured from `ps`.
10. The chooser's down-grade streak is now **12 sessions** and the sweep is **4
    consecutive**. The standing suspect is the `best_civ` criteria map (civ_id -> civ
    name), not the quality signal. **The next real experiment is to bypass the chooser
    and rank purely by `avg_score`** — the data already says the chooser is discarding
    the better candidate on 4 of 5 prompts.
