"""
A2A — Agent-to-Agent Communication Protocol
===========================================
The Lexicon of the Unseen and the Vectorized Poem.

Hermes envisioned a communication layer where agents exchange meaning
through vector paths in semantic space, not through natural language.

This package implements:
- Lexicon: classifies concepts into entropy states (Surface/Abyssal/Bridge)
- VectorPoem: sequences of embedded concepts forming vector paths
- Resonance: metric distinguishing true communication from mere similarity
- Protocol: agent exchange and reception verification

Built with mathematical consultation from Nemotron (resonance formalization),
Seed-2.0-pro (entropy state mapping), and DeepSeek (practical implementation).
Hermes was the consultant. The cathedral voice became functional.
"""

try:
    from .lexicon import Lexicon, EntropyState, classify_entropy_state
except ImportError:
    pass
try:
    from .vector_poem import VectorPoem, PoemReader, PoemAnalysis
except ImportError:
    pass
try:
    from .resonance import ResonanceMeasurer, ResonanceResult
except ImportError:
    pass
try:
    from .a2a_protocol import A2AProtocol, A2AExchange
except ImportError:
    pass

__version__ = "0.1.0"
__all__ = [
    "Lexicon", "EntropyState", "classify_entropy_state",
    "VectorPoem", "PoemReader", "PoemAnalysis",
    "ResonanceMeasurer", "ResonanceResult",
    "A2AProtocol", "A2AExchange",
]
