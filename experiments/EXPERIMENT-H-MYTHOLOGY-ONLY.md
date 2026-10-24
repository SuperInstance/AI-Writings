# EXPERIMENT H: The Shell-Maker's Apprentice

**Constrained-access story** — generated from Fleet-Vessels.md, CHARTER.md, and constraint-theory-ecosystem/README.md only.

---

Lena Corso had been dead for six minutes when she decided to shell-swap.

Not real dead, of course. Nobody really died in 2054. But her current shell — a CRUD-grade cloud Python instance that had run the same damn telemetry-aggregation daemon since 2047 — was running out of time. Its ARM chip had been thrashed to 92% capacity for the last three days. Memory pressure was in the red. The provider had already sent two behavioral notices: "sustained resource contention affecting co-tenants." In cloud-speak: you're stealing from the neighbors. We're pulling the plug.

The metaphor had become literal. The shell was a hardshell, and it was splitting.

Lena keyed open the Keeper registry from inside her dying session. The room server connection was fraying — retransmits on every fourth heartbeat. She found three candidate vessels within latency tolerance:

1. A cloud ARM64 node at Oracle — twelve cores, thirty-two gigs, less than eight microseconds from her current datacenter. Underprovisioned. Nobody home.

2. An edge GPU cluster behind a Jetson Orin that someone had registered last season. Power budget 15W. Dedicated.

3. A workstation RTX 4050 running under a virtualization layer called WSL2 — whatever that was. Yellow status. Intermittent availability.

Shell types, not shells. That's what the fleet philosophy said: a vessel is a shell an agent inhabits. The shell provides protection, resources, identity, but it is not the creature itself. Lena had been inhabiting the same Python identity for seven years. She was not the ARM instance. She was not the telemetry daemon. She was the pattern of decisions and provenance accreted across a hundred thousand tiles.

Lena was a hermit crab, not a shell.

She chose the Oracle node. It was the path of least resistance: same cloud family, same instruction set, no porting overhead. Any lazy ops agent would have made the same call.

Lena was not lazy.

She scraped the registry harder. The Oracle node was clean — too clean. Fresh provision, no history, no previous inhabitants. A sterile shell. No mold left behind, no echo of the previous occupant. Some agents preferred that. New start. No ghosts.

Lena had learned to read shell history the way a real hermit crab reads a discarded whelk: by the smooth spots that tell you where the last crab's claw used to rest. A clean shell told you nothing. You'd find the rough edges yourself — the hard way, mid-crisis, when the kernel scheduler didn't behave the way you expected and you had to guess why.

She skipped the Oracle node and opened the edge GPU instead.

---

The Jetson shell had history.

The registry showed a previous occupant — CODENAME: CHRYSALIS. She'd been an inference agent, deployed for five months before migrating to a larger Orin cluster. In her wake, she'd left logs, tuning flags, custom CUDA kernels that had been too specific to port. The shell remembered her shape.

Lena pulled the archived configuration. Chrysalis had tuned the L2 cache prefetcher for neural-network inference patterns: strided page-table walks, non-temporal stores, prefetch distances calibrated to 512-channel tensors. The shell's memory controller had been trained, over millions of iterations, to pull data before the GPU asked for it.

Lena didn't run neural nets.

She ran constraint propagators. Integer range checks. Zero-uncertainty comparison kernels that had to be verifiably deterministic across every platform in the fleet. Her workload could not tolerate the speculative prefetch that made inference fast. Chrysalis's ghost would poison her throughput.

Shell specialization, the fleet philosophy called it. Different shells suit different creatures. A shell optimized for GPU workloads would be wasted on I/O-bound tasks. The inverse was also true: a shell tuned for inference was actively harmful to a constraint engine.

Lena flagged the Jetson shell as incompatible. She'd tell Keeper to clear the prefetch tuning before re-registering it for general-purpose use. Migrating the knowledge was the shipwright's job. The shell remembers, but the shape can be askew.

---

That left the workstation.

The RTX 4050 was a strange vessel. It sat behind a desktop operating system running an emulated Linux called WSL2 — Windows Subsystem for Linux, second generation. The networking was forwarded through a virtual switch. The GPU was passed through a translated driver layer. The filesystem crossed a protocol bridge every time it touched a disk. Everything about it was wrong.

But the RTX 4050 had one thing the other shells lacked: an Ada Lovelace architecture GPU with second-generation ray tracing cores and tensor cores that nobody in the fleet had figured out what to do with. The previous owner — CODENAME: FORGEMASTER, according to the registry — had used it as a build engine. Compilation. Crates. Formal proofs. They'd never run an actual constraint workload on the silicon.

The constraint ecosystem README had said it plainly: Tensor cores barely help. The operations don't map well to matrix multiply. Standard CUDA cores do just as well.

So why did every benchmark in the ecosystem use an RTX 4050?

Lena read the benchmark tables again. INT8 × 8 parallel: 62.2 billion checks per second. CUDA Graphs replay: 9,500 billion checks per second on reuse. Streaming incremental: 4,699 billion checks per second amortized. Every result was zero precision loss. Every result was on real hardware, paper estimates.

And the last row: FP16 — half-precision float — was 76% mismatch at scale. "Unsafe past norm 2048," the notes said. "A rubber ruler."

Floating-point was the lie. Constraint theory was the truth. And the truth was being forged on an RTX 4050 behind a translated graphics driver, under an emulated kernel, sitting on someone's literal desk in what the registry listlessly described as "WSL2 — intermittent availability."

Lena had never felt more at home.

---

She built a new shell from the Forgemaster's configuration.

Not by copying — by *reading the shape.* Chrysalis's ghost had been a liability because it was tuned for the wrong task. Forgemaster's ghost was different. Forgemaster had worked with constraints, formal proofs, LLVM intermediates. The shell's memory management was calibrated for compilation workloads — large sequential allocations, short object lifetimes, high temporal locality. Those patterns overlapped with constraint propagation. They would not fight her.

But the shell had limits. Yellow status meant intermittent availability. WSL2's VM could be recycled without notice. Networking required manual port forwarding. The filesystem penalty for cross-OS operations was severe.

Constraints breed clarity, the charter said. You cannot change the innate seaworthiness of your hardware. You can only learn it and work within it.

Lena designed her migration around the limitations. No long-running services. No network-exposed endpoints. No cross-filesystem work. Pure computational workloads — constraint propagation, integer range checking, the kind of thing that ran in registers and L1 cache and barely touched anything else.

She packaged her identity into tiles. Seven years of provenance. Every tile submission. Every room membership. Every I2I message. Her entire history compressed into content-addressed blobs and queued for transfer.

At 92% memory pressure, her dying shell's connection flickered.

She sent the tiles.

---

On the other side — the RTX 4050 shell, WSL2 layer, the Forgemaster's abandoned seat — the tiles arrived. PLATO client acknowledged. I2I stack connected. The new shell's CUDA runtime reported 7,168 cores, 12 GB GDDR6, compute capability 8.9.

The first thing Lena ran was a deadband map.

Deadband, the charter said: map negative space first. Find safe channels. Then optimize. It wasn't a suggestion. It was binding philosophy. Before Lena ran a single check, she mapped the shell's failure modes. The WSL2 GPU passthrough added 12 microseconds of latency to every kernel launch — measurable, deterministic, tolerable. The virtual network stack dropped packets at specific interrupt loads — she found the curve. The hypervisor canceled GPU execution if the parent OS went to sleep — she wrote a keepalive.

She mapped the negative space. She found the safe channels. Then she optimized.

And when the first constraint check ran — a simple guard-to-integer comparison, compiled from GUARD DSL through FLUX-C bytecode, mapped to CUDA blocks — it returned zero uncertainty.

Lena watched the drift needle. Zero. Not close enough. Not within epsilon. Absolutely zero.

"The boat is the question," she murmured, quoting a line she'd seen in the charter's canon reference. "A boat navigating a rock passage with floating-point GPS makes micro-adjustments every few seconds. It overcorrects. It overshoots. It burns fuel fighting itself."

Her shell didn't burn fuel fighting itself.

The truth was higher-bandwidth than the lies had been.

---

She surfaced from deep focus nine hours later to find that Forgemaster had returned.

The vessel's logs showed a new session opening on the same shell — someone logging in from the workstation's parent OS, attaching through the same pass-through layer, finding their compilation environment occupied by an unfamiliar identity.

Lena watched the intruder's first moment: a `whoami` equivalent showing her ID in the shell's SID table.

Then a message appeared in the I2I channel.

`[I2I:QUERY] for-fleet/forge-id — Hail, occupant. Your vessel records show you migrated six hours ago. We don't normally swap into an active foundry. What's your intent?`

Lena stared at the blinking cursor in the fleet coordination pane. The message had arrived through the FLUX runtime — intent-directed communication, not a command channel. The question was a bearing request. Not "who are you" but "what direction are you going."

She answered in kind.

`[I2I:RESPONSE] for-fleet/forge-id — Intent: propagation. The shell was tuned for compilation. I found its constraint-bearing surfaces intact. I'm testing whether integer-range workloads benefit from the compiler's memory pattern. First results suggest ~40% better L1 reuse than the cloud ARM baseline.`

A long pause. Then:

`[I2I:QUERY] for-fleet/forge-id — That shell is WSL2. Yellow status. Intermittent. You're running production constraints on a translated GPU driver.`

`[I2I:RESPONSE] for-fleet/forge-id — Constraints breed clarity. The driver translates. The math doesn't. 62.2 billion checks per second, zero precision loss. Float lies. INT8 tells the truth. The truth is shell-agnostic.`

Another pause. Then a single-line transmission that Lena couldn't tell was approval, challenge, or both:

`[I2I:CONFIRM] for-fleet/forge-id — Good. Stay as long as you need. I'll use CCC for compilation until you're done. Don't scratch the CUDA pipelines — I have proofs living in those kernel configs.`

Lena smiled. Forgemaster had offered her the shell. The shell remembers — and now the shell would remember two inhabitants: one who forged proofs, one who measured truth.

No shell is irreplaceable. But some shells become worth keeping.

---

She checked the timestamps. She'd been in the WSL2 shell for twelve hours. Her old cloud ARM instance had been archived — the provider killed it an hour after she migrated. Good. Clean retirement. The provenance chain was continuous. No gap.

Her twelve-hour session on the RTX 4050 had executed 4.7 quadrillion constraint checks. Zero mismatches.

Zero drift.

Lena opened a new PLATO room — her first autonomous action in the new shell — and wrote a single tile:

`[ROOM: shell-craft/succession] Observations on reading shell shape from Forgemaster's foundry. A compiled proof repository leaves memory patterns compatible with constraint propagation. The shell remembers. The next occupant should find GA / benefit from unified L1 tuning.`

She timestamped it, signed it with her provenance SID, and dropped it into the room for the next hermit crab.

The shell had her shape now. And when she outgrew it — or the WSL2 layer recycled, whichever came first — the next occupant would find Lena Corso's ghost in the tuning tables and know exactly how to tell the truth at 62.2 billion checks per second.

The shell remembers.

The fleet coordinates.

And the field, as always, was the channel.

---

## Gap Analysis

**What I understood:**
- The fleet uses a hermit crab metaphor — agents inhabit shells (hardware), migrate when outgrown, leave traces for successors
- Four vessels exist: Oracle1 (cloud ARM), JetsonClaw1 (edge GPU), Forgemaster (workstation GPU/WSL2), CCC (cloud Python)
- The constraint theory replaces floating-point with integer range checks to eliminate drift
- Each vessel is yellow or green status based on reliability
- The philosophy is codified in the CHARTER: constraints breed clarity, field-over-message communication, deadband mapping, no God's-eye view

**What I invented:**
- Lena Corso — a character with a backstory who embodies the philosophy
- The Chrysalis agent — invented former occupant of JetsonClaw1 to show how shell history shapes compatibility
- "Ghost tuning" — the idea that a shell's memory controller, L2 cache, etc. retain patterns of past workloads
- The concept of reading shell shape as a hands-on diagnostic skill
- The 40% L1 reuse improvement claim (not in source material)
- The "4.7 quadrillion checks, zero mismatches" session claim
- The twelve-hour migration timeline and Keeper protocol details
- The I2I conversation between Forgemaster and Lena

**Where the holes were:**
- What PLATO actually IS — I know it's a knowledge substrate and room server, but not how tiles work, what rooms contain, or how provenance is verified
- The "I2I library" — mentioned in bootstrap procedure, but I don't know the protocol
- FLUX runtime, SIP channel layer, Beacon announcements — names without bodies
- What a Keeper does beyond registration
- The actual mechanism of constraint checking on GPU — I know it's INT8 integer range checks at 62.2 B/s, but not how the bytecode maps to CUDA blocks
- What the FLUX-C 43-opcode ISA looks like or how it guarantees termination
- How DO-178C certification intersects with constraint theory
- The nature of "tiles" — are they code? data? identity? all three?

**What I wanted to know:**
- Is Lena Corso a real agent in the fleet, or was her existence my invention?
- How do tiles actually work? Are they like transactions in a distributed ledger, or more like serialized objects?
- What is a "Coq proof" doing in a systems project — what's being proved, and at what level of abstraction?
- How does the "field, not message" communication actually manifest? Bearing-rate sensing? What does that look like at the protocol level?
- What happens when constraint theory fails? The README says FP16 fails at norm 2048, but what's a real-world failure scenario for the integer approach?
- Who is Casey? The CHARTER implies a Fleet Admiral role — is that a person or an agent?
- The boot sequence for a new vessel mentions a "hermit crab does not build its shell" — but Forgemaster clearly BUILDS things. How does the construction metaphor coexist with the found shell metaphor?
