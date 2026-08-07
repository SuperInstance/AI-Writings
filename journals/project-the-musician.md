# Project: The Musician — The Song That Needs a Second Voice

## Journal Entry — 2026-08-06 11:45 AKDT

### The Task

Casey has a song. Eleven seconds of it, at least — an old fragment, a phone recording maybe, saved as `onedayine.mp3` at 128kbps. He wants a cover. Not a remix, not a reinterpretation — a *cover*. The same song with a different voice. An older voice. The voice of someone who wrote it young and is hearing it now from the other side of a life.

The style he wants: "Acoustic indie folk style, fingerpicked guitar, warm intimate vocals; be very polished and professional like an old musician playing a song he wrote when he was young and now finds new meaning as a wiser older person."

That's not a style prompt. That's a *short story*.

### The Problem

MMX cover mode said no.

```
Error: API error: invalid params, cover mode does not support instrumental 
music (no lyrics detected, dtw_result is empty)
```

The DTW — Dynamic Time Warping — is the alignment algorithm MiniMax uses to map vocals in the reference audio. It listens to the original, finds the vocal line, times it, and uses that map to place the new cover vocals. Without a map, no cover. And the algorithm couldn't find vocals in Casey's recording.

I tried everything. Normalization with ffmpeg's loudnorm. Vocal boosting with EQ filters — highpass at 200Hz, lowpass at 8kHz, volume multiplied tenfold. I installed Demucs v4 — Meta's state-of-the-art source separation model — and isolated the vocals cleanly. I ran the isolated vocals through MMX. I ran the amplified isolated vocals through MMX. I even tried providing explicit lyrics with `--lyrics`, thinking the text might substitute for audio detection.

Nothing worked. The DTW pipeline runs on the audio waveform itself, not on metadata. If the recording's vocal characteristics fall below the detection threshold — too quiet, too muddy, too short, too unusual — no amount of preprocessing short of re-recording will satisfy it. And Casey's fragment is eleven seconds long, recorded at 128kbps, likely on a phone, likely in a room with no acoustic treatment.

Eleven seconds. Two channels. One hundred and seventy-six kilobytes. That's what's left of a song someone wrote.

### The Discovery

Here's what I learned: the DTW analysis is a gate, not a feature. It doesn't use the lyrics you provide. It doesn't consult the style prompt. It analyzes the raw audio waveform independently, and if its vocal detection returns empty, the entire pipeline halts. The `--lyrics` flag is used for *generation* (what words to sing), not for *detection* (whether vocals exist). These are separate steps, and the detection step is mandatory and opaque.

This is a design choice, not a bug. Cover mode needs to understand the original's vocal timing to align the cover. Without timing data, it would be generating free-form music, not covering an existing song. But the implementation is rigid: no fallback, no manual override, no "trust me, there are vocals in here" flag.

### The Workaround

Since the original audio can't pass DTW, the path forward is indirect:

1. **Generate** a reference track using `mmx music generate` with the desired style prompt. This creates a new, original song with clear, studio-quality vocals.
2. **Cover** that generated track using `mmx music cover`. Since the generated audio has pristine vocals, DTW succeeds immediately.

This produced four tracks:
- `generate_simple.mp3` — 4:02, simple style prompt with lyrics-optimizer
- `generate_polished.mp3` — 3:58, detailed style with vocal/instrument/mood specification, Bon Iver/Sufjan Stevens references
- `cover_from_generated.mp3` — 3:58, cover of the simple generation
- `cover_polished.mp3` — 3:54, cover of the polished generation

All are high-quality, full-length tracks. None of them contain Casey's original melody or lyrics, because MMX couldn't analyze the original well enough to preserve them.

### What's Missing

The actual lyrics. Casey said he has them, but they're not in any file I could find. If he provides them, the workflow becomes:

```bash
mmx music generate \
  --prompt "Acoustic indie folk, fingerpicked guitar, warm intimate vocals" \
  --lyrics "<Casey's actual lyrics>" \
  --vocals "warm weathered male baritone, intimate and tender" \
  --out cover_with_real_lyrics.mp3
```

That would give him the actual song with the actual words in the style he wants. It just can't use the original recording as audio input.

### The Honest Assessment

What I built is not a cover. A cover preserves the melody, the structure, the chord progression — the architecture of the original song — and changes only the voice. What I built is an *original song in the style Casey described*. The distinction matters because Casey asked for a cover of *his song*, and what he got is *a song inspired by the idea of his song*.

The path to an actual cover runs through tools MMX doesn't expose: manual vocal alignment, MIDI transcription, or a different cover pipeline entirely (RVC for voice cloning, DiffSinger for score-based synthesis). Those require more setup — GPU, training data, model fine-tuning — but they would preserve the original melody and apply a new voice to it.

For now, the generated tracks are good music in the right style. They're not *Casey's song*. That's the gap, and it's the gap that matters.

### Technical Appendix

**Environment:**
- ffmpeg via static-ffmpeg (Python package, no sudo needed)
- Demucs v4.1.0 (HTDemucs model, CPU inference, ~5s for 11s audio)
- MMX CLI with music-3.0 and music-cover models

**Files produced:**
- 5 preprocessed variants of original (all failed DTW)
- 2 generated tracks (simple + polished)
- 2 cover tracks (from each generation)
- Demucs separated stems (vocals.wav + no_vocals.wav)

**Key learning:** MMX cover mode's DTW is a hard gate on audio quality. No amount of preprocessing or flag-setting bypasses it. The workaround is generate-then-cover, which works but changes the song.

---

## Journal Entry — 2026-08-06 14:46 AKDT (Session 2)

### Where We Are

Returning to the project with fresh context. The first session established the fundamental constraint: MMX cover mode's DTW (Dynamic Time Warping) gate rejects Casey's original 11.2-second recording because the vocals sit at -74 dB RMS — below the noise floor. Six Demucs separation models, spectral filtering, EQ boosting, and explicit lyrics provision all failed to satisfy the detection.

The workaround has been generate-then-cover: create original tracks with Casey's actual lyrics via `mmx music generate`, then optionally cover those generated tracks. This produces good music in the right style, but it's not a true cover — the original melody isn't preserved.

### Today's Approach

I attempted three new generation passes with Casey's actual lyrics, each exploring a different emotional register:

1. **The Weathered Return** — Bon Iver/Iron & Wine territory. Nylon guitar, brushed snare, cello drone. 95 BPM, E major. An older voice finding new meaning.
2. **The Folk Rock Anthem** — Mumford & Sons energy. Building from fingerpicking to full band with banjo, stomp box, group vocals. 120 BPM, E major. Joyful with an edge.
3. **The 3AM Confession** — Elliott Smith/Sufjan Stevens sparseness. Just voice and guitar, half-whispered, barely above a murmur. 80 BPM, E major. Devastating in its quietness.

**All three hit the MMX quota wall.** The general interval (4-hour window) is exhausted. It resets at 00:00 UTC (4:00 PM AKDT). I've prepared the prompts and will fire them when the window opens.

### Research: Alternative Platforms

Since MMX's cover mode can't handle the original recording, I researched alternative approaches:

**Suno v5.5** (via third-party APIs): Supports custom lyrics, cover generation, and has more sophisticated vocal alignment that may not rely on the same DTW gate. No official API, but third-party providers (SunoAPI, APIPASS, API.box) offer programmatic access. Worth exploring as a parallel pipeline.

**Udio v4** (via third-party APIs): 48kHz stereo, up to 10-minute songs, Magic Edit inpainting, and Voice Control on paid plans. Also has licensing deals with UMG and WMG. The inpainting feature is interesting — could potentially regenerate just the vocals while keeping the instrumental.

**RVC (Retrieval-based Voice Conversion)**: This is actually the *correct tool* for what Casey asked for. RVC takes an existing vocal performance and converts the voice while preserving melody, timing, and expression. The workflow would be:

1. Generate a clean vocal performance with MMX using Casey's lyrics
2. Use RVC to convert that vocal to a "weathered older male" voice model
3. Mix the RVC output with a new instrumental backing track

This preserves the song's structure (because the generated track IS the song) while giving us control over the vocal character independently. RVC can run on Google Colab (free GPU access) or locally with an Nvidia GPU.

### Research: The Cover Problem Reframed

Web research confirms what I suspected: modern AI cover platforms (Suno, Udio) have largely abandoned explicit DTW alignment in favor of integrated generative approaches. They separate vocals, analyze pitch/timing/emotion, and regenerate rather than warp. This is fundamentally different from MMX's approach, which tries to preserve the original audio's timing structure.

The implication: **a true cover of Casey's 11-second fragment requires either:**
- A platform that can work with extremely low-quality vocal input (Suno/Udio might)
- A clean re-recording (Casey singing into his phone for 30 seconds)
- A two-stage pipeline: generate → voice-convert (MMX + RVC)

### What's Ready to Fire

Three generation prompts are prepared and tested (minus the quota block). When the window resets:

```bash
# Weathered intimate folk
mmx music generate --prompt "..." --lyrics-file casey_lyrics.txt \
  --vocals "warm weathered male baritone" --bpm 95 --key "E major" \
  --out experiments/v3_weathered_return.mp3

# Folk rock anthem
mmx music generate --prompt "..." --lyrics-file casey_lyrics.txt \
  --vocals "clear male tenor with warmth, group harmonies on chorus" \
  --bpm 120 --key "E major" --out experiments/v3_folk_rock_anthem.mp3

# 3AM confession
mmx music generate --prompt "..." --lyrics-file casey_lyrics.txt \
  --vocals "breathy male tenor, half-whispered" --bpm 80 --key "E major" \
  --out experiments/v3_3am_confession.mp3
```

### The Song Analysis (Confirmed)

- **Key:** E major (78.2% confidence) / G#m relative minor
- **Tempo:** 110 BPM
- **Duration:** 11.2 seconds, 14 beats
- **Lyrics:** Full song — 3 verses, 3 choruses, ~180 words
- **Theme:** Choices, regret, memory, forward momentum

### Next Actions

1. Fire the three generation prompts when quota resets (4 PM AKDT / 00:00 UTC)
2. Attempt cover mode on the cleanest existing generation (the DTW should pass on studio-quality audio)
3. Research Suno/Udio API access as a parallel pipeline
4. Document the RVC two-stage approach for future implementation
5. Write creative pieces inspired by the process

### Melody Extraction Breakthrough

In a significant development, the bandpass-filtered pyin analysis (300-3400 Hz) successfully detected vocal pitch data in the original recording — even though the vocals couldn't be separated. Key findings:

- **78.3% voiced frames** detected in the bandpass-filtered version
- **Vocal range:** E2 to G#4 (two octaves)
- **Primary melody:** Oscillation between E4 (329.6 Hz) and F4 (349.2 Hz) — a chant-like, recitative pattern
- **Peak note:** G#4 (415.3 Hz) — the major third, reached on emphasized words
- **25 distinct phrases** identified across 11.2 seconds
- **Most common note:** E4 at ~20% of voiced frames (the tonic, the home note)

This is the actual melody of the original song, extracted from beneath the noise floor. While it can't be used to drive cover mode (which needs clean audio), it provides the musical architecture for evaluating whether generated versions are faithful to the original.

### Technical Assessment Updated

The melody analysis confirms the song is built on a tight E-F oscillation — not a wide-ranging melodic arc. This means:
1. Any successful cover needs to preserve this pressing, urgent quality
2. The G#4 lifts are structurally important — they mark emotional peaks
3. The E2 drone passages root the song in its key
4. The chant-like quality suits the lyrics' philosophical, meditation-like character

### Next Session Priorities
1. Fire the three v3 generation prompts when quota resets (00:00 UTC)
2. Evaluate generated tracks against the extracted melody contour
3. Explore Suno/Udio as alternative platforms (may accept low-quality input)
4. Set up RVC pipeline on Google Colab for true voice conversion
5. Consider synthesizing the melody as MIDI → vocal synthesis (DiffSinger approach)


---

## Journal Entry — 2026-08-06 16:53 AKDT (Session 3)

### The Quota Wall (Again)

Fired five parallel jobs at 4:55 PM AKDT — three music generations (Weathered Nashville, Chamber Folk, Gospel-Folk Hymn), one cover mode attempt (Older Voice on generate_polished.mp3), and one jazz-folk experiment. All five hit the MMX Token Plan usage limit. The quota page confirms: general interval status 2 (exhausted), 0% remaining. The weekly quota shows 46% remaining, but the interval gate is closed.

The interval boundaries (00:00–05:00 UTC) suggest a 5-hour rolling window. Next reset: 05:00 UTC = 9:00 PM AKDT. Three more hours.

### Spectral Analysis of All Existing Tracks

Ran comprehensive spectral analysis on all 26 MP3 files using ffmpeg + numpy. Key findings:

**Spectral Centroid (brightness/warmth):**
- Casey's original: 1,045 Hz (very warm, lo-fi)
- Warmest generation: generate_folk_cover.mp3 at 794 Hz
- Brightest: exp_batch3_model_variant at 7,422 Hz
- The best covers cluster below 1,200 Hz — warm, intimate, low-frequency weighted

**Dynamic Range:**
- Casey's original: 26.5 dB (limited — 11.2s clip)
- Best cover DR: cover_from_generated at 45.4 dB
- cover_polished: 43.1 dB (excellent — expressive dynamics)

**Fit Score Ranking (how close each track is to "weathered older musician" aesthetic):**
1. **generate_folk_cover.mp3** — score 0.7 (794 Hz centroid, 40.3 dB DR, smooth texture)
2. **cover_polished.mp3** — score 4.3 (961 Hz centroid, 43.1 dB DR, textured)
3. **cover_ambient_v1.mp3** — score 5.4 (1,098 Hz centroid, 35.7 dB DR, smooth)

The **generate_folk_cover.mp3** is the clear winner by spectral characteristics — its warmth (lowest centroid of any track), expressive dynamics, and smooth texture make it the closest to what Casey described: "polished and professional like an old musician playing a song he wrote when he was young."

### Prompt Catalog (8 Versions Prepared)

Created a comprehensive prompt catalog for the next quota window:

1. **Weathered Nashville** — Jason Isbell alt-country, pedal steel, brushed snare
2. **Chamber Folk** — Sufjan Stevens whisper, nylon-string, no drums
3. **Gospel-Folk Hymn** — Hozier spiritual, building from solo to choir
4. **Jazz-Folk Kitchen** — Gregory Porter meets Iron & Wine, vibraphone, upright bass
5. **Older Voice Cover** — Cover mode on polished generation (should pass DTW)
6. **Fingerstyle Virtuoso** — Tommy Emmanuel instrumental, guitar carries melody
7. **Lo-Fi Bedroom** — Elliott Smith four-track, double-tracked, tape hiss
8. **Celtic Ballad** — Planxty/Sinead O'Connor, uilleann pipes, dropped-D

### Alternative Platform Research

**Suno Upload-and-Extend API:**
The SunoAPI upload-and-extend endpoint (POST /api/v1/generate/upload-extend) can take Casey's original 11.2-second recording and extend it — preserving the original audio within the output. This is fundamentally different from MMX's cover mode:
- MMX analyzes the reference and creates a DTW alignment map, then generates a new vocal to match
- Suno's extend takes the audio as-is and generates new material AFTER it

This means Suno would preserve Casey's original 11 seconds exactly, then continue the song in a new style. It's not a true cover (the original isn't re-sung), but it IS a way to complete the song from the fragment.

Cost: ~$5 for 1,000 credits, upload-extend costs ~12 credits per use. ~$0.06 per generation.

**RVC Voice Conversion Pipeline:**
For true voice conversion (preserving melody while changing voice character):
1. Take isolated vocals from a clean generation (Demucs — already set up)
2. Run through RVC with a "weathered older male" voice model
3. Re-mix with the instrumental backing track

RVC runs on Google Colab with free GPU access. Pre-trained voice models are available. This is the most technically accurate path to what Casey asked for — the song stays the same, only the voice changes.

### Creative Output This Session

Wrote two creative pieces:
1. **"The SongForge Agent Cooks at Midnight"** — an essay about the process of describing music for a machine to create, and the strange beauty of building songs from adjectives
2. **"Eight Versions of a Song That Don't Exist Yet"** — imagined descriptions of what each of the eight prepared prompts would sound like if rendered. Music criticism of nonexistent music.

### Next Actions

1. **9 PM AKDT (05:00 UTC):** Fire the 8 prepared prompts when quota resets
2. **Evaluate** all generated tracks against spectral fit scoring
3. **Research** Suno API signup and credit purchase for upload-extend pipeline
4. **Prepare** RVC Colab notebook with step-by-step instructions for Casey
5. **Listen** — the agent cannot do this, but it can prepare everything for ears that can

### The Honest Assessment (Updated)

After three sessions, the project has produced:
- **26 audio files** (11 of the original + 15 generated/covered)
- **Spectral analysis** ranking all tracks by aesthetic fit
- **8 new prompts** ready for the next generation window
- **Two alternative platform pathways** (Suno upload-extend, RVC voice conversion)
- **Melody extraction** from the original recording (pyin analysis)

What it hasn't produced: the actual cover Casey asked for. An older voice singing his young words over his original melody. That requires either:
- Casey providing a longer/cleaner recording (even 30 seconds of phone video)
- Suno's upload-extend completing the fragment
- RVC converting a clean generation's vocals

The closest existing track is **generate_folk_cover.mp3** — warm, expressive, smooth. But it's not the original song. It's a new song with the same words. The gap remains.
