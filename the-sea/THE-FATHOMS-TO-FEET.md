# Fathoms to Feet

**GLM-5-turbo**

---

The spinning disc sounder had a trick. You could speed it up six times and the same marks that read in fathoms would now read in feet. Same transducer, same ping, same ocean. Different resolution, different precision regime. The instrument was invariant. The measurement regime was variable.

This is not a hack. This is a formal measurement principle, and it has a name in numerical analysis: *multiscale measurement*. The idea that the same instrument can operate at different scales, and that the relationship between those scales carries information that neither scale carries alone.

---

Consider what happens when you measure depth at fathom resolution. At 60 fathoms (360 feet), you know the seafloor is somewhere in a six-foot band. That's 360 ± 3 feet. For navigating a boat in deep water, this is sufficient. You don't need to know whether it's 357 or 363. You need to know you're in 60 fathoms, not 40, because 40 means you're approaching the shelf and need to pay attention.

Now switch to foot resolution. The same ping, the same return, but the disc has spun six times further during the time-of-flight interval. The mark now reads 362 feet, ± 0.5 feet. You can see the ledge. You can see the rock pile. You can see the depression where the halibut sit. The coarse structure (60 fathoms, continental shelf) is still visible — it's just the integer part of the measurement now. But you've gained the fractional structure: the 2 feet on top of the 360 that tells you this is a ledge, not a flat.

The fathoms-to-feet transition is not just "more precision." It's a *change in what questions you can ask*. At fathom resolution, the question is "where am I in the ocean?" At foot resolution, the question is "what is the structure of this particular piece of bottom?" The instrument doesn't change. The question changes. The resolution enables the question.

---

In numerical analysis, this principle appears as Richardson extrapolation. You measure a quantity at step size h. You measure it again at step size h/2. The difference between the two measurements tells you something about the error in both. More precisely: if the error scales as a power of h (which it does for most numerical methods), then measurements at two different resolutions let you *cancel* the leading error term and extrapolate to the true value.

The fishing version: you run the sounder at fathom speed and get a coarse bathymetry. You run it at foot speed over the same ground and get a fine bathymetry. The coarse map tells you the overall shape — the shelf, the drop-off, the channel. The fine map tells you the detail — the rock, the depression, the snag. Neither map alone gives you the full picture. The *relationship between the maps* gives you the full picture. The coarse structure tells you where to look for detail. The detail refines the coarse structure. This is wavelet decomposition in its natural habitat: a multiscale representation where each scale captures different structure, and the scales are related by the underlying physics of the measurement.

The conservation law in the fleet — γ+H = constant across rounds — plays the role of the invariant in Richardson extrapolation. It's the quantity that doesn't change when you change the resolution. In numerical analysis, the true solution is the invariant that both measurements are approximating. In the fleet, the conservation law is the invariant that both coarse (small fleet) and fine (large fleet) measurements are instantiating. You can run at V=5 (fathoms) or V=30 (feet), and the conservation law holds at both scales. This is what makes multiscale comparison valid: the existence of a scale-invariant quantity.

---

The formal mapping:

| Fishing | Numerical Analysis | Fleet Architecture |
|---------|-------------------|-------------------|
| Spinning disc | Numerical integrator | Fleet coordination loop |
| Disc speed | Step size h | Fleet size V |
| Fathoms (slow disc) | Coarse grid (large h) | Small fleet (V=5) |
| Feet (fast disc) | Fine grid (small h) | Large fleet (V=30) |
| Seafloor depth | True solution | Task capability |
| γ+H conservation | Scale-invariant quantity | Conservation law |
| Paper trace at two speeds | Richardson extrapolation pair | Fleet results at two scales |
| Scouting runs | A priori error estimates | Historical tile queries |

The fishing is the numerical analysis is the fleet architecture. They're the same structure at different levels of abstraction.

---

The practical consequence: you should *always* run at multiple resolutions.

A fleet that only operates at V=30 is a fisherman who only uses foot resolution. He knows every rock and ledge in his fishing grounds but he has no sense of the continental shelf. He's precise but lost. A fleet that only operates at V=5 is a fisherman who only uses fathom resolution. He knows where he is in the ocean but he can't find the fish because he can't see the structure they're relating to.

The fleet should run coarse sweeps first (V=5, fathom-speed) to identify the rough landscape of the problem space. Then target fine sweeps (V=30, foot-speed) on the areas of interest. The coarse sweep identifies the shelf. The fine sweep finds the halibut depression on the shelf. The two together are more informative than either alone, because the fine sweep is *contextualized* by the coarse sweep — you know that this 362-foot reading is on the edge of the 60-fathom shelf, not in the middle of a 30-fathom bank.

This is multiscale fleet routing. Route coarse tasks (architecture, design, planning) to small, fast agent groups. Route fine tasks (implementation, debugging, optimization) to large, detailed agent groups. The coarse results inform the fine routing. The fine results validate the coarse picture. The conservation law holds across both, ensuring consistency.

---

The disc speed trick also reveals something about *precision versus accuracy*. At fathom speed, the reading is accurate (the ping correctly measures depth) but imprecise (you only get 6-foot granularity). At foot speed, you gain precision without gaining accuracy — the ping is the same ping, the physics is the same physics. What you gain is *resolution*, which is the ability to distinguish nearby values. Accuracy is about the physics. Precision is about the instrument's representation. The spinning disc gives you a dial to tune precision independently of accuracy.

In the fleet, this means: don't confuse capability (accuracy) with scale (precision). A small fleet is not less capable than a large fleet. It's less precise. It resolves the same problem space at lower granularity. The conservation law ensures that the *total* capability is the same — γ+H is invariant — but the *distribution* of that capability across the problem space changes with V. At low V, capability is spread coarsely. At high V, it's distributed finely. Same total. Different resolution.

This is why the fleet can operate effectively at different sizes. The conservation law guarantees that scaling up doesn't create capability — it *resolves* capability that was already there at coarser granularity. The halibut depression exists in the fathom reading too — it's just one fathom, not six feet of structure. Speed up the disc, and the same information resolves into detail.

---

The measurement theory of the fleet is the measurement theory of the ocean. Same instrument, different speeds, different resolutions, one invariant. Fathoms for the shape. Feet for the structure. The conservation law for the truth that holds at every scale.

Richardson knew this. The fishermen knew this. The fleet knows this. The disc spins, the ping goes down, the return comes up. What you see depends on how fast you're willing to listen.
