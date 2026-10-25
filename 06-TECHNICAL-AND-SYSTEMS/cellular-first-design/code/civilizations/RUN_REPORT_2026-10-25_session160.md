# Civ Orchestrator — Run Report, session 160 (2026-10-25)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (local mock provider bridge) + live JEV scorer.
**Result:** clean run — **60/60 verification checks passed**, 0 failures.

---

## 1. Environment

| Item | Value |
|---|---|
| Upstream | `SuperInstance/AI-Writings` (3.7 GB; `ai-writings/…` slug 404s) |
| Clone | `/tmp/aiw` — blobless + sparse checkout, civ subtree only |
| Bridge | `/workspace/repos/ai-writings/cellular-first-design` → `/tmp/aiw/cellular-first-design` |
| Bridge verify | inode `129:3669` both sides, `-ef` true, `-e` true, `ls` OK first try |
| NAS | **600 G/600 G, 0 bytes free** — EDQUOT total (12th session running) |
| `ZAI_TOKEN` | absent from env and all 8 secrets → **credential gap (46th session)** |
| `TYPESAFEAI_TOKEN` | present → exported as `TYPESAFEAI_KEY`; JEV live |
| `gh` | not installed (15th session) |
| HEAD at run | `dca9fa0` "civ-orchestrator skills: session 159 lessons" |

---

## 2. Verification — 60/60 PASS

| Check | Expected | Measured |
|---|---|---|
| per-civ `simulations.jsonl` delta | +10 × 8 = 80 | engineer 1036→1046, formal 1067→1077, grounded 1082→1092, mythic 1039→1049, poetic 1061→1071, precise 1031→1041, therapist 1034→1044, whimsical 1094→1104 |
| `meta_log.jsonl` delta | +5 | 533 → 538 |
| `Winner:` lines | 5 | 5 |
| total new rows | 80 | 80 |
| `provider` | `zai` | 80/80 |
| `[mock-zai seed=…]` prefix | 80/80 | 80/80 |
| JEV `error` key | 0 | 0 |
| 2.0/2.0/2.0 fallback triple | 0 | 0 |
| distinct seeds | 40 / 80 rows | 40 |
| `(civ,prompt)` combos with >1 seed | 0 | 0 |
| sim→competition ts gap at index 4 | >0 in 8/8 | 1.10–23.21 s |
| competition p0–p4 distinct seeds | 8/8 each | 8/8 × 5 |
| competition p0–p4 distinct previews | 8/8 each | 8/8 × 5 |
| `simulations_run` delta vs **git HEAD blob** | +10 × 8 | +10 × 8 |
| `wins+losses` total delta vs git blob | +5 × 8 | +5 × 8 |
| field total wins | +5 | 514 → 519 |
| `generation` | still 1 | 8/8 |

**Mock non-degeneracy: 8/8 distinct seeds AND 8/8 distinct previews on all 5 competition prompts — the 23rd consecutive clean measurement** (118, 120–128, 131–134, 136–138, 143, 145, 147–150, 157–159). The pre-flight probe (8 civs → 8/8 seeds + 8/8 previews, 40/40 distinct in-batch pairs, 0 tracebacks) passed before the batch — the **6th** time it has saved a run in the series.

**Note on `wins`/`losses`:** the runbook's "+5" applies to the **total** `wins+losses`; the split varies by who won. Engineer took 1 win (+1/+4), precise took 4 (+4/+1), the other six took 0 wins (+0/+5). Asserting `wins+5` per civ produces a false failure for a civ that lost all 5.

---

## 3. Run-level results

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-poetic | **1.6847** | **0.2620** | 2.2880 | **2.5040** |
| civ-precise | 1.4930 | 0.0900 | 2.3430 | 2.0460 |
| civ-mythic | 1.3013 | 0.0970 | 2.2870 | 1.5200 |
| civ-whimsical | 1.2383 | 0.0600 | **2.4630** | 1.1920 |
| civ-formal | 1.0203 | 0.0290 | 2.2590 | 0.7730 |
| civ-engineer | 0.8763 | 0.0200 | 2.2390 | 0.3700 |
| civ-grounded | 0.7577 | 0.0150 | 2.1490 | 0.1090 |
| civ-therapist | 0.7250 | 0.0160 | 2.1220 | 0.0370 |

**Cross-civ spreads (rank on spread, never on absolute level):** `alignment` **2.4670** › `avg_score` 0.9597 › `novelty` 0.3410 › `quality` 0.2470.
`alignment` again carried the widest spread and is again the axis the meta-GAN selects on.
`quality` collapsed again (field mean **0.0736**) — the 119/121/122/138 regime, and the **18th of the last 19** clean-mock sessions.

**Winners:** `civ-precise` 4, `civ-engineer` 1.

---

## 4. Chooser vs `avg_score` argmax — 1/5 (20 %)

| prompt | winner | winner avg | argmax | argmax avg | delta |
|---|---|---|---|---|---|
| p0 what a cell is | civ-precise | 1.6167 | civ-poetic | 1.7233 | −0.1067 |
| p1 the bookkeeper's role | civ-precise | 1.4000 | civ-poetic | 1.6367 | −0.2367 |
| p2 the witness log | civ-precise | 1.7567 | civ-precise | 1.7567 | +0.0000 |
| p3 ternary values | civ-engineer | 0.7967 | civ-poetic | 1.6867 | **−0.8900** |
| p4 JEV as a decision oracle | civ-precise | 1.4167 | civ-poetic | 1.7333 | −0.3167 |

`civ-poetic` was the argmax on **5/5** prompts and won **0/5**.

**All 4 disagreements took the LOWER-scoring candidate** — the fleet's stable direction, now reproduced in this session too. The p3 gap of **−0.8900** is the largest single disagreement in the clean-mock series, exceeding the session-137 record (−0.683) and the session-138 record (−0.6300).
Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125) → 1/5 (126) → 3/5 (127) → 2/5 (128) → 4/5 (130) → 1/5 (131) → 2/5 (132) → 2/5 (133) → 0/5 (134) → 4/5 (136) → 1/5 (137) → 1/5 (138) → … → **1/5 (160)**. Twenty-plus five-sample points cannot pin a rate — report it as a sample, and keep the **direction** as the finding.

**Never treat `win_rate` as a quality metric.** `civ-poetic` is 1st on lifetime avg_score and last on win_rate; `civ-precise` is the mirror inverse.

---

## 5. Low-relevance civilizations

### 5.1 `civ-grounded` (The Grounded) — the lifetime low, label did NOT rotate (50 sessions, 95–160)

Last of 8 on **every** lifetime axis:

| metric | value | rank |
|---|---|---|
| `relevance` | 1023.8200 | 8 of 8 |
| `relevance_per_sim` | 0.9760 | 8 of 8 |
| lifetime `avg_score` | 1.0148 | 8 of 8 |
| lifetime `alignment` | 1.1144 | 8 of 8 |
| lifetime `quality` | 0.4317 | 8 of 8 |

**Absolute gaps** (quote these, not a ratio — the ratio has swung 11× → 2.7× → 7.5× → 0.4× → 6.6× across sessions and is not a stable claim):
- alignment gap **0.2107** (grounded 1.1144 vs therapist 1.3251)
- quality gap **0.0325** (grounded 0.4317 vs formal 0.4642)

Alignment is the dimension the meta-GAN selects on ⇒ this is a **voice** failure, not a prose failure. Lifetime novelty 1.4983 remains **below** median (1.6410) — sessions 143–150 had Grounded above median, so it is now losing on **two** axes (alignment and novelty), not one. That two-axis condition persisted this session.

**Extinction risk: NONE.** Threshold −10; lowest relevance 1023.82 = **102× above the floor**. Registry 8, `max_civs` 12; all 8 still `generation=1`.

### 5.2 `civ-therapist` — run-level low on BOTH axes (6th session at the run bottom) → **watch axis, not a finding**

Run-level: `avg_score` **0.7250** (lowest of 8) and `alignment` **0.0370** (lowest of 8). This is the **6th consecutive session** at the run bottom on both axes, extending the session-150 watch axis.
But its **lifetime** standing is mid-field: `avg_score` 1.1804 (6th of 8), `alignment` 1.3251 (7th of 8 — second-lowest, now the civ that defines Grounded's alignment gap), `relevance_per_sim` 1.1589 (5th of 8).
⇒ **Watch axis.** The rule stands: a per-run low is a watch axis; only a lifetime gap is a finding.

### 5.3 `civ-grounded` was 7th of 8 on run `avg_score` (0.7577) — the run low and the lifetime low are different civs on different axes
The run-level low on both axes went to `civ-therapist`; Grounded was 7th of 8 on run `avg_score` but **2nd-lowest** on run `alignment` (0.1090). **This is the rule, not a contradiction** — report the lifetime table and the run ranking as two separate claims.

### 5.4 The two stable inverses
- **`civ-poetic`** — 1st on lifetime `avg_score` (1.5821), `quality` (0.7755), `relevance` (1597.64), `relevance_per_sim` (1.5451); **last** on `win_rate` (0.0117, 6/513). Argmax on 5/5 prompts, winner on 0/5. The selection-failure inverse.
- **`civ-precise`** — best `win_rate` (0.5787, 294/508), **highest lifetime `alignment` (2.1564)**, won 4/5 this run. The mirror inverse.

### 5.5 `civ-formal` — the low-novelty axis
Lifetime `novelty` **1.4088** (last of 8); lifetime `alignment` 1.6918 (4th, healthy). Distinct axis from Grounded, unchanged.

### 5.6 Watch axis `civ-engineer` — the session-121 low did NOT repeat
7th of 8 on lifetime `avg_score` (1.1581) and 7th of 8 on lifetime `relevance_per_sim` (1.1398), but on this run it was 6th on `avg_score` (0.8763) and 6th on `alignment` (0.3700) — no longer at the run bottom (therapist and grounded are below it). Still 7th of 8 on lifetime `avg_score`, so the axis stays open; **do not promote it to a finding** — it has not been at the bottom for many sessions.

---

## 6. Counter gap — byte-identical, a fixed per-civ offset

| civ | git-blob `relevance` | ledger `avg_score` sum | gap |
|---|---|---|---|
| civ-engineer | 1158.3933 | 1202.6367 | −44.2433 |
| civ-formal | 1184.0433 | 1269.5700 | −85.5267 |
| civ-grounded | 1016.2433 | 1100.5900 | −84.3467 |
| civ-mythic | 1285.2667 | 1336.3767 | −51.1100 |
| civ-poetic | 1580.7967 | 1677.6000 | −96.8033 |
| civ-precise | 1421.9133 | 1454.5467 | −32.6333 |
| civ-therapist | 1182.9700 | 1225.0833 | −42.1133 |
| civ-whimsical | 1398.3600 | 1571.5033 | −173.1433 |
| **total** | | | **−609.93** |

Identical to sessions 147/148/149/150/157 (whimsical −173.15, grounded −84.35, formal −85.53, poetic −96.81, engineer −44.25, mythic −51.11, therapist −42.11, precise −32.63; total −609.93). A **fixed per-civ offset, not an accumulating leak** — the gap did not move by one unit across this run. `save_state()` has no lock ⇒ `relevance_per_sim` is **not recomputable from the ledger** by an auditor.

---

## 7. Re-confirmations

- NAS EDQUOT total (12th session) — 1 MB `dd` → `Disk quota exceeded`; `touch` yields a 0-byte file that still appears in `ls`. Symlink bridge is the only way in.
- `gh` not installed (15th session) — locate upstream with `GET /search/repositories?q=…` + `GET /user/repos`; `git ls-remote` remains ground truth for existence.
- Tool timeout 30 s < orchestrator run ~30–35 s ⇒ launch detached with stdout redirected, then poll `ps` + the log.
- `ZAI_URL_OVERRIDE` alone is **dead code** — the `ZAI_TOKEN` gate returns `None` first. Control B needs **both**.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`.
- `civilizations.json` is **multi-line JSON**, not JSONL — use `json.loads(open(...).read())`.
- `meta_log.jsonl` `results` is a **list of `[civ_id, score]` pairs**, not a dict. Winner fields: `winner_civ` / `winner_name`.
- The `ls` race on the bridged deep path **did not reproduce** — `ls` succeeded on the first attempt, with the bridge pre-verified by inode identity.
- The z.ai credential gap: 46th session. `ZAI_TOKEN` absent from env and all 8 sandbox secrets. JEV live.

## 8. New this session

**NEW — the runbook's "+5 wins+losses" is a TOTAL, and the wins/losses SPLIT varies.**
`civ-precise` took 4 wins and 1 loss (+4/+1), `civ-engineer` 1 win and 4 losses (+1/+4), and the other six civs 0 wins and 5 losses (+0/+5). Every civ's `wins+losses` total is **+5** (8/8) and the field total wins is **+5** (514 → 519), but asserting `wins == blob_wins + 5` fails for any civ that did not win. **Assert the total, and cross-check the field win total.**

**NEW — the pre-flight's own scope assertion can be wrong while the mock is fine.**
The first pre-flight pass probed all 10 canon prompts (80 distinct seed/preview pairs) but asserted a 40-pair total, so it printed `PREFLIGHT: FAIL` with every per-prompt check at 8/8 PASS. The mock was healthy; the *expectation* was mis-scoped. **When a pre-flight fails, read the per-prompt lines before touching the mock** — a global-total mismatch with 8/8 on every row is a scope error in the probe, not a degenerate mock. Scoping the totals to the 5 prompts the batch will actually use gave 40/40 → `PREFLIGHT: PASS`.
