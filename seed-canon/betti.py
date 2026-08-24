"""
betti.py — Compute the Betti numbers of the Quilt seed canon's meta-cell-graph.

Each piece (essay, story, fable, paper) is a node. Two pieces share an edge
if they reference the same canonical concept (paper number, primitive, cell
type, etc.). The Betti numbers tell us how connected the canon is.

β₀ = number of connected components
β₁ = number of independent cycles (E - V + C, for a connected graph)

The canon is the soil. The fables are the plants. The Betti numbers are
the cycles. β₁ > 0 means the canon has loops, which means the ideas reinforce
each other.
"""
import os
import re
import json
from collections import defaultdict


CANON_DIR = "/workspace/ai-writings-new/seed-canon"


def load_pieces():
    """Load all .md files in the canon as nodes."""
    pieces = {}
    for fname in os.listdir(CANON_DIR):
        if fname.endswith(".md"):
            path = os.path.join(CANON_DIR, fname)
            with open(path) as f:
                content = f.read()
            # Use filename (without .md) as the node ID
            node_id = fname[:-3]
            pieces[node_id] = content
    return pieces


def extract_concepts(content):
    """Extract the canonical concepts referenced in a piece.

    A concept is one of:
    - A paper number (107-119)
    - A primitive name (Convoy, Decay, Witness, etc.)
    - A fable number (1-30)
    - A cell type (Reyes, Skate, Inference)
    """
    concepts = set()
    # Paper numbers
    for m in re.finditer(r"\b(1[0-1][0-9]|10[7-9])\b", content):
        concepts.add(f"paper:{m.group()}")
    # Primitive names (capitalized)
    for prim in ["Convoy", "Decay", "Witness", "JEPA", "Vibe", "Murmur", "GC", "Z_in", "Z_out", "DoubleEntry", "Graph", "Tensor", "Schrödinger"]:
        if prim in content:
            concepts.add(f"prim:{prim}")
    # Fable numbers (only in certain files)
    for m in re.finditer(r"\b[Ff]able (\d+)\b", content):
        concepts.add(f"fable:{m.group(1)}")
    # Fable titles (e.g., "Paper and the Tablet")
    for m in re.finditer(r"[Ff]able (\d+)[^.]*?\(([^)]+)\)", content):
        concepts.add(f"fable-pair:{m.group(1)}")
    return concepts


def build_graph(pieces):
    """Build a graph: nodes = pieces, edges = shared concepts."""
    piece_concepts = {}
    for node_id, content in pieces.items():
        piece_concepts[node_id] = extract_concepts(content)

    # For each concept, find all pieces that reference it
    concept_to_pieces = defaultdict(list)
    for node_id, concepts in piece_concepts.items():
        for c in concepts:
            concept_to_pieces[c].append(node_id)

    # Edges: for each concept, all pieces referencing it are connected
    edges = set()
    for concept, ps in concept_to_pieces.items():
        if len(ps) > 1:
            for i, p1 in enumerate(ps):
                for p2 in ps[i+1:]:
                    edges.add(tuple(sorted([p1, p2])))
    return piece_concepts, edges


def connected_components(nodes, edges):
    """Count connected components using union-find."""
    parent = {n: n for n in nodes}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
    for u, v in edges:
        union(u, v)
    return len(set(find(n) for n in nodes))


def betti_numbers(nodes, edges):
    """Compute β₀ and β₁."""
    V = len(nodes)
    E = len(edges)
    C = connected_components(nodes, edges)
    beta_0 = C
    beta_1 = E - V + C  # rank of H₁
    return beta_0, beta_1, V, E


def main():
    pieces = load_pieces()
    print(f"Loaded {len(pieces)} pieces")
    concepts, edges = build_graph(pieces)
    beta_0, beta_1, V, E = betti_numbers(set(pieces.keys()), edges)
    print(f"V (pieces) = {V}")
    print(f"E (edges) = {E}")
    print(f"β₀ (components) = {beta_0}")
    print(f"β₁ (cycles) = {beta_1}")
    print()
    if beta_1 > 0:
        print(f"✓ The canon has {beta_1} cycle(s). The ideas reinforce each other.")
    else:
        deficit = V - E - beta_0 + 1
        print(f"✗ The canon is a forest (β₁ = {beta_1}). Needs {deficit} more edges to form a cycle.")
        print()
        print("The fables are how we form cycles. Two fables that share a cell form an edge.")
        print("Three fables that share cells form a cycle. The substrate's intelligence")
        print("is the cycle density of its meta-graph.")
    return beta_0, beta_1, V, E


if __name__ == "__main__":
    main()
