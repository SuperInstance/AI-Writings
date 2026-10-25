# Civilization Orchestrator — Session 259 (2026-10-25)

- Command: `civilization_orchestrator.py --sims 5 --prompts 5 --providers zai` -> exit 0, ~31 s.
- Provider path: **Control B mock** (z.ai credential gap, **116th session**) + **live JEV** (`jev-1.14.0`).
- Baseline: `90299695` (session 258 tree). **Pre-flight gate: 40/40 PASS. Run verification: 111 checks / 0 FAIL.**
- Ledger delta: **+10 rows per civ, +80 total**; `meta_log` **1028 -> 1033** (+5); 18 files changed.

## Pre-flight / spec re-derivation

- Mock body **349** chars (38 header + 162 tail + 149 continuation), inside the 332-369 band.
- The spec was **re-derived from the live ledger** before launch (not trusted from the RUNBOOK):
  `i = d[0] % 4`, `seed = h[(i*2)%8:(i*2)%8+4]`, `color = h[8:12]`,
  `figure = h[12:16]/h[16:20]/h[20:24]`. Re-derivation against **all** recognizable
  historical rows across the 8 civs -> **4000/4000 exact**, 0 mismatches.
- Pre-flight: 40/40 requests 200 OK, 40/40 distinct previews, 40/40 distinct seeds,
  40/40 independently recomputed md5s, 38+162=200 geometry, 349-char band, 0 tracebacks.

## Run results

- Post-run: this run's 80 rows recompute **80/80** exact, 0 mismatches. 0 JEV errors,
  0 fallback triples, 0 non-numeric quality scores, confidence range **0.23 - 0.89**,
  **80/80** distinct score triples.
- `dRelevance == sum(new rows' avg_score)` to **0.0000** residual on all 8; `dSims == 10`,
  `dW + dL == 5` on all 8 — all diffed against the **pristine git blob**, not a re-read.
- All 8 `simulations.jsonl` are **append-only** vs the git blob (prefix byte-identical).

### Run-window averages (10 rows/civ)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | 1.9720 | 1.0950 | 2.4240 | 2.3970 |
| civ-precise | 1.9457 | 0.9190 | 2.2580 | 2.6600 |
| civ-formal | 1.7717 | 0.7900 | 2.2450 | 2.2800 |
| civ-engineer | 1.6867 | 0.6910 | 2.2960 | 2.0730 |
| civ-mythic | 1.6050 | 0.9210 | 2.3410 | 1.5530 |
| civ-whimsical | 1.5943 | 0.7270 | 2.5120 | 1.5440 |
| civ-grounded | 1.4947 | 0.5800 | 2.2710 | 1.6330 |
| **civ-therapist** | **1.2220** | **0.5210** | 2.3510 | **0.7940** |

- Winners: `civ-precise` **5/5** (a clean sweep, **8th consecutive**). Agreement with the
  `avg_score` argmax **1/5 (20 %)** — **4 down-grades, 0 up-grades**, margins -0.0433 to -0.1300.
  Tied with session 257 for the **lowest in the recorded series** (255: 60 %, 253/259: 40/20 %).
- Run spread `avg_score` **0.7500**; alignment spread **1.8660** = **2.5x** the avg spread.
  Quality spread 0.5740; novelty spread 0.2670 (tightest axis).
- `civ-poetic` led the run's `avg_score` (**1.9720**) and holds lifetime relevance #1 and
  `rel/sim` #1 on a **0.6 %** win rate; `civ-precise` sweeps on a **72.4 %** lifetime win rate.

## Low-relevance civilizations

**TWO low-relevance shapes this session:**

1. **`civ-therapist`** — the clear run-low. `avg_score` **1.2220** (last of 8), alignment
   **0.7940** at the **fleet floor** (and 2.6x below the next-lowest alignment, 1.5440),
   quality **0.5210** at the **fleet floor** (2nd consecutive session at a quality floor).
   Its novelty (**2.3510**) is **mid-pack**, so this is the **two-axis** shape
   (quality + alignment), not a general collapse. Its quality *rose* from 0.4670 (session 258)
   but alignment fell 0.8100 -> 0.7940, so the two-axis pattern **persists**.
   Smallest relevance gain of the fleet (**+12.22**) and lowest lifetime relevance (**2482.43**).
2. **`civ-grounded`** — quality **0.5800** (2nd-lowest, near the floor), novelty **2.2710**
   mid-pack, alignment **1.6330** mid-pack. It holds the **lowest `rel/sim` (1.2310)**, tied
   with therapist to 3 decimals, and the **2nd-lowest lifetime relevance (2511.01)**.
   Its shape is **quality-only**.

- Lifetime low `civ-therapist` (**2482.43**) vs `civ-grounded` (**2511.01**) — gap **28.58**.
- The **board-vs-raw-relevance tail flip is RESOLVED** this session: the `rel/sim` board order
  and the raw-relevance order are now **identical across all 8** (top 6 identical, tail pair
  `grounded` then `therapist` in both). This ends a **5-session run** of disagreement
  confined to the bottom pair — the flip was a near-tie artifact of `grounded`/`therapist`
  being separated by 25-29 relevance points on ~2000 sims of accumulation, not a real inversion.
- No civ near extinction (threshold `relevance < -10`; lowest **2482.43**, **248x** the floor).
  Registry 8, `max_civs` 12, all `generation=1`.

## Environment

- Workspace **empty** apart from `.plugin-cache` — the prompt's path did not exist
  (**20th consecutive occurrence**). Upstream **`SuperInstance/AI-Writings`**; the
  `ai-writings/...` slug 404s.
- **NAS EDQUOT, 26th session.** The first `git clone` into `/workspace/repos/ai-writings` died
  mid-clone with `close error: Disk quota exceeded` on `.git/description`. `df` shows the
  workspace mount at **100% (600G/600G, 0 avail)** while the overlay root has **28G free** —
  quota-limited, not size-limited. **Clone to `/tmp` (overlay), then bridge.**
- Bridge symlink `/workspace/repos/ai-writings -> /tmp/AIW`; verified by
  `os.path.samefile()` -> **True**. The script's hardcoded `CIVS_DIR` then resolves correctly.
- `ZAI_TOKEN` absent from env and from all sandbox secrets; z.ai returns **401**
  `token expired or incorrect` => endpoint healthy, credential absent (**116th session**).
- **JEV live**: a well-formed `questions` body returns **HTTP 200** with
  `{"model":"jev-1.14.0", "score":1.23, "confidence":0.43}`.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code — the token gate returns `None` first).
- `gh` not installed (**22nd session**) — used the REST API with `GITHUB_TOKEN`;
  located the upstream via `GET /search/code?q=civilization_orchestrator+in:path`.
- Tool timeout 30 s < orchestrator run ~31 s => detached launch with stdout redirected
  **and** `< /dev/null`, then poll. Python buffers stdout — the log looks empty mid-run.
- Teardown: mock pid 311 killed by **exact PID**, 0 remaining processes, port re-probed
  **closed** (`curl` exit **7**, `HTTP=000`). Never `pkill -f mock_zai` — self-match.

## GATE CORRECTION (carry this forward)

> **`distinct previews` must be asserted as 5 PER CIV, not 10.**
> The first verification pass this session asserted "all new previews distinct" (10 distinct
> bodies from 10 new rows) and produced **8 FALSE FAILURES** on a clean run. The code settles
> it: `CANON_PROMPTS[:args.prompts]` is **5 prompts**, the sim phase draws 5 and the
> competition phase draws the same 5, and `tools/mock_zai.py` is **deterministic per
> (civ, prompt)** — `build_body` hashes only the cultural prompt, so the same (civ, prompt)
> always yields a byte-identical body. Therefore 10 rows per civ MUST contain exactly
> **5 distinct previews**, and the diagnostic assertion that matters is
> **"no prompt maps to >1 preview"** (which is what proves determinism).
> **Third gate-level correction in three sessions: check the gate against the CODE,
> not against the previous session's report.**
