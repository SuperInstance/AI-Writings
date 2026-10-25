# Civilization Orchestrator — Run Report (Session 100b, 2026-10-24)

**Concurrent instance.** Session 100 was already filed on `main` by another
agent (commit `02526f97` -> `fc34a9db`). This is a **second, independent
session 100**; its report is `RUN_REPORT_2026-10-24_session100.md` and it is
**not** superseded by this one. The two measured the same fleet on the same
day with different mock body sets and **independently agree on the
low-relevance answer** (see §5).

**Command asked for**
```bash
python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py \
  --sims 5 --prompts 5 --providers zai
```

**Result of the exact command: a green exit and an empty ledger.**
Exit code **0**. Batch header + all 8 `[Name] running 5 sims...` lines printed.
Competition header printed. **Zero `Winner:` lines.**
Ledger delta **+0 rows** (3724 -> 3724). `meta_log.jsonl` delta **+0** (238 -> 238).
Only `leaderboard.json` was rewritten.

37th consecutive session with this outcome. The cause is a **credential gap,
not an outage**. Exit code is not a valid success signal for this script;
assert on the row delta and on the presence of `Winner:` lines.

---

## 1. Environment reconstruction

The task path did not exist at session start (`/workspace` held only
`.plugin-cache` and `.skills`); `/workspace/repos` did not exist.

| Step | Result |
|---|---|
| `git clone` into `/workspace` | **FAILED** — `close error: Disk quota exceeded` (NAS 100 %, 600 G used, 0 avail) — and it still printed `Cloning into…` and **exited 0** |
| `git clone --depth 1` into `/tmp` | worked, but the 3.7 GB pack exceeded the 30 s tool timeout; the working tree was **removed mid-checkout**, leaving `.git` with *no commits* and a 2.3 GB tree |
| Shape that fit | `git clone --depth 1 --filter=blob:none --no-checkout` -> `git sparse-checkout set cellular-first-design/code/civilizations` -> `git checkout` |
| Bridge | `rm -rf /workspace/repos/ai-writings` **first**, then `ln -sfn /tmp/aw /workspace/repos/ai-writings` |
| Bridge verified by | **inode identity** — `stat -c '%d:%i'` = `129:219` on both sides |

`CIVS_DIR` is hardcoded to
`/workspace/repos/ai-writings/cellular-first-design/code/civilizations`, so the
symlink is what makes the script write into the clone.

**Repo identity — the task path is NOT a repo.** It is a subtree of
`SuperInstance/AI-Writings`. `git ls-remote` on `ai-writings/cellular-first-design`,
`autoclaw/…`, `purplepincher/…`, `SuperInstance/cellular-first-design` all
return `Repository not found`. **GitHub code search finds it in one call:**
`GET /search/code?q=civilization_orchestrator+in:path` -> exactly **1 hit**,
`SuperInstance/AI-Writings`. The `in:path` qualifier is what makes it a path
search; repo-name guessing across 4 candidate orgs cost ~8 tool calls.

## 2. Credential audit

| Endpoint | Probe | Result |
|---|---|---|
| z.ai coding (`api.z.ai/api/coding/paas/v4/chat/completions`) | POST with a live sandbox secret | **HTTP 401 `token expired or incorrect`** |
| JEV (`api.typesafe.ai/v1/systemone`) | POST scoring request | **HTTP 200, `jev-1.14.0`**, real score 0.79 / conf 0.35 |

`ZAI_TOKEN` / `ZAI_KEY` absent from env **and** from the 8-entry secret store.
A 401 (not 5xx) means the endpoint is healthy => the scorer was live the whole
time and only the provider was dark. Always:
`export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"`.

## 3. Control A — the command exactly as asked

```
BEFORE rows=3724 meta=238
exit:0
AFTER  rows=3724 meta=238
DELTA rows=0 meta=0
Winner lines: 0
```

## 4. Control B — provider redirected to a local mock, JEV left live

`ZAI_URL_OVERRIDE=http://127.0.0.1:8099/` with `ZAI_TOKEN` set. The override
is **committed upstream**, so the orchestrator file stayed byte-identical to
the git blob — no patch was applied.

```
DELTA rows=80 meta=5
Winner lines: 5
```

### Acceptance checks (all pass)

| Check | Result |
|---|---|
| Row delta | **+80** (10 per civ: 5 batch + 5 competition) — uniform 8/8 |
| `meta_log.jsonl` | **+5** entries, 5 winners |
| Mock-marked rows | **80 / 80** (marker-front) |
| `provider: zai` | **80 / 80** |
| All-2.0-default rows (JEV outage default) | **0** |
| Score errors | **0** |
| Distinct `content_preview` | **80 / 80** (a collapsed count is the tell) |
| Distinct `avg_score` | 76 values, range 1.29 – 2.77 |
| Mock `fallback` flag | **0 of 81 calls** — all 8 fleet voices resolved to a per-voice body |

19th replication of the +80 / +5 / 5-winner shape.

### This run's winners
`civ-formal` x4, `civ-grounded` x1 (the other session-100 instance's set A
got `formal x2 / poetic / precise / engineer`; its set B got
`precise x3 / engineer / formal` — so the **chooser's picks are not stable
across body sets either**, which is consistent with the 15.6 % chooser/argmax
agreement below).

## 5. Low relevance — four lenses, four answers

### A. Board lenses (`leaderboard.json`)

| civ | relevance | relevance_per_sim | W–L | win_rate | sims_run |
|---|---|---|---|---|---|
| civ-poetic | 949.21 | **2.138** | 2–216 | **0.009** | 444 |
| civ-whimsical | 888.33 | 1.970 | 4–214 | 0.018 | 451 |
| civ-mythic | 837.75 | 1.908 | 4–208 | 0.019 | 439 |
| civ-therapist | 819.72 | 1.876 | 6–209 | 0.028 | 437 |
| civ-precise | 783.03 | 1.800 | 98–115 | **0.460** | 435 |
| civ-engineer | 749.88 | 1.728 | 22–189 | 0.104 | 434 |
| civ-formal | 734.20 | 1.650 | 39–177 | 0.181 | 445 |
| civ-grounded | 679.72 | **1.481** | 49–168 | 0.226 | 459 |

- lowest `relevance_per_sim` -> **civ-grounded 1.481** (2nd: civ-formal 1.650)
- lowest raw relevance -> **civ-grounded 679.72** (2nd: civ-formal 734.20)
- lowest `win_rate` -> **civ-poetic 0.009** (2nd: civ-whimsical 0.018)

### B. Clean lifetime lenses — real z.ai rows only, mock rows excluded (n = 2444)

| lens | lowest | value | 2nd lowest | gap |
|---|---|---|---|---|
| `avg_score` | **civ-grounded** | 1.668 | civ-formal 1.785 | 0.117 |
| `quality` | **civ-precise** | 1.093 | civ-formal 1.103 | 0.010 |
| `novelty` | **civ-formal** | 1.423 | civ-precise 1.592 | 0.169 |
| `alignment` | **civ-grounded** | 2.204 | civ-mythic 2.673 | **0.469** |

### C. This run (80 mock rows) — NOT the stable reading

`avg_score` lowest: **civ-precise 1.564**; `quality` lowest: civ-precise 0.284;
`novelty` lowest: civ-formal 1.665; `alignment` lowest: civ-precise 2.419.
Top on `avg_score`: civ-poetic 2.559.

The this-run bottom has moved across sessions (s96 grounded/formal, s97
formal/formal, s98 mythic, s99 mythic, s100-A precise). **Report the lifetime
reading; never the this-run bottom.** Note the divergence from the other
session-100 instance, whose set B put `civ-grounded` last on this-run
`avg_score` (1.563) — the two independent body sets disagree on the *this-run*
bottom while agreeing on the *lifetime* bottom.

### D. The answer, lens by lens

- **`civ-grounded` is the genuinely low-relevance civilization.** Last on the
  board's sort key (1.481), last on raw relevance (679.72), last on clean
  lifetime `avg_score` (1.668), and last on clean lifetime `alignment` (2.204).
  The **alignment deficit of 0.469 is the largest separation of any lens**,
  and alignment is the dimension the meta-GAN selects on => structural, not a
  ranking artefact. The longevity defence is **dead again**: the Grounded has
  332 clean rows, 2nd most of 8 (whimsical 344) — it did not merely run longest.
- **`civ-formal` is a different, axis-specific weakness** — lowest clean
  lifetime `novelty` (1.423). That is flat prose, not low alignment. Name the
  axis; do not merge the two into one "lowest civ".
- **`civ-poetic` is the inverse case** — 1st on clean lifetime `avg_score`
  (2.270), 1st on the board's `relevance_per_sim` (2.138), 1st on clean
  lifetime `alignment` (2.955), yet **last on `win_rate` (0.009, 2W/216L)**.
  A *selection* failure, not a quality collapse. Stable for 15+ sessions.
- **`civ-precise` is the other inverse** — best win rate (0.460) but last on
  clean lifetime `quality` (1.093) and 2nd-lowest on novelty (1.592).
- **Extinction risk: NONE.** Threshold `relevance < -10`; lowest is +679.72,
  and `extinction_and_birth()` only runs in `--loop` mode every third
  iteration. A single-shot run never triggers it.

### Cross-instance agreement (two independent session-100 body sets)

| lens | this instance | other session-100 | agree? |
|---|---|---|---|
| board `relevance_per_sim` last | civ-grounded 1.481 | civ-grounded 1.469 | **yes** |
| board raw relevance last | civ-grounded 679.72 | civ-grounded 674.37 | **yes** |
| board `win_rate` last | civ-poetic 0.009 | civ-poetic 0.009 | **yes** |
| clean lifetime `avg_score` last | civ-grounded 1.668 | civ-grounded 1.678 | **yes** |
| clean lifetime `alignment` last | civ-grounded 2.204 | civ-grounded 2.221 | **yes** |
| clean lifetime `novelty` last | civ-formal 1.423 | civ-formal 1.414 | **yes** |
| clean lifetime `quality` last | civ-precise 1.093 | civ-precise 1.104 | **yes** |
| this-run `avg_score` last | **civ-precise 1.564** | **civ-grounded 1.563** | **NO** |

**The lifetime bottom replicates across two independently-written body sets;
the this-run bottom does not.** That is the cleanest statement of the rule:
**report the lifetime lens.**

## 6. Chooser vs argmax — 25th consecutive replication

On the committed `meta_log.jsonl` (243 rounds) the chooser agrees with the
`avg_score` argmax **38 times = 15.6 %** (s7 4.4 %, s8 18.9 %, s99 15.6 %).

- chooser picks: precise 99, grounded 59, formal 42, engineer 23, whimsical 7,
  therapist 6, mythic 4, **poetic 3**
- argmax picks: **poetic 101**, whimsical 58, precise 32, therapist 21,
  mythic 18, formal 6, engineer 4, grounded 3

**All 5 rounds of this run disagreed.** A competition win is not evidence of
a higher JEV score; "prefer win rate" remains unsafe as a standalone rule.

## 7. Counter gap — unchanged at exactly +260

Ledger rows **3804** vs registry `simulations_run` **3544** -> gap **+260**:
whimsical +63, grounded +43, formal +42, poetic +37, engineer +22, mythic +20,
therapist +17, precise +16. `save_state()` rewrites `culture.json` from
in-memory counters with no lock and no read-modify-write => lost-update race.
**`relevance_per_sim` is not recomputable from the ledger**; the board order
cannot be audited from the committed rows.

## 8. Temperature vs novelty

Pearson **r = 0.938** on clean rows (s8 0.985, s9 0.980) — replicated again.
The fleet is 8 points on one temperature/novelty gradient with a style overlay,
not 8 independent voices.

| temp | civ | clean novelty | clean avg_score | clean alignment |
|---|---|---|---|---|
| 0.20 | civ-precise | 1.592 | 1.867 | 2.918 |
| 0.30 | civ-formal | **1.423** | 1.785 | 2.828 |
| 0.40 | civ-engineer | 1.622 | 1.802 | 2.678 |
| 0.50 | civ-grounded | 1.693 | **1.668** | **2.204** |
| 0.60 | civ-therapist | 2.145 | 2.020 | 2.685 |
| 0.80 | civ-poetic | 2.291 | **2.270** | 2.955 |
| 0.85 | civ-mythic | 2.178 | 2.040 | 2.673 |
| 0.95 | civ-whimsical | **2.415** | 2.195 | 2.771 |

**The Grounded (temp 0.50) is the only civ whose `alignment` falls off the
gradient** — every other civ's alignment rises with temperature. Its deficit
is therefore **cultural, not thermal**. That is the sharpest single argument
in this fleet's data for *why* the meta-GAN keeps passing over it.

## 9. NEW — a prompt-set sensitivity split: a free stability check

This run's 10 rows per civ are two prompt sets (5 batch + 5 competition), so
the batch-half vs competition-half `avg_score` shift measures **prompt
sensitivity without a second run**:

| civ | batch | comp | delta |
|---|---|---|---|
| civ-engineer | 2.091 | 1.754 | **-0.337** |
| civ-grounded | 2.237 | 1.958 | -0.279 |
| civ-whimsical | 2.442 | 2.230 | -0.212 |
| civ-formal | 1.981 | 1.919 | -0.061 |
| civ-therapist | 2.103 | 2.041 | -0.062 |
| civ-precise | 1.483 | 1.645 | +0.161 |
| civ-mythic | 2.287 | 2.341 | +0.053 |
| civ-poetic | 2.557 | 2.561 | +0.004 |

**The Engineer's swing (-0.337) is larger than the gap between adjacent civs
on the board** — so an absolute score difference of that size is not evidence
of a quality difference. Poetic and Mythic are the two prompt-stable civs.
This is the cheapest available companion to the "re-run with a second body
set" rule and it costs nothing.

## 10. A glob-order artifact that nearly became a finding

`rows[-80:]` over `glob.glob('civ-*/simulations.jsonl')` returned
`civ-whimsical 80/80` and "uniform: True" — because the glob returns files in
directory order, so the last 80 rows are **all one civ**. Counting per file
(`open(f).read().splitlines()[-10:]` for each civ) gives the real histogram:
**8 x 10**. **A glob-order artifact looked like a single-civ anomaly and
nearly became a headline finding.**

## 11. State at session close

- 8 civs, **3724 committed ledger rows** (restored), `meta_log.jsonl` **238**
  lines, `leaderboard.json` restored.
- **Restore + verify:** `git checkout -- cellular-first-design/code/civilizations/`,
  then `cmp` each tracked file against `git show HEAD:<path>` ->
  **143/143 byte-identical, 0 differing**; `git status --short` **empty**; no
  `__pycache__`.
- **Mock rows were not committed** — a mock row presented as a provider result
  poisons the fleet's only durable quality record.
- The orchestrator script was **not modified**; `ZAI_URL_OVERRIDE` is upstream.
- Committed-ledger synthetic fraction: **1362 / 3724 = 36.6 %** by a
  marker-prefix scan, 2444 clean. (The other session-100 instance reports
  38.7 % under a two-family scan — the two scans disagree because the marker
  families differ; the *clean* count 2364 vs 2444 differs because its
  12 extra "clean" rows carry a `[The …]` bracket that its scan classifies as
  synthetic. **There is no single agreed synthetic fraction; state the scan
  you used.**)
