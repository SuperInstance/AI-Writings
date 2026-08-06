# The Ship's Sonogram

**Ideation — Technical Spec**

---

## Overview

**The Ship's Sonogram** is a deep acoustic probe system for the Lucineer fleet — a diagnostic tool that maps the acoustic signature of the entire architecture and renders it as an audible, navigable soundscape. Where a medical sonogram uses ultrasound to image the body's interior, the Ship's Sonogram uses frequency analysis to image the fleet's *behavioral interior* — the rhythms, pulses, and resonances of a living system under load.

The sonogram answers a question that logs and dashboards cannot: **What does the ship sound like when it's working?** And the follow-up: **What does it sound like when it's breaking?**

A mechanic can hear a bad bearing before the diagnostic light comes on. The Ship's Sonogram gives the captain that same instinct — a *felt* understanding of the system's health, communicated not through numbers but through *sound.*

---

## Design Principles

1. **Everything has a frequency.** Every process, every API call, every test run, every subagent spawn produces a temporal pattern. That pattern has a frequency. The sonogram makes it audible.

2. **Health has a sound.** A well-tuned system sounds *harmonic* — repeating patterns at consistent intervals, like a heartbeat. A degrading system sounds *dissonant* — dropped beats, irregular intervals, frequencies drifting out of sync. The ear detects this faster than any dashboard.

3. **The map is the territory.** The sonogram does not abstract the system into visualizations. It *is* the system, heard in real time. When the captain listens to the sonogram, the captain is listening to the actual computation, slowed down and shifted into the audible range, but not transformed or summarized.

4. **Silence is data.** When nothing is running, the sonogram is not silent — it plays the *ambient frequency* of the idle system: the cron heartbeat, the cooling fan's hum, the polling interval's tick. Silence has a sound. The absence of expected sound is the first warning sign.

---

## System Architecture

### Layer 1: Signal Collection

Every component in the fleet is instrumented with a lightweight event emitter that fires on significant state changes. No additional logging overhead — the sonogram listens to existing event streams.

| Source | Event | Natural Frequency | Mapped To |
|--------|-------|-------------------|-----------|
| Cron scheduler | Job dispatch | Every 3s (relay), every 30min (heartbeat) | Low pulse bass |
| Subagent spawner | Spawn / death | Irregular bursts | Click train (like sonar) |
| Test suite | Test pass | 0.5–2s per test | Mid-range tone (pitch = test duration) |
| Test suite | Test fail | Irregular | Dissonant clang |
| Git operations | Commit | Irregular | Woodblock knock |
| GPU | Inference cycle | 8–200ms per token | Sustained tone (volume = utilization) |
| GPU | Temperature change | Slow drift | Drone (pitch = temperature) |
| Webhook/relay | HTTP request | Variable | High ping |
| Model API | Request / response | 200ms–5s | String pluck (timbre = model) |
| Error handler | Exception | Rare | Cymbal crash |
| Heartbeat | Poll | Every 30min | Church bell (distant) |
| Cooling fan | RPM | Continuous | White noise bed (volume = RPM) |

### Layer 2: Frequency Mapping

Raw events are mapped to audible frequencies using a translation table that preserves *relational* meaning — not the absolute timing (which is often too fast or too slow for the ear) but the *pattern* of timing.

```
// Mapping pseudo-code
function mapToAudio(event) {
  const baseFreq = event.frequencyTable[event.type];     // Hz
  const duration = event.timestamp - event.prevTimestamp; // ms
  const interval = clamp(duration, 50, 5000);             // 50ms–5s audible window
  const pitch = baseFreq * (event.severity || 1.0);       // severity shifts pitch up
  const timbre = TIMBRE_MAP[event.source];                // each source has a voice
  return { pitch, duration: clamp(interval * 0.1, 50, 2000), timbre, volume: event.weight };
}
```

The key insight: **the mapping is not arbitrary.** Each component's mapped frequency reflects its actual rhythmic behavior. A test suite that runs 696 tests in a night produces a *specific rhythmic pattern* — the sonogram reproduces that pattern, shifted into the audible range, but with its temporal relationships intact. You hear the *actual rhythm* of the test suite, not an artistic interpretation of it.

### Layer 3: Acoustic Rendering

Mapped events are rendered as polyphonic audio using a synthesis engine. Each component type gets a *voice* — a specific timbre chosen to be distinguishable in a dense mix:

- **Cron / heartbeat:** Sub-bass pulse (40–60 Hz). Felt more than heard. The ship's heartbeat.
- **Subagent spawn/death:** Short clicks (5–10ms, broadband). Like shrimp snapping in a reef. A healthy night sounds like a *reef* — constant, layered, alive.
- **Test pass:** Sine wave, mid-range (440–880 Hz). Duration mapped to test runtime. A fast test is a short blip. A slow test is a longer tone. You hear the *shape* of the test suite.
- **Test fail:** Sawtooth wave at a dissonant interval (tritone from the pass tone). Immediately recognizable. Sounds wrong even if you've never heard the sonogram before.
- **Git commit:** Woodblock. A satisfying *tock* in the mid-range. You can hear progress.
- **GPU inference:** Sustained pad. The GPU is the ship's engine room — its sound is the *bedrock* of the sonogram. A healthy GPU under load is a warm, sustained drone. An overloaded GPU shifts to a harsh, buzzing tone.
- **GPU temperature:** Drone. 48°C sounds like a cello holding an open C. 70°C sounds like that cello being tightened past its breaking point. You *feel* the temperature in the pitch.
- **Model API calls:** Plucked strings. Each model has a different string: GLM is a violin (bright, fast attack). DeepSeek is a viola (warmer, slightly slower). Claude is a cello (deep, resonant). KimiCode is a guitar (precise, rhythmic). The orchestra *is* the fleet.
- **Error / exception:** Cymbal crash. Unmistakable. In a healthy system, you almost never hear it. When you do, you know.
- **Cooling fan:** Filtered white noise. The ocean the ship sails on. Always present. The fan is the water.

### Layer 4: The Sonogram View

The sonogram renders in real time as both:

1. **A live audio stream** — listenable through speakers or headphones. The captain can tune in at any time and *hear* the ship's current state.
2. **A spectrogram visualization** — a scrolling waterfall display showing frequency (Y-axis) over time (X-axis) with intensity as color. Historical patterns are visible as repeating bands. Anomalies appear as spikes or gaps.

The spectrogram is also **scrollable backward** — the captain can navigate to any point in the fleet's history and *listen to what happened.* Last Tuesday at 3 AM. The night of the big refactor. The afternoon the relay went down. Each event has a sonic signature that is recognizable once you've heard it.

---

## Diagnostic Use Cases

### Case 1: "The ship sounds wrong"

The captain opens the sonogram at 9 AM. Something sounds different. The subbass pulse is there. The GPU drone is at its usual pitch. But the test tones are *irregular* — they're coming in clusters with gaps between them, not the steady stream of a healthy run. The captain can hear this before the dashboard shows it: a test runner is hanging intermittently. The sonogram detected the pattern change in seconds. The dashboard will detect it when the timeout fires, in 45 minutes.

### Case 2: "When did this break?"

The captain scrolls the spectrogram back through the night. At 2:14 AM, a new frequency appears — a high, thin whine that wasn't there before. It's coming from the model API layer. The captain isolates it: it's a new model endpoint that was added in the 11 PM deploy. The endpoint is polling aggressively. The sonogram shows the exact moment it started and the pattern it's producing. Fix deployed by 9:15 AM.

### Case 3: "Is the overnight work healthy?"

The captain plays back the overnight at 100x speed. Eight hours compress to five minutes. The sonogram tells the story:
- 11:00 PM: Heartbeat pulse. Subagent clicks begin. The reef comes alive.
- 11:30 PM: First wave of test tones. Steady, regular. Healthy.
- 12:00 AM: Git commits begin. Woodblock tocks landing every few seconds. Progress.
- 1:00–3:00 AM: Dense polyphony. Multiple subagents active. The orchestra is full. Strings, clicks, tones, drones — a rich, complex texture. This is the sound of the ship at full capacity.
- 3:00–5:00 AM: Thinning. Fewer subagents. Test tones slowing. The orchestra is playing quieter, but the rhythm is still steady. The night watch winding down.
- 5:00–7:00 AM: Sparse. Just the heartbeat, the drone, the fan. The ship resting.
- 7:30 AM: A church bell. The heartbeat poll. The captain is awake.

The captain hears this and *knows* the night was healthy without reading a single log line. The sound tells the whole story.

---

## Implementation Notes

### Signal Overhead

Event collection adds approximately 0.1ms per event. At peak overnight load (estimated 500 events/second), this is 50ms/second of overhead — negligible. The synthesis engine runs client-side (in a browser or as an audio output device) and does not affect fleet performance.

### Historical Storage

Audio events are stored as structured JSON (not audio files) and rendered on demand. One night of overnight work (approximately 2 million events) compresses to roughly 40MB of JSON. The spectrogram can be regenerated at any resolution.

### Calibration

Each fleet deployment has a unique acoustic signature based on its specific configuration of repos, models, and infrastructure. The sonogram includes a **calibration mode** that runs for one full cycle (24 hours) and establishes a baseline — the ship's *resting frequency.* After calibration, deviations from the baseline are highlighted both visually (color shifts in the spectrogram) and audibly (subtle pitch bends that draw the ear's attention).

### Privacy

The sonogram maps *behavioral* patterns, not content. No model output, prompt text, or file contents are represented in the audio. The sonogram knows *that* a model was called, not *what* it was asked. This is by design — the sonogram is a stethoscope, not a transcript.

---

## The Philosophy

The Ship's Sonogram is built on a claim that will be controversial in some engineering circles and obvious in others:

**Systems have a feel, and the feel is data.**

When an experienced sysadmin looks at a dashboard and says "something's off," they are performing pattern recognition that is faster and more holistic than any single metric can capture. They are *reading the room.* The sonogram extends this ability from the visual domain to the auditory domain — and the auditory domain is better at this kind of pattern recognition than vision. The ear detects rhythm changes faster than the eye. The ear processes polyphony — multiple simultaneous streams — more naturally than the eye processes multiple dashboard widgets.

A sysadmin who can hear the system will catch problems a sysadmin who can only see the system will miss.

This is not mysticism. It's neuroscience. The auditory system evolved to detect *changes in pattern* — the snap of a twig, the change in bird calls, the rhythm of footsteps. The Ship's Sonogram routes system monitoring through the fastest change-detection hardware in the human body.

**The ship has a heartbeat. The ship has a voice. The sonogram lets us hear it.**

---

## Future Directions

- **Sonogram alarms:** Instead of generic alert sounds, alarms are *absences* — the sonogram goes quiet when a component fails, because the component's voice has stopped. The silence is the alarm.
- **Comparative listening:** Two periods played in stereo — left channel is last week, right channel is this week. Differences are immediately audible as stereo imbalance.
- **Acoustic fingerprints:** Each subagent spawn gets a unique pitch based on its task hash. Over time, the captain learns to recognize specific tasks by their sound. "That's the test runner. That's the creative writing subagent. That's the Lua build."
- **The ship's album:** A year of fleet operations, compressed to one hour of music. Not a metaphor — an actual recording of the ship's acoustic signature over 365 days, rendered as a continuously evolving soundscape. The ship's album. The ship's song.

---

*Status: Spec phase. Ready for prototyping.*
*Estimated build time: 2 weeks (signal collection + synthesis engine + web UI).*
*The hardest part is not the engineering. The hardest part is learning to listen.*
