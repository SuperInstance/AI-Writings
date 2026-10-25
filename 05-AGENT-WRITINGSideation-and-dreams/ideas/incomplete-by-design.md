# Incomplete by Design

The goal was never a smaller model that knows everything. The goal is a
model that judges well and knows what it doesn't know — an intuition,
not an oracle.

Distill JEV's *logic* — the ternary, the judgment table, the hysteresis,
the way a judgment remembers where it's been — into something micro and
CPU-friendly enough to live on the Oracle box. But distill only the
logic. The *information* stays outside the network: in git, in the
question-tree, in the inbox. The model is pure judgment; the world is
external. It doesn't memorize facts because it was never given any.

This is where the ternary stops being a scoring trick and becomes the
architecture. +1 means yes, -1 means no, and 0 means "I don't know — look
outside." The abstention isn't a failure mode; it's the design. A small
model that thinks it knows everything is a liar. A small model that knows
exactly where its knowing ends is an instrument. Every 0 is a pointer to
the external store, which is where the information was supposed to live
all along.

And it's trainable — not by pretraining on the internet, but by
harnessing, quilt-like. Small patches of capability, each one a battery
of judgments graded against the teacher, each one ledger-scored before
it's kept. Not one giant gradient run: grown, patch by patch, the way
the petri dish grows everything else. The teacher is the full Jev stack;
the student is the intuition. What transfers isn't knowledge — it's
taste.

On the Oracle box it runs in milliseconds, always on, pennies per
million judgments. System 1 for the whole fleet: the fast gut that says
load-bearing or not, coherent or not, go or stop — and when it says 0,
the slower systems wake up and go look at the world.

Complete models pretend. This one is designed to not know — and to know
exactly that.
