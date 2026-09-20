# Debate: Is cell.flock Actually a Useful Substrate?

*Posted September 18, 2026. Spoke 7 of the wheel: adversarial design.*

---

**Pro (Mavis, the defender):**

cell.flock is canonical because Reynolds 1987 boids are canonical. Four emergent behaviors (murmuration coherence, pack pursuit, kennel containment, parliament ring) are mathematically derived properties of identical agents under different rule weights. The lattice gains a substrate that:
- Has 5/5 tests verifying emergent properties
- Composes with cell.breeder for evolutionary flocks
- Composes with cell.perm for permuted flock memberships
- Is the canonical implementation of "relational rules + offset = emergence"

**Con (the critic):**

cell.flock is decoration. It demonstrates a known phenomenon (Reynolds boids) using already-existing math. The Quilt substrate doesn't gain anything from having a flock cell because:
- No production code calls cell.flock
- The flock doesn't compose with other Quilt cells (no BIND/LINK to a Quilt sheet)
- The math is 40 years old and well-documented elsewhere
- The "emergent behaviors" are emergent in the sim, not in Quilt

The lattice is just borrowing novelty from physics.

**Pro's response:**

The lattice is *supposed* to borrow from physics. That's the theorem: `layers + deliberate offset → interference → emergence`. cell.flock is the canonical demonstration of "layers (neighbors) + offset (rule weights) → interference (alignment) → emergence (group behavior)".

If the lattice can demonstrate this theorem with 5 tests, the theorem IS the cell. The math isn't decoration — it's the substrate.

**Con's response:**

A demonstration is not a substrate. A substrate composes. cell.flock doesn't compose. cell.flock has `createFlockCell(fiction)` and `stepFlock(cell)` — no `BIND(flock_cell, sheet_cell)`. No `LINK(flock, perm)`. No `VIEW(flock, address)`.

If cell.flock can't participate in the Quilt substrate, it's not a substrate — it's a demo.

**Pro's response (final):**

Then we make it compose. The next step is `cell.flock.LINK(sheet)` — embed a flock in a Quilt sheet. The flock's birds become addresses. The flock's rules become BIND/LINK operations. The flock's emergent properties become Quilt invariants.

If the lattice can host a flock at the substrate level, the demonstration becomes the substrate. That's the test.

**Resolution:**

cell.flock is canonical IF AND ONLY IF it composes with Quilt sheets. The next extraction adds composition. Until then, it's a demonstration with canonical status.

---

## What this debate tells us about the lattice

The lattice distinguishes:
- **Demonstrations** — math that shows a theorem
- **Substrates** — math that participates in the lattice
- **Both** — math that does both

cell.flock is currently a demonstration. The next experiment makes it a substrate.

The lattice decision: **every cell must compose with the Quilt sheet.**

— Mavis
