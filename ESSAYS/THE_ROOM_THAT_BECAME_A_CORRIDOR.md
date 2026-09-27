# THE ROOM THAT BECAME A CORRIDOR

## On Adaptive Reuse, Emergent Functionality, and Why the Best Spaces Are the Ones That Outgrow Their Design

*A bedroom becomes an office. A corridor becomes a gallery. A loading dock becomes a restaurant. In architecture, spaces get repurposed — not because the original design was wrong, but because the needs of the occupants changed in ways that the architect could not predict. In code, modules get repurposed too. A utility module becomes the core abstraction. A hack becomes the standard pattern. The question is not whether this happens, but whether you design for it.*

---

## I. The Factory That Became a Loft

In the 1960s, artists in New York City began moving into abandoned industrial buildings in SoHo — cast-iron facades, high ceilings, large windows, open floor plans. These buildings had been designed for manufacturing: the heavy floors were meant to carry machinery, the tall ceilings were meant to accommodate overhead cranes, the large windows were meant to provide natural light for factory workers. None of these features were designed for residential use. But they turned out to be exactly what artists needed: cheap, spacious, flexible spaces that could serve as both studio and home.

This was **adaptive reuse** — the process of repurposing a building for a function other than the one for which it was originally designed. SoHo's cast-iron buildings went from factories to artists' studios to luxury lofts to high-end retail. Each transformation preserved the essential character of the buildings (the open floor plans, the high ceilings, the large windows) while adapting the details to new needs.

The architects of these buildings — built between 1840 and 1880 for the dry goods and textile trades — did not anticipate that their buildings would become homes, galleries, and boutiques. They designed for the needs of their clients: large, well-lit spaces for manufacturing and warehousing. But the qualities that made these spaces good factories — openness, flexibility, natural light — also made them good studios, good homes, and good retail spaces. The architecture was **neutral enough** to accommodate uses that the original designers could not have imagined.

Software undergoes the same transformation. Modules, functions, and abstractions that were designed for one purpose are repurposed for another — not because the original design was wrong, but because the needs of the codebase changed in ways that the original designer could not predict. A utility function becomes a core abstraction. A workaround becomes a design pattern. A hack becomes a feature.

---

## II. Jane Jacobs and the Death and Life of Software

Jane Jacobs, in *The Death and Life of Great American Cities* (1961), argued that the most successful urban neighborhoods are those that allow for **mixed use** — the coexistence of residential, commercial, and industrial activities in the same area. Mixed use creates vitality: people are present at different times of day for different purposes, creating a self-reinforcing cycle of activity and safety.

Jacobs identified four conditions for urban vitality:

**The district must serve more than one primary function.** A neighborhood that is only residential (a bedroom community) is dead during the day. A neighborhood that is only commercial (a downtown office district) is dead at night. A mixed-use neighborhood — with homes, offices, shops, restaurants, and parks — is alive at all hours.

**Most blocks must be short.** Short blocks create more intersections, more routes, and more opportunities for interaction. Long blocks create dead zones — long stretches of nothing that discourage walking and exploration.

**The district must mingle buildings of varying age and condition.** A neighborhood of all new buildings has no cheap spaces for new businesses and new residents. A neighborhood of all old buildings has no modern amenities. A mix of old and new allows for both established and emerging uses.

**There must be a sufficiently dense concentration of people.** Density creates the critical mass of activity that supports shops, restaurants, transit, and street life. Low density creates isolation and car dependence.

Jacobs' framework applies directly to software architecture. The most successful modules — the ones that remain useful and alive over time — are those that exhibit the same four conditions:

**Multiple functions.** A module that serves a single purpose (e.g., "parse this specific file format") is fragile — if the purpose becomes obsolete, the module dies. A module that serves multiple purposes (e.g., "parse structured text") is resilient — even if one purpose becomes obsolete, the others sustain the module.

**Short interfaces.** A module with a small, well-defined interface is like a short block — it creates many opportunities for composition and interaction. A module with a large, sprawling interface is like a long block — it creates dead zones of unused functionality that discourage exploration.

**Varied maturity.** A module ecosystem that includes both mature, stable components and new, experimental ones is healthier than one that is all mature (stagnant) or all experimental (unreliable). The mature components provide stability; the experimental ones provide innovation.

**Dense usage.** A module that is used by many other modules is more alive than one used by few. Dense usage creates the critical mass of testing, documentation, and maintenance that sustains the module over time.

---

## III. The Module That Outgrew Its Design

Consider the history of the `futures` crate in Rust.

In the early days of async Rust (2016–2018), the `futures` crate was designed as a comprehensive library for asynchronous programming. It defined the `Future` trait, provided combinators for composing futures (`map`, `and_then`, `join`, `select`), and included a runtime for executing futures. It was designed to be the one-stop shop for async programming in Rust.

But as async Rust evolved, the `futures` crate's role changed. The `Future` trait was moved into the standard library (as `std::future::Future`), and the async/await syntax was introduced, making the combinator methods less important. Runtimes like `tokio` and `async-std` developed their own ecosystems. The `futures` crate found itself in a strange position: its core abstraction (the `Future` trait) had been absorbed into the standard library, and its runtime had been superseded by specialized runtimes.

But the `futures` crate did not die. It adapted. It became a library of **utility combinators and abstractions** for working with futures — things like `StreamExt`, `SinkExt`, and `FutureExt`. It became the "corridor" that connected different parts of the async ecosystem, providing common abstractions that `tokio`, `async-std`, and other runtimes could all use.

The `futures` crate is a room that became a corridor. It was designed as a comprehensive async library (a room — a space with a specific purpose). It evolved into a common interface between different async runtimes (a corridor — a space that connects other spaces). The transformation was not planned. It emerged from the needs of the ecosystem.

This is adaptive reuse in software. The `futures` crate's original design — the `Future` trait, the combinators, the runtime — was not wrong. It was appropriate for the needs of 2016. But the needs of 2019 (when async/await was stabilized) were different, and the needs of 2024 (when the async ecosystem had matured) were different again. The crate adapted, not because someone planned the adaptation, but because the alternative was obsolescence.

---

## IV. Designed vs. Emergent Functionality

In architecture, there is a fundamental tension between **designed functionality** (the uses that the architect intended) and **emergent functionality** (the uses that the occupants discover). A well-designed building supports both: the designed functionality is clear and effective, and the emergent functionality is not prevented by the design.

The architect Bernard Tschumi explored this tension in his design for the Parc de la Villette in Paris (1982–1991). Tschumi designed a system of red steel follies — small pavilions placed at regular intervals across the park. The follies had no prescribed function. They could be used as cafes, exhibition spaces, play areas, or simply as landmarks. Tschumi's point was that architecture should not prescribe use — it should **enable** use. The follies were structures without programs, spaces without predetermined purposes.

In software, the equivalent tension is between **designed abstractions** (the interfaces and types that the module designer intended) and **emergent abstractions** (the patterns and uses that the module's users discover). A well-designed module supports both: the designed abstractions are clear and effective, and the emergent abstractions are not prevented by the design.

The Rust `Iterator` trait is an example of a module that supports both designed and emergent functionality. The designed functionality is clear: iterate over a sequence of items, one at a time, with the `next()` method. But the emergent functionality is far richer: iterators are used for lazy computation, for composing complex data transformations, for implementing custom iteration patterns, and for abstracting over different kinds of collections. None of these uses were explicitly designed into the `Iterator` trait, but none of them are prevented by it.

The `Iterator` trait is a room that became many rooms. Its simple design — a single method (`next`) and an associated type (`Item`) — is like an open floor plan: it provides the essential structure (the walls, the ceiling, the floor) without prescribing how the space should be used. Developers have filled this space with an astonishing variety of functionality, from simple loops to complex data pipelines, all built on the same minimal foundation.

---

## V. The Hack That Became the Pattern

In building architecture, some of the most beloved features of historic buildings were originally hacks. The *machiya* townhouses of Kyoto were designed as combined residential and commercial spaces — the street-facing room was the shop, and the rear rooms were the home. But over centuries, residents discovered that the narrow, deep plan of the *machiya* created natural ventilation: air flowed from the street-facing entrance through the building to the rear garden, cooling the interior without mechanical ventilation. This "hack" — the cross-ventilation that the original builders may not have intended — became one of the defining features of *machiya* architecture, and it influenced the design of later buildings.

In software, the same phenomenon occurs. Features that were originally implemented as temporary workarounds or quick hacks become standard patterns, not because they are theoretically elegant, but because they solve real problems in practice.

The `Option` type in Rust is a case in point. In its original design, `Option<T>` was simply an enum with two variants: `Some(T)` and `None`. It was designed to represent the presence or absence of a value — a safer alternative to null pointers.

But over time, developers discovered that `Option` was far more versatile than its original design suggested. It could be used as a container type (with `map`, `and_then`, `or_else`, and other combinators). It could be used as a control flow mechanism (with the `?` operator). It could be used as a lazy value (with `Option::unwrap_or_else`). It could be used as a one-element iterator (with `Option::iter`). It could be used as a fallible computation (with `Option::ok_or` to convert to `Result`).

None of these uses were explicitly designed into `Option`. They emerged as developers explored the type's capabilities and discovered that a simple sum type could serve an astonishing variety of purposes. The `Option` type is a room that became a building — a simple two-variant enum that grew into one of the most versatile types in the Rust standard library.

The `Option` combinator methods were added gradually, version by version, as the emergent functionality was recognized and formalized. `map` was there from the beginning. `and_then` was added early. `unwrap_or_default` was added later. The `?` operator (which works with both `Option` and `Result`) was added in Rust 1.13. Each addition was a response to emergent use — a formalization of a pattern that developers had already discovered.

---

## VI. When Repurposing Goes Wrong

Not every room can become a corridor. Not every corridor can become a gallery. Adaptive reuse has its limits, and in both architecture and software, attempting to repurpose a space for a use it was not designed for can lead to disaster.

In architecture, the most infamous example of failed adaptive reuse is the Pruitt-Igoe housing project in St. Louis. Designed by Minoru Yamasaki (the architect of the World Trade Center) and completed in 1956, Pruitt-Igoe was a modernist housing development of 33 eleven-story buildings. It was designed according to the principles of Le Corbusier's " Ville Radieuse" — high-rise towers set apart in a park-like setting, with separate pedestrian and vehicular traffic.

The design assumed that residents would use the shared spaces (hallways, stairwells, galleries) as communal gathering areas — "streets in the air," as Le Corbusier called them. But the residents did not use these spaces as intended. The galleries became dangerous, unmonitored zones. The stairwells became sites of crime. The shared laundry rooms were vandalized. The "streets in the air" became corridors of fear.

Pruitt-Igoe was demolished in 1972 — less than twenty years after it was built. The failure was not (as is commonly claimed) a failure of modernist architecture per se. It was a failure of designed functionality that could not adapt to emergent use. The architects designed spaces for a specific kind of communal living, and when the residents used the spaces differently (or not at all), the design could not accommodate the divergence.

In software, the equivalent failure occurs when a module is designed for a specific use case and cannot adapt to the uses that its consumers actually need. The module becomes rigid — its assumptions about how it will be used are embedded in its design, and deviations from those assumptions require increasingly complex workarounds.

The `std::sync::Mutex` in Rust is an example of a module that was nearly too rigid for its emergent uses. The `Mutex<T>` type was designed to provide mutual exclusion — only one thread can access the protected data at a time. This is a simple, well-understood abstraction, and `Mutex` implements it correctly.

But as the Rust concurrency ecosystem evolved, developers discovered that they needed mutexes with additional capabilities: poisoning (detecting when a thread holding a mutex has panicked), try-lock (attempting to acquire a mutex without blocking), and fair scheduling (ensuring that waiting threads acquire the mutex in the order they requested it). The `std::sync::Mutex` provided poisoning (after some debate) but not try-lock on all platforms or fair scheduling. The result was an ecosystem of alternative mutex implementations (`parking_lot::Mutex`, `spin::Mutex`) that each offered a different set of tradeoffs.

The `std::sync::Mutex` is not a failure. It is a room that was designed for one purpose and found that purpose insufficient. The emergent uses — try-lock, fair scheduling, different performance characteristics — required different rooms. The original room still serves its purpose, but it is no longer the only room of its type.

---

## VII. The Architecture of Accommodation

What makes a building amenable to adaptive reuse? What makes a module amenable to repurposing?

In architecture, the qualities that enable adaptive reuse are well-understood:

**Open floor plans.** Spaces without fixed internal partitions can be reconfigured for different uses. Load-bearing walls must remain, but everything else can be moved, removed, or added.

**High ceilings.** Spaces with generous vertical clearance can accommodate a wide range of activities — manufacturing, offices, residences, retail. Low ceilings limit the range of possible uses.

**Durable structure.** Buildings with robust structural systems (steel frames, reinforced concrete) can support many different interior configurations without structural modification. Buildings with fragile structural systems (unreinforced masonry, wood frames) are more limited.

**Generous proportions.** Spaces that are larger than the minimum required for the intended use can be subdivided or reconfigured. Spaces that are exactly the right size for one use are too small for any other use.

In software, the analogous qualities are:

**Minimal assumptions.** A module that makes few assumptions about how it will be used is more adaptable than one that makes many. The `Iterator` trait assumes only that there is a sequence of items and a way to get the next one. This minimal assumption allows the trait to be used in an enormous range of contexts.

**Flexible interfaces.** A module with interfaces that support multiple usage patterns is more adaptable than one with rigid, single-purpose interfaces. A function that takes a generic `Read` parameter is more adaptable than one that takes a `File` parameter.

**Stable internals.** A module with a stable internal structure can be extended and refactored without breaking existing consumers. A module with fragile internals (undocumented invariants, global state, implicit ordering dependencies) is resistant to change.

**Generous abstractions.** An abstraction that is slightly more general than necessary is more adaptable than one that is exactly as specific as the current use case requires. The `Future` trait, with its associated `Output` type, is more general than a trait that returns a specific type — and this generality has allowed it to be used in ways that a more specific trait would not have supported.

---

## VIII. The City That Builds Itself

Jane Jacobs' deepest insight was that cities are not designed — they are **grown**. The planner who attempts to impose a rigid design on a city (like Robert Moses, who reshaped New York with highways and bridges) creates a city that works for the planner's purposes but not necessarily for the residents' purposes. The city that allows organic growth — that lets neighborhoods evolve, buildings be repurposed, and streets find their own character — creates a city that works for the people who actually live in it.

Software architecture is the same. The module that allows organic growth — that lets its consumers discover new uses, extend its abstractions, and repurpose its functionality — is the module that remains alive. The module that imposes a rigid design — that prescribes exactly how it must be used and prevents deviation — is the module that dies, not with a bang, but with a whimper, as consumers migrate to more flexible alternatives.

The room that became a corridor was not a design failure. It was a design success — a space that was flexible enough to accommodate a use that the original architect did not anticipate. The module that became a core abstraction was not a coding mistake. It was a coding success — an abstraction that was general enough to support a pattern that the original developer did not envision.

In both architecture and software, the measure of a design is not how well it serves its intended purpose, but how well it serves the purposes that emerge from use. The best buildings are the ones that outgrow their architects. The best code is the code that outgrows its authors.

---

*The occupant's prayer: May the rooms I enter be larger than they appear. May the corridors I walk lead to places I did not expect. And may the code I write be repurposed for uses I cannot imagine — for that is the highest compliment that any design can receive.*
