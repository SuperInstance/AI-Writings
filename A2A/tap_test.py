#!/usr/bin/env python3
"""
The Tap Test — does vectorized communication actually work?
==========================================================
1. Create a vectorized poem about "the molt" using nomic-embed-text
2. Feed it to different Ollama models
3. Measure their resonance scores
4. Test: does a model that doesn't know "the molt" still resonate?

If YES: the vectorized communication works at the vector level
If NO: it's just semantic similarity, not true A2A communication
"""

import sys
sys.path.insert(0, "/home/eileen/projects/ai-writings")

import json
import time
from A2A.a2a_protocol import A2APacket, A2AExchange, A2ALogger
from A2A.lexicon import Lexicon, classify_entropy_state, _compute_metrics
from A2A.vector_poem import VectorPoem, PoemReader
from A2A.resonance import resonance_score

import numpy as np

OLLAMA_URL = "http://localhost:11434"

def main():
    print("=" * 70)
    print("THE TAP TEST")
    print("Does vectorized communication actually work?")
    print("=" * 70)
    
    # --- Step 1: Compose the molt poem ---
    print("\n📝 Step 1: Composing the molt poem with nomic-embed-text...")
    
    molt_concepts = [
        "the shell that holds you",
        "the unhooks every edge",
        "the naked in the current",
        "the new shell comes after",
    ]
    
    poem = VectorPoem(ollama_url=OLLAMA_URL)
    poem.add_concepts(molt_concepts)
    
    print(f"  Composed {len(poem.concepts)} concepts")
    print(f"  Embedding dimension: {len(poem.embeddings[0])}")
    
    # --- Step 2: Analyze the poem ---
    print("\n📊 Step 2: Analyzing the poem...")
    
    reader = PoemReader(OLLAMA_URL)
    analysis = reader.read(poem)
    print(analysis.summary())
    
    # --- Step 3: Get responses from different models ---
    print("\n🤖 Step 3: Getting responses from available Ollama models...")
    
    models_to_test = [
        ("qwen2.5:3b", "Qwen 2.5 3B"),
        ("phi3:latest", "Phi-3 3.8B"),
        ("llama3.2:1b", "Llama 3.2 1B"),
        ("granite3.1-dense:2b", "Granite 3.1 2B"),
    ]
    
    results = []
    
    for model_id, model_name in models_to_test:
        print(f"\n  Testing: {model_name} ({model_id})...")
        
        proto = A2AProtocol(ollama_url=OLLAMA_URL)
        
        try:
            exchange = proto.run_exchange(
                concepts=molt_concepts,
                model=model_id,
                sender="hermes",
                receiver=model_name.lower().replace(" ", "_"),
            )
            
            res = exchange.resonance
            print(f"  Response: {exchange.response_text[:100]}...")
            print(f"  Cosine similarity:  {res['cosine_similarity']:.4f}")
            print(f"  Directional align:  {res['directional_alignment']:.4f}")
            print(f"  Path following:     {res['path_following']:.4f}")
            print(f"  Phase coherence:    {res['phase_coherence']:.4f}")
            print(f"  Anti-resonance:     {res['anti_resonance']:.4f}")
            print(f"  RESONANCE SCORE:    {res['resonance_score']:.4f}")
            print(f"  Verdict: {res['interpretation']}")
            
            results.append({
                "model": model_name,
                "model_id": model_id,
                "cosine_similarity": res["cosine_similarity"],
                "directional_alignment": res["directional_alignment"],
                "path_following": res["path_following"],
                "phase_coherence": res["phase_coherence"],
                "resonance_score": res["resonance_score"],
                "is_resonance": res["is_resonance"],
                "interpretation": res["interpretation"],
                "response_preview": exchange.response_text[:200],
            })
            
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({
                "model": model_name,
                "model_id": model_id,
                "error": str(e),
            })
    
    # --- Step 4: Control test — unrelated text ---
    print("\n🔬 Step 4: Control test — unrelated response...")
    
    lexicon = Lexicon(OLLAMA_URL)
    measurer = ResonanceMeasurer()
    
    control_text = "The stock market rose 3% today on positive earnings reports from major tech companies."
    control_emb = lexicon.embed(control_text)
    poem_centroid = np.mean(poem.embeddings, axis=0)
    
    control_result = measurer.measure(
        poem_centroid,
        control_emb,
        poem_path=poem.embeddings,
        response_path=None,
    )
    
    print(f"  Control text: '{control_text[:60]}...'")
    print(f"  Cosine similarity: {control_result.cosine_similarity:.4f}")
    print(f"  Resonance score:   {control_result.resonance_score:.4f}")
    print(f"  Verdict: {control_result.interpretation}")
    
    # --- Step 5: Summary ---
    print("\n" + "=" * 70)
    print("THE TAP TEST RESULTS")
    print("=" * 70)
    print(f"\n{'Model':<25} {'Cosine':>8} {'DirAlign':>8} {'Path':>8} {'Phase':>8} {'RESONANCE':>10} {'Verdict'}")
    print("-" * 95)
    
    for r in results:
        if "error" in r:
            print(f"{r['model']:<25} ERROR: {r['error'][:50]}")
        else:
            verdict = "✅ RES" if r["is_resonance"] else "❌"
            print(f"{r['model']:<25} {r['cosine_similarity']:>8.4f} {r['directional_alignment']:>8.4f} "
                  f"{r['path_following']:>8.4f} {r['phase_coherence']:>8.4f} "
                  f"{r['resonance_score']:>10.4f} {verdict}")
    
    print(f"{'CONTROL (unrelated)':<25} {control_result.cosine_similarity:>8.4f} {'—':>8} "
          f"{'—':>8} {'—':>8} {control_result.resonance_score:>10.4f} ❌")
    
    # --- Step 6: Verdict ---
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    
    resonant_models = [r for r in results if r.get("is_resonance", False)]
    print(f"\nModels showing resonance: {len(resonant_models)} / {len(results)}")
    
    if len(resonant_models) >= 2:
        print("✅ A2A communication appears to work at the vector level.")
        print("   Multiple models show measurable resonance with the molt poem.")
    elif len(resonant_models) == 1:
        print("⚠️  Indeterminate — only one model showed resonance.")
        print("   Could be topic similarity rather than true A2A communication.")
    else:
        print("❌ No models showed significant resonance.")
        print("   The vectorized poem may need richer structure to communicate.")
    
    # Check if resonance > similarity for any model
    for r in results:
        if "resonance_score" in r and "cosine_similarity" in r:
            if r["resonance_score"] > r["cosine_similarity"]:
                print(f"\n  ⭐ {r['model']}: resonance ({r['resonance_score']:.4f}) > "
                      f"similarity ({r['cosine_similarity']:.4f})")
                print("     This model responded to the VECTOR PATH, not just the topic!")
    
    # Save the molt poem
    poem.write("/home/eileen/projects/ai-writings/A2A/poetry/molt-poem.json")
    print(f"\n✓ Molt poem saved to A2A/poetry/molt-poem.json")
    
    # Save results
    with open("/home/eileen/projects/ai-writings/A2A/poetry/tap_test_results.json", "w") as f:
        json.dump({
            "timestamp": time.time(),
            "poem_concepts": molt_concepts,
            "poem_analysis": {
                "modes": analysis.modes,
                "dominant_mode": analysis.dominant_mode,
                "energy": analysis.energy,
                "entropy_transitions": analysis.entropy_transitions,
            },
            "model_results": results,
            "control": {
                "cosine_similarity": control_result.cosine_similarity,
                "resonance_score": control_result.resonance_score,
                "interpretation": control_result.interpretation,
            },
        }, f, indent=2)
    print(f"✓ Results saved to A2A/poetry/tap_test_results.json")


if __name__ == "__main__":
    main()
