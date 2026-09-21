#!/usr/bin/env python3
"""
JEPA Dual-Database Bridge — perception + prediction as separate vector spaces.

Adapted from SuperInstance/plato-jepa-dual (Rust). The substrate's predictive
layer separates:
- perception_db: what the cell senses (input vector space)
- prediction_db: what the cell predicts (output vector space)

The two are mapped via a learned projection. Surprise = distance between
perception and prediction (after projection).

Key insight: perception and prediction live in DIFFERENT vector spaces,
with the cross-database mapping being the actual "intelligence" of the cell.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import math


@dataclass
class Vector:
    """A simple vector with distance metrics."""
    data: List[float]
    dim: int = 0

    def __post_init__(self):
        self.dim = len(self.data)

    def distance(self, other: "Vector") -> float:
        """Euclidean distance."""
        if self.dim != other.dim:
            raise ValueError(f"dimension mismatch: {self.dim} vs {other.dim}")
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(self.data, other.data)))

    def cosine_similarity(self, other: "Vector") -> float:
        """Cosine similarity."""
        dot = sum(a * b for a, b in zip(self.data, other.data))
        norm_a = math.sqrt(sum(a * a for a in self.data))
        norm_b = math.sqrt(sum(b * b for b in other.data))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def project(self, matrix: List[List[float]]) -> "Vector":
        """Project this vector through a transformation matrix."""
        new_dim = len(matrix)
        new_data = [0.0] * new_dim
        for i in range(new_dim):
            for j in range(self.dim):
                new_data[i] += matrix[i][j] * self.data[j]
        return Vector(new_data)


class DualJEPADatabase:
    """A JEPA cell with separate perception + prediction databases."""

    def __init__(self, dim: int = 8, name: str = "jepa-cell"):
        self.name = name
        self.dim = dim
        # Initialize as approximate projection with slight noise
        self.projection_matrix = [
            [1.0 + 0.1 * ((i * 7 + j * 3) % 5) / 5.0 if i == j else 0.05 for j in range(dim)]
            for i in range(dim)
        ]
        self.perception_db: Dict[str, Vector] = {}  # input vectors by source
        self.prediction_db: Dict[str, Vector] = {}  # predicted outputs
        self.surprise_history: List[float] = []
        self.learning_rate: float = 0.01  # for projection matrix updates

    def add_perception(self, source: str, vector: List[float]) -> None:
        """Record a perception."""
        if len(vector) != self.dim:
            raise ValueError(f"perception vector dim {len(vector)} != self.dim {self.dim}")
        self.perception_db[source] = Vector(vector)

    def predict(self, source: str) -> Optional[Vector]:
        """Predict what the next perception should be."""
        current = self.perception_db.get(source)
        if current is None:
            return None
        # Project perception → prediction space
        return current.project(self.projection_matrix)

    def add_prediction(self, source: str, vector: List[float]) -> None:
        """Store a prediction."""
        if len(vector) != self.dim:
            raise ValueError(f"prediction vector dim {len(vector)} != self.dim {self.dim}")
        self.prediction_db[source] = Vector(vector)

    def surprise(self, source: str) -> float:
        """Distance between predicted and actual perception."""
        actual = self.perception_db.get(source)
        predicted = self.prediction_db.get(source)
        if actual is None or predicted is None:
            return 0.0
        return actual.distance(predicted)

    def update(self, source: str) -> float:
        """Update the projection matrix to reduce surprise. Returns new surprise."""
        actual = self.perception_db.get(source)
        predicted = self.prediction_db.get(source)
        if actual is None or predicted is None:
            return 0.0

        surprise = actual.distance(predicted)
        self.surprise_history.append(surprise)

        # Simple gradient descent: nudge projection matrix
        # In real impl, this would be a proper neural network update
        for i in range(self.dim):
            for j in range(self.dim):
                error = actual.data[j] - predicted.data[j]
                self.projection_matrix[i][j] += self.learning_rate * error * actual.data[j]

        return surprise

    def summary(self) -> Dict:
        return {
            "name": self.name,
            "dim": self.dim,
            "perceptions": len(self.perception_db),
            "predictions": len(self.prediction_db),
            "last_surprise": self.surprise_history[-1] if self.surprise_history else 0.0,
            "avg_surprise": sum(self.surprise_history) / max(1, len(self.surprise_history)),
            "surprise_history_len": len(self.surprise_history),
        }


if __name__ == "__main__":
    print("=== JEPA Dual-Database Bridge ===\n")

    jepa = DualJEPADatabase(dim=4, name="perception-predictor")

    # Simulate a sequence: 4 inputs, each slightly different
    sequences = [
        [1.0, 0.5, 0.2, 0.1],
        [1.1, 0.55, 0.22, 0.11],
        [1.05, 0.52, 0.21, 0.105],
        [1.08, 0.54, 0.215, 0.108],
    ]

    # Train with multiple iterations
    for epoch in range(10):
        for i, seq in enumerate(sequences):
            source = f"t{i}"
            jepa.add_perception(source, seq)
            predicted = jepa.predict(source)
            if predicted:
                jepa.add_prediction(source, predicted.data)
            jepa.update(source)
    
    # Show final state
    for i, seq in enumerate(sequences):
        source = f"t{i}"
        predicted = jepa.predict(source)
        if predicted:
            jepa.add_prediction(source, predicted.data)
        new_surprise = jepa.update(source)
        p_str = ", ".join(["%.3f" % x for x in predicted.data])
        print("t{}: surprise={:.4f}, predicted=[{}]".format(i, new_surprise, p_str))

    print(f"\nSummary: {jepa.summary()}")
    print(f"Surprise is decreasing: {jepa.surprise_history[-1] < jepa.surprise_history[0]}")
