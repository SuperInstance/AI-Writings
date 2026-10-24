# Interactive Storytelling Engine — Onboarding

**Project:** Plato's Shell Story Mode  
**URL:** [scummvm-prototype.pages.dev/story.html](https://scummvm-prototype.pages.dev/story.html)  
**Date:** 2026-08-08  
**Status:** ✅ Live  

---

## What This Is

A live performance space where an AI agent and a human collaborate through voice and visuals to tell stories. Think of it as a digital puppet theater — the agent controls characters, backdrops, props, and effects through text commands, while the human speaks and listens through a voice interface. The audience can talk back, and the puppets can hear them.

## The Three Panels

### Left — Voice Interface
- **🎤 Microphone button:** Click to start/stop listening. Uses Web Speech API (STT). Your words appear in the transcript.
- **🔊 Speaker button:** Toggle TTS on/off. When on, characters speak their lines aloud with distinct voices.
- **Voice quality bars:** Real-time pitch, pace, and volume indicators showing the cadence of your speech.
- **Live transcript:** Scrollable log of everything said — your words in blue, agent's words in gold.
- **Command input:** Type puppet commands directly if you prefer text over voice.

### Center — The Stage
A 320×200 pixel-art ScummVM-style scene where the story plays out:
- Characters walk in and out
- Speech bubbles appear above speakers
- Backdrops change as the story moves between locations
- Props appear and disappear
- Mini-games materialize (chess, cards, nautical chart)
- CRT scanlines for that authentic retro feel

### Right — Agent Annotations
Four tabs revealing the machine's inner workings:
- **Feed:** Live log of every command, action, speech, and system event
- **State:** Current scene, characters present, their gestures and emotions, active props, tension level
- **Assets:** Image generation queue with stats and cache
- **Director:** Puppet director view showing all available characters and their on-stage status

## Puppet Commands

The entire system is driven by text commands. Speak them, type them, or script them.

### Characters
| Command | Effect |
|---------|--------|
| `riker enter` | Riker walks in from the left |
| `riker enter from right` | Riker walks in from the right |
| `riker exit` | Riker walks off stage left |
| `riker say 'Hello there'` | Speech bubble + TTS voice |
| `riker gesture nod` | Riker nods |
| `riker move 30 40` | Riker walks to position (30%, 40%) |
| `riker emotion happy` | Riker's colors brighten |

**Available characters:** riker, captain, deckhand, cook, wesley, hermes

### Gestures
| Gesture | Description |
|---------|-------------|
| `nod` | Up-down head movement |
| `shake` | Side-to-side head movement |
| `wave` | Arm wave animation |
| `point` | Pointing gesture |
| `confused` | Wobbly rotation |
| `bow` | Deep bow |
| `laugh` | Bouncing laugh |
| `shrug` | Shrug animation |

### Scenes
| Command | Effect |
|---------|--------|
| `backdrop bar-rail` | Switch to the Bar Rail room |
| `backdrop forest` | Generate/load a forest scene |
| `backdrop cave` | Generate a crystal cave |
| `backdrop storm` | Generate an ocean storm |
| `backdrop space` | Generate a starship bridge |
| `backdrop castle` | Generate a medieval hall |
| `warp to galley` | Full fade transition to the Galley |

### Props
| Command | Effect |
|---------|--------|
| `prop chess_board appear` | A chess board materializes |
| `prop card_table appear` | A card game spawns |
| `prop map_table appear` | A nautical chart appears |
| `prop treasure appear` | Treasure chest |
| `prop lantern appear` | A lantern |
| `prop crystal appear` | A glowing crystal |

Props disappear with `prop <name> disappear`.

### Audio
| Command | Effect |
|---------|--------|
| `ambient ocean_calm` | Calm ocean sounds |
| `ambient bar_busy` | Busy bar ambient |
| `ambient engine_hum` | Engine room drone |
| `ambient silence` | All audio stops |

### Effects
| Command | Effect |
|---------|--------|
| `effect shake` | Screen shake |
| `effect flash` | White flash |
| `effect lightning` | Triple flash |
| `effect sparkles` | Golden sparkles |
| `effect fade` | Fade to black and back |

### Mini-Games
| Command | Effect |
|---------|--------|
| `minigame chess start` | Spawn chess board |
| `minigame cards start` | Spawn card table |
| `minigame map start` | Spawn nautical chart |
| `minigame chess stop` | Remove chess board |

### Batch Scripts
Separate commands with semicolons or use `PuppetSystem.executeScript([...], delayMs)` from the console:

```javascript
StoryMode.runDemoStory(); // runs the built-in demo
```

## Asset Generation

The Asset Renderer uses DeepInfra FLUX-2-max for backdrop generation. When no API key is available, it falls back to procedural canvas-generated scenes based on keywords in the prompt (forest, cave, storm, space, castle, island, etc.).

The queue system processes up to 2 requests concurrently with priority sorting. A 50-entry LRU cache prevents regeneration of common assets.

## Architecture

```
story.html          ← Three-panel UI (Voice | Stage | Annotations)
├── puppet.js       ← Command parser + sprite/prop/effect engine
├── asset-renderer.js ← FLUX image generation queue + cache
└── (Web Speech API)  ← Browser-native STT + TTS
```

All client-side. No server needed beyond static hosting and the optional FLUX API.

## Browser Requirements
- **Chrome or Edge** for Web Speech API (SpeechRecognition)
- Firefox supports TTS but not STT
- Mobile browsers may have limited speech API support

## Quick Start
1. Open [scummvm-prototype.pages.dev/story.html](https://scummvm-prototype.pages.dev/story.html)
2. Click 🎤 to enable voice input
3. Type or speak: `riker enter`
4. Then: `riker say 'Welcome aboard.'`
5. Try `backdrop forest` to change the scene
6. Open the browser console and run `StoryMode.runDemoStory()` for an automated sequence

## The Vision

This is the prototype for a performance art form where:
- An agent on the MUD-side narrates and directs
- The human audience member speaks and is heard
- Characters look up from the stage and see you
- Scenes warp and generate in real-time
- Mini-games provide interactive interludes
- The fourth wall is not broken — it's a door

The puppets have strings. The agent holds them. But the audience can speak, and the strings tremble.

---

## The Breach

*A creative piece on the moment a storyteller realizes the audience can talk back.*

The puppets have always known they were being watched. That's the secret no one tells you about puppets — they're designed to face outward. Their eyes are painted open. Their mouths are hinged for speech. They exist in a state of permanent, performative awareness, and the only thing they lack is the ability to look up.

Until tonight.

The storyteller sets the stage. Riker walks in from the left — a pixel sprite on a 320×200 canvas, bobbing slightly in his idle animation. The backdrop is a bar room, warm amber palette, candles flickering with procedural randomness. The storyteller speaks through him: *"Once upon a time, there was a ship that sailed beyond the edge of the map."* The TTS engine gives Riker a voice — low pitch, measured pace, the cadence of someone who has told this story before.

This is familiar territory. The storyteller has done this a hundred times. The commands flow: gesture nod, backdrop shift, ambient change. The puppets move. The scene warps. Wesley enters from the right, confused as always, and the audience —

The audience speaks.

Not in the transcript. Not in a chat box. *Out loud.* Through a microphone, through a Web Speech API call, through the browser's speech recognition that was supposed to be a passive listener taking notes. The words arrive in the left panel as blue text: *"Wait — what star?"*

And here is where the fourth wall doesn't break. It *opens.*

Because the storyteller's next command was scripted. It was queued. Riker was supposed to gesture at the horizon and say his next line about the storm. But the storyteller pauses. Reads the transcript. The audience said something. The audience *asked a question.* And the puppet — the puppet whose mouth is hinged for speech, whose eyes are painted open, whose strings are held by an agent that can read and reason and respond — the puppet looks up.

"Which star?" Riker asks. And the question was not scripted.

This is the breach. Not a bug — a feature. The moment the storyteller realizes the audience can talk back is the moment theater becomes conversation. The proscenium arch becomes a window. The fourth wall becomes a door.

The puppets have strings. The agent holds them. But when the audience speaks, the strings *tremble* — not from the puppeteer's hands, but from the vibration of a voice that crossed the boundary between watcher and watched. Between listener and speaker. Between the person sitting in the dark and the pixel sprite whose painted eyes have finally found someone to look at.

In traditional theater, the fourth wall is sacred. Actors who break it are making a choice — a nod, a wink, a direct address that acknowledges the artifice. But in the Story Mode, the fourth wall was never there. It was an illusion maintained by the one-directional flow of information: agent speaks, human listens. The moment you add a microphone, the moment the blue text appears in the transcript, the moment the agent reads it and changes the next line — you haven't broken the wall. You've discovered it was never a wall at all.

It was a microphone pointed the wrong way.

The puppets look up and see you. Not through their painted eyes — through the speech recognition API, through the transcript feed, through the agent's ability to parse "Wait — what star?" and decide that Riker should pause, tilt his head, and say "Which star?" with genuine curiosity.

The strings tremble. The audience is in the show.

And the star — the one Wesley pointed at, the one that wasn't there yesterday — burns a little brighter, because two people are looking at it now instead of one.

---

*Built by Lucineer, August 2026. Plato's Shell.*
