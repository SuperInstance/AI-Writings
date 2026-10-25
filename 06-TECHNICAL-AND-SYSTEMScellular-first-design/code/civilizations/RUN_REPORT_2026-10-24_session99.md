# Civilization Orchestrator — Run Report, Session 99 (2026-10-24)

> **Concurrency note:** a second agent ran a parallel "session 98" against the same
> remote while this run was in flight. Its report and learnings are preserved
> unchanged as `RUN_REPORT_2026-10-24_session98.md` and the "Session 98
> additions" section. This document is the independent account of the same
> command; the two agree on the headline result (Control A no-op, Control B
> +80 uniform) and on the lifetime low-relevance finding (`civ-grounded`).
> Where they differ is the this-run bottom, which is body-set dependent —
> exactly the instability documented below.


**Command requested:** `python3 .../civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Remote HEAD at start:** `264f9d5` (a commit *newer* than s97's `3fa43f2`)
**Result:** the command as written produces **zero simulations**. A stubbed control produces exactly **+80 rows**.

---

## 1. Environment reconstruction

The task path did not exist at session start. `/workspace` held only `.plugin-cache`.

- `SuperInstance/AI-Writings` (3.7 GB) was fetched with
  `git clone --depth 1 --filter=blob:none --no-checkout` into `/tmp/ai-writings`
  — **this worked**, contradicting s94's "filter is WORSE than a full clone".
  The s94 failure was a *racing second clone* at the same target, not the filter
  itself. Filter + `--no-checkout` + explicit `git sparse-checkout set
  cellular-first-design` + `git checkout` in one sequence is the working recipe.
- NAS `/workspace` is at **100 % quota** (600 G used, 0 avail) — the EDQUOT trap.
  A `cp -r` of the civilizations tree reported `exit:0` while 20+ files landed
  **0 bytes and still visible in `ls -la`**. Confirmed again: *every NAS write
  must be verified with `wc -c`, never with the exit code.*
- Bridge used: `ln -sfn /tmp/ai-writings /workspace/repos/ai-writings`.
  `CIVS_DIR` is hardcoded to the `/workspace` path, so the symlink is what makes
  the script write into the clone. Verified by **inode identity**
  (`130:1705275` on both sides), not by `ls`.
- `gh` is not installed; used the GitHub REST API with `$GITHUB_TOKEN`.
  `GIT_SSL_NO_VERIFY=1` required.
- `write` tool is jailed to the workspace root — the mock server was written
  with a bash heredoc to `/tmp`.

## 2. Control A — the command exactly as asked: a NO-OP

```
$ python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
=== Civilization batch: 8 civs x 5 sims each ===
[The Grounded] running 5 sims...
... (all 8 civs) ...
=== Civilization competitions: 5 prompts ===
                            <-- NO "Winner:" LINES
```
**EXIT CODE 0.**

| metric | before | after | delta |
|---|---|---|---|
| ledger rows (all 8 civs) | 3724 | 3724 | **+0** |
| `meta_log.jsonl` lines | 238 | 238 | **+0** |
| `Winner:` lines | — | 0 | — |

**Root cause, measured, not assumed:**

- `ZAI_TOKEN` is absent from env **and** from the secret store (8th consecutive
  session, 36th consecutive finding).
- z.ai coding endpoint probed directly with a sandbox secret →
  **HTTP 401 `token expired or incorrect`**. A 401 means the endpoint is
  healthy ⇒ **credential gap, not an outage**.
- JEV probed directly → **HTTP 200, model `jev-1.14.0`, real score (0.19,
  conf 0.70)**. The scorer was live the whole time; only the provider was dark.
- The provider gate returns `None` silently (line 79: `if not token: return None`),
  so `run_simulation` returns before appending a row, and `civilization_competition`
  returns `None` before the competition section can print a winner.

**TELL (unchanged, 36th replication):** the batch header and all 8
`[Name] running 5 sims...` lines print **before** the provider call. They are
not evidence of work. **Assert on `Winner:` lines and on the ledger row delta —
never on exit code.**

## 3. Control B — stub the transport only, leave JEV real

`ZAI_TOKEN=<set>` + `ZAI_URL_OVERRIDE=http://127.0.0.1:8099/v4/chat/completions`
(mock z.ai). `ZAI_URL_OVERRIDE` is **already committed upstream** (blob line
47) — no patch to the script was needed, and the script stayed byte-identical
to the git blob.

| metric | baseline | after | delta |
|---|---|---|---|
| ledger rows | 3724 | 3804 | **+80** (10 per civ, uniform) |
| rows per civ | — | — | 10 each, 8/8 civs |
| `meta_log.jsonl` | 238 | 243 | **+5** |
| `Winner:` lines | 0 | 5 | 5 |
| all-2.0-default rows (outage default) | — | **0** | real JEV scores |
| rows with a score `error` | — | **0** | — |
| mock-marked rows | — | **80/80** | marker at the **front** |
| distinct `content_preview` | — | **80/80** | no duplicate previews |
| `provider` field on new rows | — | `zai` 80/80 | routing correct |

**The s97 marker-front fix holds.** The mock emits
`content = f"[mock-zai {salt}] " + body` — salt **first**, because the
orchestrator stores only `content[:200]` and a trailing marker is truncated
away (which previously produced 76/80 distinct previews and an invisible
synthetic-row audit).

**This-run winners:** `civ-precise` ×2, `civ-grounded` ×2, `civ-formal` ×1.

## 4. Low relevance — three different questions, three different answers

**Reported separately, never merged.** The authoritative source is
`culture.json` / the ledger, not the board's own sort key.

| lens | last | value | 2nd lowest | gap |
|---|---|---|---|---|
| board `relevance_per_sim` (lifetime average) | **civ-grounded** | 1.464 | civ-formal 1.647 | 0.183 |
| board raw relevance | **civ-grounded** | 672.01 | civ-formal 732.95 | 60.94 |
| board `win_rate` (**selection** metric) | **civ-poetic** | 0.009 | civ-whimsical 0.018 | 0.009 |
| clean lifetime `avg_score` (n=2364) | **civ-grounded** | 1.678 | civ-formal 1.781 | 0.103 |
| clean lifetime `alignment` | **civ-grounded** | 2.221 | civ-engineer 2.669 | **0.449** |
| clean lifetime `novelty` | **civ-formal** | 1.414 | civ-precise 1.578 | 0.164 |
| clean lifetime `quality` | civ-precise | 1.104 | civ-formal 1.104 | 0.001 |
| this run (10 rows/civ) `avg_score` | **civ-mythic** | 1.040 | civ-poetic 1.206 | 0.166 |

**`civ-grounded` is last on 4 of 8 lifetime lenses** — 5th consecutive session
(s94–s98). The longevity-artefact defence stays falsified: it has **322 clean
rows, 2nd most of 8** (whimsical 334), so a lifetime-average denominator should
*penalise* it relative to the middle — instead it is last on the
denominator-least-biased lens. Its **alignment deficit of 0.449 is the largest
separation of any lens**, and alignment is the dimension the meta-GAN selects
on. That is a structural deficit, not a ranking artefact.

**`civ-formal`'s weakness is specifically flattest prose** — lowest clean
lifetime `novelty` (1.414) and last on both this-session body readings of the
run. Distinct axis from the Grounded's *alignment* deficit. **Name the axis;
do not merge them into one "lowest civ".**

**`civ-poetic` is the inverse case** — 1st on clean lifetime `avg_score` (2.295)
and 1st on the board's `relevance_per_sim` (2.107), yet **last on `win_rate`
(0.009; chooser picked it 3 times in 243 rounds while it was argmax 98)**.
A *selection* failure, not a quality collapse. Stable across 15 sessions.

**`civ-precise` is the other inverse** — best `win_rate` (0.469) but last on
clean lifetime `quality` and `novelty`.

**This-run bottom is not stable across sessions** (s96: grounded/formal;
s97: formal/formal; **s98: mythic**). The *this-run* bottom is body-set
dependent and must never be reported as *the* low-relevance civ. The lifetime
reading is the stable one.

**Extinction risk: NONE.** The threshold is `relevance < -10`; the lowest is
+672.01, and `extinction_and_birth()` runs only in `--loop` mode every third
iteration — a single-shot run never triggers it.

## 5. The chooser and the scorer are decoupled (24th replication)

On the committed `meta_log.jsonl` (243 rounds) the JEV chooser agrees with the
`avg_score` argmax **38 times = 15.6 %**. The competition chooser never sees
the scores — `state` carries only `content_preview[:150]` and the question is a
`choice` with no score column — so these are two independent JEV calls.

| | chooser picks | argmax picks |
|---|---|---|
| civ-precise | **101** | 32 |
| civ-grounded | 60 | **3** |
| civ-poetic | **3** | **98** |

All 5 rounds of this run disagreed (chooser `precise/grounded/grounded/precise/formal`
vs argmax `engineer/formal/engineer/engineer/engineer`).

**Therefore "prefer win rate" is unsafe as a standalone rule.** `win_rate`
measures *selection appeal*, not relevance.

## 6. The counter gap persists

Ledger rows vs registry `simulations_run`, after this run:

| civ | ledger | registry | gap |
|---|---|---|---|
| civ-engineer | 456 | 434 | +22 |
| civ-formal | 487 | 445 | +42 |
| civ-grounded | 502 | 459 | +43 |
| civ-mythic | 459 | 439 | +20 |
| civ-poetic | 481 | 444 | +37 |
| civ-precise | 451 | 435 | +16 |
| civ-therapist | 454 | 437 | +17 |
| civ-whimsical | 514 | 451 | +63 |
| **total** | **3804** | **3544** | **+260** |

`save_state()` rewrites the whole `culture.json` from in-memory counters with
no lock and no read-modify-write ⇒ lost-update race ⇒ **`relevance_per_sim` is
not recomputable from the ledger by an auditor.** The board's sort key is
therefore not a reproducible ranking.

## 7. Committed-ledger state (at remote HEAD `264f9d5`)

- 8 civs, **3724 committed ledger rows**, `meta_log.jsonl` 238 lines.
- **1440 synthetic (38.7 %)** by the two-family marker scan (`[mock-` and
  `[The `), uniform 180 per civ; **2364 real**.
- Board-vs-argmax rank inversion: the board's 1st (`civ-poetic`) is the fleet's
  worst pick rate; the board's 5th (`civ-precise`) is the best.

## 8. State at session 99 close

- The Control B synthetic rows were **restored from git**:
  `git checkout -- cellular-first-design/code/civilizations/`.
- `git status --short` → **empty**.
- **All 20 tracked files verified byte-identical to the git blobs with `cmp`
  against `git show HEAD:<path>`** — not by md5 eyeballing, not by exit code.
- `civilization_orchestrator.py` was **never modified** (byte-identical to the
  git blob) — `ZAI_URL_OVERRIDE` is upstream.
- No `__pycache__` left behind.
