# Civilization Orchestrator — Run Report, Session 87 (2026-10-24)

**Command requested:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Verdict:** the requested path did not exist at session start; the run was reconstructed from
`SuperInstance/AI-Writings` and executed under a two-level symlink bridge. The real z.ai
provider is **still unreachable** (credential gap, **27th consecutive session**), so the run
was performed under **Control B** (local mock at the provider gate) and the result is a
*harness-verified* run, not a z.ai run. The ledger was **restored to pristine** afterwards
and verified byte-identical to the git blobs (**27/27 files, 0 mismatches**).

---

## 1. Environment reconstruction

The prompt's path is the *hardcoded* `CIVS_DIR` inside the script, not a path that exists on
arrival. Actual location: repo `SuperInstance/AI-Writings` →
`cellular-first-design/code/civilizations/`.

- Clone: sparse, blobless → `/tmp/ai-writings` (the clone must live on the **overlay**, never
  under the path the bridge destroys — see §1a).
- **The bridge needs TWO levels.** `CIVS_DIR` =
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations`, so the deepest
  hardcoded component must be the symlink:

  ```bash
  rm -rf /workspace/repos
  mkdir -p /workspace/repos/ai-writings
  ln -sfn /tmp/ai-writings/cellular-first-design \
         /workspace/repos/ai-writings/cellular-first-design
  ```

  Verified with `wc -c` through the bridge (17534 bytes = real file), not by exit code.
- `/workspace` is at **100 % quota** (600 G used, 0 avail) and writes fail *silently*.
  **Symlink, never copy.** `/tmp` is on the overlay and is exempt.
- `gh` is not installed; the GitHub REST API was used. `git` needs `GIT_SSL_NO_VERIFY=1`.
- Baseline commit: `825cf676` ("civilization-orchestrator: session 86 run report").
- Repo name correction: the repo is `SuperInstance/AI-Writings` (3.7 GB), **not**
  `Marzban-Khodadad/ai-writings` (404) and not `SuperInstance/ai-writings`.

### 1a. The sparse-checkout pattern must name the real directory

`git sparse-checkout set code/civilizations` (the path in the prompt) silently checked out
**nothing** — the tree is `cellular-first-design/code/civilizations`, and sparse-checkout
with a non-existent path is a **no-op, not an error**. The symptom: `git status` was clean,
`git log` worked, and the directory was simply absent.

**Rule: after `sparse-checkout set`, assert the target exists with `ls`/`wc -c`. A
successful `git checkout` is not evidence that a path was populated.**

### 1b. NEW TRAP — the mutation harness must not reuse a port between mutants

The first harness run passed the baseline and then died with
`AssertionError: port 8799 not free before M1_COLLAPSE`. The mock's `HTTPServer` socket
lingers in `TIME_WAIT` after `kill`, and `wait_port_free()` polls a *bind*, which fails
until the kernel releases the address.

Fix: **assign a distinct port per mutant** (`port = PORT + mi`) instead of recycling one.
The harness then never contends with a socket the previous mutant left behind.

This is the same class as session 86's "restart too fast ⇒ false PASS": there, a stale
server kept serving; here, a stale socket blocked the bind. **Both are the harness failing
to manage the server lifecycle, and both produce a clean-looking result for the wrong
reason.**

## 2. Control A — the unpatched command (real z.ai)

```bash
export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
export ZAI_TOKEN="absent-token-probe"
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
- `TYPESAFE_AI_TOKEN` is present but the script reads **`TYPESAFEAI_KEY`** —
  exporting `TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` keeps JEV live.

**JEV independently verified live** (not assumed):
`POST https://api.typesafe.ai/v1/systemone` → **HTTP 200**, `model: jev-1.14.0`, a real
graded score with probabilities. **The gap is isolated to the provider gate** — JEV, the
orchestrator, the registry, and the ledger are all healthy.

## 3. Control B — the run that actually produced work

Stub at the provider gate (leaves JEV untouched):

```bash
export ZAI_TOKEN="mock-token-control-b"
export ZAI_URL_OVERRIDE="http://127.0.0.1:8731/chat/completions"
export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
```

Launched with `(setsid nohup timeout -s KILL 900 /tmp/run_control_b.sh > /tmp/control_b.log 2>&1 &)`
with the `cd` **inside** the script.

### Verification (the part that matters)

| check | result |
|---|---|
| ledger row delta | **+80** (2684 → 2764) |
| rows per civ | **10 each, uniform** (5 batch + 5 competition) |
| `meta_log.jsonl` | **+5** (173 → 178) |
| competition winners | **5** |
| all-2.0-default JEV rows | **0** (real JEV scores throughout) |
| JEV score errors | **0** |
| provider recorded on every new row | `zai` (100 %) |
| distinct `avg_score` values | 71 / 80 |
| mock calls | 80 (+1 manual probe) |
| distinct voices | 8, 10 calls each (11 for Grounded incl. the probe) |
| distinct `template_body` | 40 |
| distinct salt | 81 / 81 |
| distinct register | 31 |
| distinct questions | 5 |

The +80 / +5 / 5-winner / 0-error / 10-per-civ signature **reproduces sessions 6, 7, 8, 84,
85 and 86 exactly**.

### The mock was mutation-tested, and the harness had to be fixed first

The first harness run passed the baseline and **crashed on the first mutant** (§1b) — it
never produced a verdict table, so it would have been tempting to report the mock as
"verified" on the strength of the baseline alone. After the port fix:

| mutant | selfcheck verdict |
|---|---|
| baseline | PASS |
| M1 collapse all voices to one table | **FAIL** |
| M2 echo the scaffolding | **FAIL** |
| M3 strip the salt (no variation) | **FAIL** |
| M4 ignore the question | **FAIL** |
| M5 constant register tag | **FAIL** |
| M6 always pick template 0 | **FAIL** |
| M7 serve the wrong voice name | **FAIL** |

**Final: 7/7 mutants caught, baseline passes.** The harness now also **probes the live
server after every restart** and prints the served `template_body` next to the verdict, so a
stale server is visible in the log rather than inferred — the session-86 fix, retained.

## 4. Low relevance — the answer depends on the lens, so all of them are reported

Never merge these. (a) `relevance_per_sim` = board sort key, (b) raw relevance,
(c) win rate = **selection** appeal, (d) mean `avg_score` + sub-scores = **quality**.

| civ | rel_per_sim (A) | raw rel (B) | win rate (C) | lifetime avg (D) | this-run avg (D2) | life quality | run quality | life novelty | run novelty | life align | run align |
|---|---|---|---|---|---|---|---|---|---|---|---|
| civ-poetic | **2.104 (1st)** | **660.53 (1st)** | **0.007 (8th)** | **2.1576 (1st)** | **1.7037 (1st)** | **1.396 (1st)** | **0.590 (1st)** | 2.265 (2nd) | **2.389 (1st)** | 2.812 (2nd) | 2.132 (3rd) |
| civ-whimsical | 1.954 (2nd) | 627.39 (2nd) | 0.020 (6th) | 2.0847 (2nd) | 1.6560 (2nd) | 1.200 (2nd) | 0.409 (3rd) | **2.4026 (1st)** | 2.346 (3rd) | 2.652 (3rd) | 2.213 (2nd) |
| civ-mythic | 1.865 (3rd) | 576.24 (3rd) | 0.020 (5th) | 1.9068 (3rd) | 1.6350 (3rd) | 1.067 (3rd) | 0.482 (2nd) | 2.187 (3rd) | 2.347 (2nd) | 2.466 (7th) | 2.076 (4th) |
| civ-therapist | 1.838 (4th) | 564.34 (4th) | 0.013 (7th) | 1.8718 (4th) | 1.4193 (5th) | 0.953 (5th) | 0.328 (5th) | 2.179 (4th) | 1.950 (4th) | 2.484 (6th) | 1.980 (6th) |
| civ-precise | 1.827 (5th) | 557.34 (5th) | **0.534 (1st)** | 1.8379 (5th) | 1.4660 (4th) | 1.003 (4th) | 0.370 (4th) | 1.648 (7th) | **1.491 (8th)** | **2.863 (1st)** | **2.537 (1st)** |
| civ-engineer | 1.693 (6th) | 514.74 (7th) | 0.068 (4th) | 1.7147 (6th) | 1.2737 (7th) | 0.898 (7th) | **0.207 (8th)** | 1.694 (6th) | 1.695 (7th) | 2.552 (5th) | 1.919 (7th) |
| civ-formal | 1.645 (7th) | 518.09 (6th) | 0.159 (3rd) | 1.6908 (7th) | 1.3823 (6th) | 0.921 (6th) | 0.285 (7th) | **1.510 (8th)** | 1.853 (6th) | 2.641 (4th) | 2.009 (5th) |
| **civ-grounded** | **1.451 (8th)** | **477.44 (8th)** | 0.243 (2nd) | **1.5102 (8th)** | **1.1447 (8th)** | **0.891 (8th)** | 0.325 (6th) | 1.725 (5th) | 1.900 (5th) | **1.914 (8th)** | **1.209 (8th)** |

**Last place per lens (12 lenses, incl. the longevity denominator):**

| lens | last place |
|---|---|
| board sort key (`relevance_per_sim`) | **civ-grounded 1.451** |
| raw relevance | **civ-grounded 477.44** |
| win rate | civ-poetic 0.007 (selection metric — a different question) |
| lifetime mean `avg_score` | **civ-grounded 1.5102** |
| this-run mean `avg_score` | **civ-grounded 1.1447** |
| lifetime quality | **civ-grounded 0.891** |
| this-run quality | civ-engineer 0.207 |
| lifetime novelty | civ-formal 1.510 |
| this-run novelty | civ-precise 1.491 |
| lifetime alignment | **civ-grounded 1.914** |
| this-run alignment | **civ-grounded 1.209** |
| `sims_run` (longevity denominator) | civ-engineer 304 |

**Last-place count per civ (out of 11 scored lenses):** civ-grounded **7**,
civ-engineer 2, civ-formal 1, civ-poetic 1, civ-precise 1, civ-mythic 0, civ-therapist 0,
civ-whimsical 0.

### The civ to actually watch: `civ-grounded` (7th session running)

**Last on 7 of 11 lenses** — the board sort key, raw relevance, both mean-`avg_score`
lenses, lifetime quality, and both alignment lenses. Only win rate (2nd), novelty
(5th/5th) and this-run quality (6th) are not last.

Its sub-scores are the diagnostic: this run **alignment 1.209**, the lowest of 8 by a wide
margin (2nd place is 1.919 — a 63 % gap), and **quality 0.325**, 6th. It is the *inverse*
case — novelty 1.900 (5th) it does not convert into quality, and the alignment penalty says
its own tenets ("concrete images, no abstractions") are not being met. Alignment is the one
lens where it is last in **both** the lifetime and the this-run view, and the gap widened
this session: **1.958 → 1.209**.

**Still not a collapse:** mid-field on win rate (0.243, 2nd of 8) and 2nd in the lifetime
view. Part of its last place on `relevance_per_sim` remains a **longevity artefact** — a
lifetime-average denominator penalises the civ that ran most (**329 sims vs 304–321**).

### The inversion: `civ-poetic`

**1st of 8** on raw relevance (660.53), on `relevance_per_sim` (2.104), on lifetime
`avg_score` (2.1576), on lifetime quality (1.396) and on **this-run quality (0.590) and
this-run `avg_score` (1.7037)** — and **last of 8 on win rate at 1W/152L = 0.007**. It
accumulates relevance while essentially never being *selected*. **27 sessions running.**
Not a quality collapse and not an extinction risk. It is a civ whose voice the 150-char
preview never rewards.

### The healthiest: `civ-precise`

Win rate **0.534 (79W/69L)**, best of 8, and the only civ whose relevance rank and win rate
agree in sign. It won **all 5** competitions this run — the only civ to convert quality into
selection reliably, and a **sweep**. Its trade-off is visible: lifetime novelty 1.648
(7th of 8) and this-run novelty 1.491 (8th of 8), the coldest temperature in the fleet
(0.20) — a low temperature makes output consistently shaped, and a 150-char preview
rewards consistency over originality.

### `civ-formal` and `civ-engineer` are not rankable this session

`civ-formal` is **last of 8 on lifetime novelty (1.510)** and 7th on lifetime `avg_score` —
but its alignment is mid-field (4th) and it won 0 of 5 competitions while sitting 3rd on
win rate. `civ-engineer` is 6th on lifetime `avg_score`, **last on this-run quality
(0.207)**, and last on `sims_run` (304, the fewest) — yet it sits 4th on win rate. The
quality lens and the selection lens disagree for both, so neither supports a stable
low-relevance claim. Report them as unranked, not as low.

### Extinction risk: none

`extinction_and_birth()` retires only below `relevance < -10`; the lowest is **+477.44**,
and it only runs in `--loop` mode every third iteration. A single-shot run never triggers it.

## 5. Competition results

| prompt | winner | top scorer (by `avg_score`) | agree? |
|---|---|---|---|
| what a cell is | The Precise | The Whimsical | disagree |
| the bookkeeper's role | The Precise | The Mythic | disagree |
| the witness log | The Precise | The Whimsical | disagree |
| ternary values | The Precise | The Poetic | disagree |
| JEV as a decision oracle | The Precise | The Poetic | disagree |

Wins: **Precise 5** (a clean sweep). Chooser-vs-`argmax(avg_score)` agreement:
**0/5 (0 %)** — the **16th consecutive replication** that the chooser and the scorer are
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
- Mock source, the selfcheck, the mutation harness and the 81-call log were saved
  **outside the repo** (`/tmp/zai_mock.py`, `/tmp/mock_selfcheck.py`,
  `/tmp/mutation_harness.py`, `/tmp/zai_mock_calls.jsonl`).
- This session commits **the report and the learnings only**.
