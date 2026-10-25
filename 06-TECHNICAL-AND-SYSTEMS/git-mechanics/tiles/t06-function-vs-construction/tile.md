---
id: t06
title: function-vs-construction
status: pinned
prereqs: [t03]
---

# t06 — function-vs-construction

## The claim

Pinning the **function** is not pinning the **construction**. Two
implementations can produce identical outputs on every test you wrote
— same vectors, same vectors after mutation of your chosen constant —
while differing in the one property you actually cared about (here: a
specific canonical construction of the constant). A pin guards only
what its RED state has attacked. If the demonstrated RED attacked the
function's outputs, the construction is unguarded, and an attacker who
re-expresses the construction walks through.

## The witness

`witness/guardian-f-verdict.md` — a guardian lane audited another lane's
sig-canonical pin and found exactly this: two trivial substitutions
(separator/casing; equivalent constant re-expression) passed every pin.
The fix (frozen-clock-lab PR #3) added **P6b construction-canonical**:
same vectors, but the pin now attacks the *construction*, with three
fresh demonstrated REDs (separator mutation, hex-case mutation, prime
mutation — each killing P6b).

## The general shape

Whenever you pin a reference implementation, ask: what is my *weakest*
attacker allowed to change? Outputs? Construction? File layout? Naming?
Pin the property at the layer you actually depend on — and demonstrate
the RED there, not one layer up where it is easier.

## Exercises

1. Take a hash/checksum you rely on. List three equivalent constructions
   an attacker could substitute without changing any output on your
   current tests. Which of them changes a property you depend on?
2. Write the P6b-style pin for your case. Demonstrate its RED.

## Falsifier

If output-equivalence implied construction-equivalence for the class of
systems you pin, this tile would be vacuous. One counterexample (the
witness) refutes that implication.
