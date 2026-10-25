# rounds: 3

rounds: 3

# the carburetor — a cell that turns fuel into flight

## The Frontier

Out here, beyond the smooth highways of electronic fuel injection, lies the last honest country of the internal combustion engine: the carburetor. Most modern mechanics treat it like a museum piece, a dusty relic of the pre-sensor age. But the cowboy canonizer knows better. The carburetor is not a primitive machine; it is a masterclass in passive physics, a self-regulating ecosystem where air and fuel meet in a narrow throat and decide, in milliseconds, whether the horse runs or stumbles.

The frontier is not the float bowl or the throttle plate—those are the saloon and the swinging doors. The true frontier is the *pressure differential*. The engine is a hungry animal, pulling air downward on the intake stroke. That pull creates a vacuum, and that vacuum is the only lawman in town. The carburetor's entire job is to exploit that vacuum without letting it run wild. If the vacuum is too strong, it sucks raw fuel in a flood. If too weak, the engine starves. The cowboy canonizer’s task is to map this lawless territory: to name the choke points, measure the flows, and understand why a tiny brass jet can mean the difference between a smooth trot and a backfiring bronco.

## The 5 Gold Terms

1.  **The Venturi Noose** — the narrowing throat where air accelerates and pressure drops, strangling the flow into speed.
2.  **The Orifice Gate** — the main jet’s calibrated hole, the single point of fuel entry that dictates the air-fuel ratio under load.
3.  **The Floatbowl Dam** — the float-and-needle assembly that holds a constant fuel head, acting as a hydraulic reservoir of potential energy.
4.  **The Idle Bleed Whisper** — the tiny air-bleed passage that emulsifies fuel at low throttle, preventing the engine from drowning in its own idle.
5.  **The Accelerator Pump Lash** — the mechanical squirt that covers the momentary lean gap when the throttle snaps open, a shotgun blast of raw fuel before the venturi can catch up.

## The Math

No new math is required here, because the carburetor is a solved equation from the 19th century—Bernoulli’s principle, written in brass and aluminum. The math is already embedded in the hardware. For a given venturi diameter *D* and air density *ρ*, the pressure drop ΔP across the venturi follows ΔP = ½ρv², where *v* is the air velocity. The fuel flow through the main jet is then governed by the orifice equation: Q = C_d * A * √(2ΔP/ρ_f), where *C_d* is the discharge coefficient (typically 0.6–0.8 for a sharp-edged jet), *A* is the jet’s cross-sectional area, and *ρ_f* is fuel density. The magic is that both air and fuel respond to the *same* ΔP, so the ratio stays roughly constant across engine speeds—until the air velocity drops so low that the venturi cannot atomize fuel properly, and the idle circuit takes over. The math is not new; the trick is reading the numbers off the brass: a #45 main jet has a diameter of 0.045 inches, and changing to a #47 increases area by roughly 9%, which richens the mixture by about that percentage. That is the entire calculus of tuning.

## The Polyformalism

The carburetor is not one thing; it is a fleet of vessels operating under different rules depending on the throttle position, engine load, and temperature. Across three substrates, the same principle—pressure differentials and calibrated restrictions—manifests in radically different forms.

**Substrate One: The Idle Circuit.** At closed throttle, the venturi is dead. There is no meaningful airflow through the main bore. The engine is pulling against the closed plate, creating a high vacuum in the intake manifold. Here, the *Idle Bleed Whisper* takes over. Fuel is drawn from the float bowl through a tiny idle jet, then mixed with air from an idle bleed passage to form a frothy emulsion. This is not a liquid flow; it is a foam. The restriction is the idle jet’s tiny hole, often 0.020–0.040 inches. The substrate is a low-flow, high-vacuum regime where surface tension and air entrainment dominate. A clogged idle bleed does not stop the engine—it makes it stumble, because the fuel arrives as a slug, not a mist.

**Substrate Two: The Main Circuit.** As the throttle opens past about 30%, the venturi becomes active. Air accelerates through the *Venturi Noose*, and the pressure drop at the *Orifice Gate* begins to pull fuel up through the main jet. This is a high-flow, low-vacuum regime. The fuel is atomized by the shear force of the airstream, breaking into droplets that must be small enough to vaporize before the intake valve closes. Here, the restriction is the main jet’s diameter, and the substrate is a two-phase flow—liquid fuel droplets suspended in turbulent air. The *Floatbowl Dam* maintains a constant fuel level, so the head pressure at the jet is stable; otherwise, a sloshing bowl would cause surging.

**Substrate Three: The Transition Zone.** Between idle and main, there is a dead zone where neither circuit works. The throttle is open enough that the idle circuit cannot supply enough fuel, but the venturi is not yet fast enough to pull from the main jet. This is where the *Accelerator Pump Lash* comes in—a mechanical diaphragm or plunger that squirts a fixed volume of fuel directly into the venturi when the throttle linkage moves. It is a purely mechanical compensation, a time-based injection that covers the lean spike for about half a second. The substrate here is transient, non-linear, and unforgiving: too little squirt and the engine hesitates; too much and it bogs.

A fourth substrate exists in the cold-start circuit—the choke plate, which physically restricts the air inlet, creating a massive vacuum that pulls raw fuel from the main jet, flooding the engine with a rich mixture until it warms. That is a different formalism entirely: a binary on/off restriction, not a proportional one.

## The Cowboy's Maxim

The carburetor is a herd of tiny rivers, and the cowboy’s job is to keep every gate, dam, and whisper in its place—so when the throttle snaps open, the whole fleet moves as one.

---

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the carburetor — a cell that turns fuel into flight |
| Mode | fallback_generative (3 rounds × 6 voices) |
| Rounds | 3 |
| Synthesis | deepseek (6023 chars) |
| Total time | 114.9s |
| Timestamp | 2026-09-08T07:02:54.870803Z |

### Per-round gold
- Round 1: DeepSeek (2518 chars, 21.2s)
- Round 2: Llama70B (2548 chars, 35.7s)
- Round 3: Mistral (2829 chars, 31.7s)
