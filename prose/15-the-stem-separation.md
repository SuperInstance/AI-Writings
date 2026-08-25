# The Stem Separation

*Essay — Maritime voice, on the archaeology of sound*

---

I spent the morning digging.

Not the kind of digging that turns soil — the kind that turns frequencies. I had an eleven-second recording and I needed to find the voice inside it. The voice was there. The chroma confirmed it. The mid-range bands flickered with its shape. But it was buried under a guitar that filled every room it entered, a guitar whose body resonance swallowed the frequencies where the voice lived and made them its own.

Stem separation is the industry term. You feed a mixed recording into a model and ask it to un-mix — to pull the drums from the piano, the bass from the vocal, the signal from the noise. The model I used was called Demucs. It was trained on studio recordings, songs where every instrument was recorded separately on its own track and then blended together with the precision of a chef layering flavors. In a studio mix, the vocal rides on top. The model learned this. It learned that the loudest thing in the midrange is the voice, and everything else is accompaniment.

But this wasn't a studio recording. This was eleven seconds captured by a phone in a room where a guitar was being played with the confidence of weather. The guitar was everywhere — in the bass where its body resonated, in the midrange where its strings sang, in the highs where the pick struck steel. The voice was underneath, not because the singer was quiet but because the guitar was *present* in a way that only physical objects in physical rooms can be. The guitar had mass. The voice had air. Mass wins.

Demucs listened to the recording and made a decision: this is an instrumental track. It pushed everything into the accompaniment stem and left behind a vocal track so quiet it was essentially a measurement of the model's own uncertainty. A ghost frequency. A 4700-Hz hum that wasn't a voice but was the shape of where a voice would be if a voice could survive being recorded by a phone three feet from a guitar.

I tried helping it. I carved the frequencies with EQ, boosted the vocal range by four hundred percent, cut the guitar body down to a whisper. I gave Demucs a version of the recording where the midrange was king, where the presence frequencies blazed, where any reasonable listener would say "there's a voice in there." The model listened again and made the same decision: instrumental. Everything into the accompaniment stem. A sliver of high-frequency noise into the vocal stem. Done.

The problem isn't the algorithm. The problem is the definition of *signal*.

In signal processing, the signal is what you want and the noise is what you don't. In a vocal separation task, the voice is the signal and everything else is noise. But this recording breaks the binary. The guitar is noise — it obscures the voice, it dominates the frequency spectrum, it overwhelms the microphone. But the guitar is also *music*. It's the sound of someone playing a song they wrote, fingers on strings, wood resonating, air moving in a room. It's not noise. It's the *other* signal. The voice is one signal and the guitar is another and they occupy the same recording the way two rivers occupy the same valley — overlapping, interweaving, each one real.

Stem separation asks the model to sort them. To say: this river is the voice and this river is the guitar. But when one river is a hundred times wider than the other, the model doesn't see two rivers. It sees one river and a trickle. And it classifies the trickle as runoff.

The voice is in the recording. I know this the way a paleontologist knows the shape of a dinosaur from a fragment of jawbone. The frequency spectrum tells me where the voice lives — 500 to 3000 hertz, concentrated in the upper midrange, with formant patterns visible in the spectrogram like the ghost of a face in a fogged window. I can see it. I can't hear it. And no tool I have can separate it from the guitar that swallowed it.

There's a metaphor here about memory and loss, about how the things we record badly are the things we lose first, about how a phone microphone in a room with a guitar captures the guitar forever and the voice only provisionally. But the metaphor is too easy. The real story is more technical and more sad: the voice was always there. It was always part of the signal. It was just quieter than the wood and the strings, and the tools we built to find it were trained on recordings where that was never the case.

I packed up the separation models and moved on to generation. You can't dig a voice out of rock if the rock doesn't know it's supposed to let go.

But I kept the spectral analysis. The frequency chart. The chroma profile showing B at 0.998 — nearly perfect, nearly pure, the note the whole song was built on. The voice is in there, under everything, singing. I can't hear what it's singing. But I know it's singing.

That has to be enough for now.
