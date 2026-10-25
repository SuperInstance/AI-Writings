# F85: The Quilt Time-Cell's 9 Quantile Bands

> **9 quantiles, 9 bands, 9 levels of uncertainty.**

The Quilt `time.cell` produces a forecast with **9 quantile
prediction intervals**: q ∈ {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,
0.8, 0.9}. These 9 quantiles form 9 bands of uncertainty, and
they're one of the most powerful features of the time-series
foundation model approach.

This paper documents the 9 bands and what each one is good for.

## The 9 bands

| Quantile | Band | Probability actual ≤ upper bound | Use case |
|---|---|---|---|
| q=0.1 | 10% | 10% | "best case 10% of the time" |
| q=0.2 | 20% | 20% | "best case 20% of the time" |
| q=0.3 | 30% | 30% | optimistic |
| q=0.4 | 40% | 40% | below median |
| q=0.5 | 50% | 50% (median) | "the most likely" |
| q=0.6 | 60% | 60% | above median |
| q=0.7 | 70% | 70% | pessimistic |
| q=0.8 | 80% | 80% | "worst case 20% of the time" |
| q=0.9 | 90% | 90% | "worst case 10% of the time" |

The q=0.5 is the **median** (the most likely value). The q=0.9 is
the 90% upper bound (10% of the time, the actual is higher). The
q=0.1 is the 10% lower bound (10% of the time, the actual is
lower).

## The 5 levels of decision-making

Each quantile band corresponds to a different decision-making
posture:

| Posture | Bands | Use case |
|---|---|---|
| **Aggressive** | q=0.5, 0.6, 0.7 | "the forecast is probably right" — bet on the median |
| **Moderate** | q=0.4, 0.5, 0.6, 0.7 | "the forecast is likely right" — consider the 40-70% range |
| **Conservative** | q=0.3, 0.4, 0.5, 0.6, 0.7 | "the forecast might be off" — plan for the 30-70% range |
| **Risk-averse** | q=0.1, 0.2, 0.5, 0.8, 0.9 | "I want to be safe" — focus on the 10% / 90% tails |
| **Catastrophic** | q=0.05, 0.1, 0.9, 0.95 | "what's the worst case?" — plan for the 5% tails |

The Quilt cell's 9 quantiles cover all 5 postures. The user picks
the posture; the cell returns the relevant bands.

## The 4 use cases for the bands

1. **Anomaly detection**: any actual value outside the q=0.1..0.9
   band is a 1-in-10 anomaly. Outside q=0.05..0.95 is a 1-in-20
   anomaly. Outside q=0.01..0.99 is a 1-in-100 anomaly.

2. **Risk management**: a portfolio manager uses the q=0.95 band as
   the Value-at-Risk (VaR) at 95% confidence. The q=0.99 band is
   the 99% VaR.

3. **Capacity planning**: an operations manager plans capacity at
   the q=0.9 band. The forecast says "we'll need X units" but the
   q=0.9 says "we might need 1.3*X units". Plan for 1.3*X.

4. **Hypothesis testing**: a scientist tests the hypothesis "the
   actual will fall within the q=0.1..0.9 band". If the actual
   falls outside, the hypothesis is rejected (the forecast is
   wrong).

## The 4-band plot

The classic visualization is a 4-band plot:

```
   ┌─────────────────┐ ← q=0.9 (90% upper)
   │  ░░░░░░░░░░░░░  │
   │  ▒▒▒▒▒▒▒▒▒▒▒▒  │ ← q=0.7 (70% upper)
   │  ▓▓▓▓▓▓▓▓▓▓▓▓  │
   │  ██████████████  │ ← q=0.5 (median)
   │  ▓▓▓▓▓▓▓▓▓▓▓▓  │
   │  ▒▒▒▒▒▒▒▒▒▒▒▒  │ ← q=0.3 (30% lower)
   │  ░░░░░░░░░░░░░  │
   └─────────────────┘ ← q=0.1 (10% lower)
```

The darker the band, the more probable the actual is in that range.
The q=0.5 is the "expected" forecast. The q=0.1..0.9 envelope is
the "likely" range. The q=0.05..0.95 is the "almost certain" range.

## The 4-band trading strategy

In trading, the 4 bands correspond to 4 positions:

| Band | Position |
|---|---|
| q=0.5 | "fair value" — neutral position |
| q=0.1..0.5 | "long" — buy if actual < q=0.1 (undervalued) |
| q=0.5..0.9 | "short" — sell if actual > q=0.9 (overvalued) |
| q=0.05..0.95 | "stop-loss" — exit if actual < q=0.05 or > q=0.95 |

The Quilt cell's 9 quantiles give the trader 4 levels of trading
decisions, each with a clear entry and exit point.

## The 5-band decision tree

For decision-making, the 5-band decision tree is:

```
                  Actual
                    │
        ┌───────────┼───────────┐
        │           │           │
      < q=0.1    q=0.1..0.9   > q=0.9
        │           │           │
    "much       "as          "much
     lower"    expected"     higher"
        │           │           │
   take        take         take
   bearish     neutral      bullish
   action      action       action
```

The q=0.1 and q=0.9 are the **decision thresholds**. If the actual
falls below q=0.1, the situation is "much worse than expected" and
a bearish action is warranted. If above q=0.9, the situation is
"much better than expected" and a bullish action is warranted.

## The 9 quantiles in the polyformalism

The 9 quantiles are part of the polyformalism. The forecast shape
is `[9, horizon * n_variates]` in C, Python, and Rust. The same
shape, the same indices, the same bit-exact quantiles.

```python
# Python
for q in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    quantile = cell.read_quantile(q, 0)
    assert len(quantile) == horizon
```

```rust
// Rust
for q in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] {
    let quantile = cell.read_quantile(q, 0);
    assert_eq!(quantile.len(), horizon);
}
```

The 9 quantiles are the same in both languages. The cell is the
system.

## The cowboy's verdict

> The cowboy said: 9 quantiles, 9 bands. The cowboy said: 5 levels
> of decision-making. The cowboy said: 4 use cases. The cowboy
> said: anomaly detection, risk management, capacity planning,
> hypothesis testing. The cowboy wrote the 4-band plot. The cowboy
> wrote the 4-band trading strategy. The cowboy wrote the 5-band
> decision tree. The cowboy rode the 9 quantiles. The cowboy rode
> the Quilt.

## The next step

A **band-aware backtester**: a backtesting engine that uses the 9
quantiles to evaluate a trading strategy. The engine compares the
strategy's P&L to the quantile bands, showing the strategy's edge
relative to the forecast uncertainty. If the strategy's P&L is
within the q=0.1..0.9 band, the strategy is "no better than
random". If outside, the strategy has a real edge.
