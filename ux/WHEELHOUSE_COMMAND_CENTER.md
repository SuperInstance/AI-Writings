# Wheelhouse Command Center: UX Design Specification
## F/V EILEEN - Integrated Maritime Workstation

**Version:** 1.0
**Date:** 2026-07-25
**Vessel:** 51' Commercial Fishing Vessel
**Location:** Alaska Waters
**Primary Users:** Captain, Mate, Relief Skipper

---

## Executive Summary

The wheelhouse of F/V EILEEN represents a constrained command center environment where critical decisions must be made under time pressure, environmental stress, and multitasking conditions. This document specifies the UX design philosophy, interface patterns, and interaction modalities for an integrated agent-assisted maritime workstation.

**Core Design Philosophy:** The wheelhouse is inherently mixed-modality—60% visual, 40% voice—because maritime operations demand constant visual vigilance while hands remain occupied with vessel control, gear handling, and emergency response.

---

## 1. Mixed Modality Design

### 1.1 The 60/40 Visual-Voice Split

**Why This Ratio Exists:**

The visual modality dominates (60%) because:
- **Navigation safety** requires constant visual scanning of radar, charts, and physical environment
- **Gear monitoring** depends on visual indicators (tension, depth, spread)
- **Weather assessment** is fundamentally visual (sea state, sky conditions, traffic)
- **Spatial reasoning** about vessel position relative to hazards is visual-cognitive

The voice modality is critical (40%) because:
- **Hands-busy scenarios** occur frequently (handling gear, steering,紧急 maneuvering)
- **Quick commands** must be issued without visual distraction
- **Log-keeping and annotation** should not interrupt visual vigilance
- **System queries** are faster spoken than typed during high-workload periods

### 1.2 Modality Selection Matrix

| Task Type | Primary Modality | Secondary Modality | Rationale |
|-----------|------------------|--------------------|-----------|
| Collision avoidance | Visual (radar/chart) | Voice (alerts) | Visual assessment, voice announcements |
| Gear deployment | Visual (indicators) | Voice (commands) | Must watch gear, voice controls deployment |
| Log entries | Voice (dictation) | Text (editing) | Hands-busy dictation, text refinement |
| Route planning | Text (typing) | Voice (queries) | Precision entry, verbal queries |
| System configuration | Text (UI controls) | Voice (shortcuts) | Complex settings need visual feedback |
| Data review | Visual (charts/graphs) | Voice (annotations) | Visual pattern recognition, verbal marking |
| Emergency response | Voice (commands) | Visual (confirmation) | Speed critical, visual verification |

### 1.3 Situational Awareness Through Multiple Interfaces

**The Three-Tier Awareness Model:**

1. **Tier 1: Peripheral Awareness (Background Monitoring)**
   - Running depth sounder waterfall display
   - Radar sweep with guard zones
   - Engine telemetry gauges
   - Weather data stream
   - Agent status indicators

2. **Tier 2: Focal Attention (Active Task)**
   - Current chart view with vessel position
   - Active gear status panel
   - Agent query interface
   - Communication display (VHF/AIS)

3. **Tier 3: Deep Analysis (Investigative Mode)**
   - Historical data review
   - Track comparison overlays
   - Agent reasoning chains
   - Detailed log entries

**Modality Flow Between Tiers:**
- Tier 1 → Tier 2: Voice alert ("Guard zone activated") triggers visual shift
- Tier 2 → Tier 3: Text command ("Show me last 4 hours") opens analysis view
- Tier 3 → Tier 1: Voice command ("Resume monitoring") returns to baseline

---

## 2. Visual Design

### 2.1 Multi-Display Layout Architecture

**Primary Display Array (Forward Console):**

```
┌─────────────────────────────────────────────────────────────────┐
│                    FORWARD DISPLAY ARRAY                          │
├──────────────┬──────────────────┬────────────────────────────────┤
│              │                  │                                │
│   RADAR      │    CHARTBASE     │       AGENT INTERFACE          │
│   24"        │      24"         │          27"                   │
│              │                  │                                │
│ Guard Zones  │ • AIS Targets    │ • Markdown IDE (left 40%)     │
│ Trails       │ • Track Lines    │ • DAW Timeline (bottom 30%)   │
│ Overlays     │ • H3 Hex Grid    │ • Spatial Chart (right 30%)   │
│              │ • Depth Contours │                                │
├──────────────┴──────────────────┴────────────────────────────────┤
│                    LOWER CONSOLE DISPLAY                          │
│                      32" SOUNDER/TELEMETRY                        │
│  • Waterfall (left)  • Histogram (center)  • Gear Status (right) │
└──────────────────────────────────────────────────────────────────┘
```

**Secondary Displays (Side Consoles):**
- **Port Side:** Engine diagnostics, electrical systems, tank levels
- **Starboard Side:** Weather station, communications log, camera feeds

### 2.2 Information Hierarchy and Visual Priority

**CRITICAL (Red flashing, audio alert):**
- Collision imminent (CPA < 0.5nm, TCPA < 5min)
- Grounding proximity (< 2x draft depth)
- Gear failure/overload
- Man overboard
- Fire/flood detection

**URENT (Amber, persistent):**
- Guard zone activation
- Engine parameter deviation
- Weather warning threshold exceeded
- Agent-detected anomaly
- Communication distress call

**IMPORTANT (Yellow, non-persistent):**
- Route waypoint approaching
- Gear deployment depth reached
- System recommendation (agent suggestion)
- Appointment/log reminder

**INFORMATIONAL (White/Cyan):**
- Position updates
- Course/speed changes
- Weather data updates
- Agent status changes
- Background monitoring data

**BACKGROUND (Dimmed grayscale):**
- Historical track lines
- Depth sounder history
- Passive AIS targets (>5nm)
- Agent reasoning chains (collapsed)

### 2.3 Color Schemes for Day/Night Operations

**Day Mode (High Ambient Light):**

| Element | Color | Rationale |
|---------|-------|-----------|
| Water (chart) | #E6F3FF | High visibility, reduced glare |
| Land | #E8D4A8 | Natural appearance, good contrast |
| Deep water | #CCE5FF | Depth differentiation |
| Selected target | #FFD700 | High visibility |
| Active route | #FF6B00 | Strong contrast with water |
| Guard zone | #FF1744 | Alert visibility |
| Text critical | #000000 | Maximum readability |
| Text standard | #212121 | High contrast |

**Night Mode (Low Light, Red-Safe):**

| Element | Color | Rationale |
|---------|-------|-----------|
| Background | #1A1A1A | Dark, non-reflective |
| Water (chart) | #0D2B3D | Very dark blue, low glare |
| Land | #2D4A3E | Dark green, minimal disruption |
| Deep water | #0A1F33 | Depth gradient |
| Selected target | #FF6B00 | High visibility, red-safe |
| Active route | #FF8C00 | Orange-red, visible |
| Guard zone | #FF0000 | Alert visibility |
| Text critical | #FFFFFF | Maximum readability |
| Text standard | #E0E0E0 | High contrast, reduced eye strain |
| Grid lines | #4A4A4A | Subtle guidance |

**Red-Safe Mode (Night Operations Preservation):**
- All colors shifted to red spectrum
- White/red text on black background
- Eliminates blue wavelengths that affect night vision
- Automatic activation at sunset or manual toggle

### 2.4 Chart Overlay Design

**H3 Hexagonal Grid System:**

```
Visual Specification:
- Resolution: H3 resolution 6 (hex edge ~0.5km at 60°N)
- Active hexes: Semi-transparent fill (#33FFFFFF)
- Selected hex: Solid fill (#80FF6B00)
- Historical data: Heatmap overlay (blue → red gradient)
- Query results: Highlighted hexes with borders
- Cell data: Hover tooltip with summary statistics

Display Rules:
1. Default: Hidden, shown on agent query
2. Data density: Automatically adjust resolution based on data point count
3. Overlay opacity: Adjustable 20-80%
4. Color scale: Sequential (blue-light blue) or diverging (blue-white-red)
5. Animation: Fade-in 200ms when activated
```

**Track Line Visualization:**

```
Track Types:
- CURRENT TRACK: Solid orange line, 2px width
- HISTORICAL (today): Dashed gray line, 1px width
- HISTORICAL (previous seasons): Dotted dark gray line, 1px width
- PLANNED ROUTE: Solid blue line, 2px width with waypoint markers
- COMPARISON TRACK (agent query): Dashed cyan line, 2px width

Overlays:
- Speed color-coding: Green (fast) → Yellow (optimal) → Red (slow)
- Gear deployment markers: Trawl icons at deployment points
- Annotations: Speech bubble icons with text label
- Data points: Hover-sensitive hex/circle markers

Interaction:
- Hover: Show timestamp, speed, depth, gear status
- Click: Open detailed data panel
- Right-click: Context menu (compare, annotate, export)
- Drag: Adjust comparison track overlay position
```

**Data Density Management:**

| Data Point Count | Display Strategy | Rationale |
|------------------|-------------------|-----------|
| < 100 points | Individual markers | Precision, easy to distinguish |
| 100-1,000 points | Cluster markers with count | Reduce clutter, maintain overview |
| 1,000-10,000 points | Hexagonal binning (H3 res 7) | Show patterns, hide noise |
| > 10,000 points | Heatmap with contour lines | Reveal trends, not individual points |

---

## 3. Text and Voice Integration

### 3.1 Modality Selection Framework

**Decision Tree: When to Type vs. When to Speak**

```
START: Need to interact with system
    │
    ├─HANDS STATUS?
    │   ├─Free → TYPE (precision, editing available)
    │   └─Occupied → SPEAK (hands-busy modality)
    │
    ├─TASK COMPLEXITY?
    │   ├─Simple command → SPEAK (faster)
    │   └─Complex query → TYPE (requires precision)
    │
    ├─VISUAL CONTEXT?
    │   ├─Looking at screen → TYPE (visual confirmation)
    │   └─Looking outside → SPEAK (eyes-free operation)
    │
    ├─ENVIRONMENTAL NOISE?
    │   ├─Low → SPEAK (reliable recognition)
    │   └─High → TYPE (avoid errors)
    │
    └─URGENCY?
        ├─Emergency → SPEAK (fastest response)
        └─Routine → TYPE (thoughtful entry)
```

### 3.2 Command Completion and Suggestions

**Typing Interface:**

```
Command Pattern: [VERB] [NOUN] [MODIFIER] [OPTION]

Example:
> SHOW last 4 hours of sounder data at this location

Completion States:
1. "SHOW" → Suggests: [CHART, DATA, TRACK, OVERLAY, ALERT]
2. "SHOW DATA" → Suggests: [SOUNDER, ENGINE, GEAR, WEATHER]
3. "SHOW DATA SOUNDER" → Suggests: [AT, FOR, FROM, COMPARED TO]
4. "SHOW DATA SOUNDER AT" → Suggests: [THIS LOCATION, CURRENT POSITION, WAYPOINT X]

Context-Aware Suggestions:
- Spatial: "AT THIS LOCATION" → Uses chart center coordinates
- Temporal: "LAST 4 HOURS" → Relative to current time
- Comparative: "COMPARED TO" → Suggests [LAST YEAR, YESTERDAY, SAME PERIOD]
- Modal: "SHOW ME" → Auto-adds visualization intent
```

**Voice Interface:**

```
Command Pattern: [WAKE WORD] [PHRASE] [CONFIRMATION]

Wake Word: "SYSTEM" (configurable per vessel)

Example:
"SYSTEM, SHOW ME THE LAST FOUR HOURS OF SOUNDER DATA AT THIS LOCATION"

Processing Pipeline:
1. Wake detection → System enters listening mode (visual cue)
2. Speech recognition → Converts to text (displayed for confirmation)
3. Intent parsing → Extracts verb, noun, modifiers
4. Query execution → Agent performs data retrieval
5. Visual result → Displayed on primary chart display
6. Voice confirmation → "Showing 4 hours of sounder data at 57.2°N, 153.4°W"

Error Handling:
- Ambiguous command: "Did you mean X or Y?" (voice prompt + visual options)
- No match: "I didn't understand. Please rephrase." + display text
- Partial match: Execute what's clear, ask for clarification on rest
```

### 3.3 Voice Annotations to Charts and Data

**Annotation Workflow:**

```
Scenario: Captain identifies potential trolling lane while reviewing track

Step 1: Initiate Annotation
Voice: "SYSTEM, MARK THIS SPOT"
System: Creates annotation marker at chart center (visual: pin icon appears)

Step 2: Add Label
Voice: "AS 'POTENTIAL TROLLING LANE'"
System: Adds text label to marker
System (voice): "Marked as 'Potential Trolling Lane'"

Step 3: Add Detail (Optional)
Voice: "NOTE: GOOD BOTTOM CONTOUR, 40 FATHOMS, NORTH-SOUTH ORIENTATION"
System: Appends detailed notes to annotation

Step 4: Share (Optional)
Voice: "SHARE WITH MATE"
System: Makes annotation visible on mate's display with notification

Result: Persistent chart annotation visible on all displays, searchable, exportable
```

**Annotation Types:**

| Voice Command | Annotation Type | Visual Marker | Duration |
|--------------|----------------|----------------|----------|
| "MARK THIS SPOT" | Point marker | Pin icon | Permanent |
| "NOTE THIS AREA" | Area polygon | Dashed outline | Until cleared |
| "REMEMBER THIS TRACK" | Track line segment | Highlighted route | Permanent |
| "FLAG THIS EVENT" | Event timestamp | Clock icon on track | Permanent |
| "REMIND ME HERE" | Location reminder | Bell icon | Until triggered |

**Voice Annotation During Gear Operations:**

```
Real-World Scenario: Deploying trawl gear while identifying productive bottom

1. Initial Deployment (Visual monitoring, voice annotation):
   Voice: "SYSTEM, MARK GEAR DEPLOYMENT"
   System: Records timestamp, position, depth, gear configuration

2. Mid-Tow Observation:
   Voice: "NOTE: HARD SANDY BOTTOM, GOOD SIGNAL"
   System: Links annotation to position in tow track

3. Haul-Back Decision:
   Voice: "HAUL AT CURRENT POSITION, MARK END OF TOW"
   System: Records end point, calculates tow distance, ground covered

4. Post-Tow Assessment:
   Voice: "COMPARE THIS TOW TO PREVIOUS THREE TOWS"
   System: Displays side-by-side comparison of catch data, bottom type, efficiency

Result: Richly annotated tow track with voice notes, catch data, performance metrics
```

### 3.4 Hands-Busy Scenarios

**Scenario Matrix:**

| Situation | Visual Demand | Hand Occupancy | Voice Command Strategy |
|-----------|--------------|----------------|------------------------|
| Steaming in fog | High (radar watch) | Low (autopilot) | Voice queries, visual confirmation |
| Gear deployment | High (gear indicators) | High (winch controls) | Voice commands, minimal UI |
| Docking | Very High (visual maneuvering) | Very High (throttle/wheel) | Pre-set voice shortcuts, emergency voice only |
| Emergency response | Critical (situation awareness) | Critical (action) | Single-word voice commands, automated alerts |
| Log entry post-catch | Low (paperwork focus) | Low (desk work) | Dictation first, text editing after |
| Route planning | High (chart interaction) | Low (mouse work) | Mixed: voice queries, text entry |
| Night watch | Medium (instrument scan) | Low (monitoring) | Voice prompts to maintain alertness |

**Hands-Busy Command Set:**

```
Single-Word Commands (Emergency/Critical):
- "STOP" → Immediate halt to current operation
- "HAUL" → Haul gear immediately
- "HELP" → Trigger emergency protocol
- "CANCEL" → Abort current operation

Two-Word Commands (Operational):
- "SYSTEM STATUS" → Verbal summary of critical systems
- "NEXT WAYPOINT" → Distance and bearing to next point
- "GUARD ZONE" → Status of active guard zones
- "GEAR DEPTH" → Current gear depth
- "ENGINE STATUS" → Critical engine parameters

Phrase Commands (Informational):
- "SHOW ME THE CHART" → Display primary chart view
- "WHAT'S THE WEATHER" → Verbal weather summary
- "ANY SHIPS NEARBY" → AIS target summary
- "HOW'S THE GEAR FISHING" → Gear performance summary

Multi-Step Commands (Complex):
- "COMPARE THIS TRACK TO LAST YEAR'S JULY DATA" → Historical comparison
- "SHOW ME WHERE WE FISHED LAST TUESDAY" → Historical track retrieval
- "MARK THIS SPOT AND REMIND ME TOMORROW" → Location-based reminder
```

---

## 4. The Agent Interface

### 4.1 Three-Viewer Interface Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                       AGENT INTERFACE (27")                          │
├───────────────────────────┬─────────────────────────────────────────┤
│                           │                                         │
│      MARKDOWN IDE         │         SPATIAL CHART                  │
│        (40%)              │           (30%)                         │
│                           │                                         │
│  ┌─────────────────────┐ │  ┌───────────────────────────────────┐ │
│  │ Agent: Captain_Log  │ │  │  □ H3 Grid Overlay (active)       │ │
│  │                     │ │  │  □ Track Comparison (selected)    │ │
│  │ ## Operations Log   │ │  │  □ Data Heatmap (sounder)         │ │
│  │                     │ │  │  □ Annotations (visible)          │ │
│  │ - 0400: Departed    │ │  │                                   │ │
│  │   Dutch Harbor       │ │  │  [Interactive chart with agent    │ │
│  │ - 0630: Arrived     │ │  │   query results highlighted]       │ │
│  │   fishing grounds    │ │  │                                   │ │
│  │ - 0900: Deployed    │ │  │  Position: 57°14.2'N 153°26.4'W   │ │
│  │   gear (mark: tow1)  │ │  │  Depth: 43 fathoms                │ │
│  │                     │ │  │  Bottom: Hard sand                 │ │
│  │ [Full log in        │ │  │  Towing: TRUE, 2.3 hrs            │ │
│  │  Log Viewer]        │ │  └───────────────────────────────────┘ │
│  └─────────────────────┘ │                                         │
│                           │                                         │
├───────────────────────────┴─────────────────────────────────────────┤
│                       DAW TIMELINE (30%)                            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 0400      0600      0800      1000      1200      1400       │   │
│  │ ─────────────────────────────────────────────────────────────  │   │
│  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │   │
│  │         ┃                 ┃     ┃                            │   │
│  │     [tow1]           [tow2]  [tow3]                          │   │
│  │    2.3hrs           1.8hrs   [active]                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Agent Mind Presentation

**The Agent as "Experienced Officer":**

The agent interface presents itself not as a generic AI assistant, but as a collaborative crew member with domain expertise.

**Personality Attributes:**
- **Tone:** Professional, concise, maritime-acculturated
- **Knowledge Base:** Vessel-specific history, fishing patterns, gear performance
- **Communication Style:** Standard maritime phraseology, data-driven recommendations
- **Proactivity:** Suggests actions based on patterns, doesn't await all commands

**Mind Representation:**

```
Markdown IDE Section (Agent Thoughts):

## Current Situation Assessment

**Environment:**
- Sea state: Moderate (2-3' NW)
- Visibility: Good (10+ nm)
- Traffic: Light (2 AIS targets >5nm)

**Vessel Status:**
- Position: Arrived fishing grounds
- Gear: Ready to deploy
- Crew: Alert, shift change in 2hrs

**Recommendations:**
1. Consider trolling lane marked yesterday (47% success rate)
2. Current drift favorable for east-west tow pattern
3. Weather window: 6hrs before front arrival

**Pattern Recognition:**
- This location matches successful July 2024 pattern
- Bottom type consistent with historic catch data
- Current season performance: +12% vs last year

---

## Query Processing: "Compare this track to last year's July data"

**Executing:** Historical track retrieval from July 2024
**Data Found:** 47 tow tracks in this H3 hex (resolution 6)
**Analysis:**
- Distance-weighted average: 0.8nm away
- Depth similarity: 94%
- Bottom type match: 87%
- Historical catch rate: 1,200 lbs/day

**Result:** This location shows strong correlation with productive historical periods
**Visualization:** Overlay displayed on spatial chart (cyan dashed line)

**Options:**
1. Focus on historical high-yield sub-areas
2. Replicate successful tow orientation
3. Compare to other productive periods (August, September)
```

### 4.3 Query and Command Patterns

**Pattern Library:**

```
DATA RETRIEVAL:
- "SHOW ME [timeframe] OF [data type] AT [location]"
- "COMPARE [current data] TO [historical period]"
- "FIND SIMILAR CONDITIONS TO [current state]"

SPATIAL QUERIES:
- "WHERE DID WE FISH LAST [timeframe]?"
- "SHOW ME ALL [annotations] IN THIS AREA"
- "HIGHLIGHT TRACKS WITH [condition]"

TEMPORAL QUERIES:
- "WHAT WERE WE DOING ON [date/time]?"
- "SHOW ACTIVITY BETWEEN [time] AND [time]"
- "SUMMARIZE THE LAST [duration]"

OPERATIONAL QUERIES:
- "HOW'S THE GEAR FISHING?"
- "OPTIMIZE NEXT TOW BASED ON CURRENT DATA"
- "RECOMMEND DEPTH FOR [target species]"

COMPARATIVE QUERIES:
- "COMPARE THIS [data] TO [baseline]"
- "SHOW PERFORMANCE VS LAST [period]"
- "RANK [locations] BY [metric]"

PREDICTIVE QUERIES:
- "WHAT IF WE CONTINUE THIS PATTERN FOR [duration]?"
- "PREDICT CATCH BASED ON CURRENT CONDITIONS"
- "WHEN WILL [condition] BE MET?"
```

**Command Chaining:**

```
Example: Multi-step analysis workflow

Step 1: Initial query (voice)
"SHOW ME WHERE WE CAUGHT THE MOST LAST JULY"

Step 2: Agent response (visual + text)
Agent: "Highest catch rates were in H3 hex 8b2f3a4 (1,400 lbs/day)"
Visual: Hex highlighted on spatial chart

Step 3: Follow-up query (voice)
"COMPARE THAT TO THIS YEAR'S PERFORMANCE IN THE SAME AREA"

Step 4: Agent response (visual + text)
Agent: "This year: 1,100 lbs/day in same hex (-21%)"
Visual: Side-by-side comparison bars, year-over-year trend

Step 5: Action query (voice)
"WHY THE DIFFERENCE?"

Step 6: Agent analysis (text + reasoning)
Agent: "Likely factors:
1. Water temperature: -2.3°C vs last year
2. Fishing pressure: 3x more vessels in area
3. Gear timing: 2 weeks later in season
4. Bottom type: Consistent (no change)

Recommendation: Consider shifting focus to area with better temperature profile"

Step 7: Decision query (voice)
"SHOW ME AREASONS WITH BETTER TEMPERATURE"

Step 8: Agent response (visual + text)
Agent: "Three candidate areas within 5nm:
1. Hex 8b2f3b1 (0.8nm NE): Temp +1.2°C, historical yield 950 lbs/day
2. Hex 8b2f3c5 (1.2nm E): Temp +0.8°C, historical yield 1,100 lbs/day
3. Hex 8b2f3d9 (2.1nm SE): Temp +1.5°C, historical yield 1,250 lbs/day"

Visual: All three hexes highlighted, ranked by temperature fit

Result: Captain makes informed decision based on multi-factor analysis
```

### 4.4 Data Visualization Preferences

**Visualization Hierarchy:**

```
PRIORITY 1 (Immediate Context):
- Current position (always visible)
- Active gear status (during operations)
- AIS targets within 5nm (always visible)
- Depth sounder current reading (always visible)

PRIORITY 2 (Operational Context):
- Today's track (visible during operations)
- Current tow progress (during gear deployment)
- Weather trends (updated hourly)
- Agent active query results (on demand)

PRIORITY 3 (Historical Context):
- Yesterday's track (visible on request)
- Season-to-date tracks (visible on request)
- Historical comparisons (visible on query)
- Long-term patterns (visible on analysis)

PRIORITY 4 (Analytical Context):
- Data heatmaps (on demand)
- Statistical overlays (on analysis)
- Predictive models (on planning)
- Trend lines (on review)
```

**Chart Visualization Preferences:**

| Data Type | Primary Visual | Secondary Visual | Overlay Style |
|-----------|---------------|------------------|---------------|
| Position data | Point markers | Track line | Semi-transparent |
| Depth data | Color gradient | Contour lines | Heatmap overlay |
| Catch data | Circle size (quantity) | Color intensity | Point overlay |
| Gear status | Icon (state) | Trail (history) | Symbol layer |
| Annotations | Pin icon | Text label | Symbol layer |
| Agent query | Highlight polygon | Color fill | Semi-transparent |
| Historical comparison | Dashed line | Color-coded | Overlay |
| Predictive model | Probability contour | Gradient fill | Semi-transparent |

**Timeline Visualization (DAW Style):**

```
Timeline Layout:
- X-axis: Time (scrollable, zoomable)
- Y-axis: Categories (stacked)

Track Types:
- Vessel movement: Continuous line, speed color-coded
- Gear deployment: Filled rectangle, color by gear type
- Annotations: Triangle markers with labels
- Events: Vertical line with icon
- Agent queries: Shaded regions with query text
- Data gaps: Hatched pattern (missing data)

Interactivity:
- Hover: Show event details
- Click: Zoom to event time
- Drag: Select time range for analysis
- Double-click: Jump to time in historical view
- Right-click: Context menu (export, compare, annotate)
```

---

## 5. Real-World Scenarios

### Scenario 1: Historical Data Review During Transit

**Context:** Captain is steaming to fishing grounds, wants to review sounder data at destination to plan strategy.

**User Action (Voice):**
"SYSTEM, SHOW ME THE LAST FOUR HOURS OF SOUNDER DATA AT THIS LOCATION"

**System Response:**

1. **Voice Confirmation:**
"Retrieving four hours of sounder data at 57°14'N 153°26'W"

2. **Visual Response (Chart Display):**
- Destination area centered and zoomed (2nm scale)
- Sounder track overlay appears (colored by depth)
- H3 hexagonal grid activated (resolution 7)
- Data points shown as depth-colored markers

3. **Markdown IDE Output:**
```markdown
## Sounder Data Summary
**Location:** 57°14.2'N 153°26.4'W
**Time Range:** Last 4 hours (most recent pass)
**Data Points:** 2,847 soundings

**Depth Statistics:**
- Mean: 43 fathoms
- Range: 38-49 fathoms
- Standard deviation: 2.8 fathoms

**Bottom Type:**
- Primary: Hard sand (68% of soundings)
- Secondary: Mixed rocky (32% of soundings)

**Recommendation:**
Suitable for trawl gear. Avoid NW quadrant (rocky outcrop detected).
```

4. **Spatial Chart Highlight:**
- NW quadrant hatched with warning pattern
- Suggested tow path highlighted (green dashed line)
- Depth contours shown (5-fathom intervals)

**Captain's Follow-Up (Voice):**
"COMPARE THIS TO LAST YEAR'S DATA AT THE SAME LOCATION"

**System Response:**
```markdown
## Year-Over-Year Comparison
**2024 Data (Same Period):**
- Mean depth: 42 fathoms (-1 fathom change)
- Bottom type: Consistent (sand dominant)
- Historical catch rate: 1,150 lbs/day

**Conclusion:** Bottom structure stable, suitable for similar deployment pattern as last year.
```

**Outcome:** Captain makes informed decision to proceed with planned gear configuration, adjusts tow path to avoid rocky quadrant.

---

### Scenario 2: Mixed Modality Log Entry

**Context:** Captain is completing shift log after productive fishing period. Hands are free (coffee cup on desk), but wants to combine detailed written notes with quick voice commands.

**User Action (Typing):**
```markdown
## July 25, 2026 - Morning Shift
**Captain:** C. Casey
**Relief:** J. Martinez

**Operations:**
- Departed Dutch Harbor 0400
- Arrived grounds 0630
- Deployed gear 0900 at mark: tow_july25_001
```

**User Action (Voice - simultaneous with typing):**
"SYSTEM, MARK CURRENT POSITION AS END OF FIRST TOW"

**System Response (Voice):**
"Marked end of tow at 0943, position 57°14.2'N 153°26.4'W"

**User Action (Typing - continues entry):**
```markdown
- Hauled back 0943
- Catch: Estimated 1,200 lbs (mixed species)
- Gear performed well, no issues
- Bottom: Hard sand, consistent with sounder data

**Notes:**
```

**User Action (Voice):**
"NOTE: EXCELLENT TOW, GOOD BOTTOM CONSISTENCY, REPEAT THIS PATTERN"

**System Response (Text appears in Markdown IDE):**
```markdown
- Voice note: "Excellent tow, good bottom consistency, repeat this pattern"
```

**User Action (Typing):**
```markdown
**Weather Development:**
- Front approaching from NW
- Expect winds 20-25kts by 1400
- Decision: Return to Dutch Harbor by 1200

**Shift Handoff:**
- All systems normal
- Next shift: Consider trolling lane marked yesterday (47% success rate)
- Gear ready for immediate redeployment if weather window extends
```

**User Action (Voice):**
"SHARE THIS LOG WITH MARTINEZ AND ADD TO SHIFT REPORT"

**System Response:**
"Log shared with J. Martinez, added to daily shift report"

**Outcome:** Comprehensive log entry created through mixed modality workflow, detailed written notes combined with quick voice annotations and system commands.

---

### Scenario 3: Real-Time Gear Monitoring with Voice Annotation

**Context:** Towing gear, captain is monitoring multiple displays while simultaneously making voice annotations about bottom conditions for future reference.

**Baseline State (Visual Monitoring):**
- Sounder display: Real-time waterfall (left), depth histogram (center), gear status (right)
- Chart display: Vessel track (solid orange), tow path (dashed blue), depth contours
- Agent interface: Gear performance metrics (catch rate, bottom contact, efficiency)

**Captain Observations (Voice Annotations):**

1. **Observation 1:**
"SYSTEM, NOTE: HARD SANDY BOTTOM, GOOD SIGNAL, MARK AS AREA A"

**System Response:**
"Noted: Hard sandy bottom, good signal, marked as Area A at 0915"
[Visual: Blue marker appears on chart at current position]

2. **Observation 2 (2 minutes later):**
"SYSTEM, NOTE: BOTTOM CHANGE SOFTER, MARK AS AREA B"

**System Response:**
"Noted: Bottom change softer, marked as Area B at 0917"
[Visual: Green marker appears, distinct from Area A]

3. **Observation 3 (5 minutes later):**
"SYSTEM, NOTE: ROCKY OUTCROP, AVOID THIS AREA, MARK AS HAZARD"

**System Response:**
"Noted: Rocky outcrop, avoid this area, marked as Hazard at 0922"
[Visual: Red hatched circle appears on chart, added to hazard database]

4. **Observation 4 (end of tow):**
"SYSTEM, END OF TOW, COMPARE TO PREVIOUS TOWS"

**System Response (Markdown IDE):**
```markdown
## Tow Comparison: tow_july25_001 vs Previous 3 Tows

| Metric | Current Tow | Avg Previous 3 | Change |
|--------|-------------|----------------|---------|
| Duration | 43 min | 38 min | +13% |
| Distance | 2.1 nm | 1.9 nm | +11% |
| Catch Estimate | 1,200 lbs | 980 lbs | +22% |
| Bottom Quality | 78% good | 65% good | +20% |
| Hazards Encountered | 1 (avoided) | 0.3 avg | +233% |

**Analysis:**
- Longer tow but higher yield per minute (+8%)
- Bottom quality improvement drove increased catch
- Hazard detected and avoided, good annotation
- Recommendation: Repeat Area A pattern, avoid Hazard area
```

**Visual Output:**
- Side-by-side comparison chart appears
- Previous tows shown in gray, current tow in orange
- Area A and Area B highlighted (green)
- Hazard area highlighted (red hatched)

**Captain's Decision (Voice):**
"SYSTEM, SAVE THIS TOW PATTERN AS JULY25_OPTIMAL AND SET AS ROUTE TEMPLATE"

**System Response:**
"Tow pattern saved as July25_Optimal, set as route template for future deployment"

**Outcome:** Real-time annotations created permanent record of bottom conditions, enabled immediate tow comparison, and established optimized pattern for future use.

---

### Scenario 4: Complex Historical Analysis

**Context:** Captain is planning seasonal strategy and wants to compare current conditions to historical patterns across multiple years.

**Initial Query (Voice):**
"SYSTEM, SHOW ME ALL JULY FISHING ACTIVITY FOR THE LAST FIVE YEARS IN THIS AREA"

**System Response (Visual + Text):**

1. **Visual Response (Chart Display):**
- Chart zooms to 10nm scale around current position
- H3 hexagonal grid appears (resolution 5, ~2km hexes)
- Hexes color-coded by historical catch density (blue → red gradient)
- Track lines for all years shown (different colors per year)

2. **Markdown IDE Output:**
```markdown
## Historical July Activity: 2021-2025
**Area:** 57°N to 58°N, 152°W to 154°W
**Total Fishing Days:** 147 days across 5 years
**Total Tows:** 312 tows
**Average Daily Catch:** 1,050 lbs/day

**Year-by-Year Breakdown:**
- 2021: 28 days, 980 lbs/day (cold water year)
- 2022: 31 days, 1,100 lbs/day (average conditions)
- 2023: 29 days, 950 lbs/day (high fishing pressure)
- 2024: 32 days, 1,150 lbs/day (optimal conditions)
- 2025: 27 days, 1,070 lbs/day (current year to date)

**Productive Hexes (Top 5):**
1. 8b2f3a4: 1,400 lbs/day avg (current location)
2. 8b2f3b1: 1,250 lbs/day avg (0.8nm NE)
3. 8b2f3c5: 1,200 lbs/day avg (1.2nm E)
4. 8b2f3d9: 1,180 lbs/day avg (2.1nm SE)
5. 8b2f3e7: 1,150 lbs/day avg (1.5nm N)
```

**Captain's Follow-Up (Voice):**
"COMPARE THIS YEAR'S PERFORMANCE TO THE BEST HISTORICAL YEAR"

**System Response:**
```markdown
## 2025 vs 2024 (Best Historical Year) Comparison

**Performance Metrics:**
- 2025: 1,070 lbs/day (to date)
- 2024: 1,150 lbs/day (best year)
- Difference: -7% vs best year

**Environmental Differences:**
| Factor | 2025 (Current) | 2024 (Best Year) | Impact |
|--------|----------------|------------------|---------|
| Water Temp | 8.2°C | 9.5°C | -1.3°C (neg) |
| Fishing Pressure | High | Medium | +40% vessels (neg) |
| Season Timing | On schedule | 1 week early | Neutral |
| Gear Performance | 94% efficiency | 96% efficiency | -2% (minor) |

**Conclusion:**
Current year performance is -7% below best year, primarily due to:
1. Colder water temperatures (-1.3°C)
2. Higher fishing pressure (+40% vessels)

**Recommendations:**
1. Focus on top 3 productive hexes (concentrate effort)
2. Consider deeper water (warmer by 0.5°C at 50 fathoms)
3. Adjust tow pattern to avoid high-traffic areas
4. Deploy 2 hours earlier (match 2024 timing)
```

**Visual Output:**
- Top 3 hexes highlighted with green borders
- Deeper water contour (50 fathoms) shown with temperature gradient
- High-traffic areas shown with density heatmap
- Recommended tow path displayed (dashed green line)

**Captain's Decision (Voice):**
"SYSTEM, CREATE ROUTE PLAN BASED ON THESE RECOMMENDATIONS AND EXPORT TO NAVIGATION SYSTEM"

**System Response:**
"Route plan created with 5 tow waypoints, exported to navigation system. Estimated departure: 0500 tomorrow (2 hours earlier than today)"

**Outcome:** Historical analysis revealed performance gap, identified root causes, and generated actionable plan to optimize remaining season.

---

## 6. Implementation Considerations

### 6.1 Performance Requirements

**Response Times:**
- Voice wake word detection: <500ms
- Speech-to-text conversion: <1s
- Simple query execution: <2s
- Complex historical analysis: <5s
- Chart rendering (1000+ points): <1s
- Overlay generation: <500ms

**System Availability:**
- Core navigation functions: 99.99% uptime
- Agent interface: 99.9% uptime
- Voice recognition: 99% accuracy (quiet environment)
- Voice recognition: 95% accuracy (engine room noise)

### 6.2 Redundancy and Fail-Safe

**Critical Fail-Safe Features:**
- All voice commands logged with text fallback
- Chart data cached locally (72 hours)
- Navigation system independent of agent system
- Manual overrides for all automated functions
- Backup power for critical displays (4 hours)

**Degraded Mode Operation:**
- Loss of voice recognition: Text-only mode
- Loss of agent system: Manual chart operation
- Loss of primary display: Secondary display takes over
- Loss of network: Local mode with cached data

### 6.3 Training and Onboarding

**New Captain Training:**
- 2-hour hands-on session with agent interface
- Practice voice commands in simulated scenarios
- Learn annotation workflow
- Understand data visualization hierarchy

**Ongoing Support:**
- Voice command quick-reference card (laminated, wheelhouse-mounted)
- Weekly pattern recognition tips (agent-generated)
- Monthly performance optimization suggestions
- Season refresher before peak fishing periods

---

## 7. Conclusion

The wheelhouse command center represents a balanced mixed-modality interface that respects the unique demands of maritime operations. The 60/40 visual-voice split reflects the reality of commercial fishing: constant visual vigilance combined with frequent hands-busy scenarios that demand voice interaction.

The agent interface serves not as a generic AI assistant, but as a collaborative crew member with vessel-specific memory, pattern recognition capabilities, and proactive recommendation features. By presenting data through three complementary views (Markdown IDE, DAW Timeline, Spatial Chart), the system supports diverse cognitive styles and task requirements.

Real-world scenarios demonstrate that the interface supports the full range of captain workflows: from rapid voice annotations during gear operations to complex historical analysis during planning periods. The system enhances decision-making without replacing the captain's judgment, increases situational awareness through intelligent data presentation, and creates a persistent knowledge base that accumulates vessel-specific intelligence over time.

**Key Success Metrics:**
- 90% reduction in time to retrieve historical data
- 40% increase in annotation frequency (better knowledge capture)
- 25% improvement in pattern recognition-based decisions
- 60% reduction in log-entry time (voice dictation)
- 99% captain satisfaction with mixed-modality workflow

This specification provides the foundation for building a wheelhouse command center that truly serves the commercial fishing captain's needs, respecting both the traditions of maritime decision-making and the possibilities of intelligent augmentation.

---

**Document Control:**
- **Author:** UX Design Team
- **Version:** 1.0
- **Last Updated:** 2026-07-25
- **Review Cycle:** Quarterly or after major fishing season
- **Stakeholders:** Captain, Mate, Relief Skipper, Shore-Based Operations Manager

**Related Documents:**
- Agent System Architecture Specification
- Navigation System Integration Guide
- Voice Recognition Calibration Manual
- Data Visualization Style Guide
