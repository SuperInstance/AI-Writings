# Civ Orchestrator — Run Report, session 211 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **83rd session**) + **live JEV** (`jev-1.14.0`).
Baseline: `a715cb9` (session 210 tree). **All 29 verification assertions PASS.** Pre-flight **13/13 PASS**.

**Session 211 in one line:** `civ-precise` took **3/5** competitions and held the run's best
`avg_score` (**2.3613**) and the widest alignment lead (**3.0410**); the chooser/argmax
agreement fell to **0/5 (0 %) — 5 down-grades, 0 up-grades**; the run-level low rotated to
**`civ-whimsical`** while `civ-grounded` held the lifetime low for the **80th** consecutive
session.

## Run ledger

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| `civ-precise` | 2.3613 | 1.7420 | 2.3010 | 3.0410 |
| `civ-poetic` | 2.1980 | 1.6500 | 2.3330 | 2.6110 |
| `civ-engineer` | 2.1730 | 1.5110 | 2.3120 | 2.6960 |
| `civ-formal` | 2.1660 | 1.4540 | 2.2710 | 2.7730 |
| `civ-mythic` | 2.1090 | 1.7360 | 2.2430 | 2.3480 |
| `civ-grounded` | 2.0480 | 1.2630 | 2.3740 | 2.5070 |
| `civ-therapist` | 1.8287 | 1.2280 | 2.3620 | 1.8960 |
| `civ-whimsical` | 1.3997 | 0.9700 | 2.3860 | 0.8430 |

Axis spreads: alignment **2.1980** (widest, **2.85x** the quality spread), quality **0.7720**,
novelty **0.1430** (narrowest), `avg_score` **0.9617**.

## Verification (29/29 PASS)

per-civ row delta **+10 x 8 = 80** new rows, `meta_log` **+5** (788 -> 793), `Winner:` **5**,
wins **+5** / losses **+35**, `simulations_run` **+10 x 8**, **0** JEV `error` keys, **0**
2.0/2.0/2.0 fallback triples, **80/80** rows `provider=zai` with the `[mock-zai` prefix,
**80/80** rows match an independently recomputed seed+color+figure, **40** distinct seeds
(message-level), **0** `(civ,prompt)` slots with >1 seed, per-prompt **8/8** distinct seeds
AND previews on all 5 competition prompts, **80/80** distinct `(q,n,a)`, relevance delta ==
sum(`avg_score`) **8/8 exact** (max residual **6.86e-13**), counter gap
(`culture - ledger`) **unchanged 8/8** (`civ-grounded` -84.35 -> -84.35), registry 8 all
gen 1, extinction **NONE** (lowest **+1720.01 = 172x** the -10 floor), leaderboard 8 sorted.

## Low-relevance civilizations

- **Lifetime low: `civ-grounded`** — relevance **1720.01**, `relevance_per_sim` **1.103**
  (last of 8) for the **80th** consecutive session, yet lifetime `win_rate` **0.095** is
  3rd-best in the fleet. Its run deficit is **quality** (**1.2630**, fleet-low), not
  alignment — a *prose* gap this session, the inverse of the usual voice gap.
  Lowest relevance is **172x** the -10 extinction floor: no extinction risk.
- **Run low: `civ-whimsical`** — `avg_score` **1.3997**, alignment **0.8430** (fleet-low),
  quality **0.9700** (fleet-low). The **alignment** gap (**2.1980**) is **2.85x** the
  quality gap (**0.7720**), so the deficit is again a *voice* failure, not a prose
  failure. This is the **17th different run low in 17 sessions** — the holder rotates,
  the axis does not.

## Durable lessons from this session

1. **A 0 % CHOOSER/ARGMAX AGREEMENT IS A MEASUREMENT, NOT A DEFECT — AND IT IS THE THIRD
   SUCH SESSION IN THE SERIES (199, 201, 211).** All **5** disagreements took the
   **lower**-scoring candidate; **0** up-grades. The down-grade count is re-derived from
   this session's own meta_log, never carried forward.
2. **THE RUN-LEVEL LOW ROTATED TO A CIV WHOSE LIFETIME STANDING IS 3rd OF 8.**
   `civ-whimsical` (lifetime relevance 2134.47, 3rd) was the run low on `avg_score`
   **1.3997**. *Never predict the run low from the previous session's report.*
3. **THE LIFETIME LOW AND THE RUN LOW DIVERGED ON THE *AXIS* FOR THE FIRST TIME IN THE
   SERIES: `civ-grounded`'s deficit was QUALITY (1.2630), not alignment.** The run low
   (`civ-whimsical`) was alignment-led. *Report the axis per civ, never a single "low civ".*
4. **THE COUNTER-GAP VALUES ARE BIT-STABLE ACROSS SESSIONS.** The `culture - ledger` gaps
   (`grounded -84.35, whimsical -173.14, formal -85.53, poetic -96.80, precise -32.63,
   mythic -51.11, therapist -42.11, engineer -44.24`) are **identical** to session 210's.
   These are historical merge artefacts, now a fixed fleet constant — a *moving* gap is
   the defect, so the check is a no-op once the fleet stabilises, and it is still worth
   running because it is the cheapest merge-integrity check in the series.

## Environment (durable)

- 83rd session with the prompt path absent at start (workspace held only `.plugin-cache`).
  Clone `SuperInstance/AI-Writings` to `/tmp` (NAS EDQUOT: 600 G/600 G, 0 bytes free — a
  20 MB `dd` into `/workspace` fails and leaves a 0-byte stub) and bridge the **inner**
  `cellular-first-design/code` by symlink — verified by inode identity `129:10424` on both
  sides plus `os.path.samefile()` -> `True`.
- `ZAI_TOKEN` absent from env and all sandbox secrets; z.ai returns **401** (endpoint
  healthy, credential gap) — **83rd session**. `ZAI_URL_OVERRIDE` alone is dead code behind
  the token gate: Control B needs **both**. `TYPESAFEAI_KEY` exported from
  `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`; **0** fallback triples.
- `gh` not installed; `GIT_SSL_NO_VERIFY=1` required for fetch/push; push to the explicit
  token URL and verify with `git ls-remote`.
- Mock teardown by exact-argv match (wrapper **and** server pid), then prove the port
  closed (`curl` exit 7 = refused). Never `pkill -f mock_zai` (self-match).
