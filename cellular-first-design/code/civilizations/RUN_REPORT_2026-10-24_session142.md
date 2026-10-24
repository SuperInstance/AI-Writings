# Civ Orchestrator — RUN REPORT session 142 (2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `d89285d` (session 141 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override is dead code without a token). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe -> HTTP 200, real score
body, model `jev-1.14.0`).
**Run status:** all verification checks PASS (row deltas exact, 5/5 competitions, 0 JEV errors,
mock non-degenerate 5/5, 14th consecutive clean measurement).

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `/workspace` is 600 G/600 G, 0 bytes free; `git config --global` fails with `Disk quota exceeded`; `/tmp` (overlay, 28 G free) is exempt |
| Bridge | `ln -sfn /tmp/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; inode identity `129:12602` on both sides, `-ef` confirms |
| Clone target | `/tmp/ai-writings` (full clone, `--depth 1`); `/tmp` is exempt from the NAS quota |
| Upstream owner | `SuperInstance/AI-Writings` — the `ai-writings/cellular-first-design` slug 404s; `GET /search/repositories?q=ai-writings` with `GITHUB_TOKEN` resolves it (case-insensitive) |
| `gh` | not installed (23rd session) — use the REST API with `GITHUB_TOKEN` |
| Tool timeout | 30 s < run ~45 s -> launched detached under `setsid nohup timeout -s KILL 600`, polled by PID |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env and in all 8 sandbox secrets; real endpoint unusable |
| JEV | live — HTTP 200 with a scored body, model `jev-1.14.0` |
| Mock teardown | killed server pid 277 (wrapper 276 died with it); `curl` exit 7 = port closed; 0 tracebacks in `/tmp/mock_zai.log` |

## Mock rebuild

`/tmp` was wiped again => the mock was rebuilt from the RUNBOOK. **Both** historical bugs had to be
re-applied, and both are load-bearing:

- session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]` — without it the bridge 500s on `i>=4`
  **while the socket stays open**, so a port/200 probe looks healthy.
- session-118 md5-of-whole-message seeding `md5(msg)[:8]` — without it all 8 civs emit
  identical text (`"YouAreA"` is the first 8 alnum chars of *every* cultural prompt) and every
  competition result is void.

**Pre-flight probe (live mock, exact long cultural prompt):** 8 civs -> **8/8 distinct seeds**,
**8/8 distinct previews**, HTTP 200, `[mock-zai seed=...]` prefix present on every body,
**0 tracebacks** in `/tmp/mock_zai.log`.

## Verification — asserted on rows, not on exit code

| Check | Expected | Observed | |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | **+10 each** (5 sims + 5 competition sims) | +10 on all 8 | PASS |
| total new rows | 80 | 80 | PASS |
| `meta_log.jsonl` delta | **+5** | +5 (443 -> 448) | PASS |
| `Winner:` lines | **5** | 5 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` set | `{zai}` | `{zai}` (all 80) | PASS |
| rows with a JEV `error` key | **0** | 0 | PASS |
| rows with the 2.0/2.0/2.0 fallback triple | **0** | 0 | PASS |
| distinct seeds across the 80 new rows | 40 (8 civs x 5 prompts) | 40 | PASS |
| `(civ, prompt)` combos with >1 seed | 0 | 0 | PASS |
| per-prompt (ts-sorted last 8) distinct seeds & previews | 8/8 on all 5 | 8/8 on all 5 | PASS |
| mock tracebacks | 0 | 0 | PASS |
| port closed after teardown | `curl` exit 7 | exit 7 | PASS |
| `leaderboard.json` rewritten | yes | 23:13:30Z | PASS |
| registry | 8 civs, all `generation=1` | 8 civs, all gen 1, no birth/extinction | PASS |

### Per-civ line deltas

| civ | before | after | delta |
|---|---|---|---|
| civ-engineer | 856 | 866 | +10 |
| civ-formal | 887 | 897 | +10 |
| civ-grounded | 902 | 912 | +10 |
| civ-mythic | 859 | 869 | +10 |
| civ-poetic | 881 | 891 | +10 |
| civ-precise | 851 | 861 | +10 |
| civ-therapist | 854 | 864 | +10 |
| civ-whimsical | 914 | 924 | +10 |

**Mock non-degeneracy: 5/5 competition prompts at 8/8 distinct seeds AND 8/8 distinct previews** —
the **fourteenth consecutive clean measurement** (118, 120-123, 125, 131-134, 136, 139-141).

## Results

### Chooser vs `avg_score` argmax: 2/5 (40 %)

| prompt | winner | winner `avg_score` | argmax | argmax score | delta | |
|---|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 0.630 | `civ-poetic` | 0.777 | **-0.147** | disagree |
| the bookkeeper's role | `civ-precise` | 0.560 | `civ-precise` | 0.560 | +0.000 | match |
| the witness log | `civ-formal` | 0.097 | `civ-precise` | 0.917 | **-0.820** | disagree |
| ternary values | `civ-formal` | 0.247 | `civ-whimsical` | 0.587 | **-0.340** | disagree |
| JEV as a decision oracle | `civ-precise` | 0.677 | `civ-precise` | 0.677 | +0.000 | match |

Clean-mock series: 0/5 (118) -> 3/5 (119) -> 1/5 (120) -> 4/5 (121) -> 4/5 (122) -> 3/5 (123) ->
0/5 (124) -> 4/5 (125) -> 1/5 (126) -> 3/5 (127) -> 2/5 (128) -> 4/5 (130) -> 1/5 (131) -> 2/5 (132) ->
2/5 (133) -> 0/5 (134) -> 4/5 (136) -> 1/5 (137) -> 1/5 (141) -> **2/5 (142)**. Twenty 5-sample
points cannot narrow a rate — the honest claim stays *somewhere in 0-80 %*. What survives every
session: the chooser is **not** a pure argmax, and **every** observed disagreement across the
fleet goes the same way — it picks a **lower**-scoring candidate. **Never treat `win_rate` as a
quality metric.**

Winner tally this run: `civ-precise` 3, `civ-formal` 2.

### `civ-grounded` (The Grounded) remains the low-relevance civ — 41 consecutive sessions (95-142)

Last on lifetime `avg_score` (**1.0947**), `alignment` (**1.2666**), `quality` (**0.5070**),
`relevance` (**914.02**) and `relevance_per_sim` (**1.052**).

| | Grounded | next civ | gap |
|---|---|---|---|
| `alignment` | 1.2666 | engineer 1.7281 | **0.4615** |
| `quality` | 0.5070 | engineer 0.5523 | 0.0453 |

The structural gap is **alignment** — **10.2x** wider than quality (the fleet's widest alignment
gap to date; prior session was 8.1x). Alignment is the dimension the meta-GAN **selects** on, so
Grounded fails to *embody a distinctive voice*: a **voice** failure, not a prose failure. Its
tenets ("concrete images, everyday language, specific examples, no abstractions") and voice
("warm, factual") are the least differentiating prompt in the field.

Grounded was **also the run-level low** on `avg_score` (0.2053) — 5th of 8 this session, behind
`civ-mythic` (0.1963) and `civ-engineer` (0.1963) by <0.01. The 7th consecutive session where
the run-level label went to it.

**Watch: `civ-therapist` is the new run-level low** (0.1720, last of 8 on this run's `avg_score`),
and it is now **8th of 8 on lifetime `avg_score`** (1.2928) — the second consecutive session it has
been last on either axis. Session 141 flagged this as "if it repeats, the low-relevance label is
starting to rotate rather than sit on Grounded." **It repeated.** This is now a two-session
pattern, not a single-run blip. Keep both axes open: the *lifetime* low is still Grounded
(41 straight sessions), but the *run-level* low has moved to Therapist and stayed there.

### Other axes

- **`civ-formal`** is the low-**novelty** axis — lifetime novelty **1.3930** (last), alignment
  1.8538 healthy.
- **`civ-poetic`** = 1st on lifetime `avg_score` (1.6729) / `quality` (0.8865) / `relevance`
  (1393.74) / `relevance_per_sim` (1.632) but **last on `win_rate` (0.014, 6/417)** — the stable
  selection-failure inverse. It was argmax in 1/5 this run and won **0/1** of that.
- **`civ-precise`** = best `win_rate` (0.550, 230/188), won 3/5, 2nd on lifetime `alignment`
  (2.2590) and 2nd on `relevance_per_sim` (1.453) — the mirror inverse, and it **overtook
  `civ-whimsical` for rank 2** on the leaderboard (1.453 vs 1.452) for the first time.
- **Watch-axis `civ-engineer`** — 7th of 8 on lifetime `relevance_per_sim` (1.233), 7th of 8 on
  lifetime `avg_score` (1.2524), took **no** competition win this run. No trend; **do not promote**.
- **Extinction risk: NONE** — threshold -10; lowest raw relevance +914.02 (91x above the floor).
  Registry 8 civs, `max_civs` 12; birth/extinction only runs under `--loop`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` **0.9780**,
  `avg_score` 0.3760, `novelty` 0.2850, `quality` **0.0130**. `alignment` again carried the widest
  spread and is again the axis the chooser selects on. `quality` again collapsed (0.007-0.020) —
  the long regime vs session-120's 0.106-0.446. **The quality collapse is a LEVEL that moves, not
  a stable property** — compare cross-civ spreads, not absolute levels, before ranking.
- **Absolute run levels are depressed vs lifetime** (run `avg_score` 0.172-0.548 vs lifetime
  1.09-1.67) — a level shift in the JEV scorer's output for this batch, **not a civ effect**; the
  cross-civ *ordering* carries the information.
- **Counter gap per-civ uneven, unchanged**: whimsical +65, grounded +43, formal +42, poetic +37,
  engineer +22, mythic +20, therapist +17, precise +16 (total +262). `save_state()` rewrites
  `culture.json` with no lock => `relevance_per_sim` is **not recomputable from the ledger** by an
  auditor.

## Leaderboard after the run

| rank | civ | relevance | rel/sim | sims | W/L | win rate | gen | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1393.74 | 1.632 | 854 | 6/417 | 0.014 | 1 | 0.80 |
| 2 | civ-precise | 1227.74 | 1.453 | 845 | 230/188 | 0.550 | 1 | 0.20 |
| 3 | civ-whimsical | 1250.49 | 1.452 | 861 | 5/418 | 0.012 | 1 | 0.95 |
| 4 | civ-mythic | 1147.76 | 1.352 | 849 | 7/410 | 0.017 | 1 | 0.85 |
| 5 | civ-therapist | 1074.91 | 1.269 | 847 | 9/411 | 0.021 | 1 | 0.60 |
| 6 | civ-engineer | 1040.36 | 1.233 | 844 | 37/379 | 0.089 | 1 | 0.40 |
| 7 | civ-formal | 1047.00 | 1.225 | 855 | 68/353 | 0.162 | 1 | 0.30 |
| 8 | **civ-grounded** | **914.02** | **1.052** | 869 | 67/355 | 0.159 | 1 | 0.50 |

All eight civs advanced by exactly **+10 sims**. No mutation (all `gen=1`), no birth, no
extinction — `relevance` never approached the `-10` threshold.

## Low-relevance civilizations — the direct answer

**`civ-grounded` — "The Grounded" is the low-relevance civilization.** It is last on lifetime
`relevance` (914.02), last on `relevance_per_sim` (1.052), last on lifetime `avg_score` (1.0947),
last on `quality` (0.5070) and last on `alignment` (1.2666) — 41 consecutive sessions.

It is also the **highest-volume** civ (869 sims) and yet scored the least per unit of work.

**But it is not win-starved.** It holds a 15.9 % win rate (67/355) — mid-field. So the finding is
a **two-axis split**:

- `civ-grounded` — low on the *scoring* accumulator, competitive at the *meta-GAN*.
- `civ-poetic` / `civ-whimsical` — **#1 and #3 on relevance with 1.4 % and 1.2 % win rates**,
  i.e. the headline leaders essentially never win the meta-GAN.
- `civ-precise` — best `win_rate` (55.0 %) but only 2nd on relevance.

The leaderboard is therefore **not** a fitness ranking: the accumulator is `relevance += avg_score`,
which rewards raw score volume, while the chooser selects on fit. A civ can be reliably *fit*
without being *highly scored*, and vice-versa.

**Watch item for the next session — the label is starting to rotate.** `civ-grounded` held the
run-level low for 7 consecutive sessions, but **this run it was 5th of 8** on run-level
`avg_score` (0.2053), behind `civ-mythic` and `civ-engineer` by less than 0.01, while
**`civ-therapist` took the run-level low (0.1720) for the second consecutive session** and now
sits **8th of 8 on lifetime `avg_score`** (1.2928) — the first time it has been last on either
axis in two running sessions. If session 143 puts Therapist last again, the low-relevance label
has genuinely rotated. Until then, keep the lifetime Grounded finding and the run-level label as
**two separate claims**.

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild it from the RUNBOOK with
   **both** fixes, and re-run the pre-flight probe (8 civs -> 8 distinct seeds) before the batch.
2. `ZAI_TOKEN` is still absent => the real z.ai endpoint is unusable; Control B remains the only
   provider path. JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
3. Use the **run-wide** integrity checks (80 rows, 40 seeds, per-`(civ,prompt)` 1:1) and the
   **ts-sorted last-8-per-prompt** slice for per-prompt distinctness.
4. The low-relevance label may be rotating from `civ-grounded` to `civ-therapist` (2 consecutive
   run-level lows). If a session ever finds Grounded mid-table, that is a *finding* — check the
   run-wide seed count first to rule out a degenerate mock before believing it.
5. `civ-precise` took rank 2 on `relevance_per_sim` (1.453 vs whimsical 1.452) for the first time
   — a hairline lead; do not report it as a crossover until the gap exceeds 0.01.
