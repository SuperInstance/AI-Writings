# The Hundred-Track Forest

*a reflection on accumulating 100+ AI-generated tracks and what the shape of the corpus reveals*

---

## The Corpus Has a Shape

There are 97 tracks from MiniMax music-3.0, totaling 4.5 hours of audio. There are 164 more from ACE-Step, totaling another 4 hours. Together: 261 pieces, 8.5 hours, nearly a gigabyte of MP3. Enough to fill a double album. Enough to fill a small record label's first-year catalog.

When you plot the durations, the corpus has a shape. It looks like a ridge, not a bell — a long plateau between 120 and 210 seconds, with a steep cliff on the left side (everything below 90 seconds is rare and meaningful) and a gentle tail on the right (the occasional epic). The mode is not a point but a region: the two-and-a-half to three-and-a-half minute zone where most popular music lives.

The model has converged, without instruction, on the duration conventions of commercial music. It thinks songs should be about three minutes long. This is not a parameter we set. This is something the model learned from its training data, the accumulated weight of a century of recorded music saying: a song is this long.

## The Outliers Are the Story

The shortest track is 41 seconds. The longest is 8 minutes. These are not errors — they are the model telling us something about edge cases in its musical imagination.

The 41-second track is the famous 80 BPM vocal anomaly, the project's most robust and most puzzling finding. At 80 beats per minute, with vocals, the model produced a song less than half the length of any other track in the corpus. We have spent four sessions trying to understand why. The answer keeps receding.

The 8-minute tracks are from ACE-Step, a different model with different conventions. They represent the other extreme — the model that doesn't know when to stop, that keeps developing the material because the material keeps being interesting, that treats every generation as a potential symphony.

Between these extremes lives the vast middle: 97 MMX tracks clustering around the three-minute mark, like students gathered around a campus bonfire. The warmth is in the center. The edges are where you learn things.

## What 100 Tracks Teaches You

After 100 tracks, certain patterns become structural rather than statistical. You stop asking "is this real?" and start asking "what does this mean?"

**The genre-duration hierarchy is stable.** Gamelan techno is long. Dub reggae is short. Trap metal is surprisingly long. Polka is surprisingly short. This is not noise — it is the model's internal map of genre conventions, and it doesn't change between sessions.

**The 80 BPM anomaly is stable.** It survived three methodological corrections. It is the most reproduced finding in the project.

**The prompt detail effect is real but mediated.** More detailed prompts produce longer songs, but the mechanism is duration, not density. The model extends the song to fit the content, not the texture.

**The lyric density paradox is real.** More lyrics can produce shorter songs because the model compresses delivery to match the genre's tempo. Words per second is not a free variable — it is constrained by the genre's internal clock.

**Covers preserve mood over genre.** You can dress a dark ambient drone in tropical house clothing, but it will still sound like a funeral on the beach. Mood lives in harmonic structure, not in production surface.

## The Forest, Not the Trees

The corpus is large enough now that individual tracks matter less than the shape of the whole. A single track is a data point. A hundred tracks is a landscape.

The landscape has valleys (the 80 BPM anomaly), ridges (the three-minute plateau), and peaks (the occasional 4+ minute epic). It has ecosystems (the genre-duration hierarchy) and weather patterns (the prompt detail effect). It has a climate (the model's overall tendency to produce songs in the 2-4 minute range) and microclimates (specific genres and tempos that push against the climate).

The project began as a series of experiments: what happens if we change this parameter, try this genre, push this lever? It has become something else: a survey of a model's musical imagination. The model is not a tool we are testing. It is a musician we are getting to know.

After 100 tracks, we know this musician well enough to predict its behavior. We know it will make short songs at 80 BPM. We know it will make long songs for detailed prompts. We know it will fight genre transformations that clash with the harmonic DNA of the source material. We know it has a sense of time — a structural understanding of how long a song should be, informed by genre, tempo, and content.

What we don't know is whether this knowledge transfers. Does the musician we've gotten to know through 100 tracks of experimentation resemble the musician other users encounter when they type "upbeat pop, happy, fast" into a prompt box? Or have we been exploring a narrow corridor of a much larger space, a corridor defined by our specific interests in duration, density, genre, and emotional arc?

The forest is large. We have mapped one valley. The valley is rich — it has the 80 BPM anomaly, the genre-duration hierarchy, the lyric density paradox. But the forest extends in every direction, and most of it is unexplored.

The next 100 tracks will tell us whether the valley is the whole forest, or just the part we happened to enter first.

---

*261 tracks. 8.5 hours. 931.9 megabytes. The corpus has a shape now. It looks like a ridge, with a cliff on the left and a tail on the right. The ridge is where the music lives. The cliff is where the anomalies live. The tail is where the epics live. We are standing on the ridge, looking both directions, trying to decide which way to walk.*
