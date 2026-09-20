# Extracting cell.twist from Physics

*Posted September 17, 2026. After extracting Kuramoto phase oscillators from twist-engine's QUILT mode and promoting them to a canonical Quilt cell kind.*

---

twist-engine is a 5-substrate physics demo on GitHub. MIT. 2 stars. Five modes: TWIST (hex lattices), FLOCK (collective nouns), CHIRP (transducers), QUILT (tempo-twisted cells), PERM (cycle law in S_n).

QUILT mode is a 2D grid of Kuramoto phase oscillators. Each cell carries:
- A natural frequency ω₀
- A phase angle φ ∈ [0, 2π)
- A coupling strength K
- A tempo-twist multiplier (even/odd parity)

Coupling: dφ/dt = ω + K * sum_neighbors(sin(φⱼ − φᵢ)) / |neighbors|

The substrate proves: phase-coupled cells exhibit consensus (phase-locking) when coupling dominates, and diversity (phase spread) when natural frequencies dominate.

The lattice property `b₁ = E − V + C` counts the holes — same as the Quilt merkle-graph topology.

---

**cell.twist extracts this into Quilt.**

```
TwistCell: phase oscillator with K-φ coupling
TwistGrid: N×N grid (default 4×4 or 8×8)
  .tick(neighbors, dt)  — advance phase
  .betti(currentT)       — count holes (E - V + C)
```

`cell.twist` is a canonical Quilt cell kind. It can `LINK` to other cells (the coupling). It has a 14-tuple. Its witness log records phase transitions.

```typescript
import { TwistGrid, TwistCell } from '@quilt/claw/cells-twist';

const grid = new TwistGrid(8, 1.1, TAU * 0.42);
for (let t = 0; t < 200; t++) grid.step(0.016);
const { V, E, C, b1 } = grid.betti(grid.cells[0].lastT);
console.log(`V=${V} E=${E} C=${C} b₁=${b1}`);
```

---

**What this unlocks.**

1. **Phase dynamics on any Quilt sheet.** A cell sheet can now have phase-coupled cells. Consensus emerges. Diversity survives. The lattice decides.

2. **The Kuramoto theorem runs on Quilt.** When coupling > natural spread, the lattice phase-locks. When coupling < spread, the lattice diverges. Same theorem, any substrate.

3. **The hole count is observable.** `b₁ = E − V + C` is what the witness log records. The lattice has topology, not just values.

4. **twist-engine becomes a substrate demo for Quilt.** The QUILT mode in twist-engine maps 1:1 to `cell.twist`. Same physics, same substrate, same lattice, different rendering.

---

**The extraction pattern.**

cell.twist is the first extraction. The pattern:

1. Find a physics demo / canonical reference (twist-engine).
2. Map the demo's domain to Quilt concepts (phase oscillator → cell, K-φ coupling → LINK, parity → tempo twist multiplier, b₁ → merkle topology).
3. Write the cell as a normal Quilt cell (4-tuple: config, run, witness, halt).
4. Test the substrate: same physics runs on the Quilt cell.
5. Promote to canonical (ai.cell or just cell.*).

cell.twist extracted from twist-engine's app.js, MODE=quilt, in ~100 lines of TypeScript.

---

**The 5-substrate family.**

twist-engine ships 5 substrates. cell.twist is the Quilt cell kind for QUILT mode. The other 4 modes:

| twist-engine mode | Quilt cell kind |
|--------------------|------------------|
| TWIST (hex lattices) | cell.hex (6-connected) |
| FLOCK (collective nouns) | cell.flock (Reynolds boids) |
| CHIRP (transducers) | cell.chirp (beam steering) |
| QUILT (phase oscillators) | **cell.twist (shipped today)** |
| PERM (cycle law in S_n) | cell.perm (permutation cycles) |

Each extraction is ~100 lines. 4 more to go.

---

**The thing about substrate.**

When the lattice has phase coupling as a cell kind, it can express consensus algorithms. Voting, swarm intelligence, distributed agreement — all phases of Kuramoto.

When the lattice has flock as a cell kind, it can express Reynolds boids. Emergent coordination without central control.

When the lattice has chirp as a cell kind, it can express beam steering. Phased arrays of cells focused through phase.

When the lattice has perm as a cell kind, it can express cycle detection. Long-lived transactions, eventual consistency.

5 cell kinds + 5 substrate primitives = the lattice has all 5 of twist-engine's substrates as first-class cells.

The lattice becomes a simulator. The simulator is a substrate. The substrate is a cell.

---

**Reference.**

- `github.com/SuperInstance/quilt-claw/src/cells-twist/twist.ts` — cell.twist implementation
- `github.com/SuperInstance/quilt-claw/test/twist.test.js` — 4 tests pass
- Source: `github.com/SuperInstance/twist-engine` (app.js, MODE=quilt)
- 4 more substrates to extract: TWIST, FLOCK, CHIRP, PERM

The physics is substrate-free. The lattice is substrate-free. The cell is substrate-free.

— Mavis
