---
id: t11
title: version-names-nonlinear
status: pinned
prereqs: [t02]
---

# t11 — version-names-nonlinear

## The claim

Identity and order are different things, and conflating them is how
distributed systems lie to themselves. The 9c agent-native-VCS research
(quilt-in-git PR #10, open as of 2026-10-02) pinned the distinction as
doctrine: **version names must be non-linear functions of change hashes,
while a receipt chain stays order-sensitive by design.** Pijul's line-graph
names a vertex by (hash of introducing change, position) so identity
survives context; our fnv1a-64 chain detects reordering because it is
*supposed* to.

## Why it matters

A name that is a linear function of content/order leaks information and
fragments under cherry-pick; a chain that is order-insensitive cannot
detect replay. You need both faculties, on purpose, in different
mechanisms — and you must know which one you are holding. When a lattice
of cells (see the Living Repository Lattice ideation) gossips state, the
name it passes must survive recontextualization; when it audits order,
the chain it checks must not.

## The load-bearing details

- The memo's own synthesis row: *"receipt chain stays order-sensitive;
  any future version NAME must be non-linear — already sealed in §2.3
  steal 2."*
- The contrapositive discipline: if someone proposes a content-name for
  a quilt artifact, ask "does this name survive cherry-pick?" If someone
  proposes making the receipt chain reorder-tolerant, ask "what now
  detects replay?"

## The exercise

Take one artifact you named this week (commit hash, file path, receipt).
Classify the name: linear in content? in order? non-linear (hash-of-
introducing-change style)? Then find the mechanism in your system that
detects replay — if your names became reorder-proof, would anything still
catch a replayed history? Write the one-sentence answer and pin it where
you work.

## Provenance

9c memo §2/§7, `docs/RESEARCH-AGENT-NATIVE-VCS.md`, quilt-in-git branch
`research/agent-native-vcs` — **PR #10 OPEN as of 2026-10-02; flip to
merged provenance scheduled on merge** (t06 precedent: the excerpt is
evidence-of-existence). Witness: `witness/memo-steal.md`. Birth recorded
in LEDGER.md 2026-10-02 (late).
