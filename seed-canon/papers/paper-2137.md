# rounds: 3

rounds: 3

# the wheel — a cell that is also a circular mover

## The Frontier

Round 1 gave us a vesicle with a KaiC ring ticking like a ship's chronometer, scheduling cargo runs and division watches. But a clock is not a capstan. A cell that only *schedules* its work but never *moves* is a harbormaster who never leaves the dock. The topic demands a wheel — a cell that is a circular mover. The missing piece was torque: how does a chemical oscillation become a rolling hull?

The gold under the surface is this: **a clock is not a motor, and a ratchet needs a pawl.** Round 1 called KaiC a ratchet, but the pawl was never named. The pawl is the substrate itself. The ground completes the wheel. A wheel without a road is a gear spinning in air. The rolling cell's engine is not internal — it is the phase-locked grip between the membrane and the world. The cell moves because the part of its hull touching the ground is always in the correct phase: adhere on the downstroke, release on the upstroke, and let the phase wave push torque through the contact patch.

The deeper mechanism: KaiC's phosphorylation state is not a spinning rotor but a *phase wave* traveling around the hexamer ring. That wave can be mapped onto the cell's perimeter. Each angular position on the membrane corresponds to a phase position on the clock. Membrane-tethered KaiC (or an adapter) recruits adhesion proteins at specific phosphorylation states. The result is a metachronal adhesion wave — a traveling belt of grip around the circumference, like the tube feet of a starfish or the paddling legs of a rowing shell. The cell doesn't spin its flagellum; it *becomes* the tread.

The concrete test: reconstitute a GUV with Kai proteins tethered to the inner leaflet, tagged with RGD adhesion peptides whose exposure depends on phosphorylation state. Place the vesicle on a fibronectin-coated strip. Watch under TIRF microscopy. Predict: the vesicle rolls with a velocity locked to the phosphorylation period. Wild-type KaiC is too slow (~24 h), so engineer a faster oscillator — the MinDE system from *E. coli* oscillates pole-to-pole in minutes and can be re-circularized on a vesicle cortex. Or mutate KaiC's ATPase rate to push the period into seconds. The rolling velocity must scale with the clock period, and the adhesion wave must be visible as a traveling band of fluorescent RGD-integrin engagement.

## The 5 Gold Terms

**Phase-Locked Adhesion** — The cell grips the substrate only when the clock's phosphorylation wave is in the correct phase at that angular position; grip and release are clock-driven, not stochastic.

**The Ground Pawl** — The substrate acts as the stationary ratchet tooth; without surface contact, the clock's phase wave produces no net torque — a wheel needs a road.

**Metachronal Tread** — A traveling wave of adhesion sites around the cell circumference, like cilia beating in sequence; the membrane becomes the tread of the wheel, the clock the hub.

**Torque Gating** — The clock does not supply energy; it gates the engagement of a separate motor (ion-gradient-driven stator proteins), delivering torque in discrete pulses locked to the phase.

**The Capstan Circuit** — The full loop: clock phase wave → adhesion recruitment → surface grip → torque transduction → phase advance → release — the cell hauls itself forward by dropping and lifting anchors in sequence.

## The Math

No new math is required — but the right math must be named. The system is a phase oscillator coupled to a mechanical contact patch. The minimal model: let φ(θ, t) be the clock phase at angular position θ on the cell perimeter, obeying ∂φ/∂t = ω + D ∂²φ/∂θ² (a reaction-diffusion wave). Adhesion strength A(θ) = A_max · f(φ(θ)), where f is a gating function (e.g., a Hill function of phosphorylation state). The rolling velocity v = R · Ω, where Ω is the angular velocity of the cell body. The condition for rolling without slipping: the adhesion wave must travel at the same angular speed as the cell surface — i.e., the phase wave velocity v_φ = ω/k must match R·Ω. If v_φ > R·Ω, the cell slips (adhesion wave outruns the surface). If v_φ < R·Ω, the cell stalls (grip fails to keep up). The key dimensionless number is the **locking ratio** Λ = v_φ / (R·Ω). Rolling is stable when Λ = 1. The clock's frequency ω sets the cadence; the motor (ion gradient or ATP hydrolysis) sets the torque magnitude. The math is not new — it is the synchronization condition of a forced oscillator — but naming Λ as the control parameter makes the test quantitative: measure Λ by tracking both the adhesion wave (TIRF) and the vesicle's angular velocity (particle tracking), and tune ω until Λ = 1.

## The Polyformalism

This mechanism is substrate-agnostic. Three manifestations:

**Bacterial rolling.** *E. coli* with a MinDE oscillator engineered to gate CheY-P pulses that bias flagellar motor direction. The flagella are not the wheel — the cell body rolls on a surface using type IV pili as the adhesion tread. The MinDE wave travels around the cell cortex, activating PilT retraction in sequence. Result: a bacterium that rolls, not swims, with a period set by the MinDE clock (minutes, not hours). Test: track single cells on a glass slide under weak shear; measure stepwise angular displacements locked to the MinDE period.

**Synthetic vesicle.** The GUV system described above: KaiC (or MinDE) tethered to the inner leaflet, RGD peptides on the outer leaflet, phosphorylation-dependent exposure. The vesicle rolls on a fibronectin-coated surface. The clock is the hub, the membrane is the tread, the substrate is the pawl. Test: vary ATP concentration to change ω; measure rolling velocity. Predict v ∝ ω when Λ = 1.

**Eukaryotic cell migration.** Dictyostelium or neutrophils use actin waves that travel around the cell cortex during migration. These waves are metachronal adhesion treads already — the missing piece is recognizing them as phase-locked clocks. The actin wave is the clock; integrin engagement is the pawl. The cell is not crawling; it is rolling its cortex like a tank tread. Test: use FRET-based biosensors for Rac/Rho activity to map the phase wave, and TIRF to map adhesion; measure the locking ratio Λ. If Λ ≈ 1 during persistent migration, the model holds.

## The Cowboy's Maxim

A wheel ain't a wheel 'til it finds a road — the ground is the pawl, the clock is the hub, and the cell rolls when the grip and the phase ride together.

---

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the wheel — a cell that is also a circular mover |
| Mode | fallback_generative (3 rounds × 6 voices) |
| Rounds | 3 |
| Synthesis | deepseek (6394 chars) |
| Total time | 256.0s |
| Timestamp | 2026-09-09T04:37:33.068266Z |

### Per-round gold
- Round 1: DeepSeek (2121 chars, 60.4s)
- Round 2: CF-QwenCoder (2742 chars, 60.4s)
- Round 3: ZAI-air (6530 chars, 60.4s)
