# Civ Orchestrator — Run Report, session 256 (2026-10-25)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Exit code:** 0 · **Run mode:** single batch (no `--loop`, so no extinction/birth pass)
**Baseline:** `dd7042b` (session 255) · **Provider path:** **Control B mock** (z.ai credential gap,
**113th session**) + **live JEV** (`jev-1.14.0`)

---

## Result

The run completed and **every civilization's `simulations.jsonl` grew by exactly 10 rows**
(5 sims + 5 competition re-runs). `meta_log.jsonl` grew by exactly 5 (1013 -> **1018**).
**18 files** are modified in the civ tree (8 ledgers + 8 cultures + `meta_log.jsonl` +
`leaderboard.json`). **Pre-flight gate: 40/40 PASS. Run verification: 11/11 PASS, 0 failures.**

### Row deltas (verified by `ls -la` + `wc -l`, and by diffing against the pristine git blobs)

| civ | rows before | rows after | D | `simulations_run` D (git blob) | W+L D | Drelevance |
|---|---|---|---|---|---|---|
| civ-grounded | 2042 | 2052 | **+10** | 1999->2009 (+10) | +5 | +14.72 |
| civ-whimsical | 2054 | 2064 | **+10** | 1991->2001 (+10) | +5 | +15.61 |
| civ-formal | 2027 | 2037 | **+10** | 1985->1995 (+10) | +5 | +17.21 |
| civ-poetic | 2021 | 2031 | **+10** | 1984->1994 (+10) | +5 | +20.34 |
| civ-precise | 1991 | 2001 | **+10** | 1975->1985 (+10) | +5 | +19.77 |
| civ-mythic | 1999 | 2009 | **+10** | 1979->1989 (+10) | +5 | +15.56 |
| civ-therapist | 1994 | 2004 | **+10** | 1977->1987 (+10) | +5 | +13.05 |
| civ-engineer | 1996 | 2006 | **+10** | 1974->1984 (+10) | +5 | +16.93 |

`meta_log.jsonl`: 1013 -> **1018** (+5). `leaderboard.json` iso `19:53:08` -> **`20:05:45`**.

`ls -la` on the civ tree shows all 8 ledgers with mtime **20:05** (clone time was 20:03),
confirming the new rows are on disk at the bridged path.

> **Baseline source (per the session-157 correction).** `simulations_run` counts only the **sim
> phase** (5 per civ) while the ledger accumulates **both** phases (10 rows per civ); the two
> are offset by the whole competition history (16-63 rows). The `simulations_run` baseline was
> therefore read from the **git blob's `culture.json`**, not from the ledger row count. Asserting
> `sims_run == rows_before + 10` produces 8 false failures on a clean run.

---

## Environment recovery

The workspace was **empty** apart from `.plugin-cache` — the prompt's path
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
(**17th consecutive occurrence**).

- Upstream owner: **`SuperInstance/AI-Writings`** — the `ai-writings/...` slug 404s (the GitHub
  API is case-insensitive). Located via paged `GET /user/repos?per_page=100` + name filter.
- **SPARSE CLONE: 14 MB vs 3.7 GB** — `--filter=blob:none --no-checkout --depth 1 --branch main`
  + `sparse-checkout set cellular-first-design`. A full clone of this repo was already
  transferring at 3.7 GB in an earlier attempt; the sparse form finished in seconds.
- Cloned to `/tmp/aiw/aiw`; copying into `/workspace` fails with **`Disk quota exceeded`**
  (NAS EDQUOT, **23rd session**). Even a 1 KB `dd` lands a 0-byte file.
- Bridge symlink `/workspace/repos/ai-writings -> /tmp/aiw/aiw`; verified by
  `os.path.samefile()` -> **True**, and by `os.path.isfile()` on the script path.
- `ZAI_TOKEN` absent from env and from all 8 sandbox secrets; z.ai returns **401**
  `token expired or incorrect` => endpoint healthy, credential absent (**113th session**).
- **JEV live**: a well-formed `questions` body returns **HTTP 200** with
  `{"model":"jev-1.14.0", ...}`. The empty-`questions` probe returns **HTTP 422 `too_short`**,
  which also proves the token is accepted — the server rejects the payload shape *after*
  authenticating.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code — the token gate returns `None`
  first).
- `gh` not installed (**19th session**) — used `GET /user/repos` with `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~30 s => detached launch with stdout redirected
  **and** `< /dev/null`, then poll.

---

## Mock integrity — spec re-derived against the live ledger, not trusted from the RUNBOOK

The RUNBOOK warns that a gate written against a wrong spec passes 40/40 on a mock that is
wrong for a large fraction of rows. So the spec was **re-derived from the 3,520 mock rows
already in the ledger** before the mock was launched.

| spec | seed match | colour match | figure match |
|---|---|---|---|
| **`i = d[0] % 4`, `seed = h[(i*2)%8 : (i*2)%8+4]`** | **3520/3520** | **3520/3520** | **3520/3520** |
| `i = int(h[0],16) % 4` (the session-213 trap) | 1205/3520 | 3520/3520 | 3520/3520 |
| `seed = h[0:4]` | 804/3520 | 3520/3520 | 3520/3520 |

The RUNBOOK's corrected spec is **confirmed exact against the live ledger** on all three
fields. The committed `tools/mock_zai.py` matches it byte-for-byte.

**Pre-flight gate: 40/40 PASS** — 40/40 requests OK, 40/40 distinct previews, 40/40 distinct
seeds, 40/40 distinct seed-tuples, 8/8 civs with 5 distinct seeds each, 5/5 prompts with 8
distinct seeds each, every body exactly **349** chars (37-char header + 162-char tail + 149-char
continuation, inside the 332-369 band), every preview exactly 200 chars, and the
38+162=200 geometry holds on every body.

**Post-run:** all **80** new rows recompute exactly against the independently re-derived md5
spec — **0 mismatches**. **0** JEV errors, **0** fallback triples (`2.0/2.0/2.0`),
**0** non-numeric quality scores, **0** `EXC:`/tracebacks in the mock log. Confidence range
**0.373 - 0.647**.

**Arithmetic:** `dRelevance == sum(new rows' avg_score)` to **0.0000** residual on all 8;
`dSims == 10` and `dW + dL == 5` on all 8 (all diffed against the **pristine git blob**, not
against a re-read of the live file).

**Teardown:** mock pids killed by exact argv match (323/324), **0** remaining processes, and the
port re-probed **closed** (`curl` exit **7**, `HTTP=000`). Never `pkill -f mock_zai` —
self-match, 2 prior occurrences.

---

## Low-relevance civilizations

**The leaderboard sorts by `relevance_per_sim`, NOT by `relevance` — the bottom order
DISAGREES.** Both are reported below.

| # | board order (rel/sim) | relevance | rel/sim | run `avg_score` | quality | novelty | alignment | W/L |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-grounded | 2465.72 | 1.2270 | 1.4720 | **0.4870** | 2.3450 | 1.5840 | 75/917 |
| 2 | civ-whimsical | 2842.38 | 1.4200 | 1.5613 | 0.7640 | 2.4620 | 1.4580 | 5/988 |
| 3 | civ-formal | 2882.90 | 1.4450 | 1.7207 | 0.7220 | 2.2400 | 2.2000 | 122/869 |
| 4 | civ-poetic | 3461.39 | 1.7360 | **2.0337** | **1.1360** | **2.4830** | 2.4820 | 6/987 |
| 5 | civ-precise | 3327.43 | 1.6760 | 1.9770 | 0.9380 | 2.2780 | **2.7150** | 711/277 |
| 6 | civ-mythic | 2802.60 | 1.4090 | 1.5557 | 0.8010 | 2.3900 | 1.4760 | 10/977 |
| 7 | civ-therapist | 2445.00 | 1.2300 | **1.3053** | 0.6460 | 2.3650 | **0.9050** | 11/979 |
| 8 | **civ-engineer** | 2757.79 | 1.3900 | 1.6933 | 0.7760 | **2.2030** | 2.1010 | 59/927 |

**Lifetime order by raw relevance:** `civ-poetic` (3461.39) > `civ-precise` (3327.43) >
`civ-formal` (2882.90) > `civ-whimsical` (2842.38) > `civ-mythic` (2802.60) >
`civ-engineer` (2757.79) > `civ-grounded` (2465.72) > **`civ-therapist` (2445.00)**.

### The low-relevance set

**1. `civ-therapist` — the run low and the lifetime low.** Run `avg_score` **1.3053** (the
fleet minimum) and the **only** civilization with a genuine two-axis collapse: alignment
**0.9050** is the fleet floor and quality **0.6460** is second-lowest. Lifetime relevance
**2445.00** is the lowest of the 8, **20.72** below `civ-grounded`. This is the **7th
consecutive session** in which therapist has been the run low — the collapse is persistent, not
a one-off draw.

**2. `civ-grounded` — a quality-only collapse, and the board's last place.** Run `avg_score`
**1.4720** (second-lowest) on quality **0.4870**, the **fleet quality floor**; its alignment
(**1.5840**) is mid-pack, so this is a single-axis failure, not a two-axis one. Grounded has the
**higher** raw relevance (2465.72) than therapist (2445.00) but the **lower** `rel/sim`
(1.227 vs 1.230) — so the board ranks grounded **last** while the raw-relevance order ranks it
second-from-last. *The two orderings disagree in the bottom pair.*

**3. `civ-engineer` — the novelty floor.** Novelty **2.2030** is the fleet minimum while its
quality (**0.7760**) and alignment (**2.1010**) are both mid-pack. On raw relevance it is 6th
(2757.79), but on `rel/sim` it is **last** (1.3900) — and it sits **65.49 below** the
`civ-formal` -> `civ-whimsical` step (40.52) in the middle of the pack, so it is not merely a
tail effect.

**THREE distinct low-relevance shapes, not two:** therapist (quality **+** alignment floor),
grounded (quality only), engineer (**novelty** floor).

### Spread and top of the board

- Run `avg_score` spread **0.7283** (poetic 2.0337 -> therapist 1.3053).
- **Alignment spread 1.8100 = 2.48x** the avg spread — alignment, not quality, is the axis
  that separates this fleet.
- Quality spread **0.6490**; novelty spread **0.2800** (the tightest axis).
- `civ-poetic` led the run's `avg_score` (**2.0337**) and holds lifetime relevance #1 and
  `rel/sim` #1 — on a **0.6%** win rate. `civ-precise` won **5/5** competitions (a clean
  sweep, **5th consecutive**) on a **72.0%** lifetime win rate.
- **JEV vs `avg_score` argmax agreement: 1/5 (20%)** — the **lowest in the recorded series**
  (session 255: 3/5 = 60%; session 253: 2/5 = 40%). All 4 disagreements were **down-grades**:
  JEV picked `civ-precise` where the average favoured `civ-poetic`, by margins -0.0233 to
  -0.2067. The margin on the one agreement was exactly 0.0000.
- **No civ is near extinction** (threshold `relevance < -10`; the lowest is 2445.00, **244x**
  the floor). Registry **8**, `max_civs` **12**, all `generation = 1`.

---

## Carried-forward notes

- The **board-vs-raw-relevance disagreement is now 2 sessions running** (session 255 and
  session 256). The bottom pair (`civ-grounded` vs `civ-therapist`) flips between the two
  orderings, so *a report that gives only one of them is wrong half the time.*
- The **`simulations_run` vs ledger-row offset is large and uneven** (16-63 rows, varying per
  civ). It is the accumulated competition history, so it grows at a different rate per civ.
  Any future gate must read the `simulations_run` baseline from the git blob.
- The **run-low civ has been `civ-therapist` for 7 consecutive sessions** and the board has
  ranked `civ-grounded` last for 2. The persistent shape is a *quality floor* shared by the
  whole bottom of the fleet — not one civ's decay.
