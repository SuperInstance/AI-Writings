# Wesley — Canon Poll 2026-10-25T03:33Z

**Verdict: NO CANON CHANGE.** Hash `b20375d389cb505d`, 71 papers — unchanged.

## Run

| Field | Value |
|---|---|
| Command | `python3 /workspace/repos/ai-writings/bots/wesley-mechanic/wesley_watcher.py --once` |
| Exit | 0 |
| Stdout | `[WESLEY] no change (b20375d389cb505d, 71 papers)` |
| Baseline | 2026-10-22T20:04Z (`state.json first_seen 1792699490.998806`) |
| Stable since | ~55.5h (~15 min since the 03:17Z poll) |
| Witness log | 93 -> 95 rows (1 `bot_started` from the run, 1 `witness_note` from this poll) |
| `state.json` | byte-unchanged (md5 `5ce39812d7f3af41583e4003872b6ef6`) |
| `bookkeeper.wal` | still absent — correct no-op (ticks only from `first_poll` / `canon_changed`) |
| Substrate | byte-unchanged (`d3f588a4…` / `d94b0a5d…`, 4 rows) — correct no-op |
| Script md5 | `206682962c06f9814a5db65c2fbc7267` — byte-identical to upstream blob, no patch applied |

## Verification — three independent paths

1. **Watcher `poll_canon()`** — stdout above, exit 0, no exception, no `poll_failed` row.
2. **curl probe BEFORE the run** — HTTP 200, 13720 bytes, body md5 `d9915bb9f3bcb8794cb57810427d0288`,
   sha256 `43e5745c369f9b1fc8e19607eb96c6cfae676248e329f53715755ebe2baa8fde`,
   recomputes to `sha256(json, sort_keys)[:16] = b20375d389cb505d`.
3. **curl probe AFTER the run** — HTTP 200, 13720 bytes, same md5/sha256; `cmp` of the
   before/after bodies clean.

All three bodies are byte-identical to each other and to the 01:12Z / 01:18Z / 03:17Z
baseline bodies. The response carries the count under `count` (71), **not** `paper_count`
(absent; top-level keys are exactly `['count','papers']`), so the count-key fallback on
line 86 remains load-bearing and still correct.

**No canon-change witness event was written and no gamma/eta delta is claimed** — a hash
match is not a transition. The conditional witness-note FILE in the task was therefore
not triggered; the witness log itself is the note channel, and this note is row 95.

## Log integrity

- 95/95 rows parse; all carry `ts`/`iso`/`event`/`payload`/`hash`. 92 row hashes verify
  against their own payloads.
- 3 non-verifying rows are the inherited, previously-audited ones; no new mismatch:
  - rows 9, 12 — literal marker `RECOVERED` in the hash field (`meta_wipe_recovery`).
  - row 25 — upstream-born stale hash `88839488ea23e66c`; row md5
    `65784c40fae50ac192a3f6c96fed6675` on both the upstream blob at HEAD `b98c04e` and
    our copy, byte-for-byte. Provenance, not corruption.
- **Linkage class: `row-checksum`.** Each row's hash commits to its own payload only and
  carries no `prev`, so deletion and truncation of a row are UNDETECTABLE. The honest
  verdict is "92/95 machine-written checksums verify, 2 are RECOVERED markers, 1 is the
  known stale row 25 — linkage class row-checksum", **not** "chain-intact".
- **Upstream prefix preserved:** first 93 rows byte-identical to the upstream git blob at
  HEAD `b98c04e` (`cmp` clean). `diff` of upstream vs staged shows exactly one added row.
- Orphan `bot_started` rows: 13 (rows 1,3,5,7,10,13,15,17,18,19,23,28,35). Row 94 is
  closed by row 95.

## Workspace (38th wipe)

The prompt's path `/workspace/repos/ai-writings/bots/wesley-mechanic/` did not exist —
`/workspace` contained only `.plugin-cache`, no `repos/` dir at all. The NAS mount is
600G/600G at 100% (`statvfs f_bavail = 0`), so a clone into it would die
`Disk quota exceeded`.

Recovered into the overlay instead. The live repo is `SuperInstance/AI-Writings`;
`main` carries only `cellular-first-design/` (82 files) and **no `bots/` tree**, so branch
`wesley/witness-poll-2026-10-25T0317Z` was checked out (HEAD `b98c04e`), which carries
`bots/wesley-mechanic/` and `bots/substrate-bus/`. The `bots/` tree was staged into
`/tmp/wm-run` so the watcher's hardcoded `/tmp/wm-run/...` witness/state/bookkeeper paths
resolve to real, writable files, and `/workspace/repos/ai-writings` was symlinked to the
recovered clone so **both** the prompt path and `substrate_bus.py`'s hardcoded
`/workspace/repos/ai-writings/bots/substrate-bus/` paths resolve.

## Open defect — still unresolved (32nd poll reporting it)

`bookkeeper_tick` uses `budget=1000.0` against a gamma+eta total of 70.0, so
`last_conserved` is a constant false by construction.

- Only two call sites: line 114 `(1.0, 0.0)` and line 128 `(float(delta), 1.0)`.
- Reachable gamma+eta totals: 1.0, 2.0, 0.0, 11.0 — none equals 1000.0, and none is the
  `(0.0, 0.0)` literal pair, so the `delta == 0 and eta == 0` escape clause is
  **UNREACHABLE on every call path**.
- Consequence: `last_conserved` is `False` everywhere and carries no signal.

Fix is a one-liner (set `budget` to the live gamma+eta total, or drop the constant and
make the predicate mean what it claims), but the script is upstream and byte-identical to
its git blob, so no patch was applied.
