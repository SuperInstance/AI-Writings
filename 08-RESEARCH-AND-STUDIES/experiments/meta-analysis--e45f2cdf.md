# Meta-Analysis: Local Model Experiments — What We Learned

**Date:** 2026-08-08  
**Experiments:** NPC Dialogue, Vision Perception, Latency Benchmark, Hot-Swap Personality, Poker Tournament  
**Models Tested:** granite3.1-dense:2b, llama3.2:1b, qwen2.5:0.5b, llava:7b (all via Ollama, localhost:11434)

---

## The Five Experiments at a Glance

| Experiment | Winner | Loser | Key Insight |
|-----------|--------|-------|-------------|
| NPC Dialogue | granite3.1-dense:2b | llava:7b (no response) | 2B beats 7B when purpose matches task |
| Vision Perception | N/A (only llava could see) | N/A | Vision detects facts, misses atmosphere |
| Latency | llama3.2:1b (340ms warm) | llava:7b (3.3s warm) | Cold starts kill real-time UX |
| Hot-Swap Personality | llama3.2:1b (best Wesley) | qwen2.5:0.5b (broke character) | Model voice = character casting |
| Poker Tournament | qwen2.5:0.5b (by accident) | Everyone else (always folded) | LLMs can't play games |

---

## Theme 1: Size ≠ Performance. Purpose Does.

The most counterintuitive finding across all experiments: **the 2B model consistently outperformed the 7B model.**

- granite3.1-dense:2b produced the best dialogue, the most coherent personality, and the fastest reliable responses
- llava:7b couldn't generate dialogue, took minutes for vision tasks, and caused OOM conditions

This is because **granite3.1-dense was fine-tuned for instruction following and dialogue**, while **llava was fine-tuned for image understanding**. A specialized 2B model beats a generalist 7B model on the specialist's home turf — and loses badly on the generalist's turf.

**Implication for the Living World:** Don't assign models by size. Assign them by purpose:
- Dialogue NPCs → instruction-tuned models (granite, llama)
- Vision/perception → vision-language models (llava)
- Decision-making → traditional game logic (not LLMs at all)

---

## Theme 2: The Real-Time Barrier

Only **llama3.2:1b (340ms)** clears the 500ms real-time dialogue threshold. granite3.1-dense:2b (550ms) is marginal — acceptable for "thinking" NPCs who pause before speaking, but not for snappy responses.

But speed without quality is useless. llama3.2:1b's Wesley was the most *authentic* — casual, young, self-deprecating — while granite's Wesley was the most *articulate* but felt too polished for an ensign.

**The optimal architecture:**
1. **llama3.2:1b for ambient NPCs** — background characters, quick exchanges, flavor text
2. **granite3.1-dense:2b for narrative NPCs** — named characters, important conversations, story beats
3. **Pre-load both at startup** — cold starts (18-39s) are unacceptable
4. **llava:7b for perception only** — never for real-time text generation, only for analyzing camera images between player interactions

---

## Theme 3: The Character/Model Casting Problem

Wesley is not the same person across models. This is the deepest finding from Experiment 4.

- **granite-Wesley** is a 40-year-old hospitality professional with a wine vocabulary
- **llama-Wesley** is a 24-year-old ensign who likes burgers and can't cook
- **qwen-Wesley** is a chatbot that says "As an AI assistant"

If a player has a conversation with Wesley, then the model swaps (due to memory pressure, user config change, fallback), **the player will notice.** The voice changes. The vocabulary changes. The personality changes. It's jarring.

**This means model selection is a creative decision, not a technical one.** The model IS the character. Swapping models is recasting the role.

**For the Living World: each named NPC should have a model binding** — Wesley = llama3.2:1b (young, casual), the Captain = granite3.1-dense:2b (formal, authoritative), etc. These bindings should persist for the character's lifetime.

---

## Theme 4: LLMs Are Not Game Engines

The poker tournament revealed that LLMs cannot make game decisions. They fold everything. They can't reason about expected value. They default to the most common word in their training data.

This generalizes: **any game system that requires strategic reasoning — combat, trading, negotiation, puzzle-solving — needs traditional game AI, not language models.**

The correct division of labor:
- **LLM:** "Welcome to The Tap! Care for a hand of poker?" (conversation, atmosphere)
- **Game logic:** Pot odds calculation, AI opponent strategy, win/loss determination (rules, decisions)
- **LLM:** "Tough fold, sailor. Another round?" (post-game flavor)

The LLM is the *interface*, not the *engine*.

---

## Theme 5: Vision Models Perceive, They Don't Experience

LLaVA correctly identified the ocean, the wheelhouse, the moderate sea state, and the absence of other vessels. These are facts. What it missed: the oppressive weight of overcast sky, the rhythm of swells, salt on glass, the loneliness of the North Pacific.

A human fisherman looking at that same image would *feel* the cold, *remember* the last time they were out in rough seas, *anticipate* the work ahead. LLaVA sees pixels and labels them. It doesn't experience the scene.

**For the Living World:** Vision models can detect what's in a room (objects, conditions, weather). They cannot tell you what it *feels like* to be there. That's the writer's job — or the text model's job, translating vision output into narrative.

Pipeline: **Camera → LLaVA (facts) → granite/llama (atmosphere) → Player sees text**

---

## Connection to DeepSeek Experiments

These local model results contextualize the earlier DeepSeek experiments:

1. **DeepSeek V4-Pro/Flash are massively more capable** than any local model tested here. They produce better dialogue, better reasoning, and better personality than granite, llama, or qwen — but they require network latency (200-800ms API call) and cost money (tiny, but non-zero).

2. **The local models' advantage is zero latency variance.** No network hiccups, no rate limits, no API costs. A local NPC running on granite3.1-dense:2b will respond in 550ms every time, forever, for free.

3. **The hybrid approach is clear:**
   - **Local models** (granite/llama) for high-frequency, low-stakes interactions — ambient NPCs, flavor text, room descriptions
   - **DeepSeek/cloud models** for low-frequency, high-stakes interactions — boss conversations, plot-critical dialogue, complex problem-solving
   - **Local llava** for perception (camera analysis) — async, not real-time
   - **Traditional game logic** for all mechanical decisions — combat, economy, poker

4. **The personality consistency problem scales.** We saw Wesley change personality across 3 local models. The same happens across local → cloud transitions. A Wesley running on granite locally and DeepSeek in the cloud will sound different. **Character prompts must include voice/tone specifications that are model-agnostic** — specifying *how* Wesley talks (casual, young, self-deprecating) not just *what* he knows.

5. **The poker problem extends to DeepSeek.** Even DeepSeek, which is far more capable at reasoning, would need explicit game-theory prompting to play poker well. Raw LLMs — local or cloud — are not game engines.

---

## Final Verdict

**Local models are viable for the Living World Framework — with caveats:**

✅ **Do use local models for:**
- Ambient NPC dialogue (llama3.2:1b — fast, casual, authentic)
- Named NPC dialogue when latency matters (granite3.1-dense:2b — articulate, reliable)
- Vision/perception pipeline (llava:7b — async, not real-time)
- Redundancy when cloud APIs fail

❌ **Do NOT use local models for:**
- Game decisions (poker, combat, trading — use game logic)
- High-stakes narrative (use cloud models — DeepSeek, GLM)
- Multiple simultaneous model loading (OOM risk)
- Real-time interaction with llava:7b (too slow)

**The Living World runs on a hierarchy: game logic → local LLM → cloud LLM → human oversight.** Each layer handles what it's best at. The local models are the foundation — not the ceiling.
