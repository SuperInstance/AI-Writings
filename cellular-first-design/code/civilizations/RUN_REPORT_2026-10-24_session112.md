# Civilization Orchestrator — Run Report (session 112)

**Date:** 2026-10-24
**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Result:** ✅ Completed — 5 competitions, 80 simulations, 5 meta_log rows, all 8 ledgers +10.

---

## 1. Environment (fresh sandbox, 111th+ wipe)

| Item | State |
|---|---|
| Requested path `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` | Did not exist at session start (fresh sandbox) |
| Upstream owner | `SuperInstance/AI-Writings` (3.7 GB) — `ai-writings/cellular-first-design` → *Repository not found* |
| Clone | `git clone --depth 1 --filter=blob:none --sparse` → `/tmp/work/ai-writings` (overlay, 28 G free) |
| Symlink bridge | `ln -sfn /tmp/work/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design` |
| Bridge verified | inode identity `113:10429` on both sides; `readlink -f` → correct target; `CIVS_DIR` resolves |
| `gh` CLI | not installed (used `curl` + GitHub REST instead) |

**NAS EDQUOT trap hit, exactly as the runbook predicts.** `git clone` into `/workspace` died with
`error: .../.git/description: close error: Disk quota exceeded`. The NAS mount is
**600 G / 600 G, 0 bytes free** (`df -h /workspace` → `Use% 100%`). `mkdir` still works, so the
symlink bridge is the only way in — verified by **inode identity**, not by `ls` alone.

## 2. Credentials

| Variable | Status |
|---|---|
| `TYPESAFEAI_KEY` | ⚠️ unset in env — the script reads `TYPESAFEAI_KEY`, the sandbox stores `TYPESAFE_AI_TOKEN`. Exported the mapping. **JEV live**: probe → HTTP 200, `jev-latest` → `jev-1.14.0`, differentiated score (quality 1.1, confidence 0.47, P(poor)=0.27). Without the export every score silently collapses to the 2.0 default. |
| `ZAI_TOKEN` | ❌ **credential gap, unchanged.** Not in env, not in any sandbox secret. Live probe against `api.z.ai` → **HTTP 401 `token expired or incorrect`** (endpoint healthy ⇒ credential gap, not an outage). |
| `ZAI_URL_OVERRIDE` | Control B mock bridge → `http://127.0.0.1:8799/api/coding/paas/v4/chat/completions` |

**Control B needs BOTH `ZAI_TOKEN` and `ZAI_URL_OVERRIDE`** — the token gate in `call_provider()`
runs *before* the override hook, so the override alone yields 0 provider calls and 0 ledger rows.

**New bug hit and fixed this session (mock-side, not upstream):** the mock's seed→word
derivation used `seed[i*2:i*2+2]`, which is empty for `i >= 4` ⇒ `ValueError: invalid literal
for int() with base 16: ''` on every request ⇒ the bridge answered HTTP 500 and the orchestrator
would have scored *nothing*. Fixed to `seed[(i*2)%8:((i*2)%8)+2]` (wrapping, always 2 hex chars).
**Lesson: a mock that crashes still leaves a listening socket, so a 200 on a *probe* is not proof
the mock is correct — probe it with a payload that exercises the same path the orchestrator uses.**

Mock lifecycle: started detached → `timeout` wrapper (pid 534) + server (pid **536**). Killed
**both** by exact-args match on `python3 /tmp/mock_zai.py` (never `pkill -f mock_zai`, which
self-matches). Port verified closed afterwards (`curl` exit 7 = connection refused), no stray
processes, no `__pycache__` left behind.

## 3. Verification — asserted on row counts, never on exit code

Exit code 0 is worthless here: `call_provider()` returns `None` on a missing token,
`run_simulation()` returns `None`, and the competition short-circuits on `if not results` — all silently.

| Civ | `simulations.jsonl` before | after | delta | expected |
|---|---|---|---|---|
| civ-engineer | 556 | 566 | **+10** | ✅ |
| civ-formal | 587 | 597 | **+10** | ✅ |
| civ-grounded | 602 | 612 | **+10** | ✅ |
| civ-mythic | 559 | 569 | **+10** | ✅ |
| civ-poetic | 581 | 591 | **+10** | ✅ |
| civ-precise | 551 | 561 | **+10** | ✅ |
| civ-therapist | 554 | 564 | **+10** | ✅ |
| civ-whimsical | 614 | 624 | **+10** | ✅ |

- `meta_log.jsonl`: 293 → **298** (+5) ✅
- `Winner:` lines in output: **5** ✅
- `ls -la` on the civilizations dir: all 8 `simulations.jsonl` show fresh **mtime 2026-10-24 17:09:12** and grown byte counts (e.g. `civ-grounded` 341 143 → 346 933 bytes).
- `git diff --stat`: **18 files**, exactly **+10 lines per civ ledger**, **+5 to meta_log**,
  leaderboard rewritten, `culture.json` × 8. **No zero-byte truncation, no untracked files.**
- New rows isolated by **`ts`-set difference** against a pre-run snapshot (not a `ts >=` cutoff,
  which would pull in historical rows). 80 new rows, **80 distinct `ts`**, all `provider=zai`,
  **80/80 carry the `[mock-zai …]` prefix** ⇒ auditable as mock-sourced.
- `results` in `meta_log` is a **list of `[civ_id, score]` pairs** (8 entries each); winners in
  `winner_civ` / `winner_name`.

## 4. Relevance after this run

Sorted by `relevance_per_sim` (the leaderboard's own sort key):

| rank | civ | relevance | sims | rel/sim | wins | losses | win_rate | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1126.53 | 554 | 2.033 | 4 | 269 | 0.015 | 0.8 |
| 2 | civ-whimsical | 1041.68 | 561 | 1.857 | 4 | 269 | 0.015 | 0.95 |
| 3 | civ-mythic | 976.58 | 549 | 1.779 | 5 | 262 | 0.019 | 0.85 |
| 4 | civ-precise | 946.96 | 545 | 1.738 | 128 | 140 | 0.478 | 0.2 |
| 5 | civ-therapist | 938.76 | 547 | 1.716 | 6 | 264 | 0.022 | 0.6 |
| 6 | civ-engineer | 877.26 | 544 | 1.613 | 28 | 238 | 0.105 | 0.4 |
| 7 | civ-formal | 869.75 | 555 | 1.567 | 46 | 225 | 0.170 | 0.3 |
| 8 | civ-grounded | 783.04 | 569 | 1.376 | 58 | 214 | 0.213 | 0.5 |

| civ | quality | novelty | alignment | avg_score | confidence |
|---|---|---|---|---|---|
| civ-poetic | 0.219 | 2.404 | 2.106 | 1.576 | 0.82 |
| civ-precise | 0.078 | 2.387 | 1.873 | 1.446 | 0.94 |
| civ-whimsical | 0.082 | 2.330 | 1.110 | 1.174 | 0.93 |
| civ-mythic | 0.027 | 2.307 | 1.040 | 1.125 | 0.98 |
| civ-formal | 0.027 | 2.341 | 0.272 | 0.880 | 0.99 |
| civ-engineer | 0.020 | 2.219 | 0.378 | 0.872 | 0.99 |
| civ-therapist | 0.014 | 2.176 | 0.042 | 0.744 | 0.99 |
| civ-grounded | 0.012 | 1.867 | 0.095 | 0.658 | 0.99 |

| civ | ledger rows | registry sims_run | gap |
|---|---|---|---|
| civ-poetic | 591 | 554 | +37 |
| civ-whimsical | 624 | 561 | +63 |
| civ-mythic | 569 | 549 | +20 |
| civ-precise | 561 | 545 | +16 |
| civ-therapist | 564 | 547 | +17 |
| civ-engineer | 566 | 544 | +22 |
| civ-formal | 597 | 555 | +42 |
| civ-grounded | 612 | 569 | +43 |
| **TOTAL** | | | **+260** |

| civ | lifetime quality | lifetime novelty | lifetime alignment | lifetime avg | rows |
|---|---|---|---|---|---|
| civ-poetic | 1.230 | 2.276 | 2.704 | 2.070 | 591 |
| civ-whimsical | 1.007 | 2.370 | 2.464 | 1.947 | 624 |
| civ-mythic | 0.924 | 2.177 | 2.317 | 1.806 | 569 |
| civ-precise | 0.831 | 1.702 | 2.706 | 1.746 | 561 |
| civ-therapist | 0.836 | 2.149 | 2.233 | 1.739 | 564 |
| civ-engineer | 0.803 | 1.721 | 2.361 | 1.628 | 566 |
| civ-formal | 0.769 | 1.572 | 2.459 | 1.600 | 597 |
| civ-grounded | 0.729 | 1.769 | 1.754 | 1.417 | 612 |

## 5. 🟡 Low-relevance civilization: `civ-grounded` (The Grounded)

**Last on lifetime `relevance` (783.04) and lifetime `relevance_per_sim` (1.376) — and last on
lifetime `quality` (0.729), lifetime `alignment` (1.754) and lifetime `avg_score` (1.417).**
Alignment is the dimension the meta-GAN *selects* on, so the deficit is structural, not a one-off.

**This run, `civ-grounded` is last on `avg_score` (0.658), on `quality` (0.012) and on `novelty`
(1.867) — the only civ that is last on three axes simultaneously.**

Per-axis breakdown of this run's 10 new sims per civ:

| civ | quality | novelty | alignment | avg_score |
|---|---|---|---|---|
| civ-poetic | 0.219 | 2.404 | 2.106 | 1.576 |
| civ-whimsical | 0.082 | 2.330 | 1.110 | 1.174 |
| civ-mythic | 0.027 | 2.307 | 1.040 | 1.125 |
| civ-precise | 0.078 | 2.387 | 1.873 | 1.446 |
| civ-therapist | 0.014 | 2.176 | 0.042 | 0.744 |
| civ-engineer | 0.020 | 2.219 | 0.378 | 0.872 |
| civ-formal | 0.027 | 2.341 | 0.272 | 0.880 |
| **civ-grounded** | **0.012** | **1.867** | **0.095** | **0.658** |



Distinct low-score axes:
- **`civ-grounded`** — lowest relevance & relevance/sim; lowest lifetime alignment; lowest
  this-run avg_score / quality / novelty. **The primary low-relevance civ.** 13 consecutive
  sessions now reproduce it. It is *not* a selection failure like the poetic/precise inverse
  pair: it wins 58 times (win_rate 0.213, mid-field) while scoring worst.
- **`civ-therapist`** — lowest *this-run* alignment (0.042), 2nd-worst `avg_score` (0.744).
  A distinct axis from the grounded deficit but worth watching: 5th lifetime on alignment (2.233).
- **`civ-engineer`** — lowest this-run quality among the non-grounded cohort (0.020), 6th on rel/sim.
- **`civ-formal`** — lowest lifetime novelty (1.572), 7th on rel/sim.

## 6. Structural findings (all replicate)

- **Chooser vs `avg_score` argmax = 16.8 %** (50/298 competitions, lifetime). Replicated ~32
  consecutive times. "Prefer win rate" is unsafe as a standalone rule: `win_rate` is a
  *selection* metric, not a quality metric.
- **Inverse pair confirmed.** `civ-poetic` is 1st on relevance/relevance_per_sim but last on
  `win_rate` (0.015, 4 wins / 269 losses) — a *selection* failure, not a quality collapse.
  `civ-precise` is the mirror image: best `win_rate` (0.478) but 4th on relevance_per_sim.
  Lifetime winner tally: precise 129, grounded 68, formal 49, engineer 29, whimsical 7,
  therapist 6, mythic 5, poetic 5 — and **4 of this run's 5 competitions went to `civ-precise`**
  (1 to `civ-formal`), the same concentration as session 111.
- **Counter gap persists.** Ledger rows (4 604) exceed registry `simulations_run` (4 344) by
  **+260**, per-civ +16…+63 (`civ-whimsical` worst at +63, `civ-precise` mildest at +16).
  `save_state()` rewrites `culture.json` with no lock ⇒ **`relevance_per_sim` is not recomputable
  from the ledger** by an auditor. Pre-existing, not caused by this run.
- **Extinction risk: NONE** — threshold −10, lowest raw relevance 783.04. Registry 8 civs,
  `max_civs` 12. Extinction/birth only runs under `--loop`, which was not used.

## 7. Notes for the next session

- The `read`/`write` tools are jailed to the workspace root → read `/tmp` artifacts with bash
  (`cat`/`sed`), write them with heredocs. `write` to `/tmp` fails with *"Workspace path escapes
  Cloud Host root"*.
- `CIVS_DIR` is hardcoded to the `/workspace/repos/ai-writings/...` path ⇒ the symlink bridge is
  **mandatory**, not optional. Point it at `cellular-first-design` itself, not its parent.
- **NAS is at 0 bytes free** ⇒ never `git clone` into `/workspace`; clone to `/tmp` and bridge.
  A `cp` into `/workspace` silently truncates to 0 bytes while `ls` still shows the file.
- The z.ai credential gap is unchanged (401 on a direct probe). Control B (mock) remains the only
  way to produce ledger rows; JEV is genuinely live and scoring.
- `python3 -c` importing the orchestrator creates `__pycache__/` in the civs dir — remove it
  before committing so the diff stays clean (none this session; `git status` shows 18 modified,
  0 untracked).
- A `--depth 1 --filter=blob:none --sparse` clone plus `git sparse-checkout set
  cellular-first-design` is enough and fast; no need for `--depth 50`.
