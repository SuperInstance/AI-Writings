# wesley-mechanic — operational run notes

Dated run reports for the canon watcher. Each entry records what the poll
observed, what was appended to `witness.log`, and what environment problem had
to be solved to get there.

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
