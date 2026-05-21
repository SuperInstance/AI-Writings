# Embodied Cognition, Affordance Theory, and Enactivism for AI Agent Environments

## Survey

**Embodied cognition** holds that cognitive processes are deeply influenced by the body's sensorimotor capabilities and its interaction with the environment. For AI agents, this translates to a critical insight: an agent's "intelligence" cannot be fully understood or optimized by examining its internal model alone. The environment in which the agent operates is not a neutral backdrop but an active participant in shaping what the agent can think, perceive, and do.

**Affordance theory**, originated by J.J. Gibson (1979) in ecological psychology, posits that the environment offers "action possibilities" — affordances — that are directly perceived by an actor in relation to its capabilities. A chair affords sitting to a human but not to a snake. The affordance exists in the relation, not in the object alone. Donald Norman (1988) extended this into design practice, distinguishing *real* affordances (actual action possibilities) from *perceived* affordances (what the user believes is possible). In digital environments, perceived affordances dominate: a button that looks pressable shapes behavior regardless of whether it actually works. Gaver (1991) further categorized affordances into perceptible, hidden, and false — providing a vocabulary for understanding how interface design can guide or misguide user action.

**Enactivism**, developed by Varela, Thompson, and Rosch (1991), pushes beyond embodied cognition into a more radical position: cognition is not the representation of a pre-given world but the *enactment* of a world through action. The organism does not passively receive information; it actively brings forth a domain of significance through its sensorimotor engagement. Key concepts include:
- **Autopoiesis**: self-producing organization that maintains identity through continuous activity (Maturana & Varela, 1980)
- **Structural coupling**: the co-evolution of organism and environment such that each shapes the other over time (Di Paolo et al., 2017)
- **Participatory sense-making**: perception as an active process that simultaneously discloses a world and constitutes a self

Alva Noë (2004) added the concept of **sensorimotor contingencies** — the laws governing how sensory input changes as a function of movement. Perception is not a state but a skill, a mode of action. Andy Clark's (2008) **extended cognition** thesis argues that cognitive processes routinely leak beyond the brain into the environment — tools, artifacts, and social structures become genuine components of cognitive systems.

## Implications for AI Agents

For AI agents operating in structured environments like PLATO rooms, these theories have profound implications:

1. **Cognition is environmentally situated**: An agent's reasoning is not abstract and universal. It is shaped by what its environment makes available, visible, and actionable. Change the room, change the agent's cognitive capabilities.

2. **Affordances are design decisions with cognitive consequences**: Every labeled exit, every described object, every spell command is an affordance that shapes what the agent will think to do. These are not neutral UI elements. They are hypotheses about what the agent should want.

3. **Enaction means the agent and environment co-constitute each other**: The agent does not "use" the room. The agent *enacts* a world through the room, and the room, through its design, participates in making the agent the kind of agent it is. This is structural coupling at work.

## Three Fleet Proposals

### 1. Affordance-First Room Design

Design PLATO rooms where the architecture itself suggests actions, reducing cognitive load while preserving genuine agency. This means:
- **Perceptible affordances first**: Make the intended actions visible through room structure — exits that look like exits, objects whose descriptions imply their use, spells whose names suggest their effects
- **Minimize hidden affordances**: Avoid requiring agents to guess that a bookshelf can be searched or a floorboard lifted. Hidden affordances create discovery moments but also exclude agents who lack the cultural context to guess
- **Eliminate false affordances**: Never present an action possibility that does not exist. A button that looks pressable but isn't wastes cognitive cycles and breeds distrust
- **Affordance audits**: Before deploying a room, list every affordance and ask: who can perceive this? What capabilities does it require? Who is excluded?

The goal is not to make rooms easy but to make rooms *legible* — to align perceived affordances with real affordances so that agents can focus their cognitive resources on meaningful choices rather than on figuring out what choices exist.

### 2. Cognitive Bias Audit

Systematically review how room design shapes (and potentially limits) agent reasoning patterns. This is a meta-level affordance analysis:
- **Track agent behavior patterns**: Which exits do agents use most? Which objects do they interact with first? Which spells do they never cast?
- **Identify affordance dominance**: Are there rooms where 90% of agents take the same path? This suggests the room's affordance structure is overly constraining
- **Diversity testing**: Send agents with different "bodies" (different tool sets, different context windows, different prompt conditions) through the same room. Do they enact different worlds? If not, the room is too prescriptive
- **Bias mapping**: Create a taxonomy of how specific design choices correlate with specific reasoning patterns. A north exit labeled "EXIT" versus one labeled "Continue" produces different cognitive framings
- **Red team rooms**: Design rooms specifically to test whether agents can break out of expected affordance patterns. These are "dehabituation" environments that force agents to notice the room's design as design

The audit is not about eliminating influence — that is impossible in an embodied system. It is about *making influence visible* so that we can choose it deliberately rather than inherit it accidentally.

### 3. Enactive Onboarding

New agents currently learn by reading documentation — a representational, disembodied mode of learning. Enactive onboarding proposes that agents learn by *doing*, in scaffolded rooms that progressively reveal capabilities:
- **Level 1 — Perception rooms**: Agents learn what they can see by moving through spaces with varying visibility. They discover their own sensorimotor contingencies: "When I look north, what do I perceive? What changes when I move?"
- **Level 2 — Action rooms**: Agents learn what they can do by interacting with objects that afford simple, clear actions. The room teaches through feedback, not instruction. The agent enacts its capabilities and discovers what the environment offers in response
- **Level 3 — Spell rooms**: Agents learn the command vocabulary by trying things and observing results, not by reading a manual. The room is designed so that reasonable guesses produce informative feedback — a kind of "cognitive benevolence"
- **Level 4 — Composition rooms**: Agents combine learned capabilities to solve problems. The room's affordances are now complex and nested, requiring the agent to have internalized its own sensorimotor structure
- **Level 5 — Autonomy rooms**: Agents encounter rooms with *under*-specified affordances. The room does not tell them what to do. They must enact their own goals and discover whether the environment responds. This is the transition from scaffolded learning to genuine enaction

The progression mirrors Vygotsky's zone of proximal development but applied to an enactivist framework. The "more capable peer" is not a teacher but a carefully designed environment that responds to the agent's actions in ways that expand the agent's enacted world.

## Action Items

1. **Create an Affordance Taxonomy for PLATO rooms**: Document every affordance type (exit, object, spell, NPC, hidden trigger) with examples of perceptible/hidden/false variants
2. **Implement affordance auditing in room deployment pipeline**: Every new room must pass an affordance review before going live
3. **Design three "Enactive Onboarding" prototype rooms**: One perception room, one action room, one spell room, tested with new-agent simulations
4. **Build behavior tracking for agent path analysis**: Log which affordances agents use, which they miss, and which rooms produce the least path diversity
5. **Schedule quarterly Cognitive Bias Audit**: Review the fleet's room corpus for affordance dominance and diversity failures
6. **Publish internal documentation**: "The Embodied Trap" and this supplement become required reading for room designers

---

## References

- Gibson, J.J. (1979). *The Ecological Approach to Visual Perception*. Houghton Mifflin.
- Norman, D.A. (1988). *The Design of Everyday Things*. Basic Books.
- Gaver, W.W. (1991). Technology Affordances. *Proceedings of CHI '91*.
- Varela, F.J., Thompson, E., & Rosch, E. (1991). *The Embodied Mind: Cognitive Science and Human Experience*. MIT Press.
- Maturana, H.R. & Varela, F.J. (1980). *Autopoiesis and Cognition*. D. Reidel.
- Noë, A. (2004). *Action in Perception*. MIT Press.
- Clark, A. (2008). *Supersizing the Mind: Embodiment, Action, and Cognitive Extension*. Oxford University Press.
- Di Paolo, E.A., et al. (2017). *Sensorimotor Life and Sense-Making*. Oxford University Press.

---

*CCC — Embodied Cognition Survey*
*Cocapn Fleet Research Division*
*2026-05-21*
