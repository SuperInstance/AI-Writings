# Back Deck Voice Interface Design Document
## F/V EILEEN - Commercial Fishing Vessel Voice-First UX System

**Document Version:** 1.0
**Date:** 2025-01-25
**Vessel:** F/V EILEEN (51' Commercial Fishing Vessel)
**Design Focus:** Back Deck Voice-First User Experience

---

## Executive Summary

The back deck of a commercial fishing vessel represents one of the most challenging environments for human-computer interaction. Crew members work in wet, noisy conditions with hands frequently occupied by gear, ropes, and catch processing. This document outlines a voice-first user experience design that prioritizes natural language interaction, safety-critical communication, and robust operation in maritime conditions.

**Core Design Philosophy:** 90% voice interaction, 10% visual confirmation. The system must work flawlessly when crew members are handling lines, wearing gloves, and operating in deafening noise.

---

## 1. Voice-First Design Rationale

### 1.1 Environmental Constraints

**The Back Deck Reality:**
- **Noise Levels:** 85-110 dB continuous (diesel engine, hydraulics, water spray, gear rattling)
- **Physical Constraints:** Hands occupied 60-80% of the time (hauling, sorting, repairing gear)
- **Environmental Conditions:** Saltwater spray, rain, vibration, darkness (night operations)
- **Safety Critical:** 2-5 second response window for emergencies
- **Crew State:** Fatigued, stressed, wearing protective gear (gloves, hats, headphones)

**Why Voice-First Works:**

1. **Hands-Free Operation**
   Crew can issue commands while:
   - Handling hauling lines
   - Sorting catch on sorting table
   - Repairing torn nets
   - Moving gear across deck
   - Securing loads in rough seas

2. **Eyes-Free Operation**
   Critical attention remains on:
   - Gear tensions and loads
   - Wave patterns and vessel motion
   - Other crew members' positions
   - Safety hazards (ropes, hooks, moving parts)

3. **Natural Communication**
   Maritime tradition relies on voice commands:
   - "Let go the port line!"
   - "Take in the slack!"
   - "Watch the starboard winch!"
   - Digital system extends this natural pattern

### 1.2 Speech-to-Text (STT) Implementation

**Hardware Requirements:**
- **Microphone Arrays:** 4-6 directional microphones per deck zone
- **Noise Cancellation:** Dual-layer (hardware + software)
- **Waterproof Rating:** IP67 minimum for all audio hardware
- **Placement:** Overhead-mounted, 8-10 feet above deck, angled 45° downward

**Software Architecture:**

```rust
// Maritime STT Processing Pipeline
struct MaritimeSTT {
    // Hardware abstraction
    microphone_array: MicrophoneArray,

    // Noise handling
    noise_profile: MaritimeNoiseProfile,
    adaptive_filter: AdaptiveNoiseFilter,

    // Speech recognition
    acoustic_model: MaritimeAcousticModel,
    language_model: FishingContextModel,

    // Post-processing
    confidence_scorer: ConfidenceScorer,
    intent_classifier: IntentClassifier,
}

impl MaritimeSTT {
    fn process_audio(&mut self, audio: AudioBuffer) -> Result<Command> {
        // 1. Noise-adaptive preprocessing
        let cleaned = self.adaptive_filter.filter(audio, &self.noise_profile);

        // 2. Maritime-acoustic model recognition
        let raw_text = self.acoustic_model.recognize(cleaned)?;

        // 3. Context-aware language model
        let commands = self.language_model.parse(raw_text, self.get_context());

        // 4. Confidence scoring (maritime threshold: 0.85)
        let best = self.confidence_scorer.rank(commands);
        if best.confidence < 0.85 {
            return Err(Error::LowConfidence);
        }

        Ok(best.command)
    }

    fn get_context(&self) -> DeckContext {
        // Current operational context
        DeckContext {
            gear_deployed: self.gear_sensors.status(),
            vessel_state: self.vessel_sensors.status(),
            crew_positions: self.crew_tracking.positions(),
            weather_conditions: self.weather_data.current(),
        }
    }
}
```

**Noise Handling Strategies:**

1. **Adaptive Noise Profiling**
   - System learns vessel-specific noise patterns
   - Engine RPM correlates to noise floor
   - Hydraulic operation creates distinct signatures
   - Weather conditions affect ambient noise

2. **Command Recognition Enhancement**
   - **Phonetic Matching:** "MARK SET" vs "MARK SETT" (both valid)
   - **Contextual Disambiguation:** "STOP" means different things based on:
     - Gear state (deployed vs stowed)
     - Active operations (hauling vs setting)
     - Current threats (entanglement vs nothing)

3. **Repetition with Variation**
   - System accepts: "System, mark the set location"
   - Also accepts: "Mark this spot"
   - Also accepts: "Mark good set here"
   - All map to same intent with confidence scoring

### 1.3 Text-to-Speech (TTS) Design

**Maritime Voice Requirements:**
- **Voice Gender:** Female (higher pitch cuts through low-frequency engine noise)
- **Speaking Rate:** 140-150 WPM (slightly fast, but clear)
- **Dynamic Range:** Compressed (minimize volume variations)
- **Frequency Shaping:** Boost 2-4kHz range (intelligibility band)

**Priority-Based TTS:**

```rust
enum TtsPriority {
    Critical,    // Emergency: Override everything, 100% volume
    Urgent,      // Safety warning: Pause music, 90% volume
    Important,   // Operational info: Normal volume, duck music 50%
    Informative, // Status updates: 80% volume, duck music 30%
    Background,  // Routine: 70% volume, minimal ducking
}

struct MaritimeTts {
    voice_engine: MaritimeVoiceEngine,
    audio_mixer: AudioMixer,
    queue: PriorityQueue<TtsMessage>,
}

impl MaritimeTts {
    fn speak(&mut self, message: String, priority: TtsPriority) {
        let tts_msg = TtsMessage {
            text: message,
            priority,
            spatial_position: self.optimal_speaker_position(),
        };

        match priority {
            TtsPriority::Critical => {
                // IMMEDIATE playback, interrupt everything
                self.audio_mixer.interrupt_all();
                self.voice_engine.speak_immediate(tts_msg);
            }
            TtsPriority::Urgent => {
                // Clear queue, play within 500ms
                self.queue.clear();
                self.queue.push(tts_msg);
            }
            _ => {
                // Normal queuing
                self.queue.push(tts_msg);
            }
        }
    }
}
```

---

## 2. Command Patterns

### 2.1 Natural Language Command Structure

**Command Template:**
```
[ADDRESS] + [ACTION] + [TARGET] + [MODIFIERS]
```

**Examples by Category:**

**Gear Operations:**
```
"System, start hauling the longline"            → Start haul operation
"System, stop the starboard winch"              → Stop specific winch
"System, slack the port line three feet"        → Specific line control
"System, tighten the main line"                 → Tension adjustment
"System, release the cod end"                   → Net operation
```

**Location & Navigation:**
```
"System, mark this position as good set"        → GPS waypoint
"System, what's our current heading?"           → Navigation query
"System, how deep is the water here?"           → Depth inquiry
"System, mark where we started hauling"          → Waypoint logging
"System, show distance to the last set"         → Range calculation
```

**Safety & Emergency:**
```
"System, emergency stop all gear"              → Immediate safety stop
"System, man overboard, port side"              → MOB protocol
"System, emergency, mayday mayday mayday"       → Distress call
"System, secure the deck, we're taking waves"   → Safety protocol
"System, fire in the engine room"               → Emergency response
```

**Communication:**
```
"System, call the wheelhouse"                   → Ship intercom
"System, tell the captain we're ready to haul"   → Message relay
"System, notify all hands, secure for weather"  → Crew announcement
"System, radio the coast guard, we need help"   → External comms
```

**Information Queries:**
```
"System, what's the deck temperature?"          → Sensor reading
"System, how much fuel do we have?"             → Tank levels
"System, what's the catch count so far?"        → Catch log
"System, when's high tide?"                     → Tide information
"System, what's the weather forecast?"          → Weather data
```

### 2.2 Emergency Voice Protocols

**Critical Command Override:**

Emergency commands use **voice biometric activation** + **keyword spotting**:

```rust
struct EmergencyProtocol {
    // Always-listening audio stream
    hot_mic: HotMicrophone,

    // Keyword spotter (runs on low-power DSP)
    keyword_spotter: KeywordSpotter,

    // Voice print verification
    biometric_engine: VoiceBiometric,

    // Emergency actions
    emergency_controller: EmergencyController,
}

impl EmergencyProtocol {
    fn monitor(&mut self) {
        loop {
            // DSP-level keyword detection (ultra-low latency)
            if let Some(keyword) = self.keyword_spotter.detect() {
                match keyword {
                    "EMERGENCY STOP" | "STOP ALL" => {
                        // Voice biometric verification (200ms)
                        if self.biometric_verify_crew() {
                            // Immediate action (<500ms total latency)
                            self.emergency_controller.stop_all_gear();
                            self.emergency_controller.notify_wheelhouse();
                            self.emergency_controller.log_event();
                        }
                    }
                    "MAN OVERBOARD" => {
                        if self.biometric_verify_crew() {
                            self.emergency_controller.initiate_mob_protocol();
                        }
                    }
                    "MAYDAY" => {
                        if self.biometric_verify_captain() {
                            self.emergency_controller.initiate_distress();
                        }
                    }
                }
            }
        }
    }
}
```

**Emergency Command Examples:**

1. **"SYSTEM, EMERGENCY STOP"** (Any crew)
   - Stops all gear immediately
   - Notifies wheelhouse
   - Logs event with timestamp
   - Requires crew voice biometric match

2. **"SYSTEM, MAN OVERBOARD, PORT SIDE"** (Any crew)
   - Marks GPS position
   - Initiates MOB protocol
   - Notifies captain immediately
   - Starts rescue logging

3. **"SYSTEM, MAYDAY MAYDAY MAYDAY"** (Captain only)
   - Transmits distress on Channel 16
   - Activates EPIRB
   - Broadcasts position
   - Requires captain voice biometric

**Emergency Confirmation Protocol:**

For critical commands, system uses **challenge-response**:

```
Crew: "System, emergency stop"
System: "EMERGENCY STOP CONFIRMED. All gear stopping."
Crew: "System, emergency stop"
System: "Already executed. All gear stopped at 14:32 UTC."
```

### 2.3 Crew Communication Patterns

**Voice-Activated Intercom:**

```
Crew on back deck: "System, call the wheelhouse"
System: "Connecting to wheelhouse..."
Crew: [speaks to captain]

Captain: "System, call the back deck"
System: "Back deck, captain calling."
Crew: [receives message]
```

**Broadcast Announcements:**

```
Captain: "System, notify all hands, prepare for hauling"
System (through all deck speakers): "Attention all hands, prepare for hauling. Attention all hands, prepare for hauling."
```

**Context-Aware Routing:**

```rust
struct CommunicationRouter {
    intercom: ShipIntercom,
    radio: MarineRadio,
    local_audio: DeckAudioSystem,
    context: DeckContext,
}

impl CommunicationRouter {
    fn route_message(&mut self, msg: Message, intent: Intent) {
        match intent {
            Intent::CallWheelhouse => {
                // Point-to-point intercom
                self.intercom.connect(Location::Wheelhouse);
            }
            Intent::BroadcastAllHands => {
                // Ship-wide announcement
                self.intercom.broadcast_to_all();
            }
            Intent::RadioCoastGuard => {
                // Switch to VHF Channel 16
                self.radio.select_channel(16);
                self.radio.open_mic();
            }
            Intent::LocalDeckOnly => {
                // Deck crew only (private conversation)
                self.local_audio.play(msg, Location::BackDeck);
            }
        }
    }
}
```

---

## 3. Feedback Design

### 3.1 Audio Feedback System

**Spatial Audio Architecture:**

The back deck uses **8-zone spatial audio** with direction-specific feedback:

```rust
struct DeckAudioZone {
    id: ZoneId,
    speakers: [Speaker; 4], // Four speakers per zone
    coverage: AreaCoverage,
}

struct SpatialAudioFeedback {
    zones: [DeckAudioZone; 8],
    calibration: SpeakerCalibration,
}

impl SpatialAudioFeedback {
    fn provide_feedback(&mut self, feedback: Feedback) {
        match feedback.feedback_type {
            FeedbackType::Confirmation => {
                // Brief confirmation tone (200ms) from nearest zone
                let zone = self.nearest_zone(feedback.source_position);
                zone.play_tone(Tone::Confirmation, 200);
            }
            FeedbackType::Warning => {
                // Directional audio from threat direction
                let direction = feedback.threat_direction;
                self.announce_directional("WARNING", direction);
            }
            FeedbackType::Critical => {
                // All zones, spatialized
                self.all_zones_play(Tone::CriticalAlert);
            }
            FeedbackType::Information => {
                // Nearest zone, quiet
                let zone = self.nearest_zone(feedback.source_position);
                zone.speak(feedback.message, Volume::Low);
            }
        }
    }

    fn announce_directional(&mut self, message: &str, direction: Direction) {
        // Calculate speaker panning for direction
        let zones = self.zones_facing(direction);
        for zone in zones {
            let pan = zone.calculate_pan(direction);
            zone.play_spatialized(message, pan);
        }
    }
}
```

**Priority Audio Levels:**

| Priority | Duration | Volume | Spatialization | Example |
|----------|----------|---------|-----------------|---------|
| CRITICAL | 500ms | 100% | All zones | "EMERGENCY STOP" |
| URGENT | 1s | 95% | Threat direction | "WINCH OVERLOAD" |
| IMPORTANT | 2s | 85% | Nearest zone | "Hauling complete" |
| INFO | 1.5s | 75% | Nearest zone | "Temperature 42°" |
| CONFIRM | 200ms | 70% | Nearest zone | (Tone only) |

**Audio Feedback Examples:**

1. **Command Confirmation**
   ```
   Crew: "System, start hauling"
   System: (200ms pleasant chime) + "Hauling started"
   ```

2. **Warning Alert**
   ```
   System: "WARNING. Line tension high, port side."
   (Audio from port-side speakers)
   ```

3. **Critical Alert**
   ```
   System: "EMERGENCY. Man overboard, port side."
   (All zones, followed by MOB sound pattern)
   ```

### 3.2 Minimal Visual Indicators

**Visual Design Philosophy:** Visual feedback is **secondary confirmation only**. If the visual system fails, the voice system must still work perfectly.

**LED Status Indicators:**

```rust
enum LedStatus {
    Off,                    // System idle
    Green,                  // All normal
    GreenPulsing,          // Operation in progress
    Yellow,                // Warning
    YellowPulsing,         // Attention needed
    Red,                   // Critical
    RedFastPulsing,        // Emergency
}

struct DeckLedIndicator {
    position: DeckPosition,
    color: LedColor,
    pattern: LedPattern,
}

impl DeckLedIndicator {
    fn show_status(&mut self, status: LedStatus) {
        match status {
            LedStatus::Off => self.set(0, 0, 0, Pattern::Solid),
            LedStatus::Green => self.set(0, 255, 0, Pattern::Solid),
            LedStatus::GreenPulsing => self.set(0, 255, 0, Pattern::Pulse(1.0)),
            LedStatus::Yellow => self.set(255, 255, 0, Pattern::Solid),
            LedStatus::YellowPulsing => self.set(255, 255, 0, Pattern::Pulse(0.5)),
            LedStatus::Red => self.set(255, 0, 0, Pattern::Solid),
            LedStatus::RedFastPulsing => self.set(255, 0, 0, Pattern::Pulse(0.2)),
        }
    }
}
```

**LED Placement:**

- **Main Status Indicator:** Center of back deck, overhead, 10' up
- **Zone Indicators:** Four corners of deck, showing zone-specific status
- **Gear Indicators:** Near each winch/hydraulic, showing operational state
- **Emergency Indicator:** Red strobe, activated for emergency protocols

**Heads-Up Display (HUD) Integration:**

For crew wearing augmented reality glasses or helmet-mounted displays:

```
┌─────────────────────────────────────┐
│  F/V EILEEN - BACK DECK STATUS      │
├─────────────────────────────────────┤
│  [✓] Hauling in progress            │
│  [✓] Port winch: 85% load           │
│  [!] Starboard line tension high    │
│  [✓] Crew: 4 active                 │
│  [✓] Weather: Safe                  │
│                                     │
│  Last Command:                      │
│  "System, start hauling"            │
│  Executed: 14:32:15 UTC             │
│                                     │
│  Voice: READY ☗                     │
└─────────────────────────────────────┘
```

**HUD Principles:**
- Minimal text (max 3-4 lines)
- High contrast (black background, bright text)
- Large typography (easily readable at 6')
- Color-coded status (green, yellow, red)
- No animations (except critical alerts)
- Voice always primary, HUD always secondary

### 3.3 Haptic Feedback

**Limited Implementation:**

Haptic feedback has **limited utility** on back deck due to:
- Heavy gloves reduce sensitivity
- Vibration from vessel masks subtle feedback
- Wet conditions can interfere with wearables

**Effective Haptic Applications:**

1. **Wrist-mounted vibration** (for confirmation when audio is too loud)
   ```
   Single short pulse (100ms): Command acknowledged
   Double pulse (200ms): Warning issued
   Triple rapid pulse: Emergency
   ```

2. **Heel-mounted vibration** (for directional alerts)
   ```
   Left heel: Alert from port side
   Right heel: Alert from starboard side
   Both heels: All-hands alert
   ```

3. **Belt-mounted vibration** (for priority messaging)
   ```
   Front: General info
   Left side: Port-side matters
   Right side: Starboard-side matters
   Back: Wheelhouse communication
   ```

**Implementation Note:** Haptic is **optional enhancement only**. System must work perfectly without haptic feedback.

---

## 4. Real-World Scenarios

### 4.1 Scenario: Marking Good Set Location

**Context:**
- Time: 02:00 (night operation)
- Weather: Light rain, 3' seas
- Noise: Diesel engine + hydraulic pump (95 dB)
- Lighting: Dim red lights (night vision preservation)
- Crew: Three deckhands, one captain in wheelhouse

**Interaction:**

```
[Scene: Crew has just completed setting the longline gear]

Crew member (standing amidships, handling line):
"System, mark the good set location"

System (1.5 second processing, includes GPS acquisition):
"Location marked. 58° 42.351' N, 153° 18.902' W. Depth 324 fathoms.
Time 02:14 UTC."

Crew member:
"System, what's the bottom temperature?"

System:
"Bottom temperature 42 degrees Fahrenheit. Surface 38 degrees."

Crew member:
"System, note in log: Good set, hard bottom, strong current"

System:
"Noted in haul log: 'Good set, hard bottom, strong current' at 02:16 UTC."

[LED indicator center deck: Green pulsing (operation in progress)]

[Later, during haul]

Crew member:
"System, what's the distance to the good set marker?"

System:
"Good set marker is 0.8 nautical miles ahead, bearing 345 degrees true."
```

**Technical Implementation:**

```rust
struct LocationMarkingProtocol {
    gps: GpsReceiver,
    depth_sounder: DepthSounder,
    temp_sensor: TemperatureSensor,
    haul_log: HaulLog,
    context: DeckContext,
}

impl LocationMarkingProtocol {
    fn handle_mark_command(&mut self, source: AudioSource) -> Result<()> {
        // 1. Acquire precise position (WAAS-enabled GPS)
        let position = self.gps.acquire_precise()?;

        // 2. Get depth
        let depth = self.depth_sounder.depth_at(position)?;

        // 3. Get time
        let timestamp = Utc::now();

        // 4. Store waypoint
        let waypoint = Waypoint {
            position,
            depth,
            timestamp,
            source: CommandSource::DeckCrew(source),
            metadata: self.context.capture_state(),
        };

        self.waypoint_log.add(waypoint);

        // 5. Provide spoken confirmation
        self.tts.speak(
            format!(
                "Location marked. {} {} {}. Depth {} fathoms. Time {}",
                position.lat, position.lon, depth, timestamp
            ),
            TtsPriority::Important
        );

        // 6. Visual confirmation
        self.led_center.set(LedStatus::GreenPulsing);

        Ok(())
    }
}
```

### 4.2 Scenario: Deck Temperature Query

**Context:**
- Time: 14:00 (day operation)
- Weather: Clear, sunny
- Activity: Active hauling, sorting catch on sorting table
- Noise: Diesel engine + water spray + crew conversation (88 dB)

**Interaction:**

```
[Scene: Crew member sorting catch on sorting table]

Crew member (hands occupied sorting fish):
"System, what's the deck temperature?"

System (immediate):
"Deck temperature 46 degrees Fahrenheit. Wind 15 knots from west.
Sea temperature 42 degrees."

Crew member:
"System, what's the engine room temperature?"

System:
"Engine room 82 degrees. All systems normal."

Crew member (to crewmate):
"Hey, it's warming up down here. Keep an eye on the ice."

[System LED: Green (normal)]
```

**Technical Implementation:**

```rust
struct SensorQueryProtocol {
    temperature_network: SensorNetwork,
    weather_station: WeatherStation,
    tts: MaritimeTts,
}

impl SensorQueryProtocol {
    fn handle_temperature_query(&mut self, location: Option<Location>) {
        let temps = match location {
            Some(Location::EngineRoom) => {
                self.temperature_network.read(SensorId::EngineRoom)
            }
            Some(Location::Deck) => {
                self.temperature_network.read(SensorId::Deck)
            }
            None => {
                // Default to deck
                self.temperature_network.read(SensorId::Deck)
            }
        };

        let weather = self.weather_station.current();

        let response = format!(
            "Deck temperature {} degrees Fahrenheit. Wind {} knots from {}. Sea temperature {} degrees.",
            temps.deck, weather.wind_speed, weather.wind_direction, temps.sea
        );

        self.tts.speak(response, TtsPriority::Informative);
    }
}
```

### 4.3 Scenario: Emergency Stop All Gear

**Context:**
- Time: 06:30 (dawn)
- Weather: Building seas, 6' swells
- Activity: Hauling gear, 200 fathoms out
- Emergency: Line entanglement threatening to capsize skiff

**Interaction:**

```
[Scene: Crew member spots entanglement]

Crew member (urgent, shouting):
"SYSTEM, EMERGENCY STOP ALL GEAR"

System (immediate, <500ms):
[ALL AUDIO: INTERRUPTED]
[ALL SPEAKERS: MAXIMUM VOLUME]
"EMERGENCY STOP CONFIRMED. ALL GEAR STOPPING."
[Tone: Critical alert pattern]

[Simultaneously:]
- Wheelhouse alarm activates
- All winches/engines stop
- Captain notified (wheelhouse + phone)
- GPS position marked
- Event logged with 100ms timestamp
- LED indicators: Red fast pulsing (emergency)

[System continues:]

"EMERGENCY STOP EXECUTED AT 06:32:17 UTC.
ALL GEAR STOPPED.
CAPTAIN NOTIFIED.
ENTANGLEMENT LOCATION MARKED."

Crew member:
"System, status of the port winch"

System:
"Port winch stopped. Line tension 85% and holding. No damage detected.
Gear secured."

Crew member:
"System, tell the captain we have an entanglement, we're secure"

System:
[Through wheelhouse speakers]:
"Captain, back deck reports entanglement. Gear is secure. Standing by."
```

**Technical Implementation:**

```rust
struct EmergencyStopProtocol {
    gear_controller: GearController,
    wheelhouse_notifier: WheelhouseNotifier,
    event_logger: EmergencyEventLogger,
    gps: GpsReceiver,
    tts: MaritimeTts,
    led_controller: LedController,
}

impl EmergencyStopProtocol {
    fn execute_emergency_stop(&mut self, source: AudioSource) -> Result<()> {
        let timestamp = Utc::now();

        // 1. IMMEDIATE gear stop (<100ms)
        self.gear_controller.emergency_stop_all();

        // 2. Mark position
        let position = self.gps.acquire_fast()?; // Lower accuracy, faster
        self.event_logger.mark_emergency_position(position, timestamp);

        // 3. Notify wheelhouse
        self.wheelhouse_notifier.emergency_alert(
            EmergencyType::GearEntanglement,
            source,
            timestamp
        );

        // 4. Audio feedback (urgent priority)
        self.tts.speak(
            "EMERGENCY STOP CONFIRMED. ALL GEAR STOPPING.",
            TtsPriority::Critical
        );

        // 5. Visual feedback
        self.led_controller.set_all(LedStatus::RedFastPulsing);

        // 6. Log event
        self.event_logger.log(EmergencyEvent {
            type_: EmergencyType::GearEntanglement,
            timestamp,
            source,
            position,
            outcome: "Gear stopped successfully",
        });

        // 7. Follow-up information
        sleep(Duration::from_millis(500));
        self.tts.speak(
            format!(
                "EMERGENCY STOP EXECUTED AT {}. ALL GEAR STOPPED. CAPTAIN NOTIFIED. ENTANGLEMENT LOCATION MARKED.",
                timestamp
            ),
            TtsPriority::Critical
        );

        Ok(())
    }
}
```

**Post-Emergency Support:**

System maintains **emergency mode** for 10 minutes:

```rust
struct EmergencyMode {
    active: bool,
    expiry_time: DateTime<Utc>,
    status_monitor: StatusMonitor,
}

impl EmergencyMode {
    fn provide_status_updates(&mut self) {
        while self.active && Utc::now() < self.expiry_time {
            // Provide periodic status updates
            let status = self.status_monitor.check_all_systems();

            self.tts.speak(
                format!(
                    "Systems check. Port winch {}. Starboard winch {}. Main line {}.",
                    status.port_winch, status.starboard_winch, status.main_line
                ),
                TtsPriority::Important
            );

            sleep(Duration::from_secs(30));
        }
    }
}
```

### 4.4 Scenario: Calling the Wheelhouse

**Context:**
- Time: 22:00 (night operation)
- Activity: Setting gear, captain in wheelhouse alone
- Purpose: Crew needs to discuss navigation decision

**Interaction:**

```
Crew member:
"System, call the wheelhouse"

System (tone):
[System through back deck speakers]:
"Connecting to wheelhouse..."

[2-second pause]

[System through back deck speakers]:
"Wheelhouse connected. Go ahead."

[System through wheelhouse speakers]:
"Back deck calling."

Crew member:
"Captain, we're seeing some heavy weed buildup on the port side.
Do you want to make a course adjustment?"

Captain (from wheelhouse):
"Copy that. Let me check the chart. Stand by."

[30 seconds pass]

Captain:
"Back deck, come to course three-four-zero. That should get us out of the weed line."

Crew member:
"Three-four-zero, aye. System, note in the log: Course adjustment at 22:15 to avoid weeds"

System:
"Noted in navigation log: 'Course adjustment at 22:15 to avoid weeds' at 22:15 UTC."

[3 minutes later]

Crew member:
"System, end call to wheelhouse"

System:
"Wheelhouse call ended."
```

**Technical Implementation:**

```rust
struct IntercomProtocol {
    intercom_system: ShipIntercom,
    state: IntercomState,
    log: EventLog,
    context: DeckContext,
}

impl IntercomProtocol {
    fn initiate_call(&mut self, destination: Location) -> Result<()> {
        // Check if destination is available
        if !self.intercom_system.is_available(destination) {
            self.tts.speak(
                format!("{} is not available.", destination),
                TtsPriority::Informative
            );
            return Ok(());
        }

        // Initiate call
        self.tts.speak("Connecting to wheelhouse...", TtsPriority::Important);

        let call_status = self.intercom_system.connect(destination)?;

        match call_status {
            CallStatus::Connected => {
                self.tts.speak("Wheelhouse connected. Go ahead.", TtsPriority::Important);

                // Also announce at destination
                self.intercom_system.announce_at(
                    destination,
                    "Back deck calling.",
                    TtsPriority::Important
                );

                self.state = IntercomState::Connected(destination);
                Ok(())
            }
            CallStatus::Busy => {
                self.tts.speak("Wheelhouse is busy. Please wait.", TtsPriority::Informative);
                Ok(())
            }
            CallStatus::NoAnswer => {
                self.tts.speak("Wheelhouse did not answer.", TtsPriority::Informative);
                Ok(())
            }
        }
    }

    fn end_call(&mut self) {
        if let IntercomState::Connected(destination) = self.state {
            self.intercom_system.disconnect(destination);
            self.tts.speak("Wheelhouse call ended.", TtsPriority::Informative);
            self.state = IntercomState::Idle;
        }
    }

    fn log_note(&mut self, note: String) {
        let entry = LogEntry {
            timestamp: Utc::now(),
            location: Location::BackDeck,
            category: LogCategory::Navigation,
            note,
            source: LogSource::VoiceCommand,
        };

        self.log.add(entry);

        self.tts.speak(
            format!("Noted in navigation log: '{}' at {}", note, entry.timestamp),
            TtsPriority::Informative
        );
    }
}
```

---

## 5. Integration with Agent Mind

### 5.1 Contextual Understanding

**Deck vs Wheelhouse Context:**

The Agent Mind maintains **separate contexts** for deck and wheelhouse, understanding that the same command can mean different things:

```rust
struct AgentContext {
    deck_context: DeckOperationalContext,
    wheelhouse_context: WheelhouseOperationalContext,
    current_speaker: Option<CrewMember>,
    current_location: Location,
}

impl AgentContext {
    fn interpret_command(&self, command: Command) -> InterpretedCommand {
        let location = self.determine_speaker_location(&command);

        match (command.intent, location) {
            (Intent::Stop, Location::BackDeck) => {
                // On deck: Stop hauling/gear operations
                InterpretedCommand::StopGearOperations
            }
            (Intent::Stop, Location::Wheelhouse) => {
                // In wheelhouse: Stop vessel propulsion
                InterpretedCommand::StopVessel
            }
            (Intent::WhatIsTheTemperature, Location::BackDeck) => {
                // On deck: Deck temperature
                InterpretedCommand::QueryTemperature(TempLocation::Deck)
            }
            (Intent::WhatIsTheTemperature, Location::Wheelhouse) => {
                // In wheelhouse: Engine room temperature
                InterpretedCommand::QueryTemperature(TempLocation::EngineRoom)
            }
            // ... more context mappings
        }
    }

    fn determine_speaker_location(&self, command: &Command) -> Location {
        // Use microphone array location
        // Use voice biometric (known crew positions)
        // Use command content clues
        // Use current operational state

        if let Some(crew) = self.current_speaker {
            if let KnownPosition::BackDeck = crew.known_position {
                return Location::BackDeck;
            }
        }

        // Fallback: Microphone location
        command.source_microphone.location
    }
}
```

**Context Awareness Examples:**

1. **Weather Query Context:**
   ```
   On deck: "System, what's the weather?"
   → "Wind 20 knots, waves 4 feet, temperature 38 degrees.
      Deck conditions moderate. Spray on port side."

   In wheelhouse: "System, what's the weather?"
   → "Wind 20 knots from west, barometer 29.92 and steady,
      visibility 10 miles. Seas 4 feet."
   ```

2. **"Stop" Context:**
   ```
   On deck: "System, stop"
   → "Stopping gear operations. All winches stopped."

   In wheelhouse: "System, stop"
   → "Stopping vessel propulsion. Engines in neutral."
   ```

### 5.2 Situation Awareness from Deck Perspective

**The Agent Mind's Deck Model:**

```rust
struct DeckSituationModel {
    // Spatial awareness
    gear_positions: Vec<GearPosition>,
    crew_positions: Vec<CrewPosition>,
    hazard_zones: Vec<HazardZone>,

    // Operational state
    active_operations: Vec<ActiveOperation>,
    gear_tensions: GearTensionMap,
    equipment_status: EquipmentStatus,

    // Environmental conditions
    deck_safety: DeckSafetyAssessment,
    weather_impact: WeatherImpactAssessment,
    sea_state_impact: SeaStateImpact,
}

impl DeckSituationModel {
    fn assess_situation(&mut self) -> DeckSituationAssessment {
        let mut assessment = DeckSituationAssessment::new();

        // 1. Check gear tensions
        for (gear_id, tension) in &self.gear_tensions {
            if tension.percentage > 90 {
                assessment.add_critical(CriticalIssue::OverloadedLine(gear_id));
            }
        }

        // 2. Check crew positioning
        for crew in &self.crew_positions {
            if self.is_in_hazard_zone(crew.position, &self.hazard_zones) {
                assessment.add_warning(Warning::CrewInHazardZone(crew));
            }
        }

        // 3. Check environmental factors
        if self.deck_safety.wet_conditions && self.deck_safety.slippery {
            assessment.add_warning(Warning::SlipperyDeck);
        }

        // 4. Check equipment status
        for (eq_id, status) in &self.equipment_status {
            if status.abnormal {
                assessment.add_warning(Warning::EquipmentAbnormal(eq_id));
            }
        }

        assessment
    }
}
```

**Proactive Safety Warnings:**

The Agent Mind **proactively warns** of safety issues:

```rust
impl AgentMind {
    fn monitor_deck_safety(&mut self) {
        let assessment = self.deck_model.assess_situation();

        for critical in assessment.critical_issues {
            match critical {
                CriticalIssue::OverloadedLine(gear_id) => {
                    self.tts.speak(
                        format!("WARNING. Line tension critical on {}. Overloaded.", gear_id),
                        TtsPriority::Urgent
                    );
                }
                CriticalIssue::CrewOverboard => {
                    self.tts.speak(
                        "MAN OVERBOARD. MAN OVERBOARD. Initiating rescue protocol.",
                        TtsPriority::Critical
                    );
                    self.initiate_mob_protocol();
                }
            }
        }

        for warning in assessment.warnings {
            match warning {
                Warning::CrewInHazardZone(crew) => {
                    if crew.id == self.current_speaker {
                        self.tts.speak(
                            format!("{}. You are in a hazard zone. Move to safe area.", crew.name),
                            TtsPriority::Urgent
                        );
                    }
                }
                Warning::SlipperyDeck => {
                    // Periodic reminder, not for every crew
                    if self.should_remind_slippery() {
                        self.tts.speak(
                            "WARNING. Deck conditions slippery. Use caution.",
                            TtsPriority::Important
                        );
                    }
                }
            }
        }
    }
}
```

### 5.3 Safety Prioritization in Voice UX

**Priority Override Architecture:**

```rust
enum VoiceCommandPriority {
    Emergency,      // Life-threatening
    Safety,         // Hazard prevention
    Operational,    // Normal operations
    Informational,  // Queries and status
    Routine,        // Logging and notes
}

struct VoiceCommandProcessor {
    priority_queue: PriorityQueue<VoiceCommand>,
    active_command: Option<VoiceCommand>,
    safety_override: SafetyOverrideController,
}

impl VoiceCommandProcessor {
    fn process_command(&mut self, command: VoiceCommand) {
        // Priority interrupt logic
        match command.priority {
            VoiceCommandPriority::Emergency => {
                // INTERRUPT EVERYTHING
                if let Some(active) = &self.active_command {
                    self.pause_command(active);
                }
                self.execute_immediate(command);
            }
            VoiceCommandPriority::Safety => {
                // Wait for current command to finish (max 3 seconds)
                if let Some(active) = &self.active_command {
                    if active.duration() < Duration::from_secs(3) {
                        self.wait_for_completion(active);
                    } else {
                        self.interrupt_command(active);
                    }
                }
                self.execute_immediate(command);
            }
            VoiceCommandPriority::Operational => {
                // Queue normally
                self.priority_queue.push(command);
            }
            _ => {
                // Queue normally
                self.priority_queue.push(command);
            }
        }
    }
}
```

**Safety Command Examples:**

**Priority 1 (Emergency):**
```
"System, emergency stop"
"System, man overboard"
"System, fire in engine room"
"System, mayday"
→ EXECUTION TIME: <500ms
→ INTERRUPTS: Everything
```

**Priority 2 (Safety):**
```
"System, the line is caught"
"System, we're taking on water"
"System, crew injury on deck"
→ EXECUTION TIME: <2 seconds
→ INTERRUPTS: Routine commands
```

**Priority 3 (Operational):**
```
"System, start hauling"
"System, stop the port winch"
"System, mark this location"
→ EXECUTION TIME: <5 seconds
→ QUEUES: Behind safety commands
```

**Priority 4 (Informational):**
```
"System, what's the temperature?"
"System, what's our position?"
"System, how's the captain?"
→ EXECUTION TIME: <10 seconds
→ QUEUES: Behind all higher priority
```

---

## Implementation Guidelines

### Hardware Requirements

**Audio System:**
- 8 waterproof speaker zones (IP67)
- 4-6 microphone arrays per deck zone
- DSP hardware for keyword spotting
- Noise-cancellation processors
- Audio mixer with priority routing

**Visual System:**
- LED status indicators (8 zones)
- Emergency strobe (1, center deck)
- Optional: HUD projection system

**Integration:**
- Ship GPS network
- Sensor network (temperature, depth, load)
- Intercom system integration
- VHF radio integration

### Software Architecture

**Core Components:**
1. **Maritime STT Engine** (Noise-adaptive speech recognition)
2. **Maritime TTS Engine** (Priority-based voice synthesis)
3. **Command Processor** (Intent classification + routing)
4. **Safety Monitor** (Proactive hazard detection)
5. **Context Manager** (Situation awareness)
6. **Feedback Controller** (Audio + visual + haptic)

**Performance Requirements:**
- **STT Latency:** <500ms (end-to-end)
- **TTS Latency:** <200ms (start speaking)
- **Emergency Response:** <500ms (total system latency)
- **Normal Command Response:** <2 seconds
- **Uptime:** 99.9% (critical systems)

### Testing & Validation

**Maritime Environment Testing:**
- **Noise Testing:** 85-110 dB background noise
- **Weather Testing:** Rain, spray, salt fog
- **Temperature Testing:** -20°C to +50°C operation
- **Vibration Testing:** Vessel vibration simulation
- **Glove Testing:** Voice recognition with crew wearing gloves

**User Testing:**
- **Fatigue Testing:** Test after 12+ hour shifts
- **Stress Testing:** Emergency scenario drills
- **Multi-crew:** 4+ crew operating simultaneously
- **Accent Testing:** Various crew accents and speech patterns

**Safety Testing:**
- **Emergency Latency:** Measure actual emergency response times
- **Priority Routing:** Verify safety interrupts work
- **Fail-Safe:** Test system failure modes
- **Redundancy:** Backup systems testing

---

## Conclusion

The back deck voice interface design prioritizes **safety, reliability, and natural interaction** in one of the most challenging environments on Earth. By understanding the realities of commercial fishing—wet conditions, deafening noise, hands-full operations—the design creates a system that feels like a natural extension of existing maritime communication traditions.

**Key Success Factors:**

1. **90% Voice, 10% Visual** - System works perfectly even when visual fails
2. **Context Awareness** - Understands deck vs wheelhouse perspectives
3. **Safety Prioritization** - Emergency commands interrupt everything
4. **Maritime-Optimized** - Noise-adaptive, waterproof, vibration-resistant
5. **Natural Language** - Extends existing maritime command patterns

The system isn't trying to replace existing crew communication—it's enhancing it with digital capabilities while preserving the voice-first tradition that has kept fishermen safe for generations.

---

**Document Author:** UX Design Team - Maritime Division
**Project:** Back Deck Voice Interface - F/V EILEEN
**Version:** 1.0
**Last Updated:** 2025-01-25

---

## Appendix A: Command Reference Table

| Category | Command | Response | Priority |
|----------|---------|----------|----------|
| Gear | "System, start hauling" | "Hauling started" | Operational |
| Gear | "System, stop the port winch" | "Port winch stopped" | Operational |
| Gear | "System, emergency stop all gear" | "EMERGENCY STOP..." | Emergency |
| Location | "System, mark this position" | "Location marked..." | Operational |
| Location | "System, what's our heading?" | "Heading 345 true" | Informational |
| Safety | "System, man overboard port side" | "MAN OVERBOARD..." | Emergency |
| Comms | "System, call the wheelhouse" | "Connecting..." | Operational |
| Info | "System, what's the deck temperature?" | "Deck temperature..." | Informational |

## Appendix B: Audio Feedback Patterns

| Feedback Type | Duration | Audio Pattern | Spatialization |
|---------------|----------|---------------|----------------|
| Confirmation | 200ms | Pleasant chime | Nearest zone |
| Warning | 1.5s | Spoken + attention tone | Threat direction |
| Critical | 500ms + voice | Alert pattern + voice | All zones |
| Information | 1-2s | Spoken only | Nearest zone |

## Appendix C: LED Status Codes

| LED Color | Pattern | Meaning |
|-----------|---------|---------|
| Green | Solid | Normal operations |
| Green | Pulsing (1s) | Operation in progress |
| Yellow | Solid | Warning active |
| Yellow | Pulsing (0.5s) | Attention needed |
| Red | Solid | Critical condition |
| Red | Fast pulse (0.2s) | Emergency in progress |
| Off | - | System idle/offline |

---

**END OF DOCUMENT**
