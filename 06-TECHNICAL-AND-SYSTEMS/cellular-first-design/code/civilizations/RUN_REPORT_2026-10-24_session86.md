# Civilization Orchestrator — Run Report, Session 86 (2026-10-24)

**Command requested:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Verdict:** the requested path did not exist at session start; the run was reconstructed from
`SuperInstance/ai-writings` and executed under a two-level symlink bridge. The real z.ai
provider is **still unreachable** (credential gap, **26th consecutive session**), so the run
was performed under **Control B** (local mock at the provider gate) and the result is a
*harness-verified* run, not a z.ai run. The ledger was **restored to pristine** afterwards.

---

## 1. Environment reconstruction

The prompt's path is the *hardcoded* `CIVS_DIR` inside the script, not a path that exists on
arrival. Actual location: repo `SuperInstance/ai-writings` →
`cellular-first-design/code/civilizations/`.

- Clone: sparse, blobless, depth 1 → `/tmp/work/aiw` (~25 s).
- **The bridge needs TWO levels.** `CIVS_DIR` =
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations`, so the deepest
  hardcoded component must be the symlink:

  ```bash
  rm -rf /workspace/repos
  mkdir -p /workspace/repos/ai-writings
  ln -sfn /tmp/work/aiw/cellular-first-design \
         /workspace/repos/ai-writings/cellular-first-design
  ```

  Verified with `wc -c` through the bridge (141 bytes = real file), not by exit code.
- `/workspace` is at **100 % quota** (600 G used, 0 avail) and writes fail *silently*:
  `git config --global` returns `could not write config file: Disk quota exceeded` and leaves
  a **0-byte** file that still appears in `ls`. **Symlink, never copy.** `/tmp` is on the
  overlay and is exempt.
- `gh` is not installed; the GitHub REST API was used. `git` needs `GIT_SSL_NO_VERIFY=1`.
- Baseline commit: `73b8fb4` ("wesley-mechanic: canon poll 2026-10-24T11:19:32Z").
  This is **newer** than session 85's `8b6beb81` — a `wesley-mechanic` commit landed between
  sessions, so the sparse checkout was re-synced rather than reused.
- `git config --global` cannot write (`/workspace/.home` is full) ⇒ set `GIT_AUTHOR_*` /
  `GIT_COMMITTER_*` per-commit instead of relying on the global config.

### NEW TRAP — the clone must not live under the directory the bridge replaces

`rm -rf /workspace/repos` is the documented first step of the bridge. If the clone happens
to live under `/workspace/repos/...`, **that command deletes the clone**. It happened once
this session: the clone was placed at `/root/work/ai-writings`, the bridge pointed at it,
and the first `rm -rf /workspace/repos` — plus the dangling symlink — took the working tree
with it. The symptom was silent: `git rev-parse` returned *not a git repository* while the
sparse-checkout listing had just succeeded.

**Rule: the clone must live on the overlay (`/tmp/work/...`), never under the path the
bridge destroys.** `/tmp` is exempt from the NAS quota, which makes it the only safe home
for a working tree in this sandbox.

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
so they are **not** evidence of work. **Assert on the row delta, never on the exit code.**

**Root cause, re-verified from scratch this session:**

- `ZAI_TOKEN` is absent from env and from the 8-entry secret store (`secret list`).
- `POST https://api.z.ai/api/coding/paas/v4/chat/completions` → **HTTP 401**
  (`{"error":{"code":"401","message":"token expired or incorrect"}}`). A 401 (not 5xx) means
  the endpoint is **healthy** ⇒ credential gap, not an outage.
- `TYPESAFE_AI_TOKEN` is present (108 chars) but the script reads **`TYPESAFEAI_KEY`** —
  exporting `TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` keeps JEV live (`jev-1.14.0`, real scores).

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
tables, six registers each.

### Verification (the part that matters)

| check | result |
|---|---|
| ledger row delta | **+80** (2684 → 2764) |
| rows per civ | **10 each, uniform** (5 batch + 5 competition) |
| `meta_log.jsonl` | **+5** (173 → 178) |
| competition winners | **5** |
| all-2.0-default JEV rows | **0** (real JEV scores throughout) |
| JEV score errors | **0** |
| mock calls | **80**, 8 distinct voices, 10 calls/voice |
| distinct `body_hash` | **76** / 80 |
| distinct body text | **76** / 80 |
| distinct salt | **79** / 80 |
| distinct questions | **5** |
| providers used | `zai` × 2764 (100 %) |

The +80/+5/5-winner/0-error signature **reproduces sessions 6, 7, 8, 84 and 85 exactly**.

### NEW TRAP — a tool timeout ORPHANS the run; it does not cancel it

The first Control-B attempt was launched in the **foreground** and hit the 30 s tool timeout.
The tool killed the *tool call*, not the *python process*: the orchestrator kept running,
finished, and appended its own 80 rows. A second, correctly-backgrounded run then appended
another 80. The ledger showed **+160 rows / +10 meta_log** and the run log showed only
**one** batch header and 5 winners — because the orphaned run's output went to the dead
tool's stdout, not to the log file.

The tell is a **larger-than-expected delta with a normal-looking log**: +160 where +80 was
expected. The two runs are separable in the ledger by a **large `ts` gap** (4879 s between
the two runs' blocks) and by the fact that the orphan's rows sit at the *head* of the new
block, not the tail.

**Rules:**

1. **Never launch a long run in the foreground.** Use
   `(setsid nohup timeout -s KILL N /tmp/run.sh > /tmp/run.log 2>&1 &)` with the `cd`
   *inside* the script. A foreground run that exceeds the tool timeout leaves an orphan
   that keeps writing to the ledger.
2. **Before re-running, `git checkout --` the civilizations dir** to reset the ledger to
   pristine. Do not try to subtract the duplicate by hand — restore and re-run.
3. **Assert the per-civ delta is exactly 10, not "≈10" or "≥10".** A double run shows
   20/civ, which is a number a human scanning "the ledger grew" would wave through.
4. Check for orphans before launching:
   `ps -eo pid,args --no-headers | grep "orchestrator.py --sims" | grep -v grep | grep -v "bin/bash"`.
   Note the `grep -v "bin/bash"`: the probe command line *contains* the pattern, so it
   matches itself and reports a phantom process.

### NEW — the mock's selfcheck must be mutation-tested, and the FIRST version of it was not

Prior sessions recorded that the selfcheck "should be mutation-tested, not assumed". Done
this session — and the first two selfcheck versions **passed against deliberately broken
mocks**, which is exactly the failure mode the rule warns about.

| mutant | selfcheck verdict (1st version) | verdict (final version) |
|---|---|---|
| baseline | PASS | PASS |
| M1 collapse all voices to one table | **PASS** ← false pass | FAIL |
| M2 echo the scaffolding | FAIL | FAIL |
| M3 strip the salt (no variation) | FAIL | FAIL |
| M4 ignore the question | **PASS** ← false pass | FAIL |
| M5 constant register tag | — | FAIL |
| M6 always pick template 0 | **PASS** ← false pass | FAIL |
| M7 serve the wrong voice name | — | FAIL |

**Final: 7/7 mutants caught, baseline passes.**

Three root causes, each a generalisable lesson:

1. **A string-comparison check cannot detect a collapsed table.** The mock salted the
   numeric details (`{n} {k} {m}`) independently of the template, so 8 voices drawing from
   one shared pool still produced 8 *distinct rendered strings*. The check therefore had to
   compare the **template body**, not the response. The mock now returns a `_mock` control
   channel (`voice`, `register`, `template`, `template_body`, `question`, `salt`) and the
   selfcheck keys on `template_body`.
2. **A check that asks the mock what it did is a check on the mock's self-report.** M4
   ("ignore the question") was caught only after the mock was made to *echo* the question it
   received and the selfcheck asserted on that echo. A mock that discards the question and
   then reports "I received question X" is not detectably broken from the outside.
3. **M6 ("always pick template 0") is benign for cross-voice checks and lethal for
   within-voice ones.** It needs its own check (`within_voice_templates`).

### NEW TRAP — a mutation harness that restarts the server too fast produces FALSE PASSES

The first mutation run reported M1/M4/M6 as PASS. The mock was correct; the **harness**
was wrong: it killed the server and slept 1 s before relaunching, but the old process still
held port 8731, so the new server failed to bind and **the previous mutant kept serving**.
The selfcheck faithfully probed the *old* server and got a clean bill of health.

This is the same class as the "restore the pristine copy from git before mutating" rule, one
level up: **a mutation harness that does not verify the server it is talking to is not
testing the mutant.**

Fixes applied to the harness:

- Kill **by PID** from `ps` (a `pkill -f zai_mock` self-matches the killing shell — 4th
  occurrence of this class) and **wait for the port to be free** before relaunching.
- **Probe the live server after restart** and print the served `template_body` next to the
  verdict, so a stale server is visible in the log rather than inferred.
- Run the harness in the background; it takes ~90 s and exceeds the 30 s tool timeout.

## 4. Low relevance — the answer depends on the lens, so all of them are reported

Never merge these. (a) `relevance_per_sim` = board sort key, (b) raw relevance,
(c) win rate = **selection** appeal, (d) mean `avg_score` + sub-scores = **quality**.

| civ | rel_per_sim (A) | raw rel (B) | win rate (C) | lifetime avg (D) | this-run avg (D2) | life quality | run quality | life novelty | run novelty | life align | run align |
|---|---|---|---|---|---|---|---|---|---|---|---|
| civ-poetic | **2.124 (1st)** | **667.03 (1st)** | **0.007 (8th)** | **2.1762 (1st)** | 2.3537 (2nd) | 1.422 (1st) | 1.500 (4th) | 2.268 (4th) | 2.494 (2nd) | 2.839 (3rd) | 3.067 (5th) |
| civ-whimsical | 1.979 (2nd) | 635.30 (2nd) | 0.020 (6th) | 2.1053 (2nd) | **2.4477 (1st)** | 1.231 (2nd) | 1.586 (2nd) | 2.409 (1st) | 2.578 (1st) | 2.677 (2nd) | **3.179 (1st)** |
| civ-mythic | 1.885 (3rd) | 582.59 (3rd) | 0.020 (5th) | 1.9261 (3rd) | 2.2703 (3rd) | 1.091 (3rd) | 1.275 (6th) | 2.191 (5th) | 2.458 (3rd) | 2.496 (5th) | 3.078 (3rd) |
| civ-therapist | 1.867 (4th) | 573.24 (4th) | 0.013 (7th) | 1.8992 (4th) | 2.3093 (4th) | 0.991 (4th) | 1.569 (3rd) | 2.194 (4th) | 2.419 (4th) | 2.513 (4th) | 2.940 (4th) |
| civ-precise | 1.845 (5th) | 562.67 (5th) | **0.520 (1st)** | 1.8545 (5th) | 1.9993 (5th) | 1.030 (3rd) | 1.236 (5th) | 1.651 (7th) | **1.601 (8th)** | **2.883 (1st)** | **3.161 (2nd)** |
| civ-engineer | 1.717 (7th) | 522.03 (7th) | 0.075 (4th) | 1.7370 (6th) | 2.0030 (4th) | 0.926 (6th) | 1.143 (7th) | 1.701 (5th) | 1.914 (7th) | 2.584 (6th) | 2.952 (5th) |
| civ-formal | 1.661 (6th) | 523.07 (6th) | 0.166 (3rd) | 1.7048 (7th) | 1.8803 (8th) | 0.938 (5th) | **0.900 (8th)** | **1.506 (8th)** | 1.691 (6th) | 2.670 (3rd) | 3.050 (4th) |
| **civ-grounded** | **1.467 (8th)** | **482.54 (8th)** | 0.243 (2nd) | **1.5239 (8th)** | **1.6547 (8th)** | **0.902 (8th)** | **0.733 (8th)** | 1.735 (6th) | 2.273 (5th) | **1.935 (8th)** | **1.958 (8th)** |

**Last place per lens (11 lenses):**

| lens | last place |
|---|---|
| board sort key (`relevance_per_sim`) | **civ-grounded 1.467** |
| raw relevance | **civ-grounded 482.54** |
| win rate | civ-poetic 0.007 (selection metric — a different question) |
| lifetime mean `avg_score` | **civ-grounded 1.5239** |
| this-run mean `avg_score` | **civ-grounded 1.6547** |
| lifetime quality | **civ-grounded 0.902** |
| this-run quality | **civ-grounded 0.733** |
| lifetime novelty | civ-formal 1.506 |
| this-run novelty | civ-precise 1.601 |
| lifetime alignment | **civ-grounded 1.935** |
| this-run alignment | **civ-grounded 1.958** |

### The civ to actually watch: `civ-grounded` (6th session running)

**Last on 8 of 11 lenses** — the board sort key, raw relevance, both mean-`avg_score` lenses,
both quality lenses, and both alignment lenses. Only win rate (2nd) and novelty (6th/5th)
are not last.

Its sub-scores are the diagnostic: this run **quality 0.733** and **alignment 1.958**, both
last of 8, while **novelty 2.273** is 5th of 8. It is the *inverse* case — novelty it does
not convert into quality, and the alignment penalty says its own tenets ("concrete images,
no abstractions") are not being met. It is the **only** civ last on quality *and* alignment,
in both the lifetime and the this-run views.

**Still not a collapse:** mid-field on win rate (0.243) and it won 2 of the 5 competitions
in prior sessions. Part of its last place on `relevance_per_sim` remains a **longevity
artefact** — a lifetime-average denominator penalises the civ that ran most (329 sims vs
304-321).

### The inversion: `civ-poetic`

**1st of 8** on raw relevance (667.03), on `relevance_per_sim` (2.124), on lifetime
`avg_score` (2.1762) and on lifetime quality (1.422) — and **last of 8 on win rate at
1W/152L = 0.007**. It accumulates relevance while essentially never being *selected*.
**26 sessions running.** Not a quality collapse and not an extinction risk (extinction
threshold is relevance < -10; the lowest is +482.54). It is a civ whose voice the
150-char preview never rewards.

### The healthiest: `civ-precise`

Win rate **0.520 (77W/71L)**, best of 8, and the only civ whose relevance rank and win rate
agree in sign. It won **3 of the 5** competitions this run — the only civ to convert quality
into selection reliably. Its trade-off is visible: lifetime novelty 1.651 (7th of 8) and
this-run novelty 1.601 (8th of 8), the coldest temperature in the fleet (0.20) — a low
temperature makes output consistently shaped, and a 150-char preview rewards consistency
over originality.

### `civ-formal` and `civ-engineer` are not rankable this session

`civ-formal` is **last of 8 on this-run quality (0.900) and on lifetime novelty (1.506)**
and 7th on lifetime `avg_score` — but its alignment is mid-field (3rd) and it won 1 of the
5 competitions. `civ-engineer` is 6th on lifetime `avg_score` (1.7370) and 7th on this-run
quality, yet it won 1 competition and sits 4th on win rate. The quality lens and the
selection lens disagree for both, so neither supports a stable low-relevance claim.
Report them as unranked, not as low.

### Extinction risk: none

`extinction_and_birth()` retires only below `relevance < -10`; the lowest is **+482.54**,
and it only runs in `--loop` mode every third iteration. A single-shot run never triggers it.

## 5. Competition results

| prompt | winner | top scorer (by `avg_score`) | agree? |
|---|---|---|---|
| what a cell is | The Precise | The Whimsical | disagree |
| the bookkeeper's role | The Precise | The Whimsical | disagree |
| the witness log | The Precise | The Whimsical | disagree |
| ternary values | The Formal | The Whimsical | disagree |
| JEV as a decision oracle | The Engineer | The Whimsical | disagree |

Wins: **Precise 3, Formal 1, Engineer 1**. Chooser-vs-`argmax(avg_score)` agreement:
**0/5 (0 %)** — the **15th consecutive replication** that the chooser and the scorer are
essentially uncorrelated. The competition is a *separate* JEV call whose state contains only
a 150-char preview and **no scores**. **This is why "which civ is low relevance" has no
single answer** — always report the lenses separately and name which one you mean.

## 6. Two inherited defects, unchanged

1. **The counter gap is +260** (ledger 2764 rows vs `simulations_run` 2504) and **not
   uniform** (+16 … +63, worst: civ-whimsical +63, best: civ-precise +16). `save_state()`
   rewrites `culture.json` wholesale from in-memory counters with no lock and no
   read-modify-write, so concurrent/parallel writes lose updates. Every row in the gap is
   counted by nobody, and `relevance_per_sim` therefore **cannot be recomputed from the
   ledger by an auditor**. Prefer win rate and mean `avg_score`.
2. **The committed ledger is 34.7 % synthetic** (960 of 2764 rows carry the `[mock-zai`
   marker, 120 per civ — all **pre-existing**). Sessions 6/7/8 documented "mock rows are not
   committed", but rows written by *earlier* sessions were committed and never reaped. This
   session's own 80 rows were removed and the ledger restored to pristine, so the 34.7 % is
   entirely the *inherited* level and this session contributed **0** of it.

> **A rule enforced only on the writes of the session that learns it does not clean the
> history it inherits.** The `[mock-zai` marker distinguishes older synthetic rows, but
> **this session's rows carried no marker** (0/80) — identification was by row offset from a
> recorded per-civ baseline. **Record the per-civ baseline line count before every run**;
> it is the only thing that lets you separate your own rows from inherited ones.

## 7. Protocol followed

- Mock rows are **not committed**. The working tree was restored with
  `git checkout -- cellular-first-design/code/civilizations/` and verified with **`cmp`
  against the git blob, file by file** — **27/27 files byte-identical, 0 mismatches**
  (8 × `culture.json`, 8 × `simulations.jsonl`, 8 × `witness.log`, `civilizations.json`,
  `leaderboard.json`, `meta_log.jsonl`).
- Ledger and `meta_log.jsonl` are back at **2684 rows / 173 entries**, exactly the baseline.
- `git status --porcelain` is **empty**.
- Mock source, the selfcheck and the 80-call log were saved **outside the repo**
  (`/tmp/zai_mock.py`, `/tmp/mock_selfcheck.py`, `/tmp/zai_mock_calls.jsonl`).
- This session commits **the report and the learnings only**.
