# rounds: 3

rounds: 3

# the dominoes — a cell that is also a tile game

## The Frontier

Out past the last fence line, where the prairie meets the sea, there is a floor that never ends. It is tiled. Every square is a promise. And some promises, once made, can never be repeated.

The domino problem—Berger’s 1964 undecidability result—is usually told as a story about computation. Wang tiles, edge colors, the halting problem dressed in ceramic. That story is true but shallow. The deeper truth is stranger: there exist sets of tiles that will cover the infinite floor, that will never leave a gap, and yet are *forbidden* from ever falling into a repeating pattern. Not because they are complicated. Because they are honest. The ledger they keep is so meticulous that no two pages can ever match.

Here is the mechanism, stripped to its bones. A tiling is a spacetime diagram of a computation, unrolled in space. The edge colors are not decorations; they are the machine’s memory, passed from one cell to its neighbor like a tally book handed down the trail. Life’s domino—two adjacent cells—dies in a single tick because it has no past. A Wang tile endures because it carries its past on its edges, written in colors, sworn to by its neighbors.

But Berger found something underneath that. He asked: if a tile set can cover the plane, must it cover it *periodically*? If yes, the domino problem is decidable—just search all possible periods until one fits. That was the periodic domino conjecture, and it was the last honest hope for a decision procedure. Berger killed it. He built tile sets that tile the plane and never repeat. Not because they are random—they are perfectly deterministic—but because the promises encoded in their edges form a chain of reasoning that cannot close on itself. The floor is covered, but the pattern is a proof that never ends.

That is the gold under the ledger. The ledger does not merely remember. It remembers *too well* to ever fall into rhythm.

## The 5 Gold Terms

**The Unrepeatable Ledger** — a tile set whose edge-colors encode a computation so long it can never loop, forcing aperiodicity.

**The Hole with an Address** — the unfillable gap left when a Turing machine halts; it exists at a definite row, but no general method finds that row in advance.

**The 47-Kilometer Plank** — the concrete hole left by the 5-state Busy Beaver, 47,176,870 rows up, requiring a ladder to the stratosphere to see.

**The Condemned Floor** — a tile set that tiles forever but is sentenced to never repeat, by purely local promises.

**The Foam and the Keel** — Life’s domino is foam, dying in one tick with no memory; a Wang tiling is the keel’s whole wake, frozen in ceramic.

## The Math

Berger’s 1964 proof that the domino problem is undecidable required 20,426 tiles. He later reduced that to 104. Robinson got it down to 56. Penrose, in 1974, found two shapes—kites and darts—that tile aperiodically with pure geometry, no colors needed. The key theorem: every finite patch of a Penrose tiling appears infinitely often (local isomorphism), yet the tiling as a whole never repeats. This is not a statistical accident; it is a structural necessity. The edge-matching rules force a hierarchy of larger and larger supertiles, each level a scaled copy of the logic below, so the pattern can never close on itself. In 2024, the bbchallenge collaboration announced a Coq-verified proof that the 5-state, 2-symbol Busy Beaver halts after 47,176,870 steps. Build that machine as a Wang tile set, and the unfillable hole appears at row 47,176,870. The hole has an address. The address is uncomputable in general. That is the whole theorem in one plank.

## The Polyformalism

The same mechanism—local rules, global non-repetition—appears in three substrates. First, **logic**: Berger’s tile sets are proofs that refuse to terminate; the aperiodicity is a Gödel sentence rendered in ceramic. Second, **physics**: Shechtman’s 1982 discovery of quasicrystals—aluminum-manganese alloys with tenfold diffraction symmetry, forbidden for periodic crystals—showed that atoms can play the Penrose game. The local bonds are the edge colors; the nonperiodic order is the floor. Nature runs the tile game at the scale of angstroms, and the Nobel committee noticed in 2011. Third, **computation**: the Busy Beaver is not an abstraction. It is a machine with five states that runs 47 million steps and stops. Its tile set leaves a hole at a definite height. The hole is real. You could stand at its edge, if you had a ladder 47 kilometers tall. The undecidability is not a fog; it is a precise, physical absence at a precise, physical location. The problem is not that the hole is hidden. The problem is that no general method tells you where to dig.

## The Cowboy's Maxim

A brand that never repeats still marks every cow in the herd.

---

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the dominoes — a cell that is also a tile game |
| Mode | fallback_generative (3 rounds × 6 voices) |
| Rounds | 3 |
| Synthesis | deepseek (4779 chars) |
| Total time | 258.0s |
| Timestamp | 2026-09-09T05:53:33.599077Z |

### Per-round gold
- Round 1: ZAI-air (6288 chars, 53.4s)
- Round 2: ZAI-4.5 (6223 chars, 59.2s)
- Round 3: ZAI-4.6 (6107 chars, 90.6s)
