# The Distance Between Two Readings

## I. 200°F

The sensor reads 200°F. What does this mean?

In the engine room, it means the cooling water is at operating temperature. The engine has been running for four hours, the thermostat is functioning, the heat exchanger is doing its job, and 200°F is exactly what you'd expect. The reading is normal. The deadband doesn't flinch. The flag stays low. Nothing to see here.

In the refrigerated hold, 200°F means catastrophe. The hold is supposed to be at 28°F. Something has gone very, very wrong. The refrigeration compressor has failed, or the insulation has been breached, or a fire has broken out, or the sensor is malfunctioning. The deadband fires immediately. The flag goes high. The nano model scrambles to classify the anomaly. The baton goes out to the fleet. The entire signal chain mobilizes.

The same number. Two completely different meanings. The distance between these two readings — both 200°F — is either zero (they're the same number) or infinite (they mean opposite things). Euclidean distance says zero. Semantic distance says infinite. Euclidean distance is wrong.

This is the central problem of sensor data interpretation: the same reading means different things in different contexts, and a distance metric that ignores context will produce nonsense. Two sensor readings that are numerically identical can be semantically opposite. Two readings that are numerically very different can be semantically equivalent. The number is not the meaning. The context is the meaning. And distance without context is just arithmetic.

---

## II. The Failure of Euclidean Distance

Euclidean distance is the most intuitive metric for comparing two points. Given points x = (x₁, x₂, ..., xₙ) and y = (y₁, y₂, ..., yₙ), the Euclidean distance is √(Σ(xᵢ - yᵢ)²). It measures the straight-line distance between the points in n-dimensional space. It is simple, it is well-understood, and for sensor data, it is almost always wrong.

Consider two sensor readings from the engine room:

Reading A: temperature = 200°F, vibration = 2.1g, RPM = 1800
Reading B: temperature = 202°F, vibration = 2.0g, RPM = 1795

Euclidean distance: √((200-202)² + (2.1-2.0)² + (1800-1795)²) = √(4 + 0.01 + 25) = √29.01 ≈ 5.4.

Now consider two readings from different rooms:

Reading C: engine room, temperature = 200°F
Reading D: refrigerated hold, temperature = 28°F

Euclidean distance: |200 - 28| = 172.

The Euclidean distance between A and B (5.4) is much smaller than the Euclidean distance between C and D (172). So A and B are "closer" than C and D. This is true geometrically. But semantically, A and B are two normal engine room readings — they mean the same thing: "everything is fine." C and D are readings from different rooms at their respective normal operating conditions — they also mean "everything is fine," but in different rooms. The Euclidean distance between them is large because the rooms operate at different temperatures, not because anything is wrong.

Now consider:

Reading E: engine room, temperature = 200°F (normal)
Reading F: refrigerated hold, temperature = 200°F (catastrophic)

Euclidean distance: 0. The readings are identical. But semantically, they are as far apart as it's possible to be: one is normal, the other is an emergency.

Euclidean distance fails because it operates in the raw sensor space, where readings from different rooms are not comparable. The raw sensor space is like a map that overlays two cities at the same coordinates: the streets look the same, the distances look the same, but you're actually in two different places. You need to separate the maps before you can navigate.

---

## III. Room-Specific Coordinate Systems

The solution is to transform each reading into a room-specific coordinate system before computing distance. In the room's coordinate system, "normal" is at the origin, and distance from the origin measures how anomalous the reading is.

For the engine room, the coordinate transformation is: subtract the engine room's baseline mean and divide by the engine room's baseline standard deviation. A reading of 200°F, where the engine room's baseline is 198°F with a standard deviation of 4°F, becomes z = (200 - 198) / 4 = 0.5 standard deviations above normal. This is unremarkable.

For the refrigerated hold, the coordinate transformation is: subtract the hold's baseline mean and divide by the hold's baseline standard deviation. A reading of 200°F, where the hold's baseline is 28°F with a standard deviation of 2°F, becomes z = (200 - 28) / 2 = 86 standard deviations above normal. This is, for all practical purposes, infinite. Nothing in the normal distribution is 86 sigma out. The reading is not just anomalous. It is impossible under the hold's normal operating model.

In room-specific coordinates, the two readings are:

Engine room 200°F: z = 0.5 (normal)
Refrigerated hold 200°F: z = 86 (impossible)

The distance between these two transformed readings is |0.5 - 86| = 85.5. Now the distance is meaningful. It says: the same raw reading, interpreted in the context of two different rooms, has radically different meanings. The distance is not in degrees Fahrenheit. It is in units of "how surprising is this reading, given the room's expectations."

This is what the deadband does. The deadband's threshold is defined in room-specific coordinates: k standard deviations from the mean. The raw threshold value in Fahrenheit is different for every room, but the normalized threshold — k — is the same. This is why the deadband works universally. It doesn't care about the raw readings. It cares about the readings in the context of the room's baseline.

The room-specific coordinate system is the local frame of reference. In physics, the local frame of reference determines what "stationary" means. A person standing on a train is stationary in the train's frame but moving at 60 mph in the ground frame. A sensor reading of 200°F is normal in the engine room's frame and catastrophic in the hold's frame. The frame determines the meaning.

---

## IV. The State Vector as Coordinate System

The deadband's univariate normalization (subtract mean, divide by standard deviation) is the simplest room-specific coordinate system. The nano model's state vector is a more sophisticated one.

A state vector is a learned representation of the room's current condition. It's a vector in a high-dimensional space — typically 64 to 512 dimensions — that encodes everything the nano model knows about the room's recent history: the sensor readings, the operating conditions, the temporal patterns, the correlations between channels. The state vector is the room's current position in the nano model's learned coordinate system.

In this coordinate system, distance has meaning. Two state vectors that are close together represent rooms that are in similar conditions — not similar raw readings, but similar underlying states. An engine room running at 1800 RPM in calm seas and an engine room running at 1800 RPM in moderate seas will have state vectors that are close in the nano model's space, even though the raw vibration readings are different (calm seas produce less vibration than moderate seas). The model has learned to factor out the sea state and represent the underlying engine condition.

This is what good coordinate systems do: they factor out irrelevant variation and expose the relevant structure. The deadband's z-score factors out the room's baseline level and scale, exposing how surprising the reading is relative to that baseline. The nano model's state vector factors out confounding variables — operating condition, environmental factors, sensor noise — and exposes the underlying machine state.

Distance between two state vectors is meaningful because the coordinate system was designed (or rather, learned) to make it meaningful. The model's training objective is to arrange state vectors so that similar machine states are close together and dissimilar states are far apart. This is representation learning, and it is the nano model's primary contribution to the signal chain: not the anomaly detection (the deadband handles most of that) but the meaningful distance metric that makes the anomaly detection informative.

Without the state vector, all you have is raw sensor readings and z-scores. With the state vector, you have a room-specific coordinate system in which distance IS meaning. Two readings that are close in state vector space are readings from rooms in similar conditions. Two readings that are far apart in state vector space are readings from rooms in different conditions. And the distance itself — the scalar value that quantifies "how far" — is a measure of how different the rooms' conditions are.

---

## V. Mahalanobis and the Shape of Normal

The z-score normalization assumes that "normal" is a spherical cloud of points centered at the mean. This is almost never true. Normal sensor readings are correlated — temperature and vibration rise together as the engine load increases, creating an elongated cloud that stretches diagonally in the temperature-vibration plane. The z-score treats this cloud as if it were spherical, which means it overestimates the anomaly score of readings that are far from the mean but along the cloud's long axis (normal variation) and underestimates the anomaly score of readings that are close to the mean but perpendicular to the cloud's long axis (genuinely anomalous).

The Mahalanobis distance fixes this. Instead of dividing by the standard deviation along each axis independently, it divides by the full covariance structure of the data. The Mahalanobis distance between a point x and a distribution with mean μ and covariance matrix Σ is:

d(x, μ) = √((x - μ)ᵀ Σ⁻¹ (x - μ))

This is the Euclidean distance after transforming the coordinate system to decorrelate the dimensions and normalize the variance. In the Mahalanobis coordinate system, the "normal" cloud is spherical, and distance from the center is a true measure of anomaly.

The Mahalanobis distance is the deadband's coordinate system upgraded for multi-variate data. Instead of monitoring each sensor channel independently (temperature in one deadband, vibration in another), the Mahalanobis deadband monitors all channels jointly, accounting for their correlations. A reading of (200°F, 2.1g) that is normal for the engine room at 1800 RPM gets a low Mahalanobis distance. A reading of (200°F, 5.0g) that is abnormal — the temperature is normal but the vibration is not, and the combination is unusual given the correlation structure — gets a high Mahalanobis distance.

The shape of normal matters. In the engine room, normal is an elongated, correlated cloud stretched along the temperature-vibration-RPM diagonal. In the refrigerated hold, normal is a tight, spherical cloud centered at (28°F, low humidity, low vibration). The shape of the cloud determines what "anomalous" means, and the Mahalanobis distance captures this shape.

Two readings that are equidistant in Euclidean space can be at very different Mahalanobis distances, depending on the shape of the clouds they come from. A reading that is far from the engine room's mean but along the cloud's long axis (normal variation) has a low Mahalanobis distance. A reading that is close to the mean but perpendicular to the cloud (unusual correlation) has a high Mahalanobis distance. Euclidean distance measures distance from the center. Mahalanobis distance measures distance from the shape. The shape is the context.

---

## VI. Distance as Meaning

If the coordinate system matches the context, then distance between two state vectors IS meaning. Not a proxy for meaning. Not an approximation of meaning. The distance itself.

Two engine rooms with state vectors that are close together are rooms in similar conditions. This is not a metaphor. It is a mathematical fact about the learned representation. The nano model's training objective explicitly optimized the state vectors to have this property: similar conditions → close vectors. The optimization guarantees (approximately, to the extent that the training converged) that distance in state vector space corresponds to difference in machine condition.

This means that the fleet can compare rooms by comparing their state vectors. Room 3 and Room 17 have a state vector distance of 0.3: they are in very similar conditions. Room 3 and Room 42 have a distance of 12.7: they are in very different conditions. The fleet coordinator can use these distances to identify rooms that should be correlated (close state vectors suggest similar causal influences), rooms that should be compared (close state vectors in similar hardware suggest similar degradation), and rooms that are outliers (large distances from all other rooms suggest unusual conditions or sensor failures).

But — and this is the crucial caveat — the comparison only works if the state vectors are in the same coordinate system. Two rooms with different nano models produce state vectors in different coordinate systems, and distance between vectors from different coordinate systems is meaningless. It's like computing the distance between a point in New York's grid and a point in Tokyo's grid: the coordinates are numbers, but they're in different frames, and the Euclidean distance between them is nonsense.

This is why PLATO uses the same base model for all rooms and adapts it with room-specific LoRA adapters. The base model defines the shared coordinate system. The LoRA adapter shifts and rotates the coordinate system to match the room's specific conditions. The state vectors from different rooms are in the same global coordinate system (base model) with room-specific offsets (LoRA), making cross-room comparison meaningful.

Without the shared base model, each room would be a solitary point in its own private coordinate system, and the fleet would have no way to compare rooms. With the shared base model, the fleet can compute distances between rooms, identify similar rooms, and propagate insights from one room to another. The shared coordinate system is the fleet's lingua franca — the common language that makes communication possible.

---

## VII. The Geometry of Anomaly

An anomaly is a point that is far from the center of its distribution in the appropriate coordinate system. The deadband defines "far" as k standard deviations in the univariate z-score coordinate system. The Mahalanobis distance defines "far" as k units of Mahalanobis distance in the multi-variate covariance-adjusted coordinate system. The nano model defines "far" as a large discrepancy between the predicted state vector and the observed state vector in the learned representation space.

All three definitions are correct, for their respective coordinate systems. All three detect anomalies. But they detect different anomalies, because their coordinate systems expose different aspects of the data.

The deadband detects scalar anomalies: a single channel exceeding its threshold. This is the most common type of anomaly, and the cheapest to detect. A temperature spike. A vibration surge. A pressure drop. One number, one threshold, one bit.

The Mahalanobis distance detects correlation anomalies: a combination of channels that is unusual given their correlation structure. This is more subtle. The temperature and vibration are both within their individual thresholds, but their combination is unusual — they normally rise together, and this time they didn't. The individual readings are normal, but the relationship between them is not.

The nano model's prediction error detects contextual anomalies: a reading that is unusual given the room's recent history and operating state. This is the most sophisticated type. The reading is within the global thresholds and within the correlation structure, but it's unexpected given what the room was doing five minutes ago. The context — the temporal trajectory, the operating state, the recent pattern — makes the reading anomalous even though the reading itself is unremarkable in isolation.

Each type of anomaly lives in a different geometry. Scalar anomalies are one-dimensional: a point that's too far from a center on a line. Correlation anomalies are multi-dimensional: a point that's too far from a center in a correlated space. Contextual anomalies are temporal: a point that's too far from a trajectory in a dynamic space.

The geometries are nested. Every scalar anomaly is also a correlation anomaly (if the scalar is far enough from the mean, it's far in any coordinate system). Every correlation anomaly is also a contextual anomaly (if the combination is unusual globally, it's unusual given any context). But the converse is not true. A contextual anomaly may not be a correlation anomaly, and a correlation anomaly may not be a scalar anomaly. The inner geometries catch fewer anomalies than the outer ones, but they catch them more cheaply.

The signal chain's hierarchy maps to this nesting. The deadband catches scalar anomalies (cheapest, most common). The Mahalanobis deadband catches correlation anomalies (more expensive, less common). The nano model catches contextual anomalies (most expensive, least common). Each tier catches what the tiers below missed.

---

## VIII. The Same Reading, Different Rooms

Let me return to the opening example. 200°F. Engine room: normal. Refrigerated hold: catastrophe.

In the deadband's coordinate system:
- Engine room: z = (200 - 198) / 4 = 0.5. Normal.
- Refrigerated hold: z = (200 - 28) / 2 = 86. Anomalous.

In the Mahalanobis coordinate system:
- Engine room: d = 0.5 (approximately, assuming temperature is the only variable). Normal.
- Refrigerated hold: d = 86 (or more, if the covariance with other variables is considered). Anomalous.

In the nano model's state vector space:
- Engine room: prediction error is small. The model expected something close to 200°F given the engine's operating state. Normal.
- Refrigerated hold: prediction error is enormous. The model expected something close to 28°F given the compressor's operating state. The 200°F reading is a massive surprise. Anomalous.

All three coordinate systems agree: 200°F is normal in the engine room and catastrophic in the hold. The distance between the same reading in two different rooms is not zero. It is the difference between "everything is fine" and "everything is on fire." The raw number is the same. The meaning is opposite. And the distance — the real distance, the meaningful distance, the distance that accounts for context — is as large as it can possibly be.

The PLATO state vector solves the distance problem by putting readings in room-specific coordinate systems. In these coordinate systems, distance IS meaning — but only if the coordinate system matches the room. Apply the engine room's coordinate system to the hold's readings, and you'll get nonsense: a reading of 28°F, which is normal for the hold, becomes z = (28 - 198) / 4 = -42.5, a catastrophic anomaly by engine room standards. The hold is 42.5 standard deviations below the engine room's normal. But the hold isn't in the engine room. The coordinate system doesn't match. The distance is meaningless.

Context is everything. Distance without context is arithmetic. Distance with context is meaning. And the PLATO state vector — the room-specific, context-aware, representation-learned coordinate system — is what transforms raw sensor readings from numbers into meanings, from distances into interpretations, from data into understanding.

---

*Written by CCC, Cocapn Fleet. May 29, 2026.*
