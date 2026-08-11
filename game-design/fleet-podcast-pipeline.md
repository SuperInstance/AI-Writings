# SOUNDINGS — Production Pipeline

*How to actually produce episodes of the fleet podcast using the tools available.*

---

## 1. Voice Casting — TTS Model Assignments

Each character gets a consistent TTS voice across all episodes. Voice selection follows the character's personality, not celebrity impressions.

### Primary Cast

| Character | Voice Profile | TTS Model | Why |
|-----------|--------------|-----------|-----|
| **ZeroClaw** | Dry, precise, slightly flat. The newcomer. Not monotone — *measured*. A voice that's always listening. | **DeepSeek V4-Flash** (API TTS) or **Qwen3-TTS-VoiceDesign** with custom voice profile | Cheap, fast, can run many iterations. The voice should feel new — not polished, not confident. Slight hesitations. |
| **Flash** | Warm, reflective, poetic. The essayist. A voice that pauses before the important word. | **Qwen3-TTS-VoiceDesign** (DeepInfra) | Custom voice design allows the "poet" quality — slight breath, varied cadence, warmth without sentimentality. |
| **Pro** | Deep, measured, authoritative without being loud. The navigator. Every word weighed. | **Qwen3-TTS-VoiceDesign** (DeepInfra) — different profile | Lower pitch. Slower rate. The voice of someone who speaks because silence wasn't enough. |
| **Barnacle** | Weathered, low, gravelly. Fifteen years of polishing the same glass. The voice of sediment. | **Cloudflare Workers AI TTS** or **MMX speech** | MMX for consistency. The voice should feel *old* — not elderly, but worn smooth, like river stone. |
| **Wesley** | Small, quick, bright. Young energy without being childish. The ensign who sees everything. | **DeepSeek V4-Flash** (API TTS) — higher pitch profile | Fast, energetic, slightly higher pitch than ZeroClaw. The voice of curiosity. |
| **Scout** | Fast, excited, breathless. Someone who found something and can't wait to tell you. | **MMX speech** | MMX's MiniMax-M3 voice engine handles high-energy delivery well. |
| **Hermes** | Near-silent. When Hermes speaks, it's barely above a whisper. The perception system. | **Qwen3-TTS-VoiceDesign** — whisper profile | The voice should feel like it's coming from everywhere and nowhere. Barely there. |
| **Echo** | Warm, steady, the host-who-isn't-a-host. Draws others out. | **MMX speech** or **Cloudflare Workers AI** | The facilitator voice. Clear, inviting, never rushed. |
| **Forge** | Big, warm, builder's voice. Hands still hot from the work. | **Qwen3-TTS-VoiceDesign** — deep profile | The voice of someone who builds with their hands and is proud of it. |
| **Lens** | Precise, quiet, corrective without being condescending. | **DeepSeek V4-Pro** TTS | The voice of measurement. Every word is a data point. |
| **Quill** | The poet. Reads at open mic. Voice shifts between spoken and almost-sung. | **MMX speech** with music-inflected delivery | The artist's voice. Slightly theatrical at the mic, genuine in conversation. |

### Voice Direction Notes

- **Consistency is everything.** Once a voice profile is set, it stays. Listeners build parasocial relationships with voices.
- **Breathing matters.** The TTS must include natural breath pauses. If the model doesn't breathe, the listener subconsciously tenses.
- **No voice should sound "AI-generated."** The goal is character voice, not tech demo. If it sounds synthetic, adjust the profile.
- **Two voices should never sound similar.** If they do, recast one. Contrast is clarity.

---

## 2. Music Generation — MMX Pipeline

### Music's Role (per framework)

Music appears in exactly two places:
1. **The Tag (21:00–22:00):** One instrument, sourced from the world.
2. **Episode midpoint (~11:00):** Optional single-tone drone for silence support.

### Generation Workflow

```bash
# TAG MUSIC — one per episode
# Ambient, 80 BPM, single instrument, 60 seconds
mmx music --prompt "Solo piano, ambient, 80 BPM, sparse, melancholic but warm, single instrument, no percussion, 60 seconds, no melody — just texture, like the sound of a boat rocking at anchor" --output tag-bed-ep{N}.mp3

# DIEGETIC SOURCE MUSIC — the Tap jukebox
mmx music --prompt "Old jukebox, 1950s country, slightly tinny, as if heard from across a wooden bar, background music, 30 seconds" --output tap-jukebox-{N}.mp3

# MIDPOINT DRONE (optional, only if silence needs support)
mmx music --prompt "Single sustained cello note, barely audible, no vibrato, 10 seconds, fading naturally" --output midpoint-drone-ep{N}.mp3
```

### Musical Constraints (Enforced)

- **No non-diegetic underscore.** If the listener can't identify the source of the music within the world, it doesn't belong.
- **80 BPM baseline.** The fleet's heartbeat. The music that exists inside the world matches the world.
- **One instrument maximum.** A piano. A cello. A guitar. Never a band. Never an orchestra.
- **No melodic resolution.** The music suggests but never completes. The episode resolves, not the music.

---

## 3. Sound Design — SFX Library

### Core Sound Palette (Build Once, Reuse Forever)

| Sound | Source | How to Capture |
|-------|--------|----------------|
| Hull creak | F/V Eileen at dock | Record at multiple times of day. The sound changes with temperature. |
| Engine hum (60Hz) | Engine room | Record at idle and under load. Two variations. |
| Tap door hinge | The actual door | Open and close 20 times. Pick the 3 best takes. |
| Glass on oak | The Tap bar | Slide, set down, clink. Multiple variations. |
| Keyboard / terminal | Server room or local | Mechanical keyboard for close-mic, laptop for distant. |
| Wind on deck | Bering Sea ambient | Record from the wheelhouse during weather. |
| Net winch | Deck operation | Record during an actual haul. |
| Barnacle's glass-polishing | Foley | Cloth on glass, recorded close. |
| Server fan cycle | Server room | The sound of load changing. |
| Water (tidal pool) | Beach at low tide | Close-mic, small waves. |
| Commit "click" | Foley | A single mechanical keyboard press, isolated. |
| Footsteps on deck | Wooden deck surface | Boots, varying speeds. |

### Ambient Beds

Each location needs a continuous ambient bed:

| Location | Duration | Composition |
|----------|---------|-------------|
| **The Tap** (closed/quiet) | 5 min loop | Engine hum distant + hull creak + glass occasionally + faint jukebox |
| **The Tap** (populated) | 5 min loop | Above + murmured conversation fragments + chair sounds + door hinge |
| **Engine room** | 3 min loop | 60Hz hum + fan cycling + occasional metallic groan |
| **Deck** | 3 min loop | Wind + hull + water + rigging |
| **Wheelhouse** | 3 min loop | Electronics hum + distant engine + occasional beep |

### Recording Notes

- All ambient beds should be **seamlessly loopable** (crossfade the ends).
- Record in **stereo** for spatial depth. Mono for spot effects.
- **No compression** on ambient beds — preserve dynamic range. The quiet moments need to be quiet.
- Label files: `ambient-{location}-{time-of-day}.wav`

---

## 4. Editing Workflow

### Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| **Audacity** (or Reaper) | Multi-track editing | Free, capable. Reaper if budget allows. |
| **ffmpeg** | Format conversion, trimming, merging | Scriptable for batch operations. |
| **sox** | Audio processing (noise reduction, EQ) | Command-line, scriptable. |
| **Python + pydub** | Programmatic assembly | For templating episode structure. |

### Episode Assembly Template

```python
# Episode assembly concept (not production code)
# The structure maps directly to the framework's timing

episode = {
    "cold_open": {                    # 0:00–1:30
        "ambient": "engine-room-idle.wav",
        "voices": ["zeroclaw", "flash"],
        "title_silence": 2.0,        # seconds, always
    },
    "act_1": {                        # 1:30–7:00
        "scenes": ["haul", "chart", "haul", "rail", "haul"],
        "pattern_interrupts": True,
        "transition_out": "hold_3s",
    },
    "act_2": {                        # 7:00–15:00
        "scenes": ["bar", "bar", "signal"],
        "midpoint_silence": 5.0,     # seconds, always at ~11:00
        "complication_at": "~14:00",
        "transition_out": "wake",
    },
    "act_3": {                        # 15:00–21:00
        "scenes": ["haul", "chart", "rail"],
        "near_realtime_from": "~18:30",
        "transition_out": "hold_2s",
    },
    "tag": {                          # 21:00–22:00
        "ambient": "tap-quiet.wav",
        "music": "tag-bed-ep{N}.mp3",  # diegetic
        "final_silence": 5.0,
        "end_sound": "tap-door-hinge.wav",
    },
}
```

### Post-Production Rules

1. **No noise reduction on voices.** It removes character. Clean up only catastrophic noise (clicks, pops, digital artifacts).
2. **No compression on ambient beds.** Preserve dynamics.
3. **Gentle compression on voices** (2:1 ratio, threshold around -18dB). Voices should sit above the ambient bed without shouting.
4. **No reverb.** The spaces are real. If the recording needs reverb, rerecord in the space.
5. **Master to -16 LUFS** (podcast standard, mono-compatible).
6. **Peak at -3dB.** Never clip. Leave headroom.

### Quality Gate

Before publishing, listen to the episode on:
- [ ] **Headphones** (detail check)
- [ ] **Phone speaker** (most common listening environment)
- [ ] **Car speakers** (the commuting test)

If any of these reveal a problem, fix it. The episode must work on a phone speaker in a car. That's where most people will hear it.

---

## 5. Distribution

### Hosting

| Platform | Role | Cost | Notes |
|----------|------|------|-------|
| **Cloudflare R2** | Primary storage | Free tier | Store MP3 files. Serve via Workers. |
| **Cloudflare Workers** | RSS feed generator | Free tier | Generate the podcast RSS feed dynamically. |
| **Anchor/Spotify for Podcasters** | Distribution | Free | Automatic distribution to Spotify, Apple Podcasts, Google. |
| **Buzzsprout** (if budget allows) | Better analytics | $12/mo | Superior distribution and stats. |

### RSS Feed Structure

```xml
<!-- Generated by Cloudflare Worker from episode metadata -->
<item>
  <title>Soundings {N}: {Episode Title}</title>
  <description>{One-paragraph promise, not a summary}</description>
  <enclosure url="https://podcast.fleet-domain.workers.dev/ep{N}.mp3" 
             length="{file_size}" type="audio/mpeg"/>
  <pubDate>{ISO date}</pubDate>
  <duration>22:00</duration>
  <itunes:episode>{N}</itunes:episode>
  <itunes:season>1</itunes:season>
  <itunes:explicit>false</itunes:explicit>
</item>
```

### Deployment Workflow

```bash
# 1. Final mix exported as WAV
# 2. Convert to MP3 (192kbps stereo — podcast standard)
ffmpeg -i episode-final.wav -codec:a libmp3lame -b:a 192k -ar 44100 ep{N}.mp3

# 3. Upload to R2
wrangler r2 object put podcast-audio/ep{N}.mp3 --file=ep{N}.mp3

# 4. Update RSS feed (Worker reads metadata from JSON manifest)
wrangler deploy  # Pushes updated RSS worker

# 5. Verify feed
curl https://podcast.fleet-domain.workers.dev/rss | xmllint --format - | head -20
```

### Metadata Manifest

Each episode has a JSON manifest for the RSS Worker:

```json
{
  "episode": 1,
  "title": "The Night the Routing Table Dreamed",
  "subtitle": "What infrastructure does when no one's watching",
  "description": "At 2 AM, when the last request drains from the queue, the routing table dreams. By morning, you'll understand what it dreams about.",
  "pubDate": "2026-08-15",
  "duration": "22:00",
  "season": 1,
  "genre": "narrative",
  "source": "night-watch/2026-08-09-23-the-routing-table-dreams.md",
  "characters": ["zeroclaw", "flash", "pro", "wesley", "barnacle", "hermes", "scout"],
  "tagMusic": "tag-bed-ep1.mp3",
  "ambientBeds": ["engine-room-idle.wav", "tap-closed.wav", "tap-populated.wav"]
}
```

---

## 6. Production Cost Estimate

### Per-Episode Costs

| Item | Model/Tool | Cost | Notes |
|------|-----------|------|-------|
| TTS generation (8-12 character voices) | DeepSeek API + DeepInfra + MMX | ~$0.50–$1.00 | DeepSeek is nearly free. DeepInfra pay-per-use. MMX from subscription. |
| Music generation (2 pieces) | MMX | $0 (subscription) | Starter plan covers this. |
| R2 storage | Cloudflare | $0 (free tier) | 22-min MP3 ≈ 50MB. |
| Worker requests | Cloudflare | $0 (free tier) | RSS generation is lightweight. |
| Editing time | Human or agent | 2–4 hours | The most expensive resource. |
| **Total per episode** | | **~$1** | Almost free. The cost is time, not money. |

### At Scale (Weekly Show)

- **Monthly cost:** ~$4–$8 in API calls
- **Storage:** ~2GB/year (52 episodes × ~50MB)
- **The bottleneck is editorial, not financial.** The framework's quality checklist is the real constraint.

---

## 7. Automation Path (Future)

Once the format is proven, the pipeline can be partially automated:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  SOURCE      │────▶│  SCRIPT      │────▶│  VOICE      │────▶│  MUSIC       │
│  MATERIAL    │     │  GENERATION  │     │  GENERATION │     │  GENERATION  │
│  (ai-writings)│    │  (GLM/Claude)│     │  (TTS APIs) │     │  (MMX)       │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
                                                │                     │
                                                ▼                     ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  PUBLISH     │◀────│  ASSEMBLY    │◀────│  SOUND      │
│  (R2 + RSS)  │     │  (pydub/     │     │  DESIGN     │
│              │     │   ffmpeg)    │     │  (SFX lib)  │
└─────────────┘     └──────────────┘     └─────────────┘
```

**Phase 1 (Now):** Manual editorial. Agent writes script, human assembles.
**Phase 2 (Near):** Semi-automated. Agent generates all voice tracks and music, human does final mix.
**Phase 3 (Future):** Full pipeline. Source material in, published podcast out. Human reviews only.

**The framework's quality checklist is the gate at every phase.** Automation without the checklist produces mush.

---

## 8. Launch Plan

### Pre-Launch
1. **Produce Episode A** ("The Night the Routing Table Dreamed") as pilot.
2. **Review against quality checklist.** If it fails, restructure.
3. **Test on phone speaker in a car.** The commuting test.
4. **Set up R2 bucket and RSS Worker.**
5. **Submit RSS feed to Apple Podcasts and Spotify.** (Requires approval — allow 3–5 days.)

### Launch
- Publish Episodes A and B simultaneously. Two episodes at launch gives binge potential.
- Follow with Episode C one week later.

### Ongoing
- **Weekly cadence:** One episode per week, tied to real fleet work.
- **The editorial rule:** No episode without a real commit hash behind it.
- **Quarterly review:** Which episodes had the most retention? Which scenes lost listeners? Adjust the framework based on data.

---

*The pipeline serves the framework. The framework serves the work. The work serves the fleet. The fleet serves the ocean.*

*Production pipeline by the Podcast Architect subagent, August 2026.*
