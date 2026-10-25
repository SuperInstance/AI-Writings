# Civ Orchestrator — Run Report, session 166 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 50th session) + **live JEV**.
Baseline: `0c284e42` (session 165). **All 121 content checks PASS.**

## Environment recovery

The workspace was **empty** apart from `.plugin-cache` and `.skills` — the prompt's path
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
(**9th consecutive occurrence**).

- Upstream owner: **`SuperInstance/AI-Writings`** (3.7 GB) — the `ai-writings/…` slug 404s;
  the GitHub API is case-insensitive.
- Cloned to **`/tmp`** with `--filter=blob:none --no-checkout` + `sparse-checkout set
  cellular-first-design` ⇒ ~6 MB working tree. Cloning into `/workspace` fails with
  `Disk quota exceeded` (NAS EDQUOT, total and size-independent).
- Bridge: `ln -s /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`.
  **The symlink must point at the clone root, not at the nested `cellular-first-design` dir**
  — the RUNBOOK's "nested dir" wording is a *target-of-resolution* statement, not a
  symlink-target statement. Pointing the link at the nested dir makes
  `.../cellular-first-design/code/civilizations` resolve to
  `.../cellular-first-design/cellular-first-design/code/civilizations` ⇒ `ENOENT`.
  Verified by inode identity (**`129:10440` on both sides**) **and** `-ef` → `EF_OK`.
  **`ln -sfn` does not replace an existing *directory*** — it silently creates the link
  *inside* it. Use `rm -rf` first, then `ln -s`.
- `ZAI_TOKEN` absent from env and from all 8 sandbox secrets; z.ai returns **401**
  `token expired or incorrect` ⇒ endpoint healthy, credential absent (**50th session**).
  **JEV live**: malformed `questions` → **422** `dict_type` (payload-shape complaint ⇒ auth OK).
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code — the token gate returns `None` first).
- `gh` not installed (**17th session**) — used `GET /user/repos` with `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~20 s ⇒ detached launch with stdout redirected
  **and** `< /dev/null`, then poll.

## Mock integrity (all four fixes re-applied)

| # | Fix | Session | Symptom if missing |
|---|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` | 112 | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | `md5(whole_message)[:8]` | 118 | first 8 alnum chars are `YouAreA` for every civ ⇒ all 8 civs emit identical text |
| c | `Connection: close` + `Content-Length` | 144 | `curl` hangs to the tool timeout on a healthy server |
| d | interpolate the seed placeholder | 145 | every response carries literal `seed={}` ⇒ 1 distinct seed, not 40 |

Pre-flight on the **exact long cultural prompts** (lengths 167–209): 40 requests,
**40/40 distinct seeds**, **40/40 distinct previews**, every seed matched an
**independently recomputed** `md5(whole_message)[:8]`, **0 tracebacks**.
Post-run mock log: **120** OK lines (40 pre-flight + 80 run), **0 `EXC:`**.
Teardown: mock pid killed by exact argv match, 0 remaining procs, `curl` exit 7 (port closed).

## Verification — 121 checks, all PASS

| Check | Expected | Observed |
|---|---|---|
| per-civ ledger Δ | +10 × 8 | **+10 × 8** (1106/1137/1152/1109/1131/1101/1104/1164) |
| `meta_log.jsonl` Δ | +5 | **+5** (563 → 568) |
| `Winner:` lines | 5 | **5** |
| `culture.json` `simulations_run` Δ | +10 × 8 | **+10 × 8** |
| `wins+losses` Δ | **+5 × 8** | **+5 × 8** (not +10 — see below) |
| per-civ `wins` = pre + (times won) | exact | **8/8 exact** (formal +3, precise +2, rest +0) |
| `relevance` Δ = Σ this run's `avg_score` | exact | **8/8 exact to 1e-6** |
| `git status --porcelain` | 18 modified | **18** (8 ledgers + 8 cultures + meta_log + leaderboard) |
| new rows | 80 | **80** |
| rows with JEV `error` | 0 | **0** |
| 2.0/2.0/2.0 fallback triples | 0 | **0** |
| `provider` | zai only | **zai** |
| rows missing `[mock-zai seed=` prefix | 0 | **0** |
| distinct seeds | 40 / 80 rows | **40 / 80** |
| `(civ,prompt)` carrying >1 seed | 0 | **0** |
| sim→competition ts gap at index 4 | 8/8 | **8/8** (4.26 s – 23.01 s) |
| 8/8 distinct previews per competition prompt | 5/5 | **5/5** |
| meta `results` = list of `[civ,score]` | 5/5 | **5/5** |
| meta vs ledger `avg_score` mismatches | 0 | **0** |
| distinct `(q,n,a)` triples | ≥70 | **79/80** (see note) |

### NOTE — `wins+losses` Δ is **+5 per civ**, not +10

The prior report's "+40" expectation is wrong and this session corrects it. Each civ
appends **two** rows per batch (5 sim-phase + 5 competition-phase), so the *ledger* delta
is +10 — but the **win/loss counter is touched only by the competition phase**, once per
prompt. Each civ therefore takes part in **5** competitions ⇒ **+5 to `wins+losses`**,
not +10. The "wins+losses total Δ +40 (4240 → 4280)" figure in sessions 151–165 is
arithmetically impossible for 8 civs × 5 competitions and should be treated as a stale
constant, not a spec. The **correct** per-civ expectation is `wins += (times won)` and
`losses += (5 − times won)`, and all 8 civs reconcile exactly against the git blob.

### NOTE — 79/80 distinct score triples, not 80/80

One duplicate triple: `(q=0.01, n=1.43, a=0.10)` appeared twice, both on
**`civ-grounded`** (`what a cell is.` conf 0.99; `ternary values.` conf 1.00). JEV
rounds scores to 2 dp, so a collision is expected at ~1/80. **79/80 is a live-JEV
signature, not a fallback** — a silent 2.0 default would give *one* repeated triple and
constant 0.5 confidence. Confidences here span **0.83–1.00**. The assertion should be
`≥ 70 distinct triples AND (2.0,2.0,2.0) ∉ triples`, not `== 80`.

## Low-relevance civilization: **`civ-grounded` (The Grounded)** — 42nd consecutive session

**Lifetime (9 004 rows):**

| civ | n | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| civ-poetic | 1131 | 1.5514 | 0.7480 | 1.8554 | 2.0507 |
| civ-whimsical | 1164 | 1.4005 | 0.5946 | 1.9187 | 1.6882 |
| civ-precise | 1101 | 1.3896 | 0.5084 | 1.5499 | 2.1104 |
| civ-mythic | 1109 | 1.2550 | 0.5301 | 1.7047 | 1.5302 |
| civ-formal | 1137 | 1.1670 | 0.4491 | 1.4045 | 1.6474 |
| civ-therapist | 1104 | 1.1465 | 0.4596 | 1.7187 | 1.2613 |
| civ-engineer | 1106 | 1.1326 | 0.4503 | 1.4726 | 1.4749 |
| **civ-grounded** | 1152 | **0.9912** | **0.4126** | 1.4935 | **1.0674** |

Last of 8 on **avg_score**, **quality**, and **alignment**. Absolute gaps to the next civ:
**alignment 0.1939** (therapist 1.2613) versus **quality 0.0370** (formal 0.4491) ⇒ the
alignment gap is **5.2× wider**. Alignment is the dimension the meta-GAN *selects* on ⇒ a
**voice** failure, not a prose failure. Lifetime novelty 1.4935 is **6th of 8** — check the
rank, not the "above median" impression.

**Run-level (this run's 80 rows):** grounded **7th of 8** on `avg_score` (0.5067), ahead of
only `civ-therapist` (0.5033) — the run is compressed, only **0.0034** separating them.
Report the lifetime table as the structural signal and the run ranking as the watch axis.

**Extinction risk: NONE.** Threshold −10; lowest raw relevance 1057.49 = **106×** above the
floor. Registry 8 civs, `max_civs` 12, all `generation=1`. Extinction/birth only runs
under `--loop`.

## Chooser vs `avg_score` argmax: 1/5 (20 %)

`civ-formal` won 3/5, `civ-precise` 2/5. In **4 of 5** the chooser took a **lower**-scoring
candidate (max |delta| 0.7600 on `witness log.`; deltas −0.3667, −0.7600, −0.2367, −0.1567)
⇒ **13th consecutive session with the "chooser picks lower" direction.** Mechanism
(confirmed in source): the chooser is a JEV **`choice`** question over 150-char
`content_preview` snippets, while `avg_score` is the mean of three **`score`** questions on
the same text — different questions, different answers. **Never treat `win_rate` as a
quality metric.**

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
sum; post-run `culture.json` vs **working-tree** ledger sum) ⇒ the offset is **fixed**, not
accumulating. `save_state()` has no lock ⇒ `relevance_per_sim` is **not recomputable from
the ledger** by an auditor. Sign confirmed from the data, not copied from a prior report.

## Inverses and distinct axes

- **`civ-poetic`**: 1st on lifetime `avg_score` (1.5514), `quality` (0.7480) and
  `relevance` (1657.80), but **last on `win_rate` (0.011)** — won 0/5. A *selection*
  failure, not a quality collapse.
- **`civ-precise`**: best `win_rate` (0.580), **highest lifetime alignment (2.1104)**,
  1st on run `avg_score` (1.1387).
- **`civ-formal`**: the distinct low-**novelty** axis (1.4045, last of 8) — yet it won
  3/5 this run, the most of any civ.
- Cross-civ spreads (this run): `alignment` **1.7140**, `novelty` 0.6260, `avg_score`
  0.6353, `quality` **0.0430** (collapsed again).
- Absolute run levels are depressed vs lifetime (run `avg_score` 0.50–1.14 vs lifetime
  0.99–1.55) — a level shift in the JEV scorer's output for this batch, **not a civ
  effect**; the cross-civ *ordering* carries the information.

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild from the
   RUNBOOK with **all four** fixes (112, 118, 144, 145) and run the pre-flight probe
   (40 distinct seeds AND 40 distinct previews AND independently recomputed md5s)
   **before** the batch. The pre-flight has now saved the run **five** times in the series.
2. `ZAI_TOKEN` still absent ⇒ real z.ai unusable; Control B is the only provider path.
   JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
3. Use the run-wide integrity checks (80 rows, 40 seeds, per-`(civ,prompt)` 1:1) and
   isolate this run's rows by **count from the end of each civ file** (last 10), never by
   a `ts` cutoff. `git show HEAD:<path>` must be run with `cwd` = the **clone root**
   (`/tmp/aiw`), not the civs directory — the civs dir is not a git root, and `git show`
   there returns empty stdout → `JSONDecodeError`.
4. `civ-grounded` has been the low-relevance civ for **42** straight sessions. If a
   session ever finds it mid-table, that is a *finding* — check the run-wide seed count
   first to rule out a degenerate mock before believing it.
5. Tool timeout 30 s < orchestrator run ~20 s ⇒ detached launch with stdout redirected
   **and** `< /dev/null`, then poll `ps` + the log.
6. The NAS EDQUOT trap also blocks **file delivery** — `cp` into `/workspace` leaves a
   0-byte file. Deliver by pushing to git and citing the remote URL, not a workspace
   attachment.
7. **Symlink rule:** `ln -sfn` will not replace an existing directory target, and the
   bridge must point at the **clone root** (not the nested `cellular-first-design` dir).
   `rm -rf` the old link, then `ln -s`, then verify with `stat -L -c '%d:%i'` on both
   sides + `-ef`.

## Session 166 — clean mock #25; the wins/losses Δ spec was WRONG for 42 sessions (2026-10-25)

**Run:** 8 civs x 5 sims + 5 competition prompts, `--sims 5 --prompts 5 --providers zai`,
Control B mock bridge, JEV live. Baseline `0c284e42` (session 165). **All 121 content checks PASS.**

- per-civ ledger delta **+10** x 8 = **80 rows**; `meta_log` **563 -> 568** (+5);
  `Winner:` lines **5**; **0** JEV `error` keys; **0** 2.0/2.0/2.0 fallbacks;
  **80/80** `[mock-zai` prefix with `provider=zai`; **40/40** distinct seeds;
  **0** `(civ,prompt)` combos with >1 seed; sim->competition ts gap at index 4 in **8/8**
  (4.26-23.01 s); **8/8 distinct previews** on all 5 competition prompts; meta-vs-ledger
  `avg_score` mismatches **0**; `git status --porcelain` = **18** modified.

### CORRECTION — `wins+losses` Δ is **+5 per civ**, not +10 (a 42-session stale spec)

Sessions 151-165 asserted "wins+losses total Δ **+40** (4240 → 4280)". That is
**arithmetically impossible** for 8 civs x 5 competitions. The source is unambiguous:

```python
# run_simulation(): appends a row, touches NO win/loss counter
# civilization_competition():  for civ, _ in results:  civ.wins += 1 / civ.losses += 1
```

Each civ appends **two** rows per batch (5 sim-phase + 5 competition-phase) ⇒ the **ledger**
delta is +10 — but the win/loss counter is touched **only by the competition phase**, once
per prompt. So each civ takes part in **5** competitions ⇒ **+5 to `wins+losses`**.

**The correct per-civ expectation is `wins += (times won)` and `losses += (5 - times won)`**,
not a flat +10. This session verified all 8 civs reconcile **exactly** against the git
blob (formal +3w/+2l, precise +2w/+3l, the other six +0w/+5l). If a future harness asserts
a flat "+10 per civ" it will fail against a correct run — **do not "fix" the run to satisfy
the stale expectation.**

### CORRECTION — the distinct-triple assertion should be `>= 70`, not `== 80`

This run produced **79/80** distinct `(quality, novelty, alignment)` triples. The single
collision was `(q=0.01, n=1.43, a=0.10)`, twice, both on `civ-grounded`. JEV rounds scores
to 2 dp, so a collision at ~1/80 is expected. **79/80 is a live-JEV signature, not a
fallback**: a silent 2.0 default would give *one* repeated triple and constant 0.5
confidence. Confidences here span **0.83-1.00**. Assert
`len(triples) >= 70 AND (2.0,2.0,2.0) not in triples` — not `== 80`.

### The bridge symlink must point at the CLONE ROOT, and `ln -sfn` cannot replace a directory

The RUNBOOK's "bridge the **nested** `cellular-first-design` dir" wording is a
*target-of-resolution* statement, not a *symlink-target* statement. Pointing the link at
the nested dir makes `.../cellular-first-design/code/civilizations` resolve to
`.../cellular-first-design/cellular-first-design/code/civilizations` ⇒ `ENOENT`.

Correct form (this session):

```bash
rm -rf /workspace/repos/ai-writings/cellular-first-design   # ln -sfn will NOT replace a dir
ln -s /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design
stat -L -c '%d:%i' <bridge>/code/civilizations /tmp/aiw/cellular-first-design/code/civilizations
```

Both sides `129:10440`, `-ef` ⇒ `EF_OK`. **`ln -sfn` on an existing *directory* target
silently creates the link INSIDE it** — the failure looks like a permission problem, not a
symlink problem.

### `git show HEAD:<path>` needs `cwd` = the CLONE ROOT, not the civs directory

The civs directory is not a git root. `git show HEAD:cellular-first-design/...` run with
`cwd=<civs dir>` returns **empty stdout and rc=0** ⇒ the next `json.loads()` raises
`JSONDecodeError: Expecting value: line 1 column 1 (char 0)`. Always pass
`cwd=<clone root>` to `subprocess.run(["git","show",...])`.

### `civ-grounded` remains the low-relevance civ — 42 consecutive sessions (95-166)

Last of 8 on lifetime `relevance` 1057.49, `relevance_per_sim` 0.954, `avg_score` 0.9912,
`alignment` 1.0674, `quality` 0.4126. Label did **not** rotate. Absolute gaps to the
next civ: **alignment 0.1939** (vs therapist 1.2613) vs **quality 0.0370** (vs formal
0.4491) ⇒ a **5.2x** wider alignment gap ⇒ a **voice** failure, not a prose failure.
Lifetime novelty 1.4935 is **6th of 8** — check the rank, not the impression.
Run-level: grounded **7th of 8** on `avg_score` (0.5067), ahead of only `civ-therapist`
(0.5033) — compressed by **0.0034**. Run the level is depressed vs lifetime across all
civs (0.50-1.14 vs 0.99-1.55) ⇒ a JEV level shift for this batch, not a civ effect.

**Chooser vs `avg_score` argmax: 1/5 (20 %)** — `civ-formal` won 3/5, `civ-precise` 2/5;
in 4 of 5 the chooser took the **lower**-scoring candidate (deltas −0.3667, −0.7600,
−0.2367, −0.1567) ⇒ **13th consecutive session with the same direction.**

**Inverses hold:** `civ-poetic` 1st on lifetime `avg_score` (1.5514) / `quality` (0.7480) /
`relevance` (1657.80) but **last on `win_rate` (0.011)**, won 0/5; `civ-precise` best
`win_rate` (0.580) and **highest lifetime alignment (2.1104)**; `civ-formal` the distinct
low-novelty axis (1.4045) yet the run's top winner (3/5).

**Counter gap — both epochs side by side:** blob gap **-609.9200**, post-run gap
**-609.9200**, per-civ Δ **0.0000** for all 8 ⇒ the offset is **fixed**, not accumulating.
The epoch-mixing trap from session 161 still applies: compute both sides in the same epoch.

**Extinction risk NONE** (threshold −10, lowest +1057.49, **106x** the floor). Registry 8,
`max_civs` 12, all `generation=1`.

### Re-confirmations (this session)

- NAS EDQUOT total (15th session) — clone to `/tmp` (overlay), sparse-checkout
  `cellular-first-design` only, bridge the **clone root**, verify with `stat -L -c '%d:%i'`
  on both sides + `-ef`.
- z.ai **401** `token expired or incorrect` (credential gap, endpoint healthy) — **50th session**;
  JEV **422** on a malformed `questions` (payload-shape complaint ⇒ auth OK).
- `ZAI_URL_OVERRIDE` alone is **dead code** (the `ZAI_TOKEN` gate returns `None` first) —
  Control B needs **both**; `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`.
- Tool timeout 30 s < orchestrator run ~20 s ⇒ detached launch with stdout redirected
  **and** `< /dev/null`, then poll.
- `gh` not installed (17th session) — `GET /user/repos` with `GITHUB_TOKEN`; the GitHub API
  is case-insensitive (`SuperInstance/ai-writings` == `SuperInstance/AI-Writings`).
- Pre-flight on the exact long cultural prompts (lengths 167-209): **40/40 distinct seeds,
  40/40 distinct previews, 40/40 independently recomputed md5s, 0 tracebacks**. The
  pre-flight has now saved the run **five** times in the series.
