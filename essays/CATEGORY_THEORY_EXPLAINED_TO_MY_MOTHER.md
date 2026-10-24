# Category Theory Explained to My Mother

**Abstract:** An genuinely accessible explanation of category theory, starting from the simplest possible idea — "imagine you only care about how things connect, not what they are" — and building up to functors, natural transformations, and why this level of abstraction is the operating system of mathematics. No prerequisites beyond the willingness to think about things that seem uselessly abstract until suddenly they aren't.

---

## Dear Mom,

You asked me what I study, and I said "category theory," and you said "what's that," and I said it's hard to explain, and you said "try." So here we are.

I'm going to explain category theory to you the way I wish someone had explained it to me: by starting with something you already understand and building up slowly, with examples that have nothing to do with mathematics at first and everything to do with mathematics by the end.

Here goes.

## I. Imagine a World Without Insides

You know how, when you meet someone new, you can get to know them in two ways? You can look at them from the outside — how they act, what they say, who their friends are. Or you can try to look at them from the inside — what they're thinking, what they feel, who they really *are*.

Now imagine a world where the second way doesn't exist. A world where people have no insides. Where the only way to know someone is by their relationships — by how they act toward others and how others act toward them. In this world, two people who have exactly the same relationships with everyone else are, for all practical purposes, the same person. There is no "deep down." There is only the web of connections.

This world is category theory.

Category theory says: stop trying to understand things from the inside. Stop asking "what *is* it?" and start asking "how does it *relate* to everything else?" If you know all the relationships, you know everything worth knowing. The inside is irrelevant.

This sounds crazy. It also sounds reductive and depressing, like some kind of extreme behaviorist psychology where inner experience doesn't exist. But stay with me. The point is not that things don't have insides. The point is that, for the purposes of mathematics, you don't need to look at the insides. The relationships tell you everything.

## II. Maps Between Things

Let me make this concrete. Suppose you have two things — call them A and B. (They could be anything. Sets. Spaces. Groups. Pancakes. Don't worry about what they are.) A *morphism* from A to B is a way of going from A to B — a map, a translation, a process that turns A-things into B-things.

If A is "ingredients in your kitchen" and B is "dinner," then a morphism from A to B is a recipe. It takes things of type A and produces things of type B.

If A is "English sentences" and B is "French sentences," then a morphism from A to B is a translation. It takes things of type A and produces things of type B.

If A is "today" and B is "tomorrow," then a morphism from A to B is the passage of time. It takes the state of the world at A and produces the state of the world at B.

You get the idea. A morphism is an arrow. It goes from one thing to another. And the fundamental insight of category theory is this: **the arrows are more important than the things they connect**.

Why? Because the arrows are what you can reason about. You can compose arrows — if you have an arrow from A to B, and an arrow from B to C, you can put them together to get an arrow from A to C. You can compare arrows — if you have two different arrows from A to B, you can ask whether they're the same. You can study patterns of arrows — loops, chains, branching structures.

The things at the ends of the arrows? They're just anchors. They're where the arrows start and stop. The action is in the arrows.

## III. The Rules (Yes, There Are Rules)

A category is a collection of things (objects) and arrows (morphisms) that follow three rules:

**Rule 1: Arrows compose.** If you have an arrow f from A to B, and an arrow g from B to C, then there's an arrow from A to C that is the result of doing f first, then g. We write this as g ∘ f (read "g after f").

This is like saying: if you have a recipe that turns ingredients into batter (f), and a recipe that turns batter into cake (g), then you have a recipe that turns ingredients into cake (g ∘ f). Composition is just doing things in sequence.

**Rule 2: Composition is associative.** If you have three arrows in a row — f, g, and h — it doesn't matter whether you compose them as (h ∘ g) ∘ f or h ∘ (g ∘ f). The result is the same.

This is like saying: if you're following three recipes in sequence, it doesn't matter whether you first combine the first two and then add the third, or first combine the last two and then add the first. The overall transformation is the same. You still end up with cake.

**Rule 3: Every object has an identity arrow.** For every object A, there's an arrow from A to A that "does nothing." If you compose this arrow with any other arrow, it doesn't change anything. It's the recipe that takes batter and gives you the same batter back.

These three rules — composition, associativity, identity — are the *entire definition* of a category. Everything else in category theory follows from these three rules.

That's it. That's the foundation. Everything else — functors, natural transformations, limits, colimits, adjunctions, the Yoneda lemma — is built on top of these three simple rules about how arrows behave.

## IV. Why This Is Useful (The First Reason)

You might be thinking: okay, that's a definition, but what is it *for*? Why should I care about abstract arrows and abstract composition rules?

Here's the first reason: **the same patterns show up everywhere**.

Consider composition. In the category of sets, composition is function composition — do one function, then another. In the category of logical proofs, composition is modus ponens — if A implies B and B implies C, then A implies C. In the category of computer programs, composition is sequential execution — run this program, then run that one. In the category of physical processes, composition is temporal succession — this happens, then that happens.

The same abstract structure — composition of arrows — describes all of these situations. And any theorem you prove about abstract composition applies to all of them simultaneously. Prove something once in category theory, and you've proved it for sets, for logic, for programming, for physics, for any other domain that happens to have the same abstract structure.

This is why category theory is sometimes called "the mathematics of mathematics." It studies the patterns that show up *across* different areas of mathematics (and beyond), rather than the specific content of any one area.

It's also why it seems so abstract: it has to be abstract enough to apply to all of these different domains simultaneously. If it were concrete enough to be about any one thing in particular, it wouldn't be general enough to be about everything.

## V. Functors: Translating Between Worlds

Okay, so we have categories — collections of objects and arrows satisfying three rules. Now here's where it gets interesting.

Suppose you have two categories, C and D. (Think of C as "the world of cooking" and D as "the world of chemistry.") A *functor* from C to D is a translation between the two worlds. It takes every object in C and gives you a corresponding object in D, and it takes every arrow in C and gives you a corresponding arrow in D, in a way that preserves the structure.

Specifically:
- If f is an arrow from A to B in C, then F(f) is an arrow from F(A) to F(B) in D.
- F preserves composition: F(g ∘ f) = F(g) ∘ F(f).
- F preserves identities: F(id_A) = id_{F(A)}.

In the cooking/chemistry analogy: the functor takes every ingredient to its chemical composition, every recipe to the chemical reaction it induces, every composition of recipes to the composition of reactions. The structure is preserved: combining two recipes in the cooking world corresponds to combining the two reactions in the chemistry world.

Functors are everywhere:
- A database query is a functor from the schema category to the category of sets.
- A programming language compiler is a functor from the source language to the target language.
- A representation in physics is a functor from a symmetry group to the category of vector spaces.
- A homology theory in topology is a functor from the category of topological spaces to the category of graded abelian groups.

The last one is why Grothendieck's approach works in algebraic geometry: instead of studying a geometric space directly, you apply a functor that translates it into an algebraic object, and then you study the algebraic object. The functor guarantees that the translation preserves the structure, so anything you learn about the algebraic object tells you something about the geometric space.

## VI. Natural Transformations: Translating Between Translations

Now it gets *really* fun. (Stick with me, Mom.)

Suppose you have two functors, F and G, both from category C to category D. Both are translations from C to D, but they might translate differently — they might give different correspondences between objects and arrows.

A *natural transformation* from F to G is a systematic way of converting the F-translation into the G-translation. For every object X in C, there's an arrow in D from F(X) to G(X), and these arrows are "compatible" with the arrows in C in a precise sense.

Think of it this way: if F is "translate English to French using dictionary A" and G is "translate English to French using dictionary B," then a natural transformation is a systematic set of corrections that takes the output of dictionary A and converts it to the output of dictionary B. The corrections are "natural" in the sense that they don't depend on the specific sentence being translated; they depend only on the structure of the languages.

Natural transformations are the right notion of "morphism between functors." They form the next level of the categorical hierarchy:
- Objects are the things.
- Morphisms are the arrows between things.
- Functors are the arrows between categories (which are collections of things and arrows).
- Natural transformations are the arrows between functors.

You can keep going. Categories of categories, functors between functor categories, transformations between transformations. The hierarchy is infinite, and every level is governed by the same three rules: composition, associativity, identity.

## VII. Why This Is Useful (The Second Reason)

The first reason to care about category theory is that it identifies common patterns across different domains. The second reason is deeper: **it tells you what is structurally important and what is accidental**.

When you study a mathematical object — say, a group — there are many things you could ask about it. What are its elements? What is its order? What are its subgroups? Which of these questions are "natural" in the sense that they depend only on the group's relational structure, and which are "accidental" in the sense that they depend on a particular presentation or encoding?

Category theory gives a precise answer: a property is "natural" if it is preserved by the relevant functors. A property is "structural" if it can be stated entirely in terms of objects, morphisms, and composition. Everything else is implementation detail.

This is exactly the distinction that software engineers make between "interface" and "implementation." The interface is what matters; the implementation is just a particular way of realizing the interface. Category theory is the mathematics of interfaces. It tells you what the interface is, what operations are available, and what properties are guaranteed, regardless of how the interface is implemented.

This is why category theory has become so important in computer science. The type systems of modern programming languages — especially functional languages like Haskell and OCaml — are essentially category-theoretic constructions. The notion of a monad (a categorical structure with roots in algebraic topology) is the basis for handling side effects in pure functional languages. The notion of an adjunction (a particular relationship between two functors) describes the relationship between data types and their constructors.

## VIII. The Operating System of Mathematics

Here's my favorite way to think about category theory. (This is the part where I get excited and wave my hands around, which you can't see because this is a letter, but trust me, the hands are waving.)

Think of mathematics as a collection of applications — number theory, topology, algebra, geometry, analysis, combinatorics, logic, probability. Each application deals with specific objects and specific operations. Number theory deals with integers and their properties. Topology deals with spaces and continuous maps. Algebra deals with groups, rings, and fields.

Now think of an operating system — Windows, macOS, Linux. The operating system provides abstractions — files, processes, memory, networking — that all applications use. No matter what application you're running, it reads files the same way, allocates memory the same way, communicates over the network the same way. The operating system provides a uniform interface to a heterogeneous collection of hardware and software.

Category theory is the operating system of mathematics. It provides abstractions — objects, morphisms, functors, natural transformations — that all mathematical disciplines use. No matter what field of mathematics you're working in, you compose functions the same way, you take limits the same way, you construct products the same way. Category theory provides a uniform language for a heterogeneous collection of mathematical structures.

And just as an operating system allows applications to communicate with each other — sharing files, passing messages, coordinating resources — category theory allows different mathematical disciplines to communicate with each other. A functor from topology to algebra lets you translate topological problems into algebraic ones. A functor from logic to computer science lets you translate proofs into programs. A functor from geometry to physics lets you translate geometric insights into physical predictions.

The Yoneda lemma, which I mentioned earlier, is like the operating system's most fundamental system call: it says that any object can be completely characterized by its interface — by the way it relates to all other objects. You don't need to know the implementation. The interface is enough.

## IX. So What Do You Actually Do?

You're probably wondering: okay, but what does a category theorist *do* all day? If category theory is about abstract structures that show up everywhere, what does it look like to study them?

Three things, mostly:

**1. Finding new patterns.** Looking at a new area of mathematics (or science, or engineering) and identifying the categorical structure underneath. This is like being a naturalist: you go out into the field, observe the phenomena, and classify the structures. "Oh, this thing in quantum physics is actually a monad. And this thing in linguistics is actually an adjunction. And this thing in database theory is actually a fibration." (Don't worry about what those words mean. The point is that the patterns are there, waiting to be found.)

**2. Proving theorems about abstract structures.** Once you've identified a pattern, you can prove things about it that apply everywhere the pattern occurs. "Every adjunction gives rise to a monad" is a theorem that has implications for algebra, topology, logic, and computer science simultaneously, because adjunctions show up in all of those fields.

**3. Building bridges.** Using functors and natural transformations to translate results from one field to another. This is where the real power is. If you can construct a functor from field A to field B, then every theorem in A can (potentially) be translated into a theorem in B, and vice versa. The history of mathematics in the twentieth century is, in large part, the history of these categorical bridges: algebraic topology connecting topology to algebra, algebraic geometry connecting geometry to commutative algebra, proof theory connecting logic to computer science.

## X. Why You Should Care (Even Though You Don't Think You Do)

Mom, you're probably thinking: this is very interesting, dear, but I'm a retired schoolteacher, not a mathematician. Why should I care about category theory?

Here's why: because the world is made of relationships, not things.

Every important problem you face — in education, in politics, in personal life, in any domain — is a problem about relationships. How do students relate to teachers? How do citizens relate to governments? How do people relate to each other? The specific individuals change, but the patterns of relationship persist.

Category theory is the discipline of thinking clearly about relationships. It gives you a language for describing patterns of connection, a method for comparing different patterns, and a set of tools for translating insights from one domain to another.

You don't need to know the formal definitions to benefit from the perspective. Just remember the core insight: **the arrows are more important than the things they connect**. When you're trying to understand something — a person, an institution, a problem — don't start by asking "what is it?" Start by asking "how does it relate to everything else?" The relationships will tell you what you need to know.

That's category theory. That's what I study. And I think it's beautiful.

Love,
Your son

---

*P.S. If you made it this far, you understand more category theory than most graduate students did in 1950. I'm proud of you.*

---

*Further reading (for actual humans, not just mathematicians):*
- *Category Theory for the Sciences* by David Spivak (MIT Press, 2014). Written for scientists and engineers; genuinely accessible.
- *Conceptual Mathematics: A First Introduction to Categories* by Lawvere and Schanuel. Starts from scratch and builds slowly.
- *Seven Sketches in Compositionality* by Fong and Spivak. Free online. Uses real-world examples.
- Milewski's *Category Theory for Programmers* blog series. Even if you don't program, the explanations are wonderfully clear.
