# Civ Orchestrator — Run Report, session 165 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 49th session) + **live JEV**.

## Environment recovery

The workspace was **empty** apart from `.plugin-cache` — the prompt's path
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
(8th consecutive occurrence).

- Upstream owner: **`SuperInstance/AI-Writings`** (3.7 GB) — the `ai-writings/…` slug 404s.
- Cloned to **`/tmp`** with `--filter=blob:none --depth 1 --sparse` + `sparse-checkout set
  --no-cone cellular-first-design/code/civilizations` ⇒ ~6 MB working tree. Cloning into
  `/workspace` fails with `Disk quota exceeded` (NAS EDQUOT, total and size-independent).
- Bridge: `ln -s /tmp/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`
  — target is the **nested** `cellular-first-design` dir, never the clone root.
  Verified by inode identity (**`129:10423` on both sides**) **and** `-ef` → `EF_OK`.
- `ZAI_TOKEN` absent from env and from all 8 sandbox secrets; z.ai returns **401**
  `token expired or incorrect` ⇒ endpoint healthy, credential absent.
  **JEV live**: malformed `questions` → **422** `dict_type` (payload-shape complaint ⇒ auth OK).
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code — the token gate returns `None` first).

## Mock integrity (all four fixes re-applied)

| # | Fix | Session |
|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` | 112 |
| b | `md5(whole_message)[:8]` | 118 |
| c | `Connection: close` + `Content-Length` | 144 |
| d | interpolate the seed placeholder | 145 |

Pre-flight on the **exact long cultural prompts** (lengths 167–209): 40 requests,
**40/40 distinct seeds**, **40/40 distinct previews**, every seed matched an
independently recomputed `md5(whole_message)[:8]`, **0 tracebacks**.
Post-run mock log: **121** OK lines (1 ping + 40 pre-flight + 80 run), **0 `EXC:`**.
Teardown: server pid killed by exact argv, 0 remaining procs, `curl` exit 7 (port closed).

## Verification — 26/26 checks pass

| Check | Expected | Observed |
|---|---|---|
| per-civ ledger Δ | +10 × 8 | **+10 × 8** (1096/1127/1142/1099/1121/1091/1094/1154) |
| `meta_log.jsonl` Δ | +5 | **+5** (558 → 563) |
| `Winner:` lines | 5 | **5** |
| `culture.json` `simulations_run` Δ | +10 × 8 | **+10 × 8** |
| `wins+losses` total Δ | +40 | **+40** (4240 → 4280) |
| `git status --porcelain` | 18 modified | **18** (8 ledgers + 8 cultures + meta_log + leaderboard) |
| new rows | 80 | **80** |
| rows with JEV `error` | 0 | **0** |
| 2.0/2.0/2.0 fallback triples | 0 | **0** |
| `provider` | zai only | **zai** |
| rows missing `[mock-zai seed=` prefix | 0 | **0** |
| distinct seeds | 40 / 80 rows | **40 / 80** |
| `(civ,prompt)` carrying >1 seed | 0 | **0** |
| JEV `confidence` non-null | 80/80 | **80/80** |
| distinct quality / alignment values | >1 (real variation) | **62 / 68** |

## Low-relevance civilization: **`civ-grounded` (The Grounded)** — 41st consecutive session

**Lifetime (8 924 rows):**

| civ | n | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| civ-poetic | 1121 | 1.5562 | 0.7542 | 1.8554 | 2.0589 |
| civ-whimsical | 1154 | 1.4069 | 0.5996 | 1.9206 | 1.7006 |
| civ-precise | 1091 | 1.3919 | 0.5127 | 1.5491 | 2.1138 |
| civ-mythic | 1099 | 1.2612 | 0.5348 | 1.7077 | 1.5410 |
| civ-formal | 1127 | 1.1728 | 0.4530 | 1.4061 | 1.6594 |
| civ-therapist | 1094 | 1.1524 | 0.4637 | 1.7210 | 1.2725 |
| civ-engineer | 1096 | 1.1373 | 0.4543 | 1.4728 | 1.4849 |
| **civ-grounded** | 1142 | **0.9954** | **0.4161** | 1.4942 | **1.0760** |

Last of 8 on **avg_score**, **quality**, and **alignment**. The structural gap is
**alignment 0.1965** below the next civ (therapist 1.2725) versus **quality 0.0369**
below the next (formal 0.4530) ⇒ the alignment gap is **5.3× wider**. Alignment is the
dimension the meta-GAN *selects* on ⇒ a **voice** failure, not a prose failure.
Lifetime novelty 1.4942 is **6th of 8** (not "above median" — check the rank).

**Run-level (this run's 80 rows):** grounded **7th of 8** on `avg_score` (1.1330), ahead
of only `civ-therapist` (1.0620) — the run is compressed, only **0.0710** separating them.
Report the lifetime table as the structural signal and the run ranking as the watch axis.

**Extinction risk: NONE.** Threshold −10; lowest raw relevance 1052.42 = 105× above the floor.
Registry 8 civs, `max_civs` 12. Extinction/birth only runs under `--loop`.

## Chooser vs `avg_score` argmax: 1/5 (20 %)

`civ-precise` won 2/5, `civ-therapist`/`civ-grounded`/`civ-engineer` 1 each.
In **4 of 5** the chooser took a **lower**-scoring candidate (e.g. p1 therapist 1.187 vs
argmax poetic 2.077; p3 grounded 1.360 vs argmax precise 2.640) ⇒ **12th consecutive
session with the "chooser picks lower" direction.** Mechanism (confirmed in source): the
chooser is a JEV **`choice`** question over 150-char `content_preview` snippets, while
`avg_score` is the mean of three **`score`** questions on the same text — different
questions, different answers. **Never treat `win_rate` as a quality metric.**

## Counter gap: NEGATIVE, and unchanged in magnitude

`culture.json` `relevance_score` − ledger Σ`avg_score` = **−609.92** total, with per-civ
offsets **identical to the pre-run git blobs** (whimsical −173.14, poetic −96.80, formal
−85.53, grounded −84.35, mythic −51.11, engineer −44.24, therapist −42.11, precise −32.63).
`save_state()` has no lock ⇒ **`relevance_per_sim` is not recomputable from the ledger by
an auditor.** Sign confirmed from the data, not copied from a prior report.

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild from the
   RUNBOOK with **all four** fixes (112, 118, 144, 145) and run the pre-flight probe
   (40 distinct seeds AND 40 distinct previews) **before** the batch.
2. `ZAI_TOKEN` still absent ⇒ real z.ai unusable; Control B is the only provider path.
   JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
3. Use the run-wide integrity checks (80 rows, 40 seeds, per-`(civ,prompt)` 1:1) and
   isolate this run's rows by **count from the end of each civ file** (last 10), never by
   a `ts` cutoff.
4. `civ-grounded` has been the low-relevance civ for **41** straight sessions. If a
   session ever finds it mid-table, that is a *finding* — check the run-wide seed count
   first to rule out a degenerate mock before believing it.
5. Tool timeout 30 s < orchestrator run ~20 s ⇒ detached launch with stdout redirected
   **and** `< /dev/null`, then poll `ps` + the log.
6. The NAS EDQUOT trap also blocks **file delivery** — `cp` into `/workspace` leaves a
   0-byte file. Deliver by pushing to git and citing the remote URL, not a workspace
   attachment.
