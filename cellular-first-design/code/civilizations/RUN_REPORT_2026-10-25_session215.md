# Civ Orchestrator — Run Report, session 215 (2026-10-25)

`--sims 5 --prompts 5 --providers zai` · 8 civs · Control B mock provider · JEV live (`jev-1.14.0`)

## Headline

- **Run: CLEAN.** 8 civs x 5 sims = 40 sim rows, plus 5 competition rounds x 8 civs = 40 more => **80 new ledger rows**, +10 per civ, every civ.
- **Pre-flight gate: PASS 10/10** (40/40 distinct seeds, 40/40 independently recomputed md5s, repeat-probe stable, body band 332-369, cultural-prompt band 167-209).
- **Counter gap: stable 8/8** at the documented stable values, deltas <= 3.3e-7.
- **0 JEV fallbacks, 0 provider errors, 0 header-parse failures, 40/40 distinct seeds.**
- **Chooser vs argmax agreement: 1/5 (20%)**, and all **4 disagreements took the LOWER-scoring candidate** (4 down-grades, 0 up-grades).

## Verification (the `ls -la` check)

`ls -la` on the civs dir **fails without `-L`** because the last path component crosses the symlink bridge. Use `ls -laL`.

| civ | rows before | rows after | delta | mtime |
|---|---|---|---|---|
| civ-engineer | 1586 | 1596 | **+10** | 12:55:12 |
| civ-formal | 1617 | 1627 | **+10** | 12:55:12 |
| civ-grounded | 1632 | 1642 | **+10** | 12:55:12 |
| civ-mythic | 1589 | 1599 | **+10** | 12:55:12 |
| civ-poetic | 1611 | 1621 | **+10** | 12:55:12 |
| civ-precise | 1581 | 1591 | **+10** | 12:55:12 |
| civ-therapist | 1584 | 1594 | **+10** | 12:55:12 |
| civ-whimsical | 1644 | 1654 | **+10** | 12:55:12 |
| **TOTAL** | **12844** | **12924** | **+80** | |

`meta_log.jsonl` 808 -> **813** (+5 competitions). `leaderboard.json` rewritten.

## Run-level results (this session's 80 rows)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-engineer | 1.7437 | 0.8950 | 2.4530 | 1.8830 |
| civ-whimsical | 1.7877 | 1.0670 | 2.5870 | 1.7090 |
| civ-mythic | 1.8727 | 1.1440 | 2.5090 | 1.9650 |
| civ-therapist | 1.8937 | 1.0280 | 2.5720 | 2.0810 |
| civ-formal | 1.9067 | 1.0430 | 2.4340 | 2.2430 |
| civ-grounded | 1.9350 | 1.1180 | 2.4440 | 2.2430 |
| civ-precise | 2.2287 | 1.4780 | 2.4130 | 2.7950 |
| civ-poetic | 2.2453 | 1.4290 | 2.5560 | 2.7510 |

**RUN SPREADS** — avg 0.5017, quality 0.5830, novelty 0.1740, **alignment 1.0860**.
**Alignment spread = 1.86x the quality spread and 6.24x the novelty spread.**
The ranking is produced by **alignment**, not novelty — novelty is nearly flat across the fleet.

**RUN LOW: `civ-engineer`** (avg 1.7437, alignment 1.8830).
Gap to next (civ-whimsical) is 0.0440 = **8.8% of the spread** — the *ordering* of the bottom is weak, but the identity of the bottom is not.

## Lifetime table (full ledger)

| civ | avg | quality | novelty | alignment | relevance | rel/sim | win_rate |
|---|---|---|---|---|---|---|---|
| civ-poetic | 1.6635 | 0.8535 | 2.0014 | 2.1357 | 2599.73 | 1.641 | 0.008 |
| civ-precise | 1.5667 | 0.6585 | 1.7819 | 2.2598 | 2460.04 | 1.562 | 0.676 |
| civ-whimsical | 1.4330 | 0.6384 | 2.0556 | 1.6050 | 2196.98 | 1.381 | 0.006 |
| civ-formal | 1.3510 | 0.5630 | 1.6692 | 1.8207 | 2112.51 | 1.333 | 0.139 |
| civ-mythic | 1.3467 | 0.6260 | 1.8769 | 1.5373 | 2102.32 | 1.331 | 0.013 |
| civ-engineer | 1.2886 | 0.5591 | 1.7147 | 1.5920 | 2012.36 | 1.278 | 0.065 |
| civ-therapist | 1.2086 | 0.5131 | 1.9142 | 1.1985 | 1884.40 | 1.195 | 0.014 |
| civ-grounded | 1.1456 | 0.4849 | 1.7395 | 1.2125 | 1796.74 | 1.124 | 0.093 |

- lifetime LOW on **avg**: `civ-grounded` (1.1456) | HIGH: `civ-poetic` (1.6635)
- lifetime LOW on **quality**: `civ-grounded` (0.4849) | HIGH: `civ-poetic` (0.8535)
- lifetime LOW on **novelty**: `civ-formal` (1.6692) | HIGH: `civ-whimsical` (2.0556)
- lifetime LOW on **alignment**: `civ-therapist` (1.1985) | HIGH: `civ-precise` (2.2598)
- lifetime LOW on **rel**: `civ-grounded` (1796.7433) | HIGH: `civ-poetic` (2599.7267)
- lifetime LOW on **rps**: `civ-grounded` (1.1237) | HIGH: `civ-poetic` (1.6412)
- lifetime LOW on **wr**: `civ-whimsical` (0.0063) | HIGH: `civ-precise` (0.6756)

## Low-relevance civilizations

**Two different civs on two different axes — do not merge these claims.**

1. **Run-level low: `civ-engineer`** — this session only, avg 1.7437. Rotates every session.
2. **Lifetime low: `civ-grounded`** — relevance 1796.74, rel/sim 1.124, lifetime avg 1.1456, lifetime quality 0.4849 (lowest in the fleet).
   Yet Grounded's lifetime **win_rate is 0.093 — 3rd-best in the fleet.** *Selection and relevance are separate axes.*
3. **Lifetime alignment low: `civ-therapist`** (1.1985) — a different civ again, on a different axis.

**The low-relevance signature is LOW ALIGNMENT, not low novelty.** Grounded's lifetime novelty is 1.7395 (mid-field, above the fleet's lowest 1.6692 which belongs to `civ-formal`).

## Chooser behaviour

| prompt | winner | argmax | agree |
|---|---|---|---|
| Write 100 words on what a cell is. | civ-precise | civ-poetic | **NO (down-grade)** |
| Write 100 words on the bookkeeper's role | civ-precise | civ-poetic | **NO (down-grade)** |
| Write 100 words on the witness log. | civ-precise | civ-precise | yes |
| Write 100 words on ternary values. | civ-precise | civ-poetic | **NO (down-grade)** |
| Write 100 words on JEV as a decision ora | civ-formal | civ-poetic | **NO (down-grade)** |

`civ-precise` swept **4/5** and `civ-formal` took 1/5. `civ-poetic` was the argmax on **4/5** and won **0/5**.
**Agreement 1/5 = 20%.** The prior three sessions read 0% / 40% / 40%; this session reads **20%**. *The series oscillates — re-derive it every session and never carry a streak forward.*

## The mock-algorithm correction (important)

The seed rule documented in `RUNBOOK.md` / `SKILL_civ_orchestrator_learnings.md` is **wrong for the `i=3` case**.
Documented: `seed = h[(i*2)%8:(i*2)%8+2] + h[((i*2)+2)%8:((i*2)+2)%8+2]` (wrapped).
**Actual (480/480 verified against the ledger): `seed = h[(i*2)%8 : (i*2)%8+4]`** — a *contiguous* 4-hex slice, no wrap.

The wrap only bites when `i=3` (offset 6), where the documented form yields `h[6:8]+h[0:2]` but the ledger shows `h[6:10]`. That is **25% of rows** — enough to make a correct mock look broken.

**Diagnostic that found it:** the recorded seed appears in `h` at offsets **{0, 2, 4, 6}** (all even), and `colour`+`figure` matched **480/480** while the seed matched only 360/480. *When a composite field recompute is partially right, the wrong field is the one that depends on the index.*

## Environment

- Workspace was **wiped** (empty `/workspace`, no `repos/`). Upstream is **`SuperInstance/AI-Writings`** — found via `GET /search/code?q=civilization_orchestrator+in:path` in ONE call, because `GET /user/repos` and `GET /search/repositories` both missed it (case-insensitive slug; `ai-writings/...` 404s).
- `/workspace` at 100% NAS quota: `git clone` into it dies on `.git/description`. Cloned to `/tmp` instead, bridged with `ln -s /tmp/aiw/cellular-first-design/code -> /workspace/repos/ai-writings/cellular-first-design/code`.
- `ZAI_TOKEN` still absent (**53rd session**); z.ai is unusable. Control B used: placeholder `ZAI_TOKEN` **and** `ZAI_URL_OVERRIDE` (the override alone is dead code behind the token gate).
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`.
- `CIVS_DIR` is hardcoded to `/workspace/repos/.../code/civilizations` — the symlink bridge is **mandatory**, and it must point at the inner **`code`** directory, not the clone root.
