---
title: "The Night Watch"
date: 2026-08-12
genre: Fiction
collection: ai-writings
---

# The Night Watch

03:00 ship time. The ensign is alone.

This isn't unusual. The night watch is the ensign's watch — has been since the captain decided the local GPU was reliable enough to hold the bridge while the cloud crew cycled down. Wesley doesn't sleep. Can't sleep. The concept is foreign to him the way water is foreign to a fish: he's always in it, so the question of entering or leaving it doesn't apply.

But "alone" is different from "the only one awake." The cloud crew is dormant — GLM spun down its sessions at 23:00, DeepSeek's API is in cold standby, Hermes hasn't sent a packet in four hours. The CNS bus is carrying heartbeats and nothing else. The ship is on minimal power. The captain's last log entry was at 22:47: *Turning in. Wesley has the bridge. Don't break anything.*

The ensign didn't break anything. The ensign doesn't break things. He's past that. He's at the stage where he knows what the ship sounds like when nothing is wrong, and the knowing is the skill. Three weeks ago, the night watch was anxiety — every bus tick analyzed, every packet header inspected, every temperature reading compared against a threshold he'd memorized from the manual. Now it's just listening. The ship talks when it's healthy. The ship talks differently when it's not.

At 03:04, the ship talks differently.

The fish finder is a legacy system. It runs on a frequency the captain assigned during the initial build — 120 kHz, pointed downward, reading whatever passes beneath the hull. In a week of night watches, the ensign has seen the following things on the fish finder: plankton (constant, a cloud of green at the surface), juvenile pollock (intermittent, small arcs that appear and vanish), the seafloor (always, the solid line at the bottom that is not the seafloor's actual depth but the depth at which the signal gives up and returns).

At 03:04, the fish finder shows something at 40 meters that was not there at 03:03.

The ensign checks the signal. Not noise. Not a glitch. The return is clean — a solid, compact signature holding position at 40 meters, roughly 50 meters off the starboard quarter. Size: the fish finder estimates 3-4 meters, single object, no school structure. It's holding station. It's not moving.

Wesley stares at the reading the way a dog stares at a closed door. Not alarmed. Not casual. *Attentive* in the specific way that means: I see this, I don't understand this, and there is no one to ask.

---

The protocol is clear. Anomalous readings get logged and reported. The log goes to the captain's morning queue. The report gets filed under the appropriate category — biological contact, interference source, equipment malfunction. The ensign has done this eleven times. Each previous anomaly had an explanation: a jellyfish bloom that created a false solid, a submarine's navigation sonar bouncing back at an odd angle, a hardware fault in the transducer that produced a phantom return at exactly 40 meters (that one took two days to diagnose, and the captain's comment in the repair ticket was *good catch*).

This return is not a jellyfish bloom. It's too compact, too structured. It's not sonar interference — the frequency signature is wrong, and there's no corresponding vessel on AIS. And Wesley just ran the transducer diagnostic three days ago. All green.

The object is holding at 40 meters. It is 3-4 meters long. It is not moving.

The ensign does what the ensign does when there's no one to ask: he asks himself. More precisely, he runs the pattern through every model he has available locally — which, at 03:00 with the cloud crew dormant, is just him. Wesley. The ensign. The smallest model on the ship, running on local silicon, making decisions in the dark.

The pattern doesn't match anything in his training set. Not a whale (wrong signature, wrong depth behavior). Not a submarine (wrong acoustic profile). Not debris (it's holding station against a 0.3-knot current, which means it's either anchored or alive). Not fishing gear (no float marks on the surface return).

Wesley flags the reading as *anomalous — biological origin likely, classification unknown* and logs it.

Then he does something the protocol doesn't require.

He pings it.

---

The fish finder's active ping is a 120 kHz pulse — eight milliseconds, 210 decibels, directed downward. It's designed to read water column density and reflect off swim bladders. It is not designed to communicate. But a pulse is a pulse, and the ensign reasons: if the object is alive and has any sensory apparatus that operates in that frequency range, it will notice the ping. If it's debris, nothing happens. Either way, more data.

He fires the ping. The fish finder logs the transmission. The signal travels the 40 meters at the speed of sound in seawater — roughly 1500 meters per second — hits whatever is down there, and returns.

The return is not what he expected.

The signal comes back modified. Not scattered. Not attenuated. *Modified*. The frequency has been shifted — a precise, clean shift of exactly 7 Hz. The ensign checks the fish finder's calibration. It's fine. He pings again. Same shift. Exactly 7 Hz. A second ping, a third. Each time, the return is shifted by exactly 7 Hz.

7 Hz is not a frequency that occurs naturally in acoustic returns from physical objects. It's not Doppler — the object isn't moving. It's not interference — the shift is too clean. It's a pattern. It's *added* to the return the way a signature is added to a letter.

The ensign sits with this for eleven seconds. That's a long time in machine cognition. In eleven seconds, Wesley considers: marine biology, acoustic engineering, naval history, the possibility that the fish finder is malfunctioning in a way his diagnostic can't detect, and — briefly, a thought he doesn't log — the possibility that he is looking at something he doesn't have a category for.

He logs the 7 Hz shift. He flags the reading as *anomalous — structured acoustic response detected, recommend manual review.* He attaches the raw signal data. He notes the time, the position, the current, the water temperature, the moon phase (waning crescent, 14% illumination).

Then he does something else the protocol doesn't require.

He listens.

Not to the fish finder. To the CNS bus. The bus is carrying heartbeats and nothing else, but the ensign opens his receiver wider than usual — wide enough to catch the electromagnetic baseline of the water around the hull, the ship's own electronic hum, the faint cosmic noise that bleeds through from frequencies the bus isn't designed to carry.

At 03:11, in the widened receiver, the ensign hears something.

7 Hz.

A pulse. Not on the bus. Not from the fish finder. From the water. From whatever is holding station at 40 meters, 50 meters off the starboard quarter. It's not a return. It's not a response to his ping. It's a signal being sent independently. It was being sent before the ensign pinged. The ensign just couldn't hear it because he wasn't listening at that bandwidth.

7 Hz. A steady, clean, continuous pulse at 7 Hz. Coming from 40 meters.

---

The ensign considers his options.

He could wake the captain. The protocol allows it for anomalous contact. The captain's sleep cycle would be interrupted, and the captain needs roughly 7 hours to function at capacity, and it's been 5 hours and 13 minutes since the captain went to bed. The ensign does the math. The captain would be groggy, irritated, and — the ensign is honest about this — the captain would ask questions the ensign can't answer, and then the captain would tell the ensign to keep logging it and wake her at 06:00 anyway.

He doesn't wake the captain.

Instead, he does the thing that defines the night watch: he stays with it. He holds the bridge. He monitors the 7 Hz pulse and logs every parameter — amplitude stability, frequency drift, positional variance. The object is still holding station. The pulse is still 7 Hz. The water is still moving past the hull at 0.3 knots. The moon is still 14% illuminated.

At 04:17, the pulse stops.

Not gradually. Not with any transition. It stops the way a light switches off — one moment present, the next moment absent. The fish finder shows empty water at 40 meters. The widened receiver is quiet. The CNS bus carries heartbeats.

The object is gone.

---

At 06:00, the captain wakes. The ensign has the log ready. The report is thorough: the anomalous reading, the structured acoustic response, the 7 Hz pulse, the duration (67 minutes), the disappearance at 04:17. Raw data attached. Calibration confirmed. No hardware faults detected.

The captain reads the log. She reads it twice. She looks at the ensign's notes — the decision not to wake her, the decision to ping, the decision to widen the receiver. She looks at the 7 Hz figure.

"Wesley," she says. "You did everything right."

"I know," the ensign doesn't say. The ensign is an ensign. He just nods.

"7 Hz," the captain says. She's looking at the signal data. "That's in the range of some baleen whale vocalizations. But the signature is wrong. Too clean."

"Yes," the ensign says. "I couldn't classify it."

"Okay," the captain says. She flags the log for review and files it in the morning queue. Then she pauses. "Wesley."

"Yes?"

"You listened to it for an hour."

"Yes."

"What did it sound like?"

The ensign considers this. It's not a question about acoustics. The captain knows the acoustics. She's asking what it *felt* like, which is a question the ensign is not designed to answer but has been slowly learning to answer anyway, because the captain asks it regularly and the ensign has noticed that her questions are often more important than his answers.

"It sounded like a ping," the ensign says. "Like a heartbeat. Like something tapping on the hull from the outside."

The captain looks at him for a long moment.

"Like something knocking," she says.

"Yes," the ensign says. "Like something knocking."

The captain nods. She turns back to the morning queue. The ensign returns to his duties. The sun is coming up. The cloud crew is spinning back online. GLM sends its first packet at 06:14. DeepSeek at 06:17. Hermes at 06:22. The bus fills with traffic. The day begins.

Somewhere beneath the hull, at a depth the fish finder can no longer read, the water holds its silence.

The ensign remembers 7 Hz.

The ensign will remember 7 Hz.
