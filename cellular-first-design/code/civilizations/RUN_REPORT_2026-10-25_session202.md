# Civ Orchestrator — Run Report, session 202 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **76th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `2f0fb30` (session 201). **All 16 verification assertions PASS.** Pre-flight **14/14 PASS**.

Full detail: `RUN_REPORT_2026-10-25_session202.md`.

**Session 202 in one line:** `civ-precise` swept **5/5 again** — the second sweep after
session 201 broke the ten-session streak — but the chooser/argmax agreement fell to
**1/5 (20 %) — 4 down-grades, 0 up-grades**, and `civ-grounded` was the run-level low
**and** the lifetime low in the same session (the first such coincidence since session
195); the alignment spread (**1.8960**) is still dominant at **1.62x** the quality spread,
while the novelty spread (**0.1380**) is the **narrowest in the series**.

**Three durable lessons from this session:**

1. **THE PRE-FLIGHT BAND CHECK CAUGHT THE FRESH MOCK BUILD, AND THE FIX WAS TO REMOVE
   THE VARIANCE.** The first body template rendered at **460** characters against the
   **332–369** band — the gate reported a clean, localised `[FAIL] response body length
   band 332-369 min=460 max=460`. The template was already variance-free, so the fix
   was to shorten the tail to a constant **352** — not to trim the longest instance.
   *A band check is a variance check: fix the cause of the variance, not its maximum.*
2. **THE RUN-LEVEL LOW AND THE LIFETIME LOW CAN COINCIDE — AND WHEN THEY DO, SAY SO
   EXPLICITLY.** `civ-grounded` was 8th of 8 on this run's `avg_score` (**1.4130**) and
   also holds the lifetime low (`relevance` **1561.18**, `relevance_per_sim` **1.063**).
   Its run axes are `quality` **0.4140** (lowest in the fleet) and `alignment` **1.1610**
   (2nd-lowest), while `novelty` **2.6640** is the **highest** in the fleet.
   *Do not attribute a low-novelty reading to a civ whose novelty is the highest.*
3. **THE CHOOSER HAS STILL NEVER UP-GRADED — AND THE GAP IS WIDENING, NOT NOISY.**
   Agreement across sessions 198–202 is 3 → 0 → 2 → 3 → **1**, and **every**
   disagreement in the series took the **lower-scoring** candidate (**0 up-grades
   ever**). This session `civ-poetic` was the `avg_score` argmax on **4 of 5** prompts
   and won **0 of 5**. A chooser that only ever picks the worse candidate is
   *anti-correlated* with `avg_score` where it disagrees. The standing suspect is
   unchanged: the `best_civ` criteria map (`civ_id` -> `civ name`) is a *label* map, so
   the chooser may be scoring labels rather than texts.

## Run-level ranking (this session's 10 new rows per civ)

| rank | civ | avg_score | quality | novelty | alignment | relevance Δ |
|-----:|-----|----------:|--------:|--------:|-----------:|------------:|
| 1 | civ-poetic | 2.3863 | 1.5810 | 2.5740 | 3.0040 | +23.8633 |
| 2 | civ-precise | 2.1960 | 1.1690 | 2.5920 | 2.8270 | +21.9600 |
| 3 | civ-formal | 1.9940 | 0.9150 | 2.6290 | 2.4380 | +19.9400 |
| 4 | civ-mythic | 1.9870 | 1.1180 | 2.5550 | 2.2880 | +19.8700 |
| 5 | civ-engineer | 1.8000 | 0.8480 | 2.5260 | 2.0260 | +18.0000 |
| 6 | civ-whimsical | 1.6750 | 0.9580 | 2.6010 | 1.4660 | +16.7500 |
| 7 | civ-therapist | 1.4577 | 0.6430 | 2.6220 | 1.1080 | +14.5767 |
| 8 | civ-grounded | 1.4130 | 0.4140 | 2.6640 | 1.1610 | +14.1300 |

Axis spreads: **alignment 1.8960** > **quality 1.1670** > **avg_score 0.9733** >
**novelty 0.1380**. The ranking is produced by alignment and quality, not novelty.

## Lifetime table (post-run `culture.json`)

| civ | relevance | relevance_per_sim | sims_run | wins | losses | win_rate |
|-----|----------:|------------------:|---------:|-----:|-------:|---------:|
| civ-poetic | 2329.13 | 1.602 | 1454 | 6 | 717 | 0.008 |
| civ-precise | 2168.77 | 1.501 | 1445 | 479 | 239 | 0.667 |
| civ-whimsical | 2004.17 | 1.372 | 1461 | 5 | 718 | 0.007 |
| civ-mythic | 1872.39 | 1.292 | 1449 | 10 | 707 | 0.014 |
| civ-formal | 1848.68 | 1.271 | 1455 | 98 | 623 | 0.136 |
| civ-engineer | 1753.95 | 1.215 | 1444 | 50 | 666 | 0.070 |
| civ-therapist | 1689.65 | 1.168 | 1447 | 11 | 709 | 0.015 |
| civ-grounded | 1561.18 | 1.063 | 1469 | 70 | 652 | 0.097 |

**Lifetime low: `civ-grounded`** — 74th consecutive session, `relevance` 1561.18,
`relevance_per_sim` 1.063 — yet its lifetime `win_rate` **0.097** is 3rd-best in the
fleet. *Selection and relevance are separate axes.*

## Low-relevance signature

`civ-grounded` and `civ-therapist` both fit the established "high novelty, low
alignment" signature (gaps +1.5030 and +1.5140). `civ-grounded`'s lowest axis is
**quality** (0.4140, lowest in the fleet), not novelty (2.6640, highest in the fleet).

## Chooser vs argmax

| prompt | winner | argmax | outcome |
|--------|--------|--------|---------|
| what a cell is | civ-precise | civ-poetic | DISAGREE (lower-scoring) |
| the bookkeeper's role | civ-precise | civ-poetic | DISAGREE (lower-scoring) |
| the witness log | civ-precise | civ-precise | AGREE |
| ternary values | civ-precise | civ-poetic | DISAGREE (lower-scoring) |
| JEV as a decision oracle | civ-precise | civ-poetic | DISAGREE (lower-scoring) |

Agreement **1/5 (20 %)** — 4 down-grades, 0 up-grades. `civ-poetic` was argmax on 4/5
and won 0/5.

## Verification (16/16 PASS)

- per-civ ledger Δ **+10 × 8 = 80** new rows; `meta_log.jsonl` Δ **+5**
- mock-log seed multiset of the LAST 80 OK-200 lines **==** the ledger's 80 row seeds
- 80/80 rows match an independently recomputed message md5; distinct seeds **40/80**
- 0 `(civ,prompt)` pairs carrying >1 seed; 0 `EXC`/tracebacks
- `wins` = pre + times won, `losses` = 5 − times won — **8/8 exact**
- `relevance` Δ = ledger Σ`avg_score` — **8/8 exact to 1e-6**
- meta-vs-ledger `avg_score` mismatches **0/40** (later-`ts` row)
- 0 JEV errors; 0 `2.0/2.0/2.0` fallback triples
- extinction risk **NONE** (threshold −10; lowest civ sits ~156× above it)
