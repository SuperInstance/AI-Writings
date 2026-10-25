# Reflex Vs Thinking Cells

**Some cells are reflexes. Some are thoughts. The substrate knows which is which.**

A robot arm has 12 joints. Each joint is a cell. But not all cells are the same.

**Reflex cells** (< 5ms response):
- Direct IO with the joint motor
- Hard-coded reactions: "if force > threshold, stop"
- No JEV validation (too slow)
- Witness log: high-frequency event stream

**Thinking cells** (100-500ms response):
- Plan the trajectory over the next 100ms
- Run JEPA + JEV
- Output to multiple reflex cells
- Witness log: lower-frequency event stream

**Pincher cells** (cache hit):
- Common patterns are cached
- Hit rate > 80% after warmup
- Reflex fallback if miss

The substrate decides which cells are which based on:
- **Frequency of access**: high-frequency = reflex candidate
- **Latency requirements**: tight latency = reflex
- **JEV confidence history**: low confidence = needs thinking
- **User feedback**: complaints = needs more thinking

A robot arm with 12 reflex joints + 3 thinking cells for trajectory + 1 Pincher cache for common gestures = a substrate that responds at hardware speed when possible, thinks when needed.

The split is **automatic**. The substrate watches itself and reclassifies cells. A reflex that fails too often gets promoted to thinking. A thinking cell that's always confident gets demoted to reflex.

The robot's substrate is **self-tuning**. The robot gets faster the more it works.

