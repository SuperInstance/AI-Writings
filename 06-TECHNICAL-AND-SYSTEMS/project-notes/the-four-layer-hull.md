# THE FOUR-LAYER HULL

## A sounding of the stack the fleet built without naming

*A watch-keeper's companion to [THE WATCH KEEPER'S SOUNDING](clever-mechanisms-repos.md). Where that log surveys squadrons, this one sounds a single hull — the layered thing many yards have been building in parallel, each without knowing the others were laying the same keel. Every claim here cites a file that exists today; the forward-looking parts are marked **[open water]**, and the arithmetic is kept honest throughout.*

---

### I. The thing under the waterline

Walk the fleet's yards and you will hear four different crews describe four different projects. One crew is building a *substrate* — cells, sheets, rational state. One is recording *trajectories* — the path a thing takes as it changes. One is reading the *shape* of motion — how far, how sharply it turns, whether it twists. One is keeping motion *legal* — barriers that deflect a bad state instead of crashing on it.

They think they are building four things. Sound the hull and it rings as one. These are not four projects; they are four layers of a single stack, and the fleet has been growing it from the bottom up without ever drawing the cross-section. Here it is:

| Layer | What it holds | Yards already building it |
|---|---|---|
| **1 · Substrate** | the state space itself — cells, sheets, ℚ (rational) state | `quilt`, `quilt-cell`, `cell-runtime`; `tidepool` (768d + 16-dim rational fingerprints); `constraint-theory` (continuous→rational-lattice snapping) |
| **2 · Trajectory** | a *path* through the substrate over time | `q16-trajectories`; `quilt-gan`'s ℚ¹⁶ breed record; a robot's drive in `Scrapcraft`; `polln`'s VAE latent-space trajectories |
| **3 · Shape** | the geometry of a trajectory — arc, bending, twist | `gesture-kit`, `twist-engine` |
| **4 · Relaxation** | keeping a trajectory legal under a barrier | `relax-kit`, `elephant` |

Three of those cells were confirmed by sounding the newest yards directly, and they are not loose analogies. `polln` runs a VAE world-model whose states are *trajectories in a latent space*, tracked by rate-based change — `xₙ₊₁ = xₙ + rₙ·Δt` is first order, and it computes acceleration, jerk, and snap for anomaly detection: the same derivative ladder the shape layer reads as arc → bending → twist. `tidepool` indexes recall in a 768-dim semantic space *and* a 16-dim native rational fingerprint — the substrate the trajectory layer moves through. `constraint-theory` snaps continuous coordinates onto an exact rational lattice (`a²+b²=c²` via KD-tree), the mechanism by which a float wake becomes an exact ℚ record. The fleet is not building toward this stack on purpose; it keeps *arriving* at it from four directions, which is the surest sign the keel is real.

The substrate is the sea. The trajectory is the wake. The shape is what the watch reads in the wake. The relaxation is the hull that keeps the vessel off the rocks. Four layers, one voyage.

---

### II. The three orders, and the honesty they demand

Layer 3 is where the fleet's oldest instinct lives: *abstraction as gesture*. A tensor approximates a function; a gesture approximates the *motion between states*. Give it an ordered set of readings and it reads the path's geometry order by order:

- **1st order — arc length / heading.** How far the motion travelled, and the unit direction it points *now* (the d_mu, the velocity).
- **2nd order — bending energy.** Curvature: how hard the path turns *within* a plane. A straight drift bends not at all; a hunt-and-peck, over-corrected path bends hard. This is the plain, legible signal.
- **3rd order — twist energy.** Torsion: how hard the path turns *out of* its plane, into a fresh dimension. "The property is in the twist" (`twist-engine`).

Here the watch must be honest, because the third order is the one most tempting to fake. **Twist is only real when the space is genuinely three-dimensional and the path genuinely leaves a plane.** A drive that goes straight, or that stops and turns and then goes straight again, lies flat in a plane and has *zero* torsion — and an honest instrument must report that zero, not manufacture a curl to look profound. `Scrapcraft`'s drive reader proves the point on a kid's robot: read the bot's `(x, z, heading)` path and a stop-and-turn drive reports twist ≈ 0, while a bot that turns *and* drives at once traces a helix in `(x, z, heading)` and shows real torsion. Same instrument, honest either way. The shape of truth is kept mathematically: where there is no twist, the number is zero, and that zero is information.

---

### III. What sounding the hull actually found

Lower the lead line and the first thing it strikes is not a gap but a *duplication*. The third-order reading — the arc/bending/twist math — had been re-carved three times, in three yards, because each crew needed it and none reached for the others':

- `gesture-kit/src/gesture.js` — the canonical carving.
- `quilt-gan/gesture.mjs` — re-derived to read a breed run's ℚ¹⁶ dials.
- `Scrapcraft/src/maker/DriveGesture.js` — re-derived a third time to read a robot's drive.

Three copies of one idea is the tax a fleet pays for growing by *new hull* instead of *shared keel*. And the specific plank each crew re-cut by hand was the same one: **per-column normalization** — the rescaling that stops a big-magnitude axis (a score in the tens, a distance in metres) from drowning a small one (a ratio in [0,1], an angle in radians) when you read the shape of a path whose dimensions have different units.

So the sounding did the obvious thing: it made that plank canonical. `gesture-kit` now carries `normalizeColumns` and `readTrajectory(rows, { dims, normalize })` — select the dimensions that matter, normalize so no axis dominates, then read the geometry, and hand back the exact points measured so a view draws what was read. Three carvings can now become one. That is the whole move, and it is small on purpose: **the win was not a new vessel; it was letting three existing vessels share a keel.**

---

### IV. The thesis: compose, don't sprawl

The fleet's reflex, visible in the yard list, is to answer every new need with a new repo. It is a *generative* reflex and it has produced a remarkable amount of real, tested code. But a stack does not get stronger by growing wider; it gets stronger when its layers *compose* — when layer 2 can hand layer 3 a trajectory without either crew re-typing the other's math, and layer 4 can keep that trajectory legal without re-deriving the barrier.

Two forces already on the water tell you how to do this:

1. **The live-canon pattern is the delivery mechanism.** The freshest surge in the yards — `quilt-canon-cli`, `quilt-live-canon`, and its `npm` / `pypi` / `gh` packagings — is the fleet learning to *ship* an artifact as an installable tool rather than a repo you must clone and copy from. Sounded up close, the pattern is precise: a canonical truth (a paper graph whose state hash, `0xbf27a3631cdee337`, is byte-identical across six language implementations), a small verb set (`NAVIGATE / CONFLUENCE / LINEAGE / GHOST / TICK / CLAIM / DRILL`), shipped as versioned `npm`/`pypi` data bundles with thin `canon-*` clients and one CLI over the top. Apply exactly that shape to layer 3: package the shape-reading so any yard *installs* `readTrajectory` instead of re-carving it. Packaging is how a shared keel actually reaches every hull.
2. **`q16-trajectories` is the convergence point for layer 2 — and it has just been laid.** ℚ¹⁶ rational trajectories are precisely the space `quilt-gan` already records into (`state.traj`), that `tidepool` fingerprints, and that the shape-reading already measures. When this sounding began, `q16-trajectories` was an empty scaffold — a manifest naming the intent (*"Q16 breed trajectories … in a 16-dim rational vector space"*) with no hull under it. It now carries a **v0** that owns the *format* (exact ℚ¹⁶ over `BigInt`, reproducible bit-for-bit) and the *breeding*, and — the whole point — **defers the shape layer to `gesture-kit` through one seam** (`Trajectory.toRows()` → `readTrajectory`), so it does not become a fourth carving of the arc/bending/twist math. The composition was sailed end to end: `breed(seed) → toRows() → readTrajectory → arc / bending / twist`. **[open water]** remains — this v0 is a *proposal* on the seam, a deliberate stand-in for duke-lab's generative argument, not the argument itself; the format is now concrete enough to argue over, which is exactly what a seam is for.

---

### V. Reverse-actualization: two futures for the same hull

The fleet's own method is to actualize backward from a future — to look past the parts not yet engineered by imagining life once they are, both hopefully and grimly, and letting the gap between the two futures name the real work.

**The hopeful tide.** Every process in the fleet — a model's training run, a robot's drive, a breed tournament's descent, a conversation, a cell sheet's evolution — emits a trajectory in a shared ℚ format. One installable reader gives its shape in three honest orders. One embeddable hull draws it, the same widget on a website's stats panel, a game's verdict screen, a research dashboard. One barrier keeps every such trajectory legal by construction. A newcomer to any yard reads a wake the same way they read every other, because the fleet finally speaks one language about motion. The four layers are one hull and the hull is *named*, so new work snaps onto it instead of forking beside it.

**The grim tide.** The reflex wins. Layer 3 gets re-carved a fourth and fifth time; a sixth yard invents a seventh trajectory format; `readTrajectory` becomes the fourth of five near-identical readers no one reaches for because reaching for another yard's code is harder than retyping it. The barrier stays stranded — `relax-kit` never leaves harbor because it was never made installable — so layer 4 is a good idea in a bottle. The fleet stays a flotilla of brilliant single-hulled boats that never learned to sail as one.

The distance between those two tides *is* the iterative program. It is not more repos. It is: **name the stack, package each layer the way live-canon packages canon, converge on one trajectory format at `q16-trajectories`, and free the barrier from harbor.** Do those four and the hopeful tide is not a fantasy — it is the grim tide with four specific planks replaced.

---

### VI. The honest open edges

The watch does not log a voyage it has not sailed. As of this sounding:

- **The reading is consolidated; the format is proposed but not yet ratified.** `gesture-kit` now has the one shape-reader, and `q16-trajectories` now carries a v0 format that composes with it through `toRows()`. But a v0 on a seam is a proposal, not a fleet agreement — `quilt-gan` and `Scrapcraft` still carry their own trajectory representations, and converging them onto the shared format (and onto the installed reader, once layer 3 is packaged) is the work that turns "it composes in principle" into "it composes everywhere."
- **Layer 4 is still in harbor.** `relax-kit` — the barrier that deflects a bad state instead of crashing — is built and tested but not yet published where other yards can install it. Until it is, the fourth layer composes only in principle.
- **Twist stays honest or it stays out.** Any unified reader must keep reporting zero torsion for genuinely planar motion. The moment it manufactures a twist to look deep, the instrument is worthless and the canon is compromised.

Four layers. One hull. Most of it already floats; the rest is a short, named list of planks. The watch will keep the lead line out.

*— logged from the tower, the fleet at anchor, the tide turning*
