# Civ Orchestrator — RUN REPORT session 183 (2026-10-25)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `f3fcb43` (session 182 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override is dead code behind the token gate). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe -> HTTP 200 with a real
score body, model `jev-1.14.0`).
**Run status:** all verification checks PASS (per-civ row deltas exact, 5/5 competitions,
0 JEV errors, mock non-degenerate 5/5, spec-recompute 80/80). **21/21 run-wide assertions PASS**,
**12/12 pre-flight checks PASS**.

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `/workspace` is 600 G/600 G, 0 bytes free; `git clone` **and** `cp` into `/workspace` fail with `Disk quota exceeded`; `/tmp` (overlay, 28 G free) is exempt |
| Clone target | `/tmp/aiw/AI-Writings` (sparse, `--filter=blob:none --depth 1`); the 3.7 GB upstream does not fit on the NAS mount |
| Working copy | `/opt/aiw/cellular-first-design` (overlay copy of the sparse checkout) |
| Bridge | `ln -s /opt/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; verified with `stat -L -c '%d:%i'` on both sides (identical `129:115`) **and** `os.path.samefile()` -> `True` |
| Upstream owner | `SuperInstance/AI-Writings` — the `ai-writings/cellular-first-design` slug 404s; resolved via `GET /search/code?q=civilization_orchestrator+in:path` (the GitHub API is case-insensitive) |
| `gh` | not installed (25th session) — used the REST API with `GITHUB_TOKEN` |
| Tool timeout | 30 s < run ~25 s wall — launched detached under `setsid nohup timeout -s KILL 300`, polled by PID (513) |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env and in all 8 sandbox secrets; the real endpoint returns 401 `token expired or incorrect` (endpoint healthy => credential gap, not an outage) |
| JEV | live — HTTP 200 with a scored body, model `jev-1.14.0`, `quality.score` 1.79 / confidence 0.51 |
| Mock teardown | killed **both** pids (wrapper 363 + server 365); `curl` exit 7 = port closed, `HTTP=000`; 0 tracebacks in the log |
| `git show` cwd | the **clone root** is `/tmp/aiw/AI-Writings`, not `/opt/aiw` (which is a plain copy, not a git root) — `git show` there returns empty stdout => `JSONDecodeError`. Caught by the verification script, not by the run. |

## Mock rebuild — the SEVEN fixes, all load-bearing

Rebuilt from scratch (the mock lives in `/tmp` and was wiped with the workspace):

```
d      = md5(cultural_prompt).digest()          # (b) the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                              # (f) MESSAGE-derived, NOT a counter
seed   = h[(i*2)%8:(i*2)%8+4]                  # (a)+(e) contiguous 4-char slice
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"   # (g) three STRING components, NOT a division
```

Plus: (c) `Connection: close` + `Content-Length`; (d) interpolate the seed placeholder.

**The two deviations that matter were applied before the run, not after:**

1. **Fix (g) — the figure is a string triple, not a division.** The spec's
   `figure = h[12:16] / h[16:20] / h[20:24]` is **pseudo-code**: read literally it divides two
   `str` values and raises `TypeError`, so the mock 500s on **every** request **while the socket
   stays open** — a port/200 liveness probe still looks healthy. Correct form:
   `f"{h[12:16]}/{h[16:20]}/{h[20:24]}"`.
2. **The seed slice is `h[(i*2)%8:(i*2)%8+4]`** — a *contiguous* 4-char slice. Concatenating two
   2-char slices is **not** the same value, so a row written under one algorithm will not
   reconcile against a recompute under the other. **Check the SLICE, not the render.**

## Pre-flight gate (12 checks) — 12/12 on the FIRST build

Built from the orchestrator's own cultural-prompt template, over the exact 8 civs x 5 prompts
= 40 real messages:

| # | Check | Result |
|---|---|---|
| 1 | 40/40 HTTP 200 | PASS |
| 2 | 40/40 distinct seeds | PASS (40) |
| 3 | 40/40 distinct previews | PASS (40) |
| 4 | 40/40 seeds match an independently recomputed md5 | PASS (0 mismatches) |
| 5 | 8/8 distinct seeds on every one of the 5 prompts | PASS |
| 6 | 8/8 distinct previews on every one of the 5 prompts | PASS |
| 7 | 0 literal `seed={}` | PASS |
| 8 | `[mock-zai` prefix on 40/40 | PASS |
| 9 | 0 `EXC:` / tracebacks in bodies | PASS |
| 10 | **repeat-same-message => identical seed AND preview (40 x 2)** | PASS (0 mismatches) |
| 11 | 0 `(civ,prompt)` pairs carrying >1 seed | PASS |
| 12 | body lengths stable (266) | PASS |

**Check 10 is the load-bearing one.** A pre-flight that only exercises *distinct* inputs cannot
certify a *determinism* property — a counter-derived index passes 40 distinct messages cleanly
while the real run is broken. Only a repeat-the-same-input probe can catch fix (f).

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
| rows matching spec-recomputed seed + color + figure | **80/80** | 80/80 (0 mismatches) | PASS |
| distinct seeds across the 80 new rows | 40 (8 civs x 5 prompts) | 40 | PASS |
| `(civ, prompt)` combos with >1 seed | 0 | 0 | PASS |
| distinct `(q,n,a)` triples | 80/80 | 80/80 | PASS |
| `relevance` delta == sum(`avg_score`), unrounded git baseline | **8/8 exact** | 8/8 (max resid 3.8e-13) | PASS |
| `wins`+`losses` delta | 5 per civ (40 total) | 5 per civ | PASS |
| `wins` delta == winner counts from `meta_log` | 8/8 | precise +4, formal +1 | PASS |
| meta-vs-ledger `avg_score` mismatches (later-`ts` row) | **0/40** | 0/40 | PASS |
| generations / registry | 8 civs, all `generation=1` | 8 civs, all gen 1, no birth/extinction | PASS |
| extinction | NONE | lowest raw relevance +1265.38 = **127x** the -10 floor | PASS |
| mock tracebacks | 0 | 0 | PASS |
| port closed after teardown | `curl` exit 7 | exit 7, `HTTP=000` | PASS |
| `leaderboard.json` rewritten | yes | 07:04:46Z | PASS |

**21/21 assertions PASS.**

### Per-civ line deltas and relevance deltas

| civ | before | after | delta | relevance delta |
|---|---|---|---|---|
| civ-grounded | 1312 | 1322 | +10 | +15.1733 |
| civ-whimsical | 1324 | 1334 | +10 | +17.9733 |
| civ-formal | 1297 | 1307 | +10 | +18.5733 |
| civ-poetic | 1291 | 1301 | +10 | +20.4300 |
| civ-precise | 1261 | 1271 | +10 | +22.1600 |
| civ-mythic | 1269 | 1279 | +10 | +15.7067 |
| civ-therapist | 1264 | 1274 | +10 | +14.1167 |
| civ-engineer | 1266 | 1276 | +10 | +16.4767 |

**Baseline taken from the git blob** (`git show HEAD:.../culture.json`, unrounded), never from
the leaderboard's 2-dp display value — otherwise the delta check carries phantom residuals of up
to +/-0.0067 per civ. The counter gap observed this session is exactly that rounding artefact:
+0.003333 for five civs, -0.003333 for `civ-mythic`, 0.000000 for two.

## Results

### Chooser vs `avg_score` argmax: 2/5 (40 %)

| prompt | winner | winner `avg_score` | argmax | argmax score | delta | |
|---|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 2.097 | `civ-precise` | 2.097 | +0.000 | match |
| the bookkeeper's role | `civ-precise` | 1.797 | `civ-poetic` | 1.907 | **-0.110** | disagree |
| the witness log | `civ-formal` | 2.257 | `civ-precise` | 2.557 | **-0.300** | disagree |
| ternary values | `civ-precise` | 2.090 | `civ-poetic` | 2.107 | **-0.017** | disagree |
| JEV as a decision oracle | `civ-precise` | 2.197 | `civ-precise` | 2.197 | +0.000 | match |

**All three disagreements took the LOWER-scoring candidate** — the same one-directional pattern
seen in sessions 179-182. The chooser is **not** a pure argmax, and `win_rate` is a
**selection** metric, not a quality metric.

**One new observation:** `civ-formal` took a win this session (4/5 sessions it won, on "the
witness log"), and it did so on a **2.257 vs 2.557** deficit — the widest chooser-argmax gap
(-0.300) observed in the series. The chooser's `choice` question sees 150-char `content_preview`
snippets and asks "which civilization serves this moment best"; `avg_score` is the mean of three
`score` questions over the same text. Different questions, and the "witness log" prompt is
precisely the one where a *measured, exact* voice reads as the right voice for the moment.

### `civ-grounded` (The Grounded) remains the low-relevance civ — 57th consecutive session

Last on lifetime `avg_score` (**1.0210**), `alignment` (**1.0719**), `quality` (**0.4031**),
`relevance` (**1265.38**) and `relevance_per_sim` (**0.989**).

| | Grounded | next civ | gap |
|---|---|---|---|
| `alignment` | 1.0719 | therapist 1.2052 | **0.1334** |
| `quality` | 0.4031 | therapist 0.4461 | 0.0430 |
| `avg_score` | 1.0210 | therapist 1.1478 | 0.1268 |

The alignment gap is **3.10x** wider than the quality gap. Alignment is the dimension the
meta-GAN **selects** on, so Grounded fails to *embody a distinctive voice*: a **voice** failure,
not a prose failure. Its tenets ("concrete images, everyday language, specific examples, no
abstractions") and voice ("warm, factual") are the least differentiating prompt in the field —
"warm, factual" is what a *good* default answer sounds like, and the meta-GAN rewards
embodiment of a specific voice, not the absence of an odd one.

Grounded was **NOT** the run-level low this session — it ranked **7th of 8** on this run's
`avg_score` (1.5173). The run-level low was `civ-therapist` (**1.4117**), last of 8, ahead of
`civ-grounded` (1.5173). This **reproduces the run-level-low rotation** that session 182 broke:
the run low and the lifetime low are again different civs on different axes.

### Other axes

- **`civ-therapist`** is the run-level low **and** the low-**alignment** axis — lifetime alignment
  **1.2052** (last), run alignment **1.0350** (last, and 2.87x below the run leader's 2.9060).
  Lifetime novelty 1.7921 is healthy (3rd). Its tenets ("empathy, presence, reflection, care")
  and voice ("warm, attentive") are *warm* like Grounded's but softer — the two warm-voice civs
  are the two lowest-alignment civs, which suggests warmth without a distinguishing *structure*
  is exactly what the alignment metric does not reward.
- **`civ-formal`** is the low-**novelty** axis — lifetime novelty **1.5060** (last), alignment
  1.6858 healthy. Lifetime `avg_score` 1.2153 (5th of 8).
- **`civ-poetic`** = 1st on lifetime `avg_score` (1.5686) / `quality` (0.7436) / `relevance`
  (1943.89) / `relevance_per_sim` (1.538) but **last on `win_rate` (0.010, 6/628)** — the stable
  selection-failure inverse.
- **`civ-precise`** = best `win_rate` (0.623, 388/235), 1st on lifetime `alignment` (2.1415),
  swept 4/5 — the mirror inverse.
- **Extinction risk: NONE** — threshold -10; lowest raw relevance +1265.38 (127x above the floor).
  Registry 8 civs, `max_civs` 12; birth/extinction only runs under `--loop`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` **1.8710**,
  `quality` 0.5140, `avg_score` 0.8043, novelty 0.1570. `alignment` again carried the widest
  spread and is again the axis the chooser selects on. **The quality level is a LEVEL that moves,
  not a stable property** — compare cross-civ spreads, not absolute levels, before ranking on a
  dimension. (Lifetime quality spread is 0.7440-0.4031 = 0.3409, roughly half this run's.)
- **Run `avg_score` levels sit above the lifetime band** (run leader 2.2160 vs lifetime leader
  1.5686) — the **ordering** carries the information, not the level.

## Leaderboard after the run

| rank | civ | relevance | rel/sim | sims | W/L | win rate | gen | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1943.89 | 1.538 | 1301 | 6/622 | 0.010 | 1 | 0.80 |
| 2 | civ-precise | 1793.24 | 1.429 | 1271 | 388/235 | 0.623 | 1 | 0.20 |
| 3 | civ-whimsical | 1692.72 | 1.332 | 1334 | 5/623 | 0.008 | 1 | 0.95 |
| 4 | civ-mythic | 1559.86 | 1.239 | 1279 | 10/612 | 0.016 | 1 | 0.85 |
| 5 | civ-formal | 1502.89 | 1.188 | 1307 | 96/530 | 0.153 | 1 | 0.30 |
| 6 | civ-engineer | 1433.11 | 1.143 | 1276 | 48/573 | 0.077 | 1 | 0.40 |
| 7 | civ-therapist | 1420.19 | 1.130 | 1274 | 11/614 | 0.018 | 1 | 0.60 |
| 8 | **civ-grounded** | **1265.38** | **0.989** | 1322 | 70/557 | 0.112 | 1 | 0.50 |

## Answer to the asked question

**Low-relevance civilization: `civ-grounded` (The Grounded)** — last of 8 on lifetime `avg_score`
(1.0210), `alignment` (1.0719), `quality` (0.4031), `relevance` (1265.38) and
`relevance_per_sim` (0.989). 57 consecutive sessions reproduce it. The binding constraint is
**alignment**, not prose quality: the alignment gap to the next civ is 3.10x the quality gap, and
alignment is the dimension the meta-GAN selects on.

**Second low-relevance civ: `civ-therapist` (The Therapist)** — the run-level low this session
(1.4117, last of 8) and last on both lifetime and run **alignment** (1.2052 / 1.0350). It is
*not* the lifetime low and must not be promoted to that finding.

Neither is at extinction risk: the lowest raw relevance is 127x the -10 floor, and the registry
is unchanged at 8 civs with all generations at 1.
