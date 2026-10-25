# Civ Orchestrator — Run Report, session 161 (2026-10-25)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (local mock provider bridge) + live JEV scorer.
**Result:** clean run — **48/48 verification checks passed**, 0 failures.

---

## 1. Environment

| Item | Value |
|---|---|
| Upstream | `SuperInstance/AI-Writings` (3.7 GB; `ai-writings/…` slug 404s) |
| Clone | `/tmp/aiw` — blobless + sparse checkout, civ subtree only |
| Bridge | `/workspace/repos/ai-writings/cellular-first-design` → `/tmp/aiw/cellular-first-design` |
| Bridge verify | inode `129:12601` both sides, `-ef` true, `-e` true, `ls` OK first try |
| NAS | **600 G/600 G, 0 bytes free** — EDQUOT total (14th session running) |
| `ZAI_TOKEN` | absent from env and all 8 secrets → **credential gap (47th session)** |
| z.ai probe | HTTP **401** `token expired or incorrect` — endpoint healthy, credential absent |
| `TYPESAFE_AI_TOKEN` | present → exported as `TYPESAFEAI_KEY`; JEV live |
| JEV probe | HTTP **422** on a malformed `questions` — payload-shape complaint ⇒ auth OK |
| `gh` | not installed (16th session) |
| HEAD at run | `d61ffbe4` "civ-orchestrator session 160: clean run, 60/60 checks, civ-grounded low on 50 sessions" |

---

## 2. Verification — 48/48 PASS

| Check | Expected | Measured |
|---|---|---|
| per-civ `simulations.jsonl` delta | +10 × 8 = 80 | grounded 1092→1102, whimsical 1104→1114, formal 1077→1087, poetic 1071→1081, precise 1041→1051, mythic 1049→1059, therapist 1044→1054, engineer 1046→1056 |
| `meta_log.jsonl` delta | +5 | 538 → 543 |
| `Winner:` lines | 5 | 5 |
| total new rows | 80 | 80 |
| `provider` | `zai` | 80/80 |
| `[mock-zai seed=…]` prefix | 80/80 | 80/80 |
| JEV `error` key | 0 | 0 |
| 2.0/2.0/2.0 fallback triple | 0 | 0 |
| distinct `(quality,novelty,alignment)` triples | ≫ 1 | **80** (a silent default would give 1) |
| confidence | not constant 0.5 | 4 distinct, range 0.93–1.00 |
| distinct seeds | 40 / 80 rows | 40 |
| `(civ,prompt)` combos with >1 seed | 0 | 0 of 40 |
| sim→competition ts gap at index 4 | >0 in 8/8 | 0.61–0.70 s |
| competition p0–p4 distinct seeds | 8/8 each | 8/8 × 5 |
| competition p0–p4 distinct previews | 8/8 each | 8/8 × 5 |
| `simulations_run` delta | +10 × 8 | +10 × 8 |
| `wins+losses` total delta | +5 × 8 | +5 × 8 |
| field total wins | +5 | 5 |
| `generation` | still 1 | 8/8 |
| `git status --porcelain` | 18 modified | 18 |

**Mock non-degeneracy: 8/8 distinct seeds AND 8/8 distinct previews on all 5 competition prompts — the 24th consecutive clean measurement** (118, 120–128, 131–134, 136–138, 143, 145, 147–150, 157–160). The pre-flight probe (8 civs → 8/8 seeds + 8/8 previews, cultural-prompt lengths 167–199, stable across two rounds, 0 tracebacks) passed before the batch — the **7th** time it has saved a run in the series.

**Note on `wins`/`losses`:** the "+5" applies to the **total** `wins+losses`; the split varies by who won. Precise took 3 wins (+3/+2), formal and mythic 1 each (+1/+4), the other five took 0 (+0/+5). Asserting `wins == blob_wins + 5` per civ produces a false failure for any civ that lost all 5.

---

## 3. Run-level results

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| civ-precise | **0.3923** | **0.0180** | 0.2630 | **0.8960** |
| civ-poetic | 0.3183 | 0.0160 | **0.5720** | 0.3670 |
| civ-whimsical | 0.2347 | 0.0180 | 0.3880 | 0.2980 |
| civ-engineer | 0.2240 | 0.0130 | 0.1790 | 0.4800 |
| civ-formal | 0.2153 | 0.0110 | 0.3110 | 0.3240 |
| civ-grounded | 0.1890 | 0.0100 | 0.5000 | 0.0570 |
| civ-mythic | 0.1407 | 0.0080 | 0.1550 | 0.2590 |
| civ-therapist | **0.1103** | 0.0080 | 0.2980 | **0.0250** |

**Cross-civ spreads (rank on spread, never on absolute level):** `alignment` **0.8710** › `novelty` 0.4170 › `avg_score` 0.2820 › `quality` **0.0100**.
`alignment` carried the widest spread again and is again the axis the meta-GAN selects on. `quality` collapsed again (field mean **0.0128**, spread 0.0100) — the 119/121/122/138 regime, and the **19th of the last 20** clean-mock sessions.

**Winners:** `civ-precise` 3, `civ-formal` 1, `civ-mythic` 1.

---

## 4. Chooser vs `avg_score` argmax — 0/5 (0 %)

| prompt | winner | winner avg | argmax | argmax avg | delta |
|---|---|---|---|---|---|
| p0 what a cell is | civ-formal | 0.2033 | civ-precise | 0.6133 | **−0.4100** |
| p1 the bookkeeper's role | civ-precise | 0.1667 | civ-poetic | 0.3567 | −0.1900 |
| p2 the witness log | civ-precise | 0.3933 | civ-engineer | 0.4000 | −0.0067 |
| p3 ternary values | civ-precise | 0.2967 | civ-whimsical | 0.7600 | **−0.4633** |
| p4 JEV as a decision oracle | civ-mythic | 0.1700 | civ-precise | 0.6267 | **−0.4567** |

**All 5 disagreements took the LOWER-scoring candidate** — the fleet's stable direction, reproduced again. The p3 gap of **−0.4633** is the second-largest single disagreement in the clean-mock series (session 160's p3 was −0.8900, still the record).
Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125) → 1/5 (126) → 3/5 (127) → 2/5 (128) → 4/5 (130) → 1/5 (131) → 2/5 (132) → 2/5 (133) → 0/5 (134) → 4/5 (136) → 1/5 (137) → 1/5 (138) → … → 1/5 (160) → **0/5 (161)**. Twenty-five five-sample points cannot pin a rate — report it as a sample, and keep the **direction** as the finding.

**Never treat `win_rate` as a quality metric.** `civ-poetic` is 1st on lifetime avg_score and last on win_rate; `civ-precise` is the mirror inverse.

---

## 5. Low-relevance civilizations

### 5.1 `civ-grounded` (The Grounded) — the lifetime low, label did NOT rotate (51 sessions, 95–161)

Last of 8 on **every** lifetime axis:

| metric | value | rank |
|---|---|---|
| `relevance` | 1025.7100 | 8 of 8 |
| `relevance_per_sim` | 0.9690 | 8 of 8 |
| lifetime `avg_score` | 1.0073 | 8 of 8 |
| lifetime `alignment` | 1.1048 | 8 of 8 |
| lifetime `quality` | 0.4279 | 8 of 8 |

**Absolute gaps** (quote these, not a ratio — the ratio has swung 11× → 2.7× → 7.5× → 0.4× → 6.6× across sessions and is not a stable claim):
- alignment gap **0.2080** (grounded 1.1048 vs therapist 1.3128)
- quality gap **0.0321** (grounded 0.4279 vs formal 0.4600)

Alignment is the dimension the meta-GAN selects on ⇒ this is a **voice** failure, not a prose failure. Lifetime novelty 1.4892 sits **below** median (1.6160) — it is now losing on **two** axes (alignment and novelty), not one. That two-axis condition persisted this session.

**Extinction risk: NONE.** Threshold −10; lowest relevance 1025.71 = **102× above the floor**. Registry 8, `max_civs` 12; all 8 still `generation=1`.

### 5.2 `civ-therapist` — run-level low on BOTH axes (7th session at the run bottom) → **watch axis, not a finding**

Run-level: `avg_score` **0.1103** (lowest of 8) and `alignment` **0.0250** (lowest of 8). This is the **7th consecutive session** at the run bottom on both axes, extending the session-150 watch axis.
But its **lifetime** standing is mid-field: `avg_score` 1.1702 (6th of 8), `alignment` 1.3128 (7th of 8 — second-lowest, now the civ that defines Grounded's alignment gap), `relevance_per_sim` 1.1490 (5th of 8).
⇒ **Watch axis.** The rule stands: a per-run low is a watch axis; only a lifetime gap is a finding.

### 5.3 The run low and the lifetime low are different civs on different axes
The run-level low on both axes went to `civ-therapist`; Grounded was 7th of 8 on run `avg_score` (0.1890) but **2nd-lowest** on run `alignment` (0.0570). **This is the rule, not a contradiction** (session-132 rule) — report the lifetime table and the run ranking as two separate claims.

### 5.4 The two stable inverses
- **`civ-poetic`** — 1st on lifetime `avg_score` (1.5704), `quality` (0.7684), `relevance` (1600.83), `relevance_per_sim` (1.481); **last** on `win_rate` (0.012, 6/518). Argmax on 0/5 prompts, winner on 0/5. The selection-failure inverse.
- **`civ-precise`** — best `win_rate` (0.579, 297/513), **highest lifetime `alignment` (2.1444)**, 1st on run `avg_score` (0.3923) at `preferred_temp` **0.2**. The mirror inverse.

### 5.5 `civ-formal` — the low-novelty axis
Lifetime `novelty` **1.3987** (last of 8); lifetime `alignment` 1.6793 (4th, healthy). Distinct axis from Grounded, unchanged.

### 5.6 Watch axis `civ-engineer` — the session-121 low did NOT repeat
7th of 8 on lifetime `avg_score` (1.1493) and 7th of 8 on lifetime `relevance_per_sim` (1.1310), but on this run it was 4th on `avg_score` (0.2240) and **2nd on `alignment` (0.4800)** — not at the run bottom (therapist and grounded are below it). The axis stays open; **do not promote it to a finding**.

---

## 6. Counter gap — a fixed per-civ offset, unchanged

| civ | HEAD-blob `relevance` | blob ledger sum | gap | post-run `relevance` | post-run ledger sum | gap | Δ |
|---|---|---|---|---|---|---|---|
| civ-grounded | 1023.8200 | 1108.1667 | −84.3467 | 1025.7100 | 1110.0567 | −84.3467 | 0.0000 |
| civ-whimsical | 1410.7433 | 1583.8867 | −173.1433 | 1413.0900 | 1586.2333 | −173.1433 | 0.0000 |
| civ-formal | 1194.2467 | 1279.7733 | −85.5267 | 1196.4000 | 1281.9267 | −85.5267 | 0.0000 |
| civ-poetic | 1597.6433 | 1694.4467 | −96.8033 | 1600.8267 | 1697.6300 | −96.8033 | 0.0000 |
| civ-precise | 1436.8433 | 1469.4767 | −32.6333 | 1440.7667 | 1473.4000 | −32.6333 | 0.0000 |
| civ-mythic | 1298.2800 | 1349.3900 | −51.1100 | 1299.6867 | 1350.7967 | −51.1100 | 0.0000 |
| civ-therapist | 1190.2200 | 1232.3333 | −42.1133 | 1191.3233 | 1233.4367 | −42.1133 | 0.0000 |
| civ-engineer | 1167.1567 | 1211.4000 | −44.2433 | 1169.3967 | 1213.6400 | −44.2433 | 0.0000 |
| **total** | | | **−609.92** | | | **−609.92** | **0.0000** |

Identical to sessions 147/148/149/150/157/160 (whimsical −173.14, grounded −84.35, formal −85.53, poetic −96.80, engineer −44.24, mythic −51.11, therapist −42.11, precise −32.63; total **−609.92**). A **fixed per-civ offset, not an accumulating leak** — the gap did not move by one unit across this run. `save_state()` has no lock ⇒ `relevance_per_sim` is **not recomputable from the ledger** by an auditor.

---

## 7. Re-confirmations

- NAS EDQUOT total (14th session) — clone to `/tmp` (overlay, 28 G free; the 3.7 GB repo's *working tree* is only ~6 MB after sparse checkout), then bridge the **nested** `cellular-first-design` dir and verify with `stat -L -c '%d:%i'` on both sides + `-ef`; never flatten.
- `gh` not installed (16th session) — locate upstream with `GET /search/repositories?q=…` + `GET /user/repos`; `git ls-remote` remains ground truth for existence. The API is case-insensitive: `SuperInstance/ai-writings` == `SuperInstance/AI-Writings`.
- Tool timeout 30 s < orchestrator run ~20 s ⇒ detached launch with stdout redirected, then poll `ps` + the log. The run happened to finish inside the window this session, but the detached pattern is retained.
- `ZAI_URL_OVERRIDE` alone is **dead code** — the `ZAI_TOKEN` gate returns `None` first. Control B needs **both**.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`.
- JEV liveness = **422** on a malformed `questions` (payload-shape complaint ⇒ auth OK). z.ai = **401** `token expired or incorrect` (credential gap, endpoint healthy) — **47th session**.
- `civilizations.json` is **multi-line JSON**, not JSONL — use `json.loads(open(...).read())`.
- `meta_log.jsonl` `results` is a **list of `[civ_id, score]` pairs**, not a dict. A dict-shaped reader silently yields 0 % agreement and empty pick tallies. Winner fields are `winner_civ` / `winner_name`.
- The `ls` race on the bridged deep path **did not reproduce** — `ls` succeeded on the first attempt, with the bridge pre-verified by inode identity.
- Run isolation used the documented method: **last 10 rows of each civ file**, then an explicit `ts` sort — never `rows[-80:]` over a concatenation (glob order is filesystem order, not chronological).

---

## 8. New this session

**NEW — the counter-gap method has an epoch-mixing trap that fakes an accumulating leak.**
This session the gap was first computed as *pre-run blob `relevance`* vs *post-run ledger sum*, which gave **−628.17** — a value that had drifted from session 160's −609.93 and looked like the fixed offset was finally accumulating. It is not. The comparison **mixes epochs**: the blob's `relevance` predates this run while the ledger includes it, so the run's own scores are subtracted twice.

The correct method computes **both sides in the same epoch** — either both at HEAD (blob `relevance` vs blob ledger sum) or both post-run (`culture.json` `relevance` vs working-tree ledger sum). Both give **−609.92**, byte-identical to session 160, and the per-civ deltas are **0.0000** across the run.

⇒ **The gap table must show both epochs side by side.** If the gap moves, first check that the two columns come from the same snapshot; a per-civ Δ of 0.0000 is the proof that the offset is fixed. A "gap that grows every session" is the classic symptom of this mistake, not of a leak in `save_state()`.

**NEW — a mock rebuilt from the RUNBOOK must re-apply three independent fixes, not two.**
The session-160 report names the session-112 index wrap and the session-118 md5-of-whole-message seeding as the two load-bearing fixes. A third is equally required: the **session-144 `Connection: close` + `Content-Length`** pair, without which `curl -X POST` hangs to the tool timeout even though the server logged `200`. A rebuild that applies only the two named fixes produces a mock that *looks* healthy to `urllib` (the orchestrator's client) but hangs any `curl`-based probe — and a hung probe is easy to misread as "the mock is down" and to re-debug a healthy server.

⇒ Treat all three as one checklist on every rebuild: (a) `seed[(i*2)%8:((i*2)%8)+2]`, (b) `md5(whole_message)[:8]`, (c) `Connection: close`. All three were applied and verified this session: HTTP 200 in 1 ms, `[mock-zai seed=…]` present, 8/8 distinct seeds and previews on the long cultural prompt, stable across two rounds, 0 tracebacks.
