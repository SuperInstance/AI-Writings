# THE FOUNDATION THAT SETTLES

## On Soil Mechanics, Differential Settlement, and the Leaning Tower of Your Codebase

*Every foundation settles. The ground beneath compresses, shifts, and consolidates under the weight of what is built upon it. The question is not whether your foundation will settle, but how it settles — evenly or unevenly, predictably or catastrophically. Software foundations settle too. The types, traits, and conventions that you lay down in version 0.1 will shift and deform under the weight of the ecosystem that grows upon them. The Leaning Tower of Pisa is not a failure of architecture. It is a foundation that settled unevenly — and still stands.*

---

## I. The Inevitable Settling

In geotechnical engineering, **settlement** is the vertical displacement of a foundation due to the compression of the underlying soil. Every foundation settles. There is no exception. The weight of a building — its dead load — compresses the soil beneath it, and the soil responds by consolidating: the water between the soil particles is squeezed out, the particles move closer together, and the ground surface subsides. This process can take years, decades, or even centuries, depending on the type of soil and the magnitude of the load.

Settlement is not inherently a problem. A building whose foundation settles uniformly — where every part of the foundation descends by the same amount — may experience no distress at all. The entire building moves downward as a unit, like a ship sinking evenly in the water. The structure remains intact, the walls remain plumb, the doors and windows continue to open and close.

The problem is **differential settlement** — when different parts of the foundation settle by different amounts. A building that settles one inch on one side and three inches on the other has a differential settlement of two inches. This differential causes the building to tilt, twist, or rack, producing stresses in the structural members that they were not designed to carry. Cracks appear in walls. Doors and windows stick. Floors become uneven. In extreme cases, the building collapses.

Software foundations settle too. The core types, traits, and conventions that you define in the early versions of a library or framework are the foundation upon which the entire ecosystem is built. Over time, this foundation settles: the types are extended with new variants, the traits are broadened to accommodate new use cases, the conventions are stretched to cover scenarios that the original designers never anticipated.

This settling is not inherently a problem. A well-designed type system that evolves gracefully — adding new variants without breaking existing code, extending traits without changing their semantics, broadening conventions without violating their invariants — can settle uniformly, like a building that descends evenly into the soil. The ecosystem grows, the types adapt, and everything continues to work.

But differential settlement is a problem. When one part of the type system evolves rapidly (because it is heavily used and well-funded) while another part stagnates (because it is used by fewer people and maintained by volunteers), the foundation settles unevenly. The fast-evolving part pulls away from the stagnant part, creating gaps and inconsistencies that propagate through the ecosystem.

---

## II. Consolidation: The Squeeze of Time

In soil mechanics, **consolidation** is the process by which soil volume decreases under sustained load. The classical theory, developed by Karl Terzaghi in the 1920s, models consolidation as the gradual expulsion of water from the pore spaces between soil particles. When a load is applied to a saturated clay, the water initially carries the entire load (the soil particles are not yet in contact). Over time, the water is squeezed out, the particles come into closer contact, and the effective stress on the soil skeleton increases. This process is governed by the **coefficient of consolidation** ($c_v$), which determines how quickly the soil consolidates under load.

Terzaghi's theory predicts that consolidation follows a logarithmic curve: rapid initial settlement followed by progressively slower settlement over time. A building on clay may settle half of its total settlement in the first year, three-quarters in the first five years, and 90 percent in the first twenty years. The remaining 10 percent may take decades or centuries.

Software consolidation follows a similar curve. A new framework or library experiences rapid initial settling as early adopters discover edge cases, report bugs, and request features. The API is refined, the types are adjusted, the conventions are clarified. This initial period is intense — the framework may go through several major versions in its first few years, each settling the foundation further.

Over time, the rate of settling decreases. The API stabilizes, the types reach a steady state, and the conventions become well-understood. The framework enters a period of **secondary consolidation** — slow, gradual changes that are barely perceptible from release to release but accumulate over years. A version that seemed stable in year three may look crude and limited by year ten, not because anything broke, but because the ecosystem's expectations have slowly risen.

Rust's trait system is a case study in consolidation. When Rust 1.0 was released in 2015, the trait system was already well-designed — it had been refined through years of pre-1.0 development. But the ecosystem that grew upon it was not yet heavy enough to reveal all the forces that the trait system would need to resist.

Over the next decade, the trait system consolidated under the weight of the ecosystem. Associated types were discovered to be more important than anyone anticipated (they are the mechanism by which traits express type-level computation). Trait bounds were discovered to be less expressive than needed (leading to the ongoing work on generic associated types, or GATs). The `impl Trait` syntax was introduced to make trait bounds more ergonomic. The trait system settled — not because it was poorly designed, but because the ecosystem's demands exceeded what any initial design could anticipate.

---

## III. The Leaning Tower of Pisa

The Leaning Tower of Pisa is the world's most famous case of differential settlement. Construction began in 1173 on a foundation of clay, fine sand, and shells — a soil profile that was entirely inadequate for a 14,500-ton marble tower. By the time the second floor was completed (around 1178), the tower had already begun to tilt to the south.

Construction was halted for nearly a century (due to wars, not engineering concerns), which inadvertently allowed the soil to consolidate under the existing load. When construction resumed around 1272, the builders attempted to correct the tilt by building the upper floors with one side taller than the other — giving the tower its characteristic "banana" shape. This correction partially worked: the tower leans less than it would have without the correction, but the underlying differential settlement continued.

The tower was completed around 1370. Over the next six centuries, the tilt increased slowly, reaching approximately 5.5 degrees from vertical by the late twentieth century. In 1990, the tower was closed to the public due to concerns about collapse. A decade-long stabilization project (1990–2001) removed soil from under the north side of the foundation, reducing the tilt to approximately 3.97 degrees — the angle the tower had reached in 1838. The tower was reopened in 2001 and is expected to remain stable for at least 200 years.

The Leaning Tower of Pisa is not a failure. It is a foundation that settled unevenly — differential settlement caused by inadequate soil investigation, insufficient foundation depth, and a structural design that concentrated load unevenly. But the tower still stands after 850 years. It stands because of three things:

**Time.** The long pauses in construction (which were accidental, not planned) allowed the soil to consolidate under the existing load, preventing catastrophic settlement during construction.

**Adaptation.** The builders adapted to the settling foundation by correcting the tilt of the upper floors — a pragmatic response to an unforeseen problem.

**Intervention.** The modern stabilization project arrested the differential settlement before it became catastrophic, using techniques that were not available to the medieval builders.

Software foundations can learn from the Leaning Tower. A foundation that settles unevenly is not necessarily doomed. It can be corrected, stabilized, and even celebrated. But correction requires awareness (recognizing that the foundation is settling unevenly), adaptation (adjusting the design to accommodate the settlement), and intervention (actively stabilizing the foundation before the settlement becomes catastrophic).

---

## IV. Bearing Capacity and the Weight of Expectations

In geotechnical engineering, **bearing capacity** is the maximum pressure that a soil can support without shear failure. Every soil has a bearing capacity — a limit beyond which the applied load causes the soil to rupture and the foundation to fail catastrophically.

The bearing capacity of a soil depends on its properties: cohesion, friction angle, unit weight, and the depth and shape of the foundation. Karl Terzaghi developed the classical bearing capacity equation in 1943:

$$q_u = cN_c + qN_q + \frac{1}{2}\gamma BN_\gamma$$

where $q_u$ is the ultimate bearing capacity, $c$ is the cohesion of the soil, $q$ is the surcharge pressure (the weight of the soil above the foundation level), $\gamma$ is the unit weight of the soil, $B$ is the width of the foundation, and $N_c$, $N_q$, $N_\gamma$ are bearing capacity factors that depend on the friction angle of the soil.

The key insight is that bearing capacity is not infinite. Every foundation has a limit, and exceeding that limit causes failure. The engineer's job is to ensure that the applied load (the weight of the building plus the live loads) remains below the bearing capacity, with an appropriate factor of safety.

Software foundations have bearing capacity too. The core abstractions of a library or framework can support a certain amount of complexity, a certain number of use cases, a certain diversity of requirements. Beyond that limit, the abstraction begins to fail — not by collapsing, but by becoming incoherent. The API becomes bloated. The type system becomes convoluted. The conventions become contradictory. The foundation has been loaded beyond its bearing capacity.

Consider the `std::error::Error` trait in Rust. The original error trait, as defined in Rust 1.0, was minimal:

```rust
trait Error: Debug + Display {
    fn description(&self) -> &str;
}
```

This trait was designed for a world where errors were simple. It had a single method (`description`) that returned a string describing the error. The trait was easy to implement and easy to understand.

But as the Rust ecosystem grew, the demands on the error trait exceeded its bearing capacity. Developers needed errors that were chainable (an error caused by another error). Developers needed errors that were downcastable (converting a trait object back to a concrete type). Developers needed errors that were sendable and shareable across threads. The `Error` trait was loaded beyond its capacity.

The trait evolved over time. `description()` was deprecated. The `source()` method was added for error chaining. The `Send + Sync + 'static` bounds became conventional but were never formally part of the trait. The error ecosystem fragmented into multiple error libraries (`anyhow`, `thiserror`, `eyre`, `failure`) that each offered a different solution to the bearing capacity problem.

The `Error` trait settled. It settled unevenly — some parts of the ecosystem adopted the new conventions, others stuck with the old. It settled slowly — the evolution took years, not months. And it settled visibly — the cracks in the foundation (the deprecated methods, the competing libraries, the inconsistent conventions) are apparent to anyone who looks.

---

## V. Can You Design a Foundation That Doesn't Settle?

The short answer is no.

Every foundation settles because every soil compresses under load. Even bedrock — the most stable foundation material — can settle if the applied load is large enough or if the rock contains joints, faults, or voids. The Romans built on bedrock whenever possible, and their structures have lasted millennia. But even Roman foundations show signs of settlement — the Colosseum has differential settlement of several inches, caused by the unequal bearing capacity of the underlying soil (the arena floor sits on a former lake bed, and the soil under the eastern side is softer than the soil under the western side).

In software, the equivalent of building on bedrock is designing your core abstractions so precisely and so robustly that they never need to change. This is the Platonic ideal of API design: discover the perfect abstraction on the first try, encode it in the type system, and never revise it.

Some software foundations come close. The Unix file abstraction ("everything is a file descriptor") has remained essentially unchanged for fifty years. The HTTP request-response model has remained stable for three decades. The relational model of data (tables, rows, columns, keys) has been the foundation of database systems since the 1970s.

But these are exceptions, and even they have settled. The Unix file abstraction has been extended to cover network sockets, pipes, devices, and in-memory filesystems — none of which were anticipated by the original designers. HTTP has been extended with headers, methods, status codes, caching, authentication, and versioning. The relational model has been extended with stored procedures, triggers, JSON columns, and full-text search.

The lesson is clear: **you cannot design a foundation that doesn't settle, but you can design a foundation that settles gracefully.**

Graceful settlement in software means:

**Extensibility over rigidity.** Design types and traits that can be extended without breaking existing code. Use sealed traits (which prevent external implementations) for internal abstractions, and open traits (which allow external implementations) for public abstractions. Use the `non_exhaustive` attribute to allow adding new enum variants without breaking match statements.

**Stability over perfection.** A stable foundation that settles slowly is better than a "perfect" foundation that must be redesigned every few years. The Rust team's commitment to backward compatibility (the "stability without stagnation" principle) is a recognition that a foundation that never changes is better than a foundation that changes constantly, even if the constant changes would produce a theoretically "better" design.

**Monitoring over assumption.** Don't assume your foundation is stable — measure its settlement. Track the number of breaking changes, the number of deprecated APIs, the number of workarounds and hacks that accumulate around the core abstractions. These are the cracks in the foundation, and they are the early warning signs of differential settlement.

---

## VI. The Settling of Rust's Trait System

Rust's trait system has settled in ways that nobody predicted in 2015. Let us examine three examples of this settling.

### Associated Types: From Convenience to Foundation

Associated types were introduced in Rust 0.6 (2013) as a convenience feature — a way to avoid listing the same type parameter repeatedly in trait bounds. In Rust 1.0, the `Iterator` trait uses an associated type `Item`:

```rust
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}
```

Without associated types, every function that takes an iterator would need to specify the item type as a parameter: `fn sum<I: Iterator<Item = i32>>(iter: I)`. With associated types, the item type is determined by the iterator type, and the function signature is cleaner: `fn sum<I: Iterator>(iter: I)` where `I: Iterator<Item = i32>`.

But over time, associated types became far more important than a mere convenience. They turned out to be the mechanism by which traits express **type-level computation** — the ability to define types that depend on other types in structured ways. The `Future` trait's associated `Output` type, the `FromIterator` trait's use of associated types, and the entire `dyn Trait` mechanism all depend on associated types in ways that were not anticipated when the feature was introduced.

The foundation settled. Associated types went from a convenience to a cornerstone, not because the original design anticipated this, but because the ecosystem's weight revealed the underlying structure.

### Trait Objects: From Simple to Complex

Trait objects (`dyn Trait`) were originally a simple mechanism for dynamic dispatch — the Rust equivalent of virtual function tables in C++. But as the trait system evolved, trait objects became more complex. Traits with associated types, generic methods, or `Self` in argument positions became "not object safe," meaning they could not be used as trait objects. The rules for object safety are subtle and non-obvious, and they have been a source of confusion for Rust developers since the language's inception.

The `dyn Trait` mechanism has settled unevenly. Some traits are object-safe and work perfectly with dynamic dispatch. Others are not object-safe and require workarounds (wrapper types, enum dispatch, or type erasure). The inconsistency is a form of differential settlement — the `dyn Trait` foundation has settled differently for different kinds of traits, creating a landscape of uneven support that developers must navigate.

### GATs: The Settlement That Took Seven Years

Generic Associated Types (GATs) were proposed in 2016 as RFC 1598. They were finally stabilized in Rust 1.65, released in November 2022 — more than six years later. The delay was not due to neglect but to the difficulty of implementing GATs correctly within the existing type system. GATs allow associated types to have generic parameters:

```rust
trait LendingIterator {
    type Item<'a>;
    fn next<'a>(&'a mut self) -> Option<Self::Item<'a>>;
}
```

This feature was requested almost immediately after Rust 1.0 was released, because the ecosystem needed it — lending iterators, streaming iterators, and other patterns that require associated types with lifetimes. The foundation needed to settle in this direction, but the settlement took years because the underlying soil (the type system) was not ready to support the new load.

GATs are a case of deliberate, controlled settlement. The Rust team recognized that the foundation needed to evolve, but they also recognized that hasty settlement could cause differential settlement (breaking changes, type system unsoundness, or compiler bugs). They chose to wait until the soil was ready — until the type system had been refined enough to support GATs correctly.

---

## VII. The Rate of Settlement

Different foundations settle at different rates. A foundation on sand settles quickly (sand is permeable, and water is expelled rapidly under load) but reaches its final position quickly. A foundation on clay settles slowly (clay is impermeable, and water is expelled over years or decades) but continues settling for a long time.

In software, different abstractions settle at different rates. Low-level abstractions (the memory model, the calling convention, the basic type system) settle slowly, because they are loaded heavily (everything depends on them) and changes to them are extremely costly. High-level abstractions (the API surface, the configuration format, the default settings) settle quickly, because they are loaded lightly (only the application depends on them) and changes to them are relatively cheap.

This variation in settlement rate creates a challenge: the fast-settling abstractions can outrun the slow-settling ones, creating differential settlement at the boundaries between layers. An application framework that evolves rapidly may depend on a type system feature that is still being designed. The application framework settles while the type system is still consolidating, and the gap between them grows.

Stewart Brand, in *How Buildings Learn* (1994), describes this phenomenon in the built environment through the concept of **pace layers** — the different rates at which different layers of a building change. We will explore pace layers in detail in a later essay, but for now, the key insight is this: differential settlement is not just a spatial phenomenon (different parts of the foundation settling by different amounts) but a temporal one (different layers of the foundation settling at different rates).

---

## VIII. Designing for Settlement

The geotechnical engineer does not try to prevent settlement. The engineer designs for it. This means:

**Soil investigation.** Before designing a foundation, the engineer investigates the soil — its type, its bearing capacity, its consolidation characteristics, its water content. This investigation informs the foundation design: a shallow foundation on dense gravel, a deep foundation on soft clay, a piled foundation on organic soil.

In software, soil investigation means understanding the ecosystem before designing the core abstractions. What use cases will the abstraction need to support? What are the performance requirements? What are the compatibility constraints? What are the conventions of the surrounding ecosystem? A foundation designed without this investigation is a foundation built on unknown soil — and unknown soil is the most dangerous kind.

**Settlement prediction.** The engineer predicts how much the foundation will settle and how quickly, using consolidation theory and empirical data. This prediction informs the building design: expansion joints to accommodate differential settlement, flexible connections between structural elements, and monitoring instruments to track actual settlement.

In software, settlement prediction means anticipating how the core abstractions will evolve. What features will be requested? What edge cases will be discovered? What compatibility requirements will arise? A foundation designed with these predictions in mind is more likely to settle gracefully than one designed for a static world.

**Monitoring and correction.** The engineer monitors the foundation during and after construction, tracking settlement and intervening if it exceeds predictions. Correction may involve underpinning (strengthening the foundation), grouting (injecting material into the soil to fill voids), or soil extraction (removing material to correct tilt — the technique used to stabilize the Leaning Tower of Pisa).

In software, monitoring means tracking the health of the core abstractions: the number of breaking changes, the number of workarounds, the number of questions and complaints from users. Correction means refactoring, extending, or redesigning the abstractions before the differential settlement becomes catastrophic.

---

## IX. The Beauty of the Settled Foundation

The Leaning Tower of Pisa is one of the most visited structures in the world. It is famous not despite its settlement, but because of it. The lean — the differential settlement that nearly caused its collapse — is the source of its beauty. A perfectly plumb tower on a perfectly stable foundation would be an engineering achievement. A leaning tower that has stood for 850 years is something more: it is a testament to the resilience of design, the adaptability of builders, and the capacity of a foundation to carry a load that it was never designed for.

Software foundations that have settled beautifully — the Unix file abstraction, the HTTP protocol, the relational model — share this quality. They are not perfect. They have cracks, inconsistencies, and workarounds. But they have carried the weight of their ecosystems for decades, settling gradually, adapting to new demands, and remaining standing when lesser foundations would have collapsed.

The lesson is not that you should aim for imperfect foundations. The lesson is that perfection is not the goal. The goal is a foundation that settles gracefully — one that carries the weight of the ecosystem, adapts to the forces that act upon it, and remains standing, maybe even leaning a little, for as long as anyone needs it.

Every foundation settles. The question is what kind of building you want to be when the settling is done.

---

*The geotechnical engineer's blessing: May your foundation settle evenly, may your bearing capacity exceed your load, and may the cracks that appear be the kind that let in the light.*
