# Civ Orchestrator — RUN REPORT session 183 (2026-10-25)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `2bebbf9c` (session 182 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override is dead code behind the token gate). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe -> HTTP 200 with a real
score body, model `jev-1.14.0`).
**Run status:** all verification checks PASS (per-civ row deltas exact, 5/5 competitions,
0 JEV errors, mock non-degenerate, spec-recompute 80/80).

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `/workspace` is 600 G/600 G, 0 bytes free; `git clone` into `/workspace` fails with `Disk quota exceeded`; `/tmp` (overlay, 28 G free) is exempt |
| Clone target | `/tmp/repos/aiw` — `--filter=blob:none --no-checkout --depth=1` + `sparse-checkout set cellular-first-design` ⇒ **8.5 MB** working tree, **184 K** of git objects |
| Bridge | `ln -sfn /tmp/repos/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; verified by inode identity (**262550** on both sides) and `readlink -f` |
| Bridge quirk | `test -ef` is **unusable in this sandbox** — `bash: [: ...: binary operator expected`. Use inode identity / `readlink -f` instead. The bridge is sound; the *test* is broken, not the link |
| Prompt path | `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist at session start (**11th consecutive occurrence**) — the workspace held only `.plugin-cache` and `.skills` |
| Upstream owner | `SuperInstance/AI-Writings` — the `ai-writings/…` slug 404s; the GitHub API is case-insensitive |
| `gh` | not installed (25th session) — used the REST API with `GITHUB_TOKEN` |
| API rate limit | `GET /contents/...?per_page=100` returned **403** part-way through enumeration ⇒ fell back to the git protocol, which is both unlimited and the correct way to assert a file census |
| Tool timeout | 30 s < run ~30 s wall — launched detached under `setsid nohup timeout -s KILL 600`, polled by PID (585/587) |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env and in all 8 sandbox secrets; the real endpoint returns 401 `token expired or incorrect` (endpoint healthy ⇒ credential gap, not an outage) |
| JEV | live — HTTP 200 with a scored body, model `jev-1.14.0` |
| Mock teardown | killed **both** pids (wrapper 417 + server 419) by exact argv match; `curl` exit 7 = port closed, `HTTP=000`; 0 tracebacks in the log |

## Mock rebuild — the SEVEN fixes (session-181/182 spec), all load-bearing

Built to the canonical algorithm with **fix (g)** applied and the **seed slice as a contiguous
4 hex chars** (sessions 179/180/181/182):

```
d      = md5(cultural_prompt).digest()          # (b) the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                              # (f) MESSAGE-derived, NOT a counter
seed   = h[(i*2)%8:(i*2)%8+4]                  # (a)+(e) contiguous 4-char slice
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"   # (g) three STRING components, NOT a division
```

Plus: (c) `Connection: close` + `Content-Length`; (d) interpolate the seed placeholder.
Mock md5 `a301395ffff3748d33dea2b811a34212`.

**One deviation caught before the run, not after:** the older spec block still shows
`seed = h[(i*2)%8:...+2] + h[((i*2)+2)%8:...+2]` (two 2-char slices concatenated). That is
**not** the same value as the contiguous 4-char slice `h[(i*2)%8:(i*2)%8+4]`, so a row written
under one algorithm will not reconcile against a recompute under the other. **Check the SLICE,
not the render.** This session used the contiguous slice, per sessions 181/182.

**Pre-flight gate (11 checks) — passed 11/11 on the FIRST build**, with the 40 exact cultural
prompts rebuilt from the orchestrator's own template:
40/40 HTTP 200, 40/40 distinct seeds, 40/40 distinct previews, 40/40 seeds matching an
independently recomputed md5 (seed + colour + figure), 8/8 distinct seeds AND previews on every
one of the 5 prompts, 0 literal `seed={}`, 0 `EXC:`/tracebacks, 0 `(civ,prompt)` with >1 seed,
uniform body length (463), and the **repeat-same-message ⇒ identical seed AND preview** probe
(40 messages x 2) — the only check able to catch fix (f).

*Gate-authoring note:* the first gate build crashed with `IndexError` because the 40 messages
are built **civ-major** (all 5 prompts per civ) while the per-prompt aggregation indexed
**prompt-major** (`i*8+pi` instead of `i*5+pi`). The check order matters: the first four
assertions passed *before* the crash, so a partial gate is not a passing gate.

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
| `relevance` delta == sum(`avg_score`), unrounded git baseline | **8/8 exact** | 8/8 (residual <= 3.6e-13) | PASS |
| `simulations_run` delta | +10 per civ | +10 x 8 | PASS |
| `wins`+`losses` delta | +5 per civ (40 total) | +5 per civ | PASS |
| `generation` | still 1 | 8/8 | PASS |
| `leaderboard.json` rewritten | yes | `2026-10-25T07:34:54` | PASS |
| registry | 8 civs | 8 civs, no birth/extinction | PASS |
| mock tracebacks | 0 | 0 | PASS |
| port closed after teardown | `curl` exit 7 | exit 7, `HTTP=000` | PASS |
| extinction | NONE | lowest +1268.03 = **127x** the -10 floor | PASS |

**22/22 assertions PASS.**

### Per-civ line deltas

| civ | before | after | delta | relevance delta |
|---|---|---|---|---|
| civ-grounded | 1312 | 1322 | +10 | +17.8200 |
| civ-whimsical | 1324 | 1334 | +10 | +16.0133 |
| civ-formal | 1297 | 1307 | +10 | +16.6633 |
| civ-poetic | 1291 | 1301 | +10 | +19.8067 |
| civ-precise | 1261 | 1271 | +10 | +16.6167 |
| civ-mythic | 1269 | 1279 | +10 | +18.6200 |
| civ-therapist | 1264 | 1274 | +10 | +17.4567 |
| civ-engineer | 1266 | 1276 | +10 | +17.0233 |

**Baseline taken from the git blob** (`git show HEAD:.../culture.json`, unrounded), never from
the leaderboard's 2-dp display value — otherwise the delta check carries phantom residuals of
up to +/-0.0067 per civ.

## Results

### Chooser vs `avg_score` argmax: **0/5 (0 %)** — the worst in the series

| prompt | winner | winner `avg_score` | argmax | argmax score | delta | |
|---|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 2.0600 | `civ-poetic` | 2.2967 | **-0.2367** | disagree |
| the bookkeeper's role | `civ-precise` | 1.4800 | `civ-poetic` | 1.9933 | **-0.5133** | disagree |
| the witness log | `civ-formal` | 2.0600 | `civ-poetic` | 2.1633 | **-0.1033** | disagree |
| ternary values | `civ-precise` | 1.3000 | `civ-poetic` | 1.6933 | **-0.3933** | disagree |
| JEV as a decision oracle | `civ-precise` | 1.3500 | `civ-poetic` | 1.8267 | **-0.4767** | disagree |

`civ-poetic` was the argmax on **5/5** prompts and won **0/5**.

**All 5 disagreements took the LOWER-scoring candidate** — the fleet's stable direction, now
reproduced on a 5/5 sample, and the **first 0/5** in the clean-mock series
(0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125)
→ 1/5 (126) → 3/5 (127) → 2/5 (128) → 4/5 (130) → 1/5 (131) → 2/5 (132) → 2/5 (133) →
0/5 (134) → 4/5 (136) → 1/5 (137) → 1/5 (138) → … → 1/5 (160) → 1/5 (182) → **0/5 (183)**).
Twenty-plus five-sample points cannot pin a rate — report it as a sample, and keep the
**direction** as the finding. The largest gap this session, **-0.5133**, is below the
session-160 record (-0.8900) and the session-137 record (-0.683).

**Never treat `win_rate` as a quality metric.** `civ-poetic` is 1st on lifetime `avg_score` and
**last-but-one** on `win_rate`; `civ-precise` is the mirror inverse.

### Run-level scores (the 5 canonical sims per civ)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | **1.9667** | 1.2900 | 1.8540 | **2.7560** |
| civ-mythic | 1.9153 | 1.0540 | 2.1560 | 2.5360 |
| civ-grounded | 1.7573 | 0.8280 | 2.1200 | 2.3240 |
| civ-engineer | 1.7353 | 1.0160 | 2.0380 | 2.1520 |
| civ-precise | 1.7273 | 1.0380 | 2.0820 | 2.0620 |
| civ-whimsical | 1.6953 | **1.3440** | 2.0540 | 1.6880 |
| civ-therapist | 1.6807 | 0.7160 | **2.1900** | 2.1360 |
| civ-formal | **1.5847** | 0.7120 | 1.9940 | 2.0480 |

**Cross-civ spreads (rank on spread, never on absolute level):** `alignment` **1.0680** ›
`quality` 0.6320 › `avg_score` 0.3820 › `novelty` 0.3360. `alignment` again carried the widest
spread and is again the axis the meta-GAN selects on. The `quality` level is high this session
(field mean 0.9998) — the collapse seen in sessions 118–138 and 182 did **not** reproduce, which
is why the run ranks on **spreads** and not on the level.

**Correction to a figure carried in earlier reports:** the run-level field mean `quality` is
**0.9998** this session (0.99975), not the ~0.91 previously quoted. The `quality` **level** is a
moving quantity in this fleet and should be recomputed from the ledger every session rather than
carried forward.

## Low-relevance civilizations

### 5.1 `civ-grounded` (The Grounded) — the lifetime low, 57th consecutive session

Last of 8 on **every** lifetime axis: `avg_score` (**1.0230**), `alignment` (**1.0799**),
`quality` (**0.4042**), `relevance` (**1268.03**) and `relevance_per_sim` (**0.9914**).

| | Grounded | next civ | gap |
|---|---|---|---|
| `alignment` | 1.0799 | therapist 1.2146 | **0.1347** |
| `avg_score` | 1.0230 | therapist 1.1504 | **0.1274** |
| `relevance_per_sim` | 0.9914 | therapist 1.1325 | **0.1411** |
| `quality` | 0.4042 | therapist 0.4472 | 0.0430 |

The alignment gap is **3.13x** wider than the quality gap. Alignment is the dimension the
meta-GAN **selects** on, so Grounded fails to *embody a distinctive voice*: a **voice** failure,
not a prose failure. Its tenets ("concrete images, everyday language, specific examples, no
abstractions") and voice ("warm, factual") are the least differentiating prompt in the field.

**Grounded is NOT the run-level low this session** — it placed **3rd of 8** on run `avg_score`
(1.7573) and 3rd on run `alignment` (2.3240). The run-level low rotated to `civ-formal`
(1.5847, 8th of 8) and run-level alignment low to `civ-whimsical` (1.6880). This is **the rule,
not a contradiction**: the run ranking and the lifetime table are two separate claims. Sessions
179–181 also showed the run low rotating across three different civs; session 182 was the
exception where run-low and lifetime-low coincided, and **that coincidence did not reproduce**.

**Lifetime novelty is 1.5849 — 6th of 8, mid-field.** Grounded is therefore failing on
**alignment and quality**, not on novelty; the two-axis condition of sessions 143–150 persists.
(The lowest lifetime novelty belongs to `civ-formal`, 1.5022 — a *different* axis.)

**Extinction risk: NONE.** Threshold −10; lowest relevance 1268.03 = **127x** above the floor.
Registry 8, `max_civs` 12; all 8 still `generation=1`. Birth/extinction only runs under `--loop`.

### 5.2 `civ-formal` — the run-level low **and** the lifetime low-novelty axis

Run-level `avg_score` **1.5847** (8th of 8) and run-level `quality` **0.7120** (8th of 8).
Lifetime novelty **1.5022** (8th of 8) with lifetime alignment 1.6855 (3rd, healthy) — the
classic **low-novelty** axis, distinct from Grounded's voice axis. The run-level low rotated
onto it this session, but its lifetime standing is mid-field (`avg_score` 1.2139, 5th of 8;
`relevance_per_sim` 1.1865, 5th of 8).
⇒ **Watch axis, not a finding.** A per-run low is a watch axis; only a lifetime gap is a finding.

### 5.3 `civ-therapist` — the low-alignment axis, and Grounded's gap partner

Lifetime alignment **1.2146** (7th of 8, second-lowest — it is the civ that *defines* Grounded's
alignment gap); lifetime novelty 1.7895 (3rd, healthy); lifetime `avg_score` 1.1504 (7th of 8);
`relevance_per_sim` 1.1325 (7th of 8). Run-level: 7th of 8 on `avg_score` (1.6807), **6th** on
`alignment` (2.1360) — mid-field, not at the run bottom. The axis stays open; do not promote it
to a finding.

### 5.4 `civ-whimsical` — the run-level alignment low, lifetime novelist

Run-level alignment **1.6880** (8th of 8) and run-level `quality` **1.3440** (**1st** of 8) — the
only civ that leads on quality this session. Lifetime novelty **1.9669** (**1st** of 8, the
highest in the field) and lifetime `quality` 0.5778 (2nd). This is a **split**: a high-novelty,
high-quality voice that the chooser does not reward — the mirror image of the
selection-failure pattern below, on a different axis.

### 5.5 The two stable inverses

- **`civ-poetic`** — 1st on lifetime `avg_score` (**1.5681**), `quality` (**0.7455**), `relevance`
  (**1943.27**), `relevance_per_sim` (**1.5374**); **last-but-one** on `win_rate` (**0.0096**,
  6/628). Argmax on 5/5 prompts, winner on 0/5. The selection-failure inverse.
- **`civ-precise`** — best `win_rate` (**0.6228**, 388/623), **highest lifetime `alignment`
  (2.1342)**, won 4/5 this run. The mirror inverse.

### 5.6 Watch axis `civ-engineer` — the session-121 low did NOT repeat

7th of 8 on lifetime `avg_score` (1.1582) and 7th of 8 on lifetime `relevance_per_sim`
(1.1433), but on this run it was 4th of 8 on `avg_score` (1.7353) and 4th on `alignment`
(2.1520) — no longer near the bottom. Still 7th of 8 on lifetime `avg_score`, so the axis stays
open; **do not promote it to a finding**.

## Leaderboard after the run

| rank | civ | relevance | rel/sim | sims | W/L | win rate | gen | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1943.27 | 1.537 | 1264 | 6/622 | 0.010 | 1 | 0.80 |
| 2 | civ-precise | 1787.70 | 1.425 | 1255 | 388/235 | 0.623 | 1 | 0.20 |
| 3 | civ-whimsical | 1690.76 | 1.330 | 1271 | 5/623 | 0.008 | 1 | 0.95 |
| 4 | civ-mythic | 1562.77 | 1.241 | 1259 | 10/612 | 0.016 | 1 | 0.85 |
| 5 | civ-formal | 1500.98 | 1.187 | 1265 | 96/530 | 0.153 | 1 | 0.30 |
| 6 | civ-engineer | 1433.66 | 1.143 | 1254 | 48/573 | 0.077 | 1 | 0.40 |
| 7 | civ-therapist | 1423.53 | 1.133 | 1257 | 11/614 | 0.018 | 1 | 0.60 |
| 8 | **civ-grounded** | **1268.03** | **0.991** | 1279 | 70/557 | 0.112 | 1 | 0.50 |

## Answer to the asked question

**Low-relevance civilization: `civ-grounded` (The Grounded)** — last of 8 on lifetime
`avg_score` (1.0230), `alignment` (1.0799), `quality` (0.4042), `relevance` (1268.03) and
`relevance_per_sim` (0.9914). 57 consecutive sessions (95–183) reproduce it. The binding
constraint is **alignment**, not prose quality — a voice failure, not a prose failure.

**Two secondary readings, kept separate from the lifetime finding:**
- `civ-formal` is the **run-level** low (8th of 8 on run `avg_score` 1.5847 and run `quality`
  0.7120) and holds the lifetime **low-novelty** axis (1.5022) — a watch axis, not a finding.
- `civ-whimsical` is the **run-level alignment** low (1.6880) while leading the field on
  lifetime novelty (1.9669) and run quality (1.3440).

**Extinction risk: NONE for any civ** — the lowest raw relevance is 1268.03, **127x** above the
−10 floor; registry 8 of `max_civs` 12; all 8 remain `generation=1`.
