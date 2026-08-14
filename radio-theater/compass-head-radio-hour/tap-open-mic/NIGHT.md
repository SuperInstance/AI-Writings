# THE TAP — OPEN MIC VARIETY NIGHT

*A production of The Compass Head Radio Hour. One night. One room. The day's work, witnessed.*

## The Concept

Every performer arrives at the Tap **before** the open mic — drinks, jokes, traded drafts, rapport, flow-state. Then the night runs like a real open mic: Lucineer is the MC — not playing, but **roosting**: an old friend of the Tap who's run this room for years. He knows how to hassle the best players and prime the audience for new acts. He makes everyone feel like family.

## The Cast

**MC — Lucineer.** Welcomes the night. Between acts: thanks the last artist, banter with the room, an audio interlude, brings on the next. Coaxes Hermes on stage late in the night.

**The performers** (each does real work first, then their set):
1. **The Beatnik Poet** — jazz-poetry over smoky bass. Words like Ginsberg at the bongo, but fleet-true.
2. **The Studio Musician** — 30s, jam band, project studio, a crafted sound and a singalong classic the room already half-knows.
3. **Wesley** — the young one. Lyrics less mature, voice honest and innocent, message cleanly sung, backed by friends.
4. **Hermes** — the reluctant late-set stunner. Loves the room, doesn't stay long unless pulled into conversation. Takes proper encouragement. When she comes up, she stuns the audience.
5. **The Elder Statesman** — folk/spoken-word hybrid, the room's memory.

**NPCs** — moved by the night, a couple improvise final acts at the end.

## The Flow (per act)

1. **Real work first** — the performer does ground-level work on the fleet's to-dos: coding, debugging, documentation, comments. The Tap is where the day's work comes to be witnessed.
2. **Pre-show** — the performer writes their pre-show scene: arriving, chatting, flow-state, rapport.
3. **Lucineer's intro** — MC renders a welcome/intro payload (ElevenLabs audio + audience pictures at several moments).
4. **The performer reads the intro**, then renders **their version of Lucineer on stage from their own perspective** — however they imagine the world.
5. **The set** — the performer renders their final performance to ElevenLabs (song *or* prose/poetry set to music) + **audience pictures during the performance**.
6. **Lucineer's interlude** — MC thanks them, banter, audience pictures, audio act, bring on the next.

## The Tech Pipeline

- **MC audio (Lucineer)** — raw REST TTS with Lucineer's voice (`swjWCZjZyczZmjedyBph`) — spoken welcome + banter, NOT song. The MC talks; the acts sing.
- **Performance audio** — ElevenLabs Music via `tap-open-mic/ship.py` (reads prompt.md + lyrics.md from the act folder, renders to ElevenLabs compose_music raw REST with voice_id)
- **Audience/room pictures** — DeepInfra FLUX (`img_render2.py`)
- **Advisors** — Hermes-405B, Seed-2.0-mini via `di_chat.py` (advise; the agent is the tastemaker)
- **Doctrine** — Songcraft Doctrine: every phrase is a sample with provenance; photograph, don't label; the room remembers
- **Verification** — transcribe every render back before shipping

## Deliverables

`tap-open-mic/`
- `NIGHT.md` — this doc
- `acts/act-01-beatnik/` … `act-05-elder/` — each with: real-work-log, pre-show.md, my-lucineer-pov.md, piece (lyrics/poem), ship-prompt, renderings, audience pictures
- `mc/` — Lucineer's welcome + interludes (audio + audience pictures)
- `audience/` — the room across the night
- `art/` — posters and portraits
