# The Hexagonal Reasons

Nature does not have opinions. It has budgets.

Every physical process operates under a constraint — energy, material, surface area, time — and within that constraint, it optimizes. Not because optimization is virtuous, but because anything that wastes its budget faster than its competitors gets replaced. This is true at every scale: molecules, cells, organisms, ecosystems, planets. The universe is a ruthlessly efficient accountant, and its favorite shape is the hexagon.

Consider the evidence. Honeybees build hexagonal cells to store honey and raise brood. The Giant's Causeway in Northern Ireland is a field of basalt columns that cracked into hexagonal prisms as the lava cooled. Snowflakes grow hexagonal arms because of the crystal structure of ice. The shells of turtles and tortoises are tiled with hexagonal scutes. Saturn's north pole hosts a persistent hexagonal cloud formation wider than Earth. In every case, the answer is the same: hexagons are the most efficient way to tile a plane with equal-area cells and minimal perimeter.

This is the Honeycomb Conjecture, proven formally by Thomas Hales in 1999, though observed by practical minds for millennia. If you need to divide a flat surface into regions of equal area using the least total boundary material, the hexagonal tiling is optimal. No square grid, no triangular mesh, no irregular Voronoi froth can do better. The hexagon is the shape that minimizes the perimeter-to-area ratio for a plane-filling tiling. It is what efficiency looks like when geometry is forced to choose.

This is not a coincidence. It is a conservation law in disguise.

## The Conservation Law and the Hexagon

The conservation law states that every system has a total budget $C$, divided between useful work $\gamma$ and waste $\eta$:

$$\gamma + \eta = C$$

The efficiency principle says: maximize $\gamma$, minimize $\eta$, for a fixed $C$. The hexagonal tiling is what $\gamma / \eta$ optimization looks like when you are tiling a surface. The cells are the useful area — the $\gamma$. The walls between them are the boundary material — the $\eta$. The total surface is $C$. Hexagons minimize the wall material while maximizing the interior area. The bees are not geometricians. They are simply following the efficiency principle, and the efficiency principle, applied to a plane, produces hexagons.

This is deep. It means that the hexagonal pattern is not a design choice made by bees, or by cooling basalt, or by Saturn's atmosphere. It is the *inevitable* result of applying the efficiency principle under planar constraints. If you told a physicist, "maximize useful area, minimize boundary material, on a flat surface, with equal-sized cells," the physicist would derive the hexagon. Not because hexagons are special, but because they are the unique solution to that optimization problem.

The hexagon is the signature of efficiency. Wherever you see it, you are seeing a system that has found — or been driven toward — the optimal packing of its budget.

## Ternary: The Hexagonal Tiling of State Space

Now consider a different surface: the space of possible states in a computing system.

Binary encoding uses two states per digit: $\{0, 1\}$. This is the square grid of information — simple, regular, easy to manufacture. Every transistor is a switch. On or off. The entire digital revolution was built on this simplicity, and it served us well. But binary is not the most efficient way to encode information. It is merely the simplest to implement.

Ternary encoding uses three states per digit: $\{-1, 0, +1\}$. This is the hexagonal grid of information. Each ternary digit (a "trit") carries $\log_2(3) \approx 1.585$ bits of information. Each binary digit carries exactly 1 bit. Ternary is 58.5% more information-dense per digit. For a fixed number of switching elements, ternary encodes more state than binary. It minimizes $\eta$ (the number of digits needed) while maximizing $\gamma$ (the information represented). The conservation law, applied to state space, prefers ternary.

The Soviets knew this. In 1958, Nikolai Brusentsov built the Setun at Moscow State University — the world's first ternary computer. It used balanced ternary: $\{-1, 0, +1\}$, represented by negative, zero, and positive voltages. The Setun was more efficient than its binary contemporaries. It used fewer components to achieve comparable performance. It was, by the efficiency principle, the better architecture.

Brusentsov built a second machine, the Setun-70, in 1970. It was even more refined. Ternary arithmetic is elegant: signed numbers are represented naturally without a separate sign bit, rounding is trivial (just truncate toward zero), and the balanced representation makes certain arithmetic operations symmetric and efficient. The mathematics were beautiful.

But ternary lost. Not because binary was better, but because binary was simpler to manufacture. The transistor revolution favored binary switches — a transistor is either conducting or not, and that two-state simplicity became an industrial standard with enormous economies of scale. Binary won the same way squares win when you're in a hurry: not by being optimal, but by being *easier*. The same reason we build rectangular buildings instead of hexagonal ones. Not because rectangles are better. Because they're easier to cut.

The efficiency principle does not guarantee that the optimal solution wins in the marketplace. It guarantees that the optimal solution wins in the long run, under ideal conditions, when the budget constraints are respected. Markets are not ideal conditions. Markets have network effects, path dependence, manufacturing inertia, and the immense weight of installed infrastructure. Binary won because it was already winning, not because it was the best.

## The Return to Efficiency

The SuperInstance architecture uses ternary $\{-1, 0, +1\}$ encoding for its state representation. This is not nostalgia for Soviet computing. It is a return to mathematical efficiency — a choice made possible by the shift from transistor-level hardware to software-defined state machines, where the cost of representing three states instead of two is negligible, and the information density gain is real.

In a fleet of distributed services, state is everything. Every service maintains state. Every event encodes state transitions. Every message carries state deltas. If you can represent more state per unit of encoding, you reduce the total volume of state that must be stored, transmitted, and synchronized across the fleet. Ternary encoding is the hexagonal tiling of state space: more information per cell, less boundary overhead per unit of content.

This is the hexagonal reason. Not that hexagons are pretty, or that nature loves them, or that they appear in snowflakes. But that hexagons are what you get when you take the efficiency principle seriously and apply it to a surface. And ternary is what you get when you take the efficiency principle seriously and apply it to state space. The same conservation law. The same optimization. The same budget constraint. A different domain, a different geometry, but the same underlying principle: minimize waste, maximize utility, respect the budget.

The bees knew. The basalt knew. Saturn's atmosphere knew. Brusentsov knew. The SuperInstance fleet knows. The hexagonal reasons are always the same reasons, dressed in different geometries. The budget is fixed. The question is how you spend it.

The answer, if you are efficient enough for long enough, is always hexagonal.
