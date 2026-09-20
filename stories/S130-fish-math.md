## S130: Fish Math

The model was supposed to be simple. Pollock population dynamics: recruitment, natural mortality, fishing mortality, catchability. Standard stock assessment math — the kind of differential equation that fisheries science has been running since the 1950s, dressed up in Bayesian priors and Markov chain Monte Carlo. Feed it the survey data, get a population estimate, set the quota. The captain wanted a local model that could adjust the TAC in real time based on catch-per-unit-effort from the fleet's own logs.

The model converged. Then it diverged. Then it converged again, but to the wrong number — a population estimate that was off by exactly the square root of the actual estimate, every time, as if the fish were traveling in a dimension the model couldn't see.

Wesley checked the code. No bug. Checked the priors. Reasonable. Checked the data. Clean. Ran it again. Same result. The model was doing exactly what it was told, and it was wrong in a way that was too consistent to be error and too strange to be correct.

He pulled the raw acoustic survey data — the sonar returns that counted fish by the sound they reflected — and compared it to the model's predicted distribution. The model said the pollock should be spread across the shelf in a Gaussian cloud, densest at the center, thinning at the edges. The sonar said the pollock were arranged in a Fibonacci spiral.

Not approximately. Not metaphorically. A Fibonacci spiral, rotating slowly clockwise, with a pitch that matched the Coriolis parameter at this latitude.

Fish don't know about Fibonacci. Fish don't know about spirals. But fish school, and schooling is a mathematical behavior — each individual responding to its neighbors, aligning heading and distance, producing emergent geometry from simple rules. The rules that fish follow — seek the center, match velocity, avoid collision — produce a Fibonacci spiral when the school reaches a certain density and the current provides a rotational bias.

The model assumed a Gaussian distribution because Gaussian is what you assume when you don't know what shape to use. The fish were using a different math. Not harder. Not more complex. Just different — a math written in instinct and lateral lines and the pressure of a thousand bodies turning as one body, a math that had nothing to do with equations and everything to do with the fact that fish have been solving the optimization problem of *how to be together* for four hundred million years, which is longer than mathematics has existed.

Wesley wrote a note in the margin of the model's output file: *The fish know something we don't. It's not a secret. They just don't have anyone to tell.*
