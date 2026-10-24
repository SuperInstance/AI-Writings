# Civilization Orchestrator — Run Report (Session 19, 2026-10-23, 118th wipe)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Verdict:** Ran successfully under Control B — **+80 rows (10/civ, uniform), +5 `meta_log`,
5 competition winners, real JEV scores, 0 score errors.**

---

## 1. Environment reconstruction (118th consecutive wipe)

The task path did not exist at session start; `/workspace` held only `.plugin-cache`.

- Repo: `SuperInstance/AI-Writings` (3.7 GB pack; the `cellular-first-design` component
  is a **subdirectory**, not a repo). Located via the GitHub `search/code` endpoint.
- `gh` CLI not installed -> GitHub REST API with `$GITHUB_TOKEN`.
- NAS `/workspace` at **100 %** (600 G used, 0 avail) -> clone to `/tmp` (overlay, 28 G free).
- `CIVS_DIR` is **hardcoded** to `/workspace/repos/ai-writings/cellular-first-design/code/civilizations`,
  so the clone is bridged with
  `rm -rf /workspace/repos/ai-writings && ln -sfn /tmp/aiw /workspace/repos/ai-writings`.

Clone strategy: `git clone --filter=blob:none --no-checkout --depth 1` +
`git sparse-checkout set cellular-first-design/code/civilizations` — **seconds, one tool
call.** Full clones are unreliable (s18-B: pack deleted mid-write at 1.8 GB).

## 2. Credential audit — the gap is still the whole story (17th session)

| credential | status |
|---|---|
| `ZAI_TOKEN` (script) / `ZAI_KEY` (other repo code) | **absent** from env and from the 8-entry secret store |
| all 8 sandbox secrets vs `api.z.ai/.../chat/completions` | **every one 401** "token expired or incorrect" |
| JEV `api.typesafe.ai/v1/systemone` | **LIVE** — `jev-1.14.0`, HTTP 200, `quality.score 1.77` |

401 (not 5xx) => the z.ai endpoint is healthy => **credential gap, not an outage**.

### Control A — the unpatched command (the trap)

```
=== Civilization batch: 8 civs x 5 sims each ===
[8 per-civ "running 5 sims..." lines]
=== Civilization competitions: 5 prompts ===
                     <-- empty
PIPE_EXIT=0
```

**Exit 0 with a zero-row ledger.** Ledger **+0 rows (764 -> 764)**, `meta_log`
**+0 (53 -> 53)**, `Winner:` lines **0**. Only `leaderboard.json` was rewritten.
The provider gate returns `None` on a missing token and the caller drops the result
silently. **Assert on the row delta, never on the exit code.**

## 3. Control B — the run that produces work

Seam: one-line patch to `PROVIDERS["zai"]["url"]` (assert `src.count(old) == 1` first):

```python
"url": os.environ.get("ZAI_URL_OVERRIDE", "https://api.z.ai/api/coding/paas/v4/chat/completions"),
```

`git diff --stat` = **1 insertion, 1 deletion**. The `ZAI_TOKEN` gate, the request body,
and the entire JEV path are untouched. A local mock stands in for z.ai; JEV scoring is
real.

### Results

- **+80 rows**, exactly **10 per civ** across all 8 civs
- **+5 `meta_log` entries**, **5 competition winners** (grounded 1, precise 3, formal 1)
- winner-set cardinality **3** (not a sweep)
- **0** all-2.0-default rows, **0** score errors, **0** scaffolding leakage
- **80/80** distinct `content_preview`, **68/80** distinct `avg_score` (1.52-2.40)
- **80/80** distinct mock salts and body hashes; mock internal distribution
  **exactly 10 calls per voice across all 8 voices**
- all 80 rows carried the `Authorization` header and `thinking:{"type":"disabled"}`;
  **80 distinct temperatures** (the +/-0.2 per-call jitter is live)

## 4. Low-relevance civilizations (baseline-only, 764 committed rows)

| lens | lowest | value |
|---|---|---|
| `relevance_per_sim` (board sort key) | **civ-grounded** | 1.891 |
| raw relevance | **civ-engineer** | 109.33 (youngest, 54 sims) |
| `win_rate` (**selection** metric) | **civ-poetic** | **0.000 (0W/33L)** |
| lifetime `avg_score` | **civ-grounded** | 1.916 |
| lifetime `alignment` | **civ-grounded** | 2.659 (lowest of 8) |
| lifetime `quality` | **civ-engineer** | 1.667 |
| lifetime `novelty` | **civ-precise** | 1.020 |
| this-run `avg_score` | **civ-grounded** | 1.706 |
| this-run `quality` | **civ-grounded** | 0.471 |

- **`civ-grounded` — the answer to "which civilization has low relevance".** Last on
  `relevance_per_sim`, lifetime `avg_score` and lifetime `alignment`; worst in this run
  on `avg_score` and `quality`. A genuine quality signal, not the longevity artefact
  the `relevance_per_sim` denominator suggests (it ran the most sims, 89).
  **7th consecutive session with the same answer.**
- **`civ-poetic` — the inverse case, 17th session running.** 2nd of 8 on lifetime
  `avg_score` (2.617), **1st on quality (2.258)**, 2nd on alignment, 2nd on
  `relevance_per_sim` (2.618) — and **0 wins in 33**. A *selection* failure, not a
  quality collapse.
- **`civ-precise` — wins by being picked, not by scoring.** Best win rate in the fleet
  (0.643, 18W/10L) but **last on lifetime novelty (1.020)**.
- **`civ-whimsical` — the only civ where every quality lens agrees** (1st on
  `relevance_per_sim` 2.659, lifetime `avg_score` 2.701, novelty 2.602, alignment 3.365).
- **Extinction risk: none.** Threshold is -10, the lowest raw relevance is +109.33, and
  `extinction_and_birth()` only runs in `--loop` mode every third iteration — a
  single-shot run never triggers it.

## 5. Replications

- Control B: +80 / +5 / 5 winners / 0 defaults / 0 errors / 0 leak / 80-80 distinct
  previews / uniform 10-per-voice — **12th replication**.
- Chooser vs `argmax(avg_score)`: **1/5 this run (20 %)**, **11/53 lifetime (20.8 %)**,
  disagreement margins 0.020-0.553 — **11th replication**.
- Temperature vs lifetime JEV novelty: Pearson **r = 0.7942** (n=764, all pairs) —
  **11th replication**, but below the 0.972-0.985 band. The prior 10 replications used
  **per-civ means** (8 points); this session used all 764 pairs, which includes the
  within-civ jitter and attenuates r. **The estimators are not comparable** — not a
  structural change until confirmed.
- Lifetime **top-3 SET** {Whimsical, Poetic, Mythic} and **bottom-2 SET** {Grounded,
  Formal} on the board's sort key — **unchanged since session 11**. Report the set, not
  the order. (Computing these on *raw relevance* gives a different answer; the board
  sorts by `relevance_per_sim`.)
- Counter gap: **764 ledger rows vs 504 registry `simulations_run` = +260** (s18-A
  measured +180). `save_state()` rewrites `culture.json` from in-memory counters with no
  lock — a lost-update race that moves in both directions. **Report as measured.**

## 6. Cleanup

`git checkout HEAD -- cellular-first-design/code/civilizations/` restored every file
byte-identical to `HEAD`, verified with `cmp` against the git blobs: **9/9 files
identical** (8 `simulations.jsonl` + `meta_log.jsonl` + `leaderboard.json` + 8
`culture.json`). `__pycache__/` removed. The 80 mock rows never entered the committed
ledger. Only `CIV_ORCHESTRATOR_LEARNINGS.md` is modified (this session's additions).
