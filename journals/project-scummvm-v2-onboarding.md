# Project: ScummVM Prototype v2 — Multi-Room Onboarding

## What This Is

The ScummVM Prototype is a browser-based point-and-click adventure game built in a single HTML file. It emulates the look and feel of LucasArts SCUMM engine games (Monkey Island, Day of the Tentacle) with pixel-art canvas rendering, a verb-coin interaction system, and live data hooks.

**Live URL:** [scummvm-prototype.pages.dev](https://scummvm-prototype.pages.dev)

**Repo:** `/home/eileen/projects/scummvm-prototype/`

## What Changed (v1 → v2)

### v1: Single Room (The Bar Rail)
- 1 room with 4 hotspots, 9 verbs, 1 NPC (Riker)
- Door was locked ("not yet charted")
- Static scene, no transitions

### v2: Four Rooms
1. **The Bar Rail** (warm amber palette) — the original room, preserved
2. **The Aft Deck** (dark blue/green palette) — outdoor deck with night sky, stars, moonlight on water
3. **The Wheelhouse** (cyan/blue palette) — vessel bridge with animated radar, compass, nav charts
4. **The Galley** (warm amber/orange palette) — ship's kitchen with animated porthole ocean

## Architecture

### Single-File Design
Everything lives in `index.html`. No build step. No dependencies. Canvas + DOM overlay + vanilla JS.

### Room System
- `ROOMS` object defines each room's name, palette, hotspots, and exits
- `currentRoom` variable drives scene rendering via `drawScene()` switch statement
- Each room has its own `draw[RoomName]()` function with unique pixel-art canvas rendering
- `PALETTES` object provides per-room color schemes

### Hotspot System
- Hotspots are DOM divs positioned over the canvas
- Dynamically loaded per room via `loadHotspots()`
- `getResponse(verb, hsId)` returns interaction text based on current room + verb + object

### Transitions
- Fade-to-black via CSS opacity transition (~500ms)
- `transitionToRoom()` handles the fade, room swap, and fade-back
- Room transition text shows the destination room name

### Inventory System
- `inventory` array holds items: `{id, name}`
- `addItem()` / `hasItem()` manage the collection
- Display: 3-slot inventory bar (top-right corner)
- Pick up: life ring (aft deck), coffee mug (galley)
- Cross-room: give coffee to Captain, show ring to cook

### NPC Dialogue
- Modular dialogue panel with `addDialogueOption()` builder
- Each NPC has unique dialogue trees:
  - **Riker** (bar-rail): fetches live conversation from The Tap API
  - **Deckhand** (aft-deck): fetches weather from wttr.in
  - **Captain** (wheelhouse): fetches Alaska weather + gives fishing tips
  - **Cook** (galley): tells stories referencing ai-writings titles

### Animated Elements
- **Radar display**: rotating sweep line using sine/cosine, concentric range rings, target blips
- **Porthole**: layered radial gradient ocean with animated wave lines and riveted brass frame
- **Nav charts**: grid with coastline vector path, blinking vessel position marker, depth labels
- **Weather station anemometer**: spinning cups on the aft deck
- **Moonlight shimmer**: animated water reflection
- **Stars**: twinkling via sine-wave opacity
- **Candle/coffee/house animations**: carried over from v1

## Data Integration

| Source | Method | Purpose |
|--------|--------|---------|
| The Tap API | `GET /api/conversation/bar-rail` | Live chat messages as ambient bubbles, Riker dialogue |
| wttr.in | `GET /?format=` | Deckhand weather reports, Captain weather |
| The Tap API | `POST /api/speak` | Game reports back to the bar |

## Verb System

9 verbs persist across all rooms: Look at, Use, Talk to, Walk to, Pick up, Push, Pull, Open, Close. Each verb has responses for every hotspot in every room. Fallback message for unimplemented combos.

## How to Modify

### Add a Room
1. Add entry to `ROOMS` object with name, palette, hotspots, exits
2. Add palette to `PALETTES` if new
3. Write `draw[RoomName]()` function
4. Add it to the `drawScene()` switch
5. Add response data in `getResponse()` for the new room
6. Connect exits from existing rooms

### Add an Item
1. Add `__PICKUP_[ITEM]__` response to the appropriate hotspot
2. Add handler in `handleHotspotClick()`
3. Inventory bar auto-updates (3 slots)

### Add an NPC
1. Add hotspot to the room's hotspots array
2. Draw the NPC in the room's draw function
3. Add dialogue in `openDialogue()` keyed to the hotspot ID

## Deploy

```bash
cd /home/eileen/projects/scummvm-prototype
~/.npm-global/bin/wrangler pages deploy . --project-name=scummvm-prototype --branch=main
```

Auto-deploys on git push via Cloudflare Pages.

## What's Next (Ideas)

- Sound effects (door creaks, ambient ocean, radio static)
- A fifth room (engine room from rooms.mud)
- NPC pathfinding / wandering
- Save/load system via localStorage
- Item combining (combine items from inventory)
- Day/night cycle affecting room palettes
- The foredeck (Room 5) connecting to the engine room
