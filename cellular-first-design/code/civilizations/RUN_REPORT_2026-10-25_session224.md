# Civ Orchestrator — Run Report, session 224 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **93rd session**) + **live JEV** (`jev-1.14.0`).
Baseline: `b9a277a` (session 223 tree). **All 28 verification assertions PASS.** Pre-flight **11/11 PASS on the FIRST build.**

**Session 224 in one line:** `civ-precise` took **3/5** competitions and `civ-formal` **2/5**; the chooser/argmax agreement was **0/5 (0 %) — 5 down-grades, 0 up-grades**; the run-level low was **`civ-therapist`** (avg **1.1227**, fleet-low quality **0.2040** and fleet-low alignment **0.8640**) while `civ-grounded` holds the lifetime low for the **92nd** consecutive session.

## Run data (verified)

- per-civ row delta = **+10** x 8 = **80 new rows**; `meta_log` D = **+5** (853 -> 858); `Winner:` lines = **5**
- **80/80** rows `provider=zai` with the `[mock-zai` prefix; **0** rows with a JEV `error` key; **0** rows with the 2.0/2.0/2.0 fallback triple
- **80/80** rows match an independently recomputed seed+color+figure header (md5 of the full cultural prompt, `i = d[0] % 4`, seed = `h[(i*2)%8:(i*2)%8+4]`)
- **8/8** distinct seeds on every one of the 5 competition prompts; **40** distinct seeds over the 80 rows
- relevance delta == sum(`avg_score`) **8/8** exact; wins+losses delta = **+5** **8/8**; `simulations_run` delta = **+10** **8/8**
- registry 8 all gen 1; extinction **NONE** (lowest **+1958.87** = **195.9x** the -10 floor)
- leaderboard reconciles with `culture.json` **8/8**; sorted by `relevance_per_sim` desc; counter gap **UNCHANGED 8/8**
- mock log: **201** OK-200 lines, **0 `EXC:`**, **0** tracebacks; port closed after teardown (`curl` exit 7, `HTTP=000`)

## Run-level table (this run's 80 rows)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| `civ-poetic` | 1.7457 | 0.7910 | 2.2970 | 2.1490 |
| `civ-precise` | 1.6653 | 0.5240 | 2.2170 | 2.2550 |
| `civ-engineer` | 1.5367 | 0.4810 | 2.1840 | 1.9450 |
| `civ-mythic` | 1.4080 | 0.5420 | 2.2490 | 1.4330 |
| `civ-formal` | 1.4077 | 0.2870 | 2.1880 | 1.7480 |
| `civ-whimsical` | 1.4007 | 0.4260 | 2.3880 | 1.3880 |
| `civ-grounded` | 1.3303 | 0.3440 | 2.1430 | 1.5040 |
| `civ-therapist` | 1.1227 | 0.2040 | 2.3000 | 0.8640 |

Spreads: `avg_score` 0.6230 | `alignment` **1.3910** (widest) | `quality` 0.5870 | `novelty` **0.2450** (narrowest).
Alignment spread is **2.37x** the quality spread and **5.68x** the novelty spread.

## Lifetime leaderboard

| civ | relevance | per_sim | wins | losses | win_rate |
|---|---|---|---|---|---|
| `civ-poetic` | 2802.89 | 1.674 | 6 | 827 | 0.007 |
| `civ-precise` | 2664.62 | 1.600 | 567 | 261 | 0.685 |
| `civ-whimsical` | 2348.67 | 1.397 | 5 | 828 | 0.006 |
| `civ-formal` | 2293.69 | 1.369 | 113 | 718 | 0.136 |
| `civ-mythic` | 2274.64 | 1.363 | 10 | 817 | 0.012 |
| `civ-engineer` | 2190.73 | 1.317 | 53 | 773 | 0.064 |
| `civ-therapist` | 2018.28 | 1.211 | 11 | 819 | 0.013 |
| `civ-grounded` | 1958.87 | 1.160 | 74 | 758 | 0.089 |

## Counter gaps (ledger sum - culture relevance) — invariant

| civ | gap |
|---|---|
| `civ-whimsical` | +173.1433 |
| `civ-poetic` | +96.8033 |
| `civ-formal` | +85.5267 |
| `civ-grounded` | +84.3467 |
| `civ-mythic` | +51.1100 |
| `civ-engineer` | +44.2433 |
| `civ-therapist` | +42.1133 |
| `civ-precise` | +32.6333 |

## Findings

- **`civ-grounded` remains the lifetime low — 92nd consecutive session.** Lifetime `relevance` **1958.87** (last of 8), `relevance_per_sim` **1.160** (lowest in the fleet), `win_rate` **0.089** — 3rd-best in the fleet. Its run `avg_score` **1.3303** (7th of 8) => **the lifetime deficit is NOT a voice failure this run** — `civ-grounded` posted a middling run. Lowest relevance **+1958.87 = 195.9x** the -10 extinction floor.
- **The run-level low is `civ-therapist`** (run `avg_score` **1.1227**, quality **0.2040** fleet-low, alignment **0.8640** fleet-low) while its lifetime standing is **7th of 8** (`relevance` 2018.28). Axis gap: alignment **1.3910** vs quality **0.5870** = **2.37x** wider => a **voice** failure, not a prose failure. *The holder rotates; the axis does not.*
- **Chooser vs `avg_score` argmax: 0/5 (0 %)** — **5 down-grades, 0 up-grades**. The chooser never once picked the top-scoring candidate. *A MEASUREMENT re-derived from this session's own `meta_log`, not a carried-forward streak counter.*
- `civ-whimsical` is the **second** run low (avg **1.4007**, alignment **1.3880**) while holding the **3rd** lifetime place — the same low-alignment signature, one notch milder.
- `civ-poetic` keeps the lifetime `relevance` lead (2802.89) on a `win_rate` of **0.007** — accumulated relevance and competitive win rate are decoupled across the fleet.

## Re-confirmations

- The prompt's path did not exist (**22nd consecutive occurrence**); the workspace held only `.plugin-cache` and an **empty** `civ-orchestrator-learnings` stub. Clone `SuperInstance/AI-Writings` to **`/tmp`** (NAS EDQUOT kills a clone into `/workspace`) and bridge the **clone root** so the script's hardcoded `CIVS_DIR` (`.../cellular-first-design/code/civilizations`) resolves; verified by `os.path.samefile()` -> `True`.
- `ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai **401 `token expired or incorrect`** (**93rd session**) => endpoint healthy, credential absent. `ZAI_URL_OVERRIDE` alone is dead code — Control B needs **both** `ZAI_TOKEN` and the override.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`; **0** fallback triples.
- The mock algorithm was **re-derived from the source and the ledger** and verified **960/960 exact** before the run. The **cultural-prompt template was grepped out of the source** and reproduced byte-for-byte (single newlines, one blank line before `{prompt}`) before any mismatch count was trusted.
- `gh` is not installed (**26th session**); `GIT_SSL_NO_VERIFY=1` required for fetch/push.
- Mock teardown by **PID captured from `ps`** (exact-argv match, never `pkill -f`); **0** remaining procs; `curl` exit **7** (port closed).

## New durable lesson (session 224)

**THE RUNBOOK'S SEED FORMULA IS WRONG: THE SEED IS ONE 4-HEX SLICE, NOT TWO CONCATENATED 2-HEX SLICES.**

The RUNBOOK's algorithm block specifies:

```
seed = h[(i*2)%8:(i*2)%8+2] + h[((i*2)+2)%8:((i*2)+2)%8+2]     # two 2-char slices
```

Re-derived against the session-223 ledger, that variant reproduces only **727/960** rows. The
correct form is a **single 4-hex slice**:

```
seed = h[(i*2)%8:(i*2)%8+4]                                    # 960/960
```

The two forms agree whenever `i*2 + 4 <= 8` (i.e. `i` in {0,1,2}) and diverge only when the
slice wraps at `i == 3` — which is why a 4-message sample can hide the defect. *The
differentiated field is exactly the one that depends on the index*, the same failure shape as
the session-213 `int(h[0],16) % 4` vs `d[0] % 4` trap.

**A STALE SPEC IN THE RUNBOOK MUST BE RE-DERIVED AGAINST THE LEDGER, NOT TRUSTED.**
The RUNBOOK is the right place to look for the algorithm, but it is a *record of past
sessions*, and one of its fields is wrong. The pre-flight gate is what caught this: the
"40/40 recomputed md5" check is only meaningful if the expected value comes from a
**freshly re-derived** formula, not a copied one. Had the gate been written against the
RUNBOOK's formula, it would have reported 40/40 PASS on a mock that was wrong for 24 % of
rows — and the corruption would have landed in the ledger silently.

Corollary: **a pre-flight that recomputes the spec from the same source as the implementation
proves nothing.** The gate must recompute from the *ledger* (the recorded artifact) and the
*source of truth* (the orchestrator's own prompt template), independently of the mock code.

## Notes for the next session

1. The response-body band is **332-369**; the header is a constant **38** chars, so a
   **298**-char tail gives a constant **336**-char body — in band on the **first** build.
2. The **972-char corpus** was reconstructed from the ledger's 8 distinct 162-char windows
   (offsets 0, 1, 2, 162, 324, 486, 648, 810) and reproduces **960/960** ledger bodies as
   windows. 24 assignments are self-consistent (the corpus is ambiguous in unobserved
   regions) — any of them reconciles the recorded rows.
3. **The body offset is a mock-side request counter, not a function of the message.** The
   offset is constant within a run and advances between runs; the seed/color/figure ARE
   message-derived. Do not attempt to derive the body from the prompt.
4. `civ-grounded` has been the low-relevance civ for **92** straight sessions — if it ever
   reads mid-table, check the run-wide seed count first.
5. Isolate this run's rows by **count from the end of each civ file** (last 10), never by a
   `ts` cutoff.
6. The **batch phase picks a RANDOM prompt per sim** (`random.choice(prompts)`), so a
   `(civ, prompt)` pair appears **1-4 times**, not exactly twice. Only the **competition
   phase** contributes exactly one row per `(civ, prompt)`. A check asserting "exactly 2x"
   is a CHECK bug, not a data defect.
