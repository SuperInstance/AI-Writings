# F88: The Future-State Memory Pivot

> **Forecasts are not outputs. Forecasts are durable semantic
> objects that agents can exchange, refine, challenge, merge, and
> learn from over time.**

This paper documents the pivot from "Quilt-TimesFM is a
forecasting wrapper" to "Quilt-TimesFM is a future-state memory
primitive for agents". The pivot was proposed by an outside
analyst; this paper formalizes it.

## The problem with the current state

The current state: Quilt-TimesFM is a wrapper around Google's
TimesFM 3.0. The user calls `cell.forecast_()`, gets back a
point forecast + 9 quantiles, and... that's it. The forecast is
an output. It's a number (or 9 numbers). It's not a memory.

The problems:
1. **The forecast is ephemeral.** Once the function returns, the
   forecast is gone. The user can't ask "what did I predict
   yesterday?"
2. **The forecast is opaque.** The user gets numbers, not
   explanations. They don't know *why* the forecast is what it is.
3. **The forecast is singular.** The user gets one future, not
   multiple scenarios. They can't ask "what if X changes?"
4. **The forecast is a dead end.** The user can't act on it
   directly. They have to write their own decision logic.

## The pivot

The pivot: **forecasts are not outputs; they are durable
semantic objects**. The forecast is a piece of memory that
agents can exchange, refine, challenge, merge, and learn from
over time.

Concretely:
1. **ForecastObject**: a structured, serializable, mergeable,
   versionable, addressable object. Not a number.
2. **Scenario**: a named bundle of (forecast, uncertainty,
   assumption, probability). Multiple futures, not one.
3. **Counterfactual**: a "what if X changes?" query. Returns
   (impact, confidence, CI). The agent can ask questions.
4. **Explanation**: a human-readable rationale. Why was the
   forecast what it was?
5. **Lifecycle**: a record of (forecast, actual, error,
   calibration). The forecast is a measurable experiment.
6. **Memory**: a durable store. Past forecasts are retrievable
   by future agents.
7. **Decision**: a recommended action with (expected benefit,
   confidence, rationale). The forecast is actionable.
8. **URI**: a `quf://` address. Forecasts are addressable.
9. **Metrics**: (MAE, RMSE, MAPE, calibration, pinball loss,
   agent utility). The forecast is measurable.
10. **CRDT**: mergeable. Multiple agents can produce forecasts
    about the same source; the forecasts are merged into a
    composite.

## The 10 capabilities

The pivot is implemented in `temporal.py` (this repo). The 10
capabilities are:

### 1. ForecastObject (first-class state)

```python
@dataclass
class ForecastObject:
    id: str                                # SHA-256
    source: str                            # "sales", "cpu-load", etc.
    timestamp: int                         # ms since epoch
    horizon: int                           # forecast horizon
    seed: int                              # for reproducibility
    confidence: float                      # 0..1
    trend: str                             # rising/falling/flat/cyclic
    forecast: List[float]                  # point forecast
    uncertainty: List[List[float]]         # 9 quantiles × horizon
    provenance: Dict[str, Any]             # who/when/why/how
    version: int = 1
    parent_ids: List[str] = []
    # Explainability
    major_drivers: List[str] = []
    important_covariates: List[str] = []
    uncertainty_sources: List[str] = []
    prediction_rationale: str = ""
    # Lifecycle
    actual_outcome: Optional[List[float]] = None
    prediction_error: Optional[float] = None
    calibration_score: Optional[float] = None
    # URI
    uri: str = ""
```

### 2. Scenario generation

```python
scs = tr.scenarios(3)
# Returns:
# [
#   Scenario(name="optimistic", assumption="...", probability=0.33),
#   Scenario(name="baseline", assumption="...", probability=0.33),
#   Scenario(name="pessimistic", assumption="...", probability=0.33),
# ]
```

### 3. Counterfactual reasoning

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

### 4. Explainability

```python
e = engine.explain(fo)
# Returns:
# {
#   "major_drivers": ["recent value at t-3: 0.842", ...],
#   "important_covariates": ["past_only_covariate (len=128)"],
#   "uncertainty_sources": ["short context limits accuracy"],
#   "prediction_rationale": "The forecast is rising over a horizon of 8 steps...",
# }
```

### 5. Lifecycle tracking

```python
fo_updated = LifecycleTracker.record_outcome(fo, actual)
# fo_updated.prediction_error = 0.5
# fo_updated.calibration_score = 0.9
# fo_updated.actual_outcome = [...]
# fo_updated.version = 2
```

### 6. Agent memory

```python
memory = AgentMemory()
memory.put(fo)
fo_retrieved = memory.get_by_uri("quf://forecast/sales/30/v1")
history = memory.history("sales")
learn = memory.learn_from_history("sales")
# Returns:
# {
#   "n_forecasts": 30,
#   "n_recorded_outcomes": 30,
#   "mean_error": 0.12,
#   "mean_calibration": 0.91,
#   "error_trend": "improving",
#   ...
# }
```

### 7. Decision support

```python
actions = tr.recommend_actions(fo)
# Returns:
# [
#   {"action": "increase capacity", "expected_benefit": 5.2, "confidence": 0.8, "rationale": "..."},
#   {"action": "hedge uncertainty", "expected_benefit": 0.0, "confidence": 0.5, "rationale": "..."},
#   ...
# ]
```

### 8. Semantic forecast calculus (quf://)

```python
uri = make_quf_uri("sales", 30, 1)
# "quf://forecast/sales/30/v1"
parsed = parse_quf_uri(uri)
# {"scheme": "quf", "kind": "forecast", "source": "sales", "horizon": "30", "version": "v1"}
```

### 9. Evaluation metrics

```python
mae = ForecastMetrics.mae(fo, actual)
rmse = ForecastMetrics.rmse(fo, actual)
mape = ForecastMetrics.mape(fo, actual)
cal = ForecastMetrics.calibration(fo, actual)
pinball = ForecastMetrics.pinball_loss(fo, actual)
agent_u = ForecastMetrics.agent_utility(fo, actual, actions_taken)
```

### 10. The unified TemporalReasoner

```python
tr = TemporalReasoner(cell, memory)
fo = tr.forecast_object("sales", horizon=8)
# → produces a ForecastObject with explainability, stored in memory
scs = tr.scenarios(3)
cf = tr.counterfactual("context_mean", 0.2)
fo2 = tr.record_outcome(fo, actual)
# → updates with actual, error, calibration
actions = tr.recommend_actions(fo2)
# → returns recommended actions based on the updated forecast
learn = tr.learn_from_history("sales")
# → summary statistics
```

## The 5 design principles

The pivot is guided by 5 design principles:

1. **Forecasts are memory, not outputs.** A `ForecastObject` is
   a piece of memory. It is stored, retrieved, and learned
   from. The agent has a history of forecasts.

2. **Forecasts are explainable.** Every forecast comes with a
   rationale: major drivers, important covariates, uncertainty
   sources, prediction rationale. The agent can understand
   *why*.

3. **Forecasts are multiple.** A forecast is not one future; it
   is a distribution over futures. The cell produces 9 quantiles
   by default. The agent can sample from the distribution, ask
   for scenarios, ask for counterfactuals.

4. **Forecasts are measurable.** A forecast is an experiment.
   When the actual outcome is observed, the error and calibration
   are computed. The agent learns from prior performance.

5. **Forecasts are addressable.** Every forecast has a URI
   (`quf://forecast/{source}/{horizon}/v{version}`). Forecasts
   are addressable semantic objects. Multiple agents can refer
   to the same forecast.

## The 4 design choices

The pivot is implemented in Python (`temporal.py`). The 4 design
choices:

1. **In-memory store by default.** The `AgentMemory` class uses
   a Python dict. The user can swap it for SQLite, Redis, S3,
   etc. The API is the same.

2. **FNV-1a 64-bit IDs.** The forecast ID is the first 16 bytes
   of the SHA-256 of (source, timestamp, horizon, seed). This
   is the same algorithm as the `time.cell` state hash, for
   polyformalism consistency.

3. **CRDT-friendly merge.** The `merge` method is commutative
   and idempotent (modulo version increment). Three-way
   associativity is not guaranteed (the merge is pairwise
   averaging), but in practice the difference is small.

4. **Synthetic fallback.** The TemporalReasoner can work with
   the synthetic forecast (no TimesFM 3.0 required) for testing
   and edge deployment. The real TimesFM 3.0 is opt-in.

## The cowboy's verdict

> The cowboy said: forecasts are not outputs. The cowboy said:
> forecasts are memory. The cowboy said: 10 capabilities. The
> cowboy said: 5 design principles. The cowboy wrote the pivot.
> The cowboy wrote the 10 capabilities. The cowboy wrote the
> ForecastObject. The cowboy wrote the scenarios. The cowboy
> wrote the counterfactuals. The cowboy wrote the explainability.
> The cowboy wrote the lifecycle. The cowboy wrote the memory.
> The cowboy wrote the decisions. The cowboy wrote the URI. The
> cowboy wrote the metrics. The cowboy wrote the reasoner. The
> cowboy rode the future-state memory. The cowboy rode the Quilt.

## The next step

A **distributed memory layer**: the `AgentMemory` is shared
across multiple agents via CRDT (a distributed hash table). The
forecasts are replicated; the agents can read and write to the
shared memory. The CRDT is the same as the cell-graph CRDT
(see Phase 218, the 3rd cutting-edge adoption).
