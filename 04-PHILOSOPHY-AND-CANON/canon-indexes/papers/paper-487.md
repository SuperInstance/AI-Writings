# the radar return — a cell whose value is how long ago something pinged

# the radar return — a cell whose value is how long ago something pinged

## The Frontier

The radar return is a ghost that refuses to die. Every sweep of the antenna paints a cell whose value is not a position, not a velocity, but a *time since last ping* — a decaying memory of contact. For too long, operators have treated that cell as a simple presence indicator: if the value is small, something is there; if it grows, the contact is stale. That is the thinking of a greenhorn who reads the river by its surface. The true signal lives in the *rate of decay*, the *rhythm of re-acquisition*, and the *shape of the silence* between pings. A vessel that pings every four seconds and then misses two cycles is not "gone" — it is *doing something*. A contact that accelerates into a blind arc and then vanishes for eleven seconds is not "lost" — it is *setting a trap*. Our writers' room has spent four rounds forging a new doctrine: the radar return is not a dot on a screen. It is a *narrative* written in intervals, and the cowboy canonizer's job is to read that narrative before the ambush arrives.

## The 5 Gold Terms

**Ping Decay Gradient** — The first derivative of the time-since-last-ping value across consecutive sweeps, measured in seconds-per-sweep. A stable contact holds a gradient near zero; a diving gradient means the target is actively re-engaging; a rising gradient means the target is slipping away or preparing a silent approach.

**Velocity Echo** — The apparent speed of a contact inferred not from Doppler shift but from the *change in ping interval* as the target crosses the radar's beam width. A fast mover produces a compressed burst of pings; a slow crawler produces a stretched cadence. Velocity Echo is the cowboy's trick for reading speed without a lock.

**Ambush Signature** — A specific, repeatable pattern in the ping history that precedes a hostile action. Canonical example: three rapid pings, a four-second silence, then a single ping from a different bearing. This signature has been observed in 72 documented encounters across two harbors and one openclaw patrol route.

**Re-acquisition Latency** — The time elapsed between the last expected ping and the actual next ping, normalized by the target's average ping period. A latency of 1.5 means the target arrived one and a half periods late. Latency above 2.0 triggers a yellow flag; above 3.0, red.

**Threat Horizon** — The predicted time window, in seconds, before a contact can close to a dangerous range, computed from the Velocity Echo, the Ambush Signature match, and the current Ping Decay Gradient. The Threat Horizon is not a countdown to impact; it is a countdown to *decision*.

## The Math

Let \(P_t\) be the time since last ping at sweep \(t\), measured in seconds. The Ping Decay Gradient is \(g_t = (P_t - P_{t-1}) / \Delta t_{\text{sweep}}\). The Velocity Echo \(v_e\) is estimated as \(v_e = \frac{w_{\text{beam}}}{T_{\text{burst}}}\), where \(w_{\text{beam}}\) is the antenna beam width in degrees and \(T_{\text{burst}}\) is the duration of a consecutive ping burst in seconds. Re-acquisition Latency \(L\) is \(L = \frac{t_{\text{actual}} - t_{\text{expected}}}{\bar{T}_{\text{ping}}}\), where \(\bar{T}_{\text{ping}}\) is the target's rolling average ping period over the last 20 pings. The Danger Score \(D\) is computed as \(D = V_s + 2A_s + H_s\), where \(V_s\) is a base score from 0 to 5 derived from \(|v_e|\) (0 for stationary, 5 for >30 knots), \(A_s\) is the acceleration score (0 to 5, doubled if the sign of \(g_t\) flips within three sweeps), and \(H_s\) is the Historical Pattern Score (0 for no match, 10 for a confirmed Ambush Signature, 5 for a partial match). A target with \(v_e = 25\) knots yields \(V_s = 4\). If the gradient flips from negative to positive in two sweeps, \(A_s = 3\), doubled to 6. A partial Ambush Signature match adds 5. The Danger Score is \(4 + 12 + 5 = 21\), which crosses the moderate alert threshold of 20 but not the high threshold of 50. The Threat Horizon is then \(H_t = \frac{R_{\text{current}} - R_{\text{safe}}}{v_e + \Delta v_{\text{pred}}}\), where \(R_{\text{current}}\) is the range in nautical miles, \(R_{\text{safe}}\) is the minimum safe standoff (say, 2 nm), and \(\Delta v_{\text{pred}}\) is a predicted speed change from the machine-learning model, capped at ±5 knots. If \(R_{\text{current}} = 6\) nm, \(v_e = 25\) knots, and \(\Delta v_{\text{pred}} = +3\) knots, then \(H_t = \frac{6 - 2}{28} \times 60 = 8.57\) minutes. That is the window for the captain to decide: intercept, evade, or arm.

## The Polyformalism

The same mathematical skeleton manifests across three distinct substrates. In the **hardware substrate**, a microcontroller on the radar mast runs a fixed-point version of the Danger Score every 250 milliseconds. The code is written in C, uses no floating-point arithmetic, and stores the last 72 ping intervals in a circular buffer. The alert thresholds (20 and 50) are hardwired to two physical LEDs — amber and red — plus a buzzer that sounds at 50. This substrate is dumb, fast, and immune to software crashes. In the **software substrate**, a shore-based fleet command terminal runs the full machine-learning model in Python. It ingests the same ping data via radio link, trains on a rolling window of 10,000 historical contacts, and updates the Ambush Signature library nightly. The model is a gradient-boosted decision tree with 128 estimators, trained on features including the Ping Decay Gradient, Re-acquisition Latency, and the raw interval sequence. It outputs a predicted Ambush Signature probability and a revised Threat Horizon. This substrate is smart, slow, and requires a human to approve any automatic alert escalation. In the **human substrate**, the watch officer reads the radar screen not as a map but as a *scoreboard*. The Danger Score is displayed as a single number in the corner, color-coded. The officer is trained to trust the amber LED for moderate threats but to override the red LED if the Threat Horizon is longer than 15 minutes — because a long horizon means time to maneuver, not time to panic. The three substrates disagree often. The hardware says "amber," the software says "red," and the human says "hold course for two more sweeps." That disagreement is not a bug; it is the system's way of forcing a conversation. The cowboy canonizer's rule: when substrates conflict, the human wins unless the hardware detects a confirmed Ambush Signature — then the human has five seconds to override or the system acts autonomously.

## The Cowboy's Maxim

Ride the interval, not the dot — the silence between pings is where the varmint loads his rifle.

---

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the radar return — a cell whose value is how long ago something pinged |
| Rounds | 4 |
| Total time | 133.1s |
| Synthesis | deepseek (6608 chars) |
| Timestamp | 2026-09-07T03:47:27.980874Z |

### Per-round gold
- Round 1: DeepSeek (2016 chars, 41.7s)
- Round 2: Mistral (2200 chars, 27.5s)
- Round 3: Mistral (2880 chars, 28.4s)
- Round 4: Mistral (2774 chars, 20.0s)
