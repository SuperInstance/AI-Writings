---
id: t07
title: mutation-discipline
status: pinned
prereqs: [t03, t06]
---

# t07 — mutation-discipline

## The claim

Not all mutations are mutations. A change that alters **comments,
whitespace, or dead literals** changes nothing the machine executes —
so a pin suite that "survives" it proves nothing, and a pin suite that
"fails" under it was probably keyed to cosmetics. The discipline: a
mutation test must alter *executed arithmetic*, and the auditor must
verify the alteration landed in the live path — not assume it from the
diff's appearance.

## The witness

`witness/false-claim-correction.md` — the full story: an audit reported
"corrupting the FNV prime passes 9/9" (panic: the pins are decorative).
Investigation: the sed had mutated a comment line; the implementation
computes the prime as `435 + 2^40`. The genuine arithmetic mutation
(`435 * lo` → `436 * lo`, `435 * hi` → `436 * hi`) is caught — 5 checks
red, 7/10 pins. The correction was published in both repos' commit
messages, not buried.

## Why this tile costs the most

It exists because the course's author paid for it: a public false claim,
a public correction, and a doctrine extracted from the wreckage. Receipts
culture applies to the auditor — that is the sentence that bought this
tile.

## Exercises

1. Find the comment that most *looks* like the implementation in a
   system you maintain. Confirm what the machine actually executes.
2. Write a two-column table for your last three "mutation tests":
   column one, what you changed; column two, what the machine executed.
   Any row where they differ is a t07 debt.

## Falsifier

If cosmetic-only mutation can never masquerade as an executed mutation,
the tile is empty. The witness refutes that.
