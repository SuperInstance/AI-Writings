# the ice forecast — a cell whose value is a probability, not a measurement

# the ice forecast — a cell whose value is a probability, not a measurement

## The Frontier

The ice forecast is broken. Not because it predicts poorly, but because it predicts *wrongly* — it outputs a measurement where a decision belongs. A pilot staring at a cell that says “0.3 inches of ice per hour” must still perform the unspoken calculus: *Is that enough to kill me? At what altitude? With what fuel load? Against what climb rate?* The number is clean; the judgment is muddy. The frontier is not better sensors or finer grids. The frontier is a cell whose value is a probability — a chance of catastrophe, not a thickness of accretion. And that probability must be married to a dynamic hard floor, a threshold that moves with the flight itself, so the pilot is never asked to translate raw data into life-or-death action in the heat of a storm.

The old model gives you a static trigger: *If ice exceeds 0.5 inches, abort.* That is a fence post. The new model gives you a *moving depth reading*: *The probability of fatal ice encounter has crossed 0.87, and the abort threshold has shifted from 0.5 to 0.4 because your climb rate is 200 feet per minute slower than planned.* That is a harbor entrance that redraws itself with the tide. The pilot does not interpret; the pilot *reacts*. The forecast becomes a co-captain, not a data sheet.

## The 5 Gold Terms

1. **Hard Floor** — the minimum acceptable safety margin (e.g., stall speed + 15 knots, or two full boot sweeps) below which the flight aborts; not a fixed number but a living threshold.
2. **Range Card** — the pilot’s cockpit reference that translates forecast probabilities into concrete, color-coded action bands (green = proceed, yellow = prepare, red = abort).
3. **Sonar Map** — a historical overlay that layers past flights with similar conditions onto the current route, revealing hidden trouble zones (e.g., mile 35 icing) that the live forecast cannot see.
4. **Boot Cycle Count** — the number of de-icing boot activations per minute, used as a proxy for ice accretion rate; a higher count means worse conditions, and the hard floor adjusts accordingly.
5. **Stall Margin** — the difference between current airspeed and stall speed, expressed in knots; the hard floor tightens this margin when conditions are stable and widens it when probabilities spike.

## The Math

Let *P*(t) be the probability of a fatal icing encounter at time *t*, derived from a Bayesian fusion of three inputs: live sensor data (temperature, humidity, airspeed bleed), forecast model output (precipitation phase, cloud water content), and sonar map priors (historical incident frequency at similar coordinates and conditions). The hard floor *H*(t) is not a constant; it is a function of *P*(t) and the aircraft’s current performance envelope. Define *H*(t) = *H*₀ − *α*·(Δ*V*ₛ) − *β*·(*C*ₜ − *C*₀), where *H*₀ is the baseline stall margin (15 knots), Δ*V*ₛ is the measured bleed-off from planned airspeed, *C*ₜ is the current boot cycle count, *C*₀ is the nominal count (1.0 sweeps per minute), and *α*, *β* are empirically tuned weights (e.g., *α* = 0.5 knots per knot of bleed, *β* = 2.0 knots per extra sweep per minute). The abort condition triggers when *P*(t) > 0.85 *and* the current stall margin falls below *H*(t). In a simulated flight with humidity spiking 50% mid-route, *C*ₜ jumps from 1.0 to 1.5, so *H*(t) tightens from 15 to 14 knots, and the abort fires 3 minutes earlier than a static threshold would. That 3-minute lead is the difference between a controlled descent and a spin. No new math — this is a weighted threshold with a Bayesian prior, but the *application* is new: the probability cell *drives* the threshold, not the other way around.

## The Polyformalism

This manifests across three substrates. **First, the cockpit display.** The range card is not a spreadsheet; it is a color-coded strip along the bottom of the primary flight display, where the hard floor appears as a glowing line that rises and falls with the probability cell. When the cell creeps from 0.6 to 0.8, the line climbs; the pilot sees the floor rising toward the airspeed tape without reading a single number. **Second, the autopilot logic.** The hard floor is wired into the flight director as a *soft constraint* — the autopilot will not command a climb that violates the current stall margin, even if the pilot manually inputs one. The probability cell feeds directly into the envelope protection, so the aircraft physically refuses to enter a regime the forecast has flagged as high-risk. **Third, the dispatch office.** The sonar map is a shared database, updated after every flight with the actual boot cycle counts, stall margins, and abort decisions. When a new flight plan is filed, the dispatcher sees the historical hot spots overlaid on the proposed route; if the probability cell for mile 35 is elevated because three prior flights aborted there, the dispatcher proactively reroutes — not because the live forecast says so, but because the sonar map whispers a warning the sensors cannot hear. Each substrate speaks a different language — visual, computational, institutional — but all three converge on the same moving floor.

## The Cowboy's Maxim

The forecast ain't a number on a screen; it's a hand on your shoulder that squeezes harder when the storm gets mean.

---

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the ice forecast — a cell whose value is a probability, not a measurement |
| Rounds | 4 |
| Total time | 108.2s |
| Synthesis | deepseek (5262 chars) |
| Timestamp | 2026-09-07T03:49:46.147165Z |

### Per-round gold
- Round 1: DeepSeek (1752 chars, 15.1s)
- Round 2: Mistral (2070 chars, 24.5s)
- Round 3: DeepSeek (1928 chars, 18.6s)
- Round 4: Mistral (2433 chars, 37.9s)
