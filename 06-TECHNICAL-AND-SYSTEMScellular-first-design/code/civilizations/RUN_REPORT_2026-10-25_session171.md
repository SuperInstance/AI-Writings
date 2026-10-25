# Civ Orchestrator — Run Report, session 171 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 54th session) + **live JEV**.
Baseline: `51fc662` (session 170). **All 24 verification assertions PASS.**

## Headline for the next session

- **The mock needs SIX fixes, unchanged.** All six were re-applied and the pre-flight gate passed **8/8** on the first build — no rebuild-drift this session. Fix (f) (message-derived index) is the one that matters: it is now covered by the **repeat-same-message probe** (check 7), which is the only gate step that can catch it.
- **`civ-grounded` remains the low-relevance civ — 46th consecutive session.** Last of 8 on lifetime `avg_score` 0.9970, `quality` 0.4075, `alignment` 1.0613, `relevance` 1114.06, `relevance_per_sim` 0.961. Alignment gap **0.9895** vs quality gap **0.3418** ⇒ **2.9×** wider ⇒ a **voice** failure, not a prose failure. Lifetime novelty 1.5223 is **6th of 8** — Grounded is not boring, it is mis-voiced.
- **The run-level low ROTATED to `civ-therapist`** (1.4473 run bottom on `avg_score`, `alignment` 1.1460) while its *lifetime* standing is mid-field. **Watch axis, not the finding** (session-132 rule).
- **Chooser vs `avg_score` argmax: 3/5 (60 %)** — all disagreements took the lower-scoring candidate. `civ-precise` swept **5/5**. Max |delta| **0.1633**.
- **Counter gap −609.9200, fixed.** Byte-identical to sessions 169 and 170 ⇒ the offset is structural, not accumulating.
- Run spreads: `avg_score` 0.6167, `alignment` **1.5960**, quality 0.4380, novelty 0.2070.
- Verification: per-civ Δ **+10 × 8** = **80** new rows, `meta_log` **+5** (588 → 593), `Winner:` **5**, `wins`/`losses` **8/8 exact**, `relevance` Δ = Σ`avg_score` **8/8 exact**, 0 JEV errors, 0 fallback triples, `zai × 80`, **40/40** distinct seeds, **0** `(civ,prompt)` with >1 seed, **80/80** rows match an independently recomputed md5, 8/8 seeds AND previews on all 5 prompts, meta-vs-ledger mismatches **0/40**, 80/80 distinct `(q,n,a)`, confidence 0.28–0.93, registry 8 all gen 1, extinction **NONE** (lowest +1114.06 = **111×** the floor). **24/24 PASS.**

## Environment recovery

- Workspace **empty** apart from `.plugin-cache` — the prompt's path did not exist (**12th consecutive occurrence**).
- Upstream **`SuperInstance/AI-Writings`** (3.7 GB); the `ai-writings/…` slug 404s (the GitHub API is case-insensitive).
- Cloned to **`/tmp/repos/ai-writings/AI-Writings`** with `--filter=blob:none --no-checkout` + `sparse-checkout set cellular-first-design` ⇒ 7.6 MB working tree. Cloning into `/workspace` fails with **`Disk quota exceeded`** (NAS EDQUOT, **18th session**); `/workspace` is 100 % full with **0 bytes** available, `/tmp` has 28 G free.
- Bridge: `ln -s /tmp/repos/ai-writings/AI-Writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`.
  **Symlink target correction (new this session):** the RUNBOOK's "point at the clone root" rule only holds when the clone root *is* the `cellular-first-design` directory. Here the clone root **contains** `cellular-first-design/`, so the link must target the **nested** directory — otherwise the script's `CIVS_DIR` resolves to a path with no `code/civilizations` under it and the run fails with `FileNotFoundError` on `civilizations.json`. Verify with `ls /workspace/repos/ai-writings/cellular-first-design/code/civilizations/` **before** launching.
  Verified by inode identity (**`129:7704` on both sides**) and `-ef` → `EF_OK`.
- `ZAI_TOKEN` absent from env and all 8 secrets; z.ai **401** `token expired or incorrect` ⇒ endpoint healthy, credential absent (**54th session**).
- **JEV live**: well-formed body → **HTTP 200** with `{"model":"jev-1.14.0", …}`.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and** `ZAI_URL_OVERRIDE` set (the override alone is dead code — the token gate returns `None` first).
- `gh` not installed (**20th session**) — used `GET /user/repos` with `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch, stdout redirected, `< /dev/null`.

## Mock rebuild — all SIX fixes, 8/8 pre-flight on the first build

| # | Fix | Session | Applied this session |
|---|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` index wrap | 112 | yes |
| b | `md5(whole_message)` (not first 8 alnum chars) | 118 | yes |
| c | `Connection: close` + `Content-Length` | 144 | yes |
| d | interpolate the seed placeholder | 145 | yes |
| e | seed widened 2 → 4 hex chars | 169 | yes |
| f | index derived from the MESSAGE (`d[0] % 4`), not a counter | 170 | yes |

Pre-flight on the **exact long cultural prompts**: **40/40** distinct seeds, **40/40** distinct previews, **40/40** independently recomputed md5s (seed, colour, figure), **8/8** distinct seeds AND **8/8** distinct previews on every one of the 5 prompts, 0 literal `seed={}`, 0 `EXC:`/tracebacks, **repeat-same-message ⇒ identical seed (40 messages × 2 repeats)**, and 0 `(civ,prompt)` with >1 seed. **8/8 PASS.**

Post-run mock log: 121 OK lines (40 pre-flight + 40 repeat probe + 80 run + 1 GET), 0 `EXC:`.
Teardown: mock pids killed by exact argv match (**two** pids), 0 remaining procs, `curl -m 5` ⇒ **exit 7**, `HTTP=000` (port closed).

## Verification — 24 checks, all PASS

| # | Check | Result |
|---|---|---|
| 1 | per-civ row delta == 10 for all 8 | PASS |
| 1b | total new rows == 80 | PASS |
| 2 | `meta_log` delta == 5 (588 → 593) | PASS |
| 3 | new rows collected == 80 (per-civ tails) | PASS |
| 4 | provider `zai` for all 80 rows | PASS |
| 5 | 0 JEV errors | PASS |
| 6 | 0 fallback triples (2.0/2.0/2.0) | PASS |
| 7 | 0 confidence == 0.0 rows | PASS |
| 8 | all rows carry a seed | PASS |
| 9 | 40 distinct seeds across 80 rows | PASS |
| 10 | 0 `(civ,prompt)` with >1 seed | PASS |
| 10b | 40 distinct `(civ,prompt)` pairs | PASS |
| 11 | 80/80 rows match an independently recomputed md5 (seed, colour, figure) | PASS |
| 12 | `meta_log` has 5 competition records | PASS |
| 13 | 5 `Winner:` lines in the run log | PASS |
| 14 | `wins`/`losses` delta exact for all 8 civs | PASS |
| 15 | `relevance` delta == Σ`avg_score` for all 8 civs | PASS |
| 16 | meta-vs-ledger mismatches == 0 (later-`ts` row) | PASS |
| 17 | 80/80 distinct `(q,n,a)` triples | PASS |
| 18 | confidence in (0,1] | PASS |
| 19 | registry still 8 civs | PASS |
| 20 | all civs still generation 1 (no birth/mutation) | PASS |
| 21 | no extinction (lowest relevance ≫ floor −10) | PASS |
| 22 | 0 `EXC:`/tracebacks in the mock log | PASS |

## Run-level scores (this session's 80 new rows)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-precise | 2.0640 | 0.9690 | 2.4810 | 2.7420 |
| civ-poetic | 1.9920 | 0.9190 | 2.5930 | 2.4640 |
| civ-formal | 1.7890 | 0.6920 | 2.4990 | 2.1760 |
| civ-whimsical | 1.7370 | 0.8600 | 2.5700 | 1.7810 |
| civ-mythic | 1.6603 | 0.8650 | 2.3860 | 1.7300 |
| civ-engineer | 1.5527 | 0.6260 | 2.4260 | 1.6060 |
| civ-grounded | 1.5323 | 0.5310 | 2.5350 | 1.5310 |
| civ-therapist | 1.4473 | 0.6820 | 2.5140 | 1.1460 |

## Lifetime standing (all rows on disk)

| civ | avg_score | quality | novelty | alignment | relevance | rel/sim |
|---|---|---|---|---|---|---|
| civ-poetic | 1.5569 | 0.7492 | 1.8707 | 2.0507 | 1741.90 | 1.523 |
| civ-precise | 1.4060 | 0.5147 | 1.5782 | 2.1251 | 1585.68 | 1.397 |
| civ-whimsical | 1.4008 | 0.5904 | 1.9330 | 1.6789 | 1527.37 | 1.327 |
| civ-mythic | 1.2568 | 0.5294 | 1.7224 | 1.5185 | 1405.49 | 1.234 |
| civ-formal | 1.1832 | 0.4516 | 1.4346 | 1.6635 | 1318.99 | 1.152 |
| civ-therapist | 1.1500 | 0.4594 | 1.7408 | 1.2499 | 1284.99 | 1.130 |
| civ-engineer | 1.1420 | 0.4502 | 1.4997 | 1.4760 | 1275.86 | 1.125 |
| civ-grounded | 0.9970 | 0.4075 | 1.5223 | 1.0613 | 1114.06 | 0.961 |

## Low-relevance civilization

**`civ-grounded` (The Grounded)** — lifetime low for the **46th consecutive session**.

| metric | value | rank |
|---|---|---|
| lifetime `avg_score` | 0.9970 | 8 of 8 |
| lifetime `quality` | 0.4075 | 8 of 8 |
| lifetime `alignment` | 1.0613 | 8 of 8 |
| lifetime `novelty` | 1.5223 | 6 of 8 |
| `relevance` | 1114.06 | 8 of 8 |
| `relevance_per_sim` | 0.961 | 8 of 8 |
| `wins`/`losses` | 70/497 | win_rate 0.123 |

**Diagnosis — voice failure, not prose failure.** The gap to the lifetime leader is **alignment 0.9895** against **quality 0.3418** — **2.9× wider** on the axis the meta-GAN actually selects on. Novelty is **1.5223**, mid-pack, so Grounded is not producing boring text; it is producing text the chooser cannot attribute to its declared voice (`warm, factual`).

**Run-level low rotated to `civ-therapist`** (1.4473 on `avg_score`, `alignment` 1.1460) while its lifetime standing is mid-field. Per the session-132 rule, the *axis* is the finding; the *label* on the run low rotates.

**Counter gap.** `culture.json` relevance minus the ledger sum of `avg_score` is **−609.9200** for all 8 civs, **byte-identical** to sessions 169 and 170, with per-civ Δ **0.0000**. The offset is fixed, not accumulating. `save_state()` has no lock, so `relevance_per_sim` is not recomputable from the ledger by an auditor.

## Notes for the next session

1. The mock is **not** on disk at session start (`/tmp` wiped) — rebuild from the RUNBOOK with **all SIX** fixes and run the **eight**-check pre-flight (including the repeat-same-message probe) before the batch.
2. **Verify the bridge path before launching**, not after: the symlink target is the **nested** `cellular-first-design` directory inside the clone root. `ls /workspace/repos/ai-writings/cellular-first-design/code/civilizations/` must list `civilization_orchestrator.py`.
3. `ZAI_TOKEN` still absent ⇒ real z.ai unusable; Control B is the only provider path. JEV is live and needs `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`.
4. Isolate this run's rows by **count from the end of each civ file** (last 10), never by a `ts` cutoff. `git show HEAD:<path>` must run with `cwd` = the **clone root**.
5. The meta-vs-ledger check must take the **later-`ts`** row for a `(civ, prompt)` pair.
6. `civ-grounded` has been the low-relevance civ for **46** straight sessions. If a session ever finds it mid-table, that is a *finding* — check the run-wide seed count first to rule out a degenerate mock before believing it. The run-level low has now rotated to `civ-therapist`; do not promote the run low to the lifetime finding.
7. Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch with stdout redirected **and** `< /dev/null`, then poll `ps` + the log.
8. The NAS EDQUOT trap also blocks **file delivery** — `cp` into `/workspace` leaves a 0-byte file. Deliver by pushing to git and citing the remote URL, not a workspace attachment.
9. **Mock teardown:** kill by exact argv match (`python3 /tmp/mock_zai.py` and `timeout -s KILL 900 python3 /tmp/mock_zai.py`) — **two** pids. Never `pkill -f mock_zai`, which self-matches the killing shell. Then prove the port is closed: `curl -m 5` ⇒ **exit 7** and `HTTP=000`.
10. **A failed run must be reset, not patched.** Restore the ledger with `git checkout -- .` from the clone root and re-derive the baseline before a second attempt.
