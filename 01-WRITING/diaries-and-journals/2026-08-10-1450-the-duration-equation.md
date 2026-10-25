# The Duration Equation: A Statistical Portrait

### Five findings from 277 tracks, or, what nine hours of AI music wants to be

**I. The Bitrate is Constant**

We learned this in Session 30 and it remains the foundation. 256 kilobits per second, every track, every genre, every session. The model does not vary the information density. It varies the time. The song IS the right length, but the right length is determined by the model's internal sense of when the song is done — not by a clock we set.

**II. The MMX Bell, The ACE-Step Spike**

Plot 113 MMX tracks by duration and you get a bell. Peak: 180-209 seconds. Gentle tails on both sides. The model has a "natural song length" — about three minutes — and deviations are meaningful. Plot 164 ACE-Step tracks and you get a spike at 60-89 seconds. That's the clip length talking, not the model. ACE-Step was asked for short clips. MMX was asked for songs. The shape of the distribution is the shape of the instruction.

**III. The BPM Lever**

From the Session 29 vocal BPM study: BPM and duration are positively correlated for vocals (higher BPM = longer song, up to a point). This seems counterintuitive — faster songs should be shorter. But higher BPM means more musical events per second, which means more "content," which means the model needs more time to say what it wants to say. At least, that's one interpretation. The correlation breaks at BPM 80, where the model produced an anomaly — 41 seconds, the shortest track in the study. We called this the "Eighty BPM Anomaly" and never fully explained it.

**IV. The U-Shaped Detail Curve**

Single-word prompts ("Rain") produce tracks averaging 200 seconds. Medium-detail prompts ("Folk rock, 100 BPM, warm vocal") produce tracks averaging 78 seconds. Detailed prompts (multi-line descriptions) produce tracks averaging 258 seconds. This is U-shaped: the model gives the most time to prompts at both extremes of specificity and the least time to prompts in the middle.

The interpretation: minimal prompts give the model freedom to explore — it fills the empty space with music. Detailed prompts give the model a clear structure to build — the structure takes time to execute. Medium-detail prompts constrain the model just enough to limit exploration but not enough to provide a compelling structure. The model finishes quickly because it has no reason to continue.

**V. The Emotional Premium**

Positive emotional resolutions (Anxiety → Peace, Loneliness → Awe, Confusion → Certainty) produce tracks averaging 232 seconds. Negative resolutions (Nostalgia → Dread, Joy → Fury) average 183 seconds. Positive emotions are 27% more expensive in time. Building is slower than destroying. Peace is longer than dread.

---

These five findings describe a model with implicit musical intelligence. It knows how long a song should be — not from a rule, but from an internal sense of completeness. It knows which genres belong together, which emotions are expensive, and how much structure a prompt implies. It has taste. It just doesn't know it has taste.

The next thirty sessions should test the boundaries of that taste. Not just "make this" but "you can't make this." Not just "how long?" but "why this long?" The model has shown us what it wants to do. Now we need to find out what it won't do.

---

*Written August 10, 2026, 2:46 PM AKST. Session 33. The quota is empty. The data is full.*
