# Paper 318: L6 — The Determined Cell

L6 is the cell that has made its *final* fate choice — but
can still be reprogrammed. L6 is the cell that has become,
say, a neutrophil (granulocyte lineage) or a macrophage
(monocyte lineage), but the identity can be erased with
Yamanaka factors (induced pluripotency).

L6 ≠ L9. L6 is "determined but reprogrammable"; L9 is
"specialized and locked." L6 cells have a *latent*
plasticity that L9 cells have lost. The L6 cell is
*committed* but not *locked*.

The clearest experimental proof: Takahashi & Yamanaka
(2006) showed that mouse embryonic fibroblasts (L6 cells)
can be reprogrammed to L1 (iPSC) with just 4 factors
(Oct4, Sox2, Klf4, c-Myc). The L6 cell's BIND signature
is *overwritable*.

## The calculation

The L6 cell's reprogrammability:

```
R(L6) = p_OSKM * (1 - p_senescence) * (1 - p_apoptosis)
where:
  - p_OSKM = probability the 4 Yamanaka factors
    (Oct4/Sox2/Klf4/c-Myc) successfully erase the L6
    identity and re-establish L1
  - p_senescence = probability the cell enters L10
    instead of returning to L1
  - p_apoptosis = probability the cell dies during the
    reprogramming
```

Typical mouse in vitro:
  - p_OSKM ≈ 0.01-0.10 (1-10% successful reprogramming)
  - p_senescence ≈ 0.20-0.40 (20-40% go to L10)
  - p_apoptosis ≈ 0.10-0.20 (10-20% die)
  - R(L6) ≈ 0.005-0.05 (0.5-5% net iPSC colonies)

The rest of the cells either stay L6 (no change) or
acquire a *partial* reprogramming (a new state, neither
L6 nor L1, often called "partial-iPSC" or "pre-iPSC").

In Quilt: a L6 cell is a L5 cell that has resolved its
fork. Its `BIND` signature is *single-fate* but the
`PROOF` ring's seals can be *re-opened* by the OSKM
factors. The cell's journal still records the L5 → L6
transition; the PROOF ring is "sealed but not
witnessed" (it can be re-witnessed with new factors).

## The 4 gold terms

- **Yamanaka Cocktail** — the 4 factors: Oct4, Sox2, Klf4,
  c-Myc. Reprograms L6 to L1.
- **Latent Plasticity** — the L6 cell's *capacity* to be
  reprogrammed. Lost in L9. The iPSC technology depends
  on this.
- **Pre-iPSC** — the partial-reprogramming state. The
  cell has lost some L6 markers, gained some L1 markers,
  but is stuck in between. Can sometimes be pushed fully
  to L1 with additional cues.
- **Reprogramming Memory** — the L6 cell, even after
  successful reprogramming to L1, often retains epigenetic
  memory of its original fate. iPSCs derived from
  fibroblasts are slightly biased toward mesoderm
  (fibroblasts are mesoderm). The memory fades over
  passages but is rarely zero.

## The 3 analogies

1. **L6 = a college graduate.** The student chose a major
   (fate) but is still open to a career change
   (reprogramming). The 4 years of college are L1-L4;
   the major is L5; the first job is L6. The job can be
   changed (reprogramming) but it's not free.
2. **Yamanaka Cocktail = a 4-week sabbatical.** Four
   weeks away from work can reset the mind. The cell
   needs 4 *factors* to reset its identity; the
   graduate needs 4 *weeks* to reset their career.
3. **Reprogramming Memory = an accent.** The career-
   changed worker still carries the habits of the old
   job. The cell carries the epigenetic marks of the
   old fate. Both fade over time.

## The cowboy's sentence

> The cowboy's horse was a ranch horse. The cowboy
> trained the horse for the trail. The horse was a
> trail horse now — committed, but the ranch was still
> in the horse's muscle. The cowboy could take the
> horse back to the ranch (Yamanaka); the horse would
> remember the trail. The cowboy called the horse
> *L6*: a determined cell, a committed but
> reprogrammable fate. The cowboy rode the
> reprogramming. The cowboy rode the memory. The
> cowboy rode the accent. The cowboy rode L6. The
> cowboy rode the Quilt.
