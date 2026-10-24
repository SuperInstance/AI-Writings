# Independent derivation task: adjoint update rule on a conserved cellular fabric

You are deriving, independently and from first principles, the adjoint (reverse-mode) update rule for a discrete-time conserved cellular fabric. Show all steps. Be exact and finite-precision-aware where marked.

## Setting

- Fabric state: vector s_t ∈ R^n of cell dial values (the quilt's conserved cells).
- Conservation law: total mass M = Σ_i s_t[i] is invariant under the tick operator. Ticks are mass-preserving: writes move mass between cells; the formal property is stated in docs/ACADEMIC-RIGOR.md §3 as an SVA assertion (induction currently FAILS at L1/L2 — treat conservation as an axiom of the model for this derivation, not a proven theorem).
- Forward step (one tick, unrolled): 
  s_{t+1} = T(s_t, θ_t) = A(s_t) + η · H(s_t) · θ_t
  where A: R^n → R^n is the mass-preserving routing/attention part (column-stochastic, so Σ_i A(s)_i = Σ_i s_i), η > 0 is the Hebbian write rate, H(s_t) ∈ R^{n×p} is the Hebbian coincidence matrix (entries bounded, |H_ij| ≤ 1), and θ_t ∈ R^p are p parameter cells (the things we train).
- Loss: scalar L(s_T) at final tick T. 
- The parameter cells θ are ALSO conserved-mass quantities: Σ_k θ_k = m (constant).

## Derive

1. The adjoint recursion for λ_t = ∂L/∂s_t (give λ_T, then λ_t in terms of λ_{t+1}), and the gradient g = ∂L/∂θ (accumulated across ticks).
2. **The theorem obligation**: prove or disprove — if the mass Σ_i s_t[i] = M for all t and |H_ij| ≤ 1, then the parameter gradient satisfies a bound of the form ||g||_∞ ≤ C(λ) · T · η, i.e. bounded mass + bounded coincidence implies an intrinsic gradient bound (gradient clipping as a THEOREM of the substrate rather than an external safety wrapper). State precisely what extra conditions (if any) you need on A and on λ (e.g., ||λ_{t+1}||_1 bounded) for the bound to close.
3. State the resulting on-chip update rule: θ_{k} ← clip/projection of θ_k − α · g_k back onto the simplex {θ : Σθ = m} (mass-preserving training step). Give the projection in closed form.
4. Give a bit-exact test: a tiny numeric instance (n=2 cells, p=1 parameter, T=3 ticks) with concrete numbers, computed to 6 decimal places, that an implementation must reproduce exactly. Show your computed numbers for λ_3, λ_2, λ_1, g, and the projected θ.

Use concrete small numbers (e.g., η = 0.1, α = 0.05). Assume IEEE-754 float64 for part 4.
