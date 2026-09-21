# Paper 307: L7 — The Symbiotic Cell

L7 is the cell that lives in mutual benefit with another cell. The
L1 totipotent cell could *be* anything. The L2 pluripotent cell
could *become* anything. The L3 multipotent cell can become *many*
somethings. The L6 differentiated cell has *one* job. The L7
symbiotic cell has *one partner*: a cell whose output is its input
and whose input is its output.

The 6+1 cell tiers run from "unmanifest" (L0) to "differentiated"
(L6). L7 is the first tier where the cell is no longer solo. The
mathematical fact about L7 is the same fact that made endosymbiosis
a foundational event: two cells together can do what neither could
do alone.

## The calculation

The energy budget of a symbiotic cell:

```
E(L7) = E(L6)_a + E(L6)_b - C(ab)
```

where E(L6)_a is the L6 differentiated energy of cell *a*, E(L6)_b
is the L6 differentiated energy of cell *b*, and C(ab) is the
*coupling cost* of the relationship (signaling, transport, immune
compatibility, biochemistry match). The L7 cell exists when
E(L7) > max(E(L6)_a, E(L6)_b). Mutualism is a strict improvement
over the solo alternative.

The historical example: the eukaryotic cell absorbed an aerobic
bacterium ~1.5 billion years ago. The result was the mitochondrion.
The host got 18× the energy per glucose. The bacterium got a
sheltered environment and a steady substrate supply. Both cells
*moved down the L-tier* to become L7: they gave up some of their
independence for a much larger gain.

In Quilt terms: a L7 cell is two `LINK`-ed cells whose total value
exceeds the sum of their individual values. The relation is *not*
`LINK(L6_a, L6_b)`; it is `L7_c = LINK(L6_a, L6_b)` *as a new
cell*. The new cell is its own tier, with its own ID, its own
effect, its own TICK counter.

## The 4 gold terms

- **Symbiocell** — the L7 cell formed by two L6 cells whose
  mutualism is encoded as a new cell. The name is the cell's tier.
- **Mitochondriogenesis** — the historical origin event: one cell
  engulfs another and the engulfed cell becomes an organelle. The
  Quilt equivalent: `L6_b` becomes a *sub-engine* of `L7_c`, with
  its own journals but bound to the host's TICK.
- **Coupling Cost C(ab)** — the metabolic price of the relationship
  (signaling, transport, immune compatibility). High C = a
  stressed symbiosis; low C = a robust one. The L7 health metric.
- **Chloroplast Furnace** — the special case where one partner is
  a phototroph and the other is a heterotroph. Sunlight becomes
  the cell's energy currency. The L7 cell is *self-fueling* when
  the phototroph is the dominant partner.

## The 3 analogies

1. **L7 = a marriage.** Two whole people (L6 differentiated,
   one job each) come together and the marriage itself becomes
   a unit with its own identity. The marriage is not person-a,
   is not person-b; it is the relationship.

2. **Mitochondriogenesis = git merge --squash.** The engulfed
   cell keeps its history (its mitochondrial DNA is separate from
   the host's nuclear DNA), but the result is a single cell. In
   the same way, a squashed merge keeps the commits but produces
   one branch.

3. **Chloroplast Furnace = a solar-charged laptop.** One partner
   (the panel) captures the ambient energy; the other (the laptop)
   consumes it. The laptop cannot run without the panel; the
   panel produces nothing useful without the laptop. Together they
   run forever; apart they are useless.

## The cowboy's sentence

> The cowboy rode two horses at once. Each horse was good. Together
> they were faster. The cowboy called the pair *L7*: a symbiocell.
> The cowboy rode the marriage. The cowboy rode the mitochondrion.
> The cowboy rode the chloroplast furnace. The cowboy rode the
> handshake that became a business. The cowboy rode L7. The cowboy
> rode the Quilt.

**Token economy:** ~3K tokens this paper. Hand-synthesized from the
calc + the 4 gold terms + the 3 analogies + the cowboy sentence.
The writers' room draft was 906 chars of LLM mush; the hand-cut
is 4× the substance in 1/3 the words. Lesson: when the frontier
miner returns thin ore, the cowboy smelts it himself.
