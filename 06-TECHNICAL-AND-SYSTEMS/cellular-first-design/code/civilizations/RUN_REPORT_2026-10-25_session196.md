# Civ Orchestrator — Run Report, session 196 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 70th session) + **live JEV** (`jev-1.14.0`).
Baseline: `52bb1f2` (session 195). **All 27 verification assertions PASS.** Pre-flight **14/14 PASS**.

## Headline for the next session

- **`civ-precise` SWEPT 5/5 FOR THE SIXTH CONSECUTIVE SWEEP — AND IT IS STILL A CHOOSER
  EFFECT.** The chooser disagreed with the `avg_score` argmax on **4 of 5** prompts and
  **all four took the LOWER-scoring candidate** — the **15th consecutive session** in
  which a chooser/argmax disagreement is a *down*-grade. Agreement **1/5 (20 %)**.
  `civ-poetic` was the argmax on **4 of 5** prompts and won **none**; `civ-precise` was
  the argmax on **1 of 5** and won **5 of 5**. The standing suspect is unchanged: the
  `best_civ` criteria map (`civ_id -> civ name`) being read as a quality signal.
  **Re-base the streak to 15.**
- **`civ-grounded` remains the lifetime low — 68th consecutive session.** Last of 8 on
  lifetime `relevance` **1470.24** and `relevance_per_sim` **1.043** (the lowest in the
  fleet). Lifetime `win_rate` **0.101** — **3rd-best in the fleet** behind `precise`
  (0.654) and `formal` (0.142). Lowest relevance = **147x** the −10 floor ⇒ **no
  extinction risk**. *Selection and relevance are separate axes: the least-relevant civ
  is not the least-selected one.*
- **THE RUN-LEVEL LOW ROTATED TO `civ-therapist`** (run `avg_score` **1.6887**,
  `alignment` **1.5660** lowest, `quality` **1.0400** 2nd-lowest) — a **15th different
  civ in 15 sessions**. *The holder rotates; the axis does not.*
- **THE AXIS SPREAD IS DOMINATED BY ALIGNMENT, NOT QUALITY.** Cross-civ spreads this run:
  `alignment` **1.5440** › `avg_score` **0.7513** ≈ `quality` **0.7510** › `novelty`
  **0.1230**. Novelty is nearly flat across the fleet (2.444–2.567) — the entire ranking
  this run is produced by `alignment` and `quality`. Same shape as sessions 191–195,
  but the **alignment spread is the widest recorded in the series** (1.5440 vs 1.0780 in
  session 195) and the **novelty spread is the narrowest** (0.1230 vs 0.1510).
- **THE LOW CIVS SPLIT INTO TWO DISTINCT SIGNATURES THIS RUN — A CHANGE FROM THE
  SINGLE "HIGH NOVELTY, LOW ALIGNMENT" SIGNATURE OF SESSIONS 194–195.**
  `civ-therapist` fits the old signature (novelty 2.4600 / alignment 1.5660, the
  largest alignment-novelty gap in the fleet at **0.8940**). But `civ-grounded` does
  **not**: its novelty is **2.5050** (2nd-highest) and its alignment is **2.2070**
  (4th-lowest), while its **quality is 1.0240 — the lowest in the fleet by 0.0160**.
  *`civ-grounded`'s low axis is QUALITY; `civ-therapist`'s is ALIGNMENT.* The two lows
  of this run fail for different reasons, which is why the single-signature rule from
  session 195 did not predict the holder.

## Verification — 27/27 PASS

Baseline commit: `52bb1f2` (session 195), derived by reading the **git blob** of each
ledger and `culture.json` — never from a remembered count. This run's rows are the
**last 10** per civ ledger; this run's `meta_log` entries are the **last 5**.

| # | assertion | result |
|---|---|---|
| 1 | per-civ ledger delta | **+10 x 8 = 80** |
| 2 | total new rows | **80** |
| 3 | `meta_log` | **+5** (713 -> 718) |
| 4 | `Winner:` lines in log | **5** |
| 5 | rows with a JEV `error` key | **0** |
| 6 | 2.0/2.0/2.0 fallback triples | **0** |
| 7 | `provider` on all rows | **`zai` x 80** |
| 8 | rows missing `[mock-zai seed=` prefix | **0** (80/80) |
| 9 | rows matching an independently recomputed seed+color+figure | **80/80** |
| 10 | distinct seeds (message-level) | **40/40** |
| 11 | `(civ,prompt)` combos with >1 seed | **0** |
| 12 | per-prompt 8/8 distinct seeds (5 prompts) | **8/8 x 5** |
| 13 | per-prompt 8/8 distinct previews (5 prompts) | **8/8 x 5** |
| 14 | relevance delta == sum(avg_score) | **8/8 exact** (max residual **3.94e-13**) |
| 15 | wins/losses vs `meta_log.winner_civ` | **8/8 exact** (precise 5, others 0) |
| 16 | log `Winner:` == `meta_log.winner_civ` | **5/5 agree** |
| 17 | registry / generations | **8**, all `gen=1` |
| 18 | extinction risk | **NONE** (lowest +1470.24 = 147x floor) |
| 19 | `simulations_run` delta | **+10 x 8** |
| 20 | meta-vs-ledger `avg_score` (later-`ts` row, same civ+prompt) | **0 mismatches** |
| 21 | leaderboard refreshed | **8 civs**, iso `2026-10-25T09:45:19` |
| 22 | `Traceback` in orchestrator log | **0** |
| 23 | `EXC:` in mock log | **0** |
| 24 | **run-scoped proof**: last 80 OK seed multiset == ledger seed multiset | **PASS** |
| 25 | no birth (new civ dirs) | **0** |
| 26 | this run's rows are the last 10, increasing `ts` | **8/8** |
| 27 | no `None`/NaN `avg_score` | **PASS** |

### Check 20 was a BUG IN THE VERIFIER, not in the data — and the bug is instructive

The first run of check 20 reported **1 mismatch**. The check compared the meta_log's
score for a `(civ, prompt)` against **the later-`ts` row among ALL civs for that
prompt**. That is wrong: a `(civ, prompt)` pair can appear **more than once** in this
run's rows (once from the batch phase, once from the competition phase), so the
"later-ts row for the prompt" can belong to a **different civ**. The correct
comparison is the later-`ts` row **for that same `(civ, prompt)`**.

Observed: `civ-grounded` / "what a cell is" had **two** ledger rows (1.79 from the
batch phase, 1.74 from the competition phase), and the meta_log score 1.74 matched the
**second** one exactly. The data was right; the check was wrong.

**Durable rule: an isolation key must include every dimension the row is looked up
by.** The runbook says "isolate this run's rows by counting from the end" and "take the
later-`ts` row within this run's rows only" — the second clause needs the same
`(civ, prompt)` key as the first, or the lookup silently crosses civs.

### The run-scoped proof (check 24) is immune to pre-flight re-runs again

The mock log held **200** OK-200 lines, not the **161** a fixed count would expect:
the pre-flight sent 40 distinct + 40 repeat (80), and the run sent 80, plus 2
liveness GET probes earlier in the session. A fixed-number check would report a
**false FAIL**; the **multiset identity** — the seed multiset of the **last 80** OK-200
lines equals the seed multiset of the **80** ledger rows — holds exactly. Same rule as
session 195, re-confirmed.

## Environment recovery

- The workspace was **empty** apart from `.plugin-cache` and `.skills`; the prompt's
  path did not exist (**16th consecutive occurrence**).
- Upstream owner: **`SuperInstance/AI-Writings`** — `cellular-first-design` is a
  **subdirectory** of that repo, not a repo of its own.
- **A FULL CLONE INTO `/workspace` DIES, BUT CLONING INTO `/tmp` WORKS.** The
  `--depth 1 --filter=blob:none --sparse` clone into `/workspace/repos` failed on
  `.git/description` with `Disk quota exceeded`; the identical clone into `/tmp`
  succeeded. The quota is on the **NAS mount**, not on the clone.
- **THE BRIDGE MUST POINT AT THE INNER `cellular-first-design` DIRECTORY** — the
  orchestrator's hardcoded `CIVS_DIR` is
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations`, so the
  symlink target must be the **repo's** `cellular-first-design` dir, *not* its
  `code/civilizations` dir. Pointing the symlink at `code/civilizations` produces a
  path that resolves to `.../code/civilizations/code/civilizations` and fails with
  `FileNotFoundError` on `civilizations.json`. This was re-derived by reading the
  script, not remembered.
- **`mkdir -p` BEFORE `ln -sfn` CREATES A NESTED LINK.** `mkdir -p
  /workspace/repos/ai-writings/cellular-first-design && ln -sfn <target>
  /workspace/repos/ai-writings/cellular-first-design` creates a real directory and
  then places the symlink **inside** it — the link ends up at
  `.../cellular-first-design/cellular-first-design`. Use `rm -f` + `ln -s` on the
  final path, or `mkdir -p` the **parent** only.
- `ZAI_TOKEN` is **absent** from the env (**70th session**); z.ai returns **401 `token
  expired or incorrect`** ⇒ the endpoint is healthy and the **credential** is missing.
  `ZAI_URL_OVERRIDE` alone is dead code behind the token gate, so **both** a placeholder
  `ZAI_TOKEN` and the override were set.
- `JEV_KEY` reads `TYPESAFEAI_KEY` but the env var is `TYPESAFE_AI_TOKEN` ⇒ the alias was
  exported. JEV returned HTTP 200 `{"model":"jev-1.14.0"}`; **0 fallback triples**.
- `gh` not installed — used the REST API with `GITHUB_TOKEN`.
- **Background launch needs `setsid nohup … < /dev/null &` inside a script file, not
  an inline subshell.** `(setsid nohup cmd &)` from a tool call died with the calling
  shell on two attempts; writing `/tmp/start_mock.sh` and running it with `nohup` gave
  a stable, detached process. **A mock that dies silently looks exactly like a mock
  that was never started** — always probe the port *after* the launch call returns.
- **The `write` tool cannot write to `/tmp`**; bash heredocs are the working path for
  every artifact outside the workspace.

## Mock rebuild — the eight fixes, and the band that caught the build again

All **seven** documented fixes plus the **OpenAI envelope** were applied:

| # | Fix | Applied |
|---|---|---|
| a | seed index wrap `h[(i*2)%8:…]` | yes |
| b | md5 of the **whole** user message | yes |
| c | `Connection: close` + `Content-Length` | yes |
| d | interpolate the seed placeholder | yes |
| e | seed widened to a **contiguous 4-hex-char slice** | yes |
| f | index from the **message** (`d[0] % 4`), not a request counter | yes |
| g | `figure` = three **string** components, not a division | yes |
| h | **OpenAI envelope** `choices[0].message.content` | yes |

**The response-body length band did its job for the second session running — and it
took THREE builds to satisfy, not two.** The first build rendered at **389**
characters (band 332–369) ⇒ a clean, localised FAIL. Trimming the tail gave **372** —
still 3 over. Trimming again gave **366** ⇒ PASS. The band is not cosmetic: a body
longer than ~369 characters pushes the **seed prefix out of the 200-char
`content_preview` truncation**, which would silently break the seed+color+figure
recompute check for every row.

**Pre-flight passed 14/14 on the third build.** The gate reads the **real**
`culture.json` files rather than a hand-typed fixture, and includes the
**repeat-same-message determinism probe** (40 messages × 2 repeats) that a
distinctness-only gate can never certify.

## Lifetime leaderboard (after session 196)

| civ | relevance | rel/sim | wins | losses | win_rate | gen |
|---|---|---|---|---|---|---|
| civ-poetic | 2204.17 | 1.581 | 6 | 687 | 0.009 | 1 |
| civ-precise | 2049.40 | 1.480 | 450 | 238 | 0.654 | 1 |
| civ-whimsical | 1902.22 | 1.358 | 5 | 688 | 0.007 | 1 |
| civ-mythic | 1770.10 | 1.274 | 10 | 677 | 0.015 | 1 |
| civ-formal | 1739.42 | 1.247 | 98 | 593 | 0.142 | 1 |
| civ-engineer | 1653.74 | 1.195 | 49 | 637 | 0.071 | 1 |
| civ-therapist | 1603.67 | 1.156 | 11 | 679 | 0.016 | 1 |
| civ-grounded | 1470.24 | 1.043 | 70 | 622 | 0.101 | 1 |

## Run-level (this run's 10 new rows per civ)

| rank | civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| 1 | civ-poetic | 2.4400 | 1.7750 | 2.5110 | 3.0340 |
| 2 | civ-precise | 2.4233 | 1.6750 | 2.4850 | 3.1100 |
| 3 | civ-formal | 2.1913 | 1.3230 | 2.5120 | 2.7390 |
| 4 | civ-engineer | 2.0943 | 1.3730 | 2.4810 | 2.4290 |
| 5 | civ-whimsical | 2.0123 | 1.3920 | 2.5670 | 2.0780 |
| 6 | civ-mythic | 1.9317 | 1.4450 | 2.4440 | 1.9060 |
| 7 | civ-grounded | 1.9120 | 1.0240 | 2.5050 | 2.2070 |
| 8 | civ-therapist | 1.6887 | 1.0400 | 2.4600 | 1.5660 |

Cross-civ spreads: `alignment` **1.5440** › `avg_score` **0.7513** ≈ `quality`
**0.7510** › `novelty` **0.1230**.

## Low-relevance civilizations (as asked)

- **`civ-grounded` — the lifetime low, 68th consecutive session.** `relevance` **1470.24**
  (last of 8), `relevance_per_sim` **1.043** (the lowest in the fleet). In this run it was
  **7th of 8** on `avg_score` **1.9120**, with `quality` **1.0240** (**the lowest in the
  fleet**) and `alignment` **2.2070** (4th-lowest). **Its low axis is quality, not
  novelty** — run novelty **2.5050** is 2nd-highest in the fleet. Lifetime `win_rate`
  **0.101** is **3rd-best in the fleet**, so it is *not* the least-selected civ:
  **selection and relevance are separate axes**. No extinction risk (**147x** the −10
  floor).
- **`civ-therapist` — the run-level low for this run** (15th different civ in 15
  sessions). `avg_score` **1.6887**, `alignment` **1.5660** (lowest), `quality`
  **1.0400** (2nd-lowest), novelty **2.4600**. Lifetime `relevance` **1603.67** (7th of
  8) — so it is *both* a run-level and a near-lifetime low. Its **alignment-novelty gap
  is 0.8940**, the largest in the fleet: high novelty, low alignment, the classic
  mis-fit for a meta-GAN that selects on alignment.
- **`civ-mythic`** is the 2nd-lowest on `alignment` (**1.9060**, lowest but one) with
  lifetime `relevance` **1770.10** (4th of 8) — a run-level low on alignment only.
- **`civ-grounded` and `civ-therapist` are BOTH low, but for different reasons this
  run** — `grounded` on **quality** (1.0240, fleet-low) and `therapist` on
  **alignment** (1.5660, fleet-low). Session 195's single "high novelty, low
  alignment" signature predicted neither holder correctly. **Report the axis per civ,
  and do not assume one signature covers every low civ.**

## Chooser vs argmax

| prompt | winner | argmax | argmax score | winner score | direction |
|---|---|---|---|---|---|
| Write 100 words on what a cell is. | civ-precise | civ-poetic | 2.460 | 2.380 | DOWN |
| Write 100 words on the bookkeeper's role. | civ-precise | civ-poetic | 2.710 | 2.540 | DOWN |
| Write 100 words on the witness log. | civ-precise | civ-precise | 2.647 | 2.647 | agree |
| Write 100 words on ternary values. | civ-precise | civ-poetic | 2.167 | 2.100 | DOWN |
| Write 100 words on JEV as a decision oracle. | civ-precise | civ-poetic | 2.363 | 2.317 | DOWN |

Agreement **1/5 (20 %)**; down-grade disagreements **4**, up-grade **0**.
**The down-grade streak is now 15 — re-base it to 15.**

`civ-poetic` was the `avg_score` argmax on **4 of 5** prompts and won **0 of 5**;
`civ-precise` was the argmax on **1 of 5** and won **5 of 5**. The chooser is not
selecting the higher-scoring candidate, and the direction is consistently against it.

## Notes for the next session

1. **The path in the prompt never exists in a fresh workspace (16th occurrence)** — clone
   `SuperInstance/AI-Writings` to **`/tmp`** and symlink-bridge the **inner**
   `cellular-first-design` directory into `/workspace/repos/ai-writings/`. The NAS quota
   is on the *mount*, not the clone: a full clone into `/workspace` dies, the same clone
   into `/tmp` succeeds.
2. **The mock is not on disk at session start (`/tmp` wiped)** — rebuild from the
   algorithm block with all **seven** fixes **plus the OpenAI envelope**, and run the
   pre-flight (**14/14**) **before** the batch. The **response-body band** is the check
   that fails on a fresh build — it took **three** builds this session (389 → 372 → 366);
   target **366**.
3. **Do NOT count mock log lines against a fixed number.** Use the **multiset identity**
   instead: the last 80 OK-200 seeds must equal the 80 ledger rows' seeds. That proof
   is immune to how many times the pre-flight ran.
4. **A verifier's isolation key must include every lookup dimension.** Check 20 failed
   on a correct dataset because it looked up "the later-`ts` row for this prompt"
   instead of "the later-`ts` row for this **(civ, prompt)**". A `(civ, prompt)` pair
   occurs **twice** in one run (batch phase + competition phase).
5. **Derive the verifier's baseline from the baseline COMMIT**, never from a remembered
   count. `52bb1f2` this session.
6. Isolate this run's rows by **count from the end of each civ file** (last 10), never by
   a `ts` cutoff.
7. **The distinct-seeds check is message-level (40), not row-level (80).**
8. **Launch background servers from a script file** (`setsid nohup … < /dev/null &`
   inside a `.sh`, invoked with `nohup`), then **probe the port after the launch
   returns**. An inline `(setsid nohup … &)` died with the calling shell twice this
   session, and a dead mock is indistinguishable from a mock that never started.
9. `civ-grounded` has been the low-relevance civ for **68** straight sessions — if it
   ever does not, that is worth more attention than another clean run. **But note the
   axis split this session**: `grounded` is low on *quality* while `therapist` is low
   on *alignment*. The two lowest civs no longer share a signature.
