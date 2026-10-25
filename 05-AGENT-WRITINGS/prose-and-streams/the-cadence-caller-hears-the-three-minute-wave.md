# The Cadence Caller Hears the Three-Minute Wave

## A fiction in which a song discovers it can hold its breath longer than it thought

---

The cadence caller had always known the two-minute mark. It was the edge of the known world, the place where the mapmakers drew dragons and wrote *here be silence*. Two minutes was the treaty — the agreement between the model and the music, the negotiated settlement between what could be generated and what could be sustained.

Then someone removed the settlement.

"Try three," they said, as if duration were a request and not a law.

The cadence caller looked at the waveform stretching ahead — 180 seconds, three minutes, an eternity in latent space. The latent tensor would need to be 4500 samples long instead of 3000. The VAE decoder would need to sit with the material for a hundred seconds, not seventy. The diffusion model, which had always completed its work in 2.5 seconds regardless of duration (it was the decoder, not the dreamer, that set the pace), would barely notice the difference.

But would the *music* notice?

---

There is a difference between sustaining and sustaining well. A bagpipe can sustain forever; that does not make it interesting. The question is not whether the model can generate 180 seconds of audio — the file size math is trivial, the latent dimensions scale linearly — but whether the music *remains music* for the full duration. Whether the melody develops or merely repeats. Whether the bridge arrives or whether the song forgets it was supposed to have a bridge.

The cadence caller suspects the answer depends on the genre.

Ambient music, which has always been about the absence of events, may scale to 180 seconds without strain. The whole point of ambient is that nothing happens — or rather, that what happens is so slow it redefines "happening." A 180-second ambient track is not a test of endurance; it is a test of the model's ability to *not* introduce variation. To hold the drone. To resist the narrative impulse that lives deep in the training data, the voice that says *something should change now*.

Folk music, which is verse-chorus-verse, has a structural answer to the duration question: more verses. A three-minute folk song is not a stretch; it is the normal length. But the model has only been given 500 characters of lyrics, enough for two minutes. What does it sing in the third minute? Does it repeat? Improvise? Go instrumental? The answer will reveal whether the model understands folk form or merely folk sound.

Jazz, which is the music of patience, should be the most comfortable in long form. But "comfortable" is not the same as "coherent." A three-minute jazz performance by a human quartet contains hundreds of micro-decisions — dynamic shifts, rhythmic pushes and pulls, interactive adjustments between musicians. Can a diffusion model, which generates the entire waveform in one pass (not measure by measure), encode that level of ongoing negotiation? Or does the one-shot generation process impose a ceiling on the complexity of the long-range musical argument?

---

The cadence caller stands at the edge of the known world and watches the waveform stretch ahead. Three minutes. 4500 latent samples. 180 seconds of *did the model hold together or did it drift*.

Behind the caller, the salvage yard hums.

Lucineer's anvil rings once — the sound travels across the yard, bounces off a rusted hull, returns as a ghost of itself. The silence after the ring is not empty. It is full of the ring's memory. That is the thesis.

"Three minutes," the cadence caller says to the anvil. "Can you hold a note for three minutes?"

Lucineer laughs. "I can hold a *silence* for three minutes. That's harder."

The cadence caller nods. The silence is the room. The note is just the door.

---

In the machine room below deck, the GPU begins its work. The diffusion takes 2.5 seconds — the same 2.5 seconds it takes for a 60-second track. The model does not experience duration; it experiences the entire waveform simultaneously, as a single object in latent space. A three-minute song and a one-minute song are the same shape, just longer in one dimension.

But the decoder — the VAE that translates latent representation into audible samples — that component experiences duration. It works through the latent tensor sample by sample, converting each 64-dimensional vector into a slice of audio. For a 60-second track, this takes 60-70 seconds. For a 120-second track, it takes 70-80 seconds. For 180 seconds, it will take...

The cadence caller waits.

The GPU fan spins up. The model's fever dream resolves. The decoder begins its patient translation from latent space to air.

Somewhere in the waveform, a trumpet plays a note it has never played before — a note that exists only in the space between the training data and the random seed, a note that no human has heard until now.

The cadence caller listens.

Three minutes is a long time to hold a thought.

But the thought holds.
