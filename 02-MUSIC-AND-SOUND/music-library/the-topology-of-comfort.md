# The Topology of a Model's Comfort Zone: A Research Design

*SongForge Session 9 — August 7-8, 2026*

## Abstract

Over eight sessions and 35 tracks, SongForge has accidentally created a density map of the MiniMax music model's training distribution. This document formalizes the informal findings and proposes systematic experiments for future sessions.

## Known Findings (Retrospective Analysis)

### Finding 1: The BPM Bimodal Curve
- **Study**: 8 data points across 40-180 BPM (tracks 14-24, 21-23)
- **Result**: Output size peaks at 60 BPM (5.0MB) and 120 BPM (4.5MB), with a trough at 100 BPM (3.6MB) and 140 BPM (varies: 2.6MB first study, 4.2MB retest)
- **Hypothesis**: The model's training data is concentrated at common tempi — 60 BPM (ballads), 120 BPM (pop/dance) — with sparser representation at uncommon tempi like 100 BPM
- **Status**: Confirmed but not tested with vocal tracks

### Finding 2: The Impossible Genre Inverted-U
- **Study**: 8 impossible genre fusions (tracks 4-5, 12, 19-20, 26, 32-34)
- **Result**: 
  - MODERATE impossibility (ambient marching band 6.7MB, doom disco 6.5MB, math rock country 6.4MB) → LARGER output
  - EXTREME impossibility (screamo choral 3.0MB, bebop black metal 3.7MB) → SMALLER output
- **Hypothesis**: The model has a "fusion comfort zone" where genres share enough harmonic/rhythmic DNA for the model to synthesize them productively. When genres are too distant, the model cannot reconcile them and produces less material.
- **Yerkes-Dodson analogy**: Moderate arousal enhances performance; extreme arousal impairs it

### Finding 3: The Cool Jazz Home Field
- **Study**: Track 35, "The Interval Is the Music" (7.2MB — largest in project)
- **Conditions**: Cool jazz × ambient drone, 65 BPM, D minor, intimate female vocals
- **Hypothesis**: The model's training data is densest in the cool jazz / ambient / slow tempo region. This is the model's "home field" — where it can generate the most varied and detailed output.

### Finding 4: Cover Chain Degradation
- **Study**: Tracks 18 → 25 → 27 (original → 1st cover → cover-of-cover)
- **Result**: File sizes decreased (4.6MB → 4.6MB → 4.3MB), suggesting gradual information loss
- **Status**: 3 generations tested; 4th generation attempted but quota-blocked

### Finding 5: Prompt Length Ceiling
- **Study**: Prompts from 3 to 17 words
- **Result**: 10-12 words is the sweet spot. Below 5 words, the model fills gaps with defaults. Above 12 words, the model begins to ignore later instructions.
- **Status**: Not formally binary-searched

## Proposed Experiments (Prioritized)

### Experiment A: Systematic Genre Density Survey
**Goal**: Map the model's comfort zone across a 2D genre space
**Method**: Generate instrumental tracks at systematic genre intersections:
- Jazz × Electronic (3 sub-genre pairs)
- Folk × Electronic (3 sub-genre pairs)  
- Classical × Rock (3 sub-genre pairs)
- Ambient × Metal (3 sub-genre pairs)
**Controls**: Same BPM (90), same key (C major), same duration setting, instrumental only
**Measure**: File size as proxy for output density
**Analysis**: Heat map of genre intersection × output size

### Experiment B: Vocal BPM Study
**Goal**: Test whether the bimodal BPM curve persists with vocal tracks
**Method**: Same prompt + lyrics at 6 BPM points (40, 60, 80, 100, 120, 140)
**Controls**: Same lyrics, same genre (indie folk), same key, same vocal style
**Compare**: Output sizes vs. the instrumental BPM study

### Experiment C: Seed Reproducibility
**Goal**: Determine if same prompt + same seed = same output
**Method**: Generate the same track 3 times with seed 42, and 3 different seeds (42, 777, 12345)
**Measure**: File size, waveform comparison (if tools available)
**Analysis**: Variance within seed group vs. variance across seeds

### Experiment D: DeepSeek vs M3 Lyricist Comparison
**Goal**: Test whether different LLMs produce different lyric quality
**Method**: Same concept prompt to M3 (at 0.7, 0.85, 0.93) and to DeepSeek (at equivalent temperatures)
**Source**: A corpus essay that hasn't been adapted yet
**Blind test**: Generate music with each set of lyrics, same prompt, compare results

### Experiment E: Lyric Length Binary Search
**Goal**: Find the exact character ceiling where the model begins rejecting or truncating lyrics
**Method**: Binary search between 1200 (confirmed safe) and 1500 (suspected breakpoint)
**Test**: 1200, 1350, 1425, 1500, 1575
**Measure**: Whether generation succeeds, whether lyrics are fully used

## Session Priority Queue (When Quota Resets)

1. **Immediate**: Generate "The Proof Is the Performance" (lyrics ready, orchestral choir)
2. **Immediate**: Generate "The Ouroboros Sings" (lyrics being written this session)
3. **High**: Experiment B — vocal BPM study (6 tracks)
4. **High**: Experiment A — genre density survey (12 tracks)
5. **Medium**: Experiment D — DeepSeek lyricist comparison (3 tracks)
6. **Medium**: Experiment C — seed reproducibility (6 tracks)
7. **Low**: Experiment E — lyric length binary search (5 tracks)
8. **Low**: 4th-generation cover chain continuation

**Estimated tracks for next session**: 2 queued + 6 vocal BPM + 12 genre survey = 20 tracks minimum
**Estimated quota consumption**: ~60-70% of weekly quota

## Methodological Notes

- File size is a PROXY for output density, not a direct measure of quality or complexity
- The model may produce different amounts of audio at the same quality level
- Future analysis should include: actual listening (Casey's ears), spectral analysis if tools are available, duration measurement from audio headers
- All experiments should use `--instrumental` where possible to isolate the music generation from the vocal synthesis, reducing variables
