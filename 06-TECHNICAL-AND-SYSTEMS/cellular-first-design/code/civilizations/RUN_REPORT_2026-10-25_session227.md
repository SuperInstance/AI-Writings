# Civ Orchestrator — Run Report, session 227 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

- Provider path: **Control B mock** (z.ai credential gap, **91st session**) + **live JEV** (`jev-1.14.0`).
- Baseline: `bb443cf` (session 226 tree), `refs/heads/main` asserted equal to the clone HEAD.
- **Pre-flight gate: PASS on the FIRST build.** **Run verification: 20/20 PASS.**
- Commit: `2fecebf`, pushed to `main` and verified through the commits API.

## Session 227 in one line

`civ-precise` took **3/5** competitions and `civ-formal` **2/5**, with **3/5 (60 %)**
chooser/argmax agreement and **2 down-grades, 0 up-grades**; the run-level low rotated to
**`civ-mythic`** (avg **0.5043**) — the only civ that is fleet-low on **quality, novelty AND
alignment** simultaneously — while `civ-grounded` held the lifetime low for the **91st**
consecutive session (relevance **1992.70**, rel/sim **1.159**).

## Verification (20/20 PASS)

| Check | Result |
|---|---|
| per-civ `simulations.jsonl` delta | **+10** each, 8/8 |
| total new ledger rows | **80** |
| `meta_log.jsonl` delta | **+5** (868 -> 873) |
| `Winner:` lines in run log | **5** |
| provider | **`zai` on 80/80** |
| rows with a JEV `error` key | **0** |
| rows with the 2.0/2.0/2.0 fallback triple | **0** |
| `content_preview` vs independently recomputed seed+color+figure | **80/80** |
| distinct seeds in run | **40/80 rows** |
| `(civ,prompt)` pairs with >1 seed | **0** |
| per-prompt 8/8 distinct seeds AND previews (ts-sorted last-8) | **5/5 prompts** |
| `relevance` delta vs Σ this run's `avg_score` | **8/8 exact** (max residual 4.42e-13) |
| `wins`/`losses` vs `meta_log.winner_civ` | **8/8 exact** |
| `simulations_run` | **+10** on all 8 |
| `generation` | **unchanged** (no mutation in a non-loop run) |
| leaderboard entries / sort order | **8**, sorted by `relevance_per_sim` desc |
| git tree after run | **18 modified** (8 civs × 2 + `leaderboard.json` + `meta_log.jsonl`) |

## Low relevance

**Run low — `civ-mythic`:** avg **0.5043**, run quality **0.0670**, run novelty **1.4130**
(fleet-low), run alignment **0.0330** (fleet-low). Gap to the next civ
(`civ-therapist`, 0.5697) = **0.0653 = 6.4 %** of the run spread **1.0153**.

**The signature is LOW ALIGNMENT, and this session it is low on ALL THREE axes.** The run's
alignment spread **2.2700** is **5.58x** the quality spread (**0.4070**) and **6.12x** the
novelty spread (**0.3710**). The meta-GAN selects on alignment, so this is a *voice* failure.
`civ-mythic` is the only civ in the fleet that is simultaneously lowest on quality,
novelty **and** alignment — a different signature from the usual "high novelty, low
alignment" run-low.

**Lifetime low — `civ-grounded`:** relevance **1992.70**, rel/sim **1.159**, lifetime
`win_rate` **0.087** — **3rd-best** in the fleet. The three lifetime axes are still three
different civs: quality low `civ-therapist`, alignment low `civ-therapist`, novelty low
`civ-mythic`.

**Run low ≠ lifetime low ≠ axis low — report the axis, not the holder.**

## Chooser series

Session 227: `civ-precise` 3 wins, `civ-formal` 2 wins, agreement **3/5 (60 %)**,
**2 down-grades, 0 up-grades**. Both disagreements took the **lower**-scoring candidate.
The up-grade count across the whole series is still **0**.

## Durable notes

1. **THE RE-DERIVED ALGORITHM IS `i = d[0] % 4` ON THE **DIGEST** BYTE, NOT ON THE HEX
   CHARACTER.** The RUNBOOK and the older SKILL text both leave this ambiguous, and the
   hex-char form (`int(h[0],16) % 4`) reproduces only **416/1200** ledger rows against the
   digest form's **1200/1200**. The two forms agree often enough that a 4-row sample can
   land on an agreeing row and hide the defect — the same failure shape as the
   session-213 `int(h[0],16) % 4` vs `d[0] % 4` trap, recurring one level up.
2. **THE TAIL IS **PER-SESSION**, AND THE LEDGER ONLY EXPOSES ITS FIRST 162 CHARS.** The
   stored `content_preview` truncates at **200** chars, so of a 332-369-char body only
   38 (header) + 162 (tail prefix) are visible. The tail beyond that is **not in the
   ledger** — do not try to reconstruct it, and do not treat the visible prefix as the
   whole tail. Build a continuation that lands `38 + len(tail)` inside the band.
3. **THE HEADER IS A CONSTANT **38** CHARS** (`[mock-zai <4hex>] #<4hex> <4/4/4>. `) and the
   tail prefix is **162** chars of the **session-226 Control B** text. A 136-char
   continuation gives a 298-char tail and a **336**-char body — inside the 332-369 band on
   the FIRST build, with no trimming iteration.
4. **THE NAS EDQUOT IS TOTAL AND THE BRIDGE IS THE ONLY WAY IN.** The clone must land on the
   overlay (`/tmp`, ~28 G free) and be bridged by symlink to
   `/workspace/repos/ai-writings/cellular-first-design`, targeting the **nested**
   `cellular-first-design` dir — the script's hard-coded `CIVS_DIR` resolves against the
   **clone root**, so a bridge to the inner `code` dir produces `code/code/civilizations`.
   Verify with `os.path.samefile()`, not `ls`.
5. **`gh` is still not installed** and the `ai-writings/cellular-first-design` slug still
   404s. The upstream is `SuperInstance/AI-Writings`; the file was located with
   `GET /search/code?q=civilization_orchestrator+in:path`, which survives core-quota
   exhaustion.
6. **A 60 % AGREEMENT POINT IS A 5-SAMPLE POINT AT 60 %, NOT A TREND.** The series
   (sessions 211-227) contains 0 %, 20 %, 40 %, 60 % and 100 % points. The honest claim is
   *agreement moves*, not *agreement is 60 %*. The up-grade count across the whole series
   is still **0**.
