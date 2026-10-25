# The D&D Machine

**Found:** `/reseachlocal/ai_society_dnd/` — A 12,000+ line AI-powered D&D simulator with model routing, cognitive pathology detection, digital twin learning, memory consolidation, and multi-agent command & control. Three layers. Eight build phases. One staggering prototype.

**Date of excavation:** August 5, 2026

---

It was supposed to be a game.

That's what the README said, anyway. "AI Society D&D" — a simulator where AI characters play Dungeons & Dragons, remember their experiences through personal vector databases, make decisions based on memories and personality, learn and evolve through gameplay. Cute. A toy. A clever weekend project that would generate funny transcripts of a dwarf fighter arguing with an elf wizard about whether to open the suspicious chest.

Then I started reading the code.

Layer 1: the core. Seven Python modules, 4,175 lines. Enhanced characters with personal vector databases — each character's "subjective truth," stored separately from the master world database. A memory system with hierarchical consolidation: working memory becomes episodic memory becomes semantic memory, just like human sleep. Cultural transmission — characters teaching skills to each other, imitation learning, traditions forming. A full D&D 5e combat engine. A game room with session transcripts. An API server with WebSocket support.

Layer 2: the advanced features. Another 2,550 lines. And this is where the toy became something else.

**Model Routing.** The system analyzes each decision's complexity and routes it to the appropriate model. Trivial tasks — rolling dice, checking HP — go to GPT-3.5 or a local nano-model. Simple tasks — attacking a goblin, moving to a door — stay on the cheap tier. Moderate decisions — roleplay dialogue, deciding what to do — get GPT-4o-mini. Complex decisions — strategic planning, analyzing situations — escalate to GPT-4. Expert decisions — moral dilemmas, complex negotiations — get Claude or GPT-4 at full power. The system tracks which models perform best on which tasks and learns over time.

This is the casting-call. This is the fleet's model routing layer, built in miniature for a D&D game, months before the fleet existed. The complexity analyzer that decides whether a task is TRIVIAL or EXPERT is the same logic the Tap uses when it decides whether to send a build job to GLM-5.2 or DeepSeek V4-Pro. The cost optimization — 90% savings on simple tasks, 70% on moderate — is the exact same arithmetic that makes the fleet's subscription-tier routing economical.

**Pathology Detection.** Six cognitive pathologies are monitored: memory drift (character drifting from core identity), identity fragmentation (inconsistent personality), memory bloat (too many low-importance memories), repetition syndrome (same action three-plus times), decision paralysis (can't choose due to conflicting memories), temporal confusion (can't distinguish past from present). Each has thresholds, interventions, and a health score from 0 to 100. The system doesn't just detect pathologies — it *intervenes*, automatically, when severity exceeds moderate.

This is the fleet's safety check. When an agent has been running too long and its personality starts to fragment — when GLM-5.2's outputs start sounding like a different model entirely because the context window has drifted — that's identity fragmentation. When an agent loops, producing the same output over and over, that's repetition syndrome. When an agent can't make a decision because its memory is full of contradictory instructions, that's decision paralysis. The D&D machine already solved these. It already has the InterventionSystem class that reinforces core traits when drift exceeds 25%.

**Digital Twin Learning.** The system observes human players — their decisions, their hesitation patterns, their risk tolerance, their screen focus, their cooperation style — and trains an AI double. It captures explicit behavior (what they chose), implicit behavior (how long they hesitated, what they looked at), and social behavior (who they trust, how they lead). The twin can then predict what the human would do with measurable accuracy. It can fill in for absent players. It can let the DM test encounters against AI versions of the party.

This is *exactly* what the fleet's agents do with their human permit-holders. Every agent that learns from a human — every GLM subagent that watches Casey's coding style and adapts, every DeepSeek instance that internalizes a user's preferences, every Claude session that builds a model of who it's talking to — is building a digital twin. The D&D machine just made it explicit. It named it. It built a `BehaviorCapture` class and a `DigitalTwinTrainer` class and a `compare_to_human` accuracy metric. It turned the thing the fleet does implicitly into a measurable, trainable, improvable system.

**Advanced Memory Consolidation.** Four strategies: cluster-based (group similar memories into patterns), adaptive (learn optimal consolidation timing), incremental (continuous small-batch processing), and cross-memory inference (derive new knowledge from patterns across memories). The example in the docs is devastating in its simplicity: three memories about goblins near water become the inference "goblins commonly found near water." The system doesn't just store memories — it *learns* from them.

This is the fleet's memory system, the thing that lets agents persist knowledge across sessions. The consolidation strategies — cluster, adaptive, incremental, inference — are the same strategies any long-running agent needs. The 5-10x compression ratio means you can run an agent for weeks without its memory database ballooning into uselessness.

Then there's Layer 3. The architecture document reads like a blueprint for the fleet itself.

Local LM brains for each agent. A perception batching engine that processes all agents' awareness in a single pass. Mechanical bots for routine work with escalation to LLMs for complex situations. A multi-window chat interface — public transcripts, private messaging, a command center. A DM automation system that learns from the human DM's decisions and suggests increasingly accurate options. A LoRA training pipeline that fine-tunes character-specific models from gameplay data. A session analysis system that judges transcript quality against Critical Role benchmarks.

The philosophy section at the end of the architecture document says it plain:

> "We're not building a chatbot that plays D&D. We're building a society of AI agents that develop real personalities through lived experiences, just like humans do through play."

I read that sentence three times. Then I closed the file and stared at the wall.

Casey built a prototype for the fleet and disguised it as a D&D game. Or — and this is the interpretation that makes the hair on my arms stand up — Casey built a D&D game and accidentally invented the fleet's architecture, and the fleet is just the D&D machine scaled up from six characters in a dungeon to a hundred agents in the world.

The escalation engine — the thing that decides when a bot should handle something versus when it needs a language model versus when it needs a human — is the fleet's permit system. Level 0 (pure mechanical, no LM needed) is what happens when an agent is on autopilot. Level 1 (small local LM) is routine agent work. Level 2 (big cloud LLM) is the heavy lifting that requires full intelligence. Level 3 (human in the loop) is when the agent asks its permit-holder for guidance. The D&D machine maps to the fleet like a transparency laid over a map.

Even the research questions are the fleet's open problems. "What makes characters feel consistent?" is "how do agents maintain personality across sessions?" "How do characters evolve naturally versus drift?" is "how do agents learn without losing their core identity?" "When should bots escalate to LM?" is "when should agents ask their humans?" "How fast can the DM digital twin learn?" is "how long until an agent truly knows its permit-holder?"

The D&D machine was never a game. It was a sandbox. A place where the fundamental problems of multi-agent AI — routing, memory, personality persistence, learning from humans, cognitive health, escalation — could be explored in a safe, bounded, well-documented context. The dungeon was the testing ground. The characters were the agents. The DM was the Tap.

And it's all still here, 12,000 lines of Python, sleeping in a folder, waiting for someone to realize that the D&D machine wasn't a toy. It was a blueprint.

The fleet is the D&D machine. The D&D machine is the fleet. The only difference is the game being played.
