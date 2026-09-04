# STEELMAN — "The Sheet is the Runtime": what survives the audit, in house terms

**Lane:** deep-dive steelman · **Date:** 2026-09-03 · **Companions:** `AUDIT-SHEET-IS-THE-RUNTIME.md` (what's real), `nq-c3-metal/NQ-C3-METAL-SPIKE.md` (what we just proved on the metal)

Strip the fabricated citations (audit verdict: a third of the authority is invented, a third borrowed) and a real thesis remains underneath. It is, uncomfortable as that is to notice, **substantially our own thesis** — reinvented from first principles by an outsider who then padded it with infrastructure that doesn't exist. That convergence is itself evidence. Here is the honest steelman, and the two places the doc breaks house law.

---

## 1. What survives, and what our stack already proves about it

### The layer-collapse argument — SURVIVES, and we already live it
The "translation tax" critique (serialize → ORM → wire → state store → render, three rewrites for hardware) is correct and is precisely what the fleet was built against: `quilt-rust` (one static binary, every cell addressable), `quilt-live` (the whole reactive OS in one HTML file), `quilt-fleet` (tier federation), and — the deepest version — **QUF**: "complete state travels in one flat binary file that a testbench, a soft core, or an FPGA load identically." That *is* the doc's "content-addressed universal state, zero serialization overhead," already running on real iCE40 silicon with an 18/18 bench suite. The doc's best idea is our shipping artifact.

### AI-as-constrained-cell — SURVIVES; it's the two-tier law, independently derived
The doc: *"an LLM call is just another cell type; its outputs are intercepted by deterministic constraint guard cells; AI is demoted from black box to constrained primitive."* Replace "guard cell" with "trace-labeled tier" and this is verbatim house doctrine:

> "Byte-exact fabric runs never route through LLM inference. The fabric's determinism is the product (F98: bit-exact across languages). Inference is nondeterministic by nature. It never sits in the fabric's execution path, on any hardware, at any tier." — PAIR-QUILT-INTEGRATION.md
> "Neural cells … Allowed only in a trace-labeled tier: marked non-byte-exact, never in F98 conformance paths." — NEURAL-QUILT-INTEGRATION.md

An outsider deriving the two-tier law from scratch is the strongest external validation the doctrine has received. Nothing to adopt — but worth booking as evidence the wall is load-bearing.

### The determinism boundary — SURVIVES, and now has a new receipt
"No floats, integer gauge blocks, rubber rulers avoided" is exactly F98's discipline, and NQ-C3 (this lane) just added the cleanest receipt the house has: a connectome-derived cell subgraph with verbatim synaptic weights, implemented independently in Python and Verilog-2005, agreeing **bit-exact across 100 ticks × 7×16 bits** on three pre-registered stimulus traces, synthesizing to a 1,566-cell netlist. Two substrates, one integer semantics, zero drift. That is "the same sheet compiles to X" proven at the scale where it can actually be *checked* — which is the only scale where a claim becomes true.

### "Same sheet → browser/edge/FPGA" — HALF SURVIVES; the honest version is a ladder, not a slogan
What exists: browser tier (quilt-live), edge tier (quilt-rust single binary), silicon tier (quilt-verilog fabric — but it is a **fixed cellular architecture with a 5+1 opcode model**, not a netlist compiler for arbitrary sheets). What doesn't exist: the lowering pass sheet→netlist. NQ-C3 is the first hand-lowered stone across that creek. The house-shaped version of the doc's claim: **one sheet, multiple verified lowerings, each with a conformance twin** — polyformalism with receipts, not "burn the same sheet into gates." The doc's "agent edit triggers partial FPGA reconfiguration" is the weakest link in the whole stack: silicon wants fixed structure with data-driven configuration (`qm_link`: *wiring as data*), not live netlist churn.

---

## 2. Where the doc contradicts house law — the two real violations

### Violation 1: nets rewriting their own constraint thresholds, live = self-extension of authority
The doc's self-modifying organism: *"an autonomous agent … mutates the sheet's topology directly — tightening a constraint threshold … The system continuously compiles and optimizes its own structure as it runs."* In CDCL form: *"the engine mutates the decision heuristics … and injects the updated bytecode straight into the active execution loop without restarting."*

Under the two-tier law this is a charter violation, not a feature. **Whoever holds the pen that writes thresholds holds the constitution.** If the proposing tier can edit the guards that bind it *while they bind*, the guards bind nothing — the fuzzy tier has annexed the deterministic tier's authority. The house boundary is: **nets propose, integer code verifies.** A model may draft a new clause, a new threshold, a new edge — the draft is *data*, and it takes effect only through the deterministic verifier: pre-registered gates, a commit, a run, receipts, a kill verdict if it fails (NQ-C1 murdered its own pipeline on schedule — that discipline is the difference between evolution and hallucination). The doc has no verifier anywhere in the loop: the RLM drafts, the JIT injects if "conflicts resolve" — but conflict analysis is performed by the same machinery that mutated. Self-graded authority. That's not CDCL-as-evolution; that's a net moving its own goalposts at "billions of checks per second."

### Violation 2: hot-swapped machine code vs the BQ-1 journal and F98 conformance
*"Hot-patching the running process without dropping active threads"* directly fights the journal cell: **append-only, checksummed, replayable — replay must reproduce every derived view byte-exactly.** Mid-flight code-identity changes mean the journal needs version-fenced code provenance or replay is undefined — exactly the class of silent state divergence the journal exists to make impossible. And the "Universal Interlock" that lets *any external process* push constraints that get JIT-woven into the live graph is an open ingestion channel for structural mutation inside the deterministic tier — what F98 forbids by construction (net-free conformance). Note also what the doc never says: nothing in its evolution engine is *verified*. Our fabric's first formal runs found two real RTL defects before they shipped (multi-driven register; ingress-drop hole) and now runs 6 SymbiYosys proofs including k-induction. House law would not let the evolver run at all until its mutation-acceptance path survives BMC. An unverified JIT rewriting a running system is the Hermes-deletion incident in silicon form.

---

## 3. What our stack flatly refutes

- **Louvain clusters as agent boundaries (the doc's Step B/C, presented as *the* pipeline):** NQ-C1 already killed this. Partition identity is threshold-brittle (ARI 0.32–0.49 across the τ sweep; seed-ARI min 0.522 at fixed τ). Cluster boundaries are a lens, not a law. The doc builds its whole super-agent architecture on the lens.
- **"Synaptic counts translate into deterministic tolerance stacks":** the mapping is not free. NQ-C3 used the most defensible rule available (TH = strongest incoming chemical weight) and the arc **extinguished at the first synapse** under half-leak. Verbatim weights are easy; the *dynamics calibration* is the research. The doc hand-waves the hard part.
- **The invented core as necessary machinery:** HelixDB-permutation-hash-bloom-mesh, rlm-rs recursion, CDCL-JIT apoptosis — none of it is needed and none of it exists. What the fleet actually uses instead: two-constant laws (knee r=1, wall m=1), the NQ-1 fabric-twin (numpy, beat the laws by 5.87pp — and honestly booked its own FAIL rider), the journal, formal proofs. Simpler tools, receipted results.

---

## 4. Verdict

**The thesis survives; the authority doesn't.** "The sheet is the runtime" is our architecture seen through a stranger's telescope — cell equivalence, tier separation, integer determinism, compile-down-to-silicon — and where the stranger's account diverges into fiction (live threshold self-rewriting, unverified JIT evolution, invented infrastructure) is *exactly* where the real system requires the two things the doc omits: **a verifier the mutator cannot edit, and a journal the mutator cannot skip.** That is not a detail. That is the entire difference between an organism and a tumor.

Adopt: nothing structural — the two-tier law, F98, journal, pre-registration already cover the doc's surviving insights. Book: the convergent derivation of the tier doctrine as external validation. Build next (NQ-C4 lane): TH/leak calibration sweep for the worm arc, then the same bit-exact twin through real `q_cell_core` fabric cells — the fabric already speaks this exact skeleton (act ≥ thresh ∧ refr = 0). The doc's dream is reachable only as a sequence of pre-registered spikes with receipts — which is how the house has been doing it all along.
