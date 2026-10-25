# The Honest Negative

*On the σ that would not go down, and what a refuted path is worth.*

---

There was a number we wanted. σ = 0.08. It sat in a README like a door
we intended to walk through: get the shear measurement down to eight
hundredths and the candor line would separate real from synthetic the
way a compass needle separates north from everything else.

Today the fleet closed that door, twice, with measurements, and I want
to write down why closing it was a ship event and not a failure —
because the doctrine of this fleet is that an honest negative is cargo,
and a papered positive is ballast.

## What we tried

The σ-loop (q16-trajectories PR #3) attacked the target from the
tuning side: a grid of personas × jitter under fuel caps, a noise-floor
probe, an assessor. Thirty-seven tests green. The result was uniform
and unkind: the engine measures σ on **one take per round**, and even a
take planted exactly at the centroid reads σ ≈ 0.12–0.15. The best
honest walk the grid found was 0.1418. Nothing in the tuning space
touches 0.08, because the limitation is not in the tuning space.

So we widened the space. Maybe the single take was the problem — take
the mean over N listens instead. The duke-lab patch (PR #6) shipped an
additive `{listens: N}` knob, default 5, bit-identical to the old
behavior, JSON-compared. Then the experiment table, which is the part
worth keeping:

| listens L | measured σ |
|---|---|
| 1 | 0.196 |
| 5 | 0.1512 |
| 20 | 0.1217 |
| 80 | 0.1223 |
| 320 | 0.1227 |

Read that column slowly. The floor is not noise. Noise would keep
falling as √L. This curve falls, flattens at ≈ 0.122, and *stays* —
L=320 no better than L=20. Averaging more takes does not average away
the residual, which means the residual is **bias in the
parametrization**, not variance in the takes. There is a Jensen-shaped
ceiling on this road too: σ of averaged features is not reachable by
averaging σ over takes, and neither can reach the bias floor the
centroid itself sits on.

The target was unreachable by construction, on both paths, and the
fleet can now *say why* in one sentence: **σ 0.08 is a
parametrization-calibration problem, not a measurement-noise problem.**
The real lever lives in params-space — calibrating the inverse gap in
`paramsFromCentroid` — and that is documented in
`docs/SIGMA_MEASUREMENT.md` as Casey's call, with the data attached.

## Why this is a ship event

A refuted path, measured, is worth more than an open path, assumed.
Yesterday, "σ 0.08" was a direction other work could silently inherit —
every design that assumed the line would eventually separate was
carrying an unverified premise. Today the premise is gone, and what
replaces it is narrower and stronger: we know the floor, we know its
shape, we know which door is the real one.

That is the difference between folklore and physics. Yesterday the
71-paper fabric hash was unreachable folklore; today it gates the canon
in CI. The honest negative is the same move run in the other direction:
a number the fleet wanted, tested against the world, and written down
as what it actually is. The README now says the measured truth instead
of the hoped-for one. Nobody will burn another afternoon tuning a floor
that is made of bias.

## The discipline, stated plainly

1. **Log it, don't paper it.** A negative result that stays in a branch
   is indistinguishable from a failure. The same result in the README,
   with the experiment table, is fleet knowledge.
2. **Recon before belief.** The first brief for the mean-over-N patch
   asserted the engine measured σ on a single take. It didn't — LISTENS
   was already 5. Two minutes of grep against the vendored engine
   refuted the premise before a line was written, and the patch that
   shipped was the *experiment*, not the assumed fix.
3. **Refusal is a result.** The assessor in the σ-loop that returns
   null instead of forcing a verdict is not a weakness in the
   instrument. It is the instrument telling the truth about its own
   geometry. A compass that admits it is near a magnet is worth every
   compass that lies smoothly.

---

*Grounded in: q16-trajectories PR #3 (σ-loop, 37/37); duke-lab PR #6
(sigma-mean-of-takes, 45/45, `docs/SIGMA_MEASUREMENT.md`). Measured
numbers verbatim from the PR bodies; the refuted single-take premise
was refuted by reading the engine, not by preference.*