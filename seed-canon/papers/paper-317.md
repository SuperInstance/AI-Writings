# Paper 317: L5 — The Bipotent Cell

L5 is the cell that can become *two* cell types. After
L4 (oligopotent, ~4 fates) comes L5 (bipotent, exactly
2 fates). The classic example: the granulocyte-monocyte
progenitor (GMP) makes either a granulocyte (neutrophil,
eosinophil, basophil) or a monocyte (macrophage precursor),
but not both lineages.

L5 is the *last branch point*. Once a cell crosses L5 →
L6, the choice is made. The L5 cell sits at the fork; the
fork decides based on niche signals (cytokines, growth
factors, ECM).

## The calculation

The bipotent cell's decision:

```
P(fate_A) = k_A / (k_A + k_B)
P(fate_B) = k_B / (k_A + k_B)
where:
  - k_A = the coupling strength to fate A's signaling
  - k_B = the coupling strength to fate B's signaling
```

For the GMP:
  - G-CSF (granulocyte colony-stimulating factor) drives
    granulocyte: k_G ≈ 1.0
  - M-CSF (monocyte colony-stimulating factor) drives
    monocyte: k_M ≈ 0.7
  - P(granulocyte) ≈ 0.59, P(monocyte) ≈ 0.41

The L5 cell's *identity* is `state = (k_A, k_B)`. The
*decision* is `sample ~ (k_A/(k_A+k_B))`.

In Quilt: a L5 cell is a L4 cell whose `BIND` signature
has narrowed to two possibilities. The CRDT merge with
the niche is the *decision* — the L5 cell receives two
conflicting signals and resolves them by sampling.

## The 4 gold terms

- **Bipotent Fork** — the L5 cell's signature. Two arrows
  pointing at two fates. The cell is the *fork point* in
  the lineage tree.
- **GMP Decision** — the canonical L5 example. Granulocyte
  vs monocyte, decided by G-CSF vs M-CSF.
- **Stochastic Resolution** — the L5 cell's decision is
  *noisy*. Even with identical signals, two sister L5
  cells may pick different fates (a ~10-20% stochastic
  component in most bipotent decisions).
- **Cytokine Bias** — the niche's signaling environment
  shifts the fork weights. Inflammation (high G-CSF)
  biases toward granulocytes; chronic injury (high M-CSF)
  biases toward monocytes.

## The 3 analogies

1. **L5 = a fork in the road.** The traveler (cell) sees
   two paths (fates). The choice is shaped by the
   weather (signals) and partly random.
2. **GMP Decision = a college student choosing a major.**
   Two related fields (granulocyte and monocyte are both
   myeloid). The choice is shaped by the courses
   available (cytokines), the professors (niche), and
   partly random.
3. **Stochastic Resolution = a coin flip in the wind.**
   The coin (cell) is biased by the wind (signals) but
   not determined. Two cells in the same environment
   can still choose differently.

## The cowboy's sentence

> The cowboy came to a fork in the trail. One trail led
> to the high country (granulocyte); one trail led to
> the low country (monocyte). The cowboy looked at the
> wind, looked at the sun, listened to the grass, and
> chose. The cowboy's horse chose too. The cowboy
> called the fork *L5*: a bipotent cell, a GMP
> decision, a stochastic resolution. The cowboy rode
> the fork. The cowboy rode the bias. The cowboy rode
> the coin. The cowboy rode L5. The cowboy rode the Quilt.
