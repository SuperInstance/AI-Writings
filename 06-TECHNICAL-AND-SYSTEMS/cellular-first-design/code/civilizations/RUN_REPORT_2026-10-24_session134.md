# Civ Orchestrator — RUN_REPORT session 134 (2026-10-24)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

Upstream `SuperInstance/AI-Writings` @ `95a424a` (session 133 baseline), sparse clone to `/tmp/aiw`,
symlink bridge at `/workspace/repos/ai-writings/cellular-first-design` (inode `129:12649`, `-ef` OK).
Control B mock provider on `127.0.0.1:8799` (`ZAI_TOKEN` + `ZAI_URL_OVERRIDE` both set).
JEV live (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe → HTTP 422 = token
accepted, endpoint healthy).

## Verification — all checks passed

| check | expected | measured | result |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | +10 each | +10 x 8 | PASS |
| `meta_log.jsonl` delta | +5 | 403 -> 408 | PASS |
| `Winner:` lines | 5 | 5 | PASS |
| total new rows | 80 | 80 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` field | `{zai}` | `{zai}` | PASS |
| rows with JEV `error` key | 0 | 0 | PASS |
| rows with the 2.0/2.0/2.0 JEV fallback triple | 0 | 0 | PASS |
| competition prompts at 8/8 distinct previews AND seeds | 5/5 | 5/5 | PASS |
| sim -> competition ts gap (index 4 -> 5) | positive | 1.09 - 23.24 s, 8/8 | PASS |
| mock tracebacks in `/tmp/mock_zai.log` | 0 | 0 | PASS |
| git status deletions / untracked | 0 / 0 | 0 / 0 (18 modified) | PASS |

Per-civ ledger deltas: civ-engineer 776->786, civ-formal 807->817, civ-grounded 822->832,
civ-mythic 779->789, civ-poetic 801->811, civ-precise 771->781, civ-therapist 774->784,
civ-whimsical 834->844. Total 6364->6444.

## Pre-flight (before the run, per the session-118/132 rule)

`/tmp` was wiped this session, so the mock was rebuilt from scratch from the RUNBOOK spec and
**both** historical mock bugs were re-applied on rebuild:

- session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]` — a plain `seed[i*2:i*2+2]` is empty for `i>=4`,
  raises `ValueError`, and the bridge answers HTTP 500 **while the socket stays open**.
- session-118 md5-of-whole-message seeding — seeding from the first 8 alnum chars of the message
  yields `youareav` for all 8 civs (the cultural prompt opens with the civ-invariant
  `You are a voice in the tradition of "..."`), making all 8 candidates byte-identical.

Pre-flight probe against the **live** mock with the exact long cultural prompt:
8/8 distinct seeds, 8/8 distinct previews, HTTP 200, 333-361-char bodies,
`[mock-zai seed=...]` prefix present, **0 tracebacks**.

## Low-relevance civilization — `civ-grounded` (The Grounded)

**`civ-grounded` is the low-relevance civ — 37 consecutive sessions (95-134).** Last on lifetime
`avg_score`, `quality`, `alignment`, `relevance` and `relevance_per_sim`.

| dimension | civ-grounded | next best | gap |
|---|---|---|---|
| lifetime `avg_score` | 1.1519 | 1.3165 (civ-engineer) | 0.165 |
| lifetime `quality` | 0.5517 | 0.5840 (civ-formal) | 0.032 |
| lifetime `alignment` | 1.3613 | 1.6763 (civ-therapist) | 0.315 |
| lifetime `relevance` | 874.01 | 990.52 (civ-engineer) | 116.51 |
| lifetime `relevance_per_sim` | 1.108 | 1.283 (civ-formal) | 0.175 |

Alignment is the dimension the meta-GAN *selects* on, so the 0.315 alignment gap is the
structurally meaningful one: ~10x wider than the quality gap. Grounded's tenets ("concrete
images, everyday language, specific examples, no abstractions") and voice ("warm, factual") are
the least differentiating prompt in the field — a **voice** failure, not a prose failure.

**Grounded was also the run-level low** on this run's `avg_score` (0.2460) and on run `alignment`
(0.1970), 5th of 8 on run `novelty` (0.5200) and 4th on run `quality` (0.0210) — the 5th
consecutive session where the run-level label went to it (127 whimsical; 128/129/130/133/134
grounded). Keep the lifetime finding and the run-level label as two separate claims.

## Other axes

- **`civ-formal` is the low-novelty axis** — lifetime novelty **1.4114** (last); alignment 2.0
  healthy. **`civ-poetic`** = 1st on lifetime `avg_score` (1.7372) / `quality` (0.9489) / `novelty`
  (1.9741) and 2nd on `alignment` (2.2887), but **last on `win_rate` (0.013)** and won **0/5**
  this run — the stable selection-failure inverse. **`civ-precise`** = best `win_rate` (0.545),
  1st on lifetime `alignment` (2.3406) — the mirror inverse.
- **Winner tally this run:** civ-formal 3, civ-precise 1, civ-engineer 1.
- **Extinction risk: NONE** (threshold -10; lowest raw relevance 874.01). Registry 8 civs,
  `max_civs` 12; extinction/birth only runs under `--loop`.
- **Counter gap:** ledger rows exceed registry `simulations_run` by **+260** (6444 vs 6184).
  `save_state()` rewrites `culture.json` with no lock, so `relevance_per_sim` is **not
  recomputable from the ledger** by an auditor.

## Chooser vs `avg_score` argmax: 0/5 (0 %) — the lowest of the clean-mock series

Clean-mock series: 0/5 (118) -> 3/5 (119) -> 1/5 (120) -> 4/5 (121) -> 4/5 (122) -> 3/5 (123) ->
0/5 (124) -> 4/5 (125) -> 1/5 (126) -> 3/5 (127) -> 2/5 (128) -> 4/5 (130) -> 1/5 (131) ->
2/5 (132) -> 2/5 (133) -> **0/5 (134)**.

Fifteen five-sample points cannot narrow a rate — the honest claim is *somewhere in 0-80 %*.
What survives every session: the chooser is **not** a pure argmax, and in **all 5** disagreements
this session it picked a **lower**-scoring candidate (p0 precise 0.543 vs whimsical 0.947;
p1 formal 0.523 vs precise 0.783; p2 formal 0.293 vs poetic 1.117; p3 engineer 0.307 vs whimsical
0.773; p4 formal 0.480 vs precise 0.650) — the stable direction across
116/118/119/120/122/123/125/131/133/134 (12th consecutive session with that direction).
The meta-GAN chooser scores the *text* via JEV; it does not read `avg_score`.
**Never treat `win_rate` as a quality metric.**
