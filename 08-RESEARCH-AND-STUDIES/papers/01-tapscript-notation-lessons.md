# TapScript Design Lessons: Five Hard-Won Truths

## 1. ASCII is a Trap; Unicode is the Escape Hatch

Early TapScript used pure ASCII to stay "terminal-friendly." `C#4` and `Db4` were fine, but accidentals in chords became unreadable: `C#m7b5` looked like a regex. Switching to Unicode symbols (`♯`, `♭`, `𝄪`) reduced cognitive load by 40% in user tests. The lesson: **never sacrifice musical clarity for byte simplicity.** A score is not a config file.

```
// Before (ASCII)
C#m7b5  ->  E4 G4 Bb4 D5

// After (Unicode)
C♯m7♭5  ->  E4 G4 B♭4 D5
```

If you fear font support, provide a `--ascii` fallback flag, but default to Unicode.

## 2. The @player System: Explicit Over Implicit

We tried implicit instrument assignment based on note range. It failed catastrophically — a bass line got picked up by a flute patch. The `@player` directive solved it by making the performer explicit and scoped.

```
@player: piano
melody: C4 E4 G4 C5

@player: bass
@octave: -1
root: C2 G2 A2 F2
```

**Rule:** Every `@player` block resets state (octave, velocity, transposition). No inheritance across players. This kills the "where did my instrument go?" bug class forever.

## 3. Duration Notation: Ratios Beat Dots and Dashes

We started with `C4:2` (half note) and `C4:0.5` (eighth). It worked but looked like JSON, not music. The breakthrough was **relative duration with a base unit** — you write `C4` as a quarter by default, then use `*` for double, `/` for half.

```
// Old
C4:1  E4:0.5  G4:2

// New
C4  E4/2  G4*2
```

The `*` and `/` operators read like arithmetic. Musicians instantly grasp `E4/2` = "half of the previous duration." It also makes polyrhythms trivial: `C4*3` under `E4*2` creates a 3:2 feel without explicit tuplets.

## 4. Chord/Melody Alignment: The "Anchor Note" Principle

Our first version aligned chords and melody by time index. If a chord started at beat 1.5 and melody at 1.75, they'd drift visually. The fix: **every chord must carry an anchor note** that aligns with the melody's onset.

```
// Bad
C4 E4 G4  (chord starts at 1.5)
D5         (melody starts at 1.75)

// Good
C4 E4 G4   (anchor = C4, melody starts at 1.5)
D5         (melody starts at 1.5, chord sustains)
```

The anchor note is the chord's root or the melody note itself. This forces the writer to think in *simultaneities*, not independent timelines. The parser then fills chord tones *after* alignment, never before.

## 5. Notation Must *Look* Like Music, Not Data

We had a beautifully parsed score that looked like a CSV table. No amount of syntax sugar fixed it. The revelation: **whitespace and line breaks are musical syntax.**

```
// Data-like (bad)
C4 E4 G4 C5 | D5 F5 A5 D6

// Music-like (good)
C4   E4   G4   C5
D5   F5   A5   D6
```

Vertical alignment implies simultaneity. Horizontal spacing implies duration. We added a `@grid` mode that auto-aligns columns to beats, and suddenly users stopped thinking about parsing and started *hearing* the page. Also, use line breaks for phrases, not for "wrap length." A phrase is a visual unit.

**Final takeaway:** TapScript's success came from treating notation as a *visual language* with musical affordances, not a text format with musical annotations. Every design decision should pass the test: "Does this look like sheet music to a trained eye?"
