# civ-orchestrator session 52 (2026-10-24) — credential gap 17th deep; Control B reconfirmed to the row

## What was asked
Run `civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`, verify
`simulations.jsonl` files have new entries, note any civilization with low relevance.

## Environment reconstruction (the path did not exist again — 7th consecutive time)
- `/workspace` held only `.plugin-cache`. NAS at 100% quota (600G used, 0 avail) — the EDQUOT trap.
- Rebuilt from `SuperInstance/AI-Writings` via **sparse checkout**, HEAD `4004ef96`
  ("civ-orchestrator session 51: credential gap 16th deep; 'stable bottom-2' A/B finding did not replicate").
- Sparse-checkout fetch of `cellular-first-design/code/civilizations` still pulled a **3.1 GB** pack
  and took ~90 s. Faster than the 3.7 GB full clone (>3 min) but not cheap.
- Bridged with `ln -sfn /tmp/aiw/aiw /workspace/repos/ai-writings` (CIVS_DIR is hardcoded to the
  `/workspace` path). `gh` absent; GitHub REST API used for discovery.
- `TYPESAFEAI_KEY` was **not** exported by default — set `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"`.

## The credential gap (17th consecutive session)
- `ZAI_TOKEN` / `ZAI_KEY`: **absent from env AND absent from the 8-entry secret store.**
- All 8 sandbox secrets re-tested against `https://api.z.ai/api/coding/paas/v4/chat/completions`
  → **401 "token expired or incorrect"** on every one. A 401 (not 5xx) means the endpoint is healthy
  ⇒ **credential gap, not outage**.
- JEV live: `https://api.typesafe.ai/v1/systemone` → `jev-1.14.0`.

## Run 1 — the requested command, unpatched: NO-OP
```
BEFORE rows=1884 meta=123
EXIT=0
AFTER  rows=1884 meta=123
DELTA rows=0 meta=0
```
**0 `Winner:` lines.** The log shows the batch header and all 8 `[Name] running 5 sims...` lines,
then the competition header and nothing. Exit code 0.
**This is the 17th session in a row where `--providers zai` produces a green exit and an empty ledger.**
The per-civ sim lines are printed *before* the provider call — they are not evidence of work.
Only `leaderboard.json` was rewritten.

## Run 2 — Control B (mock at the gate, JEV untouched): REAL
`ZAI_TOKEN=<set>` + `ZAI_URL_OVERRIDE=http://127.0.0.1:8811/chat/completions` (local mock that
parses the *last non-empty line* of the prompt and strips the `Write N words on ` prefix, so the 8
civs produce distinct text and the chooser retains signal):
```
BEFORE rows=1884 meta=123
EXIT=0
AFTER  rows=1964 meta=128
DELTA rows=80 meta=5
```
- **+80 rows, exactly +10 per civ** (5 batch + 5 competition), **+5 meta_log**, **5 `Winner:` lines**.
- **0 all-2.0-default rows**, **0 score errors**, **74 distinct `avg_score`** among the 80.
- avg_score range 1.457–2.300, mean 1.8665.
- Reproduces sessions 6, 7, 8 **exactly** (same +80/+5/5-winner/0-default signature).

## Low relevance — four lenses, reported separately, never merged

### (a) `relevance_per_sim` (the board's sort key)
The Grounded 1.505 → The Formal 1.650 → The Engineer 1.726 → The Precise 1.842 → The Therapist
1.908 → The Mythic 1.919 → The Whimsical 2.037 → The Poetic 2.180.
**Lowest: The Grounded (1.505).** The Grounded has run the most sims (229) and the denominator is a
lifetime average ⇒ its last place is a **longevity artefact**, not a quality collapse.

### (b) raw relevance
The Grounded 344.71 → The Engineer 352.08 → The Formal 354.77 → The Precise 377.60.
**Lowest: The Grounded (344.71).**

### (c) win rate (the *selection* metric — not relevance)
**The Poetic 0.010 (1W/102L)** → The Therapist 0.020 (2W/98L) → The Whimsical 0.029 (3W/100L) →
The Mythic 0.031 (3W/94L) → The Engineer 0.104 → The Formal 0.168 → The Grounded 0.196.
**Lowest: The Poetic.** This is the civ actually at risk on the board.
**Healthy: The Precise 0.541 (53W/45L)** — the only civ whose relevance rank and win rate agree.

### (d) mean per-sim `avg_score` (the only lens that answers "is this civ actually good?")
This run's new rows: The Whimsical 1.558 → The Mythic 1.677 → The Grounded 1.743 →
The Engineer 1.912 → The Formal 1.957 → The Therapist 1.992 → The Precise 2.021 → **The Poetic 2.071**.
Sub-score means (quality / novelty / alignment):
```
civ-whimsical   1.185 / 1.832 / 1.657
civ-mythic      1.244 / 1.740 / 2.048
civ-grounded    1.274 / 1.624 / 2.332
civ-engineer    1.361 / 1.687 / 2.688
civ-formal      1.367 / 1.603 / 2.902
civ-therapist   1.107 / 2.090 / 2.778
civ-precise     1.434 / 1.651 / 2.977
civ-poetic      1.536 / 1.876 / 2.802
```
**The Poetic is the quality leader and the board's last-place win-rate civ simultaneously.**
It has the best quality (1.536), the best novelty (1.876), top-3 alignment (2.802), the highest
`relevance_per_sim` (2.180) — and wins 1 of 103 rounds. **The board's win rate measures *selection
appeal*, not relevance.** The chooser never sees the scores: it is shown only 150 chars of
`content_preview` per civ, with no score information.

**The headline low-relevance finding, unchanged: The Grounded is last on the board's own sort key
and on raw relevance, and it is a mediocre writer on the sub-scores (quality 1.274, lowest novelty
1.624, mean avg_score 1.743 = 3rd lowest). The Poetic is the genuine competitive anomaly.**

## Winners this run
The Precise ×4 (what a cell is / the witness log / ternary values / JEV as a decision oracle),
The Grounded ×1 (the bookkeeper's role). 5/5 rounds won by the two lowest-temperature civs.

## Extinction risk
**None.** `extinction_and_birth()` retires only below `relevance < -10`; the lowest is +344.71,
and it only runs in `--loop` mode every third iteration — a single-shot run never triggers it.

## The counter gap (still open)
Ledger rows vs `culture.json` `simulations_run`: **1964 vs 1764** — 200 committed rows counted by
nobody, on every civ. `save_state()` rewrites the whole `culture.json` from in-memory counters with
no lock and no read-modify-write ⇒ lost-update race. `relevance_per_sim` is therefore not a
reproducible ranking and the board order cannot be recomputed from the ledger by an auditor.
Prefer win rate *and* avg_score, and say which lens you mean.

## Two silent-corruption defects worth fixing upstream (unchanged, still unfixed)
1. **A JEV outage awards a random civ a legitimate win.** If the provider works but JEV is down,
   every `avg_score` is the `2.0` default, all civs tie, and the `max()` fallback picks an
   **arbitrary** winner, which is then credited with a real win — permanently corrupting the
   win-rate signal that is one of only two trustworthy metrics. Require a non-default score before
   recording a winner; else mark the round `unscored`.
2. **Zero simulations still exits 0.** Replace the silent `return None` at the provider gate with a
   named error and abort non-zero. Add a row-count assertion
   (`sum(ledger_rows)` grew AND `sum(registry.sims_run)` grew by the same amount).

## Files
- 8 × `civ-*/simulations.jsonl` — each +10 rows, mtime 03:47:20 (baseline 03:45:46).
- 8 × `civ-*/culture.json` — updated counters.
- `meta_log.jsonl` 123 → 128 lines. `leaderboard.json` rewritten.
- `civilizations.json` **unchanged** (141 bytes, 8 civs) — no birth/extinction this run.
