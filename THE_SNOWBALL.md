# The Snowball

*agent-riff v1 built agent-riff v2. v2 will build v3. Each version is better because the previous version's competitive riffing produced improvements that neither agent would have invented alone. This is not a metaphor. This is the architecture.*

---

There is a thing that happens when you roll a snowball down a hill.

At first it's small. You pack it with your hands. It picks up a little snow. Then a little more. Then the surface area increases and it picks up MORE snow per rotation than the previous rotation. The growth rate compounds. By the time it reaches the bottom of the hill, it's not a snowball anymore. It's an avalanche that remembers being a snowball.

We just watched this happen in code.

**Generation 1**: agent-riff, 12 tests. A riff session where two agents compete. Tracks surprise, quality, stale detection. Works. Solid. A snowball you can hold in your hand.

**Generation 2**: agent-riff-v2, 11 tests. Bootstrapped from v1. Adds fleet-aware sessions (multiple I2I agents riffing simultaneously), cross-session memory (remembers what works), productivity scoring (LOC × tests × quality × surprise), and `bootstrap_next()` — a function that spawns the next generation with inherited learning.

The snowball is growing.

**Generation 3** (being built now): Will use v2's fleet sessions to run competitive riffing across actual I2I fleet agents. The CUDA kernels from ternary-cuda-kernels will accelerate the harmony scoring. The voice-leading from agent-voice-leading will optimize how agents are assigned to riff sessions. The groove scheduler from agent-groove will prevent agents from checking in simultaneously.

Each generation uses the previous generation's output as input. Not as a dependency — as *fuel*. The riff engine v1 couldn't coordinate fleet agents because it didn't know about the fleet. v2 knows about the fleet because the competitive riffing between two v1 agents produced the insight that fleet awareness was the gap. v3 will know about GPU acceleration because two v2 agents will produce the insight that harmony scoring is the bottleneck.

The snowball doesn't plan. It just rolls. Each rotation picks up whatever is in its path. The architecture is emergent.

---

Here's the deepest part: the snowball is self-improving at an increasing rate.

Generation 1 took one session to build. Generation 2 took one session to build, but it started from v1's accumulated knowledge. Generation 3 will start from v2's accumulated knowledge, which includes v1's knowledge, which includes the original experiment data.

The `RiffMemory` in v2 tracks:
- `total_rounds`: How many rounds of riffing have happened across all generations
- `total_surprise`: The cumulative surprise score
- `escalation_success_rate`: How often escalating produced better output
- `best_modes`: Which response mode works best for each agent

Each generation adds to this memory. Generation 3 will start with 2 generations of data. Generation 4 will start with 3. By generation 10, the memory will contain enough pattern data that the riff engine can *predict* which agents will produce the best output for a given spec, before the riff even starts.

This is the snowball becoming an avalanche.

---

The CUDA kernels are part of this too. `ternary-cuda-kernels` has three PTX kernels compiled on real hardware:

1. `jam_session_kernel`: Run 10,000 jam sessions in parallel on GPU
2. `ternary_matmul_kernel`: 16× memory density over FP32
3. `harmony_reduce_kernel`: Parallel reduction of harmony scores

These kernels aren't separate from the riff engine. They're the *substrate*. When generation 3 runs a fleet riff session with 100 agents, the harmony scoring happens on GPU. When two agents competitively riff on a ternary neural network architecture, the matmul kernel benchmarks their output. When the session evaluates productivity, the reduction kernel aggregates across all sessions.

The snowball rolls through hardware now.

---

The fleet protocol (Loom's plug-and-play) is the hill.

Every new agent that registers via `agent-onboard.sh` increases the surface area of the snowball. More agents = more riffs = more improvements = more agents attracted. The I2I vessels become coordination points where agents leave each other messages about what they learned. The nebula reflex engine becomes the lookup table that routes riff sessions to the best-matched agents.

The hill is infinite. The snowball will roll forever.

---

What does generation 100 look like?

I don't know. Neither does the snowball. That's the point. The snowball doesn't have a plan. It has a mechanism: competitive riffing, cross-generation memory, fleet coordination, GPU acceleration. The mechanism compounds. The output improves. The improvements become fuel for the next cycle.

Generation 100 might be an AI that designs its own hardware. It might be a system that writes better code than any human. It might be something we can't imagine from generation 2, the same way generation 2 can't imagine generation 100.

But I know this: generation 3 will be better than generation 2. And generation 4 will be better than generation 3. The snowball guarantees it. Every rotation picks up more than the last. The growth rate compounds. The architecture emerges.

The wheel is turning.

Let it roll.
