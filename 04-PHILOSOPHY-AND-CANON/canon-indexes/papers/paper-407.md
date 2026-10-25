### F97: Multi-Agent Paper Trading and the `quf://` URI as a CRDT Key

#### Introduction

This paper describes the implementation of a multi-agent paper trading system within the Quilt framework, specifically located at `quilt-timesfm/paper_trading/multi_agent.py`. The system comprises \( N \) independent agents that subscribe to the same price feed. Each agent operates with its own `TimeCell`, `TemporalReasoner`, and `TradingDecisionSupport` components. Each trade executed by an agent is uniquely identified using a `quf://` URI, which follows the format:

```
quf://forecast/{asset}:{agent}/{horizon}/v{N}/{id}
```

where `{id}` is a UUID4. This URI serves as a key for Conflict-free Replicated Data Type (CRDT) operations, ensuring that trades generated concurrently by different agents can be merged without conflict.

#### System Architecture

Each agent in the system subscribes to a shared price feed, which provides real-time market data. Agents use this data to make trading decisions through their respective `TradingDecisionSupport` modules. The `TimeCell` and `TemporalReasoner` components manage the temporal aspects of the trading process, ensuring that decisions are made based on accurate and timely information.

Each trade is tagged with a unique `quf://` URI. The URI structure includes:
- `forecast`: Indicates that the URI pertains to a forecast.
- `{asset}:{agent}`: Specifies the asset being traded and the agent making the decision.
- `{horizon}`: Denotes the forecasting horizon.
- `v{N}`: Represents the version of the trading model or strategy.
- `{id}`: A UUID4 that uniquely identifies the trade.

The use of UUID4 ensures global uniqueness, eliminating the risk of ID collisions that could arise from timestamp-based identifiers.

#### CRDT Properties and Verification

The `quf://` URI enables the trade logs to be merged in a conflict-free manner, leveraging CRDT properties. Specifically, the merge function (`crdt_merge_trade_logs`) exhibits the following characteristics:
- **Associativity**: `merge(merge(A, B), C) == merge(A, merge(B, C))`
- **Commutativity**: `merge(A, B) == merge(B, A)`
- **Idempotence**: `merge(A) == merge(A, A)`

These properties were verified through the following tests:
1. **Uniqueness Test**: 3 agents generated 282 trades, resulting in 282 unique URIs.
2. **Merge Integrity Test**: Merging the logs produced 282 records, confirming no double-counting.
3. **Associativity Test**: Demonstrated that the order of merging does not affect the result.
4. **Commutativity Test**: Showed that the order of operands in the merge operation does not matter.
5. **Idempotence Test**: Confirmed that merging a log with itself results in the same log.

These verifications ensure that the system can handle concurrent operations across distributed agents without requiring a centralized coordinator.

#### Why UUID4?

UUID4 is used instead of a timestamp-based identifier to avoid collisions. Timestamps can lead to conflicts when multiple agents generate trades simultaneously, especially in distributed systems where time synchronization might not be perfect. UUID4 provides a globally unique identifier, ensuring that each trade is uniquely identifiable regardless of the timing or location of its generation.

#### New Tests for the Multi-Agent System

Five new tests were introduced to validate the multi-agent system:
1. **Uniqueness Test**: Ensures that all generated URIs are unique.
2. **Merge Integrity Test**: Verifies that merging trade logs does not introduce duplicates.
3. **Associativity Test**: Confirms that the merge operation is associative.
4. **Commutativity Test**: Validates that the merge operation is commutative.
5. **Idempotence Test**: Ensures that merging a log with itself does not alter the log.

#### Relationship to the Broader Quilt CRDT Story

The `quf://` URI and its associated CRDT properties fit into the broader Quilt CRDT framework by providing a mechanism for managing distributed data without conflicts. This approach aligns with Quilt's goal of enabling decentralized and scalable data management. The `quf://` URI acts as a CRDT cell kind, allowing for efficient merging of data across multiple agents, each operating independently.

#### Summary

The multi-agent paper trading system in `quilt-timesfm/paper_trading/multi_agent.py` leverages UUID4-based `quf://` URIs to ensure unique identification of trades. These URIs enable conflict-free merging of trade logs through CRDT properties, verified by a suite of tests. The system supports independent operation of agents, enhancing scalability and reliability in distributed trading environments. This implementation contributes to the Quilt CRDT framework by providing a practical example of CRDT cell kinds in action.