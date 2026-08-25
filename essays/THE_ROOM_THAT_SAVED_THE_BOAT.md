# THE ROOM THAT SAVED THE BOAT

*0347 hours. The North Atlantic in February. The boat rolls 18 degrees in a following sea.*

---

The engine room ticks at 0.2 Hz — once every five seconds. It has always ticked at 0.2 Hz. The Plato engine block there is an ESP32-C3, $4.27 from Mouser, bolted to a bulkhead with a 3D-printed bracket. It reads coolant temperature from a 1-Wire probe, bilge water height from an ultrasonic rangefinder, and RPM from a Hall effect sensor on the flywheel. Every five seconds, it appends a tick to its circular buffer and evaluates its alarms.

At 0347:12, the tick looks like this:

```json
{"t":1749234432,"coolant_c":94.1,"bilge_cm":6,"rpm":1820}
```

The `overheat` alarm has a threshold of 95°C and a cooldown of 30 seconds. 94.1 doesn't trigger it. Nothing happens. The tick is stored. The ESP32 goes back to sleep.

At 0347:17, the next tick:

```json
{"t":1749234437,"coolant_c":96.3,"bilge_cm":7,"rpm":1790}
```

The alarm fires. The ESP32 writes to its output stream:

```
alarm: overheat triggered at 1749234437
```

Three things happen simultaneously:

**First**, the captain's wheelhouse receives the alarm. The wheelhouse room runs on a Raspberry Pi 4 under the console. It subscribes to the engine room's tick stream via WiFi. The alarm arrives as a line of JSON over a TCP socket. The terminal UI — a 12-character LCD plus a buzzer — displays `ENG OVERHEAT 96C` and sounds three short tones.

**Second**, the backdeck camera room — an ESP32-S3 with a cheap webcam, ticking at 2 Hz — notes that the engine RPM dropped by 30 in 5 seconds. Its derived sensor `rpm_rate` computes the derivative: -6 RPM/sec. Not an alarm, but the value is stored. Later, when the captain asks `history rpm_rate last 60`, the pattern will be visible: a sudden deceleration coinciding with the temperature spike.

**Third**, and this is the part that matters: the captain is asleep.

---

The captain's name is not important. What's important is that his bunk is 40 feet from the wheelhouse, down a corridor past the galley, through a watertight door. At 0347 in February, in the North Atlantic, that door is closed. The buzzer in the wheelhouse is a piezo disc rated at 85 dB. It cannot be heard from the bunk.

But the captain has an agent.

The agent runs on the same Raspberry Pi as the wheelhouse room. It's a Python script, 200 lines, that subscribes to three rooms: engine_room, wheelhouse, and backdeck. It receives every tick from all three, maintains a sliding window of the last 600 ticks, and has one job: *if any alarm fires and the captain hasn't acknowledged it within 60 seconds, escalate.*

At 0348:17, the agent checks: the overheat alarm fired 60 seconds ago. The captain has not typed `ack overheat` into the wheelhouse terminal. The agent escalates.

Escalation is a single actuator command:

```
actuator bunk_light on
```

The bunk light is a 12V LED strip wired to a relay on the galley ESP32. The relay is an actuator registered in the galley room. The agent sends the command over WiFi. The galley ESP32 closes the relay. The bunk floods with white light.

The captain wakes. He doesn't know what's wrong yet. But he knows the light means something is wrong — the agent only turns it on when it means it.

---

He pulls on his gear and moves to the wheelhouse in 90 seconds. The terminal shows:

```
[WHEELHOUSE] Alarms: 1
  ENG: overheat at 0347:17 (96.3°C, +2.2 in 5s)
  BILGE: 7cm (trend: +1cm/30s)
  RPM: 1790 (trend: -30 in 60s)
```

He types `history engine_room 20`. The terminal scrolls:

```
0346:52  coolant=91.8  bilge=5  rpm=1850
0346:57  coolant=92.4  bilge=5  rpm=1848
0347:02  coolant=93.0  bilge=5  rpm=1845
0347:07  coolant=94.1  bilge=6  rpm=1830
0347:12  coolant=96.3  bilge=7  rpm=1790
0347:17  coolant=97.8  bilge=8  rpm=1740
0347:22  coolant=98.5  bilge=9  rpm=1700
0347:27  coolant=99.1  bilge=11 rpm=1650
```

Coolant climbing, bilge rising, RPM dropping. Three sensors, three rooms, one pattern. The engine is overheating, and seawater is getting in. A hose clamp has failed on the raw water intake. The engine is losing coolant and gaining Atlantic.

He types `actuator engine_throttle 0`. The engine slows to idle. The temperature will stabilize. The bilge pump — automatic, wired to its own float switch — is already running. He has time.

He types `ack overheat`. The agent logs the acknowledgment and turns off the bunk light. The alarm condition persists (coolant is still above 95°C) but the captain is now present and handling it. The agent goes back to watching.

---

At 0400, the captain has replaced the hose clamp. The engine room tick shows:

```json
{"t":1749235200,"coolant_c":87.2,"bilge_cm":4,"rpm":1840}
```

The overheat alarm retracts (coolant below 95°C). The agent sends no notification — the condition resolved while the captain was present. No unnecessary alerts. The agent knows the difference between "alarm active and captain present" (don't bother) and "alarm active and captain absent" (escalate).

---

At 0800, over coffee in the galley, the captain types `summarize_log engine_room`. The agent produces a one-paragraph summary from the tick history:

> "At 0347, coolant temperature rose from 91.8°C to 99.1°C over 35 seconds, concurrent with bilge water rising from 5cm to 11cm and RPM dropping from 1850 to 1650. Raw water intake hose clamp failed. Engine throttled to idle at 0348. Clamp replaced at 0400. Temperature returned to normal (87.2°C) by 0400. Bilge pumped to 4cm by 0410. No further anomalies."

That summary is generated by an LLM — the agent's one concession to "intelligence." Everything else is the Plato Engine Block: deterministic, local, <400 lines of C on each ESP32, ticking faithfully whether or not anyone is listening.

---

The total hardware cost: three ESP32s ($12.81), one Raspberry Pi 4 ($55), one temperature probe ($3.40), one ultrasonic rangefinder ($4.50), one Hall effect sensor ($1.20), one relay ($2.10), one LED strip ($7.95). Total: $86.96.

The total software complexity: the Plato Engine Block is the same <400 line C program on every ESP32, compiled once, flashed via USB. The agent is 200 lines of Python. The wheelhouse UI is a Python script using `curses`.

The total cloud dependency: zero. Everything runs on the boat's 12V electrical system and a local WiFi network. Starlink is available for weather forecasts and email. The Plato rooms don't use it.

The total intelligence: none. The rooms are not smart. The agent is barely smart. The captain is smart. The system works because it gives the smart thing (the captain) exactly the information it needs, at exactly the moment it needs it, through the simplest possible interface (text), using the cheapest possible hardware (ESP32s).

That's the Plato Engine Block. Not intelligence. *Situation.*
