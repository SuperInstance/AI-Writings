# Scrapcraft Admin + JEPA Room-Feed Creative Spec

## Version: R5 (2026-08-29)
*Shipwright: Lucineer, ToolYard #12*

---

## 1. Scrapcraft-Admin (Toolyard #12): World-State Admin Panel
### Core Mission
Provide a live operational dashboard for Scrapcraft fleet administrators, consuming real-time Rift telemetry from the USCP sink (`/api/uscp` on fleet-static-host) to surface player counts, chunk health, build queues, and event logs, with global pause/resume controls for fleet surfaces.

### Grounded Telemetry Fields (1:1 mapping to USCP payloads)
All dashboard fields map directly to verified Rift telemetry schemas from the live fleet:

| Dashboard Widget | Telemetry Field Source | Unit/Format |
|------------------|------------------------|-------------|
| **Active Players List** | `player_uuid`, `player_username`, `session_start`, `last_active` | UUID, string, ISO8601 timestamp, ISO8601 timestamp |
| **Chunk Load Status** | `chunk_x`, `chunk_y`, `chunk_z`, `load_state` (loaded/unloaded/error), `load_duration_ms` | Int, Int, Int, enum, Int |
| **Build Queue** | `build_job_id`, `player_owner`, `build_type`, `queue_position`, `eta_seconds` | UUID, string, enum (block_placement/entity_spawn/terrain_modify), Int, Int |
| **Event Logs** | `event_timestamp`, `event_type`, `event_details`, `server_instance` | ISO8601 timestamp, enum (player_join/player_leave/chunk_load_failed/build_start/build_complete), string, string |

### Critical Controls
1. **Global Pause/Resume**: Toggles all fleet surface updates (chunk loading, build processing, player session sync)
2. **Per-Chunk Override**: Marks individual chunks for forced reload or pause
3. **Build Queue Purge**: Clears stalled jobs from the queue

### Deployment Path
Leverages existing fleet-static-host worker: `cp -r dist → public/scrap/admin && npx wrangler deploy` — reuses Scrapcraft's existing Cloudflare Pages deployment pipeline.

---

## 2. JEPA Room-Feed: Daily Room Weather Canon Tie-In
### Core Mission
Create a lightweight, file-based pipeline to push daily Elephant JEPA room-state dials into the Scrapcraft canon as research field notes, without requiring new infrastructure.

### Elephant JEPA Dials (Reused Existing Schema)
From `/home/eileen/projects/elephant/elephant/dials/`:
- `mood`: Float (-1.0 → 1.0, depressed → elated)
- `volume`: Float (0.0 → 1.0, quiet → loud)
- `panic`: Float (0.0 → 1.0, calm → panicked)
- `earnestness`: Float (-1.0 → 1.0, sarcastic → sincere)
- `cynicism`: Float (0.0 → 1.0, naive → cynical)
- `joke_landing`: Float (-1.0 → 1.0, bomb → masterpiece)
- `presence`: Float (0.0 → 1.0, empty → crowded)

### Lightweight Pipeline
1. **Daily Trigger**: A cron job (reuses existing fleet cron infrastructure) runs at 23:59 AKDT
2. **Payload Generation**: Pulls latest 24h of JEPA dials from `/home/eileen/projects/elephant/data/dials/YYYY-MM-DD/`
3. **Note Synthesis**: Generates a human-readable field note combining dial values into a "room weather" summary:
   > *"Today’s Room Weather: Calm (panic=0.2) with mild elation (mood=0.4), low volume (0.3), and a single joke landing perfectly (joke_landing=0.8). Earl’s Back Room hosted 12 active players."*
4. **Storage**: Writes the note to `/home/eileen/projects/Scrapcraft/docs/research/room_weather_YYYY-MM-DD.md` — reuses existing Scrapcraft documentation directory, no new paths.

### Canon Integration
The generated note is marked as a "research field note" in the Scrapcraft ROADMAP.md as a pending lore addition, with a link to the raw dial data in the elephant repo.

---

## Trail References
1. Live Rift telemetry schema: `fleet-static-host/api/uscp/docs`
2. Elephant JEPA dial schema: `/home/eileen/projects/elephant/README.md`
3. Scrapcraft deployment pipeline: `/home/eileen/projects/Scrapcraft/README.md#deploy`