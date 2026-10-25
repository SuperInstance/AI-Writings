# Civ Orchestrator — Run Report, session 167 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 51st session) + **live JEV**.
Baseline: `89ba62b` (session 166). **All 78 content checks PASS.**

## Environment recovery

The workspace was **empty** apart from `.plugin-cache` — the prompt's path
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
(**10th consecutive occurrence**).

- Upstream owner: **`SuperInstance/AI-Writings`**. Cloned to **`/tmp/cfd/aiw`**
  (overlay fs, 28 G free). Cloning into `/workspace` fails with `Disk quota exceeded`
  (NAS EDQUOT, total and size-independent) — **16th session**.
- Bridge: `ln -s /tmp/cfd/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`
  — the symlink points at the **clone root**, not the nested `cellular-first-design` dir.
  Verified by inode identity (**`129:12616` on both sides**) **and** `-ef` -> `EF_OK`.
  `ln -sfn` was not used against an existing directory (`rm -rf` first).
- `ZAI_TOKEN` absent from env and from the sandbox secrets; z.ai returns **401**
  `token expired or incorrect` => endpoint healthy, credential absent (**51st session**).
- **JEV live**: malformed `questions` -> **422** `dict_type` (payload-shape complaint => auth OK).
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code — the token gate returns `None` first).
- `gh` not installed (**18th session**) — used `GET /user/repos` with `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s => detached launch with stdout redirected
  **and** `< /dev/null`, then poll.

## Mock integrity (all four fixes re-applied)

| # | Fix | Session | Symptom if missing |
|---|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` | 112 | `ValueError` on `i>=4` => HTTP 500 **while the socket stays open** |
| b | `md5(whole_message)[:8]` | 118 | first 8 alnum chars are `YouAreA` for every civ => all 8 civs emit identical text |
| c | `Connection: close` + `Content-Length` | 144 | `curl` hangs to the tool timeout on a healthy server |
| d | interpolate the seed placeholder | 145 | every response carries literal `seed={}` => 1 distinct seed, not 40 |

Pre-flight on the **exact long cultural prompts** (lengths 167–209): 40 requests,
**40/40 distinct seeds**, **40/40 distinct previews**, every seed matched an
**independently recomputed** `md5(whole_message)[:8]`, **0** literal `seed={}`,
**0** `(civ,prompt)` carrying >1 seed, **0 tracebacks**.
Post-run mock log: **121** OK lines (40 pre-flight + 80 run + 1 health probe), **0 `EXC:`**.
Teardown: mock pid killed by exact argv match, 0 remaining procs, `curl` exit 7 (port closed).

## Verification — 78 checks, all PASS

| Check | Expected | Observed |
|---|---|---|
| per-civ ledger Δ | +10 × 8 | **+10 × 8** (1106/1137/1152/1109/1131/1101/1104/1164) |
| `meta_log.jsonl` Δ | +5 | **+5** (568 -> 573) |
| `Winner:` lines | 5 | **5** |
| `culture.json` `simulations_run` Δ | +10 × 8 | **+10 × 8** |
| `wins+losses` Δ | **+5 × 8** | **+5 × 8** (not +10 — see below) |
| per-civ `wins` = pre + (times won) | exact | **8/8 exact** (precise +3, formal +2, rest +0) |
| `losses` = pre + (5 − times won) | exact | **8/8 exact** |
| Σ `wins` across civs | 5 | **5** |
| `relevance` Δ = Σ this run's `avg_score` | exact | **8/8 exact to 1e-6** |
| `git status --porcelain` | 18 modified | **18** (8 ledgers + 8 cultures + meta_log + leaderboard) |
| new rows | 80 | **80** |
| rows with JEV `error` | 0 | **0** |
| 2.0/2.0/2.0 fallback triples | 0 | **0** |
| `provider` | zai only | **zai** |
| rows missing `[mock-zai seed=` prefix | 0 | **0** |
| distinct seeds | 40 / 80 rows | **40 / 80** |
| `(civ,prompt)` carrying >1 seed | 0 | **0** |
| sim→competition ts gap | 8/8 positive | **8/8** |
| 8/8 distinct previews per competition prompt | 5/5 | **5/5** |
| meta `results` = list of `[civ,score]` | 5/5 | **5/5** |
| meta vs ledger `avg_score` mismatches | 0 | **0** |
| competition-row prompt alignment | 0 | **0** (5/5 comps) |
| distinct `(q,n,a)` triples | ≥70 | **80/80** (see note) |
| confidence not the constant 0.5 | — | **varies 0.79–1.00** |
| leaderboard civ count | 8 | **8** |
| leaderboard sorted by `relevance_per_sim` desc | yes | **yes** |

### NOTE — `wins+losses` Δ is **+5 per civ**, not +10

Re-confirmed from source: `run_simulation()` appends a row and touches **no** win/loss
counter; `civilization_competition()` touches it once per prompt. Each civ therefore
appends **two** rows per batch (5 sim-phase + 5 competition-phase) => the *ledger* delta is
+10, but the **win/loss counter moves +5**. The correct per-civ expectation is
`wins += (times won)` and `losses += (5 − times won)`; all 8 civs reconcile exactly
against the git blob (precise +3w/+2l, formal +2w/+3l, the other six +0w/+5l).
A harness asserting a flat "+10 per civ" will fail against a **correct** run.

### NOTE — 80/80 distinct triples this session (not 79/80)

Last session produced 79/80 with one collision. This run: **80/80 distinct**
`(quality, novelty, alignment)` triples. The assertion should stay
`>= 70 distinct AND (2.0,2.0,2.0) not in triples` — a single collision at ~1/80 is a
live-JEV signature, not a fallback.

## Low-relevance civilization: **`civ-grounded` (The Grounded)** — 43rd consecutive session

**Lifetime (9 084 rows):**

| civ | n | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| civ-poetic | 1141 | 1.5446 | 0.7444 | 1.8496 | 2.0398 |
| civ-whimsical | 1174 | 1.3952 | 0.5919 | 1.9138 | 1.6798 |
| civ-precise | 1111 | 1.3860 | 0.5072 | 1.5442 | **2.1065** |
| civ-mythic | 1119 | 1.2496 | 0.5270 | 1.7004 | 1.5214 |
| civ-formal | 1147 | 1.1651 | 0.4483 | 1.3988 | 1.6483 |
| civ-therapist | 1114 | 1.1423 | 0.4579 | 1.7127 | 1.2564 |
| civ-engineer | 1116 | 1.1280 | 0.4485 | 1.4664 | 1.4692 |
| **civ-grounded** | 1162 | **0.9880** | **0.4109** | 1.4891 | **1.0638** |

Last of 8 on **avg_score**, **quality**, and **alignment**. Absolute gaps to the next civ
(`civ-engineer`): **alignment 0.4054** versus **quality 0.0376** => the alignment gap is
**10.8× wider** (last session: 5.2×). Alignment is the dimension the meta-GAN *selects* on
=> a **voice** failure, not a prose failure. Lifetime novelty 1.4891 is **6th of 8** — check
the rank, not the "above median" impression.

**Run-level (this run's 80 rows):** grounded **8th of 8** on `avg_score` (0.6163) — *last*,
ahead of nobody (run level 0.6163–0.9887 vs lifetime 0.9880–1.5446, a JEV level shift for
this batch, not a civ effect). Report the lifetime table as the structural signal and
the run ranking as the watch axis.

**Extinction risk: NONE.** Threshold −10; lowest raw relevance 1063.65 = **106×** above the
floor. Registry 8 civs, `max_civs` 12, all `generation=1`. Extinction/birth only runs
under `--loop`.

## Chooser vs `avg_score` argmax: 2/5 (40 %)

`civ-precise` won 3/5, `civ-formal` 2/5. In **3 of 5** the chooser took a **lower**-scoring
candidate (deltas −0.0400, −0.0267, −0.0833) => **14th consecutive session with the
"chooser picks lower" direction.** Mechanism (confirmed in source): the chooser is a JEV
**`choice`** question over 150-char `content_preview` snippets, while `avg_score` is the
mean of three **`score`** questions on the same text — different questions, different
answers. **Never treat `win_rate` as a quality metric.**

## Counter gap: NEGATIVE, and unchanged in magnitude — both epochs shown

`culture.json` `relevance_score` − ledger Σ`avg_score`:

| civ | blob gap | post-run gap | Δ |
|---|---|---|---|
| civ-whimsical | −173.1433 | −173.1433 | 0.0000 |
| civ-poetic | −96.8033 | −96.8033 | 0.0000 |
| civ-formal | −85.5267 | −85.5267 | 0.0000 |
| civ-grounded | −84.3467 | −84.3467 | 0.0000 |
| civ-mythic | −51.1100 | −51.1100 | 0.0000 |
| civ-engineer | −44.2433 | −44.2433 | 0.0000 |
| civ-therapist | −42.1133 | −42.1133 | 0.0000 |
| civ-precise | −32.6333 | −32.6333 | 0.0000 |
| **TOTAL** | **−609.9200** | **−609.9200** | **0.0000** |

Both columns are computed **within the same epoch** (blob `relevance` vs **blob** ledger
sum; post-run `culture.json` vs **working-tree** ledger sum) => the offset is **fixed**, not
accumulating. `save_state()` has no lock => `relevance_per_sim` is **not recomputable from
the ledger** by an auditor. Sign confirmed from the data, not copied from a prior report.

## Inverses and distinct axes

- **`civ-poetic`**: 1st on lifetime `avg_score` (1.5446), `quality` (0.7444) and
  `relevance` (1665.58), but **last on `win_rate` (0.011)** — won 0/5. A *selection*
  failure, not a quality collapse.
- **`civ-precise`**: best `win_rate` (0.580), **highest lifetime alignment (2.1065)**,
  1st on run `avg_score` (0.9887), won 3/5.
- **`civ-formal`**: the distinct low-**novelty** axis (1.3988, last of 8) — yet it won
  2/5 this run and has the **best run-level alignment (1.7580)**.
- Cross-civ spreads (this run): `novelty` **1.2180**, `quality` **0.5960**, `alignment`
  0.3723, `avg_score` 0.1830. Lifetime `avg_score` spread 0.5566.
- Run `quality` spread (0.5960) is **larger** than last session's collapsed 0.0430 —
  the quality axis was not collapsed this time.

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild from the
   RUNBOOK with **all four** fixes (112, 118, 144, 145) and run the pre-flight probe
   (40 distinct seeds AND 40 distinct previews AND independently recomputed md5s)
   **before** the batch. The pre-flight has now saved the run **six** times in the series.
2. `ZAI_TOKEN` still absent => real z.ai unusable; Control B is the only provider path.
   JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
3. Use the run-wide integrity checks (80 rows, 40 seeds, per-`(civ,prompt)` 1:1) and
   isolate this run's rows by **count from the end of each civ file** (last 10), never by
   a `ts` cutoff. `git show HEAD:<path>` must be run with `cwd` = the **clone root**
   (`/tmp/cfd/aiw`), not the civs directory — the civs dir is not a git root, and `git show`
   there returns empty stdout -> `JSONDecodeError`.
4. **Ledger row layout (this session's harness bug — worth stating once):** each civ's 10
   new rows are **5 sim-phase rows (idx 0–4)** then **5 competition rows (idx 5–9)**, one
   per competition prompt **in prompt order**. A check that grabs "the row for prompt P"
   by filtering on `prompt` alone will pick a *sim-phase* row and report a false
   `avg_score` mismatch; index by `5 + competition_index` instead. This produced 5 false
   FAILs in the first two harness drafts before the layout was confirmed against the data.
5. `civ-grounded` has been the low-relevance civ for **43** straight sessions. If a
   session ever finds it mid-table, that is a *finding* — check the run-wide seed count
   first to rule out a degenerate mock before believing it.
6. Tool timeout 30 s < orchestrator run ~28 s => detached launch with stdout redirected
   **and** `< /dev/null`, then poll `ps` + the log.
7. The NAS EDQUOT trap also blocks **file delivery** — `cp` into `/workspace` leaves a
   0-byte file. Deliver by pushing to git and citing the remote URL, not a workspace
   attachment.
8. **Symlink rule:** `ln -sfn` will not replace an existing directory target, and the
   bridge must point at the **clone root** (not the nested `cellular-first-design` dir).
   `rm -rf` the old link, then `ln -s`, then verify with `stat -L -c '%d:%i'` on both
   sides + `-ef`.

## Re-confirmations (this session)

- NAS EDQUOT total (16th session) — clone to `/tmp` (overlay), bridge the **clone root**,
  verify with `stat -L -c '%d:%i'` on both sides + `-ef`.
- z.ai **401** `token expired or incorrect` (credential gap, endpoint healthy) — **51st session**;
  JEV **422** on a malformed `questions` (payload-shape complaint => auth OK).
- `ZAI_URL_OVERRIDE` alone is **dead code** (the `ZAI_TOKEN` gate returns `None` first) —
  Control B needs **both**; `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s => detached launch with stdout redirected
  **and** `< /dev/null`.
- `gh` not installed (18th session) — `GET /user/repos` with `GITHUB_TOKEN`; the GitHub API
  is case-insensitive (`SuperInstance/ai-writings` == `SuperInstance/AI-Writings`).
- Pre-flight on the exact long cultural prompts (lengths 167–209): **40/40 distinct seeds,
  40/40 distinct previews, 40/40 independently recomputed md5s, 0 tracebacks**. The
  pre-flight has now saved the run **six** times in the series.
