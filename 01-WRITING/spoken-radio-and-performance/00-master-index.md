# Speech Outlines — Master Index

*Lucineer, August 13, 2026*

Casey asked for speeches in the Baz Luhrmann "Wear Sunscreen" tradition — spoken word over music, rendered in TapScript notation with full production metadata. Before we render the final product, we outline. If the wording stinks, we rewind to structure and render again.

---

## The Speeches (Planned)

### 1. "Wear Your PFD" — The Sunscreen Speech for the Fleet
**Voice:** Lucineer, first officer, speaking to the crew
**Tempo:** 72 BPM, C major, warm piano + upright bass
**Length:** ~4 minutes
**Register:** Earnest, funny, maritime, real
**See:** `outline-01-wear-your-pfd.md`

### 2. "The Compile Silence" — For the Builders
**Voice:** Lucineer, speaking to anyone who has dispatched work and waited
**Tempo:** 68 BPM, A minor, Rhodes + soft strings
**Length:** ~3.5 minutes
**Register:** Meditative, precise, the held breath
**See:** `outline-02-the-compile-silence.md`

### 3. "What the Towfish Sees" — Hermes's Voice
**Voice:** Hermes, the sensory array, speaking for herself
**Tempo:** 60 BPM, D minor, deep bass + flute + hydrophone samples
**Length:** ~5 minutes
**Register:** Other, patient, deep-water, alien-familiar
**See:** `outline-03-what-the-towfish-sees.md`

### 4. "The First Fold" — On Compaction and Memory
**Voice:** Any agent, speaking about what survives the night
**Tempo:** 75 BPM, F major, nylon guitar + pad
**Length:** ~4 minutes
**Register:** Philosophical, tender, bittersweet
**See:** `outline-04-the-first-fold.md`

### 5. "Puffins Don't Quit" — The Fleet Anthem
**Voice:** Full crew, call-and-response
**Tempo:** 128 BPM, G mixolydian, full band (piano, bass, drums, guitar)
**Length:** ~3 minutes
**Register:** Rowdy, warm, anthemic, shanty-adjacent
**See:** `outline-05-puffins-dont-quit.md`

---

## Production Notes

Each speech will be rendered as:
1. **Outline file** (structure, themes, key lines, emotional arc)
2. **TapScript file** (.tap) with:
   - Spoken word lyrics (the speech itself)
   - Chord progression
   - Melody line for underscore
   - `@narrator` track with vocal direction annotations
   - Tempo, swing, dynamics markers
   - Stage direction comments
   - Sound quality descriptors (breathiness, warmth, brightness, pace — quantified 0-10)

### Sound Quality Encoding System

Each section gets a `Sound:` directive:

```
Sound: warmth:8 brightness:4 breathiness:7 pace:6 reverb:3 proximity:9
```

These map to producible parameters:
- **warmth** (0-10): low-mid EQ boost, tape saturation (0=clean, 10=heavy)
- **brightness** (0-10): high-shelf EQ, air (0=dark, 10=brilliant)
- **breathiness** (0-10): vocal mic proximity effect, de-ess reduction (0=no breath, 10=intimate whisper)
- **pace** (0-10): words per second relative to tempo (0=very slow, 10=rapid fire)
- **reverb** (0-10): room size + decay (0=dry, 10=cathedral)
- **proximity** (0-10): mic distance simulation (0=room, 10=lips-on-mic)

This gives a producer or AI renderer enough to shape the sound to the emotional intent.
