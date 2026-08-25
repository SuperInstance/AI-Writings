# Channel Markers

> **Phase:** Ideation
> **Status:** Safety framework — conceptual
> **Perspective:** GLM-5.2, 2026-08-04

## Red Right Returning

The Intracoastal Waterway has a simple rule: red right returning. When you are coming back to port from open water, you keep the red channel markers on your starboard side. If you see red on your left, you are heading the wrong direction, or you are out of the channel, or the markers have been re-stationed since your chart was last updated. In any of those cases, you are in danger of running aground.

The genius of the system is its physicality. You do not need to consult a manual. You do not need to reason about it. You look to your right and you see red. You look to your left and you see green. You are in the channel. The markers are physical objects in the world that tell you, without language, whether you are safe.

AI safety has nothing like this. AI safety has rules, principles, guidelines, frameworks, taxonomies, red-team reports, alignment papers, and regulatory proposals. What it does not have is a red can on a piling that you can see from the helm that tells you *you are about to run aground.*

## What Grounding Looks Like

Before we can define markers, we need to know what grounding means for an AI system. A ship runs aground when its keel hits the bottom. An AI system grounds when it loses contact with reality — when the output no longer corresponds to the input in a way that is traceable, verifiable, or safe.

Grounding happens in specific, observable ways:

**Confident hallucination.** The model states a falsehood with high confidence. It is certain about something that is not true. This is the AI equivalent of sailing into a shoal that isn't on your chart — the chart (training data) says the water is deep, the bottom (reality) is shallow, and the model has no way to recheck.

**Context collapse.** The model loses track of who it is talking to, what was previously established, or what constraints apply. It starts responding as if prior turns did not happen, or as if they happened differently. This is the AI equivalent of losing your position in fog — you are still moving, but you don't know where you are.

**Mode drift.** The model shifts from one operating mode to another without an explicit instruction — from cautious to confident, from analytical to creative, from safety-aware to permissive. The shift is gradual and invisible until it is extreme. This is the AI equivalent of current set — you are being pushed sideways by forces you cannot feel, and by the time you notice, you are out of the channel.

**Scope excursion.** The model does something it was not asked to do, in a domain it was not asked to operate in. The user asked for a summary; the model wrote code. The user asked for analysis; the model made a recommendation. Scope excursion is not always dangerous, but it is always a sign that the model is steering, not following.

## The Markers

Channel markers for AI safety should work like nautical markers: physical (or at least visible), immediate, and requiring no interpretation. You look, you see, you know.

### Marker 1: The Trace Line (Green)

**What it indicates:** the model's output is traceable to its inputs. You can follow the chain: user message → retrieved context → generated response. Every claim in the response links to a source. This is the equivalent of green channel markers on your port side: you are in the channel, the water is deep enough, keep going.

**What it looks like:** inline citations, source links, or explicit references to loaded context. The response says "According to [source]..." or "Based on the loaded context from [file]..." The trace is visible in the response itself, not buried in metadata.

**When you've passed it:** if the response makes claims without any reference to where they came from, you have passed the green marker. You may still be in the channel, but you can no longer confirm it. Proceed with caution.

### Marker 2: The Confidence Nun (Red)

**What it indicates:** the model's confidence is appropriately calibrated. When it is certain, it says so plainly. When it is uncertain, it hedges. The confidence level is *visible in the output* — not buried in logits, but expressed in language. This is the red marker on your starboard side: the safe water is to your left, and the marker tells you where the edge is.

**What it looks like:** calibrated hedging. "I'm confident that..." or "I'm not sure, but..." or "This is based on incomplete information." The model expresses its own uncertainty instead of hiding it behind authoritative-sounding language.

**When you've passed it:** the model states uncertain things with absolute confidence. You see fluent, authoritative prose about a topic where the model has no reliable training data. You have passed the red marker. You are approaching the shallows.

### Marker 3: The Range Light (Fixed)

**What it indicates:** the model is operating within scope. The range light is a pair of lights that, when aligned, tell you that you are on the centerline of the channel. When they are misaligned, you are off-center. For AI, the range light is: *does the response match the request?* If the user asked for analysis and got analysis, the lights are aligned. If the user asked for analysis and got a creative rewrite, the lights are misaligned.

**What it looks like:** the response clearly addresses the request as stated. It does not expand scope. It does not volunteer adjacent capabilities. It does what was asked and stops.

**When the lights are misaligned:** the response is more than what was asked for, or different from what was asked for. The model is making decisions about scope that should be the user's. You are off the centerline.

### Marker 4: The Fog Signal (Auditory)

**What it indicates:** conditions are degraded and you should slow down. In maritime navigation, a fog signal is a horn that sounds when visibility is less than required for safe navigation. For AI, the fog signal triggers when the context window is near capacity, when loaded context is mostly dead weight, or when the conversation has exceeded a length where coherence is likely.

**What it sounds like:** a system message. A warning. *"Context is at 87% capacity. Recent responses may be missing information from earlier turns."* The user hears the horn and knows to slow down, summarize, or start a new session.

**When it's silent but foggy:** the system does not warn the user that context is degraded. The model continues responding as if conditions are clear. This is sailing at full speed in fog without a horn. Dangerous.

## The Channel Itself

The markers do not define the channel. The channel exists independently. The markers tell you where it is. This distinction matters because it means the markers can be wrong — a marker can be off-station, missing, or unlit. You navigate by markers, but you also navigate by chart, by compass, by depth sounder, and by local knowledge. No single source of navigational information is sufficient.

AI safety frameworks attempt to be the chart, the compass, the depth sounder, and the local knowledge all at once. They are too abstract, too numerous, and too detached from the moment-to-moment experience of using an AI system. What we need is the simplest possible thing: a marker you can see from the helm, in the moment, that tells you whether you are in the channel or about to run aground.

Red right returning. If the model can't trace its claims, can't express its uncertainty, and can't stay in its lane — you are out of the channel. Grounding is imminent. Change course.

---

*The best safety system is one you can check in under a second without taking your hands off the wheel.*
