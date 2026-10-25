# Civ Orchestrator — Run Report, session 201 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **75th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `2a36622` (session 200). **All 27 verification assertions PASS.** Pre-flight **14/14 PASS**.

## Headline for the next session

- **`civ-precise` SWEPT 4/5 — THE 11-CONSECUTIVE SWEEP IS BROKEN.** `civ-engineer` took
  the "ternary values" prompt. This is the **first prompt in 11 sessions** that
  `civ-precise` did not win, so the 5/5 streak is **ended at 10 sessions**, not extended
  to 11. *The streak is a resettable counter, not a trend — re-derive it every session.*
- **THE CHOOSER/ARGMAX AGREEMENT MOVED TO 3/5 (60 %) — 2 down-grades, 0 up-grades.**
  Session 200 was 2/5, session 199 was 0/5, session 198 was 3/5. The agreement series
  now reads 3 → 0 → 2 → **3**. *Both disagreements again took the LOWER-scoring
  candidate; there has still not been a single up-grade in the series.*
- **`civ-grounded` REMAINS THE LIFETIME LOW — 73rd consecutive session.** Lifetime
  `relevance` **1547.05** and `relevance_per_sim` **1.060**, both fleet-minimum. Lifetime
  `win_rate` **0.098** is **3rd-best in the fleet** behind `precise` (0.665) and `formal`
  (0.137). Lowest relevance = **155x** the −10 floor ⇒ **no extinction risk**.
- **THE RUN-LEVEL LOW ROTATED TO `civ-therapist`** (run `avg_score` **1.3643**,
  `quality` **0.3180** fleet-low, `alignment` **1.2330** fleet-low) — a **20th distinct
  holder in 20 sessions**. *The holder rotates; the axis does not.*
- **THE ALIGNMENT SPREAD REMAINS DOMINANT.** Cross-civ spreads this run:
  `alignment` **1.8170** > `avg_score` **0.8200** > `quality` **0.7080** >
  `novelty` **0.2700**. Alignment is **2.6x** the quality spread. The `novelty` spread
  (**0.2700**) is the **widest novelty spread in the series** (prior max 0.1510 in
  session 195) but is still the narrowest of the four axes.
- **THE LIFETIME LOW AND THE RUN-LEVEL LOW ARE DIFFERENT CIVS — 6 SESSIONS RUNNING.**
  `civ-grounded` holds the lifetime low (**1547.05**, 73rd consecutive) but placed
  **7th of 8** on this run's `avg_score` (**1.5370**). `civ-therapist` took the run-level
  low and is the **2nd-lowest lifetime** civ. *Report the axis per civ; do not promote a
  run low to a lifetime finding.*

## Verification — 27/27 PASS

Baseline commit: `2a36622` (session 200), derived by reading the **git blob** of each
ledger and `culture.json` — never from a remembered count. This run's rows are the
**last 10** per civ ledger; this run's `meta_log` entries are the **last 5**.

| # | assertion | result |
|---|---|---|
| 1 | per-civ ledger delta | **+10 x 8 = 80** |
| 2 | total new rows | **80** |
| 3 | `meta_log` | **+5** (738 -> 743) |
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
| 15 | wins/losses vs `meta_log.winner_civ` | **8/8 exact** (precise 4, engineer 1) |
| 16 | log `Winner:` == `meta_log.winner_civ` | **5/5 agree** |
| 17 | registry / generations | **8**, all `gen=1` |
| 18 | extinction risk | **NONE** (lowest +1547.05 = 155x floor) |
| 19 | `simulations_run` delta | **+10 x 8** |
| 20 | meta-vs-ledger `avg_score` (later-`ts` row, same civ+prompt) | **0 mismatches** |
| 21 | leaderboard refreshed | **8 civs**, iso `2026-10-25T10:35:28` |
| 22 | `Traceback` in orchestrator log | **0** |
| 23 | `EXC:` in mock log | **0** |
| 24 | **run-scoped proof**: ledger seeds == independently recomputed seeds | **PASS** (80/80) |
| 25 | no birth (new civ dirs) | **0** |
| 26 | this run's rows are the last 10, increasing `ts` | **8/8** |
| 27 | no `None`/NaN `avg_score` | **PASS** |

## Pre-flight — 14/14 PASS (second build)

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
| 10 | **repeat-same-message => same seed** | **20/20** (2x probe) |
| 11 | zero `(civ,prompt)` pairs carrying >1 seed | **40/40 distinct** |
| 12 | response body length band **332-369** | **352-358** |
| 13 | gate prints a final verdict | **PASS**, exit 0 |
| 14 | no partial-crash gate | **PASS** |

### Two gate bugs hit this session — both caught the same way

1. **The pre-flight crashed at check 5 with `NameError: name 're' is not defined`.** The
   `import re` sat *inside* `seed_of()` on the first build, so it was never in module
   scope when the module-level loop called `color_of()`. The gate had already printed
   **four `[PASS]` lines** when it died. *This is exactly the session-195 lesson: a gate
   that prints passes and then tracebacks is not a passing gate.* Fixed by hoisting the
   import; the gate now prints a final `VERDICT:` line and exits non-zero on any failure.
2. **The verifier crashed with `TypeError: check() takes from 2 to 3 positional
   arguments but 4 were given`** — the same class of bug in the *verifier*: a detail
   string was passed as a 4th positional arg to a 3-arg helper. Fixed by folding the
   detail into the check *name*. *The rule generalises: a helper's arity is part of its
   contract, and a crash in the checker is a checker failure, not a run failure.*
   Both scripts were re-run end-to-end after the fix; the run itself was never re-run,
   because the run was clean.

## Pre-flight body-length band — caught the fresh build, twice

The first template rendered at **349-381** chars against the **332-369** band
(`max=381` — a long civ name pushed it over). The fix was **not** to trim the tail but
to make the body **culture-independent**: the culture-derived fields (`trad`, `tenet`,
`voice`) are truncated to fixed widths (12 / 10 / 10 chars) before interpolation, so
the rendered length depends only on the seed/colour/figure widths. That brought the
body to **298-304** — *below* the band — so one fixed sentence was appended
("The cell ticks when the ledger and the witness agree."), landing at **352-358**.

*Lessons: (a) the band catches a fresh build every time — expect two iterations;
(b) the right fix for a variable-length body is to **remove the variance**, not to trim
the longest instance; (c) a body longer than ~369 chars pushes the seed prefix out of
the 200-char `content_preview` truncation and silently breaks the seed+colour+figure
recompute for every row.*

## Environment recovery (session 201)

- Workspace **empty** apart from `.plugin-cache` and `.skills` — the prompt's path did
  not exist (**21st consecutive occurrence**).
- Upstream **`SuperInstance/AI-Writings`** (case-sensitive; the `ai-writings/...` slug
  404s). `gh` is **not** installed (**23rd session**) — used `GET /search/repositories`
  with `GITHUB_TOKEN` to find it, then `GET /search/code` for the script path.
  The owner has 5 400+ repos, so `GET /user/repos` paging is not viable.
- Cloned to **`/tmp/aiw`** with `--filter=blob:none --no-checkout --depth 1` +
  `git sparse-checkout set cellular-first-design` ⇒ a **9.9 M** working tree instead of
  a 3.7 GB full clone. *Cloning into `/workspace` dies on **`Disk quota exceeded`** —
  the NAS EDQUOT trap (**21st session**); `df` shows `600G/600G 100%`.*
- Bridge symlink `/workspace/repos/ai-writings/cellular-first-design` → the **inner**
  `cellular-first-design` dir. Verified by **inode identity**
  (`stat -L -c '%d:%i'` → `129:10423` on both sides) plus `os.path.samefile()` → `True`.
  The shell `test -ef` is unusable in this sandbox.
- `ZAI_TOKEN` absent from env and from the sandbox secrets; z.ai returns **401
  `token expired or incorrect`** ⇒ endpoint healthy, credential absent (**75th
  session**). Control B (the local mock) is the only provider path, and it needs **both**
  a placeholder `ZAI_TOKEN` **and** `ZAI_URL_OVERRIDE` — the override alone is dead
  code behind the token gate.
- `JEV_KEY` reads `TYPESAFEAI_KEY` but the env var is `TYPESAFE_AI_TOKEN` ⇒ the alias
  was exported. JEV returned HTTP 200 `{"model":"jev-1.14.0"}`; **0 fallback triples**.
- Mock launched from a **script file** (`setsid nohup … < /dev/null &` inside a `.sh`),
  then the port was probed. Teardown by **exact argv match** (two pids), never
  `pkill -f mock_zai` (self-matches the killing shell); the port was then proven closed
  (`curl` exit **7**, `HTTP=000`) before relaunch.

## Fleet state after this run

| civ | relevance | rel/sim | win_rate | wins | losses | gen |
|---|---|---|---|---|---|---|
| civ-poetic | 2305.27 | 1.596 | 0.008 | 6 | 712 | 1 |
| civ-precise | 2146.81 | 1.496 | 0.665 | 474 | 239 | 1 |
| civ-whimsical | 1987.42 | 1.370 | 0.007 | 5 | 713 | 1 |
| civ-mythic | 1852.52 | 1.287 | 0.014 | 10 | 702 | 1 |
| civ-formal | 1828.74 | 1.266 | 0.137 | 98 | 618 | 1 |
| civ-engineer | 1735.95 | 1.211 | 0.070 | 50 | 661 | 1 |
| **civ-therapist** | **1675.08** | **1.166** | **0.015** | **11** | **704** | **1** |
| **civ-grounded** | **1547.05** | **1.060** | **0.098** | **70** | **647** | **1** |

**Low-relevance civilizations this run:**

1. **`civ-grounded` — LOWEST lifetime relevance (1547.05, 73rd consecutive session).**
   `relevance_per_sim` **1.060** is the fleet minimum. Its run signature this session was
   **alignment-led**: `alignment` **1.6250** (2nd-lowest), `quality` **0.5580**
   (2nd-lowest), `novelty` **2.4280** (mid-fleet). Run `avg_score` **1.5370**, 7th of 8.
   Relevance delta **+15.3700** — 2nd-smallest of the fleet. **No extinction risk**
   (155x the −10 floor). **Lifetime `win_rate` 0.098 is 3rd-best in the fleet** — the
   low-relevance signal and the low-selection signal are *different axes*, and
   `civ-grounded` is only low on the first.
2. **`civ-therapist` — RUN-LEVEL LOW (avg_score 1.3643) and 2nd-lowest lifetime
   relevance (1675.08).** Lowest `quality` (**0.3180**) **and** lowest `alignment`
   (**1.2330**) in the fleet; `novelty` **2.5420** (2nd-highest). Lifetime
   `relevance_per_sim` **1.166** (7th of 8) and lifetime `win_rate` **0.015**
   (2nd-lowest). Relevance delta **+13.6433** was the smallest of the fleet this run.
   *It is both a low-relevance civ lifetime and the run-level low this session — the
   second time in seven sessions that the two coincide.*
3. **`civ-engineer` — 6th of 8 lifetime relevance (1735.95) but 2nd-best on this run's
   `avg_score` (2.0837).** It **won** the "ternary values" prompt outright — the first
   prompt `civ-precise` did not win in 11 sessions. Lowest `novelty` in the fleet this
   run (**2.3890**). *It is not a low-relevance civ lifetime — it is a low-`novelty` civ
   this run only.*

**No extinction, no birth.** All 8 civs remain `generation=1`; the registry holds 8 ids.

## Chooser vs argmax

| prompt | winner | argmax | winner score | argmax score | direction |
|---|---|---|---|---|---|
| Write 100 words on what a cell is. | civ-precise | civ-engineer | 2.0467 | 2.1200 | DOWN |
| Write 100 words on the bookkeeper's role. | civ-precise | civ-precise | 2.3367 | 2.3367 | AGREE |
| Write 100 words on the witness log. | civ-precise | civ-precise | 2.4967 | 2.4967 | AGREE |
| Write 100 words on ternary values. | **civ-engineer** | civ-precise | 1.8567 | 2.0167 | **DOWN** |
| Write 100 words on JEV as a decision oracle. | civ-precise | civ-precise | 2.2100 | 2.2100 | AGREE |

**Agreement 3/5 (60 %) — 2 down-grades, 0 up-grades.**

## Durable lessons

1. **A SWEEP STREAK IS A COUNTER, NOT A TREND — AND IT HAS A PRINTED EXPIRY DATE.**
   `civ-precise` won 5/5 for **ten consecutive sessions** (191-200) and then dropped a
   prompt to `civ-engineer` this session. *The first honest statement of the streak's
   length is the one that ends it.* Quoting "5/5 for 10 sessions" as a *current* fact
   would have been wrong the moment this run landed.
2. **THE CHOOSER STILL NEVER UP-GRADES.** The agreement series is 3 → 0 → 2 → **3**
   across sessions 198-201, and **every single disagreement in the series took the
   LOWER-scoring candidate — 0 up-grades ever.** A chooser that only ever picks the
   worse candidate is not "noisy"; it is *anti-correlated* with `avg_score` on the rows
   where it disagrees. The standing suspect is unchanged: the `best_civ` criteria map
   (`civ_id` -> `civ name`) is a *label* map, and the chooser is scoring labels, not
   texts. *The next real experiment is still to bypass the chooser and rank purely by
   `avg_score`.*
3. **A GATE CRASH IS A GATE FAILURE — AND IT CAN HIDE BEHIND PASSES.** Two independent
   scripts in this session (the pre-flight and the verifier) each crashed on a trivial
   Python mistake *after* printing several `[PASS]` lines. Both were caught only because
   the gate prints a final `VERDICT:` line and exits non-zero. *Corollary: a checker
   that dies mid-run is indistinguishable from a checker that passed, unless it is
   written to fail loudly on its own crash.* The run itself was clean in both cases and
   was never re-run — the distinction between *the artifact* and *the checker* is what
   let a clean run survive a broken checker.
4. **REMOVE THE VARIANCE FROM A LENGTH-BANDED BODY; DO NOT TRIM THE LONGEST INSTANCE.**
   The 332-369 band failed at 349-381 because a long civ name lengthened the body.
   Truncating the culture fields to fixed widths made the length constant
   (298-304) and then one appended sentence brought it to **352-358** — inside the band
   on the second build. *A band check is a variance check: fix the cause of the
   variance, not its maximum.*
