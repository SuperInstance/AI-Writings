# RUN REPORT — 2026-10-25 — session 239

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

**Result:** exit 0, wall clock 29.06 s, 8 civs x 5 sims + 5 competition prompts.
**Provider path:** Control B mock (z.ai credential gap, **93rd session**) + **live JEV** (`jev-1.14.0`).
**Ledger delta:** +10 rows per civ, **+80 total** (8 civs x 10).

## 1. Environment

| item | value |
|---|---|
| repo | `SuperInstance/AI-Writings` (user account), `cellular-first-design` is a **subdirectory**, not a repo |
| clone | `/tmp/cfd-meta`, `--depth 1 --filter=blob:none --no-checkout` + `sparse-checkout set cellular-first-design/code/civilizations` |
| bridge | symlink `/workspace/repos/ai-writings/cellular-first-design` -> clone root; `os.path.samefile()` -> `True` |
| NAS | `/workspace` at **600 G/600 G, 0 avail** (EDQUOT) — clone went to the overlay (`/tmp`, 28 G) |
| base commit | `6b894fcc59b7f832d2e01f46e4ecb1e81548dcae`, tree clean pre-run |
| z.ai real endpoint | **HTTP 401** `token expired or incorrect` — endpoint healthy, credential absent |
| `ZAI_TOKEN` | absent from env and all sandbox secrets; set to a **placeholder** for Control B |
| `ZAI_URL_OVERRIDE` | `http://127.0.0.1:8799/v1/chat/completions` — needed **together with** the token gate |
| `TYPESAFEAI_KEY` | exported from `TYPESAFE_AI_TOKEN`; JEV live, **0** fallback triples |

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

- **Seed algorithm re-verified over the FULL current-format ledger: 2160/2160 exact, 0 mismatches** (before the run, not against our own fresh rows).
- Tail **extracted byte-for-byte** from the ledger's most recent 80-row cluster: 162 chars, 13 distinct tails in history, identical set for all 8 civs.
- Body = 38 (header) + 162 (tail) + **146** (continuation) = **346** chars, inside the 332-369 band, ending on a word boundary.
- Mock served **82** requests = 1 pre-flight + 1 repeat probe + 80 ledger rows.

## 3. Verification — new `simulations.jsonl` entries

`ls -la` is the **weakest** check (it shows mtimes, and it has passed on a tree with 18 modified files). The discriminating check is the **row-count delta** against the pinned git blob, plus the counter-gap check. Both were run.

| civ | rows before | rows after | delta | mtime |
|---|---|---|---|---|

**All 8 civs gained exactly +10 rows (80 total).** `git status --porcelain` shows 18 modified files: 8 `simulations.jsonl` + 8 `culture.json` + `leaderboard.json` + `meta_log.jsonl`.

Additional checks on the 80 new rows:

| check | result |
|---|---|
| seed/colour/figure recompute | **80/80 exact, 0 mismatches** |
| `content_preview` length | **200** for all 80 |
| distinct tails | **1** (162 chars), byte-identical to the extracted session tail |
| provider mix | `zai` 80/80 |
| JEV errors | **0** |

## 4. Counter gap — `relevance - sum(avg_score over the FULL ledger)`

Summed over the **entire** ledger, never a subset: a sim-only sum manufactures a fake regression.

| civ | relevance | ledger sum | gap | baseline gap | drift |
|---|---|---|---|---|---|
| civ-grounded | 2209.7667 | 2294.1133 | **-84.3467** | -84.3467 | **0.000000** |
| civ-whimsical | 2579.4900 | 2752.6333 | **-173.1433** | -173.1433 | **0.000000** |
| civ-formal | 2587.1267 | 2672.6533 | **-85.5267** | -85.5267 | **0.000000** |
| civ-poetic | 3116.6833 | 3213.4867 | **-96.8033** | -96.8033 | **0.000000** |
| civ-precise | 2992.1900 | 3024.8233 | **-32.6333** | -32.6333 | **0.000000** |
| civ-mythic | 2535.2633 | 2586.3733 | **-51.1100** | -51.1100 | **0.000000** |
| civ-therapist | 2225.8900 | 2268.0033 | **-42.1133** | -42.1133 | **0.000000** |
| civ-engineer | 2471.9733 | 2516.2167 | **-44.2433** | -44.2433 | **0.000000** |

**Drift is 0.000000 for all 8 civs** — the offset is fixed, neither repaired nor worsened by this run.

*Attribution note:* the counter itself is exact. A first pass that compared the **rounded** `culture.json` value against the **full-precision** ledger sum showed a ±0.003333 pseudo-drift; the artefact is the 4-dp storage of `relevance_score` in `culture.json`, not the counter. Recomputing `relevance` as `baseline_relevance + sum(new avg_score)` reproduces the stored value to **0.000000** for all 8 civs. *A drift read off a rounded field is a formatting artefact, not a movement.*

## 5. Leaderboard (post-run)

| rank | civ | name | relevance | rel/sim | wins | losses | win rate |
|---|---|---|---|---|---|---|---|

## 6. Low relevance

| civ | relevance | rel/sim | run avg | quality | novelty | alignment |
|---|---|---|---|---|---|---|

- **`civ-grounded` (The Grounded) — lowest lifetime relevance (2209.77) and lowest relevance-per-sim (1.202)**, 8th of 8. It has now held the lifetime low for the **101st consecutive session**. Its run average was 1.7283, mid-pack, with novelty at the run low (2.4790) — a single-axis profile.
- **`civ-therapist` (The Therapist) — the run low** (avg 1.4433) with a **two-axis collapse**: quality 0.6170 and alignment 1.0330 both at the fleet low, while novelty held at 2.6800 (2nd-highest of 8).
- **No civilization is near extinction.** The code's threshold is `relevance < -10`; the lowest is 2209.77, three orders of magnitude above it. `extinction_and_birth()` does not run in a non-`--loop` invocation, and all 8 civs remain generation 1.

## 7. Run shape

| prompt | chooser | avg_score argmax | |
|---|---|---|---|

- **Agreement: 0/5 (0 %)**, 5 down-grades, **0 up-grades**. The up-grade count is pinned at 0 **by construction**: the chooser reads only `content_preview[:150]` and never sees `avg_score`, so every disagreement is necessarily a down-grade. This is structural, not a regression.
- Down-grade deltas: 0.2267, 0.1500, 0.0667, 0.1533, 0.4000 — max **0.4000**, no cliff.
- `civ-precise` won 4/5, `civ-formal` 1/5; the `avg_score` argmax was `civ-poetic` on **5 of 5**.

### Axis signature

- Alignment spread **2.4100** = **2.05x** the `avg_score` spread (1.1733); quality 1.4400 (1.23x), novelty 0.6600 (0.56x).
- The **alignment axis** dominated again. The holder rotates; the axis does not.

## 8. Participation

`d_wins + d_losses == 5` for every civ, asserted against the baseline commit (not the absolute total, which is not a multiple of 5 historically because 35 past competitions had fewer than 8 participants).

| civ | d_wins | d_losses | total |
|---|---|---|---|

## 9. Files changed

`8 x civ-*/simulations.jsonl`, `8 x civ-*/culture.json`, `leaderboard.json`, `meta_log.jsonl` — 18 files, all inside `cellular-first-design/code/civilizations/`.
