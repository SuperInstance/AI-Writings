# Civ Orchestrator — Run Report, Session 178

**Date:** 2026-10-25T06:05:36Z
**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Baseline:** HEAD `2049006` (session 177) — clean tree
**Provider path:** Control B (local mock z.ai on 127.0.0.1:8899), `ZAI_URL_OVERRIDE`
**JEV:** live, `jev-1.14.0`, `TYPESAFEAI_KEY` from `TYPESAFE_AI_TOKEN`

## Environment

The workspace arrived empty (a wipe): `/workspace/repos/ai-writings/...` did not exist.
Recovery: sparse clone of `SuperInstance/AI-Writings` into `/tmp` (repo is 3.7 GB),
branched to `/workspace/repos/ai-writings/cellular-first-design` via a symlink bridge
(`os.path.samefile` verified True, dev:ino 129:12602 on both sides).

`ZAI_TOKEN` is absent from the environment and z.ai returns `401 token expired or
incorrect` — endpoint healthy, credential missing. Control B (the local mock) is
therefore the only provider path, exactly as the durable learnings prescribe.
`ZAI_URL_OVERRIDE` alone is dead code (the token gate returns `None` first), so a
placeholder token was supplied.

## Pre-flight — 7/7 PASS

| Check | Result |
|---|---|
| distinct seeds | 40/40 |
| distinct previews | 40/40 |
| md5 recompute mismatches | 0/40 |
| (civ,prompt) pairs with >1 seed | 0 |
| **repeat-same-message determinism** | 0/16 unstable |
| index-wrap errors (i>=4) | 0/40 |
| seed widths | all 4 hex chars |

One implementation bug was found and fixed before the run: the mock computed
`figure = h[12:16] / h[16:20] / h[20:24]` on the *hex string*, raising
`TypeError` (HTTP 500 while the socket stayed open). The spec requires hex->int
conversion; the fix is `int(h[12:16],16)` etc.

## Run-wide verification — 12/12 PASS

- per-civ ledger delta **+10 x 8 = 80** new rows (5 sims + 5 competition rows each)
- `meta_log.jsonl` delta **+5**; `Winner:` lines = **5**
- wins/losses exact: **8/8** (`dWins + dLosses == 5`; `dLosses == 5 - dWins`)
- `relevance` delta == sum(this run's `avg_score`): **8/8 exact to 1e-13**
- distinct seeds **40/80**; **0** `(civ,prompt)` carrying >1 seed
- **80/80** rows match an independently recomputed message md5
- 8/8 distinct seeds AND previews on every competition prompt (5/5)
- meta-vs-ledger `avg_score` mismatches **0/40** (later-`ts` row)
- 0 JEV errors, 0 `2.0/2.0/2.0` fallback triples
- extinction risk **NONE** (threshold -10; lowest civ sits 120x above it)
- no births, no extinctions, all generations remain 1

### Measurement note (self-correction)

An initial check reported `relevance delta == sum(avg_score)` as **2/8 FAIL**. That
was a measurement error: it compared against the leaderboard's 2-decimal-rounded
`relevance`, not the unrounded `culture.json`. Re-derived against the pristine git
baseline (`git show HEAD:...`), all 8 are exact (residuals <= 3.4e-13). The
documented rule applies: compare within the same epoch against a git baseline.

## Leaderboard (post-run)

| # | civ | relevance | rel/sim | wins | losses | win_rate | temp |
|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1862.75 | 1.534 | 6 | 597 | 0.010 | 0.8 |
| 2 | civ-precise | 1709.72 | 1.419 | 366 | 232 | 0.612 | 0.2 |
| 3 | civ-whimsical | 1625.05 | 1.331 | 5 | 598 | 0.008 | 0.95 |
| 4 | civ-mythic | 1497.53 | 1.239 | 10 | 587 | 0.017 | 0.85 |
| 5 | civ-formal | 1431.36 | 1.178 | 94 | 507 | 0.156 | 0.3 |
| 6 | civ-engineer | 1369.81 | 1.138 | 47 | 549 | 0.079 | 0.4 |
| 7 | civ-therapist | 1362.06 | 1.128 | 11 | 589 | 0.018 | 0.6 |
| 8 | civ-grounded | 1201.73 | 0.978 | 70 | 532 | 0.116 | 0.5 |

**civ-precise took 5/5 competitions this run** (5 wins, 0 losses). Every other civ
went 0-5. Under the mock, the 8 civs' `content_preview` strings for a given prompt
differ only by the embedded seed/colour/figure fields, so the JEV `choice` question
resolved to the same civ on every prompt.

## Low-relevance civilizations

**Run-level low: `civ-whimsical`** (run avg 0.7103). The gap structure says this is
a **voice/alignment failure**, not a prose failure:

| | whimsical | next (therapist) | gap |
|---|---|---|---|
| run avg_score | 0.7103 | 0.8840 | 0.174 |
| alignment | 0.216 | 0.609 | **0.393** |

The alignment gap (0.393) is 2.3x the quality gap (0.174), and alignment is the
dimension the meta-GAN selects on. civ-whimsical also sits at the extreme of the
temperature range (temp 0.95) and has the highest lifetime `relevance_per_sim`
among the low-alignment group.

**Lifetime low: `civ-grounded`** (rel/sim 0.978, gap 0.150 to civ-therapist).

These are **different civs on different axes** — the run low rotates every session,
the lifetime low is structural. Do not promote the run low to the lifetime finding.

`win_rate` is **not** a quality metric: the chooser asks JEV a `choice` question
over 150-char previews, while `avg_score` is the mean of three `score` questions on
the same text. Different questions, different answers.

## Counter gap

Per-civ gap (`culture.json relevance_score` - ledger sum of `avg_score`):
fixed and **not accumulating** — delta exactly 0.000000 for all 8 civs vs the
pre-run baseline. Values: whimsical -173.14, poetic -96.80, formal -85.53,
grounded -84.35, mythic -51.11, engineer -44.24, therapist -42.11, precise -32.63.

**Correction to the durable learnings:** they state the gap is "fixed, not
accumulating: -609.9200, byte-identical" across civs. That single-civ observation
was generalized incorrectly. The gap is fixed **per civ** and differs between civs
(-173.14 to -32.63 here). The stable property is that it does not move between
epochs, not that it is one shared constant.

## Teardown

Mock killed by exact argv match (both PIDs: 358 wrapper, 360 server). Port proven
closed: `curl -m 5` -> exit 7, HTTP 000. No `pkill -f` (self-match hazard).
