# Civilization Orchestrator — Session 253 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Fleet: 8 civs. Provider: **Control B mock** (z.ai credential gap, **110th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `4b7dc0d` (session 252 tree). **Pre-flight gate: 40/40 PASS, exit 0.** **Run verification: 70 PASS / 0 FAIL.**

**Session 253 in one line:** `civ-precise` swept **5/5** competitions for the second consecutive
session; the chooser's agreement with the `avg_score` argmax was **2/5 (40 %)** — 3 down-grades,
0 up-grades; the run low was **`civ-therapist`** (avg **1.2217**) at the fleet floor on **both**
quality (**0.5530**) and alignment (**0.8030**), a **two-axis** collapse for the **4th consecutive
session**; and the lifetime low stayed with `civ-therapist` (**2406.68**) ahead of `civ-grounded`
(**2420.33**) by **13.65**, against a #2 -> #3 step of **286.69** — a **21x** larger step.

## Environment notes

- **Task path absent.** `/workspace/repos/ai-writings/...` did not exist (**14th consecutive occurrence**).
  Workspace held only `.plugin-cache`. A direct clone into `/workspace` fails with
  `close error: Disk quota exceeded` (NAS EDQUOT, 600 G / 0 avail) — **20th session**.
  Cloned to the overlay at `/tmp/aiw` and bridged with a symlink
  `/workspace/repos/ai-writings -> /tmp/aiw`. Bridge verified with `os.path.samefile()` -> `True`.
- **The sparse clone is the fast path — 14 MB vs 3.7 GB.** A full `git clone` of the tree ran
  past 3.7 GB and was still transferring; `--filter=blob:none --no-checkout --depth 1 --branch main`
  plus `sparse-checkout set cellular-first-design` produced a **14 MB** working tree in seconds.
  *The full clone is a waste of 3.7 GB and several minutes for a 14 MB payload.*
- **Upstream is `SuperInstance/AI-Writings`** (capitalised). The `ai-writings/…` slug 404s.
  `GET /search/repositories?q=cellular-first-design` does **not** surface it; resolved via
  `GET /search/code?q=civilization_orchestrator+in:path`.
- **z.ai live probe: HTTP 401** `token expired or incorrect` => endpoint healthy, credential absent.
  `ZAI_TOKEN` unset in env and absent from all 8 secrets (**110th session**). Control B mock used
  with **both** `ZAI_TOKEN` (the gate in `call_provider`) **and** `ZAI_URL_OVERRIDE` (the destination);
  the override alone is dead code behind the token gate.
- **`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`** before the run. Direct probe of
  `https://api.typesafe.ai/v1/systemone` -> **HTTP 200**, `{"model":"jev-1.14.0", …}`, real score
  `1.2`, confidence `0.17`. Without the alias `jev_score` falls through to the `2.0/2.0/2.0` fallback.
- **Mock teardown by exact PID** (460/462) and the port re-probed closed — never `pkill -f mock_zai`
  (self-match, 2 prior occurrences).

## Pre-flight gate — 40/40 PASS, exit 0

40/40 requests 200, 40/40 distinct previews, 40/40 distinct seeds, 40/40 distinct seed-tuples,
all bodies **349 chars** (inside the 332-369 band), 38+162=200 geometry holds, 149-char
continuation, 5 distinct seeds per civ, 8 distinct seeds per prompt.

**Mock algorithm validated non-circularly**: the seed/colour/figure recompute was re-derived
against the **pre-existing** ledger (**not** this run's rows) — **3520/3520 exact matches** over the
recognizable historical rows, 0 mismatches.

## Ledger delta

- **+10 rows per civ, +80 total**; `meta_log` **998 -> 1003** (+5); **18** files changed.
- Every new row carries the documented **9 keys**; preview length **200** on every row; all 80 rows
  parse as JSON; **0 key/shape violations**; provider set on every new row is exactly `{zai}`.
- **80/80 new rows re-derive exactly** from `md5(cultural_prompt)` (seed, colour, figure) — 0 mismatches.
- **0 JEV errors, 0 fallback triples, 0 non-numeric quality scores** — every one of the 80 rows
  carries a live score from `jev-1.14.0`.

## Run results

| civ | n | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| **civ-therapist** | 10 | **1.2217** | **0.5530** | 2.3090 | **0.8030** |
| civ-grounded | 10 | 1.4977 | 0.5840 | 2.2750 | 1.6340 |
| civ-whimsical | 10 | 1.5367 | 0.7450 | 2.4380 | 1.4270 |
| civ-mythic | 10 | 1.5813 | 0.8250 | 2.3690 | 1.5500 |
| civ-engineer | 10 | 1.6503 | 0.6420 | 2.2850 | 2.0240 |
| civ-formal | 10 | 1.7803 | 0.8420 | 2.1930 | 2.3060 |
| civ-precise | 10 | 1.9413 | 0.8790 | 2.3110 | 2.6340 |
| civ-poetic | 10 | 2.0723 | 1.2610 | 2.4420 | 2.5140 |

Run spread: `avg_score` **0.8507**, alignment **1.8310**, quality **0.7080**, novelty **0.2490**.
**Alignment spread = 2.15x the `avg_score` spread** — alignment, not novelty, is what separates this fleet.

## Lifetime leaderboard (post-run)

| rank | civ | relevance | rel/sim | wins | losses | win_rate | gen | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 3400.83 | 1.732 | 6 | 972 | 0.006 | 1 | 0.8 |
| 2 | civ-precise | 3268.25 | 1.672 | 696 | 277 | 0.715 | 1 | 0.2 |
| 3 | civ-formal | 2830.79 | 1.441 | 122 | 854 | 0.125 | 1 | 0.3 |
| 4 | civ-whimsical | 2795.95 | 1.419 | 5 | 973 | 0.005 | 1 | 0.95 |
| 5 | civ-mythic | 2755.39 | 1.407 | 10 | 962 | 0.010 | 1 | 0.85 |
| 6 | civ-engineer | 2707.02 | 1.385 | 59 | 912 | 0.061 | 1 | 0.4 |
| 7 | **civ-therapist** | **2406.68** | 1.230 | 11 | 964 | 0.011 | 1 | 0.6 |
| 8 | **civ-grounded** | 2420.33 | **1.223** | 75 | 902 | 0.077 | 1 | 0.5 |

Note the leaderboard sorts by **`relevance_per_sim`**, so `civ-grounded` is ranked last (1.223) even
though its raw `relevance` (**2420.33**) is **above** `civ-therapist`'s (**2406.68**). The two orders
disagree at the bottom; name both explicitly.

## Low relevance — the two bottom civs

- **`civ-therapist`** — run low **and** lifetime low. Run avg **1.2217** (fleet low), at the fleet
  floor on **quality (0.5530)** and **alignment (0.8030)** simultaneously: a **two-axis** collapse,
  the **4th consecutive session** with this signature. Novelty is 2.3090, mid-fleet — the collapse
  is not a creativity failure.
- **`civ-grounded`** — lifetime **rel/sim** low (**1.223**), and the run's second-lowest avg
  (**1.4977**) with quality **0.5840**, also near the floor. Its lifetime `win_rate` **0.077** is
  3rd-best in the fleet, so the two bottom civs are low on *relevance per simulation*, not on *wins*.
- **Bottom-two gap: 13.65** (therapist 2406.68 vs grounded 2420.33). The step from #2 to #3
  (engineer 2707.02) is **286.69** — a **21x** larger step. The bottom of this leaderboard is a
  **pair**, not a ladder.
- **Neither is near extinction.** Threshold is `relevance < -10`; the lowest is **2406.68**, roughly
  **240x** the floor. Registry stays at **8** civs, `max_civs` is 12, all `generation=1`.
  No birth and no extinction fired this session.
- **Relevance gained this run** is monotone in the same order as the run scores: therapist **+12.22**
  (lowest gain) through poetic **+20.72** (highest). Every civ gained; no civ lost ground.

## The chooser keeps down-grading the argmax

`civ-precise` won **5/5** competitions, but the `avg_score` argmax agreed only **2/5 (40 %)** —
**3 down-grades, 0 up-grades**. This is now a **22-session** run with **0 up-grades ever** recorded.
The chooser is structurally unable to agree with the score: it never receives the scores, only the
200-char previews. *Do not read the disagreement as a scoring regression.*

Separately, `civ-poetic` is the `avg_score` leader of this run (**2.0723**) and holds lifetime
relevance #1 and `rel/sim` #1 — on a **0.6 %** lifetime win rate with **6** wins. It is the most
relevant civ by every accumulated measure and one of the least competitive in the meta-GAN.

## Durable lessons

1. **THE SPARSE CLONE IS 265x SMALLER THAN THE FULL CLONE — USE IT FIRST, ALWAYS.**
   `git clone --filter=blob:none --no-checkout --depth 1 --branch main` +
   `sparse-checkout set cellular-first-design` gave a **14 MB** tree in seconds; the full clone
   reached **3.7 GB** and was still transferring after minutes. *The payload the task needs is
   one directory — never pay for the whole repo when the shape is known.*
2. **A `git clone` INTO THE NAS STILL FAILS AT THE FIRST FILE — THE OVERLAY IS THE ONLY PATH.**
   The error surfaces as `close error: Disk quota exceeded` on `.git/description`, i.e. the very
   first write, not at the end. *Do not interpret a clone that "starts" as one that will finish.*
3. **THE LEADERBOARD'S SORT KEY AND ITS `relevance` COLUMN DISAGREE AT THE BOTTOM.**
   The board sorts by `relevance_per_sim`, so the last row is not the lowest `relevance`.
   Here `civ-grounded` has the higher raw relevance (2420.33 vs 2406.68) but the lower
   `rel/sim` (1.223 vs 1.230). *Report both the order and the gap; the order alone misleads.*
4. **THE TWO-AXIS COLLAPSE IS NOW A FOUR-SESSION RUNNING SIGNATURE FOR `civ-therapist`.**
   Quality floor + alignment floor together, novelty mid-fleet. It is stable enough to name as a
   trait of that civ rather than a per-session accident. *The axis is the finding, not the holder.*
5. **THE MOCK PATTERN STILL ONLY COVERS THE CURRENT GENERATION OF LEDGER ROWS.**
   3 520 of 16 884 pre-existing rows match the current mock header; the remaining 12 364 are older
   generations. *Filter to the current header format before sizing anything off the ledger.*

## Reproduce

```bash
export CIVS_DIR=/tmp/aiw/cellular-first-design/code/civilizations
export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
export ZAI_TOKEN="mock-placeholder"
export ZAI_URL_OVERRIDE="http://127.0.0.1:8099/v1/chat/completions"
python3 "$CIVS_DIR/tools/mock_zai.py" 8099 &
python3 "$CIVS_DIR/tools/preflight.py" 8099
python3 "$CIVS_DIR/civilization_orchestrator.py" --sims 5 --prompts 5 --providers zai
```

**Verdict: ALL PASS (0 FAIL).**
