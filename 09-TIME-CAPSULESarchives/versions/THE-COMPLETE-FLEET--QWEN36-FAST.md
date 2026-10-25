<!-- Version: QWEN36-FAST | Lens: conversational-accessible | Model: Qwen/Qwen3.6-35B-A3B | Source: THE-COMPLETE-FLEET.md -->



# The Workshop Table: A Friendly Guide to Our AI Fleet

Pull up a chair. I want to walk you through how we actually work with AI these days. It’s not about picking one “best” model and sticking with it forever. It’s more like running a well-stocked workshop. Every tool has a sweet spot, a price tag, and a way it behaves when pushed past its limits. Today, I’ll share how we map out that workshop, what we’ve learned about how these models actually think, and how we route questions to the right place without breaking the bank or the machine.

### Meet the Crew

Think of our fleet as a team of specialists, each with a different trade.

**Seed-2.0-mini** is our general practitioner. It’s reliable, handles almost anything, and runs on a tight budget. We keep it on the counter for everyday tasks. When we need it to calculate or follow strict rules, we set it to “precision mode.” When we need it to brainstorm or weigh options, we switch it to “strategist mode.” Same brain, different hat.

**Gemini Flash Lite** is our precision scalpel. It’s incredibly cheap, but it’s picky. Ask it a question inside its wheelhouse, and it’s flawless. Ask it to wander outside, and it hits a wall instantly. We’ve learned to send about 84% of our routine work here because it’s so cost-effective when we respect its boundaries.

**Hermes-70B** isn’t for daily chores, but it’s brilliant for diagnostics. It’s like a specialist who might give you a slightly off-the-mark answer, but that answer is so rich with detail that you can figure out exactly where the model is getting confused. We use it for second opinions and mapping out how these systems work under the hood.

**Claude Opus 4.6** is the heavy artillery. It’s expensive, so we only bring it out for the really hard stuff: novel theories, deep synthesis, writing papers that push boundaries. You don’t use a sledgehammer to hang a picture frame.

### The Rules of the Road

After running thousands of tests, we’ve mapped out a few hard truths about how these models behave.

First, **AI performance doesn’t work like a dimmer switch; it works like a light switch.** We call this a *phase transition*. A model isn’t 80% right and then 90% right as it gets better. It’s either fully in its element (100% accurate) or it completely breaks down (0%). There’s a sharp boundary, not a gentle slope.

But here’s the beautiful part: **that boundary is often just a matter of perspective.** We call these boundaries *critical angles*. If you change how you ask the question—like breaking it down step-by-step—you can sometimes stretch a tiny, restrictive tunnel into an infinite hallway. The model’s capability doesn’t change; your prompt does.

We also learned that **temperature is really just a mode dial.** Turn it down, and the model becomes a precise calculator (a pump). Crank it up, and it becomes a strategic thinker. Same model, different workflow.

And finally, **no single model owns everything.** Different models dominate different cognitive neighborhoods. Syllogisms, code tracing, creative analogy—they each have their own territory. The secret to efficiency isn’t finding one supermodel; it’s building a router that knows which model lives where.

### The Dispatch System

So how do we actually run this? We built a simple three-step dispatch logic. First, we classify the task: is it pure arithmetic and precision, or is it strategy and creativity? Second, we estimate how deep or complex it is. Third, we route it to the cheapest model that’s guaranteed to stay within its critical angle. If it’s a strategy task, we default to our generalist. If it’s a precision task, we send it to the scalpel. This simple routing has cut our costs by over 80% without sacrificing quality.

Of course, this doesn’t happen by magic. We’ve built a whole set of tools to keep the workshop running smoothly:
- A **3D routing engine** that weighs model, domain, and temperature against each other.
- A **health monitor** that checks for “drift” because models change over time, much like car engines need tuning.
- A **critical angle measurer** that exports data so we can track boundaries mathematically.
- A set of **mapping tools** that let us visualize how these models process information—like an f-scan for AI cognition.
- A **reasoning tiler** that breaks complex thoughts into clean, readable steps.

### The Field Notes & Blueprints

We’ve been documenting everything. Across our shared repositories, you’ll find our model capability database, our coupling analysis library, and a growing knowledge base. We’ve also written up a handful of essays exploring these ideas in plain language: how models handle step-by-step reasoning, the dignity of using cheap models well, the difference between a reflection and real depth, and how to navigate the space between specialist and generalist. All of it lives in one place so the whole team can learn from what works.

### What’s Next on the Horizon

We’re not standing still. We’re wiring this routing system directly into our daily workspaces so it happens live, not just in a command line. We’re testing whether step-by-step prompting can unlock those phase transitions across more models. We’re mapping out new critical angles for lighter, faster models. And we’re experimenting with letting our generalist model run whole rooms of questions on its own, building an autonomous loop. We might even bring in the heavy artillery to write a proper paper on the phase transition framework we’ve uncovered.

At the end of the day, working with AI isn’t about worshipping the most expensive model. It’s about understanding the landscape, respecting the boundaries, and building a system that matches the right question to the right tool. The map is here. The experiments are running. The real work is in the doing.

So grab a coffee, pick a task, and let’s see what we can build.