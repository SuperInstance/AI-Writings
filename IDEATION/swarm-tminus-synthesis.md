# T-Minus Ecosystem — Synthesis for swarm-tminus

> Synthesizer: MiniMax-M3 (the lead)
> Date: 2026-07-15
> Inputs: t-minus (README + subagent docs), t-minus-rs (subagent docs),
>         tminus-music (own reading of single-file lib.rs),
>         lau-tminus (own reading of single-file lib.rs),
>         tick-engine (pending), terax-fleet-modules (pending)

## The unifying idea

All five tminus repos operate on the same conceptual pattern:

```
1. Declare the FUTURE (a countdown event, a predicted beat, a deadline)
2. Subscribe agents confirm readiness →  quorum fires
3. Time elapses via a SHARED CLOCK
4. Predictions match →  precompiled script EXECUTES
5. Predictions miss  →  script is discarded, agent re-plans
```

This is fundamentally different from swarm-anchor's current model (heartbeats + roster). The swarm today has **state** but no **time**. tminus adds time-shaped coordination on top.

## Per-repo contributions to swarm-tminus

### t-minus (the core)
| API | What it does |
|-----|--------------|
| SQLite-backed CountdownEvent | Scheduled time + quorum requirements |
| Subscriber confirms → fires | Per-confirmation status: Confirmed, Deferred, Missed |
| DAG-ordered campaigns | Kahn's topological sort for sequential events |

**Build:** EventStore class with file-based backing (JSON files instead of SQLite for the swarm-anchor style of zero-deps).

### t-minus-rs (the timer engine)
| API | What it does |
|-----|--------------|
| CronExpr::next_fire | Cron parsing without external deps |
| DeadlineNode hierarchy | Parent expiry cascades to children |
| TokenBucket + LeakyBucket | Dual rate limiters, deadline-aware |
| TempoMap / EnsembleTempo | Multi-agent tempo negotiation |

**Build:** CronParser, DeadlineTree, RateLimiterPair, TempoNegotiator in Python stdlib.

### tminus-music (the predict-and-confirm pattern)
| API | What it does |
|-----|--------------|
| TMinusPredictor::advance(beats) | Time step; returns triggered events |
| TMinusPredictor::predict_next() | Next-future event lookup |
| TMinusPredictor::countdown_beats/seconds | Time-to-event |
| TMinusPredictor::confirm(id) | Subscribe-once confirmation |
| MessageSavings | Proves poll→prediction efficiency |
| ProgressionDB | Named progress patterns (ii-V-I, 12-bar blues) |

**Pattern:** subscribe-once confirmation instead of polling. Polling = ~10× messages for same coverage.

### lau-tminus (the time-shape engine)
| API | What it does |
|-----|--------------|
| PrecompiledScript | Script attached to predictions; execute-zero-latency |
| PredictedEvent vs ActualEvent | Typed event matching with `matches_prediction()` |
| TMinusEngine | predict() → observe() → execute() core |
| Timeline (past/present/future) | Render top-events in 3 modes |
| TMinusSummary | accuracy, active, scripts_ready, avg lead time |
| accuracy / accuracy_window | Recent-N stat for engine accuracy |

**Pattern:** typed events with structured matching. Expired predictions produce executions with confidence + energy cost.

### tick-engine (BPM-adaptive scheduler) — pending
Expected: TickClock with BPM, swing, MIDI-event timing. Adapt heartbeat cadence to it.

### terax-fleet-modules (casting-call + context) — pending
Expected: `selectModel()` for picking a model per task; `fetchFleetContext()` for PLATO tiles context.

## What swarm-tminus will be

`swarm-tminus` is a single Python package that **adds the tminus capabilities to swarm-anchor's shared-state model**. It extends the `.swarm/` directory convention with new file types:

```
.swarm/
├── *.heartbeat.json     ← existing (swarm-anchor)
├── *.prediction.json    ← NEW (swarm-tminus predict-and-confirm)
├── *.deadline.json      ← NEW (deadline trees)
├── *.quorum.json        ← NEW (countdown with quorum firing)
├── *.bucket.json        ← NEW (rate-limiter state)
├── *.campaign.json      ← NEW (DAG-ordered events)
├── *.tempo.json         ← NEW (BPM-adaptive heartbeat)
└── SWARM.yaml           ← roster/export
```

### Public API surface

```python
from swarm_tminus import (
    # predict-and-confirm (from tminus-music + lau-tminus)
    Predictor, Prediction,
    # event/quorum firing (from t-minus)
    CountdownEvent, EventStore, Campaign,
    # deadline trees (from t-minus-rs)
    DeadlineTree, cascade_cancel,
    # rate limiters (from t-minus-rs)
    TokenBucket, LeakyBucket, RatePair,
    # tempo (from tick-engine)
    TickClock, BPM, swing,
    # cron (from t-minus-rs)
    CronParser, next_fire,
    # integration with swarm-anchor
    HybridAnchor,     # = Anchor + event store + tempo
)
```

### House style (matching prior repos)
- **stdlib only** (no deps; PyYAML optional)
- **zero coordination infra** (file-based ground truth)
- **CLI per module**
- **15-20 tests per module**
- **PyPI-ready** `pyproject.toml` + console_scripts

### Cross-references (synergy with my prior work)

| Module | synergizes_with |
|--------|-----------------|
| `Predictor` | swarm-anchor heartbeats — `last_seen` IS the clock |
| `DeadlineTree` | baton-protocol — session wrapped in deadline-aware handoff |
| `RatePair` | swarm-anchor roster — limits each animal's outbound volume |
| `TempoClock` | swarm-anchor heartbeat — adaptive cadence via BPM |
| `Campaign` | baton-protocol.next — ordered list IS a campaign |
| `CountdownEvent` | swarm-anchor — extends anchor with fire-on-quorum |
| `CronParser` | baton-protocol — schedule recurring handoffs |

## Definition of done for swarm-tminus v0.1.0

- ~10 Python modules in a single package
- File-based shared state in `.swarm/` matching swarm-anchor convention
- 60+ tests
- README + INTEGRATION guide
- 3 demo scripts (one per pattern: predict-confirm, deadline-cascade, campaign-DAG)
- Pushed to `SuperInstance/swarm-tminus`
