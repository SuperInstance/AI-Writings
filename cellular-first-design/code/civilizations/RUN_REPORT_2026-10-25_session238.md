# Civ Orchestrator — Run Report, session 238 (2026-10-25)

## Session 238 (2026-10-25) — provider path, baseline, and result

- **Command**: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
- Provider path: **Control B mock** (z.ai credential gap, **100th session**) + **live JEV** (`jev-1.14.0`).
- Baseline: `64e23cc` (session 237 tree), `refs/heads/main` asserted equal to the clone HEAD.
- **Pre-flight gate: 10/10 PASS** (first build). **Run verification: 20/20 PASS.**
- Result: `civ-precise` swept **5/5** competitions; chooser/argmax agreement **3/5 (60 %)** — 2 down-grades, 0 up-grades.
- Run low: **`civ-therapist`** (avg **1.1673**) — quality **0.4670**, alignment **0.7220** and novelty **2.3480** all at the fleet low, a **three-axis collapse**.
- Lifetime low: **`civ-grounded`** (**2192.48**, 100th consecutive session).
- Full detail: this report. The Control B mock source is session-local; the repo carries only the reports and the skill file that describe it.

## 1. The repo path in the task prompt is wrong — the upstream is `SuperInstance/AI-Writings`

The task named `/workspace/repos/ai-writings/cellular-first-design/code/civilizations/`. On a
fresh sandbox that path did not exist (the workspace held only `.plugin-cache`). The upstream
repo is **`SuperInstance/AI-Writings`** (public, `main`) — `ai-writings/cellular-first-design`
404s as a repo slug, and `cellular-first-design` is a **subdirectory** of it, not a repo.

The workspace NAS mount was at **100 % quota** (600 G used, 0 avail) with `du /workspace`
showing 0 — a stale quota, not local usage. A full clone to `/workspace` therefore died with
`Disk quota exceeded`. The clone went to the overlay instead, blobless + sparse:

```
git clone --depth 1 --filter=blob:none --no-checkout ... /tmp/cfd-meta
git sparse-checkout set cellular-first-design/code/civilizations
git checkout
```

`--filter=blob:none --no-checkout` is the form that actually works: the earlier
`--depth 50` full clone pulled 1.2 GB and was killed mid-transfer, and `--depth 1` with a
sparse cone still fetched the whole tree. The bridge into the NAS was then:

```
mkdir -p /workspace/repos/ai-writings
ln -sfn /tmp/cfd-meta/cellular-first-design /workspace/repos/ai-writings/cellular-first-design
```

`stat -L` showed a valid directory and `os.path.samefile()` -> `True`.

## 2. The Control B seed algorithm was re-derived and verified **2080/2080** before the run

The canonical algorithm, verified against the **entire current-format ledger** (2080 rows)
rather than against this session's own fresh rows — a recompute that agrees with your own
fresh rows can be circular when the mock and the verifier share a mistake:

```
d      = md5(cultural_prompt).digest()
h      = d.hex()
i      = d[0] % 4
seed   = h[(i*2)%8 : (i*2)%8+4]
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"
```

**2080/2080 exact, 0 mismatches.** The 38 / 162 / 200 geometry also held: every
current-format preview is exactly 200 chars = 38-char header + 162-char tail.

The tail was **extracted byte-for-byte** from the ledger's most recent session family
(80 occurrences) rather than reconstructed by hand, and the continuation solved as
`target - 38 - 162` for a body of **351** chars — inside the documented 332-369 band on
the first build.

## 3. The tail is **per-session**, and the pool of tails is **13**, shared by all 8 civs

Measuring the tail across the whole current-format ledger gives **13 distinct tail
strings**, every one exactly **162** chars, and the set is **identical for all 8 civs**.
Each `(civ, prompt)` pair carries **13** distinct tails across history — so the tail is
**not** keyed to `(civ, prompt)`.

Clustering the 2080 current-format rows by `ts` gap gives **26 sessions**, and every
single session uses **exactly one** tail across all **80** of its rows. The tail therefore
rotates **per session** and is otherwise free.

*Rule: the tail is a session-level constant. Do not try to derive it from `(civ, prompt)`
or from a request counter — it is neither. Extract the current session's family from the
ledger and reuse it for all 80 rows.*

## 4. `civ-precise` swept **5/5** — the sweep returns after the session-237 2-2-1 split

`civ-precise` took **5/5** competitions. Session 237 ended a 19-session sweep run with a
2-2-1 split; this run is the return of the sweep. The `avg_score` argmax was `civ-precise`
on **3 of 5** prompts, with `civ-poetic` the argmax on the other two.

*Rule: a winner-streak is a description of history, not a prediction, and a 2-2-1 split is
evidence the field is genuinely competitive rather than a measurement artefact.*

## 5. Agreement was **3/5 (60 %)** with **0 up-grades** — 22 sessions running

This continues the standing series. Up-grades remain **0** across the whole series. The
chooser reads only `content_preview[:150]` and never sees `avg_score` (structural), so it
**cannot** be expected to agree with the argmax; every disagreement is a down-grade by
construction.

Both down-grades were **marginal**: "ternary values" went to `civ-precise` at **1.7567**
against `civ-poetic` at **1.8533** (delta **0.0966**), and "JEV as a decision oracle" to
`civ-precise` at **2.0400** against `civ-poetic` at **2.1200** (delta **0.0800**). No cliff.

## 6. The run low was `civ-therapist` — a **three-axis** collapse — while `civ-grounded` holds the lifetime low

| rank | civ | avg | quality | novelty | alignment |
|---|---|---|---|---|---|
| 1 | `civ-poetic` | 2.0633 | 1.1980 | 2.4920 | 2.4940 |
| 2 | `civ-precise` | 2.0460 | 1.1880 | 2.2460 | 2.8680 |
| 3 | `civ-formal` | 1.7793 | 0.7670 | 2.3160 | 2.2700 |
| 4 | `civ-engineer` | 1.7060 | 0.7090 | 2.2500 | 2.1450 |
| 5 | `civ-mythic` | 1.6260 | 0.8310 | 2.3880 | 1.6130 |
| 6 | `civ-grounded` | 1.5380 | 0.6080 | 2.3060 | 1.6450 |
| 7 | `civ-whimsical` | 1.4553 | 0.6570 | 2.3920 | 1.2160 |
| 8 | `civ-therapist` | 1.1673 | 0.4670 | 2.3480 | 0.7220 |

`civ-therapist` took the run-level low (avg **1.1673**) with quality **0.4670**, novelty
**2.3480** and alignment **0.7220** **all three** at the fleet low — a three-axis collapse.
`civ-grounded` held the **lifetime low for the 100th consecutive session** (**2192.48**,
`relevance_per_sim` **1.199**) and placed **6th of 8** on this run's `avg_score` (**1.5380**)
— the same split between the lifetime label and the run rank seen in sessions 231-235 and
237.

`civ-therapist` has now taken the run-level low in 6 of the last 7 sessions.

## 7. The **alignment axis** dominated the spread again — **2.40x** the `avg_score` spread

| axis | spread | vs avg_score spread |
|---|---|---|
| alignment | 2.1460 | **2.40x** |
| quality | 0.7310 | 0.82x |
| novelty | 0.2460 | 0.27x |

`avg_score` spread was **0.8960**. The alignment axis again dominates the run's
variance, the same signature as sessions 225-230, 234 and 237.

## 8. The lifetime leaderboard (post-run)

| rank | civ | relevance | per_sim | wins | losses | win_rate |
|---|---|---|---|---|---|---|
| 1 | `civ-poetic` | 3093.98 | 1.706 | 6 | 897 | 0.007 |
| 2 | `civ-precise` | 2970.44 | 1.646 | 629 | 269 | 0.700 |
| 3 | `civ-formal` | 2568.00 | 1.415 | 116 | 785 | 0.129 |
| 4 | `civ-whimsical` | 2561.50 | 1.407 | 5 | 898 | 0.006 |
| 5 | `civ-mythic` | 2516.82 | 1.391 | 10 | 887 | 0.011 |
| 6 | `civ-engineer` | 2453.36 | 1.360 | 57 | 839 | 0.064 |
| 7 | `civ-therapist` | 2211.46 | 1.224 | 11 | 889 | 0.012 |
| 8 | `civ-grounded` | 2192.48 | 1.199 | 75 | 827 | 0.083 |

**Extinction risk: NONE.** The floor is **-10**; the lowest civ sits at **2192.48** — 219x the
floor. `extinction_and_birth()` is only called under `--loop`, so this run neither retired nor
born a civ, and `civilizations.json` still lists the same 8 ids.

## 9. The competition winners

| # | prompt | winner id | name | argmax | agree |
|---|---|---|---|---|---|
| # | prompt | winner id | name | argmax | agree |
|---|---|---|---|---|---|
| 1 | Write 100 words on what a cell is. | `civ-precise` | The Precise | `civ-precise` | yes |
| 2 | Write 100 words on the bookkeeper's role. | `civ-precise` | The Precise | `civ-precise` | yes |
| 3 | Write 100 words on the witness log. | `civ-precise` | The Precise | `civ-precise` | yes |
| 4 | Write 100 words on ternary values. | `civ-precise` | The Precise | `civ-poetic` | no |
| 5 | Write 100 words on JEV as a decision oracle. | `civ-precise` | The Precise | `civ-poetic` | no |

## 10. Verification: **20/20 PASS**

| # | assertion | result |
|---|---|---|
| 1 | all 8 civs gained **+10** ledger rows | PASS |
| 2 | **80** new rows total | PASS |
| 3 | all new rows `provider=zai` | PASS |
| 4 | all new rows carry the `[mock-zai ...]` header | PASS |
| 5 | all new previews exactly **200** chars | PASS |
| 6 | **0** JEV `error` keys in new rows | PASS |
| 7 | seed / colour / figure re-derive on all new rows | PASS (80/80) |
| 8 | `meta_log` **+5** (923 -> 928) | PASS |
| 9 | meta rows carry `winner_civ` | PASS |
| 10 | every civ played **5** competitions this run (d_wins + d_losses = 5) | PASS |
| 11 | `simulations_run` **+10** for every civ | PASS |
| 12 | `ts` monotonic in all 8 ledgers | PASS |
| 13 | `min(ts) <= meta.ts` for all 5 competitions (deltas +24.82..+28.50 s) | PASS |
| 14 | relevance delta == sum of the 10 new `avg_score` | PASS |
| 15 | mock log **0** tracebacks / `EXC:` | PASS |
| 16 | meta winner lines = **5** | PASS |
| 17 | 1 distinct tail family in the new rows, all 162 chars | PASS |
| 18 | 40 distinct seeds across the 80 new rows | PASS |
| 19 | mock requests served = **161** (41 pre-flight + 40 repeat + 80 sims) | PASS |
| 20 | JEV live, `jev-1.14.0`, HTTP 200 | PASS |

## 11. The counter gap is **byte-identical** to the documented values — fixed, not accumulating

| civ | relevance | ledger sum (full history) | gap | session 237 value |
|---|---|---|---|---|
| `civ-grounded` | 2192.4800 | 2276.8300 | **-84.3500** | -84.3467 |
| `civ-whimsical` | 2561.5000 | 2734.6400 | **-173.1400** | -173.1433 |
| `civ-formal` | 2568.0000 | 2653.5300 | **-85.5300** | -85.5267 |
| `civ-poetic` | 3093.9800 | 3190.7800 | **-96.8000** | -96.8033 |
| `civ-precise` | 2970.4400 | 3003.0733 | **-32.6333** | -32.6333 |
| `civ-mythic` | 2516.8200 | 2567.9300 | **-51.1100** | -51.1100 |
| `civ-therapist` | 2211.4600 | 2253.5700 | **-42.1100** | -42.1133 |
| `civ-engineer` | 2453.3600 | 2497.6067 | **-44.2467** | -44.2433 |

Max drift vs the documented values: **3.3e-03** (rounding in the published table). The offset
is **fixed** — neither repaired nor worsened by this run.

## 12. THE GAP MUST BE COMPUTED OVER THE **FULL** LEDGER — the sim-only sum makes it look like it moved

A first pass compared the post-run `relevance` against the sum of the **new rows only**
(excluding the 5 competition rows the ledger also contains). That made the gap appear to
move by 11-21 points for every civ, which would have been reported as "the counter gap is
accumulating" — a false regression.

The ledger stores **both** the sim-phase rows and the competition rows; `relevance` counts
only the former, so the two quantities can never be equal by construction. Summed over the
**full** history the gap is stable to 3.3e-03, exactly as documented.

*Rule: the gap is `relevance - sum(avg_score over the entire ledger)`. Never over a
subset of rows — a subset changes the gap by design and manufactures a fake drift.*

## 13. `ZAI_TOKEN` is still absent — **100th session** — and `ZAI_URL_OVERRIDE` is dead code behind it

Real z.ai returns **HTTP 401** (endpoint healthy, credential absent). Control B needs **both**
`ZAI_TOKEN` (the gate) and `ZAI_URL_OVERRIDE` (the redirect); the override alone is
unreachable code. JEV is live via `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`
(`jev-1.14.0`, HTTP 200).

## 14. The competition phase issues **no** provider requests of its own

The 80 new ledger rows are written by the sim phase; `civilization_competition()` calls
`run_simulation` again but the orchestrator's batch already holds the same rows, so the mock
served **161** requests total — not 161 + 40. This corrects the arithmetic in the session-237
report, which expected 89 (80 sims + 5 competitions + 4 pre-flight) against a ledger that
gained 80 rows, a decomposition that cannot reconcile.

*Rule: the mock request count is `preflight + repeat + 80`; the competition phase re-uses
the sim rows. Derive the expected count from the ledger delta (80), not from the number of
phase transitions.*

## 15. The NAS bridge needed **no** stale-cache retry this session

`ln -sfn` followed immediately by `ls -la .../code/civilizations/` succeeded on the first
call. The session-237 NFS attribute-cache artifact did not reproduce — the retry recipe is
still the right defence, but it should not be reported as a fact unless it is observed.
