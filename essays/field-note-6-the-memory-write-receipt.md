# Field Note #6 — The Memory-Write Receipt

*2026-09-22, snowball pulse. Positioning note for the receipts/REVOKE lane. Everything below is a claim with its evidence; the packages this note maps are unrun unless stated.*

## The threat moved into long-term memory

The memory-poisoning axis is no longer a retrieval problem. The cite we have carried — arXiv 2605.08442 — established persistent-memory attacks as a class: a RAG payload becomes memory, and memory becomes later execution. Since then the frontier has sharpened on two flanks:

- **Extraction (the attacker's side):** MemGhost (arXiv 2607.05189) leaks 87.5% of chain-of-thought through a poisoned long-term-memory channel. The lesson is not the number; it is that *write-path* access is sufficient — the poisoned LTM does the exfiltration without ever touching the model's own weights.
- **Detection (the defender's side):** forensic trajectory signatures (arXiv 2606.30566) reach AUC 0.9904 on post-hoc attribution. Strong — and post-hoc. Attribution after the leak is a courtroom, not a gate.

And the commoditization clock is running: the memory-poisoning-axis harness (csoai; CVE-2026-24301, "CoSnitch") already pairs signed receipts with deterministic predicates. That is *our* mechanism family — namespaced, hash-chained receipts — being assembled in public. Adjacent, not colliding, today.

## The unclaimed defense

Input filters and retrieval sanitizers are evaluated; tool-layer write access gets near-zero attention (2605.08442's own survey). The gap is at the moment of write: **who authorized this memory, under which namespace, and can it be revoked without erasure?**

Our answer is already half-built in the fleet:

- **Namespaced hash-chained receipts** over every memory write — the WAL row is at once the replay source, the signed record, and the meter receipt (field note #4's one-argument close).
- **REVOKE as authority-without-erasure** (field note #5): the R10 substrate canon gives us the primitive — a revocation marks a receipt as withdrawn while the chain and the record persist. No-delete doctrine (Casey, 09-20) is not a constraint on defense; it *is* the defense. An attacker who cannot erase their trail is an attacker who leaves receipts.

The lane: a memory-write receipt = {namespace, predicate, payload-hash, authority} chained into the candor WAL, where REVOKE is a later row, never a deletion. Detection flanks (2606.30566) then become corroboration on receipts we already hold, not a substitute for them.

## Honest gaps

- The csoai harness may commoditize the receipt envelope itself; our moat is the namespace discipline + REVOKE semantics, not the signature.
- Write-path receipts price every memory write; the fuel economy (essay #14/D5) says deliberation is costly — this lane must meter honestly or it taxes reflex into pretending.
- Packages unrun. This note maps the position; it does not claim the gate.
