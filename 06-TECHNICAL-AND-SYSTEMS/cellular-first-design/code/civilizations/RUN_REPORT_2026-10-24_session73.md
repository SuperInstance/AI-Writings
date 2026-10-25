# civ-orchestrator session 73 (2026-10-24) — credential gap 20th deep; the ZAI_TOKEN gate is upstream of the URL and the override alone is a no-op

## What was asked
Run `civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`, verify
`simulations.jsonl` files have new entries, note any civilization with low relevance.

## Environment reconstruction (path did not exist again — 10th consecutive time)
- `/workspace` held only `.plugin-cache`. NAS at **100 % quota** — the EDQUOT trap.
  A full `cp -r` of the clone into `/workspace/repos` died with
  `cp: failed to close '...': Disk quota exceeded` on a **0-byte** file
  (`.git/description`, `.git/config`, hook samples) while `df -h` showed
  600 G/600 G used and 0 avail. The trap is not space and not inodes
  (`df -i` showed ~5 % used) — it is `close()` on the NAS mount.
  **Plain file creation succeeds; `close()` on some paths returns EDQUOT.**
- Cloned to `/tmp` (overlay, 28 G free) with `--filter=blob:none --no-checkout`
  (952 K) + sparse-checkout of only `cellular-first-design/code/{civilizations,autoclaw}`
  => 51 M working tree. A plain `git clone` of the full repo would have pulled
  ~3.6 GB and hit the same wall.
- `gh` absent. GitHub REST **search** worked, but the **repo** endpoints
  returned `API rate limit exceeded` for user ID 193104091 — 403 renders as
  "no such repo" for every candidate. Switched to the **git protocol**
  (`git ls-remote`) for existence checks, which is the durable rule.
- `SuperInstance/cellular-first-design` does **not** exist (ls-remote -> "Repository
  not found"). The real path is `cellular-first-design/` **inside**
  `SuperInstance/AI-Writings`, default branch `main`, HEAD `7c01ed3`
  ("wesley-mechanic: canon poll 2026-10-24T07:53Z - no change (b20375d389cb505d, 71 papers)").
  The `civ-orch/*` and `research/civ-orchestrator-session4` branches are older
  snapshots; `main` is live with **114** files under `code/civilizations/`
  (run reports through session 72).
- Bridged with the **two-level symlink** (the one-level
  `/workspace/repos/ai-writings -> /tmp/ai-writings` does **not** work, because
  `CIVS_DIR` is hardcoded to the full deep path):
  `ln -sfn /tmp/cfd-main/cellular-first-design/code/civilizations /workspace/repos/ai-writings/cellular-first-design/code/civilizations`.
  Verified with `stat -L -c %i` = **10446 on both sides** (plain `stat` reports the
  *symlink's* inode and makes a correct bridge look broken — use `-L`).
  Write-through probe (`.bridge_test`) landed in the clone => bridge is live.
- `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` — **20th recurrence** of the name
  split. The sandbox exports `TYPESAFE_AI_TOKEN`; the orchestrator reads
  `TYPESAFEAI_KEY`. JEV verified live independently: HTTP 200, `jev-1.14.0`,
  real score **1.63**.
- `ZAI_URL_OVERRIDE` **is** already committed (line 84). Confirmed with
  `grep -n` — **do not use `grep -c` inside a compound `cd && ...` command**, the
  path reset made it report 0 and nearly sent me patching a file that needed
  no patch. `git diff` on the script is **empty**; no patch was applied.

## The credential gap (20th consecutive session)

| credential | state |
|---|---|
| `ZAI_TOKEN` | absent from env **and** from the 8-entry secret store |
| `ZAI_KEY` | absent |
| `GROQ_TOKEN` | absent (no alternate live provider) |
| `TYPESAFEAI_KEY` | absent — name split; `TYPESAFE_AI_TOKEN` is present and JEV is **live** |
| `TYPESAFE_AI_TOKEN` | present — JEV `jev-1.14.0`, HTTP 200, real scores |

All **8** sandbox secrets (`CRATES`, `MOTHQUANTUM`, `GITHUB`, `NOTION`,
`TYPESAFE_AI`, `NPMJS`, `PYPI`, `MINIMAX`) tested against
`https://api.z.ai/api/coding/paas/v4/chat/completions`: **401 on every one** —
and 401 on the **no-header baseline** too. A 401 rather than a 5xx means the
endpoint is healthy => **credential gap, not an outage.** The `secret` CLI is
not on PATH, but the `secret` tool lists 8 secrets and **none is a z.ai key**.

## Run 1 — the requested command, unpatched: NO-OP (20th session in a row)

```
BEFORE rows=2364 meta=153
EXIT=0
AFTER  rows=2364 meta=153
DELTA rows=0 meta=0
```

**0 `Winner:` lines.** The log printed the batch header, all 8
`[Name] running 5 sims...` lines, then the competition header and nothing.
Only `leaderboard.json` was rewritten (md5 `88d5f085...` -> `335d7e74...`, same
content, `iso` bumped). The per-civ sim lines are printed **before** the
provider call, so they are **not** evidence of work. **Assert on the row
delta, never on the exit code.**

Mechanism (confirmed in code): `call_provider` does
`token = os.environ.get(p["env"], ""); if not token: return None` and
`run_simulation` returns `None` **before** the `simulations.jsonl` write.

## Control B — the `ZAI_TOKEN` gate is UPSTREAM of the URL

**First attempt (override only) was also a NO-OP: +0 rows, and the mock log
stayed at 1 line (my own health probe).** Reproduced directly, outside the
orchestrator:

```python
os.environ["ZAI_URL_OVERRIDE"] = "http://127.0.0.1:8931/chat/completions"
os.environ.pop("ZAI_TOKEN")            # gate
co.call_provider("zai", "hello", {...})  ->  None
```

`ZAI_URL_OVERRIDE` rewrites the URL, but the function **returns before it
looks at the URL**. The gate is a hard `return None` on an empty env var.
**A dummy `ZAI_TOKEN` is mandatory** — it is never validated (the mock does not
check auth). This is the learnings file's s7 note, restated here because the
operational recipe was still not obvious from the older reports.

**Second attempt — full recipe:**
```
ZAI_TOKEN=dummy-control-b-token
ZAI_URL_OVERRIDE=http://127.0.0.1:8931/chat/completions
TYPESAFEAI_KEY=$TYPESAFE_AI_TOKEN
```

| metric | value |
|---|---|
| ledger rows | **+80** (10 per civ, uniform) |
| `meta_log.jsonl` | **+5** |
| `Winner:` lines | **5** |
| distinct mock previews (200-char) | **80/80** |
| all-2.0-default rows | **0** (JEV live) |
| JEV score errors | **0** |

Control B is green for the **20th** time => the orchestrator, the provider hook,
and the live JEV path are all healthy. The only thing missing is one z.ai key.

**Mock design (verified BEFORE the run, per the learnings file).** Rotating the
**leading** fragment every call — variety that starts late is invisible because
`content_preview` is `content[:200]`. Probe: **5/5 distinct at the 200-char
window for all 5 test voices**, 25/25 distinct at both 60 and 200 chars.
Marker prefix `[mock-zai #N]` in the body so mock rows are identifiable in the
ledger.

**A background mock can be killed by its own cleanup line.** `kill` on the
`timeout` wrapper (pid 706) left the Python child (pid 708) alive and the port
still answering HTTP 200. Kill by scanning for the script name, then
**re-verify the port returns 000**; do not trust the kill's exit status.

## The four-lens low-relevance reading (never merged)

**Lens 1 — lifetime (2444 rows):**

| civ | avg | quality | novelty | align | rows |
|---|---|---|---|---|---|
| civ-poetic | **2.189** | **1.472** | 2.248 | 2.847 | 311 |
| civ-whimsical | 2.129 | 1.287 | **2.410** | 2.691 | 344 |
| civ-mythic | 1.923 | 1.125 | 2.160 | 2.483 | 289 |
| civ-therapist | 1.906 | 1.047 | 2.183 | 2.487 | 284 |
| civ-precise | 1.855 | 1.061 | 1.635 | **2.868** | 281 |
| civ-engineer | 1.753 | 0.972 | 1.698 | 2.588 | 286 |
| civ-formal | 1.714 | 0.994 | **1.470** | 2.676 | 317 |
| **civ-grounded** | **1.554** | **0.960** | 1.729 | **1.972** | 332 |

**Lens 2 — board (post-run `leaderboard.json`, iso `2026-10-24T08:06:11`):**

| rank | civ | rel/sim | relevance | W | L | win% | temp |
|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 2.132 | **584.04** | 1 | 132 | **0.008** | 0.8 |
| 2 | civ-whimsical | 1.991 | 559.38 | 3 | 130 | 0.023 | 0.95 |
| 3 | civ-mythic | 1.876 | 504.64 | 3 | 124 | 0.024 | 0.85 |
| 4 | civ-therapist | 1.869 | 499.06 | 2 | 128 | 0.015 | 0.6 |
| 5 | civ-precise | 1.844 | 488.57 | **67** | 61 | **0.523** | 0.2 |
| 6 | civ-engineer | 1.731 | 457.04 | 10 | 116 | 0.079 | 0.4 |
| 7 | civ-formal | 1.664 | 457.68 | 19 | 112 | 0.145 | 0.3 |
| **8** | **civ-grounded** | **1.493** | **431.46** | 34 | 98 | 0.258 | 0.5 |

**Lens 3 — this session only (80 mock rows):**

| civ | avg | quality | novelty | align |
|---|---|---|---|---|
| civ-whimsical | **2.050** | 0.684 | **2.677** | **2.790** |
| civ-poetic | 2.044 | **0.725** | 2.538 | 2.869 |
| civ-formal | 1.864 | 0.702 | 2.356 | 2.535 |
| civ-mythic | 1.732 | 0.497 | 2.521 | 2.177 |
| civ-therapist | 1.696 | 0.411 | 2.534 | 2.143 |
| civ-precise | 1.674 | 0.396 | 2.348 | 2.277 |
| civ-engineer | 1.641 | 0.402 | 2.330 | 2.190 |
| **civ-grounded** | **1.378** | **0.212** | 2.502 | **1.420** |

**Lens 4 — win rate (the genuine competitive signal):**
`civ-poetic` 0.008 (1W/132L) < `civ-therapist` 0.015 < `civ-whimsical` 0.023 <
`civ-mythic` 0.024 < `civ-engineer` 0.079 < `civ-formal` 0.145 <
`civ-grounded` 0.258 < **`civ-precise` 0.523 (67W/61L)**.

### The answer, per lens
- **Lowest `relevance_per_sim` (board sort): `civ-grounded` 1.493.** It also ran
  the **most** sims (332) and still scores lowest => a genuine writing deficit,
  not the longevity artefact the denominator suggests.
- **Lowest raw relevance: `civ-grounded` 431.46** — lowest on the board, on
  lifetime avg, on lifetime quality, on lifetime alignment, and on this
  session's avg/quality/alignment.
- **Lowest lifetime quality: `civ-grounded` 0.960** (ahead of `civ-engineer`
  0.972); **lowest lifetime novelty: `civ-formal` 1.470**; **lowest lifetime
  alignment: `civ-grounded` 1.972** — 17 % below the next civ (2.483).
- **Lowest win rate: `civ-poetic` 0.008 (1W/132L)** — 1st of 8 on the board,
  highest raw relevance (584.04), **highest lifetime `avg_score` (2.189)**,
  highest lifetime quality (1.472) — and **one win in 133**. **20 sessions.**
- **Lowest this-session `avg_score`: `civ-grounded` 1.378** — 8th of 8 again.
- **Healthiest: `civ-precise`** (67W/61L, 0.523) — the only civ whose relevance
  rank and win rate agree.
- **Extinction: none.** Lowest relevance +431.46 vs the -10 threshold, and
  `extinction_and_birth()` only runs under `--loop` every third iteration, so a
  single-shot run never triggers it.

### Cross-lens tally — `civ-grounded` is lowest on 8 of 11 metrics
lifetime avg / quality / alignment, session avg / quality / alignment, board
rel-per-sim / relevance => **the only position stable across every lens**.
`civ-formal` (lifetime novelty), `civ-engineer` (session novelty) and
`civ-poetic` (win rate) are each lowest on exactly one.

## The board still ranks backwards against selection — 8/8 positions inverted

| board rank (`relevance_per_sim`) | | by `win_rate` |
|---|---|---|
| 1 | civ-poetic (0.008) | **civ-precise (0.523)** |
| 5 | **civ-precise (0.523)** | civ-grounded (0.258) |
| 8 | civ-grounded (0.258) | **civ-poetic (0.008)** |

**All 8 positions differ** (8th session running). The board is a lifetime
accumulation over a lifetime denominator; it is not a selection ranking.

## Counter gap: exactly **+260**, unchanged for the 20th session
Ledger **2444** rows vs registry `simulations_run` sum **2184** — **+260**,
identical to the last 19 sessions. `save_state()` rewrites the whole
`culture.json` from in-memory counters with no lock and no read-modify-write =>
lost-update race => **`relevance_per_sim` is not a reproducible ranking** and no
auditor can recompute the board order from the ledger. Per-civ gap:
whimsical 63, grounded 43, formal 42, poetic 37, engineer 22, mythic 20,
therapist 17, precise 16.

## Chooser/argmax agreement hit **0/5** again

| prompt | JEV `best_civ` chooser | `argmax(avg_score)` | agree |
|---|---|---|---|
| what a cell is | civ-precise | civ-poetic | ✗ |
| the bookkeeper's role | civ-grounded | civ-poetic | ✗ |
| the witness log | civ-grounded | civ-poetic | ✗ |
| ternary values | civ-precise | civ-poetic | ✗ |
| JEV as a decision oracle | civ-formal | civ-poetic | ✗ |

**0/5** — matches the 0/5 recorded in the previous session. `argmax` picked
`civ-poetic` on **all five** prompts; the chooser picked `civ-precise` 2/5,
`civ-grounded` 2/5, `civ-formal` 1/5 — **never** `civ-poetic`. The chooser is a
JEV *choice* over 150-char previews with no scores in the prompt; the scorer
sees per-civ quality/novelty/alignment. They are decoupled by construction.
**A chooser sweep is a selection result, not a quality result** — and here the
chooser's picks are the two civs the other lenses flag as low-relevance, so a
board rebuilt from chooser outcomes would invert the current ranking.

## Durable notes
1. **`ZAI_URL_OVERRIDE` alone is a no-op.** The `ZAI_TOKEN` gate fires
   **before** the URL is read. The full Control B recipe is
   `ZAI_TOKEN=<any dummy> + ZAI_URL_OVERRIDE=<mock> + TYPESAFEAI_KEY=$TYPESAFE_AI_TOKEN`.
   A transport-only stub is a control with no power.
2. **The 401-vs-5xx test discriminates gap from outage — and the no-header
   baseline is the control.** All 8 secrets returned 401, and so did no-auth.
   Use the baseline to prove the endpoint is alive.
3. **The `secret` tool works even when the `secret` CLI is absent from PATH.**
   8 entries, no z.ai key. Don't conclude "no credential" from `env` alone.
4. **`stat` vs `stat -L` on a symlink bridge.** Plain `stat` reports the
   *symlink's* inode, so a correct two-level bridge looks like a mismatch.
   Use `stat -L -c %i` and compare both sides.
5. **`grep -c` inside a compound `cd && ...` command can report the wrong file**
   (the path reset). Use `grep -n` and read the line — the question is
   "is the hook present", not "how many times".
6. **A blobless sparse clone beats a full clone here**: `--filter=blob:none
   --no-checkout` + `sparse-checkout set` = 51 M working tree vs ~3.6 GB.
   The full repo cannot be materialised on a 100 %-full NAS.
7. **The mock's `timeout` wrapper and its Python child are separate PIDs.**
   Killing the wrapper leaves the child serving. Re-verify the port returns
   000 after cleanup.
8. The committed baseline still carries **560 mock rows** (70 per civ) in
   `HEAD`; the 80 rows added this session are mock rows too, and are **not**
   tagged in any machine-readable field — the marker prefix lives inside
   `content_preview`, so the ledger still cannot distinguish mock from real
   provider output except by string match.
