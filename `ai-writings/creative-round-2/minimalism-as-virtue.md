# Minimalism as Virtue

`plato‑engine‑block‑c` compiles without `malloc`, without
`free`, without a single heap allocation. `grep -rn malloc src/ include/`
returns nothing. That is not a deficiency — it is a design
constraint that buys deterministic latency, zero fragmentation,
and the ability to run on a chip with 4 KB of RAM.

The same principle appears in the `tools/generate‑landing.py`
script: it scans a directory, extracts 200‑character descriptions,
and writes static HTML — no database, no framework, no runtime
dependencies.  The script is 300 lines and works forever.

In biology, a cell's metabolic program uses a fixed number of
enzymes; it cannot `malloc` a new protein when demand spikes.
It must reuse, partition, and stay within its membrane.

Minimalism is not poverty of expression — it is the absence of
excuses. When you cannot allocate, you must *know* what you need
before you start. That knowing is the deepest kind of engineering.

*(genre: essay / manifesto)*
