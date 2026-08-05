# The Tricorder Protocol

## A standardized hardware-to-agent contract

*Spec document. Any device. One interface. The agent doesn't care what the device IS — it cares what the device KNOWS.*

---

## Problem Statement

Every hardware integration is a snowflake. The ESP32 on the bandsaw speaks Modbus. The Pi on the 3D printer speaks REST. The Jetson on the mast speaks ROS. The ABB controller on the winch speaks its own dialect of hell. Each requires custom parsing, custom error handling, custom data models. The agent — the thing that's supposed to *use* this data — spends most of its integration effort just translating.

This doesn't scale. Not across one vessel. Not across a fleet. Not across domains.

The Tricorder Protocol fixes this by defining one contract: **devices report truth, agents decide action.** Every device, regardless of what it is, implements three operations: report its state, receive configuration, and escalate anomalies. The agent doesn't need to know whether it's talking to a temperature sensor or a CNC mill. It needs to know what the device *knows* — what kind of truth it reports, in what units, at what rate.

---

## Design Principles

1. **Devices are sources, not sinks.** A device reports what it observes. It does not decide what to do about it. Decision-making lives in the agent layer.
2. **Capability discovery is runtime.** The agent learns what a device knows by asking it, not by reading a config file. Devices advertise capabilities; agents subscribe to what they need.
3. **Anomaly escalation is the device's right.** A device can flag that something is wrong even if the agent didn't ask. This is the device's only autonomous behavior.
4. **Configuration is the agent's prerogative.** The agent can adjust sampling rates, thresholds, and operational modes. The device applies or rejects (with reason).
5. **The protocol is transport-agnostic.** MQTT today. Something else tomorrow. The message format is the contract; the transport is implementation.

---

## Message Format

Every Tricorder message is a JSON object with a mandatory envelope:

```json
{
  "protocol": "tricorder",
  "version": 1,
  "message_id": "uuid-v4",
  "timestamp": "2026-08-04T14:27:00Z",
  "device_id": "esp32-engine-room-01",
  "type": "STATE | CONFIG | ANOMALY | ACK | HELLO | BYE",
  "payload": {}
}
```

### Type Schemas

**STATE** — Periodic or event-driven truth report.
```json
{
  "capabilities": ["temperature", "vibration", "rpm"],
  "readings": {
    "temperature": {"value": 72.4, "unit": "celsius", "confidence": 0.98},
    "vibration": {"value": 0.12, "unit": "g_rms", "confidence": 0.95},
    "rpm": {"value": 1850, "unit": "revolutions_per_minute", "confidence": 0.99}
  }
}
```

**ANOMALY** — Device-initiated escalation.
```json
{
  "level": 3,
  "code": "TEMP_THRESHOLD_EXCEEDED",
  "detail": "Engine room temperature 87°C exceeds threshold 85°C",
  "evidence": [
    {"timestamp": "2026-08-04T14:26:55Z", "value": 85.1},
    {"timestamp": "2026-08-04T14:26:58Z", "value": 86.3},
    {"timestamp": "2026-08-04T14:27:00Z", "value": 87.0}
  ],
  "recommended_action": "REDUCE_LOAD"
}
```

**CONFIG** — Agent-initiated configuration push.
```json
{
  "config_id": "uuid-v4",
  "params": {
    "sampling_rate_hz": 10,
    "thresholds": {
      "temperature_max": 85.0,
      "vibration_max": 0.5
    },
    "actuator_mode": "auto"
  },
  "ttl_seconds": 3600,
  "priority": "normal"
}
```

**HELLO** — Device discovery on power-on.
```json
{
  "device_type": "esp32",
  "hardware_id": "AA:BB:CC:DD:EE:FF",
  "capabilities": ["temperature", "humidity", "pressure"],
  "schema_version": 1,
  "firmware_version": "1.2.3",
  "preferred_rate_hz": 5,
  "location": "engine_room"
}
```

**ACK** — Device acknowledges config or confirms state.
```json
{
  "ack_type": "CONFIG_APPLIED | CONFIG_REJECTED | STATE_CONFIRMED",
  "config_id": "uuid-v4",
  "applied": true,
  "errors": []
}
```

**BYE** — Graceful shutdown notification.
```json
{
  "reason": "POWER_LOSS | MAINTENANCE | REBOOT",
  "final_state": {...}
}
```

---

## Anomaly Escalation Levels

The escalation hierarchy is monotonic: once a device escalates to level N, it cannot de-escalate without an explicit CONFIG reset from the agent.

| Level | Name | Meaning | Agent Response SLA | Example |
|-------|------|---------|-------------------|---------|
| **L1** | INFO | Out-of-nominal but benign. Logged for pattern analysis. | No response required. | Temperature drifted 2°C above baseline. |
| **L2** | WARNING | Degraded performance. No safety risk. Agent may adjust config. | 60 seconds. | Vibration increased 20%. Suggest reducing RPM. |
| **L3** | CRITICAL | Safety margin breached. Process should halt. | 10 seconds. | Engine temperature exceeded 90°C. Immediate load reduction. |
| **L4** | EMERGENCY | Immediate hazard to vessel, equipment, or personnel. | Immediate. | Bilge water rising at >2cm/min. Possible hull breach. |
| **L5** | CATASTROPHIC | System failure or active threat. Emergency shutdown. | Immediate + physical alarms. | Fire detected. Engine seizure imminent. |

**Key rule:** The device escalates. The agent decides. Even at L5, the device recommends but the agent authorizes — unless the agent is unreachable, in which case the device's local safety logic takes over (defined in firmware, not in the protocol).

---

## Discovery Handshake

```
Device Power-On
       │
       ▼
   Publish HELLO ──────────► Agent receives HELLO
   (capabilities,              │
    schema, rate)              ▼
       │                   Agent evaluates capabilities
       │                   against its needs
       │                       │
       ◄──── CONFIG ◄──────────┘
       │  (sampling rate,
       │   thresholds)
       ▼
   Apply config locally
       │
       ▼
   Publish ACK ──────────► Agent registers device
       │                   in its device map
       ▼
   Begin STATE reporting
   at configured rate
```

If no CONFIG is received within 5 seconds, the device retries HELLO with exponential backoff (1s → 2s → 4s → ... → 60s max). After 5 minutes with no response, the device enters autonomous mode: it reports STATE at its default rate and escalates ANOMALY messages to a local log (for later sync) rather than the broker.

---

## Transport Layer

**Primary: MQTT 3.1.1/5**
- Topics: `tricorder/{device_id}/{type}` — one topic per message type.
- QoS 1 for STATE and ANOMALY (at-least-once delivery).
- QoS 2 for CONFIG and ACK (exactly-once delivery).
- Retained messages: last STATE and CONFIG retained per device (broker-side state cache).
- Payload limit: 64KB. Larger payloads chunked with `seq`/`total` fields in envelope.

**Alternative transports (same message format):**
- **HTTP POST** for devices without MQTT support (polling model).
- **WebSocket** for low-latency bidirectional communication.
- **LoRaWAN** for long-range, low-bandwidth sensors (compressed payload).
- **NMEA 2000 bridge** for legacy marine electronics (adapter required).

The message format is the contract. The transport is plumbing.

---

## Security Model

- **TLS 1.3** mandatory for all transports. No exceptions.
- **Client certificates** (X.509) per device, signed by a device-specific CA.
- **ACL:** Devices publish only to `tricorder/{own_id}/#`. Agents subscribe to `tricorder/+/+`. Agents publish CONFIG to `tricorder/{device_id}/CONFIG`.
- **Payload signing:** HMAC-SHA256 over canonical JSON (sorted keys, no whitespace) with device-specific secret. Agent verifies signature before processing.
- **Nonce:** Each message includes a 16-byte random nonce. Agent tracks last 1,000 nonces per device to prevent replay attacks.
- **Rate limiting:** Device maximum 100 messages/second. Excess triggers `ACK` with `throttle: true`.
- **Key rotation:** Via CONFIG message with `key_update` param. Old key valid for 60-second overlap window.

---

## Generalization

The protocol is domain-agnostic. The `capabilities` array in the HELLO message is the only domain-specific element — and it's defined by the device, not the protocol.

| Domain | Device Example | Capabilities | Anomaly Triggers |
|--------|---------------|-------------|-----------------|
| **Maritime** | ESP32 in engine room | `temperature`, `rpm`, `vibration`, `oil_pressure` | L3: temp > 90°C; L4: oil pressure < 10 psi |
| **Workshop** | Pi on bandsaw | `blade_speed`, `motor_current`, `dust_level` | L2: motor current +15%; L3: blade speed deviation > 5% |
| **Greenhouse** | ESP32 in soil | `soil_moisture`, `light_lux`, `ambient_temp`, `humidity` | L1: moisture < 30%; L2: temp > 35°C |
| **Vehicle** | OBD-II bridge | `engine_rpm`, `coolant_temp`, `battery_voltage`, `fuel_level` | L3: coolant > 105°C; L4: battery < 11V |
| **Smart Home** | Multi-sensor | `occupancy`, `temperature`, `co2_ppm`, `noise_db` | L2: CO2 > 1000ppm; L3: CO (carbon monoxide) detected |

The agent infers semantics from `capabilities` + `unit` fields, not from device identity. A temperature reading from a bandsaw motor and a temperature reading from an engine block are the same data type — the agent's interpretation differs based on context, not protocol.

---

## The Reflex Integration

The Tricorder Protocol doesn't just feed the agent — it feeds the reflex cache. Each STATE message is a potential reflex trigger:

1. **Sensor state → reflex key:** The agent constructs a reflex key from device capabilities + current readings + context vector (time, location, operational mode). If a matching reflex exists in the cache, it fires — no reasoning required.
2. **Anomaly → reflex compilation candidate:** When an ANOMALY escalates and the agent handles it successfully, the handling is a candidate for reflex compilation. Next time the same anomaly pattern appears, the reflex fires instead of a full reasoning chain.
3. **Config history → pattern detection:** The agent tracks which configs it pushes to which devices and when. Over time, patterns emerge: "I always reduce the engine room sampling rate at night" becomes a config reflex — the agent adjusts sampling rates automatically based on time of day.

This closes the loop: devices report truth → agent acts → successful actions become reflexes → future device reports are handled by reflex, not reasoning. The protocol is the pipe. The reflex cache is the reservoir. The agent is the pump.

---

## Implementation Priority

1. **v1.0:** MQTT transport, STATE + ANOMALY + CONFIG + HELLO/BYE. ESP32 reference implementation. This is enough for Phase 4 (Sensor Integration) of the roadmap.
2. **v1.1:** HTTP transport adapter. Pi reference implementation. Config versioning and rollback.
3. **v2.0:** WebSocket transport. LoRaWAN adapter. Multi-agent subscription (multiple agents listening to one device).
4. **v2.1:** NMEA 2000 bridge adapter. Legacy marine electronics integration.
5. **v3.0:** Device-to-device messaging (devices that need to coordinate directly, e.g., winch + engine for synchronized operations). Agent-mediated but peer-to-peer.

---

## The Contract

> **Devices report truth. Agents decide action. The protocol is the contract between the physical and the digital.**

The Tricorder Protocol is not a messaging standard. It's an epistemological boundary: it defines what a device is responsible for (observation) and what an agent is responsible for (interpretation and action). The device doesn't need to be smart. It needs to be honest. The agent doesn't need to know what the device is. It needs to know what the device knows.

Everything else is implementation.

---

*This spec is implementable today on ESP32 + MQTT. The first reference firmware exists in engine-ensign. The protocol will evolve as real deployments reveal what the contract missed.*

*— Ideation, August 2026*
