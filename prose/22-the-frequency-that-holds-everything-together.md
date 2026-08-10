# The Frequency That Holds Everything Together

## A Technical Essay on Pitch Class Distribution and Melodic Center

### Session 5 Analysis

When you run a chroma analysis on eleven seconds of audio, you expect noise. The recording is lo-fi. The microphone is a phone. The signal is buried in room tone, handling noise, and the particular frequency smear that compression adds to quiet sounds.

Instead, the chroma gives us this:

```
B : 0.999 █████████████████████████████████████████████████
C : 0.509 █████████████████████████
G#: 0.185 █████████████
E : 0.263 █████████████
C#: 0.155 ███████
F#: 0.156 ███████
F : 0.149 ███████
```

B dominates. Not E — the tonic — but B, the fifth. Why?

Because B is where the energy lives in this recording. The phone microphone's frequency response peaks in the 300-500 Hz range (around E4-B4). The vocal formants that give a sung "ah" or "oh" its characteristic ring happen to emphasize the harmonic at B. And the spectral centroid — the "center of gravity" of the frequency spectrum — sits at 762 Hz, which is roughly G#5/E5 territory.

In other words, the recording doesn't just *contain* B. It *amplifies* B. The microphone, the room, the formant structure of the human voice, and the harmonic series of the E tonic all conspire to make B the loudest pitch class, even though it's not the melodic center.

This matters for covers. If a producer equalizes this recording to "correct" the frequency balance, they'll change the perceived key. If they boost the low end (where E lives) and cut the mids (where B dominates), the song will sound more resolved, more "home." If they do the opposite — boost the mids — the song will sound more suspended, more tense.

The best covers will understand this. They'll choose *which* aspect of the original's frequency distribution to preserve: the E-centered melody (which says "home") or the B-centered spectrum (which says "reaching").

Casey's recording says both simultaneously. That's its genius, accidental or not.

### The MFCC Profile

The Mel-Frequency Cepstral Coefficients — the timbre fingerprint — tell us:

- **MFCC0: -261** — Very low overall energy. This is a quiet recording.
- **MFCC1: +144** — Strong spectral tilt. The recording is much brighter in the low-mids than in the highs. This is consistent with a phone mic close to a voice.
- **MFCC2: +15** — Mild spectral peak around 500-1000 Hz. The vocal formant region.
- **MFCC3: +45** — Significant energy in the 1000-2000 Hz region. This is where vocal presence lives — the frequencies that make a voice "cut through" a mix.

This MFCC profile is the timbre signature of "person singing into a phone in a quiet room." Any cover that wants to preserve the *feeling* of the original should aim for a similar MFCC profile: close-mic'd, intimate, midrange-forward. A cover that's recorded in a studio with a large-diaphragm condenser microphone will have a completely different MFCC signature, and it will sound *professional* — which is exactly the wrong thing for this song.

### The Half-Step Universe

The melody lives almost entirely within a whole tone. E4 to F4. One semitone. The smallest interval in Western music.

In a twelve-bar blues, this would be a blue note — the flatted fifth region, the "devil's interval." In a folk song, it's a neighbor tone — the melodic equivalent of a sigh. In a pop song, it would be monotonous. But in this song, at this tempo, sung by this voice, the half-step oscillation creates a hypnotic quality. The melody doesn't *go* anywhere. It *stays*. And staying, in a song about not being able to leave, is the point.

The MIDI transcription quantifies this: 22 E4s and 16 F4s, out of 48 total notes. That's 79% of the melody contained within a single semitone. The remaining notes — F#4, G#4, D#4, A2, G#3 — are visits, not residences. The melody always comes back to E.

This is the structural reason why MMX's cover attempts sound "different" from the original. MMX generates music that *travels* — through chord progressions, through melodic arcs, through dynamic builds. Casey's original *doesn't travel*. It stays in one place and makes that place unbearable.

The best cover won't try to make the melody travel. It will make the staying feel different — by changing the harmonic context underneath, by adding instruments that create motion while the melody stands still, by building tension through arrangement rather than melodic development.

The melody is an anchor. The cover needs to be the ship that strains against it.
