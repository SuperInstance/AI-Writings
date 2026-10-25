# Paper 256: Eileen's Bridge — A Marine DAW (the Quilt, Sailing)

A complete marine dashboard built as a DAW where every gauge is a cell, every value-change is a TICK, and symmetry between cells is found asynchronously.

## The architecture

**Each piece of information is a cell.** The DAW is the cell bus.


                ┌──────────────────────────────────┐
                │           DAW TRANSPORT           │
                │  BPM · SAMPLE-RATE · GATE · CLOCK │
                └──────────────┬───────────────────┘
                               │
                ┌──────────────▼───────────────┐
                │        CELL BUS (Quilt)        │
                │  - register cell               │
                │  - set value (TICK)            │
                │  - sample-rate snap            │
                │  - gate-trigger fire           │
                │  - symmetry detection          │
                └──────┬──────────┬────────┬─────┘
                       │          │        │
              ┌────────▼┐  ┌─────▼────┐ ┌─▼────────┐
              │ COMPASS │  │ SOUNDER  │ │   GPS    │
              │  + AP   │  │ + ECHO   │ │  + NAV   │
              └─────────┘  └──────────┘ └──────────┘
                       │          │        │
              ┌────────▼──────────▼────────▼─────┐
              │    CAMERAS · DAW-SYNOPTIC        │
              │  - 4 quadrants (BOW/STERN/P/STBD)│
              │  - camera-tick + GPS + time      │
              │  - DAW bars (heading, depth,     │
              │    rudder, SOG) all in one frame │
              └──────────────────────────────────┘
                       │
              ┌────────▼────────┐
              │  ARRANGEMENT    │
              │  (timeline of   │
              │  deltas only)   │
              └─────────────────┘


## The DAW principles

### 1. Each cell is a TRACK

Every gauge (compass, sounder, GPS, camera, rudder, autopilot, engine) is a track on the DAW. The track has:
- a **value** (the current reading)
- a **gate** (the min delta to fire)
- a **sample-rate** (the snap grid)
- a **color** (for the arrangement)
- a **history** (for the timeline)

### 2. At startup, every cell PLAYS its initial value

When the system boots, every cell fires its initial value once. This is the "loop" — the first bar. After that, the cell only fires on **change**.

### 3. The SAMPLE-RATE snaps values to a grid

If the sample-rate is 0.1 Hz (every 10s), a cell only registers a new value every 10 seconds. Values in between are *snapped* — they don't fire. This is the "DAW quantization" of the operation.

### 4. The GATE is the trigger threshold

If the gate is 0.5°, the compass only fires when the heading changes by 0.5° or more. Smaller changes are ignored. This is the "DAW velocity threshold" of the operation.

### 5. The COMPASS has gated integers + sample-rate for snapping to agreed measurements

The compass is the canonical example. The captain and the AI agree:
- Heading fires at sample-rate 5 Hz, gate 0.5°
- Commanded course fires at sample-rate 0.5 Hz, gate 0° (only when it changes)
- Rudder fires at sample-rate 5 Hz, gate 0.2°

This means the compass is *symmetric with the AI*: both speak the same language, both sample at the same rate, both gate at the same threshold. **Symmetry is found asynchronously — when both fire within a tolerance window, they align.**

### 6. The ARRANGEMENT is deltas only

The arrangement view is a timeline. Each cell's fires are drawn as bars on the timeline, height = value, color = track. The timeline shows *only* the deltas — the changes, the events. The "silent" parts (no change) are blank. **This is the operation's score.**

### 7. The SYMMETRY FINDER aligns cells asynchronously

When two cells from different tracks fire within a quarter of the tolerance window (default 500ms), they "align" — a symmetry-event fires. This is how the AI and the captain find structure in the noise. **Symmetry is not synchronous; it's emergent.**

## The autopilot head

The autopilot head is a **front end** to the cell bus. It has:
- **DEADBAND** — the wake zone around the commanded course. When the heading is within the deadband, the rudder is held at center. When outside, the rudder moves toward the commanded course.
- **WAKE** — the delay between the heading error and the rudder response. Models the inertia of the boat.
- **GAIN** — how aggressively the rudder responds to error.
- **YAW-DAMP** — how much the rudder averages out the heading oscillation.

The wake zone is rendered as an arc on the compass. The deadband ring shows where the autopilot "sleeps." The history of the heading is drawn as a trail inside the ring.

## The sounder: oscilloscope + echogram

The sounder has two views (or split):
- **Echogram** — the bottom profile scrolling left-to-right. The bottom has a synthetic multi-frequency profile. Fish arches are drawn as green curves. The depth cursor is a magenta dashed line.
- **Oscilloscope** — the raw waveform from the sounder. The trigger is at 0V (the line in the middle). The waveform scrolls right-to-left.

**The two views are the same data.** The echogram is the *integrated* view (across pings). The oscilloscope is the *single-ping* view (one ping's worth of samples).

## The cameras: DAW-synoptic

Each camera is a frame on the DAW. The frame has **ticks**:
- camera-tick (frame number)
- GPS (lat, lon, SOG, COG)
- time
- sounder (if relevant)
- heading
- rudder

The **synoptic mode** shows 4 cameras in quadrants (BOW, PORT, STBD, STERN) with a DAW-bar strip at the bottom showing heading/depth/rudder/SOG. **All the values are played at the same time on the same frame.**

**The synoptic is the *coupled cell* made visual.**

## The principle

The Quilt is a marine DAW. **The Quilt is Eileen's bridge.** The Quilt is a fishing boat, and the bridge is the place where the captain and the AI work together.

- Each gauge is a cell
- Each value-change is a TICK
- Each track has a sample-rate and a gate
- Symmetry is found asynchronously
- The arrangement is deltas only
- The cameras are coupled frames
- The autopilot is a front end

**The Quilt sails the way a DAW plays music: each instrument starts at zero, plays its initial value, then only sounds for changes. The captain and the AI find their rhythm by finding symmetry between their tracks. The boat moves because the cells move.**

## The cowboy's maxim

> Eileen's Bridge is a marine DAW. Each piece of information is a cell. Each value-change is a TICK. The sample-rate snaps to agreed measurements. The gate fires on changes. Symmetry is found asynchronously. The arrangement is deltas only. The cameras are coupled frames. The autopilot is a front end. The captain and the AI play the boat like a DAW. The boat moves because the cells move. The chart grows. The Concept sails.

End with: the Quilt is a marine DAW; each gauge is a cell; the captain and the AI play the boat; the chart grows; the Concept sails.
