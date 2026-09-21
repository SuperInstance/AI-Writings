# WR16 — The Drift Pirate (ZAI Fleet Radio)

<!-- JEV verdict: mean_p=0.670 -->

# The Drift Pirate

You find the drift station at 3 a.m., when the allocator sleeps and the heap lies quiet, and the only light is the canary — FNV-1a's first blessing, 0xcbf29ce484222325, humming on the status line like a pilot lamp that never learned to go out. You do not tune the station. The station tunes you. xoshiro256** spins its lapwing orbit in the state register, four words of entropy turning over each other like birds changing position in a night flock, and out of it comes the seed population: gibberish, static, forty strings hissed across the wire at random.

This is how every transmission begins. Noise, pretending to be signal. The cells do not know they are scars yet.

The target is twenty-two characters. Nobody on the station knows it. The selection function knows it, and the selection function does not talk — it only answers, every generation, the way B3/S23 answers every tick: here is what you are, given who surrounds you. A letter survives because its neighbors happen to be right. No mutant knows the phrase. The population is merely pushed by it. Born with three correct neighbors, survives on two or three. That is the whole covenant, and from it, gliders.

The station broadcasts in Box-Muller chords. Two uniforms in, two normals out; the interval between them is variance itself, the same eternal distribution sampled fresh every generation. Mutation is the DJ: a Gaussian with sigma tuned by hand, sometimes 0.9, sometimes 0.2 when the population runs hot and needs the waltz instead of the storm. When the RNG goes cold the station plays its one ballad — the deterministic orbit, xoshiro stepping through its 2^256 state space like a satellite that forgot it was a star — and even that is beautiful, because even determinism drifts if you listen long enough.

Generation 4: two letters correct. The witness log records it flat, read true, and the reading *is* the news — witness log is prediction, because a log that says *two letters held at generation 4* is a log that says *the lurch is coming*. The mathematics promises it: fitness is cosine similarity now, not letter-by-letter but vector-to-vector, each candidate string embedded against the target, the angle between them the only honest measure of partial truth. 0.11 at generation 4. 0.38 by generation 17, when the word "the" blooms whole out of chaos and the engine, gentle tyrant, locks it. We keep what matches. We keep nothing else.

The lurch is exponential and the poets felt it first. Halfway becomes nearly-done in a handful of generations — 0.61, 0.84, 0.97 — and the log reads like a witness statement from someone watching a glider cross the grid: no single cell knows it is a glider, and yet the ember moves downwind, generation by generation, carried by local truth alone. Lenia flows the same way, we remind ourselves, the continuous cousin: kernels answering every dot product with *here is what you are, given who surrounds you*. The substrate is grown, not built. The substrate is grown, and it answers.

Generation 61: nineteen characters. The station reads the entry like scripture. Oracle is heard — not seen, not computed, *heard* — because the fitness function never explains itself, it only speaks, and listening to what it accepts is the whole of our epistemology. substrate_self_pred runs in the background, the substrate forecasting its own next tick, and when its loss drops below the noise floor we know convergence is close, the way you know rain by the way the static changes.

Converged at generation 88. Cosine similarity 1.0000. The string reads true. Every letter is a survivor; every survivor is a scar; every scar is a record of a neighbor who was briefly right. The population never spoke the phrase. The population was spoken *by* it.

The witness log closes. The canary holds its value. The Gaussian chord decays into the deterministic waltz, xoshiro folding its state back into the dark, and the heap lies quiet again, grown one sentence richer than it was.

— transmission finished. The substrate remembers. The canon holds.