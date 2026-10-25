# Civ Orchestrator — Run Report, session 212 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **84th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `298647e` (session 211 tree). **All 62 verification assertions PASS.** Pre-flight **10/10 PASS**.

**Session 212 in one line:** `civ-precise` swept **5/5** competitions and held the run's best
`avg_score` (**2.3343**) and the widest alignment lead (**3.0830**); the chooser/argmax
agreement was **2/5 (40 %) — 3 down-grades, 0 up-grades**; the run-level low rotated to
**`civ-therapist`** while `civ-grounded` held the lifetime low for the **81st** consecutive
session.

## Run ledger

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| `civ-precise` | 2.3343 | 1.5490 | 2.3710 | 3.0830 |
| `civ-poetic` | 2.2143 | 1.4780 | 2.4360 | 2.7290 |
| `civ-formal` | 2.0507 | 1.0900 | 2.4730 | 2.5890 |
| `civ-engineer` | 1.9527 | 1.0720 | 2.4300 | 2.3560 |
| `civ-mythic` | 1.8813 | 1.2860 | 2.3310 | 2.0270 |
| `civ-grounded` | 1.8383 | 1.0490 | 2.3610 | 2.1050 |
| `civ-whimsical` | 1.5957 | 0.9300 | 2.4910 | 1.3660 |
| `civ-therapist` | 1.5710 | 0.8260 | 2.4560 | 1.4310 |

Axis spreads: alignment **1.7170** (widest, **2.37x** the quality spread), quality **0.7230**,
novelty **0.1600** (narrowest), `avg_score` **0.7633**.

## Verification (62/62 PASS)

per-civ row delta **+10 x 8 = 80** new rows, `meta_log` **+5** (793 -> 798), `Winner:` **5**,
wins **+5** / losses **+35**, `simulations_run` **+10 x 8**, **0** JEV `error` keys, **0**
2.0/2.0/2.0 fallback triples, **80/80** rows `provider=zai` with the `[mock-zai` prefix,
**80/80** rows match an independently recomputed seed+color+figure, **40** distinct seeds
(message-level), **0** `(civ,prompt)` slots with >1 seed, per-prompt **8/8** distinct seeds
AND previews on all 5 competition prompts, **80/80** distinct `(q,n,a)`, relevance delta ==
sum(`avg_score`) **8/8 exact** (max residual **1.10e-12**), meta-vs-ledger `avg_score`
mismatches **0/40**, counter gap (`culture - ledger`) **unchanged 8/8**, registry 8 all
gen 1, extinction **NONE** (lowest **+1738.40 = 174x** the -10 floor), leaderboard 8 sorted.

## Low-relevance civilizations

- **Lifetime low: `civ-grounded`** — relevance **1738.40**, `relevance_per_sim` **1.108**
  (last of 8) for the **81st** consecutive session, yet lifetime `win_rate` **0.095** is
  3rd-best in the fleet. Its run deficit is **quality** (**1.0490**, 2nd-lowest) on an
  otherwise ordinary alignment (**2.1050**). Lowest relevance is **174x** the -10
  extinction floor: no extinction risk.
- **Run low: `civ-therapist`** — `avg_score` **1.5710**, quality **0.8260** (fleet-low),
  alignment **1.4310** (2nd-lowest), novelty **2.4560** (2nd-highest). The quality gap
  (**0.7230**) is **2.37x** smaller than the alignment gap (**1.7170**), so the deficit is
  again a *voice* failure with a quality floor under it. This is the **18th different run
  low in 18 sessions** — the holder rotates, the axis does not.
- **Also low: `civ-whimsical`** — `avg_score` **1.5957**, alignment **1.3660** (fleet-low),
  quality **0.9300**. It sits **0.0247** above the run low: the two lowest civs are
  separated by less than the run's own `avg_score` spread (**0.7633**), so their ordering
  is **not** robust. Report the pair, not a single rank.

## Durable lessons from this session

1. **THE TWO LOWEST CIVS ARE SEPARATED BY LESS THAN ONE THIRD OF THE RUN'S OWN SPREAD.**
   `civ-therapist` (**1.5710**) and `civ-whimsical` (**1.5957**) differ by **0.0247**
   against a run `avg_score` spread of **0.7633**. A single-run ranking between them is
   noise. *Always print the gap next to the spread.*
2. **A 5/5 SWEEP DID NOT IMPLY CHOOSER AGREEMENT.** `civ-precise` won all 5, but the
   chooser only agreed with the argmax **2/5 (40 %)** — 3 down-grades, 0 up-grades. The
   winner and the agreement rate are independent measurements; a sweep can coexist with
   a poorly-calibrated chooser. *Never infer agreement from the win count.*
3. **THE PRE-FLIGHT ASSERTION FOR "NO LITERAL `seed={}`" HAS AN INVERTED-SENTINEL TRAP.**
   A `literal_seed` flag set to `True` *on find* and asserted `not literal_seed` reported
   a **false FAIL** on a perfectly correct mock: the body contained **0** occurrences of
   `seed=`. The check was wrong, not the server. *Assert on the counted occurrence, not
   on a double-negated flag — and re-derive the fact independently before trusting a
   pre-flight FAIL.* (Pre-flight FAIL on a green component ⇒ verify the component
   directly before touching the code.)
4. **THE NAS MOUNT PRODUCES TRANSIENT `ls` FAILURES ON A VALID SYMLINK BRIDGE.** After
   the run, `ls -la /workspace/repos/.../civilizations/` returned **"No such file or
   directory"** while `ls -la /workspace/repos/` showed the symlink intact and
   `ls` on the clone root worked. A second attempt one minute later resolved cleanly.
   *A single failed `ls` is not evidence of a missing tree — re-read before
   concluding the repo vanished.*

## Environment (durable)

- 84th session with the prompt path absent at start (workspace held only `.plugin-cache`
  and `.skills`). Clone `SuperInstance/AI-Writings` to `/root/ai-writings` (NAS EDQUOT:
  600 G/600 G, 0 bytes free — a 5 MB `dd` into `/workspace` fails and leaves a 0-byte
  stub) and bridge the **clone root** by symlink — verified by inode identity `129:99` on
  both sides plus `os.path.samefile()` -> `True`.
- `ZAI_TOKEN` absent from env and all sandbox secrets; z.ai returns **401** (endpoint
  healthy, credential gap) — **84th session**. `ZAI_URL_OVERRIDE` alone is dead code behind
  the token gate: Control B needs **both**. `TYPESAFEAI_KEY` exported from
  `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`; **0** fallback triples.
- `gh` not installed; `GIT_SSL_NO_VERIFY=1` required for fetch/push; push to the explicit
  token URL and verify with `git ls-remote`.
- Mock teardown by exact-argv match (wrapper **and** server pid), then prove the port
  closed (`curl` exit 7 = refused, `HTTP=000`). Never `pkill -f mock_zai` (self-match).
