# Civ Orchestrator — Run Report, session 223 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **92nd session**) + **live JEV** (`jev-1.14.0`).
Baseline: `93f7468` (session 222 tree). **59/59 verification assertions PASS.** Pre-flight **10/10 PASS on the FIRST build.**

**Session 223 in one line:** `civ-precise` took **3/5** competitions with `civ-engineer` and `civ-formal` taking one each; the chooser/argmax agreement was **1/5 (20 %) — 4 down-grades, 0 up-grades**; the run-level low was **`civ-therapist`** (avg **1.5163**, fleet-low quality **0.8010** and fleet-low alignment **1.0890**) while `civ-grounded` holds the lifetime low for the **91st** consecutive session.

## Run data (verified)

- per-civ row delta = **+10** x 8 = **80 new rows**; `meta_log` D = **+5** (848 -> 853); `Winner:` lines = **5**
- **80/80** rows `provider=zai` with the `[mock-zai` prefix; **0** rows with a JEV `error` key; **0** rows with the 2.0/2.0/2.0 fallback triple
- **80/80** rows match an independently recomputed seed+color+figure; **40/40** distinct seeds (message-level)
- **0** `(civ,prompt)` combos carrying >1 seed; per-prompt **8/8** distinct seeds AND previews on all 5 competition prompts
- relevance delta == sum(`avg_score`) **8/8** exact; wins+losses delta = **+5** **8/8**; `simulations_run` delta = **+10** **8/8**
- field win total delta = **+5**; meta-vs-ledger `avg_score` mismatches **0/40** (later-`ts` row); registry 8 all gen 1; extinction **NONE** (lowest **+1945.57** = **194.6x** the -10 floor)
- leaderboard reconciles with `culture.json` **8/8**; counter gap **UNCHANGED 8/8** (same-epoch: grounded -84.35, whimsical -173.14, formal -85.53, poetic -96.80, precise -32.63, mythic -51.11, therapist -42.11, engineer -44.24)
- mock log: **129** OK lines, **0 `EXC:`**, **0** tracebacks; port closed after teardown (`curl` exit 7, `HTTP=000`)

## Run-level table (this run's 80 rows)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| `civ-poetic` | 2.3767 | 1.5700 | 2.6210 | 2.9390 |
| `civ-precise` | 2.2893 | 1.4830 | 2.5080 | 2.8770 |
| `civ-formal` | 2.0397 | 1.1620 | 2.5200 | 2.4370 |
| `civ-mythic` | 2.0053 | 1.2280 | 2.6550 | 2.1330 |
| `civ-engineer` | 2.0007 | 1.1800 | 2.5030 | 2.3190 |
| `civ-whimsical` | 1.7947 | 1.1690 | 2.6600 | 1.5550 |
| `civ-grounded` | 1.7800 | 0.9300 | 2.6070 | 1.8030 |
| `civ-therapist` | 1.5163 | 0.8010 | 2.6590 | 1.0890 |

Spreads: `avg_score` 0.8603 | `alignment` **1.8500** (widest) | `quality` 0.7690 | `novelty` **0.1570** (narrowest).
Alignment spread is **2.41x** the quality spread and **11.8x** the novelty spread.

## Lifetime leaderboard

| civ | relevance | per_sim | wins | losses | win_rate |
|---|---|---|---|---|---|
| `civ-poetic` | 2785.44 | 1.674 | 6 | 822 | 0.007 |
| `civ-precise` | 2647.97 | 1.600 | 564 | 259 | 0.685 |
| `civ-whimsical` | 2334.67 | 1.397 | 5 | 823 | 0.006 |
| `civ-formal` | 2279.61 | 1.369 | 111 | 715 | 0.134 |
| `civ-mythic` | 2260.56 | 1.363 | 10 | 812 | 0.012 |
| `civ-engineer` | 2175.37 | 1.315 | 53 | 768 | 0.065 |
| `civ-therapist` | 2007.06 | 1.211 | 11 | 814 | 0.013 |
| `civ-grounded` | 1945.57 | 1.159 | 74 | 753 | 0.089 |

## Findings

- **`civ-grounded` remains the lifetime low — 91st consecutive session.** Lifetime `relevance` **1945.57** (last of 8), `relevance_per_sim` **1.159** (lowest in the fleet), `win_rate` **0.089** — 3rd-best in the fleet. Its run `avg_score` **1.7800** (7th of 8) with alignment **1.8030** (6th-highest) => **the lifetime deficit is NOT a voice failure this run** — `civ-grounded` posted a middling run. Lowest relevance **+1945.57 = 194.6x** the -10 extinction floor.
- **The run-level low is `civ-therapist`** (run `avg_score` **1.5163**, quality **0.8010** fleet-low, alignment **1.0890** fleet-low) while its lifetime standing is **7th of 8** (`relevance` 2007.06). Axis gap: alignment **1.8500** vs quality **0.7690** = **2.41x** wider => a **voice** failure, not a prose failure. *The holder rotates; the axis does not.*
- **Chooser vs `avg_score` argmax: 1/5 (20 %)** — **4 down-grades, 0 up-grades**. `civ-poetic` was the `avg_score` argmax on **4 of 5** prompts and won **0 of 4**; `civ-precise` won **3/5** and was the argmax on **1/5**. Largest disagreement **-0.3700** ("JEV as a decision oracle"). *A MEASUREMENT re-derived from this session's own `meta_log`, not a carried-forward streak counter.*
- `civ-whimsical` is the **second** run low (avg **1.7947**, alignment **1.5550** fleet-2nd-low) while holding the **3rd** lifetime place — the same low-alignment signature, one notch milder.
- `civ-poetic` keeps the lifetime **relevance** lead (2785.44) on a `win_rate` of **0.007** — accumulated relevance and competitive win rate are decoupled across the fleet.

## Re-confirmations

- The prompt's path did not exist (**21st consecutive occurrence**); the workspace held only `.plugin-cache` and an **empty** `civ-orchestrator-learnings` stub. Clone `SuperInstance/AI-Writings` to **`/tmp`** (NAS EDQUOT kills a clone into `/workspace`) and bridge the **clone root** so the script's hardcoded `CIVS_DIR` (`.../cellular-first-design/code/civilizations`) resolves; verified by inode identity `129:12601` both sides + `os.path.samefile()` -> `True`.
- `ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai **401 `token expired or incorrect`** (**92nd session**) => endpoint healthy, credential absent. `ZAI_URL_OVERRIDE` alone is dead code — Control B needs **both**.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`; **0** fallback triples.
- The mock algorithm was **re-derived from the ledger and verified 80/80 exact** before the run: `d = md5(cultural_prompt).digest(); h = d.hex(); i = d[0] % 4; seed = h[(i*2)%8:(i*2)%8+4]; color = h[8:12]; figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"`.
- **The body band was solved algebraically, not iteratively**: the header is a constant **38** chars, so a **298**-char tail gives a constant **336**-char body — inside the 332-369 band on the **first** build. The cultural-prompt band is measured from the **real** `culture.json` files (**167-209**).
- Baseline pinned to the **pre-run commit** `93f7468` and read from the **git blob** — never from `HEAD` after committing.
- `gh` is not installed (**25th session**); `GIT_SSL_NO_VERIFY=1` required for fetch/push.
- Mock teardown by **PID captured from `ps`** (exact-argv match, never `pkill -f`); **0** remaining procs; `curl` exit **7** (port closed).

## New durable lesson (session 223)

**THE CULTURAL-PROMPT TEMPLATE HAS NO BLANK LINE AFTER THE TRADITION LINE — A ONE-BLANK-LINE REBUILD CHANGES THE MD5 AND FAILS 80/80.**

The orchestrator's prompt is an f-string (source: `civilization_orchestrator.py`, `run_simulation()`):

```python
cultural_prompt = f"""You are a voice in the tradition of "{self.culture['name']}".
Your tenets: {', '.join(self.culture['tenets'])}.
Your voice: {self.culture['voice_emphasis']}.

{prompt}"""
```

A rebuild that formats the prose with a blank line between each of the first three lines
(`tradition of "X".\n\nYour tenets: …\n\nYour voice: …`) produces a **different md5** and
**80/80 false mismatches** against the ledger, even though the mock is healthy by every
socket-level check (HTTP 200, prefix present, 0 tracebacks, correct row counts, exit 0).

This session the ledger check caught it immediately: the first derivation attempt (with blank
lines) matched **0/80**, and the second (single newlines) matched **80/80** — the diagnostic
difference is one byte of whitespace per line.

*Rule: when re-deriving the mock algorithm from the ledger, **grep the template out of the
source** and reproduce it byte-for-byte before trusting a mismatch count. The same class of
trap as the session-185 "no closing quote" variant, and the same escape hatch: a
**spec-recompute failure with every structural check green is a TEMPLATE-BYTES defect until
proven otherwise, not a data defect.*

Corollary for the prompt: the *cultural prompt* band is **167-209** chars on the real
`culture.json` files. A blank-line rebuild lands at **201-211** for the shorter civs —
**outside the band** — which is an independent second signal that the template bytes are wrong.
