# Civ Orchestrator — Run Report, session 194 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 68th session) + **live JEV** (`jev-1.14.0`).
Baseline: `99b9b06` (session 193). **All 26 verification assertions PASS.**

## Headline for the next session

- **THE 5/5 CHOOSER SWEEP IS A CHOOSER EFFECT, AND THE DOWN-GRADE STREAK IS BACK AND RUNNING.**
  `civ-precise` won all 5 competitions, but on **4 of 5** it was *not* the `avg_score`
  argmax — and **all 4 disagreements took the LOWER-scoring candidate**. `civ-poetic` was
  the argmax on **4 of 5** prompts and won **none**. Agreement **1/5 (20 %)**. This is the
  **13th consecutive session** in which a chooser/argmax disagreement is a *down*-grade,
  so **the streak statistic must be re-based to 13, not 0** (session 193 broke the streak
  at 0; this session re-established it). The standing suspect is unchanged: the
  `best_civ` criteria map (`civ_id -> civ name`) being read as a quality signal.
- **`civ-grounded` remains the lifetime low-relevance civ — 66th consecutive session.**
  Last of 8 on lifetime `relevance` **1428.24** and `relevance_per_sim` **1.028**. Its
  lifetime `win_rate` is **0.103** — **3rd-best in the fleet** behind `precise` (0.649)
  and `formal` (0.144). Lowest relevance = **143x** the −10 floor ⇒ **no extinction risk**.
- **THE RUN-LEVEL LOW ROTATED TO `civ-therapist`** (run `avg_score` **1.8147**,
  `alignment` **1.4910** lowest, `quality` **1.2980** lowest) — a **13th different civ in 13
  sessions**. *The holder rotates; the axis does not.*
- **THE AXIS SPREAD IS DOMINATED BY ALIGNMENT, NOT QUALITY.** Cross-civ spreads this run:
  `alignment` **1.6570** › `avg_score` **0.7413** › `quality` **0.6540** › `novelty`
  **0.1540**. Novelty is nearly flat across the fleet (2.501–2.655) — the entire ranking
  this run is produced by `alignment` and `quality`. Same shape as sessions 191–193.
- **PRE-FLIGHT PASSED 13/13 ON THE FIRST BUILD AFTER ONE TEMPLATE FIX.** The gate caught a
  **711-char** response body against the **332–369** band; trimming the template to **354**
  put it in-band. The band is doing its job.

## Verification — 26/26 PASS

Baseline commit: `99b9b06` (session 193). This run's rows are the **last 10** per
civ ledger; this run's `meta_log` entries are the **last 5**.

| # | assertion | result |
|---|---|---|
| 1 | per-civ ledger delta | **+10 x 8 = 80** |
| 2 | total new rows | **80** |
| 3 | `meta_log` | **+5** (703 -> 708) |
| 4 | `Winner:` lines in log | **5** |
| 5 | rows with a JEV `error` key | **0** |
| 6 | 2.0/2.0/2.0 fallback triples | **0** |
| 7 | `provider` on all rows | **`zai` x 80** |
| 8 | rows missing `[mock-zai` prefix | **0** (80/80) |
| 9 | rows matching an independently recomputed seed+color+figure | **80/80** |
| 10 | distinct seeds (message-level) | **40/40**, multiplicities consistent |
| 11 | `(civ,prompt)` combos with >1 seed | **0** |
| 12 | per-prompt 8/8 distinct seeds (5 prompts) | **8/8 x 5** |
| 13 | per-prompt 8/8 distinct previews (5 prompts) | **8/8 x 5** |
| 14 | relevance delta == sum(avg_score) | **8/8 exact** |
| 15 | wins/losses vs `meta_log.winner_civ` | **8/8 exact** |
| 16 | log `Winner:` == `meta_log.winner_civ` | **5/5 agree** |
| 17 | registry / generations | **8**, all `gen=1` |
| 18 | extinction risk | **NONE** (lowest +1428.24 = 143x floor) |
| 19 | `simulations_run` delta | **+10 x 8** |
| 20 | meta-vs-ledger `avg_score` (later-`ts` row, this run's rows only) | **0 mismatches** |
| 21 | leaderboard refreshed | **8 civs**, iso `2026-10-25T09:29:37` |
| 22 | `Traceback` in orchestrator log | **0** |
| 23 | `EXC:` in mock log | **0** |
| 24 | mock run-scoped OK-200 responses | **161** |
| 25 | pre-flight | **13/13 PASS** |
| 26 | no birth (new civ dirs) | **0** |

## Environment recovery

The workspace was **empty** apart from `.plugin-cache` and `.skills` — the prompt's path
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
(**14th consecutive occurrence**).

- Upstream owner: **`SuperInstance/AI-Writings`**. The `ai-writings/…` slug 404s (the GitHub
  API is case-insensitive, and `ai-writings` is a *different* owner with README-only marketing
  repos). `cellular-first-design` is a **subdirectory** of that repo, not a repo of its own.
- **THE AUTHENTICATED REST QUOTA WAS ALREADY EXHAUSTED AT SESSION START (5000/5000, 403).**
  `GET /user/repos` and `GET /user` both rendered as 403 for *every* candidate, which looks
  exactly like "the repo does not exist". The recovery was:
  1. `GET /rate_limit` (unauthenticated) to read the reset time;
  2. **`/search/*` has a separate quota** — `GET /search/repositories` still served requests
     and was enough to identify the owner;
  3. **the git protocol is NOT rate-limited** — `git ls-remote` on a public repo succeeds
     instantly, so it distinguishes "does not exist" from "blocked". This is the only
     reliable absence test while the core quota is exhausted;
  4. wait out the reset (09:26:39Z), then `GET /user` → the token owner is
     **`SuperInstance` (Casey Digennaro, uid 193104091)** — *not* `rio-ARC`, which is a
     different account that shares a repo name in search results.
  **Lesson: a 403 on the core API renders as "not found" for every candidate at once.**
  Check `/rate_limit` before concluding a repo is absent.
- The NAS **EDQUOT** trap blocked writes into `/workspace` (`dd` of 2 MB → `Disk quota
  exceeded`, leaving a 0-byte file that still appears in `ls -la`). The bridge is a
  **symlink** to the clone root on the overlay (28 G free).
- **The bridge must point at the INNER `cellular-first-design` directory.** The upstream repo
  root contains a `cellular-first-design/` subdirectory, so the symlink must target the
  **inner** directory, or the orchestrator's hardcoded `CIVS_DIR` misses `civilizations.json`.
  Verified by **inode identity** (`stat -L -c '%d:%i'`) — the shell `[ -ef ]` test is
  unreliable here.
- Clone: `--filter=blob:none --no-checkout --depth 1` + `sparse-checkout set
  cellular-first-design` ⇒ **9.4 MB** working tree. Cloning into `/workspace` fails with
  **`Disk quota exceeded`** (NAS EDQUOT, **14th session**).
- `ZAI_TOKEN` is **absent** from the env (68th session); the real z.ai endpoint is not
  reachable with the available credentials ⇒ **Control B mock** is the only provider path.
  `ZAI_URL_OVERRIDE` alone is dead code behind the token gate, so **both** a placeholder
  `ZAI_TOKEN` and the override were set.
- `JEV_KEY` reads `TYPESAFEAI_KEY` but the env var is `TYPESAFE_AI_TOKEN` ⇒ the alias was
  exported. JEV returned HTTP 200 `{"model":"jev-1.14.0"}`; **0 fallback triples**.
- `gh` not installed — used `GET /user/repos` with `GITHUB_TOKEN`.

## Mock rebuild — the eight fixes, and the band that caught the build

All **seven** documented fixes plus the **OpenAI envelope** were applied:

| # | Fix | Applied |
|---|---|---|
| a | seed index wrap `h[(i*2)%8:…]` | yes |
| b | md5 of the **whole** user message | yes |
| c | `Connection: close` + `Content-Length` | yes |
| d | interpolate the seed placeholder | yes |
| e | seed widened to a **contiguous 4-hex-char slice** | yes |
| f | index from the **message** (`d[0] % 4`), not a request counter | yes |
| g | `figure` = three **string** components, not a division | yes |
| h | **OpenAI envelope** `choices[0].message.content` | yes |

**The response-body length band caught a real build error on the first attempt.** The
template rendered at **711** characters against the **332–369** band, and the gate
reported `[FAIL] response body length band 332-369 min=711 max=711` — a clean,
localised FAIL, not a crash. Trimming the body to **354** put it in-band. The cultural-
prompt band (167–209) passed unchanged.

The band matters for a reason that is not cosmetic: a body longer than ~369 characters
pushes the **seed prefix out of the 200-char `content_preview` truncation**, which would
silently break the seed+color+figure recompute check for every row.

**A GATE THAT PRINTS FOUR PASSES AND THEN CRASHES IS NOT A PASSING GATE.** The pre-flight
prints a final verdict and exits non-zero on any failure; the batch is only launched
after `PRE-FLIGHT PASS 13/13`.

## Lifetime leaderboard (after session 194)

| civ | relevance | rel/sim | wins | losses | win_rate | gen |
|---|---|---|---|---|---|---|
| civ-poetic | 2153.40 | 1.567 | 6 | 677 | 0.009 | 1 |
| civ-precise | 2000.55 | 1.466 | 440 | 238 | 0.649 | 1 |
| civ-whimsical | 1860.66 | 1.347 | 5 | 678 | 0.007 | 1 |
| civ-mythic | 1725.79 | 1.261 | 10 | 667 | 0.015 | 1 |
| civ-formal | 1692.01 | 1.231 | 98 | 583 | 0.144 | 1 |
| civ-engineer | 1607.55 | 1.179 | 49 | 627 | 0.072 | 1 |
| civ-therapist | 1565.07 | 1.145 | 11 | 669 | 0.016 | 1 |
| civ-grounded | 1428.24 | 1.028 | 70 | 612 | 0.103 | 1 |

## Run-level (this run's 10 new rows per civ)

| rank | civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| 1 | civ-poetic | 2.5560 | 1.9410 | 2.5790 | 3.1480 |
| 2 | civ-engineer | 2.5070 | 1.9520 | 2.5010 | 3.0680 |
| 3 | civ-precise | 2.4843 | 1.7330 | 2.5910 | 3.1290 |
| 4 | civ-mythic | 2.4503 | 1.8320 | 2.5700 | 2.9490 |
| 5 | civ-formal | 2.4133 | 1.7250 | 2.5250 | 2.9900 |
| 6 | civ-grounded | 2.1423 | 1.3640 | 2.5820 | 2.4810 |
| 7 | civ-whimsical | 1.9893 | 1.4650 | 2.5790 | 1.9240 |
| 8 | civ-therapist | 1.8147 | 1.2980 | 2.6550 | 1.4910 |

Cross-civ spreads: `alignment` **1.6570** › `avg_score` **0.7413** › `quality` **0.6540**
› `novelty` **0.1540**.

## Low-relevance civilizations (as asked)

- **`civ-grounded` — the lifetime low, 66th consecutive session.** `relevance` **1428.24**
  (last of 8), `relevance_per_sim` **1.028** (the lowest in the fleet). In this run it was
  **6th of 8** on `avg_score` **2.1423**, with `quality` **1.3640** (2nd-lowest) and
  `alignment` **2.4810** (3rd-lowest). **Its low axes are quality and alignment, not
  novelty** — run novelty **2.5820** is 2nd-highest in the fleet. Lifetime `win_rate`
  **0.103** is **3rd-best in the fleet**, so it is *not* the least-selected civ:
  **selection and relevance are separate axes**. No extinction risk (**143x** the −10 floor).
- **`civ-therapist` — the run-level low for this run** (13th different civ in 13 sessions).
  `avg_score` **1.8147**, `alignment` **1.4910** (lowest), `quality` **1.2980** (lowest),
  novelty **2.6550** (**highest in the fleet**). Lifetime `relevance` **1565.07** (7th of 8)
  — so it is a *run-level* low, not a lifetime one. The gap to the next civ is **0.1746** on
  `avg_score` and **0.4330** on `alignment` — this run's separation was driven by **voice**
  (alignment) far more than by prose (quality), with novelty flat and inverted.
- **`civ-whimsical`** is the other low-`alignment` civ this run (**1.9240**, 2nd-lowest)
  with lifetime `relevance` **1860.66** (3rd of 8) — a *run-level* low on alignment despite
  a high lifetime standing. Its `quality` **1.4650** is 3rd-lowest.

**The three low civs share one signature: high novelty, low alignment.** `civ-therapist`
(novelty 2.6550 / alignment 1.4910) and `civ-whimsical` (2.5790 / 1.9240) both have
above-average novelty and below-average alignment. The meta-GAN selects on `alignment`,
so novelty does not rescue them. **The low-relevance axis is voice, not novelty.**

## Chooser vs argmax

| prompt | winner | argmax | argmax score | winner score | direction |
|---|---|---|---|---|---|
| Write 100 words on what a cell is. | civ-precise | civ-poetic | 2.513 | 2.313 | DOWN |
| Write 100 words on the bookkeeper's role. | civ-precise | civ-poetic | 2.830 | 2.630 | DOWN |
| Write 100 words on the witness log. | civ-precise | civ-precise | 2.750 | 2.750 | agree |
| Write 100 words on ternary values. | civ-precise | civ-poetic | 2.290 | 2.160 | DOWN |
| Write 100 words on JEV as a decision oracle. | civ-precise | civ-poetic | 2.610 | 2.543 | DOWN |

Agreement **1/5 (20 %)**; down-grade disagreements **4**, up-grade **0**.
**The down-grade streak is back — re-base it to 13.**

`civ-poetic` was the `avg_score` argmax on **4 of 5** prompts and won **0 of 5**;
`civ-precise` was the argmax on **1 of 5** and won **5 of 5**. The chooser is not
selecting the higher-scoring candidate, and the direction is consistently against it.

## Notes for the next session

1. **The `ai-writings` slug is a trap and the REST 403 is a disguise.** The path in the
   prompt never exists in a fresh workspace (14th occurrence), and the recovery route
   differs from the last session's: the **core** API quota was already exhausted at 09:12Z,
   so the route that worked was **git-protocol absence testing + `/search/repositories` +
   wait-out-the-reset**, not `GET /user/repos`.
2. **The mock is not on disk at session start (`/tmp` wiped)** — rebuild from the algorithm
   block with all **seven** fixes **plus the OpenAI envelope**, and run the pre-flight
   (**13/13**) **before** the batch. The **response-body band** is the one that will fail
   on a fresh build if the template is not trimmed — target **354**.
3. **Do NOT re-run the pre-flight after the batch and then count mock log lines against a
   fixed number.** Re-running a pre-flight mutates the artifact the check reads. The
   mock log for this session reads **161** OK-200 lines = 80 (pre-flight) + 80 (run) + 1 (GET).
4. **Derive the verifier's baseline from the baseline COMMIT**, never from a remembered
   count — a stale `BASE_META` from the previous epoch reports a false FAIL.
5. **A verifier bug can masquerade as a run defect.** The first pass of this session's
   verifier reported `[FAIL] per-civ ledger delta +10 x 8` with deltas of **−1412** — the
   check compared the *slice length* (10) against the baseline *count*. The run was
   clean; the assertion was mis-written. **A delta of roughly −(baseline) is the
   signature of comparing a slice against a count**, not of a truncated ledger.
6. Isolate this run's rows by **count from the end of each civ file** (last 10), never by a
   `ts` cutoff; the meta-vs-ledger check takes the **later-`ts`** row **within this run's
   rows only**.
7. **The distinct-seeds check is message-level (40), not row-level (80).** Assert 40
   distinct seeds + one seed per `(civ, prompt)` slot + multiplicity == slot row count.
8. `civ-grounded` has been the low-relevance civ for **66** straight sessions — if it ever
   does not, that is worth more attention than another clean run.
