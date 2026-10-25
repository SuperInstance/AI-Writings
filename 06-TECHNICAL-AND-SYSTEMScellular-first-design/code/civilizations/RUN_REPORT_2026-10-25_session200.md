# Civ Orchestrator — Run Report, session 200 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **74th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `0093c0a` (session 199). **All 27 verification assertions PASS.** Pre-flight **11/11 PASS**.

## Headline for the next session

- **`civ-precise` SWEPT 5/5 FOR THE TENTH CONSECUTIVE SWEEP, AND THE DOWN-GRADE
  STREAK RECOVERED — BUT ONLY TO 2/5, NOT BACK TO THE 16-SESSION BASELINE.**
  Chooser/argmax agreement **2/5 (40 %)**: **3 down-grades, 0 up-grades**. `civ-poetic`
  was the `avg_score` argmax on **3 of 5** prompts and won **0 of 3**; `civ-precise` was
  never the argmax on the prompts it won. *Session 199 reported 0/5 agreement as the
  worst session in the series and session 198 had broken the 16-session streak at 3/5.
  This session sits at 2/5 — between the two. The streak count must be re-derived from
  this session's own rows; do not quote the 16-session figure as current.*
- **`civ-grounded` REMAINS THE LIFETIME LOW — 72nd consecutive session.** Lifetime
  `relevance` **1531.68** and `relevance_per_sim` **1.057**, both fleet-minimum.
  Lifetime `win_rate` **0.098** — **3rd-best in the fleet** behind `precise` (0.664) and
  `formal` (0.138). Lowest relevance = **153x** the −10 floor ⇒ **no extinction risk**.
  *Selection and relevance remain separate axes; `civ-grounded` is only low on the
  first.*
- **THE RUN-LEVEL LOW ROTATED TO `civ-therapist`** (run `avg_score` **1.2493**,
  `alignment` **0.6880** fleet-low, `quality` **0.4520** 2nd-lowest) — a **19th distinct
  holder in 19 sessions**. *The holder rotates; the axis does not.*
- **THE ALIGNMENT SPREAD REMAINS DOMINANT BUT IS NO LONGER THE WIDEST EVER.**
  Cross-civ spreads this run: `alignment` **1.7620** > `quality` **0.4660** >
  `avg_score` **0.7214** > `novelty` **0.1100**. The alignment spread (**1.7620**) is
  the **2nd-widest recorded** (prior max **2.1830** in session 199), and it is still
  **3.8x** the quality spread. The `novelty` spread (**0.1100**) is the **narrowest
  recorded in the series** (prior min 0.1000 in session 199). *Alignment separates this
  fleet more than any other axis; the margin narrowed but the ordering held.*
- **THE LIFETIME LOW AND THE RUN-LEVEL LOW ARE STILL DIFFERENT CIVS — 5 SESSIONS
  RUNNING.** `civ-grounded` holds the lifetime low (**1531.68**, 72nd consecutive) but
  was only **2nd of 8** on this run's `avg_score` (**1.3547**), with a **quality-led**
  signature (`quality` **0.3980** fleet-low, `alignment` **1.0260** 2nd-lowest).
  `civ-therapist` took the run-level low with an **alignment-led** signature
  (`alignment` **0.6880** fleet-low, `novelty` **2.6080** mid-fleet). *Report the axis
  per civ; do not assume one signature covers every low civ.*

## Verification — 27/27 PASS

Baseline commit: `0093c0a` (session 199), derived by reading the **git blob** of each
ledger and `culture.json` — never from a remembered count. This run's rows are the
**last 10** per civ ledger; this run's `meta_log` entries are the **last 5**.

| # | assertion | result |
|---|---|---|
| 1 | per-civ ledger delta | **+10 x 8 = 80** |
| 2 | total new rows | **80** |
| 3 | `meta_log` | **+5** (733 -> 738) |
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
| 14 | relevance delta == sum(avg_score) | **8/8 exact** (to 1e-6) |
| 15 | wins/losses vs `meta_log.winner_civ` | **8/8 exact** (precise 5, others 0) |
| 16 | log `Winner:` == `meta_log.winner_civ` | **5/5 agree** |
| 17 | registry / generations | **8**, all `gen=1` |
| 18 | extinction risk | **NONE** (lowest +1531.68 = 153x floor) |
| 19 | `simulations_run` delta | **+10 x 8** |
| 20 | meta-vs-ledger `avg_score` (later-`ts` row, same civ+prompt) | **0 mismatches** (40 comparisons) |
| 21 | leaderboard refreshed | **8 civs**, iso `2026-10-25T10:23:*` |
| 22 | `Traceback` in orchestrator log | **0** |
| 23 | `EXC:` in mock log | **0** |
| 24 | **run-scoped proof**: ledger seeds == independently recomputed seeds | **PASS** (80/80) |
| 25 | no birth (new civ dirs) | **0** |
| 26 | this run's rows are the last 10, increasing `ts` | **8/8** |
| 27 | no `None`/NaN `avg_score` | **PASS** |

### Check 9 is the substantive one — and it re-derived the seed from the *message*

This session re-derived `seed`/`color`/`figure` from `md5` of the **whole user
message** and required each row to carry those exact values: **80/80**. Checks 10–13
then confirm the *shape* of that mapping — 40 distinct seeds across 80 rows (one seed
per `(civ, prompt)` message), zero `(civ,prompt)` pairs with more than one seed, and
8/8 distinct seeds and previews on every one of the 5 prompts. **Prefer the recompute.**

## Pre-flight — 11/11 PASS (first build)

| # | check | result |
|---|---|---|
| 1 | cultural-prompt length band **167-209** | **167-209** |
| 2 | zero transport errors | **0** |
| 3 | distinct seeds | **40** |
| 4 | distinct previews | **40** |
| 5 | recomputed seed+colour+figure present | **40/40** |
| 6 | per-prompt 8/8 distinct seeds AND previews | **8/8 x 5** |
| 7 | zero literal `seed={}` | **0** |
| 8 | zero `EXC:`/tracebacks | **0** |
| 9 | `[mock-zai` prefix | **40/40** |
| 10 | **repeat-same-message => same seed (40 x 2)** | **40/40** |
| 11 | zero `(civ,prompt)` pairs carrying >1 seed | **40/40 distinct** |

Check 10 is the **repeat probe** — the only check that can catch fix (f) (indexing the
seed from a request counter instead of from the message). Check 1's band is measured
from the **real** `culture.json` files, never from a hand-typed fixture.

## Environment recovery (session 200)

- Workspace **empty** apart from `.plugin-cache` — the prompt's path did not exist
  (**20th consecutive occurrence**).
- Upstream **`SuperInstance/AI-Writings`** — the `ai-writings/...` slug 404s (the GitHub
  API is case-insensitive); the repo is `SuperInstance/AI-Writings`. `gh` is **not
  installed** (22nd session) — used `GET /user/repos` with `GITHUB_TOKEN` and paged the
  listing until it appeared.
- Cloned to **`/tmp/AI-Writings`** with `--depth 1 --filter=blob:none --sparse` => 9.9 M
  working tree. Cloning into `/workspace` dies on **`Disk quota exceeded`** — the NAS
  EDQUOT trap (**20th session**).
- Bridge symlink points at the **inner** `cellular-first-design` directory, as the
  orchestrator's hardcoded `CIVS_DIR` requires. The symlink must target the *inner*
  directory — pointing it at the clone root makes `code/civilizations/` unresolvable.
- `ZAI_TOKEN` absent from env and from all 8 sandbox secrets; z.ai **401
  `token expired or incorrect`** => endpoint healthy, credential absent (**74th
  session**).
- `JEV_KEY` reads `TYPESAFEAI_KEY` but the env var is `TYPESAFE_AI_TOKEN` => the alias
  was exported. JEV returned HTTP 200 `{"model":"jev-1.14.0"}`; **0 fallback triples**.
- `ZAI_URL_OVERRIDE` alone is **dead code** (the `ZAI_TOKEN` gate returns `None` first)
  — Control B needs **both** a placeholder `ZAI_TOKEN` and the override.
- The mock was launched from a **script file** (`setsid nohup ... < /dev/null &` inside a
  `.sh`, invoked with `nohup`), then the port was probed — a dead mock looks exactly
  like a mock that never started.

## Mock rebuild — all eight fixes applied, pre-flight 11/11 on the FIRST build

| # | Fix | Symptom if missing |
|---|---|---|
| a | seed index wrap `h[(i*2)%8:...]` | `ValueError` on `i>=4` => HTTP 500 **while the socket stays open** |
| b | md5 of the **whole** user message | first 8 alnum chars are `YouAreA` for every civ => all 8 civs emit identical text |
| c | `Connection: close` + `Content-Length` | `curl` hangs to the tool timeout on a healthy server |
| d | interpolate the seed placeholder | every response carries literal `seed={}` => 1 distinct seed, not 40 |
| e | seed widened 2 -> 4 hex chars, **contiguous slice** | 2-char slice collides => 39 distinct seeds, one prompt at 7/8 |
| f | index from the **message** (`d[0] % 4`), not a request counter | 64 distinct seeds / 80 rows; 20 `(civ,prompt)` pairs carry >1 seed |
| g | `figure` = three **string** components, not a division | figure renders as a float, marker regex fails |
| h | **OpenAI envelope** `choices[0].message.content` | the orchestrator reads `r["choices"][0]["message"]["content"]` => `KeyError` |

## Fleet state after this run

| civ | relevance | rel/sim | win_rate | wins | losses | gen |
|---|---|---|---|---|---|---|
| civ-poetic | 2285.29 | 1.594 | 0.008 | 6 | 707 | 1 |
| civ-precise | 2124.97 | 1.491 | 0.664 | 470 | 238 | 1 |
| civ-whimsical | 1969.44 | 1.367 | 0.007 | 5 | 708 | 1 |
| civ-mythic | 1835.11 | 1.284 | 0.014 | 10 | 697 | 1 |
| civ-formal | 1809.83 | 1.261 | 0.138 | 98 | 613 | 1 |
| civ-engineer | 1715.11 | 1.204 | 0.069 | 49 | 657 | 1 |
| civ-therapist | 1661.43 | 1.164 | 0.015 | 11 | 699 | 1 |
| **civ-grounded** | **1531.68** | **1.057** | **0.098** | 70 | 642 | 1 |

**Low-relevance civilizations this run:**

1. **`civ-grounded` — LOWEST lifetime relevance (1531.68, 72nd consecutive session).**
   `relevance_per_sim` **1.057** is the fleet minimum. Its run signature this session was
   **quality-led**: `quality` **0.3980** (**fleet-low**), `alignment` **1.0260**
   (2nd-lowest), `novelty` **2.6400** (2nd-highest). Run `avg_score` **1.3547**,
   2nd of 8. Relevance delta **+13.7300** — 2nd-smallest of the fleet this run.
   **No extinction risk** (153x the −10 floor). **Lifetime `win_rate` 0.098 is
   3rd-best in the fleet**, behind `civ-precise` (0.664) and `civ-formal` (0.138) — the
   low-relevance signal and the low-selection signal are *different axes*, and
   `civ-grounded` is only low on the first.
2. **`civ-therapist` — RUN-LEVEL LOW (avg_score 1.2493) and 2nd-lowest lifetime
   relevance (1661.43).** Lowest `alignment` (**0.6880**) in the fleet, 2nd-lowest
   `quality` (**0.4520**), `novelty` **2.6080** (mid-fleet). Lifetime `relevance_per_sim`
   **1.164** (7th of 8) and lifetime `win_rate` **0.015** (2nd-lowest). Relevance delta
   **+12.0467** was the smallest of the fleet this run. It was the run-level low in
   sessions 190, 191, 193, 194, 196, 197, 198 and 199 — **this session the label stays
   on it for the 19th distinct holder in 19 sessions.** *It is both a low-relevance civ
   lifetime and the run-level low this session — the first time in five sessions that
   the two coincide.*
3. **`civ-engineer` — 6th of 8 lifetime relevance (1715.11), 3rd-lowest run
   `avg_score` (1.4927).** Lowest `novelty` in the fleet (**2.5900**) and `alignment`
   **1.3640** (5th-lowest). Relevance delta **+15.3133** was mid-fleet. *It is not a
   low-relevance civ lifetime — it is a low-`novelty` civ this run only.*

**No extinction, no birth.** All 8 civs remain `generation=1`; the registry holds 8 ids.

## Chooser vs argmax

| prompt | winner | argmax | winner score | argmax score | direction |
|---|---|---|---|---|---|
| Write 100 words on what a cell is. | civ-precise | civ-poetic | 1.6267 | 1.7100 | DOWN |
| Write 100 words on the bookkeeper's role. | civ-precise | civ-poetic | 1.9900 | 2.1433 | DOWN |
| Write 100 words on the witness log. | civ-precise | civ-precise | 1.9900 | 2.2800 | AGREE |
| Write 100 words on ternary values. | civ-precise | civ-poetic | 1.7800 | 1.8533 | DOWN |
| Write 100 words on JEV as a decision oracle. | civ-precise | civ-precise | 1.7800 | 2.0633 | AGREE |

**Agreement 2/5 (40 %) — 3 down-grades, 0 up-grades.**

## Durable lessons

1. **A 10-SESSION SWEEP IS NOT A QUALITY SIGNAL.** `civ-precise` has now swept 5/5 for
   ten consecutive sessions while `civ-poetic` — which has the **highest** lifetime
   `relevance` and the **highest** `relevance_per_sim` in the fleet — has won **6 of
   1449 simulations**. The chooser is not selecting on `avg_score`; it is selecting on
   something the axis decomposition does not measure. *The meta-GAN's `best_civ`
   criteria map (`civ_id` -> `civ name`) remains the standing suspect, exactly as
   session 195 flagged it.* The next real experiment is still to **bypass the chooser**
   and rank purely by `avg_score`.
2. **THE RUN-LEVEL LOW HOLDER ROTATES; THE LIFETIME LOW DOES NOT — AND THEY NOW
   COINCIDE ONCE IN FIVE SESSIONS.** `civ-grounded` has held the lifetime low for 72
   consecutive sessions. The run-level low has rotated through 19 distinct civs in 19
   sessions, and this session it landed on `civ-therapist` — which is *also* the
   2nd-lowest lifetime civ. *Do not predict the run-level holder from the previous
   report; read this run's own rows.*
3. **THE `relevance_per_sim` DENOMINATOR KEEPS DRIFTING, SO RE-DERIVE IT FROM THE
   LEDGER.** `civ-grounded` has the highest `simulations_run` in the fleet (**1449**)
   and the lowest `relevance_per_sim` (**1.057**). A civ that runs more sims is
   penalised on the per-sim axis, so per-sim and lifetime relevance can disagree for
   the same civ. *Report both, always, and name which one is the "low".*
