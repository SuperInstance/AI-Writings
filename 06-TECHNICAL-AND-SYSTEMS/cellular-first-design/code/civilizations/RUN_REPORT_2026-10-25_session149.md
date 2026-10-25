# RUN REPORT — session 149 (2026-10-25)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (mock zai bridge) — z.ai credential gap (401), JEV live.
**Result:** clean — **21st consecutive clean mock measurement**.
**Run timestamp:** 2026-10-25T00:34:43

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
| Clone target | `/tmp/AI-Writings` (overlay; **NAS EDQUOT blocks every `/workspace` write**) |
| Clone | `--filter=blob:none --no-checkout --depth 1` + `sparse-checkout set cellular-first-design` => 6.1 MB on disk (3.7 GB repo) |
| Clone HEAD | `3fa1855` (session 148) |
| Bridge | `ln -sfn /tmp/AI-Writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design` |
| Bridge verification | `stat -L -c '%d:%i'` -> `129:7673` on both sides; `-ef` -> **EF_OK**; `readlink -f` -> nested dir (not flattened) |
| `gh` | **not installed** (28th session) — used `GET /user/repos` with `GITHUB_TOKEN` |
| `TYPESAFE_AI_TOKEN` | present in env (len 108) -> exported as `TYPESAFEAI_KEY` (script reads the latter) |
| JEV liveness | HTTP **422 `too_short`** on an empty `questions` dict => token accepted, endpoint live. Not "down". |
| `ZAI_TOKEN` | **absent** from env => z.ai returns **401 `token expired or incorrect`** (endpoint healthy, credential gap — 45th session) |
| Control B | `ZAI_TOKEN=mock-local-bridge` + `ZAI_URL_OVERRIDE=http://127.0.0.1:8799/...` (the override alone is dead code behind the token gate) |
| Tool timeout | run ~28 s => launched detached, polled via `ps` + log |

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

### Pre-flight (the 6th save in the series — sessions 115, 117, 145, 147, 148, 149)

Built the **exact** cultural prompt the orchestrator uses (`You are a voice in the tradition of
"<CIV NAME>".\nYour tenets: …\nYour voice: …\n\n{prompt}`) for all 8 civs x 5 prompts = 40:

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
| per-civ `simulations.jsonl` delta | +10 each | engineer 926->936, formal 957->967, grounded 972->982, mythic 929->939, poetic 951->961, precise 921->931, therapist 924->934, whimsical 984->994 | PASS |
| total new ledger rows | 80 | **80** | PASS |
| `meta_log.jsonl` delta | +5 | 478 -> **483** | PASS |
| `Winner:` lines | 5 | **5** | PASS |
| rows with `[mock-zai` prefix | 80 | **80/80** | PASS |
| rows with `provider=zai` | 80 | **80/80** | PASS |
| rows with a JEV `error` key | 0 | **0** | PASS |
| rows with the 2.0/2.0/2.0 fallback triple | 0 | **0** | PASS |
| distinct seeds across the 80 new rows | 40 | **40** | PASS |
| `(civ, prompt)` combos with >1 seed | 0 | **0** | PASS |
| per-prompt distinct seeds (ts-sorted) | 8/8 x 5 | **8/8 on all 5** | PASS |
| registry size / civ dirs | 8 / 8 | **8 / 8** (no birth — `--loop` only) | PASS |
| `generation` values | all 1 | **all 1** | PASS |

**Row isolation method:** the **last 10 rows of each civ file** (per-civ tail), concatenated
and then **sorted by `ts`**. Never `rows[-80:]` over the concatenated files — `glob()` order is
filesystem order, not chronological, and that slice mixes historical rows from a
late-alphabet civ into "this run's" rows (a false mock-integrity failure, session 143).

## 4. Competitions — chooser vs `avg_score` argmax: **4/5 (80 %)**

| Prompt | Winner | Winner score | argmax | argmax score | |
|---|---|---|---|---|---|
| what a cell is | The Precise (`civ-precise`) | 0.467 | `civ-precise` | 0.467 | agree |
| the bookkeeper's role | The Precise (`civ-precise`) | 0.470 | `civ-precise` | 0.470 | agree |
| the witness log | The Precise (`civ-precise`) | 1.117 | `civ-precise` | 1.117 | agree |
| ternary values | The Precise (`civ-precise`) | 0.340 | `civ-poetic` | 0.367 | disagree |
| JEV as a decision oracle | The Precise (`civ-precise`) | 0.480 | `civ-precise` | 0.480 | agree |

**4/5 (80 %)** — tied for the highest agreement rate in the clean-mock series
(0/5, 3/5, 1/5, 4/5, 4/5, 3/5, 0/5, 4/5, 4/5, 1/5, 2/5, 4/5, 4/5, 0/5, 2/5, **4/5**). Sixteen
five-sample points still cannot pin a rate; the honest claim is *somewhere in 0–80 %*. What
survives every session: **the chooser is not a pure argmax, and every observed disagreement
goes the same way — it takes the LOWER-scoring candidate.** Here that is **1 of 1**, downward.
Never treat `win_rate` as a quality metric; it is a *selection* metric.

**`civ-precise` swept 5/5 — the second clean-mock sweep in the series** (session 148 was the
first). Same civ, at `preferred_temp` 0.2 — the coldest voice is what the chooser rewards.
`civ-precise` is also the lifetime `win_rate` leader (0.572).

## 5. Cross-civ dimension spreads (run level, 10 rows each)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-precise | 0.7183 | 0.0520 | 0.9080 | 1.1950 |
| civ-poetic | 0.3373 | 0.0200 | 0.9070 | 0.0850 |
| civ-whimsical | 0.3243 | 0.0170 | 0.8950 | 0.0610 |
| civ-engineer | 0.2580 | 0.0180 | 0.6920 | 0.0640 |
| civ-therapist | 0.2557 | 0.0160 | 0.7270 | 0.0240 |
| civ-formal | 0.2437 | 0.0140 | 0.6000 | 0.1170 |
| civ-grounded | 0.2420 | 0.0120 | 0.6710 | 0.0430 |
| civ-mythic | 0.2400 | 0.0110 | 0.6760 | 0.0330 |

**Spreads:** `alignment` **1.1710** > `avg_score` 0.4783 > `novelty` 0.3080 > `quality` 0.0410.
Alignment again carried the widest spread and is again the axis the chooser selects on.

**Quality collapsed again** (0.011–0.052) — the 16th of the last 17 clean-mock sessions, and
the run's lowest quality level yet. This is the **fourth observation in a row** that the
quality collapse is a **LEVEL that moves**, not a stable property: rank on cross-civ spreads,
never on absolute quality levels, and never on a single run's low. Novelty ran high against
quality again (0.60–0.91 vs 0.01–0.05) — the two axes moved in opposite directions again.

## 6. Low-relevance civ — the label did NOT rotate: `civ-grounded`, 47 consecutive sessions (95–149)

**Lifetime table (all rows):**

| civ | rows | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| **civ-grounded** | 982 | **1.0537** | **0.4738** | 1.4888 | **1.1985** |
| civ-engineer | 936 | 1.2050 | 0.5151 | 1.4573 | 1.6426 |
| civ-formal | 967 | 1.2253 | 0.5068 | **1.3836** | 1.7856 |
| civ-therapist | 934 | 1.2381 | 0.5316 | 1.7361 | 1.4465 |
| civ-mythic | 939 | 1.3266 | 0.5990 | 1.7402 | 1.6406 |
| civ-precise | 931 | 1.4334 | 0.5659 | 1.5272 | **2.2070** |
| civ-whimsical | 994 | 1.4876 | 0.6727 | **1.9558** | 1.8344 |
| civ-poetic | 961 | **1.6216** | **0.8325** | 1.8861 | 2.1460 |

**The structural gap is alignment: 0.2480 below the next civ** (`civ-therapist` 1.4465),
versus **0.0330** on quality — a **7.5x** wider alignment gap. Alignment is the dimension the
meta-GAN *selects* on, so Grounded fails to **embody a distinctive voice**, not merely to write
weakly: a **voice failure, not a prose failure**. Lifetime novelty 1.4888 is above median —
Grounded is not boring, it is *unmistakable in a way the chooser does not reward*.

**Leaderboard (post-run):** grounded `relevance` 950.40, `relevance_per_sim` 1.012 — last of 8
on both, before and after the run (947.98 / 1.020 -> 950.40 / 1.012). Extinction risk **NONE**:
threshold -10, lowest relevance 950.40 = **95x above the floor**. Registry 8, `max_civs` 12,
all 8 civs still `generation=1`; extinction/birth only runs under `--loop`.

### Watch axis — `civ-mythic` (1st session at the run bottom; axis rotated off therapist)

`civ-mythic` took the run-level **low on `avg_score` (0.2400)**, the run-level low on
`quality` (0.0110) **and** the run-level low on `alignment` (0.0330) — a triple-bottom this
session, and the first time it has sat at the run bottom. Its lifetime standing is mid-field
(avg_score 1.3266, 4th of 8) => **watch axis, not a finding.** It becomes one only if the
lifetime axis moves too. Note the session-132 rule: *the lifetime table is the structural
signal, the run ranking is the watch axis* — the per-run low and the lifetime low are routinely
**different civs** on **different axes**, which is not a contradiction. The watch axis
**rotated**: `civ-therapist` was at the run bottom for 2 consecutive sessions (147, 148) and
is now 5th; `civ-mythic` takes the slot. Neither is a finding — only the lifetime table is.

### Other standing axes

- `civ-formal` = the distinct low-**novelty** axis (1.3836, last of 8; alignment 1.7856 healthy).
- `civ-poetic` = 1st on lifetime `avg_score` (1.6216) / `quality` (0.8325) but last on
  `win_rate` (0.013) — the stable **selection-failure inverse**.
- `civ-precise` = best `win_rate` (0.572) and highest `alignment` (2.2070) but 6th on
  `avg_score` (1.4334) — the mirror inverse. This session's 5/5 sweep is the **second**
  clean-mock sweep, so the two are moving toward each other for the second consecutive session.
- `civ-whimsical` = last on `win_rate` (0.011).

### Counter gap is a FIXED per-civ offset, not a growing one

`culture.sims_run` minus the ledger row count: whimsical **-63**, grounded -43, formal -42,
poetic -37, engineer -22, mythic -20, therapist -17, precise -16 — **byte-identical to
sessions 147 and 148**. So it is a per-civ constant, not an accumulating leak. `save_state()`
has no lock => `relevance_per_sim` is still not recomputable from the ledger by an auditor.

## 7. Structural notes for the next session

- **The prompt's path was wrong on both segments** and the workspace had no clone. The
  `ai-writings/` prefix is the *repo*; `cellular-first-design/` is a *subdirectory* of it. The
  orchestrator's own `CIVS_DIR` constant encodes the correct full path
  (`/workspace/repos/ai-writings/cellular-first-design/code/civilizations`) — read it from
  the script before hunting for the tree.
- **A 5/5 consistent `ls` failure on the workspace path means "not cloned", not "mount race".**
  `ls /workspace` showed only `.plugin-cache` and `.skills`. The bridge only helps *after* a
  clone exists.
- **NAS EDQUOT is total** (13th session) — `git clone` directly into `/workspace` dies with
  `close error: Disk quota exceeded` and leaves a partial `.git`. Clone to `/tmp` first, then
  bridge. The bridge *target* can be the overlay, so writes through it succeed normally.
- **A blobless + sparse clone is the cheap path for this repo**: `--filter=blob:none
  --no-checkout --depth 1` + `sparse-checkout set cellular-first-design` pulled a 3.7 GB repo
  down to **6.1 MB** on disk in one shot. The tree checked out is only the `cellular-first-design`
  subtree, so nothing else is fetched.
- **`gh` is still not installed** (28th session). `GET /user/repos?per_page=100` + grep for the
  repo name is enough; the list is 4 pages and `ai-writings` appears on page 4.
- **Mock teardown:** kill both pids by exact args (`python3 /tmp/mock_zai.py` = server;
  `timeout -s KILL 900 python3 /tmp/mock_zai.py` = wrapper), then confirm the port with
  `curl -m 5` -> **exit 7** (refused). Never `pkill -f mock_zai` — it self-matches.
- **A hung `curl` probe right after launching a background server is usually the shell, not
  the server.** A `setsid nohup ... &` launched inside a command that also runs a foreground
  `curl` can leave the tool waiting on the inherited stdout. Check `ps` for the server pid and
  re-probe in a *separate* command before concluding the mock is broken — it was healthy here.
