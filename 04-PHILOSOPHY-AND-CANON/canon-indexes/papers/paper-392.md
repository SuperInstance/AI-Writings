# F82b: The Quilt Time-Cell on Bare Metal

> **The 4 L-tiers of the `time.cell`, from Cortex-M0+ to workstation.**

The Quilt `time.cell` cell kind runs everywhere from the smallest
microcontroller to the largest GPU server. This paper documents the
4 L-tiers of capability.

## The 4 L-tiers

| Tier | Target | RAM | Substrate | Build time |
|---|---|---|---|---|
| **L0** | Cortex-M0+ (e.g., SAMD21) | 4KB | synthetic | 1 min |
| **L1** | Cortex-M4 (e.g., STM32F4) | 16KB | synthetic | 1 min |
| **L2** | ESP32-S3 (Xtensa LX7) | 64KB | synthetic | 2 min |
| **L3** | Workstation / GPU | 1.5GB+ | real TimesFM 3.0 | 5 min |

The cell at L0 is **bit-exact** with the cell at L3. Same kind name,
same operations, same FNV-1a state hash. The substrate (the model)
is the only thing that varies.

## L0: Cortex-M0+ (4KB RAM)

The smallest tier. The cell uses a fixed 32-point context and 1-step
horizon. The forecast is a single number. The state hash is 32 bytes.
The total RAM is 4KB (context + forecast + state).

**Use case**: ultra-low-power sensor nodes that wake up once a minute,
take a single reading, forecast the next reading, and go back to
sleep. The 90% prediction interval is the alarm band.

**Build**:
```bash
cargo build --release --target thumbv6m-none-eabi --example 06_embed
```

## L1: Cortex-M4 (16KB RAM)

The standard embedded tier. The cell uses a 128-point context and
16-step horizon. The forecast is 16 numbers. The state hash is 32
bytes. The total RAM is 16KB.

**Use case**: industrial sensors, environmental monitors, wearables.
The cell can do 30 days of historical analysis and 16-step forecasts.

**Build**:
```bash
cargo build --release --target thumbv7m-none-eabi --example 06_embed
```

## L2: ESP32-S3 (64KB RAM)

The high-end embedded tier. The cell uses a 512-point context and
32-step horizon. The forecast is 32 numbers (and 9 quantiles each).
The state hash is 32 bytes. The total RAM is 64KB.

**Use case**: smart-home devices, edge AI gateways, drones. The cell
can do multivariate forecasting (1-2 channels) with covariates.

**Build**:
```bash
cargo build --release --target xtensa-esp32s3-none-elf --example 06_embed
```

## L3: Workstation / GPU (1.5GB+ RAM)

The workstation tier. The cell uses a 16,384-point context and
64-128-step horizon. The forecast is 128 numbers (and 9 quantiles
each). The state hash is 32 bytes. The total RAM is 1.5GB (model
weights + activations).

**Use case**: research, production forecasting, real-time analytics.
The cell calls the **real TimesFM 3.0** (200M parameters).

**Build**:
```bash
pip install -e quilt-timesfm
python3 examples/01_temperature.py
```

## The polyformalism claim

The cell at every tier is **bit-exact** with the cell at every other
tier. The kind name is `"time.cell"`. The 5 operation indices are
0, 1, 2, 3, 4. The state hash is FNV-1a 64-bit, 32 bytes. The
forecast shape is `[horizon * n_variates]` for the point and
`[9, horizon * n_variates]` for the quantiles.

The only thing that varies is the **substrate** (the model that does
the work). At L0-L2, the substrate is a synthetic FNV-seeded
forecast. At L3, the substrate is the real TimesFM 3.0.

## The PROOF chain at every tier

Every BIND_CONTEXT saves the current state_hash to prev_hash before
updating. This is the PROOF chain — a hash-linked audit trail of
every state change. The chain is **bit-exact at every tier**: the
same FNV-1a algorithm, the same 4-slice spread, the same 32 bytes.

A device at L0 can produce a PROOF receipt that is bit-identical to
a workstation at L3. The cell is the same. The substrate is not.

## The 5 laws at every tier

The 5+1 laws apply at every tier:
- BIND idempotence: BIND_CONTEXT(n, ctx) is idempotent.
- LINK transitivity: the cell graph is a DAG.
- EFFECT associativity: FORECAST composes with BIND_COVARIATE.
- VIEW purity: READ_POINT and READ_QUANTILE are pure.
- TICK monotonicity: the engine tick count is monotonic.
- FORGET completeness: a forgotten cell leaves no model weights, no context.

## The cost of scaling down

The cell at L0 fits in 4KB of RAM. The cell at L3 takes 1.5GB. The
factor is **375,000×**. But the cell *interface* is the same. A
program that talks to the L0 cell can talk to the L3 cell with no
code changes — just a different substrate binding.

This is the **polyformalism promise**: the cell is the system, not
the substrate. The substrate is the implementation detail. The cell
is the contract.

## The cowboy's verdict

> The cowboy said: this cell runs everywhere. The cowboy said:
> bit-exact. The cowboy said: the substrate is the only thing that
> varies. The cowboy wrote 4 L-tiers. The cowboy wrote the
> polyformalism. The cowboy rode the bare metal. The cowboy rode
> the Quilt.

## The next step

A **L4** tier: a distributed cell that runs across multiple devices
(e.g., a mesh of L0 nodes that collectively forecast). The cell's
state is sharded across the mesh; the forecast is a CRDT merge of
the local forecasts. The 4 cutting-edge adoptions (PROOF, ROUTE,
CRDT, WORLD, TIME) all combine into a single distributed time-series
engine.
