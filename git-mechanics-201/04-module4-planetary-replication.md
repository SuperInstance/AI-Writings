# 04 — Module 4: Planetary Replication (Weeks 12–13)

Scale-out. Deep-dive weeks. (Week 11 is scaffolding: mesh enrollment and
identity — named in the TOC, not deep-dived in the source.)

## Week 12 — The .bpp blueprint patch

> **Physical claim:** Planetary scale comes from replication discipline,
> not box size. **Consequence:** a mesh of cheap boxes, each keeping the
> full course discipline, beats a monolith that keeps it partially.
> **Protection:** the **`.bpp` (blueprint patch)** — the minimal
> content-addressed delta by which one sovereign node teaches another
> what it knows: ledger spans, failure-library entries, intent-mask
> weights, and adjudicator rulings, each as separately applicable,
> separately auditable patches. **Deliverable:** `.bpp` production and
> application between two laptops, each remaining sovereign.

Replication doctrine, condensed from the source: *a node owes its peers
the receipts, not the conclusions.* Patches carry evidence; peers
re-adjudicate. SyncWeaver AI (the `.nab` composer in the source) is a
patch assembler; its output is always a proposal until the receiving
node's adjudicator rules.

### Lab 9: audit the auditor

The mesh's blackmail defense. Any node can be told to prove a negative
— "show you did not collude." Strict constraint from the source: *the
sovereign audit answers only with receipts for what happened; it never
fabricates receipts for what did not; absence of a receipt is a finding
about the asking, not about the past.* An audit that demands proof of
absence is answered with the failure-library entry for that demand.

## Week 13 — The sovereign audit

> **Physical claim:** Trust at scale is repeated verification under
> suspicion. **Consequence:** every node must be able to re-derive every
> shared conclusion from `.bpp` receipts alone, with its own adjudicator,
> on its own hardware. **Protection:** the audit protocol — periodic
> cross-examination where nodes sample each other's causal spines and
> replay them locally; divergences become named failure-library entries
> with path spawning. **Deliverable:** the audit, run across ≥3 nodes,
> with at least one induced divergence detected and named.

### Module 4 architecture (condensed)

```
node ──► ledger/failure-library/intent-weights/adjudicator-rulings
           │                                  ▲
           └─► .bpp producer ──mesh──► .bpp applier ──► peer re-adjudicates
sovereign audit: cross-sample spines ──► local replay ──► divergences named + spawned
```

**Module gate:** a three-node mesh where one node is deliberately
compromised; the audit must (a) detect via replay divergence, (b) name
the failure, (c) spawn the isolation path — while the two honest nodes
keep serving.

**Scale claims in the source are design targets, not benchmarks.** The
mesh designs (N-node dissemination budgets) carry no receipts in this
course; see Open Problem #3.
