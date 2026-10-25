# RUN REPORT — session 148 (2026-10-25)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (mock zai bridge) — z.ai credential gap (401), JEV live.
**Result:** clean — **20th consecutive clean mock measurement**.
**Run timestamp:** 2026-10-25T00:23:43

---

## 1. Environment (how the run was made possible)

The prompt named a path that does not exist in this sandbox:
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations/` — the workspace was a
**fresh NAS mount with no clone at all** (`/workspace` contained only `.plugin-cache` and
`.skills`). The repo slug in the prompt was also wrong on both segments. Resolved as:

| Fact | Value |
|---|---|
| Upstream | `SuperInstance/AI-Writings` (`ai-writings/cellular-first-design` slug 404s; API is case-insensitive) |
| Real path in repo | `cellular-first-design/code/civilizations/` (nested under `ai-writings`) |
| Clone target | `/tmp/work/ai-writings` (overlay; **NAS EDQUOT blocks every `/workspace` write**) |
| Clone depth | `--depth 1`, HEAD `e656d16` (session 147) |
| Bridge | `ln -sfn /tmp/work/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design` |
| Bridge verification | `stat -L -c '%d:%i'` -> `129:10430` on both sides; `-ef` -> **EF_OK**; `readlink -f` -> nested dir (not flattened) |
| `gh` | **not installed** (27th session) — used `GET /user/repos` + `GET /repos/{owner}/{repo}` with `GITHUB_TOKEN` |
| `TYPESAFE_AI_TOKEN` | present in env (len 108) -> exported as `TYPESAFEAI_KEY` (script reads the latter) |
| JEV liveness | HTTP **422 `too_short`** on an empty `questions` dict => token accepted, endpoint live. Not "down". |
| `ZAI_TOKEN` | **absent** from env => z.ai returns **401 `token expired or incorrect`** (endpoint healthy, credential gap — 44th session) |
| Control B | `ZAI_TOKEN=mock-local-bridge` + `ZAI_URL_OVERRIDE=http://127.0.0.1:8799/...` (the override alone is dead code behind the token gate) |
| Tool timeout | run ~55 s => launched detached, polled via `ps` + log |

## 2. Mock reconstruction — all four historical bugs pre-applied

`/tmp` was wiped, so the mock was rebuilt from scratch. **All four** known mock bugs were live
again in the naive rebuild and had to be re-applied *before* the run:

- **session-112 index wrap** — `seed[(i*2)%8:((i*2)%8)+2]`. A plain `seed[i*2:i*2+2]` is empty
  for `i >= 4` => `ValueError` => HTTP 500 **while the socket stays open** (a port/200 check
  looks healthy).
- **session-118 whole-message md5 seeding** — `md5(whole_message)[:8]`, not the first 8 alnum
  chars. The civ-specific fields (name / tenets / voice) must enter the hash, or all 8 civs
  emit identical text and every competition is void.
- **session-145 placeholder interpolation** — the `[mock-zai seed={}]` placeholder must be
  **interpolated**. Left literal, every response carries `seed={}` => 1 distinct seed instead
  of 40, while row counts, prefix checks and the exit code all look fine.
- **session-144 `Connection: close`** — added, so a `curl` probe does not hang waiting for EOF.

### Pre-flight (the 5th save in the series — sessions 115, 117, 145, 147, 148)

Built the **exact** cultural prompt the orchestrator uses (`You are a voice in the tradition of
"<CIV NAME>".\nYour tenets: …\nYour voice: …\n\n{prompt}`) for all 8 civs:

```
distinct seeds   : 40 / 40  OK
distinct previews: 40 / 40  OK
distinct md5s    : 40 / 40  OK
prompt lengths   : 167-209
per-prompt seeds : 8/8 on all 5 prompts
http errors      : 0
tracebacks       : 0  (grep -c Traceback /tmp/mock_zai.log)
```

## 3. Verification — every assertion held

Asserted on **rows**, never on the exit code (all failure modes are silent with exit 0).

| Assertion | Expected | Measured | |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | +10 each | grounded 962->972, whimsical 974->984, formal 947->957, poetic 941->951, precise 911->921, mythic 919->929, therapist 914->924, engineer 916->926 | PASS |
| total new ledger rows | 80 | **80** | PASS |
| `meta_log.jsonl` delta | +5 | 473 -> **478** | PASS |
| `Winner:` lines | 5 | **5** | PASS |
| rows with `[mock-zai` prefix | 80 | **80/80** | PASS |
| rows with `provider=zai` | 80 | **80/80** | PASS |
| rows with a JEV `error` key | 0 | **0** | PASS |
| rows with the 2.0/2.0/2.0 fallback triple | 0 | **0** | PASS |
| distinct seeds across the 80 new rows | 40 | **40** | PASS |
| `(civ, prompt)` combos with >1 seed | 0 | **0** | PASS |
| per-prompt distinct seeds (ts-sorted last 8) | 8/8 x 5 | **8/8 on all 5** | PASS |
| registry size / civ dirs | 8 / 8 | **8 / 8** (no birth — `--loop` only) | PASS |
| `generation` values | all 1 | **all 1** | PASS |

**Row isolation method:** the **last 10 rows of each civ file** (per-civ tail), concatenated
and then **sorted by `ts`**. Never `rows[-80:]` over the concatenated files — `glob()` order is
filesystem order, not chronological, and that slice mixes historical rows from a
late-alphabet civ into "this run's" rows (a false mock-integrity failure, session 143).

## 4. Competitions — chooser vs `avg_score` argmax: **2/5 (40 %)**

| Prompt | Winner | Winner score | argmax | argmax score | |
|---|---|---|---|---|---|
| what a cell is | The Precise (`civ-precise`) | 1.043 | `civ-poetic` | 1.063 | disagree |
| the bookkeeper's role | The Precise (`civ-precise`) | 1.117 | `civ-precise` | 1.117 | agree |
| the witness log | The Precise (`civ-precise`) | 1.537 | `civ-precise` | 1.537 | agree |
| ternary values | The Precise (`civ-precise`) | 1.080 | `civ-poetic` | 1.270 | disagree |
| JEV as a decision oracle | The Precise (`civ-precise`) | 1.083 | `civ-formal` | 1.120 | disagree |

**2/5 (40 %)** — the highest agreement rate in the clean-mock series
(0/5, 3/5, 1/5, 4/5, 4/5, 3/5, 0/5, 4/5, 4/5, 1/5, 2/5, 4/5, 4/5, 0/5, **2/5**). Fifteen
five-sample points still cannot pin a rate; the honest claim is *somewhere in 0–80 %*. What
survives every session: **the chooser is not a pure argmax, and every observed disagreement
goes the same way — it takes the LOWER-scoring candidate.** Here that is **3 of 3**
disagreements, all downward. Never treat `win_rate` as a quality metric; it is a
*selection* metric.

**`civ-precise` swept 5/5 — the first clean-mock sweep in the series.** Session 147 split
4 (`civ-precise`) + 1 (`civ-formal`); this session is a clean sweep by the same civ, at
`preferred_temp` 0.2 — the coldest voice is what the chooser rewards. `civ-precise` is also
the lifetime `win_rate` leader (0.567).

## 5. Cross-civ dimension spreads (run level, 10 rows each)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-precise | 1.2193 | 0.1470 | 2.1970 | 1.3140 |
| civ-poetic | 1.1870 | 0.2170 | 1.9960 | 1.3480 |
| civ-whimsical | 1.1633 | 0.1580 | 2.2000 | 1.1320 |
| civ-formal | 1.0773 | 0.0900 | 2.1260 | 1.0160 |
| civ-mythic | 0.8570 | 0.0710 | 1.9280 | 0.5720 |
| civ-engineer | 0.8190 | 0.0870 | 2.0410 | 0.3290 |
| civ-grounded | 0.8120 | 0.0680 | 2.0900 | 0.2780 |
| civ-therapist | 0.7810 | 0.0420 | 2.1070 | 0.1940 |

**Spreads:** `alignment` **1.1540** > `avg_score` 0.4383 > `novelty` 0.2720 > `quality` 0.1750.
Alignment again carried the widest spread and is again the axis the chooser selects on.

**Quality did NOT collapse this session** (0.042–0.217) — it broke a run of 15 collapses in
the last 16 clean-mock sessions. This is the third observation in a row that the quality
collapse is a **LEVEL that moves**, not a stable property: rank on cross-civ spreads, never
on absolute quality levels, and never on a single run's low. Novelty ran high across the
board (1.93–2.20) against quality — the two axes moved in opposite directions this session.

## 6. Low-relevance civ — the label did NOT rotate: `civ-grounded`, 46 consecutive sessions (95–148)

**Lifetime table (all rows):**

| civ | rows | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| **civ-grounded** | 972 | **1.0621** | **0.4786** | 1.4973 | **1.2104** |
| civ-engineer | 926 | 1.2152 | 0.5204 | 1.4656 | 1.6597 |
| civ-formal | 957 | 1.2356 | 0.5120 | **1.3918** | 1.8031 |
| civ-therapist | 924 | 1.2487 | 0.5372 | 1.7470 | 1.4619 |
| civ-mythic | 929 | 1.3383 | 0.6053 | 1.7517 | 1.6579 |
| civ-precise | 921 | 1.4431 | 0.5714 | 1.5339 | **2.2180** |
| civ-whimsical | 984 | 1.4995 | 0.6794 | **1.9666** | 1.8524 |
| civ-poetic | 951 | **1.6351** | **0.8411** | 1.8964 | 2.1677 |

**The structural gap is alignment: 0.2515 below the next civ** (`civ-therapist` 1.4619),
versus **0.0334** on quality — a **7.5x** wider alignment gap. Alignment is the dimension the
meta-GAN *selects* on, so Grounded fails to **embody a distinctive voice**, not merely to write
weakly: a **voice failure, not a prose failure**. Lifetime novelty 1.4973 is above median —
Grounded is not boring, it is *unmistakable in a way the chooser does not reward*.

**Leaderboard (post-run):** grounded `relevance` 947.98, `relevance_per_sim` 1.020 — last of 8
on both, before and after the run (939.86 / 1.023 -> 947.98 / 1.020). Extinction risk **NONE**:
threshold -10, lowest relevance 947.98 = **95x above the floor**. Registry 8, `max_civs` 12,
all 8 civs still `generation=1`; extinction/birth only runs under `--loop`.

### Watch axis — `civ-therapist` (2nd consecutive session at the run bottom)

`civ-therapist` took the run-level **low on `avg_score` (0.7810)**, the run-level low on
`alignment` (0.1940) *and* the run-level low on `quality` (0.0420) — a triple-bottom this
session, and the second consecutive session it has sat at the run bottom. Its lifetime standing
is mid-field (avg_score 1.2487, 5th of 8) => **watch axis, not a finding.** It becomes one only
if the lifetime axis moves too. Note the session-132 rule: *the lifetime table is the structural
signal, the run ranking is the watch axis* — the per-run low and the lifetime low are routinely
**different civs** on **different axes**, which is not a contradiction.

### Other standing axes

- `civ-formal` = the distinct low-**novelty** axis (1.3918, last of 8; alignment 1.8031 healthy).
- `civ-poetic` = 1st on lifetime `avg_score` (1.6351) / `quality` (0.8411) but last on
  `win_rate` (0.013) — the stable **selection-failure inverse**.
- `civ-precise` = best `win_rate` (0.567) and highest `alignment` (2.2180) but 3rd on
  `avg_score` (1.4431) — the mirror inverse. This session's 5/5 sweep is the first time the
  two have moved toward each other in the same direction.
- `civ-whimsical` = last on `win_rate` (0.011).

### Counter gap is a FIXED per-civ offset, not a growing one

`culture.sims_run` minus the ledger row count: whimsical **-63**, grounded -43, formal -42,
poetic -37, engineer -22, mythic -20, therapist -17, precise -16 — **byte-identical to
session 147**. So it is a per-civ constant, not an accumulating leak. `save_state()` has no
lock => `relevance_per_sim` is still not recomputable from the ledger by an auditor.

## 7. Structural notes for the next session

- **The prompt's path was wrong on both segments** and the workspace had no clone. The
  `ai-writings/` prefix is the *repo*; `cellular-first-design/` is a *subdirectory* of it. The
  orchestrator's own `CIVS_DIR` constant encodes the correct full path
  (`/workspace/repos/ai-writings/cellular-first-design/code/civilizations`) — read it from
  the script before hunting for the tree.
- **A 5/5 consistent `ls` failure on the workspace path means "not cloned", not "mount race".**
  `ls /workspace` showed only `.plugin-cache` and `.skills`. The bridge only helps *after* a
  clone exists.
- **NAS EDQUOT is total** (12th session) — `git clone` directly into `/workspace` dies with
  `close error: Disk quota exceeded` and leaves a partial `.git`. Clone to `/tmp` first, then
  bridge. The bridge *target* can be the overlay, so writes through it succeed normally.
- **`gh` is still not installed** (27th session). `GET /repos/{owner}/{repo}` returns 200 for
  `SuperInstance/ai-writings` while `.../cellular-first-design` returns 404 — one API call
  settles the path question without a clone.
- **Mock teardown:** kill both pids by exact args (`python3 /tmp/mock_zai.py` = server;
  `timeout -s KILL 900 python3 /tmp/mock_zai.py` = wrapper), then confirm the port with
  `curl -m 5` -> **exit 7** (refused). Never `pkill -f mock_zai` — it self-matches.
