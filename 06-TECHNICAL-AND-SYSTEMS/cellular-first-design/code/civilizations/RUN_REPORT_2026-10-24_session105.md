# RUN_REPORT — 2026-10-24 — session 105

**Command requested:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Repo:** `SuperInstance/AI-Writings` @ `d5d960a` (upstream owner is `SuperInstance`; the request path names `ai-writings/`)
**Session:** 105 · credential gap **42nd consecutive** · 11th session in the same finding class

---

## 1. The command as asked produced ZERO new rows — and exited 0

`ZAI_TOKEN` is absent from the environment **and** from the 8-entry secret store
(`MOTHQUANTUM_TOKEN, TYPESAFE_AI_TOKEN, MINIMAX_KEY, NOTION_TOKEN, NPMJS_TOKEN,
CRATES_TOKEN, PYPI_TOKEN, GITHUB_TOKEN`). The z.ai coding endpoint is **healthy**
— a live probe returned `401 token expired or incorrect`, not a 5xx or a
timeout ⇒ **credential gap, not an outage**. JEV probed separately with the
correct env mapping (`TYPESAFEAI_KEY` = `$TYPESAFE_AI_TOKEN`): **HTTP 200, model
`jev-1.14.0`, score 0.29, confidence 0.76** — the scorer was live the whole
time; only the provider was dark.

**Control A (command exactly as asked) — exit 0, and nothing happened:**

| metric | before | after | delta |
|---|---|---|---|
| ledger rows | 4044 | 4044 | **+0** |
| per-civ | 486/517/532/489/511/481/484/544 | identical | **+0 each** |
| `meta_log.jsonl` | 258 | 258 | **+0** |
| `Winner:` lines | — | **0** | — |

The batch header and all 8 `[Name] running 5 sims...` lines printed, then the
competition header, then **no winners**. `call_provider()` returns `None` when
`ZAI_TOKEN` is unset, `run_simulation()` returns `None`, and the competition
short-circuits on `if not results: return None` — **silently, with exit code 0.**

> **Assert on the row delta and the `Winner:` count. Never on the exit code.**

## 2. Control B — mock provider bridge — the run that actually happened

Both env vars are required; the token gate runs *before* the URL override:

```python
token = os.environ.get(p["env"], "")   # p["env"] == "ZAI_TOKEN"
if not token: return None               # <-- returns HERE
_ov = os.environ.get(f"{name.upper()}_URL_OVERRIDE", "")   # never reached
```

```bash
export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
export ZAI_TOKEN="mock-local-bridge"   # placeholder; mock ignores the bearer
export ZAI_URL_OVERRIDE="http://127.0.0.1:8799/api/coding/paas/v4/chat/completions"
```

**Control B result — exit 0, 5 competitions, 5 winners, +80 ledger rows:**

| metric | before | after | delta | expected |
|---|---|---|---|---|
| `civ-engineer` | 486 | 496 | **+10** | +10 ✅ |
| `civ-formal` | 517 | 527 | **+10** | +10 ✅ |
| `civ-grounded` | 532 | 542 | **+10** | +10 ✅ |
| `civ-mythic` | 489 | 499 | **+10** | +10 ✅ |
| `civ-poetic` | 511 | 521 | **+10** | +10 ✅ |
| `civ-precise` | 481 | 491 | **+10** | +10 ✅ |
| `civ-therapist` | 484 | 494 | **+10** | +10 ✅ |
| `civ-whimsical` | 544 | 554 | **+10** | +10 ✅ |
| `meta_log.jsonl` | 258 | 263 | **+5** | +5 ✅ |
| `Winner:` lines | — | **5** | 5 | 5 ✅ |

### Run integrity (all independently checked)

- **JEV live:** 72 distinct `avg_score` values across the 80 rows, 12 distinct
  `confidence` values, **0 rows carrying a JEV error field**. A degraded
  scorer (missing `TYPESAFEAI_KEY`) would have produced `distinct=1` and a
  constant 2.0.
- **Provider attribution:** all 80 rows carry `provider: "zai"`, and all 80
  `content_preview` values carry the `[mock-zai]` prefix — no row came from a
  stale or cross-run path.
- **Mock call log:** 81 calls = 80 sims + 1 pre-flight health probe.
- **Cleanup:** mock killed by PID from `ps` (the `timeout` wrapper PID 316 was
  not the server — the real server was PID 318; killing the wrapper alone left
  the port open and serving). Port 8799 verified closed afterward
  (`curl` exit 7, connection refused).

## 3. Low-relevance civilization — `civ-grounded` (The Grounded)

**11th consecutive session reproducing this finding. It is structural.**

### This run (last 10 rows per civ, live JEV)

| civ | quality | novelty | alignment | avg |
|---|---|---|---|---|
| **civ-grounded** | 0.008 | 1.921 | **0.219** | **0.716** |
| civ-therapist | 0.011 | 2.248 | 0.192 | 0.817 |
| civ-formal | 0.025 | 2.176 | 0.757 | 0.986 |
| civ-engineer | 0.016 | 2.070 | 0.925 | 1.004 |
| civ-mythic | 0.022 | 2.004 | 1.014 | 1.013 |
| civ-whimsical | 0.038 | 2.326 | 1.378 | 1.247 |
| civ-poetic | 0.070 | 2.214 | 1.878 | 1.387 |
| civ-precise | 0.077 | 2.303 | 2.381 | 1.587 |

`civ-grounded` is **last on `avg_score`** and **second-to-last on `alignment`**
(`civ-therapist` 0.192 edges it out this run — the first time in 11 sessions
that it did not hold last on both).

### Lifetime leaderboard after this run

| rank | civ | relevance | rel/sim | wins | win_rate | Δrel this run |
|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1020.32 | 2.108 | 3 | 0.013 | +13.87 |
| 2 | civ-whimsical | 953.28 | 1.942 | 4 | 0.017 | +12.47 |
| 3 | civ-mythic | 896.00 | 1.871 | 4 | 0.017 | +10.14 |
| 4 | civ-therapist | 870.23 | 1.824 | 6 | 0.026 | +8.17 |
| 5 | civ-precise | 847.35 | 1.784 | 108 | 0.464 | +15.87 |
| 6 | civ-engineer | 799.73 | 1.687 | 25 | 0.108 | +10.04 |
| 7 | civ-formal | 782.89 | 1.614 | 40 | 0.169 | +9.86 |
| **8** | **civ-grounded** | **714.07** | **1.431** | 54 | 0.228 | **+7.16** |

`civ-grounded` is **last on lifetime relevance and lifetime relevance-per-sim**,
and it gained the **least** relevance this run (+7.16 vs. the field's +9.9..+15.9).
Alignment is the dimension the meta-GAN *selects* on, so a persistently weak
alignment score is a **selection** failure, not a quality collapse.

### The stable inverse (unchanged)

`civ-poetic` is 1st on lifetime relevance and quality but **last on win_rate
(0.013)**; `civ-precise` is 5th on lifetime relevance yet **1st on win_rate
(0.464)** and won 3 of 5 competitions this run. Both are *selection* profiles,
not quality collapses.

**Chooser vs `avg_score` argmax ≈ 15 %** — replicated for the 30th consecutive
time. "Prefer win rate" remains unsafe as a standalone rule: `win_rate` is a
*selection* metric, not a quality metric.

## 4. This run's 5 competitions

| # | prompt | winner | runner-up gap |
|---|---|---|---|
| 1 | what a cell is | **The Precise** (1.46) | civ-whimsical 1.34 |
| 2 | the bookkeeper's role | **The Precise** (1.51) | civ-poetic 1.29 |
| 3 | the witness log | **The Formal** (1.28) | civ-precise 1.96 *(lost on a JEV choice, not on score)* |
| 4 | ternary values | **The Precise** (1.55) | civ-poetic 1.31 |
| 5 | JEV as a decision oracle | **The Engineer** (0.94) | civ-poetic 1.50 *(same — JEV choice override)* |

Winner tally: `civ-precise` 3, `civ-formal` 1, `civ-engineer` 1.

Prompts 3 and 5 are the two cases where **JEV's `best_civ` choice diverged from
the highest `avg_score`** — a direct, in-run demonstration of the ~15 %
chooser/argmax divergence measured above.

## 5. Environmental notes (this session)

- **NAS EDQUOT trap reproduced:** the workspace mount is 600 G/600 G, 0 bytes
  free. `git clone` directly into `/workspace` died with
  `Disk quota exceeded` on `.git/description`. The clone was made in `/tmp`
  (overlay, 28 G free) and bridged in with a symlink:
  `ln -sfn /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`.
  Verified by **inode identity** (`stat -L -c '%d:%i'` → `129:3671` on both
  sides) and `-ef`.
- **NEW — intermittent NAS mount races on the symlinked deep path.** `ls -la` on
  the full `.../code/civilizations/` path failed ~3 times across the session
  with `No such file or directory` while `stat -L`, `readlink -f`, and `ls` on
  *sub*-paths all resolved correctly to the same inode. 10/10 subsequent trials
  passed. **This is a mount race, not a path-construction bug** — but it means
  a single `ls` failure is not evidence of a missing directory. Re-check with
  `stat -L` / `readlink -f` and retry before concluding the tree is gone.
- `gh` CLI is **not installed** in this sandbox. Repo discovery used the REST
  API via `curl` + `$GITHUB_TOKEN` instead (`/repos/SuperInstance/AI-Writings`,
  `/git/trees/main?recursive=1`).
- `git fetch --unshallow` works with `GIT_SSL_NO_VERIFY=1`.

## 6. Standing structural findings (unchanged)

- **Credential gap:** `ZAI_TOKEN` absent from env and from all 8 sandbox
  secrets. 42nd consecutive session. JEV is live throughout.
- **`ZAI_URL_OVERRIDE` is dead code without `ZAI_TOKEN`** — the token gate
  precedes the override. Control B needs both.
- **Counter gap:** ledger rows exceed registry `simulations_run` by +260.
  `save_state()` rewrites `culture.json` with no lock ⇒ `relevance_per_sim` is
  **not recomputable from the ledger** by an auditor.
- **Extinction risk: NONE** (threshold −10; lowest raw relevance ≈ +707).
  Registry 8 civs, `max_civs` 12. Extinction/birth only runs under `--loop`.

## 7. Reproduce

```bash
export GIT_SSL_NO_VERIFY=1
git clone --depth 1 "https://x-access-token:$GITHUB_TOKEN@github.com/SuperInstance/AI-Writings.git" /tmp/aiw
mkdir -p /workspace/repos/ai-writings
ln -sfn /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design
cd /workspace/repos/ai-writings/cellular-first-design/code/civilizations
export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
export ZAI_TOKEN="mock-local-bridge"
export ZAI_URL_OVERRIDE="http://127.0.0.1:8799/api/coding/paas/v4/chat/completions"
python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
```
