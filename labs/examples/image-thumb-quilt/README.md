# image-thumb-quilt (EX5) — mark

*Fifth worked example in the collection (§13 of `situations/arch/ACTIVELEDGER-CELL-GRAPH.md`):
"make a thumbnail" with the clever skip "don't decode or resample when the source is already ≤ target".*

- **WHAT** — A thumbnailer with **two product-identical routes** on a deterministic synthetic grayscale
  image `{w, h, pixels}` (stdlib only): **pass-through** (source already ≤ target → return it unchanged,
  no decoder/resampler shipped) and **resample** (decode + integer box-average downsample, aspect kept,
  never upscales). The quilt **chooses pass-through iff source ≤ target**. On the shared already-small
  cases resample is a no-op, so both reach the identical thumbnail. Every step is booked to an ActiveLog
  v1 run through the shared `labs/activeledger` emitter (cell.tick + balanced route.hop + ledger.transaction,
  full budget vector incl. `storage_bytes`).
- **STATE** — **HEWN.** `selftest.py`: **18 checks, 0 failures**, offline & deterministic. Cheap vs full
  on one small source: wall_ms **5 vs 24**, prod storage **176 B vs 8192 B**, train storage 352 B vs
  32768 B (resample ships the decode+resample tooling).
- **RUNS** — `python3 thumb_quilt.py` (demo) · `python3 selftest.py` (the proof).
- **SHORTCUT** — Budgets are a deterministic cost model, not measured. The "image" is a synthetic grid with a
  2-byte-header toy codec, not a real format; resample is box-average only (no filtering options).
- **ASSUMES** — Python 3.10+ stdlib; `labs/activeledger/activeledger.py` (imported via relative path).
- **BETTER-WHEN** — a real codec/resampler replaces the toy; costs come from a real meter; the
  `labs/examples/run_all` harness books it beside EX1–EX4 to one shared ActiveLog.
- **SEED** — §13: obvious use, clever skip.
- **NEXT** — EX2–EX4 siblings; interop harness; tutorial.
