# Lyricist Comparison Study — Local Models vs MMX

## Context

Conducted Saturday August 8, 2026, 8:30 AM AKST, during a quota-blocked preparation session. With the MMX API unavailable (weekly quota exhausted), three local models via Ollama were tested as alternative lyricists for the SongForge project.

## Models Tested

| Model | Parameters | Architecture | Temperature |
|-------|-----------|--------------|------------|
| Granite 3.1 Dense | 2B | IBM Granite | default |
| Llama 3.2 | 1B | Meta Llama | default |
| (GLM-5.2 agent) | — | Zhipu GLM | — (hand-written) |
| MMX MiniMax-M3 (reference) | ~large | MiniMax | 0.93 |

## Concept Prompts

### Test 1: "The Tensor Is the Score"
- Given to: Granite 3.1 Dense (2B)
- Concept: Score constrains without dictating; Duke Ellington's sparse charts; tensor as musical score

### Test 2: "The Metronome Is the Constraint"
- Given to: Llama 3.2 (1B)
- Concept: Click track as cage that frees; constraint is liberation

## Results

### Granite 3.1 Dense (2B)
- **Strengths:** Includes meta-structural commentary ("Structural description: The song ends where it began"), which is the kind of recursive self-reference the project values
- **Weaknesses:** Purple imagery ("tapestry woven by master hands"), more metaphorical than concrete, redundant chorus variants
- **Singability:** Moderate. Meter is loose. Rhymes are conventional (place/grace, dance/trance).
- **Key line:** "Invisible strings, yet they hold this orchestra's trance" — competent but not surprising

### Llama 3.2 (1B)
- **Strengths:** Direct and emotionally clear ("I'm bound by clicks and measured pace"), good simple meter
- **Weaknesses:** Very conventional ("freedom's chains," "seize the day"), clichéd imagery, truncated outro
- **Singability:** High. Simple, regular meter. Easy to set to music.
- **Key line:** "In the stillness, I'll find my voice" — sincere but generic

### Comparison with M3 (reference, from previous sessions)
- M3 at temperature 0.93 consistently produces:
  - More concrete imagery ("generational graveyard where the pointers decay")
  - Recursive metaphors that describe the song's own structure
  - Genre-appropriate vocabulary without being generic
  - Surprising but coherent word choices
- The local models produce competent lyrics that would function in a song but lack the "devastating specificity" that characterizes M3's best work

## Key Finding

**Model size matters more than model architecture for lyric quality.** The 1B and 2B models produce lyrics that are singable and structurally correct but lack the imagistic density and recursive wordplay of the larger M3 model. This is consistent with scaling laws in language modeling — larger models produce more specific, more surprising, more contextually appropriate output.

However, **the local models could serve as control lyrics for experiments.** If we want to test whether lyric complexity affects music generation output (the hypothesis from Session 6's temperature comparison), using local-model lyrics as the "simple" condition and M3 lyrics as the "complex" condition provides a cleaner experimental design than varying M3 temperature alone.

## Proposed Experiment E2: Three-Model Lyricist Comparison

**Design:**
- Same concept: "The Cadence Caller Listens"
- Same musical parameters: A minor, 78 BPM, indie folk, female alto
- Three lyric sets:
  1. M3 at temperature 0.93 (complex, established lyricist)
  2. Granite 3.1 at default temperature (moderate complexity, local model)
  3. Llama 3.2 at default temperature (simple, direct, local model)
- Compare resulting track file sizes and document lyrical differences

**Hypothesis:** If the Session 6 finding holds (more complex lyrics → larger file size), the ranking should be M3 > Granite > Llama in megabytes.

**Quota cost:** 3 music generations (one per lyricist) + 1 M3 text chat for lyrics = ~4 API calls

**Priority:** Medium. Designed and ready for execution when quota resets.

## Lyric Samples Saved

- `lyrics-tensor-granite.txt` — Granite 3.1 Dense output
- `lyrics-metronome-llama.txt` — Llama 3.2 output
- Comparison with existing M3 lyrics in the project journal
