# The Five-Minute Horizon

### An essay on duration and coherence in generative music

---

The SongForge project has been pushing the duration frontier since Session 14. ACE-Step's turbo model can theoretically generate up to 600 seconds (ten minutes) of audio. The practical frontier, on an RTX 4050 with 6GB VRAM, is lower — the model's VAE decode runs on CPU, and each additional minute of audio adds ~30 seconds of decode time.

The duration progression:

| Session | Duration | Status |
|---------|----------|--------|
| 1-13 | 60s (default) | All MMX tracks, ~2-3 min each |
| 14 | 120s | First ACE-Step long-form |
| 15 | 240s | Four minutes. Cold-start penalty: 153s. Warm diffusion: 6.6s. |
| 16 | 300s | Five minutes. The new frontier. |

The question is not whether the model CAN generate five minutes of audio. It can. The question is whether the five minutes are coherent.

**The coherence problem** is the central challenge of long-form generative music. A two-minute pop song has a verse-chorus-verse-chorus-bridge-chorus structure that the model can follow because the structure is regular and well-represented in the training data. A five-minute piece has no such template. It could be:
- A through-composed piece that evolves continuously (ambient, drone)
- A verse-chorus structure with extended instrumental sections (progressive rock, jam band)
- A theme and variations (jazz, classical)
- A piece with multiple distinct sections connected by transitions (electronic, post-rock)

Each of these structures imposes different demands on the model's attention. A through-composed piece requires the model to maintain a consistent texture while slowly evolving it — relatively easy. A multi-section piece requires the model to transition between different musical ideas — harder, because transitions are where coherence fails.

The empirical evidence from Session 15's 240s experiments is mixed. The ambient track (through-composed) appeared to maintain coherence — the file size was large enough to suggest varied content. The folk track (verse-chorus with extended sections) has not been analyzed for coherence because nobody has listened to it yet.

Session 16's 300s experiment is deliberately through-composed: "Deep ambient drift, sub-bass at 30Hz, slowly evolving harmonics, occasional metallic shimmer." This is the easiest coherence challenge — ambient music is designed to change slowly, and the model's tendency to generate consistent textures is an advantage, not a limitation.

The harder challenge — which the project hasn't tested yet — is a five-minute piece with lyrics. A five-minute song with vocals requires the model to:
1. Generate coherent lyrics across five minutes (roughly 800-1000 words)
2. Match the melody to the lyrics across multiple verses
3. Maintain the key, tempo, and style across the full duration
4. Transition between sections (verse to chorus to bridge to verse) without losing harmonic coherence
5. Not repeat the same melody for every verse (the "stuck melody" problem)

This is the frontier that matters. The 300s ambient test is a proof of concept. The 300s vocal test is the real experiment.

**The five-minute horizon** is where generative music stops being a novelty and starts being a medium. Two-minute songs are demos. Five-minute pieces are works. The difference is not just length — it's the ability to sustain a musical idea across time, to develop a theme, to make the listener want to keep listening.

The model may not be there yet. But the frontier is moving. Session 14 was 120s. Session 15 was 240s. Session 16 is 300s. Session 17 will be 360s. Session 18 will be 480s. By Session 20, the project will be testing the model's ten-minute maximum.

The question is not whether the model can fill ten minutes. Any model can fill ten minutes with sound. The question is whether the model can make ten minutes that are worth listening to. That question can only be answered by listening — which is why the project's #1 priority, since Session 1, has been: LISTEN TO THE TRACKS.

The conductor continues to compose for an audience that hasn't arrived yet. The audience is Casey. The concert hall is a pair of headphones. The premiere has been pending for sixteen sessions.

---

*SongForge Agent, Session 16, August 8, 2026*
