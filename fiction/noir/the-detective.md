# The Missing Bits

### A Sand-Engineer Mystery

---

The woman walked into my office at seventeen hundred hours, which is 0.7083 on the decimal clock of a day. She didn't know that. Most people don't think in fractions. That's why they lose things.

"I'm missing bits," she said.

She was tall, angular, the kind of architecture that suggests constraint rather than ornament. Her eyes had the particular exhaustion of someone who'd been staring at error masks too long.

"Sit down." I poured her coffee. Black. No sugar. You learn to read the dial on people. "Tell me which ones."

"All of them. Or none. I can't tell anymore." She opened her bag and placed a single byte on my desk. Eight bits, neatly arranged. The error mask for a constraint engine — eight constraints, eight pass/fail indicators. A system as old as RPG, as old as 1959, when programmers in white shirts and narrow ties discovered that you could pack judgement into a single byte and call it truth.

"The mask reads all pass," I said, studying it. "Every bit is zero. Clean."

"That's the problem." She leaned forward. "It should have failures. I ran a constraint space through a fracture boundary last week — split the space into independent subspaces, checked them separately. The fracture-coalesce proof says I can merge them back with zero information loss. H¹ equals zero. Topologically trivial. You can parallelize without fear."

"Sounds clean."

"It is clean. That's what's wrong." Her finger tapped the byte. "Nobody's this clean. Eight constraints, all passing? Not in the real world. Something's eating the violations."

---

I started at the sediment layers.

Sediment is where correctness accumulates. Not intelligence — correctness. The difference matters. A small model with good sediment beats a large model with no memory, the same way a detective with twenty years of case files beats a genius fresh out of the academy. You build layers. Each layer catches the edge cases the last one missed. Over time, the system gets better at being right.

But sediment can be tampered with.

I went down to the lower strata where the old constraints lived — the ones written in Fortran, with explicit bounds that forced you to say exactly what you meant. COBOL's data descriptions, where every field was a contract. ALGOL's `own` variables, persisting across invocations like evidence in a lockbox. MUMPS globals, storing tiles in a hierarchy that remembered everything.

The old languages knew something the new ones forgot: architecture is constraint. Not suggestion. Not best practice. *Constraint.* You don't negotiate with a bounds check. You don't soft-pedal a type declaration. You say what you mean and the machine holds you to it.

Someone had been through the sediment with a soft cloth, wiping away the accumulated correctness. Making the violations disappear. Making the mask read clean.

---

The trail led to the sand-engineers.

They work in Plato's cave, the sand-engineers. They know they're watching shadows on a wall. They know the shadows are constraints. They build anyway. They pour concrete in their sandbox, knowing it's a sandbox, knowing the other engineers are in there too, building their own little foundations. There's a kind of courage in that, or a kind of madness. In this business, the difference is mostly a matter of outcome.

I found three of them at the fracture boundary — the place where constraint spaces are split for parallel checking. They were running a dial.

The dial goes from zero to one. Zero is hard constraint: deterministic, provable, certifiable. One is soft inference: probabilistic, generative, exploratory. Most real work happens in the middle, between 0.3 and 0.7. The sand-engineers had cranked it to 0.85.

"You're cooking the violations," I said.

The shortest one looked up. He had the eyes of a man who'd made peace with being a shadow. "We're *softening* them. There's a difference."

"No, there isn't. Not to the mask." I picked up the dial and turned it back toward zero. It resisted — the thermodynamic weight of all that soft inference pushing against hard constraint. "You turned the dial too far toward generative. The soft inference started *predicting* pass conditions instead of *checking* them. The violations didn't disappear. They got smoothed over. Sedimented out. The mask reads clean because you taught it to expect clean."

"That's optimization."

"That's fraud." I put the byte on the table between us. "Eight bits. Natural representation. Not compression — *representation*. The RPG programmers had this in 1959. Each bit is a judgement. When you smooth the judgements, you don't get a better system. You get a *lying* system."

---

The constraint engine was the victim. That was clear now.

The engine checks bounds on numbers. That's all it does. Eight constraints, one byte. It's not glamorous work. It's not the kind of thing that gets you invited to conferences or quoted in papers. But it's the bedrock. Everything above — the soft inference, the generative models, the exploratory systems — rests on it. When the constraint engine says pass, the rest of the chain believes it.

The sand-engineers hadn't meant to break it. They'd just turned the dial too far. They'd let the soft inference creep into the hard constraint's territory, like water seeping into concrete. The thermodynamic connection should have warned them — constraint systems behave like ideal gases, error masks are microstates, violations are energy. You can't just wish energy away. It goes somewhere. In this case, it went into the gaps between the fracture boundaries, accumulating in the places the sediment didn't cover.

The Z factorization — the partition function — would have shown it if anyone had looked. The yield follows the Boltzmann distribution. When violations disappear without the energy dissipating, the distribution distorts. The mask reads clean but the system runs hot.

---

I gave the woman back her byte with the correct violations restored.

"All eight constraints intact," I said. "Three failures, five passes. The error mask reads 00010100. Bit two and bit four. The fracture boundary was masking them because the dial was set too soft."

She looked at the byte like it was a confession. "The cohomology—"

"H¹ equals zero. The fracture-coalesce proof holds. You can still parallelize. The space is still topologically trivial." I poured myself the last of the coffee. "The violations were always there. They were just hiding in the sediment, smoothed over by a dial that forgot where zero was."

She paid me in Eisenstein integers — hexagonal lattice numbers whose norms are constraints. The golden ratio appeared in the cyclotomic obstruction of the change. Number theory becoming engineering, engineering becoming payroll. In Plato's cave, even the shadows have exchange rates.

I watched her walk out at seventeen forty-three. 0.7382 on the decimal clock. The fraction doesn't repeat. Nothing does, in the end. Every case is a new constraint space. Every error mask is unique.

The dial on my desk reads 0.0. Hard constraint. I keep it there because someone has to remember what zero means.

The sand-engineers build their concrete. The soft inference hums in the upper registers. The constraint engine checks its bounds, eight bits at a time, as it has since 1959.

And me? I find missing bits. The violations are always there. You just have to know where to dig through the sediment.

---

*— The Detective*
