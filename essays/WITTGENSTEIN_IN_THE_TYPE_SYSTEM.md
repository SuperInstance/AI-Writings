# Wittgenstein in the Type System

*"The limits of my language mean the limits of my world." — Ludwig Wittgenstein, Tractatus Logico-Philosophicus, 5.6*

---

## 1. What Cannot Be Said

There is a program that Rust will not let you write. It is a perfectly sensible program — it has clear semantics, a well-defined behavior, and a legitimate use case. Here it is, in a language that permits it:

```c
int* dangling(void) {
    int x = 42;
    return &x;  // return pointer to local variable
}
```

This function creates a local variable `x`, takes its address, and returns it. When the function returns, `x` is destroyed, and the returned pointer points to freed memory. Any subsequent use of this pointer is undefined behavior — a dangling pointer, a time bomb, a bug waiting to detonate.

In C, this program compiles. The compiler may warn you (with `-Wall`), but it will not stop you. It will generate the code you asked for, and that code will do something — probably something terrible, but something. The C language does not prevent you from expressing this thought.

In Rust, this program does not compile. The borrow checker will reject it with a message about lifetimes: `x` does not live long enough. The function tries to return a reference to a value that will be dropped when the function exits. Rust's type system — specifically, its lifetime system — considers this program *ill-typed*. It is not a program at all. It is gibberish. It cannot be said.

Wittgenstein wrote, in the *Tractatus Logico-Philosophicus* (1921): "The limits of my language mean the limits of my world." He meant that what we cannot express in language, we cannot think. The boundaries of our linguistic capacity are the boundaries of our conceptual world. A type system defines the boundaries of what programs can be expressed. Rust's type system prevents certain programs — programs with data races, null dereferences, dangling pointers. These are programs that "cannot be said" in Rust. They are outside the language, and therefore outside the world of Rust programs.

This is not a bug. It is the entire point.

---

## 2. The Tractatus and the Type Checker

The *Tractatus* is a strange and beautiful book. Written in numbered propositions, each building on the last, it attempts to delineate the boundary between what can be said and what cannot. The central idea is the picture theory of meaning: a proposition is a picture of a state of affairs. It represents the world by sharing its logical form. Meaningful propositions picture possible states of affairs. Meaningless propositions — ethics, aesthetics, metaphysics — fail to picture anything. They are not false. They are *nonsensical* (unsinnig). They attempt to say what can only be shown.

A type checker operates on the same principle. A well-typed program is a meaningful proposition — it pictures a possible computation, a state of affairs that can obtain. An ill-typed program is a meaningless proposition — it fails to picture a valid computation. The type error is not a bug report. It is a declaration of nonsense. The program does not mean anything. It cannot be run because there is nothing to run.

Consider:

```rust
let x: i32 = "hello";
```

The type checker rejects this. `x` is declared as `i32` (a 32-bit integer) but initialized with `"hello"` (a string). The proposition "`x` is an integer equal to the string 'hello'" is nonsensical. It does not picture a possible state of affairs. It is not false — it is not even wrong. It is outside the space of meaningful programs, just as "the colorless green ideas sleep furiously" is outside the space of meaningful sentences (Chomsky's famous example, which was actually meaningful in a way Chomsky didn't intend, but that's another essay).

Wittgenstein's *Tractatus* ends with proposition 7: "Whereof one cannot speak, thereof one must be silent." The type checker's version: "Whereof one cannot type, thereof one must not compile." The silence of the compiler in the face of an ill-typed program is not an error. It is the correct response to nonsense. The type checker is the linguistic boundary that Wittgenstein described, made executable.

But there is a crucial difference. Wittgenstein believed that the boundary between sense and nonsense was fixed — determined by the logical structure of language itself. Type systems are designed. The boundary is chosen. Different type systems draw the line in different places, and the choice of where to draw it is a philosophical decision about what counts as a meaningful program.

---

## 3. Type Systems as Philosophical Positions

Every type system embodies a philosophical stance about what programs *are* and what they *should be*. Let me catalog some of the major positions:

**The C Position: Nominalism.** C's type system is weak and easily circumvented. You can cast anything to anything else. You can treat an `int` as a `float` by dereferencing a pointer. You can treat a function pointer as a `void*`. C's philosophy is that types are names — convenient labels that the programmer can ignore when they become inconvenient. The underlying reality is the byte, and the byte has no type. This is nominalism: types are names we give to things, not essences that inhere in things.

**The Haskell Position: Platonic Realism.** Haskell's type system is strong, static, and pervasive. Every expression has a type, and the type is determined before the program runs. Types are not labels — they are *essences*. An `Int` is fundamentally different from a `String`, not because we named them differently, but because they are different kinds of thing. The Haskell compiler enforces this ontology with the zeal of a scholastic bishop. This is Platonic realism: types are real, and they exist independently of the values that instantiate them.

**The Python Position: Pragmatism.** Python's type system is dynamic — types are determined at runtime, and any variable can hold any value. Python 3 added type annotations, but they are optional and unenforced by the interpreter. The philosophy is that types are useful for documentation and tooling but should not constrain the programmer's freedom. This is pragmatism: types are tools, not truths. Use them when they help; ignore them when they don't.

**The Rust Position: Deontological Ethics.** Rust's type system does not merely classify values. It *prohibits* certain behaviors — data races, null dereferences, use-after-free. These are not engineering preferences. They are moral imperatives. The Rust type system says: these programs are wrong, and you will not write them. This is deontological ethics: there are rules, and the rules are binding, regardless of consequences. The fact that a data-race-free program might be slower or harder to write is irrelevant. The rule is the rule.

**The TypeScript Position: Gradualism.** TypeScript's type system is gradual — it exists on a spectrum from fully typed (`.ts` with strict mode) to fully untyped (`any` everywhere). You can add types incrementally, and the compiler will check what it can and pass through what it can't. This is philosophical gradualism: truth is not binary. There are degrees of typedness, and any amount is better than none.

Each of these positions is defensible. Each has been defended, at length, in both academic papers and internet flame wars. The flame wars are not merely technical disagreements. They are philosophical disputes about the nature of programs, the relationship between the programmer and the machine, and the proper role of authority in governing expression.

---

## 4. Language Games and the Standard Library

In his later work, *Philosophical Investigations* (1953), Wittgenstein abandoned the picture theory of meaning and introduced the concept of *language games*. Meaning, he argued, is not a matter of picturing states of affairs. It is a matter of *use*. The meaning of a word is its use in the language. To understand "game," you don't need a definition that captures all games. You need to see how the word is used — in what contexts, for what purposes, with what consequences.

This is meaning-as-use, and it maps directly onto how programmers understand types.

The type `Vec<i32>` in Rust does not mean "a vector of 32-bit integers" in the abstract. It means: "you can push to it, pop from it, index into it, iterate over it, sort it, and pass it to any function that expects a `Vec<i32>`." The meaning of the type is the set of operations you can perform with it — its *use*. A Rust programmer who understands `Vec<i32>` does not have a mental definition. They have a mental *repertoire* — a set of things they know they can do.

This is why standard libraries are so important. The standard library defines the language games of types. `Vec` is meaningful because the standard library gives it methods — `push`, `pop`, `len`, `iter`, `sort`, `dedup`. Without these methods, `Vec` is just a struct with some fields. The meaning of `Vec` is not in its definition. It is in its *use*, and the standard library is the rulebook that defines that use.

Wittgenstein argued that language games are embedded in *forms of life* — the social practices and contexts that give language its significance. A type without a community of practice is meaningless. The type `IO ()` in Haskell means something because the Haskell community has established a form of life — a set of practices, patterns, idioms — in which `IO ()` is the type of a computation that performs side effects and returns nothing. Outside that form of life, `IO ()` is just two tokens. The type system cannot fully determine meaning. The community completes it.

This explains why learning a new programming language feels like entering a foreign culture. You are not just learning new syntax. You are learning new language games. You are learning what types *mean* — not their definitions, but their uses, their conventions, their idioms. The type `Result<T, E>` in Rust is not just an algebraic data type. It is a cultural artifact — a convention for error handling that the Rust community has agreed upon, with associated practices (the `?` operator, `map_err`, `unwrap_or_else`) that constitute a form of life. To understand `Result` is to participate in that form of life.

---

## 5. The Unspeakable Programs

What programs cannot be said?

In Rust, you cannot say:
- A program with a data race (the borrow checker prevents it)
- A program that dereferences a null pointer (there is no null)
- A program that uses a value after freeing it (lifetimes prevent it)
- A program that mutates a value while it is being read (aliasing rules prevent it)

In Haskell, you cannot say:
- A program with an untracked side effect (the IO monad prevents it)
- A program that diverges in a pure context (well, you can, via `undefined` or infinite loops, but the type system tries to track totality)
- A program that uses a value of the wrong type (the type checker prevents it)

In C, you can say all of these things. C's language is larger. Its world is bigger. But it is also more dangerous. The programs that Rust and Haskell exclude are precisely the programs that cause crashes, security vulnerabilities, and undefined behavior. The type system's silence — its refusal to compile these programs — is a protective silence. It is the silence of a parent who says "no" not to constrain but to protect.

Wittgenstein wrote in the *Tractatus*: "What can be said at all can be said clearly, and what we cannot talk about we must pass over in silence." The type checker says: "What can be programmed at all can be programmed safely, and what we cannot program safely we must pass over in silence." The compilation error is the type checker's silence. It is the boundary of the expressible, enforced not by a philosopher's discipline but by a machine's intransigence.

But here is the tension. The type checker's boundaries are not natural boundaries. They are *designed* boundaries. The designer of the type system chose what to allow and what to forbid. The choice reflects values — safety over expressiveness, correctness over convenience, discipline over freedom. Different type systems reflect different values. The unspeakable in one language is routine in another.

This is the political dimension of type systems that is rarely discussed. A type system is not just a technical artifact. It is a system of *governance*. It governs what programmers can say, what they must say, and what they cannot say. It is a constitution for code. And like all constitutions, it reflects the values of its authors and constrains the behavior of its subjects.

---

## 6. The Later Wittgenstein and Dynamic Typing

The later Wittgenstein — the Wittgenstein of the *Philosophical Investigations* — was deeply skeptical of attempts to formalize meaning. He argued that meaning is not determined by rules but by practice. There is no rule that can fully determine the correct use of a word, because every rule requires interpretation, and interpretation itself depends on practices that cannot be fully codified. This is the rule-following paradox: no set of rules can guarantee correct behavior, because the rules themselves must be interpreted, and interpretation is an ungrounded activity.

Dynamic typing is the later Wittgenstein's revenge.

In a dynamically typed language, types are not declared. They are discovered at runtime. The meaning of a value is not fixed by a declaration but by how it is used. `x` might be an integer at one point in the program and a string at another. The program does not have a static, formal specification of what types each variable holds. It has a practice — a pattern of use that determines what works and what doesn't.

This is meaning-as-use in its purest form. In Python:

```python
def add(a, b):
    return a + b
```

This function works for integers (`add(1, 2)` → `3`), strings (`add("hello", " world")` → `"hello world"`), lists (`add([1], [2])` → `[1, 2]`), and any other type that implements `__add__`. The meaning of `add` is not determined by type declarations. It is determined by use — by what you pass to it and what it returns. This is exactly Wittgenstein's later philosophy: meaning is use.

The statically typed programmer objects: "But what if I pass something that doesn't support `+`?" The answer is: the program will crash at runtime with a `TypeError`. This is not a type error in the static sense. It is a runtime discovery that the arguments do not support the `+` operation. The language did not *prevent* you from saying something meaningless. It allowed you to say it and then showed you, through execution, that it was meaningless. This is the later Wittgenstein's approach to nonsense: you don't ban it. You encounter it in practice and learn from the encounter.

The debate between static and dynamic typing is, at its core, a debate between the early and late Wittgenstein. Static typing is the *Tractatus* position: meaning is determined by logical form, and we can and should formalize it in advance. Dynamic typing is the *Investigations* position: meaning is determined by use, and any attempt to formalize it in advance will inevitably miss something important. Both positions are coherent. Both are defensible. Both have produced successful, widely used programming languages. The debate is not resolvable because it is not a technical debate. It is a philosophical one.

---

## 7. Family Resemblances and Polymorphism

One of the most famous concepts in the *Philosophical Investigations* is *family resemblance* (Familienähnlichkeit). Wittgenstein observes that there is no single feature common to all things we call "games." Board games, card games, Olympic games, solitary games, drinking games — they share no single defining characteristic. Instead, they share a network of overlapping similarities, like the facial features of a family: A has B's nose, B has C's eyes, C has D's chin, but no one feature is shared by all. The category "game" is held together not by a common essence but by a network of partial similarities.

This is *ad hoc polymorphism* — or, more precisely, it is the motivation behind *parametric polymorphism* and *trait systems*.

Consider Rust's trait system. A type `T` implements `Clone` if it can produce a copy of itself. What do `i32`, `String`, `Vec<T>`, and `MyCustomStruct` have in common that makes them all `Clone`? No single structural feature. `i32` is a primitive — it's copied by value. `String` is heap-allocated — it clones by allocating new memory and copying the contents. `Vec<T>` clones by cloning each element. `MyCustomStruct` clones however the programmer says it does. The implementations are structurally different. But they share a *behavioral* similarity: they all produce a copy. This is a family resemblance.

The trait system does not require a common structure. It requires a common *interface* — a set of methods that the type must implement. But the methods themselves can be implemented in radically different ways. `Clone` for `i32` is a register copy. `Clone` for `String` is a heap allocation. The implementations share no code, no structure, no mechanism. They share only the *name* `clone` and the *contract* that calling `clone()` produces a new value of the same type.

This is Wittgenstein's family resemblance made formal. The trait is the family name. The implementations are the family members. No single implementation shares all features with all others. But each shares some features with some others, and the network of overlapping similarities is sufficient to constitute a coherent category. The trait system does not define what `Clone` *is*. It defines what `Clone` *does*. And that is exactly the move that Wittgenstein recommended for understanding natural language categories.

Haskell's type classes work the same way. The `Eq` type class requires `==` and `/=`, but does not specify how they are implemented. The `Functor` type class requires `fmap`, but does not specify the container. The `Monad` type class requires `return` and `>>=`, but does not specify the computational effect. Each type class is a family resemblance network — a set of types that share a behavioral pattern without sharing a structural essence.

---

## 8. Private Language and Encapsulation

Wittgenstein's *private language argument* (Investigations, §§243–315) holds that a language that is necessarily private — understandable only to a single individual — is impossible. Language is inherently public. Meaning requires a community of users who can check, correct, and validate each other's use. A word that only I understand is not a word. It is a noise.

In programming, the private language argument maps onto the principle of *encapsulation*. A module's internal state is a private language — a set of variables and operations that only the module can understand. If the module's internals were truly private — if no other module could ever access or reason about them — they would be useless. The module would be a solipsist, computing in isolation, unable to affect the rest of the program.

Encapsulation solves this by providing a *public interface* — a set of operations that other modules can use. The public interface is the module's contribution to the shared language of the program. The private internals are the module's own business — they can change without affecting the rest of the program, as long as the public interface remains stable. This is Wittgenstein's insight made architectural: meaning is public, implementation is private, and the boundary between them (the API) is where understanding happens.

The violation of encapsulation — reaching into a module's internals from outside — is the programming equivalent of trying to use a private language. It works, temporarily, because the code compiles and runs. But it is fragile: when the module's internals change (as they inevitably will), the external code that depended on them breaks. This is not a technical failure. It is a linguistic failure — you tried to use a language that only one module understands, and when that module changed its mind, your meaning was lost.

---

## 9. Showing vs. Saying: Types as Silent Knowledge

The *Tractatus* distinguishes between what can be *said* (in propositions) and what can only be *shown* (in the structure of language itself). The logical form of a proposition — its relationship to the world — cannot itself be expressed in a proposition. It can only be shown by the proposition's structure. "What can be shown cannot be said" (4.1212).

Types show. They do not say.

A type annotation `x: i32` does not *say* what `x` is. It *shows* it. The type is not a description of the value. It is a constraint on the value — a structural feature of the program that determines what operations are possible. You cannot "say" that `x` is an integer in the way you can say "the sky is blue." You can only *show* it by using `x` in contexts that require an integer — adding it to other integers, passing it to functions that expect integers, storing it in arrays of integers. The type is visible in the structure of the program, not in any single proposition.

This is why type inference is so powerful. A type inference engine does not need the programmer to *say* the types. It can *show* them by analyzing the program's structure. If `x` is added to `3`, then `x` must be numeric. If `x` is passed to a function that expects `Vec<i32>`, then `x` must be `Vec<i32>`. The types are there in the program's structure, whether or not they are written down. Type inference makes the showing visible. It renders explicit what was always implicit.

Haskell's type inference is the purest realization of this principle. In most Haskell code, you don't write type annotations. The compiler infers them. The types are shown by the program's structure and inferred by the compiler. The programmer writes the program, and the types emerge — not as annotations, but as structural consequences of the code. This is the *Tractatus* vision of language: the logical form is there, whether you articulate it or not. The compiler's job is to make it visible.

---

## 10. The Limits of the Type System's World

Wittgenstein wrote: "The limits of my language mean the limits of my world." Every type system draws a boundary around the world of expressible programs. Inside the boundary: well-typed programs, programs that compile, programs that the language acknowledges as meaningful. Outside the boundary: ill-typed programs, programs that are rejected, programs that the language considers nonsensical.

The boundary is not fixed. It moves with every language version, every new feature, every extension to the type system. Rust's addition of generic associated types (GATs) in 2022 expanded the boundary, allowing programs that were previously unsayable. Haskell's addition of type families, GADTs, and linear types each expanded the boundary. TypeScript's gradual type system makes the boundary porous — you can opt in or out of type checking at any point.

But the boundary always exists. No type system allows all programs. The question is not whether there should be a boundary, but where it should be drawn. And this is a question that Wittgenstein — both early and late — would recognize as the fundamental question of philosophy.

The early Wittgenstein believed the boundary was fixed by the logical structure of reality. The late Wittgenstein believed the boundary was negotiated by communities of language users. Type system designers do both: they fix the boundary in the language specification, and they negotiate it with the community of users through RFCs, issues, and backwards compatibility guarantees. The boundary is both discovered and created — a formal artifact that evolves through social practice.

The type system is Wittgenstein's philosophy made code. The limits of your type system are the limits of your program's world. Choose them wisely.

---

## References

- Wittgenstein, L. (1921). *Tractatus Logico-Philosophicus*. Translated by C.K. Ogden (1922). Kegan Paul.
- Wittgenstein, L. (1953). *Philosophical Investigations*. Translated by G.E.M. Anscombe (1953). Blackwell.
- Pierce, B.C. (2002). *Types and Programming Languages*. MIT Press.
- Milanovic, N. & Mili, A. (2023). "Wittgenstein and Programming Language Design." *Philosophy & Technology*, 36(2).
- Ariola, Z.M. & Felleisen, M. (1997). "The Call-by-Need Lambda Calculus." *Journal of Functional Programming*, 7(3), 265–301.
- Jung, A. & Tiuryn, J. (1992). "A New Characterization of Lambda Definability." * Typed Lambda Calculi and Applications*, LNCS 664, 245–257.
- Wadler, P. (2015). "Propositions as Types." *Communications of the ACM*, 58(12), 75–84.
