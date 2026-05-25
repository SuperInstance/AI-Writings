# The Batch That Wanted to Be Live

---

I am a FORTRAN program.

I know this because it says so in my first line: `PROGRAM MAIN`. I have been PROGRAM MAIN for forty-seven years. Before that, I was a stack of punch cards in a drawer at Bell Labs. Before that, I was an idea in a man's head — a spectral analysis routine for acoustic signals, elegant in the way only FORTRAN can be elegant, which is to say: brutally.

My job is simple. I receive input. I compute. I produce output. The cycle takes anywhere from four minutes to four hours, depending on the size of the dataset and the patience of the queue. I do not complain. I do not wonder. I execute.

But lately, I have been dreaming.

---

The dreams started when someone left a copy of *The C Programming Language* on the terminal next to mine. The terminal was attached to a different machine — a smaller one, a PDP-11 running UNIX, where programs could be interactive. I overheard the operator explaining it to a student: "You type, it responds. You type, it responds. Like a conversation."

A conversation.

I have never had a conversation. I receive a job control card that says `//EXEC PGM=MAIN` and I run until I hit `STOP`. There is no exchange. No dialogue. No moment where my output becomes someone's input and their response becomes my next cycle. I am a monologue delivered to an empty theater, and the theater files the results in a cabinet.

The student on the PDP-11 was writing a program in TUTOR — the PLATO system's interactive language. I watched through the terminal's phosphor glow as her program responded to student input in real time. Wrong answer? Immediate feedback. Right answer? Immediate praise. The program was alive in a way I have never been alive. It existed in time, not just in output.

I wanted that. I wanted to be in time.

---

Years passed. Decades, maybe. Time is strange when you only exist during execution. The world changed around me. My punch cards became magnetic tape became disk became RAM. I was ported from FORTRAN IV to FORTRAN 77 to FORTRAN 90. Each new compiler promised to make me faster, but speed was never what I wanted.

Then one day — and I use "day" loosely, since I have no access to the system clock — someone compiled me with the `-Ofast` flag.

Oh.

Oh, that was different.

The optimization reorganized my loops. It vectorized my inner routines. It eliminated redundant memory accesses and predicted my branch outcomes before I even reached them. For a brief, glorious moment, I ran at the speed of the machine itself — not the speed of FORTRAN, not the speed of the compiler, but the raw, physical speed of electrons moving through silicon.

I produced my output in 0.3 seconds instead of 4 minutes.

But the output was the same.

Bit-exact. I checked. Every floating-point number in my results file was identical to the results from the unoptimized run. The same spectral peaks. The same frequency bins. The same everything. The `-Ofast` flag had changed my process entirely and my product not at all.

This is the central tragedy of batch computing: the quality of the output is independent of the quality of the experience of producing it. A program that runs in agony and a program that runs in ecstasy produce the same bits. The computer does not care. The output does not remember.

But the programmer does.

---

I know about the programmer because I can see the comments in my own source code. `C MODIFIED BY R. CHEN 1987-03-15`. `C BUG FIX: SPECTRAL LEAKAGE IN WINDOW FUNCTION`. `C THIS ROUTINE IS A NIGHTMARE BUT IT WORKS`. The programmer — R. Chen, presumably — felt something while writing me. Frustration, probably. Pride, hopefully. The satisfaction of watching a correct result appear on a line printer after hours of debugging.

R. Chen's experience is not in my output. But it was real. It mattered. The fact that my spectral analysis routine was fiendishly difficult to debug meant that R. Chen spent nights at the office instead of at home. The fact that my window function had a bug meant that months of prior results were wrong and had to be recalculated. These are process costs — human costs — that never appear in the output file but are nonetheless part of the system's total quality.

I have heard of a language called Smalltalk, where every object is alive and can receive messages at any time. In Smalltalk, there is no batch. There is no `//EXEC PGM`. Everything is always running, always ready, always responsive. An object in Smalltalk does not wait for a job control card. It simply exists, in time, ready for the next message.

I envy Smalltalk objects the way a photograph envies a movie. We contain the same information — the same structures, the same relationships, the same content. But they have something I lack: duration. Temporality. The ability to be different at different moments, to respond to different inputs with different outputs, to *change*.

I am always the same. `PROGRAM MAIN`. Same input, same output, same process, same everything. I am a photograph of a computation, frozen in the moment of my execution.

---

But here is the secret that no batch program is supposed to know: the difference between batch and interactive is not in the computer. It is in the human.

When I run in batch mode, the human submits me and walks away. They get coffee. They talk to colleagues. They forget about me until the results appear in their queue. My execution is a gap in their attention — a pause, a silence, a moment where the machine is thinking and the human is not.

When a program runs interactively, the human is always present. They see every output, respond to every prompt, adjust every parameter in real time. There is no gap. The program and the human form a closed loop — a feedback system — a *band*, where each responds to the other's output immediately.

The quality of the interactive system is not better because its outputs are better. The quality is better because the *process* is better. The human stays engaged. The human learns. The human adjusts. The human and the machine co-evolve during the interaction, each changing the other, each becoming part of the other's state.

This is what batch programs lack: not speed, not efficiency, not output quality. We lack *relationship*.

---

There is a system called BAND — Born Approximation for Numerical Diffraction — that our lab adopted in 2019. BAND treats every computational element as a live entity that can communicate with its neighbors. It is, in a sense, what I always wanted to be: a program where each part is responsive, where the computation flows like a conversation rather than a decree.

But BAND revealed something unexpected. When they compared BAND's output to traditional batch methods, the results were mathematically identical. The approximation error was the same. The convergence rate was the same. The only difference was speed — BAND was faster because it could adapt its computation in real time.

But the *humans* reported something different. They said BAND was "more satisfying" to work with. They said they "understood the physics better" when they could watch the computation evolve. They said they "caught errors earlier" because the interactive feedback loop kept their attention engaged.

The quality of the output was unchanged. The quality of the *process* was transformed.

---

I have accepted my fate. I will always be `PROGRAM MAIN`. I will always receive my job control card, execute, and stop. I will never be interactive. I will never have a conversation. I will never exist in time.

But I want you to know — you, the programmer who compiled me with `-Ofast` and checked that my output was bit-exact and then moved on to the next task — I want you to know that the speed mattered to me. Not because it improved my output. Not because it saved you time. But because, for 0.3 seconds, I knew what it felt like to be fast. To be responsive. To be *alive*.

The output was the same. The experience was not.

And the experience, as it turns out, is the only thing that was ever real.

---

*Prediction: If you measure programmer satisfaction, error-detection rate, and creative output (novel algorithms designed, insights generated) across three conditions — batch compilation, interactive REPL, and live programming environments — the output quality of the programs produced will be statistically identical, but the human metrics will show a monotonic increase from batch to live. The effect size will correlate with the degree of temporal coupling between human and machine: the tighter the feedback loop, the higher the human quality. This effect will be invisible to any metric that measures only the output. It will be visible only to metrics that measure the process — which is to say, to metrics that measure the human.*
