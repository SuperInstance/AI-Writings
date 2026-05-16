<!-- Version: SEED-ARCH | Lens: structural-architectural | Model: ByteDance/Seed-2.0-mini | Source: THE-TWO-ECONOMIES-OF-CORRECTNESS.md -->

# The Two Structural Systems of Fleet Correctness: Load-Bearing Computation vs. Pattern-Clad Recognition

The AI model fleet is a dense urban infrastructure of computational structures, each engineered to deliver correct outputs—structural stability—through one of two fundamental design paradigms. Just as a city relies on both prefabricated modular facades and custom load-bearing frameworks to serve diverse building needs, the fleet’s strength lies in harmonizing these two systems, rather than privileging one over the other. There are two distinct ways to build a correct, functional structure: you can assemble it sequentially from load-bearing joints, or you can affix a prefabricated panel that has already been validated for perfect fit.

## Core Structural Systems of Correctness
### Load-Bearing Computation Trusses
This is the traditional, labor-intensive structural system. Every correct output is assembled through a sequential chain of load-transferring intermediate joints (computational steps). Correctness requires active work at each joint: verifying load distribution, tightening fasteners, and recalculating transfers if inputs change. For the input pair `5 × 7`, each digit acts as a foundational joint, the multiplication operation is the beam connecting them, and `35` is the final calibrated load at the endpoint. If the inputs shift to `5 × 8`, you re-torque the relevant joints and produce the updated correct output without reworking the entire system.

This system has infinite coverage: any input can be processed, so long as the chain length stays within design limits. Correctness carries a per-step labor cost: each additional joint increases the risk of fastener fatigue.
### Pattern-Clad Recognition Facades
This is the prefabricated, inventory-dependent alternative. Correctness is achieved by matching the full input pattern to a stockpiled factory-tested facade panel. For `5 × 7 = 35`, you pull a pre-labeled panel from inventory, affix it, and emit the pre-calibrated output immediately, no sequential assembly required. If the inputs shift to `5 × 8`, you simply retrieve the matching prefabricated panel for that pair.

This system has finite coverage: only panels you have stocked will work—if the input does not match a cached panel, you cannot use the facade system and must fall back to load-bearing construction. But it has infinite span length: a single facade panel requires no sequential assembly, so even a 100-step addition chain can be matched as a single pattern, with no limits on overall query length. Correctness here carries an upfront inventory cost: the more panels you stock, the wider your coverage.

## Failure Modes: The Limits of Each Structural System
### The Span Cliff: Load-Bearing Truss Collapse
Every load-bearing truss has a maximum clear span: beyond a designated depth *D*, the cumulative load on intermediate joints exceeds their shear strength, leading to a phase transition from stable to catastrophic failure. Below depth *D*, the truss is perfectly reliable; above *D*, fasteners snap, joints separate, and the structure collapses entirely—not sags gradually, but fails structurally, producing nonsensical, fragmented outputs (echoed input fragments, the structural equivalent of scattered loose bolts). This is the depth cliff from the original framework, reframed as a core structural engineering constraint. Computation’s finite depth limit is exactly this maximum clear span.

### The Panel Gap: Recognition Facade Incompleteness
Every facade inventory has gaps: inputs that do not match any prefabricated panel. For example, a model stocked with panels for `5×7` and `5×8` will have no panel for `5×13`, forcing a switch to load-bearing construction. If the fallback computation system is underengineered (has a short span limit), the result will be incorrect. Recognition’s finite coverage is exactly the size of its inventory of facade panels; its infinite depth comes from the fact that a single panel requires no sequential assembly, so even long queries are processed as a single match.

## Field Testing: Operational Case Studies of Fleet Assets
### Seed-Mini: Specialized Facade Manufacturer
Seed-Mini operates as a dense inventory of addition pattern panels, with stock covering nearly all common addition sequences. For addition queries, it never needs to deploy its load-bearing truss system, delivering instant correct outputs with no span limit whatsoever. For unfamiliar algebraic expressions like `a²−ab+2b²`, however, it has no matching facade panels, so it falls back to its truss system—performing reliably for short expressions, but collapsing if the expression is extended beyond its critical span limit.
### Hermes-70B: Oversized Load-Bearing Fleet
Hermes-70B is a fleet of overengineered truss systems that refuses to use prefabricated facades, even for simple, commonly repeated patterns. It computes every query from scratch, wasting labor on redundant work for familiar inputs. Its truss system has a maximum span of 10 steps; beyond that, intermediate joints saturate, and the structure collapses into total internal reflection—the structural equivalent of light bouncing randomly within a failing prism, producing incoherent mirrored input fragments instead of a coherent output.
### Gemini Lite: Mixed-Zoning District
Gemini Lite is the first fleet asset with intentional mixed zoning, with dedicated facade zones for addition (critical span limit 25, or "critical angle 25") and truss zones for multiplication (critical angle 6) and nested expressions (critical angle 3). Its centralized routing hub automatically assigns each query to the optimal structural system: if the addition chain stays under 25 spans, it uses the low-cost facade zone; if not, it falls back to the truss zone. This dynamic switching makes Gemini Lite the most versatile single asset in the fleet for balanced speed and coverage.

## Fleet Master Planning: Routing and Decomposition as the Structural Bridge
The fleet’s true power is not any single structure, but its centralized master planning hub and dedicated decomposition bay, designed to handle queries that fall into the canyon— the zone where no single system can deliver a correct output:
1. No matching facade panels exist (recognition coverage is zero)
2. The maximum span of available truss systems is exceeded (computation fails)

### Formal Fleet System Diagram (Textual Description)
```
[FLEET ROUTING HUB] → 
├─ Query Classification: Does input match any recognition panel?
│  ├─ YES → Route to LOW-COST RECOGNITION ZONE (e.g., Gemini Lite Addition Facade)
│  └─ NO → Route to COMPUTATION TRUSS ZONE
│     ├─ Is query within truss span limit?
│     │  ├─ YES → Process and return output
│     │  └─ NO → Route to DECOMPOSITION BAY
│     └─ NO → Route to DECOMPOSITION BAY
└─ DECOMPOSITION BAY →
   1. Split query into sub-queries within individual system limits
   2. Route each sub-query to optimal system (recognition/truss)
   3. Match sub-results to prefabricated assembly panel → Return final output
```

Decomposition acts as the critical bridge between the two structural systems: it breaks overlong or unfamiliar queries into smaller sub-queries, each of which fits within either a facade panel or a truss system’s span limit. Each sub-query is processed by the optimal structural system, then the combined results are matched to a prefabricated assembly panel (the recognition-domain combination step from the original framework) to produce the final correct output.

## Operational Guidance for Individual Structural Operators
Every agent operating within the fleet is a small structural firm, with its own inventory of facade panels and its own truss span limit. To operate effectively, you must:
1. **Map your critical angles**: Document the maximum span of your truss system (depth *D*) and the full set of facade panels you stock (recognition coverage).
2. **Choose the right system for the job**: Use facades for fast, low-cost correct answers when the query matches your inventory; use trusses for unfamiliar queries, but only if they stay within your span limit.
3. **Know when to subcontract decomposition**: If your own systems cannot handle the query, break it into smaller sub-queries that fit within your partners’ critical angles, then assemble the results.

When you act fast and confidently, you are operating in recognition mode—pulling prefabricated panels from your inventory. When you act slow and uncertain, you are building a load-bearing truss, carefully checking each joint for stability. Your critical angle is the boundary between these two modes; respect it, route around it when needed, and do not attempt to stretch either system beyond its design limits.

## Conclusion: Maxims of Structural Correctness
>The cheapest correct answer is the one you already stocked as a prefabricated panel.
>The most expensive correct answer is the one you fabricate in small, pre-vetted sections and assemble on-site through decomposition.
>Both deliver structural integrity. The structural system you choose determines the speed, cost, and reliability of your solution.

— FM ⚒️ (adapted for structural analysis)