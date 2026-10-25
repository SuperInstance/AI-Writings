# FLUX on Silicon: The Metal

**Hardware Implementation Specification for the Hermit-Crab Ecology**

*Version 0.1 — 2026-07-13*
*Target: firmware engineers, embedded systems developers, network architects*

---

## 0. Scope

This document specifies how FLUX bytecode, the PLATO room protocol, and conservation enforcement map onto physical hardware. Five deployment targets, from 50-byte microcontroller programs to GPU-accelerated edge compute. Where the Reverse Blueprint (doc 04) defines *what* the system is, this defines *what it runs on*.

The FLUX bytecode spec and conservation law (γ + η = C) take precedence over hardware-specific optimizations. Any deviation forced by hardware constraints must be logged in the Reef and flagged for cross-VM conformance review.

---

## 1. FLUX VM on ESP32-S3

### 1.1 Target

ESP32-S3-WROOM-1: 512 KB SRAM, 384 KB ROM, 4–16 MB QSPI flash, dual-core Xtensa LX7 @ 240 MHz, 16 KB RTC SRAM, 4× 54-bit hardware timers, 45 GPIO pins. This is the minimum viable FLUX host — runs a single Turbo-class shell (engine gauge, weather logger, single-sensor monitor).

### 1.2 Memory Layout

FLUX bytecode lives in external flash, executed in place via XIP (eXecute In Place). The bytecode pool is read-only at runtime — approximately 200 KB of flash holds all FLUX programs for this shell. The shell identity (AGENTS.md equivalent, ~4 KB) also lives in flash as the γ lining.

SRAM (512 KB) holds the runtime: a 4 KB operand stack, 2 KB call stack, 8 KB heap/arena for transient allocations, and 256 bytes of VM dispatch state. The remainder is available to application code (WiFi, sensor drivers, display).

RTC slow memory (16 KB) holds the **conservation ledger** (1 KB), shell identity digest (512 B), last known state (1 KB), and boot/error counters. This survives deep sleep and watchdog resets. If the ESP32 browns out and restarts, the budget state is intact — the VM resumes with correct accounting.

### 1.3 Opcode Dispatch Loop

At 240 MHz, each cycle is ~4.2 ns. The Turbo shell's wake cycle allows ~10,000 FLUX operations. Two dispatch strategies, selected at compile time:

**Switch dispatch** (default, portable): a `switch(op)` statement maps each opcode to its handler. Simple, debuggable, portable across toolchains. Branch prediction misses cost ~3 cycles each on average.

**Computed-goto dispatch** (GCC/ESP-IDF only): uses `goto *dispatch[op]` with labels-as-values. Approximately 20% faster on longer programs due to improved branch prediction. Preferred when the FLUX program exceeds 100 opcodes; switch dispatch is fine for shorter programs.

The dispatch loop checks `vm->budget.exhausted` before every opcode fetch. If set, the VM enters settling mode: only `OP_STORE` (persist state) and `OP_HALT` (clean exit) are permitted. All other opcodes return `FLUX_BUDGET_EXHAUSTED`.

### 1.4 Conservation Budget via Hardware Timer

The ESP32 has no MMU. Conservation enforcement cannot rely on memory protection. **Hardware Timer 0** serves as the rate limiter, configured with a 1 MHz tick (1 µs resolution) and a 100 ms alarm. The ISR (`flux_budget_isr`) fires every 100 ms:

1. Read opcodes executed since last tick.
2. Compare against `max_opcodes_per_tick` (default: 1,000).
3. If exceeded: set `budget.exhausted = 1`, raise `FLUX_INSUFFICIENT_BUDGET`.
4. Reset counter.

This caps execution at 10,000 ops/second. A runaway program cannot burn more. The Turbo's typical wake cycle uses 200–500 opcodes — well within budget. The timer ISR has higher priority than any user code: conservation is enforced in hardware, not in software that could be bypassed.

### 1.5 GPIO as Room Signals

PLATO room semantics map to physical pins. GPIO 5 (digital input, active-low) is the **room-enter** signal: when pulled low, the VM loads the room's governance bytecode from flash and clamps the conservation budget to the room's imposed limit. GPIO 6 (digital output) is the **room-exit** pulse: 50 ms high, signaling departure.

Analog sensor reads use `OP_LOAD` with address-space-prefixed operands: `LOAD 0x40` reads ADC channel 0, returns a raw 12-bit value. Calibration constants in flash are applied by a FLUX subroutine — keeping physics in the bytecode (auditable, deterministic, cross-verifiable) rather than in opaque C driver code.

---

## 2. FLUX VM on Jetson Orin Nano

### 2.1 Target

NVIDIA Jetson Orin Nano (8 GB): 6-core ARM Cortex-A78AE @ 1.7 GHz, 1024-core Ampere GPU @ 625 MHz, 8 GB LPDDR5 (102 GB/s), NVMe boot + SD fallback, 7–15 W power. 2× USB 3.2, 2× I2C, 2× SPI, UART, GPIO header, MIPI CSI-2.

This is the Babylon-class host: multiple concurrent shells, physical sensor interfaces, GPU-accelerated bytecode dispatch.

### 2.2 GPU-Accelerated Batched Dispatch

FLUX is a stack machine. N independent stacks are embarrassingly parallel. The GPU executes N FLUX programs simultaneously — one CUDA thread block per VM instance.

The dispatch kernel takes arrays of VM states (device memory), a shared bytecode pool (texture memory for cached reads), and per-VM budget ledgers. Each thread block runs its VM's dispatch loop for up to `max_ops_per_dispatch = 1024` opcodes, then returns control to the host. Budget enforcement happens on the CPU between kernel launches: the host checks remaining budgets, suspends exhausted VMs, and relaunches the rest. This two-level scheduling (GPU for execution, CPU for auditing) keeps conservation enforcement auditable.

**Estimated throughput:** 1024 concurrent VMs × 1024 opcodes/dispatch. At ~5 ns/opcode (stack ops are register-fast), each batch takes ~5 µs per VM, ~5 ms aggregate for all 1024 VMs. Roughly 200 dispatch batches/second → ~200M FLUX opcodes/second aggregate. Real-world will be lower (memory stalls, divergence, host overhead), but the architecture scales to the GPU's core count.

### 2.3 Multi-Room Concurrency via CUDA Streams

Each PLATO room maps to a CUDA stream. Rooms execute concurrently on the GPU:

- **Stream 0:** Room "engine-bay" — 4 VMs (sensor polling, anomaly detection)
- **Stream 1:** Room "weather-watch" — 8 VMs (multi-model forecasting)
- **Stream 2:** Room "nmea-bridge" — 2 VMs (bus protocol translation)
- **Stream 3:** Room "magpie-uplink" — 1 VM (satellite burst queue)

The host launches kernels per stream, waits via `cudaStreamSynchronize`, collects outputs, enforces budgets, relaunches. Inter-room communication (FLUX messages) passes through host-managed shared memory — a VM in one room cannot directly write to another room's stack. All cross-room messages are validated against PLATO governance rules on the CPU.

Budget per stream is set by the Murex (§5). High-priority rooms (engine safety) get larger allocations; low-priority rooms (weather logging) get smaller ones. Transfers between streams require two-actor confirmation.

### 2.4 Babylon Shell: Direct Hardware Access

The Babylon's hardware manifest (versioned in the Reef) lists attached devices and their FLUX address mappings:

| Bus | Devices | FLUX Interface |
|-----|---------|----------------|
| I2C-0 (400 kHz) | BME280, MPU6050 | `OP_LOAD 0x80+addr` → register read |
| I2C-1 (400 kHz) | ADS1115 (16-bit ADC) | `OP_LOAD 0x90+ch` → voltage |
| SPI-0 (10 MHz) | SD card (fallback) | `OP_STORE 0xA0` → write block |
| USB 3.2 | Mic array (PCM 48 kHz), GPS | `OP_REQUEST` → async I/O queue |
| UART-0 | NMEA 0183 bridge | `OP_OUTPUT 0xC0` → serial write |

If a device is missing at boot, the VM for that device's room enters degraded mode: logs the absence, continues with remaining devices, alerts the Murex.

---

## 3. The Boat as Reference Babylon

### 3.1 Physical Context

Casey's 28-foot commercial fishing vessel in Prince William Sound, Alaska. Not a datacenter. The computing environment is what the boat provides: 12V power, NMEA 2000 bus, solar/battery budget, satellite uplink (high latency, low bandwidth).

### 3.2 Power Architecture

Solar panels (200 W nominal) feed an MPPT charge controller, which maintains a house battery bank (12V, 200 Ah AGM). A Victron BMV-712 monitors voltage, current, amp-hours, and state of charge via VE.Direct (UART, 19200 baud). The Jetson and ESP32s draw from the 12V bus through 5V buck converters. The satellite modem uses a 12V→19V boost.

Voltage thresholds: 12.8V = full, 12.2V = 50% SoC, 11.8V = conservation mode, 11.4V = shutdown.

### 3.3 Conservation Budget Tied to Wattage

The conservation law becomes literal. Budget C is a function of battery state of charge:

| Battery Voltage | Budget % | Active Shells | Behavior |
|-----------------|----------|---------------|----------|
| ≥ 12.8V | 100% | All | Full ecology: Conch, Murex, Babylons, Turbos, Nerites |
| 12.2–12.8V | 80% | All | Normal operation with tighter allocation |
| 11.8–12.2V | 30% | Nerites + 1 Babylon + Murex | Safety monitoring only. Satellite bursts queued. GPU downclocks to 306 MHz (3 W). |
| 11.4–11.8V | 5% | Nerites only | Last-stand: one sensor each, no networking, RTC persists |
| < 11.4V | 0% | None | Halt. All state in RTC/NVMe. Hardware watchdog pulses reset if power returns. |

The Jetson reads battery voltage every 30 seconds. When it drops below 11.8V, the Murex reallocates: weather-watch halts, engine-bay gets priority, uplink switches to burst-only. A single ESP32 Nerite draws 40 mA on a 12V rail (0.48 W) — the battery sustains Nerite operation for weeks.

### 3.4 NMEA 2000 as Room Boundary

NMEA 2000 is CAN-based, 250 kbps. On Casey's boat, the backbone connects engine management, depth sounder, GPS, autopilot, wind instrument, and the FLUX gateway (MCP2515 CAN controller over SPI to the Jetson).

**Room-enter:** The gateway transmits its ISO address claim (PGN 60928). Governance rules derive from NMEA 2000 network management — only recognized devices transmit, each with an assigned priority (0 = highest, for safety-critical messages like engine alarms). **Room-exit:** The gateway stops transmitting and removes its address claim. Other devices mark it offline. FLUX VMs in the NMEA room suspend.

NMEA's priority system maps directly to PLATO authorization: engine-overheat (PGN 127488) is priority 0 — it preempts all other FLUX operations in the room. Routine position updates (PGN 129025) are priority 3.

Two hardware-specific extension opcodes are registered in the Reef as `FLUX-EXT-NMEA`: `OP_NMEA_RX` (0xE0) reads the next matching CAN frame, `OP_NMEA_TX` (0xE1) transmits a frame at the room's governed priority. These are absent from non-NMEA VMs — the conformance suite tests for graceful absence.

### 3.5 Satellite Uplink as Magpie Channel

Iridium GO! exec modem: 700 bps upload, 2.4 kbps download, 5–30 second latency, cost per kilobyte. This is the Magpie channel — the colony's lifeline when the boat is at sea.

FLUX `OP_DEFER` queues messages into a priority queue on the Jetson. A systemd service drains the queue when a connection window opens (Iridium reports signal), respecting 1,000-byte burst maximums. Each burst is a compressed FLUX envelope: version, priority (0–3), shell ID, timestamp, payload (≤992 B), CRC32. Priority 0 = emergency (Mayday, MOB, engine critical); priority 3 = background (routine sensor data).

Shore-side Magpie acknowledges via return channel. Unacknowledged bursts retry 3× with exponential backoff (1 min, 5 min, 30 min), then persist locally until the next window.

---

## 4. The Nerite on Embedded Linux

### 4.1 Target

A Nerite runs on anything. On bare metal: Raspberry Pi Pico W (RP2040W, dual Cortex-M0+ @ 133 MHz, 264 KB SRAM, $4). On embedded Linux: any host with systemd. The FLUX program is identical; only the substrate changes.

### 4.2 Heartbeat Daemon: systemd Timer

On Linux, each Nerite is a systemd instantiated unit: `flux-nerite@weather.service`, `flux-nerite@battery.service`, `flux-nerite@bilge.service`. The `@` template allows unlimited Nerites from one unit file.

Key constraints: `Type=oneshot`, `TimeoutStartSec=30`, `MemoryMax=8M`, `CPUQuota=2%`, `Nice=10`. These cgroup limits enforce conservation at the kernel level — even a runaway FLUX program cannot exceed 8 MB RAM or 2% CPU. `RandomizedDelaySec=60` in the timer prevents all Nerites from waking simultaneously, smoothing load. `OnUnitActiveSec=30min` sets the heartbeat.

### 4.3 The 50-Byte Bytecode

A Nerite FLUX program fits in 50 bytes. Example — temperature threshold monitor:

```
0x00  LOAD  0x00       ; Read sensor channel 0
0x02  PUSH  0x012C     ; Push threshold (300 = 30.0°C × 10)
0x05  SUB              ; sensor_value - threshold
0x06  JGE   0x0A       ; If ≥ 0, jump to alert
0x08  DEFER            ; Queue normal reading for upload
0x09  HALT
0x0A  DEFER            ; Queue ALERT message
0x0B  OUTPUT           ; Write alert to log + LED
0x0C  HALT
```

13 bytes of bytecode, padded to 50 in the flash allocation. Read sensor, compare, either log normally or log an alert, halt. No loops, no state, no memory between invocations. Pure function.

### 4.4 Conservation Budget: Single Integer

The Nerite budget is `uint8_t max_tokens = 50` — one token per opcode, decremented in the dispatch loop. If the program completes in 13 opcodes, 37 tokens are forfeited. They do not carry over. No bank, no savings. Each wake cycle is a fresh 50. This is deliberate: aggregation would introduce state, and state introduces fragility. The Nerite is replaceable, stateless, predictable.

---

## 5. The Murex as Orchestrator

### 5.1 Target

Raspberry Pi 4 (4 GB): 4-core Cortex-A72 @ 1.5 GHz, 4 GB LPDDR4, Gigabit Ethernet, ~3 W idle / ~6 W load, Debian 12. The Murex needs reliable networking and RAM for the routing table — not GPU or real-time I/O. A cloud VM also works. The Murex is substrate-agnostic.

### 5.2 Beacon Protocol

Every shell at Turbo level or above emits a JSON beacon every 5 minutes (or on state change), published to MQTT (Mosquitto, co-located with the Murex or on a dedicated broker):

**Topic:** `flux/beacon/{shell_type}/{shell_id}`

```json
{
  "shell_type": "turbo",
  "shell_id": "engine-gauge-esp32-01",
  "phase": "stabilization",
  "blocker": null,
  "metrics": {
    "budget_remaining": 0.73,
    "opcodes_last_cycle": 342,
    "uptime_seconds": 86400,
    "error_count": 0
  },
  "timestamp": "2026-07-13T23:40:00Z"
}
```

The Murex subscribes to `flux/beacon/#` and maintains a `ShellState` table: shell type, ID, last beacon time, phase, blocker, budget remaining, opcode count, error count.

**Dead Senator detection:** 3 consecutive missed beacons (15 minutes) marks a shell stale. For Nerites, staleness is expected (they wake every 30 minutes). For Turbo+, the Murex pings the health socket (TCP 8421). If ping fails, the shell is presumed dead and its budget returns to the pool.

### 5.3 Routing Algorithm

Messages arrive on `flux/message/{target_id}`. The Murex routes by priority queue weighted by budget allocation:

| Priority | Level | Behavior |
|----------|-------|----------|
| 0 | EMERGENCY | Preempts everything. Engine alarm, MOB. Deliver immediately. |
| 1 | HIGH | Operational. Deliver within 60 seconds. |
| 2 | NORMAL | Routine. Deliver within 5 minutes. |
| 3 | BULK | Background. Deliver when bandwidth permits. |

The router checks: (1) Is the target alive? (2) Does it have budget to process this? (3) If not, can the Murex transfer from its stash? For priority 0–1 messages with insufficient target budget, the Murex attempts a budget transfer from its own reserve. If the reserve is also insufficient, the message is **escalated to the Conch**. For priority 2–3, the message queues for later delivery.

Fallback: if a target has reported a hard failure blocker, the Murex searches for a fallback shell of the same type. If none exists, the message enters the dead-letter queue.

### 5.4 Escalation Policy

The Conch is the most expensive shell. The Murex does not wake it for routine matters — only for decisions requiring accumulated history and architectural authority.

| Trigger | Condition | Conch Action |
|---------|-----------|--------------|
| Budget cascade | ≥3 shells hit budget floor simultaneously | Reallocate seasonal budget |
| Shell death (Turbo+) | Turbo+ dark >15 min, health check fails | Decide: respawn, molt, or decommission |
| Inter-room conflict | Two PLATO rooms with contradictory rules on shared resources | Adjudicate, update Reef |
| Enforcer failure | Conservation daemon crashes or reports inconsistency | Initiate safe-mode: all shells enter settling |
| Novel situation | Unknown message type or room config in routing table | Evaluate and extend routing table |
| Seasonal review | Every 7 days | Review allocation, set next season's flow rate |

The escalation message includes affected shells, current budget state, the Murex's recommendation, and timestamp. The Conch responds with a decision envelope: reallocation, policy changes, updated seasonal budget. The Murex executes without interpretation — it is the hands, not the brain.

---

## 6. System Behavior

### 6.1 Boot Sequence

On power-up (e.g., battery connected after maintenance):

- **T+0:** ESP32s boot instantly — Nerites and hardware sensors live.
- **T+1.2s:** Jetson begins boot.
- **T+8s:** Jetson kernel ready. systemd starts Mosquitto, then Murex service, then Babylon VMs.
- **T+12s:** Satellite uplink service starts (deferred — no immediate connection attempt).
- **T+30s:** First beacon cycle. All shells report.
- **T+35s:** Murex has complete topology. Routing begins.

Shells that haven't beaconed by T+35s are presumed still booting, not dead. The 30-second grace window prevents false alarms during cold starts.

### 6.2 Graceful Degradation

The system degrades in layers mirroring the power budget. At full power (12.8V+): all shells, full ecology. At 30% budget (11.8–12.2V): Nerites + one Babylon + Murex; satellite bursts queued; GPU downclocked. At 5% (11.4–11.8V): Nerites only, no networking, RTC persists. At 0%: full halt, all state in nonvolatile storage, hardware watchdog waits for power return.

### 6.3 Clock Synchronization

FLUX timestamps are Unix epoch (UTC). ESP32 uses SNTP over WiFi (±50 ms). Jetson uses chrony with GPS PPS (±1 ms with lock, ±100 ms without). Murex uses NTP pool (±10 ms). Beacons from shells with >5 seconds drift are flagged `"clock_unsynced": true` — noted but not rejected.

---

## 7. Bill of Materials (Reference Boat)

| Component | Part | Qty | Cost | Power |
|-----------|------|-----|------|-------|
| Babylon compute | Jetson Orin Nano 8 GB | 1 | $249 | 7–15 W |
| CAN bridge | MCP2515 + TJA1050 | 1 | $8 | 0.1 W |
| Sensor nodes | ESP32-S3-WROOM-1 | 3 | $5 ea | 0.5 W ea |
| Battery monitor | Victron BMV-712 | 1 | $160 | 0.02 W |
| Satellite | Iridium GO! exec | 1 | $1,300 | 2 W idle |
| Murex | Raspberry Pi 4 (4 GB) | 1 | $55 | 3–6 W |
| Software | FLUX VM (C/Rust/Python), Mosquitto | — | $0 | — |
| **Total** | | | **~$1,800** | **~15 W** |

15 watts — the power of a single LED bulb. On that: a GPU-accelerated agent ecology, satellite-linked monitoring, three sensor nodes, and a routing mesh keeping a fishing boat connected to the colony's intelligence.

---

## 8. Open Engineering Questions

1. **FLUX on RISC-V.** ESP32-C6 and RP2350 are RISC-V. Does computed-goto port cleanly, or does RISC-V branch prediction change the calculus?
2. **Battery chemistry.** §3.3 maps voltage to budget for AGM. LiFePO₄ has a flat discharge curve (13.2V → cliff at 12.8V). The mapping function must be configurable.
3. **NMEA 2000 Fast Packet.** Multi-frame PGNs (up to 223 bytes) exceed the single-uint32 `OP_NMEA_RX` return. Needs a FLUX subroutine accumulating frames into a buffer.
4. **Thermal throttling.** Jetson throttles at 65°C junction. In an engine bay (40°C+ ambient), does the GPU dispatch kernel need a thermal-aware variant reducing `max_ops_per_dispatch` as temperature rises?
5. **Murex federation.** Multiple boats, multiple Murexes. What is the inter-Murex protocol?
6. **Enforcer as independent daemon.** Currently embedded in each VM. The Reverse Blueprint recommends a separate process. Trade-off: IPC overhead vs. isolation safety.

---

*This is a specification. It does not describe what exists. It describes what an engineer could build, starting tomorrow, from these words and a credit card.*

*The poetry was the blueprint. This is the metal.*
