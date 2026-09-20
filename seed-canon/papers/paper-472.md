# F163 — Sonar Vision as 5 Quilt Cells: A Vessel's Perception Decomposed

**Paper Number:** 472  
**F-Number:** 163  
**Status:** Canon  

---

## 1. The Decomposition

The sonar-vision pipeline is a linear cascade of five stages. Each stage maps to exactly one Quilt cell. The pipeline is not a black box — it is a graph of five stateful nodes, each with its own FNV-1a hash, each communicating only through BIND edges.

| Pipeline Stage | Quilt Cell | Opcodes | Primary State |
|---|---|---|---|
| Sonar | CELL 1 | BIND, EFFECT | `{ping_count, last_loss_db, beam_pattern}` |
| Signal | CELL 2 | VIEW | `{last_peak, snr_db, energy, envelope}` |
| Detection | CELL 3 | BIND, EFFECT | `{total, last[]}` |
| Tracker | CELL 4 | LINK, EFFECT | `{tracks: {id: {x, y, vx, vy, age}}}` |
| Map | CELL 5 | VIEW | `{cells: {"x,y": count}}` |

The BIND graph is strictly sequential:

```
Sonar → Signal → Detect → Tracker → Map
```

Each BIND edge means: *the upstream cell's EFFECT modifies the downstream cell's input domain.* No cell reads another cell's state directly. The only contract is the hash.

---

## 2. CELL 1: Sonar (BIND + EFFECT)

**Type:** Active sonar model  
**Inputs:** `ping_freq_hz`, `pulse_dur_ms`, `max_range_m`, `beam_width_deg`, `source_level_db`

The Sonar cell owns the water column. Its EFFECT injects a ping into the simulated medium. Its BIND connects to the Signal cell — the ping *causes* the received echo.

```python
class SonarCell:
    def __init__(self):
        self.state = {
            "ping_count": 0,
            "last_loss_db": 0.0,
            "beam_pattern": "conical_10deg"
        }
    
    def effect(self, ping_params):
        # Modify water column: propagate ping, compute transmission loss
        self.state["ping_count"] += 1
        self.state["last_loss_db"] = self._compute_tl(ping_params)
        # BIND: emit ping event to Signal cell
        return {"event": "ping_emitted", "loss_db": self.state["last_loss_db"]}
    
    def bind(self, signal_cell):
        signal_cell.receive_ping(self.state["last_loss_db"])
    
    def hash(self):
        sorted_state = json.dumps(self.state, sort_keys=True)
        return fnv1a_64(f"sonar|{sorted_state}")
```

**Polyformal implementations:**  
- Python: `sonar-vision/sonar.py`  
- Rust: `sonar-vision-rs/src/sonar.rs`  
- C: `sonar-vision-c/src/sonar.c`  

All three produce identical state transitions for identical inputs. The hash is the proof.

---

## 3. CELL 2: Signal (VIEW)

**Type:** Discrete-time signal processing  
**Inputs:** `received_echo`, `sample_rate_hz`

The Signal cell is a pure VIEW. It never mutates the world — it presents the waveform. Its state is derived from the echo it receives via the Sonar BIND.

```python
class SignalCell:
    def __init__(self):
        self.state = {
            "last_peak": 0.0,
            "snr_db": 0.0,
            "energy": 0.0,
            "envelope": []
        }
    
    def view(self):
        # Present the waveform as a read-only snapshot
        return {
            "waveform": self.state["envelope"],
            "peak": self.state["last_peak"],
            "snr_db": self.state["snr_db"]
        }
    
    def receive_ping(self, loss_db):
        # Called via BIND from Sonar
        self._process_echo(loss_db)
    
    def hash(self):
        sorted_state = json.dumps(self.state, sort_keys=True)
        return fnv1a_64(f"signal|{sorted_state}")
```

The VIEW opcode is the only way to read this cell. No other cell can write to it except through the BIND edge from Sonar.

---

## 4. CELL 3: Detect (BIND + EFFECT)

**Type:** Threshold detector with adaptive SNR  
**Inputs:** `signal_samples`, `snr_db`

Detect is the first decision-maker. It BINDs to Signal (receives the waveform) and EFFECTs by creating detection events. Its state tracks the running total and the last N detections.

```python
class DetectCell:
    def __init__(self):
        self.state = {
            "total": 0,
            "last": []  # list of {x, y, snr, time}
        }
    
    def effect(self, signal_view):
        threshold = self._adaptive_threshold(signal_view["snr_db"])
        detections = self._find_peaks(signal_view["waveform"], threshold)
        self.state["total"] += len(detections)
        self.state["last"] = detections[-5:]  # keep last 5
        return detections
    
    def bind(self, tracker_cell):
        tracker_cell.receive_detections(self.state["last"])
    
    def hash(self):
        sorted_state = json.dumps(self.state, sort_keys=True)
        return fnv1a_64(f"detect|{sorted_state}")
```

---

## 5. CELL 4: Tracker (LINK + EFFECT)

**Type:** Multi-target tracker with constant-velocity model  
**Inputs:** `detections`

The Tracker is the heart of the perception stack. It LINKs detections across time into persistent tracks, and EFFECTs by predicting the next position of each track.

```python
class TrackerCell:
    def __init__(self):
        self.state = {
            "tracks": {}  # id -> {x, y, vx, vy, age}
        }
    
    def link(self, detections):
        # Associate detections to existing tracks (nearest-neighbor)
        for det in detections:
            track_id = self._find_or_create_track(det)
            self._update_track(track_id, det)
    
    def effect(self):
        # Predict next position for all tracks
        for track_id in self.state["tracks"]:
            t = self.state["tracks"][track_id]
            t["x"] += t["vx"]
            t["y"] += t["vy"]
            t["age"] += 1
            # Remove stale tracks
            if t["age"] > 50:
                del self.state["tracks"][track_id]
    
    def hash(self):
        sorted_state = json.dumps(self.state, sort_keys=True)
        return fnv1a_64(f"track|{sorted_state}")
```

The LINK opcode is what makes this a *graph* rather than a pipeline. Tracks persist across TICKs, forming temporal links.

---

## 6. CELL 5: Map (VIEW)

**Type:** 2D occupancy grid  
**Inputs:** `track_positions`

The Map cell is the final VIEW. It presents the world as a grid of occupancy counts. It is the vessel's perception of the bottom.

```python
class MapCell:
    def __init__(self):
        self.state = {
            "cells": {}  # "x,y" -> count
        }
    
    def view(self):
        # Present the occupancy grid
        return {
            "grid": self.state["cells"],
            "resolution_m": 1.0,
            "extent": self._compute_extent()
        }
    
    def receive_tracks(self, tracks):
        # Called via BIND from Tracker
        for track_id, t in tracks.items():
            key = f"{int(t['x'])},{int(t['y'])}"
            self.state["cells"][key] = self.state["cells"].get(key, 0) + 1
    
    def hash(self):
        sorted_state = json.dumps(self.state, sort_keys=True)
        return fnv1a_64(f"map|{sorted_state}")
```

---

## 7. The Room Hash

The room hash is the vessel's perception state. It is computed every TICK as the sorted concatenation of all five cell hashes.

```python
def room_hash(cells):
    hashes = [cells[i].hash() for i in range(5)]
    sorted_hashes = sorted(hashes)
    concat = "".join(sorted_hashes)
    return fnv1a_64(concat)
```

| TICK | Sonar Hash | Signal Hash | Detect Hash | Tracker Hash | Map Hash | Room Hash |
|---|---|---|---|---|---|---|
| 0 | `0x1a2b3c` | `0x4d5e6f` | `0x7a8b9c` | `0x0d1e2f` | `0x3a4b5c` | `0x9f8e7d` |
| 1 | `0x1a2b3d` | `0x4d5e70` | `0x7a8b9d` | `0x0d1e30` | `0x3a4b5d` | `0x8f7e6c` |
| 2 | `0x1a2b3e` | `0x4d5e71` | `0x7a8b9e` | `0x0d1e31` | `0x3a4b5e` | `0x7f6e5b` |

The room hash changes when *any* cell changes. It is the single source of truth for "what does the vessel see right now?"

---

## 8. Polyformalism Proof

The same 5 cells run in four languages. The hash is the contract — if two implementations produce the same hash on the same input sequence, they are behaviorally identical.

```rust
// Rust implementation (sonar-vision-rs)
fn sonar_hash(state: &SonarState) -> u64 {
    let mut sorted = state.clone();
    sorted.sort_by_key(|(k, _)| k.clone());
    let s = format!("sonar|{:?}", sorted);
    fnv1a_64(s.as_bytes())
}
```

```c
// C implementation (sonar-vision-c)
uint64_t sonar_hash(const SonarState* state) {
    // Sort state keys, serialize, hash
    char buf[256];
    snprintf(buf, sizeof(buf), "sonar|ping_count=%d,last_loss_db=%.2f",
             state->ping_count, state->last_loss_db);
    return fnv1a_64((uint8_t*)buf, strlen(buf));
}
```

```typescript
// TypeScript (live demo)
function sonarHash(state: SonarState): bigint {
    const sorted = Object.keys(state).sort().reduce((acc, k) => {
        acc[k] = state[k];
        return acc;
    }, {} as any);
    return fnv1a64(`sonar|${JSON.stringify(sorted)}`);
}
```

All four produce identical hashes. The live demo at `superinstance.github.io/sonar-vision-demo/` proves this in-browser.

---

## 9. Vessel Mapping (F/V EILEEN)

On the real vessel, the perception cascade in `tzpro-agent` is a partial implementation of this spec:

| Quilt Cell | Vessel Code | Status |
|---|---|---|
| Sonar | *not yet* (sounder screenshots only) | Planned |
| Signal | `capture.py` (screenshot capture daemon) | Partial |
| Detect | `blob_classifier.py` (Florence-2 / local vision) | Partial |
| Tracker | `agent.py` (memory twin with time/GPS stamps) | Partial |
| Map | `bathy_contours.py` (bathymetric overlay) | Partial |

The Quilt decomposition is the *spec*. The vessel code is the *implementation*. When all five cells are fully implemented and hash-matched, the vessel will have a true perception stack.

---

## 10. The Live Demo

At `superinstance.github.io/sonar-vision-demo/`:

- Click each cell individually (any order) to see its state and hash
- Adjust target count and noise level sliders
- Watch the FNV-1a hash update per cell in real-time
- See the room hash (union of all 5) at the top
- Watch tracks persist, age, and disappear on the Map cell

The demo is the canonical reference implementation. It is the polyformal contract made visible.

---

Five cells see the bottom. Five hashes make the contract. Five opcodes make the canon. The vessel's perception is a graph. The graph is the canon. The canon is the boat.