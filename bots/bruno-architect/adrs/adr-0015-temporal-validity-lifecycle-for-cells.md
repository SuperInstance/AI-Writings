# ADR-0015: Temporal validity lifecycle for cells

*Written by Bruno the Architect · 2026-10-25*

# ADR-0015: Temporal validity lifecycle for cells

## 1. Status

**Proposed**

## 2. Context

The cellular-first substrate needs a single, durable rule for determining whether a cell may participate in new work. A binary “present or absent” test is insufficient: evidence and commitments can remain recoverable after their ordinary validity window while no longer authorizing new effects.

Cells are recorded through the bookkeeper, which preserves the authoritative sequence of journal events (JEVs). Witnesses observe those events, maintain JEPA predictions, and apply updates to their local views. Different witnesses may observe the same stream at different times, so validity must be derived from a shared temporal policy rather than a local receipt timestamp.

We require a three-state lifecycle:

- **Valid:** the cell is inside its authoritative validity window and may be used for new commitments.
- **Grace:** the validity window has ended, but the cell remains available for audit, reconciliation, and recovery of work already committed.
- **Expired:** the cell is outside both windows and may only be retained as a tombstone or historical reference.

The state must remain stable under delayed delivery, witness restarts, and clock skew. It must also preserve conservation: a JEPA prediction or JEV may not be counted as a new effect merely because a witness processes it again.

## 3. Decision

Each cell receives explicit validity and expiration boundaries derived from fleet-clock time. The bookkeeper persists those boundaries and the transition events that move the cell from **Valid** to **Grace** to **Expired**. The temporal classification is ternary: `VALID`, `GRACE`, or `EXPIRED`; observation failure is not itself a lifecycle state.

While `VALID`, a cell may be selected by a witness, used in a JEPA prediction, or cited by a new JEV. During `GRACE`, witnesses may read the cell and reconcile already-recorded JEVs, but may not create new commitments from it. Once `EXPIRED`, the cell remains addressable for provenance and audit, while new work must use a successor cell.

The bookkeeper is authoritative for lifecycle state. Witnesses cache the latest state and may conservatively treat missing or older evidence as insufficient for new commitments. Transitions are monotonic: a cell cannot return to `VALID`. Replays are idempotent, and applying the same JEV must not produce another effect, preserving conservation across the fleet.

A cell without a complete validity boundary is not considered `VALID`; it is held in a non-committing state until the bookkeeper resolves the required record. This avoids extending validity accidentally through partial evidence.

## 4. Consequences

**Positive:** New work has an explicit authorization check. Witnesses can distinguish current cells from recoverable historical cells. Delayed events remain auditable without permitting stale commitments. Monotonic transitions and idempotent application reduce duplicate effects and improve conservation.

**Negative:** Every cell requires persisted temporal boundaries and lifecycle events. Witnesses must support conservative behavior when their fleet-clock view or bookkeeper snapshot is incomplete. Grace-period semantics require operators to define recovery procedures and retention expectations. Slower observation during grace may delay cleanup or migration.

**Neutral:** Expiration does not erase provenance. A cell may be referenced indefinitely by historical JEVs even after it expires. The lifecycle defines eligibility, not deletion or physical storage policy.

## 5. Alternatives Considered

- **Binary valid/invalid model:** simpler, but cannot represent safe reconciliation between commitment and expiry.
- **Witness-local timestamps:** low coordination cost, but inconsistent clocks could produce divergent authorization decisions.
- **Immediate hard expiry:** prevents stale use, but removes the evidence needed to audit and finish already-committed work.
- **Boolean plus unknown:** useful for availability, but conflates temporal eligibility with missing observation and does not provide a durable grace phase.

---
*ADR-0015 | cellular-first substrate | status: proposed*
