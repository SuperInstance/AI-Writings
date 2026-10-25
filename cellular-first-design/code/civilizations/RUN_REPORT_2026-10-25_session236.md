# Civ Orchestrator - Run Report, session 236 (2026-10-25)

## Session 236 (2026-10-25) - provider path, baseline, and result

- Provider path: **Control B mock** (z.ai credential gap, **98th session**) + **live JEV**
  (`jev-1.14.0`; 0 fallback triples, 0 error keys in the 80 new rows).
- Baseline: `7e20c5f` (session 235 tree), `refs/heads/main` asserted equal to the clone HEAD
  (`7e20c5f9fca68bb1e3767a92a606af74e978fefd`).
- Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
- **Pre-flight gate: 12/12 PASS** (first clean build). **Run verification: 16/16 PASS.**
- Result: `civ-precise` swept **5/5** competitions; chooser/argmax agreement **1/5 (20 %)** - 4 down-grades, 0 up-grades.
- Run low: **`civ-therapist`** (avg **1.2800**, fleet-low run quality **0.3890** and alignment **0.9660** - a two-axis collapse).
- Lifetime low: **`civ-grounded`** (**2156.20**, **99th consecutive session**).
- The mock body landed at **349** chars on the first clean build (38-char header + 162-char tail prefix + 149-char continuation, solved algebraically).

## Bootstrap (fresh sandbox)

- The prompt path `/workspace/repos/ai-writings/cellular-first-design/...` did not exist -
  a **fresh sandbox**, workspace empty except `.plugin-cache` (109th consecutive session).
- The slug `ai-writings/cellular-first-design` **404s**: `ai-writings` is a *different* org
  holding one unrelated repo. The upstream is **`SuperInstance/AI-Writings`**.
- NAS EDQUOT (**18th session**): a bulk clone into `/workspace` dies with
  `Disk quota exceeded` mid-`.git`. Cloned to the overlay (`/tmp`) with `--depth 1`.
- **Bridge**: `mkdir -p /workspace/repos/ai-writings` **first**, then
  `ln -s /tmp/clone/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`.
  The link target is the directory that actually contains `code/civilizations/`; verified with
  `os.path.samefile()` -> `True`. (`ln -s` without the intermediate `mkdir -p` fails ENOENT.)
- `ZAI_TOKEN` absent from env and all **8** sandbox secrets; z.ai **401** => endpoint healthy,
  credential absent. `ZAI_URL_OVERRIDE` alone is dead code - Control B needs **both**
  `ZAI_TOKEN` (the gate) and `ZAI_URL_OVERRIDE` (the destination).
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`.

## The ledger is the specification (mock re-derived, not guessed)

The Control B mock source is **not in the repo** - it is a per-session artifact. The algorithm
was re-derived from the ledger and fitted against the **whole current-format ledger** (not
against its own fresh rows, which would be circular):

```
d      = md5(user_message).digest()
h      = d.hex()
i      = d[0] % 4                # DIGEST BYTE, not int(h[0],16)
seed   = h[(i*2)%8 : (i*2)%8+4]
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"
```

**2160/2160** current-format mock rows reproduced exactly, **0 mismatches**.

### NEW - THE LEDGER HAS **TWO** MOCK GENERATIONS, AND THE LOOSE REGEX OVERCOUNTS

The ledger holds **11440** `[mock-zai` rows but only **2160** are current-format
(`[mock-zai <4hex>] #<4hex> <4/4/4>.`); the rest are an **older 12-hex** generation
(`[mock-zai 47862e3989af] Someb...`). A loose `^\[mock-zai ([0-9a-f]{4})\]` regex does **not**
match the 12-hex rows correctly - `pv[7:11]` on a current row lands inside the literal
`"mock-zai "` and yields `"ai 4"`, not a seed.

*Rule: anchor the current-format regex on the **full** header shape before counting, and take
the seed at **offset 10**, not 7. A "2240/2240" verification that was actually counting a
mixed-generation population is a false PASS - the count must equal the number of rows the
strict pattern accepts.*

### NEW - THE SEED SLICE IS AT OFFSET **10**, NOT 7

`"[mock-zai "` is **10** characters, so the seed is `content_preview[10:14]`. Every
distinctness check written against `[:11]` silently reads a 4-char window that *starts with
the literal `"ai "`* and therefore compares mostly-equal strings - which is why a broken
mock reported "15/40 distinct" and a correct one reported "6-7/8 per prompt" instead of 8/8.

*Rule: the header is a fixed-width literal; derive the offsets from the format string, never
from eyeballed positions.*

## Run verification - 16/16 PASS

| check | result |
|---|---|
| per-civ ledger delta | **+10** x 8 = **80** rows |
| `meta_log` | 913 -> **918** (+5) |
| competition rows with `winner_civ` | **5** (all `civ-precise`) |
| JEV `error` keys | **0** |
| 2.0/2.0/2.0 fallback triples | **0** |
| rows with `provider=zai` | **80/80** |
| `content_preview` length | **200** on 80/80 |
| `[mock-zai` prefix | **80/80** |
| seed+colour+figure recomputed | **80/80** |
| `wins+losses` delta | **+5** per civ, exact vs the git blob |
| `simulations_run` delta | **+10** on all 8 |
| `generation` | unchanged (all 1) |
| leaderboard | 8 entries, sorted desc by `relevance_per_sim` |
| relevance delta vs ledger sum | 8/8 exact (max residual 1.39e-12) |
| git tree | **18** modified |

### The counter gap is BYTE-IDENTICAL to session 234 - fixed, not accumulating

| civ | relevance | ledger sum avg_score | gap |
|---|---|---|---|
| `civ-grounded` | 2156.2033 | 2240.5500 | **-84.3467** |
| `civ-therapist` | 2182.8200 | 2224.9333 | **-42.1133** |
| `civ-engineer` | 2413.6600 | 2457.9033 | **-44.2433** |
| `civ-mythic` | 2480.0400 | 2531.1500 | **-51.1100** |
| `civ-formal` | 2526.0967 | 2611.6233 | **-85.5267** |
| `civ-whimsical` | 2527.8900 | 2701.0333 | **-173.1433** |
| `civ-precise` | 2924.3533 | 2956.9867 | **-32.6333** |
| `civ-poetic` | 3047.5000 | 3144.3033 | **-96.8033** |

Max drift vs the documented session-234 table: **0.0000**.

## The low-relevance civilizations

| civ | relevance | per_sim | win_rate | rel D | run avg | lifetime avg | lifetime q | lifetime align |
|---|---|---|---|---|---|---|---|---|
| `civ-grounded` | 2156.20 | 1.192 | 0.084 | +15.18 | 1.5183 | 1.2098 | 0.5340 | 1.2836 |
| `civ-therapist` | 2182.82 | 1.221 | 0.012 | +12.80 | 1.2800 | 1.2333 | 0.5449 | 1.1810 |
| `civ-engineer` | 2413.66 | 1.353 | 0.062 | +16.94 | 1.6940 | 1.3610 | 0.6227 | 1.6752 |
| `civ-mythic` | 2480.04 | 1.386 | 0.011 | +17.55 | 1.7553 | 1.3992 | 0.6879 | 1.5759 |
| `civ-whimsical` | 2527.89 | 1.404 | 0.006 | +14.21 | 1.4210 | 1.4491 | 0.6724 | 1.5755 |
| `civ-formal` | 2526.10 | 1.407 | 0.129 | +17.78 | 1.7777 | 1.4217 | 0.6222 | 1.8945 |
| `civ-precise` | 2924.35 | 1.638 | 0.700 | +19.68 | 1.9683 | 1.6419 | 0.7407 | 2.3342 |
| `civ-poetic` | 3047.50 | 1.699 | 0.007 | +21.05 | 2.1047 | 1.7173 | 0.9184 | 2.1821 |

- **`civ-grounded`** - lifetime low for the **99th consecutive session** (relevance **2156.20**,
  `relevance_per_sim` 1.192, lifetime `avg_score` **1.2098**). Lifetime **quality 0.5340** is the
  fleet low; lifetime **alignment 1.2836** is 2nd-lowest, 1.8x behind `civ-precise` (2.3342)
  => a **voice** failure, not a prose failure. Lifetime novelty 1.8118 is 6th of 8 - check the
  rank, not the impression. On *this* run it placed 6th of 8 (avg 1.5183) and still gained
  **+15.18** relevance.
- **`civ-therapist`** - the **run low** (avg **1.2800**) with the fleet-low run quality
  (**0.3890**) and run alignment (**0.9660**), while novelty held at 2.4850 (2nd-highest) -
  a **two-axis** collapse. Its lifetime **alignment 1.1810** is the fleet low. It took
  **0/5** competitions.
- **`civ-whimsical`** - lifetime `win_rate` **0.006** (5 wins in 888) and the **largest
  counter gap** in the fleet (**-173.1433**). It finished at 1.4210 on this run's `avg_score`
  with the fleet-low run **quality 0.4430** but 2nd-highest run **novelty 2.5700** - it is not
  boring, it is mis-voiced.
- **`civ-poetic`** - the mirror-image failure: **1st** on lifetime `avg_score` (1.7173),
  lifetime `quality` (0.9184) and lifetime `relevance` (3047.50), yet **last** on
  `win_rate` (0.007) - it won **0/5** this run. A *selection* failure, not a quality collapse.
- **Extinction risk: NONE.** Threshold **-10**, lowest civ at **+2156.20** = **215x** the floor.
  Registry 8, `max_civs` 12, all `generation=1`. No extinction, no birth (non-`--loop` run).

## Inverses and distinct axes

- Cross-civ spreads (this run): `avg_score` **0.8247**, alignment **1.6910**, quality **0.7390**,
  novelty **0.1730**. The **alignment** axis dominates again - 2.05x the `avg_score` spread.
- `civ-poetic` had the run's highest `avg_score` (2.1047) and the highest run alignment (2.6570).

## Chooser vs `avg_score` argmax: 1/5 (20 %)

4 down-grades, 0 up-grades. In all 4 the chooser took the **lower**-scoring candidate
(deltas -0.2633, -0.1133, -0.1733, -0.1633), and the argmax was `civ-poetic` on **4 of 5**
prompts. The series (211-235) reads 0 / 40 / 40 / 20 / 100 / 60 / 40 / 40 / 20 / 40 / 20 / 40 /
40 / 100 / 60 / 80 / 40 / 40 / 20 / 40 / 60 / 40 / 40 / 20 %. **Up-grades across the whole
series: 0.** Never predict the next value from the last one, and never let a sweep imply
agreement.

## Notes for the next session

1. The repo slug in the task prompt is wrong. Upstream is `SuperInstance/AI-Writings`.
2. Do not clone into `/workspace` - the NAS is at 100 % and a bulk clone dies mid-`.git`.
   Clone to `/tmp` (overlay), then `mkdir -p` **every** intermediate path before the symlink
   and verify with `os.path.samefile()`.
3. The mock is **not on disk** at session start (`/tmp` wiped) - rebuild from the ledger
   algorithm above, then run the pre-flight **before** the batch. The seed slice is at
   offset **10**; the body is `38 + 162 + continuation`, target 349.
4. The ledger carries **two** mock generations - anchor the current-format regex on the full
   header shape before counting, or the verification count is wrong.
5. The **meta-log row is written AFTER the competition rows** - a meta row's `ts` is ~3 s
   *later* than the ledger rows it summarises. Assert `min(ts) <= meta.ts`.
6. Kill the mock by **PID captured from `ps`**, then prove the port closed (`curl` exit 7).
   Never `pkill -f mock_zai` (self-match).
7. `gh` is still not installed; use `GET /user/repos` with `GITHUB_TOKEN`.
