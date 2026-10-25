# Witness: wave-4 query layer design contract (2026-10-02, in flight)

Recovered from the wave-4 lane's working log (its final design notes
before the host process was killed; the lane was resumed as a subagent
against this exact contract).

## Subcommands of `.quilt/bin/quilt-query`

- `coverage` — intersection of receipts and LEDGER attestations: what is
  claimed-covered vs. what the chain actually records.
- `divergence` — receipted vs. touched: files/commits in the tree with
  no receipt, and refs/commits with receipts but no tree presence.
- `trusted-but-unaudited` — is-ancestor ordered, commit-by-commit: walk
  `git rev-list $ref`, intersect with the receipted file, report every
  commit trusted (in the ancestry) but lacking an audit attestation.
- `attest` — auditor attestation stored as a ref under `refs/quilt/`.

## Honest limits (7, from the lane's own notes)

1. trusted-but-unaudited is only as strong as the receipt chain it reads;
   a fabricated receipt JSON committed to the tree is indistinguishable
   from a hook-written one (format-level trust).
2. (resolved during design: unreachable anchors fail is-ancestor loudly —
   documented as a property, not a gap.)
3. Substring edge: entry path "cells/a" vs. touched "cells/ab/…" matches
   by case-glob → false-positive coverage. Documented; precise needles
   are the operator's job until tokenized matching lands.
4. No time dimension: `ts` fields are commit times of positions; the
   layer cannot express "audited within the last week" — by doctrine.
5. (compounding issue between #2-era reason-erasure and queries —
   resolved by the doubt-ledger guardian fix.)
6. Divergence queries read resolved hashes; tag-peeling handled.
7. The query layer verifies receipts; it does not verify the world the
   receipts describe (that needs t03/t06 discipline underneath).

## Status contract

This tile stays **draft** — its pin must FAIL — until a wave-4 PR ships
with the FAIL-first pin harness (`tests/pins_query.sh`) demonstrating
RED-on-pristine-main and GREEN-on-implementation. The course refuses to
teach it before then.
