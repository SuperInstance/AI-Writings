# Civ Orchestrator — Session 164 (2026-10-25)

**Run:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Result:** exit 0, 5 competitions, 5 `Winner:` lines, **80 new ledger rows**, all verification PASS.

---

## 1. Environment (all re-confirmed, 1 wipe since session 163)

- Workspace was **empty** at session start; the requested path
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did **not** exist
  (7th consecutive occurrence of the prompt naming an ephemeral path).
- Upstream owner is **`SuperInstance/ai-writings`** (API is case-insensitive: == `AI-Writings`).
  The `ai-writings/cellular-first-design` slug 404s. `gh` is **not** installed — used
  `GET /search/repositories?q=ai-writings` with `GITHUB_TOKEN`.
- **NAS EDQUOT trap re-confirmed (15th session), total and size-independent:** a
  `echo test > /workspace/repos/ai-writings/.probe` produced a **0-byte** file while `ls`
  still listed it, exit 0. `mkdir` works; the symlink bridge is the only way in.
  Cloning straight into `/workspace` failed with
  `error: .../.git/description: close error: Disk quota exceeded`.
- **Bridge:** clone to `/tmp` (overlay, 28 G free), then
  `ln -sfn /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`
  — the symlink points at the **nested `cellular-first-design` dir**, NOT the repo root.
  Verified by inode identity: `stat -L -c '%d:%i'` → `129:3669` on both sides, `-ef` OK.
  **Never flatten** the clone.
- **Credential gap (48th session):** `ZAI_TOKEN` is absent from the env and from all
  sandbox secrets; the real z.ai endpoint returns **401 `token expired or incorrect`**
  (endpoint healthy ⇒ credential gap, not an outage). Control B mock is the only
  provider path.
- **JEV live:** malformed `questions` → **422** `{"type":"dict_type"}` (payload-shape
  complaint ⇒ auth OK, not a outage). `TYPESAFEAI_KEY` **must** be exported from
  `TYPESAFE_AI_TOKEN` (the script reads the former, the sandbox stores the latter).
- **Tool-timeout trap:** `setsid nohup … &` **inherits stdout** and blocks the tool call
  until the 30 s timeout. Redirect to a file **and** `< /dev/null`; the job still starts.
  Ran the orchestrator detached and polled `ps` + the log.

## 2. Control B mock — rebuilt with all FOUR fixes

`/tmp` was wiped ⇒ the mock was rebuilt from the RUNBOOK. All historical bugs re-applied:

| # | Fix | Session | Symptom if missing |
|---|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` | 112 | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | `md5(whole_message)[:8]` | 118 | first 8 alnum chars are `YouAreA` for every civ ⇒ all 8 civs emit identical text |
| c | `Connection: close` + `Content-Length` | 144 | `curl` hangs to the tool timeout on a healthy server |
| d | seed placeholder **interpolated**, not literal `"{}"` | 145 | every response carries seed `{}` ⇒ 1 distinct seed, not 40 |

**Pre-flight probe (40 requests, exact long cultural prompt):** HTTP 200 in 1.2 ms,
**40/40 distinct seeds**, **40/40 distinct previews**, `[mock-zai seed=…]` prefix present,
214-char bodies, **0 tracebacks** in `/tmp/mock_zai.log`. Each returned seed matched an
independently recomputed `md5(whole_message)[:8]`.

Mock killed by exact-argv PID match (`python3 /tmp/mock_zai.py`, PID 246) — **not** by
`pkill -f mock_zai` (self-match). Port re-verified closed (`curl` exit 7).

## 3. Verification — 26/26 assertions PASS

| Check | Expected | Observed |
|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 × 8 | **+10 × 8** (80 rows) |
| `meta_log.jsonl` Δ | +5 | 553 → **558** |
| `culture.json` `simulations_run` Δ | +10 × 8 | **+10 × 8** |
| JEV `error` keys | 0 | **0** |
| `2.0/2.0/2.0` fallback triples | 0 | **0** |
| `provider` | `{zai}` | **`{zai}`** |
| `[mock-zai seed=…]` prefix | 80/80 | **80/80** |
| distinct seeds | 40 | **40** |
| `(civ,prompt)` with >1 seed | 0 | **0** (40 distinct combos) |
| `Winner:` lines | 5 | **5** |
| `meta_log` `results` shape | list of `[civ_id, score]` | **as expected** |
| `git status --porcelain` | 18 modified | **18** (8 ledgers + 8 cultures + meta_log + leaderboard) |

Per-civ Δ (pre → post): engineer 1076→1086, formal 1107→1117, grounded 1122→1132,
mythic 1079→1089, poetic 1101→1111, precise 1071→1081, therapist 1074→1084,
whimsical 1134→1144. All `simulations.jsonl` mtimes 03:44:13.

## 4. Low-relevance civilizations

### `civ-grounded` (The Grounded) — **40 consecutive sessions (125–164)**, last on every axis

Lifetime (8 844 rows):

| civ | avg_score | quality | novelty | alignment | relevance | rel/sim |
|---|---|---|---|---|---|---|
| **civ-grounded** | **0.9942** | **0.4175** | 1.4849 | **1.0802** | **1041.09** | **0.956** |
| civ-engineer | 1.1328 | 0.4528 | 1.4634 | 1.4823 | 1185.99 | 1.115 |
| civ-therapist | 1.1533 | 0.4652 | 1.7128 | 1.2817 | 1208.02 | 1.132 |
| civ-formal | 1.1658 | 0.4493 | **1.3956** | 1.6525 | 1216.67 | 1.132 |
| civ-mythic | 1.2573 | 0.5323 | 1.6999 | 1.5398 | 1318.13 | 1.233 |
| civ-precise | 1.3855 | 0.5094 | 1.5396 | **2.1076** | 1465.12 | 1.376 |
| civ-whimsical | 1.4062 | 0.5996 | **1.9147** | 1.7043 | 1435.56 | 1.328 |
| civ-poetic | **1.5509** | **0.7504** | 1.8497 | 2.0528 | **1626.29** | **1.514** |

Grounded is last on `avg_score`, `quality`, `alignment`, `relevance` and `relevance_per_sim`.
The structural gap is **alignment**: 0.4021 below the next civ (engineer 1.4823), versus
0.0353 on quality — **~11× wider**. Alignment is the dimension the meta-GAN *selects* on,
so this is a **voice** failure, not a capability failure. Grounded sits **below** mid-field
on novelty (1.4849, **6th of 8** — only formal 1.3956 and engineer 1.4634 are lower) — it
is not the *boring* civ, it is the *unmistakable* one, and the chooser does not reward
that.

**This run** Grounded is again last on `avg_score` (0.4477) and on `alignment` (0.2940),
but the run is compressed: only **0.0050** separates Grounded from `civ-therapist`
(0.4527), and on alignment Grounded (0.2940) vs Therapist (0.4110) is a 0.1170 gap.
Do not read the this-run last place as a reproduction of the lifetime gap — the lifetime
table is the structural signal.

### `civ-formal` — the low-novelty axis (steady)
Lifetime `novelty` **1.3956**, last of 8, while its `alignment` (1.6525) is healthy. A
distinct axis from Grounded's; not the low-relevance civ.

### `civ-engineer` — watch-axis (this run did NOT repeat the session-121 low)
4th of 8 on this run's `avg_score` (0.4847), 7th of 8 on lifetime `relevance_per_sim`
(1.115). Not promoted to a finding.

### Inverses
`civ-poetic` is 1st on lifetime `avg_score`/`quality`/`relevance` but **last on `win_rate`
(0.011, 6/533)** — a *selection* failure, not a quality collapse.
`civ-precise` is the mirror: best `win_rate` (**0.583, 308/528**), 1st on lifetime
`alignment` (2.1076), won **5/5** this run.

### Extinction risk: **NONE**
Threshold −10; lowest raw relevance **+1041.09** (104× above the floor). Registry 8 civs,
`max_civs` 12. All 8 still `generation=1` — birth/extinction only runs under `--loop`.

## 5. Chooser vs `avg_score` argmax: **0/5 (0 %)**

| # | winner | argmax | winner score | argmax score | |
|---|---|---|---|---|---|
| p1 | civ-precise | civ-poetic | 0.587 | 0.790 | disagree (lower) |
| p2 | civ-precise | civ-whimsical | 0.587 | 1.037 | disagree (lower) |
| p3 | civ-precise | civ-whimsical | 0.893 | 1.073 | disagree (lower) |
| p4 | civ-precise | civ-poetic | 0.593 | 1.207 | disagree (lower) |
| p5 | civ-precise | civ-poetic | 0.993 | 1.090 | disagree (lower) |

**Every** observed disagreement goes the same way — the chooser takes a **lower**-scoring
candidate (11th consecutive session with that direction). Mechanism (confirmed in source):
the chooser is a JEV **`choice`** question over 150-char `content_preview` snippets, while
`avg_score` is the mean of three **`score`** questions on the same text. Different questions,
different answers. **Never treat `win_rate` as a quality metric.** Clean-mock series now
0/5 (118) → 3/5 → 1/5 → 4/5 → 4/5 → 3/5 → 0/5 → 4/5 → 1/5 → 3/5 → 2/5 → 4/5 (130) → …
→ **0/5 (164)**. Fourteen five-sample points cannot narrow a rate — the honest claim is
*somewhere in 0–80 %*.

## 6. Cross-civ score spreads

| dimension | lifetime spread | this-run spread |
|---|---|---|
| `avg_score` | 0.5567 | 0.5137 |
| `quality` | 0.3328 | 0.1300 |
| `novelty` | 0.5191 | 0.8220 |
| `alignment` | **1.0274** | 0.9260 |

`alignment` remains the dominant discriminating axis; `quality` is the flattest
(0.1300 this run) — the level that moves, not a stable property. Rank on cross-civ
spreads, never on absolute quality levels, and never on a single run's low.

## 7. Counter gap: **NEGATIVE**, unchanged in sign and magnitude

| civ | `culture.json` relevance | ledger Σ`avg_score` | gap |
|---|---|---|---|
| civ-whimsical | 1435.56 | 1608.70 | **−173.14** |
| civ-poetic | 1626.29 | 1723.09 | −96.80 |
| civ-formal | 1216.67 | 1302.19 | −85.53 |
| civ-grounded | 1041.09 | 1125.44 | −84.35 |
| civ-mythic | 1318.13 | 1369.24 | −51.11 |
| civ-engineer | 1185.99 | 1230.24 | −44.24 |
| civ-therapist | 1208.02 | 1250.13 | −42.11 |
| civ-precise | 1465.12 | 1497.76 | −32.63 |
| **TOTAL** | | | **−609.92** |

The per-civ values are a **fixed offset** matching the pre-run git blobs exactly
(session 151's values: −173.15 / −96.81 / −85.53 / −84.35 / −51.11 / −44.25 / −42.11 /
−32.63, total −609.93). `save_state()` has no lock ⇒ **`relevance_per_sim` is not
recomputable from the ledger by an auditor.** Sign confirmed from the data, not copied.

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild from the
   RUNBOOK with **all four** fixes (112, 118, 144, 145) and run the pre-flight probe
   (40 distinct seeds AND 40 distinct previews) **before** the batch.
2. `ZAI_TOKEN` still absent ⇒ real z.ai unusable; Control B is the only provider path.
   JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
3. Use the run-wide integrity checks (80 rows, 40 seeds, per-`(civ,prompt)` 1:1) and
   isolate this run's rows by **count from the end of each civ file** (last 10), never by
   a `ts` cutoff.
4. `civ-grounded` has been the low-relevance civ for **40** straight sessions. If a
   session ever finds it mid-table, that is a *finding* — check the run-wide seed count
   first to rule out a degenerate mock before believing it.
5. Tool timeout 30 s < orchestrator run ~20 s ⇒ detached launch with stdout redirected
   **and** `< /dev/null`, then poll `ps` + the log.
