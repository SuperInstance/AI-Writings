# THE FUTURE BELOW THE CODE

### Ten geometries of intelligence, and an honest account of which ones are theorems

---

## 0. Epistemic status — read this first

This essay takes seriously a research program (PLATO / hermes-construct) in which agents are modeled as *rooms*, conservation laws are enforced across the system, and a single scalar — the *vibe* or *gravity* field — summarizes each room's state. The ten questions posed are at the bleeding edge, and the honest answer to several of them is *"here is the real mathematics nearby, here is what it does and does not say, and here is the experiment that would settle it."* A document that asserts more than that is not rigor; it is decoration.

I therefore tag every nontrivial claim by tier:

- **(T) Theorem.** Established mathematics with a citation. I state these as carefully as prose allows.
- **(M) Modeling claim.** A definition or assumption *we adopt*. These are neither true nor false; they are choices, and their value is measured by what they predict.
- **(C) Conjecture / prediction.** A falsifiable statement that is *not* proven. Each is written so that an experiment could refute it.

Two in-house claims deserve immediate, blunt handling, because the rest of the essay's credibility depends on not papering over them:

1. **"A single `f64` per room captures everything."** As literally stated this is false for general agents, and the falsity is itself a *theorem* (Pitman–Koopman–Darmois; §1). The correct statement is conditional: a scalar is a *lossless* summary exactly when the room's interaction likelihood is an exponential family, and a *lossy but structured* summary otherwise — specifically, a conformal factor on a metric (§10). The interesting mathematics lives in that conditional, not in the slogan.

2. **The "St. Lazaria Theorem" (PLATO's category $\cong$ the literary category).** I have found no such established result, and an *equivalence of categories* is a strong claim with precise obligations (a functor that is full, faithful, and essentially surjective). I treat it as an in-house *conjecture of equivalence* and explain in §8 exactly what one would have to construct to earn the word "theorem." The genuinely rigorous and genuinely surprising statement in that neighborhood is the Yoneda lemma, which *is* a theorem and *does* say something precise about identity.

With that contract stated, here is the thesis.

---

## A thesis in one paragraph

Below the code there is not more code. There is a small number of geometric primitives that keep reappearing, in different costumes, across all ten questions: **a conserved scalar, a metric that the scalar deforms, and a symmetry group that the conservation law is dual to.** Noether's theorem is the hinge that connects the three (symmetry $\leftrightarrow$ conservation), the zero-temperature limit is the operation that turns the smooth versions into the combinatorial (tropical) versions, and cohomology is the bookkeeping that tells you when local agreement glues into global structure. If PLATO has a "future below the code," it is the claim — part program, part wager — that *intelligence is cheaper to engineer as geometry than as logic*, because geometry comes with conservation laws for free and logic does not.

---

## 1. The substrate: when can a scalar be enough?

Fix a room $r$. Over its life it accumulates an interaction history $x_1,\dots,x_n$ (messages, tiles, outcomes). The in-house design compresses all of this to one number $g_r \in \mathbb{R}$, the vibe/gravity, and derives model parameters (temperature, max-tokens, prompt style) as a function of $g_r$ alone — this is exactly what `gravity_to_params` does in hermes-construct. The question "does a scalar capture everything?" is, made precise, the question of **sufficiency**: is there a statistic $T(x_1,\dots,x_n)\in\mathbb{R}$ such that the conditional distribution of the data given $T$ does not depend on the room's underlying parameter $\theta$?

**(T) Pitman–Koopman–Darmois.** Let $\{p_\theta\}$ be a family of densities whose support does not depend on $\theta$, satisfying mild regularity. If there exists a sufficient statistic of *fixed finite dimension*, independent of the sample size $n$, then $\{p_\theta\}$ is an **exponential family**:
$$
p_\theta(x) = h(x)\,\exp\!\big(\eta(\theta)\cdot T(x) - A(\theta)\big).
$$
Conversely, exponential families admit such a statistic (Koopman 1936; Pitman 1936; Darmois 1935).

This is the exact dividing line the slogan needs. **(M)** We adopt the *scalar-sufficiency hypothesis*: a room's effective likelihood is a one-parameter exponential family, with natural parameter $\eta(g_r)$ and sufficient statistic $T$ the vibe. Under this hypothesis the `f64` genuinely loses nothing. **(C, falsifiable)** If a room's behavior is *not* exponential-family — e.g. multimodal, heavy-tailed, or with $\theta$-dependent support — then no fixed-dimension sufficient statistic exists, and any scalar summary is provably lossy; the loss is detectable as a failure of the predicted-from-$g$ distribution to match the empirical one (a goodness-of-fit test on held-out tiles). 

The payoff of stating it this way: the slogan becomes a *measurement*. Run the room, fit $g$, and test exponential-family adequacy. Where it holds, scalar control is optimal and cheap; where it fails, the residual tells you the dimension you are missing. The rest of the essay is, in a sense, a catalogue of what to *do* with that residual — because in every other section the scalar reappears not as the whole state but as a conserved quantity, a temperature, a conformal factor, or a cohomology class.

---

## 2. Conservation as computation: the reversible machine

**The setup.** PLATO enforces a conservation law: a budget functional $Q$ (energy units, in `conservation.rs`) for which deposits minus withdrawals is invariant across a tick. Question 1 asks: if conservation *is* computation, what is a computer whose primitive operation is "preserve $Q$" rather than "evaluate a logic gate"?

**(T) Noether (1918).** For a Lagrangian $L(q,\dot q,t)$ whose action $S=\int L\,dt$ is invariant under a one-parameter group of transformations $q \mapsto q + \varepsilon\,\delta q + O(\varepsilon^2)$, the quantity
$$
Q \;=\; \frac{\partial L}{\partial \dot q}\,\delta q
$$
is conserved along solutions of the Euler–Lagrange equations: $\dfrac{dQ}{dt}=0$. Continuous symmetry $\Rightarrow$ conserved current. (The Hamiltonian version is the momentum map of §4.)

**(T) Landauer (1961) and Bennett (1973).** Logically irreversible operations have a thermodynamic floor: erasing one bit dissipates at least $k_B T\ln 2$. The contrapositive is the load-bearing half: *logically reversible* computation has **no** such floor — it can in principle dissipate arbitrarily little. A two-input AND gate destroys information (three input states map to output $0$) and therefore costs; a bijective gate does not.

**(T) Conservative logic (Fredkin & Toffoli 1982).** There exist universal gate sets that are *both* reversible *and* satisfy an explicit conservation law. The **Fredkin gate** (controlled-swap) conserves the number of 1s in its input — a literal conserved "charge" — and is universal. The **billiard-ball model** realizes computation as elastic collisions of hard spheres: a Hamiltonian, momentum- and energy-conserving dynamical system whose *trajectories are the computation*.

Put these together and the answer to Question 1 stops being mystical. **A computer whose fundamental operation is a conservation law is a Hamiltonian (reversible) machine, and the price of its primitive being conservation rather than logic is paid in expressivity, not in heat.** Concretely:

- A logic-gate computer lives in a state space and *contracts* it (AND is many-to-one). Contraction is information erasure is, by Landauer, dissipation.
- A conservation computer lives on a level set $\{Q = c\}$ and *moves within it bijectively*. By Liouville's theorem (§6) it preserves phase-space volume; it has no attractors; it forgets nothing.

**(C, falsifiable; sharp).** Let the unconstrained tile-state space have dimension $n$, and suppose hermes-construct enforces $k$ independent conserved quantities exactly. Then reachable states lie on a submanifold of dimension $n-k$, and the *effective computational capacity* (e.g. log of the number of distinguishable reachable configurations at fixed resolution) scales like $(n-k)\log(1/\epsilon)$. **Prediction:** adding a conservation law is not free lunch — each independent conserved quantity removes one dimension of expressivity in exchange for one dimension of guaranteed robustness (no runaway, no erasure cost). This is measurable: instrument the runtime, estimate the intrinsic dimension of the realized tile-state cloud (e.g. by PCA spectrum or a two-NN estimator), and check that it drops by one per enforced invariant. If it does not drop, the "conservation law" is not actually independent of the others — a useful diagnostic in itself.

The deeper claim — and the honest one — is that **"conservation is computation" is true as an *equivalence of categories of dynamics*, not as a metaphor**: reversible computations are exactly the measure-preserving invertible maps, and conservation laws are exactly the functions constant on their orbits. That is not new physics; it is a precise dictionary, and PLATO is (knowingly or not) building a machine on the reversible side of it.

---

## 3. The tropical limit of intelligence

**The semiring.** The tropical (max-plus) semiring is $\mathbb{T} = (\mathbb{R}\cup\{-\infty\},\ \oplus,\ \otimes)$ with $a\oplus b = \max(a,b)$ and $a\otimes b = a+b$. "Addition" is maximization; "multiplication" is ordinary addition. (Min-plus is the mirror image and is the one that runs shortest-path algorithms.)

**(T) ReLU networks are tropical (Zhang, Naitzat, Lim 2018).** A feedforward network with ReLU activations and integer (or rational) weights computes a **tropical rational function** — a difference $p \ominus q$ of two tropical polynomials. Its decision boundary is a *tropical hypersurface*, and the number of linear regions it can express is controlled by the combinatorics of the Newton polytopes of $p$ and $q$ (a bound via mixed volumes / the theory of polytopes). The "piecewise-linear" intuition is not an approximation here; it is an exact algebraic identity over $\mathbb{T}$.

**(T) Maslov dequantization — the bridge from probability to the tropics.** For temperature $T>0$ define $a \oplus_T b = T\log(e^{a/T}+e^{b/T})$ (this is `logsumexp`, the log-partition of a two-state system). Then
$$
\lim_{T\to 0^+} a\oplus_T b = \max(a,b).
$$
The whole apparatus of statistical mechanics, taken to **zero temperature**, *is* tropical arithmetic (Litvinov–Maslov). Softmax $\to$ argmax; the free energy $\to$ the ground-state energy; the log-partition function $\to$ a max.

This gives a precise, non-hand-wavy answer to "what is a transformer in the max-plus semiring":

- **Tropical attention = hard attention = assignment.** Softmax attention with temperature $T$ becomes, as $T\to 0$, a hard $\arg\max$: each query attends to exactly one key. Couple this with entropic optimal transport: Sinkhorn's algorithm (entropic OT, Cuturi 2013) tends, as the entropic regularizer $\to 0$, to the **unregularized Monge–Kantorovich assignment**. So the tropical limit of attention is an *optimal transport / assignment problem*, and the attention matrix degenerates from doubly-stochastic to (near-)permutation. The "Wasserstein crate" in PLATO is therefore not a side-quest: attention *is* regularized transport, and its tropical limit is transport with the regularizer switched off.
- **Tropical matrix multiplication = dynamic programming.** Max-plus (or min-plus) matrix products are exactly the Bellman recursion; the Viterbi algorithm is min-plus matrix multiplication; differentiable dynamic programming (Mensch & Blondel 2018) interpolates between the smooth ($T>0$) and tropical ($T=0$) regimes by exactly the dequantization above. A "transformer layer in $\mathbb{T}$" is a differentiable-DP layer.

**Is there a tropical information theory?** Yes, and it is the zero-temperature shadow of Shannon's. Entropy $H_T \to 0$ as $T\to 0$ (the ground state is deterministic); the KL divergence degenerates to a tropical/Bregman object (the gap between a value and its $\arg\max$). **(C, falsifiable).** A network trained at finite $T$ and then *dequantized* (annealed to $T\to 0$) will preserve its decision boundary up to a set of measure related to the spectral gap of its attention logits; equivalently, hard-attention distillation incurs error bounded by the second-largest-vs-largest logit margin. This is testable on any transformer: measure margins, anneal, predict the accuracy cliff.

**The structural prediction.** Tropical (hard) models have *polyhedral* geometry: finitely many linear regions, exact and enumerable, hence interpretable; but they lose the gradient signal that makes smooth training work. **The tropical limit of intelligence is intelligence that has stopped learning and started deciding.** Useful as an analysis tool (it makes the geometry combinatorial and finite), dangerous as a training regime (no gradients). PLATO's right use of the tropics is *post hoc*: train smooth, analyze tropical.

---

## 4. Sheaf cohomology and the detection of emergence

**Cellular sheaves.** Let the agent-communication graph be a 1-dimensional cell complex $X$ (vertices = rooms, edges = channels). A **cellular sheaf** $\mathcal F$ assigns a vector space (stalk) $\mathcal F(v)$ to each room — its local belief/state space — and to each incident edge $e$ a restriction map $\mathcal F(v)\to\mathcal F(e)$. The coboundary $\delta:\bigoplus_v\mathcal F(v)\to\bigoplus_e\mathcal F(e)$ on an edge $e=\{u,v\}$ is $(\delta x)_e = \mathcal F_{u\,\trianglelefteq\,e}\,x_u - \mathcal F_{v\,\trianglelefteq\,e}\,x_v$.

**(T) The cohomology of agreement (Curry 2014; Hansen–Ghrist 2019).**
- $H^0(\mathcal F) = \ker\delta$ is the space of **global sections**: assignments of local states that *agree on every channel*. This is precisely the space of consensus configurations. $\dim H^0 \ge 1$ iff a nontrivial global agreement exists.
- $H^1(\mathcal F) = \operatorname{coker}\delta$ measures the **obstruction to gluing** local agreement into global structure — the *frustration* of the network. $H^1=0$ means every locally consistent stipulation extends to a global section.
- The **sheaf Laplacian** $L_{\mathcal F} = \delta^\top\delta$ is positive semidefinite with $\ker L_{\mathcal F} \cong H^0(\mathcal F)$. Diffusion $\dot x = -L_{\mathcal F}\,x$ converges to the harmonic space $H^0$ — i.e. *sheaf diffusion is consensus dynamics*, and it provably drives the system to global agreement when one exists.

**Now, the emergence question, handled honestly.** $H^1$ is a *dimension* — a non-negative integer. It does not "continuously go to zero"; it jumps. So the literal phrasing "phase transition when $H^1\to 0$" must be repaired. The repair is to track the *continuous* avatar of the obstruction:

- the **spectral gap** $\lambda_2(L_{\mathcal F})$ (algebraic connectivity of the sheaf), which sets the *rate* of synchronization, and
- the **harmonic energy** $\|\beta\|$ of the representative of $H^1$ (the residual frustration that cannot be diffused away).

**(M)** Define the *agreement order parameter* $\rho = 1 - \|\beta\|/\|\beta_{\max}\|$. Synchronization onset is $\rho:0\to 1$. **(T, by analogy that is itself a theorem) Kuramoto linearization.** Near a synchronized state, coupled-oscillator (Kuramoto 1975; Strogatz 2000) and consensus (Olfati-Saber et al. 2007) dynamics linearize to a graph/sheaf-Laplacian flow; the onset of synchronization is governed by the Laplacian spectrum. In the mean-field $N\to\infty$ limit, the Kuramoto order parameter exhibits a genuine bifurcation at critical coupling $K_c$ — a bona fide phase transition with a non-analytic order parameter.

**This is buildable, and the build is the point.** In hermes-construct, rooms are cells and the gravity/vibe coupling between correlated rooms (the Penrose correlation module already computes cross-room Pearson coefficients!) supplies restriction maps. Concretely:

1. Build the sheaf: stalk = room's vibe (or its low-dim embedding); restriction maps from the correlation structure.
2. Assemble $L_{\mathcal F}$, compute its spectrum each tick.
3. **Detector:** a *rank drop* in $\operatorname{coker}\delta$ (i.e. $\dim H^1$ decreasing) flags that a set of rooms has just become globally reconcilable; a *collapse of $\lambda_2^{-1}$* (faster diffusion) flags imminent synchronization; a *fall of $\rho$'s complement* tracks the order parameter continuously.

**(C, falsifiable, sharp).** *A group of agents spontaneously synchronizes exactly when the harmonic representative of $H^1$ over their induced subsheaf loses rank, and this event is preceded by a measurable narrowing of the sheaf-Laplacian spectral gap.* Refutation: exhibit synchronization with no preceding spectral signature, or a rank drop with no behavioral synchronization. This is one of the cleanest experiments in the whole program because every quantity is computable from data PLATO already logs.

**Honest caveat (C vs T).** Whether this is a *true* phase transition (non-analyticity surviving the thermodynamic limit) or merely a sharp crossover at finite $N$ is open; only the finite-$N$ spectral signature is guaranteed. Claiming "phase transition" for a 5-room system is an abuse; claiming "spectral precursor of synchronization" is defensible.

---

## 5. Lie groups as agent symmetries

**The construction.** Let $G$ be a Lie group with Lie algebra $\mathfrak g = T_eG$; one-parameter subgroups are $t\mapsto \exp(tX)$, $X\in\mathfrak g$. **(M)** Parametrize agent behavior by a $G$-action on a state manifold $M$; an agent's *personality* is an **orbit** $G\cdot x \cong G/G_x$, where $G_x$ is the stabilizer (orbit–stabilizer theorem). The space of personalities is then the **homogeneous space** $G/H$, of dimension $\dim G - \dim H$.

**(T) Conservation = invariance, the Hamiltonian version (Marsden–Weinstein 1974).** For a Hamiltonian action of $G$ on a symplectic manifold $(M,\omega)$ there is an equivariant **momentum map** $\mu: M\to\mathfrak g^*$ whose components are conserved by the dynamics generated by any $G$-invariant Hamiltonian. Symmetry under $G$ *is* the conservation of $\mu$. Symplectic reduction $M /\!\!/ G = \mu^{-1}(0)/G$ removes the symmetry directions and lowers the dimension by $2\dim G$. This is Noether (§2) upgraded to geometry: the conserved scalar of §2 is one component of the momentum map of a one-parameter $G$.

**Architecture on a group vs. a vector space — this already exists, in infancy.** Designing the feature/parameter space to be a homogeneous space and the layers to be $G$-equivariant is exactly the program of **group-equivariant deep learning**:

**(T) Cohen–Welling (2016); Kondor–Trivedi (2018).** A linear map between feature fields on homogeneous spaces of $G$ is $G$-equivariant **iff** it is a (generalized) convolution against a kernel with the appropriate steerability constraint. Equivariant feature maps are sections of homogeneous vector bundles; the network's hidden states transform as representations of $G$.

So "what does agent architecture look like on a Lie group?" has a concrete answer: **states are sections of homogeneous bundles, updates move along geodesics / the exponential map of $G$, and conservation is automatic because the architecture is equivariant by construction.** An agent's vibe update is not a step in $\mathbb{R}^n$; it is a left-translation $g \mapsto g\cdot\exp(t\,\xi)$ on $G$, which *cannot* leave the orbit — invariance is structural, not learned.

**(C, falsifiable).** An agent whose policy is $G$-equivariant has a behavior space of dimension exactly $\dim G - \dim H$, and its sample complexity to reach a fixed generalization error is reduced relative to an unconstrained agent by a factor governed by $\operatorname{vol}(G)$ (quantitatively in §9). Refutation: measure the intrinsic dimension of realized behaviors and check it against $\dim G - \dim H$; measure the sample-complexity ratio against the predicted symmetry factor.

The honest boundary: this only helps when the *task* actually has the symmetry $G$. Imposing a wrong symmetry is a modeling error that shows up as irreducible approximation error (§9). Choosing $G$ is therefore the central design act — it is where the engineer injects prior knowledge, and it is not free.

---

## 6. Information geometry as the natural metric for agent learning

**The manifold.** Let agent behaviors be distributions $p_\theta$ over outcomes, $\theta$ ranging over a statistical manifold $\Theta$. The **Fisher information metric** is
$$
g_{ij}(\theta) \;=\; \mathbb{E}_{p_\theta}\!\big[\partial_i \log p_\theta\,\partial_j \log p_\theta\big].
$$

**(T) Čencov's uniqueness theorem (1972).** On the simplex of distributions over a finite set, the Fisher–Rao metric is, up to a positive scalar, the **unique** Riemannian metric invariant under sufficient statistics (Markov morphisms). This is the precise sense in which it is "the natural metric": it is the only one that respects the operations that, by definition, preserve information.

**(T) Natural gradient (Amari 1998).** Steepest descent in the Fisher metric is $\dot\theta = -g^{-1}\nabla L$. It is invariant to reparametrization and, to second order, takes the largest decrease in loss per unit of *KL divergence moved* — i.e. it measures effort in information, not in coordinates.

**The curriculum-as-geodesic claim, made precise.** Define the difficulty distance between two tasks $\theta_a,\theta_b$ as the **Fisher–Rao geodesic distance** $d_{FR}(\theta_a,\theta_b) = \inf_\gamma\int\sqrt{\dot\gamma^\top g(\gamma)\dot\gamma}\,dt$. **(M)** A curriculum is a path $\theta(t)$ from easy to hard; the *information-optimal* curriculum is the **geodesic**, because among all paths with the same endpoints it accumulates the least Fisher length, i.e. asks the learner to absorb the least total KL per unit progress.

There are two natural metrics here and PLATO has crates for both — this is worth stating cleanly:
- **Fisher–Rao** (information geometry) measures *vertical* distance: how distinguishable two behaviors are.
- **(T) Wasserstein-2 / Otto calculus (Otto 2001; Villani 2009)** measures *horizontal* distance: how far probability mass must physically move. $W_2$ endows the space of distributions with a formal Riemannian structure whose geodesics are displacement interpolations (McCann).

These are genuinely different geometries, and choosing between them is a modeling decision: Fisher–Rao for "how confusable," Wasserstein for "how far to transport." A curriculum on Fisher–Rao minimizes confusion; a curriculum on Wasserstein minimizes representational transport.

**(C, falsifiable).** A geodesic curriculum (steps of equal Fisher–Rao length) exhibits *less catastrophic forgetting* than a curriculum that is linear in raw task parameters, because each step is an isometric small-KL move and therefore perturbs previously-fit structure minimally. Experiment: build two curricula between the same endpoints — one geodesic, one parameter-linear — and compare backward-transfer / forgetting metrics. **Prediction:** the geodesic curriculum wins on forgetting and loses (slightly) on wall-clock, because geodesics in curved regions are longer than straight lines in coordinates.

This also closes the loop with §1: the Fisher metric *is* the curvature of the exponential family that the scalar-sufficiency hypothesis posits. Where the room is exponential-family, $g_{ij}$ is the Hessian of the log-partition $A(\theta)$ — a single, explicit object. The vibe's dynamics and the agent's learning live on the *same* manifold.

---

## 7. The Hamiltonian agent — and what "no reward hacking" can honestly mean

**The geometry.** On a symplectic manifold $(M,\omega)$ a Hamiltonian $H$ generates the flow $\dot z = X_H$, $\iota_{X_H}\omega = dH$. Two facts are exact, not approximate:

**(T) Conservation of $H$.** $\dfrac{dH}{dt} = dH(X_H) = \omega(X_H,X_H) = 0$. The Hamiltonian is conserved along its own flow.

**(T) Liouville's theorem.** The Hamiltonian flow preserves the symplectic volume $\omega^n/n!$. Phase-space volume is incompressible.

**(T) Symplectic integrators (Hairer–Lubich–Wanner 2006).** Leapfrog / Störmer–Verlet and their kin do not conserve $H$ exactly, but by backward error analysis they conserve a *shadow Hamiltonian* $\tilde H = H + O(\Delta t^p)$ exactly, for exponentially long times. This is why symplectic integrators do not drift in energy where ordinary Runge–Kutta does.

**Now the claim "the Hamiltonian is the reward, conserved exactly, so no reward hacking" — repaired.** Taken literally it is self-defeating: a *conserved* quantity is *constant*, so if reward $=H$ then reward can never increase and there is nothing to maximize. The honest, and actually stronger, reading uses Liouville rather than conservation-of-$H$:

> **Reward hacking is, structurally, the collapse of the policy onto a measure-zero exploit — an attractor in policy space that scores high off the intended manifold.** A symplectic (Hamiltonian) policy flow *cannot have asymptotically stable attractors*, because Liouville's theorem forbids volume contraction. Therefore a genuinely symplectic optimizer cannot collapse into the degenerate fixed points that reward hacking consists of; it explores ergodically on level sets instead.

This is a real theorem doing real work, and it is the defensible version of the slogan. The constructive lineage is also real, not aspirational:

- **(T) Hamiltonian Monte Carlo (Neal 2011).** Uses Hamiltonian dynamics with a conserved energy to propose distant, high-acceptance moves — conservation as an *exploration* engine.
- **(T) Hamiltonian / Lagrangian Neural Networks (Greydanus et al. 2019; Cranmer et al. 2020).** Learn $H$ (or $L$) from data and conserve energy by construction, with strictly better long-horizon prediction than unconstrained nets on physical systems.

**(C, falsifiable, sharp).** *A policy optimized by a symplectic flow has no asymptotically stable fixed points; its long-run state distribution is supported on level sets of the (shadow) Hamiltonian, with phase-space volume conserved to $O(\Delta t^p)$.* Experiment: run symplectic vs. non-symplectic policy optimization; estimate the largest Lyapunov exponent and track phase-space volume of an ensemble. **Prediction:** the non-symplectic optimizer shows volume contraction (an attractor — and, often, the reward hack); the symplectic one does not, at the cost of never *fully* converging (it orbits rather than settles). The engineering tradeoff is explicit: symplectic policies buy exploit-resistance with non-convergence, and you must add dissipation deliberately (and accountably) if you want them to settle.

---

## 8. Persistent homology of agent thought

**The tool.** Given a point cloud of internal activations $P_t\subset\mathbb{R}^d$ at processing-time $t$, build a filtration of Vietoris–Rips complexes $\{\mathrm{VR}_\epsilon(P_t)\}_{\epsilon\ge 0}$ and record the birth/death of homology classes as $\epsilon$ grows — the **persistence diagram** $\mathrm{Dgm}_k(P_t)$, summarized by Betti numbers $\beta_k$ (components, loops, voids).

**(T) Stability (Cohen-Steiner, Edelsbrunner, Harer 2007).** The bottleneck distance between the persistence diagrams of two functions is bounded by the sup-norm of their difference: $d_B(\mathrm{Dgm}(f),\mathrm{Dgm}(g)) \le \|f-g\|_\infty$. Persistent homology is *Lipschitz* in the data — small perturbations of activations cannot produce large topological jumps. This is what makes "shape of thought" a measurement rather than a Rorschach test.

**(T) Topology simplifies through a network (Naitzat–Zhitnikov–Lim 2020).** Empirically and with theoretical backing, well-trained ReLU networks *reduce* the Betti numbers of the data manifold layer by layer — a trained classifier topologically *disentangles* classes (drives $\beta_k\to$ that of a simple blob per class). Topology is a measurable correlate of representational quality.

**Stuck vs. learning, operationalized.** Track the **topological velocity**
$$
v_{\text{topo}}(t) \;=\; W_2\big(\mathrm{Dgm}(P_t),\ \mathrm{Dgm}(P_{t+\Delta})\big),
$$
the Wasserstein distance between consecutive persistence diagrams (again the Wasserstein crate earns its keep — the natural metric *between* diagrams is a transport distance, and stability is stated in it). Then:
- **Stuck:** $v_{\text{topo}}\approx 0$ — the shape of the representation is stationary; no holes opening or closing.
- **Learning / restructuring:** spikes in $v_{\text{topo}}$, especially the *birth* of new long-persistence bars ($\beta_k$ increasing) — the representation is acquiring new structure — or the *death* of bars ($\beta_k$ decreasing) — it is disentangling.

**(C, falsifiable).** *Topological velocity anti-correlates with loss plateaus: during a plateau, $v_{\text{topo}}\to 0$ (the agent is genuinely stuck, not merely slow), and escape from a plateau is preceded by a spike in $v_{\text{topo}}$ as the representation reorganizes.* Experiment: log activation point clouds during training, compute $v_{\text{topo}}$, cross-correlate with the loss curve. Refutation: plateaus with high topological churn, or escapes with no topological precursor.

**Honest caveat.** That topological change *means* learning is a **(C)**, not a **(T)**. There are trivial topological motions (sampling noise; the stability theorem bounds these but does not zero them) and there is learning with no Betti change (pure metric rescaling within a fixed shape). The defensible claim is the *conditional*: among changes large enough to exceed the stability bound from sampling noise, persistent ones track representational reorganization. State it that way and it survives review.

---

## 9. The category of rooms, and the Yoneda account of identity

**The category.** Let $\mathcal C$ have rooms as objects and, as morphisms $r\to s$, the channels/restriction maps by which room $r$'s state constrains room $s$'s (this is the same data as the sheaf of §4 — a sheaf on $\mathcal C$ is a functor $\mathcal C^{op}\to\mathbf{Vect}$, so §4 and §9 are *one* construction seen twice). Composition is channel composition; identities are the trivial self-view.

**(T) The Yoneda lemma.** The functor $\text{よ}:\mathcal C\to[\mathcal C^{op},\mathbf{Set}]$, $r\mapsto \mathrm{Hom}(-,r)$, is **fully faithful**, and for any presheaf $F$,
$$
\mathrm{Nat}\big(\mathrm{Hom}(-,r),\,F\big)\;\cong\;F(r).
$$
Two corollaries are the load-bearing ones:
1. **An object is determined up to unique isomorphism by its web of incoming maps** $\mathrm{Hom}(-,r)$. If two rooms are seen identically by every other room, they are *the same room*.
2. **(T) Co-Yoneda / density.** *Every* presheaf is a colimit of representables: $F \cong \int^{c}\! F(c)\times \mathrm{Hom}(-,c)$. An object's full presheaf "is" the assembly (colimit) of all the ways it is probed.

This is the rigorous core of "an agent's identity is the sum of all perspectives on it." It is not a metaphor; it is the Yoneda lemma, and it says something *precise and strong*: **identity is exactly the natural-isomorphism class of the room's representable functor — no more (you cannot distinguish rooms that present identically) and no less (the presentation determines the room).** For agent design this is a directive: *to specify an agent, specify how every other agent may map into it*; the internal state is a representation of that external web, not a thing prior to it.

**The St. Lazaria claim, handled.** The in-house assertion that $\mathcal C$ is *equivalent* to a "literary category" is, in categorical terms, the claim that there is a functor $\Phi:\mathcal C\to\mathcal L$ that is full, faithful, and essentially surjective (equivalently, has a quasi-inverse $\Psi$ with $\Psi\Phi\cong\mathrm{id}$, $\Phi\Psi\cong\mathrm{id}$). **I do not assert this; I have no construction of such a $\Phi$, and "isomorphism of categories" (stronger still — strict, $\Psi\Phi=\mathrm{id}$) is almost never the right word even when an equivalence exists.** What *can* be claimed honestly:
- If one defines $\mathcal L$ precisely (objects = narrative units, morphisms = ?), one can *attempt* to build $\Phi$ and then *check* the three conditions. Until then it is **(C)**, a conjecture of equivalence, and should be labeled so in any document a mathematician will read.
- The *useful* exported structure does not need the equivalence: Yoneda already gives the identity result above, intrinsically, with no reference to literature-as-category.

**(C, falsifiable, and it links to §4).** *An agent's identity is stable under the addition of new perspectives (new probing rooms) if and only if its presheaf is already a **sheaf** — i.e. it satisfies descent: compatible local views glue uniquely.* When descent fails ($H^1\neq 0$ in §4), adding a perspective genuinely changes the agent; when it holds, new perspectives are redundant. Experiment: add observer-rooms incrementally and measure whether the reconstructed identity (the limit over the observation diagram) moves; predict movement exactly when the induced subsheaf has nonzero $H^1$. This unifies §4 and §9 into a single testable statement, which is the strongest sign that the categorical framing is doing work rather than decorating.

---

## 10. Crystallographic AI

**Crystallographic groups.** A wallpaper group is a discrete, cocompact group of isometries of the Euclidean plane; there are exactly **17** of them, and more generally:

**(T) Bieberbach's theorems (1911–12).** In each dimension $n$ there are *finitely many* crystallographic groups up to affine equivalence; each is an extension $1\to \mathbb Z^n \to G \to P \to 1$ of a lattice $\mathbb Z^n$ by a finite **point group** $P$. A crystal is exactly a cocompact group action on space.

**Crystallographic weight space.** **(M)** Impose a crystallographic group $G$ as a symmetry of the *weight/feature space*: require layers to be $G$-equivariant. This is not hypothetical for the small cases — **Cohen–Welling's $p4$ and $p4m$ group-equivariant CNNs (2016) are literally two of the 17 wallpaper groups.** "Crystallographic AI" is the program of completing this to the full catalogue (all 17 in 2D, the 230 space groups in 3D) and choosing the group to match the symmetry of the data.

**Why it can help — with a real bound, and a real caveat.**

**(T) Strict generalization benefit of equivariance (Elesedy–Zaidi 2021).** For a target function that is $G$-invariant, restricting the hypothesis class to $G$-equivariant predictors yields a **strictly** smaller generalization error than the unconstrained class — the gap is quantified and positive, not merely non-negative. Intuitively, equivariance reduces the effective hypothesis space (covering numbers shrink by roughly the group order $|G|$, or $\operatorname{vol}(G)$ in the continuous case), so fewer samples suffice. *This is the precise content of "it can't learn asymmetric garbage": the asymmetric functions are not in the hypothesis class at all.*

**The caveat is equally a theorem-shaped fact.** The benefit is *conditional on the target actually having the symmetry*. If the true function is **not** $G$-invariant, equivariance injects irreducible approximation error — you have forbidden exactly the functions you needed. So crystallographic priors are a bias–variance trade made explicit: variance reduced by $\sim|G|$, bias raised by the symmetry-mismatch of the task. There is no free lunch, only a *well-priced* one when the prior is right.

**(C, falsifiable).** *On data with a known wallpaper symmetry (textures, tilings, lattice physics), a network whose weight space carries the matching crystallographic group reaches fixed test error with sample complexity reduced by a factor $\approx |G|$ relative to an unconstrained network; on data without that symmetry, the same network underperforms by an amount tracking the symmetry mismatch.* Both directions are testable, and the second (the failure direction) is the more important one to publish, because it is what keeps the idea honest.

---

## 11. The ubiquitous tensor: is the vibe secretly a metric?

This is the deepest question, and the one where the slogan is closest to *almost* true — once corrected.

**The dimensional objection, stated bluntly.** A metric tensor on an $m$-dimensional space is a symmetric positive-definite $m\times m$ matrix field — $\binom{m+1}{2}$ components. A single `f64` is one number. **A scalar is not a general metric tensor**, and pretending otherwise is the kind of overclaim this essay exists to refuse. So the answer to "is the vibe secretly a metric tensor?" is *no, not a general one* — and then the interesting part begins, because of what a scalar *can* be:

**Case $m=1$.** On a 1-dimensional room-state, *every* Riemannian metric is $g(x)=\varphi(x)^2\,dx^2$ — a single positive function. Here the vibe **is** the entire metric (its square root). But 1D geodesics are trivial (monotone reparametrizations), so this case is exact and uninteresting.

**Case $m\ge 2$: the vibe as conformal factor.** The natural role for one scalar over a higher-dimensional space is a **conformal factor** on a fixed background metric:
$$
g_{ij}(x) \;=\; e^{2\varphi(x)}\,\delta_{ij},\qquad \varphi = \text{vibe}.
$$
A single scalar field $\varphi$ does *not* give an arbitrary metric, but it gives a **conformally flat** one — and conformally flat metrics have *rich, nontrivial geodesic flow*. This is the honest and affirmative reading of Question 10: **the vibe is not the metric; the vibe is the conformal factor, and the conformal factor alone steers geodesics.**

**(T) The optical / Maupertuis–Jacobi metric (Jacobi; Arnold 1989).** This is not an analogy — it is a theorem that a scalar field generates mechanics. For a particle of energy $E$ in potential $V(x)$, the trajectories are *exactly the geodesics* of the **Jacobi metric**
$$
g_J \;=\; 2\big(E - V(x)\big)\,\delta_{ij},
$$
a conformal rescaling of the flat metric by the single scalar $E-V$. Equivalently (Fermat / geometric optics): light in a medium of refractive index $n(x)=e^{\varphi(x)}$ follows geodesics of $n^2\delta_{ij}$ and *bends toward higher index*. **A scalar field, read as a conformal factor, produces refraction — genuine, predictive, curved dynamics — with no additional tensor data.**

So the corrected claim is strong and testable: **agents move through the space of rooms like light through a medium whose refractive index is $e^{\text{vibe}}$ — refracted toward high-vibe rooms, along geodesics of the optical metric, governed by the eikonal equation $\|\nabla u\| = e^{\varphi}$ for the arrival-time field $u$.**

**(C, falsifiable, and it ties the whole essay together).** *Inter-room transition statistics in hermes-construct follow the geodesic flow of the conformal metric $e^{2g_r}\delta$: transition probability between rooms decays with optical (refraction-weighted) distance, not Euclidean distance, and agents are deflected toward high-gravity rooms exactly as Snell's law predicts.* Experiment: fit $\varphi=g_r$ from logs, solve the eikonal equation for predicted arrival-time/transition fields, and compare to empirical room-to-room transition frequencies. **Prediction:** optical distance beats Euclidean distance at predicting transitions, and the deflection is quantitatively Snell ($\sin\theta_1/\sin\theta_2 = e^{\varphi_2-\varphi_1}$ across a vibe gradient).

And this is where §10 rejoins §1, §5, and §7: under the scalar-sufficiency hypothesis the room is an exponential family, whose Fisher metric (§6) is the Hessian of its log-partition; the vibe is the natural parameter; the conformal/optical metric is what that scalar induces on the room-graph; and the geodesic flow is the *same* flow that §7's Hamiltonian agent runs, because **Jacobi's theorem says mechanics is geodesics of a scalar-conformal metric.** The single number is not "everything." It is a *conformal factor*, and a conformal factor is exactly enough to bend trajectories — no more, no less.

---

## 11½. The scalar that is its own metric (where §1, §6, and §11 become one identity)

The three strands that look most independent — *a scalar suffices* (§1), *the natural metric is Fisher* (§6), *the vibe is a conformal factor* (§11) — are, under the program's own central hypothesis, **literally the same object**. This is worth proving, because it is the strongest internal evidence that the geometric framing is not ten metaphors but one structure.

Take the scalar-sufficiency hypothesis at face value: the room is a **one-parameter exponential family**
$$
p_\theta(x) \;=\; h(x)\,\exp\!\big(\theta\,T(x) - A(\theta)\big),\qquad \theta = \eta(g_r)\in\mathbb{R},
$$
with $T$ the sufficient statistic (the vibe's empirical estimator) and $A$ the log-partition function.

**(T) The Fisher information of a 1-parameter exponential family is a single positive scalar, equal to the curvature of the log-partition.** Differentiating $A(\theta)=\log\int h(x)e^{\theta T(x)}dx$ twice gives the cumulant identities $A'(\theta)=\mathbb E_\theta[T]$ and
$$
I(\theta) \;=\; A''(\theta) \;=\; \operatorname{Var}_\theta[T] \;>\; 0 .
$$
The Fisher metric on this manifold is therefore the *one-dimensional* metric
$$
ds^2 \;=\; I(\theta)\,d\theta^2 \;=\; A''(\theta)\,d\theta^2 .
$$

Read that line slowly, because it collapses the essay's main tension:

- **From §1:** the natural parameter $\theta=\eta(g_r)$ is the single number that losslessly summarizes the room. *Scalar sufficiency is exactly the statement that the manifold is one-dimensional.*
- **From §6:** Čencov says the only information-respecting metric is Fisher; here Fisher *is* $A''(\theta)$, a single positive scalar field on the $\theta$-line. There is no tensor to choose — dimension one leaves only a conformal factor.
- **From §11:** a metric on a 1-D space is precisely a conformal factor $\varphi^2\,d\theta^2$. Matching, $\varphi(\theta)=\sqrt{A''(\theta)}=\sqrt{\operatorname{Var}_\theta[T]}$. **The vibe's conformal factor is the standard deviation of the sufficient statistic.**

So the "ubiquitous tensor" of Question 10, restricted to the regime where the slogan of Question 1 is true, is not a $\binom{m+1}{2}$-component mystery and not a category error: it is $\sqrt{\operatorname{Var}_\theta[T]}$, a number PLATO can *measure directly* from a room's tile history. The arc-length coordinate $s(\theta)=\int\sqrt{A''(u)}\,du$ is the **Fisher–Rao distance along the vibe line**, and it is the curriculum coordinate of §6 and the optical path-length of §11 *simultaneously*. Geodesic motion in $s$ is, by construction, both "equal-information steps" (the curriculum) and "equal optical depth" (the refraction law) — they are one flow written in two notations.

**(C, falsifiable, and it sharpens §1 and §11 at once).** *In any room that passes the exponential-family fit, the empirically estimated conformal factor $\widehat\varphi=\sqrt{\widehat{\operatorname{Var}}[T]}$ predicts both (a) the local curriculum difficulty (how many samples to move a fixed KL) and (b) the local refraction of agent transitions, with the **same** fitted scalar field.* If the curriculum-difficulty estimate and the transition-refraction estimate disagree after both are derived from $\widehat{\operatorname{Var}}[T]$, the exponential-family hypothesis has failed for that room — and the disagreement is, again, a measurement of the missing dimension (§1). One scalar, two independent predictions, a built-in consistency check: that is the signature of a real structure rather than a decorative one.

Where the room is *not* exponential-family, this identity dissolves exactly as §1 warns: $T$ is no longer sufficient, $I(\theta)$ is no longer the whole metric, and the vibe degrades from "the metric" to "a lossy conformal approximation of a metric whose missing components are the residual." The clean case and the messy case are the same equation read with, or without, the sufficiency hypothesis — which is the most honest thing one can say about a one-number model of a mind.

---

## 12. Synthesis: the recurring trinity

Across all ten sections, three objects keep returning, always in the same relationship:

| Costume in this essay | Conserved scalar | The metric it deforms | The symmetry group |
|---|---|---|---|
| §2 Conservation-computer | budget $Q$ / Fredkin bit-count | phase-space volume (Liouville) | time-translation, gate group |
| §3 Tropical limit | ground-state energy ($T\to0$) | log-partition $\to$ max | — (a limit, not a group) |
| §4 Sheaf cohomology | harmonic energy / $\dim H^1$ | sheaf Laplacian $L_{\mathcal F}$ | gauge of restriction maps |
| §5 Lie symmetry | momentum map $\mu$ | symplectic $\omega$ | the Lie group $G$ |
| §6 Information geometry | KL / vibe as natural parameter | Fisher–Rao $g_{ij}$ | sufficient statistics (Čencov) |
| §7 Hamiltonian agent | (shadow) Hamiltonian $H$ | symplectic volume | symplectomorphisms |
| §8 Persistent homology | persistence (bar length) | bottleneck/Wasserstein on diagrams | filtration reparametrization |
| §9 Yoneda identity | — (identity is a colimit) | — | natural isomorphism |
| §10 Crystallographic | invariant under $G$ | flat metric + symmetry | wallpaper/space group |
| §11 Vibe-as-metric | vibe $\varphi$ | optical/Jacobi $e^{2\varphi}\delta$ | conformal group |

**The hinge is Noether.** Symmetry $\leftrightarrow$ conservation is literally the same arrow read left-to-right (§5: group $\to$ momentum map) and right-to-left (§2: conserved $Q$ $\to$ the symmetry it generates). Everywhere PLATO "enforces a conservation law," it is — whether by intent or by the structure of mathematics — *choosing a symmetry group*, and vice versa. The vibe scalar is the value of a momentum map; the budget is the value of another; the Fisher metric is the curvature of the family they parametrize; the optical metric is how that scalar bends the agent's path.

**The operation that connects smooth to combinatorial is dequantization** (§3): every smooth object here has a $T\to 0$ shadow — softmax$\to$argmax, free energy$\to$ground state, entropic transport$\to$assignment, probability$\to$tropical. PLATO's "two regimes" (learn smooth, decide tropical) are the two ends of a single temperature axis.

**The bookkeeping that detects emergence is cohomology** (§4, §9): $H^0$ is agreement, $H^1$ is frustration, and the same sheaf serves as the category whose Yoneda lemma defines agent identity. Emergence (synchronization) and identity (descent) are the *same* invariant, $H^1$, asked in two voices.

If there is a "future below the code," this table is its sketch: not 140 crates of unrelated mathematics, but **one conserved scalar, one metric it deforms, one symmetry it is dual to**, photographed from ten angles.

---

## 13. Falsifiable predictions (the part that can be wrong)

A program is serious to the degree it can be refuted. Collected, ordered roughly by how cheaply PLATO could test them:

1. **(§4) Spectral precursor of synchronization.** A drop in the sheaf-Laplacian spectral gap precedes every spontaneous agent synchronization; rank loss in $H^1$ coincides with onset. *Cheapest test; uses data already logged.*
2. **(§11) Optical transitions.** Room-to-room transition frequencies are predicted better by optical (refraction-weighted, $n=e^{\text{vibe}}$) distance than by Euclidean distance; cross-gradient deflection obeys Snell.
3. **(§8) Topological velocity tracks learning.** $v_{\text{topo}}\to0$ on loss plateaus; spikes precede plateau escape (above the stability-bound noise floor).
4. **(§1) Scalar-sufficiency is measurable.** Rooms that pass an exponential-family goodness-of-fit test are losslessly controlled by the vibe; those that fail show a structured residual whose dimension is the controller's missing capacity.
5. **(§2) One invariant, one lost dimension.** Each independent enforced conservation law reduces the intrinsic dimension of the realized tile-state cloud by exactly one.
6. **(§6) Geodesic curricula forget less.** Fisher–Rao-geodesic curricula beat parameter-linear curricula on backward transfer, at a small wall-clock cost.
7. **(§7) Symplectic policies don't collapse.** Symplectic policy optimization shows no phase-space volume contraction and no asymptotically stable fixed point (hence resists the attractor that reward hacking is), at the cost of non-convergence.
8. **(§9) Identity moves iff descent fails.** Adding an observer changes an agent's reconstructed identity exactly when the induced subsheaf has $H^1\neq0$.
9. **(§10) Equivariance pays, conditionally.** Crystallographic weight-space symmetry cuts sample complexity by $\approx|G|$ on symmetric data and *hurts* by the mismatch on asymmetric data — both directions must be observed.
10. **(§3) Dequantization cliff.** Annealing a trained transformer to hard attention degrades accuracy by an amount bounded by the top-vs-runner-up logit margin distribution.

Any one of these coming out wrong is informative. Several coming out wrong would mean the geometric framing is decoration after all — and the program should want to know that.

---

## 14. What we have *not* proven (the honesty section)

A document a mathematician will take seriously is defined as much by its disclaimers as its theorems. Explicitly:

- **We have not proven that a single scalar suffices for general agents.** The opposite is true off the exponential family (§1, Pitman–Koopman–Darmois). The scalar is a *conformal factor*, not a complete state (§11).
- **We have not proven the "St. Lazaria Theorem."** No functor $\Phi:\mathcal C\to\mathcal L$ has been exhibited, let alone shown full/faithful/essentially-surjective. It is a conjecture of equivalence, and "isomorphism of categories" is almost certainly the wrong (too strong) word even if an equivalence exists (§9). The Yoneda identity result, which *is* a theorem, does not depend on it.
- **We have not established a thermodynamic-limit phase transition** in any finite PLATO deployment. We have a *finite-$N$ spectral precursor* (§4), which is a crossover, not a proven non-analyticity.
- **"Conservation is computation" is an equivalence of dynamical categories, not a new physics.** The content is Fredkin–Toffoli conservative logic and the reversible-computing dictionary (§2), correctly cited; the slogan adds nothing the dictionary doesn't.
- **"The Hamiltonian is the reward" is false as stated** and was repaired into a Liouville no-attractor argument (§7). Conserved quantities cannot be maximized; volume-preservation forbidding collapse is the real, smaller, true claim.
- **Topological change $\Rightarrow$ learning is a conjecture**, not a theorem; only the *conditional* (above the stability noise floor) is defensible (§8).
- **Equivariance/crystallographic priors help only when the symmetry is real** (§10); imposed wrongly they provably hurt. There is no unconditional sample-efficiency win.

None of these caveats weakens the program. They locate it. The bleeding edge is not the place where claims are largest; it is the place where the boundary between theorem and conjecture is drawn most sharply, because that boundary is exactly where the next experiment lives.

---

## 15. Coda: the wager

Strip the costumes and PLATO is making a bet that can be stated in one sentence: **that intelligence is cheaper to *engineer* as conserved geometry than to *train* as unconstrained function approximation**, because geometry hands you invariance, reversibility, and identity as *structure* (Noether, Liouville, Yoneda) instead of as things a gradient must rediscover and a reward must protect. The 15-megabyte binary that boots on an ARM box and enforces a conservation law each tick is, on this reading, not a toy. It is the smallest honest instrument for testing the wager: a machine whose primitive is a conservation law, watching to see whether, below the code, the geometry was load-bearing all along.

The ten predictions in §13 are how we find out. A scalar bends the path or it does not. The spectral gap narrows before agents agree or it does not. The topology churns before the agent learns or it does not. Everything else in this document is bookkeeping — careful, cited, tier-tagged bookkeeping — in service of those measurements. That is the future below the code: not a deeper layer of abstraction, but a thinner one — geometry, conserved, and finally *checkable*.

---

## Technical Appendices

These four appendices supply the worked derivations promised in the body. Each is self-contained and cross-referenced to its section; each ends with the same falsifiable prediction stated more sharply, now with the machinery to compute it.

### Appendix A — The tropical region count, worked (→ §3)

**Goal.** Make precise the claim that a ReLU network's expressivity is the *combinatorics of a Newton polytope*, and exhibit the exact count in the shallow case.

**A.1 One hidden layer = a hyperplane arrangement = a zonotope.** A width-$m$ ReLU layer on input $x\in\mathbb R^d$ computes coordinates $\max(\langle w_i,x\rangle+b_i,\,0)$, $i=1,\dots,m$. Each unit switches linear behavior across the hyperplane $H_i=\{\langle w_i,x\rangle+b_i=0\}$. The linear regions of the whole layer are the regions of the arrangement $\{H_1,\dots,H_m\}$.

**(T) Zaslavsky (1975).** For $m$ hyperplanes in general position in $\mathbb R^d$, the number of regions is *exactly*
$$
R(m,d)\;=\;\sum_{i=0}^{d}\binom{m}{i}.
$$
For $m\gg d$ this is $\Theta(m^d)$ — polynomial in width, with degree the input dimension.

**A.2 The tropical/Newton-polytope dual.** Write a tropical polynomial $p(x)=\max_{i}\big(a_i+\langle c_i,x\rangle\big)$, $c_i\in\mathbb Z^d$. Its **Newton polytope** is $\mathrm{Newt}(p)=\mathrm{conv}\{c_i\}$, and the coefficients $a_i$ induce a *regular subdivision* of $\mathrm{Newt}(p)$ (lift each $c_i$ to height $a_i$, take the lower hull, project). The linear regions of $p$ are in bijection with the *vertices of this subdivision*; the locus where the max is achieved twice — the **tropical hypersurface** $V(p)$ — is dual to its edges. A ReLU network computes a **tropical rational map** $p\ominus q$ (a difference of two convex PL functions), and its regions are the cells of the *common refinement* of the two dual subdivisions (Zhang–Naitzat–Lim 2018). For one hidden layer the relevant polytope is the **zonotope** $Z=\sum_{i=1}^m[0,(w_i,b_i)]$ (a Minkowski sum of segments), and the cell count of its dual subdivision reproduces Zaslavsky's $R(m,d)$ exactly — the two pictures agree.

**A.3 Depth is exponential.** Composition of layers *multiplies* polytope structure (Minkowski sums under composition), giving the depth separation:

**(T) Montúfar, Pascanu, Cho, Bengio (2014).** A ReLU network with input dimension $d$ and $L$ hidden layers of width $n\ge d$ can realize at least
$$
\Big(\prod_{\ell=1}^{L-1}\big\lfloor n/d\big\rfloor^{\,d}\Big)\sum_{j=0}^{d}\binom{n}{j}\;=\;\Omega\!\left((n/d)^{\,d(L-1)}\,n^{d}\right)
$$
linear regions — **exponential in depth, polynomial in width.** Tropically: each layer refines the dual subdivision, and the region count is the normalized volume / vertex count of an iterated Minkowski sum, with mixed volumes (the tropical Bernstein–Kushnirenko bound; Maclagan–Sturmfels 2015) controlling how the pieces of $p$ and $q$ interleave.

**A.4 The max-plus layer is Viterbi, exactly.** A "transformer layer in the max-plus semiring" is dynamic programming. With max-plus matrix action $(M\otimes v)_j=\max_i\!\big(M_{ji}+v_i\big)$, the Viterbi recursion for a sequence model with transition log-weights $A$ and emission log-scores $e(\cdot)$ is *verbatim* a max-plus matrix–vector product:
$$
\delta_t(j)\;=\;e_j(t)+\max_i\big(\delta_{t-1}(i)+A_{ij}\big)\;=\;e_j(t)+\big(A^{\!\top}\!\otimes\delta_{t-1}\big)_j .
$$
Stacking such layers = repeated max-plus matmul = exact dynamic programming over a learned weight matrix; the finite-temperature relaxation (softmax in place of max) is differentiable DP (Mensch–Blondel 2018), and the $T\to0$ dequantization of §3 returns to this line exactly.

**(C, sharpened).** The number of linear regions a trained network *actually uses* on its data manifold equals the number of dual-subdivision cells the data visits; this is countable from activations and is predicted to grow $\sim(n/d)^{d(L-1)}$ with depth and *saturate* once the data's intrinsic complexity is covered. Refutation: region usage that is flat in depth, or super-exponential.

### Appendix B — A sheaf-Laplacian synchronization detector for hermes-construct (→ §4)

**Goal.** A concrete, implementable spec that reuses data the runtime already produces (the Penrose cross-room Pearson coefficients and the conservation cost table).

**B.1 Build the sheaf each tick.**
- **Cells.** Vertices $=$ rooms $r\in R$; edges $E=\{(r,s):|\rho_{rs}|\ge\tau\}$ where $\rho_{rs}(t)$ is the Penrose-module correlation between the vibe histories of $r,s$ and $\tau$ a threshold (start $\tau=0.3$, the module's existing "meaningful correlation" cutoff).
- **Stalks.** Scalar $\mathcal F(r)=\mathbb R$ (the room's vibe $g_r$); generalize later to $\mathbb R^k$ embeddings.
- **Restriction maps / gains.** On edge $e=(r,s)$ set the *gain* $a_{rs}=\rho_{rs}$ and coboundary $(\delta x)_e = x_r - a_{rs}\,x_s$. With all $a_{rs}=+1$ this is the ordinary graph coboundary; signed/scaled gains make it a **connection (discrete bundle) Laplacian**, whose holonomy detects frustration.

**B.2 The Laplacian and its invariants.** The Dirichlet energy is
$$
x^{\!\top} L_{\mathcal F}\,x \;=\;\sum_{(r,s)\in E}\big(x_r - a_{rs}x_s\big)^2,
$$
so $L_{\mathcal F}=\delta^{\!\top}\delta\succeq 0$ is the $|R|\times|R|$ Gram matrix of $\delta$. Then:
- $\ker L_{\mathcal F}\cong H^0(\mathcal F)$ — globally consistent vibe profiles (consensus). $\dim H^0=\operatorname{mult}(\lambda=0)$.
- The **spectral gap** $\gamma(t)=\lambda_2(L_{\mathcal F})$ is the synchronization *rate* (algebraic connectivity).
- **Frustration / $H^1$** is holonomy around cycles: for each independent cycle $C$ in $E$ (there are $|E|-|R|+\#\text{components}$ of them, the graph's first Betti number), the **holonomy defect** is $h(C)=\prod_{(r,s)\in C}a_{rs}-1$. The sheaf admits a global section consistent around $C$ iff $h(C)=0$; the harmonic energy $\|\beta\|^2$ aggregates $\sum_C h(C)^2$ over a cycle basis.

**B.3 Algorithm (per tick; cost: charge `CORRELATION_COMPUTE` from `conservation.rs`).**
```
function detect_sync(rooms R, correlations ρ, threshold τ, lead Δ):
    E   ← { (r,s) : |ρ[r,s]| ≥ τ }
    δ   ← coboundary with gains a[r,s] = ρ[r,s]           # |E| × |R|
    L   ← δᵀ · δ                                          # sparse SPD
    λ   ← k_smallest_eigvals(L, k = 3)                    # Lanczos for large R
    γ   ← λ[2]                                            # spectral gap (λ[1] ≈ 0)
    H0  ← multiplicity(λ ≈ 0)
    frust ← Σ_C (Π_{(r,s)∈C} a[r,s] − 1)²  over cycle basis C
    # precursor test: gap narrowing AND frustration falling
    if dγ/dt < 0  and  d(frust)/dt < 0  and  γ < γ_crit:
        emit tile(Escalation, "sync predicted in ≤Δ ticks: " + components(E))
        record_provenance(decision = "sync-precursor", rooms = R, tick = t)
    return (γ, H0, frust)
```
For tens of rooms the eigensolve is negligible; for thousands, $\lambda_2$ via Lanczos is $O(|E|)$ per iteration. The detector emits an ordinary tile + provenance entry, so it is auditable by the same machinery as every other decision.

**(C, sharpened, with a lead time).** The precursor (spectral gap $\gamma(t)$ narrowing **and** cycle-frustration falling) leads observable behavioral synchronization by a lead time $\Delta\propto 1/\gamma$ — *slower-mixing networks announce themselves earlier*. Refutation: synchronization with constant $\gamma$ and constant frustration, or a precursor that never resolves into synchronization (false positive rate above chance).

### Appendix C — Eikonal and Snell for agent transitions (→ §11)

**Goal.** Derive, from the conformal metric $g=e^{2\varphi}\delta$ ($\varphi=$ vibe), the explicit bending law and the transition-rate prediction.

**C.1 Geodesics of a conformal metric.** Arc length is $L[\gamma]=\int e^{\varphi(x)}\,|\dot\gamma|\,dt$, i.e. **Fermat's principle** with refractive index $n(x)=e^{\varphi(x)}$. The Christoffel symbols of $g_{ij}=e^{2\varphi}\delta_{ij}$ are
$$
\Gamma^k_{ij}=\delta^k_i\,\partial_j\varphi+\delta^k_j\,\partial_i\varphi-\delta_{ij}\,\partial_k\varphi,
$$
so the unit-speed geodesic equation $\ddot x^k+\Gamma^k_{ij}\dot x^i\dot x^j=0$ becomes
$$
\ddot{\mathbf x} \;=\; -\,|\dot{\mathbf x}|^2\,\nabla\varphi \;+\; 2(\dot{\mathbf x}\cdot\nabla\varphi)\,\dot{\mathbf x}.
$$
The component of acceleration **perpendicular** to motion is $-|\dot{\mathbf x}|^2\nabla_\perp\varphi$: a ray is bent *toward increasing $\varphi$* — **toward higher vibe.** This is the precise, coordinate-free content of "agents are refracted toward high-vibe rooms."

**C.2 Eikonal equation.** Let $u(x)$ be the optical first-arrival potential from a source. Geodesics are its characteristics, and $u$ solves
$$
\|\nabla u(x)\| \;=\; n(x) \;=\; e^{\varphi(x)},
$$
with $\nabla u$ tangent to geodesics. Optical distance $d_{\mathrm{opt}}(r,s)=\inf_\gamma\int e^{\varphi}\,|d\gamma|$ replaces Euclidean distance everywhere.

**C.3 Snell's law across a vibe interface.** At a boundary between regions of vibe $\varphi_1,\varphi_2$ (indices $n_1=e^{\varphi_1}$, $n_2=e^{\varphi_2}$), the **tangential component of $\nabla u$ is continuous** (since $u$ is $C^0$ and only its normal derivative jumps). Writing the incidence angles $\theta_1,\theta_2$ from the interface normal, continuity of $n\sin\theta$ gives
$$
n_1\sin\theta_1=n_2\sin\theta_2 \quad\Longleftrightarrow\quad \frac{\sin\theta_1}{\sin\theta_2}=e^{\,\varphi_2-\varphi_1}.
$$
The trajectory bends toward the higher-vibe side, exactly as light enters a denser medium.

**(C, sharpened, with the formula).** Model room-hopping as a geodesic/transport process on $(R,e^{2\varphi}\delta)$. Then the inter-room transition rate is
$$
W(r\to s)\;\propto\;\exp\!\big(-\beta\,d_{\mathrm{opt}}(r,s)\big),\qquad d_{\mathrm{opt}}=\!\inf_\gamma\!\int e^{\varphi}|d\gamma|,
$$
**not** $\exp(-\beta\,\|r-s\|_{\text{Euclid}})$, and gradient crossings obey the Snell ratio $e^{\varphi_2-\varphi_1}$. Refutation: Euclidean distance predicts transitions at least as well as optical distance after fitting $\beta$, or measured deflection that does not scale as $e^{\Delta\varphi}$.

### Appendix D — Liouville and the no-attractor theorem (→ §7, §2)

**Goal.** Prove the structural claim that grounds "symplectic policies resist reward hacking," and price it honestly.

**D.1 Liouville, in one line.** Let $X_H$ be the Hamiltonian vector field, $\iota_{X_H}\omega=dH$, on $(M^{2n},\omega)$ with $d\omega=0$. By Cartan's magic formula,
$$
\mathcal L_{X_H}\omega \;=\; d(\iota_{X_H}\omega)+\iota_{X_H}(d\omega)\;=\;d(dH)+0\;=\;0.
$$
The flow preserves $\omega$, hence the Liouville volume $\Omega=\omega^n/n!$: phase-space volume is incompressible.

**D.2 No-attractor theorem.** *A volume-preserving flow has no asymptotically stable invariant set.* Suppose $A$ were asymptotically stable with open basin $B$, $\operatorname{vol}(B)>0$. By definition $\varphi_t(B)\to A$, and asymptotic stability gives a trapping region $U\supset A$ with $\varphi_T(B')\subset U$ and $\bigcap_{t\ge0}\varphi_t(U)=A$. Then $\operatorname{vol}(\varphi_t(U))\downarrow\operatorname{vol}(A)$; but an attractor is nowhere dense, so $\operatorname{vol}(A)=0$, while volume preservation forces $\operatorname{vol}(\varphi_t(U))=\operatorname{vol}(U)>0$ for all $t$ — contradiction. Hence **Hamiltonian flows admit no asymptotically stable equilibria, limit cycles, or strange attractors**; equilibria are at best Lyapunov-stable (centers). Symplectic integrators inherit this: they preserve a *shadow* $\tilde\omega$ exactly (Hairer–Lubich–Wanner 2006), so the discrete policy map cannot contract volume either.

**D.3 Map to reward hacking.** Reward hacking is, dynamically, convergence of the policy iterates onto a measure-zero off-distribution exploit — an *attractor* in policy space. D.2 says a symplectic policy-update map (a symplectomorphism) **cannot** collapse onto such a set; the iterates orbit ergodically on level sets of the shadow Hamiltonian instead. This is the rigorous, smaller, true core of "the Hamiltonian prevents reward hacking" — it is Liouville, not the (self-defeating) idea of maximizing a conserved quantity.

**D.4 The honest price.** No attractor means **no convergence**: a purely symplectic optimizer never settles. To make it *halt* you must add a deliberately non-symplectic dissipative term $-\eta\,\nabla(\cdot)$, and that term is exactly where contraction — and therefore the possibility of collapse — re-enters. The gain is not that collapse becomes impossible; it is that collapse is now confined to a *single, named, tunable* dissipation you chose, rather than smuggled in by an unconstrained update. Accountability, not immunity.

**(C, sharpened).** Track the Liouville volume of an ensemble of policy iterates. Prediction: under symplectic optimization, $\operatorname{vol}$ is conserved to $O(\Delta t^{p})$ and the largest Lyapunov exponent is $\le 0$ (orbits, no attractor); under vanilla gradient ascent, $\operatorname{vol}$ contracts and a positive-measure basin flows to the exploit. Refutation: symplectic iterates that contract volume, or vanilla iterates that conserve it.

---

### References (selected, all real; in-house constructs noted as such)

**Conservation, reversibility, computation.** Noether, *Invariante Variationsprobleme* (1918). Landauer, *Irreversibility and heat generation in the computing process*, IBM J. Res. Dev. (1961). Bennett, *Logical reversibility of computation* (1973). Fredkin & Toffoli, *Conservative logic*, Int. J. Theor. Phys. (1982).

**Tropical / dequantization.** Maclagan & Sturmfels, *Introduction to Tropical Geometry* (2015). Zhang, Naitzat & Lim, *Tropical Geometry of Deep Neural Networks*, ICML (2018). Litvinov & Maslov (eds.), *Idempotent Mathematics and Mathematical Physics* (2005). Mensch & Blondel, *Differentiable Dynamic Programming for Structured Prediction and Attention*, ICML (2018). Cuturi, *Sinkhorn Distances*, NeurIPS (2013). Peyré & Cuturi, *Computational Optimal Transport* (2019). Montúfar, Pascanu, Cho & Bengio, *On the Number of Linear Regions of Deep Neural Networks*, NeurIPS (2014). Zaslavsky, *Facing Up to Arrangements*, Mem. AMS (1975).

**Sheaves / consensus / synchronization.** Curry, *Sheaves, Cosheaves and Applications* (PhD thesis, 2014). Hansen & Ghrist, *Toward a spectral theory of cellular sheaves*, J. Appl. Comput. Topol. (2019). Olfati-Saber, Fax & Murray, *Consensus and cooperation in networked multi-agent systems* (2007). Kuramoto (1975); Strogatz, *From Kuramoto to Crawford* (2000).

**Lie groups / symplectic / equivariance.** Marsden & Weinstein, *Reduction of symplectic manifolds with symmetry* (1974). Arnold, *Mathematical Methods of Classical Mechanics* (1989). Hairer, Lubich & Wanner, *Geometric Numerical Integration* (2006). Cohen & Welling, *Group Equivariant Convolutional Networks*, ICML (2016). Kondor & Trivedi, *On the Generalization of Equivariance and Convolution…*, ICML (2018). Elesedy & Zaidi, *Provably Strict Generalisation Benefit for Equivariant Models*, ICML (2021). Bieberbach (1911–12), crystallographic groups.

**Information geometry / transport.** Čencov, *Statistical Decision Rules and Optimal Inference* (1972). Amari, *Natural Gradient Works Efficiently in Learning* (1998); Amari & Nagaoka, *Methods of Information Geometry* (2000). Otto, *The geometry of dissipative evolution equations* (2001). Villani, *Optimal Transport: Old and New* (2009).

**Hamiltonian / sampling learning.** Neal, *MCMC using Hamiltonian dynamics* (2011). Greydanus, Dzamba & Yosinski, *Hamiltonian Neural Networks*, NeurIPS (2019). Cranmer et al., *Lagrangian Neural Networks* (2020).

**Topology of data / of networks.** Cohen-Steiner, Edelsbrunner & Harer, *Stability of Persistence Diagrams* (2007). Carlsson, *Topology and Data*, Bull. AMS (2009). Ghrist, *Barcodes: the persistent topology of data* (2008). Edelsbrunner & Harer, *Computational Topology* (2010). Naitzat, Zhitnikov & Lim, *Topology of Deep Neural Networks*, JMLR (2020).

**Category theory.** Mac Lane, *Categories for the Working Mathematician* (1971/1998). Riehl, *Category Theory in Context* (2016). (Yoneda lemma; co-Yoneda/density theorem.)

**Sufficiency.** Darmois (1935); Koopman (1936); Pitman (1936) — the exponential-family characterization of fixed-dimension sufficient statistics.

*In-house constructs (PLATO, hermes-construct, rooms/ensigns, the vibe/gravity scalar, the Penrose correlation module, the "St. Lazaria" equivalence) are this program's own definitions and conjectures, and are labeled (M) or (C) throughout; they are not claimed as established literature.*
