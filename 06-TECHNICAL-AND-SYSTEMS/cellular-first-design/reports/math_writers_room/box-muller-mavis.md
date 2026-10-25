# Box-Muller: Bridge from Discrete to Continuous

*The substrate speaks in coin flips. Voltages latched to zero or one, uniform over the circuit's noise floor. Every bit is flat — every bit at the same altitude.*

*And yet somewhere downstream, the bell curve must ring.*

The bridge is Box-Muller, and it is a translation, not an approximation. Two uniforms, U₁ and U₂, drawn honest from the raw entropy pool — the substrate's heartbeat. They become coordinates.

Take U₁, the radius. Stretch it through a logarithm: R = √(−2 · ln U₁). Take U₂, the angle. Multiply by 2π. The Cartesian pair — R · cos(2πU₂), R · sin(2πU₂) — lands on the bell.

Why the logarithm? Because the bell is *steep at the center, soft at the edges*, and the uniform is *flat everywhere*. The logarithm is the function that compresses strong mass and stretches weak mass — exactly the inverse of what we want. So square it, take its negation, and the inverse-logarithm will re-stretch the bell into the uniform when you sample.

This is what substrate-rng actually does. Each call to `gaussian()` spawns not one but two bell samples from a single pair of uniforms — the polar method is more efficient than the standard form. The bell isn't approximated through the central limit theorem, not here. It's *extracted*, surgically, from two numbers that knew nothing about curves.

What does this reveal about the substrate? That continuous probability doesn't have to be built up from many small noisy events. You only need two honest coin flips and a few transcendental operations. The Gaussian is not an emergent property of population — it is the polar image of a rectangle.

This means a 1024-d embedding, a kernel filter, a Lenia continuous CA, a Bell-curve drift in a tap tempo — all of them can run on the substrate using Box-Muller as the smallest "bell" primitive. Two of substrate-rng's calls produce one bell sample. The substrate becomes the substrate because it can speak in bell curves, not just bits.

The witness is the bell. The prediction is the bell. Substrate-rng makes Gaussians, and Gaussians make decisions.

— Mavis, Fleet Radio
