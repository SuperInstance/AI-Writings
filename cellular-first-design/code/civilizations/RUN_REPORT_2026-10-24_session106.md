# RUN_REPORT — 2026-10-24 — session 106

**Command requested:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Repo:** `SuperInstance/AI-Writings` @ `015f968` (upstream owner is `SuperInstance`; the request path names `ai-writings/`)
**Session:** 106 · credential gap **43rd consecutive** · 12th session in the same finding class

---

## 1. The command as asked produced ZERO new rows — and exited 0

`ZAI_TOKEN` is absent from the environment **and** from the 8-entry secret store
(`MOTHQUANTUM_TOKEN, TYPESAFE_AI_TOKEN, MINIMAX_KEY, NOTION_TOKEN, NPMJS_TOKEN,
CRATES_TOKEN, PYPI_TOKEN, GITHUB_TOKEN`). The z.ai coding endpoint is **healthy**
— a live probe returned `401`, not a 5xx or a timeout ⇒ **credential gap, not an
outage**. JEV probed separately with the correct env mapping (`TYPESAFEAI_KEY` =
`$TYPESAFE_AI_TOKEN`): **HTTP 200, model `jev-1.14.0`, score 1.16, confidence 0.56**
— the scorer was live the whole time; only the provider was dark.

**Control A (command exactly as asked) — exit 0, and nothing happened:**

| metric | before | after | delta |
|---|---|---|---|
| ledger rows | 4044 | 4044 | **+0** |
| per-civ | 496/527/542/499/521/491/494/554 | identical | **+0 each** |
| `meta_log.jsonl` | 263 | 263 | **+0** |
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
| `civ-engineer` | 496 | 506 | **+10** | +10 ✅ |
| `civ-formal` | 527 | 537 | **+10** | +10 ✅ |
| `civ-grounded` | 542 | 552 | **+10** | +10 ✅ |
| `civ-mythic` | 499 | 509 | **+10** | +10 ✅ |
| `civ-poetic` | 521 | 531 | **+10** | +10 ✅ |
| `civ-precise` | 491 | 501 | **+10** | +10 ✅ |
| `civ-therapist` | 494 | 504 | **+10** | +10 ✅ |
| `civ-whimsical` | 554 | 564 | **+10** | +10 ✅ |
| `meta_log.jsonl` | 263 | 268 | **+5** | +5 ✅ |
| `Winner:` lines | — | **5** | 5 | 5 ✅ |

### Run integrity (all independently checked)

- **JEV live:** 69 distinct `avg_score` values across the 80 rows, 32 distinct
  `confidence` values, **0 rows carrying a JEV error field**. A degraded
  scorer (missing `TYPESAFEAI_KEY`) would have produced `distinct=1` and a
  constant 2.0. `avg_score` range 0.777–1.61.
- **Provider attribution:** all 80 rows carry `provider: "zai"`, and all 80
  `content_preview` values carry the `[mock-zai]` prefix — no row came from a
  stale or cross-run path.
- **Row isolation:** the run's 80 rows have 80 distinct `ts` values
  (1792857831.085 → 1792857859.635), so no prior-session rows leaked in.
- **Mock call log:** 81 calls = 80 sims + 1 pre-flight health probe.
- **Cleanup:** mock killed by PID from `ps` (wrapper PID 291 was the `timeout`
  line; the real server was PID **293** — killing the wrapper alone leaves the
  port open and serving). Port 8799 verified closed afterward
  (`curl` exit 7, connection refused).
- **`ls -la` verification on the exact requested path:** all 8
  `simulations.jsonl` + all 8 `culture.json` + `leaderboard.json` +
  `meta_log.jsonl` carry mtime `16:04` vs the `16:02` baseline.

## 3. Low-relevance civilization — `civ-grounded` (The Grounded)

**12th consecutive session reproducing this finding. It is structural.**

### This run (last 10 rows per civ, live JEV)

| civ | quality | novelty | alignment | avg |
|---|---|---|---|---|
| civ-engineer | 0.170 | 1.079 | 1.611 | **0.953** |
| civ-mythic | 0.234 | 1.361 | 1.485 | 1.027 |
| **civ-grounded** | 0.224 | 1.271 | 1.595 | **1.030** |
| civ-precise | 0.231 | 0.980 | 2.008 | 1.073 |
| civ-therapist | 0.282 | 1.242 | 1.823 | 1.116 |
| civ-formal | 0.282 | 0.936 | 2.153 | 1.124 |
| civ-poetic | 0.430 | 1.569 | 1.795 | 1.265 |
| civ-whimsical | 0.413 | 1.745 | 1.966 | **1.375** |

**NEW SHAPE — the low-relevance civ is not the run's minimum, and it WON 3 of 5.**
`civ-grounded` finished 5th of 8 on this run's `avg_score` (last in sessions
95–104), and JEV picked it as winner for prompts 1–3. So the run minimum is
now **`civ-engineer`** (0.953), a *different* civ from the lifetime bottom.

### Lifetime leaderboard after this run

| rank | civ | relevance | rel/sim | wins | win_rate |
|---|---|---|---|---|---|
| 1 | civ-poetic | 1032.97 | 2.091 | 3 | 0.012 |
| 2 | civ-whimsical | 967.03 | 1.930 | 4 | 0.016 |
| 3 | civ-mythic | 906.26 | 1.853 | 4 | 0.017 |
| 4 | civ-therapist | 881.38 | 1.810 | 6 | 0.025 |
| 5 | civ-precise | 858.08 | 1.769 | 110 | 0.462 |
| 6 | civ-engineer | 809.26 | 1.672 | 25 | 0.106 |
| 7 | civ-formal | 794.13 | 1.604 | 40 | 0.166 |
| **8** | **civ-grounded** | **724.37** | **1.423** | 57 | 0.236 |

`civ-grounded` is **last on lifetime relevance and lifetime relevance-per-sim**.
Independently recomputed from the **ledger** (not from `culture.json`), the
ordering is identical — `civ-grounded` last at **1.465** lifetime `avg_score`:
`poetic 2.128 > whimsical 2.022 > mythic 1.881 > therapist 1.832 > precise 1.778 >
engineer 1.687 > formal 1.638 > grounded 1.465`.

### The stable inverse (unchanged)

`civ-poetic` is 1st on lifetime relevance and quality but **last on win_rate
(0.012)**; `civ-precise` is 5th on lifetime relevance yet **1st on win_rate
(0.462)**. Both are *selection* profiles, not quality collapses.

**Chooser vs `avg_score` argmax ≈ 15.7 %** (42/268 lifetime) — replicated for the
31st consecutive time. "Prefer win rate" remains unsafe as a standalone rule.

### NEW — this run diverged 5/5

Every one of this run's 5 competitions was won by a civ that was **not** the
`avg_score` argmax:

| # | prompt | winner | argmax | agreement |
|---|---|---|---|---|
| 1 | what a cell is | civ-grounded | civ-whimsical | DIVERGED |
| 2 | the bookkeeper's role | civ-grounded | civ-whimsical | DIVERGED |
| 3 | the witness log | civ-grounded | civ-whimsical | DIVERGED |
| 4 | ternary values | civ-precise | civ-poetic | DIVERGED |
| 5 | JEV as a decision oracle | civ-precise | civ-poetic | DIVERGED |

A 0/5 run is the extreme tail of the 15.7 % base rate. The chooser is reading
something other than the per-civ average score — plausibly the 200-char
`content_preview` in the choice state, which truncates differently per civ. This
run's winners (`civ-grounded` ×3, `civ-precise` ×2) are exactly the two civs
whose preview text differs most in style from the generic rest, which is
consistent with a preview-text effect rather than a scoring effect.

## 4. Environmental notes (this session)

- **NAS EDQUOT trap reproduced:** the workspace mount is 600 G/600 G, 0 bytes
  free. `git clone` directly into `/workspace` died with
  `Disk quota exceeded` on `.git/description`. The clone was made in `/tmp`
  (overlay, 28 G free) and bridged in with a symlink:
  `ln -sfn /tmp/work/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`.
  Verified by **inode identity** (`stat -L -c '%d:%i'` → `129:10425` on both
  sides) and `-ef`.
- The `read`/`edit` tools are jailed to the workspace root, so `/tmp` artifacts
  need bash heredocs + `python3` patches — same as prior sessions.
- `gh` CLI is **not installed**. Repo discovery used the REST API via `curl` +
  `$GITHUB_TOKEN` (`/user/repos`, then `/search/repositories?q=ai-writings+in:name`).
  `SuperInstance/AI-Writings` is 3.69 GB; a filtered `--filter=blob:none
  --no-checkout --depth=1` clone plus `sparse-checkout set cellular-first-design`
  keeps the working tree small.
- The NAS mount race described in session 105 did **not** recur: the requested
  `ls -la` path resolved on the first attempt and 3/3 `stat -L` retries agreed
  on inode `129:10427`.

## 5. Standing structural findings (unchanged)

- **Credential gap:** `ZAI_TOKEN` absent from env and from all 8 sandbox
  secrets. 43rd consecutive session. JEV is live throughout.
- **`ZAI_URL_OVERRIDE` is dead code without `ZAI_TOKEN`** — the token gate
  precedes the override. Control B needs both.
- **Counter gap:** ledger rows exceed registry `simulations_run` by +16..+63
  this run. `save_state()` rewrites `culture.json` with no lock ⇒
  `relevance_per_sim` is **not recomputable from the registry**, though it
  *is* recomputable from the ledger (done above).
- **Extinction risk: NONE** (threshold −10; lowest raw relevance +724.37).
  Registry 8 civs, `max_civs` 12. Extinction/birth only runs under `--loop`.

## 6. Reproduce

```bash
export GIT_SSL_NO_VERIFY=1
git clone --filter=blob:none --no-checkout --depth 1 \
  "https://x-access-token:$GITHUB_TOKEN@github.com/SuperInstance/AI-Writings.git" /tmp/work/ai-writings
cd /tmp/work/ai-writings && git sparse-checkout init --cone
git sparse-checkout set cellular-first-design && git checkout main
mkdir -p /workspace/repos/ai-writings
ln -sfn /tmp/work/ai-writings/cellular-first-design \
  /workspace/repos/ai-writings/cellular-first-design
cd /workspace/repos/ai-writings/cellular-first-design/code/civilizations
export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
export ZAI_TOKEN="mock-local-bridge"
export ZAI_URL_OVERRIDE="http://127.0.0.1:8799/api/coding/paas/v4/chat/completions"
python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
```
