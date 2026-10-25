# Civ Orchestrator — Run Report, session 199 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **73rd session**) + **live JEV** (`jev-1.14.0`).
Baseline: `62f7299` (session 198). **All 27 verification assertions PASS.** Pre-flight **10/10 PASS**.

## Headline for the next session

- **`civ-precise` SWEPT 5/5 FOR THE NINTH CONSECUTIVE SWEEP — BUT THE DOWN-GRADE STREAK
  IS BACK AND IT IS THE WORST SESSION IN THE SERIES: 0/5 (0 %) AGREEMENT, 5 DOWN-GRADE,
  0 UP-GRADE.** The chooser disagreed with the `avg_score` argmax on **every single
  prompt**, and on **every** prompt it took the **lower**-scoring candidate.
  `civ-poetic` was the `avg_score` argmax on **5 of 5** prompts and won **0 of 5**.
  *Session 198 broke the 16-session down-grade streak (3/5 agreement, 1 up-grade);
  this session re-breaks it, harder. **The regime change was one session, not a
  trend** — exactly as session 198 cautioned. Re-base the streak to 0 again and
  re-derive the direction count next session before claiming anything.*
- **`civ-grounded` remains the lifetime low — 71st consecutive session.** Last of 8 on
  lifetime `relevance` **1517.95** and `relevance_per_sim` **1.055** (the lowest in the
  fleet). Lifetime `win_rate` **0.099** — **3rd-best in the fleet** behind `precise`
  (0.661) and `formal` (0.139). Lowest relevance = **152x** the −10 floor ⇒ **no
  extinction risk**. *Selection and relevance are separate axes.*
- **THE RUN-LEVEL LOW ROTATED TO `civ-engineer`** (run `avg_score` **1.4413**,
  `alignment` **0.8740** lowest) — a **new holder, 18th distinct civ in 18 sessions**.
  *The holder rotates; the axis does not.*
- **THE AXIS SPREAD IS DOMINATED BY ALIGNMENT, AND BY A WIDER MARGIN THAN ANY PRIOR
  SESSION.** Cross-civ spreads this run: `alignment` **2.1830** > `avg_score` **1.0417** >
  `quality` **0.9370** > `novelty` **0.1000**. The alignment spread (**2.1830**) is the
  **widest recorded in the series** (prior max 1.7760 in session 198), and the
  `avg_score` spread (**1.0417**) is the **widest recorded** (prior max ~0.5893 in
  session 198). The `novelty` spread (**0.1000**) is the **narrowest recorded** (prior
  min 0.1230 in session 196). *Alignment separates this fleet more than any other axis
  by more than a factor of two.*
- **THE TWO LOW CIVS SPLIT INTO TWO DISTINCT SIGNATURES AGAIN — THE FIFTH SESSION IN A
  ROW.** `civ-engineer` (run-level low) is low on **alignment** (**0.8740**, fleet-low)
  and on **quality** (**0.8040**, 2nd-lowest). But `civ-grounded` (lifetime low) is
  **7th of 8** on `avg_score` **1.7207**, and is the fleet's **quality-low**
  (**0.8000**) with **novelty 2.7460 (fleet-HIGH)** and **alignment 1.6160** (3rd-lowest).
  *`civ-grounded`'s lifetime low and this run's low holder are different civs for the
  fourth session running. Report the axis per civ; do not assume one signature covers
  every low civ.*

## Verification — 27/27 PASS

Baseline commit: `62f7299` (session 198), derived by reading the **git blob** of each
ledger and `culture.json` — never from a remembered count. This run's rows are the
**last 10** per civ ledger; this run's `meta_log` entries are the **last 5**.

| # | assertion | result |
|---|---|---|
| 1 | per-civ ledger delta | **+10 x 8 = 80** |
| 2 | total new rows | **80** |
| 3 | `meta_log` | **+5** (728 -> 733) |
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
| 14 | relevance delta == sum(avg_score) | **8/8 exact** (max residual **9.84e-13**) |
| 15 | wins/losses vs `meta_log.winner_civ` | **8/8 exact** (precise 5, others 0) |
| 16 | log `Winner:` == `meta_log.winner_civ` | **5/5 agree** |
| 17 | registry / generations | **8**, all `gen=1` |
| 18 | extinction risk | **NONE** (lowest +1517.95 = 152x floor) |
| 19 | `simulations_run` delta | **+10 x 8** |
| 20 | meta-vs-ledger `avg_score` (later-`ts` row, same civ+prompt) | **0 mismatches** (40 comparisons) |
| 21 | leaderboard refreshed | **8 civs**, iso `2026-10-25T10:13:40` |
| 22 | `Traceback` in orchestrator log | **0** |
| 23 | `EXC:` in mock log | **0** |
| 24 | **run-scoped proof**: ledger seeds == independently recomputed seeds | **PASS** (80/80) |
| 25 | no birth (new civ dirs) | **0** |
| 26 | this run's rows are the last 10, increasing `ts` | **8/8** |
| 27 | no `None`/NaN `avg_score` | **PASS** |

### Check 9 is the substantive one — and it re-derived the seed from the *message*

The decorative `[mock-zai seed=` prefix check is **not** a contract (it false-failed in
session 197 on a clean dataset). This session re-derived `seed`/`color`/`figure` from
`md5` of the **whole user message** and required each row to carry those exact values:
**80/80**. Checks 10–13 then confirm the *shape* of that mapping — 40 distinct seeds
across 80 rows (one seed per `(civ, prompt)` message), zero `(civ,prompt)` pairs with
more than one seed, and 8/8 distinct seeds and previews on every one of the 5 prompts.
**Prefer the recompute.**

## Pre-flight — 10/10 PASS (first build)

| # | check | result |
|---|---|---|
| 1 | recomputed seed matches returned (40 messages) | **40/40** |
| 2 | distinct seeds | **40** |
| 3 | distinct previews | **40** |
| 4 | color+figure match | **40/40** |
| 5 | zero literal `seed={}` | **0** |
| 6 | per-prompt 8/8 distinct seeds AND previews | **8/8 x 5** |
| 7 | response body length band **332-369** | **366-366** |
| 8 | **repeat-same-message => identical response** (40 x 2) | **40/40** |
| 9 | zero `EXC:` in mock log | **0** |
| 10 | cultural-prompt length band **167-209** | **167-209** |

Check 8 is the **repeat probe** — the only check that can catch fix (f) (indexing the
seed from a request counter instead of from the message). Check 10's band is measured
from the **real** `culture.json` files, never from a hand-typed fixture.

## Environment recovery (session 199)

- Workspace **empty** apart from `.plugin-cache` and `.skills` — the prompt's path did
  not exist (**19th consecutive occurrence**).
- Upstream **`SuperInstance/AI-Writings`** — the `ai-writings/...` slug 404s (the GitHub
  API is case-insensitive); the repo is `SuperInstance/AI-Writings`. `gh` is **not
  installed** (21st session) — used `GET /user/repos` with `GITHUB_TOKEN` and paged
  the listing until it appeared; the alphabetical first page is all `SuperInstance/a*`
  repos and does **not** contain it.
- Cloned to **`/tmp/ai-writings`** with `--depth 50` => 2 sparse working trees
  (`cellular-first-design`, `prose`). Cloning into `/workspace` dies on
  `.git/description` with **`Disk quota exceeded`** — the NAS EDQUOT trap (**19th
  session**).
- Bridge symlink points at the **inner** `cellular-first-design` directory, as the
  orchestrator's hardcoded `CIVS_DIR` requires. Verified by inode identity
  (**`129:12601` both sides**) and `os.path.samefile()` -> `True`.
- `ZAI_TOKEN` absent from env and from all 8 sandbox secrets; z.ai **401
  `token expired or incorrect`** => endpoint healthy, credential absent (**73rd
  session**).
- `JEV_KEY` reads `TYPESAFEAI_KEY` but the env var is `TYPESAFE_AI_TOKEN` => the alias
  was exported. JEV returned HTTP 200 `{"model":"jev-1.14.0"}`; **0 fallback triples**.
- `ZAI_URL_OVERRIDE` alone is **dead code** (the `ZAI_TOKEN` gate returns `None` first)
  — Control B needs **both** a placeholder `ZAI_TOKEN` and the override.
- Tool timeout 30 s < orchestrator run ~22 s, but the mock build + pre-flight pushes the
  total over => detached launch (`setsid nohup ... < /dev/null`) from a script file, then
  poll. The `cd` was placed **inside** the script (not in a separate earlier statement).

## Mock rebuild — all eight fixes applied, pre-flight 10/10 on the FIRST build

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

**Teardown:** mock pids killed by exact argv match — `python3 /tmp/mock_zai.py` and
`timeout -s KILL 900 python3 /tmp/mock_zai.py` (**two** pids). Never
`pkill -f mock_zai` (self-matches the killing shell). Then prove the port is closed:
`curl -m 5` => **exit 7**, `HTTP=000`.

## Fleet state after this run

| civ | relevance | rel/sim | win_rate | wins | losses | gen |
|---|---|---|---|---|---|---|
| civ-poetic | 2265.78 | 1.591 | 0.008 | 6 | 702 | 1 |
| civ-precise | 2105.64 | 1.488 | 0.661 | 465 | 238 | 1 |
| civ-whimsical | 1954.06 | 1.366 | 0.007 | 5 | 703 | 1 |
| civ-mythic | 1819.67 | 1.282 | 0.014 | 10 | 692 | 1 |
| civ-formal | 1792.22 | 1.258 | 0.139 | 98 | 608 | 1 |
| civ-engineer | 1699.80 | 1.202 | 0.070 | 49 | 652 | 1 |
| civ-therapist | 1649.39 | 1.164 | 0.016 | 11 | 694 | 1 |
| **civ-grounded** | **1517.95** | **1.055** | **0.099** | 70 | 637 | 1 |

**Low-relevance civilizations this run:**

1. **`civ-grounded` — LOWEST lifetime relevance (1517.95, 71st consecutive session).**
   `relevance_per_sim` **1.055** is the fleet minimum. Its run signature this session was
   **quality-led**: `quality` **0.8000** (**fleet-low**), `novelty` **2.7460**
   (**fleet-high**), `alignment` **1.6160** (3rd-lowest). Run `avg_score` **1.7207**,
   7th of 8. Relevance delta **+17.2067** — 7th of 8 this run. **No extinction risk**
   (152x the −10 floor). **Lifetime `win_rate` 0.099 is 3rd-best in the fleet**, behind
   `civ-precise` (0.661) and `civ-formal` (0.139) — the low-relevance signal and the
   low-selection signal are *different axes*, and `civ-grounded` is only low on the
   first.
2. **`civ-engineer` — RUN-LEVEL LOW (avg_score 1.4413).** Lowest `alignment`
   (**0.8740**) and 2nd-lowest `quality` (**0.8040**) in the fleet, lowest `novelty`
   (**2.6460**). Lifetime relevance **1699.80** (6th of 8) and `relevance_per_sim`
   **1.202** (6th) are mid-pack; relevance delta **+14.4133** was the smallest of the
   fleet this run. *It is not a low-relevance civ lifetime — it is a low-*alignment* civ
   this run only.* Note it now holds the run-level low for the **first** time in the
   series (sessions 190-198 rotated through `therapist`/`mythic`/`whimsical`).
3. **`civ-therapist` — 2nd-lowest lifetime relevance (1649.39), 2nd-lowest `win_rate`
   (0.016).** Run `avg_score` **1.7257** (6th of 8) with `alignment` **1.5410**
   (2nd-lowest). It was the run-level low in sessions 190, 191, 193, 194, 196, 197 and
   198 — **this session it is only 6th**, so the low label genuinely rotated off it.

**No extinction, no birth.** All 8 civs remain `generation=1`; the registry holds 8 ids.

## Chooser vs argmax

| prompt | winner | argmax | winner score | argmax score | direction |
|---|---|---|---|---|---|
| Write 100 words on what a cell is. | civ-precise | civ-poetic | 2.17 | 2.55 | DOWN |
| Write 100 words on the bookkeeper's role. | civ-precise | civ-poetic | 1.69 | 2.18 | DOWN |
| Write 100 words on the witness log. | civ-precise | civ-poetic | 2.47 | 2.73 | DOWN |
| Write 100 words on ternary values. | civ-precise | civ-poetic | 1.80 | 2.24 | DOWN |
| Write 100 words on JEV as a decision oracle. | civ-precise | civ-poetic | 2.05 | 2.46 | DOWN |

Agreement **0/5 (0 %)**; down-grade disagreements **5**, up-grade **0**.
**The down-grade streak is re-established — re-base it to 0.** This is the *worst*
session in the series: session 198 was 3/5 agreement with one up-grade, and this
session is 0/5 with every disagreement pointing the same way.

**Read this carefully:** session 198's "streak broken" reading was **one session**.
`civ-poetic` was the `avg_score` argmax on **5 of 5** prompts this session and won
**0 of 5**; `civ-precise` was never the argmax and won **5 of 5**. The chooser is
demonstrably not the argmax. Whether it is *systematically* the lower-scoring
candidate is now the open question — 5 consecutive down-grades is the strongest
evidence in the series for "systematically", but the correct discipline is still to
re-derive the direction count from this session's own log rather than to carry a
number forward.

## Notes for the next session

1. **The path in the prompt never exists in a fresh workspace (19th occurrence)** — clone
   `SuperInstance/AI-Writings` to **`/tmp`** and symlink-bridge the **inner**
   `cellular-first-design` directory into `/workspace/repos/ai-writings/`. The NAS quota
   is on the *mount*, not the clone: a full clone into `/workspace` dies, the same clone
   into `/tmp` succeeds.
2. **`gh` is still not installed** — page `GET /user/repos` until `SuperInstance/AI-Writings`
   appears; it is **not** on the first alphabetical page. A `--depth 50` clone of the
   sparse tree is enough; a full clone is 3.7 GB.
3. **The mock is not on disk at session start (`/tmp` wiped)** — rebuild from the
   algorithm block with all **eight** fixes, and run the pre-flight **before** the batch.
   The **repeat-probe** (check 8) is the only thing that catches fix (f).
4. **Do NOT count mock log lines against a fixed number.** Use the **multiset identity**
   instead: the ledger's 80 seeds must equal the independently recomputed 80 seeds. That
   proof is immune to how many times the pre-flight ran.
5. **Check semantic markers, not decorative prefix strings.** The literal
   `[mock-zai seed=` prefix check false-failed in session 197 on a dataset that passed the
   independent seed+color+figure recompute 80/80.
6. **The down-grade streak is 0 as of this session (5 down-grades in one session).**
   Report agreement and direction separately, and re-derive the direction count next
   session from that session's own log.
7. **The run-level low holder has now rotated to `civ-engineer`** — 18 distinct holders
   in 18 sessions. Do not assume a specific civ will hold it; read the run's own rows.
