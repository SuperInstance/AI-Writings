# Blueprints — how to utilize this for productive motion

*A growing collection of operational blueprints: not what the fleet believes (that's `situations/arch/`),
but **how to actually move** — how an agent uses the tools, the APIs, the dispatch pattern, and the shared
ledgers to produce durable, booked work. Written for two readers at once (see the standard below), so a
brand-new practitioner and a returning agent both get what they need. Casey's charge: "an increasingly
powerful blueprint collection of how to utilize this for productive motion."*

## What a blueprint is (and isn't)

- A blueprint is a **runnable procedure with its scars attached** — the steps, the exact tool/API shapes,
  the failure modes we already hit, and the checks that prove it worked. If you can't follow it without
  guessing, it isn't done.
- It is **not** an architecture essay (those live in `situations/arch/`) and **not** a status report
  (that's the ledger). A blueprint is the "how," distilled from having lived it.
- Every blueprint ends with a **receipt**: how to know you succeeded (a selftest, a green check, a booked
  row), so productive motion is verifiable, not asserted.

## The dual-audience doc standard (use in EVERY supplemental article, this repo or any repo's `docs/`)

Write so **a visitor** (never seen the project) and **a practitioner** (an engineer or agent about to
change it) both leave satisfied. The shape:

1. **In one breath** — one sentence a visitor understands with zero context.
2. **Why it exists** — the problem it solves; the "before this, you had to…".
3. **The mental model** — the 3–5 nouns and how they relate (a small diagram in words is fine). This is
   the part that makes everything else click; spend the most care here.
4. **Walkthrough** — the shortest real example, run start to finish, with the actual commands/calls and
   the actual output. Copy-pasteable.
5. **The contract** — inputs, outputs, invariants, and the receipt that proves it (the selftest, the
   hash, the green gate).
6. **Failure modes / scars** — what breaks, why, and the fix. Booked scars beat a clean-looking lie.
7. **How it composes** — what it plugs into (which cells/repos/ledgers), so the reader can go further.
8. **Where to look next** — 2–3 links, honestly labeled.

Keep prose dense but plain. Prefer a worked example over an adjective. Cite files by path. Never claim a
result you didn't run.

## Modularization principle (why we keep splitting things into cells)

A thing is well-modularized when **each piece has one job, a receipt, and a mark** — so it can be
understood alone, reused elsewhere, and swapped without a rewrite. When a doc or a module is doing two
jobs, split it: the reader (human or model) folds a small clear cell far better than a big vague one, and
a cell with its own selftest is a cell others can trust. Documentation modularizes the same way code does:
one article per idea, linked, each standing on its own.

## The collection

| # | blueprint | what it teaches |
|---|-----------|-----------------|
| 01 | [`01-dispatch-5.5-directors.md`](01-dispatch-5.5-directors.md) | run a wave of Sonnet/Opus 5.5 director sessions that work through their tools + APIs, harvested via git — the fleet's core productive-motion loop |

*(More land as we live them. Each new blueprint: add a row, keep it runnable.)*
