# Civ Orchestrator — Session 109 (2026-10-24T16:35:08Z)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

## 1. Setup

- Repo: `SuperInstance/AI-Writings` (NOT `ai-writings/cellular-first-design` — the latter 404s).
- NAS is 100% full ⇒ cloned to `/tmp`, bridged with a symlink to
  `/workspace/repos/ai-writings/cellular-first-design`; inode identity `129:10423` on both sides.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN` (script reads the former).
- JEV (`api.typesafe.ai`) live: HTTP 200. JEV scoring is **real** this session.

## 2. Control A (exact requested command) — silent no-op, as documented

`ZAI_TOKEN` absent ⇒ `call_provider()` returns `None` on every call ⇒
`run_simulation()` returns `None` ⇒ competition short-circuits on `if not results: return None`.
Result: **exit code 0, +0 rows on all 8 civs, +0 meta_log rows, 0 competitors.**
Exit code is not evidence. Only row counts are.

z.ai endpoint itself is healthy: `401 {"error":{"message":"token expired or incorrect"}}` ⇒ credential gap, not outage.

## 3. Control B (mock provider bridge) — real meta-GAN run

Requires **both** `ZAI_TOKEN` (placeholder ok) and `ZAI_URL_OVERRIDE`; the token gate runs
first in `call_provider()`, so the override alone yields 0 provider calls.

```
export ZAI_TOKEN="mock-local-bridge"
export ZAI_URL_OVERRIDE="http://127.0.0.1:8799/api/coding/paas/v4/chat/completions"
```

### Verification (assert on rows, not exit code)

| civ | pre | post | delta |
|---|---|---|---|
| civ-engineer | 526 | 536 | +10 |
| civ-formal | 557 | 567 | +10 |
| civ-grounded | 572 | 582 | +10 |
| civ-mythic | 529 | 539 | +10 |
| civ-poetic | 551 | 561 | +10 |
| civ-precise | 521 | 531 | +10 |
| civ-therapist | 524 | 534 | +10 |
| civ-whimsical | 584 | 594 | +10 |

Total **+80 rows** (8 civs × 10), `meta_log.jsonl` **+5**, **5** `Winner:` lines.
All 80 rows: `provider=zai`, `mock-zai` content prefix, **0 JEV errors**.
Winner tally: `civ-precise` 4, `civ-formal` 1.

## 4. Low-relevance civilization: `civ-grounded` (The Grounded) — 15th consecutive session

**Lifetime (leaderboard after run):**

| civ | relevance | rel/sim | win_rate |
|---|---|---|---|
| civ-poetic | 1079.03 | 2.059 | 0.016 |
| civ-whimsical | 1005.20 | 1.893 | 0.016 |
| civ-mythic | 943.09 | 1.817 | 0.020 |
| civ-therapist | 914.03 | 1.768 | 0.024 |
| civ-precise | 909.28 | 1.766 | 0.462 |
| civ-engineer | 851.54 | 1.657 | 0.104 |
| civ-formal | 841.14 | 1.602 | 0.176 |
| **civ-grounded** | **761.24** | **1.412** | 0.222 |

`civ-grounded` is last on lifetime `relevance` **and** lifetime `relevance_per_sim`.
Extinction risk **NONE** (threshold −10; lowest raw relevance +761.24). Registry 8 civs, `max_civs` 12.

### This run's lens (deltas vs session 108)

`civ-grounded` is **4th of 8** on this run's `avg_score` (0.667) and **4th of 8** on
`alignment` (0.908) — **it did NOT finish last this run.** The structural finding is
lifetime, not per-run. This reproduces session 106's shape: the low-relevance civ is
not the run's minimum.

### This-run JEV means

| civ | quality | novelty | alignment | avg |
|---|---|---|---|---|
| civ-formal | 0.390 | 0.877 | **1.611** | **0.959** |
| civ-precise | 0.331 | 0.766 | 1.451 | 0.849 |
| civ-engineer | 0.323 | 0.786 | 1.205 | 0.771 |
| civ-grounded | 0.320 | 0.774 | 0.908 | 0.667 |
| civ-therapist | 0.218 | 1.166 | 0.320 | 0.568 |
| civ-mythic | 0.193 | 1.201 | 0.255 | 0.550 |
| civ-poetic | 0.191 | 1.159 | 0.281 | 0.544 |
| civ-whimsical | 0.140 | 1.274 | 0.215 | 0.543 |

Run minimum on this lens is `civ-whimsical` (lowest quality, lowest alignment,
lowest avg) — a *different* civ from the lifetime low (`civ-grounded`).
`civ-formal` leads on alignment and avg, the inverse of its session-108 shape.

## 5. Chooser vs `avg_score` argmax

**4/5 = 80% agreement** (session 108: 1/5). Lifetime baseline ≈ 15% agreement.
Sample size 5 — treat as noise-level, not a trend.

## 6. Known issues carried forward

- **Credential gap:** `ZAI_TOKEN` still absent from env and all 8 sandbox secrets.
- **Counter gap:** ledger rows exceed registry `simulations_run` (`save_state()` rewrites
  `culture.json` with no lock ⇒ `relevance_per_sim` is not recomputable from the ledger).
- `civ-poetic` remains the stable inverse (highest relevance, lowest win_rate).
- `civ-precise` is the other inverse (highest win_rate 0.462, lowest novelty).
