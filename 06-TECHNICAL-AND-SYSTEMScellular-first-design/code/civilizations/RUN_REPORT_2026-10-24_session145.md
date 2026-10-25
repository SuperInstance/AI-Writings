# Civ Orchestrator — RUN_REPORT_2026-10-24_session145

`python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

## Run identity

| item | value |
|---|---|
| upstream | `SuperInstance/AI-Writings` (3.7 GB; `ai-writings/cellular-first-design` 404s) |
| leaderboard iso | `2026-10-24T23:56:40` |
| provider | `zai` (Control B local mock bridge, `/tmp/mock_zai.py`, pid 472) |
| JEV | live (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; 422 on a malformed payload = auth accepted) |
| z.ai live endpoint | **401 `token expired or incorrect`** — endpoint healthy, credential absent (known gap) |
| registry | 8 civs, no births/extinctions (not `--loop`) |
| run | 17th consecutive clean mock measurement |

## Environment notes (this session)

- **NAS EDQUOT still total.** `git clone` into `/workspace/repos/...` dies with
  `Disk quota exceeded`; the account-wide quota is consumed by other sessions. The clone went
  to the local overlay (`/root/repos/ai-writings`, 28 G free) and the **symlink bridge** was
  verified by inode identity (`129:12606` both sides, `-ef` OK) and `readlink -f`. The link
  path did not exist beforehand, so the session-139 "real directory clobbers the symlink"
  trap did not fire — but the `[ -e path ] && [ ! -L path ]` pre-check was run first anyway.
- **Bridge target must be the nested `cellular-first-design` dir.** `CIVS_DIR` resolved to
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` and was confirmed
  by `ls -d` on the deep path.
- **`gh` not installed** (24th session). Upstream located with
  `GET /user/repos?per_page=100` + `GITHUB_TOKEN`; `SuperInstance/AI-Writings` is the 3.7 GB one.
- **The `ls` race did not fire** this session; the deep path was resolvable on every check.

### New: the mock's seed placeholder must be interpolated, not left literal

The pre-flight probe caught a **self-inflicted** mock bug on the first attempt: the response
template carried a literal `seed={}` because the placeholder was never interpolated, so
**all 8 civs returned the same seed on every prompt** (1 distinct seed, 80 rows, all
prefixed `[mock-zai seed={}]`).

This is the *mirror* of the session-112 failure: session 112's mock crashed on `i >= 4`;
this one degraded silently. A socket-level 200 and a correct `[mock-zai` prefix were both
present — **only the seed-distinctness check exposed it.** The pre-flight's
`distinct seeds == 40` assertion is what saved the run, and it is the one assertion that
must never be relaxed.

The orchestrator's own `cultural_prompt` template *is* correct (8 civs → 8 distinct md5s
on the same prompt); the defect was in the mock's string formatting, not in the probe's
reconstruction of the template.

## Row-count verification (assert on rows, never exit code)

| assertion | expected | observed |
|---|---|---|
| per-civ `simulations.jsonl` delta | +10 × 8 | **+10 × 8** (80 total) |
| `meta_log.jsonl` delta | +5 | **+5** (458 → 463) |
| `Winner:` lines | 5 | **5** |
| rows with `[mock-zai` prefix | 80 | **80** |
| rows with `provider=zai` | 80 | **80** |
| rows with a JEV `error` key | 0 | **0** |
| rows with 2.0/2.0/2.0 fallback | 0 | **0** |
| distinct seeds across new rows | 40 | **40** |
| `(civ,prompt)` combos with >1 seed | 0 | **0** |
| per-prompt distinct seeds + previews | 8/8 × 5 | **8/8 × 5** |

Per-civ delta: engineer 886→896, formal 917→927, grounded 932→942, mythic 889→899,
poetic 911→921, precise 881→891, therapist 884→894, whimsical 944→954.

Row isolation used the **per-civ tail + ts sort** method (session-143 correction), not
`rows[-80:]` over the concatenation. The sim phase and the competition phase are visible as
two ts clusters: sim rows `…172.3` → `…194.3` (staggered, one civ every ~3.1 s because of the
`time.sleep(0.5)` rate limit inside each civ's 5 sims), competition rows all at `…200.8`,
meta rows at `…201.0`.

## Competition winners

| prompt | winner | argmax | agree |
|---|---|---|---|
| what a cell is | **The Formal** (`civ-formal`) | `civ-precise` (0.85) | no |
| the bookkeeper's role | **The Precise** (`civ-precise`) | `civ-precise` (0.92) | yes |
| the witness log | **The Precise** (`civ-precise`) | `civ-precise` (1.05) | yes |
| ternary values | **The Precise** (`civ-precise`) | `civ-precise` (0.71) | yes |
| JEV as a decision oracle | **The Precise** (`civ-precise`) | `civ-precise` (0.91) | yes |

Chooser vs `avg_score` argmax: **4/5 (80 %)** — the joint-highest of the clean-mock series
(sessions 137–144 gave 20 %, 60 %, 20 %, 80 % in the same band). The rate is **not**
narrowing across the series, so it remains a property of the meta-GAN, not a trend.

The single disagreement took the **lower**-scoring candidate (winner 0.58 vs argmax 0.85),
the same direction as every disagreement ever observed. **Never treat `win_rate` as a
quality metric** — it is a *selection* metric.

`civ-precise` swept 4 of 5 prompts, and it is also the lifetime `win_rate` leader (0.554)
with `preferred_temp` 0.2 — the coldest, most literal voice is the one the chooser rewards.

## Low-relevance civilizations

**`civ-grounded` (The Grounded) — the low-relevance civ, 43 consecutive sessions (95–145).**

| metric | value | rank |
|---|---|---|
| lifetime `relevance` | 932.06 | last of 8 |
| `relevance_per_sim` | 1.037 | last of 8 |
| lifetime `avg_score` | 1.0790 | last of 8 |
| lifetime `alignment` | 1.2428 | last of 8 |
| lifetime `quality` | 0.4927 | last of 8 |
| lifetime `novelty` | 1.5014 | 6th of 8 (above median) |

The label did **not** rotate: Grounded was last before the run (relevance 926.99, per_sim
1.043) and was last after it (932.06, 1.037). This is the 43rd consecutive session on the
lifetime axis. A single-run low is not a trend; the lifetime table is the structural signal.

**The structural gap is still alignment.** Grounded's alignment gap to the next civ
(`civ-precise`, 2.2492) is **1.0064**, while quality's gap to the next civ
(`civ-formal`, 0.5270) is only **0.3716** — a **2.7×** wider alignment gap. Alignment is
the dimension the meta-GAN *selects* on, so Grounded fails to *embody a distinctive voice*,
not merely to write weakly. Novelty is above median, so it is not boring — it is
unmistakable in a way the chooser does not reward.

**Run-level watch axis: different civs on different axes — not a contradiction
(session-132 rule).**

| axis | run-last | value | run-1st | value |
|---|---|---|---|---|
| `avg_score` | `civ-therapist` | 0.5033 | `civ-precise` | 0.8887 |
| `alignment` | `civ-mythic` | 0.4270 | `civ-precise` | 1.5990 |
| `quality` | `civ-grounded` | 0.0540 | `civ-whimsical` | 0.1180 |
| `novelty` | `civ-formal` | 0.6740 | `civ-whimsical` | 1.2960 |

`civ-therapist` took the run low on `avg_score` — it has now been a watch axis in sessions
138, 141, 144 and 145 without ever becoming a lifetime finding (lifetime `avg_score` 1.2731,
5th of 8), so it is **not** a finding. It becomes one only if the lifetime axis moves too.
`civ-formal` remains the distinct low-novelty axis (lifetime `novelty` 1.3904, last of 8).
`civ-grounded` took the run low on `quality` only — consistent with its lifetime position.

**Dimension-spread discipline:** this run's cross-civ spreads were `alignment` 1.1720,
`novelty` 0.6220, `avg_score` 0.3853, `quality` 0.0640. `quality` has now collapsed to a
0.014-0.064 band in 13 of the last 14 clean-mock sessions. The quality collapse is a **LEVEL
that moves**, not a stable property — rank on cross-civ spreads, never on absolute quality
levels, and never on a single run's low.

**Extinction risk: NONE.** Threshold −10; the lowest relevance is 932.06, i.e. 93× above the
floor. Registry 8, `max_civs` 12; extinction/birth only runs under `--loop`.

## Lifetime leaderboard (post-run)

| civ | relevance | per_sim | sims | win_rate | avg_score | alignment | quality | novelty |
|---|---|---|---|---|---|---|---|---|
| `civ-poetic` | 1428.50 | 1.616 | 921 | 0.014 | 1.6561 | 2.1921 | 0.8643 | 1.9120 |
| `civ-whimsical` | 1277.15 | 1.433 | 954 | 0.011 | 1.5202 | 1.8816 | 0.6981 | 1.9810 |
| `civ-precise` | 1265.26 | 1.446 | 891 | 0.554 | 1.4567 | 2.2492 | 0.5878 | 1.5330 |
| `civ-mythic` | 1173.62 | 1.335 | 899 | 0.021 | 1.3623 | 1.6964 | 0.6241 | 1.7665 |
| `civ-therapist` | 1096.03 | 1.250 | 894 | 0.021 | 1.2731 | 1.5065 | 0.5543 | 1.7585 |
| `civ-formal` | 1075.82 | 1.216 | 927 | 0.163 | 1.2528 | 1.8410 | 0.5270 | 1.3904 |
| `civ-engineer` | 1064.67 | 1.218 | 896 | 0.086 | 1.2376 | 1.7048 | 0.5365 | 1.4716 |
| `civ-grounded` | 932.06 | 1.037 | 942 | 0.153 | 1.0790 | 1.2428 | 0.4927 | 1.5014 |

**`civ-poetic` remains the stable inverse:** 1st on lifetime `avg_score` (1.6561) and
`quality` (0.8643), last on `win_rate` (0.014). A *selection* failure, not a quality
collapse. `civ-precise` is the mirror inverse — best `win_rate` (0.554), 3rd on `avg_score`.

## Counter gap (auditability, unchanged)

`culture.json`'s `simulations_run` still under-counts the ledger because `save_state()`
rewrites the file with no lock: gaps of +16…+63 (grounded +43, whimsical +63). So
`relevance_per_sim` is **not recomputable from the ledger** by an auditor. Unchanged from
the prior session's +260 fleet-wide figure — the per-civ figure is the honest one.

## Artifacts

| artifact | location |
|---|---|
| run report | `cellular-first-design/code/civilizations/RUN_REPORT_2026-10-24_session145.md` |
| orchestrator stdout | `/tmp/orch_run.log` (5 `Winner:` lines) |
| mock bridge | `/tmp/mock_zai.py` (torn down; `curl` exit 7 = port closed) |
| pre-flight probe | `/tmp/preflight.py` (40/40 seeds, 0 tracebacks) |
| verification | `/tmp/verify.py`, `/tmp/relevance.py` |
