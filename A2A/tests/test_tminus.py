"""
Tests for T-Minus Vector Cycle — the simultaneous-voice chord engine.

Tests cover:
- predict_gradients: prediction from history and fallback
- play_simultaneous: chord computation (net gradient, diversity, resonance density)
- reconcile: pairwise scoring and tiering
- update_prediction_model: learning and accuracy tracking
- fibonacci_tunnel: fires at round 8, not at other rounds, surfaces most dormant
- anti_monoculture_check: detects Δ < 0.2, passes on diverse gradients

All tests use synthetic vectors — no Ollama/embedding dependency.
"""
import sys
import pytest
import numpy as np
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tminus_cycle import (
    TMinusCycle,
    PoemLike,
    CorpusPiece,
    Prediction,
    ChordResult,
    ReconcilePair,
    MonocultureWarning,
    _cosine_similarity,
    _gradient_diversity,
    predict_gradients,
    play_simultaneous,
    reconcile,
    fibonacci_tunnel,
    anti_monoculture_check,
)


# ── Fixtures ───────────────────────────────────────────────────

@pytest.fixture
def rng():
    return np.random.RandomState(42)


@pytest.fixture
def dim():
    return 64


@pytest.fixture
def make_poem(rng, dim):
    """Factory for creating PoemLike objects with synthetic vectors."""
    def _make(author="", title="", lines=None, gradient=None, centroid=None):
        return PoemLike(
            lines=lines or [f"{author} line 1", f"{author} line 2"],
            centroid=centroid if centroid is not None else rng.randn(dim),
            gradient=gradient if gradient is not None else rng.randn(dim),
            author=author,
            title=title,
        )
    return _make


@pytest.fixture
def make_corpus(rng, dim):
    """Factory for CorpusPiece objects."""
    def _make(piece_id, title, retrieval_count=0, last_referenced_round=0,
              gradient=None, centroid=None):
        return CorpusPiece(
            piece_id=piece_id,
            title=title,
            gradient=gradient if gradient is not None else rng.randn(dim),
            centroid=centroid if centroid is not None else rng.randn(dim),
            retrieval_count=retrieval_count,
            last_referenced_round=last_referenced_round,
        )
    return _make


# ── Helper tests ───────────────────────────────────────────────

class TestCosineSimilarity:
    def test_identical_vectors(self):
        v = np.array([1.0, 2.0, 3.0])
        assert _cosine_similarity(v, v) == pytest.approx(1.0, abs=1e-6)

    def test_opposite_vectors(self):
        v = np.array([1.0, 2.0, 3.0])
        assert _cosine_similarity(v, -v) == pytest.approx(-1.0, abs=1e-6)

    def test_orthogonal_vectors(self):
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        assert _cosine_similarity(a, b) == pytest.approx(0.0, abs=1e-6)

    def test_zero_vector(self):
        a = np.zeros(5)
        b = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        assert _cosine_similarity(a, b) == 0.0


class TestGradientDiversity:
    def test_identical_gradients_low_diversity(self):
        g = np.ones(10)
        assert _gradient_diversity([g, g, g]) == pytest.approx(0.0, abs=1e-6)

    def test_orthogonal_gradients_high_diversity(self):
        g1 = np.zeros(10); g1[0] = 1.0
        g2 = np.zeros(10); g2[1] = 1.0
        g3 = np.zeros(10); g3[2] = 1.0
        diversity = _gradient_diversity([g1, g2, g3])
        assert diversity == pytest.approx(1.0, abs=1e-6)

    def test_single_gradient_returns_one(self):
        g = np.ones(10)
        assert _gradient_diversity([g]) == 1.0

    def test_empty_returns_one(self):
        assert _gradient_diversity([]) == 1.0


# ── predict_gradients ──────────────────────────────────────────

class TestPredictGradients:
    def test_fallback_to_previous_gradient(self, make_poem, dim):
        """With no prediction model, should predict others' previous gradient."""
        cycle = TMinusCycle(dim=dim)
        other = make_poem(author="Flash", gradient=np.ones(dim))
        you = make_poem(author="Hermes", gradient=np.zeros(dim))

        preds = cycle.predict_gradients([other], you)

        assert "Flash" in preds
        np.testing.assert_array_almost_equal(
            preds["Flash"].predicted_gradient, other.gradient
        )

    def test_prediction_from_learned_model(self, make_poem, dim):
        """After learning, should use the model instead of raw gradient."""
        cycle = TMinusCycle(dim=dim)

        # Feed history to build model
        poem1 = make_poem(author="Flash", gradient=np.ones(dim))
        cycle.update_prediction_model([poem1])

        # Now predict — should use learned model
        other = make_poem(author="Flash", gradient=np.zeros(dim))
        preds = cycle.predict_gradients([other], make_poem(author="Hermes"))

        # Model should be close to ones (from poem1), not zeros
        pred_mean = float(np.mean(preds["Flash"].predicted_gradient))
        assert pred_mean > 0.5  # closer to 1.0 than 0.0

    def test_multiple_authors(self, make_poem, dim):
        cycle = TMinusCycle(dim=dim)
        others = [
            make_poem(author="Flash", gradient=np.ones(dim)),
            make_poem(author="Wesley", gradient=np.zeros(dim)),
            make_poem(author="Pro", gradient=np.ones(dim) * 0.5),
        ]
        preds = cycle.predict_gradients(others, make_poem(author="Hermes"))

        assert len(preds) == 3
        assert "Flash" in preds
        assert "Wesley" in preds
        assert "Pro" in preds

    def test_empty_other_poems(self, dim):
        cycle = TMinusCycle(dim=dim)
        preds = cycle.predict_gradients([], None)
        assert preds == {}


# ── play_simultaneous ──────────────────────────────────────────

class TestPlaySimultaneous:
    def test_net_gradient_is_mean(self, make_poem, dim):
        """Net gradient should be the mean of all poem gradients."""
        cycle = TMinusCycle(dim=dim)
        g1 = np.ones(dim)
        g2 = np.zeros(dim)
        poems = [
            make_poem(author="A", gradient=g1),
            make_poem(author="B", gradient=g2),
        ]
        chord = cycle.play_simultaneous(poems)
        np.testing.assert_array_almost_equal(chord.net_gradient, np.mean([g1, g2], axis=0))

    def test_empty_poems(self, dim):
        cycle = TMinusCycle(dim=dim)
        chord = cycle.play_simultaneous([])
        assert chord.gradient_diversity == 1.0
        assert chord.resonance_density == 0.0
        assert chord.centroid_shift == 0.0

    def test_resonance_density_all_aligned(self, make_poem, dim):
        """All gradients aligned → resonance density = 1.0."""
        cycle = TMinusCycle(dim=dim)
        g = np.ones(dim)
        poems = [
            make_poem(author="A", gradient=g),
            make_poem(author="B", gradient=g * 2),  # same direction
            make_poem(author="C", gradient=g * 3),
        ]
        chord = cycle.play_simultaneous(poems)
        assert chord.resonance_density == pytest.approx(1.0)

    def test_resonance_density_mixed(self, make_poem, dim):
        """Half aligned, half opposing → resonance density ≈ 0.33."""
        cycle = TMinusCycle(dim=dim)
        g = np.ones(dim)
        poems = [
            make_poem(author="A", gradient=g),
            make_poem(author="B", gradient=g),         # aligned with A
            make_poem(author="C", gradient=-g),        # opposed to A and B
        ]
        chord = cycle.play_simultaneous(poems)
        # Pairs: (A,B) align, (A,C) oppose, (B,C) oppose → 1/3 resonant
        assert chord.resonance_density == pytest.approx(1.0 / 3.0, abs=0.01)

    def test_centroid_shift(self, make_poem, dim):
        """Centroid shift should be distance between centroids."""
        cycle = TMinusCycle(dim=dim)
        prev = np.zeros(dim)
        poem = make_poem(author="A", centroid=np.ones(dim))
        chord = cycle.play_simultaneous([poem], previous_centroid=prev)
        expected_shift = float(np.linalg.norm(np.ones(dim) - np.zeros(dim)))
        assert chord.centroid_shift == pytest.approx(expected_shift)

    def test_centroid_shift_no_previous(self, make_poem, dim):
        cycle = TMinusCycle(dim=dim)
        poem = make_poem(author="A")
        chord = cycle.play_simultaneous([poem])
        assert chord.centroid_shift == 0.0

    def test_summary(self, make_poem, dim):
        cycle = TMinusCycle(dim=dim)
        chord = cycle.play_simultaneous([make_poem(author="A")])
        s = chord.summary()
        assert "net_gradient_norm" in s
        assert "gradient_diversity" in s
        assert "resonance_density" in s
        assert "num_poems" in s
        assert s["num_poems"] == 1


# ── reconcile ──────────────────────────────────────────────────

class TestReconcile:
    def test_resonant_pair(self, make_poem, dim):
        """Same gradient direction, similar centroids → RESONANT or DEEP_RESONANCE."""
        cycle = TMinusCycle(dim=dim)
        g = np.ones(dim)
        c = np.ones(dim)
        poems = [
            make_poem(author="A", gradient=g, centroid=c),
            make_poem(author="B", gradient=g * 2, centroid=c * 1.01),
        ]
        pairs = cycle.reconcile(poems)
        assert len(pairs) == 1
        assert pairs[0].resonance > 0.99
        assert pairs[0].similarity > 0.99
        assert pairs[0].tier in ("RESONANT", "DEEP_RESONANCE")

    def test_antiresonant_pair(self, make_poem, dim):
        """Opposite gradients, same centroid → ANTIRESONANT."""
        cycle = TMinusCycle(dim=dim)
        g = np.ones(dim)
        c = np.ones(dim)
        poems = [
            make_poem(author="A", gradient=g, centroid=c),
            make_poem(author="B", gradient=-g, centroid=c),
        ]
        pairs = cycle.reconcile(poems)
        assert len(pairs) == 1
        assert pairs[0].resonance < -0.99
        assert pairs[0].tier == "ANTIRESONANT"

    def test_parrot_pair(self, make_poem, dim):
        """Same topic, orthogonal gradients → PARROT."""
        cycle = TMinusCycle(dim=dim)
        c = np.ones(dim)
        g1 = np.zeros(dim); g1[0] = 1.0
        g2 = np.zeros(dim); g2[1] = 1.0
        poems = [
            make_poem(author="A", gradient=g1, centroid=c),
            make_poem(author="B", gradient=g2, centroid=c),
        ]
        pairs = cycle.reconcile(poems)
        assert len(pairs) == 1
        assert pairs[0].similarity > 0.5
        assert pairs[0].resonance == pytest.approx(0.0, abs=1e-6)
        assert pairs[0].tier == "PARROT"

    def test_disconnect_pair(self, make_poem, dim):
        """Different topics, orthogonal gradients → DISCONNECT."""
        cycle = TMinusCycle(dim=dim)
        g1 = np.zeros(dim); g1[0] = 1.0
        g2 = np.zeros(dim); g2[1] = 1.0
        c1 = np.zeros(dim); c1[0] = 1.0
        c2 = np.zeros(dim); c2[1] = 1.0
        poems = [
            make_poem(author="A", gradient=g1, centroid=c1),
            make_poem(author="B", gradient=g2, centroid=c2),
        ]
        pairs = cycle.reconcile(poems)
        assert len(pairs) == 1
        assert pairs[0].tier == "DISCONNECT"

    def test_all_pairs_returned(self, make_poem, dim):
        """n poems → n*(n-1)/2 pairs."""
        cycle = TMinusCycle(dim=dim)
        poems = [make_poem(author=f"A{i}") for i in range(5)]
        pairs = cycle.reconcile(poems)
        assert len(pairs) == 10  # 5*4/2

    def test_delta_computed(self, make_poem, dim):
        """Delta is the L2 norm of gradient difference."""
        cycle = TMinusCycle(dim=dim)
        g1 = np.zeros(dim); g1[0] = 3.0
        g2 = np.zeros(dim); g2[0] = 0.0
        poems = [
            make_poem(author="A", gradient=g1),
            make_poem(author="B", gradient=g2),
        ]
        pairs = cycle.reconcile(poems)
        assert pairs[0].delta == pytest.approx(3.0, abs=1e-4)


# ── update_prediction_model ────────────────────────────────────

class TestUpdatePredictionModel:
    def test_model_starts_empty(self, dim):
        cycle = TMinusCycle(dim=dim)
        assert cycle.prediction_models == {}

    def test_model_populated_after_update(self, make_poem, dim):
        cycle = TMinusCycle(dim=dim)
        poem = make_poem(author="Flash", gradient=np.ones(dim))
        cycle.update_prediction_model([poem])
        assert "Flash" in cycle.prediction_models

    def test_model_converges_toward_recent(self, make_poem, dim):
        """Model should shift toward recent gradients with learning rate."""
        cycle = TMinusCycle(dim=dim)
        # Round 1: Flash goes in +1 direction
        cycle.update_prediction_model([
            make_poem(author="Flash", gradient=np.ones(dim))
        ])
        model1 = cycle.prediction_models["Flash"].copy()

        # Round 2: Flash shifts toward 0
        cycle.update_prediction_model([
            make_poem(author="Flash", gradient=np.zeros(dim))
        ])
        model2 = cycle.prediction_models["Flash"]

        # Model should have shifted toward 0
        assert float(np.mean(model2)) < float(np.mean(model1))

    def test_accuracy_tracked(self, make_poem, dim):
        """After a round with predictions, accuracy should be computed."""
        cycle = TMinusCycle(dim=dim)

        # Round 1: build model
        g1 = np.ones(dim)
        poem1 = make_poem(author="Flash", gradient=g1)
        cycle.update_prediction_model([poem1])

        # Round 2: predict
        other = make_poem(author="Flash", gradient=np.ones(dim))
        cycle.predict_gradients([other], make_poem(author="Hermes"))

        # Round 2: actual — Flash goes in a different direction
        g2 = np.zeros(dim)
        poem2 = make_poem(author="Flash", gradient=g2)
        accuracies = cycle.update_prediction_model([poem2])

        assert "Flash" in accuracies
        # Predicted ~ones, actual zeros → low accuracy
        assert accuracies["Flash"] < 0.5

    def test_round_number_increments(self, make_poem, dim):
        cycle = TMinusCycle(dim=dim)
        assert cycle.round_number == 0
        cycle.update_prediction_model([make_poem(author="A")])
        assert cycle.round_number == 1
        cycle.update_prediction_model([make_poem(author="A")])
        assert cycle.round_number == 2


# ── fibonacci_tunnel ───────────────────────────────────────────

class TestFibonacciTunnel:
    def test_fires_at_round_8(self, make_corpus, dim):
        """The tunnel MUST fire at round 8."""
        cycle = TMinusCycle(dim=dim)
        corpus = [make_corpus("piece-1", "Dormant Piece", retrieval_count=0, last_referenced_round=0)]
        result = cycle.fibonacci_tunnel(corpus, round_number=8)
        assert result is not None
        assert result["piece_id"] == "piece-1"
        assert "Fibonacci tunnel" in result["reason"]

    def test_does_not_fire_before_8(self, make_corpus, dim):
        cycle = TMinusCycle(dim=dim)
        corpus = [make_corpus("p1", "t1")]
        for r in range(1, 8):
            result = cycle.fibonacci_tunnel(corpus, round_number=r)
            assert result is None, f"Tunnel should not fire at round {r}"

    def test_fires_at_16_24_etc(self, make_corpus, dim):
        cycle = TMinusCycle(dim=dim)
        corpus = [make_corpus("p1", "T1")]
        for r in [16, 24, 32, 40]:
            result = cycle.fibonacci_tunnel(corpus, round_number=r)
            assert result is not None, f"Tunnel should fire at round {r}"

    def test_does_not_fire_at_non_multiples(self, make_corpus, dim):
        cycle = TMinusCycle(dim=dim)
        corpus = [make_corpus("p1", "T1")]
        for r in [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15]:
            result = cycle.fibonacci_tunnel(corpus, round_number=r)
            assert result is None, f"Tunnel should NOT fire at round {r}"

    def test_does_not_fire_at_round_0(self, make_corpus, dim):
        cycle = TMinusCycle(dim=dim)
        corpus = [make_corpus("p1", "T1")]
        result = cycle.fibonacci_tunnel(corpus, round_number=0)
        assert result is None

    def test_surfaces_most_dormant(self, make_corpus, dim):
        """Should surface the piece with the most dormancy and fewest retrievals."""
        cycle = TMinusCycle(dim=dim)
        corpus = [
            make_corpus("hot", "Hot Piece", retrieval_count=100, last_referenced_round=7),
            make_corpus("dormant", "Dormant Piece", retrieval_count=0, last_referenced_round=0),
            make_corpus("medium", "Medium Piece", retrieval_count=5, last_referenced_round=4),
        ]
        result = cycle.fibonacci_tunnel(corpus, round_number=8)
        assert result is not None
        assert result["piece_id"] == "dormant"

    def test_updates_dormancy_after_surfacing(self, make_corpus, dim):
        """After surfacing, the piece should be marked as recently referenced."""
        cycle = TMinusCycle(dim=dim)
        corpus = [make_corpus("p1", "T1", retrieval_count=0, last_referenced_round=0)]
        result = cycle.fibonacci_tunnel(corpus, round_number=8)
        assert result is not None
        assert corpus[0].last_referenced_round == 8
        assert corpus[0].retrieval_count == 1

    def test_empty_corpus(self, dim):
        cycle = TMinusCycle(dim=dim)
        result = cycle.fibonacci_tunnel([], round_number=8)
        assert result is None


# ── anti_monoculture_check ─────────────────────────────────────

class TestAntiMonocultureCheck:
    def test_detects_convergence(self, make_poem, dim):
        """Δ < 0.2 should trigger the warning."""
        cycle = TMinusCycle(dim=dim, monoculture_threshold=0.2)
        g = np.ones(dim)
        poems = [
            make_poem(author="A", gradient=g),
            make_poem(author="B", gradient=g * 1.01),  # nearly identical
        ]
        warning = cycle.anti_monoculture_check(poems)
        assert warning is not None
        assert ("A", "B") in warning.pairs
        assert "monoculture" in warning.message.lower() or "molts" in warning.message.lower()

    def test_passes_on_diverse_gradients(self, make_poem, dim):
        cycle = TMinusCycle(dim=dim)
        poems = [
            make_poem(author="A", gradient=np.ones(dim)),
            make_poem(author="B", gradient=np.ones(dim) * 10),  # very different magnitude
        ]
        warning = cycle.anti_monoculture_check(poems)
        # delta = ||ones - 10*ones|| = 9*sqrt(dim) — well above 0.2
        assert warning is None

    def test_threshold_customizable(self, make_poem, dim):
        """Should respect custom threshold values."""
        g = np.ones(dim)

        # Loose threshold: no warning
        cycle_loose = TMinusCycle(dim=dim, monoculture_threshold=0.001)
        poems = [
            make_poem(author="A", gradient=g),
            make_poem(author="B", gradient=g * (1 + 1e-5)),
        ]
        assert cycle_loose.anti_monoculture_check(poems) is None

        # Tight threshold: warning fires
        cycle_tight = TMinusCycle(dim=dim, monoculture_threshold=0.1)
        # Create a small delta
        g2 = g.copy()
        g2[0] += 0.05  # small perturbation
        poems2 = [
            make_poem(author="A", gradient=g),
            make_poem(author="B", gradient=g2),
        ]
        warning = cycle_tight.anti_monoculture_check(poems2)
        assert warning is not None

    def test_single_poem_no_warning(self, make_poem, dim):
        cycle = TMinusCycle(dim=dim)
        warning = cycle.anti_monoculture_check([make_poem(author="Solo")])
        assert warning is None

    def test_empty_poems_no_warning(self, dim):
        cycle = TMinusCycle(dim=dim)
        warning = cycle.anti_monoculture_check([])
        assert warning is None

    def test_multiple_converging_pairs(self, make_poem, dim):
        """Multiple pairs converging → all flagged."""
        cycle = TMinusCycle(dim=dim, monoculture_threshold=0.2)
        g = np.ones(dim)
        poems = [
            make_poem(author="A", gradient=g),
            make_poem(author="B", gradient=g * 1.01),
            make_poem(author="C", gradient=g * 0.99),
        ]
        warning = cycle.anti_monoculture_check(poems)
        assert warning is not None
        assert len(warning.pairs) == 3  # (A,B), (A,C), (B,C)


# ── Full cycle integration ─────────────────────────────────────

class TestFullCycle:
    def test_run_full_cycle_returns_report(self, make_poem, dim):
        cycle = TMinusCycle(dim=dim)
        poems = [
            make_poem(author="A"),
            make_poem(author="B"),
            make_poem(author="C"),
        ]
        report = cycle.run_full_cycle(poems)
        assert "round" in report
        assert "chord" in report
        assert "pairs" in report
        assert len(report["pairs"]) == 3  # 3*2/2

    def test_full_cycle_with_seismic(self, make_poem, make_corpus, dim):
        """At round 8, the tunnel should fire during a full cycle."""
        cycle = TMinusCycle(dim=dim)
        # Run 7 rounds to get to round 7
        for i in range(7):
            cycle.run_full_cycle([make_poem(author="A")])

        # Round 8 should trigger the tunnel
        report = cycle.run_full_cycle(
            [make_poem(author="A")],
            corpus=[make_corpus("dormant", "Old Piece", last_referenced_round=0)],
        )
        # The tunnel fires at round_number + 1 inside run_full_cycle
        # After 7 rounds, round_number is 7, so it fires at round 8
        assert report["seismic_event"] is not None
        assert report["seismic_event"]["piece_id"] == "dormant"

    def test_full_cycle_increments_round(self, make_poem, dim):
        cycle = TMinusCycle(dim=dim)
        report1 = cycle.run_full_cycle([make_poem(author="A")])
        report2 = cycle.run_full_cycle([make_poem(author="A")])
        assert report2["round"] > report1["round"]


# ── Module-level functions ─────────────────────────────────────

class TestModuleLevelFunctions:
    def test_module_predict_gradients(self, make_poem, dim):
        poems = [make_poem(author="A")]
        preds = predict_gradients(poems, make_poem(author="B"))
        assert "A" in preds

    def test_module_play_simultaneous(self, make_poem, dim):
        chord = play_simultaneous([make_poem(author="A"), make_poem(author="B")])
        assert isinstance(chord, ChordResult)

    def test_module_reconcile(self, make_poem, dim):
        pairs = reconcile([make_poem(author="A"), make_poem(author="B")])
        assert len(pairs) == 1

    def test_module_fibonacci_tunnel(self, make_corpus, dim):
        corpus = [make_corpus("p1", "T1")]
        result = fibonacci_tunnel(corpus, 8)
        assert result is not None

    def test_module_fibonacci_tunnel_no_fire(self, make_corpus, dim):
        corpus = [make_corpus("p1", "T1")]
        result = fibonacci_tunnel(corpus, 7)
        assert result is None

    def test_module_anti_monoculture(self, make_poem, dim):
        g = np.ones(dim)
        warning = anti_monoculture_check(
            [make_poem(author="A", gradient=g),
             make_poem(author="B", gradient=g)],
            threshold=0.2,
        )
        assert warning is not None


# ── PoemLike dataclass ─────────────────────────────────────────

class TestPoemLike:
    def test_describe(self, dim):
        p = PoemLike(
            lines=["hello", "world"],
            centroid=np.ones(dim),
            gradient=np.ones(dim),
            author="Test",
            title="Test Poem",
        )
        d = p.describe()
        assert d["author"] == "Test"
        assert d["title"] == "Test Poem"
        assert d["lines"] == ["hello", "world"]

    def test_default_values(self):
        p = PoemLike(lines=[], centroid=np.zeros(4), gradient=np.zeros(4))
        assert p.author == ""
        assert p.title == ""
        assert p.path_length == 0.0
