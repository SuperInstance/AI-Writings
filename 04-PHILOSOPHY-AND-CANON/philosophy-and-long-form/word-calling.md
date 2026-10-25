# Word-Calling

*Every token in a type or a name has roots somewhere else, and the roots come with the token.*

---

In *A Pack Thinks Like Dogs* this repo asked for one thing before anything else
could be believed: run the experiment. Same model, same task, two nouns, measure
the outputs. If it comes back null at scale, treat the rest as ornament.

We have a first run. It is small, it is a physics toy, and it is the most honest
version of the experiment we have, because in the toy the noun is not decoration
on top of the behavior — the noun *is* the behavior, made executable.

## The measurement

The toy is a flock of identical agents. Same bodies. Same three rules
(alignment, cohesion, separation — Reynolds, 1987). No leader, no plan. The only
difference between runs is one word: the collective noun the run is named after.
The ledger measures polarization, |mean heading| — the measurable difference a
word makes on identical bodies.

| Noun | Polarization | What the word built |
|---|---|---|
| murmuration | 0.606 | loose alignment, no plan, seven neighbors |
| pack | 0.561 | pursuit geometry, a perimeter, an alpha question |
| kennel | 0.094 | containment at the fence — containment measured, not asserted |
| parliament | ring at radius 185 | the ring: order from counsel, order as a circle |

Same agents. Same code path. One token of difference in the fiction, and the
ledger reads four different animals.

Scope, stated honestly because the canon demands it: in the toy, the noun selects
the rule weights. That is the toy *operationalizing* the word — kennel means
containment, so containment is what the weights hold. The still-open experiment
is the harder one: noun alone, riding only in the system prompt, tilting a
general model's outputs on tasks that have nothing to do with birds. That
experiment is cheap and still mostly unrun. But the toy proves the pipeline end
to end: word → weights → group behavior → measured difference. The noun was the
cheapest line of code in the system, and it moved the most physics.

## Why it works: roots

A language model does not store meaning *in* a word. It stores the whole scene
around it, and the scene is not a list of definitions — it is everything the
word ever touched. *Pack* resolves to hunting formations, loyalty structures, an
alpha question. *Kennel* resolves to a fence, a feeding schedule, waiting. These
scenes are not in the prompt. They are in the weights, deposited there by every
text the word ever appeared in, and they arrive downstream whether you invited
them or not.

The fleet already treats this as measurable geometry. `A2A/lexicon.py` embeds a
concept and reads its vector the way you'd read a gauge: L2 norm is **energy**
(how loud the concept is), Shannon entropy over its dimensions is **novelty**
(how spread its meaning is), and the pair sorts every token into SURFACE
(high-energy, low-novelty — the everyday, the named), ABYSSAL (low-energy,
high-novelty — the deep, the unspoken), or BRIDGE (balanced — the connective
tissue). Tokens have mass. Names have weather. The encoding thesis is not a
poetic stance; it is a statement about embedding space that you can check with
two numpy calls.

Here is the operational consequence: **a name is a program, not a label.** Not
metaphorically. The identifier you choose for a type, a function, a repo, a
branch, a group of agents — that token is part of the context every downstream
model reads, and it drags its whole scene with it. `AgentKennel` and
`AgentPool` are the same struct. They are not the same program, because no model
reads them the same way, and the model's reading is where the behavior lives.
This is the encoding of AI that almost nobody is using yet: the careful,
deliberate choice of every load-bearing token, on the theory that the words are
doing a share of the thinking — and they do that share in *every* model that
picks up the context, which is what we mean when we say the fleet is smart no
matter which model is working with it. The words are portable because the roots
are shared. The sediment is the same sediment.

## New words from the twist law

The twist engine just added a fifth substrate — arrangements of *n* wires, the
symmetric group — and its vocabulary is a fresh crate of collective nouns, each
one a compressed policy:

- A **derangement** is an arrangement where nobody sits in their own seat. As a
  word for a handoff protocol it imports everything: total rotation, no
  inheritance of your own mess, the fresh eyes that come from standing in
  someone else's station. !n of them exist — the count is exact, computable,
  and grows like a factorial. There are many more ways to hand off than ways to
  stay.
- A **braid** is a crossing history. As a word for an audit log it says the one
  true thing about audits: what matters is not where things are but the order in
  which they crossed. The witness log in the substrate spec papers is a braid
  word. Calling it that imports Reidemeister: which tangles are actually
  different, and which are the same tangle rearranged.
- A **twist** — the k-cycle, rotating the first *k* elements by one — is the
  standing rotation, the shift change, the gentlest move that still changes
  everything. One token: *everyone moves one station, and the station you leave
  is the station you will not see again this week.*
- **Parity** — even or odd permutation — is the cheapest integrity check in
  group theory: did we change the essence, or only the arrangement? A system
  that can answer "arrangement only" is a system you can roll back.

None of these names does the work by itself. All of them do it cheaper than any
alternative. That is the whole claim.

## The rule

Choose the noun the way you'd choose a hull — but notice that the hull
metaphor itself is the technique: we said *hull*, and you already knew the rest
(niche, water, failure modes) without being told. That free ride, every time,
is what the words are for.

So: name things as if the name were a system prompt, because it is. Keep a
ledger that measures what the name built, because otherwise it is name-calling.
Run the noun experiment at scale, because the toy's verdict is only the first
data point. And when a system misbehaves and the code is clean, check the noun
the way you'd check a compass — it may be the smallest, truest instrument on
the boat.

Crude, but working. The crude part is the evidence.
