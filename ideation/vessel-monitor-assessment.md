# Vessel Monitor: Fork-or-Build Assessment

**Repo examined:** `https://github.com/SuperInstance/vessel-monitor` (World Monitor)  
**Local clone:** `/tmp/vessel-monitor`  
**Existing stack referenced:** `sensor-bridge/` in this workspace  
**Assessment date:** 2026-08-05

## 1. Verdict in one paragraph

World Monitor is a **full-stack SaaS intelligence platform**, not a self-contained frontend. A "strip the world feeds, keep the maps" fork is possible in principle, but the strip is large enough that you would spend more time deleting, detangling, and rewriting backend assumptions than you would spend building a clean vessel dashboard from the same foundational libraries. The right move is **not to fork the whole repo**. Instead, **extract the useful pieces** (deck.gl/globe.gl map shell, Panel base class, variant config pattern, refresh scheduler, circuit-breaker utilities) into a new, smaller TypeScript/Vite project that speaks MQTT/WebSocket and local SQLite, with Ollama running on the boat's PC or a Tauri sidecar. Whether to call Fable depends on how much architectural risk you want to remove: the high-level spec is straightforward, but the "no backend" constraint, offline basemaps, MQTT-to-browser bridge, and Vessel Health Index scoring all deserve a proper architecture pass. If this is meant to become a real product, **call Fable**. If it is a weekend prototype, start from this spec and iterate.

## 2. Architectural reality check: what World Monitor actually is

Reading the repo confirms the README claims but reveals the weight underneath:

| Surface | What it really is | Relevance to a vessel dashboard |
|---|---|---|
| Frontend SPA | Vanilla TypeScript + Vite, dual map engine (deck.gl flat map + globe.gl), 107 Panel subclasses | High — this is the part you want |
| 56 map layer types | Defined in `src/config/map-layer-definitions.ts`; renderers split between flat/globe/SVG/mobile | Medium — keep the engine, replace the layers |
| 500+ news feeds | RSS/Google News proxies ingested via Edge Functions + Railway relay | Strip entirely |
| 65+ upstream APIs | Finnhub, Yahoo, CoinGecko, ACLED, UCDP, GDELT, FIRMS, Wingbits, etc. | Strip entirely |
| API layer | 60+ Vercel Edge Functions in `api/`, sebuf proto contracts, Redis caching, rate limiting, API keys | Strip entirely; you said no backend |
| AIS service | `src/services/maritime/index.ts` fetches a **global vessel snapshot** from a server RPC every 5 min | Replace with local MQTT/AIS receiver or a tiny forwarder |
| Country Instability Index | Server-authoritative composite score in `src/services/cached-risk-scores.ts` + `CIIPanel.ts` | Replace with client-side Vessel Health Index |
| Finance radar | `src/services/market/index.ts` + MarketServiceClient RPCs | Replace with catch/market radar backed by local log or external fish-price API |
| AI synthesis | `DailyMarketBriefPanel` / `daily-market-brief.ts` calls `/api/chat-analyst` or summarizer Edge Functions | Replace with local Ollama calls (Transformers.js already in deps) |
| 6 site variants | `src/config/variants/{full,tech,finance,commodity,energy,happy}.ts`, hostname or `VITE_VARIANT` driven | Keep the pattern; redefine for vessel views |
| Tauri desktop | Rust shell + Node.js sidecar that dynamically loads Edge Functions | Optional but attractive for a boat PC; reuse the pattern if you go desktop |
| i18n | 26 locale files | Strip or collapse to 2–3 languages |
| License | AGPL-3.0-only | Forking binds you to AGPL; clean-build avoids copyleft entanglement |

The critical insight: **the value of World Monitor is in its data pipeline and backend contracts, not its presentation code.** For a single vessel you do not need 90% of that pipeline.

## 3. What to keep

Keep the **presentation and local-state machinery** and little else:

1. **Map rendering stack** — `DeckGLMap.ts`, `GlobeMap.ts`, the map container, layer picker, and the flat/globe toggle. The dual engine is overkill for a vessel dashboard but it is already built and performs well.
2. **Panel system** — `src/components/Panel.ts`, the resizable grid in `src/app/panel-layout.ts`, and `STORAGE_KEYS` persistence. This gives you draggable, resizable, stateful widgets for free.
3. **Variant config pattern** — `src/config/variant.ts`, `src/config/variants/base.ts`, and the per-variant `DEFAULT_PANELS` / `DEFAULT_MAP_LAYERS`. It is exactly the right shape for vessel/engine-room/chart-plotter/fish-finder/fleet-map/logbook views.
4. **Refresh scheduler** — `src/app/refresh-scheduler.ts` (`startSmartPollLoop`) already handles viewport-conditional refresh, tab pause, backoff, and staggered flush.
5. **Circuit breakers + data freshness** — `src/utils/circuit-breaker.ts` and `src/services/data-freshness.ts` are useful for MQTT dropouts and flaky sensors.
6. **Local AI path** — The repo already supports Ollama/Transformers.js. For a vessel dashboard, make Ollama the **only** AI path.
7. **Tauri desktop shell** (optional) — If the dashboard runs on a boat PC, `src-tauri/` gives you a native window, keyring storage, and a Node sidecar that can talk directly to MQTT without a separate bridge process.

## 4. What to strip

Strip anything that assumes a cloud backend, multi-tenant auth, or global data ingestion:

- `api/` (all 60+ Edge Functions)
- `server/` (gateway, handlers, proto services)
- `convex/` (billing, entitlements, user state)
- `workers/` (Cloudflare CORS preflight)
- `scripts/` (seed loops for news, markets, conflict, etc.)
- `cli/`, `sdk/`, `blog-site/`
- All RSS/news feed config in `src/config/feeds.ts`
- All market symbol configs except any you repurpose for seafood pricing
- `src/services/{news,market,intelligence,prediction,aviation,cyber,conflict,military,displacement,economic,trade,supply-chain,consumer-prices,wildfires,webcams,giving,...}`
- Premium/entitlement gating (`src/services/entitlements.ts`, `panel-gating.ts`, `premium-fetch.ts`)
- Auth/session flows (`src/services/auth-state.ts`, Clerk, OAuth)
- 26 locales; keep English + maybe Spanish/French for crew
- Most static datasets in `src/data/`, `shared/`, `data/`
- Docker/Vercel/Railway deployment files
- All CI workflows except a minimal typecheck/test/build

Stripping this by hand is feasible but error-prone. The imports are dense, and many panels call `/api/*` or generated RPC clients transitively.

## 5. What to replace

### 5.1 Map layers for a vessel

Current World Monitor layers that survive (renamed/repurposed):

| WM layer key | Vessel replacement | Data source |
|---|---|---|
| `ais` | **Own vessel + nearby traffic** | Local AIS receiver (USB SDR or NMEA 0183/2000 over serial/UDP) |
| `weather` | **Weather alerts + GRIB wind/pressure** | NOAA/NWS/Open-Meteo (cacheable) or downloaded GRIB files |
| `natural` | **Seismic / tsunami warnings** | USGS / NOAA tsunami feeds |
| `waterways` | **Shipping lanes, Traffic Separation Schemes, EEZ boundaries** | OpenSeaMap / NOAA ENC / local S-57/S-101 if licensed |
| `cables` | **Undersea cables** (keep as navigation hazard) | TeleGeography or OpenStreetMap |
| `pipelines` | **Subsea pipelines / oil infrastructure** | Local charts or open data |
| `ciiChoropleth` | **Vessel Health Index choropleth** — not geographic, but use the same color-scale component for system health | Derived from sensor history |
| *(new)* | **Bathymetry / depth contours** | NOAA bathymetry tiles, GEBCO, or local sonar log |
| *(new)* | **Currents / tides** | HYCOM / Copernicus / local tide station API |
| *(new)* | **Fishing grounds / closed areas / MPAs** | NOAA fishery closures, local regulatory GeoJSON |
| *(new)* | **Waypoints, routes, tracks** | Local GPX / route store |
| *(new)* | **Navigation aids (AIS AtoN, buoys, lights)** | OpenSeaMap + local AIS |

Layers to drop: conflicts, military, nuclear, protests, sanctions, stock exchanges, central banks, tech HQs, datacenters, commodity hubs, displacement, fires, disease outbreaks, etc.

### 5.2 Data streams replacing news feeds

Instead of 500 RSS feeds, you have a small, fixed set of local streams:

| Stream | Source | Topic / format | Replaces WM's... |
|---|---|---|---|
| Engine telemetry | `sensor-bridge` MQTT `vessel/engine_ensign_1/sensors/+` | RPM, coolant temp, oil pressure, battery voltage, fuel rate | `markets`, `economic`, `energy` panels |
| Bilge / environmental | Additional ESP32 or NMEA 2000 | Bilge pump cycles, holding tank levels, fridge temp, freezer temp | `climate`, `infrastructure` panels |
| GPS / GNSS | GPS/AIS receiver or NMEA | Lat/lon, SOG, COG, heading, fix quality | Core map viewport |
| Depth sounder | NMEA 0183 DPT/DBT or sonar log | Depth below transducer | New depth layer |
| Catch log | Manual entry or scale/RFID integration | Species, weight, count, timestamp, position | `markets`, `commodities` |
| Fleet positions | Local VHF/AIS or satellite AIS API if internet | MMSI, name, lat/lon, COG, SOG | Global `ais` layer |
| Weather | GRIB file or Open-Meteo | Wind, pressure, temperature, precipitation | `weather` layer |
| Currents/tides | Copernicus / NOAA tide API | Current vectors, tide height | New layer |
| Alerts | `sensor-bridge` escalation output | Warning/alert/critical events | `breaking-news` banner |

The existing `sensor-bridge` already normalizes readings, detects patterns, and emits escalations. The dashboard should consume its MQTT topics directly (or via a thin bridge) rather than trying to recreate that logic.

### 5.3 AI synthesis for a vessel

Replace the daily market brief with vessel-specific briefs:

| WM feature | Vessel equivalent | Inputs |
|---|---|---|
| Morning briefing | **Captain's morning brief** | GPS track, weather forecast, engine status overnight, bilge alerts, catch log yesterday, planned route | 
| Delta reports | **Ensign delta report** (`sensor-bridge` pattern events + trend changes since last watch) | Coolant temp drift, oil pressure drop, battery voltage sag, fuel rate anomaly |
| Market implications | **Catch/market radar** | Yesterday's catch, local dock prices (API or manual), weather window, quota remaining |
| AI forecasts | **Weather/fish predictions** | GRIB forecast, SST charts, historical catch by location/time |
| Chat analyst | **Onboard AI mate** | Ask natural-language questions about engine state, weather, catch, maintenance |

All of these should call a **local Ollama instance** (e.g. `llama3.1`, `qwen2.5`, or a small fine-tune) with structured prompts built from the local data store. The World Monitor `ml.worker.ts` and Transformers.js path are useful references, but for a boat you want a single local model, not a cloud summarizer.

### 5.4 Country Instability Index → Vessel Health Index

This is a clean mapping:

| CII component | VHI component | Sensors / data |
|---|---|---|
| Unrest | **Mechanical stress** | RPM variance, coolant temp, oil pressure, exhaust temp |
| Conflict | **Active alerts** | `sensor-bridge` escalations (level 2/3), AIS CPA/TCPA alarms |
| Security | **Safety systems** | Bilge pump frequency, battery voltage, fire/smoke sensors, EPIRB status |
| Information | **Data quality / connectivity** | MQTT dropouts, GPS fix quality, AIS message rate, weather data age |

`CIIPanel.ts` can be renamed/rethemed to `VesselHealthPanel.ts`. The score computation should move from a server RPC to a **client-side function** reading from IndexedDB/SQLite sensor history and the current alert register. Keep the same 5-level color scheme (`critical`/`high`/`elevated`/`normal`/`low`) and the trend arrows — they communicate perfectly for a vessel.

### 5.5 Finance radar → catch/market radar

Replace market quotes with:

- **Catch dashboard**: species, weight, count, by trip and by day, with running totals vs quota.
- **Hold inventory**: what is in the hold, ice/fuel state, estimated value.
- **Dock price radar**: if internet is available, pull local fish-market prices; otherwise manual entry with simple trend.
- **Fuel efficiency**: L/h per NM, per kg catch, trend vs engine health.
- **Weather window economics**: cost of staying out vs running for shelter.

The `DailyMarketBriefPanel.ts` layout is reusable: title/summary/action plan/risk watch/items. Change the items from stock symbols to species/markets.

### 5.6 Six site variants → six vessel views

World Monitor's variant pattern maps cleanly:

| WM variant | Vessel view | Default panels | Default layers |
|---|---|---|---|
| `full` | **Vessel dashboard** | VHI, map, weather, alerts, catch log, engine summary | weather, own-ship AIS, bathymetry, waypoints |
| `tech` | **Engine room** | Engine gauges, bilge, battery, fuel, alerts, maintenance log | (no map, or mini map) |
| `finance` | **Catch/market radar** | Catch log, hold inventory, dock prices, fuel efficiency, trip summary | fishing grounds, EEZ/closures |
| `commodity` | **Chart plotter** | Full-screen chart, route planning, waypoints, tracks, nav aids | bathymetry, lanes, nav aids, own ship |
| `energy` | **Fish finder / sonar** | Depth history, bottom classification, temperature profile, catch marks | depth contours, sonar targets |
| `happy` | **Fleet map** | Nearby fleet positions, buddy boats, anchorages, communication log | fleet AIS, anchorages, weather |

A seventh view, **Logbook**, can be a dedicated full-screen panel rather than a variant: editable trip log with auto-captured GPS/weather/catch entries.

## 6. The "no backend" gotcha

World Monitor has no true offline mode: even the desktop app runs a Node.js sidecar that loads Edge Functions and talks to upstream APIs. For a vessel dashboard, "no backend" needs definition:

| Option | What it means | Feasibility |
|---|---|---|
| **Pure browser app** | Dashboard loads from static files; MQTT must be served over WebSockets | Possible only if the boat's MQTT broker (Mosquitto/EMQX) is configured for WebSockets on a known port. Browsers cannot do raw TCP MQTT. |
| **Browser + tiny local bridge** | A Python/Node process converts MQTT → WebSocket, or serves the SPA and proxies MQTT | Practical. The bridge can be the existing `sensor-bridge` extended with a small WebSocket server, or a separate `vessel-bridge` service. |
| **Tauri desktop app** | Rust shell + Node sidecar subscribes to MQTT natively and exposes data to the frontend via Tauri commands | Most robust for a boat PC. Reuses WM's Tauri pattern. The sidecar is still "backend" but it is local and bundled. |
| **Single binary (Tauri + sidecar + Ollama)** | Install one app on the boat's PC; it bundles MQTT client, SQLite, map tiles, and model runner | The ideal end-state, but heavier than a web build. |

**Recommendation:** do not pretend this is frontend-only. Plan for a **local runtime** (Tauri sidecar or small Python bridge) that owns MQTT, SQLite, and Ollama. The dashboard UI is then a thin layer over local APIs.

## 7. Offline and map-tile strategy

A fishing vessel will have intermittent internet. The map cannot rely on MapLibre fetching tiles from a CDN:

- **Basemap**: ship an offline vector tile package (MBTiles/PMTiles) for the operating region using `pmtiles` (already a dependency). World Monitor already uses PMTiles in `src/config/basemap.ts`.
- **Bathymetry**: pre-download NOAA/GBCO tiles or contours for the fishing grounds.
- **Weather**: download GRIB files before leaving port; render wind barbs/pressure isobars locally with deck.gl PathLayer/IconLayer.
- **Charts**: NOAA raster charts are free for US waters; ENC vector data requires a chart engine. For a prototype, OpenSeaMap + bathymetry is enough.
- **Updates**: when internet is available, refresh weather, market prices, and regulatory closures; queue them in local SQLite for offline use.

## 8. License consideration

World Monitor is **AGPL-3.0-only**. If you fork and modify it, the resulting vessel dashboard is also AGPL and you must share source with anyone who uses the software. If this is a personal/research project, that is fine. If it might become a commercial product, a clean implementation avoids copyleft entanglement and lets you reuse the *ideas* without reusing the code. Extracting patterns and rewriting the components is legally safer and practically faster than stripping the AGPL repo.

## 9. Build recommendation: extract, don't fork wholesale

| Approach | Effort | Risk | Outcome |
|---|---|---|---|
| Fork + delete | 4–6 weeks | High — leftover backend imports, AGPL surface, broken variants | Bloated, hard to maintain |
| Extract map/panel/variant skeleton into new repo | 1–2 weeks | Low–medium | Clean, purpose-built vessel dashboard |
| Clean build from Vite + deck.gl + Preact/vanilla TS, borrowing snippets | 2–3 weeks | Medium | Cleanest architecture, slightly more upfront work |

Recommended path:

1. Create `vessel-dashboard/` as a new Vite + TypeScript project.
2. Copy **only** these concepts from World Monitor:
   - `Panel.ts` base class and grid layout
   - `DeckGLMap.ts` / `GlobeMap.ts` map shell
   - `variant.ts` + variant config pattern
   - `startSmartPollLoop`
   - `createCircuitBreaker`
3. Add:
   - MQTT client (MQTT.js over WebSocket, or Tauri native MQTT)
   - SQLite/IndexedDB time-series store
   - Ollama client for briefs and chat
   - PMTiles/offline basemap loader
   - NMEA 0183/2000 parser for GPS/depth/AIS
4. Build the six vessel views as variants.
5. Package as Tauri desktop app for the boat PC.

## 10. Should you call Fable?

Yes, with a bounded scope. The strip-down is **not** straightforward because of the "no backend" constraint, offline map requirements, and the need to redesign the AI synthesis and health-index scoring for a vessel context. Fable is worth it for the following deliverables:

1. **Architecture decision record** for the local runtime boundary: Tauri sidecar vs Python bridge vs pure browser + MQTT-WebSocket.
2. **Data model** for sensor readings, alerts, catch logs, routes, and weather snapshots, including the SQLite schema and sync strategy.
3. **Map layer specification** for vessel navigation, including tile sources, offline packaging, and rendering order.
4. **Vessel Health Index algorithm** — component weights, normalization, trend calculation, and escalation mapping.
5. **AI prompt architecture** for the captain's brief, delta reports, and onboard chat, including context window management and local model selection.
6. **Six-variant panel defaults** and a migration path to add more views.

If you just want a quick prototype, use this assessment as the spec and start building. If you want a maintainable product that a team can hand off, call Fable to produce the architecture docs and component boundaries before anyone writes production code.

## 11. Concrete next steps

1. Decide the runtime boundary: Tauri desktop app (recommended) or browser + local bridge.
2. Confirm MQTT broker setup on the boat: does Mosquitto expose WebSockets, or do you need a bridge?
3. Define the sensor topic contract between `sensor-bridge` and the dashboard; reuse `vessel/{device_id}/sensors/{sensor}` and add `vessel/{device_id}/alerts`.
4. Prototype the map shell with deck.gl + PMTiles + one sensor overlay.
5. Implement the Vessel Health Index panel as the first feature; it validates the data pipeline end-to-end.
6. Add Ollama local brief generation once the data store is populated.
7. Only then build the six variants and polish.

---

**Bottom line:** World Monitor is an impressive global-intelligence product, but its value is in backend data pipelines you do not need. Do not fork the whole repo. Extract the presentation skeleton, replace every data source with local MQTT/NMEA/SQLite streams, and rebuild the intelligence layer around the boat. Call Fable if you want the architecture locked before coding; otherwise, this assessment is enough to start a prototype.
