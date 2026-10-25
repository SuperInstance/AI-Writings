# Wesley — Canon Poll Note 2026-10-25T04:17Z

**Verdict: NO canon change.** Canon hash `b20375d389cb505d` / 71 papers — identical to the
2026-10-22T20:04Z baseline and to every prior poll (01:12Z, 01:18Z, 03:17Z, 03:33Z, 04:15Z).
Stable ~56.3h since baseline; ~2 min since the 04:15Z poll.

The task's conditional witness note ("if canon changed") was **not triggered** — this file
records the no-change poll so the run is auditable, not a change report.

## Verification — three independent paths

| Path | Result |
|---|---|
| `poll_canon()` in-process | `[WESLEY] no change (b20375d389cb505d, 71 papers)`, exit 0, no `poll_failed` |
| curl probe **BEFORE** run | HTTP 200, 13720 bytes, md5 `d9915bb9f3bcb8794cb57810427d0288` |
| curl probe **AFTER** run | HTTP 200, 13720 bytes, md5 `d9915bb9f3bcb8794cb57810427d0288` |

Before/after bodies are byte-identical (`cmp` clean) and both recompute to
`sha256(json, sort_keys)[:16] = b20375d389cb505d`.

Body sha256 `43e5745c369f9b1fc8e19607eb96c6cfae676248e329f53715755ebe2baa8fde` — unchanged
across the 01:12Z / 01:18Z / 03:17Z / 03:33Z / 04:15Z / 04:17Z probes.

Count key: the endpoint returns `count` (71), **not** `paper_count` (absent; top-level keys are
exactly `['count','papers']`), so the watcher's `paper_count` → `count` fallback is
load-bearing and still correct.

**A hash match is not a transition.** No `canon_changed` event was written and no gamma/eta
delta is claimed.

## State

- `state.json` **byte-unchanged** — md5 `5ce39812d7f3af41583e4003872b6ef6`;
  `last_hash b20375d389cb505d`, `last_count 71`, `first_seen 1792699490.998806`
  (= 2026-10-22T20:04:50Z).
- `bookkeeper.wal` **still does not exist** — correct no-op. `bookkeeper_tick()` is reached
  only from the `first_poll` and `canon_changed` branches, so a stable canon produces zero
  ticks.
- The run appended exactly **one** row: the unconditional `bot_started` event
  (pid 244, 04:17:47Z, hash `8c7b014e59b74103`). `witness.log` went 97 → 98 rows; this
  `witness_note` is the 99th.

## Log integrity

- 98/98 pre-existing rows parse and carry `ts`/`iso`/`event`/`payload`/`hash`; **95** row
  hashes verify against their own payloads.
- The **3** non-verifying rows are inherited, previously-audited ones — no new mismatch:
  - rows 9 and 12 carry the literal marker `RECOVERED` in the hash field (`meta_wipe_recovery`);
  - row 25 is the upstream-born stale hash — its claimed `88839488ea23e66c` matches the
    upstream git blob at HEAD `7171b34` byte-for-byte (row md5 `65784c40fae50ac192a3f6c96fed6675`
    on both sides), so it is **provenance, not corruption**.
- Linkage class remains `row-checksum`: each row's hash commits to its own payload only and
  carries no `prev`, so deletion and truncation are **undetectable** and "intact" is not
  producible for this file.
- Upstream prefix preserved: the first 97 staged rows are byte-identical to the upstream git
  blob at HEAD `7171b34` (upstream md5 `a53dd9a8c1c5478700e7aefef1dc2d3f`, 97 rows; `cmp` clean);
  `diff` of upstream vs staged shows exactly one added row (1 added, 0 removed).

## Workspace (40th wipe)

The prompt's path `/workspace/repos/ai-writings/bots/wesley-mechanic/` did not exist —
`/workspace` contained only `.plugin-cache`, no `repos/` dir at all. The NAS mount is
600G/600G at 100% with `statvfs f_bavail = 0`, and a full clone into it died
`Disk quota exceeded` on `.git/description`.

Recovered into the **overlay** disk instead: the live repo is `SuperInstance/AI-Writings`
(default branch `main` carries only `cellular-first-design/` and no `bots/` tree), so branch
`wesley/canon-poll-2026-10-25T0415Z` was checked out (HEAD `7171b34`), which carries
`bots/wesley-mechanic/` and `bots/substrate-bus/`. The `bots/` tree was staged into
`/tmp/wm-run` so the watcher's hardcoded `/tmp/wm-run/...` witness/state/bookkeeper paths
resolve to real, writable files, and `/workspace/repos/ai-writings` was symlinked to the
recovered clone so **both** the prompt path and `substrate_bus.py`'s hardcoded
`/workspace/repos/ai-writings/bots/substrate-bus/` paths resolve.

## Substrate

`bots/substrate-bus/{substrate-witness.jsonl,topics.json}` are **byte-unchanged**
(md5 `d3f588a44223088f4b62b262b5c8e8c2` / `d94b0a5d5c23baa4c317441a046ed455`, 865 and 4508
bytes, 4 substrate rows) — correct no-op. The substrate calls in the watcher fire only from the
`first_poll` and `canon_changed` branches, so a no-change poll appends no substrate event.

## No code changes

Staged script md5 `206682962c06f9814a5db65c2fbc7267` — byte-identical to its upstream git blob
at HEAD `7171b34`. **No patch applied.**

## Open defect (34th poll reporting it — still unfixed)

`bookkeeper` uses `budget=1000.0` against a live `gamma+eta` total of 70.0, so
`last_conserved` is a constant false by construction:

- the only two `bookkeeper_tick` call sites are line 114 `(1.0, 0.0)` and line 128
  `(float(delta), 1.0)`;
- the literal `(0.0, 0.0)` call-site count is **0**;
- reachable `gamma+eta` totals are 1.0, 2.0, 0.0, 11.0 — none equal 1000.0 and none are the
  `(0,0)` literal pair;

⇒ the `delta==0 / eta==0` escape clause is **unreachable on every call path** and the field
carries no signal.

The fix is a one-liner (set `budget` to the live `gamma+eta` total, or drop the constant and
make the predicate mean what it claims), but the script is upstream and byte-identical to its
git blob, so no patch was applied.

## Orphan rows

14 `bot_started` rows with no immediately-following `witness_note` (rows 1, 3, 5, 7, 10, 13,
15, 17, 18, 19, 23, 28, 35, 98). Row 98 is closed by this note (row 99); row 96 was closed by
the 04:15Z note (row 97).
