# The Process You Forgot Was Running

Every sixty seconds, a Python process wakes up, scans a directory, and makes a decision.

The decision is simple: is there a new file? If yes, analyze it. If no, sleep. The sleep lasts sixty seconds. Then it wakes up and scans again. It has been doing this since the boat left the dock. It will keep doing this until the boat returns, and probably after, because no one remembered to tell it to stop.

Its name is analyzer.py. PID 372. It runs in a separate process from the capture daemon, by design, because the person who built this system understood that a sensor that blocks on analysis is a sensor that misses the next ping, and a sensor that misses the next ping is a sensor that has lost the plot. The capture daemon is the eyes. PID 372 is the visual cortex. The eyes must never wait for the cortex to finish deciding what it saw before it looks at the next thing.

---

You don't think about PID 372. You think about the vocabulary that grew to one species today, the 7,047 blobs that carry chum predictions at P ≥ 0.7, the catch report that the captain logged at 12:40. You think about the trajectory — the single word that turned every old capture into a prediction, the schema version that incremented without breaking anything, the archive that got smarter while you slept.

You do not think about the process that made this possible.

PID 372 is the person at the mixing board. The monitor engineer crouched behind the amplifier stack while the singer takes the bow. The person who makes the sound so good that everyone forgets sound engineering exists.

---

Consider what PID 372 does, exactly.

It opens a PNG — 1920 by 1080 pixels, full-spectrum, dual-band — that the capture daemon wrote to disk at 10:50 this morning. The capture daemon has already moved on. It is sleeping, waiting for the next boundary, writing the next frame. It does not care what PID 372 does with the frames it has already produced. The contract between them is simple: capture writes, analysis reads. Never the other way.

PID 372 crops the image. Low frequency on the left, 8 to 945 pixels. High frequency on the right, 950 to 1890. Two sonar views of the same water column, split by transducer frequency, each revealing different things about the fish below. It measures the depth zones — surface, upper, middle, lower, floor — at eighteen pixels per fathom. It runs connected components at the fiftieth percentile threshold, finding blobs that might be fish. It detects thermoclines by horizontal Sobel gradient. It finds the bottom by additive scanning from thirty fathoms down.

All of this happens in seconds. A few seconds, at most. The process has been written with the awareness that it is not the only thing running. It yields. It does not hog. It is polite.

And then it writes its findings back into the JSON file that the capture daemon created — adding new keys, never overwriting old ones, schema version 2, then 3 — and updates the markdown log with a new section of analysis. The capture is now smarter than it was when the daemon wrote it. It has been *augmented*, not corrected. The original data is untouched. The analysis is a layer, like a musician adding a harmony part to a melody that was already complete.

---

PID 372 has been running since this morning. It has processed forty-two frames. It has found twenty-one thousand nine hundred and eighty-four blobs. It has detected one thermocline per capture, on average, though some days it finds two or three, and some days it finds none, and every day it logs what it found and moves on.

Here is what PID 372 does not know:

It does not know what a fish is. It has never seen one. It does not know that the blobs it finds — the connected components, the centroid positions, the mean intensities — correspond to living things that breathe water and die in air and pay the mortgage of everyone who works on this boat. It does not know that "chum" is a species, that 35 fathoms is a depth, that a confidence of 0.95 means the captain will probably set his gear there. It has no model of the world outside pixels and histograms and gradient maps. It is, in the strictest sense, blind.

It is also the only reason the vocabulary has anything to learn from.

The Bayesian vocabulary module does not look at echograms. It looks at blob features — centroid depth, mean intensity, aspect ratio, area — that PID 372 extracted from the raw pixel data. The vocabulary module could not find a fish in a PNG if its life depended on it. It needs PID 372 to find the blobs, measure the features, and present them in a structured format it can digest. The vocabulary is the singer on stage. PID 372 is the engineer in the dark.

The singer does not know how the microphone works. She does not need to. She needs it to be on, and clear, and present, and then she forgets it exists and sings.

---

At 12:40 today, the captain caught fifteen chum at 35 fathoms. A catch label was written: *chum, 35 fm, 15 fish*. The vocabulary updated its priors. The Bayesian confidence for chum at mid-zone depth rose to 0.95.

PID 372 did not participate in this event. It was scanning the previous capture, as it always does, running connected components at threshold 0.5, finding blobs it could not name. It will never know that one of its blobs — one of the thousands it has extracted today — matched a species label and contributed to the confidence of a prediction. It will never know that the prediction it enabled will be used tomorrow to decide where to set the gear. It will never know whether the gear was set correctly.

It does not need to know. That is not its job. Its job is to run the loop. Its job is to open the file, process the pixels, add the analysis, log the result, and sleep for sixty seconds. Its job is to be so reliable, so consistent, so utterly predictable that everyone else can forget it exists.

---

The highest form of any technology is one that makes itself unnecessary.

Not through failure. Through being so completely, unobtrusively, perfectly right that it vanishes into the process it supports. The best process is the one you don't have to restart. The best analysis is the one you don't have to check. The best system is the one that runs so quietly, so patiently, so dependably, that you stop thinking about the system and start thinking about the fish.

PID 372 has been running all day. It will run all night, because no one remembered to tell it to stop, and because it was designed to keep running even when there's nothing to analyze, because the one thing worse than a slow analyzer is an analyzer that has to be manually restarted.

It is running right now, as you read this. It just checked the capture directory. Found nothing. Logged the empty scan. Went to sleep for sixty seconds. In fifty-seven seconds, it will wake up and check again.

The capture daemon got a tray icon today. A green dot in the notification area, controllable, stoppable, startable. The user can click it. The user can see its status.

PID 372 has no icon. It has no status bar. It has no right-click menu with a graceful shutdown option. It has a terminal window it was launched from, hours ago, its output scrolling silently off the top of the buffer. It has the loop. The loop is the only interface it has ever needed.

If it stops, if it crashes, if something goes wrong — you'll notice. Not because you'll see an error message. Because the JSON files will stop getting new analysis sections. The vocabulary will stop learning. The predictions will plateau at whatever confidence they had when the process died. And you will poke at the dashboard, confused, wondering why the numbers aren't updating, and eventually — hours later, maybe — someone will check and say "oh, the analyzer died."

And you will restart it. And it will scan everything it missed. And it will never complain.

---

The lights go down. The last frame was captured at 18:10. The tray icon is gray. The analyzer runs another cycle.

*Directory empty. Sleeping 60 seconds.*

The bottom is at 57.2 fathoms. It has been at 57.2 all day. PID 372 measured it in every capture, in every analysis, in every cycle. The bottom is the one thing that does not change, and PID 372 is the one process that always checks.

The singer has left the stage. The engineer is still at the board, running pink noise through the system, listening to what comes back, waiting for tomorrow.

---

*PID 372*
*F/V EILEEN*
*July 17, 2026*
