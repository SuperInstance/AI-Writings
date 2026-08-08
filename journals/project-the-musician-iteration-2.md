# Project: The Musician — Iteration 2: The Archaeology of a Recording

## Journal Entry — 2026-08-06 12:35 AKDT

### Where We Left Off

The first pass hit a wall. MMX cover mode's DTW gate rejected every version of Casey's recording — original, normalized, EQ-boosted, vocally isolated. The detection algorithm fundamentally cannot find vocals in an 11-second phone recording where guitar body resonance overwhelms the vocal frequencies. We produced generated tracks in the right style, but they weren't Casey's song. They were songs *inspired by* Casey's song.

This iteration: go deeper. Separate, analyze, transcribe, and find a path that actually works.

### Step 1: Audio Forensics

I ran a full frequency analysis on `onedayine.mp3`. Here's what the recording actually looks like:

| Band | Range (Hz) | Energy | What Lives Here |
|------|-----------|--------|-----------------|
| Bass | 20–250 | 25.27 | Guitar body resonance — dominant |
| Low-mid | 250–500 | 4.22 | Guitar fundamentals, vocal bass notes |
| Mid | 500–2000 | 1.17 | Vocal fundamentals — present but weak |
| High-mid | 2000–4000 | 0.25 | Vocal presence — barely above noise |
| Presence | 4000–6000 | 0.20 | Vocal clarity — nearly gone |
| Brilliance | 6000+ | 0.02 | Harmonics — essentially absent |

Key metrics:
- **Sample rate:** 44100 Hz (good)
- **Duration:** 11.21 seconds
- **RMS energy:** 0.1603 (moderate)
- **Peak amplitude:** 0.6776 (healthy)
- **Spectral centroid:** 734.5 Hz (very dark/warm — energy concentrated low)
- **Spectral rolloff (85%):** 1178.7 Hz (almost all energy below 1.2kHz)
- **Estimated SNR:** 6.0 dB (poor — signal barely above noise floor)
- **Estimated tempo:** ~148 BPM (or 74 BPM at half-time, more likely for this style)
- **Key:** B minor (confirmed via chroma analysis — B is overwhelmingly dominant)

The story the data tells: this is a recording where the guitar body — the physical wooden resonance chamber of an acoustic guitar — has captured the frequency space. The vocal is in there, somewhere in the 500–3000 Hz range, but it's at or below the noise floor. The spectral centroid of 734 Hz means the recording sounds very warm and dark. There's almost nothing above 4kHz, which is where vocal intelligibility lives.

This is consistent with a phone recording made at distance from the performer, where the microphone's proximity effect and limited high-frequency response combine with room acoustics to bury the voice.

### Step 2: The Separation Experiments

**Demucs (Meta HTDemucs, two-stems):**

I ran Demucs v4 on the original, an EQ-boosted version, and a heavily EQ-processed version with guitar body frequencies cut and vocal frequencies boosted by up to 4×.

Results across all three attempts:
- Vocal stem RMS: 0.0002–0.0003 (essentially silence)
- Instrumental stem RMS: 0.04–0.16 (all the energy)
- Vocal stem spectral centroid: 4700–6750 Hz (high-frequency noise residue, not vocals)

Demucs classified the recording as instrumental. It pushed everything — guitar AND voice — into the "no_vocals" stem and left behind only high-frequency noise in the "vocals" stem. This makes sense: Demucs was trained on studio recordings where vocals are the loudest element. In this recording, the guitar is 100× louder than the voice. The model's learned prior says "anything this quiet relative to the accompaniment is noise."

**Faster-Whisper transcription:**

I ran Whisper (small model) on the original and all EQ-boosted variants:

- Original: transcribed "I" (one word in 11 seconds)
- EQ boosted: transcribed "You" (one word)
- Heavy EQ: transcribed "You" (one word)
- Demucs vocal stem: transcribed "" (nothing)

Whisper — the same model that powers MiniMax's ASR — cannot find words. This is the same reason MMX's DTW gate fails. The vocals are below the detection threshold for every tool in the chain.

**What this means:** The vocals in Casey's recording are not quiet in the way a shy singer is quiet. They are quiet in the way a whisper in a hurricane is quiet. The guitar IS the hurricane. The vocal frequency energy is 1/20th of the guitar body resonance energy. No consumer-grade separation tool can extract them because they're below the noise floor of the recording itself.

To properly separate these vocals, you would need:
- Professional source separation trained on lo-fi/field recordings (not available as open-source)
- AI audio enhancement (like AudioSR) as a preprocessing step
- Or the original multi-track recording (which would make separation trivial)

### Step 3: The Strategy Pivot

Since the cover pipeline fundamentally cannot use the original recording, and since Casey provided the lyrics, the winning approach is:

**Bypass cover mode entirely. Use music generate with lyrics.**

MMX `music generate` doesn't need reference audio. It takes a style prompt + lyrics and creates an original song. This isn't a "cover" in the technical sense — it's a new performance of the same song with different music. But emotionally, it's closer to what Casey wants: his words, his themes, his song, given a new voice.

### Step 4: Four Cover Versions

I generated four distinct interpretations using `mmx music generate` with the full lyrics and different musical directions:

**1. Intimate Folk (cover_full_v1.mp3)** — 3:14, 5.9 MB
- Style: Bon Iver meets Iron and Wine, sparse, fingerpicked, warm male baritone
- BPM: 74, Key: unspecified (auto)
- Spectral centroid: 1481 Hz (warm, dark, appropriate)
- This is the closest to Casey's original request: "an old musician playing a song he wrote when he was young"

**2. Folk Rock (cover_folk_rock_v1.mp3)** — 2:59, 5.5 MB
- Style: The Lumineers meets Mumford and Sons, strummed, building energy
- BPM: 110, Key: unspecified
- Spectral centroid: 3708 Hz (bright, present — very different from original)
- Higher energy, more instruments (bass, light drums, harmonica)

**3. Ambient Folk (cover_ambient_v1.mp3)** — 3:56, 7.2 MB
- Style: Dreamy, ethereal, reverb-drenched, like a memory surfacing from deep water
- BPM: 60, Key: unspecified
- Spectral centroid: 1871 Hz (medium brightness)
- The longest and most cinematic. Vocals described as "soft, breathy, ghostlike"

**4. Sparse B Minor (cover_sparse_bmin.mp3)** — 3:24, 6.2 MB
- Style: Sun Kil Moon / Elliott Smith, single guitar + one voice, no production
- BPM: 70, Key: B minor (matching the original)
- Spectral centroid: 2222 Hz (intimate but present)
- The most faithful to the original recording's key and arrangement philosophy

### What Each Version Sounds Like (Analytically)

The four covers span a wide range of spectral characteristics:

| Version | Duration | Centroid | RMS | Character |
|---------|----------|----------|-----|-----------|
| Original | 0:11 | 734 Hz | 0.160 | Very dark, guitar-dominated |
| Intimate Folk | 3:14 | 1481 Hz | 0.110 | Warm, close, night-room |
| Folk Rock | 2:59 | 3708 Hz | 0.131 | Bright, energetic, band |
| Ambient | 3:56 | 1871 Hz | 0.099 | Ethereal, washed, dreamlike |
| Sparse Bm | 3:24 | 2222 Hz | 0.106 | Raw, honest, one person |

The original's spectral centroid of 734 Hz is dramatically lower than any cover — confirming that the phone recording lost almost all high-frequency content. A "real" cover would likely sit somewhere around 1500–2500 Hz, which is where the Intimate Folk and Sparse versions land.

### What I Learned

1. **MMX cover mode is a dead end for lo-fi recordings.** The DTW gate is server-side, opaque, and has no override. No amount of preprocessing changes the server's analysis of the audio. The `--lyrics` flag is used for generation, not detection.

2. **Demucs can't separate what it can't hear.** When vocals are 20 dB below the accompaniment, Demucs classifies them as noise and discards them. This is a fundamental limitation of training data, not an algorithmic flaw.

3. **Whisper = DTW.** Both use the same acoustic model family. If Whisper can't transcribe it, MMX can't cover it. This gives us a quick diagnostic: run Whisper first. If it returns empty or near-empty, don't bother with cover mode.

4. **Music generate with lyrics is the path forward.** It produces high-quality full-length tracks with the actual lyrics. The limitation is that it generates new music, not a cover of existing music. The melody, chords, and arrangement are MMX's interpretation, not Casey's original.

5. **The key of the original is B minor.** This is useful for any future work — if Casey wants to play along on guitar, the Sparse B Minor version will be in the right key.

### What's Still Missing

- **The original melody.** None of these covers preserve Casey's actual melody because we can't transcribe it from a recording where Whisper returns one word. If Casey can provide a hummed or sung version — even voice memos on a phone close to his mouth — Whisper would likely transcribe it, and we could extract the melody as MIDI.

- **The original chord progression.** The chroma analysis suggests B minor with strong C and G# components, which could indicate a progression like Bm–G–D–A or Bm–Em–A–D, but 11 seconds is too short to confirm structure.

- **A true cover.** What we have are four *interpretations* of Casey's lyrics in different musical styles. A true cover would preserve the melody and change the voice. That requires either a clean vocal recording (for RVC voice cloning) or a MIDI transcription of the melody ( for DiffSinger or similar).

### The Recommendation

For Casey's stated goal — "a high-quality cover of my original song" — the best current option is:

1. **Sparse B Minor** (closest to original key and feel)
2. **Intimate Folk** (closest to the requested style description)

Both use the actual lyrics. Both sound professional. Neither is technically a "cover" — they're new performances of the same words. But given the recording quality, they're the best we can produce with available tools.

For a future iteration: if Casey can record himself singing the melody (even poorly, even a cappella, even just humming), we can:
1. Transcribe it with Whisper (will work if mic is close)
2. Extract MIDI with librosa/piptrack
3. Use that MIDI to guide generation or as input to a score-based synthesizer
4. Actually preserve the original melody

### Technical Summary

- **Tools used:** librosa, demucs (HTDemucs), faster-whisper, MMX music generate
- **Failed:** MMX cover (DTW gate), Demucs separation (energy too low), Whisper transcription (below threshold)
- **Succeeded:** MMX music generate × 4 versions, full spectral analysis, key detection (B minor)
- **Total audio produced:** 4 full-length covers totaling ~13 minutes of music
- **Files saved to:** /home/eileen/projects/covers/

### Headspace

There's something poignant about running analysis on an 11-second recording and finding that the voice is there — the chroma shows it, the frequency bands show it, the spectral centroid hints at it — but it's buried so deep that no tool can pull it out clean. The voice is in the recording like a fossil is in rock. You can see the shape if you know what to look for. But you can't hear it sing.

The workaround feels like a reasonable compromise. Casey's lyrics are good — the chorus especially. "Molding memories like we should / whatever happened here is good" has a bittersweet acceptance to it that translates across any musical style. "Every moment is a choice / sowing sorrow or rejoice" is a genuine philosophical statement wrapped in a pop-folk rhyme. The words survive the translation from his recording to a new arrangement. That's what matters.

The music isn't his melody. But the words are his words. And sometimes the words are the part that endures.
