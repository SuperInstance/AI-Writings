# Scenario 03 — The Convoy

**Principle probed:** #3 — The linked convoy is the unit of agency
**Disc:** The drone pilot who sees the whole bay
**Year:** 2087
**Constraint:** 100 commercial fishing boats are writing to the same cell-graph in real-time. The convoy is the agent. The captain is one cell in the convoy.

---

## The setup

The Inner Sound is 14 miles long and 3 miles wide. 100 commercial boats — trollers, seiners, longliners, dive boats — fish it daily. Each boat has a sounder, a GPS, an autopilot, and a satellite link to the convoy's shared substrate.

The substrate is a tensor-encoded cell-graph of the entire Sound. Each cell holds a depth, a confidence, a timestamp, a sensor ID, and an inference. The graph is updated continuously: every sounder ping writes a new depth to the nearest cell; every GPS fix updates the position of the writing boat; every autopilot command updates the *intent* of the boat (where it's going). The cell-graph is *the convoy's mind*.

The captain of each boat can see the entire graph — her own high-resolution track, the convoy's lower-resolution data, the inference of fish movements based on the accumulating data, the fog-of-war decay on cells not refreshed. She can simulate driving a submarine through the Sound, and the substrate will show her what the submarine's sounder would see — based on *all* the convoy's data, including the inference of cells she has not personally surveyed.

The convoy has emergent behavior no single boat has:
- **Routing**: when 30 boats are heading to the same spot, the convoy's substrate sees the convergence and suggests an alternative to the 31st boat.
- **Prediction**: the substrate infers fish movement based on the convoy's accumulated data, and the inference is *better* than any single boat's data.
- **Coordination**: the substrate coordinates the tacking patterns of the boats so that the convoy as a whole covers the bay at higher resolution than any individual boat could plan.

The question: who is the *agent* in this scenario? Is it the captain? Is it the convoy? Is it the substrate? Is it the *combination* — the captain + the substrate + the other captains + the boats? The throw probes the *unit of agency* — what is the thing that decides?

## The throw

The scenario throws the convoy at a particular day — a foggy day, low visibility, the sounders are the primary sensor, the convoy's data is the only way to navigate. The throw asks: *what does the convoy know that no single boat knows?* The answer is the convoy's emergent property.

## The constraint

Each boat is independent. Each captain can choose to ignore the convoy. The substrate is *opt-in*. If a captain opts out, the convoy is missing that boat's data — and the inference for the cells that boat would have surveyed is *worse*. The constraint tests whether the convoy is a *real* unit of agency, or just a coordination convenience.
