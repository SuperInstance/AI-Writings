# Vessel Monitor — Fork Plan

**Source:** [World Monitor](https://github.com/koala73/worldmonitor) v2.10.0 (AGPL-3.0)
**Target:** Single-vessel monitoring dashboard (front-end only, MQTT-fed, Tauri desktop)
**Date:** 2026-08-04

---

## 1. What World Monitor Actually Is

World Monitor is a real-time global intelligence dashboard built in vanilla TypeScript + Vite. It aggregates 500+ news feeds, geopolitical events, financial market data, infrastructure status, and military activity into a unified situational awareness interface. It ships as 6 site variants (`world`, `tech`, `finance`, `commodity`, `happy`, `energy`) from a single codebase, runs as a web app (Vercel) or native desktop app (Tauri 2), and uses a dual map engine: globe.gl for 3D and deck.gl/MapLibre for flat WebGL rendering with 56 layer types.

The codebase is **778 TypeScript source files** in `src/`, plus a Tauri Rust shell, a Node.js sidecar server, API edge functions, SDK libraries in Python/Ruby/Go, a CLI, and 290 protobuf definitions.

The key insight: World Monitor is already a sensor dashboard. Its sensors happen to be RSS feeds and geopolitical APIs instead of ESP32s and NMEA 0183 sentences. The architecture — real-time data ingestion → state management → layered map visualization → AI synthesis → panel-based dashboard — maps directly onto vessel monitoring with a change of data source.

---

## 2. What to KEEP

### 2.1 Core Infrastructure (untouched or lightly modified)

| Component | Files | Why Keep It |
|-----------|-------|------------|
| **Vite + TypeScript build pipeline** | `vite.config.ts`, `tsconfig.json`, `package.json` | Battle-tested, PWA support, chunk splitting, env injection. Keep the whole build config. |
| **Panel system** | `src/components/Panel.ts` (1,427 lines) | The draggable/collapsible/resizable panel framework is the skeleton of the dashboard. Every gauge, readout, and chart lives in a Panel. |
| **MapContainer** | `src/components/MapContainer.ts` (1,621 lines) | The lazy-loading conditional renderer (SVG → deck.gl → globe.gl). Keep the architecture; swap the layers. |
| **deck.gl map engine** | `src/components/DeckGLMap.ts` (7,904 lines) | The WebGL renderer with 56 layer types. We keep the engine and maybe 6-8 layers. Strip the rest. |
| **globe.gl 3D globe** | `src/components/GlobeMap.ts` (3,970 lines) | A 3D globe is genuinely useful for a vessel — you see your position on Earth. Keep the marker system, auto-rotate, and atmosphere rendering. |
| **Tauri 2 desktop shell** | `src-tauri/` (Rust + sidecar) | Native desktop app with keyring secret management, local API proxy, multi-window support. Keep the shell; replace the sidecar. |
| **Settings/Preferences** | `src/services/settings-manager.ts`, `src/components/UnifiedSettings.ts` | Settings persistence, runtime config, feature flags. |
| **i18n** | `src/services/i18n.ts`, `src/config/` | 26-language support. Keep the infrastructure; we'll only need English (and maybe Korean/Chinese for crew). |
| **IndexedDB storage** | `src/services/` (various) | Already uses IndexedDB for persistence. Perfect for sensor data logging. |
| **ML Worker** | `src/workers/ml.worker.ts`, `src/services/ml-worker.ts` | ONNX inference in a Web Worker — sentiment, NER, summarization, vector search. Keep for local AI. |
| **Vector DB** | `src/workers/vector-db.ts` | In-browser vector database for semantic search. Useful for log search and pattern matching. |
| **PWA / Service Worker** | `vite-plugin-pwa` config | Offline support is critical for a vessel. Keep the PWA layer. |

### 2.2 Architecture Patterns (keep, adapt naming)

- **Variant system** (`src/config/variant.ts`, `src/config/variants/*.ts`) — The 6-variant pattern (each variant exports its own `DEFAULT_PANELS`, `DEFAULT_MAP_LAYERS`, `FEEDS`) becomes our view system: `bridge`, `engine-room`, `deck`, `galley`, `captain`. Same code, different panel selections.
- **Smart poll loop** (`src/services/smart-poll-loop.ts`) — Adaptive refresh intervals per data source. We need this: engine data at 1Hz, GPS at 5Hz, AIS at 30s, catch log on-demand.
- **Circuit breaker** (`src/utils/` — `createCircuitBreaker`) — Prevents sensor failure cascades. If ESP32 #3 stops responding, don't freeze the dashboard.
- **Data freshness tracking** (`src/services/data-freshness.ts`) — Age-based staleness indicators. Critical for knowing your sensor data is live vs. cached.

---

## 3. What to STRIP

### 3.1 Global Intelligence Domain (remove entirely)

| Remove | Files/Dirs | LOC Saved (est.) |
|--------|-----------|-----------------|
| News feeds & RSS proxy | `src/services/news/`, `api/rss-proxy.js`, feed configs | ~8,000 |
| Geopolitical panels | 60+ panel components in `src/components/` (CountryBriefPanel, SanctionsPressurePanel, MilitaryCorrelationPanel, etc.) | ~25,000 |
| Global data services | `src/services/conflict/`, `src/services/military-bases.ts`, `src/services/displacement/`, `src/services/unrest/`, `src/services/trade/`, `src/services/supply-chain/`, `src/services/prediction/`, `src/services/research/` | ~12,000 |
| Financial panels | StockAnalysisPanel, YieldCurvePanel, ETFFlowsPanel, DailyMarketBriefPanel, etc. | ~15,000 |
| Finance/energy/commodity configs | `src/config/finance-geo.ts`, `src/config/commodity-geo.ts`, `src/config/markets.ts`, etc. | ~5,000 |
| Vercel Edge Functions | `api/` directory (60+ endpoints) | ~10,000 |
| Auth/payment system | Clerk auth, DodoPayments, Convex, widget-store, panel-gating, premium-fetch | ~8,000 |
| Protocol Buffers | `src/generated/` (290 protos, 35 services) | ~6,000 |
| SDK libraries | `cli/`, `sdk/python/`, `sdk/ruby/`, `sdk/go/` | ~5,000 |
| Blog/docs site | `blog-site/`, `docs/` | n/a |
| Correlation engine | `src/services/correlation-engine/` (global event correlation) | ~2,000 |
| Analysis worker | `src/workers/analysis.worker.ts` (news analysis) | ~1,500 |
| Military/aviation services | `src/services/military-base-config.ts`, `src/services/aviation.ts` | ~3,000 |
| Webcam system | `src/services/webcams/`, `LiveWebcamsPanel.ts` | ~2,000 |
| Social/community | `src/services/social-velocity.ts`, `CommunityWidget.ts`, TelegramIntelPanel | ~3,000 |
| Climate/environmental | `src/services/climate.ts`, `src/services/wildfires.ts`, `SatelliteFiresPanel` | ~2,000 |

**Total stripped:** ~100,000+ lines. What remains: ~20,000 lines of core infrastructure.

### 3.2 Map Layers to Strip

From the 56 layer types in `map-layer-definitions.ts`, strip all but:

| Keep | Adaptation |
|------|-----------|
| `ais` (Ship Traffic) | **Core feature** — AIS vessel positions around us |
| `weather` (Weather Alerts) | **Keep** — marine weather overlays |
| `natural` (Natural Events) | **Keep** — storm tracks, tsunami warnings |
| `ciiChoropleth` | **Adapt** → Vessel Health Index choropleth (see below) |

Strip everything else: military, conflicts, sanctions, cables, pipelines, stock exchanges, financial centers, datacenters, protests, displacement, GPS jamming, spaceports, satellites, tech hubs, cloud regions, etc.

---

## 4. What to REPLACE

### 4.1 Conceptual Mappings

| World Monitor Concept | Vessel Monitor Replacement |
|----------------------|---------------------------|
| Country Instability Index (CII) | **Vessel Health Index (VHI)** — composite score from engine temp, oil pressure, fuel level, battery voltage, bilge water, vibration |
| Global threat alerts | **Vessel alerts** — collision risk, shallow water, engine overtemp, low fuel, sensor offline |
| Cross-source signal correlation | **Sensor correlation** — engine RPM vs. fuel consumption, vibration vs. speed, depth vs. position |
| News synthesis (AI briefing) | **Watch log synthesis** — AI-generated watch log from sensor data ("Engine temp climbing 2°C/h, fuel at 40%, recommend inspection at next port") |
| Global map zoom-to-region | **Vessel-centric auto-follow** — map centers on vessel, zoom level follows speed |
| Regional intelligence panels | **Zone panels** — bridge, engine room, deck, galley (each shows relevant sensors) |
| Monitor customization | **Dashboard profiles** — captain, engineer, deckhand, observer (different panel layouts) |
| 500+ RSS feeds | **MQTT topics** — `vessel/engine/*`, `vessel/gps/*`, `vessel/sensors/*`, `vessel/depth/*`, `vessel/catch/*`, `vessel/ais/*` |
| Feeds config (`src/config/feeds.ts`) | **Sensor config** — topic definitions, sampling rates, alert thresholds, sensor metadata |

### 4.2 File-Level Replacement Plan

#### `src/config/` — Replace all variant/feed/geo configs

| World Monitor File | Vessel Monitor Replacement |
|-------------------|---------------------------|
| `variants/base.ts` | `variants/base.ts` — keep structure (REFRESH_INTERVALS, STORAGE_KEYS, MONITOR_COLORS), replace intervals |
| `variants/full.ts` | `variants/bridge.ts` — bridge view: map + engine + navigation + AIS + alerts |
| `variants/tech.ts` | `variants/engine-room.ts` — engine focus: gauges + trends + vibration + maintenance |
| `variants/finance.ts` | `variants/deck.ts` — deck view: catch log + weather + depth + position |
| `variants/happy.ts` | `variants/captain.ts` — overview: everything at 30,000 feet |
| `variants/energy.ts` | `variants/galley.ts` — minimal: position, ETA, weather |
| `variants/commodity.ts` | *(delete)* |
| `feeds.ts` | `sensors.ts` — MQTT topic registry, sample rates, alert thresholds |
| `geo.ts` | `vessel-geo.ts` — home port, fishing grounds, waypoints |
| `geo-map.ts` | `nav-aid.ts` — navigation aids: buoys, lighthouses, channels |
| `pipelines.ts` | *(delete)* |
| `military.ts` | *(delete)* |
| `markets.ts` | *(delete)* |
| `entities.ts` | `fleet.ts` — sister vessels, fleet positions |
| `map-layer-definitions.ts` | New layer registry: `vessel-track`, `ais-vessels`, `depth-contour`, `weather`, `catch-heatmap`, `waypoints`, `search-pattern` |
| `cii-colors.ts` | `vhi-colors.ts` — Vessel Health Index color scale |

#### `src/services/` — Replace data services

| World Monitor Service | Vessel Monitor Service |
|----------------------|----------------------|
| `news/` | *(delete)* — replaced by MQTT subscriber |
| `conflict/`, `displacement/`, `unrest/` | *(delete)* |
| `market/`, `economic/` | *(delete)* |
| `military-bases.ts`, `aviation.ts` | *(delete)* |
| `maritime/index.ts` | **Keep and expand** — AIS parsing already exists here |
| `ollama-models.ts` | **Keep** — local LLM model discovery |
| `summarization.ts` | **Adapt** — summarize sensor trends instead of news articles |
| `ml-worker.ts`, `ml.worker.ts` | **Keep** — ONNX inference for anomaly detection |
| `vector-db.ts` | **Keep** — semantic search over historical logs |
| `insights-loader.ts` | **Adapt** — load AI watch log instead of global insights |
| `correlation-engine/` | **Adapt** — engine RPM ↔ fuel flow, vibration ↔ speed correlation |
| `smart-poll-loop.ts` | **Keep** — adaptive sensor polling |
| `data-freshness.ts` | **Keep** — sensor staleness tracking |
| `tauri-bridge.ts` | **Keep** — Tauri IPC bridge |
| `runtime-config.ts` | **Keep** — runtime feature flags |
| `i18n.ts` | **Keep** — keep infra, reduce languages |
| `settings-manager.ts` | **Keep** |
| *(new)* `mqtt-client.ts` | **New** — MQTT over WebSocket client (connects to `ws://localhost:9001`) |
| *(new)* `nmea-parser.ts` | **New** — NMEA 0183 sentence parser for GPS, depth, heading |
| *(new)* `sensor-store.ts` | **New** — time-series store for sensor data (ring buffer + IndexedDB) |
| *(new)* `alert-engine.ts` | **New** — threshold-based alert system |
| *(new)* `catch-log.ts` | **New** — catch logging service |
| *(new)* `trip-recorder.ts` | **New** — trip recording and playback |

#### `src/components/` — Replace panels

| World Monitor Panel | Vessel Monitor Panel |
|--------------------|--------------------|
| `Panel.ts` | **Keep** — the shell |
| `MapContainer.ts` | **Keep** — the map shell |
| `DeckGLMap.ts` | **Keep + strip layers** — remove 48 of 56 layer types |
| `GlobeMap.ts` | **Keep** — 3D vessel-on-globe view |
| `Map.ts` | **Keep** — SVG fallback for low-end displays |
| `CountryBriefPanel.ts` | `VesselBriefPanel.ts` — vessel overview summary |
| `StrategicRiskPanel.ts` | `VesselHealthPanel.ts` — VHI composite gauge |
| `LiveNewsPanel.ts` | `AlertFeedPanel.ts` — scrolling alert feed |
| `StatusPanel.ts` | `SensorStatusPanel.ts` — sensor grid status |
| `MarketPanel.ts` | `EngineGaugePanel.ts` — analog-style engine gauges |
| `CountersPanel.ts` | `TripStatsPanel.ts` — trip statistics |
| `InsightsPanel.ts` | `WatchLogPanel.ts` — AI-generated watch log |
| `CorrelationPanel.ts` | `SensorCorrelationPanel.ts` — sensor correlation display |
| *(new)* | `DepthSounderPanel.ts` — real-time depth + bottom profile |
| *(new)* | `NavigationPanel.ts` — heading, SOG, COG, position, waypoint |
| *(new)* | `AISRadarPanel.ts` — AIS targets in radar-style display |
| *(new)* | `CatchLogPanel.ts` — catch entry and tally |
| *(new)* | `FuelBudgetPanel.ts` — fuel consumption tracking |
| *(new)* | `WeatherPanel.ts` — marine weather forecast |
| *(new)* | `CatchHeatmapPanel.ts` — historical catch positions on map |

#### `src-tauri/` — Adapt the desktop shell

| Component | Action |
|-----------|--------|
| `src/main.rs` | **Strip** auth, keyring, Convex, shared secret. Keep window creation, menu, multi-window. |
| `sidecar/local-api-server.mjs` | **Replace** with MQTT-to-WebSocket bridge (or remove entirely if frontend connects to MQTT directly) |
| `Cargo.toml` | **Strip** `keyring`, reduce dependencies |
| `tauri.conf.json` | **Update** productName, identifier, window title, CSP for MQTT |

#### `api/` — Delete entirely

All 60+ Edge Functions are for global intelligence data. Not needed.

---

## 5. The Variant System Recast

World Monitor's variant system is its most elegant feature. One binary, six products. The build-time switch (`VITE_VARIANT`) selects which panels, map layers, and data feeds are compiled in. At runtime in the desktop app, users switch variants via `localStorage`.

### Vessel Monitor Variants

| Variant | `VITE_VARIANT` | Panels | Map Focus | Refresh |
|---------|---------------|--------|-----------|---------|
| **Bridge** | `bridge` | Map + engine gauges + nav + AIS + alerts | Vessel-centric, 2nm radius | Engine 1s, GPS 5s, AIS 30s |
| **Engine Room** | `engine-room` | Engine gauges (large) + vibration trends + maintenance log + sensor grid | Minimal | Engine 500ms, sensors 1s |
| **Deck** | `deck` | Catch log + depth + position + weather | Vessel + fishing ground | Depth 1s, catch event-driven |
| **Captain** | `captain` | Everything at summary level + watch log + fuel budget + ETA | Vessel + fleet + destination | Relaxed 5-10s |
| **Galley** | `galley` | Position + ETA + weather only | Vessel position only | 30s |

Implementation: identical to World Monitor's pattern. Each variant file in `src/config/variants/` exports `DEFAULT_PANELS`, `DEFAULT_MAP_LAYERS`, and any variant-specific config. The `SITE_VARIANT` constant resolves at build time or from `localStorage` in the desktop app.

---

## 6. AI Synthesis Pipeline Recast

World Monitor's AI pipeline:
1. Collect articles from 500+ feeds
2. Cluster by topic (geographic + semantic)
3. Score importance (velocity, source count, threat level)
4. Synthesize into a daily brief via Ollama → Groq → OpenRouter fallback chain
5. Browser-side T5 fallback for offline summarization

Vessel Monitor's AI pipeline:
1. Collect sensor readings from MQTT (engine, GPS, depth, AIS, ESP32s)
2. Detect anomalies (threshold + ML-based via ONNX)
3. Correlate patterns (RPM vs. fuel, vibration vs. speed, depth vs. chart)
4. Synthesize into a watch log via **local Ollama only** (no cloud — vessel may have no internet)
5. Browser-side ONNX fallback for anomaly classification

The fallback chain simplifies: Ollama (primary, local) → ONNX (browser-side, always available). No Groq, no OpenRouter — those require internet, which a vessel may not have.

---

## 7. MQTT Integration

World Monitor has no MQTT. This is the biggest new piece.

### Architecture

```
ESP32 sensors ──→ MQTT Broker (mosquitto) ──→ WebSocket ──→ Frontend
                          │
GPS / NMEA ───────────────┤
AIS receiver ─────────────┘
```

### Topic Structure

```
vessel/engine/rpm              (float, 1Hz)
vessel/engine/temperature      (float, 1Hz)
vessel/engine/oil_pressure     (float, 1Hz)
vessel/engine/fuel_rate        (float, 1Hz)
vessel/engine/battery_voltage  (float, 0.5Hz)
vessel/engine/hours            (float, 0.1Hz)

vessel/gps/lat                 (float, 5Hz)
vessel/gps/lng                 (float, 5Hz)
vessel/gps/speed               (float, 5Hz)
vessel/gps/heading             (float, 5Hz)

vessel/depth/reading           (float, 1Hz)
vessel/depth/water_temp        (float, 0.2Hz)

vessel/sensors/{id}/{metric}   (varies per sensor)

vessel/ais/{mmsi}/position     (lat/lng, event-driven)
vessel/ais/{mmsi}/heading      (float, event-driven)
vessel/ais/{mmsi}/speed        (float, event-driven)
vessel/ais/{mmsi}/name         (string, on first contact)

vessel/catch/add               (JSON, event-driven)
vessel/alerts/threshold        (JSON, event-driven)
```

### Implementation

Use the `mqtt` npm package (already a dependency of World Monitor via `ws`). Connect over WebSocket to the local broker:

```typescript
import mqtt from 'mqtt';

const client = mqtt.connect('ws://localhost:9001', {
  clientId: `vessel-monitor-${Math.random().toString(16).slice(2)}`,
  clean: true,
  reconnectPeriod: 2000,
});

client.on('connect', () => {
  client.subscribe([
    'vessel/engine/#',
    'vessel/gps/#',
    'vessel/depth/#',
    'vessel/sensors/#',
    'vessel/ais/#',
    'vessel/catch/#',
  ]);
});
```

The MQTT client replaces World Monitor's entire fetch-based data ingestion layer. Everything downstream (panels, map, alerts) reads from the same state stores, which are now fed by MQTT messages instead of HTTP responses.

---

## 8. Stripping Summary

| Category | World Monitor LOC | Vessel Monitor LOC | Delta |
|----------|-------------------|-------------------|-------|
| Core infra (Vite, Panel, MapContainer, Tauri shell) | ~25,000 | ~25,000 | 0 |
| Map engines (deck.gl + globe.gl + SVG) | ~16,000 | ~8,000 | -8,000 (strip layers) |
| Panel components | ~30,000 | ~8,000 | -22,000 |
| Services | ~25,000 | ~8,000 | -17,000 |
| Config | ~8,000 | ~2,000 | -6,000 |
| API edge functions | ~10,000 | 0 | -10,000 |
| Generated protos | ~6,000 | 0 | -6,000 |
| SDK/CLI/Blog/Docs | ~10,000 | 0 | -10,000 |
| **New: MQTT, NMEA, sensors, alerts** | 0 | ~5,000 | +5,000 |
| **Total** | **~130,000** | **~56,000** | **-74,000** |

---

## 9. Migration Path

### Phase 1: Strip (Week 1-2)
- Fork repo, rename to `vessel-monitor`
- Delete `api/`, `cli/`, `sdk/`, `blog-site/`, `docs/`
- Delete all geopolitical/financial panel components
- Delete all global data services
- Strip deck.gl layer definitions to the 4-6 we need
- Get it to compile: `npm run build` should produce a working (empty) dashboard

### Phase 2: MQTT (Week 3)
- Add `mqtt` package, implement `mqtt-client.ts`
- Create `sensor-store.ts` (ring buffer + IndexedDB persistence)
- Wire MQTT → state → a basic position panel and engine gauge
- Test with mock MQTT broker (`mosquitto` in Docker)

### Phase 3: Vessel Panels (Week 4-5)
- Build `EngineGaugePanel` (analog gauges: RPM, temp, oil, fuel)
- Build `NavigationPanel` (position, heading, SOG, COG, waypoint)
- Build `DepthSounderPanel` (real-time + bottom profile)
- Build `AlertFeedPanel` (scrolling alerts with severity levels)
- Adapt `AISRadarPanel` from existing `maritime/` service
- Adapt map: vessel-centric auto-follow, track breadcrumb

### Phase 4: Variants (Week 6)
- Create 5 variant configs (bridge, engine-room, deck, captain, galley)
- Panel layout per variant
- In-app variant switching (Tauri desktop)

### Phase 5: AI (Week 7-8)
- Adapt summarization pipeline for sensor trend synthesis
- Implement watch log generation via local Ollama
- ONNX anomaly detection model (train or use pre-built)
- Vector search over historical trips

### Phase 6: Polish (Week 9-10)
- Tauri multi-window (bridge display + engine room display)
- Catch log module
- Trip recording and playback
- Offline data export (CSV/JSON)
- Marine chart integration (NOAA ENC tiles via deck.gl)

---

## 10. Dependencies

### Keep from World Monitor
- `@deck.gl/core`, `@deck.gl/layers`, `@deck.gl/mapbox` — map rendering
- `globe.gl` — 3D globe
- `maplibre-gl` — base maps
- `preact` — UI framework
- `i18next` — internationalization
- `marked` — markdown rendering
- `onnxruntime-web` — local ML inference
- `ws` — WebSocket support (also used by mqtt)
- `zod` — schema validation
- `pmtiles` — map tiles

### Add
- `mqtt` — MQTT client (npm package, uses `ws` underneath)
- `nmea-0183` — NMEA sentence parser (or write our own — the format is simple)
- `claygl` or `g2` — gauge rendering (optional, can use canvas/SVG)

### Remove (partial list)
- `@anthropic-ai/sdk` — no cloud AI
- `@aws-sdk/client-s3` — no S3
- `@clerk/clerk-js` — no auth
- `convex` — no backend DB
- `@dodopayments/convex` — no payments
- `@upstash/redis`, `@upstash/ratelimit` — no server caching
- `@vercel/functions`, `@vercel/og`, `@vercel/analytics` — no Vercel
- `@sentry/browser` — no error reporting (or keep for local dev)
- `satellite.js` — no satellite tracking
- `youtubei.js` — no YouTube
- `telegram` — no Telegram
- `hls.js` — no video streaming

---

## 11. License Considerations

World Monitor is AGPL-3.0. Forking and modifying triggers AGPL obligations if distributed or made available over a network. For a private vessel dashboard not distributed to third parties, AGPL obligations are minimal. If we later distribute the app to other vessels, we must publish source under AGPL-3.0.
