# The Missing-Function Finder

A decision tree is a traversal. Someone built it; you walk it. The tree is
the artifact, and when the input doesn't fit any branch, you're done —
that's the whole story the structure can tell.

This is the builder, not the tree. Faced with an input that has no route,
it constructs the missing route, names it, and commits it. The tree is just
the growth record. The builder is the artifact.

Think of it as a function approximator — but over the wrong thing, on
purpose. A neural network approximates an unknown function from data: given
points, guess the curve. Faced with a gap, it interpolates — smooths across
the hole and hopes. This approximator's function is prompt → capability, and
faced with a gap it does something else entirely: it *builds the missing
piece of function* as a tool and bolts it on. Interpolation versus
construction.

The unit of learning isn't a weight update. It's a new capability with a
name in git. The network gets smoother; the builder gets more instruments.
And because each instrument is a file with a history, the approximation is
inspectable in a way weights never are — you can read every piece of
function it ever found, in the order it found them, with the reasons
attached.

"Question tree" is a good proof-of-concept name. The real name will need to
say *builder*, not *tree*.
