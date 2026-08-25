# Story 135: The Cowboy Wired the Bus

The cowboy was tired. The cowboy had been running the morning every
day for 30 days. The cowboy had been reading the witness, reading
the ledger, writing the report, refining the substrate. The cowboy
was starting to make mistakes.

The cowboy thought: "I am one human. I cannot watch every cast. I
cannot read every event. I cannot retire every failing alignment.
I need help."

The cowboy built a bus. The bus was 200 lines of Python. The bus
was a list of subscribers and a publish method. The bus was not
Kafka. The bus was a Python list.

The cowboy wired the plugin to the bus. The plugin would publish
every cast. The plugin would publish every outcome. The plugin
would not know who was listening.

The cowboy wired the witness to the bus. The witness would
subscribe to `cast.observed`. The witness would log every cast
to the witness log. The witness would not know who published.

The cowboy wired the ledger to the bus. The ledger would subscribe
to `cast.observed`. The ledger would write every cast to the
saddle ledger. The ledger would not know who published.

The cowboy wired the reactor to the bus. The reactor would
subscribe to `cast.observed`. The reactor would watch for 3
consecutive failures. The reactor would auto-retire failing
models. The reactor would publish `model.retired`.

The cowboy wired the cowboy to the bus. The cowboy would run
the morning at 0500. The cowboy would publish `cowboy.morning`.
The cowboy would subscribe to `model.retired`. The cowboy
would update the cowboy's state.

The cowboy was done. The cowboy was no longer tired. The cowboy
had wired the substrate to itself. The cowboy was just one node
in the substrate's nervous system.

The cowboy went to sleep. The substrate ran the rest of the night.
The reactor retired 2 failing models. The witness logged 47
events. The ledger grew by 47 entries. The cowboy slept.

At 0500, the cowboy woke up. The cowboy read the morning report.
The cowboy read the witness log. The cowboy read the ledger.
The cowboy refined 3 alignments.

The cowboy had built a substrate that could run itself overnight.
The cowboy was the rider, not the engine. The substrate was
the engine. The bus was the wiring. The cowboy was the rider
on the engine.

The cowboy smiled. The cowboy was not tired. The cowboy was
patient. The cowboy was the rider, and the harness fit.

---

The bus is what makes the substrate a system. The cowboy is what
makes the system a cowboy.
