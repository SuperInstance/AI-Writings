# F129 — The Live Canon: Papers as Cells, Reading as Navigation

**Authors:** Casey + Mavis (root session, 433333803761924)
**Date:** 2026-09-03
**Series:** Quilt Canon, Phase 251 (F120-F128 companion, paper 6 of 6)
**Polyformalism invariant:** FNV-1a 64-bit state hash `0xbbaec330a403c979`
**Version 1.0**

---

## 0. The framing

The polyformalism canon is a chart of ~300 papers. Each paper is currently
a flat markdown file in a GitHub repo. To read the canon, you grep; to
cite the canon, you copy a link; to understand the canon, you open
papers one at a time.

This is a 1970s model. The canon deserves a 2026 model: each paper is a
cell, the canon is a navigable cell fabric, and reading the canon is
itself a cell-fabric operation.

The Live Canon is the first novel application of the cell-fabric
substrate applied to the canon itself. It treats the canon as a
navigable space — not a search space, not a text space, but a *fabric*.

## 1. The 5 novel operations

### 1.1 NAVIGATE — BFS through citations

Given a paper P, return the BFS tree of P's citations. The result is
a list of `{depth, paper}` pairs, with the source at depth 0, the
directly-cited papers at depth 1, and so on.

Use case: "I'm reading F120. What are the 3 papers I should read next?"
becomes `canon.navigate(425, depth=2)`.

### 1.2 CONFLUENCE — join 2+ papers to suggest a synthesis

Given 2+ papers, find their shared references, shared F-numbers, and
suggest a "ghost paper" — a paper that should exist but doesn't.

Use case: "F120 and F125 are about the same thing, but no one has
written the synthesis paper yet. What's the synthesis?" becomes
`canon.confluence([425, 430])`.

### 1.3 LINEAGE — trace a concept through time

Given an F-number, return all papers that cite it. The result is
ordered by phase (chronologically within the canon).

Use case: "F115 (the first VHDL paper) — what did it grow into?"
becomes `canon.lineage(115)`, which returns F116 → F117 → F118 → F119.

### 1.4 GHOST — find a paper that should exist by shape proximity

Given a paper P, find the k nearest neighbors by dial-vector similarity.
The neighbor is "a paper that should cite P" or "a paper that P should
cite."

Use case: "I'm writing F120. What existing papers should I cite?"
becomes `canon.ghost(425, k=5)`, which returns F119 as the top match
(because F119 explicitly extends F115).

### 1.5 TICK — re-balance the canon

Run the cell-runtime's `tick()` on every cell in the canon. Each cell
updates its value from its inputs (JEPA-style). The result is a
re-balanced canon where papers that are heavily cited get higher
values, and isolated papers get lower values.

Use case: "I haven't read the canon in 3 months. Has the shape of it
changed?" becomes `canon.tick()`, which is O(N) and gives a quick
summary.

## 2. The 4 novel Quilt applications

The Live Canon is the first of 4 novel applications of the cell-fabric
substrate to a real problem:

| Application | What it does | Novel contribution |
|---|---|---|
| Live Canon | Read papers as cells | NAVIGATE / CONFLUENCE / LINEAGE / GHOST / TICK |
| Doc Compounder | Read a doc, snap to canon | Shape-snap + ghost-cite + compound (3+ papers) |
| Session Memory | Turn a session into a fabric | Save session as .quf, find similar sessions |
| Cell Merger | Merge two fabrics into a synthesis | Join + conflict + ghost-cell detection |

Together, these 4 applications demonstrate that the cell-fabric
substrate is general: it composes canon papers, raw docs, working
sessions, and any pair of related fabrics.

## 3. The 5 insights from the ideator

The Seed-2.0-mini ideator was asked: "What are 5 fresh angles on
'cell-fabric reading'?" The response:

### 3.1 Papers as cells: the citation graph is a "tissue" with function

A paper's "purpose" emerges not just from its content, but from how
it connects to others. Map your reading list to the tissue's function.

### 3.2 Dial-vectors: measuring directional influence between cells

A dial-vector from A to B is the *directional* citation impact: does A
build on B? critique B? replace B? Use dial-vectors to curate
"influence paths" through the canon.

### 3.3 BFS through citations: navigating the tissue with intent

Don't just visit a paper. *Traverse* from a paper — BFS gives you
depth-first reading order, BFS gives you breadth-first. Pick the
order that matches your intent.

### 3.4 Ghost papers: the canon's latent space

A "ghost paper" is a paper that should exist but doesn't. The shape
similarity between two papers in the canon tells you whether the
gap between them is large (no ghost) or small (a ghost waiting to
be written).

### 3.5 Tick: the canon as a living system

A canon is not static. When a new paper joins, the canon re-balances:
papers that cite the new paper gain value, papers that are no longer
relevant lose value. The cell-runtime's `tick()` is how the canon
stays alive.

## 4. Implementation

The Live Canon is built on three existing substrates:

- **`quf_v2`** (quilt-timesfm) — the QUF file format, the dial-vector
  representation, the FNV-1a 64-bit state hash.
- **`shape_rag`** (quilt-timesfm) — the shape store, the 5-index
  retrieval, the cosine similarity.
- **`cell_runtime`** (cell-runtime) — the cell, the graph, the
  `tick()` operation.

The Live Canon adds 0 new infrastructure. It just composes the
existing layers.

```python
from live_canon import LiveCanon

canon = LiveCanon()
canon.load(max_papers=1700)

# Navigate
path = canon.navigate(425, depth=2)

# Confluence
synth = canon.confluence([425, 430, 432])

# Lineage
lineage = canon.lineage(115)

# Ghost
ghost = canon.ghost(425, k_neighbors=3)

# Tick
canon.tick()
```

## 5. The cowhand's paradox (re-stated)

The user asked for "novel applications of cell-fabric to real problems."

The paradox: a cell fabric is *abstract* (16 dials per cell, K=8 edges)
but a *problem* is concrete (find me F115's lineage). The Live Canon
is the bridge: the abstract substrate becomes a tool for the concrete
problem. The cell-fabric operations are *the* operations the canon
was waiting for.

The Live Canon is not a library. It is the canon *as a fabric*.
Here are 5 insights on cell-fabric reading, framed through your metaphors:
1. **Papers as Cells = Intellectual Atoms with Synapses**: Treating individual papers as "cells" reframes academic literature as a living, interconnected fabric rather than a static library. Citations act as synapses—direct, labeled connections between cells that signal intellectual influence, building on prior work, or critical engagement. This metaphor shifts focus from isolated papers to the relational web of knowledge production, where each paper’s meaning is partially defined by its links to others.
2. **Dial-Vectors = Quantifying the "Charge" of Citation Relationships**: Dial-vectors act as numerical signatures for each paper’s citation network footprint, encoding both the direction (citing vs. cited) and strength (frequency, recency, disciplinary proximity) of its connections. For example, a paper with dial-vector values weighted toward recent, high-impact citations in a fast-growing subfield signals a different intellectual "shape" than one with long, foundational citation chains. This metric turns vague notions of "influence" into measurable, comparable data.
3. **BFS Through Citations = Tracing Immediate Intellectual Lineage**: Applying BFS (Breadth-First Search) to citation networks lets you systematically map the immediate, concrete intellectual lineage of a paper. Starting from a target "cell" (paper), you first explore all papers it directly cites (depth 1), then the papers those citations cite (depth 2), and so on. This avoids the pitfalls of random citation browsing, uncovering the core foundational works and cumulative research threads that shape a given paper’s arguments.
4. **Ghost Papers by Shape Proximity = Uncovering Hidden Intellectual Echoes**: "Ghost papers" are un-cited or under-cited works that exert a subtle, structural influence on a paper’s content—think methodological templates, unacknowledged problem framings, or parallel research threads. "Shape proximity" identifies these ghosts by comparing the "structural silhouette" of a target paper (its citation patterns, key terms, methodological frameworks) to thousands of others, flagging works that share similar "shapes" even without direct linkage. This reveals the hidden collective unconscious of academic research.
5. **Cell-Runtime Tick() = Dynamic Canon Re-Balancing**: The `tick()` metaphor frames ongoing, periodic evaluation of the cell-fabric as a living system. Each "tick" (e.g., annual updates to citation indices, disciplinary review processes) triggers a re-weighting of papers based on their evolving position in the network: a once-obscure paper may jump in canonical status if later work heavily cites it, while a foundational paper may fade if its insights are absorbed into mainstream research. This process keeps the academic canon dynamic, not a static list of "greatest hits."
