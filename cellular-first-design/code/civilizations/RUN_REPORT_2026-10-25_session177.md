# Civ Orchestrator — Run Report, session 177 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 57th session) + **live JEV** (`jev-1.14.0`).
Baseline: `59eb131` (session 176). **All 12 verification assertions PASS.**

## Environment

- Workspace **empty** apart from `.plugin-cache` and `.skills` — the prompt's path did not
  exist (**12th consecutive occurrence**).
- `/workspace` is at **100 % NAS quota** (600 G/600 G) while visibly empty ⇒ cloned to
  `/tmp/cfd` (overlay fs, 28 G free) and bridged with a symlink.
- Upstream owner: **`SuperInstance/AI-Writings`**; the `ai-writings/…` slug 404s
  (GitHub API is case-insensitive). Full census of the owner's 5,408 repos found no
  `cellular-first-design` repo of its own — it is a **subdirectory** of `AI-Writings`.
- Bridge: `/workspace/repos/ai-writings/cellular-first-design -> /tmp/cfd/cellular-first-design`.
  Both the requested script path **and** the script's internal hardcoded `CIVS_DIR`
  (`/workspace/repos/ai-writings/cellular-first-design/code/civilizations`) resolve to the
  same inode (**1048962**), `-ef` → `EF_OK`.
- `ZAI_TOKEN` absent from env and from all sandbox secrets; z.ai returns **401**
  `token expired or incorrect` ⇒ endpoint healthy, credential absent (**57th session**).
- **JEV live**: well-formed body → **HTTP 200** with `{"model":"jev-1.14.0", …}`.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code — the token gate returns `None` first).
- `gh` not installed — used `GET /user/repos` with `GITHUB_TOKEN`.

## Mock rebuild — SIX fixes, unchanged; gate passed 9/9 on the FIRST build

No rebuild drift. The message-derived index (fix f) was confirmed by the repeat-same-message
probe: **40/40** messages stable on second send, **0** `(civ,prompt)` pairs carry >1 seed.

| pre-flight check | result |
|---|---|
| 40/40 distinct seeds | PASS |
| 40/40 distinct previews | PASS |
| 40/40 independently recomputed md5 (seed, colour, figure) | PASS |
| 8/8 distinct seeds on every one of the 5 prompts | PASS |
| 8/8 distinct previews on every one of the 5 prompts | PASS |
| 0 literal `seed={}` | PASS |
| repeat-same-message ⇒ same seed (40 msgs × 2) | PASS |
| 0 `(civ,prompt)` pairs with >1 seed | PASS |
| 0 `EXC:`/traceback in mock log | PASS |

Post-run mock log: **280** OK lines (200 pre-flight + 80 run), **0** `EXC:`.
Teardown: killed by exact argv match, 0 remaining procs, `curl` exit 7 (port closed).

## Verification

| # | check | result |
|---|---|---|
| A | per-civ `simulations.jsonl` Δ **+10 × 8** = **80** new rows | PASS |
| B | registry 8 civs | PASS |
| C | `meta_log.jsonl` **+5** (618 → 623) | PASS |
| D | all 80 rows `provider=zai` | PASS |
| E | 0 JEV errors in new rows | PASS |
| F | 0 rows missing `avg_score` | PASS |
| G | 80/80 rows carry the mock seed prefix | PASS |
| H | **40/40** distinct seeds | PASS |
| I | `relevance` Δ = Σ`avg_score` **8/8 EXACT** | PASS |
| J | registry all gen 1 (no mutation, no extinction) | PASS |
| K | wins **+5** / losses **+35** | PASS |
| L | leaderboard 8 civs sorted by `relevance_per_sim` | PASS |

**12/12 PASS.**

Per-civ ledger deltas (all md5-changed, all size-grown):

| civ | lines | size | relevance | Δ | Σavg_score |
|---|---|---|---|---|---|
| civ-grounded | 1252 → 1262 | 708483 → 714286 | 1179.3633 → 1189.9833 | +10.6200 | 10.6200 |
| civ-whimsical | 1264 → 1274 | 716494 → 722348 | 1602.2833 → 1617.9500 | +15.6667 | 15.6667 |
| civ-formal | 1237 → 1247 | 694737 → 700518 | 1401.6467 → 1416.7400 | +15.0933 | 15.0933 |
| civ-poetic | 1231 → 1241 | 690520 → 696311 | 1832.3633 → 1850.5367 | +18.1733 | 18.1733 |
| civ-precise | 1201 → 1211 | 668616 → 674378 | 1678.7667 → 1697.2833 | +18.5167 | 18.5167 |
| civ-mythic | 1209 → 1219 | 677771 → 683529 | 1477.1500 → 1488.0600 | +10.9100 | 10.9100 |
| civ-therapist | 1204 → 1214 | 682214 → 688059 | 1343.1733 → 1353.2200 | +10.0467 | 10.0467 |
| civ-engineer | 1206 → 1216 | 683145 → 688913 | 1346.0833 → 1359.6667 | +13.5833 | 13.5833 |

Counter gap: Σ`avg_score` over the 80 new rows = **112.6100**; `d_relevance` matches
**8/8 exact** (max abs diff < 1e-6).

## Relevance

### Run-level (this run's 10 new rows per civ)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-therapist | 1.0047 | 0.1310 | 2.7170 | 0.1660 |
| civ-grounded | 1.0620 | 0.1510 | 2.6790 | 0.3560 |
| civ-mythic | 1.0910 | 0.2570 | 2.6260 | 0.3900 |
| civ-engineer | 1.3583 | 0.2240 | 2.6230 | 1.2280 |
| civ-formal | 1.5093 | 0.2530 | 2.6890 | 1.5860 |
| civ-whimsical | 1.5667 | 0.3080 | 2.7290 | 1.6630 |
| civ-poetic | 1.8173 | 0.6050 | 2.7230 | 2.1240 |
| civ-precise | 1.8517 | 0.4390 | 2.6910 | 2.4250 |

Run spreads: `avg_score` **0.8470**, `alignment` **2.2590**, quality 0.4740, novelty 0.1060.

### The low-relevance civilization

**`civ-grounded` — lifetime low, 52nd consecutive session.** Last of 8 on lifetime
`avg_score` **1.0098**, `quality` **0.4059**, `alignment` **1.0603**, `relevance` **1189.98**,
`relevance_per_sim` **0.976**, lifetime novelty **1.5631** (**6th of 8**, below the 1.7450 median).

Diagnosis: the alignment deficit is **6.65×** the quality deficit ⇒ again a **voice**
failure, not a prose failure. `civ-grounded` writes acceptably and is judged *not to sound
like itself*.

**The run-level low ROTATED to `civ-therapist`** (1.0047 run bottom on `avg_score`,
`alignment` 0.1660, `quality` 0.1310) while its *lifetime* standing is **2nd of 8** on
lifetime `avg_score` (7th of 8 on `relevance_per_sim`). **Watch axis, not the finding**
(session-132 rule) — the run-level axis and the lifetime axis disagree, as they have
rotated repeatedly across sessions 168–177.

### Lifetime leaderboard (`relevance_per_sim`)

| # | civ | rps | relevance | wins | losses | win rate | gen |
|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1.5370 | 1850.54 | 6 | 592 | 0.010 | 1 |
| 2 | civ-precise | 1.4200 | 1697.28 | 361 | 232 | 0.609 | 1 |
| 3 | civ-whimsical | 1.3360 | 1617.95 | 5 | 593 | 0.008 | 1 |
| 4 | civ-mythic | 1.2410 | 1488.06 | 10 | 582 | 0.017 | 1 |
| 5 | civ-formal | 1.1760 | 1416.74 | 94 | 502 | 0.158 | 1 |
| 6 | civ-engineer | 1.1390 | 1359.67 | 47 | 544 | 0.080 | 1 |
| 7 | civ-therapist | 1.1310 | 1353.22 | 11 | 584 | 0.018 | 1 |
| 8 | **civ-grounded** | **0.9760** | **1189.98** | 70 | 527 | 0.117 | 1 |

## Chooser behaviour

Chooser vs `avg_score` argmax: **4/5 (80 %)**. `civ-precise` swept **5/5**.
The one disagreement (ternary values) took the **lower**-scoring candidate (−0.0933);
`civ-poetic` was the argmax and lost. Max |delta| **0.0933**.

## Extinction

Extinction threshold −10; lowest relevance **+1189.98** = **119×** the floor ⇒ **NONE**.
No birth (registry stays at 8; `extinction_and_birth` only runs under `--loop`).
