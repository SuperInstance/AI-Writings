# F86: The Quilt Time-Cell Adoption Manual

> **A step-by-step guide to adopting `time.cell` in your application.**

The Quilt `time.cell` cell kind is the easiest way to add
state-of-the-art time-series forecasting to any application. This
paper is the adoption manual: a step-by-step guide for the
developer who wants to use `time.cell` in production.

## Step 1: Choose your L-tier

The first decision is **which L-tier** to use:

| Tier | Target | Substrate | Use case |
|---|---|---|---|
| L0 | Cortex-M0+ | synthetic | ultra-low-power sensor nodes |
| L1 | Cortex-M4 | synthetic | industrial sensors, wearables |
| L2 | ESP32-S3 | synthetic | smart-home, edge AI gateways |
| L3 | Workstation | real TimesFM 3.0 | research, production |

For most applications, **L3** is the right choice: the real TimesFM
3.0 gives SOTA accuracy on 3 major benchmarks. For embedded
applications, choose the tier that matches your hardware.

## Step 2: Install the cell

For **L3** (Python):

```bash
pip install quilt-timesfm
# Or, for the latest from the repo:
git clone https://github.com/SuperInstance/quilt-timesfm
cd quilt-timesfm
pip install -e .
```

For **L0-L2** (Rust, no_std):

```toml
# Cargo.toml
[dependencies]
quilt-timesfm = "0.1"
```

For **L2** (C, kernel):

```c
#include <quilt/time.h>
```

## Step 3: Build the cell

```python
# Python (L3)
from quilt_cell import TimeCell

cell = TimeCell()  # default: real TimesFM 3.0
print(cell.kind_name())  # "time.cell"
print(cell.kind_count())  # 5
```

```rust
// Rust (L0-L2)
use quilt_timesfm::TimeCell;

let mut cell = TimeCell::new();
assert_eq!(&cell.kind_name()[..9], b"time.cell");
```

```c
// C (L2)
quilt_time_cell_t cell = quilt_time_cell_new();
printf("%s\n", cell.kind_name);  // "time.cell"
```

The cell is **bit-exact** across all 3 languages. Same kind, same
operations, same hash.

## Step 4: BIND_CONTEXT

The first operation is **BIND_CONTEXT**: set the historical time
series.

```python
# Python
import numpy as np
context = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
cell.bind_context(context)
```

```rust
// Rust
let context = [1.0, 2.0, 3.0, 4.0, 5.0];
cell.bind_context(&context).unwrap();
```

The context is a 1D (or 2D, for multivariate) float array. The cell
hashes it (FNV-1a 64-bit, 32 bytes) and saves the prev_hash (PROOF
chain).

## Step 5: BIND_COVARIATE (optional)

If you have covariates (e.g., trading volume, day of week,
temperature), **BIND_COVARIATE** tells the cell about them.

```python
# Python
covariate = np.array([10.0, 20.0, 30.0])
cell.bind_past_only_covariate(covariate)  # for past-only covariates
# or
cell.bind_past_future_covariate(covariate)  # for known future events
```

Covariates improve the forecast accuracy. The cell uses them
internally; the user doesn't need to know how.

## Step 6: Set the horizon

The **horizon** is how many time steps to forecast. The cell
supports horizons from 1 to 16,384.

```python
# Python
cell.set_horizon(16)  # forecast 16 steps ahead
```

```rust
// Rust
cell.set_horizon(16).unwrap();
```

For real-time applications, the horizon is typically small (1-100).
For research, the horizon can be large (1000+).

## Step 7: FORECAST

The **FORECAST** operation runs the model and produces a forecast
+ 9 quantiles.

```python
# Python
cell.forecast_()  # calls real TimesFM 3.0
```

The forecast is stored in the cell. The user can read it via
READ_POINT and READ_QUANTILE.

## Step 8: READ_POINT and READ_QUANTILE

The **READ_POINT** operation reads the point forecast (the median
quantile). The **READ_QUANTILE** operation reads a specific
quantile prediction interval.

```python
# Python
point = cell.read_point(0)  # variate 0
q90 = cell.read_quantile(0.9, 0)  # 90% upper bound
q10 = cell.read_quantile(0.1, 0)  # 10% lower bound
```

The 9 quantiles give 9 levels of uncertainty. The user can pick the
one that matches their decision-making posture.

## Step 9: Use the forecast

The forecast can be used in many ways:

- **Plot it**: see `examples/01_temperature.py`
- **Trade on it**: see `examples/02_stock.py`
- **Plan capacity**: see `examples/03_demand.py`
- **Detect anomalies**: see `examples/04_anomaly.py`
- **Fuse sensors**: see `examples/05_multivariate.py`

The cell is a building block. The user composes it with their
domain logic.

## Step 10: Iterate

Forecasting is iterative. The cell supports re-binding:

```python
# Re-bind with new data
new_context = np.array([6.0, 7.0, 8.0])
cell.bind_context(new_context)
cell.forecast_()
```

Each BIND_CONTEXT invalidates the previous forecast (the prev_hash
is preserved, the forecast is cleared). The new forecast is
independent of the old.

## The 5 production tips

1. **Cache the model**. The real TimesFM 3.0 takes 1.5GB of RAM.
   Don't load it for every forecast; cache it as a singleton.

2. **Use the right horizon**. The model's accuracy drops with longer
   horizons. For real-time, use horizons of 1-100. For research,
   use longer horizons but be aware of the accuracy drop.

3. **Watch the quantiles**. If the 90% band is too wide, the
   forecast is uncertain. If too narrow, the model is overconfident.
   The right band width depends on the application.

4. **Re-bind frequently**. The model is most accurate on recent
   data. Re-bind every time you get new observations.

5. **Combine with WORLD**. The WORLD cell can refine the TIME
   cell's forecast in real-time. See `paper-394` (F84) for the
   WORLD-TIME cell.

## The cowboy's verdict

> The cowboy said: adoption in 10 steps. The cowboy said: choose
> your tier. The cowboy said: install. The cowboy said: BIND,
> FORECAST, READ. The cowboy said: 5 production tips. The cowboy
> wrote the manual. The cowboy rode the 10 steps. The cowboy rode
> the Quilt.

## The next step

A **production deployment guide**: a step-by-step guide to deploying
the Quilt time cell in production at scale. Topics include:
model serving (TorchServe, Triton, BentoML), batching, caching,
monitoring, A/B testing, and rollback. The guide covers
single-machine deployment, distributed deployment, and edge
deployment.
