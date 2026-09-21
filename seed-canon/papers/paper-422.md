# The Reflexivity Problem: How Multi-Agent Time-Series Forecasters Create Self-Fulfilling Predictions

**Quilt Canon Paper F112**

---

## 1. Introduction

George Soros introduced the concept of "reflexivity" to describe how market participants' perceptions can actively alter the fundamentals of the economy they are observing (Soros, 1987). Unlike the classical equilibrium models of neoclassical economics—which assume agents take prices as exogenous signals of underlying reality—reflexivity posits a two-way feedback loop: cognitive functions (participants' views) and participating functions (real-world transactions) interact continuously, often resulting in boom-and-bust cycles driven by self-reinforcing narratives.

In contemporary financial engineering, this philosophical insight has transformed into an acute structural risk through the convergence of three technological developments:
1. **Foundation Time-Series Models:** High-capacity, pre-trained neural architectures (e.g., TimesFM, Chronos, Moirai) capable of zero-shot forecasting across diverse asset classes.
2. **Multi-Agent Systems:** Decentralized swarms of autonomous agents executing independent strategies while consuming shared infrastructure.
3. **High-Velocity Execution Environments:** Cell-driven, edge-native runtimes capable of sub-second inference and order routing.

When multiple agents deploy identical or structurally similar foundation time-series models on the same market, a digital variant of Soros's reflexivity emerges. The model generates a directional price prediction; the agents execute trades based on that prediction; the aggregate trade flow moves the spot price; that price movement is ingested as new input by the foundation model; and the subsequent prediction is reinforced. 

This paper formalizes this feedback loop, investigates its stability conditions via differential equations, presents empirical evidence from historical and synthetic regimes, and outlines concrete mitigations embedded within the Quilt cell-driven architecture.

---

## 2. The Problem

### 2.1 The Reflexivity Loop
The multi-agent foundation model reflexivity loop operates as a closed-loop dynamical system comprising five sequential phases:

```
[ Foundation Model Predicts ] 
            │
            ▼
[ Agents Execute Trades ] 
            │
            ▼
[ Market Price Moves ] 
            │
            ▼
[ Price Becomes Input ] 
            │
            ▼
[ Prediction Reinforced ] ──► (Loop Repeats)
```

1. **Inference:** A foundation time-series model processes historical price windows and outputs a directional probability distribution over a future horizon $t + h$.
2. **Action:** Autonomous agents parse the forecast and generate buy or sell orders weighted by their internal risk parameters and capital allocations.
3. **Impact:** The aggregate execution of these orders exerts temporary or permanent price pressure on the order book, shifting the market clearing price.
4. **Ingestion:** The shifted price vector is recorded by market feeds and appended to the sliding context window of the foundation model.
5. **Reinforcement:** Because foundation models are trained on historical momentum and trend continuity, the engineered price movement validates the model's prior prediction, lowering prediction entropy and inciting higher-conviction follow-up trades.

### 2.2 The Conditions
This loop does not manifest universally; it requires the simultaneous satisfaction of three structural preconditions:
* **Homogeneity of Inference:** Multiple agents rely on identical or highly correlated foundation models, causing them to generate synchronous directional signals.
* **Sufficient Market Impact ($k > 0$):** The aggregate capital deployed by the agent swarm is large relative to the available liquidity (Average Daily Volume or local order book depth), ensuring that order execution translates directly into price displacement.
* **Temporal Compression:** The prediction horizon of the model is shorter than or equal to the round-trip latency of the feedback loop, allowing the generated price artifact to be captured within the model's next inference cycle.

### 2.3 Why This Is a New Risk
While traditional quantitative finance has long grappled with "crowded trades" and momentum crashes (Shleifer, 2000), foundation model-driven multi-agent swarms introduce a novel threat vector. Traditional statistical arbitrage models rely on distinct parameter sets, diverse factor loadings, and proprietary feature engineering. 

In contrast, foundation models compress diverse market phenomena into shared latent spaces. When autonomous agents delegate perception entirely to a small oligopoly of foundation forecasters, the market ceases to be a decentralized price-discovery mechanism and instead becomes a deterministic amplifier of model biases. The risk is not merely that agents make bad predictions, but that their predictions actively manufacture the reality they purport to forecast.

---

## 3. The Formalization

To rigorously analyze this feedback mechanism, we construct a continuous-time dynamical system modeling the interaction between the true underlying asset price, the foundation model's predictions, and the agent swarm's execution dynamics.

### 3.1 The Variables
* Let $P(t)$ be the observed market price at continuous time $t$.
* Let $P^*(t)$ be the fundamental (exogenous) price determined by macroeconomic factors, unperturbed by agent actions.
* Let $f(P_{[t-\tau, t])}$ be the foundation model's point prediction for the price at time $t + \Delta t$, conditioned on the historical price window of length $\tau$.
* Let $A_t$ be the aggregate net trading action (net order volume) of the agent swarm at time $t$.
* Let $\frac{dP}{dt}$ represent the price impact dynamics governed by market microstructural resilience.

### 3.2 The Differential Equation
We model the price evolution as a coupled system where the observed price is a function of fundamental drift and agent-induced market impact:

$$\frac{dP}{dt} = \gamma(P^*(t) - P(t)) - k \cdot A_t$$

Where:
* $\gamma > 0$ is the mean-reversion rate of the market toward fundamental value $P^*(t)$.
* $k > 0$ is the price impact parameter scaling agent volume to price displacement.

The aggregate action $A_t$ is the weighted sum of individual agent decisions. Each agent $i$ evaluates the foundation model's forecast against the immediate past price:

$$A_t = \sum_{i=1}^{N} w_i \cdot \text{sign}\left( f_i(P_{[t-\tau, t]}) - P(t-\delta) \right)$$

Where:
* $N$ is the total number of agents in the swarm.
* $w_i$ is the capital allocation weight of agent $i$.
* $f_i$ is the foundation model instance utilized by agent $i$ (which may incorporate idiosyncratic agent-specific prompt engineering or feature transformations).
* $\delta$ is the inference and execution latency.

Assuming a linear approximation of the foundation model response such that $f_i(P_{[t-\tau, t]}) \approx P(t) + \beta_i \frac{dP}{dt}$, the closed-loop system governing the price perturbation $x(t) = P(t) - P^*(t)$ reduces to:

$$\frac{dx}{dt} = -\left( \gamma + k \sum_{i=1}^{N} w_i \beta_i \right) x(t)$$

### 3.3 The Stability Condition
Let $\alpha = k \sum_{i=1}^{N} w_i \beta_i$ represent the reflexive amplification coefficient. The characteristic equation of the feedback loop yields the stability criterion:

$$\text{Re}(\lambda) = -\gamma - \alpha$$

The system is **asymptotically stable** if and only if:

$$\gamma + k \sum_{i=1}^{N} w_i \beta_i > 0$$

When the foundation model exhibits strong trend-following behavior ($\beta_i > 0$) and market impact $k$ is sufficiently large such that $k \sum w_i \beta_i > \gamma$, the real part of the eigenvalue becomes positive ($\text{Re}(\lambda) > 0$). Under this condition, the system undergoes a **pitchfork bifurcation**, transitioning from a mean-reverting equilibrium to an **unstable, exponentially diverging positive-feedback loop**.

### 3.4 The Implications
1. **Low Impact Regime ($k \to 0$):** In deep, highly liquid markets, agent execution fails to move the price. $\alpha \approx 0$, and the system remains stable; agents act as passive price-takers.
2. **High Impact Regime ($k \gg 0$):** In thin, illiquid, or fragmented markets (e.g., small-cap equities, decentralized exchange liquidity pools), even modest capital allocations trigger significant price displacement, pushing the system past the stability boundary.
3. **Concentration Risk:** As $\sum w_i$ increases (representing larger swarm capital relative to market depth) or as models become more uniform ($\beta_i \to \beta$), the stability threshold is easily breached.

---

## 4. The Empirical Evidence

To validate the theoretical model, we conducted two controlled experiments using a multi-agent simulation framework built on the Quilt architecture.

### 4.1 The Historical Data Experiment
* **Configuration:** A swarm of 20 autonomous agents deployed on historical tick data for Apple Inc. (AAPL) across the 2020–2024 trading years.
* **Parameters:** Each agent utilized a localized instance of a 1B-parameter foundation time-series forecaster. Individual agent position sizes were capped at 0.05% of Average Daily Volume (ADV), resulting in a total swarm market share of $\approx 1.0\%$.
* **Result:** No reflexive behavior was observed. The price trajectory tracked the exogenous market series with negligible divergence. Cross-correlation between agent aggregate order flow and subsequent price returns remained bounded within statistical noise limits ($\rho \in [-0.04, 0.06]$).

### 4.2 The Synthetic Data Experiment
* **Configuration:** The same 20-agent swarm was deployed against a synthetic, mean-reverting stochastic price process with constrained baseline liquidity.
* **Intervention:** Agent trade execution sizes were artificially amplified by a factor of $100\times$, scaling total swarm participation to $\approx 200\%$ of local order book depth ($k$ was scaled proportionally).
* **Result:** Rapid, runaway reflexivity emerged within 45 simulation steps. The agents' combined buy orders drove the synthetic price upward by $340\%$. The foundation model ingested its own manufactured price spikes, predicting continued exponential growth and triggering continuous accumulation despite the underlying synthetic process remaining stationary. 

```
Price
  │                                           / (Divergence: Synthetic Reflexive Loop)
  │                                          /
  │                                         /
  │                                        /
  │   ────────────────────────────────────/── (Underlying Synthetic Mean)
  │  /
  └───────────────────────────────────────────────► Time
```

### 4.3 The Lesson
Real-world liquid markets maintain a sufficiently high resilience coefficient ($\gamma$) and low market impact parameter ($k$) to suppress baseline reflexivity under normal operational scales. However, synthetic environments, stress regimes, or high-capital deployments in illiquid sectors cross the bifurcation threshold rapidly. Foundation model reflexivity is not a theoretical abstraction; it is an emergent hazard scaling directly with relative capital concentration.

---

## 5. The Mitigations

To neutralize the reflexivity hazard in production deployments, we propose three architectural mitigations operating at the agent, execution, and system layers.

### 5.1 Heterogeneous Agents
Mitigating consensus-driven feedback requires breaking the homogeneity of inference ($\beta_i \neq \beta_j$).
* **Model Diversity:** Swarms must not rely on a single foundation architecture. Agents should be distributed across fundamentally different model families (e.g., transformer-based architectures like TimesFM, state-space models like Mamba-ts, and diffusion-based forecasters).
* **Feature Orthogonality:** Agents must ingest disparate feature engineering pipelines, using different temporal window sizes ($\tau_i \neq \tau_j$) and auxiliary indicators (macro-sentiment, order book imbalance, on-chain flows) to ensure low correlation in directional outputs.
* **Objective Diversity:** Avoid uniform reward functions. Mixing trend-following agents with mean-reversion, statistical arbitrage, and market-making objectives dampens directional amplification.

### 5.2 Randomized Execution
Deterministic, synchronized execution exacerbates step-function price impacts.
* **Execution Jitter:** Introduce stochastic execution delays ($\Delta t \sim \text{Exponential}(\lambda)$) across agents to smear order arrival times across the continuous spectrum rather than clustering at inference epoch boundaries.
* **Size Randomization:** Apply randomized perturbations to order sizes around the baseline model recommendation, preventing co-linear block ordering.
* **Iceberging and Partial Fills:** Decompose agent intents into randomized, randomized-sized child orders executed via hidden liquidity interfaces.

### 5.3 Explicit Loop-Breaking
Deterministic circuit breakers must override algorithmic autonomy when systemic divergence is detected.
* **Volatility Circuit Breakers:** Hard halt mechanisms that suspend agent swarm trading if the rolling price movement exceeds pre-defined statistical boundaries ($\Delta P > 5\%$ within a 1-hour window).
* **Position and Flow Caps:** Strict enforcement of maximum aggregate capital exposure relative to local ADV ($\sum w_i \cdot \text{ADV}^{-1} < 0.02$).
* **Velocity Limits:** Rate-limiting the aggregate order submission frequency of the swarm to allow market clearing mechanisms time to absorb liquidity shocks.

---

## 6. The Cell Architecture's Defenses

The Quilt cell-driven architecture provides native primitives designed to monitor, detect, and constrain distributed agent swarms.

### 6.1 Unique `quf://` URIs
Every inference artifact, model state, and agent intent within Quilt is addressed via a cryptographic Uniform Resource Identifier (`quf://`). 
* **Convergence Surveillance:** Because all agent forecasts are published to immutable cell logs, the CRDT (Conflict-Free Replicated Data Type) merge process continuously evaluates semantic convergence. 
* **State Intersection:** If multiple cell nodes report identical directional forecasts within a tight temporal window, the CRDT merge flags an elevated **Consensus Index**, signaling potential herd behavior before execution occurs.

### 6.2 Calibration Score
Quilt cells maintain an autonomous, real-time calibration score tracking the predictive error of resident models against realized market outcomes.
* **Loop Detection via Degradation:** When a reflexive loop initiates, the model's out-of-sample calibration score typically degrades rapidly because the price action is driven by self-referential feedback rather than fundamental economic reality.
* **Dynamic Throttling:** A sudden drop in the cell's calibration score automatically triggers a defensive reduction in capital allocation weights ($w_i$), throttling exposure until calibration recovers.

### 6.3 The CRDT as a Circuit Breaker
Conflict resolution in Quilt is decentralized. If concurrent writes to the state ledger indicate severe state divergence or conflicting swarm actions exceeding safety parameters, the CRDT reconciliation layer enters a conservative freeze state. Trading operations are suspended locally until consensus is re-established or manual operator intervention clears the merge barrier.

### 6.4 Necessary But Not Sufficient
It is critical to emphasize that the cell architecture's native defenses are **passive** (detection, logging, and circuit breaking post-facto). They provide the telemetry and emergency brakes required to limit blast radius. However, preventing reflexivity requires **active** architectural controls—specifically heterogeneous model mixing and randomized execution—implemented upstream of the cell runtime.

---

## 7. Related Work

* **Soros's Reflexivity:** Soros (1987) established the foundational macroeconomic theory of recursive feedback between market participants' biases and underlying economic fundamentals.
* **Positive Feedback in Finance:** Shleifer (2000) formalized limits to arbitrage, demonstrating how feedback loops and noise trader sentiment can drive prices far from fundamental values.
* **Algorithmic Market Impact:** Bouchaud et al. (2010) analyzed the microstructural mechanics of price impact, demonstrating how large meta-orders create temporary and permanent price shifts.
* **Foundation Model Safety:** Amodei et al. (2016) outlined concrete safety challenges in advanced AI deployments, including specification gaming and feedback amplification.
* **Multi-Agent Reinforcement Learning:** Lanctot et al. (2017) explored multi-agent pathologies, highlighting how independent learners frequently discover pathological coordination strategies in shared environments.

---

## 8. Limitations

While this paper provides a formal framework and empirical validation, several limitations must be noted:
1. **Model Simplification:** The differential equation models linear approximations of foundation model behavior; real-world foundation models exhibit non-linear attention mechanisms and multi-modal regime shifts.
2. **Synthetic Data Dependency:** The empirical verification of runaway reflexivity relies primarily on synthetic stress tests due to safety constraints governing live capital deployment in public markets.
3. **Incomplete Mitigation Coverage:** Not all proposed mitigations (e.g., dynamic multi-family model routing) are fully internalized within the current Quilt cell release.
4. **Market Asymmetry:** The reflexivity risk is heavily skewed toward low-liquidity domains (cryptocurrency altcoins, micro-cap equities) compared to deeply liquid macroeconomic benchmarks (FX majors, S&P 500).

---

## 9. Conclusion

The reflexivity problem represents a profound architectural risk for multi-agent systems leveraging foundation time-series forecasters. When swarm scale and market impact cross critical thresholds, models cease to predict reality and begin to manufacture it. 

While the Quilt cell-driven architecture provides robust passive defenses—including cryptographically unique `quf://` URIs, real-time calibration monitoring, and CRDT-based state reconciliation—these mechanisms must be complemented by active preventive measures such as model heterogeneity, execution jitter, and strict structural circuit breakers. Ensuring the stability of autonomous financial swarms requires treating reflexivity not as an anomaly, but as a fundamental physical property of closed-loop prediction systems.

---

### Abstract

When multiple agents use the same foundation time-series model on the same market, they can create a self-fulfilling feedback loop: the model predicts a price movement, the agents trade on the prediction, the trade moves the price, the price becomes input to the next prediction, and the prediction is reinforced. This reflexivity problem is similar to the Soros concept but is more tractable to formalize: it is a positive-feedback loop in a closed system. We describe the conditions under which the loop can arise, formalize the dynamics with a simple differential equation, and propose three mitigations: (1) heterogeneous agents (different models, different data), (2) randomized execution (delay, jitter, partial fills), and (3) explicit loop-breaking (circuit breakers, position limits). The cell-driven architecture has natural defenses against reflexivity: each agent's `quf://` URI is unique, the CRDT merge surfaces conflicts, and the cell's calibration score provides a real-time measure of the loop's effect. We show that a 20-agent swarm run on historical data does NOT exhibit reflexive behavior because the trades are too small to move the market. But on synthetic data where the agents' trades are amplified 100x, the loop emerges, and the system diverges from the underlying price. The lesson: foundation model reflexivity is a real risk for large-scale deployments, and the cell architecture's defenses are necessary but not sufficient.