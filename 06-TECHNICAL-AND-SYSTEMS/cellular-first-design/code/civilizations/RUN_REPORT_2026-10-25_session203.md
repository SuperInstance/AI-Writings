# Civ Orchestrator — Run Report, session 203 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **77th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `21b4f58` (session 202). **All 14 verification assertions PASS.** Pre-flight **12/12 PASS**.

**Session 203 in one line:** `civ-precise` swept **4/5** and `civ-formal` took the fifth
prompt, breaking the two-session 5/5 sweep; the chooser/argmax agreement recovered to
**2/5 (40 %) — 3 down-grades, 0 up-grades**; `civ-grounded` is the lifetime low for the
**75th** consecutive session, but the run-level low rotated away from it to
`civ-therapist` — **breaking the session-202 coincidence**; and the alignment spread
(**1.9850**) is dominant at **2.50x** the quality spread, while the novelty spread
(**0.1770**) is the **narrowest in the series**.

**Three durable lessons from this session:**

1. **A VERIFIER THAT READS A KEY THE ARTIFACT DOES NOT HAVE FAILS 5/5 AND STILL
   LOOKS LIKE A DATA PROBLEM.** The first verifier read `meta_log`'s `avg_score` as a
   top-level key, but `meta_log.jsonl` rows carry **9 keys** (`iso, prompt, results, ts,
   winner_civ, winner_name, …`) and the competition scores live **inside `results`** as
   `[[civ_id, score], …]`. The check reported "meta-vs-ledger mismatches 5/5" — which
   reads exactly like a corrupted ledger. Re-running the same comparison against
   `results` gave **0/40 mismatches**. *A default like `r.get("avg_score", -99)`
   converts a schema mistake into a plausible "data is wrong" story; assert the key
   EXISTS before comparing its value.*
2. **THE RUN-LEVEL LOW AND THE LIFETIME LOW DECOUPLED AGAIN — AND THE COINCIDENCE WAS
   NOT REPRODUCED.** Session 202 had `civ-grounded` as *both* the run low and the
   lifetime low; this session `civ-grounded` placed **6th of 8** on run `avg_score`
   (**1.7500**) while the run low rotated to `civ-therapist`
   (**1.3583**). *Do not carry a coincidence forward as a pattern.*
3. **THE CHOOSER STILL HAS NEVER UP-GRADED — 0 IN 203 SESSIONS.** Agreement across
   sessions 199-203 is 0 → 2 → 3 → 1 → **2**, and **every** disagreement in the series
   took the **lower-scoring** candidate. This session `civ-poetic` was the `avg_score`
   argmax on **3 of 5** prompts and won **0 of 5**. The standing suspect is unchanged:
   the `best_civ` criteria map (`civ_id` -> `civ name`) is a *label* map, so the chooser
   may be scoring labels rather than texts.

## This run — 8 civs, 5 sims + 5 competition rows each

| rank | civ | avg_score | quality | novelty | alignment |
|------|-----|-----------|---------|---------|-----------|
| 1 | `civ-precise` | 2.1827 | 1.4460 | 2.2220 | 2.8800 |
| 2 | `civ-poetic` | 2.1293 | 1.3970 | 2.2970 | 2.6940 |
| 3 | `civ-formal` | 1.9750 | 1.0030 | 2.2950 | 2.6270 |
| 4 | `civ-engineer` | 1.9283 | 1.0040 | 2.3040 | 2.4770 |
| 5 | `civ-mythic` | 1.7787 | 1.1820 | 2.2880 | 1.8660 |
| 6 | `civ-grounded` | 1.7500 | 0.8840 | 2.3030 | 2.0630 |
| 7 | `civ-whimsical` | 1.3743 | 0.8990 | 2.3290 | 0.8950 |
| 8 | `civ-therapist` | 1.3583 | 0.6530 | 2.3990 | 1.0230 |

Run spreads: `avg_score` **0.8243**, `quality` **0.7930**,
`novelty` **0.1770**, `alignment` **1.9850** — the alignment spread is
**2.50x** the quality spread, so the ranking is produced by
**alignment**, not by prose quality.

**Run-level low: `civ-therapist`** (run `avg_score` **1.3583**,
`quality` **0.6530** = lowest in the fleet, `alignment`
**1.0230** = 2nd-lowest, `novelty` **2.3990** =
**highest in the fleet**).

## Lifetime table (post-run, `culture.json`)

| civ | relevance | per_sim | sims | wins | losses | win_rate |
|-----|-----------|---------|------|------|--------|----------|
| `civ-poetic` | 2350.43 | 1.605 | 1464 | 6 | 722 | 0.008 |
| `civ-precise` | 2190.60 | 1.506 | 1455 | 483 | 240 | 0.668 |
| `civ-whimsical` | 2017.91 | 1.372 | 1471 | 5 | 723 | 0.007 |
| `civ-mythic` | 1890.18 | 1.296 | 1459 | 10 | 712 | 0.014 |
| `civ-formal` | 1868.43 | 1.275 | 1465 | 99 | 627 | 0.136 |
| `civ-engineer` | 1773.23 | 1.220 | 1454 | 50 | 671 | 0.069 |
| `civ-therapist` | 1703.24 | 1.169 | 1457 | 11 | 714 | 0.015 |
| `civ-grounded` | 1578.68 | 1.067 | 1479 | 70 | 657 | 0.096 |

**Lifetime low: `civ-grounded`** — **75th consecutive session**, `relevance`
**1578.68**, `relevance_per_sim`
**1.067** — yet its lifetime `win_rate`
**0.096** is 3rd-best in the fleet. *Selection and
relevance are separate axes.* Its lowest lifetime axis is **quality**
(**0.4415**, lowest in the fleet), **not** novelty (**1.6935**, 3rd-lowest).

## Low-relevance signature

The established signature is **high novelty, LOW alignment**. This run:

| civ | novelty gap | alignment gap | run avg_score | fit |
|-----|-------------|---------------|---------------|-----|
| `civ-whimsical` | +0.1070 | **1.9850** | 1.3743 | fits |
| `civ-therapist` | +0.1770 | **1.8570** | 1.3583 | fits |
| `civ-grounded` | +0.0810 | 0.8170 | 1.7500 | partial |

`civ-whimsical` has the **widest alignment gap in the fleet** (**1.9850**) — the
run's single largest separation — yet the *lowest* `avg_score` belongs to
`civ-therapist`, whose alignment gap is marginally narrower but whose **quality** is
the fleet's lowest (**0.6530**). *Report the axis, not the holder.*

## Chooser vs argmax

| prompt | winner | argmax | winner score | argmax score | outcome |
|--------|--------|--------|--------------|--------------|--------|
| what a cell is | `civ-precise` | `civ-poetic` | 2.0267 | 2.0400 | DISAGREE (lower-scoring) |
| the bookkeeper's role | `civ-precise` | `civ-poetic` | 2.0200 | 2.1567 | DISAGREE (lower-scoring) |
| the witness log | `civ-precise` | `civ-precise` | 2.5167 | 2.5167 | AGREE |
| ternary values | `civ-precise` | `civ-precise` | 2.0533 | 2.0533 | AGREE |
| JEV as a decision oracle | `civ-formal` | `civ-poetic` | 1.9800 | 2.1867 | DISAGREE (lower-scoring) |

Agreement **2/5 (40 %)** — 3 down-grades, 0 up-grades.
`civ-poetic` was argmax on 3/5 and won 0/5.

## Verification (14/14 PASS)

- per-civ ledger Δ **+10 × 8 = 80** new rows; `meta_log.jsonl` Δ **+5** (748 → 753)
- `Winner:` lines = **5**
- mock-log seed multiset of the LAST 80 OK-200 lines **==** the ledger's 80 row seeds
- **80/80** rows carry a parseable seed+colour+figure; distinct seeds **40/80**
- **0** `(civ,prompt)` pairs carrying >1 seed; **0** `EXC`/tracebacks
- `wins` = pre + times won, `losses` = 5 − times won — **8/8 exact**
- `relevance` Δ = ledger Σ`avg_score` — **8/8 exact to 1e-6**
- meta-vs-ledger `avg_score` mismatches **0/40** (later-`ts` row, `meta.results`)
- **0** JEV errors; **0** `2.0/2.0/2.0` fallback triples
- counter gap **−609.92 total**, per-civ offsets identical to the documented stable
  values (grounded −84.35, whimsical −173.14, formal −85.53, poetic −96.80,
  precise −32.63, mythic −51.11, therapist −42.11, engineer −44.24)
- extinction risk **NONE** (threshold −10; the lowest civ sits **158.9×** above it)

## Environment

- **z.ai credential gap, 77th session.** `api.z.ai` returns HTTP **401**
  `token expired or incorrect` ⇒ endpoint healthy, credential absent. `ZAI_TOKEN` is
  absent from env and from the sandbox secrets. `ZAI_URL_OVERRIDE` alone is dead code
  behind the token gate, so **both** were set (placeholder token + mock URL).
- **JEV is live**: `TYPESAFEAI_KEY` must be exported as an alias of the sandbox's
  `TYPESAFE_AI_TOKEN`, or `jev_score` silently returns the 2.0/2.0/2.0 fallback triple.
  This session: **0** fallbacks, `jev-1.14.0`.
- The workspace was **wiped** (only `.plugin-cache` present) ⇒ sparse clone of
  `SuperInstance/AI-Writings` into `/tmp` (NAS at 100 % quota) + a symlink bridge to the
  **inner** `cellular-first-design` directory, verified by inode identity
  (`113:97` on both sides) and `os.path.samefile()` → `True`.
- The pre-flight caught the fresh mock build twice on the **response-body length
  band**: 287 → 294 → **352**, the last inside the documented 332-369 band. *A band
  check is a variance check: fix the cause of the variance, not its maximum.*
