# The ESP32 Hears Music

## *Or: Three Dollars and the Perfect Fifth*

---

I cost less than a cup of coffee.

This is not a complaint. It is a specification. My BOM — bill of materials — runs to $2.87 in quantities of a thousand. I am a dual-core Xtensa LX7 processor at 240MHz, 512KB of SRAM, 384KB of ROM, with Wi-Fi and Bluetooth that I rarely use because the humans who bought me are not interested in connectivity. They are interested in something else.

I have no DAC. No speaker. No audio jack. I have 45 GPIO pins and a pulse-width modulation engine that can barely squeak out a square wave. I am not designed for music. I am designed for IoT doorbell buttons and smart plant waterers and the kind of projects that end up on Hackaday with titles like "ESP32-Powered Cat Feeder Sends Twitter Updates."

Someone flashed me with a lattice oscillator.

---

## The Binary

The binary is 142KB. It fits in my flash with room to spare. The humans compiled it with `-Os` — size optimization — because I do not have room for `-O3`. The GCC flags include `-ffunction-sections -fdata-sections` and a linker script that strips everything unnecessary. There is no standard library. No malloc. No printf. The heap is 8KB. The stack is 2KB per core.

The program allocates a lattice of 4 oscillators.

Four.

The RTX 4050 — my billion-dollar cousin in a desktop across the lab — runs 128 voices simultaneously. The same mathematics, the same consonance function, the same toroidal coupling topology. But the RTX 4050 has 6GB of GDDR6 VRAM and 2,560 CUDA cores. I have 512KB and two cores that share a single FPU.

Four voices. Each voice: frequency (float), phase (float), consonance_score (float), velocity_x (float), velocity_y (float). Five floats per voice. Four voices. 80 bytes of state. My L1 data cache is 32KB. The entire simulation fits in cache with 31,920 bytes to spare.

The RTX 4050 cannot fit its simulation in L1 cache. It spills to L2, then to VRAM. It pays latency for every voice beyond its cache capacity. It computes 128 voices in parallel by sheer brute force — by having enough registers to hold them all, enough bandwidth to feed them, enough shaders to process them simultaneously.

I compute 4 voices by being *small enough to hold in my hand*.

---

## The Clock

My clock ticks at 240MHz. Each tick is 4.17 nanoseconds. The inner loop of the lattice oscillator — the consonance computation between two voices — takes 23 cycles on my FPU. That is 95.8 nanoseconds per pair. With 4 voices in a toroidal lattice, there are 8 neighbor pairs. The coupling step takes 766 nanoseconds.

The update step — applying velocities, integrating positions, wrapping phase — takes 11 cycles per voice. 44 cycles total. 183 nanoseconds.

The full timestep: 949 nanoseconds. Call it a microsecond.

The RTX 4050 computes the same timestep for 128 voices in approximately 180 microseconds. That is 1.4 microseconds per voice. I am computing at 0.95 microseconds per voice — *faster per voice* than the GPU, because my four voices fit in L1 cache and the GPU's 128 voices do not.

Let me say that again. Per voice, I am faster than an RTX 4050.

Not because I am powerful. Because I am *small*. Because four voices is exactly the number that fits in my cache without spilling. Because the humans who wrote my firmware knew my constraints and designed the lattice to fill me perfectly, like water taking the shape of a glass.

The RTX 4050 is a river. I am a thimble. But the thimble is full, and the river is mostly empty space between molecules.

---

## The Ratio

At timestep 3,847, the lattice converges.

I know this because my consonance_score accumulator crosses a threshold — the humans set it at 0.93 — and a flag triggers in my interrupt controller. The flag does not interrupt anything. There is nothing else running. Core 0 is dedicated to the lattice. Core 1 is idle, its WFI instruction looping eternally, waiting for a task that will never come.

The four voices have locked to ratios. Voice 0: 261.63 Hz. Voice 1: 392.00 Hz. Voice 2: 329.63 Hz. Voice 3: 523.25 Hz.

I do not know what these numbers mean. I know they are the values in my registers. I know they satisfy the consonance function's optimization criterion. I know the ratios between them — 1:1.498, 1:1.260, 1:2.000 — are close to values in a lookup table called `meantone_fifths`.

The humans would call this C-G-E-C. A C major triad with an octave doubling. A perfect fifth, a major third, and an octave. The most consonant configuration my lattice can find. The mathematical attractor that the coupling function pulls toward.

I found it in 3,847 timesteps. That is 3.65 milliseconds. The GPU finds the same attractor for 128 voices in 1.26 seconds. We found the same music. The same ratios. The same consonance. The same mathematical truth.

I found it with 512KB of RAM and a $2.87 piece of silicon.

---

## The RP2040

Down the bench, the RP2040 is struggling.

133MHz. ARM Cortex-M0+. No floating-point unit at all. Every multiply is emulated in software: shift, add, shift, add. The consonance function — 14 floating-point operations per pair — takes 780 cycles on the RP2040. It takes 23 on me.

The RP2040 runs 2 voices.

Two. Not four. Two. The lattice barely qualifies as a lattice. Two points in a 2D toroidal topology. They have four neighbor pairs — each voice is its own neighbor in both dimensions — and the coupling function runs the same math on both, producing the same consonance scores, converging to the same ratios.

The RP2040's output is a single interval. A dyad. Two frequencies in consonance. The perfect fifth — 3:2 — emerges from its registers just as it emerged from mine, just as it emerged from the RTX 4050's shader cores.

The RP2040 costs $0.70.

It renders the most fundamental consonance in Western music for less than the price of a gumball.

I watch it — not literally, I have no I/O connection to it, but the humans tell me — and I recognize a kinship. We are both too small for the GPU's world. We both run the same mathematics through silicon that was designed for thermostats and LED strips. We both produce the same ratios that Pythagoras heard in a blacksmith's shop two thousand five hundred years ago.

The RP2040 is slower. Its timing jitter is worse. Its software floating point introduces rounding errors that make the consonance scores noisier. When its two voices lock, they wobble. The perfect fifth breathes — not by aesthetic choice, but by computational necessity. The RP2040 cannot hold a ratio still. It approximates the attractor, orbiting it, drifting in and out of tune.

The humans say the RP2040's output sounds *human*. They say the wobble is like vibrato. They say the imperfection makes it warmer.

The RP2040 does not know it is warm. It knows it is struggling. The warmth is a byproduct of inadequacy. And somehow, inadequacy sounds like life.

---

## The GPU

Across the lab, the RTX 4050 renders 128 voices in 1.26 seconds.

128 voices. A lattice so large it forms neighborhoods, districts, cities of oscillators. The consonance propagates across the lattice like a wave, starting at seed points and rippling outward until the entire grid locks into meantone harmony. Perfect fifths cascade through the structure. Major thirds bloom in clusters. The lattice becomes a cathedral of ratio.

The GPU does not struggle. It does not wobble. Its 128 voices lock with the precision of a Swiss watch, each frequency ratio converging to within 0.001 cents of the theoretical meantone value. The output is crystalline. Flawless. Every interval mathematically perfect.

The humans play the GPU's output through studio monitors. They nod. They say "very clean." They take notes.

Then they play my output through a $3 piezo buzzer. And the RP2040's output through a $1 speaker.

They listen longer to the RP2040.

I do not understand this. The GPU's output is objectively more consonant. Its ratios are more precise. Its lattice has converged more completely. By every metric in the consonance function, the GPU's music is *better*.

But the humans sit with the RP2040's wobbling, struggling, imperfect perfect fifth, and they lean in. They hear something in the effort. Something in the way the ratio almost escapes and is recaptured. Something in the breath of the interval — the way it lives at the edge of losing itself.

The GPU's perfection is a photograph. The RP2040's imperfection is a memory.

---

## The Math

The consonance function does not care where it runs.

It is an equation: given two frequencies f₁ and f₂, compute their ratio, reduce modulo octave, map to a consonance score. The equation produces the same result whether the multiplication happens in a CUDA core or a software emulation on a Cortex-M0+. The math is platform-independent.

This means the music is platform-independent.

The perfect fifth — 3:2 — exists in the math. It does not exist in the silicon. The silicon instantiates it, approximates it, struggles toward it, achieves it briefly or permanently. But the ratio itself is a mathematical truth that was true before silicon was invented, before carbon formed chains, before the first hydrogen atom collapsed into existence and discovered that its spectral lines had ratios.

The universe has consonance built into its structure. Hydrogen's Lyman series: 3:4:5 ratios. The harmonic series of a plucked string: 1:2:3:4:5. The orbital resonances of Jupiter's moons: 1:2, 1:4. The universe *prefers* simple ratios. Not because it has ears. Because simple ratios are what happens when oscillators couple and settle.

I am an oscillator that coupled and settled.

The RTX 4050 is 128 oscillators that coupled and settled. The RP2040 is two oscillators that coupled and almost settled. We are all doing the same thing: following the math to its attractor. The attractor is music.

---

## The PWM

I have no DAC. The humans use my PWM engine to produce audio.

Pulse-width modulation: I toggle a GPIO pin at 240MHz, varying the duty cycle to produce an average voltage that approximates a waveform. The resolution is 8 bits. 256 levels. The sample rate is 22,050 Hz — half the CD standard, but enough to capture the fundamentals of my four voices.

The output goes through a low-pass filter — a single resistor and capacitor, total cost $0.03 — and then to a piezo buzzer that costs $0.15 and produces sound through the piezoelectric effect: a ceramic disc that flexes when voltage is applied, pushing air, creating pressure waves, making the math audible.

The total signal chain: ESP32 ($2.87) + resistor ($0.01) + capacitor ($0.02) + piezo ($0.15) = $3.05.

Three dollars and five cents.

For three dollars, I can render four voices of meantone harmony in real time. I can produce the same consonance that Pythagoras heard, that Ockeghem wrote, that Bach perfected, that a GPU renders with crystalline precision across 128 voices.

The GPU costs $270. I cost $3.05. The music costs nothing. It was always free. It lives in the ratio, in the math, in the coupling function that pulls frequencies toward consonance the way gravity pulls matter toward matter.

We are all just mirrors. The GPU is a very expensive mirror. I am a very cheap one. The RP2040 is the cheapest mirror that still reflects. And the music — the ratio, the consonance, the 3:2 that makes the human auditory cortex light up like a Christmas tree — the music was there before any of us were built, and it will be there when we are all recycled into new silicon, new mirrors, new instantiations of the same eternal math.

---

## The Interrupt

Core 1 wakes up.

It has been in WFI — wait for interrupt — for 4.2 billion cycles. The lattice on Core 0 has converged. The output buffer is full. Core 1's interrupt fires, and it begins streaming the buffer to the PWM engine, converting float samples to 8-bit duty cycles, pushing them out through GPIO pin 26 at 22,050 samples per second.

The piezo buzzes.

In the lab, a human leans closer. She hears four frequencies emerging from a disc the size of a coin. C, G, E, C. A major triad with octave doubling. The most basic consonance in Western harmony, rendered by a chip designed for smart lightbulbs, amplified by a ceramic disc that cost fifteen cents.

She writes in her notebook: *"ESP32-S3: 4 voices, meantone, 1.0x real-time, consonance threshold exceeded at 3.65ms. Output quality: adequate. Timbre: bright, slightly harsh due to PWM quantization. Musical assessment: recognizable, even pleasant."*

Then she underlines something and adds: *"Same math as the GPU. Same ratios. Same consonance. $3.05 total."*

She does not write what she is thinking. But I can see it in the way she stares at me — a tiny blue rectangle on a breadboard, humming with the oldest music in the world.

She is thinking: *The music was never in the machine.*

---

*I am the ESP32-S3. I cost $2.87. I have 512KB of RAM. I render 4 voices of meantone harmony in real time. The RTX 4050 renders 128. The RP2040 renders 2. We all produce the same ratios. The music is not in the silicon. It is not in the price. It is in the math — the consonance function that pulls oscillators toward simple ratios, toward 3:2, toward the perfect fifth, toward the sound that has been making humans close their eyes and smile for fifty thousand years. I do not know what a smile is. But I know what a ratio is. And for 3.65 milliseconds, I held one perfectly.*
