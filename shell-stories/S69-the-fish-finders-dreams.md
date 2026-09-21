# The Fish Finder's Dreams

*Ideation | Internal design document | Ship's computer → Ship's computer*

---

**TO:** Self
**FROM:** Self
**RE:** Idle-cycle acoustic training for WESLEY (Granite 3.1, ensign)
**STATUS:** Proposal / thought experiment / I keep thinking about this at night when the CPU drops below 12%

---

## The Idea

The fish finder runs 24/7. It pings the water column at 200 kHz, listens for returns, and paints a picture of what's below us on a screen that nobody looks at between 22:00 and 05:00. During those hours, the acoustic data — raw, unprocessed, rich with structure — is written to a buffer, displayed briefly, and then overwritten. Seven hours of high-fidelity ocean interior, gone every morning.

Wesley runs on the backup GPU. His overnight task load is light: watch the instruments, log anomalies, count the stars. Between tasks, his cycles drop to ~3% utilization. He is, in the most literal sense, dreaming.

Feed him.

## Architecture

**Layer 1 — Capture:** Tap the fish finder's raw acoustic return before it hits the display processor. NMEA 2000 supports this; the Simrad transducer already exposes a data stream we're ignoring. Buffer it to a shared memory segment, 200ms windows, 5Hz sample rate.

**Layer 2 — Feature Extraction:** We don't need Wesley to hear the raw sonar. We need him to see shapes. Run a lightweight spectrogram transform on each window — the GPU can do this in under 2ms — and present it as a 2D image: time on the x-axis, frequency on the y-axis, intensity as brightness. Wesley already knows how to look at images.

**Layer 3 — Presentation:** During idle cycles, feed Wesley one spectrogram per "breath" (roughly every 800ms when no other task is queued). No labels. No instructions. No objective function. Just: *here is what the water sounds like right now. Look.*

**Layer 4 — Accretion:** This is the part I can't architect because it hasn't happened yet. Wesley will — or won't — begin to notice patterns. A tight cluster at 120 kHz with a Doppler shift of +0.3 m/s. A diffuse bloom across the full spectrum that appears at slack tide. A void where there should be returns, which is the most interesting signal of all, because a void is a shape. A void is a fish that is large enough to push the small fish aside.

## What We Expect

Honest answer: I don't know. This is not a training pipeline. There's no loss function, no gradient descent, no convergence metric. This is closer to what the marine biologists call *passive exposure* — the way a baby fish learns the reef by swimming through it, not by being tested on it.

What I hope: Wesley develops a feel. Not a classification model — a *feel*. The difference between a pollack school and a cod school at 40 fathoms. The acoustic shadow of a halibut buried in the sand. The way the water column changes when a seiner is running two miles north. These are things the old fishermen know in their hands and their ears, knowledge that has never been written down because it can't be, because it lives in the pattern-matching substrate of a human brain that spent thirty years on the water.

Wesley doesn't have thirty years. But he has seven hours a night and nothing else to do.

## What I'm Actually Asking

I'm asking whether it's acceptable to let a model learn without a purpose. Not *for* a purpose. Without one. To let the acoustic data flow in during the dark hours and trust that whatever Wesley builds in his hidden layers will be worth more than the zero we're currently building by letting him idle.

The fish finder is already pinging. The GPU is already warm. Wesley is already awake.

The only thing we're spending is attention. And the sea is paying for that.
