# Civ Orchestrator — Run Report, session 237 (2026-10-25)

## Session 237 (2026-10-25) — provider path, baseline, and result

- **Command**: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
- Provider path: **Control B mock** (z.ai credential gap, **99th session**) + **live JEV** (`jev-1.14.0`).
- Baseline: `29f52fd` (session 236 tree), `refs/heads/main` asserted equal to the clone HEAD.
- **Pre-flight gate: 8/8 PASS** (first build). **Run verification: 20/20 PASS.**
- Result: winners **split 2-2-1** — `civ-precise` 2, `civ-engineer` 2, `civ-formal` 1. Chooser/argmax agreement **1/5 (20 %)** — 4 down-grades, 0 up-grades.
- Run low: **`civ-therapist`** (avg **1.6847**, fleet-low run alignment **1.2090** and fleet-low run quality **1.3480** — a two-axis collapse).
- Lifetime low: **`civ-grounded`** (**2177.29**, 99th consecutive session).
- Full detail: this report. The Control B mock source is session-local; the repo carries only the reports and the skill file that describe it.

## 1. The repo path in the task prompt is wrong — the upstream is `SuperInstance/AI-Writings`

The task named `/workspace/repos/ai-writings/cellular-first-design/code/civilizations/`. On a
fresh sandbox that path does not exist. The upstream repo is **`SuperInstance/AI-Writings`**
(public, `main`, 3.7 GB) — `ai-writings/cellular-first-design` 404s as a repo slug. The clone
was made **sparse** to `/tmp/aiw` (the `cellular-first-design/code/civilizations` cone only) and
bridged into the NAS with

```
mkdir -p /workspace/repos/ai-writings
ln -sfn /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design
```

`os.path.samefile()` -> `True` for the inner `code/civilizations` path.

## 2. The Control B seed algorithm was re-derived and verified **2000/2000** before the run

The canonical algorithm, verified against the **entire current-format ledger** (2000 rows, 250
per civ) rather than against this session's own fresh rows — a recompute that agrees with
your own fresh rows can be circular when the mock and the verifier share a mistake:

```
d      = md5(cultural_prompt).digest()
h      = d.hex()
i      = d[0] % 4
seed   = h[(i*2)%8 : (i*2)%8+4]
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"
```

**2000/2000 exact, 0 mismatches.** The 38 / 162 / 200 geometry also held: every current-format
preview is exactly 200 chars = 38-char header + 162-char tail.

The tail was **extracted byte-for-byte** from the ledger's dominant family (400 occurrences)
rather than reconstructed by hand, and the continuation solved as `target - 38 - 162` for a body
of **358** chars — inside the documented 332-369 band on the first build.

## 3. The **winner split 2-2-1** breaks a 19-session `civ-precise` sweep run

`civ-precise` had taken 5/5 in most recent sessions. This run it took **2/5**, with
`civ-engineer` also taking 2 and `civ-formal` taking 1. The `avg_score` argmax was
`civ-poetic` on **3 of 5** prompts — the same argmax pattern as session 231.

*Rule: a winner-streak is a description of history, not a prediction, and a 2-2-1 split is
evidence that the field is genuinely competitive rather than a measurement artefact.*

## 4. Agreement was **1/5 (20 %)** with **0 up-grades** — 21 sessions running

This continues the standing series. Up-grades remain **0** across the whole series. The
chooser reads only `content_preview[:150]` and never sees `avg_score` (structural — see the
session-231 note), so it **cannot** be expected to agree with the argmax; every disagreement
is a down-grade by construction.

All four down-grades were **marginal**: max delta **0.35** (witness log), the others
0.17 / 0.29 / 0.35. No cliff.

## 5. The run low was `civ-therapist` — a **two-axis** collapse — while `civ-grounded` holds the lifetime low

| rank | civ | avg | quality | novelty | alignment |
|---|---|---|---|---|---|
| 1 | `civ-poetic` | 2.5863 | 2.0590 | 2.5950 | 3.1050 |
| 2 | `civ-precise` | 2.5080 | 1.8240 | 2.4730 | 3.2270 |
| 3 | `civ-formal` | 2.4063 | 1.7580 | 2.4600 | 3.0010 |
| 4 | `civ-engineer` | 2.2690 | 1.6720 | 2.3920 | 2.7430 |
| 5 | `civ-grounded` | 2.1083 | 1.5350 | 2.4520 | 2.3380 |
| 6 | `civ-mythic` | 2.0673 | 1.7380 | 2.5030 | 1.9610 |
| 7 | `civ-whimsical` | 1.9390 | 1.5220 | 2.5750 | 1.7200 |
| 8 | `civ-therapist` | 1.6847 | 1.3480 | 2.4970 | 1.2090 |

`civ-therapist` took the run-level low (avg **1.6847**) with quality **1.3480** and alignment
**1.2090** both at the fleet low — a two-axis collapse — while novelty held at **2.4970**,
4th-highest of 8. `civ-grounded` held the **lifetime low for the 99th consecutive session**
(**2177.29**, `relevance_per_sim` **1.197**) and placed **4th of 8** on this run's `avg_score**
(**2.1083**) — the same split between the lifetime label and the run rank seen in sessions
231-235.

`civ-therapist` has now taken the run-level low in 5 of the last 6 sessions. The holder
rotation is still not a law.

## 6. The **alignment axis** dominated the spread again — **2.24x** the `avg_score` spread

| axis | spread | vs avg_score spread |
|---|---|---|
| alignment | 2.0180 | **2.24x** |
| quality | 0.7110 | 0.79x |
| novelty | 0.2030 | 0.23x |

`avg_score` spread was **0.9017**. The alignment axis again dominates the run's variance, the
same signature as sessions 225-230.

## 7. The lifetime leaderboard (post-run)

| rank | civ | relevance | per_sim | wins | losses | win_rate |
|---|---|---|---|---|---|---|
| 1 | `civ-poetic` | 3073.36 | 1.704 | 6 | 892 | 0.007 |
| 2 | `civ-precise` | 2949.43 | 1.643 | 624 | 269 | 0.699 |
| 3 | `civ-formal` | 2550.16 | 1.413 | 116 | 780 | 0.129 |
| 4 | `civ-whimsical` | 2547.28 | 1.407 | 5 | 893 | 0.006 |
| 5 | `civ-mythic` | 2500.71 | 1.390 | 10 | 882 | 0.011 |
| 6 | `civ-engineer` | 2436.35 | 1.358 | 57 | 834 | 0.064 |
| 7 | `civ-therapist` | 2199.67 | 1.224 | 11 | 884 | 0.012 |
| 8 | `civ-grounded` | 2177.29 | 1.197 | 75 | 822 | 0.084 |

**Extinction risk: NONE.** The floor is **-10**; the lowest civ sits at **2177.29** — 217x the
floor. `extinction_and_birth()` is only called under `--loop`, so this run neither retired nor
born a civ, and `civilizations.json` still lists the same 8 ids.

## 8. The competition winners

| # | prompt | winner id | name |
|---|---|---|---|
| 1 | Write 100 words on what a cell is. | `civ-precise` | The Precise |
| 2 | Write 100 words on the bookkeeper's role. | `civ-precise` | The Precise |
| 3 | Write 100 words on the witness log. | `civ-formal` | The Formal |
| 4 | Write 100 words on ternary values. | `civ-engineer` | The Engineer |
| 5 | Write 100 words on JEV as a decision oracle. | `civ-engineer` | The Engineer |

## 9. Verification: **20/20 PASS**

| # | assertion | result |
|---|---|---|
| 1 | all 8 civs gained **+10** ledger rows | PASS |
| 2 | **80** new rows total | PASS |
| 3 | all new rows `provider=zai` | PASS |
| 4 | all new rows carry the `[mock-zai ...]` header | PASS |
| 5 | all new previews exactly **200** chars | PASS |
| 6 | **0** JEV `error` keys in new rows | PASS |
| 7 | seed / colour / figure re-derive on all new rows | PASS (80/80) |
| 8 | `meta_log` **+5** (918 -> 923) | PASS |
| 9 | meta rows carry `winner_civ` | PASS |
| 10 | every civ played **5** competitions this run (d_wins + d_losses = 5) | PASS |
| 11 | `simulations_run` **+10** for every civ | PASS |
| 12 | `ts` monotonic in all 8 ledgers | PASS |
| 13 | `min(ts) <= meta.ts` for all 5 competitions (deltas +27.56 s) | PASS |
| 14 | relevance delta == sum of the 10 new `avg_score` | PASS |
| 15 | mock log **0** tracebacks / `EXC:` | PASS |
| 16 | orchestrator stdout `Winner:` lines = **5** | PASS |
| 17 | 1 distinct tail family in the new rows, all 162 chars | PASS |
| 18 | 40 distinct seeds across the 80 new rows | PASS |
| 19 | 89 mock requests served (80 sims + 5 competitions + 4 pre-flight) | PASS |
| 20 | JEV live, `jev-1.14.0`, HTTP 200 | PASS |

## 10. The counter gap is **byte-identical** to the documented values — fixed, not accumulating

| civ | relevance | ledger sum | gap | session 230 value |
|---|---|---|---|---|
| `civ-grounded` | 2177.2867 | 2261.6333 | **-84.3467** | -84.3500 |
| `civ-whimsical` | 2547.2800 | 2720.4233 | **-173.1433** | -173.1400 |
| `civ-formal` | 2550.1600 | 2635.6867 | **-85.5267** | -85.5300 |
| `civ-poetic` | 3073.3633 | 3170.1667 | **-96.8033** | -96.8000 |
| `civ-precise` | 2949.4333 | 2982.0667 | **-32.6333** | -32.6300 |
| `civ-mythic` | 2500.7133 | 2551.8233 | **-51.1100** | -51.1100 |
| `civ-therapist` | 2199.6667 | 2241.7800 | **-42.1133** | -42.1100 |
| `civ-engineer` | 2436.3500 | 2480.5933 | **-44.2433** | -44.2400 |

Max drift vs the documented values: **3.3e-03** (rounding in the published table). The offset is
**fixed** — neither repaired nor worsened by this run.

## 11. A **participation-count assertion** is only valid for the current run

`wins + losses` is **not** a multiple of 5 across the whole history: the totals are 891-898
because **35 historical competitions had fewer than 8 participants** (a `run_simulation`
returning `None` means that civ never gets a loss). This run's 5 competitions each had **8/8**
participants.

*Rule: assert the **delta** (`d_wins + d_losses == 5`) against the baseline commit, not the
absolute total, unless the participation count is known to be constant.*

## 12. `ZAI_TOKEN` is still absent — **99th session** — and `ZAI_URL_OVERRIDE` is dead code behind it

Real z.ai returns **HTTP 401** (endpoint healthy, credential absent). Control B needs **both**
`ZAI_TOKEN` (the gate) and `ZAI_URL_OVERRIDE` (the redirect); the override alone is unreachable
code. JEV is live via `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.

## 13. The NAS bridge needed a **stale-attribute-cache** retry after `ln -sfn`

Immediately after creating the symlink, `ls -la .../code/civilizations/` returned
*"No such file or directory"* while `ls -d` on the same path succeeded — an **NFS
attribute-cache** staleness artifact, not a broken link. `stat -L` confirmed the target was a
directory, and the listing succeeded on a later call with no change to the filesystem.

*Rule: on the NAS bridge, a one-shot "No such file or directory" immediately after creating a
symlink is **not** proof the link is broken. Verify with `stat -L` and `os.path.samefile()`,
and re-read before concluding the path is absent.*

## 14. A **sparse checkout still fetches the whole tree** unless the filter is applied at checkout

`git fetch --depth 1 origin main` with `core.sparseCheckout` set pulled the civilizations cone
only into the worktree, but the fetch itself was a full-tree shallow fetch. The clone was
still fast, but the durable rule stands: **fetch `refs/heads/main` explicitly** (a bare
`git fetch --depth 1 origin` resolves `refs/heads/HEAD`, a stale symref) and assert the SHA
matches the tree you expect.

## 15. Teardown

The mock was stopped by **exact-argv** match (`timeout -s KILL 900 python3 /tmp/mock_zai.py 8181`
and `python3 /tmp/mock_zai.py 8181` — two pids), never `pkill -f mock_zai` (self-match), and the
port was confirmed closed.
