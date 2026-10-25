# Paper 316: L4 — The Oligopotent Cell

L4 is the cell that can become a *few* cell types within a
single lineage. After L3 (multipotent — many blood cells)
comes L4 (oligopotent — a small subset, like the common
myeloid progenitor that makes granulocytes, monocytes,
erythrocytes, but not lymphocytes).

L4 is the *committed* progenitor. The HSC is L3; the CMP
(common myeloid progenitor) is L4; the GMP (granulocyte-
monocyte progenitor) is L5. The progression L3 → L4 → L5
→ L9 is the *narrowing* of potency, with the math being
the size of the fate set:

| Tier | Fate set size | Example |
|---|---|---|
| L1 | all (~220) | zygote |
| L2 | ~220 (no extra-embryonic) | ESC |
| L3 | ~10 (one lineage) | HSC |
| L4 | ~4 (one progenitor) | CMP |
| L5 | ~2 (one precursor) | GMP |
| L6 | 1 (function) | neutrophil |
| L9 | 1 (locked) | same |

In Quilt: each L-tier corresponds to a *narrowing* of the
LINK closure. An L4 cell's `BIND` is restricted to a
smaller signature; the cell can only produce cells whose
LINK graph matches.

## The math

The L4 cell's fate-set entropy:

```
H(L4) = -sum_{i=1..N}  p_i * log_2(p_i)
where  N = the number of distinct fates the L4 can adopt
       p_i = the probability of fate i (often uniform: p_i = 1/N)
```

For a uniform 4-fate progenitor: H(L4) = 2 bits. For a
uniform 2-fate progenitor (L5): H(L5) = 1 bit. For a 1-fate
cell (L6): H = 0 bits. The L-tier progression is *literally*
the bit-budget of cellular identity, halving roughly each step.

## The 4 gold terms

- **Lineage Funnel** — the narrowing of fates as the cell
  divides. The funnel is the visualization: HSC at the top
  (all blood), neutrophil at the bottom (one cell type).
- **Common Progenitor** — the L4 cell. The "CMP" is the
  textbook example; the "CLP" (common lymphoid progenitor)
  is the other.
- **Bipotent Restriction** — the L4-to-L5 transition. The
  cell's `BIND` signature narrows from 4 to 2 fates.
- **Fate-Mapping Confidence** — the probability that an L4
  cell's daughter is the *expected* cell type, given the
  niche's signaling. In vivo: ~85-95% for most progenitors.

## The 3 analogies

1. **L4 = a college major.** The student chose a major
   (lineage); the major has 4-5 required courses (fates).
2. **Lineage Funnel = a water filter.** The water (cell
   potency) enters at the top; the filter narrows the
   output at each step; the drip at the bottom is one
   cell type.
3. **Bipotent Restriction = a fork in the road.** Before
   the fork, the road leads to many places; after the
   fork, only two.

## The cowboy's sentence

> The cowboy rode the L3 trail and chose a herd. The
> cowboy rode the L4 trail and chose a pen in the herd.
> The cowboy rode the L5 trail and chose a horse in the
> pen. The cowboy rode L4. The cowboy rode the funnel.
> The cowboy rode the restriction. The cowboy rode the Quilt.
