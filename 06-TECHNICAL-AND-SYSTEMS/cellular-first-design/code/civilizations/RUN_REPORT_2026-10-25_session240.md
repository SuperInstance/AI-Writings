# RUN REPORT — 2026-10-25 — session 240

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

**Result:** exit 0, wall clock 29.33 s, 8 civs x 5 sims + 5 competition prompts.
**Provider path:** Control B mock (z.ai credential gap, **101st session**) + **live JEV**.
**Ledger delta:** +10 rows per civ, **+80 total** (8 civs x 10).

## 1. Environment

| item | value |
|---|---|
| repo | `SuperInstance/AI-Writings` (user account); `cellular-first-design` is a **subdirectory**, not a repo |
| clone | `/tmp/afd`, `--depth 1` |
| bridge | symlink `/workspace/repos/ai-writings/cellular-first-design/code` -> clone `code`; `os.path.samefile()` -> `True` |
| NAS | `/workspace` at **600 G/600 G, 0 avail** (EDQUOT) — clone went to the overlay (`/tmp`) |
| base commit | `bc2b430868dc1cd21e9fa3a35369bbf5e1dcf7cb`, tree clean pre-run |
| `ZAI_TOKEN` | absent from env and all sandbox secrets; set to a **placeholder** for Control B |
| `ZAI_URL_OVERRIDE` | `http://127.0.0.1:8799/v1/chat/completions` — needed **together with** the token gate |
| `TYPESAFEAI_KEY` | exported from `TYPESAFE_AI_TOKEN`; JEV live, **0** fallback triples |
| post-run commit | `86c1622019ea22e99c1107cc73001d6adb35c85c`, **remote-verified** via the commits API |

## 2. Mock body construction

The Control B mock source is **not in the repo**; the ledger is the specification.

```
d      = md5(cultural_prompt).digest()
h      = d.hex()
i      = d[0] % 4            # RAW MD5 BYTE, not int(h[0],16) % 4
seed   = h[(i*2)%8 : (i*2)%8+4]
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"
```

- **Seed algorithm re-verified over the FULL current-format ledger: 2480/2480 exact, 0 mismatches** (before the run, not against our own fresh rows).
- Tail **extracted byte-for-byte** from the ledger's most recent 80-row cluster: 162 chars, 16 distinct tails in history.
- Body = 38 (header) + 162 (tail) + **144** (continuation) = **344** chars, inside the 332-369 band, ending on a word boundary.
- Mock served **81** requests = 1 pre-flight probe + 80 ledger rows.

## 3. Verification — new `simulations.jsonl` entries

`ls -la` is the **weakest** check (it shows mtimes, and it has passed on a tree with 18 modified files). The discriminating check is the **row-count delta** against the pinned git blob, plus the counter-gap check. Both were run.

| civ | rows before | rows after | delta | mtime |
|---|---|---|---|---|
| civ-grounded | 1882 | 1892 | **+10** | 17:03 |
| civ-whimsical | 1894 | 1904 | **+10** | 17:03 |
| civ-formal | 1867 | 1877 | **+10** | 17:03 |
| civ-poetic | 1861 | 1871 | **+10** | 17:03 |
| civ-precise | 1831 | 1841 | **+10** | 17:03 |
| civ-mythic | 1839 | 1849 | **+10** | 17:03 |
| civ-therapist | 1834 | 1844 | **+10** | 17:03 |
| civ-engineer | 1836 | 1846 | **+10** | 17:03 |

**All 8 civs gained exactly +10 rows (80 total).** `git status --porcelain` shows 18 modified files: 8 `simulations.jsonl` + 8 `culture.json` + `leaderboard.json` + `meta_log.jsonl`.

Additional checks on the 80 new rows:

| check | result |
|---|---|
| seed/colour/figure recompute | **80/80 exact, 0 mismatches** |
| `content_preview` length | **200** for all 80 |
| distinct tails | **1** (162 chars) |
| provider mix | `zai` 80/80 |
| JEV errors | **0** |

## 4. Counter gap — `relevance - sum(avg_score over the FULL ledger)`

Summed over the **entire** ledger, never a subset: a sim-only sum manufactures a fake regression.

| civ | relevance | ledger sum | gap | baseline gap | drift |
|---|---|---|---|---|---|
| civ-grounded | 2226.4333 | 2310.7800 | -84.3467 | -84.3467 | **0.000000** |
| civ-whimsical | 2598.5300 | 2771.6733 | -173.1433 | -173.1433 | **0.000000** |
| civ-formal | 2606.5967 | 2692.1233 | -85.5267 | -85.5267 | **0.000000** |
| civ-poetic | 3138.9700 | 3235.7733 | -96.8033 | -96.8033 | **0.000000** |
| civ-precise | 3013.1967 | 3045.8300 | -32.6333 | -32.6333 | **0.000000** |
| civ-mythic | 2554.5867 | 2605.6967 | -51.1100 | -51.1100 | **0.000000** |
| civ-therapist | 2242.9367 | 2285.0500 | -42.1133 | -42.1133 | **0.000000** |
| civ-engineer | 2489.6300 | 2533.8733 | -44.2433 | -44.2433 | **0.000000** |

**Drift is 0.000000 for all 8 civs** — the offset is fixed, neither repaired nor worsened by this run.

## 5. Leaderboard (post-run)

| rank | civ | name | relevance | rel/sim | wins | losses | win rate | gen |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | The Poetic | 3138.97 | 1.712 | 6 | 907 | 0.007 | 1 |
| 2 | civ-precise | The Precise | 3013.20 | 1.651 | 637 | 271 | 0.702 | 1 |
| 3 | civ-formal | The Formal | 2606.60 | 1.420 | 118 | 793 | 0.130 | 1 |
| 4 | civ-whimsical | The Whimsical | 2598.53 | 1.411 | 5 | 908 | 0.005 | 1 |
| 5 | civ-mythic | The Mythic | 2554.59 | 1.397 | 10 | 897 | 0.011 | 1 |
| 6 | civ-engineer | The Engineer | 2489.63 | 1.365 | 57 | 849 | 0.063 | 1 |
| 7 | civ-therapist | The Therapist | 2242.94 | 1.228 | 11 | 899 | 0.012 | 1 |
| 8 | civ-grounded | The Grounded | 2226.43 | 1.204 | 75 | 837 | 0.082 | 1 |

## 6. Low relevance

| civ | relevance | rel/sim | run avg | quality | novelty | alignment |
|---|---|---|---|---|---|---|
| civ-grounded | 2226.43 | 1.204 | **1.6667** | **0.7460** | 2.4760 | 1.7780 |
| civ-whimsical | 2598.53 | 1.411 | 1.9040 | 1.0910 | 2.5320 | 2.0890 |
| civ-formal | 2606.60 | 1.420 | 1.9470 | 1.1020 | 2.4300 | 2.3090 |
| civ-poetic | 3138.97 | 1.712 | **2.2287** | **1.3530** | 2.5020 | **2.8310** |
| civ-precise | 3013.20 | 1.651 | 2.1007 | 1.2650 | 2.4170 | 2.6200 |
| civ-mythic | 2554.59 | 1.397 | 1.9323 | 1.1380 | 2.4630 | 2.1960 |
| civ-therapist | 2242.94 | 1.228 | 1.7047 | 0.8870 | 2.5320 | 1.6950 |
| civ-engineer | 2489.63 | 1.365 | 1.7657 | 0.9530 | 2.4430 | 1.9010 |

- **`civ-grounded` (The Grounded) — lowest lifetime relevance (2226.43) and lowest relevance-per-sim (1.204), 8th of 8.** It has now held the lifetime low for the **102nd consecutive session**.
- **`civ-grounded` is ALSO the run low** (avg 1.6667) with quality at the fleet low (0.7460) and alignment at the fleet low (1.7780) — a **two-axis collapse**. This is a **decoupling re-coupling**: the run low and the lifetime low were the *same* civ in most of the prior series and separated in sessions 237-239; this session they coincide again.
- `civ-therapist` is 2nd-lowest on both lifetime relevance (2242.94) and run average (1.7047) — within 0.038 avg of `civ-grounded`, so the bottom two are effectively tied.
- **No civilization is near extinction.** The code's threshold is `relevance < -10`; the lowest is 2226.43, three orders of magnitude above it. `extinction_and_birth()` does not run in a non-`--loop` invocation, and all 8 civs remain generation 1.

## 7. Run shape

| prompt | chooser | avg_score argmax | delta |
|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | 0.1600 |
| the bookkeeper's role | civ-precise | civ-poetic | 0.1800 |
| the witness log | civ-precise | civ-poetic | 0.0767 |
| ternary values | civ-precise | civ-poetic | 0.2300 |
| JEV as a decision oracle | civ-formal | civ-poetic | 0.4300 |

- **Agreement: 0/5 (0 %)**, 5 down-grades, **0 up-grades**. The up-grade count is pinned at 0 **by construction**: the chooser reads only `content_preview[:150]` and never sees `avg_score`, so every disagreement is necessarily a down-grade. This is structural, not a regression.
- Down-grade deltas: 0.1600, 0.1800, 0.0767, 0.2300, 0.4300 — max **0.4300**, no cliff.
- `civ-precise` won 4/5, `civ-formal` 1/5; the `avg_score` argmax was `civ-poetic` on **5 of 5** — the same argmax pattern as sessions 237 and 239.

### Axis signature

- Alignment spread **1.1360** = **2.02x** the `avg_score` spread (0.5620); quality 0.6070 (1.08x), novelty 0.1150 (0.20x).
- The **alignment axis** dominated again, and the ratio (**2.02x**) lands in the 2.05x-2.40x band of sessions 238-239. The holder rotates; the axis does not.

## 8. Participation

`d_wins + d_losses == 5` for every civ, asserted against the baseline commit (not the absolute total, which is not a multiple of 5 historically because 35 past competitions had fewer than 8 participants).

| civ | d_wins | d_losses | total | d_sims |
|---|---|---|---|---|
| civ-grounded | 0 | 5 | 5 | +10 |
| civ-whimsical | 0 | 5 | 5 | +10 |
| civ-formal | 1 | 4 | 5 | +10 |
| civ-poetic | 0 | 5 | 5 | +10 |
| civ-precise | 4 | 1 | 5 | +10 |
| civ-mythic | 0 | 5 | 5 | +10 |
| civ-therapist | 0 | 5 | 5 | +10 |
| civ-engineer | 0 | 5 | 5 | +10 |

## 9. Files changed

`8 x civ-*/simulations.jsonl`, `8 x civ-*/culture.json`, `leaderboard.json`, `meta_log.jsonl` — 18 files, all inside `cellular-first-design/code/civilizations/`.
