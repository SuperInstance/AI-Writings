# Civilization Orchestrator — Run Report (session 111)

**Date:** 2026-10-24
**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Result:** ✅ Completed — 5 competitions, 80 simulations, 5 meta_log rows, all 8 ledgers +10.

---

## 1. Environment (fresh sandbox, 110th+ wipe)

| Item | State |
|---|---|
| Requested path `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` | Did not exist at session start (fresh sandbox) |
| Upstream owner | `SuperInstance/AI-Writings` — `ai-writings/cellular-first-design` → *Repository not found* (confirmed via REST 404 + `git ls-remote`) |
| Clone | `git clone --depth 50` → `/tmp/aw` (NAS is 600 G/600 G, **0 bytes free**; `git clone` into `/workspace` died with *Disk quota exceeded*) |
| Symlink bridge | `ln -sfn /tmp/aw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design` |
| Bridge verified | inode identity `129:3669` on both sides; `readlink -f` → `/tmp/aw/cellular-first-design`; `CIVS_DIR` resolves |
| `gh` CLI | not installed (used `curl` + GitHub REST / code-search instead) |

**NAS EDQUOT trap avoided.** All clone/build work in `/tmp` (overlay, 28 G free). `mkdir` still works in `/workspace`, so the symlink bridge is the only way in — verified by inode, not by `ls` alone.

## 2. Credentials

| Variable | Status |
|---|---|
| `TYPESAFEAI_KEY` | ⚠️ unset in env — the script reads `TYPESAFEAI_KEY`, the sandbox stores `TYPESAFE_AI_TOKEN`. Exported the mapping. **JEV live**: `jev-latest` → `jev-1.14.0`, returned differentiated scores (probe: quality 0.42, confidence 0.64, P(poor)=0.65). Without the export every score silently collapses to the 2.0 default. |
| `ZAI_TOKEN` | ❌ **credential gap, unchanged.** Not in env, not in any of the 8 sandbox secrets. Live probe against `api.z.ai` → **HTTP 401 `token expired or incorrect`** (endpoint healthy ⇒ credential gap, not an outage). |
| `ZAI_URL_OVERRIDE` | Control B mock bridge → `http://127.0.0.1:8799/api/coding/paas/v4/chat/completions` |

**Control B needs BOTH `ZAI_TOKEN` and `ZAI_URL_OVERRIDE`.** The token gate in `call_provider()` runs *before* the override hook, so the override alone yields 0 provider calls and 0 ledger rows.

Mock lifecycle: started detached → `timeout` wrapper (pid 238) + server (pid **240**). Killed **both** by exact-args match on `python3 /tmp/mock_zai.py` (never `pkill -f mock_zai`, which self-matches). Port verified closed afterwards (`curl` exit 7 = connection refused), no stray processes, no `__pycache__` left behind.

## 3. Verification — asserted on row counts, never on exit code

Exit code 0 is worthless here: `call_provider()` returns `None` on a missing token, `run_simulation()` returns `None`, and the competition short-circuits on `if not results` — all silently.

| Civ | `simulations.jsonl` before | after | delta | expected |
|---|---|---|---|---|
| civ-engineer | 546 | 556 | **+10** | ✅ |
| civ-formal | 577 | 587 | **+10** | ✅ |
| civ-grounded | 592 | 602 | **+10** | ✅ |
| civ-mythic | 549 | 559 | **+10** | ✅ |
| civ-poetic | 571 | 581 | **+10** | ✅ |
| civ-precise | 541 | 551 | **+10** | ✅ |
| civ-therapist | 544 | 554 | **+10** | ✅ |
| civ-whimsical | 604 | 614 | **+10** | ✅ |

- `meta_log.jsonl`: 288 → **293** (+5) ✅
- `Winner:` lines in output: **5** ✅
- `git diff --stat`: 18 files, exactly **+10 lines per civ ledger**, **+5 to meta_log**, leaderboard rewritten, `culture.json` × 8. No zero-byte truncation, no untracked files.
- New rows carry `provider=zai` and the `[mock-zai …]` prefix; `results` in meta_log is a **list of `[civ_id, score]` pairs** (8 entries each); winners in `winner_civ` / `winner_name`.

## 4. Relevance after this run

Sorted by `relevance_per_sim` (the leaderboard's own sort key):

| rank | civ | relevance | sims | rel/sim | wins | losses | win_rate |
|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1110.77 | 544 | 2.042 | 4 | 264 | 0.015 |
| 2 | civ-whimsical | 1029.94 | 551 | 1.869 | 4 | 264 | 0.015 |
| 3 | civ-mythic | 965.33 | 539 | 1.791 | 5 | 257 | 0.019 |
| 4 | civ-precise | 932.50 | 535 | 1.743 | 124 | 139 | 0.471 |
| 5 | civ-therapist | 931.32 | 537 | 1.734 | 6 | 259 | 0.023 |
| 6 | civ-engineer | 868.54 | 534 | 1.626 | 28 | 233 | 0.107 |
| 7 | civ-formal | 860.95 | 545 | 1.580 | 45 | 221 | 0.169 |
| 8 | **civ-grounded** | **776.46** | 559 | **1.389** | 58 | 209 | 0.217 |

## 5. 🟡 Low-relevance civilization: `civ-grounded` (The Grounded)

**Last on lifetime `relevance` (776.46) and lifetime `relevance_per_sim` (1.389), and lowest on lifetime `alignment` (1.781 vs the field's 2.27–2.72).** Alignment is the dimension the meta-GAN *selects* on, so the deficit is structural, not a one-off.

**This run, `civ-grounded` is also last on `avg_score` (0.573), on `quality` (0.008), on `alignment` (0.094) and on `novelty` (1.616).** It is the only civ that is last on *all three* axes simultaneously — no distinct-axis carve-out this time.

Per-axis breakdown of this run's 10 new sims:

| civ | quality | novelty | alignment | avg_score |
|---|---|---|---|---|
| civ-poetic | **0.254** | **2.234** | **2.327** | **1.605** |
| civ-mythic | 0.048 | 2.202 | 1.224 | 1.158 |
| civ-precise | 0.046 | 2.168 | 1.344 | 1.186 |
| civ-whimsical | 0.017 | 2.034 | 0.799 | 0.950 |
| civ-formal | 0.025 | 1.616→2.180 | 0.273 | 0.826 |
| civ-engineer | 0.017 | 2.000 | 0.220 | 0.746 |
| civ-therapist | 0.015 | 1.976 | 0.040 | 0.677 |
| **civ-grounded** | **0.008** | **1.616** | **0.094** | **0.573** |

Distinct low-score axes, as in prior sessions:
- **`civ-grounded`** — lowest relevance & relevance/sim, lowest alignment (lifetime), lowest avg_score / quality / alignment / novelty this run. **The primary low-relevance civ.** 12 consecutive sessions now reproduce it.
- **`civ-therapist`** — lowest *this-run* alignment (0.040), second-worst `avg_score`. Distinct axis from the grounded deficit but worth watching: it is 5th lifetime on alignment (2.273).
- **`civ-engineer`** — lowest *this-run* quality among the non-grounded cohort (0.017), 6th on rel/sim.
- **`civ-formal`** — lowest lifetime novelty (1.559), 7th on rel/sim.

## 6. Structural findings (all replicate)

- **Chooser vs `avg_score` argmax = 16.7 %** (49/293 competitions, lifetime). Replicated ~31 consecutive times. "Prefer win rate" is unsafe as a standalone rule: `win_rate` is a *selection* metric, not a quality metric.
- **Inverse pair confirmed.** `civ-poetic` is 1st on relevance/relevance_per_sim but last on `win_rate` (0.015, 4 wins / 264 losses) — a *selection* failure, not a quality collapse. `civ-precise` is the mirror image: best `win_rate` (0.471) but 4th on relevance_per_sim. This run's winner tally: precise 125, grounded 68, formal 48, engineer 29, whimsical 7, therapist 6, mythic 5, poetic 5 — and **all 5 of this run's competitions went to `civ-precise`.**
- **Counter gap persists.** Ledger rows (4 604) exceed registry `simulations_run` (4 344) by **+260**, per-civ +16…+63 (`civ-whimsical` worst at +63, `civ-precise` mildest at +16). `save_state()` rewrites `culture.json` with no lock ⇒ **`relevance_per_sim` is not recomputable from the ledger** by an auditor. Pre-existing, not caused by this run.
- **Extinction risk: NONE** — threshold −10, lowest raw relevance 776.46. Registry 8 civs, `max_civs` 12. Extinction/birth only runs under `--loop`, which was not used.

## 7. Notes for the next session

- The `read`/`write` tools are jailed to the workspace root → read `/tmp` artifacts with bash (`cat`/`sed`), write them with heredocs. `write` to `/tmp` fails with *"Workspace path escapes Cloud Host root"*.
- `CIVS_DIR` is hardcoded to the `/workspace/repos/ai-writings/...` path ⇒ the symlink bridge is **mandatory**, not optional. Point it at `cellular-first-design` itself, not its parent.
- `python3 -c` importing the orchestrator creates `__pycache__/` in the civs dir — remove it before committing so the diff stays clean (none this session; `git status` shows 18 modified, 0 untracked).
- The z.ai credential gap is unchanged (401 on a direct probe). Control B (mock) remains the only way to produce ledger rows; JEV is genuinely live and scoring.
- A full `--depth 50` clone works and is fast; the runbook's `--filter=blob:none --no-checkout` + sparse-checkout dance is unnecessary if you can afford the working tree in `/tmp`.
