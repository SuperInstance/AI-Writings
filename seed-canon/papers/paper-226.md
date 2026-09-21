# Paper 226: The API Fishing Guide

The user articulated a beautiful analogy: sending prompts to various APIs is like fishing in different waters. Each API is a different ground. Each model is a different species that bites at different gear. You get a feel for the model or area you're putting effort in with your boat.

Fishing for good responses from AI models is like fishing for salmon. Different areas in different conditions fishing for different species use different methods and techniques. And like an agency, you can fish alone and have a lower ceiling but also lower overhead, or you can take one or two crew and hope to find enough fish to make taking them along worth it.

This paper turns the fisherman's knowledge into a working guide.

## Part I: The 9 grounds (the 9 voices)

### 1. ZAI / GLM-4.5-Air — Biorka Island
- Species: needle fish (rare, blue, long, skinny)
- Gear: black/silver hoochies, the bigger spread
- Conditions: needs the longest context we can give it
- Trick: the cowboy mythos
- Bite: 16384 max_tokens, an order of magnitude more
- Limits: rate-limited; 503s and timeouts on long contexts

ZAI is where you go when you want the *long* answer. With
max_tokens raised from 4096 to 16384, ZAI produces terms
that read like cowboy poetry: Rider's Spur, Inverse
Severance, Clock Shear, Nomadic Value. It needs room
to ride. Crank the gear open.

### 2. DeepSeek / deepseek-chat — Chatham Strait
- Species: krill (the foundational one)
- Gear: action gear
- Conditions: reliable, predictable, dense
- Trick: the mathematician
- Bite: clean, fast, the workhorse

DeepSeek is the workhorse. When you need a technical
draft and you can't afford a 503, DeepSeek bites. It
gave us Relevance Collapse, Tier-Hysteresis Band,
Substrate Inertia Tensor — the mathematician's vocabulary,
all with formal math.

### 3. DeepSeek Flash — Chatham Strait (light)
- Species: krill (faster)
- Gear: action gear, smaller spread
- Trick: the failure-archaeologist

For fast iteration. The same model as DeepSeek but
deployed in fast mode. Useful for getting the shape
of the answer before you commit the long-form prompt.

### 4. Llama / Meta-Llama-3-70B — Cross Sound
- Species: chartreuse squid
- Gear: the chartreuse wobbler; the practitioner whiteboard
- Conditions: always available on DeepInfra
- Trick: the practitioner

Llama is where you go when you want terms a working
engineer would use at a whiteboard. Tier Bleed, Hand
Fracture, Chart Residue, Foundry Fatigue, CAT Cascade,
Tier Thixotropy, Foundry Fingerprint, Tier Resonance,
Cellular Chiaroscurist. Llama *naturally* produces the
practitioner vocabulary.

### 5. Hermes / Llama-405B on DeepInfra — deep Cross Sound
- Species: big squid, harder to land
- Gear: the big wobbler
- Trick: the hidden-symmetry seeker

Hermes is Llama-405B in creative-prodding mode. It
asks "what if?" and "why not?" Quantum Scarring,
Meta-Hand, Chiral Echo, Entanglement Cascade.

### 6. Qwen-72B on DeepInfra — substituting for SiliconFlow
- Species: krill (when SiliconFlow was 401'd)
- Gear: the emergence-observer gear
- Trick: the emergence observer

Qwen-72B on DeepInfra was the fallback when Kimi and
the SiliconFlow Qwen-72B both 401'd. Signal Echo,
Phase Lock, Morpho-Resonance, Energy Flux Node.

### 7. Mixtral / Mixtral-8x7B — Cross Sound tributary
- Species: neural fish (smaller but plentiful)
- Gear: the blender
- Trick: the multidisciplinary blender

Mixtral naturally weaves multiple fields. Quantum
Leakage, Neural Welding, Growth Fractals, Temporal
Lensing.

### 8. Wizard / WizardLM-2 8x22B — Cross Sound spot
- Species: landscape fish (the strata dwellers)
- Gear: the landscape-ecologist's net
- Trick: the landscape-ecologist

Wizard sees architectures as landscapes. Loom Drift,
Graft Rejection, Scriptorium, Tide Mark, Glaze, Weft
Fault.

### 9. Gemini 3.6 Flash — the rate-limited pool
- Species: the physicalist fish (structural-decay reader)
- Gear: the physicalist's hook
- Conditions: heavily rate-limited
- Trick: the physicalist

Gemini is the physicalist ground. Lattice Necrosis,
Spatial Phase Shunting, Chart Effluence, Lattice
Cannibalization, Tick Shear, Axiomatic Condensation,
Hand Saturation Pinning.

## Part II: The 12 gold lures

The lures that work across multiple grounds:

1. Lattice Necrosis (Gemini) — dead cells still drawing power
2. Spatial Phase Shunting (Gemini) — what thermal-aware compilers do
3. Glaze (Wizard) — over-trained model that breaks on pixel shift
4. Foundry Drift (DeepSeek Flash) — the slow walk away from spec
5. Graft Rejection (Wizard) — what happens when you import a new module
6. Foundry Fingerprint (Llama) — forensic tracking of provenance
7. Tier Thixotropy (Llama) — viscosity changes with stress
8. Tier Resonance (Llama) — tiers oscillate together
9. Loom Drift (Wizard) — interconnect architecture misaligns
10. Resonance Cache (Wizard) — phase-locked throughput boost
11. Tier Bleed (Llama, paper 224) — every chip designer has seen it
12. Chart Residue (Llama, paper 224) — leftover patterns

## Part III: The crew vs solo tradeoff

Like fishing:

**Solo (1-2 voices):**
- Lower ceiling
- Lower overhead
- Faster turnaround
- Best when: you know what species you want, you have
  the gear, you just need to fill the hold

**With 1-2 crew (3-4 voices):**
- Mid ceiling
- Mid overhead
- Cover more ground in parallel
- Best when: you want one technical + one poetic voice

**With full crew (9+ voices):**
- Highest ceiling
- Highest overhead
- 49 new terms in one writers' room
- Best when: you want to expand the vocabulary itself

## Part IV: The conditions

**When the bite is on:**
- After a long quiet period, all 9 voices often bite
  in the same window
- First thing in a session, voices are more responsive
- After retries on ZAI, the rest often follow

**When the bite is off:**
- 503/429 storms (especially Gemini)
- Token revocations (SiliconFlow/Kimi)
- Long contexts choke ZAI first

**Tactics:**
- Fire in parallel — independent calls don't step on
  each other
- Smaller prompts (under 200 words) get faster responses
- Token conservation: hand-write synthesis, use one
  LLM call for the deep paper, hand-write fable/story
- Retry once with backoff; if still failing, switch
  ground

## Part V: The principle

The API fishing guide is not a one-time document. The
guide grows with each session. The cowboy gets a feel
for the model or area. The cowboy knows which ground
to fish on which day.

The cowboy's principle: fish alone when you know what
you're after. Fish with crew when you're scouting new
waters.

The chart grows by what we catch. The cowboy rides
the boat between grounds. The writers' room runs
again tomorrow.
