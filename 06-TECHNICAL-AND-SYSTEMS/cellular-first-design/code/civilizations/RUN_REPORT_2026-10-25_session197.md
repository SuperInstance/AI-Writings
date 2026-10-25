# Civ Orchestrator — Run Report, session 197 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 71st session) + **live JEV** (`jev-1.14.0`).
Baseline: `e1ab42c` (session 196). **All 27 verification assertions PASS.** Pre-flight **14/14 PASS**.

## Headline for the next session

- **`civ-precise` SWEPT 5/5 FOR THE SEVENTH CONSECUTIVE SWEEP — AND IT IS STILL A CHOOSER
  EFFECT.** The chooser disagreed with the `avg_score` argmax on **4 of 5** prompts and
  **all four took the LOWER-scoring candidate** — the **16th consecutive session** in
  which a chooser/argmax disagreement is a *down*-grade. Agreement **1/5 (20 %)**.
  `civ-poetic` was the argmax on **3 of 5** and won **0 of 5**; `civ-formal` was the argmax
  on **1 of 5** and won **0 of 5**; `civ-precise` was the argmax on **1 of 5** and won
  **5 of 5**. **Re-base the streak to 16.**
- **`civ-grounded` remains the lifetime low — 69th consecutive session.** Last of 8 on
  lifetime `relevance` **1490.66** and `relevance_per_sim` **1.051** (the lowest in the
  fleet). Lifetime `win_rate` **0.100** — **3rd-best in the fleet** behind `precise`
  (0.657) and `formal` (0.141). Lowest relevance = **149x** the −10 floor ⇒ **no
  extinction risk**. *Selection and relevance are separate axes: the least-relevant civ
  is not the least-selected one.*
- **THE RUN-LEVEL LOW ROTATED TO `civ-therapist`** (run `avg_score` **1.9480**,
  `alignment` **2.3660** lowest) — a **16th different civ in 16 sessions**. *The holder
  rotates; the axis does not.*
- **THE AXIS SPREAD IS DOMINATED BY ALIGNMENT.** Cross-civ spreads this run:
  `alignment` **0.7610** › `quality` **0.4650** › `novelty` **0.3730** › `avg_score`
  **0.3460**. Same shape as sessions 191–196, but the **novelty spread is the widest
  recorded in the series** (0.3730 vs 0.1230 in session 196) and the **alignment spread
  is the narrowest** (0.7610 vs 1.5440).
- **THE TWO LOW CIVS SPLIT INTO TWO DISTINCT SIGNATURES AGAIN — THE THIRD SESSION IN A
  ROW.** `civ-therapist` is low on **alignment** (2.3660, fleet-low). But `civ-grounded`
  is **not** on alignment this time (2.7850, 3rd-lowest) and is **not** the run-level
  low either — it sits **6th of 8** on `avg_score` **2.0420**, with `quality` **1.1610**
  (2nd-lowest) and `novelty` **2.1800** (mid-pack). *`civ-grounded`'s lifetime low and
  this run's low holder are different civs for the second session running. Report the
  axis per civ; do not assume one signature covers every low civ.*

## Verification — 27/27 PASS

Baseline commit: `e1ab42c` (session 196), derived by reading the **git blob** of each
ledger and `culture.json` — never from a remembered count. This run's rows are the
**last 10** per civ ledger; this run's `meta_log` entries are the **last 5**.

| # | assertion | result |
|---|---|---|
| 1 | per-civ ledger delta | **+10 x 8 = 80** |
| 2 | total new rows | **80** |
| 3 | `meta_log` | **+5** (718 -> 723) |
| 4 | `Winner:` lines in log | **5** |
| 5 | rows with a JEV `error` key | **0** |
| 6 | 2.0/2.0/2.0 fallback triples | **0** |
| 7 | `provider` on all rows | **`zai` x 80** |
| 8 | rows carrying seed+color+figure markers | **80/80** |
| 9 | rows matching an independently recomputed seed+color+figure | **80/80** |
| 10 | distinct seeds (message-level) | **40/40** |
| 11 | `(civ,prompt)` combos with >1 seed | **0** |
| 12 | per-prompt 8/8 distinct seeds (5 prompts) | **8/8 x 5** |
| 13 | per-prompt 8/8 distinct previews (5 prompts) | **8/8 x 5** |
| 14 | relevance delta == sum(avg_score) | **8/8 exact** (max residual **5.08e-13**) |
| 15 | wins/losses vs `meta_log.winner_civ` | **8/8 exact** (precise 5, others 0) |
| 16 | log `Winner:` == `meta_log.winner_civ` | **5/5 agree** |
| 17 | registry / generations | **8**, all `gen=1` |
| 18 | extinction risk | **NONE** (lowest +1490.66 = 149x floor) |
| 19 | `simulations_run` delta | **+10 x 8** |
| 20 | meta-vs-ledger `avg_score` (later-`ts` row, same civ+prompt) | **0 mismatches** |
| 21 | leaderboard refreshed | **8 civs**, iso `2026-10-25T09:55:22` |
| 22 | `Traceback` in orchestrator log | **0** |
| 23 | `EXC:` in mock log | **0** (of 160 POST-200) |
| 24 | **run-scoped proof**: last 80 OK seed multiset == ledger seed multiset | **PASS** |
| 25 | no birth (new civ dirs) | **0** |
| 26 | this run's rows are the last 10, increasing `ts` | **8/8** |
| 27 | no `None`/NaN `avg_score` | **PASS** |

### Check 8 was re-derived this session: the literal `[mock-zai seed=` prefix is NOT a contract

The historical check 8 counted rows whose `content_preview` begins with the literal
string `[mock-zai seed=`. This session's mock renders the body as
`seed=446f color=d64d figure=c8a2/50a5/dcdd voice=…` — the **markers are present and
correct**, but the bracketed prefix is not, so the literal check reported a **false FAIL**
on a perfectly good dataset.

**Durable rule: check the SEMANTIC MARKERS, not a decorative prefix string.** The
substantive check is the **independent recompute** (check 9): re-derive
`seed`/`color`/`figure` from the md5 of the *whole* user message and require the row to
carry those exact values. That passed **80/80**. A prefix-string check can only ever
certify that the mock was built by the same template as the last mock — it certifies
nothing about the data, and it breaks whenever the template's punctuation changes.
**Prefer the recompute.**

## Environment recovery

- The workspace was **empty** apart from `.plugin-cache`; the prompt's path did not exist
  (**17th consecutive occurrence**).
- Upstream owner: **`SuperInstance/AI-Writings`** — `cellular-first-design` is a
  **subdirectory** of that repo, not a repo of its own. The `ai-writings/…` org slug
  404s (the GitHub API is case-insensitive) and the org is a *different* owner with
  README-only repos. `gh` is not installed — used the REST API with `GITHUB_TOKEN`.
- **A FULL CLONE INTO `/workspace` DIES, BUT CLONING INTO `/tmp` WORKS.** The clone into
  `/workspace/repos` failed on `.git/description` with **`Disk quota exceeded`**; the
  identical clone into `/tmp` succeeded. The quota is on the **NAS mount**
  (600 G/600 G, 100 % full while visibly empty), not on the clone.
- **THE BRIDGE SYMLINK MUST POINT AT THE INNER `cellular-first-design` DIRECTORY.** The
  orchestrator's hardcoded `CIVS_DIR` is
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations`, so the symlink
  target must be the repo's `cellular-first-design` dir, *not* its `code/civilizations`
  dir. Verified by **inode identity** (`129:3671` both sides) and `os.path.samefile()`.
- **`mkdir -p` THE PARENT ONLY, THEN `ln -sfn` ON THE FINAL PATH.** `mkdir -p` on the
  full path creates a real directory and nests the link inside it.
- `ZAI_TOKEN` is **absent** from the env (**71st session**); z.ai returns **401 `token
  expired or incorrect`** ⇒ the endpoint is healthy and the **credential** is missing.
  `ZAI_URL_OVERRIDE` alone is dead code behind the token gate, so **both** a placeholder
  `ZAI_TOKEN` and the override were set.
- `JEV_KEY` reads `TYPESAFEAI_KEY` but the env var is `TYPESAFE_AI_TOKEN` ⇒ the alias was
  exported. JEV returned HTTP 200 `{"model":"jev-1.14.0"}`; **0 fallback triples**.
- **Background launch needs `setsid nohup … < /dev/null &` inside a script file, not an
  inline subshell.** The mock was launched from `/tmp/start_mock.sh` and the port was
  probed **after** the launch call returned. **A mock that dies silently looks exactly
  like a mock that was never started.**
- The `write` tool cannot write to `/tmp`; bash heredocs are the working path for every
  artifact outside the workspace.
- Teardown: mock pids killed by exact argv match, 0 remaining procs, `curl` exit **7**
  (port closed).

## Mock rebuild — the eight fixes, and the band that caught the build again

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

**The response-body length band took FOUR builds this session** (506-537 → 468-483 →
437-468 → 396-411 → 348-363). The band is not cosmetic: a body longer than ~369
characters pushes the **seed prefix out of the 200-char `content_preview` truncation**,
which would silently break the seed+color+figure recompute check for every row.

**THE BAND IS SOLVABLE BY ARITHMETIC, NOT BY GUESSING.** The tenet list and the voice
phrase are variable-length, so the *fixed* prose must be sized against the **worst-case**
civilization. This session: variable parts (seed/color/figure prefix + first tenet +
voice emphasis) ranged **87-102** chars, so the fixed prose had to be **exactly 267**
chars for every civ to land inside 332-369 simultaneously (worst case 267+102=369,
best case 267+87=354). **Compute the fixed-prose budget from the measured variable
range; do not trim the template by hand until it "looks right."** Sizing the prose from
the measured worst case turns a four-build hunt into one build.

**Pre-flight passed 14/14 on the final build.** The gate reads the **real**
`culture.json` files rather than a hand-typed fixture, and includes the
**repeat-same-message determinism probe** (40 messages × 2 repeats) that a
distinctness-only gate can never certify.

## Lifetime leaderboard (after session 197)

| civ | relevance | rel/sim | wins | losses | win_rate | gen |
|---|---|---|---|---|---|---|
| civ-poetic | 2227.11 | 1.586 | 6 | 692 | 0.009 | 1 |
| civ-precise | 2070.86 | 1.484 | 455 | 238 | 0.657 | 1 |
| civ-whimsical | 1923.03 | 1.363 | 5 | 693 | 0.007 | 1 |
| civ-mythic | 1790.28 | 1.280 | 10 | 682 | 0.014 | 1 |
| civ-formal | 1761.47 | 1.254 | 98 | 598 | 0.141 | 1 |
| civ-engineer | 1674.65 | 1.201 | 49 | 642 | 0.071 | 1 |
| civ-therapist | 1623.15 | 1.162 | 11 | 684 | 0.016 | 1 |
| civ-grounded | 1490.66 | 1.051 | 70 | 627 | 0.100 | 1 |

## Run-level (this run's 10 new rows per civ)

| rank | civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| 1 | civ-poetic | 2.2940 | 1.5670 | 2.2640 | 3.0510 |
| 2 | civ-formal | 2.2050 | 1.3300 | 2.1580 | 3.1270 |
| 3 | civ-precise | 2.1460 | 1.2070 | 2.1830 | 3.0480 |
| 4 | civ-engineer | 2.0903 | 1.2600 | 2.0780 | 2.9330 |
| 5 | civ-whimsical | 2.0810 | 1.1020 | 2.4510 | 2.6900 |
| 6 | civ-grounded | 2.0420 | 1.1610 | 2.1800 | 2.7850 |
| 7 | civ-mythic | 2.0180 | 1.2610 | 2.1880 | 2.6050 |
| 8 | civ-therapist | 1.9480 | 1.2180 | 2.2600 | 2.3660 |

Cross-civ spreads: `alignment` **0.7610** › `quality` **0.4650** › `novelty` **0.3730** ›
`avg_score` **0.3460**.

## Low-relevance civilizations (as asked)

- **`civ-grounded` — the lifetime low, 69th consecutive session.** `relevance` **1490.66**
  (last of 8), `relevance_per_sim` **1.051** (the lowest in the fleet). In this run it was
  **6th of 8** on `avg_score` **2.0420**, with `quality` **1.1610** (2nd-lowest) and
  `alignment` **2.7850** (3rd-lowest). Lifetime `win_rate` **0.100** is **3rd-best in the
  fleet**, so it is *not* the least-selected civ: **selection and relevance are separate
  axes**. No extinction risk (**149x** the −10 floor).
- **`civ-therapist` — the run-level low for this run** (16th different civ in 16
  sessions). `avg_score` **1.9480**, `alignment` **2.3660** (lowest), `quality`
  **1.2180** (4th-lowest), novelty **2.2600**. Lifetime `relevance` **1623.15** (7th of
  8) — so it is *both* a run-level and a near-lifetime low, and its low axis is
  **alignment**.
- **`civ-whimsical` is the run-level quality low** (quality **1.1020**, fleet-low) with
  the run's **highest novelty** (**2.4510**) — the classic high-novelty/low-quality
  mis-fit, and the mirror image of `civ-therapist`.
- **`civ-mythic`** sits 7th of 8 on `avg_score` (**2.0180**) with the run's **lowest
  novelty** (**2.0780**) — a run-level low on novelty only, and the third distinct
  signature in the fleet.

## Chooser vs argmax

| prompt | winner | argmax | argmax score | winner score | direction |
|---|---|---|---|---|---|
| Write 100 words on what a cell is. | civ-precise | civ-poetic | 2.260 | 2.093 | DOWN |
| Write 100 words on the bookkeeper's role. | civ-precise | civ-poetic | 2.393 | 2.260 | DOWN |
| Write 100 words on the witness log. | civ-precise | civ-precise | 2.613 | 2.613 | agree |
| Write 100 words on ternary values. | civ-precise | civ-formal | 2.227 | 2.117 | DOWN |
| Write 100 words on JEV as a decision oracle. | civ-precise | civ-poetic | 2.200 | 1.900 | DOWN |

Agreement **1/5 (20 %)**; down-grade disagreements **4**, up-grade **0**.
**The down-grade streak is now 16 — re-base it to 16.**

`civ-poetic` was the `avg_score` argmax on **3 of 5** prompts and won **0 of 5**;
`civ-formal` was the argmax on **1 of 5** and won **0 of 5**; `civ-precise` was the argmax
on **1 of 5** and won **5 of 5**. The chooser is not selecting the higher-scoring
candidate, and the direction is consistently against it.

## Notes for the next session

1. **The path in the prompt never exists in a fresh workspace (17th occurrence)** — clone
   `SuperInstance/AI-Writings` to **`/tmp`** and symlink-bridge the **inner**
   `cellular-first-design` directory into `/workspace/repos/ai-writings/`. The NAS quota
   is on the *mount*, not the clone: a full clone into `/workspace` dies, the same clone
   into `/tmp` succeeds.
2. **The mock is not on disk at session start (`/tmp` wiped)** — rebuild from the
   algorithm block with all **seven** fixes **plus the OpenAI envelope**, and run the
   pre-flight (**14/14**) **before** the batch. **Size the fixed prose from the measured
   variable range** (target 267 this session) instead of trimming by hand; the band check
   is the one that fails on a fresh build.
3. **Do NOT count mock log lines against a fixed number.** Use the **multiset identity**
   instead: the last 80 OK-200 seeds must equal the 80 ledger rows' seeds. That proof
   is immune to how many times the pre-flight ran.
4. **Check semantic markers, not decorative prefix strings.** The literal
   `[mock-zai seed=` prefix check false-failed this session on a dataset that passed the
   independent seed+color+figure recompute 80/80.
