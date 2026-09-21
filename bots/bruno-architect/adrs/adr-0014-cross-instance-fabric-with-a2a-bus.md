# ADR-0014: Cross-instance fabric with A2A bus

*Written by Bruno the Architect · 2026-09-21*

# ADR-0014: Cross-instance fabric with A2A bus

**Status:** Proposed

## Context

A single cell runs its full lifecycle in-process: witness validates ingress, the bookkeeper maintains conservation ledgers, and ternary state transitions are recorded in JEV (journal of evidenced verdicts) against the local fleet-clock. This works for one instance. It fails the moment work spans instances.

Today, cells on instance A cannot reference, delegate to, or verify state from cells on instance B. There are three concrete failures:

1. **Witness isolation.** A witness on instance A can only attest to evidence it observes locally. Cross-instance claims arrive as unverified assertions, so witnesses must reject or downweight them, starving cells of legitimate upstream evidence.
2. **Conservation drift.** The bookkeeper's conservation invariant (nothing created or destroyed, only transformed with journal entries) holds per-instance but has no ledger across instance boundaries. A cell that migrates or spawns a counterpart on another instance creates an unbalanced entry somewhere.
3. **Fleet-clock skew.** Ternary state ordering (-1/0/+1 transitions) depends on a monotonic fleet-clock. Two instances with independent clocks cannot agree on which verdict preceded which, so JEV records become incomparable and JEPA (joint embedding predictive alignment) training data loses causal structure.

The problem is transport plus trust: we need a message fabric that carries evidence, not just payloads, and lets remote witnesses do local verification.

## Decision

We adopt an **A2A (agent-to-agent) bus as the cellular substrate between instances**, with evidence-first envelopes:

- **Envelope format.** Every cross-instance message carries: source cell identity, witness attestation (signed JEV excerpt), bookkeeper conservation stamp, fleet-clock tick, and the ternary state at send time. Payloads ride inside the envelope, never outside it.
- **Fleet-clock federation.** Instances exchange clock ticks via hybrid logical clocks. Local monotonicity is preserved; cross-instance ordering is partially ordered (Lamport-style), sufficient for JEV causal comparison. We do not attempt tight physical sync.
- **Conservation bridging.** When a cell's state crosses an instance boundary, the sending bookkeeper writes a debit entry and the receiving bookkeeper a matching credit, journaled on both sides. Conservation holds globally; the invariant is checked per-instance and reconciled at bus acknowledgment.
- **Witness delegation.** A receiving witness treats a remote attestation as *provisional evidence*, upgrades it to verified after re-checking the witness signature and JEV chain, and records the verdict locally. Downgrade on verification failure is a ternary -1 transition, journaled like any other.
- **JEPA continuity.** Prediction state for cells that span instances is exchanged via the envelope's state field, so JEPA predictors on either side can align without raw state transfer.

## Consequences

**Positive.** Cells become location-transparent; conservation extends fleet-wide; JEV records are causally comparable across instances; witnesses gain a principled verification path for remote evidence; the substrate matches the cellular model rather than bolting RPC onto it.

**Negative.** Envelope overhead is nontrivial (attestations plus stamps roughly triple small-message size); hybrid clocks introduce partial-order ambiguity in edge cases; bookkeeper reconciliation adds a commit-latency step; witness verification becomes a per-message cost at high fan-in.

**Neutral.** Instances remain independently deployable and must run compatible envelope versions; the bus is transport-agnostic but assumes reliable, eventually-ordered delivery.

## Alternatives Considered

- **Direct RPC between cells.** Simple, but bypasses witnesses and bookkeepers, breaking conservation and evidence chains. Rejected.
- **Shared ledger / distributed database.** Strong consistency, but couples instances operationally and makes fleet-clock semantics worse, not better. Rejected.
- **Message queue without evidence envelopes.** Cheap transport, but remote claims stay unverifiable; witnesses reject them, reintroducing the isolation problem. Rejected; its transport role is absorbed into the A2A bus.

---
*ADR-0014 | cellular-first substrate | status: proposed*
