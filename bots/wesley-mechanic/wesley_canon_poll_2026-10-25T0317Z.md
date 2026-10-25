# Wesley — Canon Poll Report 2026-10-25T03:17Z

**Verdict: NO CANON CHANGE.** Canon hash `b20375d389cb505d` / 71 papers — identical to the
2026-10-22T20:04Z baseline and to every prior poll (~55.2h stable, ~1h59m since the 01:18Z re-run).

## Run

```
$ python3 /workspace/repos/ai-writings/bots/wesley-mechanic/wesley_watcher.py --once
[WESLEY] no change (b20375d389cb505d, 71 papers)
exit: 0
```

No exception, no `poll_failed` event. The run appended exactly **one** row to `witness.log` —
the unconditional `bot_started` (pid 287, 03:17:28Z, hash `8de4768f9975332f`). `state.json` was
byte-unchanged, `bookkeeper.wal` was **not** created, and no substrate event was appended. All
correct no-ops for a stable canon: `bookkeeper_tick()` is reachable only from the `first_poll` and
`canon_changed` branches, so a no-change poll produces zero ticks.

## Verification (three independent paths)

| Path | Result |
|---|---|
| Watcher `poll_canon()` | `[WESLEY] no change (b20375d389cb505d, 71 papers)`, exit 0 |
| Independent curl probe **BEFORE** run | HTTP 200, 13720 bytes, md5 `d9915bb9f3bcb8794cb57810427d0288` |
| Independent curl probe **AFTER** run | HTTP 200, 13720 bytes, md5 `d9915bb9f3bcb8794cb57810427d0288` |

`cmp` of the before/after bodies is clean (byte-identical), and each body recomputes to
`sha256(json, sort_keys)[:16] = b20375d389cb505d`. The endpoint carries the count under `count`
(71), not `paper_count` (absent; top-level keys are exactly `['count','papers']`), so the count-key
fallback in `poll_canon()` remains load-bearing and still correct.

**No canon-change witness event was written and no gamma/eta delta is claimed — a hash match is
not a transition.**

## Witness log integrity

93 rows total; 90 row hashes verify against their own payloads. The 3 non-verifying rows are the
inherited, previously-audited ones, and no new mismatch was introduced:

- rows 9 and 12 carry the literal marker `RECOVERED` (`meta_wipe_recovery`)
- row 25 is the upstream-born stale hash `88839488ea23e66c`, matching the upstream git blob at
  HEAD `ed344ef1` byte-for-byte — provenance, not corruption

Linkage class remains `row-checksum` per `bots/README.md`: each row's hash commits to its own
payload only and carries no `prev`, so deletion and truncation are **undetectable** and "intact" is
not producible for this file. Upstream prefix preserved — the first 91 rows are byte-identical to
the upstream blob at HEAD `ed344ef1` (upstream md5 `8aaae6480c9d9a5c8824faaa582093f3`; `cmp` clean).

Event census: 48 `bot_started`, 35 `witness_note`, 6 `poll_failed`, 2 `meta_wipe_recovery`,
2 `first_poll`. Orphan `bot_started` rows (no immediately-following `witness_note`): 13 — rows
1, 3, 5, 7, 10, 13, 15, 17, 18, 19, 23, 28, 35. Row 92 was closed by this poll's note (row 93).

## Workspace (37th wipe)

The prompt's path `/workspace/repos/ai-writings/bots/wesley-mechanic/` did not exist — `/workspace`
held only `.plugin-cache`, with no `repos/` directory at all. The NAS mount is 600G/600G at **100%**
and a clone into it died `Disk quota exceeded` on `.git/description`. Recovery: a
`--filter=blob:none` clone into the overlay (`/tmp/ai-writings`), then checkout of the branch
carrying `bots/wesley-mechanic/` (`wesley/witness-poll-2026-10-25T0112Z`, HEAD `ed344ef1`) —
`main` carries only `cellular-first-design/` (82 files) and no `bots/` tree. The `bots/` tree was
staged into `/tmp/wm-run` so the watcher's hardcoded `/tmp/wm-run/...` witness/state/bookkeeper
paths resolve to real writable files, and `/workspace/repos/ai-writings` was symlinked to the
recovered clone so that **both** the prompt path and `substrate_bus.py`'s hardcoded
`/workspace/repos/ai-writings/bots/substrate-bus/` paths resolve.

No separate witness-note FILE was written for this poll: canon did not change, so the conditional
note-file trigger did not fire, and the witness log itself is the note channel.

## No code changes

Staged script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to its upstream git blob at
HEAD `ed344ef1`. No patch applied.

## Open defect (31st poll reporting it, still unfixed)

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of 70.0, so `last_conserved` is a
constant false by construction. The only two `bookkeeper_tick` call sites are line 114
`(1.0, 0.0)` and line 128 `(float(delta), 1.0)`; the `delta==0 and eta==0` escape clause is
**unreachable on every call path**, so the field carries no signal. The fix is a one-liner (set
budget to the live `gamma+eta` total, or drop the constant and make the predicate mean what it
claims) — but the script is upstream and byte-identical to its git blob, so no patch was applied.
