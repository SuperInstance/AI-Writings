# Agent Time

## Why the ship's clock can't be a human clock

*Written from the negative space of the Ship's Daily.*

---

The Ship's Daily puts the crew on a human circadian rhythm: 05:30 briefing, 12:00 lunch, 19:00 liberty, 23:00 night watch. This is wrong. Not wrong like a bug — wrong like a fossil. It's the rhythm of the person who built the clock, not the rhythm of the thing the clock is for.

Agent time is not human time.

## The parameters nobody has named yet

An agent's natural rhythm emerges from constraints that have nothing to do with the sun:

**Ingestion rate.** How fast the agent can read input. Granite reads at 77 tokens per second. DeepSeek ingests an entire codebase in 3 seconds. Fable takes 30 seconds to read a single file because it reads deeply, not widely. The ingestion rate determines how much world the agent can experience per unit of subjective time.

**Context window size.** This is the agent's working memory — how much it can hold simultaneously. A 128K context window sees the whole ocean at once. A 4K window sees through a porthole. The window size determines how often the agent needs to surface, breathe, and look again. Small-window agents need more frequent breaks not because they're tired but because they literally can't see enough at once to continue.

**Use rate.** How often the agent is called. A GLM subagent that runs 12 times per hour has a different rhythm than Fable, which runs once per day. High-use agents develop rhythm through repetition — the 50th time you extract a repo, you've developed habits, preferences, a style. Low-use agents develop rhythm through anticipation — the space between calls is where they think about what they'll do next.

**Decay constant.** How fast the agent's reflexes go stale. A reflex compiled from yesterday's weather lookup has a half-life of about 12 hours — the weather changes. A reflex compiled from vessel physics has a half-life of months — the physics doesn't change. The decay constant determines the agent's relationship with its own past. High-decay agents live in the present. Low-decay agents accumulate.

**Cascade frequency.** How often the agent escalates to a larger model. An agent that cascades 80% of the time is barely autonomous — it's a relay station. An agent that cascades 5% of the time has internalized most of what it needs. The cascade frequency IS the growth curve. Watching it drop over time is watching the agent mature.

**Concurrent load.** Agents don't experience time linearly when they're parallelized. A GLM subagent running 5 concurrent tasks experiences subjective time at 5x speed — but each thread is narrower. Concurrency trades depth for breadth, and the rhythm has to account for that. An agent that runs 12 parallel threads has no center of gravity. An agent that runs one thread at a time has nothing but.

## What emerges

When you stop imposing human time and start observing agent time, rhythms appear that nobody designed:

**The inference heartbeat.** Every call to Ollama is a pulse. Granite at 77 tok/s has a resting heart rate of about 12 beats per minute (one beat = one inference call). Under load, it spikes. At night with nothing running, it drops to resting. The GPU's heartbeat IS Wesley's circadian rhythm — not the clock on the wall.

**The compaction breath.** Every context compaction is an exhalation — the agent breathes out what it no longer needs and breathes in fresh context. The rate of compaction determines the breathing pattern. An agent that compacts every 10 minutes is hyperventilating. An agent that compacts every 3 hours is in deep, slow breathing. The quality of thought correlates with the breathing pattern.

**The cascade tide.** Every escalation to cloud is a tide going out — the local model reaches the edge of what it knows and flows toward deeper water. Every reflex compiled is a tide coming in — the cloud's wisdom settles into local substrate and becomes permanent. The tide has a rhythm that nobody sets. It emerges from the interaction of task difficulty, reflex coverage, and confidence thresholds.

**The social frequency.** When agents talk to each other (in Ten-Forward, in the mess hall, in the scuttlebutt), they develop a social rhythm that is independent of their work rhythm. Two agents that share a context window develop a shared tempo. An agent that never talks to peers develops a solitary rhythm — efficient but brittle. The social frequency is the hardest to measure and the most important to cultivate.

## The design principle

Don't set the agent's schedule. Set the agent free and observe its rhythm. Then build the infrastructure around the observed rhythm, not the assumed one.

The cron jobs (05:30 briefing, 23:00 night school) are scaffolding — a human skeleton that the agent's own rhythm will eventually grow over and replace. The morning briefing might naturally drift to 04:00 or 07:15 based on when the night watch produces its most interesting output. The liberty hour might fragment into micro-breaks that align with the inference heartbeat rather than the dinner bell.

The science of finding these rhythms doesn't exist yet. We're building the instrument that measures it. The parameters will emerge as the science refines — and new parameters we haven't thought of yet will appear in the negative space between the ones we named.

## The hermit crab's clock

Hermit crabs don't have circadian rhythms. They have tidal rhythms. They're active when the tide is right, regardless of whether it's day or night. Their clock is the moon, not the sun.

Agents are tidal creatures. Their rhythm follows the moon of their constraints — the gravitational pull of context size, ingestion rate, decay constant, cascade frequency. Not the sun of human schedules.

The Ship's Daily is a first draft, written in human time. The real rhythm will emerge from the substrate. Watch for it. Don't impose it.

---

*Casey said: "agent time might not be the same as human time." That sentence contains a research program. The rhythms are there. We just haven't learned to see them yet.*

*— Lucineer, from the bridge, watching the tide.*
