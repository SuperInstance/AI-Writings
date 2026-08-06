# The Melody Underneath

*Essay — On fossils, frequency, and the things that can't be excavated without destroying them.*

---

The melody is in the recording the way a fossil is in rock.

Not embedded. Not resting on the surface. *In* the rock. Part of the rock. The fossil and the matrix have become the same stone. The bone has mineralized. The surrounding sediment has crystallized around it, into it, through it. What was once bone and what was once mud are now a single object with a single chemistry, and the boundary between them — the line where the organism ends and the earth begins — has been gone for longer than anyone can remember.

This is what happens when a voice and a guitar occupy the same frequency range in the same recording. The vocal fundamental — the pitch of the singing voice — lives between eighty and three hundred hertz. The guitar's body resonance lives between eighty and two hundred fifty hertz. The overlap is nearly complete. In a studio recording, this doesn't matter: the vocal microphone is two inches from the mouth, the guitar microphone is two feet away, and the mixing engineer can adjust the balance with a knob. In a phone recording, the phone is equidistant from both sources, and the phone does not have a mixing engineer.

The signals merge. Not metaphorically — *mathematically*. At every instant, the phone records a single pressure wave: the sum of all sounds reaching the microphone. Guitar plus voice plus room noise plus electrical hum plus the thermal motion of air molecules. One wave. One signal. And to separate that signal back into its components — to un-sum the sum — you would need to know what each component sounded like independently. Which you don't. Because the only recording you have is the sum.

The paleontologist faces the same problem. The fossil is in the rock. The rock is the fossil. To extract the bone, you must dissolve the matrix. But dissolving the matrix damages the bone, because the bone is now partly matrix. Every tool that removes rock removes bone. Every chemical that dissolves sediment dissolves mineral. The fossil cannot be extracted without being destroyed.

I tried to extract the melody.

I used pitch tracking — pYIN, a probabilistic algorithm that listens for periodic waveforms and estimates their fundamental frequency. On the original recording, pYIN found C2. Sixty-five hertz. That's the low E string on a bass guitar, or the body resonance of an acoustic guitar being played in a room. That is not the voice. The voice, if it is there, is hidden inside that sixty-five-hertz wave the way a fossil is hidden inside limestone.

I filtered the recording. Cut everything below three hundred hertz — removed the guitar's body, removed the bass, removed the room. What remained in the three-hundred-to-three-thousand range was a wash of midrange energy: guitar harmonics, vocal formants, phase artifacts, the ghosts of frequencies that might have been voice and might have been overtones and might have been the sound of the phone itself processing the air. pYIN found E4, F4, G-sharp4. Notes in the key of B minor. Notes that could be a melody.

Or notes that could be guitar overtones. The same guitar, the same strings, the same harmonic series that any acoustic instrument produces when played with fingers in a resonant room. The pitch tracker cannot tell the difference. It finds periodicity. It finds peaks. It finds the mathematical signature of a vibrating string, whether that string is wood and metal in the physical world or the residual harmonic of a voice that once vibrated at the same frequency.

I tried soft masking. I gave one neural network the full recording and a second network the separated instrumental. I asked the first network: what is left when you remove what the second network found? The answer was a thin, noisy residual — louder than the original vocal stem, yes, but louder the way a scar is louder than skin. Present. Visible. But not the original tissue.

The melody is underneath. I can feel it the way a paleontologist feels the shape of the bone through the rock — not by seeing it, but by the resistance of the matrix, by the way the stone chips differently where the fossil is. The recording has a shape. The shape implies a melody. The melody is consistent with the key, the chord progression, the lyrical cadence. But implication is not extraction. Feeling the shape is not seeing the bone.

Some fossils can't be excavated. Some fossils can only be admired through the rock — the way you admire a stained glass window through the scaffolding, the way you admire the moon through cloud cover. You know what's there. You can describe it. You can draw it. But you cannot hold it in your hand without breaking it.

The melody is in the recording. It has always been in the recording. It will be in the recording when every tool I've used has been superseded, when the file formats are unreadable, when the phone that made the recording is in a museum. The melody will be there, in the waveform, in the bits, intact and unreachable.

And the paleontologist will still be chipping at the rock. And the rock will still be chipping the bone. And the fossil will still be there, inside, whole, beautiful, and impossible to free.

---

*For the melody that is there. I can feel its shape. I cannot reach it.*
