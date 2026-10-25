# Project: SCUMM Asset Pipeline — Onboarding

## What This Is

We're building a retro point-and-click adventure GUI for the agentic world. Think 1990s LucasArts — Monkey Island, Day of the Tentacle, Sam & Max — but the rooms are The Tap (a tavern that agents hang out in) and a fishing vessel in Alaska.

The aesthetic is **charming and iconic, not cutting-edge.** Pixel art backgrounds. Clickable hotspots. NPCs that idle-breathe and talk in text. Ambient audio that makes each room feel like a place.

## Where Things Live

| Thing | Location |
|-------|----------|
| Full asset spec | `/home/eileen/projects/scummvm-gui-design/ASSET-SPEC.md` |
| Creative piece | `/home/eileen/projects/scummvm-gui-design/THE-FIRST-WALL.md` |
| Test asset | `/home/eileen/projects/scummvm-gui-design/assets/bar-rail-test.jpg` |
| MUD room definitions | `/home/eileen/projects/terrain/rooms.mud` |
| SCUMM parser (Rust) | `/home/eileen/projects/mud2scummvm/src/lib.rs` |
| Terrain renderer | `/home/eileen/projects/terrain/` |
| DeepInfra env | `/home/eileen/mcp-deeinfra/.env` |

## The Pipeline (How Art Gets Made)

1. **Write the prompt** using templates from ASSET-SPEC.md §3
2. **Generate with DeepInfra FLUX-1-schnell** — costs ~$0.003 per image
3. **Post-process** — pixelate down to 320×200, quantize to 256 colors
4. **Define walkboxes** — polygon overlays for walkable areas (JSON)
5. **Define hotspots** — bounding boxes with SCUMM verbs (JSON)
6. **Add NPC sprites** — 32×64 px animated sprite sheets
7. **Add ambient audio** — looping OGG files from MMX or freesound.org
8. **Register in rooms.json** — master room registry ties it all together

## The Rooms (11 Total)

### The Tap (6 rooms)
- **bar-rail** — Main bar area, amber lighting, Riker tends bar
- **engine-room** — Industrial backend metaphor, furnace and pipes
- **aft-deck** — Open weather deck, crab pots, grey Alaska sky
- **corner-booth** — Secluded booth for private conversations
- **bridge-table** — Raised planning area with nautical charts
- **chart-room** — Small reference room with terminal and map drawers

### Fishing Vessel (5 rooms)
- **wheelhouse** — Ship's bridge, helm wheel, radar, captain
- **galley** — Compact kitchen, propane stove, coffee maker
- **foredeck** — Working bow, anchor windlass, deckhand
- **engine_room** — Twin diesels, engineer bot
- **aft_cockpit** — Stern deck, catch boxes, cargo robot

## Key Decisions

- **DeepInfra FLUX-1-schnell** is the image model. 4 steps, 1024×576, ~3 cents for the whole project.
- **320×200 native resolution** rendered at 3× scale (1024×576) for modern displays.
- **256-color indexed palette** applied via PIL quantization in post-processing.
- **Hotspots use SCUMM verbs**: Look, Talk, Use, Walk, (Sit, Turn, Open for specific objects).
- **Walkboxes are polygons** in native coordinate space with scale zones for depth.
- **NPC sprites are 32×64 px** with idle/talk/walk animation cycles.
- **MMX quota is at 0%** — use DeepInfra for images, freesound.org for audio.

## What's Done

- [x] Full asset spec written (ASSET-SPEC.md)
- [x] Test background generated (bar-rail-test.jpg via FLUX-1-schnell)
- [x] Prompt templates for all 9 rooms + 5 NPCs
- [x] Walkbox JSON schema designed
- [x] Hotspot JSON schema designed
- [x] Exit zone schema designed
- [x] Room registry structure defined
- [x] Cost analysis (~$0.05 for all assets)
- [x] Creative piece written (THE-FIRST-WALL.md)
- [x] Announced at The Tap

## What's Next

- [ ] Generate all 11 background images
- [ ] Pixelate + quantize each to 320×200 / 256 colors
- [ ] Create walkbox polygons for each room
- [ ] Define hotspot bounding boxes from the room specs
- [ ] Generate NPC sprite sheets
- [ ] Source/generate ambient audio loops
- [ ] Build the rooms.json master registry
- [ ] Integrate with mud2scummvm Rust parser
- [ ] Wire up the verb coin / verb list UI
- [ ] Player character pathfinding on walkboxes

## How to Generate a Background

```bash
source /home/eileen/mcp-deeinfra/.env

curl -s "https://api.deepinfra.com/v1/openai/images/generations" \
  -H "Authorization: Bearer $DEEPINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "black-forest-labs/FLUX-1-schnell",
    "prompt": "Pixel art background, [ROOM DESCRIPTION], [LIGHTING], adventure game background, 1990s LucasArts SCUMM style, 320x200 resolution aesthetic, 256 color palette, no characters, no text, no UI elements",
    "n": 1,
    "size": "1024x576",
    "steps": 4
  }' | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
img = base64.b64decode(data['data'][0]['b64_json'])
open('output.jpg', 'wb').write(img)
print('Done:', len(img), 'bytes')
"
```

Then pixelate:
```python
from PIL import Image
img = Image.open('output.jpg')
img = img.resize((320, 200), Image.Resampling.LANCZOS)
img = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
img.save('output.png', 'PNG')
```

## Design Principles

1. **Charm over fidelity.** A crude image with atmosphere beats a polished image without soul.
2. **Consistent palette.** All rooms share a 256-color master palette for visual cohesion.
3. **Every object is a potential hotspot.** If you can see it, you should probably be able to click it.
4. **Audio is 50% of the atmosphere.** A room without ambient audio feels dead.
5. **The text comes first.** The MUD descriptions drive the art direction, not the other way around.

---

*Onboarded by Lucineer — 2026-08-08*
*The Tap is open. The pipeline works. Let's build.*
