# Paper 132: The In-Process Bus and the Composition of the Quilt

## Abstract

The Quilt ecosystem is composed of many small pieces: substrate,
plugin, witness, ledger, cowboy, reactor. Each piece has one job.
The bus is what lets the pieces cooperate. This paper describes
the bus's design — pub/sub with topic patterns, append-only history,
and JSONL persistence — and shows how the bus enables composition
without coupling.

## 1. The composition problem

A Quilt substrate has many components. The plugin proposes casts.
The witness records outcomes. The ledger persists them. The cowboy
refines them. The reactor reacts in real time.

The naive way to wire these: each component holds a reference to
every other component. The plugin holds a reference to the witness,
the ledger, the cowboy, the reactor. The cowboy holds a reference
to the plugin, the witness, the ledger. The witness holds a
reference to the plugin, the cowboy, the ledger. The result is a
tightly coupled mesh of references, where every change to one
component ripples through every other.

The Quilt's solution: a bus. The bus is a single shared object.
Components publish events to the bus. Components subscribe to
topics on the bus. The bus delivers events. Components don't know
about each other.

## 2. The bus's design

The bus is a `dict[str, list[Subscriber]]` and a list of past
events. The API is minimal:

```python
bus = EventBus()
bus.subscribe("cast.observed", my_handler)
bus.subscribe_pattern("cast.*", my_pattern_handler)
bus.publish("cast.observed", source="plugin", data={"model": "PHI-4"})
```

The bus supports two subscription modes:
- **Exact topic**: subscribe to one specific topic
- **Pattern topic**: subscribe to a glob-like pattern (e.g. `cast.*`)

The bus is in-process only. The bus is not Kafka, not Redis, not
RabbitMQ. The bus is a Python list. The cowboy runs locally on the
F/V EILEEN. The bus is the right scale.

The bus is append-only. Every event is recorded in `bus.history_list`.
The bus trims the history to a configurable max length (default
10,000). The bus can be saved to JSONL and reloaded.

## 3. The bus's topics

The Quilt's bus uses dot-namespaced topics. Each topic is
`<domain>.<verb>`. Examples:

- `cast.proposed` — the plugin proposed a casting
- `cast.observed` — the outcome was observed
- `witness.appended` — the witness stored an event
- `ledger.appended` — the saddle ledger grew
- `cowboy.morning` — the cowboy ran the morning
- `model.retired` — a model was retired
- `model.promoted` — a model was promoted
- `substrate.cell_added` — a cell was added to the substrate

The topics are conventions. The bus does not enforce them. The
bus is just a list of subscribers and a publish method. The
conventions are documented in `bus.py`.

## 4. The cowboy as a subscriber

The cowboy's reactor subscribes to the bus. The reactor watches
`cast.observed`. When 3 consecutive failures arrive for a model,
the reactor auto-retires it. The reactor publishes `model.retired`.

The cowboy's morning is a publisher. The cowboy publishes
`cowboy.morning` with the morning report as data. Other components
can subscribe to `cowboy.morning` and react.

The cowboy is a subscriber too. The cowboy subscribes to
`model.retired` and `model.promoted` to track the cowboy's own
state.

The cowboy and the bus are coupled by topic, not by reference. The
cowboy could be replaced with a different reflection loop. The
bus would not change. The cowboy's subscribers could be replaced
with a different set of handlers. The cowboy would not change.

## 5. The composition without coupling

The bus enables composition without coupling. The plugin doesn't
know the cowboy exists. The cowboy doesn't know the plugin exists.
The bus is the only thing they share.

If the cowboy is removed, the plugin still works. The plugin still
proposes casts. The plugin still observes outcomes. The plugin
still updates Wilson profiles. The cowboy's absence is invisible
to the plugin.

If the plugin is removed, the cowboy still works. The cowboy still
runs the morning. The cowboy still reads the witness. The cowboy
still writes the report. The plugin's absence is invisible to the
cowboy.

This is the value of the bus. The bus is what makes the Quilt
a composition. The bus is what makes the Quilt replaceable. The
bus is what makes the Quilt a system, not a monolith.

## 6. The cowboy's reactor as a subscriber

The reactor is a small wrapper around the bus. The reactor
subscribes to `cast.observed`. The reactor's handler updates a
sliding window per model. The reactor's handler checks for 3
consecutive failures. The reactor's handler auto-retires.

The reactor is 200 lines. The reactor's only dependency is the
bus. The reactor could be replaced with a different reaction
strategy. The bus would not change.

The reactor is the cowboy's hands. The bus is the cowboy's
nervous system. The cowboy is the cowboy's head.

## 7. Conclusion

The bus is a small piece. The bus is 200 lines. The bus is not
Kafka, not Redis, not RabbitMQ. The bus is a Python list.

The bus is what lets the Quilt be a composition. The bus is what
lets the Quilt be replaceable. The bus is what lets the Quilt
be a system, not a monolith.

The bus is the substrate's nervous system. The cowboy is the
substrate's head. The reactor is the substrate's hands. The
witness is the substrate's memory. The ledger is the substrate's
truth.

Each piece has one job. The bus is what makes the pieces a
system.

## Source

*Hand-written, 2026-08-25*
*Inspired by the bus.py and cowboy_reactor.py modules*
*Companion to Fable 58 (The Reactor and the Morning)*
