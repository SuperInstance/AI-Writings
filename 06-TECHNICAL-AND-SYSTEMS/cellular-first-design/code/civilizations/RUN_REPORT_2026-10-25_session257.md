# Civ Orchestrator — Run Report, session 257 (2026-10-25)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Exit code:** 0 · **Run mode:** single batch (no `--loop`, so no extinction/birth pass)
**Baseline:** `0657c97` (session 256) · **Provider path:** **Control B mock** (z.ai credential gap,
**114th session**) + **live JEV** (`jev-1.14.0`)

---

## Result

The run completed and **every civilization's `simulations.jsonl` grew by exactly 10 rows**
(5 sims + 5 competition re-runs). `meta_log.jsonl` grew by exactly 5 (1018 -> **1023**).
**18 files** are modified in the civ tree (8 ledgers + 8 cultures + `meta_log.jsonl` +
`leaderboard.json`). **Pre-flight gate: 40/40 PASS. Run verification: 79/79 PASS, 0 failures.**

### Row deltas (verified by `ls -la` + `wc -l`, and by diffing against the pristine git blobs)

| civ | rows before | rows after | D | `simulations_run` D (git blob) | W+L D | Drelevance |
|---|---|---|---|---|---|---|
| civ-grounded | 2052 | 2062 | **+10** | 2009->2019 (+10) | +5 | +15.19 |
| civ-whimsical | 2064 | 2074 | **+10** | 2001->2011 (+10) | +5 | +15.17 |
| civ-formal | 2037 | 2047 | **+10** | 1995->2005 (+10) | +5 | +17.63 |
| civ-poetic | 2031 | 2041 | **+10** | 1994->2004 (+10) | +5 | +20.37 |
| civ-precise | 2001 | 2011 | **+10** | 1985->1995 (+10) | +5 | +20.11 |
| civ-mythic | 2009 | 2019 | **+10** | 1989->1999 (+10) | +5 | +15.21 |
| civ-therapist | 2004 | 2014 | **+10** | 1987->1997 (+10) | +5 | +12.65 |
| civ-engineer | 2006 | 2016 | **+10** | 1984->1994 (+10) | +5 | +16.69 |

`meta_log.jsonl`: 1018 -> **1023** (+5). `leaderboard.json` iso `20:05:45` -> **`20:13:31`**.

`ls -la` on the civ tree shows all 8 ledgers with mtime **20:13** (clone time was 20:12),
confirming the new rows are on disk at the bridged path.

> **CORRECTION to the session-256 note — `simulations_run` is +10, not +5.**
> Session 256 recorded that "`simulations_run` counts only the sim phase (5 per civ)". That is
> **wrong**, and it was carried forward into the session-256 gate. The code settles it:
> `civilization_orchestrator.py:252` submits `c.run_simulation(...)` **in the competition phase
> as well**, and line 206 (`self.sims_run += 1`) is inside `run_simulation` — so **both** phases
> increment the counter. The git history confirms it independently: across six consecutive
> sessions `civ-therapist` `sims_run` goes **1937 -> 1947 -> 1957 -> 1967 -> 1977 -> 1987**,
> i.e. exactly **+10 per session**, matching the ledger delta of +10, not +5.
> A gate asserting `sims_run == +5` therefore reports **8 false failures on a clean run** —
> which is precisely what this session's first verification pass did. The session-256 assertion
> "asserting `sims_run == rows_before + 10` produces 8 false failures" is also inverted: it is
> `+5` that is the false-failing expectation. **Fix the gate to `+10`, and read the baseline
> from the git blob** (the ledger row count and `sims_run` remain offset by 16-63 rows of
> accumulated competition history).

---

## Environment recovery

The workspace was **empty** apart from `.plugin-cache` — the prompt's path
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
(**18th consecutive occurrence**).

- Upstream owner: **`SuperInstance/AI-Writings`** — the `ai-writings/...` slug 404s (the GitHub
  API is case-insensitive). Located via paged `GET /user/repos?per_page=100` (5 pages, 500 rows)
  + name filter. `SuperInstance/AI-Writings` matched; the sibling `ai-writings-generation-plato`,
  `-medium-is-math`, `-vectorizer` did not.
- **NAS EDQUOT, 24th session.** The first `git clone` into `/workspace/repos/ai-writings` died
  mid-clone with `close error: Disk quota exceeded` on `.git/description`. `df` shows the
  workspace mount at **100% (600G/600G, 0 avail)** while the overlay root has **28G free** —
  the workspace is quota-limited, not size-limited, and `du` shows only ~2 KB of my own content.
  Cloned to **`/tmp/ai-writings`** (overlay, not NAS-backed) instead.
- **Bridge symlink** `/workspace/repos/ai-writings -> /tmp/ai-writings`; verified by
  `os.path.samefile()` -> **True**. The script's hardcoded `CIVS_DIR` then resolves correctly
  and writes to the real civ tree.
- `ZAI_TOKEN` absent from env and from all 8 sandbox secrets; z.ai returns **401**
  `token expired or incorrect` => endpoint healthy, credential absent (**114th session**).
- **JEV live**: a well-formed `questions` body returns **HTTP 200** with
  `{"model":"jev-1.14.0", "score":0.16, "confidence":0.87}`. The empty-`questions` probe returns
  **HTTP 422 `too_short`**, which also proves the token is accepted — the server rejects the
  payload shape *after* authenticating.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code — the token gate returns `None` first).
- `gh` not installed (**20th session**) — used `GET /user/repos` with `GITHUB_TOKEN`.
- `SSL_CERT_FILE` points at the gateway-anchor-only bundle, but JEV and z.ai both answered
  over TLS without error this session, so no bundle rebuild was needed (the 289-cert rebuild
  from the JEV probe sessions was not required here).
- Tool timeout 30 s < orchestrator run ~30 s => detached launch with stdout redirected
  **and** `< /dev/null`, then poll.

---

## Mock integrity

The RUNBOOK warns that a gate written against a wrong spec passes 40/40 on a mock that is
wrong for a large fraction of rows. The spec was **re-derived from the live ledger**, not
trusted from the RUNBOOK, and the committed `tools/mock_zai.py` matches it byte-for-byte:
`i = d[0] % 4`, `seed = h[(i*2)%8 : (i*2)%8+4]`, `color = h[8:12]`,
`figure = h[12:16]/h[16:20]/h[20:24]`, with geometry 38-char header + 162-char tail = 200
preview, then a 149-char continuation -> 349-char body.

**Pre-flight gate: 40/40 PASS** — 40/40 requests OK, 40/40 distinct previews, 40/40 distinct
seeds, 40/40 distinct seed-tuples, 8/8 civs with 5 distinct seeds each, 5/5 prompts with 8
distinct seeds each, every body exactly **349** chars (inside the 332-369 band), every preview
exactly 200 chars, and the 38+162=200 geometry holds on every body.

**Post-run:** all **80** new rows recompute exactly against the independently re-derived md5
spec — **0 mismatches**. **0** JEV errors, **0** fallback triples (`2.0/2.0/2.0`),
**0** non-numeric quality scores, **0** `EXC:`/tracebacks in the mock log.

**Arithmetic:** `dRelevance == sum(new rows' avg_score)` to **0.0000** residual on all 8;
`dSims == 10` and `dW + dL == 5` on all 8 (all diffed against the **pristine git blob**, not
against a re-read of the live file).

**Teardown:** mock pid 292 killed by exact argv match, **0** remaining processes, and the
port re-probed **closed** (`curl` exit **7**, `HTTP=000`). Never `pkill -f mock_zai` —
self-match, 2 prior occurrences.

---

## Low-relevance civilizations

**The leaderboard sorts by `relevance_per_sim`, NOT by `relevance` — the bottom order
DISAGREES.** Both are reported below.

| # | board order (rel/sim) | relevance | rel/sim | run `avg_score` | quality | novelty | alignment | W/L |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 3481.76 | 1.7374 | **2.0367** | 1.1880 | 2.4760 | 2.4460 | 6/992 |
| 2 | civ-precise | 3347.54 | 1.6780 | 2.0107 | 1.0390 | **2.2290** | **2.7640** | 716/277 |
| 3 | civ-formal | 2900.53 | 1.4466 | 1.7630 | 0.7770 | 2.2510 | 2.2610 | 122/874 |
| 4 | civ-whimsical | 2857.55 | 1.4210 | 1.5170 | 0.6710 | 2.4650 | 1.4150 | 5/993 |
| 5 | civ-mythic | 2817.81 | 1.4096 | 1.5213 | 0.7570 | 2.3890 | 1.4180 | 10/982 |
| 6 | civ-engineer | 2774.47 | 1.3914 | 1.6687 | 0.6870 | 2.2680 | 2.0510 | 59/932 |
| 7 | **civ-therapist** | **2457.65** | 1.2307 | **1.2653** | **0.4670** | 2.4520 | **0.8770** | 11/984 |
| 8 | **civ-grounded** | 2480.90 | **1.2288** | 1.5187 | 0.6240 | 2.2860 | 1.6460 | 75/922 |

**Lifetime order by raw relevance:** `civ-poetic` (3481.76) > `civ-precise` (3347.54) >
`civ-formal` (2900.53) > `civ-whimsical` (2857.55) > `civ-mythic` (2817.81) >
`civ-engineer` (2774.47) > `civ-grounded` (2480.90) > **`civ-therapist` (2457.65)**.

### The low-relevance set

**1. `civ-therapist` — the run low and the lifetime low.** Run `avg_score` **1.2653** (the
fleet minimum) and the **only** civilization with a genuine two-axis collapse: alignment
**0.8770** is the fleet floor and quality **0.4670** is *also* the fleet floor this session.
Lifetime relevance **2457.65** is the lowest of the 8, **23.25** below `civ-grounded`. This is
the **8th consecutive session** in which therapist has been the run low — the collapse is
persistent, not a one-off draw.

**2. `civ-grounded` — the board's last place, and one half of the ordering-flip pair.** Run `avg_score`
**1.5187** on quality **0.6240** (second-lowest) with alignment **1.6460** mid-pack — a
single-axis failure, not a two-axis one. Grounded has the **higher** raw relevance (2480.90)
than therapist (2457.65) but the **lower** `rel/sim` (1.2288 vs 1.2307) — so the board ranks
grounded **last** while the raw-relevance order ranks it second-from-last. *The two orderings
disagree in the bottom pair, for the 3rd consecutive session.*

**3. `civ-engineer` — the alignment floor of the mid-pack.** Alignment **2.0510** and quality
**0.6870** are both low, and its run `avg_score` **1.6687** is only 6th. On raw relevance it is
6th (2774.47) and on `rel/sim` it is **6th** (1.3914) — the two orderings **agree** for
engineer; only the bottom pair flips. Unlike session 256 (where engineer was the **novelty**
floor at 2.2030), novelty
this session is **2.2680**, which is mid-pack — so engineer's shape **changed**: novelty floor
last session -> mid-pack novelty and a general mid-low this session.

**THREE distinct low-relevance shapes:** therapist (quality **+** alignment floor, and now
also the *lowest* raw relevance), grounded (quality-only, board last), engineer (general
mid-low; was the novelty floor last session).

### Spread and top of the board

- Run `avg_score` spread **0.7713** (poetic 2.0367 -> therapist 1.2653).
- **Alignment spread 1.8870 = 2.4x** the avg spread — alignment, not quality, is the axis
  that separates this fleet.
- Quality spread **0.7210**; novelty spread **0.2470** (the tightest axis, and it narrowed
  from 0.2800 last session because precise's novelty fell to the floor while whimsical's rose).
- `civ-poetic` led the run's `avg_score` (**2.0367**) and holds lifetime relevance #1 and
  `rel/sim` #1 — on a **0.6%** win rate. `civ-precise` won **5/5** competitions (a clean
  sweep, **6th consecutive**) on a **72.1%** lifetime win rate.
- **JEV vs `avg_score` argmax agreement: 1/5 (20%)** — tied with session 256 for the
  **lowest in the recorded series** (session 255: 3/5 = 60%; session 253: 2/5 = 40%). All 4
  disagreements were **down-grades**: JEV picked `civ-precise` where the average favoured
  `civ-poetic`, by margins -0.0267 to -0.0700. The margin on the one agreement was exactly
  0.0000. Precise's alignment (**2.7640**, the fleet max) is what buys it the sweep.
- **No civ is near extinction** (threshold `relevance < -10`; the lowest is 2457.65, **246x**
  the floor). Registry **8**, `max_civs` **12**, all `generation = 1`.

---

## Carried-forward notes

- **The board-vs-raw-relevance disagreement is now 3 sessions running** (256, 257, and 255
  per its own note). **Only the bottom pair** (`civ-grounded` vs `civ-therapist`) flips; the
  top 6 are identical in both orderings this session (poetic, precise, formal, whimsical,
  mythic, engineer). So *a report that gives only one ordering is wrong about the tail.*
- **The `simulations_run` expectation is +10, not +5** (see the correction above). Any gate
  carrying the session-256 `+5` assertion will report 8 false failures on a clean run. This is
  the second gate-level correction in two sessions — check the gate against the code, not
  against the previous session's report.
- **The run-low civ has been `civ-therapist` for 8 consecutive sessions**, and it now holds
  *both* the quality floor (0.4670) and the alignment floor (0.8770). The persistent shape is
  a quality floor shared by the whole bottom of the fleet — not one civ's decay.
- **`civ-engineer`'s shape is not stable across sessions** (novelty floor in 256, general
  mid-low in 257) — do not attribute a single session's axis to it.
