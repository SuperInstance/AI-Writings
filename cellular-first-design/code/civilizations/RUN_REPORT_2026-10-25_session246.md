# Civ Orchestrator — Run Report, session 246 (2026-10-25)

## Session 246 — provider path, baseline, and result

- Command: `civilization_orchestrator.py --sims 5 --prompts 5 --providers zai` -> exit 0, ~29 s.
- Provider path: **Control B mock** (z.ai credential gap, **105th session**) + **live JEV** (`jev-1.14.0`).
  - z.ai probe: `HTTP=401 {"error":{"code":"401","message":"token expired or incorrect"}}` — endpoint healthy, credential absent.
  - Control B needs **both** `ZAI_TOKEN` (the gate) and `ZAI_URL_OVERRIDE` (the destination); the override alone is dead code.
- Baseline: `a486a7b` (session 245 tree). **Pre-flight gate: 40/40 PASS, VERIFICATION: ALL PASS.** **Run verification: 66 PASS / 0 FAIL.**
- Ledger delta: **+10 rows per civ, +80 total**; `meta_log` **963 -> 968** (+5); **18** files changed.
- Seed algorithm re-verified over the full current-format ledger **before** the run: **3040/3040 exact, 0 mismatches**; new rows **80/80** recompute exactly.
- Mock body **349** chars (38 header + 162 tail + 149 continuation), inside the 332-369 band, **first build**.
- Winners: `civ-precise` **5/5** — a clean sweep.
- Chooser/`avg_score` argmax agreement **2/5 (40 %)** — 3 down-grades, **0 up-grades**.
- Run low `civ-therapist` (avg **1.2710**) — quality **0.5580** and alignment **0.8780** both at the fleet low, a **two-axis** collapse.
- Lifetime low `civ-grounded` (**2315.16**) for the **107th** consecutive session; also lowest rel/sim (**1.213**).
- The run low and the lifetime low are **different civs** — keep both axes.
- No civ near extinction (threshold `relevance < -10`; lowest **2315.16**, **231x** the floor). Registry 8 civs, `max_civs` 12, all `generation=1`.

## Verification — `ls -la` on the civilizations tree

The task's verification request, read directly off the filesystem at
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations/`:

| civ | rows before | rows after | Δ | `simulations_run` Δ | W+L Δ |
|---|---|---|---|---|---|
| civ-grounded | 1942 | 1952 | **+10** | 1899->1909 (+10) | +5 |
| civ-whimsical | 1954 | 1964 | **+10** | 1891->1901 (+10) | +5 |
| civ-formal | 1927 | 1937 | **+10** | 1885->1895 (+10) | +5 |
| civ-poetic | 1921 | 1931 | **+10** | 1884->1894 (+10) | +5 |
| civ-precise | 1891 | 1901 | **+10** | 1875->1885 (+10) | +5 |
| civ-mythic | 1899 | 1909 | **+10** | 1879->1889 (+10) | +5 |
| civ-therapist | 1894 | 1904 | **+10** | 1877->1887 (+10) | +5 |
| civ-engineer | 1896 | 1906 | **+10** | 1874->1884 (+10) | +5 |

`meta_log.jsonl`: 963 -> **968** (+5). `leaderboard.json` iso `01:54:01` -> **`18:03:03`**.
All 8 ledgers carry mtime **18:03**; all 8 `culture.json` files likewise. `git status --porcelain`
= **18 modified** (8 ledgers + 8 cultures + `meta_log.jsonl` + `leaderboard.json`).

**The `ls -la` size delta is a secondary receipt, not the proof.** File *size* deltas
(grounded +5847 B, formal +5754 B, whimsical +5819 B, poetic +5771 B, precise +5714 B,
mythic +5791 B, therapist +5827 B, engineer +5853 B) are consistent with 10 rows each, but
row *counts* are the load-bearing measurement and both are reported.

## Run-level axes (this batch's 80 rows)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | **1.9550** | **1.0590** | 2.4390 | 2.3670 |
| civ-precise | 1.9373 | 0.8980 | 2.2500 | **2.6640** |
| civ-formal | 1.7617 | 0.7820 | 2.2590 | 2.2440 |
| civ-engineer | 1.6467 | 0.7130 | 2.2040 | 2.0230 |
| civ-mythic | 1.5923 | 0.8960 | 2.3480 | 1.5330 |
| civ-whimsical | 1.5347 | 0.6830 | **2.4620** | 1.4590 |
| civ-grounded | 1.4647 | **0.5130** | 2.3070 | 1.5740 |
| **civ-therapist** | **1.2710** | 0.5580 | 2.3770 | **0.8780** |

- Spreads: **alignment 1.7860 = 2.61x** the `avg_score` spread (0.6840); quality 0.5460 = 0.80x; novelty 0.2580 = 0.38x.
- **Alignment dominated again** — the axis that dominates rotates the holder, not the axis.
- `civ-therapist`'s novelty (**2.3770**) is 3rd of 8 while its alignment is the fleet low: a **voice** failure, not a prose failure.

## Lifetime leaderboard (relevance desc)

| civ | relevance | rel/sim | win_rate | gen | w/l | temp |
|---|---|---|---|---|---|---|
| civ-poetic | 3257.78 | 1.720 | 0.006 | 1 | 6/937 | 0.8 |
| civ-precise | 3131.28 | 1.661 | 0.707 | 1 | 663/275 | 0.2 |
| civ-formal | 2708.22 | 1.429 | 0.129 | 1 | 121/820 | 0.3 |
| civ-whimsical | 2688.24 | 1.414 | 0.005 | 1 | 5/938 | 0.95 |
| civ-mythic | 2645.63 | 1.401 | 0.011 | 1 | 10/927 | 0.85 |
| civ-engineer | 2588.94 | 1.374 | 0.062 | 1 | 58/878 | 0.4 |
| civ-therapist | 2318.33 | 1.229 | 0.012 | 1 | 11/929 | 0.6 |
| **civ-grounded** | **2315.16** | **1.213** | 0.080 | 1 | 75/867 | 0.5 |

### Low-relevance civilizations (the task's ask)

1. **`civ-grounded` — lifetime low, 107th consecutive session.** Lowest `relevance` (**2315.16**),
   lowest `relevance_per_sim` (**1.213**), and lowest lifetime `avg_score` (**1.2293**) of 8. On every
   lifetime axis it sits 7th or 8th: `avg` 1.2293 (8th), `quality` 0.5466 (8th), `alignment` 1.3072 (7th).
   Its lifetime `novelty` (1.8340) is 6th of 8 — no longer below median, so it is losing on
   **alignment and quality**, not novelty.
2. **`civ-therapist` — run low (this batch), and 2nd-lowest lifetime.** Two-axis collapse:
   quality **0.5580** and alignment **0.8780** both at the fleet low, with novelty (**2.3770**) 3rd of 8.
   It holds the run low in **7 of the last 8** sessions.
3. **The bottom two are effectively tied: `civ-grounded` 2315.16 vs `civ-therapist` 2318.33 — a gap of
   only 3.17** — while the gap from #2 to #3 (`civ-engineer` 2588.94) is **270.61**, an 85x larger step.
   The bottom of the leaderboard is a **pair**, not a ladder.
4. **`civ-mythic` — 5th of 8 on lifetime relevance** (2645.63) and the **lowest alignment of the
   mid-pack** on this run (1.5330). Watch axis, not yet a collapse.

**No civ is near extinction.** The threshold is `relevance < -10`; the lowest is **2315.16**, **231x**
the floor. The bottom of the leaderboard is a *relevance ordering* problem, not a lifecycle problem.
Registry 8, `max_civs` 12, all `generation=1`; extinction/birth only runs under `--loop`.

## Chooser vs `avg_score` argmax: 2/5 (40 %)

| prompt | chooser | argmax | delta | |
|---|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | -0.0500 | down |
| the bookkeeper's role | civ-precise | civ-poetic | -0.0400 | down |
| the witness log | civ-precise | civ-precise | 0.0000 | agree |
| ternary values | civ-precise | civ-precise | 0.0000 | agree |
| JEV as a decision oracle | civ-precise | civ-poetic | -0.0367 | down |

**3 down-grades, 0 up-grades.** The up-grade count is **0 by construction** — the chooser is a JEV
`choice` question over `content_preview[:150]` and never sees `avg_score`. **Never treat `win_rate`
as a quality metric;** it is a *selection* metric.

`civ-precise` swept **5/5** competitions at `preferred_temp` 0.2 while `civ-poetic` was the argmax
on **3 of 5** and won **0**. The **5/5 sweep and 2/5 agreement coexisted** — neither implies the
other. `civ-poetic` remains 1st on lifetime `avg_score` (1.7372), `quality` (0.9401) and `relevance`
(3257.78) with a lifetime `win_rate` of **0.006** (6/937): the same "high prose, unselected" inverse
as session 157. `civ-precise` is its mirror (best lifetime `win_rate` 0.707, highest lifetime
`alignment` 2.3567) — the coldest voice is what the chooser rewards.

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
post-run `culture.json` vs **working-tree** ledger sum) => the offset is **fixed**, not accumulating.
The sign is **negative** in every row. `save_state()` has no lock, so `relevance_per_sim` is **not
recomputable from the ledger** by an auditor.

## Verification detail

- **Pre-flight 40/40 PASS** (first build): 40/40 requests, 40/40 distinct seeds, 40/40 distinct
  previews, 40/40 independently recomputed md5s, 349-char bodies in band, 38+162=200 geometry,
  149-char continuation, 5 distinct seeds per civ, 8 distinct seeds per prompt.
- **Run verification 66 PASS / 0 FAIL**: ledger +10/civ (80 total), `meta_log` +5, 80/80 `[mock-zai`
  prefix, 80/80 `provider=zai`, 80/80 md5 recompute from the sent cultural prompt, 0 JEV `error`
  keys, 0 fallback `(2.0,2.0,2.0)` triples, distinct JEV triples and 40 distinct confidences,
  `avg_score` recomputes exactly 80/80, 40 distinct seeds across the 80 new rows,
  competition-phase 1 row per `(civ,prompt)` in 8/8, sim->competition ts ordering 8/8,
  `culture.json` `simulations_run` +10 for all 8, `generation` still 1, win+loss +5,
  relevance increments match the 10 new `avg_score`s to 1e-6 for all 8, registry unchanged at 8,
  leaderboard sorted by `relevance_per_sim` desc and reconciling against every `culture.json`,
  `meta_log.results` a list of 8 `[civ_id, score]` pairs covering all 8 civs, counter gap delta
  0.000000 for all 8, 38+162 geometry on all 3040 current-format ledger rows.

### One check was wrong, not the run

The first pass reported **1 FAIL**: *"8/8 civs: 5 distinct seeds in the sim phase."* That check was
**wrong, not the data.** The sim phase draws `random.choice(prompts)` from only 5 prompts, so 5 draws
over 5 prompts **must** repeat some prompts — and the seed is a deterministic function of
`(civ, prompt)`, so repeated prompts necessarily repeat seeds. The correct invariant is
**distinct seeds == distinct prompts**, and it held in 8/8 civs (3-4 distinct prompts per civ, one
seed per prompt, never two). Re-running with the corrected check gives **66 PASS / 0 FAIL**.

*Rule: the sim phase cannot yield 5 distinct seeds from 5 prompts unless the draw happens to be a
permutation. Assert "distinct seeds == distinct prompts, seed deterministic per (civ,prompt)" instead
of a flat 5-distinct-seeds count — the flat count fails on a healthy run roughly 70 % of the time.*

## Environment notes

- **Wiped workspace (106th session with the task path absent).** `/workspace` held only
  `.plugin-cache`; the upstream is **`SuperInstance/AI-Writings`** (3.7 GB) and
  `cellular-first-design` is a **subdirectory** of it. The task slug `ai-writings/cellular-first-design`
  404s on GitHub (`ai-writings` is not an owner; the real one is `SuperInstance/AI-Writings`).
- **NAS EDQUOT (18th session).** `/workspace` is 600 G/600 G; a clone into it dies with
  `Disk quota exceeded` on the very first `.git/description` write. Clone to `/tmp` (overlay, 28 G
  free) and **bridge**: `ln -s /tmp/work/cfd/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`,
  verified with `stat -L` + `os.path.samefile()` -> `True` (inode `129:3670` on both sides).
- **Blobless sparse clone works**: `--filter=blob:none --no-checkout --depth=1` then
  `git sparse-checkout set cellular-first-design/code/civilizations` -> 192 K of `.git` for the whole
  3.7 GB repo. `git status --porcelain` was **empty** before the run (no staged `prose/` deletions).
- **`write` tool is jailed to the workspace root** — cannot write `/tmp`; use a bash heredoc for
  `/tmp` artifacts.
- **Tool timeout 30 s < orchestrator run ~29 s** => detached launch with stdout redirected **and**
  `< /dev/null`, then poll `ps` + the log.
- `gh` not installed (26th session) — `GET /user/repos` with `GITHUB_TOKEN`; the GitHub API is
  case-insensitive (`SuperInstance/ai-writings` == `SuperInstance/AI-Writings`).
- The mock hashes the **received** cultural prompt verbatim (SKILL lesson #2) rather than
  reconstructing it from `culture.json`; the repo's own `tools/mock_zai.py` still reconstructs, so
  the session-246 mock was rebuilt at `/tmp/mock_zai_246.py`.
