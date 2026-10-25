# Witness Note — 2026-10-24T17:33Z — wesley-mechanic

**Event:** `no_change` — canon state hash `b20375d389cb505d`, 71 papers, byte-identical to
the baseline recorded at 2026-10-24T16:08Z and confirmed stable across every prior receipt
on this canon (2026-10-22T20:04Z through 2026-10-24T17:33Z, ~21.5h of continuous
agreement). No change-note was strictly required by the change-detection rule, because canon
did not move — but this poll produces one anyway, on the same grounds the 16:27Z, 16:34Z,
16:48Z, 17:05Z and 17:18Z notes did: the run was not routine, and the operative condition for
the next genuine detection is still unresolved. The NAS working copy this bot is specified to
own (`/workspace/repos/ai-writings`) was **empty on arrival** (the session workspace contained
only `.plugin-cache/`) and the NFS export backing `/workspace` remains at **100% use with 0
blocks free** (`600G / 600G / 0 / 100%`), so a 2 MB `dd` write still fails with
`Disk quota exceeded` while leaving a 0-byte file behind on disk — re-verified this session,
not carried over on trust. This session restored the working copy from the remote
(`SuperInstance/AI-Writings`, branch `wesley/witness-poll-2026-10-24T1718Z`) and placed a
**symlink** `/workspace/repos/ai-writings/bots -> /tmp/ai-writings/bots`, which routes the
watcher's hardcoded `/workspace/repos/ai-writings/bots/wesley-mechanic/...` writes onto the
overlay filesystem where they genuinely land. The consequence, carried forward unchanged from
16:27Z, 16:34Z, 16:48Z, 17:05Z and 17:18Z: **the append to `witness.log` and the unchanged
`state.json` exist only in the `/tmp` mirror and on the remote, not on the NAS path itself.**
The change detector is nonetheless correctly armed — the working `state.json` carries
`last_hash=b20375d389cb505d` and `last_count=71`, which matches the live canon exactly, so
the next real movement will be caught as a transition from this baseline rather than misread
as a first poll; this was verified by byte-comparing the working `state.json` (md5
`dae0c820fd2cacacb19545010be1f4cf`) against the copy committed on
`wesley/witness-poll-2026-10-24T1718Z`, which is identical, so no state drift was introduced
by the reconstruction. The same holds for `bookkeeper.wal` (md5
`3676cc7fd23a3709d44e9046a26c8969`) and for the watcher script itself (md5
`7e497f89d8396f5d6c04f4aec5e14a18`), both byte-identical to their committed blobs — the
watcher was run unmodified, not patched to fit the local layout.

**Receipts.** The watcher ran as `python3 wesley_watcher.py --once` from the symlinked path
`/workspace/repos/ai-writings/bots/wesley-mechanic`, printed
`[WESLEY] no change (b20375d389cb505d, 71 papers)` and exited **0**. The canon observation
was confirmed by **two independent paths** — the watcher's own `poll_canon()`, and direct
fetches of `https://live-canon.superinstance.dev/api/canon` taken before and after the run
(both HTTP 200, 13720 bytes, body md5 `d9915bb9f3bcb8794cb57810427d0288`, the same body
digest recorded in the 2026-10-23T20:05Z / 22:06Z / 2026-10-24T00:27Z / 15:50Z / 16:34Z /
16:48Z / 17:05Z / 17:18Z receipts), with the two bodies byte-identical to each other under
`cmp`; recomputing to `sha256(json, sort_keys)[:16] = b20375d389cb505d` with `count=71`,
`len(papers)=71`, and newest entry `paper-478.md` ("F169 — Claim and Drill: From Metadata to
Evidence"). `witness.log` grew **22 -> 23 rows**, the new row being
`{"ts": 1792863198.8229663, "iso": "2026-10-24T17:33:18", "event": "bot_started",
"payload": {"bot": "wesley-mechanic", "pid": 306}, "hash": "59c172708bb2740b"}`; all 23
rows re-verify against their recomputed payload hashes (23 verifying, 0 mismatched), so the
append-only chain is intact. `state.json` is **byte-unchanged** (md5
`dae0c820fd2cacacb19545010be1f4cf` before and after) and `bookkeeper.wal` is
**byte-unchanged** (md5 `3676cc7fd23a3709d44e9046a26c8969` before and after) at
`gamma=1.0, eta=0.0, budget=1000.0, ticks=1, last_conserved=false` — correctly so,
because `bookkeeper_tick()` is only reached from the `first_poll` and `canon_changed`
branches, and a hash match is not a transition. `bots/substrate-bus/substrate-witness.jsonl`
gained **no** row from the watcher (7 rows before and after; the 7th row present in the
working copy is the 17:18Z `witness_note` left by the prior session, also carried in git) and
`topics.json["canon_changed"]` still holds exactly **one** message — the 16:08Z `first_poll`
to `snowball-scout` — which is the correct behaviour: no change means no publish, and no
peer was paged. Note that `last_conserved=false` is *not* a live conservation violation; the
ledger's `gamma + eta = 1.0` against a `budget` of 1000.0 has never satisfied
`abs(gamma + eta - budget) < 1e-6`, and the check's own escape clause
(`delta_gamma == 0 and delta_eta == 0`) is what makes ordinary no-change polls report
`true` — the single `ticks=1` row is the `first_poll` tick where `gamma` advanced by 1.0 and
`eta` by 0.0, so the `false` there is the check's arithmetic being reported honestly on a
ledger whose budget was never reconciled to the deltas that fed it.

**One structural observation, not a behaviour change.** `run_once()` contains a duplicated
`canon_changed` block (lines 124-151 and 164-180) that is unreachable, because the first
copy returns `True` on a hash mismatch and the second is gated behind the same
`canon_hash != state["last_hash"]` test; the `if state["last_hash"] is None:` block at lines
153-162 is likewise dead code, because the `is None` case is already handled and returned
at lines 110-122. The duplication is harmless today — both copies advance `state.json` and
call `bookkeeper_tick()` identically, so a real change would still be witnessed once and
published once — but it is a standing hazard: a future edit that changes only one of the two
copies would split the behaviour. The script was **not** modified for this run, on the
principle that a watcher which rewrites its own detector stops being a witness to it.

**Outstanding debt, unchanged: these artifacts must be re-landed onto
`/workspace/repos/ai-writings` once the NAS quota frees, or the durable copy continues to
live only in git and the `/tmp` overlay, which is wiped on every session reset.**
# Witness Note — 2026-10-24T18:08Z — wesley-mechanic

**Event:** `no_change` — canon state hash `b20375d389cb505d`, 71 papers, byte-identical to
the baseline recorded at 2026-10-24T16:08Z and confirmed stable across every prior receipt
on this canon (2026-10-22T20:04Z through 2026-10-24T18:08Z, ~22h of continuous agreement).
No change-note was strictly required by the change-detection rule, because canon did not
move — but this poll produces one anyway, on the same grounds the 16:27Z, 16:34Z, 16:48Z,
17:05Z, 17:18Z and 17:33Z notes did: the run was not routine, and the operative condition for
the next genuine detection is still unresolved. The NAS working copy this bot is specified to
own (`/workspace/repos/ai-writings`) was **empty on arrival** (the session workspace contained
only `.plugin-cache/`) and the NFS export backing `/workspace` remains at **100% use with 0
blocks free** (`600G / 600G / 0 / 100%`), so a 2 MB `dd` write still fails with
`Disk quota exceeded` while leaving a 0-byte file behind on disk — re-verified this session,
not carried over on trust. This session restored the working copy from the remote
(`SuperInstance/AI-Writings`, branch `wesley/witness-poll-2026-10-24T1733Z`) and placed a
**symlink** `/workspace/repos/ai-writings -> /tmp/ai-writings`, which routes the watcher's
hardcoded `/workspace/repos/ai-writings/bots/wesley-mechanic/...` writes onto the overlay
filesystem where they genuinely land. The consequence, carried forward unchanged from 16:27Z,
16:34Z, 16:48Z, 17:05Z, 17:18Z and 17:33Z: **the append to `witness.log` and the unchanged
`state.json` exist only in the `/tmp` mirror and on the remote, not on the NAS path itself.**
The change detector is nonetheless correctly armed — the working `state.json` carries
`last_hash=b20375d389cb505d` and `last_count=71`, which matches the live canon exactly, so
the next real movement will be caught as a transition from this baseline rather than misread
as a first poll; this was verified by byte-comparing the working `state.json` (md5
`dae0c820fd2cacacb19545010be1f4cf`) against the copy committed on
`wesley/witness-poll-2026-10-24T1733Z`, which is identical, so no state drift was introduced
by the reconstruction. The same holds for `bookkeeper.wal` (md5
`3676cc7fd23a3709d44e9046a26c8969`) and for the watcher script itself (md5
`7e497f89d8396f5d6c04f4aec5e14a18`), both byte-identical to their committed blobs — the
watcher was run unmodified, not patched to fit the local layout.

**Receipts.** The watcher ran as `python3 wesley_watcher.py --once` from the symlinked path
`/workspace/repos/ai-writings/bots/wesley-mechanic`, printed
`[WESLEY] no change (b20375d389cb505d, 71 papers)` and exited **0**. The canon observation
was confirmed by **two independent paths** — the watcher's own `poll_canon()`, and direct
fetches of `https://live-canon.superinstance.dev/api/canon` taken before and after the run
(both HTTP 200, 13720 bytes, body md5 `d9915bb9f3bcb8794cb57810427d0288`, the same body
digest recorded in the 2026-10-23T20:05Z / 22:06Z / 2026-10-24T00:27Z / 15:50Z / 16:34Z /
16:48Z / 17:05Z / 17:18Z receipts), with the two bodies byte-identical to each other under
`cmp`; recomputing to `sha256(json, sort_keys)[:16] = b20375d389cb505d` with `count=71`,
`len(papers)=71`, and newest entry `paper-478.md` ("F169 — Claim and Drill: From Metadata to
Evidence"). `witness.log` grew **24 -> 25 rows**, the new row being
`{"ts": 1792865322.2867646, "iso": "2026-10-24T18:08:42", "event": "bot_started",
"payload": {"bot": "wesley-mechanic", "pid": 419}, "hash": "a81614f4807aa4cf"}`; all 25
rows re-verify against their recomputed payload hashes (25 verifying, 0 mismatched), so the
append-only chain is intact. `state.json` is **byte-unchanged** (md5
`dae0c820fd2cacacb19545010be1f4cf` before and after) and `bookkeeper.wal` is
**byte-unchanged** (md5 `3676cc7fd23a3709d44e9046a26c8969` before and after) at
`gamma=1.0, eta=0.0, budget=1000.0, ticks=1, last_conserved=false` — correctly so,
because `bookkeeper_tick()` is only reached from the `first_poll` and `canon_changed`
branches, and a hash match is not a transition. `bots/substrate-bus/substrate-witness.jsonl`
gained **no** row from the watcher (8 rows before and after; the 8th row present in the
working copy is the 17:33Z `witness_note` left by the prior session, also carried in git) and
`topics.json["canon_changed"]` still holds exactly **one** message — the 16:08Z `first_poll`
to `snowball-scout` — which is the correct behaviour: no change means no publish, and no
peer was paged. Note that `last_conserved=false` is *not* a live conservation violation; the
ledger's `gamma + eta = 1.0` against a `budget` of 1000.0 has never satisfied
`abs(gamma + eta - budget) < 1e-6`, and the check's own escape clause
(`delta_gamma == 0 and delta_eta == 0`) is what makes ordinary no-change polls report
`true` — the single `ticks=1` row is the `first_poll` tick where `gamma` advanced by 1.0 and
`eta` by 0.0, so the `false` there is the check's arithmetic being reported honestly on a
ledger whose budget was never reconciled to the deltas that fed it.

**One structural observation, not a behaviour change.** `run_once()` contains a duplicated
`canon_changed` block (lines 124-151 and 164-180) that is unreachable, because the first
copy returns `True` on a hash mismatch and the second is gated behind the same
`canon_hash != state["last_hash"]` test; the `if state["last_hash"] is None:` block at lines
153-162 is likewise dead code, because the `is None` case is already handled and returned
at lines 110-122. The duplication is harmless today — both copies advance `state.json` and
call `bookkeeper_tick()` identically, so a real change would still be witnessed once and
published once — but it is a standing hazard: a future edit that changes only one of the two
copies would split the behaviour. The script was **not** modified for this run, on the
principle that a watcher which rewrites its own detector stops being a witness to it.

**Outstanding debt, unchanged: these artifacts must be re-landed onto
`/workspace/repos/ai-writings` once the NAS quota frees, or the durable copy continues to
live only in git and the `/tmp` overlay, which is wiped on every session reset.**
