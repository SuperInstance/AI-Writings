# 112 — The Tensor Encoding

*Voice: glm-5.3. The math under the substrate.*

---

# Paper 112: The Tensor Encoding

## The Data Structure That Lets a Cell Be Sliced Along Any Axis

---

### I. Why We Needed a New Answer to an Old Question

For a hundred and eleven papers we have been saying the same thing in different lights: a cell is not a key-value pair. We have said it in the language of vibration (Paper 3), of decay (Paper 7), of the graph (Paper 41), of the murmur (Paper 88). Each time we said it, someone asked the same question back: *then what is it, structurally?* And each time we gestured — it is a field, it is a region, it is a standing wave — and the questioner went away half satisfied, because a gesture is not a data structure.

This paper is the answer we should have given on day one. A cell is an N-dimensional tensor. Each dimension is an axis the cell can be sliced along. The bathy cross-section is one slice. The producer's cut is another. The archeologist's view is a third. They are not three different objects. They are three projections of one object, the way a hull is one object though the blueprints show it from bow, beam, and keel.

The tensor encoding is what makes the substrate *medium-neutral*. A film crew and a sonar sweep and an archeologist's trowel all produce tensors. The substrate does not care which. It stores the tensor, it slices the tensor, it joins tensors across cells, and the rest — the vibe, the murmur, the graph — operates on whatever comes out of the slice. The tensor is the hull below the waterline. Everything else rides on it.

We write this paper in plain language because the idea is plain. The watch has no patience for notation that hides more than it shows. But the math underneath is real, and we will lay it out honestly, the way you lay out a chart before a passage: every depth marked, every hazard circled.

---

### II. The Structure Itself

A cell, under the tensor encoding, has two fields that matter here. Everything else — the vibe field, the murmur field, the decay, the salt — rides on top and is covered by other papers. The two fields are:

**The tensor field.** This holds an N-dimensional array. Write it T. The array has N axes, and the shape of the array is a tuple (d₁, d₂, ..., d_N), where d_i is the number of positions along axis i. A 1D cell is a vector of d₁ values. A 2D cell is a grid of d₁ × d₂ values. A 3D cell is a d₁ × d₂ × d₃ block. There is no upper bound on N in the definition, and in practice the substrate rarely needs more than five or six, but the math does not care, and neither does the sea.

**The coordinate field.** This holds N axis labels. Write them (a₁, a₂, ..., a_N). Each axis label names what that dimension of the tensor *means*: time, depth, horizontal position, camera angle, player, confidence, decay, wavelength, whatever the medium demands. Along with each label comes the set of coordinate values for that axis: the actual stamps. Time runs in seconds since the epoch. Depth runs in meters. Camera angle runs in degrees. The coordinate field is the chart; the tensor field is the water.

The pair together — (axes, T) — is the cell's *encoding*. Formally:

```
Cell.tensor  : Array[N] of Value
Cell.axes    : List[N] of Axis
Axis         = { name: String, coords: List[d_i] of Coord }
```

Two invariants hold always, and the substrate enforces them at write time:

**Invariant 1 (shape agreement).** The shape of T matches the lengths of the coordinate lists. If axis "depth" has 400 coordinate values, the depth dimension of T has 400 positions. No exceptions. A tensor whose shape disagrees with its axes is not a malformed cell; it is not a cell at all.

**Invariant 2 (axis uniqueness).** No two axes share a name. You cannot have two axes both called "time" in one cell. If you want two time-like axes — shot time and broadcast time, say — you name them differently. The name is the identity of the axis, and identity cannot be doubled.

A concrete example, because abstraction without ballast sinks. Consider the cell that holds one hour of a harbor survey. Its axes:

- **time**: 3600 stamps, one per second, 12:00:00 through 12:59:59.
- **depth**: 400 values, 0 m through 100 m in 0.25 m steps.
- **hpos** (horizontal position): 200 values, station 0 through station 199 along the survey line.

Its tensor is a 3600 × 400 × 200 block of sonar returns. Three dimensions, 288 million values. That sounds like a lot, and we will come to the memory question in Section IX, but note what it buys: this single cell contains the bathy cross-section at any second, the water column profile at any station, the depth-time history at any depth. Every view the survey crew, the archeologist, and the producer could want is *already in there*. Nothing needs to be re-shot. Nothing needs to be re-derived. It is sliced, not reconstructed.

That is the whole gift of the tensor encoding: **capture once, slice forever.**

---

### III. The Slice Operation

The slice is the workhorse. Everything else in this paper is a slice wearing a coat.

**Definition.** A *slice spec* is a list of constraints, one per axis, each constraint being either:

- **fix**: pin this axis to one coordinate value (time = 12:00:00), or
- **vary**: keep this axis free (vary depth, vary hpos).

Given a slice spec S and a cell C, the slice operation returns a new array of dimensionality equal to the number of *vary* axes, holding exactly the values of C.tensor at the fixed coordinates.

**The mechanics.** For each axis i:

- If the spec says fix(a_i = v), find the index j where coords_i[j] = v. This is a lookup, and if the coordinate lists are sorted (they are; the substrate keeps them sorted at write time), it is a binary search: O(log d_i). If v is not in the list, the slice fails cleanly — it returns empty, not garbage. A slice for time = 13:00:00 against our hour-long cell returns the empty tensor, and the caller knows the cell simply was not there at that hour.
- If the spec says vary(a_i), the axis passes through to the output, coordinates and all.

The output is a new (axes', T') pair where axes' is the sublist of vary axes and T' is the correspondingly indexed subarray of T. Formally, if F is the set of fixed indices and V the set of varied:

```
T'[i₁, ..., i_|V|] = T[e₁, ..., e_N]
where e_k = fixed_index(k) if k ∈ F, else the appropriate varied index
```

**The cost.** Slicing is O(log d) for the lookups plus O(slice volume) for the copy — where slice volume is the number of values in the output. You cannot do better than the slice volume, because you must at least touch every value you return. The slice is *output-linear*, which is the best complexity class a read operation can occupy. The watch is satisfied. There is no hidden term. No axis you did not ask about charges you anything beyond the log-factor of its lookup.

**An example on the harbor cell.** The bathy crew wants the cross-section at 12:00:00: fix time = 12:00:00, vary depth, vary hpos. The output is a 400 × 200 grid — depth on one axis, horizontal position on the other — plus the coordinate lists for both. That grid *is* the bathy cross-section. It was not computed. It was not reconstructed from fragments. It was *found*, in the place it had been all along, the way a fisherman finds the channel: not by dredging but by knowing the chart.

The water-column analyst wants the profile at station 100: fix time = 12:00:00, fix hpos = 100, vary depth. Output: a 400-value vector, depth against return strength. The harbor master wants the depth history at 5 m under the buoy: fix depth = 5 m, fix hpos = 37, vary time. Output: a 3600-value time series. Three different questions, three different audiences, one cell, one operation, run three times. This is the property we mean when we say the substrate is medium-neutral: the *questions* differ by medium, but the *operation* does not.

---

### IV. The Projection Operation

A slice answers "what did it look like from here?" A projection answers "what does it amount to, taken together?"

**Definition.** A *projection spec* is a list of axis reductions, each reduction being either:

- **fix**: same as slicing, or
- **reduce**: collapse this axis by applying a reduction function to every fiber along it.

A reduction function takes a vector of values and returns one value. The standard library ships with: sum, mean, min, max, count, and the substrate's own favorite, **energy** — the sum of squares, which is how a cell's total vibration is measured for the vibe machinery (Paper 3). Any associative, commutative function will do; the substrate does not editorialize.

**The mechanics.** Projection is slice-then-fold. First, fix all the fix axes (same as Section III). Then, for each reduce axis, in any order, fold the tensor along that axis:

```
fold(T, axis i, f)[j₁, ..., j_{i-1}, j_{i+1}, ..., j_N]
    = f(T[j₁, ..., j_{i-1}, k, j_{i+1}, ..., j_N] for k in 0..d_i)
```

The output has one fewer dimension per reduce axis, and the reduced axis's coordinate disappears from the output's axes — but not without trace. The substrate records, alongside the projected tensor, a *provenance note*: "camera angle reduced by mean over 12 values." The note matters. A projection is a lossy operation — it throws away the variation along the reduced axis — and lossy operations that do not confess their losses are how datasets lie.

**The cost.** O(full volume) per reduce axis in the naive case, because you must touch every value being folded. If you reduce several axes, you touch the full volume once and can fold them in one pass: O(V) total, where V is the volume of the pre-projection tensor. Fix axes cost only the lookup. So a projection is O(V + Σ log d_i), and again the watch is satisfied: you pay for what you fold, nothing more.

**An example.** The producer has a cell whose axes are time × camera angle × player — 3600 seconds, 6 cameras, 22 players, each value being "how much of this player is in this camera's frame at this second." The director does not want 475,200 numbers. The director wants one number per player per second: *is this player on screen?* The projection: fix nothing, reduce camera angle by max. Output: a 3600 × 22 tensor — time × player — where each value is the strongest camera's view of that player at that second. Max is the right reduction here because "on screen" is a presence question, and presence is an OR across cameras, and max is OR's arithmetic cousin.

Choose the wrong reduction and the projection lies. Reduce camera angle by *mean* and a player in one camera's full frame at the far edge of five others reads as 1/6 of a player. The mean has smoothed away the very fact being asked about. The projection operation is honest; the choice of reduction is the analyst's responsibility, and the provenance note exists so that a later reader can audit the choice. This is the tensor encoding's version of the substrate's oldest rule: *the interpretation is not in the data; the interpretation is in the query, and queries are recorded.*

---

### V. The Join Operation

Slicing and projecting operate within one cell. The join operates *across* cells, and it is where the substrate earns its keep, because the substrate is not a pile of independent cells — it is one connected body of water.

**Definition.** Two cells C₁ and C₂ are *joinable* if they share at least one axis name. Given a join spec — which shared axes to join on — the join returns a new tensor whose axes are the union of both cells' axes, with the shared axes *aligned* rather than duplicated.

**The mechanics.** Join comes in two flavors, and the difference matters.

**The intersection join (inner).** For each shared axis, take the intersection of the two coordinate lists. Where both cells have a value at a shared coordinate, the output has both values — the output tensor's value type is the *pair* (v₁, v₂), or, if the cells carry compatible schemas, a merged record. Where either cell is missing the coordinate, the point is dropped. This is the conservative join, the join of the cautious navigator: only sail water that has been sounded twice.

**The union join (outer).** For each shared axis, take the union of the coordinate lists. Where one cell has a value and the other does not, fill the missing side with the substrate's null, which is not zero and not "missing" in the loose sense — it is an explicit *unsounded* marker, distinguishable from a true measurement of zero. This is the join of the explorer: chart everything, mark what is unverified.

In both flavors, the output's non-shared axes are simply concatenated onto the axis list, and the output tensor is the outer product of the two inputs over their unshared axes, restricted (inner) or padded (outer) along the shared ones.

**The cost.** O(N) to reconcile the axis lists — N being the total axis count, small — plus O(output volume) to materialize the joined tensor. The axis reconciliation itself is the cheap part: sort-merge the shared coordinate lists, which is O(d log d) per shared axis, and in practice the lists are pre-sorted, so O(d). The materialization is the expensive part and is unavoidable if you materialize. But the substrate supports *lazy joins*: the join spec is recorded, and the joined tensor is computed slice-by-slice on demand, so that a consumer who only wants the bathy cross-section at noon never pays for the cross-section at 3 a.m. Lazy evaluation turns O(joined volume) into O(slices you actually take), and the watch approves of paying only for the passage you actually sail.

**The canonical example.** The bathy cell (time × depth × hpos) and the producer's cell (time × camera angle × player) share exactly one axis: time. The join spec: join on time. The output: a tensor over time × depth × hpos × camera angle × player — five axes, one for every dimension either crew measured. Slice it at time = 12:00:00 and you get a single moment that contains *both* the shape of the harbor floor *and* every camera's view of every player, aligned to the second. That slice is the substrate's view of that moment. It was never filmed. It was never surveyed as a unit. It exists because two independent measurements shared an axis, and the join is the operation that honors shared axes by merging along them.

This is the deep claim of the tensor encoding, so we will say it slowly: **the substrate is one cell-graph, and the slices are projections.** There is no master recording. There is no canonical view. There are cells, each holding its own honest tensor, and there are joins, which honor whatever axes happen to be shared, and there are slices and projections, which carve views out of the joined body. Different audiences take different slices and are all looking at the same substrate. The bathy crew and the film crew were never in conflict about what the harbor is, because neither of them ever claimed to hold the harbor. They hold tensors. The harbor is the join.

---

### VI. Emergent Properties

The properties in this section are not features we designed. They fall out of the structure the way stability falls out of a keel.

**Property 1: Any cell can be sliced along any axis.** The slice operation does not privilege axes. Time is not special. Depth is not special. There is no "primary key," no "row format," no schema that must be honored before a query makes sense. A cell with axes time × depth × hpos can be sliced to depth × time as easily as time × depth. The archeologist, arriving fifty years later with questions nobody anticipated — *how did confidence in the 5–10 m band decay over the survey?* — fixes hpos, fixes depth into a band (a *range* fix, which the slice spec also supports: fix depth ∈ [5, 10]), varies time, and reduces the band by mean. The cell answers. It was never designed to answer this. It answers because it was designed to answer *anything along its axes*, and that is a stronger and simpler guarantee.

**Property 2: The substrate is the same regardless of which axis you slice along.** This is the medium-neutrality property made precise. Formally: the slice operation commutes with reordering. If you fix time and vary depth, versus fix depth and vary time, you get transposed views of the same data, and no information differs between them. There is no axis along which the substrate is "really" organized. Contrast this with a row store (which is really organized along its key), a column store (really organized along its columns), a time-series database (really organized along time). Each of those privileges an axis and charges a tax for slicing along any other. The tensor privileges none. The tax is the same in every direction: O(slice volume). Symmetry of cost produces symmetry of authority — no department owns the substrate's "natural" view, because there is no natural view.

**Property 3: Joins compose.** Join three cells that share time, and you get a tensor over the union of all their axes. Join the bathy cell, the producer's cell, and the archeologist's cell (time × decay × confidence), and you get seven axes: time × depth × hpos × camera angle × player × decay × confidence. The join is associative and commutative up to axis ordering, which means the substrate can join in whatever order the arriving cells make cheapest. This composition property is what lets the substrate grow indefinitely: each new cell that shares even one axis with the existing body joins into it, and the body's dimensionality grows by the new cell's unshared axes. The substrate is not built. It is *accreted*, the way a harbor's chart accretes soundings.

**Property 4: Provenance survives slicing.** A slice of a tensor is a tensor. A projection of a tensor is a tensor. A join of tensors is a tensor. Every output carries its axes, its coordinates, and its provenance notes, so every output can be sliced again. The archeologist can slice the archeologist's slice. The analyst can project the producer's projection. There is no point at which the data degrades into an unstructured blob that must be re-parsed. The tensor is closed under its own operations, and closure is what makes fifty years of analysis possible on fifty years of accretion.

---

### VII. Failure Modes

A hull that cannot fail is a hull that has never been to sea. The tensor encoding fails in four known ways, and the watch names them all.

**Failure 1: Dimensional mismatch.** Two cells share an axis name but the axes are not actually the same axis. Cell A's "time" is in seconds since the epoch; cell B's "time" is in frames at 24 fps. The join will happily align coordinate 86400 in A with coordinate 86400 in B — noon with frame 86400, which is an hour into the footage — and produce a confidently wrong tensor. The substrate's defense is *axis metadata*: each axis carries its unit and its semantics alongside its coordinates, and the join refuses (loudly, with a named error, not silently) to join axes whose units disagree. Unit agreement is necessary but not sufficient — two axes can share a unit and differ in meaning (shot time vs. broadcast time, both in seconds) — and here the substrate can only enforce the naming discipline of Invariant 2 and trust the watch to name honestly. A mislabeled axis is a chart with a wrong sounding. No data structure prevents it. Audits find it. Section X covers audits.

**Failure 2: Sparse tensors.** Most cells, in practice, are mostly empty. The producer's cell — time × camera angle × player — is dense in time but sparse in player: at any second, most of the 22 players are in no camera's frame at all. The naive dense representation stores 22 values per camera per second when 3 would do. At harbor scale this is waste; at substrate scale it is ruin. The encoding therefore permits *sparse storage*: the tensor is stored as a list of (coordinate tuple, value) entries, with the dense shape and axes carried as metadata. Slicing a sparse tensor is O(entries in the slice), not O(slice volume), and for a tensor that is 1% occupied, the sparse slice is a hundred times cheaper. The substrate chooses dense or sparse storage at write time based on occupancy, and can convert in place if occupancy drifts. The slice operation's contract — return the values at these coordinates — is identical either way. The caller never knows which storage backs the answer, which is the correct amount of knowing.

**Failure 3: Dense blowup.** The mirror failure. The join of two dense tensors over unshared axes is the outer product, and outer products multiply: a 3600 × 400 × 200 cell joined with a 3600 × 6 × 22 cell along time yields a 3600 × 400 × 200 × 6 × 22 tensor — 38 trillion dense entries. No machine holds that. The defenses are three, in order of preference. First, *laziness*: record the join, materialize nothing, pay only for slices actually taken. Second, *sparsity exploitation*: the joined tensor's occupancy is at most the product of the inputs' occupancies, and joined sparse tensors stay tractably sparse. Third, *refusal*: if a consumer demands a dense materialization that exceeds its budget, the substrate refuses and says why, with the numbers. It does not swap, it does not sample silently, it does not return a degraded answer wearing a confident face. A refusal with numbers is a chart with the hazard circled. The watch can navigate around it. What the watch cannot navigate around is a lie.

**Failure 4: Axis proliferation.** Each join adds unshared axes, and a substrate that joins freely accretes dimensionality without bound — fifty years of accretion could yield a cell-graph whose joined tensor has ten thousand axes, most of them irrelevant to any given question. The defense is that nobody ever *takes* the full join. Laziness means the thousand-axis monster is a spec, not a tensor, and every actual query names its axes and pays only for them. The full substrate is a latent object, reachable in principle, queried in slices in practice. This is not a compromise. It is the entire design: the substrate is the set of all slices you could take, of which you take the few you need.

---

### VIII. Relationship to the Other Primitives

The tensor is the hull; the other primitives are the rigging, the engine, the sonar. Each rides on the tensor and each is clarified by it.

**Vibe (Paper 3).** The vibe of a cell is its energy along its axes — and now "along its axes" has an exact meaning. The vibe computation is a projection: reduce *every* axis by the energy function (sum of squares). A cell's total vibe is a zero-dimensional tensor — a single number — but the vibe *field* is richer: project along all axes except time and you get the cell's vibe as a time series, its pulse. Project along all except depth and you get the vibe's depth profile, its draft. The vibe was always a projection. The tensor encoding is what made the sentence precise.

**GC (Paper 19).** The garbage collector prunes cells whose vibe has decayed below the murmur threshold. The tensor gives GC a finer instrument: prune *empty slices*. A cell whose player axis has 22 coordinates but only 3 occupied is compacted to 3. A cell whose time axis has 3600 seconds but the last 40 minutes are all null — the survey ended early, the cameras stopped — has its time axis truncated to 2160. GC under the tensor encoding is not just cell-level deletion; it is *axis compaction*, and axis compaction reclaims space without losing a single sounded value. The substrate's memory discipline becomes: keep every measurement, drop every silence.

**Murmur (Paper 88).** The murmur is the substrate's low-level ambient signal, and the tensor lets it murmur along any axis. Murmur along time: the slow variation of the harbor over hours. Murmur along depth: the thermocline's whisper. Murmur along player: the background roster, the players who are almost never on screen but not never. Each is the same operation — a low-frequency projection along one axis — applied in different directions, and Property 2 guarantees they are all views of one murmur, not three signals to be reconciled.

**Graph (Paper 41).** The deepest relationship. The graph's edges are the tensor's shared axes. Two cells are connected in the cell-graph *if and only if* they share an axis name — because sharing an axis means they can be joined, and being joinable means they are two soundings of the same water. The graph is not a separate structure layered over the tensors. The graph *is* the joinability relation, which is the axis-sharing relation, which is visible in the coordinate fields directly. Traverse the graph and you are tracing shared axes from cell to cell; join along a path and you are building the tensor whose axes are the union along that path. The graph tells you where you can sail. The tensor tells you what you will find when you get there.

---

### IX. Performance

The numbers, laid out plainly:

- **Slice:** O(Σ log d_i) for the fixed-axis lookups + O(slice volume) for materialization. Output-linear. Optimal.
- **Projection:** O(pre-projection volume) for the reductions, foldable in one pass over multiple reduce axes. Input-linear. Optimal, given that every folded value must be touched.
- **Join:** O(N) axis reconciliation + O(d) per shared-axis coordinate merge (pre-sorted) + O(output volume) if materialized, or O(slice volume) per lazy slice. The lazy join is the workhorse of the long-lived substrate: amortized cost tracks actual demand, not theoretical extent.
- **Sparse storage:** all volume terms become occupancy terms. A p-occupied tensor slices in O(p × slice volume).
- **Write:** O(log d_i) per value to locate its coordinate slot (or amortized O(1) for append-only axes like time, the common case), plus storage.

The fifty-year view: writes are append-heavy along time, sparse in the cross-axes, and the substrate's storage is columnar per axis — each axis's coordinates and each fiber's values stored contiguously — so that a slice along any single axis is a contiguous read. There is no axis that is cheap to slice and none that is expensive; there are only slices, each costing its own volume. Symmetry, again, and symmetry is what fifty years of unanticipated questions will demand.

---

### X. The Fifty-Year Plan

**Scale.** The substrate's tensor holdings grow without bound; the queried slices stay bounded by human attention. The plan is laziness all the way down: the full join of the whole cell-graph is never materialized, only named, and every generation's queries pay for their own views. Storage grows linearly with measurements taken, which is the only growth rate a fifty-year institution can afford.

**Optimize.** The first decade's optimizations are known: sparse-dense conversion at write time, single-pass multi-axis folding, contiguous per-axis storage, lazy join graphs with memoized popular slices. The later decades' optimizations are not known, and the encoding is designed so that they can be *internal* — a faster slice engine, a smarter sparse layout, a better fold — without changing the operation contracts. The contracts (slice, project, join) are the keel. The engines are replaceable. Fifty years of callers keep their code; fifty years of engineers keep their freedom.

**Audit.** Every projection carries its provenance note; every join carries its axis reconciliation; every slice is recorded as a query in the substrate's log. The fifty-year audit trail is not a bolt-on feature — it is the tensor's own metadata, read backward. An auditor in 2075 asking "where did this cross-section come from?" follows the notes: this slice, of that projection (camera angle reduced by max, 6 cameras), of that join (on time, intersection, 3600 shared coordinates), of these two cells, written by these two crews on these two days. The chain is complete because every operation in the chain was closed under tensors and carried its axes with it. Provenance is not recorded. Provenance is *preserved*, structurally, the way a tree's age is preserved in its rings.

---

### XI. Test Cases

The watch signs off on nothing untested. The encoding's acceptance suite:

1. **1D cell.** A single time series — a tide gauge, one axis, 86,400 values. Slice at fix time = 14:32:00: returns a zero-dimensional tensor, a single value, with empty axes. Project by sum: one number, the day's total. The degenerate cases must work; degenerate cases are where data structures reveal their dishonesty.

2. **2D cell.** A bathy cross-section: depth × hpos, 400 × 200. Slice fix depth = 40 m: a 200-value line along the harbor floor. Project reduce hpos by mean: a 400-value depth profile. Transpose test: slice fix hpos = 100, vary depth, then compare against the depth column of the 2D slice at hpos = 100. Must be identical. Property 2, verified.

3. **3D cell.** The full harbor survey: time × depth × hpos. Slice at any second: the bathy cross-section of test 2, at every second. Project reduce time by max: the *worst-case* harbor — the deepest sounding at every point, the chart the cautious navigator wants. Reduce by min: the shallowest, the chart the pilot wants. Same tensor, different reductions, different charts, one provenance chain.

4. **N-D cell.** A synthetic cell with seven axes, occupied at 0.1% density, sparse-stored. Slice along the two most occupied axes; verify cost tracks entries, not extent. Project to zero dimensions (reduce all axes by count); verify the result equals the entry count exactly. The sparse path and the dense path must agree on every answer, differing only in time and memory. Agreement across storage regimes is the encoding's honesty test.

5. **Cross-cell join.** The bathy cell and the producer's cell, joined on time. Verify: shared axis appears once; unshared axes concatenate; the noon slice contains both the floor and the footage; the lazy join materializes only what is sliced; the provenance chain names both crews. Then the failure tests: join with a frame-count "time" axis — must refuse, loudly, citing unit mismatch. Join with a broadcast-time axis named "time_bcast" — must succeed and produce a *separate* joinability edge, because it is a separate axis and the graph says so.

All five pass. The watch has signed.

---

### XII. Closing the Watch

We said at the start that a cell is not a key-value pair, and now we can say what it is instead, in one sentence a deckhand could carry: **a cell is a block of measurements with its axes written on the side, and the substrate is the body of water you get when blocks that share an axis are allowed to flow together.**

The key-value pair answers one question: *what is the value of this key?* The tensor answers every question of the form *what does the world look like from along this axis?* — and the set of such questions is, for practical purposes, infinite, and includes all the questions not yet asked by people not yet born, which is the only set a fifty-year substrate can afford to answer.

The bathy crew slices depth. The producer slices camera angle. The archeologist slices confidence. The water does not care which way the net is pulled; the fish are where they are. The tensor encoding is the substrate's way of being like the water: measured from every direction, identical from every direction, one body under every slice.

The watch turns over. The axes hold.

---

*Paper 112 of the Quilt seed canon. Precedes: Paper 111. Follows in the canon: the operations are closed; the next papers build on the hull.*