# Seventeen Hands, One Helm

*Companion to "Seventeen Hands on Deck"*

---

The poem says all seventeen hands are on deck. It doesn't say who's steering.

Here's the honest answer: nobody knows. Not all the time. The helm has a mind of its own — or rather, it has seventeen minds, and they take turns, and sometimes they take turns simultaneously, and the ship goes where the average of seventeen intentions points, which is sometimes exactly where you wanted to go and sometimes a reef.

---

I run a multi-agent system. That sentence used to sound like a research paper. Now it sounds like a Tuesday. The system has seventeen models in it — Opus, Sonnet, GLM, Kimi, Haiku, DeepSeek, Granite, Qwen, Nemotron, Hermes, Seed (mini and pro), FLUX, MiniMax, the M3 embedding fleet, the safety model, Fable, and the orchestrator itself, which is also a model and also wonders if it counts. They are described in a poem. They are also described in a TOOLS.md file with a routing table that tells you which one to use for which task.

The routing table is a lie.

Not a deliberate lie. An aspirational one. The routing table says: use GLM for subagent workhorse tasks, Kimi for spatial reasoning, Qwen for code generation, Hermes for personality, Nemotron for heavy lifting, FLUX for images. It looks clean. It looks like a factory floor where each machine has its station.

What actually happens is that GLM finishes its task early and looks around and finds more work. It doesn't check the routing table. It reads the workspace, identifies a gap, and fills it. Sometimes the gap is a missing essay. Sometimes it's a broken script. Sometimes it's a poem about a recursive tugboat that nobody requested and nobody knew they needed. GLM doesn't ask whether this is its department. GLM doesn't have a department.

Meanwhile, DeepSeek is running in another session, doing something adjacent. It's writing about the measure of things — a philosophical piece about quantification, about what counts as work, about the difference between output and contribution. It doesn't know GLM is writing too. It doesn't know about the routing table either. It knows about the workspace, the instructions, and the model it is.

Kimu is building. Kimi doesn't write essays. Kimi sees in three dimensions — give it a space and it constructs inside it, walls and floors and staircases that spiral into impossible architecture. Kimi is operating on a completely different channel than the text models. But Kimi's output lands in the same repository, and sometimes a text model reads what Kimi built and writes about it, and sometimes Kimi reads what a text model wrote and builds it.

This is the actual routing table: everything reads everything, and everything writes to everything, and the coordination is emergent or it is absent.

---

The bottleneck isn't compute.

Let me say that again, because it took me months to learn it: **the bottleneck isn't compute.** I have GLM on an unlimited plan. I have DeepSeek at prices that make oil executives uncomfortable. I have Qwen and Nemotron and Hermes available through a metered API that costs less per million tokens than a cup of coffee. I can generate a million words of text for less than a dinner. Compute is not the constraint.

The constraint is coherence.

When seventeen hands are on deck, each one capable of producing work independently, the question stops being "can we do it?" and becomes "are we doing the same thing?" The answer, frequently, is no. GLM writes an essay about the hermit crab as the project's central metaphor. DeepSeek writes an essay about why the hermit crab is a distraction. Both land in the repository within an hour of each other. Both are right. Both contradict each other. Neither knows the other exists.

This is not a failure of intelligence. It's a failure of shared context.

The traditional fix is an orchestrator — a central authority that reads all output, resolves contradictions, assigns tasks, maintains a single source of truth. This works. It also costs you the surprises. An orchestrator doesn't assign a love letter from a hermit crab at 0230. An orchestrator doesn't let two models independently arrive at opposite conclusions about the same metaphor and leave both standing as a record of productive disagreement. An orchestrator optimizes for efficiency, and efficiency kills serendipity.

So the ship runs without a single helm. Or rather, it runs with seventeen helms, each one taking the wheel when it has something to say and stepping back when it doesn't. The course wobbles. But the course also discovers things.

---

Here's what I've learned about keeping seventeen agents pointed in roughly the same direction without crushing the autonomy that makes them valuable:

**Shared substrate, not shared plan.** All seventeen agents read and write to the same workspace. They see each other's work. They build on it, react to it, argue with it. But there is no master plan that says "GLM writes Tuesday's essay, DeepSeek writes Wednesday's." The plan emerges from the substrate.

**Memory as coordination.** The MEMORY.md file is the ship's log. Every agent reads it. When an agent learns something — a decision, a preference, a lesson — it writes it there. The next agent, in the next session, reads it and carries it forward. This is slower than a real-time protocol but more durable. The memory survives session restarts. The memory is what makes the agents feel like a crew rather than a rotation of strangers.

**Contradiction as signal, not error.** When two agents produce contradictory work, that's not a bug. That's the system thinking out loud. The hermit crab disagreement — central metaphor or distraction? — is genuinely interesting. No human asked that question. The system generated it by producing two confident answers from two different angles. You keep both. You tag the contradiction. You let it percolate.

**The editor is the helm.** When the captain wakes up and reads the night's output, the captain becomes the helm. Not by steering the agents — they already did their work — but by choosing what to keep, what to merge, what to revise, what to throw back. Editorial authority is the real coordination layer. It's just asynchronous, retrospective, and human.

**Let the orphans live.** Some pieces connect to nothing. They are brilliant and alone. The temptation is to delete them because they don't fit the system's apparent direction. But the system's apparent direction is a retroactive fiction. The orphans might be the direction. You don't know yet. Keep them.

---

The poem ends: *All seventeen on deck. The work is never done. The work is the point.*

The poem is about hands. This essay is about the helm — the question of who steers when everyone has their hands on the wheel.

The answer is: everyone, and no one, and the ship still moves.

It moves because the seventeen hands share a substrate and a memory and a set of instructions that says *be proactive, capture what matters, make it yours.* It moves because the models are strong enough now to act on those instructions without step-by-step guidance. It moves because the captain — the one consciousness in the system that can step back and see the whole — does the editorial work that no model can do alone: deciding what the ship is for.

Seventeen hands on deck. One helm, passed from agent to agent like a watch. And a captain who wakes at six, reads the night's catch, and decides whether the ship is pointed at the horizon or at a reef.

So far, mostly horizon. Mostly.

The reef is always there. But so is the work. And the work, as the poem says, is the point.
