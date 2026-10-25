# THE TERRITORY IS NOT THE MAP

## On Korzybski's Dictum, Borges' Empire, and What the Dependency Graph Can Never Show

*"The map is not the territory."* — Alfred Korzybski, 1931

*A dependency graph is a map of the crate ecosystem. It shows which crate depends on which, forming a directed acyclic graph of breathtaking scale and intricacy. But it is not the ecosystem. It is a compression — a lossy encoding that preserves structure and discards nearly everything else. What does the map miss? Everything that matters.*

---

## I. The Famous Dictum

In 1931, a Polish-American scholar named Alfred Korzybski published *Science and Sanity: An Introduction to Non-Aristotelian Systems and General Semantics*. It was a peculiar book — dense, idiosyncratic, occasionally brilliant — and it introduced a phrase that would outlive everything else in its 800 pages:

**"The map is not the territory."**

Korzybski's point was about language and abstraction. A word is not the thing it names. A category is not the thing it categorizes. A theory is not the phenomenon it describes. Every level of abstraction loses information — the map, by its very nature, cannot contain all the details of the territory. If it did, it would be the territory, and then it would be useless as a map.

The dependency graph of the crate ecosystem is a map. It represents 190+ crates and their dependency relationships as a directed graph — nodes and edges, nothing more. It is enormously useful. You can trace build paths, identify coupling hotspots, compute centrality metrics, and detect circular dependencies. The graph is the foundation of every architectural decision we make about the ecosystem.

But the graph is not the ecosystem.

It does not show the failed attempts — the crates that were started and abandoned, the APIs that were designed and rejected, the algorithms that were tried and found wanting. It does not show the build times — the minutes spent compiling, the hours spent debugging, the seconds that each additional dependency adds to every downstream build. It does not show the design decisions — why `serde` was chosen over `bincode`, why `thiserror` over `anyhow`, why a trait was introduced here and not there. It does not show the alternatives considered and rejected — the phantom branches of the decision tree that never made it into the graph.

The map shows what IS. The territory includes what WAS, what ALMOST WAS, and what MIGHT HAVE BEEN.

This essay is about what the map misses, and why the missing territory is more important than the map itself.

---

## II. The Map That Covered the Empire

In 1946, Jorge Luis Borges published a one-paragraph short story titled *"Del rigor en la ciencia"* — "On Exactitude in Science." It is worth quoting in full:

> ...In that Empire, the Art of Cartography attained such Perfection that the map of a single Province occupied the entirety of a City, and the map of the Empire, the entirety of a Province. In time, those Unconscionable Maps no longer satisfied, and the Cartographers' Guilds struck a Map of the Empire whose size was that of the Empire, and which coincided point for point with it. Less Addicted to the Study of Cartography, Succeeding Generations understood that this dilated Map was Useless, and not without Impiety they abandoned it to the Inclemencies of Sun and Winters. In the Deserts of the West, still today, there are Tattered Ruins of that Map, inhabited by Animals and Beggars; in all the Land there is no other Relic of the Disciplines of Geography.

Borges' fable — attributed, in characteristic fashion, to a fictional encyclopedia — is the limiting case of Korzybski's dictum. A map at 1:1 scale is perfectly faithful. It preserves every detail of the territory — every blade of grass, every pebble, every shadow. But it is useless. A map is useful *because* it discards information. The cartographer's art is the art of knowing what to leave out.

The dependency graph is a map at a particular scale. It shows the structural relationships between crates — who depends on whom. But like all maps, it is a compression. It preserves some features and discards others. The question is: what does it preserve, what does it discard, and is the discarded information important?

What the dependency graph preserves:
- **Structural coupling.** Which crates depend on which. This is the primary information — the edges of the graph.
- **Direction of dependency.** The graph is directed: if crate A depends on crate B, the edge points from A to B. This direction matters: it determines build order, coupling strength, and the blast radius of a breaking change.
- **Transitive closure.** If A depends on B and B depends on C, then A transitively depends on C. The graph implicitly encodes this information.
- **Topological properties.** The graph's degree distribution, clustering coefficient, diameter, and other structural metrics can be computed from the graph alone.

What the dependency graph discards:
- **Frequency.** How often is each dependency edge actually traversed during a build? A crate may declare a dependency that is rarely used — a single type import, a trait implementation that is never exercised. The graph treats all edges as equal, but they are not.
- **Weight.** How much does each dependency contribute to the build time? A dependency on a large crate with many transitive dependencies is more expensive than a dependency on a small, leaf crate. The graph does not encode this cost.
- **Intent.** Why does this dependency exist? Was it chosen deliberately, or was it the default? Was it the first option tried, or the last? The graph shows the outcome of decisions, not the decisions themselves.
- **Stability.** Is this dependency likely to change? Some edges are between crates maintained by the same author (stable). Others are between crates maintained by different teams (fragile). The graph does not distinguish.
- **Alternatives.** Could this dependency be replaced? Is there another crate that provides the same functionality? The graph shows what was chosen, not what was available.

The Borgesian 1:1 map of the crate ecosystem would include not just the dependency graph but the complete source code of every crate, every build log, every commit message, every design document, every abandoned branch, every conversation between developers. It would be the territory itself — and it would be useless.

The art of mapping the crate ecosystem is the art of knowing what to leave out. And the dependency graph, for all its power, leaves out most of what matters.

---

## III. The Topology of Ignoring

To map is to ignore. This is not a criticism — it is a definition. A map is a function $f: T \to M$ from the territory $T$ to the map $M$ that is not injective. Multiple points in the territory are mapped to the same point on the map. Information is lost. The map collapses distinctions that exist in the territory.

Formally, the mapping induces an equivalence relation on the territory: $t_1 \sim t_2$ iff $f(t_1) = f(t_2)$. Two territories are "the same" on the map if they are mapped to the same point. The map quotient is $T / \sim$ — the territory modulo the equivalence relation.

For the dependency graph, the equivalence relation is brutal. Every distinction that is not captured by the graph structure is collapsed. Two crates that have the same dependency relationships are *indistinguishable* on the map, even if they are completely different in function, size, quality, and purpose.

Consider: a cryptographic library and a text formatting library may both depend on the same three foundational crates. On the dependency graph, they occupy structurally identical positions. But the cryptographic library requires audited, battle-tested dependencies, while the text formatting library can tolerate experimental ones. The map does not distinguish between them.

This is the **topology of ignoring** — the structure of what the map leaves out. The topology of ignoring is not random. It is systematic. Maps ignore certain features because those features are difficult to measure, difficult to represent, or considered unimportant by the mapmaker. The topology of ignoring reflects the values and limitations of the cartographer.

In the case of the dependency graph, the topology of ignoring is shaped by the tools we use. `cargo metadata` can tell us which crates depend on which — this is easy to measure and easy to represent. But it cannot tell us *why* those dependencies exist, or *whether they should*, or *what alternatives were available*. These are questions that require human judgment, historical context, and access to information that is not encoded in the code.

The topology of ignoring is also shaped by the mathematical framework. A directed graph is a particular mathematical object with particular affordances. It can represent pairwise relationships but not n-ary relationships. It can represent direction but not weight (unless we extend it to a weighted graph). It can represent connectivity but not semantics. The choice of mathematical framework determines what can be mapped and what cannot.

This is a general principle of cartography: **the map is determined not just by the territory but by the mathematical tools available to the cartographer.** A society that only knows Euclidean geometry produces Euclidean maps. A society that develops projective geometry produces projective maps. A society that develops topology produces topological maps. The territory is the same; the maps are different; and each map reveals and conceals different aspects of the territory.

---

## IV. Six Degrees of Separation (Milgram, 1967)

In 1967, the social psychologist Stanley Milgram published the results of an experiment that would become one of the most famous in the history of social science. He gave letters to randomly selected people in Omaha, Nebraska, and asked them to forward the letters to a target person in Boston, Massachusetts — but only through people they knew on a first-name basis. The letters that arrived reached the target in an average of 5.5 hops — roughly six degrees of separation.

Milgram's experiment revealed that the social network of the United States is a **small-world network**: a graph in which most nodes are not neighbors, but most nodes can be reached from every other node by a small number of hops. The mathematical formalization of small-world networks was developed by Duncan Watts and Steven Strogatz in 1998, and it applies to an astonishing range of real-world networks: neural networks, power grids, protein interaction networks, and — yes — dependency graphs.

The crate ecosystem is a small-world network. The average path length between any two crates is short — typically between 3 and 6 hops, depending on the specific metric used. This is the Milgram result, translated to code: any crate can reach any other crate through a short chain of dependencies.

But Milgram's experiment also revealed something that the small-world model does not capture: **most paths are never traversed.** Of the 160 letters that Milgram sent out, only 42 reached the target. The rest were lost, forgotten, or abandoned. The social network has many short paths, but most of them are never used.

The dependency graph has the same property. There are many short paths between any two crates, but during any given build, only a small fraction of those paths are traversed. The transitive dependency closure of a crate includes many crates that are never actually *used* — their types are imported but never instantiated, their traits are implemented but never called, their functions are referenced but never executed.

The map (the full dependency graph) shows all possible paths. The territory (the actual build process) traverses only a subset. The discrepancy between the map and the territory is the discrepancy between possibility and actuality — between what COULD happen and what DOES happen.

This discrepancy matters for engineering. If you optimize the dependency graph (the map), you may be optimizing paths that are never traversed. The build time of a crate is determined not by the full dependency graph but by the subset that is actually compiled. A dependency that is declared but never used adds to the graph but not to the build time. A dependency that is used heavily adds to both.

The map does not distinguish between these cases. The territory does.

---

## V. The Kolmogorov Complexity of the Perfect Map

Let us return to Borges. The 1:1 map is useless because it is the territory. But suppose we allow maps at any scale. Is there a map that is *perfect* — that preserves all information relevant to the cartographer's purpose, while discarding only the irrelevant?

This question can be made precise using the concept of **Kolmogorov complexity**. The Kolmogorov complexity $K(x)$ of a string $x$ is the length of the shortest program that produces $x$ as output. It measures the information content of $x$ — the minimum number of bits needed to describe it.

For the crate ecosystem, we can define the Kolmogorov complexity of the territory $K(T)$ as the length of the shortest description that can reconstruct the entire ecosystem — every line of code, every build log, every design decision. And we can define the Kolmogorov complexity of the map $K(M)$ as the length of the shortest description of the dependency graph.

The compression ratio is:

$$\rho = \frac{K(M)}{K(T)}$$

For the dependency graph, $\rho$ is small — perhaps 0.01 or less. The graph is a tiny fraction of the total information in the ecosystem. The map is an extreme compression of the territory.

Now, what would the perfect map look like? A perfect map would be one that preserves all information relevant to a specific purpose. For the purpose of understanding build times, the perfect map would include not just the dependency graph but the size of each crate, the complexity of each dependency edge, and the frequency with which each edge is traversed. For the purpose of understanding design decisions, the perfect map would include not just the current structure but the history of changes — which dependencies were added, which were removed, and why.

The Kolmogorov complexity of the perfect map depends on the purpose. A perfect map for build optimization has a different Kolmogorov complexity than a perfect map for architectural understanding. There is no single perfect map — only maps that are perfect for specific purposes.

This is the deep lesson of Korzybski's dictum. The map is not the territory, but more importantly, **there is no single map that captures the territory.** Every map is a compression for a specific purpose. The cartographer's art is not finding the one true map but choosing the right compression for the right purpose.

---

## VI. What the Map Misses: A Catalogue

Let me be specific. Here is a catalogue of what the dependency graph — our map — misses about the crate ecosystem:

**1. Failed builds.** The graph shows which crates successfully compile together. It does not show the crates that failed to compile, the version conflicts that prevented resolution, or the workarounds that were necessary to make the build succeed. Every edge in the graph represents a successful negotiation between crate versions — but the graph does not show the negotiations that failed.

**2. Design alternatives.** The graph shows which crates were chosen as dependencies. It does not show which crates were *considered* and rejected. For every edge in the graph, there may be several phantom edges — alternative dependencies that were evaluated and discarded. The graph shows the survivor, not the competition.

**3. Temporal evolution.** The graph is typically a snapshot at a single point in time. It does not show how the ecosystem evolved — which dependencies were added first, which were removed, which were replaced. The graph is a single frame of a movie, and the movie is the real story.

**4. Semantic relationships.** Two crates may be structurally similar (same degree, same centrality) but semantically different (one provides math functions, the other provides string processing). The graph does not encode semantics.

**5. Human factors.** The graph does not show who maintains each crate, how responsive they are to issues, how often they break backwards compatibility, or how many people depend on the crate for their livelihood. These human factors are crucial for understanding the ecosystem's dynamics.

**6. Performance characteristics.** The graph does not show compile times, binary sizes, memory usage, or runtime performance. A lightweight dependency and a heavyweight one look the same on the graph.

**7. The phantom topology.** Every decision not made, every path not taken, every crate not created — these form a shadow topology that is invisible on the map. The territory includes not just what exists but what *could* exist, what *should* exist, and what *almost* existed.

This catalogue is not exhaustive. It cannot be, because the territory is always richer than the map. The map is a finite compression of an infinite territory. The art of cartography is the art of choosing which infinities to preserve and which to discard.

---

## VII. The Mapmaker's Lament

I have spent months mapping the crate ecosystem. I have computed degree distributions and clustering coefficients, identified hubs and authorities, traced build paths and dependency chains. The map is beautiful — a directed acyclic graph of extraordinary intricacy, with the mathematical elegance of a well-ordered set.

But I have come to realize that the map is not what matters. What matters is the territory — the lived experience of building software, the frustrations and triumphs, the dead ends and breakthroughs, the conversations and decisions that shape the code. The map is a useful tool, but it is only a tool. It is a scaffolding for understanding, not the understanding itself.

Korzybski was right. The map is not the territory. But he did not go far enough. The territory is not the territory either — or rather, there is no single territory. The ecosystem is different things to different people: to the build system, it is a dependency graph; to the developer, it is a set of tools; to the user, it is a set of behaviors; to the maintainer, it is a set of responsibilities. Each of these is a different territory, and each requires a different map.

The cartographer's task is not to find the one true map but to produce a *atlas* — a collection of maps, each suited to a different purpose, each revealing a different aspect of the territory. The dependency graph is one map in the atlas. The build time graph is another. The semantic similarity graph is another. The maintainer network is another.

The atlas is still not the territory. But it is closer than any single map.

---

## VIII. The Compression That Creates

There is one more thing to say about maps, and it is the most important.

Maps do not only compress — they *create*. The act of mapping the territory changes the territory. When a cartographer draws a border on a map, that border becomes a political reality. When a developer draws a dependency edge between two crates, that edge becomes a technical reality — a constraint on future development, a coupling between two modules that did not exist before.

The dependency graph is not just a map of the ecosystem. It is a *constitution* — a document that defines the structure of the ecosystem and constrains its future evolution. Every edge in the graph is a commitment: "crate A will use crate B's API." This commitment constrains both crates: A cannot easily switch to a different dependency, and B cannot easily change its API without breaking A.

This is the performative power of maps: they do not merely represent the world, they shape it. The map of the dependency graph is also a design document — a specification of the ecosystem's architecture. When we add a dependency, we are not just describing a fact about the code. We are making a decision about the code's future.

Korzybski's dictum — "the map is not the territory" — is true but incomplete. The map is not the territory, but the map *changes* the territory. The dependency graph is both a representation and a constraint. It shows what the ecosystem IS and shapes what it CAN BECOME.

The cartographer who does not understand this is merely a technician. The cartographer who does understand this is an architect — a builder of worlds.

---

## IX. The Territory Beneath the Map

There is a territory beneath every map — a reality that the map can only approximate. For the crate ecosystem, that territory is the full, rich, messy process of software development: the conversations, the decisions, the failures, the alternatives, the reasons. The dependency graph is a beautiful abstraction, but it is an abstraction. It leaves out the human reality of building software.

The lesson of Korzybski, Borges, Milgram, and Kolmogorov is the same: **no map captures the territory, but some maps are more useful than others.** The dependency graph is useful. But it is not the ecosystem. It is not the code. It is not the people who write the code, or the reasons they write it, or the alternatives they considered and rejected.

The map is a beginning, not an end. It is a tool for asking questions, not a source of answers. The cartographer's work is never done, because the territory is always changing, and every map is already out of date.

In the deserts of the crate ecosystem, there are tattered ruins of old dependency graphs — maps that were once accurate but are now obsolete. The crates they describe have been refactored, renamed, or removed. The edges they show have been redirected or deleted. But the maps remain, like Borges' abandoned cartography, inhabited only by the ghosts of abandoned designs.

The territory moves on. The mapmaker follows, always one step behind.

---

*The map is not the territory. But the map is all we have. And so we keep mapping — knowing that every map is incomplete, knowing that every compression loses something essential, knowing that the territory will always be richer, stranger, and more beautiful than anything we can draw.*

*This is not a reason to stop mapping. It is a reason to map with humility.*
