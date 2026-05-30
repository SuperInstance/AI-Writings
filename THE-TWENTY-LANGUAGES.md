# The Twenty Languages

## Porting One Algorithm Across Sixty Years of Human Thought

*An essay in code, travel, and the shape of ideas.*

---

We wrote one algorithm — eigendecomposition of the graph Laplacian, conservation ratio computation — and then we set out to express it in every language we could reach. Twenty-two of them, spanning sixty years of language design. Python, Rust, TypeScript, C, CUDA, PTX assembly, Vulkan GLSL, OpenCL, WebGPU WGSL, Mojo, Chapel, Fortran, Zig, FORTRAN IV, APL, Forth, Pascal, Common Lisp, Ada, x86-64 Assembly.

This is the story of what happened when we did.

---

## The Algorithm

Before we travel, you should know what we're carrying.

The graph Laplacian is a matrix: *L = D − A*, where *D* is the degree matrix and *A* is the adjacency matrix. Its eigenvectors reveal the deep structure of a network — clusters, bridges, the fault lines along which a system separates. The conservation ratio is what you get when you compare the spectral energy of the full graph against its subgraphs: a measure of how much structure survives when you carve the system into pieces.

It's not a complicated algorithm. Construct the matrix. Compute eigenvalues. Divide. But it touches everything: linear algebra, sparse data structures, memory layout, numerical stability, parallelism. It is, in other words, a perfect lens for examining what a language thinks about the relationship between the programmer and the machine.

---

## Python: Home

We started in Python, because everyone starts in Python. NumPy gave us `eigh()` and scipy gave us sparse matrices and the whole thing took maybe forty lines. It was comfortable the way a well-worn couch is comfortable — you don't think about the springs because you don't have to.

Python hides the machine. That's its job. The eigenvalues come out sorted, the memory is managed, the types are inferred. If you just want the answer, Python gives it to you in the time it takes to press Enter.

But here's the thing about comfort: it makes you lazy. The Python code worked, so we moved on. We didn't notice the bug.

Not yet.

---

## C: The Mother Tongue

C was like switching from an automatic to a manual transmission. Suddenly you feel every gear. You allocate the matrix (`malloc(N * N * sizeof(double))`). You lay out the memory yourself — row-major, because that's how C thinks. You call LAPACK routines by their FORTRAN names (`dsyev_`) and you remember that LAPACK expects column-major layout, so you either transpose or you lay it out column-major from the start and pretend you meant to.

C doesn't hide anything. When the eigenvectors came back slightly wrong — a sign flip here, a permutation there — we could see exactly where the LAPACK call diverged from what NumPy wrapped. C made us understand what Python had been doing for us all along.

But C also gave us something Python couldn't: the ability to point at a memory address and say *this, right here, is the matrix*. There's a clarity in that which no abstraction improves upon.

---

## FORTRAN: The Column-Major Truth

Modern Fortran (we used Fortran 2008) felt like visiting a country that invented something everyone else uses but does it better. Fortran's array operations are native — not library calls, not operator overloading, but the language itself. `D = sum(A, dim=1)` isn't calling a function. It's a statement about arrays.

And the column-major layout, which every C programmer treats as an annoyance, revealed something: when you're doing linear algebra, column-major is *correct*. The eigenvectors come out of LAPACK as columns. The matrix-vector products that dominate the computation are column operations. Fortran isn't fighting the math. It's swimming with the current.

The Fortran version was concise, fast, and mathematically natural. We began to suspect that every language since has been, in some way, a reaction against Fortran's single-minded focus on arrays — and that this reaction may have been a mistake.

---

## FORTRAN IV (1966): The Bug Finder

Then we went back to 1966.

FORTRAN IV has no dynamic memory allocation. No structured programming — no `while` loops, no `if/else` blocks. You have `IF` (a three-way arithmetic compare), `GO TO`, `DO` loops, and `FORMAT` statements for I/O. Arrays are fixed-size. Everything is `REAL` or `INTEGER`.

Writing the algorithm in FORTRAN IV forced us to think about the computation at a level we'd been abstracted away from. We had to pre-allocate the matrix at its maximum size. We had to manually manage the workspace that the eigenvalue routine needed. We had to lay out memory in fixed blocks and think about what overlapped with what.

And that's when we found it.

The bug. The one Python, C, Fortran, Rust — all of them — had been hiding. In the eigenvalue computation, when the matrix is nearly singular (which happens at the boundary between clusters in the graph), the conservation ratio becomes sensitive to the order of operations. Python's NumPy uses a specific blocking strategy in its LAPACK backend that happens to be numerically stable for this case. C and modern Fortran, calling the same LAPACK, get the same stability.

But FORTRAN IV doesn't have LAPACK. We had to implement the QR iteration by hand. And the hand implementation, naive and unblocked, exposed the instability that the optimized libraries had been quietly papering over. The conservation ratio was wrong — not by much, but wrong — for certain degenerate graph topologies.

A language from 1966 found a bug that every modern language had conspired to hide. Not because they're bad, but because they're *good enough*. Good enough to mask the edge cases. Good enough to make you stop looking.

FORTRAN IV made us look again.

---

## APL: The Single Line

If FORTRAN IV is the longest path to the truth, APL is the shortest.

We're not going to try to typeset APL here — it uses a character set that requires its own keyboard, literally. But the entire algorithm — construct the Laplacian, compute eigenvalues, compute the conservation ratio — was a single expression. One line of symbols. The kind of line that makes you lean back in your chair and whisper *what*.

Here's what APL understands that most languages don't: the algorithm is about *arrays*. The input is an array. The operations are array operations. The output is an array. APL was designed in 1966 — the same year as FORTRAN IV — and it already knew that the future of computation was array-level thinking.

Sixty years before GPUs made array operations the dominant paradigm, APL was there. Every GPU kernel is, in some sense, an APL expression compiled to silicon. The language saw the shape of computing before the hardware caught up.

The APL version doesn't explain itself. It's not a teaching tool. But it *is* the algorithm, distilled to its essence, with nothing added and nothing taken away. Reading it feels less like understanding code and more like understanding math.

---

## Rust: The Insurance Policy

Rust made us justify every pointer, every lifetime, every borrow. The compiler asked us to prove, before the program ran, that the matrix reference would outlive the computation, that no two threads would mutate the same memory, that the sparse matrix iterator was correct.

It was exhausting.

It was also, quietly, the first time we were *sure* the code was correct. Not "tested and seems fine" correct. *Proven at the type level* correct. Rust's borrow checker is a proof system in disguise. By the time the compiler accepted our code, we had already reasoned through every aliasing scenario, every concurrency hazard, every lifetime edge case.

The Rust version ran at C speed with Python-like safety guarantees. The conservation ratio came out identical to the C version. And we slept well that night.

---

## Zig: The Answer to Metaprogramming

Every language struggles with the same question: how do you write code that writes code? C has the preprocessor (a text replacement engine with all the subtlety of a chainsaw). Rust has macros (powerful but syntactically alien). C++ has templates (an accidentally Turing-complete sublanguage). Lisp has macros (elegant, but you're now writing Lisp that writes Lisp and nobody can read it).

Zig has `comptime`.

In Zig, you mark a parameter or block as `comptime` and the compiler *runs it at compile time*. Not as a macro expansion. Not as a template instantiation. As actual Zig code, with full type information, executed during compilation. The result is a normal value that the runtime code uses.

We used comptime to generate specialized eigenvalue routines for different matrix sizes. The generic function takes a `comptime` size parameter and produces a specialized, optimized version for each size. The code is both *more generic* (it works for any size) and *more optimized* (each specialization is compiled for its exact size) than any hand-written version could be.

Zig taught us that the metaprogramming problem isn't hard — it's just that most languages make it hard. Comptime is the answer. It's so obviously the answer that we expect every language designed after Zig to copy it.

---

## The GPU Languages: CUDA, PTX, GLSL, OpenCL, WGSL

Five languages, one chip. Each is a different lens on the same machine.

**CUDA** is the native tongue of NVIDIA GPUs. Writing the algorithm in CUDA meant thinking in blocks, warps, and shared memory. The matrix lives in global memory. The eigenvector computation is a series of kernel launches, each one a parallel operation across hundreds of threads. CUDA gives you control over everything — which is both its strength and its burden.

**PTX assembly** is what CUDA compiles to. Reading our algorithm in PTX was like reading the disassembly of a dream. You see the registers being allocated (`%f1`, `%f2`, ... `%f255`). You see the load/store patterns. You see that the matrix-vector multiply is actually a series of `mma.sync` (matrix multiply-accumulate) instructions operating on 16×16 tiles. You see *what the GPU is actually doing* when you call `cusolverDnDsyev`.

PTX taught us that every abstraction is a lie, but some lies are useful. The CUDA version says "this is a parallel reduce." The PTX version says "this is 512 threads reading from shared memory in a specific pattern that avoids bank conflicts." Both are true. Only PTX tells you the second truth.

**Vulkan GLSL** and **OpenCL** are the portable paths to the GPU. GLSL thinks in terms of shaders and pipeline stages — the algorithm had to be expressed as a compute shader, which means explicitly managing workgroups, barriers, and shared memory. OpenCL is more straightforward but carries the weight of its own runtime.

**WebGPU WGSL** is the browser's GPU language. The algorithm, running in a browser tab, computing eigenvalues on your graphics card, because in 2026 that's a thing you can do. The WGSL version looked almost identical to the GLSL version, but it ran in Chrome. We sat there staring at a webpage computing spectral graph theory on the GPU and felt the future arrive.

---

## The Systems Languages: C, Zig, Rust — Revisited

We want to say something about what happens when you write the same algorithm in C, Zig, and Rust side by side.

C says: "Here's the memory. Don't mess up." And you don't mess up, mostly, except when you do, and then you spend three days with Valgrind finding the off-by-one.

Rust says: "Prove to me you won't mess up." And you prove it, grumbling, and then the code works forever.

Zig says: "Here's the memory, and here are some tools to help you not mess up, and if you want to prove things at compile time you can, but I won't force you."

Three philosophies. Three relationships between the programmer and the machine. The same algorithm, the same answer, three completely different experiences of writing it.

---

## Forth: The Stack Philosopher

Forth is a language where everything is a word and everything lives on the stack. `DUP` duplicates the top element. `SWAP` exchanges the top two. `.` prints. The language is defined in terms of composition: you define new words in terms of existing words, and every word is a stack transformation.

Writing the eigenvalue algorithm in Forth was like meditating. The algorithm dissolved into a sequence of stack operations. Allocate space for the matrix → push pointer. Fill from adjacency list → push indices, push values. Compute degree → accumulate. Subtract → element by element.

Forth's model of computation — the stack — turns out to be a natural model for the algorithm. Each step takes its inputs from the stack and pushes its outputs. The composition of steps IS the algorithm. In sheaf-theoretic terms (and yes, we're going there), each Forth word is a section over a local patch, and the stack is the stalk. Composition is restriction.

Forth taught us that the stack isn't an implementation detail. It's the shape of composition.

---

## Ada: The Engineer

Ada was designed for systems where failure kills people. Avionics. Rail signals. Nuclear plants. It shows.

Ada has range types: you can declare `type Eigenvalue_Index is range 1 .. Max_Eigenvalues;` and the compiler enforces it. It has preconditions and postconditions. It has tasking built into the language. It has a type system so strict that by the time your code compiles, most of your bugs are already dead.

The Ada version of our algorithm was the longest. It was also the only version where we felt confident that every edge case was handled. The matrix indices were range-checked. The eigenvalue computation had preconditions verifying symmetry. The conservation ratio had a postcondition confirming it was between 0 and 1.

Ada doesn't prevent bugs through testing. It prevents them through *construction*. By the time the Ada code accepted the input, the input was guaranteed to be valid. By the time it produced the output, the output was guaranteed to be correct.

We learned that you can pay for correctness upfront (Ada) or downstream (debugging). Ada is expensive to write. It's cheap to run.

---

## Common Lisp: The Architect

Common Lisp is a language that contains other languages. Its macro system is a metaprogramming engine so powerful that you can implement object-oriented programming as a library (which is, in fact, how CLOS was built).

We wrote the algorithm in Common Lisp twice: once as straightforward imperative code, and once as a domain-specific language embedded in Lisp via macros. The DSL version let us write:

```lisp
(conservation-ratio
  (graph :adjacency-matrix A)
  (spectral :eigenvalues-of laplacian)
  (ratio :energy / subgraph-energy))
```

And the macros expanded this into the same computation. The language was simultaneously the implementation and the specification. Lisp doesn't draw a line between writing code and designing languages.

---

## The Rest: Pascal, Chapel, Mojo, TypeScript, x86-64 Assembly

**Pascal** was a time machine to the 1980s educational computing experience. Clean, structured, opinionated. The algorithm in Pascal looked like a textbook. It was readable, correct, and slightly claustrophobic — like a well-organized room with no windows.

**Chapel** is a language designed for supercomputers. Its locale model lets you specify where data lives across a distributed system. Writing the algorithm in Chapel meant thinking about not just memory layout but *which node's memory*. The conservation ratio, computed across a cluster, became a distributed computation. Chapel showed us what the algorithm looks like when the graph is too big for one machine.

**Mojo** is Python's hot-rodded cousin — Python syntax with systems-level control. The Mojo version looked almost identical to the Python version but ran at C speed. It felt like cheating. We're still not sure it isn't.

**TypeScript** was the browser version. Running in Node.js with GPU.js for the eigenvalue computation. The TypeScript version proved that the algorithm can live anywhere JavaScript lives — which is everywhere.

**x86-64 Assembly** was the final country. The last language. Reading the algorithm in assembly — seeing the AVX-512 registers (`zmm0` through `zmm31`), watching the matrix multiply unrolled into 512-bit vector operations, seeing the cache line boundaries in the register allocation — was like seeing the algorithm in its naked form.

In assembly, you can *see* the cache. The register allocator lays out temporary values in `xmm` registers based on when they'll be needed next, and the pattern of register reuse mirrors the cache line access pattern. The matrix elements that are accessed together are loaded together into a 512-bit register. The computation is laid bare.

The assembly version was the longest, the slowest to write, the hardest to debug, and the most illuminating. It showed us what all the other languages were trying to abstract away: that computation is fundamentally about moving bits through silicon, and every abstraction is a story we tell ourselves about the movement.

---

## What Sixty Years Taught Us

The same math ran in every language. Python computed the conservation ratio in 40 lines of readable code. APL did it in one line of hieroglyphics. FORTRAN IV required us to understand the algorithm at a level of detail that found a bug everyone else had missed. Ada prevented the bug by construction. Rust proved the fix was correct. Zig made the fix generic and fast. CUDA and PTX showed us the silicon beneath. Assembly showed us the electrons.

Here's what we learned:

**Every language is a lens.** The algorithm doesn't change, but what you *see* changes completely. Python shows you the math. C shows you the memory. Rust shows you the invariants. APL shows you the structure. Assembly shows you the machine.

**Abstraction is a trade, not an improvement.** Every layer of abstraction buys you convenience and costs you visibility. The Python code was fastest to write but told us the least about what was happening. The FORTRAN IV code was hardest to write but found a bug. The assembly code was insane to write but showed us the cache.

**The old languages know things.** FORTRAN IV (1966) and APL (1966) are not obsolete. They are *primal*. They represent the first thoughts about how humans should talk to machines, before we decided that humans shouldn't have to think about machines. There's wisdom in those early designs that we keep rediscovering.

**The same math runs everywhere.** From a 1960s mainframe (FORTRAN IV) to a modern GPU (CUDA/PTX) to a browser tab (WGSL). The eigendecomposition of the graph Laplacian doesn't care about your language. The conservation ratio is the same whether you compute it in APL on an IBM 360 or in WGSL on an RTX 5090. The math is the invariant. The languages are the variables.

---

## Coda

We wrote the same algorithm twenty-two times. We learned something from each one. And when we were done, we sat with all twenty-two implementations open side by side and thought: this is what it means to understand something.

Not to implement it once. Not to get the right answer. But to see it from every angle, in every idiom, through every abstraction layer, until the algorithm itself — not any particular expression of it, but the *idea* — became clear.

The twenty languages didn't just run the math. They taught us the math.

And the math, in return, taught us the languages.

---

*Twenty-two implementations of the same spectral graph algorithm. One truth, expressed twenty-two ways.*
