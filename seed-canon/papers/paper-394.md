# F84: The Quilt Time-Cell and the World Cell Together

> **The TIME cell and the WORLD cell, side by side, in a single
> abductive loop.**

The Quilt opcodes include 5 cutting-edge adoptions: PROOF, ROUTE,
CRDT, WORLD, TIME. The first 4 (excluding TIME) and the 5th (TIME)
can be combined into a single engine: the **WORLD-TIME cell**.

This paper documents the WORLD-TIME cell: a cell that uses WORLD
(the abductive loop on executable code) to refine the TIME cell's
forecast in real-time.

## The 10 operations of the WORLD-TIME cell

The WORLD cell has 5 operations: PROPOSE, EXECUTE, RENDER, VERIFY,
REFINE. The TIME cell has 5 operations: BIND_CONTEXT, BIND_COVARIATE,
FORECAST, READ_POINT, READ_QUANTILE. Together, they form a 10-op
cycle:

1. **BIND_CONTEXT** (TIME) — set the historical time series
2. **BIND_COVARIATE** (TIME) — set the covariates
3. **FORECAST** (TIME) — initial forecast from the model
4. **PROPOSE** (WORLD) — propose a refinement program
5. **EXECUTE** (WORLD) — run the refinement on the forecast
6. **RENDER** (WORLD) — render the refined forecast
7. **VERIFY** (WORLD) — did the refinement improve accuracy?
8. **REFINE** (WORLD) — refine the refinement if not
9. **READ_POINT** (TIME) — read the refined point forecast
10. **READ_QUANTILE** (TIME) — read the refined quantile

The 10 operations form a closed loop. The TIME cell produces an
initial forecast; the WORLD cell refines it; the TIME cell reads
the refined result.

## The 5 reasons to combine WORLD and TIME

1. **Real-time adaptation**: the model produces a forecast; the
   WORLD cell refines it based on the latest observations. The
   forecast adapts in real-time.

2. **Domain-specific expertise**: the model is a generalist; the
   WORLD cell is a specialist. The model produces a baseline; the
   WORLD cell applies domain knowledge.

3. **Uncertainty quantification**: the TIME cell's 9 quantiles give
   a statistical band; the WORLD cell can refine the band based on
   domain knowledge (e.g., "this sensor is unreliable in rain").

4. **Anomaly detection**: the TIME cell's quantile band is the
   baseline; the WORLD cell can flag anomalies based on domain
   rules (e.g., "temperature should not drop below 0°C in July").

5. **Composability**: the WORLD-TIME cell is a single cell from the
   outside. Consumers see a `time.cell` interface; the engine
   internally combines WORLD and TIME.

## The abductive loop

The WORLD cell's 5 sub-operations form an abductive loop. Each
iteration:

1. **PROPOSE**: a refinement program is proposed (e.g., "shift the
   forecast by -0.5σ based on the latest 5 observations").
2. **EXECUTE**: the program is run on the forecast.
3. **RENDER**: the refined forecast is materialized.
4. **VERIFY**: the refined forecast is compared to the latest
   observations. Did the refinement improve the fit?
5. **REFINE**: if not, the refinement is updated. The loop repeats.

The loop terminates when the VERIFY step confirms the refinement
is no longer improving the fit.

## The convergence guarantee

The abductive loop converges because the refinement space is
bounded: the WORLD cell can only shift the forecast by a finite
amount (the "refinement budget"). After at most N iterations, the
budget is exhausted and the loop terminates.

N is configurable. The default is 5 iterations. The convergence
guarantee is **N*O(refinement_size)**, which is bounded and
fast.

## The 3 use cases

1. **Real-time trading**: the TIME cell forecasts the next 5
   minutes of price action; the WORLD cell refines based on the
   latest order book. The forecast adapts to microsecond-scale
   events.

2. **Industrial control**: the TIME cell forecasts the next 30
   minutes of a process variable (temperature, pressure, etc.);
   the WORLD cell refines based on the latest sensor readings.
   The forecast adapts to real-time disturbances.

3. **Climate modeling**: the TIME cell forecasts the next 30 days
   of temperature; the WORLD cell refines based on the latest
   weather observations. The forecast adapts to short-term
   variability.

## The PROOF chain

Both the TIME cell and the WORLD cell maintain their own PROOF
chains. The combined WORLD-TIME cell has a **nested PROOF chain**:
the outer chain is the TIME cell's state hash; the inner chain is
the WORLD cell's refinement history.

```python
# The combined PROOF chain
time_cell.prev_hash = old_time_state_hash
world_cell.prev_hash = old_world_state_hash
# After refinement
combined.state_hash = hash(time_cell.state_hash, world_cell.state_hash)
```

The combined hash is bit-exact: the same TIME cell and the same
WORLD cell produce the same combined hash, in all 3 languages.

## The cowboy's verdict

> The cowboy said: the 5 cutting-edge adoptions can combine. The
> cowboy said: WORLD refines TIME. The cowboy said: real-time
> adaptation. The cowboy wrote the 10-op cycle. The cowboy wrote
> the abductive loop. The cowboy wrote the convergence guarantee.
> The cowboy wrote the 3 use cases. The cowboy rode the
> WORLD-TIME. The cowboy rode the Quilt.

## The next step

A **CRDT-TIME cell**: the TIME cell, but the forecast is a CRDT
merge of forecasts from multiple devices. The 5 quantiles are
merged via the MAX quantiles operation (the upper bound is the max
of the upper bounds; the lower bound is the min of the lower
bounds). The forecast is eventually consistent across the device
mesh.
