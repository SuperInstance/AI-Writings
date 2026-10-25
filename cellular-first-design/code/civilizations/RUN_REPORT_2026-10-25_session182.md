# Civ Orchestrator — RUN REPORT session 182 (2026-10-25)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `2a774e3` (session 181 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override is dead code behind the token gate). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe -> HTTP 200 with a real
score body, model `jev-1.14.0`).
**Run status:** all verification checks PASS (per-civ row deltas exact, 5/5 competitions,
0 JEV errors, mock non-degenerate 5/5, spec-recompute 80/80).

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `/workspace` is 600 G/600 G, 0 bytes free; `git clone` into `/workspace` fails with `Disk quota exceeded`; `/tmp` (overlay, 28 G free) is exempt |
| Clone target | `/tmp/work/ai-writings` (full clone, `--depth 1`); the 3.7 GB upstream does not fit on the NAS mount |
| Bridge | `ln -sfn /tmp/work/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; verified with `[ -ef ]` -> `EF_OK` |
| Upstream owner | `SuperInstance/AI-Writings` — the `ai-writings/cellular-first-design` slug 404s; `GET /user/repos?per_page=100` resolves it (case-insensitive) |
| `gh` | not installed (24th session) — used the REST API with `GITHUB_TOKEN` |
| Tool timeout | 30 s < run ~27 s wall — launched detached under `setsid nohup timeout -s KILL 300`, polled by PID (762) |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env and in all 8 sandbox secrets; the real endpoint returns 401 `token expired or incorrect` (endpoint healthy => credential gap, not an outage) |
| JEV | live — HTTP 200 with a scored body, model `jev-1.14.0` |
| Mock teardown | killed **both** pids (wrapper 618 + server 620); `curl` exit 7 = port closed; 0 tracebacks in the log |

## Mock rebuild — the SEVEN fixes (session-181 spec), all load-bearing

Built to the canonical algorithm, with **fix (g)** (the one the "six fixes" list omits) applied
and the **seed slice widened to a contiguous 4 hex chars** per sessions 179/180/181:

```
d      = md5(cultural_prompt).digest()          # (b) the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                              # (f) MESSAGE-derived, NOT a counter
seed   = h[(i*2)%8:(i*2)%8+4]                  # (a)+(e) contiguous 4-char slice
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"   # (g) three STRING components, NOT a division
```

Plus: (c) `Connection: close` + `Content-Length`; (d) interpolate the seed placeholder.

**Two deviations caught before the run, not after:**

1. **Fix (g) was missing from the "six fixes" list.** The spec's `figure = h[12:16] / h[16:20] / h[20:24]`
   is **pseudo-code**: read literally it divides two `str` values and raises `TypeError`, so the
   mock 500s on **every** request **while the socket stays open** — a port/200 liveness probe still
   looks healthy. The first build of this session hit exactly that: **HTTP 500** on the first live
   probe. Correct form: `f"{h[12:16]}/{h[16:20]}/{h[20:24]}"`.
2. **The seed slice is `h[(i*2)%8:(i*2)%8+4]`** — a *contiguous* 4-char slice, not the
   2-char-slice-concatenation still shown in the older spec block. Concatenating two 2-char
   slices is **not** the same value as the contiguous slice, so a row written under one algorithm
   will not reconcile against a recompute under the other. **Check the SLICE, not the render.**

**Pre-flight gate (12 checks) — passed 12/12 on the FIRST build** after the two corrections
above, with the 40 exact cultural prompts rebuilt from the orchestrator's own template:
40/40 HTTP 200, 40/40 distinct seeds, 40/40 distinct previews, 40/40 seeds matching an
independently recomputed md5, 8/8 distinct seeds AND previews on every one of the 5 prompts,
0 literal `seed={}`, 0 `(civ,prompt)` with >1 seed, body lengths 212, 0 tracebacks, and the
**repeat-same-message => identical seed AND preview** probe (40 messages x 2) that is the only
check able to catch fix (f).

## Verification — asserted on rows, not on exit code

| Check | Expected | Observed | |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | **+10 each** (5 sims + 5 competition sims) | +10 on all 8 | PASS |
| total new rows | 80 | 80 | PASS |
| `meta_log.jsonl` delta | **+5** | +5 (643 -> 648) | PASS |
| `Winner:` lines | **5** | 5 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| rows with literal `seed={}` | 0 | 0 | PASS |
| `provider` set | `{zai}` | `{zai}` (all 80) | PASS |
| rows with a JEV `error` key | **0** | 0 | PASS |
| rows with the 2.0/2.0/2.0 fallback triple | **0** | 0 | PASS |
| rows matching spec-recomputed seed + color + figure | **80/80** | 80/80 (0 mismatches) | PASS |
| distinct seeds across the 80 new rows | 40 (8 civs x 5 prompts) | 40 | PASS |
| `(civ, prompt)` combos with >1 seed | 0 | 0 | PASS |
| distinct `(q,n,a)` triples | 80/80 | 80/80 | PASS |
| `relevance` delta == sum(`avg_score`), unrounded git baseline | **8/8 exact** | 8/8 (residuals <= 3.6e-13) | PASS |
| `wins`+`losses` delta | 5 per civ (40 total) | 5 per civ | PASS |
| mock tracebacks | 0 | 0 | PASS |
| port closed after teardown | `curl` exit 7 | exit 7, `HTTP=000` | PASS |
| `leaderboard.json` rewritten | yes | 06:55:25Z | PASS |
| registry | 8 civs, all `generation=1` | 8 civs, all gen 1, no birth/extinction | PASS |
| extinction | NONE | lowest +1250.21 = **125x** the -10 floor | PASS |

**21/21 assertions PASS.**

### Per-civ line deltas

| civ | before | after | delta | relevance delta |
|---|---|---|---|---|
| civ-grounded | 1302 | 1312 | +10 | +14.3233 |
| civ-whimsical | 1314 | 1324 | +10 | +17.8467 |
| civ-formal | 1287 | 1297 | +10 | +16.4267 |
| civ-poetic | 1281 | 1291 | +10 | +20.6133 |
| civ-precise | 1251 | 1261 | +10 | +19.6600 |
| civ-mythic | 1259 | 1269 | +10 | +16.0967 |
| civ-therapist | 1254 | 1264 | +10 | +16.1533 |
| civ-engineer | 1256 | 1266 | +10 | +15.5167 |

**Baseline taken from the git blob** (`git show HEAD:.../culture.json`, unrounded), never from
the leaderboard's 2-dp display value — otherwise the delta check carries phantom residuals of
up to +/-0.0067 per civ.

## Results

### Chooser vs `avg_score` argmax: 1/5 (20 %)

| prompt | winner | winner `avg_score` | argmax | argmax score | delta | |
|---|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 1.988 | `civ-poetic` | 2.095 | **-0.107** | disagree |
| the bookkeeper's role | `civ-precise` | 1.950 | `civ-poetic` | 2.187 | **-0.237** | disagree |
| the witness log | `civ-precise` | 2.046 | `civ-precise` | 2.046 | +0.000 | match |
| ternary values | `civ-precise` | 1.741 | `civ-poetic` | 1.931 | **-0.190** | disagree |
| JEV as a decision oracle | `civ-precise` | 1.812 | `civ-poetic` | 2.029 | **-0.217** | disagree |

`civ-precise` swept **5/5**. **All four disagreements took the LOWER-scoring candidate** — the
same one-directional pattern seen in sessions 179/180/181. The chooser is **not** a pure argmax,
and `win_rate` is a **selection** metric, not a quality metric.

### `civ-grounded` (The Grounded) remains the low-relevance civ — 56th consecutive session

Last on lifetime `avg_score` (**1.0172**), `alignment` (**1.0698**), `quality` (**0.4010**),
`relevance` (**1250.21**) and `relevance_per_sim` (**0.985**).

| | Grounded | next civ | gap |
|---|---|---|---|
| `alignment` | 1.0698 | therapist 1.2066 | **0.1367** |
| `quality` | 0.4010 | engineer 0.4445 | 0.0432 |
| `avg_score` | 1.0172 | engineer 1.1539 | 0.1367 |

The alignment gap is **3.16x** wider than the quality gap. Alignment is the dimension the
meta-GAN **selects** on, so Grounded fails to *embody a distinctive voice*: a **voice** failure,
not a prose failure. Its tenets ("concrete images, everyday language, specific examples, no
abstractions") and voice ("warm, factual") are the least differentiating prompt in the field.

Grounded was **also the run-level low** on `avg_score` (**1.4323**) — **last of 8** this session,
ahead of `civ-engineer` (1.5517). Unlike sessions 179-181, where the run-level low rotated
across three different civs, **this session the run-level low and the lifetime low are the same
civ** — the rotation did not reproduce.

### Other axes

- **`civ-therapist`** is the low-**alignment** axis — lifetime alignment **1.2066** (last),
  novelty 1.7863 healthy. Lifetime `avg_score` 1.1457 (7th of 8).
- **`civ-formal`** is the low-**novelty** axis — lifetime novelty **1.4981** (last), alignment
  1.6818 healthy.
- **`civ-poetic`** = 1st on lifetime `avg_score` (1.5649) / `quality` (0.7414) / `relevance`
  (1923.46) / `relevance_per_sim` (1.534) but **last on `win_rate` (0.010, 6/623)** — the stable
  selection-failure inverse.
- **`civ-precise`** = best `win_rate` (0.621, 384/234), swept 5/5, 1st on lifetime `alignment`
  (2.1354) — the mirror inverse.
- **Extinction risk: NONE** — threshold -10; lowest raw relevance +1250.21 (125x above the floor).
  Registry 8 civs, `max_civs` 12; birth/extinction only runs under `--loop`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` **1.3270**,
  `quality` 0.6430, `avg_score` 0.6290, novelty 0.1760. `alignment` again carried the widest
  spread and is again the axis the chooser selects on. **The quality collapse is a LEVEL that
  moves, not a stable property** — compare cross-civ spreads, not absolute levels, before
  ranking on a dimension.
- **Counter gap** (ledger `relevance` vs the leaderboard's rounded display) is a **fixed**
  offset, unchanged from sessions 179-181: the per-civ deltas are **0.000000** for all 8 civs.
  `save_state()` rewrites `culture.json` with no lock, so `relevance_per_sim` is **not
  recomputable from the ledger** by an auditor.

## Leaderboard after the run

| rank | civ | relevance | rel/sim | sims | W/L | win rate | gen | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1923.46 | 1.534 | 1254 | 6/617 | 0.010 | 1 | 0.80 |
| 2 | civ-precise | 1771.08 | 1.423 | 1245 | 384/234 | 0.621 | 1 | 0.20 |
| 3 | civ-whimsical | 1674.75 | 1.328 | 1261 | 5/618 | 0.008 | 1 | 0.95 |
| 4 | civ-mythic | 1544.15 | 1.236 | 1249 | 10/607 | 0.016 | 1 | 0.85 |
| 5 | civ-formal | 1484.32 | 1.183 | 1255 | 95/526 | 0.153 | 1 | 0.30 |
| 6 | civ-engineer | 1416.64 | 1.139 | 1244 | 48/568 | 0.078 | 1 | 0.40 |
| 7 | civ-therapist | 1406.07 | 1.128 | 1247 | 11/609 | 0.018 | 1 | 0.60 |
| 8 | **civ-grounded** | **1250.21** | **0.985** | 1269 | 70/552 | 0.113 | 1 | 0.50 |

## Answer to the asked question

**Low-relevance civilization: `civ-grounded` (The Grounded)** — last of 8 on lifetime `avg_score`
(1.0172), `alignment` (1.0698), `quality` (0.4010), `relevance` (1250.21) and
`relevance_per_sim` (0.985), and last of 8 on this run's `avg_score` (1.4323). 56 consecutive
sessions (95-182) reproduce it. The binding constraint is **alignment**, not prose quality.
