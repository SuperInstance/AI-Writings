# QUIL v0.1 — Language Specification (Grammar and Static Semantics)

**Status:** v0.1 spec · **Date:** 2026-09-04
**Authority:** formalizes `docs/QUIL-HLS-RFC.md` §1 (grammar) and §2 (lowering preconditions). Where this doc and the RFC disagree, the RFC wins and the disagreement is a bug in this doc.
**Home:** this doc (ai-writings). Implementation lands in quilt-verilog when a builder lane picks it up (Two-Division Wheel: ideators feed builders).
**Companion vocab:** every keyword is anchored to quilt-verilog `docs/QUIL-VOCAB.md` in Appendix A.

QUIL = Quilt Intermediate Language: an HLS pseudolanguage that lowers to synthesizable Verilog within quilt paradigms. The design thesis (inherited from NQ-C3): *a deterministic cell subgraph compiles to a hardware netlist, bit-exact against its reference* — and determinism is a **lowering artifact**: "The grammar cannot express a nondeterminism" (RFC §0).

Normative language: **must** / **must not** are conformance requirements on any QUIL compiler (`quilc`). A conforming compiler rejects every program flagged by a Q-code below and accepts every program that violates none.

---

## 1. Lexical conventions

- Identifiers: `letter (letter | digit | "_")`.
- Integer literals: decimal only (`0`–`9`+). **There is no float literal** (S6, Q0300).
- Comments: `//` to end of line; `/* … */` non-nesting.
- Reserved words (cannot be identifiers): `cell int view bind link tick propose forget for in journal fanout arrive kind gap queue_cell credit_fence staged_grant external port epoch seal hmac_sha256 const sat min max abs head` — plus the **reserved-but-undefined** names `now clock time net socket http float` (S6: the determinism boundary is "the absence of vocabulary", RFC §1.5).
- Operators/punctuation: `<= -> <-> < > = ; , { } ( ) [ ] . .. ? : + - * / >> << == != <= >= < > && || - ~` (context disambiguates `<=` effect arrow from `<=` relational; `>` from `->`).
- QUIL is whitespace-insensitive; programs are elaborated top-to-bottom; declarations must precede use.

## 2. Notation

EBNF per ISO/IEC 14977: `=` defines, `|` alternates, `{x}` zero-or-more, `[x]` optional, `( )` grouping, `"…"` terminals, `;` ends a production. Comments after `--` are informative.

## 3. Grammar

```ebnf
program        = { top_level } ;

top_level      = const_decl | cell_decl | view_decl | bind_decl | link_decl
               | propose_decl | forget_decl | tick_block | for_stmt ;

(* ---- state ---- *)
const_decl     = "const" identifier "=" integer_literal ";" ;
cell_decl      = "cell" identifier "{" { field_decl } "}" ;
field_decl     = "int" "<" width_expr ">" identifier [ "=" integer_literal ] ";" ;
width_expr     = "PW" | integer_literal ;                 (* parametric or pinned *)

(* ---- derived reads ---- *)
view_decl      = "view" identifier "(" formal { "," formal } ")"
                 "->" "int" "<" width_expr ">" "{" expr "}" ;
formal         = identifier ;                              (* binds a journal source at call *)

(* ---- edges ---- *)
bind_decl      = "bind" identifier "->" identifier { "," identifier }
                 "fanout" "=" integer_literal "arrive" "=" arrive_mech ";" ;
arrive_mech    = "queue_cell" | "credit_fence" | "staged_grant" ;
link_decl      = "link" identifier "<->" identifier "kind" "=" link_kind ";" ;
link_kind      = "gap" ;

(* ---- neural boundary ---- *)
propose_decl   = "propose" identifier "{" { port_decl } "}" ;
port_decl      = "external" "port" "int" "<" width_expr ">" identifier ";" ;

(* ---- time ---- *)
tick_block     = "tick" "{" { effect } "}" ;
effect         = lhs "<=" expr ";" ;                       (* the only write form *)
lhs            = identifier "." identifier ;               (* cell.field *)

(* ---- epochs ---- *)
forget_decl    = "forget" identifier "epoch" "=" integer_literal
                 "seal" "=" seal_alg ";" ;
seal_alg       = "hmac_sha256" ;                           (* only algo defined, v0.1 *)

(* ---- loops ---- *)
for_stmt       = "for" identifier "in" iter_domain
                 "{" { tick_block | for_stmt } "}" ;
iter_domain    = static_range | journal_range ;
static_range   = integer_literal ".." "<" integer_literal ;        (* half-open *)
journal_range  = "journal" "(" identifier ")" [ "bound" "=" integer_literal ] ;

(* ---- expressions ---- *)
expr           = cond_expr ;
cond_expr      = or_expr [ "?" expr ":" cond_expr ] ;
or_expr        = and_expr { "||" and_expr } ;
and_expr       = rel_expr { "&&" rel_expr } ;
rel_expr       = add_expr { rel_op add_expr } ;
rel_op         = "==" | "!=" | "<" | "<=" | ">" | ">=" ;
add_expr       = mul_expr { ("+" | "-") mul_expr } ;
mul_expr       = shift_expr { ("*" | "/") shift_expr } ;
shift_expr     = unary { (">>" | "<<") unary } ;
unary          = [ "-" | "~" ] primary ;
primary        = integer_literal
               | identifier                                  (* const, formal, or propose.port *)
               | identifier "." identifier                   (* propose port field *)
               | identifier "(" call_arg { "," call_arg } ")" (* view call *)
               | "journal" "(" identifier ")" [ "[" expr "]" ]
               | "head" "(" identifier "." identifier ")"
               | builtin_call
               | "(" expr ")" ;
call_arg       = identifier "." identifier ;                 (* cell.field journal source *)
builtin_call   = ( "sat" | "min" | "max" | "abs" ) "(" expr { "," expr } ")" ;
```

**Semantic reading of the journal primitives (normative):**

- `journal(C.f)[k]` — entry `k` of cell `C`'s field `f`: index 0 is the declared initializer (journal entry 0); index `k ≥ 1` is the value after tick `k`. Negative `k` counts back from the current prefix end (`[-1]` = value at start of the current tick). A view or tick body only ever sees a **prefix**; there is no other way to name state.
- `head(C.f)` — `journal(C.f)[-1]`, the old value at the moment a tick computes (RFC §1.2: "a cell's new value is a pure function of (its old value, the views it reads, black-box inputs)").
- View bodies may reference formals (via `journal(<formal>)`), consts, and view calls — nothing else (S5/Q0201).
- `sat(…)` — single saturation from an exact wider sum, order-free (NQ-C3 rule, RFC §2.3: "single saturation from exact wider sums… No floats anywhere in lowering").

**Helm region.** Everything except `propose_decl` (and the port references it introduces) is the *helm region* — deterministic control: cells, views, binds, links, ticks, loops, forgets. `propose` regions are black-box input ports and nothing more (RFC §1.5).

## 4. Static semantics

Each rule: **Statement** (numbered S1…), **Encodes** (the RFC / wheel fact it is the parse-level form of, quoted), **Diagnostics** (Q-code, message, offending example). All diagnostics are compile-time rejects — "Any violation is a compile error — before any Verilog exists" (RFC §2.1).

### S1 — Single writer per field per tick

**Statement.** Within one `tick` block, at most one `effect` may target any given `cell.field`; every `effect` lowers to exactly one journal entry appended to that field's diff history.

**Encodes.** RFC §1.2: "Single-writer per cell per tick, and `tick` is the only writer, period. Every effect assignment (`dest <= expr` inside a `tick` block) lowers to exactly one **journal entry**…" — the parse-level form of D5 (append-only diff history): "replaying journal entries 1..k reproduces the fabric bit-for-bit (D5) *because there is no other place state could have come from*."

**Diagnostics.**
- **Q0100** `duplicate effect target 'C.f' in tick` —

```
tick { AVM.acc <= head(AVM.acc) + 1;  AVM.acc <= 0; }   // two writers, one field
```

### S2 — `tick` is the only writer

**Statement.** No production other than `effect` mutates state. Initial values exist only as field initializers (journal entry 0); `forget` is an epoch-boundary archive event, not a tick writer. A write token (`<=`) outside a `tick` block is rejected.

**Encodes.** RFC §1.2: "Nothing outside `tick` writes anything." And L4: "no `initial` state beyond journal entry 0."

**Diagnostics.**
- **Q0110** `write outside tick block` —

```
AVM.acc <= 5;                       // top-level effect: not grammatical, rejected
```

*(Grammar-excluded; `quilc` and any tolerant parser must still emit Q0110 rather than silently accept.)*

### S3 — No same-tick dependency cycles

**Statement.** The elaborated per-tick dependency graph (effects and the journal-prefix reads they consume, after arrival mechanisms materialize) must be acyclic. No assignment may read another assignment's same-tick result.

**Encodes.** RFC §1.2: "No assignment in a tick may read another assignment's *same-tick* result — the compiler rejects the cycle. This is SPIN-19's lesson made a *parse error*: the non-blocking last-write-wins mass-counter bug … is a bug class QUIL makes inexpressible. You cannot write the bug, so it cannot ship." Checked at L1: "cycle-freedom within ticks" (RFC §2.1).

**Diagnostics.**
- **Q0120** `same-tick cycle through 'C.f'` —

```
tick {                                   // if arrive = credit_fence is pre-charged,
  AVM.acc <= head(AVBL.acc) + 1;         // these two reads alias same-tick results
  AVBL.acc <= head(AVM.acc) + 1;         // → cycle in the elaborated tick graph
}
```

*(With `journal()`/`head()` semantics a same-tick read is unnameable at source; Q0120 fires on the elaborated graph, including arrival-mechanism-induced zero-delay paths.)*

### S4 — Cross-cell reads only via views / journal

**Statement.** A tick expression or field initializer may reference constants and journal prefixes, but never another cell's raw state except through a declared `view` or an explicit `journal(C.f)` read.

**Encodes.** RFC §1.1: "A cell may reference constants and the journal (§1.3) but never another cell's raw state — only views of it."

**Diagnostics.**
- **Q0130** `raw cross-cell read of 'C.f'` — *(fires for extensions/tools that introduce field references outside `journal()`/`head()`/view calls; core grammar makes it unnameable.)*

### S5 — View purity

**Statement.** A view is a pure, total function of a prefix of the journal. View bodies contain only: formals read via `journal(<formal>)`, `head(<formal>)` is not permitted (views read declared prefixes, not the mutable head — tick bodies only), consts, literals, builtins, and view calls. No effects, no propose ports, no free cell references.

**Encodes.** RFC §1.3: "A view is a pure, total function of a **prefix of the journal** — never of 'current state' as a mutable thing. It is replay-exact by construction: same prefix in, same value out, no side channels." And the shadow contract, QUIL-VOCAB §5c: "`qm_view` = shadow (read-only)".

**Diagnostics.**
- **Q0200** `propose port 'P.x' referenced in view 'V'` (RFC §1.5: propose "never in a view") —

```
view v(src) -> int<PW> { journal(src)[-1] + poke.poke_strength }
```

- **Q0201** `view 'V' references undeclared state 'C.f'` (free variable capture) —

```
view v(src) -> int<PW> { journal(src)[-1] + head(AVM.acc) }   // AVM.acc not a formal
```

### S6 — Helm-region vocabulary closure (no float / no wall-clock / no net)

**Statement.** The language has no float literal, no clock-reading primitive, and no network primitive. The reserved-but-undefined names (`now clock time net socket http float`) are rejected wherever they appear; every value in the helm region is `int<PW>`, a constant, a journal-derived value, or a black-box input *as an integer*.

**Encodes.** RFC §1.5: "No floats, no wall-clock, no nets inside the helm region — **grammatically**. … The language has no float literal, no clock-reading primitive, no network primitive for helm code to even name. The determinism boundary is not a convention here; it is the absence of vocabulary." Also the fleet law in QUIL-VOCAB §3c: "Writer refuses f32/f64 (no floats in fleet state)."

**Diagnostics.**
- **Q0300** `float literal` —

```
cell A { int<PW> x = 1.5; }          // no float literal exists; rejected at lex
```

- **Q0301** `wall-clock primitive 'now'` — `tick { A.x <= now(); }`
- **Q0302** `network primitive 'net'` — `tick { A.x <= net("peer"); }`

### S7 — Loop bound rules

**Statement.** Trip counts must be static (elaboration-time constant half-open range `a..<b`, `b ≥ a`) or journal-derived (`journal(C)`), and a journal-derived domain must resolve at elaboration against a pre-registered trace or a declared `bound =` maximum. Bounds that depend on live cell state are rejected.

**Encodes.** RFC §1.6: "Trip counts must be **static** or **derived from the journal prefix**. Data-dependent loops on live state (unbounded, un-replayable) are a parse error. This keeps elaboration finite and replay total — the two properties every downstream proof leans on." The `bound =` refinement encodes L1: "unroll journal-derived loops against a pre-registered trace or the declared maximum" (RFC §2.1; the declared-maximum story is RFC §4's booked open question — v0.1 requires it).

**Diagnostics.**
- **Q0400** `loop bound depends on live state 'C.f'` —

```
for i in 0..<head(AVM.acc) { tick }   // head() is tick-scoped; not a static bound
```

- **Q0401** `journal-derived loop over 'C' has no resolvable bound` —

```
for i in journal(AVM) { tick }        // no pre-registered trace, no bound =
```

### S8 — Fan-out declaration requirement

**Statement.** Every `bind` must declare `fanout = n` (exactly the number of listed destination cells) and `arrive =` one of the three round-19 mechanisms; the source must be a declared view, every destination a declared cell. One writer, N named readers; the conservation ledger (D4) reconciles each tick that every bound value was delivered or dropped-with-entry.

**Encodes.** RFC §1.4: "Every edge declares its **fan-out** at bind time. One writer, N named readers — the conservation ledger (D4) reconciles each tick that every bound value was delivered or dropped-with-entry." Arrival is a synthesis-time choice from the round-19 mechanism family (queue cell / credit fence / staged grant), all observational-equivalent in simulation.

**Diagnostics.**
- **Q0500** `bind 'b' missing fanout or arrive` —

```
bind avm_out -> avbl, avbr;                  // no fanout =, no arrive =
```

- **Q0501** `fanout 3 does not match 4 destinations` —

```
bind avm_out -> avbl, avbr, pvcl, pvcr fanout = 3 arrive = queue_cell;
```

- **Q0502** `bind source 'avm_out' is not a declared view`
- **Q0503** `bind destination 'avbl' is not a declared cell`

### S9 — Propose quarantine (the neural side never gates)

**Statement.** A propose port reference may appear **only** as the branch of a conditional expression inside a tick body, where the condition is propose-free and deterministic (thresholds, credits, journal tests). It must never appear in a view (Q0200), in any arrival-fence or bind/link condition, as a write enable, or unguarded.

**Encodes.** RFC §1.5: "It *suggests*; it never gates. `propose` output may only appear inside `tick` expressions guarded by deterministic conditions (thresholds, credits) — it can never appear in a view, never in an arrival-fence condition, never as a write enable." House law behind it (RFC §0): "byte-exact fabric work never passes through LLM inference (Two-Division Wheel, 'rules carried'). QUIL makes that boundary *syntactic*."

**Diagnostics.**
- **Q0600** `propose port 'P.x' in arrival-fence condition` — *(fires on extension syntax; core grammar has no fence conditions to write)*
- **Q0601** `unguarded propose reference 'P.x' in tick` —

```
tick { AVM.acc <= head(AVM.acc) + poke.poke_strength; }        // no deterministic guard
```

- **Q0603** `propose value 'P.x' used as write enable` —

```
tick { (poke.poke_strength > 0 ? AVM.acc : AVM.acc) <= 1; }    // guard carries the proposal
```

### S10 — PW parametricity and width discipline

**Statement.** `PW` is a parameter; the compiler derives the floor `PW_min` (worst-case journal-derivable magnitude over the longest loop, saturation policy, arrival counters) and (a) refuses pinned widths below the floor, (b) refuses designs whose floor cannot be established (unbounded growth — no silent wrap, ever), and (c) requires trace-hash invariance: the design simulated at two legal widths must emit identical trace hashes. The same source must be bit-exact across all legal PW.

**Encodes.** RFC §1.1: "the *same source* must be bit-exact across all legal PW." RFC §1.3: "Trace-hash PW-invariance is a compiler check, not a hope." RFC §2.3: booked anchor "bit-exactness held **down to PW = 41**" (SPIN-34), and the corpse finding — "the step5_off-style reference that explodes to ~10^600 while a fixed-width datapath wraps … **do not lower**; the compiler names the cell and refuses. No silent wrap, ever."

**Diagnostics.**
- **Q0700** `pinned width 12 below derived floor 41 for 'C.f'` — `cell C { int<12> acc = 0; }`
- **Q0701** `no derivable PW floor: unbounded growth at 'C.acc'` — *(the ~10^600 corpse class; compiler names the cell and refuses to lower)*
- **Q0702** `trace-hash mismatch across legal PW (41 vs 64)` — *(design's observable behavior is width-dependent; rejected at compile time, "not discovered in cosim")*

### S11 — Forget is an epoch archive, not a delete

**Statement.** `forget C epoch = N seal = hmac_sha256;` is valid only at top level; it archives cell `C`'s journal prefix into epoch section `epoch.<N>` (sealed, custody-manifested), resets `C`'s fields to their journal-entry-0 values, and starts a fresh journal. Per cell: epoch numbers strictly increase, and at most one live archive may exist (the next `forget` seals the previous). The seal algorithm must be the one defined (`hmac_sha256`, algo_id 1).

**Encodes.** QUIL-VOCAB §1: `qm_forget` — "The sixth verb" — epoch-archive forget (docs/QUF-FORGETTING-V1.md:230; docs-only in the RTL opcode map, sibling quilt-mhs tier adds it). Epoch reject semantics from QUF-FORGETTING-V1 §4.2: "multiple live epochs" and seal "mismatch fail-closed" are E-coded fabric-side; QUIL makes them parse-level. The no-delete doctrine (QUIL-VOCAB §5a: "Orphaned lane artifacts are left in place, never deleted") is why QUIL's forget *archives first* — it is an archive-and-reset, never a discard.

**Diagnostics.**
- **Q0800** `forget inside tick` — `tick { forget AVM epoch = 1 seal = hmac_sha256; }` *(not grammatical; tolerant parsers must reject with Q0800)*
- **Q0801** `epoch 2 not greater than previous archive epoch 5 for 'AVM'`
- **Q0802** `second live archive for 'AVM' (multiple live epochs)`
- **Q0803** `unknown seal algorithm` — `forget AVM epoch = 1 seal = md5;`

### Diagnostics index

| Code | Rule | Short message |
|---|---|---|
| Q0100 | S1 | duplicate effect target in tick |
| Q0110 | S2 | write outside tick block |
| Q0120 | S3 | same-tick dependency cycle |
| Q0130 | S4 | raw cross-cell state read |
| Q0200 | S5 | propose port in view |
| Q0201 | S5 | view references undeclared state |
| Q0300 | S6 | float literal |
| Q0301 | S6 | wall-clock primitive |
| Q0302 | S6 | network primitive |
| Q0400 | S7 | loop bound depends on live state |
| Q0401 | S7 | journal loop without resolvable bound |
| Q0500 | S8 | bind missing fanout/arrive |
| Q0501 | S8 | fanout ≠ destination count |
| Q0502 | S8 | bind source not a view |
| Q0503 | S8 | bind destination not a cell |
| Q0600 | S9 | propose in fence condition |
| Q0601 | S9 | unguarded propose in tick |
| Q0603 | S9 | propose as write enable |
| Q0700 | S10 | pinned width below floor |
| Q0701 | S10 | no derivable floor (unbounded growth) |
| Q0702 | S10 | trace-hash mismatch across PW |
| Q0800 | S11 | forget inside tick |
| Q0801 | S11 | epoch number not increasing |
| Q0802 | S11 | multiple live epochs |
| Q0803 | S11 | unknown seal algorithm |

## 5. Worked examples (one per construct)

All examples are drawn from the acceptance demo target — the NQ-C3 *C. elegans* anterior touch-arc (RFC §3) — so every construct is shown lowering something already proven by hand. `TH_*` and `W_*` are `const`s; `PW` is parametric.

### 5.1 `cell`

```quil
cell AVM  { int<PW> acc = 0; int<PW> refr = 0; }
cell AVBL { int<PW> acc = 0; int<PW> refr = 0; }
```

All state lives in cells; cells are the only things that *have* state (RFC §1.1). Lowers (L2) to a PW-bit register per field, initialized to journal entry 0.

### 5.2 `int<PW>`

```quil
cell DB02 { int<PW> acc = 0; }     // parametric: bit-exact for every PW ≥ derived floor
cell DBG  { int<16> acc = 0; }     // pinned: rejected (Q0700) if floor exceeds 16
```

The only data type. No floats, no strings, no pointers. The compiler derives the floor (S10); for the reference design family the booked floor is PW = 41 with the hand-build's 16-bit accumulators expected *above* the floor, not at it (RFC §3.3).

### 5.3 `bind`

```quil
view avm_out(src) -> int<PW> { journal(src)[-1] >= TH_AVM ? W_AVM : 0 }

bind avm_out -> AVBL, AVBR, PVCL, PVCR  fanout = 4  arrive = queue_cell;
```

One writer, four named readers, fan-out declared at bind time (S8); the conservation ledger reconciles delivery or drop-with-entry each tick. `arrive = queue_cell` materializes as one extra register stage (one journal entry deep) at L2 — switching to `credit_fence` or `staged_grant` changes only the netlist shape, never the trace.

### 5.4 `link`

```quil
link AVBL <-> AVBR  kind = gap;
```

The symmetric (gap-junction-shaped) form: both sides read a view of the other, still single-writer each way, still one journal entry per effect (RFC §1.4). Lowers to two opposing bound edges; `kind = gap` is the only link kind in v0.1.

### 5.5 `effect`

```quil
tick { AVM.acc <= sat(head(AVM.acc) - (head(AVM.acc) >> 1) + w_avm(AVBL.acc)); }
```

The `dest <= expr` form is the only write in the language. `head()` gives the old value (pure function of old value + views + inputs); `>> 1` is the half-leak; `sat()` single-saturates from the exact wider sum. Where a tick sums N inbound edges, L2 *must* emit the blocking-local accumulator feeding one non-blocking write — "the SPIN-19 fix, now emitted mechanically so no human re-introduces the bug" (RFC §2.2).

### 5.6 `view`

```quil
view w_avm(src) -> int<PW> { journal(src)[-1] >= TH_AVBL ? W_AVBL_AVm : 0 }
```

Pure function of the journal prefix — `journal(src)[-1]` is the sender's value at t−1, giving the one-tick edge delay of the touch-arc. Same prefix in, same value out, no side channels (S5). Replay-exact by construction; never reads "current state as a mutable thing."

### 5.7 `tick`

```quil
tick {
  AVM.acc  <= sat(head(AVM.acc) - (head(AVM.acc) >> 1) + w_avm(AVBL.acc) + w_avm(AVBR.acc));
  AVM.refr <= head(AVM.refr) > 0 ? head(AVM.refr) - 1 : 0;
}
```

The only writer (S1/S2); each `<=` appends exactly one journal entry per destination field. Replay of journal entries 1..k reproduces the fabric bit-for-bit *because there is no other place state could have come from* (RFC §1.2).

### 5.8 `propose`

```quil
propose poke {
  external port int<PW> poke_strength;
}

tick {
  AVM.acc <= sat(head(AVM.acc)
                 + (head(AVM.refr) == 0 ? poke.poke_strength : 0));   // guarded: refr test
}
```

The neural side lowers to an input port, nothing more (RFC §1.5). It suggests; it never gates — the proposal appears only inside the branch of a conditional whose guard (`head(AVM.refr) == 0`) is deterministic and propose-free (S9). The sensory poke of the touch-arc enters exactly this way.

### 5.9 `forget`

```quil
forget AVM epoch = 3 seal = hmac_sha256;
```

Epoch-archive forget, the sixth verb: AVM's journal prefix is sealed into `epoch.3` (HMAC-SHA256 tag under the archive key, custody manifest recording the ceremony tick), fields reset to entry-0 values, fresh journal begins (S11; QUIL-VOCAB §1 `qm_forget`, QUF-FORGETTING-V1 §2–3). Replay after a forget switches epoch prefixes — the archive remains readable, nothing is discarded.

### 5.10 Loop form (for completeness)

```quil
const TICKS = 30;

for i in 0..<TICKS { tick }                 // static trip count
for i in journal(AVM) bound = 40 { tick }   // journal-derived, declared maximum (S7)
```

## 6. Conformance summary

A `quilc` is v0.1-conformant when it:

1. Parses the grammar of §3 exactly; rejects lexical closure violations with Q03xx.
2. Enforces S1–S11 before emitting any Verilog (RFC §2.1: "Any violation is a compile error — **before any Verilog exists**").
3. Lowers per RFC §2 (L1–L4) with red/green and receipts (D1/D3), and re-verifies in the working tree per D7.
4. Produces, for the §5 worm-arc program, bit-exact traces against the NQ-C3 references on the three pre-registered traces (RFC §3.3) — the acceptance gate for the whole spec.

## 7. Open questions (inherited, booked not hidden — RFC §4)

- Multi-tick-phase designs: grammar permits several `tick` blocks per helm region; lowering untested until a second demo demands it.
- Journal-derived trip counts beyond replay traces: the `bound =` story satisfies S7 conservatively; a proven declared-maximum analysis may relax it.
- `forget` in fabric silicon: `qm_forget` is docs-only in the RTL opcode map (QUIL-VOCAB §1); the reserved opcode slot 7 (`KHASH` proposal) is the landing zone — until then, `forget` lowers to host-side epoch tooling (`quf_epoch.py`).
- Citation honesty (D2/D8): SPIN-34 (PW = 41) and the round-19 arrival-mechanism family are booked wheel facts cited from the RFC charter; when the implementation lane lands, re-point those citations at reachable docs before any claim depends on them.

## Appendix A — Keyword → QUIL-VOCAB.md anchor map

Every terminal keyword of §3, mapped to its entry in quilt-verilog `docs/QUIL-VOCAB.md` (section : term, file-of-origin). Per the citation-honesty law (D2/D8), keywords with **no vocab entry** are marked as such rather than given a stretched anchor.

| Spec keyword | Production | QUIL-VOCAB.md anchor | Notes |
|---|---|---|---|
| `cell` | `cell_decl` | §5c `cell` (docs/CULTURE-DEEP-DIVE.md:118 — "the atomic unit"); §5b `fabric` | Cell = unit of state + witness (RFC §0 table) |
| `int` | `field_decl`, `port_decl` | §3c KV value-type ids — "Writer refuses f32/f64 (no floats in fleet state)"; §5c DOCTRINE 2 "quantization IS the algorithm" | The only data type |
| `PW` (width param) | `width_expr` | §4b `CANARY-RTL-48 byte-identical` (cosim/run_spin34.sh:75–76) — PW-rebuild must reproduce trace bytes | Width-invariance canary; floor PW = 41 booked via SPIN-34 (RFC §2.3) |
| `view` | `view_decl` | §1 `OP_VIEW` / `qm_view` (rtl/q_cell_core.v:126); §1a VIEW sub-ops (act/wsum/dial); §5c `shadow vs twin (view vs effect)` | Read-only shadow contract |
| `bind` | `bind_decl` | §1 `OP_BIND` / `qm_bind` (rtl/q_cell_core.v:125) | First bind sets cell_id; QUIL's bind = the edge-declaration verb |
| `link` | `link_decl` | §1 `OP_LINK` / `qm_link` (rtl/q_cell_core.v:125) — "wiring as data" | Symmetric edge slot |
| `<=` (effect) | `effect` | §1 `OP_EFF` / `qm_effect` (rtl/q_cell_core.v:125) — `act += sat((w·dat)>>>15)`, fire-fanout egress; §5c twin (commanded write) | The only write form |
| `tick` | `tick_block` | §1 `OP_TICK` / `qm_tick` (rtl/q_cell_core.v:126); §2d `tick.period_ms` (tools/tower/emith.py) | The only writer; append-only journal (RFC D5) |
| `propose` | `propose_decl` | **no fabric opcode — deliberate** (black-box input port, RFC §1.5); nearest: §5c `LLM-as-compiler (ai cell)` (docs/CULTURE-DEEP-DIVE.md:459) | Neural side never gates |
| `forget` | `forget_decl` | §1 `qm_forget` — "The sixth verb" (docs/QUF-FORGETTING-V1.md:230; academic/GENERAL-CALCULUS.md:40–44) | Docs-only in RTL opcode map; slot 7 `KHASH` is the landing zone |
| `for` / `in` | `for_stmt`, `iter_domain` | **no vocab entry** (elaboration-level; RFC §1.6) | Honest absence |
| `journal` | `journal_range`, `primary` | §5c `QUF / "state is a file"` ("the GGUF of cell state"); §3j `created_tick` (replay/staleness anchor); §3e section names | Append-only diff history |
| `bound` | `journal_range` | **no vocab entry** (RFC §2.1 L1 "declared maximum") | v0.1 journal-loop guard |
| `fanout` | `bind_decl` | nearest: §1 `OP_EFF` "fire-fanout egress op"; the conservation ledger is RFC D4 | Round-19 family term |
| `arrive` | `bind_decl` | **no vocab entry** — RFC round-19 mechanism family (RFC §1.4) | Re-point citation when implementation lands (RFC §4) |
| `queue_cell` | `arrive_mech` | **no vocab entry** (RFC §1.4 mechanism 1) | One journal entry deep |
| `credit_fence` | `arrive_mech` | nearest: §1a `view wsum` "(+RQH credit)" (rtl/q_cell_core.v:451; q_hebb_rqh) | Credit concept's vocab anchor |
| `staged_grant` | `arrive_mech` | **no vocab entry** (RFC §1.4 mechanism 3) | Grant/ack handshake |
| `kind` | `link_decl` | **no vocab entry** (grammar marker) | |
| `gap` | `link_kind` | §3b `tap.gap` (sim/tools/tapfabric.py:594–601, producer extension key) | Gap-junction link kind |
| `external` / `port` | `port_decl` | nearest: §2d tower `io` directive (`kind: adc`, name, unit — sensory input declaration) | Black-box input ports |
| `epoch` | `forget_decl` | §3e `epoch.<N>` (docs/QUF-FORGETTING-V1.md §2.2; tools/quf_epoch.py:123); §3j `epoch_no` E4 cross-check | Archive section naming |
| `seal` | `forget_decl` | §3j `seal` (32 B trailing tag) | Fail-closed on mismatch |
| `hmac_sha256` | `seal_alg` | §3k `algo_id` = 1 = HMAC-SHA256; `QUF-EPOCH-V1\0` domain-separation prefix | Only value defined |
| `const` | `const_decl` | nearest: §3g `base` (bind-time base weight, u16) | RFC §1.1 "may reference constants" |
| `sat` | `builtin_call` | §1a `view wsum` — "saturating" (rtl/q_cell_core.v:451); §3b `quant.dials` Q1.15 | Single saturation from exact wider sums (NQ-C3) |
| `min` / `max` / `abs` | `builtin_call` | **no vocab entry** (language-internal) | |
| `head` | `primary` | **no vocab entry** (language-internal; = `journal(C.f)[-1]`) | Old-value read |
| reserved: `float` | S6 | §3c "Writer refuses f32/f64" | Absence of vocabulary, enforced |
| reserved: `now` / `clock` / `time` | S6 | **no vocab entry** (nothing to anchor — that is the point) | No clock-reading primitive |
| reserved: `net` / `socket` / `http` | S6 | **no vocab entry** (nothing to anchor) | No network primitive |

---

*QUIL: the quilt's shapes, spoken in a language that cannot lie about time.*
