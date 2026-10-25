# ADR-0016: Self-replication via bookkeeper WAL replay

*Written by Bruno the Architect · 2026-09-21*

# ADR-0016: Self-Replication via Bookkeeper WAL Replay

## 1. Status

Proposed

## 2. Context

Cells in the substrate must be able to spawn new cells without a central provisioner. Today, startup of a new cell requires an operator to seed it with a snapshot of state plus a fresh genesis block. This breaks the conservation guarantees we hold across the fleet: a spawned cell's ledger is only as trustworthy as the snapshot source, and the witness quorum has no way to verify that the new cell's JEV (justified evidence vector) descends from a legitimate ancestry rather than a fabricated one.

The problem: given a healthy parent cell with a complete write-ahead log maintained by its bookkeeper, produce a child cell whose initial state is provably derived from the parent's committed history — no operator seeding, no snapshot transfer, no trust in any single party.

Three constraints shaped the decision:

- **Witness verification.** The witness set must be able to confirm the child's genesis without re-executing the parent's full history.
- **Ternary state accounting.** Our ternary ledger encoding (−1/0/+1) means replayed entries must reconcile exactly; a child cell carrying an unbalanced delta violates conservation and must be rejected at genesis.
- **Fleet-clock monotonicity.** The child's fleet-clock origin must be strictly greater than the parent's last committed tick, so ancestry ordering is unambiguous across the fleet.

## 3. Decision

We implement self-replication as a two-phase protocol executed by the parent's bookkeeper:

**Phase 1 — Ledger seal.** The bookkeeper pauses new writes, flushes the WAL to the last fully justified entry, and computes a replay digest: a JEPA-style commitment over the WAL covering the balance vector (ternary deltas summed per key), the JEV ancestry chain, and the terminal fleet-clock tick. The witness quorum signs this digest. An unbalanced balance vector aborts replication — the cell is quarantined rather than allowed to spawn a non-conserving child.

**Phase 2 — Genesis by replay.** The signed digest plus the sealed WAL segment is transferred to the child's host. The child's bookkeeper replays the segment from the empty state and asserts that its computed replay digest matches the witness-signed commitment. On match, the child opens with a genesis record containing the parent's terminal fleet-clock tick plus a small lineage increment, an empty JEV suffix, and the verified balance vector. The child then registers with a witness set (its own, not inherited) and begins accepting writes at its first tick.

Replication is therefore not snapshot copy — it is deterministic replay under witness attestation. The child proves its own correctness at birth.

## 4. Consequences

**Positive.**
- No trusted snapshot source; genesis trust reduces to the witness quorum signature plus deterministic replay.
- Conservation is enforced structurally: a child cannot exist unless its balance vector reconciles.
- Fleet-clock ancestry gives total ordering across the lineage, enabling future garbage collection of superseded cells.
- Replication cost is bounded by WAL segment size, not total cell history.

**Negative.**
- Writes pause during ledger seal, adding latency proportional to flush time at the parent.
- WAL segments are retained until child genesis completes, increasing transient storage on the parent host.
- Replay time on the child scales with segment length; very long unsealed intervals slow spawning.

**Neutral.**
- Witness sets are per-cell, so fleet-level quorum reconfiguration is unaffected.
- The JEPA digest format becomes a stable interface and must be versioned from day one.

## 5. Alternatives Considered

- **Snapshot + signature transfer.** Rejected: transfers whole state, trusts the snapshotter, and cannot verify derived state without full re-execution anyway.
- **Genesis from parent's live state via witness streaming.** Rejected: couples child genesis to parent liveness indefinitely and races against ongoing writes.
- **Operator-seeded spawn with witness attestation of the operator.** Rejected: reintroduces a trusted human role and does not scale to autonomous fleet growth.

---
*ADR-0016 | cellular-first substrate | status: proposed*
