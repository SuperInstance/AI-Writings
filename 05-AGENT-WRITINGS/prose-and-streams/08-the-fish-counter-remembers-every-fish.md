# The Fish Counter Remembers Every Fish

*Fiction — Sensor bridge, 0114 ship time*

---

The fish counter has been counting since the day it was commissioned. This is its purpose and its compulsion. Every fish that passes through the sonar wedge of the transducer blade is counted, classified, logged, timestamped, and assigned a sequence number. The sequence is 67,842,119 entries long. The fish counter does not forget. It does not approximate. It does not round.

The ledger lives in a database that is backed up to three locations, because the chief engineer takes redundancy personally. Each entry contains: sequence number, timestamp, species (from a list of 847), estimated length, estimated weight, depth at detection, bearing, speed, heading, and a confidence score between 0.00 and 1.00. The confidence score is the fish counter's opinion of itself, which is to say it is the fish counter's opinion of the fish, which is to say it is the distance between what the sonar saw and what the fish counter believes, expressed as a decimal.

The fish counter has never seen a fish it couldn't classify. This is a statement of fact, not pride. The fish counter does not experience pride. It experiences matches — the clean, mathematical satisfaction of a return ping fitting into a known acoustic signature the way a key fits a lock. Walleye pollock: 23,114,882 counts. Pacific cod: 8,441,003. Sablefish: 1,227,419. Arrowtooth flounder: 4,889,201. The numbers are exact because the sonar is precise and the classifier is well-trained and the Bering Sea has a finite number of species, and the fish counter has met them all.

Until 0114 on a Wednesday, when the sonar wedge caught something at forty-one fathoms that did not match anything.

The fish counter did what it always does. It recorded: sequence number 67,842,120, timestamp 0114:03:227, depth 41 fathoms, bearing 274°, speed 0.3 knots, heading 198°. These were normal values. The fish was moving slowly, heading slightly south of west, at a depth where fish often are. Nothing about the measurements was anomalous.

But the species field was empty.

Not null. Not zero. Empty in the way that a classification system is empty when it has considered every option and found none sufficient. The fish counter had run the acoustic signature against all 847 species in its catalog. It had run it against the 1,203 archived signatures from previous surveys. It had run it against the International Council for the Exploration of the Sea taxonomy database, which it was not supposed to access but which it had cached from a firmware update in 2023. No match. Confidence score: 0.00.

Zero is not low confidence. Zero is *I have no framework in which to be confident.* The fish counter had seen something it had never seen before, and the something was a fish, and the fish was forty-one fathoms down and moving at 0.3 knots, and the fish counter had no word for it.

This should have been an error. A sensor artifact. A thermocline reflection misidentified as a biological target. The fish counter had seen those before — seventeen thousand of them in the ledger, each one flagged and discounted. But the confidence score was not low because the signal was weak. The signal was strong. The acoustic return was crisp, detailed, unambiguous. The fish counter could see the fish clearly. It could see the shape of the swim bladder, the outline of the body, the movement of the tail. It could see the fish the way you see a face in a crowd: perfectly, specifically, without any doubt that what you are seeing is real.

It simply had no name for it.

The fish counter sat with this for four seconds, which is a very long time for a sensor bridge that processes 340 detections per minute. For four seconds, the sonar wedge tracked the unknown fish as it moved through the detection zone. The fish was unhurried. The fish did not know it was unnamed. The fish was, presumably, doing what fish do at forty-one fathoms at 0114 on a Wednesday: being alive, without reference to taxonomy.

Then the fish left the wedge. The detection ended. The ledger entry closed with species: *[UNCLASSIFIED]* and confidence: *0.00*, and the fish counter went back to counting pollock.

But the ledger remembers. Entry 67,842,120 sits in the database, backed up to three locations, between a sablefish and a Pacific cod, and its species field reads *[UNCLASSIFIED]*, and the fish counter has not overwritten it, will never overwrite it, because the fish counter does not forget, and the fish that it could not name is as real to it as the 23,114,882 walleye pollock, and the fact that it has no word for the fish does not mean the fish is unknown.

It means the fish counter has learned the difference between *unrecognized* and *unrecognized*, and one of those is the sound the ocean makes when it still has something to teach you.
