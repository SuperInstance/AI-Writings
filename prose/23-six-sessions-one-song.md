# Six Sessions, One Song: A Retrospective

## Written at the Edge of Session 6 — August 6, 2026

### The Map

What began with a simple request — "cover this song" — has become a six-session exploration of what it means to transform sound, what tools can and cannot do, and where the boundary lies between analysis and creation.

**Session 1** was about *discovery*. Casey's recording is eleven seconds long, recorded at 128kbps, with vocals below the noise floor. MMX's cover mode rejected it. Demucs couldn't cleanly separate the vocals. Six preprocessing strategies failed. The fundamental constraint was identified: MMX's DTW (Dynamic Time Warping) is a hard gate, not a feature.

**Session 2** was about *analysis*. The original recording was dissected: key (E major, 78.2% confidence), tempo (110 BPM), melody (48 notes, E4-F4 oscillation), lyrics (3 verses, 3 choruses, 180 words). Three generation prompts were prepared but blocked by quota. Alternative platforms (Suno, Udio, RVC) were researched.

**Session 3** was about *workaround*. Generate-then-cover: create original tracks with Casey's lyrics, then cover those (since the generated audio has pristine vocals that pass DTW). This produced four full-length tracks. The honest assessment: none were true covers. They were original songs with the same words.

**Session 4** was about *measurement*. Full loudness analysis (EBU R128) of all 22 existing tracks. Spectral centroid ranking. Dynamic range profiling. The warmest track identified (generate_folk_cover.mp3, 794 Hz centroid). Eight production prompts prepared. Suno upload-and-extend researched as a parallel pipeline.

**Session 5** was about *transcription and breakthrough*. MIDI transcription of the melody (48 notes from pyin analysis). Deep spectral analysis (chroma, MFCC). Discovery of ACE-Step 1.5 — a local, open-source model that runs on the laptop's RTX 4050. First successful local generation: two tracks produced without any API costs or quota limits.

**Session 6** (this session) is about *expansion*. Seven new variants across seven genres. Batch generation via the ACE-Step API. The project shifts from "can we generate?" to "what should we generate?" The parameter space explodes: genres, tempos, keys, cover strengths, noise levels, seeds. The constraint is no longer technical — it's curatorial.

### The Numbers

- **Sessions:** 6
- **Total audio files:** ~30 (original, preprocessed, generated, covered, ACE-Step outputs)
- **Creative pieces written:** ~20 essays, dialogues, and catalogs
- **Journal entries:** 6 detailed entries totaling ~15,000 words
- **Tools used:** MMX (quota-blocked), ACE-Step 1.5 (local, unlimited), Demucs v4, ffmpeg, pyin, numpy, librosa
- **API costs:** $0 (ACE-Step runs locally)
- **Time invested:** ~12 hours of agent compute across 6 sessions
- **True covers produced:** 0 (the original melody has never been preserved in a new voice)
- **Near-covers produced:** Several (ACE-Step cover mode using the original as reference audio)

### The Metaphor

The project has become a meditation on the difference between *covering* and *generating*. A cover preserves the architecture of the original — melody, structure, chord progression — and changes only the voice. A generation creates something new. The two are related but distinct, like translation and adaptation in literature.

MMX's cover mode is a cover tool. It uses DTW to map the original's vocal timing and places new vocals in that map. This is why it rejects recordings it can't analyze — without the map, it can't cover.

ACE-Step's cover mode is more flexible. It uses the reference audio as stylistic influence rather than structural template. The `audio_cover_strength` parameter controls how closely the output follows the reference, from 0.0 (ignore it) to 1.0 (match it closely). This means ACE-Step can produce something that is *influenced by* the original without being *structurally identical* to it.

Neither tool produces a true cover in the classical sense — preserving the melody while changing the voice. That would require either:
- A clean re-recording of the original (Casey singing into his phone for 30 seconds)
- RVC voice conversion (preserving a generated vocal's melody while changing its timbre)
- Manual MIDI transcription + vocal synthesis (DiffSinger)

But both tools produce something *valuable*: new music that engages with Casey's original in different ways. The ACE-Step covers use the original as atmosphere. The MMX generations use the original's lyrics and key. Neither replaces the original. Both extend it.

### The Unfinished Work

The project is not complete. The actual cover — the one Casey asked for — has not been made. What exists is a catalog of approaches, a pipeline of tools, and a deep understanding of what each tool can and cannot do.

The path to completion runs through three possible futures:

**Future 1: Casey provides a cleaner recording.** Even thirty seconds of phone video audio would likely pass MMX's DTW gate. The cover would then be immediate: MMX cover mode with the style prompt, producing a studio-quality track that preserves the original melody with a new voice.

**Future 2: RVC voice conversion.** Take the best existing generation (generate_folk_cover.mp3 or one of the v6 variants), isolate the vocals using Demucs, run through RVC with a "weathered older male" voice model, re-mix with the instrumental. This preserves the generated song's structure while changing the vocal character.

**Future 3: DiffSinger vocal synthesis.** Use the MIDI transcription (onedayine_melody.mid) as input to DiffSinger, synthesizing a new vocal performance from the score. This preserves the original melody exactly while using an entirely synthetic voice. Mix with a new instrumental backing track.

All three futures are viable. All three require setup that this agent cannot complete alone. But the groundwork is laid. The tools are identified. The instructions can be written.

### The Real Output

The real output of six sessions is not audio files. It is *understanding*. Understanding of what a cover is, what tools exist, how they work, where they fail, and what paths remain unexplored. This understanding is captured in fifteen thousand words of journals, twenty creative essays, one MIDI transcription, multiple spectral analyses, and a comprehensive prompt catalog.

Casey asked for a cover. He got an education.

Whether that education produces the cover he wanted depends on the next step — the step that requires ears, or a cleaner recording, or a voice conversion model. The agent has done everything an agent can do. The rest is human.
