---
id: t02
title: order-not-time
status: pinned
prereqs: []
---

# t02 — order-not-time

## The claim

Wall-clock timestamps are **decorations** on a receipt chain. Order lives
in the chain itself: each receipt commits to its predecessor. Two streams
with identical ops in identical order produce byte-identical chains even
if one runs on a clock that jumps backward, freezes, or skews. The first
position where two chains diverge is exactly the first op that differed —
position 1 for `alpha,beta,gamma` vs `alpha,gamma,beta`.

## The witness

`witness/pins-clock-p2.py` — the P2 pin from
`SuperInstance/frozen-clock-lab` (poc): two `ReceiptChain`s fed the same
ops in different orders; the pin asserts `first-divergence-position=1`.
No clock object appears anywhere. The chain *is* the time.

## The consequence

Once order is divorced from time, "when did it happen" becomes a query
over positions, not timestamps — and every temporal mechanism in the
course (replay, rewind, grafting, audit) inherits a deterministic
foundation. Git's own doctrine ("content address, not timestamps") is the
special case for trees; this is the general case for *operations*.

## Exercises

1. Implement a receipt chain in 20 lines of any language. Feed it 10,000
   ops while randomizing your OS clock between ops (set it backward,
   forward, freeze it). Regenerate from genesis. Same terminal hash?
2. Give one real system you have used that violates this doctrine and
   one that honors it.

## Falsifier

If any legitimate reordering of identical ops can produce the same chain,
order-not-time falls. (It cannot — that is the hash chain's one job.)
