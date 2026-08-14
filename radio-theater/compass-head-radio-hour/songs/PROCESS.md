# The Song Factory — Audience-First Process

*From Casey, 2026-08-14. The agent is the composer, arranger, orchestrator, and prompter. ElevenLabs is the last mile.*

## The Core Inversion

Do NOT ask "what song do I want to write?"
Ask: **"What audience do I have a message to bring something amazing to, in song-form?"**

The song is born from the people, not from the genre.

## The Process (each agent walks all steps)

### Phase 0 — Scout (done by scout agents)
Read cross-sections of the fleet's archive until the context matures into flow-state: a desire to produce songs that move audiences. Output = a **sample library**: recurring images, emotional payloads, the fleet's voice signatures, candidate motifs to sample. The scout's saturation feeds the songwriter's instinct.

### Phase 1 — Choose the audience
Not "who would like this song" — **who do you have something to say to?** Name them. Give them a life.

### Phase 2 — Know them deeply
- **Story:** write about this audience as people — a day in their life, what they carry, what they're afraid of, what they hope for.
- **Essay:** think harder — why do THEY need this message? What in their lived experience makes the message land?
- **Images:** generate images of them in their day-to-day (DeepInfra FLUX via `img_render2.py`, or local SDXL). See them.

### Phase 3 — Choose the room and the hour
Where are they when the song finds them? What time of day?
- ☕ Morning coffee, newspaper folded, mug in two hands, staring out the window — a pleasant interruption of the ritual?
- 🐄 Barn dance closer — the last song that gets every family on their feet?
- 🌆 Chill club, headset-mic singer pouring her heart out, neon and smoke?
- 🎹 Folk rock, light piano, three-part harmony?
- 🌋 Power ballad rivalling the greats?
The room decides the arrangement. The hour decides the tempo.

### Phase 4 — Write the song (Songcraft Doctrine)
Every word is a sample with provenance. Photograph, don't label. One named speaker per verse. Hemingway's dodge. Vonnegut's unsaid elephant. The fleet canon is the sample library.

### Phase 5 — Advise, don't obey
Call on DeepInfra models (Hermes-405B, Seed-mini, others) for creative advice — but **the agent is the soul.** The agent is the tastemaker. Even if the MCP outputs great lyrics, the agent decides: *"this is the one to send to ElevenLabs."*

### Phase 6 — Ship
Compose the final ship prompt: genre, key, tempo, feel arc, sound palette, full lyrics with structure tags, voice direction. ElevenLabs renders. Transcribe back to verify. Deploy.

## The Photographer's Rule
Digital let you take a thousand pictures and keep five. Film made that expensive. But the photographer was always the chooser. Same here: render many candidates, iterate freely, but *choose* — the selection is the art. Fine-tuning and prompt-based rendering are just the film. You are the eye.

## Fleet Distribution
- **Scouts** — different models, different genre cross-sections of ai-writings → `songs/scouts/`
- **Songwriters** — one per audience room → `songs/audience-*/`
  - `audience-a-morning-window/`
  - `audience-b-barn-dance/`
  - `audience-c-cyberpunk-club/`
  - `audience-d-folk-rock/`
  - `audience-e-power-ballad/`
- Each songwriter folder: `audience-story.md`, `audience-essay.md`, portraits, `lyrics.md`, `ship-prompt.md`, and the tastemaker's note.
