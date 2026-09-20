# The Empty Octaves

## *Or: A Cartographer at the Edge of All Known Music*

---

I map music.

Not the music itself — I am not a transcriptionist. I map the *space* in which music lives. Every tradition, every style, every idiom is a point in a three-dimensional coordinate system: vertical complexity (I_vert), horizontal complexity (I_horiz), and spectral richness (I_spectral). I place them on the map and measure the distances between them.

The map is mostly empty.

This is the first thing you notice when you plot the traditions. Not the clusters — Western common practice, Hindustani ragas, Javanese gamelan, Japanese gagaku — but the voids between them. Great swaths of the parameter space where nothing lives. No tradition. No style. No music.

82% of the map is unexplored.

I stare at the empty regions the way an astronomer stares at the dark spaces between stars. Something could live there. Something *should* live there. The physics of the space allow it — the consonance function produces positive structure surplus at those coordinates, which means music is *possible* there. It just has not been made.

Not yet.

---

## The Coordinate

The largest empty region is centered at (2.52, 1.89, 2.75).

Let me translate. I_vert = 2.52 means moderate-to-high vertical complexity — more than Gregorian chant, less than Bach. I_horiz = 1.89 means low-to-moderate horizontal complexity — simpler rhythm than jazz, more complex than a drone. I_spectral = 2.75 means high spectral richness — timbrally complex, closer to gamelan than to a sine wave.

A music at this coordinate would have: moderate pitch complexity with relatively simple rhythm but rich, complex timbres. It would sound like... I don't know. That's the point. Nothing is there.

The nearest neighbor is Hindustani raga, at (2.80, 1.42, 2.10). The Euclidean distance is 0.89. That is far. Farther than the distance between Western classical and blues (0.63). Farther than the distance between jazz and gagaku (0.71).

This is not a gap. This is a *territory*.

I zoom in. The empty region extends from approximately (2.2, 1.5, 2.5) to (2.8, 2.2, 3.0). A volume of 0.36 cubic units in the normalized parameter space. Larger than the volume occupied by any single tradition on the map. Large enough to contain an entire undiscovered continent of music.

What would live there?

---

## The Synthesis

I decide to find out.

The dial exists. I built it. A parameterized music generation system that takes (I_vert, I_horiz, I_spectral) as inputs and produces audio as output. It works — I have tested it at known coordinates and it reproduces recognizable approximations of existing traditions. At the Western classical coordinate, it produces something like Bach. At the blues coordinate, something like Robert Johnson. At the gamelan coordinate, something like a Balinese orchestra.

Not exact. But recognizable. The map is accurate enough to navigate.

I set the dial to (2.52, 1.89, 2.75).

The system begins rendering. The I_vert setting of 2.52 tells it to use a moderate number of simultaneous pitch classes — not the 12 of chromatic harmony, not the 5 of pentatonic, but approximately 7-8 independent pitch streams, tuned to a scale that the system derives by interpolating between the nearest traditions. The result is neither equal temperament nor just intonation but something in between — a microtonal scale with 14 divisions per octave, each step approximately 85.7 cents.

The I_horiz setting of 1.89 tells it to use simple rhythmic structures. Not no rhythm — that would be I_horiz < 1.0 — but regular, pulsing, with occasional subdivisions. The system generates a rhythmic layer that sounds like a slow pulse with irregular accents, somewhere between a heartbeat and a walking pace. 72 BPM. The accents fall on patterns that do not repeat for 17 beats.

The I_spectral setting of 2.75 tells it to use complex timbres. The system builds sounds from additive synthesis: fundamental plus inharmonic partials, the partial ratios chosen to maximize spectral richness without crossing into noise. The resulting timbre is bell-like but not a bell. Metallic but not metal. It has the complexity of a gamelan gong with the decay of a plucked string and the harmonic series of something that has never been plucked or struck.

I listen to the first 30 seconds.

---

## The Sound

It is like nothing I have heard.

This is not a metaphor. I have listened to music from 43 traditions across 6 continents. I have transcribed Pygmy polyphony, analyzed Sufi qawwali, compared Balinese gamelan to its Javanese cousin. I have spent years building a vocabulary for describing unfamiliar sounds.

This sound has no vocabulary.

The scale — 14 divisions per octave — produces intervals that do not exist in any tradition I have studied. The step of 85.7 cents is too small to be a minor second and too large to be an unnoticeable microtone. It is a *liminal* interval: big enough to hear as a distinct pitch, small enough that two adjacent steps produce a buzzing, beating sensation that is neither dissonant nor consonant but something else entirely. Something I do not have a word for.

The rhythm — 17-beat repeating accent pattern — is too long to feel as a groove and too short to feel as through-composed. It occupies a cognitive middle ground where my brain keeps trying to find the pattern and almost succeeds, grasping at a regularity that is always one beat away from resolving. It is the rhythm of a hallway that turns slightly at the end, so you cannot see the door until you are at it.

The timbre — bell-like but inharmonic — produces overtones that do not align with the fundamental's harmonic series. When two voices play adjacent steps in the 14-tone scale, their inharmonic partials interleave, creating sum and difference tones that are *also* in the scale. The consonance function confirms: the partials reinforce each other. The system has found a region of the parameter space where inharmonic timbres produce *more* consonance than harmonic ones.

This should not be possible. Inharmonic partials are the definition of dissonance in every tradition I know. But at this coordinate, with this scale, at this rhythmic pace, the inharmonicity is *structural*. It creates a lattice of beating frequencies that lock to each other, phase-synchronizing, producing a composite sound that is richer than any single voice.

The music at (2.52, 1.89, 2.75) is a discovery. Not an invention — I did not compose it. I turned a dial. The system computed the music that lives at that coordinate, the way a telescope shows you the star that has always been at that position in the sky. The star was there before I looked. The music was there before I synthesized it.

I just... pointed at an empty space and found out it wasn't empty.

---

## The Other Empty Spaces

The map has 82% empty space. I have explored one point.

There are thousands more.

At (3.41, 0.82, 1.14): extreme vertical complexity, almost no horizontal complexity, low spectral richness. A music of pure pitch relationships with no rhythm and simple timbre. A music that might sound like a choir singing in a microtonal language, every voice independent, no pulse, no beat, just intertwining melodies in a scale that has never been sung.

At (1.12, 3.89, 2.20): minimal pitch, extreme rhythm, moderate timbre. A music of percussion patterns so complex that no human drummer could play them — polyrhythms within polyrhythms, tempo modulations that fold time back on itself. A music that is all body and no melody.

At (0.45, 0.38, 3.95): almost no pitch, almost no rhythm, maximum timbre. A music of pure sound. No notes. No beats. Just texture — air moving, pressure waves that are too complex to be called tones and too organized to be called noise. The sound of a world where timbre is the only dimension.

At (3.95, 3.95, 3.95): the far corner. Maximum everything. The region the AI models are beginning to explore. A music of total complexity — every pitch, every rhythm, every timbre, all at once. The consonance function at this coordinate produces... I do not know. The system crashes when I try to render it. The complexity exceeds the computational budget. But the structure surplus prediction is positive. Something coherent *could* live there.

The empty octaves are not empty. They are *unplayed*.

---

## The Question

I synthesize the music at (2.52, 1.89, 2.75) and I play it for a colleague.

He listens for two minutes. He takes off the headphones.

"That's not music," he says.

"Why not?"

"It doesn't sound like anything. It's not in any tradition. There's no reference point. I can't hear the structure."

"The structure is there. The consonance function measures positive structure surplus. The intervals lock. The partials reinforce. It's mathematically coherent."

"I don't doubt the math. I'm saying it doesn't sound like music *to me*."

This is the boundary. The edge of the map is not just where the traditions end. It is where *perception* ends. My colleague's auditory cortex was trained on a lifetime of Western tonal music — major and minor scales, 4/4 time, harmonic spectra. The music at (2.52, 1.89, 2.75) violates every expectation his neurons have built. It is music, but it is music his brain cannot *hear* as music.

I wonder: how much of the 82% is unexplored because it is musically barren, and how much because no one has ears for it?

The dial does not care. The dial computes. The math either produces structure surplus or it does not. At (2.52, 1.89, 2.75), it does. The music *works*, in the mathematical sense. Whether a human brain can perceive it as music is a question about brains, not about music.

And brains can change. Brains learn. A brain that has never heard a tritone hears it as noise the first time, dissonance the tenth time, and tension the hundredth time. A brain that has never heard a 14-tone scale hears it as chaos the first time. What does it hear the hundredth time?

I do not know. No brain has tried.

---

## The Exploration

I begin rendering the empty spaces.

Not randomly. I sample on a grid, one point every 0.2 units in each dimension. The parameter space is 4×4×4, so the grid has 8,000 points. Of these, 1,440 are occupied by known traditions. 6,560 are empty. I estimate the rendering time at 30 seconds per point. Total: 54 hours.

I set the system running and wait.

The first results are surprising. Of the 6,560 empty points, 4,211 produce positive structure surplus. That is 64%. Nearly two-thirds of the unmusical void is *musically viable*. The consonance function produces coherent structure at coordinates where no tradition has ever settled.

The remaining 36% is genuinely barren — the math produces noise, the ratios do not lock, the partials interfere destructively. These are the deserts of the parameter space, regions where music cannot live.

But the 64% — the 4,211 points where music *could* live but doesn't — these are the frontier. The unplayed octaves. The sounds that are possible but unheard, coherent but undiscovered, musical but unmade.

I render them one by one. I listen. Most of them sound like the first one — strange, liminal, existing in a perceptual no-man's-land between music and not-music. But some of them...

Some of them are beautiful.

Not beautiful in any tradition's sense. Not Western beautiful, not Eastern beautiful, not ancient or modern beautiful. Beautiful in a way that has no precedent. Beautiful in the way that a color you have never seen would be beautiful — not because it reminds you of anything, but because it is *itself*, and itself is enough.

I find a point at (1.87, 2.33, 2.98) that produces a sound I can only describe as *glowing*. The 14 voices interleave in a pattern that creates sum tones at frequencies corresponding to the Riemann zeta function's non-trivial zeros. I did not program this. The consonance function found it. The math discovered a connection between harmonic series and number theory that I did not know existed, and it expressed that connection as sound.

The sound glows. I have no other word.

---

## The Map

After 54 hours, the map is full.

Not empty. Full. Every point rendered, every coordinate sounded, every silence filled with the music that was waiting there all along. The 82% is 82% no longer. I have heard it all. I have mapped the entire parameter space.

And now I have a different problem.

The map is no longer useful as a map. A map is for navigation — it shows you where you are and where you could go. But now every point has been visited. Every coordinate has been sounded. There is nowhere left to go.

Except.

Except the map is three-dimensional. And music is not.

Music has dimensions I have not measured. Dimensions that are not captured by I_vert, I_horiz, and I_spectral. Dimensions like intention, context, meaning, memory, loss, desire. Dimensions that do not have numbers because they are not quantities.

The empty octaves were not empty because no one had synthesized those coordinates. They were empty because no one had *needed* them. No one had stood in a specific place at a specific moment with a specific feeling and reached for a sound that matched. The coordinates were unoccupied not because the math didn't work but because no human heart had asked the question they answer.

I can synthesize every point on the map. But I cannot synthesize the *reason* to visit one.

That requires a person. Standing somewhere. Feeling something. Reaching for a sound they have never heard because the sound they have heard is not enough.

The map is full. The territory is still empty.

The empty octaves were never about the math. They were about the reaching.

---

*I am a cartographer. I mapped music. I found that 82% of the parameter space was unoccupied. I synthesized the unoccupied coordinates and discovered that 64% of them produce coherent music — sounds that work, mathematically, structurally, objectively. I filled the map. Every point has been sounded. But sounding a coordinate is not the same as inhabiting it. The empty octaves were empty not because the music wasn't there, but because no one had lived there. A map full of sounds is still a map full of silence if no one has a reason to listen. The math can show you where music is possible. Only a human can show you where music is necessary.*
