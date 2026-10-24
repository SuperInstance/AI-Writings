# ARCHITECTURE.md: `plato-engine-block`
> Atomic deterministic runtime unit for the Plato Matrix. Isolated, observable, embeddable block execution engine.
>
> Version: 0.1.0 | Status: Final Production Design
---
## 1. Module Structure
All core logic is `no_std` compatible with only `alloc` required. Optional standard library and network functionality is fully gated behind feature flags.
```
plato-engine-block/
├── src/
│   ├── lib.rs          # Root exports, error type, Engine facade & builder
│   ├── tick.rs         # Deterministic tick scheduler, drift correction
│   ├── sensor.rs       # Sensor registry, callback readers, sample validation
│   ├── actuator.rs     # Actuator registry, state tracking, write dispatch
│   ├── history.rs      # Lock-free atomic circular rolling buffer
│   ├── alarm.rs        # Rule engine, cooldown tracking, event logging
│   ├── protocol.rs     # Wire protocol parser / serializer, command semantics
│   └── server.rs       # Async TCP multi-client broadcast server (feature gated)
└── Cargo.toml
```
### Module Responsibility Matrix
| Module       | Dependencies               | No-Std | Purpose |
|--------------|----------------------------|--------|---------|
| `lib`        | `core`, `alloc`            | ✅      | Root types, unified error, public API boundary
| `tick`       | `core`                     | ✅      | Monotonic tick counter, rate limiter, drift compensation
| `sensor`     | `core`, `alloc`, `hashbrown` | ✅    | Named sensor registry, safe callback execution
| `actuator`   | `core`, `alloc`, `hashbrown` | ✅    | Actuator permission boundaries, write validation
| `history`    | `core`, `alloc`            | ✅      | Timestamped sample storage, lock-free reads
| `alarm`      | `core`, `alloc`            | ✅      | Predicate evaluation, cooldown enforcement, state tracking
| `protocol`   | `core`, `alloc`            | ✅      | Human & machine protocol implementation
| `server`     | `tokio`, `std`             | ❌      | TCP listener, client sessions, fanout broadcast
---
## 2. Public Types & Interface
All types follow Rust API guidelines, no panics in library code, all fallible operations return properly typed errors.
### 2.1 Root Error Type
```rust
#[non_exhaustive]
#[derive(Debug, Clone, PartialEq, Eq, Copy)]
pub enum BlockError {
    InvalidTickRate,
    SensorNotFound,
    ActuatorNotFound,
    ActuatorWriteFailed,
    HistoryBufferFull,
    AlarmRuleInvalid,
    ProtocolParseError,
    NotAuthorized,
    IoError,
    FeatureNotEnabled,
    TickDriftExceeded,
}
```
Implements `core::fmt::Display` and `core::error::Error`.
---
### 2.2 Engine Builder
```rust
#[derive(Default, Clone)]
pub struct EngineBuilder { /* private fields only */ }
impl EngineBuilder {
    /// Set tick execution rate in Hertz. Valid range: `1..=1000`
    pub fn tick_rate(self, hz: u32) -> Result<Self, BlockError>;
    /// Set maximum history entries retained. Must be power of two.
    pub fn history_depth(self, entries: usize) -> Result<Self, BlockError>;
    /// Register named sensor with read callback
    pub fn register_sensor<F>(self, name: &str, read_fn: F) -> Result<Self, BlockError>
        where F: FnMut() -> Result<f32, BlockError> + 'static;
    /// Register named actuator with write callback
    pub fn register_actuator<F>(self, name: &str, write_fn: F) -> Result<Self, BlockError>
        where F: FnMut(f32) -> Result<(), BlockError> + 'static;
    /// Attach alarm rule to engine
    pub fn add_alarm(self, rule: AlarmRule) -> Result<Self, BlockError>;
    /// Finalize configuration, pre-allocate all buffers, return running engine instance
    pub fn build(self) -> Result<Engine, BlockError>;
}
```
✅ **Guarantee**: No heap allocations occur after `build()` returns. All runtime buffers are pre-allocated at construction time.
---
### 2.3 Engine Runtime
```rust
pub struct Engine { /* private fields only */ }
impl Engine {
    /// Execute one single deterministic tick. Call manually for embedded no-std operation.
    pub fn tick(&mut self) -> Result<TickResult, BlockError>;
    /// Run infinite tick loop. Yields according to configured rate.
    #[cfg(feature = "std")]
    pub async fn run(&mut self) -> Result<(), BlockError>;
    /// Get current monotonic tick counter
    pub fn current_tick(&self) -> u64;
    /// Get last N history entries
    pub fn get_history(&self, count: usize) -> &[HistoryEntry];
    /// Write value to named actuator
    pub fn write_actuator(&mut self, name: &str, value: f32) -> Result<(), BlockError>;
    /// Subscribe client id to broadcast events
    pub fn subscribe(&mut self, client_id: u64);
    pub fn unsubscribe(&mut self, client_id: u64);
}
```
---
## 3. Feature Flags
All features are **default-off** for minimal embedded footprint.
| Feature Flag       | Enables | Transitive Dependencies |
|--------------------|---------|--------------------------|
| `default`          | Nothing | None |
| `std`              | Standard library support, sleep timers, `run()` method | `std` |
| `serde`            | `Serialize`/`Deserialize` for all configuration types | `serde`, `derive` |
| `tcp-server`       | Async Tokio TCP multi-client broadcast server | `tokio`, `std` |
| `metrics`          | Internal runtime performance counters | |
| `trace`            | Full per-tick structured debug logging | |
### Compilation Rules:
1.  All core logic compiles cleanly for `thumbv7em-none-eabihf` (ESP32) target
2.  `tcp-server` automatically enables `std` feature
3.  No panicking codepaths exist when `std` is disabled
4.  All unsafe code is explicitly gated, audited and documented
---
## 4. Text Protocol Specification
Formal ABNF Grammar. All commands are line-based UTF-8, terminated with `\r\n`.
```abnf
command         = tick-command / history-command / actuator-command /
                  alarm-command / subscribe-command / unsubscribe-command / help-command
tick-command    = "tick"
history-command = "history" [ 1*SP 1*DIGIT ]
actuator-command= "actuator" SP identifier SP number
alarm-command   = "alarm" SP ("set" SP alarm-rule / "list" / "clear" SP alarm-id)
subscribe-command = "subscribe"
unsubscribe-command = "unsubscribe"
help-command    = "help"
identifier      = 1*( ALPHA / DIGIT / "_" / "-" )
number          = [ "-" ] 1*DIGIT [ "." 1*DIGIT ]
alarm-rule      = identifier SP comparator SP number SP number
comparator      = "<" / ">" / "<=" / ">=" / "==" / "!="
```
### Response Format:
```
OK <payload>
ERR <code> <human readable message>
EVENT <tick> <type> <payload>
```
Broadcast events are delivered asynchronously to subscribed clients for every tick, alarm trigger and actuator state change.
---
## 5. Example Room Configurations
### 5.1 Fishing Boat Engine Room
```yaml
# Requires feature = "serde"
tick_hz: 2
history_depth: 86400 # 12 hours retention at 2Hz
sensors:
  engine_temp:    { unit: celsius }
  oil_pressure:   { unit: bar }
  exhaust_temp:   { unit: celsius }
  rpm:            { unit: rpm }
actuators:
  fuel_valve:     { range: [0, 100] }
  cooling_pump:   { range: [0, 1] }
  alarm_horn:     { range: [0, 1] }
alarms:
  engine_overheat: "engine_temp > 110 300"
  low_oil_pressure: "oil_pressure < 1.2 60"
```
### 5.2 Datacenter Server Rack
* 1Hz tick rate, 7 day history retention
* Sensors: inlet temp, exhaust temp, power draw, fan speed, humidity
* Actuators: fan curve, PDU outlet relays, warning beacons
* Alarms: high temp threshold, power loss, fan failure
### 5.3 Game World Combat Zone
* 60Hz tick rate, 10 minute history
* Sensors: player positions, projectile counts, collision events
* Actuators: door state, light controls, spawn triggers
* Alarms: raid detection, player count thresholds
---
## 6. Agent ↔ Room Binary Wire Protocol
Standard machine to machine protocol, guaranteed ordering, idempotent writes, little endian encoding:
```
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Magic 0x504C4154             | Version | Flags | Payload Len |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Tick Counter (u64)                                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| OpCode        | Reserved      | Sequence Number               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Payload ...                                                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| CRC32 Checksum                                                |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
Valid OpCodes:
| Code | Name | Description |
|------|------|-------------|
| 0x01 | Tick | Full block state snapshot |
| 0x02 | Sensor | Single sensor sample |
| 0x03 | ActuatorWrite | Actuator set command |
| 0x04 | AlarmEvent | Alarm trigger / clear |
| 0x05 | Subscribe | Register for broadcast |
| 0x06 | Ack | Command acknowledgement |
---
## 7. SuperInstance Ecosystem Integration
This block is the lowest level atomic execution unit of the Plato Matrix:
1.  **`flux-core`**: All block ticks are published to the Flux distributed immutable event log. Block state is replicated via Flux consensus.
2.  **`pincher`**: Pincher scheduler assigns blocks to physical hardware nodes, handles live migration, health checking and lifecycle management.
3.  **`ternary-state`**: All sensor / actuator values use native ternary floating point representation, alarm rules use ternary predicate logic.
4.  **`plato-matrix-orchestrator`**: Maintains block dependency graph, routes cross-block actuator commands, enforces capability and security boundaries.
5.  **`observability`**: All history buffers expose standard OpenMetrics endpoints when `std` feature is enabled.
---
### Implementation Guarantees
- Maximum tick jitter < 1% of tick period on hardware with accurate timers
- All runtime operations are O(1) or bounded O(N) with configured constants
- No undefined behaviour
- 100% test coverage for all core logic
This document is complete and sufficient for a competent Rust engineer to implement the entire crate without additional specification.