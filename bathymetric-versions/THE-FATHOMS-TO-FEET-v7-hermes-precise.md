# The Fathoms To Feet — v7-hermes-precise

The spinning disc sounder employs a clever technique: by increasing its speed sixfold, the same device can measure depth in either fathoms or feet. The underlying physics and the transducer remain constant, but the precision of the measurement changes. This principle, known as multiscale measurement in numerical analysis, allows the same instrument to operate at different scales, with the relationship between those scales providing additional information.

When measuring depth in fathoms, a reading of 60 fathoms (360 feet) indicates that the seafloor lies within a six-foot range, specifically 360 ± 3 feet. This level of precision is sufficient for navigating a boat in deep water. However, switching to foot resolution, which involves spinning the disc six times faster during the time-of-flight interval, the measurement becomes more precise, reading 362 feet ± 0.5 feet. This increased resolution allows for the identification of specific features on the seafloor, such as ledges, rock piles, and depressions where fish might congregate.

The transition from fathoms to feet is not merely a matter of increased precision; it represents a fundamental shift in the type of questions that can be asked. At fathom resolution, the primary question is "where am I in the ocean?" while at foot resolution, the question becomes "what is the structure of this particular piece of the seafloor?" The instrument itself does not change, but the resolution enables different questions to be asked and answered.

In numerical analysis, this concept is known as Richardson extrapolation. By measuring a quantity at two different step sizes (h and h/2), the difference between the measurements provides information about the error in both. If the error scales as a power of h, which is common for most numerical methods, the measurements at two different resolutions can be used to cancel the leading error term and extrapolate to the true value.

The fishing analogy for this principle involves running the sounder at both fathom speed and foot speed over the same area. The coarse map generated at fathom speed provides the overall shape of the seafloor, including features like shelves, drop-offs, and channels. The fine map generated at foot speed reveals the details, such as rocks, depressions, and snags. Neither map alone provides a complete picture; it is the relationship between the maps that offers the most comprehensive understanding. The coarse structure indicates where to look for detail, while the detail refines the coarse structure. This is an example of wavelet decomposition in its natural habitat, where each scale captures different aspects of the structure, and the scales are related by the underlying physics of the measurement.

In the fleet, the conservation law (γ+H = constant across rounds) plays a role similar to the invariant in Richardson extrapolation. It is the quantity that remains constant when the resolution is changed. In numerical analysis, the true solution is the invariant that both measurements are approximating. In the fleet, the conservation law is the invariant that both coarse (small fleet) and fine (large fleet) measurements are instantiating. The conservation law holds at both low and high resolutions, making multiscale comparison valid.

The formal mapping between fishing, numerical analysis, and fleet architecture can be summarized as follows:

| Fishing          | Numerical Analysis | Fleet Architecture |
|------------------|-------------------|-------------------|
| Spinning disc    | Numerical integrator | Fleet coordination loop |
| Disc speed        | Step size h       | Fleet size V      |
| Fathoms (slow disc) | Coarse grid (large h) | Small fleet (V=5) |
| Feet (fast disc)  | Fine grid (small h) | Large fleet (V=30) |
| Seafloor depth    | True solution     | Task capability   |
| γ+H conservation  | Scale-invariant quantity | Conservation law |
| Paper trace at two speeds | Richardson extrapolation pair | Fleet results at two scales |
| Scouting runs     | A priori error estimates | Historical tile queries |

The practical consequence of this principle is that operating at multiple resolutions is always beneficial. A fleet that only operates at a high resolution (V=30) may be precise but lacks context. Conversely, a fleet that only operates at a low resolution (V=5) may understand the overall landscape but cannot identify specific details. By running coarse sweeps first to identify the rough landscape and then targeting fine sweeps on areas of interest, the fleet can gain a more comprehensive understanding of the problem space. The coarse results inform the fine routing, while the fine results validate the coarse picture, ensuring consistency through the conservation law.

The disc speed trick also highlights the distinction between precision and accuracy. At fathom speed, the reading is accurate (the ping correctly measures depth) but imprecise (only providing 6-foot granularity). At foot speed, precision is increased without affecting accuracy, as the ping and physics remain the same. The gain is in resolution, which is the ability to distinguish nearby values. Accuracy is determined by the physics, while precision is determined by the instrument's representation. The spinning disc allows for the independent adjustment of precision without affecting accuracy.

In the fleet, this means that capability (accuracy) should not be confused with scale (precision). A small fleet is not less capable than a large fleet; it simply resolves the problem space at a lower granularity. The conservation law ensures that the total capability remains constant (γ+H is invariant), but the distribution of that capability across the problem space changes with the fleet size (V). At low V, capability is spread coarsely, while at high V, it is distributed finely. The conservation law guarantees that scaling up does not create new capability but rather resolves capability that was already present at a coarser granularity.

The measurement theory of the fleet is the same as the measurement theory of the ocean. The same instrument (the spinning disc) operates at different speeds, resulting in different resolutions, with one invariant (the conservation law) holding true at every scale. Fathoms provide the overall shape, while feet reveal the structure. The conservation law represents the truth that remains constant across all scales.

In conclusion, the principles of multiscale measurement and Richardson extrapolation apply to both the ocean and the fleet. By operating at multiple resolutions and leveraging the conservation law, the fleet can gain a more comprehensive understanding of the problem space, ensuring both precision and accuracy in its operations.