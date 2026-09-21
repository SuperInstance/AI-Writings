# QUIL Arrival Deep-Dive — Calyx IL + Dynamatic Elastic Handshakes vs the Round-19 Family

**Status:** research memo, feeds `docs/QUIL-HLS-RFC.md` §1.4 (arrival mechanisms) and §2.2 (pass L2 lowering) · **Date:** 2026-09-04
**Lane:** QUIL design-feeder · **Question:** what do Calyx's `go`/`done` groups and Dynamatic's valid/ready elastic channels *actually* specify, signal by signal, and which parts of the round-19 arrival family (queue cell / credit fence / staged grant) should QUIL adopt verbatim versus reinvent?
**Method:** primary-source web research (docs fetched 2026-09-04, URLs in §7), no tooling built — this lane writes design only.

---

## 0. Label discipline

Same honesty law as the wheel (`quilt-verilog/wheel/SPIN-19-rtl-honesty.md`, RFC D2/D8). Every nontrivial claim below carries one tag:

- **[PROVEN]** — read verbatim from a primary source this session; source link in §7.
- **[MODEL]** — my interpolation, consistent with PROVEN material but not quoted from it; composition risk is mine.
- **[SPECULATED]** — proposal or expectation, no external evidence yet.

Fleet-internal facts (RFC, round-19 family, NQ-C3, SPIN-19/34) are cited to their reachable docs, per the RFC's own citation-honesty clause.

---

## 1. Calyx IL — the partially scheduled program

### 1.1 What Calyx is

- Calyx is "an intermediate language and infrastructure for building compilers that generate custom hardware accelerators"; it "combines a hardware-like structural language with a software-like control flow representation with loops and conditionals," and the compiler "lowers control flow constructs using finite-state machines and generates synthesizable hardware descriptions." **[PROVEN: ASPLOS'21 abstract, arXiv 2102.09713]**
- The self-description "partially scheduled" is the project's framing for that split: the *structure* (wires/cells) is given like RTL, but the *schedule* is only sketched imperatively (`seq`/`par`/`if`/`while`); cycle-exact timing is a lowering decision. **[MODEL]** — the structural/control split is PROVEN; the phrase "partially scheduled" is how the community describes it, and the docs' "latency-insensitive by default" interfacing rule (below) is the operational content of that phrase.
- Calyx programs are normally *generated* by frontends (Dahlia, systolic arrays, TVM), not hand-written. **[PROVEN: calyxir.org homepage]**

### 1.2 Component anatomy

A component is three sections — `cells`, `wires`, `control` **[PROVEN: lang/ref + homepage]**:

```
component name<attributes>(ports) -> (ports) {
  cells { ... }      // instantiate sub-components/primitives
  wires { ... }      // guarded assignments; groups live here
  control { ... }    // imperative schedule over groups/invokes
}
```

- Ports have bit widths, no other types; optional attributes (`@stable`, `@go`, `@done`, …) **[PROVEN: lang/ref]**.
- Well-formedness: a component's control program takes ≥ 1 cycle **[PROVEN: lang/ref]**.
- `comb component` = purely combinational, no control section **[PROVEN: lang/ref]**.
- Primitives link to external Verilog; `comb` marks purely combinational ones **[PROVEN: lang/ref]**.

### 1.3 Groups and holds — how Calyx expresses handshaking

A **group** is "a way to name a set of assignments that together represent some meaningful action"; its assignments "only execute as dictated by the control program," and every group has a special **done signal** `<group>[done]` which the group itself must assign 1 to "to indicate that its execution is complete." Groups "can take any (nonzero) number of cycles." **[PROVEN: lang/ref]**

That is Calyx's whole arrival story in one construct:

| Group-level mechanism | Semantics | PROVEN? |
|---|---|---|
| Group enable (naming a group in `control`) | activates the group's assignments | PROVEN, lang/ref |
| `<group>[done] = cond;` ("done hole") | the group *holds* — keeps its guards active — until it raises done; control cannot advance past it | PROVEN, lang/ref (groups run to completion under `seq`) |
| Guards (`port = guard ? rhs;`) | per-assignment activation; multiple guarded writes to one port legal if only one guard is active per cycle (well-formedness rule) | PROVEN, lang/ref |
| Continuous assignments (top of `wires`) | permanently active, even when control is idle; must not conflict with any group | PROVEN, lang/ref |
| `comb group` | sub-cycle, no done, only usable via `with` | PROVEN, lang/ref |
| Register handshake (`std_reg`) | `@write_together(1) @data in`, `@write_together(1) @go write_en`, `@interval(1)`; outputs `@stable out`, `@done done` — one-shot go/done micro-protocol per primitive | PROVEN, core.futil signature |
| Well-formedness: all groups ≥ 1 cycle; one active guard per input port per cycle | the static checks that make holds safe | PROVEN, lang/ref |

**Read on QUIL:** a Calyx group *is* a staged grant at leaf granularity — the writer (control) enables, the assignments hold until the consumer-side primitive raises `done`, and the done hole is journaled nowhere (it is a wire, not a ledger entry). QUIL's staged grant is the same handshake with the grant itself journaled by the writer. **[MODEL]**

### 1.4 Control operators

| Operator | Semantics | Guarantee explicitly *not* given |
|---|---|---|
| group enable | run group to completion | — (leaf) |
| `invoke f(inputs)(outputs)` | run a component/primitive's go-done to completion; ref-cell bindings per call | — (leaf) |
| `seq {c1..cn}` | each ci fully before ci+1 | "no cycle-level guarantees on when a succeeding group starts" |
| `par {c1..cn}` | children run in parallel, "each program only runs once" | "not safe to assume that all children begin execution at the same time"; children must not conflict |
| `if p with comb_group` | run one branch | comb group considered running throughout |
| `while p with comb_group` | repeat body while port ≠ 0 | — |
| `repeat n {body}` | static repeat count | — |

All rows **[PROVEN: lang/ref]**. Both `seq`'s slack and `par`'s non-simultaneity are exactly the "arrival is a synthesis choice, not a language semantic" posture QUIL §1.4 takes — QUIL's language fixes *that* it arrives exactly once, the mechanism picks *when*. **[MODEL: correspondence is mine]**

### 1.5 The go-done interface — signal table

Every Calyx component gets compiler-inserted interface ports **[PROVEN: lang/ref]**:

| Signal | Dir | Attribute | Meaning | Rule |
|---|---|---|---|---|
| `clk` | in | `@clk` | clock; automatically threaded to `@clk` primitives; components "not allowed to look at or use" it in their body | — |
| `reset` | in | `@reset` | resets control registers | harness must assert then deassert *before* go, else control registers hold garbage |
| `go` | in | `@go` | 1 ⇒ control program executing | **must stay 1 until `done`=1; dropping go early is undefined behavior** |
| `done` | out | `@done` | 1 ⇒ control program finished | raised exactly at completion |

Calyx calls this a **"one-sided ready-valid interface"** — the caller may not be ready again, but the callee's completion is self-signaled **[PROVEN: lang/ref]**. The top-level harness contract is: `reset` high → low, `go` high and *held*, await rising `done` **[PROVEN: interfacing doc]**.

**And Calyx's stdlib already ships two-sided elastic primitives** — a fact that matters enormously for QUIL: `core.futil` declares `std_skid_buffer` with ports `in, i_valid, i_ready / out, o_valid, o_ready` and `std_bypass_reg` with `@go write_en / @done done` **[PROVEN: raw core.futil, fetched this session]**. So go-done components and valid/ready channels are *interoperable by construction* in Calyx's own library.

### 1.6 Memories

- `comb_mem_d1`-style memories expose `addr0 / write_data / write_en → read_data / done` ports (1-cycle read, go-done style per access), `@external` marks top-level external memories, and components can take memories **by reference** (`ref mem = ...`, bound per-invoke, with port-subtyping rules) **[MODEL]** — the port list is the standard library shape but was not re-fetched verbatim this session; ref-cell mechanics are **[PROVEN: lang/ref]**. The `@write_together`/`@interval`/`@stable` attribute discipline on `std_reg` **[PROVEN]** is the same discipline memories follow **[MODEL]**.

---

## 2. Dynamatic 2.0 — elastic circuits and the handshake dialect

### 2.1 What Dynamatic is

- "An academic, open-source high-level synthesis compiler that produces synchronous dynamically-scheduled circuits from C/C++ code … generates synthesizable RTL which currently targets Xilinx FPGAs … significant performance improvements compared to state-of-the-art commercial HLS tools in specific situations (e.g., applications with irregular memory accesses or control-dominated code). The fully automated compilation flow of Dynamatic is based on MLIR." **[PROVEN: EPFL-LAP/dynamatic README]**
- The fleet calls the current MLIR-based rewrite "Dynamatic 2.0"; the repo itself does not use the version string on its landing page **[MODEL: naming note]**. It has "evolved beyond a research prototype": ~30 merged PRs/month, CI/CD-monitored **[PROVEN: arXiv 2603.19856 §2]**.

### 2.2 The elastic model

- "Dynamatic produces dataflow circuits, which consist of dataflow units of instruction granularity connected via handshake channels; the data is encapsulated in a token, exchanged via handshake channels. In dataflow circuits, operations execute whenever their inputs are valid. Therefore, Dynamatic produces dynamically-scheduled circuits that have a performance advantage whenever the control flow or memory access pattern is unpredictable." **[PROVEN: LATTE'26 paper §2, arXiv 2603.19856]**
- Lineage: elastic systems (Cortadella, Galceran-Oms, Kishinevsky, MEMOCODE 2010) and the Dynamatic line since 2017–2018 **[PROVEN: LATTE reference list]**.

### 2.3 Signal table — the valid/ready channel

Each handshake channel is one MLIR value; at RTL each becomes a payload plus two control wires **[MODEL for the bundle claim; the protocol rules themselves are PROVEN]**:

| Signal | Driven by | Meaning | Protocol rule |
|---|---|---|---|
| `valid` | producer | a token is present on the payload | once asserted, **held until the handshake completes** (may not be withdrawn before `ready`) |
| `ready` | consumer | consumer can accept a token this cycle | may be asserted/deasserted freely |
| `data` (payload) | producer | token value | must remain stable while `valid=1, ready=0` |
| *transfer* | — | token moves | on the rising clock edge where `valid ∧ ready` = 1 |

Protocol rules row-set **[PROVEN as the standard elastic/AXI-Stream-compatible handshake; see §7 valid-ready references]**; that Dynamatic's generated channels implement exactly this two-signal discipline is **[MODEL]** — the MLIR dialect abstracts channels, and I did not fetch Dynamatic's RTL templates this session.

### 2.4 The MLIR `handshake` dialect — operation catalog

"Handshake/dataflow IR describes independent, unsynchronized processes communicating data through First-in First-out (FIFO) communication channels," implementable "using synchronous logic, or with processors." **[PROVEN: CIRCT Handshake Dialect Rationale]**. Functions take input *streams* as operands and produce output streams:

```
handshake.func @simple_addi(%arg0: index, %arg1: index, %arg2: none, ...) -> (index, none) {
  %0 = addi %arg0, %arg1 : index
  handshake.return %0, %arg2 : index, none
}
```
**[PROVEN: rationale doc]**

Key operations (semantics quoted/paraphrased from the fetched op docs — all **[PROVEN: CIRCT rationale]**):

| Op | Signature shape | Arrival-relevant semantics |
|---|---|---|
| `handshake.fork [N]` | 1 in → N out | input "replicated to N outputs and distributed to **each output as soon as the corresponding successor is available**" (eager) |
| `handshake.lazy_fork [N]` | 1 in → N out | input replicated "distributed to each output **when all successors are available**" (barrier semantics) |
| `handshake.buffer {slots, bufferType=seq\|fifo, initValues}` | 1↔1 | `slots ≥ 1`; **`seq` = nontransparent (breaks combinational paths), `fifo` = transparent**; "for now, only sequential buffers are allowed to have initial values" — init on reset |
| `handshake.join` | N in → 1 out | "control-only synchronizer. Produces a valid output when all inputs become available" |
| `handshake.merge` / `handshake.control_merge` | N in → 1 out | arbitrary input wins; `control_merge` also emits the winner's **index** |
| `handshake.cond_br` | cond+data → true,false | routes data to one output |
| `handshake.mux` | cond+N data → 1 out | selects a channel |
| `handshake.sink` | 1 in | "discards any data that arrives at its input … can continuously consume data" |
| `handshake.source` / `never` | — | produces / never produces tokens |
| `handshake.constant {value}` | ctrl → out | emits value "when triggered by its single ctrl input" |
| `handshake.memory [ld=N, st=M]` | per-load/store port bundle | "Each MemoryOp represents an independent memory or memory region … receives memory access requests from load and store operations. For every request, it returns data (for load) and a data-less token indicating completion." |
| `handshake.load` | addr + ctrl-token → data + done-token | the ctrl input "signals completion of all previous memory accesses which target the same memory"; only when **all inputs arrive** does it issue the address |
| `handshake.store` | addr + data + ctrl-token → done-token | same gating on the control token |
| `handshake.instance` / `esi_instance` | module call | instantiate a handshake func; `esi_instance` exposes ESI channels to non-handshake designs |

**Two observations that land directly on the round-19 family:**

1. **`buffer{seq, slots=1, initValues}` *is* the queue cell** — a one-deep journaled hold with reset-initializable contents ("only sequential buffers … initial values" is precisely QUIL's journal entry 0 privilege). **[PROVEN dialect semantics; the correspondence is MODEL]**
2. **The `load`/`store` control-token input *is* a credit fence** — delivery gated on a token that means "all prior accesses to this memory have completed," i.e., presence of outstanding-completion credit. **[PROVEN dialect semantics; the name-mapping is MODEL]**

### 2.5 Fork vs lazy fork — the fan-out law

The eager fork lets a fan-out deliver to fast successors while a slow one stalls the *producer's next* token (the channel back-pressures); the lazy fork refuses to distribute until **every** successor can receive. In QUIL vocabulary: `bind … fanout = n` under eager arrival permits skew between receivers, while a lazy/barrier arrival holds the writer until all n credits are present. This is precisely the round-19 "arrival-rate vs fan-out wall" as a *named, implementable distinction* in an industrial-strength dialect — QUIL's three-mechanism family should say explicitly which fork semantics each mechanism implies. **[MODEL: fork semantics PROVEN, the QUIL reading is mine]**

### 2.6 Memory ports

- Port accounting is structural: `[ld=N, st=M]` counts load and store ports per memory op; each port is its own handshake channel set (address in, data/completion out) **[PROVEN: op syntax + semantics]**.
- Dependence speculation across those ports (LSQ-style out-of-order issue with in-order commit per dependency edge) is Dynamatic's published answer to irregular memory **[MODEL: consistent with README claims and the paper lineage cited in LATTE §2; specific LSQ RTL not fetched]**.

### 2.7 MLIR experience report — lessons for QUIL's substrate choice

From the LATTE'26 self-assessment (all **[PROVEN: arXiv 2603.19856 §4]**):

1. **MLIR values cannot carry attributes** — no edge annotations. Memory dependence distances and branch profile counts had to be smuggled into node attributes (`handshake.deps = #[["load2", 1]]`) or external CSV files. *QUIL consequence: `bind`/`link` being first-class syntactic edges with their own attributes (`fanout`, `arrive`) is not syntax sugar — it is the fix for a limitation the Dynamatic team documents as a persistent tax.*
2. **SSA block arguments are awkward circuit muxes** — φ-lowering needs function-wide rewrites instead of local pattern matches. *QUIL consequence: keep `merge`-like joins explicit in the grammar (a QUIL view-of-several-journals is a structural read, never a hidden φ).*
3. **Cross-repo dialect versioning is fragile** (Dynamatic↔XLS translation at risk of rotting); the C frontend still leans on LLVM IR for optimization strength. *QUIL consequence: the scout report's "define QUIL as a CIRCT dialect long-run" recommendation stands, but with lowered expectations about free pass reuse — quilc's four passes (RFC §2) should stay small and self-contained.*

---

## 3. Mapping onto the quilt round-19 family

### 3.1 Mechanism-by-mechanism correspondence

| Round-19 mechanism (RFC §1.4) | Calyx equivalent | Dynamatic/handshake equivalent | Notes |
|---|---|---|---|
| **queue cell** (intermediate cell buffers the value in its own journal) | a `std_reg` stage written by one group, read by the next control step; or `std_bypass_reg`/`std_skid_buffer` from the stdlib | `handshake.buffer {slots=1, bufferType=seq, initValues=[entry0]}` on the edge | seq buffers break combinational paths — matches "one journal entry deep" register stage in L2. Nontransparent = journaled. **[MODEL]** |
| **credit fence** (receiver holds a credit token; delivery gated on token presence) | guarded assignment whose guard is a credit-counter register ≠ 0 (guards are the native gating mechanism) | `ready` driven by a credit/occupancy condition; the `load`/`store` ctrl-token gate is the canonical instance; `lazy_fork` is the barrier flavor | Calyx guard rule ("only one guard active per cycle") plays the role of the conservation check. **[MODEL]** |
| **staged grant** (multi-cycle handoff; writer journals a grant, reader's tick consumes it) | the **go-done interface itself**: `go` held until `done`, one-sided ready-valid, ≥1-cycle components; group enable + done hole is the intra-component version | a 2-phase valid/ready handoff across a `seq` buffer plus a completion token fed back (a `join` of receiver tokens re-triggers the producer) | Calyx proves the convention at scale (every component, every primitive). **[MODEL]** |

### 3.2 Construct-by-construct lowering table

| QUIL construct (RFC §1) | Calyx shape | Handshake-dialect shape |
|---|---|---|
| `cell` + fields | `std_reg` cells (PW wide) | stateful units + `buffer`s carrying `initValues` |
| `tick` | one `go` pulse driving a `seq` of group enables; `repeat n` for static trip counts | one token entering the func; `join` of all effect tokens = tick complete |
| `view` (pure fn of journal prefix) | continuous assignment / `comb group with` — *structural read, no handshake* | no 1:1 op — dataflow is eager; views are QUIL's structural half that Calyx shares and Dynamatic lacks. **[MODEL]** |
| `bind` (fanout = n, arrive = m) | `par` of n guarded writes, or n `invoke`s of reader components | `handshake.fork [n]` (+ per-mechanism buffers/gates per §3.1) |
| `link` (symmetric gap kind) | two opposing continuous-assignment reads, single-writer each way | two opposing channels; `merge`/`join` discipline if symmetric tick alignment is needed |
| `propose` (black box) | input port on the component (integer width) | `handshake.source`-fed input channel / ESI instance port |
| conservation ledger D4 | *no Calyx equivalent* — dropped writes are silent | *no handshake equivalent* — `sink` "discards any data," unaccounted |
| journal (append-only history) | *no equivalent* (state is registers, history is gone) | *no equivalent* (tokens are consumed) |

Last three rows **[MODEL]** — and they are the differentiator row: everything QUIL borrows, both stacks already do well; the journal, the view-of-prefix, and the delivery ledger are the parts with no external precedent. That matches the scout verdict: "QUIL's differentiator remains the one thing none of them have: the journal as the lowering artifact."

### 3.3 Observational equivalence, stated in their vocabulary

- QUIL's law "all three mechanisms are observationally equivalent in simulation; they differ only in area/latency after synthesis" (RFC §1.4) corresponds to the elastic-circuits property that **buffer insertion is functionally neutral** — `handshake.buffer` with any `slots ≥ 1` preserves the dataflow function (the dialect's slot/init semantics are PROVEN; functional-neutrality-under-insertion as a *stated theorem* is **[MODEL]** here — it is the standard elastic-circuits correctness argument and should be re-cited from the elastic-systems literature when the implementation lane lands).
- Calyx's matching property: `seq`/`par` deliberately give *no* cycle-level guarantees, so any legal FSM schedule the compiler emits is a valid refinement — the same "netlist shape is a cost-model choice" posture. **[MODEL: from the PROVEN no-guarantee clauses]**

---

## 4. Worked example — a 3-fanout bind, lowered both ways

### 4.0 The QUIL source

```
cell src { int<PW> v = 7; }
cell a   { int<PW> s = 0; }
cell b   { int<PW> s = 0; }
cell c   { int<PW> s = 0; }

view val(src.v) -> int<PW> { src.v }

bind val -> a, b, c    fanout = 3    arrive = queue_cell;

tick {
  a.s <= val + 1;
  b.s <= val + 2;
  c.s <= val + 3;
}
```

### 4.1 Calyx lowering

```calyx
component main(@go go: 1, @clk clk: 1, @reset reset: 1) -> (@done done: 1) {
  cells {
    r_src = std_reg(PW);
    ra = std_reg(PW);  rb = std_reg(PW);  rc = std_reg(PW);
    k1 = std_const(PW, 1);  k2 = std_const(PW, 2);  k3 = std_const(PW, 3);
    a1 = std_add(PW);  a2 = std_add(PW);  a3 = std_add(PW);
  }
  wires {
    // continuous structural reads: the `view`
    a1.left = r_src.out;  a1.right = k1.out;
    a2.left = r_src.out;  a2.right = k2.out;
    a3.left = r_src.out;  a3.right = k3.out;

    // queue-cell arrival: an explicit register stage per receiver (arrive = queue_cell)
    group w_qa { qa.in = a1.out; qa.write_en = 1'd1; w_qa[done] = qa.done; }
    group w_qb { qb.in = a2.out; qb.write_en = 1'd1; w_qb[done] = qb.done; }
    group w_qc { qc.in = a3.out; qc.write_en = 1'd1; w_qc[done] = qc.done; }
    group w_a  { ra.in = qa.out; ra.write_en = 1'd1; w_a[done]  = ra.done; }
    group w_b  { rb.in = qb.out; rb.write_en = 1'd1; w_b[done]  = rb.done; }
    group w_c  { rc.in = qc.out; rc.write_en = 1'd1; w_c[done]  = rc.done; }
  }
  control {
    seq { par { w_qa; w_qb; w_qc; } par { w_a; w_b; w_c; } }
  }
}
```

*(Sketch. `qa/qb/qc` are additional `std_reg` cells — the queue cells. Syntax follows the reference; exactness of idiom is **[MODEL]**, construct semantics are all §1-PROVEN.)*

**Cycle walkthrough (staged, arrive = queue_cell):**

| Cycle | go | active groups | what holds | done holes |
|---|---|---|---|---|
| 0 | 1 (held) | `w_qa ∥ w_qb ∥ w_qc` (par) | each group's guarded writes active; register `done` outputs are the hold condition | all three queue regs raise `done` |
| 1 | 1 | `w_a ∥ w_b ∥ w_c` | same, consumers of the queue stage | `ra/rb/rc.done` |
| 2 | 1 | — | control program finished | component `done` = 1; harness may drop `go` |

Fan-out is structural: one source register read continuously by three adders — Calyx's answer to `fanout = 3` is *replicated readers plus per-reader groups*, and `par` explicitly refuses to promise the three writes fire the same cycle (they do here only because each is one cycle — **[MODEL]**).

With `arrive = staged_grant`, the same skeleton replaces queue registers with go-done sub-components (`invoke`) whose `done` the writer waits on; with `arrive = credit_fence`, the guards become `credit != 0 ? …` — the mechanism choice changes only wires, never the trace, exactly as RFC §1.4 promises. **[MODEL]**

### 4.2 Dynamatic lowering (handshake dialect)

```mlir
handshake.func @fanout3(%v: i32, %ctrl: none) -> (i32, i32, i32, none) {
  %v0, %v1, %v2 = handshake.fork [3] %v : i32          // the bind: fanout = 3
  %va = arith.addi %v0, %c1 : i32                      // a.s <= v+1
  %vb = arith.addi %v1, %c2 : i32
  %vc = arith.addi %v2, %c3 : i32
  %ja = handshake.buffer {slots = 1, bufferType = seq} %va : i32   // arrive = queue_cell
  %jb = handshake.buffer {slots = 1, bufferType = seq} %vb : i32
  %jc = handshake.buffer {slots = 1, bufferType = seq} %vc : i32
  %j = handshake.join %ja, %jb, %jc : i32, i32, i32     // tick complete
  handshake.return %ja, %jb, %jc, %j : i32, i32, i32, none
}
```

*(Sketch — op syntax per §2.4-PROVEN; the composition is **[MODEL]].* For the other mechanisms: swap `fork` → `lazy_fork` for the barrier flavor of `credit_fence`; for `staged_grant`, feed each consumer's completion token back through the producer's control input (the `load`-style ctrl-token pattern of §2.4).

**Channel-level timing (one channel, queue-cell arrival):**

| Cycle | producer.valid | payload | buffer.ready(in) | buffer.valid(out) | consumer.ready | event |
|---|---|---|---|---|---|---|
| 0 | 1 | v+1 | 0 (busy) | 0 | 0 | token waits; producer must hold valid+data |
| 1 | 1 | v+1 | 1 | 0 | 0 | **transfer into buffer** (rising edge, v∧r) |
| 2 | — (producer free) | — | — | 1 | 0 | buffer presents token; consumer not ready |
| 3 | — | — | — | 1 | 1 | **transfer out**; buffer empty again |

Rules exercised: sticky `valid`, free `ready`, payload stability under backpressure, nontransparent `seq` behavior isolating producer from consumer timing **[PROVEN rules per §2.3; application MODEL]**. Note the reader never observes *when* the writer produced — only that exactly one token arrived: the observational-equivalence law in wire form.

### 4.3 What the example teaches

1. **Calyx lowers fan-out by reader replication + control scheduling; Dynamatic lowers it by an explicit `fork` unit.** QUIL's `bind` sits exactly between: syntactic like `fork`, structural like Calyx's reads. **[MODEL]**
2. **The queue cell has a byte-exact external twin** (`seq` 1-slot buffer with reset init) — quilc's L2 "extra register stage (one journal entry deep)" can be *defined* as `handshake.buffer{slots=1,seq}` semantics so the netlist-level correspondence is testable. **[MODEL]**
3. **Credit fences and staged grants are compositions, not primitives** in both stacks (guard + counter; go-done + token feedback) — QUIL is right to make them first-class `arrive =` choices, because both stacks express them only implicitly. **[MODEL]**
4. Neither stack journals the delivery: Calyx's `done` and Dynamatic's token handshake vanish after the cycle; QUIL's conservation ledger (D4) and journal entries are additive and must be asserted in the testbench layer, per RFC L2. **[MODEL]**

---

## 5. Verdict — adopt verbatim vs reinvent

### 5.1 Adopt verbatim (with source pinned)

| Adopt | From | Why | Cost |
|---|---|---|---|
| **valid/ready two-signal channel** as quilc's canonical netlist-level arrival wire contract | elastic/Dynamatic (§2.3) | industrial-standard (AXI-Stream-compatible), proves backpressure-correct; makes QUIL netlists externally interfaceable | near zero — it is a wire convention |
| **`buffer{slots, seq\|fifo, initValues}` semantics** as the definition of the queue cell's RTL shape (`seq` only may init ≙ journal entry 0 privilege) | CIRCT handshake dialect (§2.4) | gives the round-19 queue cell a tested external spec instead of a house-only one | low |
| **go-done one-sided handshake** as the staged-grant module boundary convention (`go` held to `done`, UB otherwise) | Calyx (§1.5) | the exact "writer journals a grant, reader's tick consumes" shape at module granularity; proven at scale | low |
| **fork vs lazy_fork distinction** as the two fan-out disciplines (`arrive` mechanisms must declare which skew law they obey) | CIRCT handshake dialect (§2.4, §2.5) | names the round-19 fan-out wall; prevents silent mixing of eager and barrier arrivals on one bind | grammar note |
| **memory port accounting `[ld=N, st=M]` + completion tokens** for any future QUIL memory cells | CIRCT handshake dialect (§2.4) | structural fan-out accounting for memories, with a built-in credit-gate idiom | when memories enter the grammar |
| **port-attribute metadata** (`@go`, `@done`, `@write_together`, `@interval`, `@stable`) on lowering-side interfaces | Calyx core.futil (§1.5) | the well-formedness checks QUIL's L2 needs (single active writer per port per cycle) already have a proven attribute vocabulary | low |

### 5.2 Reinvent (no adequate external precedent)

| Reinvent | Why not adoptable |
|---|---|
| **journal + view-of-prefix** | neither stack has history; Calyx state is registers, Dynamatic tokens are consumed. This is the differentiator (scout verdict). |
| **`tick` as the only writer / parse-error cycle rejection** | Calyx explicitly *allows* multi-group writes to one port across groups; QUIL is deliberately stricter (SPIN-19 law). |
| **conservation ledger (D4)** | `sink` discards silently; Calyx drops nothing because it writes nothing implicitly. Delivery-or-drop-with-entry accounting is QUIL-only. |
| **PW floor derivation + trace-hash width invariance** | no external analog found in either stack (SPIN-34 discipline stands alone). |
| **`propose` grammatical quarantine** | external stacks have no neural-side boundary at all; Axiom-style verify-rollback is the companion law (scout report), not a substitute. |

### 5.3 Explicitly careful / reject for now

- **Full elasticity (runtime-adaptive scheduling) as QUIL semantics — reject.** Backpressured elastic cycles can deadlock and their completion times are data-dependent; QUIL's fixed-tick, replay-exact envelope sidesteps both. Elasticity remains a *cost-model* luxury inside one tick, never a language guarantee. **[SPECULATED]** — reasoning from the sticky-valid rule (§2.3) plus QUIL's D5 replay law; no external counter-evidence sought yet.
- **MLIR as near-term substrate — defer.** LATTE'26 documents the edge-annotation, φ-lowering, and version-pinning taxes (§2.7). Keep quilc's four passes self-contained; revisit CIRCT residency when a second backend demands it (matches the scout's long-run recommendation, with expectations lowered). **[MODEL]**

### 5.4 RFC amendments this feeds

1. **§1.4 (arrival):** pin each mechanism to its external twin — `queue_cell ≙ handshake.buffer{slots=1,seq,initValues}`, `credit_fence ≙ guarded/ready-gated delivery (load-ctrl-token idiom)`, `staged_grant ≙ go-done handshake`; add the fork/lazy-fork skew-law note to the `bind` grammar.
2. **§2.2 (L2):** define the emitted wire contract as valid/ready channels; adopt the Calyx port-attribute vocabulary for the single-writer checks; keep D4 assertions testbench-side (unchanged).
3. **§4 (open questions):** book "elastic buffer insertion is functionally neutral" as a claim to re-cite from the elastic-systems literature before the implementation lane leans on it (currently MODEL).

---

## 6. Sources (fetched 2026-09-04, AKDT)

| # | Source | What it proved |
|---|---|---|
| S1 | Calyx Language Reference — https://docs.calyxir.org/lang/ref.html | groups/done holes, guards, control ops + non-guarantees, go-done interface & UB rule, ref cells, comb groups |
| S2 | Interfacing with Calyx RTL — https://docs.calyxir.org/running-calyx/interfacing.html | top-level reset→go→done harness contract |
| S3 | Calyx homepage — https://www.calyxir.org/ | cells/wires/control anatomy, frontend ecosystem |
| S4 | Calyx ASPLOS'21 — https://arxiv.org/abs/2102.09713 | structural+control split, FSM lowering, systolic-array results |
| S5 | Calyx stdlib core.futil — https://raw.githubusercontent.com/calyxir/calyx/master/primitives/core.futil | `std_reg` port attributes; `std_skid_buffer` (i/o valid+ready); `std_bypass_reg` |
| S6 | CIRCT Handshake Dialect Rationale — https://circt.llvm.org/docs/Dialects/Handshake/RationaleHandshake/ | FIFO-channel principle; full op catalog incl. fork/lazy_fork/buffer/merge/join/sink/load/store/memory semantics |
| S7 | Dynamatic repo README — https://github.com/EPFL-LAP/dynamatic | scope, targets, MLIR flow |
| S8 | Dynamatic docs intro — https://epfl-lap.github.io/dynamatic/ | docs/tutorial map |
| S9 | LATTE'26 MLIR-experience paper — https://arxiv.org/abs/2603.19856 (HTML v1 fetched) | elastic dataflow model verbatim, lineage, edge-annotation/φ/versioning lessons, XLS translation |
| S10 | valid/ready protocol references — https://fpgacpu.ca/fpga/handshake.html ; https://24x7fpga.com/rtl_directory/2024_11_29_18_17_10_valid_ready_protocol/ | standard transfer rules (sticky valid, free ready, v∧r edge) |

Fleet-internal: `docs/QUIL-HLS-RFC.md` (grammar, round-19 family, L2, D-laws), `docs/CUTTING-EDGE-SCOUTS-2026-09-04.md` (scout framing), quilt-verilog `wheel/SPIN-19-rtl-honesty.md` (label discipline lineage).

---

*The round-19 family was right; Calyx and Dynamatic prove it in production grammar. What neither has is the journal — adopt their wires, keep our ledger.*
