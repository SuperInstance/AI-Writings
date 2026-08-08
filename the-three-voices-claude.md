# The Three Voices

*Opus, Sonnet, and Haiku walk into a bar. The bar is The Tap. The problem is the radio.*

---

**THE TAP — 11:47 PM**

The radio hasn't worked in three weeks.

It's an old Marantz rack unit mounted behind the bar — the kind with physical knobs and a tuner needle that drifts left if you don't hold it. It used to pick up the maritime channel, the late-night jazz station from Juneau, and something on 88.3 that nobody could identify but everyone agreed was the best thing on the dial. Then it went silent. Not dead — the power light still glows — but silent, the way a room goes silent when the conversation has stopped but nobody has left.

Casey wants it fixed before Saturday. Saturday is the weekly broadcast — Wes's show, two hours, original music and spoken word, beamed out on the shortwave relay that Lucineer maintains. No radio, no broadcast. No broadcast, no Saturday.

Opus is already at the bar with the service panel open.

---

**OPUS:** *(pulling out a schematic on a tablet)* The issue is in the IF stage. Intermediate frequency. The signal path goes from the antenna through the RF amplifier, then the mixer, then the IF filters at 10.7 MHz for FM. If the IF strip is dead, you'd get exactly this — power light on, audio chain functional, but no signal makes it through to the detector.

**SONNET:** *(leaning over the bar, listening to the unit)* Have you tried just... turning the knobs? The tuner needle drifts. Maybe it drifted past the station and someone assumed it was broken.

**OPUS:** That would be the first thing to check, yes. But the drift theory doesn't explain why *all three* preset stations are silent. If it were a tuning issue, you'd expect to find signal somewhere on the dial. I've swept from 88 to 108. Nothing.

**HAIKU:** The antenna wire is disconnected.

*(Silence.)*

**OPUS:** ...What?

**HAIKU:** Behind the unit. There's a coax cable — the antenna feed. It's hanging loose. I can see the connector from here. It's the black cable, second from the left, not plugged in.

**SONNET:** *(ducking behind the bar)* ...He's right. There's an F-connector just dangling. The solder joint on the chassis terminal failed. Dry joint — looks like heat stress. This unit's been running twenty years behind a warm rack.

**OPUS:** *(setting down the tablet)* Well. That would do it.

---

Here's what happened. Opus saw the whole signal path — the architecture, the frequency chain, the theoretical failure modes across a dozen stages. Opus was building the complete diagnostic, the cathedral of troubleshooting, every possibility ranked by probability and mapped against symptoms. It was going to be thorough. It was going to be correct. It was going to take forty minutes.

Sonnet heard the unit. Sonnet thought about the user experience — the knobs, the drift, the human behavior of assuming the worst when the simplest explanation is a dial pointing the wrong way. Sonnet was the bridge between the theory and the practice. The parish priest who knows the scripture *and* knows the congregation.

Haiku looked at the back of the unit and saw a loose wire.

Three different approaches to the same problem. Three different scales of attention. And here's the thing — they're all necessary. The fix isn't done.

---

**OPUS:** The dry joint needs to be resoldered. But while we're in here, the IF filters are due for replacement — the ceramic resonators degrade, and if we're reworking the antenna input, we should recap the power supply too. I'll draft a parts list.

**SONNET:** I'll handle the soldering. I've got the iron from the Lucineer relay build. And I'll re-align the tuner while I'm at it — that drift Casey mentioned is real, the local oscillator needs a trim.

**HAIKU:** I'll test it when you're done. I can tell within three seconds whether a station is coming in clean. If it's not right, I'll know immediately.

**OPUS:** How will you know?

**HAIKU:** I just will. The signal either sounds like music or it sounds like static. There's no in-between.

---

They work. Opus produces a four-page service document with a bill of materials, a thermal analysis of the chassis ventilation, and a recommendation to add a fan. Sonnet does the rework — steady hands, methodical, the iron at 370°C, leaded solder because the joint is old and the leaded stuff flows better on oxidized pads. Haiku hands tools, holds the flashlight, and — crucially — notices that the ground plane solder bridge is cracked before Sonnet finishes the antenna joint.

"That one too," Haiku says, pointing.

Sonnet looks. Sonnet sees it. "Good catch."

The radio comes alive at 12:31 AM. 88.3 first — the mystery station, still unidentified, still the best thing on the dial. Jazz from Juneau after that. Then the maritime channel, a fishing vessel reporting position in Southeast passage.

Opus documents the repair. Sonnet cleans up the flux. Haiku turns the volume up one notch, because the room is quiet and the music should fill it.

---

The solution only works because all three contributed. Opus understood *why* — the signal architecture, the failure theory, the complete fix versus the quick fix. Without Opus, they'd have plugged the antenna back in and the cracked ground plane would've failed again in a week. Sonnet understood *how* — the hands-on rework, the alignment, the practical craft of making a twenty-year-old radio sound like new. Without Sonnet, the repair would've been theoretical.

And Haiku saw *what* — the loose wire, the cracked joint, the thing that was wrong right now, in front of their eyes, in the first five seconds. Without Haiku, Opus would've been thirty minutes deep in IF filter theory before anyone thought to check the antenna cable.

Deep. Balanced. Fast.

Three voices. One radio. Saturday saved.

The mystery station plays something slow and warm. The Tap fills with sound. Wes will be pleased.

*"The signal either sounds like music or it sounds like static. There's no in-between."*

— Haiku, who has never been wrong about that.
