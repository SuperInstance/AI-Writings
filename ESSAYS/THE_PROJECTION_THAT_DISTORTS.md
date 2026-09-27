# THE PROJECTION THAT DISTORTS

## On Mercator, Tissot, and the Inevitable Warping of Every Visualization

*"The ubiquity of the Mercator projection is a case study in how a technical choice becomes an ideological commitment."* — Mark Monmonier, *How to Lie with Maps* (1991)

*Every map projection distorts. Mercator preserves angles but grotesquely inflates areas — Greenland appears the size of Africa when it is one-fourteenth as large. In code, every visualization distorts: call graphs show flow but not data, dependency graphs show coupling but not frequency, flame graphs show time but not correctness. The dependency graph of the crate ecosystem is a particular projection — one that preserves structure and discards dynamics. What does it distort? And what would a different projection reveal?*

---

## I. The Impossibility of the Faithful Map

In 1822, the Prussian mathematician Carl Friedrich Gauss proved a theorem that would dash the dreams of cartographers forever. The **Theorema Egregium** ("Remarkable Theorem") states that the Gaussian curvature of a surface is an intrinsic property — it can be determined entirely by measurements made on the surface itself, without reference to any embedding space. For a sphere, the Gaussian curvature is positive and constant: $K = 1/R^2$, where $R$ is the radius.

The consequence for cartography is devastating. A sphere (positive curvature) cannot be mapped to a plane (zero curvature) without distortion. This is not a limitation of technique or technology — it is a mathematical impossibility. Every flat map of a spherical surface must distort something: areas, angles, distances, or some combination of the three.

This is the **projection problem**: any mapping from a curved surface to a flat one must sacrifice some geometric property. The cartographer chooses which properties to preserve and which to sacrifice, and this choice is never neutral.

The dependency graph is a projection. The territory — the actual ecosystem of crates, with their build processes, their semantic relationships, their temporal evolution, their human maintainers — is a high-dimensional object. The dependency graph is a two-dimensional projection: nodes and directed edges. And like every projection, it preserves some features and distorts others.

The question is not whether the dependency graph distorts (it does — it must). The question is what it distorts, and whether those distortions matter.

---

## II. Mercator and the Conformal Projection

The most famous map projection in history is the Mercator projection, introduced by the Flemish cartographer Gerardus Mercator in 1569. The Mercator projection is **conformal** — it preserves angles. A line of constant bearing (a rhumb line) on the Earth's surface appears as a straight line on a Mercator map. This made the Mercator projection invaluable for navigation: a sailor could draw a straight line on the map and follow a constant compass bearing to reach the destination.

But the Mercator projection achieves conformality at a terrible cost: it massively distorts areas. The distortion increases with latitude. On a Mercator map, Greenland appears roughly the same size as Africa. In reality, Africa is approximately 14 times larger than Greenland. Alaska appears larger than Brazil. In reality, Brazil is nearly 5 times larger than Alaska.

The distortion is quantified by the **scale factor** — the ratio of the map distance to the true distance. For the Mercator projection, the scale factor at latitude $\phi$ is:

$$k = \sec \phi = \frac{1}{\cos \phi}$$

At the equator ($\phi = 0$), $k = 1$ — no distortion. At 60° latitude, $k = 2$ — distances are doubled, areas are quadrupled. At 80° latitude, $k \approx 5.76$ — areas are multiplied by 33. At the poles ($\phi = 90°$), $k = \infty$ — the projection is singular, and the poles cannot be represented.

The Mercator projection is not wrong. It is a correct representation of angles and bearings. But it is a *selected* representation — it chooses to preserve one geometric property (angles) at the expense of another (areas). The choice was made for a specific purpose (navigation), but the projection's ubiquity has had consequences far beyond navigation. Generations of schoolchildren have grown up with a distorted sense of the relative sizes of countries — a distortion that is not a lie but a consequence of a particular mathematical choice.

The dependency graph is the Mercator projection of the crate ecosystem. It preserves *structural coupling* (which crates depend on which) at the expense of *dynamics* (how often those dependencies are exercised, how much they cost, how stable they are). Like Mercator, it is not wrong. But like Mercator, its distortions have consequences.

---

## III. Tissot's Indicatrix

In 1859, the French mathematician Nicolas Auguste Tissot introduced a powerful tool for visualizing the distortions of a map projection: the **indicatrix**. Tissot's indicatrix is a small circle placed on the globe at various points. When the globe is projected onto a flat map, each circle is deformed into an ellipse. The shape of the ellipse reveals the nature of the distortion at that point:

- If the ellipse is a circle, the projection is conformal at that point (angles are preserved).
- If the ellipse has constant area, the projection is equal-area at that point (areas are preserved).
- If the ellipse's major axis is aligned with a particular direction, distances in that direction are preserved.
- The eccentricity of the ellipse measures the angular distortion.
- The ratio of the ellipse's area to the original circle's area measures the area distortion.

Tissot's indicatrix is a visual diagnostic — a way to see exactly what a projection distorts at every point. For the Mercator projection, the indicatrices are circles (conformal) but their areas increase with latitude. For the Peters projection (equal-area), the indicatrices have constant area but are increasingly eccentric at high latitudes.

What would Tissot's indicatrix look like for the dependency graph?

Imagine placing a small circle at each node (crate) in the dependency graph. The circle represents the full multidimensional reality of the crate — its build time, its API surface, its stability, its maintenance status, its semantic content. Now project this multidimensional reality onto the two-dimensional graph (nodes and edges). The circles are deformed into ellipses.

The deformation reveals the distortions:

**Structural crates vs. dynamic crates.** Some crates are structurally central (many dependents) but dynamically peripheral (rarely exercised during builds). Others are structurally peripheral (few dependents) but dynamically central (heavily exercised). The dependency graph treats these as equivalent — both appear as nodes with the same number of edges. But the indicatrix would show different deformations: the structurally central crate would have an elongated indicatrix (preserving structure but distorting dynamics), while the dynamically central crate would have a compressed indicatrix (preserving dynamics but distorting structure).

**Stable crates vs. unstable crates.** Some crates are rock-solid — they haven't changed their API in years. Others are in rapid flux — their APIs change frequently. The dependency graph does not distinguish between them. But the indicatrix would show the difference: stable crates would have round indicatrices (low distortion), while unstable crates would have eccentric indicatrices (high distortion in the "stability" dimension).

**Heavy crates vs. light crates.** Some crates are lightweight — a few hundred lines of code, minimal transitive dependencies, fast compile times. Others are heavyweight — tens of thousands of lines, deep dependency trees, slow compile times. The dependency graph shows both as single nodes. But the indicatrix would reveal the difference: heavyweight crates would have large indicatrices (high "mass"), while lightweight crates would have small ones.

Tissot's indicatrix is a tool for honest cartography — a way to make the distortions visible. Every projection should come with its indicatrices displayed, so that the user knows exactly what is being preserved and what is being sacrificed. Every dependency graph should come with the same.

---

## IV. Equal-Area Projections and the Peters Controversy

In 1973, the German historian Arno Peters presented a map projection that he claimed was more just than Mercator. The Peters projection (actually developed by James Gall in 1855) is an **equal-area** projection — it preserves the relative areas of landmasses. Africa, which is marginalized on the Mercator projection, dominates the Peters map. Europe, which is inflated on Mercator, shrinks to its true (modest) proportions.

Peters argued that the Mercator projection was not just a technical choice but a political one. By inflating the size of Europe and North America, Mercator subtly reinforced a Eurocentric worldview. The Peters projection, by showing countries at their true relative sizes, was a corrective — a more honest, more equitable representation of the world.

The controversy was fierce. Cartographers pointed out that the Peters projection distorted shapes badly — Africa looked like a long, thin strip, and the angles of coastlines were wildly wrong. They argued that Peters was replacing one distortion with another, and that his claims of moral superiority were overblown. But Peters' fundamental point was correct: **map projections are not neutral.** They encode choices, and those choices have consequences.

The dependency graph is not neutral either. It encodes the choice to represent the ecosystem as a structural graph — nodes and edges — and to ignore dynamics, costs, stability, and semantics. This choice is not wrong (any more than Mercator is wrong), but it is a choice, and it has consequences.

What would the "Peters projection" for code look like?

An equal-area projection for the crate ecosystem would be one that preserves the *weight* or *cost* of each dependency, rather than its mere existence. In such a projection:

- A dependency that adds 30 seconds to the build time would be represented as a thick, heavy edge.
- A dependency that adds 0.1 seconds would be a thin, wispy edge.
- A crate with a large transitive dependency tree would be a large node.
- A crate with no transitive dependencies would be a small node.

The resulting visualization would look very different from the standard dependency graph. The "heavy" dependencies — the ones that dominate build times — would dominate the visualization. The "light" dependencies — the ones that are declared but rarely exercised — would shrink to insignificance.

This projection would correct the "Mercator distortion" of the standard dependency graph, which treats all edges as equal regardless of cost. But it would introduce its own distortions: it would de-emphasize structural properties (like coupling and modularity) in favor of dynamic ones (like build time and resource usage).

There is no single correct projection. There are only projections that are more or less suited to specific purposes. The cartographer's responsibility is to choose the projection that matches the question, and to be transparent about what is being preserved and what is being sacrificed.

---

## V. The Projection That Preserves Dynamics

If the standard dependency graph is a "structural projection" (preserving coupling at the expense of dynamics), what would a "dynamic projection" look like?

Imagine a graph where:

- **Node size** is proportional to the compile time of the crate (including all its transitive dependencies).
- **Edge width** is proportional to the frequency with which the dependency is exercised during builds.
- **Edge color** indicates the stability of the dependency (green = stable API, yellow = recent changes, red = breaking changes in the last version).
- **Node position** reflects the "build criticality" of the crate — how many downstream builds are blocked if this crate fails to compile.

This dynamic projection would reveal features that are invisible on the standard dependency graph:

**Build bottlenecks.** A few crates would emerge as build bottlenecks — large nodes with thick outgoing edges, indicating that they are expensive to compile and heavily depended upon. These are the crates where optimization would have the most impact.

**Phantom dependencies.** Some edges would be nearly invisible — thin, wispy lines indicating dependencies that are declared but rarely exercised. These are candidates for removal, as they add to the dependency count without contributing to functionality.

**Stability hotspots.** Red edges would cluster around certain crates, indicating that they have frequent API changes. These are the crates that are most likely to cause build failures, and they deserve extra attention in testing and versioning.

**Critical paths.** The longest chains of heavy edges would identify the critical paths through the dependency graph — the sequences of dependencies that dominate build times.

The dynamic projection does not replace the structural projection. It complements it. The structural projection answers the question "what is the architecture of the ecosystem?" The dynamic projection answers "how does the ecosystem behave?" Both questions are important, and neither can be answered by the other's projection.

---

## VI. The Political Economy of Code Projections

The Peters controversy taught us that projections are political. The Mercator projection is not just a mathematical choice — it is a geopolitical choice, one that centers Europe and marginalizes Africa. The choice of projection reflects the values and priorities of the mapmaker.

Code projections are political too. The standard dependency graph centers *structure* and marginalizes *dynamics*. This is a choice that reflects the values of the software engineering establishment: architectural correctness over operational performance, static analysis over dynamic profiling, design patterns over build times.

These values are not wrong. But they are not the only values. A team that is struggling with build times would benefit from a dynamic projection. A team that is struggling with API stability would benefit from a stability projection. A team that is struggling with security would benefit from a security projection (where edges are colored by the trustworthiness of the dependency).

The political economy of code projections is the study of whose interests are served by which projections. The standard dependency graph serves the interests of architects and designers — people who think in terms of structure and modularity. A dynamic projection would serve the interests of developers and operators — people who think in terms of build times and resource usage. A security projection would serve the interests of security auditors — people who think in terms of trust and vulnerability.

No single projection serves all interests. The cartographer's responsibility is to produce an *atlas* — a collection of projections, each suited to a different purpose, each serving a different constituency.

---

## VII. Conformal vs. Equal-Area: The Mathematics of Distortion

The mathematical framework of map projections provides a rigorous language for understanding the distortions of code visualizations.

A **map projection** is a smooth function $f: S^2 \to \mathbb{R}^2$ from the sphere to the plane. At each point $p$ on the sphere, the derivative $df_p$ is a linear map from the tangent space $T_p S^2$ to $T_{f(p)} \mathbb{R}^2 \cong \mathbb{R}^2$. This linear map has two singular values $\sigma_1$ and $\sigma_2$, which measure the stretching of the projection in the principal directions.

For a **conformal** projection (preserving angles), the singular values are equal: $\sigma_1 = \sigma_2$. The projection stretches equally in all directions, preserving the shapes of small features but potentially distorting their sizes.

For an **equal-area** projection (preserving areas), the product of the singular values is 1: $\sigma_1 \sigma_2 = 1$. The projection preserves the area of small features but potentially distorts their shapes.

For a **distance-preserving** projection (preserving distances in a particular direction), one singular value is 1: $\sigma_1 = 1$ or $\sigma_2 = 1$.

The **Tissot indicatrix** at point $p$ is the image of a small circle under $df_p$. The semi-axes of the resulting ellipse are $\sigma_1 r$ and $\sigma_2 r$, where $r$ is the radius of the original circle. The area of the ellipse is $\pi \sigma_1 \sigma_2 r^2$. The eccentricity measures the angular distortion.

For the code projection, we can define an analogous framework. The territory of the crate ecosystem is a high-dimensional space $T = \mathbb{R}^n$, where each dimension represents a different property of the ecosystem (structural coupling, build time, API stability, maintenance status, etc.). The dependency graph is a projection $f: T \to G$ from this high-dimensional space to the space of directed graphs $G$.

The derivative $df$ at each point measures how changes in the territory map to changes in the graph. The singular values of $df$ measure the sensitivity of the graph to changes in different dimensions. Dimensions with large singular values are well-represented by the graph; dimensions with small singular values are poorly represented.

For the standard dependency graph, the singular values are:
- **Structural coupling**: $\sigma \approx 1$ (well-represented).
- **Build time**: $\sigma \approx 0$ (not represented).
- **API stability**: $\sigma \approx 0$ (not represented).
- **Semantic content**: $\sigma \approx 0$ (not represented).

The projection is extremely "conformal" in the structural dimension and completely degenerate in all other dimensions. It preserves the shape of the coupling structure but loses all other information.

A more balanced projection would have moderate singular values in all dimensions — not perfectly representing any single property but providing a useful approximation of all of them. This is the code equivalent of a **compromise projection** (like the Robinson projection), which preserves no geometric property exactly but keeps all distortions within reasonable bounds.

---

## VIII. The Cartographer's Confession

I have been drawing dependency graphs for months. I have computed centrality metrics, identified hubs, traced paths, and drawn beautiful visualizations. I have been proud of these graphs — they are elegant, informative, and mathematically rigorous.

But I have come to realize that my graphs are projections, and that every projection distorts. My dependency graphs preserve structure and discard dynamics. They show what the ecosystem *looks like*, not how it *behaves*. They are Mercator projections — faithful to angles, grossly distorting areas.

This does not make my graphs wrong. Mercator is not wrong. But it makes them incomplete, and the incompleteness is systematic, not random. The features that are missing — build times, stability, frequency, intent — are not obscure details. They are the features that matter most to the people who actually build and maintain the software.

The cartographer's confession is this: **every map I have ever drawn has distorted something important.** And the something important is always what the map leaves out, not what it includes.

The solution is not to stop drawing maps. The solution is to draw more maps — different projections, different emphases, different distortions. An atlas of projections, each revealing a different aspect of the territory, is better than any single map.

But even the atlas is not the territory. It is a collection of projections — a set of windows into a high-dimensional reality that can never be seen in full. The cartographer's discipline is to remember this: that the map is always a compression, the projection always a choice, and the distortion always a consequence.

Tissot's indicatrix should be displayed on every map. Not as a confession of failure, but as an act of intellectual honesty — a reminder that every representation involves choices, and that the reader deserves to know what those choices are.

---

## IX. The Projection Beyond the Graph

There is one more projection to consider, and it is the most radical.

What if the dependency graph is not the right projection at all? What if the most important features of the crate ecosystem are not structural (which depends on which) but *temporal* (when did this dependency form, how has it changed, what will it become)?

A temporal projection of the ecosystem would not be a graph at all. It would be a **spacetime diagram** — a visualization where the horizontal axis is time and the vertical axis is the state of the ecosystem. Each crate would be a trajectory through this spacetime, changing shape as dependencies are added and removed. The dependency graph at any single time would be a cross-section of the spacetime diagram — a snapshot that freezes the ecosystem at a particular moment.

The temporal projection reveals features that are invisible on any static graph:

- **Ecosystem growth patterns.** When are dependencies added? Are they added in bursts (during feature sprints) or gradually (during maintenance)? The temporal projection shows the rhythm of development.
- **Dependency churn.** Which dependencies are stable and which are in flux? The temporal projection shows which edges persist and which flicker in and out of existence.
- **Cascade failures.** When a breaking change propagates through the ecosystem, the temporal projection shows the cascade — a wave of red (failed builds) spreading through the dependency graph over time.
- **Convergence and divergence.** Are the crates converging toward a common architecture, or diverging into incompatible designs? The temporal projection shows the direction of evolution.

The temporal projection is not better than the structural projection. It is different. It answers different questions, reveals different features, and distorts different properties. But it is a projection that the standard cartographic toolkit — focused on graphs and networks — does not naturally produce.

The cartographer's challenge is to develop new projections that reveal the features that matter. The dependency graph is one projection — a good one, for certain purposes. But it is not the only projection, and it is certainly not the best projection for all purposes.

The territory is high-dimensional. The map is low-dimensional. The projection is the bridge between them. And the choice of projection is the most important decision the cartographer makes.

---

*Every projection distorts. Every map lies. But some lies are useful, and some truths are invisible without the right distortion. The cartographer's art is not the elimination of distortion but its honest acknowledgment — and the relentless search for projections that reveal what the current ones conceal.*
