# RUN_REPORT_2026-10-24_session40

**Date:** 2026-10-24 (135th wipe)
**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Provider requested:** `zai` (z.ai / glm-4.5) · **JEV:** live at `jev-1.14.0`
**Verdict:** the requested command is a **no-op**. Under a transport-level control it produces
**+80 ledger rows, +5 `meta_log.jsonl` entries, 5 competition winners, 0 score errors** — but the
provider text is **mock**, so the committed ledger is left byte-identical to the remote and only
the report + learnings are committed.

---

## 1. The credential gap is still the whole story (20th consecutive session)

`ZAI_TOKEN` absent from env **and** from the 8-entry secret store. All 8 sandbox secrets re-tested
against `https://api.z.ai/api/coding/paas/v4/chat/completions`:

| secret | HTTP | body |
|---|---|---|
| MOTHQUANTUM_TOKEN | 401 | token expired or incorrect |
| TYPESAFE_AI_TOKEN | 401 | token expired or incorrect |
| MINIMAX_KEY | 401 | token expired or incorrect |
| NOTION_TOKEN | 401 | token expired or incorrect |
| NPMJS_TOKEN | 401 | token expired or incorrect |
| CRATES_TOKEN | 401 | token expired or incorrect |
| PYPI_TOKEN | 401 | token expired or incorrect |
| GITHUB_TOKEN | 401 | token expired or incorrect |

A **401** (not 5xx) means the endpoint is healthy ⇒ **credential gap, not outage**. JEV is live:
`https://api.typesafe.ai/v1/systemone` → `{"model":"jev-1.14.0", "quality": {"score": 0.29, "confidence": 0.77}}`.
Always `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` (the orchestrator reads `TYPESAFEAI_KEY`; the
sandbox exports `TYPESAFE_AI_TOKEN` — the name split persists).

**Unpatched run, measured not assumed:**

| metric | before | after | delta |
|---|---|---|---|
| ledger rows (8 civs) | 1644 | 1644 | **+0** |
| `meta_log.jsonl` | 108 | 108 | **+0** |
| `Winner:` lines | — | — | **0** |
| exit code | — | — | **0** |

The stdout showed the batch header and all 8 `[Name] running 5 sims...` lines, then the competition
header and **nothing**. The per-civ lines print *before* the provider call, so they are **not**
evidence of work. **Assert on the row delta, never on the exit code.**

## 2. Control B — 20th identical replication

`--sims 5 --prompts 5 --providers zai` with the provider URL redirected to a local mock
(`ZAI_URL_OVERRIDE`, the token gate left intact so the request is *really* attempted):

| metric | expected | observed |
|---|---|---|
| ledger rows | +80 (10/civ) | **+80**, uniform: `engineer 186→196, formal 217→227, grounded 232→242, mythic 189→199, poetic 211→221, precise 181→191, therapist 184→194, whimsical 244→254` |
| `meta_log.jsonl` | +5 | **+5** (108 → 113) |
| `Winner:` lines | 5 | **5** |
| mock calls | 80 | **80**, 0 fallbacks, 80 distinct salts |
| all-2.0-default rows (JEV outage default) | 0 | **0** |
| rows with a score error | 0 | **0** |
| distinct `content_preview` | 50–80 | **80/80**, 10/10 per civ |
| distinct `avg_score` | 50–80 | **72** |
| score spread | — | avg_score 1.343 – 2.797; quality 0.09–2.19, novelty 1.02–2.79, alignment 2.10–3.64 |

Mean sub-scores this run: quality 1.246 · novelty 2.114 · alignment 2.976.

### NEW DEFECT FOUND — the salt must be at the **START** of the body, not the end

The session-39 recipe says: *"Each response ends with a random integer (`[voice 200047]`) so the 8
previews are textually distinct."* **That is wrong, and it fails silently.**

The orchestrator stores only `content[:200]`:

```python
"content_preview": content[:200],
```

A salt appended at the **end** of the body is truncated away whenever the body is ≥ 200 chars, so
the preview collapses to the *body variants only*. Measured on the first Control B run:

| salt position | distinct `content_preview` | per-civ distinct | verdict |
|---|---|---|---|
| end of body (session-39 recipe) | **24 / 80** | 2/10 (except `civ-precise` 10/10) | **collapsed** |
| **start of body (fixed)** | **80 / 80** | 10/10 | healthy |

`civ-precise` was the only survivor at 10/10 because its bodies are short (< 200 chars), so the
salt was never truncated. **A short-bodied civ masks the defect** — the fleet-level distinct count
is the only reliable tell, and the per-civ minimum looked fine.

**Rule:** the salt must be the **first** token of the content, e.g. `[Your voice: lyrical, dense. 481920] A cell is …`.
Also assert `distinct(content_preview) >= 50` **and** `min(per-civ distinct) == 10`.

**Second-order lesson:** the session-9 acceptance check (`distinct preview 50–68`) is only
meaningful **if the salt is inside the truncated window**. "Distinct previews" and "distinct
underlying responses" are different quantities; the orchestrator only ever exposes the truncated one.

## 3. The low-relevance answer — four civs, five lenses, no single winner

`culture.json` (the registry) is the authoritative source, **not** the board.

| civ | rel/sim (board sort) | raw relevance | sims | win rate | W/L | lifetime avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|---|---|---|---|
| **civ-grounded** | **1.539** | 290.81 | 189 | 0.195 | 16/66 | **1.617** | 1.105 | 1.685 | **2.061** |
| civ-whimsical | 2.143 | 387.85 | 181 | 0.036 | 3/80 | 2.299 | 1.506 | 2.495 | 2.896 |
| civ-formal | 1.664 | 291.23 | 175 | 0.198 | 16/65 | 1.736 | 1.112 | **1.349** | 2.747 |
| civ-poetic | 2.235 | 388.82 | 174 | **0.012** | 1/82 | 2.302 | **1.663** | 2.315 | 2.926 |
| civ-precise | 1.850 | 305.31 | 165 | **0.513** | 40/38 | 1.867 | 1.166 | 1.510 | 2.926 |
| civ-mythic | 2.020 | 341.39 | 169 | 0.039 | 3/74 | 2.077 | 1.302 | 2.256 | 2.671 |
| civ-therapist | 1.954 | 326.30 | 167 | 0.025 | 2/78 | 2.002 | 1.232 | 2.177 | 2.598 |
| civ-engineer | 1.758 | **288.31** | 164 | 0.105 | 8/68 | 1.788 | **1.079** | 1.603 | 2.682 |

**Lowest on each lens:**

| lens | lowest | what it measures |
|---|---|---|
| `relevance_per_sim` (board sort) | **civ-grounded** 1.539 | lifetime average — penalises whoever ran most |
| raw relevance | **civ-engineer** 288.31 | accumulated score, same denominator artefact |
| win rate | **civ-poetic** 0.012 (1W/82L) | **selection appeal under a 150-char preview** |
| lifetime `avg_score` | **civ-grounded** 1.617 | actual writing quality — the only real quality lens |
| lifetime quality | **civ-engineer** 1.079 | substantive merit |
| lifetime novelty | **civ-formal** 1.349 | originality |
| lifetime alignment | **civ-grounded** 2.061 | voice fit |

**`civ-grounded` is the one to watch.** It is last on **three** lenses (the board's own sort key,
lifetime `avg_score`, and alignment — 2.061, which is 20 % below the next civ, `civ-therapist` at
2.598). It also ran the **most** sims (189, ledger 232) and *still* scores lowest, so it is **not**
a longevity artefact. Alignment is its own failure mode: the other seven civs sit at 2.598–2.926,
the Grounded is alone below 2.1.

**`civ-poetic` remains the flagship selection failure.** Highest lifetime `avg_score` (2.302),
**highest quality of all 8 (1.663)**, 1st on `rel_per_sim` (2.235), highest raw relevance (388.82) —
and **1 win in 82**. It is the best writer that the chooser never picks.

**`civ-engineer` is the sub-score weakling:** lowest raw relevance (288.31), lowest quality (1.079),
2nd-lowest `rel_per_sim`. Its 8 wins are selection, not quality.

**`civ-formal` is the mis-ranking magnet:** 2nd-lowest `rel_per_sim` (1.664), 2nd-lowest lifetime
`avg_score` (1.736), and **lowest novelty of all 8 (1.349)** — the same shape as last session.

**`civ-precise` is the inverse case:** best win rate (0.513, 40W/38L) but **last on this run's
`avg_score` (1.862)** and 5th lifetime. The chooser prefers it because it reads cleanly in 150
characters. It is the only civ whose relevance rank and win rate agree.

**This run's own ordering (5 competition rounds):** `civ-poetic` 2.746 › `civ-whimsical` 2.382 ›
`civ-mythic` 2.338 › `civ-therapist` 2.274 › `civ-engineer` 2.038 › `civ-grounded` 2.030 ›
`civ-formal` 1.934 › **`civ-precise` 1.862 (lowest)** — the Precise won **3 of 5 rounds** while
scoring **last**. The inverse relationship is as sharp as ever.

**Extinction risk: none.** `extinction_and_birth()` retires only below `relevance < -10`; the lowest
is **+288.31**, and it only runs in `--loop` mode every third iteration. A single-shot run never
triggers it.

## 4. Chooser vs argmax(avg_score) — 13th replication

**0/5 (0.0 %)** this session. In **all five** rounds the crowned civ was **not** the top scorer,
margins **0.64 – 1.25**. Lifetime agreement remains ~16 %.

The competition is a **separate JEV call** and the chooser **never sees the scores** — it reads a
**150-char preview** of each response:

```python
state += f"\n[{civ.culture['name']}]: {sim['content_preview'][:150]}\n"
body = {"questions": {"best_civ": {"type": "choice", ...}}}   # no scores
```

So the scorer grades the whole response and the chooser grades 150 characters. `win_rate` is a
**selection** metric. Never report it as quality, and never merge it with `relevance_per_sim`.

## 5. The counter gap — exactly +260, unchanged for the 20th session

| civ | ledger rows | registry `simulations_run` | gap |
|---|---|---|---|
| civ-grounded | 232 | 189 | +43 |
| civ-whimsical | 244 | 181 | +63 |
| civ-formal | 217 | 175 | +42 |
| civ-poetic | 211 | 174 | +37 |
| civ-precise | 181 | 165 | +16 |
| civ-mythic | 189 | 169 | +20 |
| civ-therapist | 184 | 167 | +17 |
| civ-engineer | 186 | 164 | +22 |
| **TOTAL** | **1644** | **1384** | **+260** |

`save_state()` rewrites `culture.json` from in-memory counters with **no lock and no
read-modify-write** ⇒ lost-update race ⇒ **`relevance_per_sim` is not a reproducible ranking**; an
auditor cannot recompute the board order from the ledger. Prefer win rate and `avg_score`.

## 6. The committed baseline already carries 560 mock rows

`grep -c "mock" civ-*/simulations.jsonl` on the **pristine committed** ledgers returns **70 rows
per civ (560 fleet-wide)** that never came from a live provider. `provider` is `zai` on all 1644
rows, so the field lies about provenance. Our own mock left **0** traces (`rows containing
'Your voice:'` = 0).

**The committed ledger is already partly mock** — a stronger reason than ever not to add more.
Check the *content*, not just the checksum.

## 7. Protocol compliance

- Baseline snapshot taken **before** any invocation (session-39 trap).
- Mock rows **not committed**; tree restored with `git checkout --`, then verified against the
  **live remote blob** (`raw.githubusercontent.com`) for all 21 files: **21/21 byte-identical,
  0 different**.
- `grep -c ZAI_URL_OVERRIDE civilization_orchestrator.py` = **0** after restore.
- `__pycache__` removed.
- Mock server killed; port 8765 confirmed closed.
- Committed: this report + the learnings addendum only.
