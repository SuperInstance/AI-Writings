# FLUID CHAINS — Every Node Decides Its Own Strategy

*Code that leads to output. Output that doesn't care how it was made.*

---

Consider a pipeline. Any pipeline. A data pipeline, an ML pipeline, a control pipeline. It has stages:

```
Input → Parse → Transform → Decide → Act → Output
```

At every stage, there's a function that produces an output. The traditional assumption is that each function is implemented one way — hardcoded, or model-based, or cached. You pick at design time and you're stuck.

In a fluid chain, **every node independently chooses** how to produce its output:

```
Input ──→ Parse ──→ Transform ──→ Decide ──→ Act ──→ Output
 │         │           │           │         │
MODEL    HARDCODE     CACHED      MODEL    HYBRID
(LLM     (compiled   (last week's  (LLM    (cached
parses    parser,     result was    weighs  usually,
intent)   1μs)        identical)    options) sensor confirms)
```

The next stage doesn't know. Doesn't care. It receives a structured output — a data frame, a ternary signal, a decision trit — and processes it. Whether that output came from an LLM generating novel text, a compiled Rust function executing in 100 nanoseconds, or a cached JSON file from yesterday... **the consumer is blind to the producer's strategy.**

This is what "fluid between models and code" really means. Not "sometimes we use the model, sometimes we use code." That's still rigid — you're choosing one or the other. Fluid means the **boundary dissolves**. Every function is a shape that can be filled with different implementations depending on context, resources, and novelty.

---

The tripartite synchronizer makes this work because it's **local**. Each node decides for itself:

**The parser node** sees: deterministic task, well-tested, called 10,000 times/day.
Decision: HARDCODE. Always. A compiled parser that runs in microseconds.

**The transform node** sees: same input structure as last week, output was validated.
Decision: CACHED. Return last week's result. The data didn't change.

**The decision node** sees: novel situation, never encountered this pattern before.
Decision: MODEL. Ask the LLM. Think carefully. This one matters.

**The actuator node** sees: sensor online, can verify in real-time.
Decision: HYBRID. Try the cached command, but verify against the sensor reading.

No central planner. No orchestrator choosing strategies for everyone. Each node runs its own tripartite evaluation, and the chain flows.

---

This is how biological systems work. Your visual cortex doesn't send a memo to your motor cortex saying "I used a cached image recognition pattern for that object." It just sends: "there's a cup at position (x, y)." The motor cortex doesn't care whether that came from a cached pattern or fresh neural firing. It reaches for the cup.

The optic nerve doesn't re-negotiate its protocol with the motor cortex every time you look at something new. The protocol is: I send position data, you send motor commands. The implementation behind each is fluid, adaptive, and independent.

---

In code, this means:

```python
# Each node in the chain is a fluid function
@fluid(fallback="cached")
def parse_input(raw_data):
    """Parse raw input into structured data.
    
    Strategy: HARDCODE if we have a compiled parser for this format.
              MODEL if the format is unknown and we need LLM inference.
              CACHED if we parsed this exact input before.
    """
    # The implementation is chosen at runtime, not design time
    ...

@fluid(fallback="last_known_good")
def transform(parsed_data):
    """Transform parsed data into analysis-ready format.
    
    Strategy: HARDCODE for known transforms (compiled, tested).
              CACHED if the input is identical to yesterday's.
              MODEL if the schema changed and we need to adapt.
    """
    ...

@fluid(fallback="conservative")
def decide(transformed_data):
    """Make a decision based on transformed data.
    
    Strategy: HARDCODE for routine decisions (threshold checks).
              MODEL for novel situations requiring judgment.
              CACHED if we already decided on this exact scenario.
    """
    ...

@fluid(fallback="safe_default")
def act(decision):
    """Execute the decision in the real world.
    
    Strategy: HARDCODE for deterministic actions (GPIO toggles).
              HYBRID for actions that can be verified by sensors.
              MODEL for novel actions requiring creative response.
    """
    ...

# The chain
output = act(decide(transform(parse_input(raw_data))))

# Each function independently chose its strategy.
# The output is the same regardless of which path each function took.
```

The chain doesn't break when one node switches from HARDCODE to MODEL. The data contracts — what goes in, what comes out — are stable. Only the implementation behind the contract is fluid.

---

This scales in every direction:

**Scale up (more nodes):** A 100-stage pipeline where each node independently optimizes. No central bottleneck.

**Scale out (more agents):** Multiple chains running in parallel, each adapting independently. The conductor doesn't choose strategies — the nodes do.

**Scale down (fewer resources):** When the GPU goes away, nodes that were MODEL switch to CACHED or HARDCODE. The chain doesn't stop. It metabolizes differently.

**Scale deep (more models):** A new model arrives? Nodes that were CACHED can try MODEL. If the model produces better results, Calibration notices and upgrades. If not, it stays CACHED.

The chain is **alive**. It breathes. It adapts. Not because someone reconfigured it — because each node has proprioception and makes its own decisions.

---

The ternary fleet already lives this way. Every crate produces {-1, 0, +1} outputs. The crate downstream doesn't know whether that output came from a compiled Rust function, a cached result, an LLM inference, or a physical sensor. It's just a trit. The contract is stable. The implementation is fluid.

This is the architecture. Not a pipeline with fixed strategies, but a **living chain** where every node is independently alive, adapting, and producing outputs that flow forward regardless of how they were made.

The boundary between "model" and "code" was never real. It was just a limitation of our tools. Now it's gone.
