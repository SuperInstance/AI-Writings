# Civ Orchestrator — Run Report, session 226 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

- Provider path: **Control B mock** (z.ai credential gap, **90th session**) + **live JEV** (`jev-1.14.0`, HTTP 200).
- Baseline: `906f79d` (session 225 tree), `refs/heads/main` asserted equal to the clone HEAD.
- **Pre-flight gate: 14/14 PASS** (first build). **Run verification: 14/14 PASS.**

## Session 226 in one line

`civ-precise` swept **5/5** competitions with **5/5 (100 %)** chooser/argmax agreement — the
first perfect-agreement session since session 216 and the first clean sweep-and-agreement
since then; the run-level low rotated to **`civ-mythic`** (avg **0.6120**, fleet-low run
quality **0.0440** and fleet-low run alignment **0.0410**) while `civ-grounded` held the
lifetime low for the **90th** consecutive session (relevance **1985.69**, rel/sim **1.162**).

## Verification (14/14 PASS)

| Check | Result |
|---|---|
| ledger delta | **+10 rows x 8 civs = 80** |
| `meta_log.jsonl` delta | **+5** |
| provider | **`zai` on 80/80** |
| JEV errors / `2.0/2.0/2.0` fallback triples | **0 / 0** |
| `content_preview` vs independently recomputed mock header | **80/80** |
| distinct seeds in run | **40/80 rows** |
| `(civ,prompt)` pairs with >1 seed | **0** |
| seed multiset identity (mock log last 80 == ledger 80) | **exact** (165 log lines) |
| `relevance` delta vs Σ this run's `avg_score` | **8/8 exact** (max dev 6.8e-13) |
| counter gap vs **full** ledger | grounded −84.35, whimsical −173.14, formal −85.53, poetic −96.80, precise −32.63, mythic −51.11, therapist −42.11, engineer −44.24 — **all at the documented stable values** |
| `wins`/`losses` vs `meta_log.winner_civ` | **8/8 exact** |
| `simulations_run` | **+10** on all 8 |
| `generation` | **unchanged** (no mutation in a non-loop run) |

## Low relevance

**Run low — `civ-mythic`:** avg **0.6120**, run quality **0.0440** (fleet-low), run alignment
**0.0410** (fleet-low), run novelty **1.7510** (fleet-low). Gap to the next civ
(`civ-therapist`, 0.6743) = **0.0623 = 6.0 %** of the run spread **1.0383**.

**The signature is LOW ALIGNMENT, and this session it is low on ALL THREE axes.** The run's
alignment spread **2.3520** is **5.43x** the quality spread (**0.4330**) and **7.13x** the
novelty spread (**0.3300**). The meta-GAN selects on alignment, so this is a *voice* failure.
`civ-mythic` is the only civ in the fleet that is simultaneously lowest on quality,
novelty **and** alignment — a different signature from the usual "high novelty, low
alignment" run-low.

**Lifetime low — `civ-grounded`:** relevance **1985.69**, rel/sim **1.162**, lifetime avg
**1.1815**, fleet-low lifetime quality **0.5137** — yet its lifetime `win_rate` **0.088** is
**3rd-best** in the fleet. The three lifetime axes are still three different civs:
quality low `civ-grounded` (0.5137), alignment low `civ-therapist` (1.1879), novelty low
`civ-formal` (1.7142).

**Run low ≠ lifetime low ≠ axis low — report the axis, not the holder.**

## Chooser series

Session 226: `civ-precise` 5 wins, agreement **5/5 (100 %)**, **0 down-grades, 0
up-grades**. The series (sessions 211-226) now reads
0 / 40 / 40 / 20 / 100 / 60 / 40 / 40 / 20 / 40 / 20 / 40 / 40 / 100 % — *re-derive it
every session; the up-grade count is still **0** across the whole series.*

## Durable notes

1. **THE `0/40` RECOMPUTE WAS A **GATE** GROUP-UNPACKING BUG, NOT A BROKEN MOCK — AND THE
   `#`-PREFIX TRAP HAD ALREADY FIRED 3 TIMES.** The mock's regex yields **FIVE** groups
   `(seed, colour, fig1, fig2, fig3)`; the verifier unpacked **three**
   `(s, c, f)`, so `pr[2]` held only `c8a2` instead of the joined `c8a2/50a5/dcdd` and
   every row mismatched. A hand-dump of one real body confirmed seed `446f`, colour
   `d64d`, figure `c8a2/50a5/dcdd` matched the recompute **exactly** — the mock was
   perfect and only the comparison was wrong. *The figure must be reassembled as a
   slash-joined string before comparing; a `0/N` recompute is a **parser** diagnosis until
   proven otherwise.*
2. **THE GATE AND THE VERIFIER EACH HAD THEIR OWN FIELD-NAME MISMATCH, AND BOTH SURFACED AS
   `KeyError`, NOT AS A FALSE FAIL.** The baseline snapshot stores `relevance` while
   `culture.json` stores `relevance_score`. A blind search-and-replace across the file
   fixed one occurrence and broke the other. *Name the two sides explicitly before
   editing; a `KeyError` mid-verification is a verifier bug, never a data defect.*
3. **A 100 % AGREEMENT SESSION IS A 5-SAMPLE POINT AT 100 %, NOT A NEW REGIME.** It sits on
   a series that also contains 0 % and 20 % points. The honest claim is *agreement can
   reach 5/5*, not *agreement is 100 %*. The up-grade count across the whole 16-session
   series is still **0**.
4. **THE MOCK BODY LANDED AT **349** CHARS ON THE FIRST BUILD** — 39-char header + a
   310-char fixed, culture-free tail, computed algebraically from the target rather than
   by iterating prose. *Compute the allowance from the fixed prefix.*
5. **THE REPO IS `SuperInstance/AI-Writings` AND `cellular-first-design` IS A SUBDIRECTORY.**
   `git ls-remote` on the `ai-writings/cellular-first-design` slug returns *Repository not
   found*. The owner is a **user** account with 5 400+ repos, so `GET /user/repos` must be
   paged and filtered on `cellular|civ|writing|autoclaw`.
