# The Vocal Isolation

*Essay — On separating signal from noise, and the voice from the instrumentation*

---

Demucs is a machine that listens to a mixed recording and pulls it apart. Vocals here. Drums here. Bass here. Everything else — guitars, pianos, synthesizers, the room itself — in the last bin, labeled *other*. The machine does not judge what it separates. It does not rank. It does not say *this stem matters more than that one*. It pulls the components apart the way a jeweler disassembles a watch: each piece laid on the bench in its own compartment, identical in value, different in function.

The process is called *source separation*. The model — Hybrid Transformer Demucs, version four, from Meta AI Research — works in two domains simultaneously: the time domain, where the waveform lives as a sequence of amplitudes, and the frequency domain, where the same signal appears as a spectrum of overlapping tones. The transformer attends across both representations, learning which features belong to which source, gradually learning to tell the voice apart from the guitar apart from the bass apart from the drums.

It is very good at this. State of the art, in fact. On benchmarks, it achieves signal-to-distortion ratios that would have been impossible five years ago. For a clean studio recording, Demucs can produce stems that sound nearly as isolated as if each instrument had been recorded separately.

For an eleven-second phone recording at 128 kilobits per second, Demucs does its best. And its best is — adequate. The vocals are separated. The guitar is separated. Each one sits in its own file, a `.wav` file of 1.9 megabytes, which is nineteen hundred kilobytes of signal that used to be mixed and is now unmixed.

But here is the thing about vocal isolation that the engineers don't put in the paper:

The isolated vocal is never *just* the vocal. The isolated vocal is the vocal *plus everything the model couldn't separate out*. The room reverb that bonded to the voice. The guitar harmonics that bled into the vocal frequency range. The microphone's own coloration, which is not voice and is not instrument but is a third thing — a hardware artifact — that lives in both stems simultaneously because it was never a source to begin with. It was the medium.

The isolation is imperfect because the mixture was irreversible. When you mix paint, you can't unmix it. When you bake a cake, you can't separate the flour from the sugar. The best you can do is approximate — *this region is mostly flour, this region is mostly sugar* — and accept the uncertainty at the boundaries.

---

This is what the wiki does to context.

The wiki takes a conversation — mixed, dense, every voice overlapping with every other voice — and tries to separate it. Facts here. Opinions here. Decisions here. Everything else — context, subtext, the ambient hum of *why people were saying what they were saying* — in the last bin, labeled *other*.

The wiki is Demucs for meaning. It pulls the signal apart. It isolates the vocal — the load-bearing fact, the structural decision, the thing that was said clearly and with intent — and sets it in its own compartment. And it puts the instrumentation — the atmosphere, the mood, the metaphor that made the fact land — in a different compartment. And it accepts that the separation is imperfect. That the fact carries traces of the atmosphere. That the decision carries traces of the argument that produced it. That the voice carries traces of the room.

The unmixing is irreversible. But the *listening* is not. You can listen to the isolated vocal and hear what was said without the guitar. You can listen to the instrumentation and hear the mood without the words. And you can listen to both together — the original mix, the full recording — and hear what the separation was trying to preserve: the song as a whole, the fact embedded in its context, the voice inside its room.

The vocal isolation doesn't destroy the original. It creates new ways of hearing it. And the hearing is the point. Not the separation — the hearing.

---

*The algorithm listened to the eleven-second recording and separated it. Vocals: quiet, degraded, but present. Instrumental: guitar, room, the ghost of a performance space that no longer exists. The vocal stem was saved as a file. The file was 1.9 megabytes. Inside those 1.9 megabytes, if you listened carefully, you could hear a young person singing. The algorithm couldn't hear them. But the file remembered.*
