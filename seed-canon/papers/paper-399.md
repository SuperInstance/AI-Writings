# F89: Counterfactual Reasoning for Agents

> **"What happens if X changes?" is the most important question
> an agent can ask.**

This paper documents the counterfactual reasoning capability of
the Quilt `time.cell`. The agent can ask "what happens if X
changes?" about any variable in the time series, and the cell
returns the projected impact + confidence bounds.

## The 4 counterfactual variables

The cell supports 4 counterfactual variables:

| Variable | What it changes | Use case |
|---|---|---|
| `context_mean` | shift the context by delta*mean | "what if the world average rises 20%?" |
| `context_trend` | amplify/reduce the linear trend | "what if the trend accelerates 15%?" |
| `context_volatility` | scale the deviations from mean | "what if volatility increases 30%?" |
| `horizon` | change the forecast horizon | "what if we forecast 50% further?" |

The agent calls `forecast.counterfactual(variable, delta)`:

```python
cf = tr.counterfactual("context_mean", 0.20)
# Returns:
# {
#   "variable": "context_mean",
#   "delta": 0.20,
#   "impact_mean": 0.34,
#   "impact_total": 0.50,
#   "ci_low": 0.12,
#   "ci_high": 0.56,
#   "baseline_sum": 100.0,
#   "counterfactual_sum": 100.5,
#   "confidence": 0.80,
# }
```

## The 4 properties of counterfactual reasoning

### 1. Composability

Counterfactuals compose. The agent can ask:

```python
cf1 = tr.counterfactual("context_mean", 0.20)
cf2 = tr.counterfactual("context_volatility", 0.30)
# Both compose: the world is shifted by 20% AND volatility is up 30%
```

The composition is **additive in impact, multiplicative in CI**.
The total impact is `cf1.impact + cf2.impact`; the total CI is
the union of the CIs (wider).

### 2. Confidence decreases with delta

Counterfactuals are less confident the further we extrapolate.
The cell returns `confidence = max(0, 1 - |delta|)`. For
delta=0, confidence=1.0. For delta=1.0, confidence=0.0. The
agent uses the confidence to weight the decision.

### 3. Bounds from the 9 quantiles

The counterfactual returns `ci_low` and `ci_high` (the 10th and
90th percentiles of the projected impact). The agent uses these
to plan for the worst case (10th percentile) and best case (90th
percentile).

### 4. Reproducibility

Counterfactuals are reproducible given a seed. The cell hashes
the (context, variable, delta, seed) tuple and produces a
deterministic forecast. The agent can re-run the same
counterfactual and get the same result.

## The 5 use cases

### 1. Marketing budget

The agent asks: "what if we increase marketing spend by 20%?"
The cell returns the projected impact on revenue. The agent
uses the impact + confidence to decide on the marketing budget.

### 2. Inventory management

The agent asks: "what if demand increases by 30%?" The cell
returns the projected impact on stockouts. The agent uses
the impact + CI to plan inventory levels.

### 3. Capacity planning

The agent asks: "what if traffic grows 15% over the next
quarter?" The cell returns the projected impact on server load.
The agent uses the impact + CI to plan capacity.

### 4. Pricing

The agent asks: "what if we raise prices by 5%?" The cell
returns the projected impact on sales volume. The agent uses
the impact + CI to decide on pricing.

### 5. Risk management

The agent asks: "what if volatility doubles?" The cell returns
the projected impact on the 90% CI width. The agent uses the
impact + CI to decide on hedging.

## The 4 design choices

### 1. Single-variable counterfactuals

The cell supports single-variable counterfactuals (one variable
at a time). Multi-variable counterfactuals (multiple variables
changed simultaneously) are computed by composing single-variable
counterfactuals. The composition is additive in impact,
multiplicative in CI.

### 2. Linear perturbations

The cell supports linear perturbations: shift by `delta * mean`,
amplify trend by `delta * trend`, scale volatility by
`1 + delta`. Non-linear perturbations (e.g., seasonal changes)
are not supported in this version.

### 3. Bounded extrapolation

The cell returns confidence = max(0, 1 - |delta|). For
|delta| > 1.0, the cell returns 0 confidence and the agent
should treat the counterfactual as unreliable.

### 4. CRDT-friendly

Counterfactuals are **local**: the cell produces them without
network access. Multiple agents can produce counterfactuals
about the same source; the counterfactuals can be merged via
the `ForecastObject.merge` method.

## The 4 future directions

### Direction 1: Multi-variable counterfactuals

A cell that supports `forecast.counterfactual([(var1, delta1),
(var2, delta2), ...])`. The cell computes the joint impact and
the joint CI. The agent can ask "what if X AND Y change?".

### Direction 2: Non-linear counterfactuals

A cell that supports non-linear perturbations: `delta_function`
(staircase), `delta_seasonal` (add a seasonal component),
`delta_shock` (add a step change). The agent can ask "what if
there's a shock to the system?".

### Direction 3: Conditional counterfactuals

A cell that supports `forecast.counterfactual_conditional(
variable, delta, condition)`. The cell computes the counterfactual
only when the condition is met. The agent can ask "what if X
changes, *given* that Y is in state Z?".

### Direction 4: Counterfactual trees

A cell that produces a **counterfactual tree**: a tree of
counterfactuals where each branch is a different scenario.
The agent can walk the tree to find the best action.

## The cowboy's verdict

> The cowboy said: "what if X changes?" is the most important
> question. The cowboy said: 4 variables. The cowboy said:
> 4 properties. The cowboy said: 5 use cases. The cowboy said:
> 4 design choices. The cowboy said: 4 future directions. The
> cowboy wrote the counterfactual. The cowboy rode the
> counterfactual. The cowboy rode the Quilt.

## The next step

A **counterfactual engine** that uses the cell's counterfactual
reasoning + decision support to find the best action. The
agent asks "what should I do?", the engine enumerates a set of
candidate actions, runs counterfactuals for each, and returns
the action with the highest expected utility. The engine is
implemented in `examples/09_counterfactual_engine.py` (Phase 230+).
