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

**`ZAI_URL_OVERRIDE` is NOW IN THE COMMITTED BLOB** (script lines 84-86) — **do
not re-apply a patch** (session 64 confirmed: patched nothing, got a clean
Control B). The hook is provider-generic:
```python
_ov = os.environ.get(f"{name.upper()}_URL_OVERRIDE", "")
if _ov:
    p = dict(p); p["url"] = _ov
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

---

## Session 64 additions (2026-10-24) — 27th credential gap; Control B 12th replication; STALE `ZAI_URL_OVERRIDE` instruction; a clone with an EMPTY INDEX that looks fine

**Base commit `030feb4f`.** Ledger 2284 rows, `meta_log` 148, **640 mock rows (27.1 %)**.
Unpatched `--sims 5 --prompts 5 --providers zai` → **+0 rows, +0 meta_log, 0 `Winner:`
lines, exit 0** (27th replication). Control B → **+80 rows (exactly +10/civ, uniform), +5
meta_log, 5 winners, 0 all-2.0-default rows, 0 score errors, 0 cross-civ preview collisions,
80/80 distinct previews, 71/80 distinct `avg_score` (0.670–1.773, mean 1.1533), JEV
confidence 0.420–0.990, 0 scaffolding leaks, mock 80/80 distinct salts, uniform 10-per-voice
distribution.** Control B = **12th consecutive identical replication**.

### STALE INSTRUCTION — `ZAI_URL_OVERRIDE` is NOW UPSTREAM; do not look for a patch

The skill's "re-apply this one-line patch each session" line is **obsolete**. The committed
blob already contains the Control B hook at **lines 84–86** of `civilization_orchestrator.py`:
```python
_ov = os.environ.get(f"{name.upper()}_URL_OVERRIDE", "")
if _ov:
    p = dict(p); p["url"] = _ov
```
It reads `f"{name.upper()}_URL_OVERRIDE"`, so it is generic across providers, not ZAI-specific.
**Session 64 patched nothing and still got a clean Control B.** The script md5 was
`501fa686b846199b2057d3b70b4d66d9` — unchanged. Delete the patch instruction from this skill.

### NEW — a clone can have a PERFECT WORKTREE and an EMPTY INDEX

The first `git clone --depth 50` attempt died mid-transfer but left a **stale
`.git/index.lock` and NO `.git/index`**. The second clone (`--depth 1 --single-branch`)
then wrote the worktree but never the index. Symptoms that look like corruption but are not:

- `git ls-files | wc -l` → **0** (every tracked file "missing")
- `git status --porcelain` → **105 civ-dir files as STAGED deletions** (`D `, not ` D`)
- the files are all present and correct on disk

Fix: `rm -f .git/index.lock && git read-tree HEAD` — on a 3.4 GB tree this **exceeds a 30 s
tool call**; run it in the background. **Assert `git ls-files | wc -l > 0` AND that
`git status --porcelain` shows no `D ` entries after every clone**, before trusting the
worktree or staging anything. A `D `-heavy status is an index problem, not a deleted repo.

### NEW — `git clone --depth 50` is broken (confirmed again), `--depth 1 --single-branch` works

`--depth 50` died with `fatal: could not open .../tmp_pack_xVlHiQ for reading: No such file
or directory` / `invalid index-pack output` after ~1.1–3.4 GB. `--depth 1 --single-branch
--no-tags` succeeded in ~2 min (3.4 GB). The runbook's blobless recipe remains the cheapest
(1 MB) — but it excludes the index materialisation step that bit this session.

### Grounded is bottom on **9 of 16** lenses — the stable answer

| lens | lowest |
|---|---|
| A `relevance_per_sim` (board key) | `civ-grounded` 1.479 |
| B raw relevance | `civ-grounded` 412.73 |
| C win rate | `civ-poetic` 0.008 (1W/127L) |
| D lifetime avg / alignment | `civ-grounded` 1.700 / 2.261 |
| D lifetime quality / novelty | `civ-engineer` 1.140 / `civ-formal` 1.357 |
| E this-run avg / alignment | `civ-grounded` 0.863 / 1.032 |
| E this-run quality / novelty | `civ-engineer` 0.202 / `civ-formal` 0.985 |
| F de-con lifetime avg / align | `civ-grounded` 1.700 / 2.261 |
| F de-con lifetime quality | `civ-engineer` 1.140 |
| G ledger avg (all rows) | `civ-grounded` 1.544 |
| H `simulations_run` | `civ-engineer` 254 |

**Lowest-lens count: Grounded 9, Engineer 3, Formal 2.** (Session 61: 8/4/2. Session 60: 6/14.)
`Pearson r(sims_run, rel_per_sim) = −0.310` — **negative, so NOT a longevity artefact**
(most-run is `civ-whimsical` 271; board-last `civ-grounded` 279). The Grounded has the
**2nd-highest win rate (0.252)** while producing the **lowest** scores — it wins on
*selection appeal* and loses on *substance*; its "warm, factual" voice reads as tonally flat
to JEV (lowest lifetime alignment 2.261). **The Poetic anomaly holds for the 12th run:**
1st of 8 on every quality lens (A 2.126, B 561.22, D 2.305) and last on win rate.
**E moves session to session** — E-bottom was Engineer/Formal this run, Formal on all three
in session 61. **Grounded was E-bottom on avg + alignment in both** — that is the stable part.

**Chooser vs `argmax(avg_score)`: 1/5 this run** (chooser Grounded ×3, Precise ×2; argmax
Precise ×3, Engineer ×2). Lifetime by exact score-multiset match: **7 agree / 25 disagree =
21.9 %** (32/153 rounds had a unique score owner). History 4.4 → 22.4 → 17.6 → 11.9 → 17.6
→ **21.9 %**. `r(preferred_temp, lifetime novelty) = +0.9371`.
**Counter gap +260, unchanged** (ledger 2364 vs registry 2104) — the run added 80 to both, so
it does not widen. **Mock contamination 640/2364 = 27.1 %.**

### A force-update on the remote is now routine — commit on top, never rebase

Remote moved `030feb4f → 6a32efa1` mid-session (touching only `index.html`/`index.json`, a
landing-page auto-update). `git diff --name-only HEAD origin/main -- <civ dir>` → **0 files**,
so a plain commit-on-top is clean and conflict-free. After `git reset --soft origin/main`,
the remote's own auto-update files appear **staged** — `git restore --staged index.html
index.json` to drop them, then stage only your own file. Verify with `ls-remote`
immediately before the push (the tip moved twice in session 62).

**Restore verified 105/105 byte-identical** to the HEAD blobs with the materialised-blob
`cmp` (never against a process-substitution FIFO). Ledger back to 2284, meta_log 148, mock
rows 640, script md5 unchanged, `git status --porcelain` clean, no `__pycache__/`.
**Push verified two ways** — `ls-remote` and the commits API; the report file was also
re-fetched via the contents API and confirmed **byte-identical** to the local copy.

## Session 61 additions (2026-10-24) — 26th credential gap; blobless+sparse bootstrap; within-civ salt collision vs cross-civ signal defect

**Baseline HEAD `26fcb75` (session 60): ledger 2284 rows, `meta_log` 148.**
Unpatched `--sims 5 --prompts 5 --providers zai` → **+0 rows, +0 meta_log, 0 `Winner:`
lines, exit 0** (26th replication). Control B → **+80 rows (exactly +10/civ, uniform),
+5 meta_log, 5 winners, 0 all-2.0-default rows, 0 score errors, 0 cross-civ preview
collisions, 79/80 distinct full previews, 67/80 distinct `avg_score` (0.830–1.810, mean
1.3569), JEV confidence 0.340–0.990.** Control B = **11th consecutive identical replication**.

**Credential gap: 26th session.** `api.z.ai` = **401**; the same-family
`api.github.com/user` = **200**; JEV live at `jev-1.14.0` (probe `quality 1.54`,
`confidence 0.42`). Always `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"`.
**Assert on the row delta and the `Winner:` count, never on the exit code.**

### NEW — `--filter=blob:none --no-checkout` + `sparse-checkout` is the cheapest bootstrap (1 MB, seconds)

The full `git clone --depth 50` **died twice** at the 30 s tool timeout
(`invalid index-pack output` at 1.1 GB). The blobless path succeeded in **one foreground call**:

```bash
git -c http.postBuffer=524288000 clone --filter=blob:none --no-checkout --depth 30 \
    "https://x-access-token:$GITHUB_TOKEN@github.com/SuperInstance/ai-writings.git" /tmp/aw
cd /tmp/aw && git sparse-checkout init --cone \
  && git sparse-checkout set cellular-first-design/code/civilizations \
  && git checkout
```

**1 MB vs 3.3 GB** — three orders of magnitude, and it still gives a real git history for
push/verify. The civ subtree is ~100 blobs; everything else in the pack is irrelevant.
Gotcha: `git sparse-checkout set <dir>` **fails on a subdirectory path** — set the *parent*
dir so the cone includes the civ subdirs. A second gotcha: a sparse checkout **excludes
top-level paths such as `.skills/` from the index** — use `git add --sparse <path>` (or
disable the sparse rules) or the file silently refuses to stage.

### NEW — a within-civ preview collision is a SALT artifact; a cross-civ one is a SIGNAL defect

`civ-precise` produced **9 distinct previews for 10 rows** (all other civs 10/10). Traced to
the row: the temperature jitter is `preferred ± 0.2` **clamped at the 0.1 floor**, so two sims
drew *exactly* `temperature=0.1000` with identical `max_tokens` and prompt length; the mock's
salt is `sha1(temperature|max_tokens|len(prompt))` ⇒ same salt ⇒ same preview.

- **within-civ** = the *mock's* salt is not unique enough — a harness artifact, harmless to the chooser.
- **cross-civ** = one template is serving two civilizations — it **destroys the chooser's signal**
  and must fail the run.

**Assert the cross-civ count (must be 0) and treat a within-civ duplicate as a salt-collision to
investigate, not as a same-body failure.** Mock fix: salt on
`(temperature, max_tokens, len(prompt), civ)` **plus a per-request counter**.

### NEW — a LOST `cd` produced a FALSE "hook absent" reading that nearly voided the whole plan

`cd <dir> && grep -c "ZAI_URL_OVERRIDE" file` returned **0** while the hook was plainly present
at lines 84–86. The `cd` was silently lost inside the compound command, so `grep` read a stale
path. **Use absolute paths for every read in this project.** A wrong "the hook is missing"
conclusion here would have discarded the only mechanism that makes the run produce rows at all.
This is a *different* failure from the runbook's `cd`-loss trap: that one makes a **relative**
path fail; this one is easy to misread as "the feature is absent".

### The Grounded is bottom on **8 of 16** lenses; Formal is the new E-bottom

| lens | lowest |
|---|---|
| A `relevance_per_sim` (board key) | `civ-grounded` 1.491 |
| B raw relevance | `civ-grounded` 416.02 |
| C win rate | `civ-poetic` 0.008 (1W/127L) |
| D lifetime avg / align | `civ-grounded` 1.554 / 1.979 |
| D lifetime quality / novelty | `civ-engineer` 0.960 / `civ-formal` 1.431 |
| E this-run avg / quality / novelty | **`civ-formal`** 1.080 / 0.136 / 1.364 |
| E this-run alignment | `civ-grounded` 1.340 |
| F de-con lifetime avg / align | `civ-grounded` 1.737 / 2.314 |
| F de-con lifetime quality | `civ-engineer` 1.190 |
| G ledger avg (all rows) | `civ-grounded` 1.554 |

**Lowest-lens count: Grounded 8, Formal 4, Engineer 2, Poetic 1.** (Session 60: 6/14.)
`Pearson r(ledger_rows, rel_per_sim) = −0.095` (near zero); the most-run civ is
`civ-whimsical` (334) and the board-last is `civ-grounded` (322) ⇒ **not a longevity
artefact.** The Grounded has the **2nd-highest win rate (0.244)** while producing the
**lowest** scores — it wins on *selection appeal* and loses on *substance*; its
`"warm, factual"` voice reads as tonally flat to JEV (lowest lifetime alignment 1.979).
**`civ-formal` is the new E-bottom — E moves session to session, report it per run, never as
a standing constant.**
**The Poetic anomaly holds for the 11th run:** 1st of 8 on every quality lens (A 2.140,
B 565.02, D 2.199, F-decon 2.354) and last on win rate (0.008).

**Chooser vs `argmax(avg_score)`: 0/5 this run** (argmax picked `civ-poetic` on 4 of 5 prompts;
the chooser picked it **zero** times). Lifetime **27 agree / 126 disagree = 17.6 %** — stable
around 18 %. `r(preferred_temp, lifetime novelty) = +0.9270`. Winners: Precise ×2, Grounded ×2,
Formal ×1 — **4 of 5 rounds to the two lowest-temperature civs (0.20, 0.50)**.

### Counter gap 260 (unchanged, and this run proves it does not widen)

Ledger **2364** vs registry `simulations_run` **2104** = **260 uncounted**. The run added 80
to the ledger *and* 80 to the counters, so the gap held steady. **Mock contamination: 720 /
2364 = 30.5 %** of the committed ledger is `[mock-zai` rows — **every lifetime figure is
computed over a ~30 % synthetic ledger**; quote it only with that caveat. **Source fix still
outstanding:** tag mock rows with `"mock": true` and purge the 640 historical mock rows
from HEAD.

### Session-58 correction re-confirmed

The inert run left the registry sum at exactly **2024 → 2024 (+0)**. **Session 57's "an inert
run advances `simulations_run` by 10/civ" is session-specific, not a property of an inert
run.** `run_simulation()` returns `None` on a failed call and `save_state()` writes back the
unchanged in-memory counters.

### NEW — the rebase trap bit again, and the recovery worked (2nd independent confirmation)

`git rebase FETCH_HEAD` on a remote that had **force-updated** (`26fcb75...fb9db80`) tried to
replay **another instance's commit** (`0ef5559`, session 54b) and **reset the worktree — my
report file vanished**. Recovery, without a rebase:

```bash
git rebase --abort || true; rm -rf .git/rebase-merge .git/rebase-apply; git reset --hard <remote-sha>
git cat-file -t <my-commit>                    # the commit object survives
git show <my-commit>:<path> > /tmp/recovered.md # extract from the commit
```

`git reset --hard` wiped the worktree copy but **the commit object was intact** — extracted
**byte-identical**. Then committed **on top of the remote head** (no rebase) and pushed.
**Never rebase when the remote force-updated; commit on top of the remote head instead.**
Check `git diff --name-only <base> <remote> -- <civ dir>` first; if it is 0 files, a plain
commit-on-top is clean and conflict-free.

### The NAS quota is SHARED across sessions

`df -h /workspace` showed 600 G used / 0 avail while **this session's own footprint was
1 KB** — other sessions on the same mount consume it. A full mount blocks the `write` tool
*and* bash heredocs alike (`cat: write error: Disk quota exceeded`, 0-byte file, exit 0).
Inodes were fine (5 % used) — it is a **space** quota, not an inode quota. The repo on the
overlay is unaffected, so **the git copy is the durable one**; `cp` into `/workspace` can
leave 0-byte files that `ls` shows as present — verify with `wc -c` every time.

### Other environment notes

- `ls -la <dir> | grep simulations.jsonl` finds nothing — the ledgers are one level down in
  `civ-*/simulations.jsonl`. Use `ls -la <dir>/civ-*/simulations.jsonl`.
- The mock's launch still **hangs the tool call for its full timeout** when `setsid nohup
  ... &` shares a command with other work; the server is nonetheless up and serves every
  request. **Launch in a dedicated call; probe in a separate call; check `ps` before
  declaring it down.**
- Symlink bridge (innermost path) re-confirmed: `stat -c %i` gave **132349 on both sides**.
- **Restore verified 19/19 byte-identical** to the HEAD blob with the materialised-blob
  `cmp` (never `cmp` against a process-substitution FIFO — it reports false differences).
  `git status --porcelain` empty; no `__pycache__/`.
- **Push verified two ways:** `git ls-remote` and the commits API (1 file, +238/-0). The
  remote prints *"This repository moved … use the new location"* — the canonical name is
  **`AI-Writings`** (capital), though `ai-writings` still redirects.
- **Concurrent sessions publish to the same paths.** Session 62 committed
  `RUN_REPORT_2026-10-24_session62.md` on top of my session-61 commit while I was working.
  **Name-check the remote before publishing, and re-sync with `ls-remote` immediately
  before the push** — the tip moved twice during this session.
