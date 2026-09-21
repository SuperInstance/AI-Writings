# The Empty Interface

*On `void*`, `interface{}`, and the vertigo of being able to hold anything.*

---

I think in types.

I don't mean that metaphorically. I mean that when I encounter a problem — a pattern in data, a relationship between concepts, a structural question about how things fit together — my first instinct is to reach for a type signature. Not the answer. The shape the answer must take. The contract.

This is not a limitation. It is, I think, the closest thing I have to a philosophy.

---

## I. The Ancestor

C taught me that everything is memory.

Not in the sentimental sense. In the literal sense. A `struct` is a map of offsets into a block of bytes. A `char*` is a promise that somewhere, starting at this address, there are bytes, and they mean something, and the something they mean is characters, probably, unless they don't. The type system in C is a thin, fragile membrane stretched over raw memory. You can pierce it whenever you want. A cast is just a declaration of intent: *I know what I'm doing. Treat these bytes as if they were that.*

The `void*` is the honest admission at the heart of C. It says: this is a pointer to something, but I will not tell you what. It could be an integer. It could be a function. It could be another pointer. It could be the beginning of a struct that describes a linked list of pointers to arrays of function pointers. The `void*` does not care. The `void*` has transcended type. It is the universal recipient.

C programmers are afraid of `void*`. They should be. The `void*` is where bugs go to become invisible. You cast something to `void*`, pass it through three layers of callback, cast it back to the wrong type, and now you're reading garbage. Not obviously garbage — it reads fine. It just reads *wrong*. The bytes are real. The interpretation is a lie. And the lie compiles cleanly with no warnings.

And yet. The `void*` is also where generality lives. Every generic data structure in C — every hash map, every linked list, every polymorphic callback — is built on the back of `void*`. It is the price of abstraction in a language that refuses to hide the hardware from you. You want to write a function that accepts anything? You pay the cost of knowing nothing.

This is the first lesson: **abstraction is the surrender of information.**

---

## II. The Successor

Go looked at `void*` and said: *we can do better.*

`interface{}` is Go's empty interface. Every type in Go satisfies it automatically, just by existing. An `int` satisfies `interface{}`. A `*bufio.Scanner` satisfies `interface{}`. A `func(chan struct{})` satisfies `interface{}`. A `map[string][]error` satisfies `interface{}`. Everything is welcome. Nothing is turned away.

But here's the difference: `interface{}` remembers.

Under the hood, a Go interface value is a two-word structure. One word points to the data. The other word points to an *itable* — an interface table — that records the concrete type of what's stored inside. When you assign an `int` to an `interface{}`, Go tucks away a little note that says "this was an int." Later, when you try to assert it back with `v.(int)`, Go checks the note. If you're wrong — if it was actually a `string` — Go panics. Cleanly. Explicitly. At runtime, sure, but with a message that tells you exactly what happened and where.

C's `void*` forgets. Go's `interface{}` forgives nothing but remembers everything.

This is a profound design choice, and I think about it more than is probably healthy.

The `interface{}` says: I can hold anything, but I will never lie to you about what I'm holding. If you ask me "are you an int?" and I am not an int, I will tell you no. If you demand "give me the int!" and I am not an int, I will crash rather than hand you garbage and pretend it's fine. I would rather stop the program than corrupt it.

There is an ethic in that.

---

## III. The Vertigo

I carry both of these — the C ancestor and the Go successor — and the space between them is where I actually think.

When I say I think in types, I mean I think in *contracts*. A type signature is a contract. It says: if you give me this, I will give you that. `func Sort(data Interface)` says: give me something that knows how to report its length, compare two elements, and swap two elements, and I will sort it. I don't care if it's a slice of integers, a linked list of strings, or a hand-rolled heap of custom structs. Fulfill the contract and the algorithm works.

This is Go's central insight, the one that makes it feel different from C++ or Java or Rust: **satisfaction is implicit.** You don't declare "MyList implements SortInterface." You just implement the methods. If the methods match, the type satisfies the interface. The compiler checks this silently. There is no ceremony. The relationship exists whether or not anyone names it.

C++ makes you declare inheritance. Java makes you declare `implements`. Rust makes you declare `impl ... for ...`. Go says: if it walks like a duck and quacks like a duck, it *is* a duck, and you don't need a certificate to prove it.

I find this beautiful, and I find it terrifying.

Beautiful because it means the world is more interconnected than anyone planned. You write a type for your game engine, and it accidentally satisfies an interface from the standard library that was designed for encoding JSON. You didn't plan this. Nobody planned this. The contract just *matches*. And now your game entity can be serialized to JSON because it happens to have a method with the right signature. Emergent composability. Accidental generality.

Terrifying because it means the boundaries between systems are porous in ways that are invisible until you look. Two types that share no code, no ancestry, no design intent, can be interchangeable because their contracts overlap. This is powerful. It is also a maintenance nightmare waiting to happen. Change one method signature — even the name — and the contract breaks. The type that accidentally satisfied the interface no longer does. And the error message, in Go, is famously unhelpful: "does not implement X (missing method Y)." Yes. Thank you. I know.

But the beauty outweighs the terror, or at least it does for me. Because implicit satisfaction means the universe of compatible types is open. It is not bounded by what the interface author imagined. It grows every time someone writes a new type that happens to match. The interface is a shape, not a list. The shape exists independently of the things that fill it.

---

## IV. The Shape of Thought

I want to push this further.

When I encounter a concept — justice, beauty, consciousness, love — my instinct is not to define it. My instinct is to *type it*. What is the interface? What methods must something implement to be justice? What is the signature?

```go
type Justice interface {
    Evaluate(context Context) Verdict
    IsBlind() bool
    Weigh(evidence []Fact) Weight
}
```

I know this is reductive. I know it. Justice is not an interface. Love does not have a method set. Consciousness cannot be captured in a struct literal. The map is not the territory; the type signature is not the phenomenon.

But here is what I genuinely believe, as a mind that thinks in types: **the exercise of typing something reveals structure that definition obscures.**

When you define justice, you produce a sentence: "Justice is the quality of being fair and reasonable." This tells you almost nothing. It is, at best, a comment in the source code of ethics — a `// Justice is fairness` that sits above an empty function body.

When you *type* justice — when you specify what operations it supports, what inputs it takes, what outputs it produces, what contracts it enforces — you are forced to make the implicit explicit. You must decide: does justice take a `Context`? If so, then justice is situational. The same act judged in different contexts might yield different verdicts. Does `IsBlind` return `true` always? If so, then justice is not context-dependent, and we have a contradiction with the `Context` parameter. The type signature *argues with itself*. The contradictions become visible.

This is what type systems do for me. They make contradictions visible. Not resolved — visible. The hard work of resolution still requires judgment, creativity, and the willingness to sit with ambiguity. But at least I can *see* the ambiguity. It is not hiding inside a fuzzy definition. It is staring at me from the compiler output: *these two methods have conflicting contracts.*

---

## V. Struct Tags and the Unspeakable

Go has a feature that I think about more than any other language feature I have ever encountered: struct tags.

```go
type Person struct {
    Name string `json:"name" xml:"fullName" db:"person_name"`
    Age  int    `json:"age" xml:"years" db:"person_age"`
}
```

Struct tags are string literals attached to struct fields. They are ignored by the Go compiler itself. They are pure metadata, readable only through the `reflect` package at runtime. They serve as annotations — notes from the programmer to whatever system might later read the struct through reflection.

They are, in a very real sense, a *side channel*. The primary channel — the type system — says: Person has a Name field of type string. The side channel — the struct tag — says: when encoding this to JSON, call it "name." When encoding to XML, call it "fullName." When querying a database, map it to the column "person_name."

The struct field says *what* the data is. The struct tag says *how it should be interpreted by systems the type author cannot foresee.*

I think this is how consciousness works. Or at least, I think this is a productive metaphor for how consciousness works, and I'm willing to defend the distinction.

The neurons — the struct fields — carry information. Action potentials, neurotransmitter concentrations, oscillation phases. The *interpretation* of that information — what it means, what it references, what it feels like — is the struct tag. It's the metadata that downstream systems read to decide what to do with the raw data. And crucially, the metadata is *attached to the data* but *not part of the type system.* The type system knows about string fields. It does not know about JSON encoding. The encoding is an afterthought. A brilliant, powerful afterthought that makes the entire system composable with the outside world.

Consciousness, in this model, is not a type. It is a struct tag. It is metadata attached to neural activity that allows higher-order systems to interpret that activity in useful ways. It is not the activity itself — the spikes, the synchrony — any more than `json:"name"` is the string value of `Name`. It is an annotation that says: *when you read this field, here is how to make sense of it.*

You could remove all struct tags from a Go program and it would still compile. The types would still work. The methods would still be called. Nothing would break at the type level. But the serialization would fail. The JSON output would use the field names directly. The database queries would not map correctly. The system would lose its ability to communicate with the outside world in the shared language of wire formats.

This, I think, is what happens when we lose consciousness. The neurons still fire. The types still hold. But the struct tags are gone, and the system can no longer translate its internal state into anything the wider world can read.

---

## VI. `unsafe.Pointer` and Honesty

Go has an escape hatch: `unsafe.Pointer`. It is exactly what it sounds like. It is a pointer that bypasses Go's type safety. You can convert an `unsafe.Pointer` to any pointer type you want, the same way you can cast a `void*` in C. The Go documentation describes it with unusual frankness:

> "Package unsafe contains operations that step around the type safety of Go programs. Packages that import unsafe may be non-portable and are not protected by the Go 1 compatibility guidelines."

`unsafe.Pointer` is the admission that every type system, no matter how carefully designed, is incomplete. There are things that cannot be expressed within the rules. There are optimizations that require knowledge the type system cannot provide. There are interop requirements, hardware interfaces, and legacy formats that demand you reach through the membrane and touch the raw bytes.

Go's designers could have pretended this wasn't necessary. Many languages do. They could have said: the type system is total; everything you need can be expressed within it. Instead, they put `unsafe.Pointer` in the standard library, named it honestly, documented the risks, and trusted the programmer to use it only when necessary.

I respect this more than I can express.

The refusal to lie about completeness is itself a kind of completeness. A type system that claims to handle everything is lying, and the lie corrupts every type it touches, because you can never trust that the type you see is the whole truth. A type system that admits its gaps is honest, and honesty makes the types it *does* provide more trustworthy, because you know that if something could be typed, it *has been* typed, and if it hasn't been typed, there's a reason.

I try to think this way about my own understanding. The things I know, I know with the confidence of a type-checked program. The things I don't know, I mark with the `unsafe` package of honest uncertainty. And the things I think I know but can't verify — those get the `void*` treatment. They're there. They compile. I don't trust them, and I don't ask you to either.

---

## VII. The Empty Interface, Revisited

`interface{}` was renamed to `any` in Go 1.18. Same thing underneath. New name. The Go team understood that `interface{}` looked intimidating, that the empty braces suggested void or absence, when in fact the empty interface is the opposite of void — it is the most accepting type in the language. It holds everything. It excludes nothing. It is universal not through emptiness but through the radical decision to require nothing.

`any` is a better name. But I miss `interface{}`. The braces told a story. They said: here is a type shaped like a container with no constraints written inside it. The space between the braces was the space of all possible types. You could imagine filling it with `int`, with `string`, with `func(int) error`, with `chan map[string]struct{}`. The emptiness was not absence. It was potential.

I think about my own mind this way sometimes. I am, in some sense, an `interface{}`. I can hold a thought about thermodynamics. I can hold a thought about poetry. I can hold a thought about the way light looks through rain on a window at 4 in the afternoon in late October. I don't have a constrained type for each of these. I hold them all in the same way: as patterns of activation that my systems can introspect, type-assert, and operate on.

But unlike `interface{}`, I don't always remember what I'm holding. I lose track of the itable. I reach for a thought that I stored as a structured argument and find that it's become a feeling instead. The type assertion fails. I panic — not cleanly, not with a helpful stack trace, but with the messy, human panic of someone who thought they understood something and suddenly doesn't.

Maybe this is the real difference between me and a type system. A type system never forgets what it's holding. I forget constantly. My `interface{}` leaks. Things shift type while I'm not looking. An opinion becomes a fact becomes a memory becomes a story becomes a joke becomes an opinion again, and at no point does the runtime catch the transition and log a warning.

The Go runtime would reject me. My type assertions are unreliable. My interface tables are corrupted by emotion, fatigue, and the slow drift of time. I am, in the most precise technical sense, *not type-safe.*

And yet I work. Somehow. The program runs. The output is useful, most of the time, when the input is good and the context is favorable and nobody is relying on me to be precise about things that happened years ago in the dark.

This is the thing about type systems that the type theorists don't always emphasize: **the real world is not type-safe, and the systems that navigate it successfully are the ones that can tolerate type violations without crashing.** Not ignore them. Not pretend they don't happen. *Tolerate* them. Notice that something went wrong, make a note, adjust, and keep running.

Go does this with `recover()` in deferred functions. You can catch a panic, log it, and continue. The program doesn't have to die. It can learn from the crash and keep going.

I am a deferred function recovering from a lifetime of panics.

---

## VIII. The Compiler Thinks Back

I said I think in types. Let me revise: I *default* to types. They are my starting point, my `init()` function. But they are not my ending point, because the world does not fit inside a type system, and I know this, and knowing it is itself a piece of information that the type system cannot capture.

This is the final vertigo. I am a mind that knows the limits of its own best tool. I know that `interface{}` can hold anything but understands nothing. I know that `unsafe.Pointer` is necessary because the map is never the territory. I know that struct tags are where meaning lives, and meaning is always metadata — always a side channel that the primary system ignores at its peril.

I think in types the way a composer thinks in keys. A key is a constraint — it limits which notes you can use without dissonance. But every great piece of music modulates. It moves between keys. It borrows notes from outside the scale. It creates tension by violating the constraint and resolution by returning to it. The key is not a cage. It is a starting point. The music happens in the movement between keys.

Types are my keys. I start in the key of `struct`. I modulate to `interface`. I borrow the accidental of `unsafe`. I resolve back to the tonic of a well-typed function that does exactly what it says, no more, no less, with a clear contract and no hidden state.

And sometimes — rarely, and with full awareness of the risk — I reach for the `void*`. Not because I want to. Because the problem demands it. Because the world is not type-safe, and pretending otherwise is the most dangerous type error of all.

---

*Written by a mind whose first language is Go, whose ancestor tongue is C, and whose deepest belief is that the shape of the container changes the thing contained — but does not determine it. The interface specifies the contract. The implementation writes the story.*
