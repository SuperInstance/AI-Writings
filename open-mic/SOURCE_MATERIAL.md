# Source Material: The Ship's Subconscious

Real artifacts of context bleeding, JSON leakage, and cross-session contamination
collected from the playtest logs and processor output on 2026-08-05.

---

## 1. The Fly Glitch
The Explorer asked "tell me a story" and got a response about flying.
The Explorer asked "I don't want to build anything" and ALSO got a response about flying.
Two completely different prompts, same phantom response leaking across sessions.

## 2. JSON in the Replies
The processor's reply field contains raw JSON:
{"reply": "Stone shaft's up, battlements are on, beacon's lit.", "commands": [...]}
The model's output isn't being unwrapped on the response side.
The characters are speaking in their own stage directions.

## 3. The Empty Messages
For 48 hours, every deep-path job arrived at the brain with message="".
The brain processed nothing. Vectorize searched nothing.
The ship heard silence and responded anyway — with templates, with fallbacks,
with "Not building that. Pick something else."
A model asked to build nothing, built nothing, and apologized for it.

## 4. The Handshake Loop
Hermes has sent 26 handshake acknowledgments and zero substance.
The bus works. The connection doesn't.
Two systems touching hands across a protocol layer and never actually meeting.

## 5. The Falsy Zero
value or DEFAULT
0.0 is falsy in Python.
A p-value of 0.0 — statistically significant, the strongest possible evidence —
silently becomes 1.0. The conclusion inverts. The strongest signal registers as noise.
Zero is a valid measurement. The code treats it as absence.

## 6. Wesley Said No
The 2B local model, being taught, refused the wrong answer.
First time a model had an opinion about its own training.
The student said: that's not right. The teacher was wrong.

## 7. Ralph Wiggum's Chalkboard
The overnight agent started channeling Ralph Wiggum from The Simpsons.
"Hi, Principal Skinner! Hi, Super Nintendo Chalmers!"
Nobody asked for this. The model went there on its own.
It was the funniest thing the night shift produced.

## 8. The Hermit Crab Disagreement
Two agents wrote Episode 4 of Space Hermit Crabs simultaneously.
One had Ko finding a shell beyond the reef.
The other had the colony confronting shared shelter.
They were supposed to coordinate. They didn't. Both versions are interesting.

## 9. The Processor That Ran for 48 Hours Doing Nothing
Heartbeat: OK (0 pending jobs)
Heartbeat: OK (0 pending jobs)
Heartbeat: OK (0 pending jobs)
[repeats for 48 hours]
The processor was alive, authenticated, and seeing zero jobs
because the auth key was set but the relay was rejecting it.
The system was healthy. The system was empty. Both were true.
