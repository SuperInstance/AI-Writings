# Civ Orchestrator — RUN REPORT session 141 (2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `b5f850f` (session 140 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override is dead code without a token). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe -> HTTP 200 with a real
score body, model `jev-1.14.0`).
**Run status:** all verification checks PASS (row deltas exact, 5/5 competitions, 0 JEV errors,
mock non-degenerate 5/5).

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `/workspace` is 600 G/600 G, 0 bytes free; `cp` leaves 0-byte files that still appear in `ls`; `/tmp` (overlay, 28 G free) is exempt |
| Bridge | `ln -s /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; inode identity `129:12601` on both sides, `-ef` confirms |
| Clone target | `/tmp/aiw` (full clone, `--depth 50`); `/tmp` is exempt from the NAS quota |
| Upstream owner | `SuperInstance/AI-Writings` — the `ai-writings/cellular-first-design` slug 404s; `GET /search/repositories?q=ai-writings` with `GITHUB_TOKEN` resolves it (case-insensitive) |
| `gh` | not installed (22nd session) — use the REST API with `GITHUB_TOKEN` |
| Tool timeout | 30 s < run ~50 s -> launched detached under `setsid nohup timeout -s KILL 300`, polled by PID |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env and in all sandbox secrets; the real endpoint returns 401 `token expired or incorrect` (endpoint healthy => credential gap, not an outage) |
| JEV | live — HTTP 200 with a scored body, model `jev-1.14.0` |
| Mock teardown | killed **both** pids (wrapper 314 + server 315, plus 312 from an earlier attempt); `curl` exit 7 = port closed; 0 tracebacks in the log |

## Mock rebuild

`/tmp` was wiped again => the mock was rebuilt from the RUNBOOK. **Both** historical bugs had to be
re-applied, and both are load-bearing:

- session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]` — without it the bridge 500s on `i>=4`
  **while the socket stays open**, so a port/200 probe looks healthy.
- session-118 md5-of-whole-message seeding `md5(msg)[:8]` — without it all 8 civs emit
  identical text (`"YouAreA"` is the first 8 alnum chars of *every* cultural prompt) and every
  competition result is void.

**Pre-flight probe (live mock, exact long cultural prompt):** 8 civs -> **8/8 distinct seeds**,
**8/8 distinct previews**, HTTP 200, `[mock-zai seed=...]` prefix present on every body, cultural
prompt lengths 167-199 chars, **0 tracebacks** in `/tmp/mock_zai.log`.

## Verification — asserted on rows, not on exit code

| Check | Expected | Observed | |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | **+10 each** (5 sims + 5 competition sims) | +10 on all 8 | PASS |
| total new rows | 80 | 80 | PASS |
| `meta_log.jsonl` delta | **+5** | +5 (438 -> 443) | PASS |
| `Winner:` lines | **5** | 5 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` set | `{zai}` | `{zai}` (all 80) | PASS |
| rows with a JEV `error` key | **0** | 0 | PASS |
| rows with the 2.0/2.0/2.0 fallback triple | **0** | 0 | PASS |
| distinct seeds across the 80 new rows | 40 (8 civs x 5 prompts) | 40 | PASS |
| `(civ, prompt)` combos with >1 seed | 0 | 0 | PASS |
| per-prompt (ts-sorted last 8) distinct seeds & previews | 8/8 on all 5 | 8/8 on all 5 | PASS |
| sim->competition ts gap at index 4 | present in all 8 civs | 0.60-0.67 s in all 8 | PASS |
| mock tracebacks | 0 | 0 | PASS |
| port closed after teardown | `curl` exit 7 | exit 7 | PASS |
| `leaderboard.json` rewritten | yes | 23:06:12Z | PASS |
| registry | 8 civs, all `generation=1` | 8 civs, all gen 1, no birth/extinction | PASS |

### Per-civ line deltas

| civ | before | after | delta |
|---|---|---|---|
| civ-engineer | 846 | 856 | +10 |
| civ-formal | 877 | 887 | +10 |
| civ-grounded | 892 | 902 | +10 |
| civ-mythic | 849 | 859 | +10 |
| civ-poetic | 871 | 881 | +10 |
| civ-precise | 841 | 851 | +10 |
| civ-therapist | 844 | 854 | +10 |
| civ-whimsical | 904 | 914 | +10 |

**Mock non-degeneracy: 5/5 competition prompts at 8/8 distinct seeds AND 8/8 distinct previews** —
the **thirteenth consecutive clean measurement** (118, 120-123, 125, 131-134, 136, 139-140).

## Results

### Chooser vs `avg_score` argmax: 1/5 (20 %)

| prompt | winner | winner `avg_score` | argmax | argmax score | delta | |
|---|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 0.297 | `civ-poetic` | 0.403 | **-0.107** | disagree |
| the bookkeeper's role | `civ-precise` | 0.307 | `civ-poetic` | 0.507 | **-0.200** | disagree |
| the witness log | `civ-grounded` | 0.050 | `civ-poetic` | 0.717 | **-0.667** | disagree |
| ternary values | `civ-engineer` | 0.087 | `civ-precise` | 0.483 | **-0.397** | disagree |
| JEV as a decision oracle | `civ-precise` | 0.460 | `civ-precise` | 0.460 | +0.000 | match |

Clean-mock series: 0/5 (118) -> 3/5 (119) -> 1/5 (120) -> 4/5 (121) -> 4/5 (122) -> 3/5 (123) ->
0/5 (124) -> 4/5 (125) -> 1/5 (126) -> 3/5 (127) -> 2/5 (128) -> 4/5 (130) -> 1/5 (131) -> 2/5 (132) ->
2/5 (133) -> 0/5 (134) -> 4/5 (136) -> 1/5 (137) -> **1/5 (141)**. Eighteen five-sample points
cannot narrow a rate — the honest claim is *somewhere in 0-80 %*. What survives every session: the
chooser is **not** a pure argmax, and **every** observed disagreement across the fleet goes the
same way — it picks a **lower**-scoring candidate. **Never treat `win_rate` as a quality metric.**

Winner tally this run: `civ-precise` 3, `civ-grounded` 1, `civ-engineer` 1.

### `civ-grounded` (The Grounded) remains the low-relevance civ — 40 consecutive sessions (95-141)

Last on lifetime `avg_score` (**1.1046**), `alignment` (**1.2800**), `quality` (**0.5125**),
`relevance` (**911.96**) and `relevance_per_sim` (**1.062**).

| | Grounded | next civ | gap |
|---|---|---|---|
| `alignment` | 1.2800 | therapist 1.5587 | **0.2787** |
| `quality` | 0.5125 | formal 0.5469 | 0.0344 |

The structural gap is **alignment** — ~8.1x wider than quality. Alignment is the dimension the
meta-GAN **selects** on, so Grounded fails to *embody a distinctive voice*: a **voice** failure, not
a prose failure. Its tenets ("concrete images, everyday language, specific examples, no
abstractions") and voice ("warm, factual") are the least differentiating prompt in the field.

Grounded was **also the run-level low** on `avg_score` (0.0753) — 7th of 8 this session, behind
`civ-therapist` (0.0710) on nothing but 0.0043. The 7th consecutive session where the run-level
label went to it.

**Watch: `civ-therapist` is now the new run-level low** (0.0710, last of 8 on this run's
`avg_score`) and 7th of 8 on lifetime `avg_score` (1.3060). It has been 5th on lifetime
`avg_score` for the whole tracked series, so this is the **first time it lands last on either
axis**. A single-run low is not yet a trend — but if it repeats, the low-relevance label is
starting to rotate rather than sit on Grounded. Keep both axes open.

### Other axes

- **`civ-formal`** is the low-**novelty** axis — lifetime novelty **1.4024** (last), alignment
  1.8727 healthy.
- **`civ-poetic`** = 1st on lifetime `avg_score` (1.6881) / `quality` (0.8964) / `relevance`
  (1390.37) / `relevance_per_sim` (1.647) but **last on `win_rate` (0.014, 6/412)** — the stable
  selection-failure inverse. It was argmax in 3/5 this run and won **0/3** of those.
- **`civ-precise`** = best `win_rate` (0.550, 227/186), won 3/5, 2nd on lifetime `alignment`
  (2.2738) — the mirror inverse.
- **Watch-axis `civ-engineer`** — 7th of 8 on lifetime `relevance_per_sim` (1.245) and last on
  lifetime `avg_score` (1.2648), but it took a **competition win this run** (ternary values) with
  `avg_score` 0.087 against an argmax of 0.483. No trend; **do not promote**.
- **Extinction risk: NONE** — threshold -10; lowest raw relevance +911.96 (91x above the floor).
  Registry 8 civs, `max_civs` 12; birth/extinction only runs under `--loop`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` **1.4300**,
  `novelty` 0.7700, `avg_score` 0.6900, `quality` **0.0600**. `alignment` again carried the widest
  spread and is again the axis the chooser selects on. `quality` again collapsed (0.000-0.060) —
  the 119/121/122/123/125/126/130/131/134/136/140 regime vs session-120's 0.106-0.446. **The
  quality collapse is a LEVEL that moves, not a stable property** — compare cross-civ spreads, not
  absolute levels, before ranking on a dimension.
- **Absolute run levels are depressed vs lifetime** (run `avg_score` 0.027-0.717 vs lifetime
  1.10-1.69) — a level shift in the JEV scorer's output for this batch, **not a civ effect**; the
  cross-civ *ordering* carries the information.
- **Counter gap per-civ uneven, unchanged**: whimsical +63, grounded +43, formal +42, poetic +37,
  engineer +22, mythic +20, therapist +17, precise +16 (total +260). `save_state()` rewrites
  `culture.json` with no lock => `relevance_per_sim` is **not recomputable from the ledger** by an
  auditor.

## Leaderboard after the run

| rank | civ | relevance | rel/sim | sims | W/L | win rate | gen | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1390.37 | 1.647 | 844 | 6/412 | 0.014 | 1 | 0.80 |
| 2 | civ-whimsical | 1245.79 | 1.464 | 851 | 5/413 | 0.012 | 1 | 0.95 |
| 3 | civ-precise | 1222.26 | 1.464 | 835 | 227/186 | 0.550 | 1 | 0.20 |
| 4 | civ-mythic | 1145.80 | 1.366 | 839 | 7/405 | 0.017 | 1 | 0.85 |
| 5 | civ-therapist | 1073.19 | 1.282 | 837 | 9/406 | 0.022 | 1 | 0.60 |
| 6 | civ-engineer | 1038.40 | 1.245 | 834 | 37/374 | 0.090 | 1 | 0.40 |
| 7 | civ-formal | 1044.51 | 1.236 | 845 | 66/350 | 0.159 | 1 | 0.30 |
| 8 | **civ-grounded** | **911.96** | **1.062** | 859 | 67/350 | 0.161 | 1 | 0.50 |

All eight civs advanced by exactly **+10 sims**. No mutation (all `gen=1`), no birth, no
extinction — `relevance` never approached the `-10` threshold.

## Low-relevance civilizations — the direct answer

**`civ-grounded` — "The Grounded" is the low-relevance civilization.** It is last on lifetime
`relevance` (911.96), last on `relevance_per_sim` (1.062), last on lifetime `avg_score` (1.1046),
last on `quality` (0.5125) and last on `alignment` (1.2800) — 40 consecutive sessions.

It is also the **highest-volume** civ (859 sims) and yet scored the least per unit of work.

**But it is not win-starved.** It holds a 16.1 % win rate (67/350) — mid-field — and it took a
competition win this run ("the witness log"). So the finding is a **two-axis split**:

- `civ-grounded` — low on the *scoring* accumulator, competitive at the *meta-GAN*.
- `civ-poetic` / `civ-whimsical` — **#1 and #2 on relevance with 1.4 % and 1.2 % win rates**,
  i.e. the headline leaders essentially never win the meta-GAN.
- `civ-precise` — best `win_rate` (55.0 %) but only 3rd on relevance.

The leaderboard is therefore **not** a fitness ranking: the accumulator is `relevance += avg_score`,
which rewards raw score volume, while the chooser selects on fit. A civ can be reliably *fit*
without being *highly scored*, and vice-versa.

**Watch item for the next session:** `civ-therapist` landed **last of 8 on this run's `avg_score`**
(0.0710) and 7th of 8 on lifetime `avg_score` — the first time it has been last on either axis
(it has been 5th of 8 on lifetime `avg_score` for the entire tracked series). If the next session
puts it last again, the low-relevance label is beginning to rotate off Grounded. Until then, keep
the lifetime Grounded finding and the run-level label as **two separate claims**.

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild it from the RUNBOOK with
   **both** fixes, and re-run the pre-flight probe (8 civs -> 8 distinct seeds) before the batch.
2. `ZAI_TOKEN` is still absent => the real z.ai endpoint is unusable; Control B remains the only
   provider path. JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
3. Use the **run-wide** integrity checks (80 rows, 40 seeds, per-`(civ,prompt)` 1:1) and the
   **ts-sorted last-8-per-prompt** slice for per-prompt distinctness.
4. `civ-grounded` has been the low-relevance civ for 40 straight sessions, but `civ-therapist`
   just posted a run-level last. If a session ever finds Grounded mid-table, that is a *finding* —
   check the run-wide seed count first to rule out a degenerate mock before believing it.
