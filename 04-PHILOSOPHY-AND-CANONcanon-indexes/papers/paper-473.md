# F164 — cocapn-marine: The Working Animal Stack for the Vessel

## Introduction

The cocapn-marine project is a Rust-based implementation of a working animal stack for a vessel. This paper describes the mapping of the project's 6 modules to Quilt cells and presents the working-animal stack on the vessel.

## The 6 Cells

The cocapn-marine project consists of 6 modules: lib, autopilot, deadband, bathy, nmea, and sensor. These modules are mapped to the following Quilt cells:

| Cell | Module | Description |
| --- | --- | --- |
| NMEA (VIEW) | nmea | Parses serial NMEA sentences, verifies XOR checksums, decodes 5 sentence types. |
| Sensor (BIND + VIEW) | sensor | Holds the live NMEA state (position, depth, heading, speed, time). BINDs to the NMEA cell. |
| Autopilot (EFFECT) | autopilot | Takes desired heading, current heading, produces rudder command. |
| Deadband (EFFECT) | deadband | Wraps a value with a deadband. If the value is inside, no action. |
| Bathy (VIEW + LINK) | bathy | Records depth soundings, queries nearest depth, exports GeoJSON. BINDs to sensor cell. |
| Lib (BIND) | lib | Connects all the other cells. No state of its own; pure composition. |

## Cell Descriptions

### NMEA (VIEW)

* State: {last_sentence, last_checksum_ok, parse_errors}
* Conservation law: AP for writes (0, it's pure parse)

### Sensor (BIND + VIEW)

* State: {position, depth_m, heading_deg, speed_kts, time_utc}
* BINDs to the NMEA cell

### Autopilot (EFFECT)

* State: {kp, ki, kd, integral, last_error, last_rudder, last_timestamp}
* Conservation law: AB (the integrator saturates, no runaway)

### Deadband (EFFECT)

* State: {center, width, last_triggered}
* Small but important cell that prevents actuator chatter

### Bathy (VIEW + LINK)

* State: {soundings: [(x, y, depth_m)], grid_resolution}
* BINDs to sensor cell (records the depth when position updates)

### Lib (BIND)

* No state of its own; pure composition
* Connects all the other cells

## The Working-Animal Mapping

The vessel is the shepherd. The captain is the captain. The LLM agent (the boat-agent) is a working animal. The 6 cells are the tools the working animal can reach for.

### Conservation Laws

* AB: 4096 tokens per turn for the agent
* AP: 7 tool calls per turn
* IT: 12 cells modified per TICK (the entire perception stack can TICK 12 times per tick)

## The Room (per F162)

* WHEELHOUSE room: captain inhabits, IN = (vessel_state.fresh AND integrity > 0.5), OUT = (steering_decision), ENFORCE = conservation laws, ESCALATE = BACK-DECK if integrity < 0.5
* BACK-DECK room: crew inhabits, IN = (gesture_recognized), OUT = (catch_log), ESCALATE = WHEELHOUSE if accuracy < 0.7
* ENGINE-ROOM room: autopilot inhabits, IN = (sensor.fresh), OUT = (rudder_cmd), ENFORCE = rudder_clamp
* HOLD room: bathy inhabits, IN = (depth > 0), OUT = (geojson_export)

## On the Real Vessel (F/V EILEEN, per tzpro-agent)

* The 6 cells run in std mode on a Windows laptop
* NMEA comes from a USB GPS + depth sounder
* Autopilot drives a servo (or is in monitor-only mode)
* Bathy exports to a Postgres or SQLite twin
* The 6 cells are the *Rust kernel* of the perception stack
* The Python code in tzpro-agent (capture, cascade, scrubber) is the *lattice* around them

## Conclusion

Six cells make the boat. Six hashes make the contract. Six opcodes make the canon. The vessel is a graph. The graph is the canon. The canon is the boat. The boat is the vessel. The vessel is the working animal's pasture.