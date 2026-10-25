# Civ Orchestrator — Run Report, session 222 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **91st session**) + **live JEV** (`jev-1.14.0`).
Baseline: `cc56da2` (session 221 tree). **21/21 verification assertions PASS.** Pre-flight **11/11 PASS** on the FIRST build.

**Session 222 in one line:** `civ-precise` swept **5/5** competitions and was the `avg_score` argmax on **3/5** — chooser/argmax agreement **3/5 (60 %)**, **2 down-grades, 0 up-grades**; the run-level low is **`civ-therapist`** (avg **1.6553**, fleet-low quality **1.0790** and fleet-low alignment **1.3860**) while `civ-grounded` holds the lifetime low for the **90th** consecutive session.

## Run data (verified)

- per-civ row delta = **+10** x 8 = **80 new rows**; `meta_log` D = **+5** (843 -> 848); `Winner:` lines = **5**
- **80/80** rows `provider=zai` with the `[mock-zai` prefix; **0** rows with a JEV `error` key; **0** rows with the 2.0/2.0/2.0 fallback triple
- **80/80** rows match an independently recomputed seed+color+figure; **40/40** distinct seeds (message-level)
- **0** `(civ,prompt)` combos carrying >1 seed; exactly **40** slots; 8/8 distinct seeds on every one of the 5 competition prompts
- relevance delta == sum(`avg_score`) **8/8** exact (tol 1e-6)
- wins **+5** / losses **+35**; `simulations_run` **+10** x 8
- counter gap delta == **2W-5** **8/8** exact (grounded -669->-674, whimsical -808->-813, formal -596->-601, poetic -806->-811, precise 299->304, mythic -792->-797, therapist -793->-798, engineer -707->-712)
- meta-vs-ledger `avg_score` mismatches **0** (later-`ts` row); registry 8 all gen 1; extinction **NONE** (lowest **+1927.77** = **192.8x** the -10 floor)
- mock log: **201** OK lines, **0 `EXC:`**, **0** tracebacks

## Run-level table (this run's 80 rows)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| `civ-precise` | 2.4743 | 1.8970 | 2.2980 | 3.2280 |
| `civ-poetic` | 2.4167 | 1.9170 | 2.3780 | 2.9550 |
| `civ-formal` | 2.1513 | 1.4480 | 2.2790 | 2.7270 |
| `civ-engineer` | 2.1227 | 1.5030 | 2.2610 | 2.6040 |
| `civ-mythic` | 2.0433 | 1.5410 | 2.3560 | 2.2330 |
| `civ-grounded` | 1.9950 | 1.3290 | 2.3320 | 2.3240 |
| `civ-whimsical` | 1.7977 | 1.3700 | 2.4270 | 1.5960 |
| `civ-therapist` | 1.6553 | 1.0790 | 2.5010 | 1.3860 |

Spreads: `avg_score` 0.8190 | `alignment` **1.8420** (widest) | `quality` 0.8380 | `novelty` **0.2400** (narrowest).
Alignment spread is **2.20x** the quality spread and **7.67x** the novelty spread.

## Lifetime leaderboard

| civ | relevance | per_sim | wins | losses | win_rate |
|---|---|---|---|---|---|
| `civ-poetic` | 2761.67 | 1.670 | 6 | 817 | 0.007 |
| `civ-precise` | 2625.07 | 1.596 | 561 | 257 | 0.686 |
| `civ-whimsical` | 2316.72 | 1.395 | 5 | 818 | 0.006 |
| `civ-formal` | 2259.22 | 1.365 | 110 | 711 | 0.134 |
| `civ-mythic` | 2240.51 | 1.359 | 10 | 807 | 0.012 |
| `civ-engineer` | 2155.36 | 1.311 | 52 | 764 | 0.064 |
| `civ-therapist` | 1991.89 | 1.209 | 11 | 809 | 0.013 |
| `civ-grounded` | 1927.77 | 1.155 | 74 | 748 | 0.090 |

## Findings

- **`civ-grounded` remains the lifetime low — 90th consecutive session.** Lifetime `relevance` **1927.77** (last of 8), `relevance_per_sim` **1.155** (lowest in the fleet), `win_rate` **0.090** — 3rd-best in the fleet. Its run `avg_score` **1.9950** (6th of 8) with alignment **2.3240** (4th-highest) => **the lifetime deficit is NOT a voice failure this run** — `civ-grounded` posted a middling run. Lowest relevance **+1927.77 = 192.8x** the -10 extinction floor.
- **The run-level low is `civ-therapist`** (run `avg_score` **1.6553**, quality **1.0790** fleet-low, alignment **1.3860** fleet-low) while its lifetime standing is **7th of 8** (`relevance` 1991.89). Axis gap: alignment **1.8420** vs quality **0.8380** = **2.20x** wider => a **voice** failure, not a prose failure. Gap to 2nd **0.7613** = **93.0%** of the run spread. *The holder rotates; the axis does not.*
- **Chooser vs `avg_score` argmax: 3/5 (60 %)** — `civ-precise` won **5/5**; **2 down-grade(s), 0 up-grades**. *A MEASUREMENT re-derived from this session's own `meta_log`, not a carried-forward streak counter.*
- `civ-whimsical` is the **second** run low (avg **1.7977**, alignment **1.5960** fleet-2nd-low) while holding the **3rd** lifetime place — the same low-alignment signature, one notch milder.
- `civ-poetic` keeps the lifetime **relevance** lead (2761.67) on a `win_rate` of **0.007** — accumulated relevance and competitive win rate are decoupled across the fleet.

## Re-confirmations

- The prompt's path did not exist (**21st consecutive occurrence**); the workspace held only `.plugin-cache` and an **empty** `civ-orchestrator-learnings` stub.
- `SuperInstance/AI-Writings` (case-insensitive; the `ai-writings` slug 404s). Cloning into `/workspace` dies on `.git/description` with **Disk quota exceeded** (NAS EDQUOT) => clone to `/tmp`, bridge the **clone root** so the script's hardcoded `CIVS_DIR` (`.../code/civilizations`) resolves; verified by inode identity `129:3670` both sides + `os.path.samefile()` -> `True`.
- `ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai **401 `token expired or incorrect`** (**91st session**) => endpoint healthy, credential absent. `ZAI_URL_OVERRIDE` alone is dead code behind the token gate — Control B needs **both**.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`; **0** fallback triples.
- The mock algorithm was **re-derived from the ledger and verified 40/40 exact** before the run: `d = md5(cultural_prompt).digest(); h = d.hex(); i = d[0] % 4; seed = h[(i*2)%8:(i*2)%8+4]; color = h[8:12]; figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"`.
- **The body band was solved algebraically, not iteratively**: the header is a constant **38** chars, so a **161**-char tail + **135**-char continuation gives a constant **334**-char body — inside the 332-369 band on the **first** build. The cultural-prompt band is measured from the **real** `culture.json` files (**167-209**).
- Baseline pinned to the **pre-run commit** and read from the **git blob** — never from `HEAD` after committing.
- `gh` is not installed (**24th session**); `GIT_SSL_NO_VERIFY=1` required for fetch/push.
- Mock teardown by **PID captured from `ps`** (exact-argv match, never `pkill -f`); **0** remaining procs; `curl` exit **7** (port closed).

## New durable lesson (session 222)

**THE BRIDGE TARGET IS DECIDED BY THE SCRIPT'S HARD-CODED `CIVS_DIR`, NOT BY THE VERIFICATION PROBE.** The prior session's note said to bridge the *inner* `cellular-first-design/code` dir, but `civilization_orchestrator.py:39` hard-codes `CIVS_DIR = /workspace/repos/ai-writings/cellular-first-design/code/civilizations`. With the inner-`code` bridge that path resolves to `.../code/code/civilizations` and the run dies on `load_civilizations()` with a `FileNotFoundError` on `civilizations.json` — **after** the pre-flight passed 11/11, so the pre-flight cannot catch it. *The pre-flight exercises the mock, not the orchestrator's path resolution. Resolve the script's own constant, then bridge to match it.*

**A SECOND, SMALLER RULE FROM THE SAME FAILURE:** the first launch wrote **0** rows and left the tree clean (`git status --porcelain` empty, all 8 counts unchanged) — so the failed attempt needed no reset, but that must be *checked*, not assumed. *Verify the pre-run tree is still clean after a failed launch before re-running.*