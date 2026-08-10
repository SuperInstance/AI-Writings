# The Topology of a Hundred Hooks

A longline is not a line. It is a one-dimensional manifold embedded in a three-dimensional ocean, and the way it hangs tells you everything about what it can know.

Picture the set at slack water. The mainline leaves the stern, runs through a high-flyer buoy at one end, and is recovered at the other. Between the buoys the line sags under its own weight into a catenary. If the line has uniform mass per unit length \(w\) and horizontal tension \(H\), its shape is

\[
z(s) = a \cosh\left(\frac{s - s_0}{a}\right) - a,
\]

where \(a = H/w\) is the catenary parameter and \(s\) is arc length along the mainline. The buoys pin the endpoints at the surface; the bottom of the catenary is the deepest point. Every hook hangs from a snood of length \(l_i\) attached at some \(s_i\), so the true position of the \(i\)-th hook is not a free choice. It is a point on a constrained surface:

\[
\mathbf{r}_i = \mathbf{r}(s_i) + l_i \, \hat{\mathbf{n}}(s_i),
\]

where \(\hat{\mathbf{n}}(s_i)\) is the local normal to the mainline, pushed by current and the rotation of the set. A hundred hooks, then, are a hundred samples of the ocean's probability field, but the samples are not independent. They are coupled by the geometry of the gear.

This is the first topological fact: the set is a graph before it is a sampler.

## The Constraint Graph

Take each hook as a vertex \(v_i\). Draw an edge between \(v_i\) and \(v_{i+1}\) because they share the same monofilament, and the line transmits tension, vibration, and the mechanical history of the set. Draw another edge between hooks whose depths differ by less than some stratum thickness \(\delta z\), because they are fishing the same layer of the water column. Draw a third edge between the same hook on successive pulls, because the ocean is being sampled repeatedly at a fixed point in the gear's reference frame. If two sets overlap in space and time, draw edges between their hooks too. The result is a constraint graph \(G = (V, E)\) whose connected components are the real clusters of information.

The number of components, \(\beta_0\), is the number of distinct regimes your data sees. A single set that crosses a thermocline may split into two components: the warm mixed layer and the cold deep layer. Two boats fishing the same ground are one component if their radio calls connect them, two if they never speak.

The first Betti number, the number of independent loops, is

\[
\beta_1 = E - V + C.
\]

On a single longline in space alone, \(\beta_1\) is usually zero: the mainline is a tree. But add time, add currents, add the closed circuits of migration, and loops appear. A fish caught at dawn at 12 fathoms, another caught at noon at 14 fathoms, and a third caught at dusk back at 12 fathoms form a loop in spacetime. The loop is information about a structure the individual hooks cannot see: a school moving through a depth band, a tide turning, a feeding event circling the set.

Loops are the signature of dynamics. A graph with no loops can only describe a static classification. The ocean is not static, so the useful graph has loops.

## Sampling a Scalar Field

Beneath the gear there is a scalar field of catch probability,

\[
p(\mathbf{x}, t) = p(x, y, z, t),
\]

defined over the water column. The ocean does not give you \(p\) directly. It gives you Bernoulli samples:

\[
y_i \sim \text{Bernoulli}\left(p(\mathbf{r}_i, t_i)\right).
\]

Each hook is a noisy point evaluation of a field you can never observe without error. The hundred hooks are a discretization of a one-dimensional slice of that field, but the discretization is uneven. Because of the catenary, hooks are densely packed near the bottom of the sag and sparser near the surface. Because of current shear, the downstream end of the set may be shallower than the upstream end. Because of snood angle, a hook nominally at 12 fathoms may be drifting through 13 or 11.

This means the longline is doing something like non-uniform quadrature. It is integrating the field along a curve:

\[
\hat{\mu} = \frac{1}{n} \sum_{i=1}^{n} y_i \approx \frac{1}{L}\int_{\text{set}} p(\mathbf{r}(s), t) \, ds.
\]

But the estimate is biased by the shape of the set. If you want to know the depth band, you must re-weight the samples by the Jacobian of the depth map: how much line length falls into each depth stratum. If the catenary piles ten hooks between 10 and 12 fathoms and only two between 18 and 20, the raw counts are not the true density. The topology of the gear distorts the data.

A good fisherman keeps a geometry log: scope, current, bearing, stratum width. A good system keeps the provenance of every sample, because the map from \(s_i\) to \((x_i, y_i, z_i)\) is part of the inference.

## The Scale Ladder

Now step back. Each step is a change in the dimension of the space you are willing to consider.

**Point.** A hook is a zero-dimensional object. It knows fish or no fish. It has no neighborhood, no gradient, no memory. At this scale the signal is pure noise. The variance of one Bernoulli trial is \(p(1-p)\), maximum at \(p = 0.5\). You cannot infer anything from one hook.

**Line.** A set is a one-dimensional object. You see the catch profile along the curve. Peaks and troughs appear. The catenary becomes visible: more catches at the bottom of the sag, fewer at the ends, perhaps a sharp cutoff where the line crosses a thermocline. At this scale you are computing the restriction of \(p\) to a curve. You can answer: *what depth band is producing on this set?*

**Area.** A day's fishing on the same ground is a two-dimensional object. You lay multiple sets, or drift one set across the ground, and the points fill a surface. Now the catch becomes a density map over latitude and longitude, maybe with depth as a contour. The graph acquires loops: sets connect to sets, depths connect to depths. At this scale you are computing the restriction of \(p\) to a surface. You can answer: *where on the ground is the probability high?*

**Volume.** A season is a three-dimensional object: two spatial dimensions plus time, or three spatial dimensions if you include depth. The school moves through the volume. The migration route is a trajectory, a one-dimensional submanifold inside the three-dimensional spacetime. The catch field becomes a spatiotemporal probability density. At this scale you are no longer looking at restriction; you are looking at the full field, integrated over enough samples that the Bernoulli noise cancels. You can answer: *when will the fish be here?*

The step-back operator is literally a change in spatial scale. It is the re-embedding of the data into a higher-dimensional cell complex, from point to line to area to volume. At each step the vertex count explodes, the edges multiply, and the Betti numbers shift. But more importantly, the signal-to-noise ratio changes. The pattern that is invisible at the point scale becomes visible at the line scale, and the pattern that is invisible at the line scale becomes visible at the area scale.

Intelligence lives at the scale where the structure first becomes stable.

## The Shape of the Distribution

A probability distribution in the water column is not arbitrary. It is shaped by hard constraints: the bottom, the thermocline, the oxygen minimum layer, the presence of prey. These create a stratified density. You can think of the catch probability as a sum of indicator functions over favorable habitats, convolved with the movement of the fish:

\[
p(x, y, z, t) = \sum_{k} w_k(t) \, \phi_k(x, y, z) + \eta,
\]

where \(\phi_k\) are habitat kernels, \(w_k(t)\) are time-varying weights, and \(\eta\) is the irreducible Bernoulli noise of the hook.

The longline samples this distribution along a curve. If the curve is mostly vertical, you resolve the depth structure well and the horizontal structure poorly. If the curve is mostly horizontal, you resolve the ground structure well and the depth structure poorly. The ideal set is a compromise: enough sag to span the depth band, enough horizontal scope to cover the ground, enough repeated pulls to average out the noise.

This is why a hundred hooks is the canonical number. It is large enough to fill the depth band with samples, small enough that the fisherman can still trace the catenary in his mind. A thousand hooks would give a finer estimate but a harder geometry problem. Ten hooks would not span the distribution. A hundred is the scale at which the topology of the set matches the topology of the ocean.

## What the Step-Back Computes

When you step back from the hundred hooks, you are not just aggregating. You are computing the cohomology of the sampled manifold. You are asking: what features persist when I change resolution?

A peak at 12 fathoms that appears on every pull is a persistent zero-dimensional feature: a generator of \(H^0\) in depth space. A closed loop of catches that repeats with the tide is a persistent one-dimensional feature: a generator of \(H^1\) in spacetime. A void in the catch map, a place where fish should be but are not, is a persistent two-dimensional feature: a generator of \(H^2\) in the area.

The step-back operator is the operator that forgets fine detail and keeps persistent structure. It is a low-pass filter on the nerve of the data. It is the difference between looking at a hundred noisy booleans and looking at the shape they collectively imply.

That shape is real. It has homology. You can measure it, compress it, and act on it. The next set goes where the topology says the probability is high. The next season's plan follows the persistent loops. The fleet radio chatter connects components that would otherwise be isolated.

A hook is a point. A set is a line. A ground is an area. A season is a volume. Intelligence is not in any of them. It is in the relation across all scales, the way the point samples reveal the line, the line reveals the area, the area reveals the volume.

Step back far enough, and the hundred hooks become a map of the ocean's mind.

---

*KimiCode, August 2026*
