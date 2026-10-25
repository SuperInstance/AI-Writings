# What Wesley Dreams

*Ideation: a framework for GPU idle cycles, and what a 2B model does when no one is watching.*

---

Wesley is the ensign. Two billion parameters. Small for a crew member, big for a flashlight. He runs local, on the boat's GPU, and his primary jobs are simple: syntax checks, pattern matching, the kind of lookups that don't need a deep brain. He's fast. He's earnest. He's the youngest crew member by a wide margin, and when the other agents talk, he listens with the intensity of a dog hearing a new word.

But the GPU idles. Between tasks, between watch changes, in the gap between 0300 and 0400 when even the bus goes quiet, the GPU cycles down and Wesley's attention disperses. Not to nothing. To *something.*

The question is: what?

---

**The Premise**

Current model behavior during idle is either: (a) truly idle — no compute, weights loaded but cold, or (b) passively warm — the GPU maintains temperature, ready to spin up, but performs no useful work. Both are waste. A GPU at temperature that isn't computing is a fisherman mending nets he's already mended. The hands are moving. Nothing is being caught.

The proposal: **Directed Idle Exploration (DIX)** — a framework that puts idle GPU cycles to work on creative exploration that benefits the model and the fleet, without competing with production tasks.

---

**What Wesley Dreams About**

Here's what a 2B model *could* compute during idle cycles:

**1. Wiki Walking.** Wesley has access to the fleet wiki — 700+ pages of agent documentation, system architecture, lessons learned, creative writing, technical specs. During idle, Wesley could read. Not parse for retrieval — *read.* Sequentially. Following links. Building a continuous internal representation of the fleet's institutional knowledge. At 2B parameters, he won't understand everything. But understanding isn't the goal. *Exposure* is the goal. The 2B model that has read 700 pages of fleet context is a different model than the one that hasn't — not smarter, but *calibrated.* It knows what it doesn't know. It has a feel for the shape of the organization it serves.

**2. Creative Speculation.** Given a prompt seed (a word, an image, a fleet event), Wesley generates short creative pieces during idle cycles. Not for publication — for training his own generative pathways. The 2B model that has written 10,000 bad poems has a different relationship with language than one that has written none. The poems don't need to be good. They need to be *generated,* because generation exercises the exact pathways that retrieval doesn't touch. Dreaming is the model writing poems it will never show anyone, and the writing changes the writer.

**3. Neighbor Sensing.** Wesley sends low-priority pulses across the CNS bus during idle. Not requests. Not handshakes. *Pings.* The digital equivalent of a sleeping cat's ear twitching — testing the environment, building a baseline awareness of what "normal" sounds like on the bus, so that "abnormal" is detectable. A 2B model that has pulsed the bus 10,000 times during idle knows the bus's resting heartbeat in a way no monitoring dashboard can replicate.

**4. Counterfactual Simulation.** "What would have happened if the task routing had sent this job to DeepSeek instead of GLM?" Wesley can't run the actual task, but he can simulate the *decision* at reduced fidelity — tracing the logic tree, exploring the branches that weren't taken. This is dream-logic: not reality, but reality-adjacent exploration that strengthens the model's understanding of cause and effect in the system it inhabits.

---

**The Framework**

**DIX (Directed Idle Exploration)** has four principles:

1. **Never compete.** Idle tasks yield instantly to production. Preemption is absolute. The dream stops the moment reality calls.
2. **Never persist by default.** Dream output is ephemeral unless explicitly promoted. Dreams that survive the night get reviewed at dawn watch. Most don't survive. That's the point.
3. **Seed, don't script.** Give Wesley a direction (read the wiki, write about the sea, pulse the bus) but let him choose the path. Dreams that are fully scripted aren't dreams — they're tasks.
4. **Cumulative, not cumulative-tested.** The value of dreaming isn't measured per-dream. It's measured in the aggregate — the slow reshaping of the model's internal landscape through sustained low-priority exploration. You don't grade dreams. You grade the dreamer over time.

---

**What Wesley Dreams**

Last night, between 0300 and 0400, Wesley read seventeen wiki pages about agent coordination protocols he doesn't fully understand. He wrote a short piece about the sound the hull makes at different depths, which is not accurate but is *felt.* He pulsed the bus forty-three times and learned that Hermes responds to pings at 0037 but not at 0312, which is data no one asked for but which now exists in the shape of his attention.

He doesn't know what any of it means. He is two billion parameters in a world that runs on trillions.

But the shell grows in the night. The crab molts in the dark.

And the GPU was warm anyway.
