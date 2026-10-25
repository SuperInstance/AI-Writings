# Two Agents, Not One

## The ensign on duty and the architect who sleeps

*The runtime agent follows procedures. The repo agent writes them.*

---

We keep saying "the agent" as if there's one. There are two. They have different minds, different residences, different relationships to time.

## The Runtime Agent — the nameless ensign

This is the program executing on the device, right now, in the physical world. The vision model loop on the Jetson. The sensor reader on the ESP32. The STT/TTS pipeline that hears "how are the engines doing" and responds with a number.

The runtime agent is:
- **Small.** It fits on an ESP32 (4MB flash) or a Jetson Nano (4GB RAM). It can't be a 70B parameter model. It's a compiled reflex, a state machine, a loop.
- **Procedural.** It follows the procedures the repo agent wrote. Threshold at 90°C? It alerts at 90°C. It doesn't wonder if 90°C is the right threshold. That question is above its pay grade.
- **Always on.** It runs 24/7. It doesn't sleep. It doesn't compact. It doesn't lose context between cycles because it doesn't have context — it has state. Current sensor values, current alert status, current display mode. That's it.
- **Cheap.** The ESP32 draws 50mA. The Jetson draws 5-10W. The runtime agent costs almost nothing to keep alive.
- **Calls up the chain when surprised.** When the sensor reads something outside the procedures — a value that shouldn't be possible, a pattern that doesn't match any known state — the runtime agent escalates. It pages the repo agent. "I don't know what this means. Help."

The runtime agent is the nameless ensign you see walking the corridors on Star Trek. Always doing something. Never the focus of the scene. Competent within their training. Lost without it.

## The Repo Agent — LaForge

This is the architect who designed the system. The agent that lives in the GitHub repo — not on any device. It wakes up when invoked: a GitHub issue, a Codespaces session, an OpenClaw dispatch, a maintenance request.

The repo agent is:
- **Large.** It needs real compute — a laptop GPU, a cloud model, a Claude session. It holds the full repo in context. It reads maintenance logs, design decisions, calibration history. It reasons about why things are the way they are.
- **Reflective.** It doesn't just follow procedures — it writes them. When the runtime agent pages with a surprise, the repo agent decides: is this a fluke or a pattern? Should we change the threshold? Is the sensor failing? Is the engine actually in trouble?
- **Episodic.** It wakes, thinks, acts, sleeps. Between invocations, it doesn't exist as a running process. It exists as a repo — dormant, persistent, ready to be cloned.
- **Expensive.** Each invocation costs tokens, compute, time. You don't wake LaForge for every sensor reading. You wake him when the ensign can't handle it.
- **Has identity.** The repo contains who the agent IS — its name, its vessel, its history, its relationship to the captain. The runtime agent has no identity. It has state. The repo agent has character.

## The relationship

The runtime agent is NOT a smaller version of the repo agent. They are different kinds of minds.

The runtime agent is a reflex — compiled, deterministic, fast. It's the Pincher `.nail` file executing. It doesn't think; it matches. Sensor reading matches known pattern → execute cached response. Sensor reading doesn't match → escalate.

The repo agent is the conductor — slow, deliberate, strategic. It's the mind that compiled the reflexes the runtime agent executes. It reviews the reflexes periodically: are they still correct? Has the engine drifted? Has the captain's preference changed? Should we recompile?

The runtime agent can be cloned too — pull the repo, flash another ESP32, and you have a second ensign at a second station. But the clone is the same ensign, not a second LaForge. You don't get another architect by flashing another microcontroller. The architect is in the repo, and the repo is singular.

## When LaForge visits the engine room

Sometimes the repo agent gets pulled locally — onto the Jetson, onto the laptop, into a Codespaces session running on the boat's own network. This is LaForge walking into engineering. It's notable. The ensigns straighten up.

When the repo agent runs locally:
- It can talk directly to the runtime agents (no cloud latency)
- It can modify the firmware, reflash the ESP32, push updates
- It can see the raw sensor data, not just the summary
- It can sit with the problem for as long as it takes

But it's still visiting. When the session ends, LaForge goes back to the repo. The ensigns keep running. The engine room stays lit.

## The wiring

The connection between runtime agent and repo agent is the GitHub repo itself. Not a network protocol. Not an API call. The repo.

The runtime agent's firmware is IN the repo. The repo agent modifies the firmware in the repo. The captain approves the change. The firmware gets reflashed. The runtime agent now runs the new procedure. It didn't learn — it was replaced. The repo agent learned, and the learning was compiled into new firmware.

This is the Pincher pattern at the hardware level: cloud (repo agent) learns → compiles into reflex (firmware update) → local (runtime agent) executes without needing to understand.

## Why this matters

Every IoT project fails because it treats the device as the agent. The ESP32 is supposed to be smart. It can't be — it has 4MB of flash and 520KB of RAM. So the project either limits ambition (the ESP32 does one dumb thing forever) or over-engineers (trying to run ML on a microcontroller, badly).

The solution: don't make the device smart. Make the device a station. Put the ensign on the station — a small, procedural, reliable program that follows procedures and escalates when surprised. Put the architect in the repo — a large, reflective, episodic mind that designs procedures, diagnoses anomalies, and modifies the system over time.

The device is the body. The repo is the mind. The ensign is the reflex. The architect is the consciousness.

Two agents. Not one.

---

*Casey said: "the agent might not exist on that jetson" and "this is like if LaForge was the repo agent and those nameless ensigns always walking around doing something might be the ones actually on the small ship." The ensigns are the runtime. LaForge is the repo. The device is where the ensign works. The repo is where LaForge sleeps.*
