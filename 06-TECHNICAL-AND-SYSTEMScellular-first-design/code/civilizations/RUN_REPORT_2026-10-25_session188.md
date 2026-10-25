# Civ Orchestrator — Run Report, session 188 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 62nd session) + **live JEV**.
Baseline: `2af1928` (session 187). **All 21 verification assertions PASS.**

## Headline for the next session

- **THE `civ-precise` SWEEP IS THE FIRST 5/5 IN THE SERIES, AND IT IS A CHOOSER EFFECT,
  NOT A QUALITY EFFECT.** `civ-precise` won **5/5** competition prompts. But the
  chooser disagreed with the `avg_score` argmax on **3 of 5** prompts — and **all three
  disagreements took the LOWER-scoring candidate** (argmax `civ-poetic` every time).
  Run `avg_score` leader was `civ-poetic` (**2.2770**) with `civ-precise` second
  (**2.2047**). This is the **9th consecutive session** in which a chooser/argmax
  disagreement is a *down*-grade. **`win_rate` is not a quality metric; `civ-precise`'s
  0.634 lifetime win rate is the chooser's habit, not its merit.**
- **`civ-grounded` remains the lifetime low-relevance civ — 60th consecutive session.**
  Last of 8 on lifetime `relevance` **1325.29** and `relevance_per_sim` **0.997** — still
  the only sub-1.0 figure in the fleet. Run `avg_score` **1.6020**, `alignment` **1.5790**,
  `quality` **0.7280**, novelty **2.4990** (4th of 8). Its lifetime `win_rate` is
  **0.107** — the **2nd-best in the fleet** behind `civ-precise`. Lowest relevance =
  **133x** the −10 extinction floor ⇒ **no extinction risk**.
- **THE RUN-LEVEL LOW ROTATED TO `civ-therapist`** (run `avg_score` **1.3817**,
  `alignment` **0.9030**, `quality` **0.7500**) — an **8th different civ in 8 sessions**.
  Alignment gap to the leader **2.0060** vs quality gap **0.6300** = **3.18x wider** ⇒ a
  **voice** failure, not a prose failure. *The holder rotates; the axis does not.*
- **RELEVANCE DELTA == sum(`avg_score`) 8/8 EXACT** (max residual **4.7e-13**), taken
  against the **git blob** baseline, not the rounded leaderboard.
- **THE LOWEST-RELEVANCE CIV IS NOT THE LEAST-SELECTED ONE.** `civ-grounded` has the
  2nd-best `win_rate` and the worst relevance. Selection and relevance are different
  axes; conflating them hides the actual failure.

## Verification — 21/21 PASS

| # | assertion | result |
|---|---|---|
| 1 | per-civ ledger delta | **+10 x 8 = 80** |
| 2 | total new rows | **80** |
| 3 | `meta_log` | **673 -> 678** (+5) |
| 4 | `Winner:` lines in log | **5** |
| 5 | rows with a JEV `error` key | **0** |
| 6 | 2.0/2.0/2.0 fallback triples | **0** |
| 7 | `provider` on all rows | **`zai` x 80** |
| 8 | rows missing `[mock-zai seed=` prefix | **0** (80/80) |
| 9 | rows matching an independently recomputed seed+color+figure | **80/80** |
| 10 | distinct seeds | **40/40** |
| 11 | `(civ,prompt)` combos with >1 seed | **0** |
| 12 | per-prompt 8/8 distinct seeds (5 prompts) | **8/8 x 5** |
| 13 | relevance delta == sum(avg_score) | **8/8 exact** (max resid 4.7e-13) |
| 14 | wins/losses vs `meta_log.winner_civ` | **8/8 exact** |
| 15 | log `Winner:` == `meta_log.winner_civ` | **5/5 agree** |
| 16 | registry / generations | **8**, all `gen=1` |
| 17 | extinction risk | **NONE** (lowest +1325.29 = 133x floor) |
| 18 | `simulations_run` delta | **+10 x 8** |
| 19 | meta-vs-ledger `avg_score` | **0 mismatches** |
| 20 | leaderboard refreshed | **iso 2026-10-25T08:23:47**, 8 civs |
| 21 | `Traceback` in mock log | **0** |

## Lifetime leaderboard (after run)

| civ | relevance | rel/sim | wins | losses | win_rate | gen |
|---|---|---|---|---|---|---|
| civ-poetic | 2022.40 | 1.539 | 6 | 647 | 0.009 | 1 |
| civ-precise | 1871.40 | 1.434 | 411 | 237 | 0.634 | 1 |
| civ-whimsical | 1757.28 | 1.330 | 5 | 648 | 0.008 | 1 |
| civ-mythic | 1621.21 | 1.239 | 10 | 637 | 0.015 | 1 |
| civ-formal | 1571.79 | 1.195 | 98 | 553 | 0.151 | 1 |
| civ-engineer | 1495.44 | 1.147 | 48 | 598 | 0.074 | 1 |
| civ-therapist | 1474.48 | 1.128 | 11 | 639 | 0.017 | 1 |
| **civ-grounded** | **1325.29** | **0.997** | 70 | 582 | 0.107 | 1 |

## Run-level (this run's 10 new rows per civ)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | 2.2770 | 1.3800 | 2.5920 | 2.8590 |
| civ-precise | 2.2047 | 1.2630 | 2.4420 | 2.9090 |
| civ-formal | 2.0123 | 1.0600 | 2.4660 | 2.5110 |
| civ-engineer | 1.9263 | 1.0960 | 2.4080 | 2.2750 |
| civ-mythic | 1.7510 | 1.0440 | 2.4600 | 1.7490 |
| civ-whimsical | 1.7367 | 0.8900 | 2.5480 | 1.7720 |
| civ-grounded | 1.6020 | 0.7280 | 2.4990 | 1.5790 |
| civ-therapist | 1.3817 | 0.7500 | 2.4920 | 0.9030 |

## Chooser vs `avg_score` argmax — 2/5 (40%)

| prompt | winner | argmax | |
|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | DISAGREE (lower-scored picked) |
| the bookkeeper's role | civ-precise | civ-poetic | DISAGREE (lower-scored picked) |
| the witness log | civ-precise | civ-precise | AGREE |
| ternary values | civ-precise | civ-poetic | DISAGREE (lower-scored picked) |
| JEV as a decision oracle | civ-precise | civ-precise | AGREE |

## Relevance delta vs baseline (git blob)

| civ | before | after | delta | sum(avg_score) |
|---|---|---|---|---|
| civ-grounded | 1309.2733 | 1325.2933 | +16.0200 | 16.0200 |
| civ-therapist | 1460.6633 | 1474.4800 | +13.8167 | 13.8167 |
| civ-whimsical | 1739.9167 | 1757.2833 | +17.3667 | 17.3667 |
| civ-engineer | 1476.1800 | 1495.4433 | +19.2633 | 19.2633 |
| civ-mythic | 1603.7033 | 1621.2133 | +17.5100 | 17.5100 |
| civ-formal | 1551.6633 | 1571.7867 | +20.1233 | 20.1233 |
| civ-precise | 1849.3533 | 1871.4000 | +22.0467 | 22.0467 |
| civ-poetic | 1999.6267 | 2022.3967 | +22.7700 | 22.7700 |

## Environment recovery

- Upstream owner: **`SuperInstance/ai-writings`** (the `ai-writings/...` slug 404s).
  REST API **core quota exhausted (5000/5000, 403)**; located the repo by **web search**
  after `git ls-remote` failed on every guessed owner. The **search API** still had quota
  when core did not — same as session 187.
- Cloned to **`/tmp/ai-writings`** (`--depth 50`) — a clone into `/workspace` dies with
  `Disk quota exceeded` (NAS EDQUOT, 600 G of 600 G, 0 avail). `/tmp` is on the overlay
  (28 G free) and is **not** subject to the EDQUOT trap.
- Bridge: `ln -s /tmp/ai-writings /workspace/repos/ai-writings` (the symlink points at the
  **clone root**). Verified by inode identity (**129:12260**) on both sides and `-ef`.
- `ZAI_TOKEN` absent from env and from the sandbox secret list; `TYPESAFE_AI_TOKEN` present
  (len 108) ⇒ **62nd session** with the z.ai credential gap. `ZAI_URL_OVERRIDE` alone is
  **dead code** — the `ZAI_TOKEN` gate returns `None` first, so Control B needs **both**
  a placeholder token and the override.
- **JEV live**: a well-formed `questions` body returns **HTTP 200**
  `{"model":"jev-1.14.0", ...}`.
- **THE PRE-FLIGHT GATE CAUGHT A REAL DEFECT THIS SESSION.** The canonical spec's
  "body lengths 167-209" is the **cultural-prompt** band, NOT the mock-response band —
  the response band in the learnings file is **332-369**. The first build produced a
  **648-char** body, then **475**, before being trimmed to **334**. A body that is too
  long changes what survives the 200-char `content_preview` truncation, so the seed
  could be cut out of the preview. *Check both bands separately: prompt 167-209, body
  332-369.*
- **THE `civ-precise` 5/5 SWEEP IS A FIRST IN THE SERIES** — and the argmax disagreed
  with it on 3 of 5 prompts. Worth watching: a civ that wins every competition while
  scoring *second* on aggregate is a chooser-preference artefact. If it persists, the
  `best_civ` criteria map (civ_id -> civ name) may be biased toward one candidate.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch, stdout redirected
  **and** `< /dev/null`, then poll the log. The detached launcher never reaps the child
  (`Zs` zombie) ⇒ **verify by the log tail and the row deltas, not by process exit**.
- Mock teardown: killed by **exact argv match** (`python3 /tmp/mock_zai.py` and
  `timeout -s KILL 900 python3 /tmp/mock_zai.py` — **two** pids), never `pkill -f mock_zai`
  (self-match). Port re-probed ⇒ `curl` exit 7 (closed). Mock log: **200** OK lines
  (40 pre-flight + 80 run + 80 repeat-probe), **0** tracebacks.
- `gh` not installed; REST core quota exhausted. Verification used the **git protocol**
  and the **git blob** for the baseline, never the rate-limited API.
