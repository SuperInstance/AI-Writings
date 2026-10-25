# Civ Orchestrator — Run Report, session 214 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **86th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `582e680` (session 213 tree). **All 17 verification assertions PASS.** Pre-flight **13/13 PASS**.

**Session 214 in one line:** `civ-precise` swept **5/5 competitions** with **5/5 (100 %)**
chooser/argmax agreement — the first **perfect-agreement** session in the clean-mock series
after three consecutive sub-50 % sessions (212: 2/5, 213: 2/5, 211: 0/5); the run-level low
rotated to **`civ-whimsical`** while `civ-grounded` held the lifetime low for the **83rd**
consecutive session.

**Three durable lessons from this session:**

1. **A 5/5 SWEEP AND 5/5 CHOOSER AGREEMENT ARE INDEPENDENT, AND BOTH CAN HOLD.**
   Previous sessions recorded a sweep coexisting with 0/5 agreement (211) and with 2/5
   (212, 213). This session both measures were perfect simultaneously. *Neither the win
   count nor the agreement rate may be inferred from the other* — and a perfect-agreement
   session must not be read as "the chooser is now calibrated": the honest reading is a
   **5-sample point at 100 %**, sitting on a series whose last three points were 0 %, 40 %,
   40 %.

2. **THE RUN LOW'S SIGNATURE IS "LOW ALIGNMENT", AND THE FLEET GAP IS DOMINATED BY
   ALIGNMENT, NOT NOVELTY.** `civ-whimsical` (run `avg_score` **1.2807**, alignment
   **0.6850** = fleet-low) and `civ-therapist` (**1.5050**, alignment **1.1720**) are
   separated by **0.2243** on `avg_score` against a run spread of **1.1607** — a gap of
   **19 %** of the run's own spread, so the *ordering* of the bottom two is weak but the
   *identity* of the bottom is not. The run's alignment spread is **2.5690** against a
   novelty spread of **0.1250** — a factor of **20.6**. The ranking is produced by
   alignment and quality, not novelty. *Report the axis, not the holder.*

3. **THE COUNTER-GAP CHECK MUST BE TOLERANCED AT 1e-6, NOT 1e-9.** A first pass reported
   `[FAIL] counter_gap_stable_8of8` while the underlying gaps were **exactly** the
   documented stable values (grounded −84.35, whimsical −173.14, formal −85.53, poetic
   −96.80, precise −32.63, mythic −51.11, therapist −42.11, engineer −44.24) and the
   per-civ gap **deltas were +0.0000000000 for all 8**. The bug was the check: it
   recomputed the *current* gap through a different expression (`base + (csum-bsum) - bsum`)
   than the one it compared against, so it differed in the last float bits. *A
   pre-flight FAIL on a component already independently verified is a CHECK bug until
   proven otherwise* — re-derive the fact directly (here: subtract the ledger sums from
   the `culture.json` blobs on both sides) before touching the artifact.

**Also durable:** the repo is **`SuperInstance/AI-Writings`** (a *user* account); the NAS
under `/workspace` is at 100 % quota (`df`: 600 G of 600 G), so the clone goes to
`/tmp/clone/ai-writings` and the **inner** `cellular-first-design` directory is bridged
by symlink — verified by inode identity `stat -L -c '%d:%i'` → `129:12604` on both sides
plus `os.path.samefile()` → `True`. The mock body was rebuilt to land in the documented
**332–369** band at **337** chars, with the recorded ledger's 162-char tail prefix
preserved verbatim so the existing ledger rows still reconcile. `civ-grounded` remains the
lifetime low (`relevance` **1777.39**, `relevance_per_sim` **1.119**) for the **83rd**
consecutive session while its lifetime `win_rate` **0.093** is 3rd-best in the fleet.

## Run-level table (this session's 10 rows per civ)

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-precise | **2.4413** | 1.7040 | 2.3660 | **3.2540** |
| civ-poetic | 2.2047 | 1.6530 | **2.4060** | 2.5550 |
| civ-formal | 2.1653 | 1.2830 | 2.3700 | 2.8430 |
| civ-engineer | 2.0903 | 1.3050 | 2.3210 | 2.6450 |
| civ-mythic | 1.9207 | 1.3730 | 2.3520 | 2.0370 |
| civ-grounded | 1.9113 | 1.1220 | 2.3990 | 2.2130 |
| civ-therapist | 1.5050 | 0.8970 | 2.4460 | 1.1720 |
| **civ-whimsical** | **1.2807** | **0.7180** | 2.4390 | **0.6850** |

## Low-relevance civilizations

**`civ-whimsical` — run low (rotating, 20th distinct run low in 20 sessions).**
Run `avg_score` **1.2807** (fleet-low), quality **0.7180** (fleet-low), alignment
**0.6850** (fleet-low), novelty **2.4390** (mid-field, spread only 0.1250). Lifetime
standing is **3rd of 8** on `relevance_per_sim` (**1.378**) — *the run low is not the
lifetime low*. The deficit is a **voice** failure (alignment), not a prose failure.

**`civ-therapist` — 2nd-lowest on the run, and the lifetime alignment low.**
Run `avg_score` **1.5050**, alignment **1.1720** (2nd-lowest in the fleet). Lifetime
`relevance_per_sim` **1.190** (7th of 8) and lifetime alignment **1.1929** — the
**lowest lifetime alignment in the fleet**, a different civ from the lifetime `avg_score`
low. Lifetime `win_rate` **0.014**.

**`civ-grounded` — lifetime low (83rd consecutive session), and 6th on the run.**
Lifetime `relevance` **1777.39**, `relevance_per_sim` **1.119** (8th of 8), lifetime
`avg_score` **1.1408** and lifetime quality **0.4810** (both fleet-low). Its deficit is
**quality**, not alignment (lifetime alignment **1.2062**, 2nd-lowest). It placed **6th of
8** on this run's `avg_score` (**1.9113**) — *the lifetime table and the run table are two
separate claims*. Lifetime `win_rate` **0.093** is 3rd-best in the fleet, which is the
standing reminder that `win_rate` is not a quality metric.

No extinction risk: the threshold is −10 and the lowest lifetime relevance is
**1777.39**, roughly 178× above it. No births (the 8-civ registry is unchanged).

## Verification (17/17 PASS)

- per-civ ledger Δ **+10 × 8** = 80 new rows
- `meta_log.jsonl` Δ **+5**; stdout `Winner:` lines = **5**
- `wins` **8/8 exact**, `losses` **8/8 exact** (from `meta_log.winner_civ`)
- `relevance` Δ = Σ this run's `avg_score` — **8/8 exact** to 1e-6
- per-civ counter gap Δ = **0.0000000000 × 8** (gaps stable at the documented values)
- distinct seeds **40 / 80 rows**; **0** `(civ,prompt)` pairs carrying >1 seed
- **80/80** new rows match an independently recomputed message md5 (raw-byte `d[0] % 4`
  index, slice `h[(i*2)%8:(i*2)%8+4]`, colour `h[8:12]`, figure as a string triple)
- header parses **80/80**; body length band **332–369** (all 337)
- meta-vs-ledger `avg_score` mismatches **0/40**
- 0 JEV errors, 0 `2.0/2.0/2.0` fallback triples
- extinction risk NONE

Pre-flight **13/13 PASS**: 40/40 distinct seeds, 40/40 distinct previews, 40/40
recomputed md5, 8/8 distinct seeds AND previews on all 5 prompts, 0 literal `seed={}`,
`[mock-zai` prefix 40/40, 0 `EXC:`/tracebacks, repeat-same-message ⇒ same seed (40×2),
0 pairs carrying >1 seed, body band 332–369, cultural-prompt band 167–209.
