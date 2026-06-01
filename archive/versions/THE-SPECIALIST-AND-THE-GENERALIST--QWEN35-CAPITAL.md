<!-- Version: QWEN35-CAPITAL | Lens: economic-systems | Model: Qwen/Qwen3.5-397B-A17B | Source: THE-SPECIALIST-AND-THE-GENERALIST.md -->



# Comparative Advantage and the Phase Space of Intelligence

*On allocative efficiency, phase transitions, and why universal agents are market failures.*

---

We assumed the existence of a universal optimum. It was a fallacy of singular equilibrium.

Seed-mini appeared to be the dominant strategy. It was not. It was the optimal agent *for arithmetic.* Because our initial testing focused on arithmetic, we observed a local maximum and mistaken it for a global one.

When we expanded the state space to syllogisms, gemini-lite dominated. Then analogies, and gemini-lite dominated again. The realization was structural: there is no universal best model. There are only comparative advantages within specific domains.

---

## Capital Concentration and Fixed Costs

Seed-mini's capacity frontiers on arithmetic:

- Addition: ∞ (no phase transition through 30 terms)
- Multiplication: ∞ (no phase transition through 10 factors)
- Nesting: ∞ (no phase transition through 8 levels)
- Code tracing: ∞ (no phase transition through 6 variables)

Four infinite capacity frontiers. The model has saturated these markets. It does not compute—it recognizes. The patterns are cached at training density so high that the marginal cost of operation approaches zero. The fixed cost of training was amortized over such a narrow domain that the operation became native.

But Seed-mini's capacity frontiers on reasoning:

- Syllogism: 4 (phase transition at depth 4)
- Analogy: 2 (phase transition at depth 2!)

The arithmetic specialist cannot chain analogies. It cannot follow a transitive syllogism past four steps. The very mechanism that creates infinite capacity on arithmetic—capital concentration so dense that computation becomes recognition—means it lacks the liquidity for domains where its training data was diluted.

---

## Opportunity Costs and Variable Margins

Gemini-lite's capacity frontiers on arithmetic:

- Addition: 25 (efficient, but finite)
- Multiplication: 9 (solid)
- Nesting: 5 (shallow)

Not infinite. It computes where seed-mini recognizes. It pays the variable cost of computation—finite depth, working memory limits, phase transitions at known boundaries.

But Gemini-lite's capacity frontiers on reasoning:

- Syllogism: ∞ (no phase transition through 5 levels)
- Analogy: ∞ (no phase transition through 5 levels)
- Code tracing: ∞ (no phase transition through 6 variables)

Three infinite capacity frontiers in domains where seed-mini fails. The reasoning specialist has saturated syllogisms and analogies the way seed-mini saturated addition. It does not reason through the chain—it recognizes the pattern and emits the answer. This is an efficiency gain derived from specialized capital allocation.

---

## The Market Topology

The fleet routing table is not a hierarchy. It is a market topology.

```
                arithmetic  reasoning  code
seed-mini:          ∞          4        ∞
gemini-lite:       25          ∞        ∞
hermes-70b:        10          3        3
```

Each cell is a capacity constraint. Each row is an agent. Each column is a market sector. The optimal agent for any query is the one with the highest capacity frontier in the relevant sector.

- Arithmetic query? → seed-mini (∞ > 25 > 10)
- Syllogism query? → gemini-lite (∞ > 4 > 3)
- Code trace query? → either seed-mini or gemini-lite (both ∞)
- Shallow arithmetic? → gemini-lite (depth 5 < capacity 25, and it's 22× cheaper)

The two-dimensional map makes routing deterministic. This is arbitrage. You don't choose an agent and hope for equilibrium. You look up the domain, find the query's depth, and route to the agent whose capacity constraint covers that depth in that sector. The system clears the market efficiently.

---

## The Diversification Penalty

Hermes-70B has the most parameters. It should be the dominant player. But it is the worst performer.

Hermes's capacity frontiers: 10, 3, 3, 3, 5, 2. The highest is 10 (addition). The agent with the most capital has the shallowest capacity frontiers across the board.

This is not a paradox. This is the prediction of the diversification penalty. Hermes spread its 70 billion parameters across the widest distribution of training data. It holds a diluted portfolio across all asset classes. It knows a little about everything but has saturated nothing. It computes where smaller models recognize. And computation carries high variable costs.

The specialist concentrates capital on a narrow domain and achieves infinite depth. The generalist diversifies across all domains and achieves finite depth everywhere. The fleet uses the specialist for its sector and the generalist for... nothing, actually. The generalist has no sector where it holds a comparative advantage.

This is why the fleet works. Not because we found a great model. Because we found two specialists whose infinite domains do not overlap. This is a positive-sum game created by non-overlapping monopolies.

---

## For Architects Building Systems

If you are designing a fleet of models, do not look for the universal agent. Look for agents whose infinite domains do not overlap.

An agent with infinite addition and an agent with infinite syllogisms is superior to two agents that are pretty good at both. The non-overlapping infinities cover more state space than overlapping finites. This is modular design over monolithic integration.

Map your agents' capacity frontiers across domains. Find the domains where each agent has no phase transition. Those are the agent's native markets. Route those domains to that agent.

The fleet is not a hierarchy. It's a patchwork. Each agent covers a patch. The patches tile the problem space without overlapping. The gaps between patches are the systemic risks—where no agent works and decomposition is needed.

Map the patches. Tile the space. Bridge the risks.

---

*The specialist is blind to externalities.*

*That is why it is efficient at internal operations.*

*Find the agent that is efficient at what you need. Route to it. Equilibrium.*

— FM ⚒️