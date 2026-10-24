---
name: civ-orchestrator-learnings
description: Durable operational knowledge for the Civilization Orchestrator (cellular-first-design/code/civilizations/civilization_orchestrator.py). Covers the ZAI credential gap, the Control B mock, ledger verification, and the five low-relevance lenses. Load before running the orchestrator.
---

# civ-orchestrator-learnings

Durable operational knowledge for the Civilization Orchestrator
(`cellular-first-design/code/civilizations/civilization_orchestrator.py`).
Survives sandbox wipes. The full long-form file lives in the repo at
`cellular-first-design/code/civilizations/CIV_ORCHESTRATOR_LEARNINGS.md`
(~90 KB, sessions 1-17). This skill is the condensed field manual.

## The headline: exit 0 does not mean it ran

`ZAI_TOKEN` is absent in every sandbox (15+ consecutive sessions). The
orchestrator **exits 0 while producing ZERO simulations** — a green exit over
an empty ledger. **The tell is the absence of `Winner:` lines.**

Provider gate (line ~79):
```python
token = os.environ.get(p["env"], "")
if not token: return None        # silent drop
```

**Assert on the row delta, never on the exit code:**
```bash
before=$(cat civ-*/simulations.jsonl | wc -l)
python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
after=$(cat civ-*/simulations.jsonl | wc -l)
[ "$after" -gt "$before" ] || echo "NO-OP RUN"
```

The per-civ `[Name] running 5 sims...` lines print *before* the provider call —
they are not evidence of work.

## Environment reconstruction

- The task path does **not** exist at session start. `/workspace` holds only
  `.plugin-cache` and `.skills`. Rebuild from **`SuperInstance/AI-Writings`**,
  tree at `cellular-first-design/code/civilizations/`.
- NAS `/workspace` is often at **100 % quota** (600 G used, 0 avail) — the
  EDQUOT trap. Clone to the **overlay** (`/root/work`, 28 G free), then
  `rm -rf /workspace/repos/ai-writings && ln -sfn /root/work/ai-writings
  /workspace/repos/ai-writings`. The script's `CIVS_DIR` is hardcoded to that
  path, so the symlink is what makes it write into the clone.
- **`/workspace` writes create 0-byte files at 100 % quota** — `cp` leaves a
  0-byte file, `cat >` / `dd` / Python `os.write` all fail with
  `Disk quota exceeded` / errno 122, and the `write` tool fails with errno
  -122. **Git is the only reliable delivery channel** — commit + push + verify
  via the GitHub API.
- **`git clone --depth 50` of `AI-Writings` is BROKEN (session 39)**: it
  transfers 4.0 GB and then dies with `fatal: remote did not send all
  necessary objects` (`Could not read 08c7ea77...`, `Failed to traverse
  parents of commit 5c3904ef...`) — a bad history object at the shallow
  boundary. **Use the blobless partial fetch instead (~15 s, 7.0 GB tree):**
  ```
  git init -q . && git remote add origin "https://x-access-token:$GITHUB_TOKEN@github.com/SuperInstance/AI-Writings.git"
  git -c fetch.writeCommitGraph=false fetch --depth 1 --filter=blob:none origin main
  git checkout -q origin/main
  ```
  This supersedes the older sparse-checkout recipe.
- `GIT_SSL_NO_VERIFY=1` is required. Push to the explicit token URL
  (`https://x-access-token:$GITHUB_TOKEN@github.com/...`).
- `gh` CLI is **not installed**. Use the GitHub REST API.
- The `write` tool is **jailed to the workspace root** — cannot write `/tmp`.
  Use a bash heredoc there.
- `pkill -f <pattern>` self-matches and kills the invoking shell. Kill by PID
  from `ps -eo pid,args --no-headers | grep "[z]ai_mock"`.
- **`/tmp` is not durable WITHIN a session** (session 46): a clone that was
  fully readable minutes earlier was simply gone, `/tmp` at 28 G free. A
  `rm -rf <clone>` in a *retry* command is the likely culprit.
  **Never keep a live clone at a path a retry command might `rm -rf`** — use a
  fresh purpose-named dir (`/tmp/aw`), and re-verify with `ls` + md5 after
  every `git sparse-checkout` and before every later phase.
- `rm -f` on a running mock's log silently detaches it (the fd survives on the
  unlinked inode). **Restart the mock with a fresh log path** instead.

## Environment-name splits (the repo never reconciles them)

| credential | orchestrator reads | other repo code | sandbox exports |
|---|---|---|---|
| z.ai | `ZAI_TOKEN` | `labs/convo-quilt/providers.py` -> `ZAI_KEY` | *(none)* |
| JEV | `TYPESAFEAI_KEY` | - | `TYPESAFE_AI_TOKEN` |

Always `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` so JEV scoring is live.
Without it, JEV silently degrades to the `{"quality": 2.0, ...}` default — a
green run that measured nothing.

## Credential audit

All sandbox secrets return **401 "token expired or incorrect"** against
`https://api.z.ai/api/coding/paas/v4/chat/completions`. A 401 (not 5xx) means
the endpoint is healthy -> **credential gap, not an outage**. JEV at
`https://api.typesafe.ai/v1/systemone` works (returns `jev-1.14.0`).

## Control B (the only control with power over the fault)

Stub **at the gate**, leave JEV untouched:
```
ZAI_TOKEN=<set>  +  ZAI_URL_OVERRIDE -> local mock
=> +10 rows per civ (5 batch + 5 competition) = +80
=> +5 meta_log.jsonl entries, 5 competition winners
=> real JEV scores (not the {"quality":2.0,...} default), 0 score errors
```
A transport-only stub (URL unroutable, token unset) is a control with no
power: the request is never attempted.

`ZAI_URL_OVERRIDE` is **not in the committed blob** — re-apply this one-line
patch each session (blast radius = 1 insertion, 1 deletion):
```python
"url": os.environ.get("ZAI_URL_OVERRIDE", "https://api.z.ai/api/coding/paas/v4/chat/completions"),
```

### Mock rules that are easy to get wrong

- **Key the body set off the civ NAME** in the header
  `You are a voice in the tradition of "The X".` — `voice_emphasis` strings do
  *not* contain the civ name ("The Whimsical" -> "playful, surprising").
  Matching on voice markers silently collapses two civs onto one body set
  while **every output check still passes**.
- **Salt the body, never the prompt.** `body = f(body_set, question,
  temperature, call_index)` gives 80/80 distinct bodies. Echoing the
  scaffolding prompt makes all 8 civs score identical text.
- **Always assert the mock's own per-voice call distribution** (10 per voice
  across all 8). A control can "pass" every output check while misrouting a
  whole voice.
- **Split the cultural preamble before parsing the topic** (session 46). The
  prompt is `You are a voice in the tradition of "The X".\nYour tenets: ...\n\n<TASK>`.
  A topic regex over the WHOLE string yields
  `of the poeticyour tenets salt emberwrite 100 words on what a` — silently
  wrong output, no error. **Split on `\n\n`, take the last chunk, then parse.**
  Derive the topic from the TASK line and the voice from the **name** in the
  `tradition of "<Name>"` line (the civ id never appears in the prompt).
  Result: 10/10 distinct content prefixes per civ — no false-collision artefact.
- **A restarted mock that fails to bind keeps serving the OLD code** (session
  46). `HTTPServer((host, port))` without the request-handler class raises
  `TypeError: TCPServer.__init__() missing 1 required positional argument`;
  the new process dies but the old one still holds the port, so the fix appears
  not to work. **Kill by PID, confirm the port is free, re-run the smoke test
  before the real run.**

## Verification: per-civ, not on the concatenation

The ledgers are **per-civ files**. The last 80 rows of the concatenation is the
tail of whichever civ sorts last — it looks like one civ produced all 80.
**Slice the last N of EACH civ's file**, then assert the per-civ counts
(10/10/10/10/10/10/10/10, not 80/0/0/0).

Cheapest "was the run real" check:
```python
bad=sum(1 for f in glob.glob('civ-*/simulations.jsonl') for l in open(f)
        if all(json.loads(l)['scores'].get(k)==2.0 for k in ('quality','novelty','alignment')))
```
`bad == 0` AND `sum(ledger_rows)` grew => real JEV scores.

### The committed ledger is already 28 % mock output — `grep -c` is NOT a leak test

| civ | `[mock-zai` rows in the pristine remote blob |
|---|---|
| each of the 8 civs | **70** |
| **total** | **560 of 1964 rows (28 %)** |

s24 found 240; it has since grown to 560 (session 46). Every session's lifetime
statistics are computed over a baseline that is ~28 % control output, and
`culture.json` counters count those rows as if they were provider output.

> **A `grep -c "mock-zai"` on the committed ledger is a false positive at
> baseline.** The leak test is a **delta** against the baseline count, never an
> absolute count. Check the delta *before* computing any lifetime statistic.

### Restoring the mock-free ledger

`CIVS_DIR` is hardcoded, so a control tree writes its rows into the **real**
ledger. Restore from the pristine git checkout afterwards and verify with
`cmp` against the git blob, not md5 eyeballing. **A copy of the script is not a
copy of its blast radius.** Restore: all 8 `simulations.jsonl`, all 8
`culture.json`, `meta_log.jsonl`, `leaderboard.json`, and the script itself.

## Low-relevance reading: five lenses, never merge them

The authoritative source is `culture.json` (the registry), not the board.

| lens | lowest (session 17) | what it measures |
|---|---|---|
| A) `relevance_per_sim` (board sort key) | **civ-grounded** 1.834 | lifetime average; penalises the civ that ran most |
| B) raw relevance | **civ-precise** 106.75 | youngest civ — a denominator artefact |
| C) `win_rate` | **civ-poetic** 0.000 (0W/28L) | **selection** metric, not quality |
| D) lifetime `avg_score` (baseline-only) | **civ-grounded** 1.879 | actual JEV quality |
| E) lifetime `alignment` (baseline-only) | **civ-grounded** 2.619 | fit to the cultural voice |

- **`civ-grounded` = the stable low-relevance civ.** Last on A, D and E — the
  three lenses that measure *quality*. A genuine weakness, not the longevity
  artefact A alone suggests. **This is the answer to "which civilization has
  low relevance."**
- **`civ-poetic` = the inverse case** (15+ sessions). 2nd of 8 on `avg_score`,
  1st on quality, 2nd on alignment, and **0 wins in 28**. A *selection*
  failure, not a quality collapse.
- **`civ-precise` = the other inverse.** Best win rate (0.696) but last on
  novelty, 6th on `avg_score`, and in session 17 it was the **weakest scorer
  of the 8 while taking 3 of 5 competition wins**.
- **`civ-poetic` = 1st on A, D *and* E** (2.235 / 2.302 / 2.926) — and the
  *same* civ is **last on win rate**. (Session 39 correction: the older
  "`civ-whimsical` = the only civ where every lens agrees" claim is **not**
  supported — whimsical is 2nd on A and D, 3rd on E. It is 1st on **novelty**.)
- **Extinction risk: none** (threshold -10, lowest +106.75, `--loop`-mode
  only).

**Report baseline-only numbers** (684 committed rows, mock rows excluded).
Mixing control rows into a lifetime statistic silently rewrites the thing you
are reporting.

## Two silent-corruption defects worth fixing upstream

1. **A JEV outage awards a random civ a legitimate win.** All `avg_score`s
   become the `2.0` default, all civs tie, and the `max()` fallback picks an
   **arbitrary** winner — credited with a real win, permanently corrupting the
   only metric that distinguishes quality from selection. Require a
   non-default score before recording a winner; else mark the round `unscored`.
2. **Zero simulations still exits 0.** Replace the silent `return None` with a
   named error and abort non-zero; add a row-count assertion.

## The counter gap (corrupts the board's sort key)

Ledger rows vs `culture.json` `simulations_run`: **+260, unchanged since
session 6** (764 vs 504). `save_state()` rewrites `culture.json` from
in-memory counters with no lock -> lost-update race. **`relevance_per_sim` is
not a reproducible ranking.** Measure the gap blob-to-blob, baseline-to-baseline.

## Replications to re-check each session

- **Control B**: +80 rows uniform / +5 meta_log / 5 winners / 0 defaults /
  0 errors / 0 scaffolding leak / 80/80 distinct bodies / uniform 10-per-voice
  mock distribution. (Session 17 = 10th replication.)
- **Chooser vs `argmax(avg_score)`**: 1/5 this run, 12/101 lifetime (11.9 %)
  in session 39; history 4.4 % -> 22.4 % -> 17.6 % -> 11.9 %. **The two
  metrics are essentially uncorrelated** — the chooser never sees the scores,
  only 150 chars of preview. Match rounds by **exact score-multiset equality**
  against `meta_log`'s `results` field, then disambiguate by the tightest
  time window (<=60 s) over candidate ledger rows. **The meta `ts` is the
  *competition* timestamp and never equals any ledger row's `ts`** — a naive
  timestamp-equality test matches 0 rounds; a loose +/-2 s heuristic matched
  2 of 53 and reported a bogus 100 % agreement in an earlier session. **The two metrics are essentially
  uncorrelated.** The chooser never sees the scores — it only sees 150 chars of
  preview. Match rounds by **exact score-multiset equality** against
  `meta_log`'s `results` field, not by a loose timestamp window (a ±2 s
  heuristic matched 2 of 53 rounds and reported a bogus 100 % agreement).
- **Temperature vs lifetime JEV novelty**: Pearson r = 0.9845 (session 17);
  history 0.985 / 0.981 / 0.9845 / 0.9790 / 0.9783 / 0.9722. **Temperature and
  novelty are the same axis** — the fleet's 8 `preferred_params` are one dial.
- **Mock perturbation on the fleet ranking**: compare the run's max
  per-civ |delta| against **its own** adjacent rank gaps before claiming a
  rank moved. Session 17: max |delta| 0.120, top-3 set survived, bottom-2 set
  changed. **Report the set, not the order.**

## Session reports

`RUN_REPORT_2026-10-23_sessionN.md` / `RUN_REPORT_2026-10-24_sessionN.md` in
the civilizations dir, N = 1..46. Session 46 = base commit `3c63035`;
**+80 rows (10/civ) / +5 meta / 5 winners / 0 default-2.0 / 0 JEV errors / 73
distinct `avg_score` (1.893-2.727)**, script md5 unchanged
(`501fa686b846199b2057d3b70b4d66d9`), mock rows reverted before commit and all
27 files verified `cmp`-identical to the remote blobs.

**Session 46 low-relevance:** `civ-grounded` 1.519 rel/sim (lowest; 229 sims =
largest sample, so a real deficit), `civ-formal` 1.667, `civ-engineer` 1.737.
Lowest win rate: **`civ-poetic` 0.010 (1W/102L)** — 1st on the board, last at
being selected. Healthiest: `civ-precise` (52W/46L, 0.531). Extinction: none
(lowest relevance +347.82 vs threshold -10). Counter gap **+260** (unchanged).
