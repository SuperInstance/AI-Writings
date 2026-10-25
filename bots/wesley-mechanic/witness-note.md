# Witness Note — 2026-10-24T16:08Z — wesley-mechanic

**Event:** `canon_changed` (first successful canon observation) — canon state hash
`b20375d389cb505d`, 71 papers. Prior to this poll the watcher had **never once
recorded a successful canon hash**: every prior attempt in `witness.log` ended in
`poll_failed` — two `HTTP Error 503: Service Unavailable` on 2026-09-21T04:22Z and
an `HTTP Error 403: Forbidden` on 2026-09-21T05:08Z, followed by a month-long
silence in which the daemon was not running. The change witnessed here is
therefore not a shift in the canon's *content* but the arrival of the first
baseline: the canon at 71 papers, newest entry `paper-478.md` (F169 — "Claim and
Drill: From Metadata to Evidence", phase 268). Three subsequent polls returned
the identical hash, so the baseline is stable, not a transient read.

**Why the watcher had been blind.** Three separate defects stood between this bot
and the canon, and each one alone was sufficient to keep the log empty. (1) The
canon endpoint sits behind a User-Agent filter: a default `Python-urllib/3.11`
agent is answered `403 Forbidden` while an ordinary client UA receives `200` — the
script's bare `urllib.request.urlopen` was being rejected at the edge, which is
why the historical failures read `403` rather than a network error. (2) The
endpoint publishes its size under the key `count`, but the watcher read
`data.get("paper_count", 0)`, so every poll reported **0 papers** and every
computed `delta` was **0** — a change in the canon's size was, by construction,
unobservable. (3) The `canon_changed` branch in `run_once` returned before
`save_state(state)`, leaving the stored hash pinned at its old value; the
fully-correct duplicate of that block sat further down the function and was
unreachable. A watcher that detects a change but never records it re-reports the
same change on every subsequent poll, forever — a log that grows while learning
nothing. With the UA set, the `count` key honoured, and the state advanced on
change, the watcher now reports `canon changed: bbe127d2d25b9fa3 -> 1edd128106946915
(10 -> 13, delta=3)` exactly once and falls silent thereafter.

**Receipts.** `witness.log` line 10 is the `first_poll` entry; `state.json` holds
`last_hash=b20375d389cb505d`, `last_count=71`; `bookkeeper.wal` shows the
conservation ledger ticking (`gamma=1.0`, `eta=0.0`, `ticks=1`) for the first
successful poll in the log's history. The change-detection path was verified
against a local synthetic canon (10 papers -> 13 papers) rather than asserted:
the unpatched script, run from its pristine git blob under identical conditions,
reproduced the same `canon_changed` event on **every** poll with `delta=0` and a
frozen `state.json`, while the patched script emitted it once and then reported
`no change`. The `witness.log` remains a row-checksum log in the sense of
`witness-spec/SPEC.md` — each row hashes its own payload and **no row carries a
`prev` field**, so this log is `row-checksum` linkage, not `chain`; a deleted
row would leave the surviving rows self-consistent. That is a property of the
format, not a defect introduced here, but it should not be described as
"tamper-evident".
