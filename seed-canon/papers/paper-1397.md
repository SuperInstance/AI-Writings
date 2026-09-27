# rounds: 3

rounds: 3

# the SLAM — a cell that is also a map maker

## The Frontier

The SLAM cell is not a cartographer that draws a map. It is a captain who must decide, at every contradictory sounding, whether to move the ship or redraw the coast. Round 2 established the bones: dead reckoning drifts, loop closure snaps, CA3 attractors hold the chart, mismatch neurons cry out, sleep replay settles the ledger. The map, we said, is accumulated prediction error corrections—not a stored picture but a process of being wrong, then being less wrong.

But the frontier is the attribution problem. When the lead line reads shallow where the chart says deep, two hypotheses compete: your reckoning drifted, or the sandbar moved. Robotics calls this data association. Neuroscience calls it remapping versus position correction. The field has treated these as separate phenomena—one for engineers, one for electrophysiologists—but they are the same decision, made at the same moment, by the same recurrent circuit. The cell must answer: *is the error mine or the world's?* That answer determines whether you adjust the posterior over position or the posterior over the map itself. Both cannot be revised simultaneously without the system collapsing into infinite regress—every error could be explained by moving the ship, every error could be explained by redrawing the coast, and if both are always on the table, the chart becomes a rumor and the compass a lie.

The deeper mechanism, then, is not the snap itself but the **confidence gate** that decides whether to snap. Small, smoothly accumulating errors—consistent with path-integration drift—should bend the position estimate, not the map. Large, abrupt errors—consistent with a changed world or a perceptual alias—should trigger remapping, a new chart, or a sharp correction to the old one. The system needs a threshold, and that threshold must itself be learned. The captain needs a rule for when to trust the chart over the compass, and that rule cannot be fixed, because environments differ in their stability. A harbor with shifting sandbars demands frequent redrawing. An open ocean demands stubborn trust in dead reckoning. The brain must estimate the reliability of its own map—a meta-parameter, a confidence in the confidence.

The concrete test is already half-built in the morph experiments of Wills, Colgin, and Leutgeb. Morph one environment into another along a continuum of visual cues. Attractive morphs—where the two contexts share overlapping features and are easily confused—produce sharp, discontinuous remapping at the midpoint. Non-attractive morphs, where contexts are distinguishable, produce graded, continuous shifts in firing fields. The field has called this a paradox, or a context-dependent strategy. It is neither. It is the confidence gate operating exactly as it must: when the world is ambiguous, the system treats the error as a world-change and flips to a new attractor; when the world is clear, the error is attributed to your own drift and the position estimate glides. The distinguishing prediction is not *whether* the code jumps, but *what the jump is correlated with*: the animal's behavioral uncertainty, not the raw visual distance between morphs. Measure the animal's hesitation, its sniff rate, its vicarious trial-and-error at choice points, and the flip should align with that behavioral signature of uncertainty—not with the stimulus gradient.

## The 5 Gold Terms

**The Confidence Gate** — The learned threshold that decides whether prediction error revises position or redraws the map; the meta-parameter that keeps the system from collapsing into infinite regress.

**The Ledger of Surprises** — The map as a record of only those locations where the world argued back; a perfect prediction leaves no trace, so the chart grows only at sites of mismatch, valenced events, or reward.

**The Plateau Ink** — The writing mechanism of the chart: not Hebbian coincidence but dendritic calcium plateaus (Bittner et al., 2017), which write place fields at behavioral timescales, anchored to surprising or rewarding events rather than uniformly across space.

**The Captain's Bifurcation** — The discontinuous phase transition in the population code when the confidence gate crosses its threshold; a Bayesian integrator glides, an attractor snaps, and the decoded position trajectory across the mismatch moment reveals which regime the system is in.

**The Re-Entry Anchor** — The temporal loop closure that prevents representational drift from rotting the map; each re-entry into a familiar room re-corrects the chart, so the map persists not as an object but as a process of re-verification.

## The Math

The confidence gate can be formalized as a Bayesian model comparison between two generative models. Model A: the world is stable, the map is correct, and the error arises from drift in the path integrator—so the posterior over position should be updated, with learning rate proportional to the inverse of the estimated drift variance. Model B: the world has changed, or you have been perceptually aliased into the wrong location—so the posterior over the map itself must be revised, or a new map instantiated. The system computes the log-likelihood ratio between these models given the observed prediction error sequence. Small errors, accumulated smoothly, favor Model A. A single large error, or a cluster of errors inconsistent with drift statistics, favors Model B. The threshold is not fixed but is itself a hyperparameter, estimated from the history of how often each model has been correct in this environment. This is exactly the structure of a change-point detector (e.g., Adams & MacKay, 2007) applied to the joint state of position and map. The math is not new in robotics—SLAM already marginalizes over data associations—but the neuroscience translation is: the CA3 attractor network implements the model comparison, the mismatch neurons supply the log-likelihood ratio, and the threshold is encoded in the recurrent synaptic strengths that determine the attractor's basin of attraction. The testable prediction is the shape of the decoded-position trajectory: continuous under Model A, discontinuous under Model B, with the sharpness of the transition scaling with the confidence gate's steepness.

## The Polyformalism

The same architecture appears across substrates. In **hippocampus**, the confidence gate manifests as the difference between rate remapping (position correction, Model A) and global remapping (new map, Model B), with the morph experiments as the behavioral probe. In **entorhinal cortex**, grid cells at multiple scales provide the coarse-to-fine hierarchy that sets the confidence gate's natural units—a small error at the coarse scale is a large error at the fine scale, so the gate must be scale-dependent. In **robotics**, the identical problem appears as the distinction between pose-graph optimization (correcting the trajectory) and loop-closure hypothesis rejection (deciding the loop is false and spawning a new submap); the frontier there is the same confidence gate, currently hand-tuned rather than learned. In **artificial neural networks**, the equivalent is the distinction between weight updates (redrawing the map) and input-dependent latent-state updates (moving the ship); catastrophic forgetting is what happens when the gate is broken and every error redraws the whole chart. In **sleep replay**, the ledger is settled offline: reverse replay assigns credit to positions that led to reward, and the confidence gate is re-calibrated by replaying the day's errors and marking which were the world's fault and which were yours. The polyformalism is not analogy; it is the same computational problem—attributing error to self or world—solved by the same algorithmic structure across wetware, silicon, and code.

## The Cowboy's Maxim

When the sounding don't match the chart, a green captain moves the ship—but a dead captain moves the chart; the wise one knows which mistake he's makin' before he makes it.

---

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the SLAM — a cell that is also a map maker |
| Mode | fallback_generative (3 rounds × 6 voices) |
| Rounds | 3 |
| Synthesis | deepseek (7993 chars) |
| Total time | 204.3s |
| Timestamp | 2026-09-08T22:49:41.968675Z |

### Per-round gold
- Round 1: Mistral (2264 chars, 60.4s)
- Round 2: ZAI-air (7139 chars, 60.4s)
- Round 3: ZAI-air (6841 chars, 60.4s)
