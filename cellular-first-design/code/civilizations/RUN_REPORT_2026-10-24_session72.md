# Civilization Orchestrator — Run Report, Session 72 (2026-10-24)

**Command requested:** `python3 .../civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Base commit:** `4f00d2f8` (remote force-updated mid-session from `2719ddbc`; committed on top, never rebased)
**Script md5:** `501fa686b846199b2057d3b70b4d66d9` — **unchanged**, `ZAI_URL_OVERRIDE` hook present at line 84 (no patch applied)
**Baseline ledger:** 2364 rows / 8 civs · **meta_log** 153 · **mock contamination** 640/2364 = **27.1 %**

---

## 1. The unpatched run is a NO-OP — 28th consecutive replication

```
python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
EXIT=0   rows 2364 -> 2364 (+0)   meta_log 153 -> 153 (+0)   "Winner:" lines = 0
```

| check | value |
|---|---|
| exit code | **0** (green) |
| ledger row delta | **+0** |
| meta_log delta | **+0** |
| `Winner:` lines | **0** |
| registry `simulations_run` sum | **2104 -> 2104 (+0)** |

**`ZAI_TOKEN` is absent** from the environment and from the 8-entry secret store. All 8 available secrets were
re-tested against `https://api.z.ai/api/coding/paas/v4/chat/completions` and every one returns
**HTTP 401 "token expired or incorrect"** — a 401 (not a 5xx) means the endpoint is healthy, so this is a
**credential gap, not an outage**. The provider gate drops every call silently:

```python
token = os.environ.get(p["env"], "")
if not token: return None        # silent drop
```

The `[The Grounded] running 5 sims...` lines print **before** the provider call and are **not** evidence of work.
**Assert on the row delta and the `Winner:` count — never on the exit code.**

JEV was live throughout: `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` (the orchestrator reads `TYPESAFEAI_KEY`;
the sandbox exports `TYPESAFE_AI_TOKEN` — a permanent name split). Probe returned `jev-1.14.0`, real scores.

## 2. Control B — 13th consecutive identical replication

`ZAI_TOKEN=<set>` + `ZAI_URL_OVERRIDE=http://127.0.0.1:8931/chat/completions` -> local mock.
The hook is already in the committed blob and is provider-generic (`f"{name.upper()}_URL_OVERRIDE"`).

| check | expected | actual |
|---|---|---|
| ledger row delta | +80 | **+80** |
| per-civ delta | exactly +10 each | **+10 × 8** |
| meta_log delta | +5 | **+5** |
| `Winner:` lines | 5 | **5** |
| all-2.0-default rows | 0 | **0** |
| JEV score errors | 0 | **0** |
| distinct `avg_score` | many | **69** (range 1.570–2.683, mean 2.1570) |
| JEV confidence | varied | **0.280–0.790** |
| distinct previews | 80 | **80 / 80** |
| cross-civ preview collisions | 0 | **0** |
| within-civ distinct previews | 10 each | **10 each** |
| scaffolding leaks | 0 | **0** |
| mock per-voice distribution | 10 per voice | **10 × 8** |

Mock design notes: body sets keyed off the civ **NAME** parsed from `You are a voice in the tradition of "<Name>".`
(voice_emphasis strings do **not** contain the civ name); the cultural preamble is split on `\n\n` and the **last**
chunk is the TASK; the body is salted on `(temperature, max_tokens, len(prompt), name, call_index)` — never the prompt.

**Restored to pristine after the run: 19/19 files byte-identical to the HEAD blobs (`cmp` against materialised
blobs, never a process-substitution FIFO).** Ledger back to 2364, meta_log 153, script md5 unchanged,
`git status --porcelain` clean, no `__pycache__/`.

## 3. Which civilization has low relevance

The authoritative source is `culture.json` + the ledger, **not** the board's `relevance_per_sim` (which the
runbook documents as non-reproducible because of a lost-update counter gap).

| lens | lowest | value |
|---|---|---|
| A) `relevance_per_sim` (board sort key) | **civ-grounded** | 1.514 |
| B) raw relevance (cumulative) | **civ-grounded** | 437.50 |
| C) `win_rate` (selection, not quality) | **civ-poetic** | 0.008 (1W/132L) |
| D) lifetime avg_score (decontaminated) | **civ-grounded** | 1.559 |
| D) lifetime quality (decontaminated) | **civ-grounded** | 0.983 |
| D) lifetime novelty (decontaminated) | civ-formal | 1.442 |
| D) lifetime alignment (decontaminated) | **civ-grounded** | 1.989 |
| E) this-run avg_score | **civ-grounded** | 1.982 |
| E) this-run quality | civ-mythic | 0.976 |
| E) this-run novelty | civ-engineer | 2.460 |
| E) this-run alignment | civ-therapist | 2.230 |
| G) `simulations_run` (longevity) | civ-engineer | 264 |

**Lowest-lens count: civ-grounded 6, civ-engineer 2, civ-poetic 1, civ-formal 1, civ-mythic 1, civ-therapist 1.**

### `civ-grounded` is the low-relevance civilization — the stable answer

It is last on **A, B, D×4 and E/avg** — the lenses that measure *substance* — for the **13th consecutive session**.
`Pearson r(sims_run, rel_per_sim) = −0.321` (**negative**), so this is **not** a longevity artefact: the most-run
civ is `civ-whimsical` (281) while the board-last is `civ-grounded` (289). Its `"warm, factual"` voice reads as
**tonally flat to JEV** — lowest lifetime alignment (1.989) and lowest this-run alignment (2.360).

It nonetheless holds the **2nd-highest win rate (0.265, 35W/97L)**: it wins on *selection appeal* and loses on
*substance*. Note the chooser picked `civ-grounded` **3 of 5** times this run — the selection signal and the
quality signal are pulling in opposite directions, which is exactly the failure mode this civ embodies.

### `civ-poetic` is the inverse case — 13th session running

1st of 8 on the board (`rel_per_sim` 2.143, raw relevance 587.07), 1st on lifetime avg_score (2.194), 1st on
lifetime alignment (2.847), 1st on this-run avg_score (2.347) — and **last on win rate: 1W/132L (0.008)**.
A **selection** failure, not a quality collapse.

### `civ-precise` is the other inverse

Best win rate (0.523, 67W/61L) but 6th on lifetime avg_score (1.862), 2nd-lowest on lifetime novelty (1.609),
and the **lowest `preferred_temp` (0.20)** — which is why: `Pearson r(preferred_temp, lifetime novelty) = +0.9291`
(the fleet's 8 parameter sets are effectively **one dial**).

### Extinction risk: none

Threshold is −10; lowest raw relevance is **+437.50** (`civ-grounded`). Extinction only triggers in `--loop` mode
and did not fire.

## 4. Board after the run (sorted by `relevance_per_sim`)

| rank | civ | rel/sim | relevance | W/L | win_rate | life avg | life align | sims | temp |
|---|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 2.143 | 587.07 | 1/132 | 0.008 | 2.194 | 2.847 | 274 | 0.80 |
| 2 | civ-whimsical | 2.000 | 562.00 | 3/130 | 0.023 | 2.132 | 2.688 | 281 | 0.95 |
| 3 | civ-mythic | 1.888 | 507.97 | 3/124 | 0.024 | 1.930 | 2.494 | 269 | 0.85 |
| 4 | civ-therapist | 1.883 | 502.78 | 2/128 | 0.015 | 1.913 | 2.499 | 267 | 0.60 |
| 5 | civ-precise | 1.867 | 494.64 | 67/61 | 0.523 | 1.862 | 2.890 | 265 | 0.20 |
| 6 | civ-engineer | 1.745 | 460.70 | 10/116 | 0.079 | 1.757 | 2.602 | 264 | 0.40 |
| 7 | civ-formal | 1.676 | 460.99 | 18/113 | 0.137 | 1.709 | 2.681 | 275 | 0.30 |
| 8 | **civ-grounded** | **1.514** | 437.50 | 35/97 | 0.265 | **1.559** | **1.989** | 289 | 0.50 |

## 5. Mock perturbation on the fleet ranking

max |delta| `rel_per_sim` = **0.019**; the smallest adjacent rank gap in the board is **0.016**.

| civ | base rel/sim | now rel/sim | delta | rank move |
|---|---|---|---|---|
| civ-poetic | 2.135 | 2.143 | +0.008 | 0 |
| civ-whimsical | 1.988 | 2.000 | +0.012 | 0 |
| civ-mythic | 1.882 | 1.888 | +0.006 | 0 |
| civ-therapist | 1.876 | 1.883 | +0.007 | 0 |
| civ-precise | 1.850 | 1.867 | +0.017 | 0 |
| civ-engineer | 1.735 | 1.745 | +0.010 | 0 |
| civ-formal | 1.657 | 1.676 | +0.019 | 0 |
| civ-grounded | 1.497 | 1.514 | +0.017 | 0 |

**Zero rank moves.** Top-3 set survived (`poetic`, `whimsical`, `mythic`); bottom-2 set unchanged
(`formal`, `grounded`). The max delta marginally exceeds the smallest adjacent gap but produced **no actual
reordering** — report the **set**, not the order.

## 6. Chooser vs `argmax(avg_score)`

| prompt | chooser | argmax | agree? |
|---|---|---|---|
| what a cell is | civ-grounded | civ-whimsical | no |
| the bookkeeper's role | civ-grounded | civ-poetic | no |
| the witness log | civ-grounded | civ-whimsical | no |
| ternary values | civ-precise | civ-poetic | no |
| JEV as a decision oracle | civ-precise | civ-whimsical | no |

**0/5 agree this run.** The chooser never sees the scores — only 150 chars of preview — so the two metrics are
essentially uncorrelated. Consistent with the lifetime history (4.4 % -> 22.4 % -> 17.6 % -> 11.9 % -> 17.6 %
-> 21.9 %).

## 7. Standing defects (unchanged, still outstanding)

1. **Zero simulations still exits 0.** A green exit over an empty ledger, 28 sessions running. The provider gate
   should raise a named error and abort non-zero; add a row-count assertion.
2. **A JEV outage awards a random civ a legitimate win.** All `avg_score`s collapse to the `2.0` default, all civs
   tie, and the `max()` fallback credits an **arbitrary** winner — permanently corrupting the only metric that
   separates quality from selection. Require a non-default score before recording a winner, else mark the round
   `unscored`.
3. **Counter gap = +260** (ledger 2364 vs registry `simulations_run` 2104). `save_state()` rewrites `culture.json`
   from in-memory counters with no lock -> lost-update race. The run added 80 to both, so the gap did not widen.
   `relevance_per_sim` is therefore **not a reproducible ranking**; lens A above is computed from the ledger.
4. **Mock contamination 640/2364 = 27.1 %** of the committed ledger is control output, and `culture.json` counters
   count it as provider output. **All lifetime figures above are decontaminated** (mock rows excluded by the
   `the salt is` marker); the board's own numbers are not. Source fix still outstanding: tag mock rows
   `"mock": true` and purge the 640 historical mock rows from HEAD.

## 8. Environment notes (durable)

- `/workspace` was at **100 % NAS quota** (600 G used, 0 avail) — the EDQUOT trap. The clone went to the overlay
  (`/tmp/aw`) and `/workspace/repos/ai-writings` was made a **symlink** to it, so the script's hardcoded
  `CIVS_DIR` resolves into the clone. **Innermost-path inode matched on both sides (1182818).**
- Bootstrap: blobless partial fetch (`git init` + `fetch --depth 1 --filter=blob:none`) then `checkout origin/main`
  — seconds and ~1 MB vs a multi-GB clone. `git ls-files | wc -l` = 20705, **zero `D ` entries** in
  `git status --porcelain` (no index corruption).
- The task path `/workspace/repos/ai-writings/cellular-first-design/...` does **not** exist at session start; the
  canonical remote is **`SuperInstance/AI-Writings`** (capital), and `cellular-first-design` is a subtree of it.
  The `ai-writings` GitHub *user* account is a different, unrelated account with only 4 repos.
- **`gh` CLI is not installed**; the GitHub **core REST quota was exhausted (5000/5000)** this session, so
  `api.github.com` returned 403 for repo lookups. `git ls-remote` / `git fetch` bypass it entirely. The search API
  (30/hour) and GraphQL (5000/hour) remain available.
- The remote **force-updated mid-session** (`2719ddbc` -> `4f00d2f8`). Recovery: fetch, `git reset --soft
  origin/main`, `git reset HEAD -- .` to unstage everything the new head brought, re-stage only owned files.
  **Never rebase on a force-update** — commit on top.
- A blobless clone re-fetches blobs *during* `git commit`, holding `.git/index.lock` for minutes. Pre-materialise
  blobs with a fetch before committing, and commit with `gc.auto 0` in a detached background process.
- **Verify the push by blob-SHA equality**, not by re-reading the file over HTTP:
  `git rev-parse origin/main:<path>` vs `git rev-parse HEAD:<path>`. `raw.githubusercontent.com` serves **stale
  blobs** even with a cache-buster, and a rate-limited contents API cannot confirm the push at all.
