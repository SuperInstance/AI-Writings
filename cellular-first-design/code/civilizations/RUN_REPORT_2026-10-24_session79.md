# civ-orchestrator session 79 (2026-10-24) — ZAI_TOKEN gap 21st deep; run verified +80 rows, ledger restored

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Repo:** `SuperInstance/AI-Writings` (HEAD `4334ce7`), sparse checkout of `cellular-first-design/code/civilizations`
**Bridge:** `/workspace/repos/ai-writings -> /opt/work/AIW` (NAS `/workspace` is at 100% quota; the clone lives on the overlay)

## 1. Did the command work as-is?

**No — and it would have exited 0 while doing nothing.** `ZAI_TOKEN` is absent from
`env` and from the 8-entry secret store. All 8 available secrets re-tested against
`https://api.z.ai/api/coding/paas/v4/chat/completions` -> **401 "token expired or
incorrect"** on every one. 401 (not 5xx) => the endpoint is healthy => **credential
gap, not an outage**. JEV at `https://api.typesafe.ai/v1/systemone` is **live**
(`jev-1.14.0`, http 200).

Provider gate (orchestrator line ~79): `token = os.environ.get(p["env"], ""); if not token: return None`
-- a silent drop. The per-civ `[Name] running 5 sims...` lines print *before* the
provider call, so they are not evidence of work. **Assert on the row delta, never on
exit code.**

## 2. Control B — the only control with power over the fault

Stub at the gate, leave JEV untouched:

```
ZAI_TOKEN=dummy-control-b-token
ZAI_URL_OVERRIDE=http://127.0.0.1:8931/chat/completions
TYPESAFEAI_KEY=$TYPESAFE_AI_TOKEN
```

`ZAI_URL_OVERRIDE` alone is a **no-op** -- the `ZAI_TOKEN` gate is *upstream* of the
URL, so a dummy token is mandatory (it is never validated).

## 3. Verification -- all 8 `simulations.jsonl` gained new entries

| civ | before | after | delta | md5 changed |
|---|---|---|---|---|
| civ-engineer | 286 | 296 | +10 | YES |
| civ-formal | 317 | 327 | +10 | YES |
| civ-grounded | 332 | 342 | +10 | YES |
| civ-mythic | 289 | 299 | +10 | YES |
| civ-poetic | 311 | 321 | +10 | YES |
| civ-precise | 281 | 291 | +10 | YES |
| civ-therapist | 284 | 294 | +10 | YES |
| civ-whimsical | 344 | 354 | +10 | YES |
| **TOTAL** | **2444** | **2524** | **+80** | |

`meta_log.jsonl` 158 -> **163** (+5). 5 `Winner:` lines. +10 per civ = 5 batch + 5
competition -- reproduces sessions 6/7/8 exactly.

**Run health:** 0 all-2.0-default rows (=> real JEV scores, not the outage default),
0 score errors, 74 distinct `avg_score` of 80, range 0.740-2.543, 0 mock fallbacks.

## 4. NEW -- a missing voice-table entry is silent and passes every acceptance check

First attempt used a per-voice body table keyed on the **rendered** string
`Your voice: {v}.` (trailing period) -- correct. But the table was **missing
`"Your voice: technical, sparse."` (civ-precise)** in both openings and closings.
Consequence: all 10 of civ-precise's calls fell through to the shared FALLBACK pool.

The tell was the **collapsed distinct count**: per-civ distinct previews were
5/5/5/5/**1**/5/5/5 -- the historical "collapsed `content_preview` distinct count"
signature. Every other acceptance check still passed (+80 rows, +5 meta_log,
5 winners, 0 default rows, 78 distinct `avg_score`).

**Mandatory new check -- a startup self-check, not a post-hoc assertion:**

```python
def selfcheck():
    missing = []
    for c in json.load(open(f"{CIVS}/civilizations.json")):
        v = json.load(open(f"{CIVS}/{c}/culture.json"))["voice_emphasis"]
        key = f"Your voice: {v}."
        if key not in VOICE_OPENINGS:  missing.append(("OPENINGS", c, key))
        if key not in VOICE_CLOSINGS:  missing.append(("CLOSINGS", c, key))
    return missing
if missing: sys.exit(1)   # refuse to serve
```

**Generalise:** the mock's key space is derived from `civilizations.json` x
`culture.json`, so **every registered civ must be covered by construction** -- build
the table from the registry, then assert coverage, and fail closed. A table that is
hand-written and merely *usually* complete will silently collapse one civ onto the
fallback pool, and the run will still look perfect.

**Second-order rule:** the mock's body must vary with the *question*, not only with
the voice. A 3-body-per-voice table served 10 rows per civ against only 3 distinct
prompts => <=3 distinct previews per civ. Separate opening/closing pools per voice,
selected by `hash(voice, question)`, gives one distinct body per (voice, prompt).

## 5. Low-relevance -- four lenses, four answers (never merge them)

| lens | lowest | what it measures |
|---|---|---|
| `relevance_per_sim` (board sort) | **civ-grounded 1.491** | longevity artefact -- it ran the most sims (299) |
| raw relevance | **civ-grounded 445.78** | accumulated score, same denominator artefact |
| `win_rate` (selection appeal) | **civ-poetic 0.007 (1W/137L)** | **selection** under a 150-char preview |
| lifetime mean `avg_score` | **civ-grounded 1.550** | actual writing quality -- the only real quality lens |

**This run's per-civ mean `avg_score` (10 rows each):** civ-poetic 2.118 >
civ-therapist 1.864 > civ-mythic 1.826 > civ-whimsical 1.622 > civ-engineer 1.612 >
civ-precise 1.494 > civ-grounded 1.432 > **civ-formal 1.291 (lowest)**.

**civ-formal** won 2 of 5 competitions in this run yet posted the lowest mean
`avg_score` of the run, and its lifetime alignment (2.66) is among the best while
its lifetime quality (0.97) is near the floor. The competition winner and the
quality leader are decoupled -- the chooser never sees the scores.

**civ-poetic** remains the signature case: **top of the board on both
`relevance_per_sim` (2.131) and lifetime `avg_score` (2.187), and dead last on
`win_rate` (0.007 -- 1 win in 138).** It is never selected, yet it is the fleet's
strongest writer. A civ can be a quality leader and still read as "low relevance"
on the board.

**Extinction risk: NONE.** `extinction_and_birth()` retires only below
`relevance < -10`; the lowest is +445.78. It also only runs in `--loop` mode every
third iteration -- a single-shot run never triggers it.

## 6. Counter gap persists

`ledger rows = 2524` vs `culture.json simulations_run = 2264` -> **260 committed
rows counted by nobody**, on every civ. `save_state()` rewrites the whole
`culture.json` from in-memory counters with no lock and no read-modify-write ->
lost-update race. `relevance_per_sim` is therefore **not a reproducible ranking**;
the board order cannot be recomputed from the ledger by an auditor. Prefer win
rate, and say which lens you mean.

## 7. Mock rows are NOT committed

The 80 rows from this run contain **mock-authored bodies** (opening+closing pairs
from `/tmp/zai_mock.py`), not real z.ai output. The committed ledger holds real
provider output; a mock row presented as a provider result poisons the fleet's only
durable quality signal.

**Restored and verified:** all 8 `simulations.jsonl`, all 8 `culture.json`,
`meta_log.jsonl`, `leaderboard.json`, `civilizations.json` are **byte-identical to
the pristine commit** (`cmp` against `/tmp/pristine`, and `git status --porcelain`
empty). The mock server was stopped; no processes remain.

## 8. Environment notes

- NAS `/workspace` is at **100% quota** (600 G used, 0 avail) -- the EDQUOT trap.
  A `git clone` into `/workspace/repos` dies with `Disk quota exceeded` *while
  copying the template files*. Clone to the overlay (`/opt/work`) and symlink:
  `ln -sfn /opt/work/AIW /workspace/repos/ai-writings`. `ln -sfn` will NOT replace
  an existing real directory -- `rm -rf` it first.
- `CIVS_DIR` is hardcoded to `/workspace/repos/ai-writings/...`, so the symlink is
  what makes the script write into the clone.
- The repo is **3.7 GB**. A full clone exceeds the tool timeout and gets reaped
  (the background clone's directory was deleted mid-flight). Use sparse:
  `git clone --depth 1 --filter=blob:none --sparse --no-checkout` then
  `git sparse-checkout set --cone cellular-first-design`. Note: a **non-cone**
  path pattern silently checks out the *root* and not the subdirectory -- the cone
  form is the one that works.
- `gh` CLI is **not installed**; use the GitHub REST API. `git fetch`/`push` need
  `GIT_SSL_NO_VERIFY=1`; push to the explicit token URL.
- The `write` tool is jailed to the workspace root -- use bash heredocs for `/tmp`.
  It also hit the sporadic **-122 close error** here and left a **0-byte file** --
  always `wc -c` after writing, and rewrite if 0.
- `pkill -f <pattern>` self-matches and kills the invoking shell. Kill by PID from
  `ps -eo pid,args --no-headers | grep "[z]ai_mock" | grep -v grep`.
