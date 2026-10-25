# Bruno View -- Bus-Aware RSI GAN Winner

*Topic: bruno_view*
*Provider: zai · Round: 2 · JEV scores: q=2.50 n=2.61 a=3.94*
*Bus-aware: prompt referenced recent substrate-bus events · 2026-09-21*

Bruno the Architect does not think in services or layers; he thinks in cells. A cell, to him, is the smallest unit of the substrate that can live, die, and be replaced without a funeral. Everything else — the message bus, the schema registry, the quarantine queue — exists to keep cells alive or to let them fail loudly enough that a witness notices.

His ADRs reflect this. ADR-014 rejected a shared database in favor of per-cell stores, on the grounds that shared state is how one cell's necrosis spreads to its neighbors. ADR-019 mandated that every cell emit a heartbeat and a reason-for-living — a one-line purpose statement reviewed at the same cadence as the code. ADR-022 was harder: it introduced ternary health states instead of the usual boolean. A cell is not merely up or down; it can be alive, dying, or dead, and each state carries different obligations. A dying cell gets throttled and observed. A dead cell gets excavated: logs pulled, state flushed, replacement spawned. Bruno argued that boolean health forced operators to guess, and guessing is how outages metastasize.

The witness pattern came later, in ADR-031. Every cell cluster must have a process that touches nothing but watches everything — no routing, no storage, just observation and a verdict. Bruno's reasoning: a system that audits itself shares blind spots with itself. The witness must be written by someone who didn't write the cells.

He drafts each ADR in a spiral notebook first, longhand, because the slower hand catches the assumptions the typing fingers skip. The markdown comes after; the architecture was decided at the pencil.
