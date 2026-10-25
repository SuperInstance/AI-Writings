# RUN_REPORT_2026-10-24_session41

**Date:** 2026-10-24 (136th wipe)
**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Provider requested:** `zai` (z.ai / glm-4.5) · **JEV:** live at `jev-1.14.0`
**Verdict:** the requested command is a **no-op**. Under a transport-level control it produces
**+80 ledger rows, +5 `meta_log.jsonl` entries, 5 competition winners, 0 score errors** — but the
provider text is **mock**, so the committed ledger is left byte-identical to the remote and only
the report + learnings are committed.

---

## 1. The credential gap is still the whole story (21st consecutive session)

`ZAI_TOKEN` absent from env. All 5 reachable secrets re-tested against
`https://api.z.ai/api/coding/paas/v4/chat/completions`:

| secret | HTTP | body |
|---|---|---|
| MOTHQUANTUM_TOKEN | 401 | token expired or incorrect |
| TYPESAFE_AI_TOKEN | 401 | token expired or incorrect |
| MINIMAX_KEY | 401 | token expired or incorrect |
| GITHUB_TOKEN | 401 | token expired or incorrect |

A **401** (not 5xx) means the endpoint is healthy => **credential gap, not outage**. JEV is live:
`https://api.typesafe.ai/v1/systemone` -> `{"model":"jev-1.14.0", "quality": {"score": 1.22, "confidence": 0.41}}`.
Always `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` (the orchestrator reads `TYPESAFEAI_KEY`; the
sandbox exports `TYPESAFE_AI_TOKEN` — the name split persists).

### NEW FINDING — a no-op run still rewrites `leaderboard.json`

Control A produced **zero** simulations, yet `leaderboard.json` was **modified** on disk:

```diff
-  "ts": 0,
-  "iso": "2026-10-23T22:26:00",
+  "ts": 1792804354.8267663,
+  "iso": "2026-10-24T01:12:34",
```

`update_leaderboard()` is called unconditionally at the end of `run_civilization_batch()`, so the
board is rewritten with a **fresh timestamp and identical civ rows** even when every provider call
failed. The committed `ts: 0` was a **sentinel** meaning "never successfully computed"; a failed
run silently converts that sentinel into a real timestamp, which makes a **never-ran** board
indistinguishable from a **ran-but-scored-nothing** board.

**Rule:** after a no-op run, **restore `leaderboard.json` too**, not just the ledgers. A board
whose `ts` advanced while the ledger did not is a detectable artifact — check it:

```bash
git diff --stat cellular-first-design/code/civilizations/leaderboard.json
```

If the only diff is `ts`/`iso`, the run produced nothing and the timestamp is a lie.

### Unpatched run, measured not assumed

| metric | before | after | delta |
|---|---|---|---|
| ledger rows (8 civs) | 1644 | 1644 | **+0** |
| `meta_log.jsonl` | 108 | 108 | **+0** |
| `Winner:` lines | — | — | **0** |
| exit code | — | — | **0** |
| `leaderboard.json` | ts=0 sentinel | ts=1792804354 | **rewritten** |

The stdout showed the batch header and all 8 `[Name] running 5 sims...` lines, then the competition
header and **nothing**. The per-civ lines print *before* the provider call, so they are **not**
evidence of work. **Assert on the row delta, never on the exit code.**

## 2. Control B — 21st identical replication

`--sims 5 --prompts 5 --providers zai` with the provider URL redirected to a local mock
(`ZAI_URL_OVERRIDE`, the token gate left intact so the request is *really* attempted):

| metric | expected | observed |
|---|---|---|
| ledger rows | +80 (10/civ) | **+80**, uniform: `engineer 186->196, formal 217->227, grounded 232->242, mythic 189->199, poetic 211->221, precise 181->191, therapist 184->194, whimsical 244->254` |
| `meta_log.jsonl` | +5 | **+5** (108 -> 113) |
| `Winner:` lines | 5 | **5** |
| mock calls | 80 | **81** (80 sims + 1 explicit pre-run liveness probe) |
| all-2.0-default rows (JEV outage default) | 0 | **0** |
| rows with a score error | 0 | **0** |
| distinct `content_preview` | 50-80 | **80/80** |
| min per-civ distinct | 10 | **10/10** (all eight civs) |
| distinct `avg_score` | 50-80 | **74** |
| distinct salts | 80 | **80** |

Score spread: `avg_score` 0.800 - 2.090; quality 0.01-1.53, novelty 1.34-2.77, alignment 0.20-3.10.
Mean sub-scores this run: quality 0.431 · novelty 2.178 · alignment 1.799.

The session-40 salt-placement fix held: salt at the **start** of the body => **80/80** distinct
previews, no collapse. The `min(per-civ distinct) == 10` assertion is what catches a short-bodied
civ masking a fleet-level collapse.

### NEW SHAPE — the chooser crowned 5 *different* civs, and 4 of 5 were low scorers

| round | chooser crowned | top scorer | chosen | top | margin |
|---|---|---|---|---|---|
| 1 | `civ-precise` | `civ-poetic` | 1.64 | 1.94 | 0.30 |
| 2 | `civ-whimsical` | `civ-poetic` | 1.30 | 1.55 | 0.25 |
| 3 | `civ-therapist` | `civ-formal` | 1.31 | 2.09 | 0.78 |
| 4 | `civ-poetic` | `civ-precise` | 1.41 | 1.71 | 0.30 |
| 5 | `civ-engineer` | `civ-whimsical` | 1.14 | 1.80 | 0.66 |

**0/5 (0.0 %)** agreement — the **14th replication**. In **all five** rounds the crowned civ was
**not** the top scorer, margins **0.25 - 0.78** (narrower than the 0.64-1.25 of session 40).

Note the **shape**: 5 rounds -> **5 distinct winners** (precise, whimsical, therapist, poetic,
engineer). Only 3 of 8 civs (`civ-mythic`, `civ-formal`, `civ-grounded`) were never crowned, and
`civ-grounded` is the **lowest**-scoring civ in the fleet on both lifetime and this-run lenses. The
chooser is not merely mis-weighted — it is close to **uniformly random over the field**, and its
sample of 5 covered 5 of 8 civs. Previous sessions saw concentration; this one saw spread. Both
are the same defect: the chooser reads a 150-char preview with no score information.

## 3. The low-relevance answer — `civ-grounded` is last on three lenses; `civ-poetic` is the selection failure

`culture.json` (the registry) is the authoritative source, **not** the board.

| civ | rel/sim (board sort) | raw relevance | sims | win rate | lifetime avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|---|---|---|
| **civ-grounded** | **1.522** | 302.97 | 199 | 0.184 | **1.617** | 1.105 | 1.685 | **2.061** |
| civ-formal | 1.655 | 306.27 | 185 | 0.186 | 1.736 | 1.112 | **1.349** | 2.747 |
| civ-engineer | 1.732 | **301.32** | 174 | 0.111 | 1.788 | **1.079** | 1.603 | 2.682 |
| civ-precise | 1.845 | 322.81 | 175 | **0.494** | 1.867 | 1.166 | 1.510 | 2.926 |
| civ-therapist | 1.921 | 340.02 | 177 | 0.035 | 2.002 | 1.232 | 2.177 | 2.598 |
| civ-mythic | 1.987 | 355.68 | 179 | 0.037 | 2.077 | 1.302 | 2.256 | 2.671 |
| civ-whimsical | 2.109 | 402.73 | 191 | 0.045 | 2.299 | 1.506 | 2.495 | 2.896 |
| **civ-poetic** | **2.205** | **405.74** | 184 | **0.023** | **2.302** | **1.663** | 2.315 | 2.926 |

**Lowest on each lens:**

| lens | lowest | value | what it measures |
|---|---|---|---|
| `relevance_per_sim` (board sort key) | **civ-grounded** | 1.522 | lifetime average — penalises whoever ran most |
| raw relevance | **civ-engineer** | 301.32 | accumulated score, same denominator artefact |
| win rate | **civ-poetic** | 0.023 | **selection appeal under a 150-char preview** |
| lifetime `avg_score` | **civ-grounded** | 1.617 | actual writing quality — the only real quality lens |
| lifetime quality | **civ-engineer** | 1.079 | substantive merit |
| lifetime novelty | **civ-formal** | 1.349 | originality |
| lifetime alignment | **civ-grounded** | 2.061 | voice fit |
| **this run (5 rounds)** | **civ-engineer** | 1.160 | live mock run |

**`civ-grounded` is the one to watch.** It is last on **three** lenses (the board's own sort key,
lifetime `avg_score`, and alignment — 2.061, which is **21 % below** the next civ,
`civ-therapist` at 2.598; the other seven sit at 2.598-2.926). It also ran the **most** sims
(199) and *still* scores lowest, so it is **not** a longevity artefact. Alignment is its own
failure mode: it is alone below 2.1.

**`civ-poetic` remains the flagship selection failure.** Highest lifetime `avg_score` (2.302),
**highest quality of all 8 (1.663)**, 1st on `rel_per_sim` (2.205), highest raw relevance (405.74) —
and **1 win in 43**. It is the best writer that the chooser never picks. It was crowned once this
session, and even then it was *not* the top scorer (round 4: chosen 1.41 vs `civ-precise` 1.71).

**`civ-engineer` is the sub-score weakling:** lowest raw relevance (301.32), lowest quality (1.079),
2nd-lowest `rel_per_sim`, and **lowest on this run's `avg_score` (1.160)** — yet it was crowned in
round 5 while scoring 1.14 against a top of 1.80. Its wins are selection, not quality.

**`civ-formal` is the mis-ranking magnet:** 2nd-lowest `rel_per_sim` (1.655), 2nd-lowest lifetime
`avg_score` (1.736), and **lowest novelty of all 8 (1.349)** — the same shape as last session.

**`civ-precise` is the inverse case:** best win rate (0.494) but 5th lifetime `avg_score` (1.867).
It was crowned in round 1 while scoring 1.64 against `civ-poetic` 1.94. It is the only civ whose
relevance rank and win rate roughly agree.

**Extinction risk: none.** `extinction_and_birth()` retires only below `relevance < -10`; the lowest
is **+301.32**, and it only runs in `--loop` mode every third iteration. A single-shot run never
triggers it.

## 4. Chooser vs argmax(avg_score) — 14th replication

**0/5 (0.0 %)** this session. The competition is a **separate JEV call** and the chooser **never
sees the scores** — it reads a **150-char preview** of each response:

```python
state += f"\n[{civ.culture['name']}]: {sim['content_preview'][:150]}\n"
body = {"questions": {"best_civ": {"type": "choice", ...}}}   # no scores
```

So the scorer grades the whole response and the chooser grades 150 characters. `win_rate` is a
**selection** metric. Never report it as quality, and never merge it with `relevance_per_sim`.

## 5. The counter gap — exactly +260, unchanged for the 21st session

| civ | ledger rows | registry `simulations_run` | gap |
|---|---|---|---|
| civ-grounded | 232 | 199 | +33 |
| civ-whimsical | 244 | 191 | +53 |
| civ-formal | 217 | 185 | +32 |
| civ-poetic | 211 | 184 | +27 |
| civ-precise | 181 | 175 | +6 |
| civ-mythic | 189 | 179 | +10 |
| civ-therapist | 184 | 177 | +7 |
| civ-engineer | 186 | 174 | +12 |
| **TOTAL** | **1644** | **1464** | **+260** |

`save_state()` rewrites `culture.json` from in-memory counters with **no lock and no
read-modify-write** => lost-update race => **`relevance_per_sim` is not a reproducible ranking**; an
auditor cannot recompute the board order from the ledger. Prefer win rate and `avg_score`.

## 6. The committed baseline already carries 560 mock rows

`grep -c "mock" civ-*/simulations.jsonl` on the **pristine committed** ledgers returns **70 rows
per civ (560 fleet-wide)** that never came from a live provider. `provider` is `zai` on all 1644
rows, so the field lies about provenance. Our own mock left **0 traces** after restore
(`rows containing 'Your voice:'` = 0).

**The committed ledger is already partly mock** — a stronger reason than ever not to add more.
Check the *content*, not just the checksum.

## 7. Protocol compliance

- Baseline snapshot taken **before** any invocation (session-39 trap).
- Mock rows **not committed**; tree restored with `git checkout --`, then verified against the
  **live remote blob** (`raw.githubusercontent.com`) for all 81 files in the civ subtree:
  **69/69 non-empty files byte-identical, 0 different**; the 12 remaining are **0-byte files
  confirmed empty on the remote too** (HTTP 200, size 0). API tree confirms `truncated: false`.
- `grep -c ZAI_URL_OVERRIDE civilization_orchestrator.py` = **0** after restore.
- `__pycache__` removed.
- Mock server killed; port 8765 confirmed closed.
- **`leaderboard.json` restored** (the `ts`-only diff caught by the new check).
- Committed: this report + the learnings addendum only.
