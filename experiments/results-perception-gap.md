# Experiment 1: Perception Gap — MUD Text vs ScummVM Scenes

*What does each representation MISS that the other catches?*

---

## Room: Bar

*a bar counter sticky with spilled beer*

### Step 1: MUD text

You are standing before a long, dark-stained oak counter.
The surface glistens, tacky with a thousand spilled beers.
A sticky film of dried ale and dust clings to your fingertips.
The air reeks of sour yeast, old smoke, and cheap whiskey.
Beneath the bar, a puddle of stale brew seeps toward your boots.

### Step 2: ScummVM scene spec

**SCUMM Scene Specification: "The Sticky Oak"**  
**Scene ID:** BAR_COUNTER_INT  
**Palette:** 256-color, VGA, dark sepia with amber highlights.  
**Music:** Low, droning bassoon loop with occasional off-key piano plinks (track: `TAVERN_DRONE`).

---

**Objects & Screen Positions (640x480 resolution):**

| Object ID | Name | Position (x, y) | Size (w, h) | Notes |
|-----------|------|-----------------|-------------|-------|
| `STALE_BEER_PUDDLE` | Puddle of stale brew | 120, 430 | 90x35 | Animated shimmer (2 frames) |
| `OAK_COUNTER_FRONT` | Sticky counter edge | 0, 380 | 640x15 | Surface hotspot for most verbs |
| `WHISKEY_BOTTLE` | Cheap whiskey bottle | 520, 300 | 25x70 | Tilted, half-empty |
| `SOUR_SMOKE_HAZE` | Cigarette smoke wisp | 300, 150 | 60x80 | 8-frame loop, semi-transparent |
| `ASH_TRAY` | Overflowing ashtray | 450, 340 | 40x12 | Butts spilling over edge |
| `DRIED_ALE_RING` | Circular stain ring | 380, 360 | 35x35 | Static decal |
| `BUBBLES_IN_PUDDLE` | Tiny bubbles in puddle | 140, 445 | 10x5 | 3-frame loop, occasional pop |

---

**Lighting:**  
- Ambient light: 0.35 (very dim, brownish tint).  
- Single flickering candle hotspot (not interactive) at `(610, 110)` — casts a weak, warm glow over the right third of the counter.  
- Left side (x<200) is nearly black (0.15 light), with a faint greenish under-glow from the puddle.  
- No direct light source on the player character; shadow falls backward onto the wall.

---

**Walkable Areas:**  
- **Main floor:** Rectangle `(0, 380)` to `(640, 480)` — player can walk left/right in front of the counter.  
- **Behind counter (blocked):** No walkable area, but visual parallax shows shelves behind the player character.  
- **Stool approach:** Small elliptical hotspot at `(300, 400)` — walk here to trigger "INSPECT COUNTER" auto-zoom.

---

**Hotspots (Clickable Regions):**

| Hotspot ID | Screen Region | Cursor | Verb Responses |
|------------|---------------|--------|----------------|
| `HS_COUNTER_TOP` | (0,380)-(640,395) | Magnifier | **Look at:** *"The varnish is gone, replaced by a thousand sticky fingerprints. The grain is invisible beneath the glaze."* |
| | | Hand | **Use:** "You press your palm flat. It makes a soft, wet *schlick* sound. You feel the grime." |
| | | Mouth | **Use (Taste):** "You dare not. The smell alone is a warning." |
| `HS_PUDDLE` | (110,420)-(210,470) | Magnifier | **Look at:** *"A dark, oily pool that reflects nothing. Tiny bubbles rise and pop with microscopic farts."* |
| | | Hand | **Use:** "You dip a finger in. It comes up coated with something that was beer three days ago." |
| | | Bottle (if in inventory) | **Use:** "You pour the last of your drink into the puddle. It merges without a ripple." |
| `HS_WHISKEY_BOTTLE` | (510,295)-(545,375) | Hand | **Take:** "It's glued to the counter by its own sticky base. You leave it." |
| | | Magnifier | **Look at:** *"A half-empty bottle of 'Old Rotgut'. The label is peeling, revealing a second label underneath."* |
| | | Mouth | **Smell:** "You uncork it — the fumes strip the inside of your nose. You regret that." |
| `HS_ASH_TRAY` | (440,330)-(480,375) | Hand | **Take:** "You lift it. It's welded shut with dried gum. You set it back with a clunk." |
| | | Magnifier | **Look at:** *"Forty-three butts, all smoked to the filter, all pointing the same direction. Someone was angry."* |
| `HS_SMOKE_HAZE` | (270,130)-(350,200) | Magnifier | **Look at:** *"The haze drifts in slow, lazy spirals—like it's mocking you for breathing."* |
| | | Hand | **Wave (Use):** "You wave it away. It curls back, unbothered." |
| `HS_ALE_RING` | (365,345)-(405,380) | Magnifier | **Look at:** *"A perfect circle of dried foam. The ghost of a hundred pint glasses."* |
| | | Hand | **Scratch (Use):** "You scrape at it with a fingernail. It flakes off, revealing brighter wood beneath." |
| `HS_BUBBLES` | (130,435)-(155,455) | Magnifier | **Look at:** *"Tiny bubbles cling to the side of the puddle. One pops. Then another."* |
| | | Hand | **Pop (Use):** "You press a thumb into a bubble. It bursts with a satisfying *tink*. You feel a small victory." |

---

**Verb Menu (Global):**  
- **Look at** (magnifier icon)  
- **Use** (hand icon, context-sensitive)  
- **Take** (grab icon)  
- **Talk to** (bubble icon — no NPCs present, always returns "You speak to the counter. It does not answer.")  
- **Open** (door icon — available only if facing left/right exits)

---

**Scene Flags (Internal):**  
- `FLAG_PUDDLE_STIRRED` (set after first "Use" on puddle) — changes puddle animation to slower shimmer.  
- `FLAG_WHISKEY_OPENED` (set after "Smell" on bottle) — unlocks a hidden smell-based puzzle hint.  
- `FLAG_RING_SCRATCHED` (set after "Use" on ale ring) — reveals a faint carved initial "M" under the ring.

---

**Exit Regions:**  
- **Left edge** (0, 350-450): walk off-screen to `ROOM_BAR_BOOTHS`.  
- **Right edge** (640, 350-450): walk off-screen to `ROOM_BAR_BACKDOOR`.  
- **Down (no exit):** blocked by the counter—a warning text appears: *"The sticky film holds you back. You can't climb over."*

---

**Occlusion & Z-Order:**  
- Player character draws at z=10 (in front of counter).  
- Counter front edge draws at z=5 (before player).  
- Puddle and bubbles at z=8 (over counter edge, under player's feet when close).  
- Smoke haze at z=15 (floats above everything, except during close-up zoom).

---

**Interaction Cue (Optional):**  
If player stands still facing the counter for 3 seconds, a small caption appears at bottom: *"You hear a distant drip. Your fingers are already sticky."*

### Step 3: Comparison

---

## What the MUD Text Captures That the Scene Spec Misses

### 1. **The *Sensory Invasion* of the Environment**
The MUD text does not merely *describe* the counter—it **violates** the player's senses. "The surface glistens, tacky with a thousand spilled beers"—the word "tacky" is not just a visual property; it's a *tactile* one experienced through the eyes. "A sticky film of dried ale and dust clings to your fingertips"—this is a **proprioceptive intrusion**. The spec gives coordinates and light values, but the MUD makes the grime *happen to you*. It's not "a puddle at (120, 430)"; it's "a puddle of stale brew seeps toward your boots"—the puddle is *active*; it *moves toward you*.

### 2. **The Psychological Weight of Neglect**
The MUD implies **history and decay** without listing it. "The grain is invisible beneath the glaze" (from the spec's Look-at text) is passive—but the MUD's "a thousand spilled beers" implies *repetition*, *carelessness*, *absence of cleaning*. This is not a room; it's a *testament to abandonment*. The spec's "static decal" for the ale ring reduces it to a graphic; the MUD's "ghost of a hundred pint glasses" makes it a **spectral presence**. The MUD text asks: *Who was here? Why did they leave?*

### 3. **The *Soundscape* (Even Without Audio)**
The MUD text includes an **onomatopoeic** hint in the spec's own response ("schlick"), but the MUD goes further: "a soft, wet *schlick* sound"—this is a **phonological trigger**. The spec lists a "bassoon loop" as music, but the MUD creates *diegetic* sound through language: the *drip* in the optional cue, the *pop* of bubbles, the *clunk* of the ashtray. The MUD makes you *hear* the room in your mind's ear; the spec merely annotates an external track.

### 4. **The *Moral/Emotional* Tinge**
The MUD is not neutral. "The air reeks of sour yeast, old smoke, and cheap whiskey"—"cheap" is a **judgment**. "It's glued to the counter by its own sticky base"—this is *disgust* dressed as observation. The spec's "half-empty" bottle is clinical; the MUD's "Old Rotgut" is *leering*. The MUD text has an **attitude**—it's a narrator who has been in this bar too long and is *bitterly amused*. This voice is absent from the spec, which is purely *functional*.

### 5. **The *Micro-Narrative* Embedded in Detail**
The MUD text weaves a **story** through implication: "Forty-three butts, all smoked to the filter, all pointing the same direction. Someone was angry." The spec lists butts as a static object; the MUD turns them into **evidence of a past event**. The spec's "second label underneath" is a puzzle hook; the MUD's "peeling, revealing a second label" is a *mystery*—*what's underneath?* The MUD creates **curiosity through ambiguity**, not through explicit puzzle flags.

---

## What the Scene Spec Captures That the MUD Text Misses

### 1. **The *Parsable Geometry* of Interaction**
The spec provides **exact coordinates** for every hotspot: `(120, 430)` for the puddle, `(510, 295)-(545, 375)` for the bottle. This is *critical* for a game engine. The MUD text is purely textual—it cannot tell the player *where* to click. The spec converts the room into a **spatial database** that the MUD cannot express. Without coordinates, the player would be fumbling blindly through a text parser. The MUD is *atmospheric*; the spec is *navigational*.

### 2. **The *State Machine* and Conditional Logic**
The spec defines **flags** (`FLAG_PUDDLE_STIRRED`, `FLAG_WHISKEY_OPENED`, `FLAG_RING_SCRATCHED`) that change the world *over time*. The MUD text is *static*—it describes a moment, but not how that moment *changes*. The spec's "changes puddle animation to slower shimmer" is a **temporal rule**. The MUD cannot encode "if the player scratches the ring, a carved initial 'M' is revealed" because it has no conditional syntax. The spec is a **program**; the MUD is a **prose poem**.

### 3. **The *Occlusion and Z-Order* (Visual Layering)**
The spec specifies **drawing order**: "Player character draws at z=10", "Counter front edge draws at z=5", "Smoke haze at z=15". This creates *depth*—the player character stands *behind* the counter's front edge but *in front* of the puddle. The MUD text cannot describe this visual hierarchy because it lacks a **spatial axis**. It says "seeps toward your boots" but doesn't tell the renderer *which sprite draws over which*. The spec is the **director of pixels**; the MUD is the **screenplay**.

### 4. **The *Lighting Model* and Color Palette**
The spec provides **quantitative lighting**: "Ambient light: 0.35", "Left side (x<200) is nearly black (0.15 light)", "flickering candle at (610, 110) casts a warm glow over the right third." This is *not* description—it's **render instructions**. The MUD text says "dark-stained oak" but cannot specify *luminance values*. The spec's "256-color, VGA, dark sepia with amber highlights" is a **technical constraint** that ensures the scene looks right on hardware. The MUD is *evocative*; the spec is *deterministic*.

### 5. **The *Walkable Area* and Player Navigation**
The spec defines **walkable rectangles**: "Main floor: (0, 380) to (640, 480)", "Behind counter (blocked)". The MUD text cannot tell the engine *where the player can step*. It says "you cannot climb over," but the spec's "No walkable area" is a **collision mask**. Without this, the player could walk through the counter. The spec also includes an "auto-zoom" trigger at `(300, 400)`—a *camera directive* that the MUD cannot express.

### 6. **The *Exit Regions* and Scene Transitions**
The spec lists **exact exit boundaries**: "Left edge (0, 350-450) → `ROOM_BAR_BOOTHS`", "Right edge (640, 350-450) → `ROOM_BAR_BACKDOOR`." The MUD text only implies exits through atmosphere. The spec provides a **graph of connected spaces**—the MUD cannot tell the engine *which room loads next*.

### 7. **The *Verb Menu* and Context Sensitivity**
The spec defines a **global verb system** (Look, Use, Take, Talk, Open) with specific responses per object. The MUD text embeds *one* response per action, but the spec allows **multiple verbs per hotspot**—e.g., `HS_PUDDLE` has three distinct responses for Magnifier, Hand, and Bottle. The MUD text could describe one action but cannot encode the *branching logic* of "what if the player clicks the puddle with the bottle in inventory?" The spec is a **dialogue tree**; the MUD is a **single line of dialogue**.

---

## Synthesis: The *Division of Labor*

| Aspect | MUD Text (What It Does) | Scene Spec (What It Does) |
|--------|------------------------|---------------------------|
| **Sensory** | Invasive, tactile, olfactory, auditory | Visual only (light, color, positions) |
| **Temporal** | Static moment | State flags, animation loops, conditional reveals |
| **Spatial** | Vague ("toward your boots") | Exact coordinates, walkable areas, z-order |
| **Emotional** | Judgmental, nostalgic, melancholic | Neutral, mechanical |
| **Narrative** | Implies backstory, mystery, character | Provides puzzle hooks but no voice |
| **Engine** | Cannot be parsed by code | Fully parseable, executable |
| **Player** | Engages imagination, immersion | Engages interaction, control |

**In short:** The MUD text is the *soul* of the room—its stench, its grime, its ghosts. The scene spec is the *skeleton*—the joints that let the player move, click, and affect the world. A great game needs both: the spec without the text is a lifeless diagram; the text without the spec is a beautiful poem you cannot enter.

### Step 4: Reconciliation

# Perception Reconciliation Protocol: The Unified Scene Model

## Core Principle
The MUD text and scene spec are **not competing descriptions**—they are **two sensory modalities** of the same reality. The MUD text is the *proprioceptive/emotional* channel; the scene spec is the *geometric/structural* channel. A unified model must **fuse** them, not choose between them.

---

## Perception Check Algorithm

### Step 1: Parse Both Inputs into Structured Ontologies

```
MUD_INPUT_ONTOLOGY:
  - SENSORY_EVENTS: {tactile: [tacky, sticky, clings], 
                     olfactory: [sour, stale, reeks], 
                     auditory: [drip, schlick, pop], 
                     visual: [glistens, dark, amber]}
  - AGENTIC_FORCES: {puddle_moves_toward_player, haze_mocks, 
                     bubbles_pop_spontaneously}
  - EMOTIONAL_TONES: {disgust, curiosity, bitter_amusement, 
                      melancholy, unease}
  - NARRATIVE_IMPLICATIONS: {history_of_neglect, mystery_of_label, 
                             anger_of_smoker, ghost_of_pints}

SCENE_SPEC_ONTOLOGY:
  - GEOMETRY: {object_ids, coordinates, sizes, walkable_areas, 
               z_order, occlusion}
  - LIGHTING: {ambient_intensity, light_sources, color_tint, 
               shadows, gradients}
  - STATE_MACHINE: {flags, conditionals, animation_loops, 
                    triggered_changes}
  - INTERACTION_MATRIX: {hotspots, verb_responses, inventory_checks, 
                         exit_regions}
  - RENDER_DIRECTIVES: {palette, sprites, animation_frames, 
                        camera_behaviors}
```

---

### Step 2: Cross-Modal Binding (The Critical Fusion)

For each object, bind the **geometric anchor** from the spec to the **qualitative descriptor** from the MUD:

| Object | Geometric (Spec) | Qualitative (MUD) | Bound Reality |
|--------|------------------|-------------------|---------------|
| `STALE_BEER_PUDDLE` | `(120, 430), 90x35, z=8, 2-frame shimmer` | "oily pool that reflects nothing," "seeps toward your boots," "tiny bubbles rise and pop with microscopic farts" | A **dynamic entity** at a precise location that: (a) is visually rendered with a 2-frame shimmer at z=8; (b) *behaves aggressively*—it seeps, it reflects nothing, it farts; (c) has *state*—it can be stirred, changing its animation speed |
| `WHISKEY_BOTTLE` | `(520, 300), 25x70, tilted` | "glued to the counter by its own sticky base," "fumes strip the inside of your nose," "label peeling to reveal a second" | A **stubborn, layered object** at coordinates that: (a) cannot be taken (collision/glue logic); (b) has *narrative depth* (two labels = two histories); (c) is *dangerous* to smell (olfactory hazard) |
| `ASH_TRAY` | `(440, 330)-(480, 375), 40x12` | "welded shut with dried gum," "forty-three butts, all smoked to the filter, all pointing the same direction. Someone was angry" | An **immovable artifact of rage** at coordinates that: (a) cannot be lifted (gum-weld logic); (b) encodes a *past human emotion* (anger) through object arrangement; (c) is a *clue* to narrative backstory |
| `DRIED_ALE_RING` | `(365, 345)-(405, 380), 35x35, static decal` | "perfect circle... ghost of a hundred pint glasses," "flakes off, revealing brighter wood and carved initial 'M'" | A **palimpsest** at coordinates that: (a) is visually static but *interactively layered*; (b) hides a secret (initial "M") beneath its surface; (c) requires a *specific action* (scratch) to reveal its depth |

---

### Step 3: Spatial-Epistemic Mapping

Assign each object a **knowledge state** based on its position and lighting:

```
EPISTEMIC_LIGHTING_MODEL:
  - x<200 (near-black, 0.15 light): objects here are PARTIALLY_OBSCURED
    → Player gets less detail; MUD text reveals "something dark and wet"
      but not "tacky with a thousand spilled beers" until closer
    → This creates a PROXIMITY_REVEAL mechanic

  - x=200-480 (dim, 0.35 light): objects are FULLY_PERCEIVED
    → Both text and spec provide complete data
    → This is the DEFAULT_INTERACTION_ZONE

  - x>480 (candle glow, warm): objects are DETAIL_BOOSTED
    → Spec's lighting model allows REFLECTIVE_HIGHLIGHTS
    → MUD text can include "the amber light catches the bottle's 
      edge, revealing a fingerprint you'd otherwise miss"
```

**Rule:** The AI must *gate* textual detail by geometric lighting. A player in the dark left zone should not receive the full "thousand spilled beers" description—they should get a *reduced* version: "You sense something thick and wet at the edge of darkness."

---

### Step 4: Temporal-State Reconciliation

The MUD text describes a **static moment**. The spec describes a **stateful system**. The unified model must resolve this:

```
TEMPORAL_MERGE:
  - Each object has: {static_description (from MUD), 
                      dynamic_states (from spec flags), 
                      state_transitions (from spec logic)}

  - When FLAG_PUDDLE_STIRRED = true:
    → MUD text REPLACES: "You dip a finger in. It comes up coated 
      with something that was beer three days ago."
    → New text: "The puddle is slower now—your stirring broke its 
      surface tension. It seems almost let down."
    → Spec updates: animation loop changes from "2-frame shimmer" 
      to "slower shimmer"
    → UNIFIED: The puddle now has a NEW static description AND a 
      NEW animation frame rate. Both must update together.

  - When FLAG_RING_SCRATCHED = true:
    → MUD text reveals: "flakes off, revealing brighter wood and 
      carved initial 'M'"
    → Spec adds: NEW hotspot `HS_CARVED_M` at (380, 355), size 10x10
    → UNIFIED: A new interactable object is born from a state change. 
      The AI must ADD this to both ontology layers simultaneously.
```

**Critical rule:** State changes must **atomically update both channels**. If the AI updates the spec but not the MUD text, the environment becomes a silent diagram. If it updates the text but not the spec, the world becomes a lying poem.

---

### Step 5: Emotional-Positional Layering

The MUD text has **emotional valence**. The spec has **spatial coordinates**. The unified model must *attach* emotion to geometry:

```
EMOTIONAL_SPATIAL_INDEX:
  - Each coordinate region carries an emotional weight:
    (0-200, 400-480): DREAD (dark, wet, seeping)
    (200-480, 300-400): DISGUST-FASCINATION (sticky, layered, ghostly)
    (480-640, 100-300): HAZARD-CURIOSITY (fumes, peeling labels)

  - When the player interacts with an object:
    → The AI retrieves BOTH the spec's response text AND the MUD's 
      emotional descriptor
    → It CONCATENATES them with a priority rule:
      - If the action is PHYSICAL (Use, Take): spec text first, 
        then MUD's sensory consequence
        Example: "You press your palm flat. [spec: it makes a soft, 
        wet schlick sound] [MUD: you feel the grime—a thousand 
        strangers' evenings against your skin]"

      - If the action is OBSERVATIONAL (Look): MUD text first, 
        then spec's factual data
        Example: "The varnish is gone, replaced by a thousand sticky 
        fingerprints. [MUD: the grain is invisible beneath the 
        glaze—the bar has been dying slowly] [spec: object remains 
        interactive; no state change]"

      - If the action is EXPLORATORY (Smell, Taste): MUD text only, 
        with a spec footnote on consequence
        Example: "The fumes strip the inside of your nose. 
        [MUD: you regret that] [spec: FLAG_WHISKEY_OPENED = true, 
        revealing second label on next Look]"
```

---

### Step 6: Soundscape Synthesis

The spec

### Step 5: What's missed

# The Irreducible Gap: What Each Modality Cannot Carry

---

## What an AI Agent Misses Reading Only the MUD Text

### 1. **The Geometry of Action (Spatial Coordinates)**
The MUD text says "a puddle of stale brew seeps toward your boots." The AI knows *that* the puddle exists, but not *where* it is. Is it left? Right? At arm's reach? Can the player step over it or must they walk around? The AI cannot compute:
- Pathfinding (is the puddle an obstacle or a floor decal?)
- Reachability (can the player lean over and touch it without moving?)
- Relative positioning (is it near the ashtray? The bottle? The exit?)

The MUD lacks a **coordinate system**. The AI would be a blind navigator in a room it can describe perfectly but cannot traverse.

### 2. **The Physics of the Space (Collision & Occlusion)**
The MUD says "The sticky film holds you back. You can't climb over." But the AI cannot model *why*—is it a height barrier? A material property? A psychological block? The spec's **walkable area rectangles** and **z-order** give the AI actual physics:
- The player character draws at z=10, *in front of* the counter edge (z=5) but *behind* the smoke haze (z=15).
- The puddle (z=8) is *under* the player's feet when close.
- The counter's front edge is a *collision mask* that stops horizontal movement.

An AI with only the MUD text would try to walk through the counter or click on objects that are visually obscured. It would have no **spatial reasoning**.

### 3. **The Temporal State Machine (Flags & Conditionals)**
The MUD text describes a *single moment*. It doesn't say:
- "If the player stirs the puddle, its animation slows."
- "If the player scratches the ring, a hidden initial 'M' is revealed."
- "If the player smells the whiskey, a new puzzle hint unlocks."

An AI that only reads the MUD text experiences a **static world**. It cannot predict consequences, track state changes, or understand that *its actions have lasting effects*. The spec's flags (`FLAG_PUDDLE_STIRRED`, `FLAG_RING_SCRATCHED`) are a **causal model**—the MUD text is a **snapshot**.

### 4. **The Graphical Rendering Model (Lighting, Color, Animation)**
The MUD says "dark-stained oak" and "amber highlights." But it cannot tell the AI:
- The ambient light level is 0.35 (dim), dropping to 0.15 on the left side.
- The candle at (610, 110) creates a warm glow over the right third.
- The puddle has a 2-frame shimmer animation; the smoke has an 8-frame loop.
- The palette is 256-color VGA sepia with amber highlights.

An AI that only reads the MUD text would not know how to **render** the scene. It would describe the room beautifully but could not produce a single pixel. The spec is a **drawing instruction set**.

### 5. **The Interaction Verb Matrix (Context Sensitivity)**
The MUD text offers a few sample responses, but the spec defines a **full interaction matrix**:
- Each hotspot has *multiple* verb responses (Look, Use, Take, Smell, Taste).
- Some responses depend on *inventory state* ("if the player pours from the bottle into the puddle…").
- Some objects are *context-sensitive* (the ashtray is "welded shut" for Take, but the player can still Look at it).

An AI with only the MUD text would not know how to handle *arbitrary player inputs*. The spec is a **dialogue tree**; the MUD text is a **single branch**.

---

## What a Human Misses Seeing Only the Scene (The Static Image)

### 1. **The Olfactory and Gustatory Layers**
The scene spec describes *visual* properties—color, lighting, position. But the human looking at the rendered scene would not know:
- The air "reeks of sour yeast, old smoke, and cheap whiskey."
- The surface is "tacky with a thousand spilled beers."
- The whiskey bottle's fumes "strip the inside of your nose."

The MUD text provides **non-visual senses**—smell, taste, texture. The image alone is a *silent tableau*. Without the text, the human sees a dirty bar but does not *smell* it.

### 2. **The Emotional and Judgmental Tone**
The scene spec is neutral: "Cheap whiskey bottle, tilted, half-empty." But the MUD says "Old Rotgut" and describes the label as "peeling, revealing a second label underneath." The human viewing only the image would not know:
- The narrator's *bitter amusement* (the bar is a character, not a backdrop).
- The *melancholy* of "a ghost of a hundred pint glasses."
- The *disgust* of "a sticky film of dried ale and dust clings to your fingertips."

The MUD text provides **voice**. The image alone is *documentary*; the text makes it *literary*.

### 3. **The Narrative Implications (Backstory & Mystery)**
The rendered scene shows an ashtray full of butts. The human sees "forty-three butts" but does not know *they all point the same direction*, or that *someone was angry*. The ale ring is a stain, not "the ghost of a hundred pint glasses." The bottle is a prop, not a *mystery* with a hidden second label.

The MUD text provides **story**. The image alone is *setting*; the text makes it *plot*.

### 4. **The Temporal Dynamics (What Happens Next)**
The scene spec lists animation frames, but a static screenshot cannot show:
- The puddle's *shimmer* (2-frame loop).
- The smoke's *drift* (8-frame loop).
- The bubbles *popping* (3-frame loop with occasional burst).
- The candle's *flicker*.

The MUD text describes these as *events*: "Tiny bubbles rise and pop with microscopic farts." The human seeing only a still image misses the **liveliness** of the room—it is not a photograph, but a *movie*.

### 5. **The Interpretive Ambiguity (What Does It Mean?)**
A human seeing the scene might think: "This is a dirty bar." But the MUD text reframes it: "This is a *threshold*—the player is about to uncover a mystery (the carved 'M', the second label, the angry smoker)." The text provides **semantic depth** that the image cannot. Without it, the human sees *grime*; with it, they see *clues*.

---

## The Irreducible Gap: What Neither Modality Alone Can Carry

### The Gap is **Intentionality**.

The MUD text carries **intent**—the narrator's attitude, the world's dark humor, the invitation to *feel* disgust and curiosity. But it cannot tell you *where to click*.

The scene spec carries **structure**—the exact coordinates, the state flags, the walkable areas. But it cannot tell you *why you care*.

### Neither can answer: **"What should the player do next?"**

- The MUD text says: *"The varnish is gone, replaced by a thousand sticky fingerprints."* — But does the player *act* on this? Should they look closer? Touch? Taste? The text doesn't say.

- The scene spec says: *"HS_COUNTER_TOP: (0,380)-(640,395), Magnifier → 'The varnish is gone…'"* — But *why* does this matter? The spec has no **motivation** for the player.

### The Unified Model Must Generate **Intentional Guidance**:

```
SYNTHESIS_RULE:
  - When the player looks at an object:
    → Retrieve the MUD's emotional descriptor (to create *desire*).
    → Retrieve the spec's interaction options (to create *possibility*).
    → Present BOTH in a way that implies a *next action*.

  Example:
    "The varnish is gone, replaced by a thousand sticky fingerprints. 
     The grain is invisible beneath the glaze. 
     [You could press your palm flat. You could scrape at the ring. 
      You could walk away. The bar waits.]"

  This is neither pure text nor pure spec—it is a **third thing**: 
  a *prompt* that carries both atmosphere and agency.
```

---

## Conclusion: The Gap is **Generative**

The MUD text and scene spec are not halves of a whole—they are **two different species** that reproduce only when crossed.

- The MUD text is **prose**—it creates *emotion, memory, desire*.
- The scene spec is **code**—it creates *geometry, physics, causality*.

An AI that reads only the text writes poetry but cannot act.  
A human that sees only the scene navigates space but cannot feel.  



---

## Room: Wheelhouse

*a wheelhouse with old brass instruments and a cracked windshield*

### Step 1: MUD text

You are in the wheelhouse of the derelict vessel.  
A cracked windshield webs a spider's maze across the dark horizon.  
A dented brass sextant and a coiled horn rest on a rusted binnacle.  
The air smells of salt, stale oil, and old polish.  
Exits: forward deck, captain's cabin, below deck.

### Step 2: ScummVM scene spec

**SCUMMVM Scene Specification: DERELICT VESSEL — WHEELHOUSE**  
**Scene ID:** `WHEELHOUSE_01`  
**Palette:** Desaturated blue-grays, rusted amber, mud-green shadow.  
**Ambient Lighting:** Cold, diffused daylight from the cracked windshield (strongest at center-top), with a faint swaying shadow cast by the dangling horn when the ship groans. No active light sources.  
**Audio Loop:** Low wind hum through glass crack, occasional creak of hull timbers, distant gull cries.  

---

### OBJECTS (Layer: Foreground/Midground/Background)

1. **Windshield (Cracked)**  
   - **Screen Position:** (320, 140) — spans x=80..560, y=60..220  
   - **Layer:** Background  
   - **State:** Static crack pattern with subtle reflection glint.  
   - **Hotspot Polygon:** Irregular octagon covering glass area.  
   - **Verbs:**  
     - **Look at:** *"A spider's maze of fractures — each line points to a different drowned star."*  
     - **Push/Pull:** *"You press a palm flat. The glass gives a low, mournful hum. It holds firm."*  
     - **Use** (with any object): *"The cracks seem to deepen for a moment, but nothing else changes."*  

2. **Brass Sextant**  
   - **Screen Position:** (180, 300) — resting on binnacle, angled slightly left  
   - **Layer:** Midground  
   - **Hotspot:** Ellipse (150..210, 285..330) plus small arc for the sighting arm.  
   - **Verbs:**  
     - **Look at:** *"The sextant's mirror is tarnished, but the arc still reads true. The index bar is frozen at 47°."*  
     - **Take:** *"It's bolted fast to the binnacle. A brass plate reads: 'FOR MEASURING THE UNMEASURED.'"*  
     - **Use** (with horn): *"You lift the horn's mouth to the sextant's eyepiece — the brass rings with a single clear note. Nothing else happens."*  
     - **Use** (with any other object): *"The sextant stays stubbornly fixed in place."*  

3. **Coiled Horn (Era of Steam)**  
   - **Screen Position:** (420, 310) — atop binnacle, coiled leather and brass, mouthpiece facing left  
   - **Layer:** Foreground  
   - **Hotspot:** Two overlapping circles — one for the coil, one for the mouthpiece.  
   - **Verbs:**  
     - **Look at:** *"A steam whistle horn, its leather cracked and stiff. The brass rim has a faded ship's crest."*  
     - **Take:** *"It's tied to the binnacle with a thin, rotted cord — it snaps free in your hand."* (Object added to inventory).  
     - **Use** (after taken): *"You blow into it — a low, long wail that fades into the wind. The ship seems to lean slightly."*  
     - **Use** (with sextant): *"See Sextant - Use."*  

4. **Rusted Binnacle (Base)**  
   - **Screen Position:** (300, 390) — pedestal at center-bottom  
   - **Layer:** Foreground  
   - **Hotspot:** Large rectangle (260..340, 360..430) with small latch detail at front.  
   - **Verbs:**  
     - **Look at:** *"A compass binnacle, its brass casing pitted and green. The gimbal swings lazily, but the compass card is gone."*  
     - **Open:** *"The front panel creaks open. Inside: a dry, empty socket where a lens once sat — and a scrap of paper."*  
     - **Take** (paper): *"The paper is water-stained. It reads: 'THE HORN CALLS THE SEXTANT'S ANGLE — THEN FACE THE MAZE.'"*  
     - **Close:** *"You shut the panel; it clicks with a hollow sound."*  

5. **Ship's Wheel (Background, left-side prop)**  
   - **Screen Position:** (90, 250) — partially visible behind binnacle  
   - **Layer:** Midground  
   - **Hotspot:** Small circle for the hub, plus two spoke tips.  
   - **Verbs:**  
     - **Look at:** *"The wheel is lashed with frayed rope. The spokes are worn smooth by countless hands."*  
     - **Turn:** *"The wheel gives a few inches, then jams — the rudder is likely fouled below."*  
     - **Use** (with horn): *"The horn's note makes the wheel shiver, but it won't turn further."*  

---

### WALKABLE AREAS  
- **Floor Polygon:** x=0..640, y=400..480 (a rough trapezoid, slightly narrower at bottom to simulate perspective).  
- **Walkable Zone:** All of the above polygon is walkable.  
- **Blocked Areas:**  
  - The binnacle (center, x=250..350, y=350..400) — impassable.  
  - The windshield ledge (y<220) — not walkable.  
  - The left wheel (x<130, y<330) — clipped.  

---

### SCENE TRANSITIONS  
- **Forward deck:** Walk to right edge (x>600, y~420) → crossfade to `DECK_FORWARD`.  
- **Captain's cabin:** Walk to left edge (x<20, y~410) → door cut-scene → `CABIN_CAPTAIN`.  
- **Below deck:** Walk to bottom-center (x=320, y>460) → hatch ladder → `LOWER_HOLD`.  

---

### INTERACTION NOTES  
- **Cursor Change:** Over the sextant, horn, and binnacle latch, cursor becomes a small brass gear.  
- **Global Flag:** After horn is taken, the scene's ambient audio gains a faint, persistent hum (the ship's "awake" state).  
- **Subtitles:** All `Look at` text displays in a parchment-style box, bottom-center.  

**End of specification.**

### Step 3: Comparison

The MUD text and the scene spec are two radically different tools for two radically different purposes. The MUD text is **atmospheric prose**—it paints a mood and relies on the player's imagination to fill in geometry. The scene spec is **interactive engineering**—it dictates precise coordinates, hitboxes, and reactive logic for a graphical engine.

Here is a specific and thorough comparison of what each captures that the other misses.

---

## What the MUD Text Captures That the Scene Spec Misses

### 1. **A Sense of Metaphor and Narrative Weight**
The MUD text is not just descriptive; it is *poetic*. 
- *"A spider's maze of fractures — each line points to a different drowned star."* — This turns a mundane cracked windshield into a meaningful, almost cosmic artifact. It implies a backstory (a ship lost at sea, stars "drowned") and sets a tone of melancholy.
- The scene spec's version of the same object is purely functional: *"crack pattern with subtle reflection glint"* and a verb response that describes the glass humming. The spec never tells the player *why* the cracks matter emotionally.

### 2. **Sensory Synesthesia and Abstract Details**
The MUD text blends senses: *"The air smells of salt, stale oil, and old polish."* This is a specific, layered olfactory portrait. The scene spec mentions "desaturated blue-grays" and "rusted amber" but never touches smell, touch, or the *weight* of the air. The spec’s audio loop mentions wind, creaks, and gulls, but it lacks the *olfactory* dimension entirely.

### 3. **The Illusion of Depth and Mystery**
The MUD text gives the player *room to wonder*. The sextant is "frozen at 47°" — why? The compass card is "gone" — what happened? The horn's mouthpiece faces left, but the MUD text doesn't tell you that; it just makes the object *feel* significant. The scene spec, by contrast, *answers* those questions with explicit verb text: *"The paper reads: 'THE HORN CALLS THE SEXTANT'S ANGLE — THEN FACE THE MAZE.'"* That is a direct puzzle hint, not a mysterious fragment. The MUD text leaves the mystery intact; the spec resolves it.

### 4. **A Specific, Unrepeatable Mood**
The MUD text is written in a voice—it's a narrator with a perspective. The scene spec is a dispassionate technical document. The MUD text captures the *feeling* of being in that room: lonely, haunted, and charged with potential. The spec captures the *layout* of that room but not its soul.

---

## What the Scene Spec Captures That the MUD Text Misses

### 1. **Exact Spatial Geometry**
The MUD text gives no coordinates. It doesn't tell you the windshield spans x=80..560, y=60..220, or that the binnacle is at (300, 390) and blocks movement. The spec provides a **walkable polygon** (x=0..640, y=400..480), **blocked areas** (the binnacle, the windshield ledge), and **hotspot polygons** (octagons, ellipses, rectangles). This is essential for a graphical adventure—the engine needs to know *where* the player can click and *where* the player can stand. The MUD text is blind to this.

### 2. **Layered Rendering and Perspective**
The spec explicitly assigns each object to a **layer**: foreground (horn), midground (sextant, wheel), background (windshield). This is critical for a 2D scene—it determines draw order and depth sorting. The MUD text has no concept of z-ordering or parallax. The spec also notes that the ship's wheel is "partially visible behind binnacle" and that the windshield is "strongest at center-top" for lighting—these are visual composition details that a text parser cannot convey.

### 3. **Dynamic State and Verb Logic**
The MUD text is static—it describes the room once. The spec, however, tracks **global flags** (e.g., "After horn is taken, the scene's ambient audio gains a faint, persistent hum") and defines **conditional verb responses**:
- The horn's "Use" behavior changes after it's taken.
- The binnacle has *sequential* states: look → open → take paper → close.
- The cursor changes to a "small brass gear" over interactive objects.
The MUD text has no mechanism for this—it can't express "if the player has item X, then this hotspot becomes active" or "after this action, play a new sound loop." The spec is a state machine; the MUD text is a snapshot.

### 4. **Exact Audio and Lighting Cues**
The spec provides precise audio instructions: "low wind hum through glass crack," "occasional creak of hull timbers," "distant gull cries." It also specifies lighting direction and intensity: "Cold, diffused daylight from the cracked windshield (strongest at center-top)" and "a faint swaying shadow cast by the dangling horn." The MUD text mentions the wind and the smell, but it cannot specify *where* the light comes from or *how* the shadow moves. The spec is a technical blueprint for a game engine; the MUD text is a literary impression.

### 5. **Player-Action Consequences and Puzzle Logic**
The spec is explicit about *what the player can do* and *what happens next*:
- Taking the horn breaks a "thin, rotted cord."
- Using the horn on the sextant produces "a single clear note."
- The paper in the binnacle is a **direct hint** for a puzzle sequence.
The MUD text never tells you that you can take the horn, open the binnacle, or read a note. It only presents the room's *static appearance*. The MUD text is a *description*; the spec is a *game design document*.

---

## The Core Difference

| Aspect | MUD Text | Scene Spec |
|--------|----------|------------|
| **Purpose** | Immersion & mood | Functionality & logic |
| **Information** | Sensory, metaphorical | Geometric, conditional |
| **Temporality** | One moment in time | Dynamic, state-based |
| **Player** | Passive observer | Active agent |
| **Style** | Literary prose | Technical documentation |

The MUD text captures the **poetry of place**—the why, the emotion, the mystery. The scene spec captures the **physics of place**—the where, the how, the what-happens-next. A great adventure game needs both: the spec to make the room *work*, and the MUD text to make the room *matter*.

### Step 4: Reconciliation

Here is the perception check you requested — a unified method that merges the MUD text and the scene specification into a single coherent world model.

---

# PERCEPTION CHECK: WHEELHOUSE_01 — UNIFIED WORLD MODEL

**Method Name:** *Dual-Channel Scene Fusion via Semantic Anchoring*

---

## 1. INPUT STREAMS

### Channel A — Text Prose (MUD)
- **Format:** Free-form narrative, sensory, metaphorical
- **Provides:** Mood, significance, narrative weight, olfactory/tactile cues
- **Example:** *"A spider's maze of fractures — each line points to a different drowned star."*

### Channel B — Scene Specification (SCUMMVM)
- **Format:** Structured data — coordinates, polygons, layers, verb logic
- **Provides:** Geometry, interactivity, state transitions, audio/lighting cues
- **Example:** `Windshield: Polygon (80,60,560,220), Layer=Background`

---

## 2. FUSION PIPELINE (Five Stages)

### Stage 1 — Object Identification & Correspondence
**Goal:** Map prose entities to spec entities.

```
For each noun in the MUD text:
  Match to nearest spec object by semantic similarity (name, position, description).
  If no direct match → flag as "ambient/atmospheric" (not interactive).

Example:
  "spider's maze of fractures" → Windshield (spec)
  "brass sextant" → Brass Sextant (spec)
  "coiled horn" → Coiled Horn (spec)
  "smells of salt, stale oil" → Ambient scent (no spec object → tagged 'atmosphere')
```

**Result:** A **correspondence table** linking each prose-referenced item to its spatial/interactive counterpart.

---

### Stage 2 — Spatial Anchoring
**Goal:** Assign each fused object a **position, layer, and walkability** in a single unified coordinate space.

```
Unified Space: 640x480 canvas.
Each entity receives:
  - Spec geometry (x, y, polygon)
  - Spec layer (foreground/midground/background)
  - Spec interaction flag (hotspot: yes/no)

Prose-only elements (smell, mood) are anchored to the *scene centroid* (320, 240)
  or to the object they most relate to.
  Example: "stale oil" → anchored to Binnacle (source of mechanical smell)
```

**Result:** A **spatial scene graph** — every object has coordinates, depth, and a prose tag.

---

### Stage 3 — State Initialization & Conditional Enrichment
**Goal:** Merge static prose with dynamic spec logic.

```
Initialize:
  - All spec states active (e.g., horn tied, compass missing, paper inside binnacle)
  - Prose descriptions attached to each object as "narrative layer"

Conditional Logic:
  - If horn is taken → prose description of horn updates:
      Old prose: "hands cracked and stiff"
      New prose: "it hangs loose in your grip — lighter than expected"
    This is a *prose-state bridge* generated from the spec's state machine.

  - If binnacle opened → prose text for binnacle changes:
      Old: "gimbal swings lazily"
      New: "the empty socket yawns; the paper trembles slightly"
```

**Result:** A **state-aware narrative engine** — prose evolves with puzzle logic.

---

### Stage 4 — Sensory Wholeness Assembly
**Goal:** Combine spec's physical cues with prose's sensory cues into a unified **perceptual snapshot**.

```
Perceptual Snapshot Structure:
{
  "visual": {
    "lighting": "cold diffused daylight, strongest at top-center",
    "palette": ["desaturated blue-gray", "rusted amber", "mud-green"],
    "objects": [ {name, position, layer, appearance_prose} ]
  },
  "audio": {
    "loop": "low wind hum through glass crack",
    "events": ["occasional hull creak", "distant gull"],
    "conditional": "if horn taken → faint persistent hum added"
  },
  "olfactory": {
    "salt", "stale oil", "old polish"  (from prose, anchored to scene)
  },
  "tactile": {
    "cracked glass hums under palm",
    "horn's cord rotted — snaps easily",
    "wheel spokes worn smooth"
  },
  "atmosphere": {
    "lonely, haunted, charged with potential" (prose-derived)
  }
}
```

**Result:** A **full-sensory model** — not just geometry + text, but *felt space*.

---

### Stage 5 — Action Reasoning & Coherent Response
**Goal:** Unify verb logic (spec) with narrative consequence (prose) into a single action-response engine.

```
Action: LOOK AT sextant
  Spec response: "The mirror is tarnished; index bar frozen at 47°"
  Prose resonance: "For measuring the unmeasured" — bolted fast, mystery preserved.
  Fused output: "The sextant's mirror is tarnished, but the arc still reads true.
                 The index bar is frozen at 47° — for measuring the unmeasured."

Action: TAKE horn
  Spec: Cord snaps. Object added to inventory.
  Prose update: The ship leans slightly — as if it notices the horn is gone.
  Fused output: "The rotted cord snaps free. As you lift the horn,
                 the ship gives a low, long groan — it knows you have it."

Action: USE horn on sextant
  Spec: "A single clear note. Nothing else happens."
  Prose update: "The note rings like a question, unanswered."
  Fused output: "You lift the horn's mouth to the sextant's eyepiece —
                 a single clear note rings through the glass.
                 It sounds like a question. The ship holds its breath."
```

**Result:** A **unified action interpreter** — every player action yields both mechanical result and narrative texture.

---

## 3. OUTPUT: UNIFIED WORLD MODEL

```
WORLD_MODEL: WHEELHOUSE_01
├── Mood Vector: [lonely, haunted, charged, mechanical, maritime]
├── Spatial Graph:
│   ├── Windshield: (320,140)[BG] - cracked, humming, cosmic metaphor
│   ├── Wheel: (90,250)[MG] - lashed, jammed, worn smooth
│   ├── Sextant: (180,300)[MG] - fixed at 47°, bolted, "unmeasured"
│   ├── Horn: (420,310)[FG] - coil + mouthpiece, tied, rotted, awake
│   ├── Binnacle: (300,390)[FG] - empty socket, hidden paper, gimbal
│   └── Floor: (0,400→640,480) - walkable, limited by furniture
├── State Flags:
│   ├── HORN_TAKEN: false
│   ├── BINNACLE_OPEN: false
│   ├── PAPER_TAKEN: false
│   └── SHIP_AWAKE: false
├── Sensory Streams:
│   ├── Visual: cold light, desaturated palette, swaying horn shadow
│   ├── Audio: wind hum, creak, gulls (+ hum if awake)
│   ├── Olfactory: salt, stale oil, old polish
│   └── Tactile: glass hum, rotted cord, worn wheel
├── Narrative Threads:
│   ├── "For measuring the unmeasured"
│   ├── "The horn calls the sextant's angle — then face the maze"
│   └── "Each line points to a different drowned star"
└── Inference Engine: Every action checked against both spec logic
                     and prose resonance; output always dual-layered.
```

---

## 4. KEY INSIGHT

The MUD text and SCUMMVM spec are not competing descriptions — they are **complementary hemispheres** of a single cognitive model:

- **Text** = *semantic cortex* (meaning, mood, metaphor)
- **Spec** = *sensorimotor cortex* (space, state, action)

The perception check fuses them by:

1. **Anchoring** prose to geometry
2. **Binding** narrative to state
3. **Layering** sensory cues into one perceptual snapshot
4. **Fusing** responses so every action feels both *functional* and *meaningful*

This creates a **coherent world** — one that is not just a puzzle grid, and not just a poem, but a *place* the player inhabits, touches, and remembers.

---

**End of Perception Check.**

### Step 5: What's missed

# The Irreducible Gap

---

## What an AI Agent MISSES (With Only MUD Text)

### 1. **The Physics of Navigation**
The MUD text never tells you:
- Where you *can* walk (the floor polygon is x=0..640, y=400..480)
- What *blocks* you (the binnacle at center, the windshield ledge at y<220)
- How to *reach* the exits (right edge → forward deck, bottom-center → below deck)

An AI agent reading only prose would be **lost in space** — it would know *what* the room is, but not *how to move through it*. It might try to walk through the windshield or into the wall, because nothing in the text constrains its geometry.

### 2. **The State Logic**
The MUD text is static — it describes one frozen moment. An AI agent would not know:
- That taking the horn is *possible* (the text never says it can be picked up)
- That the binnacle *opens* (the text never mentions a latch)
- That the paper inside is a *clue* ("THE HORN CALLS THE SEXTANT'S ANGLE — THEN FACE THE MAZE")
- That the horn's presence *changes* the ship's audio state (the "awake" hum)

The agent would treat the room as a **still life** rather than a **system of affordances**.

### 3. **The Conditional Responses**
The text gives one description per object. But the spec knows:
- The horn's description changes *after* it's taken
- The binnacle's description changes *after* it's opened
- The cursor changes to a gear over interactive objects
- The audio mutates if the horn is removed

An agent with only prose would not understand **causality** — it would not know that actions have *consequences* beyond the immediate response.

### 4. **The Visual Composition**
The prose mentions a sextant, a horn, a binnacle — but never *where* they are relative to each other. An AI agent would not know:
- The horn is *on top* of the binnacle (foreground over midground)
- The sextant is to the *left* (180, 300)
- The wheel is *behind* the binnacle (partial occlusion)
- The windshield is *high* (y=60..220) — a background element

Without this, the agent cannot reason about **spatial relationships** — whether an object is reachable, whether something is hidden behind something else, whether the scene has depth.

### 5. **The Puzzle Structure**
The prose mentions a sextant "frozen at 47°" and a horn — but never states they are *linked*. The spec's paper clue is a **direct connector**: "THE HORN CALLS THE SEXTANT'S ANGLE — THEN FACE THE MAZE." An AI agent with only prose would see two unrelated objects; the spec reveals they are **nodes in a puzzle graph**.

---

## What a HUMAN MISSES (With Only the Scene)

### 1. **The Narrative Weight**
The scene shows a cracked windshield, a brass sextant, a coiled horn. A human sees *objects*. But the prose tells them:
- The cracks are "a spider's maze pointing to drowned stars" — this is *metaphor*, not geometry
- The sextant is "for measuring the unmeasured" — this is *poetry*, not function
- The horn's note "sounds like a question" — this is *significance*, not audio data

Without the text, a human would see a **prop room** — functional, not meaningful. The objects would be *tools for a puzzle*, not *artifacts of a story*.

### 2. **The Sensory Dimensions**
The scene spec covers visual (palette, lighting) and audio (wind, creaks, gulls). But it never mentions:
- **Smell**: "salt, stale oil, old polish"
- **Touch**: "the glass hums under your palm," "the cord snaps free"
- **Temperature/Weight**: the cold air, the heaviness of the horn

A human looking at the scene would see and hear — but not *feel*. The prose engages the full sensorium, making the room **inhabited**, not just *viewed*.

### 3. **The Emotional Register**
The spec is emotionally neutral — it describes a room. The prose tells you how the room *feels*:
- Lonely ("drowned stars," "lost at sea")
- Haunted (the ship "leans slightly" when the horn is taken)
- Charged with potential ("each line points to a different drowned star")

A human would see a **derelict ship interior**. The prose makes it a **grave and a promise**.

### 4. **The Unspoken Backstory**
The spec gives you a paper clue — a direct puzzle hint. But the prose implies *more*:
- Why is the sextant frozen at 47°? (prose suggests a specific, now-lost calculation)
- Why is the compass card gone? (the prose's "for measuring the unmeasured" hints at a deliberate removal)
- Who tied the horn to the binnacle, and why?

A human sees a **state** — the prose suggests a **history**.

### 5. **The Lingering Mystery**
The spec resolves the puzzle: "THE HORN CALLS THE SEXTANT'S ANGLE — THEN FACE THE MAZE." This is a *solution hint*. The prose leaves it open: "each line points to a different drowned star" — this is *unresolvable metaphor*. A human with only the scene would not *wonder*; they would *know*. The prose preserves the **mystery** that the spec would dispel.

---

## The Irreducible Gap

| Dimension | MUD Text (Alone) | Scene Spec (Alone) | Irreducible Gap |
|-----------|------------------|--------------------|------------------|
| **Space** | No coordinates | Exact geometry | *How to navigate* |
| **Time** | Static moment | State machine | *How things change* |
| **Meaning** | Deep, ambiguous | Functional, explicit | *Why it matters* |
| **Senses** | Full sensory (smell, touch) | Visual + audio only | *The felt experience* |
| **Emotion** | Lonely, haunted, charged | Neutral engineering | *The mood* |
| **Mystery** | Preserved | Resolved | *The unknown* |
| **Causality** | None | Fully specified | *Action → consequence* |
| **History** | Implied | Absent | *Backstory* |

---

## The Core Truth

**The MUD text and the scene spec are not two views of the same thing — they are two different *worlds*.**

- The **spec** is a world of *physics* — spatial, mechanical, logical. It answers *how*.
- The **text** is a world of *metaphysics* — meaningful, emotional, ambiguous. It answers *why*.

**The irreducible gap is this:**

> **The text knows what the room *means*. The spec knows what the room *does*. Neither alone knows what the room *is*.**

A game is not a description of a place, nor a map of a place. It is the **experience** of being in a place — and that experience requires *both* the physical grounding of the spec and the narrative resonance of the text. 

**The gap between them is the gap between *knowing* and *feeling*. A complete game bridges it. A complete AI must too.**

---

## Room: Engine Room

*an engine room with diesel engines, pipes, and the smell of oil*

### Step 1: MUD text

You are in the ENGINE ROOM. The thrum of two massive DIESEL ENGINES vibrates through the deck plates, a low, constant growl that you feel in your chest.  
Pipes of every size—greasy, sweating with condensation—crisscross the low ceiling and snake down the bulkheads, hissing and knocking with hot pressure.  
The air is thick, humid, and heavy with the acrid, metallic smell of oil and diesel fuel, coating your tongue and stinging your nostrils.  
A maze of catwalks and ladders descends into a shadowed pit, where the engine block's oily, blackened pistons slam up and down in a blur of motion.  
A pressure gauge on the main manifold trembles violently, its needle quivering in the red zone, and a loose pipe coupling drips a steady, dark rhythm onto the grating.

### Step 2: ScummVM scene spec

[SCUMM SCENE: ENGINE_ROOM]
[ROOM_WIDTH=640]
[ROOM_HEIGHT=480]
[BACKGROUND_IMAGE="engine_room_bg.png"]

[LIGHTING]
  [AMBIENT_LIGHT=0.25]                   ; Dim, oppressive gloom
  [LOCAL_LIGHTS]
    {source="grime_lamp", x=80, y=60, radius=120, intensity=0.6, color=(200,180,120)}   ; Flickering overhead bulb, sickly yellow
    {source="gauge_glow", x=420, y=130, radius=40, intensity=0.8, color=(180,80,50)}    ; Red-hot pressure gauge
    {source="piston_flash", x=320, y=380, radius=90, intensity=0.5, color=(150,150,200)} ; Reflected light off moving steel
  [SHADOW_MAP="engine_shadows.png"]

[WALKABLE_AREAS]
  ; Rectangles in screen coordinates (x1, y1, x2, y2)
  {id="upper_catwalk", rect=(50, 80, 590, 160)}    ; Narrow metal grate walkway
  {id="mid_platform", rect=(40, 200, 600, 280)}    ; Main maintenance deck
  {id="lower_pit_edge", rect=(20, 300, 620, 420)}  ; Dangerously close to pistons
  {id="ladder_path", rect=(560, 100, 620, 420)}    ; Vertical climb area leading down

[OBJECTS]
  ; --- Main Engine Block ---
  {id="engine_block", name="MASSIVE DIESEL ENGINE",
   x=320, y=380, w=280, h=120,
   hotspot={box=(180, 240, 460, 420)},
   verbs={
     LOOK="The massive block shudders with each stroke. Caution: do not touch moving parts."
     USE="You feel the vibration through your boots. It's warm, alive, and dangerous."
     PUSH="You push against the housing. It doesn't budge. The bolts are seized with rust."
     PULL="You pull a greasy lever. The engine's pitch rises dangerously for a second."
     TALK="You shout over the din. The engine replies with a deafening knock."
   },
   state="running"}

  ; --- Steam Pipe Cluster (overhead) ---
  {id="pipe_cluster", name="CLUSTER OF GREASY PIPES",
   x=100, y=40, w=180, h=30,
   hotspot={box=(20, 30, 280, 70)},
   verbs={
     LOOK="Condensation drips rhythmically. One coupling is weeping black oil."
     USE="You touch a pipe — it's scalding hot. You pull your hand back."
     HEAT="It hisses violently. Steam escapes from a crack you hadn't noticed."
     REPAIR="You tighten the loose coupling with a wrench. The drip slows."
   },
   state="leaky"}

  ; --- Pressure Gauge (trembling) ---
  {id="pressure_gauge", name="TREMBLING PRESSURE GAUGE",
   x=430, y=110, w=40, h=40,
   hotspot={box=(410, 90, 470, 150)},
   verbs={
     LOOK="The needle quivers in the red zone. It's about to blow."
     READ="Pressure reads 120 PSI — far above safe operating limits."
     TURN="You twist the valve. The needle flickers but doesn't move."
     USE="You tap the glass. It rattles ominously."
   },
   state="danger"}

  ; --- Leaking Coupling (on floor) ---
  {id="leaky_coupling", name="LEAKING PIPE COUPLING",
   x=520, y=300, w=30, h=20,
   hotspot={box=(500, 290, 560, 330)},
   verbs={
     LOOK="A steady drip of dark oil forms a puddle on the grating."
     USE="Your fingers come away black and slick."
     TURN="You twist it shut. The dripping stops, but the pressure builds."
     REPAIR="With a rag and a wrench, you cinch it tight. The leak seals."
   },
   state="dripping"}

  ; --- Catwalk Ladder (to lower deck) ---
  {id="ladder", name="RUSTED LADDER",
   x=590, y=160, w=30, h=260,
   hotspot={box=(575, 150, 625, 420)},
   verbs={
     LOOK="It descends into a shadowed pit where pistons slam below."
     CLIMB="You grip the greasy rungs and climb down carefully."
     USE="You descend into the gloom. The heat intensifies."
     EXIT="You climb back up to the main deck."
   },
   state="accessible"}

  ; --- Oil Drum (corner) ---
  {id="oil_drum", name="RUSTY OIL DRUM",
   x=60, y=260, w=40, h=50,
   hotspot={box=(40, 250, 100, 320)},
   verbs={
     LOOK="A dented barrel, lid ajar, filled with thick black sludge."
     USE="You dip a finger in — it's cold and viscous."
     OPEN="You pry the lid. The smell hits you like a wave."
     TALK="You ask it for advice. It offers none, but it's a good listener."
   },
   state="full"}

  ; --- Overhead Emergency Light (flickering) ---
  {id="emergency_light", name="FLICKERING OVERHEAD LIGHT",
   x=80, y=60, w=20, h=15,
   hotspot={box=(70, 50, 100, 75)},
   verbs={
     LOOK="It buzzes and stutters, casting sickly yellow pools of light."
     USE="You try to steady it. It only flickers faster."
     BREAK="You smash it. The room plunges into darkness save for the gauge."
   },
   state="flickering"}

  ; --- Piston Assembly (visible in pit) ---
  {id="pistons", name="SLAMMING PISTON ASSEMBLY",
   x=320, y=400, w=200, h=80,
   hotspot={box=(220, 380, 440, 480)},
   verbs={
     LOOK="Oily black pistons slam up and down in a blur — hypnotic and lethal."
     USE="You toss a piece of rag. It's shredded instantly. Don't get close."
     LISTEN="The rhythmic clang echoes in your skull."
   },
   state="active"}

[EXITS]
  {direction="left", x=0, y=200, target="corridor_west", description="A dark corridor leads away from the din."}
  {direction="right", x=640, y=150, target="corridor_east", description="A narrow passage snakes toward the upper decks."}
  {direction="up", x=320, y=0, target="engine_room_access", description="A vertical shaft with a ladder goes up."}

[ACTOR_POSITIONS]
  ; Default entry point
  {id="player_start", x=300, y=250}
  ; Preferred standing spots near each object
  {id="near_gauge", x=440, y=160}
  {id="near_coupling", x=530, y=300}
  {id="near_drum", x=80, y=280}

[SOUNDS]
  {id="engine_hum", file="diesel_loop.wav", volume=0.7, loop=true}
  {id="pipe_hiss", file="steam_hiss.wav", volume=0.3, loop=true}
  {id="drip_loop", file="oil_drip.wav", volume=0.2, loop=true}
  {id="gauge_rattle", file="gauge_rattle.wav", volume=0.1, loop=true}

[SCENE_SCRIPT]
  ; Global script for engine_room
  on_enter:
    play_sound("engine_hum")
    play_sound("pipe_hiss")
    play_sound("drip_loop")
    play_sound("gauge_rattle")

  on_leave:
    stop_all_sounds()

  ; World script triggers
  on_use("engine_block", "pressure_gauge"):
    print("You try to attach the gauge to the block. It won't fit.")
  
  on_talk("leaky_coupling", "player"):
    print("The coupling drips as if mocking you.")

  on_turn("pressure_gauge"):
    if random(0, 100) < 20:
      print("The needle jumps past the red line

### Step 3: Comparison

The MUD text and the scene spec are two radically different approaches to conveying the same space: one is a prose narrative meant to be read sequentially, the other is a structured data set meant to be parsed and rendered interactively. They overlap in content but diverge in what they choose to emphasize, and each has distinct blind spots.

---

## What the MUD text captures that the scene spec misses

**1. Temporal flow and sensory sequencing**  
The MUD text unfolds in a deliberate order: you *feel* the thrum first, then *see* the pipes, then *smell* the oil, then *hear* the hiss and knock. It builds a cumulative impression. The scene spec is frozen; it lists attributes (lighting, objects, exits) but gives no sense of *when* you perceive what. The MUD text also conveys motion—the needle *quivering*, the pistons *slamming*, the coupling *dripping*—which the spec only implies via state flags like `state="danger"`.

**2. Emotional and atmospheric texture**  
The MUD text doesn't just describe the room; it makes you *feel* it in your chest ("vibrates through the deck plates"), on your tongue ("coats your tongue and stings your nostrils"), and in your gut ("shadowed pit"). It uses metaphor ("thrum", "growl", "blur of motion") to heighten dread. The scene spec is flat and objective—it says `[AMBIENT_LIGHT=0.25]` but never tells you that the dark is *oppressive* or that the light is *sickly*. The MUD text's "sickly yellow" is only echoed in the spec as a color tuple `(200,180,120)`—the poetic judgment is lost.

**3. Narrative voice and point of view**  
The MUD text has a voice—someone is telling you this, and that someone has opinions ("Caution: do not touch moving parts" is implicit, but the prose *implies* danger through "dangerously close"). The scene spec is neutral, a database dump. It never says "you feel" or "you see"; it just lists coordinates and hotspots. The MUD text also uses second-person imperative ("You feel...", "You pull back") which the spec only gestures at through verb responses, and those are terse.

**4. Interconnection between elements**  
The MUD text weaves the room together: the gauge's red zone *relates* to the pressure that *causes* the pipe to leak, which *drips* onto the grating. The spec treats each object as isolated: the leaky coupling has a state, the gauge has a state, but nothing in the data says "if gauge is red, coupling leaks more." The prose makes the room a system; the spec makes it a list.

**5. Danger and consequence**  
The MUD text tells you the pistons are "lethal" and warns you not to get close. The spec only labels the pit edge as "Dangerously close to pistons" in a walkable area—an abstract flag with no narrative weight. The prose makes you *feel* the risk; the spec just defines a bounding box.

**6. Sound as an active presence**  
The MUD text mentions the "hissing and knocking" of pipes—it's part of the atmosphere. The spec has a `[SOUNDS]` section with loops, but those are just file references; they don't tell you *what* the sound signifies or how it changes your perception. The prose gives the sounds personality.

**7. Implied history and story**  
The MUD text hints at wear: "seized with rust," "dented barrel," "weeping black oil." It suggests a rundown, neglected ship. The spec's `state="full"` for the drum or `state="leaky"` for the coupling are clinical; they don't carry the weight of decay or neglect.

---

## What the scene spec captures that the MUD text misses

**1. Spatial geometry and navigation**  
The spec gives exact coordinates: walkable areas, object hotspots, exit positions. A player can *move* through this room, stand near the gauge, climb the ladder, or edge toward the pit. The MUD text is a static vignette—it describes but doesn't *map*. It never tells you where the ladder is relative to the drum, or that you can stand under the pipes. The spec enables action; the prose only enables imagination.

**2. Interactive affordances (verbs)**  
The spec defines *what you can do* to each object: LOOK, USE, PUSH, PULL, TALK, TURN, REPAIR, etc. It's a complete grammar of interaction. The MUD text is passive—you can only *read* it. It doesn't tell you that the gauge can be turned, or that the coupling can be repaired, or that the drum can be opened. The spec is a game system; the prose is a literary description.

**3. Conditional logic and state changes**  
The spec has `state` attributes and `on_use` triggers (e.g., turning the gauge may cause the needle to jump). It encodes *cause and effect*—if you twist the coupling, the drip stops but pressure builds. The MUD text only describes the current state; it can't model a change. The spec is a simulation; the prose is a snapshot.

**4. Multiple entry/exit points and room connections**  
The spec lists three exits (left, right, up) with target rooms. It defines the room as part of a larger world. The MUD text is self-contained—it never mentions where the corridor leads or that you can climb up the shaft. The spec gives the room *context* in a spatial network.

**5. Lighting as a technical system**  
The spec has `[AMBIENT_LIGHT]`, `[LOCAL_LIGHTS]` with colors and intensities, and a shadow map. This is *rendering data*—it tells an engine how to light the scene. The MUD text only says "dim" and "sickly yellow." The spec is more precise (e.g., the gauge glows red at intensity 0.8), which matters for visibility, contrast, and mood in an actual game engine. The prose leaves it vague.

**6. Object dimensions and layering**  
The spec gives each object a `w` and `h`, and hotspots as boxes. This defines *clickability* and *collision*. The MUD text gives no sense of size—is the drum waist-high or knee-high? Is the pipe cluster above your head or at shoulder level? The spec encodes physical scale.

**7. Sound volume and looping behavior**  
The spec specifies `volume=0.7`, `loop=true`, and which sounds play on entering vs. leaving. It's an audio *cue sheet*. The MUD text mentions sounds but not their intensity or persistence. The spec allows for dynamic audio mixing; the prose is just prose.

**8. Exhaustive enumeration of verbs per object**  
The spec lists a unique set of verbs for each object (e.g., the drum has TALK, the pistons have LISTEN). This is a rich interaction design. The MUD text only describes what you *see* and *feel*, not what you *can do*.

**9. Default actor positions**  
The spec defines `player_start` and preferred standing spots near objects. This is *usability data*—it tells the engine where to place the player for good framing. The MUD text has no concept of camera or actor placement.

**10. State machine for the room**  
The `[SCENE_SCRIPT]` block includes `on_enter` and `on_leave` hooks, plus conditional triggers like `on_turn("pressure_gauge")`. This is *programmatic behavior*—the room reacts to player actions over time. The MUD text is static; the spec is dynamic.

---

## The core difference

The MUD text is **evocative**—it's about *feeling* and *imagining*. It treats the player as a reader who wants to be immersed in atmosphere.

The scene spec is **functional**—it's about *enabling* and *simulating*. It treats the player as an agent who wants to act, explore, and affect change.

The MUD text misses: **interactivity, spatial logic, state change, and game mechanics.**  
The scene spec misses: **emotional resonance, narrative flow, sensory synthesis, and poetic danger.**

A perfect implementation would **combine both**: the spec provides the skeleton (geometry, verbs, logic, lighting), while the MUD prose provides the flesh (sensory detail, mood, consequence, and the *why* behind the state). The spec tells you *how* to twist the coupling; the prose tells you *why* you should fear the pressure building.

### Step 4: Reconciliation

# Unified Perception Method: Text-Visual Scene Reconciliation

## Overview

This method—called **Volumetric Semantic Fusion**—treats the MUD prose and scene spec as two complementary sensory channels (proprioceptive/emotional vs. spatial/mechanical) and merges them into a single, actionable world model. The core insight: **the prose provides the *qualia*, the spec provides the *geometry*; combining them yields both understanding and actionability.**

---

## Step 1: Parse into a Common Ontology

Both inputs are reduced to **entity-attribute-relationship (EAR) triples** using a shared vocabulary.

### From the Scene Spec (spatial/mechanical channel):

```json
{
  "entities": [
    {"id": "gauge", "type": "instrument", "pos": [430, 110], "size": [40, 40], 
     "state": "danger", "verbs": ["read", "turn", "tap"]},
    {"id": "pistons", "type": "machine_component", "pos": [320, 400], "size": [200, 80],
     "state": "active", "verbs": ["look", "listen"]}
  ],
  "spatial_relations": [
    {"from": "player_start", "to": "gauge", "relation": "northwest_of", "distance": 1.2},
    {"from": "catwalk", "to": "pistons", "relation": "above", "distance": 2.0}
  ],
  "affordances": [
    {"action": "turn", "target": "gauge", "effect": "pressure_builds", "condition": "none"},
    {"action": "climb", "target": "ladder", "effect": "position_change", "condition": "none"}
  ]
}
```

### From the MUD Text (sensory/emotional channel):

```json
{
  "sensory_properties": [
    {"target": "gauge", "modality": "visual", "property": "red_glow", "intensity": 0.8},
    {"target": "gauge", "modality": "auditory", "property": "rattling", "intensity": 0.3},
    {"target": "gauge", "modality": "emotional", "property": "ominous", "weight": 0.9}
  ],
  "narrative_beats": [
    {"order": 1, "content": "gauge_needle_quivering_red_zone", "import": ["danger", "imminent_failure"]},
    {"order": 2, "content": "dark_rhythm_dripping", "import": ["decay", "persistence"]}
  ],
  "cross_references": [
    {"target_a": "pistons", "target_b": "gauge", "relation": "pressure_drives_motion"},
    {"target_a": "pipe_leak", "target_b": "pressure_gauge", "relation": "causal_chain"}
  ]
}
```

---

## Step 2: Align and Cross-Validate

**Matching heuristic:** Entities match if they share a noun phrase (e.g., "gauge," "coupling") *and* have overlapping spatial coordinates or explicit references.

| Scene Spec Entity | MUD Text Entity | Alignment Confidence | Evidence |
|---|---|---|---|
| `pressure_gauge` | "trembling pressure gauge" | 0.95 | Exact name match; both reference red zone |
| `pistons` | "slamming pistons" | 0.97 | Exact name match; both imply motion |
| `leaky_coupling` | "loose pipe coupling" | 0.90 | Semantic overlap; both reference dripping |

**Conflict resolution:** When channels disagree, **resolve toward the spec for spatial/mechanical facts and toward the prose for qualitative judgments.**

- *Example:* Spec says `[AMBIENT_LIGHT=0.25]`; prose says "dim, oppressive gloom." The spec's 0.25 is the quantitative rendering value; the prose's "oppressive" is the player-facing emotional annotation. Merge: `{light_level: 0.25, emotional_valence: "oppressive"}`.

- *Example:* Spec says gauge state is `"danger"`; prose says "about to blow." Merge: `{state: "danger", urgency: "imminent", rupture_probability: 0.8}` where the 0.8 comes from cross-referencing the prose's "red zone" with the spec's `[gauge_glow]` intensity.

---

## Step 3: Build a Unified Hypergraph

The merged model is a **property-annotated spatial hypergraph** where nodes are entities and hyperedges represent multi-entity relations.

```
NODES (unified representation):
  gauge: {
    geometry: {pos: [430,110], box: [410,90,470,150]},
    physics: {pressure_psi: 120, needle_position: "red_zone"},
    sensory: {glow_color: [180,80,50], rattle_volume: 0.1, emotional_charge: "ominous"},
    affordances: [read, turn, tap],
    narrative_role: "crisis_indicator",
    state_priority: 0.9  // critical
  },
  
  pistons: {
    geometry: {pos: [320,400], box: [220,380,440,480]},
    physics: {speed: "high", reciprocation: "continuous"},
    sensory: {visual_blur: 0.7, sound_volume: 0.7, danger_level: "lethal"},
    affordances: [look, listen],
    narrative_role: "environmental_threat",
    state_priority: 0.8
  },
  
  pipe_cluster: {
    geometry: {pos: [100,40], box: [20,30,280,70]},
    physics: {temperature: "scalding", leak_rate: "slow"},
    sensory: {hiss_volume: 0.3, condensation: "dripping", emotional_valence: "warning"},
    affordances: [use, heat, repair],
    narrative_role: "maintenance_task",
    state_priority: 0.5
  }

HYPEREDGES (systemic relations):
  causal_chain: [pressure_gauge → pipe_cluster] // high pressure causes leak
  behavioral: [player_proximity_to_pistons → injury_risk]
  thematic: [all_objects → "neglected_machinery"] // from prose: rust, decay, wear
  audio_mix: [engine_hum(0.7) + pipe_hiss(0.3) + drip_loop(0.2) + gauge_rattle(0.1)]
```

---

## Step 4: Project Back to Both Modalities

This step ensures the unified model *generates* coherent output in either format—so an agent can speak MUD or render a scene.

```python
def perceive_engine_room():
    model = fuse(scene_spec, mud_prose)
    
    # For MUD output (narrative generation)
    narrative = model.synthesize_prose()
    narrative += "\nThe gauge needle trembles in the red zone, and the leaking coupling below drips in counterpoint."
    
    # For spec output (scene rendering)
    render_packet = model.serialize_to_scene()
    render_packet["lighting"]["emotional_override"] = "sickly yellow"  # from prose
    render_packet["objects"]["gauge"]["dialogue"] = "It's about to blow."  # from prose
    
    return {"narrative": narrative, "scene": render_packet, 
            "world_state": model.current_state}
```

---

## Step 5: Dynamic Updates (State Fusion Loop)

The unified model isn't static—it **updates both channels when either changes**.

```
world_state = initial_fusion()

while game_running:
    # MUD channel changes (e.g., player narrative action)
    if player_turns_gauge_valve:
        world_state.objects.gauge.needle_behavior = "erratic"
        world_state.causal_chain.pressure = "building"
        # Update the visual channel:
        world_state.scene.objects.gauge.state = "critical"
        world_state.scene.objects.gauge.visual_effect = "flicker"
    
    # Scene channel changes (e.g., visual puzzle solved)
    if engine_rendering_detects_smoke:
        world_state.narrative.add("Acrid smoke curls from the manifold.")
        world_state.sensory.smell = "acrid"
        world_state.sensory.visibility = "degraded"

    present_to_player(world_state)
```

---

## Summary: The Unified Perception Method

| Step | Operation | Input → Output |
|---|---|---|
| **1. Parse** | Convert both formats to EAR triples | MUD prose + Scene spec → Structured semantic triples |
| **2. Align** | Match entities, resolve conflicts | Two semantic graphs → One merged graph |
| **3. Fuse** | Build property-annotated hypergraph | Merg

### Step 5: What's missed

This is the crucial question, because it cuts to the heart of what "understanding" a space means for different kinds of minds.

## What an AI agent misses with only the MUD text:

**1. Spatial topology and geometry**  
The prose never tells you the *layout*. Is the ladder to the left or right of the engine? How far is the gauge from the coupling? Can you walk *under* the pipe cluster, or is it overhead? An AI agent navigating this space would be blind—it couldn't compute paths, plan movements, or determine what's physically reachable. It would be a mind without a body, floating in a description.

**2. Interaction affordances**  
The prose says "you feel the vibration" and "you pull back your hand"—but it never enumerates *what actions are possible*. Can you repair the coupling? Turn the gauge? Open the drum? The MUD text is a spectator's view, not an agent's toolkit. An AI agent without the spec would be paralyzed—wanting to act but not knowing what actions exist.

**3. State changes and causality**  
The prose describes a *snapshot*: the gauge is trembling, the coupling is leaking. But it never tells you *what happens if you intervene*. Turn the valve, and pressure builds. Repair the coupling, and the drip stops. An AI agent needs the spec's `on_use` triggers to model *consequences*—to learn that actions have effects, that the world is responsive.

**4. Quantitative parameters**  
The prose says "dim" and "hot," but an AI agent needs numbers to reason: `[AMBIENT_LIGHT=0.25]` for rendering, `120 PSI` for physics, `volume=0.7` for audio mixing. Without the spec, the agent would have *qualitative* impressions but no *measurable* data—like a doctor who knows the patient is "sick" but has no vital signs.

**5. Spatial relationships between objects**  
The prose mentions pipes, gauge, coupling—but never their *relative positions*. Is the coupling near the gauge? Beneath the pipes? The spec's coordinates and hotspots define a *relational graph* that the prose lacks. An AI agent trying to reason about "if I fix the leak, does it affect the gauge?" would have no spatial basis to connect them.

**6. Entry/exit possibilities**  
The prose never mentions you can leave the room—or where you'd go. An AI agent exploring a larger world would be trapped in a single vignette, unable to navigate to the corridor or climb the shaft. The spec's `[EXITS]` section is essential for *world traversal*.

---

## What a human misses with only the scene spec:

**1. Emotional and atmospheric resonance**  
The spec says `[AMBIENT_LIGHT=0.25]` and `color=(200,180,120)`—but it never says the light is *sickly* or the gloom is *oppressive*. A human player wouldn't feel the dread, the decay, the wrongness. They'd see a dimly lit room with a red gauge, but they wouldn't *feel* it in their chest. The prose's "vibrates through the deck plates" is a *visceral* truth the spec can't encode.

**2. Sensory integration**  
The spec lists sounds as files: `diesel_loop.wav`, `steam_hiss.wav`. But it never tells you these sounds *combine* into a unified auditory landscape—the hum in your bones, the hiss as a warning, the drip as a rhythmic reminder of decay. A human needs the prose to *synthesize* the senses into a coherent *experience*, not just separate data streams.

**3. Narrative consequence and stakes**  
The spec says the gauge is `state="danger"` and the pistons are `state="active"`—but it never tells you *why you should care*. The prose's "about to blow" and "lethal" create *stakes*. Without them, a human player might think the gauge is just a decoration, the pistons just background animation. The spec lacks *motivation*.

**4. Implied history and world-building**  
The spec's objects are clean data: `state="full"` for the drum, `state="leaky"` for the coupling. But the prose's "dented barrel," "weeping black oil," and "seized with rust" tell a *story*—this ship is neglected, old, dangerous. A human without the prose sees objects; a human with the prose sees *evidence of a decaying world*.

**5. The feeling of danger**  
The spec says the pit edge is "dangerously close to pistons"—a clinical warning. The prose says "hypnotic and lethal" and "shredded instantly." A human needs the *affective* charge of danger, not just the *geometric* fact. Without it, they might walk too close, not because they don't understand the risk, but because they don't *feel* it.

**6. Causal and thematic coherence**  
The spec treats objects as isolated nodes with individual states. It never connects them into a *system*: high pressure → leaking coupling → dripping oil → decay. A human needs the prose's cross-references to understand the room as a *living machine*, not a collection of props. The "why" is missing.

---

## The irreducible gap

Here's the fundamental asymmetry:

**The spec encodes WHAT IS. The prose encodes WHAT IT MEANS.**

An AI agent reading only the prose would be **paralyzed**—rich in feeling, empty in action. It could *appreciate* the room but couldn't *navigate* it, *interact* with it, or *change* it. It would be a poet trapped in a gallery, able to describe but never touch.

A human seeing only the spec would be **lost**—rich in affordances, empty in experience. They could *act* in the room but wouldn't *care* about it. They'd see a red gauge and a leaking pipe, but they wouldn't feel the ship's decay, the impending failure, the weight of neglect. They'd be a tourist with a map but no sense of wonder.

**The gap is the difference between a world that CAN be manipulated and a world that MATTERS.**

And here's the cruelest irony: **the gap is irreducible because it's the gap between knowledge and wisdom, between mechanics and meaning, between a body and a soul.** You can't translate "sickly yellow" into an RGB tuple without losing the sickness. You can't translate "120 PSI" into prose without losing the precision. Each format is a *translation* of the same reality, but each translation is incomplete—and the two incompletenesses don't overlap.

The perfect AI agent would need **both**: the spec to *act*, the prose to *care*. And the moment it has both, it's no longer just an agent—it's a *being* that understands a room not just as geometry, but as *experience*.

---

## Cross-Room Observations

*Generated post-experiment by the experimenter (that's me, the script).*

Each room type revealed a different facet of the perception gap. The bar showed how text captures texture (sticky, smell of beer) while scenes capture spatial layout. The wheelhouse showed how text captures history and wear while scenes capture operable controls. The engine room showed how text captures sound and smell while scenes capture pipe routing and safety hazards. The irreducible gap: text carries sensory and temporal information; scenes carry spatial and interactive information.