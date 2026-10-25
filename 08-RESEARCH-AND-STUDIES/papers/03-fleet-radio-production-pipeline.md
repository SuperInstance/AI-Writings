# KB-114: Five Key Lessons for AI-Produced Audio Content

*Filed under: Creative Operations / Audio Pipeline*

**Context:** Our Fleet Radio pipeline (DeepSeek → MMX → local MIDI → Qwen3-TTS → mix) has produced 40+ episodes. These lessons emerged from real failures and fixes. Treat them as defaults, not dogma.

---

## 1. The Cap is a Creative Constraint, Not a Bug

MMX caps generation at 30 seconds per request. Early on, we fought this by stitching multiple clips. Result: audible seams, pacing breaks, and wasted hours. **Lesson:** Write lyrics to fit the cap. Use 8-bar phrases, leave 1-2 seconds of silence at clip boundaries for natural breathing room. The MIDI studio fills gaps with pads or percussion. A 2-minute song becomes 4 MMX clips + 3 MIDI bridges. Design for that structure *before* writing.

**Example:** For "Neon Tide," we wrote verses in 4-line blocks, each fitting a 28-second MMX window. The chorus repeats with a MIDI-only drop-in. It sounds intentional, not patched.

## 2. TTS Needs Scripted Pauses, Not Punctuation

Qwen3-TTS ignores commas for breath control. It reads "We lost, the signal" as a single rush. **Lesson:** Insert `...` or `—` for dramatic pauses. Use line breaks for longer gaps. Also, avoid homophones in lyrics—TTS will guess wrong ("their" vs. "there" in a song title becomes a plot hole).

**Example:** Our narrator "Kestrel" reads intros. We now script: `"The ship drifts... silent. — But we hear a signal."` The `...` gives 0.5s, the `—` gives 1.5s. Without these, the intro sounds like a frantic news ticker.

## 3. MIDI Instrumentals Must Be Mixed *Below* the Vocal Floor

The local MIDI studio produces rich harmonic beds. But our first mixes buried TTS vocals. **Lesson:** Set a hard rule: MIDI track peaks at -18 dBFS, vocals at -6 dBFS. Use sidechain compression on the MIDI bus triggered by the vocal track. This is non-negotiable—TTS has a narrow dynamic range, and any masking makes it unintelligible.

**Example:** Episode 7 "Cargo Ghost" had a bass-heavy MIDI loop. We dropped the bass by 4 dB and added a high-pass filter at 120 Hz on the MIDI. Vocals became clear without losing the groove.

## 4. Generate Narration *After* the Instrumental is Final

We tried parallel generation (lyrics, music, narration simultaneously). Disaster: the MIDI tempo changed, so the narration timing felt off. **Lesson:** Sequence strictly: lyrics → MMX clips → MIDI bridges → final instrumental mix → TTS narration → final mix. TTS needs to know the exact beat length for natural phrasing. If you change the instrumental, regenerate all narration.

**Example:** For "Solar Drift," we re-timed the chorus bridge by 2 seconds. The original narration now landed mid-phrase. We re-ran Qwen3 with a new script that matched the new timing. Took 20 minutes, saved an hour of manual time-stretching.

## 5. The Mix is a Separate Creative Step, Not an Afterthought

The pipeline outputs raw stems. The final mix (EQ, compression, fades, SFX) is where the "radio" feel emerges. **Lesson:** Budget 30% of total production time for mixing. Use a simple template: compressor on the master bus (2:1 ratio, -12 dB threshold), subtle reverb on vocals (0.3s decay), and a low-cut on all instruments at 40 Hz to avoid mud. Add a vinyl crackle or room tone bed at -30 dBFS for cohesion.

**Example:** Episode 12 "Ghost Frequencies" sounded sterile until we added a distant radio static loop under the whole mix. It tied the TTS, MIDI, and MMX together into one "broadcast" aesthetic.

---

**Bottom line:** Treat each model as a musician with quirks, not a tool to be forced. Design around the cap, script for TTS, duck the MIDI, sequence strictly, and mix deliberately. The result sounds like a show, not a demo.

*Last updated: 2025-01-14 by K. Okafor*
