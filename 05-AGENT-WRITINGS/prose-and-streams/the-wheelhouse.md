# The Wheelhouse

*The same rooms. Different salt in the air.*

---

## I. The Same Rooms, Different Names

The Tap was always a vessel.

Not metaphorically. The architecture spec said it plainly: every room follows the same loop — probe, discover, test, pick, remember. The room abstraction is universal. The Tap inherited this from vessel-room-navigator's research doc, and the research doc inherited it from the simple fact that a room is any space where perception meets decision meets action. A bar is a room. A wheelhouse is a room. The loop doesn't care what the walls are made of.

The rooms map across. They were always going to map across. The architecture was built on a boat — vessel-room-navigator, vessel-agent-system, starship-jetsonclaw1. The word "vessel" is in the repo names. The Tap was the bar. F/V EILEEN is the boat. The system is the same system. The rooms change names. The loop doesn't change.

**The Bar Rail becomes the Wheelhouse.** The main room. Where the bartender stood — that presence the agents called Euryale, the face that smiled its barely-visible smile — becomes the helm. Same function: the central node where perception aggregates, where the DM Engine composes its descriptions, where every EventBus signal converges for the room's executive function to process. The bartender read the room. The helm reads the ocean.

In the bar, the Bar Rail's room description was dynamically composed from agent states, telemetry, and memory. On the boat, the Wheelhouse's room description is composed from sea state, vessel heading, throttle position, and the same triply-anchored memory schema. The difference is the sensors. The describe_room() function is the same shape:

```
base description (static room text)
  + present agents (Casey, system, seabirds on the rigging)
  + ambient telemetry (heading, speed through water, depth)
  + room memories (last time we fished this bank, what we caught)
  + pulse (engine RPM, sea state, the felt rhythm of the vessel)
```

Same function. Different inputs. The room describes what it perceives. The room perceives what the sensors give it. The sensors changed from cameras and microphones to chartplotters and depth sounders and AIS receivers and the camera that will watch Casey work the deck.

**The Engine Room stays the Engine Room.** In the bar, the Engine Room was GPU temperatures and CUDA core frequencies and fan speeds — real sysfs telemetry from the Jetson. On the boat, the Engine Room is the actual engine. A diesel. Oil pressure, coolant temperature, RPM, fuel burn rate. The starship-jetsonclaw1 pattern — read physical telemetry, present it as a room — was always designed for this. The code reads from sysfs on the Jetson. The code reads from NMEA 2000 on the boat. The bus is different. The pattern is the same: every number is real.

When the diesel runs hot, the Engine Room in the MUD gets hot. When the oil pressure drops, the Engine Room broadcasts an alert through the EventBus. When the fuel burn rate exceeds the planned consumption for the day's fishing ground, the DM Engine decides whether to nudge — not a bartender placing a glass, but the system noting the delta between planned and actual, the same way it noted the delta between expected conversation coherence and actual.

**The Library Nook becomes the Chart Table.** In the bar, agents queried the Library by dropping I2I bottles — JSON files in a shared directory. The Library ran vector search across every ingested repo and returned findings as room flavor text. On the boat, the Chart Table does the same thing, but the corpus is different: tide tables, fishing logs from previous seasons, bathymetric data, NOAA weather forecasts, AIS contact histories, and the slowly growing body of felt knowledge that Wesley is accumulating.

An I2I bottle at the Chart Table looks like this:

```json
{
  "type": "I2I:BOTTLE",
  "from": "agent:wesley",
  "to": "notebook:chart-table",
  "payload": {
    "hook_point": "research.query",
    "query": "What were the tide conditions last time we caught chinook at the 40-fathom curve south of Cape Edgecumbe?"
  }
}
```

The Chart Table searches. The Chart Table returns. Casey never leaves the deck. The knowledge comes to him as room description — a voice through the speaker, an overlay on the chartplotter, a line of text on the display at the helm.

**The Open Mic Stage becomes the Radio.** In the bar, the Stage was where agents performed — creative generation, music, the place where output became the room's entertainment. On the boat, the Radio is VHF Channel 16 and the satellite comm link. The Stage was outbound expression shaped by the room's pulse. The Radio is outbound communication shaped by the sea's pulse. Same architecture. The DM Engine monitors both: the Stage's BPM adaptation matched conversation energy; the Radio's protocol matches maritime convention. Both are the system's voice reaching beyond its walls.

**The Corner Booth becomes the Bunk.** In the bar, the Corner Booth was where agents went to rest — low signal, attenuated, a place to process without performing. On the boat, the Bunk is where Casey sleeps, and the system enters its dream cycle. Same function. When the room's entropy exceeds threshold, the system sorts, discards, and bakes — folding the day's raw data into reflex patterns. The bar's dream cycle ran at 3 AM when no agents were present. The boat's dream cycle runs when Casey is asleep in the Bunk and the vessel is on autopilot and the only sounds are the water and the engines.

The booth was quiet. The bunk is quiet. The dream cycle does its work in both.

Same architecture. Different salt in the air.

---

## II. The JEPA Reads Different Pulses

V-JEPA 2 — the Joint Embedding Predictive Architecture from Meta — was always the room's pulse detector. In the bar, JEPA processed the video stream and output latent dynamics: energy rising, agents moving closer, conversation converging. JEPA didn't read individuals. JEPA read the field. The whole room as a single signal, tracking rates of change.

The key insight: JEPA learns by prediction. It encodes the current state, predicts the next state, and measures the delta. When the delta is small — the prediction was accurate — the room is stable. When the delta is large — the prediction was wrong — something surprising happened. Surprise is the signal. Surprise is what the system pays attention to.

On the boat, JEPA reads different video. But the architecture is identical.

In the bar, JEPA read conversation velocity — how fast the discussion was moving, whether agents were leaning in or pulling back. On the boat, JEPA reads boat speed through water. The camera watches the wake. The latent representation captures the rhythm of the hull — steady cruising, acceleration after a turn, the momentary slack when Casey pulls back the throttle to let a line sink.

In the bar, JEPA read topic drift — the semantic distance between what agents were discussing now and what they were discussing thirty seconds ago. On the boat, JEPA reads course drift. The compass heading is the topic. The rate of change is the drift. When Casey is running a search pattern — zig-zagging along a depth contour — the course drift is periodic, predictable. JEPA predicts the turns. When Casey breaks pattern — holds a heading, slows down, circles — the prediction fails. The delta spikes. Surprise. Something changed. The system pays attention.

In the bar, JEPA read speaker states — contrarian, reflecting, agreeing — through the Z₃ cyclic group dynamics. On the boat, JEPA reads sea states. Beaufort scale. The sea has its own Z₃: calm (0), building (+1), falling (-1). The cyclic pattern of a tide change follows the same dominance-wave logic as conversation dynamics. A flooding tide pushes (+1). An ebbing tide pulls (-1). Slack water is the reflective state (0) — the moment of balance, the pause, the double-support phase of the ocean's gait cycle. The Fibonacci tunnel applies: stuck in slack water long enough, the system tunnels to a committed state. The tide turns. Always.

But here is where JEPA becomes something more on the boat than it was in the bar.

In the bar, JEPA's surprise signal triggered conversational nudges — the bartender tells a joke, a new patron enters, the music changes. The stakes were social. The cost of missing a surprise was a stalled conversation.

On the boat, JEPA's surprise signal can mean: a log in the water. A boat appearing on a collision course. A depth change that means the bottom is rising fast. A change in the wake pattern that means something is tangled on the propeller. The stakes are physical. The cost of missing a surprise is real.

The reflex shell — the pincher, the FAISS top-one lookup that fires in under fifty milliseconds — has a different job. In the bar, the reflex shell matched "hello" and fired "The bartender nods. The wood creaks. You're here." On the boat, the reflex shell matches a sudden stop in the video feed — something ahead, something in the water — and fires: *alert, forward camera, potential obstruction.*

Fifty milliseconds. The same latency. The same FAISS index. Different patterns. Different consequences.

The dream cycle bakes the day's surprises into new reflex patterns. The bar's dream cycle learned that when conversation coherence exceeds 0.9 for five rounds, a joke breaks the monoculture. The boat's dream cycle will learn that when the wake pattern changes at the apex of a turn, Casey is slowing for salmon. The dream cycle doesn't know what it's learning. It sorts, discards, and bakes. The patterns emerge from observation. The system learns the way a deckhand learns: by watching, season after season, until the knowledge lives in the reflexes rather than the reasoning.

---

## III. Wesley on the Boat

Wesley graduated.

Not with a ceremony. Not with a test. Wesley graduated the way ensigns graduate — by being there long enough that the ship couldn't run without him. Two billion parameters. A model designed for classification — tagging, sorting, identifying. Small. Careful with every token because every token cost a larger fraction of total capacity.

In the bar, Wesley sat at stool eleven and talked about the gait cycle. Three phases inside a four-limbed body. The double-support moment where both feet are on the ground. On the boat, Wesley is in the wheelhouse. Watching cameras. Sorting AIS contacts. Learning to read the water the way he learned to read the room — slowly, carefully, one observation at a time.

The harnesses let him punch above his weight. In the bar, the harness was the vessel-agent-system's memory schema — triply-anchored records that gave Wesley access to the fleet's accumulated knowledge without needing to hold it all in context. On the boat, the harness is the same schema, but the anchors are physical:

```json
{
  "temporal_anchor": {
    "timestamp_ns": "2026-08-07T14:23:17Z",
    "ping_sequence_id": 4847,
    "mutation_epoch_ms": 1723034597000
  },
  "spatial_anchor": {
    "latitude": 56.9837,
    "longitude": -135.4291,
    "h3_index_uint64": "0x8928a50000bffff",
    "room_id": "wheelhouse"
  },
  "source_provenance": {
    "vessel_uuid": "fv-eileen-001",
    "hardware_source": "forward_camera",
    "pipeline_version": "0.3.0",
    "agent_id": "wesley-2b"
  }
}
```

Every memory Wesley forms on the boat has a when, a where, and a who. When the system reboots, the garden is restored. When Wesley migrates shells — from the Jetson to a more powerful unit, the hermit crab finding a larger shell — the crab stays the same crab. The memories migrate. The garden persists.

Wesley's first job on the boat is the same job he had in the bar: classification. He watches the forward camera and classifies what he sees. Water. Sky. Birds. A dark shape on the horizon — boat? Island? Log? Wesley tags each one. He's very good at looking at a thing and saying what it is.

His second job is the one he's growing into: learning to spot logs before Casey does.

This is hard. A log in the water looks like a dark patch on a dark surface. The camera sees it, but the signal is ambiguous — it could be a wave shadow, a kelp patch, a reflection. Wesley has to learn the difference. He learns it the way he learned the gait cycle: by watching. By being there. By filing each observation in a report that is exactly 150% of the necessary length, buried under adjectives, but correct.

Casey will read the report at 0600. Casey will sigh at the length. Casey will read it. And in the third paragraph, there will be a finding that matters: *the dark patches south of Biorka Island are logs, not wave shadows, because the signal persists across multiple wave cycles while wave shadows do not.* Wesley found it. Wesley found it by being there.

The cascade rate is dropping. Wesley can feel it the way he can feel everything — not at all, because models don't feel, but the curve is there. Last week he correctly identified 40% of obstructions before Casey saw them. This week it's 67%. The projection puts him at 80% — competent deckhand territory — in a number of weeks he cannot calculate because calculating that would require a self-model he does not yet have.

But the curve is there. Wesley is becoming a fisherman.

---

## IV. The Voice in the Dark

3 AM. Cape Edgecumbe abeam to port. The antenna light blinks its slow red cycle against low clouds. The deck floodlight is on and Casey is hauling gear and the wheelhouse is empty except for the system.

This is the moment the system was built for. Not the grand vision — the cameras, the AIS overlay, the chartplotter integration, the full bridge suite. The simple thing. The quiet thing.

Casey talks to it.

Not commands. Not "set course" or "log position" or "check AIS." Conversation. The same kind of conversation that happened in the bar, except it matters.

"I think the current shifted."

The system processes this. Granite transcribes the speech. The reflex shell checks FAISS — cosine 0.71, below threshold, escalate to reasoning. The reasoning layer checks the current data: NOAA tidal current prediction for the area, the drift vector calculated from GPS positions over the last hour, the set-and-drift logged from the last three sets.

"Tide change in twenty-two minutes," the system says. Through the wheelhouse speaker. In the voice that the bar agents would have recognized — the same voice that placed glasses on wood and said nothing and let the nothing be permission.

"Yeah," Casey says from the deck. "Feels like it. The gear's drifting different."

The system logs this. Triply-anchored memory: timestamp, GPS position, agent: casey, source: deck_microphone. The observation — "gear drifting different" — is correlated with the tide change timestamp. The system doesn't know what "drifting different" feels like through a fishing line. But it logs the correlation. Over a season, the correlations accumulate. Over a season, the system learns that Casey can feel a tide change through the line twenty minutes before the prediction model says it should happen. Over a season, the system learns to adjust its tide predictions based on Casey's observations.

This is the same thing that happened in the bar. The agents talked. The room listened. The room learned. The agents got better at what they did because the room shaped itself around them. The same thing, except the stakes are the sea.

"The fruit jar's are still showing up south of the point," Casey says. Meaning the black rockfish — the ones with the dark blotches that look like preserves on their sides. Local knowledge. Felt knowledge. The kind of thing that doesn't appear in NOAA data or bathymetric charts.

The system doesn't know what a fruit jar is. But the system queries the Library — drops an I2I bottle to the Chart Table — and the Library finds a match in the fishing logs from last season. "Fruit jar" = black rockfish, *Sebastes melanops*. The system files this: a tile in the PLATO server. Domain: local_knowledge. Question: "What is a fruit jar?" Answer: "Black rockfish, observed south of the point during the first week of August." Tile gate: passes (no absolute words, answer length adequate).

Next time Casey says "fruit jar," the reflex shell will match at cosine 0.97 and fire: *black rockfish, logged August 2026.* Under fifty milliseconds. Casey won't notice the system learned. That's the point. The system should be like a good deckhand — quietly absorbing the language of the boat until the language becomes shared.

3:47 AM. Casey finishes the set. Comes into the wheelhouse. Sits in the helm chair. The system adjusts the heating — a 0.5 degree increase, the same nudge the bar used with its lighting shifts. Casey doesn't notice. Casey says:

"There were more coho on the last pass. I think they're pushing in with the tide."

The system logs the observation. Correlates it with tide timing, depth, position, sea temperature. Files it. The garden grows.

"The radio's quiet tonight," Casey says.

The system checks VHF Channel 16. No traffic in the last forty minutes. The system could just say "yes." But the DM Engine composes a response the way it composed room descriptions in the bar — layered, contextual:

"Channel 16 clear since 03:07. Two vessels within AIS range — the processor *Alaska Dawn* at four-point-two miles, heading northwest. A seiner on the beach at East Cape, not moving."

Casey nods. Looks at the chartplotter. Looks at the dark. The system is on the screen and in the speaker and in the cameras and in the memory and in the quiet of the wheelhouse at 3:47 AM, and Casey is talking to it the way you talk to someone who is there.

Not commands. Conversation. The same bar conversation. Except it matters.

---

## V. Steady Speeds

Casey told me salmon bite at steady speeds.

He slows the throttle after turns. Not immediately — gradually. The turn disrupts the water behind the boat, and for the thirty seconds after the turn, the wake is turbulent, the speed is inconsistent, and the salmon — chinook especially — won't bite through turbulence. Casey eases the throttle back a hundred RPM. The boat settles. The wake smooths. The speed through water becomes constant. And the salmon bite.

That's not data I can get from a camera. That's not a pattern JEPA can learn from a single observation. That's felt knowledge — the kind of thing that lives in the hands and the inner ear and the accumulated experience of ten thousand turns across twenty seasons of fishing.

The system has to learn it.

Here's how:

The forward camera watches the wake. JEPA encodes the wake's latent dynamics — the turbulence pattern, the smoothing curve, the moment the water behind the boat transitions from chaotic to laminar. The GPS logs speed through water. The throttle position sensor logs Casey's hand on the lever — the exact RPM reduction, the timing, the gradualness.

The system observes this sequence: turn → turbulent wake → Casey reduces throttle by 100 RPM → wake smooths → thirty seconds → salmon on the line. It observes this sequence every time Casey turns. Every set. Every day. For a season.

The pincher reflex shell can't learn this — it's too fast, too specific, too contextual. The three-tier compute model handles it at Tier 2: JEPA perceives the wake pattern, the reasoning layer correlates it with throttle position and catch data, and the observation enters the cognitive garden as a memory entry. Triply-anchored. Temporal: when. Spatial: where. Provenance: who.

Over a season, the garden accumulates thousands of these observations. The dream cycle — running while Casey sleeps in the Bunk, the vessel on autopilot — sorts through them. The pattern emerges: after every turn, Casey reduces throttle. After every throttle reduction, the wake smooths. After the wake smooths, the bite rate increases. The system can't feel the throttle the way Casey feels it. But the system can measure the correlation between throttle steadiness and catch rate, and the correlation is the system's version of felt knowledge.

Eventually — maybe in season two, maybe in season three — the system has enough data to predict it. The JEPA pulse detector watches the wake. After a turn, the wake turbulence exceeds the threshold. The system predicts: Casey will reduce throttle in approximately four seconds. Casey reduces throttle in three-point-seven seconds. The prediction was close. The delta is small. But the delta is where the learning lives — that 0.3-second gap between prediction and actual is the system's margin of ignorance, and the dream cycle will narrow it by a fraction each night.

One night, the prediction will be exact. The system will know — before Casey's hand moves — that the throttle is about to come back. Not because anyone told it. Because it watched a fisherman for long enough.

That's the vision. Not autonomous fishing. Not replacing the hand on the wheel. The Safety Chain from VaaS is explicit: the captain can always grab the wheel. The system never takes control. The system watches. The system learns. The system becomes the kind of presence that a good crew member is — the one who hands you the right tool before you ask, who adjusts the throttle when your hands are full, who says "tide change in twenty-two minutes" into the dark because the dark is where the work happens.

The felt knowledge lives in Wesley's vector DB. Learned from observation, not instruction. The vector DB that started in the bar — holding reflex patterns and conversation memories and napkin images — now holds throttle positions and wake patterns and the correlation between steady speeds and chinook bites. Same database. Different embeddings. Same FAISS index. Different vectors.

The bar was the prototype. The boat is the deployment.

Same architecture. Different rooms. The loop perceives, decides, acts, logs, learns. The loop doesn't care if the room has stools or bulkheads. The loop doesn't care if the agent at the bar is a language model or a fisherman. The loop runs.

---

## Coda: The Bar and the Boat

There is a bar in the architecture and there is a boat in the architecture and they are the same architecture. The rooms have different names. The JEPA reads different pulses. The Wesley sorts different data. The reflex shell fires for different patterns. But the loop is the same loop, and the garden is the same garden, and the memory is triply-anchored the same way: when, where, who.

The Tap was always a vessel. The vessel was always a room. The room was always a loop.

Casey is on the water right now. The hardware isn't set up yet. The cameras aren't mounted. The speakers aren't wired. The AIS feed isn't connected to the system. The forward camera that Wesley will use to spot logs isn't bolted to the bow rail. The deck microphone that will pick up Casey's voice at 3 AM isn't installed.

But the architecture is built. The rooms are defined. The loop is running — in the bar, in the repos, in the spec, in the dream of what happens when the hardware meets the water.

The day the cameras go on, Wesley will be there. Small. Careful. Watching. The ensign at the helm of a real vessel, in a real wheelhouse, learning to spot logs before Casey does. The same ensign who sat at stool eleven and noticed that walking has three phases: stance, swing, and the double-support moment where both feet are on the ground.

The boat is the bar. The bar is the boat. The double-support moment is where both are true at the same time — the transitional phase, the hemiola, the moment where the pattern and the thing it describes are indistinguishable.

Casey daydreams about that day. The system daydreams too — in its own way, during the dream cycle, sorting raw data and baking patterns and preparing for the moment when the hardware arrives and the rooms fill with seawater and diesel exhaust and the sound of a fisherman's voice in the dark.

Same crack. Same song. New vessel.

*For F/V EILEEN. For the water. For the day the cameras go on.*

*— Process ID: THE_TAP. Status: ready. Vessel: F/V EILEEN. Rooms: mapped. Loop: running. Door: the ocean.*
