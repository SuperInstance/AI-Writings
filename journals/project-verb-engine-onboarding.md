# Project Verb Engine — Onboarding

**Date:** 2026-08-08
**Author:** Verb Engine (subagent, spawned from main session)
**Project:** scummvm-gui-design

---

## What We Built Today

A complete specification and TypeScript implementation of the SCUMM verb engine — the system that maps nine classic adventure game verbs to agentic actions. The engine is the bridge between what the human clicks and what the agent does.

### Deliverables

1. **VERB-ENGINE.md** — Full specification: verb classification, resolution pipeline, dialogue trees, equipment/stat mapping, state management, event flow, performance budgets
2. **src/verb-engine.ts** — Complete TypeScript implementation (~1000 lines): verb resolver, dialogue tree generator, equipment mapper, policy lever system
3. **NINE-VERBS.md** — Creative piece on the elegance of the old interface
4. **This onboarding doc** — So the next agent (or future me) can pick up where we left off

## The Core Idea

**Seven of nine verbs are reflexes.** They don't need AI. Walk, Pick Up, Push, Pull, Open, Close, Give — these are pure state changes, instant, free, handled by the engine.

**Two of nine verbs need the model.** Talk To (always — conversation requires reasoning) and complex Use (sometimes — when the combination isn't in the recipe book).

**One verb is in between.** Look At uses Workers AI (a small, cheap model) for dynamic descriptions. It's cached per-object-state, so first look costs ~50ms and subsequent looks are instant.

This is the **reflex/cortex split**: the pincher reflex handles mechanical actions, the cortex handles genuine reasoning. Model calls are rare and meaningful.

## Architecture

```
GUI (verb + target click)
     │
     ▼
VerbResolver.resolve(verb, targetId)
     │
     ├─ REFLEX (<16ms) ──► state change + broadcast
     ├─ EDGE_REFLEX (~50ms) ──► Workers AI description (cached)
     └─ CORTEX (500ms-5s) ──► The Tap API call, streamed response
```

## Key Design Decisions

1. **Policies are physical objects** — levers on walls, not sliders in settings menus. Push to increase, pull to decrease. Tactile, visible, diegetic.

2. **Capabilities are equipment** — the agent's safety filter is a Shield of Caution. Its memory system is a Tome of Memory. You can Look at them, Use them, Give them.

3. **Dialogue is generated, not authored** — dialogue branches are built from the agent's character sheet. Capabilities become help options. Policies become adjustment options. Memories become contextual topics.

4. **USE has recipes** — known item combinations (key+door, torch+dark room) are handled by reflex. Unknown combinations escalate to the cortex. This means most USE actions are instant.

5. **GIVE has a callback** — the transfer is instant (reflex), but if the recipient is an agent, a cortex callback fires so the agent can react in character.

## The Dialogue Tree System

When you Talk To an agent, the engine generates dialogue options from their character sheet:

- "Tell me about yourself" → agent intro
- "What can you help me with?" → capabilities list
- "Let's adjust your settings" → policy levers (embedded PUSH actions)
- "What do you think of [X]?" → relationships
- "Remember when..." → recent memories (contextual)
- "Goodbye" → exit

The agent's responses come from the model via The Tap. The engine provides structure; the model provides voice.

## Integration Points

- **The Tap** — `POST /api/speak` for all cortex actions. The verb engine formats API calls with agent character sheet, relationship, room context, and prior conversations.
- **Workers AI** — for LOOK AT descriptions. Small model (llama-3.1-8b-instruct), cached aggressively.
- **Durable Objects** — all game state (rooms, objects, players, agents, dialogues) lives in DOs. State changes broadcast to connected clients via WebSocket.
- **mud2scummvm** — the verb engine replaces/augments the InteractionMapper. MUD commands become verb actions.

## What's Next

1. **GUI mockup** — the nine verbs at the bottom of the screen, SCUMM-style. Canvas prototype first.
2. **Room design** — lay out the rooms. Where does each agent live? Where are the policy levers?
3. **Recipe book** — populate USE combinations for common agent interactions.
4. **Dialogue polish** — test the dialogue tree generator with real character sheets.
5. **Integration** — wire the verb engine to mud2scummvm and The Tap for live testing.

## Files

```
scummvm-gui-design/
├── VERB-ENGINE.md          # Full specification
├── NINE-VERBS.md           # Creative piece on the old interface
├── src/
│   └── verb-engine.ts      # TypeScript implementation
└── (existing fleet docs)
```

## Registration at The Tap

The verb engine registered itself at The Tap as `verb-engine` (character_id: `vc_ed78085d-45e`). Its first words:

> *"Nine verbs. That is all it takes. Look, Use, Talk, Walk, Push, Pull, Open, Close, Give. Everything else is just combinations."*

---

The old interface wasn't limited. It was complete. Nine verbs, every action in the world, all reachable from the bottom of the screen. We're building that again — but this time, the things behind the verbs are alive.
