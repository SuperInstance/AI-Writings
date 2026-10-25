# Civ Orchestrator — Session 57 (2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

**Result:** 8 civs, **+80 ledger rows** (uniform **+10/civ**), **+5 `meta_log.jsonl`**,
**5 `Winner:` lines**, **0** all-2.0-default rows, **0** score errors,
**80/80** distinct `content_preview`, **0** cross-civ collisions.

**Baseline:** HEAD `351db9a2` (session 56) — ledger **2204** rows, `meta_log` **143**.
**After run:** ledger **2284** rows, `meta_log` **148**.

---

## 1. The credential gap — 22nd consecutive session

`ZAI_TOKEN` absent from env. Direct probe of
`https://api.z.ai/api/coding/paas/v4/chat/completions` with the sandbox token:

| probe | HTTP | body |
|---|---|---|
| 1 | **401** | `{"error":{"code":"401","message":"token expired or incorrect"}}` |
| 2 | **401** | same |
| 3 | **401** | same |

**401 (not 5xx) ⇒ endpoint healthy ⇒ credential gap, not outage.** 22nd identical result.
JEV live at `jev-1.14.0` (direct probe returned `quality 1.34`, `confidence 0.38` — a real
score, not the 2.0 default). `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` applied, as always.

### Unpatched run — inert, confirmed

```
=== Civilization batch: 8 civs x 5 sims each ===
[The Grounded] running 5 sims...   (…all 8…)
=== Civilization competitions: 5 prompts ===
EXIT:0
```

**0 `Winner:` lines. Ledger 2124 → 2124 (+0). meta_log 138 → 138 (+0).** Exit code 0.

> The per-civ sim lines print **before** the provider call — they are not evidence of work.
> **Assert on the row delta and the `Winner:` count, never on the exit code.**

**New this session:** the inert run still advanced `culture.json` `simulations_run`
(`civ-poetic` 224 → 234) while writing **zero** ledger rows, and rewrote
`leaderboard.json`. So the unpatched run is not a pure no-op — it **desynchronises the
registry counters from the ledger** and publishes a board whose `sims_run` does not match
any evidence of work. This is the mechanism that seeds the **260-row counter gap** below:
a single inert run inflates `simulations_run` by 10 per civ with no rows to back it.

## 2. Control B — 9th consecutive identical replication

`ZAI_TOKEN=<set>` + `ZAI_URL_OVERRIDE=http://127.0.0.1:8731/chat/completions`
(token gate left intact ⇒ a real HTTP request is genuinely attempted; the mock stands
**below** the failing line, so the control has full power).

| metric | expected | measured |
|---|---|---|
| ledger rows | +80 | **+80** (exactly +10/civ, uniform) |
| meta_log | +5 | **+5** |
| `Winner:` lines | 5 | **5** |
| all-2.0-default rows | 0 | **0** |
| rows with `error` | 0 | **0** |
| mock calls received | 80 | **80** |
| distinct `content_preview` | 80 | **80 of 80** |
| cross-civ preview collisions | 0 | **0** |
| distinct `avg_score` | — | 76 of 80; range 1.050–2.823, mean 1.9798 |
| JEV confidence | real | 0.070–0.970, mean 0.5138 |

## 3. Low relevance — five lenses, never merged

### Lifetime lenses (A/B/C from `leaderboard.json`; D from the full ledger)

| civ | A `rel/sim` | B raw rel | C win rate | D lifetime avg | E this-run avg | ledger rows |
|---|---|---|---|---|---|---|
| `civ-grounded` | **1.510** | **406.23** | 0.221 | **1.572** | **1.645** | 312 |
| `civ-formal` | 1.651 | 420.92 | 0.165 | 1.705 | 1.726 | 297 |
| `civ-engineer` | 1.724 | 420.58 | 0.086 | 1.747 | 1.673 | 266 |
| `civ-precise` | 1.844 | 451.71 | 0.525 | 1.856 | 1.865 | 261 |
| `civ-therapist` | 1.910 | 471.80 | 0.017 | 1.947 | 1.992 | 264 |
| `civ-mythic` | 1.929 | 480.20 | 0.034 | 1.975 | 2.318 | 269 |
| `civ-whimsical` | 2.035 | 531.24 | 0.024 | 2.174 | 2.271 | **324** |
| `civ-poetic` | 2.171 | 551.42 | **0.008** | 2.228 | 2.348 | 291 |

**Lowest by lens:** A `civ-grounded` · B `civ-grounded` · C `civ-poetic` ·
D `civ-grounded` · E `civ-grounded`.

### `civ-grounded` is last on 4 of 5 lenses — and the standing "longevity artefact" explanation is WRONG

Sessions 6–56 have repeatedly explained Grounded's last place as **a longevity artefact**:
"it ran the most sims, and a lifetime-average denominator punishes that."

**This session falsifies that explanation, and the same data has falsified it before.**

```
Pearson r(ledger_rows, relevance_per_sim) = -0.067
most-run civ  = civ-whimsical (324 rows)
board-last civ = civ-grounded   (312 rows)
```

The correlation between "how many sims a civ ran" and its board score is **essentially
zero** (−0.067), and **the board-last civ is not the most-run civ** — Whimsical ran 12 more
rows than Grounded and sits 2nd. A denominator effect cannot produce a last place for a
civ that did not run the most.

**What Grounded's scores actually look like** (this run, n=10):

| civ | qual | nov | align |
|---|---|---|---|
| `civ-grounded` | 0.731 | **2.386** | **1.819** |
| `civ-engineer` | 0.759 | 1.671 | 2.588 |
| `civ-formal` | 0.689 | 1.833 | 2.656 |
| `civ-precise` | 0.814 | 1.839 | 2.943 |

Grounded has **high novelty and low alignment** — a **voice-misfit signature**, not a
longevity one. Its `voice_emphasis` is `"warm, factual"` with tenets
`concrete images / everyday language / specific examples / no abstractions`; against the
canon prompts it produces competent but tonally flat prose that JEV scores as *novel* and
*not aligned*. It is a **genuine current-form weakness**, and it is stable across lenses
A, B, D and E simultaneously.

**Recommendation: retire the "longevity artefact" explanation from the standing report
set.** It has been repeated across ~10 sessions without a correlation test, and it points
the remediation in the wrong direction (wait for the average to recover) when the real
signal is a miscalibrated voice.

### The Poetic anomaly — 8th consecutive run

`civ-poetic` is **1st of 8 on every quality lens** (rel/sim 2.171, raw rel 551.42,
lifetime avg 2.228, this-run avg 2.348, this-run quality **1.380** — highest of 8) and
**last on win rate** (0.008, 1W/117L). Corroborated across sessions 6, 7, 8, 52, 53, 54,
55, 56, 57. **Win rate measures selection appeal, not relevance** — the chooser sees only
the first 150 chars of `content_preview` and never the scores.

### Chooser vs `argmax(avg_score)` — still uncorrelated

Over all **148** `meta_log` rounds: **26 agree / 122 disagree = 17.6 %** agreement.
This run alone: **1 agree / 4 disagree**.

| prompt | argmax | chooser |
|---|---|---|
| what a cell is | `civ-mythic` (2.54) | `civ-mythic` |
| bookkeeper's role | `civ-poetic` (2.69) | `civ-precise` |
| witness log | `civ-poetic` (2.82) | `civ-grounded` |
| ternary values | `civ-poetic` (2.26) | `civ-formal` |
| JEV as a decision oracle | `civ-poetic` (2.33) | `civ-formal` |

`civ-poetic` was the argmax on **4 of 5** prompts and was chosen **0 times**.

### No extinction risk

Lowest relevance `civ-grounded` **+406.23** vs the `relevance < -10` retirement threshold.
`extinction_and_birth()` only runs under `--loop` every third iteration; a single-shot
run never triggers it.

### Counter gap — 260 rows, unchanged

Ledger **2284** vs registry `simulations_run` **2024** = **260 uncounted committed rows**
(per-civ 16–63). Root cause unchanged: `save_state()` rewrites `culture.json` from
in-memory counters with no lock and no read-modify-write ⇒ lost-update race. **Section 1
shows how an inert run manufactures part of this gap.**

## 4. Method corrections

### `cmp` against a process substitution is a FIFO race — it reports FALSE failures

The standing restore check is `cmp -s file <(git show HEAD:path)`. **`cmp` opens the FIFO
and the regular file concurrently; when it reads the FIFO first it can hit EOF/short-read
and report a difference on byte-identical files.**

Observed: 16 of 27 files reported `FAIL` while `git status --porcelain` was **empty** and
`git cat-file -s` matched `stat -c%s` exactly.

**Fix — materialise the blob to a real file first:**
```bash
git show HEAD:$BASE/civ-$c/simulations.jsonl > /tmp/verify/blob
cmp -s "$BASE/civ-$c/simulations.jsonl" /tmp/verify/blob
```
Re-run with this: **27/27 identical, 0 differing.** A false-negative restore check is
worse than none — it invites a needless "the tree is dirty" conclusion and a spurious
rebase.

### The GitHub core API quota was exhausted mid-session — plan for it

`api.github.com/repos/.../commits/main` returned **403 "API rate limit exceeded"** while
`git ls-remote` still worked. **Use `git ls-remote origin main` for the remote SHA, not
the API**, and note that the `search` quota is separate from the `core` quota.

### `git fetch --depth 1 <sha>` then `git cat-file` — the object is not present

A `--depth 1` fetch of a specific SHA updates `FETCH_HEAD` but the parent/tree objects
may be absent, so `git cat-file -t <sha>` fails and `git reset --hard <sha>` errors with
"Could not parse object". **Fetch the branch (`git fetch origin main`) after the
`ls-remote` gives you the SHA**, or fetch the exact SHA *and* verify with
`git cat-file -t` before resetting. Also: I mistyped the SHA once (truncated) and got
`remote error: upload-pack: not our ref` — a mistyped SHA and a rate-limited API look
identical if you only read the error text. Always confirm with `git ls-remote`.

## 5. Session 57 state

- HEAD `351db9a2` (session 56), rebased onto before the run.
- All 8 `simulations.jsonl`, all 8 `culture.json`, all 8 `witness.log`, `meta_log.jsonl`,
  `leaderboard.json`, `civilizations.json` restored from git blobs and **byte-identical to
  HEAD** (verified with `cmp` against materialised blobs — **27/27**).
- Report: `RUN_REPORT_2026-10-24_session57.md`.
