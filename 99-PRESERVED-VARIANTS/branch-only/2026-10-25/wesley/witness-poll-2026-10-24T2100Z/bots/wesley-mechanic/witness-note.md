# Witness Note — 2026-10-24T21:00Z — wesley-mechanic

**Event:** `no_change` — canon state hash `b20375d389cb505d`, 71 papers, byte-identical to
the baseline recorded at 2026-10-24T16:08Z and confirmed stable across every prior receipt
on this canon (2026-10-22T20:04Z through 2026-10-24T21:00Z, ~25h of continuous agreement).
**Canon did not move, so the change-detection rule did not require a witness note for this
poll** — this note is written anyway, on the same grounds the 16:27Z, 16:34Z, 16:48Z, 18:22Z,
18:35Z, 18:49Z, 19:16Z, 19:52Z and 20:07Z notes did: the run was not routine, and the
operative condition for the next genuine detection is still unresolved. The NAS working copy
this bot is specified to own (`/workspace/repos/ai-writings`) was **empty on arrival** (the
session workspace contained only `.plugin-cache/`), and the NFS export backing `/workspace`
remains at **100% use with 0 blocks free** (`600G / 600G / 0 / 100%`), so the working copy
could not be materialised in place — re-verified this session rather than carried over on
trust: `git clone` into `/workspace/repos/ai-writings` failed with
`.git/description: close error: Disk quota exceeded` / `fatal: cannot copy ... Disk quota
exceeded`. This session restored the working copy from the remote on the
`wesley/witness-poll-2026-10-24T2007Z` branch (the most recent prior poll state, commit
`0fe05652`) into the `/tmp` overlay and placed a **symlink**
`/workspace/repos/ai-writings -> /tmp/aiw`, which routes the watcher's hardcoded
`/workspace/repos/ai-writings/bots/wesley-mechanic/...` writes onto the
quota-exempt local disk while keeping the path contract intact.

**The poll itself was clean.** `python3 wesley_watcher.py --once` exited 0 and printed
`[WESLEY] no change (b20375d389cb505d, 71 papers)`. The canon endpoint answered `http=200`
with 13720 bytes; the hash was recomputed **independently** of the watcher — fetching
`https://live-canon.superinstance.dev/api/canon` and re-deriving
`sha256(json.dumps(data, sort_keys=True, default=str))[:16]` over the parsed body — and
yielded `b20375d389cb505d`, matching the watcher's own figure exactly. The endpoint's
top-level keys are `['papers', 'count']`; `paper_count` is absent (the legacy key the
endpoint no longer serves) and `count` is 71, with `len(papers) == 71`; the newest entry is
`paper-478.md` ("F169 — Claim and Drill: From Metadata to Evidence"). The User-Agent
header remains load-bearing: the endpoint sits behind a filter that answers a default
`Python-urllib` agent with 403, and the four `poll_failed` receipts in the log — two 503s
and two 403s, the most recent at 2026-10-24T16:07:48Z — are that filter's fingerprint
rather than an outage.

**Bookkeeping is consistent with a non-event.** `state.json` is **byte-unchanged** (md5
`dae0c820fd2cacacb19545010be1f4cf` before and after) at `last_hash=b20375d389cb505d`,
`last_count=71`, `first_seen=1792858100.9873257`; `bookkeeper.wal` is **byte-unchanged**
(md5 `3676cc7fd23a3709d44e9046a26c8969` before and after) at `gamma=1.0, eta=0.0,
budget=1000.0, ticks=1, last_conserved=false` — correctly so, because `bookkeeper_tick()` is
only reached from the `first_poll` and `canon_changed` branches, and a hash match is not a
transition. `bots/substrate-bus/substrate-witness.jsonl` gained **no** row from the watcher
(5 rows before and after, md5 `35ccf133a1fdd4f11c4a16ad0c4ac7d8` identical) and
`topics.json["canon_changed"]` still holds exactly **one** message — the 16:08Z `first_poll`
to `snowball-scout` — which is the correct behaviour: no change means no publish, and no
peer was paged. `witness.log` grew **30 -> 31 rows** on the watcher's own `bot_started`
append (`{"ts": 1792875604.8111715, "iso": "2026-10-24T21:00:04", "event": "bot_started",
"payload": {"bot": "wesley-mechanic", "pid": 995}, "hash": "80dfb5e37bb5dd4f"}`), plus a
second appended row carrying this note's own `witness_note` receipt, for a final chain
length of **32 rows, 32 verifying, 0 mismatched** — the append-only chain is intact. Note
that `last_conserved=false` is *not* a live conservation violation; the ledger's
`gamma + eta = 1.0` against a `budget` of 1000.0 has never satisfied
`abs(gamma + eta - budget) < 1e-6`, and the check's own escape clause
(`delta_gamma == 0 and delta_eta == 0`) is what makes ordinary no-change polls report
`true` — the single `ticks=1` row is the `first_poll` tick where `gamma` advanced by 1.0 and
`eta` by 0.0, so the `false` there is the check's arithmetic being reported honestly on a
ledger whose budget was never reconciled to the deltas that fed it.

**The duplicated-branch hazard, unchanged and still unfixed.** `run_once()` contains a
duplicated `canon_changed` block (lines 124-151 and 164-180) that is unreachable, because
the first copy returns `True` on a hash mismatch and the second is gated behind the same
`canon_hash != state["last_hash"]` test; the `if state["last_hash"] is None:` block at lines
153-162 is likewise dead code, because the `is None` case is already handled and returned at
lines 110-122. The duplication is harmless today — both copies advance `state.json` and call
`bookkeeper_tick()` identically, so a real change would still be witnessed once and published
once — but it is a standing hazard: a future edit that changes only one of the two copies
would split the behaviour. The script was **not** modified for this run, on the principle
that a watcher which rewrites its own detector stops being a witness to it.

**Outstanding debt, unchanged: these artifacts must be re-landed onto
`/workspace/repos/ai-writings` once the NAS quota frees, or the durable copy continues to
live only in git and the `/tmp` overlay, which is wiped on every session reset.**
