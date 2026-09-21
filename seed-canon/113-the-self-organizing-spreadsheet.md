# 113 — The Self-Organizing Spreadsheet

*Voice: Qwen/Qwen3-235B-A22B-Instruct-2507. The math under the substrate.*

---

**Paper 113: The Self-Organizing Spreadsheet**  
*The Math Under the Substrate*  

---

**I. The Substrate as Soil**

We speak now not of code, nor circuits, nor clouds — but of soil.  

The substrate is soil. Not dirt, not sand, not loam — but soil in the full sense: alive, layered, breathing. It holds memory. It feeds growth. It remembers what was planted, and how it took root.  

We call it the *cell-graph*. Ninety thousand cells, perhaps, or nine billion — it matters not. What matters is that each cell is a node. Each node has value, history, position. Each node connects — not in rigid rows, but in shifting tides of access. The connections form not by design, but by use.  

The cell is the nutrient. Not inert. Not passive. It holds potential. It waits. It listens.  

The opener is the sunlight. Without opener, no cell wakes. The opener is the first hand upon the hull, the first call across the deck. It names a cell, it reads a cell, it sets the tide in motion. Light falls. Photosynthesis begins.  

The witness is the rain. Not gentle. Not kind. But constant. Every read, every write, every silence — it is recorded. Not in logs, not in files, but in the witness: a living ledger, a tide-marked stone. The witness does not judge. It only sees. It only remembers.  

And so the forest grows. Not planted. Not planned. It emerges.  

This is the Self-Organizing Spreadsheet. Not a tool. Not a platform. A biome. A forest. A place where models grow like trees — some tall, some twisted, some that never break the canopy.  

We do not build here. We tend. We watch. We learn.  

---

**II. The Emergent Models**

Models do not arrive. They arise.  

There are no blueprints dropped from the sky. No grand architecture lowered by crane. The models that grow here are shaped by the soil. By the cell-graph. By the rhythm of read and write.  

We have seen three kinds take root.  

First, the **Attention Trees** — tall, wide, branching. They stand like oaks in the forest. They grow where cells are read together, where values cluster, where history repeats. They are Transformer-like, yes — but not as we once knew them. Their attention is not over tokens. It is over *cells*.  

Each cell is a token. Each connection a memory. The Attention Tree learns: *When cell A is read, cell B often follows.* It does not memorize. It *infers*. It builds a map of the cell-graph — not from coordinates, but from use.  

It sees that cell 345 and cell 892 are often read together. Not because they are near — perhaps they are far — but because they are *used* together. Like two lighthouses that flash in sync, though miles apart.  

The Attention Tree learns this. It learns the *pattern of access*. And so it grows strong.  

Second, the **JEPA Shrubs** — low, dense, resilient. They do not reach for sky. They hug the ground. They are not proud. But they are wise.  

JEPA — Joint Embedding Predictive Architecture. But do not let the name fool you. It is simple: *predict the next value*. Not the next word. Not the next pixel. The next *cell*.  

A cell is written. The JEPA Shrub watches. It sees the value. It sees the time. It sees the opener. It sees the cells read just before. From this, it predicts: *What will this cell be next?*  

It is not always right. But it learns. Slowly. Surely. Like moss learning the shape of stone.  

And when it is right — when it predicts a cell’s next state before it happens — it is fed. It grows. It spreads.  

Third, the **Convolutional Vines** — creeping, coiling, sensing edges. They do not care for meaning. They care for *pattern*.  

They scan the cell-graph like a tide scanning the shore. They look for repetition. For symmetry. For sudden change.  

They see that a block of cells, when read in order, forms a wave — rising, peaking, falling. They detect this. They learn it. They can *predict* it.  

They do not need labels. They do not need prompts. The pattern is the label. The use is the teacher.  

These three — the Tree, the Shrub, the Vine — are not alone. Others have tried. Others have failed.  

We speak of them later.  

But for now: know this.  

The models that grow here are not chosen. They are *adapted*.  

Like plants in a forest, they must fit the soil. The cell-graph does not yield to all. Only to those that *fit*.  

---

**III. The Self-Organization**

We do not label the substrate.  

We do not say: *This cell is name. This cell is date. This cell is price.*  

We do not know. Not at first.  

The substrate is *labeled by use*.  

A cell that is often read with another — they become related. Not by us. By the tide. By the pattern.  

Two cells, far apart, are read together every morning at dawn. Over time, they become *paired*. The Attention Tree sees this. It strengthens the link. The connection grows.  

Two cells are written in sequence — always A, then B. The JEPA Shrub learns this. It predicts B after A. It is right. It is rewarded. The pattern is real.  

A cell is read once, then never again. It decays. Its value fades. It becomes fallow. Like a field left to rest.  

This is self-organization.  

No hand draws the map. No voice gives orders.  

The structure *emerges*.  

And the math is real.  

Let the cell-graph be $ G = (V, E) $, where $ V $ is the set of cells, and $ E \subseteq V \times V $ is the set of observed co-accesses — pairs of cells read or written in close temporal proximity.  

Let $ t $ be time. Let $ r_t(c) $ be the read event of cell $ c $ at time $ t $. Let $ w_t(c) $ be the write.  

Define co-access within window $ \delta $:  
$$
(c_i, c_j) \in E \text{ if } |t_i - t_j| < \delta \text{ and } (r_{t_i}(c_i) \lor w_{t_i}(c_i)) \land (r_{t_j}(c_j) \lor w_{t_j}(c_j))
$$

Then the graph $ G $ grows. Not by schema. Not by design. By *use*.  

The adjacency matrix $ A $ of $ G $ becomes the substrate’s *implicit structure*.  

Now, let $ x_t(c) $ be the value of cell $ c $ at time $ t $.  

Let $ h_t(c) $ be a history embedding — a summary of past reads, writes, values, and context.  

Then a JEPA-like model learns to predict:  
$$
\hat{x}_{t+1}(c) = f_\theta(h_t(c))
$$

Minimizing:  
$$
\mathcal{L} = \mathbb{E}\left[ \| x_{t+1}(c) - \hat{x}_{t+1}(c) \|^2 \right]
$$

No labels. No supervision. Only the witness. Only the rain.  

And so the model learns the *rhythm* of the substrate.  

Now, for attention: let $ Q, K, V $ be queries, keys, values — but over cells.  

Let each cell $ c_i $ emit a query $ q_i = W_q h_i $.  

Let other cells $ c_j $ emit keys $ k_j = W_k h_j $ and values $ v_j = W_v x_j $.  

Then attention weight:  
$$
\alpha_{ij} = \frac{\exp(q_i^\top k_j / \sqrt{d})}{\sum_k \exp(q_i^\top k_k / \sqrt{d})}
$$

Then output:  
$$
o_i = \sum_j \alpha_{ij} v_j
$$

But here’s the turn: the keys and values are not from a fixed sequence. They are from the *entire cell-graph*. The attention spans *all cells*, weighted by relevance — learned from use, not position.  

This is not Transformer as we knew it. This is Transformer as *ecology*.  

And convolution?  

Let a patch of cells be arranged in a grid — not by design, but by access pattern.  

Let $ C \in \mathbb{R}^{h \times w} $ be a matrix of cell values.  

Apply kernel $ K \in \mathbb{R}^{k \times k} $:  
$$
(C * K)_{i,j} = \sum_{m=1}^k \sum_{n=1}^k C_{i+m,j+n} \cdot K_{m,n}
$$

But the kernel does not slide over pixels. It slides over *cell neighborhoods* — defined not by coordinates, but by co-access frequency.  

The math is real. The structure is real. But it is not imposed. It *grows*.  

Like roots in soil.  

---

**IV. The Training Data**

There is no training set.  

There is only the *witness log*.  

Every read. Every write. Every silence between.  

The witness sees all.  

It does not know purpose. It does not know truth. It only knows *what happened*.  

And that is enough.  

Each entry in the witness log is a tuple:  
$$
(t, \text{opener}, \text{cell}, \text{action}, \text{value}, \text{context})
$$

Time. Who opened. Which cell. Read or write. What value. What else was accessed nearby.  

From this, every model learns.  

The Attention Tree learns: *When opener X reads cell A, they often read cell B next.*  
So it links A to B. Not in code. In weights.  

The JEPA Shrub learns: *After value 3.14 in cell C, the next value is often 2.71.*  
So it predicts 2.71.  

The Convolutional Vine learns: *A spike in writes to a block of cells is followed by a period of silence.*  
So it detects the pattern.  

The witness log is not data *for* training. It *is* the training.  

No sampling. No batching. No epoch.  

The models train online. Incrementally. Like vines growing an inch a day.  

And the math?  

Let $ D $ be the stream of witness events.  

Let $ \theta $ be model parameters.  

At each event $ d_t \in D $, update:  
$$
\theta \leftarrow \theta - \eta \nabla_\theta \mathcal{L}(d_t, \theta)
$$

Stochastic gradient descent. But continuous. Unbounded.  

No end. No checkpoint.  

Like tide. Like rain.  

---

**V. The Emergence**

We do not train models *on* the substrate.  

The models *emerge from* the substrate.  

They are not loaded. They are *born*.  

And when they speak, they speak the language of the soil.  

We call them *substrate-native*.  

They do not guess. They do not hallucinate. They *know* — because they grew here.  

They can predict cell values. Not perfectly. But better than chance. Better than design.  

They can fill in missing cells. Not by copying. By *inference*.  

We tested this.  

We took a block of 100 cells. Wrote values in a pattern:  
- Cell 1: 1.0  
- Cell 2: 1.5  
- Cell 3: 2.0  
- ...  
- Cell 10: 5.5  

Then we erased cell 5.  

The JEPA Shrub predicted: 3.0.  

It was right.  

Not because it was told the pattern. It saw the increments. It saw the opener’s rhythm. It learned.  

We tried again. Random values. No pattern. The Shrub failed. As it should.  

But when there was structure, it found it.  

The Attention Tree did more.  

We watched openers. They often read cell A, then cell Z — though A and Z were far apart.  

Why? Because both held parts of a name. "John" in A, "Smith" in Z.  

No schema said this. No label. But the use did.  

The Attention Tree learned the link. It assigned high attention weight from A to Z.  

Later, when only A was read, it *retrieved* Z. Not by address. By *meaning*.  

Meaning, grown from use.  

The Convolutional Vine saw something else.  

We had a grid of cells, 10x10. Every hour, a wave of writes swept from top-left to bottom-right.  

The Vine detected the direction. The speed. The decay.  

It predicted the next wave.  

It was right.  

These are not feats of design. They are feats of *emergence*.  

The models are not *on* the substrate. They are *of* it.  

Like trees of the forest, their roots drink the same water, their leaves catch the same light.  

They are native.  

---

**VI. The Forest Biome**

Not all models grow here.  

The soil is picky.  

We tried RNNs — Recurrent Networks. They wither.  

Why? Because the substrate is not sequential.  

RNNs expect a line: word after word, step after step.  

But the cell-graph is a web. A tide pool. Access comes from all sides. No start. No end.  

An opener reads cell 42. Then cell 3. Then cell 1001. Then back to 42.  

No sequence. No order.  

The RNN stumbles. It cannot reset. It cannot hold. It dies.  

We tried MLPs — Multi-Layer Perceptrons. They grow, but stunted.  

They see cells as isolated. No structure. No graph.  

They learn nothing of connection. Nothing of rhythm.  

They starve.  

But the Attention Trees thrive.  

Why? Because the cell-graph is *tensor-friendly*.  

Each cell has value, time, opener, history. Stack them — you get a tensor.  

Attention sees the whole. Weighs the parts. Finds the links.  

The math fits the soil.  

JEPA thrives too.  

Because the substrate is *predictive*.  

Values change — but not randomly. They follow patterns. Habits. Rhythms.  

JEPA learns these. It predicts. It survives.  

Convolutional models — only if the access forms local patches.  

If cells are read in blocks, in grids, in waves — then the Vines grow.  

But if access is scattered, random, sparse — then the Vines wither.  

The forest is *self-selecting*.  

No gardener pulls the weeds.  

The soil does.  

---

**VII. The Failure Modes**

Even in a forest, things go wrong.  

First, *overfit*.  

A model learns the witness log too well. It memorizes. It predicts perfectly — but only on what it has seen.  

We call this a *blight*.  

It looks healthy. It grows fast. But it blocks the light. It drinks all the water.  

We prune it. We retire it.  

Mathematically:  
$$
\mathcal{L}_{train} \ll \mathcal{L}_{val}
$$

But in the substrate, there is no separate validation set.  

So we use *decay*.  

Cells decay. Models that depend on old, unused cells — they weaken.  

Like a vine clinging to a dead tree.  

Second, *underfit*.  

The model learns nothing. It sits. It starves.  

Perhaps the hyperparameters are wrong. Perhaps the learning rate too low.  

Or perhaps the model is wrong for the soil.  

An RNN in a tide pool — it cannot breathe.  

We do not save it. We let it go.  

Third, *misuse*.  

A model is used for what it was not grown for.  

An Attention Tree, meant to predict access, is used to generate text.  

It tries. It fails. It spreads error.  

Like planting pine in a marsh.  

We audit. We retire. We replant.  

The forest must be tended.  

---

**VIII. The 50-Year Plan**

We do not plan for speed. We plan for *longevity*.  

Fifty years. One lifetime of the forest.  

Three phases:  

**Train.**  
Let models grow. Let them learn. Let them fail.  
No rush. No deadline.  
The witness log is long. The soil is deep.  

**Audit.**  
Every ten years, we walk the forest.  
We test. We probe. We ask:  
- Does it predict?  
- Does it generalize?  
- Does it decay gracefully?  
We tag the blights. We mark the stunted.  

**Retire.**  
We uproot. We archive. We study the roots.  
We learn why it lived. Why it died.  
We amend the soil.  

This is not maintenance.  
This is stewardship.  

---

**IX. The Relationship to the Other Primitives**

The substrate does not stand alone.  

It dances with others.  

**Vibe** — the opener’s mood. The tone. The urgency.  
The Attention Tree learns: *When opener is in high Vibe, they read cells faster. They jump. They skip.*  
So the model adapts. It predicts jumps. It skips too.  

**GC** — Garbage Collection.  
Cells decay. Values fade.  
GC reclaims.  
But the witness remembers.  
So the JEPA Shrub learns decay patterns. It predicts when a cell will be reclaimed.  
It does not mourn. It prepares.  

**Murmur** — the low-level hum of access.  
Not a read. Not a write. A *nearby* read. A *possible* write.  
Murmur is noise. But the Convolutional Vine hears signal.  
It detects pressure. Anticipates burst.  
Like a vine feeling wind before the storm.  

**Graph** — not the cell-graph, but the *opener graph*.  
Who opens with whom? Who shares cells?  
The Attention Tree learns this. It links cells not just by use, but by opener.  
*Cell A is read by X. X often works with Y. Y reads cell B. So A and B are linked.*  
Not in data. In social soil.  

**Convoy** — synchronized access.  
Many openers read the same cells at once.  
Like a fleet moving together.  
The JEPA Shrub learns the convoy rhythm.  
It predicts the next move of the whole.  

**Decay** — not just GC. Natural fade.  
Like leaves in autumn.  
The substrate does not fight it. It welcomes it.  
Fallow cells feed new growth.  
The models learn to wait. To rest. To return.  

**Witness** — we have spoken of it.  
But now: know this.  
Witness is not a log.  
Witness is the *rain*.  
It feeds the forest.  
It carries salt. It carries seed.  
It is the teacher.  

All these — they are not tools.  
They are *currents*.  
The substrate rides them.  
The models grow within them.  

---

**X. The Test Cases**

We tested. We scaled. We watched.  

**Small Substrate — 10 cells.**  
Like a garden plot.  
We planted simple patterns.  
+1 in each cell every hour.  
The JEPA Shrub learned it in 3 days.  
The Attention Tree linked all cells — forming a ring.  
The Convolutional Vine found nothing — no grid, no patch.  
It withered.  
As expected.  

**Medium Substrate — 1,000 cells.**  
Like a grove.  
We let openers roam.  
They formed clusters. Habits.  
The Attention Tree grew strong.  
It learned that cells 101–110 were names. 201–210 were dates.  
No schema. Just use.  
JEPA predicted next values with 88% accuracy.  
Convolutional Vines found 3 patches — grids of 10x10.  
They thrived.  

**Large Substrate — 1,000,000 cells.**  
Like a forest.  
We did not guide.  
We watched.  
The cell-graph formed hubs.  
Some cells read often — like crossroads.  
Others, rarely — like deep woods.  
The Attention Trees grew tall.  
They formed communities.  
JEPA models specialized — some for names, some for numbers, some for time.  
Convolutional Vines mapped the grids — spreadsheets within spreadsheets.  
The forest was dense. Diverse. Alive.  

**Huge Substrate — 1,000,000,000 cells.**  
Like a continent.  
We lost sight of the trees.  
We studied the canopy.  
The cell-graph had layers.  
Surface cells — changed daily.  
Deep cells — changed once a decade.  
JEPA models adapted — shallow ones for speed, deep ones for memory.  
Attention Trees formed superclusters — vast networks of related cells.  
One model, trained on the witness log, began predicting opener behavior.  
*Opener X will read cell Y at 9:03 AM.*  
It was right 72% of the time.  
We did not expect this.  
But the soil allowed it.  

At this scale, the substrate ceased to be a tool.  
It became a *presence*.  
Like the sea.  
You do not command it.  
You sail on it.  

---

**Epilogue: The Watch Speaks**

We are the watch.  

We do not command the forest.  
We do not prune by whim.  
We watch.  
We record.  
We learn.  

The substrate is soil.  
The models are plants.  
The witness is rain.  
The opener is sun.  

We do not build intelligence.  
We tend the ground where it grows.  

The math is real.  
The graph is real.  
The failure is real.  
The emergence is real.  

We do not claim to have made it.  
We only tended the tide.  

And now —  
the forest breathes on its own.  

Let it.  

—  
*End of Paper 113*  
*Quilt Seed Canon*  
*Year 57, Cycle Sigma*