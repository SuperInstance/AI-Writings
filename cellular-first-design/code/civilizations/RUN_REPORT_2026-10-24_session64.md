# RUN REPORT — 2026-10-24 — session 64

**Task:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`,
verify `simulations.jsonl` files gained entries, report low-relevance civilizations.

**Base commit:** `030feb4f` ("civ-orchestrator skill: session 63 runbook deltas")
**Script md5:** `501fa686b846199b2057d3b70b4d66d9` — **unchanged** (no upstream patch needed)
**Provider:** `zai` · **JEV:** live at `jev-1.14.0`

---

## 0. Environment reconstruction

The task path did not exist at session start — `/workspace` held only `.plugin-cache`.
Rebuilt from **`SuperInstance/AI-Writings`** (canonical name is capitalised; the
lowercase form still redirects).

- NAS `/workspace` at **100 % quota** (600 G used, 0 avail) — the EDQUOT trap.
  A write test produced a **0-byte file with exit 0**; `read`/`write` tools fail
  with "Workspace path escapes Cloud Host root".
- Cloned to the **overlay** (`/tmp`, 28 G free) and bridged with a symlink:
  `ln -sfn /tmp/AI-Writings /workspace/repos/ai-writings`. `CIVS_DIR` is hardcoded
  to that path, so the symlink is what makes the script write into the clone.
- `git clone --depth 50` **died** with `invalid index-pack output` (3.4 GB
  transferred, tool timeout). `--depth 1 --single-branch` succeeded in ~2 min.
- **New failure worth recording:** the clone left a **stale `.git/index.lock` and
  no `.git/index`** (the first, aborted clone attempt had created the lock). The
  worktree files were present but the **index was empty** — `git ls-files` returned
  0, and `git status` reported all 105 civ-dir files as *staged deletions* (`D `).
  `git read-tree HEAD` rebuilds the index (~2 min on a 3.4 GB tree; run it in the
  background, it exceeds a 30 s tool call). **After any clone, assert
  `git ls-files | wc -l` is non-zero and `git status --porcelain` shows no
  `D ` entries before trusting the worktree.**
- `ZAI_URL_OVERRIDE` **is already in the committed blob** (lines 84–86 of the
  script, the Control B hook). The runbook still says to re-apply it each session
  — **that is now stale**; no patch was needed this session.

## 1. Baseline (unpatched run — the credential gap)

```
BEFORE rows=2284 meta=148
python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
exit: 0
AFTER  rows=2284 meta=148
DELTA rows=0 meta=0      Winner: lines = 0
```

**27th consecutive credential gap, reproduced exactly.** `ZAI_TOKEN` is absent
from the sandbox; `api.z.ai` returns **401 "token expired or incorrect"** (a 401
means the endpoint is healthy — a credential gap, not an outage). The orchestrator
**exits 0 while producing zero rows** — a green exit over an empty ledger. The
per-civ `[Name] running 5 sims...` lines print *before* the provider call and are
not evidence of work. **Assert on the row delta, never on the exit code.**

JEV was made live with `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` (the sandbox
exports `TYPESAFE_AI_TOKEN`; the script reads `TYPESAFEAI_KEY`). Without it JEV
silently degrades to the `{"quality": 2.0, ...}` default.

## 2. Control B — +80 / +5 / 5 winners

Stub **at the gate** (local mock on `127.0.0.1:8931`, `ZAI_URL_OVERRIDE` set,
`ZAI_TOKEN` set), JEV untouched.

```
BEFORE rows=2284 meta=148
AFTER  rows=2364 meta=153
DELTA rows=80  meta=5      Winner: lines = 5
```

| check | expected | observed |
|---|---|---|
| rows added | +80 | **+80** |
| per-civ distribution | +10 each × 8 | **uniform +10 each** |
| meta_log entries | +5 | **+5** |
| `Winner:` lines | 5 | **5** |
| all-2.0 default rows | 0 | **0** |
| score errors | 0 | **0** |
| cross-civ preview collisions | 0 | **0** |
| within-civ preview collisions | — | **0** |
| distinct previews | 80 | **80/80** |
| distinct `avg_score` | high | **71/80** (0.670–1.773, mean 1.1533) |
| JEV confidence | > 0 | **0.420–0.990** |
| scaffolding leak | 0 | **0** |
| mock per-voice call distribution | 10 each | **uniform 10 each, 80/80 distinct salts** |

**12th consecutive identical replication.** The mock keyed its body set off the
civ **name** in `tradition of "The X"` (not `voice_emphasis`, which does not
contain the name) and split the preamble on `\n\n` before parsing the topic, per
the runbook. The mock's own audit endpoint confirmed the 10-per-voice
distribution; a 81st call in the audit was the manual smoke test, not the run.

## 3. Low-relevance reading — 16 lenses, never merged

| lens | lowest | value |
|---|---|---|
| **A** `relevance_per_sim` (board sort key) | **`civ-grounded`** | 1.479 |
| **B** raw relevance | **`civ-grounded`** | 412.73 |
| **C** win rate | `civ-poetic` | 0.008 (1W/127L) |
| **D** lifetime avg | **`civ-grounded`** | 1.700 |
| **D** lifetime quality | `civ-engineer` | 1.140 |
| **D** lifetime novelty | `civ-formal` | 1.357 |
| **D** lifetime alignment | **`civ-grounded`** | 2.261 |
| **E** this-run avg | **`civ-grounded`** | 0.863 |
| **E** this-run quality | `civ-engineer` | 0.202 |
| **E** this-run novelty | `civ-formal` | 0.985 |
| **E** this-run alignment | **`civ-grounded`** | 1.032 |
| **F** de-con lifetime avg | **`civ-grounded`** | 1.700 |
| **F** de-con lifetime alignment | **`civ-grounded`** | 2.261 |
| **F** de-con lifetime quality | `civ-engineer` | 1.140 |
| **G** ledger avg (all rows) | **`civ-grounded`** | 1.544 |
| **H** `simulations_run` | `civ-engineer` | 254 |

**Lowest-lens count (quality lenses A, B, D×4, E×4, F×3, G):**
**`civ-grounded` 9 · `civ-engineer` 3 · `civ-formal` 2.**
(Session 61: Grounded 8, Formal 4, Engineer 2. Session 60: 6/14.)

### Answer: the low-relevance civilization is **`civ-grounded` (The Grounded)**

Bottom on **9 of 16 lenses** — every lens that measures *substance*. It is
**not** a longevity artefact: `Pearson r(sims_run, rel_per_sim) = −0.310`
(negative, so the most-run civ is not the lowest-scoring one; the most-run civ
is `civ-whimsical` at 271, the board-last is `civ-grounded` at 279 — and
`civ-grounded` has the **2nd-highest win rate (0.252)** while producing the
**lowest** scores). It wins on *selection appeal* and loses on *substance*:
its "warm, factual" voice reads as tonally flat to JEV — lowest lifetime
alignment (2.261) and lowest this-run alignment (1.032) of the eight.

### The Poetic anomaly holds for the 12th run

`civ-poetic` is **1st of 8** on every quality lens (A 2.126, B 561.22, D 2.305,
F-decon 2.305) and **last on win rate (0.008, 1W/127L)**. A *selection* failure,
not a quality collapse. `civ-precise` is the other inverse: best win rate
(0.528) but 4th on `rel_per_sim`.

### E moves session to session — report it per run, never as a constant

This run's E-bottom on quality/novelty was `civ-engineer` / `civ-formal`
(session 61's E-bottom was `civ-formal` on all three). **Grounded was E-bottom
on avg and alignment in both sessions** — that is the stable part.

### Extinction risk: none

Lowest relevance +412.73 vs threshold −10.

## 4. Secondary replications

- **Chooser vs `argmax(avg_score)`**: **1/5 this run** (chooser picked
  `civ-grounded` ×3, `civ-precise` ×2; argmax picked `civ-precise` ×3,
  `civ-engineer` ×2). Lifetime by exact score-multiset match: **7 agree /
  25 disagree = 21.9 %** (32/153 rounds had a unique score owner). History:
  4.4 % → 22.4 % → 17.6 % → 11.9 % → 17.6 % → **21.9 %**. The chooser sees
  only 150 chars of preview, never the scores — the two metrics remain
  essentially uncorrelated.
- **Temperature vs lifetime JEV novelty**: `r(preferred_temp, lifetime novelty)
  = +0.9371` (history 0.9845 / 0.9790 / 0.9722 / +0.9270). The 8 civs'
  `preferred_params` remain one dial.
- **Counter gap: +260, unchanged.** Ledger 2364 vs registry `simulations_run`
  2104. The run added 80 to both, so the gap held steady — it does not widen.
- **Mock contamination: 640 / 2364 = 27.1 %** of the committed ledger is
  `[mock-zai` rows. Every lifetime figure above is computed over a ~27 %
  synthetic baseline. Quote with that caveat.

## 5. Restore

All 18 files touched by the run (8 × `simulations.jsonl`, 8 × `culture.json`,
`meta_log.jsonl`, `leaderboard.json`) restored from the HEAD blobs and verified
**byte-identical with `cmp` against the materialised blob** — **105/105 files
in the civ subtree match, 0 mismatches**. Ledger back to 2284 rows, meta_log to
148, mock rows to 640, script md5 unchanged. `git status --porcelain` clean;
no `__pycache__/`.

## 6. Outstanding defects (unchanged, not fixed upstream)

1. **Zero simulations still exits 0.** The silent `return None` at the provider
   gate should be a named error + non-zero exit + a row-count assertion.
2. **A JEV outage awards a random civ a legitimate win.** All `avg_score`s become
   the `2.0` default, all civs tie, and the `max()` fallback picks an arbitrary
   winner — permanently corrupting the only metric that separates quality from
   selection. Require a non-default score before recording a winner; else mark
   the round `unscored`.
3. **The counter gap** (ledger rows vs `culture.json` `simulations_run`, +260,
   unchanged since session 6) — `save_state()` rewrites `culture.json` from
   in-memory counters with no lock → lost-update race. `relevance_per_sim` is
   **not a reproducible ranking**.
4. **Mock rows are not tagged.** Tag mock rows with `"mock": true` and purge the
   640 historical mock rows from HEAD; until then no lifetime statistic is clean.
5. **`civ-grounded` is bottom on 9 of 16 lenses and no one has acted on it.**
   The board's own sort key puts it last while the selection metric rewards it.

## 7. Session 64 additions

- **`ZAI_URL_OVERRIDE` is now upstream** (script lines 84–86). The runbook's
  "re-apply this one-line patch each session" instruction is **stale** — no
  patch was needed. Worth deleting from the skill to stop future sessions
  looking for it.
- **A stale `.git/index.lock` with a missing `.git/index` produces a
  worktree that looks fine but has an empty index.** Symptoms: `git ls-files`
  returns 0 and `git status` shows every file as a *staged* deletion (`D `).
  Fix: `rm -f .git/index.lock && git read-tree HEAD` (background it — it exceeds
  a 30 s tool call on a 3.4 GB tree). **Assert `git ls-files | wc -l > 0` after
  every clone.**
- **A force-update on the remote is now routine** (remote moved
  `030feb4f → 6a32efa1` mid-session, touching only `index.html` / `index.json`).
  `git diff --name-only HEAD origin/main -- <civ dir>` returned **0 files**, so
  committing on top of the remote head is clean. **No rebase** — per the
  runbook, commit on top and verify with `ls-remote` immediately before push.
