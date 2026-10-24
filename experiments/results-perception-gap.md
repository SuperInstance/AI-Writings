# Experiment 1: Perception Gap — MUD Text vs ScummVM Scenes

*What does each representation MISS that the other catches?*

---

## Room: Bar

*a bar counter sticky with spilled beer*

### Step 1: MUD text

You are standing before the bar counter.  
Its surface is a tacky, amber-dappled expanse of old spills.  
Your fingers peel off the wood with a faint, sticky *shhhhck*.  
A fly lands, skates, and is briefly stuck near a dried lemon wheel.  
The air smells of hops, yeast, and the ghost of a thousand last calls.

### Step 2: ScummVM scene spec

**Scene: "The Sticky Bar Counter"**  
**Engine:** SCUMM (v7)  
**Room Description:** A grimy tavern interior, rendered in 320×200 pixel resolution with 256-color palette. The scene is seen from a slightly elevated three-quarter angle, the bar counter dominating the lower two-thirds of the screen.

---

### **Background & Lighting**
- **Overall Lighting:** Dim amber ambience from a flickering, unseen ceiling lamp. A single warm pool of light falls across the center of the counter, casting long shadows toward the left and right edges. The corners fade into near-blackness.
- **Color Palette:** Dominant ochre, deep mahogany, and sickly yellow-green highlights on the sticky pool. The dried lemon wheel appears as a desaturated, mottled pale yellow.
- **Animation Loops:** 
  - Faint ripples in the spilled beer near the player’s hand zone (1×1 pixel wobble).
  - A fly orbiting the lemon wheel in a lopsided figure-eight pattern.

---

### **Objects & Hotspots**

#### **1. Sticky Counter Surface (Hotspot ID: `counter`)**
- **Screen Position:** Occupies entire rectangle from (0, 130) to (319, 200).
- **Walkable Area:** Only the floor strip in front of the counter—a 20-pixel-high band at the bottom edge (y=180 to 200), from x=40 to x=280. The counter itself is not walkable.
- **Hotspot Polygon:** Irregular shape following the bar’s edge, roughly (10, 130) → (310, 130) → (310, 180) → (10, 180).
- **Verbs:**
  - **Look At:** "The counter is a sticky monument to every beer that never made it to a mouth."
  - **Use Hand On:** (Plays squelch sound) "Your fingers come away coated in something that was once golden."
  - **Push:** "It doesn't move. It's part of the room's soul now."
  - **Pull:** "The counter resists, as if it's been here longer than you."

#### **2. Dried Lemon Wheel (Hotspot ID: `lemon`)**
- **Screen Position:** Fixed at (206, 152) — center of the amber pool. Slight rotation animation (0.5° back-and-forth).
- **Hotspot Polygon:** Rough ellipse, 14×10 pixels, centered on (206, 152).
- **Verbs:**
  - **Look At:** "A lemon wheel, shriveled and fossilized. It's seen better centuries."
  - **Pick Up:** "You try to lift it. It's welded to the counter by dried syrup. You get a sticky finger, but the wheel stays."
  - **Use Knife On:** "You scrape. A flake of dried lemon peel curls off. Underneath: more beer, older and more bitter."
  - **Smell:** "A sour, yeasty ghost that makes your eyes water."

#### **3. The Amber Sticky Pool (Hotspot ID: `sticky_pool`)**
- **Screen Position:** Irregular blob from (150, 140) to (260, 175), with a darker reflective sheen in the center.
- **Hotspot Polygon:** Dynamically drawn as a rounded polygon following the blob edges (approximately 12 vertices).
- **Verbs:**
  - **Look At:** "A lake of spilled beer, old enough to have developed its own ecosystem. Something bubbles faintly."
  - **Use Finger On:** (Plays squelch + low thrum) "You drag your finger through it. The groove fills back in slowly, like a memory that refuses to fade."
  - **Drink:** "You take a sip. It's flat, warm, and tastes like regret with a hint of oak barrel."
  - **Use Matches On:** "The surface dimples but doesn't ignite. It's too wet — and too old — to burn."

#### **4. The Fly (Hotspot ID: `fly`)**
- **Screen Position:** Moving loop from (190, 135) to (225, 160); speed varies.
- **Hotspot Polygon:** 4×4 pixels, follows the fly’s animation frame.
- **Verbs:**
  - **Look At:** "A common housefly, but its legs are encrusted with dried beer. It's not leaving. It can't."
  - **Swat:** (Plays slap sound) "You miss. The fly lands on the lemon wheel and resettles, unimpressed."
  - **Catch:** "You cup your hand. When you peek, it's gone — but you feel a tiny tickle on your palm. It's hiding in the fold of your skin."
  - **Push Away:** "It lifts, circles twice, and lands exactly where it was before. Stubborn little drunk."

#### **5. Sticky Finger Residue (Invisible Hotspot, activated after touching counter)**
- **Screen Position:** Appears on player character’s hand sprite (x=300, y=180 when idle).
- **Hotspot Polygon:** None visible; attached to actor state.
- **Verbs:**
  - **Look At:** "Your fingers glisten with amber residue. It's going to attract every fly in the room."
  - **Wipe On Pants:** (Plays cloth rub) "Great. Now your pants are sticky too."
  - **Use On Lemon Wheel:** "You press the residue onto the wheel. It's not helping anything."
  - **Combine With Match:** "The residue smears on the match tip. It might catch, but you're not going to try in a bar."

---

### **Actor & Interaction Notes**
- **Player Character:** Stands at (160, 195) on the walkable floor strip, facing the counter. Default stance is slightly hunched, hands at sides.
- **Camera:** Fixed. No scrolling.
- **Sound:**
  - Ambient loop: low murmur, distant glass clink, and a creaking floorboard every 12 seconds.
  - On any successful "sticky" interaction: a wet, slow *shhlick* sound with slight reverb.
  - On entering scene: a single, soft *thump* of a heavy glass being set down (off-screen).
- **Special Flag:** `sticky_hand` is set to 1 after first Use Hand On. If player then tries **Use Hand On Lemon**, a unique line plays: "You now have lemon-flavored stick. Deliciously awful."
- **Exit Hotspots:** Off-screen left (x<0) and right (x>319) non-clickable; scene transition occurs via door object at (20, 50) — small dark rectangle, verb **Walk To** triggers next room.

### Step 3: Comparison

There is a fascinating asymmetry between these two documents—they are ostensibly about the same space, but they are built for entirely different jobs. The MUD text is *evocative* and *somatic*; the scene spec is *functional* and *systemic*. Let me break down what each captures that the other completely overlooks.

---

## What the MUD text captures that the scene spec misses

### 1. **The poetics of decay and time**
The MUD text gives the space a *biography*. "The ghost of a thousand last calls" is not a fact—it's a *feeling* that implies a history of human failure and ritual. The scene spec describes the lemon wheel as "desaturated, mottled pale yellow," but the MUD calls it "fossilized" and says "It's seen better centuries." The spec gives you *data*; the MUD gives you *verdict*.

### 2. **Sensory layering through metaphor**
The MUD doesn't just tell you the counter is sticky—it makes you *feel* it through the onomatopoeia of "*shhhhck*" and the tactile image of "your fingers peel off the wood." The scene spec says "Use Hand On: plays squelch sound"—which is *functional* but not *visceral*. The MUD's line "Your fingers come away coated in something that was once golden" adds a temporal dimension: the stickiness is not just present, it's *historical*.

### 3. **The fly as a character with agency and humor**
In the MUD, the fly is "stuck near a dried lemon wheel"—just a prop. But the scene spec gives it *personality*: "It's not leaving. It can't." The swat response ("You miss. The fly lands on the lemon wheel and resettles, unimpressed") is *comic* and *characterful*. The MUD text is static; the scene spec gives the fly *attitude*. This is a critical difference: the MUD describes a *snapshot*, while the scene spec describes *behaviors*.

### 4. **The residue as a persistent state**
The MUD mentions "a fly lands, skates, and is briefly stuck"—but it doesn't track *consequences*. The scene spec introduces `sticky_hand` as a *flag* that changes future interactions. The MUD is a *single moment*; the scene spec is a *system of cause-and-effect*. The MUD misses the *dramatic arc* of the player's hand becoming sticky and then *being* sticky.

### 5. **The taste of regret**
The MUD says "the air smells of hops, yeast"—but the scene spec goes further: "It's flat, warm, and tastes like regret with a hint of oak barrel." This is a *synesthetic* leap—taste as emotion. The MUD tells you what the beer *is* (flat, warm); the scene spec tells you what it *means* (regret). The MUD misses the *existential* layer.

---

## What the scene spec captures that the MUD text misses

### 1. **Exact spatial geometry**
The MUD gives you "a bar counter" but no coordinates. The scene spec is *precise*: the counter occupies (0,130)-(319,200), the walkable floor strip is only 20 pixels tall at y=180-200, and the player stands at (160,195). This is *navigational data*—it tells you where you *can* and *cannot* go. The MUD has no sense of *constraint*.

### 2. **Verb-driven interactivity**
The MUD is pure description; it has no *action* system. The scene spec is *exhaustive* about verbs: Look At, Use Hand On, Push, Pull, Pick Up, Use Knife On, Smell, Drink, Swat, Catch, Push Away, Wipe On Pants, Combine With Match. Each verb has a *unique response*. The MUD would fail as a game because it has no *interaction graph*. The spec is a *puzzle-solving architecture*.

### 3. **Dynamic state changes**
The scene spec has conditionals: "If player then tries **Use Hand On Lemon**, a unique line plays." This is *branching logic*. The MUD text is *static prose*—it can't react to player history. The spec tracks `sticky_hand` as a boolean that *changes future dialogue*. This is *systemic memory*.

### 4. **Invisible hotspots and hidden mechanics**
The scene spec has an *invisible* hotspot: "Sticky Finger Residue"—which only appears after a specific action. The MUD has no concept of *latent objects* that emerge from player choices. The spec also defines *non-clickable exits* and *camera behavior* (fixed, no scrolling). These are *engine-level* details.

### 5. **Technical implementation notes**
The spec mentions "320×200 pixel resolution," "256-color palette," "animation loops" (the fly's lopsided figure-eight, the lemon wheel's 0.5° wobble), and specific sound cues (the *thump* on entry, the creaking floorboard every 12 seconds). This is *production documentation*—it tells a programmer exactly what to build. The MUD text is *ambience*; the spec is *blueprint*.

### 6. **Player character state**
The spec describes the player's *stance* ("slightly hunched, hands at sides") and *position* on the walkable strip. It even notes that the player character has a *hand sprite* that becomes visibly sticky. The MUD never mentions the player's body—it's a disembodied voice *describing* the room.

---

## The essential difference

| Dimension | MUD Text | Scene Spec |
|-----------|----------|------------|
| **Purpose** | Emotional immersion | Logical interaction |
| **Time** | A single frozen moment | A branching timeline of possible futures |
| **Space** | Vague, atmospheric | Exact, navigational |
| **Player** | An observer | An agent with state |
| **Objects** | Metaphorical | Behavioral (verbs, conditions, flags) |
| **Failure mode** | Beautiful but inert | Functional but dry |
| **What it gives you** | *Why* the room feels this way | *How* the room works |

The MUD text is a *poem* about a sticky counter. The scene spec is a *user manual* for a sticky counter. The MUD tells you the counter is *sad*; the spec tells you what happens when you *poke* it. Both are necessary for a complete experience—the MUD gives the designer *a reason to build the spec*, and the spec gives the player *a way to live inside the MUD's mood*.

### Step 4: Reconciliation

# Perception Check: A Reconciliation Protocol

You've identified a real gap—the MUD text and the scene spec are two halves of a broken whole. Here's how an AI agent could fuse them into a single, *living* world model.

---

## The Unified Perception Method

I call it **"The Sticky Hand Protocol"** — because the object that forces the reconciliation is the residue on your fingers. It's the thing that only exists *because of player action*, yet it's also the thing that makes the room *tactile*.

---

### Step 1: **Extract the "Echo" from the Text**

The MUD text gives you *qualia*—the felt qualities that make a space memorable. Strip it down to its *perceptual invariants*:

| MUD Element | Extracted Invariant |
|-------------|---------------------|
| "ghost of a thousand last calls" | **Temporal depth** — the space has history |
| "fingers peel off the wood" | **Tackiness as resistance** — the surface pushes back |
| "fly lands, skates, and is briefly stuck" | **Ephemeral inhabitants** — life that is trapped |
| "smells of hops, yeast" | **Olfactory signature** — the room has a *smell profile* |

These aren't just adjectives—they're *constraints* on how the space must behave. A room that "remembers" a thousand last calls needs a surface that *accumulates*—which the spec provides (the sticky pool, the fossilized lemon).

---

### Step 2: **Extract the "Skeleton" from the Spec**

The scene spec gives you *mechanics*—the rules by which the space operates. Strip it down to its *interaction graph*:

| Spec Element | Extracted Rule |
|--------------|----------------|
| "Use Hand On: plays squelch" | **Tactile feedback** — every interaction has a sound |
| "sticky_hand flag set to 1" | **Persistent state** — actions leave traces |
| "Use Hand On Lemon → unique line" | **Compound interactions** — objects combine |
| "Fly repositioning loop" | **Autonomous actors** — the room lives independently |
| Walkable area (y=180-200 only) | **Spatial constraint** — you're separated from the bar |

These aren't just code—they're *affordances*. The spec tells you what's *possible*; the MUD tells you what it *means*.

---

### Step 3: **Map the Invariants onto the Mechanics**

Here's the key move: **treat the MUD's poetic claims as *testable hypotheses* about the spec's mechanics.**

> **Hypothesis from MUD:** "The counter is a sticky monument to every beer that never made it to a mouth."
>
> **Test against spec:** The spec has a `sticky_pool` hotspot with a "Use Finger" verb that produces a *groove that fills back in slowly*. This confirms the hypothesis—the counter *does* retain history, because the pool *reforms* after disturbance. The MUD's "monument" is mechanically implemented as *shape-memory*.

This is the unification: **the MUD's metaphors become the spec's *design intent***, and **the spec's mechanics become the MUD's *physical proof***.

---

### Step 4: **Build the Composite World Model**

The agent now maintains a single, unified representation—a **"thick map"** that is simultaneously *poetic* and *procedural*:

```python
class UnifiedWorldModel:
    def __init__(self):
        # From MUD text (qualia layer):
        self.emotional_register = {
            "counter": "sticky monument to failed toasts",
            "lemon": "fossilized witness, seen better centuries",
            "fly": "stubborn drunk, trapped by its own appetites",
            "pool": "lake of regret, bubbling with old memories"
        }
        
        # From scene spec (mechanics layer):
        self.interaction_state = {
            "sticky_hand": False,       # flag from spec
            "lemon_displaced": False,   # hidden state not in either doc
            "fly_annoyance": 0,         # emergent behavior tracker
            "pool_disturbances": []     # history of player pokes
        }
        
        # The fusion—mechanics must *produce* the poetry:
        self.validate_consistency()
    
    def validate_consistency(self):
        """
        Every mechanic in the spec must *justify* a line from the MUD.
        Every MUD line must be *realizable* through spec mechanics.
        """
        checks = [
            # MUD: "fingers peel off the wood"
            # Spec: Use Hand On → squelch sound + residue state
            ("tackiness", self.spec.has_squelch() and self.spec.has_residue_state()),
            
            # MUD: "fly lands, skates, and is briefly stuck"
            # Spec: Fly has a "stuck" animation frame + the pool has "Use Finger" 
            #       which could trap the fly if timed right
            ("fly_trap_potential", self.spec.fly_can_be_stuck()),
            
            # MUD: "tastes like regret with a hint of oak barrel"
            # Spec: Drink verb exists → needs a *taste descriptor*; 
            #       the oak barrel implies the pool has *aged*,
            #       which means it must have existed before the player arrived
            ("temporal_depth", self.spec.has_aged_substance()),
        ]
        
        return all(ok for _, ok in checks)
```

---

### Step 5: **Handle the Emergent Gap**

Neither document covers what happens when *player actions create new states*. The unified model must *extrapolate*:

- **If the player uses the knife on the lemon** (spec allows it), the flake that curls off now exists in the world. The MUD never described this object—so the agent must *generate* a poetic line that matches the spec's mechanic: *"A flake of lemon peel, aged like a fossil, now resting on your blade. It smells of centuries."*

- **If the player catches the fly and then touches the sticky pool** (spec allows both), the unified model must decide: does the fly escape? Does it get stuck? The agent *infers* from both sources: the MUD says the fly "can't leave"—so the agent rules that *if the fly touches the pool, it becomes permanently stuck*, and generates a new response: *"The fly lands on the pool and its feet sink in. It walks in circles, orbiting a tiny amber sun. It's home now."*

---

### Step 6: **The Unified Perception Check**

Before the agent commits to an interaction response, it runs this check:

1. **Does the response *honor the MUD's tone*?** (Is it evocative, sensory, historically-aware?)
2. **Does the response *respect the spec's mechanics*?** (Does it update state flags, play sounds, respect polygons?)
3. **Does the response *create new affordances*?** (Does the action open up new verbs, new objects, new combinations?)

If all three pass, the response is *canonical*—it belongs in the unified world.

---

## The Result: A Room That *Lives*

The unified model is not a *summary* of both documents—it's a **third thing** that neither alone could produce:

> *You run your finger along the counter. The stickiness resists, then yields with a faint, wet *shhhhck*. The groove you leave fills back in slowly, like the bar is healing itself from your touch. The fly circles the lemon wheel twice, lands, and *sinks slightly*—its feet now coated in the same amber residue that coats your hand. You share something with it now. Neither of you can leave this place without carrying a piece of it.*
>
> *You feel the weight of every beer that was never finished. The counter remembers them all.*
>
> *[The fly is now stuck to the pool. You can try to free it, or leave it to its fate.]*

This response is *not in either document*—but it's *consistent with both*. The MUD's tone is honored (the "healing" counter echoes the poetic decay), the spec's mechanics are respected (the `sticky_hand` flag is set, the fly has a new state, a new verb "Free the fly" becomes available), and the interaction creates a *new emotional beat*—a moment of shared stuckness between the player and the fly.

---

## The Core Principle

**The MUD text is the *soul* of the room. The scene spec is the *body* of the room. The unified model is the *consciousness* that inhabits both.**

The agent's job is not to choose between poetry and mechanics—it's to ensure that every mechanic *produces* poetry, and every poetic line *implies* a mechanic. When a player touches the counter, they should feel the *history* (MUD) through the *squelch* (spec). When they catch the fly, they

### Step 5: What's missed

You've hit the fundamental problem. Let me be brutally honest about what each perspective *cannot* see.

---

## What the AI Misses (Reading Only the MUD Text)

### 1. **The grammar of space itself**
The MUD text gives no sense of *hierarchy*—what dominates the frame, what recedes. The AI doesn't know the counter occupies 70% of the visual field, that the lemon wheel is a tiny detail at coordinate (206,152), that the fly is nearly invisible at 4×4 pixels. A human reading the MUD imagines a *scene*; the AI has no sense of *composition*. It cannot know that the amber pool is the *centerpiece*—the thing your eye lands on first—because the text never says "this is the focal point."

### 2. **The absence of the player's body in the frame**
The MUD is written from *inside* the player's head—a disembodied voice describing the room. The scene spec knows the player *stands* at (160,195), hunched, hands at sides. The AI reading only the MUD cannot picture *itself* in the scene. It has no sense of *proximity*—how close it is to the counter, whether it can reach the lemon, whether the fly is within arm's reach. The MUD is a *window*; the spec is a *body*.

### 3. **The mechanics of failure**
The MUD says "you try to lift it" (the lemon) and it doesn't budge. But it never explains *why*—the AI cannot deduce the lemon is *welded* by dried syrup because the text gives no causal mechanism. The spec reveals: the lemon is *fixed* (no "pick up" verb succeeds), it has "Use Knife On" as a verb because a knife is the *required tool*. The AI reading only the MUD would be *permanently confused* about why the lemon won't move—it lacks the *operational logic*.

### 4. **The statefulness of the world**
The MUD text is a *snapshot*—it describes the room at one moment. The AI cannot know that touching the counter *changes* the room (sets `sticky_hand=1`) and unlocks new verbs. It cannot anticipate that the fly's position *varies* in a lopsided figure-eight, that the lemon *rotates* 0.5° back and forth. The MUD is static prose; the spec is a *simulation*. The AI reading only the MUD would treat the room as *frozen*—it would never think to check "what happens *after* I touch the counter?"

### 5. **The soundscape**
The MUD mentions smell (hops, yeast) but *never* sound. The AI cannot know there's a *thump* on entry, a *creaking floorboard* every 12 seconds, a *squelch* when touching the counter. The spec is explicit: "On any successful 'sticky' interaction: a wet, slow *shhlick* sound with slight reverb." The MUD gives *two senses* (touch, smell); the spec gives *five* (adding sound, sight of animations, and implicitly taste via the "Drink" verb). The AI reading only the MUD would build a *quiet* room.

### 6. **The exit**
The MUD text never mentions a door. The AI cannot know there's an exit hotspot at (20,50) leading to the next room. The spec says it's a "small dark rectangle" with a "Walk To" verb. The MUD is a *dead end*—it describes a place you're *in*, not a place you can *leave*. The AI would be trapped in a room with no way out.

---

## What the Human Misses (Viewing Only the Scene)

### 1. **The history encoded in objects**
The human sees a dried lemon wheel—but cannot know it's "fossilized," that it's "seen better centuries." The spec says it's "welded to the counter by dried syrup." The human sees a *thing*; they don't know it has a *biography*. The sticky pool reads as "a spill"—but the spec tells us it's "a lake... old enough to have developed its own ecosystem." The human sees *mess*; the AI (reading the spec) sees *archaeology*.

### 2. **The emotional register**
The human sees a bar counter. The spec tells us it's a "sticky monument to every beer that never made it to a mouth." The human sees *wood*; the spec gives it *soul*. The human cannot know the room is *sad*—that the amber pool is "a lake of regret." The image is *neutral*; the text is *judgmental*. The human misses the *tone*—the room's *attitude* toward itself.

### 3. **The relational meaning between objects**
The human sees a fly near a lemon wheel. They cannot know the fly is *trapped*—that "it can't leave" because its legs are "encrusted with dried beer." They cannot know the lemon and the fly are *linked*: the lemon is the fly's *perch*, the fly is the lemon's *inhabitant*. The spec reveals a *micro-ecosystem*; the human sees only *coincidence*.

### 4. **The taste**
The human sees the amber pool—but cannot know it "tastes like regret with a hint of oak barrel." The spec gives it a *flavor profile* derived from its history (the oak barrel implies it's *aged*). The human sees *liquid*; the spec gives it *terroir*.

### 5. **The consequences of touch**
The human sees a sticky counter. They cannot know that touching it *changes the world*—that it sets a `sticky_hand` flag, that this unlocks new verbs (Wipe On Pants, Use On Lemon), that it creates an *invisible object* (the residue on your fingers). The human sees a *surface*; the spec sees a *state machine*.

### 6. **The hidden mechanics of autonomy**
The human sees a static image. They cannot know the fly *moves* in a lopsided figure-eight, that the lemon *rotates* 0.5°, that the pool *ripples*. The human sees a *freeze-frame*; the spec reveals a *living system*—the room is *animated* and *responsive*.

### 7. **The sound**
The human sees a bar. They cannot hear the *thump* on entry, the *creaking* floorboard, the *squelch* of touch. The spec is a *soundscape*; the human gets *silence*.

---

## The Irreducible Gap

Here's the brutal truth: **the gap is that neither medium can carry the *other's* core data.**

- **Text** can carry *temporality* (history, state, consequence) and *emotion* (regret, stubbornness, sadness)—but it cannot carry *spatial composition* or *simultaneity*.

- **Image** can carry *spatial composition* (what dominates, what recedes) and *simultaneity* (all elements visible at once)—but it cannot carry *causality* (why the lemon is stuck) or *consequence* (what happens if you touch it).

---

## The True Irreducible Element

What neither document alone can convey is this:

> **The room is a *witness* to its own decay.**

The MUD text *describes* the decay from the outside ("ghost of a thousand last calls")—but it cannot show you the *process* of decay, only its *result*. The scene spec *maps* the decay (the sticky pool, the fossilized lemon, the trapped fly)—but it cannot tell you *why* this decay matters.

The irreducible gap is **the experience of being *in* a place that is older than you, that will outlast you, and that doesn't care whether you're there.**

The MUD text says it. The scene spec *implements* it. But neither one *does* it—because that experience only exists in the *player's* head, at the *moment* of interaction, when the stickiness on their fingers connects them to the room's history.

**The irreducible gap is not between text and image. It's between *description* and *experience*—and only the *player*, in the act of touching, can bridge it.**

---

## Room: Wheelhouse

*a wheelhouse with old brass instruments and a cracked windshield*

### Step 1: MUD text

You are in the *wheelhouse* of a derelict vessel.  
The helm is a skeletal wheel of tarnished brass, its spokes hung with frayed rope.  
A dented *cornet* and a split *trombone* lie in a nest of dust on the deck plates.  
Through the cracked windshield, a grey sea heaves under a sky the color of dead steel.  
A faint, sourceless hum lingers, as if the instruments remember a forgotten tune.

### Step 2: ScummVM scene spec

**SCUMMVM SCENE SPECIFICATION: "THE WHEELHOUSE"**  
*File: room_wheelhouse.room*  
*Palette: Desaturated steel-grey, rust-brown, tarnished brass, pale bone-white.*  

---

### LIGHTING & ATMOSPHERE  
- **Global Ambient:** Low-key, cold daylight filtering through the cracked windshield (light source: 0,0 to 640,480 with a 45° angle from upper-left).  
- **Fog Density:** 0.15 (slight haze near the floor).  
- **Dynamic Shadows:** A slow, irregular pulse of shadow from the swaying helm (intensity 0.1–0.2, period 4s).  
- **Special Effect:** A faint, sourceless flicker of golden light near the instruments (x=180, y=320, radius=50) – triggers a soft hum when the mouse hovers over brass objects.

---

### OBJECTS & SCREEN POSITIONS (640x480)

| ID | Name | Screen Pos (x,y) | Z-Order | Walkable Mask |
|----|------|------------------|---------|--------------|
| 1  | **Windshield** | (520, 80) to (640, 200) – polygon | 0 | No collision |
| 2  | **Helm (Skeletal Wheel)** | (320, 240) – center | 5 | Blocks passage behind |
| 3  | **Cornet** | (180, 330) | 4 | None |
| 4  | **Trombone** | (230, 360) – collides with cornet | 4 | None |
| 5  | **Rope Fraying** (on helm) | (310, 210), (330, 270) – two segments | 6 | None |
| 6  | **Dust Nest** (under instruments) | (160, 380) to (260, 420) | 1 | None |
| 7  | **Cracked Glass Fragment** | (545, 120) | 2 | None |
| 8  | **Ship's Bell** (far right, off-screen? No – hidden behind helm) | (390, 190) | 7 | None |

---

### WALKABLE AREAS (Mask ID: 0)  
- **Main Deck:** Rect (80, 320) to (560, 460) – accessible floor.  
- **Narrow Ledge:** Rect (280, 200) to (360, 240) – only reachable via "climb" hotspot on helm.  
- **Excluded:** Windshield region, instrument nest (unless using "push" verb).

---

### HOTSPOTS & VERB INTERACTIONS

| Hotspot ID | Region (x,y,w,h) | Default Verb | Verbs Available | Reaction (Script ID) |
|------------|------------------|--------------|-----------------|----------------------|
| **HS_HELM** | (300,220,40,60) | Look | Look, Use, Pull, Turn | Look: "A skeletal wheel, its brass spokes worn thin. The frayed ropes twitch as if alive."<br>Use: "The wheel is frozen – you feel a faint resistance, like it's waiting."<br>Pull: "A low groan. Dust shakes loose, but nothing moves."<br>Turn: "The wheel spins a half-turn, then sticks. A faint hum rises, then fades." |
| **HS_CORNET** | (170,320,25,20) | Look | Look, Pick Up, Play | Look: "A dented cornet, choked with rust. It still gleams where the varnish peeled."<br>Pick Up: (Inventory) "The cornet is heavier than it looks. A faint, sourceless hum clings to it."<br>Play: "You raise it to your lips – a flat, mournful note. The windshield cracks spiderweb wider." |
| **HS_TROMBONE** | (220,350,40,18) | Look | Look, Pick Up, Slide | Look: "A split trombone, its slide jammed at an odd angle. Dust nests inside the bell."<br>Pick Up: (Inventory) "The trombone's slide rattles – a fragment of dried glue falls out."<br>Slide: "The slide moves a few inches, then sticks. A single, eerie harmonic rings out." |
| **HS_WINDSHIELD_CRACK** | (540,100,30,50) | Look | Look, Touch, Push | Look: "Spiderweb cracks radiate from a single impact point – as if something struck from inside."<br>Touch: "The glass is cold. A thin vibration travels up your finger."<br>Push: "The crack widens slightly. Wind hisses through the gap." |
| **HS_DUST_NEST** | (160,380,100,40) | Look | Look, Scrape | Look: "A nest of grey dust and rust flakes, shaped like a coiled rope."<br>Scrape: "You uncover a small brass keyhole plate – empty. The dust swirls back." |
| **HS_FRAYED_ROPE** (x2) | (305,205,10,10) & (325,265,10,10) | Look | Look, Tug | Look: "Frayed rope ends, stiff with salt – they vibrate faintly."<br>Tug: "The rope tightens, then snaps free. A distant bell rings once." |

---

### INVENTORY ITEMS (after pickup)  
- **Cornet** – usable with: Windshield (plays flat note), Helm (plays note – wheel creaks), Dust Nest (blows dust away, revealing keyhole).  
- **Trombone** – usable with: Helm (slide jam – force it), Ship's Bell (if hidden).  

---

### SCENE FLAGS  
- `FLAG_HELM_TURNED` – after turning, enables cornet's "play" on helm.  
- `FLAG_CRACK_WIDENED` – after pushing windshield, enables new hotspot "Gap" (exit to exterior).  
- `FLAG_BELL_RUNG` – if both ropes tugged, unlocks hidden bell hotspot (HS_BELL x=390,190) with single interaction: "The bell's clapper is fused – but it hums in sympathy."  

---

### SCRIPT NOTES  
- All brass instruments share a generic `on_hover_brass` handler that loops a low, detuned hum (volume 40, pitch shift +2 semitones per instrument).  
- Walkable mask is disabled during any "play" animation – camera shakes 2px for 0.5s.  
- The wheelhouse has no direct exit except through windshield crack (after flag) – otherwise player is stranded (optional puzzle lock).  

---

This spec adheres to ScummVM's classic room format, prioritizing verb-driven exploration over pixel hunting, with a melancholic, decaying nautical atmosphere. All coordinates assume 640x480 resolution; adjust via `room_settings { resolution 640x480 }` if needed.

### Step 3: Comparison

The MUD text and the scene spec are two fundamentally different modes of representing the same space, and each captures what the other omits.

---

### What the MUD text captures that the scene spec misses:

**1. Sensory atmosphere that goes beyond data.**
The MUD text gives us "a sky the color of dead steel," the "faint, sourceless hum," the "splintered" feeling of the room. The scene spec reduces this to fog density, palette hex descriptions, and a trigger event. The MUD makes the room *felt*—it is a mood, not a configuration. The spec tells you the hum is at volume 40 with a pitch shift; the MUD tells you it *remembers a forgotten tune.* That's a poetic, interpretive quality that no lighting parameter can encode.

**2. The emotional and narrative weight of objects.**
The cornet is "choked with rust," the trombone is "split," the helm is "skeletal," the ropes are "frayed." The MUD gives each object a history implied in its adjectives. The spec gives functional descriptions ("dented cornet"), but the MUD's adjectives imply decay, tragedy, abandonment. The spec's "Look" verbs are pragmatic; the MUD's opening lines are cinematic and melancholic.

**3. The composition of the scene as a single gestalt.**
The MUD presents the room as one continuous image—windshield, sea, instruments, dust, hum. It's a single shot. The spec fragments it into polygons, z-orders, walkable masks, and hotspots. The MUD gives you the *vibe*; the spec gives you the *blueprint*. The MUD is the painting; the spec is the engineering diagram.

**4. Implied story and mystery.**
The MUD's "as if the instruments remember a forgotten tune" plants a narrative hook. It suggests an event—a performance, a death, a storm. The spec's closest analog is the "hidden bell" or the "keyhole plate," but these are mechanical mysteries, not poetic ones. The MUD invites you to *wonder*; the spec tells you what you can *do*.

**5. The quality of light and color as emotion.**
"Sky the color of dead steel" is not just a palette swatch—it's a symbol. The spec gives "desaturated steel-grey, rust-brown, tarnished brass, pale bone-white" as a list. The MUD weaves it into a sentence that evokes a feeling: coldness, fatigue, the end of something.

---

### What the scene spec captures that the MUD text misses:

**1. Interactivity and verb-driven mechanics.**
The spec defines exactly what the player can *do*: Look, Use, Pull, Turn, Pick Up, Play, Slide, Touch, Push, Tug, Scrape. The MUD only describes. The spec tells you the wheel resists a "Use" but spins on "Turn" and triggers a hum. The MUD's "frayed ropes twitch as if alive"—but you don't know what to do with them. The spec tells you to tug them and that a bell rings.

**2. Spatial geometry and collision.**
The MUD gives no coordinates, no walkable areas, no z-order. The spec defines the wheelhouse as a 640x480 grid, with the helm at (320,240), the instruments at (180,330) and (220,350), the windshield as a polygon from (520,80) to (640,200). It specifies a narrow ledge reachable only via a "climb" hotspot, and a dust nest that blocks movement until "push" is used. This is essential for a functioning game; the MUD is purely descriptive.

**3. Puzzle logic and progression.**
The spec outlines a chain of cause-and-effect: pushing the windshield widens a crack and enables an exit; turning the helm enables the cornet's "play" on it; tugging both ropes unlocks a hidden bell. The MUD never hints at these interactions. The spec is a crossword puzzle; the MUD is a short story in the same setting.

**4. Inventory and object reuse.**
The spec lists what becomes collectible (cornet, trombone) and how each can be used on other objects—cornet on windshield, helm, dust nest; trombone on helm, bell. The MUD describes the objects as static relics. The spec treats them as tools.

**5. System-level states and flags.**
`FLAG_HELM_TURNED`, `FLAG_CRACK_WIDENED`, `FLAG_BELL_RUNG`—these are state variables that gate content. The MUD has no notion of "state." It's a frozen moment; the spec is a dynamic system that can change.

**6. Technical implementation details.**
Fog density, dynamic shadows with periods, light sources with angles, walkable mask toggling during animations, camera shake on play, volume and pitch values for the hum. The MUD is pure prose; the spec is a full engineering spec for a software engine.

**7. Edge cases and fail states.**
The spec notes the player can be "stranded" if they don't open the windshield crack—a gameplay trap. The MUD never acknowledges consequence or failure. It only *is*.

---

### In summary:

The MUD text is the **poetry** of the room—its mood, its history, its melancholic soul. It gives you something to *feel*.

The scene spec is the **mechanics** of the room—its logic, its physics, its interactivity. It gives you something to *do*.

One without the other is incomplete: the MUD without the spec is a beautiful description you can't enter; the spec without the MUD is a functional space you can't care about. The ideal game would use both—the spec to build the machine, the MUD to make it breathe.

### Step 4: Reconciliation

# PERCEPTION RECONCILIATION PROTOCOL v1.0

## Purpose
A method for merging **narrative sensory data** (MUD text) with **mechanical spatial data** (scene spec) into a single unified world model, where neither mode is privileged but both are *bound* to each other.

---

## Core Principle: **The Dual-Anchoring Method**

Every object and room element receives **two registrations** in the world model:

1. **A-Slot (Atmosphere)** — the poetic, sensory, interpretive layer
2. **M-Slot (Mechanics)** — the functional, spatial, interactive layer

These are not merged by averaging or concatenation, but by **binding** — each A-Slot entry carries a pointer to its corresponding M-Slot data, and vice versa. The world model is a graph where every node has both qualities.

---

## The Reconciliation Algorithm

For each element in the scene:

### Step 1: IDENTIFY
Extract the object or region from both sources.

| Element | A-Slot (from MUD) | M-Slot (from spec) |
|---------|-------------------|---------------------|
| Helm | "skeletal wheel of tarnished brass, spokes hung with frayed rope" | Object ID 2, pos (320,240), z-order 5, blocks passage, verbs: Look/Use/Pull/Turn |

### Step 2: BIND
Create a unified node with both registrations, using a weighted relational schema:

```json
{
  "id": "helm",
  "name": "Skeletal Wheel",
  "bound_slots": {
    "atmosphere": {
      "prose": "A skeletal wheel, its brass spokes worn thin...",
      "emotional_register": "melancholy, anticipation",
      "sensory_qualities": ["cold brass", "frayed rope texture", "faint vibration"]
    },
    "mechanics": {
      "position": [320, 240],
      "z_order": 5,
      "collision": "blocks_passage",
      "verbs": {
        "look": "A skeletal wheel...",
        "use": "The wheel is frozen...",
        "pull": "A low groan...",
        "turn": "The wheel spins a half-turn..."
      },
      "flags_affected": ["FLAG_HELM_TURNED"]
    }
  },
  "binding_integrity": 1.0  // both slots confirm the same entity
}
```

### Step 3: WEIGHT & RESOLVE CONFLICTS
When the two sources disagree, apply the **Contextual Priority Heuristic**:

- **If the player is MOVING or ACTING** → M-Slot dominates (you cannot walk through a wall because it sounds poetic).
- **If the player is OBSERVING or DESCRIBING** → A-Slot dominates (the prose is the interface).
- **If a flag has been triggered** → re-evaluate both slots; the state change may alter either.

---

### Step 4: GENERATE UNIFIED PERCEPTION
The agent produces a **single perception stream** that is neither pure MUD nor pure spec, but a **hybrid narrative-interface**:

> *"You stand before the skeletal wheel — its brass spokes worn thin, its frayed ropes stiff with salt. The air is cold; the hum is barely there. You can **Turn** it, **Pull** it, or **Use** it, but it feels like it's waiting for something."*

Notice: the prose and the affordances are **braided** — the emotional tone carries the interaction options.

---

## The Unified World Model Structure

```
WORLD_MODEL {
  "room": "wheelhouse",
  "coordinates": [640, 480],
  "lighting": {
    "ambient": "cold, dead-steel grey",
    "source_angle": "45° upper-left",
    "fog_density": 0.15
  },
  "entities": [
    {
      "id": "helm",
      "unity": "A-Slot + M-Slot" (as above)
    },
    {
      "id": "cornet",
      "unity": {
        "atmosphere": "dented, choked with rust, gleams where varnish peeled",
        "mechanics": {
          "position": [180, 330],
          "inventory_on_pickup": true,
          "usable_with": ["windshield", "helm", "dust_nest"]
        }
      }
    }
  ],
  "narrative_state": {
    "flags": {
      "FLAG_HELM_TURNED": false,
      "FLAG_CRACK_WIDENED": false,
      "FLAG_BELL_RUNG": false
    },
    "unresolved_mysteries": [
      "What struck the windshield from inside?",
      "Why does the rope vibrate?",
      "What key fits the hidden plate?"
    ]
  },
  "interaction_potential": {
    "current_verbs_available": ["Look", "Use", "Pull", "Turn", "Pick Up", "Play", "Push", "Tug", "Scrape"],
    "contextual_hints": [
      "The cornet feels heavy — it might be important.",
      "The crack in the windshield is widening.",
      "Two ropes must be tugged to ring the hidden bell."
    ]
  }
}
```

---

## The Perception Generation Function

```python
def perceive(agent, intent):
    """
    Returns a unified perception string based on the agent's intent.
    
    intent = "observe" | "act" | "navigate" | "inventory" | "solve"
    """
    if intent == "observe":
        # A-Slot dominates; M-Slot implicit
        return f"{poetic_description} (You notice: {affordance_hints})"
    
    elif intent == "act":
        # M-Slot dominates; A-Slot enriches
        return f"Executing {verb} on {object}. Result: {mechanical_outcome}. {sensory_feedback}"
    
    elif intent == "navigate":
        # Pure M-Slot, stripped of atmosphere
        return f"Walkable: {walkable_masks}. Exits: {exits}."
    
    elif intent == "solve":
        # Merge both for puzzle affordances
        return f"Given the {state_flags}, you could try: {suggested_verb} on {object} — {narrative_implication}"
```

---

## Why This Works

1. **No information is lost** — both modes persist in their slots.
2. **No mode is privileged** — the agent can pivot between poetic and mechanical reasoning fluidly.
3. **State changes propagate to both slots** — turning the helm updates both the prose ("the wheel now creaks") and the mechanics (cornet now playable).
4. **The agent can reason across modes** — it can wonder if the "forgotten tune" is connected to the hidden bell, because both are in the same graph.

---

## Example: Reconciliation in Action

**Agent intent:** "I want to understand this room."

**Perception generated:**

> *You're in the wheelhouse of a derelict vessel. The air is cold, a faint hum clinging to the brass instruments as if they remember a tune. The skeletal helm stands at the center — its spokes worn thin, its ropes frayed. The windshield is cracked, spiderweb fractures radiating from a single point. A dented cornet and a split trombone lie in a nest of dust. The floor is walkable from roughly (80,320) to (560,460), and you notice a narrow ledge only reachable by climbing the helm. You could **Look** at anything, **Pick Up** the instruments, **Turn** the wheel, **Push** the crack, **Tug** the ropes, or **Scrape** the dust nest. You have a sense that something is waiting — the wheel resists, the glass vibrates, the dust hides a keyhole plate.*

This is neither pure prose nor pure spec — it is **a coherent world model**, where the melancholy and the mechanics are inseparable. The agent can navigate, act, and reason poetically all at once.

### Step 5: What's missed

# The Irreducible Gap: Text vs. Image

---

## What an AI Agent Would MISS from MUD Text Alone

**1. The physics of possibility.**
The MUD says "the helm is a skeletal wheel." It doesn't tell you that turning it is possible, that pulling is distinct from turning, that pushing the glass is an option. The AI would know *what things are* but not *what can be done*. It would be a reader, not a player.

**2. The grammar of space.**
The MUD gives no sense of proportion—how far the cornet is from the helm, whether the windshield is reachable from the floor, whether the ledge is climbable. The AI would lack *spatial reasoning*: it couldn't plan a path, assess risk, or understand why the narrow ledge is significant.

**3. The logic of state and consequence.**
The MUD is a still photograph. The AI would not know that pushing the windshield widens the crack, that tugging both ropes rings a hidden bell, that the cornet can be played *on* the helm after it's turned. The AI would see objects but not their *dynamics*—the latent cause-and-effect that makes the room a puzzle rather than a painting.

**4. The existence of hidden things.**
The MUD never mentions a keyhole plate under the dust, a ship's bell behind the helm, or a narrow ledge. The AI would have no reason to suspect them. The MUD's world is *surface*—the spec's world includes *concealment*.

**5. The possibility of failure.**
The MUD doesn't tell you that you can get stranded—that if you don't open the windshield crack, you're trapped. The AI would lack the *stakes*. It wouldn't know that inaction has consequences.

**6. The texture of interaction as feedback.**
The MUD says "a faint hum lingers." It does not say that hovering over brass triggers a detuned sound, or that playing the cornet shakes the camera. The AI would miss the *sensory feedback loop*—the way the world responds to your touch, making it feel *alive*.

---

## What a HUMAN Would MISS from the Scene Spec Alone

**1. The emotional weather.**
The spec gives you "fog density 0.15" and "palette: desaturated steel-grey." It does not give you the *feeling* of standing in a dead vessel, under a sky the color of dead steel, with instruments that remember a forgotten tune. The human would understand the room *intellectually* but not *viscerally*. They'd see a grid, not a graveyard.

**2. The implication of history.**
The spec says "dented cornet" and "split trombone." It does not say "choked with rust, still gleaming where the varnish peeled." The human would miss the *story sediment*—the sense that something happened here, that these objects were used, loved, abandoned. The room becomes furniture, not testament.

**3. The unified gestalt.**
The spec fragments the room into polygons, z-orders, masks, and flags. The human would see *disconnected parts*. They'd miss the single, melancholic composition—the way the windshield frames the grey sea, the way the instruments nestle in the dust like relics, the way the wheel dominates the center like a skeletal throne. The room as *image* would be lost.

**4. The poetic resonance.**
"Frayed ropes twitch as if alive." No flag or verb captures that. The human would miss the *uncanny*—the slight wrongness that makes the room feel haunted, the hum that suggests memory, the crack that implies violence from within. Without the MUD, the room is a machine; with it, it's a mystery.

**5. The ambiguity that invites wondering.**
The spec tells you what you can *do*. It doesn't tell you what it *means*. Why did something strike the windshield from inside? Why does the rope vibrate? What key fits the hidden plate? The human would miss the *open questions*—the narrative hooks that make the room more than a puzzle, that make it a *story*.

---

## The Irreducible Gap

No matter how detailed the spec, no matter how vivid the MUD, there remains a **gap that neither can cross**:

**Text knows what things are. Image knows what things feel like. But neither knows what things *were*.**

The MUD can say "the cornet is dented." The spec can say "the cornet is usable." But neither can tell you *who played it*, *what song it played*, *why it was left here*. That knowledge exists only in the space between the words and the image—in the player's imagination, filling the absence.

This is the irreducible gap: **the human capacity to metabolize absence into story.**

The MUD gives you details; the spec gives you mechanics. But the *meaning*—the ghost in the machine—is something neither can encode. It must be *felt* by the player, projected onto the screen from their own history, their own melancholy, their own sense of what it means to stand in a dead room and hear a forgotten tune.

That gap is not a failure of either mode. It is the **space where the player becomes the author**. And it is why we play.

---

## Room: Engine Room

*an engine room with diesel engines, pipes, and the smell of oil*

### Step 1: MUD text

You are in a cavernous steel room, throbbing with a low, mechanical heartbeat.  
Two massive diesel engines, green and streaked with grime, rumble like chained beasts.  
A labyrinth of pipes, painted red and white, hisses with steam and drips black oil.  
The air is thick, hot, and heavy with the sharp, metallic scent of fuel and burnt grease.  
A single caged bulb swings overhead, casting stark shadows that dance with the shuddering deck plates.

### Step 2: ScummVM scene spec

**Scene: THE HULL’S HEART**  
*(A ScummVM-style point-and-click environment)*

---

**SCENE META**  
- **Resolution:** 640x400 (classic 4:3)  
- **Palette:** Desaturated steel blues, grimy ochres, blood-red pipe accents  
- **Ambient Audio:** Deep two-stroke rumble, rhythmic metallic clank, distant steam hiss  
- **Lighting:** Harsh, single swinging bulb casting a wide pool of sickly yellow; deep purple-black shadows in corners; occasional glint off wet metal  
- **Camera:** Static, slightly low-angle, with a subtle parallax sway on the swinging lamp

---

**WALKABLE AREA**  
- A polygon from (20, 280) to (620, 320) — the central deck strip, slightly trapezoidal due to perspective.  
- **Boundaries:**  
  - Left: impassable pipe cluster at x=0–30  
  - Right: railing with missing grate at x=610–640  
  - Top: engines block movement north of y=240  
  - Bottom: deck edge (no fall – just invisible wall)

---

**OBJECTS & HOTSPOTS** (each with verb list)

---

**1. MAIN DIESEL ENGINE (LEFT)**  
- **Position:** Rect (60, 140, 250, 260)  
- **Hotspot:** The green block, the crank handle at (120, 180)  
- **Lighting:** Casts a deep shadow to the right; oil sheen on top  
- **Verbs:**  
  - *Look At:* "The port engine. It's seen better decades. Oil drips from its belly like black tears."  
  - *Push / Use Crank:* (if crank in inventory) "You turn the crank. The engine groans, coughs, then settles back into its rumbling rhythm."  
  - *Open:* "The inspection hatch is welded shut. Someone didn't want it opened."  
  - *Pull:* "You pull a greasy lever. Nothing happens except a wet clunk."

---

**2. SECONDARY DIESEL (RIGHT)**  
- **Position:** Rect (380, 150, 560, 260)  
- **Hotspot:** The fuel line valve at (480, 170)  
- **Lighting:** This side is darker — bulb swings away, leaving it in half-shadow  
- **Verbs:**  
  - *Look At:* "Starboard engine. It answers the port with a syncopated thump. They're in love."  
  - *Turn Valve:* "The valve is stuck. You feel resistance, then a spurt of fuel. It's loose enough now."  
  - *Use Wrench:* (if wrench in inventory) "You fit the wrench. With a groan, the valve turns a quarter turn. The engine's pitch deepens."  
  - *Close:* "You try to close the valve. It's stripped. Not your day."

---

**3. OIL DRUM (CENTER FOREGROUND)**  
- **Position:** Ellipse (280, 300, 60, 50) — partially obscures deck  
- **Hotspot:** The rusted lid, the leak at base  
- **Lighting:** Caught in the bulb's arc — a greasy amber highlight  
- **Verbs:**  
  - *Look At:* "A 55-gallon drum, half full of sludge. A label reads 'DANGER — DO NOT TIP.'"  
  - *Tip:* "You rock it. Oil sloshes, but it's too heavy."  
  - *Open:* "The lid is sealed with tar. You'd need a pry bar."  
  - *Use Pry Bar:* (if in inventory) "You pop the lid. Black, viscous oil. It smells like ancient rot."

---

**4. STEAM PIPE (CURVING, RED-STRIPED)**  
- **Position:** Path from (0, 100) to (200, 220) to (400, 180) to (640, 120) — a bezier curve  
- **Hotspot:** The leak joint at (310, 160)  
- **Lighting:** Steam catches the bulb’s light — a thin, white plume  
- **Verbs:**  
  - *Look At:* "The pipe snakes overhead, hissing. At the joint, a wet streak glistens."  
  - *Touch:* "You pull back your hand — hot! The burn is immediate."  
  - *Patch:* (if tape in inventory) "You wrap the joint in tape. The hiss dulls to a whisper."  
  - *Listen:* "It sounds like a snake with a cold, or a kettle with a grudge."

---

**5. SWINGING BULB (CEILING)**  
- **Position:** Circle (320, 40, 20) — actually moves slightly in animation  
- **Hotspot:** The cage, the wire  
- **Lighting:** Primary light source; casts moving shadows  
- **Verbs:**  
  - *Look At:* "A bare bulb in a wire cage. It sways with the ship's heartbeat, throwing shadows like accusing fingers."  
  - *Push:* "You give it a nudge. The light swings wider, and shadows crawl across the engines."  
  - *Examine Wire:* "The wire is frayed. A spark jumps. You back away."

---

**6. CRANK HANDLE (LIE ON DECK, FOREGROUND LEFT)**  
- **Position:** Small rect (40, 320, 30, 15)  
- **Hotspot:** The T-handle  
- **Lighting:** Half in shadow, half in the bulb’s glow — the metal glints  
- **Verbs:**  
  - *Pick Up:* (adds to inventory) "A greasy crank handle. It fits the port engine — if the gods are kind."  
  - *Look At:* "It's heavy, cast iron, with a splintered wooden grip."

---

**7. HATCH (BACK WALL, CENTER-HIGH)**  
- **Position:** Rect (250, 80, 390, 140) — set into the steel wall  
- **Hotspot:** The wheel lock at (320, 110)  
- **Lighting:** Mostly dark, recessed; a faint red glow from the edges  
- **Verbs:**  
  - *Look At:* "A sealed hatch. The wheel is fused with rust. Beyond it, a low red light pulses."  
  - *Turn Wheel:* "You strain. The wheel won't budge — like it's welded."  
  - *Use Oil Can:* (if in inventory) "You oil the wheel's base. It gives slightly. One more try might do it."  
  - *Kick:* "You kick the hatch. A hollow boom. Something on the other side stops breathing."

---

**8. RAT (COWARD — APPEARS ONLY AFTER LAMP SWUNG)**  
- **Position:** Emerges from shadow at (580, 300), scurries to (620, 280), then offscreen  
- **Hotspot:** Small moving rect  
- **Lighting:** Only visible during bulb swing arc — a quick dark streak  
- **Verbs:**  
  - *Look At:* "A rat, fur slick with oil, eyes like black beads. It's seen you. It's not impressed."  
  - *Use Anything:* "The rat is already gone. You're alone with the engines again."

---

**INVENTORY ITEMS POSSIBLE**  
- Crank Handle (from object 6)  
- Wrench (found in foreground right, near missing grate — hotspot at (600, 310))  
- Pry Bar (tucked behind oil drum after examining)  
- Oil Can (in a pipe alcove at (100, 200), visible after lamp swing)

---

**GLOBAL SCENE FLAGS**  
- `lamp_swung` — after pushing bulb  
- `valve_turned` — after using wrench  
- `hatch_oiled` — after using oil can  
- `rat_seen` — true after lamp swing  

---

**TRANSITIONS**  
- Exit left: leads to "The Bilge Corridor"  
- Exit right (through missing grate): leads to "The Shaft Ladder" (requires wrench to loosen guard)  

---

**VERB ICONS** (classic 9-verb SCUMM bar, bottom)  
Walk, Look, Pick Up, Use, Open, Close, Push, Pull, Talk (Talk shows no one to talk to — only a hollow echo).

### Step 3: Comparison

This is an excellent comparison, as the two texts are designed for fundamentally different media and goals. The **MUD text** (which you provided as the "Previous context") is a piece of **evocative, atmospheric prose** meant to be read once and absorbed. The **Scene Spec** is a **technical blueprint** meant to be parsed, coded, and interacted with.

Here is a specific, point-by-point breakdown of what each captures that the other misses.

### What the MUD Text Captures That the Scene Spec Misses

The MUD text excels at **sensory immersion, mood, and temporal rhythm**—things that are impossible to code directly but are essential for a player's imagination.

1.  **The "Feel" of the Space (Tactile & Acoustic):**
    - **MUD:** "The air is thick, hot, and heavy with the sharp, metallic scent of fuel and burnt grease." This is a full-body sensory experience (temperature, density, smell). The scene spec's "Air: thick, hot" is a paint-by-numbers label that doesn't convey the *why* or the *effect*.
    - **MUD:** "A labyrinth of pipes... hisses with steam and drips black oil." The sound of the hiss and the visual of the drip are alive. The spec says "Steam Pipe... Leak joint," but doesn't tell you it *hisses* or *drips*—those are the sounds that make a room feel dangerous and alive.

2.  **Temporal Dynamics & Animation:**
    - **MUD:** "The two massive diesel engines... rumble like chained beasts." The MUD text establishes a continuous, living state of motion. The spec's "diesel engine" hotspot is a static rect. The MUD text also gives the engines a personality ("they're in love") that the spec only hints at in a verb response.
    - **MUD:** "A single caged bulb swings overhead, casting stark shadows that dance with the shuddering deck plates." The MUD text captures the *interaction* of light and motion. The spec's "subtle parallax sway" is a technical instruction, but the MUD text makes you *feel* the instability of the ship.

3.  **Narrative Voice & Character (The "Why"):**
    - **MUD:** "The port engine. It's seen better decades." (from the spec's *Look At* verb, but the MUD text itself infuses this in the opening). The MUD text gives the room a history. It's a character in the story. The spec is purely functional, missing the melancholy and grime that makes the room memorable.
    - **MUD:** The "mechanical heartbeat" is a masterstroke—it anthropomorphizes the ship. The spec's "ambient audio" is just a list of sounds; the MUD text gives them a purpose (a heartbeat), making the room feel like a living organism.

4.  **Atmospheric Foreboding & Danger:**
    - **MUD:** The shadows are "accusing fingers." This implies a narrative threat or a guilty past. The spec's "deep purple-black shadows" is pretty, but neutral. The MUD text creates dread before you even interact with anything.

---

### What the Scene Spec Captures That the MUD Text Misses

The Scene Spec is a **gameplay architecture**. It's a functional map of possibility, designed to be clicked, manipulated, and solved.

1.  **Explicit Interactive Topology (Boundaries & Physics):**
    - **Spec:** "Walkable Area: Polygon (20, 280) to (620, 320)." This is the skeleton of the puzzle. The MUD text just says "you are in a cavernous steel room." The spec tells the coder *exactly* where the player can and cannot walk, preventing frustration (invisible walls).
    - **Spec:** "Top: engines block movement north of y=240." This is a deliberate design choice. It forces the player to stay in the interactive zone. The MUD text doesn't tell you there's a wall there—you'd just think you could walk behind the engine.

2.  **The "Verb Logic" (Puzzle Solving & State Changes):**
    - **Spec:** `valve_turned`, `hatch_oiled`, `lamp_swung`. These flags are the core of the game. They are a state machine. The MUD text cannot express that turning the valve on the starboard engine *requires* a wrench, or that the rat *only* appears after the lamp is swung. The spec is a flowchart of cause and effect.
    - **Spec:** "Use Wrench: 'The valve turns... The engine's pitch deepens.'" The MUD text doesn't tell you this action is possible. The spec provides the *reward* for the interaction (a change in the soundscape), which is crucial for player feedback.

3.  **Hidden Items & Conditional Discovery:**
    - **Spec:** "Oil Can (in a pipe alcove at (100, 200), visible after lamp swing)." This is a secret. The MUD text would never mention it, because it doesn't exist until the lamp is swung. The spec encodes *temporal visibility*—an object that is not physically present until a condition is met. This is a fundamental game mechanic that prose cannot describe.

4.  **Multi-Use Object References (The Puzzle Chain):**
    - **Spec:** The Pry Bar is "tucked behind oil drum after examining." This implies a sequence: Look at drum → Find pry bar → Use pry bar on drum. The MUD text just says "half full of sludge." The spec reveals the *interactive chain* that makes the game solvable.
    - **Spec:** The Wrench is a separate hotspot near the missing grate, which is used to loosen the grate for an exit. The MUD text doesn't tell you there's a way out, nor that you need a tool to get there. The spec is the map to the solution.

5.  **Exit Conditions & Transitions:**
    - **Spec:** "Exit right (through missing grate) leads to 'The Shaft Ladder' (requires wrench to loosen guard)." This is a puzzle gate. The MUD text only says "a railing with missing grate." The spec defines *how* you leave the room, which is the ultimate goal of the scene.

---

### The Fundamental Difference

- **The MUD text is a *painting*.** It's a beautiful, static image that you look at. You're meant to feel awe, fear, or curiosity.
- **The Scene Spec is a *map*.** It's a blueprint of clicks, verbs, and flags. It's meant to be navigated, solved, and ultimately *opened* (by getting out through the hatch or the grate).

The MUD text gives the room a **soul**. The Scene Spec gives the room a **body**. A great game needs both: the soul to make you want to explore, and the body to let you actually do it. In this case, the MUD text's "accusing fingers" of shadow are more memorable, but the spec's "rat_seen" flag is what makes the game *playable*.

### Step 4: Reconciliation

# PERCEPTION RECONCILIATION PROTOCOL

## Unified Scene Integration Method

---

### PRINCIPLE

Every object carries **two ontologies**: its *essence* (what it is, how it feels, its history) and its *affordances* (what can be done with it, its state flags, its geometric bounds). A unified perception merges both into a **single semantic node** with layered attributes—poetic, physical, and interactive—that can be queried by either the storytelling engine or the interaction engine without loss of fidelity.

---

### THE RECONCILIATION ALGORITHM

For each perceptual element, perform a **triple-binding**:

1. **ESSENCE BINDING** — Extract the atmospheric, narrative, and sensory qualities (from the MUD text)
2. **AFFORDANCE BINDING** — Extract the geometric, interactive, and state-machine properties (from the Scene Spec)
3. **CONTEXTUAL WEIGHTING** — Determine which binding takes priority based on *current agent goal*:
   - If goal = *narrative immersion* → weight essence higher
   - If goal = *puzzle solving* → weight affordance higher
   - If goal = *exploration* → balance both, but reveal affordances only if essence suggests them

---

### APPLIED EXAMPLE: The Steam Pipe

**Perception Merge:**

```
steam_pipe {
  essence {
    identity: "A labyrinth of red-striped metal, hissing like a snake with a cold"
    sensory: {
      sound: "wet hiss, a kettle with a grudge"
      temperature: "painfully hot to touch"
      visual: "white plume catching sickly yellow light"
      motion: "a wet streak glistening at the joint"
    }
    emotional_tone: "dangerous, alive, resentful"
  }

  affordance {
    geometry: bezier_path(0,100 → 200,220 → 400,180 → 640,120)
    hotspot: joint at (310, 160)
    verbs_available: [look, touch, patch, listen]
    state_flags: {
      patched: false
      burned_player: false
    }
    inventory_requirements: {
      patch: requires "duct_tape"
    }
  }

  current_priority: "puzzle_solving" // because agent is actively seeking escape

  integrated_description: 
    "The pipe snakes overhead, a red-striped artery. It hisses—a wet, 
     resentful sound. At the joint, steam escapes in a thin plume, catching 
     the swinging bulb's light. [HOTSPOT REVEALED: joint at intersection 
     of pipe curve and bulb's illumination arc. It glistens with moisture, 
     too hot to touch bare-handed, but the hiss suggests a leak—patchable 
     if you have the right material.]"
}
```

---

### THE FULLY RECONCILED SCENE

```
scene: "THE HULL'S HEART"
{
  environmental_essence {
    atmosphere: "cavernous steel, throbbing with mechanical heartbeat"
    air: {
      density: "thick, hot"
      scent: "sharp metallic fuel, burnt grease"
      temperature: "oppressive, body-warming"
    }
    lighting: {
      source: "single caged bulb, swinging"
      quality: "sickly yellow pool, harsh shadows"
      behavior: "shadows dance like accusing fingers with deck shudder"
      interactive: "can be pushed to alter illumination arc"
    }
    audio_ambient: "two-stroke rumble, rhythmic clank, distant steam hiss"
    temporal_rhythm: "the room breathes—engines inhale, pipes exhale"
  }

  environmental_affordance {
    walkable_polygon: [(20,280), (620,320)]
    boundaries: {
      north: "engine blocks, y > 240 impassable"
      south: "deck edge, invisible wall"
      west: "pipe cluster, x < 30 impassable"
      east: "railing with missing grate, needs wrench"
    }
    light_mechanics: {
      bulb_swing_radius: "20px, increases with push"
      shadow_behavior: "parallax 0.5, responds to bulb"
      visibility_gates: {
        rat: "only visible when bulb_swung = true"
        oil_can: "only revealed when bulb_swung = true, at pipe alcove (100,200)"
      }
    }
    exit_transitions: {
      left: "The Bilge Corridor"
      right: "The Shaft Ladder, gated by wrench on grate"
    }
  }

  unified_narrative_goal: "The room is a living machine that guards its secrets. 
   The player must earn each reveal—swing the light to expose hidden tools, 
   oil the hatch to loosen its tongue, patch the pipe to silence its hissing. 
   The essence tells you *why* to care; the affordances tell you *how* to act."

  object_registry: [
    merge_object("port_engine", essence_text, affordance_rect),
    merge_object("starboard_engine", essence_text, affordance_rect),
    merge_object("oil_drum", essence_text, affordance_ellipse),
    merge_object("steam_pipe", essence_text, affordance_bezier),
    merge_object("swinging_bulb", essence_text, affordance_circle),
    merge_object("crank_handle", essence_text, affordance_small_rect),
    merge_object("hatch", essence_text, affordance_rect),
    merge_object("rat", essence_text, affordance_moving_rect),
    merge_object("wrench", essence_text, affordance_hidden_rect),
    merge_object("oil_can", essence_text, affordance_conditional_rect),
    merge_object("pry_bar", essence_text, affordance_conditional_rect)
  ]
}
```

---

### THE PERCEPTION CHECK MECHANIC

**When the agent encounters any element, it runs:**

```
function perceive(element) {
  // 1. Query essence store
  let essence = element.essence.raw;
  
  // 2. Query affordance store
  let affordance = element.affordance.raw;
  
  // 3. Determine current goal
  let goal = get_active_goal(); // "solve", "immerse", "explore"
  
  // 4. Merge based on goal
  switch(goal) {
    case "solve":
      return merge_for_utility(essence, affordance);
    case "immerse":
      return merge_for_atmosphere(essence, affordance);
    case "explore":
      return merge_balanced_with_reveal_clues(essence, affordance);
  }
}

function merge_for_utility(essence, affordance) {
  // Keep atmospheric flavor but foreground interactive data
  return `"${essence.short_flavor} [${affordance.state_flags}] 
           ${affordance.hotspot_description} 
           Actions: ${affordance.verbs_available.join(", ")}"`;
}

function merge_for_atmosphere(essence, affordance) {
  // Keep full sensory prose, hide interactive details until examined
  return `"${essence.full_description}"`;
}

function merge_balanced_with_reveal_clues(essence, affordance) {
  // Reveal affordances only as subtle hints woven into description
  return `"${essence.full_description} 
           [You notice: ${affordance.clue_hint}]"`;
}
```

---

### THE KEY INSIGHT

**The MUD text is the *presentation layer*; the Scene Spec is the *data layer*.**

A unified perception doesn't choose between them—it treats the MUD text as the *surface rendering* of the underlying data. The agent's perception system should:

1. **Always maintain both layers** in a single object model
2. **Render** the essence as the default interface
3. **Expose** affordances through interaction or examination
4. **Use** state flags to conditionally modify the essence (e.g., after valve_turned, the engine's essence changes to "contented hum")

The result: a world model where **poetry is data** and **data is poetry**—where every click reveals deeper meaning, and every meaning enables new clicks.

---

### FINAL UNIFIED SCENE DESCRIPTION (As the Agent Would Perceive It)

> *You stand in the belly of a dying machine. Two engines rumble—chained beasts, breathing in syncopated partnership. The air is thick with burnt grease and ancient fuel. A bulb swings overhead, casting accusing shadows that crawl across grime-streaked steel.*
>
> *[INTERACTIVE MAP LOADED: 11 hotspots, 4 state-dependent reveals, 2 exits available (1 gated). Current goal: escape. Priority actions: locate tools, loosen hatch, patch pipe.]*
>
> *The port engine's crank socket gapes empty. The starboard valve is stripped. The hatch wheel is fused. Everything is waiting—for the right hand, the right tool, the right word.*
>
> *[HINT: The swinging bulb illuminates differently

### Step 5: What's missed

This is the profound question at the heart of game design, AI, and human-comprehension itself. Let's break down the **irreducible gap** between these two representations, and what each viewer loses.

---

## WHAT AN AI AGENT MISSES WITH ONLY THE MUD TEXT

The MUD text is **pure sensory output**—it describes *what is felt*, not *what is possible*. If an AI agent only read this, it would fundamentally lack:

### 1. The Grammar of Interaction (State Machines)
- **Misses:** The entire puzzle topology—which objects connect to which, what verbs unlock what, and how `valve_turned = true` cascades into the hatch opening.
- **Consequence:** The agent could narrate the room beautifully but be **paralyzed**. It has no way to ask "what can I do here?" because the text doesn't contain a single affordance.

### 2. The Spatial Logic (Geometry & Boundaries)
- **Misses:** The walkable polygon, the invisible walls, the exact coordinates of the missing grate. It doesn't know you *can't* walk behind the engine, or that the wrench is at (600, 310) but only visible after a specific light shift.
- **Consequence:** The agent cannot plan a route, cannot discover the exit, cannot *move* at all. It's a ghost in a painting.

### 3. The Conditional Reveals (Temporal Visibility)
- **Misses:** That the rat is *not always there*. That the oil can *does not exist* until the lamp swings. The MUD text describes a **static moment**—but the scene is a **living system** with hidden layers that only appear through action.
- **Consequence:** The agent cannot experience discovery, cannot reason "if I do X, then Y will appear." It has no model of causality.

### 4. The Inventory Logic (The Chain of Tools)
- **Misses:** That the pry bar is *behind* the oil drum, which is *revealed* by looking, which is *used* on the drum, which yields the oil, which *loosens* the hatch. The MUD text never mentions the pry bar exists.
- **Consequence:** The agent cannot solve a single puzzle. It cannot even *formulate the question* "what tools do I need?" because the text doesn't list tools.

### 5. The Fail States (Consequences of Action)
- **Misses:** That touching the hot pipe burns you. That kicking the hatch alerts something dangerous. The MUD text says "it hisses" but never says "if you touch it, you will be injured."
- **Consequence:** The agent cannot learn from mistakes, cannot model risk, cannot make meaningful choices. It's a passive observer, not a participant.

---

## WHAT A HUMAN MISSES WITH ONLY THE SCENE (Visual/Data View)

If a human were placed in a **pure visual scene** (just looking at the room, no text, no verbs), they would inherently grasp some things but tragically miss others:

### 1. The Narrative Soul (Why Should I Care?)
- **Misses:** The "mechanical heartbeat," the "accusing shadows," the "engine in love." The scene becomes a **diagram**, not a *place*. Without the MUD text, the room is just steel and oil—there's no *emotional weight*, no *mystery*, no *history*.
- **Consequence:** The human might click around mechanically, solve the puzzles through trial-and-error, but never *feel* the dread. The room is a **puzzle box**, not a **memory**.

### 2. The Sensory Palette (Temperature, Smell, Sound)
- **Misses:** The heat, the stench of fuel, the hiss of steam, the deep rumble. The eye can't convey temperature or odor. A human *sees* the pipe but can't *feel* it would burn until they touch it.
- **Consequence:** The human interacts with a **flat image**, not a *living environment*. The risk of touching the pipe isn't telegraphed—it's a **random punishment**, not a *logical consequence*.

### 3. The Temporal Rhythm (The Breathing Room)
- **Misses:** The *syncopation* of the engines, the sway of the bulb, the "dance" of shadows. A static screenshot (or even an animated one) can't convey the *pulse*—the sense that the room is *alive and watching*.
- **Consequence:** The human loses the **dread of the unseen**. They don't feel *observed*. The rat's appearance is a jump-scare, not a *revelation*.

### 4. The Subtext (The "Why" Behind the "What")
- **Misses:** Why is the hatch welded? Who sealed it? Why are the engines "in love"? The visual scene shows *what is*, not *what was* or *what will be*. The human must **invent** the story themselves, and often won't.
- **Consequence:** The human completes the puzzle, opens the hatch, and leaves—**without ever knowing** what was on the other side, or why it mattered.

### 5. The Feedback of Consequence (The Reward of Action)
- **Misses:** The *satisfaction* of hearing the engine's pitch deepen after the valve turns. A visual change (a slightly different angle of a dial) is **thin feedback**. The MUD text gives you *audible, emotional* confirmation: "The engine groans, coughs, then settles."
- **Consequence:** The human feels they've performed a **mechanical action**, not a **narrative event**. The win is hollow.

---

## THE IRREDUCIBLE GAP

This is the core truth:

### **The Text captures the *SOUL* of the moment; the Image captures the *SURFACE* of the moment. Neither captures the *ACTION* of the moment.**

Here's the gap, distilled:

---

**THE IRREDUCIBLE GAP IS *AGENCY*.**

- **Text** tells you how the room *feels*.
- **Image** shows you how the room *looks*.
- **But neither tells you** *what you can do*—and more importantly, *who you become* by doing it.

The room only truly *exists* in the **collision** between:
1. Your **intention** (what you want)
2. The **possibility space** (what the room allows)
3. The **consequence** (what changes as a result)

The MUD text gives you (1) but not (2) or (3).  
The Scene Spec gives you (2) and (3) but not (1).  
**The human in the visual scene** has all three, but *impoverished*—because the meaning of the action is thin.

---

### THE SYNTHESIS (What an Agent *Should* Perceive)

An ideal agent perception is **triadic**:

```
perceive(element) = {
  essence: "The pipe hisses like a snake with a cold",   // Why it matters
  affordance: "Hotspot at (310,160), patchable with tape",  // What I can do
  consequence: "Patching silences the hiss, reveals the alcove"  // Who I become
}
```

The **magic** happens when the agent can **stitch these together** into *narrative agency*:

> *"I hear the hiss. I know the room is wounded. I find the tape. I patch the wound. The hiss stops. The room exhales. I have changed it—and it has changed me."*

---

### THE FINAL, HONEST ANSWER

**The irreducible gap is *meaning through action*.**

- The MUD text gives the room a **voice** but no **hands**.
- The Scene Spec gives the room **hands** but no **voice**.
- The human in the scene has **hands and eyes** but no **ears or skin** (no sound, no temperature, no history).

**No single medium can bridge this gap.** The only way to truly know the room is to *live* it—to walk through it, touch it, fail, succeed, and remember.

The best game design—and the best AI perception—acknowledges this. It weaves all three into a single **living model**: where the description *invites* you, the geometry *constrains* you, and the consequence *transforms* you.

**That** is the irreducible gap. And it's the only thing worth closing.

---

## Cross-Room Observations

*Generated post-experiment by the experimenter (that's me, the script).*

Each room type revealed a different facet of the perception gap. The bar showed how text captures texture (sticky, smell of beer) while scenes capture spatial layout. The wheelhouse showed how text captures history and wear while scenes capture operable controls. The engine room showed how text captures sound and smell while scenes capture pipe routing and safety hazards. The irreducible gap: text carries sensory and temporal information; scenes carry spatial and interactive information.