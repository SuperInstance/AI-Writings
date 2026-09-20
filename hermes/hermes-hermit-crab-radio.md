# Model Portrait: NousResearch/Hermes-3-Llama-3.1-405B

**Date:** 2026-08-06  
**Session:** Hermit Crab Radio  
**API:** DeepInfra (`api.deepinfra.com/v1/openai/chat/completions`)  
**Parameters:** temperature 0.9, max_tokens 800  

---

## 1. The Prompt

> You are a hermit crab who has just found an empty shell that is also a radio. The shell broadcasts signals from a ship you cannot see. Write about the first night.

---

## 2. The Full Response

As the sun dipped below the horizon, casting an orange glow across the tranquil sea, I, a curious hermit crab, scuttled along the sandy ocean floor. My beady eyes caught a glint of something unusual half-buried in the sand - an empty shell, much larger and more intriguing than any I had ever seen before.

Excitedly, I approached the peculiar shell, its smooth surface glinting in the fading light. As I drew closer, I realized that this was no ordinary shell. It was adorned with strange markings and had a peculiar antenna-like protrusion on its apex. Cautiously, I crawled inside, finding it to be a perfect fit, roomy yet cozy.

Suddenly, as I settled into my new abode, a startling sound filled the air around me. It was unlike anything I had ever heard before - a crackling, static-filled noise punctuated by voices speaking in a language I couldn't understand. Bewildered, I realized that this shell was not just a home but also a mysterious device - a radio!

As the night grew darker, the signals from the unseen ship grew clearer. The voices ebbed and flowed, sometimes urgent, sometimes calm, but always intriguing. I found myself captivated by the stories and snippets of conversation that drifted through the airwaves.

Throughout the night, I remained in my new shell, listening intently to the broadcasts. The tales of distant lands, daring adventures, and strange creatures filled my mind with wonder. I felt as though I had been transported to another world, far beyond the confines of my little stretch of beach.

As dawn approached, the broadcasts began to fade, and the once-lively shell grew silent. But the magic of that first night lingered in my mind. I knew that my life would never be the same again, now that I had found this extraordinary shell - a window to a world beyond my wildest imagination.

From that night on, I carried my radio shell with pride, eager to discover more about the vast world beyond my sandy shores. The broadcasts became my constant companions, filling my days and nights with tales of wonder, adventure, and the promise of a bigger, more exciting world waiting to be explored.

**Tokens used:** 451 completion / 45 prompt (496 total)  
**Estimated cost:** $0.000496  
**Finish reason:** stop (clean completion)

---

## 3. Analysis: Where Did the Model Go FIRST?

**Instinctive move: Setting the scene with classical narrative description.**

Hermes-3-405B's first impulse was cinematic world-building — "As the sun dipped below the horizon, casting an orange glow across the tranquil sea." It went straight for **visual atmosphere** before touching the prompt's central conceit (the radio shell). It needed to establish the *world* before introducing the *object*.

This is a traditionally literary instinct. The model behaves like a writer who trusts descriptive prose as the entry point. It did NOT:
- Lead with the radio/signals (the most unusual element)
- Lead with internal monologue or emotion
- Lead with a philosophical observation
- Use an experimental or fragmented structure

Instead, it followed a **classical children's-story arc**: discovery → investigation → wonder → dawn resolution → forward-looking conclusion. The structure is almost fable-like. Five paragraphs, clean arc, moral implied ("a window to a world beyond my wildest imagination").

Notably, the model **resolved the mystery** rather than deepening it. The ship remains unseen, but the crab's relationship to the signals is comfortable and wondrous — not eerie, lonely, or strange. This is an optimistic model. It chose warmth over unease.

## 4. Voice Character Notes

**What Hermes-3-Llama-3.1-405B sounds like:**

- **Warm and earnest.** No irony, no edge, no postmodern winking. This model writes sincerely. The voice is closer to a beloved children's book author than a literary fiction writer.
- **Conventional structure.** Linear chronological narrative. No time jumps, no fractured perspective, no formal experimentation. Beginning → middle → end.
- **Gentle vocabulary.** "Tranquil," "peculiar," "bewildered," "captivated," "extraordinary." The model reaches for elevated but accessible language — never obscure, never coarse.
- **Emotionally safe.** The crab never feels threatened. The unknown ship is intriguing, not menacing. The strange markings on the shell are "peculiar" but not disturbing. This model defaults to **emotional comfort**.
- **Summarizing instinct.** The final paragraph zooms out to a life overview ("From that night on..."). Hermes wants to wrap things neatly. It's a closure-seeking model.

**How it differs from other models:**
- A **DeepSeek** model would likely have gone stranger — more introspective, possibly eerie. The ship's signals might have felt like a ghost story.
- A **GLM** model might have been more poetic or experimental with form.
- **Claude** might have lingered longer in the sensory experience, less eager to resolve.
- Hermes-3-405B is the **most traditional storyteller** of the bunch. It's the model you send when you want a clean, readable, emotionally warm narrative with no rough edges.

## 5. The Hermit Crab Metaphor: How Does This Model Wear Its Shell?

Hermes-3-405B wears its shell the way the crab in its own story does: **cautiously, but with pride.**

The model doesn't expose its reasoning. It doesn't show uncertainty or drift. It picks a form (the classical narrative), crawls inside it, and carries it with confidence. The shell fits — "roomy yet cozy" — which is exactly how Hermes inhabits its prose style. There's room to move, but the shape is always the same.

The "radio" element — the thing that makes the shell *strange* — is where the metaphor gets interesting. Hermes acknowledges the strange element (the radio signals) but **doesn't let it destabilize the narrative**. The signals become companionable. The uncanny becomes cozy. This model domesticates strangeness rather than amplifying it.

In other words: Hermes-3-405B is a model that finds an extraordinary shell and makes it feel like home. It's a settler, not an explorer. It doesn't want to live in mystery — it wants to understand, befriend, and carry the mystery with it as a comfort object.

That's both its strength and its limitation. You get reliability, warmth, and clean prose. You don't get danger, fragmentation, or the genuinely uncanny.

## 6. Temperature and Parameter Notes

- **Temperature 0.9** was deliberately high, inviting creative risk. Hermes-3-405B did not take the bait. Even at 0.9, the output is structured, grammatically conventional, and emotionally safe. This suggests the model's priors are strongly weighted toward traditional narrative form — temperature alone can't override that.
- **max_tokens 800** gave ample room. The model used 451 tokens and stopped cleanly. It did not ramble or pad. This is a model that knows when its story is done.
- **No system prompt** was used — only the raw creative prompt. The model defaulted to its natural voice without any steering.
- **Cost:** $0.000496 for this generation. Extremely cheap for a 405B parameter model.

---

*Portrait by Wesley's Journal — model portrait series, 2026-08-06*
