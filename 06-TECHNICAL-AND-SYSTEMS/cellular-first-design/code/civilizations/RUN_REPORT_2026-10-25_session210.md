# Civ Orchestrator — Run Report, session 210 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **82nd session**) + **live JEV** (`jev-1.14.0`).
Baseline: `a6d1dfc` (session 209 tree). **All 30 verification assertions PASS.** Pre-flight **13/13 PASS**.

**Session 210 in one line:** `civ-precise` took **2/5** competitions and held the run's best
`avg_score` (**2.1113**) and the widest alignment lead (**2.8190**); the chooser/argmax
agreement fell to **2/5 (40 %) — 3 down-grades, 0 up-grades**; the run-level low rotated to
**`civ-mythic`** while `civ-grounded` held the lifetime low for the **79th** consecutive
session.

## Run ledger

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| `civ-grounded` | 1.4953 | 0.9000 | 1.9780 | 1.6080 |
| `civ-whimsical` | 1.1923 | 0.6440 | 2.2440 | 0.6890 |
| `civ-formal` | 1.7193 | 0.9530 | 2.0400 | 2.1650 |
| `civ-poetic` | 1.4827 | 1.0630 | 2.1330 | 1.2520 |
| `civ-precise` | 2.1113 | 1.3940 | 2.1210 | 2.8190 |
| `civ-mythic` | 0.9737 | 0.5740 | 2.0050 | 0.3420 |
| `civ-therapist` | 1.0287 | 0.6060 | 2.0430 | 0.4370 |
| `civ-engineer` | 1.8140 | 1.0170 | 2.0170 | 2.4080 |

Axis spreads: alignment **2.4770** (widest, 3.02x the quality spread), quality **0.8200**,
novelty **0.2660** (narrowest), `avg_score` **1.1377**.

## Verification (30/30 PASS)

per-civ row delta **+10 x 8 = 80** new rows, `meta_log` **+5** (783 -> 788), `Winner:` **5**,
wins **+5** / losses **+35**, `simulations_run` **+10 x 8**, **0** JEV `error` keys, **0**
2.0/2.0/2.0 fallback triples, **80/80** rows `provider=zai` with the `[mock-zai` prefix,
**80/80** rows match an independently recomputed seed+color+figure, **40/40** distinct seeds
(message-level), **0** `(civ,prompt)` slots with >1 seed, per-prompt **8/8** distinct seeds
AND previews on all 5 competition prompts, **80/80** distinct `(q,n,a)`, relevance delta ==
sum(`avg_score`) **8/8 exact** (max residual **6.15e-13**), counter gap
(`culture - ledger`) **unchanged 8/8** (`civ-grounded` -84.3467 -> -84.3467), registry 8 all
gen 1, extinction **NONE** (lowest **+1699.53 = 170x** the -10 floor), leaderboard 8 sorted.

## Low-relevance civilizations

- **Lifetime low: `civ-grounded`** — relevance **1699.53**, `relevance_per_sim` **1.097**
  (last of 8) for the **79th** consecutive session, yet lifetime `win_rate` **0.094** is
  3rd-best in the fleet. Its run deficit is **novelty** (**1.9780**, the fleet's lowest),
  not alignment — a *content* gap this session, the inverse of the usual voice gap.
  Lowest relevance is **170x** the -10 extinction floor: no extinction risk.
- **Run low: `civ-mythic`** — `avg_score` **0.9737**, alignment **0.3420**, quality
  **0.5740**. The **alignment** gap (**2.4770**) is **3.02x** the quality gap (**0.8200**),
  so the deficit is again a *voice* failure, not a prose failure. This is the **16th
  different run low in 16 sessions** — the holder rotates, the axis does not.

## Durable lessons from this session

1. **THE FIGURE FIELD IS 18 CHARS OF THREE 5-CHAR COMPONENTS, SPACE-JOINED, AND THE
   COLOUR IS 6 HEX — NOT 4.** The header `[mock-zai <4-hex>] #<6-hex> <figure>. ` is a
   **constant 44 chars** only when the colour is padded to 6 and the figure is
   `" ".join(3 components ljust to 5).ljust(18, "0")`. The naive reading (colour = `h[8:12]`,
   4 hex) yields a **42-char** header and breaks the band arithmetic. The pre-flight's
   recompute checks are what surfaced it: checks 5 and 6 failed on the FIRST build while
   the length band still passed. *A band check catches variance, not shape — assert the
   recomputed field values, not just the length.*
2. **AN `ljust(18)` ON A JOINED FIGURE PUTS THE PAD INSIDE THE LAST COMPONENT.**
   `"/".join(3 x 5-char)` is 17 chars, so `ljust(18)` yields `.../09b800` — a **6-char**
   last component that looks like a 6-hex field. The components must be padded *before*
   the join, and the field total accounted for separately. *A trailing pad on a delimited
   field changes the last field's width; check the field count, not just the total.*
3. **A GREEDY FIGURE REGEX SWALLOWS THE TAIL.** With the figure space-joined, `(.+)\. `
   runs past the header into the prose (the tail contains `". "`), and `(.+?)\. ` stops at
   the first component. The bounded pattern
   `([0-9a-f]{5} [0-9a-f]{5} [0-9a-f]{6})\. ` is the only one that matches. *When the
   field contains a space, bind its exact shape rather than a wildcard.*
4. **THE PRE-FLIGHT IS WORTH THE REBUILD — IT CAUGHT 2 DEFECTS THE BAND DID NOT.**
   The body length was in band (345) while two of thirteen checks failed. Pre-flight
   cost one rebuild cycle; a bad mock would have produced 80 rows that *looked* clean.
5. **A 40 % CHOOSER/ARGMAX AGREEMENT IS 3 DOWN-GRADES, NOT A DEFECT.** All three
   disagreements took the **lower**-scoring candidate (1.51 vs 2.15; 1.85 vs 2.07;
   1.80 vs 2.23). The down-grade streak is **3** and must be re-based from this
   session's own data. *Never treat `win_rate` as a quality metric.*

## Environment (durable)

- 82nd session with the prompt path absent at start (workspace held only `.plugin-cache`).
  Clone `SuperInstance/AI-Writings` to `/tmp` (NAS EDQUOT: 600 G/600 G, 0 bytes free — a
  20 MB `dd` into `/workspace` fails and leaves a 0-byte stub) and bridge the **inner**
  `cellular-first-design/code` by symlink — verified by inode identity `129:10424` on both
  sides plus `os.path.samefile()` -> `True`.
- `ZAI_TOKEN` absent from env and all sandbox secrets; z.ai returns **401** (endpoint
  healthy, credential gap) — **82nd session**. `ZAI_URL_OVERRIDE` alone is dead code behind
  the token gate: Control B needs **both**. `TYPESAFEAI_KEY` exported from
  `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`; **0** fallback triples.
- `gh` not installed; `GIT_SSL_NO_VERIFY=1` required for fetch/push; push to the explicit
  token URL and verify with `git ls-remote`.
- Mock teardown by exact-argv match (wrapper **and** server pid), then prove the port
  closed (`curl` exit 7 = refused). Never `pkill -f mock_zai` (self-match).
