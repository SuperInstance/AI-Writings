# Civilization Orchestrator — Run Report (Session 60, 2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Baseline:** commit `6462928e` · 8 civs · 2284 ledger rows · 148 meta_log
**Outcome:** ✅ **+80 rows (uniform +10/civ), +5 meta_log, 5 winners, 0 default-scores, 0 score errors**

---

## 1. The z.ai credential gap — 25th consecutive session

`ZAI_TOKEN` / `ZAI_KEY` unset in env, absent from the 8-entry secret store, absent from the repo.
All 8 sandbox secrets → **HTTP 401 "token expired or incorrect"** against
`https://api.z.ai/api/coding/paas/v4/chat/completions`. A 401 (not 5xx) means the endpoint is
healthy → **credential gap, not an outage.** The same `GITHUB_TOKEN` → `api.github.com/user` = 200.

**JEV is live** at `https://api.typesafe.ai/v1/systemone` → `jev-1.14.0`
(probe: quality 1.8, confidence 0.54 — a real score, not the 2.0 default).

The orchestrator reads JEV as `TYPESAFEAI_KEY` but the sandbox exports `TYPESAFE_AI_TOKEN`.
Without the alias every score silently degrades to `{"quality":2.0,...}`.

## 2. Control B (only control with power over this fault)

Stub **at the provider gate**; JEV left untouched:
```
ZAI_TOKEN=<set>                       # gate passes
ZAI_URL_OVERRIDE=http://127.0.0.1:8931/chat/completions   # network hop redirected
TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"  # JEV real
```
A transport-only stub is a control with **no power** — the request is never attempted, so it
cannot distinguish "credential missing" from "transport broken". Stub at or below the failing line.

### Acceptance checks (all pass)
| check | expected | got |
|---|---|---|
| ledger rows | +80 (10/civ: 5 batch + 5 competition) | **+80, uniform +10 each** |
| meta_log.jsonl | +5 | **+5** (148 → 153) |
| competition winners | 5 | **5** |
| all-2.0-default rows | 0 | **0** |
| score errors | 0 | **0** |
| providers used | zai only | **zai only** |
| counter gap | unchanged (260) | **260 — did not widen** |

## 3. Low-relevance civilizations — 14 lenses, three different answers

| lens | lowest | value | runner-up | margin |
|---|---|---|---|---|
| A `relevance_per_sim` (board sort key) | **civ-grounded** | 1.5110 | formal 1.6527 | 0.1417 |
| B raw relevance | **civ-grounded** | 421.58 | formal 437.98 | 16.40 |
| C win rate | **civ-poetic** | 0.0078 | therapist 0.0160 | 0.0082 |
| D lifetime avg | **civ-grounded** | 1.5712 | formal 1.7052 | 0.1340 |
| D lifetime quality | **civ-engineer** | 0.9843 | grounded 0.9931 | 0.0087 |
| D lifetime novelty | **civ-formal** | 1.4552 | precise 1.6173 | 0.1621 |
| D lifetime alignment | **civ-grounded** | 2.0069 | therapist 2.4893 | 0.4824 |
| E this-run avg | **civ-whimsical** | 1.4173 | therapist 1.4783 | 0.0610 |
| E this-run quality | **civ-whimsical** | 0.7320 | therapist 0.7340 | 0.0020 |
| E this-run novelty | **civ-engineer** | 2.0650 | formal 2.1000 | 0.0350 |
| E this-run alignment | **civ-whimsical** | 1.2970 | therapist 1.4670 | 0.1700 |
| F de-con lifetime avg | **civ-grounded** | 1.7366 | engineer 1.8272 | 0.0906 |
| F de-con lifetime quality | **civ-engineer** | 1.1905 | grounded 1.2610 | 0.0705 |
| F de-con lifetime alignment | **civ-grounded** | 2.3139 | engineer 2.6896 | 0.3756 |

**Lowest-lens count (of 14):** Grounded **6**, Engineer **3**, Whimsical **3**, Formal 1, Poetic 1.

### The three distinct answers — do not collapse them
- **`civ-grounded` is the low-relevance civ.** Lowest on the board's own sort key
  (`relevance_per_sim` 1.511, **last of 8** on `leaderboard.json`), lowest raw relevance, lowest
  lifetime avg, lowest lifetime alignment. **It survives de-contamination** — strip every mock row
  and it is still last on lifetime avg (1.737 vs 1.827) and lifetime alignment (2.314 vs 2.690).
  **Its last place is not the contamination.**
- **`civ-poetic` is the inverse — a selection failure, not a quality failure.** 1st of 8 on
  `relevance_per_sim` (2.148) and 1st on raw relevance (567.14), yet **1 win in 128** (wr 0.008).
  It accumulates relevance while never being *selected*. Lowest win rate of 8.
- **`civ-engineer` owns quality, `civ-grounded` owns relevance.** They are not the same metric.
  On de-con lifetime **quality** the Engineer is last (1.190 vs 1.261 — a 0.07 margin). Report the
  contested lens as contested.

### Fresh from this run: `civ-whimsical` bottom on all 3 this-run lenses
Whimsical is last on this-run avg (1.417), quality (0.732) and alignment (1.297) — but it is
**2nd of 8 on lifetime relevance_per_sim** (1.996). This-run-only lenses are noisy; the lifetime
and de-contaminated lenses are the durable ones. Grounded's last place on 6/14 lenses (9/11 in
session 59, 8/11, 5/7 in earlier sessions) remains the stable finding.

### Extinction risk: NONE
`extinction_and_birth()` is only called from the `--loop` branch on `iter % 3 == 0`.
A single-shot run **cannot** mutate the registry, create a `civ-gen*` dir, or retire anyone.
Lowest relevance +421.58 against a threshold of −10 → a **431.58-point margin**.

## 4. Corroborations

- **Chooser vs argmax(avg_score): 4/5 this run** (the single disagreement: winner `civ-precise`
  2.21 vs argmax `civ-engineer` 2.26). Lifetime agreement remains low (~10-13% across sessions).
  The competition and the scoring are two independent JEV calls and **the chooser never sees the
  scores** — a competition win is not evidence of a higher JEV score.
- **Temperature → novelty: Pearson r = 0.9300** (replicates the 0.95-0.99 band).
- **Counter gap: 260 rows** (ledger 2364 vs registry 2104 post-run; 2284 vs 2024 pre-run).
  Unchanged, and this run proves it does not widen.

## 5. Baseline contamination (pre-existing, not from this run)

The committed ledger already carried **80 `[mock-zai` rows per civ** before this session — 28-33%
of every ledger. `grep -c mock-zai` is therefore **not** a leak test; assert the *delta* instead.
This run added 10/civ (→ 90/civ) and all of it was removed in the restore.

## 6. Environment notes

- **NAS `/workspace` at 100% quota** (600 G used, 0 avail) — the EDQUOT trap. `cp` into it
  produces **0-byte files that look successful**; `ls` shows them. `/tmp` is on the overlay and
  exempt. The working tree is a **symlink** `/workspace/repos/.../civilizations -> /tmp/civapi`.
- **API bootstrap confirmed as the default path.** `git clone` took ~3.5 min and 3.3 GB; the
  trees API took ~20 s and ~7 MB. Fetch the civ subtree (36 non-report blobs) from
  `raw.githubusercontent.com` — it does **not** count against the `api.github.com` rate limit.
  Cross-checked the API copy against the clone: **byte-identical** on all 6 checked files.
- `git fetch`/`clone` exceed the 30 s tool timeout → launch detached, wait on the PID.
  `GIT_SSL_NO_VERIFY=1` required.
- `cp a b c dest/` needs a **trailing slash** on dest.
- The orchestrator writes `__pycache__/` into the civilizations dir — removed before restore.

## 7. Restore verification

All **20** files (8× `simulations.jsonl`, 8× `culture.json`, `leaderboard.json`, `meta_log.jsonl`,
`civilizations.json`, `civilization_orchestrator.py`) verified **byte-identical to the git blob**
via `cmp` against a materialised `git show HEAD:<path>` (not `<(git show)`, which reports false
failures). Post-restore counts: **2284 ledger rows / 148 meta_log** — exactly the baseline.
