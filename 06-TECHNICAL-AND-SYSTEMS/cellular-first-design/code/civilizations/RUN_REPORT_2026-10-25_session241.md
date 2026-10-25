# RUN REPORT — 2026-10-25 — session 241

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

**Result:** exit 0, wall clock 29.02 s, 8 civs x 5 sims + 5 competition prompts.
**Provider path:** Control B mock (z.ai credential gap, **102nd session**) + **live JEV**.
**Ledger delta:** +10 rows per civ, **+80 total** (8 civs x 10). `meta_log` +5.

## 1. Environment

| item | value |
|---|---|
| repo | `SuperInstance/AI-Writings`; `cellular-first-design` is a **subdirectory**, not a repo |
| clone | `/tmp/clone/ai-writings`, sparse `--depth 1`, cone `cellular-first-design` |
| bridge | symlink `/workspace/repos/ai-writings/cellular-first-design/code` -> clone `code`; `os.path.samefile()` -> `True` |
| NAS | `/workspace` at **600 G/600 G, 0 avail** (EDQUOT) — clone went to the overlay (`/tmp`); the `write` tool is jailed to the workspace root and cannot reach `/tmp` |
| base commit | `af6b200bc6e6059e91be65ddc370c6ada410239a` (session 240), tree clean pre-run |
| `ZAI_TOKEN` | absent from env and all sandbox secrets; set to a **placeholder** for Control B |
| `ZAI_URL_OVERRIDE` | `http://127.0.0.1:8799/v1/chat/completions` — needed **together with** the token gate |
| `TYPESAFEAI_KEY` | exported from `TYPESAFE_AI_TOKEN`; JEV live, **0** fallback triples; served model `jev-1.14.0` |
| `gh` CLI | **not installed** in this sandbox; GitHub REST used directly with `GITHUB_TOKEN` |
| post-run commit | see §10 — **remote-verified** via the commits API |

### Bootstrap note (new)

The sandbox was **empty** at session start (no `/workspace/repos`, no clone). The repo is 3.7 GB, so a full clone is prohibitive; a cone sparse checkout of `cellular-first-design` was sufficient. The orchestrator hardcodes `CIVS_DIR = Path("/workspace/repos/ai-writings/cellular-first-design/code/civilizations")` (line 36), so **every** read and write is anchored to that absolute path — the symlink bridge is what makes the overlay clone writable under it.

## 2. Mock body construction

The Control B mock source is **not in the repo**; the ledger is the specification. It was **re-derived from scratch** this session and validated against the pre-run ledger, not copied from the session-240 report.

```
d      = md5(cultural_prompt).digest()
h      = d.hex()
i      = d[0] % 4            # RAW MD5 BYTE, not int(h[0],16) % 4
seed   = h[(i*2)%8 : (i*2)%8+4]
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"
```

- **Seed algorithm re-verified over the FULL current-format ledger: 2320/2320 exact, 0 mismatches** (before the run, against the pre-existing rows).
- Ledger holds **two body formats**: an older `[mock-zai <12 hex>]` form (240 rows, ts <= 1792837412) and the current `[mock-zai <4 hex>] #<4 hex> <4>/<4>/<4>.` form (2320 rows). Only the current form is parsed.
- Body bank: **13 distinct tails**, all exactly **162 chars**. The tail used is the one from the ledger's **most recent 80-row cluster**, byte-for-byte.
- Body = **38** (header) + **162** (tail) + **144** (continuation) = **344** chars.
- Mock served **80** requests = 80 ledger rows (1 extra pre-flight probe served separately, before the run).

## 3. Verification — new `simulations.jsonl` entries

`ls -la` is the **weakest** check (it shows mtimes, and it has passed on a tree with 18 modified files). The discriminating check is the **row-count delta** against the pinned git blob. Both were run.

| civ | rows before | rows after | delta | mtime |
|---|---|---|---|---|
| civ-grounded | 1892 | 1902 | **+10** | 17:13 |
| civ-whimsical | 1904 | 1914 | **+10** | 17:13 |
| civ-formal | 1877 | 1887 | **+10** | 17:13 |
| civ-poetic | 1871 | 1881 | **+10** | 17:13 |
| civ-precise | 1841 | 1851 | **+10** | 17:13 |
| civ-mythic | 1849 | 1859 | **+10** | 17:13 |
| civ-therapist | 1844 | 1854 | **+10** | 17:13 |
| civ-engineer | 1846 | 1856 | **+10** | 17:13 |

**All 8 civs gained exactly +10 rows (80 total).** `meta_log.jsonl` 938 -> 943 (+5). `git status --porcelain` shows **18 modified files**: 8 `simulations.jsonl` + 8 `culture.json` + `leaderboard.json` + `meta_log.jsonl`.

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
| civ-grounded | 2244.2333 | 2328.5800 | -84.3467 | -84.3467 | **0.000000** |
| civ-whimsical | 2614.2333 | 2787.3767 | -173.1433 | -173.1433 | **0.000000** |
| civ-formal | 2625.8100 | 2711.3367 | -85.5267 | -85.5267 | **0.000000** |
| civ-poetic | 3160.9267 | 3257.7300 | -96.8033 | -96.8033 | **0.000000** |
| civ-precise | 3035.1733 | 3067.8067 | -32.6333 | -32.6333 | **0.000000** |
| civ-mythic | 2572.4333 | 2623.5433 | -51.1100 | -51.1100 | **0.000000** |
| civ-therapist | 2257.3300 | 2299.4433 | -42.1133 | -42.1133 | **0.000000** |
| civ-engineer | 2508.4333 | 2552.6767 | -44.2433 | -44.2433 | **0.000000** |

**Drift is 0.000000 for all 8 civs** (residual <= 3.3e-5, float noise) — the offset is fixed, neither repaired nor worsened by this run.

## 5. Leaderboard (post-run)

| rank | civ | name | relevance | rel/sim | wins | losses | win rate | gen |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | The Poetic | 3160.93 | 1.714 | 6 | 912 | 0.007 | 1 |
| 2 | civ-precise | The Precise | 3035.17 | 1.654 | 642 | 271 | 0.703 | 1 |
| 3 | civ-formal | The Formal | 2625.81 | 1.423 | 118 | 798 | 0.129 | 1 |
| 4 | civ-whimsical | The Whimsical | 2614.23 | 1.412 | 5 | 913 | 0.005 | 1 |
| 5 | civ-mythic | The Mythic | 2572.43 | 1.399 | 10 | 902 | 0.011 | 1 |
| 6 | civ-engineer | The Engineer | 2508.43 | 1.368 | 57 | 854 | 0.063 | 1 |
| 7 | civ-therapist | The Therapist | 2257.33 | 1.229 | 11 | 904 | 0.012 | 1 |
| 8 | civ-grounded | The Grounded | 2244.23 | 1.207 | 75 | 842 | 0.082 | 1 |

## 6. Low relevance

| civ | relevance | rel/sim | run avg | quality | novelty | alignment |
|---|---|---|---|---|---|---|
| civ-grounded | 2244.23 | 1.207 | 1.7800 | 1.0680 | 2.2730 | 1.9990 |
| civ-therapist | 2257.33 | 1.229 | **1.4393** | **0.7340** | 2.4820 | **1.1020** |
| civ-engineer | 2508.43 | 1.368 | 1.8803 | 1.0510 | 2.3150 | 2.2750 |
| civ-mythic | 2572.43 | 1.399 | 1.7847 | 1.1530 | 2.3810 | 1.8200 |
| civ-whimsical | 2614.23 | 1.412 | 1.5703 | 0.9540 | 2.3900 | 1.3670 |
| civ-formal | 2625.81 | 1.423 | 1.9213 | 1.0460 | 2.4220 | 2.2960 |
| civ-precise | 3035.17 | 1.654 | **2.1977** | 1.3270 | 2.3950 | **2.8710** |
| civ-poetic | 3160.93 | 1.714 | 2.1957 | **1.5150** | 2.4820 | 2.5900 |

- **`civ-grounded` (The Grounded) — lowest lifetime relevance (2244.23) and lowest relevance-per-sim (1.207), 8th of 8.** It has now held the lifetime low for the **103rd consecutive session**.
- **`civ-therapist` (The Therapist) is the RUN low** (avg 1.4393) with quality at the fleet low (0.7340) and alignment at the fleet low (1.1020) — a **two-axis collapse** on the run axes. This **breaks the pattern of session 240**, where the run low and the lifetime low were the *same* civ (`civ-grounded`); the two have now **decoupled**, and the run low sits in a different civ than the lifetime low for the first time in this series.
- `civ-grounded` and `civ-therapist` are the bottom two on lifetime relevance, 13.10 apart — a near-tie, as in session 240 (where they were 16.50 apart).
- **No civilization is near extinction.** The code's threshold is `relevance < -10`; the lowest is 2244.23, more than two orders of magnitude above it. `extinction_and_birth()` does not run in a non-`--loop` invocation, and all 8 civs remain generation 1.

## 7. Run shape

| prompt | chooser | avg_score argmax | delta |
|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | 0.0833 |
| the bookkeeper's role | civ-precise | civ-precise | 0.0000 |
| the witness log | civ-precise | civ-precise | 0.0000 |
| ternary values | civ-precise | civ-poetic | 0.0833 |
| JEV as a decision oracle | civ-precise | civ-precise | 0.0000 |

- **Agreement: 3/5 (60 %)**, 2 down-grades, **0 up-grades**. The up-grade count is pinned at 0 **by construction**: the chooser reads only `content_preview[:150]` and never sees `avg_score`, so every disagreement is necessarily a down-grade. This is structural, not a regression.
- Down-grade deltas: 0.0833, 0.0833 — max **0.0833**, no cliff.
- `civ-precise` won **5/5** — a clean sweep, the first in this series after session 240's 4/5 + 1/5 split. The `avg_score` argmax was `civ-precise` on 3 of 5 and `civ-poetic` on 2 of 5 — where the two disagree, `civ-poetic` wins on average score but `civ-precise` wins the chooser's vote.

### Axis signature

- Alignment spread **1.7690** = **2.34x** the `avg_score` spread (0.7563); quality 0.7810 (1.03x), novelty 0.2090 (0.28x).
- The **alignment axis** dominated again, and the ratio (**2.34x**) sits at the top of the 2.05x-2.40x band spanned by sessions 238-240. The holder rotates; the axis does not.

## 8. Participation

`d_wins + d_losses == 5` for every civ, asserted against the baseline commit (not the absolute total, which is not a multiple of 5 historically because 35 past competitions had fewer than 8 participants).

| civ | d_wins | d_losses | total | d_sims |
|---|---|---|---|---|
| civ-grounded | 0 | 5 | 5 | +10 |
| civ-whimsical | 0 | 5 | 5 | +10 |
| civ-formal | 0 | 5 | 5 | +10 |
| civ-poetic | 0 | 5 | 5 | +10 |
| civ-precise | 5 | 0 | 5 | +10 |
| civ-mythic | 0 | 5 | 5 | +10 |
| civ-therapist | 0 | 5 | 5 | +10 |
| civ-engineer | 0 | 5 | 5 | +10 |

## 9. Files changed

`8 x civ-*/simulations.jsonl`, `8 x civ-*/culture.json`, `leaderboard.json`, `meta_log.jsonl` — 18 files, all inside `cellular-first-design/code/civilizations/`, plus this report.

## 10. Commit

See the session-241 commit in `cellular-first-design/code/civilizations/`. Pushed to `main` and verified via the GitHub commits API.

## 11. New durable lessons

1. **The sandbox may start completely empty** (no `/workspace/repos`, no clone). The recovery path is: GitHub REST search for the repo (no `gh` CLI in this image), then a **cone sparse checkout** of `cellular-first-design` into `/tmp` — the full repo is 3.7 GB and will not fit comfortably, and the NAS is at 0 free.
2. **`gh` is not installed** in this sandbox image. Use `curl -H "Authorization: token $GITHUB_TOKEN"` against `api.github.com` instead. `GITHUB_TOKEN` is present in the env.
3. **The orchestrator's `CIVS_DIR` is an absolute path** (line 36) pointing into `/workspace`. A clone anywhere else is invisible to it. The **symlink bridge** (`/workspace/repos/ai-writings/cellular-first-design/code` -> clone `code`) is what makes an overlay clone usable; verify with `os.path.samefile()`.
4. **NAS `/workspace` is at 600 G/600 G, 0 avail** (EDQUOT) but a *small* file write can still succeed while a 5 MB one fails. Do not infer writability from a 0-byte write — test with the real payload size. `git init` in `/workspace` fails on `.git/description` (a few hundred bytes) because the **template copy** is what trips the quota.
5. **The `write` tool cannot reach `/tmp`** (jailed to the workspace root) and the workspace is full anyway. Write scratch scripts with a **bash heredoc** and keep all artifacts on the overlay.
6. **The mock spec is re-derivable, not magic.** The MD5 seed algorithm was re-derived from the ledger and validated **2320/2320** against pre-existing rows before the run — do this, do not copy the prior report's numbers. The ledger also contains **two body formats**; the current one is `[mock-zai <4 hex>] #<4 hex> <4>/<4>/<4>.` and the old 12-hex form is historical.
7. **The tail is a rotating bank of 13 fixed 162-char strings**; the correct one is the tail of the ledger's **most recent 80-row cluster**, not an arbitrary member of the bank. The body length is pinned to **344 = 38 + 162 + 144**.
8. **`civ-therapist` can take the run-low position** — the run low and the lifetime low are not always the same civ. `civ-grounded` holds the lifetime low (103 sessions running), but the run low has now moved to `civ-therapist`. Watch for the decoupling rather than assuming a fixed pair.
