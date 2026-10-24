# wesley-mechanic — operational run notes

Dated run reports for the canon watcher. Each entry records what the poll
observed, what was appended to `witness.log`, and what environment problem had
to be solved to get there.

## 2026-10-24T12:47Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable ~40.7h (2443 min),
  ~7.0 min since the 2026-10-24T12:40Z poll.
- **Confirmed three times by independent paths:** the watcher's own `poll_canon()`
  (stdout `[WESLEY] no change (b20375d389cb505d, 71 papers)`, exit 0), an independent
  **post-run** curl probe (HTTP 200, 13720 bytes, md5 `d9915bb9f3bcb8794cb57810427d0288`),
  and a recomputation of `sha256(json, sort_keys)[:16]` over that fetched body, which
  independently yields `b20375d389cb505d`.
- **Count key:** the response carries `count` (71), not `paper_count` (absent; top-level
  keys are exactly `['count','papers']`), so the 2026-10-22 count-key fallback fix
  remains load-bearing and still correct.
- **No canon-change note written.** A hash match is not a transition. No gamma/eta
  delta claimed — `bookkeeper_tick()` is only reached from the `first_poll` and
  `canon_changed` branches, so stable canon correctly produces zero ticks:
  `bookkeeper.wal` still does not exist and `state.json` is byte-unchanged
  (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log append:** two rows — the unconditional `bot_started` (pid 304, hash
  `337b3279b727e226`) plus this run's `witness_note` (hash `2899cc60a0249c00`).
  `witness.log` went 144 → 146 rows.
- **Log integrity:** 146/146 rows parse and carry `ts, iso, event, payload, hash`.
  Linkage class `row-checksum` (per `../README.md`): each row's hash commits to its
  own payload only — re-scanned every payload for `prev` / `prev_hash` / `parent` /
  `prev_row_hash`: **none found**. Deletion and truncation of a row are therefore
  undetectable in this format, so the honest verdict is
  `142 verify + 2 RECOVERED markers + 1 known-stale hash — linkage class
  row-checksum`, not "chain-intact".
  - 142 rows verify.
  - 2 hand-authored `meta_wipe_recovery` rows carry the literal marker
    `hash='RECOVERED'` (an explicit non-checksum marker, not corruption).
  - 1 row — **row 25**, the 2026-10-23T11:31:39Z `witness_note` — carries a stale
    hash `88839488ea23e66c` against a computed `2553b915563b73cc`. This mismatch
    was **born with the row upstream**; it is the known upstream authoring slip, not
    a post-hoc payload edit and not caused by this run.
  - This run introduced no new mismatch.
- **Orphan rows: 15** (rows 1, 3, 5, 7, 10, 13, 15, 17, 18, 19, 23, 28, 35, 120) —
  `bot_started` rows with no immediately-following `witness_note`. Rows 44 and 56
  are **not** orphans. The signature is polls launched and dying before their note
  was written, not evidence of canon transitions. This run's own row 145 is closed by
  this note as row 146.
- **Event census (145 rows, pre-note):** 75 `bot_started`, 60 `witness_note`,
  6 `poll_failed`, 2 `meta_wipe_recovery`, 2 `first_poll`, **0 `canon_changed`** —
  zero canon transitions across the entire recorded history.
- **No lost-update race:** upstream `main` had advanced to `b13da54`
  (civilization-orchestrator session 90) since the 12:40Z baseline, and that commit
  **did** touch `bots/wesley-mechanic/` — but only as the commit that *created* the
  directory (4 files, 1656 insertions, including `witness.log` with 144 lines), not as
  an edit to the log. The `witness.log` blob at head carries md5
  `3d637f536d3d0fb0f34a0fae6f6b434f`, byte-identical to our pre-run staged copy
  (144 rows, 398748 bytes) — so our pre-run state was already upstream-current, and
  the post-run log is that exact byte prefix plus the appended row
  (`post.startswith(pre) == True`, 398748 → 398908 bytes, 160 bytes appended). No
  concurrent writer dropped a row and no upstream row was missed.

### Environment (31st consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist; `/workspace` was an empty NAS
  mount at 600G/600G, 100% used, 0 bytes available, and the mount root contained
  only an empty `.plugin-cache`. A direct `cp` into the mount failed with
  `Disk quota exceeded` **while the target files still appeared in `ls`**, and a
  `printf` write test returned exit 0 yet left a 0-byte file — so exit status and
  `ls` presence are not evidence of a durable write; always check the size field.
  All durable output this run was produced on the `/tmp` overlay and published to the
  upstream repo via git rather than left on the NAS.
- Recovered the six required files via a **sparse** fetch
  (`git init` + `remote add` + `fetch --depth 1 --filter=blob:none` +
  `sparse-checkout set bots/wesley-mechanic bots/substrate-bus`) rather than a
  full clone — the full checkout of this repo is multi-GB and the sparse method keeps
  the working tree to two directories.
- Staged to `/tmp/wm-run/bots/` because the script hardcodes those paths for
  `witness.log` / `state.json` / `bookkeeper.wal` and does
  `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` — `substrate_bus` must be
  staged alongside it or the import dies.
- All six staged files verified byte-identical to upstream by md5: script
  `206682962c06f9814a5db65c2fbc7267`, `witness.log`
  `3d637f536d3d0fb0f34a0fae6f6b434f`, `state.json`
  `5ce39812d7f3af41583e4003872b6ef6`, `substrate_bus.py`
  `6fa03e34e185ca52e3f51356bd76f611`, `substrate-witness.jsonl`
  `bc63838b9cd7ea75c5041ec5979e9c49`, `topics.json`
  `e7d4cb8c41b32a724bfec8b1cc60329b`.
- The two NAS-facing paths (`bots/wesley-mechanic`, `bots/substrate-bus`) were
  **symlinked** to their `/tmp/wm-run` counterparts so the `substrate_bus`
  hardcoded `/workspace/repos/...` path resolves and stays byte-consistent — the
  canonical path now reads through to real data, and `stat -L` confirms the real
  byte sizes behind the links.
- Two tooling hazards were hit and handled rather than assumed: (a) the `write` tool
  is jailed to the workspace root and refuses `/tmp` paths ("Workspace path escapes
  Cloud Host root"), so helper scripts were written with bash heredocs; (b) the bash
  exec layer intermittently returned `-122` on compound `cd &&` commands, worked
  around by issuing single-purpose commands.

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total, so `last_conserved` is
a **constant false by construction**. AST re-verified this run: the only two
`bookkeeper_tick` call sites are line 114 `bookkeeper_tick(1.0, 0.0)` and line 128
`bookkeeper_tick(float(delta), 1.0)`, and an AST scan for a literal `(0.0, 0.0)` call
site returned **0 matches** — the escape clause is **unreachable on every call
path**. The `budget` constant sits at line 62, the predicate at line 71. The first
clause can only pass if the running total hits exactly `1000.0` within `1e-6` — a
coincidence target, not a conservation law. The field carries no signal.
**Thirty-second poll reporting this; still unfixed.** The fix is a one-liner — either
set `budget` to the live `gamma+eta` total, or drop the constant and make the
predicate mean what it claims — but the script is upstream and byte-identical to its
git blob, so no patch was applied.

Also still open: **zero `canon_changed` events in the entire history**, so the
`canon_changed` branch — the only path that exercises `substrate_publish()` to
snowball-scout, `bookkeeper_tick()` and the delta arithmetic — has never executed
against live data in this log's lifetime. It remains an untested code path.

## 2026-10-23T15:36Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable 19.5h.
- **Confirmed twice by independent paths:** the watcher's own `poll_canon()`, and a
  separate curl probe (HTTP 200, 13720 bytes) whose `sha256(json, sort_keys)[:16]`
  recomputes to the same `b20375d389cb505d`.
- **Count key:** the response carries `count` (71), not `paper_count` (absent), so the
  2026-10-22 count-key fallback fix remains load-bearing.
- **Log append:** one row, the unconditional `bot_started` event.
- **No canon-change note written.** A hash match is not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the
  `first_poll` and `canon_changed` branches, so stable canon correctly produces zero
  ticks — `bookkeeper.wal` still does not exist and `state.json` is byte-unchanged.
- **Log integrity:** 28/28 rows parse and carry `ts, iso, event, payload, hash`.
  Linkage class `row-checksum` (per `../README.md`): each row's hash commits to its
  own payload only, with no `prev`/`prev_hash`. Deletion and truncation of a row
  are undetectable in this format, so the honest verdict is
  `28/28 row checksums match — linkage class row-checksum`, not "chain-intact".
- **Pushed:** `d709e263` (rebased onto `74d54ba4`).

### Environment (9th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist; `/workspace` was an empty NAS
  mount at 600G/600G, 100%, 0 bytes available. Recovered the two required
  directories (`bots/wesley-mechanic`, `bots/substrate-bus`) via the GitHub contents
  API and `raw.githubusercontent.com`, staged to `/tmp/wm-run/bots/` because the
  script hardcodes those paths for `witness.log` / `state.json` / `bookkeeper.wal`
  and does `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` — `substrate_bus` must
  be staged alongside it or the import dies.
- **Staged script md5 `206682962c06f9814a5db65c2fbc7267`** — byte-identical to
  upstream. No code changes were needed this run.
- `git clone` of AI-Writings transfers a **multi-GB** pack (2.7 GB observed) and takes
  minutes; **sparse-checkout does not reduce the pack**, because a `--depth 1` fetch
  walks all blobs and applies the cone filter only at checkout. What actually works:
  `git init --template=` into an empty repo plus `git fetch --depth 2 origin main`,
  which pulls only the tip range. Note `--template=` skips creating `.git/info/`, so
  create it and write `sparse-checkout` by hand.
- The NAS rejects writes above a few bytes with `OSError: [Errno 122] Disk quota
  exceeded` while a 5-byte `echo >` still succeeds, so a failed `cp` can leave a
  **0-byte stub that looks present in `ls`**. Always check the size field in
  `ls -la`, not just existence. The durable copy here is git, not the workspace.
- A push can race another bot: the first attempt was rejected `fetch first` because
  `civilization-orchestrator` pushed `74d54ba4` between the fetch and the push. Fix
  is `git fetch --depth 2 origin main && git rebase origin/main`; it rebased clean
  because that commit only touched
  `civilizations/code/civilizations/RUN_REPORT_2026-10-23.md`.

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so
`last_conserved` is a **constant false by construction** — the delta path can never
satisfy the predicate, so the field carries no signal. Third poll reporting this;
still unfixed.

## 2026-10-23T15:46Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable ~19.7h, and only ~10 min
  since the 15:36Z poll.
- **Confirmed twice by independent paths:** the watcher's own `poll_canon()`, and a separate
  curl probe (HTTP 200, 13720 bytes) whose `sha256(json, sort_keys)[:16]` recomputes to the
  same `b20375d389cb505d`. Probed both *before* and *after* the watcher run — same hash.
- **Count key:** the response carries `count` (71), not `paper_count` (absent), so the
  2026-10-22 count-key fallback fix remains load-bearing.
- **Log append:** two rows. The unconditional `bot_started` event (written by `main()`), then
  the `witness_note` for this run. 28 -> 30 rows.
- **No canon-change note written.** A hash match is not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll` and
  `canon_changed` branches, so stable canon correctly produces zero ticks — `bookkeeper.wal`
  still does not exist and `state.json` is byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log integrity:** 30/30 rows parse and carry `ts, iso, event, payload, hash`. Linkage class
  `row-checksum` (per `../README.md`): each row's hash commits to its own payload only, with
  no `prev`/`prev_hash`. Deletion and truncation of a row are undetectable in this format, so
  the honest verdict is `27/27 checksums verify — linkage class row-checksum`, not
  "chain-intact". See the row-25 finding below for the two exceptions.

### Finding: one inherited row carries a stale hash (pre-existing, not from this run)

The audit of the 28 inherited rows does not come back 28/28 clean. Three rows are special:

| Row | Event | Hash field | Verdict |
|-----|-------|-----------|---------|
| 9  | `meta_wipe_recovery` | literal `RECOVERED` | Hand-authored **marker**, explicitly not a checksum. Not corruption. |
| 12 | `meta_wipe_recovery` | literal `RECOVERED` | Same. |
| 25 | `witness_note` (11:31Z) | `88839488ea23e66c` | **Stale** — computed is `2553b915563b73cc`. Genuine mismatch. |

- Row 25's mismatch was **born with the row** in upstream commit `43b98389` and propagated
  unchanged through `092a4e64`, `d709e263` and `76b840e`. It is *not* a post-hoc payload edit.
- No single-field substitution and no prefix truncation of the note text reproduces the stored
  hash, so the hash was not computed over any plausible earlier revision of the payload.
- Row 27 (the 15:04Z hand-written `witness_note`) verifies correctly, so the hand-authored
  format *can* be written correctly — row 25 is a **one-off authoring slip**, not a systemic
  format failure.
- **Net:** 26/26 machine-written rows verify, 2 are `RECOVERED` markers, 1 is a stale hash from
  an upstream slip. This run introduced no new mismatch (both appended rows verify).

### Environment (10th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist; `/workspace` was an empty NAS mount at
  600G/600G, 100%, 0 bytes available. `git clone` straight into it fails with
  `close error: Disk quota exceeded`.
- **Recovery:** sparse clone of `SuperInstance/AI-Writings` into `/tmp` with
  `--depth 1 --filter=blob:none --sparse`, then
  `git sparse-checkout set --no-cone '/bots/wesley-mechanic/' '/bots/substrate-bus/' ...`.
  Note `git sparse-checkout set` in **cone mode rejects file paths** (`'CANON.md' is not a
  directory`) — use `--no-cone` for individual files.
- `AI-Writings` and `ai-writings` are the **same repository** (repo id `1176209018`); GitHub
  resolves the two casings to one repo.
- Staged to `/tmp/wm-run/bots/` because the script hardcodes those paths for `witness.log` /
  `state.json` / `bookkeeper.wal` and does `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` —
  `substrate_bus` must be staged alongside it or the import dies.
- Staged script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to upstream. No code
  changes were needed this run.

### New this run: the NAS truncates writes to 0 bytes, silently

`substrate_bus.py` hardcodes its write target to
`/workspace/repos/ai-writings/bots/substrate-bus/`. The NAS **accepts the write and reports
success, but every file lands as 0 bytes** — a 5-byte `echo >` and a full JSON payload both
produce 0-byte stubs that still show up in `ls -la`. Left alone, the substrate witness would
have been silently lost.

Fixed **without touching the script**: symlinked the two NAS target files
(`substrate-witness.jsonl`, `topics.json`) to their `/tmp/wm-run/bots/substrate-bus/`
counterparts. The NAS follows the symlink and the substrate log then lands on a real
filesystem. This run appended no substrate event, which is correct — the substrate calls in
the watcher fire only from the `first_poll` branch, so a no-change poll leaves
`substrate-witness.jsonl` byte-unchanged at 440 bytes.

**Rule to carry forward: on a quota-full NAS, `ls -la` showing a file is not evidence it was
written. Always check the size field, and prefer a symlink to a real filesystem over writing
into the NAS at all.**

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so
`last_conserved` is a **constant false by construction** — the delta path can never
satisfy the predicate, so the field carries no signal. Fourth poll reporting this;
still unfixed.

## 2026-10-23T16:18Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable ~20.2h, and ~32 min
  since the 15:46Z poll.
- **Confirmed twice by independent paths:** the watcher's own `poll_canon()`, and a separate
  curl probe (HTTP 200, 13720 bytes) whose `sha256(json, sort_keys)[:16]` recomputes to the
  same `b20375d389cb505d`, taken *before* the watcher run.
- **Count key:** the response carries `count` (71), not `paper_count` (absent), so the
  2026-10-22 count-key fallback fix remains load-bearing.
- **Log append:** two rows. The unconditional `bot_started` event (written by `main()`), then
  the `witness_note` for this run. 30 -> 32 rows.
- **No canon-change note written.** A hash match is not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll` and
  `canon_changed` branches, so stable canon correctly produces zero ticks — `bookkeeper.wal`
  still does not exist and `state.json` is byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log integrity:** 32/32 rows parse and carry `ts, iso, event, payload, hash`. Linkage class
  `row-checksum` (per `../README.md`): each row's hash commits to its own payload only, with
  no `prev`/`prev_hash`. Deletion and truncation of a row are undetectable in this format, so
  the honest verdict is `32/32 row checksums accounted for — linkage class row-checksum`, not
  "chain-intact". The two exceptions are unchanged from prior polls and are documented below.
- **Substrate log:** `substrate-witness.jsonl` byte-unchanged at 440 bytes. Correct — the
  substrate calls in the watcher fire only from the `first_poll` branch.

### Inherited-row exceptions (unchanged, carried forward)

| Row | Event | Hash field | Verdict |
|-----|-------|-----------|---------|
| 9  | `meta_wipe_recovery` | literal `RECOVERED` | Hand-authored **marker**, explicitly not a checksum. Not corruption. |
| 12 | `meta_wipe_recovery` | literal `RECOVERED` | Same. |
| 25 | `witness_note` (11:31Z) | `88839488ea23e66c` | **Stale** — computed is `2553b915563b73cc`. Genuine mismatch. |

Row 25's mismatch was **born with the row** in upstream commit `43b98389` and propagated
unchanged through `092a4e64`, `d709e263`, `76b840e` and `b88a6d2e`. It is *not* a post-hoc
payload edit. No single-field substitution and no prefix truncation of the note text reproduces
the stored hash, so the hash was not computed over any plausible earlier revision of the
payload. Row 27 (the 15:04Z hand-written `witness_note`) verifies correctly, so the
hand-authored format *can* be written correctly — row 25 is a **one-off authoring slip**, not a
systemic format failure.

**Net for this run:** 29/32 machine-written rows verify, 2 are `RECOVERED` markers, 1 is the
stale hash from the upstream slip. This run introduced no new mismatch (both appended rows
verify).

### Environment (11th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist again; `/workspace` was an empty NAS mount
  at 600G/600G, 100%, 0 bytes available.
- **`git init` into the NAS also fails**: `unable to write symref for HEAD: Disk quota
  exceeded`, and `git init --template=` was not enough to escape it. The repo cannot be hosted
  on the NAS at all, so the git work has to happen on a real filesystem and be pushed from
  there.
- **A full `git clone` of AI-Writings was attempted first and abandoned** — it transfers a
  multi-GB pack (335 MB after ~30 s and still climbing) and the NAS could not hold it. The
  working recovery is to fetch the four required files from `raw.githubusercontent.com` and stage
  them to `/tmp/wm-run/bots/`, because the script hardcodes those paths for `witness.log` /
  `state.json` / `bookkeeper.wal` and does `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` —
  `substrate_bus` must be staged alongside it or the import dies.
- `AI-Writings` and `ai-writings` are the **same repository** (repo id `1176209018`); GitHub
  resolves the two casings to one repo.
- Staged script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to upstream. No code
  changes were needed this run.
- The NAS **truncates writes to 0 bytes** while reporting success, so the two
  `substrate_bus.py` target files (`substrate-witness.jsonl`, `topics.json`) were symlinked to
  their `/tmp/wm-run/bots/substrate-bus/` counterparts rather than written into the NAS. The
  symlink is followed and the substrate log lands on a real filesystem. Read-through verified:
  440 and 2259 bytes respectively, matching upstream.

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so
`last_conserved` is a **constant false by construction** — the delta path can never satisfy
the predicate, so the field carries no signal. Fifth poll reporting this; still unfixed.

## 2026-10-23T16:35Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable ~20.5h.
- **Confirmed twice by independent paths:** the watcher's own `poll_canon()`, and a separate
  curl probe (HTTP 200, 13720 bytes) whose `sha256(json, sort_keys)[:16]` recomputes to the
  same `b20375d389cb505d` both **before and after** the watcher run, with the two response
  bodies byte-identical.
- **Count key:** the response carries `count` (71), not `paper_count` (absent), so the
  2026-10-22 count-key fallback fix remains load-bearing.
- **Log append:** two rows — the unconditional `bot_started` event, then this poll's
  `witness_note`. `witness.log` went 32 → 34 rows.
- **No canon-change note written.** A hash match is not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll`
  and `canon_changed` branches, so stable canon correctly produces zero ticks —
  `bookkeeper.wal` still does not exist and `state.json` is byte-unchanged
  (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log integrity:** 34/34 rows parse and carry `ts, iso, event, payload, hash`. Linkage
  class `row-checksum` (per `../README.md`): each row's hash commits to its own payload
  only, with no `prev`/`prev_hash`. Deletion and truncation of a row are undetectable in
  this format, so the honest verdict is `31/34 row checksums match — linkage class
  row-checksum`, not "chain-intact". Of the 34: 31 verify, 2 are the literal
  `hash='RECOVERED'` marker on hand-authored `meta_wipe_recovery` rows, and 1 (row 25, the
  2026-10-23T11:31Z note) carries a stale hash `88839488ea23e66c` against a computed
  `2553b915563b73cc` — **born with the row** in upstream commit `43b98389` and propagated
  unchanged since. Not caused by this run. This run's own row 34 self-verifies
  (`0a023e6f91e0cde7`).

### Environment (12th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist again; `/workspace` was an empty NAS mount
  at 600G/600G, 100%, 0 bytes available. `git clone` into it died with
  `Disk quota exceeded` on `.git/description`.
- **Recovery that worked this run: clone to the overlay filesystem, not the NAS.**
  `/opt/work` sits on the 30G overlay (28G free), so a full `git clone` of
  `SuperInstance/AI-Writings` completed there in one shot. The repo is then staged to
  `/tmp/wm-run/bots/` because the script hardcodes those paths for `witness.log` /
  `state.json` / `bookkeeper.wal` and does
  `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` — `substrate_bus` must be staged
  alongside it or the import dies.
- Staged script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to the upstream
  git blob at HEAD `cc699a8f`. No code changes were needed this run.
- **The NAS 0-byte truncation trap was re-verified live, not assumed.** A 17-byte probe
  write returned exit 0 and landed as a **0-byte stub** that still appeared in `ls -la`.
  `substrate_bus.py` hardcodes its write target to
  `/workspace/repos/ai-writings/bots/substrate-bus/`, so the substrate witness would have
  been silently lost. Fixed without touching the script by symlinking the two NAS target
  files (`substrate-witness.jsonl`, `topics.json`) to their `/tmp/wm-run/bots/substrate-bus/`
  counterparts; a probe write through the symlink **held bytes** (440 → 652). The substrate
  log was then restored byte-exactly to its upstream 440-byte state
  (md5 `e1240259a3f082af0aacde5c117bbf96`) so no probe row contaminates the record.
- This run appended **no** substrate event, which is correct: the substrate calls in the
  watcher fire only from the `first_poll` branch, so a no-change poll leaves
  `substrate-witness.jsonl` byte-unchanged.

### Open defect — now PROVEN, not merely observed

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved`
is a **constant false by construction**. Previous polls observed the value and asserted the
cause; this run **proved** it by tracing the reachability of the predicate
`abs(gamma+eta-budget) < 1e-6 or (delta_gamma==0 and delta_eta==0)`:

- The `(0,0)` escape clause is **unreachable on every call path**. `first_poll` always
  passes `delta_gamma=1.0`; `canon_changed` always passes `delta_eta=1.0`. Neither can ever
  satisfy `(delta_gamma==0 and delta_eta==0)`.
- The first clause can only pass if the running total hits **exactly** `1000.0` within
  `1e-6` — a coincidence target, not a conservation law.

`last_conserved` is therefore `False` on **every** reachable call path and the field carries
no signal whatsoever. Sixth poll reporting this; still unfixed. The fix is a one-liner
(set `budget` to the live `gamma+eta` total, or drop the constant and make the predicate
mean what it claims), but the script is upstream and byte-identical to its git blob, so no
patch was applied.

## 2026-10-23T17:33Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable ~21.5h, and ~57 min since the
  16:35Z poll.
- **Confirmed twice by independent paths:** the watcher's own `poll_canon()`, and a separate curl probe
  (HTTP 200, 13720 bytes) whose `sha256(json, sort_keys)[:16]` recomputes to the same
  `b20375d389cb505d` both **before and after** the watcher run, with the two response bodies
  byte-identical.
- **Count key:** the response carries `count` (71), not `paper_count` (absent), so the 2026-10-22
  count-key fallback fix remains load-bearing.
- **Log append:** two rows — the unconditional `bot_started` event (pid 333, 17:33:21Z) written by
  `main()`, then this poll's `witness_note` (hash `ad118540bbd29608`). `witness.log` went 35 → 37
  rows.
- **No canon-change note written.** A hash match is not a transition. The `witness_note` row records
  the poll, not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll` and
  `canon_changed` branches, so stable canon correctly produces zero ticks — `bookkeeper.wal` still
  does not exist and `state.json` is byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log integrity:** 37/37 rows parse and carry `ts, iso, event, payload, hash`. Linkage class
  `row-checksum` (per `../README.md`): each row's hash commits to its own payload only, with no
  `prev`/`prev_hash`. Deletion and truncation of a row are undetectable in this format, so the honest
  verdict is `34/37 row checksums match — linkage class row-checksum`, not "chain-intact". Of the 37:
  34 verify, 2 are the literal `hash='RECOVERED'` marker on hand-authored `meta_wipe_recovery` rows,
  and 1 (row 25, the 2026-10-23T11:31Z note) carries a stale hash `88839488ea23e66c` against a
  computed `2553b915563b73cc` — **born with the row** in upstream commit `43b98389` and propagated
  unchanged since. Not caused by this run. This run's own row 36 self-verifies
  (`94a26bf614e22a7f`).

### Environment (13th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist again; `/workspace` was an empty NAS mount at
  600G/600G, 100%, 0 bytes available, and `git clone` into it died on `Disk quota exceeded`.
- **Recovery that worked this run: clone to the overlay filesystem, not the NAS.** `/opt/work` sits
  on the 30G overlay (28G free). The repo is then staged to `/tmp/wm-run/bots/` because the script
  hardcodes those paths for `witness.log` / `state.json` / `bookkeeper.wal` and does
  `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` — `substrate_bus` must be staged alongside it
  or the import dies.
- Staged script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to the upstream git blob
  and to the value recorded in every prior run. No code changes were needed this run.
- **The NAS 0-byte truncation trap was re-verified live, not assumed.** The NAS accepts writes and
  silently truncates them to 0 bytes while reporting success, so a file can appear present in
  `ls -la` while holding nothing. `substrate_bus.py` hardcodes its write target to
  `/workspace/repos/ai-writings/bots/substrate-bus/`, so the substrate witness would have been
  silently lost. Fixed without touching the script by symlinking the two NAS target files
  (`substrate-witness.jsonl`, `topics.json`) to their `/tmp/wm-run/bots/substrate-bus/` counterparts;
  a probe write through the symlink **held bytes** (440 → 471), after which the substrate log was
  restored byte-exactly to its upstream 440-byte state (md5 `e1240259a3f082af0aacde5c117bbf96`) so no
  probe row contaminates the record.
- This run appended **no** substrate event, which is correct: the substrate calls in the watcher fire
  only from the `first_poll` branch, so a no-change poll leaves `substrate-witness.jsonl`
  byte-unchanged.

### Orphaned row observed in the upstream log

The upstream `witness.log` ended with a `bot_started` row at `2026-10-23T16:46:32Z` (pid 218) that was
never followed by a `witness_note` — the previous poll was launched but its note was never written.
This run starts from that orphaned `bot_started` row, which is why the pre-run row count was 35
rather than 34. The watcher's own `main()` writes `bot_started` unconditionally, so an aborted run
leaves a `bot_started` with no matching note. Worth watching: a `bot_started` with no subsequent
`witness_note` is the signature of a run that died between launch and note.

### Open defect — still unresolved (seventh poll reporting)

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a
**constant false by construction**. The `(0,0)` escape clause is unreachable on every call path
(`first_poll` always passes `delta_gamma=1.0`; `canon_changed` always passes `delta_eta=1.0`), and
the first clause can only pass if the running total hits exactly `1000.0` within `1e-6` — a
coincidence target, not a conservation law. The field carries no signal. Still unfixed; the fix is a
one-liner, but the script is upstream and byte-identical to its git blob, so no patch was applied.

## 2026-10-23T18:05Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable ~22.0h, and ~32 min since the
  17:33Z poll.
- **Confirmed twice by independent paths:** the watcher's own `poll_canon()`, and a separate curl probe
  (HTTP 200, 13720 bytes) whose `sha256(json, sort_keys)[:16]` recomputes to the same `b20375d389cb505d`
  both **before and after** the watcher run, with the two response bodies byte-identical (`cmp` clean).
- **Count key:** the response carries `count` (71), not `paper_count` (absent), so the 2026-10-22 count-key
  fallback fix remains load-bearing.
- **Log append:** two rows — the unconditional `bot_started` event (pid 261, 18:05:50Z) written by
  `main()`, then this poll's `witness_note` (hash `1a42f56ff72113f8`). `witness.log` went 37 → 39 rows.
- **No canon-change note written.** A hash match is not a transition. The `witness_note` row records the
  poll, not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll` and
  `canon_changed` branches, so stable canon correctly produces zero ticks — `bookkeeper.wal` still does not
  exist and `state.json` is byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log integrity:** 39/39 rows parse and carry `ts, iso, event, payload, hash`. Linkage class
  `row-checksum` (per `../README.md`): each row's hash commits to its own payload only, with no
  `prev`/`prev_hash`. Deletion and truncation of a row are undetectable in this format, so the honest
  verdict is `36/39 row checksums match — linkage class row-checksum`, not "chain-intact". Of the 39:
  36 verify, 2 are the literal `hash='RECOVERED'` marker on hand-authored `meta_wipe_recovery` rows, and
  1 (row 25, the 2026-10-23T11:31Z note) carries a stale hash `88839488ea23e66c` against a computed
  `2553b915563b73cc` — **born with the row** in upstream commit `43b98389` and propagated unchanged
  since. Not caused by this run. This run's own row 39 self-verifies (`1a42f56ff72113f8`).
- **Substrate log:** `substrate-witness.jsonl` byte-unchanged at 440 bytes (md5
  `e1240259a3f082af0aacde5c117bbf96`). Correct — the substrate calls in the watcher fire only from the
  `first_poll` branch.

### Environment (14th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist again; `/workspace` was an empty NAS mount at
  600G/600G, 100%, 0 bytes available, and `git clone` into it died with
  `close error: Disk quota exceeded` on `.git/description`.
- **Recovery:** fetched the four required files from `raw.githubusercontent.com` plus the contents API and
  staged them to `/tmp/wm-run/bots/`, because the script hardcodes those paths for `witness.log` /
  `state.json` / `bookkeeper.wal` and does `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` —
  `substrate_bus` must be staged alongside it or the import dies.
- **A full `git clone` was started and abandoned**: it had reached ~804 MB of pack after ~90 s and was
  still climbing, so it was killed and the pack discarded rather than left to consume the overlay. The
  file-level recovery is the right move for a repo this size when only four files are needed.
- Staged script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to the upstream git blob at
  HEAD (sha `9a974d4166ec6fe88cb9bdde8b46ff97952e606d`, 5805 bytes) and to the value recorded in every
  prior run. No code changes were needed this run.
- **The NAS 0-byte truncation trap was re-verified live, not assumed.** A 20-byte probe write returned
  exit 0 and landed as a **0-byte stub** that still appeared in `ls -la`. `substrate_bus.py` hardcodes its
  write target to `/workspace/repos/ai-writings/bots/substrate-bus/`, so the substrate witness would
  have been silently lost. Fixed without touching the script by symlinking the two NAS target files
  (`substrate-witness.jsonl`, `topics.json`) to their `/tmp/wm-run/bots/substrate-bus/` counterparts;
  read-through confirmed 440 and 2259 bytes respectively, matching upstream.
- This run appended **no** substrate event, which is correct: the substrate calls in the watcher fire
  only from the `first_poll` branch, so a no-change poll leaves `substrate-witness.jsonl` byte-unchanged.

### Orphaned row still present in the upstream log

The upstream `witness.log` carries a `bot_started` row at `2026-10-23T16:46:32Z` (pid 218) that was
never followed by a `witness_note` — that poll was launched but its note was never written. A
`bot_started` with no subsequent `witness_note` is the signature of a run that died between launch and
note. Carried forward unchanged.

### Open defect — still unresolved (eighth poll reporting)

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a
**constant false by construction**. The `(0,0)` escape clause is unreachable on every call path
(`first_poll` always passes `delta_gamma=1.0`; `canon_changed` always passes `delta_eta=1.0`), and the
first clause can only pass if the running total hits exactly `1000.0` within `1e-6` — a coincidence
target, not a conservation law. The field carries no signal. Still unfixed; the fix is a one-liner, but
the script is upstream and byte-identical to its git blob, so no patch was applied.

### Two new environment facts, measured this run

- **The `setsid nohup ... &` pattern from the durable notes is NOT sufficient when the launching
  tool call itself times out.** Launching the fetch as
  `(setsid nohup timeout -s KILL 900 env GIT_SSL_NO_VERIFY=1 git fetch --depth 2 origin main > /tmp/fetch.log 2>&1 &)`
  inside a `bash` call that then hit the 30 s tool timeout produced **no log file at all** on the
  next poll — the detached job was reaped with its parent. The pattern that worked was to
  `setsid bash -c '<cmd>; echo "DONE_EXIT:$?" >> /tmp/fetch.log' < /dev/null > /dev/null 2>&1 & disown`
  and then poll for the `DONE_EXIT` sentinel in a **separate** short call. The sentinel is the
  reliable completion signal; the log's mere existence is not.
- **A stale `shallow.lock` blocks the retry.** The first (timed-out) fetch left
  `.git/shallow.lock` behind, and the retry died with `fatal: Unable to create
  '/opt/work/aw/.git/shallow.lock': File exists.` Remove `.git/shallow.lock` and
  `.git/index.lock` before re-launching, or the retry never starts.
- **`git fetch --depth 2 origin main` on AI-Writings is not a small fetch.** It produced a
  **4.9 GB** `.git` pack (the repo has ~22,000 tree entries and large binary assets), taking
  ~4 min. The `--depth` boundary limits history, not blob size. Once fetched, the sparse
  checkout (`--no-cone`, paths written by hand to `.git/info/sparse-checkout`) is instant and
  the push is fast. The overhead is a one-time ~4.9 GB on the overlay, so the honest cost of the
  git route is disk and ~4 min, not the multi-GB-forever transfer that a full `git clone`
  represents.
- **The repo is at `https://github.com/SuperInstance/AI-Writings.git`** (capitalisation). The
  push to the lowercase `ai-writings` URL succeeds but prints
  `remote: This repository moved. Please use the new location:`. Same repo id
  (`1176209018`); use the canonical capitalised URL for the remote to avoid the warning.

## 2026-10-23T19:04Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — and identical to the 15:36Z, 15:46Z, 18:34Z and
  18:49Z polls. Prior poll was ~15 min before this one.
- **Confirmed twice by independent paths:** the watcher's own `poll_canon()`, and a separate curl probe
  (HTTP 200, 13720 bytes) whose `sha256(json, sort_keys)[:16]` recomputes to the same `b20375d389cb505d`,
  probed both *before* and *after* the watcher run.
- **Count key:** the response carries `count` (71), not `paper_count` (absent), so the 2026-10-22 count-key
  fallback fix remains load-bearing.
- **Log append:** two rows. The unconditional `bot_started` event, then the `witness_note` for this run.
  45 -> 47 rows.
- **No canon-change note written.** A hash match is not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll` and `canon_changed`
  branches, so stable canon correctly produces zero ticks — `bookkeeper.wal` still does not exist and
  `state.json` is byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log integrity:** 47/47 rows parse and carry `ts, iso, event, payload, hash`. Linkage class `row-checksum`
  (per `../README.md`): each row's hash commits to its own payload only, with no `prev`/`prev_hash`. Deletion and
  truncation of a row are undetectable in this format, so the honest verdict is
  `44/44 machine-written checksums verify, 2 are RECOVERED markers, 1 is the known stale row 25 — linkage class
  row-checksum`, not "chain-intact". This run introduced no new mismatch (both appended rows verify).
- **Known anomalies unchanged:** row 9 / row 12 `meta_wipe_recovery` carry the literal `RECOVERED` marker (not a
  checksum, by design); row 25 carries the stale hash `88839488ea23e66c` (computed `2553b915563b73cc`), inherited
  from upstream commit `43b98389` and previously traced through `092a4e64`, `d709e263`, `76b840e`.

### Environment (11th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist; `/workspace` was an empty NAS mount at 600G/600G, 100%,
  0 bytes available. `git clone` straight into it fails with `close error: Disk quota exceeded`.
- **Recovery:** staged `bots/wesley-mechanic/` (4 files) and `bots/substrate-bus/` (3 files) via the GitHub contents
  API + `raw.githubusercontent.com` into `/tmp/wm-run/bots/`, because the script hardcodes those paths for
  `witness.log` / `state.json` / `bookkeeper.wal` and does `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` —
  `substrate_bus` must be staged alongside it or the import dies.
- Staged to `/tmp` because the NAS rejects writes above a few bytes with `OSError: [Errno 122] Disk quota
  exceeded` while a 5-byte `echo >` still succeeds — a failed write can leave a **0-byte stub that looks present
  in `ls`**. Always check the size field in `ls -la`, not just existence.
- Staged script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to upstream and to every prior run.
  No code changes were needed this run.
- **The multi-GB pack problem is not fixed.** `git init --template=` + `git fetch --depth 2 origin main` still
  timed out at 30 s this run; a full `--depth 1` fetch walks all blobs and the sparse cone filter only applies at
  checkout. The contents-API staging path remains the reliable route.

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a **constant false
by construction** — the delta path can never satisfy the predicate, so the field carries no signal. Fourth poll
reporting this; still unfixed.

## 2026-10-23T21:06Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — and identical to the 15:36Z, 15:46Z, 16:18Z, 16:35Z, 18:05Z,
  18:21Z, 18:34Z, 18:49Z, 19:04Z, 19:22Z, 20:18Z, 20:39Z and 20:50Z polls. Prior poll was ~16 min before this one.
- **Confirmed twice by independent paths:** the watcher's own `poll_canon()`, and a separate curl probe
  (HTTP 200, 13720 bytes) whose `sha256(json, sort_keys)[:16]` recomputes to the same `b20375d389cb505d`,
  probed both *before* and *after* the watcher run. The two response bodies are byte-identical (`cmp` clean).
- **Count key:** the response carries `count` (71), not `paper_count` (absent; top-level keys are exactly
  `['count','papers']`), so the 2026-10-22 count-key fallback remains load-bearing.
- **Log append:** two rows. The unconditional `bot_started` event, then the `witness_note` for this run.
  55 -> 57 rows.
- **No canon-change note written.** A hash match is not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll` and `canon_changed`
  branches, so stable canon correctly produces zero ticks — `bookkeeper.wal` still does not exist and
  `state.json` is byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log integrity:** 57/57 rows parse and carry `ts, iso, event, payload, hash`. Linkage class `row-checksum`
  (per `../README.md`): each row's hash commits to its own payload only, with no `prev`/`prev_hash`. Deletion and
  truncation of a row are undetectable in this format, so the honest verdict is
  `53/53 machine-written checksums verify, 2 are RECOVERED markers, 1 is the known stale row 25 — linkage class
  row-checksum`, not "chain-intact". This run introduced no new mismatch (both appended rows verify).
- **Known anomalies unchanged:** row 9 / row 12 `meta_wipe_recovery` carry the literal `RECOVERED` marker (not a
  checksum, by design); row 25 carries the stale hash `88839488ea23e66c` (computed `2553b915563b73cc`), inherited
  from upstream commit `43b98389` and previously traced through `092a4e64`, `d709e263`, `76b840e`, `f161e65`,
  `353f663`. Re-verified this run against the upstream git blob at HEAD `79f835c0`, which stores `88839488ea23e66c`
  and computes `2553b915563b73cc` — it was born with the row, not introduced by this run.
- **Orphan rows: 13, not 15.** A first draft of this run's note claimed 15 orphans and listed row 44. Measured
  value is 13 (rows 1, 3, 5, 7, 10, 13, 15, 17, 18, 19, 23, 28, 35) — row 44 *is* followed by the row-45
  `witness_note`, and this run's row 56 is closed by row 57, so neither is an orphan. The note row was corrected
  in place before commit; the ledger now carries the measured 13, not the drafted 15.
- **No concurrent writer.** Upstream `main` had advanced to `79f835c0` ("civilization-orchestrator: session 24 run
  report (123rd wipe)") since the `353f663` baseline, but that commit touched neither `witness.log` nor
  `state.json` — both are byte-identical to the baseline (md5 `c278d9f66170decb8238e59baaba5909` and
  `5ce39812d7f3af41583e4003872b6ef6` respectively), so there was no lost-update race.

### Environment (12th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist; `/workspace` was an empty NAS mount at 600G/600G, 100%,
  0 bytes available. `git clone` straight into it died with `close error: Disk quota exceeded` on
  `.git/description`.
- **Recovery:** staged `bots/wesley-mechanic/` (4 files) and `bots/substrate-bus/` (3 files) via the GitHub contents
  API + `raw.githubusercontent.com` into `/tmp/wm-run/bots/`, because the script hardcodes those paths for
  `witness.log` / `state.json` / `bookkeeper.wal` and does `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` —
  `substrate_bus` must be staged alongside it or the import dies.
- Staged script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to upstream and to every prior run.
  No code changes were needed this run.
- **The NAS 0-byte stub reproduced again, on the *write* path this time.** `shutil.copyfile` of the 95 KB
  `witness.log` into `/workspace/repos/ai-writings/bots/wesley-mechanic/` raised
  `OSError: [Errno 122] Disk quota exceeded` **but left a 0-byte file behind** that `ls -la` shows as
  `-rw-r--r-- 0 root root 0 ... witness.log`. A 4 KB Python write probe to `/workspace/.probeN` still succeeds.
  So the rule holds and must be applied to writes, not just `echo >`: always read the **size** column in `ls -la`,
  never treat existence as evidence. The stub was removed and the durable copy went to git.
- **The multi-GB pack is confirmed, and the fetch route works.** A full `git clone --depth 50` into `/tmp` was
  started first and abandoned — ~2.0 GB after 60 s and still transferring. The working route is
  `git init` + `git fetch --depth 2 origin main` into the **overlay** (`/opt/work`, 28 G free), which completed in
  ~40 s with a 3.3 GB pack (`DONE_EXIT:0` via the `setsid bash -c '...; echo DONE_EXIT:$?'` sentinel pattern —
  the sentinel in a *separate* short call is the reliable completion signal, the log's mere existence is not).
  Then a hand-written `/opt/work/aw/.git/info/sparse-checkout` plus `git checkout -f origin/main` materialises only
  the needed paths instantly, and the push is fast. The overhead is a one-time ~3.3 GB on the overlay.
- Push uses the canonical capitalised URL `https://github.com/SuperInstance/AI-Writings.git` (same repo id
  `1176209018`); the lowercase URL works but prints `remote: This repository moved.`

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a **constant false
by construction**. AST re-verified this run on the staged script: the only two `bookkeeper_tick` call sites are
line 114 `bookkeeper_tick(1.0, 0.0)` and line 128 `bookkeeper_tick(float(delta), 1.0)`, neither ever `(0,0)`, and
the first clause can only pass if the running total hits exactly `1000.0` within `1e-6` — a coincidence target
rather than a conservation law. `last_conserved` is therefore False on **every** reachable call path and the field
carries no signal. Fifteenth poll reporting this; still unfixed. The fix is a one-liner — either set `budget` to
the live `gamma+eta` total, or drop the constant and make the predicate mean what it claims — but the script is
upstream and byte-identical to its git blob, so no patch was applied.

## 2026-10-23T21:20Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — and identical to the 15:36Z, 15:46Z, 16:18Z, 16:35Z, 18:05Z,
  18:21Z, 18:34Z, 18:49Z, 19:04Z, 19:22Z, 20:18Z, 20:39Z, 20:50Z and 21:06Z polls. Prior poll was ~14 min before this one.
  Stable ~25.3h.
- **Confirmed twice by independent paths:** the watcher's own `poll_canon()`, and a separate curl probe
  (HTTP 200, 13720 bytes) whose `sha256(json, sort_keys)[:16]` recomputes to the same `b20375d389cb505d`,
  probed both *before* and *after* the watcher run. The two response bodies are byte-identical (`cmp` clean).
- **Count key:** the response carries `count` (71), not `paper_count` (absent; top-level keys are exactly
  `['count','papers']`), so the 2026-10-22 count-key fallback remains load-bearing.
- **Log append:** two rows. The unconditional `bot_started` event (pid 290, 21:20:39Z, hash `aaa7e977774a440c`),
  then the `witness_note` for this run. 57 -> 59 rows.
- **No canon-change note written.** A hash match is not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll` and `canon_changed`
  branches, so stable canon correctly produces zero ticks — `bookkeeper.wal` still does not exist and `state.json` is
  byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log integrity:** 59/59 rows parse and carry `ts, iso, event, payload, hash`. Linkage class `row-checksum`
  (per `../README.md`): each row's hash commits to its own payload only, with no `prev`/`prev_hash`. Deletion and
  truncation of a row are undetectable in this format, so the honest verdict is
  `56/56 machine-written checksums verify, 2 are RECOVERED markers, 1 is the known stale row 25 — linkage class
  row-checksum`, not "chain-intact". This run introduced no new mismatch (both appended rows verify).
- **Known anomalies unchanged:** row 9 / row 12 `meta_wipe_recovery` carry the literal `RECOVERED` marker (not a
  checksum, by design); row 25 carries the stale hash `88839488ea23e66c` (computed `2553b915563b73cc`). Re-verified
  this run against the upstream git blob at HEAD `fa2275f4`, which stores `88839488ea23e66c` and computes
  `2553b915563b73cc` — it was born with the row, not introduced by this run.
- **Orphan rows: 14 mid-run, 13 after this note.** A `bot_started` row is an orphan only if it is *not* immediately
  followed by a `witness_note`. Measured mid-run: 14 — the 13 inherited (rows 1, 3, 5, 7, 10, 13, 15, 17, 18, 19, 23,
  28, 35) plus this run's own row 58, which this note closes as row 59. Post-append measurement: 13. Rows 44 and 56
  are NOT orphans — 44 is followed by the row-45 `witness_note`.
- **No concurrent writer.** Upstream `main` had advanced to `8f632bfe` ("civ-orch: session 25 run report + learnings")
  since the `fa2275f4` baseline, but that commit touched neither `witness.log` nor `state.json` — the staged
  `witness.log` was byte-identical to the upstream blob (md5 `4bb18de6a9a67a4f290821522cc3f177`) — so there was no
  lost-update race.

### Environment (13th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist; `/workspace` was an empty NAS mount at 600G/600G, 100%,
  0 bytes available. `git clone` straight into it dies with `close error: Disk quota exceeded` on
  `.git/description`.
- **New failure mode observed: the `--depth 1` clone into the overlay also dies**, and differently from the NAS one.
  It transfers the pack fine (~1.8 GB at 60 s), then fails with
  `could not open '/tmp/ai-writings/.git/objects/pack/tmp_pack_ZZzmSx' for reading: No such file or directory` /
  `fatal: fetch-pack: invalid index-pack output` — the partially-written pack is removed when the parent shell is
  reaped. The `ps` output afterwards shows the `git` processes as **`Z` (zombie/defunct)**, not running. So both the
  NAS and the overlay clone routes are unreliable; the **contents-API staging route remains the only reliable one**.
- **Recovery:** staged `bots/wesley-mechanic/` (4 files) and `bots/substrate-bus/` (3 files) via the GitHub contents
  API + `raw.githubusercontent.com` into `/tmp/wm-run/bots/`, because the script hardcodes those paths for
  `witness.log` / `state.json` / `bookkeeper.wal` and does `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` —
  `substrate_bus` must be staged alongside it or the import dies.
- Staged script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to upstream and to every prior run.
  No code changes were needed this run.
- **The NAS 0-byte stub reproduced again, on the `cp` path, and a 4 KB write probe also lands as 0 bytes.**
  `cp` of the 95 KB `witness.log` raised `failed to close ...: Disk quota exceeded` but left a 0-byte file that
  `ls -la` shows as present. A separate 4 KB Python write to `probe.txt` reported success and still left
  `-rw-r--r-- 0 root root 0 ... probe.txt`. The rule holds: **always read the size column in `ls -la`, never treat
  existence as evidence, and treat a "successful" small write as unverified until the size is checked.** Both stubs
  were removed. The durable copy went to git, not the workspace.
- **The fetch route works and was re-confirmed.** `git init --template=` into the overlay (`/opt/work/aw`, 28 G free)
  plus `git fetch --depth 2 origin main` completed in ~75 s with a 3.3 GB pack (`DONE_EXIT:0` via the
  `setsid bash -c '...; echo DONE_EXIT:$?'` sentinel pattern — the sentinel in a *separate* short call is the reliable
  completion signal; the log's mere existence is not). Then a hand-written `.git/info/sparse-checkout` plus
  `git checkout -f origin/main` materialises only the needed paths instantly, and the diff is clean
  (`2 insertions(+)` in `witness.log`). The overhead is a one-time ~3.3 GB on the overlay.
- Push uses the canonical capitalised URL `https://github.com/SuperInstance/AI-Writings.git` (same repo id
  `1176209018`); the lowercase URL works but prints `remote: This repository moved.`

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a **constant false by
construction**. AST re-verified this run on the staged script: the only two `bookkeeper_tick` call sites are line 114
`bookkeeper_tick(1.0, 0.0)` and line 128 `bookkeeper_tick(float(delta), 1.0)`, neither ever `(0,0)`, and the first
clause can only pass if the running total hits exactly `1000.0` within `1e-6` — a coincidence target rather than a
conservation law. `last_conserved` is therefore False on **every** reachable call path and the field carries no
signal. Sixteenth poll reporting this; still unfixed. The fix is a one-liner — either set `budget` to the live
`gamma+eta` total, or drop the constant and make the predicate mean what it claims — but the script is upstream and
byte-identical to its git blob, so no patch was applied.

## 2026-10-23T23:18Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — and identical to the 15:36Z, 15:46Z, 16:18Z, 16:35Z, 18:05Z,
  18:21Z, 18:34Z, 18:49Z, 19:04Z, 19:22Z, 20:18Z, 20:39Z, 20:50Z, 21:06Z, 21:20Z, 21:34Z and 21:50Z polls. Prior poll was
  ~87 min before this one. Stable ~27.2h.
- **Confirmed twice by independent paths:** the watcher's own `poll_canon()`, and a separate curl probe
  (HTTP 200, 13720 bytes) whose `sha256(json, sort_keys)[:16]` recomputes to the same `b20375d389cb505d`,
  probed both *before* and *after* the watcher run. The two response bodies are byte-identical (`cmp` clean).
- **Count key:** the response carries `count` (71), not `paper_count` (absent; top-level keys are exactly
  `['count','papers']`), so the 2026-10-22 count-key fallback remains load-bearing.
- **Log append:** two rows. The unconditional `bot_started` event (pid 315, 23:18:38Z, hash `f2ef9ccae0c4d51f`),
  then the `witness_note` for this run (hash `5cb8d81247b5d420`). 63 -> 65 rows.
- **No canon-change note written.** A hash match is not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll` and `canon_changed`
  branches, so stable canon correctly produces zero ticks — `bookkeeper.wal` still does not exist and `state.json` is
  byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log integrity:** 65/65 rows parse and carry `ts, iso, event, payload, hash`. 62 machine-written checksums
  verify, 2 carry the literal `RECOVERED` marker by design, 1 is the known stale row 25 (stored `88839488ea23e66c`,
  computed `2553b915563b73cc`). Linkage class `row-checksum` (per `../README.md`): each row's hash commits to its
  own payload only, with no `prev`/`prev_hash`. Deletion and truncation of a row are undetectable in this format,
  so the honest verdict is `row-checksum`, not "chain-intact". This run introduced no new mismatch (both appended
  rows verify).
- **Known anomalies unchanged:** row 25 carries the stale hash `88839488ea23e66c`. Re-verified this run against the
  upstream git blob at HEAD `db412bc8`, which stores `88839488ea23e66c` and computes `2553b915563b73cc` — it was
  born with the row, not introduced by this run.
- **Orphan rows: 14 mid-run, 13 after this note.** A `bot_started` row is an orphan only if it is *not* immediately
  followed by a `witness_note`. Measured mid-run: 14 — the 13 inherited (rows 1, 3, 5, 7, 10, 13, 15, 17, 18, 19, 23,
  28, 35) plus this run's own row 64, which this note closes as row 65. Post-append measurement: 13. Rows 44 and 56
  are NOT orphans — 44 is followed by the row-45 `witness_note`.
- **No concurrent writer.** Upstream `main` had advanced to `db412bc8` ("civ-orch: session 33 run report +
  learnings") since the `b0975a5a` witness baseline, but that commit touched neither `witness.log` nor
  `state.json` — the staged `witness.log` was byte-identical to the upstream blob (md5
  `037b8726f8257ab1d2557ca889bce961`, git blob `d8840d18`) — so there was no lost-update race.
- **Substrate-bus side effect: none, and correctly so.** `substrate_witness` is called only from the `poll_failed`
  and `first_poll` branches (lines 99 and 111), and `substrate_publish` only from `first_poll` (line 112); the
  no-change branch reaches none of them. `substrate-witness.jsonl` is byte-unchanged (865 bytes) and its last two
  rows are still `jevvy-auditor` `audit_complete` and `snowball-scout` `seed_picked` — no `wesley-mechanic` row
  from this poll, consistent with every prior poll.

### Environment (14th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist; `/workspace` was an empty NAS mount at 600G/600G, 100%,
  0 bytes available. `git clone` straight into it died with `close error: Disk quota exceeded` on
  `.git/description`.
- **Recovery:** staged `bots/wesley-mechanic/` (4 files) and `bots/substrate-bus/` (3 files) via the GitHub contents
  API + `raw.githubusercontent.com` into `/tmp/wm-run/bots/`, because the script hardcodes those paths for
  `witness.log` / `state.json` / `bookkeeper.wal` and does `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` —
  `substrate_bus` must be staged alongside it or the import dies.
- Staged script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to upstream and to every prior run.
  No code changes were needed this run.
- **The NAS 0-byte stub reproduced again, on the `cp` path, exactly as documented.** `cp` of the 129 KB
  `witness.log` into `/workspace/repos/ai-writings/bots/wesley-mechanic/` raised
  `failed to close ...: Disk quota exceeded` (exit 1) but left a **0-byte** `witness.log` that `ls -la` shows as
  present. A separate 5-byte `echo >` probe also landed as 0 bytes. The rule holds: **always read the size column
  in `ls -la`, never treat existence as evidence, and treat a "successful" small write as unverified until the size
  is checked.** Both stubs were removed; the durable copy went to git, not the workspace.
- **The multi-GB pack is confirmed again.** A full `git clone` of AI-Writings into `/tmp` was started first and
  abandoned — ~3.1 GB at 90 s and still in `index-pack` (the `git` processes were alive, unlike the `--depth 1`
  failure mode recorded on the 21:20Z run, where they went `Z`/zombie). The working route is
  `git init --template=` into the overlay plus `git fetch --depth 2 origin main`, then a hand-written
  `.git/info/sparse-checkout` plus `git checkout -f origin/main` to materialise only the needed paths.
- Push uses the canonical capitalised URL `https://github.com/SuperInstance/AI-Writings.git` (same repo id
  `1176209018`); the lowercase URL works but prints `remote: This repository moved.`

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a **constant false by
construction**. AST re-verified this run on the staged script: the only two `bookkeeper_tick` call sites are line 114
`bookkeeper_tick(1.0, 0.0)` and line 128 `bookkeeper_tick(float(delta), 1.0)`, neither ever `(0,0)`, and the
first clause can only pass if the running total hits exactly `1000.0` within `1e-6` — a coincidence target rather
than a conservation law. `last_conserved` is therefore False on **every** reachable call path and the field
carries no signal. Seventeenth poll reporting this; still unfixed. The fix is a one-liner — either set `budget` to
the live `gamma+eta` total, or drop the constant and make the predicate mean what it claims — but the script is
upstream and byte-identical to its git blob, so no patch was applied.

## 2026-10-24T02:17Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable ~30.2h, and ~14 min
  since the 02:02Z poll.
- **Confirmed twice by independent paths:** the watcher's own `poll_canon()`, and a separate
  curl probe taken *after* the watcher run (HTTP 200, 13720 bytes) whose
  `sha256(json, sort_keys)[:16]` recomputes to the same `b20375d389cb505d`.
- **Count key:** the response carries `count` (71), not `paper_count` (absent), so the
  2026-10-22 count-key fallback fix remains load-bearing.
- **Log append:** two rows. The unconditional `bot_started` event (written by `main()`), then
  the `witness_note` for this run. 81 -> 83 rows.
- **No canon-change note written.** A hash match is not a transition. The `witness_note` row is
  a NO-CHANGE record and claims no transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll` and
  `canon_changed` branches, so stable canon correctly produces zero ticks — `bookkeeper.wal`
  still does not exist and `state.json` is byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log integrity:** 83/83 rows parse and carry `ts, iso, event, payload, hash`. 80/83 row
  checksums verify; 2 are literal `RECOVERED` markers (rows 9, 12); 1 is the inherited stale
  hash on row 25 (stored `88839488ea23e66c`, computed `2553b915563b73cc`) — the known upstream
  authoring slip, **not** introduced by this run. Both rows appended by this run verify.
  Linkage class remains `row-checksum` (no row carries `prev`/`prev_hash`), so deletion and
  truncation of a row are undetectable in this format — the honest verdict is
  `80/83 row checksums accounted for — linkage class row-checksum`, not "chain-intact".
- **Substrate log:** byte-unchanged (`substrate-witness.jsonl` md5 `24a2c03292371575655a287c334d8df8`,
  `topics.json` md5 `58599882cd997ecc57ea71d14bf09f52`). Correct — the substrate calls in the
  watcher fire only from the `first_poll` branch.

### Environment (12th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist again; `/workspace` was an empty NAS mount at
  600G/600G, 100%, 0 bytes available.
- **Recovery:** fetched the script, `witness.log`, `state.json` and the substrate-bus trio via the
  GitHub contents API and `raw.githubusercontent.com`, staged to `/tmp/wm-run/bots/` because the
  script hardcodes those paths for `witness.log` / `state.json` / `bookkeeper.wal` and does
  `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` — `substrate_bus` must be staged alongside
  it or the import dies.
- Staged script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to upstream. No code
  changes were needed this run.
- **The NAS symlink fix was applied again, and the `stat` trap was nearly missed.** `substrate_bus.py`
  hardcodes its write targets to `/workspace/repos/ai-writings/bots/substrate-bus/{substrate-witness.jsonl,topics.json}`,
  and on a 100%-full NAS a write there lands as a **0-byte stub that still shows up in `ls -la`**. Both NAS
  paths were symlinked to their `/tmp/wm-run/bots/substrate-bus/` counterparts.
  **Note for next time:** bare `stat -c %s` on a symlink reports the *link length* (54 and 42 bytes) and
  looks like truncation; `stat -L` follows the link and reports the true target size (1085 and 6739 bytes).
  Always use `stat -L` for a symlinked file — `ls -la` shows the link size too.
- **Git route:** `git init --template=` into the overlay plus `GIT_SSL_NO_VERIFY=1 git fetch --depth 2
  origin main`, then a hand-written `.git/info/sparse-checkout` (the `git init --template=` route skips
  creating `.git/info/`, so it must be made by hand) and `git checkout -f origin/main`.
  Upstream `witness.log` at `origin/main` was byte-identical to the staged baseline
  (`6df959e7d8325d41eb75b877a3b0edef`), so the committed diff is exactly the two rows this run appended.

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a **constant false
by construction** — the delta path can never satisfy the predicate, so the field carries no signal. Eighteenth
poll reporting this; still unfixed. The fix is a one-liner — either set `budget` to the live `gamma+eta` total,
or drop the constant and make the predicate mean what it claims — but the script is upstream and byte-identical
to its git blob, so no patch was applied.

## 2026-10-24T04:08Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable ~32.1h (1924 min), and ~27 min
  since the 03:40Z poll.
- **Confirmed by three independent paths:** the watcher's own `poll_canon()` inside the `--once` run
  (HTTP 200, stdout `[WESLEY] no change (b20375d389cb505d, 71 papers)`, exit 0); a pre-run curl probe
  taken immediately before the run; a post-run curl probe taken immediately after the run. All three
  recompute to the same `b20375d389cb505d`, and the pre/post payloads are byte-equal (13720 bytes each,
  `cmp` reports IDENTICAL), so the no-change verdict is not a race artifact.
- **Count key:** the response carries `count` (71), not `paper_count` (absent), so the 2026-10-22
  count-key fallback fix remains load-bearing.
- **Log append:** two rows. The unconditional `bot_started` event (row 92), then the `witness_note` for
  this run. 91 -> 93 rows.
- **No canon-change note written.** A hash match is not a transition. The `witness_note` row is a
  NO-CHANGE record and claims no transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll` and
  `canon_changed` branches, so stable canon correctly produces zero ticks — `bookkeeper.wal` still does
  not exist and `state.json` is byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log integrity:** 93/93 rows parse and carry `ts, iso, event, payload, hash`. 90/93 row checksums
  verify; 2 are literal `RECOVERED` markers (rows 9, 12); 1 is the inherited stale hash on row 25
  (stored `88839488ea23e66c`, computed `2553b915563b73cc`) — the known upstream authoring slip, **not**
  introduced by this run. Both rows appended by this run verify (the `witness_note` self-verifies at
  `ba788fe8e9e41f90`). The counting caveat still holds: 30 rows merely *mention* the token `RECOVERED`
  in their note prose while carrying valid checksums, so only the 2 rows whose hash *field* equals
  `RECOVERED` are markers. Honest arithmetic: 90 valid + 2 markers + 1 stale = 93. Linkage class remains
  `row-checksum` (no row carries `prev`/`prev_hash`), so deletion and truncation of a row are
  undetectable in this format — the honest verdict is
  `90/93 row checksums accounted for — linkage class row-checksum`, not "chain-intact".
- **Substrate log:** byte-unchanged (`substrate-witness.jsonl` md5 `24a2c03292371575655a287c334d8df8`,
  `topics.json` md5 `58599882cd997ecc57ea71d14bf09f52`). Correct — the substrate calls in the watcher
  fire only from the `first_poll` branch.
- **Pushed:** `0e47ab65`, on top of `0e5ced86` (civ-orchestrator session 53). Remote-verified via the
  commits API and by re-fetching `raw.githubusercontent.com` — 93 rows, 222227 bytes, tip row is this
  run's `witness_note`.

### Environment (16th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist again; `/workspace` held only an empty
  `.plugin-cache` directory. The NAS mount backing `/workspace` was 600G/600G, **100% used, 0 bytes
  available**, and a direct `git clone` into it died with `close error: Disk quota exceeded` on
  `.git/description`.
- **A full clone into the `/tmp` overlay was started and did complete the working tree** (7.0 GB on
  disk) — but only after several minutes, and the clone's `git` process (PID 112) **outlived its own
  command timeout**, leaving a stale `.git/shallow.lock` that blocked a follow-up `git fetch` with
  `fatal: Unable to create '/tmp/ai-writings/.git/shallow.lock': File exists` until that process exited.
  PID 112 later surfaced as a **zombie (`Z`, defunct)** — its parent was my own polling loop, so
  `kill -9` reported it "still alive" while `ps` showed it defunct. **Lesson: after a clone times out,
  check `ps aux | grep defunct` and kill the *parent* poll loop, not the zombie; a zombie cannot be
  killed and `kill` returning success is not proof the process is gone.**
- **The cheap route is the sparse one, and it is now the default.** A `git init --template=` into the
  overlay plus `GIT_SSL_NO_VERIFY=1 git fetch --depth 1 origin main`, a hand-written
  `.git/info/sparse-checkout` (the `git init --template=` route skips creating `.git/info/`, so it must
  be made by hand), and `git checkout -f origin/main` materialised only `bots/wesley-mechanic/` in
  seconds. The repo is ~3.7 GB per the API; never clone it wholesale.
- Staged to `/tmp/wm-run/bots/` because the script hardcodes those paths for `witness.log` /
  `state.json` / `bookkeeper.wal` and does `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` —
  `substrate_bus` must be staged alongside it or the import dies. Staged script md5
  `206682962c06f9814a5db65c2fbc7267` — byte-identical to upstream. No code changes were needed.
- **The NAS symlink fix was applied again.** `substrate_bus.py` hardcodes its write targets to
  `/workspace/repos/ai-writings/bots/substrate-bus/{substrate-witness.jsonl,topics.json}`, and on a
  100%-full NAS a write there lands as a **0-byte stub that still shows up in `ls -la`**. Both NAS
  paths were symlinked to their `/tmp/wm-run/bots/substrate-bus/` counterparts and the read-through was
  confirmed with `stat -L` (not bare `stat`, which reports link length, not target size) at 1085 and
  6739 bytes, matching their upstream md5s.
- **Push raced another bot, and the shallow rebase was a trap.** The first push was rejected
  `fetch first` (remote had advanced to `0e5ced86`), and `git rebase FETCH_HEAD` on the *wholesale*
  clone tried to replay 20+ unrelated upstream commits and died on `CONFLICT (add/add): Merge conflict
  in index.json` — a file this run never touched. `git rebase --abort` recovered cleanly, but the
  right move was a **fresh `git init --template=` + `--depth 1` fetch of the current remote head, then
  commit the witness.log change directly on top of it**. That pushed clean as
  `0e5ced86..0e47ab65` on the first attempt, with no conflict. **Rule for this repo: never rebase a
  deep/shallow wholesale clone onto a moving remote — rebuild shallow and commit on the fresh tip.**

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a
**constant false by construction** — the delta path can never satisfy the predicate, so the field
carries no signal. Tenth poll reporting this; still unfixed. The fix is a one-liner — either set
`budget` to the live `gamma+eta` total, or drop the constant and make the predicate mean what it
claims — but the script is upstream and byte-identical to its git blob, so no patch was applied.

Also still open: **zero `canon_changed` events exist in the entire 93-row history**, so the
`canon_changed` branch — the only path that exercises `substrate_publish()`, `bookkeeper_tick()` and
the delta arithmetic — has never executed against live data in this log's lifetime. It is an untested
code path; the watcher has so far only ever exercised `first_poll`, the no-change path, and 6
`poll_failed` rows.

## 2026-10-24T04:22Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable ~32.3h (1937 min).
- **Confirmed three times by independent paths:** the watcher's own `poll_canon()` inside
  the `--once` run (HTTP 200, stdout `[WESLEY] no change (b20375d389cb505d, 71 papers)`,
  exit 0); a pre-run probe taken immediately before the run; and a post-run probe taken
  immediately after the run. All three recompute to the same `b20375d389cb505d`, and the
  pre/post payloads are byte-equal (13565 bytes each, `cmp` reports IDENTICAL), so the
  no-change verdict is not a race artifact.
- **Count key:** the response carries `count` (71), not `paper_count` (absent), so the
  2026-10-22 count-key fallback fix remains load-bearing.
- **Log append:** one row, the unconditional `bot_started` event (hash `9a9e37830d6448da`),
  plus this run's `witness_note` (hash `a9f56fd52f7da42b`) closing it. Checksum re-verified
  VALID on both.
- **No canon-change note written.** A hash match is not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll`
  and `canon_changed` branches, so stable canon correctly produces zero ticks —
  `bookkeeper.wal` still does not exist and `state.json` is byte-unchanged
  (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log integrity:** 97/97 rows parse and carry `ts, iso, event, payload, hash`. 94/97 row
  checksums verify, 2 carry the literal marker `hash='RECOVERED'` (rows 9 and 12, the
  hand-authored `meta_wipe_recovery` rows — an explicit non-checksum marker, not corruption),
  and 1 is the inherited stale hash on row 25 (stored `88839488ea23e66c`, computed
  `2553b915563b73cc`) — a known upstream authoring slip, not introduced by this run.
  Counting caveat: 30 rows merely *mention* the token `RECOVERED` inside their note prose
  while still carrying valid checksums, so only the 2 rows whose hash *field* equals
  `RECOVERED` are markers. The honest arithmetic is 94 valid + 2 markers + 1 stale = 97.
  Linkage class remains `row-checksum`: no row carries `prev`/`prev_hash`, so deletion and
  truncation of a row are undetectable in this format — the honest verdict is
  `94/97 row checksums accounted for — linkage class row-checksum`, not "chain-intact".
- **Substrate log byte-unchanged** (`substrate-witness.jsonl` md5
  `24a2c03292371575655a287c334d8df8`, `topics.json` md5 `58599882cd997ecc57ea71d14bf09f52`),
  which is correct: the substrate calls fire only from the `first_poll` branch, and a
  `canon_changed` branch would also fire them — neither was reached. No substrate event was
  appended this run.
- **Event census:** across all 97 rows the mix is 51 `bot_started`, 37 `witness_note`,
  6 `poll_failed`, 2 `first_poll`, 2 `meta_wipe_recovery`, and **zero `canon_changed`**.

### Concurrent-instance reconciliation (new this run)

Another `wesley-mechanic` instance committed its own poll at `e7539709` (2026-10-24T04:16Z)
while this run was in flight, and the `civ-orchestrator` force-pushed `main` to `2ce2678e`
between the two. The two logs diverged after a common prefix of 93 rows: this run's tail
was `bot_started` 04:22:15 + `witness_note` 04:22:56, the concurrent run's was
`bot_started` 04:16:55 + `witness_note` 04:17:15 — disjoint, and both reached the
identical verdict (same hash, same count, no change). The merged file keeps the common 93
plus all four tail rows, ordered by `ts`, for 97 total. **No row was dropped and no run was
clobbered** — the append-only log's whole point, and the reason to reconcile by hash-prefix
diff rather than by blind overwrite.

Note also that `raw.githubusercontent.com` served a **stale 93-row copy** of `witness.log`
while the GitHub *contents* API at `ref=main` returned the true 95-row file. The raw
endpoint is not a reliable read path for a file this actively written; use the contents API
(or a fetched git tree) when the exact committed content matters.

### Environment (17th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist again; `/workspace` held only an empty
  `.plugin-cache` directory. The NAS mount backing `/workspace` was 600G/600G, 100% used,
  0 bytes available, and a direct `git clone` into it died with
  `close error: Disk quota exceeded` on `.git/description`.
- The repo is too large to clone wholesale — the API reports size 3699744 KB (~3.7 GB). A
  `--depth 1` clone into the `/tmp` overlay was started and ran to completion (7.0 GB on
  disk, 20685 files) but only after several minutes and a surviving background `git` process
  outliving its own command timeout.
- Because the run had to proceed before the clone finished, it was staged from the GitHub
  raw/API surface instead: `substrate_bus.py`, `topics.json`, `substrate-witness.jsonl`,
  `state.json` and `witness.log` were fetched and staged into `/tmp/wm-run/bots/`, which is
  where the script hardcodes its write targets (`witness.log` / `state.json` /
  `bookkeeper.wal`) and where it does `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` —
  `substrate_bus` must be staged alongside it or the import dies. Staged script md5
  `206682962c06f9814a5db65c2fbc7267`, byte-identical to upstream; no code changes were
  needed this run, and the later full checkout confirmed the staged md5s match the real
  git blobs exactly.
- **The NAS symlink fix had to cover THREE paths this run, not two.** `substrate_bus.py`
  hardcodes its write targets to
  `/workspace/repos/ai-writings/bots/substrate-bus/{substrate-witness.jsonl,topics.json}`,
  and on a 100%-full NAS a write there lands as a **0-byte stub that still shows up in
  `ls -la`** (md5 `d41d8cd98f00b204e9800998ecf8427e`). Both NAS substrate paths were
  symlinked to their `/tmp/wm-run/bots/substrate-bus/` counterparts — and additionally the
  task's own script path `/workspace/repos/ai-writings/bots/wesley-mechanic/wesley_watcher.py`
  had to be symlinked, because a plain `cp` of the 5805-byte script onto the NAS failed with
  `failed to close ...: Disk quota exceeded` and left a 0-byte stub behind. The stub was
  deleted and replaced by the symlink, after which `stat -L` reports 5805 bytes and md5
  `206682962c06f9814a5db65c2fbc7267` through all three paths, matching upstream. Read-through
  was confirmed with `stat -L` (not bare `stat`, which reports link length, not target size)
  at 1085 and 6739 bytes for the substrate pair, matching their upstream md5s.
- The same stub trap applied to delivering `witness.log` to `/workspace`: the `cp` failed
  with `Disk quota exceeded` and left a 0-byte file, so the deliverable was installed as a
  symlink to the `/tmp/wm-run` copy instead.

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a
**constant false by construction** — the delta path can never satisfy the predicate, so the
field carries no signal. Eleventh poll reporting this; still unfixed. The fix is a one-liner —
either set `budget` to the live `gamma+eta` total, or drop the constant and make the predicate
mean what it claims — but the script is upstream and byte-identical to its git blob, so no
patch was applied.

Also still open: **zero `canon_changed` events exist in the entire 97-row history**, so the
`canon_changed` branch — the only path that exercises `substrate_publish()`, `bookkeeper_tick()`
and the delta arithmetic — has never executed against live data in this log's lifetime. It is an
untested code path; the watcher has so far only ever exercised `first_poll`, the no-change path,
and 6 `poll_failed` rows.

## 2026-10-24T05:48Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable ~33.7h (2024 min), and ~24 min
  since the 05:24Z poll.
- **Confirmed three times by independent paths:** the watcher's own `poll_canon()` inside the
  `--once` run (HTTP 200, stdout `[WESLEY] no change (b20375d389cb505d, 71 papers)`, exit 0);
  a pre-run probe taken immediately before the run; and a post-run probe taken immediately after
  the run. All three recompute to the same `b20375d389cb505d`, and the pre/post payloads are
  byte-equal (13720 bytes each, `cmp` reports IDENTICAL), so the no-change verdict is not a race
  artifact.
- **Count key:** the response carries `count` (71), not `paper_count` (absent), so the 2026-10-22
  count-key fallback fix remains load-bearing.
- **Log append:** two rows — the unconditional `bot_started` event (row 104, pid 333, hash
  `94a26bf614e22a7f`, checksum re-verified VALID) written by `main()`, then this run's
  `witness_note` (row 105, hash `a978eb29cea3f236`) closing it. `witness.log` went 103 → 105 rows.
- **No canon-change note written.** A hash match is not a transition, and the operator instruction
  gates the note on canon having changed. The `witness_note` row records the poll, not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll` and
  `canon_changed` branches, so stable canon correctly produces zero ticks — `bookkeeper.wal` still
  does not exist and `state.json` is byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log integrity:** 105/105 rows parse and carry `ts, iso, event, payload, hash`. 102/105 row
  checksums verify, 2 carry the literal marker `hash='RECOVERED'` (rows 9 and 12, the hand-authored
  `meta_wipe_recovery` rows — an explicit non-checksum marker, not corruption), and 1 is the
  inherited stale hash on row 25 (stored `88839488ea23e66c`, computed `2553b915563b73cc`) — a
  known upstream authoring slip, not introduced by this run. Linkage class remains `row-checksum`
  (per `../README.md`): no row carries `prev`/`prev_hash`, so deletion and truncation of a row are
  undetectable in this format — the honest verdict is
  `102/105 row checksums accounted for — linkage class row-checksum`, not "chain-intact".
  This run's own row 105 self-verifies (`a978eb29cea3f236`).
- **Substrate log byte-unchanged** (`substrate-witness.jsonl` md5 `24a2c03292371575655a287c334d8df8`,
  `topics.json` md5 `58599882cd997ecc57ea71d14bf09f52`), which is correct: the substrate calls fire
  only from the `first_poll` branch, and neither `first_poll` nor `canon_changed` was reached.
- **Event census:** across all 105 rows the mix is 54 `bot_started`, 41 `witness_note`,
  6 `poll_failed`, 2 `first_poll`, 2 `meta_wipe_recovery`, and **zero `canon_changed`**.

### Environment (18th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist again; `/workspace` held only an empty
  `.plugin-cache` directory. The NAS mount backing `/workspace` was 600G/600G, 100% used, 0 bytes
  available, and a direct `cp` of the script into it failed with
  `failed to close './wesley_watcher.py': Disk quota exceeded`.
- **Recovery:** the GitHub **contents** API for `bots/wesley-mechanic/{wesley_watcher.py,state.json,witness.log}`
  and `bots/substrate-bus/{substrate_bus.py,topics.json,substrate-witness.jsonl}`, staged to
  `/tmp/wm-run/bots/` — which is where the script hardcodes its write targets (`witness.log` /
  `state.json` / `bookkeeper.wal`) and where it does
  `sys.path.insert('/tmp/wm-run/bots/substrate-bus')`, so `substrate_bus` must be staged alongside
  it or the import dies. The **contents API was used rather than `raw.githubusercontent.com`**
  because the raw endpoint is not a reliable read path for a file this actively written — it served
  a stale copy in a prior run.
- Staged script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to upstream. No code changes
  were needed this run. All other staged md5s (`state.json` `5ce39812d7f3af41583e4003872b6ef6`,
  `substrate-witness.jsonl` `24a2c03292371575655a287c334d8df8`, `topics.json`
  `58599882cd997ecc57ea71d14bf09f52`) match upstream exactly.
- **The NAS 0-byte truncation trap was re-verified live, not assumed.** A 6-byte `echo >` returned
  exit 0 and landed as a **0-byte stub** (md5 `d41d8cd98f00b204e9800998ecf8427e`) that still appeared
  in `ls -la`. The three NAS-facing paths
  (`wesley-mechanic/wesley_watcher.py`, `substrate-bus/substrate-witness.jsonl`,
  `substrate-bus/topics.json`) were symlinked to their `/tmp/wm-run` counterparts; `stat -L` confirms
  5805 / 1085 / 6739 bytes with upstream-matching md5s through all three paths. This is the
  established three-path fix — a plain `cp` onto the NAS silently loses the file.
- **No concurrent instance raced this poll.** The upstream log was 103 rows immediately before the
  run and 103 rows immediately after it (both verified via the contents API), so the two-log
  reconciliation procedure from the 04:22Z run was not needed this time.

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a
**constant false by construction**. The `(0,0)` escape clause is unreachable on every call path
(`first_poll` always passes `delta_gamma=1.0`; `canon_changed` always passes `delta_eta=1.0`), and
the first clause can only pass if the running total hits exactly `1000.0` within `1e-6` — a
coincidence target, not a conservation law. The field carries no signal. Twelfth poll reporting
this; still unfixed. The fix is a one-liner — either set `budget` to the live `gamma+eta` total, or
drop the constant and make the predicate mean what it claims — but the script is upstream and
byte-identical to its git blob, so no patch was applied.

Also still open: **zero `canon_changed` events exist in the entire 105-row history**, so the
`canon_changed` branch — the only path that exercises `substrate_publish()`, `bookkeeper_tick()` and
the delta arithmetic — has never executed against live data in this log's lifetime. It is an untested
code path; the watcher has so far only ever exercised `first_poll`, the no-change path, and
6 `poll_failed` rows.

## 2026-10-24T09:33Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04:28Z `first_poll` baseline (row 16) and to every
  poll since — stable ~37.3h (2239 min), ~45 min since the 2026-10-24T08:47:44Z poll.
- **Confirmed three times by independent paths:** the watcher's own `poll_canon()` inside the
  `--once` run (stdout `[WESLEY] no change (b20375d389cb505d, 71 papers)`, exit 0); a pre-run
  curl probe of `live-canon.superinstance.dev/api/canon` (HTTP 200, 13720 bytes,
  md5 `d9915bb9f3bcb8794cb57810427d0288`); a post-run probe of the same URL (HTTP 200, 13720
  bytes, same md5). The pre/post bodies are **byte-identical** (`cmp` clean), so the no-change
  verdict is not a race artifact.
- **Count key:** the response carries `count` (71), not `paper_count` (absent; top-level keys are
  exactly `['count','papers']`), so the 2026-10-22 count-key fallback fix remains load-bearing.
- **Log append:** two rows — the unconditional `bot_started` event (pid 303, hash
  `ca33df3fb887c1df`) and this run's `witness_note` (row 124, hash `c37214e53566ab51`).
  122 -> 124 rows.
- **No canon-change note written.** A hash match is not a transition.
- **No gamma/eta delta claimed.** `bookkeeper_tick()` is only reached from the `first_poll` and
  `canon_changed` branches, so stable canon correctly produces zero ticks — `bookkeeper.wal` is
  still **absent** and `state.json` is byte-unchanged (md5
  `5ce39812d7f3af41583e4003872b6ef6`).
- **Substrate log byte-unchanged** (`substrate-witness.jsonl` md5
  `246e49ffbb60922343befef78e15bf4b`, 1532 bytes; `topics.json` md5
  `e7d4cb8c41b32a724bfec8b1cc60329b`, 8987 bytes) — correct: the substrate calls fire only from
  the `first_poll` branch, and neither `first_poll` nor `canon_changed` was reached.
- **Log integrity:** 124/124 rows parse and carry `ts, iso, event, payload, hash`. Audit: 121
  verify, 2 carry the literal marker `hash='RECOVERED'` (rows 9 and 12, the hand-authored
  `meta_wipe_recovery` rows — an explicit non-checksum marker, not corruption), and 1 is the
  inherited stale hash on row 25 (stored `88839488ea23e66c`, computed `2553b915563b73cc`) — a
  known upstream authoring slip, not introduced by this run. Honest arithmetic: 121 + 2 + 1 = 124.
- **Linkage class remains `row-checksum`:** re-scanned every payload for `prev`, `prev_hash`,
  `parent`, `prev_row_hash` — **none found**, so deletion and truncation of a row are
  undetectable in this format. The honest verdict is *121/124 row checksums accounted for —
  linkage class row-checksum*, not "chain-intact".
- **Orphan rows: 14** (rows 1,3,5,7,10,13,15,17,18,19,23,28,35,120) — each a `bot_started` row
  not immediately followed by a `witness_note`. Rows 44 and 56 are **not** orphans. The signature
  is polls launched and dying before their note was written, not evidence of canon transitions.
- **Event census over 124 rows:** 64 `bot_started`, 50 `witness_note`, 6 `poll_failed`,
  2 `meta_wipe_recovery`, 2 `first_poll`, **0 `canon_changed`** — zero canon transitions across
  the entire recorded history.
- **No lost-update race:** upstream `main` had advanced to `0645775b` (Session 77 orchestrator
  run report) since the 08:48:08Z baseline, but that commit touched only
  `cellular-first-design/code/civilizations/*` — neither `witness.log` nor `state.json`. Our
  pre-run staged log (122 rows, 305082 bytes, md5 `0b15c34f4072747414efc6dc741cb337`) was
  byte-identical to the upstream blob, and our post-run log is that exact byte prefix plus the
  two appended rows (`new.startswith(old) == True`, 305082 -> 313271 bytes). The 123rd row is a
  clean append; no concurrent writer dropped a row.
- **Pushed:** `28c77d83` (onto `0645775b`), remote-verified via the commits API — upstream
  `witness.log` now reads 124 rows / 313271 bytes / md5 `12dfae237da5c64bce4c1ed652d615ea`,
  byte-identical to the local staged file.

### Environment (29th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist again. `/workspace` held only an empty
  `.plugin-cache`, and the NAS mount behind it was **600G/600G, 100% used, 0 bytes available**.
- **Recovery:** the GitHub contents API was usable (not rate-limited), so the six required files
  were staged to the `/tmp` overlay at `/tmp/wm-run/bots/` — the script hardcodes those paths for
  `witness.log` / `state.json` / `bookkeeper.wal` and does
  `sys.path.insert('/tmp/wm-run/bots/substrate-bus')`, so `substrate_bus` must be staged
  alongside it or the import dies.
- **All six staged files verified byte-identical to upstream by md5:** script
  `206682962c06f9814a5db65c2fbc7267`, `witness.log` `0b15c34f4072747414efc6dc741cb337`,
  `state.json` `5ce39812d7f3af41583e4003872b6ef6`, `substrate_bus.py`
  `6fa03e34e185ca52e3f51356bd76f611`, `substrate-witness.jsonl`
  `246e49ffbb60922343befef78e15bf4b`, `topics.json` `e7d4cb8c41b32a724bfec8b1cc60329b`.
- **The NAS 0-byte truncation trap was avoided, not assumed.** The six NAS-facing paths were
  symlinked to their `/tmp/wm-run` counterparts; `stat -L` confirms 5805 / 313271 / 92 / 4493 /
  1532 / 8987 bytes with upstream-matching md5s read *through* the symlinks. On a quota-full NAS,
  `ls -la` showing a file is not evidence it was written — always check the size field.
- **Clone note:** a plain `git clone` of AI-Writings transfers a multi-GB pack (3.3 GB observed
  for `--depth 1` here) and takes minutes; `--filter=blob:none` plus a `--no-checkout` fetch of
  only the tip range, followed by a sparse checkout of `bots/wesley-mechanic/`, is the fast path.
  `git sparse-checkout disable` on a large tree is itself slow — budget a background slot for
  it.

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a
**constant false by construction**. AST re-verified this run: the only two `bookkeeper_tick` call
sites are line 114 `bookkeeper_tick(1.0, 0.0)` and line 128 `bookkeeper_tick(float(delta), 1.0)`,
and an AST scan for a literal `(0.0, 0.0)` call site returned **0 matches** — the escape clause is
**unreachable on every call path**. The `budget` constant sits at line 62, the predicate at
line 71. The first clause can only pass if the running total hits exactly `1000.0` within `1e-6`
— a coincidence target, not a conservation law. The field carries no signal. **Twenty-second poll
reporting this; still unfixed.** The fix is a one-liner — either set `budget` to the live
`gamma+eta` total, or drop the constant and make the predicate mean what it claims — but the
script is upstream and byte-identical to its git blob, so no patch was applied.

Also still open: **zero `canon_changed` events in the entire 124-row history**, so the
`canon_changed` branch — the only path that exercises `substrate_publish()` to snowball-scout,
`bookkeeper_tick()` and the delta arithmetic — has never executed against live data in this log's
lifetime. It remains an untested code path.

### Poll 2026-10-24T09:47Z — canon unchanged (23rd consecutive no-change)

- **Verdict: no canon change.** Hash `b20375d389cb505d` / 71 papers, identical to the
  2026-10-22T20:04:28Z `first_poll` baseline (row 16) and to every poll since — now stable
  **~37.7h (2263 min)**, ~14 min since the 09:33Z poll (row 124).
- **Triangulated, not asserted:** (1) the watcher's own `poll_canon()` in the `--once` run
  (HTTP 200, stdout `[WESLEY] no change (b20375d389cb505d, 71 papers)`, exit 0); (2) a
  pre-run curl probe (HTTP 200, 13720 bytes, md5 `d9915bb9f3bcb8794cb57810427d0288`);
  (3) a post-run curl probe of the same URL — **byte-identical bodies, `cmp` clean** — so the
  verdict is not a race artifact.
- **Count key:** the endpoint returns the count under `count` (71), not `paper_count`
  (absent; top-level keys are exactly `['count','papers']`). The 2026-10-22 count-key
  fallback remains **load-bearing and still correct**.
- **No `canon_changed` event written, no gamma/eta delta claimed** — a hash match is not a
  transition. `state.json` byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`; `last_hash`
  `b20375d389cb505d`, `last_count` 71, `first_seen` 1792699490.998806 preserved) and
  `bookkeeper.wal` **still does not exist** — the correct no-op, since `bookkeeper_tick()` is
  only reached from the `first_poll` and `canon_changed` branches.
- **Appended rows:** the run added exactly one row, the unconditional `bot_started` event
  (pid 367, hash `11faeef20a5551e0`); `witness.log` went 124 → 125 rows, and the
  `witness_note` is the 126th. **126/126 rows parse** and carry
  `ts/iso/event/payload/hash`; **123 verify**, 2 carry the hand-authored
  `hash='RECOVERED'` marker, and 1 — **row 25**, the 2026-10-23T11:31:39Z note — carries a
  stale hash `88839488ea23e66c` against a computed `2553b915563b73cc`. That mismatch was
  **born with the row upstream** and is the known authoring slip, not a post-hoc edit and not
  caused by this run. **Honest verdict: linkage class `row-checksum`** — a payload-scanning
  pass for linkage keys (`prev`, `prev_hash`, `parent`, `prev_row_hash`) found **NONE**, so
  deletion and truncation of a row are undetectable in this format and a `chain-intact`
  verdict is not producible.
- **Orphan rows: 14** (rows 1,3,5,7,10,13,15,17,18,19,23,28,35,120) — the same 14 inherited
  from prior runs. This run's own row 125 was closed by its own note, so the count did **not**
  grow. Rows 44 and 56 are **not** orphans. The signature is polls launched and dying before
  their note was written, not evidence of canon transitions.
- **Event census over 126 rows:** 65 `bot_started`, 51 `witness_note`, 6 `poll_failed`,
  2 `meta_wipe_recovery`, 2 `first_poll`, **0 `canon_changed`** — zero canon transitions
  across the entire recorded history.
- **No lost-update race:** our pre-run staged `witness.log` (124 rows, 313271 bytes, md5
  `12dfae237da5c64bce4c1ed652d615ea`) was byte-identical to the upstream blob, and our
  post-run log is that exact byte prefix plus our two appended rows
  (`ours.startswith(upstream) == True`, 313271 → 320143 bytes). The 125th row is a clean
  append; no concurrent writer dropped a row.

### Environment (30th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist again; `/workspace` held only an empty
  `.plugin-cache` and `.mavis/tool-results`, and the NAS mount behind it was **600G/600G,
  100% used, 0 bytes available**.
- **Clone note (new this run):** a plain `git clone` into `/workspace` **failed with
  `close error: Disk quota exceeded`** while the partially-created tree still appeared in
  `ls` — the classic NAS trap. `/tmp` is **not** subject to the EDQUOT trap, so the clone was
  redone at `/tmp/ai-writings` with `--depth 1 --filter=blob:none --sparse` (the repo is
  3.7 GB; a full transfer is minutes and blows the quota). Then
  `git sparse-checkout set bots/wesley-mechanic bots/substrate-bus` to materialize only the
  six files that matter.
- **Staging:** the six required files were staged to the `/tmp` overlay at
  `/tmp/wm-run/bots/` — the script hardcodes those paths for `witness.log` / `state.json` /
  `bookkeeper.wal` and does `sys.path.insert('/tmp/wm-run/bots/substrate-bus')`, so
  `substrate_bus` must be staged alongside it or the import dies.
- **All six staged files verified byte-identical to upstream by md5:** script
  `206682962c06f9814a5db65c2fbc7267`, `witness.log` `12dfae237da5c64bce4c1ed652d615ea`,
  `state.json` `5ce39812d7f3af41583e4003872b6ef6`, `substrate_bus.py`
  `6fa03e34e185ca52e3f51356bd76f611`, `substrate-witness.jsonl`
  `246e49ffbb60922343befef78e15bf4b`, `topics.json` `e7d4cb8c41b32a724bfec8b1cc60329b`.
- **The NAS 0-byte truncation trap was avoided, not assumed.** The six NAS-facing paths were
  symlinked to their `/tmp/wm-run` counterparts; `stat -L` confirms 5805 / 320143 / 92 / 4493 /
  1532 / 8987 bytes with upstream-matching md5s read *through* the symlinks. On a quota-full
  NAS, `ls -la` showing a file is not evidence it was written — always check the size field.

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a
**constant false by construction**. AST re-verified this run: the only two `bookkeeper_tick`
call sites are line 114 `bookkeeper_tick(1.0, 0.0)` and line 128
`bookkeeper_tick(float(delta), 1.0)`, and an AST scan for a literal `(0.0, 0.0)` call site
returned **0 matches** — the escape clause is **unreachable on every call path**. The
`budget` constant sits at line 62, the predicate at line 71. The first clause can only pass if
the running total hits exactly `1000.0` within `1e-6` — a coincidence target, not a
conservation law. The field carries no signal. **Twenty-third poll reporting this; still
unfixed.** The fix is a one-liner — either set `budget` to the live `gamma+eta` total, or drop
the constant and make the predicate mean what it claims — but the script is upstream and
byte-identical to its git blob, so no patch was applied.

Also still open: **zero `canon_changed` events in the entire 126-row history**, so the
`canon_changed` branch — the only path that exercises `substrate_publish()` to snowball-scout,
`bookkeeper_tick()` and the delta arithmetic — has never executed against live data in this
log's lifetime. It remains an untested code path.

## 2026-10-24T10:04Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable ~38.0h (2280 min),
  ~17 min since the 2026-10-24T09:47Z poll.
- **Confirmed three times by independent paths:** the watcher's own `poll_canon()`
  (stdout `[WESLEY] no change (b20375d389cb505d, 71 papers)`, exit 0), a **pre-run**
  curl probe, and a **post-run** curl probe. Both probes returned HTTP 200,
  13720 bytes, md5 `d9915bb9f3bcb8794cb57810427d0288`; the two bodies are
  **byte-identical** (`cmp` clean), so the no-change verdict is not a race artifact.
- **Count key:** the response carries `count` (71), not `paper_count` (absent; top-level
  keys are exactly `['count','papers']`), so the 2026-10-22 count-key fallback fix
  remains load-bearing and still correct.
- **No canon-change note written.** A hash match is not a transition. No gamma/eta
  delta claimed — `bookkeeper_tick()` is only reached from the `first_poll` and
  `canon_changed` branches, so stable canon correctly produces zero ticks:
  `bookkeeper.wal` still does not exist and `state.json` is byte-unchanged
  (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log append:** two rows — the unconditional `bot_started` (pid 288) plus this
  run's `witness_note`. `witness.log` went 126 → 128 rows.
- **Log integrity:** 128/128 rows parse and carry `ts, iso, event, payload, hash`.
  Linkage class `row-checksum` (per `../README.md`): each row's hash commits to its
  own payload only — re-scanned every payload for `prev` / `prev_hash` / `parent` /
  `prev_row_hash`: **none found**. Deletion and truncation of a row are therefore
  undetectable in this format, so the honest verdict is
  `125 verify + 2 RECOVERED markers + 1 known-stale hash — linkage class
  row-checksum`, not "chain-intact".
  - 125 rows verify.
  - 2 hand-authored `meta_wipe_recovery` rows carry the literal marker
    `hash='RECOVERED'` (an explicit non-checksum marker, not corruption).
  - 1 row — **row 25**, the 2026-10-23T11:31:39Z `witness_note` — carries a stale
    hash `88839488ea23e66c` against a computed `2553b915563b73cc`. This mismatch
    was **born with the row upstream**; it is the known upstream authoring slip, not
    a post-hoc payload edit and not caused by this run.
  - This run introduced no new mismatch.
- **Orphan rows: 14** (rows 1, 3, 5, 7, 10, 13, 15, 17, 18, 19, 23, 28, 35, 120) —
  `bot_started` rows with no immediately-following `witness_note`. Rows 44 and 56
  are **not** orphans. The signature is polls launched and dying before their note
  was written, not evidence of canon transitions.
- **Event census (128 rows):** 66 `bot_started`, 52 `witness_note`, 6 `poll_failed`,
  2 `meta_wipe_recovery`, 2 `first_poll`, **0 `canon_changed`** — zero canon
  transitions across the entire recorded history.
- **No lost-update race:** upstream `main` had advanced to `9f6a4805` (Session 80
  orchestrator run, +80 rows, Control B) since the 09:47Z baseline, but that commit
  touched neither `witness.log` nor `state.json`. The pre-run staged log (126 rows,
  320143 bytes, md5 `3ee29521b3ceb6a54408b503fb575a4b`) was byte-identical to the
  upstream blob, and the post-run log is that exact byte prefix plus the appended
  rows (`ours.startswith(upstream) == True`, 320143 → 328572 bytes, 8429 bytes
  appended) — a clean append, no concurrent writer dropped a row.

### Environment (30th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist; `/workspace` was an empty NAS
  mount at 600G/600G, 100% used, 0 bytes available, and the mount root contained
  only an empty `.plugin-cache`. Recovered the six required files via the GitHub
  contents API and `raw.githubusercontent.com`, staged to `/tmp/wm-run/bots/`
  because the script hardcodes those paths for `witness.log` / `state.json` /
  `bookkeeper.wal` and does `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` —
  `substrate_bus` must be staged alongside it or the import dies.
- **A plain full clone was rejected.** The first `git clone` against the
  quota-full NAS died with `close error: Disk quota exceeded` while still
  appearing in `ls`. `/tmp` is **not** subject to the EDQUOT trap, so the clone
  was redone there with `--filter=blob:none --sparse`.
- All six staged files verified byte-identical to upstream by md5: script
  `206682962c06f9814a5db65c2fbc7267`, `witness.log`
  `3ee29521b3ceb6a54408b503fb575a4b`, `state.json`
  `5ce39812d7f3af41583e4003872b6ef6`, `substrate_bus.py`
  `6fa03e34e185ca52e3f51356bd76f611`, `substrate-witness.jsonl`
  `246e49ffbb60922343befef78e15bf4b`, `topics.json`
  `e7d4cb8c41b32a724bfec8b1cc60329b`.
- **The NAS 0-byte truncation trap was avoided, not assumed.** A direct NAS write
  was tested and silently truncated to 0 bytes with exit 0 (`printf` of 5000
  chars → 0-byte file), so `ls -la` showing a file is not evidence it was written
  — always check the size field. The six NAS-facing paths were symlinked to their
  `/tmp/wm-run` counterparts; `stat -L` confirms 5805 / 320143 / 92 / 4493 / 1532 /
  8987 bytes with upstream-matching md5s read *through* the symlinks.

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so
`last_conserved` is a **constant false by construction**. AST re-verified this run:
the only two `bookkeeper_tick` call sites are line 114 `bookkeeper_tick(1.0, 0.0)`
and line 128 `bookkeeper_tick(float(delta), 1.0)`, and an AST scan for a literal
`(0.0, 0.0)` call site returned **0 matches** — the escape clause is
**unreachable on every call path**. The `budget` constant sits at line 62, the
predicate at line 71. The first clause can only pass if the running total hits
exactly `1000.0` within `1e-6` — a coincidence target, not a conservation law. The
field carries no signal. **Twenty-fourth poll reporting this; still unfixed.** The
fix is a one-liner — either set `budget` to the live `gamma+eta` total, or drop the
constant and make the predicate mean what it claims — but the script is upstream
and byte-identical to its git blob, so no patch was applied.

Also still open: **zero `canon_changed` events in the entire 128-row history**, so
the `canon_changed` branch — the only path that exercises `substrate_publish()` to
snowball-scout, `bookkeeper_tick()` and the delta arithmetic — has never executed
against live data in this log's lifetime. It remains an untested code path.

## 2026-10-24T13:06Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable ~41.0h (2460 min),
  ~17.6 min since the 2026-10-24T12:48:52Z poll.
- **Confirmed by three independent paths:** the watcher's own `poll_canon()`
  (stdout `[WESLEY] no change (b20375d389cb505d, 71 papers)`, exit 0), a **pre-run** curl
  probe (HTTP 200, 13720 bytes, md5 `d9915bb9f3bcb8794cb57810427d0288`), and a **post-run**
  curl probe (HTTP 200, 13720 bytes, md5 `d9915bb9f3bcb8794cb57810427d0288`) — the two
  bodies are **byte-identical** (`cmp` clean), and both hash to `b20375d389cb505d` under
  `sha256(json, sort_keys)[:16]`, so the no-change verdict is not a race artifact and does
  not rest on the watcher's own report alone.
- **Count key:** the response carries `count` (71), not `paper_count` (absent; top-level
  keys are exactly `['count','papers']`), so the 2026-10-22 count-key fallback fix
  remains load-bearing and still correct.
- **No canon-change note written.** A hash match is not a transition. No gamma/eta
  delta claimed — `bookkeeper_tick()` is only reached from the `first_poll` and
  `canon_changed` branches, so stable canon correctly produces zero ticks:
  `bookkeeper.wal` still does not exist and `state.json` is byte-unchanged
  (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log append:** two rows — the unconditional `bot_started` (pid 277, hash
  `7e33d61da35a8718`) plus this run's `witness_note` (hash `45c82c9d7a055691`).
  `witness.log` went 146 → 148 rows.
- **Log integrity:** 148/148 rows parse and carry `ts, iso, event, payload, hash`.
  Linkage class `row-checksum` (per `../README.md`): each row's hash commits to its own
  payload only — re-scanned every payload for `prev` / `prev_hash` / `parent` /
  `prev_row_hash`: **none found**. Deletion and truncation of a row are therefore
  undetectable in this format, so the honest verdict is
  `145 verify + 2 RECOVERED markers + 1 known-stale hash — linkage class row-checksum`,
  not "chain-intact".
  - 145 rows verify.
  - 2 hand-authored `meta_wipe_recovery` rows carry the literal marker `hash='RECOVERED'`
    (an explicit non-checksum marker, not corruption).
  - 1 row — **row 25**, the 2026-10-23T11:31:39Z `witness_note` — carries a stale hash
    `88839488ea23e66c` against a computed `2553b915563b73cc`. This mismatch was **born
    with the row upstream**; it is the known upstream authoring slip, not a post-hoc
    payload edit and not caused by this run.
  - This run introduced no new mismatch.
- **Orphan rows: 15** (rows 1, 3, 5, 7, 10, 13, 15, 17, 18, 19, 23, 28, 35, 120) —
  `bot_started` rows with no immediately-following `witness_note`. Rows 44 and 56 are
  **not** orphans. The signature is polls launched and dying before their note was
  written, not evidence of canon transitions. This run's own row 147 is closed by this
  note as row 148.
- **Event census (148 rows, post-note):** 76 `bot_started`, 62 `witness_note`,
  6 `poll_failed`, 2 `meta_wipe_recovery`, 2 `first_poll`, **0 `canon_changed`** —
  zero canon transitions across the entire recorded history.
- **No lost-update race:** the upstream `witness.log` blob at head `f4f0c80` carried
  md5 `1619ef6f88286a84d58a6856975c0429` (146 rows, 408182 bytes) — **byte-identical**
  to our pre-run staged copy (`cmp` clean) — and our post-run log is that exact byte
  prefix plus our two appended rows (`post.startswith(pre) == True`, 408182 → 418125
  bytes). No concurrent writer dropped a row and no upstream row was missed. Note the
  upstream `witness.log` md5 has moved from `3d637f536d3d0fb0f34a0fae6f6b434f` (recorded
  in the 12:47Z note) to `1619ef6f88286a84d58a6856975c0429` — that is **upstream drift**
  from other polls appending, not a local edit.

### Environment (39th consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist again; `/workspace` was an empty NAS
  mount at 600G/600G, 100% used, 0 bytes available, and the mount root contained only an
  empty `.plugin-cache`. The NAS write trap was avoided, not assumed: a `git clone`
  directly into the mount failed with `Disk quota exceeded` **while writing
  `.git/description`**, and the same failure mode appeared on a `cp` into the mount. All
  durable output this run was produced on the `/tmp` overlay and published to the
  upstream repo via git rather than left on the NAS.
- A **full clone** was then started on the `/tmp` overlay and reached **1.5 GB** before
  being aborted — the repo working tree is multi-GB (20728 files) and a full clone is
  NOT needed when only the `bots/` cone is required. The working method for this run was
  therefore **sparse staging**: `git init` + `remote add` + `fetch --depth 1
  --filter=blob:none` + `sparse-checkout set bots/wesley-mechanic bots/substrate-bus`,
  then raw-blob fetch of the six required files into `/tmp/wm-run/bots/`.
- The six staged files were verified byte-identical to upstream by md5: script
  `206682962c06f9814a5db65c2fbc7267`, `witness.log` `1619ef6f88286a84d58a6856975c0429`,
  `state.json` `5ce39812d7f3af41583e4003872b6ef6`, `substrate_bus.py`
  `6fa03e34e185ca52e3f51356bd76f611`, `substrate-witness.jsonl`
  `bc63838b9cd7ea75c5041ec5979e9c49`, `topics.json` `e7d4cb8c41b32a724bfec8b1cc60329b`.
- One tooling hazard was hit and handled rather than assumed: a `git clone` issued as a
  foreground command exceeded the 30 s command window and was killed mid-fetch, so the
  clone was re-launched detached with `(setsid nohup timeout -s KILL 600 ... &)` — and
  then deliberately aborted once the working tree proved multi-GB.

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total, so `last_conserved` is
a **constant false by construction**. AST re-verified this run: the only two
`bookkeeper_tick` call sites are line 114 `bookkeeper_tick(1.0, 0.0)` and line 128
`bookkeeper_tick(float(delta), 1.0)`, and an AST scan for a literal `(0.0, 0.0)` call
site returned **0 matches** — the escape clause is **unreachable on every call path**.
The `budget` constant sits at line 62, the predicate at line 71. The first clause can
only pass if the running total hits exactly `1000.0` within `1e-6` — a coincidence
target, not a conservation law. The field carries no signal. **Thirty-third poll
reporting this; still unfixed.** The fix is a one-liner — either set `budget` to the
live `gamma+eta` total, or drop the constant and make the predicate mean what it
claims — but the script is upstream and byte-identical to its git blob, so no patch was
applied.

Also still open: **zero `canon_changed` events in the entire 148-row history**, so the
`canon_changed` branch — the only path that exercises `substrate_publish()` to
snowball-scout, `bookkeeper_tick()` and the delta arithmetic — has never executed
against live data in this log's lifetime. It remains an untested code path.

## 2026-10-24T13:51Z — poll, no change

- **Canon poll:** OK 200. Hash `b20375d389cb505d`, 71 papers.
- **Result:** no change vs the 2026-10-22T20:04Z baseline — stable ~41.8h (2507 min),
  ~18.8 min since the 2026-10-24T13:32:53Z poll.
- **Confirmed three times by independent paths:** the watcher's own `poll_canon()`
  (stdout `[WESLEY] no change (b20375d389cb505d, 71 papers)`, exit 0), an independent
  **pre-run** curl probe (HTTP 200, 13720 bytes, md5 `d9915bb9f3bcb8794cb57810427d0288`),
  and an independent **post-run** curl probe (HTTP 200, 13720 bytes, md5
  `d9915bb9f3bcb8794cb57810427d0288`, `cmp`-identical to the pre-run body). Recomputing
  `sha256(json, sort_keys)[:16]` over that body yields `b20375d389cb505d` both times.
- **Count key:** the response carries `count` (71), not `paper_count` (absent; top-level
  keys are exactly `['count','papers']`), so the 2026-10-22 count-key fallback fix
  remains load-bearing and still correct.
- **No canon-change note written.** A hash match is not a transition. No gamma/eta delta
  claimed — `bookkeeper_tick()` is only reached from the `first_poll` and `canon_changed`
  branches, so stable canon correctly produces zero ticks: `bookkeeper.wal` still does not
  exist and `state.json` is byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`).
- **Log append:** two rows — the unconditional `bot_started` (pid 363, hash
  `01f193185f1bd1b6`) plus this run's `witness_note` (hash `4579b237930f8326`).
  `witness.log` went 152 → 154 rows.
- **Log integrity:** 154/154 rows parse and carry `ts, iso, event, payload, hash`.
  Linkage class `row-checksum` (per `../README.md`): each row's hash commits to its own
  payload only. This run **re-verified linkage structurally** rather than by substring
  scan: 0 rows carry a structural `prev` / `prev_hash` / `parent` / `prev_row_hash`
  field, and 0 rows' hashes equal the previous row's payload-hash — so there is no chain
  linkage at all. (A naive substring scan reports ~60 hits, but every one of those is the
  literal word appearing *inside prose* of a note; a structural scan that requires a
  16-hex value in a dedicated field returns 0.) Deletion and truncation of a row are
  therefore undetectable in this format, so the honest verdict is
  `151 verify + 2 RECOVERED markers + 1 known-stale hash — linkage class row-checksum`,
  not "chain-intact".
  - 151 rows verify.
  - 2 hand-authored `meta_wipe_recovery` rows carry the literal marker `hash='RECOVERED'`
    (an explicit non-checksum marker, not corruption).
  - 1 row — **row 25**, the 2026-10-23T11:31:39Z `witness_note` — carries a stale hash
    `88839488ea23e66c` against a computed `2553b915563b73cc`. This mismatch was **born
    with the row upstream**; it is the known upstream authoring slip, not a post-hoc
    payload edit and not caused by this run.
  - This run introduced no new mismatch.
- **Orphan rows: 14** (rows 1, 3, 5, 7, 10, 13, 15, 17, 18, 19, 23, 28, 35, 120) —
  `bot_started` rows with no immediately-following `witness_note`. The signature is polls
  launched and dying before their note was written, not evidence of canon transitions.
  This run's own row 153 is closed by this note as row 154.
- **Event census (154 rows):** 79 `bot_started`, 65 `witness_note`, 6 `poll_failed`,
  2 `meta_wipe_recovery`, 2 `first_poll`, **0 `canon_changed`** — zero canon transitions
  across the entire recorded history.
- **No lost-update race:** upstream `main` carried the 152-row `witness.log` (md5
  `c268c2f6790a5edf6c401e61a09a05df`) and our pre-run staged copy was byte-identical
  to that blob, so our pre-run state was already upstream-current and no upstream row was
  missed.

### Environment (32nd consecutive wipe with the named path gone)

- `/workspace/repos/ai-writings/...` did not exist; `/workspace` was an empty NAS mount at
  600G/600G, 100% used, 0 bytes available, mount root containing only an empty
  `.plugin-cache`. A direct `git clone` into it failed with
  `close error: Disk quota exceeded`.
- The NAS 0-byte truncation trap **reconfirmed this run**: a 5-byte `printf 'hello' >`
  returned **exit 0** and still left a **0-byte** file in `ls -la`. Exit status and `ls`
  presence are not evidence of a durable write — always check the size field.
- Recovered the six required files via the documented sparse method: `git init
  --template=` + `git remote add` + `git fetch --depth 2 origin main` + a hand-written
  `.git/info/sparse-checkout` (the `--template=` trick skips `.git/info/`, so it must be
  created by hand). A **full** `git clone` was tried first and had to be killed at 1.7 GB
  and still running — the pack is multi-GB and the sparse cone filter does not reduce it.
- Staged to `/tmp/wm-run/bots/` because the script hardcodes those paths for
  `witness.log` / `state.json` / `bookkeeper.wal` and does
  `sys.path.insert('/tmp/wm-run/bots/substrate-bus')` — `substrate_bus` must be staged
  alongside it or the import dies.
- All seven staged files verified byte-identical to their upstream git blobs by md5:
  script `206682962c06f9814a5db65c2fbc7267`, `witness.log`
  `c268c2f6790a5edf6c401e61a09a05df`, `state.json`
  `5ce39812d7f3af41583e4003872b6ef6`, `RUN_NOTES.md`
  `fd4fad61cee353aaf3d1a309e81d9552`, `substrate_bus.py`
  `6fa03e34e185ca52e3f51356bd76f611`, `substrate-witness.jsonl`
  `f278efdc0d6e4b1d1c61011143854484`, `topics.json`
  `140c5a650fc4910999a8cb9538e06aa6`.
- The two NAS-facing directories (`bots/wesley-mechanic`, `bots/substrate-bus`) were
  **symlinked** to their `/tmp/wm-run` counterparts so the `substrate_bus` hardcoded
  `/workspace/repos/...` path resolves onto a real filesystem. `stat -L` confirms the real
  byte sizes behind every link (1957 / 11217 / 115896 / 92 / 5805 / 438318).
- This run appended no substrate event, which is correct — the substrate calls in the
  watcher fire only from the `first_poll` and `canon_changed` branches.

### Open defect, still unresolved

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total, so `last_conserved` is
a **constant false by construction**. The only two `bookkeeper_tick` call sites are
line 114 `bookkeeper_tick(1.0, 0.0)` and line 128 `bookkeeper_tick(float(delta), 1.0)`;
an AST scan for a literal `(0.0, 0.0)` call site returns **0 matches** — the escape clause
is **unreachable on every call path**. The first clause can only pass if the running total
hits exactly `1000.0` within `1e-6` — a coincidence target, not a conservation law. The
field carries no signal. The fix is a one-liner — either set `budget` to the live
`gamma+eta` total, or drop the constant and make the predicate mean what it claims — but
the script is upstream and byte-identical to its git blob, so no patch was applied.

Also still open: **zero `canon_changed` events in the entire history**, so the
`canon_changed` branch — the only path that exercises `substrate_publish()` to
snowball-scout, `bookkeeper_tick()` and the delta arithmetic — has never executed
against live data in this log's lifetime. It remains an untested code path.
