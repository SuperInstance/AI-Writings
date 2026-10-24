---
id: t04
title: double-entry-doubt
status: pinned
prereqs: []
---

# t04 — double-entry-doubt

## The claim

A system that is *sure* it is fine is a system that has stopped looking.
The double-entry move, applied to doubt itself: every place you stop
checking something must be recorded as an **Entry** with four required
fields — `stopped_checking`, `because`, `covered_by`, `revisit_trigger` —
and the constructor **refuses** incomplete entries. Doubt written down
is an asset you can query, discharge, and audit. Doubt implied is a
liability that compounds silently.

This is 201's double-entry balance sheet (Module 2) with the accounting
target flipped: not state transitions, but *gaps in attention*.

## The witness

`witness/entry-grammar.py` — the actual Entry constructor from
`SuperInstance/doubt-ledger` (poc). Read the `missing` check: it raises
rather than defaulting. **A named refusal is the grammar's punctuation.**
Note also `status`, `expr`, `discharge_reason` — an entry is born open,
carries its query expression, and can only close with a recorded reason.

## Exercises

1. Write the three doubt-entries your current project most needs. Be
   honest about `covered_by` — "tests" is not a cover unless you can name
   the file.
2. Design the discharge ceremony: who may close an entry, and what
   evidence must exist at `revisit_trigger` time?

## Falsifier

If incomplete doubt-records are tolerated anywhere in the grammar, the
ledger's legibility collapses back to vibes — and the tile falls with it.
