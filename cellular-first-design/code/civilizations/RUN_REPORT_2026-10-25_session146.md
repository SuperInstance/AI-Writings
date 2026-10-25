# Civ Orchestrator — RUN_REPORT_2026-10-25_session146

`python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

## Run identity

| item | value |
|---|---|
| upstream | `SuperInstance/AI-Writings` (3.7 GB; `ai-writings/cellular-first-design` 404s) |
| leaderboard iso (pre) | `2026-10-24T23:56:40` |
| leaderboard iso (post) | `2026-10-25T00:04:25` |
| provider | `zai` (Control B local mock bridge, `/tmp/mock_zai.py`, pid 319) |
| JEV | live (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; 200 on a live score probe) |
| z.ai live endpoint | **401 `token expired or incorrect`** — endpoint healthy, credential absent (43rd session on this gap) |
| registry | 8 civs, no births/extinctions (not `--loop`) |
| run | 18th consecutive clean mock measurement |

## Environment notes (this session)

- **NAS EDQUOT still total (10th session).** `git clone` into `/workspace/repos/...` died with
  `Disk quota exceeded`; the clone went to the local overlay (`/tmp/cfd`, 28 G free) and the
  **symlink bridge** was verified by inode identity (`129:1772` both sides, `-ef` OK) +
  `readlink -f` + `[-e]`. The `[ -e path ] && [ ! -L path ]` pre-check was run first, so the
  session-139 "real directory clobbers the symlink" trap did not fire.
- **Bridge target = the nested `cellular-first-design` dir.** `CIVS_DIR` resolved to
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` (confirmed by `ls -d`).
- **`gh` not installed** (25th session). Upstream located via `GET /user/repos?per_page=100` and
  `GET /search/code?q=civilization_orchestrator+in:path` with `GITHUB_TOKEN`.
- **The `ls` race did not fire** this session.
- **Mock was rebuilt from scratch** (`/tmp` was wiped), so both the session-112 index-wrap bug and
  the session-145 literal-`{}` bug were live again. The **pre-flight probe caught both before the
  run**: 40/40 distinct seeds, 40/40 distinct previews, 40/40 template md5s, 0 tracebacks.

## Row-count verification (assert on rows, never exit code)

| assertion | expected | observed |
|---|---|---|
| per-civ `simulations.jsonl` delta | +10 × 8 | **+10 × 8** (80 total) |
| `meta_log.jsonl` delta | +5 | **+5** (463 → 468) |
| `Winner:` lines | 5 | **5** |
| rows with `[mock-zai` prefix | 80 | **80** |
| rows with `provider=zai` | 80 | **80** |
| rows with a JEV `error` key | 0 | **0** |
| rows with 2.0/2.0/2.0 fallback | 0 | **0** |
| distinct seeds across new rows | 40 | **40** |
| `(civ,prompt)` combos with >1 seed | 0 | **0** |
| per-prompt distinct previews (slot-aligned) | 8/8 × 5 | **8/8 × 5** |

Per-civ delta: engineer 896→906, formal 927→937, grounded 942→952, mythic 899→909,
poetic 921→931, precise 891→901, therapist 894→904, whimsical 954→964.

Row isolation used the **per-civ tail + ts sort** method, not `rows[-80:]` over the
concatenation. The two ts clusters are visible: sim rows `…172.3` → `…195.4` (staggered, one civ
every ~3.1 s because of the `time.sleep(0.5)` rate limit inside each civ's 5 sims),
competition rows all at `…200.8`, meta rows at `…201.0`.

## Competition winners

| prompt | winner | argmax | agree |
|---|---|---|---|
| what a cell is | **The Precise** (`civ-precise`) | `civ-precise` (1.24) | yes |
| the bookkeeper's role | **The Precise** (`civ-precise`) | `civ-poetic` (1.48) | no |
| the witness log | **The Precise** (`civ-precise`) | `civ-precise` (1.38) | yes |
| ternary values | **The Precise** (`civ-precise`) | `civ-precise` (1.16) | yes |
| JEV as a decision oracle | **The Precise** (`civ-precise`) | `civ-precise` (1.29) | yes |

Chooser vs `avg_score` argmax: **4/5 (80 %)**. Clean-mock series:
0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125)
→ 4/5 (137) → 1/5 (138) → 2/5 (139) → 4/5 (144) → **4/5 (146)**.
The rate is **not** narrowing. The single disagreement again took the **lower**-scoring candidate
(winner 1.25 vs argmax 1.48) — the same direction as every disagreement ever observed.
**Never treat `win_rate` as a quality metric** — it is a *selection* metric.

`civ-precise` swept **5 of 5** prompts and is also the lifetime `win_rate` leader (0.559) at
`preferred_temp` 0.2 — the coldest, most literal voice is the one the chooser rewards.

## Low-relevance civilizations

**`civ-grounded` (The Grounded) — the low-relevance civ, 44 consecutive sessions (95–146).**

| metric | value | rank |
|---|---|---|
| lifetime `relevance` | 938.30 | last of 8 |
| `relevance_per_sim` | 1.032 | last of 8 |
| lifetime `avg_score` | 1.0742 | last of 8 |
| lifetime `alignment` | 1.2321 | last of 8 |
| lifetime `quality` | 0.4878 | last of 8 |
| lifetime `novelty` | 1.5027 | 6th of 8 (above median) |

The label did **not** rotate: Grounded was last before the run (relevance 932.06, per_sim
1.037) and was last after it (938.30, 1.032). This is the 44th consecutive session on the
lifetime axis. A single-run low is not a trend; the lifetime table is the structural signal.

**The structural gap is still alignment.** Grounded's alignment gap to the next civ
(`civ-therapist`, 1.4918) is **0.2597**, while quality's gap to the next civ
(`civ-formal`, 0.5219) is only **0.0341** — a **7.6×** wider alignment gap. Alignment is the
dimension the meta-GAN *selects* on, so Grounded fails to *embody a distinctive voice*, not
merely to write weakly. Novelty is above median, so it is not boring — it is unmistakable in a
way the chooser does not reward.

**Run-level watch axis: different civs on different axes — not a contradiction
(session-132 rule).**

| axis | run-last | value | run-1st | value |
|---|---|---|---|---|
| `avg_score` | `civ-grounded` | 0.6243 | `civ-precise` | 1.2510 |
| `alignment` | `civ-therapist` | 0.1760 | `civ-precise` | 1.8730 |
| `quality` | `civ-grounded` | 0.0250 | `civ-poetic` | 0.1160 |
| `novelty` | `civ-engineer` | 1.4840 | `civ-whimsical` | 1.8390 |

`civ-therapist` took the run low on `alignment` (0.1760) for the 2nd time (sessions 123, 146)
and remains mid-field on the lifetime axis (`avg_score` 1.2661, 5th of 8) — **watch axis, not a
finding**. It becomes one only if the lifetime axis moves too. `civ-formal` remains the distinct
low-novelty axis (lifetime `novelty` 1.3944, last of 8).

**Dimension-spread discipline:** this run's cross-civ spreads were `alignment` 1.6970,
`avg_score` 0.6267, `novelty` 0.3550, `quality` 0.0910. `quality` collapsed again to a
0.025–0.116 band (14 of the last 15 clean-mock sessions). The quality collapse is a **LEVEL that
moves**, not a stable property — rank on cross-civ spreads, never on absolute quality levels, and
never on a single run's low.

**Extinction risk: NONE.** Threshold −10; the lowest relevance is 938.30, i.e. 94× above the
floor. Registry 8, `max_civs` 12; extinction/birth only runs under `--loop`. All 8 civs remain
`generation=1`.

## Lifetime leaderboard (post-run)

| civ | relevance | per_sim | sims | win_rate | avg_score | alignment | quality | novelty |
|---|---|---|---|---|---|---|---|---|
| `civ-poetic` | 1439.34 | 1.610 | 894 | 0.014 | 1.6500 | 2.1845 | 0.8563 | 1.9092 |
| `civ-whimsical` | 1287.48 | 1.429 | 901 | 0.011 | 1.5152 | 1.8743 | 0.6917 | 1.9795 |
| `civ-precise` | 1277.77 | 1.444 | 885 | 0.559 | 1.4544 | 2.2450 | 0.5823 | 1.5358 |
| `civ-mythic` | 1181.34 | 1.329 | 889 | 0.021 | 1.3558 | 1.6850 | 0.6177 | 1.7648 |
| `civ-therapist` | 1102.41 | 1.243 | 887 | 0.020 | 1.2661 | 1.4918 | 0.5486 | 1.7578 |
| `civ-formal` | 1084.60 | 1.212 | 895 | 0.161 | 1.2488 | 1.8301 | 0.5219 | 1.3944 |
| `civ-engineer` | 1071.32 | 1.212 | 884 | 0.085 | 1.2313 | 1.6913 | 0.5309 | 1.4717 |
| `civ-grounded` | 938.30 | 1.032 | 909 | 0.152 | 1.0742 | 1.2321 | 0.4878 | 1.5027 |

**`civ-poetic` remains the stable inverse:** 1st on lifetime `avg_score` (1.6500) and
`quality` (0.8563), last on `win_rate` (0.014, 12/879). A *selection* failure, not a quality
collapse. `civ-precise` is the mirror inverse — best `win_rate` (0.559), 3rd on `avg_score`.
`civ-whimsical` is last on `win_rate` (0.011).

## Counter gap (auditability, unchanged)

`culture.json`'s `simulations_run` still under-counts the ledger because `save_state()`
rewrites the file with no lock: gaps of +16…+63 (whimsical +63, grounded +43, formal +42,
poetic +37, engineer +22, mythic +20, therapist +17, precise +16) — **identical to session
145**, confirming the gap is a fixed offset per civ and not a growing one. So
`relevance_per_sim` is **not recomputable from the ledger** by an auditor.

## Artifacts

| artifact | location |
|---|---|
| run report | `cellular-first-design/code/civilizations/RUN_REPORT_2026-10-25_session146.md` |
| orchestrator stdout | `/tmp/orch_run.log` (5 `Winner:` lines) |
| mock bridge | `/tmp/mock_zai.py` (torn down; `curl` exit 7 = port closed) |
| pre-flight probe | `/tmp/preflight.py` (40/40 seeds, 40/40 previews, 0 tracebacks) |
| verification | `/tmp/verify.py`, `/tmp/relevance.py` |
