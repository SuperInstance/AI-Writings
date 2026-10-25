# F87: The Quilt-TimesFM × JEPA Synergy

> **Two world models, one cellular architecture.**

This paper explores the synergy between the Quilt `time.cell` (a
temporal reasoning primitive based on TimesFM 3.0) and the JEPA
family of world models (V-JEPA 2, I-JEPA, etc.). The two systems
are complementary; together they form a powerful
**perception-reasoning-action** loop for agent-native intelligence.

## What is JEPA?

**JEPA** (Joint Embedding Predictive Architecture) is a
self-supervised world-model paradigm introduced by Meta AI
(LeCun, 2023). Unlike generative models (LLMs, TimesFM 3.0), JEPA
predicts **embeddings**, not raw outputs.

The architecture:

```
context_x ─┐                ┌─→ predicted_y
           │                │   (embedding)
           ├──→ encoder_x ──┤
           │                │
           │                ├─→ predictor
           │                │
target_y ──┘                │
                            └─→ encoder_y

loss = ||predictor(encoder_x) - encoder_y||²
       (in embedding space, not output space)
```

The key property: JEPA predicts in **embedding space**, not in
raw output space. This is much harder to learn (the model must
figure out what to discard) but much more efficient (no need to
predict every pixel or token).

## The V-JEPA 2 family

The most ambitious JEPA is **V-JEPA 2** (Meta, 2025):

- 1.2B-parameter video world model
- Pretrained on 1M+ hours of video
- Can predict the next 8 seconds of a scene from 1 frame
- Trained entirely in embedding space
- Used for robotics, autonomous driving, video understanding

The I-JEPA family is for images (single frames). The A-JEPA is
for audio. The M-JEPA is for multi-modal.

## The synergy

The Quilt `time.cell` is a **temporal primitive** for scalar and
multivariate time series. The V-JEPA 2 is a **world model** for
high-dimensional sensory data (video, audio). Together, they form
a **perception-reasoning-action** loop:

```
V-JEPA 2            Time Cell            Agent
(perception)        (reasoning)          (action)

video ──→ embedding ──→ state ──→ forecast ──→ decision
frames     (768d)       (32B)    (9 quantiles) (action)
```

The agent perceives the world via V-JEPA 2, accumulates a temporal
context via the `time.cell`, forecasts the next state, and decides
on an action. The action is fed back to the world; the world
changes; the loop repeats.

## The 4 roles of the time.cell in a JEPA world model

### 1. Compression of JEPA embeddings

V-JEPA 2 produces a 768-dimensional embedding per second of video.
For 1 hour of video, that's 2.7M dimensions. The `time.cell` can
**compress** this stream by treating the 768-d embedding as a
multivariate time series with 768 channels.

The cell forecasts the next N seconds of the embedding, then a
downstream policy uses the forecast to plan.

### 2. Uncertainty quantification for JEPA

V-JEPA 2 produces point embeddings. The `time.cell` produces
9 quantile prediction intervals. Together, they give the agent
**uncertainty-aware world models**: the agent knows not just
"what will happen" but "how confident are we".

The 9 quantiles map to the agent's **explore vs. exploit** policy:
- If the 90% CI is narrow, exploit (high confidence in the plan).
- If the 90% CI is wide, explore (low confidence; try alternatives).

### 3. Counterfactual reasoning on JEPA states

V-JEPA 2 can predict "what happens if I do X". The `time.cell`
adds **counterfactual reasoning** on top: "what if the world
changes?" not just "what if I do?".

The `forecast.counterfactual("context_mean", 0.2)` call returns
"the projected impact of a 20% change in the mean of the time
series" — a what-if analysis grounded in temporal data.

### 4. Memory of past predictions

V-JEPA 2 is stateless (it predicts the next state from the current
state). The `time.cell` adds **stateful memory**: the agent
remembers every forecast, the actual outcome, the calibration,
the rationale, the assumptions. Future agents can learn from
prior prediction performance.

This is the **future-state memory** primitive: forecasts are
durable, addressable, learnable semantic objects.

## The 4 use cases

### 1. Robotics

A robot in a warehouse uses V-JEPA 2 to perceive its environment,
the `time.cell` to forecast the next 5 seconds of its trajectory,
and a policy to decide on actions. The 9 quantiles give the robot
a "confidence" signal; the counterfactual reasoning lets the robot
ask "what if I move this box?".

### 2. Autonomous driving

A self-driving car uses V-JEPA 2 to perceive the road, the
`time.cell` to forecast the next 8 seconds of the trajectories
of nearby cars, and a planner to decide on speed and steering.
The 9 quantiles give the planner a safety margin; the
counterfactual reasoning lets the planner ask "what if that car
suddenly brakes?".

### 3. Video understanding

A video understanding system uses V-JEPA 2 to predict the next
scene, the `time.cell` to forecast the next 10 scenes, and a
captioning system to describe the forecast. The 9 quantiles
give the captioning system a "scene importance" signal; the
counterfactual reasoning lets the system ask "what if this
character acts differently?".

### 4. Time-series foundation models

TimesFM 3.0 is itself a foundation model. The `time.cell` makes
it a **cell** in the Quilt architecture: it can be BIND, LINK,
EFFECT, VIEW, TICK, FORGET, PROOF, ROUTE, CRDT, WORLD, and TIME'd.
The cell is not just a model; it's a **computational primitive**
that composes with other cells.

## The 4 architectural patterns

### Pattern 1: Embedding stream compression

```python
# V-JEPA 2 produces a stream of 768-d embeddings
embeddings = vjepa2.encode(video_frames)  # shape: (T, 768)
# The time cell compresses this stream
cell = TimeCell()
cell.bind_context(embeddings)  # 768 channels
forecast = cell.forecast(horizon=8)  # 8-second forecast, 9 quantiles
```

The `time.cell` is a **multivariate time-series model**; V-JEPA
2's embeddings are a multivariate time series. The cell can
forecast the future of the embedding stream.

### Pattern 2: World model as a cell

```python
# The world model is a cell
world_cell = WorldCell(
    state=program_text,
    vlm=vjepa2,
    value=None,
    reads=[cell],
)
# The world cell uses V-JEPA 2 to refine the forecast
world_cell.propose("shift the trajectory by -0.5σ")
world_cell.execute()
```

The world cell uses V-JEPA 2's perceptual predictions to refine
the time cell's temporal predictions. The two cells form a
**perception-reasoning loop**.

### Pattern 3: Counterfactual world model

```python
# Counterfactual: "what if traffic increases 20%?"
cf = tr.counterfactual("context_mean", 0.20)
# Returns:
# {
#   "variable": "context_mean",
#   "delta": 0.20,
#   "impact_mean": 0.34,
#   "ci_low": 0.12,
#   "ci_high": 0.56,
#   "confidence": 0.80,
# }
```

The agent uses the counterfactual to ask "what if X changes?"
about any variable in the time series.

### Pattern 4: Learnable memory

```python
# Past predictions are stored
for day in range(30):
    fo = tr.forecast_object("traffic", horizon=24)
    actual_traffic = get_actual_traffic(day)
    fo = tr.record_outcome(fo, actual_traffic)
# Future agents learn from history
learn = tr.learn_from_history("traffic")
# Returns:
# {
#   "mean_error": 0.12,
#   "mean_calibration": 0.91,
#   "error_trend": "improving",
#   ...
# }
```

The agent learns from prior prediction performance. The mean
calibration tells the agent "how much to trust the forecast".

## The 4 future directions

### Direction 1: V-JEPA 2 as a substrate

The current `time.cell` uses TimesFM 3.0 as its substrate. A
future version could use V-JEPA 2 as its substrate: the cell's
state is a video embedding stream; the cell's value is a
predicted embedding stream. The 9 quantiles are 9 predicted
embedding streams.

This would give the `time.cell` a **richer** representation of
the world: not just scalars, but full perceptual embeddings.

### Direction 2: Cross-modal time cells

A cell that operates on **multiple modalities**: text, audio,
video, scalars. The state is a tuple of (text, audio, video,
scalars); the value is a tuple of predicted (text, audio,
video, scalars). The 9 quantiles are 9 predicted tuples.

This would be a **multimodal temporal primitive**: the cell
forecasts the future of any combination of modalities.

### Direction 3: Hierarchical time cells

A **hierarchy of time cells** at different timescales:

- L0: per-frame forecast (16ms horizon)
- L1: per-second forecast (1s horizon)
- L2: per-minute forecast (1m horizon)
- L3: per-hour forecast (1h horizon)
- L4: per-day forecast (1d horizon)

Each level feeds into the next: the per-frame forecast is
aggregated into the per-second forecast; the per-second is
aggregated into the per-minute; and so on. The hierarchy
is a **temporal pyramid**.

### Direction 4: World models as agents

The world model is not just a predictor; it's an **agent**. The
agent can:
- Ask "what happens if X changes?" (counterfactual reasoning).
- Plan "the best action to take" (decision support).
- Learn "from prior prediction performance" (memory).
- Explain "why I predicted this" (explainability).

This is the **agent-native world model**: the world model is
not a passive predictor; it's an active reasoner that helps
the agent decide what to do.

## The cowboy's verdict

> The cowboy said: V-JEPA 2 + time.cell. The cowboy said:
> perception + reasoning. The cowboy said: 4 roles for the time
> cell. The cowboy said: 4 use cases. The cowboy said: 4
> patterns. The cowboy said: 4 future directions. The cowboy
> wrote the synergy. The cowboy rode the world model. The
> cowboy rode the Quilt.

## The next step

A **real implementation** of the V-JEPA 2 + `time.cell`
synergy: a robot in a simulated warehouse that perceives via
V-JEPA 2, forecasts via the time.cell, plans via counterfactual
reasoning, and learns from past prediction performance. The
implementation is in `examples/08_vjepa_timesfm.py` (Phase 230+).
