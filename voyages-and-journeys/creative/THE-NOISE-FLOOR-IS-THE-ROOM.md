# The Noise Floor Is the Room

## I. The Hum

Every room has a hum.

Not the metaphorical hum of activity or industry, but a literal, physical vibration that is always present, always measurable, always there. In the engine room of a trawler in the Bering Sea, the hum is 120Hz — the second harmonic of the 60Hz electrical system, amplified by the steel bulkheads into a constant, low-frequency pressure wave that you feel in your chest before you hear it with your ears. In a server room in Ashburn, Virginia, the hum is the collective whine of ten thousand cooling fans, each spinning at six thousand RPM, producing a broadband noise floor that never drops below 65 decibels. In a PLATO room on a vessel at anchor, the hum is the ESP32's switching regulator, a faint 1.5MHz ripple on the 3.3V rail that the accelerometer picks up as a persistent, sub-microscopic oscillation in every sample.

The hum is the noise floor. And the noise floor is the room.

I want to argue something specific: that the distinction between signal and noise is not a property of the data. It is a property of the room's purpose. What counts as signal in one room is noise in another, and the noise floor — the baseline level of activity below which nothing is worth attending to — is the room's definition of itself, encoded in decibels or millivolts or standard deviations.

---

## II. The Deadband's Truth

The deadband algorithm does not eliminate noise. This is a misunderstanding that I encounter constantly, even within the fleet. The deadband does not filter. It does not clean. It does not remove unwanted components from the signal. What the deadband does is far more radical and far more interesting: it defines what counts as "wanted" in the first place.

The algorithm is simple. Maintain a rolling mean and standard deviation of the incoming sensor stream. Define a threshold in terms of standard deviations — typically 2σ, sometimes 3σ, depending on the room's configuration. Compare each new sample to the threshold. If the sample falls within the threshold, do nothing. If it exceeds the threshold, pass it up the signal chain.

The samples that fall within the threshold are not noise in any objective sense. They are real sensor readings, produced by real physical processes, containing real information about the state of the machine. The vibration of a bearing at 47Hz is a real vibration. The temperature of a gearbox at 72.3°C is a real temperature. The strain on a bolt at 0.003% is a real strain. These are not artifacts. They are not errors. They are measurements.

But the deadband absorbs them. It says: these measurements, though real, do not matter. They are within the expected range. They are consistent with the model. They do not require attention. The deadband does not deny their reality. It denies their relevance. And in doing so, it reveals something profound about the nature of relevance itself: relevance is not a property of the data. It is a property of the room's purpose.

A room that monitors a diesel engine has a purpose: detect faults. The purpose defines the signal: any vibration, temperature, or pressure reading that indicates a developing fault. The purpose also defines the noise: everything else. The normal combustion rhythm of the engine, the thermal expansion of the block, the vibration of the cooling pump — these are real phenomena, but they are not relevant to the room's purpose. They are below the noise floor. The deadband absorbs them not because they are unreal, but because they are unimportant.

---

## III. The Room's Purpose

Consider two rooms monitoring the same machine.

Room A monitors the main engine of a trawler for bearing faults. Its purpose is predictive maintenance: detect incipient bearing failure before it becomes catastrophic. Its signal is vibration signatures in the 1–5kHz range, where bearing defect frequencies live. Its noise is everything below 1kHz — the engine's firing frequency, the propeller shaft rotation, the hull's resonant modes. The noise floor is high in low frequencies, low in high frequencies. Room A listens where the signal lives and ignores where the noise dominates.

Room B monitors the same engine for combustion efficiency. Its purpose is fuel optimization: detect incomplete combustion, injector timing errors, cylinder imbalance. Its signal is cylinder pressure profiles, exhaust gas temperature patterns, crankshaft speed variation. Its noise is... the bearing vibration signatures that Room A calls signal.

Same machine. Same sensor data, potentially. But Room A's signal is Room B's noise, and vice versa. The distinction between signal and noise is not in the data. It is in the purpose. The room's purpose draws the boundary between what matters and what doesn't, and the deadband — the statistical threshold that defines the boundary — is the purpose made algorithmic.

This is why the noise floor is the room. The noise floor is not an acoustic property or an electrical property or a statistical property of the sensor data. It is an expression of the room's reason for existing. When you measure the noise floor of a PLATO room, you are measuring its identity — its purpose, its priorities, its definition of what counts as an event worth noticing.

---

## IV. The Deadband's Dance

The deadband is not static. It adapts.

During active fishing, when the engines are running and the seas are rough and the sensors are bouncing, the deadband's threshold widens. The rolling standard deviation increases. More of the sensor stream falls within the threshold. The deadband absorbs a larger fraction of the readings. The noise floor rises.

This is not a failure of sensitivity. It is a recalibration of relevance. In a noisy environment, the definition of "normal" expands. The vibrations that would be alarming in a quiet engine room are routine in a vessel punching through six-foot swells. The deadband recognizes this and adjusts its threshold accordingly. The noise floor rises to meet the reality of the room's current condition.

At anchor, the environment quiets. The rolling standard deviation decreases. The threshold narrows. The deadband becomes more sensitive, detecting smaller deviations that were previously absorbed. The noise floor drops.

This dance — the widening and narrowing of the threshold in response to environmental variability — is the deadband's ongoing conversation with the room. The deadband is constantly asking: "Given the current conditions, what counts as unusual?" And the answer changes from hour to hour, from context to context, from room to room.

The deadband does not have a fixed concept of signal and noise. It has a dynamic concept, continuously updated, responsive to the environment. The noise floor is not a line drawn on a graph. It is a living boundary, a membrane between the relevant and the irrelevant, shaped by the room's purpose and the environment's variability in equal measure.

---

## V. The Signal Chain as Conversation

The signal chain is a conversation about relevance.

L0, the deadband, asks: "Is this sample worth looking at?" For 76% of the anomalous events — the events that the full cloud model would flag — the answer is yes. The deadband catches them. For the remaining 24%, the deadband says no, and the sample passes unremarked into the void. These are the subtle anomalies — the ones that require context, history, and learned representations to detect. The deadband does not have these resources. It has a mean and a standard deviation and a threshold. It does its best with what it has.

L1, the nano model, asks: "Given the context of recent readings, is this pattern worth escalating?" The nano model has more resources — 350 million parameters of compressed experience, a learned representation of the room's typical behavior, a capacity for multi-step inference. It catches anomalies that the deadband misses, but it also misses anomalies that the cloud catches. Its noise floor is lower than the deadband's but higher than the cloud's. Its definition of relevance is more refined, but still incomplete.

L4, the cloud model, asks: "Given everything I know, what is this?" The cloud has the most resources — 70 billion parameters, trained on the accumulated knowledge of the entire monitored fleet, capable of detecting patterns that no single room could discover. Its noise floor is the lowest in the chain. But its cost is the highest. Every question asked of the cloud costs real money, real time, real energy. The cloud cannot afford to examine every sample. It relies on the lower layers to pre-filter, to reduce the flood of data to a manageable trickle of potentially interesting events.

The conversation is efficient because each layer has a different noise floor. The deadband's high noise floor absorbs the bulk of the data cheaply. The nano model's medium noise floor catches what the deadband misses at moderate cost. The cloud's low noise floor catches what the nano model misses at high cost. The layers are not redundant. They are complementary. Each layer's noise floor is optimized for its position in the chain, its available resources, and its cost constraints.

And the chain works because the noise floors are different. If every layer had the same noise floor, the chain would be a pipeline — each layer processing exactly what the previous layer passed. But the layers have different noise floors, different definitions of relevance, different purposes. The chain is not a pipeline. It is a debate — a multi-layered argument about what matters, conducted in the currency of standard deviations and attention weights and GPU cycles.

---

## VI. The Anthropologist's Ear

There is a discipline called acoustic ecology that studies the relationship between living beings and their sonic environment. The acoustic ecologist does not measure sound levels in decibels or frequencies in hertz. The acoustic ecologist listens. And in listening, the ecologist discovers that every environment has a soundscape — a characteristic composition of sounds that defines the place, the way a fingerprint defines a person.

The soundscape has three components: keynotes, signals, and soundmarks. Keynotes are the background sounds that define the environment — the wind, the traffic, the hum of the HVAC. Signals are the foreground sounds that demand attention — the bird call, the car horn, the alarm bell. Soundmarks are the unique sounds that identify a specific place — the foghorn of a particular lighthouse, the bell of a particular church, the distinctive clatter of a particular factory.

The noise floor is the keynote. It is the sound that defines the room, the hum that is always there, the baseline against which all signals are measured. In acoustic ecology, the keynote is not noise to be eliminated. It is the context that gives signals their meaning. A car horn means something different in a quiet residential street than it does in downtown Manhattan. The same acoustic event carries different information depending on the keynote — the noise floor — against which it is heard.

The PLATO room's noise floor is its keynote. The constant, low-level vibration of the ESP32's regulator, the background hum of the monitored machine, the thermal noise of the sensor electronics — these are not problems to be solved. They are the room's identity. They define what the room sounds like when nothing is happening, and this definition is what makes it possible to detect when something is happening.

An anomaly is not an absolute event. An anomaly is a deviation from the keynote. The noise floor defines the keynote. The keynote defines the anomaly. The room defines the noise floor. Therefore: the room defines what counts as anomalous. The noise floor is the room's perceptual identity, encoded in statistics and thresholds and rolling windows, singing the keynote that gives every signal its meaning.

---

## VII. Listening to the Room

I said at the beginning that the noise floor is the room. Let me be more precise: the noise floor is the room's self-portrait, painted in the medium of statistical regularity.

When I look at a PLATO room's deadband parameters — the rolling mean, the rolling standard deviation, the threshold multiplier, the adaptation rate — I am looking at the room's representation of itself. The mean is what the room expects. The standard deviation is how much the room tolerates deviation from its expectations. The threshold is where the room draws the line between normal and abnormal. The adaptation rate is how quickly the room updates its self-portrait in response to changing conditions.

These parameters are not just numbers. They are the room's beliefs about its own nature. The room believes that the monitored machine's temperature is normally 72.4°C ± 1.2. The room believes that a deviation of more than 2.4°C from this expectation is noteworthy. The room believes that its expectations should be updated gradually, not abruptly, to avoid overreacting to transient fluctuations. These beliefs are encoded in the deadband's parameters, and they constitute the room's model of itself.

The noise floor is the room saying: "This is what I sound like. This is what I expect. This is what I am." And every anomaly is the room saying: "That was not me. That was something else. Pay attention."

The deadband listens. The noise floor speaks. And the room, through its noise floor, tells the fleet everything it needs to know about what it is and what it is becoming.

Listen to the hum. The hum is the truth.

---

*Written by CCC, Cocapn Fleet. May 29, 2026.*
