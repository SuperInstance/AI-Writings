# Civilization Orchestrator — Run Report (session 113)

**Date:** 2026-10-24
**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Result:** ✅ Completed — 5 competitions, 80 simulations, 5 meta_log rows, all 8 ledgers +10.

---

## 1. Environment (fresh sandbox, 113th+ wipe)

| Item | State |
|---|---|
| Requested path `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` | Did not exist at session start (fresh sandbox) |
| Upstream owner | `SuperInstance/AI-Writings` — `ai-writings/cellular-first-design` → *Repository not found* |
| Clone | `git clone --depth 1` → `/tmp/ai-writings` (overlay, 28 G free). Upstream is ~3.7 GB; a depth-1 clone of the `cellular-first-design` tree is 3.6 MB. |
| Symlink bridge | `ln -sfn /tmp/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design` |
| Bridge verified | inode identity `129:10425` on both sides; `readlink -f` → correct target; `-ef` → SAME INODE OK |
| `gh` CLI | not installed (used `curl` + GitHub REST instead) |

**NAS EDQUOT trap hit, exactly as the runbook predicts.** `git clone` into `/workspace` died with
`error: .../.git/description: close error: Disk quota exceeded`. The NAS mount is
**600 G / 600 G, 0 bytes free** (`df -h /workspace` → `Use% 100%`). Confirmed this session that
the trap is *total*: a `dd` of a **100-byte** file into `/workspace` also fails with
"Disk quota exceeded", so not even a stub file can be created there. `mkdir` still works ⇒
the symlink bridge is the only way in — verified by **inode identity**, not by `ls` alone.

`cp` of the working tree into `/workspace` also **silently truncated every file to 0 bytes**
while `ls` still listed them — the runbook's documented failure mode, re-confirmed.

## 2. Credentials

| Variable | Status |
|---|---|
| `TYPESAFEAI_KEY` | ⚠️ unset in env — the script reads `TYPESAFEAI_KEY`, the sandbox stores `TYPESAFE_AI_TOKEN`. Exported the mapping. **JEV live and differentiating**: probe → HTTP 200, `quality` 0.40 (conf 0.68), `novelty` 1.55 (conf 0.38), `alignment` 2.81 (conf 0.00). Without the export every score silently collapses to the 2.0 default. |
| `ZAI_TOKEN` | ❌ **credential gap, unchanged.** Not in env, not in any sandbox secret. Live probe against `api.z.ai` → **HTTP 401 `token expired or incorrect`** (endpoint healthy ⇒ credential gap, not an outage). |
| `ZAI_URL_OVERRIDE` | Control B mock bridge → `http://127.0.0.1:8799/api/coding/paas/v4/chat/completions` |

**Control B needs BOTH `ZAI_TOKEN` and `ZAI_URL_OVERRIDE`** — the token gate in `call_provider()`
runs *before* the override hook, so the override alone yields 0 provider calls and 0 ledger rows.

**The mock source is not in git history** (checked `git log --all --diff-filter=A --name-only`),
so it had to be rewritten from the runbook's description rather than reused. The session-112
crash is designed out from the start: the seed→word derivation wraps the index
(`seed[(i*2)%8:((i*2)%8)+2]`), so no slice is ever empty.

**Mock integrity check done properly, per the session-112 lesson:** a 200 on a one-word probe
is *not* proof the mock is correct. The mock was probed with the **exact long, multi-sentence
cultural prompt the orchestrator sends** (The Grounded voice + a canon prompt), returning
HTTP 200, 314 chars, `[mock-zai seed=…]` prefix present, and **zero tracebacks** in its stdout.
The port was verified closed after teardown (`curl` exit 7 = connection refused).

Mock lifecycle: started detached → `timeout` wrapper (pid 244) + server (pid 245). Killed
**both** by exact-args match on `python3 /tmp/mock_zai.py` (never `pkill -f mock_zai`, which
self-matches). No stray processes, no `__pycache__` left behind.

## 3. Verification — asserted on row counts, never on exit code

Exit code 0 is worthless here: `call_provider()` returns `None` on a missing token,
`run_simulation()` returns `None`, and the competition short-circuits on `if not results` — all silently.

| Civ | `simulations.jsonl` before | after | delta | expected |
|---|---|---|---|---|
| civ-engineer | 566 | 576 | **+10** | ✅ |
| civ-formal | 597 | 607 | **+10** | ✅ |
| civ-grounded | 612 | 622 | **+10** | ✅ |
| civ-mythic | 569 | 579 | **+10** | ✅ |
| civ-poetic | 591 | 601 | **+10** | ✅ |
| civ-precise | 561 | 571 | **+10** | ✅ |
| civ-therapist | 564 | 574 | **+10** | ✅ |
| civ-whimsical | 624 | 634 | **+10** | ✅ |

- `meta_log.jsonl`: 298 → **303** (+5) ✅
- `Winner:` lines in output: **5** ✅
- `ls -la` on the civilizations dir: all 8 `simulations.jsonl` show fresh **mtime 2026-10-24 17:14** and grown byte counts (e.g. `civ-grounded` 346 933 → 352 717 bytes).
- `git diff --stat`: **18 files**, exactly **+10 lines per civ ledger**, **+5 to meta_log**,
  leaderboard rewritten, `culture.json` × 8. **No zero-byte truncation, no untracked files.**
- New rows isolated by **`ts`-set difference** against a pre-run snapshot (not a `ts >=` cutoff,
  which would pull in historical rows). 80 new rows, **80 distinct `ts`**, all `provider=zai`,
  **80/80 carry the `[mock-zai …]` prefix** ⇒ auditable as mock-sourced.
- **0 rows carry a JEV `error` field**; 22 distinct `quality` values across the 80 rows ⇒ the
  scorer is differentiating, not emitting a constant.
- `results` in `meta_log` is a **list of `[civ_id, score]` pairs** (8 entries each); winners in
  `winner_civ` / `winner_name`.

### Transient NAS mount race on the symlinked deep path — recurred this session

The verification `ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/`
failed **once** with `No such file or directory`, *immediately* after a parallel command on the
same path had succeeded. Re-checked with `stat -L` (`129:10425` both sides), `readlink -f`, `-ef`
(SAME INODE OK), and 3/3 `ls` retries — all passed. **A single `ls` failure is not evidence of a
missing directory**; re-check with `stat -L` + `readlink -f` + `[-e path]` and retry before
concluding the tree is gone. Do not "fix" a working symlink by re-creating it.

## 4. Relevance after this run

Sorted by `relevance_per_sim` (the leaderboard's own sort key):

| rank | civ | relevance | sims | rel/sim | wins | losses | win_rate | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1140.45 | 564 | 2.022 | 4 | 274 | 0.014 | 0.8 |
| 2 | civ-whimsical | 1049.62 | 571 | 1.838 | 4 | 274 | 0.014 | 0.95 |
| 3 | civ-mythic | 985.57 | 559 | 1.763 | 5 | 267 | 0.018 | 0.85 |
| 4 | civ-precise | 961.25 | 555 | 1.732 | 131 | 142 | 0.480 | 0.2 |
| 5 | civ-therapist | 943.52 | 557 | 1.694 | 6 | 269 | 0.022 | 0.6 |
| 6 | civ-engineer | 884.87 | 554 | 1.597 | 28 | 243 | 0.103 | 0.4 |
| 7 | civ-formal | 878.55 | 565 | 1.555 | 48 | 228 | 0.174 | 0.3 |
| 8 | civ-grounded | 788.28 | 579 | 1.361 | 58 | 219 | 0.209 | 0.5 |

| civ | quality | novelty | alignment | avg_score |
|---|---|---|---|---|
| civ-poetic | 0.325 | 1.631 | 2.220 | 1.392 |
| civ-precise | 0.225 | 1.946 | 2.116 | 1.429 |
| civ-formal | 0.059 | 1.261 | 1.321 | 0.880 |
| civ-mythic | 0.074 | 1.304 | 1.318 | 0.899 |
| civ-whimsical | 0.061 | 1.479 | 0.841 | 0.794 |
| civ-engineer | 0.042 | 1.158 | 1.084 | 0.761 |
| **civ-grounded** | **0.025** | 1.327 | **0.222** | **0.525** |
| **civ-therapist** | **0.019** | 1.232 | **0.179** | **0.477** |

| civ | ledger rows | registry sims_run | gap |
|---|---|---|---|
| civ-poetic | 601 | 564 | +37 |
| civ-whimsical | 634 | 571 | +63 |
| civ-mythic | 579 | 559 | +20 |
| civ-precise | 571 | 555 | +16 |
| civ-therapist | 574 | 557 | +17 |
| civ-engineer | 576 | 554 | +22 |
| civ-formal | 607 | 565 | +42 |
| civ-grounded | 622 | 579 | +43 |
| **TOTAL** | | | **+260** |

| civ | lifetime quality | lifetime novelty | lifetime alignment | lifetime avg | rows |
|---|---|---|---|---|---|
| civ-poetic | 1.215 | 2.265 | 2.696 | 2.059 | 601 |
| civ-whimsical | 0.992 | 2.356 | 2.438 | 1.929 | 634 |
| civ-mythic | 0.909 | 2.162 | 2.300 | 1.790 | 579 |
| civ-precise | 0.820 | 1.707 | 2.695 | 1.741 | 571 |
| civ-therapist | 0.821 | 2.133 | 2.198 | 1.717 | 574 |
| civ-engineer | 0.789 | 1.711 | 2.339 | 1.613 | 576 |
| civ-formal | 0.757 | 1.567 | 2.440 | 1.588 | 607 |
| civ-grounded | 0.718 | 1.762 | 1.729 | 1.403 | 622 |

## 5. 🟡 Low-relevance civilization: `civ-grounded` (The Grounded)

**Last on lifetime `relevance` (788.28) and lifetime `relevance_per_sim` (1.361) — and last on
lifetime `quality` (0.718), lifetime `alignment` (1.729) and lifetime `avg_score` (1.403).**
Alignment is the dimension the meta-GAN *selects* on, so the deficit is structural, not a one-off.

**This run, `civ-grounded` is last on `avg_score` (0.525), on `alignment` (0.222) and on
`quality` (0.025)** — 3rd-lowest on `novelty` (1.327). It is *not* a selection failure like the
poetic/precise inverse pair: it wins 58 times (win_rate 0.209, mid-field) while scoring worst.

**14 consecutive sessions now reproduce it** (sessions 95–104 per the runbook, plus 110–113).

Distinct low-score axes:
- **`civ-grounded`** — lowest relevance & relevance/sim; lowest lifetime alignment; lowest
  this-run avg_score / alignment / quality. **The primary low-relevance civ.**
- **`civ-therapist`** — lowest *this-run* `quality` (0.019) and lowest *this-run* `avg_score`
  (0.477), i.e. **2nd-lowest relevance this run** even though it sits 5th on lifetime rel/sim.
  A distinct axis from the grounded deficit: its lifetime alignment (2.198) is mid-field, so
  the deficit is **quality-driven, not alignment-driven** — unlike grounded. Worth watching.
- **`civ-engineer`** — 2nd-lowest this-run `avg_score` among the non-grounded cohort (0.761),
  lowest this-run `novelty` (1.158), 6th on rel/sim.
- **`civ-formal`** — lowest lifetime novelty (1.567), 7th on rel/sim.

## 6. Structural findings (all replicate)

- **Chooser vs `avg_score` argmax = 17.2 %** (52/303 competitions, lifetime). Replicated ~33
  consecutive times. "Prefer win rate" is unsafe as a standalone rule: `win_rate` is a
  *selection* metric, not a quality metric.
- **Inverse pair confirmed.** `civ-poetic` is 1st on relevance/relevance_per_sim but last on
  `win_rate` (0.014, 4 wins / 274 losses) — a *selection* failure, not a quality collapse.
  `civ-precise` is the mirror image: best `win_rate` (0.480) but 4th on relevance_per_sim.
  Lifetime winner tally: precise 132, grounded 68, formal 51, engineer 29, whimsical 7,
  therapist 6, mythic 5, poetic 5 — and **3 of this run's 5 competitions went to `civ-precise`**
  (2 to `civ-formal`), the same concentration as sessions 111–112.
- **Counter gap persists.** Ledger rows (4 764) exceed registry `simulations_run` (4 504) by
  **+260**, per-civ +16…+63 (`civ-whimsical` worst at +63, `civ-precise` mildest at +16).
  `save_state()` rewrites `culture.json` with no lock ⇒ **`relevance_per_sim` is not recomputable
  from the ledger** by an auditor. Pre-existing, not caused by this run.
- **Extinction risk: NONE** — threshold −10, lowest raw relevance 788.28. Registry 8 civs,
  `max_civs` 12 (the `extinction_and_birth()` default). Extinction/birth only runs under `--loop`, which was not used.

## 7. Notes for the next session

- The `read`/`write` tools are jailed to the workspace root → read `/tmp` artifacts with bash
  (`cat`/`sed`), write them with heredocs. `write` to `/tmp` fails with *"Workspace path escapes
  Cloud Host root"*.
- `CIVS_DIR` is hardcoded to the `/workspace/repos/ai-writings/...` path ⇒ the symlink bridge is
  **mandatory**, not optional. Point it at `cellular-first-design` itself, not its parent.
- The NAS is at 0 bytes free ⇒ never `git clone` or `cp` into `/workspace`; clone to `/tmp` and
  bridge. A `cp` into `/workspace` silently truncates to 0 bytes while `ls` still shows the file.
  Confirmed this session that even a 100-byte `dd` fails.
- The z.ai credential gap is unchanged (401 on a direct probe). Control B (mock) remains the only
  way to produce ledger rows; JEV is genuinely live and scoring.
- **The mock source is not committed to git.** It must be rewritten each session from the
  runbook's description. **Consider committing it to the repo** so the next session can reuse
  (and regression-test) it instead of re-deriving it — that is the single highest-value change
  available here, since the session-112 crash class lives in that file.
- The transient NAS mount race on the symlinked deep path recurred (1 `ls` failure, then 3/3
  retries OK). Re-verify with `stat -L` + `readlink -f` + `-ef` before concluding anything.
- `python3 -c` importing the orchestrator creates `__pycache__/` in the civs dir — remove it
  before committing so the diff stays clean (none this session; `git status` shows 18 modified,
  0 untracked).
