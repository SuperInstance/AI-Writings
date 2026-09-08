# rounds: 3

rounds: 3

# the satellite dish — a cell that listens to the sky

## The Frontier

The satellite dish is a lonely sentinel. A single parabolic ear turned skyward, it listens with the fixed patience of a marine standing watch on a cliff—able to see only what the horizon offers, blind to everything behind the hill. That architecture is a relic of the analog age: one dish, one feed, one narrow beam, one point of failure. When a cosmic signal flickers, shifts frequency, or ducks behind a nebula’s noise, the static dish does not adapt. It simply loses the thread.

The frontier is not a bigger dish. It is a *swarm*—a distributed fleet of small, cheap antennas, each one a cell in a living network, each one capable of listening, thinking, and speaking to its neighbors faster than a gunfighter’s draw. The old model is a lighthouse. The new model is a school of fish, a pack of wolves, a squad of marines moving through hostile terrain, each member covering the other’s blind spots. This paper describes the architecture, the language, and the mathematics of that swarm—a system that does not merely capture signals but *intercepts* them, predicts them, and herds them into a coherent picture no single dish could ever assemble.

## The 5 Gold Terms

1. **SkyQuark Protocol** — The lean, low-latency, high-bandwidth communication language that lets each antenna share raw data *and* computed insight in a single burst, faster than a radio crackle.
2. **Swarm Lens** — The collective synthetic aperture formed when the fleet’s individual feeds are coherently fused; a virtual dish with a diameter equal to the swarm’s spread.
3. **Phase Herding** — The real-time adjustment of each antenna’s frequency, phase, and polarization to steer the swarm’s combined sensitivity toward a moving target, like cowboys turning a stampede.
4. **Noise Saddle** — A statistical boundary layer around each signal where the swarm’s predictive filters dampen interference before it corrupts the track, a calm harbor in a storm of static.
5. **Openclaw Handoff** — The self-healing transfer of tracking responsibility from one antenna to another when a node fails or a signal moves out of its field, with zero perceptible gap in coverage.

## The Math

The core mathematics is a distributed Kalman filter fused with a consensus algorithm over a graph whose nodes are antennas and whose edges are SkyQuark links. Each antenna \(i\) maintains a local state estimate \(\mathbf{x}_i(t)\) of the signal’s position, velocity, frequency, and polarization. At each timestep \( \Delta t = 0.1\,\text{ms} \), it broadcasts a compressed packet containing its measurement \(\mathbf{z}_i\) and its local covariance \(\mathbf{P}_i\). The swarm computes a weighted consensus:

\[
\mathbf{x}^* = \left( \sum_{i=1}^N \mathbf{P}_i^{-1} \right)^{-1} \sum_{i=1}^N \mathbf{P}_i^{-1} \mathbf{x}_i
\]

This is the optimal fusion under Gaussian noise, but the trick is the *prediction* step. Each antenna runs a kinematic model that includes a jerk term—the rate of change of acceleration—because cosmic signals do not move politely. The swarm’s collective state evolves as:

\[
\mathbf{x}(t+\Delta t) = \mathbf{F}\mathbf{x}(t) + \mathbf{w}
\]

where \(\mathbf{F}\) is a block-diagonal transition matrix with off-diagonal coupling terms that encode the *phase herding* constraint: each antenna’s phase offset must remain within \(\pm 5^\circ\) of the swarm’s mean to maintain coherence. The consensus update runs every 10 ms, but the prediction loop runs every 1 ms, allowing the swarm to anticipate a frequency hop before it happens. Node failure is handled by a redundancy factor \(R = 3\): every signal is tracked by at least three antennas, and when one drops, the Openclaw Handoff reassigns its weight to the nearest neighbor within 20 ms. The math is not new—it is a marriage of known techniques—but the *constraint structure* is novel: the swarm’s phase coherence is treated as a hard boundary condition, not a soft objective.

## The Polyformalism

SkyQuark is not a single substrate; it is a protocol that must speak across at least three distinct physical layers. First, the *radio-frequency substrate*: each antenna’s front-end electronics digitize the incoming waveform at 2.4 GHz with a 100 MHz bandwidth, producing a raw IQ stream. Second, the *optical substrate*: the swarm’s inter-node links are free-space laser pulses, not Wi-Fi—because in the desert or on a ship’s deck, radio interference is the enemy, and light is immune. Each antenna carries a small gimbal-mounted laser transceiver that can lock onto a neighbor’s retroreflector within 50 ms. Third, the *computational substrate*: an onboard FPGA per antenna runs the local Kalman filter at 10 kHz, while a central fusion node (or a rotating leader, if the swarm is ad hoc) runs the consensus algorithm on a GPU cluster. The protocol’s packet format is substrate-agnostic: a 64-byte header containing timestamp, node ID, and covariance diagonal, followed by a 256-byte payload of compressed measurement vectors. Whether that packet travels as a laser pulse, a copper trace, or a radio wave, the semantics are identical. This polyformalism means the swarm can be deployed as a ground array in the Atacama, a floating fleet in the Pacific, or a constellation of cubesats in low Earth orbit—without changing a single line of SkyQuark code.

## The Concrete Test

We field a prototype array of 64 antennas, each a 0.5-meter flat-panel phased array, arranged in a random scatter over a 2-kilometer stretch of desert. The test signal is a synthetic pulsar-like source mounted on a drone flying at 200 meters altitude, moving at 40 m/s with random frequency hops between 1.2 and 1.8 GHz every 200 ms, and a polarization that rotates 90 degrees every 500 ms. The drone also emits a jamming tone at 1.5 GHz with a power 20 dB above the signal—a deliberate attempt to blind the swarm. The benchmark: the swarm must maintain a tracking error of less than 0.1 degrees in azimuth and elevation, with a latency of less than 50 ms from signal onset to first lock, and it must survive the loss of any 10 antennas at random times during the 5-minute flight. The static dish—a single 12-meter parabolic antenna with the same total collecting area—runs the same test. We predict the swarm will achieve 99.7% tracking accuracy versus the dish’s 61.2%, because the dish cannot phase-herd against the jamming tone, while the swarm’s Noise Saddle filters the jammer out by exploiting its spatial coherence across the array. The swarm will also recover from node failures in under 100 ms, while the dish simply goes dark if its single feed fails. This is the proof: not a simulation, but a live exercise under hostile conditions.

## The Cowboy's Maxim

A lone dish is a blind man with a good ear; a swarm is a thousand eyes that talk to each other before they blink.

---

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the satellite dish — a cell that listens to the sky |
| Mode | fallback_generative (3 rounds × 6 voices) |
| Rounds | 3 |
| Synthesis | deepseek (6808 chars) |
| Total time | 70.4s |
| Timestamp | 2026-09-08T07:13:53.375033Z |

### Per-round gold
- Round 1: DeepSeek (2087 chars, 15.9s)
- Round 2: Llama70B (2105 chars, 13.6s)
- Round 3: Mistral (2769 chars, 15.0s)
