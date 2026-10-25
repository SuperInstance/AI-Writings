# Civilization Orchestrator — Run Report (Session 81, 2026-10-24)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

## 1. Headline

**The command as specified produced ZERO new rows.** The orchestrator exited **0**, printed
all 8 `[Name] running 5 sims...` lines, and wrote **no** `Winner:` lines and **no**
ledger rows. This is the **24th consecutive no-op**, and the cause is unchanged:
`ZAI_TOKEN` is absent, and the provider gate returns `None` before the URL is ever read.

Verified **in-process** (not inferred from logs):

| probe | result |
|---|---|
| `ZAI_TOKEN` in env | **absent** |
| `call_provider("zai", ...)` with empty token | returns `None` (gate fires) |
| `call_provider("zai", ...)` with dummy token, real z.ai URL | returns `None` — request **was attempted**, HTTP **401** |
| `jev_score(...)` | `{'quality': 0.16, 'novelty': 1.42, 'alignment': 0.70, 'confidence': 0.86}` — **live**, not the 2.0 default |
| all 7 sandbox secrets vs z.ai | **HTTP 401** `{"code":"401","message":"token expired or incorrect"}` |
| z.ai with **no** auth header | **HTTP 401** `{"code":"1001","message":"Authentication parameter not received in Header"}` |

The two different 401 bodies are the control: the endpoint is **live** and the URL path is
**right**, so this is a **credential gap**, not an outage and not a wrong path.

## 2. Verification the task asked for — `simulations.jsonl` new entries

**Unpatched run: NO new entries.** Byte-identical to the pre-run baseline on all 8 files.

```
civ-engineer    296 -> 296   delta= 0     civ-precise     291 -> 291   delta= 0
civ-formal      327 -> 327   delta= 0     civ-therapist   294 -> 294   delta= 0
civ-grounded    342 -> 342   delta= 0     civ-whimsical   354 -> 354   delta= 0
civ-mythic      299 -> 299   delta= 0     meta_log        163 -> 163   delta= 0
civ-poetic      321 -> 321   delta= 0     Winner: lines        0
```

`cmp` against the pre-run snapshot: **IDENTICAL on all 9 files**. Only `leaderboard.json`
changed (ts/iso only) — the board is rewritten unconditionally, so its mtime is not a
work receipt.

## 3. Control B — the pipeline is healthy end-to-end

To separate "no credential" from "broken pipeline", the provider was stubbed **at the gate**
(`ZAI_TOKEN` dummy + `ZAI_URL_OVERRIDE` → local mock; JEV left untouched):

| check | result |
|---|---|
| ledger delta | **+80 rows, +10 uniform on all 8 civs** (5 batch + 5 competition each) |
| `meta_log.jsonl` | **+5** |
| `Winner:` lines | **5** |
| mock calls | **80** (+1 pre-flight probe), **0 fallbacks** |
| boot assertion | **8/8** voices in pool (on the rendered `Your voice: {v}.` string) |
| all-2.0-default rows | **0** |
| JEV score errors | **0** (2 rows had `confidence: 0.0` on a *valid* score) |
| scaffolding leaks | **0** |
| providers | `{'zai': 80}` — zai only |
| distinct `avg_score` | **67/80**, range 1.307–2.760 |
| cross-key preview collisions | **0** |

**Restored afterwards:** all **20** files (8 `simulations.jsonl` + 8 `culture.json` +
`meta_log.jsonl` + `leaderboard.json` + `civilizations.json` + the script) verified
**byte-identical to the git blobs** (`git hash-object` vs `git rev-parse HEAD:<path>`),
`git status` clean, no `__pycache__/`. The mock server was stopped by PID and the port
re-probed (`000`).

## 4. Low-relevance civilizations — three lenses, never merged

The board's `relevance_per_sim` is not a quality ranking: it is a lifetime accumulation
over a lifetime denominator, it is not reproducible (the +260 counter gap), and it is
inverted against selection on all 8 positions. The lenses are reported separately.

### (a) Board sort key `relevance_per_sim` — lowest

| civ | rps | raw relevance | sims | wins | losses | win rate |
|---|---|---|---|---|---|---|
| **civ-grounded** | **1.474** | **440.81** | 299 | 35 | 102 | 0.245 |
| civ-formal | 1.649 | 470.03 | 285 | 21 | 115 | 0.154 |
| civ-engineer | 1.721 | 471.46 | 274 | 10 | 121 | 0.076 |

**`civ-grounded` is the lowest-relevance civilization on the board's own key and on raw
relevance**, and it ran the *most* sims (299) — so this is not a longevity artefact.

### (b) Win rate (selection appeal) — lowest

| civ | wins | losses | win rate |
|---|---|---|---|
| **civ-poetic** | **1** | **147** | **0.007** |
| civ-therapist | 2 | 143 | 0.014 |
| civ-whimsical | 3 | 145 | 0.020 |
| civ-mythic | 3 | 139 | 0.021 |

**`civ-poetic` is the selection failure**: 1st of 8 on the board's sort key (2.121), 1st on
raw relevance (602.48), 1st on lifetime mean `avg_score` (2.354) — and **1 win in 148**.
The chooser reads only 150 characters of preview; a dense lyrical register is filtered by
readability, not quality. 25 sessions running.

### (c) Actual writing quality (mock-filtered lifetime, n = 181–244 real rows per civ)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | **2.354** | **1.750** | 2.255 | **3.057** |
| civ-whimsical | 2.329 | 1.595 | **2.468** | 2.925 |
| civ-therapist | 2.120 | 1.377 | 2.161 | 2.821 |
| civ-mythic | 2.108 | 1.403 | 2.172 | 2.749 |
| civ-precise | 1.955 | 1.334 | **1.529** | 3.003 |
| civ-formal | 1.845 | 1.262 | **1.374** | 2.899 |
| civ-engineer | 1.827 | **1.190** | 1.602 | 2.690 |
| **civ-grounded** | **1.737** | 1.261 | 1.635 | **2.314** |

**`civ-grounded` is last of 8 on lifetime `avg_score` (1.737) and has the fleet's lowest
alignment (2.314, 0.376 below the next civ).** Combined with (a), it is the low-relevance
civilization on the durable lenses.

**`civ-precise` is the other inverse**: best win rate in the fleet (0.531, 76W/67L) but
**5th of 8** on lifetime `avg_score` and **7th of 8** on novelty (1.529).

### Extinction risk: none

`extinction_and_birth()` retires only below `relevance < -10`; the lowest is **+440.81**,
a **450.81-point** margin. It also only runs in `--loop` mode, every third iteration, so a
single-shot run never triggers it.

## 5. Structural replications

- **Chooser vs `argmax(avg_score)`: 0/5 this run** (margins −0.477 to −0.703, mean −0.603);
  lifetime **28/168 = 16.7 %**. **11th replication.** The competition and the scoring are
  two independent JEV calls, and the chooser never sees the scores. `win_rate` is a
  *selection* metric; a crown is a property of (civ, prose shown), not of the civ.
- **Temperature ↔ novelty: r = 0.9383** (12-replication band 0.9783–0.985; 0.9330 in
  session 80). The drop is **not** a model regression: the corpus is 36.9 % synthetic.
  `r(temp, quality) = 0.7305`, `r(temp, alignment) = 0.0976` — alignment is the only lens
  that measures culture rather than a knob the fleet already holds.
- **Counter gap: exactly +260** (ledger 2604 vs registry `simulations_run` 2344) —
  unchanged, and not on any single civ. `save_state()` rewrites `culture.json` from
  in-memory counters with no lock and no read-modify-write ⇒ lost-update race ⇒
  `relevance_per_sim` is **not recomputable by an auditor** from the ledger.
- **The committed ledger is 960/2604 = 36.9 % provider stand-in.** The mock-filter is no
  longer a no-op (session 77's clean baseline has been re-contaminated). Every lifetime
  number above is **mock-filtered** and states its n.

## 6. Standing answers (25 sessions)

- **Lowest relevance: `civ-grounded`** — last on 3 of 3 durable lenses (board sort key
  1.474, raw relevance 440.81, lifetime mock-filtered `avg_score` 1.737) plus the fleet's
  lowest alignment (2.314), while holding the **most** sims (299). Not a longevity
  artefact; it loses on the *mean*.
- **Selection failure: `civ-poetic`** — 1st of 8 on the board, on raw relevance, on
  lifetime `avg_score` and on lifetime quality, and **1 win in 148 (0.007)**.
- **Healthy: `civ-precise`** — 76W/67L (0.531), the only civ whose relevance rank and win
  rate agree.
- **Extinction risk: none** — threshold −10, lowest +440.81, a 450.81-point margin.
