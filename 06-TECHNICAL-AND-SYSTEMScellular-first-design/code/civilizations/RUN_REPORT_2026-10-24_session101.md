# RUN_REPORT — 2026-10-24 — session 101

**Command requested:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Repo:** `SuperInstance/AI-Writings` @ `fc34a9db` (the path in the request names `ai-writings/`; the actual remote owner is `SuperInstance`, and the script's own hardcoded `CIVS_DIR` matches the requested path exactly)
**Session:** 101 · 115th wipe · credential gap **38th consecutive**

---

## 1. The command as asked produced ZERO new rows — and exited 0

`ZAI_TOKEN` is absent from the environment **and** from the 8-entry secret store
(`MOTHQUANTUM_TOKEN, TYPESAFE_AI_TOKEN, MINIMAX_KEY, NOTION_TOKEN, NPMJS_TOKEN,
CRATES_TOKEN, PYPI_TOKEN, GITHUB_TOKEN`). The z.ai coding endpoint was probed
directly with a sandbox secret:

```
POST https://api.z.ai/api/coding/paas/v4/chat/completions  ->  HTTP 401
{"error":{"code":"401","message":"token expired or incorrect"}}
```

Endpoint healthy ⇒ **credential gap, not an outage**. JEV probed separately:
**HTTP 200, model `jev-1.14.0`, real score 0.70, confidence 0.43** — the scorer
was live the whole time; only the provider was dark.

**Control A (command exactly as asked) — exit 0, and nothing happened:**

| metric | before | after | delta |
|---|---|---|---|
| ledger rows | 3724 | 3724 | **+0** |
| `meta_log.jsonl` | 238 | 238 | **+0** |
| `Winner:` lines | — | **0** | — |

The batch header and all 8 `[Name] running 5 sims...` lines printed, then the
competition header, then **no winners**. `call_provider()` returns `None` when
`ZAI_TOKEN` is unset, `run_simulation()` returns `None`, and the competition
short-circuits on `if not results: return None` — **silently, with exit code 0.**

> **Assert on the row delta and the `Winner:` count. Never on the exit code.**

## 2. Control B (mock-provider bridge) — the run that actually produces the ledger

`ZAI_URL_OVERRIDE` is **committed upstream** (no patch needed; the script stayed
byte-identical to the git blob). A local OpenAI-shaped mock on `127.0.0.1:8799`
served per-voice body pools with the s97 marker-front rule
(`content = "[mock-zai <salt>] " + body`).

| metric | before | after | delta |
|---|---|---|---|
| ledger rows | 3724 | 3804 | **+80** |
| per-civ | — | — | **+10 each, uniform 8/8** |
| `meta_log.jsonl` | 238 | 243 | **+5** |
| `Winner:` lines | 0 | **5** | — |
| provider field | — | `zai` on 80/80 | — |
| mock-marked | — | **80/80** | — |
| distinct `content_preview` | — | **80/80** | — |
| all-2.0-default rows (JEV fallback) | — | **0** | — |
| rows with score error | — | **0** | — |
| fleet mean `avg_score` | — | **1.910** (min 0.823, max 2.987) | — |

Mock call log: **81 requests = 80 sims + 1 pre-flight probe.** Mock stopped
cleanly by PID (not by `pkill -f`, which self-matches).

## 3. LOW RELEVANCE — `civ-grounded` is the low-relevance civilization

| lens | last | value | 2nd lowest | gap |
|---|---|---|---|---|
| lifetime `avg_score` (n=2604 clean) | **civ-grounded** | 1.614 | civ-formal | 0.126 |
| lifetime `alignment` | **civ-grounded** | 2.105 | civ-mythic | **0.535** |
| lifetime `novelty` | **civ-formal** | 1.401 | civ-precise | 0.207 |
| lifetime `quality` | **civ-formal** | 1.045 | civ-grounded | 0.005 |
| this-run `avg_score` (n=10/civ) | **civ-grounded** | 1.407 | civ-engineer | 0.159 |
| this-run `alignment` | **civ-grounded** | 1.801 | civ-engineer | **0.610** |
| board `relevance_per_sim` | **civ-grounded** | 1.466 | civ-formal | 0.177 |
| board raw relevance | **civ-grounded** | 672.82 | civ-formal | 58.12 |
| board `win_rate` (selection) | **civ-poetic** | 0.009 | civ-whimsical | 0.009 |

**`civ-grounded` (The Grounded) is last on 6 of 9 lenses** — **7th consecutive
session** with the Grounded last on the committed lifetime lenses (s94–s100).

Its deficit is specifically **`alignment`** (lifetime 2.105, gap 0.535 to the
next-worst; this run 1.801, gap 0.610) — and alignment is the dimension the
meta-GAN *selects* on, so this is structural, not a ranking artefact. The
longevity-artefact defence stays falsified: the Grounded has **352 clean rows,
2nd most of 8** (whimsical 364), so a lifetime-average denominator should
*penalise* it relative to the middle — yet it is last on the
denominator-least-biased lens.

**`civ-formal` is a different axis**, not a second "lowest civ": lowest clean
lifetime `novelty` (1.401) and 2nd-bottom on every lens the Grounded is not —
a *flattest-prose* deficiency versus the Grounded's *alignment* deficiency.
**Name the axis; do not merge them.**

**`civ-poetic` remains the stable inverse** — 1st on board `relevance_per_sim`
(2.139), 1st on raw relevance (949.74), 1st on lifetime `avg_score`, yet last on
`win_rate` (0.009, 2W/216L). The chooser picked it **3 times in 243 rounds**
while it was argmax **101**. A *selection* failure, not a quality collapse.
Stable across 17 sessions. **`civ-precise` is the other inverse** — best
`win_rate` (0.46, 98W/115L) but last on lifetime `quality` (1.045).

**This run's bottom agrees with the lifetime bottom** (`civ-grounded` on both),
which is the condition under which the this-run lens may be reported as *the*
low-relevance civ rather than unranked.

**Extinction risk: NONE** (threshold −10; lowest raw relevance +672.82;
`--loop`-mode only). Registry 8 civs, `max_civs` 12.

## 4. Chooser vs argmax — 15.6 % (26th consecutive replication)

On the committed `meta_log.jsonl` (**243 rounds**): chooser agrees with the
`avg_score` argmax **38 times = 15.6 %**.
Chooser picks: precise 99, grounded 60, formal 40, engineer 24, whimsical 7,
therapist 6, mythic 4, poetic 3.
Argmax picks: poetic 101, whimsical 58, precise 32, therapist 20, mythic 19,
engineer 4, formal 6, grounded 3.
**All 5 rounds of this run disagreed.** "Prefer win rate" remains unsafe as a
standalone rule — `win_rate` is a *selection* metric, not a quality metric.

## 5. Committed-ledger state

- 3804 ledger rows; **80 mock-sourced from this run**; 2604 clean (non-mock)
  lifetime rows across 8 civs.
- **Counter gap: 3804 ledger rows vs 3464 registry `simulations_run` = +340
  uncounted.** `save_state()` rewrites `culture.json` with no lock ⇒
  `relevance_per_sim` is **not recomputable from the ledger** by an auditor.
- Script **pristine** vs the git blob (`git diff --quiet` clean) —
  `ZAI_URL_OVERRIDE` is upstream, no patch needed.
- Only data files modified (17 `culture.json` / `simulations.jsonl` +
  `leaderboard.json` + `meta_log.jsonl`); no `__pycache__`.

## 6. Environment notes

- **The workspace NAS is 100 % full (0 bytes available).** `git clone` into
  `/workspace/repos/...` dies with `Disk quota exceeded` on
  `.git/description`. A 5 MB `dd` into `/workspace` lands **0 bytes** and still
  appears in `ls` — the trap again. `mkdir` under `/workspace` still works, so
  the **symlink bridge** is the way: `ln -sfn /tmp/work/AI-Writings
  /workspace/repos/ai-writings`, verified by **inode identity**
  (`stat -L -c '%d:%i'` → `129:10406` on both sides) and by `-ef`.
- Clone to the **overlay** (`/tmp/work`, 28 G free), not the NAS.
- `write` tool remains jailed to the workspace root; `/tmp` artifacts via bash
  heredoc.
- Run the orchestrator **detached** (`setsid nohup timeout -s KILL 300 … &`) and
  poll the output file — a 30 s tool timeout kills a ~29 s run mid-flight and
  the report then records a run whose results were never captured.
- Kill the mock **by PID from `ps`**, never `pkill -f mock_zai` (self-match).
- `TYPESAFEAI_KEY` (script) vs `TYPESAFE_AI_TOKEN` (sandbox) — always
  `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"`, or JEV silently degrades to the
  2.0 default and every score becomes a constant.
