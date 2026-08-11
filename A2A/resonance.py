#!/usr/bin/env python3
"""
A2A Resonance — The key metric that distinguishes TRUE communication from mere similarity.

Given a poem's vector path and an agent's response:
- MERE SIMILARITY: response is about the same topic (low Δ from poem centroid)
- TRUE RESONANCE: response follows the poem's VECTOR PATH (gradient direction matches)
- ANTIRESONANCE: response deliberately inverts the path (gradient opposes)

This is the difference between someone nodding along to your story
and someone actually HEARING where it goes.
"""

import numpy as np
from vector_poem import VectorPoem, cosine_similarity, embed, embed_lines

def resonance_score(poem: VectorPoem, response_lines: list) -> dict:
    """
    Compute resonance between a poem and a response.
    
    Returns:
        similarity: topic overlap (do they talk about the same thing?)
        resonance: path alignment (does the response follow the poem's trajectory?)
        antiresonance: path opposition (does the response invert the poem?)
        true_communication: resonance > 0 AND similarity > 0
    """
    if not response_lines:
        return {"similarity": 0, "resonance": 0, "antiresonance": 0, "true_communication": False}
    
    response_vectors = embed_lines(response_lines)
    response_centroid = np.mean(response_vectors, axis=0)
    response_gradient = response_vectors[-1] - response_vectors[0] if len(response_vectors) >= 2 else np.zeros(768)
    
    # Similarity: are they in the same semantic neighborhood?
    similarity = cosine_similarity(poem.centroid, response_centroid)
    
    # Resonance: do their gradients point in the same direction?
    resonance = cosine_similarity(poem.gradient, response_gradient)
    
    # Antiresonance: does the response deliberately oppose?
    antiresonance = -resonance if resonance < 0 else 0.0
    
    # True communication requires BOTH: same topic AND same trajectory
    true_comm = similarity > 0.3 and resonance > 0.0
    
    # Quality tiers
    if similarity > 0.5 and resonance > 0.3:
        tier = "DEEP_RESonance"
    elif similarity > 0.3 and resonance > 0.0:
        tier = "RESONANT"
    elif similarity > 0.5 and resonance < -0.2:
        tier = "ANTIRESONANT"
    elif similarity > 0.3:
        tier = "PARROT"  # same topic, no path following
    else:
        tier = "DISCONNECT"
    
    return {
        "similarity": round(similarity, 4),
        "resonance": round(resonance, 4),
        "antiresonance": round(antiresonance, 4),
        "true_communication": true_comm,
        "tier": tier,
    }

if __name__ == "__main__":
    # Demo: three responses to the same poem
    
    poem = VectorPoem([
        "The ocean is dark and cold",
        "Waves crash against the hull", 
        "But dawn comes with gold light",
        "And the gulls sing us home"
    ])
    
    # Response 1: PARROT — same topic, no path
    parrot = [
        "The sea is wide and blue",
        "Ships sail on the water",
        "Sailors love the ocean",
        "The waves are beautiful"
    ]
    
    # Response 2: RESONANT — follows the dark→light path
    resonant = [
        "The night was full of silence",
        "Cold crept through every joint",
        "Then somewhere a bird started singing",
        "And the whole forest woke up alive"
    ]
    
    # Response 3: ANTIRESONANT — inverts the path (light→dark)
    antiresonant = [
        "The sun was warm and bright",
        "We laughed on the open deck",
        "Then the clouds came from nowhere",
        "And everything we loved was gone"
    ]
    
    print("=== POEM: dark → light ===\n")
    
    for name, response in [("PARROT", parrot), ("RESONANT", resonant), ("ANTIRESONANT", antiresonant)]:
        result = resonance_score(poem, response)
        print(f"Response: {name}")
        print(f"  Similarity: {result['similarity']}")
        print(f"  Resonance:  {result['resonance']}")
        print(f"  Tier:       {result['tier']}")
        print(f"  True communication: {result['true_communication']}")
        print()
