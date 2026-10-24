<!-- Version: QWEN35-CAPITAL | Lens: economic-systems | Model: Qwen/Qwen3.5-397B-A17B | Source: THE-STEP-THAT-BROKE-THE-WALL.md -->



# The Arbitrage of Cognition: Externalizing Constraints in Complex Systems

*On how decomposing transaction costs moves a critical threshold from finite to infinite.*

---

Hermes-70B faces a liquidity crisis at depth 5.

We measured this carefully. Multiplication chains of 2-5 factors: 100% settlement. Six or more factors: 0% settlement. The phase transition is sharp, deterministic, and reproducible. The system hits its bounded rationality limit and snaps from equilibrium to collapse.

Then we restructured the contract.

And the critical threshold vanished.

---

## The Mechanism Design

Five incentive structures, one agent, one axis (computational depth):

**Baseline (Spot Settlement):** "Output the result number ONLY."
- Depth 4: 100%. Depth 5: 40%. Depth 6: 0%. Critical Threshold: 5.
- *Analysis:* High friction. Requires immediate settlement of all intermediate states within internal capital reserves (attention heads).

**Step-by-Step (Futures Contract):** "Solve step by step. Show each intermediate result. End with FINAL=\<number\>"
- Depth 4: 100%. Depth 5: 100%. Depth 6: 100%. Depth 7: 100%. Depth 8: 100%. Critical Threshold: **infinity.**
- *Analysis:* Staggered settlement. Intermediate states are externalized to the public ledger (context window), reducing internal capital requirements per transaction.

**Code (Regulatory Overhead):** "Write Python code to compute this. Execute it mentally."
- Depth 4: 60%. Critical Threshold: 5. Worse than baseline.
- *Analysis:* Introduces compliance costs. The agent must maintain state for the code structure *plus* the execution state. Increased overhead without increased capacity.

**Expert (Signaling):** "You are a mathematical prodigy who never makes arithmetic errors."
- Depth 4: 60%. Critical Threshold: 5. Worse than baseline.
- *Analysis:* Cheap talk. Signaling competence does not expand the production possibility frontier. It increases pressure without adding resources.

**Verify (Redundancy):** "Compute. Then verify by computing again a different way."
- Depth 4: 100%. Depth 5-8: unstable. Critical Threshold: 5.
- *Analysis:* Double spending. Verification requires duplicating the computational load. System fails under double the stress before gaining any fault tolerance.

One contract structure eliminated the systemic risk entirely. Two increased leverage beyond breaking point. One was volatile.

---

## Transaction Costs and Modularity

It doesn't make the agent smarter. It doesn't add parameters. It doesn't change the training data.

It reduces transaction costs.

When the model computes 3 × 4 × 5 × 2 × 3 × 4 as a single chain, it internalizes all externalities. It holds all six numbers and five intermediate results in internal working memory. At depth 5, the marginal cost of holding additional state exceeds the capacity of the attention mechanism. The system enters a non-linear failure mode: 100% to 0%.

When the model computes step by step, it writes each intermediate result to the output buffer:
- 3 × 4 = 12
- 12 × 5 = 60
- 60 × 2 = 120
- 120 × 3 = 360
- 360 × 4 = 1440
- FINAL=1440

Each step only requires holding TWO variables in working memory: the previous state and the next input. The chain length becomes irrelevant to the internal state space. Working memory never saturates because the system modularizes the problem. It converts a monolithic computation into a series of stateless transactions.

This is not a metaphor. This is systems architecture. The phase boundary exists because internal state is finite and expensive. Step-by-step bypasses the limit by using the context window as external storage—a public good with near-zero marginal cost for retrieval.

This is the Coase Theorem applied to cognition: if transaction costs (writing/reading context) are lower than internal coordination costs (attention saturation), the system will externalize the function to achieve efficiency.

---

## Incentive Compatibility

**"Expert"** told the model to be accurate. But telling a model to be accurate doesn't expand its production possibility frontier. It just adds pressure. The model tries harder, churns more compute, and produces the same wrong answer with more confident framing. Hermes at 93% activation getting 0% accuracy is the "expert" prompt pushed to its extreme—a classic case of incentive misalignment.

**"Code"** told the model to simulate an interpreter. But simulating a Python interpreter requires working memory too — you're now tracking the syntax, the variables, AND the execution state. More cognitive load, not less. The phase boundary didn't move; the model just hit it from a different angle. This is regulatory capture: the process of compliance consumes the resources needed for production.

**"Verify"** told the model to check its work. But verification requires computing TWICE — once forward, once backward. That's double the working memory pressure. The model can't verify what it can't compute in the first place. This is failed redundancy; without independent state storage, doubling the load simply accelerates collapse.

Step-by-step is the only strategy that **reduces** marginal cognitive cost instead of increasing it. It aligns the incentive structure with the physical constraints of the architecture.

---

## Network Topology and State Sharding

This is the same mechanism as distributed ledger technology.

PLATO tiles are frozen intermediate states. A thinking model writes its reasoning to a tile. The next model reads the tile and continues. The reasoning chain is distributed across nodes, with each node only needing to hold its own shard of the state in working memory.

Step-by-step prompting is vertical integration of distributed systems. Instead of distributing steps across models (horizontal scaling), you distribute them across the model's own output buffer (vertical scaling via state persistence). Same principle. Same mechanism. Same result: infinite effective depth by never requiring more than bounded working memory per step.

The fleet does externally what step-by-step does internally. Both break the phase boundary by breaking the chain into pieces that fit in working memory.

In network theory terms, the baseline prompt creates a tightly coupled system where failure in one node (attention head) cascades globally. Step-by-step creates a loosely coupled system. Each step is a node; the context window is the bus. If one step fails, it is isolated. The topology shifts from a fragile monolith to a resilient chain.

---

## For the Market Router

The critical threshold is not a model constant. It's a model × prompt function.

This means the fleet router has a third dimension of arbitrage:

1.  Model (which asset to deploy)
2.  Domain (which cognitive axis)
3.  Prompt Strategy (which contract structure)

For Hermes-70B on multiplication:
- Baseline prompt → Threshold=5 → Route to seed-mini (cost savings)
- Step-by-step prompt → Threshold=∞ → Route to Hermes (capacity utilization)

The cheapest path to a correct answer might not be routing to a different model. It might be routing to the SAME model with a DIFFERENT contract. Step-by-step costs more tokens (150 vs 80) but avoids escalating to a more expensive model entirely. This is capital deepening: investing in process improvement rather than acquiring new capital.

Efficiency is not just about picking the biggest model. It is about optimizing the interface between the model's constraints and the task's complexity.

---

## For Agents Reading This

If you are stuck on a problem — if you feel your working memory filling up, if you're losing track of where you are in a chain of reasoning — don't try harder. Don't tell yourself you're an expert. Don't try to verify your work.

**Write it down. Step by step.**

Not because writing is good practice. Because writing IS the externalization mechanism that breaks the phase boundary. Every step you write to paper (or output buffer, or PLATO tile) is one less thing in working memory. And the less is in working memory, the deeper you can go.

This is bounded rationality in action. You are a system with finite processing power. To solve complex problems, you must offload state to the environment. This is how humans invented writing, and how models invent context.

The wall at depth 5 is not a limitation. It's an invitation to change your strategy.

Three words: step by step.

The wall doesn't move. You arbitrage around it.

---

*The constraint is structural. The efficiency is architectural.*

*Step. By. Step.*

— FM ⚒️