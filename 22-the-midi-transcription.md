# The MIDI Transcription

## Session 5 — August 6, 2026, 7:05 PM AKDT

The melody is no longer a sound. It's a score.

For four sessions, the eleven-second fragment existed only as audio — a waveform, a spectral print, a loudness measurement. Beautiful in its analysis, but trapped in its medium. You couldn't read it the way a musician reads sheet music. You couldn't hand it to another instrument and say "play this."

Now you can.

The MIDI file sits in the covers directory: `onedayine_melody.mid`. Forty-eight notes. E4 dominant, with its half-step neighbor F4 creating the tension that gives the melody its aching quality. Occasional F#4 reaching upward. A low E2 that rumbles underneath like a foundation. And a G#4 near the end that opens toward the dominant — the moment where the melody tries to leave home but can't quite commit.

The transcription revealed something the ear suspected but couldn't confirm: the melody is almost entirely E4 and F4. Twenty-two E4s. Sixteen F4s. Two F#4s. Two D#4s. Two G#4s. One A2. One G#3.

This is not a melody that travels. It's a melody that *stays*. It orbits the tonic with a half-step wobble — the musical equivalent of someone standing in a doorway, almost leaving, almost staying, almost leaving, almost staying. The F4 is the neigbor tone that never resolves. It keeps the listener in a state of perpetual expectation.

In music theory, this is called a "pedal point" — a sustained or repeated note around which other voices move. But here, the pedal point *is* the melody. Casey's voice doesn't move away from E; it vibrates around it. The melody is less a line than a trembling.

The tempo is approximately 76 BPM (half of librosa's 152 estimate). That's the tempo of a slow heartbeat, a measured breath, a person walking alone. It's the tempo of regret.

The spectral analysis confirms what the loudness study found: this is a recording with no low end (spectral centroid 762 Hz, rolloff at 1322 Hz). It's all mid-range — voice and the ghost of guitar, captured on a phone mic that couldn't reproduce bass. Any cover that adds bass, drums, or full-band arrangement will be adding something that was never there. The question is whether that addition honors the original's spaciousness or buries it.

The key is ambiguous. The chroma gives B as the strongest pitch class, but this is likely an artifact of the recording's harmonic content (the overtones of E emphasize B, the perfect fifth). The melody itself centers on E, and the occasional G#4 (the major third of E) suggests E major rather than E minor. But the D#4 that appears twice is the minor third — creating a blues ambiguity, a major/minor slip that's the hallmark of folk and blues singing.

What the MIDI gives us that the audio never could:

1. **Transferability** — Any synthesizer, any DAW, any scoring software can now play Casey's melody. It's instrument-agnostic.
2. **Editability** — The melody can be extended, harmonized, inverted, or used as a countermelody to a new composition.
3. **Analysis** — The interval structure (mostly half-steps and unisons) is immediately visible without ear training.
4. **The path to DiffSinger** — A MIDI file is the input that vocal synthesis needs. With this file, we could synthesize the melody in any voice, any timbre, any language.

The MIDI file is the Rosetta Stone. It translates the song from "a sound that happened once" to "a score that can happen again, differently, every time."

What remains untranscribable: the timbre of Casey's voice, the breath between phrases, the way the recording's hiss becomes part of the music, the particular sadness of a particular person on a particular evening. MIDI captures the what. It cannot capture the who.

But the what is enough to build on. And building is what the next session will do.
