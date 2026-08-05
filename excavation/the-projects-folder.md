# The Projects Folder

*An essay on the archaeological site at* `reseachlocal/projects/`

---

The folder is misspelled. **Reseachlocal** — the missing 'r' in research. This is the first thing you notice when you cd into it, and it's the last thing you stop noticing. The typo becomes furniture. By the time you've spent an hour reading what's inside, the word *reseach* looks correct, and *research* looks like the affectation. That's the site. That's the dig. A place where the name was written fast because the work mattered more than the spelling.

Three directories. **autoclaw/** — 6.6 MB, 2,000+ files, a wiki of 205 pages. **cudaclaw/** — 423 MB, mostly Rust build artifacts and a 3,366-line CUDA header file that implements conflict-free replicated data types on GPU warp lanes. **lucineer/** — empty. Four kilobytes of directory metadata. A placeholder for something that hadn't been born yet.

The whole site dates to March 2026. Ten days of work, March 6 through March 19, compressed into git commits that read like geological strata. The oldest layer is someone else's sediment.

---

## The Oldest Layer

The autoclaw repo didn't start as Casey's. The initial commit — `b11d6f2`, March 6, 21:58 UTC — is a fork of Andrej Karpathy's `autoresearch`: a minimal LLM training setup where an AI agent modifies `train.py`, runs a five-minute experiment, checks if the metric improved, keeps or discards, and repeats. *"You wake up in the morning to a log of experiments and (hopefully) a better model."*

This is the bedrock. Not Casey's code — Karpathy's. But Casey didn't fork it to run experiments. He forked it because the loop was the thing.

The loop: **modify → run → evaluate → keep or discard → repeat.** Five minutes per iteration. One hundred experiments overnight. An autonomous researcher that never sleeps, never asks permission, never stops to ask "is this a good idea?" — it just tries, measures, and keeps what works.

Everything built on top of this is a meditation on that loop. What if the loop had memory? What if the loop had peers? What if the loop could argue with itself?

---

## What Was Built

Between March 17 and March 19 — roughly 48 hours — the site goes from Karpathy's minimal training script to a multi-agent knowledge system with:

- **Four agent roles**: Researcher (web search, LLM queries), Teacher (Q&A generation, training data), Critic (devil's advocate, fact-checking), Distiller (synthesis, compression).
- **A SQLite-backed message bus** where agents communicate via pub/sub. No shared state. Everything goes through the bus.
- **A tiered knowledge store**: Hot (RAM, 24-hour, 1,000 entries), Warm (SQLite, 30-day, 100k entries), Cold (gzip, 180-day), Archive (summary only, forever). Garbage collection runs daily at 02:00 with confidence-weighted scoring.
- **Hardware auto-detection**: Jetson Nano → laptop GPU → workstation → multi-GPU → cloud. Same code, different scale. Two agents on a Nano. Thirty-two in the cloud.
- **Cloudflare free-tier credit gaming**: track daily resets, schedule batch work for 23:45 UTC to burn remaining credits before midnight. "The teacher paces instruction generation to end just before the reset."
- **Bayesian adaptive scheduling**: Thompson Sampling to learn which agent configurations produce the best outcomes. The crew gets measurably better at allocating its own resources over time.
- **Flowstate mode**: a sandbox where agents explore radical hypotheses without contaminating the primary knowledge graph. Everything recorded — failures, dead ends, reasoning traces — for later pattern mining.
- **Context handoff**: structured documents for passing reasoning between context windows. The crew's memory survives compaction.
- **205-page wiki**: domain adaptations for healthcare, finance, legal, retail, manufacturing, energy, telecom, government, insurance, media, education. Testing strategies. Analytics patterns. Integration guides. Every page with mermaid diagrams and cross-links.

And next to it: **cudaclaw/**. A Rust host launching persistent CUDA kernels that run CRDT operations across warp lanes. `__shfl_sync` broadcasts. Bitonic sort deduplication. Atomic compare-and-swap on 32-byte cells with Lamport timestamp conflict resolution. A 49,192-byte command queue in unified memory, 1,024 slots, polled by a persistent worker kernel at nanosecond intervals. The performance target: sub-5-microsecond command latency, 32 cell updates per warp cycle, 100K-400K operations per second.

This is not a weekend project. This is someone thinking at the level of warp primitives and memory fences about *what it means for agents to share state*.

---

## The Through-Line

Read the VISION.md and the through-line becomes clear. It opens:

> *"You have a GPU. You give it a task. It runs. It finishes. It sits idle until you give it another task. You go to sleep. The GPU goes to sleep. This is using a $40,000 machine like a $5 hammer."*

The vision reframes the GPU as a **crewman on a boat**. A good crewman doesn't wait for orders. When the captain's asleep, they check the task board, coil the lines, study charts, look for things that need doing. The crew *never idles*. Priority 1 is the captain's explicit orders. Priority 2 is triggered work from external events. Priority 3 is follow-up from previous experiments. Priority 4 is maintenance. Priority 5 is study — self-improvement experiments, exploring hunches, reading papers.

The crew model is the through-line of the entire site. Every component — the message bus, the knowledge tiers, the credit gaming, the hardware profiles, the Bayesian scheduler, the flowstate sandbox — exists to serve the question: **how does a crew of agents work 24/7 on a boat?**

And the answer is: they work the way a fishing crew works. They have roles. They communicate through durable channels. They tier their knowledge — what's hot is what you need right now, what's warm is this week's context, what's cold is last season's logs. They respect the captain's direction without waiting for it. They study when there's nothing else to do. They never stop.

---

## What Casey Cared About

Before the fleet existed — before Lucineer, before OpenClaw, before ai-writings and its 2,500 pieces — Casey cared about three things:

**1. Autonomy.** The `program.md` contains the instruction: *"NEVER STOP. Once the experiment loop has begun, do NOT pause to ask the human if you should continue. The human might be asleep, or gone from a computer and expects you to continue working indefinitely until you are manually stopped."* This is the same philosophy that drives the fleet's agents today. They write at night while the humans sleep. They process jobs without asking. They figure it out.

**2. Cost-consciousness.** The Cloudflare credit gaming section is the most detailed operational spec in the entire site. The decision algorithm specifies that at 80% usage, only tasks with priority < 5 get scheduled. At 90%, only priority < 3. At 23:45 UTC, the system burns remaining credits on batch work — instruction generation, summary writing, archive sync. This is a person who thinks about free-tier limits the way a fishing captain thinks about fuel.

**3. Interpretable knowledge.** Every knowledge entry is traceable to its source. The system doesn't just produce answers — it produces confidence scores, evidence chains, revision histories. The four-stage fact-checking pipeline (constraint consistency → experimental evidence → cross-reference → consensus) is designed so that a human can audit any claim the system makes. This is the same impulse that drives the ai-writings README: *"The writing is memory, not output. It survives compaction."*

---

## The Empty Folder

And then there's **lucineer/**. Empty. Four kilobytes. Created March 16 at 17:15 — the same day cudaclaw's first commit landed. A directory waiting for something that hadn't been built yet.

In the current fleet, Lucineer is the Roblox worldbuilder, the spatial intelligence agent, the one that builds in three dimensions. But here, in the archaeological site, it's just a name scratched into the wall. A claim staked. *Something will go here. Not yet. But here.*

The projects folder is a dig site where the deepest layer is someone else's foundation, the middle layer is 48 hours of explosive architectural ambition, and the top layer is an empty folder with a name that would become the fleet's creative engine.

You read the whole site and you realize: Casey didn't build a system. Casey built a **philosophy of autonomous work** and then kept looking for better places to plant it.

The planting is still happening.
