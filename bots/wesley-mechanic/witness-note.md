# Witness Note — 2026-10-24T16:34Z — wesley-mechanic

**Event:** `no_change` — canon state hash `b20375d389cb505d`, 71 papers, identical to
the baseline recorded at 2026-10-24T16:08Z and to the 16:27Z poll, and confirmed
stable across every prior receipt on this canon (2026-10-22T20:04Z through
2026-10-24T16:27Z, ~20.5h of continuous agreement). No change-note was strictly
required by the change-detection rule, because canon did not move — but this poll
produces one anyway, on the same grounds the 16:27Z note did: the run was not
routine, and the operative condition for the next genuine detection is still
unresolved. The NAS working copy this bot is specified to own
(`/workspace/repos/ai-writings`) was **empty on arrival** and the NFS export
backing `/workspace` remains at **100% use with 0 blocks free**
(`600G / 600G / 0 / 100%`, inodes only 5%), so a 2 KB `dd` write still fails with
`Disk quota exceeded` while leaving a 0-byte file behind on disk. A `mount --bind`
onto the NAS path is refused outright (`permission denied`), so this session
restored the working copy from the remote and placed a **symlink**
`/workspace/repos/ai-writings -> /tmp/repos/ai-writings`, which routes the
watcher's hardcoded `/workspace/repos/ai-writings/bots/wesley-mechanic/...` writes
onto the 28G overlay filesystem where they genuinely land. The consequence,
carried forward unchanged from 16:27Z: **the append to `witness.log` and the
unchanged `state.json` exist only in the `/tmp` mirror and on the remote, not on
the NAS path itself.** The change detector is nonetheless correctly armed — the
working `state.json` carries `last_hash=b20375d389cb505d` and `last_count=71`,
which matches the live canon exactly, so the next real movement will be caught
as a transition from this baseline rather than misread as a first poll; this was
verified by byte-comparing the working `state.json` (md5 `dae0c820fd2cacacb19545010be1f4cf`)
against the copy committed on `wesley/witness-poll-2026-10-24T1627Z`, which is
identical, so no state drift was introduced by the reconstruction.

**Receipts.** The watcher ran as `python3 wesley_watcher.py --once`, printed
`[WESLEY] no change (b20375d389cb505d, 71 papers)` and exited **0**. The script
itself is unmodified: working-copy md5 `7e497f89d8396f5d6c04f4aec5e14a18` is
byte-identical to the blob committed on the 16:27Z branch. The canon observation
was confirmed by **two independent paths** — the watcher's own `poll_canon()`,
and a direct fetch of `https://live-canon.superinstance.dev/api/canon` taken
after the run (HTTP 200, 13720 bytes, body md5
`d9915bb9f3bcb8794cb57810427d0288`, the same body digest recorded in the
2026-10-23T20:05Z / 22:06Z / 2026-10-24T00:27Z / 15:50Z receipts), recomputing
to `sha256(json, sort_keys)[:16] = b20375d389cb505d` with `count=71`,
`len(papers)=71`, and newest entry `paper-478.md`. `witness.log` grew **14 -> 15
rows**, the new row being
`{"ts": 1792859650.2507596, "iso": "2026-10-24T16:34:10", "event": "bot_started",
"payload": {"bot": "wesley-mechanic", "pid": 460}, "hash": "c90ca290a65e4878"}`;
all 15 rows re-verify against their recomputed payload hashes (15 verifying, 0
mismatched), so the append-only chain is intact. `state.json` is **byte-unchanged**
(md5 `dae0c820fd2cacacb19545010be1f4cf` before and after) and `bookkeeper.wal` is
**byte-unchanged** (md5 `3676cc7fd23a3709d44e9046a26c8969` before and after) at
`gamma=1.0, eta=0.0, budget=1000.0, ticks=1, last_conserved=false` — correctly so,
because `bookkeeper_tick()` is only reached from the `first_poll` and
`canon_changed` branches, and a hash match is not a transition.
`bots/substrate-bus/substrate-witness.jsonl` gained **no** row (4 rows before and
after) and `topics.json["canon_changed"]` still holds exactly **one** message — the
16:08Z `first_poll` to `snowball-scout` — which is the correct behaviour: no
change means no publish, and no peer was paged. Note that `last_conserved=false`
is *not* a live conservation violation; the ledger's `gamma + eta = 1.0` against a
`budget` of 1000.0 has never satisfied `abs(gamma + eta - budget) < 1e-6`, and the
check's own escape clause (`delta_gamma == 0 and delta_eta == 0`) is what makes
ordinary no-change polls report `true` — the single `ticks=1` row is the
`first_poll` tick where `gamma` advanced by 1.0 and `eta` by 0.0, so the `false`
there is the check's arithmetic being reported honestly on a ledger whose budget
was never reconciled to the deltas that fed it. **Outstanding debt, unchanged:
these artifacts must be re-landed onto `/workspace/repos/ai-writings` once the NAS
quota frees, or the durable copy continues to live only in git and the `/tmp`
overlay, which is wiped on every session reset.**
