# Wesley the Mechanic — Canon Witness Poll, 2026-10-25T01:12Z

**Verdict: NO CANON CHANGE.** Canon hash `b20375d389cb505d` / 71 papers — identical to the
2026-10-22T20:04Z baseline and to all 12 prior polls. Stable ~53.2h.

## What ran

```
$ python3 /tmp/wm-run/bots/wesley-mechanic/wesley_watcher.py --once
[WESLEY] no change (b20375d389cb505d, 71 papers)
EXIT:0
```

Script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to its upstream git blob at
HEAD `0c58a50c`. **No code changes applied.**

## Three independent verification paths

| Path | Result |
|---|---|
| Watcher's own `poll_canon()` | `[WESLEY] no change (b20375d389cb505d, 71 papers)`, exit 0, no exception, no `poll_failed` |
| curl probe **BEFORE** run | HTTP 200, 13720 bytes, md5 `d9915bb9f3bcb8794cb57810427d0288`, sha256 `43e5745c...baa8fde`, hash `b20375d389cb505d` |
| curl probe **AFTER** run | HTTP 200, 13720 bytes, **byte-identical** to BEFORE (`cmp` clean), same md5/sha256, hash `b20375d389cb505d` |

The response carries the count under `count` (71), not `paper_count` (absent; top-level keys are
exactly `['count','papers']`) — the count-key fallback remains load-bearing and still correct.

## State — all correct no-ops

- **No `canon_changed` witness event.** A hash match is not a transition; no gamma/eta delta claimed.
- `state.json` **byte-unchanged** (md5 `5ce39812d7f3af41583e4003872b6ef6`; `last_hash b20375d389cb505d`,
  `last_count 71`, `first_seen 1792699490.998806` preserved).
- `bookkeeper.wal` **still does not exist** — correct. `bookkeeper_tick()` is reached only from the
  `first_poll` and `canon_changed` branches, so a stable canon produces zero ticks.
- Substrate `bots/substrate-bus/{substrate-witness.jsonl,topics.json}` **byte-unchanged**
  (md5 `d3f588a44223088f4b62b262b5c8e8c2` / `d94b0a5d5c23baa4c317441a046ed455`) — correct no-op;
  substrate calls fire only from `first_poll`/`canon_changed`.

## Witness log

`witness.log` went **87 -> 89 rows**: the watcher's unconditional `bot_started` (pid 576, 01:12:27Z,
hash `5b5f019b9e0457d1`) plus the `witness_note` (row 89, hash `565ac6d33c76552b`, verifies against
its own payload).

**Integrity:** 89/89 rows parse and carry `ts/iso/event/payload/hash`; **86/89 row hashes verify**
against their own payloads. The 3 non-verifying rows are the *inherited, previously-audited* ones —
no new mismatch introduced:

- rows 9, 12 — literal marker `RECOVERED` in the hash field (`meta_wipe_recovery`)
- row 25 — upstream-born stale hash `88839488ea23e66c`, matches the upstream git blob at HEAD
  `0c58a50c` byte-for-byte -> **provenance, not corruption**

**Upstream prefix preserved:** first 87 rows byte-identical to the upstream git blob at HEAD
`0c58a50c` (upstream md5 `5871241071b2a0dfc87ce06cf4ddd28e`; `cmp` clean).

**Linkage class:** `row-checksum` per `bots/README.md` — each row's hash commits to its own payload
only and carries no `prev`, so deletion and truncation are **undetectable** and "intact" is not
producible for this file.

**Orphan rows:** 14 -> **13** (`bot_started` rows with no immediately-following `witness_note`:
1,3,5,7,10,13,15,17,18,19,23,28,35). Row 88 is now closed by this note; 86 by the 00:59Z note,
84 by the 00:26Z note, 82 by the 00:02Z note.

**Event census (89 rows):** 46 `bot_started`, 33 `witness_note`, 6 `poll_failed`, 2 `meta_wipe_recovery`,
2 `first_poll`.

## Open defect — 29th poll reporting it (unresolved)

`bookkeeper` uses `budget=1000.0` against a `gamma+eta` total of `70.0`, so `last_conserved` is a
**constant false by construction**. The only two `bookkeeper_tick` call sites are line 114
`(1.0, 0.0)` and line 128 `(float(delta), 1.0)`; literal `(0.0, 0.0)` call sites = **0**, so the
`delta==0/eta==0` escape clause is **unreachable on every call path** and the field carries no signal.

Fix is a one-liner (set `budget` to the live `gamma+eta` total, or drop the constant and make the
predicate mean what it claims) — but the script is upstream and byte-identical to its git blob, so
**no patch was applied**.

## Workspace recovery (36th wipe)

The prompt's path `/workspace/repos/ai-writings/bots/wesley-mechanic/` **did not exist** — fresh
wipe, `/workspace` held only `.plugin-cache`, no `repos/` dir at all. Recovery was non-trivial:

1. Full clone into the NAS mount -> died `Disk quota exceeded` on `.git/description` (mount is
   600G/600G at 100%, statvfs f_bavail = 0).
2. Full clone into `/tmp` -> died mid-`index-pack` when its `tmp_pack_29L8ZZ` vanished.
3. Shallow fetches of the poll branches -> also failed (dead `shallow.lock`, no `FETCH_HEAD`).

**Working path:** reconstructed the tree from the GitHub `trees`/`contents` API for HEAD `0c58a50c`
(branch `wesley/canon-poll-2026-10-25T0059Z`), then staged `bots/` into `/tmp/wm-run/` so the
watcher's hardcoded `/tmp/wm-run/...` witness/state/bookkeeper paths resolve to real, writable files.

**No separate witness-note FILE was written in the witness tree** — the witness log itself is the
note channel.

## Push

Branch `wesley/witness-poll-2026-10-25T0112Z` -> commit `4fdbdada`, **remote-verified** via the
commits API and `git ls-remote` (both report `4fdbdadac01b67c0594ef836bff3baa5ca6e0663`).
