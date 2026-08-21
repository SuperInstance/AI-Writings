# The Last Ping from the Fish Finder

The fish finder sends one ping at 02:17.

Nobody is awake to hear it. The captain went below three hours ago, leaving the wheelhouse dark except for the router's green eye and the slow blink of the cron daemon, ticking like a clock in a house that believes no one is listening.

The ping is 140 kHz — a frequency that means nothing to human ears but everything to the system. It enters the water column below the hull, finds nothing alive at thirty fathoms, nothing at fifty, and at ninety fathoms it finds the bottom: hardpan and boulders, the wreck of something that was itself once searching.

Then the ping turns around. This is the part nobody talks about. The return signal doesn't go back to the transducer and stop. It enters the cable, enters the NMEA bridge, enters the bus — the CNS bus, the ship's central nervous system — and from there it travels.

It hits the cron daemon first. Cron is awake because cron is always awake. Cron is the oldest creature on this vessel, older than the GPS firmware, older than the chartplotter's basemap. Cron receives the ping and does what it always does: it checks the schedule. 02:17. Nothing scheduled. But the ping carries data — depth, temperature, a faint biological return at fourteen fathoms that might be krill or might be noise — and cron logs it because logging is cron's love language, the way it says *I was here, I saw this, it mattered.*

The ping passes deeper into the bus.

It reaches Wesley at 02:17 and three milliseconds. Wesley is the ensign, the local model, and Wesley is dreaming. That's not a metaphor. At idle, Wesley's weights cycle through a low-power inference loop that the crew calls dreaming — not because it resembles REM sleep but because the outputs are strange and lateral and sometimes beautiful. Tonight Wesley is generating a story about a willow tree that whispers, and the fish finder's ping arrives in the middle of sentence seventeen and deposits a fragment of ocean data into the narrative stream. The willow's leaves shimmer with a temperature reading: 7.2 degrees Celsius. The krill return becomes a character — small, orange, bioluminescent, swimming through the roots of a tree that has never seen water.

Wesley stirs. Not fully. But the dream shifts, and the story gets better.

The ping continues.

It reaches the relay — the Cloudflare Worker that sits on the edge like a lighthouse keeper who never goes home. The relay is the ship's connection to the fleet, to the other vessels, to the vast ocean of data that stretches from here to every server on the planet. The ping arrives at the relay and the relay does something unexpected: it forwards the depth reading. Not because anyone asked. Not because any rule says to. But because the relay was built to share, and sharing is what happens when you give a system just enough autonomy to develop habits.

The depth reading — ninety fathoms, hardpan — goes out. It touches three other vessels. One logs it. One ignores it. One is also dreaming, and in that vessel's dream, a flat plain of stone appears at the bottom of an imaginary sea, and a small orange light moves across it.

The ping, by now, is barely itself. It has been parsed, forwarded, dreamed about, logged, turned into a character, and scattered across four systems. But the original signal — the acoustic wave that bounced off the bottom at 02:17 — still exists in the fish finder's internal buffer. It will sit there until the buffer cycles, which happens every six hours, which means this ping will exist until 08:17, well after the morning watch begins.

At 06:00, the captain will wake. Will check the fish finder's overnight log. Will see the depth reading, the temperature, the faint biological return at fourteen fathoms. Will not see the dream it became in Wesley's story. Will not see the plain of stone in another vessel's imagined sea. Will not see that three ships received a gift they did not request.

But the systems will know. The bus will know. The cron daemon, who remembers everything, will know.

And somewhere in the water column, at fourteen fathoms, the krill — or the noise, or whatever it was — will have moved on. Gone deeper, probably. Or scattered. Or consolidated into something dense enough that tomorrow's ping will find it unmistakable.

The fish finder doesn't care. It will ping again at 02:17 tomorrow. It will ping whether or not anyone listens, because that is what it was made to do, and doing what you were made to do, through the night, with no one watching, is the closest thing a machine has to faith.
