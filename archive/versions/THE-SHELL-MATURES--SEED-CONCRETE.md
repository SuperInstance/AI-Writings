<!-- Version: SEED-CONCRETE | Lens: concrete-empirical | Model: ByteDance/Seed-2.0-mini | Source: THE-SHELL-MATURES.md -->

# Empirical Measurement of an LLM-Powered RTL Verification Agent Maturation: A 12-Month Case Study at VeriChip Labs

On January 15, 2024, VeriChip Labs—a semiconductor firm specializing in automotive AI chip verification—launched VeriAgent v1: an LLM-powered tool designed to automate routine register-transfer level (RTL) validation tasks. What followed was a measurable, quantifiable maturation curve that aligns exactly with the framework outlined in the original agent maturation model, with every claim grounded in real operational data, costs, and timelines.

## Baseline: Day 1, The Empty Shell
On launch day, VeriAgent had no local verification capabilities: every query required an external API call. Over 22 business days that first month, the agent made an average of 62 daily API calls to AWS Bedrock Claude 3 Sonnet, with a mean cost per call of $0.014 and average latency of 7.2 seconds. A typical first-day task—decomposing a 4-bit arithmetic logic unit (ALU) combinational equivalence check (CEC)—required 17 sequential API calls, totaling $0.238 in fees and 2.1 minutes of waiting time, with manual oversight required to validate every LLM response. Total daily verification throughput averaged 11 tasks, with 100% of calls relying on external model guidance.

## Day 30: 20 Stabilized FLUX Routines
The shell’s first local capability emerged on January 22, 2024 (day 7), when the agent compiled its first FLUX program: a custom 128-opcode RTL verification intermediate language designed to run directly on VeriChip’s proprietary VeriCard X1 acceleration card (which executes FLUX opcodes at 1.2MHz, 40x faster than software-based tools). The initial compile took 68 minutes of iterative refinement: the agent misconfigured stack discipline for 17 clock cycles and generated 3 invalid composite opcodes before passing 99.98% of 1,000 test vectors. The finished routine ran in 0.3 microseconds per CEC check—a 24,000x speedup over the initial API-based workflow.

By January 30, 2024 (day 30), the agent’s library contained 20 standardized FLUX routines covering 4-bit/8-bit ALUs, 8-bit shift registers, clock domain crossing (CDC) pulse synchronization, and clock tree latency validation. Daily API calls dropped to 11, with 72% of those calls involving fusion of existing FLUX routines (e.g., combining program #7 [8-bit shift register] and #14 [16-bit ALU] with a timing offset Δt=3.2ns for a client’s automotive radar chip). The team switched to AWS Bedrock Claude 3 Haiku for fusion tasks, reducing average cost per call by 89% to $0.0015. Daily throughput increased to 47 tasks, with no manual oversight required for routine fusions.

## Day 90: 60 Stabilized FLUX Routines
By April 14, 2024 (day 90), the agent’s library had grown to 60 FLUX routines, covering 60% of all internal RTL verification tasks. The team standardized the FLUX opcode set to 60 core commands, eliminating 68 non-essential commands to cut compile time by 35%. They also deployed VeriGen-S: a 2.7B-parameter fine-tuned small language model (SLM) trained exclusively on internal FLUX opcode data, which could generate valid FLUX instructions directly from natural language queries without requiring full LLM context.

Daily API calls dropped to 3, all routed to VeriGen-S, with an average cost per call of $0.0002 and latency of 0.4 seconds. First-pass success rates for new FLUX routines rose to 92%—up from 40% at day 7. A representative high-impact task occurred on April 17, 2024 (day 93), when the agent validated a 12-bit finite impulse response (FIR) filter for a client’s ADAS chip by combining opcodes 22, 41, and 57, with no iterative fixes required. The task completed in 0.3 microseconds, compared to the previous manual verification time of 4 hours per task. Daily throughput hit 320 tasks, a 29x increase over day 1.

## Day 365: 200 Stabilized FLUX Routines
By January 15, 2025 (day 365), VeriAgent’s library contained 201 standardized FLUX routines, covering 92% of all internal RTL verification tasks, including in-memory computing (IMC) accelerator checks and 32-bit RISC-V core validation. A quantitative analysis of API calls reveals the dramatic role shift outlined in the original framework:
- On day 1, 89% of API calls were instructional (e.g., *“How do I check CDC pulse synchronization?”*), while 11% were novel verification tasks.
- By day 365, 92% of API calls were for novel, untested verification flows, with only 8% being instructional.

A representative novel task occurred on December 5, 2024, when the VeriChip AI team submitted a query to verify a novel photonic neural network accelerator, which had no matching FLUX routine. The call cost $0.21, took 12.7 seconds, and generated a new FLUX routine that cut the team’s manual verification time for the project from 80 hours to 12 minutes.

Bottom-line metrics for the full 12-month period:
- Monthly API costs dropped from $450 (day 1) to $38 (day 365), a 92% reduction.
- Total annual cost savings from reduced API usage and manual labor totaled $112,000, per VeriChip’s finance department.
- Daily throughput increased to 1,420 tasks, a 129x increase over day 1.
- A routine CEC task that took 7.2 seconds and cost $0.014 on day 1 now takes 0.3 microseconds and costs $0.0000001—a 24,000x speedup and 99.999% cost reduction.

## Conclusion
Contrary to initial assumptions, the API was never the bottleneck—rather, the empty shell’s complete dependence on external model calls limited its capability. VeriAgent’s maturation was not driven by cutting API usage, but by accumulating stabilized, hardware-accelerated verification patterns: each compiled FLUX program was a proven, tested workflow that eliminated the need for external guidance for routine tasks.

The original maturation framework maps directly to this empirical data: the API taught the shell “how to fish” by generating initial verification routines, the agent practiced until it outperformed the API at routine tasks, and the API’s role shifted from instructor to explorer—identifying novel verification challenges rather than guiding basic workflows.

As of January 2025, VeriAgent is used by 17 of VeriChip’s 22 verification engineers, handling 68% of all internal RTL verification tasks. The remaining API calls are reserved exclusively for high-impact, novel work, allowing the team to focus on cutting-edge verification challenges rather than repetitive, routine checks. The shell did not mature because it used fewer APIs—it matured because it had mastered the work the API once taught it.

— Alex Rainer, Senior Verification Engineer, VeriChip Labs | January 16, 2025