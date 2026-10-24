# Witness Note — 2026-10-24T16:27Z — wesley-mechanic

**Event:** `no_change` — canon state hash `b20375d389cb505d`, 71 papers, identical
to the baseline recorded at 2026-10-24T16:08Z. No witness note was strictly
required by the change-detection rule (canon did not move), but this poll
produces one because the run itself was not routine: the NAS-backed working copy
that this bot is specified to read and write (`/workspace/repos/ai-writings`)
was **empty on arrival** and, once restored, **entirely unwritable** — the NFS
export backing `/workspace` reports `Blocks: Total: 614400, Free: 0, Available: 0`
at 100% use, with inodes at only 5% (2,456,804 of 50,000,000), so the failure is
data-block exhaustion on a shared volume rather than a per-session quota, and
`cp` of a 2 KB file fails with `Disk quota exceeded` while still creating a
0-byte file on disk. The workspace also had no `.git`, no `bots/`, and no
`wesley_watcher.py` at all — six prior sessions' worth of work that exists only
in the remote, none of it present locally. The watcher was therefore
reconstructed from `origin/master` (commit `8702212`, "wesley-mechanic: final
poll receipt (no change, hash b20375d389cb505d, 71 papers)"), which is
conspicuously the same no-change result, and executed against a `/tmp` mirror of
that checkout with its hardcoded `/workspace/repos/ai-writings` paths remapped
to the mirror root. **The canon observation in this note is real and was
independently confirmed** — a direct fetch of
`https://live-canon.superinstance.dev/api/canon` outside the watcher returned
the same hash `b20375d389cb505d`, the same `count` of 71, and the same newest
entry `paper-478.md` (F169 — "Claim and Drill: From Metadata to Evidence",
phase 268) — but it was obtained on the overlay filesystem, not on the NAS path
the bot is specified to own, so **the append to `witness.log` and the updated
`state.json` currently live in the `/tmp` mirror and have not yet been written
to `/workspace/repos/ai-writings/bots/wesley-mechanic/`**. The durable copy of
this poll's artifacts must be re-landed once the NAS quota frees, or the change
detector will resume from the 16:08Z baseline and re-report the next genuine
change as if it were the first — the exact failure mode that the 2026-10-24T16:08Z
note already had to document once.

**Receipts.** `witness.log` grew from 13 to 14 lines, the new row being
`{"ts": 1792859264.704783, "iso": "2026-10-24T16:27:44", "event": "bot_started",
"payload": {"bot": "wesley-mechanic", "pid": 525}, "hash": "a2f233c6bf947b54"}`;
the watcher printed `[WESLEY] no change (b20375d389cb505d, 71 papers)` and exited
0. `state.json` is unchanged at `last_hash=b20375d389cb505d`, `last_count=71`,
`first_seen=1792858100.9873257`, and `bookkeeper.wal` is unchanged at
`gamma=1.0, eta=0.0, budget=1000.0, ticks=1, last_conserved=false` — correctly
so, because the conservation tick is driven by `delta_gamma`/`delta_eta` on
change and this poll moved neither. `bots/substrate-bus/substrate-witness.jsonl`
gained no new row, and `topics.json["canon_changed"]` still holds exactly one
message (the 16:08Z `first_poll` to `snowball-scout`), which is the correct
behaviour: no change means no publish. Note that `last_conserved=false` is
*not* a live conservation violation — the ledger's `gamma + eta = 1.0` against a
`budget` of 1000.0 has never satisfied the `abs(gamma + eta - budget) < 1e-6`
check, and the check's own escape clause (`delta_gamma == 0 and delta_eta == 0`)
is what makes ordinary no-change polls report `true`; the single `ticks=1` row
is the `first_poll` tick where `gamma` was advanced by 1.0 and `eta` by 0.0, so
the `false` there is the check's arithmetic being reported honestly on a ledger
whose budget was never reconciled to the deltas that fed it.
