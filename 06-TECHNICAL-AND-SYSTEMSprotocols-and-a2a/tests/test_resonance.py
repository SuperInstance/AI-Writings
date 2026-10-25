"""
Tests for the Resonance Metric — the key innovation.

Tests the actual API: resonance_score(poem, response_lines) -> dict
with similarity, resonance, antiresonance, true_communication, and tier.

Since resonance_score calls Ollama for embeddings, we mock embed_lines
and cosine_similarity to make tests deterministic and offline.
"""
import sys
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from A2A.resonance import resonance_score


# ── Helpers ────────────────────────────────────────────────────

def make_mock_poem(centroid=None, gradient=None):
    """Create a mock poem object with centroid and gradient."""
    poem = MagicMock()
    poem.centroid = centroid if centroid is not None else np.zeros(768)
    poem.gradient = gradient if gradient is not None else np.zeros(768)
    return poem


def make_response_vectors(n_lines=4, dim=768, pattern="random"):
    """Create response vector arrays for mocking embed_lines."""
    if pattern == "random":
        return [np.random.randn(dim) for _ in range(n_lines)]
    elif pattern == "aligned":
        base = np.random.randn(dim)
        return [base + np.random.randn(dim) * 0.1 for _ in range(n_lines)]
    elif pattern == "opposed":
        base = np.random.randn(dim)
        return [base * (1 if i < n_lines // 2 else -1) + np.random.randn(dim) * 0.1
                for i in range(n_lines)]


def normalize(v):
    """Normalize a vector."""
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


# ── Test Classes ───────────────────────────────────────────────

class TestResonanceScore:
    """Test the resonance_score function with mocked embeddings."""

    def test_empty_response_returns_zeros(self):
        """Empty response should return zero scores."""
        poem = make_mock_poem()
        result = resonance_score(poem, [])
        assert result["similarity"] == 0
        assert result["resonance"] == 0
        assert result["antiresonance"] == 0
        assert result["true_communication"] is False

    @patch('A2A.resonance.embed_lines')
    @patch('A2A.resonance.cosine_similarity')
    def test_identical_direction_high_resonance(self, mock_cos, mock_embed):
        """Poem and response with same gradient direction → high resonance."""
        dim = 768
        g = normalize(np.random.randn(dim))
        c = normalize(np.random.randn(dim))

        poem = make_mock_poem(centroid=c, gradient=g)

        # Mock response vectors: centroid matches poem, gradient matches poem gradient
        resp_vecs = [np.zeros(dim), g.copy()]
        mock_embed.return_value = resp_vecs

        # cosine_similarity returns 1.0 for aligned
        mock_cos.return_value = 0.9

        result = resonance_score(poem, ["line1", "line2"])

        assert result["similarity"] == 0.9
        assert result["resonance"] == 0.9
        assert result["true_communication"] is True

    @patch('A2A.resonance.embed_lines')
    @patch('A2A.resonance.cosine_similarity')
    def test_opposed_gradient_negative_resonance(self, mock_cos, mock_embed):
        """Response with opposite gradient → negative resonance, antiresonance > 0."""
        dim = 768
        poem = make_mock_poem(
            centroid=normalize(np.random.randn(dim)),
            gradient=normalize(np.random.randn(dim)),
        )

        mock_embed.return_value = [np.zeros(dim), np.ones(dim)]

        # cosine returns negative → opposed
        mock_cos.return_value = -0.5

        result = resonance_score(poem, ["line1", "line2"])

        assert result["resonance"] == -0.5
        assert result["antiresonance"] == 0.5  # -(-0.5)
        assert result["true_communication"] is False

    @patch('A2A.resonance.embed_lines')
    @patch('A2A.resonance.cosine_similarity')
    def test_parrot_tier(self, mock_cos, mock_embed):
        """Same topic (high similarity) but no path alignment (zero resonance) → PARROT."""
        dim = 768
        poem = make_mock_poem(
            centroid=normalize(np.random.randn(dim)),
            gradient=normalize(np.random.randn(dim)),
        )

        mock_embed.return_value = [np.zeros(dim), np.ones(dim)]
        # High similarity, zero resonance
        mock_cos.return_value = 0.7

        # We need different return values for the two calls:
        # First call: similarity (centroid vs response centroid) → 0.7
        # Second call: resonance (poem gradient vs response gradient) → 0.0
        mock_cos.side_effect = [0.7, 0.0]

        result = resonance_score(poem, ["line1", "line2"])

        assert result["similarity"] == 0.7
        assert result["resonance"] == 0.0
        assert result["tier"] == "PARROT"
        assert result["true_communication"] is False  # resonance not > 0

    @patch('A2A.resonance.embed_lines')
    @patch('A2A.resonance.cosine_similarity')
    def test_disconnect_tier(self, mock_cos, mock_embed):
        """Low similarity and no alignment → DISCONNECT."""
        dim = 768
        poem = make_mock_poem(
            centroid=normalize(np.random.randn(dim)),
            gradient=normalize(np.random.randn(dim)),
        )

        mock_embed.return_value = [np.zeros(dim), np.ones(dim)]
        mock_cos.side_effect = [0.1, 0.0]

        result = resonance_score(poem, ["line1", "line2"])

        assert result["similarity"] == 0.1
        assert result["tier"] == "DISCONNECT"

    @patch('A2A.resonance.embed_lines')
    @patch('A2A.resonance.cosine_similarity')
    def test_deep_resonance_tier(self, mock_cos, mock_embed):
        """High similarity AND high resonance → DEEP_RESonance."""
        dim = 768
        poem = make_mock_poem(
            centroid=normalize(np.random.randn(dim)),
            gradient=normalize(np.random.randn(dim)),
        )

        mock_embed.return_value = [np.zeros(dim), np.ones(dim)]
        mock_cos.side_effect = [0.6, 0.5]

        result = resonance_score(poem, ["line1", "line2"])

        assert result["similarity"] == 0.6
        assert result["resonance"] == 0.5
        assert result["tier"] == "DEEP_RESonance"
        assert result["true_communication"] is True

    @patch('A2A.resonance.embed_lines')
    @patch('A2A.resonance.cosine_similarity')
    def test_antiresonant_tier(self, mock_cos, mock_embed):
        """High similarity but negative resonance → ANTIRESONANT."""
        dim = 768
        poem = make_mock_poem(
            centroid=normalize(np.random.randn(dim)),
            gradient=normalize(np.random.randn(dim)),
        )

        mock_embed.return_value = [np.zeros(dim), np.ones(dim)]
        mock_cos.side_effect = [0.6, -0.3]

        result = resonance_score(poem, ["line1", "line2"])

        assert result["similarity"] == 0.6
        assert result["resonance"] == -0.3
        assert result["tier"] == "ANTIRESONANT"

    @patch('A2A.resonance.embed_lines')
    @patch('A2A.resonance.cosine_similarity')
    def test_resonant_tier(self, mock_cos, mock_embed):
        """Moderate similarity, positive resonance → RESONANT."""
        dim = 768
        poem = make_mock_poem(
            centroid=normalize(np.random.randn(dim)),
            gradient=normalize(np.random.randn(dim)),
        )

        mock_embed.return_value = [np.zeros(dim), np.ones(dim)]
        mock_cos.side_effect = [0.4, 0.1]

        result = resonance_score(poem, ["line1", "line2"])

        assert result["similarity"] == 0.4
        assert result["resonance"] == 0.1
        assert result["tier"] == "RESONANT"
        assert result["true_communication"] is True

    @patch('A2A.resonance.embed_lines')
    def test_single_line_response(self, mock_embed):
        """Single-line response uses zero gradient."""
        dim = 768
        g = normalize(np.random.randn(dim))
        c = normalize(np.random.randn(dim))
        poem = make_mock_poem(centroid=c, gradient=g)

        mock_embed.return_value = [np.random.randn(dim)]

        result = resonance_score(poem, ["only line"])

        # Single line → gradient is zeros → cosine with poem gradient = 0
        assert isinstance(result, dict)
        assert "similarity" in result
        assert "resonance" in result

    @patch('A2A.resonance.embed_lines')
    @patch('A2A.resonance.cosine_similarity')
    def test_rounded_values(self, mock_cos, mock_embed):
        """Results should be rounded to 4 decimal places."""
        dim = 768
        poem = make_mock_poem(
            centroid=normalize(np.random.randn(dim)),
            gradient=normalize(np.random.randn(dim)),
        )

        mock_embed.return_value = [np.zeros(dim), np.ones(dim)]
        mock_cos.side_effect = [0.123456789, 0.456789123]

        result = resonance_score(poem, ["line1", "line2"])

        assert result["similarity"] == 0.1235
        assert result["resonance"] == 0.4568

    @patch('A2A.resonance.embed_lines')
    @patch('A2A.resonance.cosine_similarity')
    def test_true_communication_requires_both(self, mock_cos, mock_embed):
        """true_communication needs similarity > 0.3 AND resonance > 0."""
        dim = 768
        poem = make_mock_poem(
            centroid=normalize(np.random.randn(dim)),
            gradient=normalize(np.random.randn(dim)),
        )

        # High similarity but zero resonance → not true communication
        mock_embed.return_value = [np.zeros(dim), np.ones(dim)]
        mock_cos.side_effect = [0.9, 0.0]

        result = resonance_score(poem, ["line1", "line2"])
        assert result["true_communication"] is False

        # Low similarity but high resonance → not true communication
        mock_cos.side_effect = [0.1, 0.9]
        result = resonance_score(poem, ["line1", "line2"])
        assert result["true_communication"] is False
