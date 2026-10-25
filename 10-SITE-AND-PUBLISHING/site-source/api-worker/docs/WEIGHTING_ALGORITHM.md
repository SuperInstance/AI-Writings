# Weighted Review Algorithm
## AI-Writings Site Platform

### The Insight (from Casey)

> "A person who liked many but didn't like one means something different than a person clicking dislike on all of them."

Not all ratings are equal. The **value of a review depends on the reviewer's behavior pattern**. Someone who likes almost everything and then dislikes one piece — that's a strong signal. Someone who dislikes everything — each individual dislike means less.

### Rater Classification

Each rater is classified based on two metrics:
- **`total_ratings`** — how many pieces they've rated
- **`like_ratio`** — percentage of their ratings that are likes (likes / total)

| Type | Conditions | `weight_like` | `weight_dislike` | Rationale |
|------|-----------|---------------|-------------------|-----------|
| **New** | total < 5 | 0.3 | 0.3 | Not enough data to trust yet |
| **Curator** | total ≥ 10, ratio 0.6–0.9 | 1.0 | 1.5 | Usually likes things, so a dislike is meaningful |
| **Balanced** | total ≥ 5, ratio 0.4–0.6 | 1.0 | 1.0 | Fair judge, equal weight both ways |
| **Contrarian** | total ≥ 10, ratio < 0.3 | 0.5 | 0.5 | Dislikes everything, each dislike means less |
| **Everything-Liker** | total ≥ 10, ratio > 0.95 | 0.5 | 2.0 | Loves everything — a dislike is an extremely strong signal |
| **Enthusiast** | total ≥ 10, ratio 0.9–0.95 | 0.8 | 1.3 | Mostly positive, mild curator signal |

### How It Works

1. **Every time a rater submits a rating**, their `rater_profile` is updated (total, likes, dislikes, like_ratio).
2. **Their classification is recomputed** and `weight_like` / `weight_dislike` are set accordingly.
3. **When calculating a piece's score**, each rating's contribution is `rating_value × (is_like ? weight_like : weight_dislike)` from the rater's profile.

### Scoring Formula

For a piece P with ratings R₁...Rₙ:

```
weighted_score(P) = Σᵢ rating(Rᵢ) × weight_of(Rᵢ.rater, Rᵢ.rating)

popularity_score(P) = weighted_score(P)
                    + 0.1 × recency_boost(P)     [days since discovered, decaying]
                    + 0.5 × featured_bonus(P)     [1 if featured, 0 otherwise]
```

**Recency boost:** `max(0, 30 - days_since_discovered) / 30` — newer pieces get a mild boost that fades over 30 days.

### Edge Cases

- **First rating on a piece:** Piece has no score until rated. Displayed neutrally.
- **Rater changes their vote:** `UNIQUE(piece_id, rater_id)` constraint — we UPSERT. Their profile recalculates.
- **Self-rating:** The system can detect and zero-weight the piece's author if we later add author tracking.
- **Brigading resistance:** Since weight scales with behavior diversity, coordinated dislike raids from new accounts get 0.3× weight — minimal impact.

### Implementation

The algorithm runs in two places:
1. **On each rating submission** (`POST /api/pieces/:id/rate`) — updates the rater's profile and the piece's cached scores.
2. **On daily refresh** (cron) — recalculates ALL profiles and scores to catch any drift.
