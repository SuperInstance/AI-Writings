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
