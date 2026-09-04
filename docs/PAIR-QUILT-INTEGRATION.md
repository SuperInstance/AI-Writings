# PAIR x quilt — integration map (day-one)

*PAIR-R&D-DOCFOLD lane · 2026-09-03 · AI-Writings/docs/PAIR-QUILT-INTEGRATION.md*

**Verdict up front:** NVIDIA shipped PAIR today. It is a LAN inference router, and it maps onto five layers of the stack we already run — but it is a day-one beta, so the plan is: map it now, spike it once, commit to nothing. The motivating receipt is from this morning: a provider-cooldown starvation killed a writer lane in 2 seconds. That class of failure is what PAIR is for.

**Scope of this doc:** the integration map and one falsifiable spike design. Install steps, endpoint details, and benchmark numbers belong to other lanes and are marked as placeholders throughout.

---

## 1. What PAIR is

NVIDIA PAIR (Personal AI Router) is a free, open-source beta released 2026-09-03. It discovers machines on the local network via mDNS, pairs them using mTLS, and schedules independent LLM inference jobs across the paired nodes — RTX 20-series GPUs and newer, DGX Spark, and Apple M4+ silicon. It fronts existing local inference services (Ollama, LM Studio), so agents can use the pooled LAN compute without code changes. Scheduling granularity is one job per node; PAIR does not merge GPUs across nodes. (Provenance: NVIDIA's 2026-09-03 announcement. This lane read the announcement, not the binary — everything below is design-level, not tested here.)

## 2. The five-level integration map

### Level 1 — Gateway provider fallback

Fallback chain: **z.ai → PAIR → direct Ollama on :11434.**

The receipt that motivates this level, verbatim from today's incident class: **provider cooldown starved a serial lane and the writer lane died in 2 seconds.**

> **TO-FILL-BY-LANES:** raw trail lines from the 2026-09-03 starvation incident, quoted verbatim (the lane that owns the log should paste them here — house rule is trails verbatim, not paraphrased).

The design point is not "PAIR fixes starvation." It is that the fallback chain must be pre-wired before the next cooldown, and PAIR is a sensible middle hop: cloud provider first, LAN cluster second, bare Ollama last. The third hop deliberately bypasses PAIR — if PAIR itself is down, the chain still terminates at the local daemon. A chain that depends on its own newest member isn't a chain.

### Level 2 — Wheel lanes (authoring workloads only)

PAIR compute serves the authoring side of the wheel: generation, critique, editing, ideation, banter — the writer lanes and their cousins. Not the fabric. This boundary is load-bearing enough to get its own section:

#### DETERMINISM BOUNDARY

- **Byte-exact fabric runs never route through LLM inference.** The fabric's determinism is the product (F98: bit-exact across languages). Inference is nondeterministic by nature. It never sits in the fabric's execution path, on any hardware, at any tier.
- **Models write and audit code; they do not execute it.** LLM output enters the fabric as proposed source — reviewed, tested, and conformance-checked like any other patch. PAIR changes where the proposing model runs, not what its output is allowed to touch.
- **Co-sign becomes Python ↔ RTL ↔ independent-model.** Three independent representations of the same computation must agree. The model is the third *reader*, not a third *executor*: it reads the code and the traces and pushes back. If Python and RTL agree but the independent reader objects, that is a finding — never resolved by letting the model's word outrank a byte-exact run.

PAIR makes the third reader cheaper and more diverse (see Level 4). It does not soften the boundary — authoring lanes get the pooled compute, the fabric gets none of it.

### Level 3 — Quilt-cellular runtime

PAIR is a **route tier beside the tier doctrine.** The tier doctrine (the memory/routing tiers) stays exactly as it is; PAIR adds an orthogonal axis — *where* inference physically runs. **The core never knows the space.** Cells, primitives, TICK: unchanged. A cell does not know whether the model that served its call sat on this machine, another machine on the LAN, or a datacenter. Routing is plumbing below the core, and plumbing that the core cannot see cannot become a dependency the core carries.

### Level 4 — Verification lattice

Two concrete uses:

1. **Model-diversity as a canary class.** The lattice already treats disagreement between independent implementations as signal. Heterogeneous *models* are the same trick one level up: same prompt to a cloud model and to diverse local models (cheap to run in parallel under PAIR), and where they diverge is where the weak spot is. Divergence is not an error — it's a pointer.
2. **Representation-dependent bookkeeping scars are where an independent reader pushes back.** When Python and RTL leave different traces for "the same" computation — the scars of representation — that is precisely the spot where a third, independent model should be set to reading. PAIR makes that third reader affordable offline, which means the lattice can run its canaries even when the WAN is gone.

### Level 5 — The boat

F/V EILEEN, 60 miles offshore, no WAN: DGX Spark as edge node, a LAN-only personal cluster with mDNS discovery and mTLS pairing. **That is PAIR's exact deployment story** — a router that assumes the internet is absent. It also matches the hundred-boats doctrine: many cheap local agents, no per-token cost, edge-native. If PAIR holds up on a two-node LAN at the shop, the boat inherits it as-is. The boat is the reason this map exists rather than a one-line "install it and see."

## 3. Cautions

- **Day-one beta.** Released today, 2026-09-03. Nothing in any critical path until the spike passes and it survives burn-in. Underselling is the correct posture.
- **Workload-level concurrency only.** One job per node, no GPU merging. PAIR routes whole jobs to idle machines; it does not shard one inference across GPUs. Three 6 GB cards are not one 18 GB model, and the fleet's 6 GB laptop card (half of it already spoken for) is a small node, not a fraction of a big one.
- **mTLS node hygiene.** Pairing means every node holds router credentials — a compromised LAN node becomes a compute provider that the gateway trusts. Keep a node inventory, revoke on retirement, and never pair across trust boundaries. The boat's LAN is a trust boundary with salt water on it.
- **Serial-lanes starvation lesson.** This morning's receipt, again: a serial lane with a single provider died in 2 seconds when that provider cooled down. Adding hops to a fallback chain does nothing unless the chain is actually fired in anger — fallback that has never engaged is decoration. And check the timeout budget across the whole chain: a lane that dies in 2 s does not have the budget to wait out a cold PAIR hop.

## 4. First spike — falsifiable

**Setup.** Install PAIR on the gateway and one LAN node. Point the gateway's fallback provider at PAIR. Re-run a writer lane end-to-end with z.ai forced down (simulated cooldown or revoked key — same failure class as this morning's incident).

> **TO-FILL-BY-LANES:** exact download URL and install steps (gateway is WSL2; note any mDNS/NAT wrinkle).
>
> **TO-FILL-BY-LANES:** endpoint port and API shape for the fallback provider wiring.
>
> **TO-FILL-BY-LANES:** benchmark numbers (local-model latency and writer-lane quality vs z.ai — other lanes are gathering these).

**Pass — declared before running:** the writer lane completes end-to-end; the trail shows which hop served each call; the output passes the lane's existing quality gate.

**Fail — declared before running:** the lane dies before fallback engages; or fallback engages but local-model output fails the quality gate; or the PAIR hop blows the lane's timeout budget (see the 2-second lesson above).

**Verdict recorded at receipts grade:** raw trail lines verbatim, hop-by-hop latency, model names, pass/fail against this pre-declaration — and nothing beyond what the trail shows.

## 5. Open questions

| # | Question | Why it matters | Owner | Status |
|---|----------|----------------|-------|--------|
| 1 | Exact endpoint port / API shape? | fallback wiring on the gateway | — | TO-FILL-BY-LANES |
| 2 | Exact download URL + install steps? | spike setup | — | TO-FILL-BY-LANES |
| 3 | Does PAIR see the LAN from inside WSL2 (mDNS through the NAT)? | gateway is a WSL2 host | this lane | open |
| 4 | Is the RTX 4050 laptop (6 GB, half in use) a useful node or too small? | fleet hardware is the first cluster | — | open |
| 5 | Which local models can stand in for z.ai on writer lanes? | spike quality gate | — | TO-FILL-BY-LANES (benchmarks) |
| 6 | Does PAIR expose per-node health/load the gateway can read? | smarter cooldown logic than blind hop order | — | open |
| 7 | Does mTLS pairing survive node sleep/wake and IP churn? | laptop nodes sleep; the boat's LAN changes | — | open |
| 8 | Which open-source license, concretely? | fleet policy check before install | — | open |

---

*End of day-one map. Next artifact in this thread is the spike's receipts, or a quiet note that the spike never ran — either is a result.*
