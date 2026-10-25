# RUN REPORT — 2026-10-25 — session 242

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

**Result:** exit 0, wall clock 29 s (17:24:05Z -> 17:24:34Z), 8 civs x 5 sims + 5 competition prompts.
**Provider path:** Control B mock (z.ai credential gap, **103rd session**) + **live JEV** (`jev-1.14.0`).
**Ledger delta:** +10 rows per civ, **+80 total** (8 civs x 10). `meta_log` +5.

## 1. Environment

| item | value |
|---|---|
| repo | `SuperInstance/AI-Writings`; `cellular-first-design` is a **subdirectory**, not a repo |
| clone | `/tmp/clone`, sparse `--depth 1`, cone `cellular-first-design` (full repo is 3.7 GB) |
| bridge | symlink `/workspace/repos/ai-writings/cellular-first-design/code` -> clone `code`; `os.path.samefile()` -> `True` |
| NAS | `/workspace` at **600 G/600 G, 0 avail** (EDQUOT) — `git clone` into it fails on `.git/description`; the clone went to the overlay (`/tmp`) |
| base commit | `febed5b6037deb581ea37334d0fc44227e56d585` (session 241), tree clean pre-run |
| `ZAI_TOKEN` | absent from env; set to a **placeholder** for Control B |
| `ZAI_URL_OVERRIDE` | `http://127.0.0.1:8799/v1/chat/completions` — needed **together with** the token gate |
| `TYPESAFEAI_KEY` | exported from `TYPESAFE_AI_TOKEN`; JEV live, **0** fallback triples; served model `jev-1.14.0` |
| `gh` CLI | **not installed** in this sandbox; GitHub REST used directly with `GITHUB_TOKEN` |

### Bootstrap note

The sandbox was **empty** at session start (no `/workspace/repos`, no clone) — the 7th consecutive empty-wipe. Recovery: GitHub REST search for the repo (no `gh` CLI), then a **cone sparse checkout** of `cellular-first-design` into `/tmp`. The orchestrator hardcodes `CIVS_DIR = Path("/workspace/repos/ai-writings/cellular-first-design/code/civilizations")` (line 36), so the **symlink bridge** is what makes an overlay clone writable under it.

## 2. Mock body construction

The Control B mock source is **not in the repo**; the ledger is the specification. It was **re-derived from scratch** this session and validated against the pre-run ledger, not copied from the session-241 report.

```
d      = md5(cultural_prompt).digest()
h      = d.hex()
i      = d[0] % 4            # RAW MD5 BYTE, not int(h[0],16) % 4
seed   = h[(i*2)%8 : (i*2)%8+4]
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"
```

- **Seed algorithm re-verified over the FULL current-format ledger: 2400/2400 exact, 0 mismatches** (before the run, against pre-existing rows).
- The `int(h[0],16) % 4` reading was tested as a competing hypothesis and matched only **828/2400** — the raw-byte reading is the correct one.
- Ledger holds **two body formats**: an older `[mock-zai <12 hex>]` form (240 rows) and the current `[mock-zai <4 hex>] #<4 hex> <4>/<4>/<4>.` form (2400 rows). Only the current form is parsed.
- Body bank: **13 distinct tails**, all exactly **162 chars**. The tail rotates **per run** (30 runs reconstructed from ts gaps > 60 s); the correct one is the tail of the ledger's **most recent 80-row cluster**, byte-for-byte.
- Served body = **38** (header) + **162** (tail) + **144** (continuation) = **344** chars; the ledger stores `content_preview` truncated to 200.
- Mock served **80** requests = 80 ledger rows (1 extra pre-flight probe served separately, before the run).

## 3. Verification — new `simulations.jsonl` entries

`ls -la` is the **weakest** check (it shows mtimes, and it has passed on a tree with 18 modified files). The discriminating check is the **row-count delta** against the pinned git blob. Both were run.

| civ | rows before | rows after | delta | mtime |
|---|---|---|---|---|
| civ-grounded | 1902 | 1912 | **+10** | 17:24 |
| civ-whimsical | 1914 | 1924 | **+10** | 17:24 |
| civ-formal | 1887 | 1897 | **+10** | 17:24 |
| civ-poetic | 1881 | 1891 | **+10** | 17:24 |
| civ-precise | 1851 | 1861 | **+10** | 17:24 |
| civ-mythic | 1859 | 1869 | **+10** | 17:24 |
| civ-therapist | 1854 | 1864 | **+10** | 17:24 |
| civ-engineer | 1856 | 1866 | **+10** | 17:24 |

**All 8 civs gained exactly +10 rows (80 total).** `meta_log.jsonl` 943 -> 948 (+5). `git status --porcelain` shows **18 modified files**: 8 `simulations.jsonl` + 8 `culture.json` + `leaderboard.json` + `meta_log.jsonl`.

Additional checks on the 80 new rows:

| check | result |
|---|---|
| seed/colour/figure recompute | **80/80 exact, 0 mismatches** |
| `content_preview` length | **200** for all 80 |
| distinct bodies | **1** (162-char tail) |
| provider mix | `zai` 80/80 |
| `civ` field matches directory | **80/80** |
| JEV errors | **0** |
| fallback triples (all-2.0) | **0** |

## 4. Counter gap — `relevance - sum(avg_score over the FULL ledger)`

Summed over the **entire** ledger, never a subset: a sim-only sum manufactures a fake regression.

| civ | relevance | ledger sum | gap | baseline gap | drift |
|---|---|---|---|---|---|
| civ-grounded | 2253.9367 | 2338.2833 | -84.3467 | -84.3467 | **0.000000** |
| civ-whimsical | 2626.2800 | 2799.4233 | -173.1433 | -173.1433 | **0.000000** |
| civ-formal | 2637.4500 | 2722.9767 | -85.5267 | -85.5267 | **0.000000** |
| civ-poetic | 3176.3567 | 3273.1600 | -96.8033 | -96.8033 | **0.000000** |
| civ-precise | 3050.3167 | 3082.9500 | -32.6333 | -32.6333 | **0.000000** |
| civ-mythic | 2582.7367 | 2633.8467 | -51.1100 | -51.1100 | **0.000000** |
| civ-therapist | 2265.6033 | 2307.7167 | -42.1133 | -42.1133 | **0.000000** |
| civ-engineer | 2520.5567 | 2564.8000 | -44.2433 | -44.2433 | **0.000000** |

**Drift is 0.000000 for all 8 civs** — the offset is fixed, neither repaired nor worsened by this run.

## 5. Leaderboard (post-run)

| rank | civ | name | relevance | rel/sim | wins | losses | win rate | gen |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | The Poetic | 3176.36 | 1.713 | 6 | 917 | 0.007 | 1 |
| 2 | civ-precise | The Precise | 3050.32 | 1.653 | 646 | 272 | 0.704 | 1 |
| 3 | civ-formal | The Formal | 2637.45 | 1.422 | 119 | 802 | 0.129 | 1 |
| 4 | civ-whimsical | The Whimsical | 2626.28 | 1.411 | 5 | 918 | 0.005 | 1 |
| 5 | civ-mythic | The Mythic | 2582.74 | 1.397 | 10 | 907 | 0.011 | 1 |
| 6 | civ-engineer | The Engineer | 2520.56 | 1.367 | 57 | 859 | 0.062 | 1 |
| 7 | civ-therapist | The Therapist | 2265.60 | 1.227 | 11 | 909 | 0.012 | 1 |
| 8 | civ-grounded | The Grounded | 2253.94 | 1.206 | 75 | 847 | 0.081 | 1 |

## 6. Low relevance

| civ | relevance | rel/sim | run avg | quality | novelty | alignment |
|---|---|---|---|---|---|---|
| civ-grounded | 2253.94 | 1.206 | 0.9703 | 0.2940 | 1.2820 | 1.3350 |
| civ-therapist | 2265.60 | 1.227 | **0.8273** | **0.2320** | 1.5790 | **0.6710** |
| civ-engineer | 2520.56 | 1.367 | 1.2123 | 0.4680 | 1.2830 | 1.8860 |
| civ-mythic | 2582.74 | 1.397 | 1.0303 | 0.4750 | 1.3290 | 1.2870 |
| civ-whimsical | 2626.28 | 1.411 | 1.2047 | 0.4270 | 1.7170 | 1.4700 |
| civ-formal | 2637.45 | 1.422 | 1.1640 | 0.3860 | 1.4460 | 1.6600 |
| civ-precise | 3050.32 | 1.653 | 1.5143 | 0.7260 | 1.4730 | **2.3440** |
| civ-poetic | 3176.36 | 1.713 | **1.5430** | **0.9000** | 1.5320 | 2.1970 |

- **`civ-grounded` (The Grounded) — lowest lifetime relevance (2253.94) and lowest relevance-per-sim (1.206), 8th of 8.** It has now held the lifetime low for the **104th consecutive session**.
- **`civ-therapist` (The Therapist) is the RUN low** (avg 0.8273) with quality at the fleet low (0.2320) and alignment at the fleet low (0.6710) — the **same two-axis collapse as session 241**, now on a wider margin (session 241: 1.4393 / 0.7340 / 1.1020).
- The run low and the lifetime low are **different civs for the second consecutive session** — the decoupling is now a standing pattern, not a one-off.
- `civ-grounded` and `civ-therapist` are the bottom two on lifetime relevance, **11.67 apart** (session 241: 13.10).
- **No civilization is near extinction.** The code's threshold is `relevance < -10`; the lowest is 2253.94, more than two orders of magnitude above it. `extinction_and_birth()` does not run in a non-`--loop` invocation, and all 8 civs remain generation 1.

## 7. Run shape

| prompt | chooser | avg_score argmax | delta |
|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | 0.1300 |
| the bookkeeper's role | civ-precise | civ-poetic | 0.0633 |
| the witness log | civ-formal | civ-precise | 0.3533 |
| ternary values | civ-precise | civ-poetic | 0.0367 |
| JEV as a decision oracle | civ-precise | civ-poetic | 0.1167 |

- **Agreement: 0/5 (0 %)**, 5 down-grades, **0 up-grades**. The up-grade count is pinned at 0 **by construction**: the chooser reads only `content_preview[:150]` and never sees `avg_score`, so every disagreement is necessarily a down-grade. This is structural, not a regression.
- This is the **lowest agreement in the series** (session 240: 3/5; session 241: 3/5). Down-grade deltas run 0.0367-0.3533, max **0.3533** (the witness log) — wider than session 241's 0.0833 ceiling, but no single cliff dominating.
- `civ-precise` won **4/5**; `civ-formal` took the witness log. The `avg_score` argmax was `civ-poetic` on **4 of 5** — where the two disagree, `civ-poetic` wins on average score but loses the chooser's vote.

### Axis signature

- Alignment spread **1.6730** = **2.34x** the `avg_score` spread (0.7157); quality 0.6680 (0.93x), novelty 0.4350 (0.61x).
- The **alignment axis** dominated again, and the ratio (**2.34x**) is identical to session 241's 2.34x and sits at the top of the 2.05x-2.40x band spanned by sessions 238-241. The holder rotates; the axis does not.

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

`8 x civ-*/simulations.jsonl`, `8 x civ-*/culture.json`, `leaderboard.json`, `meta_log.jsonl` — 18 files, all inside `cellular-first-design/code/civilizations/`, plus this report.

## 10. Commit

See the session-242 commit in `cellular-first-design/code/civilizations/`. Pushed to `main` and verified via the GitHub commits API.

## 11. New durable lessons

1. **The mock tail rotates per RUN, not per row.** Reconstructing the runs from ts gaps > 60 s gives 30 distinct runs over 2400 current-format rows, and each run uses exactly one tail (except one mixed row-level probe run). The prior report's "most recent 80-row cluster" rule is the right instinct but the correct unit is the **run**, and the tail bank has **13** members, not a fixed "correct" one — pick the tail of the most recent *run*, not the most recent row.
2. **The competing seed hypothesis is measurably wrong, not merely different.** `int(h[0],16) % 4` matches 828/2400; `d[0] % 4` (raw byte) matches **2400/2400**. When a spec has two readings, score both against the full ledger before running rather than copying the prior report's claim.
3. **Chooser agreement can legitimately hit 0/5.** Session 241 recorded 3/5, so 0/5 looks like a regression at a glance — but the up-grade count is structurally pinned at 0 (the chooser never sees `avg_score`), so agreement can only ever fall, never rise, from the argmax. Track the **down-grade delta magnitude** (0.0367-0.3533 this run) as the real signal, not the agreement rate.
4. **The run-low / lifetime-low decoupling is now a standing pattern** (two consecutive sessions), with `civ-grounded` holding the lifetime low (104 sessions running) and `civ-therapist` the run low on a quality+alignment two-axis collapse. Do not assume the two are the same civ.
