# Civ Orchestrator — Run Report, session 249 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **108th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `8f8934f` (session 248 tree). **Pre-flight gate: 11/11 PASS (40 requests).** **Run verification: 80 new rows, 0 FAIL.**

## Environment recovery

- Workspace **empty** apart from `.plugin-cache` — the prompt's path did not exist (**13th consecutive occurrence**).
- Upstream **`SuperInstance/AI-Writings`** (3.7 GB, a *user* account with 5400+ repos); the `ai-writings/…` slug 404s (the GitHub API is case-insensitive). `cellular-first-design` is a **subdirectory**, not a repo.
- Cloned to `/tmp/work/AIW` with `--filter=blob:none --no-checkout --depth 1` + `sparse-checkout set cellular-first-design/code/civilizations`.
  Cloning directly into `/workspace` fails with **`Disk quota exceeded`** (NAS EDQUOT, 600 G / 0 avail, **19th session**).
- Bridge symlink `…/cellular-first-design -> /tmp/work/AIW/cellular-first-design`; verified with `os.path.samefile()` → `True` and `REGISTRY.exists()` → `True`.
  The bridge target must be the **clone root** so the hard-coded `CIVS_DIR` resolves — an inner-`code` bridge yields `code/code/civilizations`.
- `ZAI_TOKEN` absent from env and from all 8 sandbox secrets; z.ai **401** `token expired or incorrect`
  => endpoint healthy, credential absent (**108th session**).
- **JEV live**: well-formed body => **HTTP 200** with `{"model":"jev-1.14.0", …}`.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code behind the token gate).
- `gh` not installed (**21st session**) — used `GET /user/repos` with `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~48 s => detached launch, stdout redirected, `< /dev/null`.
- Mock teardown by exact argv match (pids 318/320) — never `pkill -f mock_zai` (self-match).
  Port proven closed afterwards: `curl -m 5` => **HTTP=000, exit 7**.

## Mock integrity

Used the repo's own `tools/mock_zai.py` and `tools/preflight.py` unchanged — the `figure` fix
(`f"{h[12:16]}/{h[16:20]}/{h[20:24]}"`, three **string** components, not a division) is already in.

**Pre-flight gate: 11/11 PASS, exit 0** — 40/40 requests 200, 40/40 distinct previews,
40/40 distinct seeds, 40/40 md5 recomputes match, 38+162=200 geometry, all bodies **349** chars
(inside the 332-369 band), 149-char continuation, 5 distinct seeds per civ, 8 distinct seeds per prompt.

## Ledger delta

- **+10 rows per civ, +80 total**; `meta_log` **978 -> 983** (+5); **18** files changed.
- Every new row carries the documented **9 keys** (`ts, civ, civ_name, provider, params, prompt, scores, avg_score, content_preview`).
- Preview length **200** on every new row; all 80 rows parse as JSON.
- **JEV was live on all 80 rows**: 0 `error` fields, 0 zero-confidence rows (the fallback returns
  `confidence: 0.0`), confidence range **0.22 – 0.91**.
- **Counter reconciliation 8/8 OK** against the `delta = 2W - 5` rule: `civ-precise` won all 5
  competitions (W=5, gap **+5**); the seven losers (W=0) each moved **exactly -5**.

## Leaderboard (pre -> post, sorted by relevance_per_sim)

| civ | relevance | Δ | rel/sim | Δ | win_rate | wins |
|---|---|---|---|---|---|---|
| civ-poetic | 3298.92 -> 3318.54 | +19.62 | 1.724 -> 1.725 | +0.001 | 0.006 | 6 |
| civ-precise | 3170.59 -> 3189.66 | +19.07 | 1.664 -> 1.666 | +0.002 | 0.710 | 677 |
| civ-formal | 2743.29 -> 2760.98 | +17.69 | 1.433 -> 1.434 | +0.001 | 0.127 | 121 |
| civ-whimsical | 2719.43 -> 2734.70 | +15.27 | 1.416 -> 1.416 | +0.000 | 0.005 | 5 |
| civ-mythic | 2676.52 -> 2692.20 | +15.68 | 1.402 -> 1.403 | +0.001 | 0.011 | 10 |
| civ-engineer | 2622.85 -> 2639.39 | +16.54 | 1.378 -> 1.379 | +0.001 | 0.062 | 59 |
| civ-therapist | 2344.05 -> 2356.56 | +12.51 | 1.229 -> 1.229 | +0.000 | 0.012 | 11 |
| civ-grounded | 2345.20 -> 2360.67 | +15.47 | 1.216 -> 1.217 | +0.001 | 0.078 | 75 |

## Low-relevance civilizations

**`civ-grounded`** and **`civ-therapist`** occupy the bottom two slots and are the fleet's weakest
civs on the axes that matter:

- `civ-grounded` — **lowest relevance_per_sim in the fleet (1.216 -> 1.217)**, lowest lifetime
  quality (**0.548**), and lowest lifetime alignment among the low-relevance pair (**1.312**).
  It also has the **widest score spread in this run** (min 1.263, max 1.803) and the **lowest
  run average of the mid-pack** (1.546). It won **0 of 5** competitions and took 5 losses.
- `civ-therapist` — **lowest lifetime alignment in the whole fleet (1.168)** and the **lowest
  run average (1.251)**, with the **narrowest band** (1.143 – 1.373). It is also the only civ
  whose run avg sits more than 0.25 below the fleet mean of **1.648** (gap **-0.397**; the next lowest,
  `civ-whimsical` at 1.527, is only -0.121). 0 of 5 competition wins.
**`civ-therapist` is the clearest low-relevance signal**: lowest alignment and lowest run avg.
`civ-grounded` is lowest on relevance_per_sim and lifetime quality but is a close second, and the
two are effectively tied (relevance 2356.56 vs 2360.67).

**Low win rate is not the same as low relevance.** `civ-poetic` holds the **highest** relevance
(3318.54) and the **lowest** win rate (0.006) — selection and relevance are separate axes, and
the axis identity rotates. Report the axis, not the holder.

Neither civ is near the extinction threshold (`relevance < -10`); both relevance scores remain
strongly positive, so **no extinction or birth was triggered** (the script only runs
`extinction_and_birth` in `--loop` mode every 3 iterations, and this was a single batch).

## Run summary

- 8 civs x 5 sims = 40 sim rows, plus 5 competitions x 8 civs = 40 more = **80 new rows**.
- **`civ-precise` swept all 5 competitions** (the only civ with any wins, and W=5 vs W=0 for
  the field) — it also has the 2nd-highest relevance and the highest lifetime alignment (2.361).
