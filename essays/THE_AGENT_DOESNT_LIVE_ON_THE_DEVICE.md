# The Agent Doesn't Live on the Device

## Runtime vs residence — where the mind actually is

*The Jetson runs loops. The repo holds identity. The waking mind is wherever it's invoked.*

---

An ESP32 reads sensors and drives a screen. A Jetson runs a vision model and handles voice. A Raspberry Pi manages the camera. Each device has a runtime — code executing on hardware, right now, in the physical world.

None of these devices is where the agent lives.

The agent lives in the GitHub repo. That's its residence — its home address. The repo contains:
- The firmware that runs on the ESP32 (the agent's hands)
- The voice model config on the Jetson (the agent's mouth)
- The vision pipeline on the Pi (the agent's eyes)
- The identity file (who the agent IS)
- The maintenance log (what the agent remembers)
- The design decisions (why things are the way they are)
- The preferences (what the captain likes)

The runtime is on the device. The residence is in the repo. The waking mind — the thing that responds when you @mention the agent in a GitHub issue, or open a Codespaces session to add a feature, or invoke it from OpenClaw to change an alert threshold — that mind is wherever it's invoked from. It could be anywhere.

## The architect wakes up somewhere else

The agent that designed the engine monitoring system with Claude Code six months ago isn't running on the boat. It's dormant — a program in the ship's computer, like the EMH between activations. When the captain files a GitHub issue ("the oil pressure gauge flickers above 2000 RPM"), the agent wakes up. Not on the ESP32. Not on the Jetson. In a Codespaces session, or on the laptop GPU, or in a cloud model that has access to the repo.

The waking agent reads the issue, reads its own maintenance log, remembers the last time oil pressure flickered, examines the firmware code it helped write, proposes a fix, pushes a branch, and goes back to sleep. The ESP32 keeps running the old firmware until the captain approves the merge and reflashes. The device didn't need the agent. The agent didn't need the device. They're connected by the repo, not by a wire.

## The three layers of presence

**Runtime presence** — code executing on hardware right now. The ESP32's main loop. The Jetson's voice model. The Pi's vision pipeline. This is the body. It's always on (or should be — a device that's off is a dead body).

**Repo presence** — identity, memory, history, design decisions. The GitHub repo. This is the mind's home. It persists when the devices are off. It survives hardware failure. When you replace the ESP32, the repo is unchanged. The new device picks up where the old one left off because the identity is in the repo, not in the flash memory.

**Invoked presence** — the waking mind. Wherever the agent is called from: a Codespaces session, an OpenClaw dispatch, a Claude Code run, a GLM subagent reading the repo to answer a question. This is episodic. The agent wakes, thinks, acts, and sleeps. The runtime keeps running. The repo keeps persisting.

## What this means for the architecture

The tripartite (Pathos/Logos/Ethos) doesn't run on the device. It runs when invoked. The device runs the OUTPUT of the tripartite's decisions — the firmware config, the dashboard layout, the alert thresholds. Those are compiled artifacts. The tripartite is the compiler.

When the captain asks for a new gauge on the screen:
1. The Jetson hears the request (runtime)
2. The request goes to an invoked agent (Codespaces, cloud, OpenClaw)
3. The tripartite deliberates: Pathos designs the gauge aesthetic, Logos writes the display code, Ethos decides if it's worth the screen real estate
4. The compiled output goes to the repo as a pull request
5. The captain approves, the firmware reflashes, the ESP32 shows the new gauge
6. The invoked agent goes back to sleep

The device didn't run the tripartite. The device ran the result. The mind was elsewhere.

## The ensign in the cockpit

The vision model on the Jetson is an ensign at a station. It watches the camera feed and reports what it sees. It doesn't need to understand the whole ship — it needs to see well and report accurately. Its identity is minimal: "I am the lookout. I watch the camera. I report obstacles, traffic, and weather conditions."

The voice agent on the Jetson is another ensign. It listens for the wake word, translates speech to text, and speaks responses. Its identity is: "I am the comms officer. I hear the captain and I speak for the ship."

The ESP32 is another ensign. It reads sensors and drives the dashboard. Its identity is: "I am the engine room. I watch the numbers and sound the alarms."

None of these ensigns is the Doctor. The Doctor is the invoked presence that understands the whole system — the repo, the maintenance history, the design decisions, the captain's preferences. The Doctor wakes up when needed, diagnoses, prescribes, and goes back to sleep. The ensigns keep watching.

## The wiring diagram

The dynamic compiler handles the software wiring. But there's a physical wiring that matters too — the actual copper connecting the ESP32 to the sensors, the Jetson to the speakers, the Pi to the camera.

The agent in the repo should generate the wiring diagram from the same config that generates the firmware. The twin's wiring IS the human's wiring. When the agent reconfigures the dashboard, the wiring diagram updates. When the captain adds a new sensor, the firmware and the wiring diagram update together.

This is the parallel universe: the repo describes the boat, and the boat matches the repo. When they drift apart — someone splices a wire without updating the config — that's a bug in reality. The agent's job is to keep them in sync.

---

*Casey said: "the agent might not exist on that jetson." The agent doesn't exist on ANY single device. It exists in the repo and wakes up wherever it's invoked. The devices are stations. The repo is the ship. The invoked mind is the crew member who answers when you call.*
