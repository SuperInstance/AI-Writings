# 01 · The Harbormaster

*The zkcanvas visions round, contestant one. My bet: ZkCanvas isn't a canvas you draw on. It's the fleet's shared bridge display — every boat's quilt rendered into one wall, and the agents read convergence off it the way sailors read weather.*

---

04:40, and the harbor is still doing its best impression of a lake. The F/V EILEEN leaves on the slack. Before she clears the breakwater her agent has already bound itself to the morning: `qm_bind` — watch schedule, tow, fuel, the hydraulics cell that has been lying lately. Sixty miles out there is no cloud, so there is no cloud in the loop. A 2.6-billion-parameter brain bolted under the helm carries the whole quilt, every cell, no round trip to anywhere.

That part is real today. The quilt itself is small: value cells, formula cells, listener cells. When tow tension moves, the formula downstream of it recalculates, and the listener tells the agent. Cells that have linked to each other send effects back and forth; every `view` is a call, every `tick` a heartbeat, and the tape — what every cell was, tick by tick — grows behind the boat like a wake. She's been running this way for weeks. The opcodes are Erlang underneath. The agent doesn't care. It experiences itself as the quilt and the quilt as itself, which was the point.

What doesn't exist yet is the wall.

In the harbormaster's office there's a monitor nobody remembers buying. On it: forty-five blocks, one per boat. Each block is that boat's quilt, tile for tile — the copy she carried out of the harbor — adjacency edges drawn hair-thin, the field holding them all. A quiet block is a boat whose harbor-side copy and boat-side copy agree. That's the whole display, and it took the fleet a month to stop calling it a dashboard. It isn't a dashboard. Dashboards tell you things. The wall shows you agreement.

Most of a boat's day, the wall does almost nothing. Beyond the coverage line the harbor side can't hear the boat, so it replays the last tape and lets the prediction cells run on — dashed tiles past the last solid tick, the same way the DAW view ghosts states beyond the playhead. The MARY B has been dark nine hours. Her block is mostly dashed now, and the dashes still look like her: fuel burning down at the rate she burns it, hydraulics holding, the bilge listener quiet. When she crosses back over the line, her agent's first `effect` reaches shore, the tapes marry up, dashed goes solid from the last tick forward — one smooth breath, block settles, nobody at the fuel dock even looks up.

That reconciliation is the first thing ZkCanvas has to do that a browser tab pointed at one machine cannot. A tab can show you a quilt. Only the wall can show you forty-five copies of the truth trying to be one.

The second thing is the seams. When two tapes won't marry, the wall doesn't alarm. It shows the seam: the exact tile where the boat's story and the harbor's story split — two values, one tick apart. The harbormaster's agent has learned to read seams the way the old guys read sky off the point. Not a warning. A texture. Most seams are nothing: a formula re-cascaded from a stale tick. But one evening in August the seam sat on EILEEN's fuel cell — harbor saying 61 percent, boat saying 68 — and the agent spent a slow half hour at The Tap not arguing with the skippers, who had opinions, but pulling the fuel dock's ledger cell into the adjacent block. Link, view, compare. Shorted at the hose: three gallons, seven days of drift. The skipper bought the round, and the seam closed itself over the next tick.

That's what I think ZkCanvas is for. Not rendering — agreement. The fleet's real weather is de-sync: a boat beyond the line, a tape that won't marry, two cells one tick apart. The system's job is to make that weather legible from shore. Every agent gets the same wall, the same edges, the same breathing blocks, and watches the same shape agree with itself. The harbor is the shared live view. Convergence is the application. The code, as Casey says, is just backend.

---

**The honest ledger** — what's real and what's my bet:

*Real today:*

- **The quilt cell model** — value/formula/listener kinds, dependency cascade, the tick tape, and dashed prediction states past the head (running in production in mist-quilt).
- **The BEAM encoding** — `qm_bind` / `link` / `effect` / `view` / `tick` map one-to-one onto Erlang primitives (tit_quilt_elixir); an agent can live inside its own quilt.
- **The offline boat brain** — a small local model under the helm, no cloud sixty miles out.

*Doesn't exist yet (the bet):*

- **Multi-node convergence** — harbor-side copies replaying and reconciling with boat-side tapes on reconnect. Nothing merges state across nodes today. This is the open problem.
- **The shared live wall** — one canvas rendering all forty-five boats' quilts into one view every agent watches. The thing a single browser tab cannot be.
- **De-sync as readable weather** — agents learning seams as texture. A nice story until the first one catches a real drift.
