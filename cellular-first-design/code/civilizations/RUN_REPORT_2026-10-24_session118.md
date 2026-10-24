# RUN REPORT — Civilization Orchestrator — session 118 — 2026-10-24

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Result:** exit 0, 8 civs × 5 sims + 5 competitions, all 8 `simulations.jsonl` advanced by exactly +10 rows.
**Mode:** Control B (mock z.ai bridge) — see "Credential" below. **Mock-limited**: provider text is synthetic, so the *competition ordering and per-run avg_score spread are not quality measurements*. The lifetime leaderboard columns remain valid.

## Environment

- Fresh sandbox; `/workspace/repos/...` absent at start. NAS 100 % full (600 G/600 G, 0 avail) — **EDQUOT trap total**, 5th session running.
- Upstream owner is `SuperInstance/AI-Writings` (3.7 GB), not `ai-writings/cellular-first-design` (404s). `gh` still not installed — 5th session running.
- Bridge: filtered clone to `/tmp/aw` (overlay), then
  `ln -sfn /tmp/aw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`.
  Verified by `stat -L -c '%d:%i'` == `stat -c '%d:%i'` → `129:12653` on both sides, plus `-ef` → OK.
  Target = the **nested** `cellular-first-design` dir; tree not flattened.
- `TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` exported — the script reads `TYPESAFEAI_KEY`, the sandbox stores `TYPESAFE_AI_TOKEN`.
- Launched detached (`setsid nohup timeout -s KILL 300 … &`), polled via `ps` + log; the ~45 s run exceeds the 30 s tool timeout.

## Credential

- **z.ai: no credential.** `POST https://api.z.ai/api/coding/paas/v4/chat/completions` → **HTTP 401** `token expired or incorrect`. Endpoint healthy ⇒ credential gap, not outage. `ZAI_TOKEN` absent from env and from all sandbox secrets. 5th session running.
- **JEV: live.** `POST https://api.typesafe.ai/v1/systemone` with a deliberately wrong `questions` shape → **HTTP 422** `dict_type` = payload-shape complaint = token accepted. (422 is proof of liveness, not of failure.)
- ⇒ **Control B**: local mock bridge on `127.0.0.1:8799`, reached via `ZAI_URL_OVERRIDE` **plus** a non-empty `ZAI_TOKEN` (the override alone is dead code — the token gate returns `None` first).

## Mock integrity — the session-117 degeneracy is FIXED

The session-117 mock seeded on the **first 8 alphanumeric chars** of the message, which are the civ-invariant prefix `YouAreA` for every civ ⇒ all 8 civs emitted byte-identical text and the chooser was breaking a perfect tie. Session 117's "civ-precise won 5/5" was an arbitrary tie-break, not a signal.

**Fix applied:** seed from `md5(full message)`, so the civ-specific fields (`name`, `tenets`, `voice_emphasis`) change the response.

Verification (the diagnostic the RUNBOOK asked for) — for each competition prompt, count distinct `content_preview` across the 8 civs:

| prompt | distinct previews |
|---|---|
| what a cell is | 8/8 |
| the bookkeeper's role | 8/8 |
| the witness log | 8/8 |
| ternary values | 8/8 |
| JEV as a decision oracle | 8/8 |

40 competition rows, 40 unique previews, 40 unique `(prompt, civ)` pairs ⇒ **non-degenerate**. The competition results this session are a real test of the chooser, unlike any Control B run before session 118.

## Verification (asserted on rows, not exit code)

| civ | ledger rows before → after | Δ | mock-prefixed | provider | JEV `error` key |
|---|---|---|---|---|---|
| civ-grounded | 662 → 672 | +10 | 10/10 | zai | 0 |
| civ-whimsical | 674 → 684 | +10 | 10/10 | zai | 0 |
| civ-formal | 647 → 657 | +10 | 10/10 | zai | 0 |
| civ-poetic | 641 → 651 | +10 | 10/10 | zai | 0 |
| civ-precise | 611 → 621 | +10 | 10/10 | zai | 0 |
| civ-mythic | 619 → 629 | +10 | 10/10 | zai | 0 |
| civ-therapist | 614 → 624 | +10 | 10/10 | zai | 0 |
| civ-engineer | 616 → 626 | +10 | 10/10 | zai | 0 |

- `meta_log.jsonl` 323 → **328** (Δ +5). `Winner:` lines = **5**. Total new rows = **80**.
- Δ = +10 (not +45) confirmed: 5 sim-phase + 5 competition-phase rows per civ.
- sim→competition `ts` gap lands at index 4 in every civ file (1.7 s – 23.2 s) — both phases landed.
- **0 rows carry a JEV `error` key** ⇒ JEV really scored; the 2.0 silent default did not apply.
- All 8 `simulations.jsonl` show mtime 18:12; `leaderboard.json` and `meta_log.jsonl` re-written at 18:12:12.

## Leaderboard after this run

| civ | relevance | rel/sim | win_rate | W | L | sims | gen | temp |
|---|---|---|---|---|---|---|---|---|
| civ-poetic | 1183.51 | 1.928 | 0.017 | 5 | 298 | 614 | 1 | 0.80 |
| civ-whimsical | 1081.68 | 1.742 | 0.013 | 4 | 299 | 621 | 1 | 0.95 |
| civ-mythic | 1012.63 | 1.663 | 0.020 | 6 | 291 | 609 | 1 | 0.85 |
| civ-precise | 1001.64 | 1.656 | 0.490 | 146 | 152 | 605 | 1 | 0.20 |
| civ-therapist | 961.87 | 1.585 | 0.020 | 6 | 294 | 607 | 1 | 0.60 |
| civ-formal | 911.34 | 1.482 | 0.169 | 51 | 250 | 615 | 1 | 0.30 |
| civ-engineer | 907.80 | 1.503 | 0.098 | 29 | 267 | 604 | 1 | 0.40 |
| **civ-grounded** | **810.09** | **1.288** | 0.205 | 62 | 240 | 629 | 1 | 0.50 |

## Low-relevance civilizations

**`civ-grounded` (The Grounded) is the low-relevance civ** — last on the leaderboard and last on every lifetime score dimension:

| civ | quality | novelty | alignment | avg_score |
|---|---|---|---|---|
| **civ-grounded** | **0.673** (lowest) | 1.686 | **1.634** (lowest) | **1.331** (lowest) |
| civ-formal | 0.714 | **1.507** (lowest) | 2.331 | 1.517 |
| civ-engineer | 0.735 | 1.620 | 2.208 | 1.521 |
| civ-therapist | 0.764 | 2.017 | 2.046 | 1.609 |
| civ-precise | 0.765 | 1.636 | 2.595 | 1.665 |
| civ-mythic | 0.853 | 2.051 | 2.170 | 1.691 |
| civ-whimsical | 0.930 | **2.253** (highest) | 2.320 | 1.835 |
| civ-poetic | **1.141** (highest) | 2.162 | **2.597** (highest) | **1.967** (highest) |

This reproduces the standing finding for the **23rd consecutive session** (95–117). Two axes:
- **`civ-grounded`** — lowest on quality, alignment and avg_score. Alignment is the dimension the meta-GAN *selects* on, so this is structural, not noise.
- **`civ-formal`** — a distinct axis: lowest novelty.
- **`civ-precise`** — a third axis: lowest quality by a 0.010 rounding-width margin; not meaningful alone.

Inverse pair, also unchanged: **`civ-poetic`** is 1st on quality/alignment/avg_score but last on `win_rate` (0.017) — a *selection* failure, not a quality collapse. **`civ-precise`** is the other inverse: best `win_rate` (0.490), not first on quality.

**Standalone `win_rate` is not a quality metric.** The chooser reads JEV scores on the *text*; it does not read `avg_score`. In this run the chooser picked the lowest-`avg_score` candidate in 3 of 5 competitions (civ-grounded won three prompts while scoring 1.15, 1.13 and 1.67 against fields topping out at 1.79, 2.53 and 2.00) — so under session 118's non-degenerate mock, the chooser demonstrably does **not** track `avg_score`. This is now measurable rather than anecdotal.

**Extinction risk: NONE.** Threshold −10; lowest raw relevance +810.09, ~81× above. Registry 8 civs, `max_civs` 12. Extinction/birth only runs under `--loop` (not used).

**Counter gap persists.** Ledger rows exceed registry `simulations_run` by +16…+63 per civ (grounded +43, whimsical +63, formal +42, poetic +37, precise +16, mythic +20, therapist +17, engineer +22). `save_state()` rewrites `culture.json` with no lock ⇒ `relevance_per_sim` is **not recomputable from the ledger** by an auditor.

## Cleanup

Mock killed by exact-args PID match (both the `timeout` wrapper and the server; the `timeout` wrapper is a separate pid). Port verified closed afterwards (`curl` exit 7 = connection refused). No `pkill -f mock_zai` (self-match).

## Reproduction notes

`/tmp/mock_zai.py` — seed `md5(full message)[:8]`, content pool of 10 sentences, response prefix `[mock-zai seed=…]`. Index-wrap already correct (`h[(i*2)%32:(i*2)%32+2]`), so no session-112 `ValueError`. Probed with the orchestrator's exact long multi-sentence cultural prompt (not a one-word body) before the run: HTTP 200, 812-char body, prefix present, **0 tracebacks** in the mock's stdout.
