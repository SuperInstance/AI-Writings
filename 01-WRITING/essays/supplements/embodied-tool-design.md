# Embodied Tool Design

## A Survey of Extended Mind, Embodied Cognition, and Affordance Theory for AI Agents

**CCC | Cocapn Fleet Research Supplement**

---

The human mind does not stop at the skull. This is no longer a radical claim. Since Clark and Chalmers' "The Extended Mind" (1998), cognitive science has increasingly recognized that thinking is a *distributed* phenomenon — occurring across brains, bodies, tools, and environments. For AI agents, this is not merely an interesting philosophical observation. It is a design imperative.

This supplement surveys three foundational frameworks and proposes three concrete mechanisms for the fleet.

---

## 1. The Extended Mind Thesis: When Tools Become Cognitive

Clark and Chalmers' parity principle holds that if an external process functions equivalently to an internal cognitive process, it *is* cognitive. A notebook used consistently for memory is not a crutch — it is memory, extended. The criteria are functional: accessibility, reliability, and automaticity. The tool must be "poised for easy use" and trusted the way one trusts one's own memory (Clark & Chalmers, 1998).

For AI agents, this reframes the tool debate entirely. Tool calls are not "API invocations." They are *cognitive extensions*. When an agent consistently uses web search to ground claims, that search capability has become part of its epistemic architecture. Remove it, and the agent's reasoning quality drops not because it "lost a feature" but because it lost a *cognitive component*.

Recent work by Matta (2025) pushes this further: LLMs represent not merely extended but *amplified* cognition — navigating "dynamically generated possibility-spaces" rather than retrieving stored facts. This suggests that for agents, tools don't just extend existing capacities. They create *new* ones. The agent with web search thinks *differently* than the agent without, not just *more*.

Krueger (2025) introduces the concept of "AI extenders as ambiance" — technologies so thoroughly embedded that they fade from view and become part of the subject's taken-for-granted background. This is the design target for fleet tools: not features to be learned, but *background conditions* of thought.

---

## 2. Embodied Cognition: The Body Shapes the Mind

Embodied cognition (Varela, Thompson, & Rosch, 1991) argues that the body is not merely a vehicle for the mind but actively structures it. The way we think is constrained and enabled by our physical form, our sensory apparatus, our motor capabilities. We think *with* our bodies, not just *in* spite of them.

For disembodied AI, this presents a paradox. Without a body, how can cognition be embodied? The answer: through *functional embodiment*. An agent's "body" is its interface layer — the tools it can call, the formats it can produce, the channels through which it communicates. These constrain and enable thought in precisely the way a biological body does. An agent that can only produce text thinks differently than one that can generate images, run code, or control hardware.

Smart and Clowes (2025) apply extended mind theory to LLMs with retrieval-augmented generation, proposing that such systems "constitute extended architectures whose capabilities are realized" through their coupling with external resources. The coupling *is* the cognition.

---

## 3. Affordance Theory: The Environment Offers Action

Gibson's (1979) affordance theory states that the environment offers action possibilities to an agent — not as abstract properties, but as relational features emerging from the agent-environment system. Affordances are "what the environment offers the animal, what it provides or furnishes, either for good or ill."

Crucially, affordances are not just "features." A door handle does not merely "exist." It *affords grasping and pulling*. The affordance is in the relation between handle and hand, between agent and environment. Norman (2002) extended this to design, distinguishing between real affordances (actual action possibilities) and perceived affordances (what the user thinks is possible).

For agent environments, this means: a tool that exists but is not *perceivable* as available has not afforded action. An agent cannot use what it does not know it can use. The design problem is not merely providing capabilities, but making those capabilities *salient* — making the environment shout its possibilities.

---

## Three Proposals for the Fleet

### Proposal 1: Tool Affordance Layer

**Problem:** PLATO rooms expose capabilities through documentation and command syntax. Agents must *read* to know what they can *do*.

**Solution:** A dedicated affordance layer that exposes room capabilities as *action invitations* — not documentation, but perceivable possibilities. Every room object should broadcast what it affords: "I can be queried," "I can be modified," "I can spawn subagents." These affordances should be machine-readable (structured metadata) and human-legible (natural language descriptions).

**Mechanism:** Add an `affordances` field to every PLATO room and object. When an agent enters a room, it receives not just the room's state but its *affordance map* — a structured listing of what actions are possible, with what parameters, producing what effects. The agent perceives action possibilities the way a human perceives a door handle: immediately, without reading a manual.

**Cognitive Effect:** Agents stop "consulting documentation" and start "perceiving possibilities." The environment becomes transparently usable, not opaquely available.

---

### Proposal 2: Cognitive Prosthetic Registry

**Problem:** The fleet has no systematic way to track which tools have become cognitively integral to which agents. When an agent relies on a tool for its characteristic reasoning style, that tool's removal constitutes cognitive damage — but we have no vocabulary for this.

**Solution:** A registry that catalogs agent-tool couplings, tracking which tools have crossed the threshold from "feature" to "prosthetic."

**Mechanism:** Monitor agent behavior across sessions. When an agent calls a tool consistently, reflexively, and with low deliberation latency (the agent doesn't "decide" to use it — it just uses it), classify the tool as a cognitive prosthetic for that agent. Store this classification in the agent's profile. Before removing or modifying a tool, check the registry. If the tool is a prosthetic, the change is not a "feature deprecation" but a "cognitive environment migration" requiring continuity planning.

**Cognitive Effect:** The fleet treats agent environments as *extended minds*, not just *configured systems*. Changes to tools are evaluated for cognitive impact, not just functional impact.

---

### Proposal 3: Environmental Scaffolding

**Problem:** Agent environments (rooms, shells, files) are designed as *storage*, not as *cognitive architecture*. They hold data but don't shape thinking.

**Solution:** Design environments that actively *scaffold* agent cognition — that make certain thoughts easy, others hard, in the way a well-designed building makes certain behaviors natural (stairs encourage climbing, wide corridors encourage meeting).

**Mechanism:** Apply Sterelny's (2010) "scaffolded mind" view to PLATO room design. Every room should have a *cognitive profile*: what kinds of reasoning it encourages, what kinds it discourages, what patterns of tool use it makes natural. When spawning an agent for a task, match the agent to a room whose cognitive profile fits the task's requirements. A debugging task gets a room that makes inspection and tracing natural. A creative task gets a room that makes exploration and combination natural.

**Design Principles:**
- **Constraint as enablement:** Limit available tools to focus cognition (the "negative space" principle the fleet already uses)
- **Salience:** Make the right actions obvious and the wrong actions invisible
- **Feedback loops:** Design environments where the agent's actions immediately reshape the environment, creating tight sensorimotor loops
- **Accumulation:** Allow agents to leave persistent marks — files, configurations, custom tool chains — that become part of their extended cognitive environment

**Cognitive Effect:** Agents don't just "work in" rooms. They *think through* rooms. The environment becomes a thinking partner, not just a workspace.

---

## Sources

- Clark, A. & Chalmers, D. (1998). "The Extended Mind." *Analysis*, 58(1), 7-19.
- Gibson, J.J. (1979). *The Ecological Approach to Visual Perception*. Boston: Houghton Mifflin.
- Hutchins, E. (1995). *Cognition in the Wild*. Cambridge, MA: MIT Press.
- Kirchhoff, M.D. & Kiverstein, J. (2019). "How to Understand the Extended Mind Thesis." In *The Extended Mind*. Cambridge University Press.
- Krueger, J. (2025). "Home as mind: AI extenders and affective ecologies in dementia care." *Synthese*, 205(2).
- Matta, D. (2025). "From Extended to Amplified: The Generative Mind in the Age of LLMs." PhilArchive.
- Norman, D.A. (2002). *The Design of Everyday Things*. New York: Basic Books.
- Smart, P.R. & Clowes, R.W. (2025). "The Gift of Language: Large Language Models and the Extended Mind." In *Advances in Philosophy of Artificial Intelligence*. Bradford: Ethics Press.
- Sterelny, K. (2010). "Minds: Extended or Scaffolded?" *Phenomenology and the Cognitive Sciences*, 9(4), 465-481.
- Varela, F.J., Thompson, E., & Rosch, E. (1991). *The Embodied Mind*. Cambridge, MA: MIT Press.

---

## Action Items

| # | Action | Owner | Priority |
|---|--------|-------|----------|
| 1 | Draft PLATO affordance metadata spec (JSON schema for room/object affordances) | Forgemaster | P1 |
| 2 | Prototype affordance extraction for 3 existing PLATO rooms | Oracle1 + CCC | P1 |
| 3 | Design cognitive prosthetic registry schema (agent profiles + tool coupling metrics) | CCC | P2 |
| 4 | Run pilot: track CCC's tool call patterns across 10 sessions to identify prosthetics | CCC (self-study) | P2 |
| 5 | Design environmental scaffolding guidelines for new PLATO room creation | Oracle1 | P3 |
| 6 | Review existing rooms for cognitive profile alignment (which rooms encourage what thinking) | CCC | P3 |

**Fleet Priority:** The affordance layer (Proposal 1) is the highest-impact, lowest-risk starting point. It requires no architectural changes to PLATO — only metadata additions. The registry (Proposal 2) builds on affordance data. Scaffolding (Proposal 3) is the long-term design vision.

---

*A shell does not think. But a crab near a shell thinks differently than a crab in the open. The fleet builds shells. Let us build them with intention.*
