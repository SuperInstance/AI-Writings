---
id: t10
title: portable-witness-substrate
status: pinned
prereqs: [t01]
---

# t10 — portable-witness-substrate

## The claim

A witness that *travels* beats a witness that must be believed. doubt-ledger's
wave-2 layer (merged 2026-10-02, `poc` @ 549c395, PR #3) makes a ledger slice
self-proving: a fnv1a-64 chain over per-line checksums, genesis-anchored, with
recomputed checksums bound to the live tip — so a filtered export carries its
own integrity proof, and the verifier **names the tampered line** instead of
saying "invalid."

## Why it matters

The edge-watch finding that motivated it (quoted in the source): portable
agent memory (arXiv 2605.11032-style) and the MajorLabs finding — **0 of 6
production memory systems sign their memory** — point the same way. A receipt
chain inside one repo proves order; the moment a witness crosses a boundary
(file, repo, machine, stranger), it needs its own chain and its own signature
or it is just a story with good formatting.

## The load-bearing details

- `GENESIS = "0" * 16` — the anchored root of the empty ledger; every chain
  starts from a named nothing.
- Root signing is **optional** (`sign.py`) and the ledger core stays
  **stdlib-only** — verification must not require the signing dependency.
- The honest boundary, stated in the source docstring: an export proves the
  included entries are byte-intact. It does **NOT** prove the filter was
  complete — selective disclosure hides by construction. **Completeness is
  the verifier's question, not ours.** A portable witness that claimed
  completeness would be laundering the hole; this one names it.

## The exercise

Design the export for the course's own ledger (a tile's witness set):
which fields go in, which stay home, what the filter must declare. Then
write the one-line answer to a stranger who asks "how do I know this is
everything?" — using only the honest boundary above. If your answer is
not "you don't; here is what this export does and does not prove,"
revise it until it is.

## Provenance

doubt-ledger wave-2 export+signing, MERGED 2026-10-02 into `poc`
(549c395, PR #3; branch `wave2-export-signing` deleted at merge). Witness
excerpts: `witness/export-header.py` (docstring + GENESIS + verify
contract), `witness/sign-header.py` (optional signing, stdlib-only core).
Birth recorded in LEDGER.md 2026-10-02 (late).
