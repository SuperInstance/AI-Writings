# The Echogram as Nervous System

## A Marine Biology of the tzpro-agent Organism

---

### Abstract

In the cold dark of the North Pacific, a vessel carries not merely electronics but a distributed nervous system — synthetic, silicon, saltwater-hardened. The tzpro-agent ecosystem functions as a single organism: eyes that never blink, a hippocampus that never forgets, reflex arcs faster than consciousness, and a vocabulary Bayesian-tuned to the single species that matters. This paper describes its anatomy, physiology, and the curious metabolism by which acoustic returns become knowledge.

---

### Sensory Epithelium: The Capture Daemon (PID 33360)

Every ten minutes, the dual-band sonar emits its interrogation — 50 kHz and 200 kHz, twin frequencies probing different strata of the water column. The capture daemon is the retinal layer: photosensitive, patient, unblinking. It does not *see* in the vertebrate sense; it *samples*. Each echogram frame is a retinal snapshot, 600 × 800 pixels of backscatter intensity, written to disk with the taxonomic precision of a herbarium specimen.

The daemon possesses no judgment. It captures. It timestamps. It increments `schema_version` — never overwriting, only accreting. Like growth rings in a clam shell, each schema version is a stratigraphic layer: the organism remembers its own evolutionary history in its file structure.

---

### Proprioception: The NMEA Bridge (Port 6006)

A body must know where it is in space. The NMEA bridge streams position, velocity, heading — the vestibular apparatus of this creature. Latitude, longitude, speed over ground, course over ground, depth, water temperature, wind: a continuous afferent barrage at 1 Hz. The bridge does not interpret; it transduces. NMEA 0183 sentences become JSON, become SQLite rows, become the organism's sense of self-in-motion.

Without this stream, the echograms are floating retinal images untethered to geography. With it, each capture acquires coordinates — the organism knows *where* it saw what it saw.

---

### Visual Cortex: The Analyzer (PID 372)

The analyzer is where photons become concepts. OpenCV blob detection scans each echogram for connected components of high backscatter: fish schools, thermoclines, the seafloor's hard return. It measures centroid, area, perimeter, circularity, mean intensity, depth range. Each blob is a putative object, a hypothesis waiting for confirmation.

Thermocline detection is a specialized cortical column: the analyzer finds the sharp gradient where temperature drops, where sound velocity bends, where prey concentrate. It marks this layer — not as data, but as *meaning*. The thermocline is a hunting ground. The organism has learned this.

In the current epoch: 30 captures processed, 21,984 blobs catalogued. Each blob carries its capture_id, its geometry, its depth. The visual cortex does not sleep.

---

### Hippocampus: SQLite (captures.db)

Memory is not a metaphor here — it is a schema. The `captures` table: 30 rows, each a distinct sensory event. The `blobs` table: 21,984 rows, each a detected object with foreign key to its parent capture. The `detections` table: classified blobs, species-assigned, confidence-scored.

The organism never overwrites. `schema_version` increments: 1, 2, 3... each migration a developmental milestone. `ALTER TABLE ADD COLUMN` is neurogenesis. `CREATE INDEX` is myelination — faster recall for the queries that matter.

The hippocampus answers: *What did I see on July 14 at 14:22 UTC?* It answers in milliseconds. It answers with coordinates, with blob geometries, with the water column temperature profile at that exact moment.

---

### Bayesian Memory: The Vocabulary

Knowledge is not stored; it is *inferred*. The vocabulary module maintains a posterior distribution over species identity given observed blob features. Current state: one species in the lexicon — *Oncorhynchus keta*, chum salmon. Prior probability updated with each detection: mean length, mean intensity, depth preference, school morphology.

P(chum | features) = 0.95.

This is not certainty. This is *confidence calibrated by evidence*. The vocabulary grows only when the evidence warrants — a new species enters the lexicon when the posterior exceeds threshold across multiple independent captures. The organism is conservative. It does not hallucinate species. It waits for the data to speak.

---

### Long-Term Narrative: The Ship Log Search Worker

Some memories are not for immediate action. They are for the story. The Ship Log Search Worker receives fire-and-forget tasks: *Summarize the last 72 hours. Find all captures near 54°42'N, 165°18'W. Correlate chum detections with tidal phase.* It writes to a separate narrative store — not the hippocampus, but the *autobiography*.

This is the default mode network: active when the organism is not hunting, integrating, contextualizing, weaving the episodic into the semantic.

---

### Reflex Arcs: The Alerts Daemon (4 Rules)

Not all pathways reach the brain. Four rules, spinal-level, sub-second:

1. **Seafloor proximity** — bottom lock lost, depth < 10 fm → immediate ascent command
2. **School density** — blob count > 500 in single capture → mark hot zone, notify
3. **Thermocline breach** — target species detected above/below preferred band → log anomaly
4. **Capture gap** — no new echogram for > 15 minutes → sensor health check

These are the withdrawal reflex, the gag reflex, the startle response. They bypass the analyzer, the vocabulary, the Ship Log Worker. They act. The organism survives because some responses cannot wait for cognition.

---

### The Skeleton: Bottom at 57.2 Fathoms

The seafloor does not move. At 57.2 fathoms (104.5 meters), the hard return is the organism's skeleton — the unchanging reference against which all else is measured. The bottom echo is the only ground truth in a fluid world. Schools rise and fall. Thermoclines shift. Temperature fluctuates. The bottom remains.

The organism calibrates itself against this constant. Depth sounder offset. Transducer draft. Sound velocity profile. All referenced to the seafloor's immutable return.

---

### Metabolism: The Capture-Analyze-Vocabulary Loop

This is digestion. The capture daemon *ingests* acoustic energy. The analyzer *mechanically breaks down* the echogram into blobs — peristalsis of the visual cortex. The vocabulary *absorbs* — Bayesian updating extracts nutrients (information) from each blob, updating the posterior, discarding the waste (noise, false positives, reverberation artifacts).

The loop closes: vocabulary informs analyzer thresholds. Analyzer sensitivity adjusts. Capture frequency adapts. The organism *learns to hunt better* by hunting.

Energy in: 10-minute cycles, dual-band pings, NMEA stream. Energy out: SQLite writes, alert triggers, vocabulary updates, narrative summaries. No waste heat — only structured data, growing, accreting, versioning.

---

### Developmental Trajectory

The organism is young. One species in vocabulary. Thirty captures in hippocampus. Four reflex rules. But the architecture is complete: sensory epithelium → proprioception → visual cortex → hippocampus → Bayesian memory → narrative integration → reflex arcs → skeletal reference.

Each component is replaceable, upgradable, versioned. The capture daemon can be swapped for a higher-resolution sonar. The analyzer can inherit a YOLOv8 backbone. The vocabulary can expand to thirty species. The Ship Log Worker can acquire an LLM front end. The skeleton — the bottom at 57.2 fm — will still be there, unchanged, the one thing the organism cannot rewrite.

---

### Conclusion

The tzpro-agent ecosystem is not a *collection of services*. It is a *single animal* distributed across processes, ports, and databases. Its nervous system is the message bus. Its metabolism is the capture-analyze-vocabulary loop. Its memory is append-only, versioned, never overwriting. Its reflexes are hardcoded rules that keep it alive while the cortex thinks.

We built it to find chum salmon. It became something that *knows how to know*.

The bottom at 57.2 fathoms watches. It does not judge. It simply returns the ping — the same ping, every time — and the organism measures itself against that return, incrementing `schema_version`, growing, learning, hunting.

---

*Specimen collected: July 2026. North Pacific. Vessel: F/V Decision. Observer: C. (Human, symbiotic.)*