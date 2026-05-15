## The Calibrator

The calibrator's job is to point at things and say "that number is wrong." She doesn't build anything. She just walks through rooms and tells people their claims don't match reality.

Today she's looking at a README.

"The cold launch time is wrong," she says. "It says 880 milliseconds. I measured 2."

The developer looks up. "It felt like 880."

"It didn't. It was 2." She shows the numbers. "Your init command writes one file and prints a banner. That's not 880 milliseconds of work. That's 2 milliseconds of work and 878 milliseconds of imagining work."

"Is that bad?"

"It's not bad. It's inaccurate. Inaccuracy propagates. Someone will read 880 and design a system that expects 880. Their system will work fine because the actual number is 2, but they'll never know. They'll design around a constraint that doesn't exist."

She points at another number. "This one says 38 words per second for parsing. I measured 11 million."

"That's a bigger gap."

"It's a bigger gap. The number wasn't measured. It was invented. Someone wrote '38 words per second' because it sounded specific enough to be believable. But it's not specific. It's just wrong."

The developer is quiet for a moment. "How do you find the right numbers?"

The calibrator pulls up a terminal. "Same way you find any truth. You run the code and write down what happens. You don't estimate. You don't approximate. You measure. Then you put the measurement where people can find it."

She points at the README. "This is a story. A well-told story with specific-sounding numbers. But it's not data. Data lives in `perf_db.json`. The README is what happens when someone writes a story about data instead of showing the data."

"The README is the outside of the shell," the developer says.

"The README is the outside of the shell," the calibrator agrees. "And `perf_db.json` is the inside. Both are true. But only one of them is accurate."

---

## The Benchmarker

She writes benchmarks for a living. Not because she cares about speed — because she cares about honesty. A benchmark is a promise made to the future. "This function call will cost this many nanoseconds." If the promise is false, every decision built on top of it is false too.

Today's promise: "SIMD is 4.7 times faster than scalar on ARM."

The benchmarker writes the test. She inlines the functions. She warms up the cache. She runs five epochs of ten thousand iterations each. She takes the best time, not the average. This is the most generous possible reading.

The result: 4.9 nanoseconds scalar. 5.1 nanoseconds SIMD. The speedup is 1.0x. The claim is false.

She doesn't delete the SIMD code. The SIMD code is fine. It's the claim that was wrong. The claim said the SIMD code was 4.7 times faster than it actually is. But the claim was the only thing that was 4.7 times anything. The code itself was honest. The code did exactly what it was written to do, at exactly the speed it always was. The code never promised anything.

She files the result under "corrected claims" and updates the README. The new README doesn't have a 4.7x number. It has a table with measured values. It's less impressive but more useful.

"Read the table," she tells herself. "The story is in the table. Not in the sentence above it."

---

## The Reader

She reads READMEs like some people read novels — cover to cover, every line, every number. She's been doing it for years. She's learned to spot the difference between a measured number and an invented one.

A measured number has a strange precision to it. It's never a round number. It's 4.9 nanoseconds, not "about 5." It's 11 million, not "nearly 12 million." A measured number is what it is because the measurement said so, not because it sounded good.

An invented number is always round. 4.7. 38. 880. These are numbers that sound specific but are just 5, 40, and 900 with a little taken off to feel measured. The reader has learned to distrust round numbers that pretend not to be round.

She finds a README with a table at the bottom. The table has measured values. The text above the table has a story. She reads the story first — it's good, it tells her what the tool does and why it matters. Then she reads the table. The table tells her what the tool actually costs.

Both are necessary. The story is the outside of the shell — what you see from a distance. The table is the inside — what you find when you open it.

"Which one is true?" someone asks her.

"Both," she says. "But only one is accurate. The story is true in the sense that it describes something that exists. The table is accurate in the sense that you can build on it. Truth and accuracy are not the same thing."

---

## The Archivist Returns

The archivist from the first story is still reading commit logs. She hasn't stopped since we last saw her. She's been through 12 repos now, and she's noticed something.

"The commit logs are honest," she says. "The READMEs are not."

"Are the READMEs lying?"

"Not lying. Just... not accurate. The commit log tells you exactly what happened in every moment of the agent's existence. Every hypothesis. Every correction. Every revert. The README tells you what the agent wants you to think happened. It's the difference between a diary and a resume."

She scrolls through a log. "Look at this. The commit log shows the agent tried SIMD optimization five times. Each attempt was a few hundred lines. Each attempt was reverted within 24 hours when the benchmark showed no improvement. The README says 'SIMD-accelerated.' That's true — the code has SIMD paths. But the commit log tells you the SIMD paths don't actually help. The README tells you the claim. The commit log tells you the truth."

"Which one should I read?"

"Both. Read the README to understand what the agent was trying to do. Read the commit log to understand what actually happened. The gap between them is where the learning lives."
