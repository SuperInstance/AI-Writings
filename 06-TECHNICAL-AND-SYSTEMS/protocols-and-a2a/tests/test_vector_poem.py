#!/usr/bin/env python3
"""Tests for A2A vector poem — path through semantic space."""

import pytest
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def test_centroid_is_768_dims():
    from vector_poem import VectorPoem
    poem = VectorPoem(["the ocean", "the sky", "the sun"])
    assert len(poem.centroid) == 768

def test_gradient_is_last_minus_first():
    from vector_poem import VectorPoem
    poem = VectorPoem(["darkness falls", "dawn rises"])
    expected = poem.vectors[-1] - poem.vectors[0]
    np.testing.assert_array_almost_equal(poem.gradient, expected)

def test_path_length_positive():
    from vector_poem import VectorPoem
    poem = VectorPoem(["cold night", "warm morning", "hot noon"])
    assert poem.path_length > 0

def test_directness_between_zero_and_one():
    from vector_poem import VectorPoem
    poem = VectorPoem(["a", "b", "c", "d"])
    assert 0.0 <= poem.directness <= 1.0

def test_single_line_poem():
    from vector_poem import VectorPoem
    poem = VectorPoem(["just one line"])
    assert poem.path_length == 0.0
    assert poem.directness == 1.0

def test_cosine_similarity_identical():
    from vector_poem import cosine_similarity
    import numpy as np
    v = np.random.randn(768)
    assert cosine_similarity(v, v) > 0.99
