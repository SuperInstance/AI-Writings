# civ-orchestrator — session 61 (2026-10-24)

**Command:** `civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Baseline HEAD:** `26fcb75` (session 60) — ledger **2284** rows, `meta_log` **148**
**Report file:** `RUN_REPORT_2026-10-24_session61.md` (checked for name collision against the remote before publishing)

---

## 1. Environment reconstruction

`/workspace` was wiped (only `.skills/`) and sits at **100 % NAS quota** (600 G used, 0 avail).
The task path `/workspace/repos/ai-writings/...` did not exist.

- Full `git clone --depth 50` → **failed** at 1.1 GB (`invalid index-pack output`) on the
  30 s tool timeout. A second detached attempt died the same way.
- **Working recipe:** `git clone --filter=blob:none --no-checkout --depth 30` (**1 MB, seconds**)
  followed by
  `git sparse-checkout set cellular-first-design/code/civilizations` + `git checkout`.
  The civ subtree is ~100 blobs; the rest of the monorepo is 3.3 GB of pack for nothing.
  This is cheaper than the API bootstrap **and** gives a real git history for push/verify.
- **Symlink bridge (innermost path — the session-55 rule, re-confirmed):**
  ```bash
  mkdir -p /workspace/repos/ai-writings/cellular-first-design/code
  ln -sfn /tmp/aw/cellular-first-design/code/civilizations \
          /workspace/repos/ai-writings/cellular-first-design/code/civilizations
  ```
  `CIVS_DIR` is hardcoded to the `/workspace` path, so the symlink is what makes the script
  write into the clone. `stat -c %i` gave **132349 on both sides** ⇒ same inode, not a copy.

## 2. The credential gap — 26th consecutive session

| probe | result |
|---|---|
| `api.z.ai/api/coding/paas/v4/chat/completions` (with `TYPESAFE_AI_TOKEN`) | **HTTP 401** |
| `api.github.com/user` (with `GITHUB_TOKEN`) | **HTTP 200** |
| `api.typesafe.ai/v1/systemone` (JEV) | **live** — `jev-1.14.0`, `quality 1.54`, `confidence 0.42` |

`ZAI_TOKEN` / `ZAI_KEY` absent from env **and** from the 8-entry secret store.
**401 (not 5xx) + a 200 from the same secret on a different endpoint ⇒ credential gap,
not an outage.** The key must be provisioned; it cannot be recovered from the environment.
Always `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` (the sandbox exports the latter,
the orchestrator reads the former, and nothing reconciles them).

## 3. Unpatched run — inert, exit 0 (26th replication)

```
=== Civilization batch: 8 civs x 5 sims each ===
[The Grounded] running 5 sims...      ... (all 8 civ lines present)
=== Civilization competitions: 5 prompts ===
(nothing)
exit: 0
```

| metric | before | after | delta |
|---|---|---|---|
| ledger rows | 2284 | 2284 | **+0** |
| `meta_log.jsonl` | 148 | 148 | **+0** |
| `Winner:` lines | — | — | **0** |
| registry `simulations_run` sum | 2024 | 2024 | **+0** |
| `leaderboard.json` | — | rewritten | (only file touched) |

**Assert on the row delta and the `Winner:` count, never on the exit code.** The per-civ
`[Name] running 5 sims...` lines are printed *before* the provider call and are not evidence of work.

**Session-58 correction re-confirmed:** the inert run left the registry counters at exactly
2024 → 2024 (+0). Session 57's claim that "an inert run advances `simulations_run` by 10/civ"
is **session-specific, not a property of an inert run** — `run_simulation()` returns `None`
on a failed call and `save_state()` writes back the *unchanged* in-memory counters.

## 4. Control B — 11th consecutive identical replication

`ZAI_TOKEN=<set>` + `ZAI_URL_OVERRIDE=http://127.0.0.1:8731/chat/completions`
(token gate left intact ⇒ a real HTTP request is genuinely attempted; the mock stands
**below** the failing line, so the control has full power).

| metric | value |
|---|---|
| ledger rows | 2284 → **2364 (+80, exactly +10/civ, uniform)** |
| `meta_log.jsonl` | 148 → **153 (+5)** |
| `Winner:` lines | **5** |
| all-2.0-default rows (JEV-outage signature) | **0** |
| rows with a score error | **0** |
| providers used | `zai` only (100 %) |
| distinct `content_preview` (full 200 chars) | **79/80** |
| cross-civ identical-preview collisions | **0** |
| distinct `avg_score` | 67/80, range 0.830–1.810, mean 1.3569 |
| JEV confidence | 0.340–0.990, mean 0.7784 |

### NEW SHAPE — the mock's salt can collide *within* one civ, and it is not a same-body defect

`civ-precise` showed **9 distinct previews for 10 rows** (all other civs 10/10). Cause,
traced to the row level: the temperature jitter is `preferred ± 0.2` **clamped at the 0.1
floor**, so two sims drew *exactly* `temperature=0.1000` with the same `max_tokens` and the
same prompt length. The mock's salt is `sha1(temperature|max_tokens|len(prompt))` ⇒ the
same salt ⇒ the same preview.

**The guard that matters is the cross-civ collision count, and it was 0.** A within-civ
duplicate is a *harness* artifact (the mock, not the orchestrator); a cross-civ duplicate
is a *signal-destroying* defect. **Assert the cross-civ count, and treat a within-civ
duplicate as a salt-collision to investigate — not as a same-body failure.**
Reusable fix for the mock: salt on `(temperature, max_tokens, len(prompt), civ)` **plus a
per-request counter**, so two identical param draws still differ.

### A shell trap that nearly produced a false negative

`cd <dir> && grep -c "ZAI_URL_OVERRIDE" file` returned **0** while the hook was plainly
present at lines 84–86. The `cd` was being lost inside the compound command, so `grep`
ran against a stale path. **Use absolute paths for every read in this project** — a
"missing hook" conclusion here would have invalidated the whole Control B plan.
(Re-confirmed with `grep -n` on the absolute path: the hook **is** present, exit 0.)

## 5. Low relevance — the Grounded is bottom on 8 of 16 lenses

| lens | lowest | value |
|---|---|---|
| A `relevance_per_sim` (board sort key) | `civ-grounded` | 1.491 |
| B raw relevance | `civ-grounded` | 416.02 |
| C win rate (selection appeal) | `civ-poetic` | 0.008 (1W/127L) |
| D lifetime `avg_score` | `civ-grounded` | 1.554 |
| D lifetime quality | `civ-engineer` | 0.960 |
| D lifetime novelty | `civ-formal` | 1.431 |
| D lifetime alignment | `civ-grounded` | 1.979 |
| E this-run avg | `civ-formal` | 1.080 |
| E this-run quality | `civ-formal` | 0.136 |
| E this-run novelty | `civ-formal` | 1.364 |
| E this-run alignment | `civ-grounded` | 1.340 |
| F de-contaminated lifetime avg | `civ-grounded` | 1.737 |
| F de-contaminated lifetime quality | `civ-engineer` | 1.190 |
| F de-contaminated lifetime alignment | `civ-grounded` | 2.314 |
| G ledger `avg_score` (all rows) | `civ-grounded` | 1.554 |

**Lowest-lens count: Grounded 8, Formal 4, Engineer 2, Poetic 1.**

| civ | A rel/sim | B raw rel | C win | D life | E run | F decon | rows | W-L | temp |
|---|---|---|---|---|---|---|---|---|---|
| `civ-poetic` | 2.140 | 565.02 | **0.008** | 2.199 | 1.658 | 2.354 | 301 | 1-127 | 0.80 |
| `civ-whimsical` | 1.987 | 538.52 | 0.023 | 2.131 | 1.188 | 2.329 | 334 | 3-125 | 0.95 |
| `civ-therapist` | 1.886 | 484.77 | 0.016 | 1.923 | 1.634 | 2.120 | 274 | 2-123 | 0.60 |
| `civ-mythic` | 1.879 | 486.56 | 0.025 | 1.927 | 1.308 | 2.108 | 279 | 3-119 | 0.85 |
| `civ-precise` | 1.831 | 467.02 | **0.528** | 1.844 | 1.439 | 1.955 | 271 | 65-58 | 0.20 |
| `civ-engineer` | 1.711 | 434.63 | 0.083 | 1.735 | 1.355 | 1.827 | 276 | 10-111 | 0.40 |
| `civ-formal` | 1.626 | 430.87 | 0.151 | 1.682 | **1.080** | 1.845 | 307 | 19-107 | 0.30 |
| `civ-grounded` | **1.491** | **416.02** | 0.244 | **1.554** | 1.192 | **1.737** | 322 | 31-96 | 0.50 |

### The three low-relevance civs, reported separately — never conflated

- **`civ-grounded` — the low-relevance civ.** Bottom on **A, B, D-avg, D-align, E-align,
  F-decon-avg, F-decon-align, G** simultaneously. **This is *not* a longevity artefact
  (session 57 falsified that):** `Pearson r(ledger_rows, rel_per_sim) = −0.095` (near zero),
  the most-run civ is `civ-whimsical` (334 rows) and the board-last civ is `civ-grounded`
  (322 rows) — a denominator effect cannot produce a last place for a civ that did not run
  most. It has the **2nd-highest win rate (0.244)** while producing the **lowest** scores:
  it wins on *selection appeal* and loses on *substance*. **Its voice is miscalibrated** —
  `voice_emphasis: "warm, factual"`, tenets `concrete images / everyday language /
  specific examples / no abstractions` — against the canon prompts it writes competent but
  tonally flat prose that JEV scores as *not aligned* (lowest lifetime alignment, 1.979).
- **`civ-formal` — the new E-bottom.** Bottom on all three this-run sub-scores
  (avg 1.080, quality 0.136, novelty 1.364). **E moves session to session; report it per
  run, never as a standing constant.**
- **`civ-poetic` — the 11th-consecutive-run mirror anomaly.** **1st of 8 on every quality
  lens** (A 2.140, B 565.02, D 2.199, F-decon 2.354) and **last on win rate (0.008, 1W/127L)**.
  The chooser sees only the **first 150 chars** of `content_preview` and **never sees the
  scores**, so `win_rate` measures *selection appeal*, not relevance.
- **`civ-precise` — healthiest.** 0.528 (65W/58L), the only civ whose relevance rank and
  win rate agree. **Lowest temperature (0.20).**
- **`civ-engineer` owns quality** (lifetime 0.960, de-contaminated 1.190, both lowest);
  **`civ-grounded` owns relevance.** Do not collapse the two — report the contested lens as contested.

### The chooser keeps preferring the low-temperature civs

Winners this run: **Precise ×2, Grounded ×2, Formal ×1.** The two lowest-temperature civs
(0.20 and 0.50) took **4 of 5 rounds**. `r(preferred_temp, lifetime novelty) = +0.9270`
(replicates the 0.93–0.99 band) — the quality lens rewards high temperature while the
chooser rewards terse, precise text. **The high-temperature, high-novelty civs accumulate
relevance while essentially never being selected.**

**Chooser vs `argmax(avg_score)`: 0/5 this run** (argmax picked `civ-poetic` on 4 of 5
prompts; the chooser picked it **zero** times). Lifetime: **27 agree / 126 disagree = 17.6 %**
— stable around 18 %, not the 4.4 % of the early small-sample runs.

## 6. Standing defects (unchanged, AST-confirmed)

1. **A JEV outage awards an arbitrary civ a legitimate win.** The fallback is
   `winner_civ = max(results, key=lambda r: r[1]["avg_score"])[0]` — on an all-`2.0` tie
   `max()` returns the **first** element encountered, with **no tie-break awareness**.
2. **The empty-token drop is silent.** `call_provider` returns `None` and the caller cannot
   distinguish "no credential" from "provider refused". A zero-usable-provider run exits 0.
   *This session reconfirmed the observable half of it: exit 0, +0 rows, 0 `Winner:` lines.*

## 7. Counter gap and contamination

- **Counter gap: ledger 2364 vs registry `simulations_run` 2104 = 260 uncounted rows**
  (unchanged from session 60's 260 — the run added 80 to the ledger *and* 80 to the
  counters, so the gap held steady). `save_state()` rewrites `culture.json` from in-memory
  counters with no lock and no read-modify-write ⇒ a lost-update race. `relevance_per_sim`
  is **not a reproducible ranking**; an auditor cannot recompute the board order from the
  ledger alone. **Prefer win rate, and always name the lens.**
- **Mock contamination: 720 / 2364 rows = 30.5 %** of the committed ledger is `[mock-zai`
  rows. **Every lifetime figure above (A, B, D, F, G) is computed over a ~30 % synthetic
  ledger.** The *ordering* is meaningful (stable across 11 sessions and 8+ lenses); the
  absolute numbers are **not** evidence of real model behaviour. **Fix at the source:** tag
  mock rows with `"mock": true` in the ledger so lifetime analytics can exclude them, and
  purge the 640 historical mock rows from HEAD. Until then, quote every lifetime number
  with this caveat.

## 8. No extinction

`extinction_and_birth()` is called **only** from the `--loop` branch, on `iter % 3 == 0`.
A single-shot `--sims 5 --prompts 5` run **cannot** mutate the registry, create a `civ-gen*`
directory, or retire anyone. Registry stayed at 8 civs. Lowest relevance **+416.02** against
a threshold of **−10** ⇒ a **426.02-point margin**. **Never report extinction/birth as a
risk of a one-shot run.**

## 9. Restore

All 8 `simulations.jsonl`, all 8 `culture.json`, `meta_log.jsonl`, `leaderboard.json` and
`civilizations.json` restored and verified **byte-identical to the HEAD blob** with the
materialised-blob `cmp` (the FIFO-race-free method): **19/19 identical, 0 differing**.
`git status --porcelain` **empty**. `__pycache__/` absent. Post-restore: **2284 ledger rows
/ 148 meta_log** = exact baseline.

**No source file modified.** Only run artifacts (restored) and this report.

## 10. Environment notes (new this session)

- **`--filter=blob:none --no-checkout` + `sparse-checkout` beats a full clone by 3 orders of
  magnitude** (1 MB + 100 blobs vs 3.3 GB). The full clone died twice at the 30 s timeout
  (`invalid index-pack output`); the blobless clone completed in one foreground call.
  **Try the cheap path first** — the API bootstrap (session 59/60) is the other cheap path.
- **`ls -la <dir> | grep simulations.jsonl` finds nothing** — the ledgers are one level down
  in `civ-*/simulations.jsonl`. Use `ls -la <dir>/civ-*/simulations.jsonl`.
- **The `cd` inside a compound command can be silently lost** in this sandbox, producing a
  **false "hook absent"** reading that would have invalidated the Control B plan. **Use
  absolute paths for every read.**
- The mock's launch still **hangs the tool call for its full timeout** when
  `setsid nohup ... &` shares a command with other work; the server was nonetheless up and
  served every request. **Launch in a dedicated call; probe in a separate call; check `ps`
  before concluding the server is down.**
