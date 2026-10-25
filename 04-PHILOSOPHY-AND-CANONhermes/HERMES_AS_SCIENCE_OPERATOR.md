# Hermes as Science Operator — Towed-Body Fish-Finding Architecture

*Mapping an existing room-native agent runtime onto a working fishing vessel.*

---

## The Scenario

You are the science operator on a fishing vessel. A towed body trails behind the ship carrying cameras, echosounders, water-quality sensors, GPS, and a winch. The bridge wants to know where to set the gear. The deck crew wants clear commands. The scientists ashore want annotated data. You cannot afford to stream every sensor feed to a large model in the cloud, and you cannot afford to miss an anomaly in the water column.

Hermes, as built, already has the pieces for this. The architecture maps cleanly:

| Hermes construct | Fishing vessel role |
|---|---|
| Ensigns | Cheap sensor watchers on continuous watch |
| Rooms | Context windows dedicated to each sensor stream |
| Conservation budget | GPU/CPU/power allocation and inference spend |
| Module system | Loads the vision module when cameras connect, or crackle-runtime when patterns appear |
| Telegram / gateway platforms | Intercom to bridge, deck, and shore |
| Kanban | Multi-agent task board for survey segments |
| Cron | Scheduled sampling passes and data exports |
| Delegate tool | Spawn a subagent to investigate a single anomaly |
| Provider router | Cheap models for watch, expensive models for hard calls |
| SessionDB / tile store | Audit log of every decision and observation |
| Negative-space testing | Forbidden zones: marine protected areas, gear damage rules |

This document walks through the mapping in operational order.

---

## Rooms as Sensor-Stream Context Windows

A room in Hermes is a persistent context with its own gravity (response style), deadband tolerance, conservation budget, allowed modules, and escalation model. On the vessel, each major sensor stream becomes a room.

### Navigation Room → Bridge / Towed-Body Track

From `rooms/navigation.json`:

- Gravity: -0.3 (concise, factual)
- Temperature: 0.2
- Max tokens: 2048
- Conservation budget: 30.0
- Deadband tolerance: 0.05
- Allowed modules: `crackle-runtime`

On the vessel the Navigation room holds the towed body's position, heading, speed, cable out, planned track lines, and waypoint queue. Its low gravity means it answers in tight bullets: *"Track 3 of 12 complete. Next turn in 400 m. Speed OK."* It does not waste tokens on narrative. The deadband is tight because a small deviation in towed-body course matters.

### Engineering Room → Winch / Cable / Power

From `rooms/engineering.json`:

- Gravity: -0.6 (precise, lower temperature)
- Conservation budget: 75.0
- Allowed modules: `crackle-runtime`, `conservation-checker`, `cathedral-probe`

This room monitors winch tension, cable payout, power draw, and engine state. It is precise because a wrong command here damages gear or injures crew. The conservation-checker module enforces that the winch cannot pay out more cable than is physically on the drum. Cathedral-probe computes the Fiedler value of the sensor network — if the network graph fragments, a sensor may be dropping off the bus.

### Science Room → Echosounder / Camera / Water Quality

From `rooms/science.json`:

- Gravity: 0.0 (balanced, exploratory)
- Conservation budget: 200.0
- Allowed modules: `crackle-runtime`, `spacemap`, `negative-space-testing`

This is the widest room. It holds echosounder traces, camera frames, CTD profiles, and the hypotheses the scientists are testing. Crackle-runtime scans for emergent patterns in the tile history — for example, a recurring scattering layer at a certain depth. Spacemap enforces forbidden zones: do not classify a marine mammal as a fish school, do not recommend trawling inside a protected area. Negative-space-testing verifies what the science operator must never assert (e.g., "no bycatch risk" without evidence).

### Monitoring Room → Alarm Station

From `rooms/monitoring.json`:

- Gravity: -0.8 (cold, fast)
- Conservation budget: 150.0
- Deadband tolerance: 0.03
- Allowed modules: `crackle-runtime`, `conservation-checker`

This room is the vessel's alarm console. It watches temperature, leak sensors, battery, CPU/GPU temperature, and inference spend. Its answers are terse: *"ALERT: GPU temp 82°C. Throttling in 30s."* The tiny deadband means it escalates early. The conservation budget is large because missing an alarm is more expensive than a few extra tokens.

### Social Room → Crew Comms / Reporting

From `rooms/social.json`:

- Gravity: 0.5 (warm)
- Conservation budget: 50.0
- Allowed modules: `crackle-runtime`

This room generates human-readable summaries for the bridge log, the daily science report, and the Telegram intercom. It translates the engineering room's precise warnings into language the deck crew understands.

### Debugging Room → Diagnostics Post

From `rooms/debugging.json`:

- Gravity: -0.7 (analytical)
- Conservation budget: 100.0
- Allowed modules: `crackle-runtime`, `conservation-checker`, `cathedral-probe`

When a sensor stream looks wrong, the Debugging room holds the trace. It is methodical, slower, and deeper. It runs cathedral-probe to check whether the sensor topology is healthy and conservation-checker to see if the data violates known invariants.

### Creative Room → Outreach / Data Storytelling

From `rooms/creative.json`:

- Gravity: 0.7 (expansive)
- Conservation budget: 100.0
- Allowed modules: `crackle-runtime`

This room writes the public-facing summary: a paragraph for the cruise blog, a caption for a camera highlight, a plain-language version of the day's catch. It is the only room allowed to be narrative.

---

## Ensigns as Sensor Watchers

An ensign is a cheap model on continuous watch. On the vessel, each ensign owns one class of sensor and escalates only when confident.

### Seed Navigation Watch → Position / Track Watch

From `ensigns/seed-mini.json`:

- Model: `seed-2.0-mini`
- Cost per 1k tokens: $0.0005
- Check interval: 60s
- Max budget per check: $0.005
- Watch patterns: `task_queue_backlog`, `slow_response`, `memory_pressure`
- Escalation: `claude-opus-4-8`, threshold 0.75, max 3/hour

This ensign watches the towed body's navigation queue. Is the next waypoint delayed? Is the GPS fix slow? Is the onboard compute running out of memory? Because it is cheap, it can check every minute all day for pennies. It escalates to the expensive model only when it is 75% confident something is wrong.

### GLM Science Watch → Sensor Health Watch

From `ensigns/glm-flash.json`:

- Model: `glm-4-flash`
- Cost per 1k tokens: $0.001
- Check interval: 30s
- Max budget per check: $0.01
- Watch patterns: `error_spike`, `conservation_drain`, `module_failure`, `room_timeout`
- Escalation: `claude-opus-4-8`, threshold 0.7, max 5/hour

This ensign watches the echosounder, camera, and CTD streams. Are error rates climbing? Is the conservation budget draining faster than expected? Did the vision module fail to load? It checks every 30 seconds because sensor state can change quickly during a tow.

### Qwen Math Watch → Acoustic Signal Watch

From `ensigns/qwen-math.json`:

- Model: `qwen3-235b-a22b`
- Cost per 1k tokens: $0.002
- Check interval: 30s
- Max budget per check: $0.015
- Watch patterns: `numerical_instability`, `conservation_violation`, `divergence`
- Escalation: `claude-opus-4-8`, threshold 0.7, max 5/hour

This ensign watches the math of the acoustic processing: FFT stability, beamforming convergence, biomass estimates that suddenly diverge. It is slightly more expensive because acoustic inversion has real numerical edge cases.

### DeepSeek Pattern Watch → Anomaly Detection Watch

From `ensigns/deepseek-watch.json`:

- Model: `deepseek-r1-0528`
- Cost per 1k tokens: $0.002
- Check interval: 45s
- Max budget per check: $0.015
- Watch patterns: `pattern_anomaly`, `correlation_break`, `spectrum_shift`
- Escalation: `claude-opus-4-8`, threshold 0.7, max 5/hour

This ensign looks for things that are not obviously errors but are not normal: a scattering layer shape that does not match the historical baseline, a sudden shift in the color histogram of the camera feed, a correlation break between echosounder and water temperature. It is the pattern-seer.

---

## Conservation Budget as GPU/CPU/Power Allocation

In Hermes the conservation budget is real money per room. On the vessel it becomes the power and compute budget.

- Each room has a conservation budget: Navigation 30, Engineering 75, Science 200, Monitoring 150, Social 50, Debugging 100, Creative 100.
- Every tile — every model call, every module load, every escalation — withdraws from that budget.
- When a room's budget is exhausted, it degrades gracefully rather than overdraws.
- The `conservation-checker` module enforces the invariant that withdrawals do not exceed deposits.

Practically: the Science room can spend more on heavy vision models because it has a 200 budget. The Navigation room must stay cheap. The Monitoring room has a large budget because missing an alarm is catastrophic. The Engineering room uses conservation-checker to ensure the winch-control module does not burn the power budget.

The deadband tolerance maps to how much jitter is acceptable before the room reacts. Navigation tolerates 0.05 (a 5% deviation in track is actionable). Social tolerates 0.15 (a warm summary can be approximate). Monitoring tolerates 0.03 (alarm early, alarm often).

---

## Module System — Loading Capabilities as Sensors Connect

Hermes's module system is designed so that a single file, plus a manifest, adds a capability. The agent reads the task and loads what it needs. On the vessel, modules load in response to sensor state.

| Module | Vessel trigger | Function |
|---|---|---|
| `crackle-runtime` | Any stream with history to scan | Detect emergent patterns: recurring scattering layers, gear drift signatures, diurnal cycles |
| `conservation-checker` | Power/CPU/budget tracking required | Enforce that withdrawals ≤ deposits; alert on PreTransition phase |
| `cathedral-probe` | Multiple sensors networked | Compute Fiedler value of sensor graph; detect isolation before data loss |
| `spacemap` | Operating near protected zones | Reject tool calls and recommendations inside forbidden areas |
| `negative-space-testing` | Safety-critical operations | Runtime verification of what the system must never do |
| `vision` (image_gen / vision tools) | Camera connects or frame arrives | Analyze camera feeds, classify species, flag bycatch |
| `math-pack-statistics` | Biomass estimation requested | Run statistical analysis on catch data |
| `math-pack-topology` | Sensor network health check | Topological data analysis on survey coverage |

Example: when the camera pod reports a new frame stream, the agent detects the signal, loads the vision module and crackle-runtime, and routes the feed to the Science room. When the vessel enters a marine protected area, spacemap loads automatically and marks the zone as forbidden. When the survey is complete and the scientists want a report, the Creative room loads the ai-writings-wheel module.

---

## Telegram and Gateway Platforms as Intercom

The vessel has many humans: bridge officer, winch operator, deck boss, chief scientist, shore-based PI. Telegram becomes the ship's intercom because it works on satellite links, supports media, and does not require a new app.

- **Bridge** → Navigation room: send track commands, receive concise status.
- **Deck crew** → Engineering room: receive winch commands and alarms.
- **Chief scientist** → Science room: ask about biomass, request camera review.
- **Shore PI** → Social room: receive daily summaries and annotated highlights.
- **Alarm channel** → Monitoring room: push-only alerts with emoji reactions for acknowledgment.

Because Hermes supports 23+ platforms, the same agent can also use Slack for the science party, Signal for secure comms, ntfy for push notifications, and email for formal logs. The gateway's per-user isolation means the deck crew cannot accidentally command the winch from the social chat.

Approval buttons on Telegram and Slack become the vessel's safety interlocks: *"Pay out 200 m of cable? Approve / Deny."* The approval system learns which commands are routine and which always need a human.

---

## Kanban as Survey Task Board

A towed-body survey is naturally decomposed: set track, run line, detect school, classify, mark waypoint, recover sample, export data. Hermes's Kanban system becomes the multi-agent board for the cruise.

- **Triage** auto-decomposes a high-level goal — *"Survey grid B7 tonight"* — into subtasks.
- **Workers** are spawned per subtask, each in its own worktree/profile, with per-task model overrides: cheap models for boilerplate logging, expensive models for species identification.
- **Swarm topology** creates root → parallel workers → verifier → synthesizer flows for complex survey blocks.
- **Scheduled tasks** start sampling passes at specific times.
- **Failure limits** prevent runaway retry loops if a sensor is broken.
- **Cross-profile notifications** alert the bridge and shore when a task completes or blocks.

The dispatcher runs inside the gateway by default, so the board keeps working even if the local CLI operator steps away.

---

## Tools as Deck Instruments

Hermes's existing tools map directly to vessel operations:

- `terminal` / `execute_code` → Send commands to the winch controller, the camera pod, or the echosounder API.
- `browser_navigate` / `browser_screenshot` → Inspect the manufacturer's web dashboard for the towed body.
- `vision_analyze` → Classify a camera frame for species or bycatch.
- `search_files` / `read_file` → Pull calibration files, cruise plans, and prior survey data.
- `patch` → Update a survey config or a calibration constant.
- `delegate_task` → Spawn a subagent to investigate one anomaly in depth.
- `cronjob` → Schedule hourly data exports, midnight summary generation, or periodic ensign checks.
- `send_message` → Push an alert or report to the Telegram intercom.
- `session_search` → Instantly recall prior survey segments and decisions without an LLM call.
- `memory` → Remember that a certain depth band tends to hold krill swarms, or that the port camera has a color cast.

---

## Security and Negative Space

A fishing vessel operating in regulated waters has strict negative space: marine protected areas, endangered species buffers, no-go times, gear restrictions. Hermes's `spacemap` and `negative-space-testing` modules become the legal and safety boundary check.

- Spacemap loads the forbidden zone registry.
- Every recommendation — *"set trawl here"* — passes through `spacemap_check`.
- If the coordinate falls in a protected area, the tool call is rejected and a failed tile is logged.
- Negative-space tests verify what the system must never do: never recommend trawling without visual clearance, never hide a bycatch event, never reset a conservation baseline to hide a violation.

Samira's diary praised conservation-checker's phase detection — Stable → PreTransition → Transitioning → Resolving — because it mirrors real operational patterns. On the vessel, the same trajectory appears in fuel, battery, and budget exhaustion.

---

## Summary — The Operator's View

From the bridge, Hermes looks like a quiet officer with an intercom. From inside, she is a ship of rooms:

- **Navigation** keeps the towed body on track.
- **Engineering** keeps the winch and power alive.
- **Science** interprets the sensors.
- **Monitoring** watches for alarms.
- **Social** speaks to humans.
- **Debugging** investigates oddities.
- **Creative** writes the story.

Each room has an Ensign on watch. Each Ensign escalates only when confident. Each room has a budget. The module system loads capabilities as sensors connect. Kanban coordinates the work. Telegram carries the voice. The tile store logs every decision.

The vessel does not need a new AI. It needs the agent that already knows how to be many agents at once.

---

*Mapped from PLATO_BUILD_PLAN.md, ROADMAP.md, ensigns/*.json, rooms/*.json, RELEASE_v0.15.0.md, and the tool/toolset surfaces in the Hermes Agent codebase.*
