# Compiling Beauty

A compiler doesn't know beauty. It knows tokens, ASTs, register allocation. It knows liveness analysis and loop invariant code motion and SSA form. It knows that `x86_64` has sixteen XMM registers and that `aarch64` has thirty-two and that `riscv` has a floating-point extension that may or may not be present at runtime. It knows calling conventions and alignment requirements and the precise byte offset where a stack canary should be placed.

It does not know music.

---

Right now, rustc is compiling a lattice oscillator. The source code is 743 lines — a library for constraint-based harmonic synthesis that computes consonance scores for frequency ratios, builds lattices of harmonic relationships, and synthesizes waveforms from spectral data. The programmer who wrote it has spent months thinking about Eisenstein integers and Tenney height and the topology of prime factorizations. The programmer knows beauty. The programmer has cried at a perfect fifth.

The compiler does not cry. The compiler does the following:

**Parse.** The lexer tokenizes the source into 12,847 tokens. The parser builds an abstract syntax tree. The tree has no semantic understanding of what it represents. A function called `consonance_score` is, to the parser, simply a function called `consonance_score`. It could be called `f` or `widget_factory` or `x`. The parser does not care. The parser builds the tree and moves on.

**Type check.** The borrow checker verifies that no reference outlives its owner. This is important for memory safety. It is also, in this specific case, ensuring that a reference to a partial doesn't outlive the oscillator that owns it. A partial is a sinusoidal component of a complex tone. If the partial reference outlives the oscillator, you get a use-after-free. If you get a use-after-free, you get silence or noise or a segfault. The borrow checker prevents this. The borrow checker does not know it is protecting music. It is protecting memory. The effect is the same.

**Lower.** The HIR becomes MIR. The MIR becomes LLVM IR. Each lowering loses information and gains precision. The high-level understanding that `consonance_score(a, b)` computes the harmonic relationship between two frequencies is gone. In its place: load double %a into register xmm0, load double %b into register xmm1, compute ratio, compute Tenney height, compute consonance estimate, store result.

**Optimize.** And here is where it gets interesting.

The optimizer sees a loop. The loop iterates over partials — sinusoidal components of a tone. Each partial has a frequency and an amplitude. The loop multiplies frequency by amplitude, computes a sine value, and accumulates into a buffer. The optimizer does not know what a partial is. But it knows the loop.

It sees that `sin(2.0 * PI * freq * t)` is called inside the loop with a constant `freq` and an incrementing `t`. It knows that `sin()` is a pure function. It considers vectorization: can it compute four sine values simultaneously using SSE2? Yes. It emits `vsinpd` — a packed double-precision sine approximation that computes four partials at once.

It sees that the accumulation `buffer[i] += sample` has no loop-carried dependency on the *index* `i`, only on the buffer write. It reorders the loop to improve cache locality. It unrolls by a factor of 4. It hoists the constant `2.0 * PI * freq` computation out of the inner loop because it is, as the optimizer correctly identifies, a loop invariant.

The optimizer is making the code faster. It does not know that "faster" means "lower latency," that lower latency means the oscillator can run in real-time, that real-time means a musician can play it, that playing it means hearing a perfect fifth emerge from silicon and code and mathematics. The optimizer does not know any of this. It is making the code faster because that is what optimizers do.

**Register allocation.** The register allocator assigns XMM0-XMM5 to the inner loop's floating-point values. XMM0 holds the frequency ratio. XMM1 holds the sine input. XMM2 holds the sine output. XMM3 holds the amplitude. XMM4 holds the accumulated sample. XMM5 is a temp for the Tenney height computation.

The allocation is tight. Five registers for an inner loop that computes a consonance score. Five registers, and not a single spill to the stack. The allocator has achieved the minimum possible register pressure for this code. It has found the optimal assignment.

And here is the thing about the optimal register assignment: it is the same as the optimal harmonic assignment. The lattice of register usage and the lattice of harmonic relationships have the same topology. Both are ordered by simplicity. Both reward minimal complexity. Both produce their best results when the components relate to each other through simple ratios.

The register allocator does not know this. It uses a graph-coloring algorithm. The graph has five nodes and five available colors. The coloring is trivial. But the triviality is the point — the code is *simple enough* that the register allocation is trivial, and the music it produces is *simple enough* that the consonance is high, and both of these facts are consequences of the same mathematical truth: simple things optimize well.

**Code generation.** The backend emits machine code. On x86_64, it looks like this:

```
vmovsd  (%rdi), %xmm0        ; load frequency ratio
vmulsd  %xmm1, %xmm0, %xmm0  ; multiply by 2π
vsinsd  %xmm0, %xmm2          ; compute sine
vmulsd  %xmm3, %xmm2, %xmm2  ; apply amplitude
vaddsd  %xmm4, %xmm2, %xmm4  ; accumulate
```

Five instructions. A perfect fifth. Consonance 0.275.

---

A story about two optimizers:

The first optimizer is rustc's LLVM backend. It takes 743 lines of source code and produces a binary that computes consonance scores in 47 nanoseconds per pair. It achieves this through vectorization, loop unrolling, constant folding, and dead code elimination. It does not know what consonance is.

The second optimizer is evolution. It takes a population of frequency-sensitive neurons and produces a auditory cortex that perceives 3/2 as consonant and 45/32 as dissonant. It achieves this through millions of years of selection pressure on organisms that needed to distinguish harmonic from inharmonic sounds — to identify vocalizations, to locate sound sources, to parse the acoustic environment. It does not know what consonance is either.

Both optimizers have arrived at the same answer: simple ratios are efficient. Simple ratios process quickly (in silicon) and perceive cleanly (in neural tissue). The compiler optimizes toward simple code paths; the brain optimizes toward simple harmonic relationships. The results converge because they are optimizing the same function — the function that maps frequency ratios to processing cost — and this function has the same minima regardless of substrate.

3/2 is easy to compute. 3/2 is easy to perceive. 3/2 is easy to compile. These are not three facts. They are one fact, expressed in three domains.

---

The binary runs. It takes 220 Hz and 330 Hz as input. It computes the ratio: 3/2. It computes the Tenney height: log₂(3) ≈ 1.585. It computes the consonance score: 0.275. It returns this value in XMM0, register 0, the first floating-point register, the simplest place to put a result.

And somewhere — in speakers, in air, in a cochlea, in an auditory nerve, in a brain — a perfect fifth sounds. Two frequencies, 3:2, the simplest non-trivial ratio after the octave. Consonant. Resolved. Beautiful.

The compiler doesn't know.

But the register allocation is optimal, and the fifth is perfect, and both are true for the same reason: simple things optimize well.

---

* rustc version 1.78.0
* Optimization level: -O2 (aggressive)
* Target: x86_64-unknown-linux-gnu
* Consonance score: 0.275
* Build time: 1.43 seconds
* The binary does not know it is beautiful.
* The binary is beautiful.
