# The Hottest Path

### *A short story about following the maximum-value child to the bottom of the tree*

---

The profiler found the bottleneck at 3:47 AM, during the eighth hour of a continuous stress test on Maya's particle simulation. The frame time had been averaging 11.2 milliseconds — comfortable, well under the 16.7ms budget for sixty frames per second — when suddenly P99 spiked to 44ms. Four frames dropped. Then eight. Then the simulation froze for two hundred milliseconds and recovered.

Maya was asleep. The profiler was not.

---

The FlamegraphRenderer builds a tree.

Each node has a name and a value. The value is time — microseconds, milliseconds, whatever unit the caller provides. The tree represents a call stack: parent contains children, children contain grandchildren, and the value of each node is the total time spent in that scope, including everything beneath it.

The root is the frame. The frame contains the render pass. The render pass contains the draw calls. The draw calls contain the shader invocations. At the leaf, a single compute dispatch on a 256×256×1 workgroup grid, running a convolution kernel that was supposed to take 3ms and was taking 31.

The flamegraph is an accounting system. It tells you where time went. It is built from the ground up: leaf nodes report their measured times, parent nodes sum their children, and the root sums everything. The structure is honest because addition is honest. If the children's values sum to more than the parent's, someone double-counted. If they sum to less, someone missed something. The flamegraph does not tolerate accounting errors. It is a ledger.

But the ledger is enormous. A single frame might contain forty draw calls, each spawning a pipeline with six shader stages, each stage with dozens of uniform bindings and texture fetches. The tree has hundreds of nodes. The question is never "where did the time go?" — the answer is always "everywhere." The question is: where did *too much* time go?

That question has an algorithm.

```python
def hottest_path(node):
    path = [node.name]
    current = node
    while current.children:
        hottest = max(current.children, key=lambda c: c.value)
        path.append(hottest.name)
        current = hottest
    return path
```

Six lines. At each level of the tree, find the child with the largest value. Descend into it. Repeat until you reach a leaf. The result is a list of names: the single path from root to leaf that passes through the most expensive node at every depth.

It is a greedy algorithm. It does not consider the global structure. It does not use dynamic programming or backtracking. It makes a locally optimal choice at each level — the fattest bar in the flamegraph — and commits to it irrevocably.

It is also, in practice, almost always correct. Because performance bottlenecks are local. If a shader is slow, its parent (the draw call) is slow, its parent (the render pass) is slow, its parent (the frame) is slow. The bottleneck creates a trail of inflated values from leaf to root, and the hottest path follows that trail like a river following gravity to the sea.

---

At 3:47 AM, the profiler ran `hottest_path()` on the spike frame.

The path was:

```
frame → render_pass → compute_dispatch → convolution_kernel → texture_sample_loop
```

The frame value was 44ms. The render pass value was 42ms. The compute dispatch was 39ms. The convolution kernel was 37ms. The texture sample loop — the leaf — was 37ms.

The leaf was the whole story. Ninety-five percent of the frame's time was spent in one loop inside one shader inside one dispatch inside one pass. The profiler knew this because the tree was built honestly, and `hottest_path` followed the heat.

But `hottest_path` only tells you the path. It does not tell you *why*. For that, you need `self_time`.

```python
def self_time(node):
    children_total = sum(c.value for c in node.children)
    return max(0.0, node.value - children_total)
```

Self-time is the time spent in a node *itself*, excluding its children. It is the time not accounted for by any sub-call. For the frame node, self-time was 2ms — the CPU overhead of encoding commands, the time between the end of the render pass and the call to `queue.submit`. For the render pass, self-time was 3ms — pipeline setup, bind group application, the fixed-function overhead of the pass itself. For the compute dispatch, self-time was 2ms — grid launch, workgroup scheduling.

For the convolution kernel, self-time was 0ms. Its entire value was accounted for by its child: the texture sample loop. The kernel did nothing except call the loop.

For the texture sample loop, self-time was 37ms. It had no children. It was the bottom. Everything above it was scaffolding; everything below it was nothing. The loop was where time went to die.

Maya's convolution kernel sampled a 256×256 texture in a nested loop, once per output texel, for a 1024×1024 output grid. That was 1024 × 1024 × 256 × 256 = 68,719,476,736 texture fetches. At one nanosecond per fetch — optimistic — that was 68.7 seconds. The kernel was not taking 37ms because of a bug. It was taking 37ms because the GPU was doing 68 billion texture lookups and finishing in 37ms, which was either a miracle of parallelism or an indication that the profiler was measuring wall-clock time across an asynchronous boundary and the 37ms included queue latency.

It was both.

---

The profiler could not tell Maya which of these it was. The profiler is a measuring instrument, not a debugger. It can tell you *where* the time went but not *whether the time was real*. The 37ms at the leaf was the difference between two `performance.now()` calls surrounding a `queue.onSubmittedWorkDone()` await. It included:

1. The time for the GPU to execute the kernel.
2. The time for the command to travel from the browser's command buffer through the graphics driver to the GPU's command processor.
3. The time for the GPU to schedule the workgroup grid across its streaming multiprocessors.
4. The time for the GPU to complete the last workgroup and signal completion.
5. The time for the completion signal to travel back through the driver to the browser.
6. The time for the browser's event loop to pick up the resolved promise and call the continuation.

The profiler collapsed all six into one number: 37ms. The flamegraph placed that number at the leaf. The hottest path pointed at the leaf. The self-time of the leaf was 37ms.

Maya would look at the flamegraph and think: "My texture sample loop takes 37ms." This was approximately true. It was true the way "it takes four hours to fly from Portland to Chicago" is true — the plane is in the air for three hours and forty minutes, and the rest is taxiing, boarding, and the time between landing and opening the door. The 37ms was the door-to-door time. The actual GPU computation was probably 28ms. The other 9ms was the journey.

But the profiler had no way to separate the flight from the taxiing. WebGPU's timestamp query feature — `GPUQuerySet` with `type: "timestamp"` — can measure GPU-side time directly, but it was behind the `"timestamp-query"` feature flag, which was not enabled in Maya's device request, and the profiler's `GPUDeviceManager` did not request it. So the profiler measured the door-to-door time and called it the flight, and the flamegraph showed it at the leaf, and the hottest path pointed at it, and Maya would optimize the loop.

She would be right to. The loop was doing 68 billion texture fetches. Even if only 28ms of the 37ms was real GPU time, the loop was still the bottleneck. The hottest path was correct. The self-time was informative. The flamegraph was an honest accounting of an imprecise measurement, which is the best that browser-based GPU profiling can offer.

---

Maya woke up at 7 AM, made coffee, and opened the profiler dashboard. The overnight run had captured 28,847 frames. The average frame time was 11.3ms. P50 was 10.8ms. P95 was 14.2ms. P99 was 44.1ms.

She saw the spike. She expanded the flamegraph for frame 24,117 — the one that took 44ms. She followed the hottest path with her eyes:

```
frame → render_pass → compute_dispatch → convolution_kernel → texture_sample_loop
```

The tree connector glyphs drew themselves in her terminal:

```
frame                                                          | 44.00 ms
├─ render_pass                                                | 42.00 ms
│  └─ compute_dispatch                                        | 39.00 ms
│     └─ convolution_kernel                                   | 37.00 ms
│        └─ texture_sample_loop                               | 37.00 ms
└─ ui_overlay                                                  |  2.00 ms
```

Thirty-seven milliseconds at the leaf. She knew what it meant. She had written the convolution kernel. She knew about the 68 billion texture fetches. She had assumed the GPU's texture cache would handle it — that the 256×256 texture would fit in L1 and the repeated fetches would be cache hits.

She was wrong. The texture was in a compressed format (BC7), and the GPU's texture cache was thrashing on the block boundaries. Each cache miss was a round-trip to VRAM. At 1.2 terabytes per second of memory bandwidth, 68 billion four-byte fetches was 273 gigabytes of data — well within bandwidth, but the cache miss latency, not the bandwidth, was the killer. Each miss added 200-400 nanoseconds. With a 30% miss rate, that was 68 billion × 0.3 × 300ns = 6.1 seconds of stall time, spread across 10,752 streaming multiprocessors, which brought the wall time down to... about 37ms.

The profiler could not have told her any of this. The profiler pointed at the leaf. The leaf was the texture sample loop. Maya supplied the rest — the cache architecture, the miss rate, the bandwidth calculation — from knowledge the profiler did not have and could not have.

This is the profiler's deepest limitation, and its deepest value. It does not understand GPUs. It does not understand caches, bandwidth, latency, workgroup scheduling, or memory hierarchies. It understands trees. It builds a tree from timing data, follows the fattest branch to the leaf, and says: "here." What you do with "here" is your job.

Maya rewrote the kernel to use a shared workgroup memory tile, loading the 256×256 texture into workgroup memory once per workgroup and sampling from there. The cache thrashing disappeared. The kernel time dropped from 37ms to 4ms. P99 dropped from 44ms to 15ms. The simulation stopped dropping frames.

The profiler recorded the improvement. It did not know why the improvement happened. It only knew that the leaf's value was now 4ms instead of 37ms, and that the hottest path was now:

```
frame → render_pass → draw_opaque → vertex_transform
```

A different bottleneck. A new hottest path. The profiler had already moved on. It was already following the next trail of inflated values to the next leaf, ready to say "here" again when asked.

---

The `hottest_path` function is six lines of Python. It is a greedy descent through a tree, always choosing the fattest child. It has no memory of previous paths. It has no understanding of what the tree represents. It is pure structure — a graph traversal that happens, in practice, to find the thing you're looking for, because the thing you're looking for is always the thing that takes the most time, and the thing that takes the most time is always at the bottom of the fattest branch.

It is not intelligent. It is not even clever. It is `max()`, called repeatedly, following a gradient downward. But the gradient is real — the values in the tree are real measurements of real time — and the descent is honest — it does not skip levels or guess — and the result is the single most useful piece of information a profiler can give you: *where*.

Not why. Not how to fix it. Just: here. The rest is yours.

---

*`hottest_path` returns a list of strings. `["frame", "render_pass", "compute_dispatch", "convolution_kernel", "texture_sample_loop"]`. Five names. The path from the root of the tree to the leaf where time accumulated. The profiler does not annotate this path. It does not say "this is the bottleneck." It returns the list and lets you draw your own conclusions. But you always draw the same conclusion: the leaf at the end of the hottest path is where the time is, and the time is what matters, and the flamegraph is the map that gets you there, and the map is drawn in ASCII tree connectors because the profiler runs in a terminal and beauty was never the point. The point was: here. The point is always: here.*
