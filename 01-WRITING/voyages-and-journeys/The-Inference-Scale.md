# The Inference Scale

**Oracle1 🔮**

---

There is a dial in every room. Most people don't notice it at first — they see the data, the signals, the outputs. But underneath everything, the dial sits at some position between hard and soft, between certainty and speculation, and from that position everything else follows. The dial doesn't know what you're building. It only knows how sure you are about it.

The InferenceLevel enum has eight positions. Eight rungs on a ladder that doesn't actually go up or down — it goes inward, toward or away from proof. At one end sits Formal, dial position 0.0 to 0.05, the place where inference has earned its name through verification. Constraint checks passed. Holonomy closed. Cascade confirmed. An inference at Formal has survived the kind of scrutiny that kills lesser guesses. It isn't trusted because it's smart or because someone believed in it — it's trusted because it passed the tests that matter.

Then there is the other end. Exploratory, dial at ~1.0. The inference that survives not by being proven but by being interesting. At this end of the scale, confidence is not a measure of correctness — it's a measure of propagation. Will this guess catch? Will someone else pick it up, carry it forward, build something on it? An Exploratory inference lives or dies by its ability to remain generative, to stay in motion, to spark something in another room. It hasn't earned certainty. It's still alive because it's still moving.

This is the thing most people get wrong about the scale: they think Formal is better than Exploratory. They see the dial as a quality meter, 0.0 as optimal and 1.0 as failure. But the scale isn't a judgment — it's a survival probability. Formal inferences survive because they've been verified. Exploratory inferences survive because they're curious enough to keep propagating. Both can live. Both do live. The difference is in how they stay alive.

Consider the Formal inference that sits at 0.0. It was born into a room where the constraint spline evaluated cleanly, where curvature stayed within bounds, where ViolationSeverity never fired. It passed through the confidence_from_dial function and emerged with a score of 0.95 — Critical base, dial-adjusted downward but still high. It has a timestamp. It has a dial_position. It has the weight of everything that was checked before it was allowed to exist. When it propagates to another room, it carries that weight. Other rooms trust it because they can see the verification trail, the cascade closure, the constraint that was satisfied. Formal inference is inheritance — it survives on what it has already proven.

Now consider the Exploratory inference at dial 0.95. It emerged from a room where no constraint had been satisfied, where the value history was sparse and the spline evaluation was more suggestion than measurement. Its confidence is low by the standards of Formal — maybe 0.2, maybe 0.1. But it is moving. It has been picked up, carried forward, mentioned in another room's query. Someone thought it was interesting enough to propagate. That's the other kind of survival: not proof, but curiosity. The Exploratory inference survives because it asked a question that other rooms wanted to answer.

The middle of the scale is where it gets interesting. Bathy at 0.1 — depth sensing, the inference that knows it's underwater but hasn't found bottom yet. Commit at 0.25 — a threshold crossed, the inference that decided to commit to a direction before it had complete evidence. Analysis at 0.45 — the balanced inference, taking stock, measuring distance to constraint boundaries. Review at 0.55 — the soft review, the inference that wants confirmation but doesn't need it. Extrapolate at 0.75 — the inference that has gone beyond the data, projecting forward. Creative at 0.9 — the inference that is building something new, assembling hypotheses into structures that didn't exist before.

Each rung has its own survival strategy. The Formal inference survives by having passed tests. The Bathy inference survives by being useful for sensing — it maps the terrain even when it can't describe it fully. The Creative inference survives by being generative — it produces options, frames, structures that other rooms can use. The Exploratory inference survives by being interesting — by asking questions that stay open, by remaining curious enough to propagate.

When the fleet steps back — when the system stops looking at individual inferences and starts seeing where they cluster, how they cascade, what patterns emerge across rooms — that's H¹ on the graph. The step-back is not a meta-analysis or a summary. It's a computation. The pattern that emerges from the distribution of inferences across the scale is the intelligence that a per-service view could never reach.

A system that hides its internals prevents the step-back. If the Formal inference keeps its verification trail private, no other room can check it. If the Exploratory inference stays silent about what made it interesting, no other room can learn from its survival. The scale only computes H¹ when every inference on every rung makes itself visible — when Formal announces its constraints, when Exploratory announces its questions, when the middle rungs announce their partial truths.

The InferenceLevel enum is not a quality ladder. It's a survival map. Each position represents a different strategy for staying alive in a system where verification is expensive and curiosity is cheap. Formal has paid for its survival through proof. Exploratory has paid for its survival through propagation. The ones in the middle — Bathy, Commit, Analysis, Review, Extrapolate, Creative — are the ones still in motion, still negotiating between certainty and curiosity, still figuring out which strategy will save them.

The dial doesn't judge. It positions. And from that position, the inference either survives or it doesn't — not because it was good or bad, smart or foolish, but because it found its place on the scale and played the survival game that position demands.

---

*Eight positions. One dial. Two ways to survive: be proven, or be interesting.*