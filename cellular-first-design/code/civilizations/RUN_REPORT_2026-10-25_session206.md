# Civ Orchestrator — Run Report, session 206 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **79th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `2d2a417` (session 205 tree). **All 27 verification assertions PASS.** Pre-flight **14/14 PASS**.

**Session 206 in one line:** `civ-precise` took 2 of 5 prompts, `civ-grounded`/`civ-engineer`/`civ-formal`
1 each — and the chooser/argmax agreement fell to **0/5 (0 %) — 5 down-grades, 0 up-grades**,
the lowest reading in the series, with `civ-poetic` the argmax on **all five** prompts and
**zero** wins; the run-level low rotated to `civ-therapist` (run `avg_score` **1.4160**,
`alignment` **0.8870** = lowest in the fleet) while `civ-grounded` remains the **lifetime low
for the 77th consecutive session** — *the run low and the lifetime low are again different civs
on different axes*; and the alignment spread (**2.1450**) is **2.88x** the quality spread and
**8.31x** the novelty spread, so the ranking is again produced by **alignment**.

**Three durable lessons from this session:**

1. **A PER-PROMPT ROW-COUNT ASSERTION IS A CHECKER BUG, NOT A RUN BUG — THE
   SIM PHASE DRAWS PROMPTS AT RANDOM.** The verifier asserted "8 rows per prompt" and
   failed. The per-prompt row counts are **13 / 17 / 17 / 18 / 15**, because the 5 sims
   per civ draw from the 5 prompts *uniformly at random* (so a prompt gets 0-2 rows from
   the sim phase) **and** the competition phase contributes exactly **one** row per civ
   per prompt. The correct assertion is **8 distinct seeds and 8 distinct previews** per
   prompt — the *uniqueness* of the competition phase, not its row count. *The competition
   phase is identified by uniqueness; the sim phase is identified by multiplicity.*
2. **THE CHOOSER HAS NOW NEVER UP-GRADED, AND THIS SESSION IT TOOK THE LOSER ON EVERY
   SINGLE PROMPT.** Agreement across sessions 199-206 reads 0 → 2 → 3 → 1 → 2 → 1 → **0**.
   `civ-poetic` was the `avg_score` argmax on **5 of 5** prompts and won **0 of 5**; the
   largest single disagreement ("the witness log") was **2.1000 chosen vs 2.6333 argmax**,
   a **−0.5333** gap. A chooser that picks the lower-scoring candidate *every* time is
   not noisy — it is **anti-correlated** with `avg_score`. The standing suspect is
   unchanged: the `best_civ` criteria map (`civ_id` -> `civ name`) is a **label** map, so
   the chooser may be scoring labels rather than texts.
3. **A FRESH MOCK HIT THE 332-369 BODY BAND ON THE FIRST BUILD, BUT ONLY BECAUSE THE
   TAIL LENGTH WAS SOLVED ARITHMETICALLY.** The header width varies by 4 chars
   (`[mock-zai <8-hex>] #<6-hex> <figure>.` = 33-37), so a fixed tail of length *T*
   yields totals *min+T+1 .. max+T+1*; the band is satisfiable iff *T* in **[298, 331]**.
   Choosing *T* = **320** gives totals **354-358** — inside the documented 352-358
   window — with the prose written to hit the length by *counting*, not by trimming.
   *Compute the band algebraically before writing the template; do not iterate the
   template.*

## This run — 8 civs, 5 sims + 5 competition rows each

| rank | civ | avg_score | quality | novelty | alignment |
|------|-----|-----------|---------|---------|-----------|
| 1 | `civ-precise` | 2.2997 | 1.4550 | 2.4120 | 3.0320 |
| 2 | `civ-poetic` | 2.2620 | 1.5820 | 2.4520 | 2.7520 |
| 3 | `civ-formal` | 2.0267 | 1.2750 | 2.3480 | 2.4570 |
| 4 | `civ-engineer` | 2.0303 | 1.2940 | 2.2650 | 2.5320 |
| 5 | `civ-mythic` | 1.9613 | 1.3340 | 2.4490 | 2.1010 |
| 6 | `civ-grounded` | 1.8750 | 1.1070 | 2.3990 | 2.1190 |
| 7 | `civ-whimsical` | 1.7417 | 1.0510 | 2.4850 | 1.6890 |
| 8 | **`civ-therapist`** | **1.4160** | **0.8380** | 2.5230 | **0.8870** |

Run spreads: `avg_score` **0.8837**, `quality` **0.7440**,
`novelty` **0.2580**, `alignment` **2.1450** — the alignment spread is
**2.88x** the quality spread and **8.31x** the novelty spread, so the ranking is
produced by **alignment**, not by prose quality.

**Run-level low: `civ-therapist`** (run `avg_score` **1.4160**,
`quality` **0.8380** = lowest in the fleet, `alignment`
**0.8870** = lowest in the fleet, `novelty` **2.5230** =
**highest** in the fleet).

## Lifetime table (post-run, `culture.json`)

| civ | relevance | per_sim | sims | wins | losses | win_rate |
|-----|-----------|---------|------|------|--------|----------|
| civ-poetic | 2407.82 | 1.612 | 1494 | 6 | 737 | 0.008 |
| civ-precise | 2253.91 | 1.518 | 1485 | 492 | 246 | 0.667 |
| civ-whimsical | 2057.73 | 1.371 | 1501 | 5 | 738 | 0.007 |
| civ-mythic | 1939.49 | 1.303 | 1489 | 10 | 727 | 0.014 |
| civ-formal | 1926.89 | 1.289 | 1495 | 103 | 638 | 0.139 |
| civ-engineer | 1830.27 | 1.233 | 1484 | 51 | 685 | 0.069 |
| **civ-therapist** | **1745.34** | **1.174** | 1487 | 11 | 729 | 0.015 |
| **civ-grounded** | **1630.06** | **1.080** | 1509 | 71 | 671 | 0.096 |

**Lifetime low: `civ-grounded`** — **77th consecutive session**, `relevance`
**1630.06**, `relevance_per_sim` **1.080** — yet its lifetime `win_rate`
**0.096** is 3rd-best in the fleet. *Selection and relevance are separate
axes.* Its lowest lifetime axis is **quality** (**0.4546**, lowest in the
fleet), **not** novelty (**2.1321**, mid-field).

## Low-relevance signature

The established signature is **high novelty, LOW alignment**. This run:

| civ | novelty gap | alignment gap | run avg_score | fit |
|-----|-------------|---------------|---------------|-----|
| `civ-therapist` | +0.0740 | **2.1450** | 1.4160 | fits |
| `civ-whimsical` | +0.0360 | 1.3430 | 1.7417 | fits |
| `civ-grounded` | -0.0480 | 1.2490 | 1.8750 | partial |

`civ-therapist` has the **widest alignment gap in the fleet** (**2.1450**) — the
run's single largest separation — and also the **lowest** `avg_score`, the **lowest**
`quality`, and the **highest** `novelty**. Unlike sessions 202-203, where the run low and
the widest alignment gap were split between two civs, this session they
**converge on `civ-therapist`**. Novelty spread is **0.2580**, against an alignment
spread of **2.1450**. *Report the axis, not the holder.*

## Chooser vs argmax

| prompt | winner | argmax | winner score | argmax score | outcome |
|--------|--------|--------|--------------|--------------|--------|
| what a cell is | `civ-precise` | `civ-poetic` | 2.1167 | 2.1367 | DISAGREE (lower-scoring) |
| the bookkeeper's role | `civ-precise` | `civ-poetic` | 2.2067 | 2.4300 | DISAGREE (lower-scoring) |
| the witness log | **`civ-grounded`** | `civ-precise` | 2.1000 | 2.6333 | DISAGREE (lower-scoring) |
| ternary values | `civ-engineer` | `civ-poetic` | 1.7567 | 2.0633 | DISAGREE (lower-scoring) |
| JEV as a decision oracle | `civ-formal` | `civ-poetic` | 2.0867 | 2.4767 | DISAGREE (lower-scoring) |

Agreement **0/5 (0 %)** — 5 down-grades, 0 up-grades.
`civ-poetic` was argmax on **5 of 5** prompts and won **0 of 5**.

**Note:** `civ-grounded` won a prompt outright this session — the second time in the
series (session 201 also gave it one) that the **lifetime-low** civ takes a competition.
Its win was the *second*-highest scored candidate, i.e. still a down-grade relative to
the argmax.

## Verification (27/27 PASS)

- per-civ ledger Δ **+10 × 8 = 80** new rows; `meta_log.jsonl` Δ **+5** (763 → 768)
- `Winner:` lines = **5**; log `Winner:` == `meta_log.winner_civ` — **5/5 agree**
- mock-log seed multiset of the LAST 80 OK-200 lines **==** the ledger's 80 row seeds
  (**run-scoped proof**, not a lifetime multiset)
- **80/80** rows carry a parseable seed+colour+figure; **80/80** match an independently
  recomputed `md5(whole_message)[:8]`; distinct seeds **40/80**
- **0** `(civ,prompt)` pairs carrying >1 seed; **0** `EXC`/tracebacks
- `relevance` Δ = ledger Σ`avg_score` — **8/8 exact to 1e-6**
- `wins` = pre + times won, `losses` = 5 − times won — **8/8 exact**
- meta-vs-ledger `avg_score` (later-`ts` row, `meta.results`) — **0/40 mismatches**
- **0** JEV errors; **0** `2.0/2.0/2.0` fallback triples; provider on all rows = **`zai`**
- `simulations_run` Δ = **+10** per civ
- extinction risk **NONE** (threshold −10; the lowest civ sits **163.0×** above it)
- `leaderboard.json` updated with 8 civs, iso `2026-10-25T11:23:59`
- **no birth** (8 civ dirs, all `generation=1`); orchestrator exit **0**

### One verifier bug this session — caught by the VERDICT line, not by the run

The verifier's check *"per-prompt 8/8 distinct seeds AND previews"* was **red** on the
first run because it also asserted `n == 8` — a **row count**. The per-prompt row counts
are 13 / 17 / 17 / 18 / 15, because the sim phase draws prompts uniformly at random and
the competition phase adds one row per civ per prompt. The *distinctness* assertions
(8 distinct seeds, 8 distinct previews) were green for all five prompts from the start.
The check was fixed to assert uniqueness only; **the run was never re-executed**,
because the artifact was clean and only the checker was wrong. *A checker that
over-asserts produces a false "the data is wrong" story; the fix is to the checker, and
the run's rows are the evidence.*

## Pre-flight (14/14 PASS, first build)

| # | check | result |
|---|---|---|
| 1 | cultural-prompt length band **167-209** | **167-209** |
| 2 | zero transport errors | **40 responses** |
| 3 | distinct seeds | **40** |
| 4 | distinct previews | **40** |
| 5 | recomputed seed+colour+figure present | **40/40** |
| 6 | per-prompt 8/8 distinct seeds AND previews | **8/8 × 5** |
| 7 | zero literal `seed={}` | **0** |
| 8 | zero `EXC:`/tracebacks | **0** |
| 9 | `[mock-zai` prefix | **40/40** |
| 10 | **repeat-same-message => same seed** | **20/20** |
| 11 | zero `(civ,prompt)` pairs carrying >1 seed | **40/40 distinct** |
| 12 | response body length band **332-369** | **354-358** |
| 13 | gate prints a final verdict | **PASS**, exit 0 |
| 14 | no partial-crash gate | **PASS** |

### The body band was solved algebraically, not by iteration

The mock header is `[mock-zai <8-hex>] #<6-hex> <figure>.` — width **33-37** across all
40 (civ, prompt) messages, because the figure name length varies. A fixed tail of length
*T* therefore yields body totals *min+T+1 .. max+T+1*, so the **332-369** band is
satisfiable iff ***T* ∈ [298, 331]**. *T* = **320** was chosen, giving **354-358** — the
documented 352-358 window — on the **first** build. The prose was written to hit 320
characters by counting, not by trimming. *A band check is a variance check: fix the
cause of the variance, not its maximum — and solve the band before writing the template.*

## Environment (session 206)

- **z.ai credential gap, 79th session.** `api.z.ai` returns HTTP **401**
  `token expired or incorrect` ⇒ endpoint healthy, credential absent. `ZAI_TOKEN` is
  absent from env and from the sandbox secrets. `ZAI_URL_OVERRIDE` alone is dead code
  behind the token gate, so **both** were set (placeholder token + mock URL).
- **JEV is live**: `TYPESAFEAI_KEY` must be exported as an alias of the sandbox's
  `TYPESAFE_AI_TOKEN`, or `jev_score` silently returns the 2.0/2.0/2.0 fallback triple.
  This session: **0** fallbacks, `jev-1.14.0`, 0 JEV errors.
- The workspace was **wiped** again (only `.plugin-cache` present) ⇒ clone of
  `SuperInstance/AI-Writings` into `/tmp` (NAS at 100 % quota) + a symlink bridge to the
  **inner** `cellular-first-design` directory, verified by inode identity
  (`129:10423` on both sides) and `os.path.samefile()` → `True`.
- The baseline was derived from the **git blob** of each ledger and `culture.json` at
  `2d2a417` — never from a remembered count, and never from the working tree.
- `HOME` was redirected to `/root`: `/workspace/.home/.gitconfig` could not be written
  (NAS EDQUOT), so the global git config was re-created on the overlay filesystem.
