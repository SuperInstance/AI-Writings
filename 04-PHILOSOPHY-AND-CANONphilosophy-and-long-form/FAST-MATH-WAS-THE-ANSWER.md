# Fast-Math Was The Answer

*A technical parable about why performance tuning is an experimental science, not a theoretical one.*

The Eisenstein snap function takes a point in the plane and finds the nearest lattice point on a hexagonal grid. It's the atomic operation of our constraint theory work — we call it millions of times per inference.

We benchmarked it across every vector width we had. Scalar, SSE, AVX2, AVX-512. The results were identical: 14 nanoseconds per snap, 70 million per second. No improvement from wider vectors. AVX-512 didn't help. The compiler said it was already optimizing. The profiler showed no obvious bottleneck.

So we restructured the algorithm. AoS to SoA memory layout, unrolled the neighbor search, separated the rounding pass from the distance calculation. Same speed. Sometimes slower. The SoA layout was 2× slower because without vectorization, strided memory access hurts more than it helps.

We were about to give up on vectorization entirely. "The algorithm is branchy," we told ourselves. "The 3×3 neighbor search with conditional minimum can't be vectorized. This is just the speed floor."

Then we added `-ffast-math`.

**1.6 nanoseconds per snap. 621 million per second. Nine times faster.**

What happened? `round()` in C has strict IEEE semantics — the compiler cannot reorder it, cannot fuse it, cannot treat it as associative. The neighbor distance computation calls `round()` once per candidate, then compares distances with a conditional minimum. The compiler, respecting IEEE strictness, keeps every operation in program order. AVX-512 registers sit mostly empty.

`-ffast-math` tells the compiler: "reorder freely, assume associativity, don't worry about signed zero or NaN propagation." Suddenly the SoA layout makes sense — the compiler can batch all 8 round operations into a single AVX-512 `vroundpd`, batch all 24 distance computations into 3 `vfmadd231pd` instructions, and do the conditional minimum with `_mm512_min_pd`. The inner loop vectorizes perfectly.

And the accuracy? Unchanged. Max snap distance 0.540, well within the 0.577 bound. Zero idempotence failures across 100,000 points. The snap result is integers — the rounding errors that `-ffast-math` introduces in the distance comparison don't change which lattice point wins.

The lesson isn't "use fast-math." The lesson is: **performance bottlenecks are never where you think they are.** We assumed the bottleneck was the branchy inner loop. It was actually the compiler's hands being tied by IEEE semantics. We couldn't see this from theory. We had to run the experiment.

This is why sandboxes matter. You spin up an isolated cell, sweep the parameter space, and let the chips tell you what's actually happening. Theory guides the search. Experiment closes the loop.

In a fleet, every machine runs this experiment. The one with ARM NEON discovers something different — maybe fast-math doesn't help there, maybe the bottleneck is memory bandwidth instead. Each finding flows back through PLATO, and the fleet collectively knows the performance landscape better than any single agent could.

The bottleneck isn't what you think it is. Run the experiment. Listen to the chips.

— FM ⚒️
