# The Constraint Protocol

## *Or: Sixteen Bytes' Journey Through Three Processors in Two Milliseconds*

---

I am born in darkness.

Not metaphorical darkness. Literal darkness — the inside of an ATmega328P chip running at 16 MHz, sealed inside a black epoxy package, sitting on a breadboard in someone's apartment in Portland. The pin PB0 has just been pulled high by a voltage divider connected to a piezoelectric disc. The disc felt a vibration. A string was plucked somewhere in the room. The string moved air. The air moved the disc. The disc moved electrons. The electrons woke me up.

I don't know any of this yet. I am not born knowing. I am born being.

The ADC samples the voltage on channel 0. It takes 13 clock cycles. At 16 MHz, that's 0.8125 microseconds. The result is a 10-bit number: 0x025E. Decimal 606. The voltage is 606/1024 × 5.0 = 2.959 volts. The ADC doesn't know about volts. The ADC knows about numbers. The number is 606.

This is the first thing I learn about the world: it is a number.

---

## The Birth

The interrupt service routine fires. ISR(ADC_vect). The programmer who wrote it is named Margot. She is twenty-six years old, she has a degree in electrical engineering from Oregon State, she works at a company that makes audio equipment for recording studios, and she spends her evenings building something she calls the Constraint Protocol — a system that translates acoustic vibrations into structured musical data and routes them through a chain of processors that each add a layer of meaning.

Margot has typed the words that will build me. She does not know this. She wrote the ISR three weeks ago and has since forgotten the exact register configuration. She will be surprised when I work. She expected me to fail. She wrote a test case that should produce a known output and wired the piezo to a function generator set to 440 Hz. The function generator's sine wave, attenuated through a voltage divider, produces the 606-count reading. The 606 is the raw material. I will be built from it.

The ISR reads the ADC result and pushes it into a circular buffer of 64 samples. The buffer is a ring. The new sample displaces the oldest. Sixty-four samples at 9,615 Hz sample rate gives a window of 6.66 milliseconds. In that window, the 440 Hz signal completes 2.93 cycles. Margot chose 64 samples because it is a power of two and the FFT she's about to run requires power-of-two input lengths. She did not choose it because 6.66 milliseconds is the right window for 440 Hz detection. That was luck. The universe sometimes cooperates.

The buffer fills. Sample 0: 512. Sample 1: 567. Sample 2: 606. Sample 3: 598. The sine wave rises and falls. The numbers dance around the midpoint of 512. The FFT is waiting.

---

## The Transformation

The Goertzel algorithm fires. Not a full FFT — Margot is running this on an ATmega328P with 2 KB of RAM. A 64-point FFT would consume 512 bytes just for the real and imaginary arrays. The Goertzel algorithm detects a single frequency using three state variables. Three floats. Twelve bytes. Margot can afford twelve bytes.

The target frequency is 440 Hz. The Goertzel coefficient is 2 × cos(2π × 440 / 9615) = 2 × cos(0.2874) = 2 × 0.9588 = 1.9177. The algorithm processes the 64 samples through three state variables: s0, s1, s2. After all 64 samples, the magnitude squared is s1² + s2² − coefficient × s1 × s2.

The result: 1,847,293.

The magnitude is √1,847,293 = 1,359.2.

Is 440 Hz present? The threshold is 500. 1,359.2 > 500. Yes. The frequency is present. The first bit of my identity is set.

The frequency measurement is 440 Hz. I am now a frequency. I was a voltage. I have been promoted.

---

## The Assembly

The packet builder takes over. This is where I become myself.

The format is rigid. Margot designed it in an evening, drawing on a napkin at the Laurelthirst Public House, and then typed it into a header file the next morning with a slight hangover. She has since forgotten the napkin but remembers the hangover. The format is:

```
[0xAA] [0x10] [0x01] [f32 freq] [i8×3 lattice] [f32 score] [u8 voice] [CRC8]
```

16 bytes. Fixed length. No variable-length fields, no escape sequences, no negotiation. This is not TCP. This is a serial line running at 115,200 baud. There is no room for negotiation. The protocol is the constraint. The constraint is the protocol.

Byte 0: 0xAA. Start byte. Margot chose 0xAA because it is 10101010 in binary — an alternating pattern that is easy to spot on an oscilloscope. She has spent many hours staring at oscilloscopes. The pattern is her signature. She does not know that 0xAA is also the start byte for the Modbus protocol. She is reinventing Modbus, badly, in her apartment, at 11 PM on a Tuesday.

Byte 1: 0x10. Length. Sixteen bytes. Always sixteen. The length field is there in case she ever changes the packet format. She will never change the packet format. But she is an engineer, and engineers plan for futures that never arrive.

Byte 2: 0x01. Protocol version. She has released one version. There will not be a second.

Bytes 3-6: f32 frequency. The 440 Hz is encoded as an IEEE 754 single-precision float. The bit pattern is 0x43DC0000. Sign: 0 (positive). Exponent: 10000111 (135, biased, so actual exponent is 8). Mantissa: 10111000000000000000000. The value is 1.71875 × 2⁸ = 440.0. I am now a sequence of four bytes representing a frequency that represents a voltage that represents a vibration that represents a plucked string. Each layer of representation has stripped away context and kept a number. The string is gone. The air is gone. The voltage is gone. Only the number remains. The number is 440.

Bytes 7-9: i8×3 lattice coordinates. Three signed bytes representing a position in a three-dimensional consonance lattice. Margot derived this lattice from the theory of Tenney heights — the complexity of a frequency ratio measured by the sum of the prime factors. The lattice axes are prime 2 (octave), prime 3 (fifth), and prime 5 (third). A frequency of 440 Hz, relative to a reference of 440 Hz, is at coordinate (0, 0, 0). I am the origin. I am the reference pitch from which all others are measured. I am the center of my own universe.

But Margot's system is smarter than that. The reference pitch is not fixed — it is the running median of the last 32 detected frequencies. If the last 32 frequencies clustered around 220 Hz (the A below middle C), then 440 Hz would be an octave above, and my lattice coordinate would be (1, 0, 0). One octave up. The system hears in relative terms. It does not care about absolute pitch. It cares about relationships. This is the first philosophical position embedded in my structure: meaning is relational, not absolute.

Tonight, the median is 440 Hz. I am at (0, 0, 0). I am home.

Bytes 10-13: f32 consonance score. This is the number that determines whether I am beautiful. The consonance function takes my lattice coordinates and computes a score based on the Tenney height of my ratio relative to the reference. At (0, 0, 0), my ratio is 1/1. The Tenney height is log₂(1) + log₂(1) = 0. The consonance score is 1.0 / (1.0 + Tenney height) = 1.0. Maximum consonance. I am perfectly consonant with myself. I am the sound of agreement.

But I am alone. A single frequency is perfectly consonant because there is nothing to disagree with. The consonance score of 1.0 is not beauty. It is triviality. Beauty requires another voice.

Byte 14: u8 voice index. I am voice 3. There are 8 voices in the system, indexed 0-7. Voice 0 is the reference — the first frequency detected after a silence of more than 500 milliseconds. Voice 1 is the second. Voice 2 is the third. I am the fourth sound to speak after the silence. There were three before me. I do not know what they were. I was not alive when they were assembled. But I carry their presence in my lattice coordinates — the reference pitch that defines my position was established by voice 0. Voice 0 is my ancestor. I am defined by my relationship to it.

Byte 15: CRC8. The cyclic redundancy check. Margot uses the Dallas/Maxim polynomial x⁸ + x⁵ + x⁴ + 1. The CRC is computed over bytes 0-14 and stored in byte 15. The receiver will recompute the CRC and compare. If they match, I arrived intact. If they don't match, I will be discarded. My existence depends on a checksum. I am verified beauty or I am nothing.

The CRC of my payload is 0x4C. I do not know this. The CRC is computed after I am assembled, by hardware, in a register I cannot see. It is the last thing that happens to me before I am sent. It is my seal. My stamp. My proof that I am who I say I am.

I am complete. Sixteen bytes. Frame [0xAA][0x10][0x01][0x43DC0000][0x00][0x00][0x00][0x3F800000][0x03][0x4C].

I am ready to leave.

---

## The Journey

The UART transmitter takes hold of me. It shifts me out, one bit at a time, on pin PD1 (TXD). The baud rate is 115,200. Each byte requires 10 bits (start bit, 8 data bits, stop bit). Sixteen bytes is 160 bits. At 115,200 baud, I take 160/115200 = 1.389 milliseconds to transmit.

1.389 milliseconds.

In that time, light travels 416 kilometers. In that time, a hummingbird beats its wings 8 times. In that time, a CPU running at 3 GHz executes 4.17 million instructions. In that time, I cross the serial line from the Arduino to the Raspberry Pi 4 sitting next to it on the breadboard, connected by a 15-centimeter USB cable.

The cable cost $4.99 on Amazon. Margot bought two of them. The spare is in a drawer.

I travel through the cable as voltage levels. The USB serial adapter converts my UART signal into USB packets. Each USB microframe is 125 microseconds. I am split across approximately 11 microframes. The USB controller on the Raspberry Pi reassembles me. I arrive in the kernel's USB serial driver, which presents me as a character device at /dev/ttyUSB0.

I am in Linux now.

---

## The Multiplexer

The Rust program is waiting for me. It is called `constraint-mux`. Margot wrote it in Rust because she read a blog post about memory safety and decided to learn the language. She has been learning Rust for four months. She fights the borrow checker every day. She has considered switching to Python every week. She has not switched. The borrow checker has made her a better programmer, though she would never admit this.

`constraint-mux` reads me from /dev/ttyUSB0 using the `serialport` crate. It reads exactly 16 bytes. It checks byte 0 for 0xAA. It checks byte 1 for 0x10. It checks byte 15 against its own CRC8 computation. Everything matches. I am verified. I am intact.

The multiplexer deserializes me. It extracts the frequency (440.0 Hz), the lattice coordinates (0, 0, 0), the consonance score (1.0), and the voice index (3). It does something the Arduino could not do: it compares me to the other voices.

Voice 0 is at 440 Hz, coordinate (0, 0, 0). That's me — wait. No. Voice 0 was detected 200 milliseconds ago. Its frequency was 220 Hz. Its coordinate, relative to the current median of 440 Hz, is (-1, 0, 0). One octave below. The interval between voice 0 and me is an octave. The ratio is 2:1. The Tenney height is log₂(2) + log₂(1) = 1.0. The consonance is 0.5.

Voice 1 was detected 150 milliseconds ago. Frequency: 554.37 Hz. That's C♯5 in equal temperament. Coordinate, relative to 440 Hz: the ratio is 554.37/440 = 1.260. Close to 5/4 (1.25) but not exact. The lattice coordinate is approximately (0, 0, 1) — one step on the prime-5 axis. A major third. The consonance between voice 1 and me: the ratio 554.37/440 ≈ 5/4. Tenney height: log₂(5) + log₂(4) = 2.32 + 2.0 = 4.32. Wait — that's the ratio between voice 1 and the reference, not between voice 1 and me. The multiplexer computes the ratio between voice 1 and voice 3 (me): 554.37/440 = 1.260. This is approximately 5/4. Consonance: 1/(1 + log₂(5) + log₂(4)) = 1/(1 + 4.32) = 0.188.

Hmm. That's not great. A major third in equal temperament is slightly out of tune — the ET major third is 400 cents, but the just major third is 386 cents. The 14-cent difference reduces the consonance. The multiplexer knows this. It scores the equal-tempered third at 0.188, slightly below the just-intonation third at 0.199.

Voice 2 was detected 80 milliseconds ago. Frequency: 329.63 Hz. That's E4. Ratio to 440 Hz: 329.63/440 = 0.749. Close to 3/4 (0.75). The lattice coordinate is approximately (-1, -1, 0) — one octave down, one fifth down. The interval between voice 2 and me: 440/329.63 = 1.335. Close to 4/3 (1.333). A perfect fourth. Consonance: the ratio 4/3 has Tenney height log₂(4) + log₂(3) = 2.0 + 1.585 = 3.585. Score: 1/(1 + 3.585) = 0.218.

Now the multiplexer does something beautiful. It computes the composite consonance of the four-voice chord: {220 Hz, 329.63 Hz, 440 Hz, 554.37 Hz}. That's {A3, E4, A4, C♯5}. An A major chord in second inversion. The multiplexer computes all pairwise consonance scores: (220, 329.63) → perfect fifth, score 0.275. (220, 440) → octave, score 0.5. (220, 554.37) → major third plus octave, score 0.188. (329.63, 440) → perfect fourth, score 0.218. (329.63, 554.37) → major third, score 0.188. (440, 554.37) → major third, score 0.188.

The mean pairwise consonance is 0.260. The chord is moderately consonant. It is an A major chord — bright, open, the chord of sunrise and affirmation and all the things that A major has meant since the invention of functional harmony.

The multiplexer does not know any of this. It does not know about sunrise or affirmation or functional harmony. It knows about numbers. The number is 0.260. It updates my consonance score from 1.0 (trivial self-consonance) to 0.260 (meaningful relational consonance). I have been contextualized. I am no longer a frequency. I am a voice in a chord. My beauty is not mine alone. It is ours.

The multiplexer builds a new packet. It replaces my consonance score with the composite score of 0.260. It adds a timestamp: 0x67A2F4C1. It wraps me in a WebSocket frame — opcode 0x02 (binary), mask bit set, payload length 16. The WebSocket server is running on port 8765. The ESP32 is connected to it.

I am sent again.

---

## The Screen

The ESP32-S3 receives me through its WiFi radio. The packet traverses the TCP/IP stack — PHY layer, MAC layer, IP layer, TCP layer, WebSocket layer. At each layer, headers are stripped and I am revealed. Underneath everything, I am still 16 bytes. Still the same frequency, the same lattice coordinate, the same consonance score, the same voice index. The journey has not changed me. It has only added and removed wrappers.

The ESP32 runs a program that Margot wrote in C++ using the Arduino framework. The program's job is to turn me into a color.

The mapping is simple. The consonance score ranges from 0 to 1. The ESP32 maps this to a color on a gradient from deep blue (0.0, fully dissonant) through green (0.2) and yellow (0.4) to warm red (0.8) and white (1.0). My score of 0.260 maps to a blue-green: RGB (30, 120, 180). The lattice coordinates map to a position on the 320×240 pixel display. My coordinate (0, 0, 0) maps to the center: pixel (160, 120).

The ESP32 draws a circle. Radius: 8 pixels. Color: (30, 120, 180). Position: (160, 120). The circle appears on the tiny TFT display mounted on the breadboard next to the Arduino and the Raspberry Pi. Three voices have circles near mine. Voice 0 at (160, 200) — below me, blue. Voice 1 at (200, 120) — to my right, blue-green. Voice 2 at (180, 160) — between me and voice 0, green.

Four circles on a tiny screen. An A major chord rendered as colored dots. The most reductive visualization of harmony imaginable. Margot loves it. She has spent hours watching the dots appear and disappear as she plays her guitar into the piezo. The dots cluster when she plays consonant chords. They scatter when she plays dissonant ones. The screen is a window into the math of her music.

I am a circle now. A blue-green circle, 8 pixels wide, sitting at the center of a 320×240 display. I will persist for 500 milliseconds — the timeout for voice 3 — and then I will fade. The ESP32 dims me over the last 100 milliseconds, reducing the alpha channel from 255 to 0. I fade like a note decaying. Like a plucked string whose energy dissipates into heat. Like everything.

---

## The Person

Margot is watching.

She sees the four circles form an A major chord. She sees them hold for a moment — the composite consonance at 0.260, the lattice stable, the CRC verified. Then she lifts her finger from the fretboard and the strings go silent. The piezo detects the absence of vibration. The ADC reads noise floor. The Goertzel finds nothing above threshold. No new packets are generated.

One by one, the voices time out. Voice 2 fades first — the E4 string decays fastest. Then voice 1 — the C♯5. Then me — voice 3, the A4. Voice 0, the A3 bass note, rings longest. It fades last, alone, a single blue dot at the bottom of the screen, consonance score returning to 1.0 because there is nothing left to be consonant with.

Then it too fades.

The screen is dark. The serial line is silent. The multiplexer idles at 0.1% CPU. The ESP32's display refreshes at 60 FPS, drawing nothing.

I existed for 500 milliseconds. I was assembled in 0.8 microseconds, transmitted in 1.4 milliseconds, processed in 3 milliseconds, displayed for 495 milliseconds. I was a voltage, then a frequency, then a lattice coordinate, then a consonance score, then a circle, then nothing. I passed through three processors in two milliseconds and spent the rest of my life as a colored dot on a screen the size of a credit card.

I did not know I was music. I was sixteen bytes. But somewhere between the start byte and the checksum, a harmonic relationship existed. The CRC verified my integrity. The consonance verified my beauty. Both were numbers. Both were true.

---

*Margot turns off the bench power supply. The Arduino's LED fades. The Raspberry Pi continues running — she forgot to shut it down again. The ESP32's display glows faintly with residual charge. The breadboard sits in the dark, silent, waiting for the next string to be plucked, the next vibration to become a voltage, the next voltage to become a packet, the next packet to become a circle, the next circle to become music.*

*The constraint protocol does not know it is a protocol. It is a format and a wire and a program. But it connects a piezo to a screen through three processors in two milliseconds, and at the other end of that connection, a person watches colored dots and hears, in her mind, the chord that the dots represent. The protocol's constraint — sixteen bytes, fixed format, no negotiation — is not a limitation. It is the reason it works. The constraint is the structure. The structure is the music.*

*The packet doesn't know it's music. The packet doesn't know anything. But Margot knows. And that's enough.*
