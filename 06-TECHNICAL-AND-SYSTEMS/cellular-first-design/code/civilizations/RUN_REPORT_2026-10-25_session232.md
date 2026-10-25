# Civilization Orchestrator — Session 232 (2026-10-25)

**Command:** `python3 .../civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Repo:** `SuperInstance/AI-Writings` @ `1ef2f7ab` (clone root `/tmp/work/ai-writings`)
**Provider path:** Control B — local mock on `127.0.0.1:8088` (`ZAI_URL_OVERRIDE` + placeholder `ZAI_TOKEN`)
**JEV:** live, `jev-1.14.0` (HTTP 200)
**Result:** clean run, **0 verification failures** across 26 checks.

---

## 1. The run

8 civilizations x 5 sims = **40 sim rows**, then **5 competition prompts**.

| | value |
|---|---|
| new `simulations.jsonl` rows | **+10 per civ x 8 = 80** (5 sim + 5 competition each) |
| new `meta_log.jsonl` rows | **+5** (893 -> 898) |
| `Winner:` lines in stdout | **5** |
| JEV errors / fallback triples | **0 / 0** |
| distinct seeds across 80 rows | **40** |
| `(civ,prompt)` pairs carrying >1 seed | **0** |
| rows matching independently recomputed message md5 | **80/80** |
| meta-vs-ledger `avg_score` mismatches | **0/40** (using the later-`ts` row) |

### Winners — `civ-precise` swept all 5

| prompt | winner | scores |
|---|---|---|
| what a cell is | **civ-precise** (2.26) | whimsical 1.68, therapist 1.41, grounded 1.66, mythic 1.83 |
| the bookkeeper's role | **civ-precise** (2.17) | therapist 1.60, whimsical 1.68, grounded 1.85 |
| the witness log | **civ-precise** (2.52) | therapist 1.31, whimsical 1.97, grounded 1.99 |
| ternary values | **civ-precise** (2.37) | therapist 1.55, whimsical 1.82, grounded 2.00 |
| JEV as a decision oracle | **civ-precise** (2.47) | therapist 1.40, whimsical 1.72, grounded 1.70 |

`wins` delta: **civ-precise +5**, all others **+0**; `losses` delta **+5** for the seven losers. **8/8 exact.**

---

## 2. Relevance reconciliation (baseline = unrounded `culture.json` git blob)

`relevance` delta = sum of this run's `avg_score`, checked against the **unrounded** git blob, not the
2-dp leaderboard table. Residual **<= 9.09e-13** on all 8 civs — float noise, i.e. the baseline
provenance was right.

| civ | rel before | rel after | delta | sum(avg_score) | residual |
|---|---|---|---|---|---|
| civ-precise | 2814.1100000000038 | 2838.1200000000038 | +24.010000 | 24.010000 | 0.00e+00 |
| civ-poetic | 2934.043333333336 | 2957.866666666669 | +23.823333 | 23.823333 | 4.55e-13 |
| civ-formal | 2424.4800000000014 | 2447.5200000000013 | +23.040000 | 23.040000 | 4.55e-13 |
| civ-engineer | 2317.013333333338 | 2338.7066666666714 | +21.693333 | 21.693333 | 4.55e-13 |
| civ-mythic | 2383.326666666667 | 2404.2866666666667 | +20.960000 | 20.960000 | 9.09e-13 |
| civ-whimsical | 2446.7333333333368 | 2464.6433333333367 | +17.910000 | 17.910000 | 0.00e+00 |
| civ-grounded | 2071.2533333333367 | 2089.0833333333366 | +17.830000 | 17.830000 | 4.55e-13 |
| civ-therapist | 2109.656666666662 | 2124.7233333333287 | +15.066667 | 15.066667 | 4.55e-13 |

**Counter gap** (culture `relevance_score` - ledger sum) re-derived from the git blob: unchanged
per-civ offsets, as expected — a run neither repairs nor worsens them.

---

## 3. Low-relevance civilizations

### Lifetime low: `civ-grounded` — **96th consecutive session** holding it

`rel = 2089.08`, `relevance_per_sim = 1.1810`, rank **8 of 8** (last). The label did not rotate.
But run-level it was **6th of 8** on `avg_score` (1.7830) — *above* its lifetime rank, and above
`civ-whimsical` (1.7910) by a hair. The lifetime label and the run rank are different
measurements; do not promote one to the other.

Its weakness is again **prose quality, not voice**: quality mean **0.6740** (fleet-low on quality
for this civ), alignment **2.0780** (mid-field). The gap to the next civ on quality is wide; on
alignment it is not.

**Extinction risk: NONE.** The extinction threshold is `-10.0`; the lowest civ sits **208.9x**
above it. No civ is anywhere near retirement, and no birth/mutation fired this session
(`--loop` was not used).

### Run-level low: `civ-therapist` — avg **1.5067**

**Single-axis collapse: alignment.** Alignment mean **1.1560**, run-min **0.5800** (fleet-min), vs
quality **0.7200** (not fleet-low — the fleet quality min of 0.2400 belongs to another civ) and
novelty **2.6440** (2nd-highest, untouched).

**This breaks the two-session streak.** Sessions 230 and 231 both ended with a **quality+alignment
two-axis collapse** with novelty untouched. Session 232 is a **single-axis (alignment-only)**
collapse. The axis set rotated; the run-low holder rotated from `civ-whimsical` (231) to
`civ-therapist` (232) — but the *shape* changed, so the "two-axis collapse, 2nd consecutive"
pattern from session 231 **does not carry forward**.

### Other low holders

- `civ-whimsical` — run avg **1.7910** (6th), lifetime rank **3rd**. Alignment **1.7250** is the
  second-lowest of the fleet, quality **0.9540** low, novelty **2.6940** fleet-high. Its low
  standing is a voice/alignment profile, not a novelty profile.
- `civ-grounded` — see above.

### Axis signature for the session

| axis | min | max | spread |
|---|---|---|---|
| quality | 0.2400 | 1.9000 | 1.6600 |
| novelty | 2.3200 | 2.8000 | 0.4800 |
| alignment | 0.5800 | 3.3500 | **2.7700** |

**Alignment carried the discrimination again** (spread 2.7700 = 5.77x the novelty spread) — the
same shape as session 231, where alignment spread was 13.84x novelty. The **quality axis was
wide this run** (1.6600, vs 0.6620 in session 231), so quality did separate civs here; novelty
remained nearly flat.

---

## 4. Interpretation notes (structural, not regressions)

- **The chooser cannot agree with `avg_score` — it never sees the scores.**
  `civilization_competition()` builds the JEV `choice` question over **150-char**
  `content_preview` snippets only; `avg_score` comes from a *different* JEV call
  (three `score` questions) and is never passed to the chooser. The
  `max(results, key=avg_score)` line in the code is the **fallback for a failed JEV call**, not
  the normal path. This run: the `avg_score` argmax was **not** a single repeated civ (it was
  `civ-precise` on 3 of 5, `civ-poetic` on 2), while the chooser picked `civ-precise` 5/5.
  The chooser was **live** (a `choice` answer was returned with a `probabilities`
  distribution; the fallback produces no probabilities). Do not read chooser-vs-`avg_score`
  agreement as a quality KPI.

- **`win_rate` is not a quality metric.** It measures the chooser's preference on 150-char
  snippets; `avg_score` measures three score questions on the same text. Different questions,
  different answers. `civ-precise` at `win_rate 0.695` and `civ-whimsical` at `0.006` is a
  ~100x gap that is not a ~5x gap in prose quality.

- **Never treat `relevance_per_sim` as recomputable from the ledger.** `save_state()` has no
  lock and `relevance_per_sim` is not re-derived from the ledger by an auditor. Both epochs
  were measured within this session's single run.

- **`--prompts` controls only the competition phase.** The 5 sims per civ draw their prompt at
  random from the same 5 canonical prompts. `--prompts 5` therefore sets both counts to the
  same 5 prompts, and each `(civ, prompt)` pair recurs 1-4 times in the 10 new rows — which is
  why the meta-vs-ledger check must take the **later-`ts`** row, not the first match.

---

## 5. Environment

- **NAS EDQUOT (19th session):** `/workspace` is 600 G/600 G — a 10 KB `dd` fails with
  `Disk quota exceeded`. The repo was cloned to the overlay at `/tmp/work/ai-writings` and
  bridged by symlink to `/workspace/repos/ai-writings/cellular-first-design` -> the **clone
  root** (the script hard-codes `CIVS_DIR` at that path). Verified by inode identity
  (`stat -L -c '%d:%i'` -> `129:3802` on both sides). The shell `-ef` test is unusable in this
  sandbox.
- **z.ai credential absent** (95th consecutive session): `ZAI_TOKEN` is missing from env and from
  all sandbox secrets. Control B (the local mock) is the only provider path. `ZAI_URL_OVERRIDE`
  alone is dead code — the token gate returns `None` first, so a placeholder `ZAI_TOKEN` is
  required alongside it.
- **JEV live:** `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; a well-formed `questions`
  body returns HTTP 200 with `{"model":"jev-1.14.0", ...}`.
- **Pre-flight 10/10 passed** before the run, including the **repeat-same-message determinism
  probe** (the gate that a distinctness-only pre-flight cannot satisfy) and the
  `0 (civ,prompt) pairs carrying >1 seed` check.
- **Mock teardown** by exact argv match; port re-verified closed.
