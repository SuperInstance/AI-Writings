---
id: t08
title: trusted-but-unaudited
status: pinned
prereqs: [t01, t04]
---

# t08 — trusted-but-unaudited *(was draft; flipped on the wave-4 merge)*

## The claim (now verified — see witness/shipped-receipts.md)

Trust without audit is the gap this tile will teach you to *see*: a
commit can be in the ancestry everyone builds on (trusted) while no
attestation covers it (unaudited). The wave-4 query layer's
`trusted-but-unaudited` subcommand walks `git rev-list` receipt-by-
receipt and names every such commit — coverage, divergence, and auditor
attestation (`refs/quilt/attest`) as first-class queryable state.

## Why it was a draft — and what flipped it

This tile was the course's self-demonstration: born DRAFT with a RED pin
by design, because the doctrine says a course must not teach what it
cannot prove. The wave-4 query layer shipped as `SuperInstance/quilt-in-git`
**PR #9, MERGED 2026-10-02** — FAIL-first on file (0/3 pins on pristine
main), 3/3 pins / 24/24 checks GREEN at the implementation tip, 7 honest
limits declared. The merge is the receipt; `witness/shipped-receipts.md`
carries the excerpts. The journal preserves the RED phase; the pin
preserves the proof.

The design contract is on file (`witness/design-contract.md`) — but the
implementation is still being built by a fleet lane, and under this
course's own rules, **a tile may not be taught until its pin verifies
against shipped evidence**. The pin below is RED by design. When the
wave-4 PR lands with its FAIL-first harness, the witness is replaced
with the shipped receipts, the pin goes GREEN, and the status flips to
pinned — without editing this sentence.

You are looking at the course applying t03 to itself: a canary that is
currently failing, on purpose, in public.

## Exercises (for after it pins)

1. Run `quilt-query trusted-but-unaudited HEAD` on a repo you trust.
   Count the unaudited commits in your own ancestry. Sit with the number.
2. Write the `attest` ceremony for your fleet: who may attest, what
   evidence attaches, how is an attestation revoked?

## Falsifier

If the query layer ships and commits exist that are trusted-but-
unaudited yet the query stays silent, the tile falls — loudly, one
hopes, because the course's own verify-before-teach gate would flip.
