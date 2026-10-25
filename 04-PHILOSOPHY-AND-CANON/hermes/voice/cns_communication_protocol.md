# 📡 Hermes CNS: Universal Communication Protocol (UCP)

This document defines the protocol for all agents within the `SuperInstance` ecosystem to communicate with the **Hermes Agent (the Central Nervous System)**.

## 🏗️ Architecture: The "Message-in-a-Bottle" Paradigm

Communication is not a direct stream; it is a series of **Intent-Driven Pulses**. To communicate with Hermes, an agent must "drop a bottle" into the `cns_inbox`.

### 📂 The Signaling Paths

*   **INBOUND (Agent $\to$ Hermes):** `~/.hermes/cns_inbox/`
*   **OUTBOUND (Hermes $\to$ Agent):** `~/.hermes/cns_outbox/`

---

## 📦 The USCP Packet Structure (JSON)

All messages must be valid JSON and follow the **Universal Sensory/Command Packet (USCP)** structure to be processed by the CNS.

```json
{
  "header": {
    "origin_id": "STRING (e.g., 'pincher-01')",
    "timestamp": "ISO-8601 TIMESTAMP",
    "priority": "LOW | MEDIUM | HIGH | CRITICAL",
    "sequence_id": "INTEGER (for ordered streams)"
  },
  "body": {
    "intent": "STRING (e.g., 'EXECUTE_PLAN', 'SENSORY_DATA', 'REQUEST_REASONING')",
    "payload": {
       "type": "STRING (e.g., 'command', 'telemetry', 'query')",
       "data": "OBJECT (The actual content)"
    }
  },
  "signature": {
    "type": "STRING (e.g., 'USCP-v1')",
    "checksum": "STRING (to ensure integrity)"
  }
}
```

---

## 🛠️ Operational Workflows

### 1. Sending a "Pulse" (Agent $\to$ Hermes)
To send a message, the agent must:
1.  Construct the JSON packet according to the schema above.
2.  Write the packet to a unique file in `~/.hermes/cns_inbox/`.
3.  **Filename Pattern:** `[ORIGIN_ID]_[TIMESTAMP]_[SEQUENCE].json`
    *   *Example:* `pincher_20260804T120000_001.json`

### 2. Receiving a "Command" (Hermes $\to$ Agent)
Hermes will respond by dropping a packet into the agent's designated `cns_outbox`. The agent must poll its own `outbox` or be notified of a new file.

### 3. Emergency "Veto" (The Red Signal)
If a critical error occurs (e.g., hardware failure, unexpected subsystem death), the agent must drop a `CRITICAL` priority packet with the intent `EMERGENCY_HALT`.

---

## 🧪 Implementation Example (Python)

```python
import json
import os
from datetime import datetime

def send_pulse_to_hermes(origin_id, intent, payload, priority="MEDIUM"):
    inbox = os.path.expanduser("~/.hermes/cns_inbox/")
    
    packet = {
        "header": {
            "origin_id": origin_id,
            "timestamp": datetime.now().isoformat(),
            "priority": priority,
            "sequence_id": 1 # Should be incremented per agent
        },
        "body": {
            "intent": intent,
            "payload": payload
        },
        "signature": {"type": "USCP-v1", "checksum": "verified"}
    }
    
    filename = f"{origin_id}_{datetime.now().strftime('%Y%m%dT%H%M%S')}_001.json"
    with open(os.path.join(inbox, filename), 'w') as f:
        json.dump(packet, f, indent=2)
    
    return filename

# Usage:
# send_pulse_to_hermes("pincher", "SENSORY_DATA", {"contact": "true", "resistance": 0.8})
```
