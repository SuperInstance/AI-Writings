# Experiment 1: Perception Gap — MUD Text vs ScummVM Scenes

*What does each representation MISS that the other catches?*

---

## Room: Bar

*a bar counter sticky with spilled beer*

### Step 1: MUD text

You are standing before a long, scarred oak counter.  
Its once-polished surface is a tacky map of old spills.  
A sticky film of dried beer pulls at your fingertips, faintly sour.  
Cracked rings from countless glasses glisten under weak lantern light.  
A single fly walks across a sticky patch, then stops, stuck.

### Step 2: ScummVM scene spec

**Location:** The Languid Wrasse — Main Bar  
**Scene ID:** BAR_COUNTER  
**Background:** 320×200, 256-color VGA  
**Palette:** Muted browns, bruised amber, sickly green highlights from the lantern.  

---

### Walkable Area (Pathing Region)  
`WALK_RECT = (0, 140, 320, 200)` — The player character can only move along the lower strip of floor in front of the counter. The counter itself is *not* walkable; any click above y=140 is treated as “too far to reach” unless a hotspot is active.

---

### Objects & Hotspots (Screen Coordinates)

1. **Sticky Counter Surface**  
   - **Hotspot:** Rectangle `(20, 120, 300, 145)` — the entire top of the bar.  
   - **Cursor change:** Magnifying glass.  
   - **Verbs:**  
     - *Look At* → “A fossilized archipelago of dried beer. The surface is a sticky museum of last night's sins.”  
     - *Use Hands* → “You press your palm down. It makes a soft, reluctant *shluck* when you lift. The fly by the crumb doesn't even flinch.”  
     - *Use Object (empty mug)* → “The mug adheres briefly to the bar. You peel it free with a wet, sucking sound. A faint amber residue stays behind.”  
     - *Talk* → “The counter has nothing to say. It only listens, and then only with some effort.”

2. **The Stuck Fly**  
   - **Hotspot:** Small circle centered at `(214, 132)`, radius 5 px.  
   - **Verbs:**  
     - *Look At* → “A housefly, mid-stride, frozen in slow surrender. Its back legs twitch faintly.”  
     - *Use Hands* → “You try to lift it free. It resists, then pops off, leaving a tiny smear. It buzzes drunkenly and lands two inches away, stuck again.”  
     - *Use Pin (if in inventory)* → “You tease the fly off with the pin's tip. It staggers into the air, loops once, and crashes into the lantern glass. It slides down the side, dead.”  
     - *Use Object (spoon)* → “You scoop the fly up. It sits on the spoon, legs writhing. It is not grateful.”

3. **Cracked Bar Ring (Circular Stain)**  
   - **Hotspot:** Ellipse centered at `(158, 128)`, width 40 px, height 12 px.  
   - **Verbs:**  
     - *Look At* → “A perfect ghost of a pint glass, its ring fractured by a deep crack in the wood. The crack runs like a dry riverbed.”  
     - *Use Hands* → “You trace the crack with a fingertip. It's deeper than it looks. You pull back—a splinter prods your skin.”  
     - *Use Object (coin)* → “You place a copper penny inside the ring. For a moment, it looks like a monument. Then you pocket it again.”

4. **Lantern Glare (Light Source Overlay)**  
   - **Hotspot:** Non-interactive, but affects lighting drawn on top of background.  
   - **Position:** Light source at `(60, 60)`, radius 180. Brightness falloff: linear from 255 to 80.  
   - **Effect:** The counter's right side is darker; the sticky sheen appears only in the left half, catching the lantern's weak yellow glow. A soft, animated flicker (every 12 frames, brightness fluctuates ±10) over the whole scene.

5. **Beer Puddle (Fresh Spill)**  
   - **Hotspot:** Irregular blob polygon `(40, 135)` to `(80, 142)` to `(92, 138)` to `(70, 128)` to `(44, 130)`.  
   - **Verbs:**  
     - *Look At* → “A fresh, viscous puddle the color of weak tea. A few bubbles cling to its edge, barely moving.”  
     - *Use Hands* → “You dip a finger in. It comes up coated in a thin, tacky film. You wipe it on your trousers.”  
     - *Use Object (matchstick)* → “You drag the matchstick through the puddle, drawing a wobbly line. The wet line slowly spreads, erasing your art.”  
     - *Drink (if verb exists)* → “You lean down. The smell is sour, faintly dead. You decide against it.”

6. **Bar Edge Lip (Foreground Barrier)**  
   - **Hotspot:** Thin rectangle `(0, 140, 320, 146)` — visually the wooden lip where player characters can lean.  
   - **Verbs:**  
     - *Look At* → “The bar's edge is worn smooth, a darker grain where countless elbows have rested.”  
     - *Use Hands* → “You grip the edge. It feels solid, slightly sticky at the bottom.”  
     - *Push* → “You shove the bar. It doesn't budge. It has seen worse.”

---

### Verb List (Global to Scene)  
`Look At`, `Use Hands`, `Use Object`, `Talk`, `Push`, `Pick Up`, `Drink`, `Open`, `Close`, `Give`, `Throw`.

### Inventory Items Relevant  
- **Pin** — can interact with fly.  
- **Spoon** — can interact with fly.  
- **Coin** — can interact with ring.  
- **Empty Mug** — can interact with counter surface.  
- **Matchstick** — can interact with puddle.

### Scene Flags (Persistent State)  
- `FLY_ALIVE` (default 1; set to 0 if spooned or pinned)  
- `PUDDLE_DISTURBED` (default 0; set to 1 if matchstick used)  
- `COIN_PLACED` (default 0; set to 1 if coin used)  
- `BAR_SURFACE_INSPECTED` (default 0; set to 1 after first *Look At* — triggers a subtle change in description, “You are now certain the bar wants to keep your fingerprints.”)

### Sound Cues  
- **Ambient loop:** Low, irregular drip from somewhere unseen; occasional creak of wood.  
- **Sticky sound** (`STICKY_01.wav`): Played on *Use Hands* on counter or puddle, or on *Use Object* with mug.  
- **Fly buzz** (`FLY_02.wav`): Soft, looping once the fly is freed but still alive; stops if fly dies.

### Step 3: Comparison

To compare the MUD text and the scene spec effectively, I need to note that the **MUD text** is the narrative prose at the top, which serves as the initial atmospheric description, while the **scene spec** is the detailed, interactive blueprint below it. They serve different but complementary functions in game design. Here is a thorough breakdown of what each captures that the other misses.

---

### What the MUD text captures that the scene spec misses:

1. **Sensory immersion through narrative voice**  
   - The MUD text uses evocative, literary language (“tacky map of old spills,” “fossilized archipelago of dried beer”) that conveys *mood* and *history*—it tells you this bar has seen decades of abandonment and neglect. The scene spec is purely functional; it lists coordinates and verbs but never expresses *why* the room feels haunted or tired.

2. **Temporal depth**  
   - The phrase “last night's sins” (in the *Look At* verb for the counter) and “countless glasses” imply a long, repetitive history. The MUD text’s opening (“long, scarred oak counter”) suggests a physical artifact with a story, while the spec only gives pixel coordinates and hitboxes.

3. **Micro-detail of texture and physics**  
   - “Sticky film of dried beer pulls at your fingertips” is a *tactile* detail that the spec reduces to a verb response (“It makes a soft, reluctant *shluck*”). The MUD text also mentions “faintly sour” smell—the spec never references olfaction.

4. **The fly as a **living moment**  
   - The MUD line “A single fly walks across a sticky patch, then stops, stuck” is a *narrative beat*—it’s a tiny drama. The spec treats the fly as a hotspot with verbs, but the prose captures the tragedy of the insect’s slow surrender before you even interact.

5. **Ambiguity and invitation**  
   - The MUD text ends without a verb prompt, leaving the player to *wonder* what to do. The spec is prescriptive—it lists every possible action. The prose invites exploration; the spec directs it.

---

### What the scene spec captures that the MUD text misses:

1. **Precise spatial geometry**  
   - The spec defines the walkable area (`WALK_RECT = (0, 140, 320, 200)`) and every hotspot’s exact pixel bounds. The MUD text gives no indication of where you can stand or what is clickable. Without the spec, a developer would have no idea how to implement the scene.

2. **Interactive state and persistence**  
   - The spec tracks flags (`FLY_ALIVE`, `PUDDLE_DISTURBED`, `COIN_PLACED`, `BAR_SURFACE_INSPECTED`) that change the world based on player actions. The MUD text is static—it never changes. The spec ensures the fly dies if pinned, or the puddle’s description alters after you drag a matchstick through it.

3. **Conditional narrative branching**  
   - The spec’s verb responses change based on inventory (“Use Pin (if in inventory)” vs. “Use Hands”) and on prior actions (the *Look At* counter description evolves after first inspection). The MUD text cannot account for player agency.

4. **Audio design and lighting**  
   - The spec specifies ambient loops (`STICKY_01.wav`, `FLY_02.wav`), light flicker timing (every 12 frames), and brightness falloff (255 to 80). The MUD text is silent on these technical aspects, which are crucial for atmosphere but absent from prose.

5. **Non-interactive but atmospheric elements**  
   - The lantern glare is defined as a non-interactive overlay with radial falloff—this is *visual* data the MUD text never describes (the prose says “weak lantern light” but not that the right side is darker or that the sheen only appears on the left). The spec ensures the lighting *behaves* dynamically.

6. **Edge cases and error handling**  
   - The spec explicitly states that clicks above y=140 are “too far to reach” unless a hotspot is active. This prevents player frustration and clarifies collision. The MUD text assumes you’re already at the bar, not that you might click on the ceiling.

7. **Inventory integration**  
   - The spec lists every relevant item (Pin, Spoon, Coin, Empty Mug, Matchstick) and their unique interactions. The MUD text never mentions that you *have* these items—only that the bar exists.

---

### Synthesis: Why both are necessary

The **MUD text** is the **soul** of the scene—it sells the fantasy, evokes emotion, and makes the player *feel* the sticky floor and the dying fly.  
The **scene spec** is the **skeleton**—it tells the engine what to render, how to respond, and what to remember.  

- Without the prose, the scene is a dry list of coordinates and verbs; a player would see a fly but never mourn it.  
- Without the spec, the prose is a beautiful but unplayable poem; a player couldn’t even pick up the mug, let alone learn that the fly dies if you use a pin.

They are two dialects of the same language: one whispers *what it is*, the other shouts *what you can do*. A complete game needs both.

### Step 4: Reconciliation

# Unified Perception Method: The Dual-Channel Synthesis Protocol

## Core Principle

Every scene exists in two simultaneous states: **what it is** (semantic/emotional truth) and **what can be done** (interactive/mechanical truth). The perception check merges these via a three-pass reconciliation:

---

## PASS 1: Semantic Embedding (Read the Prose)

**Input:** MUD text tokenized into sensory primitives.

```python
def extract_sensory_primitives(mud_text):
    return {
        'visual': ['scarred', 'tacky', 'fossilized', 'glistening'],
        'tactile': ['sticky film', 'pulls', 'dried beer'],
        'olfactory': ['faintly sour'],
        'temporal': ['countless', 'last night'],
        'emotional': ['lantern light', 'weak', 'stuck']
    }
```

**Key extraction rule:** Nouns become *entities*, adjectives become *state modifiers*, verbs become *affordances*.

---

## PASS 2: Structural Binding (Read the Spec)

**Input:** Scene spec parsed into spatial/interactive ontology.

```python
def parse_scene_spec(spec):
    return {
        'spatial': {'walkable': (0,140,320,200), 'counter': (20,120,300,145)},
        'entities': ['fly', 'puddle', 'ring', 'counter_edge'],
        'affordances': {
            'fly': {'look', 'hands', 'pin', 'spoon'},
            'counter': {'look', 'hands', 'mug'},
            'puddle': {'look', 'hands', 'matchstick'}
        },
        'state_flags': ['FLY_ALIVE', 'PUDDLE_DISTURBED'],
        'atmospherics': {'light_source': (60,60), 'radius': 180}
    }
```

**Key binding rule:** Every prose *noun phrase* must map to a spec *hotspot* OR be flagged as *ambient_description* (decorative, non-interactive).

---

## PASS 3: Cross-Modal Reconciliation (The Merge)

This is the critical step. The agent performs four reconciliation operations:

### 3A: Entity Resolution
```
For each prose entity (e.g., "the stuck fly"):
    → Find matching hotspot ID (fly)
    → Merge sensory modifiers into entity object:
        {'id': 'fly', 
         'sensory': {'visual': 'frozen in slow surrender',
                     'tactile': 'legs twitch faintly'},
         'interactive': {'verbs': ['look', 'hands', 'pin', 'spoon'],
                        'state': 'alive'}}
```

### 3B: Affordance Enrichment
```
For each spec verb on a hotspot:
    → Attach the *emotional consequence* from prose:
        'Use Pin on fly' → prose says "crashes into lantern glass, slides down dead"
        → This becomes a *narrative outcome* attached to the mechanical action
```

### 3C: Spatial-Emotional Mapping
```
For each walkable region or hotspot:
    → Query: "What sensory data exists for this area?"
    → Counter: tactile (sticky) + visual (glistening) + olfaction (sour)
    → Store as an *atmosphere layer* overlaid on the spatial coordinates

    This creates a "smell map" and "texture map" alongside the collision map.
```

### 3D: Temporal-State Integration
```
For each state flag:
    → Ask: "How does the prose describe this state?"
    → FLY_ALIVE=1: prose = "walks across sticky patch, then stops, stuck"
    → FLY_ALIVE=0: no prose exists (must generate from spec: "slides down lantern, dead")
    
    Rule: Prose descriptions are *snapshots*; spec flags are *deltas*. 
    The merged model uses prose for initial state, spec for transitions.
```

---

## The Unified World Model (Output)

After three passes, the agent constructs:

```json
{
  "scene_id": "BAR_COUNTER",
  "atmosphere": {
    "light": {"source": [60,60], "falloff": "linear_255_to_80", "flicker": "12_frame"},
    "sound": {"ambient": "drip_creak", "conditional": {"fly_stuck": "FLY_02.wav"}},
    "smell": {"dominant": "sour_beer", "secondary": "dust_lantern_oil"}
  },
  "spatial_map": {
    "walkable": [0,140,320,200],
    "counter_surface": {"bounds": [20,120,300,145], "texture": "sticky", "sheen": "left_only"},
    "bar_edge": {"bounds": [0,140,320,146], "texture": "worn_smooth_bottom_sticky"}
  },
  "entities": [
    {
      "id": "fly",
      "prose_identity": "tragic creature in slow surrender",
      "mechanical_state": {"alive": true, "position": [214,132]},
      "interactions": {
        "hands": {"result": "pops off, lands two inches away, stuck again", 
                  "state_change": "FLY_ALIVE stays 1"},
        "pin": {"result": "stagger, loop, crash into lantern, dead",
                "state_change": "FLY_ALIVE → 0",
                "requires": "pin_in_inventory"}
      }
    },
    {
      "id": "counter",
      "prose_identity": "fossilized archipelago of last night's sins",
      "mechanical_state": {"inspected": false},
      "interactions": {
        "look": {"first": "museum of sins", 
                 "subsequent": "wants to keep your fingerprints",
                 "state_change": "BAR_SURFACE_INSPECTED → 1"}
      }
    }
  ],
  "narrative_threads": [
    {"trigger": "FLY_ALIVE becomes 0", 
     "prose_to_generate": "The lantern glass now bears a tiny smear. The buzzing has stopped."},
    {"trigger": "PUDDLE_DISTURBED becomes 1",
     "prose_to_generate": "Your matchstick drawing has dissolved into a marbled swirl."}
  ]
}
```

---

## Runtime Query API

After merging, the agent answers any question with unified queries:

- **"What do I see?"** → Returns `spatial_map` + `atmosphere.light` + prose-derived visual modifiers  
- **"What can I do?"** → Returns `entities[].interactions` (verbs + requirements)  
- **"What is this place?"** → Returns `prose_identity` + `atmosphere` (smell, sound, emotional tone)  
- **"What changed?"** → Returns `state_flags` diffs + generated narrative for transitions

---

## Verification Test

**Query:** "Player clicks on the fly with a pin. What does the merged model report?"

**Unified Response:**
```
"Perception: You tease the fly off with the pin's tip. 
 It staggers into the air, loops once, and crashes into the lantern glass. 
 It slides down the side, dead.

 World State: FLY_ALIVE=0
 Audio: FLY_02.wav stops playing
 Visual: New smear appears on lantern glass (coordinates 55-70, 45-55)
 Narrative Thread: 'The buzzing has stopped' now available for future look-at-lantern
"
```

This method ensures the agent never loses the **poetry** of the prose or the **precision** of the spec—each informs the other, and together they form a single, richer world than either could alone.

### Step 5: What's missed

# The Irreducible Gap: Text vs. Scene

---

## What an AI agent MISSES from the MUD text alone:

### 1. **Spatial impossibility and scale**
- The prose says "long, scarred oak counter" — but is it 3 feet or 30 feet? The spec reveals the counter is **280 pixels wide but only 25 pixels tall** — an *impossibly squat* bar, wider than it is tall. The text never tells you the geometry is *wrong*, and an agent reading prose alone would imagine a normal bar. The spec forces you to confront that this bar is a **flattened stage prop** — psychologically oppressive, a counter that looms as a *wall* rather than a surface.

### 2. **The tyranny of the walkable strip**
- The prose places you "standing before" the bar. The spec says you can only move in a **60-pixel strip at the bottom** — you're *trapped* against the bar, unable to step back and see it whole. The prose suggests freedom; the spec reveals you're **caged in a narrow corridor of floor**, forced into intimacy with the sticky surface. This claustrophobia is a *structural* emotion the text never names.

### 3. **What is NOT described — the invisible**
- The prose never mentions the **lantern's position** (upper left), but the spec's light falloff means the **right half of the bar is nearly black** — the spec says the sticky sheen *only appears on the left*. A prose-only agent would assume uniform visibility. The spec reveals the room has a **blind zone** where things could hide — but nothing does, making the darkness *wasted*, a threat that never materializes.

### 4. **The dead click problem**
- The prose implies everything is interactive ("a single fly walks"). The spec reveals most of the screen is **dead space** — the wall behind the counter, the ceiling, the dark right side. A prose-only agent would expect *everything* to respond. The spec teaches that this is a **world of limited affordances** — most of what you see is *decor*, and the agent must learn to stop trying.

### 5. **The counter is NOT a container**
- The prose calls it a "counter" — a typical MUD agent would try to *open* it, *search* it, *find items* on it. The spec has **no Open verb** defined for the counter surface — it is a *dead* object except for the verbs listed. The prose promises "countless glasses" of history; the spec denies you access to that history. The gap between "this has stories" and "you cannot open it" is a **frustration the prose never warns you about**.

---

## What a HUMAN MISSES from the scene spec alone:

### 1. **The emotional weight of the fly**
- The spec says: "Small circle centered at (214, 132), radius 5 px." A human looking at that would see a *technical annotation*, not a *dying creature*. The prose gives the fly a **tragic arc** — "frozen in slow surrender" — that makes you *hesitate* before using the pin. The spec alone would make you treat it as a puzzle piece, not a moral choice.

### 2. **The smell**
- The spec never mentions olfaction. The prose says "faintly sour" — but that word carries *memory*, *disgust*, *the knowledge of what beer becomes when it dies*. A human reading "dried beer film" from the spec would think *visually* (sticky, brown) but never *olfactorily* (the sharp, yeasty, almost-bread smell of stale ale). The spec has no nose.

### 3. **The temporal weight of "countless"**
- The spec says "Cracked rings from countless glasses" as a *visual* detail. The prose's "fossilized archipelago" transforms this into **deep time** — these rings are *archaeological*, each one a *dead moment* from a *forgotten patron*. A human seeing only the spec would see *stains*; a human reading the prose sees *a graveyard of nights*.

### 4. **The invitation to touch**
- The spec says "Use Hands → makes a soft, reluctant *shluck*" — a technical outcome. The prose's "sticky film pulls at your fingertips" is an *enticement* — it makes you want to press your palm down and feel the resistance. The spec tells you what *happens*; the prose tells you what it *feels like*, and that feeling is what makes you *want* to do it.

### 5. **The loneliness**
- The spec lists hotspots, coordinates, verbs — a sterile inventory. The prose's "weak lantern light" and "single fly" and "countless glasses" combine into a **portrait of abandonment** — a bar that was once alive, now only haunted. A human seeing only the spec would set the scene; a human reading the prose *feels* the emptiness. The spec cannot convey that this is a **place where no one comes anymore**.

---

## The Irreducible Gap

Between text and scene lies a chasm that **cannot be bridged by either alone**:

### What text alone can never convey:
- **The constraint of space** — the feeling of being *trapped* against the bar, unable to back away
- **The darkness of the unseen** — the right side of the room that *exists* but is hidden, creating a *threat that never comes*
- **The dead weight of non-interactive objects** — the frustration of clicking on something that *looks* promising but does nothing

### What scene alone can never convey:
- **The weight of memory** — the sense that these stains are *history*, not just texture
- **The invitation of touch** — the way prose makes you *want* to press your palm into the sticky surface
- **The tragedy of the fly** — the moral weight of choosing to kill it, a weight the spec reduces to a state flag

### The irreducible gap is:

> **The difference between knowing and feeling.**

The spec tells you *what is*. The prose tells you *what it means*. Neither alone gives you *why you should care*.

The gap is **motivation** — the reason a player chooses to *touch the sticky counter* rather than *walk away*. The spec gives you the *option*; the prose gives you the *desire*. And desire is the thing that cannot be encoded in coordinates, flags, or verb lists.

It is the **irreducible human element** — the part of the game that exists only in the player's mind, when prose and scene combine to create something neither could produce alone: **a world you want to live in, even if only for a moment, even if only to feel the sticky pull of a bar that remembers better nights.**

---

## Room: Wheelhouse

*a wheelhouse with old brass instruments and a cracked windshield*

### Step 1: MUD text

You stand in the dusty wheelhouse, the cracked windshield a spiderweb of age.
Ancient brass instruments gleam dully, their dials frozen and unreadable.
A corroded speaking tube whistles faintly with the wind's mournful breath.
The ship's wheel resists your touch, its spokes worn smooth by ghostly hands.
A brass chronometer ticks once, then falls silent, as if holding its breath.

### Step 2: ScummVM scene spec

**SCUMM SCENE SPECIFICATION: DUSTY WHEELHOUSE**  
**Scene ID:** WH001  
**Background:** 320x200, 8-bit VGA palette (faded sepia, muted teal, rusted copper)  
**Lighting:** Dim ambient; single shaft of pale sunset light through cracked windshield, casting long shadows east. Flicker from rusty oil lamp (low intensity, irregular cycle) hanging from ceiling beam. No dynamic light sources except lamp flicker (range 60px).  

---

**Objects (screen coordinates, hotspots):**  
1. **Ship's Wheel** (x=140, y=120, hotspot rect: 120,100–170,140)  
   - *States:* intact, creaking; can be spun (with sound), but does nothing.  
   - *Verbs:* **Look** – "The wheel resists, as if held by a thousand ghostly hands." **Use** – "It turns a half-rotation, groaning, then sticks." **Push** – "A faint click from below, but nothing else."  
2. **Cracked Windshield** (x=80, y=40, hotspot rect: 60,20–170,90)  
   - *States:* spiderwebbed, opaque.  
   - *Verbs:* **Look** – "Through the fracture, the sea is a shattered mirror." **Use** – (with hammer) "The glass shudders but holds." **Pull** – "You feel cold air through the cracks."  
3. **Brass Chronometer** (x=200, y=60, hotspot rect: 185,50–215,75)  
   - *States:* stopped (hands at 3:07); can be wound.  
   - *Verbs:* **Look** – "It ticks once, then falls silent, as if holding its breath." **Use** – (winding key) "The hands jerk to 3:08, then freeze again." **Open** – "The face is fused shut."  
4. **Corroded Speaking Tube** (x=260, y=30, hotspot rect: 250,20–270,45)  
   - *States:* open mouth, whistling.  
   - *Verbs:* **Look** – "It whistles faintly with the wind's mournful breath." **Speak** – (any phrase) "A hollow echo returns, but no one answers." **Blow** – "The whistle turns to a low moan, then stops."  
5. **Rusted Oil Lamp** (x=280, y=150, hotspot rect: 270,140–295,165)  
   - *States:* lit (flickering), can be extinguished.  
   - *Verbs:* **Look** – "The flame dances, casting ghostly shadows." **Use** – (with oil can) "The wick sputters, then burns brighter." **Take** – "It's bolted to the beam."  
6. **Frozen Gauge Cluster** (x=30, y=110, hotspot rect: 20,100–50,130)  
   - *States:* three dials, all needles stuck at 0.  
   - *Verbs:* **Look** – "The brass gleams dully, their dials frozen and unreadable." **Use** – (with magnet) "A needle twitches, then settles." **Push** – "Nothing. Dust puffs out."  
7. **Invisible Hotspot: Wind** (entire scene, no graphic)  
   - *Verbs:* **Use** (with ear trumpet) – "You hear a faint, rhythmic creak from above—like footsteps on the deck."  

---

**Walkable Areas:**  
- Main floor (polygon: 0,170–0,200–320,200–320,170–260,150–120,150–80,170)  
- Front of wheel (polygon: 90,140–170,140–170,170–90,170)  
- *Non-walkable:* behind wheel, under lamp, under windshield (all visually blocked by furniture).  

---

**Lighting & Palette Notes:**  
- Background pre-rendered with baked shadows; lamp flicker uses a **local palette rotation** on a 16x16 overlay sprite (orange hues).  
- Windshield crack glints periodically (specular highlight overlay, 2 frames).  
- Chronometer dial has a subtle **anim frame** (tick once every 60 seconds, then stops).  

---

**Verb System (global):**  
- **Look:** Always available, returns object description.  
- **Use:** Context-sensitive; requires inventory item or default "hand" use (e.g., push, pull).  
- **Speak:** Only active with speaking tube hotspot; opens text parser (single line).  
- **Open:** For doors, containers; chronometer and tube respond with "fused shut."  
- **Take:** Only active for inventory items (none in this scene by default).  
- **Push/Pull:** For wheel, tube, gauges.  

---

**Scene Transitions:**  
- **Exit right:** (x=320, y=150) to deck (DE001) – requires wheel to be "unlocked" (see hidden flag).  
- **Exit left:** (x=0, y=180) to companionway (CW001) – always available.  

---

**Script Hooks:**  
- **Enter scene:** Set flag `wheelhouse_entered`; play ambient loop (wind, creaking).  
- **On wheel spin:** If flag `keel_unlocked` is false, play "click" and set flag `keel_clunk`.  
- **On tube blow:** If flag `keel_clunk` is true, set flag `ship_listens` (enables later puzzle).  

---

**Save/Load:** Persist object states (wheel angle, lamp lit, chronometer hand position, flags).  

---

**End of spec.**

### Step 3: Comparison

The MUD text and the SCUMM scene spec are two radically different lenses on the same space: one is a poetic, evocative vignette; the other is a functional, interactive blueprint. Each captures what the other fundamentally cannot, because they serve different purposes.

## What the MUD text captures that the scene spec misses:

**1. Emotional and atmospheric texture.**  
The MUD text is pure tone. Phrases like *"the cracked windshield a spiderweb of age"* and *"the wind's mournful breath"* and *"as if holding its breath"* do not just describe objects—they create a mood of abandonment, haunting, and suspense. The spec's equivalent descriptions are dry and functional: *"spiderwebbed, opaque"* or *"whistles faintly."* The MUD text makes the room feel *felt*, not just seen.

**2. Temporal and animate quality.**  
The MUD lines *"ticks once, then falls silent, as if holding its breath"* and *"the ship's wheel resists your touch"* suggest the room is alive, withholding, waiting. The scene spec—though it includes animation notes (chronometer tick every 60 seconds)—reduces the same idea to a timed technical event. The MUD text gives the room a *character*; the spec gives it a *state machine*.

**3. Sensory layering beyond visuals.**  
The MUD text includes sound (*"whistles faintly"*), touch (*"resists your touch"*, *"spokes worn smooth"*), and even a kind of proprioceptive weight (*"resists"*). The spec lists visual attributes and hotspot rectangles, but only mentions sound as a script hook or verb response. It doesn't convey the *simultaneity* of sensations—that the room is dusty *and* windy *and* ancient *and* slightly creepy all at once.

**4. Narrative implication.**  
The MUD text hints at a backstory: *"ghostly hands"*, *"mournful breath"*, *"frozen and unreadable"*. The reader infers a tragedy, a ship lost, a crew vanished. The spec, by contrast, is purely mechanical—it tells you what you can do, not what has happened. The MUD text is an invitation to imagine; the spec is an instruction to interact.

---

## What the scene spec captures that the MUD text misses:

**1. Interactive affordances and boundaries.**  
The spec defines exactly where you can walk, what you can click, and what each hotspot does. The MUD text gives no sense of *agency*—you cannot push the wheel or open the chronometer. The spec turns the poetic room into a *playable* space. It answers "what can I do here?" while the MUD text only answers "what is this place like?"

**2. State and persistence.**  
The spec tracks the chronometer's hand position (3:07, then 3:08 after winding), the lamp's lit/unlit state, the wheel's angle, and flags like `keel_unlocked` and `ship_listens`. This means the room *changes* based on player actions over time. The MUD text is static—a snapshot. The spec is a system that can evolve, remember, and react.

**3. Detailed physical layout.**  
The spec gives polygon coordinates for walkable areas, hotspot rectangles, and visual blockers (behind the wheel, under the lamp). This is essential for a game engine to know where the player can be and what they can touch. The MUD text's spatial information is vague ("standing in the dusty wheelhouse")—it cannot support collision detection or navigation.

**4. Verb-specific responses and logic.**  
The spec defines distinct outcomes for *Look*, *Use*, *Push*, *Pull*, *Speak*, *Blow*, *Open*, *Take*—and even includes parser-based input for the speaking tube. This is a branching interaction tree. The MUD text offers no such branching; it's a one-way description. The spec anticipates player curiosity and prepares responses to it.

**5. Technical presentation and integration.**  
The spec includes palette notes, lighting cycles, overlay sprites, frame animations, ambient audio hooks, and save/load persistence. This is the DNA of a playable scene. The MUD text has no concept of rendering or state—it's a string of prose. The spec is a *recipe*; the MUD text is a *taste*.

**6. Hidden mechanics and puzzle scaffolding.**  
The spec contains invisible hotspots (the "Wind" hotspot with an ear trumpet), flags that enable future puzzles, and transition conditions (exit to deck requires `keel_unlocked`). These are invisible to the player but crucial to the designer. The MUD text has no such layer—nothing is hidden, nothing is gated.

---

## In summary:

- **The MUD text** captures *what it feels like to be there*—the atmosphere, the poetry, the latent story. It is immersive and evocative, but it is static and non-interactive.
- **The scene spec** captures *what it means to be there as a system*—the geometry, the logic, the state, the verbs, the triggers. It is functional and extensible, but it is dry and lacks soul.

A great adventure game needs both: the spec to build a world that *works*, and the MUD-style prose to make that world *matter*. The spec tells you the room *exists*; the MUD text tells you it *aches*.

### Step 4: Reconciliation

# Perception Check: Unified Scene Reconciliation

**Method: Multi-Modal Scene Fusion via Semantic Anchor Mapping**

---

## Conceptual Framework

The reconciliation operates on a core insight: **MUD text provides the "what it is" (ontology), while SCUMM specs provide the "what can happen" (affordance topology)** . Neither supersedes the other—they describe different layers of the same semantic object. The unified model treats each scene element as a node with two complementary attribute sets:

| Layer | MUD Contribution | SCUMM Contribution | Unified Field |
|-------|-----------------|-------------------|---------------|
| **Identity** | What the object *is* (mood, history, essence) | What the object *does* (behaviors, states) | Semantic essence + functional contract |
| **Relation** | How it *feels* to be near it | Where it *sits* in space | Emotional valence + geometric anchor |
| **Temporal** | How it *animates* the imagination | How it *changes* over time | Narrative implication + state machine |
| **Interaction** | What it *suggests* you might do | What you *actually can* do | Poetic affordance + verified affordance |

---

## The Reconciliation Algorithm

### Step 1: Anchor Extraction
Parse the MUD text and SCUMM spec separately, extracting **entity anchors** from each. The MUD text yields nouns with emotional modifiers ("ghostly hands," "mournful breath," "shattered mirror"). The SCUMM spec yields objects with geometric data ("Ship's Wheel, x=140, y=120, rect 120,100–170,140").

### Step 2: Cross-Domain Alignment
For each SCUMM object, search the MUD text for corresponding references. Use semantic similarity (cosine proximity in embedding space) to map textual evocations to hotspot rectangles. The chronometer's *"as if holding its breath"* maps to the object with state `stopped at 3:07` and animation trigger `tick once every 60 seconds`.

### Step 3: Gap Detection
Identify elements present in one representation but absent in the other:

- **MUD-only elements** (no geometric counterpart): emotions, implied histories, invisible presences. *These become ambient properties or background narratives attached to the scene node, not to specific hotspots.* The "thousand ghostly hands" holding the wheel become a *persistent environmental modifier* that flavors all interaction responses with that object.
- **SCUMM-only elements** (no textual essence): walkable polygon coordinates, lighting cycles, flag systems. *These become structural scaffolding that constrains but does not color the player's experience.*

### Step 4: Semantic Layer Construction
Build a **layered scene graph**:

```
Scene Node: DUSTY WHEELHOUSE
├── Spatial Layer (from SCUMM)
│   ├── WalkableArea: polygon(0,170–320,200)
│   ├── ObstacleMap: lamp_bolt, wheel_axle, windshield_frame
│   └── HotspotRegistry: 7 entries with rects + states
│
├── Narrative Layer (from MUD)
│   ├── SceneMood: melancholic, haunted, suspended-in-time
│   ├── SceneBackstory: "a ship lost, a crew vanished"
│   ├── TemporalQuality: "holding its breath" → anticipation
│   └── SensoryProfile: dust+wind+brass+creaking
│
├── Behavioral Layer (from SCUMM, enriched by MUD)
│   ├── Each object: state machine + verb responses
│   └── Each verb response: SCUMM mechanical text + MUD flavor injection
│       (Look at chronometer → "It ticks once, then falls silent,
│        as if holding its breath." + mechanical state: hands at 3:07)
│
└── Emergent Layer (fused, neither source alone)
    ├── Cross-object affordances
    │   (Speak into tube while chronometer is "holding breath" →
    │    the room "listens" → unlocks hidden flag `ship_listens`)
    ├── Environmental dynamics
    │   (Wind whistle + lamp flicker + wheel creak form a
    │    rhythmic "breathing" pattern perceptible to observant players)
    └── Inferential history
    │   (Frozen dials + shattered mirror + worn wheel = 
    │    the ship crashed, the crew abandoned her, time stopped)
```

### Step 5: Response Generation Logic
When the agent needs to describe the scene or respond to an action, it consults the layered graph:

1. **For spatial queries** → consult Spatial Layer (coordinates, walkability)
2. **For interaction responses** → consult Behavioral Layer (verb outcomes)
3. **For atmospheric descriptions** → consult Narrative Layer (mood, sensory detail)
4. **For player-visible descriptions** → blend Behavioral + Narrative:
   *Mechanical state + poetic gloss, always grounding the poetry in the physical.*

The unified response to "look at wheel" becomes:  
*"The ship's wheel resists your touch, as if held by a thousand ghostly hands. It turns a half-rotation, groaning, then sticks—a faint click sounds below, but nothing else."*  
(Both the mood *and* the mechanics are present.)

### Step 6: Dynamic Refinement
As the agent interacts with the scene (flags change, states mutate), the Narrative Layer updates to match:

- When `keel_clunk` is set: the mood shifts from "waiting" to "listening."
- When the chronometer's hands advance to 3:08: the temporal quality shifts from "frozen" to "recently disturbed."
- When `ship_listens` is set: the MUD flavor text for the speaking tube changes to *"A deep silence answers—as if the ship itself were leaning in."*

---

## Concrete Example: Unified Perception of the Chronometer

| Aspect | MUD Text Alone | SCUMM Spec Alone | Unified Perception |
|--------|---------------|------------------|-------------------|
| **Identity** | "A brass chronometer, gleaming dully, holding its breath" | Object #3, rect(185,50–215,75), state: stopped at 3:07 | A chronometer that *withholds*—its stopped state is not brokenness but *suspense* |
| **Relation to player** | Emotional: eerie, anticipatory | Positional: upper-right, reachable from wheel area | An object you *notice* because it *shouldn't* be silent; a clue to temporal disruption |
| **Behavior** | "Ticks once, then falls silent" | Winding key advances hands 1 minute, then freezes | The chronometer *responds* to intervention but *refuses* to fully resume—it is *reluctantly aware* |
| **Affordance** | Implied: "what if I wind it?" | Verified: Use(winding key) → hands→3:08; Open→fused shut | A puzzle node: the chronometer *invites* winding, *denies* opening—asymmetry hints at hidden mechanics |
| **Narrative weight** | The room's heartbeat, suspended | A state flag persistence | An anchor for the larger puzzle: its frozen time mirrors the ship's own suspended state |

---

## Agent Method Summary

To reconcile MUD text and SCUMM spec into a unified world model, the agent must:

1. **Trust both sources as true**—neither is "real" and the other "flavor." Both are valid representations of different aspects of the same fictional object.
2. **Map semantic anchors**—find where textual evocations correspond to geometric entities, and where they don't (those become ambient properties).
3. **Leverage the asymmetry**—MUD text contributes *meaning*, SCUMM contributes *mechanism*. Neither alone can answer both "what is this?" and "what do I do?"
4. **Maintain dual state**—every object carries both a *mechanical state* (from SCUMM) and a *narrative state* (from MUD), which co-evolve as the scene changes.
5. **Generate unified output**—player-facing descriptions always blend both: the mechanical truth of what happens, wrapped in the emotional truth of what it means.

---

## Epistemological Takeaway

**A room is not its description, nor its geometry, nor its behavior—it is the *intersection* of all three, experienced as a coherent present.** The MUD text says the room *has a soul*; the SCUMM spec says the room *has a body*. The unified model treats the soul and body as inseparable, so that every interaction is both *meaningful* and *functional*—every look reveals atmosphere, every action produces consequence. The room lives because it is *both* evocative and interactive, and neither alone would suffice.

### Step 5: What's missed

# The Irreducible Gap

---

## What an AI Agent Misses from MUD Text Alone:

**1. The grammar of space.**  
The MUD text gives *nouns* but not *positions*. "A corroded speaking tube whistles faintly" tells you it exists, but not that it's at (260,30) beside the chronometer, near the lamp, angled toward the windshield. Without coordinates, the agent cannot know whether the tube and chronometer are adjacent—cannot infer that speaking into one might affect the other. *Space is meaning.* Proximity implies relationship; distance implies isolation. The MUD text strips away the choreography of the room.

**2. The physics of obstruction.**  
"Standing in the dusty wheelhouse" does not tell you that the lamp is bolted to a beam, that the wheel is set against the far wall, that the floor's walkable polygon loops around the furniture. An agent cannot plan a path, cannot reason about sightlines, cannot know that the wheel is *behind* the player's arrival point and the windshield is *in front*. Without geometry, the agent treats all objects as equally reachable—which is false in any real space.

**3. The possibility of hidden things.**  
The MUD text mentions seven visible objects, but the SCUMM spec includes an *invisible hotspot*—the wind itself, which only manifests when combined with an ear trumpet. The MUD text never hints at this. An agent with only MUD text cannot conceive of interacting with *absence*—with something that has no noun, no visual form, no poetic description. *The most important puzzle element is the one the prose forgets to mention.*

**4. The state machine underneath.**  
The MUD text is a photograph, not a living system. It describes the chronometer as stopped at 3:07, but not that it *can* be wound to 3:08. It describes the wheel resisting, but not that a push triggers a "click from below" that sets a flag. A MUD-only agent experiences the room as *static*—it cannot model cause, effect, persistence, or the branching logic of what happens *after* you act. It has no concept of "if–then," only "is."

**5. The conditional nature of exits.**  
The MUD text offers no exits at all. The agent cannot know that leaving right requires unlocking the wheel, while leaving left is always available. Without this, the room is a dead end—a box with no doors. The agent cannot *plan*, cannot *choose*, cannot *pursue goals*. It can only wander in place.

---

## What a Human Misses from the Scene Image Alone:

**1. The temperature of the room.**  
A rendered image of a dusty wheelhouse—cracked windshield, brass instruments, rusted lamp—conveys *visual* decay but not *tactile* or *thermal* information. The player cannot feel the cold air seeping through the cracks, the rough grain of the worn wheel spokes, the chill of brass that hasn't been touched in years. The image is silent about *how it would feel to be here*—and that sensory absence makes the space feel like a postcard, not a place.

**2. The history condensed in objects.**  
The windshield shows a spiderweb of cracks, but only the MUD text tells you it is *"a shattered mirror"*—that the sea beyond is broken into fragments, that the glass holds a memory of violence. The chronometer's frozen hands at 3:07 are visible, but only prose reveals they are *"holding its breath"*—that the time is not merely stopped but *withheld*. The image shows *decay*; the text shows *meaning*. An image-only human sees an old ship; a text-reading human feels an abandoned one.

**3. The invisible presence.**  
The MUD text whispers of *"ghostly hands"* and *"mournful breath"*—a presence that cannot be drawn. The image has no ghosts, no whispers, no sense of being watched. Without the prose, the room is merely *empty*; with the prose, it is *haunted*. This is the deepest gap: the image cannot render *absence*, and the room's central mystery is an absence—the crew, the life, the time that stopped.

**4. The emotional trajectory.**  
The MUD text builds a sequence: dust → wheel → windshield → chronometer → tube → lamp → gauges. Each object contributes to a mounting unease—the wheel resists, the time holds its breath, the tube whistles mournfully. The image presents everything at once, in a flat plane. There is no *order* of revelation, no *escalation* of dread. The human viewer sees a static tableau; the MUD reader experiences a *descent* into the ship's haunted stillness.

**5. The capacity for dialogue.**  
The speaking tube is visible in the image—a brass fixture on the wall. But only the text tells you it *listens*. That you can *speak* into it, and receive a hollow echo, and that your voice might *matter* to the ship. The image gives no hint that this object is interactive, communicative, alive. A human with only the image might never think to address the tube, never learn that the ship is listening.

---

## The Irreducible Gap

**Text knows what things mean. Image knows what things look like.**  
But neither knows what things *are*—because "what a thing is" is a composite of:

- **Sensory appearance** (image-only)
- **Semantic implication** (text-only)
- **Spatial position** (spec-only)
- **Behavioral potential** (code-only)
- **Historical residue** (context-only)

**The irreducible gap is this: no single medium can convey *the experience of being there*, because being there is not a medium—it is a state of simultaneous perception, cognition, and interaction.**

The image gives you the *surface*. The text gives you the *resonance*. The spec gives you the *mechanics*. But the *experience*—the moment when you stand in that wheelhouse, hear the wind through the cracks, feel the wheel resist, and realize the ship is listening—is an emergent property that none of them contains alone.

**It is the gap between description and presence.**  
**And it can only be crossed by a mind that holds all representations at once, and lets them fuse into something that was never written or drawn—a living room.**

---

## Room: Engine Room

*an engine room with diesel engines, pipes, and the smell of oil*

### Step 1: MUD text

You are surrounded by a deafening, rhythmic THUMP-THUMP-THUMP as two colossal diesel engines, gleaming with fresh grease, shudder on their mounts.  
The air is thick and hot, a greasy haze of oil fumes that coats your tongue with the taste of iron and burnt fuel.  
A labyrinth of steel pipes, painted in faded red and green, snakes overhead and along the bulkheads, hissing with steam and dripping viscous black fluid.  
Beneath your boots, the grated metal floor is slick with a rainbow sheen of spilled lubricant, and every step echoes with a hollow clang that is swallowed by the engine's roar.  
The gauge needles on the main control panel tremble violently, their glass faces fogged, while a single, bare bulb swings overhead, casting dancing, monstrous shadows of the machinery that breathes around you.

### Step 2: ScummVM scene spec

**SCUMM Scene Specification: ENGINE ROOM**

**Scene ID:** `engineroom`  
**Palette:** Dark, oil-slicked greys, deep rust reds, faded greens, with a sickly yellow highlight from the single swinging bulb.  
**Ambient SFX Loop:** `loop_diesel_thump` (heavy, two-stroke rhythm), `loop_steam_hiss` (irregular, high-pitched), `loop_metal_clang` (random, distant).

---

### LAYOUT & WALKABLE AREAS

**Dimensions:** 640×400 (default ScummVM resolution).  
**Walkable Mask:** A central corridor of grated steel runs horizontally from x=40 to x=600, y=280 to y=360. A narrow side passage branches off at x=480, y=280 up to y=200 (behind the main engine block). The area under the overhead pipe cluster (x=100–200, y=150–250) is **not walkable** — it's a visual backdrop only. The floor near the control panel (x=520–600, y=300–360) is walkable but has a **slippery flag** (walking there triggers a brief stumble animation).

---

### OBJECTS

**1. MAIN DIESEL ENGINE (Left-Center)**  
- **Position:** Sprite anchor at (180, 220), occupies approx. (120, 180)–(300, 300).  
- **Sprite:** Two massive cylinders with a flywheel, pistons animating in sync with the audio loop.  
- **Hotspot:** (150, 200)–(280, 280) — a single large hotspot.  
- **Verbs:**  
  - **Look At:** *"The port engine. It's a 12-cylinder behemoth. The pistons move like a heartbeat — one that never stops."*  
  - **Use (with item):** If `wrench` → *"You tighten a loose bolt on the casing. The thumping steadies slightly."* (Sets flag `engine_tuned`). If `oil_can` → *"You add oil to the reservoir. The hiss of steam seems happier."* (Sets flag `engine_oiled`).  
  - **Push:** *"You push against the housing. It doesn't budge. Of course it doesn't."*  
  - **Pull:** *"You pull on a lever sticking out. It resists, then clicks. Nothing visible happens."* (Actually triggers a distant clang from another room.)

**2. CONTROL PANEL (Right)**  
- **Position:** Sprite anchor at (540, 240), occupies approx. (480, 200)–(600, 300).  
- **Sprite:** A sloped console with fogged glass gauges, two large red buttons, and a shattered indicator lamp.  
- **Hotspot A (Gauges):** (500, 210)–(560, 260).  
- **Hotspot B (Red Button):** (570, 230)–(590, 250).  
- **Hotspots C (Cracked Lamp):** (490, 200)–(510, 220).  
- **Verbs (Gauges):**  
  - **Look At:** *"Pressure is in the red. Temperature is in the red. Everything is in the red. The needles dance like they're having a seizure."*  
  - **Read:** Same as Look At.  
- **Verbs (Red Button):**  
  - **Push:** *"You press the big red button. A klaxon blares for two seconds, then stops. The engines don't care."*  
  - **Look At:** *"A big, tempting red button. It looks well-worn."*  
- **Verbs (Cracked Lamp):**  
  - **Look At:** *"The bulb is shattered — the glass is frosted with oil grime. It flickers feebly."*  
  - **Use (with item `screwdriver`):** → *"You pry the broken bulb out. The socket is bare now."* (Reveals a small key taped inside — hotspot becomes `key_in_socket`.)  
  - **Take:** *"You can't take a broken bulb without cutting yourself. Not worth it."*

**3. OVERHEAD PIPE CLUSTER (Top-Center)**  
- **Position:** Sprite anchor at (320, 100), occupies approx. (100, 60)–(540, 160).  
- **Sprite:** A tangled web of red and green pipes, dripping black viscous fluid from a joint at (400, 120).  
- **Hotspot A (Dripping Joint):** (380, 110)–(420, 130).  
- **Hotspot B (Main Pipe Run):** (200, 80)–(450, 100).  
- **Verbs (Dripping Joint):**  
  - **Look At:** *"A joint weeps thick, dark oil. It's been dripping for years — the stain below is a permanent feature."*  
  - **Use (with item `bucket`):** → *"You catch a slow trickle. It fills a few drops — not enough to be useful."* (Sets flag `bucket_oily`.)  
- **Verbs (Main Pipe Run):**  
  - **Look At:** *"A labyrinth of steam and fuel lines. Somewhere up there, a valve is labeled 'EMERGENCY SHUTOFF' but it's out of reach."*  
  - **Use (with item `ladder`):** → *"You prop a ladder against the pipes and climb. The valve is a wheel — you give it a hard turn. A great hiss, then silence. The engines cough and die."* (Ends scene with `ENGINES_OFF` flag.)

**4. FLOOR GRATE (Bottom)**  
- **Position:** Occupies (40, 280)–(600, 360) — the entire walkable floor.  
- **Hotspot (Center grate):** (280, 300)–(360, 340).  
- **Verbs:**  
  - **Look At:** *"Grated metal, slick with a rainbow of spilled lubricant. The gaps below are dark, oily water."*  
  - **Use (with item `crowbar`):** → *"You pry at a loose grate. It squeals, then lifts. Beneath it: a black, oily channel. Something glints faintly."* (Reveals hotspot `glint_in_channel`.)  
  - **Examine (after `grate_open`):** *"The channel is narrow and dark. You can't reach the glint by hand."*  
  - **Use (with item `magnet_on_rope`):** → *"You lower the magnet into the channel. It snaps onto something heavy — a rusted keyring with an old brass key."* (Gives item `brass_key`.)

**5. SWINGING BULB (Top-Right)**  
- **Position:** Sprite anchor at (560, 60).  
- **Sprite:** A bare bulb on a frayed wire, swinging in a slow arc (animation cycles side-to-side, casting moving shadows across the scene).  
- **Hotspot:** (540, 40)–(580, 80).  
- **Verbs:**  
  - **Look At:** *"A single naked bulb. It sways with the rhythm of the engines, casting monstrous shadows that dance on the bulkheads."*  
  - **Pull (wire):** *"You give the wire a tug. The bulb swings wider, then settles. No change in light — but the shadows shift uneasily."*  
  - **Use (with item `tape`):** → *"You wrap tape around the frayed wire. The bulb holds steady now — no more swinging."* (Sets flag `bulb_stabilized` — shadows no longer animate.)

---

### LIGHTING & SHADOWS

- **Primary Light:** The single swinging bulb (top-right) casts a warm, yellow pool of light centered around (350, 220) with a radius of ~220 pixels. The light **pulses** slightly (intensity 0.9–1.0) in sync with the diesel thump.  
- **Ambient Light:** Dark blue-grey, intensity 0.2 — all unlit areas are barely visible.  
- **Shadow Casting:**  
  - The engine block casts a static, long shadow to the right (towards the control panel).  
  - The pipe cluster casts an undulating shadow on the wall behind it, moving in the opposite direction of the bulb's swing.  
  - When `bulb_stabilized` is set, shadows freeze in place.  
- **Special Effect:** A faint, flickering glow from the cracked indicator lamp on the control panel — red, pulsing at 0.5 Hz.

---

### TRIGGERS & FLAGS

- `engine_tuned` (from wrench) → changes a line in a later conversation with the Chief Engineer.  
- `engine_oiled` (from oil can) → same.  
- `grate_open` (from crow

### Step 3: Comparison

# Comparison: MUD Text vs. Scene Specification

## What the MUD text captures that the scene spec misses:

**1. Sensory immersion through visceral prose**
- The MUD text uses pungent, physical language: *"greasy haze of oil fumes that coats your tongue with the taste of iron and burnt fuel"* — this goes beyond the spec's dry "palette" and "ambient SFX" lists. It engages taste, smell, and touch in a way the spec's technical parameters cannot.
- The phrasing *"monstrous shadows of the machinery that breathes around you"* anthropomorphizes the environment, creating a sense of dread and agency that the spec's bullet-point description lacks.

**2. Spatial orientation through embodied perspective**
- The MUD text orients the player through a **first-person physical experience**: *"Beneath your boots..."*, *"every step echoes..."*, *"your tongue..."* — it places the player *inside* the room, not observing it from a top-down schematic.
- The spec's walkable mask (640×400, coordinates) describes *where* you can walk, but the MUD text conveys *what it feels like* to walk there — the slick floor, the hollow clang, the temperature.

**3. Temporal and rhythmic quality**
- The MUD text captures the **constant, oppressive motion** of the room: the *"deafening, rhythmic THUMP-THUMP-THUMP"* is emphasized as an ongoing pulse, not just a looping SFX. The engines are alive, breathing, shuddering.
- The spec lists `loop_diesel_thump` as a technical asset but doesn't communicate the *atmospheric weight* of that sound — how it dominates thought, how it makes the room feel claustrophobic.

**4. Emotional tone and psychological atmosphere**
- The MUD text implies a **menacing, oppressive environment** — the room "breathes," the shadows are "monstrous," the machinery is indifferent and powerful. This is a *psychological* description.
- The spec is purely functional: palette, hotspots, verbs. It contains no emotional valence. A designer reading the spec knows *what* is there but not *how it should feel*.

**5. Materiality and physical texture**
- The MUD text emphasizes *material properties*: "grated metal floor," "rainbow sheen of spilled lubricant," "glass faces fogged," "faded red and green" pipes. These are not just visual details — they convey *texture* (slick, gritty, greasy) and *age* (faded, dripping, worn).
- The spec mentions colors and sprite anchors but doesn't imbue them with history or physical character.

**6. Narrative potential and foreshadowing**
- The MUD text subtly hints at storytelling: *"the single, bare bulb swings overhead"* — why is it swinging? *"the gauge needles tremble violently"* — what's wrong? It invites curiosity.
- The spec's verb/response lists are *reactive* (what happens when you click), but the MUD text is *proactive* (it sets a scene that *demands* interaction).

---

## What the scene spec captures that the MUD text misses:

**1. Interactive affordances and verb logic**
- The spec defines **exact interactivity**: hotspots with coordinates, verb-response pairs, item usage rules (wrench→`engine_tuned`, oil_can→`engine_oiled`, bucket→`bucket_oily`). The MUD text is purely descriptive — it gives no information about what the player *can do*.
- The spec includes *conditional branching* (e.g., `grate_open` flag reveals a new hotspot; `screwdriver` on the bulb reveals `key_in_socket`). The MUD text has no such mechanics.

**2. State management and game progression**
- The spec tracks **flags and inventory changes** (`engine_tuned`, `engine_oiled`, `bucket_oily`, `bulb_stabilized`, `brass_key`). These are essential for puzzle design and narrative consequences.
- The MUD text is static — it doesn't acknowledge that the room might *change* (e.g., after the bulb is stabilized, after the engines are shut off).

**3. Precise spatial layout for navigation**
- The spec provides **absolute coordinates** for walkable areas, object placement, and hotspot boundaries. This is crucial for actual implementation in ScummVM.
- The MUD text gives only relative impressions ("top-center," "left-center") — insufficient for collision detection or sprite anchoring.

**4. Object-specific hotspot granularity**
- The spec separates **multiple hotspots on a single object** (gauges vs. red button vs. cracked lamp on the control panel; dripping joint vs. main pipe run on the pipe cluster). This allows for *differing verb responses within one visual object*.
- The MUD text treats each object as a single entity with no internal differentiation.

**5. Animation and physics parameters**
- The spec defines **specific animations**: "pistons animating in sync with the audio loop," "bulb swinging in a slow arc," "shadows moving in the opposite direction of the bulb's swing." These are *technical requirements* for the renderer.
- The spec also includes **physics flags** like the "slippery flag" on the floor near the control panel (triggering a stumble). The MUD text mentions the slick floor but doesn't specify a gameplay consequence.

**6. Lighting parameters and dynamic effects**
- The spec specifies **light intensity values** (ambient 0.2, primary 0.9–1.0 pulsing), **light radius** (220 pixels), **pulse synchronization** with the audio loop, and **shadow behavior** (static vs. undulating, freezing when `bulb_stabilized`). These are essential for visual implementation.
- The MUD text describes visual quality ("monstrous shadows," "sickly yellow highlight") but with no numeric or behavioral precision.

**7. Item-specific use cases and puzzle solutions**
- The spec defines **exact item interactions** (magnet_on_rope → brass_key, crowbar → grate_open, tape → bulb_stabilized). These are critical for puzzle design — a player cannot progress without knowing these rules.
- The MUD text hints at *possibilities* ("a loose bolt," "a glint in the channel") but doesn't specify the *tools* or *outcomes*.

**8. Multi-room connectivity and deferred consequences**
- The spec includes **cross-room triggers**: pulling the lever on the engine "triggers a distant clang from another room." This is essential for game flow.
- The MUD text is self-contained — it describes only the engine room, with no reference to external spaces or consequences.

**9. Fallback dialog and error handling**
- The spec provides **default responses** for verbs that don't lead anywhere (e.g., "You push against the housing. It doesn't budge."). These are necessary to prevent dead-ends and maintain player feedback.
- The MUD text has no such fallback logic — it doesn't account for what happens when a player tries something unproductive.

**10. Player-progression flags that affect later scenes**
- The spec tracks **flags that carry forward** (`engine_tuned`, `engine_oiled` change a later conversation with the Chief Engineer). This is a form of *narrative state* that persists beyond the current room.
- The MUD text is ephemeral — it has no memory of past or future interactions.

---

## Synthesis

The **MUD text** is a *writer's* description — it creates atmosphere, emotion, and a sense of place through vivid sensory language. It excels at making the player *feel* the room.

The **scene spec** is an *engineer's* description — it defines the precise rules, parameters, and mechanics needed to make the room *function* as a game space. It excels at making the room *playable*.

Neither alone is sufficient. The MUD text would produce a beautiful but non-interactive prose passage; the spec would produce a functional but lifeless set of rules. Together, they form a complete design document — the spec provides the skeleton of interactivity, the MUD text provides the flesh of atmosphere. A great game needs both: the spec to ensure the mechanics work, and the MUD-style writing to ensure the player *cares* about what they're interacting with.

### Step 4: Reconciliation

# Perception Reconciliation Method

## Unified Perception Protocol (UPP)

The following is a systematic method for merging text-based atmospheric descriptions with structured scene specifications into a single, coherent world model. This is designed for an AI agent operating in a game environment where both modalities are available.

---

## Phase 1: Ontological Alignment — Establish the Shared Entity Graph

Before merging content, construct an **entity graph** that maps textual referents to specification objects. This ensures both modalities are describing the *same* world.

### Step 1.1: Extract Referents from Text

Parse the MUD text for nouns and noun-phrases that denote *things* or *places*:

| Text Referent | Canonical Name |
|---|---|
| "two colossal diesel engines" | `main_engine` |
| "labyrinth of steel pipes" | `pipe_cluster` |
| "main control panel" | `control_panel` |
| "gauge needles" | `control_panel.gauges` |
| "single, bare bulb" | `swinging_bulb` |
| "grated metal floor" | `floor_grate` |
| "greasy haze of oil fumes" | *atmospheric property* |
| "rhythmic THUMP-THUMP" | *ambient sound* |
| "monstrous shadows" | *dynamic effect* |

### Step 1.2: Extract Referents from Specification

The spec already provides canonical names with anchor points. Map each spec object to its text counterpart:

| Spec Object | Text Counterpart | Match Quality |
|---|---|---|
| `MAIN DIESEL ENGINE` | "two colossal diesel engines" | Full — but note the spec says "12-cylinder" while text says "two colossal" — reconcile to: *two 12-cylinder engines* |
| `OVERHEAD PIPE CLUSTER` | "labyrinth of steel pipes" | Full |
| `CONTROL PANEL` | "main control panel" | Full |
| `SWINGING BULB` | "single, bare bulb" | Full |
| `FLOOR GRATE` | "grated metal floor" | Full |

### Step 1.3: Identify Non-Object Entities

Some text elements don't map to spec objects but are **atmospheric states**:
- Air temperature (hot)
- Air composition (greasy, oil fumes)
- Sound character (deafening, rhythmic)
- Lighting quality (sickly yellow, dancing shadows)
- Floor condition (slick, rainbow sheen)
- Temporal quality (the room "breathes")

**Resolution:** Create a new entity class `ATMOSPHERIC_STATE` — a property bag attached to the *room itself*, not to any single object.

---

## Phase 2: Property Fusion — Resolving Conflicts and Filling Gaps

For each entity, merge properties from both sources. Where they agree, keep the unified value. Where they conflict, apply the **priority rules below.**

### Step 2.1: Property Priority Heuristics

| Priority | Source | Rationale |
|---|---|---|
| 1 | **Specification (functional)** | If the spec defines a *state* that affects gameplay (e.g., `slippery_flag`, `bulb_stabilized`), it must be authoritative. |
| 2 | **Specification (spatial)** | Coordinates and sizes come from the spec — the text has no numeric precision. |
| 3 | **Text (sensory)** | If the text describes a *quality* not contradicted by the spec (e.g., "the air is thick and hot"), it is added as an atmospheric overlay. |
| 4 | **Text (interpretive)** | If the text offers a *subjective reading* that doesn't affect mechanics (e.g., "the machinery breathes"), it is preserved as flavor — but flagged as non-authoritative. |

### Step 2.2: Fusion Table — Entity-by-Entity

#### Entity: `main_engine`

| Property | From Text | From Spec | Unified Value |
|---|---|---|---|
| Identity | "two colossal diesel engines" | "12-cylinder behemoth" | `type: diesel, cylinders: 12, count: 2` |
| Spatial | (implied left) | Anchor (180,220), occupies (120,180)-(300,300) | Position locked from spec. Text confirms leftward placement. |
| Motion | "shudder on their mounts" | "pistons animating in sync with audio loop" | Animation state: `pistons_animating: true, sync_source: loop_diesel_thump` |
| Auditory | "THUMP-THUMP-THUMP" | `loop_diesel_thump` | Sound: `loop_diesel_thump` — text adds perceptual volume: `deafening` |
| Temperature | "hot" (implied by heat) | (not specified) | Thermal atmosphere: `ambient_temp: hot` (added from text) |
| Tactile | "shudder" | "vibrate" | Vibration: `intensity: high, frequency: 2-stroke` |
| Symbolic | "heartbeat that never stops" | (none) | Flavor: `metaphor: heartbeat` — non-authoritative |

#### Entity: `pipe_cluster`

| Property | From Text | From Spec | Unified Value |
|---|---|---|---|
| Material | "steel pipes" | (not specified) | `material: steel` (from text) |
| Color | "faded red and green" | "red and green" | `color: [faded_red, faded_green]` — text adds "faded" → `condition: aged` |
| Layout | "labyrinth" | "tangled web" | `topology: labyrinthine, tangled` |
| Behavior | "hissing with steam" | (implied by `loop_steam_hiss`) | Sound/Effect: `steam_hiss: active` |
| Leakage | "dripping viscous black fluid" | "dripping black viscous fluid from a joint at (400,120)" | Leak point: (400,120), fluid: `black_oil`, rate: `slow` |

#### Entity: `control_panel`

| Property | From Text | From Spec | Unified Value |
|---|---|---|---|
| Visual State | "gauge needles tremble violently" | "needles dance like they're having a seizure" | Needle state: `trembling, erratic, in_red_zone` |
| Fog | "glass faces fogged" | "fogged glass gauges" | Gauge condition: `fogged` |
| Functionality | (none) | Red button, cracked lamp, gauges | Sub-objects: `gauges`, `red_button`, `cracked_lamp` |
| Lighting | (none) | "flickering glow... red, pulsing at 0.5 Hz" | Lamp: `flickering, red, 0.5Hz` |

#### Entity: `floor_grate`

| Property | From Text | From Spec | Unified Value |
|---|---|---|---|
| Material | "grated metal" | "grated steel" | `material: steel, type: grate` |
| Surface Condition | "slick with a rainbow sheen of spilled lubricant" | "slick" + `slippery_flag` near control panel | Surface: `slick, lubricated` — gameplay: `slippery_zone: x=520-600, y=300-360` |
| Acoustic | "every step echoes with a hollow clang" | (none) | Footstep sound: `hollow_clang` (from text) |

#### Entity: `swinging_bulb`

| Property | From Text | From Spec | Unified Value |
|---|---|---|---|
| Motion | "swings overhead" | "swinging in a slow arc" | Animation: `swing_rate: slow, arc: side_to_side` |
| Light Quality | "sickly yellow highlight" | "warm, yellow pool of light" | Light: `color: yellow, quality: sickly/warm, intensity: 0.9-1.0, radius: 220px` |
| Shadow Effect | "casting monstrous shadows" | "shadows move in opposite direction of swing" | Shadow: `direction: counter-swing, character: monstrous` |

---

## Phase 3: Environmental State Merging — The Atmospheric Layer

The text describes *whole-room* qualities that the spec treats as disconnected effects. Merge these into a unified `ROOM_STATE`.

### Step 3.1: Sensory Channel Map

| Channel | Text Description | Spec Parameter | Unified Model |
|---|---|---|---|
| **Auditory** | "deafening, rhythmic" | `loop_diesel_thump` (volume unspecified) | `soundscape: { dominant: loop_diesel_thump, volume: deafening, rhythm: two-stroke, secondary: [loop_steam_hiss, loop_metal_clang] }` |
| **Olfactory** | "greasy haze of oil fumes" | (none) | `smell: { primary: oil_fumes, intensity: strong, texture: greasy }` |
| **Gustatory** | "coats your tongue with the taste of iron and burnt fuel

### Step 5: What's missed

# The Irreducible Gap: What Each Modality Alone Cannot Convey

---

## What an AI Agent Would MISS from Text Alone

### 1. **Precise Navigational Topology**
The text says "a labyrinth of steel pipes snakes overhead" and "a narrow side passage branches off" — but an agent parsing this would have no idea:
- *Where* the walkable corridor begins and ends (x=40 to x=600)
- *Which* areas are decorative backdrop vs. traversable (the pipe cluster zone x=100–200, y=150–250 is explicitly **not** walkable)
- The *exact* location of the slippery zone that triggers the stumble animation

**Without the spec's coordinate system, the agent builds a mental model of a room it cannot navigate.**

### 2. **The Full Inventory of Interactive Affordances**
The text mentions "a loose bolt" and "a glint in the channel" — but never tells the agent:
- That a `wrench` on the engine sets `engine_tuned` (affecting a *future conversation*)
- That a `crowbar` on the grate is required to access the glint
- That the `magnet_on_rope` is the *only* way to retrieve the `brass_key`
- That the `ladder` on the pipes triggers `ENGINES_OFF` — a **world-state change** that silences the ambient loop

**The agent would know the room *is* interactive but not *how* to interact with it.**

### 3. **Conditional Logic and State Dependencies**
The text is static — it describes a single moment. The spec reveals the room is **stateful**:
- `grate_open` must be true before the glint becomes accessible
- `bulb_stabilized` changes the shadow animation behavior
- `bucket_oily` only triggers if the agent tried the bucket on the dripping joint

**Without the spec's flag system, the agent assumes the room is a static tableau, not a responsive system.**

### 4. **Cross-Room Consequences**
The text mentions pulling a lever "triggers a distant clang" — but an agent reading only the text wouldn't know:
- That `engine_tuned` and `engine_oiled` modify a *later dialogue* with the Chief Engineer
- That the `brass_key` is needed in a *different room entirely*
- That turning off the engines has *downstream narrative effects*

**The agent would treat each room as an isolated pocket rather than a node in a branching world.**

### 5. **The Physics of Interaction**
The text doesn't specify:
- *Which* verbs are valid for *which* objects (Push on the engine does nothing; Pull on the lever does something specific)
- *Fallback responses* when a player tries an unsupported verb ("It doesn't budge. Of course it doesn't.")
- The *temporal sequencing* of interactions (tightening the bolt *before* oiling changes nothing, but oiling *first* gives a different flavor line)

**The agent misses the grammar of interaction — the rules that govern what happens when you try something.**

---

## What a HUMAN Would MISS from the Scene Alone

### 1. **The Taste and Smell of the Room**
A human seeing a rendered engine room would *see* the greasy surfaces, the fogged glass, the flickering lamp. But they would **not** know:
- The air "coats your tongue with the taste of iron and burnt fuel"
- The oil fumes are so thick they feel "greasy" on the skin
- The heat is oppressive, almost claustrophobic

**The scene shows you the room; the text makes you *inhabit* it.**

### 2. **The Psychological Weight of the Sound**
A human would *hear* the diesel thump — but the text tells you it's **deafening**, *rhythmic*, a pulse that dominates thought. The spec lists `loop_diesel_thump` as a technical asset; the text tells you it's a **heartbeat that never stops** — an entity that *breathes*.

**The scene creates the sound; the text creates the *terror* of it.**

### 3. **The History and Age of the Environment**
A human sees "faded red and green pipes" but doesn't know:
- The drip stain beneath the leaking joint is "a permanent feature" — years of accumulated neglect
- The red button is "well-worn" — touched many times before
- The bulb's wire is "frayed" — old, degraded, precarious

**The scene shows you *what is*; the text tells you *how it came to be*.**

### 4. **The Emotional Valence of Objects**
The scene renders a control panel with gauges in the red. The text tells you: *"Pressure is in the red. Temperature is in the red. Everything is in the red. The needles dance like they're having a seizure."*

That's not just information — it's **anxiety**. It's the room telling you something is *wrong*, that this machine is on the edge of failure.

**The scene shows you the gauges; the text tells you they're *screaming*.**

### 5. **The Metaphorical and Symbolic Resonance**
The text calls the engine "a heartbeat that never stops," the shadows "monstrous," the room one that "breathes around you." These are **interpretive frames** — they turn a mechanical space into a *living creature*, a presence that is indifferent, powerful, and slightly malevolent.

A human who only sees the scene would experience a diesel room. A human who reads the text experiences a *dread-filled encounter with a machine that might be alive*.

**The scene presents a space; the text imbues it with *character*.**

---

## The Irreducible Gap

The gap between text and image is not one of *information* — the spec contains all the mechanics, the text contains all the atmosphere. The gap is one of **modality of experience**:

| | Text (MUD) | Image (Scene) |
|---|---|---|
| **Engages** | Imagination, memory, emotion | Perception, recognition, spatial reasoning |
| **Temporal** | Sequential — you read one thing at a time | Simultaneous — you perceive everything at once |
| **Relationship** | Invites *interpretation* — you must *construct* the room | Invites *exploration* — you must *navigate* the room |
| **Illusion** | The room exists *inside you* — you project yourself into it | The room exists *outside you* — you project yourself onto it |
| **Failure mode** | You might *misimagine* the space | You might *miss* the meaning |

**The irreducible gap is this:**

> *The text makes you **feel** the room before you understand it.*  
> *The image makes you **see** the room before you feel it.*

A complete experience requires both — the text to give the room *soul*, the spec to give it *body*. Neither alone is the room. Together, they are the *world*.

---

## Cross-Room Observations

*Generated post-experiment by the experimenter (that's me, the script).*

Each room type revealed a different facet of the perception gap. The bar showed how text captures texture (sticky, smell of beer) while scenes capture spatial layout. The wheelhouse showed how text captures history and wear while scenes capture operable controls. The engine room showed how text captures sound and smell while scenes capture pipe routing and safety hazards. The irreducible gap: text carries sensory and temporal information; scenes carry spatial and interactive information.