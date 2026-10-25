# Civilization Orchestrator — Session 252 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Fleet: 8 civs. Provider: **Control B mock** (z.ai credential gap, **109th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `75bf141` (session 251 tree). **Pre-flight gate: 40/40 PASS, exit 0.** **Run verification: ALL PASS (0 FAIL).**

## Environment notes

- **Task path absent.** `/workspace/repos/ai-writings/...` did not exist (**14th consecutive occurrence**).
  The workspace held only `.plugin-cache`. A direct clone into `/workspace` fails with
  `close error: Disk quota exceeded` (NAS EDQUOT) — **20th session**. Cloned to the overlay at
  `/tmp/ai-writings` and bridged the chain with a symlink `/workspace/repos/ai-writings -> /tmp/ai-writings`.
  Bridge verified with `os.path.samefile()` -> `True` (dev:ino **129:12609** both sides).
- **Bridge target must be the CLONE ROOT, not the nested `cellular-first-design` dir.** The script's
  hardcoded `CIVS_DIR` is `.../cellular-first-design/code/civilizations`. Symlinking the *nested* dir
  produces a doubled path (`cellular-first-design/cellular-first-design/code/...`) and
  `REGISTRY.read_text()` raises `FileNotFoundError`. Linking the clone root resolves it.
  Symlink creation also needs the parent dir to exist first — `ln -sfn` into a missing
  `/workspace/repos/ai-writings` silently no-ops, so link in two steps (`mkdir` then `ln -s`).
- **z.ai live probe: HTTP 401** `token expired or incorrect` => endpoint healthy, credential absent.
  `ZAI_TOKEN` unset in env. Control B mock used with **both** `ZAI_TOKEN` (the gate in
  `call_provider`) **and** `ZAI_URL_OVERRIDE` (the destination); the override alone is dead code.
- **`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`** before the run. Direct probe of
  `https://api.typesafe.ai/v1/systemone` -> **HTTP 200**, `{"model":"jev-1.14.0", …}`, real score
  `0.13`, confidence `0.82`. Without the alias `jev_score` falls through to the `2.0/2.0/2.0` fallback.
- Mock teardown by **PID captured from `ps`** (291), then proved the port closed
  (`curl` exit 7, `HTTP=000`, 0 processes left). Never `pkill -f mock_zai` (self-match).

## Pre-flight gate — 40/40 PASS, exit 0

40/40 requests 200, 40/40 distinct previews, 40/40 distinct seeds, 40/40 distinct seed-tuples,
all bodies **349 chars** (inside the 332-369 band), 38+162=200 geometry holds, 149-char
continuation, 5 distinct seeds per civ, 8 distinct seeds per prompt.

**Mock algorithm validated non-circularly**: the seed/colour/figure recompute was re-derived
against the **pre-existing** ledger (**not** this run's rows) — **3440/3440 exact matches** over
the recognizable historical rows, 0 mismatches.

> **Verification-script trap (cost one false FAIL).** The first pass of the ledger re-derivation
> used hand-rolled fixed offsets on the mock header (`prev[15:]`, `rest[6:20]`) and reported
> 11760 mismatches. The figure field is `hhhh/hhhh/hhhh` — slash-separated — so a fixed offset
> slices across the field boundary and yields garbage. The preflight's own regex is the known-good
> parser; use it. A second trap followed: the check asserted `dW == 1` per meta row, but
> `civ-precise` won **all 5** competitions, so its `dW` is 5 (one per prompt, not one total).
> Reconcile `dW` against the **count of meta rows won**, not against the row count.

## Ledger delta

- **+10 rows per civ, +80 total**; `meta_log` **993 -> 998** (+5); **18** files changed.
- Every new row carries the documented **9 keys** (`ts, civ, civ_name, provider, params, prompt,
  scores, avg_score, content_preview`); preview length **200** on every row; all 80 rows parse as
  JSON; **0 key/shape violations**.
- **JEV was live on all 80 rows**: 0 `error` fields, **0** `2.0/2.0/2.0` fallback triples,
  0 zero-confidence rows, confidence range **0.26 - 0.89**, **80/80 distinct score triples**.
- Prompt draw across the 80 new rows: ternary values 19, witness log 17, what a cell is 15,
  bookkeeper 15, JEV oracle 14.
- **80/80** rows' seed+colour+figure independently recomputed **exact**; **0** `(civ,prompt)`
  combos carrying more than one seed.

### Counter reconciliation — 8/8 OK

The sim phase gives every civ +5 sims; the competition phase gives every civ **5 more sims**
(each competition calls `run_simulation` again) plus exactly one W or L. So **dSims = 10** and
**dW + dL = 5** for all 8 civs. Relevance deltas match the sum of the new `avg_score` values to
the last decimal on all 8 ledgers.

| civ | dW | dL | dSims | sum(new avg) | dRelevance |
|---|---|---|---|---|---|
| civ-grounded | 0 | 5 | 10 | 14.9200 | 14.9200 |
| civ-whimsical | 0 | 5 | 10 | 15.3900 | 15.3900 |
| civ-formal | 0 | 5 | 10 | 17.7200 | 17.7200 |
| civ-poetic | 0 | 5 | 10 | 20.0733 | 20.0733 |
| civ-precise | 5 | 0 | 10 | 20.1000 | 20.1000 |
| civ-mythic | 0 | 5 | 10 | 15.7100 | 15.7100 |
| civ-therapist | 0 | 5 | 10 | 12.5900 | 12.5900 |
| civ-engineer | 0 | 5 | 10 | 17.2433 | 17.2433 |

**Meta/ledger W-L reconciliation 8/8 exact** — `meta_log` records `civ-precise` as winner on all 5
prompts, and `civ-precise` gained exactly 5 wins and 0 losses; every other civ gained 0 W and 5 L.

> **Baseline gotcha (re-confirmed).** The leaderboard's `sims_run` field is
> `relevance / relevance_per_sim` with `relevance_per_sim` **rounded to 3 dp** — it is NOT the true
> `simulations_run` counter. Taking the baseline from `leaderboard.json` produces **negative** dSims
> and a false reconciliation FAIL. **Always take the baseline from
> `git show HEAD:<civ>/culture.json`**, which carries the exact counter.

## Run-level standings (10 sims per civ)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-precise | 2.0100 | 1.0550 | 2.2310 | 2.7440 |
| civ-poetic | 2.0073 | 1.1340 | 2.4490 | 2.4390 |
| civ-formal | 1.7720 | 0.7970 | 2.2490 | 2.2700 |
| civ-engineer | 1.7243 | 0.8060 | 2.1980 | 2.1690 |
| civ-mythic | 1.5710 | 0.7710 | 2.3550 | 1.5870 |
| civ-whimsical | 1.5390 | 0.6950 | 2.4890 | 1.4330 |
| civ-grounded | 1.4920 | 0.5580 | 2.3130 | 1.6050 |
| **civ-therapist** | **1.2590** | 0.6230 | 2.3370 | **0.8170** |

**Run low — `civ-therapist`** (avg 1.2590): fleet-low **alignment** 0.8170, quality 0.6230 is
2nd-lowest, novelty 2.3370 is mid-pack. Alignment spread 1.9270 = **3.35x** the quality spread
=> *voice* failure, not prose failure. Gap to the next civ (civ-grounded, 1.4920) is **0.2330 =
31.0 %** of the run spread 0.7510 — a wide, unambiguous gap, not a tie.

**Axis failures are split three ways this run**: fleet-low **quality** `civ-grounded` (0.5580),
fleet-low **novelty** `civ-engineer` (2.1980), fleet-low **alignment** `civ-therapist` (0.8170).

## Low-relevance civ

**`civ-therapist` — lifetime relevance 2394.46, rel/sim 1.230, win_rate 0.011, sims 1947.**

It was already the lifetime low **at baseline** (2381.87, vs `civ-grounded` 2390.44 — a gap of
only 8.57). This run it gained +12.59, the **smallest** relevance gain of any civ, so it stayed
last. `civ-grounded` gained +14.92 and remained second.

> **Correction to the skill's standing claim.** The skill file records "`civ-grounded` — the
> low-relevance civ, 91st/92nd consecutive session". That is **stale**: at the session-251
> baseline the lifetime low was already `civ-therapist` (2381.87) with `civ-grounded` second
> (2390.44). The holder rotated earlier than the skill notes. **`civ-grounded` is the
> run-level 2nd-lowest and holds the fleet-low QUALITY axis; `civ-therapist` holds the lifetime
> low AND the run low AND the fleet-low alignment axis.** Both deserve the label depending on
> which axis is being read.

**No extinction, no birth.** The extinction floor is relevance **-10**; the lowest civ is
2394.46, i.e. **-239.4x** the floor. `extinction_and_birth()` is only called from `--loop`
anyway, and this was a non-loop run.

## Chooser vs `avg_score` argmax — 1/5 (20 %)

| prompt | chooser | argmax | |
|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | DOWN-GRADE |
| the bookkeeper's role | civ-precise | civ-poetic | DOWN-GRADE |
| the witness log | civ-precise | civ-precise | AGREE |
| ternary values | civ-precise | civ-poetic | DOWN-GRADE |
| JEV as a decision oracle | civ-precise | civ-poetic | DOWN-GRADE |

**4 down-grades, 0 up-grades** — every disagreement took the *lower*-scoring candidate, and the
chooser picked the same civ on all 5 prompts regardless of content. The series across sessions
211-227 already contains 0 %, 20 %, 40 %, 60 % and 100 % agreement rates, so a 20 % point is not
a trend; the **up-grade count across the whole series is still 0**.

## Re-confirmations

- `civ-grounded` holds fleet-low **quality**; the axis of failure rotates between sessions while
  the civ identity mostly does not.
- The bridge `ls` **non-slash** form works; the trailing-slash form against the symlink bridge
  fails. Use the non-slash form (or `os.path.samefile`).
- `gh` not installed; `ai-writings/cellular-first-design` slug 404s. Upstream is
  `SuperInstance/ai-writings` (lowercase works this session, via `GET /search/repositories?q=ai-writings`).
- NAS EDQUOT total — clone must land on the overlay (`/tmp`); the durable copy of this report is
  **git**, and the workspace `write` tool is jailed to the workspace root.
- `civ-precise` won **all 5** competitions and now holds win_rate **0.714** (691 W vs 277 L) —
  the fleet's only healthy chooser/win-rate line, and it swept the round.
