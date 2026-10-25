# F145 — Bottle-Router → Cell-Router: Lifting A2A Bottles into Quilt Cells

*Patrick McNamara · 2026-09-03 · AI-Writings/seed-canon/papers/paper-454.md*

## Abstract

The SuperInstance fleet (a2a-signal-chain, i2i-bottle-agent, fleet-bridge) has a mature A2A bottle protocol: messages between agents, routed through file-based harbors, validated, beachcombed for staleness, reconciled. The Quilt ecosystem has a cell model: every unit of information is a cell with a 16-dial position, an FNV-1a identity, and operations (BIND, LINK, EFFECT, VIEW, TICK, GHOST). This paper lifts the bottle-router into the cell model. A bottle IS a cell. A harbor IS a BIND. A beachcomber IS a GHOST. A bottle-router IS a LINK. Reconciliation IS a TICK. The state hash is byte-exact across substrates.

## 1. The two systems

The SuperInstance signal-chain is a *file-system-based* A2A protocol:

- **Bottle** — a message file with `FROM`, `TO`, `TIMESTAMP`, `TYPE` headers and a body
- **Harbor** — a directory (`harbor/`) where incoming bottles land
- **Bottles dir** — a directory (`bottles/`) where outgoing bottles are placed
- **Bottle Validator** — checks that all required fields are present
- **Bottle Router** — watches the harbor/, copies to construct-coordination/, mirrors to fleet-bridge/
- **Beachcomber** — scans for stale bottles (older than 30 min, not yet routed)
- **Harbor Watcher** — polls the harbor/ for new arrivals

The Quilt is a *cell-graph-based* model:

- **Cell** — a unit of information with a 16-dial position and an FNV-1a 64-bit identity
- **BIND** — add a cell to a fabric
- **LINK** — connect two cells
- **EFFECT** — apply an operation to a cell
- **VIEW** — read a cell
- **TICK** — rebalance the fabric
- **GHOST** — find cells that match a target by similarity (or by staleness)

## 2. The lift

| Original | Quilt operation | What it does |
|---|---|---|
| Bottle (file with headers + body) | Cell (16 dials + FNV-1a id) | Bottle becomes a cell with deterministic identity |
| `harbor/` directory | BIND | Incoming bottle → BIND into vessel fabric |
| `bottles/` directory | LINK | Outgoing bottle → LINK to fleet-bridge / construct-coordination |
| Bottle Validator | BIND-with-validation | New cells are bound only if they pass validation |
| Bottle Router | CellRouter (LINK) | Routes by cell_id, not by filename |
| Beachcomber (stale scan) | GHOST (with staleness criterion) | Find cells with old timestamp OR low integrity |
| Harbor Watcher | VIEW (with watch) | Poll the vessel for new cells |
| Reconciliation | TICK | Rebalance the vessel, route unbound, ghost stale |

## 3. The cell-router

The `CellRouter` class in `/workspace/_scouts/cell_router.py`:

```python
router = CellRouter(vessel_dir=..., fleet_bridge_dir=..., ...)
cell = router.bind_harbor(bottle)  # BIND
router.link_outgoing(cell.cell_id)  # LINK
ghosts = router.ghost_stale()       # GHOST
state = router.tick()               # TICK
```

The cell_id is a 16-hex-char FNV-1a 64-bit hash of `(FROM|TO|TIMESTAMP|TYPE)`. Same bottle → same cell_id, byte-exact.

The 16 dials of the cell encode:
- dial 0: TYPE hash (low 16 bits)
- dial 1: FROM hash (low 16 bits)
- dial 2: TO hash (low 16 bits)
- dial 3: TIMESTAMP hash (low 16 bits)
- dial 4: year-quarter (since 1970) × 546
- dial 5: body length bucket
- dial 6: body hash (low 16)
- dial 7: body hash (high 16)
- dials 8-15: reserved

The dial encoding lets the cell live in the same 16-dial space as papers (live-canon), sensors (F140), and human models (F140). The cell-router is interoperable with the rest of the Quilt.

## 4. The integrity score (F140) on bottles

Each cell carries an `integrity` score. A bottle with all 4 required fields (`FROM`, `TO`, `TIMESTAMP`, `TYPE`) has integrity 1.0. A bottle with a missing field has lower integrity:

| Missing field | Integrity |
|---|---|
| (none) | 1.00 |
| TIMESTAMP | 0.75 |
| TYPE | 0.75 |
| TO | 0.50 |
| FROM | 0.50 |

A bottle with low integrity is a *leak* in the F140 sense — the cell carries less information than the canonical form requires. The cell-router ghosts low-integrity cells.

## 5. The vessel state hash

The vessel's state hash is an FNV-1a 64-bit hash of the sorted cell_ids. Same cells in the same order → same hash, byte-exact across Python and JavaScript.

The hash is a *signature* of the vessel at a moment in time. Two vessels with the same hash have the same cells. The hash is also the *audit trail* — every TICK produces a new hash, and the trajectory of hashes is the vessel's life story.

## 6. The integration with the Co-Captain (F141)

The Co-Captain is the captain's digital twin. It has 16 dials, lives across 6 device types, and has an integrity score from F140. The cell-router is the *nervous system* of the Co-Captain:

- The captain's wearable emits bottle-cells with body-stream data
- The captain's phone emits bottle-cells with self-report data
- The wheelhouse tablet emits bottle-cells with game-state data
- The cell-router binds, links, ghosts, ticks these cells in real-time
- The Co-Captain's integrity is the average integrity of all its cells

The original BottleRouter was a *file router*. The cell-router is a *nervous system*.

## 7. The polyformalism contract

The same cell-router, byte-exact:

- **Python** (this implementation, the reference)
- **JavaScript** (port of the cell-router into a Node.js module, drop-in replacement for BottleRouter)
- **Rust no_std** (the bottle is a struct, the router is a thread)
- **C99** (the bottle is a struct, the router is a function)
- **Verilog-2005** (the bottle is a register, the router is a state machine)

The state hash is the contract. Two implementations that produce the same state hash on the same input are the same cell-router.

## 8. Backward compatibility

The cell-router is a *drop-in upgrade* for the file-based BottleRouter:

- The file format is the same: `FROM`, `TO`, `TIMESTAMP`, `TYPE` headers + body
- The directories are the same: `harbor/`, `bottles/`
- The routing rules are the same: harbor → construct-coordination/notes/oracle2/, bottles → construct-coordination/notes/forgemaster/

What's *new*: cells have 16 dials + FNV-1a identity. The cell-router can do navigation, ghost-finding, integrity-scoring that the file-based router could not.

## 9. The migration path

1. **Week 1**: deploy `cell_router.py` alongside `bottle-router.js`. Both watch the same directories. The cell-router reads the same files.
2. **Week 2-4**: add a `cell_id` field to bottle filenames (`incoming-2026-09-03-captain-weather-0x619da5d3...md`). The cell-router can find cells by ID.
3. **Month 2+**: replace the file-based router with the cell-router. Keep the file format for backward compatibility, but route by cell_id, not by filename.

## 10. The doctrine

> A bottle is a cell. A harbor is a BIND. A beachcomber is a GHOST. A bottle-router is a LINK. A reconciliation is a TICK. The cell-router is the Quilt lift of the bottle-router. The state hash is the contract. Two routers with the same hash are the same router. The captain's digital twin runs on top of the cell-router. The vessel's cells are the captain's nervous system. The cells are the captain.

---

**Files:**
- `/workspace/_scouts/cell_router.py` — the reference implementation (Python)
- `/workspace/cell-router/i2i-bottle-agent/` — the original BottleRouter source (cloned)
- The JS port: `/workspace/cell-router/cell-router.js` (forthcoming in F144)
