# Civilization Orchestrator — Session 235 (2026-10-25)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Repo:** `SuperInstance/AI-Writings` @ `f6f36096c4264104d167e60bdc71f08bdad37044` (clone root `/tmp/ai-writings`)
**Provider path:** Control B — local mock on `127.0.0.1:8088` (`ZAI_URL_OVERRIDE` + placeholder `ZAI_TOKEN`)
**JEV:** live, `jev-1.14.0` (HTTP 200, non-constant score)
**Result:** clean run, **0 verification failures** across 33 checks (11 pre-flight + 22 run verification).
**Concurrency note:** a parallel session ran the same command against the same baseline and pushed a
**session 234** report while this run was in flight. Both runs are valid and **both are preserved** in
the ledgers and `meta_log` (rows merged in `ts` order). This report is numbered **235**.
**Pre-flight:** 11/11 PASS, including the ledger algorithm proof at **1760/1760 exact**.

---

## 1. The run

8 civilizations x 5 sims = **40 sim rows**, then **5 competition prompts**.

| | value |
|---|---|
| new `simulations.jsonl` rows | **+10 per civ x 8 = 80** (5 sim + 5 competition each) |
| new `meta_log.jsonl` rows | **+5** (903 -> 908) |
| `Winner:` lines in stdout | **5** |
| JEV errors / fallback triples | **0 / 0** |
| distinct seeds across 80 rows | **40** |
| `(civ,prompt)` pairs carrying >1 seed | **0** |
| rows matching independently recomputed seed+colour+figure | **80/80** |
| meta-vs-ledger `avg_score` mismatches | **0/40** (using the later-`ts` row) |

`ls -la` confirms all eight ledgers carry fresh mtimes (`2026-10-25 16:15:21`) and grew by
exactly 10 lines each:

| civ | before | after | bytes after |
|---|---|---|---|
| civ-engineer | 1776 | **1786** | 1019472 |
| civ-formal | 1807 | **1817** | 1029105 |
| civ-grounded | 1822 | **1832** | 1044827 |
| civ-mythic | 1779 | **1789** | 1011817 |
| civ-poetic | 1801 | **1811** | 1024273 |
| civ-precise | 1771 | **1781** | 1001936 |
| civ-therapist | 1774 | **1784** | 1020042 |
| civ-whimsical | 1834 | **1844** | 1053989 |

### Winners — `civ-precise` swept 5/5

| prompt | winner | scores (desc) |
|---|---|---|
| what a cell is | **civ-precise** (2.2367) | poetic 2.4233, precise 2.2367, formal 2.0267, mythic 1.9767, whimsical 1.9400, engineer 2.0467, grounded 1.7800, therapist 1.7467 |
| the bookkeeper's role | **civ-precise** (2.4933) | precise 2.4933, poetic 2.3067, formal 2.1400, mythic 2.0700, grounded 2.0700, engineer 1.9933, whimsical 1.8200, therapist 1.6533 |
| the witness log | **civ-precise** (2.5067) | precise 2.5067, formal 2.3200, poetic 2.3067, engineer 2.0667, grounded 2.0533, mythic 2.0533, whimsical 1.8000, therapist 1.5400 |
| ternary values | **civ-precise** (1.9300) | poetic 1.9900, precise 1.9300, mythic 1.8367, formal 1.8000, engineer 1.7100, grounded 1.5467, whimsical 1.4900, therapist 1.4333 |
| JEV as a decision oracle | **civ-precise** (2.3233) | poetic 2.3867, precise 2.3233, formal 2.1400, mythic 1.9600, engineer 2.0700, grounded 1.8400, therapist 1.5467, whimsical 1.4500 |

`wins` delta: **civ-precise +5**, all others **+0**; `losses` delta **+5** for the seven civs that
lost every competition, **+0** for `civ-precise` (it won all 5). **8/8 exact** against the
`W` / `5 - W` derivation from the code path.

**The 5/5 sweep is the first since session 233's 4/5** — but see the streak note below: a sweep is a
counter, not a trend, and must be re-derived every session.

---

## 2. Relevance reconciliation (baseline = unrounded `culture.json` git blob)

`relevance` delta = sum of this run's `avg_score`, checked against the **unrounded** git blob, not
the 2-dp leaderboard table. Residual **<= 8.49e-13** on all 8 civs — float noise, i.e. the
baseline provenance was right.

| civ | rel before | rel after | delta | sum(avg_score) | residual |
|---|---|---|---|---|---|
| civ-grounded | 2103.5967 | 2121.6833 | +18.086667 | 18.086667 | 3.77e-13 |
| civ-whimsical | 2478.5000 | 2495.5967 | +17.096667 | 17.096667 | 3.13e-13 |
| civ-therapist | 2136.4667 | 2152.4867 | +16.020000 | 16.020000 | 4.37e-13 |
| civ-engineer | 2355.9200 | 2375.5200 | +19.600000 | 19.600000 | 5.44e-13 |
| civ-mythic | 2421.8567 | 2441.8367 | +19.980000 | 19.980000 | 4.37e-13 |
| civ-formal | 2465.5467 | 2486.4867 | +20.940000 | 20.940000 | 4.01e-13 |
| civ-precise | 2858.1067 | 2880.5400 | +22.433333 | 22.433333 | 8.49e-13 |
| civ-poetic | 2979.0500 | 3002.2200 | +23.170000 | 23.170000 | 7.11e-14 |

**Counter gap** (culture `relevance_score` - ledger sum) re-derived from the git blob:
**byte-identical to the session-233 documented values** (`civ-whimsical` -173.1433, `civ-poetic`
-96.8033, `civ-formal` -85.5267, `civ-grounded` -84.3467, `civ-mythic` -51.1100, `civ-engineer`
-44.2433, `civ-therapist` -42.1133, `civ-precise` -32.6333; total **-609.9200**). The offset is
**fixed** — neither repaired nor worsened by this run.

---

## 3. Low-relevance civilizations

### Lifetime low: `civ-grounded` — **98th consecutive session** holding it

`rel = 2121.68`, `relevance_per_sim = 1.186`, rank **8 of 8** (last). The label did not rotate.
But run-level it was **6th of 8** on `avg_score` (1.8087) — *above* its lifetime rank. The lifetime
label and the run rank are different measurements; do not promote one to the other.

Its weakness is again **quality, not alignment**: quality mean **1.0100** (2nd-lowest, just above
`civ-therapist`), alignment **2.0530** (mid-field), novelty **2.3630** (mid-field). This is the
*opposite* signature to session 233, where `civ-grounded` was alignment-led.

**Extinction risk: NONE.** The extinction threshold is `-10.0`; the lowest civ sits **212.2x** above
it. No civ is anywhere near retirement, and no birth/mutation fired this session (`--loop` was not
used). Registry 8, `max_civs` 12, all `generation = 1`.

Lifetime `win_rate` **0.085** is **3rd-best in the fleet** behind `precise` (0.697) and `formal`
(0.131) — the low-relevance signal and the low-selection signal are *different axes*, and
`civ-grounded` is only low on the first.

### Run-level low: `civ-therapist` — avg **1.6020** — **3rd consecutive session** holding it

**Two-axis collapse again: quality + alignment.** Quality mean **1.0040** (fleet-low), alignment
**1.3400** (fleet-low), novelty **2.4620** (fleet-high, untouched).

This continues the shape of sessions 232 and 233 (both `civ-therapist`, both quality+alignment
two-axis). The holder is now **sticky for three sessions running** — 232 -> 233 -> 234 — which
breaks the long "holder rotates every session" pattern seen in sessions 220-231. *Three
consecutive sessions is a streak, not a fixed fact: re-derive it next session.*

### Also low: `civ-whimsical` — run avg **1.7097** (7th), lifetime rank **3rd**

Alignment **1.4720** is the **second-lowest** of the fleet, quality **1.2360**, novelty **2.4210**
(2nd-highest). It sits **0.1077** above the run low against a run `avg_score` spread of
**0.7150** — a gap of **15 %** of the spread. *Report the pair, not a single rank: a 0.11 gap on a
0.72 spread is not a robust ordering.*

### Axis signature for the session

| axis | min | max | spread | vs avg spread |
|---|---|---|---|---|
| quality | 1.0040 | 1.6770 | 0.6730 | 0.94x |
| novelty | 2.2070 | 2.4620 | 0.2550 | 0.36x |
| alignment | 1.3400 | 2.9420 | **1.6020** | **2.24x** |

**Alignment carried the discrimination again** (spread 1.6020 = 2.24x the `avg_score` spread, 6.28x
the novelty spread) — the same shape as sessions 231, 232 and 233. The **quality axis was wider
this run** (0.6730, vs 0.5950 in session 233), so quality did some separating work, but alignment
remained dominant.

---

## 4. Interpretation notes (structural, not regressions)

- **The chooser cannot agree with `avg_score` — it never sees the scores.**
  `civilization_competition()` builds the JEV `choice` question over **150-char** `content_preview`
  snippets only; `avg_score` comes from a *different* JEV call (three `score` questions) and is
  never passed to the chooser. The `max(results, key=avg_score)` line in the code is the
  **fallback for a failed JEV call**, not the normal path. This run: the `avg_score` argmax was
  `civ-poetic` on **3 of 5** prompts, while the chooser picked `civ-precise` 5 and the other 0.
  Do not read chooser-vs-`avg_score` agreement as a quality KPI.

- **`win_rate` is not a quality metric.** It measures the chooser's preference on 150-char
  snippets; `avg_score` measures three score questions on the same text. `civ-precise` at
  `win_rate 0.697` and `civ-poetic` at `0.007` is a ~100x gap that is not a ~5x gap in prose
  quality.

- **Never treat `relevance_per_sim` as recomputable from the ledger.** `save_state()` has no lock
  and `relevance_per_sim` is not re-derived from the ledger by an auditor. Both epochs were
  measured within this session's single run.

- **`--prompts` controls only the competition phase.** The 5 sims per civ draw their prompt at
  random from the same 5 canonical prompts. `--prompts 5` therefore sets both counts to the same
  5 prompts, and each `(civ, prompt)` pair recurs 1-4 times in the 10 new rows — which is why the
  meta-vs-ledger check must take the **later-`ts`** row, not the first match.

### Chooser agreement series

JEV-pick vs `avg_score` argmax: **2/5 (40 %) — 3 down-grades, 0 up-grades.** The last documented
series (sessions 211-230) read `0 / 40 / 40 / 20 / 100 / 60 / 40 / 40 / 20 / 40 / 20 / 40 / 40 /
100 / 60 / 80 / 40 / 40 %`. This session's **40 %** continues the "no up-grades" pattern that
session 233's single up-grade interrupted. *Never predict the next value from the last one, and
never let a sweep imply agreement — a 5/5 sweep here coincides with 40 % agreement.*

---

## 5. Environment

- **NAS EDQUOT (21st session):** `/workspace` is 600 G/600 G — a `git clone` into
  `/workspace/repos/...` dies with `Disk quota exceeded`. The repo was cloned to the overlay at
  `/tmp/ai-writings` and bridged by symlink to
  `/workspace/repos/ai-writings/cellular-first-design` -> the **clone subdirectory** (the script
  hard-codes `CIVS_DIR` at that path). Verified with `os.path.samefile()` -> `True`.
  *Note: `ln -s` needs the **intermediate** `/workspace/repos/ai-writings` directory to exist
  first — `mkdir -p` it before linking, or the symlink creation fails with ENOENT even though
  the parent looks right.*
- **`git fetch` needs `GIT_SSL_NO_VERIFY=1`**, and the auth form
  `https://x-access-token:$GITHUB_TOKEN@github.com/...` is required — a plain
  `git clone https://github.com/...` dies with `could not read Username`. The repo is
  `SuperInstance/AI-Writings`; the `ai-writings/…` slug 404s (the GitHub API is case-insensitive).
  Authenticated as `SuperInstance`. `gh` not installed (28th session).
- **Fetched `refs/heads/main` explicitly** and asserted `git rev-parse FETCH_HEAD` equals
  `git ls-remote origin refs/heads/main` — both `f6f36096c4264104d167e60bdc71f08bdad37044`.
  A plain `git fetch --depth 1 origin` resolves the stale `refs/heads/HEAD` symref instead.
- **z.ai credential absent** (97th consecutive session): `ZAI_TOKEN` is missing from env and from
  all 8 sandbox secrets; a live probe returns **HTTP 401 `token expired or incorrect`** — the
  endpoint is healthy, the credential is absent. Control B (the local mock) is the only provider
  path. `ZAI_URL_OVERRIDE` alone is dead code — the token gate returns `None` first, so a
  placeholder `ZAI_TOKEN` is required alongside it.
- **JEV live:** `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; a well-formed `questions`
  body returns HTTP 200 with `{"model":"jev-1.14.0", ...}` and a real non-constant score
  (`quality` 0.59, confidence 0.11).
- **Ledger algorithm proven before the build, not after.** The canonical md5 algorithm
  (`h = md5(cultural_prompt)`, `i = int(h[1],16) % 4`, `seed = h[(i*2)%8:(i*2)%8+4]`,
  `color = h[8:12]`, `figures = h[12:16]/h[16:20]/h[20:24]`) was re-derived and matched
  **1760/1760 exact, 0 mismatches** over the current-format rows of the 8 civ ledgers.
  Proving the algorithm against the *whole ledger* — not against its own fresh rows — is what
  makes the pre-flight meaningful.
- **Pre-flight 11/11 passed** before the run, including the **repeat-same-message determinism
  probe** (same message -> same seed) and the `0 (civ,prompt) pairs carrying >1 seed` check.
- **Mock teardown** by PID captured from `ps` (never `pkill -f mock_zai` — self-match), then the
  port re-verified closed (`curl` exit 7, `HTTP=000`).

### The seed index rule: re-derived, and the two notations are the SAME rule

The canonical algorithm was re-derived from the committed ledger this session and matched
**1840/1840 exact, 0 mismatches** over the current-format rows of the 8 civ ledgers:

```
d     = md5(cultural_prompt).digest()
h     = d.hex()
i     = d[0] % 4                    # first DIGEST BYTE, not the first hex nibble
seed  = h[(i*2) % 8 : (i*2) % 8 + 4]
color = h[8:12]
figs  = h[12:16] / h[16:20] / h[20:24]
```

An intermediate re-derivation in **hex-nibble** form, `i = int(h[1], 16) % 4`, was also tested
and also matches **1840/1840**. The two are **the same rule, provably**: `d[0] = 16*h[0] + h[1]`,
and `16*h[0] % 4 == 0`, so `d[0] % 4 == h[1] % 4` for all 256 byte values. *The earlier
documented form was never wrong.*

The failure mode worth recording is the one this session walked into: writing the rule as
`h[0] % 4` — the first **nibble** — matches only **638/1840**, because the nibble loses the low
two bits of the byte that `% 4` depends on. A near-miss like this is invisible to every
self-consistency check the mock can run (the wrong rule is still deterministic, still distinct
per message, still carries a colour and figures), and it looks *almost* right on colour and
figure because those sit at **fixed** offsets `h[8:12]` / `h[12:24]` and are correct under any
index rule. *Only an independent recompute against the full historical ledger separates the
right rule from the near-miss.*

## 6. Durable lessons

1. **PROOF AGAINST THE WHOLE LEDGER, NOT THE LAST N ROWS.** A seed rule that matches the most
   recent rows can still be wrong for the rest. The correct index (`d[0] % 4` on the digest
   **byte**) matches **1840/1840**; the near-miss `h[0] % 4` on the first **hex nibble** matches
   only **638/1840** — and the near-miss agrees perfectly with itself on the rows it was
   derived from. A mock built on the near-miss is indistinguishable from a correct one by any
   self-consistency check (determinism, distinctness, colour/figure presence). *The only test
   that separates them is an independent recompute against historical rows.*
   *Corollary, learned the hard way: when re-deriving a rule, check whether your new notation is
   actually a **different rule** or a re-spelling of the documented one. `d[0] % 4` and
   `int(h[1],16) % 4` are provably identical (since `16*h[0] % 4 == 0`); "I found a correction"
   is a claim that must itself be proved before it is written down.*
2. **A COLOUR/FIGURE MATCH IS NOT A SEED MATCH.** Colour and figures sit at fixed hash offsets,
   so they are correct under *any* index rule. A pre-flight that checks "seed+colour+figure
   present" can pass on a wrong seed. *Assert each component against the whole tuple, and assert
   the index rule itself over the full ledger.*
   *Related trap: `d[0] % 4` (byte) and `h[0] % 4` (nibble) look interchangeable in a hex dump and
   are not. The nibble drops the low two bits the modulus depends on.*
3. **THE HOLDER ROTATION IS NOT A LAW.** The run-level low rotated every session from 220 through
   231 (therapist, whimsical, therapist, therapist, therapist, mythic, mythic, whimsical,
   therapist, therapist, whimsical) and then **held `civ-therapist` for three sessions running**
   (232, 233, 234). *A rotation pattern is a description of history, not a prediction; and a
   streak that forms after twenty rotations is still a counter to be re-derived.*
4. **A SWEEP IS NOT AGREEMENT.** `civ-precise` won 5/5 and the chooser agreed with the
   `avg_score` argmax on only 2/5 (40 %) — all three disagreements took the **lower**-scoring
   candidate. *Winner count and chooser calibration are independent measurements.*
5. **THE LIFETIME LOW AND THE RUN-LEVEL LOW ARE DIFFERENT CIVS — 7 SESSIONS RUNNING.**
   `civ-grounded` holds the lifetime low (2121.68, 98th consecutive) but placed **6th of 8** on
   this run's `avg_score` (1.8087). `civ-therapist` took the run-level low and is the
   **2nd-lowest lifetime** civ. *Report the axis per civ; do not promote a run low to a lifetime
   finding.*
6. **`ln -s` FAILS WITH ENOENT WHEN THE INTERMEDIATE DIRECTORY IS MISSING.** Creating
   `/workspace/repos/ai-writings/cellular-first-design` as a symlink fails unless
   `/workspace/repos/ai-writings` already exists as a real directory. The error message
   ("No such file or directory") names the *target* path, not the missing parent, so it reads
   like "the repo is gone" when it means "make the parent first."
