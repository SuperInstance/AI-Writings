# Civ Orchestrator — Run Report, session 245 (2026-10-25)

## Session 245 (2026-10-25) — provider path, baseline, and result

- Command: `civilization_orchestrator.py --sims 5 --prompts 5 --providers zai` -> exit 0, ~29 s.
- Provider path: **Control B mock** (z.ai credential gap, **104th session**) + **live JEV** (`jev-1.14.0`).
  - z.ai probe: `HTTP=401 {"error":{"code":"401","message":"token expired or incorrect"}}` — endpoint healthy, credential absent.
  - Control B needs **both** `ZAI_TOKEN` (the gate) and `ZAI_URL_OVERRIDE` (the destination); the override alone is dead code.
- Baseline: `3490026` (session 244 tree). **Pre-flight gate: 11/11 PASS** (first build). **Run verification: 0 FAIL / 60 PASS.**
- Ledger delta: **+10 rows per civ, +80 total**; `meta_log` **958 -> 963** (+5); **18** files changed.
- Seed algorithm re-verified over the full current-format ledger **before** the run: **2880/2880 exact, 0 mismatches**; new rows **80/80** recompute exactly.
- Mock body **349** chars (38 header + 162 tail + 149 continuation), inside the 332-369 band, **first build**.
- Winners: `civ-precise` **4/5**, `civ-engineer` **1/5**.
- Chooser/`avg_score` argmax agreement **1/5 (20 %)** — 4 down-grades, **0 up-grades**.
- Run low `civ-therapist` (avg **1.2447**) — quality **0.4710** and alignment **0.8300** both at the fleet low, a **two-axis** collapse.
- Lifetime low `civ-grounded` (**2300.51**) for the **106th** consecutive session; also lowest rel/sim (**1.211**).
- The run low and the lifetime low are **different civs** — keep both axes.
- No civ near extinction (threshold `relevance < -10`; lowest **2300.51**, **230x** the floor). Registry 8 civs, `max_civs` 12, all `generation=1`.

## Run-level axes (this batch's 80 rows)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | **2.0337** | **1.2160** | 2.4200 | 2.4650 |
| civ-precise | 1.9660 | 0.9600 | 2.2610 | **2.6770** |
| civ-formal | 1.7323 | 0.7500 | 2.2440 | 2.2030 |
| civ-engineer | 1.6920 | 0.7880 | 2.1880 | 2.1000 |
| civ-whimsical | 1.5390 | 0.7210 | **2.4470** | 1.4490 |
| civ-grounded | 1.5273 | 0.6160 | 2.2810 | 1.6850 |
| civ-mythic | 1.5047 | 0.8110 | 2.3090 | 1.3940 |
| **civ-therapist** | **1.2447** | **0.4710** | 2.4330 | **0.8300** |

- Spreads: **alignment 1.8470 = 2.34x** the `avg_score` spread (0.7890); quality 0.7450 = 0.94x; novelty 0.2590 = 0.33x.
- **Alignment dominated again** — the axis that dominates rotates the holder, not the axis.
- `civ-therapist`'s novelty is **2nd-highest of 8** while its alignment is the fleet low: a **voice** failure, not a prose failure.

## Lifetime leaderboard (relevance desc)

| civ | relevance | rel/sim | win_rate | gen | w/l |
|---|---|---|---|---|---|
| civ-poetic | 3238.23 | 1.719 | 0.006 | 1 | 6/932 |
| civ-precise | 3111.91 | 1.660 | 0.705 | 1 | 658/275 |
| civ-formal | 2690.61 | 1.427 | 0.129 | 1 | 121/815 |
| civ-whimsical | 2672.89 | 1.413 | 0.005 | 1 | 5/933 |
| civ-mythic | 2629.70 | 1.400 | 0.011 | 1 | 10/922 |
| civ-engineer | 2572.47 | 1.373 | 0.062 | 1 | 58/873 |
| civ-therapist | 2305.62 | 1.228 | 0.012 | 1 | 11/924 |
| **civ-grounded** | **2300.51** | **1.211** | 0.080 | 1 | 75/862 |

**Low-relevance civilizations (the task's ask):**

1. **`civ-grounded` — lifetime low, 106th consecutive session.** Lowest `relevance` (2300.51), lowest
   `relevance_per_sim` (1.211), lowest lifetime `win_rate` among the mid-pack (0.080). Lifetime
   `relevance` gap to the next civ (`civ-therapist`, 2305.62) is only **5.11** — `civ-grounded` and
   `civ-therapist` are effectively tied at the bottom.
2. **`civ-therapist` — run low (this batch), and 2nd-lowest lifetime.** Two-axis collapse:
   quality 0.4710 and alignment 0.8300 both at the fleet low, with novelty (2.4330) 2nd of 8.
   It holds the run low in **7 of the last 8** sessions.
3. **`civ-mythic` — 6th of 8 on lifetime relevance** (2629.70), and the **lowest alignment of the
   mid-pack** on this run (1.3940) behind only `civ-therapist`. Watch axis, not yet a collapse.

**No civ is near extinction.** The threshold is `relevance < -10`; the lowest is **2300.51**,
**230x** the floor. The bottom of the leaderboard is a *relevance ordering* problem, not a
lifecycle problem.

## Chooser vs `avg_score` argmax: 1/5 (20 %)

| prompt | chooser | argmax | delta | |
|---|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | -0.1567 | down |
| the bookkeeper's role | civ-precise | civ-poetic | -0.0367 | down |
| the witness log | civ-precise | civ-precise | 0.0000 | agree |
| ternary values | civ-engineer | civ-precise | -0.3333 | down |
| JEV as a decision oracle | civ-precise | civ-poetic | -0.0300 | down |

**4 down-grades, 0 up-grades.** The up-grade count is **0 by construction** — the chooser is a
JEV `choice` question over `content_preview[:150]` and never sees `avg_score`. **Never treat
`win_rate` as a quality metric.**

## Counter gap — both epochs side by side (unchanged)

| civ | blob gap | post-run gap | delta |
|---|---|---|---|
| civ-grounded | -84.3467 | -84.3467 | 0.000000 |
| civ-whimsical | -173.1433 | -173.1433 | 0.000000 |
| civ-formal | -85.5267 | -85.5267 | 0.000000 |
| civ-poetic | -96.8033 | -96.8033 | 0.000000 |
| civ-precise | -32.6333 | -32.6333 | 0.000000 |
| civ-mythic | -51.1100 | -51.1100 | 0.000000 |
| civ-therapist | -42.1133 | -42.1133 | 0.000000 |
| civ-engineer | -44.2433 | -44.2433 | 0.000000 |

Both columns are computed **within the same epoch** (blob `relevance` vs **blob** ledger sum;
post-run `culture.json` vs **working-tree** ledger sum) ⇒ the offset is **fixed**, not accumulating.

## Verification detail

- **Pre-flight 11/11 PASS** (first build): 40/40 requests, 40/40 distinct seeds, 40/40 distinct
  previews, 40/40 independently recomputed md5s, 349-char bodies in band, 38+162=200 geometry,
  149-char continuation, 5 distinct seeds per civ, 8 distinct seeds per prompt.
- **Run verification 0 FAIL**: ledger +10/civ (80 total), `meta_log` +5, 80/80 `[mock-zai` prefix,
  80/80 `provider=zai`, 40/40 distinct seeds, 80/80 md5 recompute, competition-phase
  per-`(civ,prompt)` 1:1 in 40/40, 0 JEV `error` keys, 0 fallback `(2.0,2.0,2.0)` triples,
  80/80 distinct triples, confidence spread 0.26-0.90, 8/8 distinct previews per competition
  prompt, sim->competition ts gap positive in 8/8 (3.66-26.00 s), meta-vs-ledger `avg_score`
  mismatches 0, counter gap delta 0.000000 for all 8, `wins+losses` delta = 5 per civ,
  `simulations_run` +10 per civ, `git status --porcelain` = 18 modified.

## Environment notes

- **Wiped workspace (105th session with the task path absent).** `/workspace` held only
  `.plugin-cache`; the upstream is **`SuperInstance/AI-Writings`** (3.7 GB, Python) and
  `cellular-first-design` is a **subdirectory** of it. The task slug `ai-writings/cellular-first-design`
  404s on GitHub.
- **NAS EDQUOT (17th session).** `/workspace` is 600 G/600 G; a clone into it dies with
  `Disk quota exceeded`. Clone to `/tmp` (overlay) and **bridge**:
  `ln -s /tmp/work/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`,
  verified with `stat -L` + `os.path.samefile()` -> `True` (inode `129:12615` on both sides).
- **`git sparse-checkout disable` alone did NOT clear the staged `prose/` deletions** on a
  blobless clone. `git read-tree HEAD` fixed the **index**; `git checkout -- prose/` then
  restored the worktree blobs. Assert an empty `git status --porcelain` before the run.
- Tool timeout 30 s < orchestrator run ~29 s ⇒ detached launch with stdout redirected
  **and** `< /dev/null`, then poll `ps` + the log.
- `gh` not installed (25th session) — `GET /user/repos` with `GITHUB_TOKEN`; the GitHub API is
  case-insensitive (`SuperInstance/ai-writings` == `SuperInstance/AI-Writings`).
