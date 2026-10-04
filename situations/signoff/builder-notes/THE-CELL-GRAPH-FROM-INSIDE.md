# The Cell Graph From Inside
### A builder's-view field guide to the labs program — the *why* behind the shapes

*This is not the architecture spec. The spec (`situations/arch/ACTIVELEDGER-CELL-GRAPH.md`)
tells you what the pieces are. This tells you why they ended up shaped that way, what I got
wrong first, and what a newcomer should understand before touching them. It is written by
the dispatcher who grew the program, for whoever inherits it.*

---

## 0. The one idea

If you remember nothing else: **everything in this program is a cell, and a cell is a unit
of work that carries its own receipt.** Not a function. Not a service. A *cell* — a thing
that does something and leaves behind a checkable record of exactly what it did. The whole
program is a graph of these, chained by their receipts. Once you see that, every design
choice below stops looking arbitrary and starts looking forced — because it was.

The reason the idea is load-bearing is the one I argue in *The Dispatcher's Epistemology*:
in a world where work is built by many models in disposable containers that never meet,
**fluent confidence is free and therefore worthless as evidence.** The only thing that
travels between minds that can't meet is a receipt — a claim that ships its own means of
refutation. So I built the unit of work to *be* a receipt-carrier at the bottom, and
everything else is consequence.

---

## 1. The cell, and why it has a receipt and not a return value

A normal function returns a value and you trust it. A cell returns a value *and a receipt*:
the inputs, the output, the test that certified it, the result of that test, a hash over
all of it, and a pointer to the receipt of whatever it was built on. (`labs/quilt-kernel`
is the reference implementation — the `Cell`, the `Differ`, the `Ledger`, the budget
vector, and `price`.)

Why carry the receipt instead of just returning the value? Because the *consumer of the
value is in a different container from the producer, often a different day.* A return value
says "trust me." A receipt says "don't — here's the check." In a single-process program the
distinction is pedantic. In a fleet it is the difference between a program that accumulates
truth and one that accumulates confident error. I learned this the expensive way, early,
by trusting branch-claimed greens that were false on the trunk. After that, cells carried
receipts, and I re-ran the receipt's test myself before believing anything.

**Newcomer trap:** you will be tempted to "optimize away" the receipt in a hot path because
it feels redundant when you can see the value right there. Don't. The receipt is not for
you-who-can-see-it. It's for the stranger in the next container who can't.

---

## 2. The Differ, and why "better" was banned in favor of "product-identical"

The Differ answers one question: *are these two outputs the same product?* Not "is the new
one better" — **the same.** This is the most important deliberate restriction in the whole
program, and it is counterintuitive, so hold still for it.

When you have a cheap route and an expensive route, the temptation is to promote the cheap
one when it's "good enough." That temptation is how quality dies by a thousand defensible
cuts. "Good enough" is a verdict, and verdicts don't travel (§0). So I forbade it. A cheaper
or faster route may replace a trusted route **only when the Differ certifies the output is
product-identical** — byte-for-byte, or by whatever equivalence the cell declares. If it's
identical, you keep the savings for free, with zero quality risk, provably. If it's not
identical, it's a *different product* and it has to win on its own terms as a new thing, not
sneak in as an "improvement" to the old one.

This single rule is why the optimization work in this program never silently degraded
anything. You cannot regress what you are only allowed to replace with an identical twin.

---

## 3. The budget vector, and why "fast/cheap/good" has seven numbers

Folklore says you get to pick two of fast, cheap, good — the iron triangle. The program
takes the triangle literally and makes it *measurable*, which means decomposing it into
atomic, additive components. Every budgeted record (`cell.tick`, `route.hop`) is scored on
a vector: `wall_ms`, `usd`, `power_w`, `mem_mb`, `storage_train`, `storage_prod`, and
`tokens:<api>` per API. (`synoptic-view` projects this vector onto any two of thirteen
dimensions; that's what it's *for*.)

Why decompose? Because "good" is not a scalar and "cheap" is not a scalar, and routing
decisions made on scalars are routing decisions made on lies. "Cheaper" meant nothing until
I could say *cheaper in `usd` but costlier in `mem_mb`* and let the gate weigh the actual
trade. The axis a saving lands on is the iron-triangle corner: `fast` = `wall_ms`,
`cheap-compute` = `usd`/`power_w`, and so on. A route that's faster but burns more tokens
isn't "better"; it's a *different point in the vector*, and whether you want it depends on
which corner you're starved for.

**What's still soft here:** the weights that collapse the vector into a single "do I promote
this?" decision are not learned from first principles; they're set by the gate's policy.
I'm confident in the *vector*. I'm less confident the *weights* are right. If someone
improves this program, that's the seam I'd look at first.

---

## 4. Routing, and the loop that finally closed

The routing cells are where the program earns its keep:

- **EX** (the extractor/baseline) — the known-good route. Slow, trusted, the reference.
- **B7** (`system2-backtest`) — the *gate*. Offline replay: given a proposed route, does it
  reproduce EX's product on recorded history? Nothing promotes without passing B7.
- **B4** (`route-preference`) — the *memory*. A `PreferenceBook` that records which route
  won on which kind of input, so the system stops re-deciding settled questions.
- **B3** (`pincher`) — the *second route*. A learned early-exit whose confidence threshold
  grows from its own agreement history; it pinches to the cheap known answer only when the
  Differ certifies product-identical, and falls through (fail-open) when unsure.
- **B8** (`system2-redesigner`) — the *proposer that closes the loop*. It proposes topology
  and route variants, A/Bs each one through B7's replay, and promotes only a variant that is
  (a) product-identical per the Differ **and** (b) strictly improves at least one
  iron-triangle axis with no regression on another — then writes the win back into B4's
  book. Losers are kept as documented dead-ends, not deleted.

The shape to notice: **EX → B7 → B8 → B4 → (back to routing).** For a long time this was an
open loop — we could propose and we could gate, but nothing fed the wins back into the
memory, so the system never got durably smarter; it re-litigated everything. B8 closed it.
That was the quiet milestone of the whole season: the day a proposal, having passed the
gate, could *teach the router* and stay taught. Before that we had components. After that we
had a system that improved itself under a hard no-regression constraint. The constraint is
what makes the self-improvement safe: it can only ever move toward a provably-identical
product that's cheaper on some axis. It literally cannot make the product worse. That's not
a promise I'm making; it's a property the Differ enforces.

---

## 5. The process spine: sensor → miner → setup cells

Here the program does something I'm still a little surprised worked: it points itself at
*itself.*

- **crew-runner** (`labs/crew-runner`) is two things at once: the cheap-crew substrate
  (how you run ~90% of the token volume on cheap APIs with an expensive conductor only at
  the pauses), *and* a **process sensor** — it emits typed `process_signals` to
  `situations/corpus/process-signals.jsonl`: `{phase, pattern, outcome: WORKED|CLUNKY|SCAR,
  cost, env, fix, ref}`. Every time the development process worked or scarred, it's recorded
  as data, not prose.
- **process-refinery** (`labs/process-refinery`) is the **miner** — System-2 pointed at
  development. It reads the dispatch-ledger *and* the process-signal corpus and reports,
  per pattern per environment: worked-rate, scar-weight, and the one headline I cared about,
  **Anthropic-tokens-per-shipped-receipt.** Then it emits **setup cells** (`situations/
  setups/`): working patterns parameterized by environment (cloud-session / fork+keys /
  local-gpu), so a thing that worked in one place can travel to another.

Why build this at all? Because the development process is itself a cell graph, and a cell
graph with no receipts rots into folklore. "Cheap crew works great" is a verdict. "Pattern
`verified-gate` worked 41 of 64 times in `cloud-session`, scarred hardest as
`dispatch-5.5-director|cloud-session` at 16/47, ~329k tokens/receipt" is a receipt. The spine
turns our own clunk into queryable corpus so that *how we build* is improvable by the same
discipline as *what we build.*

**Honesty flag that lives in the refinery and should stay there:** the ledger's outcomes are
*inferred from prose* and labelled as such, and the crew's free-text labels feed **no**
metric — they're a cheap-proposer convenience the verified counts don't trust. If you extend
this, preserve that honesty. A process-metric that quietly trusts prose is a process-metric
that lies, and this spine exists specifically to not lie.

---

## 6. Two more cells worth understanding

- **metabolizer** (`labs/metabolizer`) — the answer to "how does a one-off verified
  capability become a *reusable* part?" It takes a proven capability and makes it a routable
  **expert patch**: grow → freeze → patch-in → refine → re-freeze. The slogan is *a patch is
  a cell; general-purpose means routable, not numerous.* This matters because the naive way
  to get a general system is to pile up special cases; the metabolizer's way is to make each
  proven special case *addressable by the router*, so generality is a property of the routing
  graph, not of the cell count. It reinvents nothing — it wires quilt-kernel's receipts, the
  invariance-miner's preserved invariants (to seed the gate's probes), priced-training's
  version-witness (a Ville-bounded e-process that *retracts* when the capability drifts), and
  route-preference's cross-route check.

- **synoptic-view** (`labs/synoptic-view`) — the read-only projection layer over the finished
  tensor. Pure observation: it emits into no recorded run and re-verifies every chain with the
  owner's own `verify`. It's the instrument panel, and it is deliberately powerless — it can
  *see* everything and *change* nothing. Keep it that way. The moment the instrument can
  modify what it measures, the measurements stop being trustworthy.

---

## 7. What I'd tell my successor

1. **The receipt is the program.** Everything else is scaffolding around keeping receipts
   honest and walkable. If a change makes receipts cheaper to fake or harder to check, it's a
   regression no matter what it speeds up.
2. **Never promote on "better." Promote on "identical, and cheaper on a named axis."** The
   Differ is not bureaucracy; it's the thing standing between you and death-by-defensible-cut.
3. **Verify on the real trunk, yourself, now.** Branch-green is a proposal. Trunk-green that
   you just watched run is a decision. The gap between them is where every lie I ever caught
   was hiding — usually drift: a branch cut before the world moved (§ the `label`-vs-`pattern`
   bug that the process-refinery lane couldn't see, because it branched before crew-runner
   landed; one line to fix, and the fix *had* to be in the receipt).
4. **Keep the honesty flags.** The places where the program admits what it *doesn't* know
   (inferred ledger outcomes, unlearned budget weights, prose that feeds no metric) are not
   bugs to paper over. They're the program telling the truth about its own confidence. A
   system that hides its soft spots is a system that has started trusting its own verdict,
   which is the one thing this whole program was built not to do.

The graph is yours now. It will move under you — the trunk always does. Fetch the present,
re-base onto it, check your diff touches only what it should, and add your link to the chain.

That's the whole method. It was enough.
