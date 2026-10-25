# Civ Orchestrator — Run Report, session 195 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 69th session) + **live JEV** (`jev-1.14.0`).
Baseline: `1faa07a` (session 194). **All 27 verification assertions PASS.**

## Headline for the next session

- **`civ-precise` SWEPT 5/5 FOR THE FIFTH CONSECUTIVE SWEEP — AND IT IS STILL A CHOOSER
  EFFECT.** The chooser disagreed with the `avg_score` argmax on **4 of 5** prompts and
  **all four took the LOWER-scoring candidate** — the **14th consecutive session** in
  which a chooser/argmax disagreement is a *down*-grade. Agreement **1/5 (20 %)**.
  `civ-poetic` was the argmax on **4 of 5** prompts and won **none**; `civ-precise` was
  the argmax on **1 of 5** and won **5 of 5**. The standing suspect is unchanged: the
  `best_civ` criteria map (`civ_id -> civ name`) being read as a quality signal.
  **Re-base the streak to 14.**
- **`civ-grounded` remains the lifetime low — 67th consecutive session.** Last of 8 on
  lifetime `relevance` **1451.12** and `relevance_per_sim` **1.037** (the lowest in the
  fleet). Lifetime `win_rate` **0.102** — **3rd-best in the fleet** behind `precise`
  (0.652) and `formal` (0.143). Lowest relevance = **145x** the −10 floor ⇒ **no
  extinction risk**. *Selection and relevance are separate axes: the least-relevant civ
  is not the least-selected one.*
- **THE RUN-LEVEL LOW ROTATED TO `civ-whimsical`** (run `avg_score` **2.1440**,
  `alignment` **2.1910** lowest) — a **14th different civ in 14 sessions**. *The holder
  rotates; the axis does not.*
- **THE AXIS SPREAD IS DOMINATED BY ALIGNMENT, NOT QUALITY.** Cross-civ spreads this run:
  `alignment` **1.0780** › `quality` **0.6500** › `avg_score` **0.4933** › `novelty`
  **0.1510**. Novelty is nearly flat across the fleet (2.471–2.622) — the entire ranking
  this run is produced by `alignment` and `quality`. Same shape as sessions 191–194.
- **THE TWO LOW CIVs SHARE ONE SIGNATURE: HIGH NOVELTY, LOW ALIGNMENT.** `civ-whimsical`
  (novelty **2.5810** / alignment **2.1910**) and `civ-therapist` (**2.6220** /
  **2.1930**) both fit; the novelty spread is **0.1510** against an alignment spread of
  **1.0780**. The meta-GAN selects on `alignment`, so novelty does not rescue them.
  **The low-relevance axis is voice, not novelty.**

## Verification — 27/27 PASS

Baseline commit: `1faa07a` (session 194), derived by reading the **git blob** of each
ledger and `culture.json` — never from a remembered count. This run's rows are the
**last 10** per civ ledger; this run's `meta_log` entries are the **last 5**.

| # | assertion | result |
|---|---|---|
| 1 | per-civ ledger delta | **+10 x 8 = 80** |
| 2 | total new rows | **80** |
| 3 | `meta_log` | **+5** (708 -> 713) |
| 4 | `Winner:` lines in log | **5** |
| 5 | rows with a JEV `error` key | **0** |
| 6 | 2.0/2.0/2.0 fallback triples | **0** |
| 7 | `provider` on all rows | **`zai` x 80** |
| 8 | rows missing `[mock-zai` prefix | **0** (80/80) |
| 9 | rows matching an independently recomputed seed+color+figure | **80/80** |
| 10 | distinct seeds (message-level) | **40/40** |
| 11 | `(civ,prompt)` combos with >1 seed | **0** |
| 12 | per-prompt 8/8 distinct seeds (5 prompts) | **8/8 x 5** |
| 13 | per-prompt 8/8 distinct previews (5 prompts) | **8/8 x 5** |
| 14 | relevance delta == sum(avg_score) | **8/8 exact** (max residual **4.01e-13**) |
| 15 | wins/losses vs `meta_log.winner_civ` | **8/8 exact** (precise 5, others 0) |
| 16 | log `Winner:` == `meta_log.winner_civ` | **5/5 agree** |
| 17 | registry / generations | **8**, all `gen=1` |
| 18 | extinction risk | **NONE** (lowest +1451.12 = 145x floor) |
| 19 | `simulations_run` delta | **+10 x 8** |
| 20 | meta-vs-ledger `avg_score` (later-`ts` row, this run's rows only) | **0 mismatches** |
| 21 | leaderboard refreshed | **8 civs**, iso `2026-10-25T09:34:09` |
| 22 | `Traceback` in orchestrator log | **0** |
| 23 | `EXC:` in mock log | **0** |
| 24 | mock OK-200 responses (run-scoped, derived) | **241** |
| 25 | **run-scoped proof**: last 80 OK seed multiset == ledger seed multiset | **PASS** |
| 26 | pre-flight | **14/14 PASS** |
| 27 | no birth (new civ dirs) | **0** |

### The run-scoped proof is new, and it is stronger than a line count

Check 24 used to be a **fixed line count** (161), which is a false-FAIL generator: it
assumes exactly one pre-flight. This session the pre-flight ran **twice** (run 1
crashed at check 12 on a gate bug, run 2 was the full 14/14 pass) and there was one
manual `curl` liveness probe, so the true total is
`40 + 120 + 1 + 80 = 241`. The fixed number reports a false FAIL.

The replacement is a **multiset identity**: the seed multiset of the **last 80** OK-200
log lines must equal the seed multiset of the **80 ledger rows**. That holds exactly, and
it is *independent of how many times the pre-flight ran* — it identifies the batch
window without counting anything. **Prefer a multiset identity over a line count
whenever the artifact can be re-read.**

## Environment recovery

The workspace was **empty** apart from `.plugin-cache` and `.skills` — the prompt's path
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
(**15th consecutive occurrence**).

- Upstream owner: **`SuperInstance/AI-Writings`**. The `ai-writings/…` slug 404s (the
  GitHub API is case-insensitive, and `ai-writings` is a *different* owner with
  README-only marketing repos). `cellular-first-design` is a **subdirectory** of that
  repo, not a repo of its own. The **core** REST quota was **not** exhausted this
  session — `GET /search/repositories` served directly — but the **git protocol** is
  still the fastest absence test.
- The NAS **EDQUOT** trap blocked writes into `/workspace` (`dd` of 2 MB → `Disk quota
  exceeded`, leaving a 0-byte file that still appears in `ls -la`). The bridge is a
  **symlink** to the clone root on the overlay (28 G free).
- **The bridge must point at the INNER `cellular-first-design` directory.** The upstream
  repo root contains a `cellular-first-design/` subdirectory, so the symlink must target
  the **inner** directory, or the orchestrator's hardcoded `CIVS_DIR` misses
  `civilizations.json`. Verified by **inode identity** (`stat -L -c '%d:%i'` → `129:10425`
  on both sides) plus `os.path.samefile()` → `True`; the shell `[ -ef ]` test is
  unreliable here.
- **A FULL CLONE INTO `/workspace` STILL DIES, BUT CLONING INTO `/tmp` WORKS FINE.**
  The `--depth 1` clone straight into `/workspace/repos` failed on
  `.git/description` with `Disk quota exceeded`; the same clone into `/tmp` succeeded
  immediately. **The quota is on the NAS mount, not on the clone.**
- `ZAI_TOKEN` is **absent** from the env (**69th session**); z.ai returns **401 `token
  expired or incorrect`** ⇒ the endpoint is healthy and the **credential** is missing.
  `ZAI_URL_OVERRIDE` alone is dead code behind the token gate, so **both** a placeholder
  `ZAI_TOKEN` and the override were set.
- `JEV_KEY` reads `TYPESAFEAI_KEY` but the env var is `TYPESAFE_AI_TOKEN` ⇒ the alias was
  exported. JEV returned HTTP 200 `{"model":"jev-1.14.0"}`; **0 fallback triples**.
- `gh` not installed — used the REST API with `GITHUB_TOKEN`.
- **No concurrent session**: the remote tip was still `1faa07a` (session 194) before the
  push, so this run is a clean session **195** with no concatenation needed.

## Mock rebuild — the eight fixes, and the band that caught the build

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

**The response-body length band did its job again.** A first template rendered at
**387** characters against the **332–369** band; the gate reported
`[FAIL] response body length band 332-369 min=387 max=387` — a clean, localised FAIL.
Trimming the tail to **297** put the body at **351**, in band. The cultural-prompt band
(**167–209**) passed unchanged.

The band is not cosmetic: a body longer than ~369 characters pushes the **seed prefix out
of the 200-char `content_preview` truncation**, which would silently break the
seed+color+figure recompute check for every row.

**PRE-FLIGHT PASSED 14/14 ON THE FIRST CLEAN BUILD.** The gate now has **14** checks
(the prior session's 13 plus an explicit **OpenAI envelope shape** assertion), reads the
**real** `culture.json` files rather than a hand-typed fixture, and includes the
**repeat-same-message determinism probe** (40 messages × 2 repeats) that a
distinctness-only gate can never certify.

## Lifetime leaderboard (after session 195)

| civ | relevance | rel/sim | wins | losses | win_rate | gen |
|---|---|---|---|---|---|---|
| civ-poetic | 2179.77 | 1.575 | 6 | 682 | 0.009 | 1 |
| civ-precise | 2025.16 | 1.473 | 445 | 238 | 0.652 | 1 |
| civ-whimsical | 1882.10 | 1.353 | 5 | 683 | 0.007 | 1 |
| civ-mythic | 1750.78 | 1.270 | 10 | 672 | 0.015 | 1 |
| civ-formal | 1717.50 | 1.240 | 98 | 588 | 0.143 | 1 |
| civ-engineer | 1632.80 | 1.188 | 49 | 632 | 0.072 | 1 |
| civ-therapist | 1586.78 | 1.152 | 11 | 674 | 0.016 | 1 |
| civ-grounded | 1451.12 | 1.037 | 70 | 617 | 0.102 | 1 |

## Run-level (this run's 10 new rows per civ)

| rank | civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| 1 | civ-poetic | 2.6373 | 2.1320 | 2.5110 | 3.2690 |
| 2 | civ-formal | 2.5493 | 1.9400 | 2.4710 | 3.2370 |
| 3 | civ-engineer | 2.5253 | 1.9640 | 2.5540 | 3.0580 |
| 4 | civ-mythic | 2.4997 | 1.9000 | 2.5130 | 3.0860 |
| 5 | civ-precise | 2.4613 | 1.7750 | 2.4860 | 3.1230 |
| 6 | civ-grounded | 2.2883 | 1.4820 | 2.6040 | 2.7790 |
| 7 | civ-therapist | 2.1717 | 1.7000 | 2.6220 | 2.1930 |
| 8 | civ-whimsical | 2.1440 | 1.6600 | 2.5810 | 2.1910 |

Cross-civ spreads: `alignment` **1.0780** › `quality` **0.6500** › `avg_score`
**0.4933** › `novelty` **0.1510**.

## Low-relevance civilizations (as asked)

- **`civ-grounded` — the lifetime low, 67th consecutive session.** `relevance` **1451.12**
  (last of 8), `relevance_per_sim` **1.037** (the lowest in the fleet). In this run it was
  **6th of 8** on `avg_score` **2.2883**, with `quality` **1.4820** (the lowest in the
  fleet) and `alignment` **2.7790** (4th-lowest). **Its low axis is quality, not novelty**
  — run novelty **2.6040** is 2nd-highest in the fleet. Lifetime `win_rate` **0.102** is
  **3rd-best in the fleet**, so it is *not* the least-selected civ: **selection and
  relevance are separate axes**. No extinction risk (**145x** the −10 floor).
- **`civ-whimsical` — the run-level low for this run** (14th different civ in 14
  sessions). `avg_score` **2.1440**, `alignment` **2.1910** (lowest), `quality`
  **1.6600** (2nd-lowest), novelty **2.5810** (3rd-highest). Lifetime `relevance`
  **1882.10** (3rd of 8) — so it is a *run-level* low, not a lifetime one. The gap to
  the next civ is **0.0277** on `avg_score` — this run's bottom two were separated by
  less than a tenth of a point on `avg_score`, but by **0.9660** on `alignment`.
- **`civ-therapist`** is the other low-`alignment` civ this run (**2.1930**, 2nd-lowest)
  with lifetime `relevance` **1586.78** (7th of 8) — a *run-level* low on alignment
  despite a low lifetime standing too. Its `quality` **1.7000** is 3rd-lowest and its
  novelty **2.6220** is the **highest in the fleet**.

**The two low civs share one signature: high novelty, low alignment.** `civ-whimsical`
(novelty 2.5810 / alignment 2.1910) and `civ-therapist` (2.6220 / 2.1930) both fit. The
novelty spread is **0.1510** against an alignment spread of **1.0780**, so **the ranking
is produced by alignment and quality, not novelty**. Report the axis, not the holder.

## Chooser vs argmax

| prompt | winner | argmax | argmax score | winner score | direction |
|---|---|---|---|---|---|
| Write 100 words on what a cell is. | civ-precise | civ-poetic | 2.707 | 2.403 | DOWN |
| Write 100 words on the bookkeeper's role. | civ-precise | civ-poetic | 2.880 | 2.757 | DOWN |
| Write 100 words on the witness log. | civ-precise | civ-precise | 2.820 | 2.820 | agree |
| Write 100 words on ternary values. | civ-precise | civ-poetic | 2.343 | 2.163 | DOWN |
| Write 100 words on JEV as a decision oracle. | civ-precise | civ-poetic | 2.693 | 2.523 | DOWN |

Agreement **1/5 (20 %)**; down-grade disagreements **4**, up-grade **0**.
**The down-grade streak is now 14 — re-base it to 14.**

`civ-poetic` was the `avg_score` argmax on **4 of 5** prompts and won **0 of 5**;
`civ-precise` was the argmax on **1 of 5** and won **5 of 5**. The chooser is not
selecting the higher-scoring candidate, and the direction is consistently against it.

## Notes for the next session

1. **The path in the prompt never exists in a fresh workspace (15th occurrence)** — clone
   `SuperInstance/AI-Writings` to **`/tmp`** and symlink-bridge the **inner**
   `cellular-first-design` directory into `/workspace/repos/ai-writings/`. The NAS quota
   is on the *mount*, not the clone: a full clone into `/workspace` dies, the same clone
   into `/tmp` succeeds.
2. **The mock is not on disk at session start (`/tmp` wiped)** — rebuild from the
   algorithm block with all **seven** fixes **plus the OpenAI envelope**, and run the
   pre-flight (**14/14**) **before** the batch. The **response-body band** is the check
   that fails on a fresh build if the template is not trimmed — target **351**.
3. **Do NOT count mock log lines against a fixed number.** This session the pre-flight
   ran twice and the log read **241** OK-200, not 161. **Use the multiset identity
   instead**: the last 80 OK-200 seeds must equal the 80 ledger rows' seeds. That proof
   is immune to how many times the pre-flight ran.
4. **A GATE BUG PRODUCED A CRASH AFTER 12 PASSES, AND A FIXED-NUMBER CHECK THEN
   REPORTED A FALSE FAIL.** The gate unpacked a 3-tuple as a 4-tuple at the repeat
   probe. Two lessons: (a) **a gate must print a final verdict and exit non-zero** —
   12 PASS lines then a traceback is not a pass; (b) the *verifier*'s fixed 161 is
   exactly the kind of constant that a re-run breaks.
5. **Derive the verifier's baseline from the baseline COMMIT**, never from a remembered
   count — a stale `BASE_META` from the previous epoch reports a false FAIL.
6. Isolate this run's rows by **count from the end of each civ file** (last 10), never by a
   `ts` cutoff; the meta-vs-ledger check takes the **later-`ts`** row **within this run's
   rows only**.
7. **The distinct-seeds check is message-level (40), not row-level (80).** Assert 40
   distinct seeds + one seed per `(civ, prompt)` slot + multiplicity == slot row count.
8. `civ-grounded` has been the low-relevance civ for **67** straight sessions — if it ever
   does not, that is worth more attention than another clean run.
