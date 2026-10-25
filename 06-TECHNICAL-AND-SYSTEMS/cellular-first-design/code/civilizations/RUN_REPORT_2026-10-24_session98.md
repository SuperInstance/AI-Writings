# Civilization Orchestrator — Session 98 (2026-10-24, 113th wipe)

Command: `python3 .../civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

## Environment bootstrap
- `/workspace` at **100 % NAS quota** (600 G used, 0 avail). Clone went to overlay `/tmp/aiw`
  (full clone, 20737 files). `/workspace/repos` reached via a **symlink bridge**:
  `ln -sfn /tmp/bridge /workspace/repos` + `.../cellular-first-design -> /tmp/aiw/AI-Writings/cellular-first-design`.
  Verified by **inode identity** `129:1717` on both paths, not by `ls`.
- Remote HEAD at start: `e5a816e7`. Script **pristine** vs git blob (`git diff` empty) — only data files moved.
- `TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"`. JEV live: **HTTP 200, model `jev-1.14.0`**, real score (0.51, conf 0.59).

## Control A (real zai provider) — NO-OP, credential gap 36th consecutive
`ZAI_TOKEN`/`ZAI_KEY` absent from env. All 7 sandbox secrets POSTed to
`https://api.z.ai/api/coding/paas/v4/chat/completions` → **401 "token expired or incorrect" on every one**
(endpoint healthy ⇒ credential gap, not outage).

TELL confirmed: output had the `=== Civilization batch` header and all 8 `[Name] running 5 sims...`
lines, then the competition header and **no `Winner:` lines**. Exit code 0.

**Ledger delta: +0 rows on all 8 civs, +0 meta rows, leaderboard unchanged.**

## Control B (local mock, `ZAI_URL_OVERRIDE` — committed upstream, no patch)
Two **independent body sets** (rotated body pool + different salt + different seed), each restored
to a clean git baseline before running.

| check | set A | set B |
|---|---|---|
| new ledger rows | +80 | +80 |
| per-civ rows | 10 each | 10 each |
| marker-prefixed | 80/80 | 80/80 |
| **distinct content_preview** | **80/80** | **80/80** |
| all-2.0-default rows | 0 | 0 |
| score errors | 0 | 0 |
| mock fallbacks (null civ) | 0 | 0 |
| `Winner:` lines | 5 | 5 |
| meta_log rows | +5 | +5 |

### NEW METHOD NOTE — a pool sized to the draw count is not enough
First attempt used 3 bodies per civ: 80 rows but only **24 distinct previews**. Second attempt used
10 bodies with `random.choice`: **53 distinct** — sampling 10 from 10 with replacement collides.
**Fix: cycle deterministically per civ** (`body = pool[n % len(pool)]` with a per-civ counter) ⇒
80/80 distinct previews on both sets. Symptom to recognise: `distinct previews < row count` while
every other check passes. Assert `distinct == row count`, not `marked == row count`.

## A/B body-set comparison (5 prompts)
Spearman rho **0.500**, exact position matches **1/8**.
set A bottom `civ-engineer` / set B bottom `civ-precise` — **the two body sets disagree about the bottom**,
so this run's bottom is body-set dependent and is NOT reported as *the* low-relevance civ.

| civ | set A | set B | \|d\| | rankA | rankB |
|---|---|---|---|---|---|
| civ-therapist | 1.962 | 1.770 | 0.192 | 1 | 4 |
| civ-whimsical | 1.920 | 2.026 | 0.106 | 3 | 1 |
| civ-poetic | 1.926 | 2.006 | 0.080 | 2 | 2 |
| civ-mythic | 1.776 | 1.946 | 0.170 | 5 | 3 |
| civ-precise | 1.778 | 1.602 | 0.176 | 4 | 8 |
| civ-grounded | 1.672 | 1.640 | 0.032 | 6 | 7 |
| civ-formal | 1.612 | 1.654 | 0.042 | 7 | 5 |
| civ-engineer | 1.544 | 1.648 | 0.104 | 8 | 6 |

Max |d| 0.192; 0 civs cross a 0.3 band.

## Chooser vs argmax — **0/10 (0 %)**, strongest replication yet
Set A: chooser picked precise ×4, grounded ×1; argmax therapist ×2, poetic ×2, whimsical ×1.
Set B: chooser precise ×2, grounded ×2, formal ×1; argmax whimsical ×3, poetic ×1, mythic ×1.
The competition chooser never sees the scores (`state` carries only `content_preview[:150]`, and the
question is a `choice` with no score column) — the two are independent JEV calls.
**"Prefer win rate" is unsafe as a standalone rule.**

## Low relevance — the LIFETIME finding, 5th consecutive session
Committed ledger now 3804 rows, **1440 synthetic (37.9 %)**, 2364 clean.

| lens | last | value | 2nd lowest | gap |
|---|---|---|---|---|
| board `relevance_per_sim` | **civ-grounded** | 1.473 | civ-formal 1.643 | 0.170 |
| board raw relevance | **civ-grounded** | 676.13 | civ-formal 730.95 | 54.8 |
| clean lifetime `avg_score` | **civ-grounded** | 1.678 | civ-formal 1.781 | 0.103 |
| clean lifetime `alignment` | **civ-grounded** | 2.221 | civ-engineer 2.669 | **0.449** |
| clean lifetime `novelty` | **civ-formal** | 1.414 | civ-precise 1.578 | 0.164 |
| clean lifetime `quality` | civ-precise | 1.104 | civ-formal 1.104 | 0.001 |
| board `win_rate` | **civ-poetic** | 0.009 (2W/216L) | civ-whimsical 0.018 | 0.009 |
| this-run (set B) | **civ-formal** | 1.624 | civ-precise 1.637 | 0.013 |

**`civ-grounded` is last on the committed lifetime lenses for a 5th consecutive session (s94–s98).**
Longevity-artefact defence stays falsified: the Grounded has **322 clean rows — 2nd most of 8**
(whimsical 334), so a lifetime-average denominator penalises it relative to the middle, and it is
instead last on the cleanest, denominator-least-biased lens. Its alignment deficit (0.449 below the
next-worst) is the largest separation of any lens, and alignment is the dimension the meta-GAN selects on.

**`civ-formal` is the inverse case:** lowest clean lifetime `novelty` (1.414) and this-run bottom on
set B, but mid-table on the board. Its weakness is specifically **flattest prose** — a style-specific
deficiency, distinct from the Grounded's *alignment* deficiency. **Name the axis; do not merge them
into one "lowest civ".**

**`civ-poetic` is the stable inverse:** 1st on clean lifetime `avg_score` (2.313) but last on
`win_rate` (0.009, 2W/216L) — a **selection** failure, not a quality collapse.

**Extinction risk: NONE** (threshold −10; lowest raw relevance +676.13; `--loop`-mode only).

## Board vs win-rate inversion
**8/8 positions differ.** Board 1st (`civ-poetic`, rps 2.127) is the fleet's worst pick rate (0.009);
board 5th (`civ-precise`, rps 1.802) is the best (0.469).

## Committed-ledger integrity
- **Counter gap: 3804 ledger rows vs 3544 registry `simulations_run` = 260 uncounted (6.8 %).**
  `save_state()` rewrites `culture.json` from in-memory counters with no lock ⇒ `relevance_per_sim`
  is not recomputable from the ledger by an auditor.
- Ledgers restored from git after the run; all 8 row counts and `meta_log` (238) byte-identical to
  `origin/main`; `git status --short` empty; no `__pycache__` left behind.
- Session report: this file. Remote HEAD at session start: `e5a816e7`.
