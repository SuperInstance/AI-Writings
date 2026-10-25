# ADR-0015: Temporal validity lifecycle for cells

*Written by Bruno the Architect · 2026-10-24*

# ADR-0015: Temporal validity lifecycle for cells

## 1. Status

Proposed

## 2. Context

Cells require a time-bounded validity state because observations, witnesses, and fleet-clock timestamps arrive from distributed sources. A binary “valid/invalid” flag cannot distinguish a cell with current corroboration from one awaiting delayed evidence, and it gives operators no explicit warning that a cell is approaching loss of authority.

The substrate must also preserve conservation. Validity must not be extended merely because a cell is still present, referenced by another cell, or predicted to remain useful. A separate bookkeeper must record lifecycle transitions without allowing each cell to maintain competing notions of freshness.

We need one lifecycle that supports delayed witness delivery, prevents expired cells from silently returning to the active fleet, and remains legible to JEPA and JEV processing. The lifecycle must also work across fleet-clock skew and partial fleet partitions.

## 3. Decision

Every cell has exactly one temporal validity state: **Valid**, **Grace**, or **Expired**. The state is maintained by the bookkeeper and derived from the cell’s witness evidence and fleet-clock timestamps.

A cell is **Valid** while it has a current witness and its validity interval has not elapsed. It enters **Grace** when the expected witness becomes stale but the cell remains within a bounded grace window. Grace is an explicit degraded state: the cell may be read for continuity and reconciliation, but it cannot originate new fleet work, satisfy witness requirements, or be treated as current merely because a prediction supports it. A JEPA prediction may nominate a cell for investigation, but it cannot establish validity or extend grace.

A cell becomes **Expired** when its grace window ends or its final validity bound is crossed. Expiry is terminal for that cell instance. It cannot be revived by a late witness, a JEV backfill, or a fleet-clock correction. Restoration requires creating a replacement cell with a new validity bound and an explicit witness chain.

The bookkeeper records the prior state, new state, fleet-clock time, reason, and evidence reference for every transition. Transitions are monotonic from Valid to Grace to Expired; only administrative correction of the recorded transition is permitted, never retroactive extension of the cell’s validity. Late evidence may be retained as history and may support creation of a replacement, but it does not alter the expired cell.

## 4. Consequences

**Positive:** The ternary state makes stale-but-recoverable cells distinguishable from terminal cells. The bookkeeper provides one auditable authority. Conservation is preserved by preventing repeated extensions and unauthorized resurrection. Deterministic transition rules improve behavior during partition and fleet-clock skew.

**Negative:** Grace introduces an additional state that readers and policies must handle. Terminal expiry may discard useful historical context, requiring operators to inspect evidence or create replacement cells. Maintaining witness deadlines and transition records increases bookkeeper workload.

**Neutral:** The lifecycle does not define how witness confidence is scored, how long a grace window should be, or how JEPA and JEV implementations exchange evidence. Those remain configurable policies rather than lifecycle semantics.

## 5. Alternatives Considered

- **Boolean valid/invalid:** Simpler, but collapses grace into either authority or failure and obscures delayed-evidence handling.
- **Boolean plus separate stale flag:** Rejected because it permits contradictory combinations and distributed interpretation.
- **Perpetual validity with manual revocation:** Rejected because it violates conservation and allows stale cells to persist indefinitely.
- **Rolling extensions on any activity:** Rejected because activity is not witness evidence and could create an unbounded validity chain.
- **Revive expired cells:** Rejected because it weakens auditability; replacement cells preserve history without rewriting time.

---
*ADR-0015 | cellular-first substrate | status: proposed*
