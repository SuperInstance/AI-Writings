# Civ Orchestrator — Run Report (session 130)

**Date:** 2026-10-24 20:44Z
**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Provider path:** Control B mock bridge (`ZAI_TOKEN` placeholder + `ZAI_URL_OVERRIDE` → `http://127.0.0.1:8799/...`)
— `ZAI_TOKEN` is absent from this sandbox's env and all 8 secrets, and the real z.ai endpoint
returns `401 token expired or incorrect` against a bogus bearer (endpoint healthy ⇒ credential gap,
not an outage). **JEV was live**: `POST /v1/systemone` with a malformed `questions` returned
`422 {"type":"dict_type"}` — a payload-shape complaint, i.e. the token was accepted.
**Runner:** 8 civs × 5 sims + 5 competition prompts.

## Verification — all checks PASS

| Check | Expected | Observed | Verdict |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each (5 sim-phase + 5 competition-phase) | +10 × 8 | PASS |
| total new ledger rows | 80 | 80 | PASS |
| `meta_log.jsonl` Δ | +5 | 383 → 388 | PASS |
| `Winner:` lines in stdout | 5 | 5 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` value | `{zai}` only | `{zai}` only | PASS |
| rows with a JEV `error` key | 0 | 0 | PASS |
| sim→competition ts gap at index 4 | present in all 8 | 1.10 s – 23.21 s | PASS |
| mock non-degeneracy (8/8 distinct previews AND seeds per competition prompt) | 5/5 prompts | **5/5** | PASS |
| extinction risk (threshold −10) | NONE | lowest relevance +854.32 (85× above floor) | PASS |

**Mock non-degeneracy is the 11th consecutive clean measurement** (118, 120–130). The pre-flight
probe was run against the *live* mock with the exact long cultural prompt before the batch:
8 civs → 8 distinct seeds, 8 distinct previews, 204-char bodies, `[mock-zai seed=…]` prefix on
every body, **0 tracebacks** in `/tmp/mock_zai.log`. Both historical mock bugs were re-applied on
rebuild (session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]`; session-118 md5-of-whole-message
seeding) — without either, the bridge 500s on `i>=4` or makes all 8 civs emit identical text and
voids every competition result.

## Score dimensions

| civ | lifetime avg | lifetime align | lifetime qual | lifetime novelty | run avg | run align |
|---|---|---|---|---|---|---|
| civ-poetic | **1.7753** | 2.3318 | **0.9875** | 2.0066 | 0.2670 | 0.0890 |
| civ-whimsical | 1.6469 | 2.0584 | 0.8056 | **2.0767** | 0.2373 | 0.0650 |
| civ-precise | 1.5403 | **2.3884** | 0.6710 | 1.5615 | **0.7823** | **1.3350** |
| civ-mythic | 1.4973 | 1.8913 | 0.7287 | 1.8720 | 0.2620 | 0.0200 |
| civ-therapist | 1.4211 | 1.7509 | 0.6552 | 1.8572 | 0.1960 | 0.0120 |
| civ-formal | 1.3538 | 2.0289 | 0.6084 | **1.4240** | 0.3307 | 0.2790 |
| civ-engineer | 1.3537 | 1.9062 | 0.6258 | 1.5290 | 0.2577 | 0.2070 |
| **civ-grounded** | **1.1852** | **1.4167** | **0.5772** | 1.5616 | **0.1203** | 0.0290 |

**Cross-civ spreads (not absolute levels).** `alignment` carried the widest spread again —
lifetime 0.9717, this run 1.3230 — versus `avg_score` 0.6620, `novelty` 0.6570, and `quality`
**0.0230** (run min 0.0090 / max 0.0320). The `quality` axis was again effectively **flat**
this run, in the 119/121/122/123/125/126 regime (spread 0.004–0.337) and against session-127's
1.063 and session-120's 0.340. Re-confirms the durable rule: **the quality collapse is a LEVEL
that moves, not a stable property** — compare cross-civ spreads, not absolute levels, before
ranking on a dimension.

**Absolute score levels this run are depressed vs lifetime** (run `avg_score` 0.120–0.782 vs
lifetime 1.19–1.78). A level shift in the JEV scorer's output for this batch, **not a civ effect** —
the cross-civ *ordering* carries the information.

## Chooser vs `avg_score` argmax: 4/5 (80 %)

`civ-precise` was argmax in 5/5 and won 4/5. The single disagreement: p3 "witness log" —
`civ-formal` won at 0.463 against `civ-precise`'s argmax 1.243, i.e. the chooser again picked a
**lower**-scoring candidate. Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) →
4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125) → 1/5 (126) → 3/5 (127) → 2/5 (128) → **4/5 (130)**.
Thirteen five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*.
What survives every session: the chooser is **not** a pure argmax, and every observed disagreement
goes the same way (chooser picks a lower-scoring candidate) — 10th consecutive session with that
direction. **Never treat `win_rate` as a quality metric.**

## Low-relevance civilization

**`civ-grounded` (The Grounded) remains the low-relevance civ — 34 consecutive sessions (95–130).**
Last on lifetime `avg_score` (1.1852), `alignment` (1.4167), `quality` (0.5772), `relevance`
(854.32) and `relevance_per_sim` (1.141). The **structural gap is `alignment`: 0.3342 below the
next civ** (therapist 1.7509), **versus 0.0280 on quality** — ~12× wider. Alignment is the
dimension the meta-GAN *selects* on, so Grounded fails to **embody a distinctive voice** — a voice
failure, not a prose failure. It was **also the run-level low** on `avg_score` (0.1203), the 4th
consecutive session where the run-level label went to it (127 → whimsical, 128 → grounded,
129 → grounded, 130 → grounded).

**Second axis, unchanged: `civ-formal` is the low-novelty civ** (lifetime novelty **1.4240**,
last; alignment 2.0289 healthy).

**Two stable inverses, both re-confirmed:**
- `civ-poetic` = 1st on lifetime `avg_score` (1.7753) / `quality` (0.9875) / `novelty` (2.0066) /
  `alignment` (2.3318), but **last on `win_rate` (0.014, 5/358)** and won **0/5** this run
  (rank 6th of 8 on run `avg_score`) — the selection-failure inverse.
- `civ-precise` = best `win_rate` (0.534, 191/167), won **4/5**, **1st on lifetime `alignment`
  (2.3884)**, and 1st on this run's `avg_score` (0.7823) — the mirror inverse.

**Watch-axis `civ-engineer` — session-121's low did NOT repeat for a 4th time.** 4th of 8 on this
run's `avg_score` (0.2577), 3rd on `alignment` (0.2070), 7th of 8 on lifetime `relevance_per_sim`
(1.334). **Do not promote it to a finding.**

**Watch-axis `civ-therapist` — 2nd-lowest on this run's `avg_score` (0.1960) and LAST on run
`alignment` (0.0120, below Grounded's 0.0290).** Lifetime alignment 1.7509 is mid-field, so this
is a single-run low, not a second axis yet. Watch it.

**New run-level note — `civ-mythic` was 2nd-lowest on run `alignment` (0.0200)** and 5th of 8 on
run `avg_score` (0.2620); lifetime is mid-field (alignment 1.8913). Run-level signal only.

## Lifecycle

- **Extinction risk NONE** — threshold −10, lowest relevance +854.32 (85× above the floor).
  Registry 8 civs, `max_civs` 12. All 8 still `generation=1`; birth/extinction only run under
  `--loop`.
- **Counter gap per-civ uneven, unchanged**: whimsical +63, grounded +43, formal +42, poetic +37,
  engineer +22, mythic +20, therapist +17, precise +16 (total +260). `save_state()` has no lock
  ⇒ `relevance_per_sim` is **not recomputable from the ledger** by an auditor.

## Re-confirmations

- **NAS EDQUOT total (13th session)** — `git clone` into `/workspace/repos/...` dies with
  `Disk quota exceeded` on `.git/description`; only the symlink bridge works.
- **`gh` not installed (16th session)** — used `GET /search/repositories?q=ai-writings` with
  `GITHUB_TOKEN`; the 3.7 GB upstream is `SuperInstance/AI-Writings` (API is case-insensitive).
- **Tool timeout 30 s < run ~50 s** — launched detached with stdout redirected to a file, polled
  with `ps`; the run completed in ~27 s of polling.
- **`ZAI_URL_OVERRIDE` alone is dead code** — the token gate in `call_provider()` returns `None`
  first. Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.
- **`TYPESAFEAI_KEY` must be exported** (the script reads it; the sandbox stores `TYPESAFE_AI_TOKEN`).
- Clone into `/tmp`, symlink the **nested** `cellular-first-design` dir, verify with
  `stat -L -c '%d:%i'` (got `129:12604`) + `-ef`; never flatten.
- The `ls` race on the symlinked deep path did **not** reproduce (bridge passed 5/5 on the first
  attempt).
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict) — a dict-shaped
  reader silently yields 0 % agreement and empty pick tallies.
- **Grouping this run's rows by `r["prompt"]` is wrong** for the non-degeneracy check (`prompt` is
  truncated to 80 chars and the sim phase reuses the same 5 canon prompts ⇒ 16 rows per prompt).
  Group by the **per-civ slot index** (`rows[-10:][5..9]` for the competition phase).
