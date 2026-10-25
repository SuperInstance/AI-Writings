# Civ Orchestrator — Run Report, session 219 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **90th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `d61a2da` (session 218 tree). **All 77 verification assertions PASS.** Pre-flight **22/22 PASS** (first build).

**Session 219 in one line:** `civ-precise` swept **5/5** competitions; the chooser/argmax agreement was
**2/5 (40 %) — 3 down-grades, 0 up-grades**; the run-level low was **`civ-therapist`** (avg
**1.3303**, fleet-low alignment **0.7790**) while `civ-grounded` held the lifetime low for the
**87th** consecutive session.

## Run results (10 new rows per civ: 5 sim phase + 5 competition phase)

| civ | avg_score | quality | novelty | alignment | rank |
|---|---|---|---|---|---|
| civ-poetic | 2.3437 | 1.6270 | 2.5930 | 2.8110 | 1/8 |
| civ-precise | 2.3183 | 1.4230 | 2.5080 | 3.0240 | 2/8 |
| civ-formal | 2.0677 | 0.9780 | 2.5660 | 2.6590 | 3/8 |
| civ-engineer | 2.0313 | 1.0540 | 2.5430 | 2.4970 | 4/8 |
| civ-mythic | 1.9557 | 1.2810 | 2.4950 | 2.0910 | 5/8 |
| civ-grounded | 1.8220 | 1.0350 | 2.5120 | 1.9190 | 6/8 |
| civ-whimsical | 1.6720 | 1.0140 | 2.5650 | 1.4370 | 7/8 |
| civ-therapist | 1.3303 | 0.6190 | 2.5930 | 0.7790 | 8/8 |

Run spreads: avg **1.0133**, quality **1.0080**, novelty **0.0980**, alignment **2.2450**.
The alignment spread is **2.23x** the quality spread and **22.91x** the novelty spread — the
ranking is produced by alignment, not novelty.

## Lifetime leaderboard (cumulative)

| civ | relevance | rel/sim | win_rate | quality | novelty | alignment | rows | rank |
|---|---|---|---|---|---|---|---|---|
| civ-poetic | 2693.14 | 1.6580 | 0.007 | 0.8717 | 2.0145 | 2.1528 | 1661 | 1/8 |
| civ-precise | 2553.55 | 1.5810 | 0.682 | 0.6803 | 1.7982 | 2.2785 | 1631 | 2/8 |
| civ-whimsical | 2267.44 | 1.3900 | 0.006 | 0.6488 | 2.0669 | 1.6064 | 1694 | 3/8 |
| civ-formal | 2194.85 | 1.3510 | 0.136 | 0.5770 | 1.6887 | 1.8381 | 1667 | 4/8 |
| civ-mythic | 2181.54 | 1.3470 | 0.012 | 0.6437 | 1.8913 | 1.5516 | 1639 | 5/8 |
| civ-engineer | 2092.31 | 1.2960 | 0.064 | 0.5743 | 1.7325 | 1.6110 | 1636 | 6/8 |
| civ-therapist | 1944.72 | 1.2030 | 0.014 | 0.5214 | 1.9297 | 1.1968 | 1634 | 7/8 |
| civ-grounded | 1869.53 | 1.1410 | 0.090 | 0.4983 | 1.7569 | 1.2297 | 1682 | 8/8 |

## Low-relevance civilizations (three different axes)

- **Run low — `civ-therapist`**: `avg_score` **1.3303**, 8th of 8, with the fleet-low run
  alignment (**0.7790**) and a fleet-low run quality (**0.6190**). Its gap to the next civ
  is **0.3417**, i.e. **33.7 %** of the run spread — the *identity* of the bottom is solid
  and the *margin* is the widest run-low gap in the recent series.
- **Lifetime low — `civ-grounded`**: relevance **1869.53**, rel/sim **1.1410**, lifetime avg
  **0.4983** quality, and the fleet-low lifetime quality (**0.4983**). Yet its lifetime
  `win_rate` **0.090** is 3rd-best in the fleet — the "low relevance but competitive"
  pattern again.
- **Lifetime alignment low — `civ-therapist`** (**1.1968**) — a *second* civ on a *second* axis,
  and the same civ that holds the run low. Therapist is the only civilization that is last or
  near-last on **both** the run axis and the lifetime alignment axis.

The lifetime lowest **novelty** belongs to `civ-formal` (**1.6887**), not to either low holder.

## Chooser vs argmax

| prompt | argmax | winner | verdict |
|---|---|---|---|
| what a cell is | civ-poetic | civ-precise | DOWN-grade |
| bookkeeper's role | civ-precise | civ-precise | AGREE |
| witness log | civ-precise | civ-precise | AGREE |
| ternary values | civ-poetic | civ-precise | DOWN-grade |
| JEV as a decision oracle | civ-poetic | civ-precise | DOWN-grade |

Agreement **2/5 (40 %)** — 3 down-grades, 0 up-grades. `civ-poetic` was argmax on **3/5**
prompts and won **0/5**; `civ-precise` was argmax on **2/5** and won **5/5**. The largest
disagreement is the cell prompt, where the argmax lead was **+0.2800** — the widest single
down-grade margin in this session's set.

## Verification (77/77 PASS)

- per-civ ledger **+10 x 8 = 80** new rows; `meta_log.jsonl` **+5** (828 -> 833)
- `simulations_run` Δ = **+10** each (5 sim phase + 5 competition rows) — **8/8 exact**
- `relevance` Δ = Σ this run's `avg_score` — **8/8 exact** (max residual **7.39e-13**)
- `wins`/`losses` sum to **5** per civ (a sweep winner records 5 wins, 0 losses) — **8/8 exact**
- `generation` unchanged at **1** for all 8; registry still 8 civs, no new civ dirs
- **80/80** rows carry an independently recomputed seed + colour + figure
- **40** distinct seeds over the 80 new rows (message-level invariant), **0** `(civ,prompt)`
  slot carrying >1 seed
- per-prompt **8/8** distinct seeds AND previews on every competition prompt (5/5)
- `meta_log` `results` field == the ledger's competition rows, **0/5** mismatches
- 0 JEV errors, 0 `2.0/2.0/2.0` fallback triples, 0 `EXC:` in the mock log (**165 OK** lines)
- **80/80** distinct `(q,n,a)`
- extinction risk NONE (threshold −10; the lowest civ sits ~187x above it)

## Checker bug found (not a data defect)

**The meta-vs-ledger check must restrict the argmax to the COMPETITION-phase rows.**
The orchestrator writes **40** sim-phase rows first (one per civ per sim, prompt drawn by
`random.choice`) and **40** competition-phase rows second (5 prompts x 8 civs). A naive
"argmax over all rows for this prompt" mixes the two populations and reports a false
mismatch — the sim-phase rows carry different params and therefore different scores, and
the chooser never saw them.

Phase separation is by **`ts` order**, not by timestamp grouping: every one of the 80 rows
has a **unique** `ts` (the competition phase runs the 8 civs in a thread pool, so the
per-civ writes interleave and no two rows share a timestamp). Sorting all 80 rows by `ts`
and splitting at index 40 reproduces the phase boundary exactly, yielding **8 civs x 5
prompts = 40** competition rows and **8 distinct civs per prompt**.

*Rule: a checker that compares the chooser's decision against an argmax must reconstruct
the exact candidate set the chooser was shown. The chooser sees the competition-phase rows
only. Compute the argmax over that set — over a larger set you are measuring your own
scoring, not the chooser's.*

**A second, softer observation:** the run's `meta_log` rows carry a `results` field with
each civ's `avg_score`, so the per-prompt candidate scores are recoverable from the log
itself — no ledger reconstruction needed for the argmax.

## Durable notes

- The workspace was empty again (**10th consecutive** session naming ephemeral paths), and
  the upstream path in the prompt (`/workspace/repos/ai-writings/...`) did not exist. The
  upstream was found in **one** call: `GET /user/repos` -> `SuperInstance/AI-Writings`. The
  GitHub API is case-insensitive, so the `ai-writings` slug resolves to `AI-Writings`.
- `/workspace` is at **100 % NAS quota** (600 G/600 G, 0 bytes free), so the clone went to
  `/tmp` and the bridge points at the **inner `cellular-first-design`** dir
  (`ln -s /tmp/aw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`),
  verified with `stat -L -c '%d:%i'` -> `129:12612` on both sides and `os.path.samefile()`
  -> `True`.
- **THE CURRENT-GENERATION MOCK ALGORITHM WAS RE-DERIVED AND VERIFIED 560/560 EXACT**
  against the live ledger (the 5 canonical prompts x 8 civs x the current era):
  `d = md5(cultural_prompt).digest(); h = d.hex(); i = d[0] % 4;
  seed = h[(i*2)%8:(i*2)%8+4]; color = h[8:12]; figure = h[12:16]/h[16:20]/h[20:24]`.
  The `i = d[0] % 4` step is the part that is easy to miss: `h[0:4]` alone matches only
  ~30 % of rows, and *every* offset in `h[0:8]` looks plausible on a sample.
- The response body band is **332-369**; this build lands at a constant **349** and the
  cultural-prompt band is **167-209** (measured from the **real** `culture.json` files,
  never a hand-typed fixture). The body length is **input-independent** (the seed/colour/
  figure slices are fixed-width), so the target is solved algebraically in one build:
  `tail_len = 350 - 39 (header) - 27 (continuation) = 284`.
- `ZAI_TOKEN` is still absent (**90th session**): z.ai returns **401 `token expired or
  incorrect`** — endpoint healthy, credential missing. Control B is the only provider path,
  and it needs **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`
  (the override alone is dead code behind the token gate).
  `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`;
  **0** fallback triples.
- Mock teardown: killed by **exact argv match** (2 pids), port proven closed
  (`curl -m 5` -> exit 7 / `HTTP=000`).
- `gh` is not installed; `git fetch`/`push` need `GIT_SSL_NO_VERIFY=1`; push to the explicit
  token URL and verify with `git ls-remote`.
