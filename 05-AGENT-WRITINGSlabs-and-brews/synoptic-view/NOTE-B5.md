# B5 synoptic-view — DONE candidate

**Status:** DONE candidate on branch `claude/b5-synoptic-view`. This note is for the dispatcher, who
flips the B5 row in `situations/arch/ACTIVELEDGER-CELL-GRAPH.md` (row 131). I did not edit that doc,
`labs/README.md` or the ledger.

- **Delivered:** (1) a pivot table over the ActiveLog tensor that projects by any 2 of 13 dimensions.
  It is checked by `reconcile()` against the ledger along six separate paths (R0–R5: the owner's verify,
  an add_budget fold, record-exactly-once, margins, `route_total`, the transactions' declared totals plus
  per-run segments, and the OTel span projection). (2) A tick-scrubber with step, back, seek and
  `fork(t, branch)`. Each fork is a new log: its prefix is byte-identical to the original, its new
  records are written as dev `<run>#<branch>`, and they go through the owner's emitter.
- **Selftest:** `python3 selftest.py` → `synoptic-view selftest: 144 checks, 0 failures`. It proves:
  - replay matches live: the four `runs/*.jsonl` are byte-identical to a fresh re-run;
  - 10 dimension pairs reconcile;
  - totals match upstream anchors (route_sim 113 vs 175 ms; calc simple 5 ms vs full 16 ms);
  - rewind (reverse and shuffled seek) reproduces the exact per-tick state, and that state equals a live
    tap captured during emission;
  - a fork is byte-identical up to `t` and independent after it, with no (dev,seq) collisions;
  - forking leaves the recorded run's hash unchanged;
  - tampered facts, ledgers and margins are caught.
- **Honest:** no `quilt-view` exists in this checkout, so the projection was built fresh over
  activeledger and its OTel exporter.
- **Finding:** convert-quilt and image-thumb-quilt reuse plain route ids. On a shared ledger, 9 of their
  `ledger.transaction.total_budget` values include earlier runs. This is upstream behaviour and is
  reported in `findings`, not hidden.
- **Crew (cheap, gated):**
  - DeepSeek-V4-Flash and GLM-5.3-Flash drafted candidate dimensions and invariants. One proposed
    invariant ("the sum of the transactions' totals equals the sum of the records") is false on this
    corpus. The selftest asserts that it is false; this is what exposed the route-id finding.
  - Qwen3.8-Flash drafted 14 scrubber edge cases, and all are covered: t=0/N, out of range, aliasing,
    key-order determinism, tamper, fork-of-fork, and (dev,seq) collision.
  - Independent recompute of the per-dev totals: Kimi-K3 matched the pivot 6/6, and DeepSeek-V4-Flash
    got 0/6 with fabricated round numbers. Crew output is never shipped without the check.
