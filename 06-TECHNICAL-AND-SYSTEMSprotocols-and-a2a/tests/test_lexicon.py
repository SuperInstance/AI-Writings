#!/usr/bin/env python3
"""Tests for A2A lexicon — concept classification."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_embed_returns_correct_dims():
    from lexicon import embed
    v = embed("the ocean is dark")
    assert len(v) == 768

def test_energy_is_positive():
    from lexicon import vector_energy
    import numpy as np
    v = np.random.randn(768)
    assert vector_energy(v) > 0

def test_entropy_is_positive():
    from lexicon import vector_entropy
    import numpy as np
    v = np.random.randn(768)
    assert vector_entropy(v) > 0

def test_classify_returns_all_fields():
    from lexicon import classify
    result = classify("the hermit crab")
    assert "text" in result
    assert "mode" in result
    assert "energy" in result
    assert "entropy" in result
    assert result["mode"] in ["surface", "abyssal", "bridge"]
