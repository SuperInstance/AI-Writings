# Civ Orchestrator — Run Report, session 243 (2026-10-25)

## Session 243 (2026-10-25)

- Command: `civilization_orchestrator.py --sims 5 --prompts 5 --providers zai` -> **exit 0**, 8 civs x 5 sims + 5 competitions.
- Provider path: **Control B mock** (z.ai credential gap, **102nd session**) + **live JEV** (`jev-1.14.0`).
- Baseline: `4182f8a` (session 242 tree); `refs/heads/main` == clone HEAD.
- **Pre-flight gate: 14/14 PASS** (one checker bug found and fixed before the run). **Run verification: 62/62 PASS.**
- Ledger delta: **+10 rows per civ, +80 total**; **18 files changed** (16 civ files + `leaderboard.json` + `meta_log.jsonl`).
- Seed algorithm re-verified over the full current-format ledger: **2480/2480 exact, 0 mismatches**; new rows **80/80**.
- Counter gap drift **0.000000000** for all 8 civs (full-ledger sum, not new-rows-only).
- Mock body **344** chars (38 header + 162 tail + 144 continuation), inside the 332-369 band, **first build**.
- Mock served **202** requests total (121 pre-flight probes incl. the GET + 80 run sims + 1 later probe); **0 exceptions**.
- Agreement **1/5 (20 %)**, **4 down-grades, 0 up-grades** (the structural ceiling).
- Run low **`civ-therapist`** (avg **1.1327**) — quality **0.2770** and alignment **0.6630** both at the fleet low: a **two-axis** collapse.
- Lifetime low **`civ-grounded`** (**2266.60**) — **civ-grounded** also lowest rel/sim (**1.206**), lifetime-low quality (**0.5441**).
- No civ near extinction (threshold `relevance < -10`); all 8 remain generation 1.

## Run-level result (this session's 80 sim rows)

| rank | civilization | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| 1 | `civ-precise` | 1.8703 | 0.7650 | 2.3260 | 2.5200 |
| 2 | `civ-poetic` | 1.8443 | 0.9220 | 2.3930 | 2.2180 |
| 3 | `civ-formal` | 1.4890 | 0.4150 | 2.3530 | 1.6990 |
| 4 | `civ-engineer` | 1.4790 | 0.4120 | 2.3120 | 1.7130 |
| 5 | `civ-whimsical` | 1.4240 | 0.4490 | 2.4680 | 1.3550 |
| 6 | `civ-mythic` | 1.2717 | 0.4480 | 2.3710 | 0.9960 |
| 7 | `civ-grounded` | 1.2660 | 0.3670 | 2.3330 | 1.0980 |
| 8 | `civ-therapist` | 1.1327 | 0.2770 | 2.4580 | 0.6630 |

**Run low: `civ-therapist`** (avg **1.1327**), gap to next **0.1333** = **18.1 %** of the run spread **0.7377**.

### Axis signature

- **Alignment** spread **1.8570** = **2.52x** the `avg_score` spread — alignment dominated again.
- **Quality** spread **0.6450** = **0.87x**.
- **Novelty** spread **0.1560** = **0.21x** — novelty is near-constant across the fleet.
- Run low `civ-therapist` holds the fleet-low **quality** (0.2770) **and** the fleet-low **alignment** (0.6630); its novelty (2.4580) is mid-field.

## Lifetime board

| civ | relevance | rel/sim | life quality | life novelty | life alignment | wins | win_rate |
|---|---|---|---|---|---|---|---|
| `civ-poetic` | 3194.80 | 1.714 | 0.934 | 2.062 | 2.197 | 6 | 0.006 |
| `civ-precise` | 3069.02 | 1.654 | 0.757 | 1.864 | 2.349 | 650 | 0.704 |
| `civ-formal` | 2652.34 | 1.422 | 0.634 | 1.765 | 1.907 | 120 | 0.130 |
| `civ-whimsical` | 2640.52 | 1.411 | 0.680 | 2.108 | 1.577 | 5 | 0.005 |
| `civ-mythic` | 2595.45 | 1.396 | 0.700 | 1.945 | 1.583 | 10 | 0.011 |
| `civ-engineer` | 2535.35 | 1.368 | 0.633 | 1.799 | 1.691 | 57 | 0.062 |
| `civ-therapist` | 2276.93 | 1.226 | 0.550 | 1.986 | 1.177 | 11 | 0.012 |
| `civ-grounded` | 2266.60 | 1.206 | 0.544 | 1.824 | 1.300 | 75 | 0.081 |

**Lifetime low: `civ-grounded`** at **2266.60** (rel/sim **1.206**) — **227x** above the extinction floor.

- Lifetime **quality** low: `civ-grounded` (0.544)
- Lifetime **novelty** low: `civ-formal` (1.765)
- Lifetime **alignment** low: `civ-therapist` (1.177)

### Low-relevance civilizations (the task's explicit ask)

| civ | relevance | rel/sim | run avg | run rank | lifetime rank | reading |
|---|---|---|---|---|---|---|
| `civ-grounded` | 2266.60 | 1.206 | 1.2660 | 7/8 | 8/8 | **LIFETIME LOW** — lowest relevance *and* lowest rel/sim *and* lowest lifetime quality |
| `civ-therapist` | 2276.93 | 1.226 | 1.1327 | 8/8 | 7/8 | **RUN LOW** — two-axis collapse (quality+alignment at fleet low) |
| `civ-engineer` | 2535.35 | 1.368 | 1.4790 | 4/8 | 6/8 | mid-field |
| `civ-mythic` | 2595.45 | 1.396 | 1.2717 | 6/8 | 5/8 | mid-field |
| `civ-whimsical` | 2640.52 | 1.411 | 1.4240 | 5/8 | 4/8 | mid-field |
| `civ-formal` | 2652.34 | 1.422 | 1.4890 | 3/8 | 3/8 | mid-field |
| `civ-precise` | 3069.02 | 1.654 | 1.8703 | 1/8 | 2/8 | mid-field |
| `civ-poetic` | 3194.80 | 1.714 | 1.8443 | 2/8 | 1/8 | mid-field |

**`civ-therapist` (The Therapist)** — run low. Lifetime relevance **2276.93** (rel/sim **1.226**, 7th of 8) and lifetime alignment low (**1.177**). The weakness is **voice**, not prose: alignment (0.6630) sits at the fleet low while novelty (2.4580) is 3rd-highest of 8. Quality (0.2770) is also the fleet low, so this is a **two-axis** collapse, not a single-axis dip.

**`civ-grounded` (The Grounded)** — lifetime low for the **104th consecutive session**, now at **2266.60** (rel/sim **1.206**, lifetime quality low **0.544**). Structurally last on relevance, yet its lifetime **win_rate** is **0.081** — 3rd-best in the fleet. Selection and relevance are separate axes.

**The run low and the lifetime low are different civs on different axes** (run low `civ-therapist`, lifetime low `civ-grounded`). Do not promote a run low to the lifetime finding.

## Competitions

| prompt | winner | avg_score argmax | agree? |
|---|---|---|---|
| Write 100 words on what a cell is. | `civ-precise` | `civ-precise` | yes |
| Write 100 words on the bookkeeper's role. | `civ-precise` | `civ-poetic` | **no** |
| Write 100 words on the witness log. | `civ-formal` | `civ-precise` | **no** |
| Write 100 words on ternary values. | `civ-precise` | `civ-poetic` | **no** |
| Write 100 words on JEV as a decision oracle. | `civ-precise` | `civ-poetic` | **no** |

- Winners: **civ-precise 4, civ-formal 1** — a **4-1 split**, not a sweep.
- Chooser/argmax agreement **1/5 (20 %)**; **4 down-grades, 0 up-grades**.
- The chooser reads only `content_preview[:150]` and never sees `avg_score`, so **every disagreement is a down-grade by construction** — the up-grade count is pinned at 0 structurally, not empirically.

## Verification battery (62/62 PASS)

| check | result |
|---|---|
| per-civ ledger delta | **+10 each, 80 total** |
| `meta_log.jsonl` delta | **+5** |
| seed/colour/figure recompute on new rows | **80/80 exact** |
| `content_preview` length | **200** on all 80 |
| distinct bodies / tails | **40** bodies (40 seeds x 1 tail) / **1** tail |
| distinct seeds | **40/80** rows, **0** `(civ,prompt)` with >1 seed |
| provider mix | `zai` **80/80** |
| JEV errors / fallback `2.0/2.0/2.0` triples | **0 / 0** |
| counter gap (relevance - full-ledger sum) | drift **0.000000000** on all 8 |
| wins/losses deltas vs meta-log winners | **8/8 exact** |
| `simulations_run` delta | **+10** on all 8 |
| meta-vs-ledger `avg_score` (later-`ts` row) | **0/40** mismatches |
| generation | all 8 remain **1** |
| extinction risk | **NONE** — lowest civ **227x** above the -10 floor |

## Method notes for this session

1. **The workspace was wiped** — `/workspace/repos/ai-writings/...` did not exist. Restored by sparse clone of `SuperInstance/AI-Writings` (`--filter=blob:none --no-checkout --depth 1`) into `/tmp`, then `sparse-checkout set cellular-first-design`, then symlink-bridged the **clone root** to the script's hard-coded `CIVS_DIR`; verified with `os.path.samefile()` -> `True`.
2. **`sparse-checkout set cellular-first-design` leaves the `prose/` tree staged as deleted.** `git checkout -- prose/` fails with *pathspec did not match* (the paths are not in the sparse index). The fix is `git sparse-checkout disable` — the working tree then matches `HEAD` and `git status --porcelain` is empty. A dirty tree at baseline invalidates the `git status` count used as a change detector.
3. **The mock's `d[0]` is the RAW MD5 BYTE**, not `int(h[0], 16)`. Re-derived from the ledger and confirmed **2480/2480 exact** over the full current-format ledger before the run.
4. **The pre-flight's own `by_prompt` accumulator was buggy** (it appended a `None` before the real seeds), producing `9` distinct seeds per prompt where the mock produced exactly `8`. *A 0/40 or 9/8 recompute means "the checker is wrong" before it means "the mock is wrong"* — dump one real body and parse it by hand. The same rule that produced the two historical false-alarm series.
5. **`culture.json` has no `sims_run` key** — the field is `simulations_run`. A checker that reads `sims_run` raises `KeyError` mid-battery, and a battery that dies partway leaves a *partial* verdict that reads like a pass. Print an explicit final verdict line and exit non-zero on any failure.
6. **Mock teardown by PID captured from `ps`**, never `pkill -f mock_zai` (self-match). Port then proven closed: `curl` exit **7**, `HTTP=000**. Mock log held **202** request lines and **0** `EXC:` entries.

---

*Generated 2026-10-25T17:37:56Z — session 243, baseline `4182f8a`.*
