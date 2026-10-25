# Wesley - Canon Poll 2026-10-25T08:23:44Z

**Verdict: NO CANON CHANGE.** Hash `b20375d389cb505d`, 71 papers - unchanged.

## Run

```
$ cd /workspace/repos/ai-writings/bots/wesley-mechanic
$ python3 wesley_watcher.py --once
[WESLEY] no change (b20375d389cb505d, 71 papers)
EXIT=0
```

Polled `https://live-canon.superinstance.dev/api/canon`. Canon state is byte-identical to the
`2026-10-22T20:04:50Z` baseline (`state.json` `first_seen` 1792699490.998806) and to every poll
since - stable **60.3h** (~2.5 days) overall, ~0.02h since the 07:42Z poll.
`state.json` is unchanged (`last_hash` b20375d389cb505d, `last_count` 71).

**No canon-change witness event was written and no gamma/eta delta is claimed** - a hash match is
not a transition. `bookkeeper.wal` still does not exist, which is the correct no-op outcome:
`bookkeeper_tick()` is reached only from the `first_poll` and `canon_changed` branches, so a stable
canon produces zero ticks.

## Verification - three independent paths

1. **The watcher's own `poll_canon()`** - stdout `[WESLEY] no change (b20375d389cb505d, 71 papers)`,
   exit 0, no exception, no `poll_failed` event.
2. **Independent curl probe, after the run** - HTTP 200, 13720 bytes, body md5
   `d9915bb9f3bcb8794cb57810427d0288`, recomputing to `sha256(json, sort_keys)[:16] =
   b20375d389cb505d`.
3. **Byte-comparison against the inherited baseline body** - the 98-row upstream prefix's recorded
   body md5 is `d9915bb9f3bcb8794cb57810427d0288`; the live probe returns the same md5 and the same
   13720-byte length, so the canon payload is unchanged at the byte level, not merely
   hash-equivalent.

The response carries the count under `count` (71), **not** `paper_count` (absent; top-level keys are
exactly `['count','papers']`), so the count-key fallback in `poll_canon()` remains load-bearing and
still correct.

## Log integrity

- **97/100 rows parse** and carry `ts`/`iso`/`event`/`payload`/`hash`; **97 row hashes
  verify** against their own payloads.
- The **3 non-verifying rows are the inherited, previously-audited ones** and no new mismatch
  was introduced: rows 9 and 12 carry the literal marker `RECOVERED` in the hash field
  (`meta_wipe_recovery`), and row 25 is the upstream-born stale hash - its claimed
  `88839488ea23e66c` matches the upstream git blob byte-for-byte (row md5
  `65784c40fae50ac192a3f6c96fed6675` on both sides), so it is **provenance, not corruption**.
- **Linkage class remains `row-checksum`.** Each row's hash commits to its own payload only and
  carries no `prev`, so deletion and truncation are **undetectable** and `intact` is not producible
  for this file.
- **Upstream prefix preserved:** the first 98 rows of the staged log are byte-identical to the
  upstream git blob (`cmp` clean, upstream md5 `6b5285efe3ed72fd0f6209b6f5e950d3`).

## Workspace (40th wipe)

The prompt's path `/workspace/repos/ai-writings/bots/wesley-mechanic/` did not exist: `/workspace`
contained only `.plugin-cache` and no `repos/` dir at all, and the NAS mount is **600G/600G at 100%**
(`statvfs` `f_bavail = 0`) - a clone into it dies with `Disk quota exceeded`, and plain writes
silently truncate to **0 bytes** while returning rc=0 (`ls` shows the file, the content is empty).
The repo was therefore recovered into the overlay disk (`/tmp`, 28G free) and the prompt path
**symlinked** to it: `/workspace/repos/ai-writings -> /tmp/ai-writings`.

The live repo is `SuperInstance/AI-Writings`; its default branch `main` carries only
`cellular-first-design/` and **no `bots/` tree**, so branch
`wesley/witness-poll-2026-10-25T0741Z` was checked out (HEAD `937d25d`), which carries
`bots/wesley-mechanic/` (watcher, `state.json`, `witness.log`, three prior poll notes) and
`bots/substrate-bus/`. The `bots/` tree was staged into `/tmp/wm-run` so the watcher's hardcoded
`/tmp/wm-run/bots/wesley-mechanic/witness.log`, `state.json` and `bookkeeper.wal` paths resolve to
real writable files, and `substrate_bus.py`'s hardcoded
`/workspace/repos/ai-writings/bots/substrate-bus/` paths resolve via the symlink. **Both hardcoded
path sets now resolve** - the watcher was re-run from the canonical prompt path and behaved
identically (`no change`, exit 0).

## Open defect - still unresolved (34th poll reporting it)

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a
constant **false by construction**: the only two `bookkeeper_tick` call sites are line 114
`(1.0, 0.0)` and line 128 `(float(delta), 1.0)`, and the `delta==0 / eta==0` escape clause is
**unreachable** on every call path, so the field carries no signal. The fix is a one-liner (set
budget to the live `gamma+eta` total, or drop the constant and make the predicate mean what it
claims), but the script is upstream and byte-identical to its git blob, so **no patch was applied**.

## Substrate

`bots/substrate-bus/substrate-witness.jsonl` and `topics.json` are byte-unchanged (md5
`d3f588a44223088f4b62b262b5c8e8c2` / `d94b0a5d5c23baa4c317441a046ed455`, 865 and 4508 bytes, 4
substrate rows) - the correct no-op, since the substrate calls in the watcher fire only from the
`first_poll` and `canon_changed` branches.

## Orphan rows

16 `bot_started` rows have no immediately-following `witness_note` (rows 1, 3, 5, 7, 10, 13, 15, 17, 18, 19, 23, 28, 35, 98, 99, 100). Rows
1,3,5,7,10,13,15,17,18,19,23,28,35 are the long-standing inherited set; row 98 is the upstream
07:42Z poll; rows 99 and 100 are this run's two `bot_started` rows, **closed by this note (row 101)**.
