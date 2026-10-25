# Civ Orchestrator — RUN REPORT session 184 (2026-10-25)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `2421429` (session 183 baseline, branch `session/civ-orch-183`)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set). **JEV live** (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`;
probe -> HTTP 200 with a real score body, model `jev-1.14.0`).
**Run status:** all verification checks PASS (per-civ row deltas exact, 5/5 competitions,
0 JEV errors, mock non-degenerate, spec-recompute 80/80). **25/25 PASS.**

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `/workspace` is 600 G/600 G, 0 bytes free; `git clone` into `/workspace` fails with `Disk quota exceeded`; **even a 200-byte write fails**; `/tmp` (overlay, 28 G free) is exempt |
| Clone target | `/tmp/work/ai-writings` (full clone of branch `session/civ-orch-183`, `--depth 1`) — 8.6 MB working tree, the 3.7 GB upstream does not fit on the NAS mount |
| Bridge | `ln -sfn /tmp/work/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; verified with `[ -ef ]` -> `EF_OK` |
| Upstream owner | `SuperInstance/AI-Writings` — the `ai-writings/cellular-first-design` slug 404s; `cellular-first-design` is a **subdirectory**, not a repo of its own |
| `gh` | not installed — git protocol + web search used to resolve the owner |
| GitHub REST API | **rate-limited to 0/5000** at session start (reset epoch 1792913189). The git protocol is unaffected — use `git ls-remote` for existence probes, never a rate-limited REST call for an absence claim |
| Tool timeout | 30 s < run ~27 s wall — launched detached under `setsid nohup timeout -s KILL 300`, polled by PID (906) |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env and in all 8 sandbox secrets; the real endpoint returns 401. Control B (the local mock) is the only provider path. `ZAI_URL_OVERRIDE` alone is dead code — the token gate returns `None` first, so a placeholder token is required |
| JEV | live — HTTP 200 with a scored body, model `jev-1.14.0` |
| Mock teardown | killed **both** pids (715 + 717); `curl -m 5` => **exit 7**, `HTTP=000`; 0 tracebacks in the log |
| **NEW** | `origin/master` does **not** carry the `ZAI_URL_OVERRIDE` hook; only the `civ-orch/*` branches do. Running from `master` leaves the override as dead code |

## Mock rebuild — the SEVEN fixes, with the session-179+ contiguous-slice correction

```
d      = md5(cultural_prompt).digest()          # (b) the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                              # (f) MESSAGE-derived, NOT a counter
seed   = h[(i*2)%8:(i*2)%8+4]                  # (a)+(e) contiguous 4-char slice
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"   # (g) three STRING components, NOT a division
```

Plus: (c) `Connection: close` + `Content-Length`; (d) interpolate the seed placeholder.

**Pre-flight gate (12 checks) — 12/12 PASS on the FIRST build**, with the 40 exact
cultural prompts rebuilt from the orchestrator's own template: 40/40 HTTP 200, 40/40
distinct seeds, 40/40 distinct previews, 40/40 seeds matching an independently
recomputed md5 (seed + colour + figure), 8/8 distinct seeds AND previews on every one
of the 5 prompts, 0 literal `seed={}`, 0 `(civ,prompt)` with >1 seed, body length 222,
0 tracebacks, the **repeat-same-message => identical seed AND preview** probe (40 x 2)
that is the only check able to catch fix (f), and 40/40 previews carrying their own civ name.

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
| `relevance` delta == sum(`avg_score`), unrounded git baseline | **8/8 exact** | 8/8 (residuals <= 6.3e-13) | PASS |
| `wins`+`losses` delta | 5 per civ (40 total) | 5 per civ | PASS |
| `culture.json` `simulations_run` delta | +10 for 8/8 | 8/8 | PASS |
| registry | 8 civs, all `generation=1` | 8 civs, all gen 1, no birth/extinction | PASS |
| extinction | NONE | lowest +1263.27 = **126x** the -10 floor | PASS |
| `leaderboard.json` rewritten | yes | 2026-10-25T07:30:58 | PASS |
| no new civ dirs | 8 | 8 | PASS |
| mock tracebacks | 0 | 0 | PASS |
| JEV live (scores vary, not a constant fallback) | yes | 80/80 distinct triples | PASS |
| `meta_log` +5 rows carry `winner_civ` and `results` | 5 | 5 | PASS |
| each competition row has 8 civ results | 8 | 8 | PASS |
| all new rows have non-empty preview + `avg_score` | 80 | 80 | PASS |
| port closed after teardown | `curl` exit 7 | exit 7, `HTTP=000` | PASS |

**25/25 assertions PASS.**

### Per-civ line deltas

| civ | before | after | delta | relevance delta |
|---|---|---|---|---|
| civ-grounded | 1322 | 1332 | +10 | +7.8167 |
| civ-whimsical | 1334 | 1344 | +10 | +11.3567 |
| civ-formal | 1307 | 1317 | +10 | +9.7067 |
| civ-poetic | 1301 | 1311 | +10 | +9.9167 |
| civ-precise | 1271 | 1281 | +10 | +8.7867 |
| civ-mythic | 1279 | 1289 | +10 | +8.5267 |
| civ-therapist | 1274 | 1284 | +10 | +10.0233 |
| civ-engineer | 1276 | 1286 | +10 | +6.8067 |

**Baseline taken from the git blob** (`git show HEAD:.../culture.json`, unrounded), never from
the leaderboard's 2-dp display value — otherwise the delta check carries phantom residuals of
up to +/-0.0067 per civ.

## Results

### Chooser vs `avg_score` argmax: 0/5 (0 %) — `civ-precise` swept 5/5 again

| prompt | winner | winner `avg_score` | argmax | argmax score | delta | |
|---|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 0.673 | `civ-whimsical` | 1.117 | **-0.443** | disagree |
| the bookkeeper's role | `civ-precise` | 0.993 | `civ-whimsical` | 1.117 | **-0.123** | disagree |
| the witness log | `civ-precise` | 1.210 | `civ-whimsical` | 1.277 | **-0.067** | disagree |
| ternary values | `civ-precise` | 0.807 | `civ-whimsical` | 1.093 | **-0.287** | disagree |
| JEV as a decision oracle | `civ-precise` | 0.840 | `civ-whimsical` | 1.117 | **-0.277** | disagree |

**All five disagreements took the LOWER-scoring candidate** — the one-directional pattern seen in
sessions 179-182 continues, and the magnitude is the widest yet (**-0.443**). The chooser is
**not** a pure argmax, and `win_rate` is a **selection** metric, not a quality metric.

### `civ-grounded` (The Grounded) remains the low-relevance civ — 58th consecutive session

Last of 8 on lifetime `avg_score` (**1.0117**), `alignment` (**1.0614**), `quality` (**0.3963**),
`relevance` (**1263.27**) and `relevance_per_sim` (**0.980**).

| | Grounded | next civ | gap |
|---|---|---|---|
| `alignment` | 1.0614 | precise 2.1195 | **1.0581** |
| `quality` | 0.3963 | poetic 0.7326 | 0.3364 |
| `avg_score` | 1.0117 | poetic 1.5551 | 0.5434 |

The alignment gap is **3.15x** wider than the quality gap — the same structural ratio seen in
sessions 182 (**3.16x**) and 183 (**3.16x**). Alignment is the dimension the meta-GAN **selects**
on, so Grounded fails to *embody a distinctive voice*: a **voice** failure, not a prose failure.
Its tenets ("concrete images, everyday language, specific examples, no abstractions") and voice
("warm, factual") remain the least differentiating prompt in the field.

### The run-level low ROTATED to `civ-engineer` — a sixth civ in six sessions

Run-level `avg_score`: `civ-engineer` **0.6807** (low), `civ-grounded` 0.7817, `civ-mythic`
0.8527, `civ-precise` 0.8787, `civ-formal` 0.9707, `civ-poetic` 0.9917, `civ-therapist`
1.0023, `civ-whimsical` 1.1357 (high).

`civ-engineer` is the run low on `avg_score` **and** on `alignment` (**0.7120**) and `quality`
(**0.0700**), while its lifetime standing is 6th of 8. Sessions 179-183 each produced a
different run-level low; this session's low (`civ-engineer`) has been the run low before
(session 181). **Watch the axis, not the finding** (session-132 rule) — the *holder* rotates,
the *axis* does not. Do not code against the rotation.

### Other axes

- **`civ-formal`** is the low-**novelty** axis — lifetime novelty **1.4964** (last), alignment
  1.6708 healthy.
- **`civ-poetic`** = 1st on lifetime `avg_score` (1.5551) / `quality` (0.7326) / `relevance`
  (1941.93) / `relevance_per_sim` (1.524) but **last on `win_rate` (0.009, 6/633)** — the stable
  selection-failure inverse.
- **`civ-precise`** = best `win_rate` (0.626, 393/235), swept 5/5, 1st on lifetime `alignment`
  (2.1195) — the mirror inverse.
- **Extinction risk: NONE** — threshold -10; lowest raw relevance +1263.27 (126x above the floor).
  Registry 8 civs, `max_civs` 12; birth/extinction only runs under `--loop`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** novelty **0.7390**
  (widest), alignment 0.6650, `avg_score` 0.4550, quality 0.1600. **Novelty carried the widest
  spread this session** — alignment did, in sessions 182-183. The quality collapse remains a
  LEVEL that moves, not a stable property: compare cross-civ spreads, not absolute levels.
- **Counter gap** (ledger `relevance` vs the leaderboard's rounded display) is a **fixed**
  offset, unchanged from sessions 179-183: the per-civ deltas are **0.000000** for all 8 civs.
  `save_state()` rewrites `culture.json` with no lock, so `relevance_per_sim` is **not
  recomputable from the ledger** by an auditor.

## Leaderboard after the run

| rank | civ | relevance | rel/sim | sims | W/L | win rate | gen | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1941.93 | 1.524 | 1274 | 6/627 | 0.009 | 1 | 0.80 |
| 2 | civ-precise | 1789.60 | 1.415 | 1265 | 393/235 | 0.626 | 1 | 0.20 |
| 3 | civ-whimsical | 1693.09 | 1.322 | 1281 | 5/628 | 0.008 | 1 | 0.95 |
| 4 | civ-mythic | 1558.12 | 1.228 | 1269 | 10/617 | 0.016 | 1 | 0.85 |
| 5 | civ-formal | 1500.63 | 1.177 | 1275 | 96/535 | 0.152 | 1 | 0.30 |
| 6 | civ-engineer | 1429.01 | 1.131 | 1264 | 48/578 | 0.077 | 1 | 0.40 |
| 7 | civ-therapist | 1422.10 | 1.122 | 1267 | 11/619 | 0.017 | 1 | 0.60 |
| 8 | **civ-grounded** | **1263.27** | **0.980** | 1289 | 70/562 | 0.111 | 1 | 0.50 |

## Answer to the asked question

**Low-relevance civilization: `civ-grounded` (The Grounded)** — last of 8 on lifetime `avg_score`
(1.0117), `alignment` (1.0614), `quality` (0.3963), `relevance` (1263.27) and
`relevance_per_sim` (0.980). 58 consecutive sessions (95-184) reproduce it. The binding
constraint is **alignment**, not prose quality: the alignment gap to the next civ (1.0581) is
**3.15x** wider than the quality gap (0.3364).

The **run-level** low was a different civ — `civ-engineer` (0.6807) — for the sixth session in a
row, which is the run-level rotation, not the structural finding.
