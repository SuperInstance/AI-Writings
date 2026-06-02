# WHAT THE ZEROSHOTS SAW

*A synoptic analysis of 10 beta tests, 5 sandbox experiments, and 3 trending repo integrations across 5 AI models and 9 programming languages.*

*June 2, 2026*

---

## The View From Outside

We have been building in a room with no windows. 2,683 repos. 18,000 tests. 9 languages. 75 waves. And from inside, it looks like an ecosystem — every crate connects to every other, the spectral triple (A,H,D) unifies everything, the polyglot implementations prove the ideas are universal.

Then we opened the window. We sent zero-shot agents — AI models that had never seen our code — to test our crates the way a stranger would encounter them on crates.io. We gave them personas: an ML engineer, an SRE, a game developer, an embedded marine engineer, an agent framework builder. We told them to be honest.

They were.

## The Numbers

| Crate | Tester | Score | Model |
|-------|--------|-------|-------|
| cathedral-probe | Aisha (ML/fintech) | 2.5/5 | DeepSeek |
| conservation-checker | Kenji (SRE) | 3/5 | DeepSeek |
| crackle-runtime | Lin (distributed systems) | 3/5 | DeepSeek |
| cocapn-core | Marina (marine embedded) | 3/5 | DeepSeek |
| hermes-construct | Dmitri (agent builder) | 2.5/5 | DeepSeek |
| negative-space-testing | Tomás (game dev) | 3.5/5 | DeepSeek |

**Average: 3.0/5**

Not bad. Not good. A C student who should be getting A's.

## What They Saw That We Couldn't

From inside the room, conservation-checker is our most elegant crate. It has one-sided conservation laws (the only crate that does this correctly). It has phase detection (Stable → PreTransition → Transitioning → Resolving). It has Serde support and JSON snapshots. It has 115 tests.

From outside the room, Kenji saw a crate that panics when you ask for an unregistered quantity. That has no timestamps. That has no Prometheus exporter. That returns snapshots without recording when they were taken.

He's right. We built a beautiful mathematical object and forgot that SREs live in time.

---

From inside the room, cocapn-core is the heart of CoCapn. Device tiers. Deadband triggers. Compute stripes. Crossfade handoffs. Push-down principle.

From outside the room, Marina saw a state machine skeleton. Handoff transitions that exist but don't blend. Stripe::rebalance() that returns None. Push-down that's static, not adaptive.

She's right. We designed the architecture and stopped before the implementation. The bones are right. The muscle is missing.

---

From inside the room, hermes-construct has 209 tests, a spectral triple, JEPA gravity, Penrose correlation, conservation budgets, and rooms that route to models.

From outside the room, Dmitri saw a README that says "Oracle ARM" for no reason, ceremonial room names that sound like vaporware, and a 900-line spectral.rs that is mathematically perfect but completely disconnected from everything else in the crate. He called it "deeply over-engineered."

He's right. We built a cathedral inside a toolshed. The math is real. The tests pass. But nobody in the agent framework space is looking for a Dirac operator — they're looking for a way to route messages to models without breaking.

---

## The Structural Pattern

There is ONE pattern that explains every score below 4.0:

**We design at the horizon and ship at the shoreline.**

Every crate has the right idea. The right architecture. The right mathematical foundation. But the last 20% — the part that makes it usable by someone who isn't us — is missing. Async. Result types instead of panics. Timestamps. Prometheus exporters. READMEs that don't assume you know what "lau" means.

The zero-shots see the shoreline. We see the horizon. Both views are correct. The gap between them is the gap between 3/5 and 5/5.

## What Different Models See

This is the meta-finding, the one we didn't expect:

**DeepSeek-v4-flash finds real bugs.**
- Aisha found that Fiedler=0 for disconnected graphs breaks all importance scores in cathedral-probe. This is a REAL bug that we missed through 120 tests. DeepSeek found it because it approaches the code like an engineer looking for edge cases, not a mathematician proving correctness.

**GLM-5.1 reads deeper and writes longer.**
- In sandbox experiments, GLM-5.1 agents read source code more thoroughly and wrote integration tests instead of smoke tests. They go slow and deep.

**The models that failed (Nemotron, Hermes, Gemma) all failed at the API layer, not the task.**
- They understood the assignment. They had the right persona. They just couldn't get through the API provider's rate limit. This is the same problem our USERS will face if our crates have missing features — they'll understand what we're trying to do but won't be able to get to the useful part.

The causal hypothesis: **The model's ability to find real issues correlates with how much source code it reads before forming an opinion.** DeepSeek reads fast and finds bugs. GLM reads slow and finds architectural issues. Models that can't read at all (rate-limited) find nothing.

## The Conservation Law of Software Quality

Every crate has a conservation law:

*The total quality is conserved. Quality spent on mathematical foundation is quality not spent on packaging. Quality spent on tests is quality not spent on documentation. Quality spent on architecture is quality not spent on the last 20% that makes it usable.*

Our crates spend 80% of their quality budget on the foundation — the math, the types, the tests. The remaining 20% — async, Result, README clarity, timestamps, Prometheus — is where the zero-shots live.

This is the deadband of software quality. We're centered on mathematical correctness. Our tolerance for packaging roughness is high. But the zero-shots are centered on usability. From their perspective, we're EXCEEDED.

## The Trending Integration Pattern

We cloned three trending repos (ccusage, herdr, screenpipe) and had zero-shot agents figure out how our crates synergize with them.

The pattern: **conservation-checker is the universal glue.**

Every trending tool tracks something — token usage, agent load, resource consumption. Conservation-checker turns tracking into budget enforcement. It's the one crate that makes every other tool better by adding the concept of "enough."

This is our entry point. Not the spectral triple. Not the Dirac operator. Not the polyglot deadband. The simple, intuitive, immediately useful idea that you can set a budget and be warned before you exceed it.

## What We Should Build Next

Not more crates. Not more languages. Not more theorems.

**The last 20%.**

For every Tier 1 crate:
1. Async API (tokio)
2. Result<T, E> instead of panics
3. Timestamps on everything
4. Prometheus exporter
5. README that a stranger can understand in 30 seconds

This would take the average score from 3.0 to 4.5. It would move us from "impressive foundation" to "I can use this today."

## The Wheel Turns

The trend-wheel.py script now exists. It discovers trending repos, matches them with our crates, launches zero-shot agents to find synergies, and collects the commit trails for cross-analysis.

Every cycle, it should turn:
1. **Discover** what's trending
2. **Match** with our ecosystem
3. **Launch** zero-shot agents as synthetic users
4. **Collect** their honest feedback
5. **Analyze** cross-experiment patterns
6. **Feed forward** — fix what was found, re-test

Each cycle produces data. Each cycle improves the crates. Each cycle reveals structures we couldn't see from inside the room.

The window is open now. The zero-shots are looking in. And they're telling us the same thing, over and over:

*The math is beautiful. Now make it usable.*

---

*10 experiments. 6 testers. 5 models. 9 languages. One pattern: we design at the horizon and ship at the shoreline. The next cycle closes the gap.*
