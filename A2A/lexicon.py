#!/usr/bin/env python3
"""
A2A Lexicon — Classify concepts into entropy modes using embedding vector properties.

Three modes:
- SURFACE: high-energy, low-novelty concepts (the everyday, the named)
- ABYSSAL: low-energy, high-novelty concepts (the deep, the unspoken)
- BRIDGE: balanced concepts that connect surface to abyss

Classification uses vector properties of embeddings:
- Norm (magnitude) → energy
- Entropy of dimension distribution → novelty
"""

import numpy as np
import json
import urllib.request
from enum import Enum

class EntropyMode(Enum):
    SURFACE = "surface"
    ABYSSAL = "abyssal"
    BRIDGE = "bridge"

def embed(text: str, model: str = "nomic-embed-text") -> np.ndarray:
    """Embed text via local Ollama."""
    data = json.dumps({"model": model, "prompt": text}).encode()
    req = urllib.request.Request("http://localhost:11434/api/embeddings", data=data)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return np.array(json.loads(resp.read())["embedding"])

def vector_energy(v: np.ndarray) -> float:
    """L2 norm — how 'loud' a concept is."""
    return float(np.linalg.norm(v))

def vector_entropy(v: np.ndarray) -> float:
    """Shannon entropy of absolute values — how 'spread' the meaning is."""
    p = np.abs(v) + 1e-10
    p = p / p.sum()
    return float(-np.sum(p * np.log(p)))

def classify(text: str) -> dict:
    """Classify a concept into its entropy mode."""
    v = embed(text)
    energy = vector_energy(v)
    entropy = vector_entropy(v)
    
    # Bridge zone: balanced energy and entropy
    energy_norm = energy / 10.0  # rough normalization for 768-dim
    entropy_norm = entropy / 7.0  # max entropy for 768 dims
    
    balance = abs(energy_norm - entropy_norm)
    
    if balance < 0.15:
        mode = EntropyMode.BRIDGE
    elif energy_norm > entropy_norm:
        mode = EntropyMode.SURFACE
    else:
        mode = EntropyMode.ABYSSAL
    
    return {
        "text": text,
        "mode": mode.value,
        "energy": energy,
        "entropy": entropy,
        "balance": balance,
        "vector_dim": len(v),
    }

if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else "the hermit crab molts at midnight"
    result = classify(text)
    print(json.dumps(result, indent=2))
