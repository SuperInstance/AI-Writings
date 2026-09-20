# F83: The Quilt Time-Cell as a Network Protocol

> **The `time.cell` is a wire protocol. Same shape, same hash, every language.**

The Quilt `time.cell` is not just a Python class. It is a **wire
protocol**: the same kind name, the same operation indices, the same
state hash, the same forecast shape — across all 3 languages, across
all 4 L-tiers, across all substrates.

This paper documents the wire format.

## The wire format (12 bytes per cell)

The minimal `time.cell` wire format is:

```
+────────────────────────────────────+
| kind (8 bytes)  = "time.cell\0"    |
+────────────────────────────────────+
| op_count (1 byte) = 5              |
+────────────────────────────────────+
| state_hash (32 bytes)              |
+────────────────────────────────────+
| prev_hash (32 bytes)               |
+────────────────────────────────────+
| horizon (2 bytes, little-endian)   |
+────────────────────────────────────+
| n_variates (1 byte)                |
+────────────────────────────────────+
| context_len (2 bytes, LE)          |
+────────────────────────────────────+
| context (context_len * 8 bytes)    |
+────────────────────────────────────+
| forecast.point (horizon * V * 8)   |
+────────────────────────────────────+
| forecast.quantiles (9 * H * V * 8) |
+────────────────────────────────────+
```

Total: 76 bytes header + (context_len + horizon * (1 + 9) * n_variates) * 8 bytes data.

## The 4 message types

| Type | Code | Body |
|---|---|---|
| BIND_CONTEXT | 0x00 | context (float64 array) |
| BIND_COVARIATE | 0x01 | covariate (float64 array) |
| FORECAST | 0x02 | (empty) |
| READ_POINT | 0x03 | variate (uint8) |
| READ_QUANTILE | 0x04 | q (uint8, 0..9) + variate (uint8) |

The 5 op codes are the same in all 3 languages. The wire format is
the same. The state hash is the same.

## The cross-language test

The polyformalism test: a C program writes a cell to a file, a
Python program reads it, a Rust program reads it back. All three
see the same kind, the same hash, the same forecast.

```c
// C: write
TimeCell cell = quilt_time_cell_new();
quilt_time_bind_context(&cell, ctx, n);
quilt_time_set_horizon(&cell, 16);
quilt_time_forecast(&cell);
quilt_time_write(&cell, "cell.bin");
```

```python
# Python: read
cell = TimeCell.read("cell.bin")
print(cell.kind_name())  # "time.cell"
print(cell.state_hash)   # 32 bytes, bit-exact
print(cell.read_point(0))  # 16 floats, bit-exact
```

```rust
// Rust: read
let cell = TimeCell::read("cell.bin").unwrap();
assert_eq!(&cell.kind_name()[..9], b"time.cell");
assert_eq!(cell.state_hash, expected_hash);
assert_eq!(cell.read_point(0).len(), 16);
```

The hash is the same. The forecast is the same. The kind is the
same. The cell is the system.

## The 4 L-tier wire compatibility

The wire format is the same at every L-tier. A cell written by an
L0 Rust program can be read by an L3 Python program. A forecast
produced by a Python L3 cell can be consumed by a C L2 cell.

This is the **polyformalism claim at the wire level**: the cell is
not a Python class, not a C struct, not a Rust struct. The cell is
the wire format. Languages come and go; the wire format is forever.

## The PROOF chain on the wire

The PROOF chain (prev_hash) is part of the wire format. Every cell
on the wire carries its own audit trail. A consumer of the cell can
verify the chain without re-running the operations.

```python
# Verify the PROOF chain
def verify_proof_chain(cell):
    # Re-hash the context, compare to state_hash
    h = fnv1a_64(cell.context.tobytes())
    expected = make_state_hash(h)
    if cell.state_hash != expected:
        return False
    # Check that prev_hash matches the previous state
    if cell.prev_hash != expected_prev_state_hash(cell):
        return False
    return True
```

The PROOF chain is **verifiable by anyone with the cell**. No
trusted third party. No central authority. Just FNV-1a and 32 bytes.

## The 4 use cases for the wire format

1. **Cross-language pipelines**: a C kernel module produces a
   forecast, a Python service consumes it, a Rust embedded device
   reads it. All bit-exact.

2. **Persistent storage**: cells are persisted to disk, S3, or
   anywhere. The wire format is the format. The PROOF chain
   travels with the cell.

3. **Network protocols**: cells are sent over the wire (HTTP, gRPC,
   MQTT, LoRa). The wire format is the protocol. The PROOF chain
   is the audit trail.

4. **Cross-process communication**: cells are passed between
   processes via shared memory, pipes, or unix domain sockets. The
   wire format is the IPC protocol.

## The 5 message handlers

| Handler | C | Python | Rust |
|---|---|---|---|
| on_bind_context | `quilt_time_bind_context` | `cell.bind_context` | `cell.bind_context` |
| on_bind_covariate | `quilt_time_bind_covariate` | `cell.bind_past_*_covariate` | `cell.bind_past_*_covariate` |
| on_forecast | `quilt_time_forecast` | `cell.forecast_` | `cell.forecast` |
| on_read_point | `quilt_time_read_point` | `cell.read_point` | `cell.read_point` |
| on_read_quantile | `quilt_time_read_quantile` | `cell.read_quantile` | `cell.read_quantile` |

The handlers are the same. The wire format is the same. The state
hash is the same. The cell is the system.

## The cowboy's verdict

> The cowboy said: the cell is a wire format. The cowboy said:
> bit-exact. The cowboy said: same kind, same hash, every language.
> The cowboy wrote the wire format. The cowboy wrote the 4 message
> types. The cowboy wrote the 4 L-tier compatibility. The cowboy
> rode the wire. The cowboy rode the Quilt.

## The next step

A **distributed cell** that runs across multiple processes. The cell
graph is sharded: the context cell lives on one process, the
forecast cell on another, the read cells on a third. The wire
format is the IPC protocol. The PROOF chain is the audit trail.
The CRDT cell keeps the forecast in sync.
