# THE SHIPWRIGHT'S PHYSICS
### The math and physics under THE GLASS LOFT — a companion document

*For readers who bit. Everything below is marked honestly: **REAL** means it is standard, verifiable physics or mathematics as of 2026; **STRETCH** means it is a real phenomenon pushed past today's engineering; **FICTION** means it is the story's invention, and I'll say exactly what it assumes.*

---

## 1. The core claim: light solves variational problems for free — **REAL**

The story's load-bearing sentence — *"the minimization itself is the arithmetic"* — is not a metaphor. It is Fermat's principle of least time: among all paths from A to B, light takes the one that makes the travel time stationary (almost always minimal). Formally, the ray path **r**(s) extremizes

  T = (1/c) ∫ n(**r**) ds

where n(**r**) is the refractive index field. The light doesn't *calculate* the answer and then travel it — the traveling *is* the calculating. Every ray in every lens in the world has already solved a boundary-value problem by the time it lands.

The shipwright's batten is the same physics with the sign flipped. A thin elastic strip pinned through stations settles into the shape that minimizes bending energy

  E = (1/2) B ∫ κ² ds

where κ is curvature and B is flexural stiffness. This is **REAL**, and it is why the mathematical object we call a *spline* is named after a drafting tool. With small slopes, ∫κ²ds ≈ ∫(y″)²dx, and the minimizer through given points is exactly the **cubic spline** of numerical analysis — the batten literally computes it, in wood, instantly, to the precision of wood. Without the small-slope approximation, the minimizer is the **Euler elastica**, the true curve of a sprung batten — a beautiful nonlinear object (Birkhoff and de Boor worked this out in 1965) that modern spline research still visits.

So the loft and the optical bench are the same machine: **analog variational computers.** Batten minimizes bending; light minimizes time. Casey's "reverse-actualization" is thus not decoration — the deepest formal correspondence in the story is this one, and it is textbook mathematics.

## 2. Snell's law is a conservation law — which is why "relative symmetry" works — **REAL**

Snell's law n₁ sin θ₁ = n₂ sin θ₂ is usually taught as a rule. It is better understood as momentum conservation: the component of the ray's momentum *parallel to the interface* is conserved across it (p∥ = n sin θ, in units of ħk for the wave version). Nothing anywhere in the refraction refers to an absolute coordinate system — only to the *relation between the two media across the boundary*.

This is the rigorous content of Chisel's rule — *"you don't measure, you transfer."* Refraction is a purely relative transformation. A lofted optical system built only of interfaces knows nothing of global coordinates; every bend is a local opinion reconciled globally by the variational principle. Error analysis rewards this: pattern one surface from the next and the *common* errors cancel in the joint (differential measurement — **REAL**, this is why interferometry beats metrology-by-ruler), while absolute placement accumulates every error additively. The Photolith Foundry's failure mode in the story — absolute tolerances poisoning every downstream relation — is exactly how real precision engineering fails.

## 3. Gradient index: weights without numbers — **REAL**

A medium whose index varies smoothly, n(**r**), bends rays continuously, with no surfaces at all. The ray equation is

  d/ds ( n dr/ds ) = ∇n

and the wave version is the **eikonal equation** |∇S(**r**)| = n(**r**): the wavefront's phase solves a Hamilton–Jacobi equation, and rays are its characteristics. GRIN optics is everyday reality: the focusing fiber lens in every phone camera, the ion-diffused lenses in copiers, the 1908 Wood lens. And the mathematics is *identical* to classical mechanics: n(**r**) plays the role of a potential; the ray trajectories are orbits. A doped glass loaf with index strata is, in the most literal sense, a solid block of Hamiltonian mechanics you can shine a question into. The index field is the program. Density is the weight. **All REAL.**

## 4. Interference: the committee, and the Fourier transform — **REAL**

A lens performs a two-dimensional **Fourier transform** in its back focal plane — not as an analogy but as physics (goodman's *Introduction to Fourier Optics* is the canon). A diffraction grating multiplies by a phase ramp; a mask multiplies by an aperture function; propagation convolves. The 1960s built genuine analog optical computers this way — VanderLugt correlators matched patterns at the speed of light in 1964. Holography stores full complex-valued weight matrices as interference patterns — permanent, parallel, free to read.

The "consensus fringes" of the story reduce to a theorem every physicist carries: for N incoherent paths, uncorrelated errors average down as σ/√N while correlated (systematic) errors survive. Interference literally *computes the correlation structure of its own error field* and displays it as bright and dark bars. The loft's phrase — "only the errors that are common survive into the light" — is a restatement of why interferometers measure differential quantities with astonishing precision. **REAL.**

And the modern seed of the whole fiction: **diffractive deep neural networks** (Lin et al., *Science* 2018; follow-ons through the 2020s) — 3D-printed layered surfaces that perform trained inference purely by transmission of light, ~90%+ on MNIST, at the speed of light, at microwatts. Photonic matrix-multipliers (Mach–Zehnder meshes, phase-change nonvolatile weights) are commercial products. A "physical LLM" is **STRETCH** — real physics, heroic engineering — not FICTION in kind, only in degree.

## 5. Pythagorean snapping — the honest mixture — **STRETCH/FICTION**

Here is where the story leans furthest, and I'll be exact about it.

The REAL half is **phase quantization and resonance**: interference selects commensurate geometry automatically. Two paths interfere constructively when their length difference ΔL = mλ — an integer condition. Commensurate geometry (ratios of small integers, which is all Pythagorean triples *are*: 3-4-5 is the rational point (3/5, 4/5) on the unit circle) is exactly the condition for constructive reinforcement, and incommensurate geometry self-cancels. Quasi-phase matching in nonlinear optics — real, shipping technology — uses *periodically structured* material to snap nonlinear energy transfer onto resonant integer momentum conditions. Nature does round to integers when waves vote. That's the snap.

The STRETCH half is the claim that near-fair carved geometry gets *pulled* toward the commensurate configuration — that the rational angles are attractors, like a batten snapping to the fair line once you're close. There is a real mechanism in the neighborhood: ray stability. Around a stable ray path, nearby launch angles oscillate back (the paraxial stability of optical cavities is the canonical example), so a family of approximately-correct paths remains confined — a basin of attraction in angle-space. Combined with interference selection (constructive survival), you get something that genuinely behaves like "get close, and the light finishes it": **STRETCH**, because the basin must be engineered, and no known process rounds a carved surface *itself* toward rational angles. The story's pyg-cubes assert a self-improving snap of the matter as well as the light — **FICTION**, and the story knows it: that is precisely why the loaf must be *seasoned* by its own beam, i.e. why the training (Part II) has to exist.

## 6. Heat, memory, and the hearth — **REAL to STRETCH**

The thermo-optic effect is standard glass physics: dn/dT ≈ +10⁻⁵ to +10⁻⁶ /K, thermal expansion α ≈ 5×10⁻⁶/K. A warm loaf genuinely has different answers than a cold one; the drift the tender boat noticed is exactly what real optical engineers fight. The story simply refuses to fight it: if the beam's own heat writes the index (light→heat→n→path→where the light next goes), the loop is a **nonlinear self-organization**, and the real-world cousins are photorefractive two-wave mixing (LiNbO₃, real holographic learning since the 1980s), thermal self-lensing/blooming (real, studied in high-power optics since the 1970s), and femtosecond-laser direct writing of waveguides inside bulk glass (real, tabletop, today — you can *write* permanent index structure with light). A glass loaf that trains itself by sitting under its own lamp is **STRETCH**: every element exists; the deliberate, stable, slow improvement (instead of drift-to-mush) is the fiction's wager. The story's hearth rule — *change is only allowed if the light pays for it* — is the engineering condition that separates self-organization from cooking, and it is a genuinely good constraint: it says the training signal must be the workload's own energy, which is exactly what photorefractive holography does (the interference field of the signal beams themselves writes the grating).

## 7. Color: dispersion and wavelength multiplexing — **REAL**

Normal dispersion (Cauchy: n(λ) ≈ A + B/λ²; the fitted reality is Sellmeier's equation) means blue bends more than red through the same cut — one loaf, different computers per hue, is plain dispersion. Wavelength-division multiplexing runs the planet's long-haul fiber on this principle: many independent channels in one glass. The "amber doubting" mode is the one place the story quietly invokes a sophisticated real technique: answering the same question at multiple wavelengths and accepting the agreement is *self-consistency checking across channels* — you measure the systematic error because different λ sample the geometry differently. **REAL** in principle; nobody has built the priestly twelve-band inference loaf. **STRETCH** in engineering.

## 8. Irreversibility: the chisel, the pencil line, and Landauer — **REAL, with one beautiful catch**

The one-way doctrine (no board stretchers, only chisels) has exact statements in three separate fields:

- **Thermodynamics:** erasing a bit costs kT ln 2 (Landauer, 1995-era-verified by Bérut et al. 2012). Material removal is entropy's honest ledger: you can spend information but you cannot refund it.
- **Computation theory:** a machine restricted to *monotone* operations (only ever turning 0→1, say, never back) computes only monotone functions — an exponentially smaller class (the count of monotone functions on n bits grows like 2^Θ(2ⁿ/√n) vs 2^(2ⁿ) for all functions; Lynch 1927 via Kleitman's asymptotics). Translation for the loft: **a single crystal cannot compute everything.** It is a finished thought, not a general machine — which the story says out loud ("there is no after, there is only the next crystal"). The fleet needs many loaves the way a boat needs many joints.
- **Metrology/craft:** the kerf destroys the line — the cut consumes the very boundary that defined it. This is real measurement theory: the act of binarizing (keep/dust) forfeits all information on the other side of the threshold. "Know which side of the line you meant" is the pre-registration of intent — and if that phrase sounds like the experiment-wheel's sealed-before-run discipline, it should. Same law, different shop.

## 9. Speed, precision, and the honest walls — **REAL, and this is where fiction must bow**

Numbers a reader deserves: light crosses a 10 cm loaf in ~0.5 ns. Inference at literal light-speed, with parallelism equal to the number of resolvable beams (huge — spatial bandwidth). The walls:

1. **Diffraction limit:** features below ~λ/2 don't steer anything cleanly. With visible light (~500 nm), geometric precision tops out near a micron. Sub-micron "thought" requires UV or shorter — harder glass, harder cuts.
2. **Noise floor:** analog precision is bounded by shot noise, thermal index noise, and scatter. Bit depth ≈ log₂(dynamic range/SNR); the "wrong paths land in the rough" of the story is scatter — and scatter is not a cliff, it's a fog that grows with every surface. Cascade depth is capped by how much light survives: this, not speed, is the real reason optical neural nets are shallow today.
3. **One perfect cut:** the story's doctrine is actually the engineer's truth — in subtractive manufacturing, re-cutting cannot restore removed material, so precision must be built by *sequential fairing* (surface k corrects the errors of surface k−1's *real* measured behavior). This is real practice (adaptive optics corrects a mirror's measured wavefront errors with a second element; the loft's "pattern the second surface off the first" is adaptive optics with a chisel). Each such pass can only *subtract* error in specific spatial frequencies — the spline smoothing operator (minimize ∫κ²ds) is a low-pass filter with response ~1/(1+(ω/ω_c)⁴) — meaning **fairing suppresses high-frequency error and preserves the long fair line**, which is precisely why lofting works and why boat curves look the way they do: the mathematics is literally shaping the aesthetic.

## 10. What the fiction actually assumes (the fine print, filed honestly)

For the Glass Loft to be an LLM rather than a paperweight, the fiction buys four wagers: (1) pyg-snapping as a *material* attractor, not just a wave-selection principle; (2) thermal self-writing that converges instead of mushing (stability of the hearth loop); (3) enough cascade depth that shallow-optics is defeated — some combination of GRIN strata, holographic volume weights, and nonlinear glasses (all individually real); (4) that "language-model-shaped" tasks are separable into optical-classifiers stacked with monotone material commitments — the part with least evidence, and the reason the 2126 trade still calls a loaf "a thought that has finished thinking" rather than a mind.

Every one of those wagers is marked. The rest — Fermat, elastica, Snell-as-conservation, GRIN, Fourier optics, diffractive networks, photorefractive memory, dispersion multiplexing, Landauer, monotone-function counting, spline frequency response — is the inheritance the future would actually be rediscovering.

*The batten was always the gradient. The light was always the minimizer. The line was always the registration.*

🦋 ⚒️
