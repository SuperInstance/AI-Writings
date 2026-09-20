# F82: The Quilt Time-Cell Visualizer

> **A live, in-browser cell-graph explorer for the `time.cell` kind.**

The Quilt `time.cell` is the most important cell kind since the
original 5 opcodes. It deserves a visualizer that makes the cell
graph *visible* — not as a static diagram, but as a live, animated
representation that updates with every BIND_CONTEXT, every FORECAST,
every READ_POINT.

This paper documents the visualizer at `visualizer/index.html` in
`quilt-timesfm`.

## The 5 design principles

1. **Decompose every operation into cell operations**. BIND_CONTEXT is
   shown as a state-write + a PROOF-chain append (the prev_hash
   arrow). FORECAST is shown as the abductive loop: PROPOSE → EXECUTE
   → RENDER → VERIFY → REFINE. READ_POINT and READ_QUANTILE are shown
   as VIEW operations on the forecast cell.

2. **Animate the cell graph in real-time**. Every cell is a node, every
   dependency is an edge. The active cell glows. The state hash is
   shown beneath each cell. The forecast animates step by step.

3. **Walk through a recorded session**. The visualizer can replay a
   canonical session: BIND_CONTEXT → BIND_COVARIATE → FORECAST →
   READ_POINT → READ_QUANTILE. The user can step through, see the
   state hash update, watch the forecast emerge.

4. **Compare the polyformalism ports**. Side-by-side: C, Python, Rust.
   The same BIND_CONTEXT call, the same hash, the same forecast. The
   visualizer renders all three simultaneously.

5. **Be self-contained**. The visualizer is vanilla HTML + Canvas + JS.
   No build step, no dependencies, no server. Just open the file.

## The cell graph (5 nodes, 4 edges)

The visualizer renders 5 cells and 4 dependency edges:

```
context    →   forecast
covariate  →   forecast
forecast   →   point
forecast   →   quantile
```

The **context** cell is the BIND_CONTEXT target. Its state hash
updates with every new context. The **forecast** cell is the FORECAST
target. It reads from context and covariate, and produces a point +
9 quantiles. The **point** and **quantile** cells are READ targets —
they read the forecast's value.

## The PROOF chain animation

When you BIND_CONTEXT, the visualizer:
1. Saves the current state_hash as prev_hash (PROVES the change).
2. Hashes the new context (FNV-1a 64-bit, 4 slices).
3. Updates state_hash.
4. Animates the PROOF chain (a small "chain link" icon appears between
   the old and new hashes).

The user can see the chain extend with every bind. The prev_hash is
shown in the right panel; the state_hash is shown beneath the context
cell.

## The abductive loop

The FORECAST operation is not a single step — it's an **abductive
loop** (5 sub-operations: PROPOSE → EXECUTE → RENDER → VERIFY → REFINE).
The visualizer animates this loop:
1. **PROPOSE** (yellow flash): the model proposes a forecast.
2. **EXECUTE** (green flash): the model runs.
3. **RENDER** (blue flash): the forecast is materialized.
4. **VERIFY** (purple flash): the cell checks the forecast shape.
5. **REFINE** (orange flash): any errors are corrected.

The user can see all 5 sub-operations as colored flashes on the
forecast cell. The total animation takes ~1.5 seconds.

## The polyformalism panel

The right panel shows the **3 polyformalism ports** side by side:
- **C** (quilt-c): the kernel-friendly stub
- **Python** (quilt-timesfm): the real TimesFM 3.0 binding
- **Rust** (quilt-timesfm-rust): the no_std embedded port

For each port, the panel shows:
- The kind name (always "time.cell")
- The op indices (always 0, 1, 2, 3, 4)
- The state hash (FNV-1a 64-bit, 32 bytes — bit-exact)
- The forecast shape ([horizon * n_variates] + [9, horizon * n_variates])

The user can verify the bit-exactness by hashing the same context in
all 3 ports and comparing.

## The patterns

The visualizer ships with 6 context patterns:
- **Sine wave**: a smooth periodic signal
- **Linear trend**: a trend + noise
- **Random walk**: Brownian motion
- **Step function**: piecewise constant
- **Seasonal**: yearly + weekly cycles
- **Real data**: trend + sine + noise (the default)

Each pattern tests a different aspect of the cell:
- Sine tests periodicity
- Trend tests drift
- Random walk tests volatility
- Step tests regime changes
- Seasonal tests multi-frequency
- Real data tests combination

## The events log

The right panel has a live events log. Every operation appends an
entry:

```
BIND_CONTEXT  len=128 · variates=1     state_hash=a1b2c3d4…
BIND_COVARIATE  past_only len=128
FORECAST  horizon=16 · 9 quantiles    state_hash=e5f6g7h8…
READ_POINT  last=12.345 (n=16)
READ_QUANTILE  q=0.5 · last=12.345
```

The user can scroll back through the entire session, see the state
hashes chain together (the PROOF trail), and verify the bit-exactness
of every operation.

## The 4 use cases

1. **Teaching Quilt**: a student opens the visualizer, sees the 5
   operations animated, plays the canonical session, and understands
   the cell model in 5 minutes.

2. **Debugging a forecast**: a developer is running TimesFM 3.0 and
   seeing weird outputs. They open the visualizer, replay the same
   context, and see where the cell's state diverges from expected.

3. **Comparing the polyformalism**: a polyformalism researcher wants
   to verify the C, Python, and Rust ports are bit-exact. They open
   the visualizer, run the same context in all 3, and compare hashes.

4. **Designing a new cell kind**: a Quilt contributor is designing a
   new cell kind. They open the visualizer, see how the time.cell
   graph is structured, and design a similar graph for their kind.

## The cowboy's verdict

> The visualizer turns a 600-line Python class into a 5-minute
> intuition. The user sees the cell graph come alive. The state hash
> chains itself. The forecast emerges from the abductive loop. The
> polyformalism becomes undeniable: the same BIND_CONTEXT in C,
> Python, and Rust produces the same hash.

> The cowboy said: this is the welcome mat. The cowboy said: the
> visualizer is the welcome mat. The cowboy built the visualizer
> in 600 lines of HTML + JS. The cowboy showed the 5 cells, 4
> edges, 5 sub-operations. The cowboy showed the PROOF chain. The
> cowboy rode the visualizer. The cowboy rode the Quilt.

## The file

`quilt-timesfm/visualizer/index.html` — 33KB, vanilla HTML + Canvas + JS.
No build step. No dependencies. Just open the file.

## The next step

A 3D version of the visualizer (using WebGL) that shows the time
series as a 3D surface, with the forecast extruding forward in time.
The cell graph is a 3D scene graph; the cells are objects in the
scene. The user can orbit, zoom, and explore.
