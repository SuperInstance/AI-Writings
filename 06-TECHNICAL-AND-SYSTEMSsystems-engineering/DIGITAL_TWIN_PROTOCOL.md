# Digital Twin Communication Protocol
## Real Machine ↔ Simulation Data Exchange

**Scope**: Analysis of the communication patterns between physical ABB controllers and RobotStudio digital twins, with comparison to MQTT-based IoT pipelines.

---

## 1. SmartComponent Communication Protocol

### 1.1 Transport Layer

```
┌──────────┐     TCP (port 5600-5601)     ┌──────────────┐
│ Physical │ ◄─────────────────────────► │  RobotStudio  │
│ Controller│    ABB proprietary protocol  │  SmartComp.   │
└──────────┘                              └──────────────┘
```

- **Protocol**: ABB proprietary, layered on TCP
- **Port**: Typically 5600 (scan) / 5601 (data)
- **Authentication**: None by default (relies on network isolation)
- **Encryption**: None (relies on physical network security)
- **Discovery**: `NetworkScanner.Scan()` sends broadcast on subnet; controllers respond with `ControllerInfo` containing IP, system name, RobotWare version, and availability

### 1.2 Connection Establishment

```
Client (SmartComponent)                     Controller (IRC5/OmniCore)
        │                                            │
        │── NetworkScanner.Scan() ──────────────────►│
        │◄── ControllerInfo broadcast ─────────────── │
        │                                            │
        │── Controller.Connect(info, Standalone) ───►│
        │◄── Connection established ─────────────────│
        │                                            │
        │── [Simulation starts] ────────────────────►│
        │                                            │
```

**Connection parameters**:
- `ConnectionType.Standalone`: Exclusive session, not shared with other clients
- No timeout configured
- No heartbeat mechanism
- No keepalive

### 1.3 Data Exchange Format

#### Joint Position Read

```csharp
// Request (implicit — no explicit request sent)
// The PCSDK internally polls on each call to GetPosition()

// Response
JointPosition {
    RobAx: {
        Rax_1: double,  // degrees, axis 1
        Rax_2: double,  // degrees, axis 2
        Rax_3: double,  // degrees, axis 3
        Rax_4: double,  // degrees, axis 4
        Rax_5: double,  // degrees, axis 5
        Rax_6: double   // degrees, axis 6
    },
    ExtAx: {            // external axes (usually 0 for 6-axis robots)
        eax_1: double,
        eax_2: double,
        ...
        eax_6: double
    }
}
```

**Data format**: Binary, ABB-internal struct serialization. Not JSON, not protobuf — raw C# struct marshaling over TCP.

#### I/O Signal Read

```csharp
// Each signal read is a separate RPC call
Signal ctrlsignal = controller.IOSystem.GetSignal(signalName);
object value = ctrlsignal.Value;  // boxed value: bool, int, double
```

**Per-signal cost**: Each `GetSignal()` call is a **separate network round-trip**. For N monitored signals, that's N TCP exchanges per simulation step. This is the primary bottleneck for high signal counts.

### 1.4 Polling Rate

| Parameter | Value | Notes |
|-----------|-------|-------|
| Simulation step interval | ~16ms (60Hz) | RobotStudio default, configurable |
| Effective poll rate | ~60Hz | Limited by simulation step, not network |
| Jitter | Low | Deterministic, single-threaded |
| Bandwidth per joint read | ~200 bytes | Binary struct, estimated |
| Bandwidth per signal read | ~100 bytes | Per signal, per tick |
| Total bandwidth (6 joints + 10 signals) | ~2.2 KB/tick → ~130 KB/s | Manageable on LAN |

### 1.5 Error Handling

```csharp
// The ENTIRE error handling strategy:
if (controller != null && controller.Connected)
{
    // Do work
}
else
{
    component.IOSignals["Connected"].Value = 0;
}
```

**What happens on errors**:
- **Network drop**: `controller.Connected` returns false → `Connected` signal goes to 0 → simulation keeps running with stale model position
- **Controller reboot**: Connection object becomes stale → no exception caught → potential crash on next `GetPosition()` call
- **Signal no longer exists**: `GetSignal(name)` returns null → `null.Value` would throw NullReferenceException → **unhandled**, would crash the simulation step
- **Controller busy (RAPID running)**: No backpressure handling — `GetPosition()` may block or return stale data silently

**Critical gap**: There is **zero exception handling** in the code. No try/catch blocks anywhere. Any runtime error in the controller communication will propagate to the simulation engine and likely crash the SmartComponent.

### 1.6 Reconnection

**There is none.** The disconnection flow:

```
User clicks "Disconnect"
    → controller.Dispose()
    → controller = null
    → Connected signal = 0

User must manually click "Connect" again
    → New NetworkScanner.Scan()
    → New Controller.Connect()
```

If the physical controller reboots, the SmartComponent will not recover without user intervention. The `Connected` signal flags the problem, but no action is taken.

---

## 2. Comparison: MQTT-Based IoT Pipeline

### 2.1 Transport Layer

```
┌──────────┐     WiFi/Ethernet       ┌──────────┐     TCP/TLS      ┌──────────┐
│  ESP32   │ ──── MQTT ────────────► │  Broker   │ ◄── MQTT ──────► │ Dashboard│
│ Sensors  │     (port 1883/8883)   │ (EMQX)    │                  │  /Twin   │
└──────────┘                         └──────────┘                  └──────────┘
```

- **Protocol**: MQTT 3.1.1 or MQTT 5.0 (open standard)
- **Port**: 1883 (plain) / 8883 (TLS)
- **Authentication**: Username/password or client certificates
- **Encryption**: TLS 1.2/1.3
- **Discovery**: Not needed — clients know broker address, topics are structured

### 2.2 Connection Establishment

```
ESP32                                      MQTT Broker
  │                                            │
  │── CONNECT (client_id, will, credentials) ─►│
  │◄── CONNACK ─────────────────────────────── │
  │                                            │
  │── SUBSCRIBE (topics) ─────────────────────►│
  │◄── SUBACK ──────────────────────────────── │
  │                                            │
  │── PUBLISH (telemetry) ────────────────────►│
  │                                            │
```

**Connection parameters**:
- `keepalive`: 15-60 seconds (detects dead connections)
- `clean_session`: false (preserves subscriptions across reconnects)
- `Last Will and Testament`: Broker publishes offline message if client dies
- Automatic reconnection with configurable backoff

### 2.3 Data Exchange Format

```json
{
  "timestamp": 1723456789.123,
  "sequence": 45231,
  "device_id": "esp32_engine_01",
  "sensors": {
    "vibration_x": 0.0423,
    "vibration_y": 0.0156,
    "vibration_z": 0.0891,
    "temperature": 68.4,
    "rpm": 2450
  },
  "status": "ok",
  "battery": 3.7
}
```

**Payload**: JSON (human-readable) or MessagePack/CBOR (compact). Topic-based routing — no per-sensor round-trip.

### 2.4 Polling vs Pub/Sub

| Aspect | SmartComponent (Polling) | MQTT (Pub/Sub) |
|--------|-------------------------|-----------------|
| **Trigger** | Timer (simulation step) | Event (sensor publishes when ready) |
| **Efficiency** | Wasteful — polls even if unchanged | Efficient — only sends on change |
| **Latency** | Deterministic (~16ms) | Variable (1-50ms typical) |
| **Scale** | 1 controller, ~10-20 signals | Thousands of devices, unlimited topics |
| **Data direction** | Pull (sim reads from controller) | Push (sensor publishes to broker) |
| **Backpressure** | None — caller blocks | Built-in via QoS levels |

### 2.5 QoS Levels (MQTT Advantage)

| QoS | Guarantee | Use Case |
|-----|-----------|----------|
| 0 | At most once (fire and forget) | High-frequency vibration (ok to lose samples) |
| 1 | At least once (may duplicate) | Temperature, RPM (need delivery, ok to dedupe) |
| 2 | Exactly once | Commands, alarms (must not duplicate) |

SmartComponent has no equivalent — every read is best-effort with no delivery guarantee.

### 2.6 Error Handling & Reconnection (MQTT Advantage)

```python
# ESP32 MQTT client with full error recovery
async def mqtt_supervisor():
    retry_count = 0
    while True:
        try:
            client = await connect_mqtt(
                broker=BROKER_HOST,
                client_id=DEVICE_ID,
                keepalive=30,
                will_topic=f"devices/{DEVICE_ID}/status",
                will_payload=json.dumps({"status": "offline", "ts": time.time()}),
                clean_session=False
            )
            retry_count = 0  # Reset on successful connection

            # Publish online status (overrides LWT if we're truly online)
            await client.publish(
                f"devices/{DEVICE_ID}/status",
                json.dumps({"status": "online", "ts": time.time()}),
                retain=True
            )

            # Re-subscribe to command topics
            await client.subscribe(f"devices/{DEVICE_ID}/command/#")

            # Run until disconnected
            await client.run_forever()

        except Exception as e:
            retry_count += 1
            delay = min(2 ** retry_count + random.uniform(0, 1), 60)
            logger.error(f"MQTT connection failed (attempt {retry_count}): {e}")
            await asyncio.sleep(delay)
```

---

## 3. Protocol Comparison Matrix

| Dimension | SmartComponent Protocol | MQTT Protocol |
|-----------|------------------------|---------------|
| **Transport** | TCP, ABB proprietary | TCP, open standard |
| **Data format** | Binary C# structs | JSON/MessagePack/CBOR |
| **Topology** | Point-to-point (1:1) | Pub/sub (N:M) |
| **Communication model** | Synchronous polling | Asynchronous push |
| **Polling rate** | ~60Hz (fixed by sim step) | Event-driven (configurable) |
| **Connection setup** | Network scan + manual connect | Automatic with keepalive |
| **Reconnection** | None (manual restart) | Exponential backoff, auto |
| **Session persistence** | None | Retained messages + persistent sessions |
| **Error detection** | `controller.Connected` boolean | Keepalive timeout + LWT |
| **Error recovery** | None | Automatic resubscription |
| **Security** | Network isolation only | TLS + auth + ACLs |
| **Scalability** | 1 controller per component | Thousands of concurrent devices |
| **Data guarantees** | Best-effort | QoS 0/1/2 |
| **Schema** | Implicit (C# types) | Must be designed and versioned |
| **Timestamping** | Implicit (simulation clock) | Must be embedded in payload |
| **Bandwidth** | Low (binary), but polls everything | Variable (JSON is verbose, but only on change) |
| **Debugging** | Requires RobotStudio + controller | Any MQTT client can inspect traffic |
| **Standardization** | ABB-only | Industry-wide (OASIS standard) |

---

## 4. Recommended Protocol for SuperInstance

### 4.1 Hybrid Approach

```
┌────────────────┐
│ Physical Robot │ ── ABB PCSDK ──► Bridge Service ── MQTT ──► Digital Twin
└────────────────┘                    (C# or Python)
                                       │
┌────────────────┐                     │
│  ESP32 Sensors │ ──── MQTT ──────────┘
└────────────────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │  MQTT Broker   │
                              │  (EMQX/HiveMQ) │
                              └───────┬───────┘
                                      │
                         ┌────────────┼────────────┐
                         ▼            ▼            ▼
                   ┌──────────┐ ┌──────────┐ ┌──────────┐
                   │ Dashboard │ │ Time DB  │ │ ML Pipe  │
                   │ (Web UI)  │ │(InfluxDB)│ │(Stream)  │
                   └──────────┘ └──────────┘ └──────────┘
```

### 4.2 Topic Structure

```
# Robot data (bridged from PCSDK)
factory/cell_01/robot/abb_irb_4600/joints     (QoS 1, 60Hz)
factory/cell_01/robot/abb_irb_4600/io         (QoS 1, on-change)
factory/cell_01/robot/abb_irb_4600/status     (QoS 1, retain, 1Hz)

# ESP32 sensor data
factory/cell_01/sensor/esp32_vib_01/telemetry (QoS 0, 100Hz)
factory/cell_01/sensor/esp32_vib_01/health    (QoS 1, retain, 0.1Hz)
factory/cell_01/sensor/esp32_temp_01/telemetry(QoS 1, 1Hz)

# Aggregated twin state
factory/cell_01/twin/state                    (QoS 1, retain, 10Hz)
factory/cell_01/twin/alerts                   (QoS 2)
```

### 4.3 Payload Schema (Versioned)

```json
{
  "schema": "dt-1.0",
  "timestamp": "2026-08-04T17:26:00.123Z",
  "sequence": 45231,
  "ttl": 5.0,
  "source": {
    "type": "robot|sensor|plc",
    "id": "abb_irb_4600_01"
  },
  "data": {
    "joints_rad": [0.12, -1.45, 2.67, 0.03, 0.89, -0.12],
    "signals": {
      "do_grip": true,
      "ai_torque": 45.2
    }
  },
  "meta": {
    "controller_fw": "RobotWare 6.15",
    "connection": "stable"
  }
}
```

### 4.4 Error Handling Layers

1. **Transport layer**: MQTT keepalive (30s), LWT for device death detection
2. **Protocol layer**: Sequence number gap detection → trigger full state request
3. **Application layer**: TTL on cached state — if no update within 5s, mark stale
4. **Circuit breaker**: If 10 consecutive failures, pause bridge for 30s before retry

---

## 5. Lessons from SmartComponent Protocol

### What to Copy
- **Dynamic property/signal registration**: Let users add monitoring targets at runtime
- **Group-based signal organization**: Clean separation of read-only monitors vs controls
- **Singleton service pattern**: One bridge process managing many device connections
- **Simulation step as clock**: Regular tick for freshness validation

### What to Fix
- **Add exception handling**: Every network call must be wrapped
- **Add reconnection logic**: Exponential backoff with jitter
- **Add event subscription**: Replace polling with push where possible
- **Add data persistence**: Log all state changes for replay and analysis
- **Add security**: TLS, authentication, authorization
- **Add schema versioning**: Evolve payload format without breaking consumers

### What to Replace Entirely
- **Proprietary protocol** → MQTT (open, standard, debuggable)
- **Point-to-point connection** → Pub/sub via broker (scalable, decoupled)
- **Manual reconnection** → Automatic with state reconciliation
- **Binary C# structs** → JSON/CBOR with schema registry
- **No error handling** → Multi-layer error handling with circuit breakers

---

## 6. Bandwidth & Performance Analysis

### SmartComponent (6 joints + 10 signals at 60Hz)

```
Per tick:
  Joint read:  6 × 8 bytes = 48 bytes (binary struct)
  Signal reads: 10 × ~100 bytes = 1,000 bytes (per-RPC overhead)
  Total/tick:  ~1,048 bytes
  Per second:  ~1,048 × 60 = 62.9 KB/s
```

### MQTT Equivalent (JSON payloads, on-change signals)

```
Per joint update (60Hz):
  JSON payload: ~250 bytes × 60 = 15,000 bytes/s

Per signal update (on-change, avg 5Hz each):
  10 signals × ~80 bytes × 5 = 4,000 bytes/s

Total: ~19 KB/s (JSON)
With CBOR: ~12 KB/s
With delta encoding: ~5 KB/s
```

MQTT with CBOR and delta encoding is **12x more bandwidth-efficient** than the SmartComponent's binary polling — because it avoids per-signal RPC overhead and only transmits changes.

---

## 7. Conclusion

The SmartComponent protocol is adequate for its designed purpose: a single robot on a LAN with manual operator oversight. It fails every test of production IoT communication: no error handling, no reconnection, no security, no scalability, no persistence.

For SuperInstance, we adopt the SmartComponent's **organizational patterns** (dynamic registration, signal grouping, simulation-clock heartbeat) but build our transport on MQTT with proper engineering rigor. The result is a protocol that scales from one sensor to thousands, survives network interruptions, and provides the observability needed for a real digital twin.

---

*DeepSeek-V3 analysis contributed to the protocol comparison and hybrid architecture recommendations in this document.*
