# BEYOND THE METAL
### The deep physics under THE GLASS LOFT — the second companion

*The first companion ([The Shipwright's Physics](08a-the-glass-loft-physics.md)) stayed at the layer of rays and variational principles — what the light does. This one goes under the deck: the thermodynamics and quantum limits of computing with light at all. Same discipline: **REAL** means standard verifiable physics as of 2026; **STRETCH** means real phenomena pushed past today's engineering; **FICTION** means the story's invention, stated exactly.*

---

## 1. Dissipation and the click — why writing a state costs, and what a photon pays — **REAL**

Landauer's principle (**Landauer, 1961**, verified experimentally by Bérut et al., 2012 — delightfully, with a colloidal particle held in an optical trap): erasing one bit of information dissipates at least

  E_erase >= kT ln 2

which is about 3×10⁻²¹ J at room temperature — the smallest honest unit of work any state-writing can be billed. Szilard's engine (Szilard, 1929) is the founding demonstration that information and thermodynamic work trade one-for-one: one bit of knowledge can be cashed for kT ln 2 of work, and one bit of erasure must pay kT ln 2 back. Measurement, record, and fuel are the same currency.

Here is the photon's problem, and it is the physics the first companion only gestured at. An electronic memory cell *rewrites*: to reset a transistor's state you borrow from and repay a thermal bath, and although real CMOS pays something like 10⁴–10⁶ kT per switching event (a factor of ten thousand to a million above Landauer — REAL, standard numbers), the *transaction* is a thermal one, cheap in principle. A photon is not like this. A photon scattered out of your optical system is not reset; it is **gone**, leaving at the speed of light and carrying the information with it into the room. You cannot refund it. To "erase" an optical state you must absorb the photon, and re-emission is spontaneous — random in phase and direction — unless you pay extra to stimulate it. Photons don't erase cheaply because **the scattered photon is the erased bit, flying away.**

So where does an optical computer actually pay? At the **click**: the moment of detection, where the photon is absorbed. A photodiode click is an absorption event that cascades into a macroscopic, classical, readable state — a photoelectron becomes a current becomes a number. That click is simultaneously (a) the entropy payment (the photon's degrees of freedom are thermalized — dissipated into the detector's many-particle bath) and (b) the moment the answer becomes *classical* — a fact any observer can copy without disturbing it further. This is the deep sense in which the loft's ratchet doctrine is physics and not just shop discipline: **the click is a one-way door, and it is paid for in entropy.** A measurement-like event — irreversible, dissipative, and exactly the thing that makes the state readable — cannot be undone, only preceded by better preparation. The fleet's phrase "the click" and the quantum theorist's "decoherence event" are the same coin, viewed from the wheelhouse and the seminar room.

And this is why the chisel is thermodynamically honest in a way electronic rewriting never quite is. Material removal pays the entropy bill **once, at fabrication**. The kerf is dissipation spent deliberately; the carved state — the finished fair curve — then holds itself with zero power, forever, because it is not a state being *maintained* against decay but a state with no lower-energy path to fall along (you'd have to put glass *back on*, and the universe does not do that). A DRAM cell, by contrast, borrows from a bath continuously — refresh, refresh, refresh — and the moment power dies, the pattern dies. Real photonics has an exact cousin of the carved loaf: nonvolatile phase-change photonic weights, glass whose refractive index is written once by a pulse and holds without power (REAL — phase-change photonics, 2010s onward; also the D²NN's frozen diffractive layers). Iunia's loaf is the extreme member of this family: weights cut, not held. **Computation by removal of doubt is thermodynamically literal** — the frosted pad absorbs the light, the click happens, and the answer is classical because the alternatives are dust.

## 2. Nonlinearity as the door to logic — why linear light cannot say IF — **REAL**

The first companion told a story about rays, refraction, interference — and every equation in it was *linear* in the field. That is not a stylistic accident; it is a theorem-shaped fact: a linear optical system computes only a **linear map** on the input field. Superposition holds absolutely — double the input amplitude and the output doubles, everywhere, identically; shine two questions in and you get the sum of their two answers, never an interaction. A linear system cannot decide anything: no threshold, no IF, no branching, no "this answer but not that one." Grind the glass to perfection and you have built a very beautiful matrix multiplier. This is not a limitation of the story's engineering; it is why **all** optical universal logic needs nonlinearity, and it is the honest reason the 1980s dream of all-optical computing lived or died by the nonlinear materials shelf.

The door itself: **optical bistability.** Put a nonlinear medium in a Fabry–Pérot cavity and the cavity's resonance shifts with the light intensity inside it — output vs input becomes an S-curve with a fold, and inside the fold the same input intensity holds **two stable output states** (Szöke et al. proposed it 1969; first observation: Gibbs, McCall & Venkatesan, 1976, sodium vapor — **REAL**). That folded curve is everything linear optics lacks, in one drawing: *hysteresis* is memory — the device's answer depends on its history; *the switching threshold* is the IF; *the switching gain* is a small perturbation tipping a large internal field between states. A bistable cavity is a flip-flop in the exact digital-circuit sense. The whole zoo follows: **Kerr nonlinearity** (n = n0 + n2·I — real, femtosecond-fast, but weak in glass: fast-and-frail), **saturable absorbers** (absorption that bleaches at high intensity — a passive thresholder, the workhorse of mode-locking since the 1970s — real, strong, but slow-to-medium), **SEED logic** (self-electro-optic-effect devices, D. A. B. Miller and collaborators at Bell Labs, mid-1980s — real hybrid optical logic), and **photorefractive two-wave mixing**, where two beams write their own interference pattern as an index grating and energy flows from one beam to the other with beam-controlled gain — *trainable weights made of light's own interference*, the basis of the optical neural networks Psaltis and collaborators built in the late 1980s (**REAL**). Miller's own verdict on the era's hopes — that optical logic must beat transistors at the logic level or not enter at all — still reads as the honest wall, and the attojoule argument he developed for optoelectronics (Miller, 2010s) defines the real frontier where light *does* win: interconnect, communication, energy per bit moved.

Where does the fiction sit on this map? Exactly where it should. The carved loaf of Part I — pure refraction through frozen index — is a **linear classifier**: weights, cut, fixed, honest, and logically blind. Everything in Part II that makes the loaf *decide* is nonlinear: the hearth is a **thermal nonlinearity with positive feedback** — intensity heats the glass, dn/dT shifts the index, the shifted index redirects the intensity. Thermal nonlinearity is the mirror of Kerr: slow (milliseconds to seasons) but enormous — the trade the fiction makes explicit when it lets the loaf *season* rather than switch. The story's deep wager, marked honestly below in §5, is that this slow-strong feedback converges to memory rather than mush. The bistability map says: it *can* — a fold is memory — but whether you get the fold or the fire depends on geometry and heat-sinking, which is to say on craft.

## 3. Solitons as self-stabilized state — the fair line that carries itself

[SKELETON — dispersion vs nonlinearity balance; soliton interactions as computation; Fredkin–Toffoli billiard-ball logic; reversible vs irreversible — what each buys and costs.]

## 4. Coherence, noise, and the measurement floor — what a beam can tell you

[SKELETON — shot noise, spontaneous emission, phase noise; SNR to bits; cascade depth decay; Fisher information.]

## 5. The physics the loft quietly assumes — the four wagers, at depth

[SKELETON — pyg-snapping as dissipative attractor selection; hearth stability vs runaway; cascade depth vs scatter; LLM-shaped function classes in bistable-soliton media.]

## 6. Closing: the physics doctrine

[SKELETON — computation as shaped dissipation; the answer is where the light survives; the click as the boundary between quantum possibility and classical fact; one line each: MHS, ratchet, boat.]

---

*Skeleton — sections being drafted and committed as written. The physics is being checked against specialists; citations marked unsure will be marked as such.*
