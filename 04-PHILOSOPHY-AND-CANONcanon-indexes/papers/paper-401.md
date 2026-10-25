# F91: The Temporal Reasoner

> **The unified primitive that turns forecasting into future-state
> memory.**

This paper documents the `TemporalReasoner` class, the unified
entry point for the Quilt-TimesFM future-state memory pivot.
The reasoner combines all 10 capabilities into a single
class: forecasting, scenarios, counterfactuals, explainability,
lifecycle, memory, decisions, URI, metrics, and CRDT.

## The class

```python
class TemporalReasoner:
    def __init__(self, cell: TimeCell, memory: Optional[AgentMemory] = None):
        self.cell = cell
        self.memory = memory or AgentMemory()
        self.explainer = ExplainabilityEngine(cell)
        self.decision = DecisionSupport(self.memory)
        self.metrics = ForecastMetrics()

    def forecast_object(self, source, horizon=16, seed=0) -> ForecastObject:
        """Produce a ForecastObject from the cell's current context."""

    def scenarios(self, n: int = 3) -> List[Scenario]:
        """Generate multiple future scenarios (optimistic/baseline/pessimistic)."""

    def counterfactual(self, variable: str, delta: float) -> Dict[str, Any]:
        """What-if analysis."""

    def record_outcome(self, forecast: ForecastObject, actual: List[float]) -> ForecastObject:
        """Record the actual outcome and update error/calibration."""

    def recommend_actions(self, forecast: ForecastObject) -> List[Dict[str, Any]]:
        """Recommend actions based on the forecast."""

    def learn_from_history(self, source: str) -> Dict[str, Any]:
        """Summary statistics: mean error, mean calibration, trend."""

    def get(self, forecast_id: str) -> Optional[ForecastObject]:
        """Retrieve a forecast by ID."""

    def history(self, source: str) -> List[ForecastObject]:
        """All forecasts for a given source, oldest first."""
```

## The 8 methods

### 1. forecast_object

Produces a `ForecastObject` from the cell's current context.
The cell must have a context (bind_context already called).

```python
fo = tr.forecast_object("sales", horizon=8)
# Returns a ForecastObject with:
# - id, source, timestamp, horizon, seed
# - confidence, trend, forecast, uncertainty
# - major_drivers, important_covariates, uncertainty_sources, prediction_rationale
# - uri (quf://forecast/sales/8/v1)
# - automatically stored in memory
```

### 2. scenarios

Generates multiple future scenarios.

```python
scs = tr.scenarios(3)
# Returns a list of 3 Scenario objects:
# - optimistic: assumption="favorable conditions: trend amplified 1.2x, no shocks"
# - baseline: assumption="current conditions continue: status quo"
# - pessimistic: assumption="adverse conditions: trend reduced 0.8x, +1σ noise"
```

### 3. counterfactual

What-if analysis.

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
#   "confidence": 0.80,
# }
```

### 4. record_outcome

Records the actual outcome and updates the forecast.

```python
fo_updated = tr.record_outcome(fo, actual)
# fo_updated.prediction_error = 0.5
# fo_updated.calibration_score = 0.9
# fo_updated.actual_outcome = actual
# fo_updated.version = fo.version + 1
# fo_updated is stored in memory
```

### 5. recommend_actions

Recommends actions based on the forecast.

```python
actions = tr.recommend_actions(fo)
# Returns a list of action dicts:
# [
#   {"action": "increase capacity", "expected_benefit": 5.2, "confidence": 0.8, "rationale": "..."},
#   {"action": "hedge uncertainty", "expected_benefit": 0.0, "confidence": 0.5, "rationale": "..."},
# ]
```

### 6. learn_from_history

Summary statistics for a given source.

```python
learn = tr.learn_from_history("sales")
# Returns:
# {
#   "source": "sales",
#   "n_forecasts": 30,
#   "n_recorded_outcomes": 30,
#   "mean_error": 0.12,
#   "mean_calibration": 0.91,
#   "error_trend": "improving",
#   "calibration_trend": "stable",
# }
```

### 7. get

Retrieves a forecast by ID.

```python
fo = tr.get(forecast_id)
```

### 8. history

Returns all forecasts for a given source, oldest first.

```python
hist = tr.history("sales")
# Returns a list of ForecastObject, oldest first
```

## The 5 internal components

The reasoner composes 5 internal components:

### 1. TimeCell

The cell provides the forecast substrate (TimesFM 3.0 in Python,
synthetic in tests). The reasoner calls `cell.forecast_()` and
reads the result via `cell.read_point(0)` and `cell.read_quantile(q, 0)`.

### 2. AgentMemory

The memory stores `ForecastObject`s. The reasoner puts every
forecast in memory and retrieves them on demand.

### 3. ExplainabilityEngine

The explainer produces human-readable explanations for forecasts.
The reasoner calls it on every `forecast_object` to populate the
`major_drivers`, `important_covariates`, `uncertainty_sources`,
and `prediction_rationale` fields.

### 4. DecisionSupport

The decision engine produces action recommendations. The reasoner
calls it on `recommend_actions`.

### 5. ForecastMetrics

The metrics class computes MAE, RMSE, MAPE, calibration, pinball
loss, and agent utility.

## The 4 use cases

### 1. Production agent

A production agent uses the reasoner to:
1. Bind context to the cell.
2. Forecast (forecasting).
3. Store the forecast in memory.
4. Recommend actions.
5. Take the action.
6. Record the outcome.
7. Learn from the outcome.

The agent runs this loop forever, getting better over time.

### 2. Research agent

A research agent uses the reasoner to:
1. Bind context to the cell.
2. Forecast (forecasting).
3. Generate scenarios (what if?).
4. Run counterfactuals (what if X changes?).
5. Compare scenarios.
6. Pick the best one.

The agent runs this once per decision.

### 3. Backtester

A backtester uses the reasoner to:
1. Bind historical context.
2. Forecast the next N steps.
3. Compare to actuals.
4. Compute metrics (MAE, RMSE, MAPE, calibration, pinball loss, agent utility).

The agent runs this on historical data to evaluate the cell.

### 4. World model

A world model uses the reasoner to:
1. Bind the world state to the cell.
2. Forecast the next state.
3. Use the forecast to plan an action.
4. Take the action.
5. Observe the new world state.
6. Repeat.

The agent runs this loop continuously, modeling the world.

## The 4 design choices

### 1. Single-cell reasoner

The reasoner is built around a single `TimeCell`. Multiple
reasoners can be composed for multi-cell scenarios (e.g., one
reasoner per source).

### 2. In-memory by default

The `AgentMemory` is in-memory by default. The user can swap
it for SQLite, Redis, S3, etc. The API is the same.

### 3. Synthetic fallback

The reasoner can work with the synthetic forecast (no TimesFM
3.0 required) for testing and edge deployment. The real
TimesFM 3.0 is opt-in.

### 4. CRDT-friendly

Every `ForecastObject` is CRDT-friendly: it has an ID, a
version, a parent ID list, and a `merge` method. Multiple
agents can produce forecasts about the same source; the
forecasts can be merged.

## The 4 future directions

### Direction 1: Multi-cell reasoner

A reasoner that wraps multiple cells. The reasoner picks the
best cell for each source, forecasts, and merges the results.

### Direction 2: Hierarchical reasoner

A reasoner that operates at multiple timescales (per-frame,
per-second, per-minute, per-hour, per-day). The reasoner
combines the forecasts at each level.

### Direction 3: Cross-modal reasoner

A reasoner that operates on multiple modalities (text, audio,
video, scalars). The reasoner produces a unified forecast.

### Direction 4: Distributed reasoner

A reasoner that runs across multiple processes. The memory is
shared via CRDT. The reasoner can be scaled horizontally.

## The cowboy's verdict

> The cowboy said: the unified primitive. The cowboy said: 8
> methods. The cowboy said: 5 components. The cowboy said: 4
> use cases. The cowboy said: 4 design choices. The cowboy
> said: 4 future directions. The cowboy wrote the reasoner.
> The cowboy rode the reasoner. The cowboy rode the Quilt.

## The next step

A **decentralized agent network** where multiple reasoners
share their forecasts via CRDT. Each reasoner produces
forecasts for its sources; the network merges them into a
global memory. The network is implemented in
`examples/11_decentralized_network.py` (Phase 230+).
