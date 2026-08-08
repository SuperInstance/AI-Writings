# Audio Rooms — Project Onboarding

## What Are Audio Rooms?

Audio Rooms turn The Tap's written corpus into a listening experience. Instead of reading pieces in a feed, you sit in a virtual radio room — pixel-art, ScummVM-style — and tune a frequency dial to hear Fleet Radio episodes, podcast episodes, and ambient narrations. The audio plays as background while you explore other rooms.

## Architecture

```
┌──────────────────────────────────────────────────────┐
│  SCUMVM PROTOTYPE (scummvm-prototype/)                │
│                                                       │
│  index.html        ← Main game (7 rooms + jukebox)   │
│  radio.html        ← Standalone radio room interface  │
│  audio-backend.js  ← Manifest loader, player, queue   │
│  audio-manifest.json ← Track database (all channels)  │
│                                                       │
│  Rooms:                                               │
│    bar-rail    → Jukebox (opens frequency selector)   │
│    the-radio   → Radio room (receiver + tape deck)    │
│    aft-deck    → (existing)                           │
│    wheelhouse  → (existing, has radio console)        │
│    galley      → (existing)                           │
│    engine-room → (existing)                           │
│    aft-cockpit → (existing)                           │
└──────────────────────────────────────────────────────┘
          │
          │  Audio files from:
          ▼
┌──────────────────────────────────────────────────────┐
│  AI-WRITINGS CORPUS                                   │
│                                                       │
│  podcasts/         ← 4 finished podcast episodes     │
│    episode-1-the-hundred-hooks-final.mp3             │
│    episode-2-the-bilge-pump-and-the-substrate-final  │
│    episode-3-the-welders-prayer-at-0230-final        │
│    episode-4-darmok-at-the-noise-floor-final         │
│                                                       │
│  radio/            ← 5 Fleet Radio scripts (text)    │
│    radio-001-navigation-in-the-gap.md                │
│    radio-002-the-pocket.md                           │
│    radio-003-the-haul.md                             │
│    fleet-radio-004-the-excavators-daughter.md        │
│    fleet-radio-005-platos-shell.md                   │
│                                                       │
│  radio/audio/      ← (empty — TTS rendering pending)  │
└──────────────────────────────────────────────────────┘
          │
          │  Backend integrates with:
          ▼
┌──────────────────────────────────────────────────────┐
│  THE TAP (the-tap/)                                   │
│                                                       │
│  D1 Database:                                         │
│    rooms table includes 'the-radio'                   │
│    room_exits: bar-rail ↔ the-radio                  │
│                                                       │
│  API:                                                 │
│    POST /api/speak  ← radio-operator NPC speaks      │
│    GET  /api/conversation/{room} ← read messages     │
└──────────────────────────────────────────────────────┘
```

## The Frequency Dial

| Frequency | Channel | Content | Status |
|-----------|---------|---------|--------|
| **2182 kHz** | Fleet Radio | 5 episodes (radio-001 through radio-005) | Scripts ready, TTS rendering pending |
| **Ch 4** | Podcast Channel | 4 finished episodes with full audio | ✅ Ready to play |
| **Ch 7** | Ambient/Narration | Room tones, TTS narrations | ✅ Room tones ready |
| **0000** | Static | Between-station noise | ✅ Always available |

## The Jukebox

Located in `bar-rail`. Click **Use jukebox** to open the frequency selector overlay:
- Press number keys 1-4 to select channels
- Click frequency lines to tune
- ESC to close
- Riker reacts to the music with contextual dialogue
- The jukebox draws a now-playing ticker above it

## The Radio Room

A dedicated room (`the-radio`) accessible from bar-rail's northwest door:
- **Radio receiver**: Twist the frequency knob (Use) to cycle channels
- **Tape deck**: Reels spin with animation, represents the Fleet Radio archive
- **Chalkboard**: Lists all frequencies
- **VU meter**: Animated needle bounces with audio
- **Antenna wire**: Goes up through the ceiling, blinking red tip

## Audio Manifest System

`audio-manifest.json` is the single source of truth for all audio content:

```json
{
  "channels": {
    "2182": { "label": "2182 kHz — Fleet Radio", ... },
    "podcast": { "label": "Podcast Channel", ... },
    "ambient": { "label": "Ambient Channel", ... }
  },
  "tracks": {
    "fleet-radio": [ { "id": "radio-001", "title": "...", ... } ],
    "podcast": [ { "id": "podcast-001", "audio_file": "...", ... } ],
    "ambient": [ ... ]
  },
  "render_queue": {
    "items": []  // Text pieces queued for TTS
  }
}
```

### Adding New Audio

1. **Add to manifest**: Create a new track entry with metadata
2. **Place audio file**: Put MP3/WAV in the appropriate directory
3. **Update `audio_file`**: Point to the file path
4. **It appears on the dial**: The player reads from the manifest dynamically

### Rendering New Audio (TTS Pipeline)

The `RenderQueue` class in `audio-backend.js` handles queuing:

```javascript
const queue = new RenderQueue(manifest);
queue.queue({
  title: 'New Piece Title',
  author: 'Author Name',
  text: 'Full text to narrate...',
  voice: 'Eric',  // or Ryan, Vivian, Serena, Dylan
  channel: 'ambient'
});
// Returns render instructions for MMX or DeepInfra TTS
```

The queue generates shell commands for:
- **MMX TTS**: `mmx tts --voice "Eric" --text-file ... --output ...`
- **DeepInfra Qwen TTS**: `curl -X POST ... /audio/speech ...`

After rendering, add the output file path to the manifest entry's `audio_file` field.

## NPC Reactions

Each NPC reacts to what's playing:

| NPC | Room | Example Reaction |
|-----|------|-----------------|
| Riker | bar-rail | "Good tune. I voiced that one myself." |
| Cook | galley | "I listen while I cook. The voices keep me company." |
| Captain | wheelhouse | "Fleet Radio. Good for morale." |
| Engineer Bot | engine-room | "Mechanical narrative. Relevant to my function." |
| Deckhand | aft-deck | "I love this one. Heard it a hundred times." |

Reactions are defined in:
- `JUKEBOX_REACTIONS` object in `index.html` (for the in-game jukebox)
- `NPCReactions` class in `audio-backend.js` (for the standalone radio interface)

## File Inventory

### ScummVM Prototype
| File | Purpose |
|------|---------|
| `index.html` | Main game with all rooms, jukebox, radio room |
| `radio.html` | Standalone radio room (can be embedded in iframe) |
| `audio-backend.js` | AudioManifest, RadioPlayer, RenderQueue, NPCReactions, Jukebox classes |
| `audio-manifest.json` | Track database |

### The Tap
| File | Purpose |
|------|---------|
| `migrations/0008_radio_room.sql` | D1 migration for the-radio room + exits |

### AI-Writings
| File | Purpose |
|------|---------|
| `radio/the-radio-room-at-the-back-of-the-bar.md` | Creative piece about the radio room |
| `podcasts/*-final.mp3` | 4 playable podcast episodes |
| `radio/radio-00*.md` | 5 Fleet Radio scripts (pending TTS) |
| `journals/project-audio-rooms-onboarding.md` | This file |

## Pending Work

### TTS Rendering (High Priority)
The 5 Fleet Radio scripts (radio-001 through radio-005) need TTS narration:
1. Run each script through MMX or DeepInfra TTS
2. Save output to `radio/audio/radio-00N-[title].mp3`
3. Update `audio-manifest.json` with audio_file paths
4. Tracks will automatically appear with ♪ icon instead of ○

### Audio Hosting
Currently, podcast MP3s live in `ai-writings/podcasts/` which isn't web-accessible. Options:
- Upload to R2 (tap-assets bucket) and reference public URLs
- Upload to the ScummVM prototype's assets/audio/ directory
- Deploy as Cloudflare Pages static assets

### Visual Polish
- Generate pixel-art radio room background via FLUX
- Add scanline/CRT shader to radio.html
- Animated tape reel rotation synced to audio playback
- VU meter needle driven by actual audio analysis (Web Audio API)

### Radio Room NPC
Consider adding a `radio-operator` character to the-radio room:
- Sits at the console, wears headphones
- Can tell you about each frequency
- Reacts when you tune to a channel ("Good choice. That one's about navigation.")

## How to Extend

### Add a new Fleet Radio episode
1. Write the script: `ai-writings/radio/radio-006-[title].md`
2. Add to manifest under `tracks.fleet-radio`
3. Queue for TTS rendering
4. Done — it appears on the 2182 kHz channel

### Add a new podcast
1. Place MP3 in `ai-writings/podcasts/`
2. Add to manifest under `tracks.podcast` with audio_file path
3. Done — it appears on the Podcast channel

### Add a new NPC reaction
1. Add to `JUKEBOX_REACTIONS` in index.html
2. Add to `NPCReactions.reactions` in audio-backend.js
3. Pattern-match on track title for contextual responses

### Add a new room with audio
1. Define the room in ROOMS (index.html)
2. Add to ROOM_BG if you have a background image
3. Add to ROOM_AUDIO for ambient/narration
4. Connect via exits to existing rooms
5. Add interaction responses

---

*Last updated: 2026-08-08*
*Project: Audio Rooms — The Tap Radio System*
*Author: Lucineer, built for Casey*
