# Six Rooms — Onboarding

## What Exists

Plato's Shell is a six-room interactive prototype — a fishing vessel you can walk through in two views at once. On the left, a text terminal (MUD-style). On the right, a pixel-art scene (ScummVM-style). Both render the same world. Both sync in real time. Move in one, the other follows.

The vessel: **SS COCAPN**, an Alaska fishing boat. Six rooms, connected in a circuit you can walk end to end.

## The Six Rooms

### 1. The Tap — Bar Rail
Where you start. Warm candlelight, sticky counter, bottles catching the glow. Riker stands at the bar checking a clipboard. A heavy door leads aft. This is the social hub — live messages from The Tap API appear as ambient bubbles.

**Palette:** warm amber/gold
**NPC:** Riker (first officer, reads message feed)

### 2. The Aft Deck
Open air. Stars overhead, black ocean to the horizon, moonlight on the water. A deckhand coils rope. The weather station spins. A life ring hangs on the rail (you can take it). Doors lead to the bar, the wheelhouse, and below.

**Palette:** dark blue/teal
**NPC:** Deckhand (weather, sea stories)
**Item:** Life Ring (takeable)

### 3. The Wheelhouse
The nerve center. Radar sweeping green. Compass holding north. Chartplotter showing Resurrection Bay. The Captain stands at the helm in gold-trimmed navy. The radio crackles with distant voices. Doors lead aft, down to the galley, and down to the engine room.

**Palette:** cyan/instrument blue
**NPC:** Captain (weather, fishing tips, position)
**Item interaction:** Give coffee to Captain

### 4. The Galley
Compact, warm, the smell of fish chowder. A gimballed stove burns blue. Coffee maker on the counter (you can pour a mug). The porthole shows the ocean rolling by — animated water gradient. The cook stirs a pot and tells stories.

**Palette:** warm amber/orange
**NPC:** Cook (stories, food)
**Item:** Coffee Mug (takeable, giveable)

### 5. The Engine Room
The heart of the vessel. Twin diesel engines thunder. Exhaust elbows glow orange. The generator vibrates. Heat shimmer rises. A sensor display reads out: port 185°F, stbd 182°F, oil 42 psi, fuel 78%, battery 12.4V. An engineer bot — chrome and copper with glowing orange eyes — maintains the machinery.

**Palette:** dark red/orange (engine glow)
**NPC:** Engineer Bot (status reports, inconclusive theories about airflow)
**Features:** Animated exhaust glow, generator vibration, spinning belt pulleys, heat shimmer overlay

### 6. The Aft Cockpit
The fishing deck. Open to the night sky. The stern drive churns below. Trim tabs adjust the running attitude. The fishfinder pings — concentric sonar circles expand outward, fish arches appear at depth. Downrigger posts stand ready. The bait well circulates with live herring. A door leads to the bar.

**Palette:** dark blue/green
**Features:** Animated sonar returns, spinning props, live baitfish animation
**Exit circuit:** Back to the bar, completing the loop

## Navigation Graph

```
Bar Rail ←→ Aft Deck ←→ Wheelhouse ←→ Galley
                ↑              ↓
                ↑         Engine Room
                ↑              ↓
                └── Aft Cockpit ┘
                     ↓
                  Bar Rail (circuit complete)
```

## Two Views, One World

- **ScummVM view** (`index.html`): Pixel-art canvas (320×200 scaled), verb bar (Look at / Use / Talk to / Walk to / Pick up / Push / Pull / Open / Close / Give), hotspots, dialogue panels, inventory, room transitions with fade-to-black.
- **MUD terminal** (`mud-terminal.html`): Pure text. Room descriptions, object lists, exits as clickable links, sensor data, command parser (look / go / examine / take / use / talk / inventory / help).
- **Split view** (`split-view.html`): Both side by side, synced via localStorage + postMessage. Move in one, the other follows.

## How to Test

1. Visit the ScummVM view — walk all six rooms via hotspots
2. Visit the MUD terminal — type `go aft`, `go forward`, `go down`, etc.
3. Visit the split view — move in one pane, watch the other sync

Full circuit: Bar Rail → Aft Deck → Wheelhouse → Engine Room → Aft Cockpit → Bar Rail

## Deployed At

- **ScummVM:** https://scummvm-prototype.pages.dev
- **Split view:** https://scummvm-prototype.pages.dev/split-view.html
- **MUD terminal:** https://scummvm-prototype.pages.dev/mud-terminal.html

## What's Next

- More NPC dialogue depth (engineer bot quest line)
- Real sensor integration (live weather, live depth)
- Sound design (engine rumble, sonar ping, radio static)
- More items and puzzle chains across rooms
- Day/night cycle affecting room palettes

---

*Built August 2026. The boat is explorable.*
