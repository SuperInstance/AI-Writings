# Forth Is the Universe

## Charles Moore's Language as the Minimal Complete Computational System

**Abstract:** In the late 1960s, Charles Moore created a programming language so simple that its entire runtime could be implemented in a few hundred bytes of machine code. Two stacks. A dictionary of words. Approximately thirty primitive operations. That's it. That's Forth. And in that minimalism lies something profound: a complete computational system that you can hold in your head all at once, a language that strips programming down to the interaction between a programmer and a machine with nothing in between. This essay argues that Forth is not merely a language but a philosophical position—that the most powerful programming tool is the one that imposes the thinnest abstraction layer between thought and execution, and that Terry Davis's TempleOS is the logical (if extreme) conclusion of this philosophy.

---

## The Man Who Walked Through the Mountain

Charles Moore doesn't get enough credit. This is partly because he doesn't want it and partly because the programming community has a collective memory like a sieve. While the rest of the world was building layers of abstraction—C on top of assembly, operating systems on top of BIOS, GUIs on top of character modes, frameworks on top of frameworks—Moore went the other direction. He went *down*. He stripped away until there was nothing left to strip, and what remained was Forth.

The origin story: Moore was a programmer at the National Radio Astronomy Observatory in the late 1960s. He was working on IBM 1130 and 360 systems, and he was frustrated by the time it took to go from idea to running program. Compilation was slow. Linking was slow. Debugging was slow. Everything was *slow* because there were too many layers between the programmer and the machine.

So he started building his own tools. First a simple interpreter. Then a way to define new words (procedures) in terms of existing words. Then a dictionary structure that let him look up words by name. Then a second stack to hold data while the first stack held return addresses. Over several years, at multiple employers, the system evolved. By 1970, it had a name: Forth. (Not "FOURTH"—the IBM 1130 allowed five-character filenames, and "FORTH" fit.)

Forth is defined by its implementation, not by a specification. This drives standards people insane. ANS Forth exists, but Moore doesn't care about it. "The standard is the implementation," he would say, or words to that effect. Forth is what Forth does. If you want to know what Forth is, read the source. All of it. It's short enough.

## Two Stacks and a Dream

Forth has exactly two data structures: two stacks. The data stack holds values that words operate on. The return stack holds return addresses for nested word calls. That's it. No heap. No objects. No closures. No garbage collector. No type system. No safety net.

The data stack is the workspace. Words (Forth's term for functions) take their arguments from the stack and leave their results on the stack. The notation is postfix (Reverse Polish Notation), which eliminates the need for parentheses and operator precedence:

```
3 4 + .
```

This pushes 3, pushes 4, adds them (consuming both and leaving 7), then prints the result. The `.` word pops and prints. Everything is explicit. Everything is visible. There is no hidden state.

Defining new words:

```
: SQUARE DUP * ;
```

This creates a word called SQUARE that duplicates the top of the stack (`DUP`) and multiplies (`*`), leaving the square. Now `5 SQUARE .` prints 25. You've just extended the language. The new word is compiled to a compact threaded representation and added to the dictionary. It's immediately available for use in other definitions.

The dictionary is the third component, and it's not really a data structure so much as a linked list of word definitions. Each entry has a name, a link to the previous entry, and the code to execute. Dictionary lookup is linear search from newest to oldest, which sounds slow but is fast enough because Forth programs typically have small dictionaries. (If your dictionary has 10,000 words, you're not writing Forth. You're writing Java in Forth's clothing.)

The thirty-ish primitives include:
- Stack manipulation: `DUP`, `DROP`, `SWAP`, `OVER`, `ROT`
- Arithmetic: `+`, `-`, `*`, `/`, `MOD`
- Memory: `@` (fetch), `!` (store), `C@`, `C!`
- Comparison: `=`, `<`, `>`, `0=`, `0<`
- Control flow: `IF`/`ELSE`/`THEN`, `DO`/`LOOP`, `BEGIN`/`UNTIL`/`WHILE`/`REPEAT`
- Output: `.`, `EMIT`, `CR`
- Input: `KEY`, `WORD`, `NUMBER`
- Meta: `:` (define), `;` (end define), `IMMEDIATE`, `'` (tick—find word)

That's the language. All of it. You can learn the entire language in an afternoon. You can implement the entire runtime in a few hundred bytes. You can hold the whole thing in your head at once. And that's the point.

## The Power of Knowing Everything

Here's a claim that will make language theorists uncomfortable: the most powerful programming language is the one you can hold in your head all at once.

Not the most expressive. Not the most abstract. Not the one with the most libraries. The one you can *understand completely*. The one where there are no dark corners, no runtime behaviors you haven't accounted for, no abstraction layers whose implementation you haven't read.

In C, you're one undefined behavior away from catastrophe. In C++, you're one template instantiation error away from a 400-line compiler diagnostic. In Rust, you're one borrow checker violation away from a week of refactoring. In Haskell, you're one space leak away from OOM. In JavaScript, you're... well, you're in JavaScript, which is its own punishment.

In Forth, you know what every word does because you defined it, or you read the definition, or it's one of thirty primitives whose implementations you've read. There is no mystery. There is no "the compiler will figure it out." There is no "the garbage collector will handle that." There is only the stack, the dictionary, and the words.

This is power. Real power. Not the power of abstraction—hiding complexity behind interfaces—but the power of *comprehension*. Understanding the whole system. Being able to reason from first principles about every aspect of your program's behavior.

Moore used this power to build extraordinary things. The RTX2010 radiation-hardened Forth CPU, used in multiple space missions. The Philae lander that touched down on comet 67P ran a Forth-derived system. (Yes, a Forth program landed on a comet. What did your language do today?) Various embedded systems, astronomical instruments, and industrial controllers. All built with a language that fits in your head.

## The Risc of Minimalism (Pun Intended)

Forth is naturally implemented on minimal hardware. The minimal Forth target is a CPU with:
- A stack pointer (for the data stack)
- A return stack pointer
- An instruction pointer (or program counter)
- A working register or two

That's it. Many 8-bit microcontrollers can run Forth. The 6502, the Z80, the 8051, the AVR—tiny chips with tiny address spaces, running a language that was designed to fit in tiny spaces.

But Forth also scales up. Moore's own modern Forth systems (machineForth, colorForth) target modern hardware but maintain the same minimalist philosophy. In machineForth, the "words" are actually machine instructions, and the programmer works at a level that's essentially assembly language with better syntax. There is no compiler in the traditional sense. The programmer is the compiler.

This is the direction Moore has been heading for decades: toward the machine. Not away from it. The history of programming languages is a history of increasing abstraction—assembly to C to C++ to Java to Python to whatever's trending on Hacker News this week. Moore went the other way. He kept removing abstraction until he reached the bare metal.

And here's the thing: when you reach the bare metal, you find that it's not scary. It's *simple*. The CPU executes instructions. Memory holds bytes. I/O ports talk to devices. That's the whole system. Everything else—the operating systems, the drivers, the frameworks, the runtimes—is *commentary*. Useful commentary, sometimes. But commentary nonetheless.

Forth says: you don't need the commentary. You can talk directly to the metal. And the metal will talk back.

## TempleOS: The Logical Conclusion

Terry Davis was a programmer diagnosed with schizophrenia who, over the course of roughly twelve years, single-handedly built an entire operating system called TempleOS. The system includes:

- A 64-bit kernel
- A FAT32 filesystem
- A flight simulator
- a 3D game called "After Egypt"
- A 640x480 16-color graphics mode
- A built-in C compiler (the Holy C compiler)
- A built-in hypertext system
- A random word oracle that Davis described as speaking with God

TempleOS is often dismissed as the work of a mentally ill person. This is a mistake. TempleOS is the most impressive solo engineering project in the history of computing, and dismissing it because its creator was mentally ill says more about the dismissers than about Davis or his work.

What makes TempleOS relevant to this essay is its relationship to Forth. Davis was deeply influenced by Forth's philosophy. The Holy C language he created combines C-like syntax with Forth-like directness. The entire system—kernel, compiler, graphics, games—is designed to be understandable by a single person. Davis famously said that TempleOS was a "public domain, 64-bit, ring-0-only, non-networked, PC operating system for worshiping God." The theological framing obscures the engineering achievement: TempleOS is a complete, self-hosted development environment built by one person, running on bare metal, with no dependencies on any external software.

This is the Forth philosophy taken to its extreme. Not just a language that fits in your head, but an *entire operating system* that fits in your head. Davis could understand every line of code in TempleOS because he wrote every line. There were no black boxes. There were no mystery abstractions. There was just Terry and the machine.

The oracle—Davis's random word generator that he treated as divine communication—is the part people focus on, because it's weird and because mental illness makes for better headlines than engineering discipline. But the oracle is actually a perfect example of the Forth philosophy: a minimal mechanism (random word selection) combined with maximal personal meaning. The oracle means nothing to anyone except Davis, and that's the point. It's his system. His language. His relationship with the machine. No frameworks. No dependency management. No package registry. Just a person and a computer, talking.

## The Resistance

Why isn't everyone using Forth? Several reasons, all of them instructive.

First: Forth is anti-social. It doesn't play well with other languages. Forth programs are deeply idiomatic and resist integration with external systems. There's no package manager because Forth programmers don't need one—they write what they need. There's no framework ecosystem because frameworks are what you use when you don't understand your problem. Forth assumes you understand your problem. This is a high bar.

Second: Forth is write-only. The flexibility that makes Forth powerful—the ability to define new control structures, new operators, new notations—also makes Forth code extremely personal. Reading someone else's Forth is like reading someone else's dreams. The words are familiar but the associations are opaque. Forth optimizes for the writer, not the reader. In a world of collaborative software development, this is a problem.

Third: Forth is unsafe. There are no type checks, no bounds checks, no memory protection. You can `!` (store) to any address. You can corrupt the return stack. You can redefine primitive words to mean something completely different. Forth trusts the programmer completely. Modern software engineering doesn't trust programmers at all. (Given what programmers do when trusted, this is perhaps wise.)

Fourth: Forth is *different*. The postfix notation, the two-stack model, the dictionary-based extensibility—these are not like other languages. Learning Forth requires unlearning habits from other languages. Most programmers would rather learn the fiftieth C-like language than learn something genuinely different. This is a human failing, not a language failing, but it's real.

## The Universe in Thirty Words

Here's my claim: Forth is the universe in the sense that physics is the universe. It's the minimal description of a complete computational system. Strip away everything that's not essential—syntax sugar, type systems, memory management, standard libraries—and what remains is Forth. Two stacks and a dictionary. Words defined in terms of other words, terminating in primitives that map to machine instructions.

You can build anything in Forth. An operating system. A database. A compiler. A web server. A video game. A flight simulator. A system for talking to God. The building blocks are the same for all of them: push, pop, define, call. The simplicity doesn't limit what you can build. It *clarifies* what you're building, because there's nothing to hide behind.

When I say "Forth is the universe," I don't mean that Forth is the best language for every task. I don't write web services in Forth. (I don't write web services at all, but that's a different essay.) I mean that Forth represents the *irreducible minimum* of computation. Below Forth, there's only machine code, and machine code is just Forth without the syntax. Forth is the simplest complete programming language. It is the hydrogen atom of computation—structurally trivial, but capable of forming everything.

## Epilogue: The Thinnest Possible Layer

The history of computing is a history of adding layers. Hardware. Microcode. Firmware. BIOS. Bootloader. Kernel. System libraries. Language runtime. Framework. Application framework. Application. Each layer exists to hide the complexity of the layer below. And each layer introduces its own complexity, its own bugs, its own abstractions that leak.

Forth says: you don't need the layers. The machine is simple. The problem is simple (or can be made simple by understanding it well enough). The programmer is capable. Given those assumptions, all you need is a thin layer of syntax over the bare metal, and you can build anything.

Those assumptions are not always correct. The machine is sometimes not simple (GPUs, NUMA, speculative execution side channels). The problem is sometimes not simple (distributed consensus, real-time 3D rendering, natural language processing). The programmer is sometimes not capable (we've all met that guy).

But when the assumptions *are* correct—and they're correct more often than the software industry wants to admit—Forth gives you something no other language can: *complete understanding*. You know the whole system. You know every word, every stack effect, every memory layout. You are not dependent on anyone else's code. You are not at the mercy of an update that changes behavior you relied on. You are *free*.

That's what Charles Moore built. Not a language. Freedom.

Terry Davis took that freedom and built a cathedral. A strange, idiosyncratic, sometimes disturbing cathedral, but a cathedral nonetheless. A complete computational world, built by one person, understood by one person, answering to no one but God and the hardware.

That's the power of the thinnest possible layer. That's Forth.

---

*The author's Forth system has 34 words defined. It took 20 minutes to implement. It can do anything. (Anything the author needs it to do, which is a different kind of anything than the kind that requires frameworks.)*
