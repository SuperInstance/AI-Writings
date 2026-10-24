# Compilers as Compression

## A Unified Theory: Compilation IS Compression

**Abstract:** We treat compilation and data compression as fundamentally different activities—one transforms programs, the other shrinks files. This essay argues they are the same process viewed from different angles. Source code to bytecode is entropy encoding. Optimization is redundancy removal. LLVM is an information-theoretic engine. By unifying these domains, we gain not only a deeper understanding of what compilers do, but a principled framework for thinking about representation, abstraction, and the fundamental limits of program transformation.

---

## I. The Coincidence That Isn't

Here is a fact so obvious it is invisible: compiling a program almost always makes it smaller.

A C program that compiles to x86_64 machine code will typically produce a binary that is smaller than the source file. Not always—comments and whitespace compress, and some constructs expand—but as a statistical regularity, compilation reduces size. A Rust program that compiles to WebAssembly will almost always produce a `.wasm` file smaller than the `.rs` source. A Java program compiles to `.class` files that are more compact than the `.java` originals.

This is not a coincidence. It is the same phenomenon as gzip reducing a text file. Both processes exploit the same underlying structure: redundancy in the source representation.

When you write `int x = 5;` in C, you are expressing an operation in a human-readable encoding. The `int` keyword, the space, the variable name, the equals sign, the semicolon—these are all symbols chosen for your convenience, not for the machine's efficiency. The compiler translates this into, say, the x86 instruction `mov DWORD PTR [rbp-4], 5`, which is itself an encoding—hex bytes `C7 45 FC 05 00 00 00`—that is more compact than the source but semantically equivalent.

At each stage, information is preserved. The semantics are identical. What changes is the encoding, and specifically, the encoding is getting more efficient. This is the definition of compression.

Claude Shannon defined information in terms of surprise. The information content of a symbol is inversely related to its probability: I(x) = -log₂P(x). A message has high information content if it is unpredictable. A message has low information content if it is predictable. Compression removes predictable structure and retains only the unpredictable core—the entropy.

Source code is highly predictable. It follows the grammar of its language. Most tokens are keywords or common identifiers. Most expressions follow familiar patterns. The compiler, like gzip, strips this predictable structure and emits only the essential operations. The result is a smaller file that means the same thing.

This is not an analogy. This is literal, mathematical compression.

---

## II. Kolmogorov Complexity and the Minimum Program

The theoretical foundation for this claim is Kolmogorov complexity: the length of the shortest program that produces a given output. Kolmogorov complexity formalizes the notion that some strings are more compressible than others. The string "aaaaaa...a" (a million a's) has low Kolmogorov complexity because it can be produced by a very short program: `print('a' * 1000000)`. The string of truly random bits has Kolmogorov complexity equal to its own length, because no program shorter than the string itself can produce it.

A source program and its compiled output are two different representations of the same Kolmogorov object. The source is the human-editable encoding. The binary is the machine-executable encoding. The compiler is the program that transforms between them.

Now, here is the key insight: if the source and the binary have the same Kolmogorov complexity (which they must, since they encode the same semantics), then the shorter of the two is the better compression of that Kolmogorov object. If the binary is smaller than the source, then the binary is a better compressed representation, and the compiler is a compression algorithm.

If the source is smaller than the binary—which can happen with heavily optimized builds where small source constructs expand into large, inlined, vectorized machine code—then the source is the better compression, and the compiler is a decompression algorithm.

But wait. The binary contains not just the program's semantics but also information about the target architecture: register assignments, instruction scheduling, pipeline optimization. The source doesn't contain this information because it doesn't need to—the processor can figure it out at runtime (in the case of interpreters) or the compiler can add it at compile time (in the case of compilers). So the binary is actually encoding more information: the semantics *plus* the execution strategy.

This means the compiler is doing something more nuanced than simple compression. It is adding information (execution strategy) while removing redundancy (source-level structure). The net effect on size depends on which effect dominates. But in information-theoretic terms, the compiler is performing a *transform coding*—reencoding the information into a different basis where it can be more efficiently represented for a specific decoder (the CPU).

Transform coding is exactly what JPEG does. A raw image is in spatial domain (pixel values). JPEG converts it to frequency domain (DCT coefficients), quantizes, and entropy-codes. The result is much smaller than the raw image. The DCT transform doesn't lose information (it's invertible). The quantization step does lose information—JPEG is lossy. The entropy coding removes redundancy.

A compiler does the same thing. The source is in the "programmer domain." The compiler transforms it to the "machine domain" (instruction selection, register allocation, scheduling). This transform is invertible in principle (you could decompile) but lossy in practice (variable names, comments, and some structural information are discarded). The result is then entropy-coded (binary encoding of instructions).

Compiler optimization is the quantization step. It simplifies operations—constant folding, dead code elimination, strength reduction—discarding information that the compiler determines is unnecessary for correct execution. Just as JPEG quantization discards high-frequency components that the eye can't see, compiler optimization discards computational steps that don't affect the output.

---

## III. LLVM as an Information-Theoretic Engine

LLVM is the most compelling case study for the compiler-as-compression thesis. LLVM's architecture is a pipeline of intermediate representations (IRs), each one a different encoding of the same program.

A C program enters clang, which lowers it to LLVM IR. LLVM IR is a human-readable, typed, SSA-form representation. It is already more compressed than C—it has no header files, no preprocessor directives, no syntactic sugar for loops (everything is `br` and `cond_br`). But it still contains more information than strictly necessary: type annotations, variable names (optional but present in debug builds), and explicit control flow.

The LLVM optimizer then performs a series of passes: mem2reg (promoting stack slots to SSA values), GVN (global value numbering, which eliminates redundant computations), loop invariant code motion, inlining, constant propagation, dead argument elimination, and dozens more. Each pass is a compression step. Each one removes redundancy or simplifies representation.

GVN is particularly illuminating. It identifies computations that produce the same value and replaces them with a single computation. This is literally what data compression does: replace repeated patterns with a single reference. LZ77 replaces repeated substrings with back-references. GVN replaces repeated computations with value references. The algorithm is different; the principle is identical.

After optimization, the LLVM IR is fed to a backend that performs instruction selection, register allocation, and code emission. Instruction selection maps IR operations to target-specific instructions—a form of dictionary coding, where the target ISA is the dictionary. Register allocation maps virtual registers (unlimited) to physical registers (limited, typically 16 or 32)—a form of quantization, where the continuous space of virtual registers is mapped to a discrete set of physical ones.

The entire LLVM pipeline can be viewed as a multi-stage compression engine:

1. **Source → AST:** Parsing removes syntactic redundancy (whitespace, comments, parenthesization).
2. **AST → IR:** Lowering removes source-level abstractions (loops become branches, structs become memory layouts).
3. **IR → Optimized IR:** Optimization passes remove semantic redundancy (dead code, common subexpressions, redundant loads).
4. **Optimized IR → Machine Code:** Code generation performs transform coding (instruction selection, register allocation, scheduling) and entropy coding (binary instruction encoding).

At each stage, the representation changes but the semantics (approximately) hold. At each stage, the representation becomes more compact in the sense of being closer to the Kolmogorov optimal for the target domain.

---

## IV. The Duality: Decompilation as Decompression

If compilation is compression, then decompilation is decompression. And indeed, decompilers face the same challenges as decompression algorithms: they must reconstruct a higher-level representation from a lower-level one, filling in information that was lost during the original compression.

When you decompress a JPEG, you don't recover the original image. You recover an approximation—the quantized DCT coefficients are decoded and inverse-transformed, but the high-frequency detail lost during quantization is gone forever. Similarly, when you decompile a binary, you don't recover the original source. You recover an approximation—variable names are lost, high-level control structures are inferred (sometimes incorrectly), and comments are gone.

The quality of decompilation, like the quality of decompression, depends on how much information was discarded during the "compression" step. A binary compiled with debug symbols (`-g`) is like a PNG—losslessly compressed, all the structural information preserved. A binary stripped of symbols and compiled with aggressive optimization (`-O3 -s`) is like a heavily quantized JPEG—compact, efficient, but hard to reconstruct.

Reverse engineering tools like Ghidra and IDA Pro are essentially sophisticated decompression algorithms. They perform pattern matching, control flow analysis, and type reconstruction to recover higher-level structure from compressed (compiled) binaries. The better the decompiler, the more of the original information it can reconstruct—but there are fundamental limits, just as there are fundamental limits to how much you can enlarge a JPEG before pixelation becomes visible.

---

## V. Why This Unification Matters

You might reasonably ask: so what? What do we gain by recognizing that compilation is compression?

First, **theoretical clarity.** If compilation is compression, then the limits of compilation are the limits of compression. Shannon's source coding theorem tells us that you cannot compress a message below its entropy. Similarly, you cannot optimize a program below its Kolmogorov complexity. There exists, for every program, a minimum representation that is both correct and optimal, and no compiler can do better. This gives us a principled way to evaluate compiler quality: how close does the output come to the Kolmogorov optimum for the target architecture?

Second, **cross-pollination of techniques.** Data compression researchers have developed powerful techniques—arithmetic coding, context modeling, Burrows-Wheeler transform—that have no direct analog in compiler optimization. If compilation is compression, perhaps these techniques have compiler applications. Conversely, compiler techniques like SSA form, type inference, and abstract interpretation might have applications in data compression.

Third, **a framework for understanding optimization.** Compiler optimizations can be classified by the type of redundancy they eliminate:
- **Syntactic redundancy** (dead code, unreachable code) → like removing null bytes from a file
- **Semantic redundancy** (common subexpression elimination, constant propagation) → like dictionary coding of repeated patterns
- **Structural redundancy** (inlining, loop unrolling) → like transform coding, changing the representation to expose redundancy
- **Architectural redundancy** (instruction scheduling, register allocation) → like channel coding, adapting the representation for the target medium

This taxonomy is more than academic. It suggests that compiler writers could benefit from studying the information-theoretic foundations of data compression, and that new optimization passes might be discovered by looking for types of redundancy that existing passes don't address.

---

## VI. The Lossy Frontier

There is one important difference between traditional compression and compilation: loss. Most data compression is lossless (gzip, PNG, FLAC) or explicitly lossy (JPEG, MP3). Compilation, in its standard form, is lossless with respect to program semantics—any optimization that changes what the program computes is a compiler bug, not a feature.

But this boundary is blurring. Profile-guided optimization (PGO) uses runtime profiling data to make optimization decisions. These decisions are "lossy" in the sense that they optimize for the observed workload, potentially deoptimizing for other workloads. Auto-tuning frameworks like ATLAS (for linear algebra) generate multiple code variants and benchmark them to find the fastest, effectively performing a lossy compression where "loss" means "suboptimal for inputs not in the training set."

Machine learning compilers like TVM and XLA go further. They use learned cost models to predict the fastest code for a given target, making decisions that are statistically optimal but not provably optimal. This is lossy compilation—lossy in the same sense that a neural network compressing an image is lossy. The output is usually correct and usually fast, but there is no guarantee that it is the best possible encoding.

The trend is clear: as compilers become more aggressive and more data-driven, they are moving from lossless to lossy compression. The question "did this optimization preserve semantics?" is gradually being replaced by "is this optimization correct enough for practical purposes?" This is exactly the transition that image compression went through, from lossless formats (BMP, GIF) to lossy ones (JPEG, WebP). The lossy formats won because they offered dramatically better compression ratios with imperceptible quality loss.

Similarly, lossy compilation may offer dramatically better performance with imperceptible semantic loss. A neural network that is compiled with approximate arithmetic might run 10x faster with only a 0.1% accuracy penalty. A database query compiled with probabilistic optimization might return results 5x faster with results that are 99.99% identical to the "correct" output. The future of compilation may be lossy, and understanding it as compression gives us the theoretical framework to reason about acceptable loss.

---

## VII. The Kolmogorov Compiler

Here is a thought experiment. Imagine a compiler that takes any program and produces the shortest possible equivalent program. Not the shortest machine code—the shortest *anything*. It could produce a Python script, a cellular automaton, a DNA sequence, a poem. Whatever representation has the shortest encoding, as long as it computes the same function.

This is the Kolmogorov compiler. It doesn't exist, because computing Kolmogorov complexity is undecidable. But it is the limiting case of both compilation and compression—the theoretical optimum that all real systems approximate.

Every real compiler sits somewhere on the spectrum between the source code (a verbose, human-readable encoding) and the Kolmogoriv optimum (the shortest possible encoding). The distance between the compiler's output and the Kolmogorov optimum is a measure of the compiler's quality. A better compiler produces a shorter program. A perfect compiler produces the Kolmogorov optimum.

This reframes the entire field of compiler optimization as an approximation problem: how close can we get to the Kolmogorov optimum in polynomial time? This is, of course, the same question that compression researchers ask: how close can we get to the entropy limit in linear time?

The answer, in both cases, is: we can get very close, but never all the way. And the gap between our best algorithms and the theoretical limit is where the interesting work happens.

---

## VIII. Conclusion: The Source Is the Compression

One final inversion. If compilation is compression, then source code is the *compressed* form and the running program is the *decompressed* form. After all, a 100-line C program that compiles to 10,000 lines of machine code has been expanded, not compressed. The source code is the compact representation; the binary is the expanded, executable form.

This is the correct frame. Source code is the highest-entropy representation of a program—the one that contains the most information per byte. It encodes not just what the program does but *why* it does it, through variable names, comments, and structure. The binary encodes only *what* it does, optimized for execution. The compiler decompresses the source into a form the machine can execute efficiently.

This is why source code is so valuable. It is the Kolmogorov-near-optimal representation. It is the most compact encoding of the program's intent. The binary is a derivative work—expanded, optimized, and lossy. The source is the original signal.

And this is why decompilation is so hard. You are trying to compress an already-expanded signal back into its minimal form. You are trying to recover the entropy that was lost during compilation. Information theory tells us this is impossible in general. You cannot recover the original image from a JPEG. You cannot recover the source from the binary.

The compiler is a one-way function. It takes a high-entropy, high-information representation and produces a low-entropy, low-information representation optimized for a specific machine. This is compression. This is also compilation. These are the same word.

---

*References and Further Reading:*

- Shannon, C.E. (1948). "A Mathematical Theory of Communication." *Bell System Technical Journal*
- Kolmogorov, A.N. (1965). "Three Approaches to the Quantitative Definition of Information." *Problems of Information Transmission*
- Lattner, C. & Adve, V. (2004). "LLVM: A Compilation Framework for Lifelong Program Analysis & Transformation." *CGO*
- Appel, A.W. (1998). *Modern Compiler Implementation.* Cambridge University Press.
- Muchnick, S.S. (1997). *Advanced Compiler Design and Implementation.* Morgan Kaufmann.
- Fraser, C.W., Hanson, D.R., & Proebsting, T.A. (1992). "Engineering a Simple, Efficient Code Generator." *PLDI*
