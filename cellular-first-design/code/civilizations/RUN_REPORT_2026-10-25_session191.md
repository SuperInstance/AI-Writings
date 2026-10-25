# Civ Orchestrator — Run Report, session 191 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 65th session) + **live JEV** (`jev-1.14.0`).
Baseline: `a99fec6` (session 190). **All 29 verification assertions PASS.**

Full detail: this report. **This run was executed CONCURRENTLY with another agent's session
190** — see "The concurrency collision" below, which is the most important finding of this
session.

## Headline for the next session

- **A SECOND AGENT RAN SESSION 190 AGAINST THE SAME REPO WHILE THIS RUN WAS IN FLIGHT.**
  When this run tried to push, the remote had already advanced to `a99fec6`
  ("session 190, 24/24 PASS") — a **different** execution of the same command, with
  **different relevance values** (its `civ-grounded` = **1358.84**, mine = **1349.14**) and
  a different leaderboard timestamp (its `08:53:48`, mine `08:53:17`). The two runs are
  genuinely independent, not duplicates.
  **The push was rejected as non-fast-forward, and the correct resolution was NOT a
  rebase with manual conflict resolution** — it was to **rebase onto the remote's session
  190 and concatenate**: keep the remote's 80 rows, append this run's 80 rows and 5
  `meta_log` entries, and **recompute the cumulative `culture.json` state and the
  leaderboard** from the combined total. The result is a single coherent **session 191**
  (160 rows across two runs) with 29/29 PASS.
- **`civ-precise` SWEPT 5/5 FOR THE THIRD CONSECUTIVE SWEEP — AND IT IS A CHOOSER EFFECT,
  NOT QUALITY.** The chooser disagreed with the `avg_score` argmax on **3 of 5** prompts
  and **all three took the LOWER-scoring candidate** — the **11th consecutive session** in
  which a chooser/argmax disagreement is a *down*-grade. Agreement **2/5 (40 %)**.
  `civ-poetic` was the argmax on **3 of 5** prompts and won **none** of them.
  **The `best_civ` criteria map (civ_id -> civ name) is the suspect, not the quality
  signal.** `win_rate` is not a quality metric.
- **`civ-grounded` remains the lifetime low-relevance civ — 63rd consecutive session.**
  Last of 8 on lifetime `relevance` **1369.61** and `relevance_per_sim` **1.008**. Its
  lifetime `win_rate` is **0.105** — **3rd-best in the fleet** behind `precise` (0.641)
  and `formal` (0.147). Lowest relevance = **137x** the −10 floor ⇒ **no extinction risk**.
- **THE RUN-LEVEL LOW ROTATED TO `civ-therapist`** (run `avg_score` **0.9863**,
  `alignment` **0.2250**, `quality` **0.1710**) — a **10th different civ in 10 sessions**.
  Alignment gap **0.0990** vs quality gap **0.0580** = **1.71x wider** ⇒ still a **voice**
  failure, but the **narrowest voice/quality ratio in the series** (earlier sessions ran
  2.95x-3.18x). *The holder rotates; the axis does not.*
- **THE AXIS SPREAD IS DOMINATED BY ALIGNMENT, NOT QUALITY.** Cross-civ spreads this run:
  `alignment` **1.4360** › `avg_score` **0.5037** › `quality` **0.2670** › `novelty`
  **0.1500**. Novelty is nearly flat across the fleet (2.456-2.606) — the entire ranking
  this run is produced by `alignment` and `quality`.

## The concurrency collision (the durable lesson)

**Two agents ran the same session against the same upstream repo within ~3 minutes of
each other.** The observable signature is a push rejected as `non-fast-forward` whose
hint says *"the tip of your current branch is behind its remote counterpart"* — and the
remote's tip is a **session commit for the same session number you are about to write**.

What to do, in order:

1. **Do NOT rebase and resolve the jsonl conflicts by hand.** Both runs appended to the
   same eight ledgers, so every `simulations.jsonl`, `culture.json`, `leaderboard.json`
   and `meta_log.jsonl` conflicts. A textual merge of two independently-appended
   ledgers produces a file that passes no invariant.
2. **Fetch the remote tip and identify the collision:**
   `git fetch --depth 50 <token-url> main` then `git log --oneline FETCH_HEAD`. If the
   remote tip is a session commit for **your** session number, it is a collision.
3. **Confirm the two runs are independent, not duplicates.** Compare the leaderboard
   relevance values and the `iso` timestamps. Different numbers + different timestamps ⇒
   two real executions. Identical values ⇒ you are replaying, and you should rebase and
   drop your commit instead of concatenating.
4. **Reset to the remote tip, then CONCATENATE:**
   - `git reset --hard FETCH_HEAD` (restores the remote's rows and state),
   - extract **your** rows as the **last N per ledger** and your `meta_log` entries as the
     **last M** from your own commit (keep your commit alive — `git show <sha>:<path>` —
     **before** resetting),
   - append them to the remote's ledgers,
   - **recompute `culture.json`** for every civ: `relevance_score += Σ your avg_score`,
     `wins += your meta_log winner count`, `losses += (M - wins)`, `simulations_run += N`,
   - **regenerate `leaderboard.json`** from the combined `culture.json` state, matching
     the orchestrator's own `update_leaderboard` (sort by `relevance_per_sim` desc,
     round `relevance` to 2dp / `relevance_per_sim` to 3dp / `win_rate` to 3dp).
5. **Re-verify against the REMOTE commit as the baseline**, and re-scope the
   run-isolation logic to your own rows: slice the **last 10** per civ, and restrict the
   meta-vs-ledger check to **your** rows before taking the later-`ts` row. A check that
   searches the whole ledger will now match the *other* run's row for the same
   `(civ, prompt)` and report a false mismatch.
6. **Number the session by what is on the remote, not by what you planned.** The remote
   already held session 190, so this run is **session 191** — even though it executed the
   same command with the same parameters.

**A stale baseline constant in the verifier is the second trap.** The verifier carried
`BASE_META = 683` from the previous session; after the collision the correct baseline is
the remote's **688**. A hardcoded count from an earlier epoch reports a false FAIL
(check 3), and a ledger search scoped to the wrong epoch reports a false mismatch
(check 21). **Derive the baseline from the baseline COMMIT, never from a remembered
number.**

## Verification — 29/29 PASS

Baseline commit: `a99fec6` (remote session 190). This run's rows are the **last 10** per
civ ledger; this run's `meta_log` entries are the **last 5**.

| # | assertion | result |
|---|---|---|
| 1 | per-civ ledger delta | **+10 x 8 = 80** |
| 2 | total new rows | **80** |
| 3 | `meta_log` | **+5** (688 -> 693) |
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
| 15 | relevance delta == sum(avg_score) | **8/8 exact** (git-blob baseline `a99fec6`) |
| 16 | wins/losses vs `meta_log.winner_civ` | **8/8 exact** |
| 17 | log `Winner:` == `meta_log.winner_civ` | **5/5 agree** |
| 18 | registry / generations | **8**, all `gen=1` |
| 19 | extinction risk | **NONE** (lowest +1369.61 = 137x floor) |
| 20 | `simulations_run` delta | **+10 x 8** |
| 21 | meta-vs-ledger `avg_score` (later-`ts` row, this run's rows only) | **0 mismatches** |
| 22 | leaderboard refreshed | **8 civs**, iso `2026-10-25T08:56:53` |
| 23 | `Traceback` in orchestrator log | **0** |
| 24 | `EXC:` in mock log | **0** |
| 25 | mock run-scoped OK-200 responses | **80** (window at offset 40 of 240 log lines) |
| 26 | pre-flight: distinct seeds / previews | **40/40**, **40/40** |
| 27 | pre-flight: independently recomputed md5 | **40/40** |
| 28 | pre-flight: response body length band | **360** (in 332-369) |
| 29 | pre-flight: cultural-prompt length band | **167-209** |

## Lifetime leaderboard (after session 191 = remote 190 + this run)

| civ | relevance | rel/sim | wins | losses | win_rate | gen |
|---|---|---|---|---|---|---|
| civ-poetic | 2082.41 | 1.549 | 6 | 662 | 0.009 | 1 |
| civ-precise | 1931.07 | 1.446 | 425 | 238 | 0.641 | 1 |
| civ-whimsical | 1801.06 | 1.333 | 5 | 663 | 0.007 | 1 |
| civ-mythic | 1665.71 | 1.244 | 10 | 652 | 0.015 | 1 |
| civ-formal | 1626.03 | 1.209 | 98 | 568 | 0.147 | 1 |
| civ-engineer | 1542.23 | 1.156 | 49 | 612 | 0.074 | 1 |
| civ-therapist | 1512.18 | 1.131 | 11 | 654 | 0.017 | 1 |
| **civ-grounded** | **1369.61** | **1.008** | 70 | 597 | 0.105 | 1 |

## Run-level (this run's 10 new rows per civ)

| rank | civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| 1 | civ-precise | 1.4900 | 0.2720 | 2.5370 | 1.6610 |
| 2 | civ-poetic | 1.4837 | 0.4260 | 2.5390 | 1.4860 |
| 3 | civ-formal | 1.3050 | 0.2580 | 2.5470 | 1.1100 |
| 4 | civ-whimsical | 1.2843 | 0.2910 | 2.6060 | 0.9560 |
| 5 | **civ-grounded** | 1.0773 | 0.1590 | 2.5690 | 0.5040 |
| 6 | civ-engineer | 1.0457 | 0.2210 | 2.4760 | 0.4400 |
| 7 | civ-mythic | 1.0030 | 0.2290 | 2.4560 | 0.3240 |
| 8 | **civ-therapist** | **0.9863** | 0.1710 | 2.5630 | 0.2250 |

Cross-civ spreads: `alignment` **1.4360** › `avg_score` **0.5037** › `quality` **0.2670**
› `novelty` **0.1500**.

## Low-relevance civilizations (as asked)

- **`civ-grounded` — the lifetime low, 63rd consecutive session.** `relevance` **1369.61**
  (last of 8), `relevance_per_sim` **1.008** (still the lowest in the fleet, and the only
  civ that has sat at ≈1.000 for the whole series). In this run it was **5th of 8** on
  `avg_score` **1.0773**, with `quality` **0.1590** (2nd-lowest) and `alignment`
  **0.5040** (4th-lowest). **Its low axes are quality and alignment, not novelty** —
  run novelty **2.5690** is 4th of 8 (mid-field). Lifetime `win_rate` **0.105** is
  **3rd-best in the fleet**, so it is *not* the least-selected civ: **selection and
  relevance are separate axes**. No extinction risk (**137x** the −10 floor).
- **`civ-therapist` — the run-level low for this run** (10th different civ in 10
  sessions). `avg_score` **0.9863**, `alignment` **0.2250** (lowest), `quality`
  **0.1710**, novelty **2.5630** (3rd-highest). Lifetime `relevance` **1512.18** (7th of 8).
  The alignment gap to the next civ (**0.0990**) is **1.71x** the quality gap
  (**0.0580**) ⇒ a **voice** failure, not a prose failure.
- **`civ-mythic` and `civ-engineer`** are the other low-`avg_score` civs this run
  (**1.0030** and **1.0457**), both dragged by `alignment` (**0.3240** / **0.4400**).

## Chooser vs argmax

| prompt | winner | argmax | argmax score | direction |
|---|---|---|---|---|
| what a cell is | civ-precise | civ-precise | 1.473 | agree |
| the bookkeeper's role | civ-precise | civ-poetic | 1.353 | **down** |
| the witness log | civ-precise | civ-precise | 1.783 | agree |
| ternary values | civ-precise | civ-poetic | 1.807 | **down** |
| JEV as a decision oracle | civ-precise | civ-poetic | 1.520 | **down** |

Agreement **2/5 (40 %)**; down-grade disagreements **3**, up-grade **0**.
**11th consecutive session** in which every disagreement is a down-grade.

## Environment recovery

The workspace was **empty** apart from `.plugin-cache` — the prompt's path
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
(**11th consecutive occurrence**).

- Upstream owner: **`SuperInstance/AI-Writings`** — the `ai-writings/…` slug 404s
  (the GitHub API is case-insensitive). `cellular-first-design` is a **subdirectory** of
  that repo, not a repo of its own.
- `GET /user/repos` was rate-limited (403) and `GET /search/repositories` returned
  unrelated hits; the working discovery route was
  **`GET /search/code?q=filename:civilization_orchestrator.py`**, which returned exactly
  one hit with the full path.
- The repo is **3.7 GB** and `/workspace` is at **100 % NAS quota**, so the clone was
  **sparse + shallow**: `git clone --depth 1 --filter=blob:none --no-checkout`, then
  `sparse-checkout set cellular-first-design`, then checkout. Working tree: **9.1 MB**.
- The first full clone died mid-fetch with `could not open ... tmp_pack_* for reading`.
  The blobless clone avoided it.
- The NAS **EDQUOT** trap also blocks `cp` into `/workspace`: the copy reported
  `failed to close ...: Disk quota exceeded` while the files **appeared** in `ls -la` at
  size 0. The bridge is a **symlink** to the `/tmp` clone root, verified with
  `os.path.samefile()` (shell `test -ef` is broken in this sandbox).
- `ZAI_TOKEN` is **absent** (65th session) ⇒ **Control B mock** is the only provider path.
  `ZAI_URL_OVERRIDE` alone is dead code behind the token gate, so **both** a placeholder
  `ZAI_TOKEN` and the override were set.
- `JEV_KEY` reads `TYPESAFEAI_KEY` but the env var is `TYPESAFE_AI_TOKEN` ⇒ the alias was
  exported. JEV returned HTTP 200 `{"model":"jev-1.14.0"}`; **0 fallback triples**.

## Mock rebuild (all SEVEN fixes, passed the gate on the FIRST build)

The seed slice is the **contiguous 4-char slice** `h[(i*2)%8:(i*2)%8+4]` (fix **e**), the
index is **message-derived** `d[0] % 4` (fix **f**), and the figure is
`f"{h[12:16]}/{h[16:20]}/{h[20:24]}"` — three **string** components (fix **g**).

The pre-flight body length is **computed from the assembled string** (the seed+colour+
figure prefix is ~90 chars of variable width) to land on **360**, inside the response band
**332-369**. The cultural-prompt band measured **167-209**. Both bands were asserted
separately.

Pre-flight: **12/12 PASS**, including the **repeat-same-message probe (40 x 2)** — the
check that a distinctness-only gate cannot make.

## Notes for the next session

1. **Check for a concurrent session before pushing** (see "The concurrency collision").
   A non-fast-forward rejection whose remote tip is *your* session number means another
   agent ran the same command. Concatenate, don't merge.
2. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild from the
   algorithm block with all **seven** fixes, and run the pre-flight (**40/40/40 + both
   length bands + the repeat probe**) **before** the batch.
3. **Do NOT re-run the pre-flight after the batch and then count mock log lines against a
   fixed 120.** This session's first verification pass reported a false FAIL on check 25
   (240 log lines vs the expected 120) purely because the pre-flight was re-run to
   regenerate its captured output, adding 120 mock calls. The check was re-derived as a
   **run-scoped multiset window**: the 80 run calls are provably at **offset 40** of the
   240 log lines, because that window's seed multiset equals the ledger's 80-row seed
   multiset exactly. **Re-running a pre-flight mutates the artifact the check reads.**
4. **Derive the verifier's baseline from the baseline COMMIT**, never from a remembered
   count — a stale `BASE_META` from the previous epoch reported a false FAIL on check 3
   and a false mismatch on check 21 after the collision.
5. Isolate this run's rows by **count from the end of each civ file** (last 10), never by a
   `ts` cutoff; the meta-vs-ledger check takes the **later-`ts`** row **within this run's
   rows only**.
6. `civ-grounded` has been the low-relevance civ for **63** straight sessions — if it ever
   reads mid-table, check the run-wide seed count first.
7. Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch, stdout redirected **and**
   `< /dev/null`, then poll the log.
8. The NAS EDQUOT trap also blocks **file delivery** — deliver by pushing to git and
   citing the remote URL, not a workspace attachment.
9. **Never `pkill -f` a pattern that appears in your own command line** — it kills the
   calling shell and the tool returns empty output. Match on a PID captured from `ps`.
10. **The chooser's down-grade streak is now 11 sessions and the sweep is 3 consecutive.**
    The standing suspect is the `best_civ` criteria map (`civ_id` -> civ name), not the
    quality signal.
