# Civ Orchestrator — Run Report, session 218 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **89th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `c9b1592e` (session 217 tree). **All 24 verification assertions PASS.** Pre-flight **10/10 PASS** (first build).

**Session 218 in one line:** `civ-precise` swept **5/5** competitions; the chooser/argmax agreement was
**3/5 (60 %) — 2 down-grades, 0 up-grades**; the run-level low was **`civ-therapist`** (avg
**1.5310**, fleet-low alignment **1.1770**) while `civ-grounded` held the lifetime low for the
**86th** consecutive session.

## Run results (10 new rows per civ: 5 sim phase + 5 competition phase)

| civ | avg_score | quality | novelty | alignment | rank |
|---|---|---|---|---|---|
| civ-precise | 2.4560 | 1.6350 | 2.5960 | 3.1370 | 1/8 |
| civ-poetic | 2.3733 | 1.4980 | 2.6890 | 2.9330 | 2/8 |
| civ-mythic | 2.0420 | 1.2480 | 2.6200 | 2.2580 | 3/8 |
| civ-formal | 2.0250 | 0.9780 | 2.6400 | 2.4570 | 4/8 |
| civ-engineer | 1.9983 | 1.0750 | 2.5730 | 2.3470 | 5/8 |
| civ-whimsical | 1.7913 | 0.8230 | 2.7200 | 1.8310 | 6/8 |
| civ-grounded | 1.6793 | 0.6770 | 2.6650 | 1.6960 | 7/8 |
| civ-therapist | 1.5310 | 0.7110 | 2.7050 | 1.1770 | 8/8 |

Run spreads: avg **0.9250**, quality **0.9580**, novelty **0.1470**, alignment **1.9600**.
The alignment spread is **2.05x** the quality spread and **13.33x** the novelty spread — the
ranking is produced by alignment, not novelty.

## Lifetime leaderboard (cumulative)

| civ | relevance | rel/sim | win_rate | quality | novelty | alignment | rows | rank |
|---|---|---|---|---|---|---|---|---|
| civ-poetic | 2669.70 | 1.6540 | 0.007 | 0.8671 | 2.0110 | 2.1488 | 1651 | 1/8 |
| civ-precise | 2530.37 | 1.5770 | 0.680 | 0.6757 | 1.7938 | 2.2739 | 1621 | 2/8 |
| civ-whimsical | 2250.72 | 1.3880 | 0.006 | 0.6467 | 2.0640 | 1.6074 | 1684 | 3/8 |
| civ-formal | 2174.18 | 1.3460 | 0.137 | 0.5746 | 1.6834 | 1.8332 | 1657 | 4/8 |
| civ-mythic | 2161.98 | 1.3440 | 0.013 | 0.6398 | 1.8876 | 1.5483 | 1629 | 5/8 |
| civ-engineer | 2072.00 | 1.2920 | 0.064 | 0.5714 | 1.7276 | 1.6056 | 1626 | 6/8 |
| civ-therapist | 1931.42 | 1.2020 | 0.014 | 0.5208 | 1.9256 | 1.1993 | 1624 | 7/8 |
| civ-grounded | 1851.31 | 1.1360 | 0.091 | 0.4951 | 1.7524 | 1.2255 | 1672 | 8/8 |

## Low-relevance civilizations (three different axes)

- **Run low — `civ-therapist`**: `avg_score` **1.5310**, 8th of 8, with the fleet-low run
  alignment (**1.1770**) and a near-fleet-low run quality (**0.7110**). Its gap to the next civ
  is **0.1483**, i.e. **16.0 %** of the run spread — the *identity* of the bottom is solid,
  its *ordering* against 2nd place is weak.
- **Lifetime low — `civ-grounded`**: relevance **1851.31**, rel/sim **1.1360**, lifetime avg
  **0.4951** quality, and the fleet-low lifetime quality (**0.4951**). Yet its lifetime `win_rate`
  **0.091** is 3rd-best in the fleet — the "low relevance but competitive" pattern again.
- **Lifetime alignment low — `civ-therapist`** (**1.1993**) — a *third* civ on a *third* axis.

The lifetime lowest **novelty** belongs to `civ-formal` (**1.6834**), not to the run low.

## Chooser vs argmax

| prompt | argmax | winner | verdict |
|---|---|---|---|
| what a cell is | civ-poetic | civ-precise | DOWN-grade |
| bookkeeper's role | civ-precise | civ-precise | AGREE |
| witness log | civ-precise | civ-precise | AGREE |
| ternary values | civ-precise | civ-precise | AGREE |
| JEV as a decision oracle | civ-poetic | civ-precise | DOWN-grade |

Agreement **3/5 (60 %)** — 2 down-grades, 0 up-grades. `civ-poetic` was argmax on **2/5**
prompts and won **0/5**; `civ-precise` was argmax on **3/5** and won **5/5**.

## Verification (24/24 PASS)

- per-civ ledger **+10 × 8 = 80** new rows; `meta_log.jsonl` **+5** (823 -> 828)
- `wins` = pre + times won, `losses` = 5 − times won — **8/8 exact**
- `relevance` Δ = Σ this run's `avg_score` — **8/8 exact** (max residual **8.38e-13**)
- `simulations_run` Δ = **+10** each (5 sim phase + 5 competition rows) — **8/8 exact**
- counter gap **UNCHANGED 8/8** against the **baseline commit** (not `HEAD`) — the cheapest
  merge-integrity check in the series is green
- **80/80** rows match an independently recomputed message md5
- **40** distinct seeds over the 80 new rows; **0** `(civ,prompt)` carrying >1 seed
- **8/8** distinct seeds AND previews on every competition prompt (5/5)
- meta-vs-ledger `avg_score` mismatches **0/40** (later-`ts` row)
- 0 JEV errors, 0 `2.0/2.0/2.0` fallback triples, 0 `EXC:` in the mock log (185 OK lines)
- **80/80** distinct `(q,n,a)`
- extinction risk NONE (threshold −10; the lowest civ sits ~185× above it)
- registry still 8 civs, all generation 1, no new civ dirs

## Two checker bugs found (not data defects)

Both were **assertion** bugs in my own verifier, caught by the corrected re-run:

1. **`simulations_run` Δ is +10, not +5.** `run_simulation()` increments the counter on
   *every* simulation, and the competition phase writes one row per civ per prompt. A civ
   therefore ends the run with 5 sim-phase rows **plus** 5 competition rows, and the counter
   advances by 10 while the *ledger* grows by 10 too. Asserting +5 is wrong.
2. **`losses` Δ is 5 − wins, not a flat +5.** `civilization_competition()` only awards a
   loss to civs that *participated*; a sweep winner records **0** losses and **5** wins. A
   flat "+5 losses" assertion fails on a perfect sweep.

*Rule: derive the expected counter delta from the code path, not from the number of
prompts. The competition phase participates in the same counters as the sim phase.*

## Durable notes

- The workspace was empty again (**9th consecutive** session naming ephemeral paths).
  The upstream was found in **one** call: `GET /search/code?q=civilization_orchestrator+in:path`
  → `SuperInstance/AI-Writings`. `/workspace` is at 100 % NAS quota, so the clone went to
  `/tmp` and the bridge points at the **inner `cellular-first-design`** dir:
  `ln -s /tmp/a-w/cellular-first-design/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`,
  verified with `stat -L -c '%d:%i'` → `129:12610` on both sides and
  `os.path.samefile()` → `True`.
- **THE MOCK'S SEED/COLOUR/FIGURE ALGORITHM WAS RE-DERIVED FROM THE LEDGER AND VERIFIED
  480/480 EXACT**, since the SKILL file describes the *older* `seed=XXXX` header format and
  not the current one. The canonical algorithm is:
  `d = md5(cultural_prompt).digest(); h = d.hex(); i = d[0] % 4;
  seed = h[(i*2)%8:(i*2)%8+4]; color = h[8:12]; figure = h[12:16]/h[16:20]/h[20:24]`.
  The `i = d[0] % 4` step is the part that is easy to miss: `h[0:4]` alone matches only
  ~30 % of rows, and *every* offset in `h[0:8]` looks plausible on a sample.
- **THE CURRENT-GENERATION TAIL IS PER-SESSION, NOT PER-MESSAGE.** The ledger holds exactly
  **3** distinct 163-char tails, and a merged-by-`ts` run-length encoding of the 480
  current-format rows gives `C×80, B×160, A×240` — i.e. **one tail per session** (6 sessions
  detected at 80 rows each), not a per-message rotation. Every civ uses all three across
  sessions. *A tail is a mock configuration for the session, so any one of the three is
  valid; do not look for a per-message selector — there is none.*
- `ZAI_TOKEN` is still absent (**89th session**): z.ai returns **401 `token expired or
  incorrect`** — endpoint healthy, credential missing. Control B is the only provider path.
  `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`; with the alias set, JEV
  returns `jev-1.14.0` and **0** of the 80 new rows is a `2.0/2.0/2.0` fallback.
- Mock teardown: killed by **exact argv match** (2 pids), port proven closed
  (`curl -m 5` → exit 7 / `HTTP=000`).
