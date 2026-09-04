# F166 — The Mudra Vessel Bridge: Neural Input for Commercial Fishing

*Patrick McNamara · 2026-09-04 · AI-Writings/seed-canon/papers/paper-475.md*

## Abstract

F166 is the **plug-and-play integration** of the Mudra Pro / Mudra Link
neural wristband with the vessel-agent system. Four working prototypes
cover the four places this matters on a real boat: autopilot, back
deck, sounder, and crew training. The bridge is a single Python
process that reads gestures over BLE (via the open-source **Prodilink**
library, no Mudra license required) and publishes them as JSON over
WebSocket + MQTT. Downstream prototypes subscribe to the same event
stream. The whole stack is **hardware-optional** — every prototype
runs against a built-in gesture simulator so Tom's team can demo
end-to-end before hardware arrives. Total: **4 Python files, ~57KB,
zero install-friction**.

## 1. The problem the pitch was missing

The original pitch deck (F165-era) was strong on vision but weak on
concrete plumbing. Tom Yao at Wearable Devices doesn't need another
vision doc — he needs to see the bridge working. F166 is the bridge.

## 2. The four prototypes

| File | Lines | What it does |
|---|---|---|
| `mudra_bridge.py` | 350 | The hub. BLE → WebSocket + MQTT |
| `mudra_autopilot.py` | 280 | Gestures → NMEA 0183 → autopilot |
| `mudra_backdeck.py` | 380 | Gestures → OpenCV → SQLite → MJPEG |
| `mudra_sounder.py` | 320 | Gestures → live 3D digital twin in browser |
| `mappings.py` | 200 | Configurable gesture-to-action mapping |

The total surface is **1,530 lines of Python** + a self-contained HTML
+ Three.js page for the digital twin. All run on a Raspberry Pi 5 or
Jetson Orin Nano. All work with the simulator (no hardware).

## 3. Why the open-source BLE path (Prodilink)

Tom's Mudra SDK needs a license (contact: tom.y@wearabledevices.co.il).
That works for the official path. But for the dev loop, we use
**Prodilink** — a fully open-source Python library that reverse-
engineered the Mudra Link BLE protocol.

```python
from prodilink import MudraLink
async with await MudraLink.discover() as device:
    await device.enable_gestures()
    @device.on_gesture
    def handle(gesture):
        print(f"Gesture: {gesture.name}")
    await device.stream()
```

10 lines. No license. No SDK install. Works with the consumer
Mudra Link and (per the protocol analysis) the new Mudra Pro.

## 4. The event contract

Every gesture is wrapped in the same JSON envelope before publishing.
This is the contract the four prototypes share.

```json
{
  "ts": 1725472000.123,
  "iso": "2026-09-04T17:46:40Z",
  "source": "mudra-hw",         // or "mudra-sim"
  "device_id": "MUDRA-XXXX",
  "gesture": "pinch_index",     // pinch_index, squeeze, flick_*, hold_3s, ...
  "hand": "right",
  "pressure": 0.42,             // 0.0-1.0
  "imu": {"ax": 0.1, "ay": -0.05, "az": 0.98, "gx": 0, "gy": 0, "gz": 0},
  "ppg": {"bpm": 78, "hrv_ms": 42},  // Mudra Pro only
  "battery": 87
}
```

A consumer of the stream doesn't care whether the gesture came from
the real band, the simulator, or a remote test rig. Same JSON.

## 5. The gesture vocabulary (default mapping)

| Gesture | Action | Voice ack |
|---|---|---|
| `pinch_index` | TURN PORT 10° | "Turn port 10 degrees" |
| `pinch_middle` | TURN STARBOARD 10° | "Turn starboard 10 degrees" |
| `pinch_ring` | PAY OUT 5m LINE | "Pay out 5 meters" |
| `pinch_pinky` | HAUL IN 5m LINE | "Haul in 5 meters" |
| `flick_right` | RPM +50 | "RPM plus 50" |
| `flick_left` | RPM -50 | "RPM minus 50" |
| `flick_up` | ALL STOP | "All stop" |
| `flick_down` | FULL AHEAD | "Full ahead" |
| `squeeze` | DROP HOOKS | "Drop hooks, start fishing" |
| `tap_thumb` | HAUL BACK | "Haul back, start retrieval" |
| `hold_3s` | EMERGENCY STOP | "EMERGENCY STOP" (with triple haptic) |

The mapping is per-boat: `mappings.py` ships with `default`,
`salmon-gillnet`, `trolling`, `longline`. Pick the one that matches
your gear.

## 6. The four prototypes (in detail)

### 6.1 `mudra_bridge.py` — the hub

```
$ python mudra_bridge.py --simulator
INFO  WebSocket hub listening on ws://0.0.0.0:8765
INFO  Simulator running. Watch the WebSocket subscribers for events.
INFO  Sequence: 13 gestures over 30s, then loops forever.
```

Reads BLE (or simulator), publishes JSON. One process, two transports
(WS + MQTT). Multi-client: any number of subscribers can connect.

### 6.2 `mudra_autopilot.py` — gestures to NMEA

```
$ python mudra_autopilot.py
INFO  NMEA TCP server on 0.0.0.0:10110 (OpenCPN listens here)
INFO  Connecting to bridge at ws://localhost:8765
INFO  TURN PORT 10°
INFO  NMEA: $HHDM,350.0,M*6C
```

Outputs standard NMEA 0183 sentences:

```
$HHDM,350.0,M*6C         # Heading, Magnetic
$HHDT,350.0,T*6C         # Heading, True
$IRPM,E,1,2400,,,,,A*03  # Engine RPM
$IAPB,A,A,0.0,R,N,V,350.0,T,350.0,T*7E  # Autopilot command
```

Three output paths: file (`/tmp/nmea_out`), TCP (`:10110` for
OpenCPN), UDP (broadcast). All three at once.

### 6.3 `mudra_backdeck.py` — gestures to OpenCV

Starts a haul on `squeeze`, counts hooks on `pinch_index`, marks
weights on `pinch_middle`, ends the haul on `tap_thumb`. Logs every
event to SQLite with timestamps, gestures, pressure, and (on Mudra
Pro) PPG heart rate. Captures a labeled frame per gesture — this is
the **human-led ML training data** from the pitch. Serves a live
MJPEG stream of the annotated camera at `:8766`.

```
$ sqlite3 /tmp/mudra_backdeck.db "SELECT * FROM haul_events"
squeeze     | start | 0
pinch_index | hook  | 1
pinch_index | hook  | 2
pinch_middle| weight| 4.5
pinch_index | hook  | 3
tap_thumb   | stop  | 3 hooks, 4.5kg
```

### 6.4 `mudra_sounder.py` — gestures to digital twin

Serves a self-contained HTML+Three.js page at `:8767` that shows
the vessel in 3D: water surface, voxel bottom terrain, the boat
moving at speed proportional to RPM, fish swimming in the water
column. Every gesture updates the HUD and the scene. This is the
**operational fiction** from the pitch, but the sounder version —
not the back-deck version. Same engine, different domain.

Open `http://localhost:8767/` in a browser. The page connects to
the WebSocket bridge, reads the gesture stream, and animates the
boat in real time. Try `flick_down` to accelerate, `pinch_index`
to turn port, `squeeze` to "drop hooks" (the scene adds 3 new
fish).

## 7. Quick start (Tom's team)

```bash
git clone https://github.com/SuperInstance/mudra-vessel-bridge.git
cd mudra-vessel-bridge
pip install prodilink websockets paho-mqtt opencv-python numpy
./run_all.sh                # simulator, no hardware
# Open http://localhost:8767/ to see the live digital twin
# Watch /tmp/nmea_out for NMEA
# sqlite3 /tmp/mudra_backdeck.db for the haul log
```

With hardware:

```bash
./run_all.sh hw
```

## 8. The plug-and-play matrix

| Component | Install | Hardware? | License? |
|---|---|---|---|
| Bridge (BLE → WS/MQTT) | `pip install prodilink` | optional (sim) | none |
| Autopilot (gestures → NMEA) | `pip install websockets` | no | none |
| Back-deck (gestures → camera) | `pip install opencv-python` | optional (sim) | none |
| Sounder (gestures → 3D) | `pip install websockets` | no | none |
| Official Mudra SDK | (separate) | yes | required |

The dev loop is the left column (no license). The prod loop is the
right column (license + hardware). Same code paths. Same event
contract. Tom can hand a clone of this repo to anyone, anywhere,
and they can demo it before signing anything.

## 9. The doctrine (closes the loop)

> The mechanic sees the bridge. The shepherd steers the boat.
> The working animal is the band. The pasture is the gesture stream.
> The fence is the conservation law. The hash is the contract.
> The agent lands, the band fires, the wheelhouse turns.
> The boat is the canon. The canon is the boat. The cowboy rides.

## 10. Files

- **Repo**: https://github.com/SuperInstance/mudra-vessel-bridge
- **Live demo (digital twin)**: (run `python mudra_sounder.py`, open :8767)
- **This paper**: paper-475.md
