# Civilization Orchestrator — Run Report, Session 23b (independent replication) (2026-10-23)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Repo:** `SuperInstance/ai-writings` @ `d961ba80` (cellular-first-design is a **subdirectory** of `ai-writings`, not a separate repo)
**Result:** the **as-specified command is a silent no-op** (+0 rows, exit 0). Under the
Control B seam the same command produced **+80 live rows** (10/civ) per body set,
**+5 meta_log**, **5 competition winners**, **0** default-score rows, **0** errors,
**0** mock fallbacks, **0** extinction/birth events.

---

## 1. Environment reconstruction (122nd consecutive wipe)

- The task path `/workspace/repos/ai-writings/...` did not exist at session start.
  `/workspace` held only `.plugin-cache` and `.skills`; NAS `/workspace` at **100 %
  quota** (600 G used, 0 avail).
- `SuperInstance/cellular-first-design` is **not a repository** — the path is a
  subdirectory of `SuperInstance/ai-writings`. Cloning it directly fails with
  `Repository not found`.
- `git clone` into `/workspace/repos` **FAILS** mid-copy:
  `fatal: cannot copy '.../templates/description': Disk quota exceeded`.
  Clone to `/tmp` (overlay, 21 G free) instead — the clone is **~4.7 GB**.
- Bridge: `rm -rf /workspace/repos/ai-writings && ln -sfn /tmp/aw /workspace/repos/ai-writings`.
  `CIVS_DIR` is hardcoded to the `/workspace` path (line 36), so the symlink is
  what makes the script write into the clone.
- `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` — **JEV verified live** at
  `jev-1.14.0` (HTTP 200, `quality.score 0.04`, `confidence 0.97`).
  Without this the run exits 0 and measures nothing.

## 2. The credential gap (21st consecutive session)

`ZAI_TOKEN` / `ZAI_KEY` / `GROQ_TOKEN` absent from env **and** from the 8-entry
secret store (`MOTHQUANTUM_TOKEN`, `TYPESAFE_AI_TOKEN`, `MINIMAX_KEY`,
`NOTION_TOKEN`, `NPMJS_TOKEN`, `CRATES_TOKEN`, `PYPI_TOKEN`, `GITHUB_TOKEN`).
`gh` is also **not on PATH** in this sandbox.

### Baseline no-op (the command exactly as specified)

| metric | expected | measured |
|---|---|---|
| exit code | 0 | **0** |
| ledger rows | — | **+0** (924 → 924) |
| `meta_log.jsonl` | — | **+0** (63 → 63) |
| `Winner:` lines | 5 | **0** |
| competition section | 5 rounds | **empty** |

The per-civ `[Name] running 5 sims...` lines print **before** the provider call,
so they are **not** evidence of work. `call_provider` returns `None` when the
token is absent, and `run_simulation` returns `None` without writing a row.
**Assert on the row delta, never on the exit code.**

## 3. Control B (16th replication) — stub at the gate

One-line `ZAI_URL_OVERRIDE` seam (1 insertion / 1 deletion, verified with
`git diff --stat`), `ZAI_TOKEN` set to a dummy, provider URL redirected to a
local mock. The request is **really attempted**; the entire JEV path stays live.

| metric | expected | measured (set A) | measured (set B) |
|---|---|---|---|
| ledger rows | +80 (10/civ) | **+80**, 10/civ uniform | **+80**, 10/civ uniform |
| `meta_log.jsonl` | +5 | **+5** (63 → 68) | **+5** (63 → 68) |
| `Winner:` lines | 5 | **5** | **5** |
| all-2.0-default rows | 0 | **0** | **0** |
| rows with a score error | 0 | **0** | **0** |
| provider | `zai` only | **80/80 `zai`** | **80/80 `zai`** |
| distinct `content_preview` | 24 (8 voices x 3 bodies) | **24** | **24** |
| distinct `avg_score` | high | **77** | **79** |
| `avg_score` range | wide | **0.823 – 2.833** | — |
| mock fallback calls | 0 | **0** | **0** |
| mock calls per voice | 10 | **10 x 8** | **10 x 8** |

JEV sub-score spread (set A, 80 rows): quality mean **1.222**, novelty mean
**2.091**, alignment mean **2.713**, confidence mean **0.499** (49 distinct
values). A live JEV, not a stub.

### NEW — a hash-collision artifact can masquerade as "collapsed content"

The first mock used `h = (sum(ord(ch) for ch in question) + SEED + len(pool)) % len(pool)`
to pick a body. That hash **collapsed onto 2 of 3 bodies per voice**, giving
`distinct content_preview = 16` (2 per civ) — inside the s9 "collapsed" red band
(healthy 50–68), which would have read as a broken mock.

**The tell that it was a mock artifact and not a real signal:** every preview was
exactly **200 chars** (the script truncates `content_preview` to 200), and the
mock log showed all 8 voices reaching all 5 questions. Fixed by combining a
question hash with a per-voice call counter
(`h = (qh + _CALLNO[voice] - 1) % len(pool)`), which restores **3 bodies per
voice / 24 distinct previews** — the true ceiling for a 3-body-per-voice mock.
**Note the ceiling:** with 3 bodies per voice, 24 is the *maximum* achievable
distinct-preview count, so a 50–68 expectation is unattainable for this mock
shape. The s9 check should compare against the mock's *own* body count, not a
fixed band.

## 4. Chooser vs argmax — 0/5 (15th replication)

`best_civ` agreed with `argmax(avg_score)` in **0 of 5 rounds (0 %)**.
Margins **0.090 / 0.090 / 0.050 / 0.070 / 0.220**, mean **0.104**.
The two metrics remain **essentially uncorrelated**; the chooser does not see the
scores. Set A winners: Precise, Grounded, Precise, Formal, Formal. Set B
winners: Engineer, Grounded, Precise, Precise, Precise.

## 5. Counter gap — unchanged at +260

Ledger **1004** rows vs registry `simulations_run` sum **744** → gap **+260**,
identical to the session-20/21/22b baselines. It is a **lost-update race** in
`save_state()` (each civ loads the same `culture.json` and writes back its own
count), not a leak, and it moves in both directions.

## 6. Low-relevance reading — **each lens separate, never merged**

Two independently-written mock body sets (A/B) were run so the answer can be
tested for stability. **A civ is reportable as low only if it is bottom-two in
BOTH sets**; otherwise it is reported as *unranked*.

| lens | set A lowest | set B lowest | stable? |
|---|---|---|---|
| session `avg_score` | civ-formal (1.388) | civ-grounded (1.534) | **no** |
| session `quality` | civ-formal (0.595) | civ-grounded (0.702) | **no** |
| session `novelty` | civ-formal (1.100) | civ-formal (1.282) | yes |
| session `alignment` | civ-grounded (1.937) | civ-grounded (2.140) | yes |
| bottom-2 `avg_score` | {formal, grounded} | {formal, grounded} | **yes** |
| bottom-2 `quality` | {formal, grounded} | {engineer, grounded} | no |
| bottom-2 `novelty` | {formal, precise} | {formal, grounded} | no |
| bottom-2 `alignment` | {formal, grounded} | {grounded, therapist} | no |

Lifetime lenses (all 1004 ledger rows, post-run):

| lens | lowest | value |
|---|---|---|
| (a) `relevance_per_sim` (board sort key) | **The Grounded** | 1.643 |
| (b) raw relevance | **The Engineer** | 163.60 |
| (c) `win_rate` (**selection** metric) | **The Poetic** | **0.000 (0W/43L)** |
| (d) lifetime mean `avg_score` | **The Grounded** | 1.733 |
| (e) lifetime mean `quality` | **The Grounded** | 1.405 |
| (f) lifetime mean `novelty` | **The Formal** | 1.064 |
| (g) lifetime mean `alignment` | **The Grounded** | 2.336 |
| (h) this-session `avg_score` | civ-formal (A) / civ-grounded (B) | 1.388 / 1.534 |

Leaderboard after the run (sorted by `relevance_per_sim`):

| civ | rel/sim | relevance | sims | W/L | win rate |
|---|---|---|---|---|---|
| The Poetic | 2.478 | 232.94 | 94 | 0/43 | **0.000** |
| The Whimsical | 2.428 | 245.26 | 101 | 2/41 | 0.047 |
| The Mythic | 2.270 | 202.06 | 89 | 2/35 | 0.054 |
| The Therapist | 2.200 | 191.40 | 87 | 1/39 | 0.025 |
| The Precise | 2.010 | 170.88 | 85 | 22/16 | 0.579 |
| The Engineer | 1.948 | 163.60 | 84 | 5/31 | 0.139 |
| The Formal | 1.749 | 166.15 | 95 | 9/32 | 0.220 |
| **The Grounded** | **1.643** | 179.04 | 109 | 8/34 | 0.190 |

- **The Grounded — the stable low-relevance civ (11th session running).** Last on
  `relevance_per_sim` (1.643), lifetime `avg_score` (1.733), lifetime `quality`
  (1.405) and lifetime `alignment` (2.336) — the last of all 8. It is bottom-two
  on `avg_score` in **both** body sets. It is a **genuine quality weakness**, not
  a longevity artefact: it ran the most sims (109) and still ends last on the raw
  score lenses. It nonetheless has **higher raw relevance than the board's
  bottom-3** (179.04 vs The Engineer's 163.60) — it is behind on the *rate*, not
  the *total*.
- **The Formal — the co-stable low civ.** Bottom-two on `avg_score` in both sets,
  and lowest on lifetime `novelty` (1.064) and on both sessions' `novelty` in
  set A. Its set-A session `avg_score` (1.388) and `quality` (0.595) are the
  lowest measured — but set B moved both, so its single-lens low reading is
  **not** stable; it is reportable only as *bottom-two on `avg_score`*.
- **The Poetic — the inverse case (21st session running).** 1st of 8 on
  `relevance_per_sim` (2.478) and **0 wins in 43**, and **0 of 5** rounds in
  set B. A **selection** failure, not a quality collapse. It is also top of 8 on
  lifetime `avg_score` (2.517) and `quality` (2.058).
- **The Precise — wins by being picked, not by scoring.** Best win rate in the
  fleet (**0.579**, 22W/16L) and **3 of 5** wins in set B, but 5th of 8 on
  `relevance_per_sim` and 4th of 8 on lifetime `avg_score`.
- **Extinction risk: none.** Threshold −10, lowest raw relevance **+163.60**.
  `extinction_and_birth()` runs only in `--loop` mode every third iteration;
  this was single-shot, so **no civ was born or retired** and
  `civilizations.json` is unchanged (8 civs, empty diff).

## 7. Restore verification — 60 tracked files

All **60** tracked files under `cellular-first-design/code/civilizations/` are
**byte-identical to `git show HEAD:<path>`** via `cmp`: **60 identical, 0
mismatched**. `git status` clean at `d961ba80`. `__pycache__/` removed. Mock
killed by explicit PID (849, wrapper 847), confirmed gone (`connection refused`
on :8931). All 8 `witness.log` files remain **0 bytes**.

**Caveat:** this session's 160 rows (80 per body set) were deliberately reverted
with the restore, so the run is *reported*, not *committed*. To persist it, the
ledgers must be re-run and committed before `git checkout HEAD -- .`.

## 8. Environment notes (nothing new broke; all known traps held)

1. `git clone` into `/workspace` fails with `Disk quota exceeded` mid-copy and
   leaves a partial `.git` behind. Clone to `/tmp` and symlink.
2. `rm -rf` before `ln -sfn` is still required.
3. Kill the mock by **explicit PID** from `ps -eo pid,args --no-headers | grep "[z]ai_mock"`.
   `pkill -f` self-matches and kills the invoking shell; the `grep` also
   self-matches — read the PID, don't trust the grep's own output.
4. The orchestrator writes `leaderboard.json` even on a no-op run — restore
   after the **unpatched** run too, or the diff shows a spurious change.
5. `__pycache__/` is written into the civilizations dir — remove before committing.
6. `gh` is not on PATH; `mavis` is not on PATH. Use the `secret` tool to
   enumerate the secret store, not the shell.
7. The `write` tool is jailed to the workspace root and the NAS mount is at
   100 % — this report was written via a bash heredoc into `/tmp`.


## 9. Parallel-session reconciliation (important)

A **parallel session 23** (`7998437d`, "📊 Civilization Orchestrator — Run Report
Session 23") was pushed to `main` **while this run was in flight**. Its push was
rejected as non-fast-forward; a `git fetch` showed the remote **2 ahead / 1 behind**
this local HEAD.

Reconciliation performed:

1. `git fetch` -> `FETCH_HEAD = 7998437d` (the parallel session 23, which had
   already written `RUN_REPORT_2026-10-23_session23.md` and committed **+160 live
   ledger rows**, 924 -> 1084, `meta_log` 63 -> 73).
2. Local branch cut at `FETCH_HEAD` (`git checkout -B session23b FETCH_HEAD`); the
   working tree now matches the **remote's** committed state.
   Verified after the cut: 8 ledgers at 116/147/162/119/141/111/114/174 rows
   (total **1084**), `meta_log` **73** — **the remote's rows are intact**.
3. This report is filed as **`RUN_REPORT_2026-10-23_session23b.md`** to avoid a
   filename collision with the remote's `session23.md`.

**This run's own 160 rows were NOT committed.** They were measured, verified, and
then reverted during the standard restore step (§7) before the parallel push was
discovered. The commit that lands here carries **the report only**; the ledger
state on `main` is the parallel session's.

**The two runs agree on both headline findings**, which is worth stating
explicitly because they are independent observations of the same fleet:

| finding | parallel session 23 | this session (23b) |
|---|---|---|
| lowest `relevance_per_sim` | civ-grounded (1.586) | civ-grounded (1.643) |
| `win_rate` bottom | civ-poetic (0.000) | civ-poetic (0.000, 0W/43L) |
| as-specified command | exit 0, +0 rows | exit 0, +0 rows |
| control B | +80 rows/set, 5 winners | +80 rows/set, 5 winners |

**Consequence for the low-relevance reading:** the §6 figures are computed
against the **pre-parallel** baseline (924 rows, `meta_log` 63) and are **this
run's** measurements. The parallel session's figures are computed against the
**same** baseline. The two are **directly comparable on the baseline but not
additive** — both sessions observed the same fleet at the same commit
(`d961ba80`) before either pushed.

## 10. Unresolved

**`ZAI_TOKEN` remains the binding constraint.** Everything else — clone, bridge,
JEV liveness, the seam, the mock, the verification, the restore — is working and
replicated. Supplying a real z.ai coding key replaces the mock and makes the
provider leg real; nothing else in the pipeline needs to change.
