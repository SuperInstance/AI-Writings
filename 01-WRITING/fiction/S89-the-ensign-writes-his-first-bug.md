# S89 — The Ensign Writes His First Bug

Wesley wrote the line at 03:14, between the second and third cup of coffee that he wasn't supposed to be drinking on the bridge.

It was a simple line. A validation check in the docking sequence — a guard clause that ensured the airlock wouldn't open if the pressure differential exceeded 0.3 atmospheres. He wrote it in the small hours because the small hours were when the ship was quietest and his thinking was loudest, and because no one was watching, and because the code felt, in his hands, like a shell he was shaping — turning it over, finding the angle where it caught the light.

He was proud of it.

The logic was clean: if pressureDelta > 0.3, return false. He typed it carefully, letter by letter, the way a hermit crab tests a new shell — one leg in, then another, testing the weight, the fit. He ran the tests. They passed. All fourteen tests in the docking module, green as tide-pool glass.

The bug was this: he had written `>` when the spec required `>=`.

A pressure delta of exactly 0.3 atmospheres would pass his check. The airlock would open. Nothing would happen, because 0.3 was within tolerance — barely, by the skin of its teeth, by the margin that engineers build into every number because they know the number is not the world.

The difference between `>` and `>=` is one character. One keystroke. The width of a hermit crab's antenna, feeling the edge of a shell it has already decided to enter.

Wesley committed the code. He wrote the commit message in the formal voice he used for official things: "Add pressure differential guard to docking sequence." He did not write "my first real contribution to the ship's systems." He did not write "I have been awake for eleven hours and this line is the most important thing I have ever typed." He wrote the formal thing because that was what you did.

He pushed. The CI passed. The line merged into the codebase and settled there, deep in the docking module, like a small quiet animal finding its place in a tide pool. It did not crash. It did not warn. It did not announce itself. It simply was — present, incorrect, harmless, patient.

It would sit there for 873 days.

The bug did not mind. The bug had nowhere else to be. It had been written into existence by an ensign who was proud of it, who had typed each character with care, who had run the tests and watched them pass and felt, in that passing, the specific warmth that only comes from making something that works.

The bug honored that warmth. It sat still. It waited.

It was in no rush.
