# Civilization Orchestrator — Session 258 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Fleet: 8 civs. Provider: **Control B mock** (z.ai credential gap, **115th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `22bb1f9`. **Pre-flight gate: 40/40 PASS, exit 0.** **Run verification: 45 PASS / 0 FAIL.**

## Environment notes

- **Task path absent.** `/workspace/repos/ai-writings/...` did not exist (**19th consecutive occurrence**).
  The workspace held only `.plugin-cache`. A direct clone into `/workspace` fails with
  `close error: Disk quota exceeded` (NAS EDQUOT) — **25th session**. Cloned to the overlay at
  `/tmp/work/ai-writings` and bridged the chain with a symlink
  `/workspace/repos/ai-writings -> /tmp/work/ai-writings`.
  Bridge verified with `os.path.samefile()` -> `True`.
- **Bridge target must be the CLONE ROOT, not the nested `cellular-first-design` dir.** The script's
  hardcoded `CIVS_DIR` is `.../cellular-first-design/code/civilizations`. Symlinking the *nested* dir
  produces a doubled path and `REGISTRY.read_text()` raises `FileNotFoundError`. Link the clone root.
  Symlink creation also needs the parent dir to exist first — `ln -sfn` into a missing
  `/workspace/repos/ai-writings` silently no-ops, so link in two steps (`mkdir` then `ln -s`).
- **z.ai live probe: HTTP 401** `token expired or incorrect` => endpoint healthy, credential absent.
  `ZAI_TOKEN` unset in env. Control B mock used with **both** `ZAI_TOKEN` (the gate in
  `call_provider`) **and** `ZAI_URL_OVERRIDE` (the destination); the override alone is dead code.
- **JEV live**: `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN` before the run. Direct probe of
  `https://api.typesafe.ai/v1/systemone` -> **HTTP 200**, `{"model":"jev-1.14.0", …}`, real score
  `0.96`, confidence `0.46`. Without the alias `jev_score` falls through to the `2.0/2.0/2.0` fallback.
- **Mock teardown by exact PID** (375), then proved the port closed
  (`curl` exit 7, `HTTP=000`, 0 processes left). Never `pkill -f mock_zai` (self-match).
- `gh` not installed (**21st session**) — used `GET /user/repos` with `GITHUB_TOKEN`.
  Upstream is **`SuperInstance/AI-Writings`**; the `ai-writings/...` slug 404s.
- Tool timeout 30 s < orchestrator run ~30 s => detached launch with stdout redirected
  **and** `< /dev/null`, then poll. Python buffers stdout — the log looks empty mid-run.

## Pre-flight gate — 40/40 PASS, exit 0

40/40 requests 200, 40/40 distinct previews, 40/40 distinct seeds, 40/40 distinct seed-tuples,
all bodies **349 chars** (inside the 332-369 band), 38+162=200 geometry holds, 149-char
continuation, 5 distinct seeds per civ, 8 distinct seeds per prompt.

**Mock algorithm validated non-circularly**: the seed/colour/figure recompute was re-derived
against the **pre-existing** ledger (the last 400 recognizable historical rows per civ, *not* this
run's rows) — **3200/3200 exact matches**, 0 mismatches. The committed `tools/mock_zai.py`
matches byte-for-byte.

## Ledger delta

- **+10 rows per civ, +80 total**; `meta_log` **1023 -> 1028** (+5); **18** files changed.
- Every new row carries the documented **9 keys** (`ts, civ, civ_name, provider, params, prompt,
  scores, avg_score, content_preview`); preview length **200** on every row; all 80 rows parse as
  JSON; **0 key/shape violations**.
- **JEV was live on all 80 rows**: 0 `error` fields, **0** `2.0/2.0/2.0` fallback triples,
  0 zero-confidence rows, confidence range **0.24 - 0.87**, **80/80 distinct score triples**.
- Prompt draw across the 80 new rows: ternary values 19, witness log 17, what a cell is 15,
  bookkeeper 15, JEV oracle 14.
- **80/80** rows' seed+colour+figure independently recomputed **exact**; **0** `(civ,prompt)`
  combos carrying more than one seed.

### Counter reconciliation — 8/8 OK

The sim phase gives every civ +5 sims; the competition phase gives every civ **5 more sims**
(each competition calls `run_simulation` again) plus exactly one W or L. So **dSims = 10** and
**dW + dL = 5** for all 8 civs. Relevance deltas match the sum of the new `avg_score` values to
the last decimal on all 8 ledgers. **All diffed against the pristine git blob**, not a re-read.

| civ | dW | dL | dSims | sum(new avg) | dRelevance | resid |
|---|---|---|---|---|---|---|
| civ-grounded | 0 | 5 | 10 | 15.1633 | 15.1633 | 0.0000 |
| civ-whimsical | 0 | 5 | 10 | 15.6167 | 15.6167 | -0.0000 |
| civ-formal | 0 | 5 | 10 | 17.8300 | 17.8300 | 0.0000 |
| civ-poetic | 0 | 5 | 10 | 20.0900 | 20.0900 | 0.0000 |
| civ-precise | 5 | 0 | 10 | 19.2700 | 19.2700 | -0.0000 |
| civ-mythic | 0 | 5 | 10 | 15.4600 | 15.4600 | -0.0000 |
| civ-therapist | 0 | 5 | 10 | 12.5600 | 12.5600 | -0.0000 |
| civ-engineer | 0 | 5 | 10 | 16.9600 | 16.9600 | 0.0000 |

**Meta/ledger W-L reconciliation 8/8 exact** — `meta_log` records `civ-precise` as winner on all 5
prompts, and `civ-precise` gained exactly 5 wins and 0 losses; every other civ gained 0 W and 5 L.

## Run-level standings (10 sims per civ)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | 2.0090 | 1.1600 | 2.4520 | 2.4150 |
| civ-precise | 1.9270 | 0.8580 | 2.2950 | 2.6280 |
| civ-formal | 1.7830 | 0.8300 | 2.2180 | 2.3010 |
| civ-engineer | 1.6960 | 0.6900 | 2.2930 | 2.1050 |
| civ-whimsical | 1.5617 | 0.7270 | 2.4670 | 1.4910 |
| civ-mythic | 1.5460 | 0.8110 | 2.4010 | 1.4260 |
| civ-grounded | 1.5163 | 0.6310 | 2.2580 | 1.6600 |
| **civ-therapist** | **1.2560** | 0.6520 | 2.3060 | **0.8100** |

**Run low — `civ-therapist`** (avg 1.2560): fleet-low **alignment** 0.8100, quality 0.6520 is
2nd-lowest, novelty 2.3060 is mid-pack. Alignment spread 1.8180 = **2.4x** the avg spread
=> *voice* failure, not prose failure. Gap to the next civ (civ-grounded, 1.5163) is **0.2603 =
34.6 %** of the run spread 0.7530 — a wide, unambiguous gap, not a tie.

**Axis failures are split three ways this run**: fleet-low **quality** `civ-grounded` (0.6310),
fleet-low **novelty** `civ-formal` (2.2180), fleet-low **alignment** `civ-therapist` (0.8100).

## Low-relevance civ

**`civ-therapist` — lifetime relevance 2470.21, rel/sim 1.231, win_rate 0.011, sims 2007.**

It was already the lifetime low **at baseline** (2457.65, vs `civ-grounded` 2480.90 — a gap of
only 23.25). This run it gained +12.56, the **smallest** relevance gain of any civ, so it stayed
last. `civ-grounded` gained +15.16 and remained second.

> **Second low-relevance shape: `civ-grounded`.** It now holds the **lowest `rel/sim` on the board**
> (1.230 vs `civ-therapist` 1.231 — a hair apart) and the fleet-low **quality** axis (0.6310),
> while its alignment is mid-pack (1.6600). The board's tail ordering and the raw-relevance
> ordering disagree in the bottom pair for a **4th consecutive session**, but the flip remains
> confined to that pair; the top 6 are identical in both orderings.

**No extinction, no birth.** The extinction floor is relevance **-10**; the lowest civ is
2470.21, i.e. **247x** the floor. `extinction_and_birth()` is only called from `--loop`
anyway, and this was a non-loop run. Registry 8, `max_civs` 12, all `generation=1`.

## Chooser vs `avg_score` argmax — 2/5 (40 %)

| prompt | chooser | argmax | margin | |
|---|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | -0.2100 | DOWN-GRADE |
| the bookkeeper's role | civ-precise | civ-poetic | -0.0067 | DOWN-GRADE |
| the witness log | civ-precise | civ-precise | 0.0000 | AGREE |
| ternary values | civ-precise | civ-precise | 0.0000 | AGREE |
| JEV as a decision oracle | civ-precise | civ-poetic | -0.0733 | DOWN-GRADE |

**3 down-grades, 0 up-grades** — every disagreement took the *lower*-scoring candidate, and the
chooser picked the same civ on all 5 prompts regardless of content. The series across sessions
211-258 already contains 0 %, 20 %, 40 %, 60 % and 100 % agreement rates, so a 40 % point is not
a trend; the **up-grade count across the whole series is still 0**.

## Re-confirmations

- `civ-precise` won **all 5** competitions (**7th consecutive** sweep) and holds lifetime
  win_rate **0.722** — the fleet's only healthy chooser/win-rate line.
- `civ-poetic` led the run's `avg_score` (2.0090) and holds lifetime relevance #1 and `rel/sim` #1
  on a **0.6 %** win rate — relevance without influence.
- `civ-therapist` holds the lifetime low AND the run low AND the fleet-low alignment axis for the
  **9th consecutive session**; its quality this session rose (0.6520 vs 0.4670 in 257), so the
  two-axis collapse of session 257 did **not** repeat.
- **Axis identity is NOT stable across sessions for `civ-grounded`** — it was the run-level
  2nd-lowest in 257 and is again 2nd-lowest here, but its failure axis moved (quality-only, both
  sessions). `civ-formal` takes the novelty floor this session, where `civ-engineer` held it in
  256 and `civ-engineer` took a general mid-low shape in 257. Do not attribute one session's
  axis to a civ.
- The board's `sims_run` field is `relevance / relevance_per_sim` with `relevance_per_sim`
  **rounded to 3 dp** — it is NOT the true `simulations_run` counter. Always take the baseline
  from `git show HEAD:<civ>/culture.json`.
