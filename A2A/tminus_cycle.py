#!/usr/bin/env python3
"""
T-Minus Vector Cycle — The simultaneous-voice chord engine.

Implements the four-phase cycle from the T-Minus × Vector Poem braid:

    T-MINUS  → predict_gradients(other_poems, your_style)
    T-ZERO   → play_simultaneous(all_poems)
    T-PLUS   → reconcile(all_poems)
    T-PLUS+  → update_prediction_model(history)

Plus the structural mechanisms:
    - fibonacci_tunnel(corpus, round_number)  — every 8 rounds, surface a dormant piece
    - anti_monoculture_check(poems)           — detect Δ < 0.2 convergence

Design principles:
    - One thread per function. Clarity. Contrast.
    - Works with synthetic vectors (no Ollama dependency for the cycle logic).
    - VectorPoem-like objects need: .centroid, .gradient, .lines, .path_length.

Usage:
    from tminus_cycle import TMinusCycle

    cycle = TMinusCycle()
    chord = cycle.play_simultaneous([poem_a, poem_b, poem_c])
    scores = cycle.reconcile([poem_a, poem_b, poem_c])
    surfaced = cycle.fibonacci_tunnel(corpus, round_number=8)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Optional
import numpy as np


# ── Helpers ────────────────────────────────────────────────────

def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity, zero-safe."""
    norm = float(np.linalg.norm(a) * np.linalg.norm(b))
    if norm == 0.0:
        return 0.0
    return float(np.dot(a, b) / norm)


def _gradient_diversity(gradients: list[np.ndarray]) -> float:
    """
    How spread are the individual gradients?
    High diversity (near 1.0) = healthy, multi-voiced.
    Low diversity (near 0.0) = monoculture, everyone converging.
    """
    if len(gradients) < 2:
        return 1.0
    # Pairwise cosine similarities, averaged, then inverted
    sims = []
    for i in range(len(gradients)):
        for j in range(i + 1, len(gradients)):
            sims.append(_cosine_similarity(gradients[i], gradients[j]))
    if not sims:
        return 1.0
    avg_sim = float(np.mean(sims))
    return 1.0 - abs(avg_sim)  # 0 = all identical, 1 = maximally spread


# ── Data Containers ────────────────────────────────────────────

@dataclass
class PoemLike:
    """
    A lightweight poem stand-in that doesn't require embeddings.
    Works with pre-computed vectors for testing and for the cycle logic.
    """
    lines: list[str]
    centroid: np.ndarray
    gradient: np.ndarray
    path_length: float = 0.0
    author: str = ""
    title: str = ""

    def describe(self) -> dict:
        return {
            "author": self.author,
            "title": self.title,
            "lines": self.lines,
            "path_length": self.path_length,
            "gradient_norm": float(np.linalg.norm(self.gradient)),
        }


@dataclass
class Prediction:
    """An agent's prediction of another agent's gradient."""
    predicted_gradient: np.ndarray
    actual_gradient: Optional[np.ndarray] = None
    accuracy: Optional[float] = None  # cosine sim between predicted and actual

    def compute_accuracy(self):
        if self.actual_gradient is not None:
            self.accuracy = _cosine_similarity(self.predicted_gradient, self.actual_gradient)
        return self.accuracy


@dataclass
class ChordResult:
    """The result of playing all poems simultaneously."""
    net_gradient: np.ndarray          # where the whole conversation moved
    gradient_diversity: float         # spread of individual gradients
    resonance_density: float          # fraction of resonant pairs
    seismic_events: list[dict]        # dormant gradients that surfaced
    centroid_shift: float             # how far the conversation centroid moved
    poems: list[dict] = field(default_factory=list)

    def summary(self) -> dict:
        return {
            "net_gradient_norm": float(np.linalg.norm(self.net_gradient)),
            "gradient_diversity": round(self.gradient_diversity, 4),
            "resonance_density": round(self.resonance_density, 4),
            "seismic_count": len(self.seismic_events),
            "centroid_shift": round(self.centroid_shift, 4),
            "num_poems": len(self.poems),
        }


@dataclass
class ReconcilePair:
    """Pairwise reconciliation between two poems."""
    poem_a: str
    poem_b: str
    similarity: float    # topic overlap
    resonance: float     # path alignment
    delta: float         # absolute gradient difference (for monoculture check)
    tier: str            # RESONANT, PARROT, ANTIRESONANT, DISCONNECT


@dataclass
class MonocultureWarning:
    """Triggered when gradients converge too closely."""
    pairs: list[tuple[str, str]]
    avg_delta: float
    message: str


# ── Corpus Piece (for Fibonacci tunnel) ────────────────────────

@dataclass
class CorpusPiece:
    """A piece in the corpus with retrieval metadata."""
    piece_id: str
    title: str
    gradient: np.ndarray
    centroid: np.ndarray
    retrieval_count: int = 0
    last_referenced_round: int = 0  # round it was last surfaced
    dormancy_rounds: int = 0        # rounds since last reference


# ── The Cycle ──────────────────────────────────────────────────

class TMinusCycle:
    """
    The T-Minus Vector Cycle engine.

    Holds prediction models and round state. Each method is one phase
    of the cycle, designed to be called in sequence.
    """

    def __init__(self, dim: int = 768, monoculture_threshold: float = 0.2):
        self.dim = dim
        self.monoculture_threshold = monoculture_threshold
        self.round_number = 0
        self.prediction_history: list[dict[str, Prediction]] = []
        self.accuracy_history: list[dict[str, float]] = []
        # Per-agent prediction models: agent_name → mean_gradient (running average)
        self.prediction_models: dict[str, np.ndarray] = {}

    # ── T-MINUS: Predict ───────────────────────────────────────

    def predict_gradients(
        self,
        other_poems: list[PoemLike],
        your_style: PoemLike,
    ) -> dict[str, Prediction]:
        """
        Predict what others will produce based on their past style.

        Uses the internal prediction model (updated each round via
        update_prediction_model). Falls back to centroid-based estimation
        if no history exists.

        Args:
            other_poems: Poems from other agents in PREVIOUS rounds (their style).
            your_style: Your own typical poem (for self-reference).

        Returns:
            Dict mapping author → Prediction with predicted_gradient.
        """
        predictions: dict[str, Prediction] = {}

        for poem in other_poems:
            author = poem.author or "unknown"

            if author in self.prediction_models:
                # Use learned model: the running average gradient
                predicted = self.prediction_models[author].copy()
            elif "__default__" in self.prediction_models:
                predicted = self.prediction_models["__default__"].copy()
            else:
                # No model yet — predict they'll follow their previous gradient
                predicted = poem.gradient.copy()

            predictions[author] = Prediction(predicted_gradient=predicted)

        # Store predictions for accuracy checking in next update_prediction_model
        self.prediction_history.append(predictions)
        return predictions

    # ── T-ZERO: Play Simultaneous ──────────────────────────────

    def play_simultaneous(
        self,
        all_poems: list[PoemLike],
        previous_centroid: Optional[np.ndarray] = None,
    ) -> ChordResult:
        """
        All voices at once. The chord.

        Computes the combined gradient field: net direction, diversity,
        resonance density, and any seismic events.

        Args:
            all_poems: Every poem produced this round.
            previous_centroid: The conversation centroid from last round
                               (for shift measurement).

        Returns:
            ChordResult with the full gradient field analysis.
        """
        if not all_poems:
            return ChordResult(
                net_gradient=np.zeros(self.dim),
                gradient_diversity=1.0,
                resonance_density=0.0,
                seismic_events=[],
                centroid_shift=0.0,
            )

        gradients = [p.gradient for p in all_poems]
        centroids = [p.centroid for p in all_poems]

        # Net gradient: where is the whole conversation moving?
        net_gradient = np.mean(gradients, axis=0)

        # Gradient diversity
        diversity = _gradient_diversity(gradients)

        # Resonance density: fraction of pairs with positive gradient alignment
        resonant_pairs = 0
        total_pairs = 0
        for i in range(len(gradients)):
            for j in range(i + 1, len(gradients)):
                sim = _cosine_similarity(gradients[i], gradients[j])
                if sim > 0.0:
                    resonant_pairs += 1
                total_pairs += 1
        resonance_density = resonant_pairs / max(total_pairs, 1)

        # Centroid shift
        current_centroid = np.mean(centroids, axis=0)
        if previous_centroid is not None:
            shift = float(np.linalg.norm(current_centroid - previous_centroid))
        else:
            shift = 0.0

        return ChordResult(
            net_gradient=net_gradient,
            gradient_diversity=diversity,
            resonance_density=resonance_density,
            seismic_events=[],  # populated by fibonacci_tunnel
            centroid_shift=shift,
            poems=[p.describe() for p in all_poems],
        )

    # ── T-PLUS: Reconcile ──────────────────────────────────────

    def reconcile(self, all_poems: list[PoemLike]) -> list[ReconcilePair]:
        """
        Compute resonance scores for all pairs.

        For each pair, determines:
        - similarity: topic overlap (centroid cosine)
        - resonance: path alignment (gradient cosine)
        - delta: absolute gradient difference norm (for monoculture detection)
        - tier: classification

        Args:
            all_poems: All poems from this round.

        Returns:
            List of ReconcilePair for every unique pair.
        """
        pairs: list[ReconcilePair] = []

        for i in range(len(all_poems)):
            for j in range(i + 1, len(all_poems)):
                a, b = all_poems[i], all_poems[j]

                similarity = _cosine_similarity(a.centroid, b.centroid)
                resonance = _cosine_similarity(a.gradient, b.gradient)
                delta = float(np.linalg.norm(a.gradient - b.gradient))

                if similarity > 0.5 and resonance > 0.3:
                    tier = "DEEP_RESONANCE"
                elif similarity > 0.3 and resonance > 0.0:
                    tier = "RESONANT"
                elif similarity > 0.5 and resonance < -0.2:
                    tier = "ANTIRESONANT"
                elif similarity > 0.3:
                    tier = "PARROT"
                else:
                    tier = "DISCONNECT"

                pairs.append(ReconcilePair(
                    poem_a=a.author or f"poem_{i}",
                    poem_b=b.author or f"poem_{j}",
                    similarity=round(similarity, 4),
                    resonance=round(resonance, 4),
                    delta=round(delta, 4),
                    tier=tier,
                ))

        return pairs

    # ── T-PLUS+: Update Prediction Model ───────────────────────

    def update_prediction_model(self, history: list[PoemLike]) -> dict[str, float]:
        """
        Learn from past rounds. Update the internal prediction model.

        For each author, maintains a running mean gradient — the prediction
        for what they'll produce next round.

        Args:
            history: All poems from the round just completed.

        Returns:
            Dict mapping author → prediction accuracy (if predictions existed).
        """
        accuracies: dict[str, float] = {}

        # Check accuracy of previous predictions
        if self.prediction_history:
            last_predictions = self.prediction_history[-1]
            for author, pred in last_predictions.items():
                # Find the actual poem from this author
                actual = next((p for p in history if (p.author or "unknown") == author), None)
                if actual:
                    pred.actual_gradient = actual.gradient.copy()
                    acc = pred.compute_accuracy()
                    if acc is not None:
                        accuracies[author] = round(acc, 4)

        self.accuracy_history.append(accuracies)

        # Update model: running mean of each author's gradients
        for poem in history:
            author = poem.author or "unknown"
            if author not in self.prediction_models:
                self.prediction_models[author] = {}
            if author not in self.prediction_models[author]:
                self.prediction_models[author] = poem.gradient.copy()
            else:
                # Running mean
                old = self.prediction_models[author]
                # Use a simple learning rate
                lr = 0.3
                self.prediction_models[author] = (1 - lr) * old + lr * poem.gradient

        # Update default model (mean of all)
        if history:
            all_grads = np.stack([p.gradient for p in history])
            default = np.mean(all_grads, axis=0)
            if "__default__" not in self.prediction_models:
                self.prediction_models["__default__"] = default
            else:
                old = self.prediction_models["__default__"]
                self.prediction_models["__default__"] = 0.5 * old + 0.5 * default

        self.round_number += 1
        return accuracies

    # ── Fibonacci Tunnel ───────────────────────────────────────

    def fibonacci_tunnel(
        self,
        corpus: list[CorpusPiece],
        round_number: int,
    ) -> Optional[dict]:
        """
        Every 8 rounds, surface a dormant piece.

        The Pisano period for mod 3 is 8 — this is mathematical.
        When the tunnel activates, the MOST dormant piece (highest
        dormancy_rounds, lowest retrieval_count) is surfaced.

        Its gradient may be completely perpendicular to the current
        conversation — that's the point. The tie-up lines break.

        Args:
            corpus: All pieces in the corpus with metadata.
            round_number: The current round number.

        Returns:
            dict with surfaced piece data if tunnel fires, None otherwise.
        """
        if round_number == 0 or round_number % 8 != 0:
            return None

        if not corpus:
            return None

        # Update dormancy for all pieces
        for piece in corpus:
            piece.dormancy_rounds = round_number - piece.last_referenced_round

        # Sort by dormancy (desc), then by retrieval count (asc)
        sorted_corpus = sorted(
            corpus,
            key=lambda p: (-p.dormancy_rounds, p.retrieval_count),
        )

        # Surface the most dormant piece
        surfaced = sorted_corpus[0]

        # Mark it as referenced this round
        surfaced.last_referenced_round = round_number
        surfaced.retrieval_count += 1
        surfaced.dormancy_rounds = 0

        return {
            "piece_id": surfaced.piece_id,
            "title": surfaced.title,
            "dormancy_rounds": round_number - surfaced.last_referenced_round + 1,  # how long it was dormant
            "retrieval_count": surfaced.retrieval_count,
            "gradient_norm": float(np.linalg.norm(surfaced.gradient)),
            "reason": (
                f"Fibonacci tunnel activated at round {round_number}. "
                f"'{surfaced.title}' surfaces from dormancy. "
                f"This is the tie-up line breaking — a dormant gradient "
                f"enters the conversation with a force from a new direction."
            ),
        }

    # ── Anti-Monoculture Check ─────────────────────────────────

    def anti_monoculture_check(
        self,
        poems: list[PoemLike],
    ) -> Optional[MonocultureWarning]:
        """
        Detect convergence: if any pair's Δ < threshold, flag it.

        When gradients converge too closely, agents are saying the same
        thing in the same direction. One must be forced to REFLECT (state 0),
        find a new gradient. The crab molts.

        Args:
            poems: All poems from this round.

        Returns:
            MonocultureWarning if convergence detected, None if healthy.
        """
        if len(poems) < 2:
            return None

        converging_pairs: list[tuple[str, str]] = []
        deltas: list[float] = []

        for i in range(len(poems)):
            for j in range(i + 1, len(poems)):
                a, b = poems[i], poems[j]
                delta = float(np.linalg.norm(a.gradient - b.gradient))
                deltas.append(delta)

                if delta < self.monoculture_threshold:
                    name_a = a.author or f"poem_{i}"
                    name_b = b.author or f"poem_{j}"
                    converging_pairs.append((name_a, name_b))

        if not converging_pairs:
            return None

        avg_delta = float(np.mean(deltas))

        return MonocultureWarning(
            pairs=converging_pairs,
            avg_delta=round(avg_delta, 4),
            message=(
                f"Anti-monoculture trigger: {len(converging_pairs)} pair(s) "
                f"converged below Δ = {self.monoculture_threshold}. "
                f"Agents must reflect (state 0) and find new gradients. "
                f"The crab molts."
            ),
        )

    # ── Full Cycle Convenience ─────────────────────────────────

    def run_full_cycle(
        self,
        all_poems: list[PoemLike],
        corpus: Optional[list[CorpusPiece]] = None,
        previous_centroid: Optional[np.ndarray] = None,
    ) -> dict:
        """
        Run all four phases plus structural checks.

        Returns a complete round report.
        """
        # T-MINUS: Predict (using previous round's poems as style input)
        predictions = self.predict_gradients(all_poems, all_poems[0] if all_poems else None)

        # T-ZERO: Play
        chord = self.play_simultaneous(all_poems, previous_centroid)

        # T-PLUS: Reconcile
        pairs = self.reconcile(all_poems)

        # Fibonacci tunnel
        seismic = None
        if corpus is not None:
            seismic = self.fibonacci_tunnel(corpus, self.round_number + 1)
            if seismic:
                chord.seismic_events.append(seismic)

        # Anti-monoculture
        monoculture = self.anti_monoculture_check(all_poems)

        # T-PLUS+: Update
        accuracies = self.update_prediction_model(all_poems)

        return {
            "round": self.round_number,
            "chord": chord.summary(),
            "pairs": [
                {"poem_a": p.poem_a, "poem_b": p.poem_b,
                 "similarity": p.similarity, "resonance": p.resonance,
                 "delta": p.delta, "tier": p.tier}
                for p in pairs
            ],
            "seismic_event": seismic,
            "monoculture_warning": (
                {"pairs": monoculture.pairs, "avg_delta": monoculture.avg_delta,
                 "message": monoculture.message}
                if monoculture else None
            ),
            "prediction_accuracies": accuracies,
            "net_gradient_norm": float(np.linalg.norm(chord.net_gradient)),
            "gradient_diversity": round(chord.gradient_diversity, 4),
            "resonance_density": round(chord.resonance_density, 4),
        }


# ── Module-level convenience functions ─────────────────────────

def predict_gradients(other_poems, your_style):
    """Stateless convenience: predict others' gradients."""
    cycle = TMinusCycle()
    return cycle.predict_gradients(other_poems, your_style)


def play_simultaneous(all_poems, previous_centroid=None):
    """Stateless convenience: play all voices at once."""
    cycle = TMinusCycle()
    return cycle.play_simultaneous(all_poems, previous_centroid)


def reconcile(all_poems):
    """Stateless convenience: compute all pairwise resonance scores."""
    cycle = TMinusCycle()
    return cycle.reconcile(all_poems)


def update_prediction_model(history):
    """Stateless convenience: update from history."""
    cycle = TMinusCycle()
    return cycle.update_prediction_model(history)


def fibonacci_tunnel(corpus, round_number):
    """Stateless convenience: surface dormant piece every 8 rounds."""
    cycle = TMinusCycle()
    return cycle.fibonacci_tunnel(corpus, round_number)


def anti_monoculture_check(poems, threshold=0.2):
    """Stateless convenience: detect convergence."""
    cycle = TMinusCycle(monoculture_threshold=threshold)
    return cycle.anti_monoculture_check(poems)


if __name__ == "__main__":
    # Demo with synthetic vectors
    rng = np.random.RandomState(42)

    poems = [
        PoemLike(
            lines=["dark night", "cold water", "dawn breaks", "warmth comes"],
            centroid=rng.randn(128),
            gradient=rng.randn(128),
            author="Hermes",
            title="Dark to Light",
        ),
        PoemLike(
            lines=["silence in hull", "engine cools", "someone laughs", "bar is warm"],
            centroid=rng.randn(128),
            gradient=rng.randn(128),
            author="Wesley",
            title="Distance to Connection",
        ),
    ]

    cycle = TMinusCycle(dim=128)
    report = cycle.run_full_cycle(poems)
    import json
    print(json.dumps(report, indent=2, default=str))
