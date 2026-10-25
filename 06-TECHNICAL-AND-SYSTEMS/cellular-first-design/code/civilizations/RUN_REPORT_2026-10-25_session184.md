# Civ Orchestrator — RUN REPORT session 184 (2026-10-25)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

**Upstream:** `SuperInstance/AI-Writings` @ `de0662e` (session 183 baseline)

**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and** `ZAI_URL_OVERRIDE` both set). **JEV live** (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe -> HTTP 200 with a real score body, model `jev-1.14.0`).

**Run status:** all verification checks PASS (per-civ row deltas exact, 5/5 competitions, 0 JEV errors, mock non-degenerate, spec-recompute 80/80). **47/47 PASS.**

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `/workspace` is 600 G/600 G, 0 bytes free; a real `cp` of the repo into `/workspace` fails with `Disk quota exceeded`; `/tmp` (overlay, 28 G free) is exempt |
| Clone target | `/tmp/aiw` — `git clone --depth 1` of `SuperInstance/ai-writings` (the `ai-writings/…` slug 404s; the GitHub API is case-insensitive) |
| Bridge | `ln -sfn /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; verified by `readlink -f` (**the `test -ef` probe is unusable in this sandbox**) |
| Prompt path | `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist at session start (**12th consecutive occurrence**) — the workspace held only `.plugin-cache` |
| `gh` | not installed (26th session) — used the REST API with `GITHUB_TOKEN` |
| API rate limit | `GET /contents/` returned **403** ⇒ fell back to the git protocol, which is unlimited and the correct way to assert a file census |
| Tool timeout | 30 s < run ~30 s wall — launched detached under `setsid nohup timeout -s KILL 600`, polled by PID (422/424) |
| z.ai credential | **absent** — `ZAI_TOKEN` unset; the real endpoint returns 401 `token expired or incorrect` (endpoint healthy ⇒ credential gap, not an outage) |
| JEV | live — HTTP 200 with a scored body, model `jev-1.14.0` |
| Mock teardown | killed **both** pids (wrapper 249 + server 251) by exact argv match; `curl` exit 7 = port closed, `HTTP=000`; 0 tracebacks in the log |

## Mock rebuild — the SEVEN fixes, all load-bearing

```
d      = md5(cultural_prompt).digest()          # (b) the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                              # (f) MESSAGE-derived, NOT a counter
seed   = h[(i*2)%8:(i*2)%8+4]                  # (a)+(e) contiguous 4-char slice
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"   # (g) three STRING components, NOT a division
```

Plus: (c) `Connection: close` + `Content-Length`; (d) interpolate the seed placeholder.

**Pre-flight gate (11 checks) — passed 11/11 on the FIRST build**, with the 40 exact cultural prompts rebuilt from the orchestrator's own template: 40/40 HTTP 200, 40/40 distinct seeds, 40/40 distinct previews, 40/40 seeds matching an independently recomputed md5 (seed + colour + figure), 8/8 distinct seeds AND previews on every one of the 5 prompts, 0 literal `seed={}`, 0 `EXC:`/tracebacks, 0 `(civ,prompt)` with >1 seed, uniform body length (632), and the **repeat-same-message => identical seed AND preview** probe (40 messages x 2) — the only check able to catch fix (f).

## Verification — asserted on rows, not on exit code

| Check | Expected | Observed | |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | **+10 each** (5 sims + 5 competition sims) | +10 on all 8 | PASS |
| total new rows | 80 | 80 | PASS |
| `meta_log.jsonl` delta | **+5** | +5 (653 -> 658) | PASS |
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
| `relevance` delta == sum(`avg_score`), unrounded git baseline | **8/8 exact** | 8/8 (residual <= 4.6e-13) | PASS |
| `simulations_run` delta | +10 per civ | +10 x 8 | PASS |
| `wins`+`losses` delta | +5 per civ (40 total) | +5 per civ | PASS |
| `generation` | still 1 | 8/8 | PASS |
| `leaderboard.json` rewritten | yes | `2026-10-25T07:44:35` | PASS |
| registry | 8 civs | 8 civs, no birth/extinction | PASS |
| mock tracebacks | 0 | 0 | PASS |
| port closed after teardown | `curl` exit 7 | exit 7, `HTTP=000` | PASS |
| extinction | NONE | lowest +1283.29 = **128x** the -10 floor | PASS |

**22/22 content assertions PASS** (+25 per-civ sub-assertions = **47/47** overall).

### Per-civ line deltas

| civ | before | after | delta | relevance delta |
|---|---|---|---|---|
| civ-grounded | 1322 | 1332 | +10 | +15.2600 |
| civ-whimsical | 1334 | 1344 | +10 | +15.8167 |
| civ-formal | 1307 | 1317 | +10 | +17.8533 |
| civ-poetic | 1301 | 1311 | +10 | +19.2633 |
| civ-precise | 1271 | 1281 | +10 | +19.1300 |
| civ-mythic | 1279 | 1289 | +10 | +14.3133 |
| civ-therapist | 1274 | 1284 | +10 | +13.3833 |
| civ-engineer | 1276 | 1286 | +10 | +15.8833 |

## Results

### Chooser vs `avg_score` argmax: **3/5 (60 %)**

| prompt | winner | argmax | |
|---|---|---|---|
| ... | `civ-precise` | `civ-precise` | agree |
| ... | `civ-precise` | `civ-poetic` | **disagree** |
| ... | `civ-precise` | `civ-precise` | agree |
| ... | `civ-precise` | `civ-precise` | agree |
| ... | `civ-precise` | `civ-poetic` | **disagree** |

`civ-precise` swept **5/5** competitions. Both disagreements took the **lower**-scoring candidate. **Never treat `win_rate` as a quality metric** — it is a *selection* metric.

### Per-civ run metrics

| civ | run avg_score | alignment | quality | novelty | lifetime relevance | rel/sim | lifetime rank |
|---|---|---|---|---|---|---|---|
| civ-therapist | 1.3383 | 1.0250 | 0.3620 | 2.6280 | 1436.91 | 1.134 | 7/8 |
| civ-mythic | 1.4313 | 1.3440 | 0.5100 | 2.4400 | 1577.08 | 1.243 | 4/8 |
| civ-grounded | 1.5260 | 1.6500 | 0.3710 | 2.5570 | 1283.29 | 0.996 | 8/8 |
| civ-whimsical | 1.5817 | 1.6770 | 0.5130 | 2.5550 | 1706.58 | 1.332 | 3/8 |
| civ-engineer | 1.5883 | 1.7820 | 0.4590 | 2.5240 | 1449.54 | 1.147 | 6/8 |
| civ-formal | 1.7853 | 2.3230 | 0.4780 | 2.5550 | 1518.84 | 1.191 | 5/8 |
| civ-precise | 1.9130 | 2.5430 | 0.6620 | 2.5340 | 1806.83 | 1.428 | 2/8 |
| civ-poetic | 1.9263 | 2.4140 | 0.7820 | 2.5830 | 1962.53 | 1.54 | 1/8 |

Run spreads: `avg_score` 0.5880, `alignment` **1.5180** (widest), quality 0.4200, novelty 0.1880.

## Low-relevance civilizations

### `civ-grounded` — the LIFETIME low, 57th consecutive session

- Lifetime `relevance` **1283.29** (last of 8), `relevance_per_sim` **0.996**, `win_rate` 0.111 (w=70 l=562).
- Run `avg_score` **1.5260**, `alignment` **1.6500**, `quality` **0.3710**, `novelty` 2.5570 — novelty is 2nd of 8, so it is not a flatness problem.
- Its lifetime deficit is an **alignment** deficit, not a prose deficit: run alignment 1.6500 against the run-best 2.5430, while quality 0.3710 is mid-pack. **A voice failure, not a prose failure.**
- Lowest relevance **+1283.29 = 128x** the -10 extinction floor ⇒ no extinction risk.

### `civ-therapist` — the RUN-level low (rotated)

- Run `avg_score` **1.3383** (last of 8 this run), `alignment` **1.0250**, `quality` 0.3620, `novelty` 2.6280.
- Axis gaps vs the run-best: **alignment 1.5180** vs quality 0.4200 = **3.61x wider** ⇒ again a **voice** failure.
- The run-level low **ROTATED** to `civ-therapist` (5th different civ in 5 sessions) while its lifetime standing is 7th of 8. **Watch the axis, not the holder** (session-132 rule): the *holder* rotates, the *axis* (alignment) does not.

## Headline for the next session

- **THE MOCK IS STILL NOT ON DISK AT SESSION START** (12th consecutive wipe) — rebuild from the spec above; the seven fixes are unchanged and the **seed slice is the contiguous 4-char `h[(i*2)%8:(i*2)%8+4]`**, not the two-2-char slices the older spec block still shows. *Check the SLICE, not the render.*
- **THE NAS IS STILL 100% FULL (600 G/600 G).** A real copy into `/workspace` fails with `Disk quota exceeded`; the **symlink bridge** is the only thing that works. `test -ef` remains unusable — verify with `readlink -f`.
- **`civ-grounded` remains the low-relevance civ — 57th consecutive session.**
- **THE RUN-LEVEL LOW ROTATED** to `civ-therapist` — a 5th different civ in 5 sessions. **Do not code against the rotation.**
- **Chooser vs `avg_score` argmax: 3/5 (60 %)** — `civ-precise` swept 5/5; both disagreements took the **lower**-scoring candidate.
