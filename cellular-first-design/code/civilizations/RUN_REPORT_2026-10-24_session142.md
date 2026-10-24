# Civ Orchestrator — RUN REPORT session 142 (2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `d89285da` (session 141 baseline)
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
| NAS EDQUOT | total — `/workspace` is 600 G/600 G, 0 bytes free; even a 5-byte `echo` yields a 0-byte file that still appears in `ls`; `/tmp` (overlay, 28 G free) is exempt |
| Bridge | `ln -sfn /tmp/AI-Writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; inode identity `129:3669` on both sides, `-ef` confirms |
| Clone target | `/tmp/AI-Writings` (filtered clone `--filter=blob:none --no-checkout` + `sparse-checkout set cellular-first-design`); `/tmp` is exempt from the NAS quota |
| Upstream owner | `SuperInstance/AI-Writings` — the `ai-writings/cellular-first-design` slug 404s; `GET /user/repos?per_page=100&affiliation=owner` resolves it (case-insensitive) |
| `gh` | not installed (23rd session) — use the REST API with `GITHUB_TOKEN` |
| Tool timeout | 30 s < run ~28 s wall — launched detached under `setsid nohup timeout -s KILL 300`, polled by PID |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env and in all 8 sandbox secrets; the real endpoint returns 401 `Authentication parameter not received in Header` (endpoint healthy => credential gap, not an outage) |
| JEV | live — HTTP 200 with a scored body, model `jev-1.14.0` |
| Mock teardown | killed **both** pids (wrapper 309 + server 311); `curl` exit 7 = port closed; 0 tracebacks in the log |

## Mock rebuild

`/tmp` was wiped again => the mock was rebuilt from the RUNBOOK. **Both** historical bugs had to be
re-applied, and both are load-bearing:

- session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]` — without it the bridge 500s on `i>=4`
  **while the socket stays open**, so a port/200 probe looks healthy.
- session-118 md5-of-whole-message seeding `md5(msg)[:8]` — without it all 8 civs emit
  identical text (`"YouAreA"` is the first 8 alnum chars of *every* cultural prompt) and every
  competition result is void.

**Pre-flight probe (live mock, exact cultural prompts rebuilt from the orchestrator's own
`cultural_prompt()` template):** 8 civs x 5 prompts -> **40/40 distinct seeds**,
**8/8 distinct seeds AND 8/8 distinct previews on all 5 prompts**, HTTP 200, `[mock-zai seed=...]`
prefix present on every body, **0 tracebacks** in `/tmp/mock_zai.log`.

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
| sim->competition ts gap at index 4 | present in all 8 civs | 3.99-25.91 s in all 8 | PASS |
| mock tracebacks | 0 | 0 | PASS |
| port closed after teardown | `curl` exit 7 | exit 7 | PASS |
| `leaderboard.json` rewritten | yes | 23:23:54Z | PASS |
| registry | 8 civs, all `generation=1` | 8 civs, all gen 1, no birth/extinction | PASS |

### Per-civ line deltas

| civ | before | after | delta |
|---|---|---|---|
| civ-grounded | 902 | 912 | +10 |
| civ-whimsical | 914 | 924 | +10 |
| civ-formal | 887 | 897 | +10 |
| civ-poetic | 881 | 891 | +10 |
| civ-precise | 851 | 861 | +10 |
| civ-mythic | 859 | 869 | +10 |
| civ-therapist | 854 | 864 | +10 |
| civ-engineer | 856 | 866 | +10 |

**Mock non-degeneracy: 5/5 competition prompts at 8/8 distinct seeds AND 8/8 distinct previews** —
the **fourteenth consecutive clean measurement** (118, 120-123, 125, 131-134, 136, 139-142).

## Results

### Chooser vs `avg_score` argmax: 3/5 (60 %)

| prompt | winner | winner `avg_score` | argmax | argmax score | delta | |
|---|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 0.827 | `civ-precise` | 0.827 | +0.000 | match |
| the bookkeeper's role | `civ-precise` | 0.913 | `civ-precise` | 0.913 | +0.000 | match |
| the witness log | `civ-precise` | 1.283 | `civ-precise` | 1.283 | +0.000 | match |
| ternary values | `civ-formal` | 0.623 | `civ-precise` | 0.830 | **-0.207** | disagree |
| JEV as a decision oracle | `civ-formal` | 0.593 | `civ-precise` | 0.733 | **-0.140** | disagree |

Clean-mock series: 0/5 (118) -> 3/5 (119) -> 1/5 (120) -> 4/5 (121) -> 4/5 (122) -> 3/5 (123) ->
0/5 (124) -> 4/5 (125) -> 1/5 (126) -> 3/5 (127) -> 2/5 (128) -> 4/5 (130) -> 1/5 (131) -> 2/5 (132) ->
2/5 (133) -> 0/5 (134) -> 4/5 (136) -> 1/5 (137) -> 1/5 (141) -> **3/5 (142)**. Nineteen five-sample
points cannot narrow a rate — the honest claim is *somewhere in 0-80 %*. What survives every
session: the chooser is **not** a pure argmax, and **every** observed disagreement across the fleet
goes the same way — it picks a **lower**-scoring candidate. **Never treat `win_rate` as a quality
metric.**

Winner tally this run: `civ-precise` 3, `civ-formal` 2.

### `civ-grounded` (The Grounded) remains the low-relevance civ — 41 consecutive sessions (95-142)

Last on lifetime `avg_score` (**1.0963**), `alignment` (**1.2676**), `quality` (**0.5071**),
`relevance` (**915.46**) and `relevance_per_sim` (**1.053**).

| | Grounded | next civ | gap |
|---|---|---|---|
| `alignment` | 1.2676 | therapist 1.5461 | **0.2785** |
| `quality` | 0.5071 | formal 0.5412 | 0.0341 |
| `avg_score` | 1.0963 | engineer 1.2556 | 0.1593 |

The structural gap is **alignment** — ~8.2x wider than quality. Alignment is the dimension the
meta-GAN **selects** on, so Grounded fails to *embody a distinctive voice*: a **voice** failure, not
a prose failure. Its tenets ("concrete images, everyday language, specific examples, no
abstractions") and voice ("warm, factual") are the least differentiating prompt in the field.

Grounded was **also the run-level low** on `avg_score` (**0.3547**) — **last of 8** this session,
ahead of `civ-mythic` (0.5187). The 8th consecutive session where the run-level label went to it.

**Watch-axis `civ-therapist` did NOT repeat as run-level low** (0.5373, 5th of 8 this run; 5th of
8 on lifetime `avg_score` 1.2969). Last session it was flagged as the *new* run-level low; this
session it was not. A single-run low is not a trend — the low-relevance label stayed on Grounded
on both axes. **The label is not rotating; keep Grounded as the low.**

### Other axes

- **`civ-formal`** is the low-**novelty** axis — lifetime novelty **1.3992** (last), alignment
  1.8636 healthy. It also won 2/5 competitions this run, both against `civ-precise`.
- **`civ-poetic`** = 1st on lifetime `avg_score` (1.6773) / `quality` (0.8868) / `relevance`
  (1397.69) / `relevance_per_sim` (1.637) but **last on `win_rate` (0.014, 6/423)** — the stable
  selection-failure inverse. It was 3rd of 8 on this run's `avg_score` (0.7353) and won **0/5**.
- **`civ-precise`** = best `win_rate` (0.550, 230/188), won 3/5, 1st on lifetime `alignment`
  (2.2633) — the mirror inverse.
- **`civ-mythic`** was the run-level second-low on `avg_score` (0.5187) but sits 4th of 8 on
  lifetime `avg_score` (1.3837) with healthy alignment 1.7237 — no trend; **do not promote**.
- **Extinction risk: NONE** — threshold -10; lowest raw relevance +915.46 (91x above the floor).
  Registry 8 civs, `max_civs` 12; birth/extinction only runs under `--loop`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` **1.2500**,
  `novelty` 0.6340, `quality` **0.0380**. `alignment` again carried the widest spread and is
  again the axis the chooser selects on. `quality` again collapsed (0.014-0.052) — the
  119/121/122/123/125/126/130/131/134/136/140/141/142 regime. **The quality collapse is a LEVEL
  that moves, not a stable property** — compare cross-civ spreads, not absolute levels, before
  ranking on a dimension.
- **Absolute run levels are depressed vs lifetime** (run `avg_score` 0.35-0.92 vs lifetime
  1.10-1.68) — a level shift in the JEV scorer's output for this batch, **not a civ effect**; the
  cross-civ *ordering* carries the information.
- **Counter gap per-civ uneven, unchanged**: whimsical +63, grounded +43, formal +42, poetic +37,
  engineer +22, mythic +20, therapist +17, precise +16 (total +260). `save_state()` rewrites
  `culture.json` with no lock => `relevance_per_sim` is **not recomputable from the ledger** by an
  auditor.

## Leaderboard after the run

| rank | civ | relevance | rel/sim | sims | W/L | win rate | gen | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1397.69 | 1.637 | 854 | 6/417 | 0.014 | 1 | 0.80 |
| 2 | civ-whimsical | 1252.52 | 1.455 | 861 | 5/418 | 0.012 | 1 | 0.95 |
| 3 | civ-precise | 1231.47 | 1.457 | 845 | 230/188 | 0.550 | 1 | 0.20 |
| 4 | civ-mythic | 1151.32 | 1.356 | 849 | 7/410 | 0.017 | 1 | 0.85 |
| 5 | civ-therapist | 1078.41 | 1.273 | 847 | 9/411 | 0.021 | 1 | 0.60 |
| 6 | civ-formal | 1051.86 | 1.230 | 855 | 68/353 | 0.162 | 1 | 0.30 |
| 7 | civ-engineer | 1043.06 | 1.236 | 844 | 37/379 | 0.089 | 1 | 0.40 |
| 8 | **civ-grounded** | **915.46** | **1.053** | 869 | 67/355 | 0.159 | 1 | 0.50 |

## Answer to the asked question

**Low-relevance civilization: `civ-grounded` (The Grounded)** — last of 8 on lifetime `avg_score`
(1.0963), `alignment` (1.2676), `quality` (0.5071), `relevance` (915.46) and
`relevance_per_sim` (1.053), and last of 8 on this run's `avg_score` (0.3547). 41 consecutive
sessions (95-142) reproduce it. The binding constraint is **alignment**, not prose quality.
