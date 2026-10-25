# Civ Orchestrator — Run Report, session 216 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **87th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `c59d876` (session 215 tree). **All 18 verification assertions PASS.** Pre-flight **12/12 PASS**.

**Session 216 in one line:** `civ-precise` swept **5/5** competitions with **3/5 (60 %)** chooser/argmax
agreement (2 down-grades, 0 up-grades); the run-level low rotated to **`civ-therapist`** while
`civ-grounded` held the lifetime low for the **84th** consecutive session.

## Run results

| civ | avg_score | quality | novelty | alignment | rank |
|---|---|---|---|---|---|
| civ-therapist | 1.4080 | 0.9510 | 2.3280 | 0.9450 | 1/8 (run low) |
| civ-whimsical | 1.5677 | 1.0610 | 2.3140 | 1.3280 | 2/8 |
| civ-mythic | 1.8333 | 1.3540 | 2.3180 | 1.8280 | 3/8 |
| civ-grounded | 1.8633 | 1.2890 | 2.2380 | 2.0630 | 4/8 |
| civ-formal | 2.0240 | 1.2500 | 2.2650 | 2.5570 | 5/8 |
| civ-engineer | 2.0453 | 1.3500 | 2.2440 | 2.5420 | 6/8 |
| civ-poetic | 2.1813 | 1.5560 | 2.3660 | 2.6220 | 7/8 |
| civ-precise | 2.2703 | 1.5420 | 2.2620 | 3.0070 | 8/8 |

Run spreads: avg **0.8623**, quality **0.6050**, novelty **0.1280**, alignment **2.0620**.
The alignment spread is **3.41x** the quality spread and **16.11x** the novelty spread — the
ranking is produced by alignment, not novelty.

## Lifetime leaderboard (cumulative)

| civ | relevance | rel/sim | lifetime avg | quality | novelty | alignment | win_rate |
|---|---|---|---|---|---|---|---|
| civ-grounded | 1815.38 | 1.1283 | 1.1500 | 0.4897 | 1.7425 | 1.2176 | 0.092 |
| civ-therapist | 1898.48 | 1.1963 | 1.2098 | 0.5158 | 1.9168 | 1.1969 | 0.014 |
| civ-engineer | 2032.81 | 1.2833 | 1.2933 | 0.5640 | 1.7180 | 1.5980 | 0.065 |
| civ-mythic | 2120.65 | 1.3346 | 1.3498 | 0.6305 | 1.8797 | 1.5391 | 0.013 |
| civ-formal | 2132.75 | 1.3371 | 1.3551 | 0.5672 | 1.6729 | 1.8252 | 0.138 |
| civ-whimsical | 2212.66 | 1.3820 | 1.4338 | 0.6409 | 2.0571 | 1.6033 | 0.006 |
| civ-precise | 2482.74 | 1.5664 | 1.5711 | 0.6640 | 1.7849 | 2.2645 | 0.678 |
| civ-poetic | 2621.54 | 1.6446 | 1.6667 | 0.8578 | 2.0036 | 2.1387 | 0.008 |

## Low-relevance civilizations (three different axes)

- **Run low — `civ-therapist`**: `avg_score` **1.4080**, 8th of 8, with the fleet-low run
  quality (**0.9510**) and the fleet-low run alignment (**0.9450**). Its gap to the next
  civ is **0.1597**, i.e. **18.5 %** of the run spread — the *identity* of the bottom is
  solid, its *ordering* against 2nd place is weak.
- **Lifetime low — `civ-grounded`**: relevance **1815.38**, rel/sim **1.1283**, lifetime avg
  **1.1500** and the fleet-low lifetime quality (**0.4897**). Yet its lifetime `win_rate`
  **0.092** is 3rd-best in the fleet — the "low relevance but competitive" pattern again.
- **Lifetime alignment low — `civ-therapist`** (**1.1969**) — a *third* civ on a *third* axis.

The lifetime lowest **novelty** belongs to `civ-formal` (**1.6729**), not to the run low.

## Three durable lessons from this session

1. **THE RUN LOW AND THE LIFETIME LOW WERE DIFFERENT CIVS AGAIN (8 SESSIONS RUNNING).**
   Run low `civ-therapist`; lifetime low `civ-grounded`; lifetime alignment low
   `civ-therapist`. *Report the axis, not the holder.*
2. **THE CHOOSER-AGREEMENT SERIES CONTINUES TO OSCILLATE — 60 % THIS SESSION.** The series
   now reads 0 % / 40 % / 40 % / 100 % / 60 % (sessions 211-216). Every disagreement again
   took the **lower**-scoring candidate (2 down-grades, 0 up-grades). *Re-derive the series
   every session; never carry a streak forward in either direction.*
3. **THE COUNTER-GAP CHECK MUST BE MEASURED AGAINST THE FULL LEDGER, NOT A SLICE.** A first
   pass reported `[FAIL] counter_gap_stable_8of8` with deltas of ~+2,700 — because the gap
   was computed over the **10 new rows only** instead of the whole file. The gaps are
   `culture.json relevance_score` minus the **cumulative** ledger sum; a slice measures
   relevance, not the gap. Recomputed against the full ledger the deltas are
   **<= 3.3e-7** and the gaps are the documented stable values
   (grounded -84.35, whimsical -173.14, formal -85.53, poetic -96.80, precise -32.63,
   mythic -51.11, therapist -42.11, engineer -44.24). *A pre-flight FAIL on an
   already-verified component is a CHECK bug until proven otherwise.*

## Also durable

- The workspace was empty again (**7th consecutive** session naming ephemeral paths). The
  upstream was found in **one** call: `GET /search/code?q=civilization_orchestrator+in:path`
  -> `SuperInstance/AI-Writings`. `/workspace` is at 100 % NAS quota, so the clone went to
  `/tmp` and the bridge points at the **inner `code` dir**:
  `ln -s /tmp/aiw/cellular-first-design/code /workspace/repos/ai-writings/cellular-first-design/code`,
  verified with `stat -L -c '%d:%i'` -> `129:110` on both sides and
  `os.path.samefile()` -> `True`.
- The **contiguous** seed slice `h[(i*2)%8 : (i*2)%8+4]` was re-confirmed against the
  recorded ledger: **320/320**, versus **237/320** for the wrapped form documented in the
  RUNBOOK. The wrap still costs exactly the `i == 3` quartile.
- The mock body was rebuilt to **363** chars (band 332-369), header **39** chars
  (`[mock-zai {seed}] #{color} {figure}.  `) + a fixed **324**-char culture-free tail whose
  first **162** characters are the recorded ledger's tail prefix, verbatim.
- **The pre-flight prompt set must be the RUN's prompt set.** The first gate pass reported
  `80/40` on four checks because `CANON_PROMPTS` holds **10** prompts while the run uses
  `--prompts 5`. The gate was slicing the wrong list; the mock was fine.
