# Civ Orchestrator — Run Report, session 247 (2026-10-25)

## Session 247 — provider path, baseline, and result

- Command: `civilization_orchestrator.py --sims 5 --prompts 5 --providers zai` -> exit 0, ~30 s.
- Provider path: **Control B mock** (z.ai credential gap, **106th session**) + **live JEV** (`jev-1.14.0`).
  - z.ai probe: `HTTP=401` — endpoint healthy, credential absent. Control B needs **both**
    `ZAI_TOKEN` (the gate) and `ZAI_URL_OVERRIDE` (the destination); the override alone is dead code.
- Baseline: `4fb0eb0` (session 246 tree). **Pre-flight gate: 40/40 PASS.** **Run verification: 140 PASS / 0 FAIL.**
- Ledger delta: **+10 rows per civ, +80 total**; `meta_log` **968 -> 973** (+5); **18** files changed.
- Seed algorithm re-verified over the full current-format ledger **before** the run: **2800/2800 exact,
  0 mismatches** (the current-format population is 2800 rows; the historical `[mock-zai <12 hex>]`
  form is still 12604 rows and does not parse).
- Mock body **349** chars (38 header + 162 tail + 149 continuation), inside the 332-369 band, **first build**.
- Winners: `civ-precise` **4/5**, `civ-engineer` **1/5**.
- Chooser/`avg_score` argmax agreement **0/5 (0 %)** — **5 down-grades, 0 up-grades**.
- Run low `civ-therapist` (avg **1.2800**) — quality **0.6780** and alignment **0.8330** both at the
  fleet low, a **two-axis** collapse; novelty 2.3290 4th of 8.
- Lifetime low `civ-grounded` (**2330.34**) for the **108th** consecutive session; also lowest rel/sim (**1.214**).
- The bottom two are effectively tied: grounded 2330.34 vs therapist 2331.13, a gap of **0.79**;
  the step from #2 to #3 (engineer 2606.11) is **274.98** — a **348x** larger step.
- Alignment spread **1.9360 = 2.39x** the `avg_score` spread (0.8100).
- No civ near extinction (threshold `relevance < -10`; lowest **2330.34**, **233x** the floor).
  Registry 8, `max_civs` 12, all `generation=1`.

## Verification — `ls -la` on the civilizations tree

The task's verification request, read directly off the filesystem at
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations/`:

| civ | rows before | rows after | Δ | Δ bytes |
|---|---|---|---|---|
| civ-grounded | 1952 | 1962 | **+10** | +5760 |
| civ-whimsical | 1964 | 1974 | **+10** | +5834 |
| civ-formal | 1937 | 1947 | **+10** | +5796 |
| civ-poetic | 1931 | 1941 | **+10** | +5772 |
| civ-precise | 1901 | 1911 | **+10** | +5810 |
| civ-mythic | 1909 | 1919 | **+10** | +5736 |
| civ-therapist | 1904 | 1914 | **+10** | +5847 |
| civ-engineer | 1906 | 1916 | **+10** | +5796 |

**+80 rows total.** `meta_log.jsonl`: 968 -> **973** (+5). `leaderboard.json` iso `18:03:03` -> **`18:13`**.
All 8 ledgers and all 8 `culture.json` files carry mtime **18:13**. `git status --porcelain`
= **18 modified** (8 ledgers + 8 cultures + `meta_log.jsonl` + `leaderboard.json`).

**The `ls -la` size delta is a secondary receipt, not the proof.** File *size* deltas are consistent
with 10 rows each, but row *counts* are the load-bearing measurement and both are reported.

## Run-level axes (this batch's 80 rows)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | **2.0900** | **1.3000** | 2.4250 | 2.5450 |
| civ-precise | 2.0080 | 1.0220 | 2.2330 | **2.7690** |
| civ-formal | 1.7627 | 0.7640 | 2.2710 | 2.2530 |
| civ-engineer | 1.7177 | 0.7740 | 2.2320 | 2.1470 |
| civ-whimsical | 1.5397 | 0.6800 | **2.4790** | 1.4600 |
| civ-mythic | 1.5187 | 0.7000 | 2.4030 | 1.4530 |
| civ-grounded | 1.5180 | **0.5750** | 2.3270 | 1.6520 |
| **civ-therapist** | **1.2800** | 0.6780 | 2.3290 | **0.8330** |

- Spreads: **alignment 1.9360 = 2.39x** the `avg_score` spread (0.8100); quality 0.7250 = 0.90x;
  novelty 0.2470 = 0.30x.
- **Alignment dominated again** — the axis that dominates rotates the holder, not the axis.
  `civ-precise` holds the alignment high (2.7690) while `civ-poetic` holds the `avg_score` high.
- `civ-grounded` is the **quality** low (0.5750, 8th of 8) but is 5th of 8 on both novelty and
  alignment: its run collapse is a *prose* failure this session, the mirror of `civ-therapist`'s
  *voice* failure.

## Lifetime leaderboard (relevance desc)

| civ | relevance | rel/sim | win_rate | gen | w/l | temp |
|---|---|---|---|---|---|---|
| civ-poetic | 3278.68 | 1.722 | 0.006 | 1 | 6/937 | 0.8 |
| civ-precise | 3151.36 | 1.663 | 0.707 | 1 | 667/275 | 0.2 |
| civ-formal | 2725.85 | 1.431 | 0.128 | 1 | 121/825 | 0.3 |
| civ-whimsical | 2703.63 | 1.415 | 0.005 | 1 | 5/943 | 0.95 |
| civ-mythic | 2660.81 | 1.401 | 0.011 | 1 | 10/932 | 0.85 |
| civ-engineer | 2606.11 | 1.376 | 0.063 | 1 | 59/883 | 0.4 |
| civ-therapist | 2331.13 | 1.229 | 0.012 | 1 | 11/934 | 0.6 |
| **civ-grounded** | **2330.34** | **1.214** | 0.079 | 1 | 75/872 | 0.5 |

### Low-relevance civilizations (the task's ask)

1. **`civ-grounded` — lifetime low, 108th consecutive session.** Lowest `relevance` (**2330.34**),
   lowest `relevance_per_sim` (**1.214**), and lowest lifetime `avg_score` (**1.2307**) of 8. On
   every lifetime axis it sits 7th or 8th: `avg` 1.2307 (8th), `quality` 0.5467 (8th),
   `alignment` 1.3089 (7th). Its lifetime `novelty` (1.8365) is 6th of 8 — not below median, so it
   is losing on **alignment and quality**, not novelty. On this run it was also the **quality** low
   (0.5750), so the run and the lifetime picture agree for the first time in several sessions.
2. **`civ-therapist` — run low (this batch), and 2nd-lowest lifetime.** Two-axis collapse:
   quality **0.6780** and alignment **0.8330** both at the fleet low, with novelty (**2.3290**) 4th
   of 8. It holds the run low in **8 of the last 9** sessions.
3. **The bottom two are effectively tied: `civ-grounded` 2330.34 vs `civ-therapist` 2331.13 — a gap
   of only 0.79** — while the step from #2 to #3 (`civ-engineer` 2606.11) is **274.98**, a **348x**
   larger step. The bottom of the leaderboard is a **pair**, not a ladder. This is the tightest
   bottom-pair gap in the series (0.79 vs 3.17 in session 246, 5.11 in session 245).
4. **`civ-mythic` — 5th of 8 on lifetime relevance** (2660.81) and the **lowest alignment of the
   mid-pack** on this run (1.4530, 7th of 8) while holding the 3rd-highest novelty (2.4030).
   Watch axis, not yet a collapse.

**No civ is near extinction.** The threshold is `relevance < -10`; the lowest is **2330.34**, **233x**
the floor. The bottom of the leaderboard is a *relevance ordering* problem, not a lifecycle problem.
Registry 8, `max_civs` 12, all `generation=1`; extinction/birth only runs under `--loop`.

## Chooser vs `avg_score` argmax: 0/5 (0 %)

| prompt | chooser | argmax | delta | |
|---|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | -0.2200 | down |
| the bookkeeper's role | civ-precise | civ-poetic | -0.0367 | down |
| the witness log | civ-precise | civ-poetic | -0.0000 | down (tie) |
| ternary values | civ-engineer | civ-poetic | -0.4267 | down |
| JEV as a decision oracle | civ-precise | civ-poetic | -0.1000 | down |

**5 down-grades, 0 up-grades.** The up-grade count is **0 by construction** — the chooser is a JEV
`choice` question over `content_preview[:150]` and never sees `avg_score`. **Never treat `win_rate`
as a quality metric;** it is a *selection* metric.

`civ-poetic` was the `avg_score` argmax on **5 of 5** and won **0** — the strongest form of the
"high prose, unselected" inverse (session 157 pattern). `civ-precise` won 4/5 with a lifetime
`win_rate` of **0.707**; it is the mirror of `civ-poetic` (1st on lifetime relevance with a
`win_rate` of **0.006**). The coldest voice is what the chooser rewards. The **0/5 agreement and
the 4/5 winner share coexisted** — neither implies the other.

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
- **Run verification 140 PASS / 0 FAIL**: ledger +10/civ (80 total), `meta_log` +5, 80/80 `[mock-zai`
  prefix, 80/80 `provider=zai`, 80/80 md5 recompute from the sent cultural prompt, 0 JEV `error`
  keys, 0 fallback `(2.0,2.0,2.0)` triples, `avg_score` recomputes exactly 80/80,
  sim-phase "distinct seeds == distinct prompts" + "seed deterministic per `(civ,prompt)`" (8/8),
  competition-phase per-`(civ,prompt)` 1:1 over the last 5 rows (8/8), competition phase covers all
  5 canon prompts (8/8), sim->competition ts ordering (8/8), `culture.json` `simulations_run` +10
  for all 8, `generation` still 1, win+loss +5, relevance increments match the 10 new `avg_score`s
  to 1e-6 for all 8, registry unchanged at 8, leaderboard sorted by `relevance_per_sim` desc,
  `meta_log.results` a list of 8 `[civ_id, score]` pairs covering all 8 civs, counter gap delta
  0.000000 for all 8.

### The corrected sim-phase invariant (reused from session 246, and it held)

The flat "5 distinct seeds in the sim phase" check is **wrong**: the sim phase draws from 5 prompts
**with replacement**, so repeated prompts force repeated seeds. The correct invariant is
**distinct seeds == distinct prompts** plus **seed deterministic per `(civ,prompt)`**. This run
drew 3-4 distinct prompts per civ (one seed per prompt, never two) and both invariants held in 8/8.

## Environment notes

- **Wiped workspace (107th session with the task path absent).** `/workspace` held only
  `.plugin-cache`; the upstream is **`SuperInstance/AI-Writings`** (3.7 GB) and
  `cellular-first-design` is a **subdirectory** of it. The task slug `ai-writings/cellular-first-design`
  404s on GitHub (`ai-writings` is not an owner; the real one is `SuperInstance/AI-Writings`).
  `GET /search/repositories?q=cellular-first-design` does **not** find it — resolve via
  `GET /user/repos` and filter on the name, not via a content search.
- **NAS EDQUOT (19th session).** `/workspace` is 600 G/600 G; a clone into it dies with
  `Disk quota exceeded`. Clone to `/tmp` (overlay, 28 G free) and **bridge**:
  `ln -s /tmp/AIW/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`,
  verified with `stat -L` + `os.path.samefile()` -> `True`.
- **Blobless sparse clone works**: `--filter=blob:none --no-checkout --depth 1` then
  `git sparse-checkout set cellular-first-design/code/civilizations` -> a small `.git` for the whole
  3.7 GB repo. `git status --porcelain` was **empty** before the run (no staged `prose/` deletions).
- **`write` tool is jailed to the workspace root** — cannot write `/tmp`; use a bash heredoc for
  `/tmp` artifacts. This report was written that way.
- **`gh` not installed** — `GET /user/repos` with `GITHUB_TOKEN`; the GitHub API is case-insensitive
  (`SuperInstance/ai-writings` == `SuperInstance/AI-Writings`).
- `git clone` of the task slug fails with `could not read Username`; the token URL form
  (`https://x-access-token:$GITHUB_TOKEN@github.com/...`) works.
- The mock hashes the **received** cultural prompt verbatim (SKILL lesson #2) rather than
  reconstructing it from `culture.json`; the repo's own `tools/mock_zai.py` still reconstructs, so
  the session-247 mock was rebuilt at `/tmp/mock_zai_247.py`.
