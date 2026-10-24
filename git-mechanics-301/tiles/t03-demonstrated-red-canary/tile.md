---
id: t03
title: demonstrated-red-canary
status: pinned
prereqs: [t01]
---

# t03 — demonstrated-red-canary

## The claim

A check that has never been seen failing is **not a check** — it is a
decoration that reassures. A canary that cannot fail is worse than no
canary, because it spends your vigilance on theater. The doctrine:
every load-bearing pin must carry a **demonstrated RED** — a recorded
run where the pin failed because the guarded property was genuinely
violated, by a real mutation, applied on purpose.

## The witnesses

- `witness/audit-p6-red.log` — the frozen-clock-lab P6 pin's own RED
  record: P1–P5 PASS while **P6 FAILs** (`reference-vectors-match=False`)
  under the arithmetic mutation. The pin was seen dying.
- `witness/r73-mutation.md` — pong-quilt's R73 franken-save guard
  mutation-tested: one-line guard kill → two tests RED with the exact
  assertion "the franken file must never download"; unrelated tests
  correctly stayed green.

## The doctrine's edge

Demonstrated-RED is necessary, not sufficient: see t06 (the RED must
attack the real property, not a decoy) and t07 (the mutation must alter
executed arithmetic, not comments). Together the three tiles are the
verification triad.

## Exercises

1. Pick the most important test in a system you maintain. Kill the
   property it guards — one line, the real line, not a comment. Run it.
   Did it fail? If not, you have found your first honest debt.
2. Write the RED record to a file. Commit it. That file is now an asset.

## Falsifier

If a pin suite can be shown to guard a real property without any member
ever having been demonstrated failing, this tile falls. No such suite is
known to this course.
