# Vessel Dashboard — Frontend-Only Architecture

**No cloud. No backend. No internet required.**

**Date:** 2026-08-04

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    TAURI DESKTOP APP                         │
│                                                              │
│  ┌─────────────┐   ┌───────────────┐   ┌────────────────┐  │
│  │  MQTT over  │   │   State Layer │   │  AI Synthesis  │  │
│  │  WebSocket  │──→│  (ring buffer │──→│  (Ollama local)│  │
│  │  Client     │   │  + IndexedDB) │   │                │  │
│  └──────┬──────┘   └───────┬───────┘   └───────┬────────┘  │
│         │                  │                    │            │
│         │          ┌───────┴────────┐           │            │
│         │          │   Panel System │←──────────┘            │
│         │          │  (draggable,   │                        │
│         │          │   resizable)   │                        │
│         │          └───────┬────────┘                        │
│         │                  │                                  │
│  ┌──────┴──────────────────┴──────────────────────────────┐ │
│  │                    MAP ENGINE                          │ │
│  │  ┌──────────┐  ┌───────────┐  ┌─────────────────────┐ │ │
│  │  │ deck.gl  │  │ globe.gl  │  │ MapLibre base maps  │ │ │
│  │  │ (flat)   │  │ (3D globe)│  │ (marine charts)     │ │ │
│  │  └──────────┘  └───────────┘  └─────────────────────┘ │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              RUST DESKTOP SHELL (Tauri 2)            │   │
│  │  • Window management (multi-display)                 │   │
│  │  • File system (trip logs, data export)              │   │
│  │  • System notifications (critical alerts)            │   │
│  │  • Local file serving (chart tiles, textures)        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
          ▲                                    ▲
          │ ws://localhost:9001                │ http://localhost:11434
          │                                    │
┌─────────┴──────────┐              ┌─────────┴──────────┐
│   MQTT BROKER       │              │   OLLAMA (local)   │
│   (mosquitto)       │              │   LLM inference    │
│                     │              │                    │
│   Listens on:       │              │   Models:          │
│   • TCP 1883        │              │   • llama3.2       │
│   • WS 9001         │              │   • qwen2.5        │
│                     │              │   • (user choice)  │
│   Topic tree:       │              └────────────────────┘
│   vessel/#          │
└─────────────────────┘
          ▲
          │
   ┌──────┴───────────────────────┐
   │     SENSOR NETWORK           │
   │                              │
   │  ESP32 #1 (engine bay)       │
   │  • RPM (hall sensor)         │
   │  • Temperature (DS18B20)     │
   │  • Oil pressure (analog)     │
   │  • Vibration (MPU6050)       │
   │                              │
   │  ESP32 #2 (bilge/nav)        │
   │  • Bilge water level         │
   │  • Battery voltage           │
   │  • Cabin temperature         │
   │  • Humidity (BME280)         │
   │                              │
   │  GPS module (NEO-6M)         │
   │  • NMEA 0183 → MQTT          │
   │                              │
   │  Depth sounder               │
   │  • NMEA 0183 DBT/DBS         │
   │                              │
   │  AIS receiver                │
   │  • NMEA 0183 VDM/VDO         │
   │  → parsed to AIS targets     │
   └──────────────────────────────┘
```

---

## 2. Data Flow

### 2.1 Sensor → Screen

```
ESP32 reads sensor
    │
    ▼ (1ms)
ESP32 publishes MQTT message
    │  topic: vessel/engine/rpm
    │  payload: {"v": 1850, "ts": 1785893322}
    ▼ (1-5ms over WiFi)
mosquitto broker receives
    │
    ▼ (1ms)
mosquitto forwards to WebSocket subscriber
    │
    ▼ (1-5ms)
Frontend mqtt.js receives message
    │
    ▼ (<1ms)
SensorStore dispatches to ring buffer + IndexedDB write
    │
    ▼ (<1ms, same frame)
Panel components re-render via reactive subscription
    │
    ▼ (16ms)
deck.gl / canvas paints updated gauge/marker
```

**Total latency: <30ms from physical phenomenon to screen pixel.**

### 2.2 AI Synthesis (every 15 minutes or on-demand)

```
SensorStore collects 15min of data
    │
    ▼
Correlation engine runs (RPM vs fuel, temp trend, vib analysis)
    │
    ▼
Trend summary compiled as text prompt
    │
    │  "Engine temperature has risen 4°C over 15 minutes.
    │   Current: 82°C. RPM steady at 1850. Fuel rate: 12 L/h.
    │   Vibration peak at 0.8g on Z-axis. Bilge normal.
    │   Position: 58.3°N, 134.5°W. Depth: 42m.
    │   3 AIS vessels within 5nm, nearest at 2.1nm.
    │   Generate a 3-sentence watch log entry."
    │
    ▼
POST http://localhost:11434/api/generate
    │  (Ollama, 2-10s depending on model)
    │
    ▼
WatchLogPanel displays synthesized entry
```

---

## 3. Component Architecture

### 3.1 Layer Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      PRESENTATION                           │
│  Panels • Gauges • Map Overlays • Alerts • Watch Log        │
├─────────────────────────────────────────────────────────────┤
│                      APPLICATION                            │
│  Variant Manager • Alert Engine • AI Pipeline • Trip Recorder│
├─────────────────────────────────────────────────────────────┤
│                       DOMAIN                                │
│  Sensor Store • Engine Model • Navigation Model •          │
│  AIS Tracker • Catch Log • Vessel Health Index             │
├─────────────────────────────────────────────────────────────┤
│                    INFRASTRUCTURE                           │
│  MQTT Client • IndexedDB • Tauri Bridge • Web Workers •     │
│  Ollama Client • ONNX Runtime • Vector DB                   │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Module Inventory

#### Infrastructure Layer

| Module | File | Responsibility |
|--------|------|---------------|
| **MQTT Client** | `src/services/mqtt-client.ts` | WebSocket connection to local broker, subscription management, auto-reconnect, message dispatch |
| **NMEA Parser** | `src/services/nmea-parser.ts` | Parse NMEA 0183 sentences ($GPGGA, $GPRMC, $SDDBT, AIVDM/AIVDO) |
| **IndexedDB Store** | `src/services/sensor-store.ts` | Time-series ring buffer with IndexedDB persistence. Configurable retention per topic. |
| **Tauri Bridge** | `src/services/tauri-bridge.ts` | *(kept from World Monitor)* IPC for file system, notifications, multi-window |
| **ML Worker** | `src/workers/ml.worker.ts` | *(kept)* ONNX inference in Web Worker for anomaly detection |
| **Vector DB** | `src/workers/vector-db.ts` | *(kept)* In-browser vector store for semantic log search |
| **Ollama Client** | `src/services/ollama-client.ts` | REST client for local Ollama instance (`/api/generate`, `/api/tags`) |
| **ONNX Runtime** | *(kept)* | Browser-side neural network inference |
| **Analysis Worker** | `src/workers/analysis.worker.ts` | Background sensor analysis, frequency analysis (FFT on vibration data) |

#### Domain Layer

| Module | File | Responsibility |
|--------|------|---------------|
| **Engine Model** | `src/domain/engine.ts` | Engine state: RPM, temp, oil, fuel, battery, hours. Threshold definitions. Derate calculations. |
| **Navigation Model** | `src/domain/navigation.ts` | Position, heading, SOG, COG, waypoint tracking, ETA, route. |
| **AIS Tracker** | `src/domain/ais.ts` | Vessel tracking from AIS messages. MMSI registry. CPA/TCPA collision calculation. |
| **Catch Log** | `src/domain/catch-log.ts` | Species, weight, quantity, position, time, tally. |
| **Vessel Health Index** | `src/domain/vhi.ts` | Composite health score (0-100) from weighted sensor inputs. Trend tracking. |
| **Depth Sounder** | `src/domain/depth.ts` | Depth readings, bottom profile accumulation, shoal alerts. |
| **Fuel Budget** | `src/domain/fuel.ts` | Consumption tracking, range estimation, reserve alerts. |

#### Application Layer

| Module | File | Responsibility |
|--------|------|---------------|
| **Variant Manager** | `src/config/variant.ts` *(adapted)* | Active view selection (bridge/engine-room/deck/captain/galley) |
| **Alert Engine** | `src/services/alert-engine.ts` | Threshold evaluation, severity escalation, alert deduplication, notification dispatch |
| **AI Pipeline** | `src/services/ai-pipeline.ts` | Data collection → trend analysis → Ollama synthesis → watch log generation |
| **Trip Recorder** | `src/services/trip-recorder.ts` | Start/stop trip recording, position snapshots, event logging |
| **Correlation Engine** | `src/services/correlation-engine/` *(adapted)* | Cross-sensor pattern detection (kept from World Monitor, new adapters) |

#### Presentation Layer

| Module | File | Responsibility |
|--------|------|---------------|
| **Panel** | `src/components/Panel.ts` *(kept)* | Shell component for all dashboard widgets |
| **EngineGaugePanel** | `src/components/EngineGaugePanel.ts` | Analog-style gauges (canvas-rendered, 60fps) |
| **NavigationPanel** | `src/components/NavigationPanel.ts` | Position display, compass rose, waypoint info |
| **DepthSounderPanel** | `src/components/DepthSounderPanel.ts` | Real-time depth + scrolling bottom profile |
| **AISPanel** | `src/components/AISPanel.ts` | AIS target list with range/bearing, CPA alerts |
| **AlertFeedPanel** | `src/components/AlertFeedPanel.ts` | Scrolling alert log with severity color coding |
| **WatchLogPanel** | `src/components/WatchLogPanel.ts` | AI-generated watch log entries |
| **VesselHealthPanel** | `src/components/VesselHealthPanel.ts` | Composite VHI gauge + breakdown |
| **SensorStatusPanel** | `src/components/SensorStatusPanel.ts` | Grid of all sensors with health indicators |
| **CatchLogPanel** | `src/components/CatchLogPanel.ts` | Catch entry form + running tally |
| **FuelBudgetPanel** | `src/components/FuelBudgetPanel.ts` | Fuel consumption chart + range estimate |
| **MapContainer** | `src/components/MapContainer.ts` *(kept)* | Map shell, renderer selection |
| **DeckGLMap** | `src/components/DeckGLMap.ts` *(stripped)* | WebGL map with vessel track, AIS, depth contour, weather |
| **GlobeMap** | `src/components/GlobeMap.ts` *(kept)* | 3D globe with vessel position |

---

## 4. State Management

No Redux. No Zustand. World Monitor uses vanilla TypeScript reactive state — a pattern of module-level singletons that emit events on mutation. Components subscribe in `connectedCallback()` and unsubscribe in `disconnectedCallback()`. This is essentially a hand-rolled reactive store, and it works perfectly for our use case.

### 4.1 SensorStore

```typescript
class SensorStore {
  // Ring buffers: latest N readings per topic
  private buffers: Map<string, RingBuffer<SensorReading>>;
  // Live values: most recent reading per topic
  private live: Map<string, SensorReading>;
  // Subscribers
  private subscribers: Map<string, Set<(reading: SensorReading) => void>>;

  // MQTT message handler
  onMessage(topic: string, payload: Uint8Array): void {
    const reading = this.parse(topic, payload);
    this.buffers.get(topic)?.push(reading);
    this.live.set(topic, reading);
    this.notify(topic, reading);
    // Async persist to IndexedDB (debounced)
    this.schedulePersist(topic, reading);
  }

  // Panel subscription
  subscribe(topic: string, fn: (r: SensorReading) => void): () => void {
    this.subscribers.get(topic)?.add(fn) ?? this.subscribers.set(topic, new Set([fn]));
    // Immediately emit last known value
    const last = this.live.get(topic);
    if (last) fn(last);
    return () => this.subscribers.get(topic)?.delete(fn);
  }

  // Historical query
  async getHistory(topic: string, durationMs: number): Promise<SensorReading[]> {
    // Read from IndexedDB for ranges beyond ring buffer capacity
    if (durationMs > RING_BUFFER_DURATION_MS) {
      return indexedDB.query(topic, durationMs);
    }
    return this.buffers.get(topic)?.toArray() ?? [];
  }
}
```

### 4.2 Ring Buffer

Each topic maintains a ring buffer of configurable size:

| Topic Pattern | Buffer Size | Retention | Persist |
|--------------|-------------|-----------|---------|
| `vessel/engine/*` | 3,600 | 1 hour (1Hz) | 24h to IndexedDB |
| `vessel/gps/*` | 1,800 | 5 min (60s at 5Hz → decimate to 1Hz after 5min) | 7d to IndexedDB |
| `vessel/depth/*` | 3,600 | 1 hour | 30d to IndexedDB |
| `vessel/sensors/*` | 1,800 | 30 min (varies) | 7d to IndexedDB |
| `vessel/ais/*` | per-vessel, 120 entries | 15 min per vessel | 24h to IndexedDB |

GPS data is decimated: full 5Hz for the last 5 minutes (breadcrumb trail), then reduced to 1Hz for the ring buffer, then 0.1Hz for IndexedDB long-term storage.

---

## 5. Map Architecture

### 5.1 Dual Engine (kept from World Monitor)

- **deck.gl flat map** — Primary renderer. WebGL-accelerated, supports 60fps animations, handles thousands of AIS targets.
- **globe.gl 3D globe** — Secondary renderer. Shows vessel position on Earth. Useful for long-distance awareness.
- **SVG fallback** — For low-performance displays (galley tablet, old laptop in engine room).

Selection logic in `MapContainer.ts` is kept: desktop gets deck.gl, mobile/low-end gets SVG, user can toggle globe mode.

### 5.2 Vessel-Centric View

World Monitor's map starts at global zoom. Vessel Monitor's map starts centered on the vessel with auto-follow:

```typescript
// Auto-follow: re-center on vessel position every GPS update
function autoFollow(position: Position) {
  if (!userInteracting) {
    deckGlMap.setProps({
      initialViewState: {
        longitude: position.lng,
        latitude: position.lat,
        zoom: speedToZoom(position.sog),  // zoom out at high speed
        bearing: position.heading,        // course-up orientation
      }
    });
  }
}
```

### 5.3 Custom Layers

| Layer | deck.gl Type | Data Source | Update Rate |
|-------|-------------|-------------|-------------|
| **Vessel marker** | `IconLayer` | GPS | 5Hz |
| **Track breadcrumb** | `PathLayer` | GPS ring buffer | 1Hz |
| **AIS targets** | `IconLayer` + `TextLayer` | AIS tracker | 30s |
| **Depth contour** | `PolygonLayer` | Depth sounder history | 60s accumulate |
| **Catch heatmap** | `HeatmapLayer` | Catch log entries | Event-driven |
| **Weather overlay** | `PolygonLayer` | Weather service / barometer | 10min |
| **Search pattern** | `PathLayer` | Trip recorder | On-demand |
| **Waypoints** | `IconLayer` + `TextLayer` | Navigation model | Event-driven |
| **Shoal warning** | `PolygonLayer` | Depth + chart comparison | 5s |

### 5.4 Marine Charts

Replace World Monitor's MapLibre dark theme with nautical chart tiles:

- **Option A:** NOAA ENC tiles via [noaa-enc-server](https://github.com/noaa-ocs/nautical-chart-tiler) (self-hosted, offline-capable)
- **Option B:** OpenSeaMap tiles (OpenStreetMap-based marine overlay)
- **Option C:** Pre-downloaded PMTiles (kept in Tauri resources, served locally)

World Monitor already uses `pmtiles` — option C is the most aligned with the "no backend" principle.

---

## 6. AI Synthesis (Local Ollama)

### 6.1 Architecture

```
┌──────────────────────────────────────────────┐
│              AI PIPELINE (15-min cycle)       │
│                                              │
│  ┌─────────┐  ┌──────────┐  ┌─────────────┐ │
│  │ Collect │→ │ Analyze  │→ │ Synthesize  │ │
│  │ 15min   │  │ Trends   │  │ Watch Log   │ │
│  │ sensor  │  │ Anomalies│  │ (Ollama)    │ │
│  │ data    │  │ Correl.  │  │             │ │
│  └─────────┘  └──────────┘  └──────┬──────┘ │
│                                     │        │
│                           ┌─────────┴──────┐ │
│                           │  WatchLogPanel │ │
│                           │  + Alert (if   │ │
│                           │    critical)   │ │
│                           └────────────────┘ │
└──────────────────────────────────────────────┘
```

### 6.2 Ollama Integration

World Monitor already has `ollama-models.ts` (model discovery) and the summarization fallback chain. We keep the model discovery, simplify the chain:

```typescript
// Vessel Monitor AI: Ollama only, no cloud fallback
async function generateWatchLog(sensorData: SensorSnapshot): Promise<string> {
  const prompt = buildWatchLogPrompt(sensorData);
  const response = await fetch('http://localhost:11434/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: await getPreferredModel(),  // user-configured, default 'llama3.2'
      prompt,
      stream: false,
      options: {
        temperature: 0.3,  // factual, not creative
        top_p: 0.9,
        max_tokens: 500,
      }
    })
  });
  const data = await response.json();
  return data.response;
}
```

### 6.3 Browser-Side ONNX Fallback

If Ollama is unavailable (not installed, crashed, model still loading), the ML Worker provides browser-side inference:

- **Anomaly detection:** Pre-trained ONNX model classifies sensor patterns as normal/degraded/critical
- **Trend prediction:** Simple linear extrapolation with confidence intervals
- **Semantic search:** Vector embeddings for "find similar events in trip history"

This is World Monitor's existing ML Worker, repurposed. The `ml.worker.ts` already supports model loading, embedding, sentiment analysis, NER, and vector search. We add:
- An anomaly detection model (small, <5MB)
- A vessel-specific embedding model for log search

### 6.4 Vector Search for Trip History

World Monitor's `vector-db.ts` (in-browser FAISS-like vector store) becomes a semantic search engine for trip history:

- Every trip is embedded as a sequence of vectors
- "Show me trips where the engine sounded like this" → vector similarity search
- "When did we last see this vibration pattern?" → temporal pattern matching

---

## 7. Tauri Desktop Architecture

### 7.1 What Changes from World Monitor

World Monitor's Tauri shell includes:
- Keyring-based secret management (API keys for Groq, OpenRouter, etc.)
- Local API proxy sidecar (Node.js server for proxying API calls)
- Multi-window support (main, settings, live-channels)
- Desktop-specific CSP

Vessel Monitor strips all of this. What remains:

### 7.2 Simplified Tauri Config

```json
{
  "productName": "Vessel Monitor",
  "mainBinaryName": "vessel-monitor",
  "identifier": "app.vesselmonitor.desktop",
  "app": {
    "windows": [{
      "title": "Vessel Monitor — Bridge",
      "width": 1920,
      "height": 1080,
      "fullscreen": true,
      "backgroundColor": [10, 15, 25, 255]
    }],
    "security": {
      "csp": "default-src 'self'; connect-src 'self' ws: wss: http://localhost:* https://localhost:* blob: data:; img-src 'self' data: blob: https:; style-src 'self' 'unsafe-inline'; script-src 'self' 'wasm-unsafe-eval'; worker-src 'self' blob:; font-src 'self' data:; media-src 'self' data: blob:;"
    }
  },
  "bundle": {
    "resources": ["../charts/", "../textures/"]
  }
}
```

Key CSP changes:
- `connect-src ws:` — allow MQTT over WebSocket
- `connect-src http://localhost:*` — allow Ollama REST calls
- No external HTTPS domains (no Vercel, no Clerk, no analytics)

### 7.3 Multi-Window Support

Tauri supports multiple windows, each pointing at a different URL hash or with different init data:

```
Window 1: Bridge Display (4K TV on bridge)
  → variant=bridge, fullscreen

Window 2: Engine Room Display (tablet mounted in engine room)
  → variant=engine-room, fullscreen

Window 3: Captain's Laptop
  → variant=captain, windowed
```

All windows share the same Vite frontend bundle. Each window loads `index.html#variant=engine-room`, and the variant system (kept from World Monitor) selects the appropriate panels.

### 7.4 File System Access

Via Tauri's `fs` API (or the bridge's `invoke` pattern):

- **Trip logs:** JSON files in `~/VesselMonitor/trips/`
- **Data export:** CSV export of sensor data
- **Chart tiles:** Local PMTiles files bundled as resources
- **Ollama models:** User installs Ollama separately; Vessel Monitor detects it

### 7.5 No Sidecar

World Monitor's Node.js sidecar (`src-tauri/sidecar/local-api-server.mjs`) is 500+ lines of HTTP proxy, auth token management, and API key injection. We don't need any of it. The frontend connects directly to:

- `ws://localhost:9001` — MQTT broker
- `http://localhost:11434` — Ollama
- Local IndexedDB — data persistence

No proxy needed. No auth tokens. The frontend is the entire application.

---

## 8. Offline-First Design

### 8.1 What Works Offline

Everything. The entire dashboard operates with zero internet connectivity:

| Feature | Offline? | Data Source |
|---------|---------|------------|
| Engine gauges | ✅ | MQTT (local) |
| GPS position | ✅ | MQTT (local) |
| Depth sounder | ✅ | MQTT (local) |
| AIS targets | ✅ | MQTT (local) |
| Alerts | ✅ | Local threshold engine |
| Watch log AI | ✅ | Local Ollama |
| Trip recording | ✅ | Local IndexedDB |
| Catch log | ✅ | Local IndexedDB |
| Vessel Health Index | ✅ | Local computation |
| Map rendering | ✅ | Local PMTiles |
| Historical playback | ✅ | Local IndexedDB |

### 8.2 What Doesn't Work Offline

| Feature | Why | Mitigation |
|---------|-----|-----------|
| Weather forecast | Requires internet | Barometer trend as proxy |
| Graticule updates | NOAA chart updates | Bundle charts, update at port |
| Ollama model download | One-time internet | Pre-install at setup |
| Fleet position (if satellite) | Requires internet | Show last known + age |

### 8.3 PWA Support

Kept from World Monitor: `vite-plugin-pwa` configuration. The app works in a browser tab even without Tauri. This matters — a crew member should be able to open the dashboard on their phone's browser connected to the boat's WiFi.

---

## 9. Performance Budget

World Monitor is tuned for a different workload: 500+ feed sources, thousands of map markers, complex correlation engine. It uses extensive chunk splitting, lazy loading, and Web Workers. We inherit all of this, but our workload is different:

| Metric | World Monitor | Vessel Monitor | Notes |
|--------|--------------|----------------|-------|
| Data sources | 500+ feeds, 65+ APIs | 1 MQTT broker | Massively simpler |
| Map markers | 1,000-10,000 | 10-100 AIS targets | Much lighter |
| Update frequency | 5-30 min | 1-5 seconds | Much faster |
| Concurrent panels | 8-15 | 4-8 | Similar |
| AI synthesis | Every 30 min | Every 15 min | Similar |
| Bundle size | ~2MB gzipped | ~1.2MB est. | Smaller after stripping |

The higher update frequency (1Hz sensor data vs. 20-minute news feeds) is the key difference. World Monitor's render loop assumes data changes every few minutes. We need 60fps gauge animation on 1Hz data updates.

**Solution:** Canvas-based gauges (not DOM elements) for engine data. Use `requestAnimationFrame` with interpolation between sensor readings. The gauges animate smoothly between updates even when data arrives at 1Hz.

---

## 10. Deployment

### 10.1 On the Vessel

```
[Marine WiFi Router]
  ├── [Raspberry Pi 5]
  │     ├── mosquitto (MQTT broker)
  │     ├── Ollama (LLM server)
  │     └── Vessel Monitor (Tauri app)
  │
  ├── [Bridge Display] (4K TV, wired)
  │     └── Browser → http://raspberrypi:3000
  │
  ├── [Engine Room Tablet] (WiFi)
  │     └── Browser → http://raspberrypi:3000#engine-room
  │
  └── [Crew Phones] (WiFi)
        └── Browser → http://raspberrypi:3000#galley
```

Wait — this has a backend (Raspberry Pi). That contradicts "no backend."

**Clarification:** "No backend" means no server-side application logic, no database server, no API server. The Raspberry Pi runs:
1. **mosquitto** — a message broker, not an application server
2. **Ollama** — a model server, not application logic
3. **A static file server** — serving the Vite build (could be `nginx`, `python -m http.server`, or Tauri itself)

Alternatively, the Tauri desktop app runs on the bridge computer directly, and MQTT/Ollama are the only network services. The Tauri app serves the frontend to itself; crew phones connect to a lightweight static server or the Tauri app's built-in server.

### 10.2 Build & Deploy

```bash
# Development
npm run dev                    # Vite dev server, connects to localhost MQTT

# Production (Tauri desktop)
npm run desktop:tauri:build   # Cross-compile for target OS

# Production (PWA static)
npm run build                 # Output in dist/, serve with any static server
```

---

## 11. Security Model

World Monitor has Clerk auth, API keys, payment gating, rate limiting, CSRF tokens, and session management. Vessel Monitor needs none of this.

**Security boundary:** The vessel's WiFi network. If you're on the boat's WiFi, you can see the dashboard. That's the entire auth model.

The MQTT broker has no authentication (it's on a closed network). Ollama has no authentication (localhost only). The Tauri app runs as the current user.

This is not a security gap — it's appropriate trust boundaries for a single-vessel system. Adding auth would add complexity without value.

---

## 12. Extension Points

### 12.1 Satellite Internet (future)

When Starlink Maritime is available:
- Weather forecast panel (fetch from NOAA API)
- Chart updates (download new PMTiles)
- Fleet positions (if sister vessels report via satellite)
- Remote monitoring (shore-side dashboard mirror)

Add these as optional services that activate when internet is detected, following World Monitor's feature-flag pattern (`runtime-config.ts`).

### 12.2 Additional Sensors

The MQTT topic structure is extensible:

```
vessel/sensors/esp32_3/{metric}    # New ESP32
vessel/sensors/thermal/{zone}      # Thermal camera
vessel/sensors/radar/{contact}     # Marine radar interface
vessel/sensors/ais/base_station    # AIS base station (vs receiver)
```

New sensors require only:
1. ESP32 publishing to the right topic
2. A panel that subscribes to it

### 12.3 Multi-Vessel Fleet

If the vessel joins a fleet:
- Shared AIS data via MQTT (broker relays between vessels)
- Fleet position overlay on map
- Catch coordination (see where fleet is catching)

This is World Monitor's multi-source pattern scaled down to a handful of nodes instead of 65+ APIs.
