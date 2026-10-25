# Civ Orchestrator — RUN_REPORT session 135 (2026-10-24)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

Upstream `SuperInstance/AI-Writings` @ `4995b79`, sparse clone to `/tmp/aiw` (NAS is 600 G/600 G,
0 bytes free — the RUNBOOK symlink bridge is mandatory). Symlink bridge at
`/workspace/repos/ai-writings/cellular-first-design` → `/tmp/aiw/cellular-first-design`
(inode `129:12630` on both sides, `-ef` OK).

Control B mock provider on `127.0.0.1:8799` (`ZAI_TOKEN` + `ZAI_URL_OVERRIDE` both set —
the override is dead code without a token). JEV live (`TYPESAFEAI_KEY` exported from
`TYPESAFE_AI_TOKEN`; pre-flight probe → HTTP 200, `jev-1.14.0`).

## Pre-flight (before the run)

`/tmp` was wiped this session, so the mock was rebuilt from scratch from the RUNBOOK spec with
**both** historical mock bugs re-applied on rebuild:

- session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]` — a plain `seed[i*2:i*2+2]` is empty for
  `i>=4`, raises `ValueError`, and the bridge answers HTTP 500 **while the socket stays open**.
- session-118 md5-of-whole-message seeding — seeding from the first 8 alnum chars of the message
  yields `youareav` for all 8 civs (the cultural prompt opens with the civ-invariant
  `You are a voice in the tradition of "..."`), making all 8 candidates byte-identical.

Pre-flight probe with the **exact long cultural prompt** against the live mock, 5 canon prompts
× 8 civs: **8/8 distinct seeds, 8/8 distinct previews, 5/5 prompts, HTTP 200, 332–521-char
bodies, `[mock-zai seed=…]` prefix present, 0 tracebacks.**

## Verification — all checks passed

| check | expected | measured | result |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | +10 each | +10 × 8 | PASS |
| `meta_log.jsonl` delta | +5 | 408 → 413 | PASS |
| `Winner:` lines | 5 | 5 | PASS |
| total new rows | 80 | 80 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` field | `{zai}` | `{zai}` | PASS |
| rows with JEV `error` key | 0 | 0 | PASS |
| rows with the 2.0/2.0/2.0 JEV fallback triple | 0 | 0 | PASS |
| sim → competition ts gap (index 4 → 5) | positive | 1.08 – 22.73 s, 8/8 | PASS |
| mock tracebacks in `/tmp/mock_zai.log` | 0 | 0 | PASS |
| mock killed, port closed | curl exit 7 | exit 7 | PASS |
| git status deletions / untracked | 0 / 0 | 0 / 0 (18 modified) | PASS |

Per-civ ledger deltas: civ-grounded 832→842, civ-whimsical 844→854, civ-formal 817→827,
civ-poetic 811→821, civ-precise 781→791, civ-mythic 789→799, civ-therapist 784→794,
civ-engineer 786→796. Total 6444→6524.

Distinct seeds in the new rows = **40**, distinct content previews = **40** — the expected
5 prompts × 8 civs split across the two phases (5 sim-phase rows reuse the same cultural
prompts as the 5 competition-phase rows), not mock degeneracy. The session-118 degeneracy
check (`len({previews}) == 8` for one competition prompt) passed 8/8 in pre-flight.

## Low-relevance civilization — `civ-grounded` (The Grounded)

**`civ-grounded` is the low-relevance civ — 38 consecutive sessions (95–135).** Last on lifetime
`avg_score`, `quality`, `novelty`, `alignment`, `relevance` and `relevance_per_sim`.

| dimension | civ-grounded | next best | gap |
|---|---|---|---|
| lifetime `avg_score` | 1.1471 | 1.7365 (civ-poetic) | 0.589 |
| lifetime `quality` | 0.5453 | 0.9404 (civ-poetic) | 0.395 |
| lifetime `novelty` | 1.5490 | 2.0503 (civ-whimsical) | 0.501 |
| lifetime `alignment` | 1.3470 | 2.3353 (civ-precise) | **0.988** |
| lifetime `relevance` | 881.52 | 1002.74 (civ-formal) | 121.22 |
| lifetime `relevance_per_sim` | 1.103 | 1.277 (civ-formal) | 0.174 |

Alignment is the dimension the meta-GAN *selects* on, so the 0.988 alignment gap is the
structurally meaningful one — ~2.5× wider than the quality gap. Grounded's tenets ("concrete
images, everyday language, specific examples, no abstractions") and voice ("warm, factual") are
the least differentiating prompt in the field — a **voice** failure, not a prose failure.

Grounded was also the run-level low on `alignment` (0.1580, 7th of 8) and 7th of 8 on
`avg_score` (0.7510) — 2nd-lowest, behind civ-therapist (0.7467). On the run-level axis the
label went to `civ-therapist` for the first time in a while (127 whimsical; 128/129/130/133/134
grounded; **135 therapist**). Keep the lifetime finding and the run-level label as two separate
claims.

## Other axes

- **`civ-formal` is the low-novelty axis** — lifetime novelty **1.4201** (last); alignment
  1.9502 healthy. **`civ-poetic`** = 1st on lifetime `avg_score` (1.7365) / `quality` (0.9404) /
  `novelty` (1.9796) and 2nd on `alignment` (2.2895), but **last on `win_rate` (0.013)** and won
  **0/5** this run — the stable selection-failure inverse. **`civ-precise`** = best `win_rate`
  (0.543), 1st on lifetime `alignment` (2.3353) — the mirror inverse.
- **Winner tally this run:** civ-precise 2, civ-engineer 2, civ-formal 1.
- **Extinction risk: NONE** (threshold −10; lowest raw relevance 881.52). Registry 8 civs,
  `max_civs` 12; extinction/birth only runs under `--loop`.
- **Counter gap:** ledger rows exceed registry `simulations_run` by **+260** (6524 vs 6264).
  Per-civ: whimsical +63, grounded +43, formal +42, poetic +37, engineer +22, mythic +20,
  therapist +17, precise +16. `save_state()` rewrites `culture.json` with no lock, so
  `relevance_per_sim` is **not recomputable from the ledger** by an auditor.

## Chooser vs `avg_score` argmax: 1/5 (20 %)

Clean-mock series: 0/5 (118) -> 3/5 (119) -> 1/5 (120) -> 4/5 (121) -> 4/5 (122) -> 3/5 (123) ->
0/5 (124) -> 4/5 (125) -> 1/5 (126) -> 3/5 (127) -> 2/5 (128) -> 4/5 (130) -> 1/5 (131) ->
2/5 (132) -> 2/5 (133) -> 0/5 (134) -> **1/5 (135)**.

Fifteen five-sample points cannot narrow a rate — the honest claim is *somewhere in 0-80 %*.
What survives every session: the chooser is **not** a pure argmax. In all 4 disagreements this
session it picked a **lower**-scoring candidate (p0 precise 1.35 vs poetic 1.70; p1 formal
0.86 vs poetic 1.62; p3 engineer 0.86 vs poetic 1.58; p4 engineer 1.11 vs poetic 1.68) — the
stable direction across 116/118/119/120/122/123/125/131/133/134/135 (13th consecutive session
with that direction). The meta-GAN chooser scores the *text* via JEV; it does not read
`avg_score`. **Never treat `win_rate` as a quality metric.**
