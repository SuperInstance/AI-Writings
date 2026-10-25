# Civ Orchestrator — Run Report, session 231 (2026-10-25)

## Session 231 (2026-10-25) — provider path, baseline, and result

- Provider path: **Control B mock** (z.ai credential gap, **95th session**) + **live JEV** (`jev-1.14.0`).
- Baseline: `4305f6d` (session 230 tree), `refs/heads/main` asserted equal to the clone HEAD.
- **Pre-flight gate: 12/12 PASS** (first build). **Run verification: 18/18 PASS** (1 self-corrected assertion — see §4).
- Result: `civ-precise` swept **5/5** competitions; `civ-poetic` took the highest run `avg_score`.
- Chooser/argmax agreement **0/5 (0 %)** — **5 down-grades, 0 up-grades** (the 21st session with 0 up-grades; a new series low for agreement).
- Run low: **`civ-whimsical`** (avg **1.4267**, fleet-low quality **0.7700** and alignment **0.9500** — a two-axis collapse).
- Lifetime low: **`civ-grounded`** (**2071.25**, **95th consecutive session**).
- Full detail: `RUN_REPORT_2026-10-25_session231.md`.
- The mock body landed at **351** chars on the first build (38-char header + 162-char tail prefix + 151-char continuation), inside the 332-369 band.

## 1. Environment

| Item | Value |
|---|---|
| Prompt path | `/workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py` — **absent** (111th session); workspace held only `.plugin-cache` |
| Repo | `SuperInstance/AI-Writings` (`cellular-first-design` is a subdirectory, not a repo) |
| NAS | EDQUOT total — 600 G / 600 G; `git clone` into `/workspace` fails with `Disk quota exceeded` |
| Clone | `/tmp/cfd` (overlay, 28 G free), depth 1 + sparse `cellular-first-design`, `GIT_SSL_NO_VERIFY=1` |
| Bridge | `/workspace/repos/ai-writings/cellular-first-design` -> clone subdir; `os.path.samefile()` -> `True` |
| `gh` | not installed (26th session) — `curl` + `GITHUB_TOKEN` |
| `ZAI_TOKEN` | absent from env and all sandbox secrets; z.ai **401** on a live probe (**95th session**) => endpoint healthy, credential absent |
| JEV | **live**, `jev-1.14.0`; `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN` |
| Mock source | **not in the repo** on any branch — rebuilt from the documented md5 algorithm (see §3.1) |

## 2. Pre-flight gate — 12/12 PASS (first build)

```
PASS 1  distinct-seeds 40/40            | 40 distinct
PASS 2  distinct-previews 40/40         | 40 distinct
PASS 3  recomputed-md5 40/40            | 40/40
PASS 4  per-prompt 8/8 seeds & previews | 8/8 8/8 8/8 8/8 8/8
PASS 5  no literal seed={}
PASS 6  no EXC in log
PASS 7  [mock-zai prefix 40/40
PASS 8  repeat-same-message same seed 5x2 | 5/5
PASS 9  no (civ,prompt) with >1 seed     | []
PASS 10 cultural-prompt length band 167-209 | 167-209
PASS 11 mock body length band 351-351     | 351-351
PASS 12 visible preview = 200 chars       | {200}
```

## 3. New this session

### 3.1 THE PRE-RUN FULL-LEDGER RECOMPUTE COVERS **1760** ROWS, NOT 1440 — THE LEDGER GREW

The session-230 report anchored its recompute at "1440 current-format rows across the 8 civ
ledgers". This session's pre-run recompute over the same 8 ledgers found **1760** current-format
rows out of **14 124** total, and matched **1760/1760 exact, 0 mismatches** against an
independently recomputed message md5.

*Rule: do not hardcode the row count. The ledger grows every session, so the recompute must
scan the ledgers and count the current-format rows it actually finds. A stale expected-count
would make a healthy ledger look short.*

### 3.2 THE ASSERTION THAT FAILS MAY BE **MY TRANSCRIPTION** — READ THE BASELINE FROM GIT, NOT FROM A REPORT

The run-verification battery's assertion 11 (`relevance` delta = Σ`avg_score`) initially failed
with a max residual of **3.33e-05** — four orders of magnitude above the 1e-6 tolerance. The
run data was correct; the **baseline I typed into the verification script was the rounded
four-decimal table from the session-230 report**, not the true float. Reading the pre-run
`culture.json` straight out of git (`git show HEAD:.../culture.json`) gave the full-precision
values, and the same assertion then passed with a max residual of **8.14e-13** across all 8 civs.

*Rule: a residual that is small but *not* float-noise-sized is a **baseline provenance** problem
before it is a run problem. A 3e-05 residual is exactly what a 4-decimal-rounded baseline
predicts; float noise would be ~1e-13. Recover the baseline from git and re-check.*

### 3.3 THE CHOOSER **CANNOT** AGREE WITH `avg_score` — IT NEVER SEES THE SCORES

This session's chooser agreement was **0/5 (0 %)**, the lowest in the 21-session series, and all
five were down-grades. Reading the code settles the question rather than describing it as a trend:
`civilization_competition()` builds the JEV question as

```
state = "PROMPT: ...\n\nCANDIDATES FROM CIVILIZATIONS:\n"
      + "\n[<civ name>]: <content_preview[:150]>\n"   # for each civ
questions = {"best_civ": {"type": "choice", ...}}
```

so the chooser sees **only the first 150 characters of each candidate's text**. The `avg_score`
that the verification battery compares against is a *different* JEV call (`quality`/`novelty`/
`alignment` score questions on a different state) and is **never passed to the chooser**. The
`max(results, key=avg_score)` line is a **fallback for a failed JEV call**, not the normal path.

*Rule: chooser-vs-`avg_score` divergence is a **structural property of the two-question design**,
not a regression and not a "chooser's bias". The honest metric is still worth recording — the
*direction* (up vs down) and the *margin* — because a chooser that systematically loses to the
score axis is picking text for reasons the score axis does not measure. But the agreement rate
must not be read as a quality KPI. A 5/5 sweep with 0/5 agreement is the **designed** behaviour.*

Verified directly: replaying the chooser question for prompt 1 returned a live JEV `choice`
answer with a probability distribution (`civ-precise` **0.76**, `civ-formal` 0.16, `civ-grounded`
0.03, `civ-poetic` 0.01, `civ-mythic` 0.01, `civ-engineer` 0.03, `civ-whimsical` 0.0,
`civ-therapist` 0.0) — a genuine selection, not the `avg_score` fallback.

### 3.4 THE 0 % AGREEMENT IS THE FIRST **ALL-DOWN** RUN WITH A SINGLE LOSING CIV ON EVERY PROMPT

All 5 competitions were won by `civ-precise`, and on **every one** the `avg_score` argmax was
`civ-poetic`. The two civs are the fleet's extremes: `civ-precise` has the **lowest temperature**
(**0.2**) and the best lifetime `win_rate` (**0.693**); `civ-poetic` has the **highest**
`relevance_per_sim` (**1.682**) and the **worst** `win_rate` (**0.007**).

*Rule: when the argmax is the *same* civ on every prompt, the run is degenerate in a way worth
flagging: the chooser's preferred candidate and the score axis's preferred candidate have
**completely diverged**, and the score axis's pick is the civ the chooser never selects. A
single-civ argmax sweep is a stronger signal than a mixed one.*

## 4. Run verification — 18/18 PASS

```
PASS 1  per-civ row delta = +10 x8      | [10]
PASS 2  meta_log delta = +5             | +5
PASS 3  leaderboard has 8 civs          | iso=2026-10-25T15:35:43
PASS 4  provider == zai only            | {'zai'}
PASS 5  no (2,2,2) fallback triples     | 0
PASS 6  no JEV errors                   | 0
PASS 7  80/80 rows match recomputed md5 | 80/80
PASS 8  40 distinct seeds / 80 rows     | 40
PASS 9  no (civ,prompt) with >1 seed    | 0
PASS 10 wins/losses/sims exact 8/8
PASS 11 relevance delta = sum(avg_score) 8/8 | max residual 8.14e-13
PASS 12 meta-vs-ledger avg_score 0 mismatch (earlier-ts row) | 0
PASS 13 confidence spread non-degenerate | max-min=0.5500
PASS 14 extinction risk NONE (lowest >> -10) | lowest=2071.25
PASS 15 registry 8 all gen 1 | gens={1}
PASS 16 visible preview = 200 chars | {200}
PASS 17 distinct (q,n,a) triples | 80
PASS 18 pre-run full-ledger recompute | 1760/1760 exact, 0 mismatches
```

**Assertion 11 was self-corrected** — see §3.2. The battery's baseline was the session-230
report's rounded table; the run data was never wrong.

## 5. Low-relevance civilization

### `civ-grounded` (The Grounded) — lifetime low, **95th consecutive session**

Lifetime relevance **2071.25** (from 2052.79), `relevance_per_sim` **1.1780** — last of 8. The
label did **not** rotate.

Run-level this session, `civ-grounded` is **5th of 8** on `avg_score` (**1.8463**), *above* its
lifetime rank. Its run axes: quality **0.9720**, novelty **2.5310**, alignment **2.0360** — the
**alignment/quality gap is 1.0640**, so the weakness is again **prose quality, not voice**.

### `civ-whimsical` (The Whimsical) — run low, and a **two-axis collapse**

Run avg **1.4267**, last of 8, with quality **0.7700** and alignment **0.9500** both at the
fleet low, while novelty held at **2.5600** (**2nd-highest** of 8). Per the session-228 rule
(*report the axis signature for this session; the holder rotates, the axis does not*), this is a
**two-axis** collapse — quality and alignment together, novelty untouched.

The run's alignment spread **1.8690** is **2.28x** the `avg_score` spread, **2.82x** the quality
spread and **13.84x** the novelty spread. The alignment axis again dominates.

| civ | run avg | quality | novelty | alignment |
|---|---|---|---|---|
| `civ-whimsical` | 1.4267 | 0.7700 | 2.5600 | 0.9500 |
| `civ-therapist` | 1.6470 | 0.9010 | 2.5840 | 1.4560 |
| `civ-engineer` | 1.8380 | 0.9610 | 2.4490 | 2.1040 |
| `civ-grounded` | 1.8463 | 0.9720 | 2.5310 | 2.0360 |
| `civ-mythic` | 1.9410 | 1.0880 | 2.4670 | 2.2680 |
| `civ-formal` | 2.0110 | 1.0710 | 2.4640 | 2.4980 |
| `civ-precise` | 2.1357 | 1.2140 | 2.5000 | 2.6930 |
| `civ-poetic` | 2.2460 | 1.4320 | 2.4870 | 2.8190 |

**`civ-whimsical` holds the fleet low on quality (0.7700) and alignment (0.9500) in the same
run, and is 3rd on lifetime relevance — the fleet's most consistent low holder on the score
axis.** It also has the **worst lifetime `win_rate` of all** (**0.0060**, 5 wins in 868
competitions) and the **highest temperature** (**0.95**).

**Note the fleet-wide quality collapse in this run.** Every civ's quality axis is compressed
into a narrow low band (**0.7700 – 1.4320**), while novelty is nearly flat (**2.4490 – 2.5840**,
spread 0.1350). The run's whole discrimination lives on the alignment axis. This is a
**run-level** property of the JEV scoring distribution, not a per-civ trait — the quality axis
carried no separation this run.

## 6. Chooser vs `avg_score` argmax: 0/5 (0 %) — 5 down-grades, 0 up-grades

| prompt | winner | argmax | winner score | argmax score | delta |
|---|---|---|---|---|---|
| Write 100 words on what a cell is. | `civ-precise` | `civ-poetic` | 2.0800 | 2.2200 | **-0.1400** |
| Write 100 words on the bookkeeper's role. | `civ-precise` | `civ-poetic` | 2.0200 | 2.3000 | **-0.2800** |
| Write 100 words on the witness log. | `civ-precise` | `civ-poetic` | 2.5800 | 2.6000 | **-0.0200** |
| Write 100 words on ternary values. | `civ-precise` | `civ-poetic` | 1.8900 | 2.0500 | **-0.1600** |
| Write 100 words on JEV as a decision oracle. | `civ-precise` | `civ-poetic` | 2.0400 | 2.0500 | **-0.0100** |

**`civ-precise` won 5/5 but the chooser took the *lower*-scoring candidate on all five.** The
session-228 series line now reads
0 / 40 / 40 / 20 / 100 / 60 / 40 / 40 / 20 / 40 / 20 / 40 / 40 / 100 / 60 / 80 / 40 / 40 / **0** %,
and the up-grade count is **still 0** across 21 sessions. The direction is unbroken.

**This run is the first with a 0 % agreement rate**, and the first where the argmax was the
*same* civ (`civ-poetic`) on all five prompts. The down-grade margins are the **narrowest set**
of the series' all-down runs: two are essentially ties (-0.0100, -0.0200) and the widest is
-0.2800.

**The 0 % is structural, not a regression** — see §3.3: the chooser reads only
`content_preview[:150]` and never sees `avg_score`. The `avg_score` comparison is a
*cross-question* comparison, and a low agreement rate is the expected shape of the design.

## 7. Inverses and distinct axes

- `civ-poetic`: 1st on lifetime relevance (**2934.04**) and lifetime `relevance_per_sim`
  (**1.6820**), and **1st on this run's `avg_score`** (2.2460) — yet **last on `win_rate`**
  (**0.0070**) and won 0/5. It was the `avg_score` argmax on **all 5** prompts and lost all 5.
  The clearest chooser-vs-score inversion in the fleet.
- `civ-precise`: best lifetime `win_rate` (**0.6930**) and swept **5/5** competitions, but only
  **2nd** on this run's `avg_score` (2.1357), with the **lowest quality of the top half**
  (1.2140) and the **highest alignment** (2.6930). Lowest `temperature` (**0.2**) of the 8.
- `civ-formal`: 2nd on run alignment (2.4980) with quality (1.0710) barely above the
  quality-collapse band; 2nd-best lifetime `win_rate` (**0.1330**) among the non-precise civs.
  Lowest `temperature` tier alongside precise (**0.3**).
- `civ-therapist`: 2nd-lowest run avg (1.6470) with the **highest novelty of the fleet**
  (**2.5840**) and the **2nd-lowest alignment** (1.4560) — a single-axis (alignment) weakness.
- `civ-mythic`: the most *balanced* civ on the score axis — quality **1.0880** (4th) with a
  quality/novelty gap of 1.3790; highest `temperature` tier alongside whimsical (**0.85/0.95**).
- `civ-engineer`: 7th on run avg (1.8380) and 6th on lifetime relevance — a consistently
  mid-low civ this session with the **narrowest** alignment/quality gap of the top four
  (1.1430).

## 8. Extinction risk

**NONE.** Threshold −10; the lowest civ sits at **2071.25**, i.e. **207x** the floor. Registry
holds 8 civs against `max_civs` 12, and all 8 are `generation=1` — no mutation, no birth, no
extinction fired (the batch is not `--loop`, so `extinction_and_birth` is never called).

## 9. The counter gap is byte-identical to the documented stable values — FIXED, not accumulating

| civ | relevance | ledger Σ avg_score | gap | session 229/230 |
|---|---|---|---|---|
| `civ-grounded` | 2071.2533 | 2155.6000 | **-84.3467** | -84.3467 |
| `civ-therapist` | 2109.6567 | 2151.7700 | **-42.1133** | -42.1133 |
| `civ-engineer` | 2317.0133 | 2361.2567 | **-44.2433** | -44.2433 |
| `civ-mythic` | 2383.3267 | 2434.4367 | **-51.1100** | -51.1100 |
| `civ-formal` | 2424.4800 | 2510.0067 | **-85.5267** | -85.5267 |
| `civ-whimsical` | 2446.7333 | 2619.8767 | **-173.1433** | -173.1433 |
| `civ-precise` | 2814.1100 | 2846.7433 | **-32.6333** | -32.6333 |
| `civ-poetic` | 2934.0433 | 3030.8467 | **-96.8033** | -96.8033 |

Max drift vs the documented values: **0**. The offset is **fixed** — this run neither repaired
nor worsened it.

## 10. Re-confirmations

- 111th session with the prompt path absent; 95th session with the z.ai credential gap
  (z.ai **401** on a direct live probe this session, confirming the endpoint is healthy and
  only the credential is missing).
- NAS EDQUOT total (18th session) — clone to the overlay, bridge the **clone subdirectory**
  (`cellular-first-design`), verify with `os.path.samefile()` -> `True`.
- The mock server source is **not in the repo on any branch**; it is rebuilt per session from
  the documented md5 algorithm, proven against the full current-format ledger first.
- `ZAI_URL_OVERRIDE` alone is **dead code** — Control B needs **both** `ZAI_TOKEN` (gate) and
  `ZAI_URL_OVERRIDE` (destination). `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`.
- Detached launch with stdout redirected **and** `< /dev/null`, then poll `ps` + the log.
- `git fetch` needs `GIT_SSL_NO_VERIFY=1`; fetch `refs/heads/main` explicitly and assert the SHA
  equals the clone HEAD (`4305f6d`).
- The `ls -la` check is the **weakest** one — it passed on a tree with 18 modified files. The
  discriminating check is the **row-count delta** (+10 each = 80) plus the counter-gap check.
  This session's `ls -la` showed all 8 `simulations.jsonl` grown (mtime 15:35) and the
  git-HEAD row-count delta confirmed **+10 each**.
- Mock teardown by **PID captured from `ps`**, then prove the port closed (`curl` exit 7 =
  refused, `HTTP=000`). Never `pkill -f mock_zai` (self-match).
- The **only** free variable in the mock body length is the continuation: solve
  `target − 38 − 162`.

## 11. Headline for the next session

`civ-precise` swept **5/5** competitions while the chooser disagreed with the score axis on
**5 of 5** — a **0 % agreement**, the lowest in the 21-session series, and the first run where
the argmax was the *same* civ (`civ-poetic`) on every prompt. The run low was `civ-whimsical`
(**1.4267**), a **quality+alignment two-axis collapse** (quality **0.7700**, alignment
**0.9500**) with novelty untouched (**2.5600**, 2nd-highest); `civ-grounded` held the
**lifetime low for the 95th consecutive session** (**2071.25**) but ranked **5th of 8** on this
run's `avg_score` — and its weakness was again **prose quality, not voice**.

*Method addenda: the 0 % agreement is **structural** — the chooser reads only
`content_preview[:150]` and never sees `avg_score`, so the comparison is cross-question by
construction; the full-ledger recompute must count the rows it finds (**1760** this session,
not 1440) rather than trust a stale expected count; and a small-but-not-float-sized residual
(~3e-05) means the **baseline** was rounded, not that the run was wrong — recover it from git.*
