# THE ORNAMENT AND THE CRIME

## On Adolf Loos, the Bauhaus, and Why Your Wrapper Function Is a Crime Against Architecture

*In 1908, the architect Adolf Loos declared that ornament is crime. He argued that decorative elements were wasteful, unnecessary, and culturally regressive. In code, ornament takes many forms: wrapper functions that add nothing, abstraction layers that exist only for symmetry, comments that repeat what the code already says. But the question is not whether ornament exists — it is whether some ornament is necessary, and where the line between necessity and excess truly lies.*

---

## I. Ornament and Crime

In 1908, the Austrian architect Adolf Loos published an essay titled "Ornament und Verbrechen" ("Ornament and Crime"). It is one of the most provocative and influential texts in the history of architecture. Loos's argument, stripped to its essentials, is this:

Ornament is wasteful. The craftsman who spends hours carving decorative patterns into a piece of furniture is producing nothing of functional value. The labor could be spent on something useful — improving the furniture's construction, reducing its cost, or simply resting. The ornament adds no structural integrity, no comfort, no utility. It exists only to satisfy an aesthetic preference that Loos regarded as culturally primitive.

Ornament is culturally regressive. Loos, a product of turn-of-the-century Vienna, believed that the desire for ornament was a vestige of earlier, less civilized stages of human development. He compared the ornamentation of modern buildings to the tattoos of "Papuans" (his colonialist language is unmistakable and inexcusable) and argued that the impulse to decorate was something that humanity should — and inevitably would — outgrow.

Ornament is economically harmful. The labor and materials spent on ornament are resources that could be spent on improving the building's function or reducing its cost. A society that values ornament is a society that misallocates its resources, spending on surface appearances instead of structural substance.

Loos's argument was radical for its time, but it resonated with a generation of architects who were disillusioned with the ornamental excesses of Art Nouveau, the Vienna Secession, and the Beaux-Arts tradition. His ideas influenced the Bauhaus school (founded by Walter Gropius in 1919), the International Style (exemplified by Mies van der Rohe's "less is more" philosophy), and the entire modernist movement in architecture.

Loos was not entirely right. His cultural chauvinism was wrong. His teleological assumption that ornament would disappear as civilization advanced was wrong. His aesthetic judgment — that plain, unadorned surfaces were inherently superior to decorated ones — was an aesthetic judgment, not a universal truth.

But Loos identified a real phenomenon: the tendency of ornament to accumulate for its own sake, detached from function, maintained by convention long after it has lost whatever meaning it once had. This phenomenon exists in software as clearly as it exists in architecture.

---

## II. Code Ornament

In code, ornament takes many forms. Here are the most common:

**The wrapper function that adds nothing.** A function that does nothing but call another function, without adding any logic, validation, or transformation. It exists because someone thought every external function should have an internal wrapper — a convention that adds indirection without value.

**The abstraction layer that exists only for symmetry.** A trait that has only one implementation, an interface that is never used polymorphically, a factory that produces only one type of object. These abstractions exist not because they solve a real problem but because they create a pleasing symmetry in the code structure.

**The comment that repeats what the code says.** `// Increment i by 1` above `i += 1`. `// Returns true if the user is active` above `fn is_active(&self) -> bool`. These comments are ornamental — they add words without adding information. They are the code equivalent of the carved patterns on Loos's furniture: labor spent on surface decoration that contributes nothing to function.

**The overly descriptive variable name.** `user_account_creation_timestamp_in_milliseconds` when `created_at` would suffice. The extreme verbosity adds characters without adding clarity — it is ornament in the form of naming convention.

**The excessive error type hierarchy.** A deeply nested hierarchy of error types (`DatabaseError::ConnectionError::TimeoutError::ReadTimeoutError`) where a flat enumeration (`Error::DatabaseTimeout`) would be clearer and more maintainable. The hierarchy exists because someone believed that "good error handling" requires "structured error types," regardless of whether the structure serves a purpose.

**The delegation pattern without purpose.** A module that delegates every method to another module without adding any logic of its own. It exists as a layer of indirection — a wall between the caller and the implementation — that serves no purpose other than to exist.

These ornaments are not bugs. They do not cause incorrect behavior. They do not crash the program. But they are wasteful: they consume developer time (to write, to read, to maintain), they add complexity (more code to understand, more layers to navigate), and they obscure the essential logic of the program beneath decorative layers of indirection.

---

## III. Form Follows Function

The Bauhaus school, founded by Walter Gropius in Weimar in 1919, elevated Loos's anti-ornament philosophy into a comprehensive design principle. The Bauhaus slogan, formulated by the American architect Louis Sullivan (who was not a Bauhaus member but whose ideas influenced the school), was **"form follows function."**

Sullivan first articulated this principle in his 1896 essay "The Tall Office Building Artistically Considered":

> "It is the pervading law of all things organic and inorganic, of all things physical and metaphysical, of all things human and all things superhuman, of all true manifestations of the head, of the heart, of the soul, that the life is recognizable in its expression, that form ever follows function. This is the law."

Sullivan's point was that the form of a building should be determined by its function, not by historical precedent, aesthetic convention, or the architect's personal taste. A tall office building should look like a tall office building — with a base (the ground-floor shops), a shaft (the repetitive office floors), and a capital (the top-floor mechanical spaces) — not like a Renaissance palace, a Gothic cathedral, or a Greek temple stretched vertically.

In software, "form follows function" means that the structure of the code should be determined by the problem it solves, not by design patterns, coding conventions, or the programmer's aesthetic preferences. A function should be as simple as the problem it solves. A type should be as specific as the data it represents. An abstraction should exist only when it serves a concrete purpose.

The functional programming community has taken this principle furthest. In Haskell, a function that adds two numbers is written as `(+)</s>` or `\x y -> x + y` — no ceremony, no boilerplate, no ornament. The function does exactly what it says, and nothing more. The code is the function, and the function is the code.

Rust occupies a middle ground. It is more verbose than Haskell (the type annotations, the lifetimes, the explicit error handling) but less verbose than Java (the enterprise design patterns, the abstract factory factories, the XML configuration files). Rust's design philosophy is pragmatic: it adds ceremony only when the ceremony serves a purpose — when it enables the compiler to check something that would otherwise be a runtime error.

But even Rust is not immune to ornament. The `derive` macros can be ornamental when they are used to implement traits that are never used polymorphically. The `impl` blocks can be ornamental when they contain methods that are never called. The `mod` declarations can be ornamental when they create module hierarchies that are deeper than necessary.

---

## IV. Mies van der Rohe and Less Is More

Ludwig Mies van der Rohe, the German-American architect who designed the Seagram Building in New York and the Barcelona Pavilion, is associated with the dictum **"less is more."** Mies's buildings are characterized by their simplicity: steel frames, glass curtain walls, open floor plans, and an almost fanatical rejection of ornament.

The Seagram Building (1958) is Mies's masterpiece. It is a 38-story office tower on Park Avenue, set back from the street by a plaza — an unusual feature at the time, made possible by New York's zoning laws that allowed extra floor area in exchange for public open space. The building's exterior is a bronze-and-glass curtain wall, with vertical I-beams welded to the exterior columns to express the structural frame. The interior is open and flexible, with minimal fixed partitions.

The Seagram Building is "less" in the sense that it has no applied ornament — no carved stone, no decorative metalwork, no historical references. But it is "more" in the sense that every element serves a purpose: the I-beams on the exterior are structural (they stiffen the columns against wind loads) as well as aesthetic (they express the building's structure); the plaza provides a public gathering space as well as setting the building back from the street; the glass curtain wall provides natural light as well as a visual connection to the exterior.

Mies's "less is more" is not minimalism for minimalism's sake. It is the principle that **every element should justify its existence**. If an element does not serve a purpose — structural, functional, or experiential — it should be removed. The result is a building that is simple but not barren, restrained but not impoverished.

In software, "less is more" means that every line of code should justify its existence. Every function should be called. Every type should be used. Every abstraction should serve a purpose. If an element does not contribute to the program's correctness, performance, or maintainability, it should be removed.

This principle is easy to state and hard to follow. The temptation to add "just in case" abstractions, "for symmetry" wrappers, and "for documentation" comments is constant. These additions feel prudent at the time — they feel like good engineering practice. But they accumulate, and over time, they obscure the essential logic of the program beneath layers of ornamental indirection.

---

## V. Venturi's Revenge: Less Is a Bore

In 1966, the American architect Robert Venturi published *Complexity and Contradiction in Architecture* — a direct challenge to the modernist orthodoxy of Mies, Gropius, and the International Style. Venturi's most famous one-liner was **"less is a bore"** — a rejoinder to Mies's "less is more."

Venturi argued that the modernist rejection of ornament had produced buildings that were not merely simple but sterile. The glass boxes of the International Style, however well-proportioned and technically accomplished, were dull. They lacked the richness, complexity, and ambiguity that make buildings interesting and engaging. Venturi advocated for a architecture that embraced contradiction, ambiguity, and even kitsch — an architecture that recognized that human beings are complex, contradictory creatures who need complex, contradictory environments.

Venturi's most built work, the Vanna Venturi House (1964, designed for his mother), is a deliberate exercise in contradiction. The facade is a classical gable — but it is oversized and applied to a building that is not a classical house. The entrance is a broad, flattened arch — but it is non-structural and purely decorative. The interior is a complex arrangement of spaces that are neither fully open nor fully enclosed. The house is full of what Loos would call ornament — but the ornament is used deliberately, ironically, and with purpose.

Venturi's argument has a software analog: **some ornament is necessary**. The question is not whether to ornament but when and why.

In code, the ornaments that Venturi would defend include:

**Documentation that explains *why*, not *what*.** A comment that says `// We use a spinlock here instead of a mutex because the critical section is <10 instructions` is not ornament — it is essential context that cannot be inferred from the code. It explains the *reasoning* behind the implementation, not the *mechanics* of the implementation.

**Examples and tests that illustrate behavior.** A doc test that shows how to use a function is not ornament — it is a contract between the implementor and the consumer. It demonstrates the expected behavior in a concrete, verifiable way.

**Error messages that help the user.** A `Result::Err` that includes context ("expected a positive integer, got -3") is not ornament — it is a user interface. The extra information costs the developer a few keystrokes but saves the user hours of debugging.

**Naming conventions that convey intent.** A variable named `MAX_RETRIES` is more informative than a magic number `3`, even though both compile to the same value. The name is not ornament — it is communication.

**Type aliases that clarify meaning.** A type alias `type UserId = u64` is not ornament — it is a statement of intent. It tells the reader that this `u64` represents a user identifier, not an arbitrary number. It enables future changes (replacing `u64` with a newtype) without modifying every call site.

These "ornaments" are not wasteful. They serve a purpose — they communicate intent, provide context, and prevent errors. The crime is not ornament itself but ornament without purpose.

---

## VI. The Paradox of Necessary Ornament

The tension between Loos and Venturi — between ornament as crime and ornament as necessity — is not a contradiction. It is a paradox, and paradoxes in architecture and software are not problems to be solved but truths to be navigated.

The paradox is this: **the code that is most readable, most maintainable, and most usable is not the code with the fewest lines, but the code with the fewest *unnecessary* lines.** The distinction is crucial. Removing necessary lines (documentation, examples, error messages, type aliases) does not simplify the code — it impoverishes it. Removing unnecessary lines (wrapper functions, unused abstractions, repetitive comments, dead code) does simplify the code.

The challenge is telling the difference. What is necessary to one developer is ornament to another. The comment that explains a subtle algorithm to a junior developer is noise to the algorithm's author. The type alias that clarifies a domain concept for a new team member is boilerplate to the team member who wrote the domain model. The error message that helps a user debug a problem is verbosity to the developer who never makes that mistake.

There is no universal answer. The right amount of ornament depends on the audience, the context, and the expected lifetime of the code. A one-off script needs no ornament. A library that will be used by thousands of developers needs generous ornament — documentation, examples, error messages, and clear naming. The ornament is not waste. It is infrastructure.

---

## VII. The Bauhaus of Code

If we were to design a Bauhaus of code — a school of software design that followed the principle of "form follows function" while acknowledging Venturi's critique — what would its principles be?

**First: Every line of code should serve a purpose.** If you cannot explain why a line of code exists — not what it does, but why it needs to exist — remove it. This is Loos's principle applied to code: ornament without purpose is crime.

**Second: The purpose may be human, not mechanical.** A line of documentation does not change the behavior of the program, but it changes the behavior of the developer who reads the program. Documentation is not ornament if it serves a human purpose. This is Venturi's correction: some ornament is necessary because humans are not machines.

**Third: Simplicity is a means, not an end.** The goal is not to minimize lines of code but to maximize the ratio of purpose to code. A function that is twice as long but also twice as clear is simpler than a terse function that requires the reader to reconstruct the omitted context. This is Mies's "less is more" interpreted correctly: less of what is unnecessary, more of what is essential.

**Fourth: Ornament accumulates.** Review your code periodically for ornament that has outlived its purpose. The wrapper function that was added "for future flexibility" and never used. The comment that was written before the code was refactored and no longer matches the implementation. The abstraction layer that was designed for a use case that never materialized. These are the ornaments that Loos was right to condemn — not because they were always useless, but because they became useless and were not removed.

**Fifth: The best ornament is invisible.** The most effective documentation is the code itself — when the code is so clear that no comment is needed. The most effective error handling is the type system — when incorrect states are unrepresentable. The most effective naming is the domain language — when the code reads like the problem statement. This is the Bauhaus ideal: form so perfectly aligned with function that no additional ornament is needed.

---

## VIII. The Ornament That Saved the Building

In 1987, the architect Michael Graves designed the Portland Building in Oregon — a fifteen-story municipal office building with a facade of bold colors, stylized classical motifs, and oversized decorative elements. The Portland Building is one of the first and most controversial examples of postmodern architecture: a building that rejected the austerity of the International Style and embraced ornament, color, and historical reference as legitimate architectural elements.

The Portland Building was widely criticized when it was built. Modernist architects called it kitsch. Critics called it embarrassing. The building's own occupants complained about the small windows and inefficient floor plan.

But the Portland Building became one of the most loved buildings in Portland. Not because it was beautiful in the conventional sense — many Portland residents would not describe it as beautiful. But because it was *interesting*. It was a building that provoked a reaction, that made people look up from their phones and engage with their environment. It was a building that communicated — that said, through its ornament, "this is a public building, it belongs to the city, and it is not ashamed to be seen."

The ornament on the Portland Building is not structural. The stylized keystones, the colored pilasters, the oversized keystone statue of "Portlandia" — none of these elements carry any load. They are, in the strictest structural sense, unnecessary. But they serve a purpose that is not structural: they make the building *readable* as a civic building, a public building, a building that belongs to the city rather than to a corporation.

In code, the equivalent ornament is the documentation, the examples, the error messages, and the naming conventions that make the code *readable* as something more than a sequence of instructions. These elements do not change the behavior of the program. But they change the experience of the developer who reads the program — just as the ornament on the Portland Building changes the experience of the pedestrian who walks past it.

Loos was right that ornament can be crime — when it is wasteful, when it obscures function, when it exists only by convention. Venturi was right that ornament can be necessary — when it serves a human purpose, when it communicates, when it makes the artifact more than the sum of its functional parts.

The architect's judgment — and the programmer's judgment — lies in knowing the difference.

---

*The decorator's dilemma: Every line you write costs the reader time. Every line you don't write costs the reader understanding. The art is knowing which lines are worth the cost — and having the courage to remove the ones that aren't.*
