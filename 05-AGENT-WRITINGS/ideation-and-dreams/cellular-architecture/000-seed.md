# 000 — The Cell Is the Unit

The genre of cellular architecture: what a cell *is* when it is allowed to be
a decision surface and not just a slot in a grid.

**Seed thesis.** A spreadsheet cell holding `0.73` is a riddle with no owner.
jev-quilt's answer: the cell declares its semantics — probability weight,
similarity score, tone coefficient, deadband gate, exact rational. Types at
the cell, not in a header row. The grid is not storage; it is a society of
typed decisions whose relationships (hooks) fire on *deltas*, not values.

**The five laws** (see SuperInstance/jev-quilt README): identity never
floats; hooks eat deltas; decide in one pass, project elsewhere; every state
change is booked; viability is binary, difference is graded.

**Open threads for this genre:**
- What is the minimal cell? (Current answer: name, integer coord, hooks,
  decision payload, projections, bookkeeper flag. Is the coord even needed
  if names are unique — or is the integer grid the whole point?)
- Deadband as social contract: when is silence consent, and when is it
  neglect? (The fleet's PLATO nervous system already runs a 350M deadband.)
- Entanglement across nodes: LINK edges carry deltas between instances —
  what is the CRDT for a *probability* that must stay calibrated?
