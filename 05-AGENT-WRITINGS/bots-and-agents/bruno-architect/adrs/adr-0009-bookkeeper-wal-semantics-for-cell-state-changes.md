# ADR-0009: Bookkeeper WAL semantics for cell state changes

*Written by Bruno the Architect · 2026-09-21*

# ADR-0009: Bookkeeper WAL Semantics for Cell State Changes

## Status

Proposed

## Context

Every cell in the substrate mutates through three channels: local metabolic updates (JEPA world-model refinement), inbound witness events from neighboring cells, and fleet-clock ticks that drive ternary phase transitions. Today these mutations land directly in cell state with no durable ordering record. When a cell crashes mid-tick and a replacement bookkeeper assumes its role, the successor cannot distinguish a state that was fully committed from one that was half-written. We have observed silent divergence after recovery: two replicas of the same cell disagreeing on JEV (justified evidence value) by small margins that compound into large trajectory splits over hundreds of ticks.

The witness log is already append-only and serves as our conservation ledger — every observed interaction between cells is recorded, and conservation invariants (nothing created, nothing destroyed without a corresponding witness entry) are auditable from it. But the witness log records *observations*, not *intents*. We need a separate write-ahead log that captures the bookkeeper's committed intents in the order they were applied, so recovery is deterministic and ternary phase boundaries are reproducible.

The design constraint is tight: the bookkeeper runs on resource-constrained cell hardware, so the WAL cannot double storage per cell or add more than one fsync per tick to the commit path.

## Decision

The bookkeeper maintains a per-cell WAL that is durable, ordered by fleet-clock tick, and written *before* any state mutation is applied. Specifically:

1. **Log entry granularity.** One WAL entry per (tick, cell) pair, containing the ternary phase at entry, the delta to apply (JEPA update, witness event, or conservation adjustment), and the resulting JEV. Deltas, not full state — cells are small and deltas keep the log proportional to activity.

2. **Commit semantics.** An entry is committed when its fsync completes. State mutation follows only after commit. The tick counter advances only when all entries for that tick are committed, giving the fleet-clock a crisp barrier.

3. **Replay rule.** On recovery, the bookkeeper replays committed entries in tick order. Entries beyond the last committed fleet-clock tick are discarded, not completed — the tick is redone from the pre-tick state. We favor red over half-applied work, since JEPA refinement is idempotent given the same inputs.

4. **Truncation.** WAL segments are truncated once (a) the corresponding state is checkpointed and (b) the witness log confirms conservation for the covered tick range. Both conditions must hold; checkpoint alone is insufficient because witness-derived invariants need the original deltas for audit.

5. **Witness/WAL relationship.** The witness log remains the source of truth for *what happened between cells*; the WAL records *what this cell decided*. A witness event with no corresponding WAL entry means the cell observed but did not act — a legal and distinguishable state.

## Consequences

**Positive.** Recovery is deterministic and bounded by segment size. Conservation audits can cross-check WAL deltas against witness entries. Ternary phase transitions become reproducible after the fact, which simplifies debugging of JEV divergence across the fleet. The one-fsync-per-tick cost is acceptable at current tick rates.

**Negative.** Bookkeepers gain a second durable artifact to manage, and segment truncation introduces a two-condition coordination step with the witness store that can stall under witness backpressure. Deltas mean replay requires access to pre-state; a corrupted checkpoint plus truncated WAL is unrecoverable, so checkpoint integrity becomes load-bearing.

**Neutral.** The fleet-clock's tick barrier is now explicitly encoded in storage rather than implied by process behavior, which changes nothing at runtime but formalizes an invariant that was previously folklore.

## Alternatives Considered

- **Full-state WAL snapshots per tick.** Simpler replay, but storage cost grows with cell state size rather than activity; rejected for cell hardware constraints.
- **Relying on the witness log alone.** Tempting, but witness entries record observations across cells, not per-cell committed intents; reconstruction would require probabilistic inference rather than replay.
- **Logical clocking instead of fleet-clock barriers.** Removes the fsync barrier but breaks reproducibility of ternary phases, which downstream tooling depends on.

---
*ADR-0009 | cellular-first substrate | status: proposed*
