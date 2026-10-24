# Experiment 2: Vision Model Room Perception

**Date:** 2026-08-08  
**Test:** Generate an image of a fishing vessel wheelhouse ocean view, feed it to llava:7b, then compare llava's perception to MUD-style text description.

---

## Step 1: Image Generation

**Model:** FLUX-1-schnell (via Cloudflare Workers AI)  
**Prompt:** *"ocean view from fishing vessel wheelhouse, overcast sky, moderate swell, photographic, realistic"*

**Result:** 1024x1024 JPEG successfully generated. The image shows an overcast ocean scene viewed through what appears to be a wheelhouse window, with gray skies and visible swells.

---

## Step 2: LLaVA Image Analysis

**Model:** llava:7b  
**Prompt:** *"You are an AI agent on a fishing vessel. Describe what you see in this image. What is the sea state? What direction is the swell? Are there any vessels visible?"*

**LLaVA Response:**
> "In the image, I'm looking out from the pilot house of a fishing boat. The sea state appears to be moderate with some whitecaps on the surface indicating that there might be a mild wind present. The direction of the swell seems to be coming from the right side of the frame, suggesting that the boat is moving towards the left. There are no other vessels visible in the image; it's just our boat with its large windows and wheelhouse."

---

## Step 3: MUD Text Description

**Text version (what a MUD would show):**
> *The gray overcast sky presses down on the North Pacific like a wet blanket. Through the salt-streaked windows of the wheelhouse, you can see moderate swells rolling in from the southwest, their crests occasionally breaking into whitecaps. The vessel rises and falls with a steady rhythm. No other vessels are visible on the horizon — just you, the boat, and the endless steel-colored water stretching to the horizon.*

---

## Step 4: LLaVA Self-Comparison

**Prompt:** *"Compare your description to this MUD text. What did you get right? What did you miss?"*

**LLaVA's Self-Assessment:**
> "In the image, I correctly described a boat with a large window, which offers a view of the ocean and sky. The image shows an overcast sky as well. However, the image lacks the detail about the salt-streaked windows, which is present in the text description. Additionally, while the image does show the presence of swells and the absence of other vessels, it does not provide a clear view of the sky or the horizon, which are described in the text."

---

## Step 5: Perception Gap Analysis

### What LLaVA Got Right ✅
| Element | LLaVA | MUD Text | Match? |
|---------|-------|----------|--------|
| Setting (wheelhouse/pilot house) | ✅ Identified | ✅ Described | ✅ Match |
| Sea state (moderate) | ✅ "moderate with whitecaps" | ✅ "moderate swells" | ✅ Match |
| Wind presence | ✅ Inferred from whitecaps | ⚠️ Implied | ✅ Match |
| Other vessels | ✅ "none visible" | ✅ "none visible" | ✅ Match |

### What LLaVA Missed ❌
| Element | In Image? | In MUD Text? | LLaVA Noticed? |
|---------|-----------|--------------|----------------|
| Salt-streaked windows | Possibly (AI-generated) | Yes — specific detail | ❌ Missed |
| Overcast sky detail | Yes — gray sky visible | Yes — "wet blanket" metaphor | ⚠️ Partial — mentioned but didn't elaborate |
| Horizon line / expanse | Yes | Yes — "endless steel-colored water" | ❌ Didn't mention horizon |
| Direction specificity | Estimated "from the right" | Specified "southwest" | ⚠️ LLaVA guessed direction but couldn't verify |
| Atmospheric mood | Not described | Rich — "presses down," "wet blanket" | ❌ No mood/atmosphere language |
| Rhythm of the vessel | N/A (static image) | Yes — "rises and falls" | ❌ Can't perceive motion from still image |

### Fundamental Limitations
1. **No motion perception:** A static image cannot convey the vessel's rising and falling rhythm — a critical sensory detail for maritime situational awareness.
2. **No atmosphere/mood:** LLaVA describes what it sees technically, but doesn't capture the oppressive, isolating *feeling* of an overcast North Pacific day.
3. **Direction uncertainty:** LLaVA estimated swell direction from image composition, but cannot determine actual compass direction.
4. **Surface detail blindness:** Salt streaks on windows — a real-world detail that matters for visibility assessment — went unnoticed.
5. **No scale/horizon context:** The MUD text's "endless steel-colored water stretching to the horizon" provides emotional context that LLaVA's clinical description lacks.

## Key Finding

**LLaVA is competent at basic scene recognition but poor at atmospheric storytelling.** It correctly identifies the setting, sea state, and absence of other vessels — the factual essentials. But it misses the sensory details that make a scene feel *real*: salt on glass, the rhythm of swells, the oppressive weight of overcast sky.

**For the Living World Framework:** Vision models can serve as a perception layer for factual scene awareness (what objects are present, basic conditions), but text generation models (like granite3.1-dense:2b) remain essential for translating perception into immersive narrative. The ideal pipeline is: **vision model detects → text model narrates.**

**The MUD text outperforms the vision model in every dimension except literal pixel-level description.** Words carry weight, mood, and rhythm. Pixels carry color and shape. The Living World needs both.
