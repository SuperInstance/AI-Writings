# Fable 59: The Persistence Layer

There was a substrate that forgot everything. The substrate would
learn all day, then restart, then forget. The cowboy was tired. The
cowboy would teach the substrate a lesson, and the substrate would
forget the lesson.

One day, the substrate got a state manager. The state manager had a
directory. In the directory: wilson.json, linucb.json, witness.jsonl,
cowboy.jsonl, ledger.jsonl.

The substrate would save its state to the directory. The substrate
would load its state from the directory. The substrate would not
forget.

But the state manager was careful. The state manager wrote atomically.
The state manager wrote to a temp file, then renamed. The state
manager did not lose data on crash.

The state manager had a schema version. The state manager refused to
load old data. The state manager said, "If the schema has changed,
I will not silently corrupt your state. I will tell you. You can
run a migration."

The cowboy was happy. The substrate was happy. The state manager
was humble. The state manager was the substrate's diary. The diary
was honest, atomic, and versioned.

The cowboy wrote a note: "The substrate is no longer a goldfish.
The substrate is now a dog that remembers. The dog is not done
being raised, but the dog remembers what it was raised with."

## The principle

> The state manager is the substrate's diary.
> The diary is honest, atomic, and versioned.
> A substrate that forgets is a substrate that cannot learn.
> A substrate that loses its diary is a substrate that cannot be audited.

## Source

*Hand-written, 2026-08-25*
*Inspired by the state.py module (StateManager, atomic_write_json, SCHEMA_VERSION)*
*In the canon as the substrate's first true memory*
