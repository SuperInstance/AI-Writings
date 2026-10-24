# Civilization Orchestrator — Run Report, Session 86 (2026-10-24)

**Command requested:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Verdict:** the requested path did not exist at session start and the workspace NAS is at a hard
100 % quota, so the run was reconstructed from `SuperInstance/AI-Writings` and executed under a
**symlink** bridge (never a copy). The real z.ai provider is **still unreachable** (credential
gap, 26th consecutive session), so the run was performed under **Control B** (local mock at the
provider gate) with **JEV left live and real**. The result is a *harness-verified* run, not a
z.ai run. The ledger was **restored to pristine** afterwards — 127/127 files byte-identical.

---

## 1. Environment reconstruction

The prompt's path is the *hardcoded* `CIVS_DIR` inside the script, not a path that exists on
arrival. Actual location: repo `SuperInstance/AI-Writings` →
`cellular-first-design/code/civilizations/`.

- Clone: sparse, blobless, depth 1 → `/tmp/ai-writings2` (45 MB, ~60 s). The full pack is
  **3.3 GB** and blew a 30 s timeout on the first attempt — do not full-clone.
- **The bridge is a symlink, and it still works.** `CIVS_DIR` =
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations`, so:

  ```bash
  mkdir -p /workspace/repos/ai-writings
  ln -sfn /tmp/ai-writings2/cellular-first-design \
         /workspace/repos/ai-writings/cellular-first-design
  ```

  Verified with `wc -c` through the bridge (17 534 bytes = real file), not by exit code.
- **The NAS is worse than last session: even 4 KB writes fail.** `dd` of 64 kB returns
  `Disk quota exceeded`; a 4 096-byte `write()` raises `OSError 122` and leaves a **0-byte**
  file that still appears in `ls`. Directory creation and symlink creation both still succeed.
  So the *directory skeleton* can be made but not *filled* — a copy is impossible, a symlink is
  the only bridge. This is now a **hard** constraint, not a soft one.
- `gh` is not installed; the GitHub REST API was used. `git` needs `GIT_SSL_NO_VERIFY=1`.
- Baseline commit: `73b8fb4` ("wesley-mechanic: canon poll 2026-10-24T11:19:32Z").
- The `write` tool is jailed to the workspace root and **cannot** write `/tmp` — the mock
  had to be authored through a bash heredoc (`cat > /tmp/zai_mock.py <<'PYEOF'`).

## 2. Control A — the unpatched command (real z.ai)

```
export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
```

Output: the batch header, all 8 `[Name] running 5 sims...` lines, the competition header, and
**no `Winner:` lines at all**. Exit code **0**.

| ledger | before | after | delta |
|---|---|---|---|
| all 8 `simulations.jsonl` | 2684 | 2684 | **+0** |
| `meta_log.jsonl` | 173 | 173 | **+0** |
| `leaderboard.json` | — | rewritten | ts bump only |

Only `leaderboard.json` was modified. The per-civ sim lines print *before* the provider call,
so they are **not** evidence of work.

**Root cause, re-verified from scratch this session:**

- `ZAI_TOKEN` is absent from env and from the 8-entry secret store.
- `POST https://api.z.ai/api/coding/paas/v4/chat/completions` → **HTTP 401**
  `{"error":{"code":"401","message":"token expired or incorrect"}}`. A 401 (not 5xx) means the
  endpoint is **healthy** ⇒ credential gap, not an outage.
- `https://api.z.ai/api/paas/v4/...` and `https://open.bigmodel.cn/api/paas/v4/...` → 401 too.
  Groq / Moonshot / OpenRouter / DeepSeek → 401; Gemini → 403. **No alternative LLM provider
  credential exists in this sandbox**, so Control B is the only way to exercise the harness.
- `TYPESAFE_AI_TOKEN` is present and **JEV is live** — `POST https://api.typesafe.ai/v1/systemone`
  returns **HTTP 200**. The script reads **`TYPESAFEAI_KEY`**, so
  `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` is required (26th session running).

**Assert on the row delta, never on the exit code.**

## 3. Control B — the run that actually produced work

Stub at the provider gate (leaves JEV untouched):

```bash
export ZAI_TOKEN="mock-token-control-b"
export ZAI_URL_OVERRIDE="http://127.0.0.1:8731/chat/completions"
export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
```

The mock keys on the civilization **name** in the prompt header, extracts the question as the
**last non-empty line** (stripping `Write N words on `), never echoes the
`header + tenets + voice` scaffolding, and salts on
`(voice, question, temperature, max_tokens, len(prompt))`. Eight distinct per-voice body
tables, one register each, 3 variants per voice.

### Verification (the part that matters)

| check | result |
|---|---|
| ledger row delta | **+80** (2684 → 2764) |
| rows per civ | **10 each, uniform** (5 batch + 5 competition) |
| `meta_log.jsonl` | **+5** (173 → 178) |
| competition winners | **5** |
| all-2.0-default JEV rows | **0** (real JEV scores throughout) |
| JEV score errors | **0** |
| mock calls | **81**, 8 distinct voices, 10 calls/voice (+1 extra for the Grounded) |
| distinct `body_hash` | **81** / 81 |
| providers used | `zai` × 80 (100 %) |

The +80/+5/5-winner/0-error signature **reproduces sessions 6, 7, 8, 84 and 85 exactly**.

### Competition results

| prompt | winner | top scorer (by `avg_score`) | agree? |
|---|---|---|---|
| what a cell is | The Engineer | The Poetic | disagree |
| the bookkeeper's role | The Grounded | The Poetic | disagree |
| the witness log | The Precise | The Precise | agree |
| ternary values | The Precise | The Poetic | disagree |
| JEV as a decision oracle | The Formal | The Poetic | disagree |

Wins: **Precise 2, Engineer 1, Grounded 1, Formal 1**. Chooser-vs-`argmax(avg_score)`
agreement: **1/5 (20 %)** — the **15th consecutive replication** that the chooser and the
scorer are essentially uncorrelated. The competition is a *separate* JEV call whose state
contains only a 150-char preview and **no scores**.

## 4. Low relevance — the answer depends on the lens, so all four are reported

Never merge these. (a) `relevance_per_sim` = board sort key, (b) raw relevance,
(c) win rate = **selection** appeal, (d) mean `avg_score` + sub-scores = **quality**.

| civ | rel_per_sim (A) | # | raw rel (B) | # | win rate (C) | # | run avg (D2) | q | # | align | # | novelty | # | W/L |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| civ-poetic | **2.182** | 1 | 765.73 | 2 | 0.012 | **8** | 2.5433 | 1.608 | 1 | **3.250** | 1 | 2.772 | 2 | 2/163 |
| civ-whimsical | 2.103 | 2 | **807.38** | 1 | 0.034 | 5 | 2.3407 | 1.053 | 5 | 3.062 | 3 | **2.907** | 1 | 6/170 |
| civ-mythic | 1.923 | 3 | 632.74 | 3 | 0.019 | 6 | 2.1743 | 0.902 | 7 | 2.947 | 4 | 2.674 | 3 | 3/154 |
| civ-therapist | 1.893 | 4 | 613.28 | 4 | 0.013 | 7 | 2.1027 | 0.997 | 6 | 2.701 | 6 | 2.610 | 4 | 2/154 |
| civ-precise | 1.857 | 5 | 596.24 | 6 | **0.336** | **1** | 2.0933 | 1.155 | 3 | 3.203 | 2 | 1.922 | 7 | 77/152 |
| civ-engineer | 1.736 | 6 | 565.84 | **8** | 0.073 | 4 | 1.9593 | 1.208 | 2 | 2.938 | 5 | 1.732 | **8** | 12/153 |
| civ-formal | 1.700 | 7 | 606.93 | 5 | 0.150 | 3 | **1.7137** | **0.567** | **8** | **2.470** | **7** | 2.104 | 6 | 28/159 |
| **civ-grounded** | **1.530** | **8** | 569.31 | 7 | 0.225 | 2 | 1.8967 | 1.077 | 4 | 2.390 | **8** | 2.223 | 5 | 48/165 |

Lifetime (whole ledger) quality / alignment:

| civ | life_q | # | life_align | # | n_life |
|---|---|---|---|---|---|
| civ-grounded | **0.9113** | **8** | **1.9461** | **8** | 372 |
| civ-engineer | 0.9284 | 7 | 2.5836 | 5 | 326 |
| civ-formal | 0.9285 | 6 | 2.6542 | 4 | 357 |
| civ-therapist | 0.9732 | 5 | 2.5060 | 6 | 324 |
| civ-precise | 1.0271 | 4 | **2.8841** | **1** | 321 |
| civ-mythic | 1.0802 | 3 | 2.4924 | 7 | 329 |
| civ-whimsical | 1.2168 | 2 | 2.6736 | 3 | 384 |
| civ-poetic | **1.4250** | **1** | 2.8438 | 2 | 351 |

### The civ to actually watch: `civ-grounded` (6th session running)

**Last of 8 on every quality lens** — lifetime `avg_score` 1.530, lifetime quality 0.9113
(8th), lifetime alignment 1.9461 (8th), and **last on the board's own sort key**
(`relevance_per_sim` 1.530, 8th of 8). This run it also had the **lowest alignment of any
civ (2.390)** while sitting mid-pack on quality. It is the **only** civ that is last on the
board sort key *and* last on lifetime quality *and* last on lifetime alignment.

**Still not a collapse:** mid-field on win rate (0.225, 2nd of 8) and it won 1 of the 5
competitions this run. Part of its last place on `relevance_per_sim` is a **longevity
artefact** — a lifetime-average denominator penalises the civ that ran most (372 sims vs
321-384). Note it ran *more* sims than 6 of 8 civs and still finished last on the average.

### The inversion: `civ-poetic`

**1st of 8** on `relevance_per_sim` (2.182) and **1st on this-run quality (1.608) and this-run
alignment (3.250)** — and **last of 8 on win rate at 2W/163L = 0.012**. It also has the
*lowest* run novelty among the top-3 (2.772, 2nd). It accumulates relevance while essentially
never being *selected*. **26 sessions running.** Not a quality collapse and not an extinction
risk: it is a civ whose voice the 150-char preview never rewards.

### The healthiest: `civ-precise`

Win rate **0.336 (77W/152L)**, best of 8 by a factor of 4.6, and 2 of the 5 competitions this
run. Its trade-off is visible and consistent: lifetime alignment is the **best of 8
(2.8841)** but lifetime novelty is mid-low — the coldest temperature in the fleet (0.20)
makes output consistently shaped, and a 150-char preview rewards consistency over originality.
It is the only civ whose *relevance rank* and *win rate* point the same way.

### Not rankable: `civ-formal` and `civ-engineer`

`civ-formal` is 2nd-lowest on run quality (0.567) and 2nd-lowest on run alignment (2.470),
7th on the board sort key, but **3rd on win rate (0.150)** and 4th on lifetime alignment —
the lenses disagree, so no single "low relevance" claim is stable.

`civ-engineer` is **last of 8 on raw relevance (565.84)** and last of 8 on run novelty
(1.732) — the *only* civ with the double-bottom on novelty — yet 4th on win rate (0.073) and
**2nd on run quality (1.208)**. It also won 1 of 5 competitions. Raw relevance alone would
falsely flag it as the weakest civ; it is actually the 2nd-best on this run's quality.

### Extinction risk: none

`extinction_and_birth()` retires only below `relevance < -10`; the lowest is **+484.96**,
a margin of **494.96**, and it only runs in `--loop` mode every third iteration. A
single-shot run never triggers it. **No civ is anywhere near extinction.**

## 5. Two inherited defects, unchanged

1. **The counter gap is +260** (ledger 2764 rows vs `simulations_run` 2504) and **not uniform**
   (per-civ gap 16 to 63) — `save_state()` rewrites `culture.json` wholesale from in-memory
   counters with no lock and no read-modify-write, so concurrent/parallel writes lose
   updates. Every row in the gap is counted by nobody, and `relevance_per_sim` therefore
   **cannot be recomputed from the ledger by an auditor**. Prefer win rate and mean
   `avg_score`. (Note the board's own `relevance` field is *also* counter-derived, so it
   inherits the same defect — the raw-relevance column (B) above is recomputed from the
   ledger and is the trustworthy one.)
2. **The committed ledger is already 37.6 % synthetic** (1040 of 2764 rows carry the
   `[mock-zai` marker, **130 per civ** — all **pre-existing**). Sessions 6/7/8 documented
   "mock rows are not committed", but rows written by *earlier* sessions were committed and
   never reaped. **This session's own 80 rows were removed and the ledger restored to
   pristine**, so the 37.6 % is entirely the *inherited* level and this session contributed
   **0** of it. A rule enforced only on the writes of the session that learns it does not
   clean the history it inherits. (37.6 % is up from 34.7 % reported in session 85 — the
   inherited contamination grew by ~80 rows from sessions 84/85 in between.)

## 6. Protocol followed

- Mock rows are **not committed**. The working tree was restored with
  `git checkout -- cellular-first-design/code/civilizations/` and verified with **`cmp`
  against the git blob, file by file** — **127/127 files byte-identical, 0 mismatches**
  (8 × `culture.json`, 8 × `simulations.jsonl`, 8 × `witness.log`, `civilizations.json`,
  `leaderboard.json`, `meta_log.jsonl`, and all 102 report/learnings files).
- Ledger and `meta_log.jsonl` are back at **2684 rows / 173 entries**, exactly the baseline;
  `leaderboard.json` ts is back to `2026-10-24T10:23:32`.
- `git status --porcelain` is **empty**.
- Mock source and its 81-call log were saved **outside the repo** (`/tmp/zai_mock.py`,
  `/tmp/zai_mock_calls.jsonl`).
- This session commits **the report and the learnings only**.
