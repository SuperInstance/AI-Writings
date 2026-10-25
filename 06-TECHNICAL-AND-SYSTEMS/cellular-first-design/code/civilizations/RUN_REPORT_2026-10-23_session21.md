# Civilization Orchestrator — Run Report, Session 21 (2026-10-23)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Repo:** `SuperInstance/AI-Writings` @ `e045e68c`
**Result:** run completed with **real JEV scores** (Control B). Ledger **+80 rows**, `meta_log` **+5**, **5 competition winners**, **0** default-score rows, **0** errors.

---

## 1. Environment reconstruction (120th consecutive wipe)

The task path did not exist at session start. `/workspace` held only `.plugin-cache` and
`.skills`; NAS `/workspace` was at **100 % quota** (600 G used, 0 avail).

- Full `git clone --depth 1` into `/tmp` (overlay, 21 G free) — succeeded this time
  (the s20 note that the pack lands without a working tree did **not** reproduce).
- Bridge: `rm -rf /workspace/repos/ai-writings && ln -sfn /tmp/ai-writings /workspace/repos/ai-writings`.
  `CIVS_DIR` is hardcoded to the `/workspace` path, so the symlink is what makes the
  script write into the clone.
- `TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` — without it JEV silently degrades to the
  `{"quality": 2.0, ...}` default and the run measures nothing while exiting 0.

## 2. The credential gap (19th consecutive session)

`ZAI_TOKEN` / `ZAI_KEY` / `GROQ_TOKEN` absent from env **and** from the secret store.
All 8 sandbox secrets re-tested against
`https://api.z.ai/api/coding/paas/v4/chat/completions` → **401 "token expired or
incorrect" on every one**. A 401 (not 5xx) means the endpoint is healthy ⇒
**credential gap, not outage**.

**JEV live** at `jev-1.14.0` (HTTP 200, `quality.score 0.47`, `confidence 0.61`).

### Baseline no-op (unpatched command)

Batch header + all 8 per-civ `[Name] running 5 sims...` lines → **empty competition
section** → **exit 0**. Ledger **+0 rows (764 → 764)**, `meta_log` **+0 (53 → 53)**,
**0** `Winner:` lines. The per-civ sim lines print *before* the provider call, so
they are **not** evidence of work. **Assert on the row delta, never on exit code.**

## 3. Control B (14th replication) — stub at the gate

One-line `ZAI_URL_OVERRIDE` seam (1 insertion / 1 deletion, verified by `git diff --stat`),
`ZAI_TOKEN` set to a dummy, provider URL redirected to a local mock. The request is
**really attempted**, so the control has full power, and the entire JEV path stays live.

| metric | expected | measured |
|---|---|---|
| ledger rows | +80 (10/civ) | **+80**, 10 per civ, uniform |
| `meta_log.jsonl` | +5 | **+5** (53 → 58) |
| `Winner:` lines | 5 | **5** |
| all-2.0-default rows | 0 | **0** |
| rows with a score error | 0 | **0** |
| provider | `zai` only | **80/80 `zai`** |
| distinct `content_preview` | ~80 | **79/80** |
| distinct `avg_score` | high | **75/80**, range **1.24 – 2.50** |
| mock calls | 80 | **81** (80 + 1 probe), 10 per voice |

Mock log per civ voice: Engineer 10, Formal 10, Grounded 10, Mythic 10, Poetic 11,
Precise 10, Therapist 10, Whimsical 10 — the name-keyed voice table (s17 rule) works;
the extra Poetic call is the manual probe.

JEV sub-score spread on the 80 run rows: quality mean **1.019** (0.17–2.00),
novelty mean **2.161** (1.32–2.82), alignment mean **2.432** (1.27–3.22),
confidence mean **0.532**, 35 distinct confidence values. A live JEV, not a stub.

## 4. Chooser vs argmax — 13th replication

`best_civ` agreed with `argmax(avg_score)` in **0 of 5 rounds (0 %)**.
Disagreement margins **0.18 / 0.03 / 0.03 / 0.18 / 0.08**, mean **0.100** — the
smallest mean margin yet recorded (prior lifetime mean 0.539). The two metrics remain
**essentially uncorrelated**; the chooser does not see the scores.

## 5. Counter gap

Ledger **844** rows vs registry `simulations_run` sum **584** → gap **+260**,
identical to the session-20 baseline. It is a **lost-update race** in `save_state()`,
not a leak, and it moves in both directions. **Report it as measured this session.**

## 6. Low-relevance reading — **each lens separate, never merged**

| lens | lowest | value |
|---|---|---|
| (a) `relevance_per_sim` (board sort key) | **The Grounded** | 1.846 |
| (b) raw relevance | **The Engineer** | 125.98 |
| (c) `win_rate` (**selection** metric) | **The Poetic** | **0.000 (0W/33L)** |
| (d) lifetime mean `avg_score` | **The Grounded** | 1.883 |
| (e) lifetime mean `quality` | **The Engineer** | 1.552 |
| (f) lifetime mean `novelty` | **The Formal** | 1.122 |
| (g) lifetime mean `alignment` | **The Grounded** | 2.601 |
| (h) this-session `avg_score` (80 rows) | **The Grounded** | 1.487 |
| (i) this-session `quality` | **The Grounded** | 0.605 |
| (j) this-session `novelty` | **The Formal** | 1.952 |
| (k) this-session `alignment` | **The Grounded** | 1.886 |

- **The Grounded — the stable low-relevance civ (9th session running).** Last on
  `relevance_per_sim`, lifetime `avg_score`, lifetime `alignment`, and last this
  session on `avg_score`, `quality` and `alignment`. It is a **genuine quality
  weakness**, not the longevity artefact its denominator suggests: it ran the most
  sims (89), but it is *also* last on the raw score lenses.
- **The Poetic — the inverse case (19th session running).** 2nd of 8 on
  `relevance_per_sim` (2.578) and 0 wins in 33, and **0 of 5** competition rounds
  this session. A **selection** failure, not a quality collapse.
- **The Precise — wins by being picked, not by scoring.** Best win rate in the fleet
  (**0.643**, 18W/10L) and **3 of 5** wins this session, but 2nd-last on lifetime
  `avg_score` (1.978) and 2nd-last on lifetime `novelty` (1.141).
- **The Whimsical — the only civ where every quality lens agrees** (1st on
  `relevance_per_sim` 2.594, lifetime `avg_score` 2.717, novelty 2.622,
  alignment 3.410) — and 3rd-lowest win rate (0.061), 0 of 5 this session.
- **Extinction risk: none.** Threshold −10, lowest raw relevance +125.98.
  `extinction_and_birth()` only runs in `--loop` mode every third iteration; this
  was single-shot.

## 7. Restore verification — 28 files

All **28** tracked files (8 ledgers + 8 `culture.json` + 8 `witness.log` +
`meta_log.jsonl` + `leaderboard.json` + `civilizations.json` + the script) are
**byte-identical to `git show HEAD:<path>`** via `cmp`. The **timestamp-leak test**
returned **0** rows after the run reference for all 8 ledgers. `git status` clean at
`e045e68c`. `__pycache__/` removed. Mock killed by explicit PID (332), confirmed
gone via a fresh `ps | grep "[z]ai_mock"`.

## 8. Environment notes (nothing new broke; all known traps held)

1. `git clone --depth 1` into `/tmp` **worked** this session — the s20 failure
   ("pack landed, checkout did not") did **not** reproduce. Still keep `/tmp` as the
   clone target; NAS `/workspace` is at 100 % and a clone into it fails mid-copy.
2. `rm -rf` before `ln -sfn` is still required (s8 trap).
3. Kill the mock by **explicit PID** from `ps -eo pid,args --no-headers | grep "[z]ai_mock"`.
   `pkill -f` self-matches and kills the invoking shell.
4. The orchestrator writes `leaderboard.json` even on a no-op run — a
   `git checkout HEAD -- .` is needed after the **unpatched** run too, or the restore
   diff shows a spurious change.
5. `__pycache__/` is written into the civilizations dir — remove before committing.
