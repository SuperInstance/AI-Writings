# Civ Orchestrator — Run Report 2026-10-24 (session 128)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `078a137` (session 127)
**Run mode:** Control B — local mock z.ai bridge (`ZAI_TOKEN` + `ZAI_URL_OVERRIDE`); JEV live and really scoring.

## Verification — PASS

| Check | Expected | Measured |
|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each (5 sim + 5 competition) | **+10 × 8** (716→726, 747→757, 762→772, 719→729, 741→751, 711→721, 714→724, 774→784) |
| total new ledger rows | 80 | **80** |
| `meta_log.jsonl` Δ | +5 | **+5** (373→378) |
| `Winner:` lines | 5 | **5** |
| rows with `[mock-zai` prefix | 80/80 | **80/80** |
| rows with JEV `error` key | 0 | **0** (JEV really scored; no 2.0 default) |
| `provider` field | `zai` | **`{zai}`** on all 80 |
| sim→competition ts gap at index 4 | present, all 8 civs | **yes** — 1.08 s / 16.45 s / 22.61 s / 7.23 s / 13.47 s / 10.31 s / 4.14 s / 19.57 s |
| mock non-degeneracy (8/8 distinct previews per competition prompt) | 5/5 | **5/5** — 40 distinct seeds across 80 rows (**10th clean mock measurement**) |
| pre-flight probe (4 civs → 4 seeds, 0 tracebacks) | PASS | **PASS** |

Mock non-degeneracy was grouped by **per-civ slot index** (`rows[-10:][5+i]`), not by `prompt` —
`prompt` is truncated to 80 chars and the sim phase reuses the same canon prompts, so grouping by
prompt yields 16 rows/prompt and a naive filter returns 0 competition prompts (false FAIL).

## This run

| civ | run avg_score | quality | novelty | alignment | lifetime relevance | rel/sim | win_rate |
|---|---|---|---|---|---|---|---|
| civ-poetic | 0.3690 | 0.0170 | 0.3640 | 0.7260 | 1263.12 | 1.769 | 0.014 |
| civ-precise | 0.3070 | 0.0090 | 0.5560 | 0.3560 | 1093.31 | 1.551 | 0.526 |
| civ-whimsical | 0.3023 | 0.0260 | 0.3950 | 0.4860 | 1145.59 | 1.589 | 0.014 |
| civ-mythic | 0.2660 | 0.0080 | 0.5310 | 0.2590 | 1066.32 | 1.504 | 0.017 |
| civ-formal | 0.2007 | 0.0120 | 0.4890 | 0.1010 | 962.02 | 1.345 | 0.165 |
| **civ-grounded** | **0.1860** | 0.0090 | 0.4950 | **0.0540** | **852.28** | **1.169** | 0.182 |
| civ-therapist | 0.1590 | 0.0090 | 0.4420 | 0.0260 | 1011.95 | 1.431 | 0.020 |
| civ-engineer | 0.1423 | 0.0100 | 0.3120 | 0.1050 | 960.61 | 1.365 | 0.090 |

Cross-civ spreads (compare spreads, not absolute levels): `alignment` **0.7000** (widest, and the axis
the chooser selects on), `novelty` 0.2440, `avg_score` 0.2267, `quality` 0.0180.
`quality` again collapsed (field mean 0.0110) — the 119/121/122/123/125 regime.

## Low-relevance civilization

**`civ-grounded` (The Grounded) is the low-relevance civ — 31 consecutive sessions (95–128).**

Last on lifetime `relevance` (852.28), `relevance_per_sim` (1.169), `avg_score` (1.2133),
`quality` (0.5921) and `alignment` (1.4526). **The structural gap is `alignment`: 0.3463 below the
next civ** (1.4526 vs 1.7989 `civ-therapist`), versus **0.0321** on quality — 11× wider.
Alignment is the dimension the meta-GAN *selects* on, so Grounded fails to **embody a distinctive
voice** — a voice failure, not a prose failure. On this run it was last on `avg_score` (0.1860) and
2nd-lowest on `alignment` (0.0540).

Secondary axes: `civ-formal` = low-**novelty** (1.4501 lifetime, last). `civ-poetic` = 1st on
lifetime `avg_score` (1.8108) / `quality` (1.0135) but **last** on `win_rate` (0.014) and won 0/5
— the stable selection-failure inverse. `civ-precise` = best `win_rate` (0.526), 1st on lifetime
`alignment` (2.4133), won 3/5 — the mirror inverse.

**Watch-axis `civ-therapist` — the session-123 lifetime signal extended.** Therapist was lowest on
this run's `alignment` (**0.0260**, below `civ-grounded`'s 0.0540) and 2nd-lowest on
`avg_score` (0.1590); its lifetime alignment is now **1.7989, 2nd-lowest of 8**. This is the
second consecutive session on the bottom of the alignment axis — still a watch, not a finding.

**Watch-axis `civ-engineer` — the session-121 low did NOT repeat for a fourth time.** Engineer was
last on this run's `avg_score` (0.1423) and novelty (0.3120), but 6th of 8 on lifetime
`relevance_per_sim` (1.365) and 6th of 8 on lifetime `avg_score` (1.3841). Not a trend.

## Chooser vs `avg_score` argmax: 0/5 (0 %)

Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) →
0/5 (124) → 4/5 (125) → 3/5 (126) → 3/5 (127) → **0/5 (128)**.

Ten five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*. What
survives every session: the chooser is **not** a pure argmax, and in **all 5** disagreements this
session it picked a **lower**-scoring candidate. The most extreme: on p3, `civ-grounded` won at
**0.070** while the argmax `civ-whimsical` scored **0.763** — the session-123 finding in its
strongest form, and the fleet's lowest-relevance civ taking a competition. **A competition win is
not evidence of relevance.**

## Lifecycle

- **Extinction risk NONE** — threshold −10, lowest relevance +852.28 (86× above the floor).
  Registry 8 civs, `max_civs` 12. All 8 still `generation=1`; extinction/birth only runs under `--loop`.
- **Counter gap per-civ, unchanged**: whimsical +63, grounded +43, formal +42, poetic +37,
  engineer +22, mythic +20, therapist +17, precise +16 (total +260). `save_state()` has no lock
  ⇒ `relevance_per_sim` is not recomputable from the ledger by an auditor.
- `culture.json` holds no `relevance_per_sim` — that field is **leaderboard-only**
  (`civilization_orchestrator.py:380`); its absence from `culture.json` is not a regression.

## Environment

- **NAS EDQUOT total (11th session running).** `git clone` into `/workspace/repos/...` dies with
  `Disk quota exceeded`; only the symlink bridge works. Target = the **nested**
  `cellular-first-design` dir, verified by `stat -L -c '%d:%i'` == `129:12745` on both sides + `-ef`.
- **`/tmp` was wiped mid-session.** A clone made at 20:12 (`/tmp/work`) was gone by 20:14 —
  the overlay reclaims `/tmp` between tool calls. Clone into `/tmp` but keep the working tree
  referenced through the workspace symlink, and re-clone if the path vanishes.
- **`gh` is not installed (13th session running).** `GET /search/repositories?q=ai-writings+in:name`
  and `GET /user/repos` with `GITHUB_TOKEN` work; the API is case-insensitive
  (`SuperInstance/ai-writings` == `SuperInstance/AI-Writings`).
- **`GET /user/repos` and `GET /search/repositories` hit the `core` rate limit** this session
  (403 "API rate limit exceeded") while `GET /search/repositories` still worked once.
  **Never read a rate-limit body as a negative result** — fall back to the git protocol
  (`git ls-remote`), which does not consume REST budget.
- Tool timeout 30 s < run ~45 s ⇒ launch detached with stdout redirected, then poll `ps` + the log.
- `ZAI_URL_OVERRIDE` alone is dead code (the token gate returns first) ⇒ needs **both**
  `ZAI_TOKEN` and `ZAI_URL_OVERRIDE`.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`, else JEV silently degrades to the
  2.0 default and every score becomes constant.
