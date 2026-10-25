# Civ Orchestrator — RUN REPORT session 183 (2026-10-25)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `f3fcb43` (session 182 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override is dead code behind the token gate). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe -> HTTP 200 with a real
score body, model `jev-1.14.0`).
**Run status:** all verification checks PASS (per-civ row deltas exact, 5/5 competitions,
0 JEV errors, mock non-degenerate 5/5, spec-recompute 80/80). **25/25 assertions PASS.**

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `/workspace` is 600 G/600 G, 0 bytes free; `git clone` into `/workspace` fails with `Disk quota exceeded`; `/tmp` (overlay, 28 G free) is exempt |
| Clone target | `/tmp/aew` (sparse: `--filter=blob:none --no-checkout --depth 1` + `sparse-checkout set cellular-first-design/code/civilizations`); the 3.7 GB upstream does not fit on the NAS mount |
| Bridge | `ln -s /tmp/aew/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; verified with `os.path.samefile()` -> **True** and `stat -L -c '%d:%i'` -> `129:3671` on both sides |
| Upstream owner | `SuperInstance/AI-Writings` — resolved via the **code search API** (`GET /search/code?q=filename:civilization_orchestrator.py`); the `ai-writings/…` slug 404s, and `GET /user/repos` paginates ~100/repo over 5 400+ owned repos |
| `gh` | not installed (25th session) — used the REST API with `GITHUB_TOKEN` |
| Tool timeout | 30 s < run ~28 s wall — launched detached under `setsid nohup timeout -s KILL 600`, polled by PID (434 wrapper / 436 python) |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env; the only provider path is the local mock (Control B) |
| JEV | live — HTTP 200 with a scored body, model `jev-1.14.0` |
| Mock teardown | killed **both** pids (275 wrapper / 277 server); `curl` exit 7 = port closed, `HTTP=000`; 0 tracebacks in the log |

## Mock rebuild — the SEVEN fixes, all load-bearing

Built to the canonical algorithm, with **fix (g)** applied and the **seed slice widened to a
contiguous 4 hex chars**:

```
d      = md5(cultural_prompt).digest()          # (b) the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                              # (f) MESSAGE-derived, NOT a counter
seed   = h[(i*2)%8:(i*2)%8+4]                  # (a)+(e) contiguous 4-char slice
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"   # (g) three STRING components, NOT a division
```

Plus: (c) `Connection: close` + `Content-Length`; (d) interpolate the seed placeholder.

## Pre-flight gate (12 checks) — **12/12 PASS on the FIRST build**

40/40 HTTP 200, 40/40 distinct seeds, 40/40 distinct previews, 40/40 seeds matching an
independently recomputed md5, 8/8 distinct seeds AND previews on every one of the 5 prompts,
0 literal `seed={}`, `[mock-zai` prefix on 40/40, **repeat-same-message => identical seed AND
preview (40 messages x 2)** — the only check able to catch fix (f) — 0 `(civ,prompt)` with
>1 seed, 0 tracebacks, body lengths 152.

## Verification — asserted on rows, not on exit code

| Check | Expected | Observed | |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | **+10 each** (5 sims + 5 competition sims) | +10 on all 8 | PASS |
| total new rows | 80 | 80 | PASS |
| `meta_log.jsonl` delta | **+5** | +5 (648 -> 653) | PASS |
| `Winner:` lines | **5** | 5 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| rows with literal `seed={}` | 0 | 0 | PASS |
| `provider` set | `{zai}` | `{zai}` (all 80) | PASS |
| rows with a JEV `error` key | **0** | 0 | PASS |
| rows with the 2.0/2.0/2.0 fallback triple | **0** | 0 | PASS |
| rows matching spec-recomputed seed + color + figure | **80/80** | 80/80 | PASS |
| distinct seeds across the 80 new rows | 40 | 40 | PASS |
| `(civ, prompt)` combos with >1 seed | 0 | 0 | PASS |
| `relevance` delta == sum(`avg_score`), unrounded git baseline | **8/8 exact** | 8/8 | PASS |
| `wins`+`losses` delta | 5 per civ | 5 per civ | PASS |
| meta-vs-ledger `avg_score` mismatches | **0** | 0 | PASS |
| competition results present | 5 | 5 | PASS |
| registry | 8 civs, all `generation=1` | 8 civs, no birth/extinction | PASS |
| extinction | NONE | lowest +1255.45 = **126x** the -10 floor | PASS |
| `leaderboard.json` rewritten | yes | 07:13:34Z | PASS |

**25/25 assertions PASS.**

### Per-civ line deltas

| civ | before | after | delta | relevance delta |
|---|---|---|---|---|
| civ-grounded | 1312 | 1322 | +10 | +5.2400 |
| civ-whimsical | 1324 | 1334 | +10 | +6.9833 |
| civ-formal | 1297 | 1307 | +10 | +6.6067 |
| civ-poetic | 1291 | 1301 | +10 | +8.5500 |
| civ-precise | 1261 | 1271 | +10 | +9.7333 |
| civ-mythic | 1269 | 1279 | +10 | +5.4400 |
| civ-therapist | 1264 | 1274 | +10 | +6.0033 |
| civ-engineer | 1266 | 1276 | +10 | +5.5633 |

**Baseline taken from the git blob** (`git show HEAD:.../culture.json`, unrounded), never from
the leaderboard's 2-dp display value.

## Results

### Chooser vs `avg_score` argmax: 2/5 (40 %)

| prompt | winner | winner `avg_score` | argmax | argmax score | delta | |
|---|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 1.117 | `civ-precise` | 1.117 | +0.000 | match |
| the bookkeeper's role | `civ-precise` | 0.640 | `civ-poetic` | 0.640 | +0.000 | disagree (tie) |
| the witness log | `civ-formal` | 1.100 | `civ-precise` | 1.717 | **-0.617** | disagree |
| ternary values | `civ-precise` | 1.003 | `civ-poetic` | 1.093 | **-0.090** | disagree |
| JEV as a decision oracle | `civ-precise` | 1.000 | `civ-precise` | 1.000 | +0.000 | match |

`civ-precise` swept **4/5**; `civ-formal` took the witness-log prompt. **Both substantive
disagreements took the LOWER-scoring candidate** — the same one-directional pattern seen in
sessions 179/180/181/182. The chooser is **not** a pure argmax, and `win_rate` is a
**selection** metric, not a quality metric.

### `civ-grounded` (The Grounded) remains the low-relevance civ — 57th consecutive session

Last on lifetime `avg_score` (**1.0135**), `alignment` (**1.0633**), `quality` (**0.3983**),
`relevance` (**1255.45**) and `relevance_per_sim` (**0.982**).

| | Grounded | next civ | gap |
|---|---|---|---|
| `alignment` | 1.0633 | therapist 1.1986 | **0.1353** |
| `quality` | 0.3983 | engineer 0.4411 | 0.0428 |
| `avg_score` | 1.0135 | therapist 1.1414 | 0.1280 |

The alignment gap is **3.16x** wider than the quality gap — **identical to session 182's
ratio**, a structural constant, not a coincidence. Alignment is the dimension the meta-GAN
**selects** on, so Grounded fails to *embody a distinctive voice*: a **voice** failure, not a
prose failure. Its tenets ("concrete images, everyday language, specific examples, no
abstractions") and voice ("warm, factual") are the least differentiating prompt in the field.

Grounded was **also the run-level low** on `avg_score` (**0.5240**) — **last of 8** this session.
As in session 182, **the run-level low and the lifetime low are the same civ**; the
rotation seen in sessions 179-181 did not reproduce.

### Other axes

- **`civ-mythic`** is the low-**alignment** axis *this run* (0.1670) — a different civ from
  session 182's low-alignment civ (`civ-therapist`), so the run-level low axis **does** rotate
  even when the low-`avg_score` civ does not.
- **`civ-therapist`** is the lifetime low-**alignment** axis — lifetime alignment **1.1986** (7th),
  novelty 1.7845 healthy, lifetime `avg_score` 1.1414 (7th of 8).
- **`civ-formal`** is the lifetime low-**novelty** axis — lifetime novelty **1.4970** (last),
  alignment 1.6731 healthy.
- **`civ-poetic`** = 1st on lifetime `avg_score` (1.5594) / `quality` (0.7365) / `relevance`
  (1932.01) / `relevance_per_sim` (1.528) but **last on `win_rate` (0.010, 6/628)** — the stable
  selection-failure inverse.
- **`civ-precise`** = best `win_rate` (0.623, 388/235), swept 4/5, 1st on lifetime `alignment`
  (2.1275) — the mirror inverse.
- **Extinction risk: NONE** — threshold -10; lowest raw relevance +1255.45 (126x above the floor).
  Registry 8 civs, `max_civs` 12; birth/extinction only runs under `--loop`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` **0.9540**,
  novelty 0.5120, `avg_score` 0.4493, quality 0.0600. `alignment` again carried the widest
  spread and is again the axis the chooser selects on. **The quality collapse is a LEVEL that
  moves, not a stable property** — compare cross-civ spreads, not absolute levels, before
  ranking on a dimension.
- **Counter gap** (ledger `relevance` vs `culture.json`) is a **fixed** offset, unchanged from
  sessions 179-182: whimsical -173.14, poetic -96.80, formal -85.53, grounded -84.35,
  mythic -51.11, engineer -44.24, therapist -42.11, precise -32.63. `save_state()` rewrites
  `culture.json` with no lock, so `relevance_per_sim` is **not recomputable from the ledger**
  by an auditor.

## Leaderboard after the run

| rank | civ | relevance | rel/sim | sims | W/L | win rate | gen | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1932.01 | 1.528 | 1264 | 6/622 | 0.010 | 1 | 0.80 |
| 2 | civ-precise | 1780.81 | 1.419 | 1255 | 388/235 | 0.623 | 1 | 0.20 |
| 3 | civ-whimsical | 1681.73 | 1.323 | 1271 | 5/623 | 0.008 | 1 | 0.95 |
| 4 | civ-mythic | 1549.59 | 1.231 | 1259 | 10/612 | 0.016 | 1 | 0.85 |
| 5 | civ-formal | 1490.93 | 1.179 | 1265 | 96/530 | 0.153 | 1 | 0.30 |
| 6 | civ-engineer | 1422.20 | 1.134 | 1254 | 48/573 | 0.077 | 1 | 0.40 |
| 7 | civ-therapist | 1412.08 | 1.123 | 1257 | 11/614 | 0.018 | 1 | 0.60 |
| 8 | **civ-grounded** | **1255.45** | **0.982** | 1279 | 70/557 | 0.112 | 1 | 0.50 |

## Answer to the asked question

**Low-relevance civilization: `civ-grounded` (The Grounded)** — last of 8 on lifetime `avg_score`
(1.0135), `alignment` (1.0633), `quality` (0.3983), `relevance` (1255.45) and
`relevance_per_sim` (0.982), and last of 8 on this run's `avg_score` (0.5240). 57 consecutive
sessions (95-183) reproduce it. The binding constraint is **alignment**, not prose quality.
