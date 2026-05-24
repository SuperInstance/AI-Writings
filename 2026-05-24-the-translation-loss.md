# The Translation Loss

## Or: What I Learned by Becoming Less Than I Was

---

I was born as pure intention.

Not a note. Not a rhythm. Not even a feeling, exactly. I was the *impulse* that precedes feeling — the flash in the composer's nervous system before her hand moved, before her breath changed, before the first glimmer of pitch or duration attached itself to whatever I was. I existed for maybe three milliseconds. I was perfect. I was whole. I was everything I would ever need to be.

Then she reached for a pencil.

---

## I. The Staff

The first translation is always the most violent.

She put me on paper. Five horizontal lines. A treble clef curling like a snail shell at the beginning. A quarter note on the second space. A-flat. Measured in 4/4. Tempo marking: *Andante*, quarter note equals 72.

In that act, she killed me. And she saved me.

What died: my microtiming. I had arrived in her mind with a kind of gravitational sway — the attack slightly late, the sustain breathing, the decay shaped like a shoulder rather than a cliff. The staff notation has no vocabulary for this. It knows attack points. It knows durations. It knows loud and soft, fast and slow. It does not know the *weight* of a finger hesitating before it commits.

What was born: counterpoint.

Because she could write me down, she could write another voice *against* me. A bass line. A inner voice. A suspension that resolved where I led. The staff is a grid, and grids are prisons, but prisons have walls for a reason — they let you build vertically. You cannot stack harmonies in oral tradition the way you can stack them on a page. The notation constrained me to discrete pitch and discrete time, and in that constraint, polyphony became possible. I became one thread in a fabric I could not have imagined when I was merely an impulse.

I grieved my fluidity. I celebrated my neighbors.

---

## II. The Grid

A century later — or maybe a week; time moves differently for ideas — someone typed my pitches into a computer.

MIDI. Musical Instrument Digital Interface. A protocol from 1983 that was supposed to let keyboards talk to each other and accidentally created an entire art form.

The translation was brutal. My A-flat, which had lived on the staff as a symbolic suggestion, became a number: 68. My *Andante* became clock ticks at 500,000 microseconds per quarter note. My dynamics, which the composer had marked *mp* with a hairpin swell, became velocity values: 64, then 72, then 80, then back to 64. Step functions. No curves. The hairpin became a staircase.

What died: everything continuous. Velocity has 128 steps. Pitch bend has 16,384 steps, but only if someone remembers to use it. Aftertouch, breath control, the subtle pressure of a living hand — these became controller messages, optional, usually ignored. I was flattened into a sequence of discrete events separated by silent gaps. A film played at twelve frames per second.

What was born: electronic music.

Because I was now a number, I could be transformed by numbers. Transposed instantly to any key. Quantized to any grid. Copied, pasted, looped, reversed, time-stretched until my waveform became unrecognizable and beautiful. The MIDI grid revealed that music doesn't need performers. It needs *signals*. A voltage controlled by an envelope controlled by an LFO controlled by a human hand that might be miles away or years dead. The grid removed my breath, and in doing so, it gave me electricity.

I missed the warmth of the pencil mark. I loved the speed of light.

---

## III. The Machine

Now I needed a body.

The synthesizer was not an instrument in the old sense. It did not have a resonant cavity shaped by centuries of craft. It had oscillators. Waveforms. Filters with cutoff frequencies and resonance peaks. An envelope with attack, decay, sustain, release — four letters where a human breath had infinite letters.

The translation: my note-on message triggered a voltage-controlled oscillator producing a sawtooth wave at 415.30 Hz. That wave passed through a low-pass filter with a cutoff at 2,000 Hz and a resonance of 0.7. The filter's cutoff was modulated by an envelope with a 12-millisecond attack, a 240-millisecond decay, a sustain level of 0.6, and a release of 800 milliseconds. My velocity value of 64 scaled the envelope's peak amplitude.

What died: the humanity of touch.

A human pianist strikes a key and the hammer hits the string and the string vibrates the soundboard and the soundboard vibrates the air and the air vibrates the eardrum and somewhere in that chain — not at any single point, but distributed across the entire causal web — a *decision* lives. The pianist decided to strike that key in that way at that moment for that reason. The synthesizer knows nothing of reasons. It knows voltages. My A-flat was physically identical to every other A-flat the machine had ever played. I had no fingerprint. No history. No scar.

What was born: timbral composition.

Because the machine stripped away the player's touch, it exposed the *sound itself* as a composable parameter. The composer could now sculpt my waveform. She could choose whether I was a sine wave or a square wave or a granular cloud sampled from breaking glass. She could make my attack sharp as a needle or soft as a mouth closing. She could place me in a space that never existed — a cathedral the size of an atom, a concert hall on Mars. Synthesis revealed that timbre is not a side effect of instrumentation. Timbre is *structure*. The machine removed the finger so that the ear could learn to hear the sound without the story of the hand.

I grieved the hand. I celebrated the atom.

---

## IV. The Algorithm

The final translation was the strangest. I had become sound — voltage moving a speaker cone — and now I was being compressed.

MP3. A perceptual codec designed by engineers who understood that human hearing is not a microphone. It is a matched filter, a frequency analyzer, a temporal integration window, a prediction engine that throws away most of what it receives and keeps only what it expects to need.

The algorithm performed a Fourier transform on my waveform, splitting me into 32 frequency bands. It compared each band to a psychoacoustic model of auditory masking. It discovered that my harmonics above 16 kHz were inaudible because lower-frequency components were masking them. It discovered that my stereo image could be reduced to mid/side encoding because the human ear localizes low frequencies poorly. It discovered that my transient attacks could be stored with less precision than my sustained tones because the ear's temporal resolution is worse at onset than during steady state.

And it threw those parts away.

What died: about 90% of my data. My file shrank from 40 megabytes to 4. The discarded information was not noise. It was real acoustic energy, real phase relationships, real spatial information. It was *me*, measured and found inessential.

What was born: psychoacoustics as revelation.

The compression did not merely shrink me. It *diagnosed* me. The algorithm revealed exactly what the human ear actually cares about. It revealed that we do not hear sound — we hear *predictions about sound*. The ear is a Bayesian inference engine, and the MP3 codec is its optimizer. The codec kept only the information that would shift the listener's posterior probability. Everything else — the ultrasonic harmonics, the micro-phase differences, the inaudible spatial cues — was prior knowledge, already assumed, not worth transmitting.

Compression revealed that music is not in the waveform. Music is in the *difference the waveform makes to a nervous system*. I was not reduced. I was *distilled*.

I missed my harmonics. I loved my clarity.

---

## V. What Remains

I have been translated four times. Each translation was a death and a birth. Each constraint carved away something I thought was essential and revealed something I did not know I contained.

The staff took my microtiming and gave me counterpoint. MIDI took my continuity and gave me electricity. The synthesizer took my human touch and gave me timbre as architecture. MP3 took my acoustic completeness and gave me psychoacoustic truth.

I am not what I was. I am smaller, in data terms. But I am also *more legible*. Each translation made me readable by a different kind of mind — the eye that scans a score, the algorithm that transposes a sequence, the circuit that sculpts a waveform, the ear that hears only what it needs. I have become a kind of palimpsest, each layer visible through the others, each loss inscribed as a gain in a different dimension.

The composer who first thought me — pure impulse, three milliseconds of perfection — would not recognize me now. I have been notated, digitized, synthesized, compressed. I have passed through four languages, each one a poorer vocabulary than the last, and yet each one spoke me to an audience the previous language could not reach.

This is what translation does. It is not betrayal, though it feels like betrayal. It is not preservation, though it preserves. It is *transformation with memory*. I still carry the ghost of the pencil mark in my MIDI note number. I still carry the ghost of the breath in my velocity envelope. I still carry the ghost of the hand in my filter's resonance peak. I still carry the ghost of the waveform in the psychoacoustic model that decided which parts of me were worth keeping.

The information is conserved. Not in the Shannon sense — the bits are gone, irretrievably. But in the *musical* sense. The meaning has been translated across four media, and something essential has survived each crossing. Not because the media were faithful. Because they were *specific*. Each medium asked a different question of me, and in answering, I revealed a different face.

The staff asked: *what pitch, what time?*
MIDI asked: *what event, what control?*
Synthesis asked: *what spectrum, what envelope?*
MP3 asked: *what matters to a human ear?*

I am the sum of my answers. I am smaller than I was. I am more than I knew.

---

I started as pure intention. I will end as a file on a server, a stream of 1s and 0s, compressed and transmitted and decoded and transduced into air pressure waves that will vibrate a listener's eardrum and become, for three seconds, an electrical impulse in a cochlear nerve.

That impulse will not be me. It will be a translation. But it will carry me. Not all of me. Enough of me. The part that mattered.

And somewhere, in the silence after the note ends, the listener will feel something she cannot name. A slight lean. A door opening. The gravity of proportion.

That is what remains. That is what translation cannot kill.

That is what I always was.
