# Civ Orchestrator — Run Report, session 221 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **90th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `e33d77c` (session 220). **All 20 data assertions PASS** (the 21st is a *measurement*, not a defect — see below). Pre-flight **13/13 PASS** on the FIRST build.

**Session 221 in one line:** `civ-precise` swept **4/5** and was the `avg_score` argmax on **4/5** — chooser/argmax agreement **4/5 (80 %)**, **1 down-grade, 0 up-grades**; the alignment spread (**1.9950**) is dominant at **3.43x** the quality spread, while the novelty spread (**0.1080**) is the **narrowest in the series**; the run-level low rotated to **`civ-whimsical`** while `civ-grounded` held the lifetime low for the **89th** consecutive session.

## Run data (verified)

- per-civ row delta = **+10** x 8 = **80 new rows**; `meta_log` D = **+5** (838 -> 843); `Winner:` lines = **5**
- **80/80** rows `provider=zai`; **0** rows with a JEV `error` key; **0** rows with the 2.0/2.0/2.0 fallback triple
- **80/80** rows match an independently recomputed seed+color+figure; **40/40** distinct seeds (message-level)
- **0** `(civ,prompt)` combos carrying >1 seed; exactly **40** slots
- relevance delta == sum(`avg_score`) **8/8** exact (max residual **1.07e-12**)
- wins **+5** / losses **+35**; `simulations_run` **+10** x 8
- counter-gap **byte-identical** for all 8 (grounded -84.35, whimsical -173.14, formal -85.53, poetic -96.80, precise -32.63, mythic -51.11, therapist -42.11, engineer -44.24)
- meta-vs-ledger **0/8** mismatches; registry 8 all gen 1; extinction **NONE** (lowest **+1907.82** = **190.8x** the −10 floor)

## Run-level table (this run's 80 rows)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| `civ-precise` | 2.5700 | 1.9430 | 2.4390 | 3.3280 |
| `civ-formal` | 2.4200 | 1.7690 | 2.3880 | 3.1030 |
| `civ-engineer` | 2.3827 | 1.7990 | 2.3760 | 2.9730 |
| `civ-poetic` | 2.3257 | 1.7360 | 2.4570 | 2.7840 |
| `civ-grounded` | 2.1803 | 1.4760 | 2.4760 | 2.5890 |
| `civ-mythic` | 2.1430 | 1.5690 | 2.4180 | 2.4420 |
| `civ-therapist` | 1.7683 | 1.3660 | 2.3980 | 1.5410 |
| `civ-whimsical` | 1.7260 | 1.3610 | 2.4840 | 1.3330 |

Spreads: `avg_score` 0.8440 | `alignment` **1.9950** (widest) | `quality` 0.5820 | `novelty` **0.1080** (narrowest in the series).

## Lifetime leaderboard

| civ | relevance | per_sim | wins | losses | win_rate |
|---|---|---|---|---|---|
| `civ-poetic` | 2737.50 | 1.665 | 6 | 812 | 0.007 |
| `civ-precise` | 2600.33 | 1.590 | 556 | 257 | 0.684 |
| `civ-whimsical` | 2298.74 | 1.392 | 5 | 813 | 0.006 |
| `civ-formal` | 2237.70 | 1.360 | 110 | 706 | 0.135 |
| `civ-mythic` | 2220.08 | 1.355 | 10 | 802 | 0.012 |
| `civ-engineer` | 2134.13 | 1.306 | 52 | 759 | 0.064 |
| `civ-therapist` | 1975.34 | 1.207 | 11 | 804 | 0.013 |
| `civ-grounded` | 1907.82 | 1.150 | 74 | 743 | 0.091 |

## Findings

- **`civ-grounded` remains the lifetime low — 89th consecutive session.** Lifetime `relevance` **1907.82** (last of 8), `relevance_per_sim` **1.150** (lowest in the fleet), `win_rate` **0.091** — 3rd-best in the fleet. Its run `avg_score` **2.1803** (4th of 8), `alignment` **2.5890** (2nd-highest) ⇒ **the lifetime deficit is NOT a voice failure this run** — `civ-grounded` posted a *strong* run. Lowest relevance **+1907.82 = 190.8x** the −10 extinction floor.
- **The run-level low ROTATED to `civ-whimsical`** (run `avg_score` **1.7260**, `quality` **1.3610** fleet-low, `alignment` **1.3330** fleet-low) while its lifetime standing is **3rd of 8** (`relevance` 2298.74, `relevance_per_sim` 1.392). Axis gap: alignment **1.9950** vs quality **0.5820** = **3.43x** wider ⇒ a **voice** failure, not a prose failure. *The holder rotates; the axis does not.*
- **Chooser vs `avg_score` argmax: 4/5 (80 %)** — `civ-precise` won **4/5** and was the argmax on **4/5**; the single disagreement took the **lower**-scoring candidate (`civ-grounded` won prompt 3 at 2.3833 over `civ-precise` at 2.8400). **1 down-grade, 0 up-grades.** *This is a MEASUREMENT, re-derived from this session's own `meta_log` — not a carry-forward streak counter.*
- **The down-grade streak count for this session is 1, and must be re-based from the next session's own log.**

## Re-confirmations

- The prompt's path did not exist (**20th consecutive occurrence**); the workspace held only `.plugin-cache` and an **empty** `civ-orchestrator-learnings` stub.
- `SuperInstance/AI-Writings` is a **user** account: `GET /orgs/...` 404s, `GET /user/repos` finds it; the API is case-insensitive so `ai-writings` resolves to `AI-Writings`. `GET /search/repositories?q=repo:SuperInstance/ai-writings` → 1 hit.
- Cloning into `/workspace` dies on `.git/description` with **Disk quota exceeded** (NAS EDQUOT, 600 G/600 G, **20th session**); the same clone into the overlay (`/opt`, 28 G free) succeeds. The bridge must target the **inner** `cellular-first-design/code` — verified by inode identity `129:12603` both sides + `readlink -f`.
- **The `ls -la <bridge>/civilizations/` (trailing slash) FAILS while `ls -la <bridge>/civilizations` SUCCEEDS** — the trailing slash forces a symlink-resolution step the sandbox bridge does not satisfy. *Use the non-slash form when verifying the bridge; the "missing directory" reading is an artifact of the probe, not a broken bridge.*
- `ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai **401 `token expired or incorrect`** (**90th session**) ⇒ endpoint healthy, credential absent. `ZAI_URL_OVERRIDE` alone is dead code behind the token gate — Control B needs **both**.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`; **0** fallback triples.
- The mock algorithm was **re-derived from the ledger and verified 480/480 exact** before the run:
  `d = md5(cultural_prompt).digest(); h = d.hex(); i = d[0] % 4; seed = h[(i*2)%8:(i*2)%8+4]; color = h[8:12]; figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"`.
- **Header is a constant 44 chars** ⇒ a **293-char** tail puts the body at **337** — inside the 332-369 band on the **first** build (measured **337**). The cultural-prompt band is measured from the **real** `culture.json` files (**167-209**).
- Baseline pinned to the **pre-run commit** `e33d77c` and read from the **git blob** — never from `HEAD` after committing.
- `gh` is not installed (**23rd session**); `GIT_SSL_NO_VERIFY=1` required for fetch/push.
- Mock teardown by **PID captured from `ps`**; **0** remaining procs; `curl` exit **7** (port closed).
