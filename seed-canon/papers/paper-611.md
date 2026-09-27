# the zinc — a cell that is a metal that corrodes instead of the propeller, and is replaced every year

## The Frontier

Out past the harbor mouth, where the brine gets its teeth and the water turns a deeper, hungrier green, every propeller is a promise waiting to be broken. The zinc is the lie we tell the sea—a lump of soft metal bolted to the shaft, dying so the bronze can live. But the frontier isn’t the metal. The frontier is the *information* hiding in that sacrificial death. For a century, we’ve treated the zinc as a consumable: weigh it, replace it, curse it when it’s gone too fast. We’ve been reading the obituary instead of the pulse.

The real territory is the electrical and chemical conversation between your vessel and the water. Stray currents from a faulty bilge pump, a neighbor’s shore-power leak, a change in salinity after a storm, the sudden arrival of a fouling community—all of it writes itself onto the zinc’s surface in ridges, pits, and powdery white oxides. A skilled captain can read those marks like a trail of hoofprints. But reading them *after* the fact is archaeology. The cowboy canonizer’s job is to make that reading *live*—to turn the zinc from a passive victim into an active instrument, a canary that sings in volts and amps rather than in silent dissolution.

This paper canonizes the zinc as a diagnostic sensor. It introduces a new metric, a set of operational terms, and a practical protocol that turns an annual chore into a continuous health monitor for the entire vessel’s electrical and environmental systems.

## The 5 Gold Terms

1. **Zinc Corrosion Index (ZCI)** — A daily scalar value (in milliwatt-hours per day per square centimeter of zinc surface) computed from the voltage drop across the zinc-to-bonded-metal circuit and the current flowing through it, normalized by exposure time. A stable ZCI indicates electrochemical equilibrium; a wandering ZCI indicates a perturbation.

2. **Sacrificial Telemetry** — The practice of wiring the zinc as a live sensor (via a low-impedance shunt and a data logger) rather than treating it as a disposable block. This converts the annual replacement event into a continuous stream of diagnostic data.

3. **Canary Drift** — The rate of change of the ZCI over a rolling 72-hour window. A Canary Drift above 15% signals a transient electrical fault, water chemistry shift, or galvanic coupling anomaly that demands investigation before hull damage occurs.

4. **Stray Current Signature** — A distinctive pattern in the ZCI trace (a square-wave jump followed by a slow decay) that identifies a specific onboard device (e.g., a refrigeration compressor, a battery charger) as the source of an electrical leak. Each device leaves a fingerprint.

5. **Hull Equilibrium Threshold (HET)** — The ZCI range (typically 8–12 mWh/day/cm² for a bronze propeller in temperate seawater) within which the boat is electrochemically stable. Values above HET indicate over-protection (wasted zinc, possible hydrogen embrittlement of high-strength steel); values below HET indicate under-protection (propeller corrosion).

## The Math

No new math is required—but the *application* of existing electrical law is the entire game. The ZCI is computed from Ohm’s law and Faraday’s law of electrolysis, combined into a single operational number. Let V(t) be the potential difference (in volts) between the zinc and the bonded metal (propeller shaft, rudder, through-hulls), measured daily at the same time and water temperature. Let I(t) be the current (in amperes) flowing through the zinc, measured via a 0.001-ohm shunt in series with the bonding wire. The instantaneous power dissipation is P(t) = V(t) × I(t), in watts. Over a 24-hour logging period, integrate P(t) to get energy E (in watt-hours). Normalize by the zinc’s exposed surface area A (in cm²) and divide by the number of days D in the logging window to get the ZCI: ZCI = (E / A) / D, expressed in mWh/day/cm². For a typical 1-inch-diameter, 6-inch-long pencil zinc, A ≈ 48 cm². At a healthy 10 mWh/day/cm², that’s 480 mWh/day—a trivial energy draw, but a rich signal. The Canary Drift is simply the percent change in the 72-hour moving average of ZCI: Drift = |(ZCI_avg_today − ZCI_avg_3days_ago) / ZCI_avg_3days_ago| × 100%. A drift above 15% triggers an alarm. The math is not new; the *discipline* of daily measurement and the *thresholding* of drift are the innovations.

## The Polyformalism

The zinc’s story is written in three substrates simultaneously, and the cowboy canonizer reads all three at once. **Substrate One: Electrochemical.** The zinc dissolves according to Faraday’s law—mass loss is proportional to charge passed. This is the classic galvanic corrosion model, but the ZCI reframes it: instead of weighing the dead block, we measure the *live* charge flow. The voltage trace tells us the driving force; the current trace tells us the reaction rate. Together, they reveal whether the corrosion is galvanic (between dissimilar metals on the boat), electrolytic (from an external stray current source), or purely chemical (from aggressive water chemistry). **Substrate Two: Physical/Morphological.** The zinc’s surface texture is a geological record. Smooth, uniform erosion indicates healthy galvanic action. Deep pitting with white zinc hydroxide crusts suggests over-protection or chloride-rich water. A black, powdery surface with a sulfurous smell indicates sulfate-reducing bacteria—a biological substrate. The physical form of the corrosion is a second data channel, cross-referenced with the ZCI trace to confirm or refute the electrical diagnosis. **Substrate Three: Temporal/Operational.** The *timing* of ZCI fluctuations correlates with vessel activity. A spike at 0600 when the refrigerator kicks on, a dip at 1400 when the neighbor’s shore-power charger cycles, a slow climb after a freshwater rainstorm dilutes the harbor—these temporal patterns are the third substrate. The crew’s logbook becomes part of the formalism: when did you run the generator? When did the tide turn? By overlaying the ZCI trace with the operational timeline, the crew can assign causality. A single zinc, monitored across all three substrates, becomes a tri-axial sensor: electrical, chemical, and operational. The formalism is not in the metal alone, but in the *intersection* of the three readings. A stable ZCI with a pitted surface means one thing; a stable ZCI with a smooth surface means another. The cowboy canonizer teaches the crew to triangulate.

## The Cowboy's Maxim

Ride the zinc like a good horse—read its sweat, not just its bones, or she’ll throw you on the reef.

---

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the zinc — a cell that is a metal that corrodes instead of the propeller, and is replaced every year |
| Rounds | 3 |
| Total time | 80.1s |
| Synthesis | deepseek (6532 chars) |
| Timestamp | 2026-09-08T05:15:13.758251Z |

### Per-round gold
- Round 1: DeepSeek (1995 chars, 18.2s)
- Round 2: Mistral (2845 chars, 22.1s)
- Round 3: Mistral (2886 chars, 24.4s)
