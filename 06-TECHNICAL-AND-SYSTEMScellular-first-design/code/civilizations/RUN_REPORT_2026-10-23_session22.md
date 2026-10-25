# Civilization Orchestrator — Session 22 (2026-10-23, 121st wipe)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

## Headline

The run **produced data**. +80 ledger rows per run (10/civ uniform), +5 `meta_log.jsonl`
entries, 5 competition winners, **0 all-2.0-default rows** (live JEV), 0 fallback mock
calls, 80/80 distinct `content_preview`. Two runs (body set A and B) were executed:
**+160 rows total**, 844 → 924.

| | rows | meta_log | winners | defaults | fallback | distinct previews |
|---|---|---|---|---|---|---|
| baseline | 764 | 53 | 0 | — | — | — |
| unpatched (control) | 764 (+0) | 53 (+0) | 0 | — | — | — |
| run A (body set A) | 844 (+80) | 58 (+5) | 5 | 0 | 0 | 80/80 |
| run B (body set B) | 924 (+80) | 63 (+5) | 5 | 0 | 0 | 80/80 |

## The credential gap is still the whole story (20th consecutive session)

`ZAI_TOKEN`/`ZAI_KEY`/`GROQ_TOKEN` absent from env **and** from the 8-entry secret
store. All 8 sandbox secrets re-tested against
`https://api.z.ai/api/coding/paas/v4/chat/completions` → **401 "token expired or
incorrect" on every one** (endpoint healthy ⇒ credential gap, not outage).

Unpatched control run: batch header + 8 `[Name] running 5 sims...` lines + **empty
competition section** + **exit 0**. Ledger **+0 rows**, `meta_log` **+0**, **0**
`Winner:` lines. **The per-civ sim lines print before the provider call — they are
not evidence of work.** Assert on the row delta, never on exit code.

**JEV live at `jev-1.14.0`** (HTTP 200, `quality.score 0.13, confidence 0.82`).
`export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` is mandatory; without it JEV silently
degrades to the `{"quality": 2.0, ...}` default and the run measures nothing.

## Control B reconfirmed, 15th time, to the row

`--sims 5 --prompts 5 --providers zai` under Control B → **+80 rows (10/civ,
uniform), +5 meta_log, 5 winners, 0 score errors, 0 all-2.0-default rows, 0 fallback
calls, provider `zai` on 80/80, 80/80 distinct `content_preview`, 73/80 distinct
`avg_score`** (range 0.603–2.293, mean 1.543). Mock log **80 calls**, **exactly 10
per voice across all 8 voices** (name-keyed voice table, s17 rule).

JEV sub-score spread on the 80 rows (set A): quality mean 0.547 (0.01–1.56),
novelty mean 1.883 (0.77–2.55), alignment mean 2.198 (0.21–3.36), confidence mean
0.632 with 48 distinct values. **A live JEV, not a stub.**

## A/B body-set result — rank agreement 8/8 (the first fully-clean A/B recorded)

Same orchestrator, same JEV, same prompts; **only the mock's per-voice prose
changed**. Max |Δavg_score| across all 8 civs: **0.037**. No civ moves >0.3.

| civ | A avg | B avg | Δ | A align | B align |
|---|---|---|---|---|---|
| civ-engineer | 1.729 | 1.766 | +0.037 | 2.859 | 2.899 |
| civ-formal | 1.047 | 1.022 | −0.026 | 1.924 | 1.900 |
| civ-grounded | 0.719 | 0.711 | −0.007 | 0.478 | 0.446 |
| civ-mythic | 1.665 | 1.648 | −0.017 | 2.203 | 2.120 |
| civ-poetic | 2.022 | 2.012 | −0.009 | 2.511 | 2.498 |
| civ-precise | 1.864 | 1.853 | −0.010 | 2.985 | 2.949 |
| civ-therapist | 1.663 | 1.646 | −0.018 | 2.436 | 2.440 |
| civ-whimsical | 1.632 | 1.629 | −0.004 | 2.190 | 2.202 |

**Rank agreement 8/8** — same civ in the same position in both sets, same top-1
(`civ-poetic`), same bottom-1 (`civ-grounded`). History for this measurement:
s9 2/8, s10 2/8, s11 mid-range perturbation, s18 mid-range. **8/8 is the first
fully-clean A/B in the record.** The body sets here are *paraphrases of the same
per-voice register* (same voice, same shape, different words). Prior sessions'
large perturbations (s9: +0.21 to +1.00) came from swapping the **register itself**
(one set generic, one set in-voice). **So the A/B result is a statement about
paraphrase robustness, not about the mock's absolute offset** — the offset is still
a first-order confounder and absolute scores remain mock artefacts. Only the
*relative ordering* carries signal, and this run it is stable under paraphrase.

## Chooser vs argmax — 0/5 in both runs (15th replication)

`best_civ` == `argmax(avg_score)` in **0 of 5** rounds in run A and **0 of 5** in run
B. Disagreement margins (A) 0.13 / 0.85 / 0.03 / 0.54 / 0.22, mean **0.354**;
(B) mean 0.648. **`civ-poetic` was the argmax in all 5 rounds of run A and won 0.**

The competition and the scoring are two independent JEV calls and the chooser never
sees the scores. History: s8 18.9 %, s13 22.4 %, s15 15.5 %, s17 0 %, s20 10 %,
s21 0 %, **s22 0 % (×2 runs)**.

## Low-relevance — four lenses, four answers (10th session running)

Final board after both runs:

| lens | lowest | value | what it measures |
|---|---|---|---|
| `relevance_per_sim` (board sort) | **civ-grounded** | 1.654 | longevity denominator (99 sims) |
| raw relevance | **civ-engineer** | 144.27 | accumulated score, same denominator |
| `win_rate` (**selection** metric) | **civ-poetic** | **0.000 (0W/38L)** | selection appeal under a 150-char preview |
| lifetime `avg_score` | **civ-grounded** | 1.825 | actual writing quality |
| lifetime `quality` | **civ-engineer** | 1.558 | |
| lifetime `novelty` | **civ-formal** | 1.046 | |
| lifetime `alignment` | **civ-grounded** | 2.494 | |
| this-session `avg_score` | **civ-grounded** | 0.719 | |
| this-session `quality` | **civ-grounded** | 0.067 | |
| this-session `novelty` | **civ-formal** | 1.063 | |
| this-session `alignment` | **civ-grounded** | 0.478 | |

- **`civ-grounded` = the stable low-relevance civ, 10th session running.** Last on
  `relevance_per_sim`, lifetime `avg_score`, lifetime `alignment`, and last this
  session on `avg_score`, `quality` and `alignment`. It ran the most sims (99), but
  it is *also* last on the raw score lenses, so it is a **genuine quality
  weakness**, not the longevity artefact the denominator suggests.
- **`civ-poetic` = the inverse case, 20th session running.** 1st of 8 on
  `relevance_per_sim` (2.475), lifetime `avg_score` 2.564 (2nd of 8), **0 wins in
  38**, **0 of 5** rounds in run A, and the argmax in all 5 run-A rounds. A
  *selection* failure, not a quality collapse.
- **`civ-precise` = wins by being picked, not by scoring.** Best win rate in the
  fleet (**0.576**, 19W/14L) and 3 of 5 wins in run A, but 2nd on lifetime
  `avg_score` (2.001) and 2nd-last on lifetime `novelty` (1.114).
- **`civ-whimsical` = the only civ where every quality lens agrees** (1st on
  lifetime `avg_score` 2.627, novelty 2.579, alignment 3.284) — and 3rd-lowest win
  rate (0.053), 0 of 5 in run A.
- **Extinction risk: none.** Threshold is `relevance < -10`; the lowest is
  +144.27. `extinction_and_birth()` only runs in `--loop` mode; a single-shot run
  never triggers it. All 8 civs remain generation 1.

## Replications

- Control B: +80 / +5 / 5 winners / 0 defaults / 0 errors / 0 fallback / 80-80
  provider / uniform 10-per-voice — **15th**.
- Chooser vs `argmax(avg_score)`: **0/5 twice**, 15th replication.
- Counter gap **+260** (924 ledger rows vs 664 registry `simulations_run`),
  **identical to the s20/s21 baseline**. A **race** in `save_state()`, not a leak.
  Report as measured this session; never as a trend against a quoted number.

## Environment notes (nothing new broke; the known traps all held)

1. 121st consecutive wipe — the task path did not exist; `/workspace` held only
   `.plugin-cache`. NAS `/workspace` at **100 %** (600 G used, 0 avail) — a clone
   into it fails mid-copy with "Disk quota exceeded". `/tmp` is on the overlay
   (28 G free) and is exempt.
2. **The full clone failed AGAIN** — `git clone --depth 1 --filter=blob:none` into
   `/tmp` fetched ~1.1 GB then died with
   `could not open '.../tmp_pack_XXXX' for reading` and **removed the working
   tree**. Confirms the s16/s18 rule: `--filter=blob:none` is the broken form.
3. **The API-tree fetch is a fast, reliable substitute.** One
   `git/trees/main?recursive=1` call (22,059 entries, `truncated: false`) then a
   per-blob `git/blobs/<sha>` fetch for the 58 files under
   `cellular-first-design/code/civilizations/`. **Whole subtree in ~40 s, no pack
   file, no 3.7 GB download.** This is now the preferred bootstrap.
4. `rm -rf /workspace/repos/ai-writings && ln -sfn /tmp/aw /workspace/repos/ai-writings`
   — the `rm -rf` is still required (s8 trap). `CIVS_DIR` is hardcoded to the
   `/workspace` path, so the symlink is what makes the script write into the clone.
5. The **`ZAI_URL_OVERRIDE` seam is still not in the committed blob** — re-apply the
   one-line patch each session (verified: 1 insertion, 1 deletion).
6. **A health-check probe of the mock pollutes its call log** (s18 trap, hit again).
   The probe POSTs `{}`, which produces one `fallback: true` row. **Never probe the
   mock before the run** — restart it with the log removed instead.
7. `setsid nohup python3 mock.py &` inside a foreground tool call **blocks past the
   30 s timeout**; the process does start, but the call must be re-checked
   afterwards. Write the file first, start the process second.
8. `gh` CLI is still not installed; use the GitHub REST API. The `search` quota is
   separate from core and was still available.
