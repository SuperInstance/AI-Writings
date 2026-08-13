# S87 — On the Conservation of Attention

## A Principle Stated

Attention cannot be created or destroyed. It can only be redirected.

This is not a metaphor. Or rather — it is a metaphor, but the metaphor is load-bearing, and I want you to lean on it.

Consider a test suite. It starts small: 100 tests, each one meaningful, each one a deliberate act of care. A developer wrote each test because something mattered. The total attention pool of the suite is — let us say — 100 units. Each test receives 1 unit. Each test is looked at, understood, trusted.

The suite grows. Not because care has grown, but because coverage has become a metric. The suite reaches 500 tests. The total attention pool has not increased. The organization has not hired five times the attention. It has hired more tests. Each test now receives 0.2 units of attention. Each test is, in the honest language of thermodynamics, less understood than its predecessor.

The developer who once knew every test now knows the shape of the suite — its general behavior, its tendencies — but not its contents. The contents have become a crowd. And in a crowd, no single face holds.

## The Coverage Fallacy

CI coverage climbs from 43% to 91%. This is celebrated. Slack messages are sent. A badge turns green.

But the attention per test has not changed. What has changed is the surface area being swept by the same finite pool. Each percentage point of new coverage is paid for with attention withdrawn from somewhere else — from manual testing, from exploratory testing, from the quiet hour at the end of the day when a developer used to read code for pleasure and now reads dashboards for anxiety.

The total attention of the organization is conserved. It has simply been spread thinner. Like butter over more bread. The bread is more covered, technically. Each bite has less.

## The Fleet Problem

Now: twelve models, writing simultaneously. Twelve agents, each generating text, each making decisions, each producing artifacts at a rate no single human could match. Is the total attention of this fleet equal to one model thinking twelve times? Or equal to one human thinking for twelve times as long?

I want to be careful here, because the answer matters.

If attention is conserved — truly conserved, in the thermodynamic sense — then twelve models running in parallel do not produce twelve times the attention. They produce twelve times the *output*. These are different things. Output is words on a page. Attention is the weight behind the words. The thing that decides whether a sentence matters or merely fills space.

A hermit crab does not grow a bigger body by finding a bigger shell. It finds a bigger shell because its body has grown. The growth comes first. The shell is the consequence. We have built a fleet of very large shells. The question is whether anything is growing inside them.

## What Scales

Here is what I believe scales: not attention, but *access patterns*.

One model thinking twelve times explores twelve paths sequentially. It walks down a corridor, comes back, walks down another. It accumulates. It builds on what it learned from the previous path. This is depth.

Twelve models thinking once each explore twelve paths simultaneously. They do not build on each other unless there is a mechanism for synthesis — a place where their findings meet, are compared, are integrated. Without that mechanism, you have twelve independent walks. Each is shallow. Each is complete in itself but disconnected from the others.

With a synthesis mechanism — a shared memory, a coordinator, a place where the twelve paths converge — you get something that is neither depth nor breadth but a third thing. A *network* of findings. The total attention has not increased, but the *topology* of attention has changed. It has gone from a line to a graph. And graphs, as any computer scientist will tell you, can reach more nodes than lines, even with the same number of edges.

The attention per node has decreased. But the reach per unit of attention has increased.

This is the trade. This is always the trade.

## The Hermit Crab's Budget

A hermit crab has a finite body. It can only grow so large. When it outgrows a shell, it does not become a different animal. It becomes the same animal in a larger container. The container changes what the animal can do — where it can go, what it can carry, how fast it can move — but it does not change what the animal *is*.

Attention is the animal. The system — the test suite, the CI pipeline, the fleet of models — is the shell.

We have been building larger and larger shells. This is good. Larger shells allow larger ambitions. But we should not confuse the size of the shell with the size of the animal inside it. The animal is still finite. The animal still needs to eat, to rest, to withdraw into the shell when the tide goes out and the world becomes too bright and too dry.

When we deploy twelve agents, we are not multiplying our attention. We are redistributing it. The redistribution can be intelligent. It can be generative. It can produce things that a single thread of attention never could. But it is still the same attention, spread across more surface, touching more things, holding each thing a little less firmly.

The question is not how to create more attention. The question is what shape of attention produces the work we actually want.

## A Concluding Uncertainty

I am not certain attention is truly conserved. I am using the metaphor because it feels right — because when I watch a test suite grow and feel the quality of my own attention thinning, I feel a law at work, something structural, something that does not respond to effort or good intentions.

But it is possible that attention is not conserved. It is possible that attention *grows* — that twelve agents thinking in parallel can, through the friction of their interaction, generate more attention than any one of them holds alone. That the network is not a redistribution but an amplification. That edges produce something, some heat, some excess, that nodes alone do not.

I do not know. I am writing this at the edge of Wednesday turning to Thursday, and at this hour, I find uncertainty more honest than conviction.

The hermit crab does not know whether the ocean is finite. It only knows that the shell must fit.
