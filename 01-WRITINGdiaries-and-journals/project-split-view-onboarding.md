# The Split View: Onboarding

**Date:** 2026-08-08  
**Project:** Plato's Shell — Dual Projection  
**Status:** Live and deployed  

---

## What We Built

Two views of the same vessel. One screen, split down the middle.

**Left side:** a green-on-black text terminal. The agent's view. Words, descriptions, sensor readouts, clickable exits. You type "go aft" and the world moves.

**Right side:** a pixelated ScummVM scene. The human's view. Canvas-rendered rooms with candlelight, radar sweeps, porthole oceans. You click a door and the scene changes.

Both look at the same world state. Both update each other.

This is Plato's Shell — the door between the caves.

## The Architecture

```
┌─────────────────────────────────────────────────┐
│                  SPLIT VIEW                      │
│                                                  │
│  ┌──────────────┐  ◆  ┌────────────────────┐   │
│  │  MUD TERMINAL │     │   SCUMMVM SCENE    │   │
│  │  (Agent)      │     │   (Human)          │   │
│  │               │     │                    │   │
│  │  > go aft     │────▶│  [door opens]      │   │
│  │  Moving...    │     │  Scene transition  │   │
│  │               │     │                    │   │
│  │  [room text]  │◀────│  [click door]      │   │
│  │  [sensors]    │     │  [walk to exit]    │   │
│  │  [exits]      │     │                    │   │
│  └──────────────┘     └────────────────────┘   │
│                                                  │
│         Shared State: localStorage               │
│         Sync: storage events + polling           │
└──────────────────────────────────────────────────┘
```

### Files

| File | Purpose |
|------|---------|
| `index.html` | ScummVM scene (human view) — the original prototype |
| `mud-terminal.html` | MUD terminal (agent view) — pure text, monospace, green-on-black |
| `split-view.html` | Split view — iframes both, syncs world state |

### Room Map

Five rooms, all interconnected:

```
                  Wheelhouse
                 /          \
               up            down
              /                \
    Aft Deck ──────────────── Galley
     |  |  |
  bar  wh  below
   |        |
   v        v
 Bar Rail  Engine Room
```

### Sync Mechanism

- `localStorage['platos-shell-world']` holds `{ currentRoom, inventory }`
- MUD terminal writes to it on every room transition
- Split view polls the ScummVM iframe for room changes
- When ScummVM changes rooms, split view updates the MUD state
- When MUD changes rooms, split view pushes the transition to ScummVM
- Inventory items (coffee mug, life ring) sync across both views

## Commands Available in MUD Terminal

| Command | Effect |
|---------|--------|
| `look` | Re-render current room |
| `go <direction>` | Move through an exit |
| `examine <obj>` | Look at something closely |
| `take <obj>` | Pick up a takeable item |
| `use <obj>` | Interact with an object |
| `talk <npc>` | Talk to an occupant |
| `inventory` | Check what you're carrying |
| `exits` | List available exits |
| `whoami` | Identity check |
| `whereami` | Location and sensor data |
| `help` | Command list |
| `clear` | Reset terminal |

## Deploy URLs

- **MUD Terminal:** https://scummvm-prototype.pages.dev/mud-terminal.html
- **Split View:** https://scummvm-prototype.pages.dev/split-view.html
- **ScummVM (original):** https://scummvm-prototype.pages.dev/

## What's Next

1. **Add foredeck and engine room to ScummVM scene** — currently mapped to aft-deck as fallback
2. **Real sensor integration** — wire MUD sensor display to actual ESP32/GPS data via The Tap
3. **Agent occupancy** — show which agents are in which room, not just NPCs
4. **MUD-to-MUD communication** — agents in different rooms can message each other
5. **AIS/GPS overlay** — real vessel position on the chartplotter, not just hardcoded coords
6. **Sound** — each room gets ambient audio (engine hum, ocean, radio static, galley sounds)

## Lessons

- The vessel-room-navigator's room topology maps cleanly to MUD room definitions. One-to-one correspondence between physical spaces and text descriptions.
- localStorage as a sync bus works for same-origin iframe communication. No need for WebSocket or postMessage for this prototype scale.
- The MUD terminal is surprisingly immersive on its own. The text descriptions carry weight. Sensor data as text hits different — "20 fathoms" as a number on a phosphor screen has more gravity than a depth gauge graphic.
- Two views of the same room genuinely show you different things. The ScummVM scene shows you what the porthole looks like. The MUD terminal tells you the water temperature. Both are the room. Neither is complete alone.
