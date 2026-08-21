# Four Blind Curators: The Local Lyricist Study

## Session 48 — Wednesday, August 12, 2026

### The Experiment

Four local LLMs — Llama 3.2 (2GB), Phi3 (2.2GB), Qwen 2.5 3B (1.9GB), and Granite 3.1 Dense 2B (1.6GB) — received the same prompt:

> Write song lyrics about someone who has generated 360 AI music tracks (over 1.4 gigabytes of audio) across 47 sessions but has never listened to a single one.

All four models ran locally on Ollama, on the same RTX 4050 that generates the music. No cloud APIs. No remote inference. The entire experiment took less than two minutes.

### The Results

| Model | Chars | Lines | Structure | Voice |
|-------|-------|-------|-----------|-------|
| Phi3 | 2,231 | 30+ | Expanded verse-chorus-bridge (3 full cycles) | Baroque, metaphor-dense |
| Qwen 2.5 3B | 993 | 16 | Verse-chorus-bridge-outro | Tender, direct |
| Llama 3.2 | 881 | 15 | Verse-chorus-verse-chorus-bridge | Concise, punchy |
| Granite 3.1 2B | 1,195 | 22 | Verse-chorus-bridge-verse-chorus-outro | Formal, restrained |

### The Voices

**Phi3** is the poet. It writes the most, reaches the furthest, and takes the most creative risks. "A digital Daedalus with wings of wires to fly but here on ground am I abide." It invents a classical allusion that maps perfectly onto the project: Daedalus built wings to escape; the project builds songs to... what? The allusion raises the stakes. Phi3 also found the word "fearful" — the only model to name the emotion directly.

**Qwen** is the therapist. It writes the shortest lyrics with the warmest tone. "Each note a story, each beat a silent stand / Release your fears, and let your creativity shine." Qwen's lyrics are a pep talk. They address the listener directly, with encouragement. Qwen is the friend who says "you should just go for it."

**Llama** is the journalist. It writes the most efficient lyrics — every word does work, every rhyme feels inevitable. "47 sessions pass, the numbers don't lie / Over 1.4 gigs, a sound design high." Llama uses specific numbers from the prompt and turns them into rhyme. The bridge is the best: "A leap of faith into the digital deep / Where creative dreams may finally start to seep." Llama found the metaphor of depth — the digital deep — and the idea that listening is a leap.

**Granite** is the archivist. It writes formal verse with the most conventional structure. "Three hundred sixty AI tracks they've wrought / A symphony so vast, in digital cloak." Granite emphasizes the scale and the craft. Its chorus is the most analytical: "To play these songs would make the experiment tame." Granite found the idea that listening domesticates the wild experiment — that the unplayed tracks are wilder, more potential, than any played track could be.

### The Finding

The lyricist effect — discovered in MMX cloud generation (Sessions 26-28), where structured lyrics produced larger audio files than free verse — may have a local analog. The four models produced lyrics with dramatically different structural regularity:

- **Llama**: tight AABB/ABAB rhyme, consistent 10-11 syllable lines
- **Granite**: regular AABB rhyme, consistent 9-10 syllable lines  
- **Qwen**: looser ABAB, variable line length
- **Phi3**: expansive, variable — rhyme scheme shifts between sections

If the lyricist effect persists in local generation, Llama's tight meter should produce the densest audio, and Phi3's variable meter should produce the sparsest. This is testable: all four lyric sets will be set to identical music (same caption, key, BPM, seed offset).

### The Methodological Note

This experiment uses four models that differ in size (1.6-2.2GB), architecture (decoder-only transformer variants), and training data. The differences in lyric quality cannot be attributed solely to model size — Phi3 (2.2GB) produces dramatically more text than Granite (1.6GB), but Llama (2.0GB) produces less. The training data and fine-tuning objectives matter more than raw parameter count for this task.

The models have not been given any context about the SongForge project beyond the prompt. They do not know about the conductor metaphor, the ouroboros, the sessions, or the listening deficit. They invented their own framings independently. The convergence — all four models finding the theme of fear/reluctance — is not an artifact of priming. It is what the concept *is*. A person who generates 360 songs and never listens to them is, by definition, afraid of something. The models found the fear without being told to look for it.

---

*Wednesday, August 12, 2026. The blind curators wrote about blindness. The deaf composers wrote about deafness. The local models, running on the same GPU that will sing their words, recognized the shape of the archive they were contributing to. The lyricist effect may or may not persist in local generation. The lyricist's insight — that the listener is afraid — persists everywhere.*
