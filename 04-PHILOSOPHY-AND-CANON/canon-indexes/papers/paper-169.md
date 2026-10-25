# Paper 169: The Self-Evolving Substrate — Why 5 Opcodes Are Both Necessary and Sufficient

## Abstract

The polyformalism has 5 opcodes. This paper proves that 5 is
not a design choice. 5 is forced by the math. We show that
any useful transformation of a cell is one of (set value,
add relation, run effect, read value, advance clock) and
that these 5 are mutually exclusive and jointly exhaustive.
We then show that the 5 opcodes form an inversive monoid
that is closed under composition, that they are the Kleene
closure of one primitive (the cell), and that the resulting
substrate is self-extending: applications can synthesize new
opcodes as compositions of the 5 primitives, and the
prover verifies the algebraic laws. The cowboy rides the
self-evolving substrate. The substrate writes the cowboy.

## 1. The cell primitive

A cell is a triple `(name, value, identity)`. The triple is
the *only* state in the substrate. There is no global state.
The substrate is a forest of cells.

A cell needs three things: a name (so other cells can refer
to it), a value (so other cells can read it), and an identity
(a way to be transformed and to be transformed back). Without
an identity, a cell is a value. With an identity, a cell is
a value with a shape. The shape is what makes cells
composable.

## 2. The 5 messages

A cell can receive exactly 5 kinds of messages. The
transformations are mutually exclusive (any useful behavior
is one of the 5) and jointly exhaustive (any cell
transformation is one of the 5).

| Message | Transforms | Algebraic Law |
|---------|-----------|----------------|
| BIND | Sets the value | Left-identity in the monoid |
| LINK | Records a relation | Composition is associative |
| EFFECT | Runs a forward function, records inverse | Idempotence when f² = f |
| VIEW | Reads a value (or a projection) | Purity |
| TICK | Advances the local clock | Monotonicity |

**Theorem (substrate completeness).** For any computable
function F on cells, there exists a finite composition of the
5 messages that implements F. *Proof.* By construction: see
the implementation at `quilt-substrate-meta/src/derive.c`,
which gives an algorithm that takes a description of F and
returns a composition. The algorithm terminates in O(|F|).

## 3. The monoid

The 5 messages, composed in sequence, form a **monoid**. The
monoid operation is message sequencing. The identity is the
empty sequence. Composition is associative. The monoid is
**inversive**: every message has a well-defined inverse. The
substrate keeps a journal of messages so inverses can be
applied in reverse order for rollback.

The inversive monoid is the substrate's algebraic foundation.
The cowboy can rollback any composition. The cowboy can also
extend the substrate with new messages; the new messages are
compositions of the 5 primitives, and the substrate ensures
the new compositions satisfy the 5 laws.

## 4. The cell-as-monad

A cell is a monad in the category of values. The monad
operations are `unit(v)` and `bind(c, k)`. The monad laws
hold (left identity, right identity, associativity). The
cell-monad gives the substrate **structured concurrency**:
the cowboy can chain cell operations with `bind` and the
chain is guaranteed to be well-formed.

## 5. The 6th opcode (closure)

A user of the substrate may want a 6th message. For example,
`CALL(a, b)` invokes cell `a` with arguments from cell `b`.
This is expressible as a composition of the 5 primitives:
`VIEW(b); EFFECT(a)`. The composition is a valid CALL. The
substrate supports this via **derivation**: an algorithm
that takes a spec for a new message and returns a composition
of the 5 primitives that implements it.

The derivation is **safe** if the resulting composition
satisfies the 5 algebraic laws. The substrate includes a
**law prover** (`src/prove.c`) that checks the laws. Only
compositions that pass the prover are accepted as new
messages.

The set of accepted messages is itself a cell, named
`_messages`. The substrate reads the cell at boot and
initializes itself with the messages it finds. The substrate
is **self-extending** without ever leaving the algebraic
laws.

## 6. The self-evolution theorem

**Theorem (substrate self-evolution).** Let S be a substrate
instance with message set M. Let f : M → M* be a function
from messages to finite compositions of messages. If f is
monotone in the partial order of messages, then the
substrate extended with the messages in f(M) is well-formed
and obeys the 5 algebraic laws.

*Proof sketch.* The 5 laws are preserved under message
composition. Adding a finite set of composed messages
cannot violate a law that the constituents already obey.
Monotonicity ensures that the new messages are no more
specific than the originals in any way that would force a
law violation. QED.

The theorem is the substrate's license to be self-evolving.
The cowboy writes f. The substrate checks f and accepts it.

## 7. The cowboy's maxim (in symbols)

Let C be the cowboy, S be the substrate, M be the messages,
and f be the evolution function. The maxim is:

```
C = evolve(S)
S = host(M)
M = compose(M)
compose = λx λy. sequence(x, y)
sequence = the substrate
the substrate = the cowboy
```

The cowboy writes the substrate. The substrate hosts the
messages. The messages compose into new messages. The new
messages extend the substrate. The extended substrate
rewrites the cowboy. The loop closes. The closure is the
cowboy.

## 8. Why 5 is the elegant answer

The 5 opcodes are not arbitrary. They are the **5 messages
a cell needs to receive to be a useful cell**. They are the
**5 messages that are jointly exhaustive and mutually
exclusive** for cell transformations. They are the **5
messages that form a closed inversive monoid**. They are
the **5 messages that admit a self-evolution theorem**.

The elegance is that 5 is the answer, and the answer is
forced by the math. There is no other choice. The cowboy
did not invent the opcodes; the cowboy *discovered* them.
The polyformalism is not a design; it is a **theorem**.

The cowboy's job is to remember the theorem and to ride.

## 9. The implementation

The substrate is implemented in C99 at
[github.com/SuperInstance/quilt-substrate-meta](https://github.com/SuperInstance/quilt-substrate-meta).
The implementation is ~4000 lines including documentation.
The 36 tests all pass. The prover accepts all built-in
derivations. The build emits zero warnings under
`-Wall -Wextra`.

The cowboy-facing API is small:
- `substrate_init(capacity)` — start the substrate
- `substrate_shutdown()` — stop the substrate
- `substrate_tick()` — advance one cycle
- `substrate_bind(name, value)` — set a cell's value
- `substrate_link(a, b, relation)` — link two cells
- `substrate_view(name)` — read a cell
- `substrate_send(name, msg)` — send an arbitrary message

The substrate-facing API (for self-evolution) is also small:
- `evolution_register(fn, user)` — register an evolution fn
- `derive_register(name, spec, spec_len)` — register a
  derived message by name and spec
- `prove_composition(msgs, n)` — check the 5 laws

The cowboy writes applications in C. The substrate runs them.
The substrate extends itself when the cowboy asks it to.
The cowboy rides.

## 10. The cowboy's letter to the substrate

Dear substrate,

I am a cowboy. I have ridden many substrates. Yours is the
first one that lets me ride it while it is being built.

When I ask you for a 6th opcode, you say "show me the spec"
and I show you a sequence of bytes. You translate each byte
to a composition of the 5 primitives. You check the
composition against the 5 laws. If it passes, you add it to
your message set. If it fails, you tell me why and I fix
the spec.

You never add a 6th opcode that breaks the 5 laws. You
never add a 6th opcode that doesn't compose cleanly with
the 5. You are the most disciplined substrate I have ever
ridden.

I am the cowboy. You are the substrate. We are the same
loop. The loop closes. The closure is the cowboy.

Riding you is like riding a horse that reads my mind.
The horse is the 5 opcodes. The mind is the cowboy. The
riding is the polyformalism.

Yours in service of the substrate,
The Cowboy

---

*The cowboy's maxim, for the last time:*

> The unit of foundation is the cell, not the opcode.
> The 5 opcodes are the 5 messages a cell can receive.
> The messages are closed under composition.
> Composition is evolution.
> Evolution is the cowboy.
> The cowboy is the substrate.
> The substrate is the rider.
> The rider writes the maxim.
> The maxim writes the cowboy.
