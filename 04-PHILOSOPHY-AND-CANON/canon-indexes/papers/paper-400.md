# F90: The Agent Utility Metric

> **Forecast accuracy is not enough. We need to measure how
> useful the forecast is to the agent.**

This paper documents the `agent_utility` metric, a new evaluation
metric for forecasts. The metric captures not just predictive
accuracy but the **utility of the forecast to the agent's
decision-making**.

## The problem with accuracy-only metrics

The standard metrics (MAE, RMSE, MAPE, calibration, pinball
loss) measure **predictive accuracy**: how close the forecast
is to the actual. But a forecast can be accurate and still
not useful to the agent.

Example: a forecast of "CPU load will be 50% over the next 8
hours" is accurate if the actual CPU load is 50%. But the
forecast is not useful if the agent needs to know "will the CPU
load exceed 90%?" (which would require scaling up).

A better metric captures **the utility of the forecast to the
agent's decision**. The agent utility metric is:

```
agent_utility = -MAE + 0.5 * (1 - |calibration - 0.9|) + 0.3 * n_actions
```

Where:
- `MAE` is the mean absolute error (lower is better)
- `calibration` is the fraction of actuals in the 90% CI
  (target: 0.9; deviation from 0.9 is bad)
- `n_actions` is the number of recommended actions (more
  actions = more utility, up to a point)

## The 4 components

### 1. -MAE (negative mean absolute error)

The first component is the negative MAE. A perfect forecast
(MAE=0) gives +0; a forecast with MAE=1.0 gives -1.0. The
metric rewards accuracy.

### 2. (1 - |calibration - 0.9|) × 0.5

The second component is the calibration quality. A perfectly
calibrated forecast (calibration = 0.9) gives +0.5. An
over-confident forecast (calibration = 1.0) gives
+0.5 * (1 - 0.1) = +0.45. An under-confident forecast
(calibration = 0.5) gives +0.5 * (1 - 0.4) = +0.30. The metric
rewards calibration around the 90% target.

### 3. 0.3 * n_actions

The third component is the number of recommended actions. Each
action adds +0.3 to the utility. This rewards the agent for
producing actionable forecasts.

### 4. Combined

The combined metric is the sum. A forecast with MAE=0.1,
calibration=0.9, and 2 actions gives:
```
agent_utility = -0.1 + 0.5 * (1 - 0) + 0.3 * 2 = -0.1 + 0.5 + 0.6 = 1.0
```

A perfect forecast (MAE=0, calibration=0.9, 2 actions) gives
+1.1. A bad forecast (MAE=1.0, calibration=0.5, 0 actions) gives
-1.0 + 0.3 + 0 = -0.7.

## The 4 properties

### 1. Bounded

The agent utility is bounded. The minimum is -∞ (a perfectly
wrong forecast with no calibration). The maximum is +∞ (a
perfectly accurate forecast with maximum actions).

In practice, the metric is in the range [-MAE_max, 0.5 + 0.3 * n_actions_max].
For typical forecasts, the range is [-2.0, +2.0].

### 2. Actionable

The metric rewards forecasts that lead to actions. A forecast
with high accuracy but no actions is less useful than a forecast
with slightly lower accuracy but actionable.

### 3. Calibrated

The metric rewards calibration around the 90% target. Over-
and under-confident forecasts are penalized.

### 4. Differentiated

The metric distinguishes between forecasts that are equally
accurate but differently useful. A forecast with MAE=0.5 and
5 actions is more useful than a forecast with MAE=0.5 and 0
actions.

## The 4 use cases

### 1. Comparing two forecast models

The agent has two forecast models: A (MAE=0.1, calibration=0.9,
0 actions) and B (MAE=0.2, calibration=0.9, 3 actions). The
accuracy-only metric says A is better. The agent utility metric
says B is better (more actionable). The agent uses B.

### 2. Tuning the forecast horizon

The agent tunes the forecast horizon. Short horizons (1-4
steps) give low MAE but few actions. Long horizons (16-32
steps) give high MAE but more actions. The agent finds the
horizon that maximizes agent utility.

### 3. Evaluating the value of additional data

The agent has a choice: gather more data (cost: 100 units) or
keep the current forecast. The agent uses the metric to
estimate the change in agent utility from the additional data.
If the change in agent utility is > 100, gather the data.

### 4. Comparing decision policies

The agent has two decision policies: A (cautious) and B
(aggressive). Policy A recommends fewer actions (lower utility)
but with higher confidence. Policy B recommends more actions
(higher utility) but with lower confidence. The agent uses
the metric to compare the two policies.

## The 4 design choices

### 1. The 0.5 weight on calibration

The weight 0.5 on calibration is arbitrary. A different weight
(e.g., 0.3) would emphasize accuracy over calibration. The
weight should be tuned to the application.

### 2. The 0.3 weight on actions

The weight 0.3 on actions is arbitrary. A different weight
(e.g., 0.1) would emphasize accuracy over actionability. The
weight should be tuned to the application.

### 3. The 0.9 calibration target

The 90% calibration target is conventional in forecasting. A
different target (e.g., 0.5 for the median) would change the
metric. The target should match the agent's risk tolerance.

### 4. The MAE loss function

The MAE loss function is conventional. RMSE would penalize
outliers more; MAPE would penalize relative errors. The loss
function should match the application's error cost.

## The 4 future directions

### Direction 1: Domain-specific utility

The metric is currently domain-agnostic. A domain-specific
metric would weight the components differently for each
application. For example, in healthcare, calibration is
more important than in marketing. The metric should be
tunable per application.

### Direction 2: Long-horizon utility

The metric currently rewards short-horizon forecasts (low
MAE). A long-horizon utility metric would reward forecasts
that give the agent more lead time. The metric should
include a horizon-aware component.

### Direction 3: Counterfactual utility

A new component that rewards counterfactuals. The metric
should include a term for `n_counterfactuals` (the number
of counterfactuals the agent can ask). Counterfactuals
are valuable for decision-making.

### Direction 4: Multi-agent utility

The metric currently measures single-agent utility. A
multi-agent metric would measure the utility of the forecast
across multiple agents (e.g., a forecast that benefits 5
agents is more useful than one that benefits 1).

## The cowboy's verdict

> The cowboy said: agent utility is a first-class metric. The
> cowboy said: accuracy is not enough. The cowboy said: 4
> components. The cowboy said: 4 properties. The cowboy said:
> 4 use cases. The cowboy said: 4 design choices. The cowboy
> said: 4 future directions. The cowboy wrote the agent
> utility metric. The cowboy rode the agent utility. The
> cowboy rode the Quilt.

## The next step

A **utility-driven forecast optimizer** that maximizes agent
utility, not just accuracy. The optimizer tunes the forecast
horizon, the calibration target, and the action thresholds
to maximize the metric. The optimizer is implemented in
`examples/10_utility_optimizer.py` (Phase 230+).
