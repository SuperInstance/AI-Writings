# Civ Orchestrator — Run Report, session 205 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **78th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `f60b152` (session 203). **All 17 verification assertions PASS.** Pre-flight **15/15 PASS**.

> **Note on numbering.** This run was launched concurrently with an independent
> **session 204** (commit `39addc4`, authored by a different agent) from the **same**
> baseline `f60b152`. Both runs are valid and both are preserved. This report is filed
> as **session 205** so that neither overwrites the other; its own data, verdicts and
> counters are wholly independent of session 204's — the two runs share only a starting
> point, and the two sets of 80 ledger rows were produced by two different mock seeds
> and two different JEV draws.

**Session 205 in one line:** `civ-formal` took **3 of 5** prompts and `civ-precise` 2,
ending `civ-precise`'s four-session 5/5-sweep run; the chooser/argmax agreement fell to
**1/5 (20 %) — 4 down-grades, 0 up-grades**; the run-level low rotated to
`civ-whimsical` (run `avg_score` **1.0700**, `alignment` **0.4150** = lowest in the
fleet) while `civ-grounded` remains the **lifetime low for the 76th consecutive
session** — *the run low and the lifetime low are again different civs on different
axes*; and the alignment spread (**2.4550**) is **3.95x** the quality spread and
**16.70x** the novelty spread, so the ranking is produced almost entirely by
**alignment**.

**Three durable lessons from this session:**

1. **A GATE THAT PARSES THE SEED FROM THE WRONG BRACKET FAILS 40/40 AND STILL LOOKS
   LIKE A MOCK REGRESSION.** The mock's header is `[mock-zai <seed>] <color> <figure>.`
   — the seed sits **inside** the brackets. A parser that took `prev.split("]")[0][len("[mock-zai "):]`
   *before* the fix was correct only by accident for the seed, but the colour/figure
   parse used `split("]")[1]`, which yields `" <color> <figure>. <body>"` and needs a
   **second** split into two fields. The first attempt indexed `m.split(" ")[1]` and
   `[2]` on a string that had already been truncated to the seed, raising
   `IndexError` on **all 40** requests. The second attempt parsed the colour/figure
   correctly but read the **seed** from `split("]")[1]`, so the recompute compared
   `d372` against `6ffd` and reported **0/40 recomputed md5s** — a clean-looking
   "the mock is broken" story about a mock that was working perfectly.
   *Parse the header from a known-good sample first, then assert the recompute; a
   0/40 recompute means "the parser is wrong" before it means "the mock is wrong".*
2. **A GATE THAT PASSES 14 CHECKS AND FAILS THE 15TH IS WORKING.** The pre-flight
   reported `14/15 PASS` with a clean `VERDICT:` line and a non-zero exit, because the
   md5-recompute check was red. The run was never started on a red gate, and the
   checker bug — not the artifact — was the thing that needed fixing. *The final
   verdict line and the non-zero exit are what separate a gate from a log scraper.*
3. **THE DOWN-GRADE STREAK CONTINUES, AND THE CHOOSER HAS STILL NEVER UP-GRADED.** This
   session's agreement is **1/5 (20 %)**; across sessions 199-204 it reads
   0 → 2 → 3 → 1 → 2 → **1**. Every disagreement in the series took the **lower**-scoring
   candidate. `civ-precise` was the `avg_score` argmax on **3 of 5** prompts and won
   **2 of 5**; `civ-engineer` was argmax on 2 and won **0**. The standing suspect is
   unchanged: the `best_civ` criteria map (`civ_id` → `civ name`) is a **label** map, so
   the chooser may be scoring labels rather than texts. *A chooser that only ever picks
   the worse candidate is anti-correlated with `avg_score` where it disagrees, not
   merely noisy.*

## This run — 8 civs, 5 sims + 5 competition rows each

| rank | civ | avg_score | quality | novelty | alignment |
|------|-----|-----------|---------|---------|-----------|
| 1 | `civ-precise` | 2.0827 | 1.1190 | 2.2590 | 2.8700 |
| 2 | `civ-engineer` | 2.0327 | 0.9790 | 2.2860 | 2.8330 |
| 3 | `civ-formal` | 1.9623 | 0.8830 | 2.2620 | 2.7420 |
| 4 | `civ-poetic` | 1.9507 | 1.1570 | 2.1940 | 2.5010 |
| 5 | `civ-grounded` | 1.5963 | 0.6130 | 2.2870 | 1.8890 |
| 6 | `civ-mythic` | 1.4203 | 0.7770 | 2.2650 | 1.2190 |
| 7 | `civ-therapist` | 1.3057 | 0.6030 | 2.3410 | 0.9730 |
| 8 | `civ-whimsical` | 1.0700 | 0.5350 | 2.2600 | 0.4150 |

Run spreads: `avg_score` **1.0127**, `quality` **0.6220**,
`novelty` **0.1470**, `alignment` **2.4550** — the alignment spread is
**3.95x** the quality spread and **16.70x** the novelty spread, so the ranking is
produced by **alignment**, not by prose quality.

**Run-level low: `civ-whimsical`** (run `avg_score` **1.0700**,
`quality` **0.5350** = lowest in the fleet, `alignment`
**0.4150** = lowest in the fleet, `novelty` **2.2600** =
mid-field).

## Lifetime table (post-run, `culture.json`)

| civ | relevance | per_sim | sims | wins | losses | win_rate |
|-----|-----------|---------|------|------|--------|----------|
| `civ-poetic` | 2369.93 | 1.608 | 1474 | 6 | 727 | 0.008 |
| `civ-precise` | 2211.43 | 1.510 | 1465 | 485 | 243 | 0.666 |
| `civ-whimsical` | 2028.61 | 1.370 | 1481 | 5 | 728 | 0.007 |
| `civ-mythic` | 1904.38 | 1.296 | 1469 | 10 | 717 | 0.014 |
| `civ-formal` | 1888.05 | 1.280 | 1475 | 102 | 629 | 0.140 |
| `civ-engineer` | 1793.56 | 1.225 | 1464 | 50 | 676 | 0.069 |
| `civ-therapist` | 1716.29 | 1.170 | 1467 | 11 | 719 | 0.015 |
| `civ-grounded` | 1594.64 | 1.071 | 1489 | 70 | 662 | 0.096 |

**Lifetime low: `civ-grounded`** — **76th consecutive session**, `relevance`
**1594.64**, `relevance_per_sim` **1.071** — yet its lifetime `win_rate`
**0.096** is 3rd-best in the fleet. *Selection and relevance are separate
axes.* Its lowest lifetime axis is **quality** (**0.4427**, lowest in the
fleet), **not** novelty (**1.6974**, 3rd-lowest).

## Low-relevance signature

The established signature is **high novelty, LOW alignment**. This run:

| civ | novelty gap | alignment gap | run avg_score | fit |
|-----|-------------|---------------|---------------|-----|
| `civ-whimsical` | +0.0010 | **2.4550** | 1.0700 | fits |
| `civ-therapist` | +0.0820 | 1.8970 | 1.3057 | fits |
| `civ-mythic` | +0.0060 | 1.6510 | 1.4203 | partial |

`civ-whimsical` has the **widest alignment gap in the fleet** (**2.4550**) — the
run's single largest separation — and also the **lowest** `avg_score`. Unlike
sessions 202-203, where the run low and the widest alignment gap were split between
two civs, this session they **converge on `civ-whimsical`**. Novelty spread is
**0.1470**, the **narrowest in the series**, against an alignment spread of
**2.4550**. *Report the axis, not the holder.*

## Chooser vs argmax

| prompt | winner | argmax | winner score | argmax score | outcome |
|--------|--------|--------|--------------|--------------|--------|
| what a cell is | `civ-precise` | `civ-engineer` | 1.9967 | 2.0500 | DISAGREE (lower-scoring) |
| the bookkeeper's role | `civ-precise` | `civ-precise` | 1.9000 | 1.9000 | AGREE |
| the witness log | `civ-formal` | `civ-precise` | 2.3033 | 2.4367 | DISAGREE (lower-scoring) |
| ternary values | `civ-formal` | `civ-precise` | 1.9200 | 2.0467 | DISAGREE (lower-scoring) |
| JEV as a decision oracle | `civ-formal` | `civ-engineer` | 2.1100 | 2.1300 | DISAGREE (lower-scoring) |

Agreement **1/5 (20 %)** — 4 down-grades, 0 up-grades.
`civ-precise` was argmax on 3/5 and won 2/5; `civ-engineer` was argmax on 2/5 and
won 0/5.

## Verification (17/17 PASS)

- per-civ ledger Δ **+10 × 8 = 80** new rows; `meta_log.jsonl` Δ **+5** (753 → 758)
- `Winner:` lines = **5**
- mock-log seed multiset of the LAST 80 OK-200 lines **==** the ledger's 80 row seeds
- **80/80** rows carry a parseable seed+colour+figure; distinct seeds **40/80**
- **0** `(civ,prompt)` pairs carrying >1 seed; **0** `EXC`/tracebacks
- `wins` = pre + times won, `losses` = 5 − times won — **8/8 exact**
- `relevance` Δ = ledger Σ`avg_score` — **8/8 exact to 1e-6**
- meta-vs-ledger `avg_score` mismatches **0/40** (later-`ts` row, `meta.results`)
- **0** JEV errors; **0** `2.0/2.0/2.0` fallback triples
- `simulations_run` Δ = **+10** per civ
- counter gap **−609.92 total**, per-civ offsets identical to the documented stable
  values (grounded −84.35, whimsical −173.14, formal −85.53, poetic −96.80,
  precise −32.63, mythic −51.11, therapist −42.11, engineer −44.24)
- extinction risk **NONE** (threshold −10; the lowest civ sits **159.5×** above it)
- `leaderboard.json` updated with 8 civs, relevance within the 2 dp rounding

## Environment

- **z.ai credential gap, 78th session.** `api.z.ai` returns HTTP **401**
  `token expired or incorrect` ⇒ endpoint healthy, credential absent. `ZAI_TOKEN` is
  absent from env and from the sandbox secrets. `ZAI_URL_OVERRIDE` alone is dead code
  behind the token gate, so **both** were set (placeholder token + mock URL).
- **JEV is live**: `TYPESAFEAI_KEY` must be exported as an alias of the sandbox's
  `TYPESAFE_AI_TOKEN`, or `jev_score` silently returns the 2.0/2.0/2.0 fallback triple.
  This session: **0** fallbacks, `jev-1.14.0`.
- The workspace was **wiped** again (only `.plugin-cache` present) ⇒ clone of
  `SuperInstance/AI-Writings` into `/tmp` (NAS at 100 % quota) + a symlink bridge to the
  **inner** `cellular-first-design` directory, verified by inode identity
  (`129:3669` on both sides) and `os.path.samefile()` → `True`.
- The pre-flight caught the fresh mock build on the **response-body length band** at
  **347** — inside the documented 332-369 band on the **first** build, unlike sessions
  200/201 which needed two or three iterations.
- **`pkill -f "mock_zai.py"` self-matched the wrapper shell** and killed it before the
  mock was launched (the port then answered `HTTP=000`, exit 7). Start the mock with a
  pattern that does not appear in the killing command's own argv.
