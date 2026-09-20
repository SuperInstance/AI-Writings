# Quartet-Arrival — Lead Sheet

*A Compass Head Radio Hour — Song Factory lead sheet. Playable now; renderable when quota returns.*

## Song Header

| | |
|---|---|
| **Title** | Quartet-Arrival |
| **Genre** | A cappella vocal counterpoint (Renaissance-style round, modern close harmony) |
| **Tempo** | 80 BPM (4/4, spacious) |
| **Key** | D major |
| **Mood** | Expectant, radiant, resolving |
| **Instruments** | Four vocal parts. *No instruments.* An instrument would be a fourth presence that wasn't *the* fourth. |

**The idea in one line:** the music performs the arrival. Three voices sing the same phrase in staggered canon, sparse and familiar — the high register a gap in the stereo field, unoccupied for years — and the fourth voice enters last, on top, and the harmony changes from sparse to full in a single bar.

---

## Chord Chart — The Canon's Harmonic Skeleton

The piece is a round: every voice sings the same eight-bar phrase at staggered entries. The chart below is the phrase's implied harmony — with only three voices singing, the top of each chord is deliberately *missing*.

```
Phrase (8 bars, 4/4 @ 80 BPM, D major)
   | D      | A/C♯   | Bm     | G      |
   | D/A    | A7     | D      | D      |

Melody bones (one voice's line, rising):
   | D–F♯–A | A–C♯–E | B–D–F♯ | G–B–D |
   | D–F♯–A | A–C♯–E | D–F♯–A | resolve |
```

While only three voices sing, the phrase's implied A/C♯ and the high F♯s are *pointed at but not touched* — the arrangement leaves a hole exactly where the fourth voice's register should be. The census of the harmony reports an address, not a flaw.

---

## Entry Map — Who Sings When

Entries are 2 bars apart. Three voices enter, weave through the phrase twice (the texture thin at the top), and then — on the third pass — the fourth arrives.

```
Bar 1:   Tenor    begins the phrase (mid register, D3–A4)
Bar 3:   Baritone enters the same phrase an octave down (D2–D4),
         rounding beneath, slow and grounded
Bar 5:   Alto     enters (A3–D5), weaving between them

         — two full passes of sparse three-voice counterpoint —
         the top line simply not there, the empty register sung around

Bar 17:  SOPRANO  — the fourth, arrives LAST — enters on the phrase's
         third pass, on a high D5–F♯5, filling the gap in one bar.
         The harmony goes sparse → full in that single bar.
```

**The moment:** the soprano's entry is not loud — it is *complete*. Every chord the trio had spent years singing around suddenly has its top. A door closes and a room becomes a home in the same motion.

---

## Voices & The Stereo Field

| Voice | Register | Pan | Role |
|---|---|---|---|
| Tenor | D3–A4 | L (40%) | carries the phrase, patient |
| Baritone | D2–D4 | R (40%) | the ground; rounds beneath |
| Alto | A3–D5 | L–R weave | the middle, binding |
| **Soprano** | **D4–A5** | **Center, slightly forward** | **the absent register — enters last, occupies the gap** |

For years the stereo field had a hole in it: center-top, empty. The soprano stands in it. Her entry should read spatially as *the missing voice taking its seat* — center, a touch forward, slightly brighter than the others.

---

## Dynamics & Shape

- **Expectant:** the trio begins at **mp**, warm but incomplete. Each new entry adds a little warmth, never volume.
- **The arrival:** the soprano enters **mf, radiant** — full but not overpowering. The fullness must come from *register*, not loudness.
- **Resolution:** a final pass at **f**, all four voices, then a **sustained D major chord** (D–F♯–A–D) with a gentle rallentando.
- **The last voice:** as the final chord decays, voices drop out one at a time — baritone, tenor, alto — leaving the soprano holding the top D alone, then releasing. The last voice completes the chord, and then the loop is whole.

---

## Renderer Notes (when the music API quota returns)

1. Render at 80 BPM, 4/4, D major, a cappella — **no instruments, no percussion, no drone**. Silence is a texture here.
2. Four distinct vocal timbres (3 adult mixed voices + 1 bright soprano). The soprano must be a *person*, not a synth layer — her entrance is the plot.
3. Entries at exact 2-bar offsets per the map above; two full sparse passes before the soprano's third-pass entry.
4. Spatial placement: the three trio voices pan L/R/weave; the soprano enters center, slightly forward — the stereo-field gap visibly filled.
5. The harmony must audibly go sparse → full in the soprano's first bar: keep the trio's top register empty (no alto doubling above D5) until bar 17.
6. Ending: sustained D major, rallentando, voices dropping one at a time, soprano's top D ringing last and releasing into silence.
7. When MMX returns, produce iterative images: the empty mic stand, the census printout, the fourth voice arriving late and choosing the empty spot.

---

## Story

📖 [The story of its making](../songs/quartet-arrival/story.md) · 🎼 [Render-ready spec](../songs/quartet-arrival/spec.md)
