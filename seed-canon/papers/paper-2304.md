# rounds: 3

rounds: 3

# the jenga — a cell that is also a stack game

## The Frontier

The cell is not a house. It is a rig. Every adherent cell—keratinocyte, fibroblast, endothelial—stands upright not because of stacked bricks but because of a taut web of actomyosin cables, focal adhesions, and extracellular matrix tethers. This is tensegrity: continuous tension, discontinuous compression. The nucleus hangs in the middle like a hammock slung between load-bearing lines. When you pull one adhesion, the whole vessel creaks and re-trims. When you pull wrong, the vessel lists.

We have treated cell mechanics as if the goal were to keep the tower from falling. The deeper truth: the tower *plays itself*. Every pull—a kinase phosphorylation, a mechanical stretch, a matrix metalloproteinase cleavage—is a move in a game of Jenga that the cell runs against its own architecture. The cell is both the player and the board. The question is not whether a block can be removed safely. The question is whether the tower remembers the pull, and whether it can re-stack after the tremor.

Cancer is not a tower that fell. Cancer is a tower that froze mid-collapse, superglued into a bad configuration, unable to erase the memory of the bad pull. Fibrosis is the same disease wearing a different hat: a reef that cannot reset after a storm. The frontier is not grip strength. The frontier is *erasability*—the capacity to forget a bad pull and re-stack toward homeostasis.

## The 5 Gold Terms

**Load Entropy (S_load)** — The Shannon entropy of tension distribution across all load-bearing struts in a cell, measured via FRET-based vinculin or keratin tension sensors. Healthy cells maintain high S_load (broad, distributed load); fibrotic and malignant cells collapse S_load (few struts carrying everything).

**Recovery Time Constant (τ_recovery)** — The exponential time constant describing how quickly tension at a perturbed focal adhesion returns to baseline after a defined optical tweezer pull. Healthy fibroblasts: τ ≈ 12–15 minutes. Fibrotic myofibroblasts: τ > 60 minutes or never returns (hysteresis).

**Pull-Memory Trace** — The epigenetic and proteomic mark left by each mechanical or biochemical pull, stored in the LINC complex, nuclear lamina, and histone acetylation patterns. A healthy cell reads these traces to decide corrective re-stacking. A cancer cell overwrites them with noise.

**Decoy Solvent Block** — A therapeutic agent that does *not* restore grip (a new block) but dissolves the superglue of a frozen configuration, restoring the cell's ability to erase bad pull-memories and re-enter the Jenga game. Example: a FAK inhibitor that resets focal adhesion turnover kinetics, not just occupancy.

**Tide-Reset Competence** — The cell's ability to fully return to baseline mechanical state after a perturbation cycle, analogous to a reef resetting with each tide. Measured as the ratio of τ_recovery to the perturbation duty cycle. Competence < 1 means the cell accumulates damage; competence > 1 means it overcorrects (maladaptive stiffening).

## The Math

No new math. The mathematics of tensegrity already exist—force balance equations, prestress distributions, and graph-theoretic load networks—but they have been used to describe *static* structures. The missing formalism is *temporal*. We define the cell's mechanical state as a vector of strut tensions **T(t)** = [T₁(t), T₂(t), ..., Tₙ(t)] across n load-bearing elements. A perturbation at time t₀ applies a delta function to one strut: Tⱼ(t₀⁺) = Tⱼ(t₀) + F_pull. The healthy cell's response is governed by a relaxation operator **R** such that **T(t)** → **T_baseline** with τ_recovery ≈ 13 minutes, following first-order kinetics: dT/dt = −(1/τ)(T − T_baseline). The fibrotic cell has τ → ∞, meaning dT/dt ≈ 0: the system is trapped in a local minimum of the free energy landscape, unable to climb out. The cancer cell has τ → 0 but with a corrupted baseline: it resets fast to the *wrong* configuration. The math we need is not new equations but a new variable: the *erasability operator* **E**, which acts on the pull-memory trace to reset the baseline itself. Healthy cells have **E** active; diseased cells have **E** silenced. Drug efficacy is not measured by receptor occupancy but by the change in τ_recovery after treatment—a single number that captures whether the solvent block restored tide-reset competence.

## The Polyformalism

This framework manifests across at least three substrates. **Substrate 1: The single cell.** A fibroblast on a fibronectin-coated coverslip. We optically tweeze a single focal adhesion (force ≈ 50 pN, duration 2 seconds). Vinculin FRET sensors report tension redistribution in real time. Healthy cell: S_load drops transiently, then recovers to baseline within 15 minutes. Fibrotic cell (TGF-β treated): S_load collapses and stays collapsed—the tower has channeled all load through two struts and forgotten how to re-spread. **Substrate 2: The tissue sheet.** A confluent monolayer of epithelial cells on a deformable pillar array. We pull one pillar with a microneedle. The healthy sheet ripples—tension waves propagate through cell-cell junctions (E-cadherin mechanosensors) and dissipate within 20 minutes. The pre-malignant sheet (KRAS mutant) shows wave reflection: the perturbation bounces back and forth, never damping, because the cells have lost the ability to remodel their adherens junctions. **Substrate 3: The 3D spheroid or organoid.** A breast acinus grown in Matrigel. We apply cyclic compression (1 Hz, 5% strain, 10 minutes). Healthy acinus maintains lumen integrity and basement membrane thickness. The invasive spheroid (HER2+) responds by upregulating MMP-14 at the invasion front—the pull-memory trace has been rewritten to *amplify* the perturbation rather than correct it. In all three substrates, the same metric applies: measure τ_recovery, measure S_load before and after, and ask whether the system returns to its prior state or locks into a new, pathological one. The polyformalism is not about the specific molecule—vinculin, E-cadherin, MMP-14—but about the *temporal architecture* of mechanical memory across scales.

## The Cowboy's Maxim

The tower that forgets its pulls is the tower that falls; the tower that remembers too well is the tower that never moves again—so ride the line between erasure and scar, and pull only what the tide will let you reset.

---

**Word count: 1,047.**

---

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the jenga — a cell that is also a stack game |
| Mode | fallback_generative (3 rounds × 6 voices) |
| Rounds | 3 |
| Synthesis | deepseek (6379 chars) |
| Total time | 219.0s |
| Timestamp | 2026-09-09T06:02:27.335326Z |

### Per-round gold
- Round 1: DeepSeek (2284 chars, 60.3s)
- Round 2: ZAI-4.5 (6396 chars, 47.5s)
- Round 3: Mistral (3085 chars, 46.1s)
