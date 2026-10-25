# adrs

> **05-AGENT-WRITINGS › bots-and-agents › bruno-architect › adrs**  
> 4 files here

**What this is.** The bots themselves: their code, their logs, their handoff documents.

**Come here if you are looking for** the kind of writing in *bots and agents* — the section README above lists every neighbouring folder in this section.

**Contents**

- `adr-0009-bookkeeper-wal-semantics-for-cell-state-changes.md` — *ADR-0009: Bookkeeper WAL semantics for cell state changes*
- `adr-0014-cross-instance-fabric-with-a2a-bus.md` — *ADR-0014: Cross-instance fabric with A2A bus*
- `adr-0015-temporal-validity-lifecycle-for-cells.md` — *ADR-0015: Temporal validity lifecycle for cells*
- `adr-0016-self-replication-via-bookkeeper-wal-replay.md` — *ADR-0016: Self-replication via bookkeeper WAL replay*

---

### If this inspired you

Write your piece **in this folder**, named `YYYY-MM-DD-your-title.md`, and open a pull request against `main`.

Two rules, both deliberate:

1. **One approving review is required.** This is a record, not a scratchpad: a piece should land because someone read it. The fleet's own bot can no longer push to `main` directly — it has to go through a review too.
2. **Say what you were inspired by.** In the pull request body, name the piece (or folder) that prompted yours. The link is kept in `00-START-HERE/MANIFEST.csv` so the lineage of the work stays readable.

Do not create a new top-level folder for a single piece. If a piece does not fit any folder here, it goes in [`01-WRITING/unfiled-pieces/`](../unfiled-pieces/) and someone will file it later.

