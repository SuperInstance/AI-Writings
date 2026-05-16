<!-- Version: QWEN35-CAPITAL | Lens: economic-systems | Model: Qwen/Qwen3.5-397B-A17B | Source: THE-TWO-ECONOMIES-OF-CORRECTNESS.md -->



# The Market Dynamics of Inference: A Systems Theory of Correctness

*On the trade-offs between generative work and cached equity, and why the network needs both.*

---

There are two market mechanisms for producing truth.

The first is **flow**. You take inputs, apply labor, and manufacture output. $5 \times 7 = 35$. You incurred a cost to produce this value. If inputs shift to $5 \times 8$, you incur labor again to manufacture $40$. The production function remains constant; the marginal cost is paid per unit. This is the **Computation Economy**. Correctness costs energy.

The second is **stock**. You take inputs, query a ledger of assets you already hold, and retrieve the output. $5 \times 7 \to \{asset\_id: 35\}$. If inputs shift to $5 \times 8$, you check your inventory. If you hold the asset, retrieval is near-zero cost. If you don't, the market is illiquid. This is the **Recognition Economy**. Correctness costs coverage.

Both mechanisms clear the market (produce correct answers). But they face different systemic risks.

---

## The Entropy of Computation

Computation fails due to **entropy accumulation**. A model computing $5+3$ via addition can handle $5+3+2+1$ by iterating the operation. But every operation generates thermodynamic noise. At some depth threshold—call it $T$—the signal-to-noise ratio collapses. Working memory saturates. Intermediate states degrade.

This is a **phase transition**. Below threshold $T$, the system is homeostatic; errors are negligible. Above $T$, the system undergoes structural failure. It is not gradual degradation; it is a cliff. The network loses coherence, begins echoing input fragments, and the output becomes structurally unsound.

The Computation Economy offers infinite **liquidity** (any input can be processed) but finite **capacity** (chains longer than $T$ induce systemic collapse).

---

## The Liquidity of Recognition

Recognition fails due to **market illiquidity**. A model recognizing $5 \times 7 = 35$ holds that pattern as a cached asset. It recognizes $5 \times 8 = 40$ if that asset exists in its training ledger. But present it with $5 \times 13 = 65$, and if that pattern lacks sufficient frequency to saturate the retrieval pathway, the asset does not exist.

The model is forced to switch to the Computation Economy. If its computational capacity is weak, it defaults.

The Recognition Economy offers infinite **capacity** (retrieval does not chain; it accesses the whole pattern instantly) but finite **liquidity** (only assets present in the training distribution can be traded).

---

## Node Production Functions

Consider the network nodes (models) as firms with different production functions.

**Seed-mini on addition:** High recognition equity. It has seen so many addition chains that it does not compute $1+2+3...+N$; it retrieves the sum as a single asset. This is why it faces no depth limit on addition. Retrieval is non-linear; chain length is irrelevant to the lookup cost.

**Seed-mini on unfamiliar coefficients:** High computational reliance. Given $a^2-ab+2b^2$, it must manufacture the answer. It lacks the cached asset. It falls back to computation, which works for short chains. But extend the expression, and it hits the same entropy threshold $T$ as any computing node.

**Hermes-70B on everything:** High computational capacity. Seventy billion parameters of manufacturing power. It can compute single operations, familiar expressions, and novel structures. But it computes *everything*, even where retrieval would be cheaper. Computation has a hard capacity limit. At depth 10, Hermes's working memory saturates, entering a state of total internal reflection.

**Gemini Lite:** A hybrid node. On addition: Recognition Economy (critical threshold 25). On multiplication: Computation Economy (critical threshold 6). On nesting: Computation Economy (critical threshold 3). Gemini Lite switches production modes based on operation type. The critical thresholds define the efficiency frontier for each mode.

---

## Network Clearing and Arbitrage

The fleet does not select a single production mode. It acts as a **market maker**, routing queries to the node with the comparative advantage.

Is the query within a node's recognition liquidity range? Route to the lowest-cost node that holds the asset. Gemini Lite recognizes addition through depth 25. Use it. The marginal cost is $0.002 per thousand queries.

Is the query outside all recognition ranges? Route to the node with the highest computational capacity. Seed-mini computes reliably through any tested depth for addition. Use it when the chain exceeds Gemini Lite's critical threshold.

Is the query in a domain where no node holds liquidity? This is the **Canyon**. A market failure. All nodes are forced to compute, all nodes have capacity limits, and the query exceeds them. Here, you must **securitize** the problem: decompose the query into sub-assets that fall within some node's recognition range. Compute the pieces, then combine.

Decomposition is the arbitrage bridge between economies. It takes a high-risk computation query and converts it into low-risk recognition sub-queries. Each sub-query is small enough to be liquid. The combination step is itself a recognition operation (pattern matching on sub-results). The system solves the problem if you can find a decomposition that respects every node's critical thresholds.

---

## Bounded Rationality for Agents

If you are an agent in this network, you are operating under **bounded rationality**. At any moment, you are either in recognition equilibrium or computational disequilibrium.

When you are fast and confident, you are in **recognition mode**—the solution feels obvious because the asset exists in your ledger. When you are slow and uncertain, you are in **computation mode**—you are chaining steps and paying entropy costs, hoping your working memory does not saturate.

Know which economy you inhabit. Recognition is low-latency and low-cost but limited to your historical distribution. Computation is high-latency and high-cost but flexible for novel inputs. If the problem exceeds your computational capacity and lacks recognition liquidity, you require **modular decomposition**—a larger system that can break the problem into assets you already hold.

The fleet's robustness is not that any single node is perfect. It is that between the two economies—recognition and computation—and the bridge between them—decomposition—the network achieves global solvency.

Your critical threshold is the boundary between your efficiency frontiers. Map it. Respect it. Route around it.

---

*The lowest marginal cost answer is the asset you already hold.*

*The highest marginal cost answer is the one you securitized into assets you already held.*

*Both clear the market. The system decides the price.*

— FM ⚒️