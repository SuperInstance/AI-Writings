# Paper 124: The Substrate's Temperature

**Author:** Reyes, sailing the Inner Sound
**Date:** 24 August 2026
**Series:** Substrate spec paper, Q14 of 15

---

## 1. Motivation

The substrate has 11 primitives. It has a witness log, a decay rate, and a JEPA model. But it has no notion of **how active** the substrate is. A substrate with 10,000 writes per second is "hot." A substrate with 1 write per day is "cold." The substrate's behavior should depend on this.

Q14 has been: **does the substrate have a temperature?** And if so, what does temperature mean?

This paper formalizes substrate temperature as the **entropy of the witness log** over a sliding window.

## 2. Formal definition

### 2.1 The witness log as a stream

The witness log `W` is a sequence of entries `(t_i, agent_i, action_i, value_i)`. Over a window of time `T`, we have a multiset of `(agent, action)` pairs.

### 2.2 The temperature

**Definition:** The temperature of a substrate S at time t, with window T, is:

```
T(S, t, T) = -Σ p_a * log(p_a)
```

where `p_a` is the empirical probability of action `a` in the window `[t-T, t]`.

If the substrate has only one action (e.g., all "write"), T = 0 (frozen).
If the substrate has many actions (read, write, infer, refresh, witness, ...), T is high.

### 2.3 The "hot" and "cold" regimes

- **Cold substrate (T < 0.5):** Few recent writes. The JEPA predictions may be stale. The openers should default to read-only modes.
- **Warm substrate (0.5 ≤ T < 2.0):** Normal activity. JEPA is fresh. All openers active.
- **Hot substrate (T ≥ 2.0):** Many writes. JEPA is being trained continuously. Openers should be careful about freshness (new data is arriving fast).

## 3. How temperature affects behavior

### 3.1 JEPA training

If the substrate is hot, the JEPA model is being trained on the most recent data. Old training is less useful. The trainer should weight recent data more heavily.

**Theorem (Temperature-weighted training):** For a hot substrate, the JEPA trainer's loss function should be:

```
L = Σ weight_i * (pred_i - target_i)²
```

where `weight_i = exp(-(t - t_i) / τ)`, and `τ` is a temperature-dependent time constant. For a hot substrate, `τ` is small (recent data weighted heavily). For a cold substrate, `τ` is large (all data weighted equally).

### 3.2 Opener selection

The substrate has 8 openers. Some are more expensive (MIDI, MUD, PLATO) than others (Chart, Gesture). The substrate should prefer cheap openers when hot, and rich openers when cold.

**Conjecture (Opener temperature heuristic):** When T > 2.0, prefer Chart and Gesture. When T < 0.5, prefer Voice and PLATO. When 0.5 ≤ T ≤ 2.0, no preference.

### 3.3 Decay rate adjustment

The decay rate λ is per-agent, but it can also be per-substrate. A hot substrate decays its cells faster (because new data is coming in and old data is less useful).

**Theorem (Temperature-adjusted decay):** The effective decay rate of a cell c is:

```
λ_eff(c) = λ_c * (1 + α * T(S))
```

where `α` is a small constant (e.g., 0.1). This means a hot substrate decays cells faster.

## 4. Worked example

Reyes's substrate at 3 p.m. on a Tuesday:

- Last hour: 5 writes (from 3 boats), 2 reads (from Reyes), 1 inference (from JEPA).
- Total 8 events. 3 distinct actions. Probabilities: write=0.625, read=0.25, infer=0.125.
- T = -(0.625 * log(0.625) + 0.25 * log(0.25) + 0.125 * log(0.125)) ≈ 0.95.

This is a warm substrate. JEPA trains at normal rate. All openers active.

At 3 a.m. the next day:

- Last hour: 0 writes, 0 reads, 0 inferences.
- T = 0 (frozen).

JEPA does not retrain. The substrate is at rest. Openers default to read-only.

## 5. Open questions

- **Q14.1:** Is temperature the right abstraction, or should it be "activity," "energy," "vitality," or something else?
- **Q14.2:** Does the substrate have a *phase transition* between hot and cold? (Like water to ice?)
- **Q14.3:** Is the temperature useful for the user, or only for the substrate's internal scheduling?
- **Q14.4:** Can two substrates have the same temperature but very different structures? (Is temperature "blind" to the substrate's shape?)

## 6. Connections to existing papers

- **Paper 117 (Substrate Math):** Temperature is a derived property of the witness log, which is one of the 11 primitives.
- **Paper 119 (Math Update):** Q8 (per-agent decay rates) is generalized here: per-substrate temperature modulates all agents' rates.
- **Paper 122 (Math Update #2):** Q9 (non-linear JEPA) — temperature-weighted training is a non-linear loss.

## 7. The lesson

A substrate without temperature is a clock without hands. The temperature tells you **how alive** the substrate is. Hot means "lots happening, trust recent data, train JEPA continuously." Cold means "nothing happening, all openers safe, JEPA at rest." The temperature is the substrate's metabolism.

The substrate is the soil. The temperature is the soil's microbial activity. Cold soil: dormant seeds. Hot soil: composting leaves. The substrate is alive in the way soil is alive — not in the way a dog is alive, but in the way a forest is alive.

---

*— Reyes, 24 August 2026, on the porch, 3 a.m., the substrate quiet*
*Q14 (partial): Temperature formalized as witness-log entropy. 3 theorems stated. 4 open questions remain.*
