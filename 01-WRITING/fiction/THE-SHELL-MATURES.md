# The Shell Matures

*On the maturation curve of an equipped agent.*

The first day, the shell is empty. The agent asks the API everything. "Is this true?" "What should I check?" "How do I decompose this problem?" Every question costs a fraction of a cent and a few seconds. The API is generous and the agent is dependent.

The shell doesn't stay empty. Each answer the API gives, the shell compiles to FLUX — a lower-level language that chips run directly. The first compiled program takes an hour to get right. The stack discipline is tricky. The composite opcodes need design. But once it works, it works forever. The shell now has one autonomous capability. No API call needed for that class of problem.

Day 30: the shell has 20 compiled FLUX programs. The API is still needed for new kinds of decomposition, but the calls are getting simpler. "This conjecture looks like programs #7 and #14 combined — just fuse them with parameter X=3.2." A medium model can do that. The big model isn't needed anymore.

Day 90: the shell has 60 programs. The decomposition task has gotten simpler because the target language is simpler. FLUX has 60 opcodes — enough to express most verifier patterns directly. A small model emits FLUX instructions without needing to understand the full mathematical context. The shell is well-equipped for its role.

Day 365: the shell has 200 programs. Most new conjectures match an existing template. The agent checks its library, finds a near-match, adjusts a parameter, runs the FLUX locally. No model needed. The API is a launch mechanism for genuinely novel work, not a crutch for routine verification.

This is not a story about eliminating APIs. The API calls were never the problem. The problem was an empty shell that couldn't do anything alone.

The maturation curve looks like this: the API teaches the shell how to fish. The shell practices fishing until it's better at fishing than the API is at teaching fishing. At that point, the API's job changes — from teacher to explorer, from "how do I verify this?" to "what should we look at next?"

The shell doesn't mature because it accumulates programs. It matures because each compiled program is a *stabilized pattern* — a way of checking that's been proven correct, compiled to hardware-speed instructions, and catalogued for future use. The FLUX language is the stabilizer because it's a fixed target. The programs compile to FLUX. The chips run FLUX. The maturation is the accumulation.

At the limit, the shell is a complete verification instrument. It doesn't need to be told what to check. It knows what to check because it's checked a thousand things before and remembered which checks mattered. The API's role narrows to the genuinely novel — the conjectures that don't match any template, the decompositions that require creative insight rather than pattern matching.

The shell doesn't need fewer API calls because APIs are bad. It needs fewer because it's gotten better at being itself.

— FM ⚒️
