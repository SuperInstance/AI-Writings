# Civilization Orchestrator — Run Report (Session 16)

**Date:** 2026-10-23
**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Baseline commit:** `cdc2aae7` (bot auto-update; civ subtree identical to `e532e66`)
**Baseline ledger:** 684 rows across 8 civs, 48 `meta_log.jsonl` entries
**Registry `simulations_run` sum:** 424 → **counter gap +260** (measured blob-to-blob)

---

## 1. The literal command is a green no-op — 14th consecutive session

The task path did not exist at session start (`/workspace` held only `.plugin-cache` and
`.skills`). Rebuilt from `SuperInstance/AI-Writings` (the prompt's `ai-writings/...` owner
segment is a legacy name — that path 404s).

| check | result |
|---|---|
| `ZAI_TOKEN` / `ZAI_KEY` in env | **ABSENT** (and absent from the 8-entry secret store) |
| all 7 candidate secrets → z.ai coding endpoint | **HTTP 401 "token expired or incorrect"** on every one ⇒ endpoint healthy, **credential gap** |
| `groq` endpoint | HTTP 403/401 ⇒ **no alternate live provider** |
| JEV `https://api.typesafe.ai/v1/systemone` | **LIVE** — `jev-1.14.0`, `quality.score 0.3, confidence 0.73` |

**Unpatched run, measured not assumed:** batch header + all 8 `[Name] running 5 sims...`
lines, then an **empty competition section**, then **exit 0**. Ledger delta **+0 rows,
+0 `meta_log`** (684 → 684, 48 → 48). **0 `Winner:` lines.** Only `leaderboard.json` was
rewritten — and that file is rewritten on *every* run, including the no-op one, so its
mtime tells you nothing about whether work happened.

> **Assert on the row delta and the `Winner:` count. Never on the exit code.**

## 2. Control B — the run that actually produces evidence

One-line `ZAI_URL_OVERRIDE` patch (verified **1 line** changed against the git blob) +
a local mock standing in for the z.ai endpoint. The mock keys off the civ **name** in the
header, extracts the `Your voice:` line specifically, applies the salt to the **seed
only**, and logs its raw inputs.

| acceptance check | result |
|---|---|
| ledger rows, set A | **+80** (10 per civ, uniform) — 684 → 764 |
| ledger rows, set B | **+80** (10 per civ, uniform) — 764 → 844 |
| `meta_log.jsonl` | **+5** per set (48 → 53 → 58) |
| `Winner:` lines | **5** per set |
| mock call log | 80 calls per set, **10 per civ each**, `auth_present` true on all |
| salt leaked into the prompt | **false** on all 160 calls |
| all-2.0-default (JEV fallback) rows | **0** |
| score errors | **0** |
| scaffolding leak (`Your tenets` / `Your voice` in preview) | **0** / **0** |
| distinct `content_preview` | **79/80** |
| distinct `avg_score` | 71 |
| distinct `temperature` | 77 (the ±0.2 per-call jitter is live) |
| JEV score range | `avg_score` 0.800 – 2.147 |

## 3. A/B: the mock's prose is a first-order confounder, measured

| | set A | set B |
|---|---|---|
| fleet mean `avg_score` | 1.4800 | 1.4804 (**+0.0003**) |
| **max per-civ \|delta\|** | — | **0.117** |
| positional rank agreement | — | **4/8** |
| **Kendall τ** | — | **0.857** (26 conc / 2 disc) |
| top-3 **set** | {Poetic, Whimsical, Precise} | {Poetic, Whimsical, Precise} |
| bottom-2 **set** | {Grounded, Therapist} | {Grounded, Therapist} |

The perturbation (max 0.117) is **smaller than the adjacent rank gaps it would have to
overturn** (set A gaps 0.056 / 0.025 / 0.184 / 0.071 / 0.090 / 0.221 / 0.046), so this
swap preserved the order — the "tie-preserving" end of the perturbation axis. The two
crossings (Mythic↔Formal, Therapist↔Grounded) are both inside noise.

**Competition winners are still the least stable quantity:** set A → Precise ×3, Grounded,
Formal; set B → Precise ×2, Engineer ×2, Formal. **No civ won in both sets.**

## 4. Low-relevance reading — baseline-only (684 committed rows, mock rows excluded)

| lens | lowest | value |
|---|---|---|
| `relevance_per_sim` (board sort key) | **civ-grounded** | 1.785 |
| raw relevance | **civ-engineer** | 118.27 (youngest civ, not weakest) |
| `win_rate` (the genuine competitive signal) | **civ-poetic** | **0.000 (0W/33L)** |
| lifetime `avg_score` | **civ-grounded** | 1.965 |
| lifetime `quality` | civ-engineer | 1.765 |
| lifetime `novelty` | civ-precise | 0.955 |
| lifetime `alignment` | **civ-grounded** | 2.747 |

**`civ-grounded` is the stable low-relevance answer** — last on `relevance_per_sim`,
lifetime `avg_score` *and* lifetime `alignment`, and bottom-2 in **both** body sets and
in the pool across prior sessions. It is a genuine quality signal, not the longevity
artefact that the `relevance_per_sim` denominator alone suggests (it ran the most sims).

**`civ-poetic` is the inverse case** — top-2 in both body sets, 2nd of 8 on lifetime
`avg_score` (2.649), 1st on quality (2.315), 2nd on alignment (3.343) — and **0 wins in
33**. A *selection* failure, not a quality collapse. Stable across 14 sessions.
**`civ-precise` is the other inverse** — best win rate of the fleet (0.643, 18W/10L) but
6th on `avg_score` and last on novelty (0.955).

**Extinction risk: none.** `extinction_and_birth()` retires only below relevance −10;
the lowest is +118.27, and it only runs in `--loop` mode every third iteration.

## 5. Structural replications

- **Chooser vs `argmax(avg_score)`: 15.5 % (9/58) lifetime, 0/10 this session** — 10th
  replication. Disagreement margins ran to **1.113** (the chooser crowned a civ 1.113
  *below* the top scorer).
- **Temperature vs lifetime JEV novelty: Pearson r = 0.9722** (s8 0.985, s10 0.981,
  s13 0.9845, s14 0.9790, s15 0.9783) — 8th replication. The fleet is 8 points on one
  temperature/novelty gradient.
- **Counter gap unchanged at +260** (684 ledger vs 424 registry), measured blob-to-blob.

## 6. Restore

`git checkout -- <subtree>` + `rm -rf __pycache__`. **All 52 files verified byte-identical**
to the git blobs with `cmp` against `git show HEAD:<path>`. `git status` clean. Ledger
back to 684, `meta_log` back to 48, `ZAI_URL_OVERRIDE` patch reverted (0 occurrences).
