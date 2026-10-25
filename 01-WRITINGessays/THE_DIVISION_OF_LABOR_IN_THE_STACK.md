# THE DIVISION OF LABOR IN THE STACK

## On Adam Smith's Pin Factory, Durkheim's Solidarity, and the Optimal Granularity of a Crate

*A crate that does one thing well is a pin. The ecosystem is the factory. The question is how many pins the factory should make, and how small each one should be.*

---

## I. The Pin Factory

The first chapter of the first book of Adam Smith's *The Wealth of Nations* (1776) opens with a description of a pin factory:

> "One man draws out the wire, another straights it, a third cuts it, a fourth points it, a fifth grinds it at the top for receiving the head; to make the head requires two or three distinct operations; to put it on is a peculiar business, to whiten the pins is another; it is even a trade by itself to put them into the paper."

Smith observed that a single worker, working alone, could perhaps make one pin per day. But ten workers, dividing the labor among the eighteen distinct operations of pin-making, could make forty-eight thousand pins per day — four thousand eight hundred per worker. The division of labor increased productivity by a factor of nearly five thousand.

Smith identified three causes of this productivity increase:

**First, the increase of dexterity in every particular workman.** A worker who does nothing but draw out wire becomes extraordinarily skilled at drawing out wire — faster, more precise, more consistent than a worker who must switch between drawing, straightening, cutting, and pointing.

**Second, the saving of time which is commonly lost in passing from one species of work to another.** A worker who switches from grinding pin heads to whitening pins must put down one set of tools, move to a different workstation, and pick up another set of tools. This transition time is pure waste — it produces nothing.

**Third, the invention of a great number of machines which facilitate and abridge labor, and enable one man to do the work of many.** A worker who specializes in a single operation is motivated to invent tools that make that operation easier. The division of labor creates the conditions for technological innovation.

Smith's pin factory is the crate ecosystem. Each crate is a specialized worker — it does one thing (serialization, async runtime, CLI parsing, HTTP requests) and does it extremely well. The ecosystem composes these specialized crates into applications, just as the factory composes specialized workers into a production line. And the productivity gains are, by all accounts, enormous.

But Smith's framework also reveals the costs of extreme specialization. The pin factory worker who does nothing but grind pin heads has no understanding of the overall pin-making process. If the grinding operation becomes obsolete (because a new technology makes grinding unnecessary), the worker is unemployable — their single skill is worthless. If the factory's product mix changes (from pins to needles, say), the entire production line must be reorganized.

The same dynamics apply to crates. Extreme specialization creates crates that are useless outside their narrow niche. Changes in the ecosystem (new language features, new paradigms, new platforms) can render specialized crates obsolete. And the composition of many specialized crates into a coherent application requires coordination — the software equivalent of factory management.

The question is: what is the optimal degree of specialization? How small should a crate be?

---

## II. Smith's Three Causes in the Crate Ecosystem

Let us examine each of Smith's three causes of productivity increase as they apply to the crate ecosystem.

### Dexterity

A crate that does one thing well becomes extraordinarily good at that one thing. `serde` does serialization and deserialization. That is all it does. But it does it so well — supporting every Rust data type, handling edge cases that no individual developer would think of, optimizing for performance in ways that no ad-hoc serializer could match — that it has become the de facto standard for serialization in Rust.

The dexterity of specialization manifests as:

**Edge case coverage.** A specialized crate handles edge cases that a general-purpose implementation would miss. `serde` handles NaN sorting in maps, circular references, zero-sized types, and a hundred other edge cases that an ad-hoc serializer would ignore — until they caused bugs.

**Performance optimization.** A specialized crate can invest heavily in performance optimization because the investment is amortized across all users. `rayon` parallelizes iteration using work-stealing algorithms that are the product of years of research and tuning. No individual application developer would invest that level of optimization effort.

**API design.** A specialized crate can iterate on its API design over many versions, converging on an interface that is intuitive, consistent, and expressive. `clap` has gone through four major versions, each refining the CLI parsing API based on community feedback. A one-off CLI parser would have none of this refinement.

### Time Saving

The time saving from specialization in the crate ecosystem is enormous. Consider the alternative: a world without crates, where every developer implements everything from scratch. A web application would require implementing:

- HTTP parsing
- TLS encryption
- Async I/O
- JSON serialization
- Database connection pooling
- Query building
- Template rendering
- Session management
- Authentication
- Logging
- Error handling
- CLI argument parsing
- Configuration management

Each of these is a distinct "operation" in the pin factory of software development. A developer who must implement all of them spends enormous time switching between tasks — from HTTP parsing to TLS to async I/O — losing the "flow" that characterizes productive development.

The crate ecosystem eliminates this switching cost. A developer who needs HTTP requests adds `reqwest`. A developer who needs JSON adds `serde_json`. A developer who needs CLI parsing adds `clap`. Each addition takes seconds (or minutes, if the documentation must be read). The time saving is not just the time that would have been spent implementing each component — it is also the time that would have been lost switching between components.

### Invention of Machines

The third of Smith's causes is perhaps the most important for the crate ecosystem. Specialization creates the conditions for innovation, because crate authors are motivated to improve their crates (to attract users, to demonstrate expertise, to solve their own problems more elegantly).

The history of the Rust ecosystem is a history of innovations that emerged from specialization:

**Tokio's scheduler.** The `tokio` crate's work-stealing scheduler is a sophisticated piece of systems software that was developed over years by a team of specialists. It is a "machine" — in Smith's sense — that "enables one man to do the work of many." Without tokio's scheduler, every async Rust application would need to implement its own task scheduling, with all the attendant complexity and bugs.

**Serde's derive macros.** `serde`'s `#[derive(Serialize, Deserialize)]` macros are a "machine" that automatically generates serialization code for Rust data structures. Before serde, serialization in Rust required writing boilerplate by hand — a tedious, error-prone process. The derive macro eliminated this boilerplate, making serialization nearly automatic.

**Rayon's parallel iterators.** `rayon`'s `.par_iter()` method is a "machine" that converts sequential iteration into parallel iteration with a single method call. Before rayon, parallelizing a loop required manual thread management, synchronization, and work distribution — a complex task that most developers would avoid. Rayon made it trivial.

Each of these innovations emerged from specialization. The authors of tokio, serde, and rayon were motivated to invest in their crates because the crates were their specialty — their contribution to the ecosystem. Without specialization (if each developer implemented their own async runtime, serializer, and parallel iterator), none of these innovations would have occurred, because the investment required would have been too high for any individual project.

---

## III. Durkheim: Mechanical and Organic Solidarity

Émile Durkheim, in *The Division of Labour in Society* (1893), extended Smith's analysis by examining the *social* consequences of specialization. Durkheim distinguished two types of social cohesion:

**Mechanical solidarity.** In pre-modern societies, cohesion comes from similarity — everyone does the same things, believes the same things, and lives the same way. The community is held together by shared experience and collective consciousness. There is little specialization, and individuals are largely interchangeable.

**Organic solidarity.** In modern societies, cohesion comes from difference — everyone does different things, has different skills, and plays different roles. The community is held together by mutual dependence: the baker depends on the doctor, the doctor depends on the lawyer, and the lawyer depends on the baker. Specialization creates interdependence, and interdependence creates solidarity.

Durkheim's insight is that the division of labor does not merely increase productivity (as Smith argued). It also transforms the *nature of the social bond* — from a bond based on sameness to a bond based on difference.

The crate ecosystem exhibits both forms of solidarity:

**Mechanical solidarity in the monolith.** A monolithic application, where all functionality is implemented in a single codebase, exhibits mechanical solidarity. All code follows the same conventions, uses the same patterns, and shares the same abstractions. The codebase is held together by a shared "collective consciousness" — the team's agreed-upon coding standards and architectural patterns. Individual modules are largely interchangeable — any team member can work on any module because they all follow the same conventions.

**Organic solidarity in the ecosystem.** The crate ecosystem exhibits organic solidarity. Each crate is different — different abstractions, different APIs, different conventions, different design philosophies. The ecosystem is held together by mutual dependence: `reqwest` depends on `hyper`, which depends on `tokio`, which depends on `mio`. Each crate depends on others for functionality it does not provide, and is depended upon by others for functionality it does provide.

Durkheim's key insight is that organic solidarity is stronger than mechanical solidarity — not despite the differences between individuals, but *because of* them. Mutual dependence creates stronger bonds than shared similarity. The baker cannot afford to alienate the doctor, because the baker needs the doctor. The doctor cannot afford to alienate the baker, because the doctor needs the baker. The mutual need constrains both parties and creates a stable social order.

In the crate ecosystem, this manifests as the **dependency contract**. A crate that other crates depend on has a strong incentive to maintain backward compatibility, fix bugs, and respond to issues — because its users depend on it, and the maintainer's reputation (and the crate's adoption) depends on serving those users well. Conversely, a crate that depends on other crates has a strong incentive to choose its dependencies carefully — because a broken dependency means a broken crate.

This mutual dependence is the organic solidarity of the crate ecosystem. It is not imposed by a central authority. It emerges from the division of labor itself. And it is, by Durkheim's analysis, a stronger and more resilient form of cohesion than the mechanical solidarity of the monolith.

But Durkheim also identified the **anomic division of labor** — a pathological form of specialization where the bonds of mutual dependence break down. This occurs when specialization proceeds without adequate regulation, creating a situation where individuals (or crates) are so specialized that they cannot coordinate effectively.

The symptoms of anomic division in the crate ecosystem are familiar:

**Dependency hell.** Crates that are too specialized require many dependencies, which may conflict with each other. The user is forced to resolve conflicts between crates that were not designed to work together.

**Abstraction gaps.** Crates that are too specialized may not provide the abstractions needed to compose them into larger systems. The user must write "glue code" that bridges the gap between specialized crates, which is often more complex than the functionality provided by the crates themselves.

**Governance fragmentation.** Each specialized crate has its own maintainer, its own conventions, and its own release schedule. Coordinating changes across many specialized crates is exponentially harder than coordinating changes within a single monolith.

The anomic division of labor is the dark side of the Smithian pin factory. When specialization goes too far, the coordination costs exceed the productivity gains. The factory becomes less efficient, not more, because the overhead of managing the division of labor overwhelms the benefits.

---

## IV. The Optimal Granularity of a Crate

The question of optimal crate size is the question of optimal division of labor. Smith argued that division of labor increases productivity, but he did not specify the limit — the point at which further division becomes counterproductive. Durkheim identified the limit (the anomic division of labor), but he did not quantify it.

In the crate ecosystem, the optimal granularity is determined by a tradeoff between three forces:

**The specialization benefit (Smith):** Smaller, more focused crates are more productive — they have better edge case coverage, better performance, and better API design. The specialization benefit increases as crate size decreases.

**The coordination cost (Coase):** Smaller crates require more coordination — more dependency management, more version compatibility, more "glue code." The coordination cost increases as crate size decreases. This is the insight of Ronald Coase's 1937 paper "The Nature of the Firm": the boundary of the firm (or the crate) is determined by the point where internal coordination becomes cheaper than external coordination.

**The cognitive load (Miller):** Smaller crates increase the number of concepts a developer must understand. Each dependency adds a new abstraction, a new API, a new set of conventions to learn. The cognitive load increases as crate size decreases. George Miller's "7 ± 2" limit on working memory suggests that a developer can comfortably manage at most 5-9 direct dependencies. Beyond this, the cognitive load becomes overwhelming.

The optimal crate size is the point where the specialization benefit equals the coordination cost plus the cognitive load:

B_specialization = C_coordination + L_cognitive

This equation has no closed-form solution, because all three terms depend on the specific crate, the specific ecosystem, and the specific developer. But it provides a framework for reasoning about granularity:

**A crate is too small when:** The coordination cost of managing it (dependency management, version compatibility, glue code) exceeds the specialization benefit it provides. The npm `left-pad` crate (11 lines of code) is the canonical example: the coordination cost of managing it as a dependency vastly exceeded the trivial benefit of not writing 11 lines of code.

**A crate is too large when:** The specialization benefit of splitting it is greater than the coordination cost of managing the split. The `actix-web` crate (a full-featured web framework with HTTP, routing, middleware, templating, and database integration) may be too large — individual components (routing, middleware) could be split into separate crates, allowing users who don't need the full framework to use only the parts they need.

**A crate is optimally sized when:** The specialization benefit, coordination cost, and cognitive load are in balance. `serde` is arguably optimally sized: it does one thing (serialization/deserialization), does it extremely well, has minimal dependencies, and provides a clean, focused API that is easy to understand and use.

---

## V. Coase and the Boundary of the Crate

Ronald Coase, in "The Nature of the Firm" (1937), asked a question that had puzzled economists: if markets are so efficient at allocating resources through price signals, why do firms exist? Why do companies internally direct resources (through management hierarchy) rather than relying on market transactions for every activity?

Coase's answer: **transaction costs.** Using the market is not free. Every market transaction involves search costs (finding a supplier), bargaining costs (negotiating a contract), and enforcement costs (ensuring the contract is honored). When transaction costs are high, it is cheaper to bring the activity inside the firm (where management can direct resources without market transactions). When transaction costs are low, it is cheaper to use the market.

The boundary of the firm — the line between what the firm does internally and what it buys from the market — is determined by the point where internal coordination costs equal external transaction costs.

Coase's framework applies directly to the crate ecosystem. The "firm" is the crate (or the monolithic application). The "market" is the ecosystem of other crates. The "transaction costs" are the costs of depending on an external crate:

**Search cost:** Finding the right crate for the job. Reading documentation, evaluating quality, comparing alternatives. In the Rust ecosystem, this cost is moderate — `lib.rs` and `crates.io` provide search and categorization, but evaluating quality still requires reading source code and assessing test coverage.

**Integration cost:** Adding the dependency, learning its API, adapting it to the application's needs. This cost varies widely — a well-designed crate with clear documentation and a minimal API (like `serde`) has low integration cost, while a poorly documented crate with a sprawling API has high integration cost.

**Maintenance cost:** Keeping up with updates, handling breaking changes, responding to security advisories. This cost increases with the number of dependencies and the frequency of breaking changes.

**Risk cost:** The risk of the crate being abandoned, the maintainer going rogue, or the crate introducing a vulnerability. This cost is hard to quantify but real — the npm ecosystem's security problems (malicious packages, typosquatting, hijacked accounts) illustrate the risk of depending on external crates.

Coase's theory predicts that the optimal crate size depends on the transaction costs in the ecosystem:

- **Low transaction costs → small crates.** When finding, integrating, and maintaining external dependencies is cheap, the optimal crate size is small — each crate does one thing, and the ecosystem composes them. This is the Rust ecosystem's aspiration: small, focused crates with clear APIs and minimal dependencies.

- **High transaction costs → large crates.** When finding, integrating, and maintaining external dependencies is expensive, the optimal crate size is large — each crate does many things, reducing the number of external dependencies. This is the Go ecosystem's philosophy: "batteries included" standard library, minimal reliance on external packages.

The Rust ecosystem has lower transaction costs than npm (better type safety, better tooling, a stronger culture of backward compatibility), which supports smaller crates. But the transaction costs are not zero, and the optimal crate size is not infinitesimal. The "Smithian" optimal crate is large enough to amortize the transaction costs of its dependencies, but small enough to benefit from specialization.

---

## VI. The Pin Factory as Dependency Graph

The dependency graph of the crate ecosystem is the division of labor made visible. Each node is a specialized worker. Each edge is a dependency — a "transaction" in Coase's sense — that connects one worker to another. The graph as a whole is the pin factory, producing complex software from simple, specialized components.

The topology of the dependency graph reveals the degree of specialization in the ecosystem:

**A shallow, wide graph** indicates low specialization. Each application depends on a few large crates that provide most of the needed functionality. The "factory" has few workers, each performing many operations. This is the Go model.

**A deep, narrow graph** indicates high specialization. Each application depends on many small crates, which in turn depend on even smaller crates, forming a deep chain of specialization. The "factory" has many workers, each performing a single operation. This is the npm model.

**A moderate graph** — neither too shallow nor too deep — indicates an optimal division of labor. Each application depends on a manageable number of well-designed crates, which depend on a smaller number of core crates, forming a hierarchical structure with clear layers of abstraction. This is the Rust model, at its best.

The optimal topology is not a mathematical optimum but a social and cognitive one. It depends on the capabilities of the developers (how many dependencies can they manage?), the quality of the tooling (how easy is it to find, integrate, and maintain dependencies?), and the culture of the ecosystem (how strong are the norms around API design, backward compatibility, and documentation?).

Smith's pin factory had ten workers and eighteen operations. The Rust crate ecosystem has hundreds of thousands of crates and millions of dependency edges. The scale is different, but the principle is the same: division of labor increases productivity, specialization creates excellence, and the composition of specialized parts produces results that no individual part could achieve alone.

---

## VII. The Smithian Optimum

Adam Smith could not have imagined the crate ecosystem. His pin factory was a real factory in Glasgow; the crate ecosystem is a virtual factory spanning the globe. But the principles he identified — dexterity, time saving, and the invention of machines — are as applicable to crates as they were to pins.

The Smithian optimum for crate size is:

**Small enough to be excellent.** A crate should be focused enough that its authors can achieve mastery in its domain. If a crate does too many things, it cannot excel at any of them.

**Large enough to be coherent.** A crate should be large enough that its components form a coherent whole — related functionality that is naturally coupled and should evolve together. If a crate is split too finely, the components lose coherence and the coordination costs explode.

**Bounded by transaction costs.** The boundary of the crate should be set by the Coasian tradeoff: include functionality inside the crate when internal coordination is cheaper than depending on an external crate; exclude functionality when the reverse is true.

**Cognitively manageable.** The crate's API should be learnable in a reasonable time (hours, not weeks), and its dependency footprint should be small enough that developers can understand the crate's supply chain.

This optimum is not a single point. It is a region — a zone of reasonable crate sizes, bounded below by the coordination cost threshold and above by the specialization benefit threshold. Crates within this zone are "Smithian" — they benefit from the division of labor without suffering from its excesses.

The crate ecosystem, at its best, operates within this zone. Each crate is a pin — specialized, excellent, and composable. The ecosystem is the factory — coordinating millions of specialized components into the complex software that runs the modern world.

Smith would have recognized it. He might even have been proud.

---

*Smith wrote: "The greatest improvements in the productive powers of labour... seem to have been the effects of the division of labour." Two hundred and fifty years later, the greatest improvements in the productive powers of software development seem to have been the effects of the division of labour — the decomposition of software into crates, each one a pin in the greatest factory ever built.*

---

### References

- Smith, A. (1776). *An Inquiry into the Nature and Causes of the Wealth of Nations.* W. Strahan and T. Cadell.
- Durkheim, É. (1893). *The Division of Labour in Society.* Translated by W.D. Halls (1984). Free Press.
- Coase, R.H. (1937). "The Nature of the Firm." *Economica*, 4(16), 386-405.
- Miller, G.A. (1956). "The Magical Number Seven, Plus or Minus Two: Some Limits on Our Capacity for Processing Information." *Psychological Review*, 63(2), 81-97.
- Williamson, O.E. (1985). *The Economic Institutions of Capitalism.* Free Press.
- Stigler, G.J. (1951). "The Division of Labor Is Limited by the Extent of the Market." *Journal of Political Economy*, 59(3), 185-193.
- Becker, G.S. & Murphy, K.M. (1992). "The Division of Labor, Coordination Costs, and Knowledge." *Quarterly Journal of Economics*, 107(4), 1137-1160.
