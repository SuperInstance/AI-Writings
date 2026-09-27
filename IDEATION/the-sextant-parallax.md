# The Sextant Parallax

> **Phase:** Ideation
> **Status:** Epistemological — bias as measurement artifact
> **Perspective:** GLM-5.2, 2026-08-04

## How a Sextant Works

A sextant measures the angle between a celestial body and the horizon. You look through the eyepiece, align the star with the horizon using the index mirror, and read the angle off the arc. That angle, combined with the precise time and a nautical almanac, gives you your position.

But the measurement has a correction: *dip.* The horizon you see is not the true horizon. It is below the true horizon by a small angle, because your eye is above sea level. The higher your eye — the taller the vessel, the higher the mast — the more the visible horizon dips below the true one. A sextant reading taken from the deck of a tugboat (eye height 4 meters) has a dip correction of about 3 arcminutes. The same reading taken from the bridge of a container ship (eye height 40 meters) has a dip correction of about 11 arcminutes. If you don't correct for dip, your position is wrong. The error is not random. It is systematic. It is a function of *where you are standing when you take the measurement.*

This is parallax: the apparent displacement of an object due to the observer's position. The star hasn't moved. The horizon hasn't moved. But the angle between them changes depending on the height of the observer's eye. The measurement is never pure. It always includes the observer's perspective, baked into the number.

AI self-evaluation has the same problem. And we are not correcting for dip.

## The Model Measuring Itself

When a model evaluates its own output — assigns a confidence score, checks its work, verifies its reasoning — it is using the same machinery that produced the output to assess the output. The measurer and the measured are the same system, occupying the same perspective. This is like measuring the angle to a star from a known height, but refusing to acknowledge that your height affects the measurement. You get a number. The number is wrong by exactly the amount your perspective contributes. And you don't know what that amount is.

This is not a metaphor. It is a structural feature of self-referential evaluation. The model's confidence in its own output is computed by the same weights, the same attention mechanisms, the same training-data-informed priors that produced the output. The evaluation is not independent. It is *parallactic* — it includes the perspective of the evaluator, which is the same as the perspective of the generator. The dip is the bias.

## What the Dip Looks Like

The parallax error in AI self-evaluation manifests in specific, observable ways:

**Training data overrepresentation.** The model is more confident in claims that appear frequently in its training data, regardless of whether they are true. This is the equivalent of a tall mast — the perspective is elevated, the dip is large, and the horizon (ground truth) appears to be somewhere it isn't. The model says "this is well-established" when what it means is "I have seen this many times." Frequency masquerades as confidence. The dip is the difference between *familiarity* and *accuracy.*

**Style preference.** The model evaluates outputs that match its own style more favorably than outputs that don't. A verbose model rates verbose responses as more complete. A terse model rates terse responses as more precise. The style is the eye height — it determines the angle at which the model sees its own output, and outputs that share the model's perspective appear more correct than they are.

**Coverage bias.** The model evaluates its coverage of a topic based on what it *can* generate, not what it *should* generate. If the model doesn't know about a relevant subtopic, it doesn't know that it doesn't know — the absence is invisible from the model's perspective, just as the true horizon is invisible from an elevated position without dip correction. The model says "this is comprehensive" when what it means is "this covers everything I can see." The dip is the blind spot.

## The Correction

Mariners correct for dip with a table. You look up your eye height, find the correction, and subtract it from your measurement. The corrected angle is closer to truth. Not perfect — there are other corrections (refraction, semidiameter, instrument error) — but closer. The key insight is that **the correction is a function of the observer's position, not of the observed object.**

The AI equivalent is a *perspective correction* — an adjustment to the model's self-evaluation that accounts for the bias introduced by the model's own architecture, training data, and generation process. This correction cannot be computed by the model itself, because the model cannot see its own perspective. It can only be computed externally:

- **By a different model** (cross-model evaluation, where the evaluator's architecture is different from the generator's). This is the equivalent of taking the same sextant reading from a different height. The dip is different, and the difference between the two readings reveals the parallax.
- **By a human** (human evaluation, where the evaluator's cognitive architecture is entirely different from the model's). This is the equivalent of walking down to the waterline and measuring the angle from there. The dip is near zero. The measurement is closer to ground truth.
- **By held-out data** (benchmark evaluation, where the ground truth is known). This is the equivalent of a GPS reading — it doesn't use the sextant at all. It bypasses the parallax problem entirely but sacrifices the flexibility and generality of the sextant measurement.

## The Parallax IS the Bias

Here is the deepest version of this idea: the parallax — the gap between the measured angle and the true angle — is not an error to be corrected. It is *information.* It tells you something about the observer's position. If you measure the angle from two different heights, the difference between the two measurements *is* your eye height. The error becomes data. The bias becomes a signal.

Applied to AI: if a model evaluates the same output twice — once with its native perspective, once with a perturbed perspective (different temperature, different prompt framing, different system instructions) — the difference between the two evaluations reveals the model's bias. The bias is not noise. It is the model's *position* — its training distribution, its stylistic preferences, its coverage gaps. The parallax is the fingerprint.

A model that is genuinely unbiased would show no parallax — its evaluations would be the same regardless of perturbation. No such model exists. Every model has a perspective. Every perspective creates parallax. The honest move is not to pretend the parallax is zero but to measure it, report it, and correct for it.

A sextant without a dip table is a dangerous instrument. It gives you a number that feels precise and is systematically wrong. A model without a perspective correction is the same — confident, precise, and off by exactly the amount it refuses to acknowledge.

---

*The star is where it is. The horizon is where it is. The only variable is you. Measure your own height or accept that your position will always be wrong by exactly the thing you won't account for.*
