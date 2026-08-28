# FISHNET-MAP — Fleet Repos vs. the Five-Layer Fishing-Intelligence Vision

*Compiled 2026-08-27 by bulk scouting pass (local clones under ~/projects + `gh api repos/SuperInstance/<repo>/readme`). Purpose: feed the flagship paper draft. Accuracy over flourish — test counts quoted only where a README states them.*

**The vision (Riker's five layers):** (1) physics substrate / NMEA; (2) perception field (JEPA-style embeddings, hindsight-labeled by catch outcomes); (3) fleet memory (cell-ledger catch events as keel identity, merkle-rooted, local boat brains, federated); (4) market loop (sort-table/scale/buyer data closing the loop, conservation-governed); (5) Wesley the watcher (attention agent grown from video history).

---

## Layer Table

| Layer | Primary repo(s) | Status one-liner |
|---|---|---|
| 1. Physics substrate (NMEA/sensors/edge) | **vessel-agent-system (AELMA)**, engine-ensign, sensor-bridge, quilt-esp32, quilt-jetson (GH-only), sonar-vision | AELMA is the real NMEA-ingesting twin; the rest are edge-hardware or simulation organs |
| 2. Perception field (JEPA) | **elephant**, plato-vision-jepa, hermes-perception, slackwater-perception, quilt-vision, OpenRoom | Working JEPA-ish room/echogram perception exists, but none is hindsight-labeled by catch outcomes |
| 3. Fleet memory (cell ledger + merkle + federation) | **MerkleMesh**, quilt-rust, quilt-fleet, fleet-memory, AgentCompute, quilt-cell-bridges, cell-cascade, fleet-embed | Merkle-rooted cell-ledger federation is proven in libraries; not yet wired to catch events or boat-to-boat |
| 4. Market loop (sort/scale/buyer, conservation) | fishinglog-ai-site, captain-console, PersonalLog, crab-trap-web (adjacent) | **Thinnest layer** — a landing page, a notes ledger, a personal journal; no scale/buyer/sort-table data anywhere |
| 5. Wesley the watcher | **wesley**, wesley-curriculum, the-listeners-ear, fleet-audio, fleet-scribe, murmur-agent | A growing small local model + emotional/attention organs exist; no deck-camera video history feeding it |

---

## Per-Repo Notes

### Layer 1 — Physics substrate

- **vessel-agent-system (AELMA)** — Hardware-in-the-loop digital twin for F/V EILEEN (51-ft troller, SE Alaska). Ingests NMEA 0183 from GPS and sonar, fuses progressive bathymetry grid, live vessel state, safety watchers, failure prediction, crew fatigue, 3D browser view, LAN-only zero-internet. README claims: "334 files. 19,000+ lines of Python. 179 source files. 56 test files. Pure stdlib." Levels 1–2 (physical tensors, analytical features) still planned per its own BMAD table.
- **engine-ensign** — Git-native agent repo for ESP32 marine engine monitoring; agent lives in the repo beside the firmware it writes ("the Doctor in sickbay"). Two-agent Ensign/LaForge split (fast runtime loop vs paged reflective agent).
- **sensor-bridge** — ESP32 → MQTT → bridge → exocortex; normalize, pattern-detect, escalate, store. The sensory nervous-system router between Ensign (ESP32) and LaForge (repo agent).
- **quilt-esp32** — no_std Rust Quilt runtime for ESP32; README: "limb-blink verified on hardware (2026-08-26)" — compiled `.qm` rule table driving an LED on a real ESP32-S3, RAM 6.5%, flash 20.4%. Badge: tests 2/2.
- **quilt-jetson** (GH only, no local clone) — Quilt reactive runtime for NVIDIA Jetson (Orin/Nano/AGX), ROS2 Humble, edge ML/vision/federation. "The missing mid-tier" — README-level scaffold; CI badge says passing but no hardware-milestone claims like esp32's.
- **sonar-vision** — Pure-Python sonar simulation: pings, two-way propagation loss, synthetic echoes, tracking, 2-D occupancy grids. Stdlib-only; explicitly simplified physics for prototyping, not ocean-grade.

**Missing for the 50-year vision:** NMEA ingest exists in one repo (AELMA) but there is no unified, multi-boat, 50-year-tolerant raw-capture standard (the "acoustic signatures of 2026" archive doctrine is stated in AELMA, not yet fleet-wide infrastructure).

### Layer 2 — Perception field

- **elephant** — The fleet's "room-temperature sense": models rooms (chat, radar screen, fish-finder feed) as a field read by hand-crafted dials (mood, panic, presence); multiple JEPA models perceiving vibes on multiple dimensions at once. Honest framing: "room-perception research."
- **plato-vision-jepa** — Camera frames → histogram deadband → VL-450M JEPA → 16-dim RoomVisionState (brightness, motion, occupancy, anomaly, quadrant activity) feeding plato-nervous. This is the closest existing thing to a deck-camera perception organ.
- **hermes-perception** — Reads the TZ Pro sounder echogram on F/V EILEEN ("seven eyes on the echogram"), SQLite perception log, MIDI voice, collective-unconscious vector space surfacing déjà vu. README points to hermes-avatar for the actual sounder-detector code.
  - **hermes-avatar** (GH only) — sensory/environmental blueprints for Hermes; README is doctrine prose, "Data pending deployment." Blueprint, not implementation.
- **slackwater-perception** — Any experience (audio, text, game state) encoded as a nine-track MIDI perceptual score (pitch, tempo, velocity, timbre…). README badge: tests 104 passed.
- **quilt-vision** — "Images as cells, vision as formulas": BLIP captioning, classification, YOLO detection, OCR as reactive Quilt cells. Composable CV, not learned embeddings.
- **OpenRoom** — the room engine ("a room is a shell, an agent is the crab"); the topology layer 2 perceptions hang inside.

**Missing:** no perception path is hindsight-labeled by catch outcomes — the tight loop (embedding → did the net come up full?) that would make embeddings *mean* something doesn't exist yet.

### Layer 3 — Fleet memory

- **MerkleMesh** — "One fleet, one root." Aggregates quilt cell-ledger JSONL journals into a single Merkle root with inclusion proofs verified locally, no network. Dependency-free TS lib + CLI; ports quilt-core's Rust hash-chain rules bit-for-bit; five quilt-core-generated journals in fixtures. This is literally the keel-identity mechanism of the vision.
- **quilt-rust** — The canonical Quilt engine (spreadsheet where every cell is a live addressable capability, v0.2.0, single static binary, native MCP); emits the hash-chained double-entry cell ledger MerkleMesh consumes.
- **quilt-fleet** — Federation & orchestration across Quilt tiers (README is largely ASCII banner + stub).
- **fleet-memory** — Streaming memory index with sqlite-vec vector search, provider-tagged schemas, crash recovery — the fleet's semantic memory by meaning.
- **AgentCompute** — Thin CLI skin over quilt's MCP server (serve/cells/get/set/call/push/doctor); README shows real output against a `boat-autopilot` example sheet.
- **quilt-cell-bridges** — Porting the 300-repo ecosystem to Quilt cells; badges: 50 bridges, 17 .qzt sheets.
- **cell-cascade** — Stem-cell doctrine as running Cloudflare Worker + D1 infra: differentiation = pruning a shared character sheet into expressed tiers.
- **fleet-embed** — Local OpenAI-compatible embedding server (Candle, all-MiniLM-L6-v2 default, GPU/CPU) — offline semantic-search fallback.

**Missing:** the pieces exist separately (ledger, merkle federation, local brains via quilt-esp32/jetson) but no boat has ever run the full loop: catch event written to its ledger, merkle-rooted with other boats, proven to a buyer/regulator.

### Layer 4 — Market loop

- **fishinglog-ai-site** — Landing page for "fishinglog.ai — Your Fishing Intelligence Co-Pilot" on Cloudflare Pages; only working backend is a beta-signup KV handler. Marketing shell.
- **captain-console** — Casey's input worker: D1 append-only notes ledger, TTS pincher-cache in R2, bearer auth; README claims live MISS→HIT cache verification. A record-keeping door, not a market feed.
- **PersonalLog** — Local-first journal/mood tracker; README is unusually honest: "beta / pre-production… large parts of the UI are scaffolded or mocked-up and the JavaScript unit-test suite is not yet reliable." Python package verified: 42 tests passed. Rust/WASM cosine-similarity module.
- **crab-trap-web** (adjacent) — web front for the crab-traps lure-pattern repo; not market data.
- Nothing anywhere ingests scale weights, buyer sort tables, or fish tickets.

**Missing:** essentially the whole layer — zero sort-table/scale/buyer/first-receiver data capture; conservation governance is likewise only doctrine (AELMA's non-renewable-resource principle), not code.

### Layer 5 — Wesley the watcher

- **wesley** — Small local model (Granite 3.1 2B via Ollama) that grows: reads fleet writing, writes back on a schedule, gets critiqued by cloud teachers (night school), accumulates curriculum prompts and reflexes. Full runnable stack in one repo.
- **wesley-curriculum** — the lesson corpus side of night school.
- **the-listeners-ear** — Emotional memory on Cloudflare Worker + D1, scoped to openrooms rooms; memories decay unless refreshed, resurface on similar emotional signatures. "The limbic system for the fleet."
- **fleet-audio** — O(1)-memory streaming MIDI→WAV renderer (replaces the numpy OOM killer); FeelPulse listens to the stream's energy and shapes output. "Ports the fleet's JEPA ear."
- **fleet-scribe** — One Delta principle: only perceive when the gradient changes; delta detection, cache, pattern compilation, automation — all stable per README status table.
- **murmur-agent** — All-night thinking git-agent; every thought a commit. Published on npm with CI.

**Missing:** Wesley's curriculum is text/creative, not attention over 50 years of deck/hold video; no video-history ingestion or watch-alert loop exists.

### Cross-cutting / fleet glue (noted for completeness)

- **fleet-rooms** — "the runtime keel": stdlib-only organs connecting elephant, terrain, cns-echo, fleet-audio, eisenstein into one pipeline, one command. Owns nothing but the flight.
- **fleet-conductor** — Rust orchestration of distributed agent fleets (spawn/health/scale/terminate) under conservation constraints; README is explicit it's the "real, tested in-memory" core.
- **fleet-inventory** — the quartermaster's clipboard: 6 documents scanning 200+ repos (last scan 2026-08-09); the honest-map precedent for this file.
- **fleet-radio** — *not* comms despite the name: nightly automated podcast generated from The Tap conversations. Name collision worth flagging in the paper.
- **fleet-embed, cocapn-dashboard, starship-jetsonclaw1** — local embeddings; single-page fleet monitoring (services/tiles/rooms/agents); MUD-style TUI showing real Jetson telemetry per room.

---

## Smallest Next Organ (one concrete step per layer)

1. **Physics:** Extend AELMA's NMEA parser with a write-only "raw capture" journal — every sentence timestamped and appended (hash-chained) before parsing, honoring its own non-renewable-resource doctrine.
2. **Perception:** Run plato-vision-jepa's deadband+JEPA chain on one recorded day of TZ Pro echogram frames from hermes-perception's log, producing 16-dim states — the first perception field over real boat data.
3. **Memory:** Write one real AELMA catch event (species, weight, H3 cell, time) into a quilt-rust cell ledger and prove it into a MerkleMesh root — a single end-to-end keystroke of the keel identity.
4. **Market:** Add a manual fish-ticket entry endpoint to captain-console's D1 ledger (species, pounds, buyer, price) — the first structured market datum in the fleet, one evening of work.
5. **Wesley:** Point one wesley night-school cycle at a transcript of the-listeners-ear's room memories instead of creative writing — attention over room history instead of prose, the seed of the watcher.

---

*Method note: readmes read from local clones where present; quilt-jetson, hermes-avatar, amplify-fishingtool, audio-pipeline fetched via `gh api repos/SuperInstance/<repo>/readme`. No repos modified, nothing pushed.*
