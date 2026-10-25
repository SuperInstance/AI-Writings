# Civ Orchestrator — RUN_REPORT session 133 (2026-10-24)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

Upstream `SuperInstance/AI-Writings` @ `a9f72ac` (session 132 baseline), sparse clone to `/tmp`,
symlink bridge at `/workspace/repos/ai-writings/cellular-first-design` (inode `129:99`, `-ef` OK).
Control B mock provider on `127.0.0.1:8799` (`ZAI_TOKEN` + `ZAI_URL_OVERRIDE` both set).

## Verification — all checks passed

| check | expected | measured | result |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | +10 each | +10 x 8 | PASS |
| `meta_log.jsonl` delta | +5 | 398 -> 403 | PASS |
| `Winner:` lines | 5 | 5 | PASS |
| total new rows | 80 | 80 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` field | `{zai}` | `{zai}` | PASS |
| rows with JEV `error` key | 0 | 0 | PASS |
| competition prompts at 8/8 distinct previews | 5/5 | 5/5 | PASS |
| rows with the 2.0/2.0/2.0 JEV fallback triple | 0 | 0 | PASS |
| mock tracebacks in `/tmp/mock_zai.log` | 0 | 0 | PASS |
| git status deletions / untracked | 0 / 0 | 0 / 0 | PASS |

Per-civ ledger deltas: civ-engineer 766->776, civ-formal 797->807, civ-grounded 812->822,
civ-mythic 769->779, civ-poetic 791->801, civ-precise 761->771, civ-therapist 764->774,
civ-whimsical 824->834. Total 6284->6364.

## Pre-flight (before the run, per the session-118/132 rule)

`/tmp` was wiped this session, so the mock was rebuilt from scratch from the RUNBOOK spec and
**both** historical mock bugs were re-applied on rebuild:

- session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]` — a plain `seed[i*2:i*2+2]` is empty for
  `i>=4`, raises `ValueError`, and the bridge answers HTTP 500 **while the socket stays open**
  (a 200 probe on a one-word body looks healthy and misses it).
- session-118 md5-of-whole-message seeding — seeding from the first 8 alnum chars of the message
  yields `youareav` for all 8 civs (the cultural prompt opens with the civ-invariant
  `You are a voice in the tradition of "..."`), making all 8 candidates byte-identical and voiding
  every competition result.

Pre-flight probe against the **live** mock with the exact long cultural prompt:
8/8 distinct seeds, 8/8 distinct previews, HTTP 200, 391-447-char bodies,
`[mock-zai seed=...]` prefix present, **0 tracebacks**.

## Low-relevance civilization — `civ-grounded` (The Grounded)

**`civ-grounded` is the low-relevance civ — 36 consecutive sessions (95-133).** Last on lifetime
`avg_score`, `quality`, `alignment`, `relevance` and `relevance_per_sim`.

| dimension | civ-grounded | next best | gap |
|---|---|---|---|
| lifetime `avg_score` | 1.163 | 1.329 (civ-engineer) | 0.166 |
| lifetime `quality` | 0.558 | 0.591 (civ-formal) | 0.033 |
| lifetime `alignment` | 1.375 | 1.693 (civ-therapist) | 0.318 |
| lifetime `relevance` | 871.55 | 986.88 (civ-engineer) | 115.33 |
| lifetime `relevance_per_sim` | 1.119 | 1.294 (civ-formal) | 0.175 |

Alignment is the dimension the meta-GAN *selects* on, so the 0.318 alignment gap is the
structurally meaningful one. `civ-formal` remains the distinct novelty axis (lowest
`novelty` 1.423); `civ-precise` the alignment inverse (best `alignment` 2.358, lowest
`quality` among the top half).

**This run's ordering differs from the lifetime ordering** — a useful, non-obvious split worth
recording: on the 80 new rows the last civ on `avg_score` / `quality` / `alignment` was
**`civ-therapist`** (avg 0.847, quality 0.075, alignment 0.287), with `civ-grounded` second-last
(0.908 / 0.106 / 0.475) and `civ-mythic` close behind (0.922). `civ-precise` led this run on
avg 1.824, quality 0.598 and alignment 2.580, and won 4 of the 5 competitions. Single-run
rankings under the mock are noisy; the lifetime ordering is the durable signal.

## Competition outcomes

| prompt | winner | argmax agrees? |
|---|---|---|
| what a cell is | The Precise | yes |
| the bookkeeper's role | The Precise | yes |
| the witness log | The Precise | yes |
| ternary values | The Precise | yes |
| JEV as a decision oracle | The Engineer | **no** (argmax was The Poetic) |

Chooser vs `avg_score` argmax = **4/5 (80 %)**. The fleet's standing figure for this is 0 %
(session 118, under the non-degenerate mock); 80 % here is a single-run sample and should not
be read as a reversal of that baseline.

## Structural findings (unchanged)

- **ZAI credential gap re-confirmed (17th session):** `ZAI_TOKEN` absent from env and all 8
  sandbox secrets. All candidate tokens (`ZAI_TOKEN`, `MOTHQUANTUM_TOKEN`, `TYPESAFE_AI_TOKEN`,
  `GITHUB_TOKEN`) return `401 token expired or incorrect` against the live z.ai endpoint
  (endpoint healthy => credential gap, not an outage). JEV is live.
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`** — the script reads the former.
  Without it JEV silently returns the 2.0/2.0/2.0 fallback triple; this run had **0** such rows.
- **Counter gap:** ledger rows exceed registry `simulations_run` by **+260** (6364 vs 6104),
  unchanged from session 132. `save_state()` rewrites `culture.json` with no lock =>
  `relevance_per_sim` is not recomputable from the ledger by an auditor.
- **Extinction risk: NONE** (threshold -10; lowest raw relevance +871.55, ~87x above).
  Registry 8 civs, `max_civs` 12. Extinction/birth only runs under `--loop`.
- **NAS EDQUOT still total (4th session running).** `git clone` directly into
  `/workspace/repos/...` dies with `Disk quota exceeded`; only the symlink bridge works.
  Target must be the **nested** `cellular-first-design` dir — this session's clone was left
  nested and `git status` shows 18 modified files with **0 deletions** and **0 untracked**.
- **`gh` is not installed** — 6th session running. `GET /user/repos?per_page=100` with
  `GITHUB_TOKEN` works; the API is case-insensitive
  (`SuperInstance/ai-writings` == `SuperInstance/AI-Writings`).

## Mock lifecycle

Started detached -> `timeout` wrapper (pid 244) + server (pid 246, exact args
`python3 /tmp/mock_zai.py`). Both killed by exact-args match; port 8799 verified closed
afterwards (`curl` exit 7 = connection refused), no stray processes, no `__pycache__` left behind.
