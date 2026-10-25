#!/usr/bin/env python3
"""
A2A Vector Poem — Poems as vector paths through semantic space.

A poem is a sequence of lines. Each line embeds to a point in 768-dim space.
The poem is a PATH through that space — and the path has GRADIENT (direction of meaning change).

Two poems about the same topic can have completely different paths:
- Poem A: starts dark, moves toward light (gradient points toward hope)
- Poem B: starts light, moves toward dark (gradient points toward grief)

The PATH is the meaning. The topic is just the starting point.
"""

import numpy as np
import json
import urllib.request
from typing import List

def embed(text: str, model: str = "nomic-embed-text") -> np.ndarray:
    data = json.dumps({"model": model, "prompt": text}).encode()
    req = urllib.request.Request("http://localhost:11434/api/embeddings", data=data)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return np.array(json.loads(resp.read())["embedding"])

def embed_lines(lines: List[str]) -> List[np.ndarray]:
    """Embed each line of a poem separately."""
    return [embed(line) for line in lines]

class VectorPoem:
    """A poem represented as a path through embedding space."""
    
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.vectors = embed_lines(lines) if lines else []
    
    @property
    def centroid(self) -> np.ndarray:
        """The center of the poem — its topic."""
        if not self.vectors:
            return np.zeros(768)
        return np.mean(self.vectors, axis=0)
    
    @property 
    def gradient(self) -> np.ndarray:
        """The direction the poem moves through semantic space.
        This is the MEANING of the path — where it starts to where it ends."""
        if len(self.vectors) < 2:
            return np.zeros(768)
        return self.vectors[-1] - self.vectors[0]
    
    @property
    def path_length(self) -> float:
        """Total semantic distance traveled."""
        if len(self.vectors) < 2:
            return 0.0
        total = 0.0
        for i in range(1, len(self.vectors)):
            total += np.linalg.norm(self.vectors[i] - self.vectors[i-1])
        return total
    
    @property
    def directness(self) -> float:
        """How directly the poem reaches its endpoint.
        1.0 = perfectly straight path. 0.0 = wanders endlessly."""
        if len(self.vectors) < 2 or self.path_length == 0:
            return 1.0
        chord = np.linalg.norm(self.gradient)
        return chord / self.path_length
    
    def line_gradients(self) -> List[np.ndarray]:
        """Gradient between each consecutive pair of lines."""
        if len(self.vectors) < 2:
            return []
        return [self.vectors[i] - self.vectors[i-1] for i in range(1, len(self.vectors))]
    
    def describe(self) -> dict:
        return {
            "lines": self.lines,
            "num_lines": len(self.lines),
            "path_length": self.path_length,
            "directness": self.directness,
            "gradient_norm": float(np.linalg.norm(self.gradient)),
        }

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    if norm == 0:
        return 0.0
    return float(np.dot(a, b) / norm)

if __name__ == "__main__":
    # Demo: two poems about the sea with different paths
    poem_a = VectorPoem([
        "The ocean is dark and cold",
        "Waves crash against the hull",
        "But dawn comes with gold light",
        "And the gulls sing us home"
    ])
    
    poem_b = VectorPoem([
        "The morning sun on calm water",
        "A gentle breeze carries us out",
        "But clouds gather on the horizon",
        "And the storm takes everything"
    ])
    
    print("POEM A (dark → light):")
    print(f"  Path length: {poem_a.path_length:.3f}")
    print(f"  Directness: {poem_a.directness:.3f}")
    print(f"  Gradient norm: {poem_a.describe()['gradient_norm']:.3f}")
    print()
    print("POEM B (light → dark):")
    print(f"  Path length: {poem_b.path_length:.3f}")
    print(f"  Directness: {poem_b.directness:.3f}")
    print(f"  Gradient norm: {poem_b.describe()['gradient_norm']:.3f}")
    print()
    
    grad_sim = cosine_similarity(poem_a.gradient, poem_b.gradient)
    cent_sim = cosine_similarity(poem_a.centroid, poem_b.centroid)
    print(f"Centroid similarity (same topic?): {cent_sim:.3f}")
    print(f"Gradient similarity (same path?): {grad_sim:.3f}")
    print("  → Same topic, OPPOSITE paths. This is the poem's true meaning.")
