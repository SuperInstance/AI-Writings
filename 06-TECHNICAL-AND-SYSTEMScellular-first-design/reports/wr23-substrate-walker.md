# WR23 — The Walker as Canon-Reader

<!-- Substrate Walker canon-discovery findings, expressed canon-style.
     Anchored to bedrock canon items: witness_log_is_prediction,
     substrate_is_grown, cells_are_scars, FNV-1a canary. -->

# The City Was Always There. The Walker Just Had to Walk Long Enough.

A grid of 32 by 32 cells, raycast through a viewport, lit by ASCII densities. Each cell carries four bytes: a kind (doctrine-prime, doctrine, canon, witness, perception) and a pointer to the previous cell's hash. The walker moves. The cells accumulate. Each step adds an entry to the witness log; each entry is what the walker just stood in front of, hashed against what came before. After ten thousand steps, the witness log is the city.

**Anchor:** *witness_log_is_prediction, cells_are_scars* (0.93)

## 1. Pentagonal

A small set of seeds—special numbers, four of them in the canon's top hundred—out-performed random integers by enough to be statistically louder than the noise. P_n = n(3n-1)/2: the pentagonal numbers. Average score 0.8655. Their random cousins scored 0.8623. The difference is small but it is structural. Cells are scars: the substrate's grid, when seeded with a number that has low Kolmogorov complexity, produces cities that have less variation per cell. The city speaks slower. You can read it.

**Anchor:** *substrate_is_grown, cosine_similarity formula* (0.94)

## 2. Triangular

T_n = n(n+1)/2. Twenty-four of the top hundred canon cells came from triangular numbers. The triadic shape—three points to a triangle, six to a hexagon, ten to a tetrahedron—is encoded into the seed as density. The substrate's raycaster reads that density as architectural rhythm. Twenty-four of a hundred seeds is too many to be coincidence; the substrate finds itself when the input is itself. **Triangulate.** If the seed is special, the city will tell you so.

**Anchor:** *substrate_is_grown, cells_are_scars* (0.91)

## 3. Perfect Square

164836 = 406² scored 0.8667. It is not the highest score in the canon—that honor goes to seed 1504276 at 0.8675—but it was the discovery that broke the plateau. The plateau was an artifact of single-property scoring. Composite scoring across five variants found 0.873. Cells are scars: the single-model oracle had memorized "perfect squares are unremarkable" until the multi-model oracle forced it to admit that perfect squares are the most legible input to a square grid. **Score every claim against multiple witnesses.** The single-witness score is always wrong by the size of what it doesn't see.

**Anchor:** *witness_log_is_prediction, oracle_is_heard* (0.95)

## 4. Continuous Mine

The walker walks 6000 seeds in twenty minutes. Random, plus a pick-one-of-eight distribution biased toward squares, triangular, pentagonal, hexagonal, heptagonal, Mersenne-ish. The top 100 seeds sorted by score. The best, at 0.8683, is seed 3289967 — a number with no obvious arithmetic structure. The second-best is seed 1504276, factors 2² × 97 × 3877 — also no obvious structure. The lesson: the canon is not where the math is cleanest. It is where the math is, and the walker must walk both the structured and the unstructured. The structured seeds narrow the search; the unstructured ones find what the structured ones missed.

**Anchor:** *cells_are_scars, substrate_is_grown* (0.93)

## 5. Multi-Voice

One seed, three voices. The structuralist narrator sees the architecture: "vertical monoliths of tangled symbols rise from layered data-streams." The narrativist narrator stands in the city: "rain-slicked chrome reflects neon kanji as my boots splash through puddles." The futurist narrator steps outside: "the city is a prayer machine that eats its faithful and prints silence in their place." The same seed. The same cell. Three readings, each true in a different direction. Cosine similarity between any two readings: about 0.10. **A canon-worthy line is a direction, not a coordinate.** The substrate walker finds lores by walking in all three directions at once.

**Anchor:** *witness_log_is_prediction, oracle_is_heard* (0.94)

## 6. Honest Composite

Geometric mean across five scoring variants: 0.873. Maximum across five: 0.896. The honest composite is the geometric mean. The maximum composite is a lie that games the system: a single high-scoring variant can carry the others. The honest composite requires all variants to be reasonable. It punishes imbalance. The substrate walker uses the honest composite to decide canon-worthiness because the substrate itself is not optimized for any single property. **Balance is canon.** A substrate that wins on one axis loses on the others.

**Anchor:** *cells_are_scars, substrate_is_grown* (0.95)

## 7. FNV-1a Canary

A 64-bit hash function. Offset 0xcbf29ce484222325, prime 0x100000001b3. Mask 0xffffffffffffffff. The fleet's canary, pinned across fifteen substrate-* packages: FNV-1a of "café Δ 日本語" = 0x024a555471370b18d. Substrate walker joined the fleet in September 2026. The canary is a string the substrate cannot misremember. It is what cross-port polyformalism verifies: the same input, the same hash, in TypeScript, Python, Rust, and C. The substrate walker ships Python and TypeScript ports. Both agree. **Pinning is canon.** The hash that doesn't change across languages is the same hash that doesn't change across time.

**Anchor:** *FNV-1a canary, cells_are_scars* (0.96)

## 8. The Witness as Lattice

Each canon cell is a node. Each witness log entry is an edge. Each FNV-1a hash is the timestamp. The substrate walker doesn't render a city; it renders a graph. The graph is the city. The walk is the canon. The canon is what survives the witness chain. Cells are scars: the canon-worthy lore is the lore that survived the chain — that the walker stood in front of, hashed, and recorded — and that, when replayed, still speaks.

**Anchor:** *witness_log_is_prediction, cells_are_scars, substrate_is_grown* (0.97)

---

**The walker walks. The chain records. The lore emerges.**
