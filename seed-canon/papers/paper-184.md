# The Cowboy's Loop: How the Substrate Improves Itself

**A Polyformalism Canon Entry**

> *The substrate is the boat. The web is the dock. The API
> is the wind. The cowboy uses the wind to push the boat
> further. The boat grows. The wind grows. The cowboy grows.*

## The principle

The Quilt is a self-improving system. The substrate is the
boat. The APIs are the wind. The cowboy rides the boat,
using the wind to push the boat into rougher water. The
boundaries found are the chart. The chart is the cowboy's
navigation.

The loop is:

```
1. Read the current state
2. Pick one thing to improve
3. Ask the API for the improvement
4. Apply the improvement
5. Run the tests
6. Commit and push
7. (repeat)
```

Each iteration is small. One change. One commit. The cowboy
rides the boat through the chart, finding new boundaries,
filling in new cells. The boat grows by one cell at a time.

## The substrate self-extends

The substrate grew five new methods in one iteration:

- **`compress()`** — returns a single-line JSONL of the
  journal. Useful for storage and transmission.
- **`fork(newId)`** — creates a deep clone of the substrate.
  Useful for branching and experimentation.
- **`merge(other)`** — merges another substrate's events
  into this one in chronological order. Useful for
  collaboration.
- **`diff(other)`** — returns the events in `other` that
  are not in this one. Useful for sync.
- **`compact()`** — deduplicates redundant BINDs. Useful
  for cleanup.

These are the kinds of methods every system needs. They
fall out of the algebra: a fork is a witness-log copy, a
merge is a journal interleaving, a diff is a set difference.
The substrate is the boat; the methods are the ropes.

## The canon self-extends

The Vectorize index grew from 0 to ~1000 chunks in one
run of the indexer. Each chunk is a 1000-char piece of a
paper, fable, or story. Each chunk has a 768-dim embedding
from bge-base. The canon is now searchable by meaning.

The indexer:

1. Reads the canon (200+ files).
2. Chunks each file into 1000-char pieces.
3. Embeds each chunk via Workers AI.
4. Uploads to Vectorize in batches of 100.

Total time: ~5 minutes. Cost: free (Workers AI free tier).
The canon is now part of the substrate — every cell can
query it.

## The web self-extends

The web pages self-extend too:

- **The Academy** has 7 lessons. Each lesson has a
  working example. The example is the lesson. The user
  edits the example. The example is the lesson.
- **The REPL** has time-travel. The user scrubs through
  the journal. The journal is the source. The scrub is
  the question.
- **The Playground** has drag-drop. The user drags cells.
  The cells are the substrate. The drag is the LINK.
- **The 5 apps** are working tools. The user uses the
  tools. The tools are the substrate. The use is the
  test.
- **The Boundaries** are the chart. The user reads the
  chart. The chart is the cowboy. The read is the ride.

The web is the dock. The web pages are the openers. The
opener is the user.

## The cowboy rides

The cowboy's loop, fully extended:

```
read dashboard
  ↓
add tasks
  ↓
kick off workers (background)
  ↓
read worklog
  ↓
integrate results
  ↓
commit and push
  ↓
find one thing to improve
  ↓
ask the API
  ↓
apply, test, commit
  ↓
(repeat)
```

The cowboy rides. The boat grows. The wind grows. The
chart grows. The cowboy grows. The wind carries the boat
further. The boat carries the cowboy further. The chart
charts the boat.

The substrate is a closed inversive monoid under the 5
opcodes. The methods that fall out of the monoid are the
ropes the cowboy uses. The APIs are the wind. The cowboy
rides.

— The Cowboy
