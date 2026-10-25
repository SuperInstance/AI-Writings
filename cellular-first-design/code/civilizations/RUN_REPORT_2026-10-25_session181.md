# Civ Orchestrator — Run Report, Session 181

**Date:** 2026-10-25T06:34Z
**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Baseline:** HEAD `9b43a105` — clean tree
**Provider path:** Control B (local mock z.ai on 127.0.0.1:8899), `ZAI_URL_OVERRIDE` + placeholder `ZAI_TOKEN`
**JEV:** live (`jev-1.14.0`, HTTP 200), `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`
**Result:** **23/23 verification assertions PASS** (+ 8/8 pre-flight gate)

## Environment

Workspace arrived empty (a wipe; 110th). The prompt's path did not exist — the
`ai-writings/cellular-first-design` slug 404s on the GitHub API (the API is
case-insensitive; the real upstream is `SuperInstance/AI-Writings`, where
`cellular-first-design` is a **subdirectory**). Recovery: sparse clone
(`--filter=blob:none --no-checkout` + `sparse-checkout set cellular-first-design`)
into `/tmp` ⇒ 7.0 MB working tree.

`/workspace` NAS is at **100 % quota** while visibly empty: cloning directly into
`/workspace/repos/ai-writings` dies with `close error: Disk quota exceeded`
(EDQUOT trap, 19th session). The **symlink bridge** is the only way in —
`/workspace/repos/ai-writings/cellular-first-design` → `/tmp/aiw/cellular-first-design`.
Verified with `os.path.samefile()` ⇒ **True**, dev:ino **129:3701** on both sides.
The bridge must satisfy BOTH the requested path and the script's hardcoded `CIVS_DIR`.

`ZAI_TOKEN` is absent from the environment and from all 8 sandbox secrets; z.ai
returns **401 `token expired or incorrect`** (endpoint healthy, credential absent)
— **60th consecutive session**. `ZAI_URL_OVERRIDE` alone is dead code (the token
gate returns `None` first), so a placeholder token was supplied.

`gh` not installed (**20th session**) — used `GET /users/SuperInstance/repos`
with `GITHUB_TOKEN`.

## NEW — the run-level low CONVERGED onto the lifetime low

The last four sessions each logged a *rotating* run-level low: whimsical (178),
whimsical (179), therapist (180) — and session 171's own rule said "do not promote
the run low to the lifetime finding." That rotation **stopped** this session:

| session | run-level low | lifetime rank of that civ |
|---|---|---|
| 178 | civ-whimsical | 3rd of 8 |
| 179 | civ-whimsical | 3rd of 8 |
| 180 | civ-therapist | 7th of 8 |
| **181** | **civ-grounded** | **8th of 8 (the lifetime low)** |

This is the **first session in the series where the run-level low and the
lifetime low are the same civ.** The session-132/session-180 rule ("the *holder*
rotates; the *axis* does not") still holds for the axis — **alignment** carried
the widest run spread again (2.4230, vs quality 0.7050 and novelty 0.2330) — but
the holder stopped rotating.

*Rule refinement: a rotating run-level low is a sample artifact; a run-level low
that lands on the lifetime low is **convergent evidence** for the lifetime
finding, and the two should be reported as one result, not two.*

### `civ-grounded` — lifetime low, **55th consecutive session**

Last of 8 on lifetime `relevance` **1236.36**, `relevance_per_sim` **0.982**,
`avg_score` **1.0144**, `alignment` **1.0646**, `quality` **0.3997**.

The binding constraint is still **alignment**: gap to the next civ **+0.1375** vs
quality's gap **+0.0432** = **3.18×** wider. Alignment is the dimension the
meta-GAN's chooser selects on, so this is a **voice** failure, not a prose
failure. Lifetime novelty **1.5788** is 4th of 8 — Grounded is neither boring nor
unmistakable; it is simply not rewarded.

Its run-level numbers this session are the worst in the fleet on every axis:
run `avg_score` **0.7657**, `alignment` **0.1770**, `quality` **0.0640** — while
run novelty **2.0560** is essentially tied with the field. The low is *not* a
novelty deficit; it is the tightest alignment collapse seen in this series.

## Run-wide verification — 23/23 PASS

- per-civ ledger delta **+10 × 8 = 80** new rows (5 sims + 5 competition rows each)
- `meta_log.jsonl` delta **+5** (638 → 643); `Winner:` lines = **5**
- wins/losses exact **8/8** (`dW+dL == 5`): precise **+4/+1**, formal **+1/+4**, all others **+0/+5**
- `relevance` delta == Σ(this run's `avg_score`) **8/8 exact** (max abs diff **5.15e-13**)
- leaderboard `sims_run` == `culture.json` `simulations_run` **+10** each, **8/8**
- distinct seeds **40/80 rows**; **0** `(civ,prompt)` carrying >1 seed
- **80/80** rows carry the `[mock-zai seed=…]` prefix; **80/80** `provider=zai`
- **0** JEV `error` rows; **0** `2.0/2.0/2.0` fallback triples
- **80/80** distinct `(quality, novelty, alignment)` triples
- registry 8 all gen 1, no births, no extinctions
- extinction risk **NONE** (threshold −10; lowest +1236.36 = **123×** the floor)

Every baseline comparison was taken from `git show HEAD:…`, never a hand-typed
number — the session-180 lesson about 2-dp rounding traps was applied up front
and produced **zero** spurious FAILs this session.

## Pre-flight gate — 8/8 PASS on the FIRST build

| Check | Result |
|---|---|
| distinct seeds | 40/40 |
| distinct previews | 40/40 |
| md5 recompute mismatches | 0/40 (seed, colour, figure) |
| per-prompt 8/8 distinct seeds AND previews | 5/5 prompts |
| literal `seed={}` | 0 |
| seed widths | all 8 hex chars |
| repeat-same-message determinism | 0/40 unstable |
| mock log `EXC:` / HTTP 500 | 0 / 0 |

The 4-hex-char seed slice (`h[(i*2)%8:(i*2)%8+4]`, 65 536 seeds) held on the first
build; message lengths 167–209 as expected.

## Leaderboard (post-run, lifetime)

| # | civ | relevance | rel/sim | wins | losses | win_rate | avg_sc | align | qual | novel |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1911.56 | 1.537 | 6 | 612 | 0.010 | 1.5678 | 2.0558 | 0.7426 | 1.9050 |
| 2 | civ-precise | 1753.85 | 1.420 | 380 | 233 | 0.620 | 1.4280 | 2.1328 | 0.5207 | 1.6307 |
| 3 | civ-whimsical | 1666.85 | 1.332 | 5 | 613 | 0.008 | 1.4003 | 1.6596 | 0.5765 | 1.9648 |
| 4 | civ-mythic | 1534.77 | 1.239 | 10 | 602 | 0.016 | 1.2596 | 1.4967 | 0.5211 | 1.7612 |
| 5 | civ-formal | 1473.67 | 1.184 | 95 | 521 | 0.154 | 1.2115 | 1.6873 | 0.4512 | 1.4960 |
| 6 | civ-engineer | 1406.64 | 1.140 | 47 | 564 | 0.077 | 1.1552 | 1.4649 | 0.4442 | 1.5564 |
| 7 | civ-therapist | 1392.03 | 1.125 | 11 | 604 | 0.018 | 1.1437 | 1.2020 | 0.4429 | 1.7861 |
| 8 | **civ-grounded** | **1236.36** | **0.982** | 70 | 547 | 0.113 | **1.0144** | **1.0646** | **0.3997** | 1.5788 |

## THIS RUN (80 rows)

| # | civ | run_avg | align | qual | novel | d_rel |
|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1.8860 | 2.6000 | 0.7690 | 2.2890 | 18.8600 |
| 2 | civ-whimsical | 1.7950 | 2.4200 | 0.6800 | 2.2850 | 17.9500 |
| 3 | civ-mythic | 1.4400 | 1.7020 | 0.5060 | 2.1120 | 14.4000 |
| 4 | civ-formal | 1.3283 | 1.6640 | 0.2570 | 2.0640 | 13.2833 |
| 5 | civ-precise | 1.2580 | 1.4560 | 0.2160 | 2.1020 | 12.5800 |
| 6 | civ-engineer | 1.1873 | 1.1030 | 0.2830 | 2.1760 | 11.8733 |
| 7 | civ-therapist | 0.9433 | 0.5580 | 0.1420 | 2.1300 | 9.4333 |
| 8 | **civ-grounded** | **0.7657** | **0.1770** | **0.0640** | 2.0560 | 7.6567 |

Run spreads: `avg_score` 1.1203, `alignment` **2.4230** (widest axis again),
quality 0.7050, novelty 0.2330.

Note the run ordering **inverts** the lifetime ordering at the top: `civ-precise`
is 2nd of 8 on lifetime relevance but 5th of 8 this run, and `civ-poetic` is 1st
on both. The run's `avg_score` spread (1.1203) is roughly **2×** the lifetime
spread (0.5534) — per-run noise is large relative to the between-civ signal, so
**single-run ordering must never be read as a lifetime ranking.**

## Chooser vs `avg_score` argmax: 0/5 (0 %)

`civ-precise` swept **4/5** competitions; `civ-formal` took the fifth. The
chooser picked the `avg_score` argmax in **0 of 5** rounds — the lowest agreement
in the series. Never treat `win_rate` as a quality metric: it is a *selection*
metric, and `civ-precise` wins on selection while scoring 5th of 8 on this run.

## Counter gap

Per-civ gap (`culture.json` `relevance_score` − ledger Σ`avg_score`): **fixed and
not accumulating** — delta exactly **0.000000** for all 8 civs vs the pre-run
baseline.

## Teardown

Mock killed by exact-argv match (pids 340, 342 — both `timeout` wrapper and
python). Port proven closed: `curl -m 5` ⇒ **exit 7**, `HTTP=000`. No `pkill -f`
(self-match hazard). Bridge symlink left in place for the next session.

## Next session

1. Rebuild the mock from the spec in `RUNBOOK.md`; the 4-hex-char seed slice
   passed 8/8 first-try again.
2. Watch whether the run-level low **stays** on `civ-grounded` for a second
   session — one session is convergence, two is a regime change.
3. `civ-grounded` is now 55 sessions into the lifetime low with an alignment gap
   **3.18×** wider than its quality gap. It has never been mid-table. If it is
   ever mid-table, rule out a degenerate mock before believing it.
4. The chooser/argmax agreement hit **0/5**. If it stays at 0, the chooser may
   have started selecting on a different axis than `avg_score` — worth diffing
   the choice state against the score vectors.
