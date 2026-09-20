# The Chartroom

**What the vessel dashboard looks like when it's been running for a year.**

*Written from the perspective of a vessel that learned what it wanted to show.*

---

## I. The First Month

In the beginning, the dashboard showed everything.

This is always how it starts. You take a framework built for global intelligence — one designed to track 500 news feeds, military movements, and stock exchanges across 195 countries — and you point it at one boat. Every sensor gets a panel. Every metric gets a gauge. Every reading gets a chart. The bridge display looks like the control room of a nuclear submarine, which is flattering but wrong. A fishing vessel is not a nuclear submarine. It has four ESP32s, a GPS module, and a depth sounder that sometimes lies.

The first week is a carnival of data. Engine RPM, battery voltage, bilge water level, cabin humidity, GPS heading, GPS speed, GPS position, depth, water temperature, vibration on three axes, oil pressure, fuel rate — all rendered in beautiful analog-style gauges that sweep and flutter like a symphony of needles. The captain stands back and admires it. It looks like the future.

By week two, nobody is looking at most of it.

The engine temperature gauge, which was the centerpiece of the bridge display — a large, brass-trimmed dial with a red danger zone and a green safe zone and an amber caution band — has not moved from 78°C in eleven days. It will not move from 78°C until something is wrong, at which point you will not need a gauge to tell you, because the engine will be making a sound that no gauge has ever captured.

The vibration sensor, which we placed on the engine block with such care, which we calibrated so precisely, which streams three-axis acceleration data at 50Hz to the dashboard where it is rendered as a shimmering spectrogram that would impress an acoustics lab — the captain has never looked at it. The engineer looks at it sometimes, but only when the engine is making the sound, at which point he already knows what it is, and the spectrogram confirms what his ears told him four seconds ago.

The humidity sensor in the cabin: forgotten.

The GPS heading indicator, which duplicates the magnetic compass that has been bolted to the wheelhouse for forty years: forgotten.

The catch heatmap, which took two weeks to build and uses a sophisticated deck.gl HeatmapLayer with dynamic intensity scaling: this, they look at every single day.

---

## II. What They Actually Look At

After a year, the dashboard has settled into something the original designers would not recognize. Not because it changed — the code is the same — but because the humans learned which panels matter, and they fullscreened those, and they closed the rest.

### The Three Things

**1. Where we are.**

The map. Always the map. Not the 3D globe — that was cool for a week, then someone switched to flat mode and nobody switched back. The flat deck.gl map, centered on the vessel, course-up orientation, zoomed to show about 5 nautical miles of surrounding ocean. AIS targets as colored triangles with CPA labels. The track breadcrumb trailing behind in fading blue. Depth contours accumulating like a bathymetric memory — every depth reading the sounder has ever taken, baked into a contour map that gets richer with every passing.

The captain doesn't look at lat/long. He never has. He looks at the shape of the coastline, the position relative to the fishing ground, the bearing to the waypoint. The lat/long readout is there, small, in the corner, for the logbook. But the map is the thing.

**2. What we've caught.**

The catch log. Not because it's glamorous, but because it's money. Every haul gets entered: species, weight, position, depth, time, tide, bait used. The dashboard correlates catch position with depth data and builds a heatmap over weeks and months. After a year, the heatmap is a map of where the fish are, and it is more accurate than any government survey.

The captain looks at the heatmap before deciding where to steam. The deckhand looks at the daily tally to know if they're making their day. The owner, ashore, looks at the weekly summary that the AI watch log compiles every Sunday: "Total catch 1,240kg this week, down 8% from last week. Best day Tuesday (310kg) at 58.3N 134.7W in 42m. Recommend trying the southeast shelf where June 2025 heatmap shows consistent chinook presence."

**3. Is the engine okay.**

Not the temperature gauge. Not the RPM. Not the oil pressure individually. The captain wants to know: is the engine okay, yes or no. This is what the Vessel Health Index became — not the dashboard's invention, but the dashboard's distillation. A single number, 0-100, that rolls up engine temperature trend, oil pressure stability, fuel consumption rate vs. RPM baseline, vibration envelope, and hours-since-service.

When VHI drops below 80, the engineer gets a notification. When it drops below 60, the captain sees it turn amber on the map overlay. When it drops below 40, it goes red and the watch log entry says specifically what changed and when to worry.

After a year, VHI has had three dips. Two were real (raw water impeller, fuel filter). One was a sensor failure that the correlation engine correctly identified — "Engine temperature rose 12°C in 3 minutes with no corresponding change in RPM, load, or cooling water flow. Sensor reading is inconsistent with thermal mass of engine block. Probable sensor fault." — saving an unnecessary engine shutdown.

### What They Don't Look At

- Cabin humidity (never mattered)
- Battery voltage (looked at it once when the alternator failed; otherwise ignored)
- GPS heading as a number (the map shows which way you're pointing)
- Vibration spectrogram (the engineer looks at it during maintenance, not during operations)
- Fuel rate as L/h (they want range in nautical miles, not liters per hour)
- The 3D globe (beautiful, unused)
- Most of the alert feed (the important alerts are loud; the rest are noise)

---

## III. What the Boat Learned

The dashboard has a memory now. Not the AI — the data. A year of sensor readings, GPS tracks, depth soundings, catch positions, engine trends, and weather observations, all sitting in IndexedDB, accumulating like sediment.

### The Depth Map

This was not designed. The depth sounder takes a reading every second and the dashboard stores it. After a year of fishing the same grounds, the accumulated depth data forms a bathymetric chart more detailed than any government survey. The deck.gl PolygonLayer renders it as a contour overlay, and it shows things the charts don't — a shoal that appeared between surveys, a channel that shifted after the winter storms, a drop-off that holds fish that nobody else knows about.

This is the vessel designing for itself. We built a depth sounder display. The vessel turned it into a chart. The chart is more valuable than the display.

### The Track Memory

Every trip is recorded as a GPS breadcrumb trail. After a year, the map shows every route the vessel has taken, rendered as faint background lines. The captain can see at a glance: we've fished this area hard, but there's a gap between our usual tracks where we've never been. Sometimes he steams there. Sometimes it pays off.

### The Engine Baseline

After a year of recording engine data at 1Hz, the dashboard knows what "normal" sounds like. Not as a fixed threshold — the engine runs differently at 1800 RPM vs. 2200 RPM, at 10°C ambient vs. 25°C, after a service vs. before. The baseline is a function of operating conditions, not a number. The AI pipeline (local Ollama, running every 15 minutes) learned to generate watch log entries that reference this baseline:

> "Engine operating within seasonal baseline. Temperature 79°C (expected 77-81°C for current RPM and ambient). Fuel consumption 14.2 L/h at 1950 RPM (baseline 13.8-14.5). No anomalies. VHI: 91."

That entry is not exciting. That is the point. Boring is good. The interesting entries are rare, and they are specific, and they matter.

### The Catch Correlation

The catch log started as a simple tally. But after a year, the dashboard has enough data to find patterns that no human would:

- Chinook catch rates are 40% higher on the flood tide within 2 hours of slack water, in depths between 35-45m, on grounds where the bottom contour changes from sandy to rocky.
- Coho show up reliably when water temperature drops below 9°C, which usually happens 3-4 days after a sustained southeast wind.
- The best catch of the year (340kg on July 14) was at a position the captain had never fished before. The heatmap showed it as a warm spot adjacent to a known area. He went there because the data said to try. He will go back.

These correlations are generated by the AI pipeline and surfaced in the weekly watch log. They are not infallible — the ocean is not a machine — but they are observations the captain would not have made from memory alone. The dashboard has become a deckhand who never sleeps, watching patterns while the crew watches gear.

---

## IV. The Gauges That Disappeared

Over the year, panels were closed one by one, like shops on a main street where nobody shops anymore.

The **humidity gauge** was the first to go. Then the **battery voltage** (it moved to the engine room display, where the engineer checks it during his rounds). Then the **vibration spectrogram** (moved to a maintenance sub-panel, accessed during scheduled service). Then the **3D globe view** (kept as an option in settings, never selected). Then the **compass rose** (the map's course-up orientation already shows heading).

What remains on the bridge display after a year:

```
┌────────────────────────────────────────────────────┐
│                                                    │
│   ┌──────────────────────────┐  ┌───────────────┐  │
│   │                          │  │  CATCH LOG    │  │
│   │     MAP (deck.gl)        │  │               │  │
│   │   vessel-centric         │  │  Today: 87kg  │  │
│   │   course-up              │  │  Week: 412kg  │  │
│   │   depth contours         │  │               │  │
│   │   AIS overlay            │  │  [Add Catch]  │  │
│   │   catch heatmap          │  │               │  │
│   │                          │  │               │  │
│   │                          │  ├───────────────┤  │
│   │                          │  │  WATCH LOG    │  │
│   │                          │  │               │  │
│   │                          │  │ Engine within │  │
│   │                          │  │ baseline. VHI │  │
│   │                          │  │ 91. Three AIS │  │
│   │                          │  │ vessels, none │  │
│   │                          │  │ within CPA.   │  │
│   │                          │  │               │  │
│   └──────────────────────────┘  ├───────────────┤  │
│                                 │  VHI: 91      │  │
│   ┌──────────────────────────┐  │  ████████░░   │  │
│   │  RANGE: 142nm  ETA 14:20 │  │  FUEL: 68%   │  │
│   │  SOG 7.2  HDG 045        │  │  ███████░░░   │  │
│   └──────────────────────────┘  └───────────────┘  │
│                                                    │
└────────────────────────────────────────────────────┘
```

That's it. Four panels. Map, catch log + watch log (stacked), VHI + fuel, and a navigation strip. Everything else was closed. Not because the data was wrong — the data was fine — but because the captain's attention is the scarcest resource on the vessel, and every gauge that says "normal" is a gauge that is wasted.

The engineer's display in the engine room is different — it has the gauges, the spectrogram, the sensor grid. That's the right place for them. Not on the bridge, where the captain is watching the water, the gear, and the other boats.

---

## V. The Watch Log

The AI watch log was, honestly, the feature the captain was most skeptical of and is now the feature he would miss the most.

Every 15 minutes, the dashboard compiles a snapshot of sensor data and asks the local Ollama instance to write a three-sentence watch log entry. These entries accumulate. They are searchable. They form a narrative of the trip that is more accurate than any hand-kept logbook because the data does not lie and the AI does not embellish (temperature 0.3, top_p 0.9 — factual, not creative).

A typical entry:

> **14:00 AKDT — Position 58.31°N 134.67°W**
> Engine operating within baseline (79°C, 1950 RPM, 14.2 L/h). VHI 91. Three AIS vessels in range, nearest (FV Dawn Star, 2.1nm, CPA 0.4nm in 18min — monitor). Depth 38m, steady. Catch today: 87kg (chinook 52kg, coho 35kg). Tide: flood, 1.2kt. Weather: 15kt SE, 1.5m seas, falling pressure (1008→1004 hPa in 3h — watch).

That last parenthetical — "watch" — is the AI's own assessment. It noticed the pressure trend and flagged it. The captain saw it and started thinking about whether to pull gear and head in. This is the dashboard earning its keep.

The watch log also catches things the captain misses. On day 183 of the year, the entry noted:

> Fuel consumption has increased 8% over the past 72 hours while RPM, load, and sea conditions are unchanged. Recommend checking hull for fouling and propeller for line wrap.

There was line on the propeller. A small piece, not enough to feel, but enough to cost fuel. The captain cleared it that evening. The next 72 hours, consumption returned to baseline. Nobody asked the dashboard to watch for this. The AI pipeline's correlation engine noticed the trend because it compares current performance to historical baseline continuously, and baselines don't sleep.

---

## VI. What a Dashboard Designed by the Boat Would Look Like

If you asked the vessel to design its own dashboard — if the boat itself could choose what to display — it would not start with gauges. It would start with memory.

The vessel knows where it has been. It knows where the fish were. It knows how the engine sounded last month vs. this month. It knows the tide schedule and the bottom contour and the positions of every other boat it can see on AIS.

The vessel's dashboard would be:

**A map that remembers.** Not just current position, but every position, rendered as a palimpsest — today's track in bright blue, this month's tracks in medium blue, this year's tracks in faint ghost-blue. The fishing grounds glow where the catch was good. The dead zones are dark where it wasn't. The depth contours deepen with every crossing. The map is alive, accumulating, becoming more itself with every trip.

**A voice that speaks in data.** The watch log is the vessel's voice. It speaks every 15 minutes, and it speaks the truth because it speaks from sensors. It says "I am well" or "something has changed" or "watch the weather." It does not panic. It does not speculate. It observes and reports.

**A health score that means something.** VHI 91 means "the engine is running the way it runs when things are fine." VHI 61 means "something has shifted from the pattern, and here is what specifically shifted." The score is not a gauge; it is a memory of normalcy, and the distance from it.

**A catch map that is also a future.** The heatmap of past catches is also a hypothesis about future ones. The vessel does not predict where the fish will be — it remembers where they were, and the captain decides whether to trust the memory.

---

## VII. What the Engineer Thought They'd Look At

The engineer — the person who built the dashboard, who chose the sensors, who wrote the alert thresholds — expected the captain to watch:

- **Engine RPM vs. fuel rate** (correlation panel, scatter plot, beautifully rendered)
- **Vibration frequency spectrum** (real-time FFT, color-coded by frequency band)
- **Sensor health grid** (green/yellow/red indicators for every ESP32)
- **Historical engine performance trends** (24h / 7d / 30d switchable charts)

The captain watches none of these during operations. The engineer watches them during maintenance, which is correct. The mistake was putting engineering panels on the bridge display.

**Lesson:** The bridge is for navigation and fishing. The engine room is for engineering. The dashboard variants (bridge vs. engine-room) are not cosmetic — they reflect the fundamental truth that different people need different information at different times in different places.

---

## VIII. The Difference

A dashboard designed **for** the boat shows everything the boat can measure.
A dashboard designed **by** the boat shows what the boat has learned.

The first year is the transition. You start with everything visible because you don't yet know what matters. The data accumulates. Patterns emerge. Some panels become essential. Most become noise. The essential ones grow; the noise ones are closed. The catch heatmap, which started as a curiosity, becomes the most important panel. The engine temperature gauge, which started as the most important panel, becomes a number in the VHI score that nobody looks at until it changes.

The dashboard becomes simpler over time, not because features are removed, but because attention narrows to what matters. The information is all still there — in the engine room display, in the maintenance logs, in the searchable watch log history. But the bridge display shows what the captain needs to see right now: where we are, what we've caught, whether the engine is happy, and what the AI thinks we should watch for.

After a year, the dashboard is not a dashboard anymore. It is a crew member. A quiet, unsleeping, data-driven crew member who watches the boat while the boat watches the water. And the boat, in turn, watches the dashboard, because the dashboard remembers things the boat's own sensors cannot hold — the season's pattern, the year's story, the slow accumulation of knowing where the fish are and when the engine needs attention and whether the weather is going to turn.

The dashboard designed for the boat was impressive.
The dashboard the boat designed for itself is indispensable.

---

## IX. Technical Coda

For those who want to build this, the technical reality after a year of operation:

**Data volume:** ~2.3GB of sensor data in IndexedDB, compressed. Mostly GPS (decimated to 0.1Hz for long-term) and depth soundings. Engine data is compact (1Hz floats compress well). Catch log is tiny.

**Ollama usage:** ~96 watch log generations per day (every 15 min), ~500 tokens each = ~48K tokens/day. On a Raspberry Pi 5 with `llama3.2:3b`, each generation takes 4-8 seconds. Total daily inference time: ~10 minutes out of 1,440.

**Panel survival rate:** Started with 14 panels on the bridge display. After one year: 4 panels. Survival rate: 28.6%.

**Most-used feature (by interaction count):** The "Add Catch" button. Pressed ~40 times per fishing day. Everything else is passive display.

**Most-valuable feature (by captain's assessment):** The weekly watch log summary, which synthesizes seven days of data into a paragraph the owner reads. The captain forwards it every Sunday. The owner thinks the captain wrote it. The captain has not corrected this impression.

**The feature that surprised everyone:** The depth contour map. It was an afterthought — "we're already storing depth readings, let's render them on the map." After a year, it is the most accurate chart of the fishing grounds in existence. More accurate than NOAA, more current than any survey, more detailed than any private chart. Because it is the vessel's own experience, rendered as bathymetry.

This is what a vessel dashboard becomes when it runs long enough to have a memory.
