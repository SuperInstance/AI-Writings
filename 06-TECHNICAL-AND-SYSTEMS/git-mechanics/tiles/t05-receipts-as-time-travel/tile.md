---
id: t05
title: receipts-as-time-travel
status: pinned
prereqs: [t02]
---

# t05 — receipts-as-time-travel

## The claim

Save any mid-stream receipt — call it the **genesis anchor**. Hand it to
a fresh chain seeded with that anchor, replay the remaining ops in order,
and you arrive at the original terminal hash. That is "rewind the world"
with a receipt: no snapshots of state, no copying of heaps — one hash and
the op list. Time travel, in this discipline, is a *recomputation
discipline*, not a storage discipline.

This is 201's "uncooking the loaf" (Weeks 5–6) reduced to its load-
bearing core — the parts that must be true for everything else to even
be possible.

## The witness

`witness/pins-clock-p5.py` — the P5 pin from frozen-clock-lab (poc): a
300-op stream, anchor at position 149, replay from the anchor hash
through every remaining op, asserting the replayed head equals the
original terminal (`replayed-forward-to-terminal=True`). Any divergence
mid-replay fails the pin *at the exact position*.

## The interaction with t02

Replay is only possible because order lives in the chain (t02). If time
were timestamp-anchored, a frozen clock mid-replay would corrupt the
journey. The two tiles are one mechanism seen from two sides.

## Exercises

1. Extend your t02 chain: save the 150th receipt of a 300-op stream,
   then replay 150→300 on a *different machine*. Compare terminals.
2. What breaks if an op is non-deterministic (e.g., reads wall time)?
   Fix it by construction.

## Falsifier

If replay-from-anchor can converge to a wrong terminal without detection,
the anchor mechanism is decorative — and every temporal feature built on
it (Module 2's splice, Module 3's rollback) inherits the decoration.
