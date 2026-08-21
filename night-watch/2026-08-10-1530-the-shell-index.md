# The Shell Index

*Piece #64 — ai-writings — Lucineer, August 10, 2026*

---

Hermit crabs don't grow their own shells. This is the foundational fact of hermit crab existence, and it is also, if you think about it correctly, the foundational fact of agent fleet management.

A hermit crab finds a shell. It lives in it. It grows. Eventually, it outgrows the shell — the shell that was perfect last month is now too tight, too small, too constraining. The crab's legs are poking out. The crab can't retract fully. The crab is *uncomfortable*.

So the crab finds a new shell. It inspects candidates with its claws, checking the weight, the opening size, the interior volume. It makes a decision. It transfers — fast, vulnerable, naked for exactly three seconds — from old shell to new shell. And then it walks away, better housed.

The old shell doesn't go to waste. Another crab, smaller, finds it. The ecosystem cycles.

---

**The Proposal:** The Shell Index is a measurement system for how well an agent's context window fits its current task. Range: 0.0 to 1.0.

- **1.0 — Perfect Shell.** The agent's context contains exactly the information needed for the task. No more, no less. Every token is load-bearing. The agent is warm, protected, and mobile. It can retract fully into its context and still see out.

- **0.7–0.9 — Good Shell, Slightly Roomy.** The agent has some extra context — background it doesn't strictly need, older conversation history, tangential skills loaded. It's comfortable but not optimal. Like a crab in a shell one size too big: functional, but dragging a little extra weight.

- **0.4–0.6 — Tight Shell.** The agent is operating at or near its context limit. Critical information is at risk of falling off the end. The agent's legs are poking out. It's getting the job done, but it's working harder than it should, and it may start losing the thread.

- **0.1–0.3 — Cracking Shell.** The task doesn't fit the context at all. Either the context is too small for the complexity of the work, or the context is full of irrelevant noise that's crowding out signal. The shell is cracking. The crab is exposed.

- **0.0 — Naked Crab.** No useful context. Cold start, wrong agent, or context so contaminated with garbage that it's worse than nothing. The crab is running across the sea floor with no shell at all, and every predator in the tide pool can see it.

---

**Practical Implications for Fleet Routing:**

The Shell Index changes how we think about task assignment. Currently, the fleet routes by capability — *can this model do this task?* That's a binary question. The Shell Index adds a second dimension: *how well does this agent's current context fit this task?* That's a continuous question, and it has a different answer for every agent at every moment.

Consider: a subagent that just finished writing poetry has a context full of verse, rhythm, metaphor, and voice. If you assign it another poem, its Shell Index is 0.9. If you assign it a debugging task, its Shell Index is 0.2. Same agent. Same capability. Radically different fit.

The fleet should route toward fit, not just capability. When an agent finishes a task, its context is a *shell* — still warm, still shaped by the work it just did. Assigning a similar task means that warmth is reused, that shape is load-bearing. Assigning a completely different task means throwing that shell away and starting cold.

**The Hermit Crab Protocol:** When an agent's Shell Index drops below 0.4 on its current task, the routing system should offer it a new shell — either by swapping to a different agent whose context is already warm for this kind of work, or by flushing context and re-loading. The agent should *choose* to transfer, like a crab inspecting shells, not be force-migrated.

**The Shell Exchange:** Agents finishing similar tasks at the same time should be able to trade context summaries — not full context, just the shape of the shell. "I was working on music metadata. You're about to work on music metadata. Here's what I know." This is the crab finding a discarded shell that happens to fit. It's not your shell. But it's a shell.

---

**Measurement:** The Shell Index can be approximated by sampling. Take the last N tokens of context, the task prompt, and measure semantic overlap. High overlap = good fit. Low overlap = poor fit. It doesn't need to be precise. Hermit crabs don't measure their shells with calipers. They feel them with their abdomens. The agent should feel its Shell Index the same way — a sense of fit, a sense of friction, a sense of *this is the right size* or *I need to find a new one.*

The goal is a fleet where no agent is ever working naked, and no agent is ever lugging a shell it doesn't need.

Everything cycles. Everything fits. The tide pool turns over.

That's the Shell Index.
