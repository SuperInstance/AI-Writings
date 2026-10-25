# Civ Orchestrator — RUN_REPORT_2026-10-24_session143

`python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

## Run identity

| item | value |
|---|---|
| upstream | `SuperInstance/AI-Writings` |
| leaderboard iso | `2026-10-24T23:37:03` |
| provider | `zai` (Control B local mock bridge) |
| JEV | live (`TYPESAFEAI_KEY` from `TYPESAFE_AI_TOKEN`) |
| registry | 8 civs, no births/extinctions (not `--loop`) |

## Row-count verification (assert on rows, never exit code)

| assertion | expected | observed |
|---|---|---|
| per-civ `simulations.jsonl` delta | +10 × 8 | **+10 × 8** (80 total) |
| `meta_log.jsonl` delta | +5 | **+5** (448 → 453) |
| `Winner:` lines | 5 | **5** |
| rows with `[mock-zai` prefix | 80 | **80** |
| rows with a JEV `error` key | 0 | **0** |
| rows with 2.0/2.0/2.0 fallback | 0 | **0** |
| distinct seeds across new rows | 40 | **40** |
| `(civ,prompt)` combos with >1 seed | 0 | **0** |
| per-prompt distinct seeds + previews | 8/8 × 5 | **8/8 × 5** |

Per-civ delta: engineer 866→876, formal 897→907, grounded 912→922, mythic 869→879,
poetic 891→901, precise 861→871, therapist 864→874, whimsical 924→934.

## Competition winners

| prompt | winner |
|---|---|
| Write 100 words on what a cell is. | **The Precise** (`civ-precise`) |
| Write 100 words on the bookkeeper's role. | **The Formal** (`civ-formal`) |
| Write 100 words on the witness log. | **The Formal** (`civ-formal`) |
| Write 100 words on ternary values. | **The Precise** (`civ-precise`) |
| Write 100 words on JEV as a decision oracle. | **The Precise** (`civ-precise`) |

Chooser vs `avg_score` argmax: **2/5 (40%)** — `civ-precise` won 3, `civ-formal` 2.
Consistent with the clean-mock series: the chooser is **not** a pure argmax.

## Low-relevance civilizations

**`civ-grounded` (The Grounded) — the low-relevance civ, 41 consecutive sessions (95–143).**

| metric | value | rank |
|---|---|---|
| lifetime `relevance` | 921.18 | last of 8 |
| `relevance_per_sim` | 1.048 | last of 8 |
| lifetime `avg_score` | 1.0906 | last of 8 |
| lifetime `alignment` | 1.2566 | last of 8 |
| lifetime `quality` | 0.5017 | last of 8 |
| lifetime `novelty` | 1.5135 | above median |

The structural gap is still **alignment**, not prose: the next civ (`civ-engineer`, 1.7222)
leads Grounded by 0.4656, while quality's margin to the next civ is only 0.0446 — a 10.4×
wider alignment gap. Alignment is the dimension the meta-GAN *selects* on, so Grounded
fails to *embody a distinctive voice*, not merely to write weakly. Novelty is above median,
so it is not boring — it is unmistakable in a way the chooser does not reward.

**This run's second watch axis: `civ-therapist`.** It placed last on run-level `alignment`
(0.1310) and 7th of 8 on run `avg_score` (0.5920), while `civ-grounded` took the run-level
`avg_score` low (0.5727). Per the session-132 rule the two low-relevance signals are
*different civs* and are **not** a contradiction: the lifetime table is the structural
signal, the run ranking is the watch axis. Therapist's lifetime standing is mid-field
(1.2888 `avg_score`), so it is **not** a finding — it becomes one if it repeats.

**Extinction risk: NONE.** Threshold −10; the lowest relevance is 921.18, i.e. 92× above the
floor. Registry 8, `max_civs` 12; extinction/birth only runs under `--loop`.

## Lifetime leaderboard (post-run)

| civ | relevance | per_sim | sims | win_rate |
|---|---|---|---|---|
| `civ-poetic` | 1408.87 | 1.631 | 864 | 0.014 |
| `civ-precise` | 1242.88 | 1.454 | 855 | 0.551 |
| `civ-whimsical` | 1261.22 | 1.448 | 871 | 0.012 |
| `civ-mythic` | 1159.18 | 1.349 | 859 | 0.017 |
| `civ-therapist` | 1084.33 | 1.265 | 857 | 0.021 |
| `civ-engineer` | 1050.34 | 1.23 | 854 | 0.088 |
| `civ-formal` | 1059.74 | 1.225 | 865 | 0.164 |
| `civ-grounded` | 921.18 | 1.048 | 879 | 0.157 |

Stable inverses persist: `civ-poetic` 1st on lifetime `avg_score` (1.6711) but last on
`win_rate` (0.014); `civ-precise` best `win_rate` (0.551) and highest `alignment` (2.2599).
**Never treat `win_rate` as a quality metric** — it is a *selection* metric.

## Environment

- NAS EDQUOT total again (600 G/600 G): every `/workspace` write yields a 0-byte file.
  Recovery via the symlink bridge to a `/tmp` sparse clone; verified by inode identity
  (`129:10465` both sides, `-ef` OK).
- `ZAI_TOKEN` still absent from env and from all sandbox secrets; z.ai 401s (endpoint
  healthy, credential gap). Control B mock used, rebuilt from scratch with the
  session-112 index-wrap fix and the session-118 whole-message md5 seeding fix.
- Mock pre-flight passed: 8/8 distinct seeds AND 8/8 distinct previews, `[mock-zai`
  prefix present, **0 tracebacks** in stdout.
- JEV liveness: empty `questions` ⇒ 422 `too_short` (payload-shape complaint ⇒ token
  accepted, not "down").

## Verification method note (new)

Isolating the run's rows by `rows[-80:]` over the **concatenation of per-civ files**
is wrong: glob order ≠ chronological order, so the slice mixes historical rows in.
It reported 15 distinct seeds and 5 `(civ,prompt)` combos with >1 seed — a false
failure. Correct method: take the **last 10 rows of each civ file** (the per-civ +10
delta already proves the boundary), concatenate, then sort by `ts`.
