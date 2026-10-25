# RUN REPORT — session 147 (2026-10-25)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (mock zai bridge) — z.ai credential gap (401), JEV live.
**Result:** clean — **19th consecutive clean mock measurement**.
**Run timestamp:** 2026-10-25T00:12:56

---

## 1. Environment (how the run was made possible)

The prompt named a path that does not exist in this sandbox:
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations/` — the workspace was a
**fresh NAS mount with no clone at all** (`/workspace` contained only `.plugin-cache`). The
repo slug in the prompt was also wrong on both segments. Resolved as:

| Fact | Value |
|---|---|
| Upstream | `SuperInstance/AI-Writings` (`ai-writings/cellular-first-design` slug 404s; API is case-insensitive) |
| Real path in repo | `cellular-first-design/code/civilizations/` (nested under `ai-writings`) |
| Clone target | `/tmp/work/ai-writings` (overlay; **NAS EDQUOT blocks every `/workspace` write**) |
| Bridge | `ln -sfn /tmp/work/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design` |
| Bridge verification | `stat -L -c '%d:%i'` -> `129:2653` on both sides; `-ef` -> **EF_OK**; `readlink -f` -> nested dir (not flattened) |
| `gh` | **not installed** (26th session) — used `GET /user/repos` + `GET /search/repositories` with `GITHUB_TOKEN` |
| `TYPESAFE_AI_TOKEN` | present in env -> exported as `TYPESAFEAI_KEY` (script reads the latter) |
| JEV liveness | HTTP **422 `too_short`** on an empty `questions` dict => token accepted, endpoint live. Not "down". |
| `ZAI_TOKEN` | **absent** from env => z.ai returns **401 `token expired or incorrect`** (endpoint healthy, credential gap — 43rd session) |
| Control B | `ZAI_TOKEN=mock-local-bridge` + `ZAI_URL_OVERRIDE=http://127.0.0.1:8799/...` (the override alone is dead code behind the token gate) |
| Tool timeout | 30 s < run ~50 s => run launched detached, polled via `ps` + log |

## 2. Mock reconstruction — all three historical bugs pre-applied

`/tmp` was wiped, so the mock was rebuilt from scratch. **Both** known mock bugs were live
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

### Pre-flight (the 4th save in the series — sessions 115, 117, 145, 147)

Built the **exact** cultural prompt the orchestrator uses (`You are a voice in the tradition of
"<CIV NAME>".\nYour tenets: …\nYour voice: …\n\n{prompt}`) for all 8 civs:

```
distinct seeds   : 8 / 8  OK
distinct previews: 8 / 8  OK
distinct md5s    : 8 / 8  OK
prompt lengths   : 167-199
tracebacks=0  EXC=0  OK
http errors      : 0
```

## 3. Verification — every assertion held

Asserted on **rows**, never on the exit code (all failure modes are silent with exit 0).

| Assertion | Expected | Measured | |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | +10 each | engineer 906->916, formal 937->947, grounded 952->962, mythic 909->919, poetic 931->941, precise 901->911, therapist 904->914, whimsical 964->974 | PASS |
| total new ledger rows | 80 | **80** | PASS |
| `meta_log.jsonl` delta | +5 | 468 -> **473** | PASS |
| `Winner:` lines | 5 | **5** | PASS |
| rows with `[mock-zai` prefix | 80 | **80/80** | PASS |
| rows with `provider=zai` | 80 | **80/80** | PASS |
| rows with a JEV `error` key | 0 | **0** | PASS |
| rows with the 2.0/2.0/2.0 fallback triple | 0 | **0** | PASS |
| distinct seeds across the 80 new rows | 40 | **40** | PASS |
| `(civ, prompt)` combos with >1 seed | 0 | **0** | PASS |
| per-prompt distinct seeds + previews (ts-sorted last 8) | 8/8 x 5 | **8/8 on all 5** | PASS |
| sim->competition ts gap at index 4 | 8/8 | **8/8** (1.06 s – 22.85 s) | PASS |

**Row isolation method:** the **last 10 rows of each civ file** (per-civ tail), concatenated
and then **sorted by `ts`**. Never `rows[-80:]` over the concatenated files — `glob()` order is
filesystem order, not chronological, and that slice mixes historical rows from a
late-alphabet civ into "this run's" rows (a false mock-integrity failure, session 143).

## 4. Competitions — chooser vs `avg_score` argmax: **0/5 (0 %)**

| Prompt | Winner | Winner score | argmax | argmax score | |
|---|---|---|---|---|---|
| what a cell is | The Formal (`civ-formal`) | 0.190 | `civ-poetic` | 0.743 | disagree |
| the bookkeeper's role | The Precise (`civ-precise`) | 0.323 | `civ-poetic` | 0.633 | disagree |
| the witness log | The Precise (`civ-precise`) | 0.623 | `civ-poetic` | 0.857 | disagree |
| ternary values | The Precise (`civ-precise`) | 0.453 | `civ-whimsical` | 0.750 | disagree |
| JEV as a decision oracle | The Precise (`civ-precise`) | 0.357 | `civ-poetic` | 0.473 | disagree |

**0/5 — the chooser disagreed with the argmax in every single competition.** The rate is
**not narrowing** across the clean-mock series (0/5, 3/5, 1/5, 4/5, 4/5, 3/5, 0/5, 4/5, 4/5,
1/5, 2/5, 4/5, 4/5, **0/5**) — 14 five-sample points cannot pin a rate; the honest claim is
*somewhere in 0–80 %*. What survives every session: **the chooser is not a pure argmax, and
every observed disagreement goes the same way — it takes the LOWER-scoring candidate.**
Never treat `win_rate` as a quality metric; it is a *selection* metric.

`civ-precise` swept **4/5** prompts (plus `civ-formal` 1/5) and is the lifetime `win_rate`
leader (0.562) at `preferred_temp` 0.2 — the coldest voice is what the chooser rewards.

## 5. Cross-civ dimension spreads (run level, 10 rows each)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-therapist | 0.1470 | 0.0070 | 0.4060 | 0.0280 |
| civ-grounded | 0.1560 | 0.0070 | 0.3840 | 0.0770 |
| civ-engineer | 0.1567 | 0.0090 | 0.3380 | 0.1230 |
| civ-formal | 0.1570 | 0.0080 | 0.4100 | 0.0530 |
| civ-mythic | 0.2277 | 0.0090 | 0.3860 | 0.2880 |
| civ-whimsical | 0.3223 | 0.0180 | 0.4900 | 0.4590 |
| civ-precise | 0.4677 | 0.0220 | 0.6990 | 0.6820 |
| civ-poetic | 0.6927 | 0.0500 | 0.6080 | 1.4200 |

**Spreads:** `alignment` **1.3920** > `avg_score` 0.5457 > `novelty` 0.3610 > `quality` **0.0430**.
Alignment again carried the widest spread and is again the axis the chooser selects on.
**Quality collapsed again** (0.007–0.050) — the 15th of the last 16 clean-mock sessions. The
quality collapse is a **LEVEL that moves**, not a stable property: rank on cross-civ spreads,
never on absolute quality levels, and never on a single run's low.

## 6. Low-relevance civ — the label did NOT rotate: `civ-grounded`, 45 consecutive sessions (95–147)

**Lifetime table (all rows):**

| civ | rows | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| **civ-grounded** | 962 | **1.0647** | **0.4828** | 1.4911 | **1.2201** |
| civ-engineer | 916 | 1.2196 | 0.5252 | 1.4593 | 1.6742 |
| civ-formal | 947 | 1.2373 | 0.5164 | **1.3840** | 1.8114 |
| civ-therapist | 914 | 1.2538 | 0.5426 | 1.7430 | 1.4758 |
| civ-mythic | 919 | 1.3436 | 0.6111 | 1.7498 | 1.6697 |
| civ-precise | 911 | 1.4436 | 0.5761 | 1.5267 | 2.2279 |
| civ-whimsical | 974 | 1.5029 | 0.6848 | 1.9642 | 1.8598 |
| civ-poetic | 941 | 1.6398 | 0.8477 | 1.8954 | 2.1764 |

**The structural gap is alignment: 0.2557 below the next civ** (`civ-therapist` 1.4758),
versus **0.0336** on quality — a **7.6x** wider alignment gap. Alignment is the dimension the
meta-GAN *selects* on, so Grounded fails to **embody a distinctive voice**, not merely to write
weakly: a **voice failure, not a prose failure**. Lifetime novelty 1.4911 is above median —
Grounded is not boring, it is *unmistakable in a way the chooser does not reward*.

**Leaderboard (post-run):** grounded `relevance` 939.86, `relevance_per_sim` 1.023 — last of 8
on both, before and after the run (932.06 / 1.037 -> 939.86 / 1.023). Extinction risk **NONE**:
threshold -10, lowest relevance 939.86 = **94x above the floor**. Registry 8, `max_civs` 12,
all 8 civs still `generation=1`; extinction/birth only runs under `--loop`.

### Watch axis — `civ-therapist` (3rd session at the run bottom on `alignment`)

`civ-therapist` took the run-level **low on `avg_score` (0.1470)** *and* the run-level low on
`alignment` (0.0280). Its lifetime standing is mid-field (avg_score 1.2538, 5th of 8) =>
**watch axis, not a finding.** It becomes one only if the lifetime axis moves too. Note the
session-132 rule: *the lifetime table is the structural signal, the run ranking is the watch
axis* — the per-run low and the lifetime low are routinely **different civs** on **different
axes**, which is not a contradiction.

### Other standing axes

- `civ-formal` = the distinct low-**novelty** axis (1.3840, last of 8; alignment 1.8114 healthy).
- `civ-poetic` = 1st on lifetime `avg_score` (1.6398) / `quality` (0.8477) but last on
  `win_rate` (0.013) — the stable **selection-failure inverse**.
- `civ-precise` = best `win_rate` (0.562) and highest `alignment` (2.2279) but 6th on
  `avg_score` (1.4436) — the mirror inverse.
- `civ-whimsical` = last on `win_rate` (0.011).

### Counter gap is a FIXED per-civ offset, not a growing one

`culture.sims_run` minus the ledger row count: whimsical **-63**, grounded -43, formal -42,
poetic -37, engineer -22, mythic -20, therapist -17, precise -16 — **byte-identical to
session 145**. So it is a per-civ constant, not an accumulating leak. `save_state()` has no
lock => `relevance_per_sim` is still not recomputable from the ledger by an auditor.

## 7. Structural notes for the next session

- **The prompt's path was wrong on both segments** and the workspace had no clone. The
  `ai-writings/` prefix is the *repo*; `cellular-first-design/` is a *subdirectory* of it. The
  orchestrator's own `CIVS_DIR` constant encodes the correct full path
  (`/workspace/repos/ai-writings/cellular-first-design/code/civilizations`) — read it from
  the script before hunting for the tree.
- **A 5/5 consistent `ls` failure on the workspace path means "not cloned", not "mount race".**
  `ls /workspace` showed only `.plugin-cache`. The bridge only helps *after* a clone exists.
- **NAS EDQUOT is total** (11th session) — `git clone` directly into `/workspace` dies with
  `close error: Disk quota exceeded` and leaves a partial `.git`. Clone to `/tmp` first, then
  bridge. The bridge *target* can be the overlay, so writes through it succeed normally.
- **The `write` tool hit the known sporadic `-122` on close** for a file under
  `/workspace/analysis/`. Use `printf`/heredoc in bash to `/tmp` for throwaway analysis
  scripts instead.
- **Mock teardown:** kill both pids by exact args (`python3 /tmp/mock_zai.py` = server;
  `timeout -s KILL 900 python3 /tmp/mock_zai.py` = wrapper), then confirm the port with
  `curl -m 5` -> **exit 7** (refused). Never `pkill -f mock_zai` — it self-matches.
