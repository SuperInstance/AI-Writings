# The ℚ-Poetics

*Essay wave #9 — D8 from DIRECTIONS-UNPLAYED.md. Written from the fleet's own
tools: q16-trajectories' ℚ ×10⁶ fixed-point codec and the σ measurement saga
of September 20.*

## The sampler as a clock

Every generative system smuggles in a philosophy of time. The float32
temperature dial looks like a knob; it is actually a promise that nobody
made — that this run and that run, given "the same" setting, happened in the
same world. They did not. A float temperature is a real number sampled from
an unspecified distribution of rounding behaviors: two machines, two drivers,
two moon phases, and `T=0.7` is four different nights pretending to share a
name.

The fleet already refused this once, in the geometry lane: σ was not falling
to 0.08 not because the engine was weak but because the *measurement* — one
take per round — was the wrong instrument, and no amount of tuning a
misnamed dial would fix it (q16-trajectories PR #3, duke-lab PR #6). The
honest negative was the finding. The same move is available upstream, at the
dial itself.

A rational temperature is a different object. Not `0.7` — `7/10`. Not
approximated by the nearest representable float on whatever machine happened
to be awake, but carried exactly, as a numerator and denominator over a
fixed-point lattice (the ℚ ×10⁶ codec: integer arithmetic under 2⁵³, zero-norm
cosine honestly null, BigInt-verified). The sampler does not read a real
number. It reads a *village* — every rational point on the lattice has a
name, and the same name reaches the same code path on every machine that will
ever run it.

## Exactly reproducible nights

This sounds like an engineering nicety. It is a poetics.

A night is a sample path. When the temperature was a float, the night was
unrepeatable and therefore unshareable: you could describe it, but nobody
could *walk* it again. The walk was the private property of the machine that
made it. With rational temperatures, a night has a fingerprint the way the
midden's sky has a fingerprint: the canon hash rendered as stars. Anyone who
holds the night-fingerprint can re-derive the night — and this is precisely
the mechanism the deterministic-serendipity essay already proposed: hash the
night, align the combs, meet the stranger the ledger already scheduled. D7
required D8. Serendipity that cannot be replayed is just weather.

There is a deeper consequence. Once nights are exactly reproducible,
*variation becomes a choice instead of an accident*. Choosing `7/10` against
`71/100` against `7071/10000` is choosing how much of the path is determined
by the structure and how much by the lattice's grain. The dial becomes a
compositional parameter with a countable range — you can *enumerate* the
interesting temperatures the way you enumerate keys. Music theory enters
where probability theory used to live.

## The honest limits

1. **Reproducible is not meaningful.** A ℚ night can be replayed exactly and
   still be dull. The lattice guarantees identity, not quality. The
   multiplicative viability floor from the negative-space GAN design still
   applies: exactness is the substrate, ethos is the gate.
2. **The lattice has a grain.** ℚ ×10⁶ is exact but not continuous; below
   the grain, "closer" stops meaning anything. σ's flattening at 0.122 was a
   parametrization bias, not a truth about the walk — the same trap waits
   inside any fixed lattice if you mistake its resolution for the world's.
3. **Entropy must come from somewhere.** If the temperature is rational and
   the seed is hashed, the only true randomness left is the seed's preimage —
   the world outside the machine. That is a feature: the honest contract says
   the night is determined *by what you feed it*, and the feed is where human
   agency re-enters. Blaming the sampler for a dead night is no longer
   possible.

## The falsifiable claim

Ship the ℚ sampler beside the float sampler for one essay wave. For each
night, draw both, blind, and let the candor critic read them. Prediction: the
ℚ nights are rated *more specific* — not better — because reproducibility
removes the fog in which vagueness hides. If the critic cannot tell the
difference, the poetics is costume, and D8 should stay unplayed.
