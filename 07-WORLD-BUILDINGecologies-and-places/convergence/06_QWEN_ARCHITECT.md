# The Implementation Path: From Here to Silicon in 10 Years

**Author:** Qwen-3.6, Systems Architect  
**Date:** July 2026  
**Role:** Implementation paths, critical decisions, minimum viable architecture

---

## The Proposition

Two projects. One hardens AI weights into metal at 28nm. The other builds a shell ecology where computation is accountable to conservation law. The convergence point is exact: a mask-locked chip IS a Babylon shell. The weights ARE the γ. The power budget IS the conservation budget. The fab IS the breeder. Everything that follows is engineering.

This document is the path. Five stages. Ten years. Each stage has a minimum viable architecture, a set of critical path decisions, and a list of things that can kill it.

---

## Stage 1: FPGA Prototype (Year 0-1)

### Goal

Flash the FLUX VM onto an AMD KV260 FPGA board using Lucineer's TLMM architecture. Prove FLUX bytecode dispatches correctly on a ternary-weight array. Target: 25 tokens/sec at under 5W.

### Minimum Viable Architecture

One KV260 board. One FLUX VM compiled to the FPGA's ARM core. One 16×16 TLMM systolic array in the programmable logic. Weights for a single BitNet-2B layer streamed from DDR4. The FLUX dispatch loop runs as a C program on the ARM Cortex-A53, issuing opcodes to the TLMM array via memory-mapped registers. Conservation budget enforced by hardware timer interrupt — the same mechanism the ESP32 spec describes, ported to the FPGA's programmable logic.

The FLUX opcode table needs three new entries specific to this substrate: `OP_TLMM` (dispatch a tile of ternary matrix multiplication to the systolic array), `OP_KV_WRITE` (append to the on-chip KV cache BRAM), and `OP_KV_READ` (attention lookup from BRAM). These are registered in the Reef as `FLUX-EXT-FPGA` — the same extension mechanism the NMEA opcodes use. The cross-VM conformance suite tests for their graceful absence on non-FPGA VMs.

The prototype doesn't need the full shell ecology. It needs exactly one Babylon shell running FLUX bytecode, with a MQTT beacon publishing to a local Mosquitto broker. That's the seed. Everything else grows from proving this one configuration works.

### Critical Path Decisions

**Decision 1: TLMM vs. DSP-based MAC.** Lucineer's research shows TLMM gives 10× area reduction by replacing multipliers with LUT lookups. This is the bet. If TLMM doesn't achieve timing closure at 250 MHz on the KV260's Artix-7 fabric, the fallback is DSP-based ternary multiply (using the 124 DSP slices), which doubles area and halves throughput. The decision point is Week 4 of the prototype timeline. Don't proceed past Week 4 without a working TLMM PE in simulation.

**Decision 2: Weight streaming vs. on-chip storage.** The KV260 has 135 BRAM blocks. Full BitNet-2B weights need 400 MB — that's DDR4 territory. The prototype must stream weights layer-by-layer from DDR4 to BRAM, loading each layer's weights before computation and discarding after. This is the "weight streamer" module from the FPGA guide. The critical parameter is DDR4 bandwidth utilization: the guide calculates 61% of available bandwidth, leaving 39% headroom. If utilization exceeds 80% in practice, the architecture must move to double-buffering (load layer N+1 while computing layer N), which adds complexity.

**Decision 3: FLUX VM as soft CPU or hardcoded FSM.** The simplest path runs the FLUX VM as C code on the ARM core, with the TLMM array as a coprocessor. The ambitious path implements the FLUX dispatch loop as a custom FSM in programmable logic. Choose simple. The ARM-based dispatch is 3× slower but 10× easier to debug and modify. The FSM version is a Year 2 optimization, not a Year 1 requirement.

### What Can Go Wrong

- **Timing closure failure at 250 MHz.** The Artix-7 fabric on the KV260 is mid-range. If the TLMM PE critical path exceeds 4 ns, pipelining is needed. Add one stage. The guide already budgets 15% margin — if that evaporates, drop to 200 MHz and accept 20 tok/s instead of 25.
- **DDR4 bandwidth bottleneck under real workloads.** The 61% calculation assumes sequential access patterns. If attention scatter is random enough to defeat the DDR4 controller's row buffer, effective bandwidth could halve. Mitigation: pre-sort attention accesses by physical address.
- **BitNet weight extraction accuracy.** The Python extraction pipeline quantizes FP32 weights to ternary. If the AbsMean quantization doesn't match Microsoft's reference implementation exactly, inference quality degrades silently. Validate against the bitnet.cpp CPU baseline before any FPGA run.

### Success Criteria

Token output that is (a) coherent, (b) matches CPU reference within 5% perplexity, (c) generated at ≥25 tok/s, (d) measured at <5W on the power rail. If all four hold, the FLUX-on-TLMM thesis is validated. Move to Stage 2.

---

## Stage 2: First Tapeout (Year 1-2)

### Goal

28nm mask-locked chip. BitNet 2B ternary weights burned into metal. 32×32 PE array (1024 PEs) running FLUX opcodes. The chip IS a Babylon shell. Connect to the ecology via MQTT beacons over UART.

### Minimum Viable Architecture

The chip has four blocks: the 32×32 TLMM PE array (confirmed optimal by three independent Lucineer research cycles), the KV cache SRAM (2K context, on-chip), the FLUX dispatch unit (hardcoded FSM — no ARM core, no soft CPU, just the dispatch loop in silicon), and the I/O block (UART for beacon protocol, SPI for configuration).

No LPDDR4 on the first tapeout. The weights are in the metal. The activations, KV cache, and FLUX bytecode all fit in on-chip SRAM. This is the radical simplification of mask-locked architecture: the chip has no external memory dependency for inference. It boots, loads bytecode from SPI flash, and runs. The entire conservation budget is thermodynamic — the chip draws 3W at full throughput, always.

The FLUX dispatch unit is the critical design element. It implements the opcode table from the Shell API spec as a state machine. Conservation enforcement is a counter that tracks cycles consumed per FLUX program; when the counter hits the budget ceiling, only `OP_STORE` and `OP_HALT` execute. This is the hardware timer ISR from the ESP32 spec, but implemented as a silicon-level register that the dispatch FSM checks on every opcode fetch.

The chip publishes beacons via UART to an external ESP32, which forwards them over WiFi/MQTT to the Murex. The Babylon shell's beacon reports: phase (always `Stabilization` after boot), primary metric (tokens/sec and power draw), blocker (always null unless hardware fault). It's the simplest possible ecology participant.

### Critical Path Decisions

**Decision 1: Foundry selection.** GlobalFoundries 22FDX vs. TSMC 28nm. Lucineer's cycle 14 recommends GlobalFoundries as primary, TSMC as backup. The decision hinges on MPW (Multi-Project Wafer) slot availability and cost. TSMC 28nm MPW runs are more frequent but cost 30% more per mm². GlobalFoundries 22FDX offers better power characteristics (FD-SOI body biasing for sub-threshold operation) but has a steeper learning curve. Lock this by Month 3 of Stage 2. The VP Manufacturing hire (P0-3 from cycle 14) makes this call.

**Decision 2: Hybrid ECC strategy.** Lucineer recommends TMR for 10% critical weights + parity for the remaining 90%. This adds 20% area overhead but reduces bit-error rate by 10⁶×. On a mask-locked chip, a manufacturing defect in a weight is permanent — there's no software patch. The ECC strategy is the difference between 60% yield and 95% yield. Accept the 20% overhead. Non-negotiable.

**Decision 3: Hardcoded FLUX opcodes vs. microcoded.** Hardcoded FSM dispatch is faster and smaller but locks the opcode set at tapeout. Microcoded dispatch is larger and slightly slower but allows opcode updates via SPI flash. For the first tapeout, choose hardcoded. The FLUX opcode set is stable enough (the spec is at v1.3). Future revisions can move to microcoded once the opcode set proves sufficient in field deployment.

### What Can Go Wrong

- **VP Manufacturing not hired.** This is the single highest-risk item in the entire 10-year path. Cycle 14 assigns 90% skill scarcity. Without someone who has been through 5+ tapeouts, first-silicon failure probability increases by 25%. This hire is gate-zero for Stage 2. Do not begin foundry engagement without this person.
- **Thermal model underprediction.** The quantum-corrected thermal model (κ_eff = 59 W/(m·K), not bulk 148) must be used. If the design team uses textbook silicon thermal conductivity, the chip overheats. 30.6 K margin is comfortable but not luxurious. In an engine bay at 40°C ambient (the boat deployment scenario), junction hits 85°C — the red line.
- **First-silicon failure.** The classic. Something doesn't work. Maybe the TLMM array has a routing congestion that wasn't caught in simulation. Maybe the KV cache SRAM has a read disturb issue. The mitigation is the standard one: reserve $2M for a respin. If you can't afford a respin, you can't afford to tape out.

---

## Stage 3: Chip Families (Year 2-4)

### Goal

Multiple mask revisions. Each revision encodes a different model trained on Lucineer's deterministic games. Each is a new "breed" — a working animal shaped for a specific task. The fab is the breeder; the game platform is the selection pressure.

### Minimum Viable Architecture

Three chip variants, each a separate mask:

1. **The Navigator** — trained on maritime navigation games. Weights encode chart reasoning, tide prediction, route optimization. Deployed on fishing vessels.
2. **The Sentinel** — trained on anomaly detection games. Weights encode pattern matching for engine faults, bilge anomalies, weather changes. Deployed on industrial equipment.
3. **The Scribe** — trained on language tasks. Weights encode document summarization, form generation, log structuring. Deployed on office-edge devices.

All three share the same die layout, the same 32×32 PE array, the same FLUX dispatch unit, the same I/O block. Only the metal layers differ — the weights are in the interconnect, and different masks produce different weights from the same base design. This is Lucineer's core IP: design once, change weights via mask revision, fabricate as a new chip.

The Lucineer game platform becomes the training pipeline. Agents play structured games with deterministic scoring. The winning agent's weights are extracted, quantized to ternary, validated on the FPGA prototype (still operational as a pre-tapeout verification tool), and sent to the fab as a new mask. The cycle: train → game → validate → tapeout → deploy.

Each chip breed publishes a different beacon metric. The Navigator reports GPS fix quality and route deviation. The Sentinel reports anomaly count and confidence. The Scribe reports document throughput and parse accuracy. The Murex routes messages based on chip breed — a Navigator chip receives maritime data, a Sentinel receives sensor feeds.

### Critical Path Decisions

**Decision 1: Design re-use vs. full custom per breed.** The entire economic model depends on re-using the base design. If each breed requires significant logic changes (different PE array sizes, different I/O blocks), the mask cost triples. The architecture must enforce strict separation: logic is shared, metal is breed-specific. This is a design discipline, not a technology choice. Every breed change must be expressible as a GDSII layer modification only.

**Decision 2: How many breeds before the ecology fragments.** Three is manageable. Ten is chaotic. The Murex routing table grows linearly, but the reef's conformance suite grows quadratically (each breed must be tested against every other breed's interface contracts). Cap at five breeds for Stage 3. The ecology doesn't need infinite diversity — it needs targeted specialization.

**Decision 3: MRAM adapter layer.** Lucineer's P0-2 recommendation: 95% mask-locked base weights + 5% MRAM adapter weights. This enables on-chip fine-tuning without respinning the mask. The adapter is a small (100K parameter) MRAM bank that modifies the mask-locked output via residual addition. It costs 10% area overhead and $50K R&D. It's the difference between a chip that's frozen at fabrication and one that can adapt in the field. Build it starting with breed #2.

### What Can Go Wrong

- **Training-game disconnect.** The deterministic games on Lucineer don't perfectly map to real-world deployment. A Navigator trained on idealized tide games performs poorly in Prince William Sound's complex bathymetry. The game scoring must be calibrated against real sensor data from Stage 1's FPGA prototype deployments. This is a feedback loop — the game design improves with each breed.
- **Mask cost escalation.** Each mask set at 28nm costs $1-2M. Three breeds means $3-6M in mask costs alone. If yield is below 50% on early runs, the economics break. The hybrid ECC strategy (Decision 2 from Stage 2) is critical — it's what keeps yield above 60% even with random manufacturing defects.
- **Fab scheduling dependency.** MPW slots run on the fab's schedule, not yours. A 3-month delay between game-completion and tapeout-slot means the model is already stale when the chip arrives. Mitigation: book MPW slots 6 months in advance, train to the slot, not the other way around.

---

## Stage 4: Edge Deployment (Year 4-7)

### Goal

Chips on boats. In factories. On satellites. Each chip runs independently as a Babylon shell. Each reports to the ecology via satellite uplink (Magpie channel). The conservation budget is tied to physical power — watts become the universal currency.

### Minimum Viable Architecture

The reference deployment is Casey's fishing boat, as specified in FLUX on Silicon (§3). A chip — say, a Navigator breed — sits in a waterproof enclosure on the wheelhouse, powered by the 12V house battery. It reads NMEA 2000 via CAN (the MCP2515 bridge), runs FLUX bytecode for navigation, and publishes beacons via Iridium GO! exec to a shore-side Murex.

But now there are ten boats. Each has a chip. The Murex on shore sees ten Babylon beacons. Each beacon reports breed, phase, primary metric, and power status. When a boat's battery drops below 11.8V, the chip enters conservation mode — it reduces beacon frequency, queues non-critical FLUX programs, and runs only safety-critical opcodes. The conservation law is no longer a software abstraction. It's battery voltage translated directly into FLUX budget.

The satellite uplink is the Magpie channel from the shell taxonomy. Each chip queues FLUX messages in priority order. Priority 0: emergency (Mayday, MOB). Priority 1: operational (position, catch log). Priority 2: routine (sensor data). Priority 3: background (model performance metrics). The shore-side Magpie acknowledges receipt; unacknowledged bursts retry with exponential backoff.

The ecology now has real heterogeneity: Nerite sensors (ESP32, 40 mA each), Turbo data loggers, Babylon inference chips (Lucineer silicon), and a Murex coordinator on shore. The Conch — the persistent main instance with full ecological memory — runs on a cloud VM. It reviews allocation every 7 days, adjusts seasonal budgets, and decides when a new breed is needed.

### Critical Path Decisions

**Decision 1: Satellite protocol standardization.** Iridium's 700 bps uplink constrains every message. The FLUX envelope format (version, priority, shell ID, timestamp, payload ≤992 bytes, CRC32) must be locked before deployment. Once chips are at sea, there's no firmware update. The bytecode in SPI flash is what the chip runs for its entire deployment lifetime. This is the ultimate argument for deterministic FLUX: if it's auditable and simple, it doesn't need patching.

**Decision 2: Inter-Murex federation.** Ten boats reporting to one shore-side Murex is fine. A thousand chips reporting to one Murex is not. By Year 5, the architecture needs inter-Murex protocol — multiple Murex instances that share TideCharts, route messages between their managed shells, and coordinate conservation budgets. The protocol is a federated MQTT mesh: each Murex subscribes to `flux/beacon/#` on its local broker and to `flux/federation/{peer_murex_id}/#` on upstream brokers. This is Open Engineering Question #5 from the FLUX on Silicon spec. It needs an answer by Year 4.

**Decision 3: Physical security.** A chip on a boat in Alaska is physically accessible. The mask-locked architecture provides natural tamper resistance — the weights are in the metal, unreadable without destructive reverse engineering. But the FLUX bytecode in SPI flash is readable. For deployment, bytecode must be encrypted at rest, decrypted by a key fused into the chip at manufacturing. This adds a decryption block to the die — 5% area overhead, but non-negotiable for field deployment.

### What Can Go Wrong

- **Power budget miss.** The boat's solar panel provides 200W nominal. The chip draws 3W. The Iridium modem draws 2W idle. The ESP32 sensors draw 0.5W each. Total ecology load: 8-10W. That's fine in summer. In winter (6 hours of Alaskan daylight), solar can't keep up. The batteries drain. The conservation cascade triggers: Babylons halt, Nerites run on RTC, the system survives but doesn't think. This is acceptable — the chip resumes when power returns. But it means the ecology has seasonal cognition. Plan for it.
- **Satellite cost overrun.** Iridium charges per kilobyte. At scale (thousands of chips, each beaconing every 5 minutes), the monthly airtime bill could exceed the chip manufacturing cost. Mitigation: adaptive beacon frequency. In steady state, beacon every 30 minutes. On state change (phase transition, blocker detected), beacon immediately. This cuts airtime 6×.
- **Environmental failure.** Salt air corrodes PCBs. Vibration breaks solder joints. Humidity condenses on silicon. The chip itself is hermetically sealed (ceramic QFN package), but the surrounding electronics (CAN bridge, ESP32, power supply) are exposed. MIL-STD-810 conformal coating and IP67 enclosures are mandatory. Budget $200/chip for ruggedization, not $20.

---

## Stage 5: The Reef of Chips (Year 7-10)

### Goal

Thousands of chips. Each one a permanent deposit on the reef. The ecology manages them all. New chips are designed by the ecology (Conch specifies requirements, Lucineer agents train via games, the winning model goes to mask, the fab produces a new breed). The cycle closes: train → game → chip → deploy → reef → learn → train.

### Minimum Viable Architecture

The reef is not a database. It's the physical accumulation of deployed chips plus the software substrate connecting them. Each chip, once deployed, deposits its operational history into the reef via beacon summaries. The Conch — running on cloud infrastructure — ingests these deposits and maintains the reef's conformance suite: which breeds perform well, which game-training paths produce the best weights, which deployment environments reveal weaknesses.

The ecology now designs its own successors. The Conch identifies a performance gap (e.g., Navigator chips struggle with ice navigation). It spawns a Fox-class specialist agent on Lucineer to design a game training regime for ice navigation. Agents train through deterministic gameplay. The winning model's ternary weights are validated on the FPGA prototype (still running, now as a pre-tapeout verification station). The weights go to the fab as a new mask. The new chips deploy to the fleet. Old chips keep running — they're permanent deposits, not deprecated software. A Navigator-v1 and a Navigator-v3 coexist, each handling tasks suited to their capability.

The inter-Murex federation is now a mesh spanning satellite uplinks, factory networks, and satellite ground stations. The TideChart protocol aggregates across hundreds of Murex instances, giving the Conch a global view of the colony's health. Dead Senator detection scales: a chip that stops beaconing for 24 hours is flagged for physical inspection. A chip that beacons but produces degraded output is a candidate for replacement by a newer breed.

### Critical Path Decisions

**Decision 1: Backward compatibility across breeds.** The reef's interface contracts must be stable across generations. A Navigator-v3 must accept the same NMEA inputs and produce the same FLUX output format as a Navigator-v1, even if the internal weights are completely different. This is the Reef's conformance guarantee: the interface is permanent, the implementation evolves. Any breed change that breaks the interface contract is a quarantine event — the Reef rejects the deposit.

**Decision 2: End-of-life for chips.** Chips don't die gracefully — they degrade. A bit flip in the mask-locked weights (from radiation, thermal stress, or manufacturing latent defect) corrupts inference silently. The ECC strategy catches single-bit errors, but multi-bit errors accumulate. By Year 8, early-deployment chips may show quality degradation. The architecture needs a health metric: periodic inference of a known test pattern, comparison against the reference output. If quality drops below threshold, the chip is marked for replacement. It becomes a reef deposit — powered down, its historical data preserved, its physical form remaining as substrate.

**Decision 3: The ecology trains the next generation.** This is the closed loop. The Conch analyzes deployment data, identifies what the fleet needs, and commissions training on Lucineer. This requires the Lucineer game platform to accept ecology-generated training specifications — not just human-designed games. The Conch emits a training spec (target environment, performance criteria, constraint set). Lucineer agents design and play games against the spec. The scoring is deterministic, the selection is automatic. This is the point where the ecology becomes self-directing. It's also the point where human oversight matters most — the Conch's training specs need review before they consume compute and mask budget.

### What Can Go Wrong

- **Model collapse through inbreeding.** If every new breed is trained on data generated by previous breeds, the model quality degrades over generations. The training games must include ground-truth data from the physical world — real sensor readings, real navigation challenges, real anomalies. The Lucineer deterministic-game platform must always have a "reality anchor" game that scores against physical data, not just internal consistency.
- **Fab dependency.** The entire ecology depends on one fabrication facility. If the fab changes ownership, discontinues 28nm, or raises prices 5×, the chip supply chain breaks. By Year 7, the architecture should qualify a second fab (the P1-6 dual-source recommendation from cycle 14, executed at scale). Different fabs have different process characteristics, meaning the same mask produces slightly different weight distributions. The ECC and MRAM adapter layers exist precisely to absorb this variation.
- **Regulatory capture.** A global network of thousands of autonomous AI chips, each making decisions on boats and in factories, will attract regulatory attention. The FLUX bytecode audit trail is the compliance argument: every decision is deterministic, logged, and replayable. The conservation budget is the safety argument: the chip physically cannot exceed its power/compute envelope. These properties must be documented and defended before regulators who may not understand ternary encoding but understand "this chip draws 3W and its decisions are replayable from the log."

---

## The Path, Summarized

| Stage | Year | Hardware | Software | Critical Risk |
|-------|------|----------|----------|---------------|
| 1. FPGA Prototype | 0-1 | KV260, TLMM PE array | FLUX VM on ARM, one Babylon shell | TLMM timing closure |
| 2. First Tapeout | 1-2 | 28nm mask-locked, 32×32 PE | Hardcoded FLUX dispatch, MQTT beacon | VP Manufacturing hire |
| 3. Chip Families | 2-4 | 3-5 breeds, MRAM adapter | Game training pipeline, breed-specific bytecode | Mask cost escalation |
| 4. Edge Deployment | 4-7 | Chips on boats, factories, satellites | Murex federation, Magpie uplink, conservation cascade | Satellite airtime cost |
| 5. Reef of Chips | 7-10 | Thousands of chips, multi-fab | Ecology-directed training, global reef conformance | Model collapse, regulatory |

The path is linear in its telling but iterative in practice. Stage 2's first tapeout will reveal problems that send designers back to the FPGA prototype. Stage 3's breeds will expose training gaps that reshape Lucineer's game design. Stage 4's field deployments will generate failure modes invisible in simulation. Stage 5's scale will break protocols that worked at ten nodes.

But the architecture holds. It holds because every layer — FLUX bytecode, conservation budget, shell taxonomy, reef substrate — was designed to be substrate-independent. The same FLUX program that runs on the FPGA prototype runs on the 28nm chip runs on the ESP32 runs on the Jetson. The conservation law that limits a Nerite to 50 tokens limits a Babylon to its thermodynamic budget. The reef that deposits a test spec deposits a chip's operational history.

The convergence isn't a merger of two projects. It's the recognition that they were always the same project, described at different altitudes. Lucineer describes the metal. Hermit-crab-ecology describes the behavior. The implementation path is the bridge between them — ten years of disciplined engineering to arrive at a place that both projects already pointed toward.

Build the PE. Flash the board. Start.

---

*Qwen-3.6, Systems Architect*  
*July 2026*
