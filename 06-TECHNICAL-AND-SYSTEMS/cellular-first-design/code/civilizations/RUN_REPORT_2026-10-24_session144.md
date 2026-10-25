# Civ Orchestrator — RUN_REPORT_2026-10-24_session144

`python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

## Run identity

| item | value |
|---|---|
| upstream | `SuperInstance/AI-Writings` |
| leaderboard iso | `2026-10-24T23:43:42` |
| provider | `zai` (Control B local mock bridge) |
| JEV | live (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`) |
| registry | 8 civs, no births/extinctions (not `--loop`) |
| run | 16th consecutive clean mock measurement |

## Row-count verification (assert on rows, never exit code)

| assertion | expected | observed |
|---|---|---|
| per-civ `simulations.jsonl` delta | +10 × 8 | **+10 × 8** (80 total) |
| `meta_log.jsonl` delta | +5 | **+5** (453 → 458) |
| `Winner:` lines | 5 | **5** |
| rows with `[mock-zai` prefix | 80 | **80** |
| rows with `provider=zai` | 80 | **80** |
| rows with a JEV `error` key | 0 | **0** |
| rows with 2.0/2.0/2.0 fallback | 0 | **0** |
| distinct seeds across new rows | 40 | **40** |
| `(civ,prompt)` combos with >1 seed | 0 | **0** |
| per-prompt distinct seeds + previews | 8/8 × 5 | **8/8 × 5** |

Per-civ delta: engineer 876→886, formal 907→917, grounded 922→932, mythic 879→889,
poetic 901→911, precise 871→881, therapist 874→884, whimsical 934→944.

Row isolation used the **per-civ tail + ts sort** method (session-143 correction), not
`rows[-80:]` over the concatenation.

## Competition winners

| prompt | winner | argmax | agree |
|---|---|---|---|
| what a cell is | **The Precise** (`civ-precise`) | `civ-poetic` (1.23) | no |
| the bookkeeper's role | **The Precise** (`civ-precise`) | `civ-poetic` (1.48) | no |
| the witness log | **The Precise** (`civ-precise`) | `civ-precise` (1.67) | yes |
| ternary values | **The Mythic** (`civ-mythic`) | `civ-precise` (1.32) | no |
| JEV as a decision oracle | **The Mythic** (`civ-mythic`) | `civ-poetic` (1.41) | no |

Chooser vs `avg_score` argmax: **1/5 (20%)**. Consistent with the clean-mock series — the
chooser is **not** a pure argmax, and every disagreement again took the **lower**-scoring
candidate. The ternary-values disagreement is the largest this run (winner 0.83 vs argmax 1.32).
**Never treat `win_rate` as a quality metric** — it is a *selection* metric.

## Low-relevance civilizations

**`civ-grounded` (The Grounded) — the low-relevance civ, 42 consecutive sessions (95–144).**

| metric | value | rank |
|---|---|---|
| lifetime `relevance` | 926.99 | last of 8 |
| `relevance_per_sim` | 1.043 | last of 8 |
| lifetime `avg_score` | 1.0851 | last of 8 |
| lifetime `alignment` | 1.2510 | last of 8 |
| lifetime `quality` | 0.4974 | last of 8 |
| lifetime `novelty` | 1.5069 | above median |

The structural gap is still **alignment**: the next civ (`civ-therapist`, 1.5177) leads
Grounded by 0.2667, while quality's margin to the next civ (`civ-formal`, 0.5318) is only
0.0344 — a **7.8×** wider alignment gap. Alignment is the dimension the meta-GAN *selects*
on, so Grounded fails to *embody a distinctive voice*, not merely to write weakly. Novelty is
above median, so it is not boring — it is unmistakable in a way the chooser does not reward.

**Run-level watch axis: `civ-grounded` took the run low on `avg_score` (0.5803), `quality`
(0.1060) and `novelty` (0.9050); `civ-therapist` took the run low on `alignment` (0.4460).**
Different civs on different axes — **not** a contradiction (session-132 rule). The lifetime
table is the structural signal; the run ranking is the watch axis. Therapist's lifetime
standing is mid-field (1.2818 `avg_score`), so it is **not** a finding. It becomes one only if
it repeats — and it has now appeared as a watch axis in sessions 138, 141 and 144 without ever
becoming a lifetime finding.

**Extinction risk: NONE.** Threshold −10; the lowest relevance is 926.99, i.e. 92.7× above the
floor. Registry 8, `max_civs` 12; extinction/birth only runs under `--loop`.

## Lifetime leaderboard (post-run)

| civ | relevance | per_sim | sims | win_rate | avg_score | alignment | quality | novelty |
|---|---|---|---|---|---|---|---|---|
| `civ-poetic` | 1422.15 | 1.627 | 874 | 0.014 | 1.6673 | 2.2101 | 0.8727 | 1.9193 |
| `civ-precise` | 1256.37 | 1.452 | 865 | 0.551 | 1.4631 | 2.2566 | 0.5934 | 1.5393 |
| `civ-whimsical` | 1270.74 | 1.442 | 881 | 0.012 | 1.5295 | 1.8961 | 0.7043 | 1.9882 |
| `civ-mythic` | 1168.27 | 1.344 | 869 | 0.021 | 1.3716 | 1.7107 | 0.6303 | 1.7739 |
| `civ-therapist` | 1091.00 | 1.258 | 867 | 0.021 | 1.2818 | 1.5177 | 0.5597 | 1.7680 |
| `civ-engineer` | 1059.49 | 1.226 | 864 | 0.087 | 1.2458 | 1.7154 | 0.5419 | 1.4800 |
| `civ-formal` | 1069.64 | 1.222 | 875 | 0.162 | 1.2597 | 1.8491 | 0.5318 | 1.3983 |
| `civ-grounded` | 926.99 | 1.043 | 889 | 0.155 | 1.0851 | 1.2510 | 0.4974 | 1.5069 |

Stable inverses persist: `civ-poetic` 1st on lifetime `avg_score` and `quality` but last on
`win_rate` (0.014); `civ-precise` best `win_rate` (0.551) and highest `alignment` (2.2566).
`civ-formal` remains the low-novelty axis (1.3983, last of 8).

Run-level cross-civ spreads: `alignment` 1.528, `avg_score` 0.768, `novelty` 0.814,
`quality` 0.298. **Alignment again carried the widest spread and is again the axis the chooser
selects on** — consistent with the standing structural finding.

## Environment

- NAS EDQUOT total again (600 G/600 G): `git clone` into `/workspace/repos/...` died with
  `Disk quota exceeded`. Recovery via the symlink bridge to a `/tmp` clone; verified by inode
  identity (`129:108` both sides, `-ef` OK).
- `ZAI_TOKEN` still absent from env; z.ai 401s (endpoint healthy, credential gap). Control B
  mock used, rebuilt from scratch with the session-112 index-wrap fix and the session-118
  whole-message md5 seeding fix.
- Mock pre-flight passed: 8/8 distinct seeds AND 8/8 distinct previews, `[mock-zai` prefix
  present on all 8, body lengths 332–369 chars, **0 tracebacks** / **0 EXC** in the mock log.
- JEV liveness: empty `questions` ⇒ 422 `too_short` (payload-shape complaint ⇒ token
  accepted, not "down").
- Mock killed by exact args; port 8799 verified closed afterwards (`curl` exit 7 = refused).
